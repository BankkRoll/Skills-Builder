# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.model

```
"""The datamodel, which represents Person that has multiple
Address objects, each with PostalCode, City, Country.

Person --(1..n)--> Address
Address --(has a)--> PostalCode
PostalCode --(has a)--> City
City --(has a)--> Country

"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from .caching_query import RelationshipCache
from .environment import Base
from .environment import bootstrap

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name):
        self.name = name

class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    country = relationship(Country)

    def __init__(self, name, country):
        self.name = name
        self.country = country

class PostalCode(Base):
    __tablename__ = "postal_code"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    city = relationship(City)

    @property
    def country(self):
        return self.city.country

    def __init__(self, code, city):
        self.code = code
        self.city = city

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    street = Column(String(200), nullable=False)
    postal_code_id = Column(Integer, ForeignKey("postal_code.id"))
    postal_code = relationship(PostalCode)

    @property
    def city(self):
        return self.postal_code.city

    @property
    def country(self):
        return self.postal_code.country

    def __str__(self):
        return "%s\t%s, %s\t%s" % (
            self.street,
            self.city.name,
            self.postal_code.code,
            self.country.name,
        )

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    addresses = relationship(Address, collection_class=set)

    def __init__(self, name, *addresses):
        self.name = name
        self.addresses = set(addresses)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Person(name=%r)" % self.name

    def format_full(self):
        return "\t".join([str(x) for x in [self] + list(self.addresses)])

# Caching options.   A set of three RelationshipCache options
# which can be applied to Query(), causing the "lazy load"
# of these attributes to be loaded from cache.
cache_address_bits = (
    RelationshipCache(PostalCode.city, "default")
    .and_(RelationshipCache(City.country, "default"))
    .and_(RelationshipCache(Address.postal_code, "default"))
)

bootstrap()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dogpile_caching.relationship_caching

```
"""Illustrates how to add cache options on
relationship endpoints, so that lazyloads load from cache.

Load a set of Person and Address objects, specifying that
related PostalCode, City, Country objects should be pulled from long
term cache.

"""

import os

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .environment import root
from .environment import Session
from .model import cache_address_bits
from .model import Person

for p in Session.scalars(
    select(Person).options(joinedload(Person.addresses), cache_address_bits)
).unique():
    print(p.format_full())

print(
    "\n\nIf this was the first run of relationship_caching.py, "
    "SQL was likely emitted to "
    "load postal codes, cities, countries.\n"
    "If run a second time, assuming the cache is still valid, "
    "only a single SQL statement will run - all "
    "related data is pulled from cache.\n"
    "To clear the cache, delete the file %r.  \n"
    "This will cause a re-load of cities, postal codes and countries on "
    "the next run.\n" % os.path.join(root, "cache.dbm")
)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.dynamic_dict.dynamic_dict

```
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

class ProxyDict:
    def __init__(self, parent, collection_name, childclass, keyname):
        self.parent = parent
        self.collection_name = collection_name
        self.childclass = childclass
        self.keyname = keyname

    @property
    def collection(self):
        return getattr(self.parent, self.collection_name)

    def keys(self):
        descriptor = getattr(self.childclass, self.keyname)
        return [x[0] for x in self.collection.values(descriptor)]

    def __getitem__(self, key):
        x = self.collection.filter_by(**{self.keyname: key}).first()
        if x:
            return x
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        try:
            existing = self[key]
            self.collection.remove(existing)
        except KeyError:
            pass
        self.collection.append(value)

engine = create_engine("sqlite://", echo=True)
Base = declarative_base(engine)

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    _collection = relationship(
        "Child", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def child_map(self):
        return ProxyDict(self, "_collection", Child, "key")

class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    key = Column(String(50))
    parent_id = Column(Integer, ForeignKey("parent.id"))

    def __repr__(self):
        return "Child(key=%r)" % self.key

Base.metadata.create_all()

sess = sessionmaker()()

p1 = Parent(name="p1")
sess.add(p1)

print("\n---------begin setting nodes, autoflush occurs\n")
p1.child_map["k1"] = Child(key="k1")
p1.child_map["k2"] = Child(key="k2")

# this will autoflush the current map.
# ['k1', 'k2']
print("\n---------print keys - flushes first\n")
print(list(p1.child_map.keys()))

# k1
print("\n---------print 'k1' node\n")
print(p1.child_map["k1"])

print("\n---------update 'k2' node - must find existing, and replace\n")
p1.child_map["k2"] = Child(key="k2")

print("\n---------print 'k2' key - flushes first\n")
# k2
print(p1.child_map["k2"])

print("\n---------print all child nodes\n")
# [k1, k2b]
print(sess.query(Child).all())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.extending_query.filter_public

```
"""Illustrates a global criteria applied to entities of a particular type.

The example here is the "public" flag, a simple boolean that indicates
the rows are part of a publicly viewable subcategory.  Rows that do not
include this flag are not shown unless a special option is passed to the
query.

Uses for this kind of recipe include tables that have "soft deleted" rows
marked as "deleted" that should be skipped, rows that have access control rules
that should be applied on a per-request basis, etc.

"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    """Intercept all ORM queries.   Add a with_loader_criteria option to all
    of them.

    This option applies to SELECT queries and adds a global WHERE criteria
    (or as appropriate ON CLAUSE criteria for join targets)
    to all objects of a certain class or superclass.

    """

    # the with_loader_criteria automatically applies itself to
    # relationship loads as well including lazy loads.   So if this is
    # a relationship load, assume the option was set up from the top level
    # query.

    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_private", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                HasPrivate,
                lambda cls: cls.public == true(),
                include_aliases=True,
            )
        )

class HasPrivate:
    """Mixin that identifies a class as having private entities"""

    public = Column(Boolean, nullable=False)

if __name__ == "__main__":
    Base = declarative_base()

    class User(HasPrivate, Base):
        __tablename__ = "user"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        addresses = relationship("Address", back_populates="user")

    class Address(HasPrivate, Base):
        __tablename__ = "address"

        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey("user.id"))

        user = relationship("User", back_populates="addresses")

    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    sess = Session()

    sess.add_all(
        [
            User(
                name="u1",
                public=True,
                addresses=[
                    Address(email="u1a1", public=True),
                    Address(email="u1a2", public=True),
                ],
            ),
            User(
                name="u2",
                public=True,
                addresses=[
                    Address(email="u2a1", public=False),
                    Address(email="u2a2", public=True),
                ],
            ),
            User(
                name="u3",
                public=False,
                addresses=[
                    Address(email="u3a1", public=False),
                    Address(email="u3a2", public=False),
                ],
            ),
            User(
                name="u4",
                public=False,
                addresses=[
                    Address(email="u4a1", public=False),
                    Address(email="u4a2", public=True),
                ],
            ),
            User(
                name="u5",
                public=True,
                addresses=[
                    Address(email="u5a1", public=True),
                    Address(email="u5a2", public=False),
                ],
            ),
        ]
    )

    sess.commit()

    # now querying Address or User objects only gives us the public ones
    for u1 in sess.query(User).options(orm.selectinload(User.addresses)):
        assert u1.public

        # the addresses collection will also be "public only", which works
        # for all relationship loaders including joinedload
        for address in u1.addresses:
            assert address.public

    # works for columns too
    cols = (
        sess.query(User.id, Address.id)
        .join(User.addresses)
        .order_by(User.id, Address.id)
        .all()
    )
    assert cols == [(1, 1), (1, 2), (2, 4), (5, 9)]

    cols = (
        sess.query(User.id, Address.id)
        .join(User.addresses)
        .order_by(User.id, Address.id)
        .execution_options(include_private=True)
        .all()
    )
    assert cols == [
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (3, 5),
        (3, 6),
        (4, 7),
        (4, 8),
        (5, 9),
        (5, 10),
    ]

    # count all public addresses
    assert sess.query(Address).count() == 5

    # count all addresses public and private
    assert (
        sess.query(Address).execution_options(include_private=True).count()
        == 10
    )

    # load an Address that is public, but its parent User is private
    # (2.0 style query)
    a1 = sess.execute(select(Address).filter_by(email="u4a2")).scalar()

    # assuming the User isn't already in the Session, it returns None
    assert a1.user is None

    # however, if that user is present in the session, then a many-to-one
    # does a simple get() and it will be present
    sess.expire(a1, ["user"])
    u1 = sess.execute(
        select(User)
        .filter_by(name="u4")
        .execution_options(include_private=True)
    ).scalar()
    assert a1.user is u1
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.extending_query.temporal_range

```
"""Illustrates a custom per-query criteria that will be applied
to selected entities.

"""

import datetime
from functools import partial

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

class HasTemporal:
    """Mixin that identifies a class as having a timestamp column"""

    timestamp = Column(
        DateTime,
        default=partial(datetime.datetime.now, datetime.timezone.utc),
        nullable=False,
    )

def temporal_range(range_lower, range_upper):
    return orm.with_loader_criteria(
        HasTemporal,
        lambda cls: cls.timestamp.between(range_lower, range_upper),
        include_aliases=True,
    )

if __name__ == "__main__":
    Base = declarative_base()

    class Parent(HasTemporal, Base):
        __tablename__ = "parent"
        id = Column(Integer, primary_key=True)
        children = relationship("Child")

    class Child(HasTemporal, Base):
        __tablename__ = "child"
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey("parent.id"), nullable=False)

    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    sess = Session()

    c1, c2, c3, c4, c5 = [
        Child(timestamp=datetime.datetime(2009, 10, 15, 12, 00, 00)),
        Child(timestamp=datetime.datetime(2009, 10, 17, 12, 00, 00)),
        Child(timestamp=datetime.datetime(2009, 10, 20, 12, 00, 00)),
        Child(timestamp=datetime.datetime(2009, 10, 12, 12, 00, 00)),
        Child(timestamp=datetime.datetime(2009, 10, 17, 12, 00, 00)),
    ]

    p1 = Parent(
        timestamp=datetime.datetime(2009, 10, 15, 12, 00, 00),
        children=[c1, c2, c3],
    )
    p2 = Parent(
        timestamp=datetime.datetime(2009, 10, 17, 12, 00, 00),
        children=[c4, c5],
    )

    sess.add_all([p1, p2])
    sess.commit()

    # use populate_existing() to ensure the range option takes
    # place for elements already in the identity map

    parents = (
        sess.query(Parent)
        .populate_existing()
        .options(
            temporal_range(
                datetime.datetime(2009, 10, 16, 12, 00, 00),
                datetime.datetime(2009, 10, 18, 12, 00, 00),
            )
        )
        .all()
    )

    assert parents[0] == p2
    assert parents[0].children == [c5]

    sess.expire_all()

    # try it with eager load
    parents = (
        sess.query(Parent)
        .options(
            temporal_range(
                datetime.datetime(2009, 10, 16, 12, 00, 00),
                datetime.datetime(2009, 10, 18, 12, 00, 00),
            )
        )
        .options(selectinload(Parent.children))
        .all()
    )

    assert parents[0] == p2
    assert parents[0].children == [c5]

    sess.expire_all()

    # illustrate a 2.0 style query
    print("------------------")
    parents = (
        sess.execute(
            select(Parent)
            .execution_options(populate_existing=True)
            .options(
                temporal_range(
                    datetime.datetime(2009, 10, 15, 11, 00, 00),
                    datetime.datetime(2009, 10, 18, 12, 00, 00),
                )
            )
            .join(Parent.children)
            .filter(Child.id == 2)
        )
        .scalars()
        .all()
    )

    assert parents[0] == p1
    print("-------------------")
    assert parents[0].children == [c1, c2]
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.generic_associations.discriminator_on_association

```
"""Illustrates a mixin which provides a generic association
using a single target table and a single association table,
referred to by all parent tables.  The association table
contains a "discriminator" column which determines what type of
parent object associates to each particular row in the association
table.

SQLAlchemy's single-table-inheritance feature is used
to target different association types.

This configuration attempts to simulate a so-called "generic foreign key"
as closely as possible without actually foregoing the use of real
foreign keys.   Unlike table-per-related and table-per-association,
it uses a fixed number of tables to serve any number of potential parent
objects, but is also slightly more complex.

"""

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class AddressAssociation(Base):
    """Associates a collection of Address objects
    with a particular parent.
    """

    __tablename__ = "address_association"

    discriminator: Mapped[str] = mapped_column()
    """Refers to the type of parent."""
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="association"
    )

    __mapper_args__ = {"polymorphic_on": discriminator}

class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.
    """

    association_id: Mapped[int] = mapped_column(
        ForeignKey("address_association.id")
    )
    street: Mapped[str]
    city: Mapped[str]
    zip: Mapped[str]
    association: Mapped["AddressAssociation"] = relationship(
        back_populates="addresses"
    )

    parent = association_proxy("association", "parent")

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )

class HasAddresses:
    """HasAddresses mixin, creates a relationship to
    the address_association table for each parent.
    """

    @declared_attr
    def address_association_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("address_association.id"))

    @declared_attr
    def address_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            f"{name}AddressAssociation",
            (AddressAssociation,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
            ),
        )

        cls.addresses = association_proxy(
            "address_association",
            "addresses",
            creator=lambda addresses: assoc_cls(addresses=addresses),
        )
        return relationship(
            assoc_cls, backref=backref("parent", uselist=False)
        )

class Customer(HasAddresses, Base):
    name: Mapped[str]

class Supplier(HasAddresses, Base):
    company_name: Mapped[str]

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all(
    [
        Customer(
            name="customer 1",
            addresses=[
                Address(
                    street="123 anywhere street", city="New York", zip="10110"
                ),
                Address(
                    street="40 main street", city="San Francisco", zip="95732"
                ),
            ],
        ),
        Supplier(
            company_name="Ace Hammers",
            addresses=[
                Address(street="2569 west elm", city="Detroit", zip="56785")
            ],
        ),
    ]
)

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)
        print(address.parent)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.generic_associations.generic_fk

```
"""Illustrates a so-called "generic foreign key", in a similar fashion
to that of popular frameworks such as Django, ROR, etc.  This
approach bypasses standard referential integrity
practices, in that the "foreign key" column is not actually
constrained to refer to any particular table; instead,
in-application logic is used to determine which table is referenced.

This approach is not in line with SQLAlchemy's usual style, as foregoing
foreign key integrity means that the tables can easily contain invalid
references and also have no ability to use in-database cascade functionality.

However, due to the popularity of these systems, as well as that it uses
the fewest number of tables (which doesn't really offer any "advantage",
though seems to be comforting to many) this recipe remains in
high demand, so in the interests of having an easy StackOverflow answer
queued up, here it is.   The author recommends "table_per_related"
or "table_per_association" instead of this approach.

"""

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import backref
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import foreign
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import remote
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.
    """

    street: Mapped[str]
    city: Mapped[str]
    zip: Mapped[str]

    discriminator: Mapped[str]
    """Refers to the type of parent."""

    parent_id: Mapped[int]
    """Refers to the primary key of the parent.

    This could refer to any table.
    """

    @property
    def parent(self):
        """Provides in-Python access to the "parent" by choosing
        the appropriate relationship.
        """
        return getattr(self, f"parent_{self.discriminator}")

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )

class HasAddresses:
    """HasAddresses mixin, creates a relationship to
    the address_association table for each parent.

    """

@event.listens_for(HasAddresses, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    discriminator = name.lower()
    class_.addresses = relationship(
        Address,
        primaryjoin=and_(
            class_.id == foreign(remote(Address.parent_id)),
            Address.discriminator == discriminator,
        ),
        backref=backref(
            "parent_%s" % discriminator,
            primaryjoin=remote(class_.id) == foreign(Address.parent_id),
            overlaps="addresses, parent_customer",
        ),
        overlaps="addresses",
    )

    @event.listens_for(class_.addresses, "append")
    def append_address(target, value, initiator):
        value.discriminator = discriminator

class Customer(HasAddresses, Base):
    name: Mapped[str]

class Supplier(HasAddresses, Base):
    company_name: Mapped[str]

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all(
    [
        Customer(
            name="customer 1",
            addresses=[
                Address(
                    street="123 anywhere street", city="New York", zip="10110"
                ),
                Address(
                    street="40 main street", city="San Francisco", zip="95732"
                ),
            ],
        ),
        Supplier(
            company_name="Ace Hammers",
            addresses=[
                Address(street="2569 west elm", city="Detroit", zip="56785")
            ],
        ),
    ]
)

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)
        print(address.parent)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.generic_associations.table_per_association

```
"""Illustrates a mixin which provides a generic association
via a individually generated association tables for each parent class.
The associated objects themselves are persisted in a single table
shared among all parents.

This configuration has the advantage that all Address
rows are in one table, so that the definition of "Address"
can be maintained in one place.   The association table
contains the foreign key to Address so that Address
has no dependency on the system.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.
    """

    street: Mapped[str]
    city: Mapped[str]
    zip: Mapped[str]

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )

class HasAddresses:
    """HasAddresses mixin, creates a new address_association
    table for each parent.

    """

    @declared_attr
    def addresses(cls):
        address_association = Table(
            "%s_addresses" % cls.__tablename__,
            cls.metadata,
            Column("address_id", ForeignKey("address.id"), primary_key=True),
            Column(
                "%s_id" % cls.__tablename__,
                ForeignKey("%s.id" % cls.__tablename__),
                primary_key=True,
            ),
        )
        return relationship(Address, secondary=address_association)

class Customer(HasAddresses, Base):
    name: Mapped[str]

class Supplier(HasAddresses, Base):
    company_name: Mapped[str]

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all(
    [
        Customer(
            name="customer 1",
            addresses=[
                Address(
                    street="123 anywhere street", city="New York", zip="10110"
                ),
                Address(
                    street="40 main street", city="San Francisco", zip="95732"
                ),
            ],
        ),
        Supplier(
            company_name="Ace Hammers",
            addresses=[
                Address(street="2569 west elm", city="Detroit", zip="56785")
            ],
        ),
    ]
)

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)
        # no parent here
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.generic_associations.table_per_related

```
"""Illustrates a generic association which persists association
objects within individual tables, each one generated to persist
those objects on behalf of a particular parent class.

This configuration has the advantage that each type of parent
maintains its "Address" rows separately, so that collection
size for one type of parent will have no impact on other types
of parent.   Navigation between parent and "Address" is simple,
direct, and bidirectional.

This recipe is the most efficient (speed wise and storage wise)
and simple of all of them.

The creation of many related tables may seem at first like an issue
but there really isn't any - the management and targeting of these tables
is completely automated.

"""

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class Address:
    """Define columns that will be present in each
    'Address' table.

    This is a declarative mixin, so additional mapped
    attributes beyond simple columns specified here
    should be set up using @declared_attr.

    """

    street: Mapped[str]
    city: Mapped[str]
    zip: Mapped[str]

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )

class HasAddresses:
    """HasAddresses mixin, creates a new Address class
    for each parent.

    """

    @declared_attr
    def addresses(cls):
        cls.Address = type(
            f"{cls.__name__}Address",
            (Address, Base),
            dict(
                __tablename__=f"{cls.__tablename__}_address",
                parent_id=mapped_column(
                    Integer, ForeignKey(f"{cls.__tablename__}.id")
                ),
                parent=relationship(cls, overlaps="addresses"),
            ),
        )
        return relationship(cls.Address)

class Customer(HasAddresses, Base):
    name: Mapped[str]

class Supplier(HasAddresses, Base):
    company_name: Mapped[str]

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = Session(engine)

session.add_all(
    [
        Customer(
            name="customer 1",
            addresses=[
                Customer.Address(
                    street="123 anywhere street", city="New York", zip="10110"
                ),
                Customer.Address(
                    street="40 main street", city="San Francisco", zip="95732"
                ),
            ],
        ),
        Supplier(
            company_name="Ace Hammers",
            addresses=[
                Supplier.Address(
                    street="2569 west elm", city="Detroit", zip="56785"
                )
            ],
        ),
    ]
)

session.commit()

for customer in session.query(Customer):
    for address in customer.addresses:
        print(address)
        print(address.parent)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.graphs.directed_graph

```
"""a directed graph example."""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Node(Base):
    __tablename__ = "node"

    node_id = Column(Integer, primary_key=True)

    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]

class Edge(Base):
    __tablename__ = "edge"

    lower_id = Column(Integer, ForeignKey("node.node_id"), primary_key=True)

    higher_id = Column(Integer, ForeignKey("node.node_id"), primary_key=True)

    lower_node = relationship(
        Node, primaryjoin=lower_id == Node.node_id, backref="lower_edges"
    )

    higher_node = relationship(
        Node, primaryjoin=higher_id == Node.node_id, backref="higher_edges"
    )

    def __init__(self, n1, n2):
        self.lower_node = n1
        self.higher_node = n2

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()

# create a directed graph like this:
#       n1 -> n2 -> n1
#                -> n5
#                -> n7
#          -> n3 -> n6

n1 = Node()
n2 = Node()
n3 = Node()
n4 = Node()
n5 = Node()
n6 = Node()
n7 = Node()

Edge(n1, n2)
Edge(n1, n3)
Edge(n2, n1)
Edge(n2, n5)
Edge(n2, n7)
Edge(n3, n6)

session.add_all([n1, n2, n3, n4, n5, n6, n7])
session.commit()

assert [x for x in n3.higher_neighbors()] == [n6]
assert [x for x in n3.lower_neighbors()] == [n1]
assert [x for x in n2.lower_neighbors()] == [n1]
assert [x for x in n2.higher_neighbors()] == [n1, n5, n7]
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.inheritance.concrete

```
"""Concrete-table (table-per-class) inheritance example."""

from __future__ import annotations

from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.declarative import ConcreteBase
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic

intpk = Annotated[int, mapped_column(primary_key=True)]
str50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "company"
    id: Mapped[intpk]
    name: Mapped[str50]

    employees: Mapped[list[Person]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Company {self.name}"

class Person(ConcreteBase, Base):
    __tablename__ = "person"
    id: Mapped[intpk]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    name: Mapped[str50]

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_identity": "person",
    }

    def __repr__(self):
        return f"Ordinary person {self.name}"

class Engineer(Person):
    __tablename__ = "engineer"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    name: Mapped[str50]
    status: Mapped[str50]
    engineer_name: Mapped[str50]
    primary_language: Mapped[str50]

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {"polymorphic_identity": "engineer", "concrete": True}

class Manager(Person):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    name: Mapped[str50]
    status: Mapped[str50]
    manager_name: Mapped[str50]

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {"polymorphic_identity": "manager", "concrete": True}

    def __repr__(self):
        return (
            f"Manager {self.name}, status {self.status}, "
            f"manager_name {self.manager_name}"
        )

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    c = Company(
        name="company1",
        employees=[
            Manager(
                name="mr krabs",
                status="AAB",
                manager_name="manager1",
            ),
            Engineer(
                name="spongebob",
                status="BBA",
                engineer_name="engineer1",
                primary_language="java",
            ),
            Person(name="joesmith"),
            Engineer(
                name="patrick",
                status="CGG",
                engineer_name="engineer2",
                primary_language="python",
            ),
            Manager(name="jsmith", status="ABA", manager_name="manager2"),
        ],
    )
    session.add(c)

    session.commit()

    for e in c.employees:
        print(e)

    spongebob = session.scalars(
        select(Person).filter_by(name="spongebob")
    ).one()
    spongebob2 = session.scalars(
        select(Engineer).filter_by(name="spongebob")
    ).one()
    assert spongebob is spongebob2

    spongebob2.engineer_name = "hes spongebob!"

    session.commit()

    # query using with_polymorphic.
    # when using ConcreteBase, use "*" to use the default selectable
    # setting specific entities won't work right now.
    eng_manager = with_polymorphic(Person, "*")
    print(
        session.scalars(
            select(eng_manager).filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )

    # illustrate join from Company.
    print(
        session.scalars(
            select(Company)
            .join(Company.employees.of_type(eng_manager))
            .filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )

    session.commit()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.inheritance.joined

```
"""Joined-table (table-per-subclass) inheritance example."""

from __future__ import annotations

from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic

intpk = Annotated[int, mapped_column(primary_key=True)]
str50 = Annotated[str, mapped_column(String(50))]

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "company"
    id: Mapped[intpk]
    name: Mapped[str50]

    employees: Mapped[list[Person]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Company {self.name}"

class Person(Base):
    __tablename__ = "person"
    id: Mapped[intpk]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    name: Mapped[str50]
    type: Mapped[str50]

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"Ordinary person {self.name}"

class Engineer(Person):
    __tablename__ = "engineer"
    id: Mapped[intpk] = mapped_column(ForeignKey("person.id"))
    status: Mapped[str50]
    engineer_name: Mapped[str50]
    primary_language: Mapped[str50]

    __mapper_args__ = {"polymorphic_identity": "engineer"}

    def __repr__(self):
        return (
            f"Engineer {self.name}, status {self.status}, "
            f"engineer_name {self.engineer_name}, "
            f"primary_language {self.primary_language}"
        )

class Manager(Person):
    __tablename__ = "manager"
    id: Mapped[intpk] = mapped_column(ForeignKey("person.id"))
    status: Mapped[str50]
    manager_name: Mapped[str50]

    __mapper_args__ = {"polymorphic_identity": "manager"}

    def __repr__(self):
        return (
            f"Manager {self.name}, status {self.status}, "
            f"manager_name {self.manager_name}"
        )

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    c = Company(
        name="company1",
        employees=[
            Manager(
                name="mr krabs",
                status="AAB",
                manager_name="manager1",
            ),
            Engineer(
                name="spongebob",
                status="BBA",
                engineer_name="engineer1",
                primary_language="java",
            ),
            Person(name="joesmith"),
            Engineer(
                name="patrick",
                status="CGG",
                engineer_name="engineer2",
                primary_language="python",
            ),
            Manager(name="jsmith", status="ABA", manager_name="manager2"),
        ],
    )
    session.add(c)

    session.commit()

    for e in c.employees:
        print(e)

    spongebob = session.scalars(
        select(Person).filter_by(name="spongebob")
    ).one()
    spongebob2 = session.scalars(
        select(Engineer).filter_by(name="spongebob")
    ).one()
    assert spongebob is spongebob2

    spongebob2.engineer_name = "hes spongebob!"

    session.commit()

    # query using with_polymorphic.  flat=True is generally recommended
    # for joined inheritance mappings as it will produce fewer levels
    # of subqueries
    eng_manager = with_polymorphic(Person, [Engineer, Manager], flat=True)
    print(
        session.scalars(
            select(eng_manager).filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )

    # illustrate join from Company.
    eng_manager = with_polymorphic(Person, [Engineer, Manager], flat=True)
    print(
        session.scalars(
            select(Company)
            .join(Company.employees.of_type(eng_manager))
            .filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.inheritance.single

```
"""Single-table (table-per-hierarchy) inheritance example."""

from __future__ import annotations

from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import FromClause
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_polymorphic

intpk = Annotated[int, mapped_column(primary_key=True)]
str50 = Annotated[str, mapped_column(String(50))]

# columns that are local to subclasses must be nullable.
# we can still use a non-optional type, however
str50subclass = Annotated[str, mapped_column(String(50), nullable=True)]

class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "company"
    id: Mapped[intpk]
    name: Mapped[str50]

    employees: Mapped[list[Person]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Company {self.name}"

class Person(Base):
    __tablename__ = "person"
    __table__: FromClause

    id: Mapped[intpk]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    name: Mapped[str50]
    type: Mapped[str50]

    company: Mapped[Company] = relationship(back_populates="employees")

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"Ordinary person {self.name}"

class Engineer(Person):
    # illustrate a single-inh "conflicting" mapped_column declaration,
    # where both subclasses want to share the same column that is nonetheless
    # not "local" to the base class
    @declared_attr
    def status(cls) -> Mapped[str50]:
        return Person.__table__.c.get(
            "status", mapped_column(String(30))  # type: ignore
        )

    engineer_name: Mapped[str50subclass]
    primary_language: Mapped[str50subclass]

    __mapper_args__ = {"polymorphic_identity": "engineer"}

    def __repr__(self):
        return (
            f"Engineer {self.name}, status {self.status}, "
            f"engineer_name {self.engineer_name}, "
            f"primary_language {self.primary_language}"
        )

class Manager(Person):
    manager_name: Mapped[str50subclass]

    # illustrate a single-inh "conflicting" mapped_column declaration,
    # where both subclasses want to share the same column that is nonetheless
    # not "local" to the base class
    @declared_attr
    def status(cls) -> Mapped[str50]:
        return Person.__table__.c.get(
            "status", mapped_column(String(30))  # type: ignore
        )

    __mapper_args__ = {"polymorphic_identity": "manager"}

    def __repr__(self):
        return (
            f"Manager {self.name}, status {self.status}, "
            f"manager_name {self.manager_name}"
        )

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    c = Company(
        name="company1",
        employees=[
            Manager(
                name="mr krabs",
                status="AAB",
                manager_name="manager1",
            ),
            Engineer(
                name="spongebob",
                status="BBA",
                engineer_name="engineer1",
                primary_language="java",
            ),
            Person(name="joesmith"),
            Engineer(
                name="patrick",
                status="CGG",
                engineer_name="engineer2",
                primary_language="python",
            ),
            Manager(name="jsmith", status="ABA", manager_name="manager2"),
        ],
    )
    session.add(c)

    session.commit()

    for e in c.employees:
        print(e)

    spongebob = session.scalars(
        select(Person).filter_by(name="spongebob")
    ).one()
    spongebob2 = session.scalars(
        select(Engineer).filter_by(name="spongebob")
    ).one()
    assert spongebob is spongebob2

    spongebob2.engineer_name = "hes spongebob!"

    session.commit()

    # query using with_polymorphic.
    eng_manager = with_polymorphic(Person, [Engineer, Manager])
    print(
        session.scalars(
            select(eng_manager).filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )

    # illustrate join from Company.
    print(
        session.scalars(
            select(Company)
            .join(Company.employees.of_type(eng_manager))
            .filter(
                or_(
                    eng_manager.Engineer.engineer_name == "engineer1",
                    eng_manager.Manager.manager_name == "manager2",
                )
            )
        ).all()
    )
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.materialized_paths.materialized_paths

```
"""Illustrates the "materialized paths" pattern.

Materialized paths is a way to represent a tree structure in SQL with fast
descendant and ancestor queries at the expense of moving nodes (which require
O(n) UPDATEs in the worst case, where n is the number of nodes in the tree). It
is a good balance in terms of performance and simplicity between the nested
sets model and the adjacency list model.

It works by storing all nodes in a table with a path column, containing a
string of delimited IDs. Think file system paths:

    1
    1.2
    1.3
    1.3.4
    1.3.5
    1.3.6
    1.7
    1.7.8
    1.7.9
    1.7.9.10
    1.7.11

Descendant queries are simple left-anchored LIKE queries, and ancestors are
already stored in the path itself. Updates require going through all
descendants and changing the prefix.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import foreign
from sqlalchemy.orm import relationship
from sqlalchemy.orm import remote
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import cast

Base = declarative_base()

class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, autoincrement=False)
    path = Column(String(500), nullable=False, index=True)

    # To find the descendants of this node, we look for nodes whose path
    # starts with this node's path.
    descendants = relationship(
        "Node",
        viewonly=True,
        order_by=path,
        primaryjoin=remote(foreign(path)).like(path.concat(".%")),
    )

    # Finding the ancestors is a little bit trickier. We need to create a fake
    # secondary table since this behaves like a many-to-many join.
    secondary = select(
        id.label("id"),
        func.unnest(
            cast(
                func.string_to_array(
                    func.regexp_replace(path, r"\.?\d+$", ""), "."
                ),
                ARRAY(Integer),
            )
        ).label("ancestor_id"),
    ).alias()
    ancestors = relationship(
        "Node",
        viewonly=True,
        secondary=secondary,
        primaryjoin=id == secondary.c.id,
        secondaryjoin=secondary.c.ancestor_id == id,
        order_by=path,
    )

    @property
    def depth(self):
        return len(self.path.split(".")) - 1

    def __repr__(self):
        return f"Node(id={self.id})"

    def __str__(self):
        root_depth = self.depth
        s = [str(self.id)]
        s.extend(
            ((n.depth - root_depth) * "  " + str(n.id))
            for n in self.descendants
        )
        return "\n".join(s)

    def move_to(self, new_parent):
        new_path = new_parent.path + "." + str(self.id)
        for n in self.descendants:
            n.path = new_path + n.path[len(self.path) :]
        self.path = new_path

if __name__ == "__main__":
    engine = create_engine(
        "postgresql+psycopg2://scott:tiger@localhost/test", echo=True
    )
    Base.metadata.create_all(engine)

    session = Session(engine)

    print("-" * 80)
    print("create a tree")
    session.add_all(
        [
            Node(id=1, path="1"),
            Node(id=2, path="1.2"),
            Node(id=3, path="1.3"),
            Node(id=4, path="1.3.4"),
            Node(id=5, path="1.3.5"),
            Node(id=6, path="1.3.6"),
            Node(id=7, path="1.7"),
            Node(id=8, path="1.7.8"),
            Node(id=9, path="1.7.9"),
            Node(id=10, path="1.7.9.10"),
            Node(id=11, path="1.7.11"),
        ]
    )
    session.flush()
    print(str(session.query(Node).get(1)))

    print("-" * 80)
    print("move 7 under 3")
    session.query(Node).get(7).move_to(session.query(Node).get(3))
    session.flush()
    print(str(session.query(Node).get(1)))

    print("-" * 80)
    print("move 3 under 2")
    session.query(Node).get(3).move_to(session.query(Node).get(2))
    session.flush()
    print(str(session.query(Node).get(1)))

    print("-" * 80)
    print("find the ancestors of 10")
    print([n.id for n in session.query(Node).get(10).ancestors])

    session.close()
    Base.metadata.drop_all(engine)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.nested_sets.nested_sets

```
"""Celko's "Nested Sets" Tree Structure.

https://www.intelligententerprise.com/001020/celko.jhtml

"""

from sqlalchemy import case
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session

Base = declarative_base()

class Employee(Base):
    __tablename__ = "personnel"
    __mapper_args__ = {
        "batch": False  # allows extension to fire for each
        # instance before going to the next.
    }

    parent = None

    emp = Column(String, primary_key=True)

    left = Column("lft", Integer, nullable=False)
    right = Column("rgt", Integer, nullable=False)

    def __repr__(self):
        return "Employee(%s, %d, %d)" % (self.emp, self.left, self.right)

@event.listens_for(Employee, "before_insert")
def before_insert(mapper, connection, instance):
    if not instance.parent:
        instance.left = 1
        instance.right = 2
    else:
        personnel = mapper.mapped_table
        right_most_sibling = connection.scalar(
            select(personnel.c.rgt).where(
                personnel.c.emp == instance.parent.emp
            )
        )

        connection.execute(
            personnel.update()
            .where(personnel.c.rgt >= right_most_sibling)
            .values(
                lft=case(
                    (
                        personnel.c.lft > right_most_sibling,
                        personnel.c.lft + 2,
                    ),
                    else_=personnel.c.lft,
                ),
                rgt=case(
                    (
                        personnel.c.rgt >= right_most_sibling,
                        personnel.c.rgt + 2,
                    ),
                    else_=personnel.c.rgt,
                ),
            )
        )
        instance.left = right_most_sibling
        instance.right = right_most_sibling + 1

    # before_update() would be needed to support moving of nodes
    # after_delete() would be needed to support removal of nodes.

engine = create_engine("sqlite://", echo=True)

Base.metadata.create_all(engine)

session = Session(bind=engine)

albert = Employee(emp="Albert")
bert = Employee(emp="Bert")
chuck = Employee(emp="Chuck")
donna = Employee(emp="Donna")
eddie = Employee(emp="Eddie")
fred = Employee(emp="Fred")

bert.parent = albert
chuck.parent = albert
donna.parent = chuck
eddie.parent = chuck
fred.parent = chuck

# the order of "add" is important here.  elements must be added in
# the order in which they should be INSERTed.
session.add_all([albert, bert, chuck, donna, eddie, fred])
session.commit()

print(session.query(Employee).all())

# 1. Find an employee and all their supervisors, no matter how deep the tree.
ealias = aliased(Employee)
print(
    session.query(Employee)
    .filter(ealias.left.between(Employee.left, Employee.right))
    .filter(ealias.emp == "Eddie")
    .all()
)

# 2. Find the employee and all their subordinates.
# (This query has a nice symmetry with the first query.)
print(
    session.query(Employee)
    .filter(Employee.left.between(ealias.left, ealias.right))
    .filter(ealias.emp == "Chuck")
    .all()
)

# 3. Find the level of each node, so you can print the tree
# as an indented listing.
for indentation, employee in (
    session.query(func.count(Employee.emp).label("indentation") - 1, ealias)
    .filter(ealias.left.between(Employee.left, Employee.right))
    .group_by(ealias.emp)
    .order_by(ealias.left)
):
    print("    " * indentation + str(employee))
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.performance.bulk_inserts

```
from __future__ import annotations

from sqlalchemy import bindparam
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Identity
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from . import Profiler

"""This series of tests illustrates different ways to INSERT a large number
of rows in bulk.

"""

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

Profiler.init("bulk_inserts", num=100000)

@Profiler.setup
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

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

@Profiler.profile
def test_flush_pk_given(n):
    """Batched INSERT statements via the ORM, PKs already defined"""
    session = Session(bind=engine)
    for chunk in range(0, n, 1000):
        session.add_all(
            [
                Customer(
                    id=i + 1,
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                )
                for i in range(chunk, chunk + 1000)
            ]
        )
        session.flush()
    session.commit()

@Profiler.profile
def test_orm_bulk_insert(n):
    """Batched INSERT statements via the ORM in "bulk", not returning rows"""
    session = Session(bind=engine)
    session.execute(
        insert(Customer),
        [
            {
                "name": "customer name %d" % i,
                "description": "customer description %d" % i,
            }
            for i in range(n)
        ],
    )
    session.commit()

@Profiler.profile
def test_orm_insert_returning(n):
    """Batched INSERT statements via the ORM in "bulk", returning new Customer
    objects"""
    session = Session(bind=engine)

    customer_result = session.scalars(
        insert(Customer).returning(Customer),
        [
            {
                "name": "customer name %d" % i,
                "description": "customer description %d" % i,
            }
            for i in range(n)
        ],
    )

    # this step is where the rows actually become objects
    customers = customer_result.all()  # noqa: F841

    session.commit()

@Profiler.profile
def test_core_insert(n):
    """A single Core INSERT construct inserting mappings in bulk."""
    with engine.begin() as conn:
        conn.execute(
            Customer.__table__.insert(),
            [
                dict(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                )
                for i in range(n)
            ],
        )

@Profiler.profile
def test_dbapi_raw(n):
    """The DBAPI's API inserting rows in bulk."""

    conn = engine.pool._creator()
    cursor = conn.cursor()
    compiled = (
        Customer.__table__.insert()
        .values(name=bindparam("name"), description=bindparam("description"))
        .compile(dialect=engine.dialect)
    )

    if compiled.positional:
        args = (
            ("customer name %d" % i, "customer description %d" % i)
            for i in range(n)
        )
    else:
        args = (
            dict(
                name="customer name %d" % i,
                description="customer description %d" % i,
            )
            for i in range(n)
        )

    cursor.executemany(str(compiled), list(args))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    Profiler.main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.performance.bulk_updates

```
"""This series of tests will illustrate different ways to UPDATE a large number
of rows in bulk (under construction! there's just one test at the moment)

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Identity
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from . import Profiler

Base = declarative_base()
engine = None

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

Profiler.init("bulk_updates", num=100000)

@Profiler.setup
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    s = Session(engine)
    for chunk in range(0, num, 10000):
        s.bulk_insert_mappings(
            Customer,
            [
                {
                    "name": "customer name %d" % i,
                    "description": "customer description %d" % i,
                }
                for i in range(chunk, chunk + 10000)
            ],
        )
    s.commit()

@Profiler.profile
def test_orm_flush(n):
    """UPDATE statements via the ORM flush process."""
    session = Session(bind=engine)
    for chunk in range(0, n, 1000):
        customers = (
            session.query(Customer)
            .filter(Customer.id.between(chunk, chunk + 1000))
            .all()
        )
        for customer in customers:
            customer.description += "updated"
        session.flush()
    session.commit()
```
