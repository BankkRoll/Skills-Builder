# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Custom Types

A variety of methods exist to redefine the behavior of existing types
as well as to provide new ones.

## Overriding Type Compilation

A frequent need is to force the “string” version of a type, that is
the one rendered in a CREATE TABLE statement or other SQL function
like CAST, to be changed.   For example, an application may want
to force the rendering of `BINARY` for all platforms
except for one, in which it wants `BLOB` to be rendered.  Usage
of an existing generic type, in this case [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary), is
preferred for most use cases.  But to control
types more accurately, a compilation directive that is per-dialect
can be associated with any type:

```
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import BINARY

@compiles(BINARY, "sqlite")
def compile_binary_sqlite(type_, compiler, **kw):
    return "BLOB"
```

The above code allows the usage of [BINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BINARY), which
will produce the string `BINARY` against all backends except SQLite,
in which case it will produce `BLOB`.

See the section [Changing Compilation of Types](https://docs.sqlalchemy.org/en/20/core/compiler.html#type-compilation-extension), a subsection of
[Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html), for additional examples.

## Augmenting Existing Types

The [TypeDecorator](#sqlalchemy.types.TypeDecorator) allows the creation of custom types which
add bind-parameter and result-processing behavior to an existing
type object.  It is used when additional in-Python [marshalling](https://docs.sqlalchemy.org/en/20/glossary.html#term-marshalling) of data
to and/or from the database is required.

Note

The bind- and result-processing of [TypeDecorator](#sqlalchemy.types.TypeDecorator)
is **in addition** to the processing already performed by the hosted
type, which is customized by SQLAlchemy on a per-DBAPI basis to perform
processing specific to that DBAPI.  While it is possible to replace this
handling for a given type through direct subclassing, it is never needed in
practice and SQLAlchemy no longer supports this as a public use case.

ORM Tip

The [TypeDecorator](#sqlalchemy.types.TypeDecorator) can be used to provide a consistent means of
converting some type of value as it is passed into and out of the database.
When using the ORM, a similar technique exists for converting user data
from arbitrary formats which is to use the [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) decorator.
This technique may be more appropriate when data coming into an ORM model
needs to be normalized in some way that is specific to the business case
and isn’t as generic as a datatype.

| Object Name | Description |
| --- | --- |
| TypeDecorator | Allows the creation of types which add additional functionality
to an existing type. |

   class sqlalchemy.types.TypeDecorator

*inherits from* `sqlalchemy.sql.expression.SchemaEventTarget`, [sqlalchemy.types.ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType), [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)

Allows the creation of types which add additional functionality
to an existing type.

This method is preferred to direct subclassing of SQLAlchemy’s
built-in types as it ensures that all required functionality of
the underlying type is kept in place.

Typical usage:

```
import sqlalchemy.types as types

class MyType(types.TypeDecorator):
    """Prefixes Unicode values with "PREFIX:" on the way in and
    strips it off on the way out.
    """

    impl = types.Unicode

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return "PREFIX:" + value

    def process_result_value(self, value, dialect):
        return value[7:]

    def copy(self, **kw):
        return MyType(self.impl.length)
```

The class-level `impl` attribute is required, and can reference any
[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class.  Alternatively, the [load_dialect_impl()](#sqlalchemy.types.TypeDecorator.load_dialect_impl)
method can be used to provide different type classes based on the dialect
given; in this case, the `impl` variable can reference
`TypeEngine` as a placeholder.

The [TypeDecorator.cache_ok](#sqlalchemy.types.TypeDecorator.cache_ok) class-level flag indicates if this
custom [TypeDecorator](#sqlalchemy.types.TypeDecorator) is safe to be used as part of a cache key.
This flag defaults to `None` which will initially generate a warning
when the SQL compiler attempts to generate a cache key for a statement
that uses this type.  If the [TypeDecorator](#sqlalchemy.types.TypeDecorator) is not guaranteed
to produce the same bind/result behavior and SQL generation
every time, this flag should be set to `False`; otherwise if the
class produces the same behavior each time, it may be set to `True`.
See [TypeDecorator.cache_ok](#sqlalchemy.types.TypeDecorator.cache_ok) for further notes on how this works.

Types that receive a Python type that isn’t similar to the ultimate type
used may want to define the [TypeDecorator.coerce_compared_value()](#sqlalchemy.types.TypeDecorator.coerce_compared_value)
method. This is used to give the expression system a hint when coercing
Python objects into bind parameters within expressions. Consider this
expression:

```
mytable.c.somecol + datetime.date(2009, 5, 15)
```

Above, if “somecol” is an `Integer` variant, it makes sense that
we’re doing date arithmetic, where above is usually interpreted
by databases as adding a number of days to the given date.
The expression system does the right thing by not attempting to
coerce the “date()” value into an integer-oriented bind parameter.

However, in the case of `TypeDecorator`, we are usually changing an
incoming Python type to something new - `TypeDecorator` by default will
“coerce” the non-typed side to be the same type as itself. Such as below,
we define an “epoch” type that stores a date value as an integer:

```
class MyEpochType(types.TypeDecorator):
    impl = types.Integer

    cache_ok = True

    epoch = datetime.date(1970, 1, 1)

    def process_bind_param(self, value, dialect):
        return (value - self.epoch).days

    def process_result_value(self, value, dialect):
        return self.epoch + timedelta(days=value)
```

Our expression of `somecol + date` with the above type will coerce the
“date” on the right side to also be treated as `MyEpochType`.

This behavior can be overridden via the
[TypeDecorator.coerce_compared_value()](#sqlalchemy.types.TypeDecorator.coerce_compared_value) method, which returns a type
that should be used for the value of the expression. Below we set it such
that an integer value will be treated as an `Integer`, and any other
value is assumed to be a date and will be treated as a `MyEpochType`:

```
def coerce_compared_value(self, op, value):
    if isinstance(value, int):
        return Integer()
    else:
        return self
```

Warning

Note that the **behavior of coerce_compared_value is not inherited
by default from that of the base type**.
If the [TypeDecorator](#sqlalchemy.types.TypeDecorator) is augmenting a
type that requires special logic for certain types of operators,
this method **must** be overridden.  A key example is when decorating
the [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON) and [JSONB](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB) types;
the default rules of [TypeEngine.coerce_compared_value()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value) should
be used in order to deal with operators like index operations:

```
from sqlalchemy import JSON
from sqlalchemy import TypeDecorator

class MyJsonType(TypeDecorator):
    impl = JSON

    cache_ok = True

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)
```

Without the above step, index operations such as `mycol['foo']`
will cause the index value `'foo'` to be JSON encoded.

Similarly, when working with the [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY) datatype, the
type coercion for index operations (e.g. `mycol[5]`) is also
handled by [TypeDecorator.coerce_compared_value()](#sqlalchemy.types.TypeDecorator.coerce_compared_value), where
again a simple override is sufficient unless special rules are needed
for particular operators:

```
from sqlalchemy import ARRAY
from sqlalchemy import TypeDecorator

class MyArrayType(TypeDecorator):
    impl = ARRAY

    cache_ok = True

    def coerce_compared_value(self, op, value):
        return self.impl.coerce_compared_value(op, value)
```

| Member Name | Description |
| --- | --- |
| cache_ok | Indicate if statements using thisExternalTypeare “safe to
cache”. |
| operate() | Operate on an argument. |
| reverse_operate() | Reverse operate on an argument. |
| __init__() | Construct aTypeDecorator. |
| bind_expression() | Given a bind value (i.e. aBindParameterinstance),
return a SQL expression which will typically wrap the given parameter. |
| bind_processor() | Provide a bound value processing function for the
givenDialect. |
| coerce_compared_value() | Suggest a type for a ‘coerced’ Python value in an expression. |
| coerce_to_is_types | Specify those Python types which should be coerced at the expression
level to “IS <constant>” when compared using==(and same forISNOTin conjunction with!=). |
| column_expression() | Given a SELECT column expression, return a wrapping SQL expression. |
| compare_values() | Given two values, compare them for equality. |
| copy() | Produce a copy of thisTypeDecoratorinstance. |
| get_dbapi_type() | Return the DBAPI type object represented by thisTypeDecorator. |
| literal_processor() | Provide a literal processing function for the givenDialect. |
| load_dialect_impl() | Return aTypeEngineobject corresponding to a dialect. |
| process_bind_param() | Receive a bound parameter value to be converted. |
| process_literal_param() | Receive a literal parameter value to be rendered inline within
a statement. |
| process_result_value() | Receive a result-row column value to be converted. |
| result_processor() | Provide a result value processing function for the givenDialect. |
| type_engine() | Return a dialect-specificTypeEngineinstance
for thisTypeDecorator. |

   attribute [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)cache_ok = None

*inherited from the* [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok) *attribute of* [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType)

Indicate if statements using this [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) are “safe to
cache”.

The default value `None` will emit a warning and then not allow caching
of a statement which includes this type.   Set to `False` to disable
statements using this type from being cached at all without a warning.
When set to `True`, the object’s class and selected elements from its
state will be used as part of the cache key.  For example, using a
[TypeDecorator](#sqlalchemy.types.TypeDecorator):

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
some configurability of caching for [TypeDecorator](#sqlalchemy.types.TypeDecorator) classes.

Added in version 1.4.28: - added the [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) mixin which
generalizes the `cache_ok` flag to both the [TypeDecorator](#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](#sqlalchemy.types.UserDefinedType) classes.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

     class Comparator

*inherits from* `sqlalchemy.types.Comparator`

A [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) that is specific to
[TypeDecorator](#sqlalchemy.types.TypeDecorator).

User-defined [TypeDecorator](#sqlalchemy.types.TypeDecorator) classes should not typically
need to modify this.

   method [sqlalchemy.types.TypeDecorator.Comparator.](#sqlalchemy.types.TypeDecorator.Comparator)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_CT]

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

      method [sqlalchemy.types.TypeDecorator.Comparator.](#sqlalchemy.types.TypeDecorator.Comparator)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_CT]

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.types.TypeDecorator.Comparator.operate).

     method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)__init__(**args:Any*, ***kwargs:Any*)

Construct a [TypeDecorator](#sqlalchemy.types.TypeDecorator).

Arguments sent here are passed to the constructor
of the class assigned to the `impl` class level attribute,
assuming the `impl` is a callable, and the resulting
object is assigned to the `self.impl` instance attribute
(thus overriding the class attribute of the same name).

If the class level `impl` is not a callable (the unusual case),
it will be assigned to the same instance attribute ‘as-is’,
ignoring those arguments passed to the constructor.

Subclasses can override this to customize the generation
of `self.impl` entirely.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)bind_expression(*bindparam:BindParameter[_T]*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_T] | None

Given a bind value (i.e. a [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) instance),
return a SQL expression which will typically wrap the given parameter.

Note

This method is called during the **SQL compilation** phase of a
statement, when rendering a SQL string. It is **not** necessarily
called against specific values, and should not be confused with the
[TypeDecorator.process_bind_param()](#sqlalchemy.types.TypeDecorator.process_bind_param) method, which is
the more typical method that processes the actual value passed to a
particular parameter at statement execution time.

Subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) can override this method
to provide custom bind expression behavior for the type.  This
implementation will **replace** that of the underlying implementation
type.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)bind_processor(*dialect:Dialect*) → _BindProcessorType[_T] | None

Provide a bound value processing function for the
given [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

This is the method that fulfills the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
contract for bound value conversion which normally occurs via
the [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor) method.

Note

User-defined subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should
**not** implement this method, and should instead implement
[TypeDecorator.process_bind_param()](#sqlalchemy.types.TypeDecorator.process_bind_param) so that the “inner”
processing provided by the implementing type is maintained.

   Parameters:

**dialect** – Dialect instance in use.

      method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)coerce_compared_value(*op:OperatorType|None*, *value:Any*) → Any

Suggest a type for a ‘coerced’ Python value in an expression.

By default, returns self.   This method is called by
the expression system when an object using this type is
on the left or right side of an expression against a plain Python
object which does not yet have a SQLAlchemy type assigned:

```
expr = table.c.somecolumn + 35
```

Where above, if `somecolumn` uses this type, this method will
be called with the value `operator.add`
and `35`.  The return value is whatever SQLAlchemy type should
be used for `35` for this particular operation.

    attribute [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)coerce_to_is_types: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[Type[Any]] = (<class 'NoneType'>,)

Specify those Python types which should be coerced at the expression
level to “IS <constant>” when compared using `==` (and same for
`IS NOT` in conjunction with `!=`).

For most SQLAlchemy types, this includes `NoneType`, as well as
`bool`.

[TypeDecorator](#sqlalchemy.types.TypeDecorator) modifies this list to only include `NoneType`,
as typedecorator implementations that deal with boolean types are common.

Custom [TypeDecorator](#sqlalchemy.types.TypeDecorator) classes can override this attribute to
return an empty tuple, in which case no values will be coerced to
constants.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)column_expression(*column:ColumnElement[_T]*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_T] | None

Given a SELECT column expression, return a wrapping SQL expression.

Note

This method is called during the **SQL compilation** phase of a
statement, when rendering a SQL string. It is **not** called
against specific values, and should not be confused with the
[TypeDecorator.process_result_value()](#sqlalchemy.types.TypeDecorator.process_result_value) method, which is
the more typical method that processes the actual value returned
in a result row subsequent to statement execution time.

Subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) can override this method
to provide custom column expression behavior for the type.  This
implementation will **replace** that of the underlying implementation
type.

See the description of [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression)
for a complete description of the method’s use.

    property comparator_factory: _ComparatorFactory[Any]

Base class for custom comparison operations defined at the
type level.  See [TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory).

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)compare_values(*x:Any*, *y:Any*) → bool

Given two values, compare them for equality.

By default this calls upon [TypeEngine.compare_values()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.compare_values)
of the underlying “impl”, which in turn usually
uses the Python equals operator `==`.

This function is used by the ORM to compare
an original-loaded value with an intercepted
“changed” value, to determine if a net change
has occurred.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)copy(***kw:Any*) → Self

Produce a copy of this [TypeDecorator](#sqlalchemy.types.TypeDecorator) instance.

This is a shallow copy and is provided to fulfill part of
the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) contract.  It usually does not
need to be overridden unless the user-defined [TypeDecorator](#sqlalchemy.types.TypeDecorator)
has local state that should be deep-copied.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)get_dbapi_type(*dbapi:DBAPIModule*) → Any | None

Return the DBAPI type object represented by this
[TypeDecorator](#sqlalchemy.types.TypeDecorator).

By default this calls upon [TypeEngine.get_dbapi_type()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.get_dbapi_type) of the
underlying “impl”.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)literal_processor(*dialect:Dialect*) → _LiteralProcessorType[_T] | None

Provide a literal processing function for the given
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

This is the method that fulfills the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
contract for literal value conversion which normally occurs via
the [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor) method.

Note

User-defined subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should
**not** implement this method, and should instead implement
[TypeDecorator.process_literal_param()](#sqlalchemy.types.TypeDecorator.process_literal_param) so that the
“inner” processing provided by the implementing type is maintained.

     method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)load_dialect_impl(*dialect:Dialect*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]

Return a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object corresponding to a dialect.

This is an end-user override hook that can be used to provide
differing types depending on the given dialect.  It is used
by the [TypeDecorator](#sqlalchemy.types.TypeDecorator) implementation of [type_engine()](#sqlalchemy.types.TypeDecorator.type_engine)
to help determine what type should ultimately be returned
for a given [TypeDecorator](#sqlalchemy.types.TypeDecorator).

By default returns `self.impl`.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)process_bind_param(*value:_T|None*, *dialect:Dialect*) → Any

Receive a bound parameter value to be converted.

Custom subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should override
this method to provide custom behaviors for incoming data values.
This method is called at **statement execution time** and is passed
the literal Python data value which is to be associated with a bound
parameter in the statement.

The operation could be anything desired to perform custom
behavior, such as transforming or serializing data.
This could also be used as a hook for validating logic.

  Parameters:

- **value** – Data to operate upon, of any type expected by
  this method in the subclass.  Can be `None`.
- **dialect** – the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in use.

See also

[Augmenting Existing Types](#types-typedecorator)

[TypeDecorator.process_result_value()](#sqlalchemy.types.TypeDecorator.process_result_value)

     method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)process_literal_param(*value:_T|None*, *dialect:Dialect*) → str

Receive a literal parameter value to be rendered inline within
a statement.

Note

This method is called during the **SQL compilation** phase of a
statement, when rendering a SQL string. Unlike other SQL
compilation methods, it is passed a specific Python value to be
rendered as a string. However it should not be confused with the
[TypeDecorator.process_bind_param()](#sqlalchemy.types.TypeDecorator.process_bind_param) method, which is
the more typical method that processes the actual value passed to a
particular parameter at statement execution time.

Custom subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should override
this method to provide custom behaviors for incoming data values
that are in the special case of being rendered as literals.

The returned string will be rendered into the output string.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)process_result_value(*value:Any|None*, *dialect:Dialect*) → _T | None

Receive a result-row column value to be converted.

Custom subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should override
this method to provide custom behaviors for data values
being received in result rows coming from the database.
This method is called at **result fetching time** and is passed
the literal Python data value that’s extracted from a database result
row.

The operation could be anything desired to perform custom
behavior, such as transforming or deserializing data.

  Parameters:

- **value** – Data to operate upon, of any type expected by
  this method in the subclass.  Can be `None`.
- **dialect** – the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in use.

See also

[Augmenting Existing Types](#types-typedecorator)

[TypeDecorator.process_bind_param()](#sqlalchemy.types.TypeDecorator.process_bind_param)

     method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)result_processor(*dialect:Dialect*, *coltype:Any*) → _ResultProcessorType[_T] | None

Provide a result value processing function for the given
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect).

This is the method that fulfills the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
contract for bound value conversion which normally occurs via
the [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor) method.

Note

User-defined subclasses of [TypeDecorator](#sqlalchemy.types.TypeDecorator) should
**not** implement this method, and should instead implement
[TypeDecorator.process_result_value()](#sqlalchemy.types.TypeDecorator.process_result_value) so that the
“inner” processing provided by the implementing type is maintained.

   Parameters:

- **dialect** – Dialect instance in use.
- **coltype** – A SQLAlchemy data type

      property sort_key_function: Callable[[Any], Any] | None

The type of the None singleton.

    method [sqlalchemy.types.TypeDecorator.](#sqlalchemy.types.TypeDecorator)type_engine(*dialect:Dialect*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]

Return a dialect-specific [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) instance
for this [TypeDecorator](#sqlalchemy.types.TypeDecorator).

In most cases this returns a dialect-adapted form of
the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) type represented by `self.impl`.
Makes usage of `dialect_impl()`.
Behavior can be customized here by overriding
[load_dialect_impl()](#sqlalchemy.types.TypeDecorator.load_dialect_impl).

## TypeDecorator Recipes

A few key [TypeDecorator](#sqlalchemy.types.TypeDecorator) recipes follow.

### Coercing Encoded Strings to Unicode

A common source of confusion regarding the [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode) type
is that it is intended to deal *only* with Python `unicode` objects
on the Python side, meaning values passed to it as bind parameters
must be of the form `u'some string'` if using Python 2 and not 3.
The encoding/decoding functions it performs are only to suit what the
DBAPI in use requires, and are primarily a private implementation detail.

The use case of a type that can safely receive Python bytestrings,
that is strings that contain non-ASCII characters and are not `u''`
objects in Python 2, can be achieved using a [TypeDecorator](#sqlalchemy.types.TypeDecorator)
which coerces as needed:

```
from sqlalchemy.types import TypeDecorator, Unicode

class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode("utf-8")
        return value
```

### Rounding Numerics

Some database connectors like those of SQL Server choke if a Decimal is passed with too
many decimal places.   Here’s a recipe that rounds them down:

```
from sqlalchemy.types import TypeDecorator, Numeric
from decimal import Decimal

class SafeNumeric(TypeDecorator):
    """Adds quantization to Numeric."""

    impl = Numeric

    def __init__(self, *arg, **kw):
        TypeDecorator.__init__(self, *arg, **kw)
        self.quantize_int = -self.impl.scale
        self.quantize = Decimal(10) ** self.quantize_int

    def process_bind_param(self, value, dialect):
        if isinstance(value, Decimal) and value.as_tuple()[2] < self.quantize_int:
            value = value.quantize(self.quantize)
        return value
```

### Store Timezone Aware Timestamps as Timezone Naive UTC

Timestamps in databases should always be stored in a timezone-agnostic way. For
most databases, this means ensuring a timestamp is first in the UTC timezone
before it is stored, then storing it as timezone-naive (that is, without any
timezone associated with it; UTC is assumed to be the “implicit” timezone).
Alternatively,  database-specific types like PostgreSQLs “TIMESTAMP WITH
TIMEZONE” are often preferred for their richer functionality; however, storing
as plain UTC will work on all databases and drivers.   When a
timezone-intelligent database type is not an option or is not preferred,  the
[TypeDecorator](#sqlalchemy.types.TypeDecorator) can be used to create a datatype that convert timezone
aware timestamps into timezone naive and back again.   Below, Python’s
built-in `datetime.timezone.utc` timezone is used to normalize and
denormalize:

```
import datetime

class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value
```

### Backend-agnostic GUID Type

Note

Since version 2.0 the built-in [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid) type that
behaves similarly should be preferred. This example is presented
just as an example of a type decorator that receives and returns
python objects.

Receives and returns Python uuid() objects.
Uses the PG UUID type when using PostgreSQL, UNIQUEIDENTIFIER when using MSSQL,
CHAR(32) on other backends, storing them in stringified format.
The `GUIDHyphens` version stores the value with hyphens instead of just the hex
string, using a CHAR(36) type:

```
from operator import attrgetter
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import uuid

class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type or MSSQL's UNIQUEIDENTIFIER,
    otherwise uses CHAR(32), storing as stringified hex values.

    """

    impl = CHAR
    cache_ok = True

    _default_type = CHAR(32)
    _uuid_as_str = attrgetter("hex")

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        elif dialect.name == "mssql":
            return dialect.type_descriptor(UNIQUEIDENTIFIER())
        else:
            return dialect.type_descriptor(self._default_type)

    def process_bind_param(self, value, dialect):
        if value is None or dialect.name in ("postgresql", "mssql"):
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return self._uuid_as_str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

class GUIDHyphens(GUID):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type or MSSQL's UNIQUEIDENTIFIER,
    otherwise uses CHAR(36), storing as stringified uuid values.

    """

    _default_type = CHAR(36)
    _uuid_as_str = str
```

#### Linking Pythonuuid.UUIDto the Custom Type for ORM mappings

When declaring ORM mappings using [Annotated Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column)
mappings, the custom `GUID` type defined above may be associated with
the Python `uuid.UUID` datatype by adding it to the
[type annotation map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map),
which is typically defined on the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class:

```
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    type_annotation_map = {
        uuid.UUID: GUID,
    }
```

With the above configuration, ORM mapped classes which extend from
`Base` may refer to Python `uuid.UUID` in annotations which will make use
of `GUID` automatically:

```
class MyModel(Base):
    __tablename__ = "my_table"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
```

See also

[Customizing the Type Map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map)

### Marshal JSON Strings

This type uses `simplejson` to marshal Python data structures
to/from JSON.   Can be modified to use Python’s builtin json encoder:

```
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage:

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
```

#### Adding Mutability

The ORM by default will not detect “mutability” on such a type as above -
meaning, in-place changes to values will not be detected and will not be
flushed.   Without further steps, you instead would need to replace the existing
value with a new one on each parent object to detect changes:

```
obj.json_value["key"] = "value"  # will *not* be detected by the ORM

obj.json_value = {"key": "value"}  # *will* be detected by the ORM
```

The above limitation may be
fine, as many applications may not require that the values are ever mutated
once created.  For those which do have this requirement, support for mutability
is best applied using the `sqlalchemy.ext.mutable` extension.  For a
dictionary-oriented JSON structure, we can apply this as:

```
json_type = MutableDict.as_mutable(JSONEncodedDict)

class MyClass(Base):
    #  ...

    json_data = Column(json_type)
```

See also

[Mutation Tracking](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html)

#### Dealing with Comparison Operations

The default behavior of [TypeDecorator](#sqlalchemy.types.TypeDecorator) is to coerce the “right hand side”
of any expression into the same type.  For a type like JSON, this means that
any operator used must make sense in terms of JSON.    For some cases,
users may wish for the type to behave like JSON in some circumstances, and
as plain text in others.  One example is if one wanted to handle the
LIKE operator for the JSON type.  LIKE makes no sense against a JSON structure,
but it does make sense against the underlying textual representation.  To
get at this with a type like `JSONEncodedDict`, we need to
**coerce** the column to a textual form using [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) or
[type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce) before attempting to use this operator:

```
from sqlalchemy import type_coerce, String

stmt = select(my_table).where(type_coerce(my_table.c.json_data, String).like("%foo%"))
```

[TypeDecorator](#sqlalchemy.types.TypeDecorator) provides a built-in system for working up type
translations like these based on operators.  If we wanted to frequently use the
LIKE operator with our JSON object interpreted as a string, we can build it
into the type by overriding the [TypeDecorator.coerce_compared_value()](#sqlalchemy.types.TypeDecorator.coerce_compared_value)
method:

```
from sqlalchemy.sql import operators
from sqlalchemy import String

class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    cache_ok = True

    def coerce_compared_value(self, op, value):
        if op in (operators.like_op, operators.not_like_op):
            return String()
        else:
            return self

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
```

Above is just one approach to handling an operator like “LIKE”.  Other
applications may wish to raise `NotImplementedError` for operators that
have no meaning with a JSON object such as “LIKE”, rather than automatically
coercing to text.

## Applying SQL-level Bind/Result Processing

As seen in the section [Augmenting Existing Types](#types-typedecorator),
SQLAlchemy allows Python functions to be invoked both when parameters are sent
to a statement, as well as when result rows are loaded from the database, to apply
transformations to the values as they are sent to or from the database.   It is also
possible to define SQL-level transformations as well.  The rationale here is when
only the relational database contains a particular series of functions that are necessary
to coerce incoming and outgoing data between an application and persistence format.
Examples include using database-defined encryption/decryption functions, as well
as stored procedures that handle geographic data.

Any [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine), [UserDefinedType](#sqlalchemy.types.UserDefinedType) or [TypeDecorator](#sqlalchemy.types.TypeDecorator)
subclass can include implementations of [TypeEngine.bind_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_expression)
and/or [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression), which when defined to return a
non-`None` value should return a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
expression to be injected into the SQL statement, either surrounding bound
parameters or a column expression.

Tip

As SQL-level result processing features are intended to assist with
coercing data from a SELECT statement into result rows in Python, the
[TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression) conversion method is applied only to
the **outermost** columns clause in a SELECT; it does **not** apply to
columns rendered inside of subqueries, as these column expressions are not
directly delivered to a result.  The expression should not be applied to
both, as this would lead to double-conversion of columns, and the
“outermost” level rather than the “innermost” level is used so that
conversion routines don’t interfere with the internal expressions used by
the statement, and so that only data that’s outgoing to a result row is
actually subject to conversion, which is consistent with the result
row processing functionality provided by
[TypeDecorator.process_result_value()](#sqlalchemy.types.TypeDecorator.process_result_value).

For example, to build a `Geometry` type which will apply the PostGIS function
`ST_GeomFromText` to all outgoing values and the function `ST_AsText` to
all incoming data, we can create our own subclass of [UserDefinedType](#sqlalchemy.types.UserDefinedType)
which provides these methods in conjunction with
[func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func):

```
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

class Geometry(UserDefinedType):
    def get_col_spec(self):
        return "GEOMETRY"

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)
```

We can apply the `Geometry` type into [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata
and use it in a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct:

```
geometry = Table(
    "geometry",
    metadata,
    Column("geom_id", Integer, primary_key=True),
    Column("geom_data", Geometry),
)

print(
    select(geometry).where(
        geometry.c.geom_data == "LINESTRING(189412 252431,189631 259122)"
    )
)
```

The resulting SQL embeds both functions as appropriate.   `ST_AsText`
is applied to the columns clause so that the return value is run through
the function before passing into a result set, and `ST_GeomFromText`
is run on the bound parameter so that the passed-in value is converted:

```
SELECT geometry.geom_id, ST_AsText(geometry.geom_data) AS geom_data_1
FROM geometry
WHERE geometry.geom_data = ST_GeomFromText(:geom_data_2)
```

The [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression) method interacts with the
mechanics of the compiler such that the SQL expression does not interfere
with the labeling of the wrapped expression.   Such as, if we rendered
a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) against a [label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.label) of our expression, the string
label is moved to the outside of the wrapped expression:

```
print(select(geometry.c.geom_data.label("my_data")))
```

Output:

```
SELECT ST_AsText(geometry.geom_data) AS my_data
FROM geometry
```

Another example is we decorate
[BYTEA](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.BYTEA) to provide a `PGPString`, which will make use of the
PostgreSQL `pgcrypto` extension to encrypt/decrypt values
transparently:

```
from sqlalchemy import (
    create_engine,
    String,
    select,
    func,
    MetaData,
    Table,
    Column,
    type_coerce,
    TypeDecorator,
)

from sqlalchemy.dialects.postgresql import BYTEA

class PGPString(TypeDecorator):
    impl = BYTEA

    cache_ok = True

    def __init__(self, passphrase):
        super(PGPString, self).__init__()

        self.passphrase = passphrase

    def bind_expression(self, bindvalue):
        # convert the bind's type from PGPString to
        # String, so that it's passed to psycopg2 as is without
        # a dbapi.Binary wrapper
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.passphrase)

    def column_expression(self, col):
        return func.pgp_sym_decrypt(col, self.passphrase)

metadata_obj = MetaData()
message = Table(
    "message",
    metadata_obj,
    Column("username", String(50)),
    Column("message", PGPString("this is my passphrase")),
)

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test", echo=True)
with engine.begin() as conn:
    metadata_obj.create_all(conn)

    conn.execute(
        message.insert(),
        {"username": "some user", "message": "this is my message"},
    )

    print(
        conn.scalar(select(message.c.message).where(message.c.username == "some user"))
    )
```

The `pgp_sym_encrypt` and `pgp_sym_decrypt` functions are applied
to the INSERT and SELECT statements:

```
INSERT INTO message (username, message)
  VALUES (%(username)s, pgp_sym_encrypt(%(message)s, %(pgp_sym_encrypt_1)s))
  -- {'username': 'some user', 'message': 'this is my message',
  --  'pgp_sym_encrypt_1': 'this is my passphrase'}

SELECT pgp_sym_decrypt(message.message, %(pgp_sym_decrypt_1)s) AS message_1
  FROM message
  WHERE message.username = %(username_1)s
  -- {'pgp_sym_decrypt_1': 'this is my passphrase', 'username_1': 'some user'}
```

## Redefining and Creating New Operators

SQLAlchemy Core defines a fixed set of expression operators available to all column expressions.
Some of these operations have the effect of overloading Python’s built-in operators;
examples of such operators include
[ColumnOperators.__eq__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__eq__) (`table.c.somecolumn == 'foo'`),
[ColumnOperators.__invert__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__invert__) (`~table.c.flag`),
and [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__) (`table.c.x + table.c.y`).  Other operators are exposed as
explicit methods on column expressions, such as
[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) (`table.c.value.in_(['x', 'y'])`) and [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)
(`table.c.value.like('%ed%')`).

When the need arises for a SQL operator that isn’t directly supported by the
already supplied methods above, the most expedient way to produce this operator is
to use the [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) method on any SQL expression object; this method
is given a string representing the SQL operator to render, and the return value
is a Python callable that accepts any arbitrary right-hand side expression:

```
>>> from sqlalchemy import column
>>> expr = column("x").op(">>")(column("y"))
>>> print(expr)
x >> y
```

When making use of custom SQL types, there is also a means of implementing
custom operators as above that are automatically present upon any column
expression that makes use of that column type, without the need to directly
call [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) each time the operator is to be used.

To achieve this, a SQL
expression construct consults the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object associated
with the construct in order to determine the behavior of the built-in
operators as well as to look for new methods that may have been invoked.
[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) defines a
“comparison” object implemented by the [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) class to provide the base
behavior for SQL operators, and many specific types provide their own
sub-implementations of this class. User-defined [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator)
implementations can be built directly into a simple subclass of a particular
type in order to override or define new operations. Below, we create a
[Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) subclass which overrides the [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__)
operator, which in turn uses [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) to produce the custom
SQL itself:

```
from sqlalchemy import Integer

class MyInt(Integer):
    class comparator_factory(Integer.Comparator):
        def __add__(self, other):
            return self.op("goofy")(other)
```

The above configuration creates a new class `MyInt`, which
establishes the [TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory) attribute as
referring to a new class, subclassing the [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) class
associated with the [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) type.

Usage:

```
>>> sometable = Table("sometable", metadata, Column("data", MyInt))
>>> print(sometable.c.data + 5)
sometable.data goofy :data_1
```

The implementation for [ColumnOperators.__add__()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.__add__) is consulted
by an owning SQL expression, by instantiating the [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) with
itself as the `expr` attribute.  This attribute may be used when the
implementation needs to refer to the originating [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
object directly:

```
from sqlalchemy import Integer

class MyInt(Integer):
    class comparator_factory(Integer.Comparator):
        def __add__(self, other):
            return func.special_addition(self.expr, other)
```

New methods added to a [Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) are exposed on an
owning SQL expression object using a dynamic lookup scheme, which exposes methods added to
[Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator) onto the owning [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
expression construct.  For example, to add a `log()` function
to integers:

```
from sqlalchemy import Integer, func

class MyInt(Integer):
    class comparator_factory(Integer.Comparator):
        def log(self, other):
            return func.log(self.expr, other)
```

Using the above type:

```
>>> print(sometable.c.data.log(5))
log(:log_1, :log_2)
```

When using [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) for comparison operations that return a
boolean result, the [Operators.op.is_comparison](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.is_comparison) flag should be
set to `True`:

```
class MyInt(Integer):
    class comparator_factory(Integer.Comparator):
        def is_frobnozzled(self, other):
            return self.op("--is_frobnozzled->", is_comparison=True)(other)
```

Unary operations
are also possible.  For example, to add an implementation of the
PostgreSQL factorial operator, we combine the [UnaryExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.UnaryExpression) construct
along with a [custom_op](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.custom_op) to produce the factorial expression:

```
from sqlalchemy import Integer
from sqlalchemy.sql.expression import UnaryExpression
from sqlalchemy.sql import operators

class MyInteger(Integer):
    class comparator_factory(Integer.Comparator):
        def factorial(self):
            return UnaryExpression(
                self.expr, modifier=operators.custom_op("!"), type_=MyInteger
            )
```

Using the above type:

```
>>> from sqlalchemy.sql import column
>>> print(column("x", MyInteger).factorial())
x !
```

See also

[Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

## Creating New Types

The [UserDefinedType](#sqlalchemy.types.UserDefinedType) class is provided as a simple base class
for defining entirely new database types.   Use this to represent native
database types not known by SQLAlchemy.   If only Python translation behavior
is needed, use [TypeDecorator](#sqlalchemy.types.TypeDecorator) instead.

| Object Name | Description |
| --- | --- |
| UserDefinedType | Base for user defined types. |

   class sqlalchemy.types.UserDefinedType

*inherits from* [sqlalchemy.types.ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType), `sqlalchemy.types.TypeEngineMixin`, [sqlalchemy.types.TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine), `sqlalchemy.util.langhelpers.EnsureKWArg`

Base for user defined types.

This should be the base of new types.  Note that
for most cases, [TypeDecorator](#sqlalchemy.types.TypeDecorator) is probably
more appropriate:

```
import sqlalchemy.types as types

class MyType(types.UserDefinedType):
    cache_ok = True

    def __init__(self, precision=8):
        self.precision = precision

    def get_col_spec(self, **kw):
        return "MYTYPE(%s)" % self.precision

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process
```

Once the type is made, it’s immediately usable:

```
table = Table(
    "foo",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("data", MyType(16)),
)
```

The `get_col_spec()` method will in most cases receive a keyword
argument `type_expression` which refers to the owning expression
of the type as being compiled, such as a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or
[cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) construct.  This keyword is only sent if the method
accepts keyword arguments (e.g. `**kw`) in its argument signature;
introspection is used to check for this in order to support legacy
forms of this function.

The [UserDefinedType.cache_ok](#sqlalchemy.types.UserDefinedType.cache_ok) class-level flag indicates if this
custom [UserDefinedType](#sqlalchemy.types.UserDefinedType) is safe to be used as part of a cache key.
This flag defaults to `None` which will initially generate a warning
when the SQL compiler attempts to generate a cache key for a statement
that uses this type.  If the [UserDefinedType](#sqlalchemy.types.UserDefinedType) is not guaranteed
to produce the same bind/result behavior and SQL generation
every time, this flag should be set to `False`; otherwise if the
class produces the same behavior each time, it may be set to `True`.
See [UserDefinedType.cache_ok](#sqlalchemy.types.UserDefinedType.cache_ok) for further notes on how this works.

Added in version 1.4.28: Generalized the [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok)
flag so that it is available for both [TypeDecorator](#sqlalchemy.types.TypeDecorator) as well
as [UserDefinedType](#sqlalchemy.types.UserDefinedType).

| Member Name | Description |
| --- | --- |
| cache_ok | Indicate if statements using thisExternalTypeare “safe to
cache”. |
| coerce_compared_value() | Suggest a type for a ‘coerced’ Python value in an expression. |
| ensure_kwarg | a regular expression that indicates method names for which the method
should accept**kwarguments. |

   attribute [sqlalchemy.types.UserDefinedType.](#sqlalchemy.types.UserDefinedType)cache_ok: bool | None = None

*inherited from the* [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok) *attribute of* [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType)

Indicate if statements using this [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) are “safe to
cache”.

The default value `None` will emit a warning and then not allow caching
of a statement which includes this type.   Set to `False` to disable
statements using this type from being cached at all without a warning.
When set to `True`, the object’s class and selected elements from its
state will be used as part of the cache key.  For example, using a
[TypeDecorator](#sqlalchemy.types.TypeDecorator):

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
some configurability of caching for [TypeDecorator](#sqlalchemy.types.TypeDecorator) classes.

Added in version 1.4.28: - added the [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType) mixin which
generalizes the `cache_ok` flag to both the [TypeDecorator](#sqlalchemy.types.TypeDecorator)
and [UserDefinedType](#sqlalchemy.types.UserDefinedType) classes.

See also

[SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching)

     method [sqlalchemy.types.UserDefinedType.](#sqlalchemy.types.UserDefinedType)coerce_compared_value(*op:OperatorType|None*, *value:Any*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]

Suggest a type for a ‘coerced’ Python value in an expression.

Default behavior for [UserDefinedType](#sqlalchemy.types.UserDefinedType) is the
same as that of [TypeDecorator](#sqlalchemy.types.TypeDecorator); by default it returns
`self`, assuming the compared value should be coerced into
the same type as this one.  See
[TypeDecorator.coerce_compared_value()](#sqlalchemy.types.TypeDecorator.coerce_compared_value) for more detail.

    attribute [sqlalchemy.types.UserDefinedType.](#sqlalchemy.types.UserDefinedType)ensure_kwarg: str = 'get_col_spec'

a regular expression that indicates method names for which the method
should accept `**kw` arguments.

The class will scan for methods matching the name template and decorate
them if necessary to ensure `**kw` parameters are accepted.

## Working with Custom Types and Reflection

It is important to note that database types which are modified to have
additional in-Python behaviors, including types based on
[TypeDecorator](#sqlalchemy.types.TypeDecorator) as well as other user-defined subclasses of datatypes,
do not have any representation within a database schema.    When using database
the introspection features described at [Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection), SQLAlchemy
makes use of a fixed mapping which links the datatype information reported by a
database server to a SQLAlchemy datatype object.   For example, if we look
inside of a PostgreSQL schema at the definition for a particular database
column, we might receive back the string `"VARCHAR"`.  SQLAlchemy’s
PostgreSQL dialect has a hardcoded mapping which links the string name
`"VARCHAR"` to the SQLAlchemy [VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR) class, and that’s how when we
emit a statement like `Table('my_table', m, autoload_with=engine)`, the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object within it would have an instance of [VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR)
present inside of it.

The implication of this is that if a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object makes use of type
objects that don’t correspond directly to the database-native type name, if we
create a new [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object against a new [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection
for this database table elsewhere using reflection, it will not have this
datatype. For example:

```
>>> from sqlalchemy import (
...     Table,
...     Column,
...     MetaData,
...     create_engine,
...     PickleType,
...     Integer,
... )
>>> metadata = MetaData()
>>> my_table = Table(
...     "my_table", metadata, Column("id", Integer), Column("data", PickleType)
... )
>>> engine = create_engine("sqlite://", echo="debug")
>>> my_table.create(engine)
INFO sqlalchemy.engine.base.Engine
CREATE TABLE my_table (
    id INTEGER,
    data BLOB
)
```

Above, we made use of [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType), which is a [TypeDecorator](#sqlalchemy.types.TypeDecorator)
that works on top of the [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary) datatype, which on SQLite
corresponds to the database type `BLOB`.  In the CREATE TABLE, we see that
the `BLOB` datatype is used.   The SQLite database knows nothing about the
[PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType) we’ve used.

If we look at the datatype of `my_table.c.data.type`, as this is a Python
object that was created by us directly, it is [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType):

```
>>> my_table.c.data.type
PickleType()
```

However, if we create another instance of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) using reflection,
the use of [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType) is not represented in the SQLite database we’ve
created; we instead get back [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB):

```
>>> metadata_two = MetaData()
>>> my_reflected_table = Table("my_table", metadata_two, autoload_with=engine)
INFO sqlalchemy.engine.base.Engine PRAGMA main.table_info("my_table")
INFO sqlalchemy.engine.base.Engine ()
DEBUG sqlalchemy.engine.base.Engine Col ('cid', 'name', 'type', 'notnull', 'dflt_value', 'pk')
DEBUG sqlalchemy.engine.base.Engine Row (0, 'id', 'INTEGER', 0, None, 0)
DEBUG sqlalchemy.engine.base.Engine Row (1, 'data', 'BLOB', 0, None, 0)

>>> my_reflected_table.c.data.type
BLOB()
```

Typically, when an application defines explicit [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata with
custom types, there is no need to use table reflection because the necessary
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata is already present.  However, for the case where an
application, or a combination of them, need to make use of both explicit
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata which includes custom, Python-level datatypes, as well
as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects which set up their [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects as
reflected from the database, which nevertheless still need to exhibit the
additional Python behaviors of the custom datatypes, additional steps must be
taken to allow this.

The most straightforward is to override specific columns as described at
[Overriding Reflected Columns](https://docs.sqlalchemy.org/en/20/core/reflection.html#reflection-overriding-columns).  In this technique, we simply
use reflection in combination with explicit [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects for those
columns for which we want to use a custom or decorated datatype:

```
>>> metadata_three = MetaData()
>>> my_reflected_table = Table(
...     "my_table",
...     metadata_three,
...     Column("data", PickleType),
...     autoload_with=engine,
... )
```

The `my_reflected_table` object above is reflected, and will load the
definition of the “id” column from the SQLite database.  But for the “data”
column, we’ve overridden the reflected object with an explicit [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
definition that includes our desired in-Python datatype, the
[PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType). The reflection process will leave this [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object intact:

```
>>> my_reflected_table.c.data.type
PickleType()
```

A more elaborate way to convert from database-native type objects to custom
datatypes is to use the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event handler.   If
for example we knew that we wanted all [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB) datatypes to in fact be
[PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType), we could set up a rule across the board:

```
from sqlalchemy import BLOB
from sqlalchemy import event
from sqlalchemy import PickleType
from sqlalchemy import Table

@event.listens_for(Table, "column_reflect")
def _setup_pickletype(inspector, table, column_info):
    if isinstance(column_info["type"], BLOB):
        column_info["type"] = PickleType()
```

When the above code is invoked *before* any table reflection occurs (note also
it should be invoked **only once** in the application, as it is a global rule),
upon reflecting any [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that includes a column with a [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB)
datatype, the resulting datatype will be stored in the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object
as [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType).

In practice, the above event-based approach would likely have additional rules
in order to affect only those columns where the datatype is important, such as
a lookup table of table names and possibly column names, or other heuristics
in order to accurately determine which columns should be established with an
in Python datatype.
