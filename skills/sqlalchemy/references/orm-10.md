# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# ORM Examples

The SQLAlchemy distribution includes a variety of code examples illustrating
a select set of patterns, some typical and some not so typical.   All are
runnable and can be found in the `/examples` directory of the
distribution.   Descriptions and source code for all can be found here.

Additional SQLAlchemy examples, some user contributed, are available on the
wiki at [https://www.sqlalchemy.org/trac/wiki/UsageRecipes](https://www.sqlalchemy.org/trac/wiki/UsageRecipes).

## Mapping Recipes

### Adjacency List

An example of a dictionary-of-dictionaries structure mapped using
an adjacency list model.

E.g.:

```
node = TreeNode("rootnode")
node.append("node1")
node.append("node3")
session.add(node)
session.commit()

dump_tree(node)
```

Listing of files:

- [adjacency_list.py](https://docs.sqlalchemy.org/en/20/_modules/examples/adjacency_list/adjacency_list.html)

### Associations

Examples illustrating the usage of the “association object” pattern,
where an intermediary class mediates the relationship between two
classes that are associated in a many-to-many pattern.

Listing of files:

- [basic_association.py](https://docs.sqlalchemy.org/en/20/_modules/examples/association/basic_association.html) - Illustrate a many-to-many relationship between an
  “Order” and a collection of “Item” objects, associating a purchase price
  with each via an association object called “OrderItem”
- [dict_of_sets_with_default.py](https://docs.sqlalchemy.org/en/20/_modules/examples/association/dict_of_sets_with_default.html) - An advanced association proxy example which
  illustrates nesting of association proxies to produce multi-level Python
  collections, in this case a dictionary with string keys and sets of integers
  as values, which conceal the underlying mapped classes.
- [proxied_association.py](https://docs.sqlalchemy.org/en/20/_modules/examples/association/proxied_association.html) - Same example as basic_association, adding in
  usage of [sqlalchemy.ext.associationproxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#module-sqlalchemy.ext.associationproxy) to make explicit references
  to `OrderItem` optional.

### Asyncio Integration

Examples illustrating the asyncio engine feature of SQLAlchemy.

Listing of files:

- [async_orm.py](https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/async_orm.html) - Illustrates use of the `sqlalchemy.ext.asyncio.AsyncSession` object
  for asynchronous ORM use.
- [async_orm_writeonly.py](https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/async_orm_writeonly.html) - Illustrates using **write only relationships** for simpler handling
  of ORM collections under asyncio.
- [basic.py](https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/basic.html) - Illustrates the asyncio engine / connection interface.
- [gather_orm_statements.py](https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/gather_orm_statements.html) - Illustrates how to run many statements concurrently using `asyncio.gather()`
  along many asyncio database connections, merging ORM results into a single
  `AsyncSession`.
- [greenlet_orm.py](https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/greenlet_orm.html) - Illustrates use of the sqlalchemy.ext.asyncio.AsyncSession object
  for asynchronous ORM use, including the optional run_sync() method.

### Directed Graphs

An example of persistence for a directed graph structure.   The
graph is stored as a collection of edges, each referencing both a
“lower” and an “upper” node in a table of nodes.  Basic persistence
and querying for lower- and upper- neighbors are illustrated:

```
n2 = Node(2)
n5 = Node(5)
n2.add_neighbor(n5)
print(n2.higher_neighbors())
```

Listing of files:

- [directed_graph.py](https://docs.sqlalchemy.org/en/20/_modules/examples/graphs/directed_graph.html)

### Dynamic Relations as Dictionaries

Illustrates how to place a dictionary-like facade on top of a
“dynamic” relation, so that dictionary operations (assuming simple
string keys) can operate upon a large collection without loading the
full collection at once.

Listing of files:

- [dynamic_dict.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dynamic_dict/dynamic_dict.html)

### Generic Associations

Illustrates various methods of associating multiple types of
parents with a particular child object.

The examples all use the declarative extension along with
declarative mixins.   Each one presents the identical use
case at the end - two classes, `Customer` and `Supplier`, both
subclassing the `HasAddresses` mixin, which ensures that the
parent class is provided with an `addresses` collection
which contains `Address` objects.

The [discriminator_on_association.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/discriminator_on_association.html) and [generic_fk.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/generic_fk.html) scripts
are modernized versions of recipes presented in the 2007 blog post
[Polymorphic Associations with SQLAlchemy](https://techspot.zzzeek.org/2007/05/29/polymorphic-associations-with-sqlalchemy/).

Listing of files:

- [discriminator_on_association.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/discriminator_on_association.html) - Illustrates a mixin which provides a generic association
  using a single target table and a single association table,
  referred to by all parent tables.  The association table
  contains a “discriminator” column which determines what type of
  parent object associates to each particular row in the association
  table.
- [generic_fk.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/generic_fk.html) - Illustrates a so-called “generic foreign key”, in a similar fashion
  to that of popular frameworks such as Django, ROR, etc.  This
  approach bypasses standard referential integrity
  practices, in that the “foreign key” column is not actually
  constrained to refer to any particular table; instead,
  in-application logic is used to determine which table is referenced.
- [table_per_association.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/table_per_association.html) - Illustrates a mixin which provides a generic association
  via a individually generated association tables for each parent class.
  The associated objects themselves are persisted in a single table
  shared among all parents.
- [table_per_related.py](https://docs.sqlalchemy.org/en/20/_modules/examples/generic_associations/table_per_related.html) - Illustrates a generic association which persists association
  objects within individual tables, each one generated to persist
  those objects on behalf of a particular parent class.

### Materialized Paths

Illustrates the “materialized paths” pattern for hierarchical data using the
SQLAlchemy ORM.

Listing of files:

- [materialized_paths.py](https://docs.sqlalchemy.org/en/20/_modules/examples/materialized_paths/materialized_paths.html) - Illustrates the “materialized paths” pattern.

### Nested Sets

Illustrates a rudimentary way to implement the “nested sets”
pattern for hierarchical data using the SQLAlchemy ORM.

Listing of files:

- [nested_sets.py](https://docs.sqlalchemy.org/en/20/_modules/examples/nested_sets/nested_sets.html) - Celko’s “Nested Sets” Tree Structure.

### Performance

A performance profiling suite for a variety of SQLAlchemy use cases.

Each suite focuses on a specific use case with a particular performance
profile and associated implications:

- bulk inserts
- individual inserts, with or without transactions
- fetching large numbers of rows
- running lots of short queries

All suites include a variety of use patterns illustrating both Core
and ORM use, and are generally sorted in order of performance from worst
to greatest, inversely based on amount of functionality provided by SQLAlchemy,
greatest to least (these two things generally correspond perfectly).

A command line tool is presented at the package level which allows
individual suites to be run:

```
$ python -m examples.performance --help
usage: python -m examples.performance [-h] [--test TEST] [--dburl DBURL]
                                      [--num NUM] [--profile] [--dump]
                                      [--echo]

                                      {bulk_inserts,large_resultsets,single_inserts}

positional arguments:
  {bulk_inserts,large_resultsets,single_inserts}
                        suite to run

optional arguments:
  -h, --help            show this help message and exit
  --test TEST           run specific test name
  --dburl DBURL         database URL, default sqlite:///profile.db
  --num NUM             Number of iterations/items/etc for tests;
                        default is module-specific
  --profile             run profiling and dump call counts
  --dump                dump full call profile (implies --profile)
  --echo                Echo SQL output
```

An example run looks like:

```
$ python -m examples.performance bulk_inserts
```

Or with options:

```
$ python -m examples.performance bulk_inserts \
    --dburl mysql+mysqldb://scott:tiger@localhost/test \
    --profile --num 1000
```

See also

[How can I profile a SQLAlchemy powered application?](https://docs.sqlalchemy.org/en/20/faq/performance.html#faq-how-to-profile)

#### File Listing

Listing of files:

- [__main__.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/__main__.html) - Allows the examples/performance package to be run as a script.
- [bulk_inserts.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/bulk_inserts.html) - This series of tests illustrates different ways to INSERT a large number
  of rows in bulk.
- [bulk_updates.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/bulk_updates.html) - This series of tests will illustrate different ways to UPDATE a large number
  of rows in bulk (under construction! there’s just one test at the moment)
- [large_resultsets.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/large_resultsets.html) - In this series of tests, we are looking at time to load a large number
  of very small and simple rows.
- [short_selects.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/short_selects.html) - This series of tests illustrates different ways to SELECT a single
  record by primary key
- [single_inserts.py](https://docs.sqlalchemy.org/en/20/_modules/examples/performance/single_inserts.html) - In this series of tests, we’re looking at a method that inserts a row
  within a distinct transaction, and afterwards returns to essentially a
  “closed” state.   This would be analogous to an API call that starts up
  a database connection, inserts the row, commits and closes.

#### Running all tests with time

This is the default form of run:

```
$ python -m examples.performance single_inserts
Tests to run: test_orm_commit, test_bulk_save,
              test_bulk_insert_dictionaries, test_core,
              test_core_query_caching, test_dbapi_raw_w_connect,
              test_dbapi_raw_w_pool

test_orm_commit : Individual INSERT/COMMIT pairs via the
    ORM (10000 iterations); total time 13.690218 sec
test_bulk_save : Individual INSERT/COMMIT pairs using
    the "bulk" API  (10000 iterations); total time 11.290371 sec
test_bulk_insert_dictionaries : Individual INSERT/COMMIT pairs using
    the "bulk" API with dictionaries (10000 iterations);
    total time 10.814626 sec
test_core : Individual INSERT/COMMIT pairs using Core.
    (10000 iterations); total time 9.665620 sec
test_core_query_caching : Individual INSERT/COMMIT pairs using Core
    with query caching (10000 iterations); total time 9.209010 sec
test_dbapi_raw_w_connect : Individual INSERT/COMMIT pairs w/ DBAPI +
    connection each time (10000 iterations); total time 9.551103 sec
test_dbapi_raw_w_pool : Individual INSERT/COMMIT pairs w/ DBAPI +
    connection pool (10000 iterations); total time 8.001813 sec
```

#### Dumping Profiles for Individual Tests

A Python profile output can be dumped for all tests, or more commonly
individual tests:

```
$ python -m examples.performance single_inserts --test test_core --num 1000 --dump
Tests to run: test_core
test_core : Individual INSERT/COMMIT pairs using Core. (1000 iterations); total fn calls 186109
         186109 function calls (186102 primitive calls) in 1.089 seconds

   Ordered by: internal time, call count

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1000    0.634    0.001    0.634    0.001 {method 'commit' of 'sqlite3.Connection' objects}
     1000    0.154    0.000    0.154    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
     1000    0.021    0.000    0.074    0.000 /Users/classic/dev/sqlalchemy/lib/sqlalchemy/sql/compiler.py:1950(_get_colparams)
     1000    0.015    0.000    0.034    0.000 /Users/classic/dev/sqlalchemy/lib/sqlalchemy/engine/default.py:503(_init_compiled)
        1    0.012    0.012    1.091    1.091 examples/performance/single_inserts.py:79(test_core)

    ...
```

#### Writing your Own Suites

The profiler suite system is extensible, and can be applied to your own set
of tests.  This is a valuable technique to use in deciding upon the proper
approach for some performance-critical set of routines.  For example,
if we wanted to profile the difference between several kinds of loading,
we can create a file `test_loads.py`, with the following content:

```
from examples.performance import Profiler
from sqlalchemy import Integer, Column, create_engine, ForeignKey
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
session = None

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    children = relationship("Child")

class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))

# Init with name of file, default number of items
Profiler.init("test_loads", 1000)

@Profiler.setup_once
def setup_once(dburl, echo, num):
    "setup once.  create an engine, insert fixture data"
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    sess = Session(engine)
    sess.add_all(
        [
            Parent(children=[Child() for j in range(100)])
            for i in range(num)
        ]
    )
    sess.commit()

@Profiler.setup
def setup(dburl, echo, num):
    "setup per test.  create a new Session."
    global session
    session = Session(engine)
    # pre-connect so this part isn't profiled (if we choose)
    session.connection()

@Profiler.profile
def test_lazyload(n):
    "load everything, no eager loading."

    for parent in session.query(Parent):
        parent.children

@Profiler.profile
def test_joinedload(n):
    "load everything, joined eager loading."

    for parent in session.query(Parent).options(joinedload("children")):
        parent.children

@Profiler.profile
def test_subqueryload(n):
    "load everything, subquery eager loading."

    for parent in session.query(Parent).options(subqueryload("children")):
        parent.children

if __name__ == "__main__":
    Profiler.main()
```

We can run our new script directly:

```
$ python test_loads.py  --dburl postgresql+psycopg2://scott:tiger@localhost/test
Running setup once...
Tests to run: test_lazyload, test_joinedload, test_subqueryload
test_lazyload : load everything, no eager loading. (1000 iterations); total time 11.971159 sec
test_joinedload : load everything, joined eager loading. (1000 iterations); total time 2.754592 sec
test_subqueryload : load everything, subquery eager loading. (1000 iterations); total time 2.977696 sec
```

### Space Invaders

A Space Invaders game using SQLite as the state machine.

Originally developed in 2012.  Adapted to work in Python 3.

Runs in a textual console using ASCII art.

 ![../_images/space_invaders.jpg](https://docs.sqlalchemy.org/en/20/_images/space_invaders.jpg)

To run:

```
$ python -m examples.space_invaders.space_invaders
```

While it runs, watch the SQL output in the log:

```
$ tail -f space_invaders.log
```

enjoy!

Listing of files:

- [space_invaders.py](https://docs.sqlalchemy.org/en/20/_modules/examples/space_invaders/space_invaders.html)

### Versioning Objects

#### Versioning with a History Table

Illustrates an extension which creates version tables for entities and stores
records for each change. The given extensions generate an anonymous “history”
class which represents historical versions of the target object.

Compare to the [Versioning using Temporal Rows](#examples-versioned-rows) examples which write updates
as new rows in the same table, without using a separate history table.

Usage is illustrated via a unit test module `test_versioning.py`, which is
run using SQLAlchemy’s internal pytest plugin:

```
$ pytest test/base/test_examples.py
```

A fragment of example usage, using declarative:

```
from history_meta import Versioned, versioned_session

class Base(DeclarativeBase):
    pass

class SomeClass(Versioned, Base):
    __tablename__ = "sometable"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __eq__(self, other):
        assert type(other) is SomeClass and other.id == self.id

Session = sessionmaker(bind=engine)
versioned_session(Session)

sess = Session()
sc = SomeClass(name="sc1")
sess.add(sc)
sess.commit()

sc.name = "sc1modified"
sess.commit()

assert sc.version == 2

SomeClassHistory = SomeClass.__history_mapper__.class_

assert sess.query(SomeClassHistory).filter(
    SomeClassHistory.version == 1
).all() == [SomeClassHistory(version=1, name="sc1")]
```

The `Versioned` mixin is designed to work with declarative.  To use
the extension with classical mappers, the `_history_mapper` function
can be applied:

```
from history_meta import _history_mapper

m = mapper(SomeClass, sometable)
_history_mapper(m)

SomeHistoryClass = SomeClass.__history_mapper__.class_
```

The versioning example also integrates with the ORM optimistic concurrency
feature documented at [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html#mapper-version-counter).   To enable this feature,
set the flag `Versioned.use_mapper_versioning` to True:

```
class SomeClass(Versioned, Base):
    __tablename__ = "sometable"

    use_mapper_versioning = True

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __eq__(self, other):
        assert type(other) is SomeClass and other.id == self.id
```

Above, if two instance of `SomeClass` with the same version identifier
are updated and sent to the database for UPDATE concurrently, if the database
isolation level allows the two UPDATE statements to proceed, one will fail
because it no longer is against the last known version identifier.

Listing of files:

- [history_meta.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_history/history_meta.html) - Versioned mixin class and other utilities.
- [test_versioning.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_history/test_versioning.html) - Unit tests illustrating usage of the `history_meta.py`
  module functions.

#### Versioning using Temporal Rows

Several examples that illustrate the technique of intercepting changes
that would be first interpreted as an UPDATE on a row, and instead turning
it into an INSERT of a new row, leaving the previous row intact as
a historical version.

Compare to the [Versioning with a History Table](#examples-versioned-history) example which writes a
history row to a separate history table.

Listing of files:

- [versioned_map.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_rows/versioned_map.html) - A variant of the versioned_rows example built around the
  concept of a “vertical table” structure, like those illustrated in
  [Vertical Attribute Mapping](#examples-vertical-tables) examples.
- [versioned_rows.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_rows/versioned_rows.html) - Illustrates a method to intercept changes on objects, turning
  an UPDATE statement on a single row into an INSERT statement, so that a new
  row is inserted with the new data, keeping the old row intact.
- [versioned_rows_w_versionid.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_rows/versioned_rows_w_versionid.html) - Illustrates a method to intercept changes on objects, turning
  an UPDATE statement on a single row into an INSERT statement, so that a new
  row is inserted with the new data, keeping the old row intact.
- [versioned_update_old_row.py](https://docs.sqlalchemy.org/en/20/_modules/examples/versioned_rows/versioned_update_old_row.html) - Illustrates the same UPDATE into INSERT technique of `versioned_rows.py`,
  but also emits an UPDATE on the **old** row to affect a change in timestamp.
  Also includes a [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) hook to limit queries
  to only the most recent version.

### Vertical Attribute Mapping

Illustrates “vertical table” mappings.

A “vertical table” refers to a technique where individual attributes
of an object are stored as distinct rows in a table. The “vertical
table” technique is used to persist objects which can have a varied
set of attributes, at the expense of simple query control and brevity.
It is commonly found in content/document management systems in order
to represent user-created structures flexibly.

Two variants on the approach are given.  In the second, each row
references a “datatype” which contains information about the type of
information stored in the attribute, such as integer, string, or date.

Example:

```
shrew = Animal("shrew")
shrew["cuteness"] = 5
shrew["weasel-like"] = False
shrew["poisonous"] = True

session.add(shrew)
session.flush()

q = session.query(Animal).filter(
    Animal.facts.any(
        and_(AnimalFact.key == "weasel-like", AnimalFact.value == True)
    )
)
print("weasel-like animals", q.all())
```

Listing of files:

- [dictlike-polymorphic.py](https://docs.sqlalchemy.org/en/20/_modules/examples/vertical/dictlike-polymorphic.html) - Mapping a polymorphic-valued vertical table as a dictionary.
- [dictlike.py](https://docs.sqlalchemy.org/en/20/_modules/examples/vertical/dictlike.html) - Mapping a vertical table as a dictionary.

## Inheritance Mapping Recipes

### Basic Inheritance Mappings

Working examples of single-table, joined-table, and concrete-table
inheritance as described in [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html).

Listing of files:

- [concrete.py](https://docs.sqlalchemy.org/en/20/_modules/examples/inheritance/concrete.html) - Concrete-table (table-per-class) inheritance example.
- [joined.py](https://docs.sqlalchemy.org/en/20/_modules/examples/inheritance/joined.html) - Joined-table (table-per-subclass) inheritance example.
- [single.py](https://docs.sqlalchemy.org/en/20/_modules/examples/inheritance/single.html) - Single-table (table-per-hierarchy) inheritance example.

## Special APIs

### Attribute Instrumentation

Examples illustrating modifications to SQLAlchemy’s attribute management
system.

Listing of files:

- [active_column_defaults.py](https://docs.sqlalchemy.org/en/20/_modules/examples/custom_attributes/active_column_defaults.html) - Illustrates use of the [AttributeEvents.init_scalar()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.init_scalar)
  event, in conjunction with Core column defaults to provide
  ORM objects that automatically produce the default value
  when an un-set attribute is accessed.
- [custom_management.py](https://docs.sqlalchemy.org/en/20/_modules/examples/custom_attributes/custom_management.html) - Illustrates customized class instrumentation, using
  the [sqlalchemy.ext.instrumentation](https://docs.sqlalchemy.org/en/20/orm/extensions/instrumentation.html#module-sqlalchemy.ext.instrumentation) extension package.
- [listen_for_events.py](https://docs.sqlalchemy.org/en/20/_modules/examples/custom_attributes/listen_for_events.html) - Illustrates how to attach events to all instrumented attributes
  and listen for change events.

### Horizontal Sharding

A basic example of using the SQLAlchemy Sharding API.
Sharding refers to horizontally scaling data across multiple
databases.

The basic components of a “sharded” mapping are:

- multiple [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) instances, each assigned a “shard id”.
  These [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) instances may refer to different databases,
  or different schemas / accounts within the same database, or they can
  even be differentiated only by options that will cause them to access
  different schemas or tables when used.
- a function which can return a single shard id, given an instance
  to be saved; this is called “shard_chooser”
- a function which can return a list of shard ids which apply to a particular
  instance identifier; this is called “id_chooser”.If it returns all shard ids,
  all shards will be searched.
- a function which can return a list of shard ids to try, given a particular
  Query (“query_chooser”).  If it returns all shard ids, all shards will be
  queried and the results joined together.

In these examples, different kinds of shards are used against the same basic
example which accommodates weather data on a per-continent basis. We provide
example shard_chooser, id_chooser and query_chooser functions. The
query_chooser illustrates inspection of the SQL expression element in order to
attempt to determine a single shard being requested.

The construction of generic sharding routines is an ambitious approach
to the issue of organizing instances among multiple databases.   For a
more plain-spoken alternative, the “distinct entity” approach
is a simple method of assigning objects to different tables (and potentially
database nodes) in an explicit way - described on the wiki at
[EntityName](https://www.sqlalchemy.org/trac/wiki/UsageRecipes/EntityName).

Listing of files:

- [asyncio.py](https://docs.sqlalchemy.org/en/20/_modules/examples/sharding/asyncio.html) - Illustrates sharding API used with asyncio.
- [separate_databases.py](https://docs.sqlalchemy.org/en/20/_modules/examples/sharding/separate_databases.html) - Illustrates sharding using distinct SQLite databases.
- [separate_schema_translates.py](https://docs.sqlalchemy.org/en/20/_modules/examples/sharding/separate_schema_translates.html) - Illustrates sharding using a single database with multiple schemas,
  where a different “schema_translates_map” can be used for each shard.
- [separate_tables.py](https://docs.sqlalchemy.org/en/20/_modules/examples/sharding/separate_tables.html) - Illustrates sharding using a single SQLite database, that will however
  have multiple tables using a naming convention.

## Extending the ORM

### ORM Query Events

Recipes which illustrate augmentation of ORM SELECT behavior as used by
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) with [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) use of
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), as well as the [1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object.

Examples include demonstrations of the [with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria)
option as well as the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) hook.

As of SQLAlchemy 1.4, the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) construct is unified
with the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct, so that these two objects
are mostly the same.

Listing of files:

- [filter_public.py](https://docs.sqlalchemy.org/en/20/_modules/examples/extending_query/filter_public.html) - Illustrates a global criteria applied to entities of a particular type.
- [temporal_range.py](https://docs.sqlalchemy.org/en/20/_modules/examples/extending_query/temporal_range.html) - Illustrates a custom per-query criteria that will be applied
  to selected entities.

### Dogpile Caching

Illustrates how to embed
[dogpile.cache](https://dogpilecache.sqlalchemy.org/)
functionality with ORM queries, allowing full cache control
as well as the ability to pull “lazy loaded” attributes from long term cache.

In this demo, the following techniques are illustrated:

- Using the [SessionEvents.do_orm_execute()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.do_orm_execute) event hook
- Basic technique of circumventing [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) to pull from a
  custom cache source instead of the database.
- Rudimental caching with dogpile.cache, using “regions” which allow
  global control over a fixed set of configurations.
- Using custom `UserDefinedOption` objects to configure options in
  a statement object.

See also

[Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing) - includes a general example of the
technique presented here.

E.g.:

```
# query for Person objects, specifying cache
stmt = select(Person).options(FromCache("default"))

# specify that each Person's "addresses" collection comes from
# cache too
stmt = stmt.options(RelationshipCache(Person.addresses, "default"))

# execute and results
result = session.execute(stmt)

print(result.scalars().all())
```

To run, both SQLAlchemy and dogpile.cache must be
installed or on the current PYTHONPATH. The demo will create a local
directory for datafiles, insert initial data, and run. Running the
demo a second time will utilize the cache files already present, and
exactly one SQL statement against two tables will be emitted - the
displayed result however will utilize dozens of lazyloads that all
pull from cache.

The demo scripts themselves, in order of complexity, are run as Python
modules so that relative imports work:

```
$ python -m examples.dogpile_caching.helloworld

$ python -m examples.dogpile_caching.relationship_caching

$ python -m examples.dogpile_caching.advanced

$ python -m examples.dogpile_caching.local_session_caching
```

Listing of files:

- [environment.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/environment.html) - Establish data / cache file paths, and configurations,
  bootstrap fixture data if necessary.
- [caching_query.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/caching_query.html) - Represent functions and classes
  which allow the usage of Dogpile caching with SQLAlchemy.
  Introduces a query option called FromCache.
- [model.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/model.html) - The datamodel, which represents Person that has multiple
  Address objects, each with PostalCode, City, Country.
- [fixture_data.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/fixture_data.html) - Installs some sample data.   Here we have a handful of postal codes for
  a few US/Canadian cities.   Then, 100 Person records are installed, each
  with a randomly selected postal code.
- [helloworld.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/helloworld.html) - Illustrate how to load some data, and cache the results.
- [relationship_caching.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/relationship_caching.html) - Illustrates how to add cache options on
  relationship endpoints, so that lazyloads load from cache.
- [advanced.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/advanced.html) - Illustrate usage of Query combined with the FromCache option,
  including front-end loading, cache invalidation and collection caching.
- [local_session_caching.py](https://docs.sqlalchemy.org/en/20/_modules/examples/dogpile_caching/local_session_caching.html) - This example creates a new dogpile.cache backend that will persist data in a
  dictionary which is local to the current session.   remove() the session and
  the cache is gone.

---

# SQLAlchemy 2.0 Documentation

# ORM Exceptions

SQLAlchemy ORM exceptions.

| Object Name | Description |
| --- | --- |
| ConcurrentModificationError | alias ofStaleDataError |
| NO_STATE | Exception types that may be raised by instrumentation implementations. |

   attribute [sqlalchemy.orm.exc..](#sqlalchemy.orm.exc.)sqlalchemy.orm.exc.ConcurrentModificationError

alias of [StaleDataError](#sqlalchemy.orm.exc.StaleDataError)

    exception sqlalchemy.orm.exc.DetachedInstanceError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError)

An attempt to access unloaded attributes on a
mapped instance that is detached.

    exception sqlalchemy.orm.exc.FlushError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError)

A invalid condition was detected during flush().

    exception sqlalchemy.orm.exc.LoaderStrategyException

*inherits from* [sqlalchemy.exc.InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)

A loader strategy for an attribute does not exist.

   method [sqlalchemy.orm.exc.LoaderStrategyException.](#sqlalchemy.orm.exc.LoaderStrategyException)__init__(*applied_to_property_type:Type[Any]*, *requesting_property:MapperProperty[Any]*, *applies_to:Type[MapperProperty[Any]]|None*, *actual_strategy_type:Type[LoaderStrategy]|None*, *strategy_key:Tuple[Any,...]*)     exception sqlalchemy.orm.exc.MappedAnnotationError

*inherits from* [sqlalchemy.exc.ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError)

Raised when ORM annotated declarative cannot interpret the
expression present inside of the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) construct.

Added in version 2.0.40.

     sqlalchemy.orm.exc.NO_STATE = (<class 'AttributeError'>, <class 'KeyError'>)

Exception types that may be raised by instrumentation implementations.

    exception sqlalchemy.orm.exc.ObjectDeletedError

*inherits from* [sqlalchemy.exc.InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)

A refresh operation failed to retrieve the database
row corresponding to an object’s known primary key identity.

A refresh operation proceeds when an expired attribute is
accessed on an object, or when [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get) is
used to retrieve an object which is, upon retrieval, detected
as expired.   A SELECT is emitted for the target row
based on primary key; if no row is returned, this
exception is raised.

The true meaning of this exception is simply that
no row exists for the primary key identifier associated
with a persistent object.   The row may have been
deleted, or in some cases the primary key updated
to a new value, outside of the ORM’s management of the target
object.

   method [sqlalchemy.orm.exc.ObjectDeletedError.](#sqlalchemy.orm.exc.ObjectDeletedError)__init__(*state:InstanceState[Any]*, *msg:str|None=None*)     exception sqlalchemy.orm.exc.ObjectDereferencedError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError)

An operation cannot complete due to an object being garbage
collected.

    exception sqlalchemy.orm.exc.StaleDataError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError)

An operation encountered database state that is unaccounted for.

Conditions which cause this to happen include:

- A flush may have attempted to update or delete rows
  and an unexpected number of rows were matched during
  the UPDATE or DELETE statement.   Note that when
  version_id_col is used, rows in UPDATE or DELETE statements
  are also matched against the current known version
  identifier.
- A mapped object with version_id_col was refreshed,
  and the version number coming back from the database does
  not match that of the object itself.
- A object is detached from its parent object, however
  the object was previously attached to a different parent
  identity which was garbage collected, and a decision
  cannot be made if the new parent was really the most
  recent “parent”.

    exception sqlalchemy.orm.exc.UnmappedClassError

*inherits from* [sqlalchemy.orm.exc.UnmappedError](#sqlalchemy.orm.exc.UnmappedError)

An mapping operation was requested for an unknown class.

   method [sqlalchemy.orm.exc.UnmappedClassError.](#sqlalchemy.orm.exc.UnmappedClassError)__init__(*cls:Type[_T]*, *msg:str|None=None*)     exception sqlalchemy.orm.exc.UnmappedColumnError

*inherits from* [sqlalchemy.exc.InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)

Mapping operation was requested on an unknown column.

    exception sqlalchemy.orm.exc.UnmappedError

*inherits from* [sqlalchemy.exc.InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)

Base for exceptions that involve expected mappings not present.

    exception sqlalchemy.orm.exc.UnmappedInstanceError

*inherits from* [sqlalchemy.orm.exc.UnmappedError](#sqlalchemy.orm.exc.UnmappedError)

An mapping operation was requested for an unknown instance.

   method [sqlalchemy.orm.exc.UnmappedInstanceError.](#sqlalchemy.orm.exc.UnmappedInstanceError)__init__(*obj:object*, *msg:str|None=None*)

---

# SQLAlchemy 2.0 Documentation

# Events and Internals

The SQLAlchemy ORM as well as Core are extended generally through the use
of event hooks.  Be sure to review the use of the event system in general
at [Events](https://docs.sqlalchemy.org/en/20/core/event.html).

- [ORM Events](https://docs.sqlalchemy.org/en/20/orm/events.html)
  - [Session Events](https://docs.sqlalchemy.org/en/20/orm/events.html#session-events)
  - [Mapper Events](https://docs.sqlalchemy.org/en/20/orm/events.html#mapper-events)
  - [Instance Events](https://docs.sqlalchemy.org/en/20/orm/events.html#instance-events)
  - [Attribute Events](https://docs.sqlalchemy.org/en/20/orm/events.html#attribute-events)
  - [Query Events](https://docs.sqlalchemy.org/en/20/orm/events.html#query-events)
  - [Instrumentation Events](https://docs.sqlalchemy.org/en/20/orm/events.html#module-sqlalchemy.orm.instrumentation)
- [ORM Internals](https://docs.sqlalchemy.org/en/20/orm/internals.html)
  - [AttributeState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeState)
  - [CascadeOptions](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.CascadeOptions)
  - [ClassManager](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ClassManager)
  - [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty)
  - [Composite](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Composite)
  - [CompositeProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.CompositeProperty)
  - [AttributeEventToken](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeEventToken)
  - [IdentityMap](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.IdentityMap)
  - [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)
  - [InspectionAttrInfo](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrInfo)
  - [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)
  - [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute)
  - [LoaderCallableStatus](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.LoaderCallableStatus)
  - [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
  - [MappedColumn](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MappedColumn)
  - [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty)
  - [MappedSQLExpression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MappedSQLExpression)
  - [InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType)
  - [NotExtension](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.NotExtension)
  - [merge_result()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.merge_result)
  - [merge_frozen_result()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.merge_frozen_result)
  - [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)
  - [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship)
  - [RelationshipDirection](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipDirection)
  - [RelationshipProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty)
  - [SQLORMExpression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.SQLORMExpression)
  - [Synonym](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Synonym)
  - [SynonymProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.SynonymProperty)
  - [QueryContext](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryContext)
  - [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute)
  - [UOWTransaction](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.UOWTransaction)
- [ORM Exceptions](https://docs.sqlalchemy.org/en/20/orm/exceptions.html)
  - [ConcurrentModificationError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.ConcurrentModificationError)
  - [DetachedInstanceError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.DetachedInstanceError)
  - [FlushError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.FlushError)
  - [LoaderStrategyException](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.LoaderStrategyException)
  - [MappedAnnotationError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.MappedAnnotationError)
  - [NO_STATE](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.NO_STATE)
  - [ObjectDeletedError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.ObjectDeletedError)
  - [ObjectDereferencedError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.ObjectDereferencedError)
  - [StaleDataError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.StaleDataError)
  - [UnmappedClassError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.UnmappedClassError)
  - [UnmappedColumnError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.UnmappedColumnError)
  - [UnmappedError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.UnmappedError)
  - [UnmappedInstanceError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.UnmappedInstanceError)
