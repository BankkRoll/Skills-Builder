# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Core API Basics

- [Events](https://docs.sqlalchemy.org/en/20/core/event.html)
  - [Event Registration](https://docs.sqlalchemy.org/en/20/core/event.html#event-registration)
  - [Named Argument Styles](https://docs.sqlalchemy.org/en/20/core/event.html#named-argument-styles)
  - [Targets](https://docs.sqlalchemy.org/en/20/core/event.html#targets)
  - [Modifiers](https://docs.sqlalchemy.org/en/20/core/event.html#modifiers)
  - [Events and Multiprocessing](https://docs.sqlalchemy.org/en/20/core/event.html#events-and-multiprocessing)
  - [Event Reference](https://docs.sqlalchemy.org/en/20/core/event.html#event-reference)
  - [API Reference](https://docs.sqlalchemy.org/en/20/core/event.html#api-reference)
- [Runtime Inspection API](https://docs.sqlalchemy.org/en/20/core/inspection.html)
  - [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect)
  - [Available Inspection Targets](https://docs.sqlalchemy.org/en/20/core/inspection.html#available-inspection-targets)
- [Core Exceptions](https://docs.sqlalchemy.org/en/20/core/exceptions.html)
  - [AmbiguousForeignKeysError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.AmbiguousForeignKeysError)
  - [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError)
  - [AwaitRequired](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.AwaitRequired)
  - [Base20DeprecationWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.Base20DeprecationWarning)
  - [CircularDependencyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CircularDependencyError)
  - [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError)
  - [ConstraintColumnNotFoundError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ConstraintColumnNotFoundError)
  - [DBAPIError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DBAPIError)
  - [DataError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DataError)
  - [DatabaseError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DatabaseError)
  - [DisconnectionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DisconnectionError)
  - [DontWrapMixin](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DontWrapMixin)
  - [DuplicateColumnError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DuplicateColumnError)
  - [HasDescriptionCode](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.HasDescriptionCode)
  - [IdentifierError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.IdentifierError)
  - [IllegalStateChangeError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.IllegalStateChangeError)
  - [IntegrityError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.IntegrityError)
  - [InterfaceError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InterfaceError)
  - [InternalError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InternalError)
  - [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError)
  - [InvalidatePoolError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidatePoolError)
  - [LegacyAPIWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.LegacyAPIWarning)
  - [MissingGreenlet](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MissingGreenlet)
  - [MovedIn20Warning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MovedIn20Warning)
  - [MultipleResultsFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.MultipleResultsFound)
  - [NoForeignKeysError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoForeignKeysError)
  - [NoInspectionAvailable](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoInspectionAvailable)
  - [NoReferenceError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoReferenceError)
  - [NoReferencedColumnError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoReferencedColumnError)
  - [NoReferencedTableError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoReferencedTableError)
  - [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound)
  - [NoSuchColumnError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchColumnError)
  - [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError)
  - [NoSuchTableError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchTableError)
  - [NotSupportedError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NotSupportedError)
  - [ObjectNotExecutableError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ObjectNotExecutableError)
  - [OperationalError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.OperationalError)
  - [PendingRollbackError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.PendingRollbackError)
  - [ProgrammingError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ProgrammingError)
  - [ResourceClosedError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ResourceClosedError)
  - [SADeprecationWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SADeprecationWarning)
  - [SAPendingDeprecationWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SAPendingDeprecationWarning)
  - [SATestSuiteWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SATestSuiteWarning)
  - [SAWarning](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SAWarning)
  - [SQLAlchemyError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.SQLAlchemyError)
  - [StatementError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.StatementError)
  - [TimeoutError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.TimeoutError)
  - [UnboundExecutionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnboundExecutionError)
  - [UnreflectableTableError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnreflectableTableError)
  - [UnsupportedCompilationError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnsupportedCompilationError)
- [Core Internals](https://docs.sqlalchemy.org/en/20/core/internals.html)
  - [BindTyping](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.BindTyping)
  - [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)
  - [DBAPIConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIConnection)
  - [DBAPICursor](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPICursor)
  - [DBAPIType](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.interfaces.DBAPIType)
  - [DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler)
  - [DefaultDialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect)
  - [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)
  - [DefaultExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext)
  - [ExecutionContext](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.ExecutionContext)
  - [ExpandedState](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.ExpandedState)
  - [GenericTypeCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.GenericTypeCompiler)
  - [Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified)
  - [IdentifierPreparer](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.IdentifierPreparer)
  - [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler)
  - [StrSQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.StrSQLCompiler)
  - [AdaptedConnection](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.AdaptedConnection)

---

# SQLAlchemy 2.0 Documentation

# Custom SQL Constructs and Compilation Extension

Provides an API for creation of custom ClauseElements and compilers.

## Synopsis

Usage involves the creation of one or more
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) subclasses and one or
more callables defining its compilation:

```
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ColumnClause

class MyColumn(ColumnClause):
    inherit_cache = True

@compiles(MyColumn)
def compile_mycolumn(element, compiler, **kw):
    return "[%s]" % element.name
```

Above, `MyColumn` extends [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause),
the base expression element for named column objects. The `compiles`
decorator registers itself with the `MyColumn` class so that it is invoked
when the object is compiled to a string:

```
from sqlalchemy import select

s = select(MyColumn("x"), MyColumn("y"))
print(str(s))
```

Produces:

```
SELECT [x], [y]
```

## Dialect-specific compilation rules

Compilers can also be made dialect-specific. The appropriate compiler will be
invoked for the dialect in use:

```
from sqlalchemy.schema import DDLElement

class AlterColumn(DDLElement):
    inherit_cache = False

    def __init__(self, column, cmd):
        self.column = column
        self.cmd = cmd

@compiles(AlterColumn)
def visit_alter_column(element, compiler, **kw):
    return "ALTER COLUMN %s ..." % element.column.name

@compiles(AlterColumn, "postgresql")
def visit_alter_column(element, compiler, **kw):
    return "ALTER TABLE %s ALTER COLUMN %s ..." % (
        element.table.name,
        element.column.name,
    )
```

The second `visit_alter_table` will be invoked when any `postgresql`
dialect is used.

## Compiling sub-elements of a custom expression construct

The `compiler` argument is the
`Compiled` object in use. This object
can be inspected for any information about the in-progress compilation,
including `compiler.dialect`, `compiler.statement` etc. The
[SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler) and
[DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler) both include a `process()`
method which can be used for compilation of embedded attributes:

```
from sqlalchemy.sql.expression import Executable, ClauseElement

class InsertFromSelect(Executable, ClauseElement):
    inherit_cache = False

    def __init__(self, table, select):
        self.table = table
        self.select = select

@compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
    return "INSERT INTO %s (%s)" % (
        compiler.process(element.table, asfrom=True, **kw),
        compiler.process(element.select, **kw),
    )

insert = InsertFromSelect(t1, select(t1).where(t1.c.x > 5))
print(insert)
```

Produces (formatted for readability):

```
INSERT INTO mytable (
    SELECT mytable.x, mytable.y, mytable.z
    FROM mytable
    WHERE mytable.x > :x_1
)
```

Note

The above `InsertFromSelect` construct is only an example, this actual
functionality is already available using the
[Insert.from_select()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.from_select) method.

### Cross Compiling between SQL and DDL compilers

SQL and DDL constructs are each compiled using different base compilers -
`SQLCompiler` and `DDLCompiler`.   A common need is to access the
compilation rules of SQL expressions from within a DDL expression. The
`DDLCompiler` includes an accessor `sql_compiler` for this reason, such as
below where we generate a CHECK constraint that embeds a SQL expression:

```
@compiles(MyConstraint)
def compile_my_constraint(constraint, ddlcompiler, **kw):
    kw["literal_binds"] = True
    return "CONSTRAINT %s CHECK (%s)" % (
        constraint.name,
        ddlcompiler.sql_compiler.process(constraint.expression, **kw),
    )
```

Above, we add an additional flag to the process step as called by
`SQLCompiler.process()`, which is the `literal_binds` flag.  This
indicates that any SQL expression which refers to a [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)
object or other “literal” object such as those which refer to strings or
integers should be rendered **in-place**, rather than being referred to as
a bound parameter;  when emitting DDL, bound parameters are typically not
supported.

## Changing the default compilation of existing constructs

The compiler extension applies just as well to the existing constructs.  When
overriding the compilation of a built in SQL construct, the @compiles
decorator is invoked upon the appropriate class (be sure to use the class,
i.e. `Insert` or `Select`, instead of the creation function such
as `insert()` or `select()`).

Within the new compilation function, to get at the “original” compilation
routine, use the appropriate visit_XXX method - this
because compiler.process() will call upon the overriding routine and cause
an endless loop.   Such as, to add “prefix” to all insert statements:

```
from sqlalchemy.sql.expression import Insert

@compiles(Insert)
def prefix_inserts(insert, compiler, **kw):
    return compiler.visit_insert(insert.prefix_with("some prefix"), **kw)
```

The above compiler will prefix all INSERT statements with “some prefix” when
compiled.

## Changing Compilation of Types

`compiler` works for types, too, such as below where we implement the
MS-SQL specific ‘max’ keyword for `String`/`VARCHAR`:

```
@compiles(String, "mssql")
@compiles(VARCHAR, "mssql")
def compile_varchar(element, compiler, **kw):
    if element.length == "max":
        return "VARCHAR('max')"
    else:
        return compiler.visit_VARCHAR(element, **kw)

foo = Table("foo", metadata, Column("data", VARCHAR("max")))
```

## Subclassing Guidelines

A big part of using the compiler extension is subclassing SQLAlchemy
expression constructs. To make this easier, the expression and
schema packages feature a set of “bases” intended for common tasks.
A synopsis is as follows:

- [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) - This is the root
  expression class. Any SQL expression can be derived from this base, and is
  probably the best choice for longer constructs such as specialized INSERT
  statements.
- [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) - The root of all
  “column-like” elements. Anything that you’d place in the “columns” clause of
  a SELECT statement (as well as order by and group by) can derive from this -
  the object will automatically have Python “comparison” behavior.
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) classes want to have a
  `type` member which is expression’s return type.  This can be established
  at the instance level in the constructor, or at the class level if its
  generally constant:
  ```
  class timestamp(ColumnElement):
      type = TIMESTAMP()
      inherit_cache = True
  ```
- [FunctionElement](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement) - This is a hybrid of a
  `ColumnElement` and a “from clause” like object, and represents a SQL
  function or stored procedure type of call. Since most databases support
  statements along the line of “SELECT FROM <some function>”
  `FunctionElement` adds in the ability to be used in the FROM clause of a
  `select()` construct:
  ```
  from sqlalchemy.sql.expression import FunctionElement
  class coalesce(FunctionElement):
      name = "coalesce"
      inherit_cache = True
  @compiles(coalesce)
  def compile(element, compiler, **kw):
      return "coalesce(%s)" % compiler.process(element.clauses, **kw)
  @compiles(coalesce, "oracle")
  def compile(element, compiler, **kw):
      if len(element.clauses) > 2:
          raise TypeError(
              "coalesce only supports two arguments on " "Oracle Database"
          )
      return "nvl(%s)" % compiler.process(element.clauses, **kw)
  ```
- [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement) - The root of all DDL expressions,
  like CREATE TABLE, ALTER TABLE, etc. Compilation of
  [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement) subclasses is issued by a
  [DDLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.DDLCompiler) instead of a [SQLCompiler](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.sql.compiler.SQLCompiler).
  [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement) can also be used as an event hook in
  conjunction with event hooks like [DDLEvents.before_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_create) and
  [DDLEvents.after_create()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_create), allowing the construct to be invoked
  automatically during CREATE TABLE and DROP TABLE sequences.
  See also
  [Customizing DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html) - contains examples of associating
  [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) objects (which are themselves [ExecutableDDLElement](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement)
  instances) with [DDLEvents](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents) event hooks.
- [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) - This is a mixin which
  should be used with any expression class that represents a “standalone”
  SQL statement that can be passed directly to an `execute()` method.  It
  is already implicit within `DDLElement` and `FunctionElement`.

Most of the above constructs also respond to SQL statement caching.   A
subclassed construct will want to define the caching behavior for the object,
which usually means setting the flag `inherit_cache` to the value of
`False` or `True`.  See the next section [Enabling Caching Support for Custom Constructs](#compilerext-caching)
for background.

## Enabling Caching Support for Custom Constructs

SQLAlchemy as of version 1.4 includes a
[SQL compilation caching facility](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching) which will allow
equivalent SQL constructs to cache their stringified form, along with other
structural information used to fetch results from the statement.

For reasons discussed at [Object will not produce a cache key, Performance Implications](https://docs.sqlalchemy.org/en/20/errors.html#caching-caveats), the implementation of this
caching system takes a conservative approach towards including custom SQL
constructs and/or subclasses within the caching system.   This includes that
any user-defined SQL constructs, including all the examples for this
extension, will not participate in caching by default unless they positively
assert that they are able to do so.  The [HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache)
attribute when set to `True` at the class level of a specific subclass
will indicate that instances of this class may be safely cached, using the
cache key generation scheme of the immediate superclass.  This applies
for example to the “synopsis” example indicated previously:

```
class MyColumn(ColumnClause):
    inherit_cache = True

@compiles(MyColumn)
def compile_mycolumn(element, compiler, **kw):
    return "[%s]" % element.name
```

Above, the `MyColumn` class does not include any new state that
affects its SQL compilation; the cache key of `MyColumn` instances will
make use of that of the `ColumnClause` superclass, meaning it will take
into account the class of the object (`MyColumn`), the string name and
datatype of the object:

```
>>> MyColumn("some_name", String())._generate_cache_key()
CacheKey(
    key=('0', <class '__main__.MyColumn'>,
    'name', 'some_name',
    'type', (<class 'sqlalchemy.sql.sqltypes.String'>,
             ('length', None), ('collation', None))
), bindparams=[])
```

For objects that are likely to be **used liberally as components within many
larger statements**, such as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) subclasses and custom SQL
datatypes, it’s important that **caching be enabled as much as possible**, as
this may otherwise negatively affect performance.

An example of an object that **does** contain state which affects its SQL
compilation is the one illustrated at [Compiling sub-elements of a custom expression construct](#compilerext-compiling-subelements);
this is an “INSERT FROM SELECT” construct that combines together a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) as well as a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct, each of
which independently affect the SQL string generation of the construct.  For
this class, the example illustrates that it simply does not participate in
caching:

```
class InsertFromSelect(Executable, ClauseElement):
    inherit_cache = False

    def __init__(self, table, select):
        self.table = table
        self.select = select

@compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
    return "INSERT INTO %s (%s)" % (
        compiler.process(element.table, asfrom=True, **kw),
        compiler.process(element.select, **kw),
    )
```

While it is also possible that the above `InsertFromSelect` could be made to
produce a cache key that is composed of that of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) components together, the API for this is not at the moment
fully public. However, for an “INSERT FROM SELECT” construct, which is only
used by itself for specific operations, caching is not as critical as in the
previous example.

For objects that are **used in relative isolation and are generally
standalone**, such as custom [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) constructs like an “INSERT FROM
SELECT”, **caching is generally less critical** as the lack of caching for such
a construct will have only localized implications for that specific operation.

## Further Examples

### “UTC timestamp” function

A function that works like “CURRENT_TIMESTAMP” except applies the
appropriate conversions so that the time is in UTC time.   Timestamps are best
stored in relational databases as UTC, without time zones.   UTC so that your
database doesn’t think time has gone backwards in the hour when daylight
savings ends, without timezones because timezones are like character
encodings - they’re best applied only at the endpoints of an application
(i.e. convert to UTC upon user input, re-apply desired timezone upon display).

For PostgreSQL and Microsoft SQL Server:

```
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True

@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

@compiles(utcnow, "mssql")
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"
```

Example usage:

```
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

metadata = MetaData()
event = Table(
    "event",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("description", String(50), nullable=False),
    Column("timestamp", DateTime, server_default=utcnow()),
)
```

### “GREATEST” function

The “GREATEST” function is given any number of arguments and returns the one
that is of the highest value - its equivalent to Python’s `max`
function.  A SQL standard version versus a CASE based version which only
accommodates two arguments:

```
from sqlalchemy.sql import expression, case
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import Numeric

class greatest(expression.FunctionElement):
    type = Numeric()
    name = "greatest"
    inherit_cache = True

@compiles(greatest)
def default_greatest(element, compiler, **kw):
    return compiler.visit_function(element)

@compiles(greatest, "sqlite")
@compiles(greatest, "mssql")
@compiles(greatest, "oracle")
def case_greatest(element, compiler, **kw):
    arg1, arg2 = list(element.clauses)
    return compiler.process(case((arg1 > arg2, arg1), else_=arg2), **kw)
```

Example usage:

```
Session.query(Account).filter(
    greatest(Account.checking_balance, Account.savings_balance) > 10000
)
```

### “false” expression

Render a “false” constant expression, rendering as “0” on platforms that
don’t have a “false” constant:

```
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

class sql_false(expression.ColumnElement):
    inherit_cache = True

@compiles(sql_false)
def default_false(element, compiler, **kw):
    return "false"

@compiles(sql_false, "mssql")
@compiles(sql_false, "mysql")
@compiles(sql_false, "oracle")
def int_false(element, compiler, **kw):
    return "0"
```

Example usage:

```
from sqlalchemy import select, union_all

exp = union_all(
    select(users.c.name, sql_false().label("enrolled")),
    select(customers.c.name, customers.c.enrolled),
)
```

| Object Name | Description |
| --- | --- |
| compiles(class_, *specs) | Register a function as a compiler for a
givenClauseElementtype. |
| deregister(class_) | Remove all custom compilers associated with a givenClauseElementtype. |

   function sqlalchemy.ext.compiler.compiles(*class_:Type[Any]*, **specs:str*) → Callable[[_F], _F]

Register a function as a compiler for a
given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) type.

    function sqlalchemy.ext.compiler.deregister(*class_:Type[Any]*) → None

Remove all custom compilers associated with a given
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) type.
