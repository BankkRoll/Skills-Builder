# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 1.3 Changelog

## 1.3.25

no release date

### orm

- Fixed issue in [Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects) when used with persistent
  objects which would fail to track the primary key of mappings where the
  column name of the primary key were different than the attribute name.
  References: [#6392](https://www.sqlalchemy.org/trac/ticket/6392)

### schema

- The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object now raises an informative error message if
  it is instantiated without passing at least the [Table.name](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.name)
  and [Table.metadata](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.metadata) arguments positionally. Previously, if
  these were passed as keyword arguments, the object would silently fail to
  initialize correctly.
  References: [#6135](https://www.sqlalchemy.org/trac/ticket/6135)

### postgresql

- Fixed regression caused by [#6023](https://www.sqlalchemy.org/trac/ticket/6023) where the PostgreSQL cast
  operator applied to elements within an [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) when using
  psycopg2 would fail to use the correct type in the case that the datatype
  were also embedded within an instance of the [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant)
  adapter.
  Additionally, repairs support for the correct CREATE TYPE to be emitted
  when using a `Variant(ARRAY(some_schema_type))`.
  References: [#6182](https://www.sqlalchemy.org/trac/ticket/6182)

### mysql

- Fixes to accommodate for the MariaDB 10.6 series, including backwards
  incompatible changes in both the mariadb-connector Python driver (supported
  on SQLAlchemy 1.4 only) as well as the native 10.6 client libraries that
  are used automatically by the mysqlclient DBAPI (applies to both 1.3 and
  1.4). The “utf8mb3” encoding symbol is now reported by these client
  libraries when the encoding is stated as “utf8”, leading to lookup and
  encoding errors within the MySQL dialect that does not expect this symbol.
  Updates to both the MySQL base library to accommodate for this utf8mb3
  symbol being reported as well as to the test suite. Thanks to Georg Richter
  for support.
  References: [#7115](https://www.sqlalchemy.org/trac/ticket/7115), [#7136](https://www.sqlalchemy.org/trac/ticket/7136)

### sqlite

- Add note regarding encryption-related pragmas for pysqlcipher passed in the
  url.
  References: [#6589](https://www.sqlalchemy.org/trac/ticket/6589)

## 1.3.24

Released: March 30, 2021

### orm

- Removed very old warning that states that passive_deletes is not intended
  for many-to-one relationships. While it is likely that in many cases
  placing this parameter on a many-to-one relationship is not what was
  intended, there are use cases where delete cascade may want to be
  disallowed following from such a relationship.
  References: [#5983](https://www.sqlalchemy.org/trac/ticket/5983)
- Fixed issue where the process of joining two tables could fail if one of
  the tables had an unrelated, unresolvable foreign key constraint which
  would raise [NoReferenceError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoReferenceError) within the join process, which
  nonetheless could be bypassed to allow the join to complete. The logic
  which tested the exception for significance within the process would make
  assumptions about the construct which would fail.
  References: [#5952](https://www.sqlalchemy.org/trac/ticket/5952)
- Fixed issue where the [MutableComposite](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableComposite) construct could be
  placed into an invalid state when the parent object was already loaded, and
  then covered by a subsequent query, due to the composite properties’
  refresh handler replacing the object with a new one not handled by the
  mutable extension.
  References: [#6001](https://www.sqlalchemy.org/trac/ticket/6001)

### engine

- Fixed bug where the “schema_translate_map” feature failed to be taken into
  account for the use case of direct execution of
  [DefaultGenerator](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultGenerator) objects such as sequences, which included
  the case where they were “pre-executed” in order to generate primary key
  values when implicit_returning was disabled.
  References: [#5929](https://www.sqlalchemy.org/trac/ticket/5929)

### schema

- Fixed bug first introduced in as some combination of [#2892](https://www.sqlalchemy.org/trac/ticket/2892),
  [#2919](https://www.sqlalchemy.org/trac/ticket/2919) nnd [#3832](https://www.sqlalchemy.org/trac/ticket/3832) where the attachment events for a
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) would be doubled up against the “impl” class,
  if the “impl” were also a [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType). The real-world case
  is any [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) against [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) or
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) would get a doubled
  [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) when the `create_constraint=True` flag
  is set.
  References: [#6152](https://www.sqlalchemy.org/trac/ticket/6152)
- Fixed issue where the CHECK constraint generated by [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
  or [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) would fail to render the naming convention
  correctly after the first compilation, due to an unintended change of state
  within the name given to the constraint. This issue was first introduced in
  0.9 in the fix for issue #3067, and the fix revises the approach taken at
  that time which appears to have been more involved than what was needed.
  References: [#6007](https://www.sqlalchemy.org/trac/ticket/6007)
- Repaired / implemented support for primary key constraint naming
  conventions that use column names/keys/etc as part of the convention. In
  particular, this includes that the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) object
  that’s automatically associated with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) will update
  its name as new primary key [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are added to
  the table and then to the constraint. Internal failure modes related to
  this constraint construction process including no columns present, no name
  present or blank name present are now accommodated.
  References: [#5919](https://www.sqlalchemy.org/trac/ticket/5919)
- Adjusted the logic that emits DROP statements for [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)
  objects among the dropping of multiple tables, such that all
  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) objects are dropped after all tables, even if the
  given [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) is related only to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  object and not directly to the overall [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object.
  The use case supports the same [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) being associated
  with more than one [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) at a time.
  References: [#6071](https://www.sqlalchemy.org/trac/ticket/6071)

### postgresql

- Fixed issue where using [aggregate_order_by](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by) would
  return ARRAY(NullType) under certain conditions, interfering with
  the ability of the result object to return data correctly.
  References: [#5989](https://www.sqlalchemy.org/trac/ticket/5989)
- Fixed issue in PostgreSQL reflection where a column expressing “NOT NULL”
  will supersede the nullability of a corresponding domain.
  References: [#6161](https://www.sqlalchemy.org/trac/ticket/6161)
- Adjusted the psycopg2 dialect to emit an explicit PostgreSQL-style cast for
  bound parameters that contain ARRAY elements. This allows the full range of
  datatypes to function correctly within arrays. The asyncpg dialect already
  generated these internal casts in the final statement. This also includes
  support for array slice updates as well as the PostgreSQL-specific
  `ARRAY.contains()` method.
  References: [#6023](https://www.sqlalchemy.org/trac/ticket/6023)

### mssql

- Fixed issue regarding SQL Server reflection for older SQL Server 2005
  version, a call to sp_columns would not proceed correctly without being
  prefixed with the EXEC keyword. This method is not used in current 1.4
  series.
  References: [#5921](https://www.sqlalchemy.org/trac/ticket/5921)

## 1.3.23

Released: February 1, 2021

### sql

- Fixed bug where making use of the [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method
  on a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) type would fail to take into account the
  dialect-specific mappings in use, due to a rule in [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  that was instead attempting to check for chains of [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  instances.
  References: [#5816](https://www.sqlalchemy.org/trac/ticket/5816)

### postgresql

- For SQLAlchemy 1.3 only, setup.py pins pg8000 to a version lower than
  1.16.6. Version 1.16.6 and above is supported by SQLAlchemy 1.4. Pull
  request courtesy Giuseppe Lumia.
  References: [#5645](https://www.sqlalchemy.org/trac/ticket/5645)
- Fixed issue where using [Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) (called
  [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) in 1.3) in conjunction with a PostgreSQL
  [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) that made use of ad-hoc column
  expressions would fail to copy correctly.
  References: [#5850](https://www.sqlalchemy.org/trac/ticket/5850)

### mysql

- Casting to `FLOAT` is now supported in MySQL >= (8, 0, 17) and
  MariaDb >= (10, 4, 5).
  References: [#5808](https://www.sqlalchemy.org/trac/ticket/5808)
- Fixed bug where MySQL server default reflection would fail for numeric
  values with a negation symbol present.
  References: [#5860](https://www.sqlalchemy.org/trac/ticket/5860)
- Fixed long-lived bug in MySQL dialect where the maximum identifier length
  of 255 was too long for names of all types of constraints, not just
  indexes, all of which have a size limit of 64. As metadata naming
  conventions can create too-long names in this area, apply the limit to the
  identifier generator within the DDL compiler.
  References: [#5898](https://www.sqlalchemy.org/trac/ticket/5898)
- Fixed deprecation warnings that arose as a result of the release of PyMySQL
  1.0, including deprecation warnings for the “db” and “passwd” parameters
  now replaced with “database” and “password”.
  References: [#5821](https://www.sqlalchemy.org/trac/ticket/5821)
- Fixed regression from SQLAlchemy 1.3.20 caused by the fix for
  [#5462](https://www.sqlalchemy.org/trac/ticket/5462) which adds double-parenthesis for MySQL functional
  expressions in indexes, as is required by the backend, this inadvertently
  extended to include arbitrary [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) expressions as well as
  Alembic’s internal textual component,  which are required by Alembic for
  arbitrary index expressions which don’t imply double parenthesis.  The
  check has been narrowed to include only binary/ unary/functional
  expressions directly.
  References: [#5800](https://www.sqlalchemy.org/trac/ticket/5800)

### oracle

- Fixed regression in Oracle dialect introduced by [#4894](https://www.sqlalchemy.org/trac/ticket/4894) in
  SQLAlchemy 1.3.11 where use of a SQL expression in RETURNING for an UPDATE
  would fail to compile, due to a check for “server_default” when an
  arbitrary SQL expression is not a column.
  References: [#5813](https://www.sqlalchemy.org/trac/ticket/5813)
- Fixed bug in Oracle dialect where retrieving a CLOB/BLOB column via
  [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) would fail as the LOB value would need to be
  read when returned; additionally, repaired support for retrieval of Unicode
  values via RETURNING under Python 2.
  References: [#5812](https://www.sqlalchemy.org/trac/ticket/5812)

### misc

- Fixed issue where the stringification that is sometimes called when
  attempting to generate the “key” for the `.c` collection on a selectable
  would fail if the column were an unlabeled custom SQL construct using the
  `sqlalchemy.ext.compiler` extension, and did not provide a default
  compilation form; while this seems like an unusual case, it can get invoked
  for some ORM scenarios such as when the expression is used in an “order by”
  in combination with joined eager loading.  The issue is that the lack of a
  default compiler function was raising [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) and not
  [UnsupportedCompilationError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnsupportedCompilationError).
  References: [#5836](https://www.sqlalchemy.org/trac/ticket/5836)

## 1.3.22

Released: December 18, 2020

### oracle

- Fixed regression which occurred due to [#5755](https://www.sqlalchemy.org/trac/ticket/5755) which implemented
  isolation level support for Oracle.   It has been reported that many Oracle
  accounts don’t actually have permission to query the `v$transaction`
  view so this feature has been altered to gracefully fallback when it fails
  upon database connect, where the dialect will assume “READ COMMITTED” is
  the default isolation level as was the case prior to SQLAlchemy 1.3.21.
  However, explicit use of the [Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
  method must now necessarily raise an exception, as Oracle databases with
  this restriction explicitly disallow the user from reading the current
  isolation level.
  References: [#5784](https://www.sqlalchemy.org/trac/ticket/5784)

## 1.3.21

Released: December 17, 2020

### orm

- Added a comprehensive check and an informative error message for the case
  where a mapped class, or a string mapped class name, is passed to
  [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary).  This is an extremely common error
  which warrants a clear message.
  Additionally, added a new rule to the class registry resolution such that
  with regards to the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter, if a
  mapped class and its table are of the identical string name, the
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) will be favored when resolving this parameter.   In all
  other cases, the class continues to be favored if a class and table
  share the identical name.
  References: [#5774](https://www.sqlalchemy.org/trac/ticket/5774)
- Fixed bug in [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) where objects in the
  `_ormsession.Session` that were already expired would be
  unnecessarily SELECTed individually when they were refreshed by the
  “evaluate”synchronize strategy.
  References: [#5664](https://www.sqlalchemy.org/trac/ticket/5664)
- Fixed bug involving the `restore_load_context` option of ORM events such
  as [InstanceEvents.load()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.load) such that the flag would not be
  carried along to subclasses which were mapped after the event handler were
  first established.
  References: [#5737](https://www.sqlalchemy.org/trac/ticket/5737)

### sql

- A warning is emitted if a returning() method such as
  [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) is called multiple times, as this does not
  yet support additive operation.  Version 1.4 will support additive
  operation for this.  Additionally, any combination of the
  [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) and `ValuesBase.return_defaults()`
  methods now raises an error as these methods are mutually exclusive;
  previously the operation would fail silently.
  References: [#5691](https://www.sqlalchemy.org/trac/ticket/5691)
- Fixed structural compiler issue where some constructs such as MySQL /
  PostgreSQL “on conflict / on duplicate key” would rely upon the state of
  the `Compiler` object being fixed against their statement as
  the top level statement, which would fail in cases where those statements
  are branched from a different context, such as a DDL construct linked to a
  SQL statement.
  References: [#5656](https://www.sqlalchemy.org/trac/ticket/5656)

### postgresql

- Added new parameter [ExcludeConstraint.ops](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.ops) to the
  [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) object, to support operator class
  specification with this constraint.  Pull request courtesy Alon Menczer.
  References: [#5604](https://www.sqlalchemy.org/trac/ticket/5604)
- Fixed regression introduced in 1.3.2 for the PostgreSQL dialect, also
  copied out to the MySQL dialect’s feature in 1.3.18, where usage of a non
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct such as [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) as the argument
  to [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of) would fail to be accommodated
  correctly within the PostgreSQL or MySQL compilers.
  References: [#5729](https://www.sqlalchemy.org/trac/ticket/5729)

### mysql

- Fixed issue where reflecting a server default on MariaDB only that
  contained a decimal point in the value would fail to be reflected
  correctly, leading towards a reflected table that lacked any server
  default.
  References: [#5744](https://www.sqlalchemy.org/trac/ticket/5744)
- Added missing keywords to the `RESERVED_WORDS` list for the MySQL
  dialect: `action`, `level`, `mode`, `status`, `text`, `time`.
  Pull request courtesy Oscar Batori.
  References: [#5696](https://www.sqlalchemy.org/trac/ticket/5696)

### sqlite

- Added `sqlite_with_rowid=False` dialect keyword to enable creating
  tables as `CREATE TABLE … WITHOUT ROWID`. Patch courtesy Sean Anderson.
  References: [#5685](https://www.sqlalchemy.org/trac/ticket/5685)

### mssql

- Fixed bug where a CREATE INDEX statement was rendered incorrectly when
  both `mssql-include` and `mssql_where` were specified. Pull request
  courtesy @Adiorz.
  References: [#5751](https://www.sqlalchemy.org/trac/ticket/5751)
- Added SQL Server code “01000” to the list of disconnect codes.
  References: [#5646](https://www.sqlalchemy.org/trac/ticket/5646)
- Fixed issue with composite primary key columns not being reported
  in the correct order. Patch courtesy @fulpm.
  References: [#5661](https://www.sqlalchemy.org/trac/ticket/5661)

### oracle

- Implemented support for the SERIALIZABLE isolation level for Oracle
  databases, as well as a real implementation for
  [Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level).
  See also
  [Transaction Isolation Level / Autocommit](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-isolation-level)
  References: [#5755](https://www.sqlalchemy.org/trac/ticket/5755)

## 1.3.20

Released: October 12, 2020

### orm

- An [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) with more detail is now raised if the target
  parameter for [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) is set to an unmapped object.
  Prior to this change a less detailed `AttributeError` was raised.
  Pull request courtesy Ramon Williams.
  References: [#4428](https://www.sqlalchemy.org/trac/ticket/4428)
- Fixed issue where using a loader option against a string attribute name
  that is not actually a mapped attribute, such as a plain Python descriptor,
  would raise an uninformative AttributeError;  a descriptive error is now
  raised.
  References: [#4589](https://www.sqlalchemy.org/trac/ticket/4589)

### engine

- Fixed issue where a non-string object sent to
  [SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError) or a subclass, as occurs with some third
  party dialects, would fail to stringify correctly. Pull request
  courtesy Andrzej Bartosiński.
  References: [#5599](https://www.sqlalchemy.org/trac/ticket/5599)
- Repaired a function-level import that was not using SQLAlchemy’s standard
  late-import system within the sqlalchemy.exc module.
  References: [#5632](https://www.sqlalchemy.org/trac/ticket/5632)

### sql

- Fixed issue where the `pickle.dumps()` operation against
  [Over](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Over) construct would produce a recursion overflow.
  References: [#5644](https://www.sqlalchemy.org/trac/ticket/5644)
- Fixed bug where an error was not raised in the case where a
  [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) were added to more than one [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table) at a
  time.  This raised correctly for the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects. An [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is now
  raised when this occurs.
  References: [#5618](https://www.sqlalchemy.org/trac/ticket/5618)

### postgresql

- The psycopg2 dialect now support PostgreSQL multiple host connections, by
  passing host/port combinations to the query string. Pull request courtesy
  Ramon Williams.
  See also
  [Specifying multiple fallback hosts](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#psycopg2-multi-host)
  References: [#4392](https://www.sqlalchemy.org/trac/ticket/4392)
- Adjusted the [Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any) and
  [Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all) methods to implement a straight “NOT”
  operation for negation, rather than negating the comparison operator.
  References: [#5518](https://www.sqlalchemy.org/trac/ticket/5518)
- Fixed issue where the [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) type would not consult the
  schema translate map when emitting a CREATE TYPE or DROP TYPE during the
  test to see if the type exists or not.  Additionally, repaired an issue
  where if the same enum were encountered multiple times in a single DDL
  sequence, the “check” query would run repeatedly rather than relying upon a
  cached value.
  References: [#5520](https://www.sqlalchemy.org/trac/ticket/5520)

### mysql

- Adjusted the MySQL dialect to correctly parenthesize functional index
  expressions as accepted by MySQL 8. Pull request courtesy Ramon Williams.
  References: [#5462](https://www.sqlalchemy.org/trac/ticket/5462)
- Add new MySQL reserved words: `cube`, `lateral` added in MySQL 8.0.1
  and 8.0.14, respectively; this indicates that these terms will be quoted if
  used as table or column identifier names.
  References: [#5539](https://www.sqlalchemy.org/trac/ticket/5539)
- The “skip_locked” keyword used with `with_for_update()` will emit a
  warning when used on MariaDB backends, and will then be ignored.   This is
  a deprecated behavior that will raise in SQLAlchemy 1.4, as an application
  that requests “skip locked” is looking for a non-blocking operation which
  is not available on those backends.
  References: [#5568](https://www.sqlalchemy.org/trac/ticket/5568)
- Fixed bug where an UPDATE statement against a JOIN using MySQL multi-table
  format would fail to include the table prefix for the target table if the
  statement had no WHERE clause, as only the WHERE clause were scanned to
  detect a “multi table update” at that particular point.  The target
  is now also scanned if it’s a JOIN to get the leftmost table as the
  primary table and the additional entries as additional FROM entries.
  References: [#5617](https://www.sqlalchemy.org/trac/ticket/5617)

### mssql

- Fixed issue where a SQLAlchemy connection URI for Azure DW with
  `authentication=ActiveDirectoryIntegrated` (and no username+password)
  was not constructing the ODBC connection string in a way that was
  acceptable to the Azure DW instance.
  References: [#5592](https://www.sqlalchemy.org/trac/ticket/5592)

### tests

- Fixed incompatibilities in the test suite when running against Pytest 6.x.
  References: [#5635](https://www.sqlalchemy.org/trac/ticket/5635)

### misc

- Fixed issue where the following pool parameters were not being propagated
  to the new pool created when [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) were called:
  `pre_ping`, `use_lifo`.  Additionally the `recycle` and
  `reset_on_return` parameter is now propagated for the
  `AssertionPool` class.
  References: [#5582](https://www.sqlalchemy.org/trac/ticket/5582)
- An informative error is now raised when attempting to use an association
  proxy element as a plain column expression to be SELECTed from or used in a
  SQL function; this use case is not currently supported.
  References: [#5541](https://www.sqlalchemy.org/trac/ticket/5541), [#5542](https://www.sqlalchemy.org/trac/ticket/5542)

## 1.3.19

Released: August 17, 2020

### orm

- Adjusted the workings of the [Mapper.all_orm_descriptors()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)
  accessor to represent the attributes in the order that they are located in
  a deterministic way, assuming the use of Python 3.6 or higher which
  maintains the sorting order of class attributes based on how they were
  declared.   This sorting is not guaranteed to match the declared order of
  attributes in all cases however; see the method documentation for the exact
  scheme.
  References: [#5494](https://www.sqlalchemy.org/trac/ticket/5494)

### orm declarative

- The name of the virtual column used when using the
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) and
  [ConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.ConcreteBase) classes can now be customized, to allow
  for models that have a column that is actually named `type`.  Pull
  request courtesy Jesse-Bakker.
  References: [#5513](https://www.sqlalchemy.org/trac/ticket/5513)

### sql

- Repaired an issue where the “ORDER BY” clause rendering a label name rather
  than a complete expression, which is particularly important for SQL Server,
  would fail to occur if the expression were enclosed in a parenthesized
  grouping in some cases.   This case has been added to test support. The
  change additionally adjusts the “automatically add ORDER BY columns when
  DISTINCT is present” behavior of ORM query, deprecated in 1.4, to more
  accurately detect column expressions that are already present.
  References: [#5470](https://www.sqlalchemy.org/trac/ticket/5470)
- The `LookupError` message will now provide the user with up to four
  possible values that a column is constrained to via the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum).
  Values longer than 11 characters will be truncated and replaced with
  ellipses. Pull request courtesy Ramon Williams.
  References: [#4733](https://www.sqlalchemy.org/trac/ticket/4733)
- Fixed issue where the
  [Connection.execution_options.schema_translate_map](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.schema_translate_map)
  feature would not take effect when the [Sequence.next_value()](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.next_value)
  function function for a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) were used in the
  [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) parameter and the create table
  DDL were emitted.
  References: [#5500](https://www.sqlalchemy.org/trac/ticket/5500)

### postgresql

- Fixed issue where the return type for the various RANGE comparison
  operators would itself be the same RANGE type rather than BOOLEAN, which
  would cause an undesirable result in the case that a
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) that defined result-processing behavior were in
  use.  Pull request courtesy Jim Bosch.
  References: [#5476](https://www.sqlalchemy.org/trac/ticket/5476)

### mysql

- The MySQL dialect will render FROM DUAL for a SELECT statement that has no
  FROM clause but has a WHERE clause. This allows things like “SELECT 1 WHERE
  EXISTS (subquery)” kinds of queries to be used as well as other use cases.
  References: [#5481](https://www.sqlalchemy.org/trac/ticket/5481)
- Fixed an issue where CREATE TABLE statements were not specifying the
  COLLATE keyword correctly.
  References: [#5411](https://www.sqlalchemy.org/trac/ticket/5411)
- Added MariaDB code 1927 to the list of “disconnect” codes, as recent
  MariaDB versions apparently use this code when the database server was
  stopped.
  References: [#5493](https://www.sqlalchemy.org/trac/ticket/5493)

### sqlite

- Applied a sweep through all included dialects to ensure names that contain
  single or double quotes are properly escaped when querying system tables,
  for all [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) methods that accept object names as an argument
  (e.g. table names, view names, etc).   SQLite and MSSQL contained two
  quoting issues that were repaired.
  References: [#5456](https://www.sqlalchemy.org/trac/ticket/5456)

### mssql

- Fixed bug where the mssql dialect incorrectly escaped object names that
  contained ‘]’ character(s).
  References: [#5467](https://www.sqlalchemy.org/trac/ticket/5467)

### misc

- Added a `**kw` argument to the `DeclarativeMeta.__init__()` method.
  This allows a class to support the [PEP 487](https://peps.python.org/pep-0487/) metaclass hook
  `__init_subclass__`.  Pull request courtesy Ewen Gillies.
  References: [##5357](https://www.sqlalchemy.org/trac/ticket/#5357)

## 1.3.18

Released: June 25, 2020

### orm

- Improve error message when using [Query.filter_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter_by) in
  a query where the first entity is not a mapped class.
  References: [#5326](https://www.sqlalchemy.org/trac/ticket/5326)
- Added a new parameter [query_expression.default_expr](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression.params.default_expr) to the
  [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression) construct, which will be appled to queries
  automatically if the [with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) option is not used. Pull
  request courtesy Haoyu Sun.
  References: [#5198](https://www.sqlalchemy.org/trac/ticket/5198)

### examples

- Added new option `--raw` to the examples.performance suite
  which will dump the raw profile test for consumption by any
  number of profiling visualizer tools.   Removed the “runsnake”
  option as runsnake is very hard to build at this point;

### engine

- Further refinements to the fixes to the “reset” agent fixed in
  [#5326](https://www.sqlalchemy.org/trac/ticket/5326), which now emits a warning when it is not being correctly
  invoked and corrects for the behavior.  Additional scenarios have been
  identified and fixed where this warning was being emitted.
  References: [#5326](https://www.sqlalchemy.org/trac/ticket/5326)
- Fixed issue in [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object where stringifying the object
  would not URL encode special characters, preventing the URL from being
  re-consumable as a real URL.  Pull request courtesy Miguel Grinberg.
  References: [#5341](https://www.sqlalchemy.org/trac/ticket/5341)

### sql

- Added a “.schema” parameter to the [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table) construct,
  allowing ad-hoc table expressions to also include a schema name.
  Pull request courtesy Dylan Modesitt.
  References: [#5309](https://www.sqlalchemy.org/trac/ticket/5309)
- Added `.offset` support to sybase dialect.
  Pull request courtesy Alan D. Snow.
  References: [#5294](https://www.sqlalchemy.org/trac/ticket/5294)
- Correctly apply self_group in type_coerce element.
  The type coerce element did not correctly apply grouping rules when using
  in an expression
  References: [#5344](https://www.sqlalchemy.org/trac/ticket/5344)
- Added [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) output to the generic SQL string that is
  produced when calling `str()` on a statement.  Previously, this clause
  would be omitted under the assumption that it was dialect specific.
  The hint text is presented within brackets to indicate the rendering
  of such hints varies among backends.
  References: [#5353](https://www.sqlalchemy.org/trac/ticket/5353)
- Introduce `IdentityOptions` to store common parameters for
  sequences and identity columns.
  References: [#5324](https://www.sqlalchemy.org/trac/ticket/5324)

### schema

- Fixed issue where `dialect_options` were omitted when a
  database object (e.g., [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)) was copied using
  `tometadata()`.
  References: [#5276](https://www.sqlalchemy.org/trac/ticket/5276)

### mysql

- Implemented row-level locking support for mysql.  Pull request courtesy
  Quentin Somerville.
  References: [#4860](https://www.sqlalchemy.org/trac/ticket/4860)

### sqlite

- SQLite 3.31 added support for computed column. This change
  enables their support in SQLAlchemy when targeting SQLite.
  References: [#5297](https://www.sqlalchemy.org/trac/ticket/5297)
- Added “exists” to the list of reserved words for SQLite so that this word
  will be quoted when used as a label or column name. Pull request courtesy
  Thodoris Sotiropoulos.
  References: [#5395](https://www.sqlalchemy.org/trac/ticket/5395)

### mssql

- Moved the `supports_sane_rowcount_returning = False` requirement from
  the `PyODBCConnector` level to the `MSDialect_pyodbc` since pyodbc
  does work properly in some circumstances.
  References: [#5321](https://www.sqlalchemy.org/trac/ticket/5321)
- Refined the logic used by the SQL Server dialect to interpret multi-part
  schema names that contain many dots, to not actually lose any dots if the
  name does not have bracking or quoting used, and additionally to support a
  “dbname” token that has many parts including that it may have multiple,
  independently-bracketed sections.
  References: [#5364](https://www.sqlalchemy.org/trac/ticket/5364), [#5366](https://www.sqlalchemy.org/trac/ticket/5366)
- Fixed an issue in the pyodbc connector such that a warning about pyodbc
  “drivername” would be emitted when using a totally empty URL.  Empty URLs
  are normal when producing a non-connected dialect object or when using the
  “creator” argument to create_engine(). The warning now only emits if the
  driver name is missing but other parameters are still present.
  References: [#5346](https://www.sqlalchemy.org/trac/ticket/5346)
- Fixed issue with assembling the ODBC connection string for the pyodbc
  DBAPI. Tokens containing semicolons and/or braces “{}” were not being
  correctly escaped, causing the ODBC driver to misinterpret the
  connection string attributes.
  References: [#5373](https://www.sqlalchemy.org/trac/ticket/5373)
- Fixed issue where `datetime.time` parameters were being converted to
  `datetime.datetime`, making them incompatible with comparisons like
  `>=` against an actual [TIME](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.TIME) column.
  References: [#5339](https://www.sqlalchemy.org/trac/ticket/5339)
- Fixed an issue where the `is_disconnect` function in the SQL Server
  pyodbc dialect was incorrectly reporting the disconnect state when the
  exception message had a substring that matched a SQL Server ODBC error
  code.
  References: [#5359](https://www.sqlalchemy.org/trac/ticket/5359)

### oracle

- Fixed bug in Oracle dialect where indexes that contain the full set of
  primary key columns would be mistaken as the primary key index itself,
  which is omitted, even if there were multiples.  The check has been refined
  to compare the name of the primary key constraint against the index name
  itself, rather than trying to guess based on the columns present in the
  index.
  References: [#5421](https://www.sqlalchemy.org/trac/ticket/5421)

## 1.3.17

Released: May 13, 2020

### orm

- Added an accessor [Comparator.expressions](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.Comparator.expressions) which
  provides access to the group of columns mapped under a multi-column
  [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) attribute.
  References: [#5262](https://www.sqlalchemy.org/trac/ticket/5262)
- Introduce [relationship.sync_backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.sync_backref) flag in a relationship
  to control if the synchronization events that mutate the in-Python
  attributes are added. This supersedes the previous change [#5149](https://www.sqlalchemy.org/trac/ticket/5149),
  which warned that `viewonly=True` relationship target of a
  back_populates or backref configuration would be disallowed.
  References: [#5237](https://www.sqlalchemy.org/trac/ticket/5237)
- Fixed bug where using [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) as the target of a join via
  `RelationshipComparator.of_type()` on a mapper that already has a
  subquery-based with_polymorphic setting that’s equivalent to the one
  requested would not correctly alias the ON clause in the join.
  References: [#5288](https://www.sqlalchemy.org/trac/ticket/5288)
- Fixed issue in the area of where loader options such as selectinload()
  interact with the baked query system, such that the caching of a query is
  not supposed to occur if the loader options themselves have elements such
  as with_polymorphic() objects in them that currently are not
  cache-compatible.  The baked loader could sometimes not fully invalidate
  itself in these some of these scenarios leading to missed eager loads.
  References: [#5303](https://www.sqlalchemy.org/trac/ticket/5303)
- Modified the internal “identity set” implementation, which is a set that
  hashes objects on their id() rather than their hash values, to not actually
  call the `__hash__()` method of the objects, which are typically
  user-mapped objects.  Some methods were calling this method as a side
  effect of the implementation.
  References: [#5304](https://www.sqlalchemy.org/trac/ticket/5304)
- An informative error message is raised when an ORM many-to-one comparison
  is attempted against an object that is not an actual mapped instance.
  Comparisons such as those to scalar subqueries aren’t supported;
  generalized comparison with subqueries is better achieved using
  [Comparator.has()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.has).
  References: [#5269](https://www.sqlalchemy.org/trac/ticket/5269)

### engine

- Fixed fairly critical issue where the DBAPI connection could be returned to
  the connection pool while still in an un-rolled-back state. The reset agent
  responsible for rolling back the connection could be corrupted in the case
  that the transaction was “closed” without being rolled back or committed,
  which can occur in some scenarios when using ORM sessions and emitting
  .close() in a certain pattern involving savepoints.   The fix ensures that
  the reset agent is always active.
  References: [#5326](https://www.sqlalchemy.org/trac/ticket/5326)

### schema

- Fixed issue where an [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) that is deferred in being associated
  with a table, such as as when it contains a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that is not
  associated with any [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) yet,  would fail to attach correctly if
  it also contained a non table-oriented expression.
  References: [#5298](https://www.sqlalchemy.org/trac/ticket/5298)
- A warning is emitted when making use of the [MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables)
  attribute as well as the [sort_tables()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables) function, and the
  given tables cannot be correctly sorted due to a cyclic dependency between
  foreign key constraints. In this case, the functions will no longer sort
  the involved tables by foreign key, and a warning will be emitted. Other
  tables that are not part of the cycle will still be returned in dependency
  order. Previously, the sorted_table routines would return a collection that
  would unconditionally omit all foreign keys when a cycle was detected, and
  no warning was emitted.
  References: [#5316](https://www.sqlalchemy.org/trac/ticket/5316)
- Add `comment` attribute to [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) `__repr__` method.
  References: [#4138](https://www.sqlalchemy.org/trac/ticket/4138)

### postgresql

- Added support for columns or type [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) of [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum),
  [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) or [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) in PostgreSQL.
  Previously a workaround was required in these use cases.
  References: [#5265](https://www.sqlalchemy.org/trac/ticket/5265)
- Raise an explicit [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) when adding a table with a
  column of type [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) of [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) configured with
  [Enum.native_enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.native_enum) set to `False` when
  [Enum.create_constraint](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.create_constraint) is not set to `False`
  References: [#5266](https://www.sqlalchemy.org/trac/ticket/5266)

### mssql

- Fix a regression introduced by the reflection of computed column in
  MSSQL when using the legacy TDS version 4.2. The dialect will try
  to detect the protocol version of first connect and run in compatibility
  mode if it cannot detect it.
  References: [#5255](https://www.sqlalchemy.org/trac/ticket/5255)
- Fix a regression introduced by the reflection of computed column in
  MSSQL when using SQL server versions before 2012, which does not support
  the `concat` function.
  References: [#5271](https://www.sqlalchemy.org/trac/ticket/5271)

### oracle

- Changed the implementation of fetching CLOB and BLOB objects to use
  cx_Oracle’s native implementation which fetches CLOB/BLOB objects inline
  with other result columns, rather than performing a separate fetch. As
  always, this can be disabled by setting auto_convert_lobs to False.
  As part of this change, the behavior of a CLOB that was given a blank
  string on INSERT now returns None on SELECT, which is now consistent with
  that of VARCHAR on Oracle.
  References: [#5314](https://www.sqlalchemy.org/trac/ticket/5314)
- Some modifications to how the cx_oracle dialect sets up per-column
  outputtype handlers for LOB and numeric datatypes to adjust for potential
  changes coming in cx_Oracle 8.
  References: [#5246](https://www.sqlalchemy.org/trac/ticket/5246)

### misc

- Adjusted dialect loading for `firebird://` URIs so the external
  sqlalchemy-firebird dialect will be used if it has been installed,
  otherwise fall back to the (now deprecated) internal Firebird dialect.
  References: [#5278](https://www.sqlalchemy.org/trac/ticket/5278)

## 1.3.16

Released: April 7, 2020

### orm

- Modified the queries used by subqueryload and selectinload to no longer
  ORDER BY the primary key of the parent entity;  this ordering was there to
  allow the rows as they come in to be copied into lists directly with a
  minimal level of Python-side collation.   However, these ORDER BY clauses
  can negatively impact the performance of the query as in many scenarios
  these columns are derived from a subquery or are otherwise not actual
  primary key columns such that SQL planners cannot make use of indexes. The
  Python-side collation uses the native itertools.group_by() to collate the
  incoming rows, and has been modified to allow multiple
  row-groups-per-parent to be assembled together using list.extend(), which
  should still allow for relatively fast Python-side performance.  There will
  still be an ORDER BY present for a relationship that includes an explicit
  order_by parameter, however this is the only ORDER BY that will be added to
  the query for both kinds of loading.
  References: [#5162](https://www.sqlalchemy.org/trac/ticket/5162)
- Fixed bug in [selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) loading option where two or more
  loaders that represent different relationships with the same string key
  name as referenced from a single [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) construct
  with multiple subclass mappers would fail to invoke each subqueryload
  separately, instead making use of a single string-based slot that would
  prevent the other loaders from being invoked.
  References: [#5228](https://www.sqlalchemy.org/trac/ticket/5228)
- Fixed issue where a lazyload that uses session-local “get” against a target
  many-to-one relationship where an object with the correct primary key is
  present, however it’s an instance of a sibling class, does not correctly
  return None as is the case when the lazy loader actually emits a load for
  that row.
  References: [#5210](https://www.sqlalchemy.org/trac/ticket/5210)

### orm declarative

- The string argument accepted as the first positional argument by the
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function when using the Declarative API is no longer
  interpreted using the Python `eval()` function; instead, the name is dot
  separated and the names are looked up directly in the name resolution
  dictionary without treating the value as a Python expression.  However,
  passing a string argument to the other [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) parameters
  that necessarily must accept Python expressions will still use `eval()`;
  the documentation has been clarified to ensure that there is no ambiguity
  that this is in use.
  See also
  [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) - details on string evaluation
  References: [#5238](https://www.sqlalchemy.org/trac/ticket/5238)

### sql

- Add ability to literal compile a `DateTime`, `Date`
  or `Time` when using the string dialect for debugging purposes.
  This change does not impact real dialect implementation that retain
  their current behavior.
  References: [#5052](https://www.sqlalchemy.org/trac/ticket/5052)

### schema

- Added support for reflection of “computed” columns, which are now returned
  as part of the structure returned by [Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns).
  When reflecting full [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, computed columns will
  be represented using the [Computed](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Computed) construct.
  References: [#5063](https://www.sqlalchemy.org/trac/ticket/5063)

### postgresql

- Fixed issue where a “covering” index, e.g. those which have an  INCLUDE
  clause, would be reflected including all the columns in INCLUDE clause as
  regular columns.  A warning is now emitted if these additional columns are
  detected indicating that they are currently ignored.  Note that full
  support for “covering” indexes is part of [#4458](https://www.sqlalchemy.org/trac/ticket/4458).  Pull request
  courtesy Marat Sharafutdinov.
  References: [#5205](https://www.sqlalchemy.org/trac/ticket/5205)

### mysql

- Fixed issue in MySQL dialect when connecting to a pseudo-MySQL database
  such as that provided by ProxySQL, the up front check for isolation level
  when it returns no row will not prevent the dialect from continuing to
  connect. A warning is emitted that the isolation level could not be
  detected.
  References: [#5239](https://www.sqlalchemy.org/trac/ticket/5239)

### sqlite

- Implemented AUTOCOMMIT isolation level for SQLite when using pysqlite.
  References: [#5164](https://www.sqlalchemy.org/trac/ticket/5164)

### mssql

- Added support for [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) and
  [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) to SQL Server,
  MySQL, and Oracle.
  References: [#5137](https://www.sqlalchemy.org/trac/ticket/5137)

### oracle

- Implemented AUTOCOMMIT isolation level for Oracle when using cx_Oracle.
  Also added a fixed default isolation level of READ COMMITTED for Oracle.
  References: [#5200](https://www.sqlalchemy.org/trac/ticket/5200)
- Fixed regression / incorrect fix caused by fix for [#5146](https://www.sqlalchemy.org/trac/ticket/5146) where the
  Oracle dialect reads from the “all_tab_comments” view to get table comments
  but fails to accommodate for the current owner of the table being
  requested, causing it to read the wrong comment if multiple tables of the
  same name exist in multiple schemas.
  References: [#5146](https://www.sqlalchemy.org/trac/ticket/5146)

### tests

- Fixed an issue that prevented the test suite from running with the
  recently released py.test 5.4.0.
  References: [#5201](https://www.sqlalchemy.org/trac/ticket/5201)

### misc

- The [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type now supports the parameter [Enum.length](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.length)
  to specify the length of the VARCHAR column to create when using
  non native enums by setting [Enum.native_enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.native_enum) to `False`
  References: [#5183](https://www.sqlalchemy.org/trac/ticket/5183)
- Ensured that the “pyproject.toml” file is not included in builds, as the
  presence of this file indicates to pip that a pep-517 installation process
  should be used.  As this mode of operation appears to be not well supported
  by current tools / distros, these problems are avoided within the scope
  of SQLAlchemy installation by omitting the file.
  References: [#5207](https://www.sqlalchemy.org/trac/ticket/5207)

## 1.3.15

Released: March 11, 2020

### orm

- Adjusted the error message emitted by [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) when a left hand
  side can’t be located that the [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method is the
  best way to resolve the issue.  Also, within the 1.3 series, used a
  deterministic ordering when determining the FROM clause from a given column
  entity passed to [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) so that the same expression is determined
  each time.
  References: [#5194](https://www.sqlalchemy.org/trac/ticket/5194)
- Fixed regression in 1.3.14 due to [#4849](https://www.sqlalchemy.org/trac/ticket/4849) where a sys.exc_info()
  call failed to be invoked correctly when a flush error would occur. Test
  coverage has been added for this exception case.
  References: [#5196](https://www.sqlalchemy.org/trac/ticket/5196)

## 1.3.14

Released: March 10, 2020

### general

- Applied an explicit “cause” to most if not all internally raised exceptions
  that are raised from within an internal exception catch, to avoid
  misleading stacktraces that suggest an error within the handling of an
  exception.  While it would be preferable to suppress the internally caught
  exception in the way that the `__suppress_context__` attribute would,
  there does not as yet seem to be a way to do this without suppressing an
  enclosing user constructed context, so for now it exposes the internally
  caught exception as the cause so that full information about the context
  of the error is maintained.
  References: [#4849](https://www.sqlalchemy.org/trac/ticket/4849)

### orm

- Added a new flag [InstanceEvents.restore_load_context](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.params.restore_load_context) and
  [SessionEvents.restore_load_context](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.params.restore_load_context) which apply to the
  [InstanceEvents.load()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.load), [InstanceEvents.refresh()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh), and
  [SessionEvents.loaded_as_persistent()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.loaded_as_persistent) events, which when set will
  restore the “load context” of the object after the event hook has been
  called.  This ensures that the object remains within the “loader context”
  of the load operation that is already ongoing, rather than the object being
  transferred to a new load context due to refresh operations which may have
  occurred in the event. A warning is now emitted when this condition occurs,
  which recommends use of the flag to resolve this case.  The flag is
  “opt-in” so that there is no risk introduced to existing applications.
  The change additionally adds support for the `raw=True` flag to
  session lifecycle events.
  References: [#5129](https://www.sqlalchemy.org/trac/ticket/5129)
- Fixed regression caused in 1.3.13 by [#5056](https://www.sqlalchemy.org/trac/ticket/5056) where a refactor of the
  ORM path registry system made it such that a path could no longer be
  compared to an empty tuple, which can occur in a particular kind of joined
  eager loading path.   The “empty tuple” use case has been resolved so that
  the path registry is compared to a path registry in all cases;  the
  `PathRegistry` object itself now implements `__eq__()` and
  `__ne__()` methods which will take place for all equality comparisons and
  continue to succeed in the not anticipated case that a non-
  `PathRegistry` object is compared, while emitting a warning that
  this object should not be the subject of the comparison.
  References: [#5110](https://www.sqlalchemy.org/trac/ticket/5110)
- Setting a relationship to viewonly=True which is also the target of a
  back_populates or backref configuration will now emit a warning and
  eventually be disallowed. back_populates refers specifically to mutation
  of an attribute or collection, which is disallowed when the attribute is
  subject to viewonly=True.   The viewonly attribute is not subject to
  persistence behaviors which means it will not reflect correct results
  when it is locally mutated.
  References: [#5149](https://www.sqlalchemy.org/trac/ticket/5149)
- Fixed an additional regression in the same area as that of [#5080](https://www.sqlalchemy.org/trac/ticket/5080)
  introduced in 1.3.0b3 via [#4468](https://www.sqlalchemy.org/trac/ticket/4468) where the ability to create a
  joined option across a [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) into a relationship
  against the base class of that with_polymorphic, and then further into
  regular mapped relationships would fail as the base class component would
  not add itself to the load path in a way that could be located by the
  loader strategy. The changes applied in [#5080](https://www.sqlalchemy.org/trac/ticket/5080) have been further
  refined to also accommodate this scenario.
  References: [#5121](https://www.sqlalchemy.org/trac/ticket/5121)

### engine

- Expanded the scope of cursor/connection cleanup when a statement is
  executed to include when the result object fails to be constructed, or an
  after_cursor_execute() event raises an error, or autocommit / autoclose
  fails.  This allows the DBAPI cursor to be cleaned up on failure and for
  connectionless execution allows the connection to be closed out and
  returned to the connection pool, where previously it waiting until garbage
  collection would trigger a pool return.
  References: [#5182](https://www.sqlalchemy.org/trac/ticket/5182)

### sql

- Fixed bug where a CTE of an INSERT/UPDATE/DELETE that also uses RETURNING
  could then not be SELECTed from directly, as the internal state of the
  compiler would try to treat the outer SELECT as a DELETE statement itself
  and access nonexistent state.
  References: [#5181](https://www.sqlalchemy.org/trac/ticket/5181)

### postgresql

- Fixed issue where the “schema_translate_map” feature would not work with a
  PostgreSQL native enumeration type (i.e. [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum),
  [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM)) in that while the “CREATE TYPE” statement would
  be emitted with the correct schema, the schema would not be rendered in
  the CREATE TABLE statement at the point at which the enumeration was
  referenced.
  References: [#5158](https://www.sqlalchemy.org/trac/ticket/5158)
- Fixed bug where PostgreSQL reflection of CHECK constraints would fail to
  parse the constraint if the SQL text contained newline characters. The
  regular expression has been adjusted to accommodate for this case. Pull
  request courtesy Eric Borczuk.
  References: [#5170](https://www.sqlalchemy.org/trac/ticket/5170)

### mysql

- Fixed issue in MySQL [Insert.on_duplicate_key_update()](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.Insert.on_duplicate_key_update) construct
  where using a SQL function or other composed expression for a column argument
  would not properly render the `VALUES` keyword surrounding the column
  itself.
  References: [#5173](https://www.sqlalchemy.org/trac/ticket/5173)

### mssql

- Fixed issue where the [DATETIMEOFFSET](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.DATETIMEOFFSET) type would not
  accommodate for the `None` value, introduced as part of the series of
  fixes for this type first introduced in [#4983](https://www.sqlalchemy.org/trac/ticket/4983), [#5045](https://www.sqlalchemy.org/trac/ticket/5045).
  Additionally, added support for passing a backend-specific date formatted
  string through this type, as is typically allowed for date/time types on
  most other DBAPIs.
  References: [#5132](https://www.sqlalchemy.org/trac/ticket/5132)

### oracle

- Fixed a reflection bug where table comments could only be retrieved for
  tables actually owned by the user but not for tables visible to the user
  but owned by someone else.  Pull request courtesy Dave Hirschfeld.
  References: [#5146](https://www.sqlalchemy.org/trac/ticket/5146)

### misc

- Added keyword arguments to the [MutableList.sort()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList.sort) function so that a
  key function as well as the “reverse” keyword argument can be provided.
  References: [#5114](https://www.sqlalchemy.org/trac/ticket/5114)
- Revised an internal change to the test system added as a result of
  [#5085](https://www.sqlalchemy.org/trac/ticket/5085) where a testing-related module per dialect would be loaded
  unconditionally upon making use of that dialect, pulling in SQLAlchemy’s
  testing framework as well as the ORM into the module import space.   This
  would only impact initial startup time and memory to a modest extent,
  however it’s best that these additional modules aren’t reverse-dependent on
  straight Core usage.
  References: [#5180](https://www.sqlalchemy.org/trac/ticket/5180)
- Vendored the `inspect.formatannotation` function inside of
  `sqlalchemy.util.compat`, which is needed for the vendored version of
  `inspect.formatargspec`.  The function is not documented in cPython and
  is not guaranteed to be available in future Python versions.
  References: [#5138](https://www.sqlalchemy.org/trac/ticket/5138)

## 1.3.13

Released: January 22, 2020

### orm

- Identified a performance issue in the system by which a join is constructed
  based on a mapped relationship.   The clause adaption system would be used
  for the majority of join expressions including in the common case where no
  adaptation is needed.   The conditions under which this adaptation occur
  have been refined so that average non-aliased joins along a simple
  relationship without a “secondary” table use about 70% less function calls.
- Added test support and repaired a wide variety of unnecessary reference
  cycles created for short-lived objects, mostly in the area of ORM queries.
  Thanks much to Carson Ip for the help on this.
  References: [#5050](https://www.sqlalchemy.org/trac/ticket/5050), [#5056](https://www.sqlalchemy.org/trac/ticket/5056), [#5071](https://www.sqlalchemy.org/trac/ticket/5071)
- Fixed regression in loader options introduced in 1.3.0b3 via [#4468](https://www.sqlalchemy.org/trac/ticket/4468)
  where the ability to create a loader option using
  [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) targeting an aliased entity that is an
  inheriting subclass of the entity which the preceding relationship refers
  to would fail to produce a matching path.   See also [#5082](https://www.sqlalchemy.org/trac/ticket/5082) fixed
  in this same release which involves a similar kind of issue.
  References: [#5107](https://www.sqlalchemy.org/trac/ticket/5107)
- Fixed regression in joined eager loading introduced in 1.3.0b3 via
  [#4468](https://www.sqlalchemy.org/trac/ticket/4468) where the ability to create a joined option across a
  [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) into a polymorphic subclass using
  `RelationshipProperty.of_type()` and then further along regular mapped
  relationships would fail as the polymorphic subclass would not add itself
  to the load path in a way that could be located by the loader strategy.  A
  tweak has been made to resolve this scenario.
  References: [#5082](https://www.sqlalchemy.org/trac/ticket/5082)
- Repaired a warning in the ORM flush process that was not covered by  test
  coverage when deleting objects that use the “version_id” feature. This
  warning is generally unreachable unless using a dialect that sets the
  “supports_sane_rowcount” flag to False, which  is not typically the case
  however is possible for some MySQL configurations as well as older Firebird
  drivers, and likely some third party dialects.
  References: [#5068](https://www.sqlalchemy.org/trac/ticket/5068)
- Fixed bug where usage of joined eager loading would not properly wrap the
  query inside of a subquery when [Query.group_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.group_by) were used against
  the query.   When any kind of result-limiting approach is used, such as
  DISTINCT, LIMIT, OFFSET, joined eager loading embeds the row-limited query
  inside of a subquery so that the collection results are not impacted.   For
  some reason, the presence of GROUP BY was never included in this criterion,
  even though it has a similar effect as using DISTINCT.   Additionally, the
  bug would prevent using GROUP BY at all for a joined eager load query for
  most database platforms which forbid non-aggregated, non-grouped columns
  from being in the query, as the additional columns for the joined eager
  load would not be accepted by the database.
  References: [#5065](https://www.sqlalchemy.org/trac/ticket/5065)

### engine

- Fixed issue where the collection of value processors on a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object would be mutated when “expanding IN” parameters
  were used with a datatype that has bind value processors; in particular,
  this would mean that when using statement caching and/or baked queries, the
  same compiled._bind_processors collection would be mutated concurrently.
  Since these processors are the same function for a given bind parameter
  namespace every time, there was no actual negative effect of this issue,
  however, the execution of a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object should never be
  causing any changes in its state, especially given that they are intended
  to be thread-safe and reusable once fully constructed.
  References: [#5048](https://www.sqlalchemy.org/trac/ticket/5048)

### sql

- A function created using [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction) can now specify that the
  name of the function should be rendered with or without quotes by assigning
  the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) construct to the .name element of the object.
  Prior to 1.3.4, quoting was never applied to function names, and some
  quoting was introduced in [#4467](https://www.sqlalchemy.org/trac/ticket/4467) but no means to force quoting for
  a mixed case name was available.  Additionally, the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name)
  construct when used as the name will properly register its lowercase name
  in the function registry so that the name continues to be available via the
  `func.` registry.
  See also
  [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction)
  References: [#5079](https://www.sqlalchemy.org/trac/ticket/5079)

### postgresql

- Added support for prefixes to the [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) construct, to allow
  support for Postgresql 12 “MATERIALIZED” and “NOT MATERIALIZED” phrases.
  Pull request courtesy Marat Sharafutdinov.
  See also
  [HasCTE.cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE.cte)
  References: [#5040](https://www.sqlalchemy.org/trac/ticket/5040)
- Fixed issue where the PostgreSQL dialect would fail to parse a reflected
  CHECK constraint that was a boolean-valued function (as opposed to a
  boolean-valued expression).
  References: [#5039](https://www.sqlalchemy.org/trac/ticket/5039)

### mssql

- Fixed issue where a timezone-aware `datetime` value being converted to
  string for use as a parameter value of a [DATETIMEOFFSET](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.DATETIMEOFFSET)
  column was omitting the fractional seconds.
  References: [#5045](https://www.sqlalchemy.org/trac/ticket/5045)

### tests

- Fixed a few test failures which would occur on Windows due to SQLite file
  locking issues, as well as some timing issues in connection pool related
  tests; pull request courtesy Federico Caselli.
  References: [#4946](https://www.sqlalchemy.org/trac/ticket/4946)
- Improved detection of two phase transactions requirement for the PostgreSQL
  database by testing that max_prepared_transactions is set to a value
  greater than 0.  Pull request courtesy Federico Caselli.
  References: [#5057](https://www.sqlalchemy.org/trac/ticket/5057)

### misc

- Fixed bug in sqlalchemy.ext.serializer where a unique
  [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) object could conflict with itself if it were
  present in the mapping itself, as well as the filter condition of the
  query, as one side would be used against the non-deserialized version and
  the other side would use the deserialized version.  Logic is added to
  [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) similar to its “clone” method which will uniquify
  the parameter name upon deserialize so that it doesn’t conflict with its
  original.
  References: [#5086](https://www.sqlalchemy.org/trac/ticket/5086)

## 1.3.12

Released: December 16, 2019

### orm

- Fixed issue involving `lazy="raise"` strategy where an ORM delete of an
  object would raise for a simple “use-get” style many-to-one relationship
  that had lazy=”raise” configured.  This is inconsistent vs. the change
  introduced in 1.3 as part of [#4353](https://www.sqlalchemy.org/trac/ticket/4353), where it was established that
  a history operation that does not expect emit SQL should bypass the
  `lazy="raise"` check, and instead effectively treat it as
  `lazy="raise_on_sql"` for this case.  The fix adjusts the lazy loader
  strategy to not raise for the case where the lazy load was instructed that
  it should not emit SQL if the object were not present.
  References: [#4997](https://www.sqlalchemy.org/trac/ticket/4997)
- Fixed regression introduced in 1.3.0 related to the association proxy
  refactor in [#4351](https://www.sqlalchemy.org/trac/ticket/4351) that prevented [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) attributes
  from working in terms of an association proxy that references them.
  References: [#5000](https://www.sqlalchemy.org/trac/ticket/5000)
- Setting persistence-related flags on [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) while also
  setting viewonly=True will now emit a regular warning, as these flags do
  not make sense for a viewonly=True relationship.   In particular, the
  “cascade” settings have their own warning that is generated based on the
  individual values, such as “delete, delete-orphan”, that should not apply
  to a viewonly relationship.   Note however that in the case of “cascade”,
  these settings are still erroneously taking effect even though the
  relationship is set up as “viewonly”.   In 1.4, all persistence-related
  cascade settings will be disallowed on a viewonly=True relationship in
  order to resolve this issue.
  References: [#4993](https://www.sqlalchemy.org/trac/ticket/4993)
- Fixed issue where when assigning a collection to itself as a slice, the
  mutation operation would fail as it would first erase the assigned
  collection inadvertently.   As an assignment that does not change  the
  contents should not generate events, the operation is now a no-op. Note
  that the fix only applies to Python 3; in Python 2, the `__setitem__`
  hook isn’t called in this case; `__setslice__` is used instead which
  recreates the list item-by-item in all cases.
  References: [#4990](https://www.sqlalchemy.org/trac/ticket/4990)
- Fixed issue where by if the “begin” of a transaction failed at the Core
  engine/connection level, such as due to network error or database is locked
  for some transactional recipes, within the context of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  procuring that connection from the connection pool and then immediately
  returning it, the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) would not close the connection
  despite this connection not being stored within the state of that
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  This would lead to the connection being cleaned out by
  the connection pool weakref handler within garbage collection which is an
  unpreferred codepath that in some special configurations can emit errors in
  standard error.
  References: [#5034](https://www.sqlalchemy.org/trac/ticket/5034)

### sql

- Fixed bug where “distinct” keyword passed to [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) would not
  treat a string value as a “label reference” in the same way that the
  `select.distinct()` does; it would instead raise unconditionally. This
  keyword argument and the others passed to [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) will ultimately
  be deprecated for SQLAlchemy 2.0.
  References: [#5028](https://www.sqlalchemy.org/trac/ticket/5028)
- Changed the text of the exception for “Can’t resolve label reference” to
  include other kinds of label coercions, namely that “DISTINCT” is also in
  this category under the PostgreSQL dialect.

### sqlite

- Fixed issue to workaround SQLite’s behavior of assigning “numeric” affinity
  to JSON datatypes, first described at [Support for SQLite JSON Added](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3850), which returns
  scalar numeric JSON values as a number and not as a string that can be JSON
  deserialized.  The SQLite-specific JSON deserializer now gracefully
  degrades for this case as an exception and bypasses deserialization for
  single numeric values, as from a JSON perspective they are already
  deserialized.
  References: [#5014](https://www.sqlalchemy.org/trac/ticket/5014)

### mssql

- Repaired support for the [DATETIMEOFFSET](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.DATETIMEOFFSET) datatype on PyODBC,
  by adding PyODBC-level result handlers as it does not include native
  support for this datatype.  This includes usage of the Python 3 “timezone”
  tzinfo subclass in order to set up a timezone, which on Python 2 makes
  use of a minimal backport of “timezone” in sqlalchemy.util.
  References: [#4983](https://www.sqlalchemy.org/trac/ticket/4983)

## 1.3.11

Released: November 11, 2019

### orm

- Added accessor [Query.is_single_entity()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.is_single_entity) to [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query), which
  will indicate if the results returned by this [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) will be a
  list of ORM entities, or a tuple of entities or column expressions.
  SQLAlchemy hopes to improve upon the behavior of single entity / tuples in
  future releases such that the behavior would be explicit up front, however
  this attribute should be helpful with the current behavior.  Pull request
  courtesy Patrick Hayes.
  References: [#4934](https://www.sqlalchemy.org/trac/ticket/4934)
- The [relationship.omit_join](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.omit_join) flag was not intended to be
  manually set to True, and will now emit a warning when this occurs.  The
  omit_join optimization is detected automatically, and the `omit_join`
  flag was only intended to disable the optimization in the hypothetical case
  that the optimization may have interfered with correct results, which has
  not been observed with the modern version of this feature.   Setting the
  flag to True when it is not automatically detected may cause the selectin
  load feature to not work correctly when a non-default primary join
  condition is in use.
  References: [#4954](https://www.sqlalchemy.org/trac/ticket/4954)
- A warning is emitted if a primary key value is passed to [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get)
  that consists of None for all primary key column positions.   Previously,
  passing a single None outside of a tuple would raise a `TypeError` and
  passing a composite None (tuple of None values) would silently pass
  through.   The fix now coerces the single None into a tuple where it is
  handled consistently with the other None conditions.  Thanks to Lev
  Izraelit for the help with this.
  References: [#4915](https://www.sqlalchemy.org/trac/ticket/4915)
- The [BakedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery) will not cache a query that was modified by a
  [QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) event, so that compilation hooks that
  may be applying ad-hoc modifications to queries will take effect on each
  run.  In particular this is helpful for events that modify queries used in
  lazy loading as well as eager loading such as “select in” loading.  In
  order to re-enable caching for a query modified by this event, a new
  flag `bake_ok` is added; see [Using the before_compile event](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#baked-with-before-compile) for
  details.
  A longer term plan to provide a new form of SQL caching should solve this
  kind of issue more comprehensively.
  References: [#4947](https://www.sqlalchemy.org/trac/ticket/4947)
- Fixed ORM bug where a “secondary” table that referred to a selectable which
  in some way would refer to the local primary table would apply aliasing to
  both sides of the join condition when a relationship-related join, either
  via [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) or by [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload), were generated.  The
  “local” side is now excluded.
  References: [#4974](https://www.sqlalchemy.org/trac/ticket/4974)

### engine

- Fixed bug where parameter repr as used in logging and error reporting needs
  additional context in order to distinguish between a list of parameters for
  a single statement and a list of parameter lists, as the “list of lists”
  structure could also indicate a single parameter list where the first
  parameter itself is a list, such as for an array parameter.   The
  engine/connection now passes in an additional boolean indicating how the
  parameters should be considered.  The only SQLAlchemy backend that expects
  arrays as parameters is that of  psycopg2 which uses pyformat parameters,
  so this issue has not been too apparent, however as other drivers that use
  positional gain more features it is important that this be supported. It
  also eliminates the need for the parameter repr function to guess based on
  the parameter structure passed.
  References: [#4902](https://www.sqlalchemy.org/trac/ticket/4902)
- Fixed bug in [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) where the cache key generation did not
  take into account arguments passed in the form of tuples, such as the tuple
  of view name styles to return for the PostgreSQL dialect. This would lead
  the inspector to cache too generally for a more specific set of criteria.
  The logic has been adjusted to include every keyword element in the cache,
  as every argument is expected to be appropriate for a cache else the
  caching decorator should be bypassed by the dialect.
  References: [#4955](https://www.sqlalchemy.org/trac/ticket/4955)

### sql

- Added new accessors to expressions of type [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) to allow for
  specific datatype access and comparison, covering strings, integers,
  numeric, boolean elements.   This revises the documented approach of
  CASTing to string when comparing values, instead adding specific
  functionality into the PostgreSQL, SQlite, MySQL dialects to reliably
  deliver these basic types in all cases.
  See also
  [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)
  [Comparator.as_string()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_string)
  [Comparator.as_boolean()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_boolean)
  [Comparator.as_float()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_float)
  [Comparator.as_integer()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.Comparator.as_integer)
  References: [#4276](https://www.sqlalchemy.org/trac/ticket/4276)
- The [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct now supports “unique” bound parameters, which
  will dynamically uniquify themselves on compilation thus allowing multiple
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) constructs with the same bound parameter names to be combined
  together.
  References: [#4933](https://www.sqlalchemy.org/trac/ticket/4933)
- Changed the `repr()` of the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) construct to use
  regular string repr() under Python 3, rather than running it through
  “backslashreplace” escaping, which can be misleading.
  References: [#4931](https://www.sqlalchemy.org/trac/ticket/4931)

### schema

- Added DDL support for “computed columns”; these are DDL column
  specifications for columns that have a server-computed value, either upon
  SELECT (known as “virtual”) or at the point of which they are INSERTed or
  UPDATEd (known as “stored”).  Support is established for Postgresql, MySQL,
  Oracle SQL Server and Firebird. Thanks to Federico Caselli for lots of work
  on this one.
  See also
  [Computed Columns (GENERATED ALWAYS AS)](https://docs.sqlalchemy.org/en/20/core/defaults.html#computed-ddl)
  References: [#4894](https://www.sqlalchemy.org/trac/ticket/4894)
- Fixed bug where a table that would have a column label overlap with a plain
  column name, such as “foo.id AS foo_id” vs. “foo.foo_id”, would prematurely
  generate the `._label` attribute for a column before this overlap could
  be detected due to the use of the `index=True` or `unique=True` flag on
  the column in conjunction with the default naming convention of
  `"column_0_label"`.  This would then lead to failures when `._label`
  were used later to generate a bound parameter name, in particular those
  used by the ORM when generating the WHERE clause for an UPDATE statement.
  The issue has been fixed by using an alternate `._label` accessor for DDL
  generation that does not affect the state of the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).   The
  accessor also bypasses the key-deduplication step as it is not necessary
  for DDL, the naming is now consistently `"<tablename>_<columnname>"`
  without any subsequent numeric symbols when used in DDL.
  References: [#4911](https://www.sqlalchemy.org/trac/ticket/4911)

### mysql

- Added “Connection was killed” message interpreted from the base
  pymysql.Error class in order to detect closed connection, based on reports
  that this message is arriving via a pymysql.InternalError() object which
  indicates pymysql is not handling it correctly.
  References: [#4945](https://www.sqlalchemy.org/trac/ticket/4945)

### mssql

- Fixed issue in MSSQL dialect where an expression-based OFFSET value in a
  SELECT would be rejected, even though the dialect can render this
  expression inside of a ROW NUMBER-oriented LIMIT/OFFSET construct.
  References: [#4973](https://www.sqlalchemy.org/trac/ticket/4973)
- Fixed an issue in the `Engine.table_names()` method where it would
  feed the dialect’s default schema name back into the dialect level table
  function, which in the case of SQL Server would interpret it as a
  dot-tokenized schema name as viewed by the mssql dialect, which would
  cause the method to fail in the case where the database username actually
  had a dot inside of it.  In 1.3, this method is still used by the
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) function so is a prominent codepath. In 1.4,
  which is the current master development branch, this issue doesn’t exist,
  both because [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) isn’t using this method nor does the
  method pass the default schema name explicitly.  The fix nonetheless
  guards against the default server name value returned by the dialect from
  being interpreted as dot-tokenized name under any circumstances by
  wrapping it in quoted_name().
  References: [#4923](https://www.sqlalchemy.org/trac/ticket/4923)

### oracle

- Added dialect-level flag `encoding_errors` to the cx_Oracle dialect,
  which can be specified as part of [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine).   This is passed
  to SQLAlchemy’s unicode decoding converter under Python 2, and to
  cx_Oracle’s `cursor.var()` object as the `encodingErrors` parameter
  under Python 3, for the very unusual case that broken encodings are present
  in the target database which cannot be fetched unless error handling is
  relaxed.  The value is ultimately one of the Python “encoding errors”
  parameters passed to `decode()`.
  References: [#4799](https://www.sqlalchemy.org/trac/ticket/4799)
- Modified the approach of “name normalization” for the Oracle and Firebird
  dialects, which converts from the UPPERCASE-as-case-insensitive convention
  of these dialects into lowercase-as-case-insensitive for SQLAlchemy, to not
  automatically apply the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) construct to a name that
  matches itself under upper or lower case conversion, as is the case for
  many non-european characters.   All names used within metadata structures
  are converted to [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) objects in any case; the change
  here would only affect the output of some inspection functions.
  References: [#4931](https://www.sqlalchemy.org/trac/ticket/4931)
- The [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR) datatype will now bind to the
  `cx_Oracle.FIXED_NCHAR` DBAPI data bindings when used in a bound
  parameter, which supplies proper comparison behavior against a
  variable-length string.  Previously, the [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR) datatype
  would bind to `cx_oracle.NCHAR` which is not fixed length; the
  [CHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR) datatype already binds to `cx_Oracle.FIXED_CHAR`
  so it is now consistent that [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR) binds to
  `cx_Oracle.FIXED_NCHAR`.
  References: [#4913](https://www.sqlalchemy.org/trac/ticket/4913)

### tests

- Fixed test failures which would occur with newer SQLite as of version 3.30
  or greater, due to their addition of nulls ordering syntax as well as new
  restrictions on aggregate functions.  Pull request courtesy Nils Philippsen.
  References: [#4920](https://www.sqlalchemy.org/trac/ticket/4920)

### misc

- Added a workaround for a setuptools-related failure that has been observed
  as occurring on Windows installations, where setuptools is not correctly
  reporting a build error when the MSVC build dependencies are not installed
  and therefore not allowing graceful degradation into non C extensions
  builds.
  References: [#4967](https://www.sqlalchemy.org/trac/ticket/4967)
- Added additional “disconnect” message “Error writing data to the
  connection” to Firebird disconnection detection.  Pull request courtesy
  lukens.
  References: [#4903](https://www.sqlalchemy.org/trac/ticket/4903)

## 1.3.10

Released: October 9, 2019

### mssql

- Fixed bug in SQL Server dialect with new “max_identifier_length” feature
  where the mssql dialect already featured this flag, and the implementation
  did not accommodate for the new initialization hook correctly.
  References: [#4857](https://www.sqlalchemy.org/trac/ticket/4857)

### oracle

- Fixed regression in Oracle dialect that was inadvertently using max
  identifier length of 128 characters on Oracle server 12.2 and greater even
  though the stated contract for the remainder of the 1.3 series is  that
  this value stays at 30 until version SQLAlchemy 1.4.  Also repaired issues
  with the retrieval of the “compatibility” version, and removed the warning
  emitted when the “v$parameter” view was not accessible as this was  causing
  user confusion.
  References: [#4857](https://www.sqlalchemy.org/trac/ticket/4857), [#4898](https://www.sqlalchemy.org/trac/ticket/4898)

## 1.3.9

Released: October 4, 2019

### orm

- Fixed regression in selectinload loader strategy caused by [#4775](https://www.sqlalchemy.org/trac/ticket/4775)
  (released in version 1.3.6) where a many-to-one attribute of None would no
  longer be populated by the loader.  While this was usually not noticeable
  due to the lazyloader populating None upon get, it would lead to a detached
  instance error if the object were detached.
  References: [#4872](https://www.sqlalchemy.org/trac/ticket/4872)
- Passing a plain string expression to [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query) is deprecated,
  as all string coercions were removed in [#4481](https://www.sqlalchemy.org/trac/ticket/4481) and this one should
  have been included.   The [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) function may be used to
  produce a textual column expression.
  References: [#4873](https://www.sqlalchemy.org/trac/ticket/4873)
- A warning is emitted for a condition in which the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) may
  implicitly swap an object out of the identity map for another one with the
  same primary key, detaching the old one, which can be an observed result of
  load operations which occur within the [SessionEvents.after_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.after_flush)
  hook.  The warning is intended to notify the user that some special
  condition has caused this to happen and that the previous object may not be
  in the expected state.
  References: [#4890](https://www.sqlalchemy.org/trac/ticket/4890)

### engine

- Added new [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) parameter
  [create_engine.max_identifier_length](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.max_identifier_length). This overrides the
  dialect-coded “max identifier length” in order to accommodate for databases
  that have recently changed this length and the SQLAlchemy dialect has
  not yet been adjusted to detect for that version.  This parameter interacts
  with the existing [create_engine.label_length](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.label_length) parameter in that
  it establishes the maximum (and default) value for anonymously generated
  labels.   Additionally, post-connection detection of max identifier lengths
  has been added to the dialect system.  This feature is first being used
  by the Oracle dialect.
  See also
  [Maximum Identifier Lengths](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-max-identifier-lengths) - in the Oracle dialect documentation
  References: [#4857](https://www.sqlalchemy.org/trac/ticket/4857)

### sql

- Added an explicit error message for the case when objects passed to
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) are not [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) objects, rather than resolving
  to an attribute error.
  References: [#4847](https://www.sqlalchemy.org/trac/ticket/4847)
- Characters that interfere with “pyformat” or “named” formats in bound
  parameters, namely `%, (, )` and the space character, as well as a few
  other typically undesirable characters, are stripped early for a
  [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) that is using an anonymized name, which is typically
  generated automatically from a named column which itself includes these
  characters in its name and does not use a `.key`, so that they do not
  interfere either with the SQLAlchemy compiler’s use of string formatting or
  with the driver-level parsing of the parameter, both of which could be
  demonstrated before the fix.  The change only applies to anonymized
  parameter names that are generated and consumed internally, not end-user
  defined names, so the change should have no impact on any existing code.
  Applies in particular to the psycopg2 driver which does not otherwise quote
  special parameter names, but also strips leading underscores to suit Oracle
  (but not yet leading numbers, as some anon parameters are currently
  entirely numeric/underscore based); Oracle in any case continues to quote
  parameter names that include special characters.
  References: [#4837](https://www.sqlalchemy.org/trac/ticket/4837)

### sqlite

- Added support for sqlite “URI” connections, which allow for sqlite-specific
  flags to be passed in the query string such as “read only” for Python
  sqlite3 drivers that support this.
  See also
  [URI Connections](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-uri-connections)
  References: [#4863](https://www.sqlalchemy.org/trac/ticket/4863)

### mssql

- Added identifier quoting to the schema name applied to the “use” statement
  which is invoked when a SQL Server multipart schema name is used within  a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that is being reflected, as well as for [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector)
  methods such as [Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names); this accommodates for
  special characters or spaces in the database name.  Additionally, the “use”
  statement is not emitted if the current database matches the target owner
  database name being passed.
  References: [#4883](https://www.sqlalchemy.org/trac/ticket/4883)

### oracle

- The Oracle dialect now emits a warning if Oracle version 12.2 or greater is
  used, and the [create_engine.max_identifier_length](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.max_identifier_length) parameter is
  not set.   The version in this specific case defaults to that of the
  “compatibility” version set in the Oracle server configuration, not the
  actual server version.   In version 1.4, the default max_identifier_length
  for 12.2 or greater will move to 128 characters.  In order to maintain
  forwards compatibility, applications should set
  [create_engine.max_identifier_length](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.max_identifier_length) to 30 in order to maintain
  the same length behavior, or to 128 in order to test the upcoming behavior.
  This length determines among other things how generated constraint names
  are truncated for statements like `CREATE CONSTRAINT` and `DROP
  CONSTRAINT`, which means a the new length may produce a name-mismatch
  against a name that was generated with the old length, impacting database
  migrations.
  See also
  [Maximum Identifier Lengths](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracle-max-identifier-lengths) - in the Oracle dialect documentation
  References: [#4857](https://www.sqlalchemy.org/trac/ticket/4857)
- Restored adding cx_Oracle.DATETIME to the setinputsizes() call when a
  SQLAlchemy [Date](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date), [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) or [Time](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Time) datatype is
  used, as some complex queries require this to be present.  This was removed
  in the 1.2 series for arbitrary reasons.
  References: [#4886](https://www.sqlalchemy.org/trac/ticket/4886)

### tests

- Fixed unit test regression released in 1.3.8 that would cause failure for
  Oracle, SQL Server and other non-native ENUM platforms due to new
  enumeration tests added as part of [#4285](https://www.sqlalchemy.org/trac/ticket/4285) enum sortability in the
  unit of work; the enumerations created constraints that were duplicated on
  name.
  References: [#4285](https://www.sqlalchemy.org/trac/ticket/4285)

## 1.3.8

Released: August 27, 2019

### orm

- Added support for the use of an [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) datatype using Python
  pep-435 enumeration objects as values for use as a primary key column
  mapped by the ORM.  As these values are not inherently sortable, as
  required by the ORM for primary keys, a new
  [TypeEngine.sort_key_function](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.sort_key_function) attribute is added to the typing
  system which allows any SQL type to  implement a sorting for Python objects
  of its type which is consulted by the unit of work.   The [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
  type then defines this using the  database value of a given enumeration.
  The sorting scheme can be  also be redefined by passing a callable to the
  [Enum.sort_key_function](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum.params.sort_key_function) parameter.  Pull request courtesy
  Nicolas Caniart.
  References: [#4285](https://www.sqlalchemy.org/trac/ticket/4285)
- Fixed bug where [Load](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load) objects were not pickleable due to
  mapper/relationship state in the internal context dictionary.  These
  objects are now converted to picklable using similar techniques as that of
  other elements within the loader option system that have long been
  serializable.
  References: [#4823](https://www.sqlalchemy.org/trac/ticket/4823)

### engine

- Added new parameter [create_engine.hide_parameters](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.hide_parameters) which when
  set to True will cause SQL parameters to no longer be logged, nor rendered
  in the string representation of a [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) object.
  References: [#4815](https://www.sqlalchemy.org/trac/ticket/4815)
- Fixed an issue whereby if the dialect “initialize” process which occurs on
  first connect would encounter an unexpected exception, the initialize
  process would fail to complete and then no longer attempt on subsequent
  connection attempts, leaving the dialect in an un-initialized, or partially
  initialized state, within the scope of parameters that need to be
  established based on inspection of a live connection.   The “invoke once”
  logic in the event system has been reworked to accommodate for this
  occurrence using new, private API features that establish an “exec once”
  hook that will continue to allow the initializer to fire off on subsequent
  connections, until it completes without raising an exception. This does not
  impact the behavior of the existing `once=True` flag within the event
  system.
  References: [#4807](https://www.sqlalchemy.org/trac/ticket/4807)

### postgresql

- Added support for reflection of CHECK constraints that include the special
  PostgreSQL qualifier “NOT VALID”, which can be present for CHECK
  constraints that were added to an existing table with the directive that
  they not be applied to existing data in the table. The PostgreSQL
  dictionary for CHECK constraints as returned by
  [Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints) may include an additional entry
  `dialect_options` which within will contain an entry `"not_valid":
  True` if this symbol is detected.   Pull request courtesy Bill Finn.
  References: [#4824](https://www.sqlalchemy.org/trac/ticket/4824)
- Revised the approach for the just added support for the psycopg2
  “execute_values()” feature added in 1.3.7 for [#4623](https://www.sqlalchemy.org/trac/ticket/4623).  The approach
  relied upon a regular expression that would fail to match for a more
  complex INSERT statement such as one which had subqueries involved.   The
  new approach matches exactly the string that was rendered as the VALUES
  clause.
  References: [#4623](https://www.sqlalchemy.org/trac/ticket/4623)
- Fixed bug where Postgresql operators such as
  [Comparator.contains()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contains) and
  [Comparator.contained_by()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator.contained_by) would fail to function
  correctly for non-integer values when used against a
  [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) object, due to an erroneous assert statement.
  References: [#4822](https://www.sqlalchemy.org/trac/ticket/4822)

### sqlite

- Fixed bug where a FOREIGN KEY that was set up to refer to the parent table
  by table name only without the column names would not correctly be
  reflected as far as setting up the “referred columns”, since SQLite’s
  PRAGMA does not report on these columns if they weren’t given explicitly.
  For some reason this was hardcoded to assume the name of the local column,
  which might work for some cases but is not correct. The new approach
  reflects the primary key of the referred table and uses the constraint
  columns list as the referred columns list, if the remote column(s) aren’t
  present in the reflected pragma directly.
  References: [#4810](https://www.sqlalchemy.org/trac/ticket/4810)

## 1.3.7

Released: August 14, 2019

### orm

- Fixed regression caused by new selectinload for many-to-one logic where
  a primaryjoin condition not based on real foreign keys would cause
  KeyError if a related object did not exist for a given key value on the
  parent object.
  References: [#4777](https://www.sqlalchemy.org/trac/ticket/4777)
- Fixed bug where using [Query.first()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.first) or a slice expression in
  conjunction with a query that has an expression based “offset” applied
  would raise TypeError, due to an “or” conditional against “offset” that did
  not expect it to be a SQL expression as opposed to an integer or None.
  References: [#4803](https://www.sqlalchemy.org/trac/ticket/4803)

### sql

- Fixed issue where [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) object which contained a mixture of
  functional expressions which were not resolvable to a particular column,
  in combination with string-based column names, would fail to initialize
  its internal state correctly leading to failures during DDL compilation.
  References: [#4778](https://www.sqlalchemy.org/trac/ticket/4778)
- Fixed bug where [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression) method would not be
  applied to subsequent SELECT statements inside of a UNION or other
  `_selectable.CompoundSelect`, even though the SELECT statements are rendered at
  the topmost level of the statement.   New logic now differentiates between
  rendering the column expression, which is needed for all SELECTs in the
  list, vs. gathering the returned data type for the result row, which is
  needed only for the first SELECT.
  References: [#4787](https://www.sqlalchemy.org/trac/ticket/4787)
- Fixed issue where internal cloning of SELECT constructs could lead to a key
  error if the copy of the SELECT changed its state such that its list of
  columns changed.  This was observed to be occurring in some ORM scenarios
  which may be unique to 1.3 and above, so is partially a regression fix.
  References: [#4780](https://www.sqlalchemy.org/trac/ticket/4780)

### postgresql

- Added new dialect flag for the psycopg2 dialect, `executemany_mode` which
  supersedes the previous experimental `use_batch_mode` flag.
  `executemany_mode` supports both the “execute batch” and “execute values”
  functions provided by psycopg2, the latter which is used for compiled
  [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) constructs.   Pull request courtesy Yuval Dinari.
  See also
  [Psycopg2 Fast Execution Helpers](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#psycopg2-executemany-mode)
  References: [#4623](https://www.sqlalchemy.org/trac/ticket/4623)

### mysql

- Added reserved words ARRAY and MEMBER to the MySQL reserved words list, as
  MySQL 8.0 has now made these reserved.
  References: [#4783](https://www.sqlalchemy.org/trac/ticket/4783)
- The MySQL dialects will emit “SET NAMES” at the start of a connection when
  charset is given to the MySQL driver, to appease an apparent behavior
  observed in MySQL 8.0 that raises a collation error when a UNION includes
  string columns unioned against columns of the form CAST(NULL AS CHAR(..)),
  which is what SQLAlchemy’s polymorphic_union function does.   The issue
  seems to have affected PyMySQL for at least a year, however has recently
  appeared as of mysqlclient 1.4.4 based on changes in how this DBAPI creates
  a connection.  As the presence of this directive impacts three separate
  MySQL charset settings which each have intricate effects based on their
  presence,  SQLAlchemy will now emit the directive on new connections to
  ensure correct behavior.
  References: [#4804](https://www.sqlalchemy.org/trac/ticket/4804)
- Added another fix for an upstream MySQL 8 issue where a case sensitive
  table name is reported incorrectly in foreign key constraint reflection,
  this is an extension of the fix first added for [#4344](https://www.sqlalchemy.org/trac/ticket/4344) which
  affects a case sensitive column name.  The new issue occurs through MySQL
  8.0.17, so the general logic of the 88718 fix remains in place.
  See also
  [https://bugs.mysql.com/bug.php?id=96365](https://bugs.mysql.com/bug.php?id=96365) - upstream bug
  References: [#4751](https://www.sqlalchemy.org/trac/ticket/4751)

### sqlite

- The dialects that support json are supposed to take arguments
  `json_serializer` and `json_deserializer` at the create_engine() level,
  however the SQLite dialect calls them `_json_serializer` and
  `_json_deserilalizer`.  The names have been corrected, the old names are
  accepted with a change warning, and these parameters are now documented as
  [create_engine.json_serializer](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.json_serializer) and
  [create_engine.json_deserializer](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.json_deserializer).
  References: [#4798](https://www.sqlalchemy.org/trac/ticket/4798)
- Fixed bug where usage of “PRAGMA table_info” in SQLite dialect meant that
  reflection features to detect for table existence, list of table columns,
  and list of foreign keys, would default to any table in any attached
  database, when no schema name was given and the table did not exist in the
  base schema.  The fix explicitly runs PRAGMA for the ‘main’ schema and then
  the ‘temp’ schema if the ‘main’ returned no rows, to maintain the behavior
  of tables + temp tables in the “no schema” namespace, attached tables only
  in the “schema” namespace.
  References: [#4793](https://www.sqlalchemy.org/trac/ticket/4793)

### mssql

- Added new [try_cast()](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.try_cast) construct for SQL Server which emits
  “TRY_CAST” syntax.  Pull request courtesy Leonel Atencio.
  References: [#4782](https://www.sqlalchemy.org/trac/ticket/4782)

### misc

- Fixed issue in event system where using the `once=True` flag with
  dynamically generated listener functions would cause event registration of
  future events to fail if those listener functions were garbage collected
  after they were used, due to an assumption that a listened function is
  strongly referenced.  The “once” wrapped is now modified to strongly
  reference the inner function persistently, and documentation is updated
  that using “once” does not imply automatic de-registration of listener
  functions.
  References: [#4794](https://www.sqlalchemy.org/trac/ticket/4794)

## 1.3.6

Released: July 21, 2019

### orm

- Added new loader option method [Load.options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load.options) which allows loader
  options to be constructed hierarchically, so that many sub-options can be
  applied to a particular path without needing to call [defaultload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.defaultload)
  many times.  Thanks to Alessio Bogon for the idea.
  References: [#4736](https://www.sqlalchemy.org/trac/ticket/4736)
- The optimization applied to selectin loading in [#4340](https://www.sqlalchemy.org/trac/ticket/4340) where a JOIN
  is not needed to eagerly load related items is now applied to many-to-one
  relationships as well, so that only the related table is queried for a
  simple join condition.   In this case, the related items are queried
  based on the value of a foreign key column on the parent; if these columns
  are deferred or otherwise not loaded on any of the parent objects in
  the collection, the loader falls back to the JOIN method.
  References: [#4775](https://www.sqlalchemy.org/trac/ticket/4775)
- Fixed regression caused by [#4365](https://www.sqlalchemy.org/trac/ticket/4365) where a join from an entity to
  itself without using aliases no longer raises an informative error message,
  instead failing on an assertion.  The informative error condition has been
  restored.
  References: [#4773](https://www.sqlalchemy.org/trac/ticket/4773)
- Fixed an issue where the `_ORMJoin.join()` method, which is a
  not-internally-used ORM-level method that exposes what is normally an
  internal process of [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join), did not propagate the `full` and
  `outerjoin` keyword arguments correctly.  Pull request courtesy Denis
  Kataev.
  References: [#4713](https://www.sqlalchemy.org/trac/ticket/4713)
- Fixed bug where a many-to-one relationship that specified `uselist=True`
  would fail to update correctly during a primary key change where a related
  column needs to change.
  References: [#4772](https://www.sqlalchemy.org/trac/ticket/4772)
- Fixed bug where the detection for many-to-one or one-to-one use with a
  “dynamic” relationship, which is an invalid configuration, would fail to
  raise if the relationship were configured with `uselist=True`.  The
  current fix is that it warns, instead of raises, as this would otherwise be
  backwards incompatible, however in a future release it will be a raise.
  References: [#4772](https://www.sqlalchemy.org/trac/ticket/4772)
- Fixed bug where a synonym created against a mapped attribute that does not
  exist yet, as is the case when it refers to backref before mappers are
  configured, would raise recursion errors when trying to test for attributes
  on it which ultimately don’t exist (as occurs when the classes are run
  through Sphinx autodoc), as the unconfigured state of the synonym would put
  it into an attribute not found loop.
  References: [#4767](https://www.sqlalchemy.org/trac/ticket/4767)

### engine

- Fixed bug where using reflection function such as [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect)
  with an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) object that had execution options applied to it
  would fail, as the resulting `OptionEngine` proxy object failed to
  include a `.engine` attribute used within the reflection routines.
  References: [#4754](https://www.sqlalchemy.org/trac/ticket/4754)

### sql

- Adjusted the initialization for [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) to minimize how often it
  invokes the `.__members__` attribute of a given PEP-435 enumeration
  object, to suit the case where this attribute is expensive to invoke, as is
  the case for some popular third party enumeration libraries.
  References: [#4758](https://www.sqlalchemy.org/trac/ticket/4758)
- Fixed issue where the [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg) construct in combination with
  [FunctionElement.filter()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.filter) would not produce the correct operator
  precedence in combination with the array index operator.
  References: [#4760](https://www.sqlalchemy.org/trac/ticket/4760)
- Fixed an unlikely issue where the “corresponding column” routine for unions
  and other `_selectable.CompoundSelect` objects could return the wrong column in
  some overlapping column situations, thus potentially impacting some ORM
  operations when set operations are in use, if the underlying
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) constructs were used previously in other similar kinds of
  routines, due to a cached value not being cleared.
  References: [#4747](https://www.sqlalchemy.org/trac/ticket/4747)

### postgresql

- Added support for reflection of indexes on PostgreSQL partitioned tables,
  which was added to PostgreSQL as of version 11.
  References: [#4771](https://www.sqlalchemy.org/trac/ticket/4771)
- Added support for multidimensional Postgresql array literals via nesting
  the [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) object within another one.  The
  multidimensional array type is detected automatically.
  See also
  [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array)
  References: [#4756](https://www.sqlalchemy.org/trac/ticket/4756)

### mysql

- Fixed bug where the special logic to render “NULL” for the
  [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP) datatype when `nullable=True` would not work if the
  column’s datatype were a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) or a [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant).
  The logic now ensures that it unwraps down to the original
  [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP) so that this special case NULL keyword is correctly
  rendered when requested.
  References: [#4743](https://www.sqlalchemy.org/trac/ticket/4743)
- Enhanced MySQL/MariaDB version string parsing to accommodate for exotic
  MariaDB version strings where the “MariaDB” word is embedded among other
  alphanumeric characters such as “MariaDBV1”.   This detection is critical in
  order to correctly accommodate for API features that have split between MySQL
  and MariaDB such as the “transaction_isolation” system variable.
  References: [#4624](https://www.sqlalchemy.org/trac/ticket/4624)

### sqlite

- Added support for composite (tuple) IN operators with SQLite, by rendering
  the VALUES keyword for this backend.  As other backends such as DB2 are
  known to use the same syntax, the syntax is enabled in the base compiler
  using a dialect-level flag `tuple_in_values`.   The change also includes
  support for “empty IN tuple” expressions for SQLite when using “in_()”
  between a tuple value and an empty set.
  References: [#4766](https://www.sqlalchemy.org/trac/ticket/4766)

### mssql

- Ensured that the queries used to reflect indexes and view definitions will
  explicitly CAST string parameters into NVARCHAR, as many SQL Server drivers
  frequently treat string values, particularly those with non-ascii
  characters or larger string values, as TEXT which often don’t compare
  correctly against VARCHAR characters in SQL Server’s information schema
  tables for some reason.    These CAST operations already take place for
  reflection queries against SQL Server `information_schema.` tables but
  were missing from three additional queries that are against `sys.`
  tables.
  References: [#4745](https://www.sqlalchemy.org/trac/ticket/4745)

## 1.3.5

Released: June 17, 2019

### orm

- Fixed a series of related bugs regarding joined table inheritance more than
  two levels deep, in conjunction with modification to primary key values,
  where those primary key columns are also linked together in a foreign key
  relationship as is typical for joined table inheritance.  The intermediary
  table in a  three-level inheritance hierarchy will now get its UPDATE if
  only the primary key value has changed and passive_updates=False (e.g.
  foreign key constraints not being enforced), whereas before it would be
  skipped; similarly, with passive_updates=True (e.g. ON UPDATE  CASCADE in
  effect), the third-level table will not receive an UPDATE statement as was
  the case earlier which would fail since CASCADE already modified it.   In a
  related issue, a relationship linked to a three-level inheritance hierarchy
  on the primary key of an intermediary table of a joined-inheritance
  hierarchy will also correctly have its foreign key column updated when the
  parent object’s primary key is modified, even if that parent object is a
  subclass of the linked parent class, whereas before these classes would
  not be counted.
  References: [#4723](https://www.sqlalchemy.org/trac/ticket/4723)
- Fixed bug where the [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors) accessor would
  return an entry for the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) itself under the declarative
  `__mapper__` key, when this is not a descriptor.  The `.is_attribute`
  flag that’s present on all [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr) objects is now
  consulted, which has also been modified to be `True` for an association
  proxy, as it was erroneously set to False for this object.
  References: [#4729](https://www.sqlalchemy.org/trac/ticket/4729)
- Fixed regression in [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) where the `aliased=True` flag
  would not properly apply clause adaptation to filter criteria, if a
  previous join were made to the same entity.  This is because the adapters
  were placed in the wrong order.   The order has been reversed so that the
  adapter for the most recent `aliased=True` call takes precedence as was
  the case in 1.2 and earlier.  This broke the “elementtree” examples among
  other things.
  References: [#4704](https://www.sqlalchemy.org/trac/ticket/4704)
- Replaced the Python compatibility routines for `getfullargspec()` with a
  fully vendored version from Python 3.3.  Originally, Python was emitting
  deprecation warnings for this function in Python 3.8 alphas.  While this
  change was reverted, it was observed that Python 3 implementations for
  `getfullargspec()` are an order of magnitude slower as of the 3.4 series
  where it was rewritten against `Signature`.  While Python plans to
  improve upon this situation, SQLAlchemy projects for now are using a simple
  replacement to avoid any future issues.
  References: [#4674](https://www.sqlalchemy.org/trac/ticket/4674)
- Reworked the attribute mechanics used by [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) to no
  longer rely upon calling `__getattribute__` on the MRO of the wrapped
  class, and to instead resolve the attribute normally on the wrapped class
  using getattr(), and then unwrap/adapt that.  This allows a greater range
  of attribute styles on the mapped class including special `__getattr__()`
  schemes; but it also makes the code simpler and more resilient in general.
  References: [#4694](https://www.sqlalchemy.org/trac/ticket/4694)

### sql

- Addressed a range of quoting issues originating from the use of the
  `literal_column`()` construct. When this construct is
  “proxied” through a subquery and referred to by a label matching its
  text, the label does not have quoting rules applied to it, even if the
  string in the [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) was set up using a `quoted_name``
  construct. Not applying quoting to the text of the [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) is a
  bug because this text is strictly a SQL identifier name and not a SQL
  expression, and the string should not have quotes embedded into it
  already unlike the [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) which it may be
  applied towards.   The existing behavior of a non-labeled
  [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column) being propagated as is on the
  outside of a subquery is maintained in order to help with manual
  quoting schemes, although it’s not clear if valid SQL can be generated
  for such a construct in any case.
  References: [#4730](https://www.sqlalchemy.org/trac/ticket/4730)

### postgresql

- Added support for column sorting flags when reflecting indexes for
  PostgreSQL, including ASC, DESC, NULLSFIRST, NULLSLAST.  Also adds this
  facility to the reflection system in general which can be applied to other
  dialects in future releases.  Pull request courtesy Eli Collins.
  References: [#4717](https://www.sqlalchemy.org/trac/ticket/4717)
- Fixed bug where PostgreSQL dialect could not correctly reflect an ENUM
  datatype that has no members, returning a list with `None` for the
  `get_enums()` call and raising a TypeError when reflecting a column which
  has such a datatype.   The inspection now returns an empty list.
  References: [#4701](https://www.sqlalchemy.org/trac/ticket/4701)

### mysql

- Fixed bug where MySQL ON DUPLICATE KEY UPDATE would not accommodate setting
  a column to the value NULL.  Pull request courtesy Lukáš Banič.
  References: [#4715](https://www.sqlalchemy.org/trac/ticket/4715)

## 1.3.4

Released: May 27, 2019

### orm

- Fixed issue where the [AttributeEvents.active_history](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.params.active_history) flag
  would not be set for an event listener that propagated to a subclass via the
  [AttributeEvents.propagate](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.params.propagate) flag.   This bug has been present
  for the full span of the [AttributeEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents) system.
  References: [#4695](https://www.sqlalchemy.org/trac/ticket/4695)
- Fixed regression where new association proxy system was still not proxying
  hybrid attributes when they made use of the `@hybrid_property.expression`
  decorator to return an alternate SQL expression, or when the hybrid
  returned an arbitrary [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator), at the expression level.
  This involved further generalization of the heuristics used to detect the
  type of object being proxied at the level of [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute),
  to better detect if the descriptor ultimately serves mapped classes or
  column expressions.
  References: [#4690](https://www.sqlalchemy.org/trac/ticket/4690)
- Applied the mapper “configure mutex” against the declarative class mapping
  process, to guard against the race which can occur if mappers are used
  while dynamic module import schemes are still in the process of configuring
  mappers for related classes.  This does not guard against all possible race
  conditions, such as if the concurrent import has not yet encountered the
  dependent classes as of yet, however it guards against as much as possible
  within the SQLAlchemy declarative process.
  References: [#4686](https://www.sqlalchemy.org/trac/ticket/4686)
- A warning is now emitted for the case where a transient object is being
  merged into the session with [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) when that object is
  already transient in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).   This warns for the case where
  the object would normally be double-inserted.
  References: [#4647](https://www.sqlalchemy.org/trac/ticket/4647)
- Fixed regression in new relationship m2o comparison logic first introduced
  at [Improvement to the behavior of many-to-one query expressions](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4359) when comparing to an attribute that is persisted as
  NULL and is in an un-fetched state in the mapped instance.  Since the
  attribute has no explicit default, it needs to default to NULL when
  accessed in a persistent setting.
  References: [#4676](https://www.sqlalchemy.org/trac/ticket/4676)

### engine

- Moved the “rollback” which occurs during dialect initialization so that it
  occurs after additional dialect-specific initialize steps, in particular
  those of the psycopg2 dialect which would inadvertently leave transactional
  state on the first new connection, which could interfere with some
  psycopg2-specific APIs which require that no transaction is started.  Pull
  request courtesy Matthew Wilkes.
  References: [#4663](https://www.sqlalchemy.org/trac/ticket/4663)

### sql

- Fixed that the [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction) class was inadvertently
  registering itself as one of the named functions.  Pull request courtesy
  Adrien Berchet.
  References: [#4653](https://www.sqlalchemy.org/trac/ticket/4653)
- Fixed issue where double negation of a boolean column wouldn’t reset
  the “NOT” operator.
  References: [#4618](https://www.sqlalchemy.org/trac/ticket/4618)
- The [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction) namespace is being migrated so that function
  names are looked up in a case-insensitive manner, as SQL  functions do not
  collide on case sensitive differences nor is this something which would
  occur with user-defined functions or stored procedures.   Lookups for
  functions declared with [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction) now use a case
  insensitive scheme,  however a deprecation case is supported which allows
  two or more [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction) objects with the same name of
  different cases to exist, which will cause case sensitive lookups to occur
  for that particular name, while emitting a warning at function registration
  time.  Thanks to Adrien Berchet for a lot of work on this complicated
  feature.
  References: [#4569](https://www.sqlalchemy.org/trac/ticket/4569)

### postgresql

- Fixed an issue where the “number of rows matched” warning would emit even if
  the dialect reported “supports_sane_multi_rowcount=False”, as is the case
  for psycogp2 with `use_batch_mode=True` and others.
  References: [#4661](https://www.sqlalchemy.org/trac/ticket/4661)

### mysql

- Added support for DROP CHECK constraint which is required by MySQL 8.0.16
  to drop a CHECK constraint; MariaDB supports plain DROP CONSTRAINT.  The
  logic distinguishes between the two syntaxes by checking the server version
  string for MariaDB presence.    Alembic migrations has already worked
  around this issue by implementing its own DROP for MySQL / MariaDB CHECK
  constraints, however this change implements it straight in Core so that its
  available for general use.   Pull request courtesy Hannes Hansen.
  References: [#4650](https://www.sqlalchemy.org/trac/ticket/4650)

### mssql

- Added support for SQL Server filtered indexes, via the `mssql_where`
  parameter which works similarly to that of the `postgresql_where` index
  function in the PostgreSQL dialect.
  See also
  [Filtered Indexes](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-index-where)
  References: [#4657](https://www.sqlalchemy.org/trac/ticket/4657)
- Added error code 20047 to “is_disconnect” for pymssql.  Pull request
  courtesy Jon Schuff.
  References: [#4680](https://www.sqlalchemy.org/trac/ticket/4680)

### misc

- Removed errant “sqla_nose.py” symbol from MANIFEST.in which created an
  undesirable warning message.
  References: [#4625](https://www.sqlalchemy.org/trac/ticket/4625)

## 1.3.3

Released: April 15, 2019

### orm

- Fixed 1.3 regression in new “ambiguous FROMs” query logic introduced in
  [Query.join() handles ambiguity in deciding the “left” side more explicitly](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4365) where a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that explicitly places an entity
  in the FROM clause with [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) and also joins to it
  using [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) would later cause an “ambiguous FROM” error if
  that entity were used in additional joins, as the entity appears twice in
  the “from” list of the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query).  The fix resolves this ambiguity by
  folding the standalone entity into the join that it’s already a part of in
  the same way that ultimately happens when the SELECT statement is rendered.
  References: [#4584](https://www.sqlalchemy.org/trac/ticket/4584)
- Adjusted the [Query.filter_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter_by) method to not call `and()`
  internally against multiple criteria, instead passing it off to
  [Query.filter()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter) as a series of criteria, instead of a single criteria.
  This allows [Query.filter_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter_by) to defer to [Query.filter()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter)’s
  treatment of variable numbers of clauses, including the case where the list
  is empty.  In this case, the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object will not have a
  `.whereclause`, which allows subsequent “no whereclause” methods like
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) to behave consistently.
  References: [#4606](https://www.sqlalchemy.org/trac/ticket/4606)

### postgresql

- Fixed regression from release 1.3.2 caused by [#4562](https://www.sqlalchemy.org/trac/ticket/4562) where a URL
  that contained only a query string and no hostname, such as for the
  purposes of specifying a service file with connection information, would no
  longer be propagated to psycopg2 properly.   The change in [#4562](https://www.sqlalchemy.org/trac/ticket/4562)
  has been adjusted to further suit psycopg2’s exact requirements, which is
  that if there are any connection parameters whatsoever, the “dsn” parameter
  is no longer required, so in this case the query string parameters are
  passed alone.
  References: [#4601](https://www.sqlalchemy.org/trac/ticket/4601)

### mssql

- Fixed issue in SQL Server dialect where if a bound parameter were present in
  an ORDER BY expression that would ultimately not be rendered in the SQL
  Server version of the statement, the parameters would still be part of the
  execution parameters, leading to DBAPI-level errors.  Pull request courtesy
  Matt Lewellyn.
  References: [#4587](https://www.sqlalchemy.org/trac/ticket/4587)

### misc

- Fixed behavioral regression as a result of deprecating the “use_threadlocal”
  flag for [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool), where the [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool) no longer
  makes use of this option which causes the “rollback on return” logic to take
  place when the same [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is used multiple times in the context
  of a transaction to connect or implicitly execute, thereby cancelling the
  transaction.   While this is not the recommended way to work with engines
  and connections, it is nonetheless a confusing behavioral change as when
  using [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool), the transaction should stay open
  regardless of what else is done with the same engine in the same thread.
  The `use_threadlocal` flag remains deprecated however the
  [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool) now implements its own version of the same
  logic.
  References: [#4585](https://www.sqlalchemy.org/trac/ticket/4585)
- Fixed bug where using `copy.copy()` or `copy.deepcopy()` on
  [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) would cause the items within the list to be
  duplicated, due to an inconsistency in how Python pickle and copy both make
  use of `__getstate__()` and `__setstate__()` regarding lists.  In order
  to resolve, a `__reduce_ex__` method had to be added to
  [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList).  In order to maintain backwards compatibility with
  existing pickles based on `__getstate__()`, the `__setstate__()` method
  remains as well; the test suite asserts that pickles made against the old
  version of the class can still be deserialized by the pickle module.
  References: [#4603](https://www.sqlalchemy.org/trac/ticket/4603)

## 1.3.2

Released: April 2, 2019

### orm

- Restored instance-level support for plain Python descriptors, e.g.
  `@property` objects, in conjunction with association proxies, in that if
  the proxied object is not within ORM scope at all, it gets classified as
  “ambiguous” but is proxed directly.  For class level access, a basic class
  level``__get__()`` now returns the
  `AmbiguousAssociationProxyInstance` directly, rather than raising
  its exception, which is the closest approximation to the previous behavior
  that returned the [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) itself that’s possible.  Also
  improved the stringification of these objects to be more descriptive of
  current state.
  References: [#4573](https://www.sqlalchemy.org/trac/ticket/4573), [#4574](https://www.sqlalchemy.org/trac/ticket/4574)
- Fixed bug where use of [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) or other aliased construct
  would not properly adapt when the aliased target were used as the
  [Select.correlate_except()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate_except) target of a subquery used inside of a
  [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property). This required a fix to the clause adaption
  mechanics to properly handle a selectable that shows up in the “correlate
  except” list, in a similar manner as which occurs for selectables that show
  up in the “correlate” list.  This is ultimately a fairly fundamental bug
  that has lasted for a long time but it is hard to come across it.
  References: [#4537](https://www.sqlalchemy.org/trac/ticket/4537)
- Fixed regression where a new error message that was supposed to raise when
  attempting to link a relationship option to an AliasedClass without using
  [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) would instead raise an `AttributeError`.
  Note that in 1.3, it is no longer valid to create an option path from a
  plain mapper relationship to an [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) without using
  [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type).
  References: [#4566](https://www.sqlalchemy.org/trac/ticket/4566)

### sql

- Thanks to [TypeEngine methods bind_expression, column_expression work with Variant, type-specific types](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3981), we no longer need to rely on recipes that
  subclass dialect-specific types directly, [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) can now
  handle all cases.   Additionally, the above change made it slightly less
  likely that a direct subclass of a base SQLAlchemy type would work as
  expected, which could be misleading.  Documentation has been updated to use
  [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) for these examples including the PostgreSQL
  “ArrayOfEnum” example datatype and direct support for the “subclass a type
  directly” has been removed.
  References: [#4580](https://www.sqlalchemy.org/trac/ticket/4580)

### postgresql

- Added support for parameter-less connection URLs for the psycopg2 dialect,
  meaning, the URL can be passed to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) as
  `"postgresql+psycopg2://"` with no additional arguments to indicate an
  empty DSN passed to libpq, which indicates to connect to “localhost” with
  no username, password, or database given. Pull request courtesy Julian
  Mehnle.
  References: [#4562](https://www.sqlalchemy.org/trac/ticket/4562)
- Modified the [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of) parameter so that if a
  join or other composed selectable is passed, the individual [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  objects will be filtered from it, allowing one to pass a join() object to
  the parameter, as occurs normally when using joined table inheritance with
  the ORM.  Pull request courtesy Raymond Lu.
  References: [#4550](https://www.sqlalchemy.org/trac/ticket/4550)

## 1.3.1

Released: March 9, 2019

### orm

- Fixed regression where an association proxy linked to a synonym would no
  longer work, both at instance level and at class level.
  References: [#4522](https://www.sqlalchemy.org/trac/ticket/4522)

### mssql

- A commit() is emitted after an isolation level change to SNAPSHOT, as both
  pyodbc and pymssql open an implicit transaction which blocks subsequent SQL
  from being emitted in the current transaction.
  This change is also **backported** to: 1.2.19
  References: [#4536](https://www.sqlalchemy.org/trac/ticket/4536)
- Fixed regression in SQL Server reflection due to [#4393](https://www.sqlalchemy.org/trac/ticket/4393) where the
  removal of open-ended `**kw` from the [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) datatype caused
  reflection of this type to fail due to a “scale” argument being passed.
  References: [#4525](https://www.sqlalchemy.org/trac/ticket/4525)

## 1.3.0

Released: March 4, 2019

### orm

- The [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get) method can now accept a dictionary of attribute keys
  and values as a means of indicating the primary key value to load; is
  particularly useful for composite primary keys.  Pull request courtesy
  Sanjana S.
  References: [#4316](https://www.sqlalchemy.org/trac/ticket/4316)
- A SQL expression can now be assigned to a primary key attribute for an ORM
  flush in the same manner as ordinary attributes as described in
  [Embedding SQL Insert/Update Expressions into a Flush](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#flush-embedded-sql-expressions) where the expression will be evaluated
  and then returned to the ORM using RETURNING, or in the case of pysqlite,
  works using the cursor.lastrowid attribute.Requires either a database that
  supports RETURNING (e.g. Postgresql, Oracle, SQL Server) or pysqlite.
  References: [#3133](https://www.sqlalchemy.org/trac/ticket/3133)

### engine

- Revised the formatting for [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) when stringified. Each
  error detail is broken up over multiple newlines instead of spaced out on a
  single line.  Additionally, the SQL representation now stringifies the SQL
  statement rather than using `repr()`, so that newlines are rendered as is.
  Pull request courtesy Nate Clark.
  See also
  [Changed StatementError formatting (newlines and %s)](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4500)
  References: [#4500](https://www.sqlalchemy.org/trac/ticket/4500)

### sql

- The [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) class and related subclasses [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE),
  [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral) and [TableSample](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableSample) have been reworked so that it is
  not possible for a user to construct the objects directly.  These constructs
  require that the standalone construction function or selectable-bound method
  be used to instantiate new objects.
  References: [#4509](https://www.sqlalchemy.org/trac/ticket/4509)

### schema

- Added new parameters [Table.resolve_fks](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.resolve_fks) and
  [MetaData.reflect.resolve_fks](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect.params.resolve_fks) which when set to False will
  disable the automatic reflection of related tables encountered in
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects, which can both reduce SQL overhead for omitted
  tables as well as avoid tables that can’t be reflected for database-specific
  reasons.  Two [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects present in the same [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  collection can still refer to each other even if the reflection of the two
  tables occurred separately.
  References: [#4517](https://www.sqlalchemy.org/trac/ticket/4517)

## 1.3.0b3

Released: February 8, 2019

### orm

- Improved the behavior of [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) in conjunction with
  loader options, in particular wildcard operations as well as
  [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only).  The polymorphic object will be more accurately
  targeted so that column-level options on the entity will correctly take
  effect.The issue is a continuation of the same kinds of things fixed in
  [#4468](https://www.sqlalchemy.org/trac/ticket/4468).
  References: [#4469](https://www.sqlalchemy.org/trac/ticket/4469)

### orm declarative

- Added some helper exceptions that invoke when a mapping based on
  [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase), [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection), or
  `AutoMap` is used before the mapping is ready to be used, which
  contain descriptive information on the class, rather than falling through
  into other failure modes that are less informative.
  References: [#4470](https://www.sqlalchemy.org/trac/ticket/4470)

### sql

- Fully removed the behavior of strings passed directly as components of a
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) or [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object being coerced to [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
  constructs automatically; the warning that has been emitted is now an
  ArgumentError or in the case of order_by() / group_by() a CompileError.
  This has emitted a warning since version 1.0 however its presence continues
  to create concerns for the potential of mis-use of this behavior.
  Note that public CVEs have been posted for order_by() / group_by() which
  are resolved by this commit:  CVE-2019-7164  CVE-2019-7548
  See also
  [Coercion of string SQL fragments to text() fully removed](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4481)
  References: [#4481](https://www.sqlalchemy.org/trac/ticket/4481)
- Quoting is applied to [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) names, those which are usually but
  not necessarily generated from the [sqlalchemy.sql.expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) construct,  at compile
  time if they contain illegal characters, such as spaces or punctuation. The
  names are as before treated as case insensitive however, meaning if the
  names contain uppercase or mixed case characters, that alone does not
  trigger quoting. The case insensitivity is currently maintained for
  backwards compatibility.
  References: [#4467](https://www.sqlalchemy.org/trac/ticket/4467)
- Added “SQL phrase validation” to key DDL phrases that are accepted as plain
  strings, including [ForeignKeyConstraint.on_delete](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.on_delete),
  [ForeignKeyConstraint.on_update](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.on_update),
  [ExcludeConstraint.using](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint.params.using),
  [ForeignKeyConstraint.initially](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.initially), for areas where a series of SQL
  keywords only are expected.Any non-space characters that suggest the phrase
  would need to be quoted will raise a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError).   This change
  is related to the series of changes committed as part of [#4481](https://www.sqlalchemy.org/trac/ticket/4481).
  References: [#4481](https://www.sqlalchemy.org/trac/ticket/4481)

### postgresql

- Fixed issue where using an uppercase name for an index type (e.g. GIST,
  BTREE, etc. ) or an EXCLUDE constraint would treat it as an identifier to
  be quoted, rather than rendering it as is. The new behavior converts these
  types to lowercase and ensures they contain only valid SQL characters.
  References: [#4473](https://www.sqlalchemy.org/trac/ticket/4473)

### tests

- The test system has removed support for Nose, which is unmaintained for
  several years and is producing warnings under Python 3. The test suite is
  currently standardized on Pytest.  Pull request courtesy Parth Shandilya.
  References: [#4460](https://www.sqlalchemy.org/trac/ticket/4460)

### misc

- Implemented a more comprehensive assignment operation (e.g. “bulk replace”)
  when using association proxy with sets or dictionaries.  Fixes the problem
  of redundant proxy objects being created to replace the old ones, which
  leads to excessive events and SQL and in the case of unique constraints
  will cause the flush to fail.
  See also
  [Implemented bulk replace for sets, dicts with AssociationProxy](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-2642)
  References: [#2642](https://www.sqlalchemy.org/trac/ticket/2642)

## 1.3.0b2

Released: January 25, 2019

### general

- A large change throughout the library has ensured that all objects,
  parameters, and behaviors which have been noted as deprecated or legacy now
  emit `DeprecationWarning` warnings when invoked.As the Python 3
  interpreter now defaults to displaying deprecation warnings, as well as that
  modern test suites based on tools like tox and pytest tend to display
  deprecation warnings, this change should make it easier to note what API
  features are obsolete. A major rationale for this change is so that long-
  deprecated features that nonetheless still see continue to see real world
  use can  finally be removed in the near future; the biggest example of this
  are the `SessionExtension` and `MapperExtension` classes as
  well as a handful of other pre-event extension hooks, which have been
  deprecated since version 0.7 but still remain in the library.  Another is
  that several major longstanding behaviors are to be deprecated as well,
  including the threadlocal engine strategy, the convert_unicode flag, and non
  primary mappers.
  See also
  [Deprecation warnings are emitted for all deprecated elements; new deprecations added](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4393-general)
  References: [#4393](https://www.sqlalchemy.org/trac/ticket/4393)

### orm

- Implemented a new feature whereby the [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) construct can
  now be used as the target of a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).  This allows the
  concept of “non primary mappers” to no longer be necessary, as the
  [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) is much easier to configure and automatically inherits
  all the relationships of the mapped class, as well as preserves the
  ability for loader options to work normally.
  See also
  [Relationship to AliasedClass replaces the need for non primary mappers](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4423)
  References: [#4423](https://www.sqlalchemy.org/trac/ticket/4423)
- Added new [MapperEvents.before_mapper_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_mapper_configured) event.   This
  event complements the other “configure” stage mapper events with a per
  mapper event that receives each [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) right before its
  configure step, and additionally may be used to prevent or delay the
  configuration of specific [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects using a new
  return value `interfaces.EXT_SKIP`.  See the
  documentation link for an example.
  See also
  [MapperEvents.before_mapper_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_mapper_configured)
  References: [#4397](https://www.sqlalchemy.org/trac/ticket/4397)
- Added a new function [close_all_sessions()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.close_all_sessions) which takes
  over the task of the [Session.close_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close_all) method, which
  is now deprecated as this is confusing as a classmethod.
  Pull request courtesy Augustin Trancart.
  References: [#4412](https://www.sqlalchemy.org/trac/ticket/4412)
- Fixed long-standing issue where duplicate collection members would cause a
  backref to delete the association between the member and its parent object
  when one of the duplicates were removed, as occurs as a side effect of
  swapping two objects in one statement.
  See also
  [Many-to-one backref checks for collection duplicates during remove operation](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-1103)
  References: [#1103](https://www.sqlalchemy.org/trac/ticket/1103)
- Extended the fix first made as part of [#3287](https://www.sqlalchemy.org/trac/ticket/3287), where a loader option
  made against a subclass using a wildcard would extend itself to include
  application of the wildcard to attributes on the super classes as well, to a
  “bound” loader option as well, e.g. in an expression like
  `Load(SomeSubClass).load_only('foo')`.  Columns that are part of the
  parent class of `SomeSubClass` will also be excluded in the same way as if
  the unbound option `load_only('foo')` were used.
  References: [#4373](https://www.sqlalchemy.org/trac/ticket/4373)
- Improved error messages emitted by the ORM in the area of loader option
  traversal.  This includes early detection of mis-matched loader strategies
  along with a clearer explanation why these strategies don’t match.
  References: [#4433](https://www.sqlalchemy.org/trac/ticket/4433)
- The “remove” event for collections is now called before the item is removed
  in the case of the `collection.remove()` method, as is consistent with the
  behavior for most other forms of collection item removal (such as
  `__delitem__`, replacement under `__setitem__`).  For `pop()` methods,
  the remove event still fires after the operation.
- Added accessors for execution options to Core and ORM, via
  [Query.get_execution_options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get_execution_options),
  [Connection.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_execution_options),
  [Engine.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.get_execution_options), and
  [Executable.get_execution_options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.get_execution_options).  PR courtesy Daniel Lister.
  References: [#4464](https://www.sqlalchemy.org/trac/ticket/4464)
- Fixed issue in association proxy due to [#3423](https://www.sqlalchemy.org/trac/ticket/3423) which caused the use
  of custom [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator) objects with hybrid attributes, such as
  the one demonstrated in  the `dictlike-polymorphic` example to not
  function within an association proxy.  The strictness that was added in
  [#3423](https://www.sqlalchemy.org/trac/ticket/3423) has been relaxed, and additional logic to accommodate for
  an association proxy that links to a custom hybrid have been added.
  References: [#4446](https://www.sqlalchemy.org/trac/ticket/4446)
- Implemented the `.get_history()` method, which also implies availability
  of [AttributeState.history](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeState.history), for [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) attributes.
  Previously, trying to access attribute history via a synonym would raise an
  `AttributeError`.
  References: [#3777](https://www.sqlalchemy.org/trac/ticket/3777)

### orm declarative

- Added a `__clause_element__()` method to [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) which
  can allow the usage of a not-fully-declared column or deferred attribute in
  a declarative mapped class slightly more friendly when it’s used in a
  constraint or other column-oriented scenario within the class declaration,
  though this still can’t work in open-ended expressions; prefer to call the
  [ColumnProperty.expression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.expression) attribute if receiving `TypeError`.
  References: [#4372](https://www.sqlalchemy.org/trac/ticket/4372)

### engine

- Added public accessor `QueuePool.timeout()` that returns the configured
  timeout for a [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) object.  Pull request courtesy Irina Delamare.
  References: [#3689](https://www.sqlalchemy.org/trac/ticket/3689)
- The “threadlocal” engine strategy which has been a legacy feature of
  SQLAlchemy since around version 0.2 is now deprecated, along with the
  [Pool.threadlocal](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool.params.threadlocal) parameter of [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) which has no
  effect in most modern use cases.
  See also
  [“threadlocal” engine strategy deprecated](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4393-threadlocal)
  References: [#4393](https://www.sqlalchemy.org/trac/ticket/4393)

### sql

- Amended the [AnsiFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.AnsiFunction) class, the base of common SQL
  functions like `CURRENT_TIMESTAMP`, to accept positional arguments
  like a regular ad-hoc function.  This to suit the case that many of
  these functions on specific backends accept arguments such as
  “fractional seconds” precision and such.  If the function is created
  with arguments, it renders the parenthesis and the arguments.  If
  no arguments are present, the compiler generates the non-parenthesized form.
  References: [#4386](https://www.sqlalchemy.org/trac/ticket/4386)
- The [create_engine.convert_unicode](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.convert_unicode) and
  [String.convert_unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String.params.convert_unicode) parameters have been deprecated.  These
  parameters were built back when most Python DBAPIs had little to no support
  for Python Unicode objects, and SQLAlchemy needed to take on the very
  complex task of marshalling data and SQL strings between Unicode and
  bytestrings throughout the system in a performant way.  Thanks to Python 3,
  DBAPIs were compelled to adapt to Unicode-aware APIs and today all DBAPIs
  supported by SQLAlchemy support Unicode natively, including on Python 2,
  allowing this long-lived and very complicated feature to finally be (mostly)
  removed.  There are still of course a few Python 2 edge cases where
  SQLAlchemy has to deal with Unicode however these are handled automatically;
  in modern use, there should be no need for end-user interaction with these
  flags.
  See also
  [convert_unicode parameters deprecated](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4393-convertunicode)
  References: [#4393](https://www.sqlalchemy.org/trac/ticket/4393)

### mssql

- The `literal_processor` for the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) and
  [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText) datatypes now render an `N` character in front of
  the literal string expression as required by SQL Server for Unicode string
  values rendered in SQL expressions.
  References: [#4442](https://www.sqlalchemy.org/trac/ticket/4442)

### misc

- Fixed a regression in 1.3.0b1 caused by [#3423](https://www.sqlalchemy.org/trac/ticket/3423) where association
  proxy objects that access an attribute that’s only present on a polymorphic
  subclass would raise an `AttributeError` even though the actual instance
  being accessed was an instance of that subclass.
  References: [#4401](https://www.sqlalchemy.org/trac/ticket/4401)

## 1.3.0b1

Released: November 16, 2018

### orm

- Added new feature [Query.only_return_tuples()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.only_return_tuples).  Causes the
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object to return keyed tuple objects unconditionally even
  if the query is against a single entity.   Pull request courtesy Eric
  Atkin.
  This change is also **backported** to: 1.2.5
- Added new flag [Session.bulk_save_objects.preserve_order](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects.params.preserve_order) to the
  [Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects) method, which defaults to True. When set
  to False, the given mappings will be grouped into inserts and updates per
  each object type, to allow for greater opportunities to batch common
  operations together.  Pull request courtesy Alessandro Cucci.
- The “selectin” loader strategy now omits the JOIN in the case of a simple
  one-to-many load, where it instead relies loads only from the related
  table, relying upon the foreign key columns of the related table in order
  to match up to primary keys in the parent table.   This optimization can be
  disabled by setting the [relationship.omit_join](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.omit_join) flag to False.
  Many thanks to Jayson Reis for the efforts on this.
  See also
  [selectin loading no longer uses JOIN for simple one-to-many](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4340)
  References: [#4340](https://www.sqlalchemy.org/trac/ticket/4340)
- Added `.info` dictionary to the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) class, the object
  that comes from calling [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) on a mapped object.
  See also
  [info dictionary added to InstanceState](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4257)
  References: [#4257](https://www.sqlalchemy.org/trac/ticket/4257)
- Fixed bug where use of [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral) construct in conjunction with
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) as well as `Query.select_entity_from()` would not
  apply clause adaption to the right side of the join.   “lateral” introduces
  the use case of the right side of a join being correlatable.  Previously,
  adaptation of this clause wasn’t considered.   Note that in 1.2 only,
  a selectable introduced by [Query.subquery()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.subquery) is still not adapted
  due to [#4304](https://www.sqlalchemy.org/trac/ticket/4304); the selectable needs to be produced by the
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) function to be the right side of the “lateral” join.
  This change is also **backported** to: 1.2.12
  References: [#4334](https://www.sqlalchemy.org/trac/ticket/4334)
- Fixed issue regarding passive_deletes=”all”, where the foreign key
  attribute of an object is maintained with its value even after the object
  is removed from its parent collection.  Previously, the unit of work would
  set this to NULL even though passive_deletes indicated it should not be
  modified.
  See also
  [passive_deletes=’all’ will leave FK unchanged for object removed from collection](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3844)
  References: [#3844](https://www.sqlalchemy.org/trac/ticket/3844)
- Improved the behavior of a relationship-bound many-to-one object expression
  such that the retrieval of column values on the related object are now
  resilient against the object being detached from its parent
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), even if the attribute has been expired.  New features
  within the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) are used to memoize the last known value
  of a particular column attribute before its expired, so that the expression
  can still evaluate when the object is detached and expired at the same
  time.  Error conditions are also improved using modern attribute state
  features to produce more specific messages as needed.
  See also
  [Improvement to the behavior of many-to-one query expressions](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4359)
  References: [#4359](https://www.sqlalchemy.org/trac/ticket/4359)
- The ORM now doubles the “FOR UPDATE” clause within the subquery that
  renders in conjunction with joined eager loading in some cases, as it has
  been observed that MySQL does not lock the rows from a subquery.   This
  means the query renders with two FOR UPDATE clauses; note that on some
  backends such as Oracle, FOR UPDATE clauses on subqueries are silently
  ignored since they are unnecessary.  Additionally, in the case of the “OF”
  clause used primarily with PostgreSQL, the FOR UPDATE is rendered only on
  the inner subquery when this is used so that the selectable can be targeted
  to the table within the SELECT statement.
  See also
  [FOR UPDATE clause is rendered within the joined eager load subquery as well as outside](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4246)
  References: [#4246](https://www.sqlalchemy.org/trac/ticket/4246)
- Refactored [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) to further clarify the individual components
  of structuring the join. This refactor adds the ability for
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) to determine the most appropriate “left” side of the
  join when there is more than one element in the FROM list or the query is
  against multiple entities.  If more than one FROM/entity matches, an error
  is raised that asks for an ON clause to be specified to resolve the
  ambiguity.  In particular this targets the regression we saw in
  [#4363](https://www.sqlalchemy.org/trac/ticket/4363) but is also of general use.   The codepaths within
  [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) are now easier to follow and the error cases are
  decided more specifically at an earlier point in the operation.
  See also
  [Query.join() handles ambiguity in deciding the “left” side more explicitly](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4365)
  References: [#4365](https://www.sqlalchemy.org/trac/ticket/4365)
- Fixed long-standing issue in [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) where a scalar subquery such
  as produced by [Query.exists()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists), [Query.as_scalar()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.as_scalar) and other
  derivations from [Query.statement](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.statement) would not correctly be adapted
  when used in a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that required entity adaptation, such as
  when the query were turned into a union, or a from_self(), etc. The change
  removes the “no adaptation” annotation from the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) object
  produced by the [Query.statement](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.statement) accessor.
  References: [#4304](https://www.sqlalchemy.org/trac/ticket/4304)
- An informative exception is re-raised when a primary key value is not
  sortable in Python during an ORM flush under Python 3, such as an `Enum`
  that has no `__lt__()` method; normally Python 3 raises a `TypeError`
  in this case.   The flush process sorts persistent objects by primary key
  in Python so the values must be sortable.
  References: [#4232](https://www.sqlalchemy.org/trac/ticket/4232)
- Removed the collection converter used by the [MappedCollection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.MappedCollection)
  class. This converter was used only to assert that the incoming dictionary
  keys matched that of their corresponding objects, and only during a bulk set
  operation.  The converter can interfere with a custom validator or
  [AttributeEvents.bulk_replace()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.bulk_replace) listener that wants to convert
  incoming values further.  The `TypeError` which would be raised by this
  converter when an incoming key didn’t match the value is removed; incoming
  values during a bulk assignment will be keyed to their value-generated key,
  and not the key that’s explicitly present in the dictionary.
  Overall, @converter is superseded by the
  [AttributeEvents.bulk_replace()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.bulk_replace) event handler added as part of
  [#3896](https://www.sqlalchemy.org/trac/ticket/3896).
  References: [#3604](https://www.sqlalchemy.org/trac/ticket/3604)
- Added new behavior to the lazy load that takes place when the “old” value of
  a many-to-one is retrieved, such that exceptions which would be raised due
  to either `lazy="raise"` or a detached session error are skipped.
  See also
  [Many-to-one replacement won’t raise for “raiseload” or detached for “old” object](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4353)
  References: [#4353](https://www.sqlalchemy.org/trac/ticket/4353)
- A long-standing oversight in the ORM, the `__delete__` method for a many-
  to-one relationship was non-functional, e.g. for an operation such as `del
  a.b`.  This is now implemented and is equivalent to setting the attribute
  to `None`.
  See also
  [“del” implemented for ORM attributes](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4354)
  References: [#4354](https://www.sqlalchemy.org/trac/ticket/4354)

### orm declarative

- Fixed bug where declarative would not update the state of the
  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) as far as what attributes were present, when additional
  attributes were added or removed after the mapper attribute collections had
  already been called and memoized.  Additionally, a `NotImplementedError`
  is now raised if a fully mapped attribute (e.g. column, relationship, etc.)
  is deleted from a class that is currently mapped, since the mapper will not
  function correctly if the attribute has been removed.
  References: [#4133](https://www.sqlalchemy.org/trac/ticket/4133)

### engine

- Added new “lifo” mode to [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool), typically enabled by setting
  the flag [create_engine.pool_use_lifo](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_use_lifo) to True.   “lifo” mode
  means the same connection just checked in will be the first to be checked
  out again, allowing excess connections to be cleaned up from the server
  side during periods of the pool being only partially utilized.  Pull request
  courtesy Taem Park.
  See also
  [New last-in-first-out strategy for QueuePool](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-pr467)

### sql

- Refactored [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler) to expose a
  [SQLCompiler.group_by_clause()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.group_by_clause) method similar to the
  [SQLCompiler.order_by_clause()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler.order_by_clause) and `SQLCompiler.limit_clause()`
  methods, which can be overridden by dialects to customize how GROUP BY
  renders.  Pull request courtesy Samuel Chou.
  This change is also **backported** to: 1.2.13
- Added [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) to the “string SQL” system that will render a
  meaningful string expression (`"<next sequence value: my_sequence>"`)
  when stringifying without a dialect a statement that includes a “sequence
  nextvalue” expression, rather than raising a compilation error.
  References: [#4144](https://www.sqlalchemy.org/trac/ticket/4144)
- Added new naming convention tokens `column_0N_name`, `column_0_N_name`,
  etc., which will render the names / keys / labels for all columns referenced
  by a particular constraint in a sequence.  In order to accommodate for the
  length of such a naming convention, the SQL compiler’s auto-truncation
  feature now applies itself to constraint names as well, which creates a
  shortened, deterministically generated name for the constraint that will
  apply to a target backend without going over the character limit of that
  backend.
  The change also repairs two other issues.  One is that the  `column_0_key`
  token wasn’t available even though this token was documented, the other was
  that the `referred_column_0_name` token would  inadvertently render the
  `.key` and not the `.name` of the column if these two values were
  different.
  See also
  [New multi-column naming convention tokens, long name truncation](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3989)
  References: [#3989](https://www.sqlalchemy.org/trac/ticket/3989)
- Added new logic to the “expanding IN” bound parameter feature whereby if
  the given list is empty, a special “empty set” expression that is specific
  to different backends is generated, thus allowing IN expressions to be
  fully dynamic including empty IN expressions.
  See also
  [Expanding IN feature now supports empty lists](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4271)
  References: [#4271](https://www.sqlalchemy.org/trac/ticket/4271)
- The Python builtin `dir()` is now supported for a SQLAlchemy “properties”
  object, such as that of a Core columns collection (e.g. `.c`),
  `mapper.attrs`, etc.  Allows iPython autocompletion to work as well.
  Pull request courtesy Uwe Korn.
- Added new feature [FunctionElement.as_comparison()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.as_comparison) which allows a SQL
  function to act as a binary comparison operation that can work within the
  ORM.
  See also
  [Binary comparison interpretation for SQL functions](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3831)
  References: [#3831](https://www.sqlalchemy.org/trac/ticket/3831)
- Added “like” based operators as “comparison” operators, including
  [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith) [ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith) [ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike) [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) among many
  others, so that all of these operators can be the basis for an ORM
  “primaryjoin” condition.
  References: [#4302](https://www.sqlalchemy.org/trac/ticket/4302)
- Fixed issue with [TypeEngine.bind_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_expression) and
  [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression) methods where these methods would not
  work if the target type were part of a [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant), or other target
  type of a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator).  Additionally, the SQL compiler now
  calls upon the dialect-level implementation when it renders these methods
  so that dialects can now provide for SQL-level processing for built-in
  types.
  See also
  [TypeEngine methods bind_expression, column_expression work with Variant, type-specific types](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3981)
  References: [#3981](https://www.sqlalchemy.org/trac/ticket/3981)

### postgresql

- Added new PG type [REGCLASS](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.REGCLASS) which assists in casting
  table names to OID values.  Pull request courtesy Sebastian Bank.
  This change is also **backported** to: 1.2.7
  References: [#4160](https://www.sqlalchemy.org/trac/ticket/4160)
- Added rudimental support for reflection of PostgreSQL
  partitioned tables, e.g. that relkind=’p’ is added to reflection
  queries that return table information.
  See also
  [Added basic reflection support for PostgreSQL partitioned tables](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4237)
  References: [#4237](https://www.sqlalchemy.org/trac/ticket/4237)

### mysql

- Support added for the “WITH PARSER” syntax of CREATE FULLTEXT INDEX
  in MySQL, using the `mysql_with_parser` keyword argument.  Reflection
  is also supported, which accommodates MySQL’s special comment format
  for reporting on this option as well.  Additionally, the “FULLTEXT” and
  “SPATIAL” index prefixes are now reflected back into the `mysql_prefix`
  index option.
  References: [#4219](https://www.sqlalchemy.org/trac/ticket/4219)
- Added support for the parameters in an ON DUPLICATE KEY UPDATE statement on
  MySQL to be ordered, since parameter order in a MySQL UPDATE clause is
  significant, in a similar manner as that described at
  [Parameter Ordered Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates).  Pull request courtesy Maxim Bublis.
  See also
  [Control of parameter ordering within ON DUPLICATE KEY UPDATE](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-mysql-ondupordering)
- The “pre-ping” feature of the connection pool now uses
  the `ping()` method of the DBAPI connection in the case of
  mysqlclient, PyMySQL and mysql-connector-python.  Pull request
  courtesy Maxim Bublis.
  See also
  [Protocol-level ping now used for pre-ping](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-mysql-ping)

### sqlite

- Added support for SQLite’s json functionality via the new
  SQLite implementation for [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON), [JSON](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.JSON).
  The name used for the type is `JSON`, following an example found at
  SQLite’s own documentation. Pull request courtesy Ilja Everilä.
  See also
  [Support for SQLite JSON Added](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3850)
  References: [#3850](https://www.sqlalchemy.org/trac/ticket/3850)
- Implemented the SQLite `ON CONFLICT` clause as understood at the DDL
  level, e.g. for primary key, unique, and CHECK constraints as well as
  specified on a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to satisfy inline primary key and NOT NULL.
  Pull request courtesy Denis Kataev.
  See also
  [Support for SQLite ON CONFLICT in constraints added](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4360)
  References: [#4360](https://www.sqlalchemy.org/trac/ticket/4360)

### mssql

- Added `fast_executemany=True` parameter to the SQL Server pyodbc dialect,
  which enables use of pyodbc’s new performance feature of the same name
  when using Microsoft ODBC drivers.
  See also
  [Support for pyodbc fast_executemany](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4158)
  References: [#4158](https://www.sqlalchemy.org/trac/ticket/4158)
- Deprecated the use of [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) with SQL Server in order to affect
  the “start” and “increment” of the IDENTITY value, in favor of new
  parameters `mssql_identity_start` and `mssql_identity_increment` which
  set these parameters directly.  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) will be used to generate
  real `CREATE SEQUENCE` DDL with SQL Server in a future release.
  See also
  [New parameters to affect IDENTITY start and increment, use of Sequence deprecated](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4362)
  References: [#4362](https://www.sqlalchemy.org/trac/ticket/4362)

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
  This change is also **backported** to: 1.2.9
  References: [#4290](https://www.sqlalchemy.org/trac/ticket/4290)
- Updated the parameters that can be sent to the cx_Oracle DBAPI to both allow
  for all current parameters as well as for future parameters not added yet.
  In addition, removed unused parameters that were deprecated in version 1.2,
  and additionally we are now defaulting “threaded” to False.
  See also
  [cx_Oracle connect arguments modernized, deprecated parameters removed](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4369)
  References: [#4369](https://www.sqlalchemy.org/trac/ticket/4369)
- The Oracle dialect will no longer use the NCHAR/NCLOB datatypes
  represent generic unicode strings or clob fields in conjunction with
  [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) and [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText) unless the flag
  `use_nchar_for_unicode=True` is passed to [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) -
  this includes CREATE TABLE behavior as well as `setinputsizes()` for
  bound parameters.   On the read side, automatic Unicode conversion under
  Python 2 has been added to CHAR/VARCHAR/CLOB result rows, to match the
  behavior of cx_Oracle under Python 3.  In order to mitigate the performance
  hit under Python 2, SQLAlchemy’s very performant (when C extensions
  are built) native Unicode handlers are used under Python 2.
  See also
  [National char datatypes de-emphasized for generic unicode, re-enabled with option](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4242)
  References: [#4242](https://www.sqlalchemy.org/trac/ticket/4242)

### misc

- Added new attribute [Query.lazy_loaded_from](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.lazy_loaded_from) which is populated
  with an [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) that is using this [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in
  order to lazy load a relationship.  The rationale for this is that
  it serves as a hint for the horizontal sharding feature to use, such that
  the identity token of the state can be used as the default identity token
  to use for the query within id_chooser().
  This change is also **backported** to: 1.2.9
  References: [#4243](https://www.sqlalchemy.org/trac/ticket/4243)
- Added new feature [BakedQuery.to_query()](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery.to_query), which allows for a
  clean way of using one [BakedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery) as a subquery inside of another
  [BakedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery) without needing to refer explicitly to a
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
  References: [#4318](https://www.sqlalchemy.org/trac/ticket/4318)
- The [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) now has standard column comparison operations
  such as [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like) and
  [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith) available when the target attribute is a
  plain column - the EXISTS expression that joins to the target table is
  rendered as usual, but the column expression is then use within the WHERE
  criteria of the EXISTS.  Note that this alters the behavior of the
  `.contains()` method on the association proxy to make use of
  [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains) when used on a column-based attribute.
  See also
  [AssociationProxy now provides standard column operators for a column-oriented target](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4351)
  References: [#4351](https://www.sqlalchemy.org/trac/ticket/4351)
- Added support for bulk [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) and [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete)
  to the [ShardedQuery](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html#sqlalchemy.ext.horizontal_shard.ShardedQuery) class within the horizontal sharding
  extension.  This also adds an additional expansion hook to the
  bulk update/delete methods `Query._execute_crud()`.
  See also
  [Horizontal Sharding extension supports bulk update and delete methods](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4196)
  References: [#4196](https://www.sqlalchemy.org/trac/ticket/4196)
- Reworked [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) to store state that’s specific to a
  parent class in a separate object, so that a single
  [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) can serve for multiple parent classes, as is
  intrinsic to inheritance, without any ambiguity in the state returned by it.
  A new method [AssociationProxy.for_class()](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.for_class) is added to allow
  inspection of class-specific state.
  See also
  [AssociationProxy stores class-specific state on a per-class basis](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-3423)
  References: [#3423](https://www.sqlalchemy.org/trac/ticket/3423)
- The long-standing behavior of the association proxy collection maintaining
  only a weak reference to the parent object is reverted; the proxy will now
  maintain a strong reference to the parent for as long as the proxy
  collection itself is also in memory, eliminating the “stale association
  proxy” error. This change is being made on an experimental basis to see if
  any use cases arise where it causes side effects.
  See also
  [New Features and Improvements - Core](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4268)
  References: [#4268](https://www.sqlalchemy.org/trac/ticket/4268)
- Fixed multiple issues regarding de-association of scalar objects with the
  association proxy.  `del` now works, and additionally a new flag
  [AssociationProxy.cascade_scalar_deletes](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.params.cascade_scalar_deletes) is added, which when
  set to True indicates that setting a scalar attribute to `None` or
  deleting via `del` will also set the source association to `None`.
  See also
  [Association proxy has new cascade_scalar_deletes flag](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4308)
  References: [#4308](https://www.sqlalchemy.org/trac/ticket/4308)
