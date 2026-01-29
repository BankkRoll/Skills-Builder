# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Mypy  / Pep-484 Support for ORM Mappings

Support for [PEP 484](https://peps.python.org/pep-0484/) typing annotations as well as the
[MyPy](https://mypy.readthedocs.io/) type checking tool when using SQLAlchemy
[declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html) mappings
that refer to the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object directly, rather than
the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct introduced in SQLAlchemy 2.0.

Deprecated since version 2.0: **The SQLAlchemy Mypy Plugin is DEPRECATED, and will be removed in
the SQLAlchemy 2.1 release.  We would urge users to please
migrate away from it ASAP.   The mypy plugin also works only up until
mypy version 1.10.1.    version 1.11.0 and greater may not work properly.**

This plugin cannot be maintained across constantly changing releases
of mypy and its stability going forward CANNOT be guaranteed.

Modern SQLAlchemy now offers
[fully pep-484 compliant mapping syntaxes](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing);
see the linked section for migration details.

SQLAlchemy Mypy Plugin Status Update

**Updated July 2024**

The mypy plugin is supported **only up until mypy 1.10.1, and it will have
issues running with 1.11.0 or greater**.   Use with mypy 1.11.0 or greater
may have error conditions which currently cannot be resolved.

For SQLAlchemy 2.0, the Mypy plugin continues to work at the level at which
it reached in the SQLAlchemy 1.4 release.  SQLAlchemy 2.0 however features
an
[all new typing system](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing)
for ORM Declarative models that removes the need for the Mypy plugin and
delivers much more consistent behavior with generally superior capabilities.
Note that this new capability is **not
part of SQLAlchemy 1.4, it is only in SQLAlchemy 2.0**.

The SQLAlchemy Mypy plugin, while it has technically never left the “alpha”
stage, should **now be considered as deprecated in SQLAlchemy 2.0, even
though it is still necessary for full Mypy support when using
SQLAlchemy 1.4**.

The Mypy plugin itself does not solve the issue of supplying correct typing
with other typing tools such as Pylance/Pyright, Pytype, Pycharm, etc, which
cannot make use of Mypy plugins. Additionally, Mypy plugins are extremely
difficult to develop, maintain and test, as a Mypy plugin must be deeply
integrated with Mypy’s internal datastructures and processes, which itself
are not stable within the Mypy project itself. The SQLAlchemy Mypy plugin
has lots of limitations when used with code that deviates from very basic
patterns which are reported regularly.

For these reasons, new non-regression issues reported against the Mypy
plugin are unlikely to be fixed.  **Existing code that passes Mypy checks
using the plugin with SQLAlchemy 1.4 installed will continue to pass all
checks in SQLAlchemy 2.0 without any changes required, provided the plugin
is still used. SQLAlchemy 2.0’s API is fully
backwards compatible with the SQLAlchemy 1.4 API and Mypy plugin behavior.**

End-user code that passes all checks under SQLAlchemy 1.4 with the Mypy
plugin may incrementally migrate to the new structures, once
that code is running exclusively on SQLAlchemy 2.0.  See the section
[ORM Declarative Models](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing) for background on how this
migration may proceed.

Code that is running exclusively on SQLAlchemy version
2.0 and has fully migrated to the new declarative constructs will enjoy full
compliance with pep-484 as well as working correctly within IDEs and other
typing tools, without the need for plugins.

## Installation

For **SQLAlchemy 2.0 only**: No stubs should be installed and packages
like [sqlalchemy-stubs](https://github.com/dropbox/sqlalchemy-stubs) and [sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs) should be fully uninstalled.

The [Mypy](https://mypy.readthedocs.io/) package itself is a dependency.

Mypy may be installed using the “mypy” extras hook using pip:

```
pip install sqlalchemy[mypy]
```

The plugin itself is configured as described in
[Configuring mypy to use Plugins](https://mypy.readthedocs.io/en/latest/extending_mypy.html#configuring-mypy-to-use-plugins),
using the `sqlalchemy.ext.mypy.plugin` module name, such as within
`setup.cfg`:

```
[mypy]
plugins = sqlalchemy.ext.mypy.plugin
```

## What the Plugin Does

The primary purpose of the Mypy plugin is to intercept and alter the static
definition of SQLAlchemy
[declarative mappings](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html) so that
they match up to how they are structured after they have been
[instrumented](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumented) by their [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects. This allows both
the class structure itself as well as code that uses the class to make sense to
the Mypy tool, which otherwise would not be the case based on how declarative
mappings currently function.    The plugin is not unlike similar plugins
that are required for libraries like
[dataclasses](https://docs.python.org/3/library/dataclasses.html) which
alter classes dynamically at runtime.

To cover the major areas where this occurs, consider the following ORM
mapping, using the typical example of the `User` class:

```
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base

# "Base" is a class that is created dynamically from the
# declarative_base() function
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

# "some_user" is an instance of the User class, which
# accepts "id" and "name" kwargs based on the mapping
some_user = User(id=5, name="user")

# it has an attribute called .name that's a string
print(f"Username: {some_user.name}")

# a select() construct makes use of SQL expressions derived from the
# User class itself
select_stmt = select(User).where(User.id.in_([3, 4, 5])).where(User.name.contains("s"))
```

Above, the steps that the Mypy extension can take include:

- Interpretation of the `Base` dynamic class generated by
  [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base), so that classes which inherit from it
  are known to be mapped.  It also can accommodate the class decorator
  approach described at [Declarative Mapping using a Decorator (no declarative base)](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-declarative-decorator).
- Type inference for ORM mapped attributes that are defined in declarative
  “inline” style, in the above example the `id` and `name` attributes of
  the `User` class. This includes that an instance of `User` will use
  `int` for `id` and `str` for `name`. It also includes that when the
  `User.id` and `User.name` class-level attributes are accessed, as they
  are above in the `select()` statement, they are compatible with SQL
  expression behavior, which is derived from the
  [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute) attribute descriptor class.
- Application of an `__init__()` method to mapped classes that do not
  already include an explicit constructor, which accepts keyword arguments
  of specific types for all mapped attributes detected.

When the Mypy plugin processes the above file, the resulting static class
definition and Python code passed to the Mypy tool is equivalent to the
following:

```
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

class User(Base):
    __tablename__ = "user"

    id: Mapped[Optional[int]] = Mapped._special_method(
        Column(Integer, primary_key=True)
    )
    name: Mapped[Optional[str]] = Mapped._special_method(Column(String))

    def __init__(self, id: Optional[int] = ..., name: Optional[str] = ...) -> None: ...

some_user = User(id=5, name="user")

print(f"Username: {some_user.name}")

select_stmt = select(User).where(User.id.in_([3, 4, 5])).where(User.name.contains("s"))
```

The key steps which have been taken above include:

- The `Base` class is now defined in terms of the `DeclarativeMeta`
  class explicitly, rather than being a dynamic class.
- The `id` and `name` attributes are defined in terms of the
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) class, which represents a Python descriptor that
  exhibits different behaviors at the class vs. instance levels.  The
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) class is now the base class for the [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute)
  class that is used for all ORM mapped attributes.
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) is defined as a generic class against arbitrary Python
  types, meaning specific occurrences of [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) are associated
  with a specific Python type, such as `Mapped[Optional[int]]` and
  `Mapped[Optional[str]]` above.
- The right-hand side of the declarative mapped attribute assignments are
  **removed**, as this resembles the operation that the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
  class would normally be doing, which is that it would be replacing these
  attributes with specific instances of [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute).
  The original expression is moved into a function call that will allow it to
  still be type-checked without conflicting with the left-hand side of the
  expression. For Mypy purposes, the left-hand typing annotation is sufficient
  for the attribute’s behavior to be understood.
- A type stub for the `User.__init__()` method is added which includes the
  correct keywords and datatypes.

## Usage

The following subsections will address individual uses cases that have
so far been considered for pep-484 compliance.

### Introspection of Columns based on TypeEngine

For mapped columns that include an explicit datatype, when they are mapped
as inline attributes, the mapped type will be introspected automatically:

```
class MyClass(Base):
    # ...

    id = Column(Integer, primary_key=True)
    name = Column("employee_name", String(50), nullable=False)
    other_name = Column(String(50))
```

Above, the ultimate class-level datatypes of `id`, `name` and
`other_name` will be introspected as `Mapped[Optional[int]]`,
`Mapped[Optional[str]]` and `Mapped[Optional[str]]`. The types are by
default **always** considered to be `Optional`, even for the primary key and
non-nullable column. The reason is because while the database columns “id” and
“name” can’t be NULL, the Python attributes `id` and `name` most certainly
can be `None` without an explicit constructor:

```
>>> m1 = MyClass()
>>> m1.id
None
```

The types of the above columns can be stated **explicitly**, providing the
two advantages of clearer self-documentation as well as being able to
control which types are optional:

```
class MyClass(Base):
    # ...

    id: int = Column(Integer, primary_key=True)
    name: str = Column("employee_name", String(50), nullable=False)
    other_name: Optional[str] = Column(String(50))
```

The Mypy plugin will accept the above `int`, `str` and `Optional[str]`
and convert them to include the `Mapped[]` type surrounding them.  The
`Mapped[]` construct may also be used explicitly:

```
from sqlalchemy.orm import Mapped

class MyClass(Base):
    # ...

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column("employee_name", String(50), nullable=False)
    other_name: Mapped[Optional[str]] = Column(String(50))
```

When the type is non-optional, it simply means that the attribute as accessed
from an instance of `MyClass` will be considered to be non-None:

```
mc = MyClass(...)

# will pass mypy --strict
name: str = mc.name
```

For optional attributes, Mypy considers that the type must include None
or otherwise be `Optional`:

```
mc = MyClass(...)

# will pass mypy --strict
other_name: Optional[str] = mc.name
```

Whether or not the mapped attribute is typed as `Optional`, the
generation of the `__init__()` method will **still consider all keywords
to be optional**.  This is again matching what the SQLAlchemy ORM actually
does when it creates the constructor, and should not be confused with the
behavior of a validating system such as Python `dataclasses` which will
generate a constructor that matches the annotations in terms of optional
vs. required attributes.

### Columns that Don’t have an Explicit Type

Columns that include a [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) modifier do not need
to specify a datatype in a SQLAlchemy declarative mapping.  For
this type of attribute, the Mypy plugin will inform the user that it
needs an explicit type to be sent:

```
# .. other imports
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
```

The plugin will deliver the message as follows:

```
$ mypy test3.py --strict
test3.py:20: error: [SQLAlchemy Mypy plugin] Can't infer type from
ORM mapped expression assigned to attribute 'user_id'; please specify a
Python type or Mapped[<python type>] on the left hand side.
Found 1 error in 1 file (checked 1 source file)
```

To resolve, apply an explicit type annotation to the `Address.user_id`
column:

```
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))
```

### Mapping Columns with Imperative Table

In [imperative table style](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration), the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) definitions are given inside of a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
construct which is separate from the mapped attributes themselves.  The Mypy
plugin does not consider this [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), but instead supports that
the attributes can be explicitly stated with a complete annotation that
**must** use the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) class to identify them as mapped attributes:

```
class MyClass(Base):
    __table__ = Table(
        "mytable",
        Base.metadata,
        Column(Integer, primary_key=True),
        Column("employee_name", String(50), nullable=False),
        Column(String(50)),
    )

    id: Mapped[int]
    name: Mapped[str]
    other_name: Mapped[Optional[str]]
```

The above [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotations are considered as mapped columns and
will be included in the default constructor, as well as provide the correct
typing profile for `MyClass` both at the class level and the instance level.

### Mapping Relationships

The plugin has limited support for using type inference to detect the types
for relationships.    For all those cases where it can’t detect the type,
it will emit an informative error message, and in all cases the appropriate
type may be provided explicitly, either with the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
class or optionally omitting it for an inline declaration.     The plugin
also needs to determine whether or not the relationship refers to a collection
or a scalar, and for that it relies upon the explicit value of
the [relationship.uselist](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist) and/or [relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class)
parameters.  An explicit type is needed if neither of these parameters are
present, as well as if the target type of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
is a string or callable, and not a class:

```
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))

    user = relationship(User)
```

The above mapping will produce the following error:

```
test3.py:22: error: [SQLAlchemy Mypy plugin] Can't infer scalar or
collection for ORM mapped expression assigned to attribute 'user'
if both 'uselist' and 'collection_class' arguments are absent from the
relationship(); please specify a type annotation on the left hand side.
Found 1 error in 1 file (checked 1 source file)
```

The error can be resolved either by using `relationship(User, uselist=False)`
or by providing the type, in this case the scalar `User` object:

```
class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))

    user: User = relationship(User)
```

For collections, a similar pattern applies, where in the absence of
`uselist=True` or a [relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class),
a collection annotation such as `List` may be used.   It is also fully
appropriate to use the string name of the class in the annotation as supported
by pep-484, ensuring the class is imported with in
the [TYPE_CHECKING block](https://www.python.org/dev/peps/pep-0484/#runtime-or-type-checking)
as appropriate:

```
from typing import TYPE_CHECKING, List

from .mymodel import Base

if TYPE_CHECKING:
    # if the target of the relationship is in another module
    # that cannot normally be imported at runtime
    from .myaddressmodel import Address

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses: List["Address"] = relationship("Address")
```

As is the case with columns, the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) class may also be
applied explicitly:

```
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))

    user: Mapped[User] = relationship(User, back_populates="addresses")
```

### Using @declared_attr and Declarative Mixins

The [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) class allows Declarative mapped attributes to
be declared in class level functions, and is particularly useful when using
[declarative mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html). For these functions, the return
type of the function should be annotated using either the `Mapped[]`
construct or by indicating the exact kind of object returned by the function.
Additionally, “mixin” classes that are not otherwise mapped (i.e. don’t extend
from a [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) class nor are they mapped with a method
such as [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped)) should be decorated with the
[declarative_mixin()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_mixin) decorator, which provides a hint to the Mypy
plugin that a particular class intends to serve as a declarative mixin:

```
from sqlalchemy.orm import declarative_mixin, declared_attr

@declarative_mixin
class HasUpdatedAt:
    @declared_attr
    def updated_at(cls) -> Column[DateTime]:  # uses Column
        return Column(DateTime)

@declarative_mixin
class HasCompany:
    @declared_attr
    def company_id(cls) -> Mapped[int]:  # uses Mapped
        return mapped_column(ForeignKey("company.id"))

    @declared_attr
    def company(cls) -> Mapped["Company"]:
        return relationship("Company")

class Employee(HasUpdatedAt, HasCompany, Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String)
```

Note the mismatch between the actual return type of a method like
`HasCompany.company` vs. what is annotated.  The Mypy plugin converts
all `@declared_attr` functions into simple annotated attributes to avoid
this complexity:

```
# what Mypy sees
class HasCompany:
    company_id: Mapped[int]
    company: Mapped["Company"]
```

### Combining with Dataclasses or Other Type-Sensitive Attribute Systems

The examples of Python dataclasses integration at [Applying ORM Mappings to an existing dataclass (legacy dataclass use)](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-dataclasses)
presents a problem; Python dataclasses expect an explicit type that it will
use to build the class, and the value given in each assignment statement
is significant.    That is, a class as follows has to be stated exactly
as it is in order to be accepted by dataclasses:

```
mapper_registry: registry = registry()

@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("fullname", String(50)),
        Column("nickname", String(12)),
    )
    id: int = field(init=False)
    name: Optional[str] = None
    fullname: Optional[str] = None
    nickname: Optional[str] = None
    addresses: List[Address] = field(default_factory=list)

    __mapper_args__ = {  # type: ignore
        "properties": {"addresses": relationship("Address")}
    }
```

We can’t apply our `Mapped[]` types to the attributes `id`, `name`,
etc. because they will be rejected by the `@dataclass` decorator.   Additionally,
Mypy has another plugin for dataclasses explicitly which can also get in the
way of what we’re doing.

The above class will actually pass Mypy’s type checking without issue; the
only thing we are missing is the ability for attributes on `User` to be
used in SQL expressions, such as:

```
stmt = select(User.name).where(User.id.in_([1, 2, 3]))
```

To provide a workaround for this, the Mypy plugin has an additional feature
whereby we can specify an extra attribute `_mypy_mapped_attrs`, that is
a list that encloses the class-level objects or their string names.
This attribute can be conditional within the `TYPE_CHECKING` variable:

```
@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("fullname", String(50)),
        Column("nickname", String(12)),
    )
    id: int = field(init=False)
    name: Optional[str] = None
    fullname: Optional[str]
    nickname: Optional[str]
    addresses: List[Address] = field(default_factory=list)

    if TYPE_CHECKING:
        _mypy_mapped_attrs = [id, name, "fullname", "nickname", addresses]

    __mapper_args__ = {  # type: ignore
        "properties": {"addresses": relationship("Address")}
    }
```

With the above recipe, the attributes listed in `_mypy_mapped_attrs`
will be applied with the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) typing information so that the
`User` class will behave as a SQLAlchemy mapped class when used in a
class-bound context.

---

# SQLAlchemy 2.0 Documentation

# Ordering List

A custom list that manages index/position information for contained
elements.

  author:

Jason Kirtland

`orderinglist` is a helper for mutable ordered relationships.  It will
intercept list operations performed on a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)-managed
collection and
automatically synchronize changes in list position onto a target scalar
attribute.

Example: A `slide` table, where each row refers to zero or more entries
in a related `bullet` table.   The bullets within a slide are
displayed in order based on the value of the `position` column in the
`bullet` table.   As entries are reordered in memory, the value of the
`position` attribute should be updated to reflect the new sort order:

```
Base = declarative_base()

class Slide(Base):
    __tablename__ = "slide"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bullets = relationship("Bullet", order_by="Bullet.position")

class Bullet(Base):
    __tablename__ = "bullet"
    id = Column(Integer, primary_key=True)
    slide_id = Column(Integer, ForeignKey("slide.id"))
    position = Column(Integer)
    text = Column(String)
```

The standard relationship mapping will produce a list-like attribute on each
`Slide` containing all related `Bullet` objects,
but coping with changes in ordering is not handled automatically.
When appending a `Bullet` into `Slide.bullets`, the `Bullet.position`
attribute will remain unset until manually assigned.   When the `Bullet`
is inserted into the middle of the list, the following `Bullet` objects
will also need to be renumbered.

The [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) object automates this task, managing the
`position` attribute on all `Bullet` objects in the collection.  It is
constructed using the [ordering_list()](#sqlalchemy.ext.orderinglist.ordering_list) factory:

```
from sqlalchemy.ext.orderinglist import ordering_list

Base = declarative_base()

class Slide(Base):
    __tablename__ = "slide"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bullets = relationship(
        "Bullet",
        order_by="Bullet.position",
        collection_class=ordering_list("position"),
    )

class Bullet(Base):
    __tablename__ = "bullet"
    id = Column(Integer, primary_key=True)
    slide_id = Column(Integer, ForeignKey("slide.id"))
    position = Column(Integer)
    text = Column(String)
```

With the above mapping the `Bullet.position` attribute is managed:

```
s = Slide()
s.bullets.append(Bullet())
s.bullets.append(Bullet())
s.bullets[1].position
>>> 1
s.bullets.insert(1, Bullet())
s.bullets[2].position
>>> 2
```

The [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) construct only works with **changes** to a
collection, and not the initial load from the database, and requires that the
list be sorted when loaded.  Therefore, be sure to specify `order_by` on the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) against the target ordering attribute, so that the
ordering is correct when first loaded.

Warning

[OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) only provides limited functionality when a primary
key column or unique column is the target of the sort.  Operations
that are unsupported or are problematic include:

> - two entries must trade values.  This is not supported directly in the
>   case of a primary key or unique constraint because it means at least
>   one row would need to be temporarily removed first, or changed to
>   a third, neutral value while the switch occurs.
> - an entry must be deleted in order to make room for a new entry.
>   SQLAlchemy’s unit of work performs all INSERTs before DELETEs within a
>   single flush.  In the case of a primary key, it will trade
>   an INSERT/DELETE of the same primary key for an UPDATE statement in order
>   to lessen the impact of this limitation, however this does not take place
>   for a UNIQUE column.
>   A future feature will allow the “DELETE before INSERT” behavior to be
>   possible, alleviating this limitation, though this feature will require
>   explicit configuration at the mapper level for sets of columns that
>   are to be handled in this way.

[ordering_list()](#sqlalchemy.ext.orderinglist.ordering_list) takes the name of the related object’s ordering
attribute as an argument.  By default, the zero-based integer index of the
object’s position in the [ordering_list()](#sqlalchemy.ext.orderinglist.ordering_list) is synchronized with the
ordering attribute: index 0 will get position 0, index 1 position 1, etc.  To
start numbering at 1 or some other integer, provide `count_from=1`.

## API Reference

| Object Name | Description |
| --- | --- |
| count_from_0(index, collection) | Numbering function: consecutive integers starting at 0. |
| count_from_1(index, collection) | Numbering function: consecutive integers starting at 1. |
| count_from_n_factory(start) | Numbering function: consecutive integers starting at arbitrary start. |
| ordering_list(attr[, count_from, ordering_func, reorder_on_append]) | Prepares anOrderingListfactory for use in mapper definitions. |
| OrderingList | A custom list that manages position information for its children. |

   function sqlalchemy.ext.orderinglist.ordering_list(*attr:str*, *count_from:int|None=None*, *ordering_func:Callable[[int,Sequence[_T]],object]|None=None*, *reorder_on_append:bool=False*) → Callable[[], [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList)[_T]]

Prepares an [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) factory for use in mapper definitions.

Returns an object suitable for use as an argument to a Mapper
relationship’s `collection_class` option.  e.g.:

```
from sqlalchemy.ext.orderinglist import ordering_list

class Slide(Base):
    __tablename__ = "slide"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bullets = relationship(
        "Bullet",
        order_by="Bullet.position",
        collection_class=ordering_list("position"),
    )
```

   Parameters:

- **attr** – Name of the mapped attribute to use for storage and retrieval of
  ordering information
- **count_from** – Set up an integer-based ordering, starting at `count_from`.  For
  example, `ordering_list('pos', count_from=1)` would create a 1-based
  list in SQL, storing the value in the ‘pos’ column.  Ignored if
  `ordering_func` is supplied.

Additional arguments are passed to the [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) constructor.

    function sqlalchemy.ext.orderinglist.count_from_0(*index:int*, *collection:object*) → int

Numbering function: consecutive integers starting at 0.

    function sqlalchemy.ext.orderinglist.count_from_1(*index:int*, *collection:object*) → int

Numbering function: consecutive integers starting at 1.

    function sqlalchemy.ext.orderinglist.count_from_n_factory(*start:int*) → Callable[[int, Sequence[Any]], [object](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState.object)]

Numbering function: consecutive integers starting at arbitrary start.

    class sqlalchemy.ext.orderinglist.OrderingList

*inherits from* `builtins.list`, `typing.Generic`

A custom list that manages position information for its children.

The [OrderingList](#sqlalchemy.ext.orderinglist.OrderingList) object is normally set up using the
[ordering_list()](#sqlalchemy.ext.orderinglist.ordering_list) factory function, used in conjunction with
the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function.

| Member Name | Description |
| --- | --- |
| __init__() | A custom list that manages position information for its children. |
| append() | Append object to the end of the list. |
| insert() | Insert object before index. |
| pop() | Remove and return item at index (default last). |
| remove() | Remove first occurrence of value. |
| reorder() | Synchronize ordering for the entire collection. |

   method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)__init__(*ordering_attr:str*, *ordering_func:Callable[[int,Sequence[_T]],object]|None=None*, *reorder_on_append:bool=False*)

A custom list that manages position information for its children.

`OrderingList` is a `collection_class` list implementation that
syncs position in a Python list with a position attribute on the
mapped objects.

This implementation relies on the list starting in the proper order,
so be **sure** to put an `order_by` on your relationship.

  Parameters:

- **ordering_attr** – Name of the attribute that stores the object’s order in the
  relationship.
- **ordering_func** –
  Optional.  A function that maps the position in
  the Python list to a value to store in the
  `ordering_attr`.  Values returned are usually (but need not be!)
  integers.
  An `ordering_func` is called with two positional parameters: the
  index of the element in the list, and the list itself.
  If omitted, Python list indexes are used for the attribute values.
  Two basic pre-built numbering functions are provided in this module:
  `count_from_0` and `count_from_1`.  For more exotic examples
  like stepped numbering, alphabetical and Fibonacci numbering, see
  the unit tests.
- **reorder_on_append** –
  Default False.  When appending an object with an existing (non-None)
  ordering value, that value will be left untouched unless
  `reorder_on_append` is true.  This is an optimization to avoid a
  variety of dangerous unexpected database writes.
  SQLAlchemy will add instances to the list via append() when your
  object loads.  If for some reason the result set from the database
  skips a step in the ordering (say, row ‘1’ is missing but you get
  ‘2’, ‘3’, and ‘4’), reorder_on_append=True would immediately
  renumber the items to ‘1’, ‘2’, ‘3’.  If you have multiple sessions
  making changes, any of whom happen to load this collection even in
  passing, all of the sessions would try to “clean up” the numbering
  in their commits, possibly causing all but one to fail with a
  concurrent modification error.
  Recommend leaving this with the default of False, and just call
  `reorder()` if you’re doing `append()` operations with
  previously ordered instances or when doing some housekeeping after
  manual sql operations.

      method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)append(*entity:_T*) → None

Append object to the end of the list.

    method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)insert(*index:SupportsIndex*, *entity:_T*) → None

Insert object before index.

    method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)pop(*index:SupportsIndex=-1*) → _T

Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.

    method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)remove(*entity:_T*) → None

Remove first occurrence of value.

Raises ValueError if the value is not present.

    method [sqlalchemy.ext.orderinglist.OrderingList.](#sqlalchemy.ext.orderinglist.OrderingList)reorder() → None

Synchronize ordering for the entire collection.

Sweeps through the list and ensures that each object has accurate
ordering information set.

---

# SQLAlchemy 2.0 Documentation

# SQLAlchemy ORM

Here, the Object Relational Mapper is introduced and fully described. If you
want to work with higher-level SQL which is constructed automatically for you,
as well as automated persistence of Python objects, proceed first to the
tutorial.

- [ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
  - [Declare Models](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models)
  - [Create an Engine](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-an-engine)
  - [Emit CREATE TABLE DDL](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#emit-create-table-ddl)
  - [Create Objects and Persist](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist)
  - [Simple SELECT](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select)
  - [SELECT with JOIN](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#select-with-join)
  - [Make Changes](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#make-changes)
  - [Some Deletes](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#some-deletes)
  - [Learn the above concepts in depth](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#learn-the-above-concepts-in-depth)
- [ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html)
  - [ORM Mapped Class Overview](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
  - [Mapping Classes with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)
  - [Integration with dataclasses and attrs](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html)
  - [SQL Expressions as Mapped Attributes](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html)
  - [Changing Attribute Behavior](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html)
  - [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html)
  - [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html)
  - [Non-Traditional Mappings](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html)
  - [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html)
  - [Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
- [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
  - [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
  - [Adjacency List Relationships](https://docs.sqlalchemy.org/en/20/orm/self_referential.html)
  - [Configuring how Relationship Joins](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html)
  - [Working with Large Collections](https://docs.sqlalchemy.org/en/20/orm/large_collections.html)
  - [Collection Customization and API Details](https://docs.sqlalchemy.org/en/20/orm/collection_api.html)
  - [Special Relationship Persistence Patterns](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html)
  - [Using the legacy ‘backref’ relationship parameter](https://docs.sqlalchemy.org/en/20/orm/backref.html)
  - [Relationships API](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
  - [Writing SELECT statements for ORM Mapped Classes](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html)
  - [Writing SELECT statements for Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/queryguide/inheritance.html)
  - [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html)
  - [Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html)
  - [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
  - [ORM API Features for Querying](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html)
  - [Legacy Query API](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html)
- [Using the Session](https://docs.sqlalchemy.org/en/20/orm/session.html)
  - [Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
  - [State Management](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html)
  - [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html)
  - [Transactions and Connection Management](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)
  - [Additional Persistence Techniques](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html)
  - [Contextual/Thread-local Sessions](https://docs.sqlalchemy.org/en/20/orm/contextual.html)
  - [Tracking queries, object and Session Changes with Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html)
  - [Session API](https://docs.sqlalchemy.org/en/20/orm/session_api.html)
- [Events and Internals](https://docs.sqlalchemy.org/en/20/orm/extending.html)
  - [ORM Events](https://docs.sqlalchemy.org/en/20/orm/events.html)
  - [ORM Internals](https://docs.sqlalchemy.org/en/20/orm/internals.html)
  - [ORM Exceptions](https://docs.sqlalchemy.org/en/20/orm/exceptions.html)
- [ORM Extensions](https://docs.sqlalchemy.org/en/20/orm/extensions/index.html)
  - [Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
  - [Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html)
  - [Automap](https://docs.sqlalchemy.org/en/20/orm/extensions/automap.html)
  - [Baked Queries](https://docs.sqlalchemy.org/en/20/orm/extensions/baked.html)
  - [Declarative Extensions](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html)
  - [Mypy  / Pep-484 Support for ORM Mappings](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html)
  - [Mutation Tracking](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html)
  - [Ordering List](https://docs.sqlalchemy.org/en/20/orm/extensions/orderinglist.html)
  - [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html)
  - [Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html)
  - [Indexable](https://docs.sqlalchemy.org/en/20/orm/extensions/indexable.html)
  - [Alternate Class Instrumentation](https://docs.sqlalchemy.org/en/20/orm/extensions/instrumentation.html)
- [ORM Examples](https://docs.sqlalchemy.org/en/20/orm/examples.html)
  - [Mapping Recipes](https://docs.sqlalchemy.org/en/20/orm/examples.html#mapping-recipes)
  - [Inheritance Mapping Recipes](https://docs.sqlalchemy.org/en/20/orm/examples.html#inheritance-mapping-recipes)
  - [Special APIs](https://docs.sqlalchemy.org/en/20/orm/examples.html#special-apis)
  - [Extending the ORM](https://docs.sqlalchemy.org/en/20/orm/examples.html#extending-the-orm)
