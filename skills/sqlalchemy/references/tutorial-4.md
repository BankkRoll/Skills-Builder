# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

SQLAlchemy 1.4 / 2.0 Tutorial

This page is part of the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

Previous: [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html)   |   Next: [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html)

# Working with Database Metadata

With engines and SQL execution down, we are ready to begin some Alchemy.
The central element of both SQLAlchemy Core and ORM is the SQL Expression
Language which allows for fluent, composable construction of SQL queries.
The foundation for these queries are Python objects that represent database
concepts like tables and columns.   These objects are known collectively
as [database metadata](https://docs.sqlalchemy.org/en/20/glossary.html#term-database-metadata).

The most common foundational objects for database metadata in SQLAlchemy are
known as  [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
The sections below will illustrate how these objects are used in both a
Core-oriented style as well as an ORM-oriented style.

**ORM readers, stay with us!**

As with other sections, Core users can skip the ORM sections, but ORM users
would best be familiar with these objects from both perspectives.
The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object discussed here is declared in a more indirect
(and also fully Python-typed) way when using the ORM, however there is still
a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object within the ORM’s configuration.

## Setting up MetaData with Table objects

When we work with a relational database, the basic data-holding structure
in the database which we query from is known as a **table**.
In SQLAlchemy, the database “table” is ultimately represented
by a Python object similarly named [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

To start using the SQLAlchemy Expression Language, we will want to have
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects constructed that represent all of the database
tables we are interested in working with. The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is
constructed programmatically, either directly by using the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) constructor, or indirectly by using ORM Mapped classes
(described later at [Using ORM Declarative Forms to Define Table Metadata](#tutorial-orm-table-metadata)).  There is also the
option to load some or all table information from an existing database,
called [reflection](https://docs.sqlalchemy.org/en/20/glossary.html#term-reflection).

Whichever kind of approach is used, we always start out with a collection
that will be where we place our tables known as the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
object.  This object is essentially a [facade](https://docs.sqlalchemy.org/en/20/glossary.html#term-facade) around a Python dictionary
that stores a series of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects keyed to their string
name.   While the ORM provides some options on where to get this collection,
we always have the option to simply make one directly, which looks like:

```
>>> from sqlalchemy import MetaData
>>> metadata_obj = MetaData()
```

Once we have a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object, we can declare some
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects. This tutorial will start with the classic
SQLAlchemy tutorial model, which has a table called `user_account` that
stores, for example, the users of a website, and a related table `address`,
which stores email addresses associated with rows in the `user_account`
table. When not using ORM Declarative models at all, we construct each
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object directly, typically assigning each to a variable
that will be how we will refer to the table in application code:

```
>>> from sqlalchemy import Table, Column, Integer, String
>>> user_table = Table(
...     "user_account",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30)),
...     Column("fullname", String),
... )
```

With the above example, when we wish to write code that refers to the
`user_account` table in the database, we will use the `user_table`
Python variable to refer to it.

When do I make a `MetaData` object in my program?

Having a single [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object for an entire application is
the most common case, represented as a module-level variable in a single place
in an application, often in a “models” or “dbschema” type of package. It is
also very common that the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) is accessed via an
ORM-centric [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) or
[Declarative Base](#tutorial-orm-declarative-base) base class, so that
this same [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) is shared among ORM- and Core-declared
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.

There can be multiple [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collections as well;
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects can refer to [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
in other collections without restrictions. However, for groups of
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that are related to each other, it is in
practice much more straightforward to have them set up within a single
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection, both from the perspective of declaring
them, as well as from the perspective of DDL (i.e. CREATE and DROP) statements
being emitted in the correct order.

### Components ofTable

We can observe that the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct as written in Python
has a resemblance to a SQL CREATE TABLE statement; starting with the table
name, then listing out each column, where each column has a name and a
datatype. The objects we use above are:

- [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) - represents a database table and assigns itself
  to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection.
- [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) - represents a column in a database table, and
  assigns itself to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.   The [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  usually includes a string name and a type object.   The collection of
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects in terms of the parent [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  are typically accessed via an associative array located at [Table.c](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.c):
  ```
  >>> user_table.c.name
  Column('name', String(length=30), table=<user_account>)
  >>> user_table.c.keys()
  ['id', 'name', 'fullname']
  ```
- [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer), [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) - these classes represent
  SQL datatypes and can be passed to a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) with or without
  necessarily being instantiated.  Above, we want to give a length of “30” to
  the “name” column, so we instantiated `String(30)`.  But for “id” and
  “fullname” we did not specify these, so we can send the class itself.

See also

The reference and API documentation for [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData),
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) is at [Describing Databases with MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html).
The reference documentation for datatypes is at [SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html).

In an upcoming section, we will illustrate one of the fundamental
functions of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) which
is to generate [DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL) on a particular database connection.  But first
we will declare a second [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

### Declaring Simple Constraints

The first [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) in the example `user_table` includes the
[Column.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.primary_key) parameter which is a shorthand technique
of indicating that this [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) should be part of the primary
key for this table.  The primary key itself is normally declared implicitly
and is represented by the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) construct,
which we can see on the [Table.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.primary_key)
attribute on the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object:

```
>>> user_table.primary_key
PrimaryKeyConstraint(Column('id', Integer(), table=<user_account>, primary_key=True, nullable=False))
```

The constraint that is most typically declared explicitly is the
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object that corresponds to a database
[foreign key constraint](https://docs.sqlalchemy.org/en/20/glossary.html#term-foreign-key-constraint).  When we declare tables that are related to
each other, SQLAlchemy uses the presence of these foreign key constraint
declarations not only so that they are emitted within CREATE statements to
the database, but also to assist in constructing SQL expressions.

A [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) that involves only a single column
on the target table is typically declared using a column-level shorthand notation
via the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object.  Below we declare a second table
`address` that will have a foreign key constraint referring to the `user`
table:

```
>>> from sqlalchemy import ForeignKey
>>> address_table = Table(
...     "address",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("user_id", ForeignKey("user_account.id"), nullable=False),
...     Column("email_address", String, nullable=False),
... )
```

The table above also features a third kind of constraint, which in SQL is the
“NOT NULL” constraint, indicated above using the [Column.nullable](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.nullable)
parameter.

Tip

When using the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object within a
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) definition, we can omit the datatype for that
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column); it is automatically inferred from that of the
related column, in the above example the [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) datatype
of the `user_account.id` column.

In the next section we will emit the completed DDL for the `user` and
`address` table to see the completed result.

### Emitting DDL to the Database

We’ve constructed an object structure that represents
two database tables in a database, starting at the root [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
object, then into two [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, each of which hold
onto a collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint)
objects.   This object structure will be at the center of most operations
we perform with both Core and ORM going forward.

The first useful thing we can do with this structure will be to emit CREATE
TABLE statements, or [DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL), to our SQLite database so that we can insert
and query data from them.   We have already all the tools needed to do so, by
invoking the
[MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) method on our [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData),
sending it the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) that refers to the target database:

```
>>> metadata_obj.create_all(engine)
BEGIN (implicit)
PRAGMA main.table_...info("user_account")
...
PRAGMA main.table_...info("address")
...
CREATE TABLE user_account (
    id INTEGER NOT NULL,
    name VARCHAR(30),
    fullname VARCHAR,
    PRIMARY KEY (id)
)
...
CREATE TABLE address (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    email_address VARCHAR NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user_account (id)
)
...
COMMIT
```

The DDL create process above includes some SQLite-specific PRAGMA statements
that test for the existence of each table before emitting a CREATE.   The full
series of steps are also included within a BEGIN/COMMIT pair to accommodate
for transactional DDL.

The create process also takes care of emitting CREATE statements in the correct
order; above, the FOREIGN KEY constraint is dependent on the `user` table
existing, so the `address` table is created second.   In more complicated
dependency scenarios the FOREIGN KEY constraints may also be applied to tables
after the fact using ALTER.

The [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object also features a
[MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all) method that will emit DROP statements in the
reverse order as it would emit CREATE in order to drop schema elements.

Migration tools are usually appropriate

Overall, the CREATE / DROP feature of [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) is useful
for test suites, small and/or new applications, and applications that use
short-lived databases.  For management of an application database schema
over the long term however, a schema management tool such as [Alembic](https://alembic.sqlalchemy.org), which builds upon SQLAlchemy, is likely
a better choice, as it can manage and orchestrate the process of
incrementally altering a fixed database schema over time as the design of
the application changes.

## Using ORM Declarative Forms to Define Table Metadata

Another way to make Table objects?

The preceding examples illustrated direct use of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object, which underlies how SQLAlchemy ultimately refers to database tables
when constructing SQL expressions. As mentioned, the SQLAlchemy ORM provides
for a facade around the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) declaration process referred
towards as **Declarative Table**.   The Declarative Table process accomplishes
the same goal as we had in the previous section, that of building
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, but also within that process gives us
something else called an [ORM mapped class](https://docs.sqlalchemy.org/en/20/glossary.html#term-ORM-mapped-class), or just “mapped class”.
The mapped class is the
most common foundational unit of SQL when using the ORM, and in modern
SQLAlchemy can also be used quite effectively with Core-centric
use as well.

Some benefits of using Declarative Table include:

- A more succinct and Pythonic style of setting up column definitions, where
  Python types may be used to represent SQL types to be used in the
  database
- The resulting mapped class can be
  used to form SQL expressions that in many cases maintain [PEP 484](https://peps.python.org/pep-0484/) typing
  information that’s picked up by static analysis tools such as
  Mypy and IDE type checkers
- Allows declaration of table metadata and the ORM mapped class used in
  persistence / object loading operations all at once.

This section will illustrate the same [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata
of the previous section(s) being constructed using Declarative Table.

When using the ORM, the process by which we declare [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata
is usually combined with the process of declaring [mapped](https://docs.sqlalchemy.org/en/20/glossary.html#term-mapped) classes.
The mapped class is any Python class we’d like to create, which will then
have attributes on it that will be linked to the columns in a database table.
While there are a few varieties of how this is achieved, the most common
style is known as
[declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html), and allows us
to declare our user-defined classes and [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) metadata
at once.

### Establishing a Declarative Base

When using the ORM, the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection remains present,
however it itself is associated with an ORM-only construct commonly referred
towards as the **Declarative Base**.   The most expedient way to acquire
a new Declarative Base is to create a new class that subclasses the
SQLAlchemy [DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) class:

```
>>> from sqlalchemy.orm import DeclarativeBase
>>> class Base(DeclarativeBase):
...     pass
```

Above, the `Base` class is what we’ll call the Declarative Base.
When we make new classes that are subclasses of `Base`, combined with
appropriate class-level directives, they will each be established as a new
**ORM mapped class** at class creation time, each one typically (but not
exclusively) referring to a particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.

The Declarative Base refers to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection that is
created for us automatically, assuming we didn’t provide one from the outside.
This [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection is accessible via the
[DeclarativeBase.metadata](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.metadata) class-level attribute. As we create new
mapped classes, they each will reference a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) within this
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection:

```
>>> Base.metadata
MetaData()
```

The Declarative Base also refers to a collection called [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry), which
is the central “mapper configuration” unit in the SQLAlchemy ORM.  While
seldom accessed directly, this object is central to the mapper configuration
process, as a set of ORM mapped classes will coordinate with each other via
this registry.   As was the case with [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData), our Declarative
Base also created a [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) for us (again with options to
pass our own [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)), which we can access
via the [DeclarativeBase.registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.registry) class variable:

```
>>> Base.registry
<sqlalchemy.orm.decl_api.registry object at 0x...>
```

Other ways to map with the `registry`

[DeclarativeBase](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase) is not the only way to map classes, only the
most common.  [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) also provides other mapper
configurational patterns, including decorator-oriented and imperative ways
to map classes.  There’s also full support for creating Python dataclasses
while mapping.  The reference documentation at [ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html)
has it all.

### Declaring Mapped Classes

With the `Base` class established, we can now define ORM mapped classes
for the `user_account` and `address` tables in terms of new classes `User` and
`Address`.  We illustrate below the most modern form of Declarative, which
is driven from [PEP 484](https://peps.python.org/pep-0484/) type annotations using a special type
[Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped), which indicates attributes to be mapped as particular
types:

```
>>> from typing import List
>>> from typing import Optional
>>> from sqlalchemy.orm import Mapped
>>> from sqlalchemy.orm import mapped_column
>>> from sqlalchemy.orm import relationship

>>> class User(Base):
...     __tablename__ = "user_account"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     name: Mapped[str] = mapped_column(String(30))
...     fullname: Mapped[Optional[str]]
...
...     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
...
...     def __repr__(self) -> str:
...         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

>>> class Address(Base):
...     __tablename__ = "address"
...
...     id: Mapped[int] = mapped_column(primary_key=True)
...     email_address: Mapped[str]
...     user_id = mapped_column(ForeignKey("user_account.id"))
...
...     user: Mapped[User] = relationship(back_populates="addresses")
...
...     def __repr__(self) -> str:
...         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

The two classes above, `User` and `Address`, are now called
as **ORM Mapped Classes**, and are available for use in
ORM persistence and query operations, which will be described later.  Details
about these classes include:

- Each class refers to a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object that was generated as
  part of the declarative mapping process, which is named by assigning
  a string to the [DeclarativeBase.__tablename__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__tablename__) attribute.
  Once the class is created, this generated [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is available
  from the [DeclarativeBase.__table__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__table__) attribute.
- As mentioned previously, this form
  is known as [Declarative Table Configuration](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-configuration).  One
  of several alternative declaration styles would instead have us
  build the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object directly, and **assign** it
  directly to [DeclarativeBase.__table__](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.__table__).  This style
  is known as [Declarative with Imperative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration).
- To indicate columns in the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), we use the
  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct, in combination with
  typing annotations based on the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) type.  This object
  will generate [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that are applied to the
  construction of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
- For columns with simple datatypes and no other options, we can indicate a
  [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) type annotation alone, using simple Python types like
  `int` and `str` to mean [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) and [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String).
  Customization of how Python types are interpreted within the Declarative
  mapping process is very open ended; see the sections
  [ORM Annotated Declarative - Complete Guide](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column) and
  [Customizing the Type Map](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map) for background.
- A column can be declared as “nullable” or “not null” based on the
  presence of the `Optional[<typ>]` type annotation (or its equivalents,
  `<typ> | None` or `Union[<typ>, None]`).  The
  [mapped_column.nullable](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column.params.nullable) parameter may also be used explicitly
  (and does not have to match the annotation’s optionality).
- Use of explicit typing annotations is **completely
  optional**.  We can also use [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) without annotations.
  When using this form, we would use more explicit type objects like
  [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) and [String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String) as well as `nullable=False`
  as needed within each [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct.
- Two additional attributes, `User.addresses` and `Address.user`, define
  a different kind of attribute called [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), which
  features similar annotation-aware configuration styles as shown.  The
  [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct is discussed more fully at
  [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects).
- The classes are automatically given an `__init__()` method if we don’t
  declare one of our own.  The default form of this method accepts all
  attribute names as optional keyword arguments:
  ```
  >>> sandy = User(name="sandy", fullname="Sandy Cheeks")
  ```
  To automatically generate a full-featured `__init__()` method which
  provides for positional arguments as well as arguments with default keyword
  values, the dataclasses feature introduced at
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) may be used.  It’s of course
  always an option to use an explicit `__init__()` method as well.
- The `__repr__()` methods are added so that we get a readable string output;
  there’s no requirement for these methods to be here.  As is the case
  with `__init__()`, a `__repr__()` method
  can be generated automatically by using the
  [dataclasses](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) feature.

Where’d the old Declarative go?

Users of SQLAlchemy 1.4 or previous will note that the above mapping
uses a dramatically different form than before; not only does it use
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) instead of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) in the Declarative
mapping, it also uses Python type annotations to derive column information.

To provide context for users of the “old” way, Declarative mappings can
still be made using [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects (as well as using the
[declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base) function to create the base class) as before,
and these forms will continue to be supported with no plans to
remove support.  The reason these two facilities
are superseded by new constructs is first and foremost to integrate
smoothly with [PEP 484](https://peps.python.org/pep-0484/) tools, including IDEs such as VSCode and type
checkers such as Mypy and Pyright, without the need for plugins. Secondly,
deriving the declarations from type annotations is part of SQLAlchemy’s
integration with Python dataclasses, which can now be
[generated natively](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses) from mappings.

For users who like the “old” way, but still desire their IDEs to not
mistakenly report typing errors for their declarative mappings, the
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) construct is a drop-in replacement for
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) in an ORM Declarative mapping (note that
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) is for ORM Declarative mappings only; it can’t
be used within a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) construct), and the type annotations are
optional. Our mapping above can be written without annotations as:

```
class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False)
    fullname = mapped_column(String)

    addresses = relationship("Address", back_populates="user")

    # ... definition continues
```

The above class has an advantage over one that uses [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
directly, in that the `User` class as well as instances of `User`
will indicate the correct typing information to typing tools, without
the use of plugins.  [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) also allows for additional
ORM-specific parameters to configure behaviors such as deferred column loading,
which previously needed a separate [deferred()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.deferred) function to be
used with [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

There’s also an example of converting an old-style Declarative class
to the new style, which can be seen at [ORM Declarative Models](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing)
in the [What’s New in SQLAlchemy 2.0?](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html) guide.

See also

[ORM Mapping Styles](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles) - full background on different ORM configurational
styles.

[Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping) - overview of Declarative class mapping

[Declarative Table with mapped_column()](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table) - detail on how to use
[mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column) and [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) to define the columns
within a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to be mapped when using Declarative.

### Emitting DDL to the database from an ORM mapping

As our ORM mapped classes refer to [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects contained
within a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection, emitting DDL given the
Declarative Base uses the same process as that described previously at
[Emitting DDL to the Database](#tutorial-emitting-ddl). In our case, we have already generated the
`user` and `address` tables in our SQLite database. If we had not done so
already, we would be free to make use of the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
associated with our ORM Declarative Base class in order to do so, by accessing
the collection from the [DeclarativeBase.metadata](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.DeclarativeBase.metadata) attribute and
then using [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) as before.  In this case,
PRAGMA statements are run, but no new tables are generated since they
are found to be present already:

```
>>> Base.metadata.create_all(engine)
BEGIN (implicit)
PRAGMA main.table_...info("user_account")
...
PRAGMA main.table_...info("address")
...
COMMIT
```

## Table Reflection

Optional Section

This section is just a brief introduction to the related subject of
**table reflection**, or how to generate [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects automatically from an existing database.  Tutorial readers who
want to get on with writing queries can feel free to skip this section.

To round out the section on working with table metadata, we will illustrate
another operation that was mentioned at the beginning of the section,
that of **table reflection**.   Table reflection refers to the process of
generating [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and related objects by reading the current
state of a database.   Whereas in the previous sections we’ve been declaring
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in Python, where we then have the option
to emit DDL to the database to generate such a schema, the reflection process
does these two steps in reverse, starting from an existing database
and generating in-Python data structures to represent the schemas within
that database.

Tip

There is no requirement that reflection must be used in order to
use SQLAlchemy with a pre-existing database.  It is entirely typical that
the SQLAlchemy application declares all metadata explicitly in Python,
such that its structure corresponds to the existing database.
The metadata structure also need not include tables, columns, or other
constraints and constructs in the pre-existing database that are not needed
for the local application to function.

As an example of reflection, we will create a new [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object which represents the `some_table` object we created manually in
the earlier sections of this document.  There are again some varieties of
how this is performed, however the most basic is to construct a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, given the name of the table and a
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection to which it will belong, then
instead of indicating individual [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) and
[Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) objects, pass it the target [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
using the [Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with) parameter:

```
>>> some_table = Table("some_table", metadata_obj, autoload_with=engine)
BEGIN (implicit)
PRAGMA main.table_...info("some_table")
[raw sql] ()
SELECT sql FROM  (SELECT * FROM sqlite_master UNION ALL   SELECT * FROM sqlite_temp_master) WHERE name = ? AND type in ('table', 'view')
[raw sql] ('some_table',)
PRAGMA main.foreign_key_list("some_table")
...
PRAGMA main.index_list("some_table")
...
ROLLBACK
```

At the end of the process, the `some_table` object now contains the
information about the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects present in the table, and
the object is usable in exactly the same way as a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that
we declared explicitly:

```
>>> some_table
Table('some_table', MetaData(),
    Column('x', INTEGER(), table=<some_table>),
    Column('y', INTEGER(), table=<some_table>),
    schema=None)
```

See also

Read more about table and schema reflection at [Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html).

For ORM-related variants of table reflection, the section
[Mapping Declaratively with Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected) includes an overview of the available
options.

## Next Steps

We now have a SQLite database ready to go with two tables present, and
Core and ORM table-oriented constructs that we can use to interact with
these tables via a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and/or ORM
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  In the following sections, we will illustrate
how to create, manipulate, and select data using these structures.

SQLAlchemy 1.4 / 2.0 Tutorial

Next Tutorial Section: [Working with Data](https://docs.sqlalchemy.org/en/20/tutorial/data.html)
