# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Changing Attribute Behavior

This section will discuss features and techniques used to modify the
behavior of ORM mapped attributes, including those mapped with
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), and others.

## Simple Validators

A quick way to add a “validation” routine to an attribute is to use the
[validates()](#sqlalchemy.orm.validates) decorator. An attribute validator can raise
an exception, halting the process of mutating the attribute’s value, or can
change the given value into something different. Validators, like all
attribute extensions, are only called by normal userland code; they are not
issued when the ORM is populating the object:

```
from sqlalchemy.orm import validates

class EmailAddress(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("failed simple email validation")
        return address
```

Validators also receive collection append events, when items are added to a
collection:

```
from sqlalchemy.orm import validates

class User(Base):
    # ...

    addresses = relationship("Address")

    @validates("addresses")
    def validate_address(self, key, address):
        if "@" not in address.email:
            raise ValueError("failed simplified email validation")
        return address
```

The validation function by default does not get emitted for collection
remove events, as the typical expectation is that a value being discarded
doesn’t require validation.  However, [validates()](#sqlalchemy.orm.validates) supports reception
of these events by specifying `include_removes=True` to the decorator.  When
this flag is set, the validation function must receive an additional boolean
argument which if `True` indicates that the operation is a removal:

```
from sqlalchemy.orm import validates

class User(Base):
    # ...

    addresses = relationship("Address")

    @validates("addresses", include_removes=True)
    def validate_address(self, key, address, is_remove):
        if is_remove:
            raise ValueError("not allowed to remove items from the collection")
        else:
            if "@" not in address.email:
                raise ValueError("failed simplified email validation")
            return address
```

The case where mutually dependent validators are linked via a backref
can also be tailored, using the `include_backrefs=False` option; this option,
when set to `False`, prevents a validation function from emitting if the
event occurs as a result of a backref:

```
from sqlalchemy.orm import validates

class User(Base):
    # ...

    addresses = relationship("Address", backref="user")

    @validates("addresses", include_backrefs=False)
    def validate_address(self, key, address):
        if "@" not in address:
            raise ValueError("failed simplified email validation")
        return address
```

Above, if we were to assign to `Address.user` as in `some_address.user = some_user`,
the `validate_address()` function would *not* be emitted, even though an append
occurs to `some_user.addresses` - the event is caused by a backref.

Note that the [validates()](#sqlalchemy.orm.validates) decorator is a convenience function built on
top of attribute events.   An application that requires more control over
configuration of attribute change behavior can make use of this system,
described at [AttributeEvents](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.AttributeEvents).

| Object Name | Description |
| --- | --- |
| validates(*names, [include_removes, include_backrefs]) | Decorate a method as a ‘validator’ for one or more named properties. |

   function sqlalchemy.orm.validates(**names:str*, *include_removes:bool=False*, *include_backrefs:bool=True*) → Callable[[_Fn], _Fn]

Decorate a method as a ‘validator’ for one or more named properties.

Designates a method as a validator, a method which receives the
name of the attribute as well as a value to be assigned, or in the
case of a collection, the value to be added to the collection.
The function can then raise validation exceptions to halt the
process from continuing (where Python’s built-in `ValueError`
and `AssertionError` exceptions are reasonable choices), or can
modify or replace the value before proceeding. The function should
otherwise return the given value.

Note that a validator for a collection **cannot** issue a load of that
collection within the validation routine - this usage raises
an assertion to avoid recursion overflows.  This is a reentrant
condition which is not supported.

  Parameters:

- ***names** – list of attribute names to be validated.
- **include_removes** – if True, “remove” events will be
  sent as well - the validation function must accept an additional
  argument “is_remove” which will be a boolean.
- **include_backrefs** –
  defaults to `True`; if `False`, the
  validation function will not emit if the originator is an attribute
  event related via a backref.  This can be used for bi-directional
  [validates()](#sqlalchemy.orm.validates) usage where only one validator should emit per
  attribute operation.
  Changed in version 2.0.16: This parameter inadvertently defaulted to
  `False` for releases 2.0.0 through 2.0.15.  Its correct default
  of `True` is restored in 2.0.16.

See also

[Simple Validators](#simple-validators) - usage examples for [validates()](#sqlalchemy.orm.validates)

## Using Custom Datatypes at the Core Level

A non-ORM means of affecting the value of a column in a way that suits
converting data between how it is represented in Python, vs. how it is
represented in the database, can be achieved by using a custom datatype that is
applied to the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata.     This is more common in the
case of some style of encoding / decoding that occurs both as data goes to the
database and as it is returned; read more about this in the Core documentation
at [Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator).

## Using Descriptors and Hybrids

A more comprehensive way to produce modified behavior for an attribute is to
use [descriptors](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptors).  These are commonly used in Python using the `property()`
function. The standard SQLAlchemy technique for descriptors is to create a
plain descriptor, and to have it read/write from a mapped attribute with a
different name. Below we illustrate this using Python 2.6-style properties:

```
class EmailAddress(Base):
    __tablename__ = "email_address"

    id = mapped_column(Integer, primary_key=True)

    # name the attribute with an underscore,
    # different from the column name
    _email = mapped_column("email", String)

    # then create an ".email" attribute
    # to get/set "._email"
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
```

The approach above will work, but there’s more we can add. While our
`EmailAddress` object will shuttle the value through the `email`
descriptor and into the `_email` mapped attribute, the class level
`EmailAddress.email` attribute does not have the usual expression semantics
usable with [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select). To provide these, we instead use the
[hybrid](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#module-sqlalchemy.ext.hybrid) extension as follows:

```
from sqlalchemy.ext.hybrid import hybrid_property

class EmailAddress(Base):
    __tablename__ = "email_address"

    id = mapped_column(Integer, primary_key=True)

    _email = mapped_column("email", String)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
```

The `.email` attribute, in addition to providing getter/setter behavior when we have an
instance of `EmailAddress`, also provides a SQL expression when used at the class level,
that is, from the `EmailAddress` class directly:

```
from sqlalchemy.orm import Session
from sqlalchemy import select

session = Session()

address = session.scalars(
    select(EmailAddress).where(EmailAddress.email == "[email protected]")
).one()
SELECT address.email AS address_email, address.id AS address_id
FROM address
WHERE address.email = ?
('[email protected]',)
address.email = "[email protected]"
session.commit()
UPDATE address SET email=? WHERE address.id = ?
('[email protected]', 1)
COMMIT
```

The [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) also allows us to change the behavior of the
attribute, including defining separate behaviors when the attribute is
accessed at the instance level versus at the class/expression level, using the
[hybrid_property.expression()](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.expression) modifier. Such as, if we wanted to add a
host name automatically, we might define two sets of string manipulation
logic:

```
class EmailAddress(Base):
    __tablename__ = "email_address"

    id = mapped_column(Integer, primary_key=True)

    _email = mapped_column("email", String)

    @hybrid_property
    def email(self):
        """Return the value of _email up until the last twelve
        characters."""

        return self._email[:-12]

    @email.setter
    def email(self, email):
        """Set the value of _email, tacking on the twelve character
        value @example.com."""

        self._email = email + "@example.com"

    @email.expression
    def email(cls):
        """Produce a SQL expression that represents the value
        of the _email column, minus the last twelve characters."""

        return func.substr(cls._email, 1, func.length(cls._email) - 12)
```

Above, accessing the `email` property of an instance of `EmailAddress`
will return the value of the `_email` attribute, removing or adding the
hostname `@example.com` from the value. When we query against the `email`
attribute, a SQL function is rendered which produces the same effect:

```
address = session.scalars(
    select(EmailAddress).where(EmailAddress.email == "address")
).one()
SELECT address.email AS address_email, address.id AS address_id
FROM address
WHERE substr(address.email, ?, length(address.email) - ?) = ?
(1, 12, 'address')
```

Read more about Hybrids at [Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html).

## Synonyms

Synonyms are a mapper-level construct that allow any attribute on a class
to “mirror” another attribute that is mapped.

In the most basic sense, the synonym is an easy way to make a certain
attribute available by an additional name:

```
from sqlalchemy.orm import synonym

class MyClass(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)
    job_status = mapped_column(String(50))

    status = synonym("job_status")
```

The above class `MyClass` has two attributes, `.job_status` and
`.status` that will behave as one attribute, both at the expression
level:

```
>>> print(MyClass.job_status == "some_status")
my_table.job_status = :job_status_1
>>> print(MyClass.status == "some_status")
my_table.job_status = :job_status_1
```

and at the instance level:

```
>>> m1 = MyClass(status="x")
>>> m1.status, m1.job_status
('x', 'x')

>>> m1.job_status = "y"
>>> m1.status, m1.job_status
('y', 'y')
```

The [synonym()](#sqlalchemy.orm.synonym) can be used for any kind of mapped attribute that
subclasses [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty), including mapped columns and relationships,
as well as synonyms themselves.

Beyond a simple mirror, [synonym()](#sqlalchemy.orm.synonym) can also be made to reference
a user-defined [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).  We can supply our
`status` synonym with a `@property`:

```
class MyClass(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)
    status = mapped_column(String(50))

    @property
    def job_status(self):
        return "Status: " + self.status

    job_status = synonym("status", descriptor=job_status)
```

When using Declarative, the above pattern can be expressed more succinctly
using the [synonym_for()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.synonym_for) decorator:

```
from sqlalchemy.ext.declarative import synonym_for

class MyClass(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)
    status = mapped_column(String(50))

    @synonym_for("status")
    @property
    def job_status(self):
        return "Status: " + self.status
```

While the [synonym()](#sqlalchemy.orm.synonym) is useful for simple mirroring, the use case
of augmenting attribute behavior with descriptors is better handled in modern
usage using the [hybrid attribute](#mapper-hybrids) feature, which
is more oriented towards Python descriptors.   Technically, a [synonym()](#sqlalchemy.orm.synonym)
can do everything that a [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) can do, as it also supports
injection of custom SQL capabilities, but the hybrid is more straightforward
to use in more complex situations.

| Object Name | Description |
| --- | --- |
| synonym(name, *, [map_column, descriptor, comparator_factory, init, repr, default, default_factory, compare, kw_only, hash, info, doc, dataclass_metadata]) | Denote an attribute name as a synonym to a mapped property,
in that the attribute will mirror the value and expression behavior
of another attribute. |

   function sqlalchemy.orm.synonym(*name:str*, ***, *map_column:bool|None=None*, *descriptor:Any|None=None*, *comparator_factory:Type[PropComparator[_T]]|None=None*, *init:_NoArg|bool=_NoArg.NO_ARG*, *repr:_NoArg|bool=_NoArg.NO_ARG*, *default:_NoArg|_T=_NoArg.NO_ARG*, *default_factory:_NoArg|Callable[[],_T]=_NoArg.NO_ARG*, *compare:_NoArg|bool=_NoArg.NO_ARG*, *kw_only:_NoArg|bool=_NoArg.NO_ARG*, *hash:_NoArg|bool|None=_NoArg.NO_ARG*, *info:_InfoType|None=None*, *doc:str|None=None*, *dataclass_metadata:_NoArg|Mapping[Any,Any]|None=_NoArg.NO_ARG*) → [Synonym](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Synonym)[Any]

Denote an attribute name as a synonym to a mapped property,
in that the attribute will mirror the value and expression behavior
of another attribute.

e.g.:

```
class MyClass(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True)
    job_status = Column(String(50))

    status = synonym("job_status")
```

   Parameters:

- **name** – the name of the existing mapped property.  This
  can refer to the string name ORM-mapped attribute
  configured on the class, including column-bound attributes
  and relationships.
- **descriptor** – a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor) that will be used
  as a getter (and potentially a setter) when this attribute is
  accessed at the instance level.
- **map_column** –
  **For classical mappings and mappings against
  an existing Table object only**.  if `True`, the [synonym()](#sqlalchemy.orm.synonym)
  construct will locate the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  object upon the mapped
  table that would normally be associated with the attribute name of
  this synonym, and produce a new [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) that instead
  maps this [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  to the alternate name given as the “name”
  argument of the synonym; in this way, the usual step of redefining
  the mapping of the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  to be under a different name is
  unnecessary. This is usually intended to be used when a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  is to be replaced with an attribute that also uses a
  descriptor, that is, in conjunction with the
  [synonym.descriptor](#sqlalchemy.orm.synonym.params.descriptor) parameter:
  ```
  my_table = Table(
      "my_table",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("job_status", String(50)),
  )
  class MyClass:
      @property
      def _job_status_descriptor(self):
          return "Status: %s" % self._job_status
  mapper(
      MyClass,
      my_table,
      properties={
          "job_status": synonym(
              "_job_status",
              map_column=True,
              descriptor=MyClass._job_status_descriptor,
          )
      },
  )
  ```
  Above, the attribute named `_job_status` is automatically
  mapped to the `job_status` column:
  ```
  >>> j1 = MyClass()
  >>> j1._job_status = "employed"
  >>> j1.job_status
  Status: employed
  ```
  When using Declarative, in order to provide a descriptor in
  conjunction with a synonym, use the
  `sqlalchemy.ext.declarative.synonym_for()` helper.  However,
  note that the [hybrid properties](#mapper-hybrids) feature
  should usually be preferred, particularly when redefining attribute
  behavior.
- **info** – Optional data dictionary which will be populated into the
  `InspectionAttr.info` attribute of this object.
- **comparator_factory** –
  A subclass of [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)
  that will provide custom comparison behavior at the SQL expression
  level.
  Note
  For the use case of providing an attribute which redefines both
  Python-level and SQL-expression level behavior of an attribute,
  please refer to the Hybrid attribute introduced at
  [Using Descriptors and Hybrids](#mapper-hybrids) for a more effective technique.

See also

[Synonyms](#synonyms) - Overview of synonyms

[synonym_for()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.synonym_for) - a helper oriented towards Declarative

[Using Descriptors and Hybrids](#mapper-hybrids) - The Hybrid Attribute extension provides an
updated approach to augmenting attribute behavior more flexibly
than can be achieved with synonyms.

## Operator Customization

The “operators” used by the SQLAlchemy ORM and Core expression language
are fully customizable.  For example, the comparison expression
`User.name == 'ed'` makes usage of an operator built into Python
itself called `operator.eq` - the actual SQL construct which SQLAlchemy
associates with such an operator can be modified.  New
operations can be associated with column expressions as well.   The operators
which take place for column expressions are most directly redefined at the
type level -  see the
section [Redefining and Creating New Operators](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-operators) for a description.

ORM level functions like [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship),
and [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) also provide for operator redefinition at the ORM
level, by passing a [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator) subclass to the `comparator_factory`
argument of each function.  Customization of operators at this level is a
rare use case.  See the documentation at [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)
for an overview.

---

# SQLAlchemy 2.0 Documentation

# SQL Expressions as Mapped Attributes

Attributes on a mapped class can be linked to SQL expressions, which can
be used in queries.

## Using a Hybrid

The easiest and most flexible way to link relatively simple SQL expressions to a class is to use a so-called
“hybrid attribute”,
described in the section [Hybrid Attributes](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html).  The hybrid provides
for an expression that works at both the Python level as well as at the
SQL expression level.  For example, below we map a class `User`,
containing attributes `firstname` and `lastname`, and include a hybrid that
will provide for us the `fullname`, which is the string concatenation of the two:

```
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname
```

Above, the `fullname` attribute is interpreted at both the instance and
class level, so that it is available from an instance:

```
some_user = session.scalars(select(User).limit(1)).first()
print(some_user.fullname)
```

as well as usable within queries:

```
some_user = session.scalars(
    select(User).where(User.fullname == "John Smith").limit(1)
).first()
```

The string concatenation example is a simple one, where the Python expression
can be dual purposed at the instance and class level.  Often, the SQL expression
must be distinguished from the Python expression, which can be achieved using
[hybrid_property.expression()](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property.expression).  Below we illustrate the case where a conditional
needs to be present inside the hybrid, using the `if` statement in Python and the
[case()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.case) construct for SQL expressions:

```
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))

    @hybrid_property
    def fullname(self):
        if self.firstname is not None:
            return self.firstname + " " + self.lastname
        else:
            return self.lastname

    @fullname.expression
    def fullname(cls):
        return case(
            (cls.firstname != None, cls.firstname + " " + cls.lastname),
            else_=cls.lastname,
        )
```

## Using column_property

The [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) function can be used to map a SQL
expression in a manner similar to a regularly mapped [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
With this technique, the attribute is loaded
along with all other column-mapped attributes at load time.  This is in some
cases an advantage over the usage of hybrids, as the value can be loaded
up front at the same time as the parent row of the object, particularly if
the expression is one which links to other tables (typically as a correlated
subquery) to access data that wouldn’t normally be
available on an already loaded object.

Disadvantages to using [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) for SQL expressions include that
the expression must be compatible with the SELECT statement emitted for the class
as a whole, and there are also some configurational quirks which can occur
when using [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) from declarative mixins.

Our “fullname” example can be expressed using [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) as
follows:

```
from sqlalchemy.orm import column_property

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))
    fullname = column_property(firstname + " " + lastname)
```

Correlated subqueries may be used as well. Below we use the
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct to create a [ScalarSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect),
representing a column-oriented SELECT statement, that links together the count
of `Address` objects available for a particular `User`:

```
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Address(Base):
    __tablename__ = "address"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("user.id"))

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    address_count = column_property(
        select(func.count(Address.id))
        .where(Address.user_id == id)
        .correlate_except(Address)
        .scalar_subquery()
    )
```

In the above example, we define a [ScalarSelect()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.ScalarSelect) construct like the following:

```
stmt = (
    select(func.count(Address.id))
    .where(Address.user_id == id)
    .correlate_except(Address)
    .scalar_subquery()
)
```

Above, we first use [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) to create a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
construct, which we then convert into a [scalar subquery](https://docs.sqlalchemy.org/en/20/glossary.html#term-scalar-subquery) using the
[Select.scalar_subquery()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.scalar_subquery) method, indicating our intent to use this
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) statement in a column expression context.

Within the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) itself, we select the count of `Address.id` rows
where the `Address.user_id` column is equated to `id`, which in the context
of the `User` class is the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) named `id` (note that `id` is
also the name of a Python built in function, which is not what we want to use
here - if we were outside of the `User` class definition, we’d use `User.id`).

The [Select.correlate_except()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.correlate_except) method indicates that each element in the
FROM clause of this [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) may be omitted from the FROM list (that is, correlated
to the enclosing SELECT statement against `User`) except for the one corresponding
to `Address`.  This isn’t strictly necessary, but prevents `Address` from
being inadvertently omitted from the FROM list in the case of a long string
of joins between `User` and `Address` tables where SELECT statements against
`Address` are nested.

For a [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) that refers to columns linked from a
many-to-many relationship, use [and_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.and_) to join the fields of the
association table to both tables in a relationship:

```
from sqlalchemy import and_

class Author(Base):
    # ...

    book_count = column_property(
        select(func.count(books.c.id))
        .where(
            and_(
                book_authors.c.author_id == authors.c.id,
                book_authors.c.book_id == books.c.id,
            )
        )
        .scalar_subquery()
    )
```

### Adding column_property() to an existing Declarative mapped class

If import issues prevent the [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) from being defined
inline with the class, it can be assigned to the class after both
are configured.   When using mappings that make use of a Declarative
base class (i.e. produced by the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) superclass
or legacy functions such as [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base)),
this attribute assignment has the effect of calling [Mapper.add_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_property)
to add an additional property after the fact:

```
# only works if a declarative base class is in use
User.address_count = column_property(
    select(func.count(Address.id)).where(Address.user_id == User.id).scalar_subquery()
)
```

When using mapping styles that don’t use Declarative base classes
such as the [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator, the [Mapper.add_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_property)
method may be invoked explicitly on the underlying [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object,
which can be obtained using [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect):

```
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped
class User:
    __tablename__ = "user"

    # ... additional mapping directives

# later ...

# works for any kind of mapping
from sqlalchemy import inspect

inspect(User).add_property(
    column_property(
        select(func.count(Address.id))
        .where(Address.user_id == User.id)
        .scalar_subquery()
    )
)
```

See also

[Appending additional columns to an existing Declarative mapped class](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-adding-columns)

### Composing from Column Properties at Mapping Time

It is possible to create mappings that combine multiple
[ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) objects together.  The [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) will
be interpreted as a SQL expression when used in a Core expression context,
provided that it is targeted by an existing expression object; this works by
the Core detecting that the object has a `__clause_element__()` method which
returns a SQL expression.   However, if the [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) is used as
a lead object in an expression where there is no other Core SQL expression
object to target it, the [ColumnProperty.expression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.expression) attribute will
return the underlying SQL expression so that it can be used to build SQL
expressions consistently.  Below, the `File` class contains an attribute
`File.path` that concatenates a string token to the `File.filename`
attribute, which is itself a [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty):

```
class File(Base):
    __tablename__ = "file"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(64))
    extension = mapped_column(String(8))
    filename = column_property(name + "." + extension)
    path = column_property("C:/" + filename.expression)
```

When the `File` class is used in expressions normally, the attributes
assigned to `filename` and `path` are usable directly.  The use of the
[ColumnProperty.expression](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty.expression) attribute is only necessary when using
the [ColumnProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.ColumnProperty) directly within the mapping definition:

```
stmt = select(File.path).where(File.filename == "foo.txt")
```

### Using Column Deferral withcolumn_property()

The column deferral feature introduced in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
at [Limiting which Columns Load with Column Deferral](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-column-deferral) may be applied at mapping time
to a SQL expression mapped by [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property) by using the
[deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred) function in place of [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property):

```
from sqlalchemy.orm import deferred

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    fullname: Mapped[str] = deferred(firstname + " " + lastname)
```

See also

[Using deferred() for imperative mappers, mapped SQL expressions](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-deferred-imperative)

## Using a plain descriptor

In cases where a SQL query more elaborate than what [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property)
or [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property) can provide must be emitted, a regular Python
function accessed as an attribute can be used, assuming the expression
only needs to be available on an already-loaded instance.   The function
is decorated with Python’s own `@property` decorator to mark it as a read-only
attribute.   Within the function, [object_session()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.object_session)
is used to locate the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) corresponding to the current object,
which is then used to emit a query:

```
from sqlalchemy.orm import object_session
from sqlalchemy import select, func

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))

    @property
    def address_count(self):
        return object_session(self).scalar(
            select(func.count(Address.id)).where(Address.user_id == self.id)
        )
```

The plain descriptor approach is useful as a last resort, but is less performant
in the usual case than both the hybrid and column property approaches, in that
it needs to emit a SQL query upon each access.

## Query-time SQL expressions as mapped attributes

In addition to being able to configure fixed SQL expressions on mapped classes,
the SQLAlchemy ORM also includes a feature wherein objects may be loaded
with the results of arbitrary SQL expressions which are set up at query time as part
of their state.  This behavior is available by configuring an ORM mapped
attribute using [query_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.query_expression) and then using the
[with_expression()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.with_expression) loader option at query time.  See the section
[Loading Arbitrary SQL Expressions onto Objects](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-with-expression) for an example mapping and usage.

---

# SQLAlchemy 2.0 Documentation

# ORM Mapped Class Configuration

Detailed reference for ORM configuration, not including
relationships, which are detailed at
[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html).

For a quick look at a typical ORM configuration, start with
[ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html#orm-quickstart).

For an introduction to the concept of object relational mapping as implemented
in SQLAlchemy, it’s first introduced in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial) at
[Using ORM Declarative Forms to Define Table Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-orm-table-metadata).

- [ORM Mapped Class Overview](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
  - [ORM Mapping Styles](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles)
    - [Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping)
    - [Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping)
  - [Mapped Class Essential Components](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#mapped-class-essential-components)
    - [The class to be mapped](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#the-class-to-be-mapped)
    - [The table, or other from clause object](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#the-table-or-other-from-clause-object)
    - [The properties dictionary](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#the-properties-dictionary)
    - [Other mapper configuration parameters](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#other-mapper-configuration-parameters)
  - [Mapped Class Behavior](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#mapped-class-behavior)
    - [Default Constructor](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#default-constructor)
    - [Maintaining Non-Mapped State Across Loads](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#maintaining-non-mapped-state-across-loads)
    - [Runtime Introspection of Mapped classes, Instances and Mappers](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#runtime-introspection-of-mapped-classes-instances-and-mappers)
      - [Inspection of Mapper objects](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#inspection-of-mapper-objects)
      - [Inspection of Mapped Instances](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#inspection-of-mapped-instances)
- [Mapping Classes with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)
  - [Declarative Mapping Styles](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html)
    - [Using a Declarative Base Class](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#using-a-declarative-base-class)
    - [Declarative Mapping using a Decorator (no declarative base)](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#declarative-mapping-using-a-decorator-no-declarative-base)
  - [Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html)
    - [Declarative Table withmapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#declarative-table-with-mapped-column)
      - [ORM Annotated Declarative - Automated Mapping with Type Annotations](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-annotated-declarative-automated-mapping-with-type-annotations)
      - [Dataclass features inmapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#dataclass-features-in-mapped-column)
      - [Accessing Table and Metadata](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#accessing-table-and-metadata)
      - [Declarative Table Configuration](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#declarative-table-configuration)
      - [Explicit Schema Name with Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#explicit-schema-name-with-declarative-table)
      - [Setting Load and Persistence Options for Declarative Mapped Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#setting-load-and-persistence-options-for-declarative-mapped-columns)
      - [Naming Declarative Mapped Columns Explicitly](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#naming-declarative-mapped-columns-explicitly)
      - [Appending additional columns to an existing Declarative mapped class](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#appending-additional-columns-to-an-existing-declarative-mapped-class)
    - [ORM Annotated Declarative - Complete Guide](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-annotated-declarative-complete-guide)
      - [mapped_column()derives the datatype and nullability from theMappedannotation](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation)
      - [Customizing the Type Map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#customizing-the-type-map)
      - [Union types inside the Type Map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#union-types-inside-the-type-map)
      - [Support for Type Alias Types (defined by PEP 695) and NewType](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#support-for-type-alias-types-defined-by-pep-695-and-newtype)
      - [Mapping Multiple Type Configurations to Python Types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-multiple-type-configurations-to-python-types)
      - [Mapping Whole Column Declarations to Python Types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-whole-column-declarations-to-python-types)
      - [Using PythonEnumor pep-586Literaltypes in the type map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-python-enum-or-pep-586-literal-types-in-the-type-map)
    - [Declarative with Imperative Table (a.k.a. Hybrid Declarative)](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#declarative-with-imperative-table-a-k-a-hybrid-declarative)
      - [Alternate Attribute Names for Mapping Table Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#alternate-attribute-names-for-mapping-table-columns)
      - [Applying Load, Persistence and Mapping Options for Imperative Table Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#applying-load-persistence-and-mapping-options-for-imperative-table-columns)
    - [Mapping Declaratively with Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-declaratively-with-reflected-tables)
      - [Using DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-deferredreflection)
      - [Using Automap](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-automap)
      - [Automating Column Naming Schemes from Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#automating-column-naming-schemes-from-reflected-tables)
      - [Mapping to an Explicit Set of Primary Key Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-to-an-explicit-set-of-primary-key-columns)
      - [Mapping a Subset of Table Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-a-subset-of-table-columns)
  - [Mapper Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html)
    - [Defining Mapped Properties with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#defining-mapped-properties-with-declarative)
    - [Mapper Configuration Options with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#mapper-configuration-options-with-declarative)
      - [Constructing mapper arguments dynamically](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#constructing-mapper-arguments-dynamically)
    - [Other Declarative Mapping Directives](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#other-declarative-mapping-directives)
      - [__declare_last__()](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#declare-last)
      - [__declare_first__()](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#declare-first)
      - [metadata](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#metadata)
      - [__abstract__](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#abstract)
      - [__table_cls__](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#table-cls)
  - [Composing Mapped Hierarchies with Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html)
    - [Augmenting the Base](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#augmenting-the-base)
    - [Mixing in Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#mixing-in-columns)
    - [Mixing in Relationships](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#mixing-in-relationships)
    - [Mixing in_orm.column_property()and other_orm.MapperPropertyclasses](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#mixing-in-orm-column-property-and-other-orm-mapperproperty-classes)
    - [Using Mixins and Base Classes with Mapped Inheritance Patterns](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#using-mixins-and-base-classes-with-mapped-inheritance-patterns)
      - [Using_orm.declared_attr()with inheritingTableandMapperarguments](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#using-orm-declared-attr-with-inheriting-table-and-mapper-arguments)
      - [Using_orm.declared_attr()to generate table-specific inheriting columns](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#using-orm-declared-attr-to-generate-table-specific-inheriting-columns)
    - [Combining Table/Mapper Arguments from Multiple Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#combining-table-mapper-arguments-from-multiple-mixins)
    - [Creating Indexes and Constraints with Naming Conventions on Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#creating-indexes-and-constraints-with-naming-conventions-on-mixins)
- [Integration with dataclasses and attrs](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html)
  - [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#declarative-dataclass-mapping)
    - [Class level feature configuration](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#class-level-feature-configuration)
    - [Attribute Configuration](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#attribute-configuration)
      - [Column Defaults](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#column-defaults)
      - [Integration with Annotated](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#integration-with-annotated)
    - [Using mixins and abstract superclasses](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#using-mixins-and-abstract-superclasses)
    - [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#relationship-configuration)
    - [Using Non-Mapped Dataclass Fields](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#using-non-mapped-dataclass-fields)
    - [Integrating with Alternate Dataclass Providers such as Pydantic](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#integrating-with-alternate-dataclass-providers-such-as-pydantic)
  - [Applying ORM Mappings to an existing dataclass (legacy dataclass use)](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#applying-orm-mappings-to-an-existing-dataclass-legacy-dataclass-use)
    - [Mapping pre-existing dataclasses using Declarative With Imperative Table](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#mapping-pre-existing-dataclasses-using-declarative-with-imperative-table)
    - [Mapping pre-existing dataclasses using Declarative-style fields](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#mapping-pre-existing-dataclasses-using-declarative-style-fields)
      - [Using Declarative Mixins with pre-existing dataclasses](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#using-declarative-mixins-with-pre-existing-dataclasses)
    - [Mapping pre-existing dataclasses using Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#mapping-pre-existing-dataclasses-using-imperative-mapping)
  - [Applying ORM mappings to an existing attrs class](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#applying-orm-mappings-to-an-existing-attrs-class)
- [SQL Expressions as Mapped Attributes](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html)
  - [Using a Hybrid](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#using-a-hybrid)
  - [Using column_property](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#using-column-property)
    - [Adding column_property() to an existing Declarative mapped class](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#adding-column-property-to-an-existing-declarative-mapped-class)
    - [Composing from Column Properties at Mapping Time](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#composing-from-column-properties-at-mapping-time)
    - [Using Column Deferral withcolumn_property()](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#using-column-deferral-with-column-property)
  - [Using a plain descriptor](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#using-a-plain-descriptor)
  - [Query-time SQL expressions as mapped attributes](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#query-time-sql-expressions-as-mapped-attributes)
- [Changing Attribute Behavior](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html)
  - [Simple Validators](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#simple-validators)
    - [validates()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.validates)
  - [Using Custom Datatypes at the Core Level](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#using-custom-datatypes-at-the-core-level)
  - [Using Descriptors and Hybrids](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#using-descriptors-and-hybrids)
  - [Synonyms](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#synonyms)
    - [synonym()](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#sqlalchemy.orm.synonym)
  - [Operator Customization](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#operator-customization)
- [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html)
  - [Working with Mapped Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html#working-with-mapped-composite-column-types)
  - [Other mapping forms for composites](https://docs.sqlalchemy.org/en/20/orm/composites.html#other-mapping-forms-for-composites)
    - [Map columns directly, then pass to composite](https://docs.sqlalchemy.org/en/20/orm/composites.html#map-columns-directly-then-pass-to-composite)
    - [Map columns directly, pass attribute names to composite](https://docs.sqlalchemy.org/en/20/orm/composites.html#map-columns-directly-pass-attribute-names-to-composite)
    - [Imperative mapping and imperative table](https://docs.sqlalchemy.org/en/20/orm/composites.html#imperative-mapping-and-imperative-table)
  - [Using Legacy Non-Dataclasses](https://docs.sqlalchemy.org/en/20/orm/composites.html#using-legacy-non-dataclasses)
  - [Tracking In-Place Mutations on Composites](https://docs.sqlalchemy.org/en/20/orm/composites.html#tracking-in-place-mutations-on-composites)
  - [Redefining Comparison Operations for Composites](https://docs.sqlalchemy.org/en/20/orm/composites.html#redefining-comparison-operations-for-composites)
  - [Nesting Composites](https://docs.sqlalchemy.org/en/20/orm/composites.html#nesting-composites)
  - [Composite API](https://docs.sqlalchemy.org/en/20/orm/composites.html#composite-api)
    - [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
- [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html)
  - [Joined Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance)
    - [Relationships with Joined Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#relationships-with-joined-inheritance)
    - [Loading Joined Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#loading-joined-inheritance-mappings)
  - [Single Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#single-table-inheritance)
    - [Resolving Column Conflicts withuse_existing_column](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#resolving-column-conflicts-with-use-existing-column)
    - [Relationships with Single Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#relationships-with-single-table-inheritance)
    - [Building Deeper Hierarchies withpolymorphic_abstract](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#building-deeper-hierarchies-with-polymorphic-abstract)
    - [Loading Single Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#loading-single-inheritance-mappings)
  - [Concrete Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#concrete-table-inheritance)
    - [Concrete Polymorphic Loading Configuration](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#concrete-polymorphic-loading-configuration)
    - [Abstract Concrete Classes](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#abstract-concrete-classes)
    - [Classical and Semi-Classical Concrete Polymorphic Configuration](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#classical-and-semi-classical-concrete-polymorphic-configuration)
    - [Relationships with Concrete Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#relationships-with-concrete-inheritance)
    - [Loading Concrete Inheritance Mappings](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#loading-concrete-inheritance-mappings)
- [Non-Traditional Mappings](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html)
  - [Mapping a Class against Multiple Tables](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html#mapping-a-class-against-multiple-tables)
  - [Mapping a Class against Arbitrary Subqueries](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html#mapping-a-class-against-arbitrary-subqueries)
  - [Multiple Mappers for One Class](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html#multiple-mappers-for-one-class)
- [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html)
  - [Simple Version Counting](https://docs.sqlalchemy.org/en/20/orm/versioning.html#simple-version-counting)
  - [Custom Version Counters / Types](https://docs.sqlalchemy.org/en/20/orm/versioning.html#custom-version-counters-types)
  - [Server Side Version Counters](https://docs.sqlalchemy.org/en/20/orm/versioning.html#server-side-version-counters)
  - [Programmatic or Conditional Version Counters](https://docs.sqlalchemy.org/en/20/orm/versioning.html#programmatic-or-conditional-version-counters)
- [Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
  - [add_mapped_attribute()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.add_mapped_attribute)
  - [as_declarative()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.as_declarative)
  - [class_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.class_mapper)
  - [clear_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.clear_mappers)
  - [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property)
  - [configure_mappers()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.configure_mappers)
  - [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base)
  - [declarative_mixin()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_mixin)
  - [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase)
    - [DeclarativeBase.__mapper__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__mapper__)
    - [DeclarativeBase.__mapper_args__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__mapper_args__)
    - [DeclarativeBase.__table__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__table__)
    - [DeclarativeBase.__table_args__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__table_args__)
    - [DeclarativeBase.__tablename__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__tablename__)
    - [DeclarativeBase.metadata](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.metadata)
    - [DeclarativeBase.registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.registry)
  - [DeclarativeBaseNoMeta](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta)
    - [DeclarativeBaseNoMeta.__mapper__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.__mapper__)
    - [DeclarativeBaseNoMeta.__mapper_args__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.__mapper_args__)
    - [DeclarativeBaseNoMeta.__table__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.__table__)
    - [DeclarativeBaseNoMeta.__table_args__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.__table_args__)
    - [DeclarativeBaseNoMeta.__tablename__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.__tablename__)
    - [DeclarativeBaseNoMeta.metadata](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.metadata)
    - [DeclarativeBaseNoMeta.registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBaseNoMeta.registry)
  - [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr)
    - [declared_attr.cascading](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.cascading)
    - [declared_attr.directive](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr.directive)
  - [has_inherited_table()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.has_inherited_table)
  - [identity_key()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.util.identity_key)
  - [mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_as_dataclass)
  - [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
  - [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass)
  - [MappedClassProtocol](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedClassProtocol)
  - [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
    - [Mapper.__init__()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.__init__)
    - [Mapper.add_properties()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_properties)
    - [Mapper.add_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.add_property)
    - [Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)
    - [Mapper.attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.attrs)
    - [Mapper.base_mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.base_mapper)
    - [Mapper.c](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.c)
    - [Mapper.cascade_iterator()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.cascade_iterator)
    - [Mapper.class_](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.class_)
    - [Mapper.class_manager](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.class_manager)
    - [Mapper.column_attrs](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.column_attrs)
    - [Mapper.columns](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.columns)
    - [Mapper.common_parent()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.common_parent)
    - [Mapper.composites](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.composites)
    - [Mapper.concrete](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.concrete)
    - [Mapper.configured](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.configured)
    - [Mapper.entity](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.entity)
    - [Mapper.get_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.get_property)
    - [Mapper.get_property_by_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.get_property_by_column)
    - [Mapper.identity_key_from_instance()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.identity_key_from_instance)
    - [Mapper.identity_key_from_primary_key()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.identity_key_from_primary_key)
    - [Mapper.identity_key_from_row()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.identity_key_from_row)
    - [Mapper.inherits](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.inherits)
    - [Mapper.is_mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.is_mapper)
    - [Mapper.is_sibling()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.is_sibling)
    - [Mapper.isa()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.isa)
    - [Mapper.iterate_properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.iterate_properties)
    - [Mapper.local_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.local_table)
    - [Mapper.mapped_table](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.mapped_table)
    - [Mapper.mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.mapper)
    - [Mapper.non_primary](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.non_primary)
    - [Mapper.persist_selectable](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.persist_selectable)
    - [Mapper.polymorphic_identity](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.polymorphic_identity)
    - [Mapper.polymorphic_iterator()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.polymorphic_iterator)
    - [Mapper.polymorphic_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.polymorphic_map)
    - [Mapper.polymorphic_on](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.polymorphic_on)
    - [Mapper.primary_key](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.primary_key)
    - [Mapper.primary_key_from_instance()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.primary_key_from_instance)
    - [Mapper.primary_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.primary_mapper)
    - [Mapper.relationships](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.relationships)
    - [Mapper.selectable](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.selectable)
    - [Mapper.self_and_descendants](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.self_and_descendants)
    - [Mapper.single](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.single)
    - [Mapper.synonyms](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.synonyms)
    - [Mapper.tables](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.tables)
    - [Mapper.validators](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.validators)
    - [Mapper.with_polymorphic_mappers](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.with_polymorphic_mappers)
  - [object_mapper()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.object_mapper)
  - [orm_insert_sentinel()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.orm_insert_sentinel)
  - [polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union)
  - [reconstructor()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.reconstructor)
  - [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)
    - [registry.__init__()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.__init__)
    - [registry.as_declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.as_declarative_base)
    - [registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure)
    - [registry.dispose()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.dispose)
    - [registry.generate_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base)
    - [registry.map_declaratively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_declaratively)
    - [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively)
    - [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped)
    - [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass)
    - [registry.mappers](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mappers)
    - [registry.update_type_annotation_map()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.update_type_annotation_map)
  - [synonym_for()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.synonym_for)
