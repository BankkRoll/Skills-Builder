# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Using the legacy ‘backref’ relationship parameter

Note

The [relationship.backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) keyword should be considered
legacy, and use of [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) with explicit
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs should be preferred.  Using
individual [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs provides advantages
including that both ORM mapped classes will include their attributes
up front as the class is constructed, rather than as a deferred step,
and configuration is more straightforward as all arguments are explicit.
New [PEP 484](https://peps.python.org/pep-0484/) features in SQLAlchemy 2.0 also take advantage of
attributes being explicitly present in source code rather than
using dynamic attribute generation.

See also

For general information about bidirectional relationships, see the
following sections:

[Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial),
presents an overview of bi-directional relationship configuration
and behaviors using [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)

[Behavior of save-update cascade with bi-directional relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#back-populates-cascade) - notes on bi-directional [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
behavior regarding [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) cascade behaviors.

[relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)

The [relationship.backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) keyword argument on the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct allows the
automatic generation of a new [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) that will be automatically
be added to the ORM mapping for the related class.  It will then be
placed into a [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) configuration
against the current [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) being configured, with both
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs referring to each other.

Starting with the following example:

```
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = "address"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey("user.id"))
```

The above configuration establishes a collection of `Address` objects on `User` called
`User.addresses`.   It also establishes a `.user` attribute on `Address` which will
refer to the parent `User` object.   Using [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)
it’s equivalent to the following:

```
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "address"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="addresses")
```

The behavior of the `User.addresses` and `Address.user` relationships
is that they now behave in a **bi-directional** way, indicating that
changes on one side of the relationship impact the other.   An example
and discussion of this behavior is in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)
at [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects).

## Backref Default Arguments

Since [relationship.backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) generates a whole new
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), the generation process by default
will attempt to include corresponding arguments in the new
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) that correspond to the original arguments.
As an example, below is a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) that includes a
[custom join condition](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-configure-joins)
which also includes the [relationship.backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) keyword:

```
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    addresses = relationship(
        "Address",
        primaryjoin=(
            "and_(User.id==Address.user_id, Address.email.startswith('tony'))"
        ),
        backref="user",
    )

class Address(Base):
    __tablename__ = "address"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)
    user_id = mapped_column(Integer, ForeignKey("user.id"))
```

When the “backref” is generated, the [relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin)
condition is copied to the new [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) as well:

```
>>> print(User.addresses.property.primaryjoin)
"user".id = address.user_id AND address.email LIKE :email_1 || '%%'
>>>
>>> print(Address.user.property.primaryjoin)
"user".id = address.user_id AND address.email LIKE :email_1 || '%%'
>>>
```

Other arguments that are transferable include the
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter that refers to a
many-to-many association table, as well as the “join” arguments
[relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin) and
[relationship.secondaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin); “backref” is smart enough to know
that these two arguments should also be “reversed” when generating
the opposite side.

## Specifying Backref Arguments

Lots of other arguments for a “backref” are not implicit, and
include arguments like
[relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy),
[relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side),
[relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade) and
[relationship.cascade_backrefs](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade_backrefs).   For this case we use
the [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) function in place of a string; this will store
a specific set of arguments that will be transferred to the new
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) when generated:

```
# <other imports>
from sqlalchemy.orm import backref

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    addresses = relationship(
        "Address",
        backref=backref("user", lazy="joined"),
    )
```

Where above, we placed a `lazy="joined"` directive only on the `Address.user`
side, indicating that when a query against `Address` is made, a join to the `User`
entity should be made automatically which will populate the `.user` attribute of each
returned `Address`.   The [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) function formatted the arguments we gave
it into a form that is interpreted by the receiving [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) as additional
arguments to be applied to the new relationship it creates.

---

# SQLAlchemy 2.0 Documentation

# Basic Relationship Patterns

A quick walkthrough of the basic relational patterns, which in this section are illustrated
using [Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-explicit-declarative-base) style mappings
based on the use of the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation type.

The setup for each of the following sections is as follows:

```
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass
```

## Declarative vs. Imperative Forms

As SQLAlchemy has evolved, different ORM configurational styles have emerged.
For examples in this section and others that use annotated
[Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-explicit-declarative-base) mappings with
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), the corresponding non-annotated form should use the
desired class, or string class name, as the first argument passed to
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).  The example below illustrates the form used in
this document, which is a fully Declarative example using [PEP 484](https://peps.python.org/pep-0484/) annotations,
where the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct is also deriving the target
class and collection type from the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation,
which is the most modern form of SQLAlchemy Declarative mapping:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

In contrast, using a Declarative mapping **without** annotations is
the more “classic” form of mapping, where [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
requires all parameters passed to it directly, as in the example below:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id = mapped_column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(ForeignKey("parent_table.id"))
    parent = relationship("Parent", back_populates="children")
```

Finally, using [Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-imperative-mapping), which
is SQLAlchemy’s original mapping form before Declarative was made (which
nonetheless remains preferred by a vocal minority of users), the above
configuration looks like:

```
registry.map_imperatively(
    Parent,
    parent_table,
    properties={"children": relationship("Child", back_populates="parent")},
)

registry.map_imperatively(
    Child,
    child_table,
    properties={"parent": relationship("Parent", back_populates="children")},
)
```

Additionally, the default collection style for non-annotated mappings is
`list`.  To use a `set` or other collection without annotations, indicate
it using the [relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class) parameter:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id = mapped_column(Integer, primary_key=True)
    children = relationship("Child", collection_class=set, ...)
```

Detail on collection configuration for [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is at
[Customizing Collection Access](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-collections).

Additional differences between annotated and non-annotated / imperative
styles will be noted as needed.

## One To Many

A one to many relationship places a foreign key on the child table referencing
the parent.  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is then specified on the parent, as referencing
a collection of items represented by the child:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship()

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
```

To establish a bidirectional relationship in one-to-many, where the “reverse”
side is a many to one, specify an additional [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) and connect
the two using the [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) parameter,
using the attribute name of each [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
as the value for [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) on the other:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

`Child` will get a `parent` attribute with many-to-one semantics.

### Using Sets, Lists, or other Collection Types for One To Many

Using annotated Declarative mappings, the type of collection used for the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is derived from the collection type passed to the
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) container type.  The example from the previous section
may be written to use a `set` rather than a `list` for the
`Parent.children` collection using `Mapped[Set["Child"]]`:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[Set["Child"]] = relationship(back_populates="parent")
```

When using non-annotated forms including imperative mappings, the Python
class to use as a collection may be passed using the
[relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class) parameter.

See also

[Customizing Collection Access](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-collections) - contains further detail on collection
configuration including some techniques to map [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
to dictionaries.

### Configuring Delete Behavior for One to Many

It is often the case that all `Child` objects should be deleted
when their owning `Parent` is deleted.  To configure this behavior,
the `delete` cascade option described at [delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete) is used.
An additional option is that a `Child` object can itself be deleted when
it is deassociated from its parent.  This behavior is described at
[delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-orphan).

See also

[delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete)

[Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes)

[delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-orphan)

## Many To One

Many to one places a foreign key in the parent table referencing the child.
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is declared on the parent, where a new scalar-holding
attribute will be created:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped["Child"] = relationship()

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
```

The above example shows a many-to-one relationship that assumes non-nullable
behavior; the next section, [Nullable Many-to-One](#relationship-patterns-nullable-m2o),
illustrates a nullable version.

Bidirectional behavior is achieved by adding a second [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
and applying the [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) parameter
in both directions, using the attribute name of each [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
as the value for [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) on the other:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped["Child"] = relationship(back_populates="parents")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent"]] = relationship(back_populates="child")
```

### Nullable Many-to-One

In the preceding example, the `Parent.child` relationship is not typed as
allowing `None`; this follows from the `Parent.child_id` column itself
not being nullable, as it is typed with `Mapped[int]`.    If we wanted
`Parent.child` to be a **nullable** many-to-one, we can set both
`Parent.child_id` and `Parent.child` to be `Optional[]` (or its
equivalent), in which case the configuration would look like:

```
from typing import Optional

class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[Optional[int]] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped[Optional["Child"]] = relationship(back_populates="parents")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent"]] = relationship(back_populates="child")
```

Above, the column for `Parent.child_id` will be created in DDL to allow
`NULL` values. When using [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) with explicit typing
declarations, the specification of `child_id: Mapped[Optional[int]]` is
equivalent to setting [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable) to `True` on the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), whereas `child_id: Mapped[int]` is equivalent to
setting it to `False`. See [mapped_column() derives the datatype and nullability from the Mapped annotation](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-nullability)
for background on this behavior.

Tip

If using Python 3.10 or greater, [PEP 604](https://peps.python.org/pep-0604/) syntax is more convenient
to indicate optional types using `| None`, which when combined with
[PEP 563](https://peps.python.org/pep-0563/) postponed annotation evaluation so that string-quoted types aren’t
required, would look like:

```
from __future__ import annotations

class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int | None] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped[Child | None] = relationship(back_populates="parents")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List[Parent]] = relationship(back_populates="child")
```

## One To One

One To One is essentially a [One To Many](#relationship-patterns-o2m)
relationship from a foreign key perspective, but indicates that there will
only be one row at any time that refers to a particular parent row.

When using annotated mappings with [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), the “one-to-one”
convention is achieved by applying a non-collection type to the
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation on both sides of the relationship, which will
imply to the ORM that a collection should not be used on either side, as in the
example below:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child: Mapped["Child"] = relationship(back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="child")
```

Above, when we load a `Parent` object, the `Parent.child` attribute
will refer to a single `Child` object rather than a collection.  If we
replace the value of `Parent.child` with a new `Child` object, the ORM’s
unit of work process will replace the previous `Child` row with the new one,
setting the previous `child.parent_id` column to NULL by default unless there
are specific [cascade](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) behaviors set up.

Tip

As mentioned previously, the ORM considers the “one-to-one” pattern as a
convention, where it makes the assumption that when it loads the
`Parent.child` attribute on a `Parent` object, it will get only one
row back.  If more than one row is returned, the ORM will emit a warning.

However, the `Child.parent` side of the above relationship remains as a
“many-to-one” relationship.  By itself, it will not detect assignment
of more than one `Child`, unless the [relationship.single_parent](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.single_parent)
parameter is set, which may be useful:

```
class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="child", single_parent=True)
```

Outside of setting this parameter, the “one-to-many” side (which here is
one-to-one by convention) will also not reliably detect if more than one
`Child` is associated with a single `Parent`, such as in the case where
the multiple `Child` objects are pending and not database-persistent.

Whether or not [relationship.single_parent](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.single_parent) is used, it is
recommended that the database schema include a [unique constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#schema-unique-constraint) to indicate that the `Child.parent_id` column
should be unique, to ensure at the database level that only one `Child` row may refer
to a particular `Parent` row at a time (see [Declarative Table Configuration](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-configuration)
for background on the `__table_args__` tuple syntax):

```
from sqlalchemy import UniqueConstraint

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="child")

    __table_args__ = (UniqueConstraint("parent_id"),)
```

Added in version 2.0: The [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct can derive
the effective value of the [relationship.uselist](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist)
parameter from a given [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation.

### Setting uselist=False for non-annotated configurations

When using [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) without the benefit of [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
annotations, the one-to-one pattern can be enabled using the
[relationship.uselist](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist) parameter set to `False` on what
would normally be the “many” side, illustrated in a non-annotated
Declarative configuration below:

```
class Parent(Base):
    __tablename__ = "parent_table"

    id = mapped_column(Integer, primary_key=True)
    child = relationship("Child", uselist=False, back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(ForeignKey("parent_table.id"))
    parent = relationship("Parent", back_populates="child")
```

## Many To Many

Many to Many adds an association table between two classes. The association
table is nearly always given as a Core [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object or
other Core selectable such as a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) object, and is
indicated by the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) argument to
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship). Usually, the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) uses the
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object associated with the declarative base class, so
that the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) directives can locate the remote tables
with which to link:

```
from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id")),
    Column("right_id", ForeignKey("right_table.id")),
)

class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List[Child]] = relationship(secondary=association_table)

class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)
```

Tip

The “association table” above has foreign key constraints established that
refer to the two entity tables on either side of the relationship.  The data
type of each of `association.left_id` and `association.right_id` is
normally inferred from that of the referenced table and may be omitted.
It is also **recommended**, though not in any way required by SQLAlchemy,
that the columns which refer to the two entity tables are established within
either a **unique constraint** or more commonly as the **primary key constraint**;
this ensures that duplicate rows won’t be persisted within the table regardless
of issues on the application side:

```
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id"), primary_key=True),
    Column("right_id", ForeignKey("right_table.id"), primary_key=True),
)
```

### Setting Bi-Directional Many-to-many

For a bidirectional relationship, both sides of the relationship contain a
collection.  Specify using [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates), and
for each [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) specify the common association table:

```
from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id"), primary_key=True),
    Column("right_id", ForeignKey("right_table.id"), primary_key=True),
)

class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List[Child]] = relationship(
        secondary=association_table, back_populates="parents"
    )

class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List[Parent]] = relationship(
        secondary=association_table, back_populates="children"
    )
```

### Using a late-evaluated form for the “secondary” argument

The [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter of
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) also accepts two different “late evaluated” forms,
including string table name as well as lambda callable.   See the section
[Using a late-evaluated form for the “secondary” argument of many-to-many](#orm-declarative-relationship-secondary-eval) for background and
examples.

### Using Sets, Lists, or other Collection Types for Many To Many

Configuration of collections for a Many to Many relationship is identical
to that of [One To Many](#relationship-patterns-o2m), as described at
[Using Sets, Lists, or other Collection Types for One To Many](#relationship-patterns-o2m-collection).    For an annotated mapping
using [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), the collection can be indicated by the
type of collection used within the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) generic class,
such as `set`:

```
class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[Set["Child"]] = relationship(secondary=association_table)
```

When using non-annotated forms including imperative mappings, as is
the case with one-to-many, the Python
class to use as a collection may be passed using the
[relationship.collection_class](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.collection_class) parameter.

See also

[Customizing Collection Access](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-collections) - contains further detail on collection
configuration including some techniques to map [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
to dictionaries.

### Deleting Rows from the Many to Many Table

A behavior which is unique to the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
argument to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is that the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) which
is specified here is automatically subject to INSERT and DELETE statements, as
objects are added or removed from the collection. There is **no need to delete
from this table manually**.   The act of removing a record from the collection
will have the effect of the row being deleted on flush:

```
# row will be deleted from the "secondary" table
# automatically
myparent.children.remove(somechild)
```

A question which often arises is how the row in the “secondary” table can be deleted
when the child object is handed directly to [Session.delete()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.delete):

```
session.delete(somechild)
```

There are several possibilities here:

- If there is a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) from `Parent` to `Child`, but there is
  **not** a reverse-relationship that links a particular `Child` to each `Parent`,
  SQLAlchemy will not have any awareness that when deleting this particular
  `Child` object, it needs to maintain the “secondary” table that links it to
  the `Parent`.  No delete of the “secondary” table will occur.
- If there is a relationship that links a particular `Child` to each `Parent`,
  suppose it’s called `Child.parents`, SQLAlchemy by default will load in
  the `Child.parents` collection to locate all `Parent` objects, and remove
  each row from the “secondary” table which establishes this link.  Note that
  this relationship does not need to be bidirectional; SQLAlchemy is strictly
  looking at every [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) associated with the `Child` object
  being deleted.
- A higher performing option here is to use ON DELETE CASCADE directives
  with the foreign keys used by the database.   Assuming the database supports
  this feature, the database itself can be made to automatically delete rows in the
  “secondary” table as referencing rows in “child” are deleted.   SQLAlchemy
  can be instructed to forego actively loading in the `Child.parents`
  collection in this case using the [relationship.passive_deletes](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes)
  directive on [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship); see [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes) for more details
  on this.

Note again, these behaviors are *only* relevant to the
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) option used with
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).   If dealing with association tables that are mapped
explicitly and are *not* present in the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
option of a relevant [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), cascade rules can be used
instead to automatically delete entities in reaction to a related entity being
deleted - see [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) for information on this feature.

See also

[Using delete cascade with many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-many-to-many)

[Using foreign key ON DELETE with many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes-many-to-many)

## Association Object

The association object pattern is a variant on many-to-many: it’s used when an
association table contains additional columns beyond those which are foreign
keys to the parent and child (or left and right) tables, columns which are most
ideally mapped to their own ORM mapped class. This mapped class is mapped
against the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that would otherwise be noted as
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) when using the many-to-many pattern.

In the association object pattern, the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
parameter is not used; instead, a class is mapped directly to the association
table. Two individual [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs then link first the
parent side to the mapped association class via one to many, and then the
mapped association class to the child side via many-to-one, to form a
uni-directional association object relationship from parent, to association, to
child. For a bi-directional relationship, four [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
constructs are used to link the mapped association class to both parent and
child in both directions.

The example below illustrates a new class `Association` which maps
to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) named `association`; this table now includes
an additional column called `extra_data`, which is a string value that
is stored along with each association between `Parent` and
`Child`.   By mapping the table to an explicit class, rudimental access
from `Parent` to `Child` makes explicit use of `Association`:

```
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Association(Base):
    __tablename__ = "association_table"
    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(
        ForeignKey("right_table.id"), primary_key=True
    )
    extra_data: Mapped[Optional[str]]
    child: Mapped["Child"] = relationship()

class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Association"]] = relationship()

class Child(Base):
    __tablename__ = "right_table"
    id: Mapped[int] = mapped_column(primary_key=True)
```

To illustrate the bi-directional version, we add two more [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
constructs, linked to the existing ones using [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates):

```
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Association(Base):
    __tablename__ = "association_table"
    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(
        ForeignKey("right_table.id"), primary_key=True
    )
    extra_data: Mapped[Optional[str]]
    child: Mapped["Child"] = relationship(back_populates="parents")
    parent: Mapped["Parent"] = relationship(back_populates="children")

class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Association"]] = relationship(back_populates="parent")

class Child(Base):
    __tablename__ = "right_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Association"]] = relationship(back_populates="child")
```

Working with the association pattern in its direct form requires that child
objects are associated with an association instance before being appended to
the parent; similarly, access from parent to child goes through the
association object:

```
# create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a.child = Child()
p.children.append(a)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)
```

To enhance the association object pattern such that direct
access to the `Association` object is optional, SQLAlchemy
provides the [Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html) extension. This
extension allows the configuration of attributes which will
access two “hops” with a single access, one “hop” to the
associated object, and a second to a target attribute.

See also

[Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html) - allows direct “many to many” style
access between parent and child for a three-class association object mapping.

Warning

Avoid mixing the association object pattern with the [many-to-many](#relationships-many-to-many)
pattern directly, as this produces conditions where data may be read
and written in an inconsistent fashion without special steps;
the [association proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html) is typically
used to provide more succinct access.  For more detailed background
on the caveats introduced by this combination, see the next section
[Combining Association Object with Many-to-Many Access Patterns](#association-pattern-w-m2m).

### Combining Association Object with Many-to-Many Access Patterns

As mentioned in the previous section, the association object pattern does not
automatically integrate with usage of the many-to-many pattern against the same
tables/columns at the same time.  From this it follows that read operations
may return conflicting data and write operations may also attempt to flush
conflicting changes, causing either integrity errors or unexpected
inserts or deletes.

To illustrate, the example below configures a bidirectional many-to-many relationship
between `Parent` and `Child` via `Parent.children` and `Child.parents`.
At the same time, an association object relationship is also configured,
between `Parent.child_associations -> Association.child`
and `Child.parent_associations -> Association.parent`:

```
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Association(Base):
    __tablename__ = "association_table"

    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(
        ForeignKey("right_table.id"), primary_key=True
    )
    extra_data: Mapped[Optional[str]]

    # association between Association -> Child
    child: Mapped["Child"] = relationship(back_populates="parent_associations")

    # association between Association -> Parent
    parent: Mapped["Parent"] = relationship(back_populates="child_associations")

class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Child, bypassing the `Association` class
    children: Mapped[List["Child"]] = relationship(
        secondary="association_table", back_populates="parents"
    )

    # association between Parent -> Association -> Child
    child_associations: Mapped[List["Association"]] = relationship(
        back_populates="parent"
    )

class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Parent, bypassing the `Association` class
    parents: Mapped[List["Parent"]] = relationship(
        secondary="association_table", back_populates="children"
    )

    # association between Child -> Association -> Parent
    parent_associations: Mapped[List["Association"]] = relationship(
        back_populates="child"
    )
```

When using this ORM model to make changes, changes made to
`Parent.children` will not be coordinated with changes made to
`Parent.child_associations` or `Child.parent_associations` in Python;
while all of these relationships will continue to function normally by
themselves, changes on one will not show up in another until the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is expired, which normally occurs automatically after
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit).

Additionally, if conflicting changes are made,
such as adding a new `Association` object while also appending the same
related `Child` to `Parent.children`, this will raise integrity
errors when the unit of work flush process proceeds, as in the
example below:

```
p1 = Parent()
c1 = Child()
p1.children.append(c1)

# redundant, will cause a duplicate INSERT on Association
p1.child_associations.append(Association(child=c1))
```

Appending `Child` to `Parent.children` directly also implies the
creation of rows in the `association` table without indicating any
value for the `association.extra_data` column, which will receive
`NULL` for its value.

It’s fine to use a mapping like the above if you know what you’re doing; there
may be good reason to use many-to-many relationships in the case where use
of the “association object” pattern is infrequent, which is that it’s easier to
load relationships along a single many-to-many relationship, which can also
optimize slightly better how the “secondary” table is used in SQL statements,
compared to how two separate relationships to an explicit association class is
used.   It’s at least a good idea to apply the
[relationship.viewonly](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.viewonly) parameter
to the “secondary” relationship to avoid the issue of conflicting
changes occurring, as well as preventing `NULL` being written to the
additional association columns, as below:

```
class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Child, bypassing the `Association` class
    children: Mapped[List["Child"]] = relationship(
        secondary="association_table", back_populates="parents", viewonly=True
    )

    # association between Parent -> Association -> Child
    child_associations: Mapped[List["Association"]] = relationship(
        back_populates="parent"
    )

class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # many-to-many relationship to Parent, bypassing the `Association` class
    parents: Mapped[List["Parent"]] = relationship(
        secondary="association_table", back_populates="children", viewonly=True
    )

    # association between Child -> Association -> Parent
    parent_associations: Mapped[List["Association"]] = relationship(
        back_populates="child"
    )
```

The above mapping will not write any changes to `Parent.children` or
`Child.parents` to the database, preventing conflicting writes.  However, reads
of `Parent.children` or `Child.parents` will not necessarily match the data
that’s read from `Parent.child_associations` or `Child.parent_associations`,
if changes are being made to these collections within the same transaction
or [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) as where the viewonly collections are being read.  If
use of the association object relationships is infrequent and is carefully
organized against code that accesses the many-to-many collections to avoid
stale reads (in extreme cases, making direct use of [Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire)
to cause collections to be refreshed within the current transaction), the pattern may be feasible.

A popular alternative to the above pattern is one where the direct many-to-many
`Parent.children` and `Child.parents` relationships are replaced with
an extension that will transparently proxy through the `Association`
class, while keeping everything consistent from the ORM’s point of
view.  This extension is known as the [Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html).

See also

[Association Proxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html) - allows direct “many to many” style
access between parent and child for a three-class association object mapping.

## Late-Evaluation of Relationship Arguments

Most of the examples in the preceding sections illustrate mappings
where the various [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs refer to their target
classes using a string name, rather than the class itself, such as when
using [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), a forward reference is generated that exists
at runtime only as a string:

```
class Parent(Base):
    # ...

    children: Mapped[List["Child"]] = relationship(back_populates="parent")

class Child(Base):
    # ...

    parent: Mapped["Parent"] = relationship(back_populates="children")
```

Similarly, when using non-annotated forms such as non-annotated Declarative
or Imperative mappings, a string name is also supported directly by
the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct:

```
registry.map_imperatively(
    Parent,
    parent_table,
    properties={"children": relationship("Child", back_populates="parent")},
)

registry.map_imperatively(
    Child,
    child_table,
    properties={"parent": relationship("Parent", back_populates="children")},
)
```

These string names are resolved into classes in the mapper resolution stage,
which is an internal process that occurs typically after all mappings have been
defined and is normally triggered by the first usage of the mappings
themselves.  The [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) object is the container where these
names are stored and resolved to the mapped classes to which they refer.

In addition to the main class argument for [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship),
other arguments which depend upon the columns present on an as-yet
undefined class may also be specified either as Python functions, or more
commonly as strings.   For most of these
arguments except that of the main argument, string inputs are
**evaluated as Python expressions using Python’s built-in eval() function**,
as they are intended to receive complete SQL expressions.

Warning

As the Python `eval()` function is used to interpret the
late-evaluated string arguments passed to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) mapper
configuration construct, these arguments should **not** be repurposed
such that they would receive untrusted user input; `eval()` is
**not secure** against untrusted user input.

The full namespace available within this evaluation includes all classes mapped
for this declarative base, as well as the contents of the `sqlalchemy`
package, including expression functions like [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) and
`sqlalchemy.sql.functions.func`:

```
class Parent(Base):
    # ...

    children: Mapped[List["Child"]] = relationship(
        order_by="desc(Child.email_address)",
        primaryjoin="Parent.id == Child.parent_id",
    )
```

For the case where more than one module contains a class of the same name,
string class names can also be specified as module-qualified paths
within any of these string expressions:

```
class Parent(Base):
    # ...

    children: Mapped[List["myapp.mymodel.Child"]] = relationship(
        order_by="desc(myapp.mymodel.Child.email_address)",
        primaryjoin="myapp.mymodel.Parent.id == myapp.mymodel.Child.parent_id",
    )
```

In an example like the above, the string passed to [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
can be disambiguated from a specific class argument by passing the class
location string directly to the first positional parameter ([relationship.argument](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.argument)) as well.
Below illustrates a typing-only import for `Child`, combined with a
runtime specifier for the target class that will search for the correct
name within the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry):

```
import typing

if typing.TYPE_CHECKING:
    from myapp.mymodel import Child

class Parent(Base):
    # ...

    children: Mapped[List["Child"]] = relationship(
        "myapp.mymodel.Child",
        order_by="desc(myapp.mymodel.Child.email_address)",
        primaryjoin="myapp.mymodel.Parent.id == myapp.mymodel.Child.parent_id",
    )
```

The qualified path can be any partial path that removes ambiguity between
the names.  For example, to disambiguate between
`myapp.model1.Child` and `myapp.model2.Child`,
we can specify `model1.Child` or `model2.Child`:

```
class Parent(Base):
    # ...

    children: Mapped[List["Child"]] = relationship(
        "model1.Child",
        order_by="desc(mymodel1.Child.email_address)",
        primaryjoin="Parent.id == model1.Child.parent_id",
    )
```

The [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct also accepts Python functions or
lambdas as input for these arguments.  A Python functional approach might look
like the following:

```
import typing

from sqlalchemy import desc

if typing.TYPE_CHECKING:
    from myapplication import Child

def _resolve_child_model():
    from myapplication import Child

    return Child

class Parent(Base):
    # ...

    children: Mapped[List["Child"]] = relationship(
        _resolve_child_model,
        order_by=lambda: desc(_resolve_child_model().email_address),
        primaryjoin=lambda: Parent.id == _resolve_child_model().parent_id,
    )
```

The full list of parameters which accept Python functions/lambdas or strings
that will be passed to `eval()` are:

- [relationship.order_by](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.order_by)
- [relationship.primaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin)
- [relationship.secondaryjoin](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin)
- [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
- [relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side)
- [relationship.foreign_keys](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys)
- [relationship._user_defined_foreign_keys](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params._user_defined_foreign_keys)

Warning

As stated previously, the above parameters to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
are **evaluated as Python code expressions using eval().  DO NOT PASS
UNTRUSTED INPUT TO THESE ARGUMENTS.**

### Adding Relationships to Mapped Classes After Declaration

It should also be noted that in a similar way as described at
[Appending additional columns to an existing Declarative mapped class](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-adding-columns), any [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty)
construct can be added to a declarative base mapping at any time
(noting that annotated forms are not supported in this context).  If
we wanted to implement this [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) after the `Address`
class were available, we could also apply it afterwards:

```
# first, module A, where Child has not been created yet,
# we create a Parent class which knows nothing about Child

class Parent(Base): ...

# ... later, in Module B, which is imported after module A:

class Child(Base): ...

from module_a import Parent

# assign the User.addresses relationship as a class variable.  The
# declarative base class will intercept this and map the relationship.
Parent.children = relationship(Child, primaryjoin=Child.parent_id == Parent.id)
```

As is the case for ORM mapped columns, there’s no capability for
the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation type to take part in this operation;
therefore, the related class must be specified directly within the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct, either as the class itself, the string
name of the class, or a callable function that returns a reference to
the target class.

Note

As is the case for ORM mapped columns, assignment of mapped
properties to an already mapped class will only
function correctly if the “declarative base” class is used, meaning
the user-defined subclass of [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) or the
dynamically generated class returned by [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base)
or [registry.generate_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base).   This “base” class includes
a Python metaclass which implements a special `__setattr__()` method
that intercepts these operations.

Runtime assignment of class-mapped attributes to a mapped class will **not** work
if the class is mapped using decorators like [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped)
or imperative functions like [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively).

### Using a late-evaluated form for the “secondary” argument of many-to-many

Many-to-many relationships make use of the
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter, which ordinarily
indicates a reference to a typically non-mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object or other Core selectable object.  Late evaluation
using a lambda callable is typical.

For the example given at [Many To Many](#relationships-many-to-many), if we assumed
that the `association_table` [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object would be defined at a point later on in the
module than the mapped class itself, we may write the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
using a lambda as:

```
class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(
        "Child", secondary=lambda: association_table
    )
```

As a shortcut for table names that are also **valid Python identifiers**, the
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter may also be passed as a
string, where resolution works by evaluation of the string as a Python
expression, with simple identifier names linked to same-named
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that are present in the same
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection referenced by the current
[registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry).

In the example below, the expression
`"association_table"` is evaluated as a variable
named “association_table” that is resolved against the table names within
the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection:

```
class Parent(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(secondary="association_table")
```

Note

When passed as a string, the name passed to
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) **must be a valid Python identifier**
starting with a letter and containing only alphanumeric characters or
underscores.   Other characters such as dashes etc. will be interpreted
as Python operators which will not resolve to the name given.  Please consider
using lambda expressions rather than strings for improved clarity.

Warning

When passed as a string,
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) argument is interpreted using Python’s
`eval()` function, even though it’s typically the name of a table.
**DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
