# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Reflecting Database Objects

A [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object can be instructed to load
information about itself from the corresponding database schema object already
existing within the database. This process is called *reflection*. In the
most simple case you need only specify the table name, a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
object, and the `autoload_with` argument:

```
>>> messages = Table("messages", metadata_obj, autoload_with=engine)
>>> [c.name for c in messages.columns]
['message_id', 'message_name', 'date']
```

The above operation will use the given engine to query the database for
information about the `messages` table, and will then generate
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey),
and other objects corresponding to this information as though the
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object were hand-constructed in Python.

When tables are reflected, if a given table references another one via foreign
key, a second [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object is created within the
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object representing the connection.
Below, assume the table `shopping_cart_items` references a table named
`shopping_carts`. Reflecting the `shopping_cart_items` table has the
effect such that the `shopping_carts` table will also be loaded:

```
>>> shopping_cart_items = Table("shopping_cart_items", metadata_obj, autoload_with=engine)
>>> "shopping_carts" in metadata_obj.tables
True
```

The [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) has an interesting “singleton-like”
behavior such that if you requested both tables individually,
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) will ensure that exactly one
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object is created for each distinct table
name. The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) constructor actually returns to
you the already-existing [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object if one
already exists with the given name. Such as below, we can access the already
generated `shopping_carts` table just by naming it:

```
shopping_carts = Table("shopping_carts", metadata_obj)
```

Of course, it’s a good idea to use `autoload_with=engine` with the above table
regardless. This is so that the table’s attributes will be loaded if they have
not been already. The autoload operation only occurs for the table if it
hasn’t already been loaded; once loaded, new calls to
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) with the same name will not re-issue any
reflection queries.

## Overriding Reflected Columns

Individual columns can be overridden with explicit values when reflecting
tables; this is handy for specifying custom datatypes, constraints such as
primary keys that may not be configured within the database, etc.:

```
>>> mytable = Table(
...     "mytable",
...     metadata_obj,
...     Column(
...         "id", Integer, primary_key=True
...     ),  # override reflected 'id' to have primary key
...     Column("mydata", Unicode(50)),  # override reflected 'mydata' to be Unicode
...     # additional Column objects which require no change are reflected normally
...     autoload_with=some_engine,
... )
```

See also

[Working with Custom Types and Reflection](https://docs.sqlalchemy.org/en/20/core/custom_types.html#custom-and-decorated-types-reflection) - illustrates how the above
column override technique applies to the use of custom datatypes with
table reflection.

## Reflecting Views

The reflection system can also reflect views. Basic usage is the same as that
of a table:

```
my_view = Table("some_view", metadata, autoload_with=engine)
```

Above, `my_view` is a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object with
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects representing the names and types of
each column within the view “some_view”.

Usually, it’s desired to have at least a primary key constraint when
reflecting a view, if not foreign keys as well. View reflection doesn’t
extrapolate these constraints.

Use the “override” technique for this, specifying explicitly those columns
which are part of the primary key or have foreign key constraints:

```
my_view = Table(
    "some_view",
    metadata,
    Column("view_id", Integer, primary_key=True),
    Column("related_thing", Integer, ForeignKey("othertable.thing_id")),
    autoload_with=engine,
)
```

## Reflecting All Tables at Once

The [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object can also get a listing of
tables and reflect the full set. This is achieved by using the
[reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) method. After calling it, all
located tables are present within the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
object’s dictionary of tables:

```
metadata_obj = MetaData()
metadata_obj.reflect(bind=someengine)
users_table = metadata_obj.tables["users"]
addresses_table = metadata_obj.tables["addresses"]
```

`metadata.reflect()` also provides a handy way to clear or delete all the rows in a database:

```
metadata_obj = MetaData()
metadata_obj.reflect(bind=someengine)
with someengine.begin() as conn:
    for table in reversed(metadata_obj.sorted_tables):
        conn.execute(table.delete())
```

## Reflecting Tables from Other Schemas

The section [Specifying the Schema Name](https://docs.sqlalchemy.org/en/20/core/metadata.html#schema-table-schema-name) introduces the concept of table
schemas, which are namespaces within a database that contain tables and other
objects, and which can be specified explicitly. The “schema” for a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, as well as for other objects like views, indexes and
sequences, can be set up using the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) parameter,
and also as the default schema for a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object using the
[MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter.

The use of this schema parameter directly affects where the table reflection
feature will look when it is asked to reflect objects.  For example, given
a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object configured with a default schema name
“project” via its [MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) parameter:

```
>>> metadata_obj = MetaData(schema="project")
```

The [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) will then utilize that configured `.schema`
for reflection:

```
>>> # uses `schema` configured in metadata_obj
>>> metadata_obj.reflect(someengine)
```

The end result is that [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects from the “project”
schema will be reflected, and they will be populated as schema-qualified
with that name:

```
>>> metadata_obj.tables["project.messages"]
Table('messages', MetaData(), Column('message_id', INTEGER(), table=<messages>), schema='project')
```

Similarly, an individual [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object that includes the
[Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) parameter will also be reflected from that
database schema, overriding any default schema that may have been configured on the
owning [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection:

```
>>> messages = Table("messages", metadata_obj, schema="project", autoload_with=someengine)
>>> messages
Table('messages', MetaData(), Column('message_id', INTEGER(), table=<messages>), schema='project')
```

Finally, the [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) method itself also allows a
[MetaData.reflect.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect.params.schema) parameter to be passed, so we
could also load tables from the “project” schema for a default configured
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object:

```
>>> metadata_obj = MetaData()
>>> metadata_obj.reflect(someengine, schema="project")
```

We can call [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect) any number of times with different
[MetaData.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.params.schema) arguments (or none at all) to continue
populating the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object with more objects:

```
>>> # add tables from the "customer" schema
>>> metadata_obj.reflect(someengine, schema="customer")
>>> # add tables from the default schema
>>> metadata_obj.reflect(someengine)
```

### Interaction of Schema-qualified Reflection with the Default Schema

Section Best Practices Summarized

In this section, we discuss SQLAlchemy’s reflection behavior regarding
tables that are visible in the “default schema” of a database session,
and how these interact with SQLAlchemy directives that include the schema
explicitly.  As a best practice, ensure the “default” schema for a database
is just a single name, and not a list of names; for tables that are
part of this “default” schema and can be named without schema qualification
in DDL and SQL, leave corresponding [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) and
similar schema parameters set to their default of `None`.

As described at [Specifying a Default Schema Name with MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#schema-metadata-schema-name), databases that have
the concept of schemas usually also include the concept of a “default” schema.
The reason for this is naturally that when one refers to table objects without
a schema as is common, a schema-capable database will still consider that
table to be in a “schema” somewhere.   Some databases such as PostgreSQL
take this concept further into the notion of a
[schema search path](https://www.postgresql.org/docs/current/static/ddl-schemas.html#DDL-SCHEMAS-PATH)
where *multiple* schema names can be considered in a particular database
session to be “implicit”; referring to a table name that it’s any of those
schemas will not require that the schema name be present (while at the same time
it’s also perfectly fine if the schema name *is* present).

Since most relational databases therefore have the concept of a particular
table object which can be referenced both in a schema-qualified way, as
well as an “implicit” way where no schema is present, this presents a
complexity for SQLAlchemy’s reflection
feature.  Reflecting a table in
a schema-qualified manner will always populate its [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.schema)
attribute and additionally affect how this [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) is organized
into the [MetaData.tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.tables) collection, that is, in a schema
qualified manner.  Conversely, reflecting the **same** table in a non-schema
qualified manner will organize it into the [MetaData.tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.tables)
collection **without** being schema qualified.  The end result is that there
would be two separate [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects in the single
[MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) collection representing the same table in the
actual database.

To illustrate the ramifications of this issue, consider tables from the
“project” schema in the previous example, and suppose also that the “project”
schema is the default schema of our database connection, or if using a database
such as PostgreSQL suppose the “project” schema is set up in the PostgreSQL
`search_path`.  This would mean that the database accepts the following
two SQL statements as equivalent:

```
-- schema qualified
SELECT message_id FROM project.messages

-- non-schema qualified
SELECT message_id FROM messages
```

This is not a problem as the table can be found in both ways.  However
in SQLAlchemy, it’s the **identity** of the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object
that determines its semantic role within a SQL statement.  Based on the current
decisions within SQLAlchemy, this means that if we reflect the same “messages” table in
both a schema-qualified as well as a non-schema qualified manner, we get
**two** [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects that will **not** be treated as
semantically equivalent:

```
>>> # reflect in non-schema qualified fashion
>>> messages_table_1 = Table("messages", metadata_obj, autoload_with=someengine)
>>> # reflect in schema qualified fashion
>>> messages_table_2 = Table(
...     "messages", metadata_obj, schema="project", autoload_with=someengine
... )
>>> # two different objects
>>> messages_table_1 is messages_table_2
False
>>> # stored in two different ways
>>> metadata.tables["messages"] is messages_table_1
True
>>> metadata.tables["project.messages"] is messages_table_2
True
```

The above issue becomes more complicated when the tables being reflected contain
foreign key references to other tables.  Suppose “messages” has a “project_id”
column which refers to rows in another schema-local table “projects”, meaning
there is a [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object that is part of the
definition of the “messages” table.

We can find ourselves in a situation where one [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
collection may contain as many as four [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
representing these two database tables, where one or two of the additional
tables were generated by the reflection process; this is because when
the reflection process encounters a foreign key constraint on a table
being reflected, it branches out to reflect that referenced table as well.
The decision making it uses to assign the schema to this referenced
table is that SQLAlchemy will **omit a default schema** from the reflected
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) object if the owning
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) also omits its schema name and also that these two objects
are in the same schema, but will **include** it if
it were not omitted.

The common scenario is when the reflection of a table in a schema qualified
fashion then loads a related table that will also be performed in a schema
qualified fashion:

```
>>> # reflect "messages" in a schema qualified fashion
>>> messages_table_1 = Table(
...     "messages", metadata_obj, schema="project", autoload_with=someengine
... )
```

The above `messages_table_1` will refer to `projects` also in a schema
qualified fashion.  This “projects” table will be reflected automatically by
the fact that “messages” refers to it:

```
>>> messages_table_1.c.project_id
Column('project_id', INTEGER(), ForeignKey('project.projects.project_id'), table=<messages>)
```

if some other part of the code reflects “projects” in a non-schema qualified
fashion, there are now two projects tables that are not the same:

```
>>> # reflect "projects" in a non-schema qualified fashion
>>> projects_table_1 = Table("projects", metadata_obj, autoload_with=someengine)
```

```
>>> # messages does not refer to projects_table_1 above
>>> messages_table_1.c.project_id.references(projects_table_1.c.project_id)
False
```

```
>>> # it refers to this one
>>> projects_table_2 = metadata_obj.tables["project.projects"]
>>> messages_table_1.c.project_id.references(projects_table_2.c.project_id)
True
```

```
>>> # they're different, as one non-schema qualified and the other one is
>>> projects_table_1 is projects_table_2
False
```

The above confusion can cause problems within applications that use table
reflection to load up application-level [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects, as
well as within migration scenarios, in particular such as when using Alembic
Migrations to detect new tables and foreign key constraints.

The above behavior can be remedied by sticking to one simple practice:

- Don’t include the [Table.schema](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.schema) parameter for any
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that expects to be located in the **default** schema
  of the database.

For PostgreSQL and other databases that support a “search” path for schemas,
add the following additional practice:

- Keep the “search path” narrowed down to **one schema only, which is the
  default schema**.

See also

[Remote-Schema Table Introspection and PostgreSQL search_path](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-schema-reflection) - additional details of this behavior
as regards the PostgreSQL database.

## Fine Grained Reflection with Inspector

A low level interface which provides a backend-agnostic system of loading
lists of schema, table, column, and constraint descriptions from a given
database is also available. This is known as the “Inspector”:

```
from sqlalchemy import create_engine
from sqlalchemy import inspect

engine = create_engine("...")
insp = inspect(engine)
print(insp.get_table_names())
```

| Object Name | Description |
| --- | --- |
| Inspector | Performs database schema inspection. |
| ReflectedCheckConstraint | Dictionary representing the reflected elements corresponding toCheckConstraint. |
| ReflectedColumn | Dictionary representing the reflected elements corresponding to
aColumnobject. |
| ReflectedComputed | Represent the reflected elements of a computed column, corresponding
to theComputedconstruct. |
| ReflectedForeignKeyConstraint | Dictionary representing the reflected elements corresponding toForeignKeyConstraint. |
| ReflectedIdentity | represent the reflected IDENTITY structure of a column, corresponding
to theIdentityconstruct. |
| ReflectedIndex | Dictionary representing the reflected elements corresponding toIndex. |
| ReflectedPrimaryKeyConstraint | Dictionary representing the reflected elements corresponding toPrimaryKeyConstraint. |
| ReflectedTableComment | Dictionary representing the reflected comment corresponding to
theTable.commentattribute. |
| ReflectedUniqueConstraint | Dictionary representing the reflected elements corresponding toUniqueConstraint. |

   class sqlalchemy.engine.reflection.Inspector

*inherits from* `sqlalchemy.inspection.Inspectable`

Performs database schema inspection.

The Inspector acts as a proxy to the reflection methods of the
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect), providing a
consistent interface as well as caching support for previously
fetched metadata.

A [Inspector](#sqlalchemy.engine.reflection.Inspector) object is usually created via the
[inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function, which may be passed an
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
or a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection):

```
from sqlalchemy import inspect, create_engine

engine = create_engine("...")
insp = inspect(engine)
```

Where above, the [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) associated
with the engine may opt to return an [Inspector](#sqlalchemy.engine.reflection.Inspector)
subclass that
provides additional methods specific to the dialect’s target database.

| Member Name | Description |
| --- | --- |
| __init__() | Initialize a newInspector. |
| bind |  |
| clear_cache() | reset the cache for thisInspector. |
| dialect |  |
| engine |  |
| from_engine() | Construct a new dialect-specific Inspector object from the given
engine or connection. |
| get_check_constraints() | Return information about check constraints intable_name. |
| get_columns() | Return information about columns intable_name. |
| get_foreign_keys() | Return information about foreign_keys intable_name. |
| get_indexes() | Return information about indexes intable_name. |
| get_materialized_view_names() | Return all materialized view names inschema. |
| get_multi_check_constraints() | Return information about check constraints in all tables
in the given schema. |
| get_multi_columns() | Return information about columns in all objects in the given
schema. |
| get_multi_foreign_keys() | Return information about foreign_keys in all tables
in the given schema. |
| get_multi_indexes() | Return information about indexes in in all objects
in the given schema. |
| get_multi_pk_constraint() | Return information about primary key constraints in
all tables in the given schema. |
| get_multi_table_comment() | Return information about the table comment in all objects
in the given schema. |
| get_multi_table_options() | Return a dictionary of options specified when the tables in the
given schema were created. |
| get_multi_unique_constraints() | Return information about unique constraints in all tables
in the given schema. |
| get_pk_constraint() | Return information about primary key constraint intable_name. |
| get_schema_names() | Return all schema names. |
| get_sequence_names() | Return all sequence names inschema. |
| get_sorted_table_and_fkc_names() | Return dependency-sorted table and foreign key constraint names in
referred to within a particular schema. |
| get_table_comment() | Return information about the table comment fortable_name. |
| get_table_names() | Return all table names within a particular schema. |
| get_table_options() | Return a dictionary of options specified when the table of the
given name was created. |
| get_temp_table_names() | Return a list of temporary table names for the current bind. |
| get_temp_view_names() | Return a list of temporary view names for the current bind. |
| get_unique_constraints() | Return information about unique constraints intable_name. |
| get_view_definition() | Return definition for the plain or materialized view calledview_name. |
| get_view_names() | Return all non-materialized view names inschema. |
| has_index() | Check the existence of a particular index name in the database. |
| has_schema() | Return True if the backend has a schema with the given name. |
| has_sequence() | Return True if the backend has a sequence with the given name. |
| has_table() | Return True if the backend has a table, view, or temporary
table of the given name. |
| info_cache |  |
| reflect_table() | Given aTableobject, load its internal
constructs based on introspection. |
| sort_tables_on_foreign_key_dependency() | Return dependency-sorted table and foreign key constraint names
referred to within multiple schemas. |

   method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)__init__(*bind:Engine|Connection*)

Initialize a new [Inspector](#sqlalchemy.engine.reflection.Inspector).

Deprecated since version 1.4: The __init__() method on [Inspector](#sqlalchemy.engine.reflection.Inspector) is deprecated and will be removed in a future release.  Please use the [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function on an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) in order to acquire an [Inspector](#sqlalchemy.engine.reflection.Inspector).

   Parameters:

**bind** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection),
which is typically an instance of
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

For a dialect-specific instance of [Inspector](#sqlalchemy.engine.reflection.Inspector), see
[Inspector.from_engine()](#sqlalchemy.engine.reflection.Inspector.from_engine)

    attribute [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)bind: [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) | [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)    method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)clear_cache() → None

reset the cache for this [Inspector](#sqlalchemy.engine.reflection.Inspector).

Inspection methods that have data cached will emit SQL queries
when next called to get new data.

Added in version 2.0.

     property default_schema_name: str | None

Return the default schema name presented by the dialect
for the current engine’s database user.

E.g. this is typically `public` for PostgreSQL and `dbo`
for SQL Server.

    attribute [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)dialect: [Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect)    attribute [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)engine: [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)    classmethod [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)from_engine(*bind:Engine*) → [Inspector](#sqlalchemy.engine.reflection.Inspector)

Construct a new dialect-specific Inspector object from the given
engine or connection.

Deprecated since version 1.4: The from_engine() method on [Inspector](#sqlalchemy.engine.reflection.Inspector) is deprecated and will be removed in a future release.  Please use the [inspect()](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect) function on an [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) in order to acquire an [Inspector](#sqlalchemy.engine.reflection.Inspector).

   Parameters:

**bind** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
or [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).

This method differs from direct a direct constructor call of
[Inspector](#sqlalchemy.engine.reflection.Inspector) in that the
[Dialect](https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.Dialect) is given a chance to
provide a dialect-specific [Inspector](#sqlalchemy.engine.reflection.Inspector) instance,
which may
provide additional methods.

See the example at [Inspector](#sqlalchemy.engine.reflection.Inspector).

    method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_check_constraints(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedCheckConstraint](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)]

Return information about check constraints in `table_name`.

Given a string `table_name` and an optional string schema, return
check constraint information as a list of
[ReflectedCheckConstraint](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a list of dictionaries, each representing the
definition of a check constraints.

See also

[Inspector.get_multi_check_constraints()](#sqlalchemy.engine.reflection.Inspector.get_multi_check_constraints)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_columns(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn)]

Return information about columns in `table_name`.

Given a string `table_name` and an optional string `schema`,
return column information as a list of [ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

list of dictionaries, each representing the definition of
a database column.

See also

[Inspector.get_multi_columns()](#sqlalchemy.engine.reflection.Inspector.get_multi_columns).

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_foreign_keys(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedForeignKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)]

Return information about foreign_keys in `table_name`.

Given a string `table_name`, and an optional string schema, return
foreign key information as a list of
[ReflectedForeignKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a list of dictionaries, each representing the
a foreign key definition.

See also

[Inspector.get_multi_foreign_keys()](#sqlalchemy.engine.reflection.Inspector.get_multi_foreign_keys)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_indexes(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedIndex](#sqlalchemy.engine.interfaces.ReflectedIndex)]

Return information about indexes in `table_name`.

Given a string `table_name` and an optional string schema, return
index information as a list of [ReflectedIndex](#sqlalchemy.engine.interfaces.ReflectedIndex).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a list of dictionaries, each representing the
definition of an index.

See also

[Inspector.get_multi_indexes()](#sqlalchemy.engine.reflection.Inspector.get_multi_indexes)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_materialized_view_names(*schema:str|None=None*, ***kw:Any*) → List[str]

Return all materialized view names in schema.

  Parameters:

- **schema** – Optional, retrieve names from a non-default schema.
  For special quoting, use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Added in version 2.0.

See also

[Inspector.get_view_names()](#sqlalchemy.engine.reflection.Inspector.get_view_names)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_check_constraints(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, List[[ReflectedCheckConstraint](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)]]

Return information about check constraints in all tables
in the given schema.

The tables can be filtered by passing the names to use to
`filter_names`.

For each table the value is a list of
[ReflectedCheckConstraint](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if constraints of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are list of dictionaries, each representing the
definition of a check constraints.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_check_constraints()](#sqlalchemy.engine.reflection.Inspector.get_check_constraints)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_columns(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, List[[ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn)]]

Return information about columns in all objects in the given
schema.

The objects can be filtered by passing the names to use to
`filter_names`.

For each table the value is a list of [ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if columns of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are list of dictionaries, each representing the
definition of a database column.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_columns()](#sqlalchemy.engine.reflection.Inspector.get_columns)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_foreign_keys(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, List[[ReflectedForeignKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)]]

Return information about foreign_keys in all tables
in the given schema.

The tables can be filtered by passing the names to use to
`filter_names`.

For each table the value is a list of
[ReflectedForeignKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if foreign keys of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are list of dictionaries, each representing
a foreign key definition.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_foreign_keys()](#sqlalchemy.engine.reflection.Inspector.get_foreign_keys)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_indexes(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, List[[ReflectedIndex](#sqlalchemy.engine.interfaces.ReflectedIndex)]]

Return information about indexes in in all objects
in the given schema.

The objects can be filtered by passing the names to use to
`filter_names`.

For each table the value is a list of [ReflectedIndex](#sqlalchemy.engine.interfaces.ReflectedIndex).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if indexes of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are list of dictionaries, each representing the
definition of an index.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_indexes()](#sqlalchemy.engine.reflection.Inspector.get_indexes)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_pk_constraint(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, [ReflectedPrimaryKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)]

Return information about primary key constraints in
all tables in the given schema.

The tables can be filtered by passing the names to use to
`filter_names`.

For each table the value is a [ReflectedPrimaryKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if primary keys of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are dictionaries, each representing the
definition of a primary key constraint.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_pk_constraint()](#sqlalchemy.engine.reflection.Inspector.get_pk_constraint)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_table_comment(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, [ReflectedTableComment](#sqlalchemy.engine.interfaces.ReflectedTableComment)]

Return information about the table comment in all objects
in the given schema.

The objects can be filtered by passing the names to use to
`filter_names`.

For each table the value is a [ReflectedTableComment](#sqlalchemy.engine.interfaces.ReflectedTableComment).

Raises `NotImplementedError` for a dialect that does not support
comments.

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if comments of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are dictionaries, representing the
table comments.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_table_comment()](#sqlalchemy.engine.reflection.Inspector.get_table_comment)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_table_options(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, Dict[str, Any]]

Return a dictionary of options specified when the tables in the
given schema were created.

The tables can be filtered by passing the names to use to
`filter_names`.

This currently includes some options that apply to MySQL and Oracle
tables.

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if options of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are dictionaries with the table options.
The returned keys in each dict depend on the
dialect in use. Each one is prefixed with the dialect name.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_table_options()](#sqlalchemy.engine.reflection.Inspector.get_table_options)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_multi_unique_constraints(*schema:str|None=None*, *filter_names:Sequence[str]|None=None*, *kind:ObjectKind=<ObjectKind.TABLE:1>*, *scope:ObjectScope=<ObjectScope.DEFAULT:1>*, ***kw:Any*) → Dict[TableKey, List[[ReflectedUniqueConstraint](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)]]

Return information about unique constraints in all tables
in the given schema.

The tables can be filtered by passing the names to use to
`filter_names`.

For each table the value is a list of
[ReflectedUniqueConstraint](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint).

  Parameters:

- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **filter_names** – optionally return information only for the
  objects listed here.
- **kind** – a `ObjectKind` that specifies the type of objects
  to reflect. Defaults to `ObjectKind.TABLE`.
- **scope** – a `ObjectScope` that specifies if constraints of
  default, temporary or any tables should be reflected.
  Defaults to `ObjectScope.DEFAULT`.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary where the keys are two-tuple schema,table-name
and the values are list of dictionaries, each representing the
definition of an unique constraint.
The schema is `None` if no schema is provided.

Added in version 2.0.

See also

[Inspector.get_unique_constraints()](#sqlalchemy.engine.reflection.Inspector.get_unique_constraints)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_pk_constraint(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedPrimaryKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)

Return information about primary key constraint in `table_name`.

Given a string `table_name`, and an optional string schema, return
primary key information as a [ReflectedPrimaryKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary representing the definition of
a primary key constraint.

See also

[Inspector.get_multi_pk_constraint()](#sqlalchemy.engine.reflection.Inspector.get_multi_pk_constraint)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_schema_names(***kw:Any*) → List[str]

Return all schema names.

  Parameters:

****kw** – Additional keyword argument to pass to the dialect
specific implementation. See the documentation of the dialect
in use for more information.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_sequence_names(*schema:str|None=None*, ***kw:Any*) → List[str]

Return all sequence names in schema.

  Parameters:

- **schema** – Optional, retrieve names from a non-default schema.
  For special quoting, use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_sorted_table_and_fkc_names(*schema:str|None=None*, ***kw:Any*) → List[Tuple[str | None, List[Tuple[str, str | None]]]]

Return dependency-sorted table and foreign key constraint names in
referred to within a particular schema.

This will yield 2-tuples of
`(tablename, [(tname, fkname), (tname, fkname), ...])`
consisting of table names in CREATE order grouped with the foreign key
constraint names that are not detected as belonging to a cycle.
The final element
will be `(None, [(tname, fkname), (tname, fkname), ..])`
which will consist of remaining
foreign key constraint names that would require a separate CREATE
step after-the-fact, based on dependencies between tables.

  Parameters:

- **schema** – schema name to query, if not the default schema.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

See also

[Inspector.get_table_names()](#sqlalchemy.engine.reflection.Inspector.get_table_names)

[sort_tables_and_constraints()](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.sort_tables_and_constraints) - similar method which works
with an already-given [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_table_comment(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedTableComment](#sqlalchemy.engine.interfaces.ReflectedTableComment)

Return information about the table comment for `table_name`.

Given a string `table_name` and an optional string `schema`,
return table comment information as a [ReflectedTableComment](#sqlalchemy.engine.interfaces.ReflectedTableComment).

Raises `NotImplementedError` for a dialect that does not support
comments.

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dictionary, with the table comment.

Added in version 1.2.

See also

[Inspector.get_multi_table_comment()](#sqlalchemy.engine.reflection.Inspector.get_multi_table_comment)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_table_names(*schema:str|None=None*, ***kw:Any*) → List[str]

Return all table names within a particular schema.

The names are expected to be real tables only, not views.
Views are instead returned using the
[Inspector.get_view_names()](#sqlalchemy.engine.reflection.Inspector.get_view_names) and/or
[Inspector.get_materialized_view_names()](#sqlalchemy.engine.reflection.Inspector.get_materialized_view_names)
methods.

  Parameters:

- **schema** – Schema name. If `schema` is left at `None`, the
  database’s default schema is
  used, else the named schema is searched.  If the database does not
  support named schemas, behavior is undefined if `schema` is not
  passed as `None`.  For special quoting, use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

See also

[Inspector.get_sorted_table_and_fkc_names()](#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names)

[MetaData.sorted_tables](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.sorted_tables)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_table_options(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → Dict[str, Any]

Return a dictionary of options specified when the table of the
given name was created.

This currently includes some options that apply to MySQL and Oracle
Database tables.

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a dict with the table options. The returned keys depend on the
dialect in use. Each one is prefixed with the dialect name.

See also

[Inspector.get_multi_table_options()](#sqlalchemy.engine.reflection.Inspector.get_multi_table_options)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_temp_table_names(***kw:Any*) → List[str]

Return a list of temporary table names for the current bind.

This method is unsupported by most dialects; currently
only Oracle Database, PostgreSQL and SQLite implements it.

  Parameters:

****kw** – Additional keyword argument to pass to the dialect
specific implementation. See the documentation of the dialect
in use for more information.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_temp_view_names(***kw:Any*) → List[str]

Return a list of temporary view names for the current bind.

This method is unsupported by most dialects; currently
only PostgreSQL and SQLite implements it.

  Parameters:

****kw** – Additional keyword argument to pass to the dialect
specific implementation. See the documentation of the dialect
in use for more information.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_unique_constraints(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedUniqueConstraint](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)]

Return information about unique constraints in `table_name`.

Given a string `table_name` and an optional string schema, return
unique constraint information as a list of
[ReflectedUniqueConstraint](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint).

  Parameters:

- **table_name** – string name of the table.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- **schema** – string schema name; if omitted, uses the default schema
  of the database connection.  For special quoting,
  use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

  Returns:

a list of dictionaries, each representing the
definition of an unique constraint.

See also

[Inspector.get_multi_unique_constraints()](#sqlalchemy.engine.reflection.Inspector.get_multi_unique_constraints)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_view_definition(*view_name:str*, *schema:str|None=None*, ***kw:Any*) → str

Return definition for the plain or materialized view called
`view_name`.

  Parameters:

- **view_name** – Name of the view.
- **schema** – Optional, retrieve names from a non-default schema.
  For special quoting, use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)get_view_names(*schema:str|None=None*, ***kw:Any*) → List[str]

Return all non-materialized view names in schema.

  Parameters:

- **schema** – Optional, retrieve names from a non-default schema.
  For special quoting, use [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Changed in version 2.0: For those dialects that previously included
the names of materialized views in this list (currently PostgreSQL),
this method no longer returns the names of materialized views.
the [Inspector.get_materialized_view_names()](#sqlalchemy.engine.reflection.Inspector.get_materialized_view_names) method should
be used instead.

See also

[Inspector.get_materialized_view_names()](#sqlalchemy.engine.reflection.Inspector.get_materialized_view_names)

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)has_index(*table_name:str*, *index_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

Check the existence of a particular index name in the database.

  Parameters:

- **table_name** – the name of the table the index belongs to
- **index_name** – the name of the index to check
- **schema** – schema name to query, if not the default schema.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Added in version 2.0.

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)has_schema(*schema_name:str*, ***kw:Any*) → bool

Return True if the backend has a schema with the given name.

  Parameters:

- **schema_name** – name of the schema to check
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Added in version 2.0.

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)has_sequence(*sequence_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

Return True if the backend has a sequence with the given name.

  Parameters:

- **sequence_name** – name of the sequence to check
- **schema** – schema name to query, if not the default schema.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Added in version 1.4.

     method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)has_table(*table_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

Return True if the backend has a table, view, or temporary
table of the given name.

  Parameters:

- **table_name** – name of the table to check
- **schema** – schema name to query, if not the default schema.
- ****kw** – Additional keyword argument to pass to the dialect
  specific implementation. See the documentation of the dialect
  in use for more information.

Added in version 1.4: - the [Inspector.has_table()](#sqlalchemy.engine.reflection.Inspector.has_table) method
replaces the `Engine.has_table()` method.

Changed in version 2.0::: [Inspector.has_table()](#sqlalchemy.engine.reflection.Inspector.has_table) now formally
supports checking for additional table-like objects:

- any type of views (plain or materialized)
- temporary tables of any kind

Previously, these two checks were not formally specified and
different dialects would vary in their behavior.   The dialect
testing suite now includes tests for all of these object types
and should be supported by all SQLAlchemy-included dialects.
Support among third party dialects may be lagging, however.

     attribute [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)info_cache: Dict[Any, Any]    method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)reflect_table(*table:Table*, *include_columns:Collection[str]|None*, *exclude_columns:Collection[str]=()*, *resolve_fks:bool=True*, *_extend_on:Set[Table]|None=None*, *_reflect_info:_ReflectionInfo|None=None*) → None

Given a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object, load its internal
constructs based on introspection.

This is the underlying method used by most dialects to produce
table reflection.  Direct usage is like:

```
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import inspect

engine = create_engine("...")
meta = MetaData()
user_table = Table("user", meta)
insp = inspect(engine)
insp.reflect_table(user_table, None)
```

Changed in version 1.4: Renamed from `reflecttable` to
`reflect_table`

   Parameters:

- **table** – a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) instance.
- **include_columns** – a list of string column names to include
  in the reflection process.  If `None`, all columns are reflected.

      method [sqlalchemy.engine.reflection.Inspector.](#sqlalchemy.engine.reflection.Inspector)sort_tables_on_foreign_key_dependency(*consider_schemas:Collection[str|None]=(None,)*, ***kw:Any*) → List[Tuple[Tuple[str | None, str] | None, List[Tuple[Tuple[str | None, str], str | None]]]]

Return dependency-sorted table and foreign key constraint names
referred to within multiple schemas.

This method may be compared to
[Inspector.get_sorted_table_and_fkc_names()](#sqlalchemy.engine.reflection.Inspector.get_sorted_table_and_fkc_names), which
works on one schema at a time; here, the method is a generalization
that will consider multiple schemas at once including that it will
resolve for cross-schema foreign keys.

Added in version 2.0.

      class sqlalchemy.engine.interfaces.ReflectedColumn

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) object.

The [ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn) structure is returned by the
`get_columns` method.

| Member Name | Description |
| --- | --- |
| autoincrement | database-dependent autoincrement flag. |
| comment | comment for the column, if present.
Only some dialects return this key |
| computed | indicates that this column is computed by the database.
Only some dialects return this key. |
| default | column default expression as a SQL string |
| dialect_options | Additional dialect-specific options detected for this reflected
object |
| identity | indicates this column is an IDENTITY column.
Only some dialects return this key. |
| name | column name |
| nullable | boolean flag if the column is NULL or NOT NULL |
| type | column type represented as aTypeEngineinstance. |

   attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)autoincrement: NotRequired[bool]

database-dependent autoincrement flag.

This flag indicates if the column has a database-side “autoincrement”
flag of some kind.   Within SQLAlchemy, other kinds of columns may
also act as an “autoincrement” column without necessarily having
such a flag on them.

See [Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) for more background on
“autoincrement”.

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)comment: NotRequired[str | None]

comment for the column, if present.
Only some dialects return this key

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)computed: NotRequired[[ReflectedComputed](#sqlalchemy.engine.interfaces.ReflectedComputed)]

indicates that this column is computed by the database.
Only some dialects return this key.

Added in version 1.3.16: - added support for computed reflection.

     attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)default: str | None

column default expression as a SQL string

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)dialect_options: NotRequired[Dict[str, Any]]

Additional dialect-specific options detected for this reflected
object

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)identity: NotRequired[[ReflectedIdentity](#sqlalchemy.engine.interfaces.ReflectedIdentity)]

indicates this column is an IDENTITY column.
Only some dialects return this key.

Added in version 1.4: - added support for identity column reflection.

     attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)name: str

column name

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)nullable: bool

boolean flag if the column is NULL or NOT NULL

    attribute [sqlalchemy.engine.interfaces.ReflectedColumn.](#sqlalchemy.engine.interfaces.ReflectedColumn)type: [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]

column type represented as a [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) instance.

     class sqlalchemy.engine.interfaces.ReflectedComputed

*inherits from* `builtins.dict`

Represent the reflected elements of a computed column, corresponding
to the [Computed](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Computed) construct.

The [ReflectedComputed](#sqlalchemy.engine.interfaces.ReflectedComputed) structure is part of the
[ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn) structure, which is returned by the
[Inspector.get_columns()](#sqlalchemy.engine.reflection.Inspector.get_columns) method.

| Member Name | Description |
| --- | --- |
| persisted | indicates if the value is stored in the table or computed on demand |
| sqltext | the expression used to generate this column returned
as a string SQL expression |

   attribute [sqlalchemy.engine.interfaces.ReflectedComputed.](#sqlalchemy.engine.interfaces.ReflectedComputed)persisted: NotRequired[bool]

indicates if the value is stored in the table or computed on demand

    attribute [sqlalchemy.engine.interfaces.ReflectedComputed.](#sqlalchemy.engine.interfaces.ReflectedComputed)sqltext: str

the expression used to generate this column returned
as a string SQL expression

     class sqlalchemy.engine.interfaces.ReflectedCheckConstraint

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
[CheckConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.CheckConstraint).

The [ReflectedCheckConstraint](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint) structure is returned by the
[Inspector.get_check_constraints()](#sqlalchemy.engine.reflection.Inspector.get_check_constraints) method.

| Member Name | Description |
| --- | --- |
| dialect_options | Additional dialect-specific options detected for this check constraint |
| sqltext | the check constraint’s SQL expression |

   attribute [sqlalchemy.engine.interfaces.ReflectedCheckConstraint.](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)dialect_options: NotRequired[Dict[str, Any]]

Additional dialect-specific options detected for this check constraint

Added in version 1.3.8.

     attribute [sqlalchemy.engine.interfaces.ReflectedCheckConstraint.](#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)sqltext: str

the check constraint’s SQL expression

     class sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
[ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint).

The [ReflectedForeignKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint) structure is returned by
the [Inspector.get_foreign_keys()](#sqlalchemy.engine.reflection.Inspector.get_foreign_keys) method.

| Member Name | Description |
| --- | --- |
| constrained_columns | local column names which comprise the foreign key |
| options | Additional options detected for this foreign key constraint |
| referred_columns | referred column names that correspond toconstrained_columns |
| referred_schema | schema name of the table being referred |
| referred_table | name of the table being referred |

   attribute [sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)constrained_columns: List[str]

local column names which comprise the foreign key

    attribute [sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)options: NotRequired[Dict[str, Any]]

Additional options detected for this foreign key constraint

    attribute [sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)referred_columns: List[str]

referred column names that correspond to `constrained_columns`

    attribute [sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)referred_schema: str | None

schema name of the table being referred

    attribute [sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)referred_table: str

name of the table being referred

     class sqlalchemy.engine.interfaces.ReflectedIdentity

*inherits from* `builtins.dict`

represent the reflected IDENTITY structure of a column, corresponding
to the [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) construct.

The [ReflectedIdentity](#sqlalchemy.engine.interfaces.ReflectedIdentity) structure is part of the
[ReflectedColumn](#sqlalchemy.engine.interfaces.ReflectedColumn) structure, which is returned by the
[Inspector.get_columns()](#sqlalchemy.engine.reflection.Inspector.get_columns) method.

| Member Name | Description |
| --- | --- |
| always | type of identity column |
| cache | number of future values in the
sequence which are calculated in advance. |
| cycle | allows the sequence to wrap around when the maxvalue
or minvalue has been reached. |
| increment | increment value of the sequence |
| maxvalue | the maximum value of the sequence. |
| minvalue | the minimum value of the sequence. |
| nomaxvalue | no maximum value of the sequence. |
| nominvalue | no minimum value of the sequence. |
| on_null | indicates ON NULL |
| order | if true, renders the ORDER keyword. |
| start | starting index of the sequence |

   attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)always: bool

type of identity column

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)cache: int | None

number of future values in the
sequence which are calculated in advance.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)cycle: bool

allows the sequence to wrap around when the maxvalue
or minvalue has been reached.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)increment: int

increment value of the sequence

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)maxvalue: int

the maximum value of the sequence.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)minvalue: int

the minimum value of the sequence.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)nomaxvalue: bool

no maximum value of the sequence.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)nominvalue: bool

no minimum value of the sequence.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)on_null: bool

indicates ON NULL

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)order: bool

if true, renders the ORDER keyword.

    attribute [sqlalchemy.engine.interfaces.ReflectedIdentity.](#sqlalchemy.engine.interfaces.ReflectedIdentity)start: int

starting index of the sequence

     class sqlalchemy.engine.interfaces.ReflectedIndex

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
[Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index).

The [ReflectedIndex](#sqlalchemy.engine.interfaces.ReflectedIndex) structure is returned by the
[Inspector.get_indexes()](#sqlalchemy.engine.reflection.Inspector.get_indexes) method.

| Member Name | Description |
| --- | --- |
| column_names | column names which the index references.
An element of this list isNoneif it’s an expression and is
returned in theexpressionslist. |
| column_sorting | optional dict mapping column names or expressions to tuple of sort
keywords, which may includeasc,desc,nulls_first,nulls_last. |
| dialect_options | Additional dialect-specific options detected for this index |
| duplicates_constraint | Indicates if this index mirrors a constraint with this name |
| expressions | Expressions that compose the index. This list, when present, contains
both plain column names (that are also incolumn_names) and
expressions (that areNoneincolumn_names). |
| include_columns | columns to include in the INCLUDE clause for supporting databases. |
| name | index name |
| unique | whether or not the index has a unique flag |

   attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)column_names: List[str | None]

column names which the index references.
An element of this list is `None` if it’s an expression and is
returned in the `expressions` list.

    attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)column_sorting: NotRequired[Dict[str, Tuple[str]]]

optional dict mapping column names or expressions to tuple of sort
keywords, which may include `asc`, `desc`, `nulls_first`,
`nulls_last`.

Added in version 1.3.5.

     attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)dialect_options: NotRequired[Dict[str, Any]]

Additional dialect-specific options detected for this index

    attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)duplicates_constraint: NotRequired[str | None]

Indicates if this index mirrors a constraint with this name

    attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)expressions: NotRequired[List[str]]

Expressions that compose the index. This list, when present, contains
both plain column names (that are also in `column_names`) and
expressions (that are `None` in `column_names`).

    attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)include_columns: NotRequired[List[str]]

columns to include in the INCLUDE clause for supporting databases.

Deprecated since version 2.0: Legacy value, will be replaced with
`index_dict["dialect_options"]["<dialect name>_include"]`

     attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)name: str | None

index name

    attribute [sqlalchemy.engine.interfaces.ReflectedIndex.](#sqlalchemy.engine.interfaces.ReflectedIndex)unique: bool

whether or not the index has a unique flag

     class sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
[PrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.PrimaryKeyConstraint).

The [ReflectedPrimaryKeyConstraint](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint) structure is returned by the
[Inspector.get_pk_constraint()](#sqlalchemy.engine.reflection.Inspector.get_pk_constraint) method.

| Member Name | Description |
| --- | --- |
| constrained_columns | column names which comprise the primary key |
| dialect_options | Additional dialect-specific options detected for this primary key |

   attribute [sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)constrained_columns: List[str]

column names which comprise the primary key

    attribute [sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint.](#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)dialect_options: NotRequired[Dict[str, Any]]

Additional dialect-specific options detected for this primary key

     class sqlalchemy.engine.interfaces.ReflectedUniqueConstraint

*inherits from* `builtins.dict`

Dictionary representing the reflected elements corresponding to
[UniqueConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.UniqueConstraint).

The [ReflectedUniqueConstraint](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint) structure is returned by the
[Inspector.get_unique_constraints()](#sqlalchemy.engine.reflection.Inspector.get_unique_constraints) method.

| Member Name | Description |
| --- | --- |
| column_names | column names which comprise the unique constraint |
| dialect_options | Additional dialect-specific options detected for this unique
constraint |
| duplicates_index | Indicates if this unique constraint duplicates an index with this name |

   attribute [sqlalchemy.engine.interfaces.ReflectedUniqueConstraint.](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)column_names: List[str]

column names which comprise the unique constraint

    attribute [sqlalchemy.engine.interfaces.ReflectedUniqueConstraint.](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)dialect_options: NotRequired[Dict[str, Any]]

Additional dialect-specific options detected for this unique
constraint

    attribute [sqlalchemy.engine.interfaces.ReflectedUniqueConstraint.](#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)duplicates_index: NotRequired[str | None]

Indicates if this unique constraint duplicates an index with this name

     class sqlalchemy.engine.interfaces.ReflectedTableComment

*inherits from* `builtins.dict`

Dictionary representing the reflected comment corresponding to
the `Table.comment` attribute.

The [ReflectedTableComment](#sqlalchemy.engine.interfaces.ReflectedTableComment) structure is returned by the
[Inspector.get_table_comment()](#sqlalchemy.engine.reflection.Inspector.get_table_comment) method.

| Member Name | Description |
| --- | --- |
| text | text of the comment |

   attribute [sqlalchemy.engine.interfaces.ReflectedTableComment.](#sqlalchemy.engine.interfaces.ReflectedTableComment)text: str | None

text of the comment

## Reflecting with Database-Agnostic Types

When the columns of a table are reflected, using either the
[Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with) parameter of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or
the [Inspector.get_columns()](#sqlalchemy.engine.reflection.Inspector.get_columns) method of
[Inspector](#sqlalchemy.engine.reflection.Inspector), the datatypes will be as specific as possible
to the target database.   This means that if an “integer” datatype is reflected
from a MySQL database, the type will be represented by the
[sqlalchemy.dialects.mysql.INTEGER](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.INTEGER) class, which includes MySQL-specific
attributes such as “display_width”.   Or on PostgreSQL, a PostgreSQL-specific
datatype such as [sqlalchemy.dialects.postgresql.INTERVAL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.INTERVAL) or
[sqlalchemy.dialects.postgresql.ENUM](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.ENUM) may be returned.

There is a use case for reflection which is that a given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
is to be transferred to a different vendor database.   To suit this use case,
there is a technique by which these vendor-specific datatypes can be converted
on the fly to be instance of SQLAlchemy backend-agnostic datatypes, for
the examples above types such as [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer), [Interval](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Interval)
and [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum).   This may be achieved by intercepting the
column reflection using the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event
in conjunction with the [TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic) method.

Given a table in MySQL (chosen because MySQL has a lot of vendor-specific
datatypes and options):

```
CREATE TABLE IF NOT EXISTS my_table (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    data1 VARCHAR(50) CHARACTER SET latin1,
    data2 MEDIUMINT(4),
    data3 TINYINT(2)
)
```

The above table includes MySQL-only integer types `MEDIUMINT` and
`TINYINT` as well as a `VARCHAR` that includes the MySQL-only `CHARACTER
SET` option.   If we reflect this table normally, it produces a
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object that will contain those MySQL-specific datatypes
and options:

```
>>> from sqlalchemy import MetaData, Table, create_engine
>>> mysql_engine = create_engine("mysql+mysqldb://scott:tiger@localhost/test")
>>> metadata_obj = MetaData()
>>> my_mysql_table = Table("my_table", metadata_obj, autoload_with=mysql_engine)
```

The above example reflects the above table schema into a new [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object.  We can then, for demonstration purposes, print out the MySQL-specific
“CREATE TABLE” statement using the [CreateTable](https://docs.sqlalchemy.org/en/20/core/ddl.html#sqlalchemy.schema.CreateTable) construct:

```
>>> from sqlalchemy.schema import CreateTable
>>> print(CreateTable(my_mysql_table).compile(mysql_engine))
CREATE TABLE my_table (
id INTEGER(11) NOT NULL AUTO_INCREMENT,
data1 VARCHAR(50) CHARACTER SET latin1,
data2 MEDIUMINT(4),
data3 TINYINT(2),
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

Above, the MySQL-specific datatypes and options were maintained.   If we wanted
a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that we could instead transfer cleanly to another
database vendor, replacing the special datatypes
[sqlalchemy.dialects.mysql.MEDIUMINT](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.MEDIUMINT) and
[sqlalchemy.dialects.mysql.TINYINT](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#sqlalchemy.dialects.mysql.TINYINT) with [Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer), we can
choose instead to “genericize” the datatypes on this table, or otherwise change
them in any way we’d like, by establishing a handler using the
[DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect) event.  The custom handler will make use
of the [TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic) method to convert the above
MySQL-specific type objects into generic ones, by replacing the `"type"`
entry within the column dictionary entry that is passed to the event handler.
The format of this dictionary is described at [Inspector.get_columns()](#sqlalchemy.engine.reflection.Inspector.get_columns):

```
>>> from sqlalchemy import event
>>> metadata_obj = MetaData()

>>> @event.listens_for(metadata_obj, "column_reflect")
... def genericize_datatypes(inspector, tablename, column_dict):
...     column_dict["type"] = column_dict["type"].as_generic()

>>> my_generic_table = Table("my_table", metadata_obj, autoload_with=mysql_engine)
```

We now get a new [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that is generic and uses
[Integer](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer) for those datatypes.  We can now emit a
“CREATE TABLE” statement for example on a PostgreSQL database:

```
>>> pg_engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/test", echo=True)
>>> my_generic_table.create(pg_engine)
CREATE TABLE my_table (
    id SERIAL NOT NULL,
    data1 VARCHAR(50),
    data2 INTEGER,
    data3 INTEGER,
    PRIMARY KEY (id)
)
```

Noting above also that SQLAlchemy will usually make a decent guess for other
behaviors, such as that the MySQL `AUTO_INCREMENT` directive is represented
in PostgreSQL most closely using the `SERIAL` auto-incrementing datatype.

Added in version 1.4: Added the [TypeEngine.as_generic()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.as_generic) method
and additionally improved the use of the [DDLEvents.column_reflect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.DDLEvents.column_reflect)
event such that it may be applied to a [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) object
for convenience.

## Limitations of Reflection

It’s important to note that the reflection process recreates [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
metadata using only information which is represented in the relational database.
This process by definition cannot restore aspects of a schema that aren’t
actually stored in the database.   State which is not available from reflection
includes but is not limited to:

- Client side defaults, either Python functions or SQL expressions defined using
  the `default` keyword of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) (note this is separate from `server_default`,
  which specifically is what’s available via reflection).
- Column information, e.g. data that might have been placed into the
  [Column.info](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.info) dictionary
- The value of the `.quote` setting for [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
- The association of a particular [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) with a given [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)

The relational database also in many cases reports on table metadata in a
different format than what was specified in SQLAlchemy.   The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects returned from reflection cannot be always relied upon to produce the identical
DDL as the original Python-defined [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects.   Areas where
this occurs includes server defaults, column-associated sequences and various
idiosyncrasies regarding constraints and datatypes.   Server side defaults may
be returned with cast directives (typically PostgreSQL will include a `::<type>`
cast) or different quoting patterns than originally specified.

Another category of limitation includes schema structures for which reflection
is only partially or not yet defined.  Recent improvements to reflection allow
things like views, indexes and foreign key options to be reflected.  As of this
writing, structures like CHECK constraints, table comments, and triggers are
not reflected.
