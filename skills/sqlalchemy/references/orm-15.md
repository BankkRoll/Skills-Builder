# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Hybrid Attributes

Define attributes on ORM-mapped classes that have “hybrid” behavior.

“hybrid” means the attribute has distinct behaviors defined at the
class level and at the instance level.

The [hybrid](#module-sqlalchemy.ext.hybrid) extension provides a special form of
method decorator and has minimal dependencies on the rest of SQLAlchemy.
Its basic theory of operation can work with any descriptor-based expression
system.

Consider a mapping `Interval`, representing integer `start` and `end`
values. We can define higher level functions on mapped classes that produce SQL
expressions at the class level, and Python expression evaluation at the
instance level.  Below, each function decorated with [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method) or
[hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) may receive `self` as an instance of the class, or
may receive the class directly, depending on context:

```
from __future__ import annotations

from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Interval(Base):
    __tablename__ = "interval"

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[int]
    end: Mapped[int]

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @hybrid_property
    def length(self) -> int:
        return self.end - self.start

    @hybrid_method
    def contains(self, point: int) -> bool:
        return (self.start <= point) & (point <= self.end)

    @hybrid_method
    def intersects(self, other: Interval) -> bool:
        return self.contains(other.start) | self.contains(other.end)
```

Above, the `length` property returns the difference between the
`end` and `start` attributes.  With an instance of `Interval`,
this subtraction occurs in Python, using normal Python descriptor
mechanics:

```
>>> i1 = Interval(5, 10)
>>> i1.length
5
```

When dealing with the `Interval` class itself, the [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)
descriptor evaluates the function body given the `Interval` class as
the argument, which when evaluated with SQLAlchemy expression mechanics
returns a new SQL expression:

```
>>> from sqlalchemy import select
>>> print(select(Interval.length))
SELECT interval."end" - interval.start AS length
FROM interval
>>> print(select(Interval).filter(Interval.length > 10))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE interval."end" - interval.start > :param_1
```

Filtering methods such as [Select.filter_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.filter_by) are supported
with hybrid attributes as well:

```
>>> print(select(Interval).filter_by(length=5))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE interval."end" - interval.start = :param_1
```

The `Interval` class example also illustrates two methods,
`contains()` and `intersects()`, decorated with
[hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method). This decorator applies the same idea to
methods that [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) applies to attributes.   The
methods return boolean values, and take advantage of the Python `|`
and `&` bitwise operators to produce equivalent instance-level and
SQL expression-level boolean behavior:

```
>>> i1.contains(6)
True
>>> i1.contains(15)
False
>>> i1.intersects(Interval(7, 18))
True
>>> i1.intersects(Interval(25, 29))
False

>>> print(select(Interval).filter(Interval.contains(15)))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE interval.start <= :start_1 AND interval."end" > :end_1
>>> ia = aliased(Interval)
>>> print(select(Interval, ia).filter(Interval.intersects(ia)))
SELECT interval.id, interval.start,
interval."end", interval_1.id AS interval_1_id,
interval_1.start AS interval_1_start, interval_1."end" AS interval_1_end
FROM interval, interval AS interval_1
WHERE interval.start <= interval_1.start
    AND interval."end" > interval_1.start
    OR interval.start <= interval_1."end"
    AND interval."end" > interval_1."end"
```

## Defining Expression Behavior Distinct from Attribute Behavior

In the previous section, our usage of the `&` and `|` bitwise operators
within the `Interval.contains` and `Interval.intersects` methods was
fortunate, considering our functions operated on two boolean values to return a
new one. In many cases, the construction of an in-Python function and a
SQLAlchemy SQL expression have enough differences that two separate Python
expressions should be defined. The [hybrid](#module-sqlalchemy.ext.hybrid) decorator
defines a **modifier** [hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) for this purpose. As an
example we’ll define the radius of the interval, which requires the usage of
the absolute value function:

```
from sqlalchemy import ColumnElement
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import type_coerce

class Interval(Base):
    # ...

    @hybrid_property
    def radius(self) -> float:
        return abs(self.length) / 2

    @radius.inplace.expression
    @classmethod
    def _radius_expression(cls) -> ColumnElement[float]:
        return type_coerce(func.abs(cls.length) / 2, Float)
```

In the above example, the [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) first assigned to the
name `Interval.radius` is amended by a subsequent method called
`Interval._radius_expression`, using the decorator
`@radius.inplace.expression`, which chains together two modifiers
[hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) and [hybrid_property.expression](#sqlalchemy.ext.hybrid.hybrid_property.expression).
The use of [hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) indicates that the
[hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) modifier should mutate the
existing hybrid object at `Interval.radius` in place, without creating a
new object.   Notes on this modifier and its
rationale are discussed in the next section [Using inplace to create pep-484 compliant hybrid properties](#hybrid-pep484-naming).
The use of `@classmethod` is optional, and is strictly to give typing
tools a hint that `cls` in this case is expected to be the `Interval`
class, and not an instance of `Interval`.

Note

[hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) as well as the use of `@classmethod`
for proper typing support are available as of SQLAlchemy 2.0.4, and will
not work in earlier versions.

With `Interval.radius` now including an expression element, the SQL
function `ABS()` is returned when accessing `Interval.radius`
at the class level:

```
>>> from sqlalchemy import select
>>> print(select(Interval).filter(Interval.radius > 5))
SELECT interval.id, interval.start, interval."end"
FROM interval
WHERE abs(interval."end" - interval.start) / :abs_1 > :param_1
```

## Usinginplaceto create pep-484 compliant hybrid properties

In the previous section, a [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) decorator is illustrated
which includes two separate method-level functions being decorated, both
to produce a single object attribute referenced as `Interval.radius`.
There are actually several different modifiers we can use for
[hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) including [hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression),
[hybrid_property.setter()](#sqlalchemy.ext.hybrid.hybrid_property.setter) and [hybrid_property.update_expression()](#sqlalchemy.ext.hybrid.hybrid_property.update_expression).

SQLAlchemy’s [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) decorator intends that adding on these
methods may be done in the identical manner as Python’s built-in
`@property` decorator, where idiomatic use is to continue to redefine the
attribute repeatedly, using the **same attribute name** each time, as in the
example below that illustrates the use of [hybrid_property.setter()](#sqlalchemy.ext.hybrid.hybrid_property.setter) and
[hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) for the `Interval.radius` descriptor:

```
# correct use, however is not accepted by pep-484 tooling

class Interval(Base):
    # ...

    @hybrid_property
    def radius(self):
        return abs(self.length) / 2

    @radius.setter
    def radius(self, value):
        self.length = value * 2

    @radius.expression
    def radius(cls):
        return type_coerce(func.abs(cls.length) / 2, Float)
```

Above, there are three `Interval.radius` methods, but as each are decorated,
first by the [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) decorator and then by the
`@radius` name itself, the end effect is that `Interval.radius` is
a single attribute with three different functions contained within it.
This style of use is taken from [Python’s documented use of @property](https://docs.python.org/3/library/functions.html#property).
It is important to note that the way both `@property` as well as
[hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) work, a **copy of the descriptor is made each time**.
That is, each call to `@radius.expression`, `@radius.setter` etc.
make a new object entirely.  This allows the attribute to be re-defined in
subclasses without issue (see [Reusing Hybrid Properties across Subclasses](#hybrid-reuse-subclass) later in this
section for how this is used).

However, the above approach is not compatible with typing tools such as
mypy and pyright.  Python’s own `@property` decorator does not have this
limitation only because
[these tools hardcode the behavior of @property](https://github.com/python/typing/discussions/1102), meaning this syntax
is not available to SQLAlchemy under [PEP 484](https://peps.python.org/pep-0484/) compliance.

In order to produce a reasonable syntax while remaining typing compliant,
the [hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) decorator allows the same
decorator to be reused with different method names, while still producing
a single decorator under one name:

```
# correct use which is also accepted by pep-484 tooling

class Interval(Base):
    # ...

    @hybrid_property
    def radius(self) -> float:
        return abs(self.length) / 2

    @radius.inplace.setter
    def _radius_setter(self, value: float) -> None:
        # for example only
        self.length = value * 2

    @radius.inplace.expression
    @classmethod
    def _radius_expression(cls) -> ColumnElement[float]:
        return type_coerce(func.abs(cls.length) / 2, Float)
```

Using [hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) further qualifies the use of the
decorator that a new copy should not be made, thereby maintaining the
`Interval.radius` name while allowing additional methods
`Interval._radius_setter` and `Interval._radius_expression` to be
differently named.

Added in version 2.0.4: Added [hybrid_property.inplace](#sqlalchemy.ext.hybrid.hybrid_property.inplace) to allow
less verbose construction of composite [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property) objects
while not having to use repeated method names.   Additionally allowed the
use of `@classmethod` within [hybrid_property.expression](#sqlalchemy.ext.hybrid.hybrid_property.expression),
[hybrid_property.update_expression](#sqlalchemy.ext.hybrid.hybrid_property.update_expression), and
[hybrid_property.comparator](#sqlalchemy.ext.hybrid.hybrid_property.comparator) to allow typing tools to identify
`cls` as a class and not an instance in the method signature.

## Defining Setters

The [hybrid_property.setter()](#sqlalchemy.ext.hybrid.hybrid_property.setter) modifier allows the construction of a
custom setter method, that can modify values on the object:

```
class Interval(Base):
    # ...

    @hybrid_property
    def length(self) -> int:
        return self.end - self.start

    @length.inplace.setter
    def _length_setter(self, value: int) -> None:
        self.end = self.start + value
```

The `length(self, value)` method is now called upon set:

```
>>> i1 = Interval(5, 10)
>>> i1.length
5
>>> i1.length = 12
>>> i1.end
17
```

## Allowing Bulk ORM Update

A hybrid can define a custom “UPDATE” handler for when using
ORM-enabled updates, allowing the hybrid to be used in the
SET clause of the update.

Normally, when using a hybrid with [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update), the SQL
expression is used as the column that’s the target of the SET.  If our
`Interval` class had a hybrid `start_point` that linked to
`Interval.start`, this could be substituted directly:

```
from sqlalchemy import update

stmt = update(Interval).values({Interval.start_point: 10})
```

However, when using a composite hybrid like `Interval.length`, this
hybrid represents more than one column.   We can set up a handler that will
accommodate a value passed in the VALUES expression which can affect
this, using the [hybrid_property.update_expression()](#sqlalchemy.ext.hybrid.hybrid_property.update_expression) decorator.
A handler that works similarly to our setter would be:

```
from typing import List, Tuple, Any

class Interval(Base):
    # ...

    @hybrid_property
    def length(self) -> int:
        return self.end - self.start

    @length.inplace.setter
    def _length_setter(self, value: int) -> None:
        self.end = self.start + value

    @length.inplace.update_expression
    def _length_update_expression(
        cls, value: Any
    ) -> List[Tuple[Any, Any]]:
        return [(cls.end, cls.start + value)]
```

Above, if we use `Interval.length` in an UPDATE expression, we get
a hybrid SET expression:

```
>>> from sqlalchemy import update
>>> print(update(Interval).values({Interval.length: 25}))
UPDATE interval SET "end"=(interval.start + :start_1)
```

This SET expression is accommodated by the ORM automatically.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-expression-update-delete) - includes background on ORM-enabled
UPDATE statements

## Working with Relationships

There’s no essential difference when creating hybrids that work with
related objects as opposed to column-based data. The need for distinct
expressions tends to be greater.  The two variants we’ll illustrate
are the “join-dependent” hybrid, and the “correlated subquery” hybrid.

### Join-Dependent Relationship Hybrid

Consider the following declarative
mapping which relates a `User` to a `SavingsAccount`:

```
from __future__ import annotations

from decimal import Decimal
from typing import cast
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import SQLColumnExpression
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class SavingsAccount(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    balance: Mapped[Decimal] = mapped_column(Numeric(15, 5))

    owner: Mapped[User] = relationship(back_populates="accounts")

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    accounts: Mapped[List[SavingsAccount]] = relationship(
        back_populates="owner", lazy="selectin"
    )

    @hybrid_property
    def balance(self) -> Optional[Decimal]:
        if self.accounts:
            return self.accounts[0].balance
        else:
            return None

    @balance.inplace.setter
    def _balance_setter(self, value: Optional[Decimal]) -> None:
        assert value is not None

        if not self.accounts:
            account = SavingsAccount(owner=self)
        else:
            account = self.accounts[0]
        account.balance = value

    @balance.inplace.expression
    @classmethod
    def _balance_expression(cls) -> SQLColumnExpression[Optional[Decimal]]:
        return cast(
            "SQLColumnExpression[Optional[Decimal]]",
            SavingsAccount.balance,
        )
```

The above hybrid property `balance` works with the first
`SavingsAccount` entry in the list of accounts for this user.   The
in-Python getter/setter methods can treat `accounts` as a Python
list available on `self`.

Tip

The `User.balance` getter in the above example accesses the
`self.accounts` collection, which will normally be loaded via the
[selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload) loader strategy configured on the `User.balance` [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship). The default loader strategy when not otherwise
stated on [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload), which emits SQL on
demand. When using asyncio, on-demand loaders such as [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload) are
not supported, so care should be taken to ensure the `self.accounts`
collection is accessible to this hybrid accessor when using asyncio.

At the expression level, it’s expected that the `User` class will
be used in an appropriate context such that an appropriate join to
`SavingsAccount` will be present:

```
>>> from sqlalchemy import select
>>> print(
...     select(User, User.balance)
...     .join(User.accounts)
...     .filter(User.balance > 5000)
... )
SELECT "user".id AS user_id, "user".name AS user_name,
account.balance AS account_balance
FROM "user" JOIN account ON "user".id = account.user_id
WHERE account.balance > :balance_1
```

Note however, that while the instance level accessors need to worry
about whether `self.accounts` is even present, this issue expresses
itself differently at the SQL expression level, where we basically
would use an outer join:

```
>>> from sqlalchemy import select
>>> from sqlalchemy import or_
>>> print(
...     select(User, User.balance)
...     .outerjoin(User.accounts)
...     .filter(or_(User.balance < 5000, User.balance == None))
... )
SELECT "user".id AS user_id, "user".name AS user_name,
account.balance AS account_balance
FROM "user" LEFT OUTER JOIN account ON "user".id = account.user_id
WHERE account.balance <  :balance_1 OR account.balance IS NULL
```

### Correlated Subquery Relationship Hybrid

We can, of course, forego being dependent on the enclosing query’s usage
of joins in favor of the correlated subquery, which can portably be packed
into a single column expression. A correlated subquery is more portable, but
often performs more poorly at the SQL level. Using the same technique
illustrated at [Using column_property](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html#mapper-column-property-sql-expressions),
we can adjust our `SavingsAccount` example to aggregate the balances for
*all* accounts, and use a correlated subquery for the column expression:

```
from __future__ import annotations

from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Numeric
from sqlalchemy import select
from sqlalchemy import SQLColumnExpression
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class SavingsAccount(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    balance: Mapped[Decimal] = mapped_column(Numeric(15, 5))

    owner: Mapped[User] = relationship(back_populates="accounts")

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    accounts: Mapped[List[SavingsAccount]] = relationship(
        back_populates="owner", lazy="selectin"
    )

    @hybrid_property
    def balance(self) -> Decimal:
        return sum(
            (acc.balance for acc in self.accounts), start=Decimal("0")
        )

    @balance.inplace.expression
    @classmethod
    def _balance_expression(cls) -> SQLColumnExpression[Decimal]:
        return (
            select(func.sum(SavingsAccount.balance))
            .where(SavingsAccount.user_id == cls.id)
            .label("total_balance")
        )
```

The above recipe will give us the `balance` column which renders
a correlated SELECT:

```
>>> from sqlalchemy import select
>>> print(select(User).filter(User.balance > 400))
SELECT "user".id, "user".name
FROM "user"
WHERE (
    SELECT sum(account.balance) AS sum_1 FROM account
    WHERE account.user_id = "user".id
) > :param_1
```

## Building Custom Comparators

The hybrid property also includes a helper that allows construction of
custom comparators. A comparator object allows one to customize the
behavior of each SQLAlchemy expression operator individually.  They
are useful when creating custom types that have some highly
idiosyncratic behavior on the SQL side.

Note

The [hybrid_property.comparator()](#sqlalchemy.ext.hybrid.hybrid_property.comparator) decorator introduced
in this section **replaces** the use of the
[hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) decorator.
They cannot be used together.

The example class below allows case-insensitive comparisons on the attribute
named `word_insensitive`:

```
from __future__ import annotations

from typing import Any

from sqlalchemy import ColumnElement
from sqlalchemy import func
from sqlalchemy.ext.hybrid import Comparator
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class CaseInsensitiveComparator(Comparator[str]):
    def __eq__(self, other: Any) -> ColumnElement[bool]:  # type: ignore[override]  # noqa: E501
        return func.lower(self.__clause_element__()) == func.lower(other)

class SearchWord(Base):
    __tablename__ = "searchword"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]

    @hybrid_property
    def word_insensitive(self) -> str:
        return self.word.lower()

    @word_insensitive.inplace.comparator
    @classmethod
    def _word_insensitive_comparator(cls) -> CaseInsensitiveComparator:
        return CaseInsensitiveComparator(cls.word)
```

Above, SQL expressions against `word_insensitive` will apply the `LOWER()`
SQL function to both sides:

```
>>> from sqlalchemy import select
>>> print(select(SearchWord).filter_by(word_insensitive="Trucks"))
SELECT searchword.id, searchword.word
FROM searchword
WHERE lower(searchword.word) = lower(:lower_1)
```

The `CaseInsensitiveComparator` above implements part of the
[ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators) interface.   A “coercion” operation like
lowercasing can be applied to all comparison operations (i.e. `eq`,
`lt`, `gt`, etc.) using [Operators.operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators.operate):

```
class CaseInsensitiveComparator(Comparator):
    def operate(self, op, other, **kwargs):
        return op(
            func.lower(self.__clause_element__()),
            func.lower(other),
            **kwargs,
        )
```

## Reusing Hybrid Properties across Subclasses

A hybrid can be referred to from a superclass, to allow modifying
methods like [hybrid_property.getter()](#sqlalchemy.ext.hybrid.hybrid_property.getter), [hybrid_property.setter()](#sqlalchemy.ext.hybrid.hybrid_property.setter)
to be used to redefine those methods on a subclass.  This is similar to
how the standard Python `@property` object works:

```
class FirstNameOnly(Base):
    # ...

    first_name: Mapped[str]

    @hybrid_property
    def name(self) -> str:
        return self.first_name

    @name.inplace.setter
    def _name_setter(self, value: str) -> None:
        self.first_name = value

class FirstNameLastName(FirstNameOnly):
    # ...

    last_name: Mapped[str]

    # 'inplace' is not used here; calling getter creates a copy
    # of FirstNameOnly.name that is local to FirstNameLastName
    @FirstNameOnly.name.getter
    def name(self) -> str:
        return self.first_name + " " + self.last_name

    @name.inplace.setter
    def _name_setter(self, value: str) -> None:
        self.first_name, self.last_name = value.split(" ", 1)
```

Above, the `FirstNameLastName` class refers to the hybrid from
`FirstNameOnly.name` to repurpose its getter and setter for the subclass.

When overriding [hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) and
[hybrid_property.comparator()](#sqlalchemy.ext.hybrid.hybrid_property.comparator) alone as the first reference to the
superclass, these names conflict with the same-named accessors on the class-
level [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) object returned at the class level.  To
override these methods when referring directly to the parent class descriptor,
add the special qualifier [hybrid_property.overrides](#sqlalchemy.ext.hybrid.hybrid_property.overrides), which will de-
reference the instrumented attribute back to the hybrid object:

```
class FirstNameLastName(FirstNameOnly):
    # ...

    last_name: Mapped[str]

    @FirstNameOnly.name.overrides.expression
    @classmethod
    def name(cls):
        return func.concat(cls.first_name, " ", cls.last_name)
```

## Hybrid Value Objects

Note in our previous example, if we were to compare the `word_insensitive`
attribute of a `SearchWord` instance to a plain Python string, the plain
Python string would not be coerced to lower case - the
`CaseInsensitiveComparator` we built, being returned by
`@word_insensitive.comparator`, only applies to the SQL side.

A more comprehensive form of the custom comparator is to construct a *Hybrid
Value Object*. This technique applies the target value or expression to a value
object which is then returned by the accessor in all cases.   The value object
allows control of all operations upon the value as well as how compared values
are treated, both on the SQL expression side as well as the Python value side.
Replacing the previous `CaseInsensitiveComparator` class with a new
`CaseInsensitiveWord` class:

```
class CaseInsensitiveWord(Comparator):
    "Hybrid value representing a lower case representation of a word."

    def __init__(self, word):
        if isinstance(word, basestring):
            self.word = word.lower()
        elif isinstance(word, CaseInsensitiveWord):
            self.word = word.word
        else:
            self.word = func.lower(word)

    def operate(self, op, other, **kwargs):
        if not isinstance(other, CaseInsensitiveWord):
            other = CaseInsensitiveWord(other)
        return op(self.word, other.word, **kwargs)

    def __clause_element__(self):
        return self.word

    def __str__(self):
        return self.word

    key = "word"
    "Label to apply to Query tuple results"
```

Above, the `CaseInsensitiveWord` object represents `self.word`, which may
be a SQL function, or may be a Python native.   By overriding `operate()` and
`__clause_element__()` to work in terms of `self.word`, all comparison
operations will work against the “converted” form of `word`, whether it be
SQL side or Python side. Our `SearchWord` class can now deliver the
`CaseInsensitiveWord` object unconditionally from a single hybrid call:

```
class SearchWord(Base):
    __tablename__ = "searchword"
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]

    @hybrid_property
    def word_insensitive(self) -> CaseInsensitiveWord:
        return CaseInsensitiveWord(self.word)
```

The `word_insensitive` attribute now has case-insensitive comparison behavior
universally, including SQL expression vs. Python expression (note the Python
value is converted to lower case on the Python side here):

```
>>> print(select(SearchWord).filter_by(word_insensitive="Trucks"))
SELECT searchword.id AS searchword_id, searchword.word AS searchword_word
FROM searchword
WHERE lower(searchword.word) = :lower_1
```

SQL expression versus SQL expression:

```
>>> from sqlalchemy.orm import aliased
>>> sw1 = aliased(SearchWord)
>>> sw2 = aliased(SearchWord)
>>> print(
...     select(sw1.word_insensitive, sw2.word_insensitive).filter(
...         sw1.word_insensitive > sw2.word_insensitive
...     )
... )
SELECT lower(searchword_1.word) AS lower_1,
lower(searchword_2.word) AS lower_2
FROM searchword AS searchword_1, searchword AS searchword_2
WHERE lower(searchword_1.word) > lower(searchword_2.word)
```

Python only expression:

```
>>> ws1 = SearchWord(word="SomeWord")
>>> ws1.word_insensitive == "sOmEwOrD"
True
>>> ws1.word_insensitive == "XOmEwOrX"
False
>>> print(ws1.word_insensitive)
someword
```

The Hybrid Value pattern is very useful for any kind of value that may have
multiple representations, such as timestamps, time deltas, units of
measurement, currencies and encrypted passwords.

See also

[Hybrids and Value Agnostic Types](https://techspot.zzzeek.org/2011/10/21/hybrids-and-value-agnostic-types/)
- on the techspot.zzzeek.org blog

[Value Agnostic Types, Part II](https://techspot.zzzeek.org/2011/10/29/value-agnostic-types-part-ii/) -
on the techspot.zzzeek.org blog

## API Reference

| Object Name | Description |
| --- | --- |
| Comparator | A helper class that allows easy construction of customPropComparatorclasses for usage with hybrids. |
| hybrid_method | A decorator which allows definition of a Python object method with both
instance-level and class-level behavior. |
| hybrid_property | A decorator which allows definition of a Python descriptor with both
instance-level and class-level behavior. |
| HybridExtensionType |  |

   class sqlalchemy.ext.hybrid.hybrid_method

*inherits from* [sqlalchemy.orm.base.InspectionAttrInfo](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrInfo), `typing.Generic`

A decorator which allows definition of a Python object method with both
instance-level and class-level behavior.

| Member Name | Description |
| --- | --- |
| __init__() | Create a newhybrid_method. |
| expression() | Provide a modifying decorator that defines a
SQL-expression producing method. |
| extension_type | The extension type, if any.
Defaults toNotExtension.NOT_EXTENSION |
| is_attribute | True if this object is a Pythondescriptor. |

   method [sqlalchemy.ext.hybrid.hybrid_method.](#sqlalchemy.ext.hybrid.hybrid_method)__init__(*func:Callable[[Concatenate[Any,_P]],_R]*, *expr:Callable[[Concatenate[Any,_P]],SQLCoreOperations[_R]]|None=None*)

Create a new [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method).

Usage is typically via decorator:

```
from sqlalchemy.ext.hybrid import hybrid_method

class SomeClass:
    @hybrid_method
    def value(self, x, y):
        return self._value + x + y

    @value.expression
    @classmethod
    def value(cls, x, y):
        return func.some_function(cls._value, x, y)
```

     method [sqlalchemy.ext.hybrid.hybrid_method.](#sqlalchemy.ext.hybrid.hybrid_method)expression(*expr:Callable[[Concatenate[Any,_P]],SQLCoreOperations[_R]]*) → [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method)[_P, _R]

Provide a modifying decorator that defines a
SQL-expression producing method.

    attribute [sqlalchemy.ext.hybrid.hybrid_method.](#sqlalchemy.ext.hybrid.hybrid_method)extension_type: [InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType) = 'HYBRID_METHOD'

The extension type, if any.
Defaults to `NotExtension.NOT_EXTENSION`

See also

[HybridExtensionType](#sqlalchemy.ext.hybrid.HybridExtensionType)

[AssociationProxyExtensionType](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxyExtensionType)

     property inplace: Self

Return the inplace mutator for this [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method).

The [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method) class already performs “in place” mutation
when the [hybrid_method.expression()](#sqlalchemy.ext.hybrid.hybrid_method.expression) decorator is called,
so this attribute returns Self.

Added in version 2.0.4.

See also

[Using inplace to create pep-484 compliant hybrid properties](#hybrid-pep484-naming)

     attribute [sqlalchemy.ext.hybrid.hybrid_method.](#sqlalchemy.ext.hybrid.hybrid_method)is_attribute = True

True if this object is a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).

This can refer to one of many types.   Usually a
[QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) which handles attributes events on behalf
of a [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty).   But can also be an extension type
such as [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) or [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property).
The [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type) will refer to a constant
identifying the specific subtype.

See also

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

      class sqlalchemy.ext.hybrid.hybrid_property

*inherits from* [sqlalchemy.orm.base.InspectionAttrInfo](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrInfo), `sqlalchemy.orm.base.ORMDescriptor`

A decorator which allows definition of a Python descriptor with both
instance-level and class-level behavior.

| Member Name | Description |
| --- | --- |
| __init__() | Create a newhybrid_property. |
| comparator() | Provide a modifying decorator that defines a custom
comparator producing method. |
| deleter() | Provide a modifying decorator that defines a deletion method. |
| expression() | Provide a modifying decorator that defines a SQL-expression
producing method. |
| extension_type | The extension type, if any.
Defaults toNotExtension.NOT_EXTENSION |
| getter() | Provide a modifying decorator that defines a getter method. |
| is_attribute | True if this object is a Pythondescriptor. |
| setter() | Provide a modifying decorator that defines a setter method. |
| update_expression() | Provide a modifying decorator that defines an UPDATE tuple
producing method. |

   method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)__init__(*fget:_HybridGetterType[_T]*, *fset:_HybridSetterType[_T]|None=None*, *fdel:_HybridDeleterType[_T]|None=None*, *expr:_HybridExprCallableType[_T]|None=None*, *custom_comparator:Comparator[_T]|None=None*, *update_expr:_HybridUpdaterType[_T]|None=None*)

Create a new [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property).

Usage is typically via decorator:

```
from sqlalchemy.ext.hybrid import hybrid_property

class SomeClass:
    @hybrid_property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
```

     method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)comparator(*comparator:_HybridComparatorCallableType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines a custom
comparator producing method.

The return value of the decorated method should be an instance of
[Comparator](#sqlalchemy.ext.hybrid.Comparator).

Note

The [hybrid_property.comparator()](#sqlalchemy.ext.hybrid.hybrid_property.comparator) decorator
**replaces** the use of the [hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression)
decorator.  They cannot be used together.

When a hybrid is invoked at the class level, the
[Comparator](#sqlalchemy.ext.hybrid.Comparator) object given here is wrapped inside of a
specialized [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute), which is the same kind of
object used by the ORM to represent other mapped attributes.   The
reason for this is so that other class-level attributes such as
docstrings and a reference to the hybrid itself may be maintained
within the structure that’s returned, without any modifications to the
original comparator object passed in.

Note

When referring to a hybrid property  from an owning class (e.g.
`SomeClass.some_hybrid`), an instance of
[QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) is returned, representing the
expression or comparator object as this  hybrid object.  However,
that object itself has accessors called `expression` and
`comparator`; so when attempting to override these decorators on a
subclass, it may be necessary to qualify it using the
[hybrid_property.overrides](#sqlalchemy.ext.hybrid.hybrid_property.overrides) modifier first.  See that
modifier for details.

     method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)deleter(*fdel:_HybridDeleterType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines a deletion method.

    method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)expression(*expr:_HybridExprCallableType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines a SQL-expression
producing method.

When a hybrid is invoked at the class level, the SQL expression given
here is wrapped inside of a specialized [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute),
which is the same kind of object used by the ORM to represent other
mapped attributes.   The reason for this is so that other class-level
attributes such as docstrings and a reference to the hybrid itself may
be maintained within the structure that’s returned, without any
modifications to the original SQL expression passed in.

Note

When referring to a hybrid property  from an owning class (e.g.
`SomeClass.some_hybrid`), an instance of
[QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) is returned, representing the
expression or comparator object as well as this  hybrid object.
However, that object itself has accessors called `expression` and
`comparator`; so when attempting to override these decorators on a
subclass, it may be necessary to qualify it using the
[hybrid_property.overrides](#sqlalchemy.ext.hybrid.hybrid_property.overrides) modifier first.  See that
modifier for details.

See also

[Defining Expression Behavior Distinct from Attribute Behavior](#hybrid-distinct-expression)

     attribute [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)extension_type: [InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType) = 'HYBRID_PROPERTY'

The extension type, if any.
Defaults to `NotExtension.NOT_EXTENSION`

See also

[HybridExtensionType](#sqlalchemy.ext.hybrid.HybridExtensionType)

[AssociationProxyExtensionType](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxyExtensionType)

     method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)getter(*fget:_HybridGetterType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines a getter method.

Added in version 1.2.

     property inplace: _InPlace[_T]

Return the inplace mutator for this [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property).

This is to allow in-place mutation of the hybrid, allowing the first
hybrid method of a certain name to be reused in order to add
more methods without having to name those methods the same, e.g.:

```
class Interval(Base):
    # ...

    @hybrid_property
    def radius(self) -> float:
        return abs(self.length) / 2

    @radius.inplace.setter
    def _radius_setter(self, value: float) -> None:
        self.length = value * 2

    @radius.inplace.expression
    def _radius_expression(cls) -> ColumnElement[float]:
        return type_coerce(func.abs(cls.length) / 2, Float)
```

Added in version 2.0.4.

See also

[Using inplace to create pep-484 compliant hybrid properties](#hybrid-pep484-naming)

     attribute [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)is_attribute = True

True if this object is a Python [descriptor](https://docs.sqlalchemy.org/en/20/glossary.html#term-descriptor).

This can refer to one of many types.   Usually a
[QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute) which handles attributes events on behalf
of a [MapperProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty).   But can also be an extension type
such as [AssociationProxy](https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html#sqlalchemy.ext.associationproxy.AssociationProxy) or [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property).
The [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type) will refer to a constant
identifying the specific subtype.

See also

[Mapper.all_orm_descriptors](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.all_orm_descriptors)

     property overrides: Self

Prefix for a method that is overriding an existing attribute.

The [hybrid_property.overrides](#sqlalchemy.ext.hybrid.hybrid_property.overrides) accessor just returns
this hybrid object, which when called at the class level from
a parent class, will de-reference the “instrumented attribute”
normally returned at this level, and allow modifying decorators
like [hybrid_property.expression()](#sqlalchemy.ext.hybrid.hybrid_property.expression) and
[hybrid_property.comparator()](#sqlalchemy.ext.hybrid.hybrid_property.comparator)
to be used without conflicting with the same-named attributes
normally present on the [QueryableAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.QueryableAttribute):

```
class SuperClass:
    # ...

    @hybrid_property
    def foobar(self):
        return self._foobar

class SubClass(SuperClass):
    # ...

    @SuperClass.foobar.overrides.expression
    def foobar(cls):
        return func.subfoobar(self._foobar)
```

Added in version 1.2.

See also

[Reusing Hybrid Properties across Subclasses](#hybrid-reuse-subclass)

     method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)setter(*fset:_HybridSetterType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines a setter method.

    method [sqlalchemy.ext.hybrid.hybrid_property.](#sqlalchemy.ext.hybrid.hybrid_property)update_expression(*meth:_HybridUpdaterType[_T]*) → [hybrid_property](#sqlalchemy.ext.hybrid.hybrid_property)[_T]

Provide a modifying decorator that defines an UPDATE tuple
producing method.

The method accepts a single value, which is the value to be
rendered into the SET clause of an UPDATE statement.  The method
should then process this value into individual column expressions
that fit into the ultimate SET clause, and return them as a
sequence of 2-tuples.  Each tuple
contains a column expression as the key and a value to be rendered.

E.g.:

```
class Person(Base):
    # ...

    first_name = Column(String)
    last_name = Column(String)

    @hybrid_property
    def fullname(self):
        return first_name + " " + last_name

    @fullname.update_expression
    def fullname(cls, value):
        fname, lname = value.split(" ", 1)
        return [(cls.first_name, fname), (cls.last_name, lname)]
```

Added in version 1.2.

      class sqlalchemy.ext.hybrid.Comparator

*inherits from* [sqlalchemy.orm.PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)

A helper class that allows easy construction of custom
[PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator)
classes for usage with hybrids.

    class sqlalchemy.ext.hybrid.HybridExtensionType

*inherits from* [sqlalchemy.orm.base.InspectionAttrExtensionType](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttrExtensionType)

| Member Name | Description |
| --- | --- |
| HYBRID_METHOD | Symbol indicating anInspectionAttrthat’s
of typehybrid_method. |
| HYBRID_PROPERTY |  |

   attribute [sqlalchemy.ext.hybrid.HybridExtensionType.](#sqlalchemy.ext.hybrid.HybridExtensionType)HYBRID_METHOD = 'HYBRID_METHOD'

Symbol indicating an `InspectionAttr` that’s
of type [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method).

Is assigned to the [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type)
attribute.

See also

`Mapper.all_orm_attributes`

     attribute [sqlalchemy.ext.hybrid.HybridExtensionType.](#sqlalchemy.ext.hybrid.HybridExtensionType)HYBRID_PROPERTY = 'HYBRID_PROPERTY'  Symbol indicating an `InspectionAttr` that’s

of type [hybrid_method](#sqlalchemy.ext.hybrid.hybrid_method).

Is assigned to the [InspectionAttr.extension_type](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InspectionAttr.extension_type)
attribute.

See also

`Mapper.all_orm_attributes`

---

# SQLAlchemy 2.0 Documentation

# ORM Extensions

SQLAlchemy has a variety of ORM extensions available, which add additional
functionality to the core behavior.

The extensions build almost entirely on public core and ORM APIs and users should
be encouraged to read their source code to further their understanding of their
behavior.   In particular the “Horizontal Sharding”, “Hybrid Attributes”, and
“Mutation Tracking” extensions are very succinct.

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

---

# SQLAlchemy 2.0 Documentation

# Indexable

Define attributes on ORM-mapped classes that have “index” attributes for
columns with [Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable) types.

“index” means the attribute is associated with an element of an
[Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable) column with the predefined index to access it.
The [Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable) types include types such as
[ARRAY](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.ARRAY), [JSON](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON) and
[HSTORE](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.HSTORE).

The [indexable](#module-sqlalchemy.ext.indexable) extension provides
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)-like interface for any element of an
[Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable) typed column. In simple cases, it can be
treated as a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) - mapped attribute.

## Synopsis

Given `Person` as a model with a primary key and JSON data field.
While this field may have any number of elements encoded within it,
we would like to refer to the element called `name` individually
as a dedicated attribute which behaves like a standalone column:

```
from sqlalchemy import Column, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.indexable import index_property

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    name = index_property("data", "name")
```

Above, the `name` attribute now behaves like a mapped column.   We
can compose a new `Person` and set the value of `name`:

```
>>> person = Person(name="Alchemist")
```

The value is now accessible:

```
>>> person.name
'Alchemist'
```

Behind the scenes, the JSON field was initialized to a new blank dictionary
and the field was set:

```
>>> person.data
{'name': 'Alchemist'}
```

The field is mutable in place:

```
>>> person.name = "Renamed"
>>> person.name
'Renamed'
>>> person.data
{'name': 'Renamed'}
```

When using [index_property](#sqlalchemy.ext.indexable.index_property), the change that we make to the indexable
structure is also automatically tracked as history; we no longer need
to use [MutableDict](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html#sqlalchemy.ext.mutable.MutableDict) in order to track this change
for the unit of work.

Deletions work normally as well:

```
>>> del person.name
>>> person.data
{}
```

Above, deletion of `person.name` deletes the value from the dictionary,
but not the dictionary itself.

A missing key will produce `AttributeError`:

```
>>> person = Person()
>>> person.name
AttributeError: 'name'
```

Unless you set a default value:

```
>>> class Person(Base):
...     __tablename__ = "person"
...
...     id = Column(Integer, primary_key=True)
...     data = Column(JSON)
...
...     name = index_property("data", "name", default=None)  # See default

>>> person = Person()
>>> print(person.name)
None
```

The attributes are also accessible at the class level.
Below, we illustrate `Person.name` used to generate
an indexed SQL criteria:

```
>>> from sqlalchemy.orm import Session
>>> session = Session()
>>> query = session.query(Person).filter(Person.name == "Alchemist")
```

The above query is equivalent to:

```
>>> query = session.query(Person).filter(Person.data["name"] == "Alchemist")
```

Multiple [index_property](#sqlalchemy.ext.indexable.index_property) objects can be chained to produce
multiple levels of indexing:

```
from sqlalchemy import Column, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.indexable import index_property

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    birthday = index_property("data", "birthday")
    year = index_property("birthday", "year")
    month = index_property("birthday", "month")
    day = index_property("birthday", "day")
```

Above, a query such as:

```
q = session.query(Person).filter(Person.year == "1980")
```

On a PostgreSQL backend, the above query will render as:

```
SELECT person.id, person.data
FROM person
WHERE person.data -> %(data_1)s -> %(param_1)s = %(param_2)s
```

## Default Values

[index_property](#sqlalchemy.ext.indexable.index_property) includes special behaviors for when the indexed
data structure does not exist, and a set operation is called:

- For an [index_property](#sqlalchemy.ext.indexable.index_property) that is given an integer index value,
  the default data structure will be a Python list of `None` values,
  at least as long as the index value; the value is then set at its
  place in the list.  This means for an index value of zero, the list
  will be initialized to `[None]` before setting the given value,
  and for an index value of five, the list will be initialized to
  `[None, None, None, None, None]` before setting the fifth element
  to the given value.   Note that an existing list is **not** extended
  in place to receive a value.
- for an [index_property](#sqlalchemy.ext.indexable.index_property) that is given any other kind of index
  value (e.g. strings usually), a Python dictionary is used as the
  default data structure.
- The default data structure can be set to any Python callable using the
  [index_property.datatype](#sqlalchemy.ext.indexable.index_property.params.datatype) parameter, overriding the previous
  rules.

## Subclassing

[index_property](#sqlalchemy.ext.indexable.index_property) can be subclassed, in particular for the common
use case of providing coercion of values or SQL expressions as they are
accessed.  Below is a common recipe for use with a PostgreSQL JSON type,
where we want to also include automatic casting plus `astext()`:

```
class pg_json_property(index_property):
    def __init__(self, attr_name, index, cast_type):
        super(pg_json_property, self).__init__(attr_name, index)
        self.cast_type = cast_type

    def expr(self, model):
        expr = super(pg_json_property, self).expr(model)
        return expr.astext.cast(self.cast_type)
```

The above subclass can be used with the PostgreSQL-specific
version of [JSON](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON):

```
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    age = pg_json_property("data", "age", Integer)
```

The `age` attribute at the instance level works as before; however
when rendering SQL, PostgreSQL’s `->>` operator will be used
for indexed access, instead of the usual index operator of `->`:

```
>>> query = session.query(Person).filter(Person.age < 20)
```

The above query will render:

```
SELECT person.id, person.data
FROM person
WHERE CAST(person.data ->> %(data_1)s AS INTEGER) < %(param_1)s
```

## API Reference

| Object Name | Description |
| --- | --- |
| index_property | A property generator. The generated property describes an object
attribute that corresponds to anIndexablecolumn. |

   class sqlalchemy.ext.indexable.index_property

*inherits from* [sqlalchemy.ext.hybrid.hybrid_property](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#sqlalchemy.ext.hybrid.hybrid_property)

A property generator. The generated property describes an object
attribute that corresponds to an [Indexable](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.Indexable)
column.

See also

[sqlalchemy.ext.indexable](#module-sqlalchemy.ext.indexable)

| Member Name | Description |
| --- | --- |
| __init__() | Create a newindex_property. |

   method [sqlalchemy.ext.indexable.index_property.](#sqlalchemy.ext.indexable.index_property)__init__(*attr_name:str*, *index:int|str*, *default:_T=<objectobject>*, *datatype:Callable[[]*, *~typing.Any]|None=None*, *mutable:bool=True*, *onebased:bool=True*)

Create a new [index_property](#sqlalchemy.ext.indexable.index_property).

  Parameters:

- **attr_name** – An attribute name of an Indexable typed column, or other
  attribute that returns an indexable structure.
- **index** – The index to be used for getting and setting this value.  This
  should be the Python-side index value for integers.
- **default** – A value which will be returned instead of AttributeError
  when there is not a value at given index.
- **datatype** – default datatype to use when the field is empty.
  By default, this is derived from the type of index used; a
  Python list for an integer index, or a Python dictionary for
  any other style of index.   For a list, the list will be
  initialized to a list of None values that is at least
  `index` elements long.
- **mutable** – if False, writes and deletes to the attribute will
  be disallowed.
- **onebased** – assume the SQL representation of this value is
  one-based; that is, the first index in SQL is 1, not zero.
