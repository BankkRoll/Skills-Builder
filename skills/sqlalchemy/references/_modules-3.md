# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Source code for examples.performance.large_resultsets

```
"""In this series of tests, we are looking at time to load a large number
of very small and simple rows.

A special test here illustrates the difference between fetching the
rows from the raw DBAPI and throwing them away, vs. assembling each
row into a completely basic Python object and appending to a list. The
time spent typically more than doubles.  The point is that while
DBAPIs will give you raw rows very fast if they are written in C, the
moment you do anything with those rows, even something trivial,
overhead grows extremely fast in cPython. SQLAlchemy's Core and
lighter-weight ORM options add absolutely minimal overhead, and the
full blown ORM doesn't do terribly either even though mapped objects
provide a huge amount of functionality.

"""

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Identity
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Bundle
from sqlalchemy.orm import Session
from . import Profiler

Base = declarative_base()
engine = None

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

Profiler.init("large_resultsets", num=500000)

@Profiler.setup_once
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    s = Session(engine)
    for chunk in range(0, num, 10000):
        s.execute(
            Customer.__table__.insert(),
            params=[
                {
                    "name": "customer name %d" % i,
                    "description": "customer description %d" % i,
                }
                for i in range(chunk, chunk + 10000)
            ],
        )
    s.commit()

@Profiler.profile
def test_orm_full_objects_list(n):
    """Load fully tracked ORM objects into one big list()."""

    sess = Session(engine)
    list(sess.query(Customer).limit(n))

@Profiler.profile
def test_orm_full_objects_chunks(n):
    """Load fully tracked ORM objects a chunk at a time using yield_per()."""

    sess = Session(engine)
    for obj in sess.query(Customer).yield_per(1000).limit(n):
        pass

@Profiler.profile
def test_orm_bundles(n):
    """Load lightweight "bundle" objects using the ORM."""

    sess = Session(engine)
    bundle = Bundle(
        "customer", Customer.id, Customer.name, Customer.description
    )
    for row in sess.query(bundle).yield_per(10000).limit(n):
        pass

@Profiler.profile
def test_orm_columns(n):
    """Load individual columns into named tuples using the ORM."""

    sess = Session(engine)
    for row in (
        sess.query(Customer.id, Customer.name, Customer.description)
        .yield_per(10000)
        .limit(n)
    ):
        pass

@Profiler.profile
def test_core_fetchall(n):
    """Load Core result rows using fetchall."""

    with engine.connect() as conn:
        result = conn.execute(Customer.__table__.select().limit(n)).fetchall()
        for row in result:
            row.id, row.name, row.description

@Profiler.profile
def test_core_fetchall_mapping(n):
    """Load Core result rows using fetchall."""

    with engine.connect() as conn:
        result = (
            conn.execute(Customer.__table__.select().limit(n))
            .mappings()
            .fetchall()
        )
        for row in result:
            row["id"], row["name"], row["description"]

@Profiler.profile
def test_core_fetchmany_w_streaming(n):
    """Load Core result rows using fetchmany/streaming."""

    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(
            Customer.__table__.select().limit(n)
        )
        while True:
            chunk = result.fetchmany(10000)
            if not chunk:
                break
            for row in chunk:
                row.id, row.name, row.description

@Profiler.profile
def test_core_fetchmany(n):
    """Load Core result rows using Core / fetchmany."""

    with engine.connect() as conn:
        result = conn.execute(Customer.__table__.select().limit(n))
        while True:
            chunk = result.fetchmany(10000)
            if not chunk:
                break
            for row in chunk:
                row.id, row.name, row.description

@Profiler.profile
def test_dbapi_fetchall_plus_append_objects(n):
    """Load rows using DBAPI fetchall(), generate an object for each row."""

    _test_dbapi_raw(n, True)

@Profiler.profile
def test_dbapi_fetchall_no_object(n):
    """Load rows using DBAPI fetchall(), don't make any objects."""

    _test_dbapi_raw(n, False)

def _test_dbapi_raw(n, make_objects):
    compiled = (
        Customer.__table__.select()
        .limit(n)
        .compile(
            dialect=engine.dialect, compile_kwargs={"literal_binds": True}
        )
    )

    if make_objects:
        # because if you're going to roll your own, you're probably
        # going to do this, so see how this pushes you right back into
        # ORM land anyway :)
        class SimpleCustomer:
            def __init__(self, id_, name, description):
                self.id_ = id_
                self.name = name
                self.description = description

    sql = str(compiled)

    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    if make_objects:
        for row in cursor.fetchall():
            # ensure that we fully fetch!
            SimpleCustomer(id_=row[0], name=row[1], description=row[2])
    else:
        for row in cursor.fetchall():
            # ensure that we fully fetch!
            row[0], row[1], row[2]

    conn.close()

if __name__ == "__main__":
    Profiler.main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.performance.short_selects

```
"""This series of tests illustrates different ways to SELECT a single
record by primary key

"""

import random

from sqlalchemy import bindparam
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Identity
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select as future_select
from sqlalchemy.orm import deferred
from sqlalchemy.orm import Session
from . import Profiler

Base = declarative_base()
engine = None

ids = range(1, 11000)

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    q = Column(Integer)
    p = Column(Integer)
    x = deferred(Column(Integer))
    y = deferred(Column(Integer))
    z = deferred(Column(Integer))

Profiler.init("short_selects", num=10000)

@Profiler.setup
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo, query_cache_size=0)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    sess = Session(engine)
    sess.add_all(
        [
            Customer(
                id=i,
                name="c%d" % i,
                description="c%d" % i,
                q=i * 10,
                p=i * 20,
                x=i * 30,
                y=i * 40,
            )
            for i in ids
        ]
    )
    sess.commit()

@Profiler.profile
def test_orm_query_classic_style(n):
    """classic ORM query of the full entity, no cache"""
    session = Session(bind=engine)
    for id_ in random.sample(ids, n):
        session.query(Customer).filter(Customer.id == id_).one()

@Profiler.profile
def test_orm_query_classic_style_w_cache(n):
    """classic ORM query of the full entity, using cache"""
    cache = {}
    session = Session(bind=engine.execution_options(compiled_cache=cache))
    for id_ in random.sample(ids, n):
        session.query(Customer).filter(Customer.id == id_).one()

@Profiler.profile
def test_orm_query_new_style(n):
    """new style ORM select() of the full entity, no cache."""

    session = Session(bind=engine)
    for id_ in random.sample(ids, n):
        stmt = future_select(Customer).where(Customer.id == id_)
        session.execute(stmt).scalar_one()

@Profiler.profile
def test_orm_query_new_style_cache(n):
    """new style ORM select() of the full entity, using cache."""

    cache = {}
    session = Session(bind=engine.execution_options(compiled_cache=cache))
    for id_ in random.sample(ids, n):
        stmt = future_select(Customer).where(Customer.id == id_)
        session.execute(stmt).scalar_one()

@Profiler.profile
def test_orm_query_classic_style_cols_only(n):
    """classic ORM query against columns, no cache"""
    session = Session(bind=engine)
    for id_ in random.sample(ids, n):
        session.query(Customer.id, Customer.name, Customer.description).filter(
            Customer.id == id_
        ).one()

@Profiler.profile
def test_orm_query_classic_style_cols_only_cache(n):
    """classic ORM query against columns, using cache"""
    cache = {}
    session = Session(bind=engine.execution_options(compiled_cache=cache))
    for id_ in random.sample(ids, n):
        session.query(Customer.id, Customer.name, Customer.description).filter(
            Customer.id == id_
        ).one()

@Profiler.profile
def test_core_new_stmt_each_time(n):
    """test core, creating a new statement each time, no cache"""

    with engine.connect() as conn:
        for id_ in random.sample(ids, n):
            stmt = select(Customer.__table__).where(Customer.id == id_)
            row = conn.execute(stmt).first()
            tuple(row)

@Profiler.profile
def test_core_new_stmt_each_time_compiled_cache(n):
    """test core, creating a new statement each time, using cache"""

    compiled_cache = {}
    with engine.connect().execution_options(
        compiled_cache=compiled_cache
    ) as conn:
        for id_ in random.sample(ids, n):
            stmt = select(Customer.__table__).where(Customer.id == id_)
            row = conn.execute(stmt).first()
            tuple(row)

@Profiler.profile
def test_core_reuse_stmt(n):
    """test core, reusing the same statement, no cache"""

    stmt = select(Customer.__table__).where(Customer.id == bindparam("id"))
    with engine.connect() as conn:
        for id_ in random.sample(ids, n):
            row = conn.execute(stmt, {"id": id_}).first()
            tuple(row)

@Profiler.profile
def test_core_reuse_stmt_compiled_cache(n):
    """test core, reusing the same statement, using cache"""

    stmt = select(Customer.__table__).where(Customer.id == bindparam("id"))
    compiled_cache = {}
    with engine.connect().execution_options(
        compiled_cache=compiled_cache
    ) as conn:
        for id_ in random.sample(ids, n):
            row = conn.execute(stmt, {"id": id_}).first()
            tuple(row)

if __name__ == "__main__":
    Profiler.main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.performance.single_inserts

```
"""In this series of tests, we're looking at a method that inserts a row
within a distinct transaction, and afterwards returns to essentially a
"closed" state.   This would be analogous to an API call that starts up
a database connection, inserts the row, commits and closes.

"""

from sqlalchemy import bindparam
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Identity
from sqlalchemy import Integer
from sqlalchemy import pool
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

Profiler.init("single_inserts", num=10000)

@Profiler.setup
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    if engine.dialect.name == "sqlite":
        engine.pool = pool.StaticPool(creator=engine.pool._creator)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

@Profiler.profile
def test_orm_commit(n):
    """Individual INSERT/COMMIT pairs via the ORM"""

    for i in range(n):
        session = Session(bind=engine)
        session.add(
            Customer(
                name="customer name %d" % i,
                description="customer description %d" % i,
            )
        )
        session.commit()

@Profiler.profile
def test_bulk_save(n):
    """Individual INSERT/COMMIT pairs using the "bulk" API"""

    for i in range(n):
        session = Session(bind=engine)
        session.bulk_save_objects(
            [
                Customer(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                )
            ]
        )
        session.commit()

@Profiler.profile
def test_bulk_insert_dictionaries(n):
    """Individual INSERT/COMMIT pairs using the "bulk" API with dictionaries"""

    for i in range(n):
        session = Session(bind=engine)
        session.bulk_insert_mappings(
            Customer,
            [
                dict(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                )
            ],
        )
        session.commit()

@Profiler.profile
def test_core(n):
    """Individual INSERT/COMMIT pairs using Core."""

    for i in range(n):
        with engine.begin() as conn:
            conn.execute(
                Customer.__table__.insert(),
                dict(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                ),
            )

@Profiler.profile
def test_core_query_caching(n):
    """Individual INSERT/COMMIT pairs using Core with query caching"""

    cache = {}
    ins = Customer.__table__.insert()
    for i in range(n):
        with engine.begin() as conn:
            conn.execution_options(compiled_cache=cache).execute(
                ins,
                dict(
                    name="customer name %d" % i,
                    description="customer description %d" % i,
                ),
            )

@Profiler.profile
def test_dbapi_raw_w_connect(n):
    """Individual INSERT/COMMIT pairs w/ DBAPI + connection each time"""

    _test_dbapi_raw(n, True)

@Profiler.profile
def test_dbapi_raw_w_pool(n):
    """Individual INSERT/COMMIT pairs w/ DBAPI + connection pool"""

    _test_dbapi_raw(n, False)

def _test_dbapi_raw(n, connect):
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
    sql = str(compiled)

    if connect:
        for arg in args:
            # there's no connection pool, so if these were distinct
            # calls, we'd be connecting each time
            conn = engine.pool._creator()
            cursor = conn.cursor()
            cursor.execute(sql, arg)
            cursor.lastrowid
            conn.commit()
            conn.close()
    else:
        for arg in args:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            cursor.execute(sql, arg)
            cursor.lastrowid
            conn.commit()
            conn.close()

if __name__ == "__main__":
    Profiler.main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.sharding.asyncio

```
"""Illustrates sharding API used with asyncio.

For the sync version of this example, see separate_databases.py.

Most of the code here is copied from separate_databases.py and works
in exactly the same way.   The main change is how the
``async_sessionmaker`` is configured, and as is specific to this example
the routine that generates new primary keys.

"""

from __future__ import annotations

import asyncio
import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import immediateload
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import operators
from sqlalchemy.sql import visitors

echo = True
db1 = create_async_engine("sqlite+aiosqlite://", echo=echo)
db2 = create_async_engine("sqlite+aiosqlite://", echo=echo)
db3 = create_async_engine("sqlite+aiosqlite://", echo=echo)
db4 = create_async_engine("sqlite+aiosqlite://", echo=echo)

# for asyncio, the ShardedSession class is passed
# via sync_session_class.  The shards themselves are used within
# implicit-awaited internals, so we use the sync_engine Engine objects
# in the shards dictionary.
Session = async_sessionmaker(
    sync_session_class=ShardedSession,
    expire_on_commit=False,
    shards={
        "north_america": db1.sync_engine,
        "asia": db2.sync_engine,
        "europe": db3.sync_engine,
        "south_america": db4.sync_engine,
    },
)

# mappings and tables
class Base(DeclarativeBase):
    pass

# we need a way to create identifiers which are unique across all databases.
# one easy way would be to just use a composite primary key, where  one value
# is the shard id.  but here, we'll show something more "generic", an id
# generation function.  we'll use a simplistic "id table" stored in database
# #1.  Any other method will do just as well; UUID, hilo, application-specific,
# etc.

ids = Table("ids", Base.metadata, Column("nextid", Integer, nullable=False))

def id_generator(ctx):
    # id_generator is run within a "synchronous" context, where
    # we use an implicit-await API that will convert back to explicit await
    # calls when it reaches the driver.
    with db1.sync_engine.begin() as conn:
        nextid = conn.scalar(ids.select().with_for_update())
        conn.execute(ids.update().values({ids.c.nextid: ids.c.nextid + 1}))
    return nextid

# table setup.  we'll store a lead table of continents/cities, and a secondary
# table storing locations. a particular row will be placed in the database
# whose shard id corresponds to the 'continent'.  in this setup, secondary rows
# in 'weather_reports' will be placed in the same DB as that of the parent, but
# this can be changed if you're willing to write more complex sharding
# functions.

class WeatherLocation(Base):
    __tablename__ = "weather_locations"

    id: Mapped[int] = mapped_column(primary_key=True, default=id_generator)
    continent: Mapped[str]
    city: Mapped[str]

    reports: Mapped[list[Report]] = relationship(back_populates="location")

    def __init__(self, continent: str, city: str):
        self.continent = continent
        self.city = city

class Report(Base):
    __tablename__ = "weather_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("weather_locations.id")
    )
    temperature: Mapped[float]
    report_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    location: Mapped[WeatherLocation] = relationship(back_populates="reports")

    def __init__(self, temperature: float):
        self.temperature = temperature

# step 5. define sharding functions.

# we'll use a straight mapping of a particular set of "country"
# attributes to shard id.
shard_lookup = {
    "North America": "north_america",
    "Asia": "asia",
    "Europe": "europe",
    "South America": "south_america",
}

def shard_chooser(mapper, instance, clause=None):
    """shard chooser.

    looks at the given instance and returns a shard id
    note that we need to define conditions for
    the WeatherLocation class, as well as our secondary Report class which will
    point back to its WeatherLocation via its 'location' attribute.

    """
    if isinstance(instance, WeatherLocation):
        return shard_lookup[instance.continent]
    else:
        return shard_chooser(mapper, instance.location)

def identity_chooser(mapper, primary_key, *, lazy_loaded_from, **kw):
    """identity chooser.

    given a primary key, returns a list of shards
    to search.  here, we don't have any particular information from a
    pk so we just return all shard ids. often, you'd want to do some
    kind of round-robin strategy here so that requests are evenly
    distributed among DBs.

    """
    if lazy_loaded_from:
        # if we are in a lazy load, we can look at the parent object
        # and limit our search to that same shard, assuming that's how we've
        # set things up.
        return [lazy_loaded_from.identity_token]
    else:
        return ["north_america", "asia", "europe", "south_america"]

def execute_chooser(context):
    """statement execution chooser.

    this also returns a list of shard ids, which can just be all of them. but
    here we'll search into the execution context in order to try to narrow down
    the list of shards to SELECT.

    """
    ids = []

    # we'll grab continent names as we find them
    # and convert to shard ids
    for column, operator, value in _get_select_comparisons(context.statement):
        # "shares_lineage()" returns True if both columns refer to the same
        # statement column, adjusting for any annotations present.
        # (an annotation is an internal clone of a Column object
        # and occur when using ORM-mapped attributes like
        # "WeatherLocation.continent"). A simpler comparison, though less
        # accurate, would be "column.key == 'continent'".
        if column.shares_lineage(WeatherLocation.__table__.c.continent):
            if operator == operators.eq:
                ids.append(shard_lookup[value])
            elif operator == operators.in_op:
                ids.extend(shard_lookup[v] for v in value)

    if len(ids) == 0:
        return ["north_america", "asia", "europe", "south_america"]
    else:
        return ids

def _get_select_comparisons(statement):
    """Search a Select or Query object for binary expressions.

    Returns expressions which match a Column against one or more
    literal values as a list of tuples of the form
    (column, operator, values).   "values" is a single value
    or tuple of values depending on the operator.

    """
    binds = {}
    clauses = set()
    comparisons = []

    def visit_bindparam(bind):
        # visit a bind parameter.

        value = bind.effective_value
        binds[bind] = value

    def visit_column(column):
        clauses.add(column)

    def visit_binary(binary):
        if binary.left in clauses and binary.right in binds:
            comparisons.append(
                (binary.left, binary.operator, binds[binary.right])
            )

        elif binary.left in binds and binary.right in clauses:
            comparisons.append(
                (binary.right, binary.operator, binds[binary.left])
            )

    # here we will traverse through the query's criterion, searching
    # for SQL constructs.  We will place simple column comparisons
    # into a list.
    if statement.whereclause is not None:
        visitors.traverse(
            statement.whereclause,
            {},
            {
                "bindparam": visit_bindparam,
                "binary": visit_binary,
                "column": visit_column,
            },
        )
    return comparisons

# further configure create_session to use these functions
Session.configure(
    shard_chooser=shard_chooser,
    identity_chooser=identity_chooser,
    execute_chooser=execute_chooser,
)

async def setup():
    # create tables
    for db in (db1, db2, db3, db4):
        async with db.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # establish initial "id" in db1
    async with db1.begin() as conn:
        await conn.execute(ids.insert(), {"nextid": 1})

async def main():
    await setup()

    # save and load objects!

    tokyo = WeatherLocation("Asia", "Tokyo")
    newyork = WeatherLocation("North America", "New York")
    toronto = WeatherLocation("North America", "Toronto")
    london = WeatherLocation("Europe", "London")
    dublin = WeatherLocation("Europe", "Dublin")
    brasilia = WeatherLocation("South America", "Brasila")
    quito = WeatherLocation("South America", "Quito")

    tokyo.reports.append(Report(80.0))
    newyork.reports.append(Report(75))
    quito.reports.append(Report(85))

    async with Session() as sess:
        sess.add_all(
            [tokyo, newyork, toronto, london, dublin, brasilia, quito]
        )

        await sess.commit()

        t = await sess.get(
            WeatherLocation,
            tokyo.id,
            options=[immediateload(WeatherLocation.reports)],
        )
        assert t.city == tokyo.city
        assert t.reports[0].temperature == 80.0

        # select across shards
        asia_and_europe = (
            await sess.execute(
                select(WeatherLocation).filter(
                    WeatherLocation.continent.in_(["Europe", "Asia"])
                )
            )
        ).scalars()

        assert {c.city for c in asia_and_europe} == {
            "Tokyo",
            "London",
            "Dublin",
        }

        # optionally set a shard id for the query and all related loaders
        north_american_cities_w_t = (
            await sess.execute(
                select(WeatherLocation)
                .filter(WeatherLocation.city.startswith("T"))
                .options(set_shard_id("north_america"))
            )
        ).scalars()

        # Tokyo not included since not in the north_america shard
        assert {c.city for c in north_american_cities_w_t} == {
            "Toronto",
        }

        # the Report class uses a simple integer primary key.  So across two
        # databases, a primary key will be repeated.  The "identity_token"
        # tracks in memory that these two identical primary keys are local to
        # different shards.
        newyork_report = newyork.reports[0]
        tokyo_report = tokyo.reports[0]

        assert inspect(newyork_report).identity_key == (
            Report,
            (1,),
            "north_america",
        )
        assert inspect(tokyo_report).identity_key == (Report, (1,), "asia")

        # the token representing the originating shard is also available
        # directly
        assert inspect(newyork_report).identity_token == "north_america"
        assert inspect(tokyo_report).identity_token == "asia"

if __name__ == "__main__":
    asyncio.run(main())
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.sharding.separate_databases

```
"""Illustrates sharding using distinct SQLite databases."""

from __future__ import annotations

import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import operators
from sqlalchemy.sql import visitors

echo = True
db1 = create_engine("sqlite://", echo=echo)
db2 = create_engine("sqlite://", echo=echo)
db3 = create_engine("sqlite://", echo=echo)
db4 = create_engine("sqlite://", echo=echo)

# create session function.  this binds the shard ids
# to databases within a ShardedSession and returns it.
Session = sessionmaker(
    class_=ShardedSession,
    shards={
        "north_america": db1,
        "asia": db2,
        "europe": db3,
        "south_america": db4,
    },
)

# mappings and tables
class Base(DeclarativeBase):
    pass

# we need a way to create identifiers which are unique across all databases.
# one easy way would be to just use a composite primary key, where  one value
# is the shard id.  but here, we'll show something more "generic", an id
# generation function.  we'll use a simplistic "id table" stored in database
# #1.  Any other method will do just as well; UUID, hilo, application-specific,
# etc.

ids = Table("ids", Base.metadata, Column("nextid", Integer, nullable=False))

def id_generator(ctx):
    # in reality, might want to use a separate transaction for this.
    with db1.begin() as conn:
        nextid = conn.scalar(ids.select().with_for_update())
        conn.execute(ids.update().values({ids.c.nextid: ids.c.nextid + 1}))
    return nextid

# table setup.  we'll store a lead table of continents/cities, and a secondary
# table storing locations. a particular row will be placed in the database
# whose shard id corresponds to the 'continent'.  in this setup, secondary rows
# in 'weather_reports' will be placed in the same DB as that of the parent, but
# this can be changed if you're willing to write more complex sharding
# functions.

class WeatherLocation(Base):
    __tablename__ = "weather_locations"

    id: Mapped[int] = mapped_column(primary_key=True, default=id_generator)
    continent: Mapped[str]
    city: Mapped[str]

    reports: Mapped[list[Report]] = relationship(back_populates="location")

    def __init__(self, continent: str, city: str):
        self.continent = continent
        self.city = city

class Report(Base):
    __tablename__ = "weather_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("weather_locations.id")
    )
    temperature: Mapped[float]
    report_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    location: Mapped[WeatherLocation] = relationship(back_populates="reports")

    def __init__(self, temperature: float):
        self.temperature = temperature

# define sharding functions.

# we'll use a straight mapping of a particular set of "country"
# attributes to shard id.
shard_lookup = {
    "North America": "north_america",
    "Asia": "asia",
    "Europe": "europe",
    "South America": "south_america",
}

def shard_chooser(mapper, instance, clause=None):
    """shard chooser.

    looks at the given instance and returns a shard id
    note that we need to define conditions for
    the WeatherLocation class, as well as our secondary Report class which will
    point back to its WeatherLocation via its 'location' attribute.

    """
    if isinstance(instance, WeatherLocation):
        return shard_lookup[instance.continent]
    else:
        return shard_chooser(mapper, instance.location)

def identity_chooser(mapper, primary_key, *, lazy_loaded_from, **kw):
    """identity chooser.

    given a primary key, returns a list of shards
    to search.  here, we don't have any particular information from a
    pk so we just return all shard ids. often, you'd want to do some
    kind of round-robin strategy here so that requests are evenly
    distributed among DBs.

    """
    if lazy_loaded_from:
        # if we are in a lazy load, we can look at the parent object
        # and limit our search to that same shard, assuming that's how we've
        # set things up.
        return [lazy_loaded_from.identity_token]
    else:
        return ["north_america", "asia", "europe", "south_america"]

def execute_chooser(context):
    """statement execution chooser.

    this also returns a list of shard ids, which can just be all of them. but
    here we'll search into the execution context in order to try to narrow down
    the list of shards to SELECT.

    """
    ids = []

    # we'll grab continent names as we find them
    # and convert to shard ids
    for column, operator, value in _get_select_comparisons(context.statement):
        # "shares_lineage()" returns True if both columns refer to the same
        # statement column, adjusting for any annotations present.
        # (an annotation is an internal clone of a Column object
        # and occur when using ORM-mapped attributes like
        # "WeatherLocation.continent"). A simpler comparison, though less
        # accurate, would be "column.key == 'continent'".
        if column.shares_lineage(WeatherLocation.__table__.c.continent):
            if operator == operators.eq:
                ids.append(shard_lookup[value])
            elif operator == operators.in_op:
                ids.extend(shard_lookup[v] for v in value)

    if len(ids) == 0:
        return ["north_america", "asia", "europe", "south_america"]
    else:
        return ids

def _get_select_comparisons(statement):
    """Search a Select or Query object for binary expressions.

    Returns expressions which match a Column against one or more
    literal values as a list of tuples of the form
    (column, operator, values).   "values" is a single value
    or tuple of values depending on the operator.

    """
    binds = {}
    clauses = set()
    comparisons = []

    def visit_bindparam(bind):
        # visit a bind parameter.

        value = bind.effective_value
        binds[bind] = value

    def visit_column(column):
        clauses.add(column)

    def visit_binary(binary):
        if binary.left in clauses and binary.right in binds:
            comparisons.append(
                (binary.left, binary.operator, binds[binary.right])
            )

        elif binary.left in binds and binary.right in clauses:
            comparisons.append(
                (binary.right, binary.operator, binds[binary.left])
            )

    # here we will traverse through the query's criterion, searching
    # for SQL constructs.  We will place simple column comparisons
    # into a list.
    if statement.whereclause is not None:
        visitors.traverse(
            statement.whereclause,
            {},
            {
                "bindparam": visit_bindparam,
                "binary": visit_binary,
                "column": visit_column,
            },
        )
    return comparisons

# further configure create_session to use these functions
Session.configure(
    shard_chooser=shard_chooser,
    identity_chooser=identity_chooser,
    execute_chooser=execute_chooser,
)

def setup():
    # create tables
    for db in (db1, db2, db3, db4):
        Base.metadata.create_all(db)

    # establish initial "id" in db1
    with db1.begin() as conn:
        conn.execute(ids.insert(), {"nextid": 1})

def main():
    setup()

    # save and load objects!

    tokyo = WeatherLocation("Asia", "Tokyo")
    newyork = WeatherLocation("North America", "New York")
    toronto = WeatherLocation("North America", "Toronto")
    london = WeatherLocation("Europe", "London")
    dublin = WeatherLocation("Europe", "Dublin")
    brasilia = WeatherLocation("South America", "Brasila")
    quito = WeatherLocation("South America", "Quito")

    tokyo.reports.append(Report(80.0))
    newyork.reports.append(Report(75))
    quito.reports.append(Report(85))

    with Session() as sess:
        sess.add_all(
            [tokyo, newyork, toronto, london, dublin, brasilia, quito]
        )

        sess.commit()

        t = sess.get(WeatherLocation, tokyo.id)
        assert t.city == tokyo.city
        assert t.reports[0].temperature == 80.0

        # select across shards
        asia_and_europe = sess.execute(
            select(WeatherLocation).filter(
                WeatherLocation.continent.in_(["Europe", "Asia"])
            )
        ).scalars()

        assert {c.city for c in asia_and_europe} == {
            "Tokyo",
            "London",
            "Dublin",
        }

        # optionally set a shard id for the query and all related loaders
        north_american_cities_w_t = sess.execute(
            select(WeatherLocation)
            .filter(WeatherLocation.city.startswith("T"))
            .options(set_shard_id("north_america"))
        ).scalars()

        # Tokyo not included since not in the north_america shard
        assert {c.city for c in north_american_cities_w_t} == {
            "Toronto",
        }

        # the Report class uses a simple integer primary key.  So across two
        # databases, a primary key will be repeated.  The "identity_token"
        # tracks in memory that these two identical primary keys are local to
        # different shards.
        newyork_report = newyork.reports[0]
        tokyo_report = tokyo.reports[0]

        assert inspect(newyork_report).identity_key == (
            Report,
            (1,),
            "north_america",
        )
        assert inspect(tokyo_report).identity_key == (Report, (1,), "asia")

        # the token representing the originating shard is also available
        # directly
        assert inspect(newyork_report).identity_token == "north_america"
        assert inspect(tokyo_report).identity_token == "asia"

if __name__ == "__main__":
    main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.sharding.separate_schema_translates

```
"""Illustrates sharding using a single database with multiple schemas,
where a different "schema_translates_map" can be used for each shard.

In this example we will set a "shard id" at all times.

"""

from __future__ import annotations

import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

echo = True
engine = create_engine("sqlite://", echo=echo)

with engine.connect() as conn:
    # use attached databases on sqlite to get "schemas"
    for i in range(1, 5):
        if os.path.exists("schema_%s.db" % i):
            os.remove("schema_%s.db" % i)
        conn.exec_driver_sql(
            'ATTACH DATABASE "schema_%s.db" AS schema_%s' % (i, i)
        )

db1 = engine.execution_options(schema_translate_map={None: "schema_1"})
db2 = engine.execution_options(schema_translate_map={None: "schema_2"})
db3 = engine.execution_options(schema_translate_map={None: "schema_3"})
db4 = engine.execution_options(schema_translate_map={None: "schema_4"})

# create session function.  this binds the shard ids
# to databases within a ShardedSession and returns it.
Session = sessionmaker(
    class_=ShardedSession,
    shards={
        "north_america": db1,
        "asia": db2,
        "europe": db3,
        "south_america": db4,
    },
)

# mappings and tables
class Base(DeclarativeBase):
    pass

# table setup.  we'll store a lead table of continents/cities, and a secondary
# table storing locations. a particular row will be placed in the database
# whose shard id corresponds to the 'continent'.  in this setup, secondary rows
# in 'weather_reports' will be placed in the same DB as that of the parent, but
# this can be changed if you're willing to write more complex sharding
# functions.

class WeatherLocation(Base):
    __tablename__ = "weather_locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    continent: Mapped[str]
    city: Mapped[str]

    reports: Mapped[list[Report]] = relationship(back_populates="location")

    def __init__(self, continent: str, city: str):
        self.continent = continent
        self.city = city

class Report(Base):
    __tablename__ = "weather_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("weather_locations.id")
    )
    temperature: Mapped[float]
    report_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    location: Mapped[WeatherLocation] = relationship(back_populates="reports")

    def __init__(self, temperature: float):
        self.temperature = temperature

# define sharding functions.

# we'll use a straight mapping of a particular set of "country"
# attributes to shard id.
shard_lookup = {
    "North America": "north_america",
    "Asia": "asia",
    "Europe": "europe",
    "South America": "south_america",
}

def shard_chooser(mapper, instance, clause=None):
    """shard chooser.

    this is primarily invoked at persistence time.

    looks at the given instance and returns a shard id
    note that we need to define conditions for
    the WeatherLocation class, as well as our secondary Report class which will
    point back to its WeatherLocation via its 'location' attribute.

    """
    if isinstance(instance, WeatherLocation):
        return shard_lookup[instance.continent]
    else:
        return shard_chooser(mapper, instance.location)

def identity_chooser(mapper, primary_key, *, lazy_loaded_from, **kw):
    """identity chooser.

    given a primary key identity, return which shard we should look at.

    in this case, we only want to support this for lazy-loaded items;
    any primary query should have shard id set up front.

    """
    if lazy_loaded_from:
        # if we are in a lazy load, we can look at the parent object
        # and limit our search to that same shard, assuming that's how we've
        # set things up.
        return [lazy_loaded_from.identity_token]
    else:
        raise NotImplementedError()

def execute_chooser(context):
    """statement execution chooser.

    given an :class:`.ORMExecuteState` for a statement, return a list
    of shards we should consult.

    """
    if context.lazy_loaded_from:
        return [context.lazy_loaded_from.identity_token]
    else:
        return ["north_america", "asia", "europe", "south_america"]

# configure shard chooser
Session.configure(
    shard_chooser=shard_chooser,
    identity_chooser=identity_chooser,
    execute_chooser=execute_chooser,
)

def setup():
    # create tables
    for db in (db1, db2, db3, db4):
        Base.metadata.create_all(db)

def main():
    setup()

    # save and load objects!

    tokyo = WeatherLocation("Asia", "Tokyo")
    newyork = WeatherLocation("North America", "New York")
    toronto = WeatherLocation("North America", "Toronto")
    london = WeatherLocation("Europe", "London")
    dublin = WeatherLocation("Europe", "Dublin")
    brasilia = WeatherLocation("South America", "Brasila")
    quito = WeatherLocation("South America", "Quito")

    tokyo.reports.append(Report(80.0))
    newyork.reports.append(Report(75))
    quito.reports.append(Report(85))

    with Session() as sess:
        sess.add_all(
            [tokyo, newyork, toronto, london, dublin, brasilia, quito]
        )

        sess.commit()

        t = sess.get(
            WeatherLocation,
            tokyo.id,
            identity_token="asia",
        )
        assert t.city == tokyo.city
        assert t.reports[0].temperature == 80.0

        # select across shards
        asia_and_europe = sess.execute(
            select(WeatherLocation).filter(
                WeatherLocation.continent.in_(["Europe", "Asia"])
            )
        ).scalars()

        assert {c.city for c in asia_and_europe} == {
            "Tokyo",
            "London",
            "Dublin",
        }

        # optionally set a shard id for the query and all related loaders
        north_american_cities_w_t = sess.execute(
            select(WeatherLocation)
            .filter(WeatherLocation.city.startswith("T"))
            .options(set_shard_id("north_america"))
        ).scalars()

        # Tokyo not included since not in the north_america shard
        assert {c.city for c in north_american_cities_w_t} == {
            "Toronto",
        }

        # the Report class uses a simple integer primary key.  So across two
        # databases, a primary key will be repeated.  The "identity_token"
        # tracks in memory that these two identical primary keys are local to
        # different shards.
        newyork_report = newyork.reports[0]
        tokyo_report = tokyo.reports[0]

        assert inspect(newyork_report).identity_key == (
            Report,
            (1,),
            "north_america",
        )
        assert inspect(tokyo_report).identity_key == (Report, (1,), "asia")

        # the token representing the originating shard is also available
        # directly
        assert inspect(newyork_report).identity_token == "north_america"
        assert inspect(tokyo_report).identity_token == "asia"

if __name__ == "__main__":
    main()
```

---

# SQLAlchemy 2.0 Documentation

# Source code for examples.sharding.separate_tables

```
"""Illustrates sharding using a single SQLite database, that will however
have multiple tables using a naming convention."""

from __future__ import annotations

import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import operators
from sqlalchemy.sql import visitors

echo = True
engine = create_engine("sqlite://", echo=echo)

db1 = engine.execution_options(table_prefix="north_america")
db2 = engine.execution_options(table_prefix="asia")
db3 = engine.execution_options(table_prefix="europe")
db4 = engine.execution_options(table_prefix="south_america")

@event.listens_for(engine, "before_cursor_execute", retval=True)
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    table_prefix = context.execution_options.get("table_prefix", None)
    if table_prefix:
        statement = statement.replace("_prefix_", table_prefix)
    return statement, parameters

# create session function.  this binds the shard ids
# to databases within a ShardedSession and returns it.
Session = sessionmaker(
    class_=ShardedSession,
    shards={
        "north_america": db1,
        "asia": db2,
        "europe": db3,
        "south_america": db4,
    },
)

# mappings and tables
class Base(DeclarativeBase):
    pass

# we need a way to create identifiers which are unique across all databases.
# one easy way would be to just use a composite primary key, where  one value
# is the shard id.  but here, we'll show something more "generic", an id
# generation function.  we'll use a simplistic "id table" stored in database
# #1.  Any other method will do just as well; UUID, hilo, application-specific,
# etc.

ids = Table("ids", Base.metadata, Column("nextid", Integer, nullable=False))

def id_generator(ctx):
    # in reality, might want to use a separate transaction for this.
    with engine.begin() as conn:
        nextid = conn.scalar(ids.select().with_for_update())
        conn.execute(ids.update().values({ids.c.nextid: ids.c.nextid + 1}))
    return nextid

# table setup.  we'll store a lead table of continents/cities, and a secondary
# table storing locations. a particular row will be placed in the database
# whose shard id corresponds to the 'continent'.  in this setup, secondary rows
# in 'weather_reports' will be placed in the same DB as that of the parent, but
# this can be changed if you're willing to write more complex sharding
# functions.

class WeatherLocation(Base):
    __tablename__ = "_prefix__weather_locations"

    id: Mapped[int] = mapped_column(primary_key=True, default=id_generator)
    continent: Mapped[str]
    city: Mapped[str]

    reports: Mapped[list[Report]] = relationship(back_populates="location")

    def __init__(self, continent: str, city: str):
        self.continent = continent
        self.city = city

class Report(Base):
    __tablename__ = "_prefix__weather_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("_prefix__weather_locations.id")
    )
    temperature: Mapped[float]
    report_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    location: Mapped[WeatherLocation] = relationship(back_populates="reports")

    def __init__(self, temperature: float):
        self.temperature = temperature

# define sharding functions.

# we'll use a straight mapping of a particular set of "country"
# attributes to shard id.
shard_lookup = {
    "North America": "north_america",
    "Asia": "asia",
    "Europe": "europe",
    "South America": "south_america",
}

def shard_chooser(mapper, instance, clause=None):
    """shard chooser.

    looks at the given instance and returns a shard id
    note that we need to define conditions for
    the WeatherLocation class, as well as our secondary Report class which will
    point back to its WeatherLocation via its 'location' attribute.

    """
    if isinstance(instance, WeatherLocation):
        return shard_lookup[instance.continent]
    else:
        return shard_chooser(mapper, instance.location)

def identity_chooser(mapper, primary_key, *, lazy_loaded_from, **kw):
    """identity chooser.

    given a primary key, returns a list of shards
    to search.  here, we don't have any particular information from a
    pk so we just return all shard ids. often, you'd want to do some
    kind of round-robin strategy here so that requests are evenly
    distributed among DBs.

    """
    if lazy_loaded_from:
        # if we are in a lazy load, we can look at the parent object
        # and limit our search to that same shard, assuming that's how we've
        # set things up.
        return [lazy_loaded_from.identity_token]
    else:
        return ["north_america", "asia", "europe", "south_america"]

def execute_chooser(context):
    """statement execution chooser.

    this also returns a list of shard ids, which can just be all of them. but
    here we'll search into the execution context in order to try to narrow down
    the list of shards to SELECT.

    """
    ids = []

    # we'll grab continent names as we find them
    # and convert to shard ids
    for column, operator, value in _get_select_comparisons(context.statement):
        # "shares_lineage()" returns True if both columns refer to the same
        # statement column, adjusting for any annotations present.
        # (an annotation is an internal clone of a Column object
        # and occur when using ORM-mapped attributes like
        # "WeatherLocation.continent"). A simpler comparison, though less
        # accurate, would be "column.key == 'continent'".
        if column.shares_lineage(WeatherLocation.__table__.c.continent):
            if operator == operators.eq:
                ids.append(shard_lookup[value])
            elif operator == operators.in_op:
                ids.extend(shard_lookup[v] for v in value)

    if len(ids) == 0:
        return ["north_america", "asia", "europe", "south_america"]
    else:
        return ids

def _get_select_comparisons(statement):
    """Search a Select or Query object for binary expressions.

    Returns expressions which match a Column against one or more
    literal values as a list of tuples of the form
    (column, operator, values).   "values" is a single value
    or tuple of values depending on the operator.

    """
    binds = {}
    clauses = set()
    comparisons = []

    def visit_bindparam(bind):
        # visit a bind parameter.

        value = bind.effective_value
        binds[bind] = value

    def visit_column(column):
        clauses.add(column)

    def visit_binary(binary):
        if binary.left in clauses and binary.right in binds:
            comparisons.append(
                (binary.left, binary.operator, binds[binary.right])
            )

        elif binary.left in binds and binary.right in clauses:
            comparisons.append(
                (binary.right, binary.operator, binds[binary.left])
            )

    # here we will traverse through the query's criterion, searching
    # for SQL constructs.  We will place simple column comparisons
    # into a list.
    if statement.whereclause is not None:
        visitors.traverse(
            statement.whereclause,
            {},
            {
                "bindparam": visit_bindparam,
                "binary": visit_binary,
                "column": visit_column,
            },
        )
    return comparisons

# further configure create_session to use these functions
Session.configure(
    shard_chooser=shard_chooser,
    identity_chooser=identity_chooser,
    execute_chooser=execute_chooser,
)

def setup():
    # create tables
    for db in (db1, db2, db3, db4):
        Base.metadata.create_all(db)

    # establish initial "id" in db1
    with db1.begin() as conn:
        conn.execute(ids.insert(), {"nextid": 1})

def main():
    setup()

    # save and load objects!

    tokyo = WeatherLocation("Asia", "Tokyo")
    newyork = WeatherLocation("North America", "New York")
    toronto = WeatherLocation("North America", "Toronto")
    london = WeatherLocation("Europe", "London")
    dublin = WeatherLocation("Europe", "Dublin")
    brasilia = WeatherLocation("South America", "Brasila")
    quito = WeatherLocation("South America", "Quito")

    tokyo.reports.append(Report(80.0))
    newyork.reports.append(Report(75))
    quito.reports.append(Report(85))

    with Session() as sess:
        sess.add_all(
            [tokyo, newyork, toronto, london, dublin, brasilia, quito]
        )

        sess.commit()

        t = sess.get(WeatherLocation, tokyo.id)
        assert t.city == tokyo.city
        assert t.reports[0].temperature == 80.0

        # optionally set a shard id for the query and all related loaders
        north_american_cities_w_t = sess.execute(
            select(WeatherLocation)
            .filter(WeatherLocation.city.startswith("T"))
            .options(set_shard_id("north_america"))
        ).scalars()

        # Tokyo not included since not in the north_america shard
        assert {c.city for c in north_american_cities_w_t} == {
            "Toronto",
        }

        asia_and_europe = sess.execute(
            select(WeatherLocation).filter(
                WeatherLocation.continent.in_(["Europe", "Asia"])
            )
        ).scalars()

        assert {c.city for c in asia_and_europe} == {
            "Tokyo",
            "London",
            "Dublin",
        }

        # the Report class uses a simple integer primary key.  So across two
        # databases, a primary key will be repeated.  The "identity_token"
        # tracks in memory that these two identical primary keys are local to
        # different shards.
        newyork_report = newyork.reports[0]
        tokyo_report = tokyo.reports[0]

        assert inspect(newyork_report).identity_key == (
            Report,
            (1,),
            "north_america",
        )
        assert inspect(tokyo_report).identity_key == (Report, (1,), "asia")

        # the token representing the originating shard is also available
        # directly
        assert inspect(newyork_report).identity_token == "north_america"
        assert inspect(tokyo_report).identity_token == "asia"

if __name__ == "__main__":
    main()
```
