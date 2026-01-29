# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 1.0 Changelog

## 1.0.19

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
  References: [#4035](https://www.sqlalchemy.org/trac/ticket/4035)

## 1.0.18

Released: July 24, 2017

### oracle

- A fix to cx_Oracle’s WITH_UNICODE mode which was uncovered by the
  fact that cx_Oracle 5.3 now seems to hardcode this flag on in
  the build; an internal method that uses this mode wasn’t using
  the correct signature.
  References: [#3937](https://www.sqlalchemy.org/trac/ticket/3937)

### tests

- Fixed issue in testing fixtures which was incompatible with a change
  made as of Python 3.6.2 involving context managers.
  References: [#4034](https://www.sqlalchemy.org/trac/ticket/4034)

## 1.0.17

Released: January 17, 2017

### orm

- Fixed bug involving joined eager loading against multiple entities
  when polymorphic inheritance is also in use which would throw
  “‘NoneType’ object has no attribute ‘isa’”.  The issue was introduced
  by the fix for [#3611](https://www.sqlalchemy.org/trac/ticket/3611).
  References: [#3884](https://www.sqlalchemy.org/trac/ticket/3884)

### misc

- Fixed Python 3.6 DeprecationWarnings related to escaped strings without
  the ‘r’ modifier, and added test coverage for Python 3.6.
  References: [#3886](https://www.sqlalchemy.org/trac/ticket/3886)

## 1.0.16

Released: November 15, 2016

### orm

- Fixed bug in [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) where an alternate-named
  primary key attribute would not track properly into the UPDATE statement.
  References: [#3849](https://www.sqlalchemy.org/trac/ticket/3849)
- Fixed bug where joined eager loading would fail for a polymorphically-
  loaded mapper, where the polymorphic_on was set to an un-mapped
  expression such as a CASE expression.
  References: [#3800](https://www.sqlalchemy.org/trac/ticket/3800)
- Fixed bug where the ArgumentError raised for an invalid bind
  sent to a Session via [Session.bind_mapper()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_mapper),
  [Session.bind_table()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_table),
  or the constructor would fail to be correctly raised.
  References: [#3798](https://www.sqlalchemy.org/trac/ticket/3798)
- Fixed bug in `Session.bulk_save()` where an UPDATE would
  not function correctly in conjunction with a mapping that
  implements a version id counter.
  References: [#3781](https://www.sqlalchemy.org/trac/ticket/3781)
- Fixed bug where the [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs),
  [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors) and other derived attributes would
  fail to refresh when mapper properties or other ORM constructs were
  added to the mapper/class after these  accessors were first called.
  References: [#3778](https://www.sqlalchemy.org/trac/ticket/3778)

### mssql

- Changed the query used to get “default schema name”, from one that
  queries the database principals table to using the
  “schema_name()” function, as issues have been reported that the
  former system was unavailable on the Azure Data Warehouse edition.
  It is hoped that this will finally work across all SQL Server
  versions and authentication styles.
  References: [#3810](https://www.sqlalchemy.org/trac/ticket/3810)
- Updated the server version info scheme for pyodbc to use SQL Server
  SERVERPROPERTY(), rather than relying upon pyodbc.SQL_DBMS_VER, which
  continues to be unreliable particularly with FreeTDS.
  References: [#3814](https://www.sqlalchemy.org/trac/ticket/3814)
- Added error code 20017 “unexpected EOF from the server” to the list of
  disconnect exceptions that result in a connection pool reset.  Pull
  request courtesy Ken Robbins.
  References: [#3791](https://www.sqlalchemy.org/trac/ticket/3791)
- Fixed bug in pyodbc dialect (as well as in the mostly non-working
  adodbapi dialect) whereby a semicolon present in the password
  or username fields could be interpreted as a separator for another
  token; the values are now quoted when semicolons are present.
  References: [#3762](https://www.sqlalchemy.org/trac/ticket/3762)

### misc

- Fixed bug where setting up a single-table inh subclass of a joined-table
  subclass which included an extra column would corrupt the foreign keys
  collection of the mapped table, thereby interfering with the
  initialization of relationships.
  References: [#3797](https://www.sqlalchemy.org/trac/ticket/3797)

## 1.0.15

Released: September 1, 2016

### orm

- Fixed bug in subquery eager loading where a subqueryload
  of an “of_type()” object linked to a second subqueryload of a plain
  mapped class, or a longer chain of several “of_type()” attributes,
  would fail to link the joins correctly.
  References: [#3773](https://www.sqlalchemy.org/trac/ticket/3773), [#3774](https://www.sqlalchemy.org/trac/ticket/3774)

### sql

- Fixed bug in [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) where the internal method
  `_reset_exported()` would corrupt the state of the object.  This
  method is intended for selectable objects and is called by the ORM
  in some cases; an erroneous mapper configuration would could lead the
  ORM to call this on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.
  References: [#3755](https://www.sqlalchemy.org/trac/ticket/3755)

### mysql

- Added support for parsing MySQL/Connector boolean and integer
  arguments within the URL query string: connection_timeout,
  connect_timeout, pool_size, get_warnings,
  raise_on_warnings, raw, consume_results, ssl_verify_cert, force_ipv6,
  pool_reset_session, compress, allow_local_infile, use_pure.
  References: [#3787](https://www.sqlalchemy.org/trac/ticket/3787)

### misc

- Fixed bug in `sqlalchemy.ext.baked` where the unbaking of a
  subquery eager loader query would fail due to a variable scoping
  issue, when multiple subquery loaders were involved.  Pull request
  courtesy Mark Hahnenberg.
  References: [#3743](https://www.sqlalchemy.org/trac/ticket/3743)

## 1.0.14

Released: July 6, 2016

### examples

- Fixed a regression that occurred in the
  examples/vertical/dictlike-polymorphic.py example which prevented it
  from running.
  References: [#3704](https://www.sqlalchemy.org/trac/ticket/3704)

### engine

- Fixed bug in cross-schema foreign key reflection in conjunction
  with the [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) argument, where a referenced
  table that is present in the “default” schema would fail since there
  would be no way to indicate a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that has “blank” for
  a schema.  The special symbol `sqlalchemy.schema.BLANK_SCHEMA` has been
  added as an available value for [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) and
  [Sequence.schema](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.schema), indicating that the schema name
  should be forced to be `None` even if [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema)
  is specified.
  References: [#3716](https://www.sqlalchemy.org/trac/ticket/3716)

### sql

- Fixed issue in SQL math negation operator where the type of the
  expression would no longer be the numeric type of the original.
  This would cause issues where the type determined result set
  behaviors.
  References: [#3735](https://www.sqlalchemy.org/trac/ticket/3735)
- Fixed bug whereby the `__getstate__` / `__setstate__`
  methods for sqlalchemy.util.Properties were
  non-working due to the transition in the 1.0 series to `__slots__`.
  The issue potentially impacted some third-party applications.
  Pull request courtesy Pieter Mulder.
  References: [#3728](https://www.sqlalchemy.org/trac/ticket/3728)
- `FromClause.count()` is pending deprecation for 1.1.  This function
  makes use of an arbitrary column in the table and is not reliable;
  for Core use, `func.count()` should be preferred.
  References: [#3724](https://www.sqlalchemy.org/trac/ticket/3724)
- Fixed bug in [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) structure which would cause it to not
  clone properly when a union was used, as is common in a recursive
  CTE.  The improper cloning would cause errors when the CTE is used
  in various ORM contexts such as that of a [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property).
  References: [#3722](https://www.sqlalchemy.org/trac/ticket/3722)
- Fixed bug whereby [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) would make a duplicate
  [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) for each [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object that
  featured the `unique=True` parameter.
  References: [#3721](https://www.sqlalchemy.org/trac/ticket/3721)

### postgresql

- Fixed bug whereby [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) and [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant)
  types were not deeply inspected enough by the PostgreSQL dialect
  to determine if SMALLSERIAL or BIGSERIAL needed to be rendered
  rather than SERIAL.
  References: [#3739](https://www.sqlalchemy.org/trac/ticket/3739)

### oracle

- Fixed bug in [Select.with_for_update.of](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_for_update.params.of), where the Oracle
  “rownum” approach to LIMIT/OFFSET would fail to accommodate for the
  expressions inside the “OF” clause, which must be stated at the topmost
  level referring to expression within the subquery.  The expressions are
  now added to the subquery if needed.
  References: [#3741](https://www.sqlalchemy.org/trac/ticket/3741)

## 1.0.13

Released: May 16, 2016

### orm

- Fixed bug in “evaluate” strategy of [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) and
  [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) which would fail to accommodate a bound
  parameter with a “callable” value, as which occurs when filtering
  by a many-to-one equality expression along a relationship.
  References: [#3700](https://www.sqlalchemy.org/trac/ticket/3700)
- Fixed bug whereby the event listeners used for backrefs could
  be inadvertently applied multiple times, when using a deep class
  inheritance hierarchy in conjunction with multiple mapper configuration
  steps.
  References: [#3710](https://www.sqlalchemy.org/trac/ticket/3710)
- Fixed bug whereby passing a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct to the
  [Query.group_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.group_by) method would raise an error, instead
  of interpreting the object as a SQL fragment.
  References: [#3706](https://www.sqlalchemy.org/trac/ticket/3706)
- Anonymous labeling is applied to a `func` construct that is
  passed to [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), so that if the same attribute
  is referred to as a column expression twice the names are de-duped,
  thus avoiding “ambiguous column” errors.   Previously, the
  `.label(None)` would need to be applied in order for the name
  to be de-anonymized.
  References: [#3663](https://www.sqlalchemy.org/trac/ticket/3663)
- Fixed regression appearing in the 1.0 series in ORM loading where the
  exception raised for an expected column missing would incorrectly
  be a `NoneType` error, rather than the expected
  [NoSuchColumnError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchColumnError).
  References: [#3658](https://www.sqlalchemy.org/trac/ticket/3658)

### examples

- Changed the “directed graph” example to no longer consider
  integer identifiers of nodes as significant; the “higher” / “lower”
  references now allow mutual edges in both directions.
  References: [#3698](https://www.sqlalchemy.org/trac/ticket/3698)

### sql

- Fixed bug where when using `case_sensitive=False` with an
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine), the result set would fail to correctly accommodate
  for duplicate column names in the result set, causing an error
  when the statement is executed in 1.0, and preventing the
  “ambiguous column” exception from functioning in 1.1.
  References: [#3690](https://www.sqlalchemy.org/trac/ticket/3690)
- Fixed bug where the negation of an EXISTS expression would not
  be properly typed as boolean in the result, and also would fail to be
  anonymously aliased in a SELECT list as is the case with a
  non-negated EXISTS construct.
  References: [#3682](https://www.sqlalchemy.org/trac/ticket/3682)
- Fixed bug where “unconsumed column names” exception would fail to
  be raised in the case where [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) were called
  with a list of parameter mappings, instead of a single mapping
  of parameters.  Pull request courtesy Athena Yao.
  References: [#3666](https://www.sqlalchemy.org/trac/ticket/3666)

### postgresql

- Added disconnect detection support for the error string
  “SSL error: decryption failed or bad record mac”.  Pull
  request courtesy Iuri de Silvio.
  References: [#3715](https://www.sqlalchemy.org/trac/ticket/3715)

### mssql

- Fixed bug where by ROW_NUMBER OVER clause applied for OFFSET
  selects in SQL Server would inappropriately substitute a plain column
  from the local statement that overlaps with a label name used by
  the ORDER BY criteria of the statement.
  References: [#3711](https://www.sqlalchemy.org/trac/ticket/3711)
- Fixed regression appearing in the 1.0 series which would cause the Oracle
  and SQL Server dialects to incorrectly account for result set columns
  when these dialects would wrap a SELECT in a subquery in order to
  provide LIMIT/OFFSET behavior, and the original SELECT statement
  referred to the same column multiple times, such as a column and
  a label of that same column.  This issue is related
  to [#3658](https://www.sqlalchemy.org/trac/ticket/3658) in that when the error occurred, it would also
  cause a `NoneType` error, rather than reporting that it couldn’t
  locate a column.
  References: [#3657](https://www.sqlalchemy.org/trac/ticket/3657)

### oracle

- Fixed a bug in the cx_Oracle connect process that caused a TypeError
  when the either the user, password or dsn was empty. This prevented
  external authentication to Oracle databases, and prevented connecting
  to the default dsn.  The connect string oracle:// now logs into the
  default dsn using the Operating System username, equivalent to
  connecting using ‘/’ with sqlplus.
  References: [#3705](https://www.sqlalchemy.org/trac/ticket/3705)
- Fixed a bug in the result proxy used mainly by Oracle when binary and
  other LOB types are in play, such that when query / statement caching
  were used, the type-level result processors, notably that required by
  the binary type itself but also any other processor, would become lost
  after the first run of the statement due to it being removed from the
  cached result metadata.
  References: [#3699](https://www.sqlalchemy.org/trac/ticket/3699)

### misc

- Fixed bug in “to_list” conversion where a single bytes object
  would be turned into a list of individual characters.  This would
  impact among other things using the [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get) method
  on a primary key that’s a bytes object.
  References: [#3660](https://www.sqlalchemy.org/trac/ticket/3660)

## 1.0.12

Released: February 15, 2016

### orm

- Fixed bug in [Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) where an object with a composite
  primary key that has values for some but not all of the PK fields
  would emit a SELECT statement leaking the internal NEVER_SET symbol
  into the query, rather than detecting that this object does not have
  a searchable primary key and no SELECT should be emitted.
  References: [#3647](https://www.sqlalchemy.org/trac/ticket/3647)
- Fixed regression since 0.9 where the 0.9 style loader options
  system failed to accommodate for multiple [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group)
  loader options in a single query.   Multiple [undefer_group()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer_group)
  options will now be taken into account even against the same
  entity.
  References: [#3623](https://www.sqlalchemy.org/trac/ticket/3623)

### engine

- Revisiting [#2696](https://www.sqlalchemy.org/trac/ticket/2696), first released in 1.0.10, which attempts to
  work around Python 2’s lack of exception context reporting by emitting
  a warning for an exception that was interrupted by a second exception
  when attempting to roll back the already-failed transaction; this
  issue continues to occur for MySQL backends in conjunction with a
  savepoint that gets unexpectedly lost, which then causes a
  “no such savepoint” error when the rollback is attempted, obscuring
  what the original condition was.
  The approach has been generalized to the Core “safe
  reraise” function which takes place across the ORM and Core in any
  place that a transaction is being rolled back in response to an error
  which occurred trying to commit, including the context managers
  provided by [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), and taking
  place for operations such as a failure on “RELEASE SAVEPOINT”.
  Previously, the fix was only in place for a specific path within
  the ORM flush/commit process; it now takes place for all transactional
  context managers as well.
  References: [#2696](https://www.sqlalchemy.org/trac/ticket/2696)

### sql

- Fixed issue where the “literal_binds” flag was not propagated
  for [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) or
  [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs when compiled to string
  SQL.  Pull request courtesy Tim Tate.
  References: [#3643](https://www.sqlalchemy.org/trac/ticket/3643)
- Fixed issue where inadvertent use of the Python `__contains__`
  override with a column expression (e.g. by using `'x' in col`)
  would cause an endless loop in the case of an ARRAY type, as Python
  defers this to `__getitem__` access which never raises for this
  type.  Overall, all use of `__contains__` now raises
  NotImplementedError.
  References: [#3642](https://www.sqlalchemy.org/trac/ticket/3642)
- Fixed bug in [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata construct which appeared
  around the 0.9 series where adding columns to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  that was unpickled would fail to correctly establish the
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) within the ‘c’ collection, leading to issues in
  areas such as ORM configuration.   This could impact use cases such
  as `extend_existing` and others.
  References: [#3632](https://www.sqlalchemy.org/trac/ticket/3632)

### postgresql

- Fixed bug in [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct where a double-colon
  expression would not escape properly, e.g. `some\:\:expr`, as is most
  commonly required when rendering PostgreSQL-style CAST expressions.
  References: [#3644](https://www.sqlalchemy.org/trac/ticket/3644)

### mssql

- Fixed the syntax of the [extract()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.extract) function when used on
  MSSQL against a datetime value; the quotes around the keyword
  are removed.  Pull request courtesy Guillaume Doumenc.
  References: [#3624](https://www.sqlalchemy.org/trac/ticket/3624)
- Fixed 1.0 regression where the eager fetch of cursor.rowcount was
  no longer called for an UPDATE or DELETE statement emitted via plain
  text or via the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, affecting those drivers
  that erase cursor.rowcount once the cursor is closed such as SQL
  Server ODBC and Firebird drivers.
  References: [#3622](https://www.sqlalchemy.org/trac/ticket/3622)

### oracle

- Fixed a small issue in the Jython Oracle compiler involving the
  rendering of “RETURNING” which allows this currently
  unsupported/untested dialect to work rudimentarily with the 1.0 series.
  Pull request courtesy Carlos Rivas.
  References: [#3621](https://www.sqlalchemy.org/trac/ticket/3621)

### misc

- Fixed bug where some exception re-raise scenarios would attach
  the exception to itself as the “cause”; while the Python 3 interpreter
  is OK with this, it could cause endless loops in iPython.
  References: [#3625](https://www.sqlalchemy.org/trac/ticket/3625)

## 1.0.11

Released: December 22, 2015

### orm

- Fixed regression caused in 1.0.10 by the fix for [#3593](https://www.sqlalchemy.org/trac/ticket/3593) where
  the check added for a polymorphic joinedload from a
  poly_subclass->class->poly_baseclass connection would fail for the
  scenario of class->poly_subclass->class.
  References: [#3611](https://www.sqlalchemy.org/trac/ticket/3611)
- Fixed bug where [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) and related
  would not bump a version id counter when in use.  The experience
  here is still a little rough as the original version id is required
  in the given dictionaries and there’s not clean error reporting
  on that yet.
  References: [#3610](https://www.sqlalchemy.org/trac/ticket/3610)
- Major fixes to the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) flag, this
  flag would not be honored correctly in the case that multiple
  UPDATE statements were to be emitted, either as part of a flush
  or a bulk update operation.  Additionally, RETURNING
  would be emitted unnecessarily within update statements.
  References: [#3609](https://www.sqlalchemy.org/trac/ticket/3609)
- Fixed bug where use of the [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method would
  cause a subsequent call to the [Query.with_parent()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_parent) method to
  fail.
  References: [#3606](https://www.sqlalchemy.org/trac/ticket/3606)

### sql

- Fixed bug in `Update.return_defaults()` which would cause all
  insert-default holding columns not otherwise included in the SET
  clause (such as primary key cols) to get rendered into the RETURNING
  even though this is an UPDATE.
  References: [#3609](https://www.sqlalchemy.org/trac/ticket/3609)

### mysql

- An adjustment to the regular expression used to parse MySQL views,
  such that we no longer assume the “ALGORITHM” keyword is present in
  the reflected view source, as some users have reported this not being
  present in some Amazon RDS environments.
  References: [#3613](https://www.sqlalchemy.org/trac/ticket/3613)
- Added new reserved words for MySQL 5.7 to the MySQL dialect,
  including ‘generated’, ‘optimizer_costs’, ‘stored’, ‘virtual’.
  Pull request courtesy Hanno Schlichting.

### misc

- Further fixes to [#3605](https://www.sqlalchemy.org/trac/ticket/3605), pop method on [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict),
  where the “default” argument was not included.
  References: [#3605](https://www.sqlalchemy.org/trac/ticket/3605)
- Fixed bug in baked loader system where the systemwide monkeypatch
  for setting up baked lazy loaders would interfere with other
  loader strategies that rely on lazy loading as a fallback, e.g.
  joined and subquery eager loaders, leading to `IndexError`
  exceptions at mapper configuration time.
  References: [#3612](https://www.sqlalchemy.org/trac/ticket/3612)

## 1.0.10

Released: December 11, 2015

### orm

- Fixed issue where post_update on a many-to-one relationship would
  fail to emit an UPDATE in the case where the attribute were set to
  None and not previously loaded.
  References: [#3599](https://www.sqlalchemy.org/trac/ticket/3599)
- Fixed bug which is actually a regression that occurred between
  versions 0.8.0 and 0.8.1, due [#2714](https://www.sqlalchemy.org/trac/ticket/2714).  The case where
  joined eager loading needs to join out over a subclass-bound
  relationship when “with_polymorphic” were also used would fail
  to join from the correct entity.
  References: [#3593](https://www.sqlalchemy.org/trac/ticket/3593)
- Fixed joinedload bug which would occur when a. the query includes
  limit/offset criteria that forces a subquery b. the relationship
  uses “secondary” c. the primaryjoin of the relationship refers to
  a column that is either not part of the primary key, or is a PK
  col in a joined-inheritance subclass table that is under a different
  attribute name than the parent table’s primary key column d. the
  query defers the columns that are present in the primaryjoin, typically
  via not being included in load_only(); the necessary column(s) would
  not be present in the subquery and produce invalid SQL.
  References: [#3592](https://www.sqlalchemy.org/trac/ticket/3592)
- A rare case which occurs when a [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) fails in the
  scope of a [Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush) operation that’s raising an
  exception, as has been observed in some MySQL SAVEPOINT cases, prevents
  the original  database exception from being observed when it was
  emitted during  flush, but only on Py2K because Py2K does not support
  exception  chaining; on Py3K the originating exception is chained.  As
  a workaround, a warning is emitted in this specific case showing at
  least the string message of the original database error before we
  proceed to raise  the rollback-originating exception.
  References: [#2696](https://www.sqlalchemy.org/trac/ticket/2696)

### orm declarative

- Fixed bug where in Py2K a unicode literal would not be accepted as the
  string name of a class or other argument within declarative using
  [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) on [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).  Pull request courtesy
  Nils Philippsen.

### sql

- Added support for parameter-ordered SET clauses in an UPDATE
  statement.  This feature is available by passing the
  [update.preserve_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update.params.preserve_parameter_order)
  flag either to the core [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct or alternatively
  adding it to the [Query.update.update_args](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update.params.update_args) dictionary at
  the ORM-level, also passing the parameters themselves as a list of 2-tuples.
  Thanks to Gorka Eguileor for implementation and tests.
  See also
  [Parameter Ordered Updates](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html#tutorial-parameter-ordered-updates)
- Fixed issue within the [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) construct whereby
  the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct would have its `._raw_columns`
  collection mutated in-place when compiling the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
  construct, when the target [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) has Python-side defaults.
  The [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct would compile standalone with the
  erroneous column present subsequent to compilation of the
  [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), and the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) statement itself would
  fail on a second compile attempt due to duplicate bound parameters.
  References: [#3603](https://www.sqlalchemy.org/trac/ticket/3603)
- Fixed bug where CREATE TABLE with a no-column table, but a constraint
  such as a CHECK constraint would render an erroneous comma in the
  definition; this scenario can occur such as with a PostgreSQL
  INHERITS table that has no columns of its own.
  References: [#3598](https://www.sqlalchemy.org/trac/ticket/3598)

### postgresql

- Fixed issue where the “FOR UPDATE OF” PostgreSQL-specific SELECT
  modifier would fail if the referred table had a schema qualifier;
  PG needs the schema name to be omitted.  Pull request courtesy
  Diana Clarke.
  References: [#3573](https://www.sqlalchemy.org/trac/ticket/3573)
- Fixed bug where some varieties of SQL expression passed to the
  “where” clause of [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) would fail
  to be accepted correctly.  Pull request courtesy aisch.
- Fixed the `.python_type` attribute of [INTERVAL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL)
  to return `datetime.timedelta` in the same way as that of
  [python_type](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval.python_type), rather than raising
  `NotImplementedError`.
  References: [#3571](https://www.sqlalchemy.org/trac/ticket/3571)

### mysql

- Fixed bug in MySQL reflection where the “fractional sections portion”
  of the [DATETIME](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.DATETIME), [TIMESTAMP](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TIMESTAMP) and
  [TIME](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TIME) types would be incorrectly placed into the
  `timezone` attribute, which is unused by MySQL, instead of the
  `fsp` attribute.
  References: [#3602](https://www.sqlalchemy.org/trac/ticket/3602)

### mssql

- Added the error “20006: Write to the server failed” to the list
  of disconnect errors for the pymssql driver, as this has been observed
  to render a connection unusable.
  References: [#3585](https://www.sqlalchemy.org/trac/ticket/3585)
- A descriptive ValueError is now raised in the event that SQL server
  returns an invalid date or time format from a DATE or TIME
  column, rather than failing with a NoneType error.  Pull request
  courtesy Ed Avis.
- Fixed issue where DDL generated for the MSSQL types DATETIME2,
  TIME and DATETIMEOFFSET with a precision of “zero” would not generate
  the precision field.  Pull request courtesy Jacobo de Vera.

### tests

- The ORM and Core tutorials, which have always been in doctest format,
  are now exercised within the normal unit test suite in both Python
  2 and Python 3.

### misc

- Added support for the `dict.pop()` and `dict.popitem()` methods
  to the [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) class.
  References: [#3605](https://www.sqlalchemy.org/trac/ticket/3605)
- Updates to internal getargspec() calls, some py36-related
  fixture updates, and alterations to two iterators to “return” instead
  of raising StopIteration, to allow tests to pass without
  errors or warnings on Py3.5, Py3.6, pull requests courtesy
  Jacob MacDonald, Luri de Silvio, and Phil Jones.
- Fixed an issue in baked queries where the .get() method, used either
  directly or within lazy loads, didn’t consider the mapper’s “get clause”
  as part of the cache key, causing bound parameter mismatches if the
  clause got re-generated.  This clause is cached by mappers
  on the fly but in highly concurrent scenarios may be generated more
  than once when first accessed.
  References: [#3597](https://www.sqlalchemy.org/trac/ticket/3597)

## 1.0.9

Released: October 20, 2015

### orm

- Added new method [Query.one_or_none()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.one_or_none); same as
  [Query.one()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.one) but returns None if no row found.  Pull request
  courtesy esiegerman.
- Fixed regression in 1.0 where new feature of using “executemany”
  for UPDATE statements in the ORM (e.g. [UPDATE statements are now batched with executemany() in a flush](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-updatemany))
  would break on PostgreSQL and other RETURNING backends
  when using server-side version generation
  schemes, as the server side value is retrieved via RETURNING which
  is not supported with executemany.
  References: [#3556](https://www.sqlalchemy.org/trac/ticket/3556)
- Fixed rare TypeError which could occur when stringifying certain
  kinds of internal column loader options within internal logging.
  References: [#3539](https://www.sqlalchemy.org/trac/ticket/3539)
- Fixed bug in [Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects) where a mapped
  column that had some kind of “fetch on update” value and was not
  locally present in the given object would cause an AttributeError
  within the operation.
  References: [#3525](https://www.sqlalchemy.org/trac/ticket/3525)
- Fixed 1.0 regression where the “noload” loader strategy would fail
  to function for a many-to-one relationship.  The loader used an
  API to place “None” into the dictionary which no longer actually
  writes a value; this is a side effect of [#3061](https://www.sqlalchemy.org/trac/ticket/3061).
  References: [#3510](https://www.sqlalchemy.org/trac/ticket/3510)

### examples

- Fixed two issues in the “history_meta” example where history tracking
  could encounter empty history, and where a column keyed to an alternate
  attribute name would fail to track properly.  Fixes courtesy
  Alex Fraser.

### sql

- Fixed regression in 1.0-released default-processor for multi-VALUES
  insert statement, [#3288](https://www.sqlalchemy.org/trac/ticket/3288), where the column type for the
  default-holding column would not be propagated to the compiled
  statement in the case where the default was being used,
  leading to bind-level type handlers not being invoked.
  References: [#3520](https://www.sqlalchemy.org/trac/ticket/3520)

### postgresql

- An adjustment to the new PostgreSQL feature of reflecting storage
  options and USING of [#3455](https://www.sqlalchemy.org/trac/ticket/3455) released in 1.0.6,
  to disable the feature for PostgreSQL versions < 8.2 where the
  `reloptions` column is not provided; this allows Amazon Redshift
  to again work as it is based on an 8.0.x version of PostgreSQL.
  Fix courtesy Pete Hollobon.

### oracle

- Fixed support for cx_Oracle version 5.2, which was tripping
  up SQLAlchemy’s version detection under Python 3 and inadvertently
  not using the correct unicode mode for Python 3.  This would cause
  issues such as bound variables mis-interpreted as NULL and rows
  silently not being returned.
  This change is also **backported** to: 0.7.0b1
  References: [#3491](https://www.sqlalchemy.org/trac/ticket/3491)
- Fixed bug in Oracle dialect where reflection of tables and other
  symbols with names quoted to force all-lower-case would not be
  identified properly in reflection queries.  The [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name)
  construct is now applied to incoming symbol names that detect as
  forced into all-lower-case within the “name normalize” process.
  References: [#3548](https://www.sqlalchemy.org/trac/ticket/3548)

### misc

- Added the [AssociationProxy.info](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.params.info) parameter to the
  [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) constructor, to suit the
  [AssociationProxy.info](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy.info) accessor that was added in
  [#2971](https://www.sqlalchemy.org/trac/ticket/2971).  This is possible because [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy)
  is constructed explicitly, unlike a hybrid which is constructed
  implicitly via the decorator syntax.
  References: [#3551](https://www.sqlalchemy.org/trac/ticket/3551)
- Fixed two issues regarding Sybase reflection, allowing tables
  without primary keys to be reflected as well as ensured that
  a SQL statement involved in foreign key detection is pre-fetched up
  front to avoid driver issues upon nested queries.  Fixes here
  courtesy Eugene Zapolsky; note that we cannot currently test
  Sybase to locally verify these changes.
  References: [#3508](https://www.sqlalchemy.org/trac/ticket/3508), [#3509](https://www.sqlalchemy.org/trac/ticket/3509)

## 1.0.8

Released: July 22, 2015

### engine

- Fixed critical issue whereby the pool “checkout” event handler
  may be called against a stale connection without the “connect”
  event handler having been called, in the case where the pool
  attempted to reconnect after being invalidated and failed; the stale
  connection would remain present and would be used on a subsequent
  attempt.  This issue has a greater impact in the 1.0 series subsequent
  to 1.0.2, as it also delivers a blanked-out `.info` dictionary to
  the event handler; prior to 1.0.2 the `.info` dictionary is still
  the previous one.
  This change is also **backported** to: 0.7.0b1
  References: [#3497](https://www.sqlalchemy.org/trac/ticket/3497)

### sqlite

- Fixed bug in SQLite dialect where reflection of UNIQUE constraints
  that included non-alphabetic characters in the names, like dots or
  spaces, would not be reflected with their name.
  This change is also **backported** to: 0.9.10
  References: [#3495](https://www.sqlalchemy.org/trac/ticket/3495)

### misc

- Fixed an issue where a particular base class within utils
  didn’t implement `__slots__`, and therefore meant all subclasses
  of that class didn’t either, negating the rationale for `__slots__`
  to be in use.  Didn’t cause any issue except on IronPython
  which apparently does not implement `__slots__` behavior compatibly
  with cPython.
  References: [#3494](https://www.sqlalchemy.org/trac/ticket/3494)

## 1.0.7

Released: July 20, 2015

### orm

- Fixed 1.0 regression where value objects that override
  `__eq__()` to return a non-boolean-capable object, such as
  some geoalchemy types as well as numpy types, were being tested
  for `bool()` during a unit of work update operation, where in
  0.9 the return value of `__eq__()` was tested against “is True”
  to guard against this.
  References: [#3469](https://www.sqlalchemy.org/trac/ticket/3469)
- Fixed 1.0 regression where a “deferred” attribute would not populate
  correctly if it were loaded within the “optimized inheritance load”,
  which is a special SELECT emitted in the case of joined table
  inheritance used to populate expired or unloaded attributes against
  a joined table without loading the base table.  This is related to
  the fact that SQLA 1.0 no longer guesses about loading deferred
  columns and must be directed explicitly.
  References: [#3468](https://www.sqlalchemy.org/trac/ticket/3468)
- Fixed 1.0 regression where the “parent entity” of a synonym-
  mapped attribute on top of an [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) object would
  resolve to the original mapper, not the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
  version of it, thereby causing problems for a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  that relies on this attribute (e.g. it’s the only representative
  attribute given in the constructor) to figure out the correct FROM
  clause for the query.
  References: [#3466](https://www.sqlalchemy.org/trac/ticket/3466)

### orm declarative

- Fixed bug in [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) extension where
  a column setup on the ABC base which had a different attribute
  name vs. column name would not be correctly mapped on the final
  base class.   The failure on 0.9 would be silent whereas on
  1.0 it raised an ArgumentError, so may not have been noticed
  prior to 1.0.
  References: [#3480](https://www.sqlalchemy.org/trac/ticket/3480)

### engine

- Fixed regression where new methods on `ResultProxy` used
  by the ORM [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object (part of the performance
  enhancements of [#3175](https://www.sqlalchemy.org/trac/ticket/3175)) would not raise the “this result
  does not return rows” exception in the case where the driver
  (typically MySQL) fails to generate cursor.description correctly;
  an AttributeError against NoneType would be raised instead.
  References: [#3481](https://www.sqlalchemy.org/trac/ticket/3481)
- Fixed regression where `ResultProxy.keys()` would return
  un-adjusted internal symbol names for “anonymous” labels, which
  are the “foo_1” types of labels we see generated for SQL functions
  without labels and similar.  This was a side effect of the
  performance enhancements implemented as part of #918.
  References: [#3483](https://www.sqlalchemy.org/trac/ticket/3483)

### sql

- Added a [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) method which performs the same
  purpose as the standalone [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) function.  Pull
  request courtesy Sebastian Bank.
  References: [#3459](https://www.sqlalchemy.org/trac/ticket/3459)
- Fixed bug where coercion of literal `True` or `False` constant
  in conjunction with [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) or [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) would fail
  with an AttributeError.
  References: [#3490](https://www.sqlalchemy.org/trac/ticket/3490)
- Fixed potential issue where a custom subclass
  of [FunctionElement](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement) or other column element that incorrectly
  states ‘None’ or any other invalid object as the `.type`
  attribute will report this exception instead of recursion overflow.
  References: [#3485](https://www.sqlalchemy.org/trac/ticket/3485)
- Fixed bug where the modulus SQL operator wouldn’t work in reverse
  due to a missing `__rmod__` method.  Pull request courtesy
  dan-gittik.

### schema

- Added support for the MINVALUE, MAXVALUE, NO MINVALUE, NO MAXVALUE,
  and CYCLE arguments for CREATE SEQUENCE as supported by PostgreSQL
  and Oracle.  Pull request courtesy jakeogh.

## 1.0.6

Released: June 25, 2015

### orm

- Fixed a major regression in the 1.0 series where the version_id_counter
  feature would cause an object’s version counter to be incremented
  when there was no net change to the object’s row, but instead an object
  related to it via relationship (e.g. typically many-to-one)
  were associated or de-associated with it, resulting in an UPDATE
  statement that updates the object’s version counter and nothing else.
  In the use case where the relatively recent “server side” and/or
  “programmatic/conditional” version counter feature were used
  (e.g. setting version_id_generator to False), the bug could cause an
  UPDATE without a valid SET clause to be emitted.
  References: [#3465](https://www.sqlalchemy.org/trac/ticket/3465)
- Fixed 1.0 regression where the enhanced behavior of single-inheritance
  joins of [#3222](https://www.sqlalchemy.org/trac/ticket/3222) takes place inappropriately
  for a JOIN along explicit join criteria with a single-inheritance
  subclass that does not make use of any discriminator, resulting
  in an additional “AND NULL” clause.
  References: [#3462](https://www.sqlalchemy.org/trac/ticket/3462)
- Fixed bug in new [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings) feature where
  the primary key columns used in the WHERE clause to locate the row
  would also be included in the SET clause, setting their value to
  themselves unnecessarily.  Pull request courtesy Patrick Hayes.
  References: [#3451](https://www.sqlalchemy.org/trac/ticket/3451)
- Fixed an unexpected-use regression whereby custom
  [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) objects that made use of the
  `__clause_element__()` method and returned an object that was an
  ORM-mapped [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute) and not explicitly a
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) would fail to be correctly handled when passed
  as an expression to [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query). The logic in 0.9 happened
  to succeed on this, so this use case is now supported.
  References: [#3448](https://www.sqlalchemy.org/trac/ticket/3448)

### sql

- Fixed a bug where clause adaption as applied to a [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)
  object would fail to accommodate the labeled SQL expression
  in all cases, such that any SQL operation that made use of
  [Label.self_group()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label.self_group) would use the original unadapted
  expression.  One effect of this would be that an ORM [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
  construct would not fully accommodate attributes mapped by
  [column_property](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), such that the un-aliased table could
  leak out when the property were used in some kinds of SQL
  comparisons.
  References: [#3445](https://www.sqlalchemy.org/trac/ticket/3445)

### postgresql

- Added support for storage parameters under CREATE INDEX, using
  a new keyword argument `postgresql_with`.  Also added support for
  reflection to support both the `postgresql_with` flag as well
  as the `postgresql_using` flag, which will now be set on
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) objects that are reflected, as well present
  in a new “dialect_options” dictionary in the result of
  [Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes).  Pull request courtesy Pete Hollobon.
  See also
  [Index Storage Parameters](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-index-storage)
  References: [#3455](https://www.sqlalchemy.org/trac/ticket/3455)
- Added new execution option `max_row_buffer` which is interpreted
  by the psycopg2 dialect when the `stream_results` option is
  used, which sets a limit on the size of the row buffer that may be
  allocated.  This value is also provided based on the integer
  value sent to [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per).  Pull request courtesy
  mcclurem.
- Re-fixed this issue first released in 1.0.5 to fix psycopg2cffi
  JSONB support once again, as they suddenly
  switched on unconditional decoding of JSONB types in version 2.7.1.
  Version detection now specifies 2.7.1 as where we should expect
  the DBAPI to do json encoding for us.
  References: [#3439](https://www.sqlalchemy.org/trac/ticket/3439)
- Repaired the [ExcludeConstraint](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ExcludeConstraint) construct to support common
  features that other objects like [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) now do, that
  the column expression may be specified as an arbitrary SQL
  expression such as [cast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) or [text](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text).
  References: [#3454](https://www.sqlalchemy.org/trac/ticket/3454)

### mssql

- Fixed issue when using [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY) type in conjunction with
  an INSERT of NULL + pyodbc; pyodbc requires a special
  object be passed in order to persist NULL.  As the [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY)
  type is now usually the default for [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) due to
  [#3039](https://www.sqlalchemy.org/trac/ticket/3039), this issue is partially a regression in 1.0.
  The pymssql driver appears to be unaffected.
  References: [#3464](https://www.sqlalchemy.org/trac/ticket/3464)

### misc

- Fixed an internal “memoization” routine for method types such
  that a Python descriptor is no longer used; repairs inspectability
  of these methods including support for Sphinx documentation.
  References: [#2077](https://www.sqlalchemy.org/trac/ticket/2077)

## 1.0.5

Released: June 7, 2015

### orm

- Added new event [InstanceEvents.refresh_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh_flush), invoked
  when an INSERT or UPDATE level default value fetched via RETURNING
  or Python-side default is invoked within the flush process.  This
  is to provide a hook that is no longer present as a result of
  [#3167](https://www.sqlalchemy.org/trac/ticket/3167), where attribute and validation events are no longer
  called within the flush process.
  References: [#3427](https://www.sqlalchemy.org/trac/ticket/3427)
- The “lightweight named tuple” used when a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) returns
  rows failed to implement `__slots__` correctly such that it still
  had a `__dict__`.    This is resolved, but in the extremely
  unlikely case someone was assigning values to the returned tuples,
  that will no longer work.
  References: [#3420](https://www.sqlalchemy.org/trac/ticket/3420)

### engine

- Added new engine event [ConnectionEvents.engine_disposed()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.engine_disposed).
  Called after the [Engine.dispose()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.dispose) method is called.
- Adjustments to the engine plugin hook, such that the
  [URL.get_dialect()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.get_dialect) method will continue to return the
  ultimate [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) object when a dialect plugin is used,
  without the need for the caller to be aware of the
  [Dialect.get_dialect_cls()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.get_dialect_cls) method.
  References: [#3379](https://www.sqlalchemy.org/trac/ticket/3379)
- Fixed bug where known boolean values used by
  [engine_from_config()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine_from_config) were not being parsed correctly;
  these included `pool_threadlocal` and the psycopg2 argument
  `use_native_unicode`.
  References: [#3435](https://www.sqlalchemy.org/trac/ticket/3435)
- Added support for the case of the misbehaving DBAPI that has
  pep-249 exception names linked to exception classes of an entirely
  different name, preventing SQLAlchemy’s own exception wrapping from
  wrapping the error appropriately.
  The SQLAlchemy dialect in use needs to implement a new
  accessor [DefaultDialect.dbapi_exception_translation_map](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.dbapi_exception_translation_map)
  to support this feature; this is implemented now for the py-postgresql
  dialect.
  References: [#3421](https://www.sqlalchemy.org/trac/ticket/3421)
- Fixed bug involving the case when pool checkout event handlers are used
  and connection attempts are made in the handler itself which fail,
  the owning connection record would not be freed until the stack trace
  of the connect error itself were freed.   For the case where a test
  pool of only a single connection were used, this means the pool would
  be fully checked out until that stack trace were freed.  This mostly
  impacts very specific debugging scenarios and is unlikely to have been
  noticeable in any production application.  The fix applies an
  explicit checkin of the record before re-raising the caught exception.
  References: [#3419](https://www.sqlalchemy.org/trac/ticket/3419)

### sql

- Added official support for a CTE used by the SELECT present
  inside of [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select).  This behavior worked
  accidentally up until 0.9.9, when it no longer worked due to
  unrelated changes as part of [#3248](https://www.sqlalchemy.org/trac/ticket/3248).   Note that this
  is the rendering of the WITH clause after the INSERT, before the
  SELECT; the full functionality of CTEs rendered at the top
  level of INSERT, UPDATE, DELETE is a new feature targeted for a
  later release.
  This change is also **backported** to: 0.9.10
  References: [#3418](https://www.sqlalchemy.org/trac/ticket/3418)

### postgresql

- Repaired some typing and test issues related to the pypy
  psycopg2cffi dialect, in particular that the current 2.7.0 version
  does not have native support for the JSONB type.  The version detection
  for psycopg2 features has been tuned into a specific sub-version
  for psycopg2cffi.  Additionally, test coverage has been enabled
  for the full series of psycopg2 features under psycopg2cffi.
  References: [#3439](https://www.sqlalchemy.org/trac/ticket/3439)

### mssql

- Added a new dialect flag to the MSSQL dialect
  `legacy_schema_aliasing` which when set to False will disable a
  very old and obsolete behavior, that of the compiler’s
  attempt to turn all schema-qualified table names into alias names,
  to work around old and no longer locatable issues where SQL
  server could not parse a multi-part identifier name in all
  circumstances.   The behavior prevented more
  sophisticated statements from working correctly, including those which
  use hints, as well as CRUD statements that embed correlated SELECT
  statements.  Rather than continue to repair the feature to work
  with more complex statements, it’s better to just disable it
  as it should no longer be needed for any modern SQL server
  version.  The flag defaults to True for the 1.0.x series, leaving
  current behavior unchanged for this version series.  In the 1.1
  series, it will default to False.  For the 1.0 series,
  when not set to either value explicitly, a warning is emitted
  when a schema-qualified table is first used in a statement, which
  suggests that the flag be set to False for all modern SQL Server
  versions.
  See also
  [Legacy Schema Mode](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#legacy-schema-rendering)
  References: [#3424](https://www.sqlalchemy.org/trac/ticket/3424), [#3430](https://www.sqlalchemy.org/trac/ticket/3430)

### misc

- Added support for `*args` to be passed to the baked query
  initial callable, in the same way that `*args` are supported
  for the [BakedQuery.add_criteria()](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery.add_criteria) and
  [BakedQuery.with_criteria()](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#sqlalchemy.ext.baked.BakedQuery.with_criteria) methods.  Initial PR courtesy
  Naoki INADA.
- Added a new semi-public method to [MutableBase](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableBase) `MutableBase._get_listen_keys()`.  Overriding this method
  is needed in the case where a [MutableBase](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableBase) subclass needs
  events to propagate for attribute keys other than the key to which
  the mutable type is associated with, when intercepting the
  [InstanceEvents.refresh()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh) or
  [InstanceEvents.refresh_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh_flush) events.  The current example of
  this is composites using [MutableComposite](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableComposite).
  References: [#3427](https://www.sqlalchemy.org/trac/ticket/3427)
- Fixed regression in the [sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable) extension
  as a result of the bugfix for [#3167](https://www.sqlalchemy.org/trac/ticket/3167),
  where attribute and validation events are no longer
  called within the flush process.  The mutable
  extension was relying upon this behavior in the case where a column
  level Python-side default were responsible for generating the new value
  on INSERT or UPDATE, or when a value were fetched from the RETURNING
  clause for “eager defaults” mode.  The new value would not be subject
  to any event when populated and the mutable extension could not
  establish proper coercion or history listening.  A new event
  [InstanceEvents.refresh_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh_flush) is added which the mutable
  extension now makes use of for this use case.
  References: [#3427](https://www.sqlalchemy.org/trac/ticket/3427)

## 1.0.4

Released: May 7, 2015

### orm

- Fixed unexpected-use regression where in the odd case that the
  primaryjoin of a relationship involved comparison to an unhashable
  type such as an HSTORE, lazy loads would fail due to a hash-oriented
  check on the statement parameters, modified in 1.0 as a result of
  [#3061](https://www.sqlalchemy.org/trac/ticket/3061) to use hashing and modified in [#3368](https://www.sqlalchemy.org/trac/ticket/3368)
  to occur in cases more common than “load on pending”.
  The values are now checked for the `__hash__` attribute beforehand.
  References: [#3416](https://www.sqlalchemy.org/trac/ticket/3416)
- Liberalized an assertion that was added as part of [#3347](https://www.sqlalchemy.org/trac/ticket/3347)
  to protect against unknown conditions when splicing inner joins
  together within joined eager loads with `innerjoin=True`; if
  some of the joins use a “secondary” table, the assertion needs to
  unwrap further joins in order to pass.
  References: [#3347](https://www.sqlalchemy.org/trac/ticket/3347), [#3412](https://www.sqlalchemy.org/trac/ticket/3412)
- Repaired / added to tests yet more expressions that were reported
  as failing with the new ‘entity’ key value added to
  [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions), the logic to discover the “from”
  clause is again reworked to accommodate columns from aliased classes,
  as well as to report the correct value for the “aliased” flag in these
  cases.
  References: [#3320](https://www.sqlalchemy.org/trac/ticket/3320), [#3409](https://www.sqlalchemy.org/trac/ticket/3409)

### schema

- Fixed bug in enhanced constraint-attachment logic introduced in
  [#3341](https://www.sqlalchemy.org/trac/ticket/3341) where in the unusual case of a constraint that refers
  to a mixture of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects and string column names
  at the same time, the auto-attach-on-column-attach logic will be
  skipped; for the constraint to be auto-attached in this case,
  all columns must be assembled on the target table up front.
  Added a new section to the migration document regarding the
  original feature as well as this change.
  See also
  [Constraints referring to unattached Columns can auto-attach to the Table when their referred columns are attached](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3341)
  References: [#3411](https://www.sqlalchemy.org/trac/ticket/3411)

### tests

- Fixed an import that prevented “pypy setup.py test” from working
  correctly.
  This change is also **backported** to: 0.9.10
  References: [#3406](https://www.sqlalchemy.org/trac/ticket/3406)

### misc

- Fixed bug where when using extended attribute instrumentation system,
  the correct exception would not be raised when [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper)
  were called with an invalid input that also happened to not
  be weak referenceable, such as an integer.
  This change is also **backported** to: 0.9.10
  References: [#3408](https://www.sqlalchemy.org/trac/ticket/3408)

## 1.0.3

Released: April 30, 2015

### orm

- Fixed regression from 0.9.10 prior to release due to [#3349](https://www.sqlalchemy.org/trac/ticket/3349)
  where the check for query state on [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) or
  [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) compared the empty tuple to itself using `is`,
  which fails on PyPy to produce `True` in this case; this would
  erroneously emit a warning in 0.9 and raise an exception in 1.0.
  References: [#3405](https://www.sqlalchemy.org/trac/ticket/3405)
- Fixed regression from 0.9.10 prior to release where the new addition
  of `entity` to the [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions) accessor
  would fail if the target entity was produced from a core selectable
  such as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE) object.
  References: [#3320](https://www.sqlalchemy.org/trac/ticket/3320), [#3403](https://www.sqlalchemy.org/trac/ticket/3403)
- Fixed regression within the flush process when an attribute were
  set to a SQL expression for an UPDATE, and the SQL expression when
  compared to the previous value of the attribute would produce a SQL
  comparison other than `==` or `!=`, the exception “Boolean value
  of this clause is not defined” would raise.   The fix ensures that
  the unit of work will not interpret the SQL expression in this way.
  References: [#3402](https://www.sqlalchemy.org/trac/ticket/3402)
- Fixed unexpected use regression due to [#2992](https://www.sqlalchemy.org/trac/ticket/2992) where
  textual elements placed
  into the [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) clause in conjunction with joined
  eager loading would be added to the columns clause of the inner query
  in such a way that they were assumed to be table-bound column names,
  in the case where the joined eager load needs to wrap the query
  in a subquery to accommodate for a limit/offset.
  Originally, the behavior here was intentional, in that a query such
  as `query(User).order_by('name').limit(1)`
  would order by `user.name` even if the query was modified by
  joined eager loading to be within a subquery, as `'name'` would
  be interpreted as a symbol to be located within the FROM clauses,
  in this case `User.name`, which would then be copied into the
  columns clause to ensure it were present for ORDER BY.  However, the
  feature fails to anticipate the case where `order_by("name")` refers
  to a specific label name present in the local columns clause already
  and not a name bound to a selectable in the FROM clause.
  Beyond that, the feature also fails for deprecated cases such as
  `order_by("name desc")`, which, while it emits a
  warning that [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) should be used here (note that the issue
  does not impact cases where [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) is used explicitly),
  still produces a different query than previously where the “name desc”
  expression is copied into the columns clause inappropriately.  The
  resolution is such that the “joined eager loading” aspect of the
  feature will skip over these so-called “label reference” expressions
  when augmenting the inner columns clause, as though they were
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) constructs already.
  References: [#3392](https://www.sqlalchemy.org/trac/ticket/3392)
- Fixed a regression regarding the [MapperEvents.instrument_class()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.instrument_class)
  event where its invocation was moved to be after the class manager’s
  instrumentation of the class, which is the opposite of what the
  documentation for the event explicitly states.  The rationale for the
  switch was due to Declarative taking the step of setting up
  the full “instrumentation manager” for a class before it was mapped
  for the purpose of the new `@declared_attr` features
  described in [Improvements to declarative mixins, @declared_attr and related features](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3150), but the change was also made
  against the classical use of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) for consistency.
  However, SQLSoup relies upon the instrumentation event happening
  before any instrumentation under classical mapping.
  The behavior is reverted in the case of classical and declarative
  mapping, the latter implemented by using a simple memoization
  without using class manager.
  References: [#3388](https://www.sqlalchemy.org/trac/ticket/3388)
- Fixed issue in new [QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) event where
  changes made to the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object’s collection of entities
  to load within the event would render in the SQL, but would not
  be reflected during the loading process.
  References: [#3387](https://www.sqlalchemy.org/trac/ticket/3387)

### engine

- New features added to support engine/pool plugins with advanced
  functionality.   Added a new “soft invalidate” feature to the
  connection pool at the level of the checked out connection wrapper
  as well as the [_ConnectionRecord](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool._ConnectionRecord).  This works similarly
  to a modern pool invalidation in that connections aren’t actively
  closed, but are recycled only on next checkout; this is essentially
  a per-connection version of that feature.  A new event
  [PoolEvents.soft_invalidate()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.soft_invalidate) is added to complement it.
  Also added new flag
  [ExceptionContext.invalidate_pool_on_disconnect](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ExceptionContext.invalidate_pool_on_disconnect).
  Allows an error handler within `ConnectionEvents.handle_error()`
  to maintain a “disconnect” condition, but to handle calling invalidate
  on individual connections in a specific manner within the event.
  References: [#3379](https://www.sqlalchemy.org/trac/ticket/3379)
- Added new event `do_connect`, which allows
  interception / replacement of when the [Dialect.connect()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.connect)
  hook is called to create a DBAPI connection.  Also added
  dialect plugin hooks [Dialect.get_dialect_cls()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.get_dialect_cls) and
  [Dialect.engine_created()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.engine_created) which allow external plugins to
  add events to existing dialects using entry points.
  References: [#3355](https://www.sqlalchemy.org/trac/ticket/3355)

### sql

- Added a placeholder method `TypeEngine.compare_against_backend()`
  which is now consumed by Alembic migrations as of 0.7.6.  User-defined
  types can implement this method to assist in the comparison of
  a type against one reflected from the database.
- Fixed bug where the truncation of long labels in SQL could produce
  a label that overlapped another label that is not truncated; this
  because the length threshold for truncation was greater than
  the portion of the label that remains after truncation.  These
  two values have now been made the same; label_length - 6.
  The effect here is that shorter column labels will be “truncated”
  where they would not have been truncated before.
  References: [#3396](https://www.sqlalchemy.org/trac/ticket/3396)
- Fixed regression due to [#3282](https://www.sqlalchemy.org/trac/ticket/3282) where the `tables` collection
  passed as a keyword argument to the [DDLEvents.before_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_create),
  [DDLEvents.after_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_create), [DDLEvents.before_drop()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_drop), and
  [DDLEvents.after_drop()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_drop) events would no longer be a list
  of tables, but instead a list of tuples which contained a second
  entry with foreign keys to be added or dropped.  As the `tables`
  collection, while documented as not necessarily stable, has come
  to be relied upon, this change is considered a regression.
  Additionally, in some cases for “drop”, this collection would
  be an iterator that would cause the operation to fail if
  prematurely iterated.   The collection is now a list of table
  objects in all cases and test coverage for the format of this
  collection is now added.
  References: [#3391](https://www.sqlalchemy.org/trac/ticket/3391)

### misc

- Fixed bug in association proxy where an any()/has()
  on an relationship->scalar non-object attribute comparison would fail,
  e.g.
  `filter(Parent.some_collection_to_attribute.any(Child.attr == 'foo'))`
  References: [#3397](https://www.sqlalchemy.org/trac/ticket/3397)

## 1.0.2

Released: April 24, 2015

### orm declarative

- Fixed unexpected use regression regarding the declarative
  `__declare_first__` and `__declare_last__` accessors where these
  would no longer be called on the superclass of the declarative base.
  References: [#3383](https://www.sqlalchemy.org/trac/ticket/3383)

### sql

- Fixed a regression that was incorrectly fixed in 1.0.0b4
  (hence becoming two regressions); reports that
  SELECT statements would GROUP BY a label name and fail was misconstrued
  that certain backends such as SQL Server should not be emitting
  ORDER BY or GROUP BY on a simple label name at all; when in fact,
  we had forgotten that 0.9 was already emitting ORDER BY on a simple
  label name for all backends, as described in [Label constructs can now render as their name alone in an ORDER BY](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-1068),
  even though 1.0 includes a rewrite of this logic as part of
  [#2992](https://www.sqlalchemy.org/trac/ticket/2992).  As far
  as emitting GROUP BY against a simple label, even PostgreSQL has
  cases where it will raise an error even though the label to group
  on should be apparent, so it is clear that GROUP BY should never
  be rendered in this way automatically.
  In 1.0.2, SQL Server, Firebird and others will again emit ORDER BY on
  a simple label name when passed a
  [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) construct that is also present in the columns clause.
  Additionally, no backend will emit GROUP BY against the simple label
  name only when passed a [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label) construct.
  References: [#3338](https://www.sqlalchemy.org/trac/ticket/3338), [#3385](https://www.sqlalchemy.org/trac/ticket/3385)

## 1.0.1

Released: April 23, 2015

### orm

- Fixed issue where a query of the form
  `query(B).filter(B.a != A(id=7))` would render the `NEVER_SET`
  symbol, when
  given a transient object. For a persistent object, it would
  always use the persisted database value and not the currently
  set value.  Assuming autoflush is turned on, this usually would
  not be apparent for persistent values, as any pending changes
  would be flushed first in any case.  However, this is inconsistent
  vs. the logic used for the  non-negated comparison,
  `query(B).filter(B.a == A(id=7))`, which does use the
  current value and additionally allows comparisons to transient
  objects.  The comparison now uses the current value and not
  the database-persisted value.
  Unlike the other `NEVER_SET` issues that are repaired as regressions
  caused by [#3061](https://www.sqlalchemy.org/trac/ticket/3061) in this release, this particular issue is
  present at least as far back as 0.8 and possibly earlier, however it
  was discovered as a result of repairing the related `NEVER_SET`
  issues.
  See also
  [A “negated contains or equals” relationship comparison will use the current value of attributes, not the database value](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3374)
  References: [#3374](https://www.sqlalchemy.org/trac/ticket/3374)
- Fixed unexpected use regression cause by [#3061](https://www.sqlalchemy.org/trac/ticket/3061) where
  the NEVER_SET
  symbol could leak into relationship-oriented queries, including
  `filter()` and `with_parent()` queries.  The `None` symbol
  is returned in all cases, however many of these queries have never
  been correctly supported in any case, and produce comparisons
  to NULL without using the IS operator.  For this reason, a warning
  is also added to that subset of relationship queries that don’t
  currently provide for `IS NULL`.
  See also
  [Warnings emitted when comparing objects with None values to relationships](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3371)
  References: [#3371](https://www.sqlalchemy.org/trac/ticket/3371)
- Fixed a regression caused by [#3061](https://www.sqlalchemy.org/trac/ticket/3061) where the
  NEVER_SET symbol could leak into a lazyload query, subsequent
  to the flush of a pending object.  This would occur typically
  for a many-to-one relationship that does not use a simple
  “get” strategy.   The good news is that the fix improves efficiency
  vs. 0.9, because we can now skip the SELECT statement entirely
  when we detect NEVER_SET symbols present in the parameters; prior to
  [#3061](https://www.sqlalchemy.org/trac/ticket/3061), we couldn’t discern if the None here were set or not.
  References: [#3368](https://www.sqlalchemy.org/trac/ticket/3368)

### engine

- Added the string value `"none"` to those accepted by the
  [Pool.reset_on_return](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool.params.reset_on_return) parameter as a synonym for `None`,
  so that string values can be used for all settings, allowing
  utilities like [engine_from_config()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine_from_config) to be usable without
  issue.
  This change is also **backported** to: 0.9.10
  References: [#3375](https://www.sqlalchemy.org/trac/ticket/3375)

### sql

- Fixed issue where a straight SELECT EXISTS query would fail to
  assign the proper result type of Boolean to the result mapping, and
  instead would leak column types from within the query into the
  result map.  This issue exists in 0.9 and earlier as well, however
  has less of an impact in those versions.  In 1.0, due to [#918](https://www.sqlalchemy.org/trac/ticket/918)
  this becomes a regression in that we now rely upon the result mapping
  to be very accurate, else we can assign result-type processors to
  the wrong column.   In all versions, this issue also has the effect
  that a simple EXISTS will not apply the Boolean type handler, leading
  to simple 1/0 values for backends without native boolean instead of
  True/False.   The fix includes that an EXISTS columns argument
  will be anon-labeled like other column expressions; a similar fix is
  implemented for pure-boolean expressions like `not_(True())`.
  References: [#3372](https://www.sqlalchemy.org/trac/ticket/3372)

### sqlite

- Fixed a regression due to [#3282](https://www.sqlalchemy.org/trac/ticket/3282), where due to the fact that
  we attempt to assume the availability of ALTER when creating/dropping
  schemas, in the case of SQLite we simply said to not worry about
  foreign keys at all, since ALTER is not available, when creating
  and dropping tables.  This meant that the sorting of tables was
  basically skipped in the case of SQLite, and for the vast majority
  of SQLite use cases, this is not an issue.
  However, users who were doing DROPs on SQLite
  with tables that contained data and with referential integrity
  turned on would then experience errors, as the
  dependency sorting *does* matter in the case of DROP with
  enforced constraints, when those tables have data (SQLite will still
  happily let you create foreign keys to nonexistent tables and drop
  tables referring to existing ones with constraints enabled, as long as
  there’s no data being referenced).
  In order to maintain the new feature of [#3282](https://www.sqlalchemy.org/trac/ticket/3282) while still
  allowing a SQLite DROP operation to maintain ordering, we now
  do the sort with full FKs taken under consideration, and if we encounter
  an unresolvable cycle, only *then* do we forego attempting to sort
  the tables; we instead emit a warning and go with the unsorted list.
  If an environment needs both ordered DROPs *and* has foreign key
  cycles, then the warning notes they will need to restore the
  `use_alter` flag to their [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) and
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects so that just those objects will
  be omitted from the dependency sort.
  See also
  [The use_alter flag on ForeignKeyConstraint is (usually) no longer needed](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3282) - contains an updated note about SQLite.
  References: [#3378](https://www.sqlalchemy.org/trac/ticket/3378)

### misc

- Fixed a regression due to [#3034](https://www.sqlalchemy.org/trac/ticket/3034) where limit/offset
  clauses were not properly interpreted by the Firebird dialect.
  Pull request courtesy effem-git.
  References: [#3380](https://www.sqlalchemy.org/trac/ticket/3380)
- Fixed support for “literal_binds” mode when using limit/offset
  with Firebird, so that the values are again rendered inline when
  this is selected.  Related to [#3034](https://www.sqlalchemy.org/trac/ticket/3034).
  References: [#3381](https://www.sqlalchemy.org/trac/ticket/3381)

## 1.0.0

Released: April 16, 2015

### orm

- Added new argument [Query.update.update_args](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update.params.update_args) which allows
  kw arguments such as `mysql_limit` to be passed to the underlying
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct.  Pull request courtesy Amir Sadoughi.
- Identified an inconsistency when handling [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) to the
  same target more than once; it implicitly dedupes only in the case of
  a relationship join, and due to [#3233](https://www.sqlalchemy.org/trac/ticket/3233), in 1.0 a join
  to the same table twice behaves differently than 0.9 in that it no
  longer erroneously aliases.   To help document this change,
  the verbiage regarding [#3233](https://www.sqlalchemy.org/trac/ticket/3233) in the migration notes has
  been generalized, and a warning has been added when [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join)
  is called against the same target relationship more than once.
  References: [#3367](https://www.sqlalchemy.org/trac/ticket/3367)
- Made a small improvement to the heuristics of relationship when
  determining remote side with semi-self-referential (e.g. two joined
  inh subclasses referring to each other), non-simple join conditions
  such that the parententity is taken into account and can reduce the
  need for using the `remote()` annotation; this can restore some
  cases that might have worked without the annotation prior to 0.9.4
  via [#2948](https://www.sqlalchemy.org/trac/ticket/2948).
  References: [#3364](https://www.sqlalchemy.org/trac/ticket/3364)

### sql

- The topological sorting used to sort [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
  and available via the [MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables) collection
  will now produce a **deterministic** ordering; that is, the same
  ordering each time given a set of tables with particular names
  and dependencies.  This is to help with comparison of DDL scripts
  and other use cases.  The tables are sent to the topological sort
  sorted by name, and the topological sort itself will process
  the incoming data in an ordered fashion.  Pull request
  courtesy Sebastian Bank.
  See also
  [MetaData.sorted_tables accessor is “deterministic”](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3084)
  References: [#3084](https://www.sqlalchemy.org/trac/ticket/3084)
- Fixed issue where a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object that used a naming
  convention would not properly work with pickle.  The attribute was
  skipped leading to inconsistencies and failures if the unpickled
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object were used to base additional tables
  from.
  This change is also **backported** to: 0.9.10
  References: [#3362](https://www.sqlalchemy.org/trac/ticket/3362)

### postgresql

- Fixed a long-standing bug where the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type as used
  with the psycopg2 dialect in conjunction with non-ascii values
  and `native_enum=False` would fail to decode return results properly.
  This stemmed from when the PG [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) type used
  to be a standalone type without a “non native” option.
  This change is also **backported** to: 0.9.10
  References: [#3354](https://www.sqlalchemy.org/trac/ticket/3354)

### mssql

- Fixed a regression where the “last inserted id” mechanics would
  fail to store the correct value for MSSQL on an INSERT where the
  primary key value was present in the insert params before execution,
  as well as in the case where an INSERT from SELECT would state the
  target columns as column objects, instead of string keys.
  References: [#3360](https://www.sqlalchemy.org/trac/ticket/3360)
- Using the `Binary` constructor now present in pymssql rather than
  patching one in.  Pull request courtesy Ramiro Morales.

### tests

- Fixed the pathing used when tests run; for sqla_nose.py and py.test,
  the “./lib” prefix is again inserted at the head of sys.path but
  only if sys.flags.no_user_site isn’t set; this makes it act just
  like the way Python puts “.” in the current path by default.
  For tox, we are setting the PYTHONNOUSERSITE flag now.
  References: [#3356](https://www.sqlalchemy.org/trac/ticket/3356)

## 1.0.0b5

Released: April 3, 2015

### orm

- Fixed bug where the state tracking within multiple, nested
  [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) operations would fail to propagate
  the “dirty” flag for an object that had been updated within
  the inner savepoint, such that if the enclosing savepoint were
  rolled back, the object would not be part of the state that was
  expired and therefore reverted to its database state.
  This change is also **backported** to: 0.9.10
  References: [#3352](https://www.sqlalchemy.org/trac/ticket/3352)
- [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) doesn’t support joins, subselects, or special
  FROM clauses when using the [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) or
  [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) methods; instead of silently ignoring these
  fields if methods like [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) or
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) has been called, an error is raised.
  In 0.9.10 this only emits a warning.
  References: [#3349](https://www.sqlalchemy.org/trac/ticket/3349)
- Added a list() call around a weak dictionary used within the
  commit phase of the session, which without it could cause
  a “dictionary changed size during iter” error if garbage collection
  interacted within the process.   Change was introduced by
  #3139.
- Fixed a bug related to “nested” inner join eager loading, which
  exists in 0.9 as well but is more of a regression in 1.0 due to
  [#3008](https://www.sqlalchemy.org/trac/ticket/3008) which turns on “nested” by default, such that
  a joined eager load that travels across sibling paths from a common
  ancestor using innerjoin=True will correctly splice each “innerjoin”
  sibling into the appropriate part of the join, when a series of
  inner/outer joins are mixed together.
  References: [#3347](https://www.sqlalchemy.org/trac/ticket/3347)

### sql

- The warning emitted by the unicode type for a non-unicode type
  has been liberalized to warn for values that aren’t even string
  values, such as integers; previously, the updated warning system
  of 1.0 made use of string formatting operations which
  would raise an internal TypeError.   While these cases should ideally
  raise totally, some backends like SQLite and MySQL do accept them
  and are potentially in use by legacy code, not to mention that they
  will always pass through if unicode conversion is turned off
  for the target backend.
  References: [#3346](https://www.sqlalchemy.org/trac/ticket/3346)

### postgresql

- Fixed bug where updated PG index reflection as a result of
  [#3184](https://www.sqlalchemy.org/trac/ticket/3184) would cause index operations to fail on PostgreSQL
  versions 8.4 and earlier.  The enhancements are now
  disabled when using an older version of PostgreSQL.
  References: [#3343](https://www.sqlalchemy.org/trac/ticket/3343)

## 1.0.0b4

Released: March 29, 2015

### sql

- Fixed bug in new “label resolution” feature of [#2992](https://www.sqlalchemy.org/trac/ticket/2992) where
  a label that was anonymous, then labeled again with a name, would
  fail to be locatable via a textual label.  This situation occurs
  naturally when a mapped [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) is given an
  explicit label in a query.
  References: [#3340](https://www.sqlalchemy.org/trac/ticket/3340)
- Fixed bug in new “label resolution” feature of [#2992](https://www.sqlalchemy.org/trac/ticket/2992) where
  the string label placed in the order_by() or group_by() of a statement
  would place higher priority on the name as found
  inside the FROM clause instead of a more locally available name
  inside the columns clause.
  References: [#3335](https://www.sqlalchemy.org/trac/ticket/3335)

### schema

- The “auto-attach” feature of constraints such as [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint)
  and [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) has been further enhanced such that
  when the constraint is associated with non-table-bound [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects, the constraint will set up event listeners with the
  columns themselves such that the constraint auto attaches at the
  same time the columns are associated with the table.  This in particular
  helps in some edge cases in declarative but is also of general use.
  See also
  [Constraints referring to unattached Columns can auto-attach to the Table when their referred columns are attached](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3341)
  References: [#3341](https://www.sqlalchemy.org/trac/ticket/3341)

### mysql

- Fixed unicode support for PyMySQL when using an “executemany”
  operation with unicode parameters.  SQLAlchemy now passes both
  the statement as well as the bound parameters as unicode
  objects, as PyMySQL generally uses string interpolation
  internally to produce the final statement, and in the case of
  executemany does the “encode” step only on the final statement.
  This change is also **backported** to: 0.9.10
  References: [#3337](https://www.sqlalchemy.org/trac/ticket/3337)

### mssql

- Turned off the “simple order by” flag on the MSSQL, Oracle dialects;
  this is the flag that per [#2992](https://www.sqlalchemy.org/trac/ticket/2992) causes an order by or group by
  an expression that’s also in the columns clause to be copied by
  label, even if referenced as the expression object.   The behavior
  for MSSQL is now the old behavior that copies the whole expression
  in by default, as MSSQL can be picky on these particularly in
  GROUP BY expressions.  The flag is also turned off defensively
  for the Firebird and Sybase dialects.
  Note
  this resolution was incorrect, please see version 1.0.2
  for a rework of this resolution.
  References: [#3338](https://www.sqlalchemy.org/trac/ticket/3338)

## 1.0.0b3

Released: March 20, 2015

### mysql

- Repaired the commit for issue #2771 which was inadvertently commented
  out.
  References: [#2771](https://www.sqlalchemy.org/trac/ticket/2771)

## 1.0.0b2

Released: March 20, 2015

### orm

- Fixed unexpected use regression from pullreq github:137 where
  Py2K unicode literals (e.g. `u""`) would not be accepted by the
  [relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade) option.
  Pull request courtesy Julien Castets.
  References: [#3327](https://www.sqlalchemy.org/trac/ticket/3327)

### orm declarative

- Loosened some restrictions that were added to `@declared_attr`
  objects, such that they were prevented from being called outside
  of the declarative process; this is related to the enhancements
  of #3150 which allow `@declared_attr` to return a value that is
  cached based on the current class as it’s being configured.
  The exception raise has been removed, and the behavior changed
  so that outside of the declarative process, the function decorated by
  `@declared_attr` is called every time just like a regular
  `@property`, without using any caching, as none is available
  at this stage.
  References: [#3331](https://www.sqlalchemy.org/trac/ticket/3331)

### engine

- The “auto close” for `ResultProxy` is now a “soft” close.
  That is, after exhausting all rows using the fetch methods, the
  DBAPI cursor is released as before and the object may be safely
  discarded, but the fetch methods may continue to be called for which
  they will return an end-of-result object (None for fetchone, empty list
  for fetchmany and fetchall).   Only if `ResultProxy.close()`
  is called explicitly will these methods raise the “result is closed”
  error.
  See also
  [ResultProxy “auto close” is now a “soft” close](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3330)
  References: [#3329](https://www.sqlalchemy.org/trac/ticket/3329), [#3330](https://www.sqlalchemy.org/trac/ticket/3330)

### mysql

- Fixed the [BIT](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.BIT) type on Py3K which was not using the
  `ord()` function correctly.  Pull request courtesy David Marin.
  This change is also **backported** to: 0.9.10
  References: [#3333](https://www.sqlalchemy.org/trac/ticket/3333)
- Fixes to fully support using the `'utf8mb4'` MySQL-specific charset
  with MySQL dialects, in particular MySQL-Python and PyMySQL.   In
  addition, MySQL databases that report more unusual charsets such as
  ‘koi8u’ or ‘eucjpms’ will also work correctly.  Pull request
  courtesy Thomas Grainger.
  References: [#2771](https://www.sqlalchemy.org/trac/ticket/2771)

## 1.0.0b1

Released: March 13, 2015

Version 1.0.0b1 is the first release of the 1.0 series.   Many changes
described here are also present in the 0.9 and sometimes the 0.8
series as well.  For changes that are specific to 1.0 with an emphasis
on compatibility concerns, see [What’s New in SQLAlchemy 1.0?](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html).

### general

- Structural memory use has been improved via much more significant use
  of `__slots__` for many internal objects.  This optimization is
  particularly geared towards the base memory size of large applications
  that have lots of tables and columns, and greatly reduces memory
  size for a variety of high-volume objects including event listening
  internals, comparator objects and parts of the ORM attribute and
  loader strategy system.
  See also
  [Significant Improvements in Structural Memory Use](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-slots)
- The `__module__` attribute is now set for all those SQL and
  ORM functions that are derived as “public factory” symbols, which
  should assist with documentation tools being able to report on the
  target module.
  References: [#3218](https://www.sqlalchemy.org/trac/ticket/3218)

### orm

- Added a new entry `"entity"` to the dictionaries returned by
  [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions).  This refers to the primary ORM
  mapped class or aliased class that is referred to by the expression.
  Compared to the existing entry for `"type"`, it will always be
  a mapped entity, even if extracted from a column expression, or
  None if the given expression is a pure core expression.
  See also [#3403](https://www.sqlalchemy.org/trac/ticket/3403) which repaired a regression in this feature
  which was unreleased in 0.9.10 but was released in the 1.0 version.
  This change is also **backported** to: 0.9.10
  References: [#3320](https://www.sqlalchemy.org/trac/ticket/3320)
- Added new parameter [Session.connection.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection.params.execution_options)
  which may be used to set up execution options on a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
  when it is first checked out, before the transaction has begun.
  This is used to set up options such as isolation level on the
  connection before the transaction starts.
  See also
  [Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-transaction-isolation) - new documentation section
  detailing best practices for setting transaction isolation with
  sessions.
  This change is also **backported** to: 0.9.9
  References: [#3296](https://www.sqlalchemy.org/trac/ticket/3296)
- Added new method [Session.invalidate()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.invalidate), functions similarly
  to [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close), except also calls
  [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate)
  on all connections, guaranteeing that they will not be returned to
  the connection pool.  This is useful in situations e.g. dealing
  with gevent timeouts when it is not safe to use the connection further,
  even for rollbacks.
  This change is also **backported** to: 0.9.9
- The “primaryjoin” model has been stretched a bit further to allow
  a join condition that is strictly from a single column to itself,
  translated through some kind of SQL function or expression.  This
  is kind of experimental, but the first proof of concept is a
  “materialized path” join condition where a path string is compared
  to itself using “like”.   The [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like) operator has
  also been added to the list of valid operators to use in a primaryjoin
  condition.
  This change is also **backported** to: 0.9.5
  References: [#3029](https://www.sqlalchemy.org/trac/ticket/3029)
- Added new utility function [make_transient_to_detached()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient_to_detached) which can
  be used to manufacture objects that behave as though they were loaded
  from a session, then detached.   Attributes that aren’t present
  are marked as expired, and the object can be added to a Session
  where it will act like a persistent one.
  This change is also **backported** to: 0.9.5
  References: [#3017](https://www.sqlalchemy.org/trac/ticket/3017)
- Added a new event suite [QueryEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents).  The
  [QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) event allows the creation
  of functions which may place additional modifications to
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects before the construction of the SELECT
  statement.   It is hoped that this event be made much more
  useful via the advent of a new inspection system that will
  allow for detailed modifications to be made against
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects in an automated fashion.
  See also
  [QueryEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents)
  References: [#3317](https://www.sqlalchemy.org/trac/ticket/3317)
- The subquery wrapping which occurs when joined eager loading
  is used with a one-to-many query that also features LIMIT,
  OFFSET, or DISTINCT has been disabled in the case of a one-to-one
  relationship, that is a one-to-many with
  [relationship.uselist](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist) set to False.  This will produce
  more efficient queries in these cases.
  See also
  [Subqueries no longer applied to uselist=False joined eager loads](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3249)
  References: [#3249](https://www.sqlalchemy.org/trac/ticket/3249)
- Mapped state internals have been reworked to allow for a 50% reduction
  in callcounts specific to the “expiration” of objects, as in
  the “auto expire” feature of [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) and
  for [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all), as well as in the “cleanup” step
  which occurs when object states are garbage collected.
  References: [#3307](https://www.sqlalchemy.org/trac/ticket/3307)
- A warning is emitted when the same polymorphic identity is assigned
  to two different mappers in the same hierarchy.  This is typically a
  user error and means that the two different mapping types cannot be
  correctly distinguished at load time.  Pull request courtesy
  Sebastian Bank.
  References: [#3262](https://www.sqlalchemy.org/trac/ticket/3262)
- A new series of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) methods which provide hooks
  directly into the unit of work’s facility for emitting INSERT
  and UPDATE statements has been created.  When used correctly,
  this expert-oriented system can allow ORM-mappings to be used
  to generate bulk insert and update statements batched into
  executemany groups, allowing the statements to proceed at
  speeds that rival direct use of the Core.
  See also
  [Bulk Operations](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#bulk-operations)
  References: [#3100](https://www.sqlalchemy.org/trac/ticket/3100)
- Added a parameter [Query.join.isouter](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join.params.isouter) which is synonymous
  with calling [Query.outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.outerjoin); this flag is to provide a more
  consistent interface compared to Core [FromClause.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join).
  Pull request courtesy Jonathan Vanasco.
  References: [#3217](https://www.sqlalchemy.org/trac/ticket/3217)
- Added new event handlers [AttributeEvents.init_collection()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.init_collection)
  and [AttributeEvents.dispose_collection()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.dispose_collection), which track when
  a collection is first associated with an instance and when it is
  replaced.  These handlers supersede the `collection.linker()`
  annotation. The old hook remains supported through an event adapter.
- The [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) will raise an exception when [Query.yield_per()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.yield_per)
  is used with mappings or options where either
  subquery eager loading, or joined eager loading with collections,
  would take place.  These loading strategies are
  not currently compatible with yield_per, so by raising this error,
  the method is safer to use.  Eager loads can be disabled with
  the `lazyload('*')` option or [Query.enable_eagerloads()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.enable_eagerloads).
  See also
  [Joined/Subquery eager loading explicitly disallowed with yield_per](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-yield-per-eager-loading)
- A new implementation for `KeyedTuple` used by the
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object offers dramatic speed improvements when
  fetching large numbers of column-oriented rows.
  See also
  [New KeyedTuple implementation dramatically faster](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3176)
  References: [#3176](https://www.sqlalchemy.org/trac/ticket/3176)
- The behavior of [joinedload.innerjoin](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload.params.innerjoin) as well as
  [relationship.innerjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin) is now to use “nested”
  inner joins, that is, right-nested, as the default behavior when an
  inner join joined eager load is chained to an outer join eager load.
  See also
  [Right inner join nesting now the default for joinedload with innerjoin=True](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-3008)
  References: [#3008](https://www.sqlalchemy.org/trac/ticket/3008)
- UPDATE statements can now be batched within an ORM flush
  into more performant executemany() call, similarly to how INSERT
  statements can be batched; this will be invoked within flush
  to the degree that subsequent UPDATE statements for the
  same mapping and table involve the identical columns within the
  VALUES clause, that no SET-level SQL expressions
  are embedded, and that the versioning requirements for the mapping
  are compatible with the backend dialect’s ability to return
  a correct rowcount for an executemany operation.
- The `info` parameter has been added to the constructor for
  [SynonymProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.SynonymProperty) and `ComparableProperty`.
  References: [#2963](https://www.sqlalchemy.org/trac/ticket/2963)
- The `InspectionAttr.info` collection is now moved down to
  [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr), where in addition to being available
  on all [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty) objects, it is also now available
  on hybrid properties, association proxies, when accessed via
  [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors).
  References: [#2971](https://www.sqlalchemy.org/trac/ticket/2971)
- Mapped attributes marked as deferred without explicit undeferral
  will now remain “deferred” even if their column is otherwise
  present in the result set in some way.   This is a performance
  enhancement in that an ORM load no longer spends time searching
  for each deferred column when the result set is obtained.  However,
  for an application that has been relying upon this, an explicit
  [undefer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.undefer) or similar option should now be used.
- The `proc()` callable passed to the `create_row_processor()`
  method of custom [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) classes now accepts only a single
  “row” argument.
  See also
  [API Change for new Bundle feature when custom row loaders are used](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bundle-api-change)
- Deprecated event hooks removed:  `populate_instance`,
  `create_instance`, `translate_row`, `append_result`
  See also
  [Deprecated ORM Event Hooks Removed](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-deprecated-orm-events)
- Fixed bug in subquery eager loading where a long chain of
  eager loads across a polymorphic-subclass boundary in conjunction
  with polymorphic loading would fail to locate the subclass-link in the
  chain, erroring out with a missing property name on an
  [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass).
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3055](https://www.sqlalchemy.org/trac/ticket/3055)
- Fixed ORM bug where the [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper) function would mask
  AttributeErrors or KeyErrors that should raise during mapper
  configuration due to user errors.  The catch for attribute/keyerror
  has been made more specific to not include the configuration step.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3047](https://www.sqlalchemy.org/trac/ticket/3047)
- Fixed bugs in ORM object comparisons where comparison of
  many-to-one `!= None` would fail if the source were an aliased
  class, or if the query needed to apply special aliasing to the
  expression due to aliased joins or polymorphic querying; also fixed
  bug in the case where comparing a many-to-one to an object state
  would fail if the query needed to apply special aliasing
  due to aliased joins or polymorphic querying.
  This change is also **backported** to: 0.9.9
  References: [#3310](https://www.sqlalchemy.org/trac/ticket/3310)
- Fixed bug where internal assertion would fail in the case where
  an `after_rollback()` handler for a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) incorrectly
  adds state to that [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) within the handler, and the task
  to warn and remove this state (established by [#2389](https://www.sqlalchemy.org/trac/ticket/2389)) attempts
  to proceed.
  This change is also **backported** to: 0.9.9
  References: [#3309](https://www.sqlalchemy.org/trac/ticket/3309)
- Fixed bug where TypeError raised when [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) called
  with unknown kw arguments would raise its own TypeError due
  to broken formatting.  Pull request courtesy Malthe Borch.
  This change is also **backported** to: 0.9.9
- Fixed bug in lazy loading SQL construction whereby a complex
  primaryjoin that referred to the same “local” column multiple
  times in the “column that points to itself” style of self-referential
  join would not be substituted in all cases.   The logic to determine
  substitutions here has been reworked to be more open-ended.
  This change is also **backported** to: 0.9.9
  References: [#3300](https://www.sqlalchemy.org/trac/ticket/3300)
- The “wildcard” loader options, in particular the one set up by
  the [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) option to cover all attributes not
  explicitly mentioned, now takes into account the superclasses
  of a given entity, if that entity is mapped with inheritance mapping,
  so that attribute names within the superclasses are also omitted
  from the load.  Additionally, the polymorphic discriminator column
  is unconditionally included in the list, just in the same way that
  primary key columns are, so that even with load_only() set up,
  polymorphic loading of subtypes continues to function correctly.
  This change is also **backported** to: 0.9.9
  References: [#3287](https://www.sqlalchemy.org/trac/ticket/3287)
- Fixed bug where if an exception were thrown at the start of a
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) before it fetched results, particularly when
  row processors can’t be formed, the cursor would stay open with
  results pending and not actually be closed.  This is typically only
  an issue on an interpreter like PyPy where the cursor isn’t
  immediately GC’ed, and can in some circumstances lead to transactions/
  locks being open longer than is desirable.
  This change is also **backported** to: 0.9.9
  References: [#3285](https://www.sqlalchemy.org/trac/ticket/3285)
- Fixed a leak which would occur in the unsupported and highly
  non-recommended use case of replacing a relationship on a fixed
  mapped class many times, referring to an arbitrarily growing number of
  target mappers.  A warning is emitted when the old relationship is
  replaced, however if the mapping were already used for querying, the
  old relationship would still be referenced within some registries.
  This change is also **backported** to: 0.9.9
  References: [#3251](https://www.sqlalchemy.org/trac/ticket/3251)
- Fixed bug regarding expression mutations which could express
  itself as a “Could not locate column” error when using
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) to  select from multiple, anonymous column
  entities when querying against SQLite, as a side effect of the
  “join rewriting” feature used by the SQLite dialect.
  This change is also **backported** to: 0.9.9
  References: [#3241](https://www.sqlalchemy.org/trac/ticket/3241)
- Fixed bug where the ON clause for [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join),
  and [Query.outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.outerjoin) to a single-inheritance subclass
  using `of_type()` would not render the “single table criteria” in
  the ON clause if the `from_joinpoint=True` flag were set.
  This change is also **backported** to: 0.9.9
  References: [#3232](https://www.sqlalchemy.org/trac/ticket/3232)
- Fixed bug that affected generally the same classes of event
  as that of [#3199](https://www.sqlalchemy.org/trac/ticket/3199), when the `named=True` parameter
  would be used.  Some events would fail to register, and others
  would not invoke the event arguments correctly, generally in the
  case of when an event was “wrapped” for adaption in some other way.
  The “named” mechanics have been rearranged to not interfere with
  the argument signature expected by internal wrapper functions.
  This change is also **backported** to: 0.9.8
  References: [#3197](https://www.sqlalchemy.org/trac/ticket/3197)
- Fixed bug that affected many classes of event, particularly
  ORM events but also engine events, where the usual logic of
  “de duplicating” a redundant call to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen)
  with the same arguments would fail, for those events where the
  listener function is wrapped.  An assertion would be hit within
  registry.py.  This assertion has now been integrated into the
  deduplication check, with the added bonus of a simpler means
  of checking deduplication across the board.
  This change is also **backported** to: 0.9.8
  References: [#3199](https://www.sqlalchemy.org/trac/ticket/3199)
- Fixed warning that would emit when a complex self-referential
  primaryjoin contained functions, while at the same time remote_side
  was specified; the warning would suggest setting “remote side”.
  It now only emits if remote_side isn’t present.
  This change is also **backported** to: 0.9.8
  References: [#3194](https://www.sqlalchemy.org/trac/ticket/3194)
- Fixed a regression caused by [#2976](https://www.sqlalchemy.org/trac/ticket/2976) released in 0.9.4 where
  the “outer join” propagation along a chain of joined eager loads
  would incorrectly convert an “inner join” along a sibling join path
  into an outer join as well, when only descendant paths should be
  receiving the “outer join” propagation; additionally, fixed related
  issue where “nested” join propagation would take place inappropriately
  between two sibling join paths.
  This change is also **backported** to: 0.9.7
  References: [#3131](https://www.sqlalchemy.org/trac/ticket/3131)
- Fixed a regression from 0.9.0 due to [#2736](https://www.sqlalchemy.org/trac/ticket/2736) where the
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method no longer set up the “from
  entity” of the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object correctly, so that
  subsequent [Query.filter_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter_by) or [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join)
  calls would fail to check the appropriate “from” entity when
  searching for attributes by string name.
  This change is also **backported** to: 0.9.7
  References: [#2736](https://www.sqlalchemy.org/trac/ticket/2736), [#3083](https://www.sqlalchemy.org/trac/ticket/3083)
- Fixed bug where items that were persisted, deleted, or had a
  primary key change within a savepoint block would not
  participate in being restored to their former state (not in
  session, in session, previous PK) after the outer transaction
  were rolled back.
  This change is also **backported** to: 0.9.7
  References: [#3108](https://www.sqlalchemy.org/trac/ticket/3108)
- Fixed bug in subquery eager loading in conjunction with
  [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic), the targeting of entities and columns
  in the subquery load has been made more accurate with respect
  to this type of entity and others.
  This change is also **backported** to: 0.9.7
  References: [#3106](https://www.sqlalchemy.org/trac/ticket/3106)
- Additional checks have been added for the case where an inheriting
  mapper is implicitly combining one of its column-based attributes
  with that of the parent, where those columns normally don’t necessarily
  share the same value.  This is an extension of an existing check that
  was added via [#1892](https://www.sqlalchemy.org/trac/ticket/1892); however this new check emits only a
  warning, instead of an exception, to allow for applications that may
  be relying upon the existing behavior.
  See also
  [I’m getting a warning or error about “Implicitly combining column X under attribute Y”](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#faq-combining-columns)
  This change is also **backported** to: 0.9.5
  References: [#3042](https://www.sqlalchemy.org/trac/ticket/3042)
- Modified the behavior of [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) such that primary key
  columns are always added to the list of columns to be “undeferred”;
  otherwise, the ORM can’t load the row’s identity.   Apparently,
  one can defer the mapped primary keys and the ORM will fail, that
  hasn’t been changed.  But as load_only is essentially saying
  “defer all but X”, it’s more critical that PK cols not be part of this
  deferral.
  This change is also **backported** to: 0.9.5
  References: [#3080](https://www.sqlalchemy.org/trac/ticket/3080)
- Fixed a few edge cases which arise in the so-called “row switch”
  scenario, where an INSERT/DELETE can be turned into an UPDATE.
  In this situation, a many-to-one relationship set to None, or
  in some cases a scalar attribute set to None, may not be detected
  as a net change in value, and therefore the UPDATE would not reset
  what was on the previous row.   This is due to some as-yet
  unresolved side effects of the way attribute history works in terms
  of implicitly assuming None isn’t really a “change” for a previously
  un-set attribute.  See also [#3061](https://www.sqlalchemy.org/trac/ticket/3061).
  Note
  This change has been **REVERTED** in 0.9.6.   The full fix
  will be in version 1.0 of SQLAlchemy.
  This change is also **backported** to: 0.9.5
  References: [#3060](https://www.sqlalchemy.org/trac/ticket/3060)
- Related to [#3060](https://www.sqlalchemy.org/trac/ticket/3060), an adjustment has been made to the unit
  of work such that loading for related many-to-one objects is slightly
  more aggressive, in the case of a graph of self-referential objects
  that are to be deleted; the load of related objects is to help
  determine the correct order for deletion if passive_deletes is
  not set.
  This change is also **backported** to: 0.9.5
- Fixed bug in SQLite join rewriting where anonymized column names
  due to repeats would not correctly be rewritten in subqueries.
  This would affect SELECT queries with any kind of subquery + join.
  This change is also **backported** to: 0.9.5
  References: [#3057](https://www.sqlalchemy.org/trac/ticket/3057)
- Fixes to the newly enhanced boolean coercion in [#2804](https://www.sqlalchemy.org/trac/ticket/2804) where
  the new rules for “where” and “having” wouldn’t take effect for the
  “whereclause” and “having” kw arguments of the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct,
  which is also what [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) uses so wasn’t working in the
  ORM either.
  This change is also **backported** to: 0.9.5
  References: [#3013](https://www.sqlalchemy.org/trac/ticket/3013)
- Fixed bug where the session attachment error “object is already
  attached to session X” would fail to prevent the object from
  also being attached to the new session, in the case that execution
  continued after the error raise occurred.
  References: [#3301](https://www.sqlalchemy.org/trac/ticket/3301)
- The primary [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) of a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is now passed to the
  [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) method when calling upon
  [Query.count()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.count), [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update), [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete),
  as well as queries against mapped columns,
  [column_property](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) objects, and SQL functions and expressions
  derived from mapped columns.   This allows sessions that rely upon
  either customized [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) schemes or “bound” metadata
  to work in all relevant cases.
  See also
  [Session.get_bind() will receive the Mapper in all relevant Query cases](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3227)
  References: [#1326](https://www.sqlalchemy.org/trac/ticket/1326), [#3227](https://www.sqlalchemy.org/trac/ticket/3227), [#3242](https://www.sqlalchemy.org/trac/ticket/3242)
- The [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) modifier has been
  improved in conjunction with loader directives such as
  [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) and [contains_eager()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.contains_eager) such that if
  two [PropComparator.of_type()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) modifiers of the same
  base type/path are encountered, they will be joined together
  into a single “polymorphic” entity, rather than replacing
  the entity of type A with the one of type B.  E.g.
  a joinedload of `A.b.of_type(BSub1)->BSub1.c` combined with
  joinedload of `A.b.of_type(BSub2)->BSub2.c` will create a
  single joinedload of `A.b.of_type((BSub1, BSub2)) -> BSub1.c, BSub2.c`,
  without the need for the `with_polymorphic` to be explicit
  in the query.
  See also
  [Eager Loading of Polymorphic Subtypes](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#eagerloading-polymorphic-subtypes) - contains an updated
  example illustrating the new format.
  References: [#3256](https://www.sqlalchemy.org/trac/ticket/3256)
- Repaired support of the `copy.deepcopy()` call when used by the
  [CascadeOptions](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.CascadeOptions) argument, which occurs
  if `copy.deepcopy()` is being used with [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
  (not an officially supported use case).  Pull request courtesy
  duesenfranz.
- Fixed bug where [Session.expunge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expunge) would not fully detach
  the given object if the object had been subject to a delete
  operation that was flushed, but not committed.  This would also
  affect related operations like [make_transient()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient).
  See also
  [session.expunge() will fully detach an object that’s been deleted](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3139)
  References: [#3139](https://www.sqlalchemy.org/trac/ticket/3139)
- A warning is emitted in the case of multiple relationships that
  ultimately will populate a foreign key column in conflict with
  another, where the relationships are attempting to copy values
  from different source columns.  This occurs in the case where
  composite foreign keys with overlapping columns are mapped to
  relationships that each refer to a different referenced column.
  A new documentation section illustrates the example as well as how
  to overcome the issue by specifying “foreign” columns specifically
  on a per-relationship basis.
  See also
  [Overlapping Foreign Keys](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-overlapping-foreignkeys)
  References: [#3230](https://www.sqlalchemy.org/trac/ticket/3230)
- The [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) method will now convert string key
  names in the given dictionary of values into mapped attribute names
  against the mapped class being updated.  Previously, string names
  were taken in directly and passed to the core update statement without
  any means to resolve against the mapped entity.  Support for synonyms
  and hybrid attributes as the subject attributes of
  [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) are also supported.
  See also
  [query.update() now resolves string names into mapped attribute names](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3228)
  References: [#3228](https://www.sqlalchemy.org/trac/ticket/3228)
- Improvements to the mechanism used by [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to locate
  “binds” (e.g. engines to use), such engines can be associated with
  mixin classes, concrete subclasses, as well as a wider variety
  of table metadata such as joined inheritance tables.
  See also
  [Session.get_bind() handles a wider variety of inheritance scenarios](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3035)
  References: [#3035](https://www.sqlalchemy.org/trac/ticket/3035)
- Fixed bug in single table inheritance where a chain of joins
  that included the same single inh entity more than once
  (normally this should raise an error) could, in some cases
  depending on what was being joined “from”, implicitly alias the
  second case of the single inh entity, producing
  a query that “worked”.   But as this implicit aliasing is not
  intended in the case of single table inheritance, it didn’t
  really “work” fully and was very misleading, since it wouldn’t
  always appear.
  See also
  [Changes and fixes in handling of duplicate join targets](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3233)
  References: [#3233](https://www.sqlalchemy.org/trac/ticket/3233)
- The ON clause rendered when using [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join),
  [Query.outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.outerjoin), or the standalone [join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.join) /
  [outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.outerjoin) functions to a single-inheritance subclass will
  now include the “single table criteria” in the ON clause even
  if the ON clause is otherwise hand-rolled; it is now added to the
  criteria using AND, the same way as if joining to a single-table
  target using relationship or similar.
  This is sort of in-between feature and bug.
  See also
  [single-table-inheritance criteria added to all ON clauses unconditionally](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-3222)
  References: [#3222](https://www.sqlalchemy.org/trac/ticket/3222)
- A major rework to the behavior of expression labels, most
  specifically when used with ColumnProperty constructs with
  custom SQL expressions and in conjunction with the “order by
  labels” logic first introduced in 0.9.  Fixes include that an
  `order_by(Entity.some_col_prop)` will now make use of “order by
  label” rules even if Entity has been subject to aliasing,
  either via inheritance rendering or via the use of the
  `aliased()` construct; rendering of the same column property
  multiple times with aliasing (e.g. `query(Entity.some_prop,
  entity_alias.some_prop)`) will label each occurrence of the
  entity with a distinct label, and additionally “order by
  label” rules will work for both (e.g.
  `order_by(Entity.some_prop, entity_alias.some_prop)`).
  Additional issues that could prevent the “order by label”
  logic from working in 0.9, most notably that the state of a
  Label could change such that “order by label” would stop
  working depending on how things were called, has been fixed.
  See also
  [ColumnProperty constructs work a lot better with aliases, order_by](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3188)
  References: [#3148](https://www.sqlalchemy.org/trac/ticket/3148), [#3188](https://www.sqlalchemy.org/trac/ticket/3188)
- Changed the approach by which the “single inheritance criterion”
  is applied, when using `Query.from_self()`, or its common
  user [Query.count()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.count).  The criteria to limit rows to those
  with a certain type is now indicated on the inside subquery,
  not the outside one, so that even if the “type” column is not
  available in the columns clause, we can filter on it on the “inner”
  query.
  See also
  [Change to single-table-inheritance criteria when using from_self(), count()](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-3177)
  References: [#3177](https://www.sqlalchemy.org/trac/ticket/3177)
- Made a small adjustment to the mechanics of lazy loading,
  such that it has less chance of interfering with a joinload() in the
  very rare circumstance that an object points to itself; in this
  scenario, the object refers to itself while loading its attributes
  which can cause a mixup between loaders.   The use case of
  “object points to itself” is not fully supported, but the fix also
  removes some overhead so for now is part of testing.
  References: [#3145](https://www.sqlalchemy.org/trac/ticket/3145)
- The “resurrect” ORM event has been removed.  This event hook had
  no purpose since the old “mutable attribute” system was removed
  in 0.8.
  References: [#3171](https://www.sqlalchemy.org/trac/ticket/3171)
- Fixed bug where attribute “set” events or columns with
  `@validates` would have events triggered within the flush process,
  when those columns were the targets of a “fetch and populate”
  operation, such as an autoincremented primary key, a Python side
  default, or a server-side default “eagerly” fetched via RETURNING.
  References: [#3167](https://www.sqlalchemy.org/trac/ticket/3167)
- The [IdentityMap](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.IdentityMap) exposed from [Session.identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.identity_map)
  now returns lists for `items()` and `values()` in Py3K.
  Early porting to Py3K here had these returning iterators, when
  they technically should be “iterable views”..for now, lists are OK.
- The “evaluator” for query.update()/delete() won’t work with multi-table
  updates, and needs to be set to synchronize_session=False or
  synchronize_session=’fetch’; this now raises an exception, with a
  message to change the synchronize setting.
  This is upgraded from a warning emitted as of 0.9.7.
  References: [#3117](https://www.sqlalchemy.org/trac/ticket/3117)
- Adjustment to attribute mechanics concerning when a value is
  implicitly initialized to None via first access; this action,
  which has always resulted in a population of the attribute,
  no longer does so; the None value is returned but the underlying
  attribute receives no set event.  This is consistent with how collections
  work and allows attribute mechanics to behave more consistently;
  in particular, getting an attribute with no value does not squash
  the event that should proceed if the value is actually set to None.
  See also
  [Changes to attribute events and other operations regarding attributes that have no pre-existing value](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-3061)
  where bound parameters are rendered inline as strings based on
  a compile-time option.
  Work on this feature is courtesy of Dobes Vandermeer.
  > See also
  >
  >
  >
  > [Select/Query LIMIT / OFFSET may be specified as an arbitrary SQL expression](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3034).
  References: [#3061](https://www.sqlalchemy.org/trac/ticket/3061)

### orm declarative

- The [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) construct has newly improved
  behaviors and features in conjunction with declarative.  The
  decorated function will now have access to the final column
  copies present on the local mixin when invoked, and will also
  be invoked exactly once for each mapped class, the returned result
  being memoized.   A new modifier [declared_attr.cascading](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.cascading)
  is added as well.
  See also
  [Improvements to declarative mixins, @declared_attr and related features](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3150)
  References: [#3150](https://www.sqlalchemy.org/trac/ticket/3150)
- Fixed “‘NoneType’ object has no attribute ‘concrete’” error
  when using [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) in conjunction with
  a subclass that declares `__abstract__`.
  This change is also **backported** to: 0.9.8
  References: [#3185](https://www.sqlalchemy.org/trac/ticket/3185)
- Fixed bug where using an `__abstract__` mixin in the middle
  of a declarative inheritance hierarchy would prevent attributes
  and configuration being correctly propagated from the base class
  to the inheriting class.
  References: [#3219](https://www.sqlalchemy.org/trac/ticket/3219), [#3240](https://www.sqlalchemy.org/trac/ticket/3240)
- A relationship set up with [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) on
  a [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) base class will now be configured
  on the abstract base mapping automatically, in addition to being
  set up on descendant concrete classes as usual.
  See also
  [Improvements to declarative mixins, @declared_attr and related features](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3150)
  References: [#2670](https://www.sqlalchemy.org/trac/ticket/2670)

### examples

- Added a new example illustrating materialized paths, using the
  latest relationship features.   Example courtesy Jack Zhou.
  This change is also **backported** to: 0.9.5
- A new suite of examples dedicated to providing a detailed study
  into performance of SQLAlchemy ORM and Core, as well as the DBAPI,
  from multiple perspectives.  The suite runs within a container
  that provides built in profiling displays both through console
  output as well as graphically via the RunSnake tool.
  See also
  [Performance](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-performance)
- Updated the [Versioning with a History Table](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioned-history) example such that
  mapped columns are re-mapped to
  match column names as well as grouping of columns; in particular,
  this allows columns that are explicitly grouped in a same-column-named
  joined inheritance scenario to be mapped in the same way in the
  history mappings, avoiding warnings added in the 0.9 series
  regarding this pattern and allowing the same view of attribute
  keys.
  This change is also **backported** to: 0.9.9
- Fixed a bug in the examples/generic_associations/discriminator_on_association.py
  example, where the subclasses of AddressAssociation were not being
  mapped as “single table inheritance”, leading to problems when trying
  to use the mappings further.
  This change is also **backported** to: 0.9.9

### engine

- Added new user-space accessors for viewing transaction isolation
  levels; [Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level),
  [Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level).
  This change is also **backported** to: 0.9.9
- Added new event `ConnectionEvents.handle_error()`, a more
  fully featured and comprehensive replacement for
  `ConnectionEvents.dbapi_error()`.
  This change is also **backported** to: 0.9.7
  References: [#3076](https://www.sqlalchemy.org/trac/ticket/3076)
- A new style of warning can be emitted which will “filter” up to
  N occurrences of a parameterized string.   This allows parameterized
  warnings that can refer to their arguments to be delivered a fixed
  number of times until allowing Python warning filters to squelch them,
  and prevents memory from growing unbounded within Python’s
  warning registries.
  See also
  [Session.get_bind() handles a wider variety of inheritance scenarios](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3178)
  References: [#3178](https://www.sqlalchemy.org/trac/ticket/3178)
- Fixed bug in [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and pool where the
  [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate) method, or an invalidation due
  to a database disconnect, would fail if the
  `isolation_level` parameter had been used with
  [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options); the “finalizer” that resets
  the isolation level would be called on the no longer opened connection.
  This change is also **backported** to: 0.9.9
  References: [#3302](https://www.sqlalchemy.org/trac/ticket/3302)
- A warning is emitted if the `isolation_level` parameter is used
  with [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) when a [Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction)
  is in play; DBAPIs and/or SQLAlchemy dialects such as psycopg2,
  MySQLdb may implicitly rollback or commit the transaction, or
  not change the setting til next transaction, so this is never safe.
  This change is also **backported** to: 0.9.9
  References: [#3296](https://www.sqlalchemy.org/trac/ticket/3296)
- The execution options passed to an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) either via
  [create_engine.execution_options](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.execution_options) or
  [Engine.update_execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine.update_execution_options) are not passed to the
  special [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) used to initialize the dialect
  within the “first connect” event; dialects will usually
  perform their own queries in this phase, and none of the
  current available  options should be applied here.  In
  particular, the “autocommit” option was causing an attempt to
  autocommit within this initial connect which would fail with
  an AttributeError due to the non-standard state of the
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
  This change is also **backported** to: 0.9.8
  References: [#3200](https://www.sqlalchemy.org/trac/ticket/3200)
- The string keys that are used to determine the columns impacted
  for an INSERT or UPDATE are now sorted when they contribute towards
  the “compiled cache” cache key.   These keys were previously not
  deterministically ordered, meaning the same statement could be
  cached multiple times on equivalent keys, costing both in terms of
  memory as well as performance.
  This change is also **backported** to: 0.9.8
  References: [#3165](https://www.sqlalchemy.org/trac/ticket/3165)
- Fixed bug which would occur if a DBAPI exception
  occurs when the engine first connects and does its initial checks,
  and the exception is not a disconnect exception, yet the cursor
  raises an error when we try to close it.  In this case the real
  exception would be quashed as we tried to log the cursor close
  exception via the connection pool and failed, as we were trying
  to access the pool’s logger in a way that is inappropriate
  in this very specific scenario.
  This change is also **backported** to: 0.9.5
  References: [#3063](https://www.sqlalchemy.org/trac/ticket/3063)
- Fixed some “double invalidate” situations were detected where
  a connection invalidation could occur within an already critical section
  like a connection.close(); ultimately, these conditions are caused
  by the change in [#2907](https://www.sqlalchemy.org/trac/ticket/2907), in that the “reset on return” feature
  calls out to the Connection/Transaction in order to handle it, where
  “disconnect detection” might be caught.  However, it’s possible that
  the more recent change in [#2985](https://www.sqlalchemy.org/trac/ticket/2985) made it more likely for this
  to be seen as the “connection invalidate” operation is much quicker,
  as the issue is more reproducible on 0.9.4 than 0.9.3.
  Checks are now added within any section that
  an invalidate might occur to halt further disallowed operations
  on the invalidated connection.  This includes two fixes both at the
  engine level and at the pool level.   While the issue was observed
  with highly concurrent gevent cases, it could in theory occur in
  any kind of scenario where a disconnect occurs within the connection
  close operation.
  This change is also **backported** to: 0.9.5
  References: [#3043](https://www.sqlalchemy.org/trac/ticket/3043)
- The engine-level error handling and wrapping routines will now
  take effect in all engine connection use cases, including
  when user-custom connect routines are used via the
  [create_engine.creator](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.creator) parameter, as well as when
  the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) encounters a connection error on
  revalidation.
  See also
  [DBAPI exception wrapping and handle_error() event improvements](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3266)
  References: [#3266](https://www.sqlalchemy.org/trac/ticket/3266)
- Removing (or adding) an event listener at the same time that the event
  is being run itself, either from inside the listener or from a
  concurrent thread, now raises a RuntimeError, as the collection used is
  now an instance of `collections.deque()` and does not support changes
  while being iterated.  Previously, a plain Python list was used where
  removal from inside the event itself would produce silent failures.
  References: [#3163](https://www.sqlalchemy.org/trac/ticket/3163)

### sql

- Liberalized the contract for [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) a bit in that you can
  specify a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) expression as the target; the index no longer
  needs to have a table-bound column present if the index is to be
  manually added to the table, either via inline declaration or via
  [Table.append_constraint()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_constraint).
  This change is also **backported** to: 0.9.5
  References: [#3028](https://www.sqlalchemy.org/trac/ticket/3028)
- Added new flag [between.symmetric](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between.params.symmetric), when set to True
  renders “BETWEEN SYMMETRIC”.  Also added a new negation operator
  “notbetween_op”, which now allows an expression like `~col.between(x, y)`
  to render as “col NOT BETWEEN x AND y”, rather than a parenthesized NOT
  string.
  This change is also **backported** to: 0.9.5
  References: [#2990](https://www.sqlalchemy.org/trac/ticket/2990)
- The SQL compiler now generates the mapping of expected columns
  such that they are matched to the received result set positionally,
  rather than by name.  Originally, this was seen as a way to handle
  cases where we had columns returned with difficult-to-predict names,
  though in modern use that issue has been overcome by anonymous
  labeling.   In this version, the approach basically reduces function
  call count per-result by a few dozen calls, or more for larger
  sets of result columns.  The approach still degrades into a modern
  version of the old approach if any discrepancy in size exists between
  the compiled set of columns versus what was received, so there’s no
  issue for partially or fully textual compilation scenarios where these
  lists might not line up.
  References: [#918](https://www.sqlalchemy.org/trac/ticket/918)
- Literal values within a [DefaultClause](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultClause), which is invoked
  when using the [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) parameter, will
  now be rendered using the “inline” compiler, so that they are rendered
  as-is, rather than as bound parameters.
  See also
  [Column server defaults now render literal values](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3087)
  References: [#3087](https://www.sqlalchemy.org/trac/ticket/3087)
- The type of expression is reported when an object passed to a
  SQL expression unit can’t be interpreted as a SQL fragment;
  pull request courtesy Ryan P. Kelly.
- Added a new parameter [Table.tometadata.name](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata.params.name) to
  the [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) method.  Similar to
  [Table.tometadata.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata.params.schema), this argument causes the newly
  copied [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to take on the new name instead of
  the existing one.  An interesting capability this adds is that of
  copying a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object to the *same* [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  target with a new name.  Pull request courtesy n.d. parker.
- Exception messages have been spiffed up a bit.  The SQL statement
  and parameters are not displayed if None, reducing confusion for
  error messages that weren’t related to a statement.  The full
  module and classname for the DBAPI-level exception is displayed,
  making it clear that this is a wrapped DBAPI exception.  The
  statement and parameters themselves are bounded within a bracketed
  sections to better isolate them from the error message and from
  each other.
  References: [#3172](https://www.sqlalchemy.org/trac/ticket/3172)
- [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) now includes Python and SQL-expression
  defaults if otherwise unspecified; the limitation where non-
  server column defaults aren’t included in an INSERT FROM
  SELECT is now lifted and these expressions are rendered as
  constants into the SELECT statement.
  See also
  [INSERT FROM SELECT now includes Python and SQL-expression defaults](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-insert-from-select-defaults)
- The [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) construct is now included when
  reflecting a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, for databases where this
  is applicable.  In order to achieve this
  with sufficient accuracy, MySQL and PostgreSQL now contain features
  that correct for the duplication of indexes and unique constraints
  when reflecting tables, indexes, and constraints.
  In the case of MySQL, there is not actually a “unique constraint”
  concept independent of a “unique index”, so for this backend
  [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) continues to remain non-present for a
  reflected [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).  For PostgreSQL, the query used to
  detect indexes against `pg_index` has been improved to check for
  the same construct in `pg_constraint`, and the implicitly
  constructed unique index is not included with a
  reflected [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  In both cases, the  [Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes) and the
  [Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints) methods return both
  constructs individually, but include a new token
  `duplicates_constraint` in the case of PostgreSQL or
  `duplicates_index` in the case
  of MySQL to indicate when this condition is detected.
  Pull request courtesy Johannes Erdfelt.
  See also
  [UniqueConstraint is now part of the Table reflection process](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3184)
  References: [#3184](https://www.sqlalchemy.org/trac/ticket/3184)
- Added new method [Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) and ORM
  method [Query.with_statement_hint()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_statement_hint) to support statement-level
  hints that are not specific to a table.
  References: [#3206](https://www.sqlalchemy.org/trac/ticket/3206)
- The `info` parameter has been added as a constructor argument
  to all schema constructs including [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData),
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey), [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint),
  [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint), [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint),
  [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint).
  References: [#2963](https://www.sqlalchemy.org/trac/ticket/2963)
- The [Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with) flag now implies that
  [Table.autoload](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload) should be `True`.  Pull request
  courtesy Malik Diarra.
  References: [#3027](https://www.sqlalchemy.org/trac/ticket/3027)
- The [Select.limit()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.limit) and [Select.offset()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.offset) methods
  now accept any SQL expression, in addition to integer values, as
  arguments.  Typically this is used to allow a bound parameter to be
  passed, which can be substituted with a value later thus allowing
  Python-side caching of the SQL query.   The implementation
  here is fully backwards compatible with existing third party dialects,
  however those dialects which implement special LIMIT/OFFSET systems
  will need modification in order to take advantage of the new
  capabilities.  Limit and offset also support “literal_binds” mode,
  References: [#3034](https://www.sqlalchemy.org/trac/ticket/3034)
- The [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) and [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table)
  constructs are now importable from the “from sqlalchemy” namespace,
  just like every other Core construct.
- The implicit conversion of strings to [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) constructs
  when passed to most builder methods of [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) as
  well as [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) now emits a warning with just the
  plain string sent.   The textual conversion still proceeds normally,
  however.  The only method that accepts a string without a warning
  are the “label reference” methods like order_by(), group_by();
  these functions will now at compile time attempt to resolve a single
  string argument to a column or label expression present in the
  selectable; if none is located, the expression still renders, but
  you get the warning again. The rationale here is that the implicit
  conversion from string to text is more unexpected than not these days,
  and it is better that the user send more direction to the Core / ORM
  when passing a raw string as to what direction should be taken.
  Core/ORM tutorials have been updated to go more in depth as to how text
  is handled.
  See also
  [Warnings emitted when coercing full SQL fragments into text()](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#migration-2992)
  References: [#2992](https://www.sqlalchemy.org/trac/ticket/2992)
- Fixed bug in [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) and other [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType)
  subclasses where direct association of the type with a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) would lead to a hang when events
  (like create events) were emitted on the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).
  This change is also **backported** to: 0.9.7, 0.8.7
  References: [#3124](https://www.sqlalchemy.org/trac/ticket/3124)
- Fixed a bug within the custom operator plus [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant)
  system, whereby using a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) in conjunction with
  variant would fail with an MRO error when a comparison operator was used.
  This change is also **backported** to: 0.9.7, 0.8.7
  References: [#3102](https://www.sqlalchemy.org/trac/ticket/3102)
- Fixed bug in INSERT..FROM SELECT construct where selecting from a
  UNION would wrap the union in an anonymous (e.g. unlabeled) subquery.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3044](https://www.sqlalchemy.org/trac/ticket/3044)
- Fixed bug where [Table.update()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.update) and [Table.delete()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.delete)
  would produce an empty WHERE clause when an empty [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
  or [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) or other blank expression were applied.  This is
  now consistent with that of [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3045](https://www.sqlalchemy.org/trac/ticket/3045)
- Added the `native_enum` flag to the `__repr__()` output
  of [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), which is mostly important when using it with
  Alembic autogenerate.  Pull request courtesy Dimitris Theodorou.
  This change is also **backported** to: 0.9.9
- Fixed bug where using a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) that implemented
  a type that was also a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) would fail with
  Python’s “Cannot create a consistent method resolution order (MRO)”
  error, when any kind of SQL comparison expression were used against
  an object using this type.
  This change is also **backported** to: 0.9.9
  References: [#3278](https://www.sqlalchemy.org/trac/ticket/3278)
- Fixed issue where the columns from a SELECT embedded in an
  INSERT, either through the values clause or as a “from select”,
  would pollute the column types used in the result set produced by
  the RETURNING clause when columns from both statements shared the
  same name, leading to potential errors or mis-adaptation when
  retrieving the returning rows.
  This change is also **backported** to: 0.9.9
  References: [#3248](https://www.sqlalchemy.org/trac/ticket/3248)
- Fixed bug where a fair number of SQL elements within
  the sql package would fail to `__repr__()` successfully,
  due to a missing `description` attribute that would then invoke
  a recursion overflow when an internal AttributeError would then
  re-invoke `__repr__()`.
  This change is also **backported** to: 0.9.8
  References: [#3195](https://www.sqlalchemy.org/trac/ticket/3195)
- An adjustment to table/index reflection such that if an index
  reports a column that isn’t found to be present in the table,
  a warning is emitted and the column is skipped.  This can occur
  for some special system column situations as has been observed
  with Oracle.
  This change is also **backported** to: 0.9.8
  References: [#3180](https://www.sqlalchemy.org/trac/ticket/3180)
- Fixed bug in CTE where `literal_binds` compiler argument would not
  be always be correctly propagated when one CTE referred to another
  aliased CTE in a statement.
  This change is also **backported** to: 0.9.8
  References: [#3154](https://www.sqlalchemy.org/trac/ticket/3154)
- Fixed 0.9.7 regression caused by [#3067](https://www.sqlalchemy.org/trac/ticket/3067) in conjunction with
  a mis-named unit test such that so-called “schema” types like
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) and [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) could no longer be pickled.
  This change is also **backported** to: 0.9.8
  References: [#3067](https://www.sqlalchemy.org/trac/ticket/3067), [#3144](https://www.sqlalchemy.org/trac/ticket/3144)
- Fix bug in naming convention feature where using a check
  constraint convention that includes `constraint_name` would
  then force all [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) and [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) types to
  require names as well, as these implicitly create a
  constraint, even if the ultimate target backend were one that does
  not require generation of the constraint such as PostgreSQL.
  The mechanics of naming conventions for these particular
  constraints has been reorganized such that the naming
  determination is done at DDL compile time, rather than at
  constraint/table construction time.
  This change is also **backported** to: 0.9.7
  References: [#3067](https://www.sqlalchemy.org/trac/ticket/3067)
- Fixed bug in common table expressions whereby positional bound
  parameters could be expressed in the wrong final order
  when CTEs were nested in certain ways.
  This change is also **backported** to: 0.9.7
  References: [#3090](https://www.sqlalchemy.org/trac/ticket/3090)
- Fixed bug where multi-valued [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct would fail
  to check subsequent values entries beyond the first one given
  for literal SQL expressions.
  This change is also **backported** to: 0.9.7
  References: [#3069](https://www.sqlalchemy.org/trac/ticket/3069)
- Added a “str()” step to the dialect_kwargs iteration for
  Python version < 2.6.5, working around the
  “no unicode keyword arg” bug as these args are passed along as
  keyword args within some reflection processes.
  This change is also **backported** to: 0.9.7
  References: [#3123](https://www.sqlalchemy.org/trac/ticket/3123)
- The [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method will now accept a
  type class as an argument which is internally converted to an
  instance, using the same convention long established by other
  constructs such as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
  This change is also **backported** to: 0.9.7
  References: [#3122](https://www.sqlalchemy.org/trac/ticket/3122)
- The [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable) flag is implicitly set to `False`
  when that [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is referred to in an explicit
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) for that table.  This behavior now
  matches that of when the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) itself has the
  [Column.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.primary_key) flag set to `True`, which is
  intended to be an exactly equivalent case.
  This change is also **backported** to: 0.9.5
  References: [#3023](https://www.sqlalchemy.org/trac/ticket/3023)
- Fixed bug where the [Operators.__and__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__and__),
  [Operators.__or__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__or__) and [Operators.__invert__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__invert__)
  operator overload methods could not be overridden within a custom
  [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) implementation.
  This change is also **backported** to: 0.9.5
  References: [#3012](https://www.sqlalchemy.org/trac/ticket/3012)
- Fixed bug in new [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method where
  adding an argument for a construct not previously included for any
  special arguments would fail.
  This change is also **backported** to: 0.9.5
  References: [#3024](https://www.sqlalchemy.org/trac/ticket/3024)
- Fixed regression introduced in 0.9 where new “ORDER BY <labelname>”
  feature from [#1068](https://www.sqlalchemy.org/trac/ticket/1068) would not apply quoting rules to the
  label name as rendered in the ORDER BY.
  This change is also **backported** to: 0.9.5
  References: [#1068](https://www.sqlalchemy.org/trac/ticket/1068), [#3020](https://www.sqlalchemy.org/trac/ticket/3020)
- Restored the import for [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) to the `sqlalchemy.sql.expression`
  import namespace, which was removed at the beginning of 0.9.
  This change is also **backported** to: 0.9.5
- The multi-values version of [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) has been
  repaired to work more usefully with tables that have Python-
  side default values and/or functions, as well as server-side
  defaults. The feature will now work with a dialect that uses
  “positional” parameters; a Python callable will also be
  invoked individually for each row just as is the case with an
  “executemany” style invocation; a server- side default column
  will no longer implicitly receive the value explicitly
  specified for the first row, instead refusing to invoke
  without an explicit value.
  See also
  [Python-side defaults invoked for each row individually when using a multivalued insert](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3288)
  References: [#3288](https://www.sqlalchemy.org/trac/ticket/3288)
- Fixed bug in [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) method where the
  [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) associated with a [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
  or [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type object would be doubled in the target table.
  The copy process now tracks the production of this constraint object
  as local to a type object.
  References: [#3260](https://www.sqlalchemy.org/trac/ticket/3260)
- The behavioral contract of the [ForeignKeyConstraint.columns](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.columns)
  collection has been made consistent; this attribute is now a
  [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) like that of all other constraints and
  is initialized at the point when the constraint is associated with
  a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  See also
  [ForeignKeyConstraint.columns is now a ColumnCollection](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3243)
  References: [#3243](https://www.sqlalchemy.org/trac/ticket/3243)
- The [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.key) attribute is now used as the source of
  anonymous bound parameter names within expressions, to match the
  existing use of this value as the key when rendered in an INSERT
  or UPDATE statement.   This allows [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.key) to be used
  as a “substitute” string to work around a difficult column name
  that doesn’t translate well into a bound parameter name.   Note that
  the paramstyle is configurable on [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) in any case,
  and most DBAPIs today support a named and positional style.
  References: [#3245](https://www.sqlalchemy.org/trac/ticket/3245)
- Fixed the name of the [PoolEvents.reset.dbapi_connection](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset.params.dbapi_connection)
  parameter as passed to this event; in particular this affects
  usage of the “named” argument style for this event.  Pull request
  courtesy Jason Goldberger.
- Reversing a change that was made in 0.9, the “singleton” nature
  of the “constants” [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null), [true()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.true), and [false()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.false)
  has been reverted.   These functions returning a “singleton” object
  had the effect that different instances would be treated as the
  same regardless of lexical use, which in particular would impact
  the rendering of the columns clause of a SELECT statement.
  See also
  [null(), false() and true() constants are no longer singletons](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3170)
  References: [#3170](https://www.sqlalchemy.org/trac/ticket/3170)
- Fixed bug where a “branched” connection, that is the kind you get
  when you call `Connection.connect()`, would not share invalidation
  status with the parent.  The architecture of branching has been tweaked
  a bit so that the branched connection defers to the parent for
  all invalidation status and operations.
  References: [#3215](https://www.sqlalchemy.org/trac/ticket/3215)
- Fixed bug where a “branched” connection, that is the kind you get
  when you call `Connection.connect()`, would not share transaction
  status with the parent.  The architecture of branching has been tweaked
  a bit so that the branched connection defers to the parent for
  all transactional status and operations.
  References: [#3190](https://www.sqlalchemy.org/trac/ticket/3190)
- Using [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select)  now implies `inline=True`
  on [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert).  This helps to fix a bug where an
  INSERT…FROM SELECT construct would inadvertently be compiled
  as “implicit returning” on supporting backends, which would
  cause breakage in the case of an INSERT that inserts zero rows
  (as implicit returning expects a row), as well as arbitrary
  return data in the case of an INSERT that inserts multiple
  rows (e.g. only the first row of many).
  A similar change is also applied to an INSERT..VALUES
  with multiple parameter sets; implicit RETURNING will no longer emit
  for this statement either.  As both of these constructs deal
  with variable numbers of rows, the
  `ResultProxy.inserted_primary_key` accessor does not
  apply.   Previously, there was a documentation note that one
  may prefer `inline=True` with INSERT..FROM SELECT as some databases
  don’t support returning and therefore can’t do “implicit” returning,
  but there’s no reason an INSERT…FROM SELECT needs implicit returning
  in any case.   Regular explicit [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) should
  be used to return variable numbers of result rows if inserted
  data is needed.
  References: [#3169](https://www.sqlalchemy.org/trac/ticket/3169)
- Custom dialects that implement [GenericTypeCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.GenericTypeCompiler) can
  now be constructed such that the visit methods receive an indication
  of the owning expression object, if any.  Any visit method that
  accepts keyword arguments (e.g. `**kw`) will in most cases
  receive a keyword argument `type_expression`, referring to the
  expression object that the type is contained within.  For columns
  in DDL, the dialect’s compiler class may need to alter its
  `get_column_specification()` method to support this as well.
  The `UserDefinedType.get_col_spec()` method will also receive
  `type_expression` if it provides `**kw` in its argument
  signature.
  References: [#3074](https://www.sqlalchemy.org/trac/ticket/3074)

### schema

- The DDL generation system of [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all)
  and [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all) has been enhanced to in most
  cases automatically handle the case of mutually dependent
  foreign key constraints; the need for the
  [ForeignKeyConstraint.use_alter](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) flag is greatly
  reduced.  The system also works for constraints which aren’t given
  a name up front; only in the case of DROP is a name required for
  at least one of the constraints involved in the cycle.
  See also
  [The use_alter flag on ForeignKeyConstraint is (usually) no longer needed](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-3282)
  References: [#3282](https://www.sqlalchemy.org/trac/ticket/3282)
- Added a new accessor [Table.foreign_key_constraints](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.foreign_key_constraints)
  to complement the [Table.foreign_keys](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.foreign_keys) collection,
  as well as [ForeignKeyConstraint.referred_table](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.referred_table).
- The [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) construct now supports naming
  conventions that include the token `%(column_0_name)s`; the
  constraint expression is scanned for columns.  Additionally,
  naming conventions for check constraints that don’t include the
  `%(constraint_name)s` token will now work for [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType)-
  generated constraints, such as those of [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) and
  [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum); this stopped working in 0.9.7 due to [#3067](https://www.sqlalchemy.org/trac/ticket/3067).
  See also
  [Naming CHECK Constraints](https://docs.sqlalchemy.org/en/20/core/constraints.html#naming-check-constraints)
  [Configuring Naming for Boolean, Enum, and other schema types](https://docs.sqlalchemy.org/en/20/core/constraints.html#naming-schematypes)
  References: [#3067](https://www.sqlalchemy.org/trac/ticket/3067), [#3299](https://www.sqlalchemy.org/trac/ticket/3299)

### postgresql

- Added support for the `CONCURRENTLY` keyword with PostgreSQL
  indexes, established using `postgresql_concurrently`.  Pull
  request courtesy Iuri de Silvio.
  See also
  [Indexes with CONCURRENTLY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-index-concurrently)
  This change is also **backported** to: 0.9.9
- Support is added for “sane multi row count” with the pg8000 driver,
  which applies mostly to when using versioning with the ORM.
  The feature is version-detected based on pg8000 1.9.14 or greater
  in use.  Pull request courtesy Tony Locke.
  This change is also **backported** to: 0.9.8
- Added kw argument `postgresql_regconfig` to the
  [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) operator, allows the “reg config” argument
  to be specified to the `to_tsquery()` function emitted.
  Pull request courtesy Jonathan Vanasco.
  This change is also **backported** to: 0.9.7
  References: [#3078](https://www.sqlalchemy.org/trac/ticket/3078)
- Added support for PostgreSQL JSONB via [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB).  Pull request
  courtesy Damian Dimmich.
  This change is also **backported** to: 0.9.7
- Added support for AUTOCOMMIT isolation level when using the pg8000
  DBAPI.  Pull request courtesy Tony Locke.
  This change is also **backported** to: 0.9.5
- Added a new flag [ARRAY.zero_indexes](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.params.zero_indexes) to the PostgreSQL
  [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) type.  When set to `True`, a value of one will be
  added to all array index values before passing to the database, allowing
  better interoperability between Python style zero-based indexes and
  PostgreSQL one-based indexes.  Pull request courtesy Alexey Terentev.
  This change is also **backported** to: 0.9.5
  References: [#2785](https://www.sqlalchemy.org/trac/ticket/2785)
- The PG8000 dialect now supports the
  [create_engine.encoding](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.encoding) parameter, by setting up
  the client encoding on the connection which is then intercepted
  by pg8000.  Pull request courtesy Tony Locke.
- Added support for PG8000’s native JSONB feature.  Pull request
  courtesy Tony Locke.
- Added support for the psycopg2cffi DBAPI on pypy.   Pull request
  courtesy shauns.
  See also
  [sqlalchemy.dialects.postgresql.psycopg2cffi](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2cffi)
  References: [#3052](https://www.sqlalchemy.org/trac/ticket/3052)
- Added support for the FILTER keyword as applied to aggregate
  functions, supported by PostgreSQL 9.4.   Pull request
  courtesy Ilja Everilä.
  See also
  [PostgreSQL FILTER keyword](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-gh134)
- Support has been added for reflection of materialized views
  and foreign tables, as well as support for materialized views
  within [Inspector.get_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names), and a new method
  [PGInspector.get_foreign_table_names()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_foreign_table_names) available on the
  PostgreSQL version of [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector).  Pull request courtesy
  Rodrigo Menezes.
  See also
  [PostgreSQL Dialect reflects Materialized Views, Foreign Tables](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#feature-2891)
  References: [#2891](https://www.sqlalchemy.org/trac/ticket/2891)
- Added support for PG table options TABLESPACE, ON COMMIT,
  WITH(OUT) OIDS, and INHERITS, when rendering DDL via
  the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct.   Pull request courtesy
  malikdiarra.
  See also
  [PostgreSQL Table Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-table-options)
  References: [#2051](https://www.sqlalchemy.org/trac/ticket/2051)
- Added new method [PGInspector.get_enums()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.base.PGInspector.get_enums), when using the
  inspector for PostgreSQL will provide a list of ENUM types.
  Pull request courtesy Ilya Pekelny.
- Added the `hashable=False` flag to the PG [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE) type, which
  is needed to allow the ORM to skip over trying to “hash” an ORM-mapped
  HSTORE column when requesting it in a mixed column/entity list.
  Patch courtesy Gunnlaugur Þór Briem.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3053](https://www.sqlalchemy.org/trac/ticket/3053)
- Added a new “disconnect” message “connection has been closed unexpectedly”.
  This appears to be related to newer versions of SSL.
  Pull request courtesy Antti Haapala.
  This change is also **backported** to: 0.9.5, 0.8.7
- Repaired support for PostgreSQL UUID types in conjunction with
  the ARRAY type when using psycopg2.  The psycopg2 dialect now
  employs use of the psycopg2.extras.register_uuid() hook
  so that UUID values are always passed to/from the DBAPI as
  UUID() objects.   The [UUID.as_uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID.params.as_uuid) flag is still
  honored, except with psycopg2 we need to convert returned
  UUID objects back into strings when this is disabled.
  This change is also **backported** to: 0.9.9
  References: [#2940](https://www.sqlalchemy.org/trac/ticket/2940)
- Added support for the `postgresql.JSONB` datatype when
  using psycopg2 2.5.4 or greater, which features native conversion
  of JSONB data so that SQLAlchemy’s converters must be disabled;
  additionally, the newly added psycopg2 extension
  `extras.register_default_jsonb` is used to establish a JSON
  deserializer passed to the dialect via the `json_deserializer`
  argument.  Also repaired the PostgreSQL integration tests which
  weren’t actually round-tripping the JSONB type as opposed to the
  JSON type.  Pull request courtesy Mateusz Susik.
  This change is also **backported** to: 0.9.9
- Repaired the use of the “array_oid” flag when registering the
  HSTORE type with older psycopg2 versions < 2.4.3, which does not
  support this flag, as well as use of the native json serializer
  hook “register_default_json” with user-defined `json_deserializer`
  on psycopg2 versions < 2.5, which does not include native json.
  This change is also **backported** to: 0.9.9
- Fixed bug where PostgreSQL dialect would fail to render an
  expression in an [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) that did not correspond directly
  to a table-bound column; typically when a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct
  was one of the expressions within the index; or could misinterpret the
  list of expressions if one or more of them were such an expression.
  This change is also **backported** to: 0.9.9
  References: [#3174](https://www.sqlalchemy.org/trac/ticket/3174)
- A revisit to this issue first patched in 0.9.5, apparently
  psycopg2’s `.closed` accessor is not as reliable as we assumed,
  so we have added an explicit check for the exception messages
  “SSL SYSCALL error: Bad file descriptor” and
  “SSL SYSCALL error: EOF detected” when detecting an
  is-disconnect scenario.   We will continue to consult psycopg2’s
  connection.closed as a first check.
  This change is also **backported** to: 0.9.8
  References: [#3021](https://www.sqlalchemy.org/trac/ticket/3021)
- Fixed bug where PostgreSQL JSON type was not able to persist or
  otherwise render a SQL NULL column value, rather than a JSON-encoded
  `'null'`.  To support this case, changes are as follows:
  - The value [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) can now be specified, which will always
    result in a NULL value resulting in the statement.
  - A new parameter [JSON.none_as_null](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON.params.none_as_null) is added, which
    when True indicates that the Python `None` value should be
    persisted as SQL NULL, rather than JSON-encoded `'null'`.
  Retrieval of NULL as None is also repaired for DBAPIs other than
  psycopg2, namely pg8000.
  This change is also **backported** to: 0.9.8
  References: [#3159](https://www.sqlalchemy.org/trac/ticket/3159)
- The exception wrapping system for DBAPI errors can now accommodate
  non-standard DBAPI exceptions, such as the psycopg2
  TransactionRollbackError.  These exceptions will now be raised
  using the closest available subclass in `sqlalchemy.exc`, in the
  case of TransactionRollbackError, `sqlalchemy.exc.OperationalError`.
  This change is also **backported** to: 0.9.8
  References: [#3075](https://www.sqlalchemy.org/trac/ticket/3075)
- Fixed bug in [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) object where comparison
  to a plain Python list would fail to use the correct array constructor.
  Pull request courtesy Andrew.
  This change is also **backported** to: 0.9.8
  References: [#3141](https://www.sqlalchemy.org/trac/ticket/3141)
- Added a supported [FunctionElement.alias()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.alias) method to functions,
  e.g. the `func` construct.  Previously, behavior for this method
  was undefined.  The current behavior mimics that of pre-0.9.4,
  which is that the function is turned into a single-column FROM
  clause with the given alias name, where the column itself is
  anonymously named.
  This change is also **backported** to: 0.9.8
  References: [#3137](https://www.sqlalchemy.org/trac/ticket/3137)
- Fixed bug introduced in 0.9.5 by new pg8000 isolation level feature
  where engine-level isolation level parameter would raise an error
  on connect.
  This change is also **backported** to: 0.9.7
  References: [#3134](https://www.sqlalchemy.org/trac/ticket/3134)
- The psycopg2 `.closed` accessor is now consulted when determining
  if an exception is a “disconnect” error; ideally, this should remove
  the need for any other inspection of the exception message to detect
  disconnect, however we will leave those existing messages in place
  as a fallback.   This should be able to handle newer cases like
  “SSL EOF” conditions.  Pull request courtesy Dirk Mueller.
  This change is also **backported** to: 0.9.5
  References: [#3021](https://www.sqlalchemy.org/trac/ticket/3021)
- The PostgreSQL [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) type will emit a
  DROP TYPE instruction when a plain `table.drop()` is called,
  assuming the object is not associated directly with a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object.   In order to accommodate the use case of
  an enumerated type shared between multiple tables, the type should
  be associated directly with the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object; in this
  case the type will only be created at the metadata level, or if
  created directly.  The rules for create/drop of
  PostgreSQL enumerated types have been highly reworked in general.
  See also
  [Overhaul of ENUM type create/drop rules](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3319)
  References: [#3319](https://www.sqlalchemy.org/trac/ticket/3319)
- The `PGDialect.has_table()` method will now query against
  `pg_catalog.pg_table_is_visible(c.oid)`, rather than testing
  for an exact schema match, when the schema name is None; this
  so that the method will also illustrate that temporary tables
  are present.  Note that this is a behavioral change, as PostgreSQL
  allows a non-temporary table to silently overwrite an existing
  temporary table of the same name, so this changes the behavior
  of `checkfirst` in that unusual scenario.
  See also
  [PostgreSQL has_table() now works for temporary tables](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3264)
  References: [#3264](https://www.sqlalchemy.org/trac/ticket/3264)
- Added a new type [OID](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.OID) to the PostgreSQL dialect.
  While “oid” is generally a private type within PG that is not exposed
  in modern versions, there are some PG use cases such as large object
  support where these types might be exposed, as well as within some
  user-reported schema reflection use cases.
  This change is also **backported** to: 0.9.5
  References: [#3002](https://www.sqlalchemy.org/trac/ticket/3002)

### mysql

- The MySQL dialect now renders TIMESTAMP with NULL / NOT NULL in
  all cases, so that MySQL 5.6.6 with the
  `explicit_defaults_for_timestamp` flag enabled will
  will allow TIMESTAMP to continue to work as expected when
  `nullable=False`.  Existing applications are unaffected as
  SQLAlchemy has always emitted NULL for a TIMESTAMP column that
  is `nullable=True`.
  See also
  [MySQL TIMESTAMP Type now renders NULL / NOT NULL in all cases](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3155)
  [TIMESTAMP Columns and NULL](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-timestamp-null)
  References: [#3155](https://www.sqlalchemy.org/trac/ticket/3155)
- Updated the “supports_unicode_statements” flag to True for MySQLdb
  and Pymysql under Python 2.   This refers to the SQL statements
  themselves, not the parameters, and affects issues such as table
  and column names using non-ASCII characters.   These drivers both
  appear to support Python 2 Unicode objects without issue in modern
  versions.
  References: [#3121](https://www.sqlalchemy.org/trac/ticket/3121)
- The `gaerdbms` dialect is no longer necessary, and emits a
  deprecation warning.  Google now recommends using the MySQLdb
  dialect directly.
  This change is also **backported** to: 0.9.9
  References: [#3275](https://www.sqlalchemy.org/trac/ticket/3275)
- MySQL error 2014 “commands out of sync” appears to be raised as a
  ProgrammingError, not OperationalError, in modern MySQL-Python versions;
  all MySQL error codes that are tested for “is disconnect” are now
  checked within OperationalError and ProgrammingError regardless.
  This change is also **backported** to: 0.9.7, 0.8.7
  References: [#3101](https://www.sqlalchemy.org/trac/ticket/3101)
- Fixed bug where column names added to `mysql_length` parameter
  on an index needed to have the same quoting for quoted names in
  order to be recognized.  The fix makes the quotes optional but
  also provides the old behavior for backwards compatibility with those
  using the workaround.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3085](https://www.sqlalchemy.org/trac/ticket/3085)
- Added support for reflecting tables where an index includes
  KEY_BLOCK_SIZE using an equal sign.  Pull request courtesy
  Sean McGivern.
  This change is also **backported** to: 0.9.5, 0.8.7
- Added a version check to the MySQLdb dialect surrounding the
  check for ‘utf8_bin’ collation, as this fails on MySQL server < 5.0.
  This change is also **backported** to: 0.9.9
  References: [#3274](https://www.sqlalchemy.org/trac/ticket/3274)
- Mysqlconnector as of version 2.0, probably as a side effect of
  the  python 3 merge, now does not expect percent signs (e.g.
  as used as the modulus operator and others) to be doubled,
  even when using the “pyformat” bound parameter format (this
  change is not documented by Mysqlconnector).  The dialect now
  checks for py2k and for mysqlconnector less than version 2.0
  when detecting if the modulus operator should be rendered as
  `%%` or `%`.
  This change is also **backported** to: 0.9.8
- Unicode SQL is now passed for MySQLconnector version 2.0 and above;
  for Py2k and MySQL < 2.0, strings are encoded.
  This change is also **backported** to: 0.9.8
- The MySQL dialect now supports CAST on types that are constructed
  as [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) objects.
- A warning is emitted when [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) is used with the MySQL
  dialect on a type where MySQL does not support CAST; MySQL only
  supports CAST on a subset of datatypes.   SQLAlchemy has for a long
  time just omitted the CAST for unsupported types in the case of
  MySQL.  While we don’t want to change this now, we emit a warning
  to show that it’s taken place.   A warning is also emitted when
  a CAST is used with an older MySQL version (< 4) that doesn’t support
  CAST at all, it’s skipped in this case as well.
  References: [#3237](https://www.sqlalchemy.org/trac/ticket/3237)
- The [SET](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.SET) type has been overhauled to no longer
  assume that the empty string, or a set with a single empty string
  value, is in fact a set with a single empty string; instead, this
  is by default treated as the empty set.  In order to handle persistence
  of a [SET](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.SET) that actually wants to include the blank
  value `''` as a legitimate value, a new bitwise operational mode
  is added which is enabled by the
  [SET.retrieve_as_bitwise](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.SET.params.retrieve_as_bitwise) flag, which will persist
  and retrieve values unambiguously using their bitflag positioning.
  Storage and retrieval of unicode values for driver configurations
  that aren’t converting unicode natively is also repaired.
  See also
  [MySQL SET Type Overhauled to support empty sets, unicode, blank value handling](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3283)
  References: [#3283](https://www.sqlalchemy.org/trac/ticket/3283)
- The [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) operator is now handled such that the
  return type is not strictly assumed to be boolean; it now
  returns a [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) subclass called [MatchType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.MatchType).
  The type will still produce boolean behavior when used in Python
  expressions, however the dialect can override its behavior at
  result time.  In the case of MySQL, while the MATCH operator
  is typically used in a boolean context within an expression,
  if one actually queries for the value of a match expression, a
  floating point value is returned; this value is not compatible
  with SQLAlchemy’s C-based boolean processor, so MySQL’s result-set
  behavior now follows that of the [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) type.
  A new operator object `notmatch_op` is also added to better allow
  dialects to define the negation of a match operation.
  See also
  [The match() operator now returns an agnostic MatchType compatible with MySQL’s floating point return value](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3263)
  References: [#3263](https://www.sqlalchemy.org/trac/ticket/3263)
- MySQL boolean symbols “true”, “false” work again.  0.9’s change
  in [#2682](https://www.sqlalchemy.org/trac/ticket/2682) disallowed the MySQL dialect from making use of the
  “true” and “false” symbols in the context of “IS” / “IS NOT”, but
  MySQL supports this syntax even though it has no boolean type.
  MySQL remains “non native boolean”, but the [true()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.true)
  and [false()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.false) symbols again produce the
  keywords “true” and “false”, so that an expression like
  `column.is_(true())` again works on MySQL.
  See also
  [MySQL boolean symbols “true”, “false” work again](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#bug-3186)
  References: [#3186](https://www.sqlalchemy.org/trac/ticket/3186)
- The MySQL dialect will now disable `ConnectionEvents.handle_error()`
  events from firing for those statements which it uses internally
  to detect if a table exists or not.   This is achieved using an
  execution option `skip_user_error_events` that disables the handle
  error event for the scope of that execution.   In this way, user code
  that rewrites exceptions doesn’t need to worry about the MySQL
  dialect or other dialects that occasionally need to catch
  SQLAlchemy specific exceptions.
- Changed the default value of “raise_on_warnings” to False for
  MySQLconnector.  This was set at True for some reason.  The “buffered”
  flag unfortunately must stay at True as MySQLconnector does not allow
  a cursor to be closed unless all results are fully fetched.
  References: [#2515](https://www.sqlalchemy.org/trac/ticket/2515)

### sqlite

- Added support for partial indexes (e.g. with a WHERE clause) on
  SQLite.  Pull request courtesy Kai Groner.
  See also
  [Partial Indexes](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-partial-index)
  This change is also **backported** to: 0.9.9
- Added a new SQLite backend for the SQLCipher backend.  This backend
  provides for encrypted SQLite databases using the pysqlcipher Python
  driver, which is very similar to the pysqlite driver.
  See also
  [pysqlcipher](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlcipher)
  This change is also **backported** to: 0.9.9
- When selecting from a UNION using an attached database file,
  the pysqlite driver reports column names in cursor.description
  as ‘dbname.tablename.colname’, instead of ‘tablename.colname’ as
  it normally does for a UNION (note that it’s supposed to just be
  ‘colname’ for both, but we work around it).  The column translation
  logic here has been adjusted to retrieve the rightmost token, rather
  than the second token, so it works in both cases.   Workaround
  courtesy Tony Roberts.
  This change is also **backported** to: 0.9.8
  References: [#3211](https://www.sqlalchemy.org/trac/ticket/3211)
- Fixed a SQLite join rewriting issue where a subquery that is embedded
  as a scalar subquery such as within an IN would receive inappropriate
  substitutions from the enclosing query, if the same table were present
  inside the subquery as were in the enclosing query such as in a
  joined inheritance scenario.
  This change is also **backported** to: 0.9.7
  References: [#3130](https://www.sqlalchemy.org/trac/ticket/3130)
- UNIQUE and FOREIGN KEY constraints are now fully reflected on
  SQLite both with and without names.  Previously, foreign key
  names were ignored and unnamed unique constraints were skipped.
  Thanks to Jon Nelson for assistance with this.
  References: [#3244](https://www.sqlalchemy.org/trac/ticket/3244), [#3261](https://www.sqlalchemy.org/trac/ticket/3261)
- The SQLite dialect, when using the [DATE](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.DATE),
  [TIME](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.TIME),
  or [DATETIME](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.DATETIME) types, and given a `storage_format` that
  only renders numbers, will render the types in DDL as
  `DATE_CHAR`, `TIME_CHAR`, and `DATETIME_CHAR`, so that despite the
  lack of alpha characters in the values, the column will still
  deliver the “text affinity”.  Normally this is not needed, as the
  textual values within the default storage formats already
  imply text.
  See also
  [Date and Time Types](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-datetime)
  References: [#3257](https://www.sqlalchemy.org/trac/ticket/3257)
- SQLite now supports reflection of unique constraints from
  temp tables; previously, this would fail with a TypeError.
  Pull request courtesy Johannes Erdfelt.
  See also
  [SQLite/Oracle have distinct methods for temporary table/view name reporting](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3204) - changes regarding SQLite temporary
  table and view reflection.
  References: [#3203](https://www.sqlalchemy.org/trac/ticket/3203)
- Added [Inspector.get_temp_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_table_names) and
  [Inspector.get_temp_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_temp_view_names); currently, only the
  SQLite and Oracle dialects support these methods.  The return of
  temporary table and view names has been **removed** from SQLite and
  Oracle’s version of [Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names) and
  [Inspector.get_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names); other database backends cannot
  support this information (such as MySQL), and the scope of operation
  is different in that the tables can be local to a session and
  typically aren’t supported in remote schemas.
  See also
  [SQLite/Oracle have distinct methods for temporary table/view name reporting](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3204)
  References: [#3204](https://www.sqlalchemy.org/trac/ticket/3204)

### mssql

- Enabled “multivalues insert” for SQL Server 2008.  Pull request
  courtesy Albert Cervin.  Also expanded the checks for “IDENTITY INSERT”
  mode to include when the identity key is present in the
  VALUEs clause of the statement.
  This change is also **backported** to: 0.9.7
- SQL Server 2012 now recommends VARCHAR(max), NVARCHAR(max),
  VARBINARY(max) for large text/binary types.  The MSSQL dialect will
  now respect this based on version detection, as well as the new
  `deprecate_large_types` flag.
  See also
  [Large Text/Binary Type Deprecation](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-large-type-deprecation)
  References: [#3039](https://www.sqlalchemy.org/trac/ticket/3039)
- The hostname-based connection format for SQL Server when using
  pyodbc will no longer specify a default “driver name”, and a warning
  is emitted if this is missing.  The optimal driver name for SQL Server
  changes frequently and is per-platform, so hostname based connections
  need to specify this.  DSN-based connections are preferred.
  See also
  [PyODBC driver name is required with hostname-based SQL Server connections](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3182)
  References: [#3182](https://www.sqlalchemy.org/trac/ticket/3182)
- Added statement encoding to the “SET IDENTITY_INSERT”
  statements which operate when an explicit INSERT is being
  interjected into an IDENTITY column, to support non-ascii table
  identifiers on drivers such as pyodbc + unix + py2k that don’t
  support unicode statements.
  This change is also **backported** to: 0.9.7, 0.8.7
- In the SQL Server pyodbc dialect, repaired the implementation
  for the `description_encoding` dialect parameter, which when
  not explicitly set was preventing  cursor.description from
  being parsed correctly in the case of result sets that
  contained names in alternate encodings.  This parameter
  shouldn’t be needed going forward.
  This change is also **backported** to: 0.9.7, 0.8.7
  References: [#3091](https://www.sqlalchemy.org/trac/ticket/3091)
- Fixed the version string detection in the pymssql dialect to
  work with Microsoft SQL Azure, which changes the word “SQL Server”
  to “SQL Azure”.
  This change is also **backported** to: 0.9.8
  References: [#3151](https://www.sqlalchemy.org/trac/ticket/3151)
- Revised the query used to determine the current default schema name
  to use the `database_principal_id()` function in conjunction with
  the `sys.database_principals` view so that we can determine
  the default schema independently of the type of login in progress
  (e.g., SQL Server, Windows, etc).
  This change is also **backported** to: 0.9.5
  References: [#3025](https://www.sqlalchemy.org/trac/ticket/3025)

### oracle

- Added support for cx_oracle connections to a specific service
  name, as opposed to a tns name, by passing `?service_name=<name>`
  to the URL.  Pull request courtesy Sławomir Ehlert.
- New Oracle DDL features for tables, indexes: COMPRESS, BITMAP.
  Patch courtesy Gabor Gombas.
- Added support for CTEs under Oracle.  This includes some tweaks
  to the aliasing syntax, as well as a new CTE feature
  `CTE.suffix_with()`, which is useful for adding in special
  Oracle-specific directives to the CTE.
  See also
  [Improved support for CTEs in Oracle](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-3220)
  References: [#3220](https://www.sqlalchemy.org/trac/ticket/3220)
- Added support for the Oracle table option ON COMMIT.
- Fixed long-standing bug in Oracle dialect where bound parameter
  names that started with numbers would not be quoted, as Oracle
  doesn’t like numerics in bound parameter names.
  This change is also **backported** to: 0.9.8
  References: [#2138](https://www.sqlalchemy.org/trac/ticket/2138)
- Fixed bug in oracle dialect test suite where in one test,
  ‘username’ was assumed to be in the database URL, even though
  this might not be the case.
  This change is also **backported** to: 0.9.7
  References: [#3128](https://www.sqlalchemy.org/trac/ticket/3128)
- An alias name will be properly quoted when referred to using the
  `%(name)s` token inside the [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) method.
  Previously, the Oracle backend hadn’t implemented this quoting.

### tests

- Fixed bug where “python setup.py test” wasn’t calling into
  distutils appropriately, and errors would be emitted at the end
  of the test suite.
  This change is also **backported** to: 0.9.7
- Corrected for some deprecation warnings involving the `imp`
  module and Python 3.3 or greater, when running tests.  Pull
  request courtesy Matt Chisholm.
  This change is also **backported** to: 0.9.5
  References: [#2830](https://www.sqlalchemy.org/trac/ticket/2830)

### misc

- Added a new extension suite [sqlalchemy.ext.baked](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html#module-sqlalchemy.ext.baked).  This
  simple but unusual system allows for a dramatic savings in Python
  overhead for the construction and processing of orm [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  objects, from query construction up through rendering of a string
  SQL statement.
  See also
  [Baked Queries](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html)
  References: [#3054](https://www.sqlalchemy.org/trac/ticket/3054)
- The [sqlalchemy.ext.automap](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#module-sqlalchemy.ext.automap) extension will now set
  `cascade="all, delete-orphan"` automatically on a one-to-many
  relationship/backref where the foreign key is detected as containing
  one or more non-nullable columns.  This argument is present in the
  keywords passed to [generate_relationship()](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.generate_relationship) in this
  case and can still be overridden.  Additionally, if the
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) specifies `ondelete="CASCADE"`
  for a non-nullable or `ondelete="SET NULL"` for a nullable set
  of columns, the argument `passive_deletes=True` is also added to the
  relationship.  Note that not all backends support reflection of
  ondelete, but backends that do include PostgreSQL and MySQL.
  References: [#3210](https://www.sqlalchemy.org/trac/ticket/3210)
- The `__mapper_args__` dictionary is copied from a declarative
  mixin or abstract class when accessed, so that modifications made
  to this dictionary by declarative itself won’t conflict with that
  of other mappings.  The dictionary is modified regarding the
  `version_id_col` and `polymorphic_on` arguments, replacing the
  column within with the one that is officially mapped to the local
  class/table.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3062](https://www.sqlalchemy.org/trac/ticket/3062)
- Fixed bug in mutable extension where [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) did not
  report change events for the `setdefault()` dictionary operation.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3051](https://www.sqlalchemy.org/trac/ticket/3051), [#3093](https://www.sqlalchemy.org/trac/ticket/3093)
- Fixed bug where [MutableDict.setdefault()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict.setdefault) didn’t return the
  existing or new value (this bug was not released in any 0.8 version).
  Pull request courtesy Thomas Hervé.
  This change is also **backported** to: 0.9.5, 0.8.7
  References: [#3051](https://www.sqlalchemy.org/trac/ticket/3051), [#3093](https://www.sqlalchemy.org/trac/ticket/3093)
- Fixed bug where the association proxy list class would not interpret
  slices correctly under Py3K.  Pull request courtesy
  Gilles Dartiguelongue.
  This change is also **backported** to: 0.9.9
- Fixed an unlikely race condition observed in some exotic end-user
  setups, where the attempt to check for “duplicate class name” in
  declarative would hit upon a not-totally-cleaned-up weak reference
  related to some other class being removed; the check here now ensures
  the weakref still references an object before calling upon it further.
  This change is also **backported** to: 0.9.8
  References: [#3208](https://www.sqlalchemy.org/trac/ticket/3208)
- Fixed bug in ordering list where the order of items would be
  thrown off during a collection replace event, if the
  reorder_on_append flag were set to True.  The fix ensures that the
  ordering list only impacts the list that is explicitly associated
  with the object.
  This change is also **backported** to: 0.9.8
  References: [#3191](https://www.sqlalchemy.org/trac/ticket/3191)
- Fixed bug where [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict)
  failed to implement the `update()` dictionary method, thus
  not catching changes. Pull request courtesy Matt Chisholm.
  This change is also **backported** to: 0.9.8
- Fixed bug where a custom subclass of [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict)
  would not show up in a “coerce” operation, and would instead
  return a plain [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict).  Pull request
  courtesy Matt Chisholm.
  This change is also **backported** to: 0.9.8
- Fixed bug in connection pool logging where the “connection checked out”
  debug logging message would not emit if the logging were set up using
  `logging.setLevel()`, rather than using the `echo_pool` flag.
  Tests to assert this logging have been added.  This is a
  regression that was introduced in 0.9.0.
  This change is also **backported** to: 0.9.8
  References: [#3168](https://www.sqlalchemy.org/trac/ticket/3168)
- Fixed bug when the declarative `__abstract__` flag was not being
  distinguished for when it was actually the value `False`.
  The `__abstract__` flag needs to actually evaluate to a True
  value at the level being tested.
  This change is also **backported** to: 0.9.7
  References: [#3097](https://www.sqlalchemy.org/trac/ticket/3097)
- In public test suite, changed to use of `String(40)` from
  less-supported `Text` in `StringTest.test_literal_backslashes`.
  Pullreq courtesy Jan.
  This change is also **backported** to: 0.9.5
- The Drizzle dialect has been removed from the Core; it is now
  available as [sqlalchemy-drizzle](https://bitbucket.org/zzzeek/sqlalchemy-drizzle),
  an independent, third party dialect.  The dialect is still based
  almost entirely off of the MySQL dialect present in SQLAlchemy.
  See also
  [Drizzle Dialect is now an External Dialect](https://docs.sqlalchemy.org/en/20/changelog/migration_10.html#change-2984)
