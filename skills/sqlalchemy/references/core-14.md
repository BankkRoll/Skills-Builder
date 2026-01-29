# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Describing Databases with MetaData

This section discusses the fundamental [Table](#sqlalchemy.schema.Table), [Column](#sqlalchemy.schema.Column)
and [MetaData](#sqlalchemy.schema.MetaData) objects.

See also

[Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata) - tutorial introduction to
SQLAlchemy’s database metadata concept in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

A collection of metadata entities is stored in an object aptly named
[MetaData](#sqlalchemy.schema.MetaData):

```
from sqlalchemy import MetaData

metadata_obj = MetaData()
```

[MetaData](#sqlalchemy.schema.MetaData) is a container object that keeps together
many different features of a database (or multiple databases) being described.

To represent a table, use the [Table](#sqlalchemy.schema.Table) class. Its two
primary arguments are the table name, then the
[MetaData](#sqlalchemy.schema.MetaData) object which it will be associated with.
The remaining positional arguments are mostly
[Column](#sqlalchemy.schema.Column) objects describing each column:

```
from sqlalchemy import Table, Column, Integer, String

user = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("email_address", String(60)),
    Column("nickname", String(50), nullable=False),
)
```

Above, a table called `user` is described, which contains four columns. The
primary key of the table consists of the `user_id` column. Multiple columns
may be assigned the `primary_key=True` flag which denotes a multi-column
primary key, known as a *composite* primary key.

Note also that each column describes its datatype using objects corresponding
to genericized types, such as [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) and
[String](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String). SQLAlchemy features dozens of types of
varying levels of specificity as well as the ability to create custom types.
Documentation on the type system can be found at [SQL Datatype Objects](https://docs.sqlalchemy.org/en/20/core/types.html).

## Accessing Tables and Columns

The [MetaData](#sqlalchemy.schema.MetaData) object contains all of the schema
constructs we’ve associated with it. It supports a few methods of accessing
these table objects, such as the `sorted_tables` accessor which returns a
list of each [Table](#sqlalchemy.schema.Table) object in order of foreign key
dependency (that is, each table is preceded by all tables which it
references):

```
>>> for t in metadata_obj.sorted_tables:
...     print(t.name)
user
user_preference
invoice
invoice_item
```

In most cases, individual [Table](#sqlalchemy.schema.Table) objects have been
explicitly declared, and these objects are typically accessed directly as
module-level variables in an application. Once a
[Table](#sqlalchemy.schema.Table) has been defined, it has a full set of
accessors which allow inspection of its properties. Given the following
[Table](#sqlalchemy.schema.Table) definition:

```
employees = Table(
    "employees",
    metadata_obj,
    Column("employee_id", Integer, primary_key=True),
    Column("employee_name", String(60), nullable=False),
    Column("employee_dept", Integer, ForeignKey("departments.department_id")),
)
```

Note the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object used in this table -
this construct defines a reference to a remote table, and is fully described
in [Defining Foreign Keys](https://docs.sqlalchemy.org/en/20/core/constraints.html#metadata-foreignkeys). Methods of accessing information about this
table include:

```
# access the column "employee_id":
employees.columns.employee_id

# or just
employees.c.employee_id

# via string
employees.c["employee_id"]

# a tuple of columns may be returned using multiple strings
# (new in 2.0)
emp_id, name, type = employees.c["employee_id", "name", "type"]

# iterate through all columns
for c in employees.c:
    print(c)

# get the table's primary key columns
for primary_key in employees.primary_key:
    print(primary_key)

# get the table's foreign key objects:
for fkey in employees.foreign_keys:
    print(fkey)

# access the table's MetaData:
employees.metadata

# access a column's name, type, nullable, primary key, foreign key
employees.c.employee_id.name
employees.c.employee_id.type
employees.c.employee_id.nullable
employees.c.employee_id.primary_key
employees.c.employee_dept.foreign_keys

# get the "key" of a column, which defaults to its name, but can
# be any user-defined string:
employees.c.employee_name.key

# access a column's table:
employees.c.employee_id.table is employees

# get the table related by a foreign key
list(employees.c.employee_dept.foreign_keys)[0].column.table
```

Tip

The [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) collection, synonymous with the
[FromClause.columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.columns) collection, is an instance of
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection), which provides a **dictionary-like interface**
to the collection of columns.   Names are ordinarily accessed like
attribute names, e.g. `employees.c.employee_name`.  However for special names
with spaces or those that match the names of dictionary methods such as
[ColumnCollection.keys()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.keys) or [ColumnCollection.values()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.values),
indexed access must be used, such as `employees.c['values']` or
`employees.c["some column"]`.  See [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) for
further information.

## Creating and Dropping Database Tables

Once you’ve defined some [Table](#sqlalchemy.schema.Table) objects, assuming
you’re working with a brand new database one thing you might want to do is
issue CREATE statements for those tables and their related constructs (as an
aside, it’s also quite possible that you *don’t* want to do this, if you
already have some preferred methodology such as tools included with your
database or an existing scripting system - if that’s the case, feel free to
skip this section - SQLAlchemy has no requirement that it be used to create
your tables).

The usual way to issue CREATE is to use
[create_all()](#sqlalchemy.schema.MetaData.create_all) on the
[MetaData](#sqlalchemy.schema.MetaData) object. This method will issue queries
that first check for the existence of each individual table, and if not found
will issue the CREATE statements:

```
engine = create_engine("sqlite:///:memory:")

metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("email_address", String(60), key="email"),
    Column("nickname", String(50), nullable=False),
)

user_prefs = Table(
    "user_prefs",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)

metadata_obj.create_all(engine)
PRAGMA table_info(user){}
CREATE TABLE user(
        user_id INTEGER NOT NULL PRIMARY KEY,
        user_name VARCHAR(16) NOT NULL,
        email_address VARCHAR(60),
        nickname VARCHAR(50) NOT NULL
)
PRAGMA table_info(user_prefs){}
CREATE TABLE user_prefs(
        pref_id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES user(user_id),
        pref_name VARCHAR(40) NOT NULL,
        pref_value VARCHAR(100)
)
```

[create_all()](#sqlalchemy.schema.MetaData.create_all) creates foreign key constraints
between tables usually inline with the table definition itself, and for this
reason it also generates the tables in order of their dependency. There are
options to change this behavior such that `ALTER TABLE` is used instead.

Dropping all tables is similarly achieved using the
[drop_all()](#sqlalchemy.schema.MetaData.drop_all) method. This method does the
exact opposite of [create_all()](#sqlalchemy.schema.MetaData.create_all) - the
presence of each table is checked first, and tables are dropped in reverse
order of dependency.

Creating and dropping individual tables can be done via the `create()` and
`drop()` methods of [Table](#sqlalchemy.schema.Table). These methods by
default issue the CREATE or DROP regardless of the table being present:

```
engine = create_engine("sqlite:///:memory:")

metadata_obj = MetaData()

employees = Table(
    "employees",
    metadata_obj,
    Column("employee_id", Integer, primary_key=True),
    Column("employee_name", String(60), nullable=False, key="name"),
    Column("employee_dept", Integer, ForeignKey("departments.department_id")),
)
employees.create(engine)
CREATE TABLE employees(
    employee_id SERIAL NOT NULL PRIMARY KEY,
    employee_name VARCHAR(60) NOT NULL,
    employee_dept INTEGER REFERENCES departments(department_id)
)
{}
```

`drop()` method:

```
employees.drop(engine)
DROP TABLE employees
{}
```

To enable the “check first for the table existing” logic, add the
`checkfirst=True` argument to `create()` or `drop()`:

```
employees.create(engine, checkfirst=True)
employees.drop(engine, checkfirst=False)
```

## Altering Database Objects through Migrations

While SQLAlchemy directly supports emitting CREATE and DROP statements for
schema constructs, the ability to alter those constructs, usually via the ALTER
statement as well as other database-specific constructs, is outside of the
scope of SQLAlchemy itself.  While it’s easy enough to emit ALTER statements
and similar by hand, such as by passing a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct to
[Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) or by using the [DDL](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.DDL) construct, it’s a
common practice to automate the maintenance of database schemas in relation to
application code using schema migration tools.

The SQLAlchemy project offers the  [Alembic](https://alembic.sqlalchemy.org)
migration tool for this purpose.   Alembic features a highly customizable
environment and a minimalistic usage pattern, supporting such features as
transactional DDL, automatic generation of “candidate” migrations, an “offline”
mode which generates SQL scripts, and support for branch resolution.

Alembic supersedes the [SQLAlchemy-Migrate](https://github.com/openstack/sqlalchemy-migrate)   project, which is the
original migration tool for SQLAlchemy and is now  considered legacy.

## Specifying the Schema Name

Most databases support the concept of multiple “schemas” - namespaces that
refer to alternate sets of tables and other constructs.  The server-side
geometry of a “schema” takes many forms, including names of “schemas” under the
scope of a particular database (e.g. PostgreSQL schemas), named sibling
databases (e.g. MySQL / MariaDB access to other databases on the same server),
as well as other concepts like tables owned by other usernames (Oracle
Database, SQL Server) or even names that refer to alternate database files
(SQLite ATTACH) or remote servers (Oracle Database DBLINK with synonyms).

What all of the above approaches have (mostly) in common is that there’s a way
of referencing this alternate set of tables using a string name.  SQLAlchemy
refers to this name as the **schema name**.  Within SQLAlchemy, this is nothing
more than a string name which is associated with a [Table](#sqlalchemy.schema.Table)
object, and is then rendered into SQL statements in a manner appropriate to the
target database such that the table is referenced in its remote “schema”,
whatever mechanism that is on the target database.

The “schema” name may be associated directly with a [Table](#sqlalchemy.schema.Table)
using the [Table.schema](#sqlalchemy.schema.Table.params.schema) argument; when using the ORM
with [declarative table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) configuration,
the parameter is passed using the `__table_args__` parameter dictionary.

The “schema” name may also be associated with the [MetaData](#sqlalchemy.schema.MetaData)
object where it will take effect automatically for all [Table](#sqlalchemy.schema.Table)
objects associated with that [MetaData](#sqlalchemy.schema.MetaData) that don’t otherwise
specify their own name.  Finally, SQLAlchemy also supports a “dynamic” schema name
system that is often used for multi-tenant applications such that a single set
of [Table](#sqlalchemy.schema.Table) metadata may refer to a dynamically configured set of
schema names on a per-connection or per-statement basis.

What’s “schema” ?

SQLAlchemy’s support for database “schema” was designed with first party
support for PostgreSQL-style schemas.  In this style, there is first a
“database” that typically has a single “owner”.  Within this database there
can be any number of “schemas” which then contain the actual table objects.

A table within a specific schema is referenced explicitly using the syntax
“<schemaname>.<tablename>”.  Contrast this to an architecture such as that
of MySQL, where there are only “databases”, however SQL statements can
refer to multiple databases at once, using the same syntax except it is
“<database>.<tablename>”.  On Oracle Database, this syntax refers to yet
another concept, the “owner” of a table.  Regardless of which kind of
database is in use, SQLAlchemy uses the phrase “schema” to refer to the
qualifying identifier within the general syntax of
“<qualifier>.<tablename>”.

See also

[Explicit Schema Name with Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-schema-name) - schema name specification when using the ORM
[declarative table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) configuration

The most basic example is that of the [Table.schema](#sqlalchemy.schema.Table.params.schema) argument
using a Core [Table](#sqlalchemy.schema.Table) object as follows:

```
metadata_obj = MetaData()

financial_info = Table(
    "financial_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),
    schema="remote_banks",
)
```

SQL that is rendered using this [Table](#sqlalchemy.schema.Table), such as the SELECT
statement below, will explicitly qualify the table name `financial_info` with
the `remote_banks` schema name:

```
>>> print(select(financial_info))
SELECT remote_banks.financial_info.id, remote_banks.financial_info.value
FROM remote_banks.financial_info
```

When a [Table](#sqlalchemy.schema.Table) object is declared with an explicit schema
name, it is stored in the internal [MetaData](#sqlalchemy.schema.MetaData) namespace
using the combination of the schema and table name.  We can view this
in the [MetaData.tables](#sqlalchemy.schema.MetaData.tables) collection by searching for the
key `'remote_banks.financial_info'`:

```
>>> metadata_obj.tables["remote_banks.financial_info"]
Table('financial_info', MetaData(),
Column('id', Integer(), table=<financial_info>, primary_key=True, nullable=False),
Column('value', String(length=100), table=<financial_info>, nullable=False),
schema='remote_banks')
```

This dotted name is also what must be used when referring to the table
for use with the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) or [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects, even if the referring table is also in that same schema:

```
customer = Table(
    "customer",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("financial_info_id", ForeignKey("remote_banks.financial_info.id")),
    schema="remote_banks",
)
```

The [Table.schema](#sqlalchemy.schema.Table.params.schema) argument may also be used with certain
dialects to indicate
a multiple-token (e.g. dotted) path to a particular table.  This is particularly
important on a database such as Microsoft SQL Server where there are often
dotted “database/owner” tokens.  The tokens may be placed directly in the name
at once, such as:

```
schema = "dbo.scott"
```

See also

[Multipart Schema Names](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#multipart-schema-names) - describes use of dotted schema names
with the SQL Server dialect.

[Reflecting Tables from Other Schemas](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-schemas)

### Specifying a Default Schema Name with MetaData

The [MetaData](#sqlalchemy.schema.MetaData) object may also set up an explicit default
option for all [Table.schema](#sqlalchemy.schema.Table.params.schema) parameters by passing the
[MetaData.schema](#sqlalchemy.schema.MetaData.params.schema) argument to the top level [MetaData](#sqlalchemy.schema.MetaData)
construct:

```
metadata_obj = MetaData(schema="remote_banks")

financial_info = Table(
    "financial_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),
)
```

Above, for any [Table](#sqlalchemy.schema.Table) object (or [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) object
directly associated with the [MetaData](#sqlalchemy.schema.MetaData)) which leaves the
[Table.schema](#sqlalchemy.schema.Table.params.schema) parameter at its default of `None` will instead
act as though the parameter were set to the value `"remote_banks"`.  This
includes that the [Table](#sqlalchemy.schema.Table) is cataloged in the [MetaData](#sqlalchemy.schema.MetaData)
using the schema-qualified name, that is:

```
metadata_obj.tables["remote_banks.financial_info"]
```

When using the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) or [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
objects to refer to this table, either the schema-qualified name or the
non-schema-qualified name may be used to refer to the `remote_banks.financial_info`
table:

```
# either will work:

refers_to_financial_info = Table(
    "refers_to_financial_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("fiid", ForeignKey("financial_info.id")),
)

# or

refers_to_financial_info = Table(
    "refers_to_financial_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("fiid", ForeignKey("remote_banks.financial_info.id")),
)
```

When using a [MetaData](#sqlalchemy.schema.MetaData) object that sets
[MetaData.schema](#sqlalchemy.schema.MetaData.params.schema), a [Table](#sqlalchemy.schema.Table) that wishes
to specify that it should not be schema qualified may use the special symbol
`BLANK_SCHEMA`:

```
from sqlalchemy import BLANK_SCHEMA

metadata_obj = MetaData(schema="remote_banks")

financial_info = Table(
    "financial_info",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),
    schema=BLANK_SCHEMA,  # will not use "remote_banks"
)
```

See also

[MetaData.schema](#sqlalchemy.schema.MetaData.params.schema)

### Applying Dynamic Schema Naming Conventions

The names used by the [Table.schema](#sqlalchemy.schema.Table.params.schema) parameter may also be
applied against a lookup that is dynamic on a per-connection or per-execution
basis, so that for example in multi-tenant situations, each transaction
or statement may be targeted at a specific set of schema names that change.
The section [Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating) describes how this feature is used.

See also

[Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating)

### Setting a Default Schema for New Connections

The above approaches all refer to methods of including an explicit schema-name
within SQL statements.  Database connections in fact feature the concept
of a “default” schema, which is the name of the “schema” (or database, owner,
etc.) that takes place if a table name is not explicitly schema-qualified.
These names are usually configured at the login level, such as when connecting
to a PostgreSQL database, the default “schema” is called “public”.

There are often cases where the default “schema” cannot be set via the login
itself and instead would usefully be configured each time a connection is made,
using a statement such as “SET SEARCH_PATH” on PostgreSQL or “ALTER SESSION” on
Oracle Database.  These approaches may be achieved by using the
`PoolEvents.connect()` event, which allows access to the DBAPI
connection when it is first created.  For example, to set the Oracle Database
CURRENT_SCHEMA variable to an alternate name:

```
from sqlalchemy import event
from sqlalchemy import create_engine

engine = create_engine(
    "oracle+oracledb://scott:tiger@localhost:1521?service_name=freepdb1"
)

@event.listens_for(engine, "connect", insert=True)
def set_current_schema(dbapi_connection, connection_record):
    cursor_obj = dbapi_connection.cursor()
    cursor_obj.execute("ALTER SESSION SET CURRENT_SCHEMA=%s" % schema_name)
    cursor_obj.close()
```

Above, the `set_current_schema()` event handler will take place immediately
when the above [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) first connects; as the event is
“inserted” into the beginning of the handler list, it will also take place
before the dialect’s own event handlers are run, in particular including the
one that will determine the “default schema” for the connection.

For other databases, consult the database and/or dialect documentation
for specific information regarding how default schemas are configured.

Changed in version 1.4.0b2: The above recipe now works without the need to
establish additional event handlers.

See also

[Setting Alternate Search Paths on Connect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-alternate-search-path) - in the [PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) dialect documentation.

### Schemas and Reflection

The schema feature of SQLAlchemy interacts with the table reflection
feature introduced at [Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html).  See the section
[Reflecting Tables from Other Schemas](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-schemas) for additional details on how this works.

## Backend-Specific Options

[Table](#sqlalchemy.schema.Table) supports database-specific options. For
example, MySQL has different table backend types, including “MyISAM” and
“InnoDB”. This can be expressed with [Table](#sqlalchemy.schema.Table) using
`mysql_engine`:

```
addresses = Table(
    "engine_email_addresses",
    metadata_obj,
    Column("address_id", Integer, primary_key=True),
    Column("remote_user_id", Integer, ForeignKey(users.c.user_id)),
    Column("email_address", String(20)),
    mysql_engine="InnoDB",
)
```

Other backends may support table-level options as well - these would be
described in the individual documentation sections for each dialect.

## Column, Table, MetaData API

| Object Name | Description |
| --- | --- |
| Column | Represents a column in a database table. |
| insert_sentinel([name, type_], *, [default, omit_from_statements]) | Provides a surrogateColumnthat will act as a
dedicated insertsentinelcolumn, allowing efficient bulk
inserts with deterministic RETURNING sorting for tables that
don’t otherwise have qualifying primary key configurations. |
| MetaData | A collection ofTableobjects and their associated schema
constructs. |
| SchemaConst |  |
| SchemaItem | Base class for items that define a database schema. |
| Table | Represent a table in a database. |

   attribute [sqlalchemy.schema.sqlalchemy.schema.](#sqlalchemy.schema.sqlalchemy.schema)sqlalchemy.schema.BLANK_SCHEMA

Refers to [SchemaConst.BLANK_SCHEMA](#sqlalchemy.schema.SchemaConst.BLANK_SCHEMA).

    attribute [sqlalchemy.schema.sqlalchemy.schema.](#sqlalchemy.schema.sqlalchemy.schema)sqlalchemy.schema.RETAIN_SCHEMA

Refers to [SchemaConst.RETAIN_SCHEMA](#sqlalchemy.schema.SchemaConst.RETAIN_SCHEMA)

    class sqlalchemy.schema.Column

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.schema.SchemaItem](#sqlalchemy.schema.SchemaItem), [sqlalchemy.sql.expression.ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause)

Represents a column in a database table.

| Member Name | Description |
| --- | --- |
| __eq__() | Implement the==operator. |
| __init__() | Construct a newColumnobject. |
| __le__() | Implement the<=operator. |
| __lt__() | Implement the<operator. |
| __ne__() | Implement the!=operator. |
| all_() | Produce anall_()clause against the
parent object. |
| any_() | Produce anany_()clause against the
parent object. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
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
| cast() | Produce a type cast, i.e.CAST(<expression>AS<type>). |
| collate() | Produce acollate()clause against
the parent object, given the collation string. |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| concat() | Implement the ‘concat’ operator. |
| contains() | Implement the ‘contains’ operator. |
| copy() |  |
| desc() | Produce adesc()clause against the
parent object. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| distinct() | Produce adistinct()clause against the
parent object. |
| endswith() | Implement the ‘endswith’ operator. |
| foreign_keys | A collection of allForeignKeymarker objects
associated with thisColumn. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| icontains() | Implement theicontainsoperator, e.g. case insensitive
version ofColumnOperators.contains(). |
| iendswith() | Implement theiendswithoperator, e.g. case insensitive
version ofColumnOperators.endswith(). |
| ilike() | Implement theilikeoperator, e.g. case insensitive LIKE. |
| in_() | Implement theinoperator. |
| index | The value of theColumn.indexparameter. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| is_() | Implement theISoperator. |
| is_distinct_from() | Implement theISDISTINCTFROMoperator. |
| is_not() | Implement theISNOToperator. |
| is_not_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| isnot() | Implement theISNOToperator. |
| isnot_distinct_from() | Implement theISNOTDISTINCTFROMoperator. |
| istartswith() | Implement theistartswithoperator, e.g. case insensitive
version ofColumnOperators.startswith(). |
| key | The ‘key’ that in some circumstances refers to this object in a
Python namespace. |
| label() | Produce a column label, i.e.<columnname>AS<name>. |
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
| params() | Return a copy withbindparam()elements
replaced. |
| proxy_set | set of all columns we are proxying |
| references() | Return True if this Column references the given column via foreign
key. |
| regexp_match() | Implements a database-specific ‘regexp match’ operator. |
| regexp_replace() | Implements a database-specific ‘regexp replace’ operator. |
| reverse_operate() | Reverse operate on an argument. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| shares_lineage() | Return True if the givenColumnElementhas a common ancestor to thisColumnElement. |
| startswith() | Implement thestartswithoperator. |
| timetuple | Hack, allows datetime objects to be compared on the LHS. |
| unique | The value of theColumn.uniqueparameter. |
| unique_params() | Return a copy withbindparam()elements
replaced. |

   method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)__eq__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__eq__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `==` operator.

In a column context, produces the clause `a = b`.
If the target is `None`, produces `a IS NULL`.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)__init__(*_Column__name_pos:str|_TypeEngineArgument[_T]|SchemaEventTarget|None=None*, *_Column__type_pos:_TypeEngineArgument[_T]|SchemaEventTarget|None=None*, **args:SchemaEventTarget*, *name:str|None=None*, *type_:_TypeEngineArgument[_T]|None=None*, *autoincrement:_AutoIncrementType='auto'*, *default:Any|None=_NoArg.NO_ARG*, *insert_default:Any|None=_NoArg.NO_ARG*, *doc:str|None=None*, *key:str|None=None*, *index:bool|None=None*, *unique:bool|None=None*, *info:_InfoType|None=None*, *nullable:bool|Literal[SchemaConst.NULL_UNSPECIFIED]|None=SchemaConst.NULL_UNSPECIFIED*, *onupdate:Any|None=None*, *primary_key:bool=False*, *server_default:_ServerDefaultArgument|None=None*, *server_onupdate:_ServerOnUpdateArgument|None=None*, *quote:bool|None=None*, *system:bool=False*, *comment:str|None=None*, *insert_sentinel:bool=False*, *_omit_from_statements:bool=False*, *_proxies:Any|None=None*, ***dialect_kwargs:Any*)

Construct a new `Column` object.

  Parameters:

- **name** –
  The name of this column as represented in the database.
  This argument may be the first positional argument, or specified
  via keyword.
  Names which contain no upper case characters
  will be treated as case insensitive names, and will not be quoted
  unless they are a reserved word.  Names with any number of upper
  case characters will be quoted and sent exactly.  Note that this
  behavior applies even for databases which standardize upper
  case names as case insensitive such as Oracle Database.
  The name field may be omitted at construction time and applied
  later, at any time before the Column is associated with a
  [Table](#sqlalchemy.schema.Table).  This is to support convenient
  usage within the [declarative](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/api.html#module-sqlalchemy.ext.declarative) extension.
- **type_** –
  The column’s type, indicated using an instance which
  subclasses [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine).  If no arguments
  are required for the type, the class of the type can be sent
  as well, e.g.:
  ```
  # use a type with arguments
  Column("data", String(50))
  # use no arguments
  Column("level", Integer)
  ```
  The `type` argument may be the second positional argument
  or specified by keyword.
  If the `type` is `None` or is omitted, it will first default to
  the special type [NullType](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.NullType).  If and when this
  [Column](#sqlalchemy.schema.Column) is made to refer to another column using
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) and/or
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint), the type
  of the remote-referenced column will be copied to this column as
  well, at the moment that the foreign key is resolved against that
  remote [Column](#sqlalchemy.schema.Column) object.
- ***args** – Additional positional arguments include various
  [SchemaItem](#sqlalchemy.schema.SchemaItem) derived constructs which will be applied
  as options to the column.  These include instances of
  [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint), [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey),
  [ColumnDefault](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), [Computed](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Computed) [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity).  In some cases an
  equivalent keyword argument is available such as `server_default`,
  `default` and `unique`.
- **autoincrement** –
  Set up “auto increment” semantics for an
  **integer primary key column with no foreign key dependencies**
  (see later in this docstring for a more specific definition).
  This may influence the [DDL](https://docs.sqlalchemy.org/en/20/glossary.html#term-DDL) that will be emitted for
  this column during a table create, as well as how the column
  will be considered when INSERT statements are compiled and
  executed.
  The default value is the string `"auto"`,
  which indicates that a single-column (i.e. non-composite) primary key
  that is of an INTEGER type with no other client-side or server-side
  default constructs indicated should receive auto increment semantics
  automatically. Other values include `True` (force this column to
  have auto-increment semantics for a [composite primary key](https://docs.sqlalchemy.org/en/20/glossary.html#term-composite-primary-key) as
  well), `False` (this column should never have auto-increment
  semantics), and the string `"ignore_fk"` (special-case for foreign
  key columns, see below).
  The term “auto increment semantics” refers both to the kind of DDL
  that will be emitted for the column within a CREATE TABLE statement,
  when methods such as [MetaData.create_all()](#sqlalchemy.schema.MetaData.create_all) and
  [Table.create()](#sqlalchemy.schema.Table.create) are invoked, as well as how the column will be
  considered when an INSERT statement is compiled and emitted to the
  database:
  - **DDL rendering** (i.e. [MetaData.create_all()](#sqlalchemy.schema.MetaData.create_all),
    [Table.create()](#sqlalchemy.schema.Table.create)): When used on a [Column](#sqlalchemy.schema.Column) that has
    no other
    default-generating construct associated with it (such as a
    [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) or [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) construct), the parameter
    will imply that database-specific keywords such as PostgreSQL
    `SERIAL`, MySQL `AUTO_INCREMENT`, or `IDENTITY` on SQL Server
    should also be rendered.  Not every database backend has an
    “implied” default generator available; for example the Oracle Database
    backends always needs an explicit construct such as
    [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) to be included with a [Column](#sqlalchemy.schema.Column) in order
    for the DDL rendered to include auto-generating constructs to also
    be produced in the database.
  - **INSERT semantics** (i.e. when a [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct is
    compiled into a SQL string and is then executed on a database using
    [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute) or equivalent): A single-row
    INSERT statement will be known to produce a new integer primary key
    value automatically for this column, which will be accessible
    after the statement is invoked via the
    [CursorResult.inserted_primary_key](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.inserted_primary_key) attribute upon the
    [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object.   This also applies towards use of the
    ORM when ORM-mapped objects are persisted to the database,
    indicating that a new integer primary key will be available to
    become part of the [identity key](https://docs.sqlalchemy.org/en/20/glossary.html#term-identity-key) for that object.  This
    behavior takes place regardless of what DDL constructs are
    associated with the [Column](#sqlalchemy.schema.Column) and is independent
    of the “DDL Rendering” behavior discussed in the previous note
    above.
  The parameter may be set to `True` to indicate that a column which
  is part of a composite (i.e. multi-column) primary key should
  have autoincrement semantics, though note that only one column
  within a primary key may have this setting.    It can also
  be set to `True` to indicate autoincrement semantics on a
  column that has a client-side or server-side default configured,
  however note that not all dialects can accommodate all styles
  of default as an “autoincrement”.  It can also be
  set to `False` on a single-column primary key that has a
  datatype of INTEGER in order to disable auto increment semantics
  for that column.
  The setting *only* has an effect for columns which are:
  - Integer derived (i.e. INT, SMALLINT, BIGINT).
  - Part of the primary key
  - Not referring to another column via [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey),
    unless
    the value is specified as `'ignore_fk'`:
    ```
    # turn on autoincrement for this column despite
    # the ForeignKey()
    Column(
        "id",
        ForeignKey("other.id"),
        primary_key=True,
        autoincrement="ignore_fk",
    )
    ```
  It is typically not desirable to have “autoincrement” enabled on a
  column that refers to another via foreign key, as such a column is
  required to refer to a value that originates from elsewhere.
  The setting has these effects on columns that meet the
  above criteria:
  - DDL issued for the column, if the column does not already include
    a default generating construct supported by the backend such as
    [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity), will include database-specific
    keywords intended to signify this column as an
    “autoincrement” column for specific backends.   Behavior for
    primary SQLAlchemy dialects includes:
    - AUTO INCREMENT on MySQL and MariaDB
    - SERIAL on PostgreSQL
    - IDENTITY on MS-SQL - this occurs even without the
      [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) construct as the
      [Column.autoincrement](#sqlalchemy.schema.Column.params.autoincrement) parameter pre-dates this
      construct.
    - SQLite - SQLite integer primary key columns are implicitly
      “auto incrementing” and no additional keywords are rendered;
      to render the special SQLite keyword `AUTOINCREMENT`
      is not included as this is unnecessary and not recommended
      by the database vendor.  See the section
      [SQLite Auto Incrementing Behavior](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-autoincrement) for more background.
    - Oracle Database - The Oracle Database dialects have no default “autoincrement”
      feature available at this time, instead the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity)
      construct is recommended to achieve this (the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)
      construct may also be used).
    - Third-party dialects - consult those dialects’ documentation
      for details on their specific behaviors.
  - When a single-row [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) construct is compiled and
    executed, which does not set the [Insert.inline()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.inline)
    modifier, newly generated primary key values for this column
    will be automatically retrieved upon statement execution
    using a method specific to the database driver in use:
    - MySQL, SQLite - calling upon `cursor.lastrowid()`
      (see
      [https://www.python.org/dev/peps/pep-0249/#lastrowid](https://www.python.org/dev/peps/pep-0249/#lastrowid))
    - PostgreSQL, SQL Server, Oracle Database - use RETURNING or an equivalent
      construct when rendering an INSERT statement, and then retrieving
      the newly generated primary key values after execution
    - PostgreSQL, Oracle Database for [Table](#sqlalchemy.schema.Table) objects that
      set [Table.implicit_returning](#sqlalchemy.schema.Table.params.implicit_returning) to False -
      for a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) only, the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) is invoked
      explicitly before the INSERT statement takes place so that the
      newly generated primary key value is available to the client
    - SQL Server for [Table](#sqlalchemy.schema.Table) objects that
      set [Table.implicit_returning](#sqlalchemy.schema.Table.params.implicit_returning) to False -
      the `SELECT scope_identity()` construct is used after the
      INSERT statement is invoked to retrieve the newly generated
      primary key value.
    - Third-party dialects - consult those dialects’ documentation
      for details on their specific behaviors.
  - For multiple-row [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) constructs invoked with
    a list of parameters (i.e. “executemany” semantics), primary-key
    retrieving behaviors are generally disabled, however there may
    be special APIs that may be used to retrieve lists of new
    primary key values for an “executemany”, such as the psycopg2
    “fast insertmany” feature.  Such features are very new and
    may not yet be well covered in documentation.
- **default** –
  A scalar, Python callable, or
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) expression representing the
  *default value* for this column, which will be invoked upon insert
  if this column is otherwise not specified in the VALUES clause of
  the insert. This is a shortcut to using [ColumnDefault](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault) as
  a positional argument; see that class for full detail on the
  structure of the argument.
  Contrast this argument to
  [Column.server_default](#sqlalchemy.schema.Column.params.server_default)
  which creates a default generator on the database side.
  See also
  [Column INSERT/UPDATE Defaults](https://docs.sqlalchemy.org/en/20/core/defaults.html)
- **insert_default** –
  An alias of [Column.default](#sqlalchemy.schema.Column.params.default)
  for compatibility with [mapped_column()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column).
- **doc** – optional String that can be used by the ORM or similar
  to document attributes on the Python side.   This attribute does
  **not** render SQL comments; use the
  [Column.comment](#sqlalchemy.schema.Column.params.comment)
  parameter for this purpose.
- **key** – An optional string identifier which will identify this
  `Column` object on the [Table](#sqlalchemy.schema.Table).
  When a key is provided,
  this is the only identifier referencing the `Column` within the
  application, including ORM attribute mapping; the `name` field
  is used only when rendering SQL.
- **index** –
  When `True`, indicates that a [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
  construct will be automatically generated for this
  [Column](#sqlalchemy.schema.Column), which will result in a “CREATE INDEX”
  statement being emitted for the [Table](#sqlalchemy.schema.Table) when the DDL
  create operation is invoked.
  Using this flag is equivalent to making use of the
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct explicitly at the level of the
  [Table](#sqlalchemy.schema.Table) construct itself:
  ```
  Table(
      "some_table",
      metadata,
      Column("x", Integer),
      Index("ix_some_table_x", "x"),
  )
  ```
  To add the [Index.unique](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.params.unique) flag to the
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index), set both the
  [Column.unique](#sqlalchemy.schema.Column.params.unique) and
  [Column.index](#sqlalchemy.schema.Column.params.index) flags to True simultaneously,
  which will have the effect of rendering the “CREATE UNIQUE INDEX”
  DDL instruction instead of “CREATE INDEX”.
  The name of the index is generated using the
  [default naming convention](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-default-naming-convention)
  which for the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct is of the form
  `ix_<tablename>_<columnname>`.
  As this flag is intended only as a convenience for the common case
  of adding a single-column, default configured index to a table
  definition, explicit use of the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct
  should be preferred for most use cases, including composite indexes
  that encompass more than one column, indexes with SQL expressions
  or ordering, backend-specific index configuration options, and
  indexes that use a specific name.
  Note
  the [Column.index](#sqlalchemy.schema.Column.index) attribute on
  [Column](#sqlalchemy.schema.Column) **does not indicate** if this column is indexed or not, only
  if this flag was explicitly set here.  To view indexes on
  a column, view the [Table.indexes](#sqlalchemy.schema.Table.indexes) collection
  or use [Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes).
  See also
  [Indexes](https://docs.sqlalchemy.org/en/20/core/constraints.html#schema-indexes)
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
  [Column.unique](#sqlalchemy.schema.Column.params.unique)
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **nullable** –
  When set to `False`, will cause the “NOT NULL”
  phrase to be added when generating DDL for the column.   When
  `True`, will normally generate nothing (in SQL this defaults to
  “NULL”), except in some very specific backend-specific edge cases
  where “NULL” may render explicitly.
  Defaults to `True` unless [Column.primary_key](#sqlalchemy.schema.Column.params.primary_key)
  is also `True` or the column specifies a `Identity`,
  in which case it defaults to `False`.
  This parameter is only used when issuing CREATE TABLE statements.
  Note
  When the column specifies a `Identity` this
  parameter is in general ignored by the DDL compiler. The
  PostgreSQL database allows nullable identity column by
  setting this parameter to `True` explicitly.
- **onupdate** –
  A scalar, Python callable, or
  [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) representing a
  default value to be applied to the column within UPDATE
  statements, which will be invoked upon update if this column is not
  present in the SET clause of the update. This is a shortcut to
  using [ColumnDefault](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault) as a positional argument with
  `for_update=True`.
  See also
  [Column INSERT/UPDATE Defaults](https://docs.sqlalchemy.org/en/20/core/defaults.html#metadata-defaults) - complete discussion of onupdate
- **primary_key** – If `True`, marks this column as a primary key
  column. Multiple columns can have this flag set to specify
  composite primary keys. As an alternative, the primary key of a
  [Table](#sqlalchemy.schema.Table) can be specified via an explicit
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) object.
- **server_default** –
  A [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) instance, str, Unicode
  or [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct representing
  the DDL DEFAULT value for the column.
  String types will be emitted as-is, surrounded by single quotes:
  ```
  Column("x", Text, server_default="val")
  ```
  will render:
  ```
  x TEXT DEFAULT 'val'
  ```
  A [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) expression will be
  rendered as-is, without quotes:
  ```
  Column("y", DateTime, server_default=text("NOW()"))
  ```
  will render:
  ```
  y DATETIME DEFAULT NOW()
  ```
  Strings and text() will be converted into a
  [DefaultClause](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.DefaultClause) object upon initialization.
  This parameter can also accept complex combinations of contextually
  valid SQLAlchemy expressions or constructs:
  ```
  from sqlalchemy import create_engine
  from sqlalchemy import Table, Column, MetaData, ARRAY, Text
  from sqlalchemy.dialects.postgresql import array
  engine = create_engine(
      "postgresql+psycopg2://scott:tiger@localhost/mydatabase"
  )
  metadata_obj = MetaData()
  tbl = Table(
      "foo",
      metadata_obj,
      Column(
          "bar", ARRAY(Text), server_default=array(["biz", "bang", "bash"])
      ),
  )
  metadata_obj.create_all(engine)
  ```
  The above results in a table created with the following SQL:
  ```
  CREATE TABLE foo (
      bar TEXT[] DEFAULT ARRAY['biz', 'bang', 'bash']
  )
  ```
  Use [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) to indicate that an already-existing
  column will generate a default value on the database side which
  will be available to SQLAlchemy for post-fetch after inserts. This
  construct does not specify any DDL and the implementation is left
  to the database, such as via a trigger.
  See also
  [Server-invoked DDL-Explicit Default Expressions](https://docs.sqlalchemy.org/en/20/core/defaults.html#server-defaults) - complete discussion of server side
  defaults
- **server_onupdate** –
  A [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) instance
  representing a database-side default generation function,
  such as a trigger. This
  indicates to SQLAlchemy that a newly generated value will be
  available after updates. This construct does not actually
  implement any kind of generation function within the database,
  which instead must be specified separately.
  Warning
  This directive **does not** currently produce MySQL’s
  “ON UPDATE CURRENT_TIMESTAMP()” clause.  See
  [Rendering ON UPDATE CURRENT TIMESTAMP for MySQL / MariaDB’s explicit_defaults_for_timestamp](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-timestamp-onupdate) for background on how to
  produce this clause.
  See also
  [Marking Implicitly Generated Values, timestamps, and Triggered Columns](https://docs.sqlalchemy.org/en/20/core/defaults.html#triggered-columns)
- **quote** – Force quoting of this column’s name on or off,
  corresponding to `True` or `False`. When left at its default
  of `None`, the column identifier will be quoted according to
  whether the name is case sensitive (identifiers with at least one
  upper case character are treated as case sensitive), or if it’s a
  reserved word. This flag is only needed to force quoting of a
  reserved word which is not known by the SQLAlchemy dialect.
- **unique** –
  When `True`, and the [Column.index](#sqlalchemy.schema.Column.params.index)
  parameter is left at its default value of `False`,
  indicates that a [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint)
  construct will be automatically generated for this
  [Column](#sqlalchemy.schema.Column),
  which will result in a “UNIQUE CONSTRAINT” clause referring
  to this column being included
  in the `CREATE TABLE` statement emitted, when the DDL create
  operation for the [Table](#sqlalchemy.schema.Table) object is invoked.
  When this flag is `True` while the
  [Column.index](#sqlalchemy.schema.Column.params.index) parameter is simultaneously
  set to `True`, the effect instead is that a
  [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct which includes the
  [Index.unique](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index.params.unique) parameter set to `True`
  is generated.  See the documentation for
  [Column.index](#sqlalchemy.schema.Column.params.index) for additional detail.
  Using this flag is equivalent to making use of the
  [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) construct explicitly at the
  level of the [Table](#sqlalchemy.schema.Table) construct itself:
  ```
  Table("some_table", metadata, Column("x", Integer), UniqueConstraint("x"))
  ```
  The [UniqueConstraint.name](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint.params.name) parameter
  of the unique constraint object is left at its default value
  of `None`; in the absence of a [naming convention](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
  for the enclosing [MetaData](#sqlalchemy.schema.MetaData), the UNIQUE CONSTRAINT
  construct will be emitted as unnamed, which typically invokes
  a database-specific naming convention to take place.
  As this flag is intended only as a convenience for the common case
  of adding a single-column, default configured unique constraint to a table
  definition, explicit use of the [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint) construct
  should be preferred for most use cases, including composite constraints
  that encompass more than one column, backend-specific index configuration options, and
  constraints that use a specific name.
  Note
  the [Column.unique](#sqlalchemy.schema.Column.unique) attribute on
  [Column](#sqlalchemy.schema.Column) **does not indicate** if this column has a unique constraint or
  not, only if this flag was explicitly set here.  To view
  indexes and unique constraints that may involve this column,
  view the
  [Table.indexes](#sqlalchemy.schema.Table.indexes) and/or
  [Table.constraints](#sqlalchemy.schema.Table.constraints) collections or use
  [Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes) and/or
  [Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints)
  See also
  [UNIQUE Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#schema-unique-constraint)
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)
  [Column.index](#sqlalchemy.schema.Column.params.index)
- **system** –
  When `True`, indicates this is a “system” column,
  that is a column which is automatically made available by the
  database, and should not be included in the columns list for a
  `CREATE TABLE` statement.
  For more elaborate scenarios where columns should be
  conditionally rendered differently on different backends,
  consider custom compilation rules for [CreateColumn](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateColumn).
- **comment** –
  Optional string that will render an SQL comment on
  table creation.
  Added in version 1.2: Added the
  [Column.comment](#sqlalchemy.schema.Column.params.comment)
  parameter to [Column](#sqlalchemy.schema.Column).
- **insert_sentinel** –
  Marks this [Column](#sqlalchemy.schema.Column) as an
  [insert sentinel](https://docs.sqlalchemy.org/en/20/glossary.html#term-insert-sentinel) used for optimizing the performance of the
  [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues) feature for tables that don’t
  otherwise have qualifying primary key configurations.
  Added in version 2.0.10.
  See also
  [insert_sentinel()](#sqlalchemy.schema.insert_sentinel) - all in one helper for declaring
  sentinel columns
  [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)
  [Configuring Sentinel Columns](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-sentinel-columns)

      method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)__le__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__le__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<=` operator.

In a column context, produces the clause `a <= b`.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)__lt__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__lt__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `<` operator.

In a column context, produces the clause `a < b`.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)__ne__(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* `sqlalchemy.sql.expression.ColumnOperators.__ne__` *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `!=` operator.

In a column context, produces the clause `a != b`.
If the target is `None`, produces `a IS NOT NULL`.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)all_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property anon_key_label: str

Deprecated since version 1.4: The [ColumnElement.anon_key_label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.anon_key_label) attribute is now private, and the public accessor is deprecated.

     property anon_label: str

Deprecated since version 1.4: The [ColumnElement.anon_label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.anon_label) attribute is now private, and the public accessor is deprecated.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)any_() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     classmethod [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

*inherited from the* `DialectKWArgs.argument_for()` *method of* `DialectKWArgs`

Add a new kind of dialect-specific keyword argument for this class.

E.g.:

```
Index.argument_for("mydialect", "length", None)

some_index = Index("a", "b", mydialect_length=5)
```

The [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method is a per-argument
way adding extra arguments to the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) dictionary. This
dictionary provides a list of argument names accepted by various
schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a
data member of the dialect class.  The use case for ad-hoc addition of
argument names is typically for end-user code that is also using
a custom compilation scheme which consumes the additional arguments.

  Parameters:

- **dialect_name** – name of a dialect.  The dialect must be
  locatable, else a [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError) is raised.   The
  dialect must also include an existing
  [DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) collection, indicating
  that it participates in the keyword-argument validation and default
  system, else [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.  If the dialect does
  not include this collection, then any keyword argument can be
  specified on behalf of this dialect already.  All dialects packaged
  within SQLAlchemy include this collection, however for third party
  dialects, support may vary.
- **argument_name** – name of the parameter.
- **default** – default value of the parameter.

      method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)asc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.asc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [asc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.asc) clause against the
parent object.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)between(*cleft:Any*, *cright:Any*, *symmetric:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.between) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [between()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.between) clause against
the parent object, given the lower and upper range.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_and(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_and()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_and) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise AND operation, typically via the `&`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_lshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_lshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_lshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise LSHIFT operation, typically via the `<<`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_not() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_not) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise NOT operation, typically via the `~`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_or(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_or()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_or) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise OR operation, typically via the `|`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_rshift(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_rshift()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_rshift) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise RSHIFT operation, typically via the `>>`
operator.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bitwise_xor(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.bitwise_xor()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.bitwise_xor) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a bitwise XOR operation, typically via the `^`
operator, or `#` for PostgreSQL.

Added in version 2.0.2.

See also

[Bitwise Operators](https://docs.sqlalchemy.org/en/20/core/operators.html#operators-bitwise)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)bool_op(*opstring:str*, *precedence:int=0*, *python_impl:Callable[[...],Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)cast(*type_:_TypeEngineArgument[_OPT]*) → [Cast](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Cast)[_OPT]

*inherited from the* [ColumnElement.cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.cast) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Produce a type cast, i.e. `CAST(<expression> AS <type>)`.

This is a shortcut to the [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) function.

See also

[Data Casts and Type Coercion](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-casts)

[cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast)

[type_coerce()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.type_coerce)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)collate(*collation:str*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.collate) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate) clause against
the parent object, given the collation string.

See also

[collate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.collate)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)compare(*other:ClauseElement*, ***kw:Any*) → bool

*inherited from the* [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Compare this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

*inherited from the* `CompilerElement.compile()` *method of* `CompilerElement`

Compile this SQL expression.

The return value is a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.
Calling `str()` or `unicode()` on the returned value will yield a
string representation of the result. The
[Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object also can return a
dictionary of bind parameter names and values
using the `params` accessor.

  Parameters:

- **bind** – An [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which
  can provide a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in order to generate a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  If the `bind` and
  `dialect` parameters are both omitted, a default SQL compiler
  is used.
- **column_keys** – Used for INSERT and UPDATE statements, a list of
  column names which should be present in the VALUES clause of the
  compiled statement. If `None`, all columns from the target table
  object are rendered.
- **dialect** – A [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) instance which can generate
  a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  This argument takes precedence over
  the `bind` argument.
- **compile_kwargs** –
  optional dictionary of additional parameters
  that will be passed through to the compiler within all “visit”
  methods.  This allows any custom flag to be passed through to
  a custom compilation construct, for example.  It is also used
  for the case of passing the `literal_binds` flag through:
  ```
  from sqlalchemy.sql import table, column, select
  t = table("t", column("x"))
  s = select(t).where(t.c.x == 5)
  print(s.compile(compile_kwargs={"literal_binds": True}))
  ```

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)concat(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.concat()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.concat) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the ‘concat’ operator.

In a column context, produces the clause `a || b`,
or uses the `concat()` operator on MySQL.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)contains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)copy(***kw:Any*) → [Column](#sqlalchemy.schema.Column)[Any]

Deprecated since version 1.4: The [Column.copy()](#sqlalchemy.schema.Column.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)desc() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.desc) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.desc) clause against the
parent object.

    property dialect_kwargs: _DialectArgView

A collection of keyword arguments specified as dialect-specific
options to this construct.

The arguments are present here in their original `<dialect>_<kwarg>`
format.  Only arguments that were actually passed are included;
unlike the [DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) collection, which
contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the
form `<dialect>_<kwarg>` where the value will be assembled
into the list of options.

See also

[DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) - nested dictionary form

     attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)dialect_options

*inherited from the* `DialectKWArgs.dialect_options` *attribute of* `DialectKWArgs`

A collection of keyword arguments specified as dialect-specific
options to this construct.

This is a two-level nested registry, keyed to `<dialect_name>`
and `<argument_name>`.  For example, the `postgresql_where`
argument would be locatable as:

```
arg = my_object.dialect_options["postgresql"]["where"]
```

Added in version 0.9.2.

See also

[DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs) - flat dictionary form

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)distinct() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.distinct) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [distinct()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.distinct) clause against the
parent object.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)endswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     property expression: [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

Return a column expression.

Part of the inspection interface; returns self.

    attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)foreign_keys: Set[[ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)] = frozenset({})

*inherited from the* [ColumnElement.foreign_keys](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.foreign_keys) *attribute of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

A collection of all [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) marker objects
associated with this [Column](#sqlalchemy.schema.Column).

Each object is a member of a [Table](#sqlalchemy.schema.Table)-wide
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).

See also

[Table.foreign_keys](#sqlalchemy.schema.Table.foreign_keys)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)get_children(***, *column_tables=False*, ***kw*)

*inherited from the* [ColumnClause.get_children()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause.get_children) *method of* [ColumnClause](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnClause)

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)icontains(*other:Any*, ***kw:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)iendswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)in_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

      attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)index: bool | None

The value of the [Column.index](#sqlalchemy.schema.Column.params.index) parameter.

Does not indicate if this [Column](#sqlalchemy.schema.Column) is actually indexed
or not; use [Table.indexes](#sqlalchemy.schema.Table.indexes).

See also

[Table.indexes](#sqlalchemy.schema.Table.indexes)

     attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)info

*inherited from the* [SchemaItem.info](#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](#sqlalchemy.schema.Table) and [Column](#sqlalchemy.schema.Column).

    attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)inherit_cache = True

Indicate if this [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)is_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS` operator.

Normally, `IS` is generated automatically when comparing to a
value of `None`, which resolves to `NULL`.  However, explicit
usage of `IS` may be desirable if comparing to boolean values
on certain platforms.

See also

[ColumnOperators.is_not()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)is_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS DISTINCT FROM` operator.

Renders “a IS DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS NOT b”.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)is_not(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)is_not_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.is_not_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.is_not_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)isnot(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)isnot_distinct_from(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.isnot_distinct_from()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.isnot_distinct_from) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Implement the `IS NOT DISTINCT FROM` operator.

Renders “a IS NOT DISTINCT FROM b” on most platforms;
on some such as SQLite may render “a IS b”.

Changed in version 1.4: The `is_not_distinct_from()` operator is
renamed from `isnot_distinct_from()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)istartswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)key: str = None

*inherited from the* [ColumnElement.key](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.key) *attribute of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

The ‘key’ that in some circumstances refers to this object in a
Python namespace.

This typically refers to the “key” of the column as present in the
`.c` collection of a selectable, e.g. `sometable.c["somekey"]` would
return a [Column](#sqlalchemy.schema.Column) with a `.key` of “somekey”.

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)label(*name:str|None*) → [Label](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Label)[_T]

*inherited from the* [ColumnElement.label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Produce a column label, i.e. `<columnname> AS <name>`.

This is a shortcut to the [label()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.label) function.

If ‘name’ is `None`, an anonymous label name will be generated.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)match(*other:Any*, ***kwargs:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)not_ilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_ilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)not_in(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)not_like(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.not_like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.not_like) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)notilike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notilike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT ILIKE` operator.

This is equivalent to using negation with
[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike), i.e. `~x.ilike(y)`.

Changed in version 1.4: The `not_ilike()` operator is renamed from
`notilike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.ilike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.ilike)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)notin_(*other:Any*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)notlike(*other:Any*, *escape:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.notlike()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.notlike) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

implement the `NOT LIKE` operator.

This is equivalent to using negation with
[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like), i.e. `~x.like(y)`.

Changed in version 1.4: The `not_like()` operator is renamed from
`notlike()` in previous releases.  The previous name remains
available for backwards compatibility.

See also

[ColumnOperators.like()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.like)

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)nulls_first() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_first) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)nulls_last() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nulls_last) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)nullsfirst() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullsfirst()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullsfirst) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_first()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_first) clause against the
parent object.

Changed in version 1.4: The `nulls_first()` operator is
renamed from `nullsfirst()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)nullslast() → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

*inherited from the* [ColumnOperators.nullslast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.nullslast) *method of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Produce a [nulls_last()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.nulls_last) clause against the
parent object.

Changed in version 1.4: The `nulls_last()` operator is
renamed from `nullslast()` in previous releases.
The previous name remains available for backwards compatibility.

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)op(*opstring:str*, *precedence:int=0*, *is_comparison:bool=False*, *return_type:Type[TypeEngine[Any]]|TypeEngine[Any]|None=None*, *python_impl:Callable[...,Any]|None=None*) → Callable[[Any], [Operators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Operators)]

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)operate(*op:OperatorType*, **other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

*inherited from the* [ColumnElement.operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.operate) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

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

      method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)proxy_set

*inherited from the* [ColumnElement.proxy_set](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.proxy_set) *attribute of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

set of all columns we are proxying

as of 2.0 this is explicitly deannotated columns.  previously it was
effectively deannotated columns but wasn’t enforced.  annotated
columns should basically not go into sets if at all possible because
their hashing behavior is very non-performant.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)references(*column:Column[Any]*) → bool

Return True if this Column references the given column via foreign
key.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)regexp_match(*pattern:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)regexp_replace(*pattern:Any*, *replacement:Any*, *flags:str|None=None*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)reverse_operate(*op:OperatorType*, *other:Any*, ***kwargs:Any*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

*inherited from the* [ColumnElement.reverse_operate()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.reverse_operate) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Reverse operate on an argument.

Usage is the same as [operate()](#sqlalchemy.schema.Column.operate).

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)self_group(*against:OperatorType|None=None*) → [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]

*inherited from the* [ColumnElement.self_group()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.self_group) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.schema.Column.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.schema.Column.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)shares_lineage(*othercolumn:ColumnElement[Any]*) → bool

*inherited from the* [ColumnElement.shares_lineage()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.shares_lineage) *method of* [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)

Return True if the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
has a common ancestor to this [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement).

    method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)startswith(*other:Any*, *escape:str|None=None*, *autoescape:bool=False*) → [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

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

     attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)timetuple = None

*inherited from the* [ColumnOperators.timetuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.timetuple) *attribute of* [ColumnOperators](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators)

Hack, allows datetime objects to be compared on the LHS.

    attribute [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)unique: bool | None

The value of the [Column.unique](#sqlalchemy.schema.Column.params.unique) parameter.

Does not indicate if this [Column](#sqlalchemy.schema.Column) is actually subject to
a unique constraint or not; use [Table.indexes](#sqlalchemy.schema.Table.indexes) and
[Table.constraints](#sqlalchemy.schema.Table.constraints).

See also

[Table.indexes](#sqlalchemy.schema.Table.indexes)

[Table.constraints](#sqlalchemy.schema.Table.constraints).

     method [sqlalchemy.schema.Column.](#sqlalchemy.schema.Column)unique_params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.unique_params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

     class sqlalchemy.schema.MetaData

*inherits from* `sqlalchemy.schema.HasSchemaAttr`

A collection of [Table](#sqlalchemy.schema.Table)
objects and their associated schema
constructs.

Holds a collection of [Table](#sqlalchemy.schema.Table) objects as well as
an optional binding to an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).  If bound, the [Table](#sqlalchemy.schema.Table) objects
in the collection and their columns may participate in implicit SQL
execution.

The [Table](#sqlalchemy.schema.Table) objects themselves are stored in the
[MetaData.tables](#sqlalchemy.schema.MetaData.tables) dictionary.

[MetaData](#sqlalchemy.schema.MetaData) is a thread-safe object for read operations.
Construction of new tables within a single [MetaData](#sqlalchemy.schema.MetaData)
object,
either explicitly or via reflection, may not be completely thread-safe.

See also

[Describing Databases with MetaData](#metadata-describing) - Introduction to database metadata

| Member Name | Description |
| --- | --- |
| __init__() | Create a new MetaData object. |
| clear() | Clear all Table objects from this MetaData. |
| create_all() | Create all tables stored in this metadata. |
| drop_all() | Drop all tables stored in this metadata. |
| reflect() | Load all available table definitions from the database. |
| remove() | Remove the given Table object from this MetaData. |
| tables | A dictionary ofTableobjects keyed to their name or “table key”. |

   method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)__init__(*schema:str|None=None*, *quote_schema:bool|None=None*, *naming_convention:_NamingSchemaParameter|None=None*, *info:_InfoType|None=None*) → None

Create a new MetaData object.

  Parameters:

- **schema** –
  The default schema to use for the [Table](#sqlalchemy.schema.Table),
  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), and potentially other objects associated with
  this [MetaData](#sqlalchemy.schema.MetaData). Defaults to `None`.
  See also
  [Specifying a Default Schema Name with MetaData](#schema-metadata-schema-name) - details on how the
  [MetaData.schema](#sqlalchemy.schema.MetaData.params.schema) parameter is used.
  [Table.schema](#sqlalchemy.schema.Table.params.schema)
  [Sequence.schema](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.schema)
- **quote_schema** – Sets the `quote_schema` flag for those [Table](#sqlalchemy.schema.Table),
  [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), and other objects which make usage of the
  local `schema` name.
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **naming_convention** –
  a dictionary referring to values which
  will establish default naming conventions for [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint)
  and [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) objects, for those objects which are not given
  a name explicitly.
  The keys of this dictionary may be:
  - a constraint or Index class, e.g. the [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
    [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) class, the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
    class
  - a string mnemonic for one of the known constraint classes;
    `"fk"`, `"pk"`, `"ix"`, `"ck"`, `"uq"` for foreign key,
    primary key, index, check, and unique constraint, respectively.
  - the string name of a user-defined “token” that can be used
    to define new naming tokens.
  The values associated with each “constraint class” or “constraint
  mnemonic” key are string naming templates, such as
  `"uq_%(table_name)s_%(column_0_name)s"`,
  which describe how the name should be composed.  The values
  associated with user-defined “token” keys should be callables of the
  form `fn(constraint, table)`, which accepts the constraint/index
  object and [Table](#sqlalchemy.schema.Table) as arguments, returning a string
  result.
  The built-in names are as follows, some of which may only be
  available for certain types of constraint:
  > - `%(table_name)s` - the name of the [Table](#sqlalchemy.schema.Table)
  >   object
  >   associated with the constraint.
  > - `%(referred_table_name)s` - the name of the
  >   [Table](#sqlalchemy.schema.Table)
  >   object associated with the referencing target of a
  >   [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).
  > - `%(column_0_name)s` - the name of the [Column](#sqlalchemy.schema.Column)
  >   at
  >   index position “0” within the constraint.
  > - `%(column_0N_name)s` - the name of all [Column](#sqlalchemy.schema.Column)
  >   objects in order within the constraint, joined without a
  >   separator.
  > - `%(column_0_N_name)s` - the name of all
  >   [Column](#sqlalchemy.schema.Column)
  >   objects in order within the constraint, joined with an
  >   underscore as a separator.
  > - `%(column_0_label)s`, `%(column_0N_label)s`,
  >   `%(column_0_N_label)s` - the label of either the zeroth
  >   [Column](#sqlalchemy.schema.Column) or all `Columns`, separated with
  >   or without an underscore
  > - `%(column_0_key)s`, `%(column_0N_key)s`,
  >   `%(column_0_N_key)s` - the key of either the zeroth
  >   [Column](#sqlalchemy.schema.Column) or all `Columns`, separated with
  >   or without an underscore
  > - `%(referred_column_0_name)s`, `%(referred_column_0N_name)s` `%(referred_column_0_N_name)s`,  `%(referred_column_0_key)s`,
  >   `%(referred_column_0N_key)s`, …  column tokens which
  >   render the names/keys/labels of columns that are referenced
  >   by a  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).
  > - `%(constraint_name)s` - a special key that refers to the
  >   existing name given to the constraint.  When this key is
  >   present, the [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) object’s existing name will be
  >   replaced with one that is composed from template string that
  >   uses this token. When this token is present, it is required that
  >   the [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) is given an explicit name ahead of time.
  > - user-defined: any additional token may be implemented by passing
  >   it along with a `fn(constraint, table)` callable to the
  >   naming_convention dictionary.
  Added in version 1.3.0: - added new `%(column_0N_name)s`,
  `%(column_0_N_name)s`, and related tokens that produce
  concatenations of names, keys, or labels for all columns referred
  to by a given constraint.
  See also
  [Configuring Constraint Naming Conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions) - for detailed usage
  examples.

      method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)clear() → None

Clear all Table objects from this MetaData.

    method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)create_all(*bind:_CreateDropBind*, *tables:_typing_Sequence[Table]|None=None*, *checkfirst:bool=True*) → None

Create all tables stored in this metadata.

Conditional by default, will not attempt to recreate tables already
present in the target database.

  Parameters:

- **bind** – A [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) used to access the
  database.
- **tables** – Optional list of `Table` objects, which is a subset of the total
  tables in the `MetaData` (others are ignored).
- **checkfirst** – Defaults to True, don’t issue CREATEs for tables already present
  in the target database.

      method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)drop_all(*bind:_CreateDropBind*, *tables:_typing_Sequence[Table]|None=None*, *checkfirst:bool=True*) → None

Drop all tables stored in this metadata.

Conditional by default, will not attempt to drop tables not present in
the target database.

  Parameters:

- **bind** – A [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) used to access the
  database.
- **tables** – Optional list of `Table` objects, which is a subset of the
  total tables in the `MetaData` (others are ignored).
- **checkfirst** – Defaults to True, only issue DROPs for tables confirmed to be
  present in the target database.

      method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)reflect(*bind:Engine|Connection*, *schema:str|None=None*, *views:bool=False*, *only:_typing_Sequence[str]|Callable[[str,MetaData],bool]|None=None*, *extend_existing:bool=False*, *autoload_replace:bool=True*, *resolve_fks:bool=True*, ***dialect_kwargs:Any*) → None

Load all available table definitions from the database.

Automatically creates `Table` entries in this `MetaData` for any
table available in the database but not yet present in the
`MetaData`.  May be called multiple times to pick up tables recently
added to the database, however no special action is taken if a table
in this `MetaData` no longer exists in the database.

  Parameters:

- **bind** – A [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) used to access the
  database.
- **schema** – Optional, query and reflect tables from an alternate schema.
  If None, the schema associated with this [MetaData](#sqlalchemy.schema.MetaData)
  is used, if any.
- **views** – If True, also reflect views (materialized and plain).
- **only** –
  Optional.  Load only a sub-set of available named tables.  May be
  specified as a sequence of names or a callable.
  If a sequence of names is provided, only those tables will be
  reflected.  An error is raised if a table is requested but not
  available.  Named tables already present in this `MetaData` are
  ignored.
  If a callable is provided, it will be used as a boolean predicate to
  filter the list of potential table names.  The callable is called
  with a table name and this `MetaData` instance as positional
  arguments and should return a true value for any table to reflect.
- **extend_existing** – Passed along to each [Table](#sqlalchemy.schema.Table) as
  [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing).
- **autoload_replace** – Passed along to each [Table](#sqlalchemy.schema.Table)
  as
  [Table.autoload_replace](#sqlalchemy.schema.Table.params.autoload_replace).
- **resolve_fks** –
  if True, reflect [Table](#sqlalchemy.schema.Table)
  objects linked
  to [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects located in each
  [Table](#sqlalchemy.schema.Table).
  For [MetaData.reflect()](#sqlalchemy.schema.MetaData.reflect),
  this has the effect of reflecting
  related tables that might otherwise not be in the list of tables
  being reflected, for example if the referenced table is in a
  different schema or is omitted via the
  [MetaData.reflect.only](#sqlalchemy.schema.MetaData.reflect.params.only) parameter.  When False,
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects are not followed to the
  [Table](#sqlalchemy.schema.Table)
  in which they link, however if the related table is also part of the
  list of tables that would be reflected in any case, the
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object will still resolve to its related
  [Table](#sqlalchemy.schema.Table) after the [MetaData.reflect()](#sqlalchemy.schema.MetaData.reflect)
  operation is
  complete.   Defaults to True.
  Added in version 1.3.0.
  See also
  [Table.resolve_fks](#sqlalchemy.schema.Table.params.resolve_fks)
- ****dialect_kwargs** – Additional keyword arguments not mentioned
  above are dialect specific, and passed in the form
  `<dialectname>_<argname>`.  See the documentation regarding an
  individual dialect at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on
  documented arguments.

See also

[Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html)

[DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) - Event used to customize
the reflected columns. Usually used to generalize the types using
[TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic)

[Reflecting with Database-Agnostic Types](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-dbagnostic-types) - describes how to
reflect tables using general types.

     method [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)remove(*table:Table*) → None

Remove the given Table object from this MetaData.

    property sorted_tables: List[[Table](#sqlalchemy.schema.Table)]

Returns a list of [Table](#sqlalchemy.schema.Table) objects sorted in order of
foreign key dependency.

The sorting will place [Table](#sqlalchemy.schema.Table)
objects that have dependencies
first, before the dependencies themselves, representing the
order in which they can be created.   To get the order in which
the tables would be dropped, use the `reversed()` Python built-in.

Warning

The [MetaData.sorted_tables](#sqlalchemy.schema.MetaData.sorted_tables) attribute cannot by itself
accommodate automatic resolution of dependency cycles between
tables, which are usually caused by mutually dependent foreign key
constraints. When these cycles are detected, the foreign keys
of these tables are omitted from consideration in the sort.
A warning is emitted when this condition occurs, which will be an
exception raise in a future release.   Tables which are not part
of the cycle will still be returned in dependency order.

To resolve these cycles, the
[ForeignKeyConstraint.use_alter](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) parameter may be
applied to those constraints which create a cycle.  Alternatively,
the [sort_tables_and_constraints()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables_and_constraints) function will
automatically return foreign key constraints in a separate
collection when cycles are detected so that they may be applied
to a schema separately.

Changed in version 1.3.17: - a warning is emitted when
[MetaData.sorted_tables](#sqlalchemy.schema.MetaData.sorted_tables) cannot perform a proper sort
due to cyclical dependencies.  This will be an exception in a
future release.  Additionally, the sort will continue to return
other tables not involved in the cycle in dependency order which
was not the case previously.

See also

[sort_tables()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables)

[sort_tables_and_constraints()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables_and_constraints)

[MetaData.tables](#sqlalchemy.schema.MetaData.tables)

[Inspector.get_table_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_names)

[Inspector.get_sorted_table_and_fkc_names()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names)

     attribute [sqlalchemy.schema.MetaData.](#sqlalchemy.schema.MetaData)tables: util.FacadeDict[str, [Table](#sqlalchemy.schema.Table)]

A dictionary of [Table](#sqlalchemy.schema.Table)
objects keyed to their name or “table key”.

The exact key is that determined by the [Table.key](#sqlalchemy.schema.Table.key)
attribute;
for a table with no [Table.schema](#sqlalchemy.schema.Table.schema) attribute,
this is the same
as `Table.name`.  For a table with a schema,
it is typically of the
form `schemaname.tablename`.

See also

[MetaData.sorted_tables](#sqlalchemy.schema.MetaData.sorted_tables)

      class sqlalchemy.schema.SchemaConst

*inherits from* `enum.Enum`

| Member Name | Description |
| --- | --- |
| BLANK_SCHEMA | Symbol indicating that aTableorSequenceshould have ‘None’ for its schema, even if the parentMetaDatahas specified a schema. |
| NULL_UNSPECIFIED | Symbol indicating the “nullable” keyword was not passed to a Column. |
| RETAIN_SCHEMA | Symbol indicating that aTable,Sequenceor in some cases aForeignKeyobject, in situations
where the object is being copied for aTable.to_metadata()operation, should retain the schema name that it already has. |

   attribute [sqlalchemy.schema.SchemaConst.](#sqlalchemy.schema.SchemaConst)BLANK_SCHEMA = 2

Symbol indicating that a [Table](#sqlalchemy.schema.Table) or [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)
should have ‘None’ for its schema, even if the parent
[MetaData](#sqlalchemy.schema.MetaData) has specified a schema.

See also

[MetaData.schema](#sqlalchemy.schema.MetaData.params.schema)

[Table.schema](#sqlalchemy.schema.Table.params.schema)

[Sequence.schema](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.schema)

     attribute [sqlalchemy.schema.SchemaConst.](#sqlalchemy.schema.SchemaConst)NULL_UNSPECIFIED = 3

Symbol indicating the “nullable” keyword was not passed to a Column.

This is used to distinguish between the use case of passing
`nullable=None` to a [Column](#sqlalchemy.schema.Column), which has special meaning
on some backends such as SQL Server.

    attribute [sqlalchemy.schema.SchemaConst.](#sqlalchemy.schema.SchemaConst)RETAIN_SCHEMA = 1

Symbol indicating that a [Table](#sqlalchemy.schema.Table), [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)
or in some cases a [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object, in situations
where the object is being copied for a [Table.to_metadata()](#sqlalchemy.schema.Table.to_metadata)
operation, should retain the schema name that it already has.

     class sqlalchemy.schema.SchemaItem

*inherits from* `sqlalchemy.sql.expression.SchemaVisitable`

Base class for items that define a database schema.

| Member Name | Description |
| --- | --- |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   attribute [sqlalchemy.schema.SchemaItem.](#sqlalchemy.schema.SchemaItem)info

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](#sqlalchemy.schema.Table) and [Column](#sqlalchemy.schema.Column).

     function sqlalchemy.schema.insert_sentinel(*name:str|None=None*, *type_:_TypeEngineArgument[_T]|None=None*, ***, *default:Any|None=None*, *omit_from_statements:bool=True*) → [Column](#sqlalchemy.schema.Column)[Any]

Provides a surrogate [Column](#sqlalchemy.schema.Column) that will act as a
dedicated insert [sentinel](https://docs.sqlalchemy.org/en/20/glossary.html#term-sentinel) column, allowing efficient bulk
inserts with deterministic RETURNING sorting for tables that
don’t otherwise have qualifying primary key configurations.

Adding this column to a [Table](#sqlalchemy.schema.Table) object requires that a
corresponding database table actually has this column present, so if adding
it to an existing model, existing database tables would need to be migrated
(e.g. using ALTER TABLE or similar) to include this column.

For background on how this object is used, see the section
[Configuring Sentinel Columns](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-sentinel-columns) as part of the
section [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues).

The [Column](#sqlalchemy.schema.Column) returned will be a nullable integer column by
default and make use of a sentinel-specific default generator used only in
“insertmanyvalues” operations.

See also

[orm_insert_sentinel()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.orm_insert_sentinel)

[Column.insert_sentinel](#sqlalchemy.schema.Column.params.insert_sentinel)

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

[Configuring Sentinel Columns](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-sentinel-columns)

Added in version 2.0.10.

     class sqlalchemy.schema.Table

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, `sqlalchemy.schema.HasSchemaAttr`, [sqlalchemy.sql.expression.TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause), `sqlalchemy.inspection.Inspectable`

Represent a table in a database.

e.g.:

```
mytable = Table(
    "mytable",
    metadata,
    Column("mytable_id", Integer, primary_key=True),
    Column("value", String(50)),
)
```

The [Table](#sqlalchemy.schema.Table)
object constructs a unique instance of itself based
on its name and optional schema name within the given
[MetaData](#sqlalchemy.schema.MetaData) object. Calling the [Table](#sqlalchemy.schema.Table)
constructor with the same name and same [MetaData](#sqlalchemy.schema.MetaData) argument
a second time will return the *same* [Table](#sqlalchemy.schema.Table)
object - in this way
the [Table](#sqlalchemy.schema.Table) constructor acts as a registry function.

See also

[Describing Databases with MetaData](#metadata-describing) - Introduction to database metadata

| Member Name | Description |
| --- | --- |
| __init__() | Constructor forTable. |
| add_is_dependent_on() | Add a ‘dependency’ for this Table. |
| alias() | Return an alias of thisFromClause. |
| append_column() | Append aColumnto thisTable. |
| append_constraint() | Append aConstraintto thisTable. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| c | A synonym forFromClause.columns |
| columns | A named-based collection ofColumnElementobjects maintained by thisFromClause. |
| compare() | Compare thisClauseElementto
the givenClauseElement. |
| compile() | Compile this SQL expression. |
| constraints | A collection of allConstraintobjects associated with
thisTable. |
| corresponding_column() | Given aColumnElement, return the exportedColumnElementobject from theSelectable.exported_columnscollection of thisSelectablewhich corresponds to that
originalColumnElementvia a common ancestor
column. |
| create() | Issue aCREATEstatement for thisTable, using the givenConnectionorEnginefor connectivity. |
| delete() | Generate adelete()construct against thisTableClause. |
| description |  |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| drop() | Issue aDROPstatement for thisTable, using the givenConnectionorEnginefor connectivity. |
| entity_namespace | Return a namespace used for name-based access in SQL expressions. |
| exported_columns | AColumnCollectionthat represents the “exported”
columns of thisSelectable. |
| foreign_keys | Return the collection ofForeignKeymarker objects
which this FromClause references. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| implicit_returning | TableClausedoesn’t support having a primary key or column
-level defaults, so implicit returning doesn’t apply. |
| indexes | A collection of allIndexobjects associated with thisTable. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |
| inherit_cache | Indicate if thisHasCacheKeyinstance should make use of the
cache key generation scheme used by its immediate superclass. |
| insert() | Generate anInsertconstruct against thisTableClause. |
| is_derived_from() | ReturnTrueif thisFromClauseis
‘derived’ from the givenFromClause. |
| join() | Return aJoinfrom thisFromClauseto anotherFromClause. |
| lateral() | Return a LATERAL alias of thisSelectable. |
| outerjoin() | Return aJoinfrom thisFromClauseto anotherFromClause, with the “isouter” flag set to
True. |
| params() | Return a copy withbindparam()elements
replaced. |
| primary_key | Return the iterable collection ofColumnobjects
which comprise the primary key of this_selectable.FromClause. |
| replace_selectable() | Replace all occurrences ofFromClause‘old’ with the givenAliasobject, returning a copy of thisFromClause. |
| schema | Define the ‘schema’ attribute for thisFromClause. |
| select() | Return a SELECT of thisFromClause. |
| self_group() | Apply a ‘grouping’ to thisClauseElement. |
| table_valued() | Return aTableValuedColumnobject for thisFromClause. |
| tablesample() | Return a TABLESAMPLE alias of thisFromClause. |
| to_metadata() | Return a copy of thisTableassociated with a
differentMetaData. |
| tometadata() | Return a copy of thisTableassociated with a differentMetaData. |
| unique_params() | Return a copy withbindparam()elements
replaced. |
| update() | Generate anupdate()construct against thisTableClause. |

   method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)__init__(*name:str*, *metadata:MetaData*, **args:SchemaItem*, *schema:str|Literal[SchemaConst.BLANK_SCHEMA]|None=None*, *quote:bool|None=None*, *quote_schema:bool|None=None*, *autoload_with:Engine|Connection|None=None*, *autoload_replace:bool=True*, *keep_existing:bool=False*, *extend_existing:bool=False*, *resolve_fks:bool=True*, *include_columns:Collection[str]|None=None*, *implicit_returning:bool=True*, *comment:str|None=None*, *info:Dict[Any,Any]|None=None*, *listeners:_typing_Sequence[Tuple[str,Callable[...,Any]]]|None=None*, *prefixes:_typing_Sequence[str]|None=None*, *_extend_on:Set[Table]|None=None*, *_no_init:bool=True*, ***kw:Any*) → None

Constructor for [Table](#sqlalchemy.schema.Table).

  Parameters:

- **name** –
  The name of this table as represented in the database.
  The table name, along with the value of the `schema` parameter,
  forms a key which uniquely identifies this [Table](#sqlalchemy.schema.Table)
  within
  the owning [MetaData](#sqlalchemy.schema.MetaData) collection.
  Additional calls to [Table](#sqlalchemy.schema.Table) with the same name,
  metadata,
  and schema name will return the same [Table](#sqlalchemy.schema.Table) object.
  Names which contain no upper case characters
  will be treated as case insensitive names, and will not be quoted
  unless they are a reserved word or contain special characters.
  A name with any number of upper case characters is considered
  to be case sensitive, and will be sent as quoted.
  To enable unconditional quoting for the table name, specify the flag
  `quote=True` to the constructor, or use the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name)
  construct to specify the name.
- **metadata** – a [MetaData](#sqlalchemy.schema.MetaData)
  object which will contain this
  table.  The metadata is used as a point of association of this table
  with other tables which are referenced via foreign key.  It also
  may be used to associate this table with a particular
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).
- ***args** – Additional positional arguments are used primarily
  to add the list of [Column](#sqlalchemy.schema.Column)
  objects contained within this
  table. Similar to the style of a CREATE TABLE statement, other
  [SchemaItem](#sqlalchemy.schema.SchemaItem) constructs may be added here, including
  [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint), and
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).
- **autoload_replace** –
  Defaults to `True`; when using
  [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with)
  in conjunction with [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing),
  indicates
  that [Column](#sqlalchemy.schema.Column) objects present in the already-existing
  [Table](#sqlalchemy.schema.Table)
  object should be replaced with columns of the same
  name retrieved from the autoload process.   When `False`, columns
  already present under existing names will be omitted from the
  reflection process.
  Note that this setting does not impact [Column](#sqlalchemy.schema.Column) objects
  specified programmatically within the call to [Table](#sqlalchemy.schema.Table)
  that
  also is autoloading; those [Column](#sqlalchemy.schema.Column) objects will always
  replace existing columns of the same name when
  [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing) is `True`.
  See also
  [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with)
  [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing)
- **autoload_with** –
  An [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
  [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object,
  or a [Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector) object as returned by
  [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect)
  against one, with which this [Table](#sqlalchemy.schema.Table)
  object will be reflected.
  When set to a non-None value, the autoload process will take place
  for this table against the given engine or connection.
  See also
  [Reflecting Database Objects](https://docs.sqlalchemy.org/en/20/core/reflection.html)
  [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect)
  [Reflecting with Database-Agnostic Types](https://docs.sqlalchemy.org/en/20/core/reflection.html#metadata-reflection-dbagnostic-types)
- **extend_existing** –
  When `True`, indicates that if this
  [Table](#sqlalchemy.schema.Table) is already present in the given
  [MetaData](#sqlalchemy.schema.MetaData),
  apply further arguments within the constructor to the existing
  [Table](#sqlalchemy.schema.Table).
  If [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing) or
  [Table.keep_existing](#sqlalchemy.schema.Table.params.keep_existing) are not set,
  and the given name
  of the new [Table](#sqlalchemy.schema.Table) refers to a [Table](#sqlalchemy.schema.Table)
  that is
  already present in the target [MetaData](#sqlalchemy.schema.MetaData) collection,
  and
  this [Table](#sqlalchemy.schema.Table)
  specifies additional columns or other constructs
  or flags that modify the table’s state, an
  error is raised.  The purpose of these two mutually-exclusive flags
  is to specify what action should be taken when a
  [Table](#sqlalchemy.schema.Table)
  is specified that matches an existing [Table](#sqlalchemy.schema.Table),
  yet specifies
  additional constructs.
  [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing)
  will also work in conjunction
  with [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with) to run a new reflection
  operation against the database, even if a [Table](#sqlalchemy.schema.Table)
  of the same name is already present in the target
  [MetaData](#sqlalchemy.schema.MetaData); newly reflected [Column](#sqlalchemy.schema.Column)
  objects
  and other options will be added into the state of the
  [Table](#sqlalchemy.schema.Table), potentially overwriting existing columns
  and options of the same name.
  As is always the case with [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with),
  [Column](#sqlalchemy.schema.Column) objects can be specified in the same
  [Table](#sqlalchemy.schema.Table)
  constructor, which will take precedence.  Below, the existing
  table `mytable` will be augmented with [Column](#sqlalchemy.schema.Column)
  objects
  both reflected from the database, as well as the given
  [Column](#sqlalchemy.schema.Column)
  named “y”:
  ```
  Table(
      "mytable",
      metadata,
      Column("y", Integer),
      extend_existing=True,
      autoload_with=engine,
  )
  ```
  See also
  [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with)
  [Table.autoload_replace](#sqlalchemy.schema.Table.params.autoload_replace)
  [Table.keep_existing](#sqlalchemy.schema.Table.params.keep_existing)
- **implicit_returning** –
  True by default - indicates that
  RETURNING can be used, typically by the ORM, in order to fetch
  server-generated values such as primary key values and
  server side defaults, on those backends which support RETURNING.
  In modern SQLAlchemy there is generally no reason to alter this
  setting, except for some backend specific cases
  (see [Triggers](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-triggers) in the SQL Server dialect documentation
  for one such example).
- **include_columns** – A list of strings indicating a subset of
  columns to be loaded via the `autoload` operation; table columns who
  aren’t present in this list will not be represented on the resulting
  `Table` object. Defaults to `None` which indicates all columns
  should be reflected.
- **resolve_fks** –
  Whether or not to reflect [Table](#sqlalchemy.schema.Table)
  objects
  related to this one via [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) objects, when
  [Table.autoload_with](#sqlalchemy.schema.Table.params.autoload_with) is
  specified.   Defaults to True.  Set to False to disable reflection of
  related tables as [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
  objects are encountered; may be
  used either to save on SQL calls or to avoid issues with related tables
  that can’t be accessed. Note that if a related table is already present
  in the [MetaData](#sqlalchemy.schema.MetaData) collection, or becomes present later,
  a
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) object associated with this
  [Table](#sqlalchemy.schema.Table) will
  resolve to that table normally.
  Added in version 1.3.
  See also
  [MetaData.reflect.resolve_fks](#sqlalchemy.schema.MetaData.reflect.params.resolve_fks)
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **keep_existing** –
  When `True`, indicates that if this Table
  is already present in the given [MetaData](#sqlalchemy.schema.MetaData), ignore
  further arguments within the constructor to the existing
  [Table](#sqlalchemy.schema.Table), and return the [Table](#sqlalchemy.schema.Table)
  object as
  originally created. This is to allow a function that wishes
  to define a new [Table](#sqlalchemy.schema.Table) on first call, but on
  subsequent calls will return the same [Table](#sqlalchemy.schema.Table),
  without any of the declarations (particularly constraints)
  being applied a second time.
  If [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing) or
  [Table.keep_existing](#sqlalchemy.schema.Table.params.keep_existing) are not set,
  and the given name
  of the new [Table](#sqlalchemy.schema.Table) refers to a [Table](#sqlalchemy.schema.Table)
  that is
  already present in the target [MetaData](#sqlalchemy.schema.MetaData) collection,
  and
  this [Table](#sqlalchemy.schema.Table)
  specifies additional columns or other constructs
  or flags that modify the table’s state, an
  error is raised.  The purpose of these two mutually-exclusive flags
  is to specify what action should be taken when a
  [Table](#sqlalchemy.schema.Table)
  is specified that matches an existing [Table](#sqlalchemy.schema.Table),
  yet specifies
  additional constructs.
  See also
  [Table.extend_existing](#sqlalchemy.schema.Table.params.extend_existing)
- **listeners** –
  A list of tuples of the form `(<eventname>, <fn>)`
  which will be passed to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) upon construction.
  This alternate hook to [listen()](https://docs.sqlalchemy.org/en/20/core/event.html#sqlalchemy.event.listen) allows the establishment
  of a listener function specific to this [Table](#sqlalchemy.schema.Table) before
  the “autoload” process begins.  Historically this has been intended
  for use with the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event, however
  note that this event hook may now be associated with the
  [MetaData](#sqlalchemy.schema.MetaData) object directly:
  ```
  def listen_for_reflect(table, column_info):
      "handle the column reflection event"
      # ...
  t = Table(
      "sometable",
      autoload_with=engine,
      listeners=[("column_reflect", listen_for_reflect)],
  )
  ```
  See also
  [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect)
- **must_exist** – When `True`, indicates that this Table must already
  be present in the given [MetaData](#sqlalchemy.schema.MetaData) collection, else
  an exception is raised.
- **prefixes** – A list of strings to insert after CREATE in the CREATE TABLE
  statement.  They will be separated by spaces.
- **quote** –
  Force quoting of this table’s name on or off, corresponding
  to `True` or `False`.  When left at its default of `None`,
  the column identifier will be quoted according to whether the name is
  case sensitive (identifiers with at least one upper case character are
  treated as case sensitive), or if it’s a reserved word.  This flag
  is only needed to force quoting of a reserved word which is not known
  by the SQLAlchemy dialect.
  Note
  setting this flag to `False` will not provide
  case-insensitive behavior for table reflection; table reflection
  will always search for a mixed-case name in a case sensitive
  fashion.  Case insensitive names are specified in SQLAlchemy only
  by stating the name with all lower case characters.
- **quote_schema** – same as ‘quote’ but applies to the schema identifier.
- **schema** –
  The schema name for this table, which is required if
  the table resides in a schema other than the default selected schema
  for the engine’s database connection.  Defaults to `None`.
  If the owning [MetaData](#sqlalchemy.schema.MetaData) of this [Table](#sqlalchemy.schema.Table)
  specifies its
  own [MetaData.schema](#sqlalchemy.schema.MetaData.params.schema) parameter,
  then that schema name will
  be applied to this [Table](#sqlalchemy.schema.Table)
  if the schema parameter here is set
  to `None`.  To set a blank schema name on a [Table](#sqlalchemy.schema.Table)
  that
  would otherwise use the schema set on the owning
  [MetaData](#sqlalchemy.schema.MetaData),
  specify the special symbol [BLANK_SCHEMA](#sqlalchemy.schema.SchemaConst.BLANK_SCHEMA).
  The quoting rules for the schema name are the same as those for the
  `name` parameter, in that quoting is applied for reserved words or
  case-sensitive names; to enable unconditional quoting for the schema
  name, specify the flag `quote_schema=True` to the constructor, or use
  the [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) construct to specify the name.
- **comment** –
  Optional string that will render an SQL comment on table
  creation.
  Added in version 1.2: Added the [Table.comment](#sqlalchemy.schema.Table.params.comment)
  parameter
  to [Table](#sqlalchemy.schema.Table).
- ****kw** – Additional keyword arguments not mentioned above are
  dialect specific, and passed in the form `<dialectname>_<argname>`.
  See the documentation regarding an individual dialect at
  [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on documented arguments.

      method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)add_is_dependent_on(*table:Table*) → None

Add a ‘dependency’ for this Table.

This is another Table object which must be created
first before this one can, or dropped after this one.

Usually, dependencies between tables are determined via
ForeignKey objects.   However, for other situations that
create dependencies outside of foreign keys (rules, inheriting),
this method can manually establish such a link.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)alias(*name:str|None=None*, *flat:bool=False*) → NamedFromClause

*inherited from the* [FromClause.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.alias) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return an alias of this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

E.g.:

```
a2 = some_table.alias("a2")
```

The above code creates an [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
object which can be used
as a FROM clause in any SELECT statement.

See also

[Using Aliases](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-using-aliases)

[alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.alias)

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)append_column(*column:ColumnClause[Any]*, *replace_existing:bool=False*) → None

Append a [Column](#sqlalchemy.schema.Column) to this [Table](#sqlalchemy.schema.Table).

The “key” of the newly added [Column](#sqlalchemy.schema.Column), i.e. the
value of its `.key` attribute, will then be available
in the `.c` collection of this [Table](#sqlalchemy.schema.Table), and the
column definition will be included in any CREATE TABLE, SELECT,
UPDATE, etc. statements generated from this [Table](#sqlalchemy.schema.Table)
construct.

Note that this does **not** change the definition of the table
as it exists within any underlying database, assuming that
table has already been created in the database.   Relational
databases support the addition of columns to existing tables
using the SQL ALTER command, which would need to be
emitted for an already-existing table that doesn’t contain
the newly added column.

  Parameters:

**replace_existing** –

When `True`, allows replacing existing
columns. When `False`, the default, an warning will be raised
if a column with the same `.key` already exists. A future
version of sqlalchemy will instead rise a warning.

Added in version 1.4.0.

       method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)append_constraint(*constraint:Index|Constraint*) → None

Append a [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) to this
[Table](#sqlalchemy.schema.Table).

This has the effect of the constraint being included in any
future CREATE TABLE statement, assuming specific DDL creation
events have not been associated with the given
[Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) object.

Note that this does **not** produce the constraint within the
relational database automatically, for a table that already exists
in the database.   To add a constraint to an
existing relational database table, the SQL ALTER command must
be used.  SQLAlchemy also provides the
[AddConstraint](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.AddConstraint) construct which can produce this SQL when
invoked as an executable clause.

    classmethod [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

*inherited from the* `DialectKWArgs.argument_for()` *method of* `DialectKWArgs`

Add a new kind of dialect-specific keyword argument for this class.

E.g.:

```
Index.argument_for("mydialect", "length", None)

some_index = Index("a", "b", mydialect_length=5)
```

The [DialectKWArgs.argument_for()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.argument_for) method is a per-argument
way adding extra arguments to the
[DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) dictionary. This
dictionary provides a list of argument names accepted by various
schema-level constructs on behalf of a dialect.

New dialects should typically specify this dictionary all at once as a
data member of the dialect class.  The use case for ad-hoc addition of
argument names is typically for end-user code that is also using
a custom compilation scheme which consumes the additional arguments.

  Parameters:

- **dialect_name** – name of a dialect.  The dialect must be
  locatable, else a [NoSuchModuleError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoSuchModuleError) is raised.   The
  dialect must also include an existing
  [DefaultDialect.construct_arguments](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultDialect.construct_arguments) collection, indicating
  that it participates in the keyword-argument validation and default
  system, else [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError) is raised.  If the dialect does
  not include this collection, then any keyword argument can be
  specified on behalf of this dialect already.  All dialects packaged
  within SQLAlchemy include this collection, however for third party
  dialects, support may vary.
- **argument_name** – name of the parameter.
- **default** – default value of the parameter.

      property autoincrement_column: [Column](#sqlalchemy.schema.Column)[int] | None

Returns the [Column](#sqlalchemy.schema.Column) object which currently represents
the “auto increment” column, if any, else returns None.

This is based on the rules for [Column](#sqlalchemy.schema.Column) as defined by the
[Column.autoincrement](#sqlalchemy.schema.Column.params.autoincrement) parameter, which generally means the
column within a single integer column primary key constraint that is
not constrained by a foreign key.   If the table does not have such
a primary key constraint, then there’s no “autoincrement” column.
A [Table](#sqlalchemy.schema.Table) may have only one column defined as the
“autoincrement” column.

Added in version 2.0.4.

See also

[Column.autoincrement](#sqlalchemy.schema.Column.params.autoincrement)

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)c

*inherited from the* [FromClause.c](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.c) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

A synonym for [FromClause.columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.columns)

  Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)

      attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)columns

*inherited from the* [FromClause.columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.columns) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

A named-based collection of [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
objects maintained by this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

The [columns](#sqlalchemy.schema.Table.columns), or [c](#sqlalchemy.schema.Table.c) collection, is the gateway
to the construction of SQL expressions using table-bound or
other selectable-bound columns:

```
select(mytable).where(mytable.c.somecolumn == 5)
```

   Returns:

a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) object.

      method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)compare(*other:ClauseElement*, ***kw:Any*) → bool

*inherited from the* [ClauseElement.compare()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compare) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Compare this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to
the given [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

Subclasses should override the default behavior, which is a
straight identity comparison.

**kw are arguments consumed by subclass `compare()` methods and
may be used to modify the criteria for comparison
(see [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)).

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)compile(*bind:_HasDialect|None=None*, *dialect:Dialect|None=None*, ***kw:Any*) → [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled)

*inherited from the* `CompilerElement.compile()` *method of* `CompilerElement`

Compile this SQL expression.

The return value is a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.
Calling `str()` or `unicode()` on the returned value will yield a
string representation of the result. The
[Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object also can return a
dictionary of bind parameter names and values
using the `params` accessor.

  Parameters:

- **bind** – An [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which
  can provide a [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) in order to generate a
  [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  If the `bind` and
  `dialect` parameters are both omitted, a default SQL compiler
  is used.
- **column_keys** – Used for INSERT and UPDATE statements, a list of
  column names which should be present in the VALUES clause of the
  compiled statement. If `None`, all columns from the target table
  object are rendered.
- **dialect** – A [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) instance which can generate
  a [Compiled](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Compiled) object.  This argument takes precedence over
  the `bind` argument.
- **compile_kwargs** –
  optional dictionary of additional parameters
  that will be passed through to the compiler within all “visit”
  methods.  This allows any custom flag to be passed through to
  a custom compilation construct, for example.  It is also used
  for the case of passing the `literal_binds` flag through:
  ```
  from sqlalchemy.sql import table, column, select
  t = table("t", column("x"))
  s = select(t).where(t.c.x == 5)
  print(s.compile(compile_kwargs={"literal_binds": True}))
  ```

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)constraints: Set[[Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint)]

A collection of all [Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Constraint) objects associated with
this [Table](#sqlalchemy.schema.Table).

Includes [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint),
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint), [UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint),
[CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint).  A separate collection
[Table.foreign_key_constraints](#sqlalchemy.schema.Table.foreign_key_constraints) refers to the collection
of all [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects, and the
[Table.primary_key](#sqlalchemy.schema.Table.primary_key) attribute refers to the single
[PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) associated with the
[Table](#sqlalchemy.schema.Table).

See also

[Table.constraints](#sqlalchemy.schema.Table.constraints)

[Table.primary_key](#sqlalchemy.schema.Table.primary_key)

[Table.foreign_key_constraints](#sqlalchemy.schema.Table.foreign_key_constraints)

[Table.indexes](#sqlalchemy.schema.Table.indexes)

[Inspector](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector)

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)corresponding_column(*column:KeyedColumnElement[Any]*, *require_embedded:bool=False*) → KeyedColumnElement[Any] | None

*inherited from the* [Selectable.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.corresponding_column) *method of* [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable)

Given a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), return the exported
[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) object from the
[Selectable.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.exported_columns)
collection of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable)
which corresponds to that
original [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) via a common ancestor
column.

  Parameters:

- **column** – the target [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  to be matched.
- **require_embedded** – only return corresponding columns for
  the given [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement), if the given
  [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)
  is actually present within a sub-element
  of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).
  Normally the column will match if
  it merely shares a common ancestor with one of the exported
  columns of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

See also

[Selectable.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.exported_columns) - the
[ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that is used for the operation.

[ColumnCollection.corresponding_column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection.corresponding_column)
- implementation
method.

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)create(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue a `CREATE` statement for this
[Table](#sqlalchemy.schema.Table), using the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
for connectivity.

See also

[MetaData.create_all()](#sqlalchemy.schema.MetaData.create_all).

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)delete() → [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)

*inherited from the* [TableClause.delete()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.delete) *method of* [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)

Generate a [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) construct against this
[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.delete().where(table.c.id == 7)
```

See [delete()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.delete) for argument and usage information.

    attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)description

*inherited from the* [TableClause.description](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.description) *attribute of* [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)

     property dialect_kwargs: _DialectArgView

A collection of keyword arguments specified as dialect-specific
options to this construct.

The arguments are present here in their original `<dialect>_<kwarg>`
format.  Only arguments that were actually passed are included;
unlike the [DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) collection, which
contains all options known by this dialect including defaults.

The collection is also writable; keys are accepted of the
form `<dialect>_<kwarg>` where the value will be assembled
into the list of options.

See also

[DialectKWArgs.dialect_options](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_options) - nested dictionary form

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)dialect_options

*inherited from the* `DialectKWArgs.dialect_options` *attribute of* `DialectKWArgs`

A collection of keyword arguments specified as dialect-specific
options to this construct.

This is a two-level nested registry, keyed to `<dialect_name>`
and `<argument_name>`.  For example, the `postgresql_where`
argument would be locatable as:

```
arg = my_object.dialect_options["postgresql"]["where"]
```

Added in version 0.9.2.

See also

[DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs) - flat dictionary form

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)drop(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue a `DROP` statement for this
[Table](#sqlalchemy.schema.Table), using the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) for connectivity.

See also

[MetaData.drop_all()](#sqlalchemy.schema.MetaData.drop_all).

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)entity_namespace

*inherited from the* [FromClause.entity_namespace](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.entity_namespace) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return a namespace used for name-based access in SQL expressions.

This is the namespace that is used to resolve “filter_by()” type
expressions, such as:

```
stmt.filter_by(address="some address")
```

It defaults to the `.c` collection, however internally it can
be overridden using the “entity_namespace” annotation to deliver
alternative results.

    attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)exported_columns

*inherited from the* [FromClause.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.exported_columns) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection)
that represents the “exported”
columns of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

The “exported” columns for a [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
object are synonymous
with the [FromClause.columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.columns) collection.

Added in version 1.4.

See also

[Selectable.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.exported_columns)

[SelectBase.exported_columns](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.SelectBase.exported_columns)

     property foreign_key_constraints: Set[[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)]

[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) objects referred to by this
[Table](#sqlalchemy.schema.Table).

This list is produced from the collection of
[ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
objects currently associated.

See also

[Table.constraints](#sqlalchemy.schema.Table.constraints)

[Table.foreign_keys](#sqlalchemy.schema.Table.foreign_keys)

[Table.indexes](#sqlalchemy.schema.Table.indexes)

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)foreign_keys

*inherited from the* [FromClause.foreign_keys](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.foreign_keys) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return the collection of [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) marker objects
which this FromClause references.

Each [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) is a member of a
[Table](#sqlalchemy.schema.Table)-wide
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).

See also

[Table.foreign_key_constraints](#sqlalchemy.schema.Table.foreign_key_constraints)

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)implicit_returning = False

*inherited from the* [TableClause.implicit_returning](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.implicit_returning) *attribute of* [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)

[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)
doesn’t support having a primary key or column
-level defaults, so implicit returning doesn’t apply.

    attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)indexes: Set[[Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)]

A collection of all [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) objects associated with this
[Table](#sqlalchemy.schema.Table).

See also

[Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes)

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)info

*inherited from the* [SchemaItem.info](#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](#sqlalchemy.schema.Table) and [Column](#sqlalchemy.schema.Column).

    attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)inherit_cache = None

*inherited from the* `HasCacheKey.inherit_cache` *attribute of* [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey)

Indicate if this [HasCacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey) instance should make use of the
cache key generation scheme used by its immediate superclass.

The attribute defaults to `None`, which indicates that a construct has
not yet taken into account whether or not its appropriate for it to
participate in caching; this is functionally equivalent to setting the
value to `False`, except that a warning is also emitted.

This flag can be set to `True` on a particular class, if the SQL that
corresponds to the object does not change based on attributes which
are local to this class, and not its superclass.

See also

[Enabling Caching Support for Custom Constructs](https://docs.sqlalchemy.org/en/20/core/compiler.html#compilerext-caching) - General guideslines for setting the
[HasCacheKey.inherit_cache](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.traversals.HasCacheKey.inherit_cache) attribute for third-party or user
defined SQL constructs.

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)insert() → [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

*inherited from the* [TableClause.insert()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.insert) *method of* [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)

Generate an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct against this
[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.insert().values(name="foo")
```

See [insert()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert) for argument and usage information.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)is_derived_from(*fromclause:FromClause|None*) → bool

*inherited from the* [FromClause.is_derived_from()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.is_derived_from) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return `True` if this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) is
‘derived’ from the given `FromClause`.

An example would be an Alias of a Table is derived from that Table.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)join(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *isouter:bool=False*, *full:bool=False*) → [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)

*inherited from the* [FromClause.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) from this
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
to another `FromClause`.

E.g.:

```
from sqlalchemy import join

j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id
)
stmt = select(user_table).select_from(j)
```

would emit SQL along the lines of:

```
SELECT user.id, user.name FROM user
JOIN address ON user.id = address.user_id
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **isouter** – if True, render a LEFT OUTER JOIN, instead of JOIN.
- **full** – if True, render a FULL OUTER JOIN, instead of LEFT OUTER
  JOIN.  Implies [FromClause.join.isouter](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join.params.isouter).

See also

[join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.join) - standalone function

[Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) - the type of object produced

     property key: str

Return the ‘key’ for this [Table](#sqlalchemy.schema.Table).

This value is used as the dictionary key within the
[MetaData.tables](#sqlalchemy.schema.MetaData.tables) collection.   It is typically the same
as that of `Table.name` for a table with no
[Table.schema](#sqlalchemy.schema.Table.schema)
set; otherwise it is typically of the form
`schemaname.tablename`.

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)lateral(*name:str|None=None*) → LateralFromClause

*inherited from the* [Selectable.lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.lateral) *method of* [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable)

Return a LATERAL alias of this [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable).

The return value is the [Lateral](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Lateral) construct also
provided by the top-level [lateral()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.lateral) function.

See also

[LATERAL correlation](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-lateral-correlation) -  overview of usage.

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)outerjoin(*right:_FromClauseArgument*, *onclause:_ColumnExpressionArgument[bool]|None=None*, *full:bool=False*) → [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)

*inherited from the* [FromClause.outerjoin()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.outerjoin) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return a [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) from this
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
to another `FromClause`, with the “isouter” flag set to
True.

E.g.:

```
from sqlalchemy import outerjoin

j = user_table.outerjoin(
    address_table, user_table.c.id == address_table.c.user_id
)
```

The above is equivalent to:

```
j = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id, isouter=True
)
```

   Parameters:

- **right** – the right side of the join; this is any
  [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause) object such as a
  [Table](#sqlalchemy.schema.Table) object, and
  may also be a selectable-compatible object such as an ORM-mapped
  class.
- **onclause** – a SQL expression representing the ON clause of the
  join.  If left at `None`, [FromClause.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join)
  will attempt to
  join the two tables based on a foreign key relationship.
- **full** – if True, render a FULL OUTER JOIN, instead of
  LEFT OUTER JOIN.

See also

[FromClause.join()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.join)

[Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join)

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Returns a copy of this ClauseElement with
[bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam)
elements replaced with values taken from the given dictionary:

```
>>> clause = column("x") + bindparam("foo")
>>> print(clause.compile().params)
{'foo':None}
>>> print(clause.params({"foo": 7}).compile().params)
{'foo':7}
```

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)primary_key

*inherited from the* [FromClause.primary_key](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.primary_key) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return the iterable collection of [Column](#sqlalchemy.schema.Column) objects
which comprise the primary key of this `_selectable.FromClause`.

For a [Table](#sqlalchemy.schema.Table) object, this collection is represented
by the [PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint) which itself is an
iterable collection of [Column](#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)replace_selectable(*old:FromClause*, *alias:Alias*) → Self

*inherited from the* [Selectable.replace_selectable()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.replace_selectable) *method of* [Selectable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable)

Replace all occurrences of [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)
‘old’ with the given [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
object, returning a copy of this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

Deprecated since version 1.4: The [Selectable.replace_selectable()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Selectable.replace_selectable) method is deprecated, and will be removed in a future release.  Similar functionality is available via the sqlalchemy.sql.visitors module.

     attribute [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)schema = None

*inherited from the* [FromClause.schema](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.schema) *attribute of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Define the ‘schema’ attribute for this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

This is typically `None` for most objects except that of
[Table](#sqlalchemy.schema.Table), where it is taken as the value of the
[Table.schema](#sqlalchemy.schema.Table.params.schema) argument.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)select() → [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)

*inherited from the* [FromClause.select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.select) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return a SELECT of this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

e.g.:

```
stmt = some_table.select().where(some_table.c.id == 5)
```

See also

[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) - general purpose
method which allows for arbitrary column lists.

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)self_group(*against:OperatorType|None=None*) → [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

*inherited from the* [ClauseElement.self_group()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.self_group) *method of* [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)

Apply a ‘grouping’ to this [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement).

This method is overridden by subclasses to return a “grouping”
construct, i.e. parenthesis.   In particular it’s used by “binary”
expressions to provide a grouping around themselves when placed into a
larger expression, as well as by [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)
constructs when placed into the FROM clause of another
[select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select).  (Note that subqueries should be
normally created using the [Select.alias()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.alias) method,
as many
platforms require nested SELECT statements to be named).

As expressions are composed together, the application of
[self_group()](#sqlalchemy.schema.Table.self_group) is automatic - end-user code should never
need to use this method directly.  Note that SQLAlchemy’s
clause constructs take operator precedence into account -
so parenthesis might not be needed, for example, in
an expression like `x OR (y AND z)` - AND takes precedence
over OR.

The base [self_group()](#sqlalchemy.schema.Table.self_group) method of
[ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
just returns self.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)table_valued() → TableValuedColumn[Any]

*inherited from the* `NamedFromClause.table_valued()` *method of* `NamedFromClause`

Return a `TableValuedColumn` object for this
[FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

A `TableValuedColumn` is a [ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement) that
represents a complete row in a table. Support for this construct is
backend dependent, and is supported in various forms by backends
such as PostgreSQL, Oracle Database and SQL Server.

E.g.:

```
>>> from sqlalchemy import select, column, func, table
>>> a = table("a", column("id"), column("x"), column("y"))
>>> stmt = select(func.row_to_json(a.table_valued()))
>>> print(stmt)
SELECT row_to_json(a) AS row_to_json_1
FROM a
```

Added in version 1.4.0b2.

See also

[Working with SQL Functions](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#tutorial-functions) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)tablesample(*sampling:float|Function[Any]*, *name:str|None=None*, *seed:roles.ExpressionElementRole[Any]|None=None*) → [TableSample](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableSample)

*inherited from the* [FromClause.tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause.tablesample) *method of* [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause)

Return a TABLESAMPLE alias of this [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause).

The return value is the [TableSample](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableSample)
construct also
provided by the top-level [tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.tablesample) function.

See also

[tablesample()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.tablesample) - usage guidelines and parameters

     method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)to_metadata(*metadata:MetaData*, *schema:str|Literal[SchemaConst.RETAIN_SCHEMA]=SchemaConst.RETAIN_SCHEMA*, *referred_schema_fn:Callable[[Table,str|None,ForeignKeyConstraint,str|None],str|None]|None=None*, *name:str|None=None*) → [Table](#sqlalchemy.schema.Table)

Return a copy of this [Table](#sqlalchemy.schema.Table) associated with a
different [MetaData](#sqlalchemy.schema.MetaData).

E.g.:

```
m1 = MetaData()

user = Table("user", m1, Column("id", Integer, primary_key=True))

m2 = MetaData()
user_copy = user.to_metadata(m2)
```

Changed in version 1.4: The [Table.to_metadata()](#sqlalchemy.schema.Table.to_metadata) function
was renamed from [Table.tometadata()](#sqlalchemy.schema.Table.tometadata).

   Parameters:

- **metadata** – Target [MetaData](#sqlalchemy.schema.MetaData) object,
  into which the
  new [Table](#sqlalchemy.schema.Table) object will be created.
- **schema** –
  optional string name indicating the target schema.
  Defaults to the special symbol [RETAIN_SCHEMA](#sqlalchemy.schema.SchemaConst.RETAIN_SCHEMA) which indicates
  that no change to the schema name should be made in the new
  [Table](#sqlalchemy.schema.Table).  If set to a string name, the new
  [Table](#sqlalchemy.schema.Table)
  will have this new name as the `.schema`.  If set to `None`, the
  schema will be set to that of the schema set on the target
  [MetaData](#sqlalchemy.schema.MetaData), which is typically `None` as well,
  unless
  set explicitly:
  ```
  m2 = MetaData(schema="newschema")
  # user_copy_one will have "newschema" as the schema name
  user_copy_one = user.to_metadata(m2, schema=None)
  m3 = MetaData()  # schema defaults to None
  # user_copy_two will have None as the schema name
  user_copy_two = user.to_metadata(m3, schema=None)
  ```
- **referred_schema_fn** –
  optional callable which can be supplied
  in order to provide for the schema name that should be assigned
  to the referenced table of a [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).
  The callable accepts this parent [Table](#sqlalchemy.schema.Table), the
  target schema that we are changing to, the
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object, and the existing
  “target schema” of that constraint.  The function should return the
  string schema name that should be applied.    To reset the schema
  to “none”, return the symbol `BLANK_SCHEMA`.  To effect no
  change, return `None` or `RETAIN_SCHEMA`.
  Changed in version 1.4.33: The `referred_schema_fn` function
  may return the `BLANK_SCHEMA` or `RETAIN_SCHEMA`
  symbols.
  E.g.:
  ```
  def referred_schema_fn(table, to_schema, constraint, referred_schema):
      if referred_schema == "base_tables":
          return referred_schema
      else:
          return to_schema
  new_table = table.to_metadata(
      m2, schema="alt_schema", referred_schema_fn=referred_schema_fn
  )
  ```
- **name** – optional string name indicating the target table name.
  If not specified or None, the table name is retained.  This allows
  a [Table](#sqlalchemy.schema.Table) to be copied to the same
  [MetaData](#sqlalchemy.schema.MetaData) target
  with a new name.

      method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)tometadata(*metadata:MetaData*, *schema:str|Literal[SchemaConst.RETAIN_SCHEMA]=SchemaConst.RETAIN_SCHEMA*, *referred_schema_fn:Callable[[Table,str|None,ForeignKeyConstraint,str|None],str|None]|None=None*, *name:str|None=None*) → [Table](#sqlalchemy.schema.Table)

Return a copy of this [Table](#sqlalchemy.schema.Table)
associated with a different
[MetaData](#sqlalchemy.schema.MetaData).

Deprecated since version 1.4: [Table.tometadata()](#sqlalchemy.schema.Table.tometadata) is renamed to [Table.to_metadata()](#sqlalchemy.schema.Table.to_metadata)

See [Table.to_metadata()](#sqlalchemy.schema.Table.to_metadata) for a full description.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)unique_params(**optionaldict:Any*, ***kwargs:Any*) → NoReturn

*inherited from the* `Immutable.unique_params()` *method of* `Immutable`

Return a copy with [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) elements
replaced.

Same functionality as [ClauseElement.params()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.params),
except adds unique=True
to affected bind parameters so that multiple statements can be
used.

    method [sqlalchemy.schema.Table.](#sqlalchemy.schema.Table)update() → [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)

*inherited from the* [TableClause.update()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause.update) *method of* [TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause)

Generate an [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) construct against this
[TableClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.TableClause).

E.g.:

```
table.update().where(table.c.id == 7).values(name="foo")
```

See [update()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.update) for argument and usage information.
