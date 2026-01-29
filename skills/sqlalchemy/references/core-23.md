# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# The Type Hierarchy

SQLAlchemy provides abstractions for most common database data types,
as well as several techniques for customization of datatypes.

Database types are represented using Python classes, all of which ultimately
extend from the base type class known as [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine). There are
two general categories of datatypes, each of which express themselves within
the typing hierarchy in different ways. The category used by an individual
datatype class can be identified based on the use of two different naming
conventions, which are “CamelCase” and “UPPERCASE”.

See also

[Setting up MetaData with Table objects](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-core-metadata) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).  Illustrates
the most rudimental use of [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) type objects to
define [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata and introduces the concept
of type objects in tutorial form.

## The “CamelCase” datatypes

The rudimental types have “CamelCase” names such as [String](#sqlalchemy.types.String),
[Numeric](#sqlalchemy.types.Numeric), [Integer](#sqlalchemy.types.Integer), and [DateTime](#sqlalchemy.types.DateTime).
All of the immediate subclasses of [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) are
“CamelCase” types. The “CamelCase” types are to the greatest degree possible
**database agnostic**, meaning they can all be used on any database backend
where they will behave in such a way as appropriate to that backend in order to
produce the desired behavior.

An example of a straightforward “CamelCase” datatype is [String](#sqlalchemy.types.String).
On most backends, using this datatype in a
[table specification](https://docs.sqlalchemy.org/en/20/core/metadata.html#metadata-describing) will correspond to the
`VARCHAR` database type being used on the target backend, delivering string
values to and from the database, as in the example below:

```
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_name", String, primary_key=True),
    Column("email_address", String(60)),
)
```

When using a particular [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) definition or in any SQL expression overall, if no
arguments are required it may be passed as the class itself, that is, without
instantiating it with `()`. If arguments are needed, such as the length
argument of 60 in the `"email_address"` column above, the type may be
instantiated.

Another “CamelCase” datatype that expresses more backend-specific behavior
is the [Boolean](#sqlalchemy.types.Boolean) datatype. Unlike [String](#sqlalchemy.types.String),
which represents a string datatype that all databases have,
not every backend has a real “boolean” datatype; some make use of integers
or BIT values 0 and 1, some have boolean literal constants `true` and
`false` while others dont.   For this datatype, [Boolean](#sqlalchemy.types.Boolean)
may render `BOOLEAN` on a backend such as PostgreSQL, `BIT` on the
MySQL backend and `SMALLINT` on Oracle Database.  As data is sent and
received from the database using this type, based on the dialect in use it
may be interpreting Python numeric or boolean values.

The typical SQLAlchemy application will likely wish to use primarily
“CamelCase” types in the general case, as they will generally provide the best
basic behavior and be automatically portable to all backends.

Reference for the general set of “CamelCase” datatypes is below at
[Generic “CamelCase” Types](#types-generic).

## The “UPPERCASE” datatypes

In contrast to the “CamelCase” types are the “UPPERCASE” datatypes. These
datatypes are always inherited from a particular “CamelCase” datatype, and
always represent an **exact** datatype.   When using an “UPPERCASE” datatype,
the name of the type is always rendered exactly as given, without regard for
whether or not the current backend supports it.   Therefore the use
of “UPPERCASE” types in a SQLAlchemy application indicates that specific
datatypes are required, which then implies that the application would normally,
without additional steps taken,
be limited to those backends which use the type exactly as given.   Examples
of UPPERCASE types include [VARCHAR](#sqlalchemy.types.VARCHAR), [NUMERIC](#sqlalchemy.types.NUMERIC),
[INTEGER](#sqlalchemy.types.INTEGER), and [TIMESTAMP](#sqlalchemy.types.TIMESTAMP), which inherit directly
from the previously mentioned “CamelCase” types
[String](#sqlalchemy.types.String),
[Numeric](#sqlalchemy.types.Numeric), [Integer](#sqlalchemy.types.Integer), and [DateTime](#sqlalchemy.types.DateTime),
respectively.

The “UPPERCASE” datatypes that are part of `sqlalchemy.types` are common
SQL types that typically expect to be available on at least two backends
if not more.

Reference for the general set of “UPPERCASE” datatypes is below at
[SQL Standard and Multiple Vendor “UPPERCASE” Types](#types-sqlstandard).

## Backend-specific “UPPERCASE” datatypes

Most databases also have their own datatypes that
are either fully specific to those databases, or add additional arguments
that are specific to those databases.   For these datatypes, specific
SQLAlchemy dialects provide **backend-specific** “UPPERCASE” datatypes, for a
SQL type that has no analogue on other backends.  Examples of backend-specific
uppercase datatypes include PostgreSQL’s [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB), SQL Server’s
[IMAGE](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.IMAGE) and MySQL’s [TINYTEXT](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TINYTEXT).

Specific backends may also include “UPPERCASE” datatypes that extend the
arguments available from that same “UPPERCASE” datatype as found in the
`sqlalchemy.types` module. An example is when creating a MySQL string
datatype, one might want to specify MySQL-specific arguments such as `charset`
or `national`, which are available from the MySQL version
of [VARCHAR](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.VARCHAR) as the MySQL-only parameters
[VARCHAR.charset](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.VARCHAR.params.charset) and [VARCHAR.national](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.VARCHAR.params.national).

API documentation for backend-specific types are in the dialect-specific
documentation, listed at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html).

## Using “UPPERCASE” and Backend-specific types for multiple backends

Reviewing the presence of “UPPERCASE” and “CamelCase” types leads to the natural
use case of how to make use of “UPPERCASE” datatypes for backend-specific
options, but only when that backend is in use.   To tie together the
database-agnostic “CamelCase” and backend-specific “UPPERCASE” systems, one
makes use of the [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method in order to
**compose** types together to work with specific behaviors on specific backends.

Such as, to use the [String](#sqlalchemy.types.String) datatype, but when running on MySQL
to make use of the [VARCHAR.charset](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.VARCHAR.params.charset) parameter of
[VARCHAR](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.VARCHAR) when the table is created on MySQL or MariaDB,
[TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) may be used as below:

```
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_name", String(100), primary_key=True),
    Column(
        "bio",
        String(255).with_variant(VARCHAR(255, charset="utf8"), "mysql", "mariadb"),
    ),
)
```

In the above table definition, the `"bio"` column will have string-behaviors
on all backends. On most backends it will render in DDL as `VARCHAR`. However
on MySQL and MariaDB (indicated by database URLs that start with `mysql` or
`mariadb`), it will render as `VARCHAR(255) CHARACTER SET utf8`.

See also

[TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) - additional usage examples and notes

## Generic “CamelCase” Types

Generic types specify a column that can read, write and store a
particular type of Python data.  SQLAlchemy will choose the best
database column type available on the target database when issuing a
`CREATE TABLE` statement.  For complete control over which column
type is emitted in `CREATE TABLE`, such as `VARCHAR` see
[SQL Standard and Multiple Vendor “UPPERCASE” Types](#types-sqlstandard) and the other sections of this chapter.

| Object Name | Description |
| --- | --- |
| BigInteger | A type for biggerintintegers. |
| Boolean | A bool datatype. |
| Date | A type fordatetime.date()objects. |
| DateTime | A type fordatetime.datetime()objects. |
| Double | A type for doubleFLOATfloating point types. |
| Enum | Generic Enum Type. |
| Float | Type representing floating point types, such asFLOATorREAL. |
| Integer | A type forintintegers. |
| Interval | A type fordatetime.timedelta()objects. |
| LargeBinary | A type for large binary byte data. |
| MatchType | Refers to the return type of the MATCH operator. |
| Numeric | Base for non-integer numeric types, such asNUMERIC,FLOAT,DECIMAL, and other variants. |
| PickleType | Holds Python objects, which are serialized using pickle. |
| SchemaType | Add capabilities to a type which allow for schema-level DDL to be
associated with a type. |
| SmallInteger | A type for smallerintintegers. |
| String | The base for all string and character types. |
| Text | A variably sized string type. |
| Time | A type fordatetime.time()objects. |
| Unicode | A variable length Unicode string type. |
| UnicodeText | An unbounded-length Unicode string type. |
| Uuid | Represent a database agnostic UUID datatype. |

   class sqlalchemy.types.BigInteger

*inherits from* [sqlalchemy.types.Integer](#sqlalchemy.types.Integer)

A type for bigger `int` integers.

Typically generates a `BIGINT` in DDL, and otherwise acts like
a normal [Integer](#sqlalchemy.types.Integer) on the Python side.

    class sqlalchemy.types.Boolean

*inherits from* [sqlalchemy.types.SchemaType](#sqlalchemy.types.SchemaType), `sqlalchemy.types.Emulated`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

A bool datatype.

[Boolean](#sqlalchemy.types.Boolean) typically uses BOOLEAN or SMALLINT on the DDL side,
and on the Python side deals in `True` or `False`.

The [Boolean](#sqlalchemy.types.Boolean) datatype currently has two levels of assertion
that the values persisted are simple true/false values.  For all
backends, only the Python values `None`, `True`, `False`, `1`
or `0` are accepted as parameter values.   For those backends that
don’t support a “native boolean” datatype, an option exists to
also create a CHECK constraint on the target column

Changed in version 1.2: the [Boolean](#sqlalchemy.types.Boolean) datatype now asserts that
incoming Python values are already in pure boolean form.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Boolean. |
| bind_processor() | Return a conversion function for processing bind values. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| result_processor() | Return a conversion function for processing result row values. |

   method [sqlalchemy.types.Boolean.](#sqlalchemy.types.Boolean)__init__(*create_constraint:bool=False*, *name:str|None=None*, *_create_events:bool=True*, *_adapted_from:SchemaType|None=None*)

Construct a Boolean.

  Parameters:

- **create_constraint** –
  defaults to False.  If the boolean
  is generated as an int/smallint, also create a CHECK constraint
  on the table that ensures 1 or 0 as a value.
  Note
  it is strongly recommended that the CHECK constraint
  have an explicit name in order to support schema-management
  concerns.  This can be established either by setting the
  [Boolean.name](#sqlalchemy.types.Boolean.params.name) parameter or by setting up an
  appropriate naming convention; see
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions) for background.
  Changed in version 1.4: - this flag now defaults to False, meaning
  no CHECK constraint is generated for a non-native enumerated
  type.
- **name** – if a CHECK constraint is generated, specify
  the name of the constraint.

      method [sqlalchemy.types.Boolean.](#sqlalchemy.types.Boolean)bind_processor(*dialect*)

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.Boolean.](#sqlalchemy.types.Boolean)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

    method [sqlalchemy.types.Boolean.](#sqlalchemy.types.Boolean)result_processor(*dialect*, *coltype*)

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

       class sqlalchemy.types.Date

*inherits from* `sqlalchemy.types._RenderISO8601NoT`, `sqlalchemy.types.HasExpressionLookup`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

A type for `datetime.date()` objects.

| Member Name | Description |
| --- | --- |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |

   method [sqlalchemy.types.Date.](#sqlalchemy.types.Date)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.Date.](#sqlalchemy.types.Date)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

     class sqlalchemy.types.DateTime

*inherits from* `sqlalchemy.types._RenderISO8601NoT`, `sqlalchemy.types.HasExpressionLookup`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

A type for `datetime.datetime()` objects.

Date and time types return objects from the Python `datetime`
module.  Most DBAPIs have built in support for the datetime
module, with the noted exception of SQLite.  In the case of
SQLite, date and time types are stored as strings which are then
converted back to datetime objects when rows are returned.

For the time representation within the datetime type, some
backends include additional options, such as timezone support and
fractional seconds support.  For fractional seconds, use the
dialect-specific datatype, such as [TIME](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TIME).  For
timezone support, use at least the [TIMESTAMP](#sqlalchemy.types.TIMESTAMP) datatype,
if not the dialect-specific datatype object.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newDateTime. |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |

   method [sqlalchemy.types.DateTime.](#sqlalchemy.types.DateTime)__init__(*timezone:bool=False*)

Construct a new [DateTime](#sqlalchemy.types.DateTime).

  Parameters:

**timezone** – boolean.  Indicates that the datetime type should
enable timezone support, if available on the
**base date/time-holding type only**.   It is recommended
to make use of the [TIMESTAMP](#sqlalchemy.types.TIMESTAMP) datatype directly when
using this flag, as some databases include separate generic
date/time-holding types distinct from the timezone-capable
TIMESTAMP datatype, such as Oracle Database.

      method [sqlalchemy.types.DateTime.](#sqlalchemy.types.DateTime)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.DateTime.](#sqlalchemy.types.DateTime)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

     class sqlalchemy.types.Enum

*inherits from* [sqlalchemy.types.String](#sqlalchemy.types.String), [sqlalchemy.types.SchemaType](#sqlalchemy.types.SchemaType), `sqlalchemy.types.Emulated`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Generic Enum Type.

The [Enum](#sqlalchemy.types.Enum) type provides a set of possible string values
which the column is constrained towards.

The [Enum](#sqlalchemy.types.Enum) type will make use of the backend’s native “ENUM”
type if one is available; otherwise, it uses a VARCHAR datatype.
An option also exists to automatically produce a CHECK constraint
when the VARCHAR (so called “non-native”) variant is produced;
see the  [Enum.create_constraint](#sqlalchemy.types.Enum.params.create_constraint) flag.

The [Enum](#sqlalchemy.types.Enum) type also provides in-Python validation of string
values during both read and write operations.  When reading a value
from the database in a result set, the string value is always checked
against the list of possible values and a `LookupError` is raised
if no match is found.  When passing a value to the database as a
plain string within a SQL statement, if the
[Enum.validate_strings](#sqlalchemy.types.Enum.params.validate_strings) parameter is
set to True, a `LookupError` is raised for any string value that’s
not located in the given list of possible values; note that this
impacts usage of LIKE expressions with enumerated values (an unusual
use case).

The source of enumerated values may be a list of string values, or
alternatively a PEP-435-compliant enumerated class.  For the purposes
of the [Enum](#sqlalchemy.types.Enum) datatype, this class need only provide a
`__members__` method.

When using an enumerated class, the enumerated objects are used
both for input and output, rather than strings as is the case with
a plain-string enumerated type:

```
import enum
from sqlalchemy import Enum

class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3

t = Table("data", MetaData(), Column("value", Enum(MyEnum)))

connection.execute(t.insert(), {"value": MyEnum.two})
assert connection.scalar(t.select()) is MyEnum.two
```

Above, the string names of each element, e.g. “one”, “two”, “three”,
are persisted to the database; the values of the Python Enum, here
indicated as integers, are **not** used; the value of each enum can
therefore be any kind of Python object whether or not it is persistable.

In order to persist the values and not the names, the
[Enum.values_callable](#sqlalchemy.types.Enum.params.values_callable) parameter may be used.   The value of
this parameter is a user-supplied callable, which  is intended to be used
with a PEP-435-compliant enumerated class and  returns a list of string
values to be persisted.   For a simple enumeration that uses string values,
a callable such as  `lambda x: [e.value for e in x]` is sufficient.

See also

[Using Python Enum or pep-586 Literal types in the type map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-enums) - background on using
the [Enum](#sqlalchemy.types.Enum) datatype with the ORM’s
[ORM Annotated Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column)
feature.

[ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) - PostgreSQL-specific type,
which has additional functionality.

[ENUM](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.ENUM) - MySQL-specific type

| Member Name | Description |
| --- | --- |
| __init__() | Construct an enum. |
| create() | Issue CREATE DDL for this type, if applicable. |
| drop() | Issue DROP DDL for this type, if applicable. |

   method [sqlalchemy.types.Enum.](#sqlalchemy.types.Enum)__init__(**enums:str|Type[Enum]*, ***kw:Any*) → None

Construct an enum.

Keyword arguments which don’t apply to a specific backend are ignored
by that backend.

  Parameters:

- ***enums** – either exactly one PEP-435 compliant enumerated type
  or one or more string labels.
- **create_constraint** –
  defaults to False.  When creating a
  non-native enumerated type, also build a CHECK constraint on the
  database against the valid values.
  Note
  it is strongly recommended that the CHECK constraint
  have an explicit name in order to support schema-management
  concerns.  This can be established either by setting the
  [Enum.name](#sqlalchemy.types.Enum.params.name) parameter or by setting up an
  appropriate naming convention; see
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions) for background.
  Changed in version 1.4: - this flag now defaults to False, meaning
  no CHECK constraint is generated for a non-native enumerated
  type.
- **metadata** –
  Associate this type directly with a `MetaData`
  object. For types that exist on the target database as an
  independent schema construct (PostgreSQL), this type will be
  created and dropped within `create_all()` and `drop_all()`
  operations. If the type is not associated with any `MetaData`
  object, it will associate itself with each `Table` in which it is
  used, and will be created when any of those individual tables are
  created, after a check is performed for its existence. The type is
  only dropped when `drop_all()` is called for that `Table`
  object’s metadata, however.
  The value of the [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter of
  the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object, if set, will be used as the
  default value of the [Enum.schema](#sqlalchemy.types.Enum.params.schema) on this object
  if an explicit value is not otherwise supplied.
  Changed in version 1.4.12: [Enum](#sqlalchemy.types.Enum) inherits the
  [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter of the
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object if present, when passed using
  the [Enum.metadata](#sqlalchemy.types.Enum.params.metadata) parameter.
- **name** – The name of this type. This is required for PostgreSQL
  and any future supported database which requires an explicitly
  named type, or an explicitly named constraint in order to generate
  the type and/or a table that uses it. If a PEP-435 enumerated
  class was used, its name (converted to lower case) is used by
  default.
- **native_enum** – Use the database’s native ENUM type when
  available. Defaults to True. When False, uses VARCHAR + check
  constraint for all backends. When False, the VARCHAR length can be
  controlled with [Enum.length](#sqlalchemy.types.Enum.params.length); currently “length” is
  ignored if native_enum=True.
- **length** –
  Allows specifying a custom length for the VARCHAR
  when a non-native enumeration datatype is used.  By default it uses
  the length of the longest value.
  Changed in version 2.0.0: The [Enum.length](#sqlalchemy.types.Enum.params.length) parameter
  is used unconditionally for `VARCHAR` rendering regardless of
  the [Enum.native_enum](#sqlalchemy.types.Enum.params.native_enum) parameter, for those backends
  where `VARCHAR` is used for enumerated datatypes.
- **schema** –
  Schema name of this type. For types that exist on the
  target database as an independent schema construct (PostgreSQL),
  this parameter specifies the named schema in which the type is
  present.
  If not present, the schema name will be taken from the
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection if passed as
  [Enum.metadata](#sqlalchemy.types.Enum.params.metadata), for a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  that includes the [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter.
  Changed in version 1.4.12: [Enum](#sqlalchemy.types.Enum) inherits the
  [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter of the
  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object if present, when passed using
  the [Enum.metadata](#sqlalchemy.types.Enum.params.metadata) parameter.
  Otherwise, if the [Enum.inherit_schema](#sqlalchemy.types.Enum.params.inherit_schema) flag is set
  to `True`, the schema will be inherited from the associated
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object if any; when
  [Enum.inherit_schema](#sqlalchemy.types.Enum.params.inherit_schema) is at its default of
  `False`, the owning table’s schema is **not** used.
- **quote** – Set explicit quoting preferences for the type’s name.
- **inherit_schema** – When `True`, the “schema” from the owning
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  will be copied to the “schema” attribute of this
  [Enum](#sqlalchemy.types.Enum), replacing whatever value was passed for the
  `schema` attribute.   This also takes effect when using the
  [Table.to_metadata()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.to_metadata) operation.
- **validate_strings** – when True, string values that are being
  passed to the database in a SQL statement will be checked
  for validity against the list of enumerated values.  Unrecognized
  values will result in a `LookupError` being raised.
- **values_callable** –
  A callable which will be passed the PEP-435
  compliant enumerated type, which should then return a list of string
  values to be persisted. This allows for alternate usages such as
  using the string value of an enum to be persisted to the database
  instead of its name. The callable must return the values to be
  persisted in the same order as iterating through the Enum’s
  `__member__` attribute. For example
  `lambda x: [i.value for i in x]`.
  Added in version 1.2.3.
- **sort_key_function** –
  a Python callable which may be used as the
  “key” argument in the Python `sorted()` built-in.   The SQLAlchemy
  ORM requires that primary key columns which are mapped must
  be sortable in some way.  When using an unsortable enumeration
  object such as a Python 3 `Enum` object, this parameter may be
  used to set a default sort key function for the objects.  By
  default, the database value of the enumeration is used as the
  sorting function.
  Added in version 1.3.8.
- **omit_aliases** –
  A boolean that when true will remove aliases from
  pep 435 enums. defaults to `True`.
  Changed in version 2.0: This parameter now defaults to True.

      method [sqlalchemy.types.Enum.](#sqlalchemy.types.Enum)create(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

*inherited from the* [SchemaType.create()](#sqlalchemy.types.SchemaType.create) *method of* [SchemaType](#sqlalchemy.types.SchemaType)

Issue CREATE DDL for this type, if applicable.

    method [sqlalchemy.types.Enum.](#sqlalchemy.types.Enum)drop(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

*inherited from the* [SchemaType.drop()](#sqlalchemy.types.SchemaType.drop) *method of* [SchemaType](#sqlalchemy.types.SchemaType)

Issue DROP DDL for this type, if applicable.

     class sqlalchemy.types.Double

*inherits from* [sqlalchemy.types.Float](#sqlalchemy.types.Float)

A type for double `FLOAT` floating point types.

Typically generates a `DOUBLE` or `DOUBLE_PRECISION` in DDL,
and otherwise acts like a normal [Float](#sqlalchemy.types.Float) on the Python
side.

Added in version 2.0.

     class sqlalchemy.types.Float

*inherits from* [sqlalchemy.types.Numeric](#sqlalchemy.types.Numeric)

Type representing floating point types, such as `FLOAT` or `REAL`.

This type returns Python `float` objects by default, unless the
[Float.asdecimal](#sqlalchemy.types.Float.params.asdecimal) flag is set to `True`, in which case they
are coerced to `decimal.Decimal` objects.

When a [Float.precision](#sqlalchemy.types.Float.params.precision) is not provided in a
[Float](#sqlalchemy.types.Float) type some backend may compile this type as
an 8 bytes / 64 bit float datatype. To use a 4 bytes / 32 bit float
datatype a precision <= 24 can usually be provided or the
[REAL](#sqlalchemy.types.REAL) type can be used.
This is known to be the case in the PostgreSQL and MSSQL dialects
that render the type as `FLOAT` that’s in both an alias of
`DOUBLE PRECISION`. Other third party dialects may have similar
behavior.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Float. |
| result_processor() | Return a conversion function for processing result row values. |

   method [sqlalchemy.types.Float.](#sqlalchemy.types.Float)__init__(*precision:int|None=None*, *asdecimal:bool=False*, *decimal_return_scale:int|None=None*)

Construct a Float.

  Parameters:

- **precision** –
  the numeric precision for use in DDL `CREATE
  TABLE`. Backends **should** attempt to ensure this precision
  indicates a number of digits for the generic
  [Float](#sqlalchemy.types.Float) datatype.
  Note
  For the Oracle Database backend, the
  [Float.precision](#sqlalchemy.types.Float.params.precision) parameter is not accepted
  when rendering DDL, as Oracle Database does not support float precision
  specified as a number of decimal places. Instead, use the
  Oracle Database-specific [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype and specify the
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) parameter. This is new
  in version 2.0 of SQLAlchemy.
  To create a database agnostic [Float](#sqlalchemy.types.Float) that
  separately specifies binary precision for Oracle Database, use
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) as follows:
  ```
  from sqlalchemy import Column
  from sqlalchemy import Float
  from sqlalchemy.dialects import oracle
  Column(
      "float_data",
      Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
  )
  ```
- **asdecimal** – the same flag as that of [Numeric](#sqlalchemy.types.Numeric), but
  defaults to `False`.   Note that setting this flag to `True`
  results in floating point conversion.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Note that the
  MySQL float types, which do include “scale”, will use “scale”
  as the default for decimal_return_scale, if not otherwise specified.

      method [sqlalchemy.types.Float.](#sqlalchemy.types.Float)result_processor(*dialect*, *coltype*)

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

       class sqlalchemy.types.Integer

*inherits from* `sqlalchemy.types.HasExpressionLookup`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

A type for `int` integers.

| Member Name | Description |
| --- | --- |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |

   method [sqlalchemy.types.Integer.](#sqlalchemy.types.Integer)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.Integer.](#sqlalchemy.types.Integer)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

     class sqlalchemy.types.Interval

*inherits from* `sqlalchemy.types.Emulated`, `sqlalchemy.types._AbstractInterval`, [sqlalchemy.types.TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)

A type for `datetime.timedelta()` objects.

The Interval type deals with `datetime.timedelta` objects.  In PostgreSQL
and Oracle Database, the native `INTERVAL` type is used; for others, the
value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).

Note that the `Interval` type does not currently provide date arithmetic
operations on platforms which do not support interval types natively. Such
operations usually require transformation of both sides of the expression
(such as, conversion of both sides into integer epoch values first) which
currently is a manual procedure (such as via
[expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func)).

| Member Name | Description |
| --- | --- |
| __init__() | Construct an Interval object. |
| adapt_to_emulated() | Given an impl class, adapt this type to the impl assuming
“emulated”. |
| bind_processor() | Return a conversion function for processing bind values. |
| cache_ok | Indicate if statements using thisExternalTypeare “safe to
cache”. |
| coerce_compared_value() | Suggest a type for a ‘coerced’ Python value in an expression. |
| comparator_factory | alias ofComparator |
| impl | alias ofDateTime |
| result_processor() | Return a conversion function for processing result row values. |

   class Comparator

*inherits from* `sqlalchemy.types.Comparator`, `sqlalchemy.types.Comparator`

     method [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)__init__(*native:bool=True*, *second_precision:int|None=None*, *day_precision:int|None=None*)

Construct an Interval object.

  Parameters:

- **native** – when True, use the actual
  INTERVAL type provided by the database, if
  supported (currently PostgreSQL, Oracle Database).
  Otherwise, represent the interval data as
  an epoch value regardless.
- **second_precision** – For native interval types
  which support a “fractional seconds precision” parameter,
  i.e. Oracle Database and PostgreSQL
- **day_precision** – for native interval types which
  support a “day precision” parameter, i.e. Oracle Database.

      method [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)adapt_to_emulated(*impltype*, ***kw*)

Given an impl class, adapt this type to the impl assuming
“emulated”.

The impl should also be an “emulated” version of this type,
most likely the same class as this type itself.

e.g.: sqltypes.Enum adapts to the Enum class.

    method [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)bind_processor(*dialect:Dialect*) → _BindProcessorType[dt.timedelta]

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      attribute [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)cache_ok = True

Indicate if statements using this [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) are “safe to
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

Added in version 1.4.28: - added the [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) mixin which
generalizes the `cache_ok` flag to both the [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType) classes.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

     method [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)coerce_compared_value(*op*, *value*)

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

    attribute [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)comparator_factory

alias of [Comparator](#sqlalchemy.types.Interval.Comparator)

    attribute [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)impl

alias of [DateTime](#sqlalchemy.types.DateTime)

    property python_type

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

    method [sqlalchemy.types.Interval.](#sqlalchemy.types.Interval)result_processor(*dialect:Dialect*, *coltype:Any*) → _ResultProcessorType[dt.timedelta]

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

       class sqlalchemy.types.LargeBinary

*inherits from* `sqlalchemy.types._Binary`

A type for large binary byte data.

The [LargeBinary](#sqlalchemy.types.LargeBinary) type corresponds to a large and/or unlengthed
binary type for the target platform, such as BLOB on MySQL and BYTEA for
PostgreSQL.  It also handles the necessary conversions for the DBAPI.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a LargeBinary type. |

   method [sqlalchemy.types.LargeBinary.](#sqlalchemy.types.LargeBinary)__init__(*length:int|None=None*)

Construct a LargeBinary type.

  Parameters:

**length** – optional, a length for the column for use in
DDL statements, for those binary types that accept a length,
such as the MySQL BLOB type.

       class sqlalchemy.types.MatchType

*inherits from* [sqlalchemy.types.Boolean](#sqlalchemy.types.Boolean)

Refers to the return type of the MATCH operator.

As the [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) is probably the most open-ended
operator in generic SQLAlchemy Core, we can’t assume the return type
at SQL evaluation time, as MySQL returns a floating point, not a boolean,
and other backends might do something different.    So this type
acts as a placeholder, currently subclassing [Boolean](#sqlalchemy.types.Boolean).
The type allows dialects to inject result-processing functionality
if needed, and on MySQL will return floating-point values.

    class sqlalchemy.types.Numeric

*inherits from* `sqlalchemy.types.HasExpressionLookup`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Base for non-integer numeric types, such as
`NUMERIC`, `FLOAT`, `DECIMAL`, and other variants.

The [Numeric](#sqlalchemy.types.Numeric) datatype when used directly will render DDL
corresponding to precision numerics if available, such as
`NUMERIC(precision, scale)`.  The [Float](#sqlalchemy.types.Float) subclass will
attempt to render a floating-point datatype such as `FLOAT(precision)`.

[Numeric](#sqlalchemy.types.Numeric) returns Python `decimal.Decimal` objects by default,
based on the default value of `True` for the
[Numeric.asdecimal](#sqlalchemy.types.Numeric.params.asdecimal) parameter.  If this parameter is set to
False, returned values are coerced to Python `float` objects.

The [Float](#sqlalchemy.types.Float) subtype, being more specific to floating point,
defaults the [Float.asdecimal](#sqlalchemy.types.Float.params.asdecimal) flag to False so that the
default Python datatype is `float`.

Note

When using a [Numeric](#sqlalchemy.types.Numeric) datatype against a database type that
returns Python floating point values to the driver, the accuracy of the
decimal conversion indicated by [Numeric.asdecimal](#sqlalchemy.types.Numeric.params.asdecimal) may be
limited.   The behavior of specific numeric/floating point datatypes
is a product of the SQL datatype in use, the Python [DBAPI](https://docs.sqlalchemy.org/en/20/glossary.html#term-DBAPI)
in use, as well as strategies that may be present within
the SQLAlchemy dialect in use.   Users requiring specific precision/
scale are encouraged to experiment with the available datatypes
in order to determine the best results.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Numeric. |
| bind_processor() | Return a conversion function for processing bind values. |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| result_processor() | Return a conversion function for processing result row values. |

   method [sqlalchemy.types.Numeric.](#sqlalchemy.types.Numeric)__init__(*precision:int|None=None*, *scale:int|None=None*, *decimal_return_scale:int|None=None*, *asdecimal:bool=True*)

Construct a Numeric.

  Parameters:

- **precision** – the numeric precision for use in DDL `CREATE
  TABLE`.
- **scale** – the numeric scale for use in DDL `CREATE TABLE`.
- **asdecimal** – default True.  Return whether or not
  values should be sent as Python Decimal objects, or
  as floats.   Different DBAPIs send one or the other based on
  datatypes - the Numeric type will ensure that return values
  are one or the other across DBAPIs consistently.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Types which
  do include an explicit “.scale” value, such as the base
  [Numeric](#sqlalchemy.types.Numeric) as well as the MySQL float types, will use the
  value of “.scale” as the default for decimal_return_scale, if not
  otherwise specified.

When using the `Numeric` type, care should be taken to ensure
that the asdecimal setting is appropriate for the DBAPI in use -
when Numeric applies a conversion from Decimal->float or float->
Decimal, this conversion incurs an additional performance overhead
for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have
better accuracy and higher performance with a setting of `True`,
as the native translation to Decimal reduces the amount of floating-
point issues at play, and the Numeric type itself doesn’t need
to apply any further conversions.  However, another DBAPI which
returns floats natively *will* incur an additional conversion
overhead, and is still subject to floating point data loss - in
which case `asdecimal=False` will at least remove the extra
conversion overhead.

    method [sqlalchemy.types.Numeric.](#sqlalchemy.types.Numeric)bind_processor(*dialect*)

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.Numeric.](#sqlalchemy.types.Numeric)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.Numeric.](#sqlalchemy.types.Numeric)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

    method [sqlalchemy.types.Numeric.](#sqlalchemy.types.Numeric)result_processor(*dialect*, *coltype*)

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

       class sqlalchemy.types.PickleType

*inherits from* [sqlalchemy.types.TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)

Holds Python objects, which are serialized using pickle.

PickleType builds upon the Binary type to apply Python’s
`pickle.dumps()` to incoming objects, and `pickle.loads()` on
the way out, allowing any pickleable Python object to be stored as
a serialized binary field.

To allow ORM change events to propagate for elements associated
with [PickleType](#sqlalchemy.types.PickleType), see [Mutation Tracking](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html).

| Member Name | Description |
| --- | --- |
| __init__() | Construct a PickleType. |
| bind_processor() | Provide a bound value processing function for the
givenDialect. |
| cache_ok | Indicate if statements using thisExternalTypeare “safe to
cache”. |
| compare_values() | Given two values, compare them for equality. |
| impl | alias ofLargeBinary |
| result_processor() | Provide a result value processing function for the givenDialect. |

   method [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)__init__(*protocol:int=5*, *pickler:Any=None*, *comparator:Callable[[Any,Any],bool]|None=None*, *impl:_TypeEngineArgument[Any]|None=None*)

Construct a PickleType.

  Parameters:

- **protocol** – defaults to `pickle.HIGHEST_PROTOCOL`.
- **pickler** – defaults to pickle.  May be any object with
  pickle-compatible `dumps` and `loads` methods.
- **comparator** – a 2-arg callable predicate used
  to compare values of this type.  If left as `None`,
  the Python “equals” operator is used to compare values.
- **impl** –
  A binary-storing [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or
  instance to use in place of the default [LargeBinary](#sqlalchemy.types.LargeBinary).
  For example the :class: _mysql.LONGBLOB class may be more effective
  when using MySQL.
  Added in version 1.4.20.

      method [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)bind_processor(*dialect*)

Provide a bound value processing function for the
given [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

This is the method that fulfills the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
contract for bound value conversion which normally occurs via
the [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor) method.

Note

User-defined subclasses of [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) should
**not** implement this method, and should instead implement
[TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param) so that the “inner”
processing provided by the implementing type is maintained.

   Parameters:

**dialect** – Dialect instance in use.

      attribute [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)cache_ok = True

Indicate if statements using this [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) are “safe to
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

Added in version 1.4.28: - added the [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) mixin which
generalizes the `cache_ok` flag to both the [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType) classes.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

     method [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)compare_values(*x*, *y*)

Given two values, compare them for equality.

By default this calls upon [TypeEngine.compare_values()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.compare_values)
of the underlying “impl”, which in turn usually
uses the Python equals operator `==`.

This function is used by the ORM to compare
an original-loaded value with an intercepted
“changed” value, to determine if a net change
has occurred.

    attribute [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)impl

alias of [LargeBinary](#sqlalchemy.types.LargeBinary)

    method [sqlalchemy.types.PickleType.](#sqlalchemy.types.PickleType)result_processor(*dialect*, *coltype*)

Provide a result value processing function for the given
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

This is the method that fulfills the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
contract for bound value conversion which normally occurs via
the [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor) method.

Note

User-defined subclasses of [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) should
**not** implement this method, and should instead implement
[TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value) so that the
“inner” processing provided by the implementing type is maintained.

   Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – A SQLAlchemy data type

       class sqlalchemy.types.SchemaType

*inherits from* `sqlalchemy.sql.expression.SchemaEventTarget`, `sqlalchemy.types.TypeEngineMixin`

Add capabilities to a type which allow for schema-level DDL to be
associated with a type.

Supports types that must be explicitly created/dropped (i.e. PG ENUM type)
as well as types that are complimented by table or schema level
constraints, triggers, and other rules.

[SchemaType](#sqlalchemy.types.SchemaType) classes can also be targets for the
[DDLEvents.before_parent_attach()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.before_parent_attach) and
[DDLEvents.after_parent_attach()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.after_parent_attach) events, where the events fire off
surrounding the association of the type object with a parent
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

See also

[Enum](#sqlalchemy.types.Enum)

[Boolean](#sqlalchemy.types.Boolean)

| Member Name | Description |
| --- | --- |
| adapt() |  |
| copy() |  |
| create() | Issue CREATE DDL for this type, if applicable. |
| drop() | Issue DROP DDL for this type, if applicable. |
| name |  |

   method [sqlalchemy.types.SchemaType.](#sqlalchemy.types.SchemaType)adapt(*cls:Type[TypeEngine|TypeEngineMixin]*, ***kw:Any*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)    method [sqlalchemy.types.SchemaType.](#sqlalchemy.types.SchemaType)copy(***kw*)    method [sqlalchemy.types.SchemaType.](#sqlalchemy.types.SchemaType)create(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue CREATE DDL for this type, if applicable.

    method [sqlalchemy.types.SchemaType.](#sqlalchemy.types.SchemaType)drop(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue DROP DDL for this type, if applicable.

    attribute [sqlalchemy.types.SchemaType.](#sqlalchemy.types.SchemaType)name: str | None     class sqlalchemy.types.SmallInteger

*inherits from* [sqlalchemy.types.Integer](#sqlalchemy.types.Integer)

A type for smaller `int` integers.

Typically generates a `SMALLINT` in DDL, and otherwise acts like
a normal [Integer](#sqlalchemy.types.Integer) on the Python side.

    class sqlalchemy.types.String

*inherits from* [sqlalchemy.types.Concatenable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Concatenable), [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

The base for all string and character types.

In SQL, corresponds to VARCHAR.

The length field is usually required when the String type is
used within a CREATE TABLE statement, as VARCHAR requires a length
on most databases.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |
| bind_processor() | Return a conversion function for processing bind values. |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| result_processor() | Return a conversion function for processing result row values. |

   method [sqlalchemy.types.String.](#sqlalchemy.types.String)__init__(*length:int|None=None*, *collation:str|None=None*)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

      method [sqlalchemy.types.String.](#sqlalchemy.types.String)bind_processor(*dialect:Dialect*) → _BindProcessorType[str] | None

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.String.](#sqlalchemy.types.String)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.String.](#sqlalchemy.types.String)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

    method [sqlalchemy.types.String.](#sqlalchemy.types.String)result_processor(*dialect:Dialect*, *coltype:object*) → _ResultProcessorType[str] | None

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

       class sqlalchemy.types.Text

*inherits from* [sqlalchemy.types.String](#sqlalchemy.types.String)

A variably sized string type.

In SQL, usually corresponds to CLOB or TEXT.  In general, TEXT objects
do not have a length; while some databases will accept a length
argument here, it will be rejected by others.

    class sqlalchemy.types.Time

*inherits from* `sqlalchemy.types._RenderISO8601NoT`, `sqlalchemy.types.HasExpressionLookup`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

A type for `datetime.time()` objects.

| Member Name | Description |
| --- | --- |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |

   method [sqlalchemy.types.Time.](#sqlalchemy.types.Time)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

    method [sqlalchemy.types.Time.](#sqlalchemy.types.Time)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

     class sqlalchemy.types.Unicode

*inherits from* [sqlalchemy.types.String](#sqlalchemy.types.String)

A variable length Unicode string type.

The [Unicode](#sqlalchemy.types.Unicode) type is a [String](#sqlalchemy.types.String) subclass that assumes
input and output strings that may contain non-ASCII characters, and for
some backends implies an underlying column type that is explicitly
supporting of non-ASCII data, such as `NVARCHAR` on Oracle Database and
SQL Server.  This will impact the output of `CREATE TABLE` statements and
`CAST` functions at the dialect level.

The character encoding used by the [Unicode](#sqlalchemy.types.Unicode) type that is used to
transmit and receive data to the database is usually determined by the
DBAPI itself. All modern DBAPIs accommodate non-ASCII strings but may have
different methods of managing database encodings; if necessary, this
encoding should be configured as detailed in the notes for the target DBAPI
in the [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) section.

In modern SQLAlchemy, use of the [Unicode](#sqlalchemy.types.Unicode) datatype does not
imply any encoding/decoding behavior within SQLAlchemy itself.  In Python
3, all string objects are inherently Unicode capable, and SQLAlchemy
does not produce bytestring objects nor does it accommodate a DBAPI that
does not return Python Unicode objects in result sets for string values.

Warning

Some database backends, particularly SQL Server with pyodbc,
are known to have undesirable behaviors regarding data that is noted
as being of `NVARCHAR` type as opposed to `VARCHAR`, including
datatype mismatch errors and non-use of indexes.  See the section
on [DialectEvents.do_setinputsizes()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.do_setinputsizes) for background on working
around unicode character issues for backends like SQL Server with
pyodbc as well as cx_Oracle.

See also

[UnicodeText](#sqlalchemy.types.UnicodeText) - unlengthed textual counterpart
to [Unicode](#sqlalchemy.types.Unicode).

[DialectEvents.do_setinputsizes()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DialectEvents.do_setinputsizes)

     class sqlalchemy.types.UnicodeText

*inherits from* [sqlalchemy.types.Text](#sqlalchemy.types.Text)

An unbounded-length Unicode string type.

See [Unicode](#sqlalchemy.types.Unicode) for details on the unicode
behavior of this object.

Like [Unicode](#sqlalchemy.types.Unicode), usage the [UnicodeText](#sqlalchemy.types.UnicodeText) type implies a
unicode-capable type being used on the backend, such as
`NCLOB`, `NTEXT`.

    class sqlalchemy.types.Uuid

*inherits from* `sqlalchemy.types.Emulated`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Represent a database agnostic UUID datatype.

For backends that have no “native” UUID datatype, the value will
make use of `CHAR(32)` and store the UUID as a 32-character alphanumeric
hex string.

For backends which are known to support `UUID` directly or a similar
uuid-storing datatype such as SQL Server’s `UNIQUEIDENTIFIER`, a
“native” mode enabled by default allows these types will be used on those
backends.

In its default mode of use, the [Uuid](#sqlalchemy.types.Uuid) datatype expects
**Python uuid objects**, from the Python
[uuid](https://docs.python.org/3/library/uuid.html)
module:

```
import uuid

from sqlalchemy import Uuid
from sqlalchemy import Table, Column, MetaData, String

metadata_obj = MetaData()

t = Table(
    "t",
    metadata_obj,
    Column("uuid_data", Uuid, primary_key=True),
    Column("other_data", String),
)

with engine.begin() as conn:
    conn.execute(
        t.insert(), {"uuid_data": uuid.uuid4(), "other_data": "some data"}
    )
```

To have the [Uuid](#sqlalchemy.types.Uuid) datatype work with string-based
Uuids (e.g. 32 character hexadecimal strings), pass the
[Uuid.as_uuid](#sqlalchemy.types.Uuid.params.as_uuid) parameter with the value `False`.

Added in version 2.0.

See also

[UUID](#sqlalchemy.types.UUID) - represents exactly the `UUID` datatype
without any backend-agnostic behaviors.

| Member Name | Description |
| --- | --- |
| __init__() | Construct aUuidtype. |
| bind_processor() | Return a conversion function for processing bind values. |
| coerce_compared_value() | SeeTypeEngine.coerce_compared_value()for a description. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| result_processor() | Return a conversion function for processing result row values. |

   method [sqlalchemy.types.Uuid.](#sqlalchemy.types.Uuid)__init__(*as_uuid:bool=True*, *native_uuid:bool=True*)

Construct a [Uuid](#sqlalchemy.types.Uuid) type.

  Parameters:

- **as_uuid=True** –
  if True, values will be interpreted
  as Python uuid objects, converting to/from string via the
  DBAPI.
- **native_uuid=True** – if True, backends that support either the
  `UUID` datatype directly, or a UUID-storing value
  (such as SQL Server’s `UNIQUEIDENTIFIER` will be used by those
  backends.   If False, a `CHAR(32)` datatype will be used for
  all backends regardless of native support.

      method [sqlalchemy.types.Uuid.](#sqlalchemy.types.Uuid)bind_processor(*dialect:Dialect*) → _BindProcessorType[_UUID_RETURN] | None

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.Uuid.](#sqlalchemy.types.Uuid)coerce_compared_value(*op*, *value*)

See [TypeEngine.coerce_compared_value()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value) for a description.

    method [sqlalchemy.types.Uuid.](#sqlalchemy.types.Uuid)literal_processor(*dialect*)

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

      property python_type

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

    method [sqlalchemy.types.Uuid.](#sqlalchemy.types.Uuid)result_processor(*dialect*, *coltype*)

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

## SQL Standard and Multiple Vendor “UPPERCASE” Types

This category of types refers to types that are either part of the
SQL standard, or are potentially found within a subset of database backends.
Unlike the “generic” types, the SQL standard/multi-vendor types have **no**
guarantee of working on all backends, and will only work on those backends
that explicitly support them by name.  That is, the type will always emit
its exact name in DDL with `CREATE TABLE` is issued.

| Object Name | Description |
| --- | --- |
| ARRAY | Represent a SQL Array type. |
| BIGINT | The SQL BIGINT type. |
| BINARY | The SQL BINARY type. |
| BLOB | The SQL BLOB type. |
| BOOLEAN | The SQL BOOLEAN type. |
| CHAR | The SQL CHAR type. |
| CLOB | The CLOB type. |
| DATE | The SQL DATE type. |
| DATETIME | The SQL DATETIME type. |
| DECIMAL | The SQL DECIMAL type. |
| DOUBLE | The SQL DOUBLE type. |
| DOUBLE_PRECISION | The SQL DOUBLE PRECISION type. |
| FLOAT | The SQL FLOAT type. |
| INT | alias ofINTEGER |
| INTEGER | The SQL INT or INTEGER type. |
| JSON | Represent a SQL JSON type. |
| NCHAR | The SQL NCHAR type. |
| NUMERIC | The SQL NUMERIC type. |
| NVARCHAR | The SQL NVARCHAR type. |
| REAL | The SQL REAL type. |
| SMALLINT | The SQL SMALLINT type. |
| TEXT | The SQL TEXT type. |
| TIME | The SQL TIME type. |
| TIMESTAMP | The SQL TIMESTAMP type. |
| UUID | Represent the SQL UUID type. |
| VARBINARY | The SQL VARBINARY type. |
| VARCHAR | The SQL VARCHAR type. |

   class sqlalchemy.types.ARRAY

*inherits from* `sqlalchemy.sql.expression.SchemaEventTarget`, [sqlalchemy.types.Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable), [sqlalchemy.types.Concatenable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Concatenable), [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Represent a SQL Array type.

Note

This type serves as the basis for all ARRAY operations.
However, currently **only the PostgreSQL backend has support for SQL
arrays in SQLAlchemy**. It is recommended to use the PostgreSQL-specific
[sqlalchemy.dialects.postgresql.ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) type directly when using
ARRAY types with PostgreSQL, as it provides additional operators
specific to that backend.

[ARRAY](#sqlalchemy.types.ARRAY) is part of the Core in support of various SQL
standard functions such as [array_agg](https://docs.sqlalchemy.org/en/20/core/functions.html#sqlalchemy.sql.functions.array_agg)
which explicitly involve
arrays; however, with the exception of the PostgreSQL backend and possibly
some third-party dialects, no other SQLAlchemy built-in dialect has support
for this type.

An [ARRAY](#sqlalchemy.types.ARRAY) type is constructed given the “type”
of element:

```
mytable = Table("mytable", metadata, Column("data", ARRAY(Integer)))
```

The above type represents an N-dimensional array,
meaning a supporting backend such as PostgreSQL will interpret values
with any number of dimensions automatically.   To produce an INSERT
construct that passes in a 1-dimensional array of integers:

```
connection.execute(mytable.insert(), {"data": [1, 2, 3]})
```

The [ARRAY](#sqlalchemy.types.ARRAY) type can be constructed given a fixed number
of dimensions:

```
mytable = Table(
    "mytable", metadata, Column("data", ARRAY(Integer, dimensions=2))
)
```

Sending a number of dimensions is optional, but recommended if the
datatype is to represent arrays of more than one dimension.  This number
is used:

- When emitting the type declaration itself to the database, e.g.
  `INTEGER[][]`
- When translating Python values to database values, and vice versa, e.g.
  an ARRAY of [Unicode](#sqlalchemy.types.Unicode) objects uses this number to efficiently
  access the string values inside of array structures without resorting
  to per-row type inspection
- When used with the Python `getitem` accessor, the number of dimensions
  serves to define the kind of type that the `[]` operator should
  return, e.g. for an ARRAY of INTEGER with two dimensions:
  ```
  >>> expr = table.c.column[5]  # returns ARRAY(Integer, dimensions=1)
  >>> expr = expr[6]  # returns Integer
  ```

For 1-dimensional arrays, an [ARRAY](#sqlalchemy.types.ARRAY) instance with no
dimension parameter will generally assume single-dimensional behaviors.

SQL expressions of type [ARRAY](#sqlalchemy.types.ARRAY) have support for “index” and
“slice” behavior.  The `[]` operator produces expression
constructs which will produce the appropriate SQL, both for
SELECT statements:

```
select(mytable.c.data[5], mytable.c.data[2:7])
```

as well as UPDATE statements when the [Update.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update.values)
method is used:

```
mytable.update().values(
    {mytable.c.data[5]: 7, mytable.c.data[2:7]: [1, 2, 3]}
)
```

Indexed access is one-based by default;
for zero-based index conversion, set [ARRAY.zero_indexes](#sqlalchemy.types.ARRAY.params.zero_indexes).

The [ARRAY](#sqlalchemy.types.ARRAY) type also provides for the operators
[Comparator.any()](#sqlalchemy.types.ARRAY.Comparator.any) and
[Comparator.all()](#sqlalchemy.types.ARRAY.Comparator.all). The PostgreSQL-specific version of
[ARRAY](#sqlalchemy.types.ARRAY) also provides additional operators.

**Detecting Changes in ARRAY columns when using the ORM**

The [ARRAY](#sqlalchemy.types.ARRAY) type, when used with the SQLAlchemy ORM,
does not detect in-place mutations to the array. In order to detect
these, the [sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable) extension must be used, using
the [MutableList](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableList) class:

```
from sqlalchemy import ARRAY
from sqlalchemy.ext.mutable import MutableList

class SomeOrmClass(Base):
    # ...

    data = Column(MutableList.as_mutable(ARRAY(Integer)))
```

This extension will allow “in-place” changes such to the array
such as `.append()` to produce events which will be detected by the
unit of work.  Note that changes to elements **inside** the array,
including subarrays that are mutated in place, are **not** detected.

Alternatively, assigning a new array value to an ORM element that
replaces the old one will always trigger a change event.

See also

[sqlalchemy.dialects.postgresql.ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY)

| Member Name | Description |
| --- | --- |
| __init__() | Construct anARRAY. |
| contains() | ARRAY.contains()not implemented for the base ARRAY type.
Use the dialect-specific ARRAY type. |
| any() | ReturnotheroperatorANY(array)clause. |
| all() | ReturnotheroperatorALL(array)clause. |

   method [sqlalchemy.types.ARRAY.](#sqlalchemy.types.ARRAY)__init__(*item_type:_TypeEngineArgument[_T]*, *as_tuple:bool=False*, *dimensions:int|None=None*, *zero_indexes:bool=False*)

Construct an [ARRAY](#sqlalchemy.types.ARRAY).

E.g.:

```
Column("myarray", ARRAY(Integer))
```

Arguments are:

  Parameters:

- **item_type** – The data type of items of this array. Note that
  dimensionality is irrelevant here, so multi-dimensional arrays like
  `INTEGER[][]`, are constructed as `ARRAY(Integer)`, not as
  `ARRAY(ARRAY(Integer))` or such.
- **as_tuple=False** – Specify whether return results
  should be converted to tuples from lists.  This parameter is
  not generally needed as a Python list corresponds well
  to a SQL array.
- **dimensions** – if non-None, the ARRAY will assume a fixed
  number of dimensions.   This impacts how the array is declared
  on the database, how it goes about interpreting Python and
  result values, as well as how expression behavior in conjunction
  with the “getitem” operator works.  See the description at
  [ARRAY](#sqlalchemy.types.ARRAY) for additional detail.
- **zero_indexes=False** – when True, index values will be converted
  between Python zero-based and SQL one-based indexes, e.g.
  a value of one will be added to all index values before passing
  to the database.

      class Comparator

*inherits from* `sqlalchemy.types.Comparator`, `sqlalchemy.types.Comparator`

Define comparison operations for [ARRAY](#sqlalchemy.types.ARRAY).

More operators are available on the dialect-specific form
of this type.  See [Comparator](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY.Comparator).

   method [sqlalchemy.types.ARRAY.Comparator.](#sqlalchemy.types.ARRAY.Comparator)contains(**arg:Any*, ***kw:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

`ARRAY.contains()` not implemented for the base ARRAY type.
Use the dialect-specific ARRAY type.

See also

[ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY) - PostgreSQL specific version.

     method [sqlalchemy.types.ARRAY.Comparator.](#sqlalchemy.types.ARRAY.Comparator)any(*other:Any*, *operator:OperatorType|None=None*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Return `other operator ANY (array)` clause.

Legacy Feature

This method is an [ARRAY](#sqlalchemy.types.ARRAY) - specific
construct that is now superseded by the [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_)
function, which features a different calling style. The
[any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) function is also mirrored at the method level
via the [ColumnOperators.any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.any_) method.

Usage of array-specific [Comparator.any()](#sqlalchemy.types.ARRAY.Comparator.any)
is as follows:

```
from sqlalchemy.sql import operators

conn.execute(
    select(table.c.data).where(table.c.data.any(7, operator=operators.lt))
)
```

   Parameters:

- **other** – expression to be compared
- **operator** – an operator object from the
  `sqlalchemy.sql.operators`
  package, defaults to `eq()`.

See also

[any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_)

[Comparator.all()](#sqlalchemy.types.ARRAY.Comparator.all)

     method [sqlalchemy.types.ARRAY.Comparator.](#sqlalchemy.types.ARRAY.Comparator)all(*other:Any*, *operator:OperatorType|None=None*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Return `other operator ALL (array)` clause.

Legacy Feature

This method is an [ARRAY](#sqlalchemy.types.ARRAY) - specific
construct that is now superseded by the [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_)
function, which features a different calling style. The
[all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) function is also mirrored at the method level
via the [ColumnOperators.all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.all_) method.

Usage of array-specific [Comparator.all()](#sqlalchemy.types.ARRAY.Comparator.all)
is as follows:

```
from sqlalchemy.sql import operators

conn.execute(
    select(table.c.data).where(table.c.data.all(7, operator=operators.lt))
)
```

   Parameters:

- **other** – expression to be compared
- **operator** – an operator object from the
  `sqlalchemy.sql.operators`
  package, defaults to `eq()`.

See also

[all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_)

[Comparator.any()](#sqlalchemy.types.ARRAY.Comparator.any)

       class sqlalchemy.types.BIGINT

*inherits from* [sqlalchemy.types.BigInteger](#sqlalchemy.types.BigInteger)

The SQL BIGINT type.

See also

[BigInteger](#sqlalchemy.types.BigInteger) - documentation for the base type.

     class sqlalchemy.types.BINARY

*inherits from* `sqlalchemy.types._Binary`

The SQL BINARY type.

    class sqlalchemy.types.BLOB

*inherits from* [sqlalchemy.types.LargeBinary](#sqlalchemy.types.LargeBinary)

The SQL BLOB type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a LargeBinary type. |

   method [sqlalchemy.types.BLOB.](#sqlalchemy.types.BLOB)__init__(*length:int|None=None*)

*inherited from the* `sqlalchemy.types.LargeBinary.__init__` *method of* [LargeBinary](#sqlalchemy.types.LargeBinary)

Construct a LargeBinary type.

  Parameters:

**length** – optional, a length for the column for use in
DDL statements, for those binary types that accept a length,
such as the MySQL BLOB type.

       class sqlalchemy.types.BOOLEAN

*inherits from* [sqlalchemy.types.Boolean](#sqlalchemy.types.Boolean)

The SQL BOOLEAN type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Boolean. |

   method [sqlalchemy.types.BOOLEAN.](#sqlalchemy.types.BOOLEAN)__init__(*create_constraint:bool=False*, *name:str|None=None*, *_create_events:bool=True*, *_adapted_from:SchemaType|None=None*)

*inherited from the* `sqlalchemy.types.Boolean.__init__` *method of* [Boolean](#sqlalchemy.types.Boolean)

Construct a Boolean.

  Parameters:

- **create_constraint** –
  defaults to False.  If the boolean
  is generated as an int/smallint, also create a CHECK constraint
  on the table that ensures 1 or 0 as a value.
  Note
  it is strongly recommended that the CHECK constraint
  have an explicit name in order to support schema-management
  concerns.  This can be established either by setting the
  [Boolean.name](#sqlalchemy.types.Boolean.params.name) parameter or by setting up an
  appropriate naming convention; see
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions) for background.
  Changed in version 1.4: - this flag now defaults to False, meaning
  no CHECK constraint is generated for a non-native enumerated
  type.
- **name** – if a CHECK constraint is generated, specify
  the name of the constraint.

       class sqlalchemy.types.CHAR

*inherits from* [sqlalchemy.types.String](#sqlalchemy.types.String)

The SQL CHAR type.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.CHAR.](#sqlalchemy.types.CHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.types.CLOB

*inherits from* [sqlalchemy.types.Text](#sqlalchemy.types.Text)

The CLOB type.

This type is found in Oracle Database and Informix.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.CLOB.](#sqlalchemy.types.CLOB)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.types.DATE

*inherits from* [sqlalchemy.types.Date](#sqlalchemy.types.Date)

The SQL DATE type.

    class sqlalchemy.types.DATETIME

*inherits from* [sqlalchemy.types.DateTime](#sqlalchemy.types.DateTime)

The SQL DATETIME type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newDateTime. |

   method [sqlalchemy.types.DATETIME.](#sqlalchemy.types.DATETIME)__init__(*timezone:bool=False*)

*inherited from the* `sqlalchemy.types.DateTime.__init__` *method of* [DateTime](#sqlalchemy.types.DateTime)

Construct a new [DateTime](#sqlalchemy.types.DateTime).

  Parameters:

**timezone** – boolean.  Indicates that the datetime type should
enable timezone support, if available on the
**base date/time-holding type only**.   It is recommended
to make use of the [TIMESTAMP](#sqlalchemy.types.TIMESTAMP) datatype directly when
using this flag, as some databases include separate generic
date/time-holding types distinct from the timezone-capable
TIMESTAMP datatype, such as Oracle Database.

       class sqlalchemy.types.DECIMAL

*inherits from* [sqlalchemy.types.Numeric](#sqlalchemy.types.Numeric)

The SQL DECIMAL type.

See also

[Numeric](#sqlalchemy.types.Numeric) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Numeric. |

   method [sqlalchemy.types.DECIMAL.](#sqlalchemy.types.DECIMAL)__init__(*precision:int|None=None*, *scale:int|None=None*, *decimal_return_scale:int|None=None*, *asdecimal:bool=True*)

*inherited from the* `sqlalchemy.types.Numeric.__init__` *method of* [Numeric](#sqlalchemy.types.Numeric)

Construct a Numeric.

  Parameters:

- **precision** – the numeric precision for use in DDL `CREATE
  TABLE`.
- **scale** – the numeric scale for use in DDL `CREATE TABLE`.
- **asdecimal** – default True.  Return whether or not
  values should be sent as Python Decimal objects, or
  as floats.   Different DBAPIs send one or the other based on
  datatypes - the Numeric type will ensure that return values
  are one or the other across DBAPIs consistently.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Types which
  do include an explicit “.scale” value, such as the base
  [Numeric](#sqlalchemy.types.Numeric) as well as the MySQL float types, will use the
  value of “.scale” as the default for decimal_return_scale, if not
  otherwise specified.

When using the `Numeric` type, care should be taken to ensure
that the asdecimal setting is appropriate for the DBAPI in use -
when Numeric applies a conversion from Decimal->float or float->
Decimal, this conversion incurs an additional performance overhead
for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have
better accuracy and higher performance with a setting of `True`,
as the native translation to Decimal reduces the amount of floating-
point issues at play, and the Numeric type itself doesn’t need
to apply any further conversions.  However, another DBAPI which
returns floats natively *will* incur an additional conversion
overhead, and is still subject to floating point data loss - in
which case `asdecimal=False` will at least remove the extra
conversion overhead.

     class sqlalchemy.types.DOUBLE

*inherits from* [sqlalchemy.types.Double](#sqlalchemy.types.Double)

The SQL DOUBLE type.

Added in version 2.0.

See also

[Double](#sqlalchemy.types.Double) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Float. |

   method [sqlalchemy.types.DOUBLE.](#sqlalchemy.types.DOUBLE)__init__(*precision:int|None=None*, *asdecimal:bool=False*, *decimal_return_scale:int|None=None*)

*inherited from the* `sqlalchemy.types.Float.__init__` *method of* [Float](#sqlalchemy.types.Float)

Construct a Float.

  Parameters:

- **precision** –
  the numeric precision for use in DDL `CREATE
  TABLE`. Backends **should** attempt to ensure this precision
  indicates a number of digits for the generic
  [Float](#sqlalchemy.types.Float) datatype.
  Note
  For the Oracle Database backend, the
  [Float.precision](#sqlalchemy.types.Float.params.precision) parameter is not accepted
  when rendering DDL, as Oracle Database does not support float precision
  specified as a number of decimal places. Instead, use the
  Oracle Database-specific [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype and specify the
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) parameter. This is new
  in version 2.0 of SQLAlchemy.
  To create a database agnostic [Float](#sqlalchemy.types.Float) that
  separately specifies binary precision for Oracle Database, use
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) as follows:
  ```
  from sqlalchemy import Column
  from sqlalchemy import Float
  from sqlalchemy.dialects import oracle
  Column(
      "float_data",
      Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
  )
  ```
- **asdecimal** – the same flag as that of [Numeric](#sqlalchemy.types.Numeric), but
  defaults to `False`.   Note that setting this flag to `True`
  results in floating point conversion.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Note that the
  MySQL float types, which do include “scale”, will use “scale”
  as the default for decimal_return_scale, if not otherwise specified.

       class sqlalchemy.types.DOUBLE_PRECISION

*inherits from* [sqlalchemy.types.Double](#sqlalchemy.types.Double)

The SQL DOUBLE PRECISION type.

Added in version 2.0.

See also

[Double](#sqlalchemy.types.Double) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Float. |

   method [sqlalchemy.types.DOUBLE_PRECISION.](#sqlalchemy.types.DOUBLE_PRECISION)__init__(*precision:int|None=None*, *asdecimal:bool=False*, *decimal_return_scale:int|None=None*)

*inherited from the* `sqlalchemy.types.Float.__init__` *method of* [Float](#sqlalchemy.types.Float)

Construct a Float.

  Parameters:

- **precision** –
  the numeric precision for use in DDL `CREATE
  TABLE`. Backends **should** attempt to ensure this precision
  indicates a number of digits for the generic
  [Float](#sqlalchemy.types.Float) datatype.
  Note
  For the Oracle Database backend, the
  [Float.precision](#sqlalchemy.types.Float.params.precision) parameter is not accepted
  when rendering DDL, as Oracle Database does not support float precision
  specified as a number of decimal places. Instead, use the
  Oracle Database-specific [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype and specify the
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) parameter. This is new
  in version 2.0 of SQLAlchemy.
  To create a database agnostic [Float](#sqlalchemy.types.Float) that
  separately specifies binary precision for Oracle Database, use
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) as follows:
  ```
  from sqlalchemy import Column
  from sqlalchemy import Float
  from sqlalchemy.dialects import oracle
  Column(
      "float_data",
      Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
  )
  ```
- **asdecimal** – the same flag as that of [Numeric](#sqlalchemy.types.Numeric), but
  defaults to `False`.   Note that setting this flag to `True`
  results in floating point conversion.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Note that the
  MySQL float types, which do include “scale”, will use “scale”
  as the default for decimal_return_scale, if not otherwise specified.

       class sqlalchemy.types.FLOAT

*inherits from* [sqlalchemy.types.Float](#sqlalchemy.types.Float)

The SQL FLOAT type.

See also

[Float](#sqlalchemy.types.Float) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Float. |

   method [sqlalchemy.types.FLOAT.](#sqlalchemy.types.FLOAT)__init__(*precision:int|None=None*, *asdecimal:bool=False*, *decimal_return_scale:int|None=None*)

*inherited from the* `sqlalchemy.types.Float.__init__` *method of* [Float](#sqlalchemy.types.Float)

Construct a Float.

  Parameters:

- **precision** –
  the numeric precision for use in DDL `CREATE
  TABLE`. Backends **should** attempt to ensure this precision
  indicates a number of digits for the generic
  [Float](#sqlalchemy.types.Float) datatype.
  Note
  For the Oracle Database backend, the
  [Float.precision](#sqlalchemy.types.Float.params.precision) parameter is not accepted
  when rendering DDL, as Oracle Database does not support float precision
  specified as a number of decimal places. Instead, use the
  Oracle Database-specific [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype and specify the
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) parameter. This is new
  in version 2.0 of SQLAlchemy.
  To create a database agnostic [Float](#sqlalchemy.types.Float) that
  separately specifies binary precision for Oracle Database, use
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) as follows:
  ```
  from sqlalchemy import Column
  from sqlalchemy import Float
  from sqlalchemy.dialects import oracle
  Column(
      "float_data",
      Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
  )
  ```
- **asdecimal** – the same flag as that of [Numeric](#sqlalchemy.types.Numeric), but
  defaults to `False`.   Note that setting this flag to `True`
  results in floating point conversion.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Note that the
  MySQL float types, which do include “scale”, will use “scale”
  as the default for decimal_return_scale, if not otherwise specified.

       attribute [sqlalchemy.types..](#sqlalchemy.types.)sqlalchemy.types.INT

alias of [INTEGER](#sqlalchemy.types.INTEGER)

    class sqlalchemy.types.JSON

*inherits from* [sqlalchemy.types.Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable), [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Represent a SQL JSON type.

Note

[JSON](#sqlalchemy.types.JSON)
is provided as a facade for vendor-specific
JSON types.  Since it supports JSON SQL operations, it only
works on backends that have an actual JSON type, currently:

- PostgreSQL - see [sqlalchemy.dialects.postgresql.JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and
  [sqlalchemy.dialects.postgresql.JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) for backend-specific
  notes
- MySQL - see
  [sqlalchemy.dialects.mysql.JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON) for backend-specific notes
- SQLite as of version 3.9 - see
  [sqlalchemy.dialects.sqlite.JSON](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.JSON) for backend-specific notes
- Microsoft SQL Server 2016 and later - see
  [sqlalchemy.dialects.mssql.JSON](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.JSON) for backend-specific notes

[JSON](#sqlalchemy.types.JSON) is part of the Core in support of the growing
popularity of native JSON datatypes.

The [JSON](#sqlalchemy.types.JSON) type stores arbitrary JSON format data, e.g.:

```
data_table = Table(
    "data_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", JSON),
)

with engine.connect() as conn:
    conn.execute(
        data_table.insert(), {"data": {"key1": "value1", "key2": "value2"}}
    )
```

**JSON-Specific Expression Operators**

The [JSON](#sqlalchemy.types.JSON)
datatype provides these additional SQL operations:

- Keyed index operations:
  ```
  data_table.c.data["some key"]
  ```
- Integer index operations:
  ```
  data_table.c.data[3]
  ```
- Path index operations:
  ```
  data_table.c.data[("key_1", "key_2", 5, ..., "key_n")]
  ```
- Data casters for specific JSON element types, subsequent to an index
  or path operation being invoked:
  ```
  data_table.c.data["some key"].as_integer()
  ```
  Added in version 1.3.11.

Additional operations may be available from the dialect-specific versions
of [JSON](#sqlalchemy.types.JSON), such as
[sqlalchemy.dialects.postgresql.JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and
[sqlalchemy.dialects.postgresql.JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) which both offer additional
PostgreSQL-specific operations.

**Casting JSON Elements to Other Types**

Index operations, i.e. those invoked by calling upon the expression using
the Python bracket operator as in `some_column['some key']`, return an
expression object whose type defaults to [JSON](#sqlalchemy.types.JSON) by default,
so that
further JSON-oriented instructions may be called upon the result type.
However, it is likely more common that an index operation is expected
to return a specific scalar element, such as a string or integer.  In
order to provide access to these elements in a backend-agnostic way,
a series of data casters are provided:

- [Comparator.as_string()](#sqlalchemy.types.JSON.Comparator.as_string) - return the element as a string
- [Comparator.as_boolean()](#sqlalchemy.types.JSON.Comparator.as_boolean) - return the element as a boolean
- [Comparator.as_float()](#sqlalchemy.types.JSON.Comparator.as_float) - return the element as a float
- [Comparator.as_integer()](#sqlalchemy.types.JSON.Comparator.as_integer) - return the element as an integer

These data casters are implemented by supporting dialects in order to
assure that comparisons to the above types will work as expected, such as:

```
# integer comparison
data_table.c.data["some_integer_key"].as_integer() == 5

# boolean comparison
data_table.c.data["some_boolean"].as_boolean() == True
```

Added in version 1.3.11: Added type-specific casters for the basic JSON
data element types.

Note

The data caster functions are new in version 1.3.11, and supersede
the previous documented approaches of using CAST; for reference,
this looked like:

```
from sqlalchemy import cast, type_coerce
from sqlalchemy import String, JSON

cast(data_table.c.data["some_key"], String) == type_coerce(55, JSON)
```

The above case now works directly as:

```
data_table.c.data["some_key"].as_integer() == 5
```

For details on the previous comparison approach within the 1.3.x
series, see the documentation for SQLAlchemy 1.2 or the included HTML
files in the doc/ directory of the version’s distribution.

**Detecting Changes in JSON columns when using the ORM**

The [JSON](#sqlalchemy.types.JSON) type, when used with the SQLAlchemy ORM, does not
detect in-place mutations to the structure.  In order to detect these, the
[sqlalchemy.ext.mutable](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#module-sqlalchemy.ext.mutable) extension must be used, most typically
using the [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) class.  This extension will
allow “in-place” changes to the datastructure to produce events which
will be detected by the unit of work.  See the example at [HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE)
for a simple example involving a dictionary.

Alternatively, assigning a JSON structure to an ORM element that
replaces the old one will always trigger a change event.

**Support for JSON null vs. SQL NULL**

When working with NULL values, the [JSON](#sqlalchemy.types.JSON) type recommends the
use of two specific constants in order to differentiate between a column
that evaluates to SQL NULL, e.g. no value, vs. the JSON-encoded string of
`"null"`. To insert or select against a value that is SQL NULL, use the
constant [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null). This symbol may be passed as a parameter value
specifically when using the [JSON](#sqlalchemy.types.JSON) datatype, which contains
special logic that interprets this symbol to mean that the column value
should be SQL NULL as opposed to JSON `"null"`:

```
from sqlalchemy import null

conn.execute(table.insert(), {"json_value": null()})
```

To insert or select against a value that is JSON `"null"`, use the
constant [JSON.NULL](#sqlalchemy.types.JSON.NULL):

```
conn.execute(table.insert(), {"json_value": JSON.NULL})
```

The [JSON](#sqlalchemy.types.JSON) type supports a flag
[JSON.none_as_null](#sqlalchemy.types.JSON.params.none_as_null) which when set to True will result
in the Python constant `None` evaluating to the value of SQL
NULL, and when set to False results in the Python constant
`None` evaluating to the value of JSON `"null"`.    The Python
value `None` may be used in conjunction with either
[JSON.NULL](#sqlalchemy.types.JSON.NULL) and [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) in order to indicate NULL
values, but care must be taken as to the value of the
[JSON.none_as_null](#sqlalchemy.types.JSON.params.none_as_null) in these cases.

**Customizing the JSON Serializer**

The JSON serializer and deserializer used by [JSON](#sqlalchemy.types.JSON)
defaults to
Python’s `json.dumps` and `json.loads` functions; in the case of the
psycopg2 dialect, psycopg2 may be using its own custom loader function.

In order to affect the serializer / deserializer, they are currently
configurable at the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) level via the
[create_engine.json_serializer](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.json_serializer) and
[create_engine.json_deserializer](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.json_deserializer) parameters.  For example,
to turn off `ensure_ascii`:

```
engine = create_engine(
    "sqlite://",
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)
```

Changed in version 1.3.7: SQLite dialect’s `json_serializer` and `json_deserializer`
parameters renamed from `_json_serializer` and
`_json_deserializer`.

See also

[sqlalchemy.dialects.postgresql.JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON)

[sqlalchemy.dialects.postgresql.JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB)

[sqlalchemy.dialects.mysql.JSON](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.JSON)

[sqlalchemy.dialects.sqlite.JSON](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlalchemy.dialects.sqlite.JSON)

| Member Name | Description |
| --- | --- |
| as_boolean() | Consider an indexed value as boolean. |
| as_float() | Consider an indexed value as float. |
| as_integer() | Consider an indexed value as integer. |
| as_json() | Consider an indexed value as JSON. |
| as_numeric() | Consider an indexed value as numeric/decimal. |
| as_string() | Consider an indexed value as string. |
| bind_processor() | Return a conversion function for processing bind values. |
| literal_processor() | Return a conversion function for processing literal values that are
to be rendered directly without using binds. |
| NULL | Describe the json value of NULL. |
| __init__() | Construct aJSONtype. |
| bind_processor() | Return a conversion function for processing bind values. |
| comparator_factory | alias ofComparator |
| hashable | Flag, if False, means values from this type aren’t hashable. |
| result_processor() | Return a conversion function for processing result row values. |

   class Comparator

*inherits from* `sqlalchemy.types.Comparator`, `sqlalchemy.types.Comparator`

Define comparison operations for [JSON](#sqlalchemy.types.JSON).

   method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_boolean()

Consider an indexed value as boolean.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_boolean()).where(
    mytable.c.json_column["some_data"].as_boolean() == True
)
```

Added in version 1.3.11.

     method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_float()

Consider an indexed value as float.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_float()).where(
    mytable.c.json_column["some_data"].as_float() == 29.75
)
```

Added in version 1.3.11.

     method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_integer()

Consider an indexed value as integer.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_integer()).where(
    mytable.c.json_column["some_data"].as_integer() == 5
)
```

Added in version 1.3.11.

     method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_json()

Consider an indexed value as JSON.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_json())
```

This is typically the default behavior of indexed elements in any
case.

Note that comparison of full JSON structures may not be
supported by all backends.

Added in version 1.3.11.

     method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_numeric(*precision*, *scale*, *asdecimal=True*)

Consider an indexed value as numeric/decimal.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_numeric(10, 6)).where(
    mytable.c.json_column["some_data"].as_numeric(10, 6) == 29.75
)
```

Added in version 1.4.0b2.

     method [sqlalchemy.types.JSON.Comparator.](#sqlalchemy.types.JSON.Comparator)as_string()

Consider an indexed value as string.

This is similar to using [type_coerce](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce), and will
usually not apply a `CAST()`.

e.g.:

```
stmt = select(mytable.c.json_column["some_data"].as_string()).where(
    mytable.c.json_column["some_data"].as_string() == "some string"
)
```

Added in version 1.3.11.

      class JSONElementType

*inherits from* [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Common function for index / path elements in a JSON expression.

   method [sqlalchemy.types.JSON.JSONElementType.](#sqlalchemy.types.JSON.JSONElementType)bind_processor(*dialect:Dialect*) → _BindProcessorType[Any]

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.JSON.JSONElementType.](#sqlalchemy.types.JSON.JSONElementType)literal_processor(*dialect:Dialect*) → _LiteralProcessorType[Any]

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
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_literal_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_literal_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

       class JSONIndexType

*inherits from* `sqlalchemy.types.JSONElementType`

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values
for special syntaxes.

    class JSONIntIndexType

*inherits from* `sqlalchemy.types.JSONIndexType`

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values
for special syntaxes.

    class JSONPathType

*inherits from* `sqlalchemy.types.JSONElementType`

Placeholder type for JSON path operations.

This allows execution-time processing of a path-based
index value into a specific SQL syntax.

    class JSONStrIndexType

*inherits from* `sqlalchemy.types.JSONIndexType`

Placeholder for the datatype of a JSON index value.

This allows execution-time processing of JSON index values
for special syntaxes.

    attribute [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)NULL = symbol('JSON_NULL')

Describe the json value of NULL.

This value is used to force the JSON value of `"null"` to be
used as the value.   A value of Python `None` will be recognized
either as SQL NULL or JSON `"null"`, based on the setting
of the [JSON.none_as_null](#sqlalchemy.types.JSON.params.none_as_null) flag; the
[JSON.NULL](#sqlalchemy.types.JSON.NULL)
constant can be used to always resolve to JSON `"null"` regardless
of this setting.  This is in contrast to the [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null)
construct,
which always resolves to SQL NULL.  E.g.:

```
from sqlalchemy import null
from sqlalchemy.dialects.postgresql import JSON

# will *always* insert SQL NULL
obj1 = MyObject(json_value=null())

# will *always* insert JSON string "null"
obj2 = MyObject(json_value=JSON.NULL)

session.add_all([obj1, obj2])
session.commit()
```

In order to set JSON NULL as a default value for a column, the most
transparent method is to use [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text):

```
Table(
    "my_table", metadata, Column("json_data", JSON, default=text("'null'"))
)
```

While it is possible to use [JSON.NULL](#sqlalchemy.types.JSON.NULL) in this context, the
[JSON.NULL](#sqlalchemy.types.JSON.NULL) value will be returned as the value of the
column,
which in the context of the ORM or other repurposing of the default
value, may not be desirable.  Using a SQL expression means the value
will be re-fetched from the database within the context of retrieving
generated defaults.

    method [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)__init__(*none_as_null:bool=False*)

Construct a [JSON](#sqlalchemy.types.JSON) type.

  Parameters:

**none_as_null=False** –

if True, persist the value `None` as a
SQL NULL value, not the JSON encoding of `null`. Note that when this
flag is False, the [null()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) construct can still be used to
persist a NULL value, which may be passed directly as a parameter
value that is specially interpreted by the [JSON](#sqlalchemy.types.JSON) type
as SQL NULL:

```
from sqlalchemy import null

conn.execute(table.insert(), {"data": null()})
```

Note

[JSON.none_as_null](#sqlalchemy.types.JSON.params.none_as_null) does **not** apply to the
values passed to [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default); a value of `None`
passed for these parameters means “no default present”.

Additionally, when used in SQL comparison expressions, the
Python value `None` continues to refer to SQL null, and not
JSON NULL.  The [JSON.none_as_null](#sqlalchemy.types.JSON.params.none_as_null) flag refers
explicitly to the **persistence** of the value within an
INSERT or UPDATE statement.   The [JSON.NULL](#sqlalchemy.types.JSON.NULL)
value should be used for SQL expressions that wish to compare to
JSON null.

See also

[JSON.NULL](#sqlalchemy.types.JSON.NULL)

       method [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)bind_processor(*dialect*)

Return a conversion function for processing bind values.

Returns a callable which will receive a bind parameter value
as the sole positional argument and will return a value to
send to the DB-API.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_bind_param()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

**dialect** – Dialect instance in use.

      attribute [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)comparator_factory

alias of [Comparator](#sqlalchemy.types.JSON.Comparator)

    attribute [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)hashable = False

Flag, if False, means values from this type aren’t hashable.

Used by the ORM when uniquing result lists.

    property python_type

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

    method [sqlalchemy.types.JSON.](#sqlalchemy.types.JSON)result_processor(*dialect*, *coltype*)

Return a conversion function for processing result row values.

Returns a callable which will receive a result row column
value as the sole positional argument and will return a value
to return to the user.

If processing is not necessary, the method should return `None`.

Tip

This method is only called relative to a **dialect specific type
object**, which is often **private to a dialect in use** and is not
the same type object as the public facing one, which means it’s not
feasible to subclass a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class in order to
provide an alternate [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
method, unless subclassing the [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
class explicitly.

To provide alternate behavior for
[TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor), implement a
[TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator) class and provide an implementation
of [TypeDecorator.process_result_value()](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_result_value).

See also

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator)

    Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – DBAPI coltype argument received in cursor.description.

      property should_evaluate_none

Alias of `JSON.none_as_null`

     class sqlalchemy.types.INTEGER

*inherits from* [sqlalchemy.types.Integer](#sqlalchemy.types.Integer)

The SQL INT or INTEGER type.

See also

[Integer](#sqlalchemy.types.Integer) - documentation for the base type.

     class sqlalchemy.types.NCHAR

*inherits from* [sqlalchemy.types.Unicode](#sqlalchemy.types.Unicode)

The SQL NCHAR type.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.NCHAR.](#sqlalchemy.types.NCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.types.NVARCHAR

*inherits from* [sqlalchemy.types.Unicode](#sqlalchemy.types.Unicode)

The SQL NVARCHAR type.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.NVARCHAR.](#sqlalchemy.types.NVARCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.types.NUMERIC

*inherits from* [sqlalchemy.types.Numeric](#sqlalchemy.types.Numeric)

The SQL NUMERIC type.

See also

[Numeric](#sqlalchemy.types.Numeric) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Numeric. |

   method [sqlalchemy.types.NUMERIC.](#sqlalchemy.types.NUMERIC)__init__(*precision:int|None=None*, *scale:int|None=None*, *decimal_return_scale:int|None=None*, *asdecimal:bool=True*)

*inherited from the* `sqlalchemy.types.Numeric.__init__` *method of* [Numeric](#sqlalchemy.types.Numeric)

Construct a Numeric.

  Parameters:

- **precision** – the numeric precision for use in DDL `CREATE
  TABLE`.
- **scale** – the numeric scale for use in DDL `CREATE TABLE`.
- **asdecimal** – default True.  Return whether or not
  values should be sent as Python Decimal objects, or
  as floats.   Different DBAPIs send one or the other based on
  datatypes - the Numeric type will ensure that return values
  are one or the other across DBAPIs consistently.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Types which
  do include an explicit “.scale” value, such as the base
  [Numeric](#sqlalchemy.types.Numeric) as well as the MySQL float types, will use the
  value of “.scale” as the default for decimal_return_scale, if not
  otherwise specified.

When using the `Numeric` type, care should be taken to ensure
that the asdecimal setting is appropriate for the DBAPI in use -
when Numeric applies a conversion from Decimal->float or float->
Decimal, this conversion incurs an additional performance overhead
for all result columns received.

DBAPIs that return Decimal natively (e.g. psycopg2) will have
better accuracy and higher performance with a setting of `True`,
as the native translation to Decimal reduces the amount of floating-
point issues at play, and the Numeric type itself doesn’t need
to apply any further conversions.  However, another DBAPI which
returns floats natively *will* incur an additional conversion
overhead, and is still subject to floating point data loss - in
which case `asdecimal=False` will at least remove the extra
conversion overhead.

     class sqlalchemy.types.REAL

*inherits from* [sqlalchemy.types.Float](#sqlalchemy.types.Float)

The SQL REAL type.

See also

[Float](#sqlalchemy.types.Float) - documentation for the base type.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a Float. |

   method [sqlalchemy.types.REAL.](#sqlalchemy.types.REAL)__init__(*precision:int|None=None*, *asdecimal:bool=False*, *decimal_return_scale:int|None=None*)

*inherited from the* `sqlalchemy.types.Float.__init__` *method of* [Float](#sqlalchemy.types.Float)

Construct a Float.

  Parameters:

- **precision** –
  the numeric precision for use in DDL `CREATE
  TABLE`. Backends **should** attempt to ensure this precision
  indicates a number of digits for the generic
  [Float](#sqlalchemy.types.Float) datatype.
  Note
  For the Oracle Database backend, the
  [Float.precision](#sqlalchemy.types.Float.params.precision) parameter is not accepted
  when rendering DDL, as Oracle Database does not support float precision
  specified as a number of decimal places. Instead, use the
  Oracle Database-specific [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) datatype and specify the
  [FLOAT.binary_precision](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT.params.binary_precision) parameter. This is new
  in version 2.0 of SQLAlchemy.
  To create a database agnostic [Float](#sqlalchemy.types.Float) that
  separately specifies binary precision for Oracle Database, use
  [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) as follows:
  ```
  from sqlalchemy import Column
  from sqlalchemy import Float
  from sqlalchemy.dialects import oracle
  Column(
      "float_data",
      Float(5).with_variant(oracle.FLOAT(binary_precision=16), "oracle"),
  )
  ```
- **asdecimal** – the same flag as that of [Numeric](#sqlalchemy.types.Numeric), but
  defaults to `False`.   Note that setting this flag to `True`
  results in floating point conversion.
- **decimal_return_scale** – Default scale to use when converting
  from floats to Python decimals.  Floating point values will typically
  be much longer due to decimal inaccuracy, and most floating point
  database types don’t have a notion of “scale”, so by default the
  float type looks for the first ten decimal places when converting.
  Specifying this value will override that length.  Note that the
  MySQL float types, which do include “scale”, will use “scale”
  as the default for decimal_return_scale, if not otherwise specified.

       class sqlalchemy.types.SMALLINT

*inherits from* [sqlalchemy.types.SmallInteger](#sqlalchemy.types.SmallInteger)

The SQL SMALLINT type.

See also

[SmallInteger](#sqlalchemy.types.SmallInteger) - documentation for the base type.

     class sqlalchemy.types.TEXT

*inherits from* [sqlalchemy.types.Text](#sqlalchemy.types.Text)

The SQL TEXT type.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.TEXT.](#sqlalchemy.types.TEXT)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.

       class sqlalchemy.types.TIME

*inherits from* [sqlalchemy.types.Time](#sqlalchemy.types.Time)

The SQL TIME type.

    class sqlalchemy.types.TIMESTAMP

*inherits from* [sqlalchemy.types.DateTime](#sqlalchemy.types.DateTime)

The SQL TIMESTAMP type.

[TIMESTAMP](#sqlalchemy.types.TIMESTAMP) datatypes have support for timezone storage on
some backends, such as PostgreSQL and Oracle Database.  Use the
`TIMESTAMP.timezone` argument in order to enable
“TIMESTAMP WITH TIMEZONE” for these backends.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newTIMESTAMP. |
| get_dbapi_type() | Return the corresponding type object from the underlying DB-API, if
any. |

   method [sqlalchemy.types.TIMESTAMP.](#sqlalchemy.types.TIMESTAMP)__init__(*timezone:bool=False*)

Construct a new [TIMESTAMP](#sqlalchemy.types.TIMESTAMP).

  Parameters:

**timezone** – boolean.  Indicates that the TIMESTAMP type should
enable timezone support, if available on the target database.
On a per-dialect basis is similar to “TIMESTAMP WITH TIMEZONE”.
If the target database does not support timezones, this flag is
ignored.

      method [sqlalchemy.types.TIMESTAMP.](#sqlalchemy.types.TIMESTAMP)get_dbapi_type(*dbapi*)

Return the corresponding type object from the underlying DB-API, if
any.

This can be useful for calling `setinputsizes()`, for example.

     class sqlalchemy.types.UUID

*inherits from* [sqlalchemy.types.Uuid](#sqlalchemy.types.Uuid), `sqlalchemy.types.NativeForEmulated`

Represent the SQL UUID type.

This is the SQL-native form of the [Uuid](#sqlalchemy.types.Uuid) database agnostic
datatype, and is backwards compatible with the previous PostgreSQL-only
version of `UUID`.

The [UUID](#sqlalchemy.types.UUID) datatype only works on databases that have a
SQL datatype named `UUID`. It will not function for backends which don’t
have this exact-named type, including SQL Server. For backend-agnostic UUID
values with native support, including for SQL Server’s `UNIQUEIDENTIFIER`
datatype, use the [Uuid](#sqlalchemy.types.Uuid) datatype.

Added in version 2.0.

See also

[Uuid](#sqlalchemy.types.Uuid)

| Member Name | Description |
| --- | --- |
| __init__() | Construct aUUIDtype. |

   method [sqlalchemy.types.UUID.](#sqlalchemy.types.UUID)__init__(*as_uuid:bool=True*)

Construct a [UUID](#sqlalchemy.types.UUID) type.

  Parameters:

**as_uuid=True** –

if True, values will be interpreted
as Python uuid objects, converting to/from string via the
DBAPI.

       class sqlalchemy.types.VARBINARY

*inherits from* `sqlalchemy.types._Binary`

The SQL VARBINARY type.

    class sqlalchemy.types.VARCHAR

*inherits from* [sqlalchemy.types.String](#sqlalchemy.types.String)

The SQL VARCHAR type.

| Member Name | Description |
| --- | --- |
| __init__() | Create a string-holding type. |

   method [sqlalchemy.types.VARCHAR.](#sqlalchemy.types.VARCHAR)__init__(*length:int|None=None*, *collation:str|None=None*)

*inherited from the* `sqlalchemy.types.String.__init__` *method of* [String](#sqlalchemy.types.String)

Create a string-holding type.

  Parameters:

- **length** – optional, a length for the column for use in
  DDL and CAST expressions.  May be safely omitted if no `CREATE
  TABLE` will be issued.  Certain databases may require a
  `length` for use in DDL, and will raise an exception when
  the `CREATE TABLE` DDL is issued if a `VARCHAR`
  with no length is included.  Whether the value is
  interpreted as bytes or characters is database specific.
- **collation** –
  Optional, a column-level collation for
  use in DDL and CAST expressions.  Renders using the
  COLLATE keyword supported by SQLite, MySQL, and PostgreSQL.
  E.g.:
  ```
  >>> from sqlalchemy import cast, select, String
  >>> print(select(cast("some string", String(collation="utf8"))))
  SELECT CAST(:param_1 AS VARCHAR COLLATE utf8) AS anon_1
  ```
  Note
  In most cases, the [Unicode](#sqlalchemy.types.Unicode) or [UnicodeText](#sqlalchemy.types.UnicodeText)
  datatypes should be used for a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that expects
  to store non-ascii data. These datatypes will ensure that the
  correct types are used on the database.
