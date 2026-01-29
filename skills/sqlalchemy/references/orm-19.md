# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# ORM Internals

Key ORM constructs, not otherwise covered in other
sections, are listed here.

| Object Name | Description |
| --- | --- |
| AttributeEventToken | A token propagated throughout the course of a chain of attribute
events. |
| AttributeState | Provide an inspection interface corresponding
to a particular attribute on a particular mapped object. |
| CascadeOptions | Keeps track of the options sent torelationship.cascade |
| ClassManager | Tracks state information at the class level. |
| ColumnProperty | Describes an object attribute that corresponds to a table column
or other column expression. |
| Composite | Declarative-compatible front-end for theCompositePropertyclass. |
| CompositeProperty | Defines a “composite” mapped attribute, representing a collection
of columns as one attribute. |
| IdentityMap |  |
| InspectionAttr | A base class applied to all ORM objects and attributes that are
related to things that can be returned by theinspect()function. |
| InspectionAttrExtensionType | Symbols indicating the type of extension that aInspectionAttris part of. |
| InspectionAttrInfo | Adds the.infoattribute toInspectionAttr. |
| InstanceState | Tracks state information at the instance level. |
| InstrumentedAttribute | Base class fordescriptorobjects that intercept
attribute events on behalf of aMapperPropertyobject.  The actualMapperPropertyis accessible
via theQueryableAttribute.propertyattribute. |
| LoaderCallableStatus |  |
| Mapped | Represent an ORM mapped attribute on a mapped class. |
| MappedColumn | Maps a singleColumnon a class. |
| MappedSQLExpression | Declarative front-end for theColumnPropertyclass. |
| MapperProperty | Represent a particular class attribute mapped byMapper. |
| merge_frozen_result(session, statement, frozen_result[, load]) | Merge aFrozenResultback into aSession,
returning a newResultobject withpersistentobjects. |
| merge_result(query, iterator[, load]) | Merge a result into the givenQueryobject’s Session. |
| NotExtension |  |
| PropComparator | Defines SQL operations for ORM mapped attributes. |
| QueryableAttribute | Base class fordescriptorobjects that intercept
attribute events on behalf of aMapperPropertyobject.  The actualMapperPropertyis accessible
via theQueryableAttribute.propertyattribute. |
| QueryContext |  |
| Relationship | Describes an object property that holds a single item or list
of items that correspond to a related database table. |
| RelationshipDirection | enumeration which indicates the ‘direction’ of aRelationshipProperty. |
| RelationshipProperty | Describes an object property that holds a single item or list
of items that correspond to a related database table. |
| SQLORMExpression | A type that may be used to indicate any ORM-level attribute or
object that acts in place of one, in the context of SQL expression
construction. |
| Synonym | Declarative front-end for theSynonymPropertyclass. |
| SynonymProperty | Denote an attribute name as a synonym to a mapped property,
in that the attribute will mirror the value and expression behavior
of another attribute. |
| UOWTransaction |  |

   class sqlalchemy.orm.AttributeState

Provide an inspection interface corresponding
to a particular attribute on a particular mapped object.

The [AttributeState](#sqlalchemy.orm.AttributeState) object is accessed
via the [InstanceState.attrs](#sqlalchemy.orm.InstanceState.attrs) collection
of a particular [InstanceState](#sqlalchemy.orm.InstanceState):

```
from sqlalchemy import inspect

insp = inspect(some_mapped_object)
attr_state = insp.attrs.some_attribute
```

| Member Name | Description |
| --- | --- |
| load_history() | Return the currentpre-flushchange history for
this attribute, via theHistoryinterface. |

   property history: [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History)

Return the current **pre-flush** change history for
this attribute, via the [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History) interface.

This method will **not** emit loader callables if the value of the
attribute is unloaded.

Note

The attribute history system tracks changes on a **per flush
basis**. Each time the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is flushed, the history
of each attribute is reset to empty.   The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) by
default autoflushes each time a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is invoked.
For
options on how to control this, see [Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing).

See also

[AttributeState.load_history()](#sqlalchemy.orm.AttributeState.load_history) - retrieve history
using loader callables if the value is not locally present.

[get_history()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_history) - underlying function

     method [sqlalchemy.orm.AttributeState.](#sqlalchemy.orm.AttributeState)load_history() → [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History)

Return the current **pre-flush** change history for
this attribute, via the [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History) interface.

This method **will** emit loader callables if the value of the
attribute is unloaded.

Note

The attribute history system tracks changes on a **per flush
basis**. Each time the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is flushed, the history
of each attribute is reset to empty.   The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) by
default autoflushes each time a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is invoked.
For
options on how to control this, see [Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing).

See also

[AttributeState.history](#sqlalchemy.orm.AttributeState.history)

[get_history()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_history) - underlying function

     property loaded_value: Any

The current value of this attribute as loaded from the database.

If the value has not been loaded, or is otherwise not present
in the object’s dictionary, returns NO_VALUE.

    property value: Any

Return the value of this attribute.

This operation is equivalent to accessing the object’s
attribute directly or via `getattr()`, and will fire
off any pending loader callables if needed.

     class sqlalchemy.orm.CascadeOptions

*inherits from* `builtins.frozenset`, `typing.Generic`

Keeps track of the options sent to
[relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade)

    class sqlalchemy.orm.ClassManager

*inherits from* `sqlalchemy.util.langhelpers.HasMemoized`, `builtins.dict`, `typing.Generic`, `sqlalchemy.event.registry.EventTarget`

Tracks state information at the class level.

| Member Name | Description |
| --- | --- |
| expired_attribute_loader | previously known as deferred_scalar_loader |
| has_parent() | TODO |
| manage() | Mark this instance as the manager for its class. |
| state_getter() | Return a (instance) -> InstanceState callable. |
| unregister() | remove all instrumentation established by this ClassManager. |

   property deferred_scalar_loader

Deprecated since version 1.4: The ClassManager.deferred_scalar_loader attribute is now named expired_attribute_loader

     attribute [sqlalchemy.orm.ClassManager.](#sqlalchemy.orm.ClassManager)expired_attribute_loader: _ExpiredAttributeLoaderProto

previously known as deferred_scalar_loader

    method [sqlalchemy.orm.ClassManager.](#sqlalchemy.orm.ClassManager)has_parent(*state:InstanceState[_O]*, *key:str*, *optimistic:bool=False*) → bool

TODO

    method [sqlalchemy.orm.ClassManager.](#sqlalchemy.orm.ClassManager)manage()

Mark this instance as the manager for its class.

    method [sqlalchemy.orm.ClassManager.](#sqlalchemy.orm.ClassManager)state_getter()

Return a (instance) -> InstanceState callable.

“state getter” callables should raise either KeyError or
AttributeError if no InstanceState could be found for the
instance.

    method [sqlalchemy.orm.ClassManager.](#sqlalchemy.orm.ClassManager)unregister() → None

remove all instrumentation established by this ClassManager.

     class sqlalchemy.orm.ColumnProperty

*inherits from* `sqlalchemy.orm._MapsColumns`, `sqlalchemy.orm.StrategizedProperty`, `sqlalchemy.orm._IntrospectsAnnotations`, [sqlalchemy.log.Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified)

Describes an object attribute that corresponds to a table column
or other column expression.

Public constructor is the [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) function.

| Member Name | Description |
| --- | --- |
| expressions |  |
| operate() | Operate on an argument. |
| reverse_operate() | Reverse operate on an argument. |
| declarative_scan() | Perform class-specific initialization at early declarative scanning
time. |
| do_init() | Perform subclass-specific initialization post-mapper-creation
steps. |
| instrument_class() | Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty. |
| merge() | Merge the attribute represented by thisMapperPropertyfrom source to destination object. |

   class Comparator

*inherits from* `sqlalchemy.util.langhelpers.MemoizedSlots`, [sqlalchemy.orm.PropComparator](#sqlalchemy.orm.PropComparator)

Produce boolean, comparison, and other operators for
[ColumnProperty](#sqlalchemy.orm.ColumnProperty) attributes.

See the documentation for [PropComparator](#sqlalchemy.orm.PropComparator) for a brief
overview.

See also

[PropComparator](#sqlalchemy.orm.PropComparator)

[ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

    attribute [sqlalchemy.orm.ColumnProperty.Comparator.](#sqlalchemy.orm.ColumnProperty.Comparator)expressions: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[NamedColumn[Any]]  The full sequence of columns referenced by this

attribute, adjusted for any aliasing in progress.

Added in version 1.3.17.

See also

[Mapping a Class against Multiple Tables](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html#maptojoin) - usage example

     method [sqlalchemy.orm.ColumnProperty.Comparator.](#sqlalchemy.orm.ColumnProperty.Comparator)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

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

      method [sqlalchemy.orm.ColumnProperty.Comparator.](#sqlalchemy.orm.ColumnProperty.Comparator)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.orm.ColumnProperty.Comparator.operate).

     property columns_to_assign: List[Tuple[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any], int]]

A list of Column objects that should be declaratively added to the
new Table object.

    method [sqlalchemy.orm.ColumnProperty.](#sqlalchemy.orm.ColumnProperty)declarative_scan(*decl_scan:_ClassScanMapperConfig*, *registry:_RegistryType*, *cls:Type[Any]*, *originating_module:str|None*, *key:str*, *mapped_container:Type[Mapped[Any]]|None*, *annotation:_AnnotationScanType|None*, *extracted_mapped_annotation:_AnnotationScanType|None*, *is_dataclass_field:bool*) → None

Perform class-specific initialization at early declarative scanning
time.

Added in version 2.0.

     method [sqlalchemy.orm.ColumnProperty.](#sqlalchemy.orm.ColumnProperty)do_init() → None

Perform subclass-specific initialization post-mapper-creation
steps.

This is a template method called by the `MapperProperty`
object’s init() method.

    property expression: ColumnsClauseRole

Return the primary column or expression for this ColumnProperty.

E.g.:

```
class File(Base):
    # ...

    name = Column(String(64))
    extension = Column(String(8))
    filename = column_property(name + "." + extension)
    path = column_property("C:/" + filename.expression)
```

See also

[Composing from Column Properties at Mapping Time](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#mapper-column-property-sql-expressions-composed)

     method [sqlalchemy.orm.ColumnProperty.](#sqlalchemy.orm.ColumnProperty)instrument_class(*mapper:Mapper[Any]*) → None

Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty.

The MapperProperty here will typically call out to the
attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute,
and is called early in the mapper setup process.

The second step is typically the init_class_attribute step,
called from StrategizedProperty via the post_instrument_class()
hook.  This step assigns additional state to the InstrumentedAttribute
(specifically the “impl”) which has been determined after the
MapperProperty has determined what kind of persistence
management it needs to do (e.g. scalar, object, collection, etc).

    property mapper_property_to_assign: [MapperProperty](#sqlalchemy.orm.MapperProperty)[_T] | None

return a MapperProperty to be assigned to the declarative mapping

    method [sqlalchemy.orm.ColumnProperty.](#sqlalchemy.orm.ColumnProperty)merge(*session:Session*, *source_state:InstanceState[Any]*, *source_dict:_InstanceDict*, *dest_state:InstanceState[Any]*, *dest_dict:_InstanceDict*, *load:bool*, *_recursive:Dict[Any,object]*, *_resolve_conflict_map:Dict[_IdentityKeyType[Any],object]*) → None

Merge the attribute represented by this `MapperProperty`
from source to destination object.

     class sqlalchemy.orm.Composite

*inherits from* [sqlalchemy.orm.descriptor_props.CompositeProperty](#sqlalchemy.orm.CompositeProperty), `sqlalchemy.orm.base._DeclarativeMapped`

Declarative-compatible front-end for the [CompositeProperty](#sqlalchemy.orm.CompositeProperty)
class.

Public constructor is the [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) function.

Changed in version 2.0: Added [Composite](#sqlalchemy.orm.Composite) as a Declarative
compatible subclass of [CompositeProperty](#sqlalchemy.orm.CompositeProperty).

See also

[Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite)

     class sqlalchemy.orm.CompositeProperty

*inherits from* `sqlalchemy.orm._MapsColumns`, `sqlalchemy.orm._IntrospectsAnnotations`, `sqlalchemy.orm.descriptor_props.DescriptorProperty`

Defines a “composite” mapped attribute, representing a collection
of columns as one attribute.

[CompositeProperty](#sqlalchemy.orm.CompositeProperty) is constructed using the [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
function.

See also

[Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite)

| Member Name | Description |
| --- | --- |
| create_row_processor() | Produce the “row processing” function for thisBundle. |
| declarative_scan() | Perform class-specific initialization at early declarative scanning
time. |
| do_init() | Initialization which occurs after theCompositehas been associated with its parent mapper. |
| get_history() | Provided for userland code that uses attributes.get_history(). |
| instrument_class() | Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty. |

   class Comparator

*inherits from* [sqlalchemy.orm.PropComparator](#sqlalchemy.orm.PropComparator)

Produce boolean, comparison, and other operators for
[Composite](#sqlalchemy.orm.Composite) attributes.

See the example in [Redefining Comparison Operations for Composites](https://docs.sqlalchemy.org/en/20/orm/composites.html#composite-operations) for an overview
of usage , as well as the documentation for [PropComparator](#sqlalchemy.orm.PropComparator).

See also

[PropComparator](#sqlalchemy.orm.PropComparator)

[ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

     class CompositeBundle

*inherits from* [sqlalchemy.orm.Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle)

    method [sqlalchemy.orm.CompositeProperty.CompositeBundle.](#sqlalchemy.orm.CompositeProperty.CompositeBundle)create_row_processor(*query:Select[Any]*, *procs:Sequence[Callable[[Row[Any]],Any]]*, *labels:Sequence[str]*) → Callable[[[Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)[Any]], Any]

Produce the “row processing” function for this [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle).

May be overridden by subclasses to provide custom behaviors when
results are fetched. The method is passed the statement object and a
set of “row processor” functions at query execution time; these
processor functions when given a result row will return the individual
attribute value, which can then be adapted into any kind of return data
structure.

The example below illustrates replacing the usual [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
return structure with a straight Python dictionary:

```
from sqlalchemy.orm import Bundle

class DictBundle(Bundle):
    def create_row_processor(self, query, procs, labels):
        "Override create_row_processor to return values as dictionaries"

        def proc(row):
            return dict(zip(labels, (proc(row) for proc in procs)))

        return proc
```

A result from the above [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle) will return dictionary
values:

```
bn = DictBundle("mybundle", MyClass.data1, MyClass.data2)
for row in session.execute(select(bn)).where(bn.c.data1 == "d1"):
    print(row.mybundle["data1"], row.mybundle["data2"])
```

      property columns_to_assign: List[Tuple[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any], int]]

A list of Column objects that should be declaratively added to the
new Table object.

    method [sqlalchemy.orm.CompositeProperty.](#sqlalchemy.orm.CompositeProperty)declarative_scan(*decl_scan:_ClassScanMapperConfig*, *registry:_RegistryType*, *cls:Type[Any]*, *originating_module:str|None*, *key:str*, *mapped_container:Type[Mapped[Any]]|None*, *annotation:_AnnotationScanType|None*, *extracted_mapped_annotation:_AnnotationScanType|None*, *is_dataclass_field:bool*) → None

Perform class-specific initialization at early declarative scanning
time.

Added in version 2.0.

     method [sqlalchemy.orm.CompositeProperty.](#sqlalchemy.orm.CompositeProperty)do_init() → None

Initialization which occurs after the [Composite](#sqlalchemy.orm.Composite)
has been associated with its parent mapper.

    method [sqlalchemy.orm.CompositeProperty.](#sqlalchemy.orm.CompositeProperty)get_history(*state:InstanceState[Any]*, *dict_:_InstanceDict*, *passive:PassiveFlag=symbol('PASSIVE_OFF')*) → [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History)

Provided for userland code that uses attributes.get_history().

    method [sqlalchemy.orm.CompositeProperty.](#sqlalchemy.orm.CompositeProperty)instrument_class(*mapper:Mapper[Any]*) → None

Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty.

The MapperProperty here will typically call out to the
attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute,
and is called early in the mapper setup process.

The second step is typically the init_class_attribute step,
called from StrategizedProperty via the post_instrument_class()
hook.  This step assigns additional state to the InstrumentedAttribute
(specifically the “impl”) which has been determined after the
MapperProperty has determined what kind of persistence
management it needs to do (e.g. scalar, object, collection, etc).

    property mapper_property_to_assign: [MapperProperty](#sqlalchemy.orm.MapperProperty)[_CC] | None

return a MapperProperty to be assigned to the declarative mapping

     class sqlalchemy.orm.AttributeEventToken

A token propagated throughout the course of a chain of attribute
events.

Serves as an indicator of the source of the event and also provides
a means of controlling propagation across a chain of attribute
operations.

The `Event` object is sent as the `initiator` argument
when dealing with events such as [AttributeEvents.append()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.append),
[AttributeEvents.set()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.set),
and [AttributeEvents.remove()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.remove).

The `Event` object is currently interpreted by the backref
event handlers, and is used to control the propagation of operations
across two mutually-dependent attributes.

Changed in version 2.0: Changed the name from `AttributeEvent`
to `AttributeEventToken`.

   Attribute impl:

The `AttributeImpl` which is the current event
initiator.

  Attribute op:

The symbol `OP_APPEND`, `OP_REMOVE`,
`OP_REPLACE`, or `OP_BULK_REPLACE`, indicating the
source operation.

      class sqlalchemy.orm.IdentityMap

| Member Name | Description |
| --- | --- |
| check_modified() | return True if any InstanceStates present have been marked
as ‘modified’. |

   method [sqlalchemy.orm.IdentityMap.](#sqlalchemy.orm.IdentityMap)check_modified() → bool

return True if any InstanceStates present have been marked
as ‘modified’.

     class sqlalchemy.orm.InspectionAttr

A base class applied to all ORM objects and attributes that are
related to things that can be returned by the [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function.

The attributes defined here allow the usage of simple boolean
checks to test basic facts about the object returned.

While the boolean checks here are basically the same as using
the Python isinstance() function, the flags here can be used without
the need to import all of these classes, and also such that
the SQLAlchemy class system can change while leaving the flags
here intact for forwards-compatibility.

| Member Name | Description |
| --- | --- |
| extension_type | The extension type, if any.
Defaults toNotExtension.NOT_EXTENSION |
| is_aliased_class | True if this object is an instance ofAliasedClass. |
| is_attribute | True if this object is a Pythondescriptor. |
| is_bundle | True if this object is an instance ofBundle. |
| is_clause_element | True if this object is an instance ofClauseElement. |
| is_instance | True if this object is an instance ofInstanceState. |
| is_mapper | True if this object is an instance ofMapper. |
| is_property | True if this object is an instance ofMapperProperty. |
| is_selectable | Return True if this object is an instance ofSelectable. |

   attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)extension_type: [InspectionAttrExtensionType](#sqlalchemy.orm.InspectionAttrExtensionType) = 'not_extension'

The extension type, if any.
Defaults to `NotExtension.NOT_EXTENSION`

See also

[HybridExtensionType](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.HybridExtensionType)

[AssociationProxyExtensionType](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxyExtensionType)

     attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_aliased_class = False

True if this object is an instance of [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_attribute = False

True if this object is a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).

This can refer to one of many types.   Usually a
[QueryableAttribute](#sqlalchemy.orm.QueryableAttribute) which handles attributes events on behalf
of a [MapperProperty](#sqlalchemy.orm.MapperProperty).   But can also be an extension type
such as [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) or [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property).
The [InspectionAttr.extension_type](#sqlalchemy.orm.InspectionAttr.extension_type) will refer to a constant
identifying the specific subtype.

See also

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

     attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_bundle = False

True if this object is an instance of [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_clause_element = False

True if this object is an instance of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_instance = False

True if this object is an instance of [InstanceState](#sqlalchemy.orm.InstanceState).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_mapper = False

True if this object is an instance of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_property = False

True if this object is an instance of [MapperProperty](#sqlalchemy.orm.MapperProperty).

    attribute [sqlalchemy.orm.InspectionAttr.](#sqlalchemy.orm.InspectionAttr)is_selectable = False

Return True if this object is an instance of
[Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

     class sqlalchemy.orm.InspectionAttrInfo

*inherits from* [sqlalchemy.orm.base.InspectionAttr](#sqlalchemy.orm.InspectionAttr)

Adds the `.info` attribute to [InspectionAttr](#sqlalchemy.orm.InspectionAttr).

The rationale for [InspectionAttr](#sqlalchemy.orm.InspectionAttr) vs. [InspectionAttrInfo](#sqlalchemy.orm.InspectionAttrInfo)
is that the former is compatible as a mixin for classes that specify
`__slots__`; this is essentially an implementation artifact.

| Member Name | Description |
| --- | --- |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisInspectionAttr. |

   attribute [sqlalchemy.orm.InspectionAttrInfo.](#sqlalchemy.orm.InspectionAttrInfo)info

Info dictionary associated with the object, allowing user-defined
data to be associated with this [InspectionAttr](#sqlalchemy.orm.InspectionAttr).

The dictionary is generated when first accessed.  Alternatively,
it can be specified as a constructor argument to the
[column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), or
[composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
functions.

See also

[QueryableAttribute.info](#sqlalchemy.orm.QueryableAttribute.info)

[SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info)

      class sqlalchemy.orm.InstanceState

*inherits from* [sqlalchemy.orm.base.InspectionAttrInfo](#sqlalchemy.orm.InspectionAttrInfo), `typing.Generic`

Tracks state information at the instance level.

The [InstanceState](#sqlalchemy.orm.InstanceState) is a key object used by the
SQLAlchemy ORM in order to track the state of an object;
it is created the moment an object is instantiated, typically
as a result of [instrumentation](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumentation) which SQLAlchemy applies
to the `__init__()` method of the class.

[InstanceState](#sqlalchemy.orm.InstanceState) is also a semi-public object,
available for runtime inspection as to the state of a
mapped instance, including information such as its current
status within a particular [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and details
about data on individual attributes.  The public API
in order to acquire a [InstanceState](#sqlalchemy.orm.InstanceState) object
is to use the [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) system:

```
>>> from sqlalchemy import inspect
>>> insp = inspect(some_mapped_object)
>>> insp.attrs.nickname.history
History(added=['new nickname'], unchanged=(), deleted=['nickname'])
```

See also

[Inspection of Mapped Instances](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapper-inspection-instancestate)

| Member Name | Description |
| --- | --- |
| attrs | Return a namespace representing each attribute on
the mapped object, including its current value
and history. |
| callables | A namespace where a per-state loader callable can be associated. |
| expired | WhenTruethe object isexpired. |
| expired_attributes | The set of keys which are ‘expired’ to be loaded by
the manager’s deferred scalar loader, assuming no pending
changes. |
| is_instance | True if this object is an instance ofInstanceState. |
| mapper | Return theMapperused for this mapped object. |
| modified | WhenTruethe object was modified. |
| unmodified_intersection() | Return self.unmodified.intersection(keys). |

   property async_session: [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) | None

Return the owning [AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) for this instance,
or `None` if none available.

This attribute is only non-None when the `sqlalchemy.ext.asyncio`
API is in use for this ORM object. The returned
[AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession) object will be a proxy for the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object that would be returned from the
[InstanceState.session](#sqlalchemy.orm.InstanceState.session) attribute for this
[InstanceState](#sqlalchemy.orm.InstanceState).

Added in version 1.4.18.

See also

[Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

     attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)attrs

Return a namespace representing each attribute on
the mapped object, including its current value
and history.

The returned object is an instance of [AttributeState](#sqlalchemy.orm.AttributeState).
This object allows inspection of the current data
within an attribute as well as attribute history
since the last flush.

    attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)callables: Dict[str, Callable[[[InstanceState](#sqlalchemy.orm.InstanceState)[_O], PassiveFlag], Any]] = {}

A namespace where a per-state loader callable can be associated.

In SQLAlchemy 1.0, this is only used for lazy loaders / deferred
loaders that were set up via query option.

Previously, callables was used also to indicate expired attributes
by storing a link to the InstanceState itself in this dictionary.
This role is now handled by the expired_attributes set.

    property deleted: bool

Return `True` if the object is [deleted](https://docs.sqlalchemy.org/en/20/glossary.html#term-deleted).

An object that is in the deleted state is guaranteed to
not be within the [Session.identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.identity_map) of its parent
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session); however if the session’s transaction is rolled
back, the object will be restored to the persistent state and
the identity map.

Note

The [InstanceState.deleted](#sqlalchemy.orm.InstanceState.deleted) attribute refers to a specific
state of the object that occurs between the “persistent” and
“detached” states; once the object is [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached), the
[InstanceState.deleted](#sqlalchemy.orm.InstanceState.deleted) attribute **no longer returns
True**; in order to detect that a state was deleted, regardless
of whether or not the object is associated with a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), use the [InstanceState.was_deleted](#sqlalchemy.orm.InstanceState.was_deleted)
accessor.

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

     property detached: bool

Return `True` if the object is [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

     property dict: _InstanceDict

Return the instance dict used by the object.

Under normal circumstances, this is always synonymous
with the `__dict__` attribute of the mapped object,
unless an alternative instrumentation system has been
configured.

In the case that the actual object has been garbage
collected, this accessor returns a blank dictionary.

    attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)expired: bool = False

When `True` the object is [expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired).

See also

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire)

     attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)expired_attributes: Set[str]

The set of keys which are ‘expired’ to be loaded by
the manager’s deferred scalar loader, assuming no pending
changes.

See also the `unmodified` collection which is intersected
against this set when a refresh operation occurs.

    property has_identity: bool

Return `True` if this object has an identity key.

This should always have the same value as the
expression `state.persistent` or `state.detached`.

    property identity: Tuple[Any, ...] | None

Return the mapped identity of the mapped object.
This is the primary key identity as persisted by the ORM
which can always be passed directly to
[Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get).

Returns `None` if the object has no primary key identity.

Note

An object which is [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) or [pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending)
does **not** have a mapped identity until it is flushed,
even if its attributes include primary key values.

     property identity_key: _IdentityKeyType[_O] | None

Return the identity key for the mapped object.

This is the key used to locate the object within
the [Session.identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.identity_map) mapping.   It contains
the identity as returned by [identity](#sqlalchemy.orm.InstanceState.identity) within it.

    attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)is_instance: bool = True

True if this object is an instance of [InstanceState](#sqlalchemy.orm.InstanceState).

    attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)mapper

Return the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) used for this mapped object.

    attribute [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)modified: bool = False

When `True` the object was modified.

    property object: _O | None

Return the mapped object represented by this
[InstanceState](#sqlalchemy.orm.InstanceState).

Returns None if the object has been garbage collected

    property pending: bool

Return `True` if the object is [pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

     property persistent: bool

Return `True` if the object is [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent).

An object that is in the persistent state is guaranteed to
be within the [Session.identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.identity_map) of its parent
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

     property session: [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) | None

Return the owning [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) for this instance,
or `None` if none available.

Note that the result here can in some cases be *different*
from that of `obj in session`; an object that’s been deleted
will report as not `in session`, however if the transaction is
still in progress, this attribute will still refer to that session.
Only when the transaction is completed does the object become
fully detached under normal circumstances.

See also

[InstanceState.async_session](#sqlalchemy.orm.InstanceState.async_session)

     property transient: bool

Return `True` if the object is [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

     property unloaded: Set[str]

Return the set of keys which do not have a loaded value.

This includes expired attributes and any other attribute that was never
populated or modified.

    property unloaded_expirable: Set[str]

Synonymous with [InstanceState.unloaded](#sqlalchemy.orm.InstanceState.unloaded).

Deprecated since version 2.0: The [InstanceState.unloaded_expirable](#sqlalchemy.orm.InstanceState.unloaded_expirable) attribute is deprecated.  Please use [InstanceState.unloaded](#sqlalchemy.orm.InstanceState.unloaded).

This attribute was added as an implementation-specific detail at some
point and should be considered to be private.

    property unmodified: Set[str]

Return the set of keys which have no uncommitted changes

    method [sqlalchemy.orm.InstanceState.](#sqlalchemy.orm.InstanceState)unmodified_intersection(*keys:Iterable[str]*) → Set[str]

Return self.unmodified.intersection(keys).

    property was_deleted: bool

Return True if this object is or was previously in the
“deleted” state and has not been reverted to persistent.

This flag returns True once the object was deleted in flush.
When the object is expunged from the session either explicitly
or via transaction commit and enters the “detached” state,
this flag will continue to report True.

See also

[InstanceState.deleted](#sqlalchemy.orm.InstanceState.deleted) - refers to the “deleted” state

[was_deleted()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.util.was_deleted) - standalone function

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

      class sqlalchemy.orm.InstrumentedAttribute

*inherits from* [sqlalchemy.orm.QueryableAttribute](#sqlalchemy.orm.QueryableAttribute)

Base class for [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor) objects that intercept
attribute events on behalf of a [MapperProperty](#sqlalchemy.orm.MapperProperty)
object.  The actual [MapperProperty](#sqlalchemy.orm.MapperProperty) is accessible
via the `QueryableAttribute.property`
attribute.

See also

[InstrumentedAttribute](#sqlalchemy.orm.InstrumentedAttribute)

[MapperProperty](#sqlalchemy.orm.MapperProperty)

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

[Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs)

     class sqlalchemy.orm.LoaderCallableStatus

*inherits from* `enum.Enum`

| Member Name | Description |
| --- | --- |
| ATTR_EMPTY | Symbol used internally to indicate an attribute had no callable. |
| ATTR_WAS_SET | Symbol returned by a loader callable to indicate the
retrieved value, or values, were assigned to their attributes
on the target object. |
| NEVER_SET | Synonymous with NO_VALUE |
| NO_VALUE | Symbol which may be placed as the ‘previous’ value of an attribute,
indicating no value was loaded for an attribute when it was modified,
and flags indicated we were not to load it. |
| PASSIVE_CLASS_MISMATCH | Symbol indicating that an object is locally present for a given
primary key identity but it is not of the requested class.  The
return value is therefore None and no SQL should be emitted. |
| PASSIVE_NO_RESULT | Symbol returned by a loader callable or other attribute/history
retrieval operation when a value could not be determined, based
on loader callable flags. |

   attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)ATTR_EMPTY = 3

Symbol used internally to indicate an attribute had no callable.

    attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)ATTR_WAS_SET = 2

Symbol returned by a loader callable to indicate the
retrieved value, or values, were assigned to their attributes
on the target object.

    attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)NEVER_SET = 4

Synonymous with NO_VALUE

Changed in version 1.4: NEVER_SET was merged with NO_VALUE

     attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)NO_VALUE = 4

Symbol which may be placed as the ‘previous’ value of an attribute,
indicating no value was loaded for an attribute when it was modified,
and flags indicated we were not to load it.

    attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)PASSIVE_CLASS_MISMATCH = 1

Symbol indicating that an object is locally present for a given
primary key identity but it is not of the requested class.  The
return value is therefore None and no SQL should be emitted.

    attribute [sqlalchemy.orm.LoaderCallableStatus.](#sqlalchemy.orm.LoaderCallableStatus)PASSIVE_NO_RESULT = 0

Symbol returned by a loader callable or other attribute/history
retrieval operation when a value could not be determined, based
on loader callable flags.

     class sqlalchemy.orm.Mapped

*inherits from* [sqlalchemy.orm.base.SQLORMExpression](#sqlalchemy.orm.SQLORMExpression), `sqlalchemy.orm.base.ORMDescriptor`, `sqlalchemy.orm.base._MappedAnnotationBase`, `sqlalchemy.sql.roles.DDLConstraintColumnRole`

Represent an ORM mapped attribute on a mapped class.

This class represents the complete descriptor interface for any class
attribute that will have been [instrumented](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumented) by the ORM
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class.   Provides appropriate information to type
checkers such as pylance and mypy so that ORM-mapped attributes
are correctly typed.

The most prominent use of [Mapped](#sqlalchemy.orm.Mapped) is in
the [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-explicit-declarative-base) form
of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) configuration, where used explicitly it drives
the configuration of ORM attributes such as `mapped_class()`
and [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

See also

[Using a Declarative Base Class](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-explicit-declarative-base)

[Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table)

Tip

The [Mapped](#sqlalchemy.orm.Mapped) class represents attributes that are handled
directly by the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class. It does not include other
Python descriptor classes that are provided as extensions, including
[Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html) and the [Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html).
While these systems still make use of ORM-specific superclasses
and structures, they are not [instrumented](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumented) by the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) and instead provide their own functionality
when they are accessed on a class.

Added in version 1.4.

     class sqlalchemy.orm.MappedColumn

*inherits from* `sqlalchemy.orm._IntrospectsAnnotations`, `sqlalchemy.orm._MapsColumns`, `sqlalchemy.orm.base._DeclarativeMapped`

Maps a single [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) on a class.

[MappedColumn](#sqlalchemy.orm.MappedColumn) is a specialization of the
[ColumnProperty](#sqlalchemy.orm.ColumnProperty) class and is oriented towards declarative
configuration.

To construct [MappedColumn](#sqlalchemy.orm.MappedColumn) objects, use the
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) constructor function.

Added in version 2.0.

     class sqlalchemy.orm.MapperProperty

*inherits from* [sqlalchemy.sql.cache_key.HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey), `sqlalchemy.orm._DCAttributeOptions`, `sqlalchemy.orm.base._MappedAttribute`, [sqlalchemy.orm.base.InspectionAttrInfo](#sqlalchemy.orm.InspectionAttrInfo), `sqlalchemy.util.langhelpers.MemoizedSlots`

Represent a particular class attribute mapped by [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

The most common occurrences of [MapperProperty](#sqlalchemy.orm.MapperProperty) are the
mapped [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), which is represented in a mapping as
an instance of [ColumnProperty](#sqlalchemy.orm.ColumnProperty),
and a reference to another class produced by [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship),
represented in the mapping as an instance of
[Relationship](#sqlalchemy.orm.Relationship).

| Member Name | Description |
| --- | --- |
| cascade_iterator() | Iterate through instances related to the given instance for
a particular ‘cascade’, starting with this MapperProperty. |
| comparator | ThePropComparatorinstance that implements SQL
expression construction on behalf of this mapped attribute. |
| create_row_processor() | Produce row processing functions and append to the given
set of populators lists. |
| do_init() | Perform subclass-specific initialization post-mapper-creation
steps. |
| doc | optional documentation string |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisInspectionAttr. |
| init() | Called after all mappers are created to assemble
relationships between mappers and perform other post-mapper-creation
initialization steps. |
| instrument_class() | Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty. |
| is_property | Part of the InspectionAttr interface; states this object is a
mapper property. |
| key | name of class attribute |
| merge() | Merge the attribute represented by thisMapperPropertyfrom source to destination object. |
| parent | theMappermanaging this property. |
| post_instrument_class() | Perform instrumentation adjustments that need to occur
after init() has completed. |
| set_parent() | Set the parent mapper that references this MapperProperty. |
| setup() | Called by Query for the purposes of constructing a SQL statement. |

   method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)cascade_iterator(*type_:str*, *state:InstanceState[Any]*, *dict_:_InstanceDict*, *visited_states:Set[InstanceState[Any]]*, *halt_on:Callable[[InstanceState[Any]],bool]|None=None*) → Iterator[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[[object](#sqlalchemy.orm.InstanceState.object), [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)[Any], [InstanceState](#sqlalchemy.orm.InstanceState)[Any], _InstanceDict]]

Iterate through instances related to the given instance for
a particular ‘cascade’, starting with this MapperProperty.

Return an iterator3-tuples (instance, mapper, state).

Note that the ‘cascade’ collection on this MapperProperty is
checked first for the given type before cascade_iterator is called.

This method typically only applies to Relationship.

    property class_attribute: [InstrumentedAttribute](#sqlalchemy.orm.InstrumentedAttribute)[_T]

Return the class-bound descriptor corresponding to this
[MapperProperty](#sqlalchemy.orm.MapperProperty).

This is basically a `getattr()` call:

```
return getattr(self.parent.class_, self.key)
```

I.e. if this [MapperProperty](#sqlalchemy.orm.MapperProperty) were named `addresses`,
and the class to which it is mapped is `User`, this sequence
is possible:

```
>>> from sqlalchemy import inspect
>>> mapper = inspect(User)
>>> addresses_property = mapper.attrs.addresses
>>> addresses_property.class_attribute is User.addresses
True
>>> User.addresses.property is addresses_property
True
```

     attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)comparator: [PropComparator](#sqlalchemy.orm.PropComparator)[_T]

The [PropComparator](#sqlalchemy.orm.PropComparator) instance that implements SQL
expression construction on behalf of this mapped attribute.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)create_row_processor(*context:ORMCompileState*, *query_entity:_MapperEntity*, *path:AbstractEntityRegistry*, *mapper:Mapper[Any]*, *result:Result[Any]*, *adapter:ORMAdapter|None*, *populators:_PopulatorDict*) → None

Produce row processing functions and append to the given
set of populators lists.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)do_init() → None

Perform subclass-specific initialization post-mapper-creation
steps.

This is a template method called by the `MapperProperty`
object’s init() method.

    attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)doc: str | None

optional documentation string

    attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)info: _InfoType

Info dictionary associated with the object, allowing user-defined
data to be associated with this [InspectionAttr](#sqlalchemy.orm.InspectionAttr).

The dictionary is generated when first accessed.  Alternatively,
it can be specified as a constructor argument to the
[column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), or [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
functions.

See also

[QueryableAttribute.info](#sqlalchemy.orm.QueryableAttribute.info)

[SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info)

     method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)init() → None

Called after all mappers are created to assemble
relationships between mappers and perform other post-mapper-creation
initialization steps.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)instrument_class(*mapper:Mapper[Any]*) → None

Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty.

The MapperProperty here will typically call out to the
attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute,
and is called early in the mapper setup process.

The second step is typically the init_class_attribute step,
called from StrategizedProperty via the post_instrument_class()
hook.  This step assigns additional state to the InstrumentedAttribute
(specifically the “impl”) which has been determined after the
MapperProperty has determined what kind of persistence
management it needs to do (e.g. scalar, object, collection, etc).

    attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)is_property = True

Part of the InspectionAttr interface; states this object is a
mapper property.

    attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)key: str

name of class attribute

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)merge(*session:Session*, *source_state:InstanceState[Any]*, *source_dict:_InstanceDict*, *dest_state:InstanceState[Any]*, *dest_dict:_InstanceDict*, *load:bool*, *_recursive:Dict[Any,object]*, *_resolve_conflict_map:Dict[_IdentityKeyType[Any],object]*) → None

Merge the attribute represented by this `MapperProperty`
from source to destination object.

    attribute [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)parent: [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)[Any]

the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) managing this property.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)post_instrument_class(*mapper:Mapper[Any]*) → None

Perform instrumentation adjustments that need to occur
after init() has completed.

The given Mapper is the Mapper invoking the operation, which
may not be the same Mapper as self.parent in an inheritance
scenario; however, Mapper will always at least be a sub-mapper of
self.parent.

This method is typically used by StrategizedProperty, which delegates
it to LoaderStrategy.init_class_attribute() to perform final setup
on the class-bound InstrumentedAttribute.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)set_parent(*parent:Mapper[Any]*, *init:bool*) → None

Set the parent mapper that references this MapperProperty.

This method is overridden by some subclasses to perform extra
setup when the mapper is first known.

    method [sqlalchemy.orm.MapperProperty.](#sqlalchemy.orm.MapperProperty)setup(*context:ORMCompileState*, *query_entity:_MapperEntity*, *path:AbstractEntityRegistry*, *adapter:ORMAdapter|None*, ***kwargs:Any*) → None

Called by Query for the purposes of constructing a SQL statement.

Each MapperProperty associated with the target mapper processes the
statement referenced by the query context, adding columns and/or
criterion as appropriate.

     class sqlalchemy.orm.MappedSQLExpression

*inherits from* [sqlalchemy.orm.properties.ColumnProperty](#sqlalchemy.orm.ColumnProperty), `sqlalchemy.orm.base._DeclarativeMapped`

Declarative front-end for the [ColumnProperty](#sqlalchemy.orm.ColumnProperty) class.

Public constructor is the [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) function.

Changed in version 2.0: Added [MappedSQLExpression](#sqlalchemy.orm.MappedSQLExpression) as
a Declarative compatible subclass for [ColumnProperty](#sqlalchemy.orm.ColumnProperty).

See also

[MappedColumn](#sqlalchemy.orm.MappedColumn)

     class sqlalchemy.orm.InspectionAttrExtensionType

*inherits from* `enum.Enum`

Symbols indicating the type of extension that a
[InspectionAttr](#sqlalchemy.orm.InspectionAttr) is part of.

    class sqlalchemy.orm.NotExtension

*inherits from* [sqlalchemy.orm.base.InspectionAttrExtensionType](#sqlalchemy.orm.InspectionAttrExtensionType)

| Member Name | Description |
| --- | --- |
| NOT_EXTENSION | Symbol indicating anInspectionAttrthat’s
not part of sqlalchemy.ext. |

   attribute [sqlalchemy.orm.NotExtension.](#sqlalchemy.orm.NotExtension)NOT_EXTENSION = 'not_extension'

Symbol indicating an [InspectionAttr](#sqlalchemy.orm.InspectionAttr) that’s
not part of sqlalchemy.ext.

Is assigned to the [InspectionAttr.extension_type](#sqlalchemy.orm.InspectionAttr.extension_type)
attribute.

     function sqlalchemy.orm.merge_result(*query:Query[Any]*, *iterator:FrozenResult|Iterable[Sequence[Any]]|Iterable[object]*, *load:bool=True*) → [FrozenResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FrozenResult) | Iterable[Any]

Merge a result into the given [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object’s Session.

Deprecated since version 2.0: The [merge_result()](#sqlalchemy.orm.merge_result) function is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The function as well as the method on [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is superseded by the [merge_frozen_result()](#sqlalchemy.orm.merge_frozen_result) function. (Background on SQLAlchemy 2.0 at: [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html))

See [Query.merge_result()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.merge_result) for top-level documentation on this
function.

    function sqlalchemy.orm.merge_frozen_result(*session*, *statement*, *frozen_result*, *load=True*)

Merge a [FrozenResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FrozenResult) back into a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
returning a new [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object with [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent)
objects.

See the section [Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing) for an example.

See also

[Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#do-orm-execute-re-executing)

[Result.freeze()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.freeze)

[FrozenResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.FrozenResult)

     class sqlalchemy.orm.PropComparator

*inherits from* `sqlalchemy.orm.base.SQLORMOperations`, `typing.Generic`, [sqlalchemy.sql.expression.ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Defines SQL operations for ORM mapped attributes.

SQLAlchemy allows for operators to
be redefined at both the Core and ORM level.  [PropComparator](#sqlalchemy.orm.PropComparator)
is the base class of operator redefinition for ORM-level operations,
including those of [ColumnProperty](#sqlalchemy.orm.ColumnProperty),
[Relationship](#sqlalchemy.orm.Relationship), and [Composite](#sqlalchemy.orm.Composite).

User-defined subclasses of [PropComparator](#sqlalchemy.orm.PropComparator) may be created. The
built-in Python comparison and math operator methods, such as
`ColumnOperators.__eq__()`,
`ColumnOperators.__lt__()`, and
`ColumnOperators.__add__()`, can be overridden to provide
new operator behavior. The custom [PropComparator](#sqlalchemy.orm.PropComparator) is passed to
the [MapperProperty](#sqlalchemy.orm.MapperProperty) instance via the `comparator_factory`
argument. In each case,
the appropriate subclass of [PropComparator](#sqlalchemy.orm.PropComparator) should be used:

```
# definition of custom PropComparator subclasses

from sqlalchemy.orm.properties import (
    ColumnProperty,
    Composite,
    Relationship,
)

class MyColumnComparator(ColumnProperty.Comparator):
    def __eq__(self, other):
        return self.__clause_element__() == other

class MyRelationshipComparator(Relationship.Comparator):
    def any(self, expression):
        "define the 'any' operation"
        # ...

class MyCompositeComparator(Composite.Comparator):
    def __gt__(self, other):
        "redefine the 'greater than' operation"

        return sql.and_(
            *[
                a > b
                for a, b in zip(
                    self.__clause_element__().clauses,
                    other.__composite_values__(),
                )
            ]
        )

# application of custom PropComparator subclasses

from sqlalchemy.orm import column_property, relationship, composite
from sqlalchemy import Column, String

class SomeMappedClass(Base):
    some_column = column_property(
        Column("some_column", String),
        comparator_factory=MyColumnComparator,
    )

    some_relationship = relationship(
        SomeOtherClass, comparator_factory=MyRelationshipComparator
    )

    some_composite = composite(
        Column("a", String),
        Column("b", String),
        comparator_factory=MyCompositeComparator,
    )
```

Note that for column-level operator redefinition, it’s usually
simpler to define the operators at the Core level, using the
[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory) attribute.  See
[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators) for more detail.

See also

[Comparator](#sqlalchemy.orm.ColumnProperty.Comparator)

`Comparator`

`Comparator`

[ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

| Member Name | Description |
| --- | --- |
| __eq__() | Implement the==operator. |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| __ne__() | Implement the!=operator. |
| adapt_to_entity() | Return a copy of this PropComparator which will use the givenAliasedInspto produce corresponding expressions. |
| adapter | Produce a callable that adapts column expressions
to suit an aliased version of this comparator. |
| all_() | Produce anall_()clause against the
parent object. |
| and_() | Add additional criteria to the ON clause that’s represented by this
relationship attribute. |
| any() | Return a SQL expression representing true if this element
references a member which meets the given criterion. |
| any_() | Produce anany_()clause against the
parent object. |
| asc() | Produce aasc()clause against the
parent object. |
| between() | Produce abetween()clause against
the parent object, given the lower and upper range. |
| bitwise_and() | Produce a bitwise AND operation, typically via the&operator. |
| bitwise_lshift() | Produce a bitwise LSHIFT operation, typically via the<<operator. |
| bitwise_not() | Produce a bitwise NOT operation, typically via the~operator. |
| bitwise_or() | Produce a bitwise OR operation, typically via the|operator. |
| bitwise_rshift() | Produce a bitwise RSHIFT operation, typically via the>>operator. |
| bitwise_xor() | Produce a bitwise XOR operation, typically via the^operator, or#for PostgreSQL. |
| bool_op() | Return a custom boolean operator. |
| collate() | Produce acollate()clause against
the parent object, given the collation string. |
| concat() | Implement the ‘concat’ operator. |
| contains() | Implement the ‘contains’ operator. |
| desc() | Produce adesc()clause against the
parent object. |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| has() | Return a SQL expression representing true if this element
references a member which meets the given criterion. |
| icontains() | Implement theicontainsoperator, e.g. case insensitive
version ofColumnOperators.contains(). |
| iendswith() | Implement theiendswithoperator, e.g. case insensitive
version ofColumnOperators.endswith(). |
| ilike() | Implement theilikeoperator, e.g. case insensitive LIKE. |
| in_() | Implement theinoperator. |
| is_() | Implement theISoperator. |
| is_distinct_from() | Implement theISDISTINCTFROMoperator. |
| is_not() | Implement theISNOToperator. |
| is_not_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| isnot() | Implement theISNOToperator. |
| isnot_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| istartswith() | Implement theistartswithoperator, e.g. case insensitive
version ofColumnOperators.startswith(). |
| like() | Implement thelikeoperator. |
| match() | Implements a database-specific ‘match’ operator. |
| not_ilike() | implement theNOTILIKEoperator. |
| not_in() | implement theNOTINoperator. |
| not_like() | implement theNOTLIKEoperator. |
| notilike() | implement theNOTILIKEoperator. |
| notin_() | implement theNOTINoperator. |
| notlike() | implement theNOTLIKEoperator. |
| nulls_first() | Produce anulls_first()clause against the
parent object. |
| nulls_last() | Produce anulls_last()clause against the
parent object. |
| nullsfirst() | Produce anulls_first()clause against the
parent object. |
| nullslast() | Produce anulls_last()clause against the
parent object. |
| of_type() | Redefine this object in terms of a polymorphic subclass,with_polymorphic()construct, oraliased()construct. |
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| property | Return theMapperPropertyassociated with thisPropComparator. |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| startswith() | Implement thestartswithoperator. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |

   method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)__eq__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__eq__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `==` operator.

In a column context, produces the clause `a = b`.
If the target is `None`, produces `a IS NULL`.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)__le__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)__lt__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)__ne__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__ne__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)adapt_to_entity(*adapt_to_entity:AliasedInsp[Any]*) → [PropComparator](#sqlalchemy.orm.PropComparator)[_T_co]

Return a copy of this PropComparator which will use the given
[AliasedInsp](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedInsp) to produce corresponding expressions.

    attribute [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)adapter

Produce a callable that adapts column expressions
to suit an aliased version of this comparator.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)all_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.all_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce an [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) clause against the
parent object.

See the documentation for [all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.all_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.all_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.all_) method with the **legacy**
version of this method, the [Comparator.all()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.all)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)and_(**criteria:_ColumnExpressionArgument[bool]*) → [PropComparator](#sqlalchemy.orm.PropComparator)[bool]

Add additional criteria to the ON clause that’s represented by this
relationship attribute.

E.g.:

```
stmt = select(User).join(
    User.addresses.and_(Address.email_address != "foo")
)

stmt = select(User).options(
    joinedload(User.addresses.and_(Address.email_address != "foo"))
)
```

Added in version 1.4.

See also

[Combining Relationship with Custom ON Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-join-on-augmented)

[Adding Criteria to loader options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#loader-option-criteria)

[with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)any(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Return a SQL expression representing true if this element
references a member which meets the given criterion.

The usual implementation of `any()` is
`Comparator.any()`.

  Parameters:

- **criterion** – an optional ClauseElement formulated against the
  member class’ table or attributes.
- ****kwargs** – key/value pairs corresponding to member class
  attribute names which will be compared via equality to the
  corresponding values.

      method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)any_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.any_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce an [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) clause against the
parent object.

See the documentation for [any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.any_) for examples.

Note

be sure to not confuse the newer
[ColumnOperators.any_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.any_) method with the **legacy**
version of this method, the [Comparator.any()](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY.Comparator.any)
method that’s specific to [ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), which uses a
different calling style.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)asc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) clause against the
parent object.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_and(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_lshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_not() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_or(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_rshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bitwise_xor(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Return a custom boolean operator.

This method is shorthand for calling
[Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) and passing the
[Operators.op.is_comparison](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.is_comparison)
flag with True.    A key advantage to using [Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op)
is that when using column constructs, the “boolean” nature of the
returned expression will be present for [PEP 484](https://peps.python.org/pep-0484/) purposes.

See also

[Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)collate(*collation:str*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)concat(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘contains’ operator.

Produces a LIKE expression that tests against a match for the middle
of a string value:

```
column LIKE '%' || <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.contains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.contains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.contains.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.contains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.contains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.contains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.contains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)desc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) clause against the
parent object.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)distinct() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘endswith’ operator.

Produces a LIKE expression that tests against a match for the end
of a string value:

```
column LIKE '%' || <other>
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.endswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.endswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.endswith.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.endswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.endswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.endswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE '%' || :param ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.endswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith)

[ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)has(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Return a SQL expression representing true if this element
references a member which meets the given criterion.

The usual implementation of `has()` is
`Comparator.has()`.

  Parameters:

- **criterion** – an optional ClauseElement formulated against the
  member class’ table or attributes.
- ****kwargs** – key/value pairs corresponding to member class
  attribute names which will be compared via equality to the
  corresponding values.

      method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.icontains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `icontains` operator, e.g. case insensitive
version of [ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains).

Produces a LIKE expression that tests against an insensitive match
for the middle of a string value:

```
lower(column) LIKE '%' || lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.icontains("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.icontains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.icontains.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.icontains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.icontains.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.icontains("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.icontains("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.contains.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains.params.autoescape):
  ```
  somecolumn.icontains("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.iendswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `iendswith` operator, e.g. case insensitive
version of [ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith).

Produces a LIKE expression that tests against an insensitive match
for the end of a string value:

```
lower(column) LIKE '%' || lower(<other>)
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.iendswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.iendswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.iendswith.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.iendswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.iendswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.iendswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE '%' || lower(:param) ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.iendswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.iendswith.params.autoescape):
  ```
  somecolumn.endswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `ilike` operator, e.g. case insensitive LIKE.

In a column context, produces an expression either of the form:

```
lower(a) LIKE lower(other)
```

Or on backends that support the ILIKE operator:

```
a ILIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.ilike("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.ilike("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)in_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `in` operator.

In a column context, produces the clause `column IN <other>`.

The given parameter `other` may be:

- A list of literal values,
  e.g.:
  ```
  stmt.where(column.in_([1, 2, 3]))
  ```
  In this calling form, the list of items is converted to a set of
  bound parameters the same length as the list given:
  ```
  WHERE COL IN (?, ?, ?)
  ```
- A list of tuples may be provided if the comparison is against a
  [tuple_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.tuple_) containing multiple expressions:
  ```
  from sqlalchemy import tuple_
  stmt.where(tuple_(col1, col2).in_([(1, 10), (2, 20), (3, 30)]))
  ```
- An empty list,
  e.g.:
  ```
  stmt.where(column.in_([]))
  ```
  In this calling form, the expression renders an “empty set”
  expression.  These expressions are tailored to individual backends
  and are generally trying to get an empty SELECT statement as a
  subquery.  Such as on SQLite, the expression is:
  ```
  WHERE col IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Changed in version 1.4: empty IN expressions now use an
  execution-time generated SELECT subquery in all cases.
- A bound parameter, e.g. [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam), may be used if it
  includes the [bindparam.expanding](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam.params.expanding) flag:
  ```
  stmt.where(column.in_(bindparam("value", expanding=True)))
  ```
  In this calling form, the expression renders a special non-SQL
  placeholder expression that looks like:
  ```
  WHERE COL IN ([EXPANDING_value])
  ```
  This placeholder expression is intercepted at statement execution
  time to be converted into the variable number of bound parameter
  form illustrated earlier.   If the statement were executed as:
  ```
  connection.execute(stmt, {"value": [1, 2, 3]})
  ```
  The database would be passed a bound parameter for each value:
  ```
  WHERE COL IN (?, ?, ?)
  ```
  Added in version 1.2: added “expanding” bound parameters
  If an empty list is passed, a special “empty list” expression,
  which is specific to the database in use, is rendered.  On
  SQLite this would be:
  ```
  WHERE COL IN (SELECT 1 FROM (SELECT 1) WHERE 1!=1)
  ```
  Added in version 1.3: “expanding” bound parameters now support
  empty lists
- a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct, which is usually a
  correlated scalar select:
  ```
  stmt.where(
      column.in_(select(othertable.c.y).where(table.c.x == othertable.c.x))
  )
  ```
  In this calling form, [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) renders as given:
  ```
  WHERE COL IN (SELECT othertable.y
  FROM othertable WHERE othertable.x = table.x)
  ```

  Parameters:

**other** – a list of literals, a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
construct, or a [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) construct that includes the
[bindparam.expanding](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam.params.expanding) flag set to True.

      method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)is_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)is_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)is_not(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)is_not_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)isnot(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT` operator.

Normally, `IS NOT` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS NOT` may be desirable if comparing to boolean values
on certain platforms.

Changed in version 1.4: The `is_not()` operator is renamed from
`isnot()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)isnot_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.istartswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `istartswith` operator, e.g. case insensitive
version of [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith).

Produces a LIKE expression that tests against an insensitive
match for the start of a string value:

```
lower(column) LIKE lower(<other>) || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.istartswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.istartswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.istartswith.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.escape) parameter will
establish a given character as an escape character which can be of
use when the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.istartswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.istartswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.istartswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  lower(somecolumn) LIKE lower(:param) || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.istartswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.istartswith.params.autoescape):
  ```
  somecolumn.istartswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `like` operator.

In a column context, produces the expression:

```
a LIKE other
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.like("%foobar%"))
```

   Parameters:

- **other** – expression to be compared
- **escape** –
  optional escape character, renders the `ESCAPE`
  keyword, e.g.:
  ```
  somecolumn.like("foo/%bar", escape="/")
  ```

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘match’ operator.

[ColumnOperators.match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.match) attempts to resolve to
a MATCH-like function or operator provided by the backend.
Examples include:

- PostgreSQL - renders `x @@ plainto_tsquery(y)`
  > Changed in version 2.0: `plainto_tsquery()` is used instead
  > of `to_tsquery()` for PostgreSQL now; for compatibility with
  > other forms, see [Full Text Search](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-match).
- MySQL - renders `MATCH (x) AGAINST (y IN BOOLEAN MODE)`
  See also
  [match](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.match) - MySQL specific construct with
  additional features.
- Oracle Database - renders `CONTAINS(x, y)`
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “MATCH”.  This is compatible with SQLite, for
  example.

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)not_in(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)notin_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notin_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notin_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT IN` operator.

This is equivalent to using negation with
[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_), i.e. `~x.in_(y)`.

In the case that `other` is an empty sequence, the compiler
produces an “empty not in” expression.   This defaults to the
expression “1 = 1” to produce true in all cases.  The
[create_engine.empty_in_strategy](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.empty_in_strategy) may be used to
alter this behavior.

Changed in version 1.4: The `not_in()` operator is renamed from
`notin_()` in previous releases.  The previous name remains
available for backwards compatibility.

Changed in version 1.2: The [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) and
[ColumnOperators.not_in()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_in) operators
now produce a “static” expression for an empty IN sequence
by default.

See also

[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)nulls_first() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)nulls_last() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)nullsfirst() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)nullslast() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)of_type(*class_:_EntityType[Any]*) → [PropComparator](#sqlalchemy.orm.PropComparator)[_T_co]

Redefine this object in terms of a polymorphic subclass,
[with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) construct, or [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct.

Returns a new PropComparator from which further criterion can be
evaluated.

e.g.:

```
query.join(Company.employees.of_type(Engineer)).filter(
    Engineer.name == "foo"
)
```

   Parameters:

**class_** – a class or mapper indicating that criterion will be
against this specific subclass.

See also

[Using Relationship to join between aliased targets](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joining-relationships-aliased) - in the
[ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Joining to specific sub-types or with_polymorphic() entities](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#inheritance-of-type)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

*inherited from the* [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Produce a generic operator function.

e.g.:

```
somecolumn.op("*")(5)
```

produces:

```
somecolumn * 5
```

This function can also be used to make bitwise operators explicit. For
example:

```
somecolumn.op("&")(0xFF)
```

is a bitwise AND of the value in `somecolumn`.

  Parameters:

- **opstring** – a string which will be output as the infix operator
  between this element and the expression passed to the
  generated function.
- **precedence** –
  precedence which the database is expected to apply
  to the operator in SQL expressions. This integer value acts as a hint
  for the SQL compiler to know when explicit parenthesis should be
  rendered around a particular operation. A lower number will cause the
  expression to be parenthesized when applied against another operator
  with higher precedence. The default value of `0` is lower than all
  operators except for the comma (`,`) and `AS` operators. A value
  of 100 will be higher or equal to all operators, and -100 will be
  lower than or equal to all operators.
  See also
  [I’m using op() to generate a custom operator and my parenthesis are not coming out correctly](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-op-parenthesis) - detailed description
  of how the SQLAlchemy SQL compiler renders parenthesis
- **is_comparison** –
  legacy; if True, the operator will be considered
  as a “comparison” operator, that is which evaluates to a boolean
  true/false value, like `==`, `>`, etc.  This flag is provided
  so that ORM relationships can establish that the operator is a
  comparison operator when used in a custom join condition.
  Using the `is_comparison` parameter is superseded by using the
  [Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op) method instead;  this more succinct
  operator sets this parameter automatically, but also provides
  correct [PEP 484](https://peps.python.org/pep-0484/) typing support as the returned object will
  express a “boolean” datatype, i.e. `BinaryExpression[bool]`.
- **return_type** – a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) class or object that will
  force the return type of an expression produced by this operator
  to be of that type.   By default, operators that specify
  [Operators.op.is_comparison](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op.params.is_comparison) will resolve to
  [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean), and those that do not will be of the same
  type as the left-hand operand.
- **python_impl** –
  an optional Python function that can evaluate
  two Python values in the same way as this operator works when
  run on the database server.  Useful for in-Python SQL expression
  evaluation functions, such as for ORM hybrid attributes, and the
  ORM “evaluator” used to match objects in a session after a multi-row
  update or delete.
  e.g.:
  ```
  >>> expr = column("x").op("+", python_impl=lambda a, b: a + b)("y")
  ```
  The operator for the above expression will also work for non-SQL
  left and right objects:
  ```
  >>> expr.operator(5, 10)
  15
  ```
  Added in version 2.0.

See also

[Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-operator)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.operate) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

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

      attribute [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)property

Return the [MapperProperty](#sqlalchemy.orm.MapperProperty) associated with this
[PropComparator](#sqlalchemy.orm.PropComparator).

Return values here will commonly be instances of
[ColumnProperty](#sqlalchemy.orm.ColumnProperty) or [Relationship](#sqlalchemy.orm.Relationship).

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp match’ operator.

E.g.:

```
stmt = select(table.c.some_column).where(
    table.c.some_column.regexp_match("^(b|c)")
)
```

[ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match) attempts to resolve to
a REGEXP-like function or operator provided by the backend, however
the specific regular expression syntax and flags available are
**not backend agnostic**.

Examples include:

- PostgreSQL - renders `x ~ y` or `x !~ y` when negated.
- Oracle Database - renders `REGEXP_LIKE(x, y)`
- SQLite - uses SQLite’s `REGEXP` placeholder operator and calls into
  the Python `re.match()` builtin.
- other backends may provide special implementations.
- Backends without any special implementation will emit
  the operator as “REGEXP” or “NOT REGEXP”.  This is compatible with
  SQLite and MySQL, for example.

Regular expression support is currently implemented for Oracle
Database, PostgreSQL, MySQL and MariaDB.  Partial support is available
for SQLite.  Support among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.
  When using the ignore case flag ‘i’ in PostgreSQL, the ignore case
  regexp match operator `~*` or `!~*` will be used.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implements a database-specific ‘regexp replace’ operator.

E.g.:

```
stmt = select(
    table.c.some_column.regexp_replace("b(..)", "XY", flags="g")
)
```

[ColumnOperators.regexp_replace()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_replace) attempts to resolve to
a REGEXP_REPLACE-like function provided by the backend, that
usually emit the function `REGEXP_REPLACE()`.  However,
the specific regular expression syntax and flags available are
**not backend agnostic**.

Regular expression replacement support is currently implemented for
Oracle Database, PostgreSQL, MySQL 8 or greater and MariaDB.  Support
among third-party dialects may vary.

  Parameters:

- **pattern** – The regular expression pattern string or column
  clause.
- **pattern** – The replacement string or column clause.
- **flags** – Any regular expression string flags to apply, passed as
  plain Python string only.  These flags are backend specific.
  Some backends, like PostgreSQL and MariaDB, may alternatively
  specify the flags as part of the pattern.

Added in version 1.4.

Changed in version 1.4.48,: 2.0.18  Note that due to an implementation
error, the “flags” parameter previously accepted SQL expression
objects such as column expressions in addition to plain Python
strings.   This implementation did not work correctly with caching
and was removed; strings only should be passed for the “flags”
parameter, as these flags are rendered as literal inline values
within SQL expressions.

See also

[ColumnOperators.regexp_match()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.regexp_match)

     method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.reverse_operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.reverse_operate) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.orm.PropComparator.operate).

    method [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.startswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `startswith` operator.

Produces a LIKE expression that tests against a match for the start
of a string value:

```
column LIKE <other> || '%'
```

E.g.:

```
stmt = select(sometable).where(sometable.c.column.startswith("foobar"))
```

Since the operator uses `LIKE`, wildcard characters
`"%"` and `"_"` that are present inside the <other> expression
will behave like wildcards as well.   For literal string
values, the [ColumnOperators.startswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag
may be set to `True` to apply escaping to occurrences of these
characters within the string value so that they match as themselves
and not as wildcard characters.  Alternatively, the
[ColumnOperators.startswith.escape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith.params.escape) parameter will establish
a given character as an escape character which can be of use when
the target expression is not a literal string.

  Parameters:

- **other** – expression to be compared.   This is usually a plain
  string value, but can also be an arbitrary SQL expression.  LIKE
  wildcard characters `%` and `_` are not escaped by default unless
  the [ColumnOperators.startswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape) flag is
  set to True.
- **autoescape** –
  boolean; when True, establishes an escape character
  within the LIKE expression, then applies it to all occurrences of
  `"%"`, `"_"` and the escape character itself within the
  comparison value, which is assumed to be a literal string and not a
  SQL expression.
  An expression such as:
  ```
  somecolumn.startswith("foo%bar", autoescape=True)
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '/'
  ```
  With the value of `:param` as `"foo/%bar"`.
- **escape** –
  a character which when given will render with the
  `ESCAPE` keyword to establish that character as the escape
  character.  This character can then be placed preceding occurrences
  of `%` and `_` to allow them to act as themselves and not
  wildcard characters.
  An expression such as:
  ```
  somecolumn.startswith("foo/%bar", escape="^")
  ```
  Will render as:
  ```
  somecolumn LIKE :param || '%' ESCAPE '^'
  ```
  The parameter may also be combined with
  [ColumnOperators.startswith.autoescape](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.startswith.params.autoescape):
  ```
  somecolumn.startswith("foo%bar^bat", escape="^", autoescape=True)
  ```
  Where above, the given literal parameter will be converted to
  `"foo^%bar^^bat"` before being passed to the database.

See also

[ColumnOperators.endswith()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.endswith)

[ColumnOperators.contains()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.contains)

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     attribute [sqlalchemy.orm.PropComparator.](#sqlalchemy.orm.PropComparator)timetuple = None

*inherited from the* [ColumnOperators.timetuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

     class sqlalchemy.orm.Relationship

*inherits from* [sqlalchemy.orm.RelationshipProperty](#sqlalchemy.orm.RelationshipProperty), `sqlalchemy.orm.base._DeclarativeMapped`

Describes an object property that holds a single item or list
of items that correspond to a related database table.

Public constructor is the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function.

See also

[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

Changed in version 2.0: Added [Relationship](#sqlalchemy.orm.Relationship) as a Declarative
compatible subclass for [RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

     class sqlalchemy.orm.RelationshipDirection

*inherits from* `enum.Enum`

enumeration which indicates the ‘direction’ of a
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

[RelationshipDirection](#sqlalchemy.orm.RelationshipDirection) is accessible from the
`Relationship.direction` attribute of
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

| Member Name | Description |
| --- | --- |
| MANYTOMANY | Indicates the many-to-many direction for arelationship(). |
| MANYTOONE | Indicates the many-to-one direction for arelationship(). |
| ONETOMANY | Indicates the one-to-many direction for arelationship(). |

   attribute [sqlalchemy.orm.RelationshipDirection.](#sqlalchemy.orm.RelationshipDirection)MANYTOMANY = 3

Indicates the many-to-many direction for a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

This symbol is typically used by the internals but may be exposed within
certain API features.

    attribute [sqlalchemy.orm.RelationshipDirection.](#sqlalchemy.orm.RelationshipDirection)MANYTOONE = 2

Indicates the many-to-one direction for a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

This symbol is typically used by the internals but may be exposed within
certain API features.

    attribute [sqlalchemy.orm.RelationshipDirection.](#sqlalchemy.orm.RelationshipDirection)ONETOMANY = 1

Indicates the one-to-many direction for a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

This symbol is typically used by the internals but may be exposed within
certain API features.

     class sqlalchemy.orm.RelationshipProperty

*inherits from* `sqlalchemy.orm._IntrospectsAnnotations`, `sqlalchemy.orm.StrategizedProperty`, [sqlalchemy.log.Identified](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.log.Identified)

Describes an object property that holds a single item or list
of items that correspond to a related database table.

Public constructor is the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function.

See also

[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

| Member Name | Description |
| --- | --- |
| __eq__() | Implement the==operator. |
| __init__() | Construction ofComparatoris internal to the ORM’s attribute mechanics. |
| __ne__() | Implement the!=operator. |
| adapt_to_entity() | Return a copy of this PropComparator which will use the givenAliasedInspto produce corresponding expressions. |
| and_() | Add AND criteria. |
| any() | Produce an expression that tests a collection against
particular criterion, using EXISTS. |
| contains() | Return a simple expression that tests a collection for
containment of a particular item. |
| entity | The target entity referred to by thisComparator. |
| has() | Produce an expression that tests a scalar reference against
particular criterion, using EXISTS. |
| in_() | Produce an IN clause - this is not implemented
forrelationship()-based attributes at this time. |
| mapper | The targetMapperreferred to by thisComparator. |
| of_type() | Redefine this object in terms of a polymorphic subclass. |
| cascade_iterator() | Iterate through instances related to the given instance for
a particular ‘cascade’, starting with this MapperProperty. |
| declarative_scan() | Perform class-specific initialization at early declarative scanning
time. |
| do_init() | Perform subclass-specific initialization post-mapper-creation
steps. |
| entity | Return the target mapped entity, which is an inspect() of the
class or aliased class that is referenced by thisRelationshipProperty. |
| instrument_class() | Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty. |
| mapper | Return the targetedMapperfor thisRelationshipProperty. |
| merge() | Merge the attribute represented by thisMapperPropertyfrom source to destination object. |

   class Comparator

*inherits from* `sqlalchemy.util.langhelpers.MemoizedSlots`, [sqlalchemy.orm.PropComparator](#sqlalchemy.orm.PropComparator)

Produce boolean, comparison, and other operators for
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty) attributes.

See the documentation for [PropComparator](#sqlalchemy.orm.PropComparator) for a brief
overview of ORM level operator definition.

See also

[PropComparator](#sqlalchemy.orm.PropComparator)

[Comparator](#sqlalchemy.orm.ColumnProperty.Comparator)

[ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

[Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators)

[TypeEngine.comparator_factory](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.comparator_factory)

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)__eq__(*other:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Implement the `==` operator.

In a many-to-one context, such as:

```
MyClass.some_prop == <some object>
```

this will typically produce a
clause such as:

```
mytable.related_id == <some id>
```

Where `<some id>` is the primary key of the given
object.

The `==` operator provides partial functionality for non-
many-to-one comparisons:

- Comparisons against collections are not supported.
  Use `Comparator.contains()`.
- Compared to a scalar one-to-many, will produce a
  clause that compares the target columns in the parent to
  the given target.
- Compared to a scalar many-to-many, an alias
  of the association table will be rendered as
  well, forming a natural join that is part of the
  main body of the query. This will not work for
  queries that go beyond simple AND conjunctions of
  comparisons, such as those which use OR. Use
  explicit joins, outerjoins, or
  `Comparator.has()` for
  more comprehensive non-many-to-one scalar
  membership tests.
- Comparisons against `None` given in a one-to-many
  or many-to-many context produce a NOT EXISTS clause.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)__init__(*prop:RelationshipProperty[_PT]*, *parentmapper:_InternalEntityType[Any]*, *adapt_to_entity:AliasedInsp[Any]|None=None*, *of_type:_EntityType[_PT]|None=None*, *extra_criteria:Tuple[ColumnElement[bool],...]=()*)

Construction of [Comparator](#sqlalchemy.orm.RelationshipProperty.Comparator)
is internal to the ORM’s attribute mechanics.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)__ne__(*other:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Implement the `!=` operator.

In a many-to-one context, such as:

```
MyClass.some_prop != <some object>
```

This will typically produce a clause such as:

```
mytable.related_id != <some id>
```

Where `<some id>` is the primary key of the
given object.

The `!=` operator provides partial functionality for non-
many-to-one comparisons:

- Comparisons against collections are not supported.
  Use
  `Comparator.contains()`
  in conjunction with [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_).
- Compared to a scalar one-to-many, will produce a
  clause that compares the target columns in the parent to
  the given target.
- Compared to a scalar many-to-many, an alias
  of the association table will be rendered as
  well, forming a natural join that is part of the
  main body of the query. This will not work for
  queries that go beyond simple AND conjunctions of
  comparisons, such as those which use OR. Use
  explicit joins, outerjoins, or
  `Comparator.has()` in
  conjunction with [not_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.not_) for
  more comprehensive non-many-to-one scalar
  membership tests.
- Comparisons against `None` given in a one-to-many
  or many-to-many context produce an EXISTS clause.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)adapt_to_entity(*adapt_to_entity:AliasedInsp[Any]*) → [RelationshipProperty.Comparator](#sqlalchemy.orm.RelationshipProperty.Comparator)[Any]

Return a copy of this PropComparator which will use the given
[AliasedInsp](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedInsp) to produce corresponding expressions.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)and_(**criteria:_ColumnExpressionArgument[bool]*) → [PropComparator](#sqlalchemy.orm.PropComparator)[Any]

Add AND criteria.

See [PropComparator.and_()](#sqlalchemy.orm.PropComparator.and_) for an example.

Added in version 1.4.

     method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)any(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Produce an expression that tests a collection against
particular criterion, using EXISTS.

An expression like:

```
session.query(MyClass).filter(
    MyClass.somereference.any(SomeRelated.x == 2)
)
```

Will produce a query like:

```
SELECT * FROM my_table WHERE
EXISTS (SELECT 1 FROM related WHERE related.my_id=my_table.id
AND related.x=2)
```

Because `Comparator.any()` uses
a correlated subquery, its performance is not nearly as
good when compared against large target tables as that of
using a join.

`Comparator.any()` is particularly
useful for testing for empty collections:

```
session.query(MyClass).filter(~MyClass.somereference.any())
```

will produce:

```
SELECT * FROM my_table WHERE
NOT (EXISTS (SELECT 1 FROM related WHERE
related.my_id=my_table.id))
```

`Comparator.any()` is only
valid for collections, i.e. a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
that has `uselist=True`.  For scalar references,
use `Comparator.has()`.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)contains(*other:_ColumnExpressionArgument[Any]*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Return a simple expression that tests a collection for
containment of a particular item.

`Comparator.contains()` is
only valid for a collection, i.e. a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) that implements
one-to-many or many-to-many with `uselist=True`.

When used in a simple one-to-many context, an
expression like:

```
MyClass.contains(other)
```

Produces a clause like:

```
mytable.id == <some id>
```

Where `<some id>` is the value of the foreign key
attribute on `other` which refers to the primary
key of its parent object. From this it follows that
`Comparator.contains()` is
very useful when used with simple one-to-many
operations.

For many-to-many operations, the behavior of
`Comparator.contains()`
has more caveats. The association table will be
rendered in the statement, producing an “implicit”
join, that is, includes multiple tables in the FROM
clause which are equated in the WHERE clause:

```
query(MyClass).filter(MyClass.contains(other))
```

Produces a query like:

```
SELECT * FROM my_table, my_association_table AS
my_association_table_1 WHERE
my_table.id = my_association_table_1.parent_id
AND my_association_table_1.child_id = <some id>
```

Where `<some id>` would be the primary key of
`other`. From the above, it is clear that
`Comparator.contains()`
will **not** work with many-to-many collections when
used in queries that move beyond simple AND
conjunctions, such as multiple
`Comparator.contains()`
expressions joined by OR. In such cases subqueries or
explicit “outer joins” will need to be used instead.
See `Comparator.any()` for
a less-performant alternative using EXISTS, or refer
to [Query.outerjoin()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.outerjoin)
as well as [Joins](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joins)
for more details on constructing outer joins.

kwargs may be ignored by this operator but are required for API
conformance.

    attribute [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)entity: _InternalEntityType[_PT]

The target entity referred to by this
[Comparator](#sqlalchemy.orm.RelationshipProperty.Comparator).

This is either a [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) or [AliasedInsp](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedInsp)
object.

This is the “target” or “remote” side of the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)has(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Produce an expression that tests a scalar reference against
particular criterion, using EXISTS.

An expression like:

```
session.query(MyClass).filter(
    MyClass.somereference.has(SomeRelated.x == 2)
)
```

Will produce a query like:

```
SELECT * FROM my_table WHERE
EXISTS (SELECT 1 FROM related WHERE
related.id==my_table.related_id AND related.x=2)
```

Because `Comparator.has()` uses
a correlated subquery, its performance is not nearly as
good when compared against large target tables as that of
using a join.

`Comparator.has()` is only
valid for scalar references, i.e. a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
that has `uselist=False`.  For collection references,
use `Comparator.any()`.

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)in_(*other:Any*) → NoReturn

Produce an IN clause - this is not implemented
for [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-based attributes at this time.

    attribute [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)mapper: [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)[_PT]

The target [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) referred to by this
[Comparator](#sqlalchemy.orm.RelationshipProperty.Comparator).

This is the “target” or “remote” side of the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

    method [sqlalchemy.orm.RelationshipProperty.Comparator.](#sqlalchemy.orm.RelationshipProperty.Comparator)of_type(*class_:_EntityType[Any]*) → [PropComparator](#sqlalchemy.orm.PropComparator)[_PT]

Redefine this object in terms of a polymorphic subclass.

See [PropComparator.of_type()](#sqlalchemy.orm.PropComparator.of_type) for an example.

     property cascade: [CascadeOptions](#sqlalchemy.orm.CascadeOptions)

Return the current cascade setting for this
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

    method [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)cascade_iterator(*type_:str*, *state:InstanceState[Any]*, *dict_:_InstanceDict*, *visited_states:Set[InstanceState[Any]]*, *halt_on:Callable[[InstanceState[Any]],bool]|None=None*) → Iterator[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[Any, [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)[Any], [InstanceState](#sqlalchemy.orm.InstanceState)[Any], _InstanceDict]]

Iterate through instances related to the given instance for
a particular ‘cascade’, starting with this MapperProperty.

Return an iterator3-tuples (instance, mapper, state).

Note that the ‘cascade’ collection on this MapperProperty is
checked first for the given type before cascade_iterator is called.

This method typically only applies to Relationship.

    method [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)declarative_scan(*decl_scan:_ClassScanMapperConfig*, *registry:_RegistryType*, *cls:Type[Any]*, *originating_module:str|None*, *key:str*, *mapped_container:Type[Mapped[Any]]|None*, *annotation:_AnnotationScanType|None*, *extracted_mapped_annotation:_AnnotationScanType|None*, *is_dataclass_field:bool*) → None

Perform class-specific initialization at early declarative scanning
time.

Added in version 2.0.

     method [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)do_init() → None

Perform subclass-specific initialization post-mapper-creation
steps.

This is a template method called by the `MapperProperty`
object’s init() method.

    attribute [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)entity

Return the target mapped entity, which is an inspect() of the
class or aliased class that is referenced by this
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

    method [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)instrument_class(*mapper:Mapper[Any]*) → None

Hook called by the Mapper to the property to initiate
instrumentation of the class attribute managed by this
MapperProperty.

The MapperProperty here will typically call out to the
attributes module to set up an InstrumentedAttribute.

This step is the first of two steps to set up an InstrumentedAttribute,
and is called early in the mapper setup process.

The second step is typically the init_class_attribute step,
called from StrategizedProperty via the post_instrument_class()
hook.  This step assigns additional state to the InstrumentedAttribute
(specifically the “impl”) which has been determined after the
MapperProperty has determined what kind of persistence
management it needs to do (e.g. scalar, object, collection, etc).

    attribute [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)mapper

Return the targeted [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) for this
[RelationshipProperty](#sqlalchemy.orm.RelationshipProperty).

    method [sqlalchemy.orm.RelationshipProperty.](#sqlalchemy.orm.RelationshipProperty)merge(*session:Session*, *source_state:InstanceState[Any]*, *source_dict:_InstanceDict*, *dest_state:InstanceState[Any]*, *dest_dict:_InstanceDict*, *load:bool*, *_recursive:Dict[Any,object]*, *_resolve_conflict_map:Dict[_IdentityKeyType[Any],object]*) → None

Merge the attribute represented by this `MapperProperty`
from source to destination object.

     class sqlalchemy.orm.SQLORMExpression

*inherits from* `sqlalchemy.orm.base.SQLORMOperations`, [sqlalchemy.sql.expression.SQLColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.SQLColumnExpression), `sqlalchemy.util.langhelpers.TypingOnly`

A type that may be used to indicate any ORM-level attribute or
object that acts in place of one, in the context of SQL expression
construction.

[SQLORMExpression](#sqlalchemy.orm.SQLORMExpression) extends from the Core
[SQLColumnExpression](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.SQLColumnExpression) to add additional SQL methods that are ORM
specific, such as [PropComparator.of_type()](#sqlalchemy.orm.PropComparator.of_type), and is part of the bases
for [InstrumentedAttribute](#sqlalchemy.orm.InstrumentedAttribute). It may be used in [PEP 484](https://peps.python.org/pep-0484/) typing to
indicate arguments or return values that should behave as ORM-level
attribute expressions.

Added in version 2.0.0b4.

     class sqlalchemy.orm.Synonym

*inherits from* [sqlalchemy.orm.descriptor_props.SynonymProperty](#sqlalchemy.orm.SynonymProperty), `sqlalchemy.orm.base._DeclarativeMapped`

Declarative front-end for the [SynonymProperty](#sqlalchemy.orm.SynonymProperty) class.

Public constructor is the [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym) function.

Changed in version 2.0: Added [Synonym](#sqlalchemy.orm.Synonym) as a Declarative
compatible subclass for [SynonymProperty](#sqlalchemy.orm.SynonymProperty)

See also

[Synonyms](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#synonyms) - Overview of synonyms

     class sqlalchemy.orm.SynonymProperty

*inherits from* `sqlalchemy.orm.descriptor_props.DescriptorProperty`

Denote an attribute name as a synonym to a mapped property,
in that the attribute will mirror the value and expression behavior
of another attribute.

[Synonym](#sqlalchemy.orm.Synonym) is constructed using the [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym)
function.

See also

[Synonyms](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#synonyms) - Overview of synonyms

| Member Name | Description |
| --- | --- |
| doc | optional documentation string |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisInspectionAttr. |
| key | name of class attribute |
| parent | theMappermanaging this property. |
| set_parent() | Set the parent mapper that references this MapperProperty. |

   attribute [sqlalchemy.orm.SynonymProperty.](#sqlalchemy.orm.SynonymProperty)doc

*inherited from the* `DescriptorProperty.doc` *attribute of* `DescriptorProperty`

optional documentation string

    attribute [sqlalchemy.orm.SynonymProperty.](#sqlalchemy.orm.SynonymProperty)info

*inherited from the* [MapperProperty.info](#sqlalchemy.orm.MapperProperty.info) *attribute of* [MapperProperty](#sqlalchemy.orm.MapperProperty)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [InspectionAttr](#sqlalchemy.orm.InspectionAttr).

The dictionary is generated when first accessed.  Alternatively,
it can be specified as a constructor argument to the
[column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), or [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
functions.

See also

[QueryableAttribute.info](#sqlalchemy.orm.QueryableAttribute.info)

[SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info)

     attribute [sqlalchemy.orm.SynonymProperty.](#sqlalchemy.orm.SynonymProperty)key

*inherited from the* [MapperProperty.key](#sqlalchemy.orm.MapperProperty.key) *attribute of* [MapperProperty](#sqlalchemy.orm.MapperProperty)

name of class attribute

    attribute [sqlalchemy.orm.SynonymProperty.](#sqlalchemy.orm.SynonymProperty)parent

*inherited from the* [MapperProperty.parent](#sqlalchemy.orm.MapperProperty.parent) *attribute of* [MapperProperty](#sqlalchemy.orm.MapperProperty)

the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) managing this property.

    method [sqlalchemy.orm.SynonymProperty.](#sqlalchemy.orm.SynonymProperty)set_parent(*parent:Mapper[Any]*, *init:bool*) → None

Set the parent mapper that references this MapperProperty.

This method is overridden by some subclasses to perform extra
setup when the mapper is first known.

    property uses_objects: bool

Returns True when the argument is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

     class sqlalchemy.orm.QueryContext   class default_load_options

*inherits from* `sqlalchemy.sql.expression.Options`

      class sqlalchemy.orm.QueryableAttribute

*inherits from* `sqlalchemy.orm.base._DeclarativeMapped`, [sqlalchemy.orm.base.SQLORMExpression](#sqlalchemy.orm.SQLORMExpression), [sqlalchemy.orm.base.InspectionAttr](#sqlalchemy.orm.InspectionAttr), [sqlalchemy.orm.PropComparator](#sqlalchemy.orm.PropComparator), `sqlalchemy.sql.roles.JoinTargetRole`, `sqlalchemy.sql.roles.OnClauseRole`, `sqlalchemy.sql.expression.Immutable`, `sqlalchemy.sql.cache_key.SlotsMemoizedHasCacheKey`, `sqlalchemy.util.langhelpers.MemoizedSlots`, `sqlalchemy.event.registry.EventTarget`

Base class for [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor) objects that intercept
attribute events on behalf of a [MapperProperty](#sqlalchemy.orm.MapperProperty)
object.  The actual [MapperProperty](#sqlalchemy.orm.MapperProperty) is accessible
via the `QueryableAttribute.property`
attribute.

See also

[InstrumentedAttribute](#sqlalchemy.orm.InstrumentedAttribute)

[MapperProperty](#sqlalchemy.orm.MapperProperty)

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

[Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs)

| Member Name | Description |
| --- | --- |
| adapt_to_entity() | Return a copy of this PropComparator which will use the givenAliasedInspto produce corresponding expressions. |
| and_() | Add additional criteria to the ON clause that’s represented by this
relationship attribute. |
| expression | The SQL expression object represented by thisQueryableAttribute. |
| is_attribute | True if this object is a Pythondescriptor. |
| of_type() | Redefine this object in terms of a polymorphic subclass,with_polymorphic()construct, oraliased()construct. |
| operate() | Operate on an argument. |
| parent | Return an inspection instance representing the parent. |
| reverse_operate() | Reverse operate on an argument. |

   method [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)adapt_to_entity(*adapt_to_entity:AliasedInsp[Any]*) → Self

Return a copy of this PropComparator which will use the given
[AliasedInsp](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedInsp) to produce corresponding expressions.

    method [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)and_(**clauses:_ColumnExpressionArgument[bool]*) → [QueryableAttribute](#sqlalchemy.orm.QueryableAttribute)[bool]

Add additional criteria to the ON clause that’s represented by this
relationship attribute.

E.g.:

```
stmt = select(User).join(
    User.addresses.and_(Address.email_address != "foo")
)

stmt = select(User).options(
    joinedload(User.addresses.and_(Address.email_address != "foo"))
)
```

Added in version 1.4.

See also

[Combining Relationship with Custom ON Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-join-on-augmented)

[Adding Criteria to loader options](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#loader-option-criteria)

[with_loader_criteria()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.with_loader_criteria)

     attribute [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)expression: [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[_T_co]

The SQL expression object represented by this
[QueryableAttribute](#sqlalchemy.orm.QueryableAttribute).

This will typically be an instance of a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
subclass representing a column expression.

    property info: _InfoType

Return the ‘info’ dictionary for the underlying SQL element.

The behavior here is as follows:

- If the attribute is a column-mapped property, i.e.
  [ColumnProperty](#sqlalchemy.orm.ColumnProperty), which is mapped directly
  to a schema-level [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object, this attribute
  will return the [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) dictionary associated
  with the core-level [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.
- If the attribute is a [ColumnProperty](#sqlalchemy.orm.ColumnProperty) but is mapped to
  any other kind of SQL expression other than a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
  the attribute will refer to the [MapperProperty.info](#sqlalchemy.orm.MapperProperty.info)
  dictionary associated directly with the [ColumnProperty](#sqlalchemy.orm.ColumnProperty),
  assuming the SQL expression itself does not have its own `.info`
  attribute (which should be the case, unless a user-defined SQL
  construct has defined one).
- If the attribute refers to any other kind of
  [MapperProperty](#sqlalchemy.orm.MapperProperty), including [Relationship](#sqlalchemy.orm.Relationship),
  the attribute will refer to the [MapperProperty.info](#sqlalchemy.orm.MapperProperty.info)
  dictionary associated with that [MapperProperty](#sqlalchemy.orm.MapperProperty).
- To access the [MapperProperty.info](#sqlalchemy.orm.MapperProperty.info) dictionary of the
  [MapperProperty](#sqlalchemy.orm.MapperProperty) unconditionally, including for a
  [ColumnProperty](#sqlalchemy.orm.ColumnProperty) that’s associated directly with a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), the attribute can be referred to using
  `QueryableAttribute.property` attribute, as
  `MyClass.someattribute.property.info`.

See also

[SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info)

[MapperProperty.info](#sqlalchemy.orm.MapperProperty.info)

     attribute [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)is_attribute = True

True if this object is a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).

This can refer to one of many types.   Usually a
[QueryableAttribute](#sqlalchemy.orm.QueryableAttribute) which handles attributes events on behalf
of a [MapperProperty](#sqlalchemy.orm.MapperProperty).   But can also be an extension type
such as [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) or [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property).
The [InspectionAttr.extension_type](#sqlalchemy.orm.InspectionAttr.extension_type) will refer to a constant
identifying the specific subtype.

See also

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

     method [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)of_type(*entity:_EntityType[_T]*) → [QueryableAttribute](#sqlalchemy.orm.QueryableAttribute)[_T]

Redefine this object in terms of a polymorphic subclass,
[with_polymorphic()](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#sqlalchemy.orm.with_polymorphic) construct, or [aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased)
construct.

Returns a new PropComparator from which further criterion can be
evaluated.

e.g.:

```
query.join(Company.employees.of_type(Engineer)).filter(
    Engineer.name == "foo"
)
```

   Parameters:

**class_** – a class or mapper indicating that criterion will be
against this specific subclass.

See also

[Using Relationship to join between aliased targets](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-joining-relationships-aliased) - in the
[ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Joining to specific sub-types or with_polymorphic() entities](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html#inheritance-of-type)

     method [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

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

      attribute [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)parent: _InternalEntityType[Any]

Return an inspection instance representing the parent.

This will be either an instance of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
or [AliasedInsp](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedInsp), depending upon the nature
of the parent entity which this attribute is associated
with.

    method [sqlalchemy.orm.QueryableAttribute.](#sqlalchemy.orm.QueryableAttribute)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.orm.QueryableAttribute.operate).

     class sqlalchemy.orm.UOWTransaction

| Member Name | Description |
| --- | --- |
| filter_states_for_dep() | Filter the given list of InstanceStates to those relevant to the
given DependencyProcessor. |
| finalize_flush_changes() | Mark processed objects as clean / deleted after a successful
flush(). |
| get_attribute_history() | Facade to attributes.get_state_history(), including
caching of results. |
| is_deleted() | ReturnTrueif the given state is marked as deleted
within this uowtransaction. |
| remove_state_actions() | Remove pending actions for a state from the uowtransaction. |
| was_already_deleted() | ReturnTrueif the given state is expired and was deleted
previously. |

   method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)filter_states_for_dep(*dep*, *states*)

Filter the given list of InstanceStates to those relevant to the
given DependencyProcessor.

    method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)finalize_flush_changes() → None

Mark processed objects as clean / deleted after a successful
flush().

This method is called within the flush() method after the
execute() method has succeeded and the transaction has been committed.

    method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)get_attribute_history(*state*, *key*, *passive=symbol('PASSIVE_NO_INITIALIZE')*)

Facade to attributes.get_state_history(), including
caching of results.

    method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)is_deleted(*state*)

Return `True` if the given state is marked as deleted
within this uowtransaction.

    method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)remove_state_actions(*state*)

Remove pending actions for a state from the uowtransaction.

    method [sqlalchemy.orm.UOWTransaction.](#sqlalchemy.orm.UOWTransaction)was_already_deleted(*state*)

Return `True` if the given state is expired and was deleted
previously.
