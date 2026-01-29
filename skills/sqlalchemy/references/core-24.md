# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# SQL Datatype Objects

- [The Type Hierarchy](https://docs.sqlalchemy.org/en/20/core/type_basics.html)
  - [The “CamelCase” datatypes](https://docs.sqlalchemy.org/en/20/core/type_basics.html#the-camelcase-datatypes)
  - [The “UPPERCASE” datatypes](https://docs.sqlalchemy.org/en/20/core/type_basics.html#the-uppercase-datatypes)
  - [Backend-specific “UPPERCASE” datatypes](https://docs.sqlalchemy.org/en/20/core/type_basics.html#backend-specific-uppercase-datatypes)
  - [Using “UPPERCASE” and Backend-specific types for multiple backends](https://docs.sqlalchemy.org/en/20/core/type_basics.html#using-uppercase-and-backend-specific-types-for-multiple-backends)
  - [Generic “CamelCase” Types](https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types)
    - [BigInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BigInteger)
    - [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
    - [Date](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Date)
    - [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime)
    - [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum)
    - [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double)
    - [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float)
    - [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer)
    - [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval)
    - [LargeBinary](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary)
    - [MatchType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.MatchType)
    - [Numeric](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Numeric)
    - [PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType)
    - [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType)
    - [SmallInteger](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SmallInteger)
    - [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)
    - [Text](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Text)
    - [Time](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Time)
    - [Unicode](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Unicode)
    - [UnicodeText](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UnicodeText)
    - [Uuid](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid)
  - [SQL Standard and Multiple Vendor “UPPERCASE” Types](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sql-standard-and-multiple-vendor-uppercase-types)
    - [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY)
    - [BIGINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BIGINT)
    - [BINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BINARY)
    - [BLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BLOB)
    - [BOOLEAN](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.BOOLEAN)
    - [CHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR)
    - [CLOB](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CLOB)
    - [DATE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATE)
    - [DATETIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DATETIME)
    - [DECIMAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DECIMAL)
    - [DOUBLE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE)
    - [DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION)
    - [FLOAT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.FLOAT)
    - [INT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INT)
    - [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON)
    - [INTEGER](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.INTEGER)
    - [NCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NCHAR)
    - [NVARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NVARCHAR)
    - [NUMERIC](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.NUMERIC)
    - [REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL)
    - [SMALLINT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SMALLINT)
    - [TEXT](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TEXT)
    - [TIME](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIME)
    - [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP)
    - [UUID](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.UUID)
    - [VARBINARY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARBINARY)
    - [VARCHAR](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.VARCHAR)
- [Custom Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html)
  - [Overriding Type Compilation](https://docs.sqlalchemy.org/en/20/core/custom_types.html#overriding-type-compilation)
  - [Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#augmenting-existing-types)
    - [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
  - [TypeDecorator Recipes](https://docs.sqlalchemy.org/en/20/core/custom_types.html#typedecorator-recipes)
    - [Coercing Encoded Strings to Unicode](https://docs.sqlalchemy.org/en/20/core/custom_types.html#coercing-encoded-strings-to-unicode)
    - [Rounding Numerics](https://docs.sqlalchemy.org/en/20/core/custom_types.html#rounding-numerics)
    - [Store Timezone Aware Timestamps as Timezone Naive UTC](https://docs.sqlalchemy.org/en/20/core/custom_types.html#store-timezone-aware-timestamps-as-timezone-naive-utc)
    - [Backend-agnostic GUID Type](https://docs.sqlalchemy.org/en/20/core/custom_types.html#backend-agnostic-guid-type)
    - [Marshal JSON Strings](https://docs.sqlalchemy.org/en/20/core/custom_types.html#marshal-json-strings)
  - [Applying SQL-level Bind/Result Processing](https://docs.sqlalchemy.org/en/20/core/custom_types.html#applying-sql-level-bind-result-processing)
  - [Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#redefining-and-creating-new-operators)
  - [Creating New Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#creating-new-types)
    - [UserDefinedType](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.UserDefinedType)
  - [Working with Custom Types and Reflection](https://docs.sqlalchemy.org/en/20/core/custom_types.html#working-with-custom-types-and-reflection)
- [Base Type API](https://docs.sqlalchemy.org/en/20/core/type_api.html)
  - [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)
    - [TypeEngine.Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.Comparator)
    - [TypeEngine.adapt()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.adapt)
    - [TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic)
    - [TypeEngine.bind_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_expression)
    - [TypeEngine.bind_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.bind_processor)
    - [TypeEngine.coerce_compared_value()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.coerce_compared_value)
    - [TypeEngine.column_expression()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.column_expression)
    - [TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)
    - [TypeEngine.compare_values()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.compare_values)
    - [TypeEngine.compile()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.compile)
    - [TypeEngine.dialect_impl()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.dialect_impl)
    - [TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none)
    - [TypeEngine.get_dbapi_type()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.get_dbapi_type)
    - [TypeEngine.hashable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.hashable)
    - [TypeEngine.literal_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.literal_processor)
    - [TypeEngine.python_type](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.python_type)
    - [TypeEngine.render_bind_cast](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.render_bind_cast)
    - [TypeEngine.render_literal_cast](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.render_literal_cast)
    - [TypeEngine.result_processor()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.result_processor)
    - [TypeEngine.should_evaluate_none](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.should_evaluate_none)
    - [TypeEngine.sort_key_function](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.sort_key_function)
    - [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant)
  - [Concatenable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Concatenable)
    - [Concatenable.Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Concatenable.Comparator)
    - [Concatenable.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Concatenable.comparator_factory)
  - [Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable)
    - [Indexable.Comparator](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable.Comparator)
    - [Indexable.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable.comparator_factory)
  - [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType)
  - [ExternalType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType)
    - [ExternalType.cache_ok](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.ExternalType.cache_ok)
  - [Variant](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant)
    - [Variant.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Variant.with_variant)

---

# SQLAlchemy 2.0 Documentation

# Visitor and Traversal Utilities

The [sqlalchemy.sql.visitors](#module-sqlalchemy.sql.visitors) module consists of classes and functions
that serve the purpose of generically **traversing** a Core SQL expression
structure.   This is not unlike the Python `ast` module in that is presents
a system by which a program can operate upon each component of a SQL
expression.   Common purposes this serves are locating various kinds of
elements such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects,
as well as altering the state of the structure such as replacing certain FROM
clauses with others.

Note

the [sqlalchemy.sql.visitors](#module-sqlalchemy.sql.visitors) module is an internal API and
is not fully public.    It is subject to change and may additionally not
function as expected for use patterns that aren’t considered within
SQLAlchemy’s own internals.

The [sqlalchemy.sql.visitors](#module-sqlalchemy.sql.visitors) module is part of the **internals** of
SQLAlchemy and it is not usually used by calling application code.  It is
however used in certain edge cases such as when constructing caching routines
as well as when building out custom SQL expressions using the
[Custom SQL Constructs and Compilation Extension](https://docs.sqlalchemy.org/en/20/core/compiler.html).

Visitor/traversal interface and library functions.

| Object Name | Description |
| --- | --- |
| anon_map | alias ofcache_anon_map |
| cloned_traverse(obj, opts, visitors) | Clone the given expression structure, allowing modifications by
visitors for mutable objects. |
| ExternalTraversal | Base class for visitor objects which can traverse externally using
thetraverse()function. |
| InternalTraversal | Defines visitor symbols used for internal traversal. |
| iterate(obj[, opts]) | Traverse the given expression structure, returning an iterator. |
| replacement_traverse(obj, opts, replace) | Clone the given expression structure, allowing element
replacement by a given replacement function. |
| traverse(obj, opts, visitors) | Traverse and visit the given expression structure using the default
iterator. |
| traverse_using(iterator, obj, visitors) | Visit the given expression structure using the given iterator of
objects. |
| Visitable | Base class for visitable objects. |

   class sqlalchemy.sql.visitors.ExternalTraversal

*inherits from* `sqlalchemy.util.langhelpers.MemoizedSlots`

Base class for visitor objects which can traverse externally using
the [traverse()](#sqlalchemy.sql.visitors.traverse) function.

Direct usage of the [traverse()](#sqlalchemy.sql.visitors.traverse) function is usually
preferred.

| Member Name | Description |
| --- | --- |
| chain() | ‘Chain’ an additional ExternalTraversal onto this ExternalTraversal |
| iterate() | Traverse the given expression structure, returning an iterator
of all elements. |
| traverse() | Traverse and visit the given expression structure. |

   method [sqlalchemy.sql.visitors.ExternalTraversal.](#sqlalchemy.sql.visitors.ExternalTraversal)chain(*visitor:ExternalTraversal*) → _ExtT

‘Chain’ an additional ExternalTraversal onto this ExternalTraversal

The chained visitor will receive all visit events after this one.

    method [sqlalchemy.sql.visitors.ExternalTraversal.](#sqlalchemy.sql.visitors.ExternalTraversal)iterate(*obj:ExternallyTraversible|None*) → Iterator[ExternallyTraversible]

Traverse the given expression structure, returning an iterator
of all elements.

    method [sqlalchemy.sql.visitors.ExternalTraversal.](#sqlalchemy.sql.visitors.ExternalTraversal)traverse(*obj:ExternallyTraversible|None*) → ExternallyTraversible | None

Traverse and visit the given expression structure.

    property visitor_iterator: Iterator[[ExternalTraversal](#sqlalchemy.sql.visitors.ExternalTraversal)]

Iterate through this visitor and each ‘chained’ visitor.

     class sqlalchemy.sql.visitors.InternalTraversal

*inherits from* `enum.Enum`

Defines visitor symbols used for internal traversal.

The [InternalTraversal](#sqlalchemy.sql.visitors.InternalTraversal) class is used in two ways.  One is that
it can serve as the superclass for an object that implements the
various visit methods of the class.   The other is that the symbols
themselves of [InternalTraversal](#sqlalchemy.sql.visitors.InternalTraversal) are used within
the `_traverse_internals` collection.   Such as, the [Case](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Case)
object defines `_traverse_internals` as

```
class Case(ColumnElement[_T]):
    _traverse_internals = [
        ("value", InternalTraversal.dp_clauseelement),
        ("whens", InternalTraversal.dp_clauseelement_tuples),
        ("else_", InternalTraversal.dp_clauseelement),
    ]
```

Above, the [Case](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Case) class indicates its internal state as the
attributes named `value`, `whens`, and `else_`.    They each
link to an [InternalTraversal](#sqlalchemy.sql.visitors.InternalTraversal) method which indicates the type
of datastructure to which each attribute refers.

Using the `_traverse_internals` structure, objects of type
`InternalTraversible` will have the following methods automatically
implemented:

- `HasTraverseInternals.get_children()`
- `HasTraverseInternals._copy_internals()`
- `HasCacheKey._gen_cache_key()`

Subclasses can also implement these methods directly, particularly for the
`HasTraverseInternals._copy_internals()` method, when special steps
are needed.

Added in version 1.4.

| Member Name | Description |
| --- | --- |
| dp_annotations_key | Visit the _annotations_cache_key element. |
| dp_anon_name | Visit a potentially “anonymized” string value. |
| dp_boolean | Visit a boolean value. |
| dp_clauseelement | Visit aClauseElementobject. |
| dp_clauseelement_list | Visit a list ofClauseElementobjects. |
| dp_clauseelement_tuple | Visit a tuple ofClauseElementobjects. |
| dp_clauseelement_tuples | Visit a list of tuples which containClauseElementobjects. |
| dp_dialect_options | Visit a dialect options structure. |
| dp_dml_multi_values | Visit the values() multi-valued list of dictionaries of anInsertobject. |
| dp_dml_ordered_values | Visit the values() ordered tuple list of anUpdateobject. |
| dp_dml_values | Visit the values() dictionary of aValuesBase(e.g. Insert or Update) object. |
| dp_fromclause_canonical_column_collection | Visit aFromClauseobject in the context of thecolumnsattribute. |
| dp_fromclause_ordered_set | Visit an ordered set ofFromClauseobjects. |
| dp_has_cache_key | Visit aHasCacheKeyobject. |
| dp_has_cache_key_list | Visit a list ofHasCacheKeyobjects. |
| dp_has_cache_key_tuples | Visit a list of tuples which containHasCacheKeyobjects. |
| dp_ignore | Specify an object that should be ignored entirely. |
| dp_inspectable | Visit an inspectable object where the return value is aHasCacheKeyobject. |
| dp_inspectable_list | Visit a list of inspectable objects which upon inspection are
HasCacheKey objects. |
| dp_multi | Visit an object that may be aHasCacheKeyor may be a
plain hashable object. |
| dp_multi_list | Visit a tuple containing elements that may beHasCacheKeyor
may be a plain hashable object. |
| dp_named_ddl_element | Visit a simple named DDL element. |
| dp_operator | Visit an operator. |
| dp_plain_dict | Visit a dictionary with string keys. |
| dp_plain_obj | Visit a plain python object. |
| dp_prefix_sequence | Visit the sequence represented byHasPrefixesorHasSuffixes. |
| dp_propagate_attrs | Visit the propagate attrs dict.  This hardcodes to the particular
elements we care about right now. |
| dp_statement_hint_list | Visit the_statement_hintscollection of aSelectobject. |
| dp_string | Visit a plain string value. |
| dp_string_clauseelement_dict | Visit a dictionary of string keys toClauseElementobjects. |
| dp_string_list | Visit a list of strings. |
| dp_string_multi_dict | Visit a dictionary of string keys to values which may either be
plain immutable/hashable orHasCacheKeyobjects. |
| dp_table_hint_list | Visit the_hintscollection of aSelectobject. |
| dp_type | Visit aTypeEngineobject |
| dp_unknown_structure | Visit an unknown structure. |

   attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_annotations_key = 'AK'

Visit the _annotations_cache_key element.

This is a dictionary of additional information about a ClauseElement
that modifies its role.  It should be included when comparing or caching
objects, however generating this key is relatively expensive.   Visitors
should check the “_annotations” dict for non-None first before creating
this key.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_anon_name = 'AN'

Visit a potentially “anonymized” string value.

The string value is considered to be significant for cache key
generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_boolean = 'B'

Visit a boolean value.

The boolean value is considered to be significant for cache key
generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_clauseelement = 'CE'

Visit a [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_clauseelement_list = 'CL'

Visit a list of [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_clauseelement_tuple = 'CT'

Visit a tuple of [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_clauseelement_tuples = 'CTS'

Visit a list of tuples which contain [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_dialect_options = 'DO'

Visit a dialect options structure.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_dml_multi_values = 'DML_MV'

Visit the values() multi-valued list of dictionaries of an
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_dml_ordered_values = 'DML_OV'

Visit the values() ordered tuple list of an
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_dml_values = 'DML_V'

Visit the values() dictionary of a [ValuesBase](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.ValuesBase)
(e.g. Insert or Update) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_fromclause_canonical_column_collection = 'FC'

Visit a [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object in the context of the
`columns` attribute.

The column collection is “canonical”, meaning it is the originally
defined location of the [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause) objects.   Right now
this means that the object being visited is a
[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)
or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object only.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_fromclause_ordered_set = 'CO'

Visit an ordered set of [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_has_cache_key = 'HC'

Visit a [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_has_cache_key_list = 'HL'

Visit a list of [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_has_cache_key_tuples = 'HT'

Visit a list of tuples which contain [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey)
objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_ignore = 'IG'

Specify an object that should be ignored entirely.

This currently applies function call argument caching where some
arguments should not be considered to be part of a cache key.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_inspectable = 'IS'

Visit an inspectable object where the return value is a
[HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_inspectable_list = 'IL'

Visit a list of inspectable objects which upon inspection are
HasCacheKey objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_multi = 'M'

Visit an object that may be a [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) or may be a
plain hashable object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_multi_list = 'MT'

Visit a tuple containing elements that may be [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) or
may be a plain hashable object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_named_ddl_element = 'DD'

Visit a simple named DDL element.

The current object used by this method is the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence).

The object is only considered to be important for cache key generation
as far as its name, but not any other aspects of it.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_operator = 'O'

Visit an operator.

The operator is a function from the `sqlalchemy.sql.operators`
module.

The operator value is considered to be significant for cache key
generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_plain_dict = 'PD'

Visit a dictionary with string keys.

The keys of the dictionary should be strings, the values should
be immutable and hashable.   The dictionary is considered to be
significant for cache key generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_plain_obj = 'PO'

Visit a plain python object.

The value should be immutable and hashable, such as an integer.
The value is considered to be significant for cache key generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_prefix_sequence = 'PS'

Visit the sequence represented by [HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes)
or [HasSuffixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes).

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_propagate_attrs = 'PA'

Visit the propagate attrs dict.  This hardcodes to the particular
elements we care about right now.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_statement_hint_list = 'SH'

Visit the `_statement_hints` collection of a
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_string = 'S'

Visit a plain string value.

Examples include table and column names, bound parameter keys, special
keywords such as “UNION”, “UNION ALL”.

The string value is considered to be significant for cache key
generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_string_clauseelement_dict = 'CD'

Visit a dictionary of string keys to [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_string_list = 'SL'

Visit a list of strings.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_string_multi_dict = 'MD'

Visit a dictionary of string keys to values which may either be
plain immutable/hashable or [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) objects.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_table_hint_list = 'TH'

Visit the `_hints` collection of a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
object.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_type = 'T'

Visit a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object

The type object is considered to be significant for cache key
generation.

    attribute [sqlalchemy.sql.visitors.InternalTraversal.](#sqlalchemy.sql.visitors.InternalTraversal)dp_unknown_structure = 'UK'

Visit an unknown structure.

     class sqlalchemy.sql.visitors.Visitable

Base class for visitable objects.

[Visitable](#sqlalchemy.sql.visitors.Visitable) is used to implement the SQL compiler dispatch
functions.    Other forms of traversal such as for cache key generation
are implemented separately using the `HasTraverseInternals`
interface.

Changed in version 2.0: The [Visitable](#sqlalchemy.sql.visitors.Visitable) class was named
`Traversible` in the 1.4 series; the name is changed back
to [Visitable](#sqlalchemy.sql.visitors.Visitable) in 2.0 which is what it was prior to 1.4.

Both names remain importable in both 1.4 and 2.0 versions.

     attribute [sqlalchemy.sql.visitors..](#sqlalchemy.sql.visitors.)sqlalchemy.sql.visitors.anon_map

alias of `cache_anon_map`

    function sqlalchemy.sql.visitors.cloned_traverse(*obj:ExternallyTraversible|None*, *opts:Mapping[str,Any]*, *visitors:Mapping[str,Callable[[Any],None]]*) → ExternallyTraversible | None

Clone the given expression structure, allowing modifications by
visitors for mutable objects.

Traversal usage is the same as that of [traverse()](#sqlalchemy.sql.visitors.traverse).
The visitor functions present in the `visitors` dictionary may also
modify the internals of the given structure as the traversal proceeds.

The [cloned_traverse()](#sqlalchemy.sql.visitors.cloned_traverse) function does **not** provide objects that are
part of the `Immutable` interface to the visit methods (this
primarily includes [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause), [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause) and [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects). As this traversal is
only intended to allow in-place mutation of objects, `Immutable`
objects are skipped. The `Immutable._clone()` method is still called
on each object to allow for objects to replace themselves with a different
object based on a clone of their sub-internals (e.g. a
[ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause) that clones its subquery to return a new
[ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause)).

Changed in version 2.0: The [cloned_traverse()](#sqlalchemy.sql.visitors.cloned_traverse) function omits
objects that are part of the `Immutable` interface.

The central API feature used by the [cloned_traverse()](#sqlalchemy.sql.visitors.cloned_traverse)
and [replacement_traverse()](#sqlalchemy.sql.visitors.replacement_traverse) functions, in addition to the
[ClauseElement.get_children()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.get_children)
function that is used to achieve
the iteration, is the `ClauseElement._copy_internals()`
method.
For a [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
structure to support cloning and replacement
traversals correctly, it needs to be able to pass a cloning function into
its internal members in order to make copies of them.

See also

[traverse()](#sqlalchemy.sql.visitors.traverse)

[replacement_traverse()](#sqlalchemy.sql.visitors.replacement_traverse)

     function sqlalchemy.sql.visitors.iterate(*obj:ExternallyTraversible|None*, *opts:Mapping[str,Any]={}*) → Iterator[ExternallyTraversible]

Traverse the given expression structure, returning an iterator.

Traversal is configured to be breadth-first.

The central API feature used by the [iterate()](#sqlalchemy.sql.visitors.iterate)
function is the
[ClauseElement.get_children()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.get_children) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects.  This method should return all
the [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects which are associated with a
particular [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) object. For example, a
[Case](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Case) structure will refer to a series of
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) objects within its “whens” and “else_”
member variables.

  Parameters:

- **obj** – [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) structure to be traversed
- **opts** – dictionary of iteration options.   This dictionary is usually
  empty in modern usage.

      function sqlalchemy.sql.visitors.replacement_traverse(*obj:ExternallyTraversible|None*, *opts:Mapping[str,Any]*, *replace:_TraverseTransformCallableType[Any]*) → ExternallyTraversible | None

Clone the given expression structure, allowing element
replacement by a given replacement function.

This function is very similar to the [cloned_traverse()](#sqlalchemy.sql.visitors.cloned_traverse)
function, except instead of being passed a dictionary of visitors, all
elements are unconditionally passed into the given replace function.
The replace function then has the option to return an entirely new object
which will replace the one given.  If it returns `None`, then the object
is kept in place.

The difference in usage between [cloned_traverse()](#sqlalchemy.sql.visitors.cloned_traverse) and
[replacement_traverse()](#sqlalchemy.sql.visitors.replacement_traverse) is that in the former case, an
already-cloned object is passed to the visitor function, and the visitor
function can then manipulate the internal state of the object.
In the case of the latter, the visitor function should only return an
entirely different object, or do nothing.

The use case for [replacement_traverse()](#sqlalchemy.sql.visitors.replacement_traverse) is that of
replacing a FROM clause inside of a SQL structure with a different one,
as is a common use case within the ORM.

    function sqlalchemy.sql.visitors.traverse(*obj:ExternallyTraversible|None*, *opts:Mapping[str,Any]*, *visitors:Mapping[str,Callable[[Any],None]]*) → ExternallyTraversible | None

Traverse and visit the given expression structure using the default
iterator.

> e.g.:
>
>
>
> ```
> from sqlalchemy.sql import visitors
>
> stmt = select(some_table).where(some_table.c.foo == "bar")
>
>
> def visit_bindparam(bind_param):
>     print("found bound value: %s" % bind_param.value)
>
>
> visitors.traverse(stmt, {}, {"bindparam": visit_bindparam})
> ```

The iteration of objects uses the [iterate()](#sqlalchemy.sql.visitors.iterate) function,
which does a breadth-first traversal using a stack.

  Parameters:

- **obj** – [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) structure to be traversed
- **opts** – dictionary of iteration options.   This dictionary is usually
  empty in modern usage.
- **visitors** – dictionary of visit functions.   The dictionary should
  have strings as keys, each of which would correspond to the
  `__visit_name__` of a particular kind of SQL expression object, and
  callable functions  as values, each of which represents a visitor function
  for that kind of object.

      function sqlalchemy.sql.visitors.traverse_using(*iterator:Iterable[ExternallyTraversible]*, *obj:ExternallyTraversible|None*, *visitors:Mapping[str,Callable[[Any],None]]*) → ExternallyTraversible | None

Visit the given expression structure using the given iterator of
objects.

[traverse_using()](#sqlalchemy.sql.visitors.traverse_using) is usually called internally as the result
of the [traverse()](#sqlalchemy.sql.visitors.traverse) function.

  Parameters:

- **iterator** – an iterable or sequence which will yield
  [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  structures; the iterator is assumed to be the
  product of the [iterate()](#sqlalchemy.sql.visitors.iterate) function.
- **obj** – the [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  that was used as the target of the
  [iterate()](#sqlalchemy.sql.visitors.iterate) function.
- **visitors** – dictionary of visit functions.  See [traverse()](#sqlalchemy.sql.visitors.traverse)
  for details on this dictionary.

See also

[traverse()](#sqlalchemy.sql.visitors.traverse)
