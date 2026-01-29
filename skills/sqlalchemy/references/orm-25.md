# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Additional Persistence Techniques

## Embedding SQL Insert/Update Expressions into a Flush

This feature allows the value of a database column to be set to a SQL
expression instead of a literal value. It’s especially useful for atomic
updates, calling stored procedures, etc. All you do is assign an expression to
an attribute:

```
class SomeClass(Base):
    __tablename__ = "some_table"

    # ...

    value = mapped_column(Integer)

someobject = session.get(SomeClass, 5)

# set 'value' attribute to a SQL expression adding one
someobject.value = SomeClass.value + 1

# issues "UPDATE some_table SET value=value+1"
session.commit()
```

This technique works both for INSERT and UPDATE statements. After the
flush/commit operation, the `value` attribute on `someobject` above is
expired, so that when next accessed the newly generated value will be loaded
from the database.

The feature also has conditional support to work in conjunction with
primary key columns.  For backends that have RETURNING support
(including Oracle Database, SQL Server, MariaDB 10.5, SQLite 3.35) a
SQL expression may be assigned to a primary key column as well.  This allows
both the SQL expression to be evaluated, as well as allows any server side
triggers that modify the primary key value on INSERT, to be successfully
retrieved by the ORM as part of the object’s primary key:

```
class Foo(Base):
    __tablename__ = "foo"
    pk = mapped_column(Integer, primary_key=True)
    bar = mapped_column(Integer)

e = create_engine("postgresql+psycopg2://scott:tiger@localhost/test", echo=True)
Base.metadata.create_all(e)

session = Session(e)

foo = Foo(pk=sql.select(sql.func.coalesce(sql.func.max(Foo.pk) + 1, 1)))
session.add(foo)
session.commit()
```

On PostgreSQL, the above [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will emit the following INSERT:

```
INSERT INTO foo (foopk, bar) VALUES
((SELECT coalesce(max(foo.foopk) + %(max_1)s, %(coalesce_2)s) AS coalesce_1
FROM foo), %(bar)s) RETURNING foo.foopk
```

Added in version 1.3: SQL expressions can now be passed to a primary key column during an ORM
flush; if the database supports RETURNING, or if pysqlite is in use, the
ORM will be able to retrieve the server-generated value as the value
of the primary key attribute.

## Using SQL Expressions with Sessions

SQL expressions and strings can be executed via the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) within its transactional context.
This is most easily accomplished using the
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method, which returns a
[CursorResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult) in the same manner as an
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection):

```
Session = sessionmaker(bind=engine)
session = Session()

# execute a string statement
result = session.execute(text("select * from table where id=:id"), {"id": 7})

# execute a SQL expression construct
result = session.execute(select(mytable).where(mytable.c.id == 7))
```

The current [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) held by the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is accessible using the
[Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) method:

```
connection = session.connection()
```

The examples above deal with a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) that’s
bound to a single [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or
[Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection). To execute statements using a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) which is bound either to multiple
engines, or none at all (i.e. relies upon bound metadata), both
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) and
[Session.connection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.connection) accept a dictionary of bind arguments
[Session.execute.bind_arguments](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.bind_arguments) which may include “mapper”
which is passed a mapped class or
[Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) instance, which is used to locate the
proper context for the desired engine:

```
Session = sessionmaker()
session = Session()

# need to specify mapper or class when executing
result = session.execute(
    text("select * from table where id=:id"),
    {"id": 7},
    bind_arguments={"mapper": MyMappedClass},
)

result = session.execute(
    select(mytable).where(mytable.c.id == 7), bind_arguments={"mapper": MyMappedClass}
)

connection = session.connection(MyMappedClass)
```

Changed in version 1.4: the `mapper` and `clause` arguments to
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) are now passed as part of a dictionary
sent as the [Session.execute.bind_arguments](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.bind_arguments) parameter.
The previous arguments are still accepted however this usage is
deprecated.

## Forcing NULL on a column with a default

The ORM considers any attribute that was never set on an object as a
“default” case; the attribute will be omitted from the INSERT statement:

```
class MyObject(Base):
    __tablename__ = "my_table"
    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(String(50), nullable=True)

obj = MyObject(id=1)
session.add(obj)
session.commit()  # INSERT with the 'data' column omitted; the database
# itself will persist this as the NULL value
```

Omitting a column from the INSERT means that the column will
have the NULL value set, *unless* the column has a default set up,
in which case the default value will be persisted.   This holds true
both from a pure SQL perspective with server-side defaults, as well as the
behavior of SQLAlchemy’s insert behavior with both client-side and server-side
defaults:

```
class MyObject(Base):
    __tablename__ = "my_table"
    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(String(50), nullable=True, server_default="default")

obj = MyObject(id=1)
session.add(obj)
session.commit()  # INSERT with the 'data' column omitted; the database
# itself will persist this as the value 'default'
```

However, in the ORM, even if one assigns the Python value `None` explicitly
to the object, this is treated the **same** as though the value were never
assigned:

```
class MyObject(Base):
    __tablename__ = "my_table"
    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(String(50), nullable=True, server_default="default")

obj = MyObject(id=1, data=None)
session.add(obj)
session.commit()  # INSERT with the 'data' column explicitly set to None;
# the ORM still omits it from the statement and the
# database will still persist this as the value 'default'
```

The above operation will persist into the `data` column the
server default value of `"default"` and not SQL NULL, even though `None`
was passed; this is a long-standing behavior of the ORM that many applications
hold as an assumption.

So what if we want to actually put NULL into this column, even though the
column has a default value?  There are two approaches.  One is that
on a per-instance level, we assign the attribute using the
[null](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) SQL construct:

```
from sqlalchemy import null

obj = MyObject(id=1, data=null())
session.add(obj)
session.commit()  # INSERT with the 'data' column explicitly set as null();
# the ORM uses this directly, bypassing all client-
# and server-side defaults, and the database will
# persist this as the NULL value
```

The [null](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.null) SQL construct always translates into the SQL
NULL value being directly present in the target INSERT statement.

If we’d like to be able to use the Python value `None` and have this
also be persisted as NULL despite the presence of column defaults,
we can configure this for the ORM using a Core-level modifier
[TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none), which indicates
a type where the ORM should treat the value `None` the same as any other
value and pass it through, rather than omitting it as a “missing” value:

```
class MyObject(Base):
    __tablename__ = "my_table"
    id = mapped_column(Integer, primary_key=True)
    data = mapped_column(
        String(50).evaluates_none(),  # indicate that None should always be passed
        nullable=True,
        server_default="default",
    )

obj = MyObject(id=1, data=None)
session.add(obj)
session.commit()  # INSERT with the 'data' column explicitly set to None;
# the ORM uses this directly, bypassing all client-
# and server-side defaults, and the database will
# persist this as the NULL value
```

Evaluating None

The [TypeEngine.evaluates_none()](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.evaluates_none) modifier is primarily intended to
signal a type where the Python value “None” is significant, the primary
example being a JSON type which may want to persist the JSON `null` value
rather than SQL NULL.  We are slightly repurposing it here in order to
signal to the ORM that we’d like `None` to be passed into the type whenever
present, even though no special type-level behaviors are assigned to it.

## Fetching Server-Generated Defaults

As introduced in the sections [Server-invoked DDL-Explicit Default Expressions](https://docs.sqlalchemy.org/en/20/core/defaults.html#server-defaults) and [Marking Implicitly Generated Values, timestamps, and Triggered Columns](https://docs.sqlalchemy.org/en/20/core/defaults.html#triggered-columns),
the Core supports the notion of database columns for which the database
itself generates a value upon INSERT and in less common cases upon UPDATE
statements.  The ORM features support for such columns regarding being
able to fetch these newly generated values upon flush.   This behavior is
required in the case of primary key columns that are generated by the server,
since the ORM has to know the primary key of an object once it is persisted.

In the vast majority of cases, primary key columns that have their value
generated automatically by the database are  simple integer columns, which are
implemented by the database as either a so-called “autoincrement” column, or
from a sequence associated with the column.   Every database dialect within
SQLAlchemy Core supports a method of retrieving these primary key values which
is often native to the Python DBAPI, and in general this process is automatic.
There is more documentation regarding this at
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement).

For server-generating columns that are not primary key columns or that are not
simple autoincrementing integer columns, the ORM requires that these columns
are marked with an appropriate `server_default` directive that allows the ORM to
retrieve this value.   Not all methods are supported on all backends, however,
so care must be taken to use the appropriate method. The two questions to be
answered are, 1. is this column part of the primary key or not, and 2. does the
database support RETURNING or an equivalent, such as “OUTPUT inserted”; these
are SQL phrases which return a server-generated value at the same time as the
INSERT or UPDATE statement is invoked.   RETURNING is currently supported
by PostgreSQL, Oracle Database, MariaDB 10.5, SQLite 3.35, and SQL Server.

### Case 1: non primary key, RETURNING or equivalent is supported

In this case, columns should be marked as [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) or with an
explicit [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default).   The ORM will
automatically add these columns to the RETURNING clause when performing
INSERT statements, assuming the
[Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) parameter is set to `True`, or
if left at its default setting of `"auto"`, for dialects that support
both RETURNING as well as [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues):

```
class MyModel(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)

    # server-side SQL date function generates a new timestamp
    timestamp = mapped_column(DateTime(), server_default=func.now())

    # some other server-side function not named here, such as a trigger,
    # populates a value into this column during INSERT
    special_identifier = mapped_column(String(50), server_default=FetchedValue())

    # set eager defaults to True.  This is usually optional, as if the
    # backend supports RETURNING + insertmanyvalues, eager defaults
    # will take place regardless on INSERT
    __mapper_args__ = {"eager_defaults": True}
```

Above, an INSERT statement that does not specify explicit values for
“timestamp” or “special_identifier” from the client side will include the
“timestamp” and “special_identifier” columns within the RETURNING clause so
they are available immediately. On the PostgreSQL database, an INSERT for the
above table will look like:

```
INSERT INTO my_table DEFAULT VALUES RETURNING my_table.id, my_table.timestamp, my_table.special_identifier
```

Changed in version 2.0.0rc1: The [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) parameter now defaults
to a new setting `"auto"`, which will automatically make use of RETURNING
to fetch server-generated default values on INSERT if the backing database
supports both RETURNING as well as [insertmanyvalues](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues).

Note

The `"auto"` value for [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) only
applies to INSERT statements.  UPDATE statements will not use RETURNING,
even if available, unless [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) is set to
`True`.  This is because there is no equivalent “insertmanyvalues” feature
for UPDATE, so UPDATE RETURNING will require that UPDATE statements are
emitted individually for each row being UPDATEd.

### Case 2: Table includes trigger-generated values which are not compatible with RETURNING

The `"auto"` setting of [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) means that
a backend that supports RETURNING will usually make use of RETURNING with
INSERT statements in order to retrieve newly generated default values.
However there are limitations of server-generated values that are generated
using triggers, such that RETURNING can’t be used:

- SQL Server does not allow RETURNING to be used in an INSERT statement
  to retrieve a trigger-generated value; the statement will fail.
- SQLite has limitations in combining the use of RETURNING with triggers, such
  that the RETURNING clause will not have the INSERTed value available
- Other backends may have limitations with RETURNING in conjunction with
  triggers, or other kinds of server-generated values.

To disable the use of RETURNING for such values, including not just for
server generated default values but also to ensure that the ORM will never
use RETURNING with a particular table, specify
[Table.implicit_returning](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.implicit_returning)
as `False` for the mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).  Using a Declarative mapping
this looks like:

```
class MyModel(Base):
    __tablename__ = "my_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column(String(50))

    # assume a database trigger populates a value into this column
    # during INSERT
    special_identifier = mapped_column(String(50), server_default=FetchedValue())

    # disable all use of RETURNING for the table
    __table_args__ = {"implicit_returning": False}
```

On SQL Server with the pyodbc driver, an INSERT for the above table will
not use RETURNING and will use the SQL Server `scope_identity()` function
to retrieve the newly generated primary key value:

```
INSERT INTO my_table (data) VALUES (?); select scope_identity()
```

See also

[INSERT behavior](https://docs.sqlalchemy.org/en/20/dialects/mssql.html#mssql-insert-behavior) - background on the SQL Server dialect’s
methods of fetching newly generated primary key values

### Case 3: non primary key, RETURNING or equivalent is not supported or not needed

This case is the same as case 1 above, except we typically don’t want to
use [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults), as its current implementation
in the absence of RETURNING support is to emit a SELECT-per-row, which
is not performant.  Therefore the parameter is omitted in the mapping below:

```
class MyModel(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)
    timestamp = mapped_column(DateTime(), server_default=func.now())

    # assume a database trigger populates a value into this column
    # during INSERT
    special_identifier = mapped_column(String(50), server_default=FetchedValue())
```

After a record with the above mapping is INSERTed on a backend that does not
include RETURNING or “insertmanyvalues” support, the “timestamp” and
“special_identifier” columns will remain empty, and will be fetched via a
second SELECT statement when they are first accessed after the flush, e.g. they
are marked as “expired”.

If the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) is explicitly provided with a
value of `True`, and the backend database does not support RETURNING or an
equivalent, the ORM will emit a SELECT statement immediately following the
INSERT statement in order to fetch newly generated values; the ORM does not
currently have the ability to SELECT many newly inserted rows in batch if
RETURNING was not available. This is usually undesirable as it adds additional
SELECT statements to the flush process that may not be needed. Using the above
mapping with the [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) flag set to True
against MySQL (not MariaDB) results in SQL like this upon flush:

```
INSERT INTO my_table () VALUES ()

-- when eager_defaults **is** used, but RETURNING is not supported
SELECT my_table.timestamp AS my_table_timestamp, my_table.special_identifier AS my_table_special_identifier
FROM my_table WHERE my_table.id = %s
```

A future release of SQLAlchemy may seek to improve the efficiency of
eager defaults in the absence of RETURNING to batch many rows within a
single SELECT statement.

### Case 4: primary key, RETURNING or equivalent is supported

A primary key column with a server-generated value must be fetched immediately
upon INSERT; the ORM can only access rows for which it has a primary key value,
so if the primary key is generated by the server, the ORM needs a way
to retrieve that new value immediately upon INSERT.

As mentioned above, for integer “autoincrement” columns, as well as
columns marked with [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity) and special constructs such as
PostgreSQL SERIAL, these types are handled automatically by the Core; databases
include functions for fetching the “last inserted id” where RETURNING
is not supported, and where RETURNING is supported SQLAlchemy will use that.

For example, using Oracle Database with a column marked as [Identity](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Identity),
RETURNING is used automatically to fetch the new primary key value:

```
class MyOracleModel(Base):
    __tablename__ = "my_table"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    data: Mapped[str] = mapped_column(String(50))
```

The INSERT for a model as above on Oracle Database looks like:

```
INSERT INTO my_table (data) VALUES (:data) RETURNING my_table.id INTO :ret_0
```

SQLAlchemy renders an INSERT for the “data” field, but only includes “id” in
the RETURNING clause, so that server-side generation for “id” will take
place and the new value will be returned immediately.

For non-integer values generated by server side functions or triggers, as well
as for integer values that come from constructs outside the table itself,
including explicit sequences and triggers, the server default generation must
be marked in the table metadata. Using Oracle Database as the example again, we can
illustrate a similar table as above naming an explicit sequence using the
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) construct:

```
class MyOracleModel(Base):
    __tablename__ = "my_table"

    id: Mapped[int] = mapped_column(Sequence("my_oracle_seq"), primary_key=True)
    data: Mapped[str] = mapped_column(String(50))
```

An INSERT for this version of the model on Oracle Database would look like:

```
INSERT INTO my_table (id, data) VALUES (my_oracle_seq.nextval, :data) RETURNING my_table.id INTO :ret_0
```

Where above, SQLAlchemy renders `my_sequence.nextval` for the primary key
column so that it is used for new primary key generation, and also uses
RETURNING to get the new value back immediately.

If the source of data is not represented by a simple SQL function or
[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), such as when using triggers or database-specific datatypes
that produce new values, the presence of a value-generating default may be
indicated by using [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) within the column definition. Below
is a model that uses a SQL Server TIMESTAMP column as the primary key; on SQL
Server, this datatype generates new values automatically, so this is indicated
in the table metadata by indicating [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) for the
[Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) parameter:

```
class MySQLServerModel(Base):
    __tablename__ = "my_table"

    timestamp: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(), server_default=FetchedValue(), primary_key=True
    )
    data: Mapped[str] = mapped_column(String(50))
```

An INSERT for the above table on SQL Server looks like:

```
INSERT INTO my_table (data) OUTPUT inserted.timestamp VALUES (?)
```

### Case 5: primary key, RETURNING or equivalent is not supported

In this area we are generating rows for a database such as MySQL
where some means of generating a default is occurring on the server, but is
outside of the database’s usual autoincrement routine. In this case, we have to
make sure SQLAlchemy can “pre-execute” the default, which means it has to be an
explicit SQL expression.

Note

This section will illustrate multiple recipes involving
datetime values for MySQL, since the datetime datatypes on this
backend has additional idiosyncratic requirements that are useful to
illustrate.  Keep in mind however that MySQL requires an explicit
“pre-executed” default generator for *any* auto-generated datatype used as
the primary key other than the usual single-column autoincrementing integer
value.

#### MySQL with DateTime primary key

Using the example of a [DateTime](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.DateTime) column for MySQL, we add an explicit
pre-execute-supported default using the “NOW()” SQL function:

```
class MyModel(Base):
    __tablename__ = "my_table"

    timestamp = mapped_column(DateTime(), default=func.now(), primary_key=True)
```

Where above, we select the “NOW()” function to deliver a datetime value
to the column.  The SQL generated by the above is:

```
SELECT now() AS anon_1
INSERT INTO my_table (timestamp) VALUES (%s)
('2018-08-09 13:08:46',)
```

#### MySQL with TIMESTAMP primary key

When using the [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP) datatype with MySQL, MySQL ordinarily
associates a server-side default with this datatype automatically.  However
when we use one as a primary key, the Core cannot retrieve the newly generated
value unless we execute the function ourselves.  As [TIMESTAMP](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.TIMESTAMP) on
MySQL actually stores a binary value, we need to add an additional “CAST” to our
usage of “NOW()” so that we retrieve a binary value that can be persisted
into the column:

```
from sqlalchemy import cast, Binary

class MyModel(Base):
    __tablename__ = "my_table"

    timestamp = mapped_column(
        TIMESTAMP(), default=cast(func.now(), Binary), primary_key=True
    )
```

Above, in addition to selecting the “NOW()” function, we additionally make
use of the `Binary` datatype in conjunction with [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast) so that
the returned value is binary.  SQL rendered from the above within an
INSERT looks like:

```
SELECT CAST(now() AS BINARY) AS anon_1
INSERT INTO my_table (timestamp) VALUES (%s)
(b'2018-08-09 13:08:46',)
```

See also

[Column INSERT/UPDATE Defaults](https://docs.sqlalchemy.org/en/20/core/defaults.html)

### Notes on eagerly fetching client invoked SQL expressions used for INSERT or UPDATE

The preceding examples indicate the use of [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default)
to create tables that include default-generation functions within their
DDL.

SQLAlchemy also supports non-DDL server side defaults, as documented at
[Client-Invoked SQL Expressions](https://docs.sqlalchemy.org/en/20/core/defaults.html#defaults-client-invoked-sql); these “client invoked SQL expressions”
are set up using the [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate) parameters.

These SQL expressions currently are subject to the same limitations within the
ORM as occurs for true server-side defaults; they won’t be eagerly fetched with
RETURNING when [Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) is set to `"auto"` or
`True` unless the [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) directive is associated with the
[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), even though these expressions are not DDL server
defaults and are actively rendered by SQLAlchemy itself. This limitation may be
addressed in future SQLAlchemy releases.

The [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue) construct can be applied to
[Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) or
[Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) at the same time that a SQL
expression is used with [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate), such as in the example below where the
`func.now()` construct is used as a client-invoked SQL expression
for [Column.default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.default) and
[Column.onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.onupdate).  In order for the behavior of
[Mapper.eager_defaults](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.eager_defaults) to include that it fetches these
values using RETURNING when available, [Column.server_default](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default) and
[Column.server_onupdate](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_onupdate) are used with [FetchedValue](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.FetchedValue)
to ensure that the fetch occurs:

```
class MyModel(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)

    created = mapped_column(
        DateTime(), default=func.now(), server_default=FetchedValue()
    )
    updated = mapped_column(
        DateTime(),
        onupdate=func.now(),
        server_default=FetchedValue(),
        server_onupdate=FetchedValue(),
    )

    __mapper_args__ = {"eager_defaults": True}
```

With a mapping similar to the above, the SQL rendered by the ORM for
INSERT and UPDATE will include `created` and `updated` in the RETURNING
clause:

```
INSERT INTO my_table (created) VALUES (now()) RETURNING my_table.id, my_table.created, my_table.updated

UPDATE my_table SET updated=now() WHERE my_table.id = %(my_table_id)s RETURNING my_table.updated
```

## Using INSERT, UPDATE and ON CONFLICT (i.e. upsert) to return ORM Objects

SQLAlchemy 2.0 includes enhanced capabilities for emitting several varieties
of ORM-enabled INSERT, UPDATE, and upsert statements.  See the
document at [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html) for documentation.  For upsert, see
[ORM “upsert” Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert).

### Using PostgreSQL ON CONFLICT with RETURNING to return upserted ORM objects

This section has moved to [ORM “upsert” Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-upsert).

## Partitioning Strategies (e.g. multiple database backends per Session)

### Simple Vertical Partitioning

Vertical partitioning places different classes, class hierarchies,
or mapped tables, across multiple databases, by configuring the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with the [Session.binds](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.binds) argument. This
argument receives a dictionary that contains any combination of
ORM-mapped classes, arbitrary classes within a mapped hierarchy (such
as declarative base classes or mixins), [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects,
and [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) objects as keys, which then refer typically to
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or less typically [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) objects as targets.
The dictionary is consulted whenever the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) needs to
emit SQL on behalf of a particular kind of mapped class in order to locate
the appropriate source of database connectivity:

```
engine1 = create_engine("postgresql+psycopg2://db1")
engine2 = create_engine("postgresql+psycopg2://db2")

Session = sessionmaker()

# bind User operations to engine 1, Account operations to engine 2
Session.configure(binds={User: engine1, Account: engine2})

session = Session()
```

Above, SQL operations against either class will make usage of the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
linked to that class.     The functionality is comprehensive across both
read and write operations; a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that is against entities
mapped to `engine1` (determined by looking at the first entity in the
list of items requested) will make use of `engine1` to run the query.   A
flush operation will make use of **both** engines on a per-class basis as it
flushes objects of type `User` and `Account`.

In the more common case, there are typically base or mixin classes that  can be
used to distinguish between operations that are destined for different database
connections.  The [Session.binds](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.binds) argument can accommodate any
arbitrary Python class as a key, which will be used if it is found to be in the
`__mro__` (Python method resolution order) for a particular  mapped class.
Supposing two declarative bases are representing two different database
connections:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

class BaseA(DeclarativeBase):
    pass

class BaseB(DeclarativeBase):
    pass

class User(BaseA): ...

class Address(BaseA): ...

class GameInfo(BaseB): ...

class GameStats(BaseB): ...

Session = sessionmaker()

# all User/Address operations will be on engine 1, all
# Game operations will be on engine 2
Session.configure(binds={BaseA: engine1, BaseB: engine2})
```

Above, classes which descend from `BaseA` and `BaseB` will have their
SQL operations routed to one of two engines based on which superclass
they descend from, if any.   In the case of a class that descends from more
than one “bound” superclass, the superclass that is highest in the target
class’ hierarchy will be chosen to represent which engine should be used.

See also

[Session.binds](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.binds)

### Coordination of Transactions for a multiple-engine Session

One caveat to using multiple bound engines is in the case where a commit
operation may fail on one backend after the commit has succeeded on another.
This is an inconsistency problem that in relational databases is solved
using a “two phase transaction”, which adds an additional “prepare” step
to the commit sequence that allows for multiple databases to agree to commit
before actually completing the transaction.

Due to limited support within DBAPIs,  SQLAlchemy has limited support for two-
phase transactions across backends.  Most typically, it is known to work well
with the PostgreSQL backend and to  a lesser extent with the MySQL backend.
However, the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is fully capable of taking advantage of the two
phase transaction feature when the backend supports it, by setting the
[Session.use_twophase](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.use_twophase) flag within [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) or
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  See [Enabling Two-Phase Commit](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-twophase) for an example.

### Custom Vertical Partitioning

More comprehensive rule-based class-level partitioning can be built by
overriding the [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) method.   Below we illustrate
a custom [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) which delivers the following rules:

1. Flush operations, as well as bulk “update” and “delete” operations,
  are delivered to the engine named `leader`.
2. Operations on objects that subclass `MyOtherClass` all
  occur on the `other` engine.
3. Read operations for all other classes occur on a random
  choice of the `follower1` or `follower2` database.

```
engines = {
    "leader": create_engine("sqlite:///leader.db"),
    "other": create_engine("sqlite:///other.db"),
    "follower1": create_engine("sqlite:///follower1.db"),
    "follower2": create_engine("sqlite:///follower2.db"),
}

from sqlalchemy.sql import Update, Delete
from sqlalchemy.orm import Session, sessionmaker
import random

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None):
        if mapper and issubclass(mapper.class_, MyOtherClass):
            return engines["other"]
        elif self._flushing or isinstance(clause, (Update, Delete)):
            # NOTE: this is for example, however in practice reader/writer
            # splits are likely more straightforward by using two distinct
            # Sessions at the top of a "reader" or "writer" operation.
            # See note below
            return engines["leader"]
        else:
            return engines[random.choice(["follower1", "follower2"])]
```

The above [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class is plugged in using the `class_`
argument to [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker):

```
Session = sessionmaker(class_=RoutingSession)
```

This approach can be combined with multiple [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) objects,
using an approach such as that of using the declarative `__abstract__`
keyword, described at [__abstract__](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#declarative-abstract).

Note

While the above example illustrates routing of specific SQL statements
to a so-called “leader” or “follower” database based on whether or not the
statement expects to write data, this is likely not a practical approach,
as it leads to uncoordinated transaction behavior between reading
and writing within the same operation.  In practice, it’s likely best
to construct the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) up front as a “reader” or “writer”
session, based on the overall operation / transaction that’s proceeding.
That way, an operation that will be writing data will also emit its read-queries
within the same transaction scope.  See the example at
[Setting Isolation For A Sessionmaker / Engine Wide](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-transaction-isolation-enginewide) for a recipe that sets up
one [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) for “read only” operations using autocommit
connections, and another for “write” operations which will include DML /
COMMIT.

See also

[Django-style Database Routers in SQLAlchemy](https://techspot.zzzeek.org/2012/01/11/django-style-database-routers-in-sqlalchemy/)  - blog post on a more comprehensive example of [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind)

### Horizontal Partitioning

Horizontal partitioning partitions the rows of a single table (or a set of
tables) across multiple databases.    The SQLAlchemy [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
contains support for this concept, however to use it fully requires that
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) subclasses are used.  A basic version
of these subclasses are available in the [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/extensions/horizontal_shard.html)
ORM extension.   An example of use is at: [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding).

## Bulk Operations

Legacy Feature

SQLAlchemy 2.0 has integrated the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) “bulk insert” and
“bulk update” capabilities into 2.0 style [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute)
method, making direct use of [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) and [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)
constructs. See the document at [ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html) for documentation,
including [Legacy Session Bulk INSERT Methods](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-legacy-bulk-insert) which illustrates migration
from the older methods to the new methods.
