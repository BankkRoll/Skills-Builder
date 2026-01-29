# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# 0.4 Changelog

## 0.4.8

Released: Sun Oct 12 2008

### orm

- Fixed bug regarding inherit_condition passed
  with “A=B” versus “B=A” leading to errors
  References: [#1039](https://www.sqlalchemy.org/trac/ticket/1039)
- Changes made to new, dirty and deleted
  collections in
  SessionExtension.before_flush() will take
  effect for that flush.
- Added label() method to InstrumentedAttribute
  to establish forwards compatibility with 0.5.

### sql

- column.in_(someselect) can now be used as
  a columns-clause expression without the subquery
  bleeding into the FROM clause
  References: [#1074](https://www.sqlalchemy.org/trac/ticket/1074)

### mysql

- Added MSMediumInteger type.
  References: [#1146](https://www.sqlalchemy.org/trac/ticket/1146)

### sqlite

- Supplied a custom strftime() function which
  handles dates before 1900.
  References: [#968](https://www.sqlalchemy.org/trac/ticket/968)
- String’s (and Unicode’s, UnicodeText’s, etc.)
  convert_unicode logic disabled in the sqlite dialect,
  to adjust for pysqlite 2.5.0’s new requirement that
  only Python unicode objects are accepted;
  [https://web.archive.org/web/20090614054912/https://itsystementwicklung.de/pipermail/list-pysqlite/2008-March/000018.html](https://web.archive.org/web/20090614054912/https://itsystementwicklung.de/pipermail/list-pysqlite/2008-March/000018.html)

### oracle

- has_sequence() now takes schema name into account
  References: [#1155](https://www.sqlalchemy.org/trac/ticket/1155)
- added BFILE to the list of reflected types
  References: [#1121](https://www.sqlalchemy.org/trac/ticket/1121)

## 0.4.7p1

Released: Thu Jul 31 2008

### orm

- Added “add()” and “add_all()” to scoped_session
  methods.  Workaround for 0.4.7:
  ```
  from sqlalchemy.orm.scoping import ScopedSession, instrument
  setattr(ScopedSession, "add", instrument("add"))
  setattr(ScopedSession, "add_all", instrument("add_all"))
  ```
- Fixed non-2.3 compatible usage of set() and generator
  expression within relation().

## 0.4.7

Released: Sat Jul 26 2008

### orm

- The contains() operator when used with many-to-many
  will alias() the secondary (association) table so
  that multiple contains() calls will not conflict
  with each other
  References: [#1058](https://www.sqlalchemy.org/trac/ticket/1058)
- fixed bug preventing merge() from functioning in
  conjunction with a comparable_property()
- the enable_typechecks=False setting on relation()
  now only allows subtypes with inheriting mappers.
  Totally unrelated types, or subtypes not set up with
  mapper inheritance against the target mapper are
  still not allowed.
- Added is_active flag to Sessions to detect when
  a transaction is in progress.  This
  flag is always True with a “transactional”
  (in 0.5 a non-“autocommit”) Session.
  References: [#976](https://www.sqlalchemy.org/trac/ticket/976)

### sql

- Fixed bug when calling select([literal(‘foo’)])
  or select([bindparam(‘foo’)]).

### schema

- create_all(), drop_all(), create(), drop() all raise
  an error if the table name or schema name contains
  more characters than that dialect’s configured
  character limit.  Some DB’s can handle too-long
  table names during usage, and SQLA can handle this
  as well. But various reflection/
  checkfirst-during-create scenarios fail since we are
  looking for the name within the DB’s catalog tables.
  References: [#571](https://www.sqlalchemy.org/trac/ticket/571)
- The index name generated when you say “index=True”
  on a Column is truncated to the length appropriate
  for the dialect. Additionally, an Index with a too-
  long name cannot be explicitly dropped with
  Index.drop(), similar to.
  References: [#571](https://www.sqlalchemy.org/trac/ticket/571), [#820](https://www.sqlalchemy.org/trac/ticket/820)

### mysql

- Added ‘CALL’ to the list of SQL keywords which return
  result rows.

### oracle

- Oracle get_default_schema_name() “normalizes” the name
  before returning, meaning it returns a lower-case name
  when the identifier is detected as case insensitive.
- creating/dropping tables takes schema name into account
  when searching for the existing table, so that tables
  in other owner namespaces with the same name do not
  conflict
  References: [#709](https://www.sqlalchemy.org/trac/ticket/709)
- Cursors now have “arraysize” set to 50 by default on
  them, the value of which is configurable using the
  “arraysize” argument to create_engine() with the
  Oracle dialect.  This to account for cx_oracle’s default
  setting of “1”, which has the effect of many round trips
  being sent to Oracle.  This actually works well in
  conjunction with BLOB/CLOB-bound cursors, of which
  there are any number available but only for the life of
  that row request (so BufferedColumnRow is still needed,
  but less so).
  References: [#1062](https://www.sqlalchemy.org/trac/ticket/1062)
- sqlite
  - add SLFloat type, which matches the SQLite REAL
    type affinity.  Previously, only SLNumeric was provided
    which fulfills NUMERIC affinity, but that’s not the
    same as REAL.

### misc

- Repaired server_side_cursors to properly detect
  text() clauses.
- Added PGCidr type.
  References: [#1092](https://www.sqlalchemy.org/trac/ticket/1092)

## 0.4.6

Released: Sat May 10 2008

### orm

- Fix to the recent relation() refactoring which fixes
  exotic viewonly relations which join between local and
  remote table multiple times, with a common column shared
  between the joins.
- Also re-established viewonly relation() configurations
  that join across multiple tables.
- Added experimental relation() flag to help with
  primaryjoins across functions, etc.,
  _local_remote_pairs=[tuples].  This complements a complex
  primaryjoin condition allowing you to provide the
  individual column pairs which comprise the relation’s
  local and remote sides.  Also improved lazy load SQL
  generation to handle placing bind params inside of
  functions and other expressions.  (partial progress
  towards)
  References: [#610](https://www.sqlalchemy.org/trac/ticket/610)
- repaired single table inheritance such that you
  can single-table inherit from a joined-table inheriting
  mapper without issue.
  References: [#1036](https://www.sqlalchemy.org/trac/ticket/1036)
- Fixed “concatenate tuple” bug which could occur with
  Query.order_by() if clause adaption had taken place.
  References: [#1027](https://www.sqlalchemy.org/trac/ticket/1027)
- Removed ancient assertion that mapped selectables require
  “alias names” - the mapper creates its own alias now if
  none is present.  Though in this case you need to use the
  class, not the mapped selectable, as the source of column
  attributes - so a warning is still issued.
- fixes to the “exists” function involving inheritance (any(),
  has(), ~contains()); the full target join will be rendered
  into the EXISTS clause for relations that link to subclasses.
- restored usage of append_result() extension method for primary
  query rows, when the extension is present and only a single-
  entity result is being returned.
- Also re-established viewonly relation() configurations that
  join across multiple tables.
- removed ancient assertion that mapped selectables require
  “alias names” - the mapper creates its own alias now if
  none is present.  Though in this case you need to use
  the class, not the mapped selectable, as the source of
  column attributes - so a warning is still issued.
- refined mapper._save_obj() which was unnecessarily calling
  __ne__() on scalar values during flush
  References: [#1015](https://www.sqlalchemy.org/trac/ticket/1015)
- added a feature to eager loading whereby subqueries set
  as column_property() with explicit label names (which is not
  necessary, btw) will have the label anonymized when
  the instance is part of the eager join, to prevent
  conflicts with a subquery or column of the same name
  on the parent object.
  References: [#1019](https://www.sqlalchemy.org/trac/ticket/1019)
- set-based collections |=, -=, ^= and &= are stricter about
  their operands and only operate on sets, frozensets or
  subclasses of the collection type. Previously, they would
  accept any duck-typed set.
- added an example dynamic_dict/dynamic_dict.py, illustrating
  a simple way to place dictionary behavior on top of
  a dynamic_loader.

### sql

- Added COLLATE support via the .collate(<collation>)
  expression operator and collate(<expr>, <collation>) sql
  function.
- Fixed bug with union() when applied to non-Table connected
  select statements
- improved behavior of text() expressions when used as
  FROM clauses, such as select().select_from(text(“sometext”))
  References: [#1014](https://www.sqlalchemy.org/trac/ticket/1014)
- Column.copy() respects the value of “autoincrement”,
  fixes usage with Migrate
  References: [#1021](https://www.sqlalchemy.org/trac/ticket/1021)

### mssql

- Added “odbc_autotranslate” parameter to engine / dburi
  parameters. Any given string will be passed through to the
  ODBC connection string as:
  > ”AutoTranslate=%s” % odbc_autotranslate
  References: [#1005](https://www.sqlalchemy.org/trac/ticket/1005)
- Added “odbc_options” parameter to engine / dburi
  parameters. The given string is simply appended to the
  SQLAlchemy-generated odbc connection string.
  This should obviate the need of adding a myriad of ODBC
  options in the future.

### misc

- Joined table inheritance mappers use a slightly relaxed
  function to create the “inherit condition” to the parent
  table, so that other foreign keys to not-yet-declared
  Table objects don’t trigger an error.
- fixed reentrant mapper compile hang when
  a declared attribute is used within ForeignKey,
  ie. ForeignKey(MyOtherClass.someattribute)
- Pool listeners can now be provided as a dictionary of
  callables or a (possibly partial) duck-type of
  PoolListener, your choice.
- added “rollback_returned” option to Pool which will
  disable the rollback() issued when connections are
  returned.  This flag is only safe to use with a database
  which does not support transactions (i.e. MySQL/MyISAM).
- set-based association proxies |=, -=, ^= and &= are
  stricter about their operands and only operate on sets,
  frozensets or other association proxies. Previously, they
  would accept any duck-typed set.
- Handle the “SUBSTRING(:string FROM :start FOR :length)”
  builtin.

## 0.4.5

Released: Fri Apr 04 2008

### orm

- A small change in behavior to session.merge() - existing
  objects are checked for based on primary key attributes, not
  necessarily _instance_key.  So the widely requested
  capability, that:
  > x = MyObject(id=1)
  > x = sess.merge(x)
  will in fact load MyObject with id #1 from the database if
  present, is now available.  merge() still copies the state
  of the given object to the persistent one, so an example
  like the above would typically have copied “None” from all
  attributes of “x” onto the persistent copy.  These can be
  reverted using session.expire(x).
- Also fixed behavior in merge() whereby collection elements
  present on the destination but not the merged collection
  were not being removed from the destination.
- Added a more aggressive check for “uncompiled mappers”,
  helps particularly with declarative layer
  References: [#995](https://www.sqlalchemy.org/trac/ticket/995)
- The methodology behind “primaryjoin”/”secondaryjoin” has
  been refactored.  Behavior should be slightly more
  intelligent, primarily in terms of error messages which
  have been pared down to be more readable.  In a slight
  number of scenarios it can better resolve the correct
  foreign key than before.
- Added comparable_property(), adds query Comparator
  behavior to regular, unmanaged Python properties
- the functionality of query.with_polymorphic() has
  been added to mapper() as a configuration option.
    It’s set via several forms:
  with_polymorphic=’*’
  with_polymorphic=[mappers]
  with_polymorphic=(‘*’, selectable)
  with_polymorphic=([mappers], selectable)
  This controls the default polymorphic loading strategy
  for inherited mappers. When a selectable is not given,
  outer joins are created for all joined-table inheriting
  mappers requested. Note that the auto-create of joins
  is not compatible with concrete table inheritance.
  The existing select_table flag on mapper() is now
  deprecated and is synonymous with
  with_polymorphic(‘*’, select_table).  Note that the
  underlying “guts” of select_table have been
  completely removed and replaced with the newer,
  more flexible approach.
  The new approach also automatically allows eager loads
  to work for subclasses, if they are present, for
  example:
  ```
  sess.query(Company).options(eagerload_all())
  ```
  to load Company objects, their employees, and the
  ‘machines’ collection of employees who happen to be
  Engineers. A “with_polymorphic” Query option should be
  introduced soon as well which would allow per-Query
  control of with_polymorphic() on relations.
- added two “experimental” features to Query,
  “experimental” in that their specific name/behavior
  is not carved in stone just yet:  _values() and
  _from_self().  We’d like feedback on these.
  - _values(*columns) is given a list of column
    expressions, and returns a new Query that only
    returns those columns. When evaluated, the return
    value is a list of tuples just like when using
    add_column() or add_entity(), the only difference is
    that “entity zero”, i.e. the mapped class, is not
    included in the results. This means it finally makes
    sense to use group_by() and having() on Query, which
    have been sitting around uselessly until now.
    A future change to this method may include that its
    ability to join, filter and allow other options not
    related to a “resultset” are removed, so the feedback
    we’re looking for is how people want to use
    _values()…i.e. at the very end, or do people prefer
    to continue generating after it’s called.
  - _from_self() compiles the SELECT statement for the
    Query (minus any eager loaders), and returns a new
    Query that selects from that SELECT. So basically you
    can query from a Query without needing to extract the
    SELECT statement manually. This gives meaning to
    operations like query[3:5]._from_self().filter(some
    criterion). There’s not much controversial here
    except that you can quickly create highly nested
    queries that are less efficient, and we want feedback
    on the naming choice.
- query.order_by() and query.group_by() will accept
  multiple arguments using *args (like select()
  already does).
- Added some convenience descriptors to Query:
  query.statement returns the full SELECT construct,
  query.whereclause returns just the WHERE part of the
  SELECT construct.
- Fixed/covered case when using a False/0 value as a
  polymorphic discriminator.
- Fixed bug which was preventing synonym() attributes from
  being used with inheritance
- Fixed SQL function truncation of trailing underscores
  References: [#996](https://www.sqlalchemy.org/trac/ticket/996)
- When attributes are expired on a pending instance, an
  error will not be raised when the “refresh” action is
  triggered and no result is found.
- Session.execute can now find binds from metadata
- Adjusted the definition of “self-referential” to be any
  two mappers with a common parent (this affects whether or
  not aliased=True is required when joining with Query).
- Made some fixes to the “from_joinpoint” argument to
  query.join() so that if the previous join was aliased and
  this one isn’t, the join still happens successfully.
- Assorted “cascade deletes” fixes:
  - Fixed “cascade delete” operation of dynamic relations,
    which had only been implemented for foreign-key
    nulling behavior in 0.4.2 and not actual cascading
    deletes
  - Delete cascade without delete-orphan cascade on a
    many-to-one will not delete orphans which were
    disconnected from the parent before session.delete()
    is called on the parent (one-to-many already had
    this).
  - Delete cascade with delete-orphan will delete orphans
    whether or not it remains attached to its also-deleted
    parent.
  - delete-orphan cascade is properly detected on relations
    that are present on superclasses when using inheritance.
  References: [#895](https://www.sqlalchemy.org/trac/ticket/895)
- Fixed order_by calculation in Query to properly alias
  mapper-config’ed order_by when using select_from()
- Refactored the diffing logic that kicks in when replacing
  one collection with another into collections.bulk_replace,
  useful to anyone building multi-level collections.
- Cascade traversal algorithm converted from recursive to
  iterative to support deep object graphs.

### sql

- schema-qualified tables now will place the schemaname
  ahead of the tablename in all column expressions as well
  as when generating column labels.  This prevents cross-
  schema name collisions in all cases
  References: [#999](https://www.sqlalchemy.org/trac/ticket/999)
- can now allow selects which correlate all FROM clauses
  and have no FROM themselves.  These are typically
  used in a scalar context, i.e. SELECT x, (SELECT x WHERE y)
  FROM table.  Requires explicit correlate() call.
- ’name’ is no longer a required constructor argument for
  Column().  It (and .key) may now be deferred until the
  column is added to a Table.
- like(), ilike(), contains(), startswith(), endswith() take
  an optional keyword argument “escape=<somestring>”, which
  is set as the escape character using the syntax “x LIKE y
  ESCAPE ‘<somestring>’”.
  References: [#791](https://www.sqlalchemy.org/trac/ticket/791), [#993](https://www.sqlalchemy.org/trac/ticket/993)
- random() is now a generic sql function and will compile to
  the database’s random implementation, if any.
- update().values() and insert().values() take keyword
  arguments.
- Fixed an issue in select() regarding its generation of
  FROM clauses, in rare circumstances two clauses could be
  produced when one was intended to cancel out the other.
  Some ORM queries with lots of eager loads might have seen
  this symptom.
- The case() function now also takes a dictionary as its
  whens parameter.  It also interprets the “THEN”
  expressions as values by default, meaning case([(x==y,
  “foo”)]) will interpret “foo” as a bound value, not a SQL
  expression.  use text(expr) for literal SQL expressions in
  this case.  For the criterion itself, these may be literal
  strings only if the “value” keyword is present, otherwise
  SA will force explicit usage of either text() or
  literal().

### mysql

- The connection.info keys the dialect uses to cache server
  settings have changed and are now namespaced.

### mssql

- Reflected tables will now automatically load other tables
  which are referenced by Foreign keys in the auto-loaded
  table,.
  References: [#979](https://www.sqlalchemy.org/trac/ticket/979)
- Added executemany check to skip identity fetch,.
  References: [#916](https://www.sqlalchemy.org/trac/ticket/916)
- Added stubs for small date type.
  References: [#884](https://www.sqlalchemy.org/trac/ticket/884)
- Added a new ‘driver’ keyword parameter for the pyodbc dialect.
  Will substitute into the ODBC connection string if given,
  defaults to ‘SQL Server’.
- Added a new ‘max_identifier_length’ keyword parameter for
  the pyodbc dialect.
- Improvements to pyodbc + Unix. If you couldn’t get that
  combination to work before, please try again.

### oracle

- The “owner” keyword on Table is now deprecated, and is
  exactly synonymous with the “schema” keyword.  Tables can
  now be reflected with alternate “owner” attributes,
  explicitly stated on the Table object or not using
  “schema”.
- All of the “magic” searching for synonyms, DBLINKs etc.
  during table reflection are disabled by default unless you
  specify “oracle_resolve_synonyms=True” on the Table
  object.  Resolving synonyms necessarily leads to some
  messy guessing which we’d rather leave off by default.
  When the flag is set, tables and related tables will be
  resolved against synonyms in all cases, meaning if a
  synonym exists for a particular table, reflection will use
  it when reflecting related tables.  This is stickier
  behavior than before which is why it’s off by default.

### misc

- The “synonym” function is now directly usable with
  “declarative”.  Pass in the decorated property using the
  “descriptor” keyword argument, e.g.: somekey =
  synonym(‘_somekey’, descriptor=property(g, s))
- The “deferred” function is usable with “declarative”.
  Simplest usage is to declare deferred and Column together,
  e.g.: data = deferred(Column(Text))
- Declarative also gained @synonym_for(…) and
  @comparable_using(…), front-ends for synonym and
  comparable_property.
- Improvements to mapper compilation when using declarative;
  already-compiled mappers will still trigger compiles of
  other uncompiled mappers when used
  References: [#995](https://www.sqlalchemy.org/trac/ticket/995)
- Declarative will complete setup for Columns lacking names,
  allows a more DRY syntax.
  > class Foo(Base):
  >
  > __tablename__ = ‘foos’
  > id = Column(Integer, primary_key=True)
- inheritance in declarative can be disabled when sending
  “inherits=None” to __mapper_args__.
- declarative_base() takes optional kwarg “mapper”, which
  is any callable/class/method that produces a mapper,
  such as declarative_base(mapper=scopedsession.mapper).
  This property can also be set on individual declarative
  classes using the “__mapper_cls__” property.
- Got PG server side cursors back into shape, added fixed
  unit tests as part of the default test suite.  Added
  better uniqueness to the cursor ID
  References: [#1001](https://www.sqlalchemy.org/trac/ticket/1001)

## 0.4.4

Released: Wed Mar 12 2008

### orm

- any(), has(), contains(), ~contains(), attribute level ==
  and != now work properly with self-referential relations -
  the clause inside the EXISTS is aliased on the “remote”
  side to distinguish it from the parent table.  This
  applies to single table self-referential as well as
  inheritance-based self-referential.
- Repaired behavior of == and != operators at the relation()
  level when compared against NULL for one-to-one relations
  References: [#985](https://www.sqlalchemy.org/trac/ticket/985)
- Fixed bug whereby session.expire() attributes were not
  loading on an polymorphically-mapped instance mapped by a
  select_table mapper.
- Added query.with_polymorphic() - specifies a list of
  classes which descend from the base class, which will be
  added to the FROM clause of the query.  Allows subclasses
  to be used within filter() criterion as well as eagerly
  loads the attributes of those subclasses.
- Your cries have been heard: removing a pending item from
  an attribute or collection with delete-orphan expunges the
  item from the session; no FlushError is raised.  Note that
  if you session.save()’ed the pending item explicitly, the
  attribute/collection removal still knocks it out.
- session.refresh() and session.expire() raise an error when
  called on instances which are not persistent within the
  session
- Fixed potential generative bug when the same Query was
  used to generate multiple Query objects using join().
- Fixed bug which was introduced in 0.4.3, whereby loading
  an already-persistent instance mapped with joined table
  inheritance would trigger a useless “secondary” load from
  its joined table, when using the default “select”
  polymorphic_fetch.  This was due to attributes being
  marked as expired during its first load and not getting
  unmarked from the previous “secondary” load.  Attributes
  are now unexpired based on presence in __dict__ after any
  load or commit operation succeeds.
- Deprecated Query methods apply_sum(), apply_max(),
  apply_min(), apply_avg().  Better methodologies are
  coming….
- relation() can accept a callable for its first argument,
  which returns the class to be related.  This is in place
  to assist declarative packages to define relations without
  classes yet being in place.
- Added a new “higher level” operator called “of_type()”:
  used in join() as well as with any() and has(), qualifies
  the subclass which will be used in filter criterion, e.g.:
  > query.filter(Company.employees.of_type(Engineer).
  >
  > any(Engineer.name==’foo’))
  >
  >
  >
  > or
  >
  >   query.join(Company.employees.of_type(Engineer)).
  >
  > filter(Engineer.name==’foo’)
- Preventive code against a potential lost-reference bug in
  flush().
- Expressions used in filter(), filter_by() and others, when
  they make usage of a clause generated from a relation
  using the identity of a child object (e.g.,
  filter(Parent.child==<somechild>)), evaluate the actual
  primary key value of <somechild> at execution time so that
  the autoflush step of the Query can complete, thereby
  populating the PK value of <somechild> in the case that
  <somechild> was pending.
- setting the relation()-level order by to a column in the
  many-to-many “secondary” table will now work with eager
  loading, previously the “order by” wasn’t aliased against
  the secondary table’s alias.
- Synonyms riding on top of existing descriptors are now
  full proxies to those descriptors.

### sql

- Can again create aliases of selects against textual FROM
  clauses.
  References: [#975](https://www.sqlalchemy.org/trac/ticket/975)
- The value of a bindparam() can be a callable, in which
  case it’s evaluated at statement execution time to get the
  value.
- Added exception wrapping/reconnect support to result set
  fetching.  Reconnect works for those databases that raise
  a catchable data error during results (i.e. doesn’t work
  on MySQL)
  References: [#978](https://www.sqlalchemy.org/trac/ticket/978)
- Implemented two-phase API for “threadlocal” engine, via
  engine.begin_twophase(), engine.prepare()
  References: [#936](https://www.sqlalchemy.org/trac/ticket/936)
- Fixed bug which was preventing UNIONS from being
  cloneable.
  References: [#986](https://www.sqlalchemy.org/trac/ticket/986)
- Added “bind” keyword argument to insert(), update(),
  delete() and DDL(). The .bind property is now assignable
  on those statements as well as on select().
- Insert statements can now be compiled with extra “prefix”
  words between INSERT and INTO, for vendor extensions like
  MySQL’s INSERT IGNORE INTO table.

### extensions

- a new super-small “declarative” extension has been added,
  which allows Table and mapper() configuration to take
  place inline underneath a class declaration.  This
  extension differs from ActiveMapper and Elixir in that it
  does not redefine any SQLAlchemy semantics at all; literal
  Column, Table and relation() constructs are used to define
  the class behavior and table definition.

### misc

- Invalid SQLite connection URLs now raise an error.
- postgres TIMESTAMP renders correctly
  References: [#981](https://www.sqlalchemy.org/trac/ticket/981)
- postgres PGArray is a “mutable” type by default; when used
  with the ORM, mutable-style equality/ copy-on-write
  techniques are used to test for changes.

## 0.4.3

Released: Thu Feb 14 2008

### general

- Fixed a variety of hidden and some not-so-hidden
  compatibility issues for Python 2.3, thanks to new support
  for running the full test suite on 2.3.
- Warnings are now issued as type exceptions.SAWarning.

### orm

- Every Session.begin() must now be accompanied by a
  corresponding commit() or rollback() unless the session is
  closed with Session.close().  This also includes the begin()
  which is implicit to a session created with
  transactional=True.  The biggest change introduced here is
  that when a Session created with transactional=True raises
  an exception during flush(), you must call
  Session.rollback() or Session.close() in order for that
  Session to continue after an exception.
- Fixed merge() collection-doubling bug when merging transient
  entities with backref’ed collections.
  References: [#961](https://www.sqlalchemy.org/trac/ticket/961)
- merge(dont_load=True) does not accept transient entities,
  this is in continuation with the fact that
  merge(dont_load=True) does not accept any “dirty” objects
  either.
- Added standalone “query” class attribute generated by a
  scoped_session.  This provides MyClass.query without using
  Session.mapper.  Use via:
  > MyClass.query = Session.query_property()
- The proper error message is raised when trying to access
  expired instance attributes with no session present
- dynamic_loader() / lazy=”dynamic” now accepts and uses
  the order_by parameter in the same way in which it works
  with relation().
- Added expire_all() method to Session.  Calls expire() for
  all persistent instances.  This is handy in conjunction
  with…
- Instances which have been partially or fully expired will
  have their expired attributes populated during a regular
  Query operation which affects those objects, preventing a
  needless second SQL statement for each instance.
- Dynamic relations, when referenced, create a strong
  reference to the parent object so that the query still has a
  parent to call against even if the parent is only created
  (and otherwise dereferenced) within the scope of a single
  expression.
  References: [#938](https://www.sqlalchemy.org/trac/ticket/938)
- Added a mapper() flag “eager_defaults”. When set to True,
  defaults that are generated during an INSERT or UPDATE
  operation are post-fetched immediately, instead of being
  deferred until later.  This mimics the old 0.3 behavior.
- query.join() can now accept class-mapped attributes as
  arguments. These can be used in place or in any combination
  with strings.  In particular this allows construction of
  joins to subclasses on a polymorphic relation, i.e.:
  > query(Company).join([‘employees’, Engineer.name])
- query.join() can also accept tuples of attribute name/some
  selectable as arguments.  This allows construction of joins
  *from* subclasses of a polymorphic relation, i.e.:
  > query(Company).join(
  >
  >
  >
  > )
- General improvements to the behavior of join() in
  conjunction with polymorphic mappers, i.e. joining from/to
  polymorphic mappers and properly applying aliases.
- Fixed/improved behavior when a mapper determines the natural
  “primary key” of a mapped join, it will more effectively
  reduce columns which are equivalent via foreign key
  relation.  This affects how many arguments need to be sent
  to query.get(), among other things.
  References: [#933](https://www.sqlalchemy.org/trac/ticket/933)
- The lazy loader can now handle a join condition where the
  “bound” column (i.e. the one that gets the parent id sent as
  a bind parameter) appears more than once in the join
  condition.  Specifically this allows the common task of a
  relation() which contains a parent-correlated subquery, such
  as “select only the most recent child item”.
  References: [#946](https://www.sqlalchemy.org/trac/ticket/946)
- Fixed bug in polymorphic inheritance where an incorrect
  exception is raised when base polymorphic_on column does not
  correspond to any columns within the local selectable of an
  inheriting mapper more than one level deep
- Fixed bug in polymorphic inheritance which made it difficult
  to set a working “order_by” on a polymorphic mapper.
- Fixed a rather expensive call in Query that was slowing down
  polymorphic queries.
- ”Passive defaults” and other “inline” defaults can now be
  loaded during a flush() call if needed; in particular, this
  allows constructing relations() where a foreign key column
  references a server-side-generated, non-primary-key
  column.
  References: [#954](https://www.sqlalchemy.org/trac/ticket/954)
- Additional Session transaction fixes/changes:
  - Fixed bug with session transaction management: parent
    transactions weren’t started on the connection when
    adding a connection to a nested transaction.
  - session.transaction now always refers to the innermost
    active transaction, even when commit/rollback are called
    directly on the session transaction object.
  - Two-phase transactions can now be prepared.
  - When preparing a two-phase transaction fails on one
    connection, all the connections are rolled back.
  - session.close() didn’t close all transactions when
    nested transactions were used.
  - rollback() previously erroneously set the current
    transaction directly to the parent of the transaction
    that could be rolled back to. Now it rolls back the next
    transaction up that can handle it, but sets the current
    transaction to its parent and inactivates the
    transactions in between. Inactive transactions can only
    be rolled back or closed, any other call results in an
    error.
  - autoflush for commit() wasn’t flushing for simple
    subtransactions.
  - unitofwork flush didn’t close the failed transaction
    when the session was not in a transaction and committing
    the transaction failed.
- Miscellaneous tickets:
  References: [#940](https://www.sqlalchemy.org/trac/ticket/940), [#964](https://www.sqlalchemy.org/trac/ticket/964)

### sql

- Added “schema.DDL”, an executable free-form DDL statement.
  DDLs can be executed in isolation or attached to Table or
  MetaData instances and executed automatically when those
  objects are created and/or dropped.
- Table columns and constraints can be overridden on a an
  existing table (such as a table that was already reflected)
  using the ‘useexisting=True’ flag, which now takes into
  account the arguments passed along with it.
- Added a callable-based DDL events interface, adds hooks
  before and after Tables and MetaData create and drop.
- Added generative where(<criterion>) method to delete() and
  update() constructs which return a new object with criterion
  joined to existing criterion via AND, just like
  select().where().
- Added “ilike()” operator to column operations.  Compiles to
  ILIKE on postgres, lower(x) LIKE lower(y) on all
  others.
  References: [#727](https://www.sqlalchemy.org/trac/ticket/727)
- Added “now()” as a generic function; on SQLite, Oracle
  and MSSQL compiles as “CURRENT_TIMESTAMP”; “now()” on
  all others.
  References: [#943](https://www.sqlalchemy.org/trac/ticket/943)
- The startswith(), endswith(), and contains() operators now
  concatenate the wildcard operator with the given operand in
  SQL, i.e. “’%’ || <bindparam>” in all cases, accept
  text(‘something’) operands properly
  References: [#962](https://www.sqlalchemy.org/trac/ticket/962)
- cast() accepts text(‘something’) and other non-literal
  operands properly
  References: [#962](https://www.sqlalchemy.org/trac/ticket/962)
- fixed bug in result proxy where anonymously generated
  column labels would not be accessible using their straight
  string name
- Deferrable constraints can now be defined.
- Added “autocommit=True” keyword argument to select() and
  text(), as well as generative autocommit() method on
  select(); for statements which modify the database through
  some user-defined means other than the usual INSERT/UPDATE/
  DELETE etc.  This flag will enable “autocommit” behavior
  during execution if no transaction is in progress.
  References: [#915](https://www.sqlalchemy.org/trac/ticket/915)
- The ‘.c.’ attribute on a selectable now gets an entry for
  every column expression in its columns clause.  Previously,
  “unnamed” columns like functions and CASE statements weren’t
  getting put there.  Now they will, using their full string
  representation if no ‘name’ is available.
- a CompositeSelect, i.e. any union(), union_all(),
  intersect(), etc. now asserts that each selectable contains
  the same number of columns.  This conforms to the
  corresponding SQL requirement.
- The anonymous ‘label’ generated for otherwise unlabeled
  functions and expressions now propagates outwards at compile
  time for expressions like select([select([func.foo()])]).
- Building on the above ideas, CompositeSelects now build up
  their “.c.” collection based on the names present in the
  first selectable only; corresponding_column() now works
  fully for all embedded selectables.
- Oracle and others properly encode SQL used for defaults like
  sequences, etc., even if no unicode idents are used since
  identifier preparer may return a cached unicode identifier.
- Column and clause comparisons to datetime objects on the
  left hand side of the expression now work (d < table.c.col).
  (datetimes on the RHS have always worked, the LHS exception
  is a quirk of the datetime implementation.)

### misc

- Better support for schemas in SQLite (linked in by ATTACH
  DATABASE … AS name).  In some cases in the past, schema
  names were omitted from generated SQL for SQLite.  This is
  no longer the case.
- table_names on SQLite now picks up temporary tables as well.
- Auto-detect an unspecified MySQL ANSI_QUOTES mode during
  reflection operations, support for changing the mode
  midstream.  Manual mode setting is still required if no
  reflection is used.
- Fixed reflection of TIME columns on SQLite.
- Finally added PGMacAddr type to postgres
  References: [#580](https://www.sqlalchemy.org/trac/ticket/580)
- Reflect the sequence associated to a PK field (typically
  with a BEFORE INSERT trigger) under Firebird
- Oracle assembles the correct columns in the result set
  column mapping when generating a LIMIT/OFFSET subquery,
  allows columns to map properly to result sets even if
  long-name truncation kicks in
  References: [#941](https://www.sqlalchemy.org/trac/ticket/941)
- MSSQL now includes EXEC in the _is_select regexp, which
  should allow row-returning stored procedures to be used.
- MSSQL now includes an experimental implementation of
  LIMIT/OFFSET using the ANSI SQL row_number() function, so it
  requires MSSQL-2005 or higher. To enable the feature, add
  “has_window_funcs” to the keyword arguments for connect, or
  add “?has_window_funcs=1” to your dburi query arguments.
- Changed ext.activemapper to use a non-transactional session
  for the objectstore.
- Fixed output order of “[‘a’] + obj.proxied” binary operation
  on association-proxied lists.

## 0.4.2p3

Released: Wed Jan 09 2008

### general

- sub version numbering scheme changed to suite
  setuptools version number rules; easy_install -u
  should now get this version over 0.4.2.

### orm

- fixed bug with session.dirty when using “mutable
  scalars” (such as PickleTypes)
- added a more descriptive error message when flushing
  on a relation() that has non-locally-mapped columns
  in its primary or secondary join condition
- suppressing *all* errors in
  InstanceState.__cleanup() now.
- fixed an attribute history bug whereby assigning a
  new collection to a collection-based attribute which
  already had pending changes would generate incorrect
  history
  References: [#922](https://www.sqlalchemy.org/trac/ticket/922)
- fixed delete-orphan cascade bug whereby setting the
  same object twice to a scalar attribute could log it
  as an orphan
  References: [#925](https://www.sqlalchemy.org/trac/ticket/925)
- Fixed cascades on a += assignment to a list-based
  relation.
- synonyms can now be created against props that don’t
  exist yet, which are later added via add_property().
  This commonly includes backrefs. (i.e. you can make
  synonyms for backrefs without worrying about the
  order of operations)
  References: [#919](https://www.sqlalchemy.org/trac/ticket/919)
- fixed bug which could occur with polymorphic “union”
  mapper which falls back to “deferred” loading of
  inheriting tables
- the “columns” collection on a mapper/mapped class
  (i.e. ‘c’) is against the mapped table, not the
  select_table in the case of polymorphic “union”
  loading (this shouldn’t be noticeable).
- fixed fairly critical bug whereby the same instance could be listed
  more than once in the unitofwork.new collection; most typically
  reproduced when using a combination of inheriting mappers and
  ScopedSession.mapper, as the multiple __init__ calls per instance
  could save() the object with distinct _state objects
- added very rudimentary yielding iterator behavior to Query.  Call
  query.yield_per(<number of rows>) and evaluate the Query in an
  iterative context; every collection of N rows will be packaged up
  and yielded.  Use this method with extreme caution since it does
  not attempt to reconcile eagerly loaded collections across
  result batch boundaries, nor will it behave nicely if the same
  instance occurs in more than one batch.  This means that an eagerly
  loaded collection will get cleared out if it’s referenced in more than
  one batch, and in all cases attributes will be overwritten on instances
  that occur in more than one batch.
- Fixed in-place set mutation operators for set collections and association
  proxied sets.
  References: [#920](https://www.sqlalchemy.org/trac/ticket/920)

### sql

- Text type is properly exported now and does not
  raise a warning on DDL create; String types with no
  length only raise warnings during CREATE TABLE
  References: [#912](https://www.sqlalchemy.org/trac/ticket/912)
- new UnicodeText type is added, to specify an
  encoded, unlengthed Text type
- fixed bug in union() so that select() statements
  which don’t derive from FromClause objects can be
  unioned
- changed name of TEXT to Text since its a “generic”
  type; TEXT name is deprecated until 0.5. The
  “upgrading” behavior of String to Text when no
  length is present is also deprecated until 0.5; will
  issue a warning when used for CREATE TABLE
  statements (String with no length for SQL expression
  purposes is still fine)
  References: [#912](https://www.sqlalchemy.org/trac/ticket/912)
- generative select.order_by(None) / group_by(None)
  was not managing to reset order by/group by
  criterion, fixed
  References: [#924](https://www.sqlalchemy.org/trac/ticket/924)

### misc

- Fixed reflection of mysql empty string column
  defaults.
- ’+’, ‘*’, ‘+=’ and ‘*=’ support for association
  proxied lists.
- mssql - narrowed down the test for “date”/”datetime”
  in MSDate/ MSDateTime subclasses so that incoming
  “datetime” objects don’t get mis-interpreted as
  “date” objects and vice versa.
  References: [#923](https://www.sqlalchemy.org/trac/ticket/923)
- Fixed the missing call to subtype result processor for the PGArray
  type.
  References: [#913](https://www.sqlalchemy.org/trac/ticket/913)

## 0.4.2

Released: Wed Jan 02 2008

### orm

- a major behavioral change to collection-based backrefs: they no
  longer trigger lazy loads !  “reverse” adds and removes
  are queued up and are merged with the collection when it is
  actually read from and loaded; but do not trigger a load beforehand.
  For users who have noticed this behavior, this should be much more
  convenient than using dynamic relations in some cases; for those who
  have not, you might notice your apps using a lot fewer queries than
  before in some situations.
  References: [#871](https://www.sqlalchemy.org/trac/ticket/871)
- mutable primary key support is added. primary key columns can be
  changed freely, and the identity of the instance will change upon
  flush. In addition, update cascades of foreign key referents (primary
  key or not) along relations are supported, either in tandem with the
  database’s ON UPDATE CASCADE (required for DB’s like Postgres) or
  issued directly by the ORM in the form of UPDATE statements, by setting
  the flag “passive_cascades=False”.
- inheriting mappers now inherit the MapperExtensions of their parent
  mapper directly, so that all methods for a particular MapperExtension
  are called for subclasses as well.  As always, any MapperExtension
  can return either EXT_CONTINUE to continue extension processing
  or EXT_STOP to stop processing.  The order of mapper resolution is:
  <extensions declared on the classes mapper> <extensions declared on the
  classes’ parent mapper> <globally declared extensions>.
  Note that if you instantiate the same extension class separately
  and then apply it individually for two mappers in the same inheritance
  chain, the extension will be applied twice to the inheriting class,
  and each method will be called twice.
  To apply a mapper extension explicitly to each inheriting class but
  have each method called only once per operation, use the same
  instance of the extension for both mappers.
  References: [#490](https://www.sqlalchemy.org/trac/ticket/490)
- MapperExtension.before_update() and after_update() are now called
  symmetrically; previously, an instance that had no modified column
  attributes (but had a relation() modification) could be called with
  before_update() but not after_update()
  References: [#907](https://www.sqlalchemy.org/trac/ticket/907)
- columns which are missing from a Query’s select statement
  now get automatically deferred during load.
- mapped classes which extend “object” and do not provide an
  __init__() method will now raise TypeError if non-empty *args
  or **kwargs are present at instance construction time (and are
  not consumed by any extensions such as the scoped_session mapper),
  consistent with the behavior of normal Python classes
  References: [#908](https://www.sqlalchemy.org/trac/ticket/908)
- fixed Query bug when filter_by() compares a relation against None
  References: [#899](https://www.sqlalchemy.org/trac/ticket/899)
- improved support for pickling of mapped entities.  Per-instance
  lazy/deferred/expired callables are now serializable so that
  they serialize and deserialize with _state.
- new synonym() behavior: an attribute will be placed on the mapped
  class, if one does not exist already, in all cases. if a property
  already exists on the class, the synonym will decorate the property
  with the appropriate comparison operators so that it can be used in
  column expressions just like any other mapped attribute (i.e. usable in
  filter(), etc.) the “proxy=True” flag is deprecated and no longer means
  anything. Additionally, the flag “map_column=True” will automatically
  generate a ColumnProperty corresponding to the name of the synonym,
  i.e.: ‘somename’:synonym(‘_somename’, map_column=True) will map the
  column named ‘somename’ to the attribute ‘_somename’. See the example
  in the mapper docs.
  References: [#801](https://www.sqlalchemy.org/trac/ticket/801)
- Query.select_from() now replaces all existing FROM criterion with
  the given argument; the previous behavior of constructing a list
  of FROM clauses was generally not useful as is required
  filter() calls to create join criterion, and new tables introduced
  within filter() already add themselves to the FROM clause.  The
  new behavior allows not just joins from the main table, but select
  statements as well.  Filter criterion, order bys, eager load
  clauses will be “aliased” against the given statement.
- this month’s refactoring of attribute instrumentation changes
  the “copy-on-load” behavior we’ve had since midway through 0.3
  with “copy-on-modify” in most cases.  This takes a sizable chunk
  of latency out of load operations and overall does less work
  as only attributes which are actually modified get their
  “committed state” copied.  Only “mutable scalar” attributes
  (i.e. a pickled object or other mutable item), the reason for
  the copy-on-load change in the first place, retain the old
  behavior.
- a slight behavioral change to attributes is, del’ing an attribute
  does *not* cause the lazyloader of that attribute to fire off again;
  the “del” makes the effective value of the attribute “None”.  To
  re-trigger the “loader” for an attribute, use
  session.expire(instance,).
- query.filter(SomeClass.somechild == None), when comparing
  a many-to-one property to None, properly generates “id IS NULL”
  including that the NULL is on the right side.
- query.order_by() takes into account aliased joins, i.e.
  query.join(‘orders’, aliased=True).order_by(Order.id)
- eagerload(), lazyload(), eagerload_all() take an optional
  second class-or-mapper argument, which will select the mapper
  to apply the option towards.  This can select among other
  mappers which were added using add_entity().
- eagerloading will work with mappers added via add_entity().
- added “cascade delete” behavior to “dynamic” relations just like
  that of regular relations.  if passive_deletes flag (also just added)
  is not set, a delete of the parent item will trigger a full load of
  the child items so that they can be deleted or updated accordingly.
- also with dynamic, implemented correct count() behavior as well
  as other helper methods.
- fix to cascades on polymorphic relations, such that cascades
  from an object to a polymorphic collection continue cascading
  along the set of attributes specific to each element in the collection.
- query.get() and query.load() do not take existing filter or other
  criterion into account; these methods *always* look up the given id
  in the database or return the current instance from the identity map,
  disregarding any existing filter, join, group_by or other criterion
  which has been configured.
  References: [#893](https://www.sqlalchemy.org/trac/ticket/893)
- added support for version_id_col in conjunction with inheriting mappers.
  version_id_col is typically set on the base mapper in an inheritance
  relationship where it takes effect for all inheriting mappers.
  References: [#883](https://www.sqlalchemy.org/trac/ticket/883)
- relaxed rules on column_property() expressions having labels; any
  ColumnElement is accepted now, as the compiler auto-labels non-labeled
  ColumnElements now.  a selectable, like a select() statement, still
  requires conversion to ColumnElement via as_scalar() or label().
- fixed backref bug where you could not del instance.attr if attr
  was None
- several ORM attributes have been removed or made private:
  mapper.get_attr_by_column(), mapper.set_attr_by_column(),
  mapper.pks_by_table, mapper.cascade_callable(),
  MapperProperty.cascade_callable(), mapper.canload(),
  mapper.save_obj(), mapper.delete_obj(), mapper._mapper_registry,
  attributes.AttributeManager
- Assigning an incompatible collection type to a relation attribute now
  raises TypeError instead of sqlalchemy’s ArgumentError.
- Bulk assignment of a MappedCollection now raises an error if a key in the
  incoming dictionary does not match the key that the collection’s keyfunc
  would use for that value.
  References: [#886](https://www.sqlalchemy.org/trac/ticket/886)
- Custom collections can now specify a @converter method to translate
  objects used in “bulk” assignment into a stream of values, as in:
  ```
  obj.col =
  # or
  obj.dictcol = {'foo': newval1, 'bar': newval2}
  ```
  The MappedCollection uses this hook to ensure that incoming key/value
  pairs are sane from the collection’s perspective.
- fixed endless loop issue when using lazy=”dynamic” on both
  sides of a bi-directional relationship
  References: [#872](https://www.sqlalchemy.org/trac/ticket/872)
- more fixes to the LIMIT/OFFSET aliasing applied with Query + eagerloads,
  in this case when mapped against a select statement
  References: [#904](https://www.sqlalchemy.org/trac/ticket/904)
- fix to self-referential eager loading such that if the same mapped
  instance appears in two or more distinct sets of columns in the same
  result set, its eagerly loaded collection will be populated regardless
  of whether or not all of the rows contain a set of “eager” columns for
  that collection.  this would also show up as a KeyError when fetching
  results with join_depth turned on.
- fixed bug where Query would not apply a subquery to the SQL when LIMIT
  was used in conjunction with an inheriting mapper where the eager
  loader was only in the parent mapper.
- clarified the error message which occurs when you try to update()
  an instance with the same identity key as an instance already present
  in the session.
- some clarifications and fixes to merge(instance, dont_load=True).
  fixed bug where lazy loaders were getting disabled on returned instances.
  Also, we currently do not support merging an instance which has uncommitted
  changes on it, in the case that dont_load=True is used….this will
  now raise an error.  This is due to complexities in merging the
  “committed state” of the given instance to correctly correspond to the
  newly copied instance, as well as other modified state.
  Since the use case for dont_load=True is caching, the given instances
  shouldn’t have any uncommitted changes on them anyway.
  We also copy the instances over without using any events now, so that
  the ‘dirty’ list on the new session remains unaffected.
- fixed bug which could arise when using session.begin_nested() in conjunction
  with more than one level deep of enclosing session.begin() statements
- fixed session.refresh() with instance that has custom entity_name
  References: [#914](https://www.sqlalchemy.org/trac/ticket/914)

### sql

- generic functions ! we introduce a database of known SQL functions, such
  as current_timestamp, coalesce, and create explicit function objects
  representing them. These objects have constrained argument lists, are
  type aware, and can compile in a dialect-specific fashion. So saying
  func.char_length(“foo”, “bar”) raises an error (too many args),
  func.coalesce(datetime.date(2007, 10, 5), datetime.date(2005, 10, 15))
  knows that its return type is a Date. We only have a few functions
  represented so far but will continue to add to the system
  References: [#615](https://www.sqlalchemy.org/trac/ticket/615)
- auto-reconnect support improved; a Connection can now automatically
  reconnect after its underlying connection is invalidated, without
  needing to connect() again from the engine.  This allows an ORM session
  bound to a single Connection to not need a reconnect.
  Open transactions on the Connection must be rolled back after an invalidation
  of the underlying connection else an error is raised.  Also fixed
  bug where disconnect detect was not being called for cursor(), rollback(),
  or commit().
- added new flag to String and create_engine(),
  assert_unicode=(True|False|’warn’|None). Defaults to False or None on
  create_engine() and String, ‘warn’ on the Unicode type. When True,
  results in all unicode conversion operations raising an exception when a
  non-unicode bytestring is passed as a bind parameter. ‘warn’ results
  in a warning. It is strongly advised that all unicode-aware applications
  make proper use of Python unicode objects (i.e. u’hello’ and not ‘hello’)
  so that data round trips accurately.
- generation of “unique” bind parameters has been simplified to use the same
  “unique identifier” mechanisms as everything else.  This doesn’t affect
  user code, except any code that might have been hardcoded against the generated
  names.  Generated bind params now have the form “<paramname>_<num>”,
  whereas before only the second bind of the same name would have this form.
- select().as_scalar() will raise an exception if the select does not have
  exactly one expression in its columns clause.
- bindparam() objects themselves can be used as keys for execute(), i.e.
  statement.execute({bind1:’foo’, bind2:’bar’})
- added new methods to TypeDecorator, process_bind_param() and
  process_result_value(), which automatically take advantage of the processing
  of the underlying type.  Ideal for using with Unicode or Pickletype.
  TypeDecorator should now be the primary way to augment the behavior of any
  existing type including other TypeDecorator subclasses such as PickleType.
- selectables (and others) will issue a warning when two columns in
  their exported columns collection conflict based on name.
- tables with schemas can still be used in sqlite, firebird,
  schema name just gets dropped
  References: [#890](https://www.sqlalchemy.org/trac/ticket/890)
- changed the various “literal” generation functions to use an anonymous
  bind parameter.  not much changes here except their labels now look
  like “:param_1”, “:param_2” instead of “:literal”
- column labels in the form “tablename.columname”, i.e. with a dot, are now
  supported.
- from_obj keyword argument to select() can be a scalar or a list.

### misc

- sqlite SLDate type will not erroneously render “microseconds” portion
  of a datetime or time object.
- oracle
  - added disconnect detection support for Oracle
  - some cleanup to binary/raw types so that cx_oracle.LOB is detected
    on an ad-hoc basis
  References: [#902](https://www.sqlalchemy.org/trac/ticket/902)
- MSSQL
  - PyODBC no longer has a global “set nocount on”.
  - Fix non-identity integer PKs on autoload
  - Better support for convert_unicode
  - Less strict date conversion for pyodbc/adodbapi
  - Schema-qualified tables / autoload
  References: [#824](https://www.sqlalchemy.org/trac/ticket/824), [#839](https://www.sqlalchemy.org/trac/ticket/839), [#842](https://www.sqlalchemy.org/trac/ticket/842), [#901](https://www.sqlalchemy.org/trac/ticket/901)
- does properly reflect domains (partially fixing) and
  PassiveDefaults
  References: [#410](https://www.sqlalchemy.org/trac/ticket/410)
- reverted to use default poolclass (was set to SingletonThreadPool in
  0.4.0 for test purposes)
- map func.length() to ‘char_length’ (easily overridable with the UDF
  ‘strlen’ on old versions of Firebird)

## 0.4.1

Released: Sun Nov 18 2007

### orm

- eager loading with LIMIT/OFFSET applied no longer adds the primary
  table joined to a limited subquery of itself; the eager loads now
  join directly to the subquery which also provides the primary table’s
  columns to the result set.  This eliminates a JOIN from all eager loads
  with LIMIT/OFFSET.
  References: [#843](https://www.sqlalchemy.org/trac/ticket/843)
- session.refresh() and session.expire() now support an additional argument
  “attribute_names”, a list of individual attribute keynames to be refreshed
  or expired, allowing partial reloads of attributes on an already-loaded
  instance.
  References: [#802](https://www.sqlalchemy.org/trac/ticket/802)
- added op() operator to instrumented attributes; i.e.
  User.name.op(‘ilike’)(‘%somename%’)
  References: [#767](https://www.sqlalchemy.org/trac/ticket/767)
- Mapped classes may now define __eq__, __hash__, and __nonzero__ methods
  with arbitrary semantics.  The orm now handles all mapped instances on
  an identity-only basis. (e.g. ‘is’ vs ‘==’)
  References: [#676](https://www.sqlalchemy.org/trac/ticket/676)
- the “properties” accessor on Mapper is removed; it now throws an informative
  exception explaining the usage of mapper.get_property() and
  mapper.iterate_properties
- added having() method to Query, applies HAVING to the generated statement
  in the same way as filter() appends to the WHERE clause.
- The behavior of query.options() is now fully based on paths, i.e. an
  option such as eagerload_all(‘x.y.z.y.x’) will apply eagerloading to
  only those paths, i.e. and not ‘x.y.x’; eagerload(‘children.children’)
  applies only to exactly two-levels deep, etc.
  References: [#777](https://www.sqlalchemy.org/trac/ticket/777)
- PickleType will compare using == when set up with mutable=False,
  and not the is operator.  To use is or any other comparator, send
  in a custom comparison function using PickleType(comparator=my_custom_comparator).
- query doesn’t throw an error if you use distinct() and an order_by()
  containing UnaryExpressions (or other) together
  References: [#848](https://www.sqlalchemy.org/trac/ticket/848)
- order_by() expressions from joined tables are properly added to columns
  clause when using distinct()
  References: [#786](https://www.sqlalchemy.org/trac/ticket/786)
- fixed error where Query.add_column() would not accept a class-bound
  attribute as an argument; Query also raises an error if an invalid
  argument was sent to add_column() (at instances() time)
  References: [#858](https://www.sqlalchemy.org/trac/ticket/858)
- added a little more checking for garbage-collection dereferences in
  InstanceState.__cleanup() to reduce “gc ignored” errors on app
  shutdown
- The session API has been solidified:
- It’s an error to session.save() an object which is already
  persistent
  References: [#840](https://www.sqlalchemy.org/trac/ticket/840)
- It’s an error to session.delete() an object which is *not*
  persistent.
- session.update() and session.delete() raise an error when updating
  or deleting an instance that is already in the session with a
  different identity.
- The session checks more carefully when determining “object X already
  in another session”; e.g. if you pickle a series of objects and
  unpickle (i.e. as in a Pylons HTTP session or similar), they can go
  into a new session without any conflict
- merge() includes a keyword argument “dont_load=True”.  setting this
  flag will cause the merge operation to not load any data from the
  database in response to incoming detached objects, and will accept
  the incoming detached object as though it were already present in
  that session.  Use this to merge detached objects from external
  caching systems into the session.
- Deferred column attributes no longer trigger a load operation when the
  attribute is assigned to.  In those cases, the newly assigned value
  will be present in the flushes’ UPDATE statement unconditionally.
- Fixed a truncation error when re-assigning a subset of a collection
  (obj.relation = obj.relation[1:])
  References: [#834](https://www.sqlalchemy.org/trac/ticket/834)
- De-cruftified backref configuration code, backrefs which step on
  existing properties now raise an error
  References: [#832](https://www.sqlalchemy.org/trac/ticket/832)
- Improved behavior of add_property() etc., fixed involving
  synonym/deferred.
  References: [#831](https://www.sqlalchemy.org/trac/ticket/831)
- Fixed clear_mappers() behavior to better clean up after itself.
- Fix to “row switch” behavior, i.e. when an INSERT/DELETE is combined
  into a single UPDATE; many-to-many relations on the parent object
  update properly.
  References: [#841](https://www.sqlalchemy.org/trac/ticket/841)
- Fixed __hash__ for association proxy- these collections are unhashable,
  just like their mutable Python counterparts.
- Added proxying of save_or_update, __contains__ and __iter__ methods for
  scoped sessions.
- fixed very hard-to-reproduce issue where by the FROM clause of Query
  could get polluted by certain generative calls
  References: [#852](https://www.sqlalchemy.org/trac/ticket/852)

### sql

- the “shortname” keyword parameter on bindparam() has been
  deprecated.
- Added contains operator (generates a “LIKE %<other>%” clause).
- anonymous column expressions are automatically labeled.
  e.g. select([x* 5]) produces “SELECT x * 5 AS anon_1”.
  This allows the labelname to be present in the cursor.description
  which can then be appropriately matched to result-column processing
  rules. (we can’t reliably use positional tracking for result-column
  matches since text() expressions may represent multiple columns).
- operator overloading is now controlled by TypeEngine objects - the
  one built-in operator overload so far is String types overloading
  ‘+’ to be the string concatenation operator.
  User-defined types can also define their own operator overloading
  by overriding the adapt_operator(self, op) method.
- untyped bind parameters on the right side of a binary expression
  will be assigned the type of the left side of the operation, to better
  enable the appropriate bind parameter processing to take effect
  References: [#819](https://www.sqlalchemy.org/trac/ticket/819)
- Removed regular expression step from most statement compilations.
  Also fixes
  References: [#833](https://www.sqlalchemy.org/trac/ticket/833)
- Fixed empty (zero column) sqlite inserts, allowing inserts on
  autoincrementing single column tables.
- Fixed expression translation of text() clauses; this repairs various
  ORM scenarios where literal text is used for SQL expressions
- Removed ClauseParameters object; compiled.params returns a regular
  dictionary now, as well as result.last_inserted_params() /
  last_updated_params().
- Fixed INSERT statements w.r.t. primary key columns that have
  SQL-expression based default generators on them; SQL expression
  executes inline as normal but will not trigger a “postfetch” condition
  for the column, for those DB’s who provide it via cursor.lastrowid
- func. objects can be pickled/unpickled
  References: [#844](https://www.sqlalchemy.org/trac/ticket/844)
- rewrote and simplified the system used to “target” columns across
  selectable expressions.  On the SQL side this is represented by the
  “corresponding_column()” method. This method is used heavily by the ORM
  to “adapt” elements of an expression to similar, aliased expressions,
  as well as to target result set columns originally bound to a
  table or selectable to an aliased, “corresponding” expression.  The new
  rewrite features completely consistent and accurate behavior.
- Added a field (“info”) for storing arbitrary data on schema items
  References: [#573](https://www.sqlalchemy.org/trac/ticket/573)
- The “properties” collection on Connections has been renamed “info” to
  match schema’s writable collections.  Access is still available via
  the “properties” name until 0.5.
- fixed the close() method on Transaction when using strategy=’threadlocal’
- fix to compiled bind parameters to not mistakenly populate None
  References: [#853](https://www.sqlalchemy.org/trac/ticket/853)
- <Engine|Connection>._execute_clauseelement becomes a public method
  Connectable.execute_clauseelement

### misc

- Added experimental support for MaxDB (versions >= 7.6.03.007 only).
- oracle will now reflect “DATE” as an OracleDateTime column, not
  OracleDate
- added awareness of schema name in oracle table_names() function,
  fixes metadata.reflect(schema=’someschema’)
  References: [#847](https://www.sqlalchemy.org/trac/ticket/847)
- MSSQL anonymous labels for selection of functions made deterministic
- sqlite will reflect “DECIMAL” as a numeric column.
- Made access dao detection more reliable
  References: [#828](https://www.sqlalchemy.org/trac/ticket/828)
- Renamed the Dialect attribute ‘preexecute_sequences’ to
  ‘preexecute_pk_sequences’.  An attribute proxy is in place for
  out-of-tree dialects using the old name.
- Added test coverage for unknown type reflection. Fixed sqlite/mysql
  handling of type reflection for unknown types.
- Added REAL for mysql dialect (for folks exploiting the
  REAL_AS_FLOAT sql mode).
- mysql Float, MSFloat and MSDouble constructed without arguments
  now produce no-argument DDL, e.g.’FLOAT’.
- Removed unused util.hash().

## 0.4.0

Released: Wed Oct 17 2007

- (see 0.4.0beta1 for the start of major changes against 0.3,
  as well as [https://www.sqlalchemy.org/trac/wiki/WhatsNewIn04](https://www.sqlalchemy.org/trac/wiki/WhatsNewIn04) )
- Added initial Sybase support (mxODBC so far)
  References: [#785](https://www.sqlalchemy.org/trac/ticket/785)
- Added partial index support for PostgreSQL. Use the postgres_where keyword
  on the Index.
- string-based query param parsing/config file parser understands
  wider range of string values for booleans
  References: [#817](https://www.sqlalchemy.org/trac/ticket/817)
- backref remove object operation doesn’t fail if the other-side
  collection doesn’t contain the item, supports noload collections
  References: [#813](https://www.sqlalchemy.org/trac/ticket/813)
- removed __len__ from “dynamic” collection as it would require issuing
  a SQL “count()” operation, thus forcing all list evaluations to issue
  redundant SQL
  References: [#818](https://www.sqlalchemy.org/trac/ticket/818)
- inline optimizations added to locate_dirty() which can greatly speed up
  repeated calls to flush(), as occurs with autoflush=True
  References: [#816](https://www.sqlalchemy.org/trac/ticket/816)
- The IdentifierPreprarer’s _requires_quotes test is now regex based.  Any
  out-of-tree dialects that provide custom sets of legal_characters or
  illegal_initial_characters will need to move to regexes or override
  _requires_quotes.
- Firebird has supports_sane_rowcount and supports_sane_multi_rowcount set
  to False due to ticket #370 (right way).
- Improvements and fixes on Firebird reflection:
  - FBDialect now mimics OracleDialect, regarding case-sensitivity of TABLE and
    COLUMN names (see ‘case_sensitive remotion’ topic on this current file).
  - FBDialect.table_names() doesn’t bring system tables (ticket:796).
  - FB now reflects Column’s nullable property correctly.
- Fixed SQL compiler’s awareness of top-level column labels as used
  in result-set processing; nested selects which contain the same column
  names don’t affect the result or conflict with result-column metadata.
- query.get() and related functions (like many-to-one lazyloading)
  use compile-time-aliased bind parameter names, to prevent
  name conflicts with bind parameters that already exist in the
  mapped selectable.
- Fixed three- and multi-level select and deferred inheritance loading
  (i.e. abc inheritance with no select_table).
  References: [#795](https://www.sqlalchemy.org/trac/ticket/795)
- Ident passed to id_chooser in shard.py always a list.
- The no-arg ResultProxy._row_processor() is now the class attribute
  _process_row.
- Added support for returning values from inserts and updates for
  PostgreSQL 8.2+.
  References: [#797](https://www.sqlalchemy.org/trac/ticket/797)
- PG reflection, upon seeing the default schema name being used explicitly
  as the “schema” argument in a Table, will assume that this is the
  user’s desired convention, and will explicitly set the “schema” argument
  in foreign-key-related reflected tables, thus making them match only
  with Table constructors that also use the explicit “schema” argument
  (even though its the default schema).
  In other words, SA assumes the user is being consistent in this usage.
- fixed sqlite reflection of BOOL/BOOLEAN
  References: [#808](https://www.sqlalchemy.org/trac/ticket/808)
- Added support for UPDATE with LIMIT on mysql.
- null foreign key on a m2o doesn’t trigger a lazyload
  References: [#803](https://www.sqlalchemy.org/trac/ticket/803)
- oracle does not implicitly convert to unicode for non-typed result
  sets (i.e. when no TypeEngine/String/Unicode type is even being used;
  previously it was detecting DBAPI types and converting regardless).
  should fix
  References: [#800](https://www.sqlalchemy.org/trac/ticket/800)
- fix to anonymous label generation of long table/column names
  References: [#806](https://www.sqlalchemy.org/trac/ticket/806)
- Firebird dialect now uses SingletonThreadPool as poolclass.
- Firebird now uses dialect.preparer to format sequences names
- Fixed breakage with postgres and multiple two-phase transactions. Two-phase
  commits and rollbacks didn’t automatically end up with a new transaction
  as the usual dbapi commits/rollbacks do.
  References: [#810](https://www.sqlalchemy.org/trac/ticket/810)
- Added an option to the _ScopedExt mapper extension to not automatically
  save new objects to session on object initialization.
- fixed Oracle non-ansi join syntax
- PickleType and Interval types (on db not supporting it natively) are now
  slightly faster.
- Added Float and Time types to Firebird (FBFloat and FBTime). Fixed
  BLOB SUB_TYPE for TEXT and Binary types.
- Changed the API for the in_ operator. in_() now accepts a single argument
  that is a sequence of values or a selectable. The old API of passing in
  values as varargs still works but is deprecated.

## 0.4.0beta6

Released: Thu Sep 27 2007

- The Session identity map is now *weak referencing* by default, use
  weak_identity_map=False to use a regular dict.  The weak dict we are using
  is customized to detect instances which are “dirty” and maintain a
  temporary strong reference to those instances until changes are flushed.
- Mapper compilation has been reorganized such that most compilation occurs
  upon mapper construction.  This allows us to have fewer calls to
  mapper.compile() and also to allow class-based properties to force a
  compilation (i.e. User.addresses == 7 will compile all mappers; this is).  The only caveat here is that an inheriting mapper now
  looks for its inherited mapper upon construction; so mappers within
  inheritance relationships need to be constructed in inheritance order
  (which should be the normal case anyway).
  References: [#758](https://www.sqlalchemy.org/trac/ticket/758)
- added “FETCH” to the keywords detected by Postgres to indicate a
  result-row holding statement (i.e. in addition to “SELECT”).
- Added full list of SQLite reserved keywords so that they get escaped
  properly.
- Tightened up the relationship between the Query’s generation of “eager
  load” aliases, and Query.instances() which actually grabs the eagerly
  loaded rows.  If the aliases were not specifically generated for that
  statement by EagerLoader, the EagerLoader will not take effect when the
  rows are fetched.  This prevents columns from being grabbed accidentally
  as being part of an eager load when they were not meant for such, which
  can happen with textual SQL as well as some inheritance situations.  It’s
  particularly important since the “anonymous aliasing” of columns uses
  simple integer counts now to generate labels.
- Removed “parameters” argument from clauseelement.compile(), replaced with
  “column_keys”.  The parameters sent to execute() only interact with the
  insert/update statement compilation process in terms of the column names
  present but not the values for those columns.  Produces more consistent
  execute/executemany behavior, simplifies things a bit internally.
- Added ‘comparator’ keyword argument to PickleType.  By default, “mutable”
  PickleType does a “deep compare” of objects using their dumps()
  representation.  But this doesn’t work for dictionaries.  Pickled objects
  which provide an adequate __eq__() implementation can be set up with
  “PickleType(comparator=operator.eq)”
  References: [#560](https://www.sqlalchemy.org/trac/ticket/560)
- Added session.is_modified(obj) method; performs the same “history”
  comparison operation as occurs within a flush operation; setting
  include_collections=False gives the same result as is used when the flush
  determines whether or not to issue an UPDATE for the instance’s row.
- Added “schema” argument to Sequence; use this with Postgres /Oracle when
  the sequence is located in an alternate schema.  Implements part of, should fix.
  References: [#584](https://www.sqlalchemy.org/trac/ticket/584), [#761](https://www.sqlalchemy.org/trac/ticket/761)
- Fixed reflection of the empty string for mysql enums.
- Changed MySQL dialect to use the older LIMIT <offset>, <limit> syntax
  instead of LIMIT <l> OFFSET <o> for folks using 3.23.
  References: [#794](https://www.sqlalchemy.org/trac/ticket/794)
- Added ‘passive_deletes=”all”’ flag to relation(), disables all nulling-out
  of foreign key attributes during a flush where the parent object is
  deleted.
- Column defaults and onupdates, executing inline, will add parenthesis for
  subqueries and other parenthesis-requiring expressions
- The behavior of String/Unicode types regarding that they auto-convert to
  TEXT/CLOB when no length is present now occurs *only* for an exact type of
  String or Unicode with no arguments.  If you use VARCHAR or NCHAR
  (subclasses of String/Unicode) with no length, they will be interpreted by
  the dialect as VARCHAR/NCHAR; no “magic” conversion happens there.  This
  is less surprising behavior and in particular this helps Oracle keep
  string-based bind parameters as VARCHARs and not CLOBs.
  References: [#793](https://www.sqlalchemy.org/trac/ticket/793)
- Fixes to ShardedSession to work with deferred columns.
  References: [#771](https://www.sqlalchemy.org/trac/ticket/771)
- User-defined shard_chooser() function must accept “clause=None” argument;
  this is the ClauseElement passed to session.execute(statement) and can be
  used to determine correct shard id (since execute() doesn’t take an
  instance.)
- Adjusted operator precedence of NOT to match ‘==’ and others, so that
  ~(x <operator> y) produces NOT (x <op> y), which is better compatible
  with older MySQL versions..  This doesn’t apply to “~(x==y)”
  as it does in 0.3 since ~(x==y) compiles to “x != y”, but still applies
  to operators like BETWEEN.
  References: [#764](https://www.sqlalchemy.org/trac/ticket/764)
- Other tickets:,,.
  References: [#728](https://www.sqlalchemy.org/trac/ticket/728), [#757](https://www.sqlalchemy.org/trac/ticket/757), [#768](https://www.sqlalchemy.org/trac/ticket/768), [#779](https://www.sqlalchemy.org/trac/ticket/779)

## 0.4.0beta5

no release date

- Connection pool fixes; the better performance of beta4 remains but fixes
  “connection overflow” and other bugs which were present (like).
  References: [#754](https://www.sqlalchemy.org/trac/ticket/754)
- Fixed bugs in determining proper sync clauses from custom inherit
  conditions.
  References: [#769](https://www.sqlalchemy.org/trac/ticket/769)
- Extended ‘engine_from_config’ coercion for QueuePool size / overflow.
  References: [#763](https://www.sqlalchemy.org/trac/ticket/763)
- mysql views can be reflected again.
  References: [#748](https://www.sqlalchemy.org/trac/ticket/748)
- AssociationProxy can now take custom getters and setters.
- Fixed malfunctioning BETWEEN in orm queries.
- Fixed OrderedProperties pickling
  References: [#762](https://www.sqlalchemy.org/trac/ticket/762)
- SQL-expression defaults and sequences now execute “inline” for all
  non-primary key columns during an INSERT or UPDATE, and for all columns
  during an executemany()-style call. inline=True flag on any insert/update
  statement also forces the same behavior with a single execute().
  result.postfetch_cols() is a collection of columns for which the previous
  single insert or update statement contained a SQL-side default expression.
- Fixed PG executemany() behavior.
  References: [#759](https://www.sqlalchemy.org/trac/ticket/759)
- postgres reflects tables with autoincrement=False for primary key columns
  which have no defaults.
- postgres no longer wraps executemany() with individual execute() calls,
  instead favoring performance.  “rowcount”/”concurrency” checks with
  deleted items (which use executemany) are disabled with PG since psycopg2
  does not report proper rowcount for executemany().
- References: [#742](https://www.sqlalchemy.org/trac/ticket/742)
- References: [#748](https://www.sqlalchemy.org/trac/ticket/748)
- References: [#760](https://www.sqlalchemy.org/trac/ticket/760)
- References: [#762](https://www.sqlalchemy.org/trac/ticket/762)
- References: [#763](https://www.sqlalchemy.org/trac/ticket/763)

## 0.4.0beta4

Released: Wed Aug 22 2007

- Tidied up what ends up in your namespace when you ‘from sqlalchemy import *’:
- ’table’ and ‘column’ are no longer imported.  They remain available by
  direct reference (as in ‘sql.table’ and ‘sql.column’) or a glob import
  from the sql package.  It was too easy to accidentally use a
  sql.expressions.table instead of schema.Table when just starting out
  with SQLAlchemy, likewise column.
- Internal-ish classes like ClauseElement, FromClause, NullTypeEngine,
  etc., are also no longer imported into your namespace
- The ‘Smallinteger’ compatibility name (small i!) is no longer imported,
  but remains in schema.py for now.  SmallInteger (big I!) is still
  imported.
- The connection pool uses a “threadlocal” strategy internally to return
  the same connection already bound to a thread, for “contextual” connections;
  these are the connections used when you do a “connectionless” execution
  like insert().execute().  This is like a “partial” version of the
  “threadlocal” engine strategy but without the thread-local transaction part
  of it.  We’re hoping it reduces connection pool overhead as well as
  database usage.  However, if it proves to impact stability in a negative way,
  we’ll roll it right back.
- Fix to bind param processing such that “False” values (like blank strings)
  still get processed/encoded.
- Fix to select() “generative” behavior, such that calling column(),
  select_from(), correlate(), and with_prefix() does not modify the
  original select object
  References: [#752](https://www.sqlalchemy.org/trac/ticket/752)
- Added a “legacy” adapter to types, such that user-defined TypeEngine
  and TypeDecorator classes which define convert_bind_param() and/or
  convert_result_value() will continue to function.  Also supports
  calling the super() version of those methods.
- Added session.prune(), trims away instances cached in a session that
  are no longer referenced elsewhere. (A utility for strong-ref
  identity maps).
- Added close() method to Transaction.  Closes out a transaction using
  rollback if it’s the outermost transaction, otherwise just ends
  without affecting the outer transaction.
- Transactional and non-transactional Session integrates better with
  bound connection; a close() will ensure that connection
  transactional state is the same as that which existed on it before
  being bound to the Session.
- Modified SQL operator functions to be module-level operators,
  allowing SQL expressions to be pickleable.
  References: [#735](https://www.sqlalchemy.org/trac/ticket/735)
- Small adjustment to mapper class.__init__ to allow for Py2.6
  object.__init__() behavior.
- Fixed ‘prefix’ argument for select()
- Connection.begin() no longer accepts nested=True, this logic is now
  all in begin_nested().
- Fixes to new “dynamic” relation loader involving cascades
- References: [#735](https://www.sqlalchemy.org/trac/ticket/735)
- References: [#752](https://www.sqlalchemy.org/trac/ticket/752)

## 0.4.0beta3

Released: Thu Aug 16 2007

- SQL types optimization:
- New performance tests show a combined mass-insert/mass-select test as
  having 68% fewer function calls than the same test run against 0.3.
- General performance improvement of result set iteration is around 10-20%.
- In types.AbstractType, convert_bind_param() and convert_result_value()
  have migrated to callable-returning bind_processor() and
  result_processor() methods.  If no callable is returned, no pre/post
  processing function is called.
- Hooks added throughout base/sql/defaults to optimize the calling of bind
  param/result processors so that method call overhead is minimized.
- Support added for executemany() scenarios such that unneeded “last row id”
  logic doesn’t kick in, parameters aren’t excessively traversed.
- Added ‘inherit_foreign_keys’ arg to mapper().
- Added support for string date passthrough in sqlite.
- References: [#738](https://www.sqlalchemy.org/trac/ticket/738)
- References: [#739](https://www.sqlalchemy.org/trac/ticket/739)
- References: [#743](https://www.sqlalchemy.org/trac/ticket/743)
- References: [#744](https://www.sqlalchemy.org/trac/ticket/744)

## 0.4.0beta2

Released: Tue Aug 14 2007

### oracle

- Auto-commit after LOAD DATA INFILE for mysql.
- A rudimental SessionExtension class has been added, allowing user-defined
  functionality to take place at flush(), commit(), and rollback() boundaries.
- Added engine_from_config() function for helping to create_engine() from an
  .ini style config.
- base_mapper() becomes a plain attribute.
- session.execute() and scalar() can search for a Table with which to bind from
  using the given ClauseElement.
- Session automatically extrapolates tables from mappers with binds, also uses
  base_mapper so that inheritance hierarchies bind automatically.
- Moved ClauseVisitor traversal back to inlined non-recursive.

### misc

- References: [#730](https://www.sqlalchemy.org/trac/ticket/730)
- References: [#732](https://www.sqlalchemy.org/trac/ticket/732)
- References: [#733](https://www.sqlalchemy.org/trac/ticket/733)
- References: [#734](https://www.sqlalchemy.org/trac/ticket/734)

## 0.4.0beta1

Released: Sun Aug 12 2007

### orm

- Speed! Along with recent speedups to ResultProxy, total number of function
  calls significantly reduced for large loads.
- test/perf/masseagerload.py reports 0.4 as having the fewest number of
  function calls across all SA versions (0.1, 0.2, and 0.3).
- New collection_class api and implementation. Collections are
  now instrumented via decorations rather than proxying.  You can now have
  collections that manage their own membership, and your class instance will
  be directly exposed on the relation property.  The changes are transparent
  for most users.
  References: [#213](https://www.sqlalchemy.org/trac/ticket/213)
- InstrumentedList (as it was) is removed, and relation properties no
  longer have ‘clear()’, ‘.data’, or any other added methods beyond those
  provided by the collection type. You are free, of course, to add them to
  a custom class.
- __setitem__-like assignments now fire remove events for the existing
  value, if any.
- dict-likes used as collection classes no longer need to change __iter__
  semantics- itervalues() is used by default instead. This is a backwards
  incompatible change.
- Subclassing dict for a mapped collection is no longer needed in most
  cases. orm.collections provides canned implementations that key objects
  by a specified column or a custom function of your choice.
- Collection assignment now requires a compatible type- assigning None to
  clear a collection or assigning a list to a dict collection will now
  raise an argument error.
- AttributeExtension moved to interfaces, and .delete is now .remove The
  event method signature has also been swapped around.
- Major overhaul for Query:
- All selectXXX methods are deprecated.  Generative methods are now the
  standard way to do things, i.e. filter(), filter_by(), all(), one(),
  etc.  Deprecated methods are docstring’ed with their new replacements.
- Class-level properties are now usable as query elements… no more
  ‘.c.’!  “Class.c.propname” is now superseded by “Class.propname”.  All
  clause operators are supported, as well as higher level operators such
  as Class.prop==<some instance> for scalar attributes,
  Class.prop.contains(<some instance>) and Class.prop.any(<some
  expression>) for collection-based attributes (all are also
  negatable).  Table-based column expressions as well as columns mounted
  on mapped classes via ‘c’ are of course still fully available and can be
  freely mixed with the new attributes.
  References: [#643](https://www.sqlalchemy.org/trac/ticket/643)
- Removed ancient query.select_by_attributename() capability.
- The aliasing logic used by eager loading has been generalized, so that
  it also adds full automatic aliasing support to Query.  It’s no longer
  necessary to create an explicit Alias to join to the same tables
  multiple times; *even for self-referential relationships*.
  - join() and outerjoin() take arguments “aliased=True”.  Yhis causes
    their joins to be built on aliased tables; subsequent calls to
    filter() and filter_by() will translate all table expressions (yes,
    real expressions using the original mapped Table) to be that of the
    Alias for the duration of that join() (i.e. until reset_joinpoint() or
    another join() is called).
  - join() and outerjoin() take arguments “id=<somestring>”.  When used
    with “aliased=True”, the id can be referenced by add_entity(cls,
    id=<somestring>) so that you can select the joined instances even if
    they’re from an alias.
  - join() and outerjoin() now work with self-referential relationships!
    Using “aliased=True”, you can join as many levels deep as desired,
    i.e. query.join([‘children’, ‘children’], aliased=True); filter
    criterion will be against the rightmost joined table
- Added query.populate_existing(), marks the query to reload all
  attributes and collections of all instances touched in the query,
  including eagerly-loaded entities.
  References: [#660](https://www.sqlalchemy.org/trac/ticket/660)
- Added eagerload_all(), allows eagerload_all(‘x.y.z’) to specify eager
  loading of all properties in the given path.
- Major overhaul for Session:
- New function which “configures” a session called “sessionmaker()”.  Send
  various keyword arguments to this function once, returns a new class
  which creates a Session against that stereotype.
- SessionTransaction removed from “public” API.  You now can call begin()/
  commit()/rollback() on the Session itself.
- Session also supports SAVEPOINT transactions; call begin_nested().
- Session supports two-phase commit behavior when vertically or
  horizontally partitioning (i.e., using more than one engine).  Use
  twophase=True.
- Session flag “transactional=True” produces a session which always places
  itself into a transaction when first used.  Upon commit(), rollback() or
  close(), the transaction ends; but begins again on the next usage.
- Session supports “autoflush=True”.  This issues a flush() before each
  query.  Use in conjunction with transactional, and you can just
  save()/update() and then query, the new objects will be there.  Use
  commit() at the end (or flush() if non-transactional) to flush remaining
  changes.
- New scoped_session() function replaces SessionContext and assignmapper.
  Builds onto “sessionmaker()” concept to produce a class whose Session()
  construction returns the thread-local session.  Or, call all Session
  methods as class methods, i.e. Session.save(foo); Session.commit().
  just like the old “objectstore” days.
- Added new “binds” argument to Session to support configuration of
  multiple binds with sessionmaker() function.
- A rudimental SessionExtension class has been added, allowing
  user-defined functionality to take place at flush(), commit(), and
  rollback() boundaries.
- Query-based relation()s available with dynamic_loader().  This is a
  *writable* collection (supporting append() and remove()) which is also a
  live Query object when accessed for reads.  Ideal for dealing with very
  large collections where only partial loading is desired.
- flush()-embedded inline INSERT/UPDATE expressions.  Assign any SQL
  expression, like “sometable.c.column + 1”, to an instance’s attribute.
  Upon flush(), the mapper detects the expression and embeds it directly in
  the INSERT or UPDATE statement; the attribute gets deferred on the
  instance so it loads the new value the next time you access it.
- A rudimental sharding (horizontal scaling) system is introduced.  This
  system uses a modified Session which can distribute read and write
  operations among multiple databases, based on user-defined functions
  defining the “sharding strategy”.  Instances and their dependents can be
  distributed and queried among multiple databases based on attribute
  values, round-robin approaches or any other user-defined
  system.
  References: [#618](https://www.sqlalchemy.org/trac/ticket/618)
- Eager loading has been enhanced to allow even more joins in more places.
  It now functions at any arbitrary depth along self-referential and
  cyclical structures.  When loading cyclical structures, specify
  “join_depth” on relation() indicating how many times you’d like the table
  to join to itself; each level gets a distinct table alias.  The alias
  names themselves are generated at compile time using a simple counting
  scheme now and are a lot easier on the eyes, as well as of course
  completely deterministic.
  References: [#659](https://www.sqlalchemy.org/trac/ticket/659)
- Added composite column properties.  This allows you to create a type which
  is represented by more than one column, when using the ORM.  Objects of
  the new type are fully functional in query expressions, comparisons,
  query.get() clauses, etc. and act as though they are regular single-column
  scalars… except they’re not!  Use the function composite(cls, *columns)
  inside of the mapper’s “properties” dict, and instances of cls will be
  created/mapped to a single attribute, comprised of the values corresponding
  to *columns.
  References: [#211](https://www.sqlalchemy.org/trac/ticket/211)
- Improved support for custom column_property() attributes which feature
  correlated subqueries, works better with eager loading now.
- Primary key “collapse” behavior; the mapper will analyze all columns in
  its given selectable for primary key “equivalence”, that is, columns which
  are equivalent via foreign key relationship or via an explicit
  inherit_condition. primarily for joined-table inheritance scenarios where
  different named PK columns in inheriting tables should “collapse” into a
  single-valued (or fewer-valued) primary key.  Fixes things like.
  References: [#611](https://www.sqlalchemy.org/trac/ticket/611)
- Joined-table inheritance will now generate the primary key columns of all
  inherited classes against the root table of the join only.  This implies
  that each row in the root table is distinct to a single instance.  If for
  some rare reason this is not desirable, explicit primary_key settings on
  individual mappers will override it.
- When “polymorphic” flags are used with joined-table or single-table
  inheritance, all identity keys are generated against the root class of the
  inheritance hierarchy; this allows query.get() to work polymorphically
  using the same caching semantics as a non-polymorphic get.  Note that this
  currently does not work with concrete inheritance.
- Secondary inheritance loading: polymorphic mappers can be constructed
  *without* a select_table argument. inheriting mappers whose tables were
  not represented in the initial load will issue a second SQL query
  immediately, once per instance (i.e. not very efficient for large lists),
  in order to load the remaining columns.
- Secondary inheritance loading can also move its second query into a
  column-level “deferred” load, via the “polymorphic_fetch” argument, which
  can be set to ‘select’ or ‘deferred’
- It’s now possible to map only a subset of available selectable columns
  onto mapper properties, using include_columns/exclude_columns..
  References: [#696](https://www.sqlalchemy.org/trac/ticket/696)
- Added undefer_group() MapperOption, sets a set of “deferred” columns
  joined by a “group” to load as “undeferred”.
- Rewrite of the “deterministic alias name” logic to be part of the SQL
  layer, produces much simpler alias and label names more in the style of
  Hibernate

### sql

- Speed!  Clause compilation as well as the mechanics of SQL constructs have
  been streamlined and simplified to a significant degree, for a 20-30%
  improvement of the statement construction/compilation overhead of 0.3.
- All “type” keyword arguments, such as those to bindparam(), column(),
  Column(), and func.<something>(), renamed to “type_”.  Those objects still
  name their “type” attribute as “type”.
- case_sensitive=(True|False) setting removed from schema items, since
  checking this state added a lot of method call overhead and there was no
  decent reason to ever set it to False.  Table and column names which are
  all lower case will be treated as case-insensitive (yes we adjust for
  Oracle’s UPPERCASE style too).

### extensions

- proxyengine is temporarily removed, pending an actually working
  replacement.
- SelectResults has been replaced by Query.  SelectResults /
  SelectResultsExt still exist but just return a slightly modified Query
  object for backwards-compatibility.  join_to() method from SelectResults
  isn’t present anymore, need to use join().

### mysql

- Table and column names loaded via reflection are now Unicode.
- All standard column types are now supported, including SET.
- Table reflection can now be performed in as little as one round-trip.
- ANSI and ANSI_QUOTES sql modes are now supported.
- Indexes are now reflected.

### oracle

- Very rudimental support for OUT parameters added; use sql.outparam(name,
  type) to set up an OUT parameter, just like bindparam(); after execution,
  values are available via result.out_parameters dictionary.
  References: [#507](https://www.sqlalchemy.org/trac/ticket/507)

### misc

- Added context manager (with statement) support for transactions.
- Added support for two phase commit, works with mysql and postgres so far.
- Added a subtransaction implementation that uses savepoints.
- Added support for savepoints.
- Tables can be reflected from the database en-masse without declaring
  them in advance.  MetaData(engine, reflect=True) will load all tables
  present in the database, or use metadata.reflect() for finer control.
- DynamicMetaData has been renamed to ThreadLocalMetaData
- The ThreadLocalMetaData constructor now takes no arguments.
- BoundMetaData has been removed- regular MetaData is equivalent
- Numeric and Float types now have an “asdecimal” flag; defaults to True for
  Numeric, False for Float.  When True, values are returned as
  decimal.Decimal objects; when False, values are returned as float().  The
  defaults of True/False are already the behavior for PG and MySQL’s DBAPI
  modules.
  References: [#646](https://www.sqlalchemy.org/trac/ticket/646)
- New SQL operator implementation which removes all hardcoded operators from
  expression structures and moves them into compilation; allows greater
  flexibility of operator compilation; for example, “+” compiles to “||”
  when used in a string context, or “concat(a,b)” on MySQL; whereas in a
  numeric context it compiles to “+”.  Fixes.
  References: [#475](https://www.sqlalchemy.org/trac/ticket/475)
- ”Anonymous” alias and label names are now generated at SQL compilation
  time in a completely deterministic fashion… no more random hex IDs
- Significant architectural overhaul to SQL elements (ClauseElement).  All
  elements share a common “mutability” framework which allows a consistent
  approach to in-place modifications of elements as well as generative
  behavior.  Improves stability of the ORM which makes heavy usage of
  mutations to SQL expressions.
- select() and union()’s now have “generative” behavior.  Methods like
  order_by() and group_by() return a *new* instance - the original instance
  is left unchanged.  Non-generative methods remain as well.
- The internals of select/union vastly simplified- all decision making
  regarding “is subquery” and “correlation” pushed to SQL generation phase.
  select() elements are now *never* mutated by their enclosing containers or
  by any dialect’s compilation process
  References: [#52](https://www.sqlalchemy.org/trac/ticket/52), [#569](https://www.sqlalchemy.org/trac/ticket/569)
- select(scalar=True) argument is deprecated; use select(..).as_scalar().
  The resulting object obeys the full “column” interface and plays better
  within expressions.
- Added select().with_prefix(‘foo’) allowing any set of keywords to be
  placed before the columns clause of the SELECT
  References: [#504](https://www.sqlalchemy.org/trac/ticket/504)
- Added array slice support to row[<index>]
  References: [#686](https://www.sqlalchemy.org/trac/ticket/686)
- Result sets make a better attempt at matching the DBAPI types present in
  cursor.description to the TypeEngine objects defined by the dialect, which
  are then used for result-processing. Note this only takes effect for
  textual SQL; constructed SQL statements always have an explicit type map.
- Result sets from CRUD operations close their underlying cursor immediately
  and will also autoclose the connection if defined for the operation; this
  allows more efficient usage of connections for successive CRUD operations
  with less chance of “dangling connections”.
- Column defaults and onupdate Python functions (i.e. passed to
  ColumnDefault) may take zero or one arguments; the one argument is the
  ExecutionContext, from which you can call “context.parameters[someparam]”
  to access the other bind parameter values affixed to the statement.  The connection used for the execution is available as well
  so that you can pre-execute statements.
  References: [#559](https://www.sqlalchemy.org/trac/ticket/559)
- Added “explicit” create/drop/execute support for sequences (i.e. you can
  pass a “connectable” to each of those methods on Sequence).
- Better quoting of identifiers when manipulating schemas.
- Standardized the behavior for table reflection where types can’t be
  located; NullType is substituted instead, warning is raised.
- ColumnCollection (i.e. the ‘c’ attribute on tables) follows dictionary
  semantics for “__contains__”
  References: [#606](https://www.sqlalchemy.org/trac/ticket/606)
- Speed! The mechanics of result processing and bind parameter processing
  have been overhauled, streamlined and optimized to issue as little method
  calls as possible.  Bench tests for mass INSERT and mass rowset iteration
  both show 0.4 to be over twice as fast as 0.3, using 68% fewer function
  calls.
- You can now hook into the pool lifecycle and run SQL statements or other
  logic at new each DBAPI connection, pool check-out and check-in.
- Connections gain a .properties collection, with contents scoped to the
  lifetime of the underlying DBAPI connection
- Removed auto_close_cursors and disallow_open_cursors arguments from Pool;
  reduces overhead as cursors are normally closed by ResultProxy and
  Connection.
- Added PGArray datatype for using postgres array datatypes.
