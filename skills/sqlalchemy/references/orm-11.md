# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Association Proxy

`associationproxy` is used to create a read/write view of a
target attribute across a relationship.  It essentially conceals
the usage of a “middle” attribute between two endpoints, and
can be used to cherry-pick fields from both a collection of
related objects or scalar relationship. or to reduce the verbosity
of using the association object pattern.
Applied creatively, the association proxy allows
the construction of sophisticated collections and dictionary
views of virtually any geometry, persisted to the database using
standard, transparently configured relational patterns.

## Simplifying Scalar Collections

Consider a many-to-many mapping between two classes, `User` and `Keyword`.
Each `User` can have any number of `Keyword` objects, and vice-versa
(the many-to-many pattern is described at [Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many)).
The example below illustrates this pattern in the same way, with the
exception of an extra attribute added to the `User` class called
`User.keywords`:

```
from __future__ import annotations

from typing import Final
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    kw: Mapped[List[Keyword]] = relationship(secondary=lambda: user_keyword_table)

    def __init__(self, name: str):
        self.name = name

    # proxy the 'keyword' attribute from the 'kw' relationship
    keywords: AssociationProxy[List[str]] = association_proxy("kw", "keyword")

class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword

user_keyword_table: Final[Table] = Table(
    "user_keyword",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keyword.id"), primary_key=True),
)
```

In the above example, [association_proxy()](#sqlalchemy.ext.associationproxy.association_proxy) is applied to the `User`
class to produce a “view” of the `kw` relationship, which exposes the string
value of `.keyword` associated with each `Keyword` object.  It also
creates new `Keyword` objects transparently when strings are added to the
collection:

```
>>> user = User("jek")
>>> user.keywords.append("cheese-inspector")
>>> user.keywords.append("snack-ninja")
>>> print(user.keywords)
['cheese-inspector', 'snack-ninja']
```

To understand the mechanics of this, first review the behavior of
`User` and `Keyword` without using the `.keywords` association proxy.
Normally, reading and manipulating the collection of “keyword” strings associated
with `User` requires traversal from each collection element to the `.keyword`
attribute, which can be awkward.  The example below illustrates the identical
series of operations applied without using the association proxy:

```
>>> # identical operations without using the association proxy
>>> user = User("jek")
>>> user.kw.append(Keyword("cheese-inspector"))
>>> user.kw.append(Keyword("snack-ninja"))
>>> print([keyword.keyword for keyword in user.kw])
['cheese-inspector', 'snack-ninja']
```

The [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) object produced by the [association_proxy()](#sqlalchemy.ext.associationproxy.association_proxy) function
is an instance of a [Python descriptor](https://docs.python.org/howto/descriptor.html),
and is not considered to be “mapped” by the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) in any way.  Therefore,
it’s always indicated inline within the class definition of the mapped class,
regardless of whether Declarative or Imperative mappings are used.

The proxy functions by operating upon the underlying mapped attribute
or collection in response to operations, and changes made via the proxy are immediately
apparent in the mapped attribute, as well as vice versa.   The underlying
attribute remains fully accessible.

When first accessed, the association proxy performs introspection
operations on the target collection so that its behavior corresponds correctly.
Details such as if the locally proxied attribute is a collection (as is typical)
or a scalar reference, as well as if the collection acts like a set, list,
or dictionary is taken into account, so that the proxy should act just like
the underlying collection or attribute does.

### Creation of New Values

When a list `append()` event (or set `add()`, dictionary `__setitem__()`,
or scalar assignment event) is intercepted by the association proxy, it
instantiates a new instance of the “intermediary” object using its constructor,
passing as a single argument the given value. In our example above, an
operation like:

```
user.keywords.append("cheese-inspector")
```

Is translated by the association proxy into the operation:

```
user.kw.append(Keyword("cheese-inspector"))
```

The example works here because we have designed the constructor for `Keyword`
to accept a single positional argument, `keyword`. For those cases where a
single-argument constructor isn’t feasible, the association proxy’s creational
behavior can be customized using the [association_proxy.creator](#sqlalchemy.ext.associationproxy.association_proxy.params.creator)
argument, which references a callable (i.e. Python function) that will produce
a new object instance given the singular argument. Below we illustrate this
using a lambda as is typical:

```
class User(Base):
    ...

    # use Keyword(keyword=kw) on append() events
    keywords: AssociationProxy[List[str]] = association_proxy(
        "kw", "keyword", creator=lambda kw: Keyword(keyword=kw)
    )
```

The `creator` function accepts a single argument in the case of a list-
or set- based collection, or a scalar attribute.  In the case of a dictionary-based
collection, it accepts two arguments, “key” and “value”.   An example
of this is below in [Proxying to Dictionary Based Collections](#proxying-dictionaries).

## Simplifying Association Objects

The “association object” pattern is an extended form of a many-to-many
relationship, and is described at [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-pattern). Association
proxies are useful for keeping “association objects” out of the way during
regular use.

Suppose our `user_keyword` table above had additional columns
which we’d like to map explicitly, but in most cases we don’t
require direct access to these attributes.  Below, we illustrate
a new mapping which introduces the `UserKeywordAssociation` class, which
is mapped to the `user_keyword` table illustrated earlier.
This class adds an additional column `special_key`, a value which
we occasionally want to access, but not in the usual case.   We
create an association proxy on the `User` class called
`keywords`, which will bridge the gap from the `user_keyword_associations`
collection of `User` to the `.keyword` attribute present on each
`UserKeywordAssociation`:

```
from __future__ import annotations

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    user_keyword_associations: Mapped[List[UserKeywordAssociation]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # association proxy of "user_keyword_associations" collection
    # to "keyword" attribute
    keywords: AssociationProxy[List[Keyword]] = association_proxy(
        "user_keyword_associations",
        "keyword",
        creator=lambda keyword_obj: UserKeywordAssociation(keyword=keyword_obj),
    )

    def __init__(self, name: str):
        self.name = name

class UserKeywordAssociation(Base):
    __tablename__ = "user_keyword"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id"), primary_key=True)
    special_key: Mapped[Optional[str]] = mapped_column(String(50))

    user: Mapped[User] = relationship(back_populates="user_keyword_associations")

    keyword: Mapped[Keyword] = relationship()

class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column("keyword", String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword

    def __repr__(self) -> str:
        return f"Keyword({self.keyword!r})"
```

With the above configuration, we can operate upon the `.keywords` collection
of each `User` object, each of which exposes a collection of `Keyword`
objects that are obtained from the underlying `UserKeywordAssociation` elements:

```
>>> user = User("log")
>>> for kw in (Keyword("new_from_blammo"), Keyword("its_big")):
...     user.keywords.append(kw)
>>> print(user.keywords)
[Keyword('new_from_blammo'), Keyword('its_big')]
```

This example is in contrast to the example illustrated previously at
[Simplifying Scalar Collections](#associationproxy-scalar-collections), where the association proxy exposed
a collection of strings, rather than a collection of composed objects.
In this case, each `.keywords.append()` operation is equivalent to:

```
>>> user.user_keyword_associations.append(
...     UserKeywordAssociation(keyword=Keyword("its_heavy"))
... )
```

The `UserKeywordAssociation` object has two attributes that are both
populated within the scope of the `append()` operation of the association
proxy; `.keyword`, which refers to the
`Keyword` object, and `.user`, which refers to the `User` object.
The `.keyword` attribute is populated first, as the association proxy
generates a new `UserKeywordAssociation` object in response to the `.append()`
operation, assigning the given `Keyword` instance to the `.keyword`
attribute. Then, as the `UserKeywordAssociation` object is appended to the
`User.user_keyword_associations` collection, the `UserKeywordAssociation.user` attribute,
configured as `back_populates` for `User.user_keyword_associations`, is initialized
upon the given `UserKeywordAssociation` instance to refer to the parent `User`
receiving the append operation.  The `special_key`
argument above is left at its default value of `None`.

For those cases where we do want `special_key` to have a value, we
create the `UserKeywordAssociation` object explicitly.  Below we assign all
three attributes, wherein the assignment of `.user` during
construction, has the effect of appending the new `UserKeywordAssociation` to
the `User.user_keyword_associations` collection (via the relationship):

```
>>> UserKeywordAssociation(
...     keyword=Keyword("its_wood"), user=user, special_key="my special key"
... )
```

The association proxy returns to us a collection of `Keyword` objects represented
by all these operations:

```
>>> print(user.keywords)
[Keyword('new_from_blammo'), Keyword('its_big'), Keyword('its_heavy'), Keyword('its_wood')]
```

## Proxying to Dictionary Based Collections

The association proxy can proxy to dictionary based collections as well.   SQLAlchemy
mappings usually use the [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict) collection type to
create dictionary collections, as well as the extended techniques described in
[Custom Dictionary-Based Collections](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#id1).

The association proxy adjusts its behavior when it detects the usage of a
dictionary-based collection. When new values are added to the dictionary, the
association proxy instantiates the intermediary object by passing two
arguments to the creation function instead of one, the key and the value. As
always, this creation function defaults to the constructor of the intermediary
class, and can be customized using the `creator` argument.

Below, we modify our `UserKeywordAssociation` example such that the `User.user_keyword_associations`
collection will now be mapped using a dictionary, where the `UserKeywordAssociation.special_key`
argument will be used as the key for the dictionary.   We also apply a `creator`
argument to the `User.keywords` proxy so that these values are assigned appropriately
when new elements are added to the dictionary:

```
from __future__ import annotations
from typing import Dict

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    # user/user_keyword_associations relationship, mapping
    # user_keyword_associations with a dictionary against "special_key" as key.
    user_keyword_associations: Mapped[Dict[str, UserKeywordAssociation]] = relationship(
        back_populates="user",
        collection_class=attribute_keyed_dict("special_key"),
        cascade="all, delete-orphan",
    )
    # proxy to 'user_keyword_associations', instantiating
    # UserKeywordAssociation assigning the new key to 'special_key',
    # values to 'keyword'.
    keywords: AssociationProxy[Dict[str, Keyword]] = association_proxy(
        "user_keyword_associations",
        "keyword",
        creator=lambda k, v: UserKeywordAssociation(special_key=k, keyword=v),
    )

    def __init__(self, name: str):
        self.name = name

class UserKeywordAssociation(Base):
    __tablename__ = "user_keyword"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id"), primary_key=True)
    special_key: Mapped[str]

    user: Mapped[User] = relationship(
        back_populates="user_keyword_associations",
    )
    keyword: Mapped[Keyword] = relationship()

class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword

    def __repr__(self) -> str:
        return f"Keyword({self.keyword!r})"
```

We illustrate the `.keywords` collection as a dictionary, mapping the
`UserKeywordAssociation.special_key` value to `Keyword` objects:

```
>>> user = User("log")

>>> user.keywords["sk1"] = Keyword("kw1")
>>> user.keywords["sk2"] = Keyword("kw2")

>>> print(user.keywords)
{'sk1': Keyword('kw1'), 'sk2': Keyword('kw2')}
```

## Composite Association Proxies

Given our previous examples of proxying from relationship to scalar
attribute, proxying across an association object, and proxying dictionaries,
we can combine all three techniques together to give `User`
a `keywords` dictionary that deals strictly with the string value
of `special_key` mapped to the string `keyword`.  Both the `UserKeywordAssociation`
and `Keyword` classes are entirely concealed.  This is achieved by building
an association proxy on `User` that refers to an association proxy
present on `UserKeywordAssociation`:

```
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    user_keyword_associations: Mapped[Dict[str, UserKeywordAssociation]] = relationship(
        back_populates="user",
        collection_class=attribute_keyed_dict("special_key"),
        cascade="all, delete-orphan",
    )
    # the same 'user_keyword_associations'->'keyword' proxy as in
    # the basic dictionary example.
    keywords: AssociationProxy[Dict[str, str]] = association_proxy(
        "user_keyword_associations",
        "keyword",
        creator=lambda k, v: UserKeywordAssociation(special_key=k, keyword=v),
    )

    def __init__(self, name: str):
        self.name = name

class UserKeywordAssociation(Base):
    __tablename__ = "user_keyword"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id"), primary_key=True)
    special_key: Mapped[str] = mapped_column(String(64))
    user: Mapped[User] = relationship(
        back_populates="user_keyword_associations",
    )

    # the relationship to Keyword is now called
    # 'kw'
    kw: Mapped[Keyword] = relationship()

    # 'keyword' is changed to be a proxy to the
    # 'keyword' attribute of 'Keyword'
    keyword: AssociationProxy[Dict[str, str]] = association_proxy("kw", "keyword")

class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))

    def __init__(self, keyword: str):
        self.keyword = keyword
```

`User.keywords` is now a dictionary of string to string, where
`UserKeywordAssociation` and `Keyword` objects are created and removed for us
transparently using the association proxy. In the example below, we illustrate
usage of the assignment operator, also appropriately handled by the
association proxy, to apply a dictionary value to the collection at once:

```
>>> user = User("log")
>>> user.keywords = {"sk1": "kw1", "sk2": "kw2"}
>>> print(user.keywords)
{'sk1': 'kw1', 'sk2': 'kw2'}

>>> user.keywords["sk3"] = "kw3"
>>> del user.keywords["sk2"]
>>> print(user.keywords)
{'sk1': 'kw1', 'sk3': 'kw3'}

>>> # illustrate un-proxied usage
... print(user.user_keyword_associations["sk3"].kw)
<__main__.Keyword object at 0x12ceb90>
```

One caveat with our example above is that because `Keyword` objects are created
for each dictionary set operation, the example fails to maintain uniqueness for
the `Keyword` objects on their string name, which is a typical requirement for
a tagging scenario such as this one.  For this use case the recipe
[UniqueObject](https://www.sqlalchemy.org/trac/wiki/UsageRecipes/UniqueObject), or
a comparable creational strategy, is
recommended, which will apply a “lookup first, then create” strategy to the constructor
of the `Keyword` class, so that an already existing `Keyword` is returned if the
given name is already present.

## Querying with Association Proxies

The [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) features simple SQL construction capabilities
which work at the class level in a similar way as other ORM-mapped attributes,
and provide rudimentary filtering support primarily based on the
SQL `EXISTS` keyword.

Note

The primary purpose of the association proxy extension is to allow
for improved persistence and object-access patterns with mapped object
instances that are already loaded.  The class-bound querying feature
is of limited use and will not replace the need to refer to the underlying
attributes when constructing SQL queries with JOINs, eager loading
options, etc.

For this section, assume a class with both an association proxy
that refers to a column, as well as an association proxy that refers
to a related object, as in the example mapping below:

```
from __future__ import annotations
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm.collections import attribute_keyed_dict
from sqlalchemy.orm.collections import Mapped

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    user_keyword_associations: Mapped[UserKeywordAssociation] = relationship(
        cascade="all, delete-orphan",
    )

    # object-targeted association proxy
    keywords: AssociationProxy[List[Keyword]] = association_proxy(
        "user_keyword_associations",
        "keyword",
    )

    # column-targeted association proxy
    special_keys: AssociationProxy[List[str]] = association_proxy(
        "user_keyword_associations", "special_key"
    )

class UserKeywordAssociation(Base):
    __tablename__ = "user_keyword"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id"), primary_key=True)
    special_key: Mapped[str] = mapped_column(String(64))
    keyword: Mapped[Keyword] = relationship()

class Keyword(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(64))
```

The SQL generated takes the form of a correlated subquery against
the EXISTS SQL operator so that it can be used in a WHERE clause without
the need for additional modifications to the enclosing query.  If the
immediate target of an association proxy is a **mapped column expression**,
standard column operators can be used which will be embedded in the subquery.
For example a straight equality operator:

```
>>> print(session.scalars(select(User).where(User.special_keys == "jek")))
SELECT "user".id AS user_id, "user".name AS user_name
FROM "user"
WHERE EXISTS (SELECT 1
FROM user_keyword
WHERE "user".id = user_keyword.user_id AND user_keyword.special_key = :special_key_1)
```

a LIKE operator:

```
>>> print(session.scalars(select(User).where(User.special_keys.like("%jek"))))
SELECT "user".id AS user_id, "user".name AS user_name
FROM "user"
WHERE EXISTS (SELECT 1
FROM user_keyword
WHERE "user".id = user_keyword.user_id AND user_keyword.special_key LIKE :special_key_1)
```

For association proxies where the immediate target is a **related object or collection,
or another association proxy or attribute on the related object**, relationship-oriented
operators can be used instead, such as [PropComparator.has()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.has) and
[PropComparator.any()](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator.any).   The `User.keywords` attribute is in fact
two association proxies linked together, so when using this proxy for generating
SQL phrases, we get two levels of EXISTS subqueries:

```
>>> print(session.scalars(select(User).where(User.keywords.any(Keyword.keyword == "jek"))))
SELECT "user".id AS user_id, "user".name AS user_name
FROM "user"
WHERE EXISTS (SELECT 1
FROM user_keyword
WHERE "user".id = user_keyword.user_id AND (EXISTS (SELECT 1
FROM keyword
WHERE keyword.id = user_keyword.keyword_id AND keyword.keyword = :keyword_1)))
```

This is not the most efficient form of SQL, so while association proxies can be
convenient for generating WHERE criteria quickly, SQL results should be
inspected and “unrolled” into explicit JOIN criteria for best use, especially
when chaining association proxies together.

Changed in version 1.3: Association proxy features distinct querying modes
based on the type of target.   See [AssociationProxy now provides standard column operators for a column-oriented target](https://docs.sqlalchemy.org/en/20/changelog/migration_13.html#change-4351).

## Cascading Scalar Deletes

Added in version 1.3.

Given a mapping as:

```
from __future__ import annotations
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm.collections import attribute_keyed_dict
from sqlalchemy.orm.collections import Mapped

class Base(DeclarativeBase):
    pass

class A(Base):
    __tablename__ = "test_a"
    id: Mapped[int] = mapped_column(primary_key=True)
    ab: Mapped[AB] = relationship(uselist=False)
    b: AssociationProxy[B] = association_proxy(
        "ab", "b", creator=lambda b: AB(b=b), cascade_scalar_deletes=True
    )

class B(Base):
    __tablename__ = "test_b"
    id: Mapped[int] = mapped_column(primary_key=True)

class AB(Base):
    __tablename__ = "test_ab"
    a_id: Mapped[int] = mapped_column(ForeignKey(A.id), primary_key=True)
    b_id: Mapped[int] = mapped_column(ForeignKey(B.id), primary_key=True)

    b: Mapped[B] = relationship()
```

An assignment to `A.b` will generate an `AB` object:

```
a.b = B()
```

The `A.b` association is scalar, and includes use of the parameter
[AssociationProxy.cascade_scalar_deletes](#sqlalchemy.ext.associationproxy.AssociationProxy.params.cascade_scalar_deletes).  When this parameter
is enabled, setting `A.b`
to `None` will remove `A.ab` as well:

```
a.b = None
assert a.ab is None
```

When [AssociationProxy.cascade_scalar_deletes](#sqlalchemy.ext.associationproxy.AssociationProxy.params.cascade_scalar_deletes) is not set,
the association object `a.ab` above would remain in place.

Note that this is not the behavior for collection-based association proxies;
in that case, the intermediary association object is always removed when
members of the proxied collection are removed.  Whether or not the row is
deleted depends on the relationship cascade setting.

See also

[Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades)

## Scalar Relationships

The example below illustrates the use of the association proxy on the many
side of of a one-to-many relationship, accessing attributes of a scalar
object:

```
from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Recipe(Base):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    steps: Mapped[List[Step]] = relationship(back_populates="recipe")
    step_descriptions: AssociationProxy[List[str]] = association_proxy(
        "steps", "description"
    )

class Step(Base):
    __tablename__ = "step"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    recipe: Mapped[Recipe] = relationship(back_populates="steps")

    recipe_name: AssociationProxy[str] = association_proxy("recipe", "name")

    def __init__(self, description: str) -> None:
        self.description = description

my_snack = Recipe(
    name="afternoon snack",
    step_descriptions=[
        "slice bread",
        "spread peanut butted",
        "eat sandwich",
    ],
)
```

A summary of the steps of `my_snack` can be printed using:

```
>>> for i, step in enumerate(my_snack.steps, 1):
...     print(f"Step {i} of {step.recipe_name!r}: {step.description}")
Step 1 of 'afternoon snack': slice bread
Step 2 of 'afternoon snack': spread peanut butted
Step 3 of 'afternoon snack': eat sandwich
```

## API Documentation

| Object Name | Description |
| --- | --- |
| association_proxy(target_collection, attr, *, [creator, getset_factory, proxy_factory, proxy_bulk_set, info, cascade_scalar_deletes, create_on_none_assignment, init, repr, default, default_factory, compare, kw_only, hash, dataclass_metadata]) | Return a Python property implementing a view of a target
attribute which references an attribute on members of the
target. |
| AssociationProxy | A descriptor that presents a read/write view of an object attribute. |
| AssociationProxyExtensionType |  |
| AssociationProxyInstance | A per-class object that serves class- and object-specific results. |
| ColumnAssociationProxyInstance | anAssociationProxyInstancethat has a database column as a
target. |
| ObjectAssociationProxyInstance | anAssociationProxyInstancethat has an object as a target. |

   function sqlalchemy.ext.associationproxy.association_proxy(*target_collection:str*, *attr:str*, ***, *creator:_CreatorProtocol|None=None*, *getset_factory:_GetSetFactoryProtocol|None=None*, *proxy_factory:_ProxyFactoryProtocol|None=None*, *proxy_bulk_set:_ProxyBulkSetProtocol|None=None*, *info:_InfoType|None=None*, *cascade_scalar_deletes:bool=False*, *create_on_none_assignment:bool=False*, *init:_NoArg|bool=_NoArg.NO_ARG*, *repr:_NoArg|bool=_NoArg.NO_ARG*, *default:Any|None=_NoArg.NO_ARG*, *default_factory:_NoArg|Callable[[],_T]=_NoArg.NO_ARG*, *compare:_NoArg|bool=_NoArg.NO_ARG*, *kw_only:_NoArg|bool=_NoArg.NO_ARG*, *hash:_NoArg|bool|None=_NoArg.NO_ARG*, *dataclass_metadata:_NoArg|Mapping[Any,Any]|None=_NoArg.NO_ARG*) → [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy)[Any]

Return a Python property implementing a view of a target
attribute which references an attribute on members of the
target.

The returned value is an instance of [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy).

Implements a Python property representing a relationship as a collection
of simpler values, or a scalar value.  The proxied property will mimic
the collection type of the target (list, dict or set), or, in the case of
a one to one relationship, a simple scalar value.

  Parameters:

- **target_collection** – Name of the attribute that is the immediate
  target.  This attribute is typically mapped by
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) to link to a target collection, but
  can also be a many-to-one or non-scalar relationship.
- **attr** – Attribute on the associated instance or instances that
  are available on instances of the target object.
- **creator** –
  optional.
  Defines custom behavior when new items are added to the proxied
  collection.
  By default, adding new items to the collection will trigger a
  construction of an instance of the target object, passing the given
  item as a positional argument to the target constructor.  For cases
  where this isn’t sufficient, [association_proxy.creator](#sqlalchemy.ext.associationproxy.association_proxy.params.creator)
  can supply a callable that will construct the object in the
  appropriate way, given the item that was passed.
  For list- and set- oriented collections, a single argument is
  passed to the callable. For dictionary oriented collections, two
  arguments are passed, corresponding to the key and value.
  The [association_proxy.creator](#sqlalchemy.ext.associationproxy.association_proxy.params.creator) callable is also invoked
  for scalar (i.e. many-to-one, one-to-one) relationships. If the
  current value of the target relationship attribute is `None`, the
  callable is used to construct a new object.  If an object value already
  exists, the given attribute value is populated onto that object.
  See also
  [Creation of New Values](#associationproxy-creator)
- **cascade_scalar_deletes** –
  when True, indicates that setting
  the proxied value to `None`, or deleting it via `del`, should
  also remove the source object.  Only applies to scalar attributes.
  Normally, removing the proxied target will not remove the proxy
  source, as this object may have other state that is still to be
  kept.
  Added in version 1.3.
  See also
  [Cascading Scalar Deletes](#cascade-scalar-deletes) - complete usage example
- **create_on_none_assignment** –
  when True, indicates that setting
  the proxied value to `None` should **create** the source object
  if it does not exist, using the creator.  Only applies to scalar
  attributes.  This is mutually exclusive
  vs. the [association_proxy.cascade_scalar_deletes](#sqlalchemy.ext.associationproxy.association_proxy.params.cascade_scalar_deletes).
  Added in version 2.0.18.
- **init** –
  Specific to [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  specifies if the mapped attribute should be part of the `__init__()`
  method as generated by the dataclass process.
  Added in version 2.0.0b4.
- **repr** –
  Specific to [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  specifies if the attribute established by this [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy)
  should be part of the `__repr__()` method as generated by the dataclass
  process.
  Added in version 2.0.0b4.
- **default_factory** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), specifies a default-value
  generation function that will take place as part of the `__init__()`
  method as generated by the dataclass process.
  Added in version 2.0.0b4.
- **compare** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), indicates if this field
  should be included in comparison operations when generating the
  `__eq__()` and `__ne__()` methods for the mapped class.
  Added in version 2.0.0b4.
- **kw_only** –
  Specific to [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  indicates if this field should be marked as keyword-only when generating
  the `__init__()` method as generated by the dataclass process.
  Added in version 2.0.0b4.
- **hash** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), controls if this field
  is included when generating the `__hash__()` method for the mapped
  class.
  Added in version 2.0.36.
- **dataclass_metadata** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), supplies metadata
  to be attached to the generated dataclass field.
  Added in version 2.0.42.
- **info** – optional, will be assigned to
  [AssociationProxy.info](#sqlalchemy.ext.associationproxy.AssociationProxy.info) if present.

The following additional parameters involve injection of custom behaviors
within the [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) object and are for advanced use
only:

  Parameters:

- **getset_factory** –
  Optional.  Proxied attribute access is
  automatically handled by routines that get and set values based on
  the attr argument for this proxy.
  If you would like to customize this behavior, you may supply a
  getset_factory callable that produces a tuple of getter and
  setter functions.  The factory is called with two arguments, the
  abstract type of the underlying collection and this proxy instance.
- **proxy_factory** – Optional.  The type of collection to emulate is
  determined by sniffing the target collection.  If your collection
  type can’t be determined by duck typing or you’d like to use a
  different collection implementation, you may supply a factory
  function to produce those collections.  Only applicable to
  non-scalar relationships.
- **proxy_bulk_set** – Optional, use with proxy_factory.

      class sqlalchemy.ext.associationproxy.AssociationProxy

*inherits from* [sqlalchemy.orm.base.InspectionAttrInfo](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrInfo), `sqlalchemy.orm.base.ORMDescriptor`, `sqlalchemy.orm._DCAttributeOptions`, `sqlalchemy.ext.associationproxy._AssociationProxyProtocol`

A descriptor that presents a read/write view of an object attribute.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newAssociationProxy. |
| cascade_scalar_deletes |  |
| create_on_none_assignment |  |
| creator |  |
| extension_type | The extension type, if any.
Defaults toNotExtension.NOT_EXTENSION |
| for_class() | Return the internal state local to a specific mapped class. |
| getset_factory |  |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisInspectionAttr. |
| is_aliased_class | True if this object is an instance ofAliasedClass. |
| is_attribute | True if this object is a Pythondescriptor. |
| is_bundle | True if this object is an instance ofBundle. |
| is_clause_element | True if this object is an instance ofClauseElement. |
| is_instance | True if this object is an instance ofInstanceState. |
| is_mapper | True if this object is an instance ofMapper. |
| is_property | True if this object is an instance ofMapperProperty. |
| is_selectable | Return True if this object is an instance ofSelectable. |
| key |  |
| proxy_bulk_set |  |
| proxy_factory |  |
| target_collection |  |
| value_attr |  |

   method [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)__init__(*target_collection:str*, *attr:str*, ***, *creator:_CreatorProtocol|None=None*, *getset_factory:_GetSetFactoryProtocol|None=None*, *proxy_factory:_ProxyFactoryProtocol|None=None*, *proxy_bulk_set:_ProxyBulkSetProtocol|None=None*, *info:_InfoType|None=None*, *cascade_scalar_deletes:bool=False*, *create_on_none_assignment:bool=False*, *attribute_options:_AttributeOptions|None=None*)

Construct a new [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy).

The [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) object is typically constructed using
the [association_proxy()](#sqlalchemy.ext.associationproxy.association_proxy) constructor function. See the
description of [association_proxy()](#sqlalchemy.ext.associationproxy.association_proxy) for a description of all
parameters.

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)cascade_scalar_deletes: bool    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)create_on_none_assignment: bool    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)creator: _CreatorProtocol | None    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)extension_type: [InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType) = 'ASSOCIATION_PROXY'

The extension type, if any.
Defaults to `NotExtension.NOT_EXTENSION`

See also

[HybridExtensionType](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.HybridExtensionType)

[AssociationProxyExtensionType](#sqlalchemy.ext.associationproxy.AssociationProxyExtensionType)

     method [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)for_class(*class_:Type[Any]*, *obj:object|None=None*) → [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)[_T]

Return the internal state local to a specific mapped class.

E.g., given a class `User`:

```
class User(Base):
    # ...

    keywords = association_proxy("kws", "keyword")
```

If we access this [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) from
[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors), and we want to view the
target class for this proxy as mapped by `User`:

```
inspect(User).all_orm_descriptors["keywords"].for_class(User).target_class
```

This returns an instance of [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance) that
is specific to the `User` class.   The [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy)
object remains agnostic of its parent class.

  Parameters:

- **class_** – the class that we are returning state for.
- **obj** – optional, an instance of the class that is required
  if the attribute refers to a polymorphic target, e.g. where we have
  to look at the type of the actual destination object to get the
  complete path.

Added in version 1.3: - [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) no longer stores
any state specific to a particular parent class; the state is now
stored in per-class [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance) objects.

     attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)getset_factory: _GetSetFactoryProtocol | None    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)info

*inherited from the* `InspectionAttrInfo.info` *attribute of* [InspectionAttrInfo](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrInfo)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr).

The dictionary is generated when first accessed.  Alternatively,
it can be specified as a constructor argument to the
[column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property), [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), or
[composite()](https://docs.sqlalchemy.org/en/20/orm/composites.html#sqlalchemy.orm.composite)
functions.

See also

[QueryableAttribute.info](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute.info)

[SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info)

     attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_aliased_class = False

*inherited from the* `InspectionAttr.is_aliased_class` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of [AliasedClass](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.util.AliasedClass).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_attribute = True

True if this object is a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).

This can refer to one of many types.   Usually a
[QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) which handles attributes events on behalf
of a [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty).   But can also be an extension type
such as [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) or [hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property).
The [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type) will refer to a constant
identifying the specific subtype.

See also

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

     attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_bundle = False

*inherited from the* `InspectionAttr.is_bundle` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of [Bundle](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.Bundle).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_clause_element = False

*inherited from the* `InspectionAttr.is_clause_element` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_instance = False

*inherited from the* `InspectionAttr.is_instance` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_mapper = False

*inherited from the* `InspectionAttr.is_mapper` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_property = False

*inherited from the* `InspectionAttr.is_property` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

True if this object is an instance of [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)is_selectable = False

*inherited from the* `InspectionAttr.is_selectable` *attribute of* [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr)

Return True if this object is an instance of
[Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)key: str    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)proxy_bulk_set: _ProxyBulkSetProtocol | None    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)proxy_factory: _ProxyFactoryProtocol | None    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)target_collection: str    attribute [sqlalchemy.ext.associationproxy.AssociationProxy.](#sqlalchemy.ext.associationproxy.AssociationProxy)value_attr: str     class sqlalchemy.ext.associationproxy.AssociationProxyInstance

*inherits from* `sqlalchemy.orm.base.SQLORMOperations`

A per-class object that serves class- and object-specific results.

This is used by [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) when it is invoked
in terms of a specific class or instance of a class, i.e. when it is
used as a regular Python descriptor.

When referring to the [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) as a normal Python
descriptor, the [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance) is the object that
actually serves the information.   Under normal circumstances, its presence
is transparent:

```
>>> User.keywords.scalar
False
```

In the special case that the [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy) object is being
accessed directly, in order to get an explicit handle to the
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance), use the
[AssociationProxy.for_class()](#sqlalchemy.ext.associationproxy.AssociationProxy.for_class) method:

```
proxy_state = inspect(User).all_orm_descriptors["keywords"].for_class(User)

# view if proxy object is scalar or not
>>> proxy_state.scalar
False
```

Added in version 1.3.

| Member Name | Description |
| --- | --- |
| __eq__() | Implement the==operator. |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| __ne__() | Implement the!=operator. |
| all_() | Produce anall_()clause against the
parent object. |
| any() | Produce a proxied ‘any’ expression using EXISTS. |
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
| collection_class |  |
| concat() | Implement the ‘concat’ operator. |
| contains() | Implement the ‘contains’ operator. |
| delete() |  |
| desc() | Produce adesc()clause against the
parent object. |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| for_proxy() |  |
| get() |  |
| has() | Produce a proxied ‘has’ expression using EXISTS. |
| icontains() | Implement theicontainsoperator, e.g. case insensitive
version ofColumnOperators.contains(). |
| iendswith() | Implement theiendswithoperator, e.g. case insensitive
version ofColumnOperators.endswith(). |
| ilike() | Implement theilikeoperator, e.g. case insensitive LIKE. |
| in_() | Implement theinoperator. |
| info |  |
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
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| parent |  |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| scalar | ReturnTrueif thisAssociationProxyInstanceproxies a scalar relationship on the local side. |
| set() |  |
| startswith() | Implement thestartswithoperator. |
| target_class | The intermediary class handled by thisAssociationProxyInstance. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |

   method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)__eq__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__eq__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `==` operator.

In a column context, produces the clause `a = b`.
If the target is `None`, produces `a IS NULL`.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)__le__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)__lt__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)__ne__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__ne__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)all_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)any(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)any_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)asc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) clause against the
parent object.

    property attr: Tuple[SQLORMOperations[Any], SQLORMOperations[_T]]

Return a tuple of `(local_attr, remote_attr)`.

This attribute was originally intended to facilitate using the
[Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method to join across the two relationships
at once, however this makes use of a deprecated calling style.

To use `select.join()` or [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) with
an association proxy, the current method is to make use of the
[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr) and
[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr) attributes separately:

```
stmt = (
    select(Parent)
    .join(Parent.proxied.local_attr)
    .join(Parent.proxied.remote_attr)
)
```

A future release may seek to provide a more succinct join pattern
for association proxy attributes.

See also

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_and(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_lshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_not() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_or(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_rshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bitwise_xor(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)collate(*collation:str*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)

     attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)collection_class: Type[Any] | None    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)concat(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)delete(*obj:Any*) → None    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)desc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)distinct() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     classmethod [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)for_proxy(*parent:AssociationProxy[_T]*, *owning_class:Type[Any]*, *parent_instance:Any*) → [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)[_T]    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)get(*obj:Any*) → _T | None | [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)[_T]    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)has(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)in_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

      attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)info    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)is_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)is_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)is_not(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)is_not_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)isnot(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)isnot_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property local_attr: SQLORMOperations[Any]

The ‘local’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)not_in(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)notin_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)nulls_first() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)nulls_last() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)nullsfirst() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)nullslast() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

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

      attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)parent: _AssociationProxyProtocol[_T]    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property remote_attr: SQLORMOperations[_T]

The ‘remote’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

     method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.reverse_operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.reverse_operate) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.operate).

    attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)scalar

Return `True` if this [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)
proxies a scalar relationship on the local side.

    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)set(*obj:Any*, *values:_T*) → None    method [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)target_class: Type[Any]

The intermediary class handled by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

Intercepted append/set/assignment events will result
in the generation of new instances of this class.

    attribute [sqlalchemy.ext.associationproxy.AssociationProxyInstance.](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)timetuple: Literal[None] = None

*inherited from the* [ColumnOperators.timetuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

     class sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance

*inherits from* [sqlalchemy.ext.associationproxy.AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

an [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance) that has an object as a target.

| Member Name | Description |
| --- | --- |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| all_() | Produce anall_()clause against the
parent object. |
| any() | Produce a proxied ‘any’ expression using EXISTS. |
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
| contains() | Produce a proxied ‘contains’ expression using EXISTS. |
| desc() | Produce adesc()clause against the
parent object. |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| has() | Produce a proxied ‘has’ expression using EXISTS. |
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
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| scalar | ReturnTrueif thisAssociationProxyInstanceproxies a scalar relationship on the local side. |
| startswith() | Implement thestartswithoperator. |
| target_class | The intermediary class handled by thisAssociationProxyInstance. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |

   method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)__le__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)__lt__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)all_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)any(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

*inherited from the* [AssociationProxyInstance.any()](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.any) *method of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)any_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)asc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) clause against the
parent object.

    property attr: Tuple[SQLORMOperations[Any], SQLORMOperations[_T]]

Return a tuple of `(local_attr, remote_attr)`.

This attribute was originally intended to facilitate using the
[Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method to join across the two relationships
at once, however this makes use of a deprecated calling style.

To use `select.join()` or [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) with
an association proxy, the current method is to make use of the
[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr) and
[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr) attributes separately:

```
stmt = (
    select(Parent)
    .join(Parent.proxied.local_attr)
    .join(Parent.proxied.remote_attr)
)
```

A future release may seek to provide a more succinct join pattern
for association proxy attributes.

See also

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_and(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_lshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_not() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_or(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_rshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bitwise_xor(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)collate(*collation:str*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)concat(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)contains(*other:Any*, ***kw:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

Produce a proxied ‘contains’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`,
`Comparator.has()`,
and/or `Comparator.contains()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)desc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)distinct() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)has(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

*inherited from the* [AssociationProxyInstance.has()](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.has) *method of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)in_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

      method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)is_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)is_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)is_not(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)is_not_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)isnot(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)isnot_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property local_attr: SQLORMOperations[Any]

The ‘local’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)not_in(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)notin_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)nulls_first() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)nulls_last() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)nullsfirst() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)nullslast() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

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

      method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property remote_attr: SQLORMOperations[_T]

The ‘remote’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

     method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.reverse_operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.reverse_operate) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.operate).

    attribute [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)scalar

*inherited from the* [AssociationProxyInstance.scalar](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.scalar) *attribute of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Return `True` if this [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)
proxies a scalar relationship on the local side.

    method [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     attribute [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)target_class: Type[Any]

The intermediary class handled by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

Intercepted append/set/assignment events will result
in the generation of new instances of this class.

    attribute [sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ObjectAssociationProxyInstance)timetuple: Literal[None] = None

*inherited from the* [ColumnOperators.timetuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

     class sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance

*inherits from* [sqlalchemy.ext.associationproxy.AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

an [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance) that has a database column as a
target.

| Member Name | Description |
| --- | --- |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| __ne__() | Implement the!=operator. |
| all_() | Produce anall_()clause against the
parent object. |
| any() | Produce a proxied ‘any’ expression using EXISTS. |
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
| has() | Produce a proxied ‘has’ expression using EXISTS. |
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
| op() | Produce a generic operator function. |
| operate() | Operate on an argument. |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| scalar | ReturnTrueif thisAssociationProxyInstanceproxies a scalar relationship on the local side. |
| startswith() | Implement thestartswithoperator. |
| target_class | The intermediary class handled by thisAssociationProxyInstance. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |

   method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)__le__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)__lt__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)__ne__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__ne__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)all_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)any(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

*inherited from the* [AssociationProxyInstance.any()](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.any) *method of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Produce a proxied ‘any’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)any_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)asc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) clause against the
parent object.

    property attr: Tuple[SQLORMOperations[Any], SQLORMOperations[_T]]

Return a tuple of `(local_attr, remote_attr)`.

This attribute was originally intended to facilitate using the
[Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) method to join across the two relationships
at once, however this makes use of a deprecated calling style.

To use `select.join()` or [Query.join()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join) with
an association proxy, the current method is to make use of the
[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr) and
[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr) attributes separately:

```
stmt = (
    select(Parent)
    .join(Parent.proxied.local_attr)
    .join(Parent.proxied.remote_attr)
)
```

A future release may seek to provide a more succinct join pattern
for association proxy attributes.

See also

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_and(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_lshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_not() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_or(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_rshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bitwise_xor(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)collate(*collation:str*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)concat(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)desc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)distinct() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)has(*criterion:_ColumnExpressionArgument[bool]|None=None*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[bool]

*inherited from the* [AssociationProxyInstance.has()](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.has) *method of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Produce a proxied ‘has’ expression using EXISTS.

This expression will be a composed product
using the `Comparator.any()`
and/or `Comparator.has()`
operators of the underlying proxied attributes.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)in_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

      method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)is_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)is_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)is_not(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)is_not_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)isnot(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)isnot_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property local_attr: SQLORMOperations[Any]

The ‘local’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.remote_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.remote_attr)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)not_in(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)notin_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)nulls_first() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)nulls_last() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)nullsfirst() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)nullslast() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

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

      method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property remote_attr: SQLORMOperations[_T]

The ‘remote’ class attribute referenced by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

See also

[AssociationProxyInstance.attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.attr)

[AssociationProxyInstance.local_attr](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.local_attr)

     method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

*inherited from the* [Operators.reverse_operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.reverse_operate) *method of* [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.operate).

    attribute [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)scalar

*inherited from the* [AssociationProxyInstance.scalar](#sqlalchemy.ext.associationproxy.AssociationProxyInstance.scalar) *attribute of* [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)

Return `True` if this [AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance)
proxies a scalar relationship on the local side.

    method [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     attribute [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)target_class: Type[Any]

The intermediary class handled by this
[AssociationProxyInstance](#sqlalchemy.ext.associationproxy.AssociationProxyInstance).

Intercepted append/set/assignment events will result
in the generation of new instances of this class.

    attribute [sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance.](#sqlalchemy.ext.associationproxy.ColumnAssociationProxyInstance)timetuple: Literal[None] = None

*inherited from the* [ColumnOperators.timetuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

     class sqlalchemy.ext.associationproxy.AssociationProxyExtensionType

*inherits from* [sqlalchemy.orm.base.InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType)

| Member Name | Description |
| --- | --- |
| ASSOCIATION_PROXY | Symbol indicating anInspectionAttrthat’s
of typeAssociationProxy. |

   attribute [sqlalchemy.ext.associationproxy.AssociationProxyExtensionType.](#sqlalchemy.ext.associationproxy.AssociationProxyExtensionType)ASSOCIATION_PROXY = 'ASSOCIATION_PROXY'

Symbol indicating an [InspectionAttr](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr) that’s
of type [AssociationProxy](#sqlalchemy.ext.associationproxy.AssociationProxy).

Is assigned to the [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type)
attribute.
