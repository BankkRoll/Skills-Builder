# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Customizing DDL

In the preceding sections we’ve discussed a variety of schema constructs
including [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint),
[CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint), and
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence). Throughout, we’ve relied upon the
`create()` and [create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) methods of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) in
order to issue data definition language (DDL) for all constructs. When issued,
a pre-determined order of operations is invoked, and DDL to create each table
is created unconditionally including all constraints and other objects
associated with it. For more complex scenarios where database-specific DDL is
required, SQLAlchemy offers two techniques which can be used to add any DDL
based on any condition, either accompanying the standard generation of tables
or by itself.

## Custom DDL

Custom DDL phrases are most easily achieved using the
[DDL](#sqlalchemy.schema.DDL) construct. This construct works like all the
other DDL elements except it accepts a string which is the text to be emitted:

```
event.listen(
    metadata,
    "after_create",
    DDL(
        "ALTER TABLE users ADD CONSTRAINT "
        "cst_user_name_length "
        " CHECK (length(user_name) >= 8)"
    ),
)
```

A more comprehensive method of creating libraries of DDL constructs is to use
custom compilation - see [Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html) for
details.

## Controlling DDL Sequences

The [DDL](#sqlalchemy.schema.DDL) construct introduced previously also has the
ability to be invoked conditionally based on inspection of the
database.  This feature is available using the [ExecutableDDLElement.execute_if()](#sqlalchemy.schema.ExecutableDDLElement.execute_if)
method.  For example, if we wanted to create a trigger but only on
the PostgreSQL backend, we could invoke this as:

```
mytable = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", String(50)),
)

func = DDL(
    "CREATE FUNCTION my_func() "
    "RETURNS TRIGGER AS $$ "
    "BEGIN "
    "NEW.data := 'ins'; "
    "RETURN NEW; "
    "END; $$ LANGUAGE PLPGSQL"
)

trigger = DDL(
    "CREATE TRIGGER dt_ins BEFORE INSERT ON mytable "
    "FOR EACH ROW EXECUTE PROCEDURE my_func();"
)

event.listen(mytable, "after_create", func.execute_if(dialect="postgresql"))

event.listen(mytable, "after_create", trigger.execute_if(dialect="postgresql"))
```

The [ExecutableDDLElement.execute_if.dialect](#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.dialect) keyword also accepts a tuple
of string dialect names:

```
event.listen(
    mytable, "after_create", trigger.execute_if(dialect=("postgresql", "mysql"))
)
event.listen(
    mytable, "before_drop", trigger.execute_if(dialect=("postgresql", "mysql"))
)
```

The [ExecutableDDLElement.execute_if()](#sqlalchemy.schema.ExecutableDDLElement.execute_if) method can also work against a callable
function that will receive the database connection in use.  In the
example below, we use this to conditionally create a CHECK constraint,
first looking within the PostgreSQL catalogs to see if it exists:

```
def should_create(ddl, target, connection, **kw):
    row = connection.execute(
        "select conname from pg_constraint where conname='%s'" % ddl.element.name
    ).scalar()
    return not bool(row)

def should_drop(ddl, target, connection, **kw):
    return not should_create(ddl, target, connection, **kw)

event.listen(
    users,
    "after_create",
    DDL(
        "ALTER TABLE users ADD CONSTRAINT "
        "cst_user_name_length CHECK (length(user_name) >= 8)"
    ).execute_if(callable_=should_create),
)
event.listen(
    users,
    "before_drop",
    DDL("ALTER TABLE users DROP CONSTRAINT cst_user_name_length").execute_if(
        callable_=should_drop
    ),
)

users.create(engine)
CREATE TABLE users (
    user_id SERIAL NOT NULL,
    user_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (user_id)
)

SELECT conname FROM pg_constraint WHERE conname='cst_user_name_length'
ALTER TABLE users ADD CONSTRAINT cst_user_name_length  CHECK (length(user_name) >= 8)
users.drop(engine)
SELECT conname FROM pg_constraint WHERE conname='cst_user_name_length'
ALTER TABLE users DROP CONSTRAINT cst_user_name_length
DROP TABLE users
```

## Using the built-in DDLElement Classes

The `sqlalchemy.schema` package contains SQL expression constructs that
provide DDL expressions, all of which extend from the common base
[ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement). For example, to produce a `CREATE TABLE` statement,
one can use the [CreateTable](#sqlalchemy.schema.CreateTable) construct:

```
from sqlalchemy.schema import CreateTable

with engine.connect() as conn:
    conn.execute(CreateTable(mytable))
CREATE TABLE mytable (
    col1 INTEGER,
    col2 INTEGER,
    col3 INTEGER,
    col4 INTEGER,
    col5 INTEGER,
    col6 INTEGER
)
```

Above, the [CreateTable](#sqlalchemy.schema.CreateTable) construct works like any
other expression construct (such as `select()`, `table.insert()`, etc.).
All of SQLAlchemy’s DDL oriented constructs are subclasses of
the [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) base class; this is the base of all the
objects corresponding to CREATE and DROP as well as ALTER,
not only in SQLAlchemy but in Alembic Migrations as well.
A full reference of available constructs is in [DDL Expression Constructs API](#schema-api-ddl).

User-defined DDL constructs may also be created as subclasses of
[ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) itself.   The documentation in
[Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html) has several examples of this.

## Controlling DDL Generation of Constraints and Indexes

Added in version 2.0.

While the previously mentioned [ExecutableDDLElement.execute_if()](#sqlalchemy.schema.ExecutableDDLElement.execute_if) method is
useful for custom [DDL](#sqlalchemy.schema.DDL) classes which need to invoke conditionally,
there is also a common need for elements that are typically related to a
particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), namely constraints and indexes, to also be
subject to “conditional” rules, such as an index that includes features
that are specific to a particular backend such as PostgreSQL or SQL Server.
For this use case, the [Constraint.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint.ddl_if) and [Index.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.ddl_if)
methods may be used against constructs such as [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint),
[UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) and [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), accepting the same
arguments as the [ExecutableDDLElement.execute_if()](#sqlalchemy.schema.ExecutableDDLElement.execute_if) method in order to control
whether or not their DDL will be emitted in terms of their parent
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.  These methods may be used inline when
creating the definition for a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
(or similarly, when using the `__table_args__` collection in an ORM
declarative mapping), such as:

```
from sqlalchemy import CheckConstraint, Index
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer, String

meta = MetaData()

my_table = Table(
    "my_table",
    meta,
    Column("id", Integer, primary_key=True),
    Column("num", Integer),
    Column("data", String),
    Index("my_pg_index", "data").ddl_if(dialect="postgresql"),
    CheckConstraint("num > 5").ddl_if(dialect="postgresql"),
)
```

In the above example, the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct refers to both an
[Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) and a [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint) construct, both which
indicate `.ddl_if(dialect="postgresql")`, which indicates that these
elements will be included in the CREATE TABLE sequence only against the
PostgreSQL dialect.  If we run `meta.create_all()` against the SQLite
dialect, for example, neither construct will be included:

```
>>> from sqlalchemy import create_engine
>>> sqlite_engine = create_engine("sqlite+pysqlite://", echo=True)
>>> meta.create_all(sqlite_engine)
BEGIN (implicit)
PRAGMA main.table_info("my_table")
[raw sql] ()
PRAGMA temp.table_info("my_table")
[raw sql] ()

CREATE TABLE my_table (
    id INTEGER NOT NULL,
    num INTEGER,
    data VARCHAR,
    PRIMARY KEY (id)
)
```

However, if we run the same commands against a PostgreSQL database, we will
see inline DDL for the CHECK constraint as well as a separate CREATE
statement emitted for the index:

```
>>> from sqlalchemy import create_engine
>>> postgresql_engine = create_engine(
...     "postgresql+psycopg2://scott:tiger@localhost/test", echo=True
... )
>>> meta.create_all(postgresql_engine)
BEGIN (implicit)
select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
[generated in 0.00009s] {'name': 'my_table'}

CREATE TABLE my_table (
    id SERIAL NOT NULL,
    num INTEGER,
    data VARCHAR,
    PRIMARY KEY (id),
    CHECK (num > 5)
)
[no key 0.00007s] {}
CREATE INDEX my_pg_index ON my_table (data)
[no key 0.00013s] {}
COMMIT
```

The [Constraint.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint.ddl_if) and [Index.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.ddl_if) methods create
an event hook that may be consulted not just at DDL execution time, as is the
behavior with [ExecutableDDLElement.execute_if()](#sqlalchemy.schema.ExecutableDDLElement.execute_if), but also within the SQL compilation
phase of the [CreateTable](#sqlalchemy.schema.CreateTable) object, which is responsible for rendering
the `CHECK (num > 5)` DDL inline within the CREATE TABLE statement.
As such, the event hook that is received by the `ddl_if.callable_()`
parameter has a richer argument set present, including that there is
a `dialect` keyword argument passed, as well as an instance of [DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler)
via the `compiler` keyword argument for the “inline rendering” portion of the
sequence.  The `bind` argument is **not** present when the event is triggered
within the [DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler) sequence, so a modern event hook that wishes
to inspect the database versioning information would best use the given
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) object, such as to test PostgreSQL versioning:

```
def only_pg_14(ddl_element, target, bind, dialect, **kw):
    return dialect.name == "postgresql" and dialect.server_version_info >= (14,)

my_table = Table(
    "my_table",
    meta,
    Column("id", Integer, primary_key=True),
    Column("num", Integer),
    Column("data", String),
    Index("my_pg_index", "data").ddl_if(callable_=only_pg_14),
)
```

See also

[Constraint.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint.ddl_if)

[Index.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.ddl_if)

## DDL Expression Constructs API

| Object Name | Description |
| --- | --- |
| _CreateDropBase | Base class for DDL constructs that represent CREATE and DROP or
equivalents. |
| AddConstraint | Represent an ALTER TABLE ADD CONSTRAINT statement. |
| BaseDDLElement | The root of DDL constructs, including those that are sub-elements
within the “create table” and other processes. |
| CreateColumn | Represent aColumnas rendered in a CREATE TABLE statement,
via theCreateTableconstruct. |
| CreateIndex | Represent a CREATE INDEX statement. |
| CreateSchema | Represent a CREATE SCHEMA statement. |
| CreateSequence | Represent a CREATE SEQUENCE statement. |
| CreateTable | Represent a CREATE TABLE statement. |
| DDL | A literal DDL statement. |
| DropConstraint | Represent an ALTER TABLE DROP CONSTRAINT statement. |
| DropIndex | Represent a DROP INDEX statement. |
| DropSchema | Represent a DROP SCHEMA statement. |
| DropSequence | Represent a DROP SEQUENCE statement. |
| DropTable | Represent a DROP TABLE statement. |
| ExecutableDDLElement | Base class for standalone executable DDL expression constructs. |
| sort_tables(tables[, skip_fn, extra_dependencies]) | Sort a collection ofTableobjects based on
dependency. |
| sort_tables_and_constraints(tables[, filter_fn, extra_dependencies, _warn_for_cycles]) | Sort a collection ofTable/ForeignKeyConstraintobjects. |

   function sqlalchemy.schema.sort_tables(*tables:Iterable[TableClause]*, *skip_fn:Callable[[ForeignKeyConstraint],bool]|None=None*, *extra_dependencies:typing_Sequence[Tuple[TableClause,TableClause]]|None=None*) → List[[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)]

Sort a collection of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects based on
dependency.

This is a dependency-ordered sort which will emit [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects such that they will follow their dependent [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects.
Tables are dependent on another based on the presence of
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects as well as explicit dependencies
added by [Table.add_is_dependent_on()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.add_is_dependent_on).

Warning

The [sort_tables()](#sqlalchemy.schema.sort_tables) function cannot by itself
accommodate automatic resolution of dependency cycles between
tables, which are usually caused by mutually dependent foreign key
constraints. When these cycles are detected, the foreign keys
of these tables are omitted from consideration in the sort.
A warning is emitted when this condition occurs, which will be an
exception raise in a future release.   Tables which are not part
of the cycle will still be returned in dependency order.

To resolve these cycles, the
[ForeignKeyConstraint.use_alter](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) parameter may be
applied to those constraints which create a cycle.  Alternatively,
the [sort_tables_and_constraints()](#sqlalchemy.schema.sort_tables_and_constraints) function will
automatically return foreign key constraints in a separate
collection when cycles are detected so that they may be applied
to a schema separately.

Changed in version 1.3.17: - a warning is emitted when
[sort_tables()](#sqlalchemy.schema.sort_tables) cannot perform a proper sort due to
cyclical dependencies.  This will be an exception in a future
release.  Additionally, the sort will continue to return
other tables not involved in the cycle in dependency order
which was not the case previously.

    Parameters:

- **tables** – a sequence of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.
- **skip_fn** – optional callable which will be passed a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object; if it returns True, this
  constraint will not be considered as a dependency.  Note this is
  **different** from the same parameter in
  [sort_tables_and_constraints()](#sqlalchemy.schema.sort_tables_and_constraints), which is
  instead passed the owning [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object.
- **extra_dependencies** – a sequence of 2-tuples of tables which will
  also be considered as dependent on each other.

See also

[sort_tables_and_constraints()](#sqlalchemy.schema.sort_tables_and_constraints)

[MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables) - uses this function to sort

     function sqlalchemy.schema.sort_tables_and_constraints(*tables*, *filter_fn=None*, *extra_dependencies=None*, *_warn_for_cycles=False*)

Sort a collection of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)  /
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects.

This is a dependency-ordered sort which will emit tuples of
`(Table, [ForeignKeyConstraint, ...])` such that each
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) follows its dependent [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects.
Remaining [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects that are separate due to
dependency rules not satisfied by the sort are emitted afterwards
as `(None, [ForeignKeyConstraint ...])`.

Tables are dependent on another based on the presence of
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects, explicit dependencies
added by [Table.add_is_dependent_on()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.add_is_dependent_on),
as well as dependencies
stated here using the [sort_tables_and_constraints.skip_fn](#sqlalchemy.schema.sort_tables_and_constraints.params.skip_fn)
and/or [sort_tables_and_constraints.extra_dependencies](#sqlalchemy.schema.sort_tables_and_constraints.params.extra_dependencies)
parameters.

  Parameters:

- **tables** – a sequence of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.
- **filter_fn** – optional callable which will be passed a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object,
  and returns a value based on
  whether this constraint should definitely be included or excluded as
  an inline constraint, or neither.   If it returns False, the constraint
  will definitely be included as a dependency that cannot be subject
  to ALTER; if True, it will **only** be included as an ALTER result at
  the end.   Returning None means the constraint is included in the
  table-based result unless it is detected as part of a dependency cycle.
- **extra_dependencies** – a sequence of 2-tuples of tables which will
  also be considered as dependent on each other.

See also

[sort_tables()](#sqlalchemy.schema.sort_tables)

     class sqlalchemy.schema.BaseDDLElement

*inherits from* [sqlalchemy.sql.expression.ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

The root of DDL constructs, including those that are sub-elements
within the “create table” and other processes.

Added in version 2.0.

     class sqlalchemy.schema.ExecutableDDLElement

*inherits from* `sqlalchemy.sql.roles.DDLRole`, [sqlalchemy.sql.expression.Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable), [sqlalchemy.schema.BaseDDLElement](#sqlalchemy.schema.BaseDDLElement)

Base class for standalone executable DDL expression constructs.

This class is the base for the general purpose [DDL](#sqlalchemy.schema.DDL) class,
as well as the various create/drop clause constructs such as
[CreateTable](#sqlalchemy.schema.CreateTable), [DropTable](#sqlalchemy.schema.DropTable), [AddConstraint](#sqlalchemy.schema.AddConstraint),
etc.

Changed in version 2.0: [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) is renamed from
`DDLElement`, which still exists for backwards compatibility.

[ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) integrates closely with SQLAlchemy events,
introduced in [Events](https://docs.sqlalchemy.org/en/20/core/event.html).  An instance of one is
itself an event receiving callable:

```
event.listen(
    users,
    "after_create",
    AddConstraint(constraint).execute_if(dialect="postgresql"),
)
```

See also

[DDL](#sqlalchemy.schema.DDL)

[DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents)

[Events](https://docs.sqlalchemy.org/en/20/core/event.html)

[Controlling DDL Sequences](#schema-ddl-sequences)

| Member Name | Description |
| --- | --- |
| __call__() | Execute the DDL as a ddl_listener. |
| against() | Return a copy of thisExecutableDDLElementwhich
will include the given target. |
| execute_if() | Return a callable that will execute thisExecutableDDLElementconditionally within an event
handler. |

   method [sqlalchemy.schema.ExecutableDDLElement.](#sqlalchemy.schema.ExecutableDDLElement)__call__(*target*, *bind*, ***kw*)

Execute the DDL as a ddl_listener.

    method [sqlalchemy.schema.ExecutableDDLElement.](#sqlalchemy.schema.ExecutableDDLElement)against(*target:SchemaItem*) → Self

Return a copy of this [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) which
will include the given target.

This essentially applies the given item to the `.target` attribute of
the returned [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) object. This target
is then usable by event handlers and compilation routines in order to
provide services such as tokenization of a DDL string in terms of a
particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

When a [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) object is established as
an event handler for the [DDLEvents.before_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_create) or
[DDLEvents.after_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_create) events, and the event then
occurs for a given target such as a [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) or
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), that target is established with a copy of the
[ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) object using this method, which
then proceeds to the `ExecutableDDLElement.execute()`
method in order to invoke the actual DDL instruction.

  Parameters:

**target** – a [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) that will be the subject
of a DDL operation.

  Returns:

a copy of this [ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) with the
`.target` attribute assigned to the given
[SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

See also

[DDL](#sqlalchemy.schema.DDL) - uses tokenization against the “target” when
processing the DDL string.

     method [sqlalchemy.schema.ExecutableDDLElement.](#sqlalchemy.schema.ExecutableDDLElement)execute_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

Return a callable that will execute this
[ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement) conditionally within an event
handler.

Used to provide a wrapper for event listening:

```
event.listen(
    metadata,
    "before_create",
    DDL("my_ddl").execute_if(dialect="postgresql"),
)
```

   Parameters:

- **dialect** –
  May be a string or tuple of strings.
  If a string, it will be compared to the name of the
  executing database dialect:
  ```
  DDL("something").execute_if(dialect="postgresql")
  ```
  If a tuple, specifies multiple dialect names:
  ```
  DDL("something").execute_if(dialect=("postgresql", "mysql"))
  ```
- **callable_** –
  A callable, which will be invoked with
  three positional arguments as well as optional keyword
  arguments:
  > ddl:
  >
  > This DDL element.
  >
  >   target:
  >
  > The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  > object which is the
  > target of this event. May be None if the DDL is executed
  > explicitly.
  >
  >   bind:
  >
  > The [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) being used for DDL execution.
  > May be None if this construct is being created inline within
  > a table, in which case `compiler` will be present.
  >
  >   tables:
  >
  > Optional keyword argument - a list of Table objects which are to
  > be created/ dropped within a MetaData.create_all() or drop_all()
  > method call.
  >
  >   dialect:
  >
  > keyword argument, but always present - the
  > [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) involved in the operation.
  >
  >   compiler:
  >
  > keyword argument.  Will be `None` for an engine
  > level DDL invocation, but will refer to a [DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler)
  > if this DDL element is being created inline within a table.
  >
  >   state:
  >
  > Optional keyword argument - will be the `state` argument
  > passed to this function.
  >
  >   checkfirst:
  >
  > Keyword argument, will be True if the ‘checkfirst’ flag was
  > set during the call to `create()`, `create_all()`,
  > `drop()`, `drop_all()`.
  If the callable returns a True value, the DDL statement will be
  executed.
- **state** – any value which will be passed to the callable_
  as the `state` keyword argument.

See also

`SchemaItem.ddl_if()`

[DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents)

[Events](https://docs.sqlalchemy.org/en/20/core/event.html)

      class sqlalchemy.schema.DDL

*inherits from* [sqlalchemy.schema.ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement)

A literal DDL statement.

Specifies literal SQL DDL to be executed by the database.  DDL objects
function as DDL event listeners, and can be subscribed to those events
listed in [DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents), using either [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) objects as targets.
Basic templating support allows
a single DDL instance to handle repetitive tasks for multiple tables.

Examples:

```
from sqlalchemy import event, DDL

tbl = Table("users", metadata, Column("uid", Integer))
event.listen(tbl, "before_create", DDL("DROP TRIGGER users_trigger"))

spow = DDL("ALTER TABLE %(table)s SET secretpowers TRUE")
event.listen(tbl, "after_create", spow.execute_if(dialect="somedb"))

drop_spow = DDL("ALTER TABLE users SET secretpowers FALSE")
connection.execute(drop_spow)
```

When operating on Table events, the following `statement`
string substitutions are available:

```
%(table)s  - the Table name, with any required quoting applied
%(schema)s - the schema name, with any required quoting applied
%(fullname)s - the Table name including schema, quoted if needed
```

The DDL’s “context”, if any, will be combined with the standard
substitutions noted above.  Keys present in the context will override
the standard substitutions.

| Member Name | Description |
| --- | --- |
| __init__() | Create a DDL statement. |

   method [sqlalchemy.schema.DDL.](#sqlalchemy.schema.DDL)__init__(*statement*, *context=None*)

Create a DDL statement.

  Parameters:

- **statement** –
  A string or unicode string to be executed.  Statements will be
  processed with Python’s string formatting operator using
  a fixed set of string substitutions, as well as additional
  substitutions provided by the optional [DDL.context](#sqlalchemy.schema.DDL.params.context)
  parameter.
  A literal ‘%’ in a statement must be escaped as ‘%%’.
  SQL bind parameters are not available in DDL statements.
- **context** – Optional dictionary, defaults to None.  These values will be
  available for use in string substitutions on the DDL statement.

See also

[DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents)

[Events](https://docs.sqlalchemy.org/en/20/core/event.html)

      class sqlalchemy.schema._CreateDropBase

*inherits from* [sqlalchemy.schema.ExecutableDDLElement](#sqlalchemy.schema.ExecutableDDLElement), `typing.Generic`

Base class for DDL constructs that represent CREATE and DROP or
equivalents.

The common theme of _CreateDropBase is a single
`element` attribute which refers to the element
to be created or dropped.

    class sqlalchemy.schema.CreateTable

*inherits from* `sqlalchemy.schema._CreateBase`

Represent a CREATE TABLE statement.

| Member Name | Description |
| --- | --- |
| __init__() | Create aCreateTableconstruct. |

   method [sqlalchemy.schema.CreateTable.](#sqlalchemy.schema.CreateTable)__init__(*element:Table*, *include_foreign_key_constraints:typing_Sequence[ForeignKeyConstraint]|None=None*, *if_not_exists:bool=False*) → None

Create a [CreateTable](#sqlalchemy.schema.CreateTable) construct.

  Parameters:

- **element** – a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that’s the subject
  of the CREATE
- **on** – See the description for ‘on’ in [DDL](#sqlalchemy.schema.DDL).
- **include_foreign_key_constraints** – optional sequence of
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects that will be included
  inline within the CREATE construct; if omitted, all foreign key
  constraints that do not specify use_alter=True are included.
- **if_not_exists** –
  if True, an IF NOT EXISTS operator will be
  applied to the construct.
  Added in version 1.4.0b2.

       class sqlalchemy.schema.DropTable

*inherits from* `sqlalchemy.schema._DropBase`

Represent a DROP TABLE statement.

| Member Name | Description |
| --- | --- |
| __init__() | Create aDropTableconstruct. |

   method [sqlalchemy.schema.DropTable.](#sqlalchemy.schema.DropTable)__init__(*element:Table*, *if_exists:bool=False*) → None

Create a [DropTable](#sqlalchemy.schema.DropTable) construct.

  Parameters:

- **element** – a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that’s the subject
  of the DROP.
- **on** – See the description for ‘on’ in [DDL](#sqlalchemy.schema.DDL).
- **if_exists** –
  if True, an IF EXISTS operator will be applied to the
  construct.
  Added in version 1.4.0b2.

       class sqlalchemy.schema.CreateColumn

*inherits from* [sqlalchemy.schema.BaseDDLElement](#sqlalchemy.schema.BaseDDLElement)

Represent a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
as rendered in a CREATE TABLE statement,
via the [CreateTable](#sqlalchemy.schema.CreateTable) construct.

This is provided to support custom column DDL within the generation
of CREATE TABLE statements, by using the
compiler extension documented in [Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html)
to extend [CreateColumn](#sqlalchemy.schema.CreateColumn).

Typical integration is to examine the incoming [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object, and to redirect compilation if a particular flag or condition
is found:

```
from sqlalchemy import schema
from sqlalchemy.ext.compiler import compiles

@compiles(schema.CreateColumn)
def compile(element, compiler, **kw):
    column = element.element

    if "special" not in column.info:
        return compiler.visit_create_column(element, **kw)

    text = "%s SPECIAL DIRECTIVE %s" % (
        column.name,
        compiler.type_compiler.process(column.type),
    )
    default = compiler.get_column_default_string(column)
    if default is not None:
        text += " DEFAULT " + default

    if not column.nullable:
        text += " NOT NULL"

    if column.constraints:
        text += " ".join(
            compiler.process(const) for const in column.constraints
        )
    return text
```

The above construct can be applied to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
as follows:

```
from sqlalchemy import Table, Metadata, Column, Integer, String
from sqlalchemy import schema

metadata = MetaData()

table = Table(
    "mytable",
    MetaData(),
    Column("x", Integer, info={"special": True}, primary_key=True),
    Column("y", String(50)),
    Column("z", String(20), info={"special": True}),
)

metadata.create_all(conn)
```

Above, the directives we’ve added to the [Column.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.info)
collection
will be detected by our custom compilation scheme:

```
CREATE TABLE mytable (
        x SPECIAL DIRECTIVE INTEGER NOT NULL,
        y VARCHAR(50),
        z SPECIAL DIRECTIVE VARCHAR(20),
    PRIMARY KEY (x)
)
```

The [CreateColumn](#sqlalchemy.schema.CreateColumn) construct can also be used to skip certain
columns when producing a `CREATE TABLE`.  This is accomplished by
creating a compilation rule that conditionally returns `None`.
This is essentially how to produce the same effect as using the
`system=True` argument on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), which marks a column
as an implicitly-present “system” column.

For example, suppose we wish to produce a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
which skips
rendering of the PostgreSQL `xmin` column against the PostgreSQL
backend, but on other backends does render it, in anticipation of a
triggered rule.  A conditional compilation rule could skip this name only
on PostgreSQL:

```
from sqlalchemy.schema import CreateColumn

@compiles(CreateColumn, "postgresql")
def skip_xmin(element, compiler, **kw):
    if element.element.name == "xmin":
        return None
    else:
        return compiler.visit_create_column(element, **kw)

my_table = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("xmin", Integer),
)
```

Above, a [CreateTable](#sqlalchemy.schema.CreateTable) construct will generate a `CREATE TABLE`
which only includes the `id` column in the string; the `xmin` column
will be omitted, but only against the PostgreSQL backend.

    class sqlalchemy.schema.CreateSequence

*inherits from* `sqlalchemy.schema._CreateBase`

Represent a CREATE SEQUENCE statement.

    class sqlalchemy.schema.DropSequence

*inherits from* `sqlalchemy.schema._DropBase`

Represent a DROP SEQUENCE statement.

    class sqlalchemy.schema.CreateIndex

*inherits from* `sqlalchemy.schema._CreateBase`

Represent a CREATE INDEX statement.

| Member Name | Description |
| --- | --- |
| __init__() | Create aCreateindexconstruct. |

   method [sqlalchemy.schema.CreateIndex.](#sqlalchemy.schema.CreateIndex)__init__(*element:Index*, *if_not_exists:bool=False*) → None

Create a `Createindex` construct.

  Parameters:

- **element** – a [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) that’s the subject
  of the CREATE.
- **if_not_exists** –
  if True, an IF NOT EXISTS operator will be
  applied to the construct.
  Added in version 1.4.0b2.

       class sqlalchemy.schema.DropIndex

*inherits from* `sqlalchemy.schema._DropBase`

Represent a DROP INDEX statement.

| Member Name | Description |
| --- | --- |
| __init__() | Create aDropIndexconstruct. |

   method [sqlalchemy.schema.DropIndex.](#sqlalchemy.schema.DropIndex)__init__(*element:Index*, *if_exists:bool=False*) → None

Create a [DropIndex](#sqlalchemy.schema.DropIndex) construct.

  Parameters:

- **element** – a [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) that’s the subject
  of the DROP.
- **if_exists** –
  if True, an IF EXISTS operator will be applied to the
  construct.
  Added in version 1.4.0b2.

       class sqlalchemy.schema.AddConstraint

*inherits from* `sqlalchemy.schema._CreateBase`

Represent an ALTER TABLE ADD CONSTRAINT statement.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newAddConstraintconstruct. |

   method [sqlalchemy.schema.AddConstraint.](#sqlalchemy.schema.AddConstraint)__init__(*element:Constraint*, ***, *isolate_from_table:bool=True*) → None

Construct a new [AddConstraint](#sqlalchemy.schema.AddConstraint) construct.

  Parameters:

- **element** – a [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) object
- **isolate_from_table** –
  optional boolean, defaults to True.  Has
  the effect of the incoming constraint being isolated from being
  included in a CREATE TABLE sequence when associated with a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  Added in version 2.0.39: - added
  [AddConstraint.isolate_from_table](#sqlalchemy.schema.AddConstraint.params.isolate_from_table), defaulting
  to True.  Previously, the behavior of this parameter was implicitly
  turned on in all cases.

       class sqlalchemy.schema.DropConstraint

*inherits from* `sqlalchemy.schema._DropBase`

Represent an ALTER TABLE DROP CONSTRAINT statement.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newDropConstraintconstruct. |

   method [sqlalchemy.schema.DropConstraint.](#sqlalchemy.schema.DropConstraint)__init__(*element:Constraint*, ***, *cascade:bool=False*, *if_exists:bool=False*, *isolate_from_table:bool=True*, ***kw:Any*) → None

Construct a new [DropConstraint](#sqlalchemy.schema.DropConstraint) construct.

  Parameters:

- **element** – a [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) object
- **cascade** – optional boolean, indicates backend-specific
  “CASCADE CONSTRAINT” directive should be rendered if available
- **if_exists** – optional boolean, indicates backend-specific
  “IF EXISTS” directive should be rendered if available
- **isolate_from_table** –
  optional boolean, defaults to True.  Has
  the effect of the incoming constraint being isolated from being
  included in a CREATE TABLE sequence when associated with a
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  Added in version 2.0.39: - added
  [DropConstraint.isolate_from_table](#sqlalchemy.schema.DropConstraint.params.isolate_from_table), defaulting
  to True.  Previously, the behavior of this parameter was implicitly
  turned on in all cases.

       class sqlalchemy.schema.CreateSchema

*inherits from* `sqlalchemy.schema._CreateBase`

Represent a CREATE SCHEMA statement.

The argument here is the string name of the schema.

| Member Name | Description |
| --- | --- |
| __init__() | Create a newCreateSchemaconstruct. |

   method [sqlalchemy.schema.CreateSchema.](#sqlalchemy.schema.CreateSchema)__init__(*name:str*, *if_not_exists:bool=False*) → None

Create a new [CreateSchema](#sqlalchemy.schema.CreateSchema) construct.

     class sqlalchemy.schema.DropSchema

*inherits from* `sqlalchemy.schema._DropBase`

Represent a DROP SCHEMA statement.

The argument here is the string name of the schema.

| Member Name | Description |
| --- | --- |
| __init__() | Create a newDropSchemaconstruct. |

   method [sqlalchemy.schema.DropSchema.](#sqlalchemy.schema.DropSchema)__init__(*name:str*, *cascade:bool=False*, *if_exists:bool=False*) → None

Create a new [DropSchema](#sqlalchemy.schema.DropSchema) construct.
