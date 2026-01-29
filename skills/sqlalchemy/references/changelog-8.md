# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 0.9 Changelog

## 0.9.10

Released: July 22, 2015

### orm

- Added a new entry `"entity"` to the dictionaries returned by
  [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions).  This refers to the primary ORM
  mapped class or aliased class that is referred to by the expression.
  Compared to the existing entry for `"type"`, it will always be
  a mapped entity, even if extracted from a column expression, or
  None if the given expression is a pure core expression.
  See also [#3403](https://www.sqlalchemy.org/trac/ticket/3403) which repaired a regression in this feature
  which was unreleased in 0.9.10 but was released in the 1.0 version.
  References: [#3320](https://www.sqlalchemy.org/trac/ticket/3320)
- [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) doesn’t support joins, subselects, or special
  FROM clauses when using the [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) or
  [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete) methods; instead of silently ignoring these
  fields if methods like [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) or
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) has been called, a warning is emitted.
  As of 1.0.0b5 this will raise an error.
  References: [#3349](https://www.sqlalchemy.org/trac/ticket/3349)
- Fixed bug where the state tracking within multiple, nested
  [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) operations would fail to propagate
  the “dirty” flag for an object that had been updated within
  the inner savepoint, such that if the enclosing savepoint were
  rolled back, the object would not be part of the state that was
  expired and therefore reverted to its database state.
  References: [#3352](https://www.sqlalchemy.org/trac/ticket/3352)

### engine

- Added the string value `"none"` to those accepted by the
  [Pool.reset_on_return](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool.params.reset_on_return) parameter as a synonym for `None`,
  so that string values can be used for all settings, allowing
  utilities like [engine_from_config()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine_from_config) to be usable without
  issue.
  References: [#3375](https://www.sqlalchemy.org/trac/ticket/3375)

### sql

- Added official support for a CTE used by the SELECT present
  inside of [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select).  This behavior worked
  accidentally up until 0.9.9, when it no longer worked due to
  unrelated changes as part of [#3248](https://www.sqlalchemy.org/trac/ticket/3248).   Note that this
  is the rendering of the WITH clause after the INSERT, before the
  SELECT; the full functionality of CTEs rendered at the top
  level of INSERT, UPDATE, DELETE is a new feature targeted for a
  later release.
  References: [#3418](https://www.sqlalchemy.org/trac/ticket/3418)
- Fixed issue where a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object that used a naming
  convention would not properly work with pickle.  The attribute was
  skipped leading to inconsistencies and failures if the unpickled
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object were used to base additional tables
  from.
  References: [#3362](https://www.sqlalchemy.org/trac/ticket/3362)

### postgresql

- Fixed a long-standing bug where the [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) type as used
  with the psycopg2 dialect in conjunction with non-ascii values
  and `native_enum=False` would fail to decode return results properly.
  This stemmed from when the PG [ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) type used
  to be a standalone type without a “non native” option.
  References: [#3354](https://www.sqlalchemy.org/trac/ticket/3354)

### mysql

- Fixed unicode support for PyMySQL when using an “executemany”
  operation with unicode parameters.  SQLAlchemy now passes both
  the statement as well as the bound parameters as unicode
  objects, as PyMySQL generally uses string interpolation
  internally to produce the final statement, and in the case of
  executemany does the “encode” step only on the final statement.
  References: [#3337](https://www.sqlalchemy.org/trac/ticket/3337)
- Fixed the [BIT](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.BIT) type on Py3K which was not using the
  `ord()` function correctly.  Pull request courtesy David Marin.
  References: [#3333](https://www.sqlalchemy.org/trac/ticket/3333)

### sqlite

- Fixed bug in SQLite dialect where reflection of UNIQUE constraints
  that included non-alphabetic characters in the names, like dots or
  spaces, would not be reflected with their name.
  References: [#3495](https://www.sqlalchemy.org/trac/ticket/3495)

### tests

- Fixed an import that prevented “pypy setup.py test” from working
  correctly.
  References: [#3406](https://www.sqlalchemy.org/trac/ticket/3406)

### misc

- Fixed bug where when using extended attribute instrumentation system,
  the correct exception would not be raised when [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper)
  were called with an invalid input that also happened to not
  be weak referenceable, such as an integer.
  References: [#3408](https://www.sqlalchemy.org/trac/ticket/3408)
- Fixed regression from 0.9.9 where the [as_declarative()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.as_declarative)
  symbol was removed from the `sqlalchemy.ext.declarative`
  namespace.
  References: [#3324](https://www.sqlalchemy.org/trac/ticket/3324)

## 0.9.9

Released: March 10, 2015

### orm

- Added new parameter [Session.connection.execution_options](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection.params.execution_options)
  which may be used to set up execution options on a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
  when it is first checked out, before the transaction has begun.
  This is used to set up options such as isolation level on the
  connection before the transaction starts.
  See also
  [Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-transaction-isolation) - new documentation section
  detailing best practices for setting transaction isolation with
  sessions.
  References: [#3296](https://www.sqlalchemy.org/trac/ticket/3296)
- Added new method [Session.invalidate()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.invalidate), functions similarly
  to [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close), except also calls
  [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate)
  on all connections, guaranteeing that they will not be returned to
  the connection pool.  This is useful in situations e.g. dealing
  with gevent timeouts when it is not safe to use the connection further,
  even for rollbacks.
- Fixed bugs in ORM object comparisons where comparison of
  many-to-one `!= None` would fail if the source were an aliased
  class, or if the query needed to apply special aliasing to the
  expression due to aliased joins or polymorphic querying; also fixed
  bug in the case where comparing a many-to-one to an object state
  would fail if the query needed to apply special aliasing
  due to aliased joins or polymorphic querying.
  References: [#3310](https://www.sqlalchemy.org/trac/ticket/3310)
- Fixed bug where internal assertion would fail in the case where
  an `after_rollback()` handler for a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) incorrectly
  adds state to that [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) within the handler, and the task
  to warn and remove this state (established by [#2389](https://www.sqlalchemy.org/trac/ticket/2389)) attempts
  to proceed.
  References: [#3309](https://www.sqlalchemy.org/trac/ticket/3309)
- Fixed bug where TypeError raised when [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) called
  with unknown kw arguments would raise its own TypeError due
  to broken formatting.  Pull request courtesy Malthe Borch.
- Fixed bug in lazy loading SQL construction whereby a complex
  primaryjoin that referred to the same “local” column multiple
  times in the “column that points to itself” style of self-referential
  join would not be substituted in all cases.   The logic to determine
  substitutions here has been reworked to be more open-ended.
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
  References: [#3287](https://www.sqlalchemy.org/trac/ticket/3287)
- Fixed bug where if an exception were thrown at the start of a
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) before it fetched results, particularly when
  row processors can’t be formed, the cursor would stay open with
  results pending and not actually be closed.  This is typically only
  an issue on an interpreter like PyPy where the cursor isn’t
  immediately GC’ed, and can in some circumstances lead to transactions/
  locks being open longer than is desirable.
  References: [#3285](https://www.sqlalchemy.org/trac/ticket/3285)
- Fixed a leak which would occur in the unsupported and highly
  non-recommended use case of replacing a relationship on a fixed
  mapped class many times, referring to an arbitrarily growing number of
  target mappers.  A warning is emitted when the old relationship is
  replaced, however if the mapping were already used for querying, the
  old relationship would still be referenced within some registries.
  References: [#3251](https://www.sqlalchemy.org/trac/ticket/3251)
- Fixed bug regarding expression mutations which could express
  itself as a “Could not locate column” error when using
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) to  select from multiple, anonymous column
  entities when querying against SQLite, as a side effect of the
  “join rewriting” feature used by the SQLite dialect.
  References: [#3241](https://www.sqlalchemy.org/trac/ticket/3241)
- Fixed bug where the ON clause for [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join),
  and [Query.outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.outerjoin) to a single-inheritance subclass
  using `of_type()` would not render the “single table criteria” in
  the ON clause if the `from_joinpoint=True` flag were set.
  References: [#3232](https://www.sqlalchemy.org/trac/ticket/3232)

### examples

- Updated the [Versioning with a History Table](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioned-history) example such that
  mapped columns are re-mapped to
  match column names as well as grouping of columns; in particular,
  this allows columns that are explicitly grouped in a same-column-named
  joined inheritance scenario to be mapped in the same way in the
  history mappings, avoiding warnings added in the 0.9 series
  regarding this pattern and allowing the same view of attribute
  keys.
- Fixed a bug in the examples/generic_associations/discriminator_on_association.py
  example, where the subclasses of AddressAssociation were not being
  mapped as “single table inheritance”, leading to problems when trying
  to use the mappings further.

### engine

- Added new user-space accessors for viewing transaction isolation
  levels; [Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level),
  [Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level).
- Fixed bug in [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and pool where the
  [Connection.invalidate()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.invalidate) method, or an invalidation due
  to a database disconnect, would fail if the
  `isolation_level` parameter had been used with
  [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options); the “finalizer” that resets
  the isolation level would be called on the no longer opened connection.
  References: [#3302](https://www.sqlalchemy.org/trac/ticket/3302)
- A warning is emitted if the `isolation_level` parameter is used
  with [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options) when a [Transaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Transaction)
  is in play; DBAPIs and/or SQLAlchemy dialects such as psycopg2,
  MySQLdb may implicitly rollback or commit the transaction, or
  not change the setting til next transaction, so this is never safe.
  References: [#3296](https://www.sqlalchemy.org/trac/ticket/3296)

### sql

- Added the `native_enum` flag to the `__repr__()` output
  of [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), which is mostly important when using it with
  Alembic autogenerate.  Pull request courtesy Dimitris Theodorou.
- Fixed bug where using a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) that implemented
  a type that was also a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) would fail with
  Python’s “Cannot create a consistent method resolution order (MRO)”
  error, when any kind of SQL comparison expression were used against
  an object using this type.
  References: [#3278](https://www.sqlalchemy.org/trac/ticket/3278)
- Fixed issue where the columns from a SELECT embedded in an
  INSERT, either through the values clause or as a “from select”,
  would pollute the column types used in the result set produced by
  the RETURNING clause when columns from both statements shared the
  same name, leading to potential errors or mis-adaptation when
  retrieving the returning rows.
  References: [#3248](https://www.sqlalchemy.org/trac/ticket/3248)

### schema

- Fixed bug in 0.9’s foreign key setup system, such that
  the logic used to link a [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) to its parent could fail
  when the foreign key used “link_to_name=True” in conjunction with
  a target [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that would not receive its parent column until
  later, such as within a reflection + “useexisting” scenario,
  if the target column in fact had a key value different from its name,
  as would occur in reflection if column reflect events were used to
  alter the .key of reflected [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects so that the
  link_to_name becomes significant.  Also repaired support for column
  type via FK transmission in a similar way when target columns had a
  different key and were referenced using link_to_name.
  References: [#1765](https://www.sqlalchemy.org/trac/ticket/1765), [#3298](https://www.sqlalchemy.org/trac/ticket/3298)

### postgresql

- Added support for the `CONCURRENTLY` keyword with PostgreSQL
  indexes, established using `postgresql_concurrently`.  Pull
  request courtesy Iuri de Silvio.
  See also
  [Indexes with CONCURRENTLY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-index-concurrently)
- Repaired support for PostgreSQL UUID types in conjunction with
  the ARRAY type when using psycopg2.  The psycopg2 dialect now
  employs use of the psycopg2.extras.register_uuid() hook
  so that UUID values are always passed to/from the DBAPI as
  UUID() objects.   The [UUID.as_uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID.params.as_uuid) flag is still
  honored, except with psycopg2 we need to convert returned
  UUID objects back into strings when this is disabled.
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
- Repaired the use of the “array_oid” flag when registering the
  HSTORE type with older psycopg2 versions < 2.4.3, which does not
  support this flag, as well as use of the native json serializer
  hook “register_default_json” with user-defined `json_deserializer`
  on psycopg2 versions < 2.5, which does not include native json.
- Fixed bug where PostgreSQL dialect would fail to render an
  expression in an [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) that did not correspond directly
  to a table-bound column; typically when a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct
  was one of the expressions within the index; or could misinterpret the
  list of expressions if one or more of them were such an expression.
  References: [#3174](https://www.sqlalchemy.org/trac/ticket/3174)

### mysql

- The `gaerdbms` dialect is no longer necessary, and emits a
  deprecation warning.  Google now recommends using the MySQLdb
  dialect directly.
  References: [#3275](https://www.sqlalchemy.org/trac/ticket/3275)
- Added a version check to the MySQLdb dialect surrounding the
  check for ‘utf8_bin’ collation, as this fails on MySQL server < 5.0.
  References: [#3274](https://www.sqlalchemy.org/trac/ticket/3274)

### sqlite

- Added support for partial indexes (e.g. with a WHERE clause) on
  SQLite.  Pull request courtesy Kai Groner.
  See also
  [Partial Indexes](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-partial-index)
- Added a new SQLite backend for the SQLCipher backend.  This backend
  provides for encrypted SQLite databases using the pysqlcipher Python
  driver, which is very similar to the pysqlite driver.
  See also
  [pysqlcipher](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlcipher)

### misc

- Fixed bug where the association proxy list class would not interpret
  slices correctly under Py3K.  Pull request courtesy
  Gilles Dartiguelongue.

## 0.9.8

Released: October 13, 2014

### orm

- Fixed bug that affected generally the same classes of event
  as that of [#3199](https://www.sqlalchemy.org/trac/ticket/3199), when the `named=True` parameter
  would be used.  Some events would fail to register, and others
  would not invoke the event arguments correctly, generally in the
  case of when an event was “wrapped” for adaption in some other way.
  The “named” mechanics have been rearranged to not interfere with
  the argument signature expected by internal wrapper functions.
  References: [#3197](https://www.sqlalchemy.org/trac/ticket/3197)
- Fixed bug that affected many classes of event, particularly
  ORM events but also engine events, where the usual logic of
  “de duplicating” a redundant call to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen)
  with the same arguments would fail, for those events where the
  listener function is wrapped.  An assertion would be hit within
  registry.py.  This assertion has now been integrated into the
  deduplication check, with the added bonus of a simpler means
  of checking deduplication across the board.
  References: [#3199](https://www.sqlalchemy.org/trac/ticket/3199)
- Fixed warning that would emit when a complex self-referential
  primaryjoin contained functions, while at the same time remote_side
  was specified; the warning would suggest setting “remote side”.
  It now only emits if remote_side isn’t present.
  References: [#3194](https://www.sqlalchemy.org/trac/ticket/3194)

### orm declarative

- Fixed “‘NoneType’ object has no attribute ‘concrete’” error
  when using [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) in conjunction with
  a subclass that declares `__abstract__`.
  References: [#3185](https://www.sqlalchemy.org/trac/ticket/3185)

### engine

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
  References: [#3200](https://www.sqlalchemy.org/trac/ticket/3200)
- The string keys that are used to determine the columns impacted
  for an INSERT or UPDATE are now sorted when they contribute towards
  the “compiled cache” cache key.   These keys were previously not
  deterministically ordered, meaning the same statement could be
  cached multiple times on equivalent keys, costing both in terms of
  memory as well as performance.
  References: [#3165](https://www.sqlalchemy.org/trac/ticket/3165)

### sql

- Fixed bug where a fair number of SQL elements within
  the sql package would fail to `__repr__()` successfully,
  due to a missing `description` attribute that would then invoke
  a recursion overflow when an internal AttributeError would then
  re-invoke `__repr__()`.
  References: [#3195](https://www.sqlalchemy.org/trac/ticket/3195)
- An adjustment to table/index reflection such that if an index
  reports a column that isn’t found to be present in the table,
  a warning is emitted and the column is skipped.  This can occur
  for some special system column situations as has been observed
  with Oracle.
  References: [#3180](https://www.sqlalchemy.org/trac/ticket/3180)
- Fixed bug in CTE where `literal_binds` compiler argument would not
  be always be correctly propagated when one CTE referred to another
  aliased CTE in a statement.
  References: [#3154](https://www.sqlalchemy.org/trac/ticket/3154)
- Fixed 0.9.7 regression caused by [#3067](https://www.sqlalchemy.org/trac/ticket/3067) in conjunction with
  a mis-named unit test such that so-called “schema” types like
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) and [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) could no longer be pickled.
  References: [#3067](https://www.sqlalchemy.org/trac/ticket/3067), [#3144](https://www.sqlalchemy.org/trac/ticket/3144)

### postgresql

- Support is added for “sane multi row count” with the pg8000 driver,
  which applies mostly to when using versioning with the ORM.
  The feature is version-detected based on pg8000 1.9.14 or greater
  in use.  Pull request courtesy Tony Locke.
- A revisit to this issue first patched in 0.9.5, apparently
  psycopg2’s `.closed` accessor is not as reliable as we assumed,
  so we have added an explicit check for the exception messages
  “SSL SYSCALL error: Bad file descriptor” and
  “SSL SYSCALL error: EOF detected” when detecting an
  is-disconnect scenario.   We will continue to consult psycopg2’s
  connection.closed as a first check.
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
  References: [#3159](https://www.sqlalchemy.org/trac/ticket/3159)
- The exception wrapping system for DBAPI errors can now accommodate
  non-standard DBAPI exceptions, such as the psycopg2
  TransactionRollbackError.  These exceptions will now be raised
  using the closest available subclass in `sqlalchemy.exc`, in the
  case of TransactionRollbackError, `sqlalchemy.exc.OperationalError`.
  References: [#3075](https://www.sqlalchemy.org/trac/ticket/3075)
- Fixed bug in [array](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.array) object where comparison
  to a plain Python list would fail to use the correct array constructor.
  Pull request courtesy Andrew.
  References: [#3141](https://www.sqlalchemy.org/trac/ticket/3141)
- Added a supported [FunctionElement.alias()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement.alias) method to functions,
  e.g. the `func` construct.  Previously, behavior for this method
  was undefined.  The current behavior mimics that of pre-0.9.4,
  which is that the function is turned into a single-column FROM
  clause with the given alias name, where the column itself is
  anonymously named.
  References: [#3137](https://www.sqlalchemy.org/trac/ticket/3137)

### mysql

- Mysqlconnector as of version 2.0, probably as a side effect of
  the  python 3 merge, now does not expect percent signs (e.g.
  as used as the modulus operator and others) to be doubled,
  even when using the “pyformat” bound parameter format (this
  change is not documented by Mysqlconnector).  The dialect now
  checks for py2k and for mysqlconnector less than version 2.0
  when detecting if the modulus operator should be rendered as
  `%%` or `%`.
- Unicode SQL is now passed for MySQLconnector version 2.0 and above;
  for Py2k and MySQL < 2.0, strings are encoded.

### sqlite

- When selecting from a UNION using an attached database file,
  the pysqlite driver reports column names in cursor.description
  as ‘dbname.tablename.colname’, instead of ‘tablename.colname’ as
  it normally does for a UNION (note that it’s supposed to just be
  ‘colname’ for both, but we work around it).  The column translation
  logic here has been adjusted to retrieve the rightmost token, rather
  than the second token, so it works in both cases.   Workaround
  courtesy Tony Roberts.
  References: [#3211](https://www.sqlalchemy.org/trac/ticket/3211)

### mssql

- Fixed the version string detection in the pymssql dialect to
  work with Microsoft SQL Azure, which changes the word “SQL Server”
  to “SQL Azure”.
  References: [#3151](https://www.sqlalchemy.org/trac/ticket/3151)

### oracle

- Fixed long-standing bug in Oracle dialect where bound parameter
  names that started with numbers would not be quoted, as Oracle
  doesn’t like numerics in bound parameter names.
  References: [#2138](https://www.sqlalchemy.org/trac/ticket/2138)

### misc

- Fixed an unlikely race condition observed in some exotic end-user
  setups, where the attempt to check for “duplicate class name” in
  declarative would hit upon a not-totally-cleaned-up weak reference
  related to some other class being removed; the check here now ensures
  the weakref still references an object before calling upon it further.
  References: [#3208](https://www.sqlalchemy.org/trac/ticket/3208)
- Fixed bug in ordering list where the order of items would be
  thrown off during a collection replace event, if the
  reorder_on_append flag were set to True.  The fix ensures that the
  ordering list only impacts the list that is explicitly associated
  with the object.
  References: [#3191](https://www.sqlalchemy.org/trac/ticket/3191)
- Fixed bug where [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict)
  failed to implement the `update()` dictionary method, thus
  not catching changes. Pull request courtesy Matt Chisholm.
- Fixed bug where a custom subclass of [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict)
  would not show up in a “coerce” operation, and would instead
  return a plain [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict).  Pull request
  courtesy Matt Chisholm.
- Fixed bug in connection pool logging where the “connection checked out”
  debug logging message would not emit if the logging were set up using
  `logging.setLevel()`, rather than using the `echo_pool` flag.
  Tests to assert this logging have been added.  This is a
  regression that was introduced in 0.9.0.
  References: [#3168](https://www.sqlalchemy.org/trac/ticket/3168)

## 0.9.7

Released: July 22, 2014

### orm

- Fixed a regression caused by [#2976](https://www.sqlalchemy.org/trac/ticket/2976) released in 0.9.4 where
  the “outer join” propagation along a chain of joined eager loads
  would incorrectly convert an “inner join” along a sibling join path
  into an outer join as well, when only descendant paths should be
  receiving the “outer join” propagation; additionally, fixed related
  issue where “nested” join propagation would take place inappropriately
  between two sibling join paths.
  References: [#3131](https://www.sqlalchemy.org/trac/ticket/3131)
- Fixed a regression from 0.9.0 due to [#2736](https://www.sqlalchemy.org/trac/ticket/2736) where the
  [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method no longer set up the “from
  entity” of the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object correctly, so that
  subsequent [Query.filter_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter_by) or [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join)
  calls would fail to check the appropriate “from” entity when
  searching for attributes by string name.
  References: [#2736](https://www.sqlalchemy.org/trac/ticket/2736), [#3083](https://www.sqlalchemy.org/trac/ticket/3083)
- The “evaluator” for query.update()/delete() won’t work with multi-table
  updates, and needs to be set to synchronize_session=False or
  synchronize_session=’fetch’; a warning is now emitted.  In
  1.0 this will be promoted to a full exception.
  References: [#3117](https://www.sqlalchemy.org/trac/ticket/3117)
- Fixed bug where items that were persisted, deleted, or had a
  primary key change within a savepoint block would not
  participate in being restored to their former state (not in
  session, in session, previous PK) after the outer transaction
  were rolled back.
  References: [#3108](https://www.sqlalchemy.org/trac/ticket/3108)
- Fixed bug in subquery eager loading in conjunction with
  [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic), the targeting of entities and columns
  in the subquery load has been made more accurate with respect
  to this type of entity and others.
  References: [#3106](https://www.sqlalchemy.org/trac/ticket/3106)
- Fixed bug involving dynamic attributes, that was again a regression
  of [#3060](https://www.sqlalchemy.org/trac/ticket/3060) from version 0.9.5.  A self-referential relationship
  with lazy=’dynamic’ would raise a TypeError within a flush operation.
  References: [#3099](https://www.sqlalchemy.org/trac/ticket/3099)

### engine

- Added new event `ConnectionEvents.handle_error()`, a more
  fully featured and comprehensive replacement for
  `ConnectionEvents.dbapi_error()`.
  References: [#3076](https://www.sqlalchemy.org/trac/ticket/3076)

### sql

- Fixed bug in [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) and other [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType)
  subclasses where direct association of the type with a
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) would lead to a hang when events
  (like create events) were emitted on the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).
  This change is also **backported** to: 0.8.7
  References: [#3124](https://www.sqlalchemy.org/trac/ticket/3124)
- Fixed a bug within the custom operator plus [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant)
  system, whereby using a [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) in conjunction with
  variant would fail with an MRO error when a comparison operator was used.
  This change is also **backported** to: 0.8.7
  References: [#3102](https://www.sqlalchemy.org/trac/ticket/3102)
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
  References: [#3067](https://www.sqlalchemy.org/trac/ticket/3067)
- Fixed bug in common table expressions whereby positional bound
  parameters could be expressed in the wrong final order
  when CTEs were nested in certain ways.
  References: [#3090](https://www.sqlalchemy.org/trac/ticket/3090)
- Fixed bug where multi-valued [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct would fail
  to check subsequent values entries beyond the first one given
  for literal SQL expressions.
  References: [#3069](https://www.sqlalchemy.org/trac/ticket/3069)
- Added a “str()” step to the dialect_kwargs iteration for
  Python version < 2.6.5, working around the
  “no unicode keyword arg” bug as these args are passed along as
  keyword args within some reflection processes.
  References: [#3123](https://www.sqlalchemy.org/trac/ticket/3123)
- The [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method will now accept a
  type class as an argument which is internally converted to an
  instance, using the same convention long established by other
  constructs such as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
  References: [#3122](https://www.sqlalchemy.org/trac/ticket/3122)

### postgresql

- Added kw argument `postgresql_regconfig` to the
  [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) operator, allows the “reg config” argument
  to be specified to the `to_tsquery()` function emitted.
  Pull request courtesy Jonathan Vanasco.
  References: [#3078](https://www.sqlalchemy.org/trac/ticket/3078)
- Added support for PostgreSQL JSONB via [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB).  Pull request
  courtesy Damian Dimmich.
- Fixed bug introduced in 0.9.5 by new pg8000 isolation level feature
  where engine-level isolation level parameter would raise an error
  on connect.
  References: [#3134](https://www.sqlalchemy.org/trac/ticket/3134)

### mysql

- MySQL error 2014 “commands out of sync” appears to be raised as a
  ProgrammingError, not OperationalError, in modern MySQL-Python versions;
  all MySQL error codes that are tested for “is disconnect” are now
  checked within OperationalError and ProgrammingError regardless.
  This change is also **backported** to: 0.8.7
  References: [#3101](https://www.sqlalchemy.org/trac/ticket/3101)

### sqlite

- Fixed a SQLite join rewriting issue where a subquery that is embedded
  as a scalar subquery such as within an IN would receive inappropriate
  substitutions from the enclosing query, if the same table were present
  inside the subquery as were in the enclosing query such as in a
  joined inheritance scenario.
  References: [#3130](https://www.sqlalchemy.org/trac/ticket/3130)

### mssql

- Enabled “multivalues insert” for SQL Server 2008.  Pull request
  courtesy Albert Cervin.  Also expanded the checks for “IDENTITY INSERT”
  mode to include when the identity key is present in the
  VALUEs clause of the statement.
- Added statement encoding to the “SET IDENTITY_INSERT”
  statements which operate when an explicit INSERT is being
  interjected into an IDENTITY column, to support non-ascii table
  identifiers on drivers such as pyodbc + unix + py2k that don’t
  support unicode statements.
  This change is also **backported** to: 0.8.7
- In the SQL Server pyodbc dialect, repaired the implementation
  for the `description_encoding` dialect parameter, which when
  not explicitly set was preventing  cursor.description from
  being parsed correctly in the case of result sets that
  contained names in alternate encodings.  This parameter
  shouldn’t be needed going forward.
  This change is also **backported** to: 0.8.7
  References: [#3091](https://www.sqlalchemy.org/trac/ticket/3091)
- Fixed a regression from 0.9.5 caused by [#3025](https://www.sqlalchemy.org/trac/ticket/3025) where the
  query used to determine “default schema” is invalid in SQL Server 2000.
  For SQL Server 2000 we go back to defaulting to the “schema name”
  parameter of the dialect, which is configurable but defaults
  to ‘dbo’.
  References: [#3025](https://www.sqlalchemy.org/trac/ticket/3025)

### oracle

- Fixed bug in oracle dialect test suite where in one test,
  ‘username’ was assumed to be in the database URL, even though
  this might not be the case.
  References: [#3128](https://www.sqlalchemy.org/trac/ticket/3128)

### tests

- Fixed bug where “python setup.py test” wasn’t calling into
  distutils appropriately, and errors would be emitted at the end
  of the test suite.

### misc

- Fixed bug when the declarative `__abstract__` flag was not being
  distinguished for when it was actually the value `False`.
  The `__abstract__` flag needs to actually evaluate to a True
  value at the level being tested.
  References: [#3097](https://www.sqlalchemy.org/trac/ticket/3097)

## 0.9.6

Released: June 23, 2014

### orm

- Reverted the change for [#3060](https://www.sqlalchemy.org/trac/ticket/3060) - this is a unit of work
  fix that is updated more comprehensively in 1.0 via [#3061](https://www.sqlalchemy.org/trac/ticket/3061).
  The fix in [#3060](https://www.sqlalchemy.org/trac/ticket/3060) unfortunately produces a new issue whereby
  an eager load of a many-to-one attribute can produce an event
  that is interpreted into an attribute change.
  References: [#3060](https://www.sqlalchemy.org/trac/ticket/3060)

## 0.9.5

Released: June 23, 2014

### orm

- The “primaryjoin” model has been stretched a bit further to allow
  a join condition that is strictly from a single column to itself,
  translated through some kind of SQL function or expression.  This
  is kind of experimental, but the first proof of concept is a
  “materialized path” join condition where a path string is compared
  to itself using “like”.   The [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like) operator has
  also been added to the list of valid operators to use in a primaryjoin
  condition.
  References: [#3029](https://www.sqlalchemy.org/trac/ticket/3029)
- Added new utility function [make_transient_to_detached()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient_to_detached) which can
  be used to manufacture objects that behave as though they were loaded
  from a session, then detached.   Attributes that aren’t present
  are marked as expired, and the object can be added to a Session
  where it will act like a persistent one.
  References: [#3017](https://www.sqlalchemy.org/trac/ticket/3017)
- Fixed bug in subquery eager loading where a long chain of
  eager loads across a polymorphic-subclass boundary in conjunction
  with polymorphic loading would fail to locate the subclass-link in the
  chain, erroring out with a missing property name on an
  [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass).
  This change is also **backported** to: 0.8.7
  References: [#3055](https://www.sqlalchemy.org/trac/ticket/3055)
- Fixed ORM bug where the [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper) function would mask
  AttributeErrors or KeyErrors that should raise during mapper
  configuration due to user errors.  The catch for attribute/keyerror
  has been made more specific to not include the configuration step.
  This change is also **backported** to: 0.8.7
  References: [#3047](https://www.sqlalchemy.org/trac/ticket/3047)
- Additional checks have been added for the case where an inheriting
  mapper is implicitly combining one of its column-based attributes
  with that of the parent, where those columns normally don’t necessarily
  share the same value.  This is an extension of an existing check that
  was added via [#1892](https://www.sqlalchemy.org/trac/ticket/1892); however this new check emits only a
  warning, instead of an exception, to allow for applications that may
  be relying upon the existing behavior.
  See also
  [I’m getting a warning or error about “Implicitly combining column X under attribute Y”](https://docs.sqlalchemy.org/en/20/faq/ormconfiguration.html#faq-combining-columns)
  References: [#3042](https://www.sqlalchemy.org/trac/ticket/3042)
- Modified the behavior of [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only) such that primary key
  columns are always added to the list of columns to be “undeferred”;
  otherwise, the ORM can’t load the row’s identity.   Apparently,
  one can defer the mapped primary keys and the ORM will fail, that
  hasn’t been changed.  But as load_only is essentially saying
  “defer all but X”, it’s more critical that PK cols not be part of this
  deferral.
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
  References: [#3060](https://www.sqlalchemy.org/trac/ticket/3060)
- Related to [#3060](https://www.sqlalchemy.org/trac/ticket/3060), an adjustment has been made to the unit
  of work such that loading for related many-to-one objects is slightly
  more aggressive, in the case of a graph of self-referential objects
  that are to be deleted; the load of related objects is to help
  determine the correct order for deletion if passive_deletes is
  not set.
- Fixed bug in SQLite join rewriting where anonymized column names
  due to repeats would not correctly be rewritten in subqueries.
  This would affect SELECT queries with any kind of subquery + join.
  References: [#3057](https://www.sqlalchemy.org/trac/ticket/3057)
- Fixes to the newly enhanced boolean coercion in [#2804](https://www.sqlalchemy.org/trac/ticket/2804) where
  the new rules for “where” and “having” wouldn’t take effect for the
  “whereclause” and “having” kw arguments of the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct,
  which is also what [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) uses so wasn’t working in the
  ORM either.
  References: [#3013](https://www.sqlalchemy.org/trac/ticket/3013)

### examples

- Added a new example illustrating materialized paths, using the
  latest relationship features.   Example courtesy Jack Zhou.

### engine

- Fixed bug which would occur if a DBAPI exception
  occurs when the engine first connects and does its initial checks,
  and the exception is not a disconnect exception, yet the cursor
  raises an error when we try to close it.  In this case the real
  exception would be quashed as we tried to log the cursor close
  exception via the connection pool and failed, as we were trying
  to access the pool’s logger in a way that is inappropriate
  in this very specific scenario.
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
  References: [#3043](https://www.sqlalchemy.org/trac/ticket/3043)

### sql

- Liberalized the contract for [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) a bit in that you can
  specify a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) expression as the target; the index no longer
  needs to have a table-bound column present if the index is to be
  manually added to the table, either via inline declaration or via
  [Table.append_constraint()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_constraint).
  References: [#3028](https://www.sqlalchemy.org/trac/ticket/3028)
- Added new flag [between.symmetric](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between.params.symmetric), when set to True
  renders “BETWEEN SYMMETRIC”.  Also added a new negation operator
  “notbetween_op”, which now allows an expression like `~col.between(x, y)`
  to render as “col NOT BETWEEN x AND y”, rather than a parenthesized NOT
  string.
  References: [#2990](https://www.sqlalchemy.org/trac/ticket/2990)
- Fixed bug in INSERT..FROM SELECT construct where selecting from a
  UNION would wrap the union in an anonymous (e.g. unlabeled) subquery.
  This change is also **backported** to: 0.8.7
  References: [#3044](https://www.sqlalchemy.org/trac/ticket/3044)
- Fixed bug where [Table.update()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.update) and [Table.delete()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.delete)
  would produce an empty WHERE clause when an empty [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
  or [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) or other blank expression were applied.  This is
  now consistent with that of [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).
  This change is also **backported** to: 0.8.7
  References: [#3045](https://www.sqlalchemy.org/trac/ticket/3045)
- The [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable) flag is implicitly set to `False`
  when that [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is referred to in an explicit
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) for that table.  This behavior now
  matches that of when the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) itself has the
  [Column.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.primary_key) flag set to `True`, which is
  intended to be an exactly equivalent case.
  References: [#3023](https://www.sqlalchemy.org/trac/ticket/3023)
- Fixed bug where the [Operators.__and__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__and__),
  [Operators.__or__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__or__) and [Operators.__invert__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.__invert__)
  operator overload methods could not be overridden within a custom
  [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) implementation.
  References: [#3012](https://www.sqlalchemy.org/trac/ticket/3012)
- Fixed bug in new [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method where
  adding an argument for a construct not previously included for any
  special arguments would fail.
  References: [#3024](https://www.sqlalchemy.org/trac/ticket/3024)
- Fixed regression introduced in 0.9 where new “ORDER BY <labelname>”
  feature from [#1068](https://www.sqlalchemy.org/trac/ticket/1068) would not apply quoting rules to the
  label name as rendered in the ORDER BY.
  References: [#1068](https://www.sqlalchemy.org/trac/ticket/1068), [#3020](https://www.sqlalchemy.org/trac/ticket/3020)
- Restored the import for [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function) to the `sqlalchemy.sql.expression`
  import namespace, which was removed at the beginning of 0.9.

### postgresql

- Added support for AUTOCOMMIT isolation level when using the pg8000
  DBAPI.  Pull request courtesy Tony Locke.
- Added a new flag [ARRAY.zero_indexes](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.params.zero_indexes) to the PostgreSQL
  [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) type.  When set to `True`, a value of one will be
  added to all array index values before passing to the database, allowing
  better interoperability between Python style zero-based indexes and
  PostgreSQL one-based indexes.  Pull request courtesy Alexey Terentev.
  References: [#2785](https://www.sqlalchemy.org/trac/ticket/2785)
- Added the `hashable=False` flag to the PG [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE) type, which
  is needed to allow the ORM to skip over trying to “hash” an ORM-mapped
  HSTORE column when requesting it in a mixed column/entity list.
  Patch courtesy Gunnlaugur Þór Briem.
  This change is also **backported** to: 0.8.7
  References: [#3053](https://www.sqlalchemy.org/trac/ticket/3053)
- Added a new “disconnect” message “connection has been closed unexpectedly”.
  This appears to be related to newer versions of SSL.
  Pull request courtesy Antti Haapala.
  This change is also **backported** to: 0.8.7
- The psycopg2 `.closed` accessor is now consulted when determining
  if an exception is a “disconnect” error; ideally, this should remove
  the need for any other inspection of the exception message to detect
  disconnect, however we will leave those existing messages in place
  as a fallback.   This should be able to handle newer cases like
  “SSL EOF” conditions.  Pull request courtesy Dirk Mueller.
  References: [#3021](https://www.sqlalchemy.org/trac/ticket/3021)
- Added a new type [OID](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.OID) to the PostgreSQL dialect.
  While “oid” is generally a private type within PG that is not exposed
  in modern versions, there are some PG use cases such as large object
  support where these types might be exposed, as well as within some
  user-reported schema reflection use cases.
  References: [#3002](https://www.sqlalchemy.org/trac/ticket/3002)

### mysql

- Fixed bug where column names added to `mysql_length` parameter
  on an index needed to have the same quoting for quoted names in
  order to be recognized.  The fix makes the quotes optional but
  also provides the old behavior for backwards compatibility with those
  using the workaround.
  This change is also **backported** to: 0.8.7
  References: [#3085](https://www.sqlalchemy.org/trac/ticket/3085)
- Added support for reflecting tables where an index includes
  KEY_BLOCK_SIZE using an equal sign.  Pull request courtesy
  Sean McGivern.
  This change is also **backported** to: 0.8.7

### mssql

- Revised the query used to determine the current default schema name
  to use the `database_principal_id()` function in conjunction with
  the `sys.database_principals` view so that we can determine
  the default schema independently of the type of login in progress
  (e.g., SQL Server, Windows, etc).
  References: [#3025](https://www.sqlalchemy.org/trac/ticket/3025)

### tests

- Corrected for some deprecation warnings involving the `imp`
  module and Python 3.3 or greater, when running tests.  Pull
  request courtesy Matt Chisholm.
  References: [#2830](https://www.sqlalchemy.org/trac/ticket/2830)

### misc

- The `__mapper_args__` dictionary is copied from a declarative
  mixin or abstract class when accessed, so that modifications made
  to this dictionary by declarative itself won’t conflict with that
  of other mappings.  The dictionary is modified regarding the
  `version_id_col` and `polymorphic_on` arguments, replacing the
  column within with the one that is officially mapped to the local
  class/table.
  This change is also **backported** to: 0.8.7
  References: [#3062](https://www.sqlalchemy.org/trac/ticket/3062)
- Fixed bug in mutable extension where [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) did not
  report change events for the `setdefault()` dictionary operation.
  This change is also **backported** to: 0.8.7
  References: [#3051](https://www.sqlalchemy.org/trac/ticket/3051), [#3093](https://www.sqlalchemy.org/trac/ticket/3093)
- Fixed bug where [MutableDict.setdefault()](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict.setdefault) didn’t return the
  existing or new value (this bug was not released in any 0.8 version).
  Pull request courtesy Thomas Hervé.
  This change is also **backported** to: 0.8.7
  References: [#3051](https://www.sqlalchemy.org/trac/ticket/3051), [#3093](https://www.sqlalchemy.org/trac/ticket/3093)
- In public test suite, changed to use of `String(40)` from
  less-supported `Text` in `StringTest.test_literal_backslashes`.
  Pullreq courtesy Jan.
- Fixed bug where the combination of “limit” rendering as
  “SELECT FIRST n ROWS” using a bound parameter (only firebird has both),
  combined with column-level subqueries
  which also feature “limit” as well as “positional” bound parameters
  (e.g. qmark style) would erroneously assign the subquery-level positions
  before that of the enclosing SELECT, thus returning parameters which
  are out of order.
  References: [#3038](https://www.sqlalchemy.org/trac/ticket/3038)

## 0.9.4

Released: March 28, 2014

### general

- Support has been added for pytest to run tests.   This runner
  is currently being supported in addition to nose, and will likely
  be preferred to nose going forward.   The nose plugin system used
  by SQLAlchemy has been split out so that it works under pytest as
  well.  There are no plans to drop support for nose at the moment
  and we hope that the test suite itself can continue to remain as
  agnostic of testing platform as possible.  See the file
  README.unittests.rst for updated information on running tests
  with pytest.
  The test plugin system has also been enhanced to support running
  tests against multiple database URLs at once, by specifying the `--db`
  and/or `--dburi` flags multiple times.  This does not run the entire test
  suite for each database, but instead allows test cases that are specific
  to certain backends make use of that backend as the test is run.
  When using pytest as the test runner, the system will also run
  specific test suites multiple times, once for each database, particularly
  those tests within the “dialect suite”.   The plan is that the enhanced
  system will also be used by Alembic, and allow Alembic to run
  migration operation tests against multiple backends in one run, including
  third-party backends not included within Alembic itself.
  Third party dialects and extensions are also encouraged to standardize
  on SQLAlchemy’s test suite as a basis; see the file README.dialects.rst
  for background on building out from SQLAlchemy’s test platform.
- Adjusted `setup.py` file to support the possible future
  removal of the `setuptools.Feature` extension from setuptools.
  If this keyword isn’t present, the setup will still succeed
  with setuptools rather than falling back to distutils.  C extension
  building can be disabled now also by setting the
  DISABLE_SQLALCHEMY_CEXT environment variable.  This variable works
  whether or not setuptools is even available.
  This change is also **backported** to: 0.8.6
  References: [#2986](https://www.sqlalchemy.org/trac/ticket/2986)
- Fixed some test/feature failures occurring in Python 3.4,
  in particular the logic used to wrap “column default” callables
  wouldn’t work properly for Python built-ins.
  References: [#2979](https://www.sqlalchemy.org/trac/ticket/2979)

### orm

- Added new parameter `mapper.confirm_deleted_rows`.  Defaults
  to True, indicates that a series of DELETE statements should confirm
  that the cursor rowcount matches the number of primary keys that should
  have matched;  this behavior had been taken off in most cases
  (except when version_id is used) to support the unusual edge case of
  self-referential ON DELETE CASCADE; to accommodate this, the message
  is now just a warning, not an exception, and the flag can be used
  to indicate a mapping that expects self-referential cascaded
  deletes of this nature.  See also [#2403](https://www.sqlalchemy.org/trac/ticket/2403) for background on the
  original change.
  References: [#3007](https://www.sqlalchemy.org/trac/ticket/3007)
- A warning is emitted if the [MapperEvents.before_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured)
  or [MapperEvents.after_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_configured) events are applied to a
  specific mapper or mapped class, as the events are only invoked
  for the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) target at the general level.
- Added a new keyword argument `once=True` to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen)
  and [listens_for()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listens_for).  This is a convenience feature which
  will wrap the given listener such that it is only invoked once.
- Added a new option to [relationship.innerjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.innerjoin) which is
  to specify the string `"nested"`.  When set to `"nested"` as opposed
  to `True`, the “chaining” of joins will parenthesize the inner join on the
  right side of an existing outer join, instead of chaining as a string
  of outer joins.   This possibly should have been the default behavior
  when 0.9 was released, as we introduced the feature of right-nested
  joins in the ORM, however we are keeping it as a non-default for now
  to avoid further surprises.
  See also
  [Right-nested inner joins available in joined eager loads](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-2976)
  References: [#2976](https://www.sqlalchemy.org/trac/ticket/2976)
- Fixed ORM bug where changing the primary key of an object, then marking
  it for DELETE would fail to target the correct row for DELETE.
  This change is also **backported** to: 0.8.6
  References: [#3006](https://www.sqlalchemy.org/trac/ticket/3006)
- Fixed regression from 0.8.3 as a result of [#2818](https://www.sqlalchemy.org/trac/ticket/2818)
  where [Query.exists()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists) wouldn’t work on a query that only
  had a [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) entry but no other entities.
  This change is also **backported** to: 0.8.6
  References: [#2995](https://www.sqlalchemy.org/trac/ticket/2995)
- Improved an error message which would occur if a query() were made
  against a non-selectable, such as a [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column), and then
  an attempt was made to use [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) such that the “left”
  side would be determined as `None` and then fail.  This condition
  is now detected explicitly.
  This change is also **backported** to: 0.8.6
- Removed stale names from `sqlalchemy.orm.interfaces.__all__` and
  refreshed with current names, so that an `import *` from this
  module again works.
  This change is also **backported** to: 0.8.6
  References: [#2975](https://www.sqlalchemy.org/trac/ticket/2975)
- Fixed a very old behavior where the lazy load emitted for a one-to-many
  could inappropriately pull in the parent table, and also return results
  inconsistent based on what’s in the parent table, when the primaryjoin
  includes some kind of discriminator against the parent table, such
  as `and_(parent.id == child.parent_id, parent.deleted == False)`.
  While this primaryjoin doesn’t make that much sense for a one-to-many,
  it is slightly more common when applied to the many-to-one side, and
  the one-to-many comes as a result of a backref.
  Loading rows from `child` in this case would keep `parent.deleted == False`
  as is within the query, thereby yanking it into the FROM clause
  and doing a cartesian product.  The new behavior will now substitute
  the value of the local “parent.deleted” for that parameter as is
  appropriate.   Though typically, a real-world app probably wants to use a
  different primaryjoin for the o2m side in any case.
  References: [#2948](https://www.sqlalchemy.org/trac/ticket/2948)
- Improved the check for “how to join from A to B” such that when
  a table has multiple, composite foreign keys targeting a parent table,
  the [relationship.foreign_keys](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys) argument will be properly
  interpreted in order to resolve the ambiguity; previously this condition
  would raise that there were multiple FK paths when in fact the
  foreign_keys argument should be establishing which one is expected.
  References: [#2965](https://www.sqlalchemy.org/trac/ticket/2965)
- Added support for the not-quite-yet-documented `insert=True`
  flag for [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) to work with mapper / instance events.
- Fixed bug where events set to listen at the class
  level (e.g. on the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) or [ClassManager](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ClassManager)
  level, as opposed to on an individual mapped class, and also on
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)) that also made use of internal argument conversion
  (which is most within those categories) would fail to be removable.
  References: [#2973](https://www.sqlalchemy.org/trac/ticket/2973)
- Fixed regression from 0.8 where using an option like
  [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload) with the “wildcard” expression, e.g. `"*"`,
  would raise an assertion error in the case where the query didn’t
  contain any actual entities.  This assertion is meant for other cases
  and was catching this one inadvertently.
- More fixes to SQLite “join rewriting”; the fix from [#2967](https://www.sqlalchemy.org/trac/ticket/2967)
  implemented right before the release of 0.9.3 affected the case where
  a UNION contained nested joins in it.   “Join rewriting” is a feature
  with a wide range of possibilities and is the first intricate
  “SQL rewriting” feature we’ve introduced in years, so we’re sort of
  going through a lot of iterations with it (not unlike eager loading
  back in the 0.2/0.3 series, polymorphic loading in 0.4/0.5). We should
  be there soon so thanks for bearing with us :).
  References: [#2969](https://www.sqlalchemy.org/trac/ticket/2969)

### examples

- Fixed bug in the versioned_history example where column-level INSERT
  defaults would prevent history values of NULL from being written.

### engine

- Added some new event mechanics for dialect-level events; the initial
  implementation allows an event handler to redefine the specific mechanics
  by which an arbitrary dialect invokes execute() or executemany() on a
  DBAPI cursor.  The new events, at this point semi-public and experimental,
  are in support of some upcoming transaction-related extensions.
- An event listener can now be associated with a [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
  after one or more [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) objects have been created
  (such as by an orm [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or via explicit connect)
  and the listener will pick up events from those connections.
  Previously, performance concerns pushed the event transfer from
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) to  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) at init-time only, but
  we’ve inlined a bunch of conditional checks to make this possible
  without any additional function calls.
  References: [#2978](https://www.sqlalchemy.org/trac/ticket/2978)
- A major improvement made to the mechanics by which the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
  recycles the connection pool when a “disconnect” condition is detected;
  instead of discarding the pool and explicitly closing out connections,
  the pool is retained and a “generational” timestamp is updated to
  reflect the current time, thereby causing all existing connections
  to be recycled when they are next checked out.   This greatly simplifies
  the recycle process, removes the need for “waking up” connect attempts
  waiting on the old pool and eliminates the race condition that many
  immediately-discarded “pool” objects could be created during the
  recycle operation.
  References: [#2985](https://www.sqlalchemy.org/trac/ticket/2985)
- The [ConnectionEvents.after_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.after_cursor_execute) event is now
  emitted for the “_cursor_execute()” method of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection);
  this is the “quick” executor that is used for things like
  when a sequence is executed ahead of an INSERT statement, as well as
  for dialect startup checks like unicode returns, charset, etc.
  the [ConnectionEvents.before_cursor_execute()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute) event was already
  invoked here.  The “executemany” flag is now always set to False
  here, as this event always corresponds to a single execution.
  Previously the flag could be True if we were acting on behalf of
  an executemany INSERT statement.

### sql

- Added support for literal rendering of boolean values, e.g.
  “true” / “false” or “1” / “0”.
- Added a new feature [conv()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.conv), the purpose of which is to
  mark a constraint name as already having had a naming convention applied.
  This token will be used by Alembic migrations as of Alembic 0.6.4
  in order to render constraints in migration scripts with names marked
  as already having been subject to a naming convention.
- The new dialect-level keyword argument system for schema-level
  constructs has been enhanced in order to assist with existing
  schemes that rely upon addition of ad-hoc keyword arguments to
  constructs.
  E.g., a construct such as [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) will again accept
  ad-hoc keyword arguments within the [Index.kwargs](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.kwargs) collection,
  after construction:
  ```
  idx = Index("a", "b")
  idx.kwargs["mysql_someargument"] = True
  ```
  To suit the use case of allowing custom arguments at construction time,
  the [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method now allows this registration:
  ```
  Index.argument_for("mysql", "someargument", False)
  idx = Index("a", "b", mysql_someargument=True)
  ```
  See also
  [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for)
  References: [#2866](https://www.sqlalchemy.org/trac/ticket/2866), [#2962](https://www.sqlalchemy.org/trac/ticket/2962)
- Fixed bug in [tuple_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.tuple_) construct where the “type” of essentially
  the first SQL expression would be applied as the “comparison type”
  to a compared tuple value; this has the effect in some cases of an
  inappropriate “type coercion” occurring, such as when a tuple that
  has a mix of String and Binary values improperly coerces target
  values to Binary even though that’s not what they are on the left
  side.  [tuple_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.tuple_) now expects heterogeneous types within its
  list of values.
  This change is also **backported** to: 0.8.6
  References: [#2977](https://www.sqlalchemy.org/trac/ticket/2977)
- Fixed an 0.9 regression where a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that failed to
  reflect correctly wouldn’t be removed from the parent
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), even though in an invalid state.  Pullreq
  courtesy Roman Podoliaka.
  References: [#2988](https://www.sqlalchemy.org/trac/ticket/2988)
- [MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) feature will now also
  apply to [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) objects that are associated
  directly with a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) instead of just on the
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
- Fixed bug in new [MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) feature
  where the name of a check constraint making use of the
  “%(constraint_name)s” token would get doubled up for the
  constraint generated by a boolean or enum type, and overall
  duplicate events would cause the “%(constraint_name)s” token
  to keep compounding itself.
  References: [#2991](https://www.sqlalchemy.org/trac/ticket/2991)
- Adjusted the logic which applies names to the .c collection when
  a no-name [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) is received, e.g. via [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal)
  or similar; the “key” of the bind param is used as the key within
  .c. rather than the rendered name.  Since these binds have “anonymous”
  names in any case, this allows individual bound parameters to
  have their own name within a selectable if they are otherwise unlabeled.
  References: [#2974](https://www.sqlalchemy.org/trac/ticket/2974)
- Some changes to how the [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) collection behaves
  when presented with duplicate columns.  The behavior of emitting a
  warning and replacing the old column with the same name still
  remains to some degree; the replacement in particular is to maintain
  backwards compatibility.  However, the replaced column still remains
  associated with the `c` collection now in a collection `._all_columns`,
  which is used by constructs such as aliases and unions, to deal with
  the set of columns in `c` more towards what is actually in the
  list of columns rather than the unique set of key names.  This helps
  with situations where SELECT statements with same-named columns
  are used in unions and such, so that the union can match the columns
  up positionally and also there’s some chance of `FromClause.corresponding_column()`
  still being usable here (it can now return a column that is only
  in selectable.c._all_columns and not otherwise named).
  The new collection is underscored as we still need to decide where this
  list might end up.   Theoretically it
  would become the result of iter(selectable.c), however this would mean
  that the length of the iteration would no longer match the length of
  keys(), and that behavior needs to be checked out.
  References: [#2974](https://www.sqlalchemy.org/trac/ticket/2974)
- Fixed issue in new [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method where the ordering
  of columns given positionally would not be preserved.   This could
  have potential impact in positional situations such as applying the
  resulting `TextAsFrom` object to a union.

### postgresql

- Enabled “sane multi-row count” checking for the psycopg2 DBAPI, as
  this seems to be supported as of psycopg2 2.0.9.
  This change is also **backported** to: 0.8.6
- Fixed regression caused by release 0.8.5 / 0.9.3’s compatibility
  enhancements where index reflection on PostgreSQL versions specific
  to only the 8.1, 8.2 series again
  broke, surrounding the ever problematic int2vector type.  While
  int2vector supports array operations as of 8.1, apparently it only
  supports CAST to a varchar as of 8.3.
  This change is also **backported** to: 0.8.6
  References: [#3000](https://www.sqlalchemy.org/trac/ticket/3000)

### mysql

- Tweaked the settings for mysql-connector-python; in Py2K, the
  “supports unicode statements” flag is now False, so that SQLAlchemy
  will encode the *SQL string* (note: *not* the parameters)
  to bytes before sending to the database.  This seems to allow
  all unicode-related tests to pass for mysql-connector, including those
  that use non-ascii table/column names, as well as some tests for the
  TEXT type using unicode under cursor.executemany().

### oracle

- Added a new engine option `coerce_to_unicode=True` to the
  cx_Oracle dialect, which restores the cx_Oracle outputtypehandler
  approach to Python unicode conversion under Python 2, which was
  removed in 0.9.2 as a result of [#2911](https://www.sqlalchemy.org/trac/ticket/2911).  Some use cases would
  prefer that unicode coercion is unconditional for all string values,
  despite performance concerns.  Pull request courtesy
  Christoph Zwerschke.
  References: [#2911](https://www.sqlalchemy.org/trac/ticket/2911)
- Added new datatype [DATE](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.DATE), which is a subclass of
  [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime).  As Oracle has no “datetime” type per se,
  it instead has only `DATE`, it is appropriate here that the
  `DATE` type as present in the Oracle dialect be an instance of
  [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime).  This issue doesn’t change anything as far as
  the behavior of the type, as data conversion is handled by the
  DBAPI in any case, however the improved subclass layout will help
  the use cases of inspecting types for cross-database compatibility.
  Also removed uppercase `DATETIME` from the Oracle dialect as this
  type isn’t functional in that context.
  References: [#2987](https://www.sqlalchemy.org/trac/ticket/2987)

### tests

- Fixed a few errant `u''` strings that would prevent tests from passing
  in Py3.2.  Patch courtesy Arfrever Frehtes Taifersar Arahesis.
  References: [#2980](https://www.sqlalchemy.org/trac/ticket/2980)

### misc

- Fixed bug in mutable extension as well as
  [flag_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified) where the change event would not be
  propagated if the attribute had been reassigned to itself.
  This change is also **backported** to: 0.8.6
  References: [#2997](https://www.sqlalchemy.org/trac/ticket/2997)
- Added support to automap for the case where a relationship should
  not be created between two classes that are in a joined inheritance
  relationship, for those foreign keys that link the subclass back to
  the superclass.
  References: [#3004](https://www.sqlalchemy.org/trac/ticket/3004)
- Fixed small issue in [SingletonThreadPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.SingletonThreadPool) where the current
  connection to be returned might get inadvertently cleaned out during
  the “cleanup” process.  Patch courtesy jd23.
- Fixed bug in association proxy where assigning an empty slice
  (e.g. `x[:] = [...]`) would fail on Py3k.
- Fixed a regression in association proxy caused by [#2810](https://www.sqlalchemy.org/trac/ticket/2810) which
  caused a user-provided “getter” to no longer receive values of `None`
  when fetching scalar values from a target that is non-present.  The
  check for None introduced by this change is now moved into the default
  getter, so a user-provided getter will also again receive values of
  None.
  References: [#2810](https://www.sqlalchemy.org/trac/ticket/2810)

## 0.9.3

Released: February 19, 2014

### orm

- Added new [MapperEvents.before_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured) event which allows
  an event at the start of [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers), as well
  as `__declare_first__()` hook within declarative to complement
  `__declare_last__()`.
- Fixed bug where [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get) would fail to consistently
  raise the [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) that invokes when called
  on a query with existing criterion, when the given identity is
  already present in the identity map.
  This change is also **backported** to: 0.8.5
  References: [#2951](https://www.sqlalchemy.org/trac/ticket/2951)
- Fixed bug in SQLite “join rewriting” where usage of an exists() construct
  would fail to be rewritten properly, such as when the exists is
  mapped to a column_property in an intricate nested-join scenario.
  Also fixed a somewhat related issue where join rewriting would fail
  on the columns clause of the SELECT statement if the targets were
  aliased tables, as opposed to individual aliased columns.
  References: [#2967](https://www.sqlalchemy.org/trac/ticket/2967)
- Fixed an 0.9 regression where ORM instance or mapper events applied
  to a base class such as a declarative base with the propagate=True
  flag would fail to apply to existing mapped classes which also
  used inheritance due to an assertion.  Additionally, repaired an
  attribute error which could occur during removal of such an event,
  depending on how it was first assigned.
  References: [#2949](https://www.sqlalchemy.org/trac/ticket/2949)
- Improved the initialization logic of composite attributes such that
  calling `MyClass.attribute` will not require that the configure
  mappers step has occurred, e.g. it will just work without throwing
  any error.
  References: [#2935](https://www.sqlalchemy.org/trac/ticket/2935)
- More issues with [ticket:2932] first resolved in 0.9.2 where
  using a column key of the form `<tablename>_<columnname>`
  matching that of an aliased column in the text would still not
  match at the ORM level, which is ultimately due to a core
  column-matching issue.  Additional rules have been added so that the
  column `_label` is taken into account when working with a
  `TextAsFrom` construct or with literal columns.
  References: [#2932](https://www.sqlalchemy.org/trac/ticket/2932)

### orm declarative

- Fixed bug where [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase) would fail to be
  fully usable within declarative relationship configuration, as its
  string classname would not be available in the registry of classnames
  at mapper configuration time.   The class now explicitly adds itself
  to the class registry, and additionally both [AbstractConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.AbstractConcreteBase)
  as well as [ConcreteBase](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.ConcreteBase) set themselves up *before* mappers
  are configured within the [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers) setup, using
  the new [MapperEvents.before_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured) event.
  References: [#2950](https://www.sqlalchemy.org/trac/ticket/2950)

### examples

- Added optional “changed” column to the versioned rows example, as well
  as support for when the versioned [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) has an explicit
  [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) argument.   Pull request
  courtesy jplaverdure.

### engine

- Fixed a critical regression caused by [#2880](https://www.sqlalchemy.org/trac/ticket/2880) where the newly
  concurrent ability to return connections from the pool means that the
  “first_connect” event is now no longer synchronized either, thus leading
  to dialect mis-configurations under even minimal concurrency situations.
  This change is also **backported** to: 0.8.5
  References: [#2880](https://www.sqlalchemy.org/trac/ticket/2880), [#2964](https://www.sqlalchemy.org/trac/ticket/2964)

### sql

- Fixed bug where calling [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) with an empty list
  or tuple would raise an IndexError.   It now produces an empty
  insert construct as would be the case with an empty dictionary.
  This change is also **backported** to: 0.8.5
  References: [#2944](https://www.sqlalchemy.org/trac/ticket/2944)
- Fixed bug where [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) would go into an endless
  loop if erroneously passed a column expression whose comparator
  included the `__getitem__()` method, such as a column that uses the
  [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type.
  This change is also **backported** to: 0.8.5
  References: [#2957](https://www.sqlalchemy.org/trac/ticket/2957)
- Fixed regression in new “naming convention” feature where conventions
  would fail if the referred table in a foreign key contained a schema
  name.  Pull request courtesy Thomas Farvour.
- Fixed bug where so-called “literal render” of [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
  constructs would fail if the bind were constructed with a callable,
  rather than a direct value.  This prevented ORM expressions
  from being rendered with the “literal_binds” compiler flag.

### postgresql

- Added the [TypeEngine.python_type](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.python_type) convenience accessor onto the
  [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type.  Pull request courtesy Alexey Terentev.
- Added an additional message to psycopg2 disconnect detection,
  “could not send data to server”, which complements the existing
  “could not receive data from server” and has been observed by users.
  This change is also **backported** to: 0.8.5
  References: [#2936](https://www.sqlalchemy.org/trac/ticket/2936)
- > Support has been improved for PostgreSQL reflection behavior on very old
  > (pre 8.1) versions of PostgreSQL, and potentially other PG engines
  > such as Redshift (assuming Redshift reports the version as < 8.1).
  > The query for “indexes” as well as “primary keys” relies upon inspecting
  > a so-called “int2vector” datatype, which refuses to coerce to an array
  > prior to 8.1 causing failures regarding the “ANY()” operator used
  > in the query.  Extensive googling has located the very hacky, but
  > recommended-by-PG-core-developer query to use when PG version < 8.1
  > is in use, so index and primary key constraint reflection now work
  > on these versions.
  This change is also **backported** to: 0.8.5
- Revised this very old issue where the PostgreSQL “get primary key”
  reflection query were updated to take into account primary key constraints
  that were renamed; the newer query fails on very old versions of
  PostgreSQL such as version 7, so the old query is restored in those cases
  when server_version_info < (8, 0) is detected.
  This change is also **backported** to: 0.8.5
  References: [#2291](https://www.sqlalchemy.org/trac/ticket/2291)
- Added server version detection to the newly added dialect startup
  query for  “show standard_conforming_strings”; as this variable was
  added as of PG 8.2, we skip the query for PG versions who report a
  version string earlier than that.
  References: [#2946](https://www.sqlalchemy.org/trac/ticket/2946)

### mysql

- Added new MySQL-specific [DATETIME](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.DATETIME) which includes
  fractional seconds support; also added fractional seconds support
  to [TIMESTAMP](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TIMESTAMP).  DBAPI support is limited, though
  fractional seconds are known to be supported by MySQL Connector/Python.
  Patch courtesy Geert JM Vanderkelen.
  This change is also **backported** to: 0.8.5
  References: [#2941](https://www.sqlalchemy.org/trac/ticket/2941)
- Added support for the `PARTITION BY` and `PARTITIONS`
  MySQL table keywords, specified as `mysql_partition_by='value'` and
  `mysql_partitions='value'` to [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).  Pull request
  courtesy Marcus McCurdy.
  This change is also **backported** to: 0.8.5
  References: [#2966](https://www.sqlalchemy.org/trac/ticket/2966)
- Fixed bug which prevented MySQLdb-based dialects (e.g.
  pymysql) from working in Py3K, where a check for “connection
  charset” would fail due to Py3K’s more strict value comparison
  rules.  The call in question  wasn’t taking the database
  version into account in any case as the server version was
  still None at that point, so the method overall has been
  simplified to rely upon connection.character_set_name().
  This change is also **backported** to: 0.8.5
  References: [#2933](https://www.sqlalchemy.org/trac/ticket/2933)
- Fixed bug in cymysql dialect where a version string such as
  `'33a-MariaDB'` would fail to parse properly.  Pull request
  courtesy Matt Schmidt.
  References: [#2934](https://www.sqlalchemy.org/trac/ticket/2934)

### sqlite

- The SQLite dialect will now skip unsupported arguments when reflecting
  types; such as if it encounters a string like `INTEGER(5)`, the
  [INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER) type will be instantiated without the “5” being included,
  based on detecting a `TypeError` on the first attempt.
- Support has been added to SQLite type reflection to fully support
  the “type affinity” contract specified at [https://www.sqlite.org/datatype3.html](https://www.sqlite.org/datatype3.html).
  In this scheme, keywords like `INT`, `CHAR`, `BLOB` or
  `REAL` located in the type name generically associate the type with
  one of five affinities.  Pull request courtesy Erich Blume.
  See also
  [Type Reflection](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-type-reflection)

### misc

- Fixed bug where the [AutomapBase](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#sqlalchemy.ext.automap.AutomapBase) class of the
  new automap extension would fail if classes
  were pre-arranged in single or potentially joined inheritance patterns.
  The repaired joined inheritance issue could also potentially apply when
  using [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) as well.

## 0.9.2

Released: February 2, 2014

### orm

- Added a new parameter [Operators.op.is_comparison](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.is_comparison).  This
  flag allows a custom op from [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) to be considered
  as a “comparison” operator, thus usable for custom
  [relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin) conditions.
  See also
  [Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-operator)
- Support is improved for supplying a [join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.join) construct as the
  target of [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) for the purposes
  of creating very complex [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) join conditions.
  The change includes adjustments to query joining, joined eager loading
  to not render a SELECT subquery, changes to lazy loading such that
  the “secondary” target is properly included in the SELECT, and
  changes to declarative to better support specification of a
  join() object with classes as targets.
  The new use case is somewhat experimental, but a new documentation section
  has been added.
  See also
  [Composite “Secondary” Joins](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#composite-secondary-join)
- Fixed error message when an iterator object is passed to
  [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper) or similar, where the error would fail to
  render on string formatting.  Pullreq courtesy Kyle Stark.
  This change is also **backported** to: 0.8.5
- Fixed bug in new `TextAsFrom` construct where [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)-
  oriented row lookups were not matching up to the ad-hoc [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause)
  objects that `TextAsFrom` generates, thereby making it not
  usable as a target in [Query.from_statement()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.from_statement).  Also fixed
  [Query.from_statement()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.from_statement) mechanics to not mistake a `TextAsFrom`
  for a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct.  This bug is also an 0.9 regression
  as the [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method is called to accommodate the
  [text.typemap](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text.params.typemap) argument.
  References: [#2932](https://www.sqlalchemy.org/trac/ticket/2932)
- Added a new directive used within the scope of an attribute “set” operation
  to disable autoflush, in the case that the attribute needs to lazy-load
  the “old” value, as in when replacing one-to-one values or some
  kinds of many-to-one.  A flush at this point otherwise occurs
  at the point that the attribute is None and can cause NULL violations.
  References: [#2921](https://www.sqlalchemy.org/trac/ticket/2921)
- Fixed an 0.9 regression where the automatic aliasing applied by
  [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) and in other situations where selects or joins
  were aliased (such as joined table inheritance) could fail if a
  user-defined [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) subclass were used in the expression.
  In this case, the subclass would fail to propagate ORM-specific
  “annotations” along needed by the adaptation.  The “expression
  annotations” system has been corrected to account for this case.
  References: [#2918](https://www.sqlalchemy.org/trac/ticket/2918)
- Fixed a bug involving the new flattened JOIN structures which
  are used with [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload) (thereby causing a regression
  in joined eager loading) as well as [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
  in conjunction with the `flat=True` flag and joined-table inheritance;
  basically multiple joins across a “parent JOIN sub” entity using different
  paths to get to a target class wouldn’t form the correct ON conditions.
  An adjustment / simplification made in the mechanics of figuring
  out the “left side” of the join in the case of an aliased, joined-inh
  class repairs the issue.
  References: [#2908](https://www.sqlalchemy.org/trac/ticket/2908)

### examples

- Added a tweak to the “history_meta” example where the check for
  “history” on a relationship-bound attribute will now no longer emit
  any SQL if the relationship is unloaded.

### engine

- Added a new pool event [PoolEvents.invalidate()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.invalidate).  Called when
  a DBAPI connection is to be marked as “invalidated” and discarded
  from the pool.

### sql

- Added [MetaData.reflect.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect.params.dialect_kwargs)
  to support dialect-level reflection options for all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  objects reflected.
- Added a new feature which allows automated naming conventions to be
  applied to [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) and [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) objects.  Based
  on a recipe in the wiki, the new feature uses schema-events to set up
  names as various schema objects are associated with each other.  The
  events then expose a configuration system through a new argument
  [MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention).  This system allows production
  of both simple and custom naming schemes for constraints and indexes
  on a per-[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) basis.
  See also
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
  References: [#2923](https://www.sqlalchemy.org/trac/ticket/2923)
- Options can now be specified on a [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) object
  independently of the specification of columns in the table with
  the `primary_key=True` flag; use a [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint)
  object with no columns in it to achieve this result.
  Previously, an explicit [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) would have the
  effect of those columns marked as `primary_key=True` being ignored;
  since this is no longer the case, the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint)
  will now assert that either one style or the other is used to specify
  the columns, or if both are present, that the column lists match
  exactly.  If an inconsistent set of columns in the
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint)
  and within the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) marked as `primary_key=True` are
  present, a warning is emitted, and the list of columns is taken
  only from the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) alone as was the case
  in previous releases.
  See also
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint)
  References: [#2910](https://www.sqlalchemy.org/trac/ticket/2910)
- The system by which schema constructs and certain SQL constructs
  accept dialect-specific keyword arguments has been enhanced.  This
  system includes commonly the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) constructs,
  which accept a wide variety of dialect-specific arguments such as
  `mysql_engine` and `postgresql_where`, as well as the constructs
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint), [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete), and also
  newly added kwarg capability to [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  and [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey).  The change is that participating dialects
  can now specify acceptable argument lists for these constructs, allowing
  an argument error to be raised if an invalid keyword is specified for
  a particular dialect.  If the dialect portion of the keyword is unrecognized,
  a warning is emitted only; while the system will actually make use
  of setuptools entrypoints in order to locate non-local dialects,
  the use case where certain dialect-specific arguments are used
  in an environment where that third-party dialect is uninstalled remains
  supported.  Dialects also have to explicitly opt-in to this system,
  so that external dialects which aren’t making use of this system
  will remain unaffected.
  References: [#2866](https://www.sqlalchemy.org/trac/ticket/2866)
- The behavior of [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) has been adjusted such that
  the schema target of a [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) will not be changed unless
  that schema matches that of the parent table.  That is, if
  a table “schema_a.user” has a foreign key to “schema_b.order.id”,
  the “schema_b” target will be maintained whether or not the
  “schema” argument is passed to [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata).  However
  if a table “schema_a.user” refers to “schema_a.order.id”, the presence
  of “schema_a” will be updated on both the parent and referred tables.
  This is a behavioral change hence isn’t likely to be backported to
  0.8; it is assumed that the previous behavior is pretty buggy
  however and that it’s unlikely anyone was relying upon it.
  Additionally, a new parameter has been added
  [Table.tometadata.referred_schema_fn](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata.params.referred_schema_fn).  This refers to a
  callable function which will be used to determine the new referred
  schema for any [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) encountered in the
  tometadata operation.  This callable can be used to revert to the
  previous behavior or to customize how referred schemas are treated
  on a per-constraint basis.
  References: [#2913](https://www.sqlalchemy.org/trac/ticket/2913)
- Fixed bug whereby binary type would fail in some cases
  if used with a “test” dialect, such as a DefaultDialect or other
  dialect with no DBAPI.
- Fixed bug where “literal binds” wouldn’t work with a bound parameter
  that’s a binary type.  A similar, but different, issue is fixed
  in 0.8.
- Fixed regression whereby the “annotation” system used by the ORM was leaking
  into the names used by standard functions in `sqlalchemy.sql.functions`,
  such as `func.coalesce()` and `func.max()`.  Using these functions
  in ORM attributes and thus producing annotated versions of them could
  corrupt the actual function name rendered in the SQL.
  References: [#2927](https://www.sqlalchemy.org/trac/ticket/2927)
- Fixed 0.9 regression where the new sortable support for `RowProxy`
  would lead to `TypeError` when compared to non-tuple types as it attempted
  to apply tuple() to the “other” object unconditionally.  The
  full range of Python comparison operators have now been implemented on
  `RowProxy`, using an approach that guarantees a comparison
  system that is equivalent to that of a tuple, and the “other” object
  is only coerced if it’s an instance of RowProxy.
  References: [#2848](https://www.sqlalchemy.org/trac/ticket/2848), [#2924](https://www.sqlalchemy.org/trac/ticket/2924)
- A [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) created inline with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  that has no columns within it will be skipped.  Pullreq courtesy
  Derek Harland.
- Fixed the multiple-table “UPDATE..FROM” construct, only usable on
  MySQL, to correctly render the SET clause among multiple columns
  with the same name across tables.  This also changes the name used for
  the bound parameter in the SET clause to “<tablename>_<colname>” for
  the non-primary table only; as this parameter is typically specified
  using the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object directly this should not have an
  impact on applications.   The fix takes effect for both
  [Table.update()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.update) as well as [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) in the ORM.
  References: [#2912](https://www.sqlalchemy.org/trac/ticket/2912)

### schema

- Restored `sqlalchemy.schema.SchemaVisitor` to the `.schema`
  module.  Pullreq courtesy Sean Dague.

### postgresql

- Added a new dialect-level argument `postgresql_ignore_search_path`;
  this argument is accepted by both the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) constructor
  as well as by the [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) method.  When in use
  against PostgreSQL, a foreign-key referenced table which specifies
  a remote schema name will retain that schema name even if the name
  is present in the `search_path`; the default behavior since 0.7.3
  has been that schemas present in `search_path` would not be copied
  to reflected [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects.  The documentation has been
  updated to describe in detail the behavior of the `pg_get_constraintdef()`
  function and how the `postgresql_ignore_search_path` feature essentially
  determines if we will honor the schema qualification reported by
  this function or not.
  See also
  [Remote-Schema Table Introspection and PostgreSQL search_path](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-schema-reflection)
  References: [#2922](https://www.sqlalchemy.org/trac/ticket/2922)

### mysql

- Some missing methods added to the cymysql dialect, including
  _get_server_version_info() and _detect_charset().  Pullreq
  courtesy Hajime Nakagami.
  This change is also **backported** to: 0.8.5
- Added new test coverage for so-called “down adaptions” of SQL types,
  where a more specific type is adapted to a more generic one - this
  use case is needed by some third party tools such as `sqlacodegen`.
  The specific cases that needed repair within this test suite were that
  of [ENUM](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.ENUM) being downcast into a [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum),
  and that of SQLite date types being cast into generic date types.
  The `adapt()` method needed to become more specific here to counteract
  the removal of a “catch all” `**kwargs` collection on the base
  [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class that was removed in 0.9.
  References: [#2917](https://www.sqlalchemy.org/trac/ticket/2917)
- The MySQL CAST compilation now takes into account aspects of a string
  type such as “charset” and “collation”.  While MySQL wants all character-
  based CAST calls to use the CHAR type, we now create a real CHAR
  object at CAST time and copy over all the parameters it has, so that
  an expression like `cast(x, mysql.TEXT(charset='utf8'))` will
  render `CAST(t.col AS CHAR CHARACTER SET utf8)`.
- Added new “unicode returns” detection to the MySQL dialect and
  to the default dialect system overall, such that any dialect
  can add extra “tests” to the on-first-connect “does this DBAPI
  return unicode directly?” detection. In this case, we are
  adding a check specifically against the “utf8” encoding with
  an explicit “utf8_bin” collation type (after checking that
  this collation is available) to test for some buggy unicode
  behavior observed with MySQLdb version 1.2.3.  While MySQLdb
  has resolved this issue as of 1.2.4, the check here should
  guard against regressions.  The change also allows the “unicode”
  checks to log in the engine logs, which was not previously
  the case.
  References: [#2906](https://www.sqlalchemy.org/trac/ticket/2906)
- [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) now associates a new
  [RootTransaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.RootTransaction) or [TwoPhaseTransaction](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction)
  with its immediate [_ConnectionFairy](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool._ConnectionFairy) as a “reset handler”
  for the span of that transaction, which takes over the task
  of calling commit() or rollback() for the “reset on return” behavior
  of [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool) if the transaction was not otherwise completed.
  This resolves the issue that a picky transaction
  like that of MySQL two-phase will be
  properly closed out when the connection is closed without an
  explicit rollback or commit (e.g. no longer raises “XAER_RMFAIL”
  in this case - note this only shows up in logging as the exception
  is not propagated within pool reset).
  This issue would arise e.g. when using an orm
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with `twophase` set, and then
  [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) is called without an explicit rollback or
  commit.   The change also has the effect that you will now see
  an explicit “ROLLBACK” in the logs when using a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  object in non-autocommit mode regardless of how that session was
  discarded.  Thanks to Jeff Dairiki and Laurence Rowe for isolating
  the issue here.
  References: [#2907](https://www.sqlalchemy.org/trac/ticket/2907)

### sqlite

- Fixed bug whereby SQLite compiler failed to propagate compiler arguments
  such as “literal binds” into a CAST expression.

### mssql

- Added an option `mssql_clustered` to the [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint)
  and [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) constructs; on SQL Server, this adds
  the `CLUSTERED` keyword to the constraint construct within DDL.
  Pullreq courtesy Derek Harland.

### oracle

- It’s been observed that the usage of a cx_Oracle “outputtypehandler”
  in Python 2.xx in order to coerce string values to Unicode is inordinately
  expensive; even though cx_Oracle is written in C, when you pass the
  Python `unicode` primitive to cursor.var() and associate with an output
  handler, the library counts every conversion as a Python function call
  with all the requisite overhead being recorded; this *despite* the fact
  when running in Python 3, all strings are also unconditionally coerced
  to unicode but it does *not* incur this overhead,
  meaning that cx_Oracle is failing to use performant techniques in Py2K.
  As SQLAlchemy cannot easily select for this style of type handler on a
  per-column basis, the handler was assembled unconditionally thereby
  adding the overhead to all string access.
  So this logic has been replaced with SQLAlchemy’s own unicode
  conversion system, which now
  only takes effect in Py2K for columns that are requested as unicode.
  When C extensions are used, SQLAlchemy’s system appears to be 2-3x faster than
  cx_Oracle’s.  Additionally, SQLAlchemy’s unicode conversion has been
  enhanced such that when the “conditional” converter is required
  (now needed for the Oracle backend), the check for “already unicode” is now
  performed in C and no longer introduces significant overhead.
  This change has two impacts on the cx_Oracle backend.  One is that
  string values in Py2K which aren’t specifically requested with the
  Unicode type or convert_unicode=True will now come back as `str`,
  not `unicode` - this behavior is similar to a backend such as
  MySQL.  Additionally, when unicode values are requested with the cx_Oracle
  backend, if the C extensions are *not* used, there is now an additional
  overhead of an isinstance() check per column.  This tradeoff has been
  made as it can be worked around and no longer places a performance burden
  on the likely majority of Oracle result columns that are non-unicode
  strings.
  References: [#2911](https://www.sqlalchemy.org/trac/ticket/2911)

### misc

- The argument names for the [PoolEvents.reset()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.reset) event have been
  renamed to `dbapi_connection` and `connection_record` in order
  to maintain consistency with all the other pool events.  It is expected
  that any existing listeners for this relatively new and
  seldom-used event are using positional style to receive arguments in
  any case.
- Fixed an issue where the C extensions in Py3K are using the wrong API
  to specify the top-level module function, which breaks
  in Python 3.4b2.  Py3.4b2 changes PyMODINIT_FUNC to return
  “void” instead of `PyObject *`, so we now make sure to use
  “PyMODINIT_FUNC” instead of `PyObject *` directly.  Pull request
  courtesy cgohlke.

## 0.9.1

Released: January 5, 2014

### orm

- Fixed regression where using a `functools.partial()` with the event
  system would cause a recursion overflow due to usage of inspect.getargspec()
  on it in order to detect a legacy calling signature for certain events,
  and apparently there’s no way to do this with a partial object.  Instead
  we skip the legacy check and assume the modern style; the check itself
  now only occurs for the SessionEvents.after_bulk_update and
  SessionEvents.after_bulk_delete events.  Those two events will require
  the new signature style if assigned to a “partial” event listener.
  References: [#2905](https://www.sqlalchemy.org/trac/ticket/2905)
- Fixed bug where using new [Session.info](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.info) attribute would fail
  if the `.info` argument were only passed to the [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker)
  creation call but not to the object itself.  Courtesy Robin Schoonover.
- Fixed regression where we don’t check the given name against the
  correct string class when setting up a backref based on a name,
  therefore causing the error “too many values to unpack”.  This was
  related to the Py3k conversion.
  References: [#2901](https://www.sqlalchemy.org/trac/ticket/2901)
- Fixed regression where we apparently still create an implicit
  alias when saying query(B).join(B.cs), where “C” is a joined inh
  class; however, this implicit alias was created only considering
  the immediate left side, and not a longer chain of joins along different
  joined-inh subclasses of the same base.   As long as we’re still
  implicitly aliasing in this case, the behavior is dialed back a bit
  so that it will alias the right side in a wider variety of cases.
  References: [#2903](https://www.sqlalchemy.org/trac/ticket/2903)

### orm declarative

- Fixed an extremely unlikely memory issue where when using
  [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection)
  to define classes pending for reflection, if some subset of those
  classes were discarded before the [DeferredReflection.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection.prepare)
  method were called to reflect and map the class, a strong reference
  to the class would remain held within the declarative internals.
  This internal collection of “classes to map” now uses weak
  references against the classes themselves.
- A quasi-regression where apparently in 0.8 you can set a class-level
  attribute on declarative to simply refer directly to an [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute)
  on a superclass or on the class itself, and it
  acts more or less like a synonym; in 0.9, this fails to set up enough
  bookkeeping to keep up with the more liberalized backref logic
  from [#2789](https://www.sqlalchemy.org/trac/ticket/2789).  Even though this use case was never directly
  considered, it is now detected by declarative at the “setattr()” level
  as well as when setting up a subclass, and the mirrored/renamed attribute
  is now set up as a [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) instead.
  References: [#2900](https://www.sqlalchemy.org/trac/ticket/2900)

### orm extensions

- A new, **experimental** extension [sqlalchemy.ext.automap](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html#module-sqlalchemy.ext.automap) is added.
  This extension expands upon the functionality of Declarative as well as
  the [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) class to produce a base class which
  automatically generates mapped classes *and relationships* based on
  table metadata.
  See also
  [Automap Extension](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-automap)
  [Automap](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html)

### sql

- Conjunctions like [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) and [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_) can now accept
  Python generators as a single argument, e.g.:
  ```
  and_(x == y for x, y in tuples)
  ```
  The logic here looks for a single argument `*args` where the first
  element is an instance of `types.GeneratorType`.

### schema

- The [Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing) and [Table.autoload_replace](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_replace)
  parameters are now available on the [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect)
  method.

## 0.9.0

Released: December 30, 2013

### orm

- The [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) or DBAPI-related subclass
  now can accommodate additional information about the “reason” for
  the exception; the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) now adds some detail to it
  when the exception occurs within an autoflush.  This approach
  is taken as opposed to combining [FlushError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.FlushError) with
  a Python 3 style “chained exception” approach so as to maintain
  compatibility both with Py2K code as well as code that already
  catches `IntegrityError` or similar.
- Added new argument `include_backrefs=True` to the
  [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) function; when set to False, a validation event
  will not be triggered if the event was initiated as a backref to
  an attribute operation from the other side.
  See also
  [include_backrefs=False option for @validates](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-1535)
  References: [#1535](https://www.sqlalchemy.org/trac/ticket/1535)
- A new API for specifying the `FOR UPDATE` clause of a `SELECT`
  is added with the new [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update) method,
  to complement the new [GenerativeSelect.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update) method.
  Pull request courtesy Mario Lassnig.
  See also
  [New FOR UPDATE support on select(), Query()](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-github-42)
- An adjustment to the [subqueryload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.subqueryload) strategy which ensures that
  the query runs after the loading process has begun; this is so that
  the subqueryload takes precedence over other loaders that may be
  hitting the same attribute due to other eager/noload situations
  at the wrong time.
  This change is also **backported** to: 0.8.5
  References: [#2887](https://www.sqlalchemy.org/trac/ticket/2887)
- Fixed bug when using joined table inheritance from a table to a
  select/alias on the base, where the PK columns were also not same
  named; the persistence system would fail to copy primary key values
  from the base table to the inherited table upon INSERT.
  This change is also **backported** to: 0.8.5
  References: [#2885](https://www.sqlalchemy.org/trac/ticket/2885)
- [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) will raise an informative error message when the
  columns/attribute (names) passed don’t resolve to a Column or mapped
  attribute (such as an erroneous tuple); previously raised an unbound
  local.
  This change is also **backported** to: 0.8.5
  References: [#2889](https://www.sqlalchemy.org/trac/ticket/2889)
- Fixed a regression introduced by [#2818](https://www.sqlalchemy.org/trac/ticket/2818) where the EXISTS
  query being generated would produce a “columns being replaced”
  warning for a statement with two same-named columns,
  as the internal SELECT wouldn’t have use_labels set.
  This change is also **backported** to: 0.8.4
  References: [#2818](https://www.sqlalchemy.org/trac/ticket/2818)
- Added support for the Python 3 method `list.clear()` within
  the ORM collection instrumentation system; pull request
  courtesy Eduardo Schettino.
- Some refinements to the [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) construct with regards
  to descriptors, like hybrids, synonyms, composites, user-defined
  descriptors, etc.  The attribute
  adaptation which goes on has been made more robust, such that if a descriptor
  returns another instrumented attribute, rather than a compound SQL
  expression element, the operation will still proceed.
  Additionally, the “adapted” operator will retain its class; previously,
  a change in class from `InstrumentedAttribute` to `QueryableAttribute`
  (a superclass) would interact with Python’s operator system such that
  an expression like `aliased(MyClass.x) > MyClass.x` would reverse itself
  to read `myclass.x < myclass_1.x`.   The adapted attribute will also
  refer to the new [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass) as its parent which was not
  always the case before.
  References: [#2872](https://www.sqlalchemy.org/trac/ticket/2872)
- The `viewonly` flag on [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) will now prevent
  attribute history from being written on behalf of the target attribute.
  This has the effect of the object not being written to the
  Session.dirty list if it is mutated.  Previously, the object would
  be present in Session.dirty, but no change would take place on behalf
  of the modified attribute during flush.   The attribute still emits
  events such as backref events and user-defined events and will still
  receive mutations from backrefs.
  See also
  [viewonly=True on relationship() prevents history from taking effect](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2833)
  References: [#2833](https://www.sqlalchemy.org/trac/ticket/2833)
- Added support for new [Session.info](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.info) attribute to
  [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session).
- Fixed bug where usage of new [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) object would cause
  the [Query.column_descriptions](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.column_descriptions) attribute to fail.
- Fixed a regression introduced by the join rewriting feature of
  [#2369](https://www.sqlalchemy.org/trac/ticket/2369) and [#2587](https://www.sqlalchemy.org/trac/ticket/2587) where a nested join with one side
  already an aliased select would fail to translate the ON clause on the
  outside correctly; in the ORM this could be seen when using a
  SELECT statement as a “secondary” table.
  References: [#2858](https://www.sqlalchemy.org/trac/ticket/2858)

### orm declarative

- Declarative does an extra check to detect if the same
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is mapped multiple times under different properties
  (which typically should be a [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) instead) or if two
  or more [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects are given the same name, raising
  a warning if this condition is detected.
  References: [#2828](https://www.sqlalchemy.org/trac/ticket/2828)
- The [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) class has been enhanced to provide
  automatic reflection support for the “secondary” table referred
  to by a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).   “secondary”, when specified
  either as a string table name, or as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object with
  only a name and [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object will also be included
  in the reflection process when [DeferredReflection.prepare()](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection.prepare)
  is called.
  References: [#2865](https://www.sqlalchemy.org/trac/ticket/2865)
- Fixed bug where in Py2K a unicode literal would not be accepted
  as the string name of a class or other argument within
  declarative using [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

### examples

- Fixed bug which prevented history_meta recipe from working with
  joined inheritance schemes more than one level deep.

### engine

- The [engine_from_config()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine_from_config) function has been improved so that
  we will be able to parse dialect-specific arguments from string
  configuration dictionaries.  Dialect classes can now provide their
  own list of parameter types and string-conversion routines.
  The feature is not yet used by the built-in dialects, however.
  References: [#2875](https://www.sqlalchemy.org/trac/ticket/2875)
- A DBAPI that raises an error on `connect()` which is not a subclass
  of dbapi.Error (such as `TypeError`, `NotImplementedError`, etc.)
  will propagate the exception unchanged.  Previously,
  the error handling specific to the `connect()` routine would both
  inappropriately run the exception through the dialect’s
  [Dialect.is_disconnect()](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect.is_disconnect) routine as well as wrap it in
  a [sqlalchemy.exc.DBAPIError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DBAPIError).  It is now propagated unchanged
  in the same way as occurs within the execute process.
  This change is also **backported** to: 0.8.4
  References: [#2881](https://www.sqlalchemy.org/trac/ticket/2881)
- The [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) has been enhanced to not block new connection
  attempts when an existing connection attempt is blocking.  Previously,
  the production of new connections was serialized within the block
  that monitored overflow; the overflow counter is now altered within
  its own critical section outside of the connection process itself.
  This change is also **backported** to: 0.8.4
  References: [#2880](https://www.sqlalchemy.org/trac/ticket/2880)
- Made a slight adjustment to the logic which waits for a pooled
  connection to be available, such that for a connection pool
  with no timeout specified, it will every half a second break out of
  the wait to check for the so-called “abort” flag, which allows the
  waiter to break out in case the whole connection pool was dumped;
  normally the waiter should break out due to a notify_all() but it’s
  possible this notify_all() is missed in very slim cases.
  This is an extension of logic first introduced in 0.8.0, and the
  issue has only been observed occasionally in stress tests.
  This change is also **backported** to: 0.8.4
  References: [#2522](https://www.sqlalchemy.org/trac/ticket/2522)
- Fixed bug where SQL statement would be improperly ASCII-encoded
  when a pre-DBAPI [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError) were raised within
  [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), causing encoding errors for
  non-ASCII statements.  The stringification now remains within
  Python unicode thus avoiding encoding errors.
  This change is also **backported** to: 0.8.4
  References: [#2871](https://www.sqlalchemy.org/trac/ticket/2871)
- The [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) routine and the related [make_url()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.make_url)
  function no longer considers the `+` sign to be a space within the
  password field. The parsing in this area has been adjusted to match
  more closely to how RFC 1738 handles these tokens, in that both
  `username` and `password` expect only `:`, `@`, and `/` to be
  encoded.
  See also
  [The “password” portion of a create_engine() no longer considers the + sign as an encoded space](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2873)
  References: [#2873](https://www.sqlalchemy.org/trac/ticket/2873)
- The `RowProxy` object is now sortable in Python as a regular
  tuple is; this is accomplished via ensuring tuple() conversion on
  both sides within the `__eq__()` method as well as
  the addition of a `__lt__()` method.
  See also
  [RowProxy now has tuple-sorting behavior](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2848)
  References: [#2848](https://www.sqlalchemy.org/trac/ticket/2848)

### sql

- New improvements to the [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, including
  more flexible ways to set up bound parameters and return types;
  in particular, a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) can now be turned into a full
  FROM-object, embeddable in other statements as an alias or CTE
  using the new method [TextClause.columns()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns).   The [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
  construct can also render “inline” bound parameters when the construct
  is compiled in a “literal bound” context.
  See also
  [New text() Capabilities](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-2877)
  References: [#2877](https://www.sqlalchemy.org/trac/ticket/2877), [#2882](https://www.sqlalchemy.org/trac/ticket/2882)
- A new API for specifying the `FOR UPDATE` clause of a `SELECT`
  is added with the new [GenerativeSelect.with_for_update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect.with_for_update) method.
  This method supports a more straightforward system of setting
  dialect-specific options compared to the `for_update` keyword
  argument of [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), and also includes support for the
  SQL standard `FOR UPDATE OF` clause.   The ORM also includes
  a new corresponding method [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update).
  Pull request courtesy Mario Lassnig.
  See also
  [New FOR UPDATE support on select(), Query()](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-github-42)
- The precision used when coercing a returned floating point value to
  Python `Decimal` via string is now configurable.  The
  flag `decimal_return_scale` is now supported by all [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric)
  and [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) types, which will ensure this many digits are taken
  from the native floating point value when it is converted to string.
  If not present, the type will make use of the value of `.scale`, if
  the type supports this setting and it is non-None.  Otherwise the original
  default length of 10 is used.
  See also
  [Floating Point String-Conversion Precision Configurable for Native Floating Point Types](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-2867)
  References: [#2867](https://www.sqlalchemy.org/trac/ticket/2867)
- Fixed issue where a primary key column that has a Sequence on it,
  yet the column is not the “auto increment” column, either because
  it has a foreign key constraint or `autoincrement=False` set,
  would attempt to fire the Sequence on INSERT for backends that don’t
  support sequences, when presented with an INSERT missing the primary
  key value.  This would take place on non-sequence backends like
  SQLite, MySQL.
  This change is also **backported** to: 0.8.5
  References: [#2896](https://www.sqlalchemy.org/trac/ticket/2896)
- Fixed bug with [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) method where the order
  of the given names would not be taken into account when generating
  the INSERT statement, thus producing a mismatch versus the column
  names in the given SELECT statement.  Also noted that
  [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) implies that Python-side insert defaults
  cannot be used, since the statement has no VALUES clause.
  This change is also **backported** to: 0.8.5
  References: [#2895](https://www.sqlalchemy.org/trac/ticket/2895)
- The [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) function, when given a plain literal value,
  will now apply the given type to the given literal value on the
  bind parameter side according to the type given to the cast,
  in the same manner as that of the [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) function.
  However unlike [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), this only takes effect if a
  non-clauseelement value is passed to [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast); an existing typed
  construct will retain its type.
- The [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) class more aggressively checks the given
  column argument.   If not a string, it checks that the object is
  at least a [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause), or an object that resolves to one,
  and that the `.table` attribute, if present, refers to a
  [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause) or subclass, and not something like an
  [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias).  Otherwise, a [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.
  References: [#2883](https://www.sqlalchemy.org/trac/ticket/2883)
- The precedence rules for the [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) operator
  have been modified, such that the COLLATE operator is now of lower
  precedence than the comparison operators.  This has the effect that
  a COLLATE applied to a comparison will not render parenthesis
  around the comparison, which is not parsed by backends such as
  MSSQL.  The change is backwards incompatible for those setups that
  were working around the issue by applying `Operators.collate()`
  to an individual element of the comparison expression,
  rather than the comparison expression as a whole.
  See also
  [The precedence rules for COLLATE have been changed](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2879)
  References: [#2879](https://www.sqlalchemy.org/trac/ticket/2879)
- The exception raised when a [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) is present
  in a compiled statement without a value now includes the key name
  of the bound parameter in the error message.
  This change is also **backported** to: 0.8.5

### schema

- Fixed a regression caused by [#2812](https://www.sqlalchemy.org/trac/ticket/2812) where the repr() for
  table and column names would fail if the name contained non-ascii
  characters.
  References: [#2868](https://www.sqlalchemy.org/trac/ticket/2868)

### postgresql

- Support for PostgreSQL JSON has been added, using the new
  [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) type.   Huge thanks to Nathan Rice for
  implementing and testing this.
  References: [#2581](https://www.sqlalchemy.org/trac/ticket/2581)
- Added support for PostgreSQL TSVECTOR via the
  [TSVECTOR](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.TSVECTOR) type.  Pull request courtesy
  Noufal Ibrahim.
- Fixed bug where index reflection would mis-interpret indkey values
  when using the pypostgresql adapter, which returns these values
  as lists vs. psycopg2’s return type of string.
  This change is also **backported** to: 0.8.4
  References: [#2855](https://www.sqlalchemy.org/trac/ticket/2855)
- Now using psycopg2 UNICODEARRAY extension for handling unicode arrays
  with psycopg2 + normal “native unicode” mode, in the same way the
  UNICODE extension is used.
- Fixed bug where values within an ENUM weren’t escaped for single
  quote signs.   Note that this is backwards-incompatible for existing
  workarounds that manually escape the single quotes.
  See also
  [PostgreSQL CREATE TYPE <x> AS ENUM now applies quoting to values](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2878)
  References: [#2878](https://www.sqlalchemy.org/trac/ticket/2878)

### mysql

- Improvements to the system by which SQL types generate within
  `__repr__()`, particularly with regards to the MySQL integer/numeric/
  character types which feature a wide variety of keyword arguments.
  The `__repr__()` is important for use with Alembic autogenerate
  for when Python code is rendered in a migration script.
  References: [#2893](https://www.sqlalchemy.org/trac/ticket/2893)

### mssql

- The “asdecimal” flag used with the [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) type will now
  work with Firebird as well as the mssql+pyodbc dialects; previously the
  decimal conversion was not occurring.
  This change is also **backported** to: 0.8.5
- Added “Net-Lib error during Connection reset by peer” message
  to the list of messages checked for “disconnect” within the
  pymssql dialect.  Courtesy John Anderson.
  This change is also **backported** to: 0.8.5
- Fixed bug introduced in 0.8.0 where the `DROP INDEX`
  statement for an index in MSSQL would render incorrectly if the
  index were in an alternate schema; the schemaname/tablename
  would be reversed.  The format has been also been revised to
  match current MSSQL documentation.  Courtesy Derek Harland.
  This change is also **backported** to: 0.8.4

### oracle

- Added ORA-02396 “maximum idle time” error code to list of
  “is disconnect” codes with cx_oracle.
  This change is also **backported** to: 0.8.4
  References: [#2864](https://www.sqlalchemy.org/trac/ticket/2864)
- Fixed bug where Oracle `VARCHAR` types given with no length
  (e.g. for a `CAST` or similar) would incorrectly render `None CHAR`
  or similar.
  This change is also **backported** to: 0.8.4
  References: [#2870](https://www.sqlalchemy.org/trac/ticket/2870)

### misc

- The firebird dialect will quote identifiers which begin with an
  underscore.  Courtesy Treeve Jelbert.
  This change is also **backported** to: 0.8.5
  References: [#2897](https://www.sqlalchemy.org/trac/ticket/2897)
- Fixed bug in Firebird index reflection where the columns within the
  index were not sorted correctly; they are now sorted
  in order of RDB$FIELD_POSITION.
  This change is also **backported** to: 0.8.5
- Error message when a string arg sent to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) which
  doesn’t resolve to a class or mapper has been corrected to work
  the same way as when a non-string arg is received, which indicates
  the name of the relationship which had the configurational error.
  This change is also **backported** to: 0.8.5
  References: [#2888](https://www.sqlalchemy.org/trac/ticket/2888)
- Fixed bug which prevented the `serializer` extension from working
  correctly with table or column names that contain non-ASCII
  characters.
  This change is also **backported** to: 0.8.4
  References: [#2869](https://www.sqlalchemy.org/trac/ticket/2869)
- Changed the queries used by Firebird to list table and view names
  to query from the `rdb$relations` view instead of the
  `rdb$relation_fields` and `rdb$view_relations` views.
  Variants of both the old and new queries are mentioned on many
  FAQ and blogs, however the new queries are taken straight from
  the “Firebird FAQ” which appears to be the most official source
  of info.
  References: [#2898](https://www.sqlalchemy.org/trac/ticket/2898)
- The “informix” and “informixdb” dialects have been removed; the code
  is now available as a separate repository on Bitbucket.   The IBM-DB
  project has provided production-level Informix support since the
  informixdb dialect was first added.

## 0.9.0b1

Released: October 26, 2013

### general

- The C extensions are ported to Python 3 and will build under
  any supported CPython 2 or 3 environment.
  References: [#2161](https://www.sqlalchemy.org/trac/ticket/2161)
- The codebase is now “in-place” for Python
  2 and 3, the need to run 2to3 has been removed.
  Compatibility is now against Python 2.6 on forward.
  References: [#2671](https://www.sqlalchemy.org/trac/ticket/2671)
- A large refactoring of packages has reorganized
  the import structure of many Core modules as well as some aspects
  of the ORM modules.  In particular `sqlalchemy.sql` has been broken
  out into several more modules than before so that the very large size
  of `sqlalchemy.sql.expression` is now pared down.   The effort
  has focused on a large reduction in import cycles.   Additionally,
  the system of API functions in `sqlalchemy.sql.expression` and
  `sqlalchemy.orm` has been reorganized to eliminate redundancy
  in documentation between the functions vs. the objects they produce.

### orm

- Added new option to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) `distinct_target_key`.
  This enables the subquery eager loader strategy to apply a DISTINCT
  to the innermost SELECT subquery, to assist in the case where
  duplicate rows are generated by the innermost query which corresponds
  to this relationship (there’s not yet a general solution to the issue
  of dupe rows within subquery eager loading, however, when joins outside
  of the innermost subquery produce dupes).  When the flag
  is set to `True`, the DISTINCT is rendered unconditionally, and when
  it is set to `None`, DISTINCT is rendered if the innermost relationship
  targets columns that do not comprise a full primary key.
  The option defaults to False in 0.8 (e.g. off by default in all cases),
  None in 0.9 (e.g. automatic by default).   Thanks to Alexander Koval
  for help with this.
  See also
  [Subquery Eager Loading will apply DISTINCT to the innermost SELECT for some queries](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2836)
  This change is also **backported** to: 0.8.3
  References: [#2836](https://www.sqlalchemy.org/trac/ticket/2836)
- The association proxy now returns `None` when fetching a scalar
  attribute off of a scalar relationship, where the scalar relationship
  itself points to `None`, instead of raising an `AttributeError`.
  See also
  [Association Proxy Missing Scalar returns None](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2810)
  References: [#2810](https://www.sqlalchemy.org/trac/ticket/2810)
- Added new method [AttributeState.load_history()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeState.load_history), works like
  [AttributeState.history](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeState.history) but also fires loader callables.
  See also
  [attributes.get_history() will query from the DB by default if value not present](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2787)
  References: [#2787](https://www.sqlalchemy.org/trac/ticket/2787)
- Added a new load option [load_only()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.load_only).  This allows a series
  of column names to be specified as loading “only” those attributes,
  deferring the rest.
  References: [#1418](https://www.sqlalchemy.org/trac/ticket/1418)
- The system of loader options has been entirely rearchitected to build
  upon a much more comprehensive base, the [Load](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.Load) object.  This
  base allows any common loader option like [joinedload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload),
  [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer), etc. to be used in a “chained” style for the purpose
  of specifying options down a path, such as `joinedload("foo").subqueryload("bar")`.
  The new system supersedes the usage of dot-separated path names,
  multiple attributes within options, and the usage of `_all()` options.
  See also
  [New Query Options API; load_only() option](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-1418)
  References: [#1418](https://www.sqlalchemy.org/trac/ticket/1418)
- The [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) construct now maintains the return object
  when used in a column-oriented [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query), rather than expanding
  out into individual columns.  This makes use of the new [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle)
  feature internally.  This behavior is backwards incompatible; to
  select from a composite column which will expand out, use
  `MyClass.some_composite.clauses`.
  See also
  [Composite attributes are now returned as their object form when queried on a per-attribute basis](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2824)
  References: [#2824](https://www.sqlalchemy.org/trac/ticket/2824)
- A new construct [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) is added, which allows for specification
  of groups of column expressions to a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) construct.
  The group of columns are returned as a single tuple by default.  The
  behavior of [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) can be overridden however to provide
  any sort of result processing to the returned row.  The behavior
  of [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) is also embedded into composite attributes now
  when they are used in a column-oriented [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query).
  See also
  [Column Bundles for ORM queries](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2824)
  [Composite attributes are now returned as their object form when queried on a per-attribute basis](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2824)
  References: [#2824](https://www.sqlalchemy.org/trac/ticket/2824)
- The `version_id_generator` parameter of `Mapper` can now be specified
  to rely upon server generated version identifiers, using triggers
  or other database-provided versioning features, or via an optional programmatic
  value, by setting `version_id_generator=False`.
  When using a server-generated version identifier, the ORM will use RETURNING when
  available to immediately
  load the new version value, else it will emit a second SELECT.
  References: [#2793](https://www.sqlalchemy.org/trac/ticket/2793)
- The `eager_defaults` flag of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) will now allow the
  newly generated default values to be fetched using an inline
  RETURNING clause, rather than a second SELECT statement, for backends
  that support RETURNING.
  References: [#2793](https://www.sqlalchemy.org/trac/ticket/2793)
- Added a new attribute [Session.info](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.info) to [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session);
  this is a dictionary where applications can store arbitrary
  data local to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
  The contents of [Session.info](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.info) can be also be initialized
  using the `info` argument of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or
  [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker).
- Removal of event listeners is now implemented.    The feature is
  provided via the [remove()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.remove) function.
  See also
  [Event Removal API](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-2268)
  References: [#2268](https://www.sqlalchemy.org/trac/ticket/2268)
- The mechanism by which attribute events pass along an
  `AttributeImpl` as an “initiator” token has been changed;
  the object is now an event-specific object called `Event`.
  Additionally, the attribute system no longer halts events based
  on a matching “initiator” token; this logic has been moved to be
  specific to ORM backref event handlers, which are the typical source
  of the re-propagation of an attribute event onto subsequent append/set/remove
  operations.  End user code which emulates the behavior of backrefs
  must now ensure that recursive event propagation schemes are halted,
  if the scheme does not use the backref handlers.   Using this new system,
  backref handlers can now perform a
  “two-hop” operation when an object is appended to a collection,
  associated with a new many-to-one, de-associated with the previous
  many-to-one, and then removed from a previous collection.   Before this
  change, the last step of removal from the previous collection would
  not occur.
  See also
  [Backref handlers can now propagate more than one level deep](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2789)
  References: [#2789](https://www.sqlalchemy.org/trac/ticket/2789)
- A major change regarding how the ORM constructs joins where
  the right side is itself a join or left outer join.   The ORM
  is now configured to allow simple nesting of joins of
  the form `a JOIN (b JOIN c ON b.id=c.id) ON a.id=b.id`,
  rather than forcing the right side into a `SELECT` subquery.
  This should allow significant performance improvements on most
  backends, most particularly MySQL.   The one database backend
  that has for many years held back this change, SQLite, is now addressed by
  moving the production of the `SELECT` subquery from the
  ORM to the SQL compiler; so that a right-nested join on SQLite will still
  ultimately render with a `SELECT`, while all other backends
  are no longer impacted by this workaround.
  As part of this change, a new argument `flat=True` has been added
  to the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased), `Join.alias()`, and
  [with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) functions, which allows an “alias” of a
  JOIN to be produced which applies an anonymous alias to each component
  table within the join, rather than producing a subquery.
  See also
  [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped in (SELECT * FROM ..) AS ANON_1](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-joins-09)
  References: [#2587](https://www.sqlalchemy.org/trac/ticket/2587)
- Fixed bug where list instrumentation would fail to represent a
  setslice of `[0:0]` correctly, which in particular could occur
  when using `insert(0, item)` with the association proxy.  Due
  to some quirk in Python collections, the issue was much more likely
  with Python 3 rather than 2.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2807](https://www.sqlalchemy.org/trac/ticket/2807)
- Fixed bug where using an annotation such as [remote()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.remote) or
  [foreign()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.foreign) on a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) before association with a parent
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) could produce issues related to the parent table not
  rendering within joins, due to the inherent copy operation performed
  by an annotation.
  This change is also **backported** to: 0.8.3
  References: [#2813](https://www.sqlalchemy.org/trac/ticket/2813)
- Fixed bug where [Query.exists()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.exists) failed to work correctly
  without any WHERE criterion.  Courtesy Vladimir Magamedov.
  This change is also **backported** to: 0.8.3
  References: [#2818](https://www.sqlalchemy.org/trac/ticket/2818)
- Fixed a potential issue in an ordered sequence implementation used
  by the ORM to iterate mapper hierarchies; under the Jython interpreter
  this implementation wasn’t ordered, even though cPython and PyPy
  maintained ordering.
  This change is also **backported** to: 0.8.3
  References: [#2794](https://www.sqlalchemy.org/trac/ticket/2794)
- Fixed bug in ORM-level event registration where the “raw” or
  “propagate” flags could potentially be mis-configured in some
  “unmapped base class” configurations.
  This change is also **backported** to: 0.8.3
  References: [#2786](https://www.sqlalchemy.org/trac/ticket/2786)
- A performance fix related to the usage of the [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer) option
  when loading mapped entities.   The function overhead of applying
  a per-object deferred callable to an instance at load time was
  significantly higher than that of just loading the data from the row
  (note that `defer()` is meant to reduce DB/network overhead, not
  necessarily function call count); the function call overhead is now
  less than that of loading data from the column in all cases.  There
  is also a reduction in the number of “lazy callable” objects created
  per load from N (total deferred values in the result) to 1 (total
  number of deferred cols).
  This change is also **backported** to: 0.8.3
  References: [#2778](https://www.sqlalchemy.org/trac/ticket/2778)
- Fixed bug whereby attribute history functions would fail
  when an object we moved from “persistent” to “pending”
  using the [make_transient()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient) function, for operations
  involving collection-based backrefs.
  This change is also **backported** to: 0.8.3
  References: [#2773](https://www.sqlalchemy.org/trac/ticket/2773)
- A warning is emitted when trying to flush an object of an inherited
  class where the polymorphic discriminator has been assigned
  to a value that is invalid for the class.
  This change is also **backported** to: 0.8.2
  References: [#2750](https://www.sqlalchemy.org/trac/ticket/2750)
- Fixed bug in polymorphic SQL generation where multiple joined-inheritance
  entities against the same base class joined to each other as well
  would not track columns on the base table independently of each other if
  the string of joins were more than two entities long.
  This change is also **backported** to: 0.8.2
  References: [#2759](https://www.sqlalchemy.org/trac/ticket/2759)
- Fixed bug where sending a composite attribute into [Query.order_by()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by)
  would produce a parenthesized expression not accepted by some databases.
  This change is also **backported** to: 0.8.2
  References: [#2754](https://www.sqlalchemy.org/trac/ticket/2754)
- Fixed the interaction between composite attributes and
  the [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) function.  Previously, composite attributes
  wouldn’t work correctly in comparison operations when aliasing
  was applied.
  This change is also **backported** to: 0.8.2
  References: [#2755](https://www.sqlalchemy.org/trac/ticket/2755)
- Fixed bug where [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) didn’t report a change event
  when `clear()` was called.
  This change is also **backported** to: 0.8.2
  References: [#2730](https://www.sqlalchemy.org/trac/ticket/2730)
- [get_history()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_history) when used with a scalar column-mapped
  attribute will now honor the “passive” flag
  passed to it; as this defaults to `PASSIVE_OFF`, the function will
  by default query the database if the value is not present.
  This is a behavioral change vs. 0.8.
  See also
  [attributes.get_history() will query from the DB by default if value not present](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2787)
  References: [#2787](https://www.sqlalchemy.org/trac/ticket/2787)
- Added additional criterion to the ==, != comparators, used with
  scalar values, for comparisons to None to also take into account
  the association record itself being non-present, in addition to the
  existing test for the scalar endpoint on the association record
  being NULL.  Previously, comparing `Cls.scalar == None` would return
  records for which `Cls.associated` were present and
  `Cls.associated.scalar` is None, but not rows for which
  `Cls.associated` is non-present.  More significantly, the
  inverse operation `Cls.scalar != None` *would* return `Cls`
  rows for which `Cls.associated` was non-present.
  The case for `Cls.scalar != 'somevalue'` is also modified
  to act more like a direct SQL comparison; only rows for
  which `Cls.associated` is present and `Associated.scalar`
  is non-NULL and not equal to `'somevalue'` are returned.
  Previously, this would be a simple `NOT EXISTS`.
  Also added a special use case where you
  can call `Cls.scalar.has()` with no arguments,
  when `Cls.scalar` is a column-based value - this returns whether or
  not `Cls.associated` has any rows present, regardless of whether
  or not `Cls.associated.scalar` is NULL or not.
  See also
  [Association Proxy SQL Expression Improvements and Fixes](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2751)
  References: [#2751](https://www.sqlalchemy.org/trac/ticket/2751)
- Fixed an obscure bug where the wrong results would be
  fetched when joining/joinedloading across a many-to-many
  relationship to a single-table-inheriting
  subclass with a specific discriminator value, due to “secondary”
  rows that would come back.  The “secondary” and right-side
  tables are now inner joined inside of parenthesis for all
  ORM joins on many-to-many relationships so that the left->right
  join can accurately filtered.  This change was made possible
  by finally addressing the issue with right-nested joins
  outlined in [#2587](https://www.sqlalchemy.org/trac/ticket/2587).
  See also
  [Many JOIN and LEFT OUTER JOIN expressions will no longer be wrapped in (SELECT * FROM ..) AS ANON_1](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-joins-09)
  References: [#2369](https://www.sqlalchemy.org/trac/ticket/2369)
- The “auto-aliasing” behavior of the [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from)
  method has been turned off.  The specific behavior is now
  available via a new method `Query.select_entity_from()`.
  The auto-aliasing behavior here was never well documented and
  is generally not what’s desired, as [Query.select_from()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from)
  has become more oriented towards controlling how a JOIN is
  rendered.  `Query.select_entity_from()` will also be made
  available in 0.8 so that applications which rely on the auto-aliasing
  can shift their applications to use this method.
  See also
  [_query.Query.select_from() no longer applies the clause to corresponding entities](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2736)
  References: [#2736](https://www.sqlalchemy.org/trac/ticket/2736)

### orm declarative

- Added a convenience class decorator [as_declarative()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.as_declarative), is
  a wrapper for [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) which allows an existing base
  class to be applied using a nifty class-decorated approach.
  This change is also **backported** to: 0.8.3
- ORM descriptors such as hybrid properties can now be referenced
  by name in a string argument used with `order_by`,
  `primaryjoin`, or similar in [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship),
  in addition to column-bound attributes.
  This change is also **backported** to: 0.8.2
  References: [#2761](https://www.sqlalchemy.org/trac/ticket/2761)

### examples

- Improved the examples in `examples/generic_associations`, including
  that `discriminator_on_association.py` makes use of single table
  inheritance do the work with the “discriminator”.  Also
  added a true “generic foreign key” example, which works similarly
  to other popular frameworks in that it uses an open-ended integer
  to point to any other table, foregoing traditional referential
  integrity.  While we don’t recommend this pattern, information wants
  to be free.
  This change is also **backported** to: 0.8.3
- Added “autoincrement=False” to the history table created in the
  versioning example, as this table shouldn’t have autoinc on it
  in any case, courtesy Patrick Schmid.
  This change is also **backported** to: 0.8.3
- Fixed an issue with the “versioning” recipe whereby a many-to-one
  reference could produce a meaningless version for the target,
  even though it was not changed, when backrefs were present.
  Patch courtesy Matt Chisholm.
  This change is also **backported** to: 0.8.2

### engine

- `repr()` for the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) of an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
  will now conceal the password using asterisks.
  Courtesy Gunnlaugur Þór Briem.
  This change is also **backported** to: 0.8.3
  References: [#2821](https://www.sqlalchemy.org/trac/ticket/2821)
- New events added to [ConnectionEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents):
  - [ConnectionEvents.engine_connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.engine_connect)
  - [ConnectionEvents.set_connection_execution_options()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.set_connection_execution_options)
  - [ConnectionEvents.set_engine_execution_options()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.set_engine_execution_options)
  References: [#2770](https://www.sqlalchemy.org/trac/ticket/2770)
- The regexp used by the `make_url()` function now parses
  ipv6 addresses, e.g. surrounded by brackets.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2851](https://www.sqlalchemy.org/trac/ticket/2851)
- Dialect.initialize() is not called a second time if an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
  is recreated, due to a disconnect error.   This fixes a particular
  issue in the Oracle 8 dialect, but in general the dialect.initialize()
  phase should only be once per dialect.
  This change is also **backported** to: 0.8.3
  References: [#2776](https://www.sqlalchemy.org/trac/ticket/2776)
- Fixed bug where [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) would lose the correct
  checked out count if an existing pooled connection failed to reconnect
  after an invalidate or recycle event.
  This change is also **backported** to: 0.8.3
  References: [#2772](https://www.sqlalchemy.org/trac/ticket/2772)
- Fixed bug where the `reset_on_return` argument to various [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
  implementations would not be propagated when the pool was regenerated.
  Courtesy Eevee.
  This change is also **backported** to: 0.8.2
- The method signature of `Dialect.reflecttable()`, which in
  all known cases is provided by [DefaultDialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect), has been
  tightened to expect `include_columns` and `exclude_columns`
  arguments without any kw option, reducing ambiguity - previously
  `exclude_columns` was missing.
  References: [#2748](https://www.sqlalchemy.org/trac/ticket/2748)

### sql

- Added support for “unique constraint” reflection, via the
  [Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints) method.
  Thanks for Roman Podolyaka for the patch.
  This change is also **backported** to: 0.8.4
  References: [#1443](https://www.sqlalchemy.org/trac/ticket/1443)
- The [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update), [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert), and [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs
  will now interpret ORM entities as target tables to be operated upon,
  e.g.:
  ```
  from sqlalchemy import insert, update, delete
  ins = insert(SomeMappedClass).values(x=5)
  del_ = delete(SomeMappedClass).where(SomeMappedClass.id == 5)
  upd = update(SomeMappedClass).where(SomeMappedClass.id == 5).values(name="ed")
  ```
  This change is also **backported** to: 0.8.3
- The PostgreSQL and MySQL dialects now support reflection/inspection
  of foreign key options, including ON UPDATE, ON DELETE.  PostgreSQL
  also reflects MATCH, DEFERRABLE, and INITIALLY.  Courtesy ijl.
  References: [#2183](https://www.sqlalchemy.org/trac/ticket/2183)
- A [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) construct with a “null” type (e.g. no type
  specified) is now copied when used in a typed expression, and the
  new copy is assigned the actual type of the compared column.  Previously,
  this logic would occur on the given [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) in place.
  Additionally, a similar process now occurs for [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) constructs
  passed to [ValuesBase.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.ValuesBase.values) for an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) or
  [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct, within the compilation phase of the
  construct.
  These are both subtle behavioral changes which may impact some
  usages.
  See also
  [A bindparam() construct with no type gets upgraded via copy when a type is available](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2850)
  References: [#2850](https://www.sqlalchemy.org/trac/ticket/2850)
- An overhaul of expression handling for special symbols particularly
  with conjunctions, e.g.
  `None` [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) [true()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.true) [false()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.false), including consistency in rendering NULL
  in conjunctions, “short-circuiting” of [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) and [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_)
  expressions which contain boolean constants, and rendering of
  boolean constants and expressions as compared to “1” or “0” for backends
  that don’t feature `true`/`false` constants.
  See also
  [Improved rendering of Boolean constants, NULL constants, conjunctions](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-2804)
  References: [#2734](https://www.sqlalchemy.org/trac/ticket/2734), [#2804](https://www.sqlalchemy.org/trac/ticket/2804), [#2823](https://www.sqlalchemy.org/trac/ticket/2823)
- The typing system now handles the task of rendering “literal bind” values,
  e.g. values that are normally bound parameters but due to context must
  be rendered as strings, typically within DDL constructs such as
  CHECK constraints and indexes (note that “literal bind” values
  become used by DDL as of [#2742](https://www.sqlalchemy.org/trac/ticket/2742)).  A new method
  [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor) serves as the base, and
  [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param) is added to allow wrapping
  of a native literal rendering method.
  See also
  [The typing system now handles the task of rendering “literal bind” values](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2838)
  References: [#2838](https://www.sqlalchemy.org/trac/ticket/2838)
- The [Table.tometadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.tometadata) method now produces copies of
  all [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) dictionaries from all [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)
  objects within the structure including columns, constraints,
  foreign keys, etc.   As these dictionaries
  are copies, they are independent of the original dictionary.
  Previously, only the `.info` dictionary of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) was transferred
  within this operation, and it was only linked in place, not copied.
  References: [#2716](https://www.sqlalchemy.org/trac/ticket/2716)
- The `default` argument of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) now accepts a class
  or object method as an argument, in addition to a standalone function;
  will properly detect if the “context” argument is accepted or not.
- Added new method to the [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct
  [Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select).  Given a list of columns and
  a selectable, renders `INSERT INTO (table) (columns) SELECT ..`.
  While this feature is highlighted as part of 0.9 it is also
  backported to 0.8.3.
  See also
  [INSERT from SELECT](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#feature-722)
  References: [#722](https://www.sqlalchemy.org/trac/ticket/722)
- Provided a new attribute for [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  called [TypeDecorator.coerce_to_is_types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.coerce_to_is_types),
  to make it easier to control how comparisons using
  `==` or `!=` to `None` and boolean types goes
  about producing an `IS` expression, or a plain
  equality expression with a bound parameter.
  References: [#2734](https://www.sqlalchemy.org/trac/ticket/2734), [#2744](https://www.sqlalchemy.org/trac/ticket/2744)
- A [label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.label) construct will now render as its name alone
  in an `ORDER BY` clause, if that label is also referred to
  in the columns clause of the select, instead of rewriting the
  full expression.  This gives the database a better chance to
  optimize the evaluation of the same expression in two different
  contexts.
  See also
  [Label constructs can now render as their name alone in an ORDER BY](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-1068)
  References: [#1068](https://www.sqlalchemy.org/trac/ticket/1068)
- Fixed regression dating back to 0.7.9 whereby the name of a CTE might
  not be properly quoted if it was referred to in multiple FROM clauses.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2801](https://www.sqlalchemy.org/trac/ticket/2801)
- Fixed bug in common table expression system where if the CTE were
  used only as an `alias()` construct, it would not render using the
  WITH keyword.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2783](https://www.sqlalchemy.org/trac/ticket/2783)
- Fixed bug in [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) DDL where the “quote” flag from a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object would not be propagated.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2784](https://www.sqlalchemy.org/trac/ticket/2784)
- Fixed bug where [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) would not interpret ORM
  elements with a `__clause_element__()` method properly.
  This change is also **backported** to: 0.8.3
  References: [#2849](https://www.sqlalchemy.org/trac/ticket/2849)
- The [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) and [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) types now bypass
  any custom (e.g. TypeDecorator) type in use when producing the
  CHECK constraint for the “non native” type.  This so that the custom type
  isn’t involved in the expression within the CHECK, since this
  expression is against the “impl” value and not the “decorated” value.
  This change is also **backported** to: 0.8.3
  References: [#2842](https://www.sqlalchemy.org/trac/ticket/2842)
- The `.unique` flag on [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) could be produced as `None`
  if it was generated from a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that didn’t specify `unique`
  (where it defaults to `None`).  The flag will now always be `True` or
  `False`.
  This change is also **backported** to: 0.8.3
  References: [#2825](https://www.sqlalchemy.org/trac/ticket/2825)
- Fixed bug in default compiler plus those of postgresql, mysql, and
  mssql to ensure that any literal SQL expression values are
  rendered directly as literals, instead of as bound parameters,
  within a CREATE INDEX statement.  This also changes the rendering
  scheme for other DDL such as constraints.
  This change is also **backported** to: 0.8.3
  References: [#2742](https://www.sqlalchemy.org/trac/ticket/2742)
- A [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) that is made to refer to itself in its FROM clause,
  typically via in-place mutation, will raise an informative error
  message rather than causing a recursion overflow.
  This change is also **backported** to: 0.8.3
  References: [#2815](https://www.sqlalchemy.org/trac/ticket/2815)
- Fixed bug where using the `column_reflect` event to change the `.key`
  of the incoming [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) would prevent primary key constraints,
  indexes, and foreign key constraints from being correctly reflected.
  This change is also **backported** to: 0.8.3
  References: [#2811](https://www.sqlalchemy.org/trac/ticket/2811)
- The [ColumnOperators.notin_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notin_) operator added in 0.8 now properly
  produces the negation of the expression “IN” returns
  when used against an empty collection.
  This change is also **backported** to: 0.8.3
- Fixed bug where the expression system relied upon the `str()`
  form of a some expressions when referring to the `.c` collection
  on a `select()` construct, but the `str()` form isn’t available
  since the element relies on dialect-specific compilation constructs,
  notably the `__getitem__()` operator as used with a PostgreSQL
  `ARRAY` element.  The fix also adds a new exception class
  [UnsupportedCompilationError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnsupportedCompilationError) which is raised in those cases
  where a compiler is asked to compile something it doesn’t know
  how to.
  This change is also **backported** to: 0.8.3
  References: [#2780](https://www.sqlalchemy.org/trac/ticket/2780)
- Multiple fixes to the correlation behavior of
  [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) constructs, first introduced in 0.8.0:
  - To satisfy the use case where FROM entries should be
    correlated outwards to a SELECT that encloses another,
    which then encloses this one, correlation now works
    across multiple levels when explicit correlation is
    established via [Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate), provided
    that the target select is somewhere along the chain
    contained by a WHERE/ORDER BY/columns clause, not
    just nested FROM clauses. This makes
    [Select.correlate()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate) act more compatibly to
    that of 0.7 again while still maintaining the new
    “smart” correlation.
  - When explicit correlation is not used, the usual
    “implicit” correlation limits its behavior to just
    the immediate enclosing SELECT, to maximize compatibility
    with 0.7 applications, and also prevents correlation
    across nested FROMs in this case, maintaining compatibility
    with 0.8.0/0.8.1.
  - The [Select.correlate_except()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate_except) method was not
    preventing the given FROM clauses from correlation in
    all cases, and also would cause FROM clauses to be incorrectly
    omitted entirely (more like what 0.7 would do),
    this has been fixed.
  - Calling select.correlate_except(None) will enter
    all FROM clauses into correlation as would be expected.
  This change is also **backported** to: 0.8.2
  References: [#2668](https://www.sqlalchemy.org/trac/ticket/2668), [#2746](https://www.sqlalchemy.org/trac/ticket/2746)
- Fixed bug whereby joining a select() of a table “A” with multiple
  foreign key paths to a table “B”, to that table “B”, would fail
  to produce the “ambiguous join condition” error that would be
  reported if you join table “A” directly to “B”; it would instead
  produce a join condition with multiple criteria.
  This change is also **backported** to: 0.8.2
  References: [#2738](https://www.sqlalchemy.org/trac/ticket/2738)
- Fixed bug whereby using [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) across a remote
  schema as well as a local schema could produce wrong results
  in the case where both schemas had a table of the same name.
  This change is also **backported** to: 0.8.2
  References: [#2728](https://www.sqlalchemy.org/trac/ticket/2728)
- Removed the “not implemented” `__iter__()` call from the base
  [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators) class, while this was introduced
  in 0.8.0 to prevent an endless, memory-growing loop when one also
  implements a `__getitem__()` method on a custom
  operator and then calls erroneously `list()` on that object,
  it had the effect of causing column elements to report that they
  were in fact iterable types which then throw an error when you try
  to iterate.   There’s no real way to have both sides here so we
  stick with Python best practices.  Careful with implementing
  `__getitem__()` on your custom operators!
  This change is also **backported** to: 0.8.2
  References: [#2726](https://www.sqlalchemy.org/trac/ticket/2726)
- The “name” attribute is set on [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) before the “attach”
  events are called, so that attachment events can be used to dynamically
  generate a name for the index based on the parent table and/or
  columns.
  References: [#2835](https://www.sqlalchemy.org/trac/ticket/2835)
- The erroneous kw arg “schema” has been removed from the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
  object. this was an accidental commit that did nothing; a warning is raised
  in 0.8.3 when this kw arg is used.
  References: [#2831](https://www.sqlalchemy.org/trac/ticket/2831)
- A rework to the way that “quoted” identifiers are handled, in that
  instead of relying upon various `quote=True` flags being passed around,
  these flags are converted into rich string objects with quoting information
  included at the point at which they are passed to common schema constructs
  like [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), etc.   This solves the issue
  of various methods that don’t correctly honor the “quote” flag such
  as `Engine.has_table()` and related methods.  The [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name)
  object is a string subclass that can also be used explicitly if needed;
  the object will hold onto the quoting preferences passed and will
  also bypass the “name normalization” performed by dialects that
  standardize on uppercase symbols, such as Oracle, Firebird and DB2.
  The upshot is that the “uppercase” backends can now work with force-quoted
  names, such as lowercase-quoted names and new reserved words.
  See also
  [Schema identifiers now carry along their own quoting information](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#change-2812)
  References: [#2812](https://www.sqlalchemy.org/trac/ticket/2812)
- The resolution of [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects to their
  target [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) has been reworked to be as
  immediate as possible, based on the moment that the
  target [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is associated with the same
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) as this [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey), rather
  than waiting for the first time a join is constructed,
  or similar. This along with other improvements allows
  earlier detection of some foreign key configuration
  issues.  Also included here is a rework of the
  type-propagation system, so that
  it should be reliable now to set the type as `None`
  on any [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that refers to another via
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) - the type will be copied from the
  target column as soon as that other column is associated,
  and now works for composite foreign keys as well.
  See also
  [Columns can reliably get their type from a column referred to via ForeignKey](https://docs.sqlalchemy.org/en/20/changelog/migration_09.html#migration-1765)
  References: [#1765](https://www.sqlalchemy.org/trac/ticket/1765)

### postgresql

- Support for PostgreSQL 9.2 range types has been added.
  Currently, no type translation is provided, so works
  directly with strings or psycopg2 2.5 range extension types
  at the moment.  Patch courtesy Chris Withers.
  This change is also **backported** to: 0.8.2
- Added support for “AUTOCOMMIT” isolation when using the psycopg2
  DBAPI.   The keyword is available via the `isolation_level`
  execution option.  Patch courtesy Roman Podolyaka.
  This change is also **backported** to: 0.8.2
  References: [#2072](https://www.sqlalchemy.org/trac/ticket/2072)
- Added support for rendering `SMALLSERIAL` when a [SmallInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SmallInteger)
  type is used on a primary key autoincrement column, based on server
  version detection of PostgreSQL version 9.2 or greater.
  References: [#2840](https://www.sqlalchemy.org/trac/ticket/2840)
- Removed a 128-character truncation from the reflection of the
  server default for a column; this code was original from
  PG system views which truncated the string for readability.
  This change is also **backported** to: 0.8.3
  References: [#2844](https://www.sqlalchemy.org/trac/ticket/2844)
- Parenthesis will be applied to a compound SQL expression as
  rendered in the column list of a CREATE INDEX statement.
  This change is also **backported** to: 0.8.3
  References: [#2742](https://www.sqlalchemy.org/trac/ticket/2742)
- Fixed bug where PostgreSQL version strings that had a prefix preceding
  the words “PostgreSQL” or “EnterpriseDB” would not parse.
  Courtesy Scott Schaefer.
  This change is also **backported** to: 0.8.3
  References: [#2819](https://www.sqlalchemy.org/trac/ticket/2819)
- The behavior of [extract()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.extract) has been simplified on the
  PostgreSQL dialect to no longer inject a hardcoded `::timestamp`
  or similar cast into the given expression, as this interfered
  with types such as timezone-aware datetimes, but also
  does not appear to be at all necessary with modern versions
  of psycopg2.
  This change is also **backported** to: 0.8.2
  References: [#2740](https://www.sqlalchemy.org/trac/ticket/2740)
- Fixed bug in HSTORE type where keys/values that contained
  backslashed quotes would not be escaped correctly when
  using the “non native” (i.e. non-psycopg2) means
  of translating HSTORE data.  Patch courtesy Ryan Kelly.
  This change is also **backported** to: 0.8.2
  References: [#2766](https://www.sqlalchemy.org/trac/ticket/2766)
- Fixed bug where the order of columns in a multi-column
  PostgreSQL index would be reflected in the wrong order.
  Courtesy Roman Podolyaka.
  This change is also **backported** to: 0.8.2
  References: [#2767](https://www.sqlalchemy.org/trac/ticket/2767)

### mysql

- The `mysql_length` parameter used with [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) can now
  be passed as a dictionary of column names/lengths, for use
  with composite indexes.  Big thanks to Roman Podolyaka for the
  patch.
  This change is also **backported** to: 0.8.2
  References: [#2704](https://www.sqlalchemy.org/trac/ticket/2704)
- The MySQL [SET](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.SET) type now features the same auto-quoting
  behavior as that of [ENUM](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.ENUM).  Quotes are not required when
  setting up the value, but quotes that are present will be auto-detected
  along with a warning.  This also helps with Alembic where
  the SET type doesn’t render with quotes.
  References: [#2817](https://www.sqlalchemy.org/trac/ticket/2817)
- Updates to MySQL reserved words for versions 5.5, 5.6, courtesy
  Hanno Schlichting.
  This change is also **backported** to: 0.8.3, 0.7.11
  References: [#2791](https://www.sqlalchemy.org/trac/ticket/2791)
- The change in [#2721](https://www.sqlalchemy.org/trac/ticket/2721), which is that the `deferrable` keyword
  of [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) is silently ignored on the MySQL
  backend, will be reverted as of 0.9; this keyword will now render again, raising
  errors on MySQL as it is not understood - the same behavior will also
  apply to the `initially` keyword.  In 0.8, the keywords will remain
  ignored but a warning is emitted.   Additionally, the `match` keyword
  now raises a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) on 0.9 and emits a warning on 0.8;
  this keyword is not only silently ignored by MySQL but also breaks
  the ON UPDATE/ON DELETE options.
  To use a [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  that does not render or renders differently on MySQL, use a custom
  compilation option.  An example of this usage has been added to the
  documentation, see [MySQL / MariaDB Foreign Keys](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-foreign-keys).
  This change is also **backported** to: 0.8.3
  References: [#2721](https://www.sqlalchemy.org/trac/ticket/2721), [#2839](https://www.sqlalchemy.org/trac/ticket/2839)
- MySQL-connector dialect now allows options in the create_engine
  query string to override those defaults set up in the connect,
  including “buffered” and “raise_on_warnings”.
  This change is also **backported** to: 0.8.3
  References: [#2515](https://www.sqlalchemy.org/trac/ticket/2515)
- Fixed bug when using multi-table UPDATE where a supplemental
  table is a SELECT with its own bound parameters, where the positioning
  of the bound parameters would be reversed versus the statement
  itself when using MySQL’s special syntax.
  This change is also **backported** to: 0.8.2
  References: [#2768](https://www.sqlalchemy.org/trac/ticket/2768)
- Added another conditional to the `mysql+gaerdbms` dialect to
  detect so-called “development” mode, where we should use the
  `rdbms_mysqldb` DBAPI.  Patch courtesy Brett Slatkin.
  This change is also **backported** to: 0.8.2
  References: [#2715](https://www.sqlalchemy.org/trac/ticket/2715)
- The `deferrable` keyword argument on [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) and
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) will not render the `DEFERRABLE` keyword
  on the MySQL dialect.  For a long time we left this in place because
  a non-deferrable foreign key would act very differently than a deferrable
  one, but some environments just disable FKs on MySQL, so we’ll be less
  opinionated here.
  This change is also **backported** to: 0.8.2
  References: [#2721](https://www.sqlalchemy.org/trac/ticket/2721)
- Fix and test parsing of MySQL foreign key options within reflection;
  this complements the work in [#2183](https://www.sqlalchemy.org/trac/ticket/2183) where we begin to support
  reflection of foreign key options such as ON UPDATE/ON DELETE
  cascade.
  References: [#2839](https://www.sqlalchemy.org/trac/ticket/2839)
- Improved support for the cymysql driver, supporting version 0.6.5,
  courtesy Hajime Nakagami.

### sqlite

- The newly added SQLite DATETIME arguments storage_format and
  regexp apparently were not fully implemented correctly; while the
  arguments were accepted, in practice they would have no effect;
  this has been fixed.
  This change is also **backported** to: 0.8.3
  References: [#2781](https://www.sqlalchemy.org/trac/ticket/2781)
- Added [sqlalchemy.types.BIGINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BIGINT) to the list of type names that can be
  reflected by the SQLite dialect; courtesy Russell Stuart.
  This change is also **backported** to: 0.8.2
  References: [#2764](https://www.sqlalchemy.org/trac/ticket/2764)

### mssql

- When querying the information schema on SQL Server 2000, removed
  a CAST call that was added in 0.8.1 to help with driver issues,
  which apparently is not compatible on 2000.
  The CAST remains in place for SQL Server 2005 and greater.
  This change is also **backported** to: 0.8.2
  References: [#2747](https://www.sqlalchemy.org/trac/ticket/2747)
- Fixes to MSSQL with Python 3 + pyodbc, including that statements
  are passed correctly.
  References: [#2355](https://www.sqlalchemy.org/trac/ticket/2355)

### oracle

- The Oracle unit tests with cx_oracle now pass
  fully under Python 3.
- Fixed bug where Oracle table reflection using synonyms would fail
  if the synonym and the table were in different remote schemas.
  Patch to fix courtesy Kyle Derr.
  This change is also **backported** to: 0.8.3
  References: [#2853](https://www.sqlalchemy.org/trac/ticket/2853)

### misc

- Added a new flag `system=True` to [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), which marks
  the column as a “system” column which is automatically made present
  by the database (such as PostgreSQL `oid` or `xmin`).  The
  column will be omitted from the `CREATE TABLE` statement but will
  otherwise be available for querying.   In addition, the
  [CreateColumn](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateColumn) construct can be applied to a custom
  compilation rule which allows skipping of columns, by producing
  a rule that returns `None`.
  This change is also **backported** to: 0.8.3
- Added new flag `retaining=True` to the kinterbasdb and fdb dialects.
  This controls the value of the `retaining` flag sent to the
  `commit()` and `rollback()` methods of the DBAPI connection.
  Due to historical concerns, this flag defaults to `True` in 0.8.2,
  however in 0.9.0b1 this flag defaults to `False`.
  This change is also **backported** to: 0.8.2
  References: [#2763](https://www.sqlalchemy.org/trac/ticket/2763)
- Added a new variant to [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) called
  `ValuesBase.return_defaults()`; this allows arbitrary columns
  to be added to the RETURNING clause of the statement without interfering
  with the compilers usual “implicit returning” feature, which is used to
  efficiently fetch newly generated primary key values.  For supporting
  backends, a dictionary of all fetched values is present at
  `ResultProxy.returned_defaults`.
  References: [#2793](https://www.sqlalchemy.org/trac/ticket/2793)
- Added pool logging for “rollback-on-return” and the less used
  “commit-on-return”.  This is enabled with the rest of pool
  “debug” logging.
  References: [#2752](https://www.sqlalchemy.org/trac/ticket/2752)
- The `fdb` dialect is now the default dialect when
  specified without a dialect qualifier, i.e. `firebird://`,
  per the Firebird project publishing `fdb` as their
  official Python driver.
  References: [#2504](https://www.sqlalchemy.org/trac/ticket/2504)
- Type lookup when reflecting the Firebird types LONG and
  INT64 has been fixed so that LONG is treated as INTEGER,
  INT64 treated as BIGINT, unless the type has a “precision”
  in which case it’s treated as NUMERIC.  Patch courtesy
  Russell Stuart.
  This change is also **backported** to: 0.8.2
  References: [#2757](https://www.sqlalchemy.org/trac/ticket/2757)
- Fixed bug whereby if a composite type were set up
  with a function instead of a class, the mutable extension
  would trip up when it tried to check that column
  for being a [MutableComposite](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableComposite) (which it isn’t).
  Courtesy asldevi.
  This change is also **backported** to: 0.8.2
- The Python [mock](https://pypi.org/project/mock) library
  is now required in order to run the unit test suite.  While part
  of the standard library as of Python 3.3, previous Python installations
  will need to install this in order to run unit tests or to
  use the `sqlalchemy.testing` package for external dialects.
  This change is also **backported** to: 0.8.2
