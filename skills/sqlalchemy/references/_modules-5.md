# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_rows.versioned_rows_w_versionid

```
"""Illustrates a method to intercept changes on objects, turning
an UPDATE statement on a single row into an INSERT statement, so that a new
row is inserted with the new data, keeping the old row intact.

This example adds a numerical version_id to the Versioned class as well
as the ability to see which row is the most "current" version.

"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import attributes
from sqlalchemy.orm import backref
from sqlalchemy.orm import column_property
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

class Versioned:
    # we have a composite primary key consisting of "id"
    # and "version_id"
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, primary_key=True, default=1)

    # optional - add a persisted is_current_version column
    is_current_version = Column(Boolean, default=True)

    # optional - add a calculated is_current_version column
    @classmethod
    def __declare_last__(cls):
        alias = cls.__table__.alias()
        cls.calc_is_current_version = column_property(
            select(func.max(alias.c.version_id) == cls.version_id).where(
                alias.c.id == cls.id
            )
        )

    def new_version(self, session):
        # optional - set previous version to have is_current_version=False
        old_id = self.id
        session.query(self.__class__).filter_by(id=old_id).update(
            values=dict(is_current_version=False), synchronize_session=False
        )

        # make us transient (removes persistent
        # identity).
        make_transient(self)

        # increment version_id, which means we have a new PK.
        self.version_id += 1

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    for instance in session.dirty:
        if not isinstance(instance, Versioned):
            continue
        if not session.is_modified(instance):
            continue

        if not attributes.instance_state(instance).has_identity:
            continue

        # make it transient
        instance.new_version(session)

        # re-add
        session.add(instance)

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)

Session = sessionmaker(engine)

# example 1, simple versioning

class Example(Versioned, Base):
    __tablename__ = "example"
    data = Column(String)

Base.metadata.create_all(engine)

session = Session()
e1 = Example(id=1, data="e1")
session.add(e1)
session.commit()

e1.data = "e2"
session.commit()

assert session.query(
    Example.id,
    Example.version_id,
    Example.is_current_version,
    Example.calc_is_current_version,
    Example.data,
).order_by(Example.id, Example.version_id).all() == (
    [(1, 1, False, False, "e1"), (1, 2, True, True, "e2")]
)

# example 2, versioning with a parent

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer)
    child_version_id = Column(Integer)
    child = relationship("Child", backref=backref("parent", uselist=False))

    __table_args__ = (
        ForeignKeyConstraint(
            ["child_id", "child_version_id"], ["child.id", "child.version_id"]
        ),
    )

class Child(Versioned, Base):
    __tablename__ = "child"

    data = Column(String)

    def new_version(self, session):
        # expire parent's reference to us
        session.expire(self.parent, ["child"])

        # create new version
        Versioned.new_version(self, session)

        # re-add ourselves to the parent.  this causes the
        # parent foreign key to be updated also
        self.parent.child = self

Base.metadata.create_all(engine)

session = Session()

p1 = Parent(child=Child(id=1, data="c1"))
session.add(p1)
session.commit()

p1.child.data = "c2"
session.commit()

assert p1.child_id == 1
assert p1.child.version_id == 2

assert session.query(
    Child.id,
    Child.version_id,
    Child.is_current_version,
    Child.calc_is_current_version,
    Child.data,
).order_by(Child.id, Child.version_id).all() == (
    [(1, 1, False, False, "c1"), (1, 2, True, True, "c2")]
)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.versioned_rows.versioned_update_old_row

```
"""Illustrates the same UPDATE into INSERT technique of ``versioned_rows.py``,
but also emits an UPDATE on the **old** row to affect a change in timestamp.
Also includes a :meth:`.SessionEvents.do_orm_execute` hook to limit queries
to only the most recent version.

"""

import datetime
import time

from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import attributes
from sqlalchemy.orm import backref
from sqlalchemy.orm import make_transient
from sqlalchemy.orm import make_transient_to_detached
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import with_loader_criteria

Base = declarative_base()

# this will be the current time as the test runs
now = None

# in practice this would be a real "now" function
def current_time():
    return now

class VersionedStartEnd:
    start = Column(DateTime, primary_key=True)
    end = Column(DateTime, primary_key=True)

    def __init__(self, **kw):
        # reduce some verbosity when we make a new object
        kw.setdefault("start", current_time() - datetime.timedelta(days=3))
        kw.setdefault("end", current_time() + datetime.timedelta(days=3))
        super().__init__(**kw)

    def new_version(self, session):
        # our current identity key, which will be used on the "old"
        # version of us to emit an UPDATE. this is just for assertion purposes
        old_identity_key = inspect(self).key

        # make sure self.start / self.end are not expired
        self.id, self.start, self.end

        # turn us into an INSERT
        make_transient(self)

        # make the "old" version of us, which we will turn into an
        # UPDATE
        old_copy_of_us = self.__class__(
            id=self.id, start=self.start, end=self.end
        )

        # turn old_copy_of_us into an UPDATE
        make_transient_to_detached(old_copy_of_us)

        # the "old" object has our old identity key (that we no longer have)
        assert inspect(old_copy_of_us).key == old_identity_key

        # now put it back in the session
        session.add(old_copy_of_us)

        # now update the 'end' - SQLAlchemy sees this as a PK switch
        old_copy_of_us.end = current_time()

        # fun fact!  the new_version() routine is *not* called for
        # old_copy_of_us!  because we are already in the before_flush() hook!
        # this surprised even me.   I was thinking we had to guard against
        # it.  Still might be a good idea to do so.

        self.start = current_time()
        self.end = current_time() + datetime.timedelta(days=2)

@event.listens_for(Session, "before_flush")
def before_flush(session, flush_context, instances):
    for instance in session.dirty:
        if not isinstance(instance, VersionedStartEnd):
            continue
        if not session.is_modified(instance):
            continue

        if not attributes.instance_state(instance).has_identity:
            continue

        # make it transient
        instance.new_version(session)
        # re-add
        session.add(instance)

@event.listens_for(Session, "do_orm_execute", retval=True)
def do_orm_execute(execute_state):
    """ensure all queries for VersionedStartEnd include criteria"""

    ct = current_time() + datetime.timedelta(seconds=1)
    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(
            VersionedStartEnd,
            lambda cls: and_(ct > cls.start, ct < cls.end),
            include_aliases=True,
        )
    )

class Parent(VersionedStartEnd, Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime, primary_key=True)
    end = Column(DateTime, primary_key=True)
    data = Column(String)

    child_n = Column(Integer)

    child = relationship(
        "Child",
        primaryjoin=("Child.id == foreign(Parent.child_n)"),
        # note the primaryjoin can also be:
        #
        #  "and_(Child.id == foreign(Parent.child_n), "
        #  "func.now().between(Child.start, Child.end))"
        #
        # however the before_compile() above will take care of this for us in
        # all cases except for joinedload.  You *can* use the above primaryjoin
        # as well, it just means the criteria will be present twice for most
        # parent->child load operations
        #
        uselist=False,
        backref=backref("parent", uselist=False),
    )

class Child(VersionedStartEnd, Base):
    __tablename__ = "child"

    id = Column(Integer, primary_key=True)
    start = Column(DateTime, primary_key=True)
    end = Column(DateTime, primary_key=True)
    data = Column(String)

    def new_version(self, session):
        # expire parent's reference to us
        session.expire(self.parent, ["child"])

        # create new version
        VersionedStartEnd.new_version(self, session)

        # re-add ourselves to the parent
        self.parent.child = self

times = []

def time_passes(s):
    """keep track of timestamps in terms of the database and allow time to
    pass between steps."""

    # close the transaction, if any, since PG time doesn't increment in the
    # transaction
    s.commit()

    # get "now" in terms of the DB so we can keep the ranges low and
    # still have our assertions pass
    if times:
        time.sleep(1)

    times.append(datetime.datetime.now())

    if len(times) > 1:
        assert times[-1] > times[-2]
    return times[-1]

e = create_engine("sqlite://", echo="debug")
Base.metadata.create_all(e)

s = Session(e)

now = time_passes(s)

c1 = Child(id=1, data="child 1")
p1 = Parent(id=1, data="c1", child=c1)

s.add(p1)
s.commit()

# assert raw DB data
assert s.query(Parent.__table__).all() == [
    (
        1,
        times[0] - datetime.timedelta(days=3),
        times[0] + datetime.timedelta(days=3),
        "c1",
        1,
    )
]
assert s.query(Child.__table__).all() == [
    (
        1,
        times[0] - datetime.timedelta(days=3),
        times[0] + datetime.timedelta(days=3),
        "child 1",
    )
]

now = time_passes(s)

p1_check = s.query(Parent).first()
assert p1_check is p1
assert p1_check.child is c1

p1.child.data = "elvis presley"

s.commit()

p2_check = s.query(Parent).first()
assert p2_check is p1_check
c2_check = p2_check.child

# same object
assert p2_check.child is c1

# new data
assert c1.data == "elvis presley"

# new end time
assert c1.end == now + datetime.timedelta(days=2)

# assert raw DB data
assert s.query(Parent.__table__).all() == [
    (
        1,
        times[0] - datetime.timedelta(days=3),
        times[0] + datetime.timedelta(days=3),
        "c1",
        1,
    )
]
assert s.query(Child.__table__).order_by(Child.end).all() == [
    (1, times[0] - datetime.timedelta(days=3), times[1], "child 1"),
    (1, times[1], times[1] + datetime.timedelta(days=2), "elvis presley"),
]

now = time_passes(s)

p1.data = "c2 elvis presley"

s.commit()

# assert raw DB data.  now there are two parent rows.
assert s.query(Parent.__table__).order_by(Parent.end).all() == [
    (1, times[0] - datetime.timedelta(days=3), times[2], "c1", 1),
    (
        1,
        times[2],
        times[2] + datetime.timedelta(days=2),
        "c2 elvis presley",
        1,
    ),
]
assert s.query(Child.__table__).order_by(Child.end).all() == [
    (1, times[0] - datetime.timedelta(days=3), times[1], "child 1"),
    (1, times[1], times[1] + datetime.timedelta(days=2), "elvis presley"),
]

# add some more rows to test that these aren't coming back for
# queries
s.add(Parent(id=2, data="unrelated", child=Child(id=2, data="unrelated")))
s.commit()

# Query only knows about one parent for id=1
p3_check = s.query(Parent).filter_by(id=1).one()

assert p3_check is p1
assert p3_check.child is c1

# and one child.
c3_check = s.query(Child).filter(Child.parent == p3_check).one()
assert c3_check is c1

# one child one parent....
c3_check = (
    s.query(Child).join(Parent.child).filter(Parent.id == p3_check.id).one()
)
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.vertical.dictlike-polymorphic

```
"""Mapping a polymorphic-valued vertical table as a dictionary.

Builds upon the dictlike.py example to also add differently typed
columns to the "fact" table, e.g.::

  Table(
      "properties",
      metadata,
      Column("owner_id", Integer, ForeignKey("owner.id"), primary_key=True),
      Column("key", UnicodeText),
      Column("type", Unicode(16)),
      Column("int_value", Integer),
      Column("char_value", UnicodeText),
      Column("bool_value", Boolean),
      Column("decimal_value", Numeric(10, 2)),
  )

For any given properties row, the value of the 'type' column will point to the
'_value' column active for that row.

This example approach uses exactly the same dict mapping approach as the
'dictlike' example.  It only differs in the mapping for vertical rows.  Here,
we'll use a @hybrid_property to build a smart '.value' attribute that wraps up
reading and writing those various '_value' columns and keeps the '.type' up to
date.

"""

from sqlalchemy import and_
from sqlalchemy import Boolean
from sqlalchemy import case
from sqlalchemy import cast
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import literal_column
from sqlalchemy import null
from sqlalchemy import or_
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_keyed_dict
from sqlalchemy.orm.interfaces import PropComparator
from .dictlike import ProxiedDictMixin

class PolymorphicVerticalProperty:
    """A key/value pair with polymorphic value storage.

    The class which is mapped should indicate typing information
    within the "info" dictionary of mapped Column objects; see
    the AnimalFact mapping below for an example.

    """

    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    @hybrid_property
    def value(self):
        fieldname, discriminator = self.type_map[self.type]
        if fieldname is None:
            return None
        else:
            return getattr(self, fieldname)

    @value.setter
    def value(self, value):
        py_type = type(value)
        fieldname, discriminator = self.type_map[py_type]

        self.type = discriminator
        if fieldname is not None:
            setattr(self, fieldname, value)

    @value.deleter
    def value(self):
        self._set_value(None)

    @value.comparator
    class value(PropComparator):
        """A comparator for .value, builds a polymorphic comparison
        via CASE."""

        def __init__(self, cls):
            self.cls = cls

        def _case(self):
            pairs = set(self.cls.type_map.values())
            whens = [
                (
                    literal_column("'%s'" % discriminator),
                    cast(getattr(self.cls, attribute), String),
                )
                for attribute, discriminator in pairs
                if attribute is not None
            ]
            return case(*whens, value=self.cls.type, else_=null())

        def __eq__(self, other):
            return self._case() == cast(other, String)

        def __ne__(self, other):
            return self._case() != cast(other, String)

    def __repr__(self):
        return "<%s %r=%r>" % (self.__class__.__name__, self.key, self.value)

@event.listens_for(
    PolymorphicVerticalProperty, "mapper_configured", propagate=True
)
def on_new_class(mapper, cls_):
    """Look for Column objects with type info in them, and work up
    a lookup table."""

    info_dict = {}
    info_dict[type(None)] = (None, "none")
    info_dict["none"] = (None, "none")

    for k in mapper.c.keys():
        col = mapper.c[k]
        if "type" in col.info:
            python_type, discriminator = col.info["type"]
            info_dict[python_type] = (k, discriminator)
            info_dict[discriminator] = (k, discriminator)
    cls_.type_map = info_dict

if __name__ == "__main__":
    Base = declarative_base()

    class AnimalFact(PolymorphicVerticalProperty, Base):
        """A fact about an animal."""

        __tablename__ = "animal_fact"

        animal_id = Column(ForeignKey("animal.id"), primary_key=True)
        key = Column(Unicode(64), primary_key=True)
        type = Column(Unicode(16))

        # add information about storage for different types
        # in the info dictionary of Columns
        int_value = Column(Integer, info={"type": (int, "integer")})
        char_value = Column(UnicodeText, info={"type": (str, "string")})
        boolean_value = Column(Boolean, info={"type": (bool, "boolean")})

    class Animal(ProxiedDictMixin, Base):
        """an Animal"""

        __tablename__ = "animal"

        id = Column(Integer, primary_key=True)
        name = Column(Unicode(100))

        facts = relationship(
            "AnimalFact", collection_class=attribute_keyed_dict("key")
        )

        _proxied = association_proxy(
            "facts",
            "value",
            creator=lambda key, value: AnimalFact(key=key, value=value),
        )

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return "Animal(%r)" % self.name

        @classmethod
        def with_characteristic(self, key, value):
            return self.facts.any(key=key, value=value)

    engine = create_engine("sqlite://", echo=True)

    Base.metadata.create_all(engine)
    session = Session(engine)

    stoat = Animal("stoat")
    stoat["color"] = "red"
    stoat["cuteness"] = 7
    stoat["weasel-like"] = True

    session.add(stoat)
    session.commit()

    critter = session.query(Animal).filter(Animal.name == "stoat").one()
    print(critter["color"])
    print(critter["cuteness"])

    print("changing cuteness value and type:")
    critter["cuteness"] = "very cute"

    session.commit()

    marten = Animal("marten")
    marten["cuteness"] = 5
    marten["weasel-like"] = True
    marten["poisonous"] = False
    session.add(marten)

    shrew = Animal("shrew")
    shrew["cuteness"] = 5
    shrew["weasel-like"] = False
    shrew["poisonous"] = True

    session.add(shrew)
    session.commit()

    q = session.query(Animal).filter(
        Animal.facts.any(
            and_(AnimalFact.key == "weasel-like", AnimalFact.value == True)
        )
    )
    print("weasel-like animals", q.all())

    q = session.query(Animal).filter(
        Animal.with_characteristic("weasel-like", True)
    )
    print("weasel-like animals again", q.all())

    q = session.query(Animal).filter(
        Animal.with_characteristic("poisonous", False)
    )
    print("animals with poisonous=False", q.all())

    q = session.query(Animal).filter(
        or_(
            Animal.with_characteristic("poisonous", False),
            ~Animal.facts.any(AnimalFact.key == "poisonous"),
        )
    )
    print("non-poisonous animals", q.all())

    q = session.query(Animal).filter(Animal.facts.any(AnimalFact.value == 5))
    print("any animal with a .value of 5", q.all())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.vertical.dictlike

```
"""Mapping a vertical table as a dictionary.

This example illustrates accessing and modifying a "vertical" (or
"properties", or pivoted) table via a dict-like interface.  These are tables
that store free-form object properties as rows instead of columns.  For
example, instead of::

  # A regular ("horizontal") table has columns for 'species' and 'size'
  Table(
      "animal",
      metadata,
      Column("id", Integer, primary_key=True),
      Column("species", Unicode),
      Column("size", Unicode),
  )

A vertical table models this as two tables: one table for the base or parent
entity, and another related table holding key/value pairs::

  Table("animal", metadata, Column("id", Integer, primary_key=True))

  # The properties table will have one row for a 'species' value, and
  # another row for the 'size' value.
  Table(
      "properties",
      metadata,
      Column(
          "animal_id", Integer, ForeignKey("animal.id"), primary_key=True
      ),
      Column("key", UnicodeText),
      Column("value", UnicodeText),
  )

Because the key/value pairs in a vertical scheme are not fixed in advance,
accessing them like a Python dict can be very convenient.  The example below
can be used with many common vertical schemas as-is or with minor adaptations.

"""

from sqlalchemy import and_
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_keyed_dict

class ProxiedDictMixin:
    """Adds obj[key] access to a mapped class.

    This class basically proxies dictionary access to an attribute
    called ``_proxied``.  The class which inherits this class
    should have an attribute called ``_proxied`` which points to a dictionary.

    """

    def __len__(self):
        return len(self._proxied)

    def __iter__(self):
        return iter(self._proxied)

    def __getitem__(self, key):
        return self._proxied[key]

    def __contains__(self, key):
        return key in self._proxied

    def __setitem__(self, key, value):
        self._proxied[key] = value

    def __delitem__(self, key):
        del self._proxied[key]

if __name__ == "__main__":
    Base = declarative_base()

    class AnimalFact(Base):
        """A fact about an animal."""

        __tablename__ = "animal_fact"

        animal_id = Column(ForeignKey("animal.id"), primary_key=True)
        key = Column(Unicode(64), primary_key=True)
        value = Column(UnicodeText)

    class Animal(ProxiedDictMixin, Base):
        """an Animal"""

        __tablename__ = "animal"

        id = Column(Integer, primary_key=True)
        name = Column(Unicode(100))

        facts = relationship(
            "AnimalFact", collection_class=attribute_keyed_dict("key")
        )

        _proxied = association_proxy(
            "facts",
            "value",
            creator=lambda key, value: AnimalFact(key=key, value=value),
        )

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return "Animal(%r)" % self.name

        @classmethod
        def with_characteristic(self, key, value):
            return self.facts.any(key=key, value=value)

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    stoat = Animal("stoat")
    stoat["color"] = "reddish"
    stoat["cuteness"] = "somewhat"

    # dict-like assignment transparently creates entries in the
    # stoat.facts collection:
    print(stoat.facts["color"])

    session.add(stoat)
    session.commit()

    critter = session.query(Animal).filter(Animal.name == "stoat").one()
    print(critter["color"])
    print(critter["cuteness"])

    critter["cuteness"] = "very"

    print("changing cuteness:")

    marten = Animal("marten")
    marten["color"] = "brown"
    marten["cuteness"] = "somewhat"
    session.add(marten)

    shrew = Animal("shrew")
    shrew["cuteness"] = "somewhat"
    shrew["poisonous-part"] = "saliva"
    session.add(shrew)

    loris = Animal("slow loris")
    loris["cuteness"] = "fairly"
    loris["poisonous-part"] = "elbows"
    session.add(loris)

    q = session.query(Animal).filter(
        Animal.facts.any(
            and_(AnimalFact.key == "color", AnimalFact.value == "reddish")
        )
    )
    print("reddish animals", q.all())

    q = session.query(Animal).filter(
        Animal.with_characteristic("color", "brown")
    )
    print("brown animals", q.all())

    q = session.query(Animal).filter(
        ~Animal.with_characteristic("poisonous-part", "elbows")
    )
    print("animals without poisonous-part == elbows", q.all())

    q = session.query(Animal).filter(Animal.facts.any(value="somewhat"))
    print('any animal with any .value of "somewhat"', q.all())
```
