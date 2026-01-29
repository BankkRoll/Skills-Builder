# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# SQL Expression Language Tutorial

We’ve Moved!

This page is the previous home of the SQLAlchemy 1.x Tutorial.  As of 2.0,
SQLAlchemy presents a revised way of working and an all new tutorial that
presents Core and ORM in an integrated fashion using all the latest usage
patterns.    See [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).

---

# SQLAlchemy 2.0 Documentation

# Base Type API

| Object Name | Description |
| --- | --- |
| Concatenable | A mixin that marks a type as supporting ‘concatenation’,
typically strings. |
| ExternalType | mixin that defines attributes and behaviors specific to third-party
datatypes. |
| Indexable | A mixin that marks a type as supporting indexing operations,
such as array or JSON structures. |
| NullType | An unknown type. |
| TypeEngine | The ultimate base class for all SQL datatypes. |
| Variant | deprecated.  symbol is present for backwards-compatibility with
workaround recipes, however this actual type should not be used. |

   class sqlalchemy.types.TypeEngine

*inherits from* [sqlalchemy.sql.visitors.Visitable](https://docs.sqlalchemy.org/en/20/core/visitors.html#sqlalchemy.sql.visitors.Visitable), `typing.Generic`

The ultimate base class for all SQL datatypes.

Common subclasses of [TypeEngine](#sqlalchemy.types.TypeEngine) include
[String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String), [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer), and [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean).

For an overview of the SQLAlchemy typing system, see
[SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html).

See also

[SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html)

| Member Name | Description |
| --- | --- |
| operate() | Operate on an argument. |
| reverse_operate() | Reverse operate on an argument. |
| adapt() | Produce an “adapted” form of this type, given an “impl” class
to work with. |
| as_generic() | Return an instance of the generic type corresponding to this type
using heuristic rule. The method may be overridden if this
heuristic rule is not sufficient. |
| bind_expression() | Given a bind value (i.e. aBindParameterinstance),
return a SQL expression in its place. |
| bind_processor() | Return a conversion function for processing bind values. |
| coerce_compared_value() | Suggest a type for a ‘coerced’ Python value in an expression. |
| column_expression() | Given a SELECT column expression, return a wrapping SQL expression. |
| comparator_factory | alias ofComparator |
| compare_values() | Compare two values for equality. |
| compile() | Produce a string-compiled form of thisTypeEngine. |
| dialect_impl() | Return a dialect-specific implementation for thisTypeEngine. |
| evaluates_none() | Return a copy of this type which has theshould_evaluate_noneflag set to True. |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| hashable | Flag, if False, means values from this type aren’t hashable. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| render_bind_cast | Render bind casts forBindTyping.RENDER_CASTSmode. |
| render_literal_cast | render casts when rendering a value as an inline literal,
e.g. withTypeEngine.literal_processor(). |
| result_processor() | Return a conversion function for processing result row values. |
| should_evaluate_none | If True, the Python constantNoneis considered to be handled
explicitly by this type. |
| sort_key_function | A sorting function that can be passed as the key to sorted. |
| with_variant() | Produce a copy of this type object that will utilize the given
type when applied to the dialect of the given name. |

   class Comparator

*inherits from* [sqlalchemy.sql.expression.ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators), `typing.Generic`

Base class for custom comparison operations defined at the
type level.  See [TypeEngine.comparator_factory](#sqlalchemy.types.TypeEngine.comparator_factory).

   method [sqlalchemy.types.TypeEngine.Comparator.](#sqlalchemy.types.TypeEngine.Comparator)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

Operate on an argument.

This is the lowest level of operation, raises
`NotImplementedError` by default.

Overriding this on a subclass can allow common
behavior to be applied to all operations.
For example, overriding [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)
to apply `func.lower()` to the left and right
side:

```
class MyComparator(ColumnOperators):
    def operate(self, op, other, **kwargs):
        return op(func.lower(self), func.lower(other), **kwargs)
```

   Parameters:

- **op** – Operator callable.
- ***other** – the ‘other’ side of the operation. Will
  be a single scalar for most operations.
- ****kwargs** – modifiers.  These may be passed by special
  operators such as `ColumnOperators.contains()`.

      method [sqlalchemy.types.TypeEngine.Comparator.](#sqlalchemy.types.TypeEngine.Comparator)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_CT]

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.types.TypeEngine.Comparator.operate).

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)adapt(*cls:Type[TypeEngine|TypeEngineMixin]*, ***kw:Any*) → [TypeEngine](#sqlalchemy.types.TypeEngine)

Produce an “adapted” form of this type, given an “impl” class
to work with.

This method is used internally to associate generic
types with “implementation” types that are specific to a particular
dialect.

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)as_generic(*allow_nulltype:bool=False*) → [TypeEngine](#sqlalchemy.types.TypeEngine)

Return an instance of the generic type corresponding to this type
using heuristic rule. The method may be overridden if this
heuristic rule is not sufficient.

```
>>> from sqlalchemy.dialects.mysql import INTEGER
>>> INTEGER(display_width=4).as_generic()
Integer()
```

```
>>> from sqlalchemy.dialects.mysql import NVARCHAR
>>> NVARCHAR(length=100).as_generic()
Unicode(length=100)
```

Added in version 1.4.0b2.

See also

[Reflecting with Database-Agnostic Types](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-dbagnostic-types) - describes the
use of [TypeEngine.as_generic()](#sqlalchemy.types.TypeEngine.as_generic) in conjunction with
the `DDLEvents.column_reflect()` event, which is its
intended use.

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)bind_expression(*bindvalue:BindParameter[_T]*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_T] | None

Given a bind value (i.e. a [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) instance),
return a SQL expression in its place.

This is typically a SQL function that wraps the existing bound
parameter within the statement.  It is used for special data types
that require literals being wrapped in some special database function
in order to coerce an application-level value into a database-specific
format.  It is the SQL analogue of the
[TypeEngine.bind_processor()](#sqlalchemy.types.TypeEngine.bind_processor) method.

This method is called during the **SQL compilation** phase of a
statement, when rendering a SQL string. It is **not** called
against specific values.

Note that this method, when implemented, should always return
the exact same structure, without any conditional logic, as it
may be used in an executemany() call against an arbitrary number
of bound parameter sets.

Note

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_expression()](#sqlalchemy.types.TypeEngine.bind_expression)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_expression()](#sqlalchemy.types.TypeEngine.bind_expression), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.bind_expression()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.bind_expression).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

See also

[Applying SQL-level Bind/Result Processing](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-sql-value-processing)

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)bind_processor(*dialect:Dialect*) → _BindProcessorType[_T] | None

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)coerce_compared_value(*op:OperatorType|None*, *value:Any*) → [TypeEngine](#sqlalchemy.types.TypeEngine)[Any]

Suggest a type for a ‘coerced’ Python value in an expression.

Given an operator and value, gives the type a chance
to return a type which the value should be coerced into.

The default behavior here is conservative; if the right-hand
side is already coerced into a SQL type based on its
Python type, it is usually left alone.

End-user functionality extension here should generally be via
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator), which provides more liberal behavior in that
it defaults to coercing the other side of the expression into this
type, thus applying special Python conversions above and beyond those
needed by the DBAPI to both ides. It also provides the public method
[TypeDecorator.coerce_compared_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.coerce_compared_value) which is intended for
end-user customization of this behavior.

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)column_expression(*colexpr:ColumnElement[_T]*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_T] | None

Given a SELECT column expression, return a wrapping SQL expression.

This is typically a SQL function that wraps a column expression
as rendered in the columns clause of a SELECT statement.
It is used for special data types that require
columns to be wrapped in some special database function in order
to coerce the value before being sent back to the application.
It is the SQL analogue of the [TypeEngine.result_processor()](#sqlalchemy.types.TypeEngine.result_processor)
method.

Note

The `column_expression()` method is applied
only to the **outermost columns clause** of a SELECT statement, that
is, the columns that are to be delivered directly into the returned
result rows.  It does **not** apply to the columns clause inside
of subqueries.  This necessarily avoids double conversions against
the column and only runs the conversion when ready to be returned
to the client.

This method is called during the **SQL compilation** phase of a
statement, when rendering a SQL string. It is **not** called
against specific values.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.column_expression()](#sqlalchemy.types.TypeEngine.column_expression)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.column_expression()](#sqlalchemy.types.TypeEngine.column_expression), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.column_expression()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.column_expression).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

See also

[Applying SQL-level Bind/Result Processing](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-sql-value-processing)

     attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)comparator_factory

alias of [Comparator](#sqlalchemy.types.TypeEngine.Comparator)

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)compare_values(*x:Any*, *y:Any*) → bool

Compare two values for equality.

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)compile(*dialect:Dialect|None=None*) → str

Produce a string-compiled form of this [TypeEngine](#sqlalchemy.types.TypeEngine).

When called with no arguments, uses a “default” dialect
to produce a string result.

  Parameters:

**dialect** – a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) instance.

      method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)dialect_impl(*dialect:Dialect*) → [TypeEngine](#sqlalchemy.types.TypeEngine)[_T]

Return a dialect-specific implementation for this
[TypeEngine](#sqlalchemy.types.TypeEngine).

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)evaluates_none() → Self

Return a copy of this type which has the
[should_evaluate_none](#sqlalchemy.types.TypeEngine.should_evaluate_none) flag set to True.

E.g.:

```
Table(
    "some_table",
    metadata,
    Column(
        String(50).evaluates_none(),
        nullable=True,
        server_default="no value",
    ),
)
```

The ORM uses this flag to indicate that a positive value of `None`
is passed to the column in an INSERT statement, rather than omitting
the column from the INSERT statement which has the effect of firing
off column-level defaults.   It also allows for types which have
special behavior associated with the Python None value to indicate
that the value doesn’t necessarily translate into SQL NULL; a
prime example of this is a JSON type which may wish to persist the
JSON value `'null'`.

In all cases, the actual NULL SQL value can be always be
persisted in any column by using
the [null](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) SQL construct in an INSERT statement
or associated with an ORM-mapped attribute.

Note

The “evaluates none” flag does **not** apply to a value
of `None` passed to [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) or
[Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default); in these cases,
`None`
still means “no default”.

See also

[Forcing NULL on a column with a default](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#session-forcing-null) - in the ORM documentation

[JSON.none_as_null](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON.params.none_as_null) - PostgreSQL JSON
interaction with this flag.

[TypeEngine.should_evaluate_none](#sqlalchemy.types.TypeEngine.should_evaluate_none) - class-level flag

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)get_dbapi_type(*dbapi:DBAPIModule*) → Any | None

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)hashable = True

Flag, if False, means values from this type aren’t hashable.

Used by the ORM when uniquing result lists.

    method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)literal_processor(*dialect:Dialect*) → _LiteralProcessorType[_T] | None

Return a conversion function for processing literal values that are
to be rendered directly without using binds.

This function is used when the compiler makes use of the
“literal_binds” flag, typically used in DDL generation as well
as in certain scenarios where backends don’t accept bound parameters.

Returns a callable which will receive a literal Python value
as the sole positional argument and will return a string representation
to be rendered in a SQL statement.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type: Type[Any]

Return the Python type object expected to be returned
by instances of this type, if known.

Basically, for those types which enforce a return type,
or are known across the board to do such for all common
DBAPIs (like `int` for example), will return that type.

If a return type is not defined, raises
`NotImplementedError`.

Note that any type also accommodates NULL in SQL which
means you can also get back `None` from any type
in practice.

    attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)render_bind_cast = False

Render bind casts for [BindTyping.RENDER_CASTS](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.BindTyping.RENDER_CASTS) mode.

If True, this type (usually a dialect level impl type) signals
to the compiler that a cast should be rendered around a bound parameter
for this type.

Added in version 2.0.

See also

[BindTyping](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.BindTyping)

     attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)render_literal_cast = False

render casts when rendering a value as an inline literal,
e.g. with [TypeEngine.literal_processor()](#sqlalchemy.types.TypeEngine.literal_processor).

Added in version 2.0.

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)result_processor(*dialect:Dialect*, *coltype:object*) → _ResultProcessorType[_T] | None

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

      attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)should_evaluate_none: bool = False

If True, the Python constant `None` is considered to be handled
explicitly by this type.

The ORM uses this flag to indicate that a positive value of `None`
is passed to the column in an INSERT statement, rather than omitting
the column from the INSERT statement which has the effect of firing
off column-level defaults.   It also allows types which have special
behavior for Python None, such as a JSON type, to indicate that
they’d like to handle the None value explicitly.

To set this flag on an existing type, use the
[TypeEngine.evaluates_none()](#sqlalchemy.types.TypeEngine.evaluates_none) method.

See also

[TypeEngine.evaluates_none()](#sqlalchemy.types.TypeEngine.evaluates_none)

     attribute [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)sort_key_function: Callable[[Any], Any] | None = None

A sorting function that can be passed as the key to sorted.

The default value of `None` indicates that the values stored by
this type are self-sorting.

Added in version 1.3.8.

     method [sqlalchemy.types.TypeEngine.](#sqlalchemy.types.TypeEngine)with_variant(*type_:_TypeEngineArgument[Any]*, **dialect_names:str*) → Self

Produce a copy of this type object that will utilize the given
type when applied to the dialect of the given name.

e.g.:

```
from sqlalchemy.types import String
from sqlalchemy.dialects import mysql

string_type = String()

string_type = string_type.with_variant(
    mysql.VARCHAR(collation="foo"), "mysql", "mariadb"
)
```

The variant mapping indicates that when this type is
interpreted by a specific dialect, it will instead be
transmuted into the given type, rather than using the
primary type.

Changed in version 2.0: the [TypeEngine.with_variant()](#sqlalchemy.types.TypeEngine.with_variant)
method now works with a [TypeEngine](#sqlalchemy.types.TypeEngine) object “in
place”, returning a copy of the original type rather than returning
a wrapping object; the `Variant` class is no longer used.

   Parameters:

- **type_** – a [TypeEngine](#sqlalchemy.types.TypeEngine) that will be selected
  as a variant from the originating type, when a dialect
  of the given name is in use.
- ***dialect_names** –
  one or more base names of the dialect which
  uses this type. (i.e. `'postgresql'`, `'mysql'`, etc.)
  Changed in version 2.0: multiple dialect names can be specified
  for one variant.

See also

[Using “UPPERCASE” and Backend-specific types for multiple backends](https://docs.sqlalchemy.org/en/20/core/type_basics.html#types-with-variant) - illustrates the use of
[TypeEngine.with_variant()](#sqlalchemy.types.TypeEngine.with_variant).

      class sqlalchemy.types.Concatenable

*inherits from* `sqlalchemy.types.TypeEngineMixin`

A mixin that marks a type as supporting ‘concatenation’,
typically strings.

| Member Name | Description |
| --- | --- |
| comparator_factory | alias ofComparator |

   class Comparator

*inherits from* `sqlalchemy.types.Comparator`

     attribute [sqlalchemy.types.Concatenable.](#sqlalchemy.types.Concatenable)comparator_factory

alias of [Comparator](#sqlalchemy.types.Concatenable.Comparator)

     class sqlalchemy.types.Indexable

*inherits from* `sqlalchemy.types.TypeEngineMixin`

A mixin that marks a type as supporting indexing operations,
such as array or JSON structures.

| Member Name | Description |
| --- | --- |
| comparator_factory | alias ofComparator |

   class Comparator

*inherits from* `sqlalchemy.types.Comparator`

     attribute [sqlalchemy.types.Indexable.](#sqlalchemy.types.Indexable)comparator_factory

alias of [Comparator](#sqlalchemy.types.Indexable.Comparator)

     class sqlalchemy.types.NullType

*inherits from* [sqlalchemy.types.TypeEngine](#sqlalchemy.types.TypeEngine)

An unknown type.

[NullType](#sqlalchemy.types.NullType) is used as a default type for those cases where
a type cannot be determined, including:

- During table reflection, when the type of a column is not recognized
  by the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)
- When constructing SQL expressions using plain Python objects of
  unknown types (e.g. `somecolumn == my_special_object`)
- When a new [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is created,
  and the given type is passed
  as `None` or is not passed at all.

The [NullType](#sqlalchemy.types.NullType) can be used within SQL expression invocation
without issue, it just has no behavior either at the expression
construction level or at the bind-parameter/result processing level.
[NullType](#sqlalchemy.types.NullType) will result in a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) if the compiler
is asked to render the type itself, such as if it is used in a
[cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) operation or within a schema creation operation such as that
invoked by [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) or the
[CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable)
construct.

    class sqlalchemy.types.ExternalType

*inherits from* `sqlalchemy.types.TypeEngineMixin`

mixin that defines attributes and behaviors specific to third-party
datatypes.

“Third party” refers to datatypes that are defined outside the scope
of SQLAlchemy within either end-user application code or within
external extensions to SQLAlchemy.

Subclasses currently include [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) and
[UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType).

Added in version 1.4.28.

| Member Name | Description |
| --- | --- |
| cache_ok | Indicate if statements using thisExternalTypeare “safe to
cache”. |

   attribute [sqlalchemy.types.ExternalType.](#sqlalchemy.types.ExternalType)cache_ok: bool | None = None

Indicate if statements using this [ExternalType](#sqlalchemy.types.ExternalType) are “safe to
cache”.

The default value `None` will emit a warning and then not allow caching
of a statement which includes this type.   Set to `False` to disable
statements using this type from being cached at all without a warning.
When set to `True`, the object’s class and selected elements from its
state will be used as part of the cache key.  For example, using a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator):

```
class MyType(TypeDecorator):
    impl = String

    cache_ok = True

    def __init__(self, choices):
        self.choices = tuple(choices)
        self.internal_only = True
```

The cache key for the above type would be equivalent to:

```
>>> MyType(["a", "b", "c"])._static_cache_key
(<class '__main__.MyType'>, ('choices', ('a', 'b', 'c')))
```

The caching scheme will extract attributes from the type that correspond
to the names of parameters in the `__init__()` method.  Above, the
“choices” attribute becomes part of the cache key but “internal_only”
does not, because there is no parameter named “internal_only”.

The requirements for cacheable elements is that they are hashable
and also that they indicate the same SQL rendered for expressions using
this type every time for a given cache value.

To accommodate for datatypes that refer to unhashable structures such
as dictionaries, sets and lists, these objects can be made “cacheable”
by assigning hashable structures to the attributes whose names
correspond with the names of the arguments.  For example, a datatype
which accepts a dictionary of lookup values may publish this as a sorted
series of tuples.   Given a previously un-cacheable type as:

```
class LookupType(UserDefinedType):
    """a custom type that accepts a dictionary as a parameter.

    this is the non-cacheable version, as "self.lookup" is not
    hashable.

    """

    def __init__(self, lookup):
        self.lookup = lookup

    def get_col_spec(self, **kw):
        return "VARCHAR(255)"

    def bind_processor(self, dialect): ...  # works with "self.lookup" ...
```

Where “lookup” is a dictionary.  The type will not be able to generate
a cache key:

```
>>> type_ = LookupType({"a": 10, "b": 20})
>>> type_._static_cache_key
<stdin>:1: SAWarning: UserDefinedType LookupType({'a': 10, 'b': 20}) will not
produce a cache key because the ``cache_ok`` flag is not set to True.
Set this flag to True if this type object's state is safe to use
in a cache key, or False to disable this warning.
symbol('no_cache')
```

If we **did** set up such a cache key, it wouldn’t be usable. We would
get a tuple structure that contains a dictionary inside of it, which
cannot itself be used as a key in a “cache dictionary” such as SQLAlchemy’s
statement cache, since Python dictionaries aren’t hashable:

```
>>> # set cache_ok = True
>>> type_.cache_ok = True

>>> # this is the cache key it would generate
>>> key = type_._static_cache_key
>>> key
(<class '__main__.LookupType'>, ('lookup', {'a': 10, 'b': 20}))

>>> # however this key is not hashable, will fail when used with
>>> # SQLAlchemy statement cache
>>> some_cache = {key: "some sql value"}
Traceback (most recent call last): File "<stdin>", line 1,
in <module> TypeError: unhashable type: 'dict'
```

The type may be made cacheable by assigning a sorted tuple of tuples
to the “.lookup” attribute:

```
class LookupType(UserDefinedType):
    """a custom type that accepts a dictionary as a parameter.

    The dictionary is stored both as itself in a private variable,
    and published in a public variable as a sorted tuple of tuples,
    which is hashable and will also return the same value for any
    two equivalent dictionaries.  Note it assumes the keys and
    values of the dictionary are themselves hashable.

    """

    cache_ok = True

    def __init__(self, lookup):
        self._lookup = lookup

        # assume keys/values of "lookup" are hashable; otherwise
        # they would also need to be converted in some way here
        self.lookup = tuple((key, lookup[key]) for key in sorted(lookup))

    def get_col_spec(self, **kw):
        return "VARCHAR(255)"

    def bind_processor(self, dialect): ...  # works with "self._lookup" ...
```

Where above, the cache key for `LookupType({"a": 10, "b": 20})` will be:

```
>>> LookupType({"a": 10, "b": 20})._static_cache_key
(<class '__main__.LookupType'>, ('lookup', (('a', 10), ('b', 20))))
```

Added in version 1.4.14: - added the `cache_ok` flag to allow
some configurability of caching for [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) classes.

Added in version 1.4.28: - added the [ExternalType](#sqlalchemy.types.ExternalType) mixin which
generalizes the `cache_ok` flag to both the [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType) classes.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

      class sqlalchemy.types.Variant

*inherits from* [sqlalchemy.types.TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)

deprecated.  symbol is present for backwards-compatibility with
workaround recipes, however this actual type should not be used.

| Member Name | Description |
| --- | --- |
| with_variant() | Produce a copy of this type object that will utilize the given
type when applied to the dialect of the given name. |

   method [sqlalchemy.types.Variant.](#sqlalchemy.types.Variant)with_variant(*type_:_TypeEngineArgument[Any]*, **dialect_names:str*) → Self

*inherited from the* [TypeEngine.with_variant()](#sqlalchemy.types.TypeEngine.with_variant) *method of* [TypeEngine](#sqlalchemy.types.TypeEngine)

Produce a copy of this type object that will utilize the given
type when applied to the dialect of the given name.

e.g.:

```
from sqlalchemy.types import String
from sqlalchemy.dialects import mysql

string_type = String()

string_type = string_type.with_variant(
    mysql.VARCHAR(collation="foo"), "mysql", "mariadb"
)
```

The variant mapping indicates that when this type is
interpreted by a specific dialect, it will instead be
transmuted into the given type, rather than using the
primary type.

Changed in version 2.0: the [TypeEngine.with_variant()](#sqlalchemy.types.TypeEngine.with_variant)
method now works with a [TypeEngine](#sqlalchemy.types.TypeEngine) object “in
place”, returning a copy of the original type rather than returning
a wrapping object; the `Variant` class is no longer used.

   Parameters:

- **type_** – a [TypeEngine](#sqlalchemy.types.TypeEngine) that will be selected
  as a variant from the originating type, when a dialect
  of the given name is in use.
- ***dialect_names** –
  one or more base names of the dialect which
  uses this type. (i.e. `'postgresql'`, `'mysql'`, etc.)
  Changed in version 2.0: multiple dialect names can be specified
  for one variant.

See also

[Using “UPPERCASE” and Backend-specific types for multiple backends](https://docs.sqlalchemy.org/en/20/core/type_basics.html#types-with-variant) - illustrates the use of
[TypeEngine.with_variant()](#sqlalchemy.types.TypeEngine.with_variant).
