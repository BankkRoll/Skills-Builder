# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Automap

Define an extension to the [sqlalchemy.ext.declarative](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/api.html#module-sqlalchemy.ext.declarative) system
which automatically generates mapped classes and relationships from a database
schema, typically though not necessarily one which is reflected.

It is hoped that the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) system provides a quick
and modernized solution to the problem that the very famous
[SQLSoup](https://pypi.org/project/sqlsoup/)
also tries to solve, that of generating a quick and rudimentary object
model from an existing database on the fly.  By addressing the issue strictly
at the mapper configuration level, and integrating fully with existing
Declarative class techniques, [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) seeks to provide
a well-integrated approach to the issue of expediently auto-generating ad-hoc
mappings.

Tip

The [Automap](#) extension is geared towards a
“zero declaration” approach, where a complete ORM model including classes
and pre-named relationships can be generated on the fly from a database
schema. For applications that still want to use explicit class declarations
including explicit relationship definitions in conjunction with reflection
of tables, the [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) class, described at
[Using DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected-deferred-reflection), is a better choice.

## Basic Use

The simplest usage is to reflect an existing database into a new model.
We create a new [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class in a similar manner as to how
we create a declarative base class, using [automap_base()](#sqlalchemy.ext.automap.automap_base).
We then call [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) on the resulting base class,
asking it to reflect the schema and produce mappings:

```
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("sqlite:///mydatabase.db")

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.user
Address = Base.classes.address

session = Session(engine)

# rudimentary relationships are produced
session.add(Address(email_address="[email protected]", user=User(name="foo")))
session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
u1 = session.query(User).first()
print(u1.address_collection)
```

Above, calling [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) while passing along the
[AutomapBase.prepare.reflect](#sqlalchemy.ext.automap.AutomapBase.prepare.params.reflect) parameter indicates that the
[MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect)
method will be called on this declarative base
classes’ [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection; then, each **viable** [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) within the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
will get a new mapped class
generated automatically.  The [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects which
link the various tables together will be used to produce new, bidirectional
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) objects between classes.
The classes and relationships
follow along a default naming scheme that we can customize.  At this point,
our basic mapping consisting of related `User` and `Address` classes is
ready to use in the traditional way.

Note

By **viable**, we mean that for a table to be mapped, it must
specify a primary key.  Additionally, if the table is detected as being
a pure association table between two other tables, it will not be directly
mapped and will instead be configured as a many-to-many table between
the mappings for the two referring tables.

## Generating Mappings from an Existing MetaData

We can pass a pre-declared [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object to
[automap_base()](#sqlalchemy.ext.automap.automap_base).
This object can be constructed in any way, including programmatically, from
a serialized file, or from itself being reflected using
[MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect).
Below we illustrate a combination of reflection and
explicit table declaration:

```
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///mydatabase.db")

# produce our own MetaData object
metadata = MetaData()

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
metadata.reflect(engine, only=["user", "address"])

# ... or just define our own Table objects with it (or combine both)
Table(
    "user_order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id")),
)

# we can then produce a set of mappings from this MetaData.
Base = automap_base(metadata=metadata)

# calling prepare() just sets up mapped classes and relationships.
Base.prepare()

# mapped classes are ready
User = Base.classes.user
Address = Base.classes.address
Order = Base.classes.user_order
```

## Generating Mappings from Multiple Schemas

The [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method when used with reflection may reflect
tables from one schema at a time at most, using the
[AutomapBase.prepare.schema](#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema) parameter to indicate the name of a
schema to be reflected from. In order to populate the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase)
with tables from multiple schemas, [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) may be invoked
multiple times, each time passing a different name to the
[AutomapBase.prepare.schema](#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema) parameter. The
[AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method keeps an internal list of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that have already been mapped, and will add new
mappings only for those [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that are new since the
last time [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) was run:

```
e = create_engine("postgresql://scott:tiger@localhost/test")

Base.metadata.create_all(e)

Base = automap_base()

Base.prepare(e)
Base.prepare(e, schema="test_schema")
Base.prepare(e, schema="test_schema_2")
```

Added in version 2.0: The [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method may be called
any number of times; only newly added tables will be mapped
on each run.   Previously in version 1.4 and earlier, multiple calls would
cause errors as it would attempt to re-map an already mapped class.
The previous workaround approach of invoking
[MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) directly remains available as well.

### Automapping same-named tables across multiple schemas

For the common case where multiple schemas may have same-named tables and
therefore would generate same-named classes, conflicts can be resolved either
through use of the [AutomapBase.prepare.classname_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.classname_for_table) hook to
apply different classnames on a per-schema basis, or by using the
[AutomapBase.prepare.modulename_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.modulename_for_table) hook, which allows
disambiguation of same-named classes by changing their effective `__module__`
attribute. In the example below, this hook is used to create a `__module__`
attribute for all classes that is of the form `mymodule.<schemaname>`, where
the schema name `default` is used if no schema is present:

```
e = create_engine("postgresql://scott:tiger@localhost/test")

Base.metadata.create_all(e)

def module_name_for_table(cls, tablename, table):
    if table.schema is not None:
        return f"mymodule.{table.schema}"
    else:
        return f"mymodule.default"

Base = automap_base()

Base.prepare(e, modulename_for_table=module_name_for_table)
Base.prepare(
    e, schema="test_schema", modulename_for_table=module_name_for_table
)
Base.prepare(
    e, schema="test_schema_2", modulename_for_table=module_name_for_table
)
```

The same named-classes are organized into a hierarchical collection available
at [AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module).  This collection is traversed using the
dot-separated name of a particular package/module down into the desired
class name.

Note

When using the [AutomapBase.prepare.modulename_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.modulename_for_table)
hook to return a new `__module__` that is not `None`, the class is
**not** placed into the [AutomapBase.classes](#sqlalchemy.ext.automap.AutomapBase.classes) collection; only
classes that were not given an explicit modulename are placed here, as the
collection cannot represent same-named classes individually.

In the example above, if the database contained a table named `accounts` in
all three of the default schema, the `test_schema` schema, and the
`test_schema_2` schema, three separate classes will be available as:

```
Base.by_module.mymodule.default.accounts
Base.by_module.mymodule.test_schema.accounts
Base.by_module.mymodule.test_schema_2.accounts
```

The default module namespace generated for all [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) classes is
`sqlalchemy.ext.automap`. If no
[AutomapBase.prepare.modulename_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.modulename_for_table) hook is used, the
contents of [AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module) will be entirely within the
`sqlalchemy.ext.automap` namespace (e.g.
`MyBase.by_module.sqlalchemy.ext.automap.<classname>`), which would contain
the same series of classes as what would be seen in
[AutomapBase.classes](#sqlalchemy.ext.automap.AutomapBase.classes). Therefore it’s generally only necessary to use
[AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module) when explicit `__module__` conventions are
present.

## Specifying Classes Explicitly

Tip

If explicit classes are expected to be prominent in an application,
consider using [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) instead.

The [automap](#module-sqlalchemy.ext.automap) extension allows classes to be defined
explicitly, in a way similar to that of the [DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html#sqlalchemy.ext.declarative.DeferredReflection) class.
Classes that extend from [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) act like regular declarative
classes, but are not immediately mapped after their construction, and are
instead mapped when we call [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare).  The
[AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method will make use of the classes we’ve
established based on the table name we use.  If our schema contains tables
`user` and `address`, we can define one or both of the classes to be used:

```
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# automap base
Base = automap_base()

# pre-declare User for the 'user' table
class User(Base):
    __tablename__ = "user"

    # override schema elements like Columns
    user_name = Column("name", String)

    # override relationships too, if desired.
    # we must use the same name that automap would use for the
    # relationship, and also must refer to the class name that automap will
    # generate for "address"
    address_collection = relationship("address", collection_class=set)

# reflect
engine = create_engine("sqlite:///mydatabase.db")
Base.prepare(autoload_with=engine)

# we still have Address generated from the tablename "address",
# but User is the same as Base.classes.User now

Address = Base.classes.address

u1 = session.query(User).first()
print(u1.address_collection)

# the backref is still there:
a1 = session.query(Address).first()
print(a1.user)
```

Above, one of the more intricate details is that we illustrated overriding
one of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) objects that automap would have created.
To do this, we needed to make sure the names match up with what automap
would normally generate, in that the relationship name would be
`User.address_collection` and the name of the class referred to, from
automap’s perspective, is called `address`, even though we are referring to
it as `Address` within our usage of this class.

## Overriding Naming Schemes

[automap](#module-sqlalchemy.ext.automap) is tasked with producing mapped classes and
relationship names based on a schema, which means it has decision points in how
these names are determined.  These three decision points are provided using
functions which can be passed to the [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method, and
are known as [classname_for_table()](#sqlalchemy.ext.automap.classname_for_table),
[name_for_scalar_relationship()](#sqlalchemy.ext.automap.name_for_scalar_relationship),
and [name_for_collection_relationship()](#sqlalchemy.ext.automap.name_for_collection_relationship).  Any or all of these
functions are provided as in the example below, where we use a “camel case”
scheme for class names and a “pluralizer” for collection names using the
[Inflect](https://pypi.org/project/inflect) package:

```
import re
import inflect

def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g."
    "'words_and_underscores' -> 'WordsAndUnderscores'"

    return str(
        tablename[0].upper()
        + re.sub(
            r"_([a-z])",
            lambda m: m.group(1).upper(),
            tablename[1:],
        )
    )

_pluralizer = inflect.engine()

def pluralize_collection(base, local_cls, referred_cls, constraint):
    "Produce an 'uncamelized', 'pluralized' class name, e.g."
    "'SomeTerm' -> 'some_terms'"

    referred_name = referred_cls.__name__
    uncamelized = re.sub(
        r"[A-Z]",
        lambda m: "_%s" % m.group(0).lower(),
        referred_name,
    )[1:]
    pluralized = _pluralizer.plural(uncamelized)
    return pluralized

from sqlalchemy.ext.automap import automap_base

Base = automap_base()

engine = create_engine("sqlite:///mydatabase.db")

Base.prepare(
    autoload_with=engine,
    classname_for_table=camelize_classname,
    name_for_collection_relationship=pluralize_collection,
)
```

From the above mapping, we would now have classes `User` and `Address`,
where the collection from `User` to `Address` is called
`User.addresses`:

```
User, Address = Base.classes.User, Base.classes.Address

u1 = User(addresses=[Address(email="[email protected]")])
```

## Relationship Detection

The vast majority of what automap accomplishes is the generation of
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) structures based on foreign keys.  The mechanism
by which this works for many-to-one and one-to-many relationships is as
follows:

1. A given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), known to be mapped to a particular class,
  is examined for [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects.
2. From each [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint), the remote
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  object present is matched up to the class to which it is to be mapped,
  if any, else it is skipped.
3. As the [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  we are examining corresponds to a
  reference from the immediate mapped class,  the relationship will be set up
  as a many-to-one referring to the referred class; a corresponding
  one-to-many backref will be created on the referred class referring
  to this class.
4. If any of the columns that are part of the
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  are not nullable (e.g. `nullable=False`), a
  [relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade) keyword argument
  of `all, delete-orphan` will be added to the keyword arguments to
  be passed to the relationship or backref.  If the
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) reports that
  [ForeignKeyConstraint.ondelete](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.ondelete)
  is set to `CASCADE` for a not null or `SET NULL` for a nullable
  set of columns, the option [relationship.passive_deletes](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes)
  flag is set to `True` in the set of relationship keyword arguments.
  Note that not all backends support reflection of ON DELETE.
5. The names of the relationships are determined using the
  [AutomapBase.prepare.name_for_scalar_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_scalar_relationship) and
  [AutomapBase.prepare.name_for_collection_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_collection_relationship)
  callable functions.  It is important to note that the default relationship
  naming derives the name from the **the actual class name**.  If you’ve
  given a particular class an explicit name by declaring it, or specified an
  alternate class naming scheme, that’s the name from which the relationship
  name will be derived.
6. The classes are inspected for an existing mapped property matching these
  names.  If one is detected on one side, but none on the other side,
  [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) attempts to create a relationship on the missing side,
  then uses the [relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)
  parameter in order to
  point the new relationship to the other side.
7. In the usual case where no relationship is on either side,
  [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) produces a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) on the
  “many-to-one” side and matches it to the other using the
  [relationship.backref](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) parameter.
8. Production of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) and optionally the
  [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref)
  is handed off to the [AutomapBase.prepare.generate_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship)
  function, which can be supplied by the end-user in order to augment
  the arguments passed to [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) or [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) or to
  make use of custom implementations of these functions.

### Custom Relationship Arguments

The [AutomapBase.prepare.generate_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship) hook can be used
to add parameters to relationships.  For most cases, we can make use of the
existing [generate_relationship()](#sqlalchemy.ext.automap.generate_relationship) function to return
the object, after augmenting the given keyword dictionary with our own
arguments.

Below is an illustration of how to send
[relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade) and
[relationship.passive_deletes](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes)
options along to all one-to-many relationships:

```
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces

def _gen_relationship(
    base, direction, return_fn, attrname, local_cls, referred_cls, **kw
):
    if direction is interfaces.ONETOMANY:
        kw["cascade"] = "all, delete-orphan"
        kw["passive_deletes"] = True
    # make use of the built-in function to actually return
    # the result.
    return generate_relationship(
        base, direction, return_fn, attrname, local_cls, referred_cls, **kw
    )

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# automap base
Base = automap_base()

engine = create_engine("sqlite:///mydatabase.db")
Base.prepare(autoload_with=engine, generate_relationship=_gen_relationship)
```

### Many-to-Many relationships

[automap](#module-sqlalchemy.ext.automap) will generate many-to-many relationships, e.g.
those which contain a `secondary` argument.  The process for producing these
is as follows:

1. A given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is examined for
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  objects, before any mapped class has been assigned to it.
2. If the table contains two and exactly two
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  objects, and all columns within this table are members of these two
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects, the table is assumed to be a
  “secondary” table, and will **not be mapped directly**.
3. The two (or one, for self-referential) external tables to which the
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  refers to are matched to the classes to which they will be
  mapped, if any.
4. If mapped classes for both sides are located, a many-to-many bi-directional
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) / [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref)
  pair is created between the two
  classes.
5. The override logic for many-to-many works the same as that of one-to-many/
  many-to-one; the [generate_relationship()](#sqlalchemy.ext.automap.generate_relationship) function is called upon
  to generate the structures and existing attributes will be maintained.

### Relationships with Inheritance

[automap](#module-sqlalchemy.ext.automap) will not generate any relationships between
two classes that are in an inheritance relationship.   That is, with two
classes given as follows:

```
class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": type,
    }

class Engineer(Employee):
    __tablename__ = "engineer"
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "engineer",
    }
```

The foreign key from `Engineer` to `Employee` is used not for a
relationship, but to establish joined inheritance between the two classes.

Note that this means automap will not generate *any* relationships
for foreign keys that link from a subclass to a superclass.  If a mapping
has actual relationships from subclass to superclass as well, those
need to be explicit.  Below, as we have two separate foreign keys
from `Engineer` to `Employee`, we need to set up both the relationship
we want as well as the `inherit_condition`, as these are not things
SQLAlchemy can guess:

```
class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": type,
    }

class Engineer(Employee):
    __tablename__ = "engineer"
    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    favorite_employee_id = Column(Integer, ForeignKey("employee.id"))

    favorite_employee = relationship(
        Employee, foreign_keys=favorite_employee_id
    )

    __mapper_args__ = {
        "polymorphic_identity": "engineer",
        "inherit_condition": id == Employee.id,
    }
```

### Handling Simple Naming Conflicts

In the case of naming conflicts during mapping, override any of
[classname_for_table()](#sqlalchemy.ext.automap.classname_for_table), [name_for_scalar_relationship()](#sqlalchemy.ext.automap.name_for_scalar_relationship),
and [name_for_collection_relationship()](#sqlalchemy.ext.automap.name_for_collection_relationship) as needed.  For example, if
automap is attempting to name a many-to-one relationship the same as an
existing column, an alternate convention can be conditionally selected.  Given
a schema:

```
CREATE TABLE table_a (
    id INTEGER PRIMARY KEY
);

CREATE TABLE table_b (
    id INTEGER PRIMARY KEY,
    table_a INTEGER,
    FOREIGN KEY(table_a) REFERENCES table_a(id)
);
```

The above schema will first automap the `table_a` table as a class named
`table_a`; it will then automap a relationship onto the class for `table_b`
with the same name as this related class, e.g. `table_a`.  This
relationship name conflicts with the mapping column `table_b.table_a`,
and will emit an error on mapping.

We can resolve this conflict by using an underscore as follows:

```
def name_for_scalar_relationship(
    base, local_cls, referred_cls, constraint
):
    name = referred_cls.__name__.lower()
    local_table = local_cls.__table__
    if name in local_table.columns:
        newname = name + "_"
        warnings.warn(
            "Already detected name %s present.  using %s" % (name, newname)
        )
        return newname
    return name

Base.prepare(
    autoload_with=engine,
    name_for_scalar_relationship=name_for_scalar_relationship,
)
```

Alternatively, we can change the name on the column side.   The columns
that are mapped can be modified using the technique described at
[Naming Declarative Mapped Columns Explicitly](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-column-distinct-names), by assigning the column explicitly
to a new name:

```
Base = automap_base()

class TableB(Base):
    __tablename__ = "table_b"
    _table_a = Column("table_a", ForeignKey("table_a.id"))

Base.prepare(autoload_with=engine)
```

## Using Automap with Explicit Declarations

As noted previously, automap has no dependency on reflection, and can make
use of any collection of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects within a
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
collection.  From this, it follows that automap can also be used
generate missing relationships given an otherwise complete model that fully
defines table metadata:

```
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = automap_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(ForeignKey("user.id"))

# produce relationships
Base.prepare()

# mapping is complete, with "address_collection" and
# "user" relationships
a1 = Address(email="u1")
a2 = Address(email="u2")
u1 = User(address_collection=[a1, a2])
assert a1.user is u1
```

Above, given mostly complete `User` and `Address` mappings, the
[ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) which we defined on `Address.user_id` allowed a
bidirectional relationship pair `Address.user` and
`User.address_collection` to be generated on the mapped classes.

Note that when subclassing [AutomapBase](#sqlalchemy.ext.automap.AutomapBase),
the [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) method is required; if not called, the classes
we’ve declared are in an un-mapped state.

## Intercepting Column Definitions

The [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) and [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects support an
event hook [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) that may be used to intercept
the information reflected about a database column before the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object is constructed.   For example if we wanted to map columns using a
naming convention such as `"attr_<columnname>"`, the event could
be applied as:

```
@event.listens_for(Base.metadata, "column_reflect")
def column_reflect(inspector, table, column_info):
    # set column.key = "attr_<lower_case_name>"
    column_info["key"] = "attr_%s" % column_info["name"].lower()

# run reflection
Base.prepare(autoload_with=engine)
```

Added in version 1.4.0b2: the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event
may be applied to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object.

See also

[DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect)

[Automating Column Naming Schemes from Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-automated-reflection-schemes) - in the ORM mapping documentation

## API Reference

| Object Name | Description |
| --- | --- |
| automap_base([declarative_base], **kw) | Produce a declarative automap base. |
| AutomapBase | Base class for an “automap” schema. |
| classname_for_table(base, tablename, table) | Return the class name that should be used, given the name
of a table. |
| generate_relationship(base, direction, return_fn, attrname, ..., **kw) | Generate arelationship()orbackref()on behalf of two
mapped classes. |
| name_for_collection_relationship(base, local_cls, referred_cls, constraint) | Return the attribute name that should be used to refer from one
class to another, for a collection reference. |
| name_for_scalar_relationship(base, local_cls, referred_cls, constraint) | Return the attribute name that should be used to refer from one
class to another, for a scalar object reference. |

   function sqlalchemy.ext.automap.automap_base(*declarative_base:Type[Any]|None=None*, ***kw:Any*) → Any

Produce a declarative automap base.

This function produces a new base class that is a product of the
[AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class as well a declarative base produced by
`declarative_base()`.

All parameters other than `declarative_base` are keyword arguments
that are passed directly to the `declarative_base()`
function.

  Parameters:

- **declarative_base** – an existing class produced by
  `declarative_base()`.  When this is passed, the function
  no longer invokes `declarative_base()` itself, and all
  other keyword arguments are ignored.
- ****kw** – keyword arguments are passed along to
  `declarative_base()`.

      class sqlalchemy.ext.automap.AutomapBase

Base class for an “automap” schema.

The [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class can be compared to the “declarative base”
class that is produced by the `declarative_base()`
function.  In practice, the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class is always used
as a mixin along with an actual declarative base.

A new subclassable [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) is typically instantiated
using the [automap_base()](#sqlalchemy.ext.automap.automap_base) function.

See also

[Automap](#)

| Member Name | Description |
| --- | --- |
| by_module | An instance ofPropertiescontaining a hierarchal
structure of dot-separated module names linked to classes. |
| classes | An instance ofPropertiescontaining classes. |
| metadata | Refers to theMetaDatacollection that will be used
for newTableobjects. |
| prepare() | Extract mapped classes and relationships from theMetaDataand perform mappings. |

   attribute [sqlalchemy.ext.automap.AutomapBase.](#sqlalchemy.ext.automap.AutomapBase)by_module: ClassVar[ByModuleProperties]

An instance of `Properties` containing a hierarchal
structure of dot-separated module names linked to classes.

This collection is an alternative to the [AutomapBase.classes](#sqlalchemy.ext.automap.AutomapBase.classes)
collection that is useful when making use of the
[AutomapBase.prepare.modulename_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.modulename_for_table) parameter, which will
apply distinct `__module__` attributes to generated classes.

The default `__module__` an automap-generated class is
`sqlalchemy.ext.automap`; to access this namespace using
[AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module) looks like:

```
User = Base.by_module.sqlalchemy.ext.automap.User
```

If a class had a `__module__` of `mymodule.account`, accessing
this namespace looks like:

```
MyClass = Base.by_module.mymodule.account.MyClass
```

Added in version 2.0.

See also

[Generating Mappings from Multiple Schemas](#automap-by-module)

     attribute [sqlalchemy.ext.automap.AutomapBase.](#sqlalchemy.ext.automap.AutomapBase)classes: ClassVar[Properties[Type[Any]]]

An instance of `Properties` containing classes.

This object behaves much like the `.c` collection on a table.  Classes
are present under the name they were given, e.g.:

```
Base = automap_base()
Base.prepare(autoload_with=some_engine)

User, Address = Base.classes.User, Base.classes.Address
```

For class names that overlap with a method name of
`Properties`, such as `items()`, the getitem form
is also supported:

```
Item = Base.classes["items"]
```

     attribute [sqlalchemy.ext.automap.AutomapBase.](#sqlalchemy.ext.automap.AutomapBase)metadata: ClassVar[[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)]

Refers to the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection that will be used
for new [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.

See also

[Accessing Table and Metadata](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-metadata)

     classmethod [sqlalchemy.ext.automap.AutomapBase.](#sqlalchemy.ext.automap.AutomapBase)prepare(*autoload_with:Engine|None=None*, *engine:Any|None=None*, *reflect:bool=False*, *schema:str|None=None*, *classname_for_table:PythonNameForTableType|None=None*, *modulename_for_table:PythonNameForTableType|None=None*, *collection_class:Any|None=None*, *name_for_scalar_relationship:NameForScalarRelationshipType|None=None*, *name_for_collection_relationship:NameForCollectionRelationshipType|None=None*, *generate_relationship:GenerateRelationshipType|None=None*, *reflection_options:Dict[_KT,_VT]|immutabledict[_KT,_VT]={}*) → None

Extract mapped classes and relationships from the
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) and perform mappings.

For full documentation and examples see
[Basic Use](#automap-basic-use).

  Parameters:

- **autoload_with** – an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) with which
  to perform schema reflection; when specified, the
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) method will be invoked within
  the scope of this method.
- **engine** – legacy; use [AutomapBase.autoload_with](#sqlalchemy.ext.automap.AutomapBase.params.autoload_with).
  Used to indicate the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) with which to reflect tables with,
  if [AutomapBase.reflect](#sqlalchemy.ext.automap.AutomapBase.params.reflect) is True.
- **reflect** – legacy; use [AutomapBase.autoload_with](#sqlalchemy.ext.automap.AutomapBase.params.autoload_with).
  Indicates that [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) should be invoked.
- **classname_for_table** – callable function which will be used to
  produce new class names, given a table name.  Defaults to
  [classname_for_table()](#sqlalchemy.ext.automap.classname_for_table).
- **modulename_for_table** –
  callable function which will be used to
  produce the effective `__module__` for an internally generated
  class, to allow for multiple classes of the same name in a single
  automap base which would be in different “modules”.
  Defaults to `None`, which will indicate that `__module__` will not
  be set explicitly; the Python runtime will use the value
  `sqlalchemy.ext.automap` for these classes.
  When assigning `__module__` to generated classes, they can be
  accessed based on dot-separated module names using the
  [AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module) collection.   Classes that have
  an explicit `__module_` assigned using this hook do **not** get
  placed into the [AutomapBase.classes](#sqlalchemy.ext.automap.AutomapBase.classes) collection, only
  into [AutomapBase.by_module](#sqlalchemy.ext.automap.AutomapBase.by_module).
  Added in version 2.0.
  See also
  [Generating Mappings from Multiple Schemas](#automap-by-module)
- **name_for_scalar_relationship** – callable function which will be
  used to produce relationship names for scalar relationships.  Defaults
  to [name_for_scalar_relationship()](#sqlalchemy.ext.automap.name_for_scalar_relationship).
- **name_for_collection_relationship** – callable function which will
  be used to produce relationship names for collection-oriented
  relationships.  Defaults to [name_for_collection_relationship()](#sqlalchemy.ext.automap.name_for_collection_relationship).
- **generate_relationship** – callable function which will be used to
  actually generate [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) and [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref)
  constructs.  Defaults to [generate_relationship()](#sqlalchemy.ext.automap.generate_relationship).
- **collection_class** – the Python collection class that will be used
  when a new [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
  object is created that represents a
  collection.  Defaults to `list`.
- **schema** –
  Schema name to reflect when reflecting tables using
  the [AutomapBase.prepare.autoload_with](#sqlalchemy.ext.automap.AutomapBase.prepare.params.autoload_with) parameter. The name
  is passed to the [MetaData.reflect.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect.params.schema) parameter
  of [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect). When omitted, the default schema
  in use by the database connection is used.
  Note
  The [AutomapBase.prepare.schema](#sqlalchemy.ext.automap.AutomapBase.prepare.params.schema)
  parameter supports reflection of a single schema at a time.
  In order to include tables from many schemas, use
  multiple calls to [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare).
  For an overview of multiple-schema automap including the use
  of additional naming conventions to resolve table name
  conflicts, see the section [Generating Mappings from Multiple Schemas](#automap-by-module).
  Added in version 2.0: [AutomapBase.prepare()](#sqlalchemy.ext.automap.AutomapBase.prepare) supports being
  directly invoked any number of times, keeping track of tables
  that have already been processed to avoid processing them
  a second time.
- **reflection_options** –
  When present, this dictionary of options
  will be passed to [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect)
  to supply general reflection-specific options like `only` and/or
  dialect-specific options like `oracle_resolve_synonyms`.
  Added in version 1.4.

       function sqlalchemy.ext.automap.classname_for_table(*base:Type[Any]*, *tablename:str*, *table:Table*) → str

Return the class name that should be used, given the name
of a table.

The default implementation is:

```
return str(tablename)
```

Alternate implementations can be specified using the
[AutomapBase.prepare.classname_for_table](#sqlalchemy.ext.automap.AutomapBase.prepare.params.classname_for_table)
parameter.

  Parameters:

- **base** – the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class doing the prepare.
- **tablename** – string name of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
- **table** – the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object itself.

  Returns:

a string class name.

Note

In Python 2, the string used for the class name **must** be a
non-Unicode object, e.g. a `str()` object.  The `.name` attribute
of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is typically a Python unicode subclass,
so the
`str()` function should be applied to this name, after accounting for
any non-ASCII characters.

       function sqlalchemy.ext.automap.name_for_scalar_relationship(*base:Type[Any]*, *local_cls:Type[Any]*, *referred_cls:Type[Any]*, *constraint:ForeignKeyConstraint*) → str

Return the attribute name that should be used to refer from one
class to another, for a scalar object reference.

The default implementation is:

```
return referred_cls.__name__.lower()
```

Alternate implementations can be specified using the
[AutomapBase.prepare.name_for_scalar_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_scalar_relationship)
parameter.

  Parameters:

- **base** – the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class doing the prepare.
- **local_cls** – the class to be mapped on the local side.
- **referred_cls** – the class to be mapped on the referring side.
- **constraint** – the [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) that is being
  inspected to produce this relationship.

      function sqlalchemy.ext.automap.name_for_collection_relationship(*base:Type[Any]*, *local_cls:Type[Any]*, *referred_cls:Type[Any]*, *constraint:ForeignKeyConstraint*) → str

Return the attribute name that should be used to refer from one
class to another, for a collection reference.

The default implementation is:

```
return referred_cls.__name__.lower() + "_collection"
```

Alternate implementations
can be specified using the
[AutomapBase.prepare.name_for_collection_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.name_for_collection_relationship)
parameter.

  Parameters:

- **base** – the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class doing the prepare.
- **local_cls** – the class to be mapped on the local side.
- **referred_cls** – the class to be mapped on the referring side.
- **constraint** – the [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) that is being
  inspected to produce this relationship.

      function sqlalchemy.ext.automap.generate_relationship(*base:Type[Any]*, *direction:RelationshipDirection*, *return_fn:Callable[...,Relationship[Any]]|Callable[...,ORMBackrefArgument]*, *attrname:str*, *local_cls:Type[Any]*, *referred_cls:Type[Any]*, ***kw:Any*) → [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship)[Any] | ORMBackrefArgument

Generate a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) or [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref)
on behalf of two
mapped classes.

An alternate implementation of this function can be specified using the
[AutomapBase.prepare.generate_relationship](#sqlalchemy.ext.automap.AutomapBase.prepare.params.generate_relationship) parameter.

The default implementation of this function is as follows:

```
if return_fn is backref:
    return return_fn(attrname, **kw)
elif return_fn is relationship:
    return return_fn(referred_cls, **kw)
else:
    raise TypeError("Unknown relationship function: %s" % return_fn)
```

   Parameters:

- **base** – the [AutomapBase](#sqlalchemy.ext.automap.AutomapBase) class doing the prepare.
- **direction** – indicate the “direction” of the relationship; this will
  be one of `ONETOMANY`, `MANYTOONE`, `MANYTOMANY`.
- **return_fn** – the function that is used by default to create the
  relationship.  This will be either [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) or
  [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref).  The [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) function’s result will be used to
  produce a new [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) in a second step,
  so it is critical
  that user-defined implementations correctly differentiate between the two
  functions, if a custom relationship function is being used.
- **attrname** – the attribute name to which this relationship is being
  assigned. If the value of [generate_relationship.return_fn](#sqlalchemy.ext.automap.generate_relationship.params.return_fn) is
  the [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) function, then this name is the name that is being
  assigned to the backref.
- **local_cls** – the “local” class to which this relationship or backref
  will be locally present.
- **referred_cls** – the “referred” class to which the relationship or
  backref refers to.
- ****kw** – all additional keyword arguments are passed along to the
  function.

  Returns:

a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) or [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref) construct,
as dictated
by the [generate_relationship.return_fn](#sqlalchemy.ext.automap.generate_relationship.params.return_fn) parameter.
