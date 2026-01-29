# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Core Exceptions

Exceptions used with SQLAlchemy.

The base exception class is [SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError).  Exceptions which are
raised as a result of DBAPI exceptions are all subclasses of
[DBAPIError](#sqlalchemy.exc.DBAPIError).

   exception sqlalchemy.exc.AmbiguousForeignKeysError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

Raised when more than one foreign key matching can be located
between two selectables during a join.

    exception sqlalchemy.exc.ArgumentError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

Raised when an invalid or conflicting function argument is supplied.

This error generally corresponds to construction time state errors.

    exception sqlalchemy.exc.AwaitRequired

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

Error raised by the async greenlet spawn if no async operation
was awaited when it required one.

    exception sqlalchemy.exc.Base20DeprecationWarning

*inherits from* [sqlalchemy.exc.SADeprecationWarning](#sqlalchemy.exc.SADeprecationWarning)

Issued for usage of APIs specifically deprecated or legacy in
SQLAlchemy 2.0.

See also

[The <some function> in SQLAlchemy 2.0 will no longer <something>](https://docs.sqlalchemy.org/en/20/errors.html#error-b8d9).

[SQLAlchemy 2.0 Deprecations Mode](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#deprecation-20-mode)

    attribute [sqlalchemy.exc.Base20DeprecationWarning.](#sqlalchemy.exc.Base20DeprecationWarning)deprecated_since: str | None = '1.4'

Indicates the version that started raising this deprecation warning

     exception sqlalchemy.exc.CircularDependencyError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

Raised by topological sorts when a circular dependency is detected.

There are two scenarios where this error occurs:

- In a Session flush operation, if two objects are mutually dependent
  on each other, they can not be inserted or deleted via INSERT or
  DELETE statements alone; an UPDATE will be needed to post-associate
  or pre-deassociate one of the foreign key constrained values.
  The `post_update` flag described at [Rows that point to themselves / Mutually Dependent Rows](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#post-update) can resolve
  this cycle.
- In a [MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables) operation, two
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
  or [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects mutually refer to each
  other.  Apply the `use_alter=True` flag to one or both,
  see [Creating/Dropping Foreign Key Constraints via ALTER](https://docs.sqlalchemy.org/en/20/core/constraints.html#use-alter).

   method [sqlalchemy.exc.CircularDependencyError.](#sqlalchemy.exc.CircularDependencyError)__init__(*message:str*, *cycles:Any*, *edges:Any*, *msg:str|None=None*, *code:str|None=None*)     exception sqlalchemy.exc.CompileError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

Raised when an error occurs during SQL compilation

    exception sqlalchemy.exc.ConstraintColumnNotFoundError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

raised when a constraint refers to a string column name that
is not present in the table being constrained.

Added in version 2.0.

     exception sqlalchemy.exc.DBAPIError

*inherits from* [sqlalchemy.exc.StatementError](#sqlalchemy.exc.StatementError)

Raised when the execution of a database operation fails.

Wraps exceptions raised by the DB-API underlying the
database operation.  Driver-specific implementations of the standard
DB-API exception types are wrapped by matching sub-types of SQLAlchemy’s
[DBAPIError](#sqlalchemy.exc.DBAPIError) when possible.  DB-API’s `Error` type maps to
[DBAPIError](#sqlalchemy.exc.DBAPIError) in SQLAlchemy, otherwise the names are identical.  Note
that there is no guarantee that different DB-API implementations will
raise the same exception type for any given error condition.

[DBAPIError](#sqlalchemy.exc.DBAPIError) features [StatementError.statement](#sqlalchemy.exc.StatementError.statement)
and [StatementError.params](#sqlalchemy.exc.StatementError.params) attributes which supply context
regarding the specifics of the statement which had an issue, for the
typical case when the error was raised within the context of
emitting a SQL statement.

The wrapped exception object is available in the
[StatementError.orig](#sqlalchemy.exc.StatementError.orig) attribute. Its type and properties are
DB-API implementation specific.

   method [sqlalchemy.exc.DBAPIError.](#sqlalchemy.exc.DBAPIError)__init__(*statement:str|None*, *params:_AnyExecuteParams|None*, *orig:BaseException*, *hide_parameters:bool=False*, *connection_invalidated:bool=False*, *code:str|None=None*, *ismulti:bool|None=None*)     exception sqlalchemy.exc.DataError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API DataError.

    exception sqlalchemy.exc.DatabaseError

*inherits from* [sqlalchemy.exc.DBAPIError](#sqlalchemy.exc.DBAPIError)

Wraps a DB-API DatabaseError.

    exception sqlalchemy.exc.DisconnectionError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

A disconnect is detected on a raw DB-API connection.

This error is raised and consumed internally by a connection pool.  It can
be raised by the [PoolEvents.checkout()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.checkout)
event so that the host pool
forces a retry; the exception will be caught three times in a row before
the pool gives up and raises [InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)
regarding the connection attempt.

| Object Name | Description |
| --- | --- |
| DontWrapMixin | A mixin class which, when applied to a user-defined Exception class,
will not be wrapped inside ofStatementErrorif the error is
emitted within the process of executing a statement. |
| HasDescriptionCode | helper which adds ‘code’ as an attribute and ‘_code_str’ as a method |

   class sqlalchemy.exc.DontWrapMixin

A mixin class which, when applied to a user-defined Exception class,
will not be wrapped inside of [StatementError](#sqlalchemy.exc.StatementError) if the error is
emitted within the process of executing a statement.

E.g.:

```
from sqlalchemy.exc import DontWrapMixin

class MyCustomException(Exception, DontWrapMixin):
    pass

class MySpecialType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value == "invalid":
            raise MyCustomException("invalid!")
```

     exception sqlalchemy.exc.DuplicateColumnError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

a Column is being added to a Table that would replace another
Column, without appropriate parameters to allow this in place.

Added in version 2.0.0b4.

     class sqlalchemy.exc.HasDescriptionCode

helper which adds ‘code’ as an attribute and ‘_code_str’ as a method

    exception sqlalchemy.exc.IdentifierError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

Raised when a schema name is beyond the max character limit

    exception sqlalchemy.exc.IllegalStateChangeError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

An object that tracks state encountered an illegal state change
of some kind.

Added in version 2.0.

     exception sqlalchemy.exc.IntegrityError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API IntegrityError.

    exception sqlalchemy.exc.InterfaceError

*inherits from* [sqlalchemy.exc.DBAPIError](#sqlalchemy.exc.DBAPIError)

Wraps a DB-API InterfaceError.

    exception sqlalchemy.exc.InternalError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API InternalError.

    exception sqlalchemy.exc.InvalidRequestError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

SQLAlchemy was asked to do something it can’t do.

This error generally corresponds to runtime state errors.

    exception sqlalchemy.exc.InvalidatePoolError

*inherits from* [sqlalchemy.exc.DisconnectionError](#sqlalchemy.exc.DisconnectionError)

Raised when the connection pool should invalidate all stale connections.

A subclass of [DisconnectionError](#sqlalchemy.exc.DisconnectionError) that indicates that the
disconnect situation encountered on the connection probably means the
entire pool should be invalidated, as the database has been restarted.

This exception will be handled otherwise the same way as
[DisconnectionError](#sqlalchemy.exc.DisconnectionError), allowing three attempts to reconnect
before giving up.

Added in version 1.2.

     exception sqlalchemy.exc.LegacyAPIWarning

*inherits from* [sqlalchemy.exc.Base20DeprecationWarning](#sqlalchemy.exc.Base20DeprecationWarning)

indicates an API that is in ‘legacy’ status, a long term deprecation.

    exception sqlalchemy.exc.MissingGreenlet

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

Error raised by the async greenlet await_ if called while not inside
the greenlet spawn context.

    exception sqlalchemy.exc.MovedIn20Warning

*inherits from* [sqlalchemy.exc.Base20DeprecationWarning](#sqlalchemy.exc.Base20DeprecationWarning)

Subtype of RemovedIn20Warning to indicate an API that moved only.

    exception sqlalchemy.exc.MultipleResultsFound

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

A single database result was required but more than one were found.

Changed in version 1.4: This exception is now part of the
`sqlalchemy.exc` module in Core, moved from the ORM.  The symbol
remains importable from `sqlalchemy.orm.exc`.

     exception sqlalchemy.exc.NoForeignKeysError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

Raised when no foreign keys can be located between two selectables
during a join.

    exception sqlalchemy.exc.NoInspectionAvailable

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

A subject passed to `sqlalchemy.inspection.inspect()` produced
no context for inspection.

    exception sqlalchemy.exc.NoReferenceError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

Raised by `ForeignKey` to indicate a reference cannot be resolved.

    exception sqlalchemy.exc.NoReferencedColumnError

*inherits from* [sqlalchemy.exc.NoReferenceError](#sqlalchemy.exc.NoReferenceError)

Raised by `ForeignKey` when the referred `Column` cannot be
located.

   method [sqlalchemy.exc.NoReferencedColumnError.](#sqlalchemy.exc.NoReferencedColumnError)__init__(*message:str*, *tname:str*, *cname:str*)     exception sqlalchemy.exc.NoReferencedTableError

*inherits from* [sqlalchemy.exc.NoReferenceError](#sqlalchemy.exc.NoReferenceError)

Raised by `ForeignKey` when the referred `Table` cannot be
located.

   method [sqlalchemy.exc.NoReferencedTableError.](#sqlalchemy.exc.NoReferencedTableError)__init__(*message:str*, *tname:str*)     exception sqlalchemy.exc.NoResultFound

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

A database result was required but none was found.

Changed in version 1.4: This exception is now part of the
`sqlalchemy.exc` module in Core, moved from the ORM.  The symbol
remains importable from `sqlalchemy.orm.exc`.

     exception sqlalchemy.exc.NoSuchColumnError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError), `builtins.KeyError`

A nonexistent column is requested from a `Row`.

    exception sqlalchemy.exc.NoSuchModuleError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

Raised when a dynamically-loaded module (usually a database dialect)
of a particular name cannot be located.

    exception sqlalchemy.exc.NoSuchTableError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

Table does not exist or is not visible to a connection.

    exception sqlalchemy.exc.NotSupportedError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API NotSupportedError.

    exception sqlalchemy.exc.ObjectNotExecutableError

*inherits from* [sqlalchemy.exc.ArgumentError](#sqlalchemy.exc.ArgumentError)

Raised when an object is passed to .execute() that can’t be
executed as SQL.

   method [sqlalchemy.exc.ObjectNotExecutableError.](#sqlalchemy.exc.ObjectNotExecutableError)__init__(*target:Any*)     exception sqlalchemy.exc.OperationalError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API OperationalError.

    exception sqlalchemy.exc.PendingRollbackError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

A transaction has failed and needs to be rolled back before
continuing.

Added in version 1.4.

     exception sqlalchemy.exc.ProgrammingError

*inherits from* [sqlalchemy.exc.DatabaseError](#sqlalchemy.exc.DatabaseError)

Wraps a DB-API ProgrammingError.

    exception sqlalchemy.exc.ResourceClosedError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

An operation was requested from a connection, cursor, or other
object that’s in a closed state.

    exception sqlalchemy.exc.SADeprecationWarning

*inherits from* [sqlalchemy.exc.HasDescriptionCode](#sqlalchemy.exc.HasDescriptionCode), `builtins.DeprecationWarning`

Issued for usage of deprecated APIs.

   attribute [sqlalchemy.exc.SADeprecationWarning.](#sqlalchemy.exc.SADeprecationWarning)deprecated_since: str | None = None

Indicates the version that started raising this deprecation warning

     exception sqlalchemy.exc.SAPendingDeprecationWarning

*inherits from* `builtins.PendingDeprecationWarning`

A similar warning as [SADeprecationWarning](#sqlalchemy.exc.SADeprecationWarning), this warning
is not used in modern versions of SQLAlchemy.

   attribute [sqlalchemy.exc.SAPendingDeprecationWarning.](#sqlalchemy.exc.SAPendingDeprecationWarning)deprecated_since: str | None = None

Indicates the version that started raising this deprecation warning

     exception sqlalchemy.exc.SATestSuiteWarning

*inherits from* `builtins.Warning`

warning for a condition detected during tests that is non-fatal

Currently outside of SAWarning so that we can work around tools like
Alembic doing the wrong thing with warnings.

    exception sqlalchemy.exc.SAWarning

*inherits from* [sqlalchemy.exc.HasDescriptionCode](#sqlalchemy.exc.HasDescriptionCode), `builtins.RuntimeWarning`

Issued at runtime.

    exception sqlalchemy.exc.SQLAlchemyError

*inherits from* [sqlalchemy.exc.HasDescriptionCode](#sqlalchemy.exc.HasDescriptionCode), `builtins.Exception`

Generic error class.

    exception sqlalchemy.exc.StatementError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

An error occurred during execution of a SQL statement.

[StatementError](#sqlalchemy.exc.StatementError) wraps the exception raised
during execution, and features [statement](#sqlalchemy.exc.StatementError.statement)
and [params](#sqlalchemy.exc.StatementError.params) attributes which supply context regarding
the specifics of the statement which had an issue.

The wrapped exception object is available in
the [orig](#sqlalchemy.exc.StatementError.orig) attribute.

   method [sqlalchemy.exc.StatementError.](#sqlalchemy.exc.StatementError)__init__(*message:str*, *statement:str|None*, *params:_AnyExecuteParams|None*, *orig:BaseException|None*, *hide_parameters:bool=False*, *code:str|None=None*, *ismulti:bool|None=None*)    attribute [sqlalchemy.exc.StatementError.](#sqlalchemy.exc.StatementError)ismulti: bool | None = None

multi parameter passed to repr_params().  None is meaningful.

    attribute [sqlalchemy.exc.StatementError.](#sqlalchemy.exc.StatementError)orig: BaseException | None = None

The original exception that was thrown.

    attribute [sqlalchemy.exc.StatementError.](#sqlalchemy.exc.StatementError)params: _AnyExecuteParams | None = None

The parameter list being used when this exception occurred.

    attribute [sqlalchemy.exc.StatementError.](#sqlalchemy.exc.StatementError)statement: str | None = None

The string SQL statement being invoked when this exception occurred.

     exception sqlalchemy.exc.TimeoutError

*inherits from* [sqlalchemy.exc.SQLAlchemyError](#sqlalchemy.exc.SQLAlchemyError)

Raised when a connection pool times out on getting a connection.

    exception sqlalchemy.exc.UnboundExecutionError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

SQL was attempted without a database connection to execute it on.

    exception sqlalchemy.exc.UnreflectableTableError

*inherits from* [sqlalchemy.exc.InvalidRequestError](#sqlalchemy.exc.InvalidRequestError)

Table exists but can’t be reflected for some reason.

Added in version 1.2.

     exception sqlalchemy.exc.UnsupportedCompilationError

*inherits from* [sqlalchemy.exc.CompileError](#sqlalchemy.exc.CompileError)

Raised when an operation is not supported by the given compiler.

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

[Compiler StrSQLCompiler can’t render element of type <element type>](https://docs.sqlalchemy.org/en/20/errors.html#error-l7de)

    method [sqlalchemy.exc.UnsupportedCompilationError.](#sqlalchemy.exc.UnsupportedCompilationError)__init__(*compiler:Compiled|TypeCompiler*, *element_type:Type[ClauseElement]*, *message:str|None=None*)

---

# SQLAlchemy 2.0 Documentation

# SQL Statements and Expressions API

This section presents the API reference for the SQL Expression Language.
For an introduction, start with [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html#tutorial-working-with-data)
in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).

- [Column Elements and Expressions](https://docs.sqlalchemy.org/en/20/core/sqlelement.html)
  - [Column Element Foundational Constructors](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#column-element-foundational-constructors)
    - [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_)
    - [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
    - [bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bitwise_not)
    - [case()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.case)
    - [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast)
    - [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column)
    - [custom_op](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.custom_op)
    - [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct)
    - [extract()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.extract)
    - [false()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.false)
    - [func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func)
    - [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt)
    - [literal()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal)
    - [literal_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.literal_column)
    - [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_)
    - [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null)
    - [or_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.or_)
    - [outparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.outparam)
    - [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text)
    - [true()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.true)
    - [try_cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.try_cast)
    - [tuple_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.tuple_)
    - [type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce)
    - [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name)
  - [Column Element Modifier Constructors](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#column-element-modifier-constructors)
    - [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_)
    - [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_)
    - [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc)
    - [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between)
    - [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)
    - [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc)
    - [funcfilter()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.funcfilter)
    - [label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.label)
    - [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first)
    - [nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullsfirst)
    - [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last)
    - [nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nullslast)
    - [over()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.over)
    - [within_group()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.within_group)
  - [Column Element Class Documentation](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#column-element-class-documentation)
    - [BinaryExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BinaryExpression)
    - [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)
    - [Case](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Case)
    - [Cast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Cast)
    - [ClauseList](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ClauseList)
    - [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause)
    - [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
    - [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
    - [ColumnExpressionArgument](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnExpressionArgument)
    - [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)
    - [Extract](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Extract)
    - [False_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.False_)
    - [FunctionFilter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.FunctionFilter)
    - [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)
    - [Null](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Null)
    - [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)
    - [Over](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Over)
    - [SQLColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.SQLColumnExpression)
    - [TextClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TextClause)
    - [TryCast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TryCast)
    - [Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)
    - [WithinGroup](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.WithinGroup)
    - [WrapsColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.elements.WrapsColumnExpression)
    - [True_](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.True_)
    - [TypeCoerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.TypeCoerce)
    - [UnaryExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.UnaryExpression)
  - [Column Element Typing Utilities](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#column-element-typing-utilities)
    - [NotNullable()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.NotNullable)
    - [Nullable()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.Nullable)
- [Operator Reference](https://docs.sqlalchemy.org/en/20/core/operators.html)
  - [Comparison Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#comparison-operators)
  - [IN Comparisons](https://docs.sqlalchemy.org/en/20/core/operators.html#in-comparisons)
    - [IN against a list of values](https://docs.sqlalchemy.org/en/20/core/operators.html#in-against-a-list-of-values)
    - [Empty IN Expressions](https://docs.sqlalchemy.org/en/20/core/operators.html#empty-in-expressions)
    - [NOT IN](https://docs.sqlalchemy.org/en/20/core/operators.html#not-in)
    - [Tuple IN Expressions](https://docs.sqlalchemy.org/en/20/core/operators.html#tuple-in-expressions)
    - [Subquery IN](https://docs.sqlalchemy.org/en/20/core/operators.html#subquery-in)
  - [Identity Comparisons](https://docs.sqlalchemy.org/en/20/core/operators.html#identity-comparisons)
  - [String Comparisons](https://docs.sqlalchemy.org/en/20/core/operators.html#string-comparisons)
  - [String Containment](https://docs.sqlalchemy.org/en/20/core/operators.html#string-containment)
  - [String matching](https://docs.sqlalchemy.org/en/20/core/operators.html#string-matching)
  - [String Alteration](https://docs.sqlalchemy.org/en/20/core/operators.html#string-alteration)
  - [Arithmetic Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#arithmetic-operators)
  - [Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#bitwise-operators)
  - [Using Conjunctions and Negations](https://docs.sqlalchemy.org/en/20/core/operators.html#using-conjunctions-and-negations)
  - [Conjunction Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#conjunction-operators)
  - [Parentheses and Grouping](https://docs.sqlalchemy.org/en/20/core/operators.html#parentheses-and-grouping)
- [SELECT and Related Constructs](https://docs.sqlalchemy.org/en/20/core/selectable.html)
  - [Selectable Foundational Constructors](https://docs.sqlalchemy.org/en/20/core/selectable.html#selectable-foundational-constructors)
    - [except_()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.except_)
    - [except_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.except_all)
    - [exists()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.exists)
    - [intersect()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.intersect)
    - [intersect_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.intersect_all)
    - [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
    - [table()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.table)
    - [union()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union)
    - [union_all()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.union_all)
    - [values()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.values)
  - [Selectable Modifier Constructors](https://docs.sqlalchemy.org/en/20/core/selectable.html#selectable-modifier-constructors)
    - [alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.alias)
    - [cte()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.cte)
    - [join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.join)
    - [lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.lateral)
    - [outerjoin()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.outerjoin)
    - [tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.tablesample)
  - [Selectable Class Documentation](https://docs.sqlalchemy.org/en/20/core/selectable.html#selectable-class-documentation)
    - [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
    - [AliasedReturnsRows](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.AliasedReturnsRows)
    - [CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect)
    - [CTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CTE)
    - [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable)
    - [Exists](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Exists)
    - [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
    - [GenerativeSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.GenerativeSelect)
    - [HasCTE](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasCTE)
    - [HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes)
    - [HasSuffixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes)
    - [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)
    - [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral)
    - [ReturnsRows](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ReturnsRows)
    - [ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect)
    - [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
    - [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable)
    - [SelectBase](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase)
    - [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery)
    - [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)
    - [TableSample](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableSample)
    - [TableValuedAlias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableValuedAlias)
    - [TextualSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TextualSelect)
    - [Values](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Values)
    - [ScalarValues](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarValues)
  - [Label Style Constants](https://docs.sqlalchemy.org/en/20/core/selectable.html#label-style-constants)
    - [SelectLabelStyle](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectLabelStyle)
- [Insert, Updates, Deletes](https://docs.sqlalchemy.org/en/20/core/dml.html)
  - [DML Foundational Constructors](https://docs.sqlalchemy.org/en/20/core/dml.html#dml-foundational-constructors)
    - [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete)
    - [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert)
    - [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update)
  - [DML Class Documentation Constructors](https://docs.sqlalchemy.org/en/20/core/dml.html#dml-class-documentation-constructors)
    - [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)
    - [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)
    - [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
    - [UpdateBase](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase)
    - [ValuesBase](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.ValuesBase)
- [SQL and Generic Functions](https://docs.sqlalchemy.org/en/20/core/functions.html)
  - [Function API](https://docs.sqlalchemy.org/en/20/core/functions.html#function-api)
    - [AnsiFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.AnsiFunction)
    - [Function](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.Function)
    - [FunctionElement](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.FunctionElement)
    - [GenericFunction](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.GenericFunction)
    - [register_function()](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.register_function)
  - [Selected “Known” Functions](https://docs.sqlalchemy.org/en/20/core/functions.html#selected-known-functions)
    - [aggregate_strings](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.aggregate_strings)
    - [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg)
    - [char_length](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.char_length)
    - [coalesce](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.coalesce)
    - [concat](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.concat)
    - [count](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.count)
    - [cube](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.cube)
    - [cume_dist](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.cume_dist)
    - [current_date](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.current_date)
    - [current_time](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.current_time)
    - [current_timestamp](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.current_timestamp)
    - [current_user](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.current_user)
    - [dense_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.dense_rank)
    - [grouping_sets](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.grouping_sets)
    - [localtime](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.localtime)
    - [localtimestamp](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.localtimestamp)
    - [max](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.max)
    - [min](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.min)
    - [mode](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.mode)
    - [next_value](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.next_value)
    - [now](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.now)
    - [percent_rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percent_rank)
    - [percentile_cont](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_cont)
    - [percentile_disc](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.percentile_disc)
    - [random](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.random)
    - [rank](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.rank)
    - [rollup](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.rollup)
    - [session_user](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.session_user)
    - [sum](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.sum)
    - [sysdate](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.sysdate)
    - [user](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.user)
- [Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html)
  - [Synopsis](https://docs.sqlalchemy.org/en/20/core/compiler.html#synopsis)
  - [Dialect-specific compilation rules](https://docs.sqlalchemy.org/en/20/core/compiler.html#dialect-specific-compilation-rules)
  - [Compiling sub-elements of a custom expression construct](https://docs.sqlalchemy.org/en/20/core/compiler.html#compiling-sub-elements-of-a-custom-expression-construct)
    - [Cross Compiling between SQL and DDL compilers](https://docs.sqlalchemy.org/en/20/core/compiler.html#cross-compiling-between-sql-and-ddl-compilers)
  - [Changing the default compilation of existing constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#changing-the-default-compilation-of-existing-constructs)
  - [Changing Compilation of Types](https://docs.sqlalchemy.org/en/20/core/compiler.html#changing-compilation-of-types)
  - [Subclassing Guidelines](https://docs.sqlalchemy.org/en/20/core/compiler.html#subclassing-guidelines)
  - [Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#enabling-caching-support-for-custom-constructs)
  - [Further Examples](https://docs.sqlalchemy.org/en/20/core/compiler.html#further-examples)
    - [“UTC timestamp” function](https://docs.sqlalchemy.org/en/20/core/compiler.html#utc-timestamp-function)
    - [“GREATEST” function](https://docs.sqlalchemy.org/en/20/core/compiler.html#greatest-function)
    - [“false” expression](https://docs.sqlalchemy.org/en/20/core/compiler.html#false-expression)
  - [compiles()](https://docs.sqlalchemy.org/en/20/core/compiler.html#sqlalchemy.ext.compiler.compiles)
  - [deregister()](https://docs.sqlalchemy.org/en/20/core/compiler.html#sqlalchemy.ext.compiler.deregister)
- [Expression Serializer Extension](https://docs.sqlalchemy.org/en/20/core/serializer.html)
  - [Deserializer](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.Deserializer)
    - [Deserializer.get_engine()](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.Deserializer.get_engine)
    - [Deserializer.persistent_load()](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.Deserializer.persistent_load)
  - [Serializer](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.Serializer)
    - [Serializer.persistent_id()](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.Serializer.persistent_id)
  - [dumps()](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.dumps)
  - [loads()](https://docs.sqlalchemy.org/en/20/core/serializer.html#sqlalchemy.ext.serializer.loads)
- [SQL Expression Language Foundational Constructs](https://docs.sqlalchemy.org/en/20/core/foundation.html)
  - [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey)
    - [CacheKey.bindparams](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey.bindparams)
    - [CacheKey.key](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey.key)
    - [CacheKey.to_offline_string()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey.to_offline_string)
  - [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
    - [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare)
    - [ClauseElement.compile()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compile)
    - [ClauseElement.get_children()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.get_children)
    - [ClauseElement.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.inherit_cache)
    - [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params)
    - [ClauseElement.self_group()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.self_group)
    - [ClauseElement.unique_params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.unique_params)
  - [DialectKWArgs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs)
    - [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for)
    - [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs)
    - [DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options)
    - [DialectKWArgs.kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.kwargs)
  - [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey)
    - [HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache)
  - [LambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.LambdaElement)
  - [StatementLambdaElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement)
    - [StatementLambdaElement.add_criteria()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.add_criteria)
    - [StatementLambdaElement.is_delete](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_delete)
    - [StatementLambdaElement.is_dml](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_dml)
    - [StatementLambdaElement.is_insert](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_insert)
    - [StatementLambdaElement.is_select](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_select)
    - [StatementLambdaElement.is_text](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_text)
    - [StatementLambdaElement.is_update](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.is_update)
    - [StatementLambdaElement.spoil()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.StatementLambdaElement.spoil)
- [Visitor and Traversal Utilities](https://docs.sqlalchemy.org/en/20/core/visitors.html)
  - [ExternalTraversal](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.ExternalTraversal)
    - [ExternalTraversal.chain()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.ExternalTraversal.chain)
    - [ExternalTraversal.iterate()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.ExternalTraversal.iterate)
    - [ExternalTraversal.traverse()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.ExternalTraversal.traverse)
    - [ExternalTraversal.visitor_iterator](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.ExternalTraversal.visitor_iterator)
  - [InternalTraversal](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal)
    - [InternalTraversal.dp_annotations_key](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_annotations_key)
    - [InternalTraversal.dp_anon_name](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_anon_name)
    - [InternalTraversal.dp_boolean](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_boolean)
    - [InternalTraversal.dp_clauseelement](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_clauseelement)
    - [InternalTraversal.dp_clauseelement_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_clauseelement_list)
    - [InternalTraversal.dp_clauseelement_tuple](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_clauseelement_tuple)
    - [InternalTraversal.dp_clauseelement_tuples](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_clauseelement_tuples)
    - [InternalTraversal.dp_dialect_options](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_dialect_options)
    - [InternalTraversal.dp_dml_multi_values](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_dml_multi_values)
    - [InternalTraversal.dp_dml_ordered_values](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_dml_ordered_values)
    - [InternalTraversal.dp_dml_values](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_dml_values)
    - [InternalTraversal.dp_fromclause_canonical_column_collection](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_fromclause_canonical_column_collection)
    - [InternalTraversal.dp_fromclause_ordered_set](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_fromclause_ordered_set)
    - [InternalTraversal.dp_has_cache_key](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_has_cache_key)
    - [InternalTraversal.dp_has_cache_key_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_has_cache_key_list)
    - [InternalTraversal.dp_has_cache_key_tuples](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_has_cache_key_tuples)
    - [InternalTraversal.dp_ignore](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_ignore)
    - [InternalTraversal.dp_inspectable](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_inspectable)
    - [InternalTraversal.dp_inspectable_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_inspectable_list)
    - [InternalTraversal.dp_multi](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_multi)
    - [InternalTraversal.dp_multi_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_multi_list)
    - [InternalTraversal.dp_named_ddl_element](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_named_ddl_element)
    - [InternalTraversal.dp_operator](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_operator)
    - [InternalTraversal.dp_plain_dict](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_plain_dict)
    - [InternalTraversal.dp_plain_obj](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_plain_obj)
    - [InternalTraversal.dp_prefix_sequence](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_prefix_sequence)
    - [InternalTraversal.dp_propagate_attrs](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_propagate_attrs)
    - [InternalTraversal.dp_statement_hint_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_statement_hint_list)
    - [InternalTraversal.dp_string](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_string)
    - [InternalTraversal.dp_string_clauseelement_dict](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_string_clauseelement_dict)
    - [InternalTraversal.dp_string_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_string_list)
    - [InternalTraversal.dp_string_multi_dict](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_string_multi_dict)
    - [InternalTraversal.dp_table_hint_list](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_table_hint_list)
    - [InternalTraversal.dp_type](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_type)
    - [InternalTraversal.dp_unknown_structure](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.InternalTraversal.dp_unknown_structure)
  - [Visitable](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.Visitable)
  - [anon_map](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.anon_map)
  - [cloned_traverse()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.cloned_traverse)
  - [iterate()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.iterate)
  - [replacement_traverse()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.replacement_traverse)
  - [traverse()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.traverse)
  - [traverse_using()](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.traverse_using)

---

# SQLAlchemy 2.0 Documentation

# SQL Expression Language Foundational Constructs

Base classes and mixins that are used to compose SQL Expression Language
elements.

| Object Name | Description |
| --- | --- |
| CacheKey | The key used to identify a SQL statement construct in the
SQL compilation cache. |
| ClauseElement | Base class for elements of a programmatically constructed SQL
expression. |
| DialectKWArgs | Establish the ability for a class to have dialect-specific arguments
with defaults and constructor validation. |
| HasCacheKey | Mixin for objects which can produce a cache key. |
| LambdaElement | A SQL construct where the state is stored as an un-invoked lambda. |
| StatementLambdaElement | Represent a composable SQL statement as aLambdaElement. |

   class sqlalchemy.sql.expression.CacheKey

*inherits from* `builtins.tuple`

The key used to identify a SQL statement construct in the
SQL compilation cache.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

| Member Name | Description |
| --- | --- |
| bindparams | Alias for field number 1 |
| key | Alias for field number 0 |
| to_offline_string() | Generate an “offline string” form of thisCacheKey |

   attribute [sqlalchemy.sql.expression.CacheKey.](#sqlalchemy.sql.expression.CacheKey)bindparams: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)[Any]]

Alias for field number 1

    attribute [sqlalchemy.sql.expression.CacheKey.](#sqlalchemy.sql.expression.CacheKey)key: [Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[Any, ...]

Alias for field number 0

    method [sqlalchemy.sql.expression.CacheKey.](#sqlalchemy.sql.expression.CacheKey)to_offline_string(*statement_cache:MutableMapping[Any,str]*, *statement:ClauseElement*, *parameters:_CoreSingleExecuteParams*) → str

Generate an “offline string” form of this [CacheKey](#sqlalchemy.sql.expression.CacheKey)

The “offline string” is basically the string SQL for the
statement plus a repr of the bound parameter values in series.
Whereas the [CacheKey](#sqlalchemy.sql.expression.CacheKey) object is dependent on in-memory
identities in order to work as a cache key, the “offline” version
is suitable for a cache that will work for other processes as well.

The given `statement_cache` is a dictionary-like object where the
string form of the statement itself will be cached.  This dictionary
should be in a longer lived scope in order to reduce the time spent
stringifying statements.

     class sqlalchemy.sql.expression.ClauseElement

*inherits from* `sqlalchemy.sql.annotation.SupportsWrappingAnnotations`, `sqlalchemy.sql.cache_key.MemoizedHasCacheKey`, `sqlalchemy.sql.traversals.HasCopyInternals`, `sqlalchemy.sql.visitors.ExternallyTraversible`, `sqlalchemy.sql.expression.CompilerElement`

Base class for elements of a programmatically constructed SQL
expression.

| Member Name | Description |
| --- | --- |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| params() | Return a copy withbindparam()elements
replaced. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| unique_params() | Return a copy withbindparam()elements
replaced. |

   method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)compare(*other:ClauseElement*, ***kw:Any*) → bool

Compare this [ClauseElement](#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

*inherited from the* `CompilerElement.compile()` *method of* `CompilerElement`

Compile this SQL expression.

The return value is a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.
Calling `str()` or `unicode()` on the returned value will yield a
string representation of the result. The
[Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object also can return a
dictionary of bind parameter names and values
using the `params` accessor.

  Parameters:

- **bind** – An [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which
  can provide a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in order to generate a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  If the `bind` and
  `dialect` parameters are both omitted, a default SQL compiler
  is used.
- **column_keys** – Used for INSERT and UPDATE statements, a list of
  column names which should be present in the VALUES clause of the
  compiled statement. If `None`, all columns from the target table
  object are rendered.
- **dialect** – A [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) instance which can generate
  a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  This argument takes precedence over
  the `bind` argument.
- **compile_kwargs** –
  optional dictionary of additional parameters
  that will be passed through to the compiler within all “visit”
  methods.  This allows any custom flag to be passed through to
  a custom compilation construct, for example.  It is also used
  for the case of passing the `literal_binds` flag through:
  ```
  from sqlalchemy.sql import table, column, select
  t = table("t", column("x"))
  s = select(t).where(t.c.x == 5)
  print(s.compile(compile_kwargs={"literal_binds": True}))
  ```

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

     method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    attribute [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)inherit_cache = None

*inherited from the* `HasCacheKey.inherit_cache` *attribute of* [HasCacheKey](#sqlalchemy.sql.traversals.HasCacheKey)

Indicate if this [HasCacheKey](#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

     method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)params(*_ClauseElement__optionaldict:Mapping[str,Any]|None=None*, ***kwargs:Any*) → Self

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)self_group(*against:OperatorType|None=None*) → [ClauseElement](#sqlalchemy.sql.expression.ClauseElement)

Apply a ‘grouping’ to this [ClauseElement](#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.sql.expression.ClauseElement.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.sql.expression.ClauseElement.self_group) method of
[ClauseElement](#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.sql.expression.ClauseElement.](#sqlalchemy.sql.expression.ClauseElement)unique_params(*_ClauseElement__optionaldict:Dict[str,Any]|None=None*, ***kwargs:Any*) → Self

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

     class sqlalchemy.sql.base.DialectKWArgs

Establish the ability for a class to have dialect-specific arguments
with defaults and constructor validation.

The [DialectKWArgs](#sqlalchemy.sql.base.DialectKWArgs) interacts with the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) present on a dialect.

See also

[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments)

| Member Name | Description |
| --- | --- |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |

   classmethod [sqlalchemy.sql.base.DialectKWArgs.](#sqlalchemy.sql.base.DialectKWArgs)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

Add a new kind of dialect-specific keyword argument for this class.

E.g.:

```
Index.argument_for("mydialect", "length", None)

some_index = Index("a", "b", mydialect_length=5)
```

The [DialectKWArgs.argument_for()](#sqlalchemy.sql.base.DialectKWArgs.argument_for) method is a per-argument
way adding extra arguments to the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) dictionary. This
dictionary provides a list of argument names accepted by various
schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a
data member of the dialect class.  The use case for ad-hoc addition of
argument names is typically for end-user code that is also using
a custom compilation scheme which consumes the additional arguments.

  Parameters:

- **dialect_name** – name of a dialect.  The dialect must be
  locatable, else a [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError) is raised.   The
  dialect must also include an existing
  [DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) collection, indicating
  that it participates in the keyword-argument validation and default
  system, else [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.  If the dialect does
  not include this collection, then any keyword argument can be
  specified on behalf of this dialect already.  All dialects packaged
  within SQLAlchemy include this collection, however for third party
  dialects, support may vary.
- **argument_name** – name of the parameter.
- **default** – default value of the parameter.

      property dialect_kwargs: _DialectArgView

A collection of keyword arguments specified as dialect-specific
options to this construct.

The arguments are present here in their original `<dialect>_<kwarg>`
format.  Only arguments that were actually passed are included;
unlike the [DialectKWArgs.dialect_options](#sqlalchemy.sql.base.DialectKWArgs.dialect_options) collection, which
contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the
form `<dialect>_<kwarg>` where the value will be assembled
into the list of options.

See also

[DialectKWArgs.dialect_options](#sqlalchemy.sql.base.DialectKWArgs.dialect_options) - nested dictionary form

     attribute [sqlalchemy.sql.base.DialectKWArgs.](#sqlalchemy.sql.base.DialectKWArgs)dialect_options

A collection of keyword arguments specified as dialect-specific
options to this construct.

This is a two-level nested registry, keyed to `<dialect_name>`
and `<argument_name>`.  For example, the `postgresql_where`
argument would be locatable as:

```
arg = my_object.dialect_options["postgresql"]["where"]
```

Added in version 0.9.2.

See also

[DialectKWArgs.dialect_kwargs](#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs) - flat dictionary form

     property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     class sqlalchemy.sql.traversals.HasCacheKey

Mixin for objects which can produce a cache key.

This class is usually in a hierarchy that starts with the
`HasTraverseInternals` base, but this is optional.  Currently,
the class should be able to work on its own without including
`HasTraverseInternals`.

See also

[CacheKey](#sqlalchemy.sql.expression.CacheKey)

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

| Member Name | Description |
| --- | --- |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |

   attribute [sqlalchemy.sql.traversals.HasCacheKey.](#sqlalchemy.sql.traversals.HasCacheKey)inherit_cache: bool | None = None

Indicate if this [HasCacheKey](#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

      class sqlalchemy.sql.expression.LambdaElement

*inherits from* [sqlalchemy.sql.expression.ClauseElement](#sqlalchemy.sql.expression.ClauseElement)

A SQL construct where the state is stored as an un-invoked lambda.

The [LambdaElement](#sqlalchemy.sql.expression.LambdaElement) is produced transparently whenever
passing lambda expressions into SQL constructs, such as:

```
stmt = select(table).where(lambda: table.c.col == parameter)
```

The [LambdaElement](#sqlalchemy.sql.expression.LambdaElement) is the base of the
[StatementLambdaElement](#sqlalchemy.sql.expression.StatementLambdaElement) which represents a full statement
within a lambda.

Added in version 1.4.

See also

[Using Lambdas to add significant speed gains to statement production](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-lambda-caching)

     class sqlalchemy.sql.expression.StatementLambdaElement

*inherits from* `sqlalchemy.sql.roles.AllowsLambdaRole`, [sqlalchemy.sql.lambdas.LambdaElement](#sqlalchemy.sql.expression.LambdaElement), [sqlalchemy.sql.expression.Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable)

Represent a composable SQL statement as a [LambdaElement](#sqlalchemy.sql.expression.LambdaElement).

The [StatementLambdaElement](#sqlalchemy.sql.expression.StatementLambdaElement) is constructed using the
[lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt) function:

```
from sqlalchemy import lambda_stmt

stmt = lambda_stmt(lambda: select(table))
```

Once constructed, additional criteria can be built onto the statement
by adding subsequent lambdas, which accept the existing statement
object as a single parameter:

```
stmt += lambda s: s.where(table.c.col == parameter)
```

Added in version 1.4.

See also

[Using Lambdas to add significant speed gains to statement production](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-lambda-caching)

| Member Name | Description |
| --- | --- |
| add_criteria() | Add new criteria to thisStatementLambdaElement. |
| spoil() | Return a newStatementLambdaElementthat will run
all lambdas unconditionally each time. |

   method [sqlalchemy.sql.expression.StatementLambdaElement.](#sqlalchemy.sql.expression.StatementLambdaElement)add_criteria(*other:Callable[[Any],Any]*, *enable_tracking:bool=True*, *track_on:Any|None=None*, *track_closure_variables:bool=True*, *track_bound_values:bool=True*) → [StatementLambdaElement](#sqlalchemy.sql.expression.StatementLambdaElement)

Add new criteria to this [StatementLambdaElement](#sqlalchemy.sql.expression.StatementLambdaElement).

E.g.:

```
>>> def my_stmt(parameter):
...     stmt = lambda_stmt(
...         lambda: select(table.c.x, table.c.y),
...     )
...     stmt = stmt.add_criteria(lambda: table.c.x > parameter)
...     return stmt
```

The [StatementLambdaElement.add_criteria()](#sqlalchemy.sql.expression.StatementLambdaElement.add_criteria) method is
equivalent to using the Python addition operator to add a new
lambda, except that additional arguments may be added including
`track_closure_values` and `track_on`:

```
>>> def my_stmt(self, foo):
...     stmt = lambda_stmt(
...         lambda: select(func.max(foo.x, foo.y)),
...         track_closure_variables=False,
...     )
...     stmt = stmt.add_criteria(lambda: self.where_criteria, track_on=[self])
...     return stmt
```

See [lambda_stmt()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.lambda_stmt) for a description of the parameters
accepted.

    property is_delete

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    property is_dml

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    property is_insert

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    property is_select

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    property is_text

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    property is_update

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

    method [sqlalchemy.sql.expression.StatementLambdaElement.](#sqlalchemy.sql.expression.StatementLambdaElement)spoil() → NullLambdaStatement

Return a new [StatementLambdaElement](#sqlalchemy.sql.expression.StatementLambdaElement) that will run
all lambdas unconditionally each time.
