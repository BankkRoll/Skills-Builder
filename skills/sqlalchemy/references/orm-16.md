# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Alternate Class Instrumentation

Extensible class instrumentation.

The [sqlalchemy.ext.instrumentation](#module-sqlalchemy.ext.instrumentation) package provides for alternate
systems of class instrumentation within the ORM.  Class instrumentation
refers to how the ORM places attributes on the class which maintain
data and track changes to that data, as well as event hooks installed
on the class.

Note

The extension package is provided for the benefit of integration
with other object management packages, which already perform
their own instrumentation.  It is not intended for general use.

For examples of how the instrumentation extension is used,
see the example [Attribute Instrumentation](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-instrumentation).

## API Reference

| Object Name | Description |
| --- | --- |
| ExtendedInstrumentationRegistry | ExtendsInstrumentationFactorywith additional
bookkeeping, to accommodate multiple types of
class managers. |
| instrumentation_finders | An extensible sequence of callables which return instrumentation
implementations |
| INSTRUMENTATION_MANAGER | Attribute, elects custom instrumentation when present on a mapped class. |
| InstrumentationFactory | Factory for new ClassManager instances. |
| InstrumentationManager | User-defined class instrumentation extension. |

   sqlalchemy.ext.instrumentation.INSTRUMENTATION_MANAGER = '__sa_instrumentation_manager__'

Attribute, elects custom instrumentation when present on a mapped class.

Allows a class to specify a slightly or wildly different technique for
tracking changes made to mapped attributes and collections.

Only one instrumentation implementation is allowed in a given object
inheritance hierarchy.

The value of this attribute must be a callable and will be passed a class
object.  The callable must return one of:

> - An instance of an [InstrumentationManager](#sqlalchemy.ext.instrumentation.InstrumentationManager) or subclass
> - An object implementing all or some of InstrumentationManager (TODO)
> - A dictionary of callables, implementing all or some of the above (TODO)
> - An instance of a [ClassManager](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ClassManager) or subclass

This attribute is consulted by SQLAlchemy instrumentation
resolution, once the [sqlalchemy.ext.instrumentation](#module-sqlalchemy.ext.instrumentation) module
has been imported.  If custom finders are installed in the global
instrumentation_finders list, they may or may not choose to honor this
attribute.

    class sqlalchemy.orm.instrumentation.InstrumentationFactory

*inherits from* `sqlalchemy.event.registry.EventTarget`

Factory for new ClassManager instances.

    class sqlalchemy.ext.instrumentation.InstrumentationManager

User-defined class instrumentation extension.

[InstrumentationManager](#sqlalchemy.ext.instrumentation.InstrumentationManager) can be subclassed in order
to change
how class instrumentation proceeds. This class exists for
the purposes of integration with other object management
frameworks which would like to entirely modify the
instrumentation methodology of the ORM, and is not intended
for regular usage.  For interception of class instrumentation
events, see [InstrumentationEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstrumentationEvents).

The API for this class should be considered as semi-stable,
and may change slightly with new releases.

| Member Name | Description |
| --- | --- |
| dict_getter() |  |
| get_instance_dict() |  |
| initialize_instance_dict() |  |
| install_descriptor() |  |
| install_member() |  |
| install_state() |  |
| instrument_attribute() |  |
| instrument_collection_class() |  |
| manage() |  |
| manager_getter() |  |
| post_configure_attribute() |  |
| remove_state() |  |
| state_getter() |  |
| uninstall_descriptor() |  |
| uninstall_member() |  |
| unregister() |  |

   method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)dict_getter(*class_*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)get_instance_dict(*class_*, *instance*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)initialize_instance_dict(*class_*, *instance*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)install_descriptor(*class_*, *key*, *inst*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)install_member(*class_*, *key*, *implementation*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)install_state(*class_*, *instance*, *state*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)instrument_attribute(*class_*, *key*, *inst*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)instrument_collection_class(*class_*, *key*, *collection_class*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)manage(*class_*, *manager*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)manager_getter(*class_*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)post_configure_attribute(*class_*, *key*, *inst*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)remove_state(*class_*, *instance*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)state_getter(*class_*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)uninstall_descriptor(*class_*, *key*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)uninstall_member(*class_*, *key*)    method [sqlalchemy.ext.instrumentation.InstrumentationManager.](#sqlalchemy.ext.instrumentation.InstrumentationManager)unregister(*class_*, *manager*)     sqlalchemy.ext.instrumentation.instrumentation_finders = [<function find_native_user_instrumentation_hook>]

An extensible sequence of callables which return instrumentation
implementations

When a class is registered, each callable will be passed a class object.
If None is returned, the
next finder in the sequence is consulted.  Otherwise the return must be an
instrumentation factory that follows the same guidelines as
sqlalchemy.ext.instrumentation.INSTRUMENTATION_MANAGER.

By default, the only finder is find_native_user_instrumentation_hook, which
searches for INSTRUMENTATION_MANAGER.  If all finders return None, standard
ClassManager instrumentation is used.

    class sqlalchemy.ext.instrumentation.ExtendedInstrumentationRegistry

*inherits from* [sqlalchemy.orm.instrumentation.InstrumentationFactory](#sqlalchemy.orm.instrumentation.InstrumentationFactory)

Extends [InstrumentationFactory](#sqlalchemy.orm.instrumentation.InstrumentationFactory) with additional
bookkeeping, to accommodate multiple types of
class managers.

---

# SQLAlchemy 2.0 Documentation

# Mutation Tracking

Provide support for tracking of in-place changes to scalar values,
which are propagated into ORM change events on owning parent objects.

## Establishing Mutability on Scalar Column Values

A typical example of a “mutable” structure is a Python dictionary.
Following the example introduced in [SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html), we
begin with a custom type that marshals Python dictionaries into
JSON strings before being persisted:

```
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncodedDict(TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
```

The usage of `json` is only for the purposes of example. The
[sqlalchemy.ext.mutable](#module-sqlalchemy.ext.mutable) extension can be used
with any type whose target Python type may be mutable, including
[PickleType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType), [ARRAY](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ARRAY), etc.

When using the [sqlalchemy.ext.mutable](#module-sqlalchemy.ext.mutable) extension, the value itself
tracks all parents which reference it.  Below, we illustrate a simple
version of the [MutableDict](#sqlalchemy.ext.mutable.MutableDict) dictionary object, which applies
the [Mutable](#sqlalchemy.ext.mutable.Mutable) mixin to a plain Python dictionary:

```
from sqlalchemy.ext.mutable import Mutable

class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()
```

The above dictionary class takes the approach of subclassing the Python
built-in `dict` to produce a dict
subclass which routes all mutation events through `__setitem__`.  There are
variants on this approach, such as subclassing `UserDict.UserDict` or
`collections.MutableMapping`; the part that’s important to this example is
that the [Mutable.changed()](#sqlalchemy.ext.mutable.Mutable.changed) method is called whenever an in-place
change to the datastructure takes place.

We also redefine the [Mutable.coerce()](#sqlalchemy.ext.mutable.Mutable.coerce) method which will be used to
convert any values that are not instances of `MutableDict`, such
as the plain dictionaries returned by the `json` module, into the
appropriate type.  Defining this method is optional; we could just as well
created our `JSONEncodedDict` such that it always returns an instance
of `MutableDict`, and additionally ensured that all calling code
uses `MutableDict` explicitly.  When [Mutable.coerce()](#sqlalchemy.ext.mutable.Mutable.coerce) is not
overridden, any values applied to a parent object which are not instances
of the mutable type will raise a `ValueError`.

Our new `MutableDict` type offers a class method
[Mutable.as_mutable()](#sqlalchemy.ext.mutable.Mutable.as_mutable) which we can use within column metadata
to associate with types. This method grabs the given type object or
class and associates a listener that will detect all future mappings
of this type, applying event listening instrumentation to the mapped
attribute. Such as, with classical table metadata:

```
from sqlalchemy import Table, Column, Integer

my_data = Table(
    "my_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", MutableDict.as_mutable(JSONEncodedDict)),
)
```

Above, [Mutable.as_mutable()](#sqlalchemy.ext.mutable.Mutable.as_mutable) returns an instance of `JSONEncodedDict`
(if the type object was not an instance already), which will intercept any
attributes which are mapped against this type.  Below we establish a simple
mapping against the `my_data` table:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class MyDataClass(Base):
    __tablename__ = "my_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict[str, str]] = mapped_column(
        MutableDict.as_mutable(JSONEncodedDict)
    )
```

The `MyDataClass.data` member will now be notified of in place changes
to its value.

Any in-place changes to the `MyDataClass.data` member
will flag the attribute as “dirty” on the parent object:

```
>>> from sqlalchemy.orm import Session

>>> sess = Session(some_engine)
>>> m1 = MyDataClass(data={"value1": "foo"})
>>> sess.add(m1)
>>> sess.commit()

>>> m1.data["value1"] = "bar"
>>> assert m1 in sess.dirty
True
```

The `MutableDict` can be associated with all future instances
of `JSONEncodedDict` in one step, using
[Mutable.associate_with()](#sqlalchemy.ext.mutable.Mutable.associate_with).  This is similar to
[Mutable.as_mutable()](#sqlalchemy.ext.mutable.Mutable.as_mutable) except it will intercept all occurrences
of `MutableDict` in all mappings unconditionally, without
the need to declare it individually:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

MutableDict.associate_with(JSONEncodedDict)

class Base(DeclarativeBase):
    pass

class MyDataClass(Base):
    __tablename__ = "my_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict[str, str]] = mapped_column(JSONEncodedDict)
```

### Supporting Pickling

The key to the [sqlalchemy.ext.mutable](#module-sqlalchemy.ext.mutable) extension relies upon the
placement of a `weakref.WeakKeyDictionary` upon the value object, which
stores a mapping of parent mapped objects keyed to the attribute name under
which they are associated with this value. `WeakKeyDictionary` objects are
not picklable, due to the fact that they contain weakrefs and function
callbacks. In our case, this is a good thing, since if this dictionary were
picklable, it could lead to an excessively large pickle size for our value
objects that are pickled by themselves outside of the context of the parent.
The developer responsibility here is only to provide a `__getstate__` method
that excludes the [MutableBase._parents()](#sqlalchemy.ext.mutable.MutableBase._parents) collection from the pickle
stream:

```
class MyMutableType(Mutable):
    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop("_parents", None)
        return d
```

With our dictionary example, we need to return the contents of the dict itself
(and also restore them on __setstate__):

```
class MutableDict(Mutable, dict):
    # ....

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.update(state)
```

In the case that our mutable value object is pickled as it is attached to one
or more parent objects that are also part of the pickle, the [Mutable](#sqlalchemy.ext.mutable.Mutable)
mixin will re-establish the [Mutable._parents](#sqlalchemy.ext.mutable.Mutable._parents) collection on each value
object as the owning parents themselves are unpickled.

### Receiving Events

The [AttributeEvents.modified()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents.modified) event handler may be used to receive
an event when a mutable scalar emits a change event.  This event handler
is called when the [flag_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified) function is called
from within the mutable extension:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import event

class Base(DeclarativeBase):
    pass

class MyDataClass(Base):
    __tablename__ = "my_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict[str, str]] = mapped_column(
        MutableDict.as_mutable(JSONEncodedDict)
    )

@event.listens_for(MyDataClass.data, "modified")
def modified_json(instance, initiator):
    print("json value modified:", instance.data)
```

## Establishing Mutability on Composites

Composites are a special ORM feature which allow a single scalar attribute to
be assigned an object value which represents information “composed” from one
or more columns from the underlying mapped table. The usual example is that of
a geometric “point”, and is introduced in [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite).

As is the case with [Mutable](#sqlalchemy.ext.mutable.Mutable), the user-defined composite class
subclasses [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite) as a mixin, and detects and delivers
change events to its parents via the [MutableComposite.changed()](#sqlalchemy.ext.mutable.MutableComposite.changed) method.
In the case of a composite class, the detection is usually via the usage of the
special Python method `__setattr__()`. In the example below, we expand upon the `Point`
class introduced in [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#mapper-composite) to include
[MutableComposite](#sqlalchemy.ext.mutable.MutableComposite) in its bases and to route attribute set events via
`__setattr__` to the [MutableComposite.changed()](#sqlalchemy.ext.mutable.MutableComposite.changed) method:

```
import dataclasses
from sqlalchemy.ext.mutable import MutableComposite

@dataclasses.dataclass
class Point(MutableComposite):
    x: int
    y: int

    def __setattr__(self, key, value):
        "Intercept set events"

        # set the attribute
        object.__setattr__(self, key, value)

        # alert all parents to the change
        self.changed()
```

The [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite) class makes use of class mapping events to
automatically establish listeners for any usage of [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) that
specifies our `Point` type. Below, when `Point` is mapped to the `Vertex`
class, listeners are established which will route change events from `Point`
objects to each of the `Vertex.start` and `Vertex.end` attributes:

```
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import composite, mapped_column

class Base(DeclarativeBase):
    pass

class Vertex(Base):
    __tablename__ = "vertices"

    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[Point] = composite(
        mapped_column("x1"), mapped_column("y1")
    )
    end: Mapped[Point] = composite(
        mapped_column("x2"), mapped_column("y2")
    )

    def __repr__(self):
        return f"Vertex(start={self.start}, end={self.end})"
```

Any in-place changes to the `Vertex.start` or `Vertex.end` members
will flag the attribute as “dirty” on the parent object:

```
>>> from sqlalchemy.orm import Session
>>> sess = Session(engine)
>>> v1 = Vertex(start=Point(3, 4), end=Point(12, 15))
>>> sess.add(v1)
sql>>> sess.flush()
BEGIN (implicit)
INSERT INTO vertices (x1, y1, x2, y2) VALUES (?, ?, ?, ?)
[...] (3, 4, 12, 15)
>>> v1.end.x = 8
>>> assert v1 in sess.dirty
True
sql>>> sess.commit()
UPDATE vertices SET x2=? WHERE vertices.id = ?
[...] (8, 1)
COMMIT
```

### Coercing Mutable Composites

The [MutableBase.coerce()](#sqlalchemy.ext.mutable.MutableBase.coerce) method is also supported on composite types.
In the case of [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite), the [MutableBase.coerce()](#sqlalchemy.ext.mutable.MutableBase.coerce)
method is only called for attribute set operations, not load operations.
Overriding the [MutableBase.coerce()](#sqlalchemy.ext.mutable.MutableBase.coerce) method is essentially equivalent
to using a [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates) validation routine for all attributes which
make use of the custom composite type:

```
@dataclasses.dataclass
class Point(MutableComposite):
    # other Point methods
    # ...

    def coerce(cls, key, value):
        if isinstance(value, tuple):
            value = Point(*value)
        elif not isinstance(value, Point):
            raise ValueError("tuple or Point expected")
        return value
```

### Supporting Pickling

As is the case with [Mutable](#sqlalchemy.ext.mutable.Mutable), the [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite) helper
class uses a `weakref.WeakKeyDictionary` available via the
[MutableBase._parents()](#sqlalchemy.ext.mutable.MutableBase._parents) attribute which isn’t picklable. If we need to
pickle instances of `Point` or its owning class `Vertex`, we at least need
to define a `__getstate__` that doesn’t include the `_parents` dictionary.
Below we define both a `__getstate__` and a `__setstate__` that package up
the minimal form of our `Point` class:

```
@dataclasses.dataclass
class Point(MutableComposite):
    # ...

    def __getstate__(self):
        return self.x, self.y

    def __setstate__(self, state):
        self.x, self.y = state
```

As with [Mutable](#sqlalchemy.ext.mutable.Mutable), the [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite) augments the
pickling process of the parent’s object-relational state so that the
[MutableBase._parents()](#sqlalchemy.ext.mutable.MutableBase._parents) collection is restored to all `Point` objects.

## API Reference

| Object Name | Description |
| --- | --- |
| Mutable | Mixin that defines transparent propagation of change
events to a parent object. |
| MutableBase | Common base class toMutableandMutableComposite. |
| MutableComposite | Mixin that defines transparent propagation of change
events on a SQLAlchemy “composite” object to its
owning parent or parents. |
| MutableDict | A dictionary type that implementsMutable. |
| MutableList | A list type that implementsMutable. |
| MutableSet | A set type that implementsMutable. |

   class sqlalchemy.ext.mutable.MutableBase

Common base class to [Mutable](#sqlalchemy.ext.mutable.Mutable)
and [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite).

| Member Name | Description |
| --- | --- |
| _parents | Dictionary of parent object’sInstanceState->attribute
name on the parent. |
| coerce() | Given a value, coerce it into the target type. |

   attribute [sqlalchemy.ext.mutable.MutableBase.](#sqlalchemy.ext.mutable.MutableBase)_parents

Dictionary of parent object’s [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)->attribute
name on the parent.

This attribute is a so-called “memoized” property.  It initializes
itself with a new `weakref.WeakKeyDictionary` the first time
it is accessed, returning the same object upon subsequent access.

Changed in version 1.4: the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) is now used
as the key in the weak dictionary rather than the instance
itself.

     classmethod [sqlalchemy.ext.mutable.MutableBase.](#sqlalchemy.ext.mutable.MutableBase)coerce(*key:str*, *value:Any*) → Any | None

Given a value, coerce it into the target type.

Can be overridden by custom subclasses to coerce incoming
data into a particular type.

By default, raises `ValueError`.

This method is called in different scenarios depending on if
the parent class is of type [Mutable](#sqlalchemy.ext.mutable.Mutable) or of type
[MutableComposite](#sqlalchemy.ext.mutable.MutableComposite).  In the case of the former, it is called
for both attribute-set operations as well as during ORM loading
operations.  For the latter, it is only called during attribute-set
operations; the mechanics of the [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) construct
handle coercion during load operations.

  Parameters:

- **key** – string name of the ORM-mapped attribute being set.
- **value** – the incoming value.

  Returns:

the method should return the coerced value, or raise
`ValueError` if the coercion cannot be completed.

       class sqlalchemy.ext.mutable.Mutable

*inherits from* [sqlalchemy.ext.mutable.MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Mixin that defines transparent propagation of change
events to a parent object.

See the example in [Establishing Mutability on Scalar Column Values](#mutable-scalars) for usage information.

| Member Name | Description |
| --- | --- |
| _get_listen_keys() | Given a descriptor attribute, return aset()of the attribute
keys which indicate a change in the state of this attribute. |
| _listen_on_attribute() | Establish this type as a mutation listener for the given
mapped descriptor. |
| _parents | Dictionary of parent object’sInstanceState->attribute
name on the parent. |
| as_mutable() | Associate a SQL type with this mutable Python type. |
| associate_with() | Associate this wrapper with all future mapped columns
of the given type. |
| associate_with_attribute() | Establish this type as a mutation listener for the given
mapped descriptor. |
| changed() | Subclasses should call this method whenever change events occur. |
| coerce() | Given a value, coerce it into the target type. |

   classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)_get_listen_keys(*attribute:QueryableAttribute[Any]*) → Set[str]

*inherited from the* `sqlalchemy.ext.mutable.MutableBase._get_listen_keys` *method of* [MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Given a descriptor attribute, return a `set()` of the attribute
keys which indicate a change in the state of this attribute.

This is normally just `set([attribute.key])`, but can be overridden
to provide for additional keys.  E.g. a [MutableComposite](#sqlalchemy.ext.mutable.MutableComposite)
augments this set with the attribute keys associated with the columns
that comprise the composite value.

This collection is consulted in the case of intercepting the
[InstanceEvents.refresh()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh) and
[InstanceEvents.refresh_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh_flush) events, which pass along a list
of attribute names that have been refreshed; the list is compared
against this set to determine if action needs to be taken.

    classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)_listen_on_attribute(*attribute:QueryableAttribute[Any]*, *coerce:bool*, *parent_cls:_ExternalEntityType[Any]*) → None

*inherited from the* `sqlalchemy.ext.mutable.MutableBase._listen_on_attribute` *method of* [MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Establish this type as a mutation listener for the given
mapped descriptor.

    attribute [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)_parents

*inherited from the* `sqlalchemy.ext.mutable.MutableBase._parents` *attribute of* [MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Dictionary of parent object’s [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)->attribute
name on the parent.

This attribute is a so-called “memoized” property.  It initializes
itself with a new `weakref.WeakKeyDictionary` the first time
it is accessed, returning the same object upon subsequent access.

Changed in version 1.4: the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState) is now used
as the key in the weak dictionary rather than the instance
itself.

     classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)as_mutable(*sqltype:_TypeEngineArgument[_T]*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[_T]

Associate a SQL type with this mutable Python type.

This establishes listeners that will detect ORM mappings against
the given type, adding mutation event trackers to those mappings.

The type is returned, unconditionally as an instance, so that
[as_mutable()](#sqlalchemy.ext.mutable.Mutable.as_mutable) can be used inline:

```
Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data", MyMutableType.as_mutable(PickleType)),
)
```

Note that the returned type is always an instance, even if a class
is given, and that only columns which are declared specifically with
that type instance receive additional instrumentation.

To associate a particular mutable type with all occurrences of a
particular type, use the [Mutable.associate_with()](#sqlalchemy.ext.mutable.Mutable.associate_with) classmethod
of the particular [Mutable](#sqlalchemy.ext.mutable.Mutable) subclass to establish a global
association.

Warning

The listeners established by this method are *global*
to all mappers, and are *not* garbage collected.   Only use
[as_mutable()](#sqlalchemy.ext.mutable.Mutable.as_mutable) for types that are permanent to an application,
not with ad-hoc types else this will cause unbounded growth
in memory usage.

     classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)associate_with(*sqltype:type*) → None

Associate this wrapper with all future mapped columns
of the given type.

This is a convenience method that calls
`associate_with_attribute` automatically.

Warning

The listeners established by this method are *global*
to all mappers, and are *not* garbage collected.   Only use
[associate_with()](#sqlalchemy.ext.mutable.Mutable.associate_with) for types that are permanent to an
application, not with ad-hoc types else this will cause unbounded
growth in memory usage.

     classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)associate_with_attribute(*attribute:InstrumentedAttribute[_O]*) → None

Establish this type as a mutation listener for the given
mapped descriptor.

    method [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)changed() → None

Subclasses should call this method whenever change events occur.

    classmethod [sqlalchemy.ext.mutable.Mutable.](#sqlalchemy.ext.mutable.Mutable)coerce(*key:str*, *value:Any*) → Any | None

*inherited from the* [MutableBase.coerce()](#sqlalchemy.ext.mutable.MutableBase.coerce) *method of* [MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Given a value, coerce it into the target type.

Can be overridden by custom subclasses to coerce incoming
data into a particular type.

By default, raises `ValueError`.

This method is called in different scenarios depending on if
the parent class is of type [Mutable](#sqlalchemy.ext.mutable.Mutable) or of type
[MutableComposite](#sqlalchemy.ext.mutable.MutableComposite).  In the case of the former, it is called
for both attribute-set operations as well as during ORM loading
operations.  For the latter, it is only called during attribute-set
operations; the mechanics of the [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) construct
handle coercion during load operations.

  Parameters:

- **key** – string name of the ORM-mapped attribute being set.
- **value** – the incoming value.

  Returns:

the method should return the coerced value, or raise
`ValueError` if the coercion cannot be completed.

       class sqlalchemy.ext.mutable.MutableComposite

*inherits from* [sqlalchemy.ext.mutable.MutableBase](#sqlalchemy.ext.mutable.MutableBase)

Mixin that defines transparent propagation of change
events on a SQLAlchemy “composite” object to its
owning parent or parents.

See the example in [Establishing Mutability on Composites](#mutable-composites) for usage information.

| Member Name | Description |
| --- | --- |
| changed() | Subclasses should call this method whenever change events occur. |

   method [sqlalchemy.ext.mutable.MutableComposite.](#sqlalchemy.ext.mutable.MutableComposite)changed() → None

Subclasses should call this method whenever change events occur.

     class sqlalchemy.ext.mutable.MutableDict

*inherits from* [sqlalchemy.ext.mutable.Mutable](#sqlalchemy.ext.mutable.Mutable), `builtins.dict`, `typing.Generic`

A dictionary type that implements [Mutable](#sqlalchemy.ext.mutable.Mutable).

The [MutableDict](#sqlalchemy.ext.mutable.MutableDict) object implements a dictionary that will
emit change events to the underlying mapping when the contents of
the dictionary are altered, including when values are added or removed.

Note that [MutableDict](#sqlalchemy.ext.mutable.MutableDict) does **not** apply mutable tracking to  the
*values themselves* inside the dictionary. Therefore it is not a sufficient
solution for the use case of tracking deep changes to a *recursive*
dictionary structure, such as a JSON structure.  To support this use case,
build a subclass of  [MutableDict](#sqlalchemy.ext.mutable.MutableDict) that provides appropriate
coercion to the values placed in the dictionary so that they too are
“mutable”, and emit events up to their parent structure.

See also

[MutableList](#sqlalchemy.ext.mutable.MutableList)

[MutableSet](#sqlalchemy.ext.mutable.MutableSet)

| Member Name | Description |
| --- | --- |
| clear() | Remove all items from the dict. |
| coerce() | Convert plain dictionary to instance of this class. |
| pop() | If the key is not found, return the default if given; otherwise,
raise a KeyError. |
| popitem() | Remove and return a (key, value) pair as a 2-tuple. |
| setdefault() | Insert key with a value of default if key is not in the dictionary. |
| update() | If E is present and has a .keys() method, then does:  for k in E.keys(): D[k] = E[k]
If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
In either case, this is followed by: for k in F:  D[k] = F[k] |

   method [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)clear() → None

Remove all items from the dict.

    classmethod [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)coerce(*key:str*, *value:Any*) → [MutableDict](#sqlalchemy.ext.mutable.MutableDict)[_KT, _VT] | None

Convert plain dictionary to instance of this class.

    method [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)pop(*k*[, *d*]) → v, remove specified key and return the corresponding value.

If the key is not found, return the default if given; otherwise,
raise a KeyError.

    method [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)popitem() → Tuple[_KT, _VT]

Remove and return a (key, value) pair as a 2-tuple.

Pairs are returned in LIFO (last-in, first-out) order.
Raises KeyError if the dict is empty.

    method [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)setdefault(**arg*)

Insert key with a value of default if key is not in the dictionary.

Return the value for key if key is in the dictionary, else default.

    method [sqlalchemy.ext.mutable.MutableDict.](#sqlalchemy.ext.mutable.MutableDict)update([*E*, ]***F*) → None. Update D from mapping/iterable E and F.

If E is present and has a .keys() method, then does:  for k in E.keys(): D[k] = E[k]
If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
In either case, this is followed by: for k in F:  D[k] = F[k]

     class sqlalchemy.ext.mutable.MutableList

*inherits from* [sqlalchemy.ext.mutable.Mutable](#sqlalchemy.ext.mutable.Mutable), `builtins.list`, `typing.Generic`

A list type that implements [Mutable](#sqlalchemy.ext.mutable.Mutable).

The [MutableList](#sqlalchemy.ext.mutable.MutableList) object implements a list that will
emit change events to the underlying mapping when the contents of
the list are altered, including when values are added or removed.

Note that [MutableList](#sqlalchemy.ext.mutable.MutableList) does **not** apply mutable tracking to  the
*values themselves* inside the list. Therefore it is not a sufficient
solution for the use case of tracking deep changes to a *recursive*
mutable structure, such as a JSON structure.  To support this use case,
build a subclass of  [MutableList](#sqlalchemy.ext.mutable.MutableList) that provides appropriate
coercion to the values placed in the dictionary so that they too are
“mutable”, and emit events up to their parent structure.

See also

[MutableDict](#sqlalchemy.ext.mutable.MutableDict)

[MutableSet](#sqlalchemy.ext.mutable.MutableSet)

| Member Name | Description |
| --- | --- |
| append() | Append object to the end of the list. |
| clear() | Remove all items from list. |
| coerce() | Convert plain list to instance of this class. |
| extend() | Extend list by appending elements from the iterable. |
| insert() | Insert object before index. |
| pop() | Remove and return item at index (default last). |
| remove() | Remove first occurrence of value. |
| reverse() | ReverseIN PLACE. |
| sort() | Sort the list in ascending order and return None. |

   method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)append(*x:_T*) → None

Append object to the end of the list.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)clear() → None

Remove all items from list.

    classmethod [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)coerce(*key:str*, *value:MutableList[_T]|_T*) → [MutableList](#sqlalchemy.ext.mutable.MutableList)[_T] | None

Convert plain list to instance of this class.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)extend(*x:Iterable[_T]*) → None

Extend list by appending elements from the iterable.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)insert(*i:SupportsIndex*, *x:_T*) → None

Insert object before index.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)pop(**arg:SupportsIndex*) → _T

Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)remove(*i:_T*) → None

Remove first occurrence of value.

Raises ValueError if the value is not present.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)reverse() → None

Reverse *IN PLACE*.

    method [sqlalchemy.ext.mutable.MutableList.](#sqlalchemy.ext.mutable.MutableList)sort(***kw:Any*) → None

Sort the list in ascending order and return None.

The sort is in-place (i.e. the list itself is modified) and stable (i.e. the
order of two equal elements is maintained).

If a key function is given, apply it once to each list item and sort them,
ascending or descending, according to their function values.

The reverse flag can be set to sort in descending order.

     class sqlalchemy.ext.mutable.MutableSet

*inherits from* [sqlalchemy.ext.mutable.Mutable](#sqlalchemy.ext.mutable.Mutable), `builtins.set`, `typing.Generic`

A set type that implements [Mutable](#sqlalchemy.ext.mutable.Mutable).

The [MutableSet](#sqlalchemy.ext.mutable.MutableSet) object implements a set that will
emit change events to the underlying mapping when the contents of
the set are altered, including when values are added or removed.

Note that [MutableSet](#sqlalchemy.ext.mutable.MutableSet) does **not** apply mutable tracking to  the
*values themselves* inside the set. Therefore it is not a sufficient
solution for the use case of tracking deep changes to a *recursive*
mutable structure.  To support this use case,
build a subclass of  [MutableSet](#sqlalchemy.ext.mutable.MutableSet) that provides appropriate
coercion to the values placed in the dictionary so that they too are
“mutable”, and emit events up to their parent structure.

See also

[MutableDict](#sqlalchemy.ext.mutable.MutableDict)

[MutableList](#sqlalchemy.ext.mutable.MutableList)

| Member Name | Description |
| --- | --- |
| add() | Add an element to a set. |
| clear() | Remove all elements from this set. |
| coerce() | Convert plain set to instance of this class. |
| difference_update() | Update the set, removing elements found in others. |
| discard() | Remove an element from a set if it is a member. |
| intersection_update() | Update the set, keeping only elements found in it and all others. |
| pop() | Remove and return an arbitrary set element. |
| remove() | Remove an element from a set; it must be a member. |
| symmetric_difference_update() | Update the set, keeping only elements found in either set, but not in both. |
| update() | Update the set, adding elements from all others. |

   method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)add(*elem:_T*) → None

Add an element to a set.

This has no effect if the element is already present.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)clear() → None

Remove all elements from this set.

    classmethod [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)coerce(*index:str*, *value:Any*) → [MutableSet](#sqlalchemy.ext.mutable.MutableSet)[_T] | None

Convert plain set to instance of this class.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)difference_update(**arg:Iterable[Any]*) → None

Update the set, removing elements found in others.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)discard(*elem:_T*) → None

Remove an element from a set if it is a member.

Unlike set.remove(), the discard() method does not raise
an exception when an element is missing from the set.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)intersection_update(**arg:Iterable[Any]*) → None

Update the set, keeping only elements found in it and all others.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)pop(**arg:Any*) → _T

Remove and return an arbitrary set element.

Raises KeyError if the set is empty.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)remove(*elem:_T*) → None

Remove an element from a set; it must be a member.

If the element is not a member, raise a KeyError.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)symmetric_difference_update(**arg:Iterable[_T]*) → None

Update the set, keeping only elements found in either set, but not in both.

    method [sqlalchemy.ext.mutable.MutableSet.](#sqlalchemy.ext.mutable.MutableSet)update(**arg:Iterable[_T]*) → None

Update the set, adding elements from all others.
