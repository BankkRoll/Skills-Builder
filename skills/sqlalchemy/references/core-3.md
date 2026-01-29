# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Defining Constraints and Indexes

This section will discuss SQL [constraints](https://docs.sqlalchemy.org/en/20/glossary.html#term-constraints) and indexes.  In SQLAlchemy
the key classes include [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) and [Index](#sqlalchemy.schema.Index).

## Defining Foreign Keys

A *foreign key* in SQL is a table-level construct that constrains one or more
columns in that table to only allow values that are present in a different set
of columns, typically but not always located on a different table. We call the
columns which are constrained the *foreign key* columns and the columns which
they are constrained towards the *referenced* columns. The referenced columns
almost always define the primary key for their owning table, though there are
exceptions to this. The foreign key is the “joint” that connects together
pairs of rows which have a relationship with each other, and SQLAlchemy
assigns very deep importance to this concept in virtually every area of its
operation.

In SQLAlchemy as well as in DDL, foreign key constraints can be defined as
additional attributes within the table clause, or for single-column foreign
keys they may optionally be specified within the definition of a single
column. The single column foreign key is more common, and at the column level
is specified by constructing a [ForeignKey](#sqlalchemy.schema.ForeignKey) object
as an argument to a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object:

```
user_preference = Table(
    "user_preference",
    metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)
```

Above, we define a new table `user_preference` for which each row must
contain a value in the `user_id` column that also exists in the `user`
table’s `user_id` column.

The argument to [ForeignKey](#sqlalchemy.schema.ForeignKey) is most commonly a
string of the form *<tablename>.<columnname>*, or for a table in a remote
schema or “owner” of the form *<schemaname>.<tablename>.<columnname>*. It may
also be an actual [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object, which as we’ll
see later is accessed from an existing [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object via its `c` collection:

```
ForeignKey(user.c.user_id)
```

The advantage to using a string is that the in-python linkage between `user`
and `user_preference` is resolved only when first needed, so that table
objects can be easily spread across multiple modules and defined in any order.

Foreign keys may also be defined at the table level, using the
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) object. This object can
describe a single- or multi-column foreign key. A multi-column foreign key is
known as a *composite* foreign key, and almost always references a table that
has a composite primary key. Below we define a table `invoice` which has a
composite primary key:

```
invoice = Table(
    "invoice",
    metadata_obj,
    Column("invoice_id", Integer, primary_key=True),
    Column("ref_num", Integer, primary_key=True),
    Column("description", String(60), nullable=False),
)
```

And then a table `invoice_item` with a composite foreign key referencing
`invoice`:

```
invoice_item = Table(
    "invoice_item",
    metadata_obj,
    Column("item_id", Integer, primary_key=True),
    Column("item_name", String(60), nullable=False),
    Column("invoice_id", Integer, nullable=False),
    Column("ref_num", Integer, nullable=False),
    ForeignKeyConstraint(
        ["invoice_id", "ref_num"], ["invoice.invoice_id", "invoice.ref_num"]
    ),
)
```

It’s important to note that the
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) is the only way to define a
composite foreign key. While we could also have placed individual
[ForeignKey](#sqlalchemy.schema.ForeignKey) objects on both the
`invoice_item.invoice_id` and `invoice_item.ref_num` columns, SQLAlchemy
would not be aware that these two values should be paired together - it would
be two individual foreign key constraints instead of a single composite
foreign key referencing two columns.

### Creating/Dropping Foreign Key Constraints via ALTER

The behavior we’ve seen in tutorials and elsewhere involving
foreign keys with DDL illustrates that the constraints are typically
rendered “inline” within the CREATE TABLE statement, such as:

```
CREATE TABLE addresses (
    id INTEGER NOT NULL,
    user_id INTEGER,
    email_address VARCHAR NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users (id)
)
```

The `CONSTRAINT .. FOREIGN KEY` directive is used to create the constraint
in an “inline” fashion within the CREATE TABLE definition.   The
[MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) and [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all) methods do
this by default, using a topological sort of all the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
involved such that tables are created and dropped in order of their foreign
key dependency (this sort is also available via the
[MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables) accessor).

This approach can’t work when two or more foreign key constraints are
involved in a “dependency cycle”, where a set of tables
are mutually dependent on each other, assuming the backend enforces foreign
keys (always the case except on SQLite, MySQL/MyISAM).   The methods will
therefore break out constraints in such a cycle into separate ALTER
statements, on all backends other than SQLite which does not support
most forms of ALTER.  Given a schema like:

```
node = Table(
    "node",
    metadata_obj,
    Column("node_id", Integer, primary_key=True),
    Column("primary_element", Integer, ForeignKey("element.element_id")),
)

element = Table(
    "element",
    metadata_obj,
    Column("element_id", Integer, primary_key=True),
    Column("parent_node_id", Integer),
    ForeignKeyConstraint(
        ["parent_node_id"], ["node.node_id"], name="fk_element_parent_node_id"
    ),
)
```

When we call upon [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) on a backend such as the
PostgreSQL backend, the cycle between these two tables is resolved and the
constraints are created separately:

```
>>> with engine.connect() as conn:
...     metadata_obj.create_all(conn, checkfirst=False)
CREATE TABLE element (
    element_id SERIAL NOT NULL,
    parent_node_id INTEGER,
    PRIMARY KEY (element_id)
)

CREATE TABLE node (
    node_id SERIAL NOT NULL,
    primary_element INTEGER,
    PRIMARY KEY (node_id)
)

ALTER TABLE element ADD CONSTRAINT fk_element_parent_node_id
    FOREIGN KEY(parent_node_id) REFERENCES node (node_id)
ALTER TABLE node ADD FOREIGN KEY(primary_element)
    REFERENCES element (element_id)
```

In order to emit DROP for these tables, the same logic applies, however
note here that in SQL, to emit DROP CONSTRAINT requires that the constraint
has a name.  In the case of the `'node'` table above, we haven’t named
this constraint; the system will therefore attempt to emit DROP for only
those constraints that are named:

```
>>> with engine.connect() as conn:
...     metadata_obj.drop_all(conn, checkfirst=False)
ALTER TABLE element DROP CONSTRAINT fk_element_parent_node_id
DROP TABLE node
DROP TABLE element
```

In the case where the cycle cannot be resolved, such as if we hadn’t applied
a name to either constraint here, we will receive the following error:

```
sqlalchemy.exc.CircularDependencyError: Can't sort tables for DROP;
an unresolvable foreign key dependency exists between tables:
element, node.  Please ensure that the ForeignKey and ForeignKeyConstraint
objects involved in the cycle have names so that they can be dropped
using DROP CONSTRAINT.
```

This error only applies to the DROP case as we can emit “ADD CONSTRAINT”
in the CREATE case without a name; the database typically assigns one
automatically.

The [ForeignKeyConstraint.use_alter](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) and
[ForeignKey.use_alter](#sqlalchemy.schema.ForeignKey.params.use_alter) keyword arguments can be used
to manually resolve dependency cycles.  We can add this flag only to
the `'element'` table as follows:

```
element = Table(
    "element",
    metadata_obj,
    Column("element_id", Integer, primary_key=True),
    Column("parent_node_id", Integer),
    ForeignKeyConstraint(
        ["parent_node_id"],
        ["node.node_id"],
        use_alter=True,
        name="fk_element_parent_node_id",
    ),
)
```

in our CREATE DDL we will see the ALTER statement only for this constraint,
and not the other one:

```
>>> with engine.connect() as conn:
...     metadata_obj.create_all(conn, checkfirst=False)
CREATE TABLE element (
    element_id SERIAL NOT NULL,
    parent_node_id INTEGER,
    PRIMARY KEY (element_id)
)

CREATE TABLE node (
    node_id SERIAL NOT NULL,
    primary_element INTEGER,
    PRIMARY KEY (node_id),
    FOREIGN KEY(primary_element) REFERENCES element (element_id)
)

ALTER TABLE element ADD CONSTRAINT fk_element_parent_node_id
FOREIGN KEY(parent_node_id) REFERENCES node (node_id)
```

[ForeignKeyConstraint.use_alter](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) and
[ForeignKey.use_alter](#sqlalchemy.schema.ForeignKey.params.use_alter), when used in conjunction with a drop
operation, will require that the constraint is named, else an error
like the following is generated:

```
sqlalchemy.exc.CompileError: Can't emit DROP CONSTRAINT for constraint
ForeignKeyConstraint(...); it has no name
```

See also

[Configuring Constraint Naming Conventions](#constraint-naming-conventions)

[sort_tables_and_constraints()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables_and_constraints)

### ON UPDATE and ON DELETE

Most databases support *cascading* of foreign key values, that is the when a
parent row is updated the new value is placed in child rows, or when the
parent row is deleted all corresponding child rows are set to null or deleted.
In data definition language these are specified using phrases like “ON UPDATE
CASCADE”, “ON DELETE CASCADE”, and “ON DELETE SET NULL”, corresponding to
foreign key constraints. The phrase after “ON UPDATE” or “ON DELETE” may also
allow other phrases that are specific to the database in use. The
[ForeignKey](#sqlalchemy.schema.ForeignKey) and
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) objects support the
generation of this clause via the `onupdate` and `ondelete` keyword
arguments. The value is any string which will be output after the appropriate
“ON UPDATE” or “ON DELETE” phrase:

```
child = Table(
    "child",
    metadata_obj,
    Column(
        "id",
        Integer,
        ForeignKey("parent.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)

composite = Table(
    "composite",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("rev_id", Integer),
    Column("note_id", Integer),
    ForeignKeyConstraint(
        ["rev_id", "note_id"],
        ["revisions.id", "revisions.note_id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    ),
)
```

Note that some backends have special requirements for cascades to function:

- MySQL / MariaDB - the `InnoDB` storage engine should be used (this is
  typically the default in modern databases)
- SQLite - constraints are not enabled by default.
  See [Foreign Key Support](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-foreign-keys)

See also

For background on integration of `ON DELETE CASCADE` with
ORM [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs, see the following sections:

[Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes)

[Using foreign key ON DELETE with many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes-many-to-many)

[PostgreSQL Constraint Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-constraint-options) - indicates additional options
available for foreign key cascades such as column lists

[Foreign Key Support](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-foreign-keys) - background on enabling foreign key support
with SQLite

## UNIQUE Constraint

Unique constraints can be created anonymously on a single column using the
`unique` keyword on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column). Explicitly named
unique constraints and/or those with multiple columns are created via the
[UniqueConstraint](#sqlalchemy.schema.UniqueConstraint) table-level construct.

```
from sqlalchemy import UniqueConstraint

metadata_obj = MetaData()
mytable = Table(
    "mytable",
    metadata_obj,
    # per-column anonymous unique constraint
    Column("col1", Integer, unique=True),
    Column("col2", Integer),
    Column("col3", Integer),
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint("col2", "col3", name="uix_1"),
)
```

## CHECK Constraint

Check constraints can be named or unnamed and can be created at the Column or
Table level, using the [CheckConstraint](#sqlalchemy.schema.CheckConstraint) construct.
The text of the check constraint is passed directly through to the database,
so there is limited “database independent” behavior. Column level check
constraints generally should only refer to the column to which they are
placed, while table level constraints can refer to any columns in the table.

Note that some databases do not actively support check constraints such as
older versions of MySQL (prior to 8.0.16).

```
from sqlalchemy import CheckConstraint

metadata_obj = MetaData()
mytable = Table(
    "mytable",
    metadata_obj,
    # per-column CHECK constraint
    Column("col1", Integer, CheckConstraint("col1>5")),
    Column("col2", Integer),
    Column("col3", Integer),
    # table level CHECK constraint.  'name' is optional.
    CheckConstraint("col2 > col3 + 5", name="check1"),
)

mytable.create(engine)
CREATE TABLE mytable (
    col1 INTEGER  CHECK (col1>5),
    col2 INTEGER,
    col3 INTEGER,
    CONSTRAINT check1  CHECK (col2 > col3 + 5)
)
```

## PRIMARY KEY Constraint

The primary key constraint of any [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object is implicitly
present, based on the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that are marked with the
[Column.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.primary_key) flag.   The [PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint)
object provides explicit access to this constraint, which includes the
option of being configured directly:

```
from sqlalchemy import PrimaryKeyConstraint

my_table = Table(
    "mytable",
    metadata_obj,
    Column("id", Integer),
    Column("version_id", Integer),
    Column("data", String(50)),
    PrimaryKeyConstraint("id", "version_id", name="mytable_pk"),
)
```

See also

[PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint) - detailed API documentation.

## Setting up Constraints when using the Declarative ORM Extension

The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is the SQLAlchemy Core construct that allows one to define
table metadata, which among other things can be used by the SQLAlchemy ORM
as a target to map a class.  The [Declarative](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html)
extension allows the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object to be created automatically, given
the contents of the table primarily as a mapping of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

To apply table-level constraint objects such as [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint)
to a table defined using Declarative, use the `__table_args__` attribute,
described at [Table Configuration](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/table_config.html#declarative-table-args).

## Configuring Constraint Naming Conventions

Relational databases typically assign explicit names to all constraints and
indexes.  In the common case that a table is created using `CREATE TABLE`
where constraints such as CHECK, UNIQUE, and PRIMARY KEY constraints are
produced inline with the table definition, the database usually has a system
in place in which names are automatically assigned to these constraints, if
a name is not otherwise specified.  When an existing database table is altered
in a database using a command such as `ALTER TABLE`, this command typically
needs to specify explicit names for new constraints as well as be able to
specify the name of an existing constraint that is to be dropped or modified.

Constraints can be named explicitly using the [Constraint.name](#sqlalchemy.schema.Constraint.params.name) parameter,
and for indexes the [Index.name](#sqlalchemy.schema.Index.params.name) parameter.  However, in the
case of constraints this parameter is optional.  There are also the use
cases of using the [Column.unique](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.unique) and [Column.index](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.index)
parameters which create [UniqueConstraint](#sqlalchemy.schema.UniqueConstraint) and [Index](#sqlalchemy.schema.Index) objects
without an explicit name being specified.

The use case of alteration of existing tables and constraints can be handled
by schema migration tools such as [Alembic](https://alembic.sqlalchemy.org/).
However, neither Alembic nor SQLAlchemy currently create names for constraint
objects where the name is otherwise unspecified, leading to the case where
being able to alter existing constraints means that one must reverse-engineer
the naming system used by the relational database to auto-assign names,
or that care must be taken to ensure that all constraints are named.

In contrast to having to assign explicit names to all [Constraint](#sqlalchemy.schema.Constraint)
and [Index](#sqlalchemy.schema.Index) objects, automated naming schemes can be constructed
using events.  This approach has the advantage that constraints will get
a consistent naming scheme without the need for explicit name parameters
throughout the code, and also that the convention takes place just as well
for those constraints and indexes produced by the [Column.unique](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.unique)
and [Column.index](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.index) parameters.  As of SQLAlchemy 0.9.2 this
event-based approach is included, and can be configured using the argument
[MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention).

### Configuring a Naming Convention for a MetaData Collection

[MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) refers to a dictionary which accepts
the [Index](#sqlalchemy.schema.Index) class or individual [Constraint](#sqlalchemy.schema.Constraint) classes as keys,
and Python string templates as values.   It also accepts a series of
string-codes as alternative keys, `"fk"`, `"pk"`,
`"ix"`, `"ck"`, `"uq"` for foreign key, primary key, index,
check, and unique constraint, respectively.  The string templates in this
dictionary are used whenever a constraint or index is associated with this
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object that does not have an existing name given (including
one exception case where an existing name can be further embellished).

An example naming convention that suits basic cases is as follows:

```
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(naming_convention=convention)
```

The above convention will establish names for all constraints within
the target [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection.
For example, we can observe the name produced when we create an unnamed
[UniqueConstraint](#sqlalchemy.schema.UniqueConstraint):

```
>>> user_table = Table(
...     "user",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30), nullable=False),
...     UniqueConstraint("name"),
... )
>>> list(user_table.constraints)[1].name
'uq_user_name'
```

This same feature takes effect even if we just use the [Column.unique](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.unique)
flag:

```
>>> user_table = Table(
...     "user",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("name", String(30), nullable=False, unique=True),
... )
>>> list(user_table.constraints)[1].name
'uq_user_name'
```

A key advantage to the naming convention approach is that the names are established
at Python construction time, rather than at DDL emit time.  The effect this has
when using Alembic’s `--autogenerate` feature is that the naming convention
will be explicit when a new migration script is generated:

```
def upgrade():
    op.create_unique_constraint("uq_user_name", "user", ["name"])
```

The above `"uq_user_name"` string was copied from the [UniqueConstraint](#sqlalchemy.schema.UniqueConstraint)
object that `--autogenerate` located in our metadata.

The tokens available include `%(table_name)s`, `%(referred_table_name)s`,
`%(column_0_name)s`, `%(column_0_label)s`, `%(column_0_key)s`,
`%(referred_column_0_name)s`, and  `%(constraint_name)s`, as well as
multiple-column versions of each including `%(column_0N_name)s`,
`%(column_0_N_name)s`,  `%(referred_column_0_N_name)s` which render all
column names separated with or without an underscore.  The documentation for
[MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) has further detail on each  of these
conventions.

### The Default Naming Convention

The default value for [MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) handles
the long-standing SQLAlchemy behavior of assigning a name to a [Index](#sqlalchemy.schema.Index)
object that is created using the [Column.index](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.index) parameter:

```
>>> from sqlalchemy.sql.schema import DEFAULT_NAMING_CONVENTION
>>> DEFAULT_NAMING_CONVENTION
immutabledict({'ix': 'ix_%(column_0_label)s'})
```

### Truncation of Long Names

When a generated name, particularly those that use the multiple-column tokens,
is too long for the identifier length limit of the target database
(for example, PostgreSQL has a limit of 63 characters), the name will be
deterministically truncated using a 4-character suffix based on the md5
hash of the long name.  For example, the naming convention below will
generate very long names given the column names in use:

```
metadata_obj = MetaData(
    naming_convention={"uq": "uq_%(table_name)s_%(column_0_N_name)s"}
)

long_names = Table(
    "long_names",
    metadata_obj,
    Column("information_channel_code", Integer, key="a"),
    Column("billing_convention_name", Integer, key="b"),
    Column("product_identifier", Integer, key="c"),
    UniqueConstraint("a", "b", "c"),
)
```

On the PostgreSQL dialect, names longer than 63 characters will be truncated
as in the following example:

```
CREATE TABLE long_names (
    information_channel_code INTEGER,
    billing_convention_name INTEGER,
    product_identifier INTEGER,
    CONSTRAINT uq_long_names_information_channel_code_billing_conventi_a79e
    UNIQUE (information_channel_code, billing_convention_name, product_identifier)
)
```

The above suffix `a79e` is based on the md5 hash of the long name and will
generate the same value every time to produce consistent names for a given
schema.

### Creating Custom Tokens for Naming Conventions

New tokens can also be added, by specifying an additional token
and a callable within the naming_convention dictionary.  For example, if we
wanted to name our foreign key constraints using a GUID scheme, we could do
that as follows:

```
import uuid

def fk_guid(constraint, table):
    str_tokens = (
        [
            table.name,
        ]
        + [element.parent.name for element in constraint.elements]
        + [element.target_fullname for element in constraint.elements]
    )
    guid = uuid.uuid5(uuid.NAMESPACE_OID, "_".join(str_tokens).encode("ascii"))
    return str(guid)

convention = {
    "fk_guid": fk_guid,
    "ix": "ix_%(column_0_label)s",
    "fk": "fk_%(fk_guid)s",
}
```

Above, when we create a new [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint), we will get a
name as follows:

```
>>> metadata_obj = MetaData(naming_convention=convention)

>>> user_table = Table(
...     "user",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("version", Integer, primary_key=True),
...     Column("data", String(30)),
... )
>>> address_table = Table(
...     "address",
...     metadata_obj,
...     Column("id", Integer, primary_key=True),
...     Column("user_id", Integer),
...     Column("user_version_id", Integer),
... )
>>> fk = ForeignKeyConstraint(["user_id", "user_version_id"], ["user.id", "user.version"])
>>> address_table.append_constraint(fk)
>>> fk.name
fk_0cd51ab5-8d70-56e8-a83c-86661737766d
```

See also

[MetaData.naming_convention](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.naming_convention) - for additional usage details
as well as a listing of all available naming components.

[The Importance of Naming Constraints](https://alembic.sqlalchemy.org/en/latest/naming.html) - in the Alembic documentation.

Added in version 1.3.0: added multi-column naming tokens such as `%(column_0_N_name)s`.
Generated names that go beyond the character limit for the target database will be
deterministically truncated.

### Naming CHECK Constraints

The [CheckConstraint](#sqlalchemy.schema.CheckConstraint) object is configured against an arbitrary
SQL expression, which can have any number of columns present, and additionally
is often configured using a raw SQL string.  Therefore a common convention
to use with [CheckConstraint](#sqlalchemy.schema.CheckConstraint) is one where we expect the object
to have a name already, and we then enhance it with other convention elements.
A typical convention is `"ck_%(table_name)s_%(constraint_name)s"`:

```
metadata_obj = MetaData(
    naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
)

Table(
    "foo",
    metadata_obj,
    Column("value", Integer),
    CheckConstraint("value > 5", name="value_gt_5"),
)
```

The above table will produce the name `ck_foo_value_gt_5`:

```
CREATE TABLE foo (
    value INTEGER,
    CONSTRAINT ck_foo_value_gt_5 CHECK (value > 5)
)
```

[CheckConstraint](#sqlalchemy.schema.CheckConstraint) also supports the `%(columns_0_name)s`
token; we can make use of this by ensuring we use a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or
[column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) element within the constraint’s expression,
either by declaring the constraint separate from the table:

```
metadata_obj = MetaData(naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"})

foo = Table("foo", metadata_obj, Column("value", Integer))

CheckConstraint(foo.c.value > 5)
```

or by using a [column()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.column) inline:

```
from sqlalchemy import column

metadata_obj = MetaData(naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"})

foo = Table(
    "foo", metadata_obj, Column("value", Integer), CheckConstraint(column("value") > 5)
)
```

Both will produce the name `ck_foo_value`:

```
CREATE TABLE foo (
    value INTEGER,
    CONSTRAINT ck_foo_value CHECK (value > 5)
)
```

The determination of the name of “column zero” is performed by scanning
the given expression for column objects.  If the expression has more than
one column present, the scan does use a deterministic search, however the
structure of the expression will determine which column is noted as
“column zero”.

### Configuring Naming for Boolean, Enum, and other schema types

The [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) class refers to type objects such as [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
and [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) which generate a CHECK constraint accompanying the type.
The name for the constraint here is most directly set up by sending
the “name” parameter, e.g. [Boolean.name](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean.params.name):

```
Table("foo", metadata_obj, Column("flag", Boolean(name="ck_foo_flag")))
```

The naming convention feature may be combined with these types as well,
normally by using a convention which includes `%(constraint_name)s`
and then applying a name to the type:

```
metadata_obj = MetaData(
    naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
)

Table("foo", metadata_obj, Column("flag", Boolean(name="flag_bool")))
```

The above table will produce the constraint name `ck_foo_flag_bool`:

```
CREATE TABLE foo (
    flag BOOL,
    CONSTRAINT ck_foo_flag_bool CHECK (flag IN (0, 1))
)
```

The [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) classes use special internal symbols so that
the naming convention is only determined at DDL compile time.  On PostgreSQL,
there’s a native BOOLEAN type, so the CHECK constraint of [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean)
is not needed; we are safe to set up a [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) type without a
name, even though a naming convention is in place for check constraints.
This convention will only be consulted for the CHECK constraint if we
run against a database without a native BOOLEAN type like SQLite or
MySQL.

The CHECK constraint may also make use of the `column_0_name` token,
which works nicely with [SchemaType](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.SchemaType) since these constraints have
only one column:

```
metadata_obj = MetaData(naming_convention={"ck": "ck_%(table_name)s_%(column_0_name)s"})

Table("foo", metadata_obj, Column("flag", Boolean()))
```

The above schema will produce:

```
CREATE TABLE foo (
    flag BOOL,
    CONSTRAINT ck_foo_flag CHECK (flag IN (0, 1))
)
```

### Using Naming Conventions with ORM Declarative Mixins

When using the naming convention feature with [ORM Declarative Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html), individual constraint objects must exist for each
actual table-mapped subclass.  See the section
[Creating Indexes and Constraints with Naming Conventions on Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#orm-mixins-named-constraints) for background and examples.

## Constraints API

| Object Name | Description |
| --- | --- |
| CheckConstraint | A table- or column-level CHECK constraint. |
| ColumnCollectionConstraint | A constraint that proxies a ColumnCollection. |
| ColumnCollectionMixin | AColumnCollectionofColumnobjects. |
| Constraint | A table-level SQL constraint. |
| conv | Mark a string indicating that a name has already been converted
by a naming convention. |
| ForeignKey | Defines a dependency between two columns. |
| ForeignKeyConstraint | A table-level FOREIGN KEY constraint. |
| HasConditionalDDL | define a class that includes theHasConditionalDDL.ddl_if()method, allowing for conditional rendering of DDL. |
| PrimaryKeyConstraint | A table-level PRIMARY KEY constraint. |
| UniqueConstraint | A table-level UNIQUE constraint. |

   class sqlalchemy.schema.Constraint

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.schema.HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL), [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

A table-level SQL constraint.

[Constraint](#sqlalchemy.schema.Constraint) serves as the base class for the series of
constraint objects that can be associated with [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects, including [PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint),
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) [UniqueConstraint](#sqlalchemy.schema.UniqueConstraint), and
[CheckConstraint](#sqlalchemy.schema.CheckConstraint).

| Member Name | Description |
| --- | --- |
| __init__() | Create a SQL constraint. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)__init__(*name:_ConstraintNameArgument=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *info:_InfoType|None=None*, *comment:str|None=None*, *_create_rule:Any|None=None*, *_type_bound:bool=False*, ***dialect_kw:Any*) → None

Create a SQL constraint.

  Parameters:

- **name** – Optional, the in-database name of this `Constraint`.
- **deferrable** – Optional bool.  If set, emit DEFERRABLE or NOT DEFERRABLE when
  issuing DDL for this constraint.
- **initially** – Optional string.  If set, emit INITIALLY <value> when issuing DDL
  for this constraint.
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **comment** –
  Optional string that will render an SQL comment on
  foreign key constraint creation.
  > Added in version 2.0.
- ****dialect_kw** – Additional keyword arguments are dialect
  specific, and passed in the form `<dialectname>_<argname>`.  See
  the documentation regarding an individual dialect at
  [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on documented arguments.
- **_create_rule** – used internally by some datatypes that also create constraints.
- **_type_bound** – used internally to indicate that this constraint is associated with
  a specific datatype.

      classmethod [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      method [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)copy(***kw:Any*) → Self

Deprecated since version 1.4: The [Constraint.copy()](#sqlalchemy.schema.Constraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)dialect_options

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

     attribute [sqlalchemy.schema.Constraint.](#sqlalchemy.schema.Constraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     class sqlalchemy.schema.ColumnCollectionMixin

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects.

This collection represents the columns which are referred to by
this object.

    class sqlalchemy.schema.ColumnCollectionConstraint

*inherits from* [sqlalchemy.schema.ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin), [sqlalchemy.schema.Constraint](#sqlalchemy.schema.Constraint)

A constraint that proxies a ColumnCollection.

| Member Name | Description |
| --- | --- |
| __init__() |  |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| columns | AColumnCollectionrepresenting the set of columns
for this constraint. |
| contains_column() | Return True if this constraint contains the given column. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)__init__(**columns:_DDLColumnArgument*, *name:_ConstraintNameArgument=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *info:_InfoType|None=None*, *_autoattach:bool=True*, *_column_flag:bool=False*, *_gather_expressions:List[_DDLColumnArgument]|None=None*, ***dialect_kw:Any*) → None  Parameters:

- ***columns** – A sequence of column names or Column objects.
- **name** – Optional, the in-database name of this constraint.
- **deferrable** – Optional bool.  If set, emit DEFERRABLE or NOT DEFERRABLE when
  issuing DDL for this constraint.
- **initially** – Optional string.  If set, emit INITIALLY <value> when issuing DDL
  for this constraint.
- ****dialect_kw** – other keyword arguments including
  dialect-specific arguments are propagated to the [Constraint](#sqlalchemy.schema.Constraint)
  superclass.

      classmethod [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      attribute [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)columns: ReadOnlyColumnCollection[str, [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]]

*inherited from the* `ColumnCollectionMixin.columns` *attribute of* [ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) representing the set of columns
for this constraint.

    method [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)contains_column(*col:Column[Any]*) → bool

Return True if this constraint contains the given column.

Note that this object also contains an attribute `.columns`
which is a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)copy(***, *target_table:Table|None=None*, ***kw:Any*) → [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Deprecated since version 1.4: The [ColumnCollectionConstraint.copy()](#sqlalchemy.schema.ColumnCollectionConstraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)dialect_options

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

     attribute [sqlalchemy.schema.ColumnCollectionConstraint.](#sqlalchemy.schema.ColumnCollectionConstraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     class sqlalchemy.schema.CheckConstraint

*inherits from* [sqlalchemy.schema.ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

A table- or column-level CHECK constraint.

Can be included in the definition of a Table or Column.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a CHECK constraint. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| columns | AColumnCollectionrepresenting the set of columns
for this constraint. |
| contains_column() | Return True if this constraint contains the given column. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)__init__(*sqltext:_TextCoercedExpressionArgument[Any]*, *name:_ConstraintNameArgument=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *table:Table|None=None*, *info:_InfoType|None=None*, *_create_rule:Any|None=None*, *_autoattach:bool=True*, *_type_bound:bool=False*, ***dialect_kw:Any*) → None

Construct a CHECK constraint.

  Parameters:

- **sqltext** –
  A string containing the constraint definition, which will be used
  verbatim, or a SQL expression construct.   If given as a string,
  the object is converted to a [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) object.
  If the textual
  string includes a colon character, escape this using a backslash:
  ```
  CheckConstraint(r"foo ~ E'a(?\:b|c)d")
  ```
- **name** – Optional, the in-database name of the constraint.
- **deferrable** – Optional bool.  If set, emit DEFERRABLE or NOT DEFERRABLE when
  issuing DDL for this constraint.
- **initially** – Optional string.  If set, emit INITIALLY <value> when issuing DDL
  for this constraint.
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) attribute of this object.

      classmethod [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      attribute [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)columns

*inherited from the* `ColumnCollectionMixin.columns` *attribute of* [ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) representing the set of columns
for this constraint.

    method [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)contains_column(*col:Column[Any]*) → bool

*inherited from the* [ColumnCollectionConstraint.contains_column()](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Return True if this constraint contains the given column.

Note that this object also contains an attribute `.columns`
which is a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)copy(***, *target_table:Table|None=None*, ***kw:Any*) → [CheckConstraint](#sqlalchemy.schema.CheckConstraint)

Deprecated since version 1.4: The [CheckConstraint.copy()](#sqlalchemy.schema.CheckConstraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)dialect_options

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

     attribute [sqlalchemy.schema.CheckConstraint.](#sqlalchemy.schema.CheckConstraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     class sqlalchemy.schema.ForeignKey

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Defines a dependency between two columns.

`ForeignKey` is specified as an argument to a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object,
e.g.:

```
t = Table(
    "remote_table",
    metadata,
    Column("remote_id", ForeignKey("main_table.id")),
)
```

Note that `ForeignKey` is only a marker object that defines
a dependency between two columns.   The actual constraint
is in all cases represented by the [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint)
object.   This object will be generated automatically when
a `ForeignKey` is associated with a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) which
in turn is associated with a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).   Conversely,
when [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) is applied to a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
`ForeignKey` markers are automatically generated to be
present on each associated [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), which are also
associated with the constraint object.

Note that you cannot define a “composite” foreign key constraint,
that is a constraint between a grouping of multiple parent/child
columns, using `ForeignKey` objects.   To define this grouping,
the [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) object must be used, and applied
to the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).   The associated `ForeignKey` objects
are created automatically.

The `ForeignKey` objects associated with an individual
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
object are available in the foreign_keys collection
of that column.

Further examples of foreign key configuration are in
[Defining Foreign Keys](#metadata-foreignkeys).

| Member Name | Description |
| --- | --- |
| __init__() | Construct a column-level FOREIGN KEY. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| column | Return the targetColumnreferenced by thisForeignKey. |
| copy() |  |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| get_referent() | Return theColumnin the givenTable(or anyFromClause)
referenced by thisForeignKey. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |
| references() | Return True if the givenTableis referenced by thisForeignKey. |

   method [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)__init__(*column:_DDLColumnArgument*, *_constraint:ForeignKeyConstraint|None=None*, *use_alter:bool=False*, *name:_ConstraintNameArgument=None*, *onupdate:str|None=None*, *ondelete:str|None=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *link_to_name:bool=False*, *match:str|None=None*, *info:_InfoType|None=None*, *comment:str|None=None*, *_unresolvable:bool=False*, ***dialect_kw:Any*)

Construct a column-level FOREIGN KEY.

The [ForeignKey](#sqlalchemy.schema.ForeignKey) object when constructed generates a
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint)
which is associated with the parent
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object’s collection of constraints.

  Parameters:

- **column** – A single target column for the key relationship. A
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object or a column name as a string:
  `tablename.columnkey` or `schema.tablename.columnkey`.
  `columnkey` is the `key` which has been assigned to the column
  (defaults to the column name itself), unless `link_to_name` is
  `True` in which case the rendered name of the column is used.
- **name** – Optional string. An in-database name for the key if
  constraint is not provided.
- **onupdate** –
  Optional string. If set, emit ON UPDATE <value> when
  issuing DDL for this constraint. Typical values include CASCADE,
  DELETE and RESTRICT.
  See also
  [ON UPDATE and ON DELETE](#on-update-on-delete)
- **ondelete** –
  Optional string. If set, emit ON DELETE <value> when
  issuing DDL for this constraint. Typical values include CASCADE,
  SET NULL and RESTRICT.  Some dialects may allow for additional
  syntaxes.
  See also
  [ON UPDATE and ON DELETE](#on-update-on-delete)
- **deferrable** – Optional bool. If set, emit DEFERRABLE or NOT
  DEFERRABLE when issuing DDL for this constraint.
- **initially** – Optional string. If set, emit INITIALLY <value> when
  issuing DDL for this constraint.
- **link_to_name** – if True, the string name given in `column` is
  the rendered name of the referenced column, not its locally
  assigned `key`.
- **use_alter** –
  passed to the underlying
  [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint)
  to indicate the constraint should
  be generated/dropped externally from the CREATE TABLE/ DROP TABLE
  statement.  See [ForeignKeyConstraint.use_alter](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter)
  for further description.
  See also
  [ForeignKeyConstraint.use_alter](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter)
  [Creating/Dropping Foreign Key Constraints via ALTER](#use-alter)
- **match** – Optional string. If set, emit MATCH <value> when issuing
  DDL for this constraint. Typical values include SIMPLE, PARTIAL
  and FULL.
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **comment** –
  Optional string that will render an SQL comment on
  foreign key constraint creation.
  > Added in version 2.0.
- ****dialect_kw** – Additional keyword arguments are dialect
  specific, and passed in the form `<dialectname>_<argname>`.  The
  arguments are ultimately handled by a corresponding
  [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint).
  See the documentation regarding
  an individual dialect at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on
  documented arguments.

      classmethod [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      attribute [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)column

Return the target [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) referenced by this
[ForeignKey](#sqlalchemy.schema.ForeignKey).

If no target column has been established, an exception
is raised.

    method [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)copy(***, *schema:str|None=None*, ***kw:Any*) → [ForeignKey](#sqlalchemy.schema.ForeignKey)

Deprecated since version 1.4: The [ForeignKey.copy()](#sqlalchemy.schema.ForeignKey.copy) method is deprecated and will be removed in a future release.

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

     attribute [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)dialect_options

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

     method [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)get_referent(*table:FromClause*) → [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any] | None

Return the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) in the given
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) (or any [FromClause](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.FromClause))
referenced by this [ForeignKey](#sqlalchemy.schema.ForeignKey).

Returns None if this [ForeignKey](#sqlalchemy.schema.ForeignKey)
does not reference the given
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).

    attribute [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    method [sqlalchemy.schema.ForeignKey.](#sqlalchemy.schema.ForeignKey)references(*table:Table*) → bool

Return True if the given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
is referenced by this
[ForeignKey](#sqlalchemy.schema.ForeignKey).

    property target_fullname: str

Return a string based ‘column specification’ for this
[ForeignKey](#sqlalchemy.schema.ForeignKey).

This is usually the equivalent of the string-based “tablename.colname”
argument first passed to the object’s constructor.

     class sqlalchemy.schema.ForeignKeyConstraint

*inherits from* [sqlalchemy.schema.ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

A table-level FOREIGN KEY constraint.

Defines a single column or composite FOREIGN KEY … REFERENCES
constraint. For a no-frills, single column foreign key, adding a
[ForeignKey](#sqlalchemy.schema.ForeignKey) to the definition of a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
is a
shorthand equivalent for an unnamed, single column
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint).

Examples of foreign key configuration are in [Defining Foreign Keys](#metadata-foreignkeys).

| Member Name | Description |
| --- | --- |
| __init__() | Construct a composite-capable FOREIGN KEY. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| columns | AColumnCollectionrepresenting the set of columns
for this constraint. |
| contains_column() | Return True if this constraint contains the given column. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| elements | A sequence ofForeignKeyobjects. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)__init__(*columns:_typing_Sequence[_DDLColumnArgument]*, *refcolumns:_typing_Sequence[_DDLColumnArgument]*, *name:_ConstraintNameArgument=None*, *onupdate:str|None=None*, *ondelete:str|None=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *use_alter:bool=False*, *link_to_name:bool=False*, *match:str|None=None*, *table:Table|None=None*, *info:_InfoType|None=None*, *comment:str|None=None*, ***dialect_kw:Any*) → None

Construct a composite-capable FOREIGN KEY.

  Parameters:

- **columns** – A sequence of local column names. The named columns
  must be defined and present in the parent Table. The names should
  match the `key` given to each column (defaults to the name) unless
  `link_to_name` is True.
- **refcolumns** – A sequence of foreign column names or Column
  objects. The columns must all be located within the same Table.
- **name** – Optional, the in-database name of the key.
- **onupdate** –
  Optional string. If set, emit ON UPDATE <value> when
  issuing DDL for this constraint. Typical values include CASCADE,
  DELETE and RESTRICT.
  See also
  [ON UPDATE and ON DELETE](#on-update-on-delete)
- **ondelete** –
  Optional string. If set, emit ON DELETE <value> when
  issuing DDL for this constraint. Typical values include CASCADE,
  SET NULL and RESTRICT.  Some dialects may allow for additional
  syntaxes.
  See also
  [ON UPDATE and ON DELETE](#on-update-on-delete)
- **deferrable** – Optional bool. If set, emit DEFERRABLE or NOT
  DEFERRABLE when issuing DDL for this constraint.
- **initially** – Optional string. If set, emit INITIALLY <value> when
  issuing DDL for this constraint.
- **link_to_name** – if True, the string name given in `column` is
  the rendered name of the referenced column, not its locally assigned
  `key`.
- **use_alter** –
  If True, do not emit the DDL for this constraint as
  part of the CREATE TABLE definition. Instead, generate it via an
  ALTER TABLE statement issued after the full collection of tables
  have been created, and drop it via an ALTER TABLE statement before
  the full collection of tables are dropped.
  The use of [ForeignKeyConstraint.use_alter](#sqlalchemy.schema.ForeignKeyConstraint.params.use_alter) is
  particularly geared towards the case where two or more tables
  are established within a mutually-dependent foreign key constraint
  relationship; however, the [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all) and
  [MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all)
  methods will perform this resolution
  automatically, so the flag is normally not needed.
  See also
  [Creating/Dropping Foreign Key Constraints via ALTER](#use-alter)
- **match** – Optional string. If set, emit MATCH <value> when issuing
  DDL for this constraint. Typical values include SIMPLE, PARTIAL
  and FULL.
- **info** – Optional data dictionary which will be populated into the
  [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- **comment** –
  Optional string that will render an SQL comment on
  foreign key constraint creation.
  > Added in version 2.0.
- ****dialect_kw** – Additional keyword arguments are dialect
  specific, and passed in the form `<dialectname>_<argname>`.  See
  the documentation regarding an individual dialect at
  [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on documented arguments.

      classmethod [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      property column_keys: Sequence[str]

Return a list of string keys representing the local
columns in this [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint).

This list is either the original string arguments sent
to the constructor of the [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint),
or if the constraint has been initialized with [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects, is the string `.key` of each element.

    attribute [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)columns: ReadOnlyColumnCollection[str, [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]]

*inherited from the* `ColumnCollectionMixin.columns` *attribute of* [ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) representing the set of columns
for this constraint.

    method [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)contains_column(*col:Column[Any]*) → bool

*inherited from the* [ColumnCollectionConstraint.contains_column()](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Return True if this constraint contains the given column.

Note that this object also contains an attribute `.columns`
which is a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)copy(***, *schema:str|None=None*, *target_table:Table|None=None*, ***kw:Any*) → [ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint)

Deprecated since version 1.4: The [ForeignKeyConstraint.copy()](#sqlalchemy.schema.ForeignKeyConstraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)dialect_options

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

     attribute [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)elements: List[[ForeignKey](#sqlalchemy.schema.ForeignKey)]

A sequence of [ForeignKey](#sqlalchemy.schema.ForeignKey) objects.

Each [ForeignKey](#sqlalchemy.schema.ForeignKey)
represents a single referring column/referred
column pair.

This collection is intended to be read-only.

    attribute [sqlalchemy.schema.ForeignKeyConstraint.](#sqlalchemy.schema.ForeignKeyConstraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

    property referred_table: [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)

The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object to which this
[ForeignKeyConstraint](#sqlalchemy.schema.ForeignKeyConstraint) references.

This is a dynamically calculated attribute which may not be available
if the constraint and/or parent table is not yet associated with
a metadata collection that contains the referred table.

     class sqlalchemy.schema.HasConditionalDDL

define a class that includes the [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if)
method, allowing for conditional rendering of DDL.

Currently applies to constraints and indexes.

Added in version 2.0.

| Member Name | Description |
| --- | --- |
| ddl_if() | apply a conditional DDL rule to this schema item. |

   method [sqlalchemy.schema.HasConditionalDDL.](#sqlalchemy.schema.HasConditionalDDL)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

      class sqlalchemy.schema.PrimaryKeyConstraint

*inherits from* [sqlalchemy.schema.ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

A table-level PRIMARY KEY constraint.

The [PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint) object is present automatically
on any [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object; it is assigned a set of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects corresponding to those marked with
the [Column.primary_key](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.primary_key) flag:

```
>>> my_table = Table(
...     "mytable",
...     metadata,
...     Column("id", Integer, primary_key=True),
...     Column("version_id", Integer, primary_key=True),
...     Column("data", String(50)),
... )
>>> my_table.primary_key
PrimaryKeyConstraint(
    Column('id', Integer(), table=<mytable>,
           primary_key=True, nullable=False),
    Column('version_id', Integer(), table=<mytable>,
           primary_key=True, nullable=False)
)
```

The primary key of a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) can also be specified by using
a [PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint) object explicitly; in this mode of usage,
the “name” of the constraint can also be specified, as well as other
options which may be recognized by dialects:

```
my_table = Table(
    "mytable",
    metadata,
    Column("id", Integer),
    Column("version_id", Integer),
    Column("data", String(50)),
    PrimaryKeyConstraint("id", "version_id", name="mytable_pk"),
)
```

The two styles of column-specification should generally not be mixed.
An warning is emitted if the columns present in the
[PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint)
don’t match the columns that were marked as `primary_key=True`, if both
are present; in this case, the columns are taken strictly from the
[PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint) declaration, and those columns otherwise
marked as `primary_key=True` are ignored.  This behavior is intended to
be backwards compatible with previous behavior.

For the use case where specific options are to be specified on the
[PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint), but the usual style of using
`primary_key=True` flags is still desirable, an empty
[PrimaryKeyConstraint](#sqlalchemy.schema.PrimaryKeyConstraint) may be specified, which will take on the
primary key column collection from the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) based on the
flags:

```
my_table = Table(
    "mytable",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("version_id", Integer, primary_key=True),
    Column("data", String(50)),
    PrimaryKeyConstraint(name="mytable_pk", mssql_clustered=True),
)
```

| Member Name | Description |
| --- | --- |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| columns | AColumnCollectionrepresenting the set of columns
for this constraint. |
| contains_column() | Return True if this constraint contains the given column. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   classmethod [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      attribute [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)columns

*inherited from the* `ColumnCollectionMixin.columns` *attribute of* [ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) representing the set of columns
for this constraint.

    method [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)contains_column(*col:Column[Any]*) → bool

*inherited from the* [ColumnCollectionConstraint.contains_column()](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Return True if this constraint contains the given column.

Note that this object also contains an attribute `.columns`
which is a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)copy(***, *target_table:Table|None=None*, ***kw:Any*) → [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

*inherited from the* [ColumnCollectionConstraint.copy()](#sqlalchemy.schema.ColumnCollectionConstraint.copy) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Deprecated since version 1.4: The [ColumnCollectionConstraint.copy()](#sqlalchemy.schema.ColumnCollectionConstraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)dialect_options

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

     attribute [sqlalchemy.schema.PrimaryKeyConstraint.](#sqlalchemy.schema.PrimaryKeyConstraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     class sqlalchemy.schema.UniqueConstraint

*inherits from* [sqlalchemy.schema.ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

A table-level UNIQUE constraint.

Defines a single column or composite UNIQUE constraint. For a no-frills,
single column constraint, adding `unique=True` to the `Column`
definition is a shorthand equivalent for an unnamed, single column
UniqueConstraint.

| Member Name | Description |
| --- | --- |
| __init__() |  |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| columns | AColumnCollectionrepresenting the set of columns
for this constraint. |
| contains_column() | Return True if this constraint contains the given column. |
| copy() |  |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)__init__(**columns:_DDLColumnArgument*, *name:_ConstraintNameArgument=None*, *deferrable:bool|None=None*, *initially:str|None=None*, *info:_InfoType|None=None*, *_autoattach:bool=True*, *_column_flag:bool=False*, *_gather_expressions:List[_DDLColumnArgument]|None=None*, ***dialect_kw:Any*) → None

*inherited from the* `sqlalchemy.schema.ColumnCollectionConstraint.__init__` *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

   Parameters:

- ***columns** – A sequence of column names or Column objects.
- **name** – Optional, the in-database name of this constraint.
- **deferrable** – Optional bool.  If set, emit DEFERRABLE or NOT DEFERRABLE when
  issuing DDL for this constraint.
- **initially** – Optional string.  If set, emit INITIALLY <value> when issuing DDL
  for this constraint.
- ****dialect_kw** – other keyword arguments including
  dialect-specific arguments are propagated to the [Constraint](#sqlalchemy.schema.Constraint)
  superclass.

      classmethod [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      attribute [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)columns

*inherited from the* `ColumnCollectionMixin.columns` *attribute of* [ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin)

A [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) representing the set of columns
for this constraint.

    method [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)contains_column(*col:Column[Any]*) → bool

*inherited from the* [ColumnCollectionConstraint.contains_column()](#sqlalchemy.schema.ColumnCollectionConstraint.contains_column) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Return True if this constraint contains the given column.

Note that this object also contains an attribute `.columns`
which is a [ColumnCollection](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnCollection) of
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects.

    method [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)copy(***, *target_table:Table|None=None*, ***kw:Any*) → [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

*inherited from the* [ColumnCollectionConstraint.copy()](#sqlalchemy.schema.ColumnCollectionConstraint.copy) *method of* [ColumnCollectionConstraint](#sqlalchemy.schema.ColumnCollectionConstraint)

Deprecated since version 1.4: The [ColumnCollectionConstraint.copy()](#sqlalchemy.schema.ColumnCollectionConstraint.copy) method is deprecated and will be removed in a future release.

     method [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)dialect_options

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

     attribute [sqlalchemy.schema.UniqueConstraint.](#sqlalchemy.schema.UniqueConstraint)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).

     function sqlalchemy.schema.conv(*value:str*, *quote:bool|None=None*) → Any

Mark a string indicating that a name has already been converted
by a naming convention.

This is a string subclass that indicates a name that should not be
subject to any further naming conventions.

E.g. when we create a [Constraint](#sqlalchemy.schema.Constraint) using a naming convention
as follows:

```
m = MetaData(
    naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
)
t = Table(
    "t", m, Column("x", Integer), CheckConstraint("x > 5", name="x5")
)
```

The name of the above constraint will be rendered as `"ck_t_x5"`.
That is, the existing name `x5` is used in the naming convention as the
`constraint_name` token.

In some situations, such as in migration scripts, we may be rendering
the above [CheckConstraint](#sqlalchemy.schema.CheckConstraint) with a name that’s already been
converted.  In order to make sure the name isn’t double-modified, the
new name is applied using the [conv()](#sqlalchemy.schema.conv) marker.  We can
use this explicitly as follows:

```
m = MetaData(
    naming_convention={"ck": "ck_%(table_name)s_%(constraint_name)s"}
)
t = Table(
    "t",
    m,
    Column("x", Integer),
    CheckConstraint("x > 5", name=conv("ck_t_x5")),
)
```

Where above, the [conv()](#sqlalchemy.schema.conv) marker indicates that the constraint
name here is final, and the name will render as `"ck_t_x5"` and not
`"ck_t_ck_t_x5"`

See also

[Configuring Constraint Naming Conventions](#constraint-naming-conventions)

## Indexes

Indexes can be created anonymously (using an auto-generated name `ix_<column
label>`) for a single column using the inline `index` keyword on
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), which also modifies the usage of
`unique` to apply the uniqueness to the index itself, instead of adding a
separate UNIQUE constraint. For indexes with specific names or which encompass
more than one column, use the [Index](#sqlalchemy.schema.Index) construct,
which requires a name.

Below we illustrate a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) with several
[Index](#sqlalchemy.schema.Index) objects associated. The DDL for “CREATE
INDEX” is issued right after the create statements for the table:

```
metadata_obj = MetaData()
mytable = Table(
    "mytable",
    metadata_obj,
    # an indexed column, with index "ix_mytable_col1"
    Column("col1", Integer, index=True),
    # a uniquely indexed column with index "ix_mytable_col2"
    Column("col2", Integer, index=True, unique=True),
    Column("col3", Integer),
    Column("col4", Integer),
    Column("col5", Integer),
    Column("col6", Integer),
)

# place an index on col3, col4
Index("idx_col34", mytable.c.col3, mytable.c.col4)

# place a unique index on col5, col6
Index("myindex", mytable.c.col5, mytable.c.col6, unique=True)

mytable.create(engine)
CREATE TABLE mytable (
    col1 INTEGER,
    col2 INTEGER,
    col3 INTEGER,
    col4 INTEGER,
    col5 INTEGER,
    col6 INTEGER
)
CREATE INDEX ix_mytable_col1 ON mytable (col1)
CREATE UNIQUE INDEX ix_mytable_col2 ON mytable (col2)
CREATE UNIQUE INDEX myindex ON mytable (col5, col6)
CREATE INDEX idx_col34 ON mytable (col3, col4)
```

Note in the example above, the [Index](#sqlalchemy.schema.Index) construct is created
externally to the table which it corresponds, using [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
objects directly.  [Index](#sqlalchemy.schema.Index) also supports
“inline” definition inside the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table), using string names to
identify columns:

```
metadata_obj = MetaData()
mytable = Table(
    "mytable",
    metadata_obj,
    Column("col1", Integer),
    Column("col2", Integer),
    Column("col3", Integer),
    Column("col4", Integer),
    # place an index on col1, col2
    Index("idx_col12", "col1", "col2"),
    # place a unique index on col3, col4
    Index("idx_col34", "col3", "col4", unique=True),
)
```

The [Index](#sqlalchemy.schema.Index) object also supports its own `create()` method:

```
i = Index("someindex", mytable.c.col5)
i.create(engine)
CREATE INDEX someindex ON mytable (col5)
```

### Functional Indexes

[Index](#sqlalchemy.schema.Index) supports SQL and function expressions, as supported by the
target backend.  To create an index against a column using a descending
value, the [ColumnElement.desc()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.desc) modifier may be used:

```
from sqlalchemy import Index

Index("someindex", mytable.c.somecol.desc())
```

Or with a backend that supports functional indexes such as PostgreSQL,
a “case insensitive” index can be created using the `lower()` function:

```
from sqlalchemy import func, Index

Index("someindex", func.lower(mytable.c.somecol))
```

## Index API

| Object Name | Description |
| --- | --- |
| Index | A table-level INDEX. |

   class sqlalchemy.schema.Index

*inherits from* `sqlalchemy.sql.expression.DialectKWArgs`, [sqlalchemy.schema.ColumnCollectionMixin](#sqlalchemy.schema.ColumnCollectionMixin), [sqlalchemy.schema.HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL), [sqlalchemy.schema.SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

A table-level INDEX.

Defines a composite (one or more column) INDEX.

E.g.:

```
sometable = Table(
    "sometable",
    metadata,
    Column("name", String(50)),
    Column("address", String(100)),
)

Index("some_index", sometable.c.name)
```

For a no-frills, single column index, adding
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) also supports `index=True`:

```
sometable = Table(
    "sometable", metadata, Column("name", String(50), index=True)
)
```

For a composite index, multiple columns can be specified:

```
Index("some_index", sometable.c.name, sometable.c.address)
```

Functional indexes are supported as well, typically by using the
[func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func) construct in conjunction with table-bound
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects:

```
Index("some_index", func.lower(sometable.c.name))
```

An [Index](#sqlalchemy.schema.Index) can also be manually associated with a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table),
either through inline declaration or using
[Table.append_constraint()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.append_constraint).  When this approach is used,
the names
of the indexed columns can be specified as strings:

```
Table(
    "sometable",
    metadata,
    Column("name", String(50)),
    Column("address", String(100)),
    Index("some_index", "name", "address"),
)
```

To support functional or expression-based indexes in this form, the
[text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text) construct may be used:

```
from sqlalchemy import text

Table(
    "sometable",
    metadata,
    Column("name", String(50)),
    Column("address", String(100)),
    Index("some_index", text("lower(name)")),
)
```

See also

[Indexes](#schema-indexes) - General information on [Index](#sqlalchemy.schema.Index).

[PostgreSQL-Specific Index Options](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-indexes) - PostgreSQL-specific options available for
the [Index](#sqlalchemy.schema.Index) construct.

[MySQL / MariaDB- Specific Index Options](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-indexes) - MySQL-specific options available for the
[Index](#sqlalchemy.schema.Index) construct.

[Clustered Index Support](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-indexes) - MSSQL-specific options available for the
[Index](#sqlalchemy.schema.Index) construct.

| Member Name | Description |
| --- | --- |
| __init__() | Construct an index object. |
| argument_for() | Add a new kind of dialect-specific keyword argument for this class. |
| create() | Issue aCREATEstatement for thisIndex, using the givenConnectionorEngine`for connectivity. |
| ddl_if() | apply a conditional DDL rule to this schema item. |
| dialect_options | A collection of keyword arguments specified as dialect-specific
options to this construct. |
| drop() | Issue aDROPstatement for thisIndex, using the givenConnectionorEnginefor connectivity. |
| info | Info dictionary associated with the object, allowing user-defined
data to be associated with thisSchemaItem. |

   method [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)__init__(*name:str|None*, **expressions:_DDLColumnArgument*, *unique:bool=False*, *quote:bool|None=None*, *info:_InfoType|None=None*, *_table:Table|None=None*, *_column_flag:bool=False*, ***dialect_kw:Any*) → None

Construct an index object.

  Parameters:

- **name** – The name of the index
- ***expressions** – Column expressions to include in the index.   The expressions
  are normally instances of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), but may also
  be arbitrary SQL expressions which ultimately refer to a
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).
- **unique=False** – Keyword only argument; if True, create a unique index.
- **quote=None** – Keyword only argument; whether to apply quoting to the name of
  the index.  Works in the same manner as that of
  [Column.quote](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.quote).
- **info=None** – Optional data dictionary which will be populated
  into the [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) attribute of this object.
- ****dialect_kw** – Additional keyword arguments not mentioned above
  are dialect specific, and passed in the form
  `<dialectname>_<argname>`. See the documentation regarding an
  individual dialect at [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html) for detail on
  documented arguments.

      classmethod [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)argument_for(*dialect_name:str*, *argument_name:str*, *default:Any*) → None

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

      method [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)create(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue a `CREATE` statement for this
[Index](#sqlalchemy.schema.Index), using the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or `Engine`` for connectivity.

See also

[MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all).

     method [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)ddl_if(*dialect:str|None=None*, *callable_:DDLIfCallable|None=None*, *state:Any|None=None*) → Self

*inherited from the* [HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) *method of* [HasConditionalDDL](#sqlalchemy.schema.HasConditionalDDL)

apply a conditional DDL rule to this schema item.

These rules work in a similar manner to the
[ExecutableDDLElement.execute_if()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if) callable, with the added
feature that the criteria may be checked within the DDL compilation
phase for a construct such as [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable).
[HasConditionalDDL.ddl_if()](#sqlalchemy.schema.HasConditionalDDL.ddl_if) currently applies towards the
[Index](#sqlalchemy.schema.Index) construct as well as all [Constraint](#sqlalchemy.schema.Constraint)
constructs.

  Parameters:

- **dialect** – string name of a dialect, or a tuple of string names
  to indicate multiple dialect types.
- **callable_** – a callable that is constructed using the same form
  as that described in
  [ExecutableDDLElement.execute_if.callable_](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.ExecutableDDLElement.execute_if.params.callable_).
- **state** – any arbitrary object that will be passed to the
  callable, if present.

Added in version 2.0.

See also

[Controlling DDL Generation of Constraints and Indexes](https://docs.sqlalchemy.org/en/20/core/ddl.html#schema-ddl-ddl-if) - background and usage examples

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

     attribute [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)dialect_options

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

     method [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)drop(*bind:_CreateDropBind*, *checkfirst:bool=False*) → None

Issue a `DROP` statement for this
[Index](#sqlalchemy.schema.Index), using the given
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) for connectivity.

See also

[MetaData.drop_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all).

     attribute [sqlalchemy.schema.Index.](#sqlalchemy.schema.Index)info

*inherited from the* [SchemaItem.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem.info) *attribute of* [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem)

Info dictionary associated with the object, allowing user-defined
data to be associated with this [SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem).

The dictionary is automatically generated when first accessed.
It can also be specified in the constructor of some objects,
such as [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) and [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column).

    property kwargs: _DialectArgView

A synonym for [DialectKWArgs.dialect_kwargs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs.dialect_kwargs).
