# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Integration with dataclasses and attrs

SQLAlchemy as of version 2.0 features “native dataclass” integration where
an [Annotated Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column)
mapping may be turned into a Python [dataclass](https://docs.python.org/3/library/dataclasses.html) by adding a single mixin
or decorator to mapped classes.

Added in version 2.0: Integrated dataclass creation with ORM Declarative classes

There are also patterns available that allow existing dataclasses to be
mapped, as well as to map classes instrumented by the
[attrs](https://pypi.org/project/attrs/) third party integration library.

## Declarative Dataclass Mapping

SQLAlchemy [Annotated Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column)
mappings may be augmented with an additional
mixin class or decorator directive, which will add an additional step to
the Declarative process after the mapping is complete that will convert
the mapped class **in-place** into a Python [dataclass](https://docs.python.org/3/library/dataclasses.html), before completing
the mapping process which applies ORM-specific [instrumentation](https://docs.sqlalchemy.org/en/20/glossary.html#term-instrumentation)
to the class.   The most prominent behavioral addition this provides is
generation of an `__init__()` method with fine-grained control over
positional and keyword arguments with or without defaults, as well as
generation of methods like `__repr__()` and `__eq__()`.

From a [PEP 484](https://peps.python.org/pep-0484/) typing perspective, the class is recognized
as having Dataclass-specific behaviors, most notably  by taking advantage of [PEP 681](https://peps.python.org/pep-0681/)
“Dataclass Transforms”, which allows typing tools to consider the class
as though it were explicitly decorated using the `@dataclasses.dataclass`
decorator.

Note

Support for [PEP 681](https://peps.python.org/pep-0681/) in typing tools as of **April 4, 2023** is
limited and is currently known to be supported by [Pyright](https://github.com/microsoft/pyright) as well
as [Mypy](https://mypy.readthedocs.io/en/stable/) as of **version 1.2**.  Note that Mypy 1.1.1 introduced
[PEP 681](https://peps.python.org/pep-0681/) support but did not correctly accommodate Python descriptors
which will lead to errors when using SQLAlchemy’s ORM mapping scheme.

See also

[https://peps.python.org/pep-0681/#the-dataclass-transform-decorator](https://peps.python.org/pep-0681/#the-dataclass-transform-decorator) - background
on how libraries like SQLAlchemy enable [PEP 681](https://peps.python.org/pep-0681/) support

Dataclass conversion may be added to any Declarative class either by adding the
[MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) mixin to a [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class
hierarchy, or for decorator mapping by using the
[registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) class decorator.

The [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) mixin may be applied either
to the Declarative `Base` class or any superclass, as in the example
below:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

Or may be applied directly to classes that extend from the Declarative base:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass

class Base(DeclarativeBase):
    pass

class User(MappedAsDataclass, Base):
    """User class will be converted to a dataclass"""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

When using the decorator form, the [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass)
decorator is supported:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

The same method is available in a standalone function form, which may
have better compatibility with some versions of the mypy type checker:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_as_dataclass
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@mapped_as_dataclass(reg)
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

Added in version 2.0.44: Added [mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_as_dataclass) after observing
mypy compatibility issues with the method form of the same feature

### Class level feature configuration

Support for dataclasses features is partial.  Currently **supported** are
the `init`, `repr`, `eq`, `order` and `unsafe_hash` features,
`match_args` and `kw_only` are supported on Python 3.10+.
Currently **not supported** are the `frozen` and `slots` features.

When using the mixin class form with [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass),
class configuration arguments are passed as class-level parameters:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass

class Base(DeclarativeBase):
    pass

class User(MappedAsDataclass, Base, repr=False, unsafe_hash=True):
    """User class will be converted to a dataclass"""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

When using the decorator form with [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) or
[mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_as_dataclass), class configuration arguments are passed to
the decorator directly:

```
from sqlalchemy.orm import registry
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

reg = registry()

@reg.mapped_as_dataclass(unsafe_hash=True)
class User:
    """User class will be converted to a dataclass"""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
```

For background on dataclass class options, see the [dataclasses](https://docs.python.org/3/library/dataclasses.html) documentation
at [@dataclasses.dataclass](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass).

### Attribute Configuration

SQLAlchemy native dataclasses differ from normal dataclasses in that
attributes to be mapped are described using the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
generic annotation container in all cases.    Mappings follow the same
forms as those documented at [Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table), and all
features of [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) and [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) are supported.

Additionally, ORM attribute configuration constructs including
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) and [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
support **per-attribute field options**, including `init`, `default`,
`default_factory` and `repr`.  The names of these arguments is fixed
as specified in [PEP 681](https://peps.python.org/pep-0681/).   Functionality is equivalent to dataclasses:

- `init`, as in [mapped_column.init](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.init),
  [relationship.init](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.init), if False indicates the field should
  not be part of the `__init__()` method
- `default`, as in [mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default),
  [relationship.default](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default)
  indicates a default value for the field as given as a keyword argument
  in the `__init__()` method.
- `default_factory`, as in [mapped_column.default_factory](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default_factory),
  [relationship.default_factory](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default_factory), indicates a callable function
  that will be invoked to generate a new default value for a parameter
  if not passed explicitly to the `__init__()` method.
- `repr` True by default, indicates the field should be part of the generated
  `__repr__()` method

Another key difference from dataclasses is that default values for attributes
**must** be configured using the `default` parameter of the ORM construct,
such as `mapped_column(default=None)`.   A syntax that resembles dataclass
syntax which accepts simple Python values as defaults without using
`@dataclases.field()` is not supported.

As an example using [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column), the mapping below will
produce an `__init__()` method that accepts only the fields `name` and
`fullname`, where `name` is required and may be passed positionally,
and `fullname` is optional.  The `id` field, which we expect to be
database-generated, is not part of the constructor at all:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(default=None)

# 'fullname' is optional keyword argument
u1 = User("name")
```

#### Column Defaults

In order to accommodate the name overlap of the `default` argument with
the existing [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) parameter of the  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
construct, the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct disambiguates the two
names by adding a new parameter [mapped_column.insert_default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.insert_default),
which will be populated directly into the
[Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) parameter of  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
independently of what may be set on
[mapped_column.default](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.default), which is always used for the
dataclasses configuration.  For example, to configure a datetime column with
a [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) set to the `func.utc_timestamp()` SQL function,
but where the parameter is optional in the constructor:

```
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.utc_timestamp(), default=None
    )
```

With the above mapping, an `INSERT` for a new `User` object where no
parameter for `created_at` were passed proceeds as:

```
>>> with Session(e) as session:
...     session.add(User())
...     session.commit()
BEGIN (implicit)
INSERT INTO user_account (created_at) VALUES (utc_timestamp())
[generated in 0.00010s] ()
COMMIT
```

#### Integration with Annotated

The approach introduced at [Mapping Whole Column Declarations to Python Types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-pep593)
illustrates how to use [PEP 593](https://peps.python.org/pep-0593/) `Annotated` objects to package whole
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) constructs for reuse.  While `Annotated` objects
can be combined with the use of dataclasses, **dataclass-specific keyword
arguments unfortunately cannot be used within the Annotated construct**.  This
includes [PEP 681](https://peps.python.org/pep-0681/)-specific arguments `init`, `default`, `repr`, and
`default_factory`, which **must** be present in a [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
or similar construct inline with the class attribute.

Changed in version 2.0.14/2.0.22: the `Annotated` construct when used with
an ORM construct like [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) cannot accommodate dataclass
field parameters such as `init` and `repr` - this use goes against the
design of Python dataclasses and is not supported by [PEP 681](https://peps.python.org/pep-0681/), and therefore
is also rejected by the SQLAlchemy ORM at runtime.   A deprecation warning
is now emitted and the attribute will be ignored.

As an example, the `init=False` parameter below will be ignored and additionally
emit a deprecation warning:

```
from typing import Annotated

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

# typing tools as well as SQLAlchemy will ignore init=False here
intpk = Annotated[int, mapped_column(init=False, primary_key=True)]

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"
    id: Mapped[intpk]

# typing error as well as runtime error: Argument missing for parameter "id"
u1 = User()
```

Instead, [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) must be present on the right side
as well with an explicit setting for [mapped_column.init](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.init);
the other arguments can remain within the `Annotated` construct:

```
from typing import Annotated

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

intpk = Annotated[int, mapped_column(primary_key=True)]

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    # init=False and other pep-681 arguments must be inline
    id: Mapped[intpk] = mapped_column(init=False)

u1 = User()
```

### Using mixins and abstract superclasses

Any mixins or base classes that are used in a [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass)
mapped class which include [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) attributes must themselves be
part of a [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass)
hierarchy, such as in the example below using a mixin:

```
class Mixin(MappedAsDataclass):
    create_user: Mapped[int] = mapped_column()
    update_user: Mapped[Optional[int]] = mapped_column(default=None, init=False)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class User(Base, Mixin):
    __tablename__ = "sys_user"

    uid: Mapped[str] = mapped_column(
        String(50), init=False, default_factory=uuid4, primary_key=True
    )
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
```

Python type checkers which support [PEP 681](https://peps.python.org/pep-0681/) will otherwise not consider
attributes from non-dataclass mixins to be part of the dataclass.

Deprecated since version 2.0.8: Using mixins and abstract bases within
[MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) or
[registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) hierarchies which are not
themselves dataclasses is deprecated, as these fields are not supported
by [PEP 681](https://peps.python.org/pep-0681/) as belonging to the dataclass.  A warning is emitted for this
case which will later be an error.

See also

[When transforming <cls> to a dataclass, attribute(s) originate from superclass <cls> which is not a dataclass.](https://docs.sqlalchemy.org/en/20/errors.html#error-dcmx) - background on rationale

### Relationship Configuration

The [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation in combination with
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is used in the same way as described at
[Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns).    When specifying a collection-based
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) as an optional keyword argument, the
[relationship.default_factory](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default_factory) parameter must be passed and it
must refer to the collection class that’s to be used.  Many-to-one and
scalar object references may make use of
[relationship.default](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default) if the default value is to be `None`:

```
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

reg = registry()

@reg.mapped_as_dataclass
class Parent:
    __tablename__ = "parent"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(
        default_factory=list, back_populates="parent"
    )

@reg.mapped_as_dataclass
class Child:
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(default=None)
```

The above mapping will generate an empty list for `Parent.children` when a
new `Parent()` object is constructed without passing `children`, and
similarly a `None` value for `Child.parent` when a new `Child()` object
is constructed without passing `parent`.

While the [relationship.default_factory](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default_factory) can be automatically
derived from the given collection class of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
itself, this would break compatibility with dataclasses, as the presence
of [relationship.default_factory](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default_factory) or
[relationship.default](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.default) is what determines if the parameter is
to be required or optional when rendered into the `__init__()` method.

### Using Non-Mapped Dataclass Fields

When using Declarative dataclasses, non-mapped fields may be used on the
class as well, which will be part of the dataclass construction process but
will not be mapped.   Any field that does not use [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) will
be ignored by the mapping process.   In the example below, the fields
`ctrl_one` and `ctrl_two` will be part of the instance-level state
of the object, but will not be persisted by the ORM:

```
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped_as_dataclass
class Data:
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[str]

    ctrl_one: Optional[str] = None
    ctrl_two: Optional[str] = None
```

Instance of `Data` above can be created as:

```
d1 = Data(status="s1", ctrl_one="ctrl1", ctrl_two="ctrl2")
```

A more real world example might be to make use of the Dataclasses
`InitVar` feature in conjunction with the `__post_init__()` feature to
receive init-only fields that can be used to compose persisted data.
In the example below, the `User`
class is declared using `id`, `name` and `password_hash` as mapped features,
but makes use of init-only `password` and `repeat_password` fields to
represent the user creation process (note: to run this example, replace
the function `your_hash_function_here()` with a third party hash
function, such as [bcrypt](https://pypi.org/project/bcrypt/) or
[argon2-cffi](https://pypi.org/project/argon2-cffi/)):

```
from dataclasses import InitVar
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    password: InitVar[str]
    repeat_password: InitVar[str]

    password_hash: Mapped[str] = mapped_column(init=False, nullable=False)

    def __post_init__(self, password: str, repeat_password: str):
        if password != repeat_password:
            raise ValueError("passwords do not match")

        self.password_hash = your_hash_function_here(password)
```

The above object is created with parameters `password` and
`repeat_password`, which are consumed up front so that the `password_hash`
variable may be generated:

```
>>> u1 = User(name="some_user", password="xyz", repeat_password="xyz")
>>> u1.password_hash
'$6$9ppc... (example hashed string....)'
```

Changed in version 2.0.0rc1: When using [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass)
or [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass), fields that do not include the
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation may be included, which will be treated as part
of the resulting dataclass but not be mapped, without the need to
also indicate the `__allow_unmapped__` class attribute.  Previous 2.0
beta releases would require this attribute to be explicitly present,
even though the purpose of this attribute was only to allow legacy
ORM typed mappings to continue to function.

### Integrating with Alternate Dataclass Providers such as Pydantic

Warning

The dataclass layer of Pydantic is **not fully compatible** with
SQLAlchemy’s class instrumentation without additional internal changes,
and many features such as related collections may not work correctly.

For Pydantic compatibility, please consider the
[SQLModel](https://sqlmodel.tiangolo.com) ORM which is built with
Pydantic on top of SQLAlchemy ORM, which includes special implementation
details which **explicitly resolve** these incompatibilities.

SQLAlchemy’s [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) class
and [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) method call directly into
the Python standard library `dataclasses.dataclass` class decorator, after
the declarative mapping process has been applied to the class.  This
function call may be swapped out for alternateive dataclasses providers,
such as that of Pydantic, using the `dataclass_callable` parameter
accepted by [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) as a class keyword argument
as well as by [registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass):

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import registry

class Base(
    MappedAsDataclass,
    DeclarativeBase,
    dataclass_callable=pydantic.dataclasses.dataclass,
):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

The above `User` class will be applied as a dataclass, using Pydantic’s
`pydantic.dataclasses.dataclasses` callable.     The process is available
both for mapped classes as well as mixins that extend from
[MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) or which have
[registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass) applied directly.

Added in version 2.0.4: Added the `dataclass_callable` class and method
parameters for [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) and
[registry.mapped_as_dataclass()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped_as_dataclass), and adjusted some of the
dataclass internals to accommodate more strict dataclass functions such as
that of Pydantic.

## Applying ORM Mappings to an existing dataclass (legacy dataclass use)

Legacy Feature

The approaches described here are superseded by
the [Declarative Dataclass Mapping](#orm-declarative-native-dataclasses) feature new in the 2.0
series of SQLAlchemy.  This newer version of the feature builds upon
the dataclass support first added in version 1.4, which is described
in this section.

To map an existing dataclass, SQLAlchemy’s “inline” declarative directives
cannot be used directly; ORM directives are assigned using one of three
techniques:

- Using “Declarative with Imperative Table”, the table / column to be mapped
  is defined using a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object assigned to the
  `__table__` attribute of the class; relationships are defined within
  `__mapper_args__` dictionary.  The class is mapped using the
  [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator.   An example is below at
  [Mapping pre-existing dataclasses using Declarative With Imperative Table](#orm-declarative-dataclasses-imperative-table).
- Using full “Declarative”, the Declarative-interpreted directives such as
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) are added to the
  `.metadata` dictionary of the `dataclasses.field()` construct, where
  they are consumed by the declarative process.  The class is again
  mapped using the [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator.  See the example
  below at [Mapping pre-existing dataclasses using Declarative-style fields](#orm-declarative-dataclasses-declarative-table).
- An “Imperative” mapping can be applied to an existing dataclass using
  the [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method to produce the mapping
  in exactly the same way as described at [Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-imperative-mapping).
  This is illustrated below at [Mapping pre-existing dataclasses using Imperative Mapping](#orm-imperative-dataclasses).

The general process by which SQLAlchemy applies mappings to a dataclass
is the same as that of an ordinary class, but also includes that
SQLAlchemy will detect class-level attributes that were part of the
dataclasses declaration process and replace them at runtime with
the usual SQLAlchemy ORM mapped attributes.   The `__init__` method that
would have been generated by dataclasses is left intact, as is the same
for all the other methods that dataclasses generates such as
`__eq__()`, `__repr__()`, etc.

### Mapping pre-existing dataclasses using Declarative With Imperative Table

An example of a mapping using `@dataclass` using
[Declarative with Imperative Table (a.k.a. Hybrid Declarative)](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration) is below. A complete
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object is constructed explicitly and assigned to the
`__table__` attribute. Instance fields are defined using normal dataclass
syntaxes. Additional [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty)
definitions such as [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), are placed in the
[__mapper_args__](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-mapper-options) class-level
dictionary underneath the `properties` key, corresponding to the
[Mapper.properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.properties) parameter:

```
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()

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
        "properties": {
            "addresses": relationship("Address"),
        }
    }

@mapper_registry.mapped
@dataclass
class Address:
    __table__ = Table(
        "address",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, ForeignKey("user.id")),
        Column("email_address", String(50)),
    )
    id: int = field(init=False)
    user_id: int = field(init=False)
    email_address: Optional[str] = None
```

In the above example, the `User.id`, `Address.id`, and `Address.user_id`
attributes are defined as `field(init=False)`. This means that parameters for
these won’t be added to `__init__()` methods, but
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will still be able to set them after getting their values
during flush from autoincrement or other default value generator.   To
allow them to be specified in the constructor explicitly, they would instead
be given a default value of `None`.

For a [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) to be declared separately, it needs to be
specified directly within the [Mapper.properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.properties) dictionary
which itself is specified within the `__mapper_args__` dictionary, so that it
is passed to the constructor for [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper). An alternative to this
approach is in the next example.

Warning

Declaring a dataclass `field()` setting a `default` together with `init=False`
will not work as would be expected with a totally plain dataclass,
since the SQLAlchemy class instrumentation will replace
the default value set on the class by the dataclass creation process.
Use `default_factory` instead. This adaptation is done automatically when
making use of [Declarative Dataclass Mapping](#orm-declarative-native-dataclasses).

### Mapping pre-existing dataclasses using Declarative-style fields

Legacy Feature

This approach to Declarative mapping with
dataclasses should be considered as legacy.  It will remain supported
however is unlikely to offer any advantages against the new
approach detailed at [Declarative Dataclass Mapping](#orm-declarative-native-dataclasses).

Note that **mapped_column() is not supported with this use**;
the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) construct should continue to be used to declare
table metadata within the `metadata` field of `dataclasses.field()`.

The fully declarative approach requires that [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
are declared as class attributes, which when using dataclasses would conflict
with the dataclass-level attributes.  An approach to combine these together
is to make use of the `metadata` attribute on the `dataclass.field`
object, where SQLAlchemy-specific mapping information may be supplied.
Declarative supports extraction of these parameters when the class
specifies the attribute `__sa_dataclass_metadata_key__`.  This also
provides a more succinct method of indicating the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
association:

```
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()

@mapper_registry.mapped
@dataclass
class User:
    __tablename__ = "user"

    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(default=None, metadata={"sa": Column(String(50))})
    fullname: str = field(default=None, metadata={"sa": Column(String(50))})
    nickname: str = field(default=None, metadata={"sa": Column(String(12))})
    addresses: List[Address] = field(
        default_factory=list, metadata={"sa": relationship("Address")}
    )

@mapper_registry.mapped
@dataclass
class Address:
    __tablename__ = "address"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: int = field(init=False, metadata={"sa": Column(ForeignKey("user.id"))})
    email_address: str = field(default=None, metadata={"sa": Column(String(50))})
```

#### Using Declarative Mixins with pre-existing dataclasses

In the section [Composing Mapped Hierarchies with Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html), Declarative Mixin classes
are introduced.  One requirement of declarative mixins is that certain
constructs that can’t be easily duplicated must be given as callables,
using the [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) decorator, such as in the
example at [Mixing in Relationships](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#orm-declarative-mixins-relationships):

```
class RefTargetMixin:
    @declared_attr
    def target_id(cls) -> Mapped[int]:
        return mapped_column("target_id", ForeignKey("target.id"))

    @declared_attr
    def target(cls):
        return relationship("Target")
```

This form is supported within the Dataclasses `field()` object by using
a lambda to indicate the SQLAlchemy construct inside the `field()`.
Using [declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) to surround the lambda is optional.
If we wanted to produce our `User` class above where the ORM fields
came from a mixin that is itself a dataclass, the form would be:

```
@dataclass
class UserMixin:
    __tablename__ = "user"

    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})

    addresses: List[Address] = field(
        default_factory=list, metadata={"sa": lambda: relationship("Address")}
    )

@dataclass
class AddressMixin:
    __tablename__ = "address"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: int = field(
        init=False, metadata={"sa": lambda: Column(ForeignKey("user.id"))}
    )
    email_address: str = field(default=None, metadata={"sa": Column(String(50))})

@mapper_registry.mapped
class User(UserMixin):
    pass

@mapper_registry.mapped
class Address(AddressMixin):
    pass
```

Added in version 1.4.2: Added support for “declared attr” style mixin attributes,
namely [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs as well as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects with foreign key declarations, to be used within “Dataclasses
with Declarative Table” style mappings.

### Mapping pre-existing dataclasses using Imperative Mapping

As described previously, a class which is set up as a dataclass using the
`@dataclass` decorator can then be further decorated using the
[registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator in order to apply declarative-style
mapping to the class. As an alternative to using the
[registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator, we may also pass the class through the
[registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively) method instead, so that we may pass all
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) configuration imperatively to
the function rather than having them defined on the class itself as class
variables:

```
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()

@dataclass
class User:
    id: int = field(init=False)
    name: str = None
    fullname: str = None
    nickname: str = None
    addresses: List[Address] = field(default_factory=list)

@dataclass
class Address:
    id: int = field(init=False)
    user_id: int = field(init=False)
    email_address: str = None

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

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
        "addresses": relationship(Address, backref="user", order_by=address.c.id),
    },
)

mapper_registry.map_imperatively(Address, address)
```

The same warning mentioned in [Mapping pre-existing dataclasses using Declarative With Imperative Table](#orm-declarative-dataclasses-imperative-table)
applies when using this mapping style.

## Applying ORM mappings to an existing attrs class

Warning

The `attrs` library is not part of SQLAlchemy’s continuous
integration testing, and compatibility with this library may change without
notice due to incompatibilities introduced by either side.

The [attrs](https://pypi.org/project/attrs/) library is a popular third party library that provides similar
features as dataclasses, with many additional features provided not
found in ordinary dataclasses.

A class augmented with [attrs](https://pypi.org/project/attrs/) uses the `@define` decorator. This decorator
initiates a process to scan the class for attributes that define the class’
behavior, which are then used to generate methods, documentation, and
annotations.

The SQLAlchemy ORM supports mapping an [attrs](https://pypi.org/project/attrs/) class using **Imperative** mapping.
The general form of this style is equivalent to the
[Mapping pre-existing dataclasses using Imperative Mapping](#orm-imperative-dataclasses) mapping form used with
dataclasses, where the class construction uses `attrs` alone, with ORM mappings
applied after the fact without any class attribute scanning.

The `@define` decorator of [attrs](https://pypi.org/project/attrs/) by default replaces the annotated class
with a new __slots__ based class, which is not supported. When using the old
style annotation `@attr.s` or using `define(slots=False)`, the class
does not get replaced. Furthermore `attrs` removes its own class-bound attributes
after the decorator runs, so that SQLAlchemy’s mapping process takes over these
attributes without any issue. Both decorators, `@attr.s` and `@define(slots=False)`
work with SQLAlchemy.

Changed in version 2.0: SQLAlchemy integration with `attrs` works only
with imperative mapping style, that is, not using Declarative.
The introduction of ORM Annotated Declarative style is not cross-compatible
with `attrs`.

The `attrs` class is built first.  The SQLAlchemy ORM mapping can be
applied after the fact using [registry.map_imperatively()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.map_imperatively):

```
from __future__ import annotations

from typing import List

from attrs import define
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()

@define(slots=False)
class User:
    id: int
    name: str
    fullname: str
    nickname: str
    addresses: List[Address]

@define(slots=False)
class Address:
    id: int
    user_id: int
    email_address: Optional[str]

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

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
        "addresses": relationship(Address, backref="user", order_by=address.c.id),
    },
)

mapper_registry.map_imperatively(Address, address)
```

---

# SQLAlchemy 2.0 Documentation

# Mapper Configuration with Declarative

The section [Mapped Class Essential Components](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapper-configuration-overview) discusses the general
configurational elements of a [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) construct, which is the
structure that defines how a particular user defined class is mapped to a
database table or other SQL construct.    The following sections describe
specific details about how the declarative system goes about constructing
the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

## Defining Mapped Properties with Declarative

The examples given at [Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html)
illustrate mappings against table-bound columns, using the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
construct.  There are several other varieties of ORM mapped constructs
that may be configured besides table-bound columns, the most common being the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct.  Other kinds of properties include
SQL expressions that are defined using the [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property)
construct and multiple-column mappings using the [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
construct.

While an [imperative mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-imperative-mapping) makes use of
the [properties](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-properties) dictionary to establish
all the mapped class attributes, in the declarative
mapping, these properties are all specified inline with the class definition,
which in the case of a declarative table mapping are inline with the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that will be used to generate a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.

Working with the example mapping of `User` and `Address`, we may illustrate
a declarative table mapping that includes not just [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column)
objects but also relationships and SQL expressions:

```
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(firstname + " " + lastname)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]
    address_statistics: Mapped[Optional[str]] = mapped_column(Text, deferred=True)

    user: Mapped["User"] = relationship(back_populates="addresses")
```

The above declarative table mapping features two tables, each with a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) referring to the other, as well as a simple
SQL expression mapped by [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), and an additional
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) that indicates loading should be on a
“deferred” basis as defined
by the [mapped_column.deferred](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.deferred) keyword.    More documentation
on these particular concepts may be found at [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns),
[Using column_property](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#mapper-column-property-sql-expressions), and [Limiting which Columns Load with Column Deferral](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#orm-queryguide-column-deferral).

Properties may be specified with a declarative mapping as above using
“hybrid table” style as well; the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that
are directly part of a table move into the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) definition
but everything else, including composed SQL expressions, would still be
inline with the class definition.  Constructs that need to refer to a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) directly would reference it in terms of the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.  To illustrate the above mapping using
hybrid table style:

```
# mapping attributes using declarative with imperative table
# i.e. __table__

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import column_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import deferred
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __table__ = Table(
        "user",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("firstname", String(50)),
        Column("lastname", String(50)),
    )

    fullname = column_property(__table__.c.firstname + " " + __table__.c.lastname)

    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __table__ = Table(
        "address",
        Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user.id")),
        Column("email_address", String),
        Column("address_statistics", Text),
    )

    address_statistics = deferred(__table__.c.address_statistics)

    user = relationship("User", back_populates="addresses")
```

Things to note above:

- The address [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) contains a column called `address_statistics`,
  however we re-map this column under the same attribute name to be under
  the control of a [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred) construct.
- With both declararative table and hybrid table mappings, when we define a
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) construct, we always name the target table
  using the **table name**, and not the mapped class name.
- When we define [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs, as these constructs
  create a linkage between two mapped classes where one necessarily is defined
  before the other, we can refer to the remote class using its string name.
  This functionality also extends into the area of other arguments specified
  on the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) such as the “primary join” and “order by”
  arguments.   See the section [Late-Evaluation of Relationship Arguments](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#orm-declarative-relationship-eval) for
  details on this.

## Mapper Configuration Options with Declarative

With all mapping forms, the mapping of the class is configured through
parameters that become part of the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) object.
The function which ultimately receives these arguments is the
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) function, and are delivered to it from one of
the front-facing mapping functions defined on the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)
object.

For the declarative form of mapping, mapper arguments are specified
using the `__mapper_args__` declarative class variable, which is a dictionary
that is passed as keyword arguments to the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) function.
Some examples:

**Map Specific Primary Key Columns**

The example below illustrates Declarative-level settings for the
[Mapper.primary_key](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.primary_key) parameter, which establishes
particular columns as part of what the ORM should consider to be a primary
key for the class, independently of schema-level primary key constraints:

```
class GroupUsers(Base):
    __tablename__ = "group_users"

    user_id = mapped_column(String(40))
    group_id = mapped_column(String(40))

    __mapper_args__ = {"primary_key": [user_id, group_id]}
```

See also

[Mapping to an Explicit Set of Primary Key Columns](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapper-primary-key) - further background on ORM mapping of explicit
columns as primary key columns

**Version ID Column**

The example below illustrates Declarative-level settings for the
[Mapper.version_id_col](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_col) and
[Mapper.version_id_generator](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.version_id_generator) parameters, which configure
an ORM-maintained version counter that is updated and checked within the
[unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) flush process:

```
from datetime import datetime

class Widget(Base):
    __tablename__ = "widgets"

    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime, nullable=False)

    __mapper_args__ = {
        "version_id_col": timestamp,
        "version_id_generator": lambda v: datetime.now(),
    }
```

See also

[Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html#mapper-version-counter) - background on the ORM version counter feature

**Single Table Inheritance**

The example below illustrates Declarative-level settings for the
[Mapper.polymorphic_on](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_on) and
[Mapper.polymorphic_identity](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.polymorphic_identity) parameters, which are used when
configuring a single-table inheritance mapping:

```
class Person(Base):
    __tablename__ = "person"

    person_id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False)

    __mapper_args__ = dict(
        polymorphic_on=type,
        polymorphic_identity="person",
    )

class Employee(Person):
    __mapper_args__ = dict(
        polymorphic_identity="employee",
    )
```

See also

[Single Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#single-inheritance) - background on the ORM single table inheritance
mapping feature.

### Constructing mapper arguments dynamically

The `__mapper_args__` dictionary may be generated from a class-bound
descriptor method rather than from a fixed dictionary by making use of the
[declared_attr()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) construct.    This is useful to create arguments
for mappers that are programmatically derived from the table configuration
or other aspects of the mapped class.    A dynamic `__mapper_args__`
attribute will typically be useful when using a Declarative Mixin or
abstract base class.

For example, to omit from the mapping
any columns that have a special [Column.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.info) value, a mixin
can use a `__mapper_args__` method that scans for these columns from the
`cls.__table__` attribute and passes them to the [Mapper.exclude_properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.exclude_properties)
collection:

```
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

class ExcludeColsWFlag:
    @declared_attr
    def __mapper_args__(cls):
        return {
            "exclude_properties": [
                column.key
                for column in cls.__table__.c
                if column.info.get("exclude", False)
            ]
        }

class Base(DeclarativeBase):
    pass

class SomeClass(ExcludeColsWFlag, Base):
    __tablename__ = "some_table"

    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(String)
    not_needed = mapped_column(String, info={"exclude": True})
```

Above, the `ExcludeColsWFlag` mixin provides a per-class `__mapper_args__`
hook that will scan for [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that include the key/value
`'exclude': True` passed to the [Column.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.info) parameter, and then
add their string “key” name to the [Mapper.exclude_properties](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.exclude_properties)
collection which will prevent the resulting [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) from considering
these columns for any SQL operations.

See also

[Composing Mapped Hierarchies with Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html)

## Other Declarative Mapping Directives

### __declare_last__()

The `__declare_last__()` hook allows definition of
a class level function that is automatically called by the
[MapperEvents.after_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_configured) event, which occurs after mappings are
assumed to be completed and the ‘configure’ step has finished:

```
class MyClass(Base):
    @classmethod
    def __declare_last__(cls):
        """ """
        # do something with mappings
```

### __declare_first__()

Like `__declare_last__()`, but is called at the beginning of mapper
configuration via the [MapperEvents.before_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured) event:

```
class MyClass(Base):
    @classmethod
    def __declare_first__(cls):
        """ """
        # do something before mappings are configured
```

### metadata

The [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection normally used to assign a new
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is the `registry.metadata` attribute
associated with the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) object in use. When using a
declarative base class such as that produced by the
[DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) superclass, as well as legacy functions such as
[declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) and [registry.generate_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.generate_base), this
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) is also normally present as an attribute named
`.metadata` that’s directly on the base class, and thus also on the mapped
class via inheritance. Declarative uses this attribute, when present, in order
to determine the target [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection, or if not
present, uses the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) associated directly with the
[registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry).

This attribute may also be assigned towards in order to affect the
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection to be used on a per-mapped-hierarchy basis
for a single base and/or [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry). This takes effect whether a
declarative base class is used or if the [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) decorator
is used directly, thus allowing patterns such as the metadata-per-abstract base
example in the next section, [__abstract__](#declarative-abstract). A similar pattern can
be illustrated using [registry.mapped()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.mapped) as follows:

```
reg = registry()

class BaseOne:
    metadata = MetaData()

class BaseTwo:
    metadata = MetaData()

@reg.mapped
class ClassOne:
    __tablename__ = "t1"  # will use reg.metadata

    id = mapped_column(Integer, primary_key=True)

@reg.mapped
class ClassTwo(BaseOne):
    __tablename__ = "t1"  # will use BaseOne.metadata

    id = mapped_column(Integer, primary_key=True)

@reg.mapped
class ClassThree(BaseTwo):
    __tablename__ = "t1"  # will use BaseTwo.metadata

    id = mapped_column(Integer, primary_key=True)
```

See also

[__abstract__](#declarative-abstract)

### __abstract__

`__abstract__` causes declarative to skip the production
of a table or mapper for the class entirely.  A class can be added within a
hierarchy in the same way as mixin (see [Mixin and Custom Base Classes](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/mixins.html#declarative-mixins)), allowing
subclasses to extend just from the special class:

```
class SomeAbstractBase(Base):
    __abstract__ = True

    def some_helpful_method(self):
        """ """

    @declared_attr
    def __mapper_args__(cls):
        return {"helpful mapper arguments": True}

class MyMappedClass(SomeAbstractBase):
    pass
```

One possible use of `__abstract__` is to use a distinct
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) for different bases:

```
class Base(DeclarativeBase):
    pass

class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData()

class OtherBase(Base):
    __abstract__ = True
    metadata = MetaData()
```

Above, classes which inherit from `DefaultBase` will use one
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) as the registry of tables, and those which inherit from
`OtherBase` will use a different one. The tables themselves can then be
created perhaps within distinct databases:

```
DefaultBase.metadata.create_all(some_engine)
OtherBase.metadata.create_all(some_other_engine)
```

See also

[Building Deeper Hierarchies with polymorphic_abstract](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#orm-inheritance-abstract-poly) - an alternative form of “abstract”
mapped class that is appropriate for inheritance hierarchies.

### __table_cls__

Allows the callable / class used to generate a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to be customized.
This is a very open-ended hook that can allow special customizations
to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that one generates here:

```
class MyMixin:
    @classmethod
    def __table_cls__(cls, name, metadata_obj, *arg, **kw):
        return Table(f"my_{name}", metadata_obj, *arg, **kw)
```

The above mixin would cause all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects generated to include
the prefix `"my_"`, followed by the name normally specified using the
`__tablename__` attribute.

`__table_cls__` also supports the case of returning `None`, which
causes the class to be considered as single-table inheritance vs. its subclass.
This may be useful in some customization schemes to determine that single-table
inheritance should take place based on the arguments for the table itself,
such as, define as single-inheritance if there is no primary key present:

```
class AutoTable:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    @classmethod
    def __table_cls__(cls, *arg, **kw):
        for obj in arg[1:]:
            if (isinstance(obj, Column) and obj.primary_key) or isinstance(
                obj, PrimaryKeyConstraint
            ):
                return Table(*arg, **kw)

        return None

class Person(AutoTable, Base):
    id = mapped_column(Integer, primary_key=True)

class Employee(Person):
    employee_name = mapped_column(String)
```

The above `Employee` class would be mapped as single-table inheritance
against `Person`; the `employee_name` column would be added as a member
of the `Person` table.
