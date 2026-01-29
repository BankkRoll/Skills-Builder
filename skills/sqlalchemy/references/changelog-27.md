# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# What’s New in SQLAlchemy 2.0?

Note for Readers

SQLAlchemy 2.0’s transition documents are separated into **two**
documents - one which details major API shifts from the 1.x to 2.x
series, and the other which details new features and behaviors relative
to SQLAlchemy 1.4:

- [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html) - 1.x to 2.x API shifts
- [What’s New in SQLAlchemy 2.0?](#) - this document, new features and behaviors for SQLAlchemy 2.0

Readers who have not yet updated their 1.4 application to follow
SQLAlchemy 2.0 engine and ORM conventions may navigate to
[SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html) for a guide to ensuring SQLAlchemy 2.0
compatibility, which is a prerequisite for having working code under
version 2.0.

About this Document

This document describes changes between SQLAlchemy version 1.4
and SQLAlchemy version 2.0, **independent** of the major changes between
[1.x style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1.x-style) and [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) usage.   Readers should start
with the [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html) document to get an overall picture
of the major compatibility changes between the 1.x and 2.x series.

Aside from the major 1.x->2.x migration path, the next largest
paradigm shift in SQLAlchemy 2.0 is deep integration with [PEP 484](https://peps.python.org/pep-0484/) typing
practices and current capabilities, particularly within the ORM. New
type-driven ORM declarative styles inspired by Python [dataclasses](https://docs.python.org/3/library/dataclasses.html), as well
as new integrations with dataclasses themselves, complement an overall
approach that no longer requires stubs and also goes very far towards
providing a type-aware method chain from SQL statement to result set.

The prominence of Python typing is significant not only so that type checkers
like [mypy](https://mypy.readthedocs.io/en/stable/) can run without plugins; more significantly it allows IDEs
like [vscode](https://code.visualstudio.com/) and [pycharm](https://www.jetbrains.com/pycharm/) to take a much more active role in assisting
with the composition of a SQLAlchemy application.

## New Typing Support in Core and ORM - Stubs / Extensions no longer used

The approach to typing for Core and ORM has been completely reworked, compared
to the interim approach that was provided in version 1.4 via the
[sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs) package.   The new approach begins at the most fundamental
element in SQLAlchemy which is the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), or more
accurately the [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) that underlies all SQL
expressions that have a type.   This expression-level typing then extends into the area of
statement construction, statement execution, and result sets, and finally into the ORM
where new [declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html) forms allow
for fully typed ORM models that integrate all the way from statement to
result set.

Tip

Typing support should be considered **beta level** software
for the 2.0 series. Typing details are subject to change however
significant backwards-incompatible changes are not planned.

### SQL Expression / Statement / Result Set Typing

This section provides background and examples for SQLAlchemy’s new
SQL expression typing approach, which extends from base [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
constructs through SQL statements and result sets and into realm of ORM mapping.

#### Rationale and Overview

Tip

This section is an architectural discussion. Skip ahead to
[SQL Expression Typing - Examples](#whatsnew-20-expression-typing-examples) to just see what the new typing
looks like.

In [sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs), SQL expressions were typed as [generics](https://peps.python.org/pep-0484/#generics) that then
referred to a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object such as [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer),
[DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime), or [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) as their generic argument
(such as `Column[Integer]`). This was itself a departure from what
the original Dropbox [sqlalchemy-stubs](https://github.com/dropbox/sqlalchemy-stubs) package did, where
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and its foundational constructs were directly generic on
Python types, such as `int`, `datetime` and `str`.   It was hoped
that since [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) / [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) / [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) themselves
are generic against `int` / `datetime` / `str`, there would be ways
to maintain both levels of information and to be able to extract the Python
type from a column expression via the [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) as an intermediary
construct.  However, this is not the case, as [PEP 484](https://peps.python.org/pep-0484/)
doesn’t really have a rich enough feature set for this to be viable,
lacking capabilities such as
[higher kinded TypeVars](https://github.com/python/typing/issues/548).

So after a [deep assessment](https://github.com/python/typing/discussions/999)
of the current capabilities of [PEP 484](https://peps.python.org/pep-0484/), SQLAlchemy 2.0 has realized the
original wisdom of [sqlalchemy-stubs](https://github.com/dropbox/sqlalchemy-stubs) in this area and returned to linking
column expressions directly to Python types.  This does mean that if one
has SQL expressions to different subtypes, like `Column(VARCHAR)` vs.
`Column(Unicode)`, the specifics of those two [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) subtypes
is not carried along as the type only carries along `str`,
but in practice this is usually not an issue and it is generally vastly more
useful that the Python type is immediately present, as it represents the
in-Python data one will be storing and receiving for this column directly.

Concretely, this means that an expression like `Column('id', Integer)`
is typed as `Column[int]`.    This allows for a viable pipeline of
SQLAlchemy construct -> Python datatype to be set up, without the need for
typing plugins.  Crucially, it allows full interoperability with
the ORM’s paradigm of using [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) and [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
constructs that reference ORM mapped class types (e.g. a [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
containing instances of user-mapped instances, such as the `User` and
`Address` examples used in our tutorials).   While Python typing currently has very limited
support for customization of tuple-types (where [PEP 646](https://peps.python.org/pep-0646/), the first pep that
attempts to deal with tuple-like objects, was [intentionally limited
in its functionality](https://mail.python.org/archives/list/typing-sig@python.org/message/G2PNHRR32JMFD3JR7ACA2NDKWTDSEPUG/)
and by itself is not yet viable for arbitrary tuple
manipulation),
a fairly decent approach has been devised that allows for basic
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) -> [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) -> [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) typing
to function, including for ORM classes, where at the point at which a
[Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) object is to be unpacked into individual column entries,
a small typing-oriented accessor is added that allows the individual Python
values to maintain the Python type linked to the SQL expression from which
they originated (translation: it works).

#### SQL Expression Typing - Examples

A brief tour of typing behaviors.  Comments
indicate what one would see hovering over the code in [vscode](https://code.visualstudio.com/) (or roughly
what typing tools would display when using the [reveal_type()](https://mypy.readthedocs.io/en/latest/common_issues.html?highlight=reveal_type#reveal-type)
helper):

- Simple Python Types Assigned to SQL Expressions
  ```
  # (variable) str_col: ColumnClause[str]
  str_col = column("a", String)
  # (variable) int_col: ColumnClause[int]
  int_col = column("a", Integer)
  # (variable) expr1: ColumnElement[str]
  expr1 = str_col + "x"
  # (variable) expr2: ColumnElement[int]
  expr2 = int_col + 10
  # (variable) expr3: ColumnElement[bool]
  expr3 = int_col == 15
  ```
- Individual SQL expressions assigned to [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) constructs, as well as any
  row-returning construct, including row-returning DML
  such as [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) with [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning), are packed
  into a `Tuple[]` type which retains the Python type for each element.
  ```
  # (variable) stmt: Select[Tuple[str, int]]
  stmt = select(str_col, int_col)
  # (variable) stmt: ReturningInsert[Tuple[str, int]]
  ins_stmt = insert(table("t")).returning(str_col, int_col)
  ```
- The `Tuple[]` type from any row returning construct, when invoked with an
  `.execute()` method, carries through to [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
  and [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row).  In order to unpack the [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row)
  object as a tuple, the [Row.tuple()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row.tuple) or [Row.t](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row.t)
  accessor essentially casts the [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) into the corresponding
  `Tuple[]` (though remains the same [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) object at runtime).
  ```
  with engine.connect() as conn:
      # (variable) stmt: Select[Tuple[str, int]]
      stmt = select(str_col, int_col)
      # (variable) result: Result[Tuple[str, int]]
      result = conn.execute(stmt)
      # (variable) row: Row[Tuple[str, int]] | None
      row = result.first()
      if row is not None:
          # for typed tuple unpacking or indexed access,
          # use row.tuple() or row.t  (this is the small typing-oriented accessor)
          strval, intval = row.t
          # (variable) strval: str
          strval
          # (variable) intval: int
          intval
  ```
- Scalar values for single-column statements do the right thing with
  methods like [Connection.scalar()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.scalar), [Result.scalars()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result.scalars),
  etc.
  ```
  # (variable) data: Sequence[str]
  data = connection.execute(select(str_col)).scalars().all()
  ```
- The above support for row-returning constructs works the best with
  ORM mapped classes, as a mapped class can list out specific types
  for its members.  The example below sets up a class using
  [new type-aware syntaxes](#whatsnew-20-orm-declarative-typing),
  described in the following section:
  ```
  from sqlalchemy.orm import DeclarativeBase
  from sqlalchemy.orm import Mapped
  from sqlalchemy.orm import mapped_column
  class Base(DeclarativeBase):
      pass
  class User(Base):
      __tablename__ = "user_account"
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str]
      addresses: Mapped[List["Address"]] = relationship()
  class Address(Base):
      __tablename__ = "address"
      id: Mapped[int] = mapped_column(primary_key=True)
      email_address: Mapped[str]
      user_id = mapped_column(ForeignKey("user_account.id"))
  ```
  With the above mapping, the attributes are typed and express themselves
  all the way from statement to result set:
  ```
  with Session(engine) as session:
      # (variable) stmt: Select[Tuple[int, str]]
      stmt_1 = select(User.id, User.name)
      # (variable) result_1: Result[Tuple[int, str]]
      result_1 = session.execute(stmt_1)
      # (variable) intval: int
      # (variable) strval: str
      intval, strval = result_1.one().t
  ```
  Mapped classes themselves are also types, and behave the same way, such
  as a SELECT against two mapped classes:
  ```
  with Session(engine) as session:
      # (variable) stmt: Select[Tuple[User, Address]]
      stmt_2 = select(User, Address).join_from(User, Address)
      # (variable) result_2: Result[Tuple[User, Address]]
      result_2 = session.execute(stmt_2)
      # (variable) user_obj: User
      # (variable) address_obj: Address
      user_obj, address_obj = result_2.one().t
  ```
  When selecting mapped classes, constructs like [aliased](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) work
  as well, maintaining the column-level attributes of the original mapped
  class as well as the return type expected from a statement:
  ```
  with Session(engine) as session:
      # this is in fact an Annotated type, but typing tools don't
      # generally display this
      # (variable) u1: Type[User]
      u1 = aliased(User)
      # (variable) stmt: Select[Tuple[User, User, str]]
      stmt = select(User, u1, User.name).filter(User.id == 5)
      # (variable) result: Result[Tuple[User, User, str]]
      result = session.execute(stmt)
  ```
- Core Table does not yet have a decent way to maintain typing of
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects when accessing them via the [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c) accessor.
  Since [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is set up as an instance of a class, and the
  [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c) accessor typically accesses [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
  dynamically by name, there’s not yet an established typing approach for this; some
  alternative syntax would be needed.
- ORM classes, scalars, etc. work great.
  The typical use case of selecting ORM classes, as scalars or tuples,
  all works, both 2.0 and 1.x style queries, getting back the exact type
  either by itself or contained within the appropriate container such
  as `Sequence[]`, `List[]` or `Iterator[]`:
  ```
  # (variable) users1: Sequence[User]
  users1 = session.scalars(select(User)).all()
  # (variable) user: User
  user = session.query(User).one()
  # (variable) user_iter: Iterator[User]
  user_iter = iter(session.scalars(select(User)))
  ```
- Legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) gains tuple typing as well.
  The typing support for [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) goes well beyond what
  [sqlalchemy-stubs](https://github.com/dropbox/sqlalchemy-stubs) or [sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs) offered, where both scalar-object
  as well as tuple-typed [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects will retain result level
  typing for most cases:
  ```
  # (variable) q1: RowReturningQuery[Tuple[int, str]]
  q1 = session.query(User.id, User.name)
  # (variable) rows: List[Row[Tuple[int, str]]]
  rows = q1.all()
  # (variable) q2: Query[User]
  q2 = session.query(User)
  # (variable) users: List[User]
  users = q2.all()
  ```

#### the catch - all stubs must be uninstalled

A key caveat with the typing support is that **all SQLAlchemy stubs packages
must be uninstalled** for typing to work.   When running [mypy](https://mypy.readthedocs.io/en/stable/) against a
Python virtualenv, this is only a matter of uninstalling those packages.
However, a SQLAlchemy stubs package is also currently part of [typeshed](https://github.com/python/typeshed), which
itself is bundled into some typing tools such as [Pylance](https://github.com/microsoft/pylance-release), so it may be
necessary in some cases to locate the files for these packages and delete them,
if they are in fact interfering with the new typing working correctly.

Once SQLAlchemy 2.0 is released in final status, typeshed will remove
SQLAlchemy from its own stubs source.

### ORM Declarative Models

SQLAlchemy 1.4 introduced the first SQLAlchemy-native ORM typing support
using a combination of [sqlalchemy2-stubs](https://github.com/sqlalchemy/sqlalchemy2-stubs) and the [Mypy Plugin](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html).
In SQLAlchemy 2.0, the Mypy plugin **remains available, and has been updated
to work with SQLAlchemy 2.0’s typing system**.  However, it should now be
considered **deprecated**, as applications now have a straightforward path to adopting the
new typing support that does not use plugins or stubs.

#### Overview

The fundamental approach for the new system is that mapped column declarations,
when using a fully [Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table) model (that is,
not [hybrid declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration) or
[imperative](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-imperative-mapping) configurations, which are unchanged),
are first derived at runtime by inspecting the type annotation on the left side
of each attribute declaration, if present.  Left hand type annotations are
expected to be contained within the
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) generic type, otherwise the attribute is not considered
to be a mapped attribute.  The attribute declaration may then refer to
the [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct on the right hand side, which is used
to provide additional Core-level schema information about the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to be produced and mapped. This right hand side
declaration is optional if a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation is present on the
left side; if no annotation is present on the left side, then the
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) may be used as an exact replacement for the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) directive where it will provide for more accurate (but
not exact) typing behavior of the attribute, even though no annotation is
present.

The approach is inspired by the approach of Python [dataclasses](https://docs.python.org/3/library/dataclasses.html) which starts
with an annotation on the left, then allows for an optional
`dataclasses.field()` specification on the right; the key difference from the
dataclasses approach is that SQLAlchemy’s approach is strictly **opt-in**,
where existing mappings that use [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) without any type
annotations continue to work as they always have, and the
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct may be used as a direct replacement for
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) without any explicit type annotations. Only for exact
attribute-level Python types to be present is the use of explicit annotations
with [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) required. These annotations may be used on an
as-needed, per-attribute basis for those attributes where specific types are
helpful; non-annotated attributes that use [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) will be
typed as `Any` at the instance level.

#### Migrating an Existing Mapping

Transitioning to the new ORM approach begins as more verbose, but becomes more
succinct than was previously possible as the available new features are used
fully. The following steps detail a typical transition and then continue
on to illustrate some more options.

##### Step one -declarative_base()is superseded byDeclarativeBase.

One observed limitation in Python typing is that there seems to be
no ability to have a class dynamically generated from a function which then
is understood by typing tools as a base for new classes.  To solve this problem
without plugins, the usual call to [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) can be replaced
with using the [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class, which produces the same
`Base` object as usual, except that typing tools understand it:

```
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

##### Step two - replace Declarative use ofColumnwithmapped_column()

The [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) is an ORM-typing aware construct that can
be swapped directly for the use of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).  Given a
1.x style mapping as:

```
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
```

We replace [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) with [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column); no
arguments need to change:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False)
    fullname = mapped_column(String)
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    email_address = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")
```

The individual columns above are **not yet typed with Python types**,
and are instead typed as `Mapped[Any]`; this is because we can declare any
column either with `Optional` or not, and there’s no way to have a
“guess” in place that won’t cause typing errors when we type it
explicitly.

However, at this step, our above mapping has appropriate [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor) types
set up for all attributes and may be used in queries as well as for
instance-level manipulation, all of which will **pass mypy –strict mode** with no
plugins.

##### Step three - apply exact Python types as needed usingMapped.

This can be done for all attributes for which exact typing is desired;
attributes that are fine being left as `Any` may be skipped.   For
context we also illustrate [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) being used for a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) where we apply an exact type.
The mapping within this interim step
will be more verbose, however with proficiency, this step can
be combined with subsequent steps to update mappings more directly:

```
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String)
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="addresses")
```

At this point, our ORM mapping is fully typed and will produce exact-typed
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) and [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)
constructs.   We now can proceed to pare down redundancy in the mapping
declaration.

##### Step four - removemapped_column()directives where no longer needed

All `nullable` parameters can be implied using `Optional[]`; in
the absence of `Optional[]`, `nullable` defaults to `False`. All SQL
types without arguments such as `Integer` and `String` can be expressed
as a Python annotation alone. A [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) directive with no
parameters can be removed entirely. [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) now derives its
class from the left hand annotation, supporting forward references as well
(as [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) has supported string-based forward references
for ten years already ;) ):

```
from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
```

##### Step five - make use of pep-593Annotatedto package common directives into types

This is a radical new
capability that presents an alternative, or complementary approach, to
[declarative mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html) as a means to provide type
oriented configuration, and also replaces the need for
[declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr) decorated functions in most cases.

First, the Declarative mapping allows the mapping of Python type to
SQL type, such as `str` to [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String), to be customized
using [registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map).   Using [PEP 593](https://peps.python.org/pep-0593/) `Annotated` allows us to create variants of a particular Python type so that
the same type, such as `str`, may be used which each provide variants
of [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String), as below where use of an `Annotated` `str` called
`str50` will indicate `String(50)`:

```
from typing_extensions import Annotated
from sqlalchemy.orm import DeclarativeBase

str50 = Annotated[str, 50]

# declarative base with a type-level override, using a type that is
# expected to be used in multiple places
class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
    }
```

Second, Declarative will extract full
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) definitions from the left hand type if
`Annotated[]` is used, by passing a [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct
as any argument to the `Annotated[]` construct (credit to [@adriangb01](https://twitter.com/adriangb01/status/1532841383647657988)
for illustrating this idea).   This capability may be extended in future releases
to also include [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), [composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite) and other
constructs, but currently is limited to [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column).  The
example below adds additional `Annotated` types in addition to our
`str50` example to illustrate this feature:

```
from typing_extensions import Annotated
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# declarative base from previous example
str50 = Annotated[str, 50]

class Base(DeclarativeBase):
    type_annotation_map = {
        str50: String(50),
    }

# set up mapped_column() overrides, using whole column styles that are
# expected to be used in multiple places
intpk = Annotated[int, mapped_column(primary_key=True)]
user_fk = Annotated[int, mapped_column(ForeignKey("user_account.id"))]

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[intpk]
    name: Mapped[str50]
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id: Mapped[intpk]
    email_address: Mapped[str50]
    user_id: Mapped[user_fk]
    user: Mapped["User"] = relationship(back_populates="addresses")
```

Above, columns that are mapped with `Mapped[str50]`, `Mapped[intpk]`,
or `Mapped[user_fk]` draw from both the
[registry.type_annotation_map](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.params.type_annotation_map) as well as the
`Annotated` construct directly in order to reuse pre-established typing
and column configurations.

##### Optional step - turn mapped classes intodataclasses

We can turn mapped classes into [dataclasses](https://docs.python.org/3/library/dataclasses.html), where a key advantage
is that we can build a strictly-typed `__init__()` method with explicit
positional, keyword only, and default arguments, not to mention we get methods
such as `__str__()` and `__repr__()` for free. The next section
[Native Support for Dataclasses Mapped as ORM Models](#whatsnew-20-dataclasses) illustrates further transformation of the above
model.

##### Typing is supported from step 3 onwards

With the above examples, any example from “step 3” on forward will include
that the attributes
of the model are typed
and will populate through to [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select), [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query),
and [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects:

```
# (variable) stmt: Select[Tuple[int, str]]
stmt = select(User.id, User.name)

with Session(e) as sess:
    for row in sess.execute(stmt):
        # (variable) row: Row[Tuple[int, str]]
        print(row)

    # (variable) users: Sequence[User]
    users = sess.scalars(select(User)).all()

    # (variable) users_legacy: List[User]
    users_legacy = sess.query(User).all()
```

See also

[Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table) - Updated Declarative documentation for
Declarative generation and mapping of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) columns.

### Using Legacy Mypy-Typed Models

SQLAlchemy applications that use the [Mypy plugin](https://docs.sqlalchemy.org/en/20/orm/extensions/mypy.html) with
explicit annotations that don’t use [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) in their annotations
are subject to errors under the new system, as such annotations are flagged as
errors when using constructs such as [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

The section [Migration to 2.0 Step Six - Add __allow_unmapped__ to explicitly typed ORM models](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-step-six) illustrates how to temporarily
disable these errors from being raised for a legacy ORM model that uses
explicit annotations.

See also

[Migration to 2.0 Step Six - Add __allow_unmapped__ to explicitly typed ORM models](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-step-six)

### Native Support for Dataclasses Mapped as ORM Models

The new ORM Declarative features introduced above at
[ORM Declarative Models](#whatsnew-20-orm-declarative-typing) introduced the
new [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct and illustrated type-centric
mapping with optional use of [PEP 593](https://peps.python.org/pep-0593/) `Annotated`.  We can take
the mapping one step further by integrating this with Python
[dataclasses](https://docs.python.org/3/library/dataclasses.html).   This new feature is made possible via [PEP 681](https://peps.python.org/pep-0681/) which
allows for type checkers to recognize classes that are dataclass compatible,
or are fully dataclasses, but were declared through alternate APIs.

Using the dataclasses feature, mapped classes gain an `__init__()` method
that supports positional arguments as well as customizable default values
for optional keyword arguments.  As mentioned previously, dataclasses also
generate many useful methods such as `__str__()`, `__eq__()`.  Dataclass
serialization methods such as
[dataclasses.asdict()](https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict) and
[dataclasses.astuple()](https://docs.python.org/3/library/dataclasses.html#dataclasses.astuple)
also work, but don’t currently accommodate for self-referential structures, which
makes them less viable for mappings that have bidirectional relationships.

SQLAlchemy’s current integration approach converts the user-defined class
into a **real dataclass** to provide runtime functionality; the feature
makes use of the existing dataclass feature introduced in SQLAlchemy 1.4 at
[Python Dataclasses, attrs Supported w/ Declarative, Imperative Mappings](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5027) to produce an equivalent runtime mapping with a fully integrated
configuration style, which is also more correctly typed than was possible
with the previous approach.

To support dataclasses in compliance with [PEP 681](https://peps.python.org/pep-0681/), ORM constructs like
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) and [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) accept additional
[PEP 681](https://peps.python.org/pep-0681/) arguments `init`, `default`, and `default_factory` which
are passed along to the dataclass creation process.  These
arguments currently must be present in an explicit directive on the right side,
just as they would be used with `dataclasses.field()`; they currently
can’t be local to an `Annotated` construct on the left side.   To support
the convenient use of `Annotated` while still supporting dataclass
configuration, [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) can merge
a minimal set of right-hand arguments with that of an existing
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct located on the left side within an `Annotated`
construct, so that most of the succinctness is maintained, as will be seen
below.

To enable dataclasses using class inheritance we make
use of the [MappedAsDataclass](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.MappedAsDataclass) mixin, either directly on each class, or
on the `Base` class, as illustrated below where we further modify the
example mapping from “Step 5” of [ORM Declarative Models](#whatsnew-20-orm-declarative-typing):

```
from typing_extensions import Annotated
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""

intpk = Annotated[int, mapped_column(primary_key=True)]
str30 = Annotated[str, mapped_column(String(30))]
user_fk = Annotated[int, mapped_column(ForeignKey("user_account.id"))]

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str30]
    fullname: Mapped[Optional[str]] = mapped_column(default=None)
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", default_factory=list
    )

class Address(Base):
    __tablename__ = "address"

    id: Mapped[intpk] = mapped_column(init=False)
    email_address: Mapped[str]
    user_id: Mapped[user_fk] = mapped_column(init=False)
    user: Mapped["User"] = relationship(back_populates="addresses", default=None)
```

The above mapping has used the `@dataclasses.dataclass` decorator directly
on each mapped class at the same time that the declarative mapping was
set up, internally setting up each `dataclasses.field()` directive as
indicated.   `User` / `Address` structures can be created using
positional arguments as configured:

```
>>> u1 = User("username", fullname="full name", addresses=[Address("email@address")])
>>> u1
User(id=None, name='username', fullname='full name', addresses=[Address(id=None, email_address='email@address', user_id=None, user=...)])
```

See also

[Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses)

## Optimized ORM bulk insert now implemented for all backends other than MySQL

The dramatic performance improvement introduced in the 1.4 series and described
at [ORM Batch inserts with psycopg2 now batch statements with RETURNING in most cases](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5263) has now been generalized to all included backends that
support RETURNING, which is all backends other than MySQL: SQLite, MariaDB,
PostgreSQL (all drivers), and Oracle; SQL Server has support but is
temporarily disabled in version 2.0.9 [[1]](#id2). While the original feature
was most critical for the psycopg2 driver which otherwise had major performance
issues when using `cursor.executemany()`, the change is also critical for
other PostgreSQL drivers such as asyncpg, as when using RETURNING,
single-statement INSERT statements are still unacceptably slow, as well
as when using SQL Server that also seems to have very slow executemany
speed for INSERT statements regardless of whether or not RETURNING is used.

The performance of the new feature provides an almost across-the-board
order of magnitude performance increase for basically every driver when
INSERTing ORM objects that don’t have a pre-assigned primary key value, as
indicated in the table below, in most cases specific to the use of RETURNING
which is not normally supported with executemany().

The psycopg2 “fast execution helper” approach consists of transforming an
INSERT..RETURNING statement with a single parameter set into a single
statement that INSERTs many parameter sets, using multiple “VALUES…”
clauses so that it can accommodate many parameter sets at once.
Parameter sets are then typically batched into groups of 1000
or similar, so that no single INSERT statement is excessively large, and the
INSERT statement is then invoked for each batch of parameters, rather than
for each individual parameter set.  Primary key values and server defaults
are returned by RETURNING, which continues to work as each statement execution
is invoked using `cursor.execute()`, rather than `cursor.executemany()`.

This allows many rows to be inserted in one statement while also being able to
return newly-generated primary key values as well as SQL and server defaults.
SQLAlchemy historically has always needed to invoke one statement per parameter
set, as it relied upon Python DBAPI Features such as `cursor.lastrowid` which
do not support multiple rows.

With most databases now offering RETURNING (with the conspicuous exception of
MySQL, given that MariaDB supports it), the new change generalizes the psycopg2
“fast execution helper” approach to all dialects that support RETURNING, which
now includes SQlite and MariaDB, and for which no other approach for
“executemany plus RETURNING” is possible, which includes SQLite, MariaDB, and all
PG drivers. The cx_Oracle and oracledb drivers used for Oracle
support RETURNING with executemany natively, and this has also been implemented
to provide equivalent performance improvements.  With SQLite and MariaDB now
offering RETURNING support, ORM use of `cursor.lastrowid` is nearly a thing
of the past, with only MySQL still relying upon it.

For INSERT statements that don’t use RETURNING, traditional executemany()
behavior is used for most backends, with the current exception of psycopg2,
which has very slow executemany() performance overall
and are still improved by the “insertmanyvalues” approach.

### Benchmarks

SQLAlchemy includes a [Performance Suite](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-performance) within
the `examples/` directory, where we can make use of the `bulk_insert`
suite to benchmark INSERTs of many rows using both Core and ORM in different
ways.

For the tests below, we are inserting **100,000 objects**, and in all cases we
actually have 100,000 real Python ORM objects in memory, either created up
front or generated on the fly. All databases other than SQLite are run over a
local network connection, not localhost; this causes the “slower” results to be
extremely slow.

Operations that are improved by this feature include:

- unit of work flushes for objects added to the session using
  [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) and [Session.add_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add_all).
- The new [ORM Bulk Insert Statement](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) feature,
  which improves upon the experimental version of this feature first introduced
  in SQLAlchemy 1.4.
- the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) “bulk” operations described at
  [Bulk Operations](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#bulk-operations), which are superseded by the above mentioned
  ORM Bulk Insert feature.

To get a sense of the scale of the operation, below are performance
measurements using the `test_flush_no_pk` performance suite, which
historically represents SQLAlchemy’s worst-case INSERT performance task,
where objects that don’t have primary key values need to be INSERTed, and
then the newly generated primary key values must be fetched so that the
objects can be used for subsequent flush operations, such as establishment
within relationships, flushing joined-inheritance models, etc:

```
@Profiler.profile
def test_flush_no_pk(n):
    """INSERT statements via the ORM (batched with RETURNING if available),
    fetching generated row id"""
    session = Session(bind=engine)
    for chunk in range(0, n, 1000):
        session.add_all(
            [
                Customer(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                )
                for i in range(chunk, chunk + 1000)
            ]
        )
        session.flush()
    session.commit()
```

This test can be run from any SQLAlchemy source tree as follows:

```
python -m examples.performance.bulk_inserts --test test_flush_no_pk
```

The table below summarizes performance measurements with
the latest 1.4 series of SQLAlchemy compared to 2.0, both running
the same test:

| Driver | SQLA 1.4 Time (secs) | SQLA 2.0 Time (secs) |
| --- | --- | --- |
| sqlite+pysqlite2 (memory) | 6.204843 | 3.554856 |
| postgresql+asyncpg (network) | 88.292285 | 4.561492 |
| postgresql+psycopg (network) | N/A (psycopg3) | 4.861368 |
| mssql+pyodbc (network) | 158.396667 | 4.825139 |
| oracle+cx_Oracle (network) | 92.603953 | 4.809520 |
| mariadb+mysqldb (network) | 71.705197 | 4.075377 |

Note

   [[1](#id1)]

The feature is was temporarily disabled for SQL Server in
SQLAlchemy 2.0.9 due to issues with row ordering when RETURNING is used.
In SQLAlchemy 2.0.10, the feature is re-enabled, with special
case handling for the unit of work’s requirement for RETURNING to be
ordered.

Two additional drivers have no change in performance; the psycopg2 drivers,
for which fast executemany was already implemented in SQLAlchemy 1.4,
and MySQL, which continues to not offer RETURNING support:

| Driver | SQLA 1.4 Time (secs) | SQLA 2.0 Time (secs) |
| --- | --- | --- |
| postgresql+psycopg2 (network) | 4.704876 | 4.699883 |
| mysql+mysqldb (network) | 77.281997 | 76.132995 |

### Summary of Changes

The following bullets list the individual changes made within 2.0 in order to
get all drivers to this state:

- RETURNING implemented for SQLite - [#6195](https://www.sqlalchemy.org/trac/ticket/6195)
- RETURNING implemented for MariaDB - [#7011](https://www.sqlalchemy.org/trac/ticket/7011)
- Fix multi-row RETURNING for Oracle - [#6245](https://www.sqlalchemy.org/trac/ticket/6245)
- make insert() executemany() support RETURNING for as many dialects as
  possible, usually with VALUES() - [#6047](https://www.sqlalchemy.org/trac/ticket/6047)
- Emit a warning when RETURNING w/ executemany is used for non-supporting
  backend (currently no RETURNING backend has this limitation) - [#7907](https://www.sqlalchemy.org/trac/ticket/7907)
- The ORM [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) parameter now defaults to a
  a new setting `"auto"`, which will enable “eager defaults” automatically
  for INSERT statements, when the backend in use supports RETURNING with
  “insertmanyvalues”.  See [Fetching Server-Generated Defaults](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#orm-server-defaults) for documentation.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) - Documentation and background on the
new feature as well as how to configure it

## ORM-enabled Insert, Upsert, Update and Delete Statements, with ORM RETURNING

SQLAlchemy 1.4 ported the features of the legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object to
[2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) execution, which meant that the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct
could be passed to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) to deliver ORM results. Support
was also added for [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) to be passed to
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), to the degree that they could provide
implementations of [Query.update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.update) and [Query.delete()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.delete).

The major missing element has been support for the [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct.
The 1.4 documentation addressed this with some recipes for “inserts” and “upserts”
with use of [Select.from_statement()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.from_statement) to integrate RETURNING
into an ORM context.  2.0 now fully closes the gap by integrating direct support for
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) as an enhanced version of the [Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings)
method, along with full ORM RETURNING support for all DML structures.

### Bulk Insert with RETURNING

[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) can be passed to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute), with
or without [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning), which when passed with a
separate parameter list will invoke the same process as was previously
implemented by
[Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings), with additional enhancements.  This will optimize the
batching of rows making use of the new [fast insertmany](#change-6047)
feature, while also adding support for
heterogeneous parameter sets and multiple-table mappings like joined table
inheritance:

```
>>> users = session.scalars(
...     insert(User).returning(User),
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ],
... )
>>> print(users.all())
[User(name='spongebob', fullname='Spongebob Squarepants'),
 User(name='sandy', fullname='Sandy Cheeks'),
 User(name='patrick', fullname='Patrick Star'),
 User(name='squidward', fullname='Squidward Tentacles'),
 User(name='ehkrabs', fullname='Eugene H. Krabs')]
```

RETURNING is supported for all of these use cases, where the ORM will construct
a full result set from multiple statement invocations.

See also

[ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert)

### Bulk UPDATE

In a similar manner as that of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert), passing the
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) construct along with a parameter list that includes
primary key values to [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) will invoke the same process
as previously supported by the [Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings)
method.  This feature does not however support RETURNING, as it uses
a SQL UPDATE statement that is invoked using DBAPI [executemany](https://docs.sqlalchemy.org/en/20/glossary.html#term-executemany):

```
>>> from sqlalchemy import update
>>> session.execute(
...     update(User),
...     [
...         {"id": 1, "fullname": "Spongebob Squarepants"},
...         {"id": 3, "fullname": "Patrick Star"},
...     ],
... )
```

See also

[ORM Bulk UPDATE by Primary Key](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update)

### INSERT / upsert … VALUES … RETURNING

When using [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) with [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values), the set of
parameters may include SQL expressions. Additionally, upsert variants
such as those for SQLite, PostgreSQL and MariaDB are also supported.
These statements may now include [Insert.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning) clauses
with column expressions or full ORM entities:

```
>>> from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
>>> stmt = sqlite_upsert(User).values(
...     [
...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
...         {"name": "sandy", "fullname": "Sandy Cheeks"},
...         {"name": "patrick", "fullname": "Patrick Star"},
...         {"name": "squidward", "fullname": "Squidward Tentacles"},
...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
...     ]
... )
>>> stmt = stmt.on_conflict_do_update(
...     index_elements=[User.name], set_=dict(fullname=stmt.excluded.fullname)
... )
>>> result = session.scalars(stmt.returning(User))
>>> print(result.all())
[User(name='spongebob', fullname='Spongebob Squarepants'),
User(name='sandy', fullname='Sandy Cheeks'),
User(name='patrick', fullname='Patrick Star'),
User(name='squidward', fullname='Squidward Tentacles'),
User(name='ehkrabs', fullname='Eugene H. Krabs')]
```

See also

[ORM Bulk Insert with Per Row SQL Expressions](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-insert-values)

[ORM “upsert” Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert)

### ORM UPDATE / DELETE with WHERE … RETURNING

SQLAlchemy 1.4 also had some modest support for the RETURNING feature to be
used with the [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) and [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) constructs, when
used with [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).  This support has now been upgraded
to be fully native, including that the `fetch` synchronization strategy
may also proceed whether or not explicit use of RETURNING is present:

```
>>> from sqlalchemy import update
>>> stmt = (
...     update(User)
...     .where(User.name == "squidward")
...     .values(name="spongebob")
...     .returning(User)
... )
>>> result = session.scalars(stmt, execution_options={"synchronize_session": "fetch"})
>>> print(result.all())
```

See also

[ORM UPDATE and DELETE with Custom WHERE Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-where)

[Using RETURNING with UPDATE/DELETE and Custom WHERE Criteria](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-where-returning)

### Improvedsynchronize_sessionbehavior for ORM UPDATE / DELETE

The default strategy for [synchronize_session](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-sync)
is now a new value `"auto"`.  This strategy will attempt to use the
`"evaluate"` strategy and then automatically fall back to the `"fetch"`
strategy.   For all backends other than MySQL / MariaDB, `"fetch"` uses
RETURNING to fetch UPDATE/DELETEd primary key identifiers within the
same statement, so is generally more efficient than previous versions
(in 1.4, RETURNING was only available for PostgreSQL, SQL Server).

See also

[Selecting a Synchronization Strategy](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-update-delete-sync)

### Summary of Changes

Listed tickets for new ORM DML with RETURNING features:

- convert `insert()` at ORM level to interpret `values()` in an ORM
  context - [#7864](https://www.sqlalchemy.org/trac/ticket/7864)
- evaluate feasibility of dml.returning(Entity) to deliver ORM expressions,
  automatically apply select().from_statement equiv - [#7865](https://www.sqlalchemy.org/trac/ticket/7865)
- given ORM insert, try to carry the bulk methods along, re: inheritance -
  [#8360](https://www.sqlalchemy.org/trac/ticket/8360)

## New “Write Only” relationship strategy supersedes “dynamic”

The `lazy="dynamic"` loader strategy becomes legacy, in that it is hardcoded
to make use of legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query). This loader strategy is both not
compatible with asyncio, and additionally has many behaviors that implicitly
iterate its contents, which defeat the original purpose of the “dynamic”
relationship as being for very large collections that should not be implicitly
fully loaded into memory at any time.

The “dynamic” strategy is now superseded by a new strategy
`lazy="write_only"`.  Configuration of “write only” may be achieved using
the [relationship.lazy](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.lazy) parameter of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship),
or when using [type annotated mappings](#whatsnew-20-orm-declarative-typing),
indicating the [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped) annotation as the mapping style:

```
from sqlalchemy.orm import WriteOnlyMapped

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    account_transactions: WriteOnlyMapped["AccountTransaction"] = relationship(
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AccountTransaction.timestamp",
    )

class AccountTransaction(Base):
    __tablename__ = "account_transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="cascade")
    )
    description: Mapped[str]
    amount: Mapped[Decimal]
    timestamp: Mapped[datetime] = mapped_column(default=func.now())
```

The write-only-mapped collection resembles `lazy="dynamic"` in that
the collection may be assigned up front, and also has methods such as
[WriteOnlyCollection.add()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.add) and [WriteOnlyCollection.remove()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.remove)
to modify the collection on an individual item basis:

```
new_account = Account(
    identifier="account_01",
    account_transactions=[
        AccountTransaction(description="initial deposit", amount=Decimal("500.00")),
        AccountTransaction(description="transfer", amount=Decimal("1000.00")),
        AccountTransaction(description="withdrawal", amount=Decimal("-29.50")),
    ],
)

new_account.account_transactions.add(
    AccountTransaction(description="transfer", amount=Decimal("2000.00"))
)
```

The bigger difference is on the database loading side, where the collection
has no ability to load objects from the database directly; instead,
SQL construction methods such as [WriteOnlyCollection.select()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.select) are used to
produce SQL constructs such as [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) which are then executed
using [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) to load the desired objects in an explicit way:

```
account_transactions = session.scalars(
    existing_account.account_transactions.select()
    .where(AccountTransaction.amount < 0)
    .limit(10)
).all()
```

The [WriteOnlyCollection](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection) also integrates with the new
[ORM bulk dml](#change-8360) features, including support for bulk INSERT
and UPDATE/DELETE with WHERE criteria, all including RETURNING support as
well.   See the complete documentation at [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship).

See also

[Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship)

### New pep-484 / type annotated mapping support for Dynamic Relationships

Even though “dynamic” relationships are legacy in 2.0, as these patterns
are expected to have a long lifespan,
[type annotated mapping](#whatsnew-20-orm-declarative-typing) support
is now added for “dynamic” relationships in the same way that its available
for the new `lazy="write_only"` approach, using the [DynamicMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.DynamicMapped)
annotation:

```
from sqlalchemy.orm import DynamicMapped

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    account_transactions: DynamicMapped["AccountTransaction"] = relationship(
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AccountTransaction.timestamp",
    )

class AccountTransaction(Base):
    __tablename__ = "account_transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="cascade")
    )
    description: Mapped[str]
    amount: Mapped[Decimal]
    timestamp: Mapped[datetime] = mapped_column(default=func.now())
```

The above mapping will provide an `Account.account_transactions` collection
that is typed as returning the [AppenderQuery](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.AppenderQuery) collection type,
including its element type, e.g. `AppenderQuery[AccountTransaction]`.  This
then allows iteration and queries to yield objects which are typed
as `AccountTransaction`.

See also

[Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship)

[#7123](https://www.sqlalchemy.org/trac/ticket/7123)

## Installation is now fully pep-517 enabled

The source distribution now includes a `pyproject.toml` file to allow for
complete [PEP 517](https://peps.python.org/pep-0517/) support. In particular this allows a local source build
using `pip` to automatically install the [Cython](https://cython.org/) optional dependency.

[#7311](https://www.sqlalchemy.org/trac/ticket/7311)

## C Extensions now ported to Cython

The SQLAlchemy C extensions have been replaced with all new extensions written
in [Cython](https://cython.org/). While Cython was evaluated back in 2010 when the C extensions were
first created, the nature and focus of the C extensions in use today has
changed quite a bit from that time. At the same time, Cython has apparently
evolved significantly, as has the Python build / distribution toolchain which
made it feasible for us to revisit it.

The move to Cython provides dramatic new advantages with
no apparent downsides:

- The Cython extensions that replace specific C extensions have all benchmarked
  as **faster**, often slightly, but sometimes significantly, than
  virtually all the C code that SQLAlchemy previously
  included. While this seems amazing, it appears to be a product of
  non-obvious optimizations within Cython’s implementation that would not be
  present in a direct Python to C port of a function, as was particularly the
  case for many of the custom collection types added to the C extensions.
- Cython extensions are much easier to write, maintain and debug compared to
  raw C code, and in most cases are line-per-line equivalent to the Python
  code.   It is expected that many more elements of SQLAlchemy will be
  ported to Cython in the coming releases which should open many new doors
  to performance improvements that were previously out of reach.
- Cython is very mature and widely used, including being the basis of some
  of the prominent database drivers supported by SQLAlchemy including
  `asyncpg`, `psycopg3` and `asyncmy`.

Like the previous C extensions, the Cython extensions are pre-built within
SQLAlchemy’s wheel distributions which are automatically available to `pip`
from PyPi.  Manual build instructions are also unchanged with the exception
of the Cython requirement.

See also

[Building the Cython Extensions](https://docs.sqlalchemy.org/en/20/intro.html#c-extensions)

[#7256](https://www.sqlalchemy.org/trac/ticket/7256)

## Major Architectural, Performance and API Enhancements for Database Reflection

The internal system by which [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects and their components are
[reflected](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection) has been completely rearchitected to
allow high performance bulk reflection of thousands of tables at once for
participating dialects. Currently, the **PostgreSQL** and **Oracle** dialects
participate in the new architecture, where the PostgreSQL dialect can now
reflect a large series of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects nearly three times faster,
and the Oracle dialect can now reflect a large series of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects ten times faster.

The rearchitecture applies most directly to dialects that make use of SELECT
queries against system catalog tables to reflect tables, and the remaining
included dialect that can benefit from this approach will be the SQL Server
dialect. The MySQL/MariaDB and SQLite dialects by contrast make use of
non-relational systems to reflect database tables, and were not subject to a
pre-existing performance issue.

The new API is backwards compatible with the previous system, and should
require no changes to third party dialects to retain compatibility; third party
dialects can also opt into the new system by implementing batched queries for
schema reflection.

Along with this change, the API and behavior of the [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector)
object has been improved and enhanced with more consistent cross-dialect
behaviors as well as new methods and new performance features.

### Performance Overview

The source distribution includes a script
`test/perf/many_table_reflection.py` which benches both existing reflection
features as well as new ones. A limited set of its tests may be run on older
versions of SQLAlchemy, where here we use it to illustrate differences in
performance to invoke `metadata.reflect()` to reflect 250 [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects at once over a local network connection:

| Dialect | Operation | SQLA 1.4 Time (secs) | SQLA 2.0 Time (secs) |
| --- | --- | --- | --- |
| postgresql+psycopg2 | metadata.reflect(), 250 tables | 8.2 | 3.3 |
| oracle+cx_oracle | metadata.reflect(), 250 tables | 60.4 | 6.8 |

### Behavioral Changes forInspector()

For SQLAlchemy-included dialects for SQLite, PostgreSQL, MySQL/MariaDB,
Oracle, and SQL Server, the [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table),
[Inspector.has_sequence()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_sequence), [Inspector.has_index()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_index),
[Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names) and
[Inspector.get_sequence_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_sequence_names) now all behave consistently in terms
of caching: they all fully cache their result after being called the first
time for a particular [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) object. Programs that create or
drop tables/sequences while calling upon the same [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector)
object will not receive updated status after the state of the database has
changed. A call to [Inspector.clear_cache()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.clear_cache) or a new
[Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) should be used when DDL changes are to be executed.
Previously, the [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table),
[Inspector.has_sequence()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_sequence) methods did not implement caching nor did
the [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) support caching for these methods, while the
[Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names) and
[Inspector.get_sequence_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_sequence_names) methods were, leading to inconsistent
results between the two types of method.

Behavior for third party dialects is dependent on whether or not they
implement the “reflection cache” decorator for the dialect-level
implementation of these methods.

### New Methods and Improvements forInspector()

- added a method
  [Inspector.has_schema()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_schema) that returns if a schema
  is present in the target database
- added a method [Inspector.has_index()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_index) that returns if a table has
  a particular index.
- Inspection methods such as [Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns) that work
  on a single table at a time should now all consistently
  raise [NoSuchTableError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchTableError) if a
  table or view is not found; this change is specific to individual
  dialects, so may not be the case for existing third-party dialects.
- Separated the handling of “views” and “materialized views”, as in
  real world use cases, these two constructs make use of different DDL
  for CREATE and DROP; this includes that there are now separate
  [Inspector.get_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_view_names) and
  [Inspector.get_materialized_view_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_materialized_view_names) methods.

[#4379](https://www.sqlalchemy.org/trac/ticket/4379)

## Dialect support for psycopg 3 (a.k.a. “psycopg”)

Added dialect support for the [psycopg 3](https://pypi.org/project/psycopg/)
DBAPI, which despite the number “3” now goes by the package name `psycopg`,
superseding the previous `psycopg2` package that for the time being remains
SQLAlchemy’s “default” driver for the `postgresql` dialects. `psycopg` is a
completely reworked and modernized database adapter for PostgreSQL which
supports concepts such as prepared statements as well as Python asyncio.

`psycopg` is the first DBAPI supported by SQLAlchemy which provides
both a pep-249 synchronous API as well as an asyncio driver.  The same
`psycopg` database URL may be used with the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
and [create_async_engine()](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine) engine-creation functions, and the
corresponding sync or asyncio version of the dialect will be selected
automatically.

See also

[psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-psycopg)

## Dialect support for oracledb

Added dialect support for the [oracledb](https://pypi.org/project/oracledb/)
DBAPI, which is the renamed, new major release of the popular cx_Oracle driver.

See also

[python-oracledb](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#oracledb)

## New Conditional DDL for Constraints and Indexes

A new method [Constraint.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint.ddl_if) and [Index.ddl_if()](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.ddl_if)
allows constructs such as [CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint), [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint)
and [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) to be rendered conditionally for a given
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), based on the same kinds of criteria that are accepted
by the `DDLElement.execute_if()` method.  In the example below,
the CHECK constraint and index will only be produced against a PostgreSQL
backend:

```
meta = MetaData()

my_table = Table(
    "my_table",
    meta,
    Column("id", Integer, primary_key=True),
    Column("num", Integer),
    Column("data", String),
    Index("my_pg_index", "data").ddl_if(dialect="postgresql"),
    CheckConstraint("num > 5").ddl_if(dialect="postgresql"),
)

e1 = create_engine("sqlite://", echo=True)
meta.create_all(e1)  # will not generate CHECK and INDEX

e2 = create_engine("postgresql://scott:tiger@localhost/test", echo=True)
meta.create_all(e2)  # will generate CHECK and INDEX
```

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if)

[#7631](https://www.sqlalchemy.org/trac/ticket/7631)

## DATE, TIME, DATETIME datatypes now support literal rendering on all backends

Literal rendering is now implemented for date and time types for backend
specific compilation, including PostgreSQL and Oracle:

```
>>> import datetime

>>> from sqlalchemy import DATETIME
>>> from sqlalchemy import literal
>>> from sqlalchemy.dialects import oracle
>>> from sqlalchemy.dialects import postgresql

>>> date_literal = literal(datetime.datetime.now(), DATETIME)

>>> print(
...     date_literal.compile(
...         dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
...     )
... )
'2022-12-17 11:02:13.575789'
>>> print(
...     date_literal.compile(
...         dialect=oracle.dialect(), compile_kwargs={"literal_binds": True}
...     )
... )
TO_TIMESTAMP('2022-12-17 11:02:13.575789', 'YYYY-MM-DD HH24:MI:SS.FF')
```

Previously, such literal rendering only worked when stringifying statements
without any dialect given; when attempting to render with a dialect-specific
type, a `NotImplementedError` would be raised, up until
SQLAlchemy 1.4.45 where this became a [CompileError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.CompileError) (part of
[#8800](https://www.sqlalchemy.org/trac/ticket/8800)).

The default rendering is modified ISO-8601 rendering (i.e. ISO-8601 with the T
converted to a space) when using `literal_binds` with the SQL compilers
provided by the PostgreSQL, MySQL, MariaDB, MSSQL, Oracle dialects. For Oracle,
the ISO format is wrapped inside of an appropriate TO_DATE() function call.
The rendering for SQLite is unchanged as this dialect always included string
rendering for date values.

[#5052](https://www.sqlalchemy.org/trac/ticket/5052)

## Context Manager Support forResult,AsyncResult

The [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object now supports context manager use, which will
ensure the object and its underlying cursor is closed at the end of the block.
This is useful in particular with server side cursors, where it’s important that
the open cursor object is closed at the end of an operation, even if user-defined
exceptions have occurred:

```
with engine.connect() as conn:
    with conn.execution_options(yield_per=100).execute(
        text("select * from table")
    ) as result:
        for row in result:
            print(f"{row}")
```

With asyncio use, the [AsyncResult](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncResult) and [AsyncConnection](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncConnection) have
been altered to provide for optional async context manager use, as in:

```
async with async_engine.connect() as conn:
    async with conn.execution_options(yield_per=100).execute(
        text("select * from table")
    ) as result:
        for row in result:
            print(f"{row}")
```

[#8710](https://www.sqlalchemy.org/trac/ticket/8710)

## Behavioral Changes

This section covers behavioral changes made in SQLAlchemy 2.0 which are
not otherwise part of the major 1.4->2.0 migration path; changes here are
not expected to have significant effects on backwards compatibility.

### New transaction join modes forSession

The behavior of “joining an external transaction into a Session” has been
revised and improved, allowing explicit control over how the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will accommodate an incoming [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
that already has a transaction and possibly a savepoint already established.
The new parameter [Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode) includes a
series of option values which can accommodate the existing transaction in
several ways, most importantly allowing a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to operate in a
fully transactional style using savepoints exclusively, while leaving the
externally initiated transaction non-committed and active under all
circumstances, allowing test suites to rollback all changes that take place
within tests.

The primary improvement this allows is that the recipe documented at
[Joining a Session into an External Transaction (such as for test suites)](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-external-transaction), which also changed from SQLAlchemy 1.3
to 1.4, is now simplified to no longer require explicit use of an event
handler or any mention of an explicit savepoint; by using
`join_transaction_mode="create_savepoint"`, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will
never affect the state of an incoming transaction, and will instead create a
savepoint (i.e. “nested transaction”) as its root transaction.

The following illustrates part of the example given at
[Joining a Session into an External Transaction (such as for test suites)](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-external-transaction); see that section for a full example:

```
class SomeTest(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection, selecting
        # "create_savepoint" join_transaction_mode
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def tearDown(self):
        self.session.close()

        # rollback non-ORM transaction
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
```

The default mode selected for [Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode)
is `"conditional_savepoint"`, which uses `"create_savepoint"` behavior
if the given [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is itself already on a savepoint.
If the given [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is in a transaction but not a
savepoint, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will propagate “rollback” calls
but not “commit” calls, but will not begin a new savepoint on its own.  This
behavior is chosen by default for its maximum compatibility with
older SQLAlchemy versions as well as that it does not start a new SAVEPOINT
unless the given driver is already making use of SAVEPOINT, as support
for SAVEPOINT varies not only with specific backend and driver but also
configurationally.

The following illustrates a case that worked in SQLAlchemy 1.3, stopped working
in SQLAlchemy 1.4, and is now restored in SQLAlchemy 2.0:

```
engine = create_engine("...")

# setup outer connection with a transaction and a SAVEPOINT
conn = engine.connect()
trans = conn.begin()
nested = conn.begin_nested()

# bind a Session to that connection and operate upon it, including
# a commit
session = Session(conn)
session.connection()
session.commit()
session.close()

# assert both SAVEPOINT and transaction remain active
assert nested.is_active
nested.rollback()
trans.rollback()
```

Where above, a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is joined to a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
that has a savepoint started on it; the state of these two units remains
unchanged after the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has worked with the transaction. In
SQLAlchemy 1.3, the above case worked because the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) would
begin a “subtransaction” upon the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), which would
allow the outer savepoint / transaction to remain unaffected for simple cases
as above. Since subtransactions were deprecated in 1.4 and are now removed in
2.0, this behavior was no longer available. The new default behavior improves
upon the behavior of “subtransactions” by using a real, second SAVEPOINT
instead, so that even calls to [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) prevent the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) from “breaking out” into the externally initiated
SAVEPOINT or transaction.

New code that is joining a transaction-started [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) into
a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) should however select a
[Session.join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode) explicitly, so that the desired
behavior is explicitly defined.

[#9015](https://www.sqlalchemy.org/trac/ticket/9015)

### str(engine.url)will obfuscate the password by default

To avoid leakage of database passwords, calling `str()` on a
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) will now enable the password obfuscation feature by default.
Previously, this obfuscation would be in place for `__repr__()` calls
but not `__str__()`.   This change will impact applications and test suites
that attempt to invoke [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) given the stringified URL
from another engine, such as:

```
>>> e1 = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
>>> e2 = create_engine(str(e1.url))
```

The above engine `e2` will not have the correct password; it will have the
obfuscated string `"***"`.

The preferred approach for the above pattern is to pass the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object directly, there’s no need to stringify:

```
>>> e1 = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
>>> e2 = create_engine(e1.url)
```

Otherwise, for a stringified URL with cleartext password, use the
[URL.render_as_string()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.render_as_string) method, passing the
[URL.render_as_string.hide_password](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.render_as_string.params.hide_password) parameter
as `False`:

```
>>> e1 = create_engine("postgresql+psycopg2://scott:tiger@localhost/test")
>>> url_string = e1.url.render_as_string(hide_password=False)
>>> e2 = create_engine(url_string)
```

[#8567](https://www.sqlalchemy.org/trac/ticket/8567)

### Stricter rules for replacement of Columns in Table objects with same-names, keys

Stricter rules are in place for appending of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects to
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, both moving some previous deprecation warnings to
exceptions, and preventing some previous scenarios that would cause
duplicate columns to appear in tables, when
[Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing) were set to `True`, for both
programmatic [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construction as well as during reflection
operations.

- Under no circumstances should a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object ever have two or more
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects with the same name, regardless of what .key they
  have.  An edge case where this was still possible was identified and fixed.
- Adding a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that has the same name or
  key as an existing [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) will always raise
  [DuplicateColumnError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.DuplicateColumnError) (a new subclass of [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) in
  2.0.0b4) unless additional parameters are present;
  [Table.append_column.replace_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_column.params.replace_existing) for
  [Table.append_column()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_column), and [Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing) for
  construction of a same-named [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) as an existing one, with or
  without reflection being used. Previously, there was a deprecation warning in
  place for this scenario.
- A warning is now emitted if a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is created, that does
  include [Table.extend_existing](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.extend_existing), where an incoming
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that has no separate [Column.key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.key) would fully
  replace an existing [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) that does have a key, which suggests
  the operation is not what the user intended.  This can happen particularly
  during a secondary reflection step, such as `metadata.reflect(extend_existing=True)`.
  The warning suggests that the [Table.autoload_replace](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_replace) parameter
  be set to `False` to prevent this. Previously, in 1.4 and earlier, the
  incoming column would be added **in addition** to the existing column.
  This was a bug and is a behavioral change in 2.0 (as of 2.0.0b4), as the
  previous key will **no longer be present** in the column collection
  when this occurs.

[#8925](https://www.sqlalchemy.org/trac/ticket/8925)

### ORM Declarative Applies Column Orders Differently; Control behavior usingsort_order

Declarative has changed the system by which mapped columns that originate from
mixin or abstract base classes are sorted along with the columns that are on the
declared class itself to place columns from the declared class first, followed
by mixin columns.  The following mapping:

```
class Foo:
    col1 = mapped_column(Integer)
    col3 = mapped_column(Integer)

class Bar:
    col2 = mapped_column(Integer)
    col4 = mapped_column(Integer)

class Model(Base, Foo, Bar):
    id = mapped_column(Integer, primary_key=True)
    __tablename__ = "model"
```

Produces a CREATE TABLE as follows on 1.4:

```
CREATE TABLE model (
  col1 INTEGER,
  col3 INTEGER,
  col2 INTEGER,
  col4 INTEGER,
  id INTEGER NOT NULL,
  PRIMARY KEY (id)
)
```

Whereas on 2.0 it produces:

```
CREATE TABLE model (
  id INTEGER NOT NULL,
  col1 INTEGER,
  col3 INTEGER,
  col2 INTEGER,
  col4 INTEGER,
  PRIMARY KEY (id)
)
```

For the specific case above, this can be seen as an improvement, as the primary
key columns on the `Model` are now where one would typically prefer.  However,
this is no comfort for the application that defined models the other way
around, as:

```
class Foo:
    id = mapped_column(Integer, primary_key=True)
    col1 = mapped_column(Integer)
    col3 = mapped_column(Integer)

class Model(Foo, Base):
    col2 = mapped_column(Integer)
    col4 = mapped_column(Integer)
    __tablename__ = "model"
```

This now produces CREATE TABLE output as:

```
CREATE TABLE model (
  col2 INTEGER,
  col4 INTEGER,
  id INTEGER NOT NULL,
  col1 INTEGER,
  col3 INTEGER,
  PRIMARY KEY (id)
)
```

To solve this issue, SQLAlchemy 2.0.4 introduces a new parameter on
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) called [mapped_column.sort_order](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.sort_order),
which is an integer value, defaulting to `0`,
that can be set to a positive or negative value so that columns are placed
before or after other columns, as in the example below:

```
class Foo:
    id = mapped_column(Integer, primary_key=True, sort_order=-10)
    col1 = mapped_column(Integer, sort_order=-1)
    col3 = mapped_column(Integer)

class Model(Foo, Base):
    col2 = mapped_column(Integer)
    col4 = mapped_column(Integer)
    __tablename__ = "model"
```

The above model places “id” before all others and “col1” after “id”:

```
CREATE TABLE model (
  id INTEGER NOT NULL,
  col1 INTEGER,
  col2 INTEGER,
  col4 INTEGER,
  col3 INTEGER,
  PRIMARY KEY (id)
)
```

Future SQLAlchemy releases may opt to provide an explicit ordering hint for the
[mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct, as this ordering is ORM specific.

### TheSequenceconstruct reverts to not having any explicit default “start” value; impacts MS SQL Server

Prior to SQLAlchemy 1.4, the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) construct would emit only
simple `CREATE SEQUENCE` DDL, if no additional arguments were specified:

```
>>> # SQLAlchemy 1.3 (and 2.0)
>>> from sqlalchemy import Sequence
>>> from sqlalchemy.schema import CreateSequence
>>> print(CreateSequence(Sequence("my_seq")))
CREATE SEQUENCE my_seq
```

However, as [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) support was added for MS SQL Server, where the
default start value is inconveniently set to `-2**63`,
version 1.4 decided to default the DDL to emit a start value of 1, if
[Sequence.start](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.start) were not otherwise provided:

```
>>> # SQLAlchemy 1.4 (only)
>>> from sqlalchemy import Sequence
>>> from sqlalchemy.schema import CreateSequence
>>> print(CreateSequence(Sequence("my_seq")))
CREATE SEQUENCE my_seq START WITH 1
```

This change has introduced other complexities, including that when
the [Sequence.min_value](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.min_value) parameter is included, this default of
`1` should in fact default to what [Sequence.min_value](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.min_value)
states, else a min_value that’s below the start_value may be seen as
contradictory.     As looking at this issue started to become a bit of a
rabbit hole of other various edge cases, we decided to instead revert this
change and restore the original behavior of [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) which is
to have no opinion, and just emit CREATE SEQUENCE, allowing the database
itself to make its decisions on how the various parameters of `SEQUENCE`
should interact with each other.

Therefore, to ensure that the start value is 1 on all backends,
**the start value of 1 may be indicated explicitly**, as below:

```
>>> # All SQLAlchemy versions
>>> from sqlalchemy import Sequence
>>> from sqlalchemy.schema import CreateSequence
>>> print(CreateSequence(Sequence("my_seq", start=1)))
CREATE SEQUENCE my_seq START WITH 1
```

Beyond all of that, for autogeneration of integer primary keys on modern
backends including PostgreSQL, Oracle, SQL Server, the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity)
construct should be preferred, which also works the same way in 1.4 and 2.0
with no changes in behavior.

[#7211](https://www.sqlalchemy.org/trac/ticket/7211)

### “with_variant()” clones the original TypeEngine rather than changing the type

The [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method, which is used to apply
alternate per-database behaviors to a particular type, now returns a copy of
the original [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object with the variant information
stored internally, rather than wrapping it inside the `Variant` class.

While the previous `Variant` approach was able to maintain all the in-Python
behaviors of the original type using dynamic attribute getters, the improvement
here is that when calling upon a variant, the returned type remains an instance
of the original type, which works more smoothly with type checkers such as mypy
and pylance.  Given a program as below:

```
import typing

from sqlalchemy import String
from sqlalchemy.dialects.mysql import VARCHAR

type_ = String(255).with_variant(VARCHAR(255, charset="utf8mb4"), "mysql", "mariadb")

if typing.TYPE_CHECKING:
    reveal_type(type_)
```

A type checker like pyright will now report the type as:

```
info: Type of "type_" is "String"
```

In addition, as illustrated above, multiple dialect names may be passed for
single type, in particular this is helpful for the pair of `"mysql"` and
`"mariadb"` dialects which are considered separately as of SQLAlchemy 1.4.

[#6980](https://www.sqlalchemy.org/trac/ticket/6980)

### Python division operator performs true division for all backends; added floor division

The Core expression language now supports both “true division” (i.e. the `/`
Python operator) and “floor division” (i.e. the `//` Python operator)
including backend-specific behaviors to normalize different databases in this
regard.

Given a “true division” operation against two integer values:

```
expr = literal(5, Integer) / literal(10, Integer)
```

The SQL division operator on PostgreSQL for example normally acts as “floor division”
when used against integers, meaning the above result would return the integer
“0”.  For this and similar backends, SQLAlchemy now renders the SQL using
a form which is equivalent towards:

```
%(param_1)s / CAST(%(param_2)s AS NUMERIC)
```

With `param_1=5`, `param_2=10`, so that the return expression will be of type
NUMERIC, typically as the Python value `decimal.Decimal("0.5")`.

Given a “floor division” operation against two integer values:

```
expr = literal(5, Integer) // literal(10, Integer)
```

The SQL division operator on MySQL and Oracle for example normally acts
as “true division” when used against integers, meaning the above result
would return the floating point value “0.5”.  For these and similar backends,
SQLAlchemy now renders the SQL using a form which is equivalent towards:

```
FLOOR(%(param_1)s / %(param_2)s)
```

With param_1=5, param_2=10, so that the return expression will be of type
INTEGER, as the Python value `0`.

The backwards-incompatible change here would be if an application using
PostgreSQL, SQL Server, or SQLite which relied on the Python “truediv” operator
to return an integer value in all cases.  Applications which rely upon this
behavior should instead use the Python “floor division” operator `//`
for these operations, or for forwards compatibility when using a previous
SQLAlchemy version, the floor function:

```
expr = func.floor(literal(5, Integer) / literal(10, Integer))
```

The above form would be needed on any SQLAlchemy version prior to 2.0
in order to provide backend-agnostic floor division.

[#4926](https://www.sqlalchemy.org/trac/ticket/4926)

### Session raises proactively when illegal concurrent or reentrant access is detected

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can now trap more errors related to illegal concurrent
state changes within multithreaded or other concurrent scenarios as well as for
event hooks which perform unexpected state changes.

One error that’s been known to occur when a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is used in
multiple threads simultaneously is
`AttributeError: 'NoneType' object has no attribute 'twophase'`, which is
completely cryptic. This error occurs when a thread calls
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) which internally invokes the
`SessionTransaction.close()` method to end the transactional context,
at the same time that another thread is in progress running a query
as from [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).  Within [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute),
the internal method that acquires a database connection for the current
transaction first begins by asserting that the session is “active”, but
after this assertion passes, the concurrent call to [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close)
interferes with this state which leads to the undefined condition above.

The change applies guards to all state-changing methods surrounding the
[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) object so that in the above case, the
[Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) method will instead fail as it will seek to change
the state to one that is disallowed for the duration of the already-in-progress
method that wants to get the current connection to run a database query.

Using the test script illustrated at [#7433](https://www.sqlalchemy.org/trac/ticket/7433), the previous
error case looks like:

```
Traceback (most recent call last):
File "/home/classic/dev/sqlalchemy/test3.py", line 30, in worker
    sess.execute(select(A)).all()
File "/home/classic/tmp/sqlalchemy/lib/sqlalchemy/orm/session.py", line 1691, in execute
    conn = self._connection_for_bind(bind)
File "/home/classic/tmp/sqlalchemy/lib/sqlalchemy/orm/session.py", line 1532, in _connection_for_bind
    return self._transaction._connection_for_bind(
File "/home/classic/tmp/sqlalchemy/lib/sqlalchemy/orm/session.py", line 754, in _connection_for_bind
    if self.session.twophase and self._parent is None:
AttributeError: 'NoneType' object has no attribute 'twophase'
```

Where the `_connection_for_bind()` method isn’t able to continue since
concurrent access placed it into an invalid state.  Using the new approach, the
originator of the state change throws the error instead:

```
File "/home/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 1785, in close
   self._close_impl(invalidate=False)
File "/home/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 1827, in _close_impl
   transaction.close(invalidate)
File "<string>", line 2, in close
File "/home/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 506, in _go
   raise sa_exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Method 'close()' can't be called here;
method '_connection_for_bind()' is already in progress and this would cause
an unexpected state change to symbol('CLOSED')
```

The state transition checks intentionally don’t use explicit locks to detect
concurrent thread activity, instead relying upon simple attribute set / value
test operations that inherently fail when unexpected concurrent changes occur.
The rationale is that the approach can detect illegal state changes that occur
entirely within a single thread, such as an event handler that runs on session
transaction events calls a state-changing method that’s not expected, or under
asyncio if a particular [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) were shared among multiple
asyncio tasks, as well as when using patching-style concurrency approaches
such as gevent.

[#7433](https://www.sqlalchemy.org/trac/ticket/7433)

### The SQLite dialect uses QueuePool for file-based databases

The SQLite dialect now defaults to [QueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool) when a file
based database is used. This is set along with setting the
`check_same_thread` parameter to `False`. It has been observed that the
previous approach of defaulting to [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool), which does not
hold onto database connections after they are released, did in fact have a
measurable negative performance impact. As always, the pool class is
customizable via the [create_engine.poolclass](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.poolclass) parameter.

Changed in version 2.0.38: - an equivalent change is also made for the
`aiosqlite` dialect, using [AsyncAdaptedQueuePool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.AsyncAdaptedQueuePool) instead
of [NullPool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.NullPool).  The `aiosqlite` dialect was not included
in the initial change in error.

See also

[Threading/Pooling Behavior](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-threading-pooling)

[#7490](https://www.sqlalchemy.org/trac/ticket/7490)

### New Oracle FLOAT type with binary precision; decimal precision not accepted directly

A new datatype [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) has been added to the Oracle dialect, to
accompany the addition of [Double](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Double) and database-specific
[DOUBLE](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE), [DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION) and
[REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL) datatypes. Oracle’s `FLOAT` accepts a so-called
“binary precision” parameter that per Oracle documentation is roughly a
standard “precision” value divided by 0.3103:

```
from sqlalchemy.dialects import oracle

Table("some_table", metadata, Column("value", oracle.FLOAT(126)))
```

A binary precision value of 126 is synonymous with using the
[DOUBLE_PRECISION](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DOUBLE_PRECISION) datatype, and a value of 63 is equivalent
to using the [REAL](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.REAL) datatype.  Other precision values are
specific to the [FLOAT](https://docs.sqlalchemy.org/en/20/dialects/oracle.html#sqlalchemy.dialects.oracle.FLOAT) type itself.

The SQLAlchemy [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) datatype also accepts a “precision”
parameter, but this is decimal precision which is not accepted by
Oracle.  Rather than attempting to guess the conversion, the Oracle dialect
will now raise an informative error if [Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) is used with
a precision value against the Oracle backend.  To specify a
[Float](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Float) datatype with an explicit precision value for
supporting backends, while also supporting other backends, use
the [TypeEngine.with_variant()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.with_variant) method as follows:

```
from sqlalchemy.types import Float
from sqlalchemy.dialects import oracle

Table(
    "some_table",
    metadata,
    Column("value", Float(5).with_variant(oracle.FLOAT(16), "oracle")),
)
```

### New RANGE / MULTIRANGE support and changes for PostgreSQL backends

RANGE / MULTIRANGE support has been fully implemented for psycopg2, psycopg3,
and asyncpg dialects.  The new support uses a new SQLAlchemy-specific
[Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) object that is agnostic of the different backends
and does not require the use of backend-specific imports or extension
steps.  For multirange support, lists of [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range)
objects are used.

Code that used the previous psycopg2-specific types should be modified
to use [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range), which presents a compatible interface.

The [Range](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range) object also features comparison support which
mirrors that of PostgreSQL.  Implemented so far are [Range.contains()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.contains)
and [Range.contained_by()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.Range.contained_by) methods which work in the same way as
the PostgreSQL `@>` and `<@`.  Additional operator support may be added
in future releases.

See the documentation at [Range and Multirange Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-ranges) for background on
using the new feature.

See also

[Range and Multirange Types](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-ranges)

[#7156](https://www.sqlalchemy.org/trac/ticket/7156) [#8706](https://www.sqlalchemy.org/trac/ticket/8706)

### match()operator on PostgreSQL usesplainto_tsquery()rather thanto_tsquery()

The `Operators.match()` function now renders
`col @@ plainto_tsquery(expr)` on the PostgreSQL backend, rather than
`col @@ to_tsquery()`.  `plainto_tsquery()` accepts plain text whereas
`to_tsquery()` accepts specialized query symbols, and is therefore less
cross-compatible with other backends.

All PostgreSQL search functions and operators are available through use of
[func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) to generate PostgreSQL-specific functions and
[Operators.bool_op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.bool_op) (a boolean-typed version of [Operators.op()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.op))
to generate arbitrary operators, in the same manner as they are available
in previous versions.  See the examples at [Full Text Search](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-match).

Existing SQLAlchemy projects that make use of PG-specific directives within
`Operators.match()` should make use of `func.to_tsquery()` directly.
To render SQL in exactly the same form as would be present
in 1.4, see the version note at [Simple plain text matching with match()](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-simple-match).

[#7086](https://www.sqlalchemy.org/trac/ticket/7086)
