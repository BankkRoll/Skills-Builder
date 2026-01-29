# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Glossary

  1.x style2.0 style1.x-style2.0-style

These terms are new in SQLAlchemy 1.4 and refer to the SQLAlchemy 1.4->
2.0 transition plan, described at [SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html).  The
term “1.x style” refers to an API used in the way it’s been documented
throughout the 1.x series of SQLAlchemy and earlier (e.g. 1.3, 1.2, etc)
and the term “2.0 style” refers to the way an API will look in version
2.0.   Version 1.4 implements nearly all of 2.0’s API in so-called
“transition mode”, while version 2.0 still maintains the legacy
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object to allow legacy code to remain largely
2.0 compatible.

See also

[SQLAlchemy 2.0 - Major Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)

   ACIDACID model

An acronym for “Atomicity, Consistency, Isolation,
Durability”; a set of properties that guarantee that
database transactions are processed reliably.
(via Wikipedia)

See also

[atomicity](#term-atomicity)

[consistency](#term-consistency)

[isolation](#term-isolation)

[durability](#term-durability)

[ACID Model (via Wikipedia)](https://en.wikipedia.org/wiki/ACID_Model)

   association relationship

A two-tiered [relationship](#term-relationship) which links two tables
together using an association table in the middle.  The
association relationship differs from a [many to many](#term-many-to-many)
relationship in that the many-to-many table is mapped
by a full class, rather than invisibly handled by the
[sqlalchemy.orm.relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct as in the case
with many-to-many, so that additional attributes are
explicitly available.

For example, if we wanted to associate employees with
projects, also storing the specific role for that employee
with the project, the relational schema might look like:

```
CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE project (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE employee_project (
    employee_id INTEGER PRIMARY KEY,
    project_id INTEGER PRIMARY KEY,
    role_name VARCHAR(30),
    FOREIGN KEY employee_id REFERENCES employee(id),
    FOREIGN KEY project_id REFERENCES project(id)
)
```

A SQLAlchemy declarative mapping for the above might look like:

```
class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

class EmployeeProject(Base):
    __tablename__ = "employee_project"

    employee_id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)
    role_name = Column(String(30))

    project = relationship("Project", backref="project_employees")
    employee = relationship("Employee", backref="employee_projects")
```

Employees can be added to a project given a role name:

```
proj = Project(name="Client A")

emp1 = Employee(name="emp1")
emp2 = Employee(name="emp2")

proj.project_employees.extend(
    [
        EmployeeProject(employee=emp1, role_name="tech lead"),
        EmployeeProject(employee=emp2, role_name="account executive"),
    ]
)
```

See also

[many to many](#term-many-to-many)

   atomicity

Atomicity is one of the components of the [ACID](#term-ACID) model,
and requires that each transaction is “all or nothing”:
if one part of the transaction fails, the entire transaction
fails, and the database state is left unchanged. An atomic
system must guarantee atomicity in each and every situation,
including power failures, errors, and crashes.
(via Wikipedia)

See also

[ACID](#term-ACID)

[Atomicity (via Wikipedia)](https://en.wikipedia.org/wiki/Atomicity_(database_systems))

   attached

Indicates an ORM object that is presently associated with a specific
[Session](#term-Session).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   backrefbidirectional relationship

An extension to the [relationship](#term-relationship) system whereby two
distinct [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) objects can be
mutually associated with each other, such that they coordinate
in memory as changes occur to either side.   The most common
way these two relationships are constructed is by using
the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function explicitly
for one side and specifying the `backref` keyword to it so that
the other [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is created
automatically.  We can illustrate this against the example we’ve
used in [one to many](#term-one-to-many) as follows:

```
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    employees = relationship("Employee", backref="department")

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dep_id = Column(Integer, ForeignKey("department.id"))
```

A backref can be applied to any relationship, including one to many,
many to one, and [many to many](#term-many-to-many).

See also

[relationship](#term-relationship)

[one to many](#term-one-to-many)

[many to one](#term-many-to-one)

[many to many](#term-many-to-many)

   bound parameterbound parametersbind parameterbind parameters

Bound parameters are the primary means in which data is passed to the
[DBAPI](#term-DBAPI) database driver.    While the operation to be invoked is
based on the SQL statement string, the data values themselves are
passed separately, where the driver contains logic that will safely
process these strings and pass them to the backend database server,
which may either involve formatting the parameters into the SQL string
itself, or passing them to the database using separate protocols.

The specific system by which the database driver does this should not
matter to the caller; the point is that on the outside, data should
**always** be passed separately and not as part of the SQL string
itself.  This is integral both to having adequate security against
SQL injections as well as allowing the driver to have the best
performance.

See also

[Prepared Statement](https://en.wikipedia.org/wiki/Prepared_statement) - at Wikipedia

[bind parameters](https://use-the-index-luke.com/sql/where-clause/bind-parameters) - at Use The Index, Luke!

[Sending Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-sending-parameters) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

   candidate key

A [relational algebra](#term-relational-algebra) term referring to an attribute or set
of attributes that form a uniquely identifying key for a
row.  A row may have more than one candidate key, each of which
is suitable for use as the primary key of that row.
The primary key of a table is always a candidate key.

See also

[primary key](#term-primary-key)

[Candidate key (via Wikipedia)](https://en.wikipedia.org/wiki/Candidate_key)

[https://www.databasestar.com/database-keys/](https://www.databasestar.com/database-keys/)

   cartesian product

Given two sets A and B, the cartesian product is the set of all ordered pairs (a, b)
where a is in A and b is in B.

In terms of SQL databases, a cartesian product occurs when we select from two
or more tables (or other subqueries) without establishing any kind of criteria
between the rows of one table to another (directly or indirectly).  If we
SELECT from table A and table B at the same time, we get every row of A matched
to the first row of B, then every row of A matched to the second row of B, and
so on until every row from A has been paired with every row of B.

Cartesian products cause enormous result sets to be generated and can easily
crash a client application if not prevented.

See also

[Cartesian Product (via Wikipedia)](https://en.wikipedia.org/wiki/Cartesian_product)

   cascade

A term used in SQLAlchemy to describe how an ORM persistence action that
takes place on a particular object would extend into other objects
which are directly associated with that object.  In SQLAlchemy, these
object associations are configured using the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
construct.   [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) contains a parameter called
[relationship.cascade](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.cascade) which provides options on how certain
persistence operations may cascade.

The term “cascades” as well as the general architecture of this system
in SQLAlchemy was borrowed, for better or worse, from the Hibernate
ORM.

See also

[Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades)

   check constraint

A check constraint is a
condition that defines valid data when adding or updating an
entry in a table of a relational database. A check constraint
is applied to each row in the table.

(via Wikipedia)

A check constraint can be added to a table in standard
SQL using [DDL](#term-DDL) like the following:

```
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);
```

See also

[CHECK constraint (via Wikipedia)](https://en.wikipedia.org/wiki/Check_constraint)

   columns clause

The portion of the `SELECT` statement which enumerates the
SQL expressions to be returned in the result set.  The expressions
follow the `SELECT` keyword directly and are a comma-separated
list of individual expressions.

E.g.:

```
SELECT user_account.name, user_account.email
FROM user_account WHERE user_account.name = 'fred'
```

Above, the list of columns `user_acount.name`,
`user_account.email` is the columns clause of the `SELECT`.

  composite primary key

A [primary key](#term-primary-key) that has more than one column.   A particular
database row is unique based on two or more columns rather than just
a single value.

See also

[primary key](#term-primary-key)

   consistency

Consistency is one of the components of the [ACID](#term-ACID) model,
and ensures that any transaction will
bring the database from one valid state to another. Any data
written to the database must be valid according to all defined
rules, including but not limited to [constraints](#term-constraints), cascades,
triggers, and any combination thereof.
(via Wikipedia)

See also

[ACID](#term-ACID)

[Consistency (via Wikipedia)](https://en.wikipedia.org/wiki/Consistency_(database_systems))

   constraintconstraintsconstrained

Rules established within a relational database that ensure
the validity and consistency of data.   Common forms
of constraint include [primary key constraint](#term-primary-key-constraint),
[foreign key constraint](#term-foreign-key-constraint), and [check constraint](#term-check-constraint).

  correlatescorrelated subquerycorrelated subqueries

A [subquery](#term-subquery) is correlated if it depends on data in the
enclosing `SELECT`.

Below, a subquery selects the aggregate value `MIN(a.id)`
from the `email_address` table, such that
it will be invoked for each value of `user_account.id`, correlating
the value of this column against the `email_address.user_account_id`
column:

```
SELECT user_account.name, email_address.email
 FROM user_account
 JOIN email_address ON user_account.id=email_address.user_account_id
 WHERE email_address.id = (
    SELECT MIN(a.id) FROM email_address AS a
    WHERE a.user_account_id=user_account.id
 )
```

The above subquery refers to the `user_account` table, which is not itself
in the `FROM` clause of this nested query.   Instead, the `user_account`
table is received from the enclosing query, where each row selected from
`user_account` results in a distinct execution of the subquery.

A correlated subquery is in most cases present in the [WHERE clause](#term-WHERE-clause)
or [columns clause](#term-columns-clause) of the immediately enclosing `SELECT`
statement, as well as in the ORDER BY or HAVING clause.

In less common cases, a correlated subquery may be present in the
[FROM clause](#term-FROM-clause) of an enclosing `SELECT`; in these cases the
correlation is typically due to the enclosing `SELECT` itself being
enclosed in the WHERE,
ORDER BY, columns or HAVING clause of another `SELECT`, such as:

```
SELECT parent.id FROM parent
WHERE EXISTS (
    SELECT * FROM (
        SELECT child.id AS id, child.parent_id AS parent_id, child.pos AS pos
        FROM child
        WHERE child.parent_id = parent.id ORDER BY child.pos
    LIMIT 3)
WHERE id = 7)
```

Correlation from one `SELECT` directly to one which encloses the correlated
query via its `FROM`
clause is not possible, because the correlation can only proceed once the
original source rows from the enclosing statement’s FROM clause are available.

  crudCRUD

An acronym meaning “Create, Update, Delete”.  The term in SQL refers to the
set of operations that create, modify and delete data from the database,
also known as [DML](#term-DML), and typically refers to the `INSERT`,
`UPDATE`, and `DELETE` statements.

  cursor

A control structure that enables traversal over the records in a database.
In the Python DBAPI, the cursor object is in fact the starting point
for statement execution as well as the interface used for fetching
results.

See also

[Cursor Objects (in pep-249)](https://www.python.org/dev/peps/pep-0249/#cursor-objects)

[Cursor (via Wikipedia)](https://en.wikipedia.org/wiki/Cursor_(databases))

   cyclomatic complexity

A measure of code complexity based on the number of possible paths
through a program’s source code.

See also

[Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)

   DBAPIpep-249

DBAPI is shorthand for the phrase “Python Database API
Specification”.  This is a widely used specification
within Python to define common usage patterns for all
database connection packages.   The DBAPI is a “low level”
API which is typically the lowest level system used
in a Python application to talk to a database.  SQLAlchemy’s
[dialect](#term-dialect) system is constructed around the
operation of the DBAPI, providing individual dialect
classes which service a specific DBAPI on top of a
specific database engine; for example, the [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)
URL `postgresql+psycopg2://@localhost/test`
refers to the [psycopg2](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)
DBAPI/dialect combination, whereas the URL `mysql+mysqldb://@localhost/test`
refers to the [MySQLforPython](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb)
DBAPI/dialect combination.

See also

[PEP 249 - Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/)

   DDL

An acronym for **Data Definition Language**.  DDL is the subset
of SQL that relational databases use to configure tables, constraints,
and other permanent objects within a database schema.  SQLAlchemy
provides a rich API for constructing and emitting DDL expressions.

See also

[Describing Databases with MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html)

[DDL (via Wikipedia)](https://en.wikipedia.org/wiki/Data_definition_language)

[DML](#term-DML)

[DQL](#term-DQL)

   deleted

This describes one of the major object states which
an object can have within a [Session](#term-Session); a deleted object
is an object that was formerly persistent and has had a
DELETE statement emitted to the database within a flush
to delete its row.  The object will move to the [detached](#term-detached)
state once the session’s transaction is committed; alternatively,
if the session’s transaction is rolled back, the DELETE is
reverted and the object moves back to the [persistent](#term-persistent)
state.

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   descriptordescriptors

In Python, a descriptor is an object attribute with “binding behavior”,
one whose attribute access has been overridden by methods in the
[descriptor protocol](https://docs.python.org/howto/descriptor.html).
Those methods are `__get__()`, `__set__()`, and `__delete__()`.
If any of those methods are defined for an object, it is said to be a
descriptor.

In SQLAlchemy, descriptors are used heavily in order to provide attribute behavior
on mapped classes.   When a class is mapped as such:

```
class MyClass(Base):
    __tablename__ = "foo"

    id = Column(Integer, primary_key=True)
    data = Column(String)
```

The `MyClass` class will be [mapped](#term-mapped) when its definition
is complete, at which point the `id` and `data` attributes,
starting out as [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects, will be replaced
by the [instrumentation](#term-instrumentation) system with instances
of [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute), which are descriptors that
provide the above mentioned `__get__()`, `__set__()` and
`__delete__()` methods.   The [InstrumentedAttribute](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstrumentedAttribute)
will generate a SQL expression when used at the class level:

```
>>> print(MyClass.data == 5)
data = :data_1
```

and at the instance level, keeps track of changes to values,
and also [lazy loads](#term-lazy-loads) unloaded attributes
from the database:

```
>>> m1 = MyClass()
>>> m1.id = 5
>>> m1.data = "some data"

>>> from sqlalchemy import inspect
>>> inspect(m1).attrs.data.history.added
"some data"
```

   detached

This describes one of the major object states which
an object can have within a [Session](#term-Session); a detached object
is an object that has a database identity (i.e. a primary key)
but is not associated with any session.  An object that
was previously [persistent](#term-persistent) and was removed from its
session either because it was expunged, or the owning
session was closed, moves into the detached state.
The detached state is generally used when objects are being
moved between sessions or when being moved to/from an external
object cache.

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   dialect

In SQLAlchemy, the “dialect” is a Python object that represents information
and methods that allow database operations to proceed on a particular
kind of database backend and a particular kind of Python driver (or
[DBAPI](#term-DBAPI)) for that database.   SQLAlchemy dialects are subclasses
of the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) class.

See also

[Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)

   discriminator

A result-set column which is used during [polymorphic](#term-polymorphic) loading
to determine what kind of mapped class should be applied to a particular
incoming result row.

See also

[Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html)

   DML

An acronym for **Data Manipulation Language**.  DML is the subset of
SQL that relational databases use to *modify* the data in tables. DML
typically refers to the three widely familiar statements of INSERT,
UPDATE and  DELETE, otherwise known as [CRUD](#term-CRUD) (acronym for “Create,
Read, Update, Delete”).

> See also
>
>
>
> [DML (via Wikipedia)](https://en.wikipedia.org/wiki/Data_manipulation_language)
>
>
>
> [DDL](#term-DDL)
>
>
>
> [DQL](#term-DQL)

  domain model

A domain model in problem solving and software engineering is a conceptual model of all the topics related to a specific problem. It describes the various entities, their attributes, roles, and relationships, plus the constraints that govern the problem domain.

(via Wikipedia)

See also

[Domain Model (via Wikipedia)](https://en.wikipedia.org/wiki/Domain_model)

   DQL

An acronym for **Data Query Language**.  DQL is the subset of
SQL that relational databases use to *read* the data in tables.
DQL almost exclusively refers to the SQL SELECT construct as the
top level SQL statement in use.

See also

[DQL (via Wikipedia)](https://en.wikipedia.org/wiki/Data_query_language)

[DML](#term-DML)

[DDL](#term-DDL)

   durability

Durability is a property of the [ACID](#term-ACID) model
which means that once a transaction has been committed,
it will remain so, even in the event of power loss, crashes,
or errors. In a relational database, for instance, once a
group of SQL statements execute, the results need to be stored
permanently (even if the database crashes immediately
thereafter).
(via Wikipedia)

See also

[ACID](#term-ACID)

[Durability (via Wikipedia)](https://en.wikipedia.org/wiki/Durability_(database_systems))

   eager loadeager loadseager loadedeager loadingeagerly load

In object relational mapping, an “eager load” refers to an attribute
that is populated with its database-side value at the same time as when
the object itself is loaded from the database. In SQLAlchemy, the term
“eager loading” usually refers to related collections and instances of
objects that are linked between mappings using the
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct, but can also refer to additional
column attributes being loaded, often from other tables related to a
particular table being queried, such as when using
[inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html) mappings.

Eager loading is the opposite of [lazy loading](#term-lazy-loading).

See also

[Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)

   executemany

This term refers to a part of the [PEP 249](https://peps.python.org/pep-0249/) DBAPI specification
indicating a single SQL statement that may be invoked against a
database connection with multiple parameter sets.   The specific
method is known as
[cursor.executemany()](https://peps.python.org/pep-0249/#executemany),
and it has many behavioral differences in comparison to the
[cursor.execute()](https://peps.python.org/pep-0249/#execute)
method which is used for single-statement invocation.   The “executemany”
method executes the given SQL statement multiple times, once for
each set of parameters passed.  The general rationale for using
executemany is that of improved performance, wherein the DBAPI may
use techniques such as preparing the statement just once beforehand,
or otherwise optimizing for invoking the same statement many times.

SQLAlchemy typically makes use of the `cursor.executemany()` method
automatically when the [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) method is
used where a list of parameter dictionaries were passed; this indicates
to SQLAlchemy Core that the SQL statement and processed parameter sets
should be passed to `cursor.executemany()`, where the statement will
be invoked by the driver for each parameter dictionary individually.

A key limitation of the `cursor.executemany()` method as used with
all known DBAPIs is that the `cursor` is not configured to return
rows when this method is used.  For **most** backends (a notable
exception being the python-oracledb / cx_Oracle DBAPIs), this means that
statements like `INSERT..RETURNING` typically cannot be used with
`cursor.executemany()` directly, since DBAPIs typically do not
aggregate the single row from each INSERT execution together.

To overcome this limitation, SQLAlchemy as of the 2.0 series implements
an alternative form of “executemany” which is known as
[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues). This feature makes use of
`cursor.execute()` to invoke an INSERT statement that will proceed
with multiple parameter sets in one round trip, thus producing the same
effect as using `cursor.executemany()` while still supporting
RETURNING.

See also

[Sending Multiple Parameters](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-multiple-parameters) - tutorial introduction to
“executemany”

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) - SQLAlchemy feature which allows
RETURNING to be used with “executemany”

   expireexpiredexpiresexpiringExpiring

In the SQLAlchemy ORM, refers to when the data in a [persistent](#term-persistent)
or sometimes [detached](#term-detached) object is erased, such that when
the object’s attributes are next accessed, a [lazy load](#term-lazy-load) SQL
query will be emitted in order to refresh the data for this object
as stored in the current ongoing transaction.

See also

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire)

   facade

An object that serves as a front-facing interface masking more complex
underlying or structural code.

See also

[Facade pattern (via Wikipedia)](https://en.wikipedia.org/wiki/Facade_pattern)

   flushflushingflushed

This refers to the actual process used by the [unit of work](#term-unit-of-work)
to emit changes to a database.  In SQLAlchemy this process occurs
via the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object and is usually automatic, but
can also be controlled manually.

See also

[Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-flushing)

   foreign key constraint

A referential constraint between two tables.  A foreign key is a field or set of fields in a
relational table that matches a [candidate key](#term-candidate-key) of another table.
The foreign key can be used to cross-reference tables.
(via Wikipedia)

A foreign key constraint can be added to a table in standard
SQL using [DDL](#term-DDL) like the following:

```
ALTER TABLE employee ADD CONSTRAINT dep_id_fk
FOREIGN KEY (employee) REFERENCES department (dep_id)
```

See also

[Foreign Key Constraint (via Wikipedia)](https://en.wikipedia.org/wiki/Foreign_key_constraint)

   FROM clause

The portion of the `SELECT` statement which indicates the initial
source of rows.

A simple `SELECT` will feature one or more table names in its
FROM clause.  Multiple sources are separated by a comma:

```
SELECT user.name, address.email_address
FROM user, address
WHERE user.id=address.user_id
```

The FROM clause is also where explicit joins are specified.  We can
rewrite the above `SELECT` using a single `FROM` element which consists
of a `JOIN` of the two tables:

```
SELECT user.name, address.email_address
FROM user JOIN address ON user.id=address.user_id
```

   identity key

A key associated with ORM-mapped objects that identifies their
primary key identity within the database, as well as their unique
identity within a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) [identity map](#term-identity-map).

In SQLAlchemy, you can view the identity key for an ORM object
using the [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) API to return the [InstanceState](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.InstanceState)
tracking object, then looking at the `InstanceState.key`
attribute:

```
>>> from sqlalchemy import inspect
>>> inspect(some_object).key
(<class '__main__.MyTable'>, (1,), None)
```

See also

[identity map](#term-identity-map)

   identity map

A mapping between Python objects and their database identities.
The identity map is a collection that’s associated with an
ORM [Session](#term-Session) object, and maintains a single instance
of every database object keyed to its identity.   The advantage
to this pattern is that all operations which occur for a particular
database identity are transparently coordinated onto a single
object instance.  When using an identity map in conjunction with
an [isolated](#term-isolated) transaction, having a reference
to an object that’s known to have a particular primary key can
be considered from a practical standpoint to be a
proxy to the actual database row.

See also

[Identity Map (via Martin Fowler)](https://martinfowler.com/eaaCatalog/identityMap.html)

[Get by Primary Key](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-get) - how to look up an object in the identity map
by primary key

   imperativedeclarative

In the SQLAlchemy ORM, these terms refer to two different styles of
mapping Python classes to database tables.

See also

[Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping)

[Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-imperative-mapping)

   insertmanyvalues

This refers to a SQLAlchemy-specific feature which allows INSERT
statements to emit thousands of new rows within a single statement
while at the same time allowing server generated values to be returned
inline from the statement using RETURNING or similar, for performance
optimization purposes. The feature is intended to be transparently
available for selected backends, but does offer some configurational
options. See the section [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) for a full
description of this feature.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

   instrumentationinstrumentedinstrumenting

Instrumentation refers to the process of augmenting the functionality
and attribute set of a particular class.   Ideally, the
behavior of the class should remain close to a regular
class, except that additional behaviors and features are
made available.  The SQLAlchemy [mapping](#term-mapping) process,
among other things, adds database-enabled [descriptors](#term-descriptors)
to a mapped
class each of which represents a particular database column
or relationship to a related class.

  isolationisolatedisolation level

The isolation property of the [ACID](#term-ACID) model
ensures that the concurrent execution
of transactions results in a system state that would be
obtained if transactions were executed serially, i.e. one
after the other. Each transaction must execute in total
isolation i.e. if T1 and T2 execute concurrently then each
should remain independent of the other.
(via Wikipedia)

See also

[ACID](#term-ACID)

[Isolation (via Wikipedia)](https://en.wikipedia.org/wiki/Isolation_(database_systems))

[read uncommitted](#term-read-uncommitted)

[read committed](#term-read-committed)

[repeatable read](#term-repeatable-read)

[serializable](#term-serializable)

   lazy initialization

A tactic of delaying some initialization action, such as creating objects,
populating data, or establishing connectivity to other services, until
those resources are required.

See also

[Lazy initialization (via Wikipedia)](https://en.wikipedia.org/wiki/Lazy_initialization)

   lazy loadlazy loadslazy loadedlazy loading

In object relational mapping, a “lazy load” refers to an
attribute that does not contain its database-side value
for some period of time, typically when the object is
first loaded.  Instead, the attribute receives a
*memoization* that causes it to go out to the database
and load its data when it’s first used.   Using this pattern,
the complexity and time spent within object fetches can
sometimes be reduced, in that
attributes for related tables don’t need to be addressed
immediately.

Lazy loading is the opposite of [eager loading](#term-eager-loading).

Within SQLAlchemy, lazy loading is a key feature of the ORM, and
applies to attributes which are [mapped](#term-mapped) on a user-defined class.
When attributes that refer to database columns or related objects
are accessed, for which no loaded value is present, the ORM makes
use of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) for which the current object is
associated with in the [persistent](#term-persistent) state, and emits a SELECT
statement on the current transaction, starting a new transaction if
one was not in progress.   If the object is in the [detached](#term-detached)
state and not associated with any [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), this is
considered to be an error state and an
[informative exception](https://docs.sqlalchemy.org/en/20/errors.html#error-bhk3) is raised.

See also

[Lazy Load (via Martin Fowler)](https://martinfowler.com/eaaCatalog/lazyLoad.html)

[N plus one problem](#term-N-plus-one-problem)

[Column Loading Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#loading-columns) - includes information on lazy loading of
ORM mapped columns

[Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) - includes information on lazy
loading of ORM related objects

[Preventing Implicit IO when Using AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads) - tips on avoiding lazy loading
when using the [Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) extension

   many to many

A style of [sqlalchemy.orm.relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) which links two tables together
via an intermediary table in the middle.   Using this configuration,
any number of rows on the left side may refer to any number of
rows on the right, and vice versa.

A schema where employees can be associated with projects:

```
CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE project (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE employee_project (
    employee_id INTEGER PRIMARY KEY,
    project_id INTEGER PRIMARY KEY,
    FOREIGN KEY employee_id REFERENCES employee(id),
    FOREIGN KEY project_id REFERENCES project(id)
)
```

Above, the `employee_project` table is the many-to-many table,
which naturally forms a composite primary key consisting
of the primary key from each related table.

In SQLAlchemy, the [sqlalchemy.orm.relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function
can represent this style of relationship in a mostly
transparent fashion, where the many-to-many table is
specified using plain table metadata:

```
class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    projects = relationship(
        "Project",
        secondary=Table(
            "employee_project",
            Base.metadata,
            Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
            Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
        ),
        backref="employees",
    )

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
```

Above, the `Employee.projects` and back-referencing `Project.employees`
collections are defined:

```
proj = Project(name="Client A")

emp1 = Employee(name="emp1")
emp2 = Employee(name="emp2")

proj.employees.extend([emp1, emp2])
```

See also

[association relationship](#term-association-relationship)

[relationship](#term-relationship)

[one to many](#term-one-to-many)

[many to one](#term-many-to-one)

   many to one

A style of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) which links
a foreign key in the parent mapper’s table to the primary
key of a related table.   Each parent object can
then refer to exactly zero or one related object.

The related objects in turn will have an implicit or
explicit [one to many](#term-one-to-many) relationship to any number
of parent objects that refer to them.

An example many to one schema (which, note, is identical
to the [one to many](#term-one-to-many) schema):

```
CREATE TABLE department (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    dep_id INTEGER REFERENCES department(id)
)
```

The relationship from `employee` to `department` is
many to one, since many employee records can be associated with a
single department.  A SQLAlchemy mapping might look like:

```
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dep_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department")
```

See also

[relationship](#term-relationship)

[one to many](#term-one-to-many)

[backref](#term-backref)

   mappingmappedmapped classORM mapped class

We say a class is “mapped” when it has been associated with an
instance of the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) class. This process associates
the class with a database table or other [selectable](#term-selectable) construct,
so that instances of it can be persisted and loaded using a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[ORM Mapped Class Overview](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)

   marshallingdata marshalling

The process of transforming the memory representation of an object to
a data format suitable for storage or transmission to another part of
a system, when data must be moved between different parts of a
computer program or from one program to another.   In terms of
SQLAlchemy, we often need to “marshal” data into a format appropriate
for passing into the relational database.

See also

[Marshalling (via Wikipedia)](https://en.wikipedia.org/wiki/Marshalling_(computer_science))

[Augmenting Existing Types](https://docs.sqlalchemy.org/en/20/core/custom_types.html#types-typedecorator) - SQLAlchemy’s [TypeDecorator](https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator)
is commonly used for data marshalling as data is sent into the
database for INSERT and UPDATE statements, and “unmarshalling”
data as it is retrieved using SELECT statements.

   metadatadatabase metadatatable metadata

The term “metadata” generally refers to “data that describes data”;
data that itself represents the format and/or structure of some other
kind of data.  In SQLAlchemy, the term “metadata” typically refers  to
the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) construct, which is a collection of information
about the tables, columns, constraints, and other [DDL](#term-DDL) objects
that may exist in a particular database.

See also

[Metadata Mapping (via Martin Fowler)](https://www.martinfowler.com/eaaCatalog/metadataMapping.html)

[Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata)  - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

   method chaininggenerative

“Method chaining”, referred to within SQLAlchemy documentation as
“generative”, is an object-oriented technique whereby the state of an
object is constructed by calling methods on the object. The object
features any number of methods, each of which return a new object (or
in some cases the same object) with additional state added to the
object.

The two SQLAlchemy objects that make the most use of
method chaining are the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
object and the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object.
For example, a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object can
be assigned two expressions to its WHERE clause as well
as an ORDER BY clause by calling upon the [Select.where()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.where)
and [Select.order_by()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by) methods:

```
stmt = (
    select(user.c.name)
    .where(user.c.id > 5)
    .where(user.c.name.like("e%"))
    .order_by(user.c.name)
)
```

Each method call above returns a copy of the original
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object with additional qualifiers
added.

  mixin classmixin classes

A common object-oriented pattern where a class that contains methods or
attributes for use by other classes without having to be the parent class
of those other classes.

See also

[Mixin (via Wikipedia)](https://en.wikipedia.org/wiki/Mixin)

   N plus one problemN plus one

The N plus one problem is a common side effect of the
[lazy load](#term-lazy-load) pattern, whereby an application wishes
to iterate through a related attribute or collection on
each member of a result set of objects, where that
attribute or collection is set to be loaded via the lazy
load pattern.   The net result is that a SELECT statement
is emitted to load the initial result set of parent objects;
then, as the application iterates through each member,
an additional SELECT statement is emitted for each member
in order to load the related attribute or collection for
that member.  The end result is that for a result set of
N parent objects, there will be N + 1 SELECT statements emitted.

The N plus one problem is alleviated using [eager loading](#term-eager-loading).

See also

[Loader Strategies](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-loader-strategies)

[Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)

   one to many

A style of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) which links
the primary key of the parent mapper’s table to the foreign
key of a related table.   Each unique parent object can
then refer to zero or more unique related objects.

The related objects in turn will have an implicit or
explicit [many to one](#term-many-to-one) relationship to their parent
object.

An example one to many schema (which, note, is identical
to the [many to one](#term-many-to-one) schema):

```
CREATE TABLE department (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30)
)

CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30),
    dep_id INTEGER REFERENCES department(id)
)
```

The relationship from `department` to `employee` is
one to many, since many employee records can be associated with a
single department.  A SQLAlchemy mapping might look like:

```
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    employees = relationship("Employee")

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dep_id = Column(Integer, ForeignKey("department.id"))
```

See also

[relationship](#term-relationship)

[many to one](#term-many-to-one)

[backref](#term-backref)

   ORM-annotatedannotations

The phrase “ORM-annotated” refers to an internal aspect of SQLAlchemy,
where a Core object such as a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object can carry along
additional runtime information that marks it as belonging to a particular
ORM mapping.   The term should not be confused with the common phrase
“type annotation”, which refers to Python source code “type hints” used
for static typing as introduced at [PEP 484](https://peps.python.org/pep-0484/).

Most of SQLAlchemy’s documented code examples are formatted with a
small note regarding “Annotated Example” or “Non-annotated Example”.
This refers to whether or not the example is [PEP 484](https://peps.python.org/pep-0484/) annotated,
and is not related to the SQLAlchemy concept of “ORM-annotated”.

When the phrase “ORM-annotated” appears in documentation, it is
referring to Core SQL expression objects such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), and [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) objects, which originate from,
or refer to sub-elements that originate from, one or more ORM mappings,
and therefore will have ORM-specific interpretations and/or behaviors
when passed to ORM methods such as [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).
For example, when we construct a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object from an ORM
mapping, such as the `User` class illustrated in the
[ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-declaring-mapped-classes):

```
>>> stmt = select(User)
```

The internal state of the above [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) refers to the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to which `User` is mapped.   The `User` class
itself is not immediately referenced.  This is how the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
construct remains compatible with Core-level processes (note that
the `._raw_columns` member of [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) is private and
should not be accessed by end-user code):

```
>>> stmt._raw_columns
[Table('user_account', MetaData(), Column('id', Integer(), ...)]
```

However, when our [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) is passed along to an ORM
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), the ORM entities that are indirectly associated
with the object are used to interpret this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) in an
ORM context.  The actual “ORM annotations” can be seen in another
private variable `._annotations`:

```
>>> stmt._raw_columns[0]._annotations
immutabledict({
  'entity_namespace': <Mapper at 0x7f4dd8098c10; User>,
  'parententity': <Mapper at 0x7f4dd8098c10; User>,
  'parentmapper': <Mapper at 0x7f4dd8098c10; User>
})
```

Therefore we refer to `stmt` as an **ORM-annotated select()** object.
It’s a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) statement that contains additional information
that will cause it to be interpreted in an ORM-specific way when passed
to methods like [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute).

  pending

This describes one of the major object states which
an object can have within a [Session](#term-Session); a pending object
is a new object that doesn’t have any database identity,
but has been recently associated with a session.   When
the session emits a flush and the row is inserted, the
object moves to the [persistent](#term-persistent) state.

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   persistent

This describes one of the major object states which
an object can have within a [Session](#term-Session); a persistent object
is an object that has a database identity (i.e. a primary key)
and is currently associated with a session.   Any object
that was previously [pending](#term-pending) and has now been inserted
is in the persistent state, as is any object that’s
been loaded by the session from the database.   When a
persistent object is removed from a session, it is known
as [detached](#term-detached).

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   pluginplugin-enabledplugin-specific

“plugin-enabled” or “plugin-specific” generally indicates a function or method in
SQLAlchemy Core which will behave differently when used in an ORM
context.

SQLAlchemy allows Core constructs such as [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) objects
to participate in a “plugin” system, which can inject additional
behaviors and features into the object that are not present by default.

Specifically, the primary “plugin” is the “orm” plugin, which is
at the base of the system that the SQLAlchemy ORM makes use of
Core constructs in order to compose and execute SQL queries that
return ORM results.

See also

[ORM Query Unified with Core Select](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-unify-select)

   polymorphicpolymorphically

Refers to a function that handles several types at once.  In SQLAlchemy,
the term is usually applied to the concept of an ORM mapped class
whereby a query operation will return different subclasses
based on information in the result set, typically by checking the
value of a particular column in the result known as the [discriminator](#term-discriminator).

Polymorphic loading in SQLAlchemy implies that a one or a
combination of three different schemes are used to map a hierarchy
of classes; “joined”, “single”, and “concrete”.   The section
[Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html) describes inheritance mapping fully.

  primary keyprimary key constraint

A [constraint](#term-constraint) that uniquely defines the characteristics
of each row in a table. The primary key has to consist of
characteristics that cannot be duplicated by any other row.
The primary key may consist of a single attribute or
multiple attributes in combination.
(via Wikipedia)

The primary key of a table is typically, though not always,
defined within the `CREATE TABLE` [DDL](#term-DDL):

```
CREATE TABLE employee (
     emp_id INTEGER,
     emp_name VARCHAR(30),
     dep_id INTEGER,
     PRIMARY KEY (emp_id)
)
```

See also

[composite primary key](#term-composite-primary-key)

[Primary key (via Wikipedia)](https://en.wikipedia.org/wiki/Primary_Key)

   read committed

One of the four database [isolation](#term-isolation) levels, read committed
features that the transaction will not be exposed to any data from
other concurrent transactions that has not been committed yet,
preventing so-called “dirty reads”.  However, under read committed
there can be non-repeatable reads, meaning data in a row may change
when read a second time if another transaction has committed changes.

  read uncommitted

One of the four database [isolation](#term-isolation) levels, read uncommitted
features that changes made to database data within a transaction will
not become permanent until the transaction is committed.   However,
within read uncommitted, it may be possible for data that is not
committed in other transactions to be viewable within the scope of
another transaction; these are known as “dirty reads”.

  reflectionreflected

In SQLAlchemy, this term refers to the feature of querying a database’s
schema catalogs in order to load information about existing tables,
columns, constraints, and other constructs.   SQLAlchemy includes
features that can both provide raw data for this information, as well
as that it can construct Core/ORM usable [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
from database schema catalogs automatically.

See also

[Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html) - complete background on
database reflection.

[Mapping Declaratively with Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected) - background on integrating
ORM mappings with reflected tables.

   registry

An object, typically globally accessible, that contains long-lived
information about some program state that is generally useful to many
parts of a program.

See also

[Registry (via Martin Fowler)](https://martinfowler.com/eaaCatalog/registry.html)

   relationalrelational algebra

An algebraic system developed by Edgar F. Codd that is used for
modelling and querying the data stored in relational databases.

See also

[Relational Algebra (via Wikipedia)](https://en.wikipedia.org/wiki/Relational_algebra)

   relationshiprelationships

A connecting unit between two mapped classes, corresponding
to some relationship between the two tables in the database.

The relationship is defined using the SQLAlchemy function
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).   Once created, SQLAlchemy
inspects the arguments and underlying mappings involved
in order to classify the relationship as one of three types:
[one to many](#term-one-to-many), [many to one](#term-many-to-one), or [many to many](#term-many-to-many).
With this classification, the relationship construct
handles the task of persisting the appropriate linkages
in the database in response to in-memory object associations,
as well as the job of loading object references and collections
into memory based on the current linkages in the
database.

See also

[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

   releasereleasesreleased

In the context of SQLAlchemy, the term “released”
refers to the process of ending the usage of a particular
database connection.    SQLAlchemy features the usage
of connection pools, which allows configurability as to
the lifespan of database connections.   When using a pooled
connection, the process of “closing” it, i.e. invoking
a statement like `connection.close()`, may have the effect
of the connection being returned to an existing pool,
or it may have the effect of actually shutting down the
underlying TCP/IP connection referred to by that connection -
which one takes place depends on configuration as well
as the current state of the pool.  So we used the term
*released* instead, to mean “do whatever it is you do
with connections when we’re done using them”.

The term will sometimes be used in the phrase, “release
transactional resources”, to indicate more explicitly that
what we are actually “releasing” is any transactional
state which as accumulated upon the connection.  In most
situations, the process of selecting from tables, emitting
updates, etc. acquires [isolated](#term-isolated) state upon
that connection as well as potential row or table locks.
This state is all local to a particular transaction
on the connection, and is released when we emit a rollback.
An important feature of the connection pool is that when
we return a connection to the pool, the `connection.rollback()`
method of the DBAPI is called as well, so that as the
connection is set up to be used again, it’s in a “clean”
state with no references held to the previous series
of operations.

See also

[Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)

   repeatable read

One of the four database [isolation](#term-isolation) levels, repeatable read
features all of the isolation of [read committed](#term-read-committed), and
additionally features that any particular row that is read within a
transaction is guaranteed from that point to not have any subsequent
external changes in value (i.e. from other concurrent UPDATE
statements) for the duration of that transaction.

  RETURNING

This is a non-SQL standard clause provided in various forms by
certain backends, which provides the service of returning a result
set upon execution of an INSERT, UPDATE or DELETE statement.  Any set
of columns from the matched rows can be returned, as though they were
produced from a SELECT statement.

The RETURNING clause provides both a dramatic performance boost to
common update/select scenarios, including retrieval of inline- or
default- generated primary key values and defaults at the moment they
were created, as well as a way to get at server-generated
default values in an atomic way.

An example of RETURNING, idiomatic to PostgreSQL, looks like:

```
INSERT INTO user_account (name) VALUES ('new name') RETURNING id, timestamp
```

Above, the INSERT statement will provide upon execution a result set
which includes the values of the columns `user_account.id` and
`user_account.timestamp`, which above should have been generated as default
values as they are not included otherwise (but note any series of columns
or SQL expressions can be placed into RETURNING, not just default-value columns).

The backends that currently support RETURNING or a similar construct
are PostgreSQL, SQL Server, Oracle Database, and Firebird.  The
PostgreSQL and Firebird implementations are generally full featured,
whereas the implementations of SQL Server and Oracle Database have
caveats. On SQL Server, the clause is known as “OUTPUT INSERTED” for
INSERT and UPDATE statements and “OUTPUT DELETED” for DELETE
statements; the key caveat is that triggers are not supported in
conjunction with this keyword.  In Oracle Database, it is known as
“RETURNING…INTO”, and requires that the value be placed into an OUT
parameter, meaning not only is the syntax awkward, but it can also only
be used for one row at a time.

SQLAlchemy’s [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) system provides a layer of abstraction
on top of the RETURNING systems of these backends to provide a consistent
interface for returning columns.  The ORM also includes many optimizations
that make use of RETURNING when available.

  selectable

A term used in SQLAlchemy to describe a SQL construct that represents
a collection of rows.   It’s largely similar to the concept of a
“relation” in [relational algebra](#term-relational-algebra).  In SQLAlchemy, objects
that subclass the [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable) class are considered to be
usable as “selectables” when using SQLAlchemy Core.  The two most
common constructs are that of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and that of the
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) statement.

  sentinelinsert sentinel

This is a SQLAlchemy-specific term that refers to a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) which can be used for a bulk
[insertmanyvalues](#term-insertmanyvalues) operation to track INSERTed data records
against rows passed back using RETURNING or similar.   Such a
column configuration is necessary for those cases when the
[insertmanyvalues](#term-insertmanyvalues) feature does an optimized INSERT..RETURNING
statement for many rows at once while still being able to guarantee the
order of returned rows matches the input data.

For typical use cases, the SQLAlchemy SQL compiler can automatically
make use of surrogate integer primary key columns as “insert
sentinels”, and no user-configuration is required.  For less common
cases with other varieties of server-generated primary key values,
explicit “insert sentinel” columns may be optionally configured within
[table metadata](#term-table-metadata) in order to optimize INSERT statements that
are inserting many rows at once.

See also

[Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order) - in the section
[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

   serializable

One of the four database [isolation](#term-isolation) levels, serializable
features all of the isolation of [repeatable read](#term-repeatable-read), and
additionally within a lock-based approach guarantees that so-called
“phantom reads” cannot occur; this means that rows which are INSERTed
or DELETEd within the scope of other transactions will not be
detectable within this transaction.   A row that is read within this
transaction is guaranteed to continue existing, and a row that does not
exist is guaranteed that it cannot appear of inserted from another
transaction.

Serializable isolation typically relies upon locking of rows or ranges
of rows in order to achieve this effect and can increase the chance of
deadlocks and degrade performance.   There are also non-lock based
schemes however these necessarily rely upon rejecting transactions if
write collisions are detected.

  Session

The container or scope for ORM database operations. Sessions
load instances from the database, track changes to mapped
instances and persist changes in a single unit of work when
flushed.

See also

[Using the Session](https://docs.sqlalchemy.org/en/20/orm/session.html)

   subqueryscalar subquery

Refers to a `SELECT` statement that is embedded within an enclosing
`SELECT`.

A subquery comes in two general flavors, one known as a “scalar select”
which specifically must return exactly one row and one column, and the
other form which acts as a “derived table” and serves as a source of
rows for the FROM clause of another select.  A scalar select is eligible
to be placed in the [WHERE clause](#term-WHERE-clause), [columns clause](#term-columns-clause),
ORDER BY clause or HAVING clause of the enclosing select, whereas the
derived table form is eligible to be placed in the FROM clause of the
enclosing `SELECT`.

Examples:

1. a scalar subquery placed in the [columns clause](#term-columns-clause) of an enclosing
  `SELECT`.  The subquery in this example is a [correlated subquery](#term-correlated-subquery) because part
  of the rows which it selects from are given via the enclosing statement.
  ```
  SELECT id, (SELECT name FROM address WHERE address.user_id=user.id)
  FROM user
  ```
2. a scalar subquery placed in the [WHERE clause](#term-WHERE-clause) of an enclosing
  `SELECT`.  This subquery in this example is not correlated as it selects a fixed result.
  ```
  SELECT id, name FROM user
  WHERE status=(SELECT status_id FROM status_code WHERE code='C')
  ```
3. a derived table subquery placed in the [FROM clause](#term-FROM-clause) of an enclosing
  `SELECT`.   Such a subquery is almost always given an alias name.
  ```
  SELECT user.id, user.name, ad_subq.email_address
  FROM
      user JOIN
      (select user_id, email_address FROM address WHERE address_type='Q') AS ad_subq
      ON user.id = ad_subq.user_id
  ```

  transient

This describes one of the major object states which
an object can have within a [Session](#term-Session); a transient object
is a new object that doesn’t have any database identity
and has not been associated with a session yet.  When the
object is added to the session, it moves to the
[pending](#term-pending) state.

See also

[Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-object-states)

   unique constraintunique key index

A unique key index can uniquely identify each row of data
values in a database table. A unique key index comprises a
single column or a set of columns in a single database table.
No two distinct rows or data records in a database table can
have the same data value (or combination of data values) in
those unique key index columns if NULL values are not used.
Depending on its design, a database table may have many unique
key indexes but at most one primary key index.

(via Wikipedia)

See also

[Unique key (via Wikipedia)](https://en.wikipedia.org/wiki/Unique_key#Defining_unique_keys)

   unit of work

A software architecture where a persistence system such as an object
relational mapper maintains a list of changes made to a series of
objects, and periodically flushes all those pending changes out to the
database.

SQLAlchemy’s [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) implements the unit of work pattern,
where objects that are added to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) using methods
like [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) will then participate in unit-of-work
style persistence.

For a walk-through of what unit of work persistence looks like in
SQLAlchemy, start with the section [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation)
in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).    Then for more detail, see
[Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1) in the general reference documentation.

See also

[Unit of Work (via Martin Fowler)](https://martinfowler.com/eaaCatalog/unitOfWork.html)

[Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation)

[Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

   version id column

In SQLAlchemy, this refers to the use of a particular table column that
tracks the “version” of a particular row, as the row changes values.   While
there are different kinds of relational patterns that make use of a
“version id column” in different ways, SQLAlchemy’s ORM includes a particular
feature that allows for such a column to be configured as a means of
testing for stale data when a row is being UPDATEd with new information.
If the last known “version” of this column does not match that of the
row when we try to put new data into the row, we know that we are
acting on stale information.

There are also other ways of storing “versioned” rows in a database,
often referred to as “temporal” data.  In addition to SQLAlchemy’s
versioning feature, a few more examples are also present in the
documentation, see the links below.

See also

[Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html#mapper-version-counter) - SQLAlchemy’s built-in version id feature.

[Versioning Objects](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-versioning) - other examples of mappings that version rows
temporally.

   WHERE clause

The portion of the `SELECT` statement which indicates criteria
by which rows should be filtered.   It is a single SQL expression
which follows the keyword `WHERE`.

```
SELECT user_account.name, user_account.email
FROM user_account
WHERE user_account.name = 'fred' AND user_account.status = 'E'
```

Above, the phrase `WHERE user_account.name = 'fred' AND user_account.status = 'E'`
comprises the WHERE clause of the `SELECT`.
