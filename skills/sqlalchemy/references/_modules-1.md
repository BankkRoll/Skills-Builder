# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Source code for examples.adjacency_list.adjacency_list

```
from __future__ import annotations

from typing import Dict
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_keyed_dict

class Base(DeclarativeBase):
    pass

class TreeNode(MappedAsDataclass, Base):
    __tablename__ = "tree"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tree.id"), init=False
    )
    name: Mapped[str]

    children: Mapped[Dict[str, TreeNode]] = relationship(
        cascade="all, delete-orphan",
        back_populates="parent",
        collection_class=attribute_keyed_dict("name"),
        init=False,
        repr=False,
    )

    parent: Mapped[Optional[TreeNode]] = relationship(
        back_populates="children", remote_side=id, default=None
    )

    def dump(self, _indent: int = 0) -> str:
        return (
            "   " * _indent
            + repr(self)
            + "\n"
            + "".join([c.dump(_indent + 1) for c in self.children.values()])
        )

if __name__ == "__main__":
    engine = create_engine("sqlite://", echo=True)

    print("Creating Tree Table:")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        node = TreeNode("rootnode")
        TreeNode("node1", parent=node)
        TreeNode("node3", parent=node)

        node2 = TreeNode("node2")
        TreeNode("subnode1", parent=node2)
        node.children["node2"] = node2
        TreeNode("subnode2", parent=node.children["node2"])

        print(f"Created new tree structure:\n{node.dump()}")

        print("flush + commit:")

        session.add(node)
        session.commit()

        print(f"Tree after save:\n{node.dump()}")

        session.add_all(
            [
                TreeNode("node4", parent=node),
                TreeNode("subnode3", parent=node.children["node4"]),
                TreeNode("subnode4", parent=node.children["node4"]),
                TreeNode(
                    "subsubnode1",
                    parent=node.children["node4"].children["subnode3"],
                ),
            ]
        )

        # remove node1 from the parent, which will trigger a delete
        # via the delete-orphan cascade.
        del node.children["node1"]

        print("Removed node1.  flush + commit:")
        session.commit()

        print("Tree after save, will unexpire all nodes:\n")
        print(f"{node.dump()}")

    with Session(engine) as session:
        print(
            "Perform a full select of the root node, eagerly loading "
            "up to a depth of four"
        )
        node = session.scalars(
            select(TreeNode)
            .options(selectinload(TreeNode.children, recursion_depth=4))
            .filter(TreeNode.name == "rootnode")
        ).one()

        print(f"Full Tree:\n{node.dump()}")

        print("Marking root node as deleted, flush + commit:")

        session.delete(node)
        session.commit()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.association.basic_association

```
"""Illustrate a many-to-many relationship between an
"Order" and a collection of "Item" objects, associating a purchase price
with each via an association object called "OrderItem"

The association object pattern is a form of many-to-many which
associates additional data with each association between parent/child.

The example illustrates an "order", referencing a collection
of "items", with a particular price paid associated with each "item".

"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(30))
    order_date: Mapped[datetime] = mapped_column(default=datetime.now())
    order_items: Mapped[list[OrderItem]] = relationship(
        cascade="all, delete-orphan", backref="order"
    )

    def __init__(self, customer_name: str) -> None:
        self.customer_name = customer_name

class Item(Base):
    __tablename__ = "item"
    item_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(30))
    price: Mapped[float]

    def __init__(self, description: str, price: float) -> None:
        self.description = description
        self.price = price

    def __repr__(self) -> str:
        return "Item({!r}, {!r})".format(self.description, self.price)

class OrderItem(Base):
    __tablename__ = "orderitem"
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.order_id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.item_id"), primary_key=True
    )
    price: Mapped[float]

    def __init__(self, item: Item, price: float | None = None) -> None:
        self.item = item
        self.price = price or item.price

    item: Mapped[Item] = relationship(lazy="joined")

if __name__ == "__main__":
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        # create catalog
        tshirt, mug, hat, crowbar = (
            Item("SA T-Shirt", 10.99),
            Item("SA Mug", 6.50),
            Item("SA Hat", 8.99),
            Item("MySQL Crowbar", 16.99),
        )
        session.add_all([tshirt, mug, hat, crowbar])
        session.commit()

        # create an order
        order = Order("john smith")

        # add three OrderItem associations to the Order and save
        order.order_items.append(OrderItem(mug))
        order.order_items.append(OrderItem(crowbar, 10.99))
        order.order_items.append(OrderItem(hat))
        session.add(order)
        session.commit()

        # query the order, print items
        order = session.scalars(
            select(Order).filter_by(customer_name="john smith")
        ).one()
        print(
            [
                (order_item.item.description, order_item.price)
                for order_item in order.order_items
            ]
        )

        # print customers who bought 'MySQL Crowbar' on sale
        q = (
            select(Order)
            .join(OrderItem)
            .join(Item)
            .where(
                Item.description == "MySQL Crowbar",
                Item.price > OrderItem.price,
            )
        )

        print([order.customer_name for order in session.scalars(q)])
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.association.dict_of_sets_with_default

```
"""An advanced association proxy example which
illustrates nesting of association proxies to produce multi-level Python
collections, in this case a dictionary with string keys and sets of integers
as values, which conceal the underlying mapped classes.

This is a three table model which represents a parent table referencing a
dictionary of string keys and sets as values, where each set stores a
collection of integers. The association proxy extension is used to hide the
details of this persistence. The dictionary also generates new collections
upon access of a non-existent key, in the same manner as Python's
"collections.defaultdict" object.

"""

from __future__ import annotations

import operator
from typing import Mapping

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import KeyFuncDict

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

class GenDefaultCollection(KeyFuncDict[str, "B"]):
    def __missing__(self, key: str) -> B:
        self[key] = b = B(key)
        return b

class A(Base):
    __tablename__ = "a"
    associations: Mapped[Mapping[str, B]] = relationship(
        "B",
        collection_class=lambda: GenDefaultCollection(
            operator.attrgetter("key")
        ),
    )

    collections: AssociationProxy[dict[str, set[int]]] = association_proxy(
        "associations", "values"
    )
    """Bridge the association from 'associations' over to the 'values'
    association proxy of B.
    """

class B(Base):
    __tablename__ = "b"
    a_id: Mapped[int] = mapped_column(ForeignKey("a.id"))
    elements: Mapped[set[C]] = relationship("C", collection_class=set)
    key: Mapped[str]

    values: AssociationProxy[set[int]] = association_proxy("elements", "value")
    """Bridge the association from 'elements' over to the
    'value' element of C."""

    def __init__(self, key: str, values: set[int] | None = None) -> None:
        self.key = key
        if values:
            self.values = values

class C(Base):
    __tablename__ = "c"
    b_id: Mapped[int] = mapped_column(ForeignKey("b.id"))
    value: Mapped[int]

    def __init__(self, value: int) -> None:
        self.value = value

if __name__ == "__main__":
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    session = Session(engine)

    # only "A" is referenced explicitly.  Using "collections",
    # we deal with a dict of key/sets of integers directly.

    session.add_all([A(collections={"1": {1, 2, 3}})])
    session.commit()

    a1 = session.scalars(select(A)).one()
    print(a1.collections["1"])
    a1.collections["1"].add(4)
    session.commit()

    a1.collections["2"].update([7, 8, 9])
    session.commit()

    print(a1.collections["2"])
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.association.proxied_association

```
"""Same example as basic_association, adding in
usage of :mod:`sqlalchemy.ext.associationproxy` to make explicit references
to ``OrderItem`` optional.

"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(30))
    order_date: Mapped[datetime] = mapped_column(default=datetime.now())
    order_items: Mapped[list[OrderItem]] = relationship(
        cascade="all, delete-orphan", backref="order"
    )
    items: AssociationProxy[list[Item]] = association_proxy(
        "order_items", "item"
    )

    def __init__(self, customer_name: str) -> None:
        self.customer_name = customer_name

class Item(Base):
    __tablename__ = "item"
    item_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(30))
    price: Mapped[float]

    def __init__(self, description: str, price: float) -> None:
        self.description = description
        self.price = price

    def __repr__(self) -> str:
        return "Item({!r}, {!r})".format(self.description, self.price)

class OrderItem(Base):
    __tablename__ = "orderitem"
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.order_id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.item_id"), primary_key=True
    )
    price: Mapped[float]

    item: Mapped[Item] = relationship(lazy="joined")

    def __init__(self, item: Item, price: float | None = None):
        self.item = item
        self.price = price or item.price

if __name__ == "__main__":
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        # create catalog
        tshirt, mug, hat, crowbar = (
            Item("SA T-Shirt", 10.99),
            Item("SA Mug", 6.50),
            Item("SA Hat", 8.99),
            Item("MySQL Crowbar", 16.99),
        )
        session.add_all([tshirt, mug, hat, crowbar])
        session.commit()

        # create an order
        order = Order("john smith")

        # add items via the association proxy.
        # the OrderItem is created automatically.
        order.items.append(mug)
        order.items.append(hat)

        # add an OrderItem explicitly.
        order.order_items.append(OrderItem(crowbar, 10.99))

        session.add(order)
        session.commit()

        # query the order, print items
        order = session.scalars(
            select(Order).filter_by(customer_name="john smith")
        ).one()

        # print items based on the OrderItem collection directly
        print(
            [
                (assoc.item.description, assoc.price, assoc.item.price)
                for assoc in order.order_items
            ]
        )

        # print items based on the "proxied" items collection
        print([(item.description, item.price) for item in order.items])

        # print customers who bought 'MySQL Crowbar' on sale
        orders_stmt = (
            select(Order)
            .join(OrderItem)
            .join(Item)
            .filter(Item.description == "MySQL Crowbar")
            .filter(Item.price > OrderItem.price)
        )
        print([o.customer_name for o in session.scalars(orders_stmt)])
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.asyncio.async_orm

```
"""Illustrates use of the ``sqlalchemy.ext.asyncio.AsyncSession`` object
for asynchronous ORM use.

"""

from __future__ import annotations

import asyncio
import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

class Base(AsyncAttrs, DeclarativeBase):
    pass

class A(Base):
    __tablename__ = "a"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Optional[str]]
    create_date: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    bs: Mapped[List[B]] = relationship()

class B(Base):
    __tablename__ = "b"
    id: Mapped[int] = mapped_column(primary_key=True)
    a_id: Mapped[int] = mapped_column(ForeignKey("a.id"))
    data: Mapped[Optional[str]]

async def async_main():
    """Main program function."""

    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        # for relationship loading, eager loading should be applied.
        stmt = select(A).options(selectinload(A.bs))

        # AsyncSession.execute() is used for 2.0 style ORM execution
        # (same as the synchronous API).
        result = await session.scalars(stmt)

        # result is a buffered Result object.
        for a1 in result:
            print(a1)
            print(f"created at: {a1.create_date}")
            for b1 in a1.bs:
                print(b1)

        # for streaming ORM results, AsyncSession.stream() may be used.
        result = await session.stream(stmt)

        # result is a streaming AsyncResult object.
        async for a1 in result.scalars():
            print(a1)
            for b1 in a1.bs:
                print(b1)

        result = await session.scalars(select(A).order_by(A.id))

        a1 = result.first()

        a1.data = "new data"

        await session.commit()

        # use the AsyncAttrs interface to accommodate for a lazy load
        for b1 in await a1.awaitable_attrs.bs:
            print(b1)

asyncio.run(async_main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.asyncio.async_orm_writeonly

```
"""Illustrates using **write only relationships** for simpler handling
of ORM collections under asyncio.

"""

from __future__ import annotations

import asyncio
import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import WriteOnlyMapped

class Base(AsyncAttrs, DeclarativeBase):
    pass

class A(Base):
    __tablename__ = "a"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Optional[str]]
    create_date: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    # collection relationships are declared with WriteOnlyMapped.  There
    # is no separate collection type
    bs: WriteOnlyMapped[B] = relationship()

class B(Base):
    __tablename__ = "b"
    id: Mapped[int] = mapped_column(primary_key=True)
    a_id: Mapped[int] = mapped_column(ForeignKey("a.id"))
    data: Mapped[Optional[str]]

async def async_main():
    """Main program function."""

    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            # WriteOnlyMapped may be populated using any iterable,
            # e.g. lists, sets, etc.
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        stmt = select(A)

        result = await session.scalars(stmt)

        for a1 in result:
            print(a1)
            print(f"created at: {a1.create_date}")

            # to iterate a collection, emit a SELECT statement
            for b1 in await session.scalars(a1.bs.select()):
                print(b1)

        result = await session.stream(stmt)

        async for a1 in result.scalars():
            print(a1)

            # similar using "streaming" (server side cursors)
            async for b1 in (await session.stream(a1.bs.select())).scalars():
                print(b1)

        await session.commit()
        result = await session.scalars(select(A).order_by(A.id))

        a1 = result.first()

        a1.data = "new data"

asyncio.run(async_main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.asyncio.basic

```
"""Illustrates the asyncio engine / connection interface.

In this example, we have an async engine created by
:func:`_engine.create_async_engine`.   We then use it using await
within a coroutine.

"""

import asyncio

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine

meta = MetaData()

t1 = Table(
    "t1", meta, Column("id", Integer, primary_key=True), Column("name", String)
)

async def async_main():
    # engine is an instance of AsyncEngine
    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )

    # conn is an instance of AsyncConnection
    async with engine.begin() as conn:
        # to support SQLAlchemy DDL methods as well as legacy functions, the
        # AsyncConnection.run_sync() awaitable method will pass a "sync"
        # version of the AsyncConnection object to any synchronous method,
        # where synchronous IO calls will be transparently translated for
        # await.
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        # for normal statement execution, a traditional "await execute()"
        # pattern is used.
        await conn.execute(
            t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
        )

    async with engine.connect() as conn:
        # the default result object is the
        # sqlalchemy.engine.Result object
        result = await conn.execute(t1.select())

        # the results are buffered so no await call is necessary
        # for this case.
        print(result.fetchall())

        # for a streaming result that buffers only segments of the
        # result at time, the AsyncConnection.stream() method is used.
        # this returns a sqlalchemy.ext.asyncio.AsyncResult object.
        async_result = await conn.stream(t1.select())

        # this object supports async iteration and awaitable
        # versions of methods like .all(), fetchmany(), etc.
        async for row in async_result:
            print(row)

asyncio.run(async_main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.asyncio.gather_orm_statements

```
"""
Illustrates how to run many statements concurrently using ``asyncio.gather()``
along many asyncio database connections, merging ORM results into a single
``AsyncSession``.

Note that this pattern loses all transactional safety and is also not
necessarily any more performant than using a single Session, as it adds
significant CPU-bound work both to maintain more database connections
and sessions, as well as within the merging of results from external sessions
into one.

Python is a CPU-intensive language even in trivial cases, so it is strongly
recommended that any workarounds for "speed" such as the one below are
carefully vetted to show that they do in fact improve performance vs a
traditional approach.

"""

import asyncio
import random

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import merge_frozen_result

class Base(DeclarativeBase):
    pass

class A(Base):
    __tablename__ = "a"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str]

    def __repr__(self):
        id_, data = self.id, self.data
        return f"A({id_=}, {data=})"

async def run_out_of_band(async_sessionmaker, statement, merge_results=True):
    """run an ORM statement in a distinct session,
    returning the frozen results
    """

    async with async_sessionmaker() as oob_session:
        # use AUTOCOMMIT for each connection to reduce transaction
        # overhead / contention
        await oob_session.connection(
            execution_options={"isolation_level": "AUTOCOMMIT"}
        )

        result = await oob_session.execute(statement)

        if merge_results:
            return result.freeze()
        else:
            await result.close()

async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session, session.begin():
        session.add_all([A(data="a_%d" % i) for i in range(100)])

    statements = [
        select(A).where(A.data == "a_%d" % random.choice(range(100)))
        for i in range(30)
    ]

    frozen_results = await asyncio.gather(
        *(
            run_out_of_band(async_session, statement)
            for statement in statements
        )
    )
    results = [
        # merge_results means the ORM objects from the result
        # will be merged back into the original session.
        # load=False means we can use the objects directly without
        # re-selecting them.  however this merge operation is still
        # more expensive CPU-wise than a regular ORM load because the
        # objects are copied into new instances
        (
            await session.run_sync(
                merge_frozen_result, statement, result, load=False
            )
        )()
        for statement, result in zip(statements, frozen_results)
    ]

    print(f"results: {[r.all() for r in results]}")

asyncio.run(async_main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.asyncio.greenlet_orm

```
"""Illustrates use of the sqlalchemy.ext.asyncio.AsyncSession object
for asynchronous ORM use, including the optional run_sync() method.

"""

import asyncio

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass

class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    bs = relationship("B")

class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
    data = Column(String)

def run_queries(session):
    """A function written in "synchronous" style that will be invoked
    within the asyncio event loop.

    The session object passed is a traditional orm.Session object with
    synchronous interface.

    """

    stmt = select(A)

    result = session.execute(stmt)

    for a1 in result.scalars():
        print(a1)
        # lazy loads
        for b1 in a1.bs:
            print(b1)

    result = session.execute(select(A).order_by(A.id))

    a1 = result.scalars().first()

    a1.data = "new data"

async def async_main():
    """Main program function."""

    engine = create_async_engine(
        "postgresql+asyncpg://scott:tiger@localhost/test",
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        # we have the option to run a function written in sync style
        # within the AsyncSession.run_sync() method.  The function will
        # be passed a synchronous-style Session object and the function
        # can use traditional ORM patterns.
        await session.run_sync(run_queries)

        await session.commit()

asyncio.run(async_main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.custom_attributes.active_column_defaults

```
"""Illustrates use of the :meth:`.AttributeEvents.init_scalar`
event, in conjunction with Core column defaults to provide
ORM objects that automatically produce the default value
when an un-set attribute is accessed.

"""

import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import event
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

def configure_listener(mapper, class_):
    """Establish attribute setters for every default-holding column on the
    given mapper."""

    # iterate through ColumnProperty objects
    for col_attr in mapper.column_attrs:
        # look at the Column mapped by the ColumnProperty
        # (we look at the first column in the less common case
        # of a property mapped to multiple columns at once)
        column = col_attr.columns[0]

        # if the Column has a "default", set up a listener
        if column.default is not None:
            default_listener(col_attr, column.default)

def default_listener(col_attr, default):
    """Establish a default-setting listener.

    Given a class attribute and a :class:`.DefaultGenerator` instance.
    The default generator should be a :class:`.ColumnDefault` object with a
    plain Python value or callable default; otherwise, the appropriate behavior
    for SQL functions and defaults should be determined here by the
    user integrating this feature.

    """

    @event.listens_for(col_attr, "init_scalar", retval=True, propagate=True)
    def init_scalar(target, value, dict_):
        if default.is_callable:
            # the callable of ColumnDefault always accepts a context
            # argument; we can pass it as None here.
            value = default.arg(None)
        elif default.is_scalar:
            value = default.arg
        else:
            # default is a Sequence, a SQL expression, server
            # side default generator, or other non-Python-evaluable
            # object.  The feature here can't easily support this.   This
            # can be made to return None, rather than raising,
            # or can procure a connection from an Engine
            # or Session and actually run the SQL, if desired.
            raise NotImplementedError(
                "Can't invoke pre-default for a SQL-level column default"
            )

        # set the value in the given dict_; this won't emit any further
        # attribute set events or create attribute "history", but the value
        # will be used in the INSERT statement
        dict_[col_attr.key] = value

        # return the value as well
        return value

if __name__ == "__main__":
    Base = declarative_base()

    event.listen(Base, "mapper_configured", configure_listener, propagate=True)

    class Widget(Base):
        __tablename__ = "widget"

        id = Column(Integer, primary_key=True)

        radius = Column(Integer, default=30)
        timestamp = Column(DateTime, default=datetime.datetime.now)

    e = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(e)

    w1 = Widget()

    # not persisted at all, default values are present the moment
    # we access them
    assert w1.radius == 30

    # this line will invoke the datetime.now() function, and establish
    # its return value upon the w1 instance, such that the
    # Column-level default for the "timestamp" column will no longer fire
    # off.
    current_time = w1.timestamp
    assert current_time > datetime.datetime.now() - datetime.timedelta(
        seconds=5
    )

    # persist
    sess = Session(e)
    sess.add(w1)
    sess.commit()

    # data is persisted.  The timestamp is also the one we generated above;
    # e.g. the default wasn't re-invoked later.
    assert sess.query(Widget.radius, Widget.timestamp).first() == (
        30,
        current_time,
    )
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.custom_attributes.custom_management

```
"""Illustrates customized class instrumentation, using
the :mod:`sqlalchemy.ext.instrumentation` extension package.

In this example, mapped classes are modified to
store their state in a dictionary attached to an attribute
named "_goofy_dict", instead of using __dict__.
this example illustrates how to replace SQLAlchemy's class
descriptors with a user-defined system.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.ext.instrumentation import InstrumentationManager
from sqlalchemy.orm import registry as _reg
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import del_attribute
from sqlalchemy.orm.attributes import get_attribute
from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy.orm.instrumentation import is_instrumented

registry = _reg()

class MyClassState(InstrumentationManager):
    def get_instance_dict(self, class_, instance):
        return instance._goofy_dict

    def initialize_instance_dict(self, class_, instance):
        instance.__dict__["_goofy_dict"] = {}

    def install_state(self, class_, instance, state):
        instance.__dict__["_goofy_dict"]["state"] = state

    def state_getter(self, class_):
        def find(instance):
            return instance.__dict__["_goofy_dict"]["state"]

        return find

class MyClass:
    __sa_instrumentation_manager__ = MyClassState

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __getattr__(self, key):
        if is_instrumented(self, key):
            return get_attribute(self, key)
        else:
            try:
                return self._goofy_dict[key]
            except KeyError:
                raise AttributeError(key)

    def __setattr__(self, key, value):
        if is_instrumented(self, key):
            set_attribute(self, key, value)
        else:
            self._goofy_dict[key] = value

    def __delattr__(self, key):
        if is_instrumented(self, key):
            del_attribute(self, key)
        else:
            del self._goofy_dict[key]

if __name__ == "__main__":
    engine = create_engine("sqlite://")
    meta = MetaData()

    table1 = Table(
        "table1",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", Text),
    )
    table2 = Table(
        "table2",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", Text),
        Column("t1id", Integer, ForeignKey("table1.id")),
    )
    meta.create_all(engine)

    class A(MyClass):
        pass

    class B(MyClass):
        pass

    registry.map_imperatively(A, table1, properties={"bs": relationship(B)})

    registry.map_imperatively(B, table2)

    a1 = A(name="a1", bs=[B(name="b1"), B(name="b2")])

    assert a1.name == "a1"
    assert a1.bs[0].name == "b1"

    sess = Session(engine)
    sess.add(a1)

    sess.commit()

    a1 = sess.query(A).get(a1.id)

    assert a1.name == "a1"
    assert a1.bs[0].name == "b1"

    a1.bs.remove(a1.bs[0])

    sess.commit()

    a1 = sess.query(A).get(a1.id)
    assert len(a1.bs) == 1
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.custom_attributes.listen_for_events

```
"""Illustrates how to attach events to all instrumented attributes
and listen for change events.

"""

from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

def configure_listener(class_, key, inst):
    def append(instance, value, initiator):
        instance.receive_change_event("append", key, value, None)

    def remove(instance, value, initiator):
        instance.receive_change_event("remove", key, value, None)

    def set_(instance, value, oldvalue, initiator):
        instance.receive_change_event("set", key, value, oldvalue)

    event.listen(inst, "append", append)
    event.listen(inst, "remove", remove)
    event.listen(inst, "set", set_)

if __name__ == "__main__":

    class Base:
        def receive_change_event(self, verb, key, value, oldvalue):
            s = "Value '%s' %s on attribute '%s', " % (value, verb, key)
            if oldvalue:
                s += "which replaced the value '%s', " % oldvalue
            s += "on object %s" % self
            print(s)

    Base = declarative_base(cls=Base)

    event.listen(Base, "attribute_instrument", configure_listener)

    class MyMappedClass(Base):
        __tablename__ = "mytable"

        id = Column(Integer, primary_key=True)
        data = Column(String(50))
        related_id = Column(Integer, ForeignKey("related.id"))
        related = relationship("Related", backref="mapped")

        def __str__(self):
            return "MyMappedClass(data=%r)" % self.data

    class Related(Base):
        __tablename__ = "related"

        id = Column(Integer, primary_key=True)
        data = Column(String(50))

        def __str__(self):
            return "Related(data=%r)" % self.data

    # classes are instrumented.  Demonstrate the events !

    m1 = MyMappedClass(data="m1", related=Related(data="r1"))
    m1.data = "m1mod"
    m1.related.mapped.append(MyMappedClass(data="m2"))
    del m1.data
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.advanced

```
"""Illustrate usage of Query combined with the FromCache option,
including front-end loading, cache invalidation and collection caching.

"""

from sqlalchemy import select
from .caching_query import FromCache
from .caching_query import RelationshipCache
from .environment import cache
from .environment import Session
from .model import cache_address_bits
from .model import Person

def load_name_range(start, end, invalidate=False):
    """Load Person objects on a range of names.

    start/end are integers, range is then
    "person <start>" - "person <end>".

    The cache option we set up is called "name_range", indicating
    a range of names for the Person class.

    The `Person.addresses` collections are also cached.  Its basically
    another level of tuning here, as that particular cache option
    can be transparently replaced with joinedload(Person.addresses).
    The effect is that each Person and their Address collection
    is cached either together or separately, affecting the kind of
    SQL that emits for unloaded Person objects as well as the distribution
    of data within the cache.
    """
    q = (
        select(Person)
        .filter(
            Person.name.between("person %.2d" % start, "person %.2d" % end)
        )
        .options(cache_address_bits)
        .options(FromCache("default", "name_range"))
    )

    # have the "addresses" collection cached separately
    # each lazyload of Person.addresses loads from cache.
    q = q.options(RelationshipCache(Person.addresses, "default"))

    # alternatively, eagerly load the "addresses" collection, so that they'd
    # be cached together.   This issues a bigger SQL statement and caches
    # a single, larger value in the cache per person rather than two
    # separate ones.
    # q = q.options(joinedload(Person.addresses))

    # if requested, invalidate the cache on current criterion.
    if invalidate:
        cache.invalidate(q, {}, FromCache("default", "name_range"))
        cache.invalidate(q, {}, RelationshipCache(Person.addresses, "default"))

    return Session.scalars(q).all()

print("two through twelve, possibly from cache:\n")
print(", ".join([p.name for p in load_name_range(2, 12)]))

print("\ntwenty five through forty, possibly from cache:\n")
print(", ".join([p.name for p in load_name_range(25, 40)]))

# loading them again, no SQL is emitted
print("\ntwo through twelve, from the cache:\n")
print(", ".join([p.name for p in load_name_range(2, 12)]))

# but with invalidate, they are
print("\ntwenty five through forty, invalidate first:\n")
print(", ".join([p.name for p in load_name_range(25, 40, True)]))

# illustrate the address loading from either cache/already
# on the Person
print(
    "\n\nPeople plus addresses, two through twelve, addresses "
    "possibly from cache"
)
for p in load_name_range(2, 12):
    print(p.format_full())

# illustrate the address loading from either cache/already
# on the Person
print("\n\nPeople plus addresses, two through twelve, addresses from cache")
for p in load_name_range(2, 12):
    print(p.format_full())

print(
    "\n\nIf this was the first run of advanced.py, try "
    "a second run.  Only one SQL statement will be emitted."
)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.caching_query

```
"""Represent functions and classes
which allow the usage of Dogpile caching with SQLAlchemy.
Introduces a query option called FromCache.

.. versionchanged:: 1.4  the caching approach has been altered to work
   based on a session event.

The three new concepts introduced here are:

 * ORMCache - an extension for an ORM :class:`.Session`
   retrieves results in/from dogpile.cache.
 * FromCache - a query option that establishes caching
   parameters on a Query
 * RelationshipCache - a variant of FromCache which is specific
   to a query invoked during a lazy load.

The rest of what's here are standard SQLAlchemy and
dogpile.cache constructs.

"""

from dogpile.cache.api import NO_VALUE

from sqlalchemy import event
from sqlalchemy.orm import loading
from sqlalchemy.orm import Query
from sqlalchemy.orm.interfaces import UserDefinedOption

class ORMCache:
    """An add-on for an ORM :class:`.Session` optionally loads full results
    from a dogpile cache region.

    """

    def __init__(self, regions):
        self.cache_regions = regions
        self._statement_cache = {}

    def listen_on_session(self, session_factory):
        event.listen(session_factory, "do_orm_execute", self._do_orm_execute)

    def _do_orm_execute(self, orm_context):
        for opt in orm_context.user_defined_options:
            if isinstance(opt, RelationshipCache):
                opt = opt._process_orm_context(orm_context)
                if opt is None:
                    continue

            if isinstance(opt, FromCache):
                dogpile_region = self.cache_regions[opt.region]

                our_cache_key = opt._generate_cache_key(
                    orm_context.statement, orm_context.parameters or {}, self
                )

                if opt.ignore_expiration:
                    cached_value = dogpile_region.get(
                        our_cache_key,
                        expiration_time=opt.expiration_time,
                        ignore_expiration=opt.ignore_expiration,
                    )
                else:

                    def createfunc():
                        return orm_context.invoke_statement().freeze()

                    cached_value = dogpile_region.get_or_create(
                        our_cache_key,
                        createfunc,
                        expiration_time=opt.expiration_time,
                    )

                if cached_value is NO_VALUE:
                    # keyerror?   this is bigger than a keyerror...
                    raise KeyError()

                orm_result = loading.merge_frozen_result(
                    orm_context.session,
                    orm_context.statement,
                    cached_value,
                    load=False,
                )
                return orm_result()

        else:
            return None

    def invalidate(self, statement, parameters, opt):
        """Invalidate the cache value represented by a statement."""

        if isinstance(statement, Query):
            statement = statement.__clause_element__()

        dogpile_region = self.cache_regions[opt.region]

        cache_key = opt._generate_cache_key(statement, parameters, self)

        dogpile_region.delete(cache_key)

class FromCache(UserDefinedOption):
    """Specifies that a Query should load results from a cache."""

    propagate_to_loaders = False

    def __init__(
        self,
        region="default",
        cache_key=None,
        expiration_time=None,
        ignore_expiration=False,
    ):
        """Construct a new FromCache.

        :param region: the cache region.  Should be a
         region configured in the dictionary of dogpile
         regions.

        :param cache_key: optional.  A string cache key
         that will serve as the key to the query.   Use this
         if your query has a huge amount of parameters (such
         as when using in_()) which correspond more simply to
         some other identifier.

        """
        self.region = region
        self.cache_key = cache_key
        self.expiration_time = expiration_time
        self.ignore_expiration = ignore_expiration

    # this is not needed as of SQLAlchemy 1.4.28;
    # UserDefinedOption classes no longer participate in the SQL
    # compilation cache key
    def _gen_cache_key(self, anon_map, bindparams):
        return None

    def _generate_cache_key(self, statement, parameters, orm_cache):
        """generate a cache key with which to key the results of a statement.

        This leverages the use of the SQL compilation cache key which is
        repurposed as a SQL results key.

        """
        statement_cache_key = statement._generate_cache_key()

        key = statement_cache_key.to_offline_string(
            orm_cache._statement_cache, statement, parameters
        ) + repr(self.cache_key)
        # print("here's our key...%s" % key)
        return key

class RelationshipCache(FromCache):
    """Specifies that a Query as called within a "lazy load"
    should load results from a cache."""

    propagate_to_loaders = True

    def __init__(
        self,
        attribute,
        region="default",
        cache_key=None,
        expiration_time=None,
        ignore_expiration=False,
    ):
        """Construct a new RelationshipCache.

        :param attribute: A Class.attribute which
         indicates a particular class relationship() whose
         lazy loader should be pulled from the cache.

        :param region: name of the cache region.

        :param cache_key: optional.  A string cache key
         that will serve as the key to the query, bypassing
         the usual means of forming a key from the Query itself.

        """
        self.region = region
        self.cache_key = cache_key
        self.expiration_time = expiration_time
        self.ignore_expiration = ignore_expiration
        self._relationship_options = {
            (attribute.property.parent.class_, attribute.property.key): self
        }

    def _process_orm_context(self, orm_context):
        current_path = orm_context.loader_strategy_path

        if current_path:
            mapper, prop = current_path[-2:]
            key = prop.key

            for cls in mapper.class_.__mro__:
                if (cls, key) in self._relationship_options:
                    relationship_option = self._relationship_options[
                        (cls, key)
                    ]
                    return relationship_option

    def and_(self, option):
        """Chain another RelationshipCache option to this one.

        While many RelationshipCache objects can be specified on a single
        Query separately, chaining them together allows for a more efficient
        lookup during load.

        """
        self._relationship_options.update(option._relationship_options)
        return self
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.environment

```
"""Establish data / cache file paths, and configurations,
bootstrap fixture data if necessary.

"""

from hashlib import md5
import os

from dogpile.cache.region import make_region

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from . import caching_query

# dogpile cache regions.  A home base for cache configurations.
regions = {}

# scoped_session.
Session = scoped_session(sessionmaker())

cache = caching_query.ORMCache(regions)
cache.listen_on_session(Session)

# global declarative base class.
Base = declarative_base()

root = "./dogpile_data/"

if not os.path.exists(root):
    input(
        "Will create datafiles in %r.\n"
        "To reset the cache + database, delete this directory.\n"
        "Press enter to continue.\n" % root
    )
    os.makedirs(root)

dbfile = os.path.join(root, "dogpile_demo.db")
engine = create_engine("sqlite:///%s" % dbfile, echo=True)
Session.configure(bind=engine)

def md5_key_mangler(key):
    """Receive cache keys as long concatenated strings;
    distill them into an md5 hash.

    """
    return md5(key.encode("ascii")).hexdigest()

# configure the "default" cache region.
regions["default"] = make_region(
    # the "dbm" backend needs
    # string-encoded keys
    key_mangler=md5_key_mangler
).configure(
    # using type 'file' to illustrate
    # serialized persistence.  Normally
    # memcached or similar is a better choice
    # for caching.
    "dogpile.cache.dbm",
    expiration_time=3600,
    arguments={"filename": os.path.join(root, "cache.dbm")},
)

# optional; call invalidate() on the region
# once created so that all data is fresh when
# the app is restarted.  Good for development,
# on a production system needs to be used carefully
# regions['default'].invalidate()

installed = False

def bootstrap():
    global installed
    from . import fixture_data

    if not os.path.exists(dbfile):
        fixture_data.install()
        installed = True
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.fixture_data

```
"""Installs some sample data.   Here we have a handful of postal codes for
a few US/Canadian cities.   Then, 100 Person records are installed, each
with a randomly selected postal code.

"""

import random

from .environment import Base
from .environment import Session
from .model import Address
from .model import City
from .model import Country
from .model import Person
from .model import PostalCode

def install():
    Base.metadata.create_all(Session().bind)

    data = [
        ("Chicago", "United States", ("60601", "60602", "60603", "60604")),
        ("Montreal", "Canada", ("H2S 3K9", "H2B 1V4", "H7G 2T8")),
        ("Edmonton", "Canada", ("T5J 1R9", "T5J 1Z4", "T5H 1P6")),
        (
            "New York",
            "United States",
            ("10001", "10002", "10003", "10004", "10005", "10006"),
        ),
        (
            "San Francisco",
            "United States",
            ("94102", "94103", "94104", "94105", "94107", "94108"),
        ),
    ]

    countries = {}
    all_post_codes = []
    for city, country, postcodes in data:
        try:
            country = countries[country]
        except KeyError:
            countries[country] = country = Country(country)

        city = City(city, country)
        pc = [PostalCode(code, city) for code in postcodes]
        Session.add_all(pc)
        all_post_codes.extend(pc)

    for i in range(1, 51):
        person = Person(
            "person %.2d" % i,
            Address(
                street="street %.2d" % i,
                postal_code=all_post_codes[
                    random.randint(0, len(all_post_codes) - 1)
                ],
            ),
        )
        Session.add(person)

    Session.commit()

    # start the demo fresh
    Session.remove()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.helloworld

```
"""Illustrate how to load some data, and cache the results."""

from sqlalchemy import select
from .caching_query import FromCache
from .environment import cache
from .environment import Session
from .model import Person

# load Person objects.  cache the result in the "default" cache region
print("loading people....")
people = Session.scalars(select(Person).options(FromCache("default"))).all()

# remove the Session.  next query starts from scratch.
Session.remove()

# load again, using the same FromCache option. now they're cached,
# so no SQL is emitted.
print("loading people....again!")
people = Session.scalars(select(Person).options(FromCache("default"))).all()

# Specifying a different query produces a different cache key, so
# these results are independently cached.
print("loading people two through twelve")
people_two_through_twelve = Session.scalars(
    select(Person)
    .options(FromCache("default"))
    .filter(Person.name.between("person 02", "person 12"))
).all()

# the data is cached under string structure of the SQL statement, *plus*
# the bind parameters of the query.    So this query, having
# different literal parameters under "Person.name.between()" than the
# previous one, issues new SQL...
print("loading people five through fifteen")
people_five_through_fifteen = Session.scalars(
    select(Person)
    .options(FromCache("default"))
    .filter(Person.name.between("person 05", "person 15"))
).all()

# ... but using the same params as are already cached, no SQL
print("loading people two through twelve...again!")
people_two_through_twelve = Session.scalars(
    select(Person)
    .options(FromCache("default"))
    .filter(Person.name.between("person 02", "person 12"))
).all()

# invalidate the cache for the three queries we've done.  Recreate
# each Query, which includes at the very least the same FromCache,
# same list of objects to be loaded, and the same parameters in the
# same order, then call invalidate().
print("invalidating everything")

cache.invalidate(Session.query(Person), {}, FromCache("default"))
cache.invalidate(
    select(Person).filter(Person.name.between("person 02", "person 12")),
    {},
    FromCache("default"),
)
cache.invalidate(
    select(Person).filter(Person.name.between("person 05", "person 15")),
    {},
    FromCache("default", "people_on_range"),
)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.local_session_caching

```
"""This example creates a new dogpile.cache backend that will persist data in a
dictionary which is local to the current session.   remove() the session and
the cache is gone.

Create a new Dogpile cache backend that will store
cached data local to the current Session.

This is an advanced example which assumes familiarity
with the basic operation of CachingQuery.

"""

from dogpile.cache import make_region
from dogpile.cache.api import CacheBackend
from dogpile.cache.api import NO_VALUE
from dogpile.cache.region import register_backend

from sqlalchemy import select
from . import environment
from .caching_query import FromCache
from .environment import regions
from .environment import Session

class ScopedSessionBackend(CacheBackend):
    """A dogpile backend which will cache objects locally on
    the current session.

    When used with the query_cache system, the effect is that the objects
    in the cache are the same as that within the session - the merge()
    is a formality that doesn't actually create a second instance.
    This makes it safe to use for updates of data from an identity
    perspective (still not ideal for deletes though).

    When the session is removed, the cache is gone too, so the cache
    is automatically disposed upon session.remove().

    """

    def __init__(self, arguments):
        self.scoped_session = arguments["scoped_session"]

    def get(self, key):
        return self._cache_dictionary.get(key, NO_VALUE)

    def set(self, key, value):
        self._cache_dictionary[key] = value

    def delete(self, key):
        self._cache_dictionary.pop(key, None)

    @property
    def _cache_dictionary(self):
        """Return the cache dictionary linked to the current Session."""

        sess = self.scoped_session()
        try:
            cache_dict = sess._cache_dictionary
        except AttributeError:
            sess._cache_dictionary = cache_dict = {}
        return cache_dict

register_backend("sqlalchemy.session", __name__, "ScopedSessionBackend")

if __name__ == "__main__":
    # set up a region based on the ScopedSessionBackend,
    # pointing to the scoped_session declared in the example
    # environment.
    regions["local_session"] = make_region().configure(
        "sqlalchemy.session", arguments={"scoped_session": Session}
    )

    from .model import Person

    # query to load Person by name, with criterion
    # of "person 10"
    q = (
        select(Person)
        .filter(Person.name == "person 10")
        .options(FromCache("local_session"))
    )

    # load from DB
    person10 = Session.scalars(q).one()

    # next call, the query is cached.
    person10 = Session.scalars(q).one()

    # clear out the Session.  The "_cache_dictionary" dictionary
    # disappears with it.
    Session.remove()

    # query calls from DB again
    person10 = Session.scalars(q).one()

    # identity is preserved - person10 is the *same* object that's
    # ultimately inside the cache.   So it is safe to manipulate
    # the not-queried-for attributes of objects when using such a
    # cache without the need to invalidate - however, any change
    # that would change the results of a cached query, such as
    # inserts, deletes, or modification to attributes that are
    # part of query criterion, still require careful invalidation.
    cache_key = FromCache("local_session")._generate_cache_key(
        q, {}, environment.cache
    )

    assert person10 is regions["local_session"].get(cache_key)().scalar()
```
