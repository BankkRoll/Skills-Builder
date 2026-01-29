# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Mapping Table Columns

This section has been integrated into the
[Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) section.

---

# SQLAlchemy 2.0 Documentation

# ORM Mapped Class Overview

Overview of ORM class mapping configuration.

For readers new to the SQLAlchemy ORM and/or new to Python in general,
it’s recommended to browse through the
[ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#orm-quickstart) and preferably to work through the
[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial), where ORM configuration is first introduced at
[Using ORM Declarative Forms to Define Table Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-orm-table-metadata).

## ORM Mapping Styles

SQLAlchemy features two distinct styles of mapper configuration, which then
feature further sub-options for how they are set up.   The variability in mapper
styles is present to suit a varied list of developer preferences, including
the degree of abstraction of a user-defined class from how it is to be
mapped to relational schema tables and columns, what kinds of class hierarchies
are in use, including whether or not custom metaclass schemes are present,
and finally if there are other class-instrumentation approaches present such
as if Python [dataclasses](https://docs.python.org/3/library/dataclasses.html) are in use simultaneously.

In modern SQLAlchemy, the difference between these styles is mostly
superficial; when a particular SQLAlchemy configurational style is used to
express the intent to map a class, the internal process of mapping the class
proceeds in mostly the same way for each, where the end result is always a
user-defined class that has a [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) configured against a
selectable unit, typically represented by a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, and
the class itself has been [instrumented](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumented) to include behaviors linked to
relational operations both at the level of the class as well as on instances of
that class. As the process is basically the same in all cases, classes mapped
from different styles are always fully interoperable with each other.
The protocol [MappedClassProtocol](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedClassProtocol) can be used to indicate a mapped
class when using type checkers such as mypy.

The original mapping API is commonly referred to as “classical” style,
whereas the more automated style of mapping is known as “declarative” style.
SQLAlchemy now refers to these two mapping styles as **imperative mapping**
and **declarative mapping**.

Regardless of what style of mapping used, all ORM mappings as of SQLAlchemy 1.4
originate from a single object known as [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry), which is a
registry of mapped classes. Using this registry, a set of mapper configurations
can be finalized as a group, and classes within a particular registry may refer
to each other by name within the configurational process.

Changed in version 1.4: Declarative and classical mapping are now referred
to as “declarative” and “imperative” mapping, and are unified internally,
all originating from the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) construct that represents
a collection of related mappings.

### Declarative Mapping

The **Declarative Mapping** is the typical way that mappings are constructed in
modern SQLAlchemy. The most common pattern is to first construct a base class
using the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) superclass. The resulting base class,
when subclassed will apply the declarative mapping process to all subclasses
that derive from it, relative to a particular [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) that
is local to the new base by default. The example below illustrates
the use of a declarative base which is then used in a declarative table mapping:

```
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# declarative base class
class Base(DeclarativeBase):
    pass

# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]
```

Above, the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class is used to generate a new
base class (within SQLAlchemy’s documentation it’s typically referred to
as `Base`, however can have any desired name) from
which new classes to be mapped may inherit from, as above a new mapped
class `User` is constructed.

Changed in version 2.0: The [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) superclass supersedes
the use of the [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) function and
[registry.generate_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base) methods; the superclass approach
integrates with [PEP 484](https://peps.python.org/pep-0484/) tools without the use of plugins.
See [ORM Declarative Models](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing) for migration notes.

The base class refers to a [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) object that maintains a
collection of related mapped classes. as well as to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
object that retains a collection of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects to which
the classes are mapped.

The major Declarative mapping styles are further detailed in the following
sections:

- [Using a Declarative Base Class](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-declarative-generated-base-class) - declarative mapping using a
  base class.
- [Declarative Mapping using a Decorator (no declarative base)](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-declarative-decorator) - declarative mapping using a decorator,
  rather than a base class.

Within the scope of a Declarative mapped class, there are also two varieties
of how the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata may be declared.  These include:

- [Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table) - table columns are declared inline
  within the mapped class using the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) directive
  (or in legacy form, using the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object directly).
  The [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) directive may also be optionally combined with
  type annotations using the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) class which can provide
  some details about the mapped columns directly.  The column
  directives, in combination with the `__tablename__` and optional
  `__table_args__` class level directives will allow the
  Declarative mapping process to construct a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object to
  be mapped.
- [Declarative with Imperative Table (a.k.a. Hybrid Declarative)](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration) - Instead of specifying table name
  and attributes separately, an explicitly constructed [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object
  is associated with a class that is otherwise mapped declaratively.  This
  style of mapping is a hybrid of “declarative” and “imperative” mapping,
  and applies to techniques such as mapping classes to [reflected](https://docs.sqlalchemy.org/en/20/glossary.html#term-reflected) [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, as well as mapping classes to existing
  Core constructs such as joins and subqueries.

Documentation for Declarative mapping continues at [Mapping Classes with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html).

### Imperative Mapping

An **imperative** or **classical** mapping refers to the configuration of a
mapped class using the [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method,
where the target class does not include any declarative class attributes.

Tip

The imperative mapping form is a lesser-used form of mapping that
originates from the very first releases of SQLAlchemy in 2006.  It’s
essentially a means of bypassing the Declarative system to provide a
more “barebones” system of mapping, and does not offer modern features
such as [PEP 484](https://peps.python.org/pep-0484/) support.  As such, most documentation examples
use Declarative forms, and it’s recommended that new users start
with [Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html)
configuration.

Changed in version 2.0: The [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method
is now used to create classical mappings.  The `sqlalchemy.orm.mapper()`
standalone function is effectively removed.

In “classical” form, the table metadata is created separately with the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct, then associated with the `User` class via
the [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method, after establishing
a [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) instance.  Normally, a single instance of
[registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)
shared for all mapped classes that are related to each other:

```
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

class User:
    pass

mapper_registry.map_imperatively(User, user_table)
```

Information about mapped attributes, such as relationships to other classes, are provided
via the `properties` dictionary.  The example below illustrates a second [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object, mapped to a class called `Address`, then linked to `User` via [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship):

```
address = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

mapper_registry.map_imperatively(
    User,
    user,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id)
    },
)

mapper_registry.map_imperatively(Address, address)
```

Note that classes which are mapped with the Imperative approach are **fully
interchangeable** with those mapped with the Declarative approach. Both systems
ultimately create the same configuration, consisting of a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), user-defined class, linked together with a
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object. When we talk about “the behavior of
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)”, this includes when using the Declarative system as well
- it’s still used, just behind the scenes.

## Mapped Class Essential Components

With all mapping forms, the mapping of the class can be configured in many ways
by passing construction arguments that ultimately become part of the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
object via its constructor.  The parameters that are delivered to
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) originate from the given mapping form, including
parameters passed to [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) for an Imperative
mapping, or when using the Declarative system, from a combination
of the table columns, SQL expressions and
relationships being mapped along with that of attributes such as
[__mapper_args__](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-mapper-options).

There are four general classes of configuration information that the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class looks for:

### The class to be mapped

This is a class that we construct in our application.
There are generally no restrictions on the structure of this class. [[1]](#id4)
When a Python class is mapped, there can only be **one** [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
object for the class. [[2]](#id5)

When mapping with the [declarative](#orm-declarative-mapping) mapping
style, the class to be mapped is either a subclass of the declarative base class,
or is handled by a decorator or function such as [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped).

When mapping with the [imperative](#orm-imperative-mapping) style, the
class is passed directly as the
[map_imperatively.class_](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively.params.class_) argument.

### The table, or other from clause object

In the vast majority of common cases this is an instance of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).  For more advanced use cases, it may also refer
to any kind of [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object, the most common
alternative objects being the [Subquery](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Subquery) and [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)
object.

When mapping with the [declarative](#orm-declarative-mapping) mapping
style, the subject table is either generated by the declarative system based
on the `__tablename__` attribute and the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
presented, or it is established via the `__table__` attribute.  These
two styles of configuration are presented at
[Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table) and [Declarative with Imperative Table (a.k.a. Hybrid Declarative)](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration).

When mapping with the [imperative](#orm-imperative-mapping) style, the
subject table is passed positionally as the
[map_imperatively.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively.params.local_table) argument.

In contrast to the “one mapper per class” requirement of a mapped class,
the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object that
is the subject of the mapping may be associated with any number of mappings.
The [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) applies modifications directly to the user-defined
class, but does not modify the given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) in any way.

### The properties dictionary

This is a dictionary of all of the attributes
that will be associated with the mapped class.    By default, the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) generates entries for this dictionary derived from the
given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), in the form of [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty)
objects which each refer to an individual [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) of the
mapped table.  The properties dictionary will also contain all the other
kinds of [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty) objects to be configured, most
commonly instances generated by the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct.

When mapping with the [declarative](#orm-declarative-mapping) mapping
style, the properties dictionary is generated by the declarative system
by scanning the class to be mapped for appropriate attributes.  See
the section [Defining Mapped Properties with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-properties) for notes on this process.

When mapping with the [imperative](#orm-imperative-mapping) style, the
properties dictionary is passed directly as the
`properties` parameter
to [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively), which will pass it along to the
[Mapper.properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.properties) parameter.

### Other mapper configuration parameters

When mapping with the [declarative](#orm-declarative-mapping) mapping
style, additional mapper configuration arguments are configured via the
`__mapper_args__` class attribute.   Examples of use are available
at [Mapper Configuration Options with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-mapper-options).

When mapping with the [imperative](#orm-imperative-mapping) style,
keyword arguments are passed to the to [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively)
method which passes them along to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class.

The full range of parameters accepted are documented at  [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

## Mapped Class Behavior

Across all styles of mapping using the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) object,
the following behaviors are common:

### Default Constructor

The [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) applies a default constructor, i.e. `__init__`
method, to all mapped classes that don’t explicitly have their own
`__init__` method.   The behavior of this method is such that it provides
a convenient keyword constructor that will accept as optional keyword arguments
all the attributes that are named.   E.g.:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str]
```

An object of type `User` above will have a constructor which allows
`User` objects to be created as:

```
u1 = User(name="some name", fullname="some fullname")
```

Tip

The [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) feature provides an alternate
means of generating a default `__init__()` method by using
Python dataclasses, and allows for a highly configurable constructor
form.

Warning

The `__init__()` method of the class is called only when the object is
constructed in Python code, and **not when an object is loaded or refreshed
from the database**.  See the next section [Maintaining Non-Mapped State Across Loads](#mapped-class-load-events)
for a primer on how to invoke special logic when objects are loaded.

A class that includes an explicit `__init__()` method will maintain
that method, and no default constructor will be applied.

To change the default constructor used, a user-defined Python callable may be
provided to the [registry.constructor](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.constructor) parameter which will be
used as the default constructor.

The constructor also applies to imperative mappings:

```
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

class User:
    pass

mapper_registry.map_imperatively(User, user_table)
```

The above class, mapped imperatively as described at [Imperative Mapping](#orm-imperative-mapping),
will also feature the default constructor associated with the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry).

Added in version 1.4: classical mappings now support a standard configuration-level
constructor when they are mapped via the [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively)
method.

### Maintaining Non-Mapped State Across Loads

The `__init__()` method of the mapped class is invoked when the object
is constructed directly in Python code:

```
u1 = User(name="some name", fullname="some fullname")
```

However, when an object is loaded using the ORM [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
the `__init__()` method is **not** called:

```
u1 = session.scalars(select(User).where(User.name == "some name")).first()
```

The reason for this is that when loaded from the database, the operation
used to construct the object, in the above example the `User`, is more
analogous to **deserialization**, such as unpickling, rather than initial
construction.  The majority of the object’s important state is not being
assembled for the first time, it’s being re-loaded from database rows.

Therefore to maintain state within the object that is not part of the data
that’s stored to the database, such that this state is present when objects
are loaded as well as constructed, there are two general approaches detailed
below.

1. Use Python descriptors like `@property`, rather than state, to dynamically
  compute attributes as needed.
  For simple attributes, this is the simplest approach and the least error prone.
  For example if an object `Point` with `Point.x` and `Point.y` wanted
  an attribute with the sum of these attributes:
  ```
  class Point(Base):
      __tablename__ = "point"
      id: Mapped[int] = mapped_column(primary_key=True)
      x: Mapped[int]
      y: Mapped[int]
      @property
      def x_plus_y(self):
          return self.x + self.y
  ```
  An advantage of using dynamic descriptors is that the value is computed
  every time, meaning it maintains the correct value as the underlying
  attributes (`x` and `y` in this case) might change.
  Other forms of the above pattern include Python standard library
  [cached_property](https://docs.python.org/3/library/functools.html#functools.cached_property)
  decorator (which is cached, and not re-computed each time), as well as SQLAlchemy’s [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) decorator which
  allows for attributes that can work for SQL querying as well.
2. Establish state on-load using [InstanceEvents.load()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.load), and optionally
  supplemental methods [InstanceEvents.refresh()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh) and [InstanceEvents.refresh_flush()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.refresh_flush).
  These are event hooks that are invoked whenever the object is loaded
  from the database, or when it is refreshed after being expired.   Typically
  only the [InstanceEvents.load()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.InstanceEvents.load) is needed, since non-mapped local object
  state is not affected by expiration operations.   To revise the `Point`
  example above looks like:
  ```
  from sqlalchemy import event
  class Point(Base):
      __tablename__ = "point"
      id: Mapped[int] = mapped_column(primary_key=True)
      x: Mapped[int]
      y: Mapped[int]
      def __init__(self, x, y, **kw):
          super().__init__(x=x, y=y, **kw)
          self.x_plus_y = x + y
  @event.listens_for(Point, "load")
  def receive_load(target, context):
      target.x_plus_y = target.x + target.y
  ```
  If using the refresh events as well, the event hooks can be stacked on
  top of one callable if needed, as:
  ```
  @event.listens_for(Point, "load")
  @event.listens_for(Point, "refresh")
  @event.listens_for(Point, "refresh_flush")
  def receive_load(target, context, attrs=None):
      target.x_plus_y = target.x + target.y
  ```
  Above, the `attrs` attribute will be present for the `refresh` and
  `refresh_flush` events and indicate a list of attribute names that are
  being refreshed.

### Runtime Introspection of Mapped classes, Instances and Mappers

A class that is mapped using [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) will also feature a few
attributes that are common to all mappings:

- The `__mapper__` attribute will refer to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) that
  is associated with the class:
  ```
  mapper = User.__mapper__
  ```
  This [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) is also what’s returned when using the
  [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function against the mapped class:
  ```
  from sqlalchemy import inspect
  mapper = inspect(User)
  ```
- The `__table__` attribute will refer to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), or
  more generically to the [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object, to which the
  class is mapped:
  ```
  table = User.__table__
  ```
  This [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) is also what’s returned when using the
  [Mapper.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.local_table) attribute of the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper):
  ```
  table = inspect(User).local_table
  ```
  For a single-table inheritance mapping, where the class is a subclass that
  does not have a table of its own, the [Mapper.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.local_table) attribute as well
  as the `.__table__` attribute will be `None`.   To retrieve the
  “selectable” that is actually selected from during a query for this class,
  this is available via the [Mapper.selectable](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.selectable) attribute:
  ```
  table = inspect(User).selectable
  ```

#### Inspection of Mapper objects

As illustrated in the previous section, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object is
available from any mapped class, regardless of method, using the
[Runtime Inspection API](https://docs.sqlalchemy.org/en/20/core/inspection.html) system.  Using the
[inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function, one can acquire the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) from a
mapped class:

```
>>> from sqlalchemy import inspect
>>> insp = inspect(User)
```

Detailed information is available including [Mapper.columns](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.columns):

```
>>> insp.columns
<sqlalchemy.util._collections.OrderedProperties object at 0x102f407f8>
```

This is a namespace that can be viewed in a list format or
via individual names:

```
>>> list(insp.columns)
[Column('id', Integer(), table=<user>, primary_key=True, nullable=False), Column('name', String(length=50), table=<user>), Column('fullname', String(length=50), table=<user>), Column('nickname', String(length=50), table=<user>)]
>>> insp.columns.name
Column('name', String(length=50), table=<user>)
```

Other namespaces include [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors), which includes all mapped
attributes as well as hybrids, association proxies:

```
>>> insp.all_orm_descriptors
<sqlalchemy.util._collections.ImmutableProperties object at 0x1040e2c68>
>>> insp.all_orm_descriptors.keys()
['fullname', 'nickname', 'name', 'id']
```

As well as [Mapper.column_attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.column_attrs):

```
>>> list(insp.column_attrs)
[<ColumnProperty at 0x10403fde0; id>, <ColumnProperty at 0x10403fce8; name>, <ColumnProperty at 0x1040e9050; fullname>, <ColumnProperty at 0x1040e9148; nickname>]
>>> insp.column_attrs.name
<ColumnProperty at 0x10403fce8; name>
>>> insp.column_attrs.name.expression
Column('name', String(length=50), table=<user>)
```

See also

[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)

#### Inspection of Mapped Instances

The [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function also provides information about instances
of a mapped class.  When applied to an instance of a mapped class, rather
than the class itself, the object returned is known as [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState),
which will provide links to not only the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) in use by the
class, but also a detailed interface that provides information on the state
of individual attributes within the instance including their current value
and how this relates to what their database-loaded value is.

Given an instance of the `User` class loaded from the database:

```
>>> u1 = session.scalars(select(User)).first()
```

The [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function will return to us an [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)
object:

```
>>> insp = inspect(u1)
>>> insp
<sqlalchemy.orm.state.InstanceState object at 0x7f07e5fec2e0>
```

With this object we can see elements such as the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper):

```
>>> insp.mapper
<Mapper at 0x7f07e614ef50; User>
```

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to which the object is [attached](https://docs.sqlalchemy.org/en/20/glossary.html#term-attached), if any:

```
>>> insp.session
<sqlalchemy.orm.session.Session object at 0x7f07e614f160>
```

Information about the current [persistence state](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)
for the object:

```
>>> insp.persistent
True
>>> insp.pending
False
```

Attribute state information such as attributes that have not been loaded or
[lazy loaded](https://docs.sqlalchemy.org/en/20/glossary.html#term-lazy-loaded) (assume `addresses` refers to a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
on the mapped class to a related class):

```
>>> insp.unloaded
{'addresses'}
```

Information regarding the current in-Python status of attributes, such as
attributes that have not been modified since the last flush:

```
>>> insp.unmodified
{'nickname', 'name', 'fullname', 'id'}
```

as well as specific history on modifications to attributes since the last flush:

```
>>> insp.attrs.nickname.value
'nickname'
>>> u1.nickname = "new nickname"
>>> insp.attrs.nickname.history
History(added=['new nickname'], unchanged=(), deleted=['nickname'])
```

See also

[InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)

[InstanceState.attrs](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.attrs)

[AttributeState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.AttributeState)

    [[1](#id2)]

When running under Python 2, a Python 2 “old style” class is the only
kind of class that isn’t compatible.    When running code on Python 2,
all classes must extend from the Python `object` class.  Under
Python 3 this is always the case.

   [[2](#id3)]

There is a legacy feature known as a “non primary mapper”, where
additional [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects may be associated with a class
that’s already mapped, however they don’t apply instrumentation
to the class.  This feature is deprecated as of SQLAlchemy 1.3.

---

# SQLAlchemy 2.0 Documentation

# Non-Traditional Mappings

## Mapping a Class against Multiple Tables

Mappers can be constructed against arbitrary relational units (called
*selectables*) in addition to plain tables. For example, the [join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.join)
function creates a selectable unit comprised of
multiple tables, complete with its own composite primary key, which can be
mapped in the same way as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table):

```
from sqlalchemy import Table, Column, Integer, String, MetaData, join, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import column_property

metadata_obj = MetaData()

# define two Table objects
user_table = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String),
)

# define a join between them.  This
# takes place across the user.id and address.user_id
# columns.
user_address_join = join(user_table, address_table)

class Base(DeclarativeBase):
    metadata = metadata_obj

# map to it
class AddressUser(Base):
    __table__ = user_address_join

    id = column_property(user_table.c.id, address_table.c.user_id)
    address_id = address_table.c.id
```

In the example above, the join expresses columns for both the
`user` and the `address` table.  The `user.id` and `address.user_id`
columns are equated by foreign key, so in the mapping they are defined
as one attribute, `AddressUser.id`, using [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) to
indicate a specialized column mapping.   Based on this part of the
configuration, the mapping will copy
new primary key values from `user.id` into the `address.user_id` column
when a flush occurs.

Additionally, the `address.id` column is mapped explicitly to
an attribute named `address_id`.   This is to **disambiguate** the
mapping of the `address.id` column from the same-named `AddressUser.id`
attribute, which here has been assigned to refer to the `user` table
combined with the `address.user_id` foreign key.

The natural primary key of the above mapping is the composite of
`(user.id, address.id)`, as these are the primary key columns of the
`user` and `address` table combined together.  The identity of an
`AddressUser` object will be in terms of these two values, and
is represented from an `AddressUser` object as
`(AddressUser.id, AddressUser.address_id)`.

When referring to the `AddressUser.id` column, most SQL expressions will
make use of only the first column in the list of columns mapped, as the
two columns are synonymous.  However, for the special use case such as
a GROUP BY expression where both columns must be referenced at the same
time while making use of the proper context, that is, accommodating for
aliases and similar, the accessor [Comparator.expressions](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.Comparator.expressions)
may be used:

```
stmt = select(AddressUser).group_by(*AddressUser.id.expressions)
```

Added in version 1.3.17: Added the
[Comparator.expressions](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.Comparator.expressions) accessor.

Note

A mapping against multiple tables as illustrated above supports
persistence, that is, INSERT, UPDATE and DELETE of rows within the targeted
tables. However, it does not support an operation that would UPDATE one
table and perform INSERT or DELETE on others at the same time for one
record. That is, if a record PtoQ is mapped to tables “p” and “q”, where it
has a row based on a LEFT OUTER JOIN of “p” and “q”, if an UPDATE proceeds
that is to alter data in the “q” table in an existing record, the row in
“q” must exist; it won’t emit an INSERT if the primary key identity is
already present.  If the row does not exist, for most DBAPI drivers which
support reporting the number of rows affected by an UPDATE, the ORM will
fail to detect an updated row and raise an error; otherwise, the data
would be silently ignored.

A recipe to allow for an on-the-fly “insert” of the related row might make
use of the .MapperEvents.before_update event and look like:

```
from sqlalchemy import event

@event.listens_for(PtoQ, "before_update")
def receive_before_update(mapper, connection, target):
    if target.some_required_attr_on_q is None:
        connection.execute(q_table.insert(), {"id": target.id})
```

where above, a row is INSERTed into the `q_table` table by creating an
INSERT construct with [Table.insert()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.insert), then executing it  using the
given [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) which is the same one being used to emit other
SQL for the flush process.   The user-supplied logic would have to detect
that the LEFT OUTER JOIN from “p” to “q” does not have an entry for the “q”
side.

## Mapping a Class against Arbitrary Subqueries

Similar to mapping against a join, a plain [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) object
can be used with a mapper as well.  The example fragment below illustrates
mapping a class called `Customer` to a [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) which
includes a join to a subquery:

```
from sqlalchemy import select, func

subq = (
    select(
        func.count(orders.c.id).label("order_count"),
        func.max(orders.c.price).label("highest_order"),
        orders.c.customer_id,
    )
    .group_by(orders.c.customer_id)
    .subquery()
)

customer_select = (
    select(customers, subq)
    .join_from(customers, subq, customers.c.id == subq.c.customer_id)
    .subquery()
)

class Customer(Base):
    __table__ = customer_select
```

Above, the full row represented by `customer_select` will be all the
columns of the `customers` table, in addition to those columns
exposed by the `subq` subquery, which are `order_count`,
`highest_order`, and `customer_id`.  Mapping the `Customer`
class to this selectable then creates a class which will contain
those attributes.

When the ORM persists new instances of `Customer`, only the
`customers` table will actually receive an INSERT.  This is because the
primary key of the `orders` table is not represented in the mapping;  the ORM
will only emit an INSERT into a table for which it has mapped the primary
key.

Note

The practice of mapping to arbitrary SELECT statements, especially
complex ones as above, is
almost never needed; it necessarily tends to produce complex queries
which are often less efficient than that which would be produced
by direct query construction.   The practice is to some degree
based on the very early history of SQLAlchemy where the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
construct was meant to represent the primary querying interface;
in modern usage, the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object can be used to construct
virtually any SELECT statement, including complex composites, and should
be favored over the “map-to-selectable” approach.

## Multiple Mappers for One Class

In modern SQLAlchemy, a particular class is mapped by only one so-called
**primary** mapper at a time.   This mapper is involved in three main areas of
functionality: querying, persistence, and instrumentation of the mapped class.
The rationale of the primary mapper relates to the fact that the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) modifies the class itself, not only persisting it towards a
particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), but also [instrumenting](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumenting) attributes upon the
class which are structured specifically according to the table metadata.   It’s
not possible for more than one mapper to be associated with a class in equal
measure, since only one mapper can actually instrument the class.

The concept of a “non-primary” mapper had existed for many versions of
SQLAlchemy however as of version 1.3 this feature is deprecated.   The
one case where such a non-primary mapper is useful is when constructing
a relationship to a class against an alternative selectable.   This
use case is now suited using the `aliased` construct and is described
at [Relationship to Aliased Class](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-aliased-class).

As far as the use case of a class that can actually be fully persisted
to different tables under different scenarios, very early versions of
SQLAlchemy offered a feature for this adapted from Hibernate, known
as the “entity name” feature.  However, this use case became infeasible
within SQLAlchemy once the mapped class itself became the source of SQL
expression construction; that is, the class’ attributes themselves link
directly to mapped table columns.   The feature was removed and replaced
with a simple recipe-oriented approach to accomplishing this task
without any ambiguity of instrumentation - to create new subclasses, each
mapped individually.  This pattern is now available as a recipe at [Entity Name](https://www.sqlalchemy.org/trac/wiki/UsageRecipes/EntityName).
