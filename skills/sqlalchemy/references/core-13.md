# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Core Internals

Some key internal constructs are listed here.

| Object Name | Description |
| --- | --- |
| AdaptedConnection | Interface of an adapted connection object to support the DBAPI protocol. |
| BindTyping | Define different methods of passing typing information for
bound parameters in a statement to the database driver. |
| Compiled | Represent a compiled SQL or DDL expression. |
| DBAPIConnection | protocol representing aPEP 249database connection. |
| DBAPICursor | protocol representing aPEP 249database cursor. |
| DBAPIType | protocol representing aPEP 249database type. |
| DDLCompiler |  |
| DefaultDialect | Default implementation of Dialect |
| DefaultExecutionContext |  |
| Dialect | Define the behavior of a specific database and DB-API combination. |
| ExecutionContext | A messenger object for a Dialect that corresponds to a single
execution. |
| ExpandedState | represents state to use when producing “expanded” and
“post compile” bound parameters for a statement. |
| GenericTypeCompiler |  |
| Identified |  |
| IdentifierPreparer | Handle quoting and case-folding of identifiers based on options. |
| SQLCompiler | Default implementation ofCompiled. |
| StrSQLCompiler | ASQLCompilersubclass which allows a small selection
of non-standard SQL features to render into a string value. |

   class sqlalchemy.engine.BindTyping

*inherits from* `enum.Enum`

Define different methods of passing typing information for
bound parameters in a statement to the database driver.

Added in version 2.0.

| Member Name | Description |
| --- | --- |
| NONE | No steps are taken to pass typing information to the database driver. |
| RENDER_CASTS | Render casts or other directives in the SQL string. |
| SETINPUTSIZES | Use the pep-249 setinputsizes method. |

   attribute [sqlalchemy.engine.BindTyping.](#sqlalchemy.engine.BindTyping)NONE = 1

No steps are taken to pass typing information to the database driver.

This is the default behavior for databases such as SQLite, MySQL / MariaDB,
SQL Server.

    attribute [sqlalchemy.engine.BindTyping.](#sqlalchemy.engine.BindTyping)RENDER_CASTS = 3

Render casts or other directives in the SQL string.

This method is used for all PostgreSQL dialects, including asyncpg,
pg8000, psycopg, psycopg2.   Dialects which implement this can choose
which kinds of datatypes are explicitly cast in SQL statements and which
aren’t.

When RENDER_CASTS is used, the compiler will invoke the
`SQLCompiler.render_bind_cast()` method for the rendered
string representation of each [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) object whose
dialect-level type sets the [TypeEngine.render_bind_cast](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine.render_bind_cast) attribute.

The `SQLCompiler.render_bind_cast()` is also used to render casts
for one form of “insertmanyvalues” query, when both
`InsertmanyvaluesSentinelOpts.USE_INSERT_FROM_SELECT` and
`InsertmanyvaluesSentinelOpts.RENDER_SELECT_COL_CASTS` are set,
where the casts are applied to the intermediary columns e.g.
“INSERT INTO t (a, b, c) SELECT p0::TYP, p1::TYP, p2::TYP ”
“FROM (VALUES (?, ?), (?, ?), …)”.

Added in version 2.0.10: - `SQLCompiler.render_bind_cast()` is now
used within some elements of the “insertmanyvalues” implementation.

     attribute [sqlalchemy.engine.BindTyping.](#sqlalchemy.engine.BindTyping)SETINPUTSIZES = 2

Use the pep-249 setinputsizes method.

This is only implemented for DBAPIs that support this method and for which
the SQLAlchemy dialect has the appropriate infrastructure for that dialect
set up.  Current dialects include python-oracledb, cx_Oracle as well as
optional support for SQL Server using pyodbc.

When using setinputsizes, dialects also have a means of only using the
method for certain datatypes using include/exclude lists.

When SETINPUTSIZES is used, the [Dialect.do_set_input_sizes()](#sqlalchemy.engine.Dialect.do_set_input_sizes) method
is called for each statement executed which has bound parameters.

     class sqlalchemy.engine.Compiled

Represent a compiled SQL or DDL expression.

The `__str__` method of the `Compiled` object should produce
the actual text of the statement.  `Compiled` objects are
specific to their underlying database dialect, and also may
or may not be specific to the columns referenced within a
particular set of bind parameters.  In no case should the
`Compiled` object be dependent on the actual values of those
bind parameters, even though it may reference those values as
defaults.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newCompiledobject. |
| cache_key | TheCacheKeythat was generated ahead of creating thisCompiledobject. |
| compile_state | OptionalCompileStateobject that maintains additional
state used by the compiler. |
| construct_params() | Return the bind params for this compiled object. |
| dml_compile_state | OptionalCompileStateassigned at the same point that
.isinsert, .isupdate, or .isdelete is assigned. |
| execution_options | Execution options propagated from the statement.   In some cases,
sub-elements of the statement can modify these. |
| state | description of the compiler’s state |
| statement | The statement to compile. |
| string | The string representation of thestatement |

   method [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)__init__(*dialect:Dialect*, *statement:ClauseElement|None*, *schema_translate_map:SchemaTranslateMapType|None=None*, *render_schema_translate:bool=False*, *compile_kwargs:Mapping[str,Any]={}*)

Construct a new [Compiled](#sqlalchemy.engine.Compiled) object.

  Parameters:

- **dialect** – [Dialect](#sqlalchemy.engine.Dialect) to compile against.
- **statement** – [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to be compiled.
- **schema_translate_map** –
  dictionary of schema names to be
  translated when forming the resultant SQL
  See also
  [Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating)
- **compile_kwargs** – additional kwargs that will be
  passed to the initial call to `Compiled.process()`.

      attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)cache_key: [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) | None = None

The [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) that was generated ahead of creating this
[Compiled](#sqlalchemy.engine.Compiled) object.

This is used for routines that need access to the original
[CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) instance generated when the [Compiled](#sqlalchemy.engine.Compiled)
instance was first cached, typically in order to reconcile
the original list of [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with a
per-statement list that’s generated on each call.

    attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)compile_state: CompileState | None = None

Optional `CompileState` object that maintains additional
state used by the compiler.

Major executable objects such as [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert),
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete),
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) will generate this
state when compiled in order to calculate additional information about the
object.   For the top level object that is to be executed, the state can be
stored here where it can also have applicability towards result set
processing.

Added in version 1.4.

     method [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)construct_params(*params:_CoreSingleExecuteParams|None=None*, *extracted_parameters:Sequence[BindParameter[Any]]|None=None*, *escape_names:bool=True*) → _MutableCoreSingleExecuteParams | None

Return the bind params for this compiled object.

  Parameters:

**params** – a dict of string/object pairs whose values will
override bind values compiled in to the
statement.

      attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)dml_compile_state: CompileState | None = None

Optional `CompileState` assigned at the same point that
.isinsert, .isupdate, or .isdelete is assigned.

This will normally be the same object as .compile_state, with the
exception of cases like the `ORMFromStatementCompileState`
object.

Added in version 1.4.40.

     attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)execution_options: _ExecuteOptions = {}

Execution options propagated from the statement.   In some cases,
sub-elements of the statement can modify these.

    property params

Return the bind params for this compiled object.

    property sql_compiler: [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler)

Return a Compiled that is capable of processing SQL expressions.

If this compiler is one, it would likely just return ‘self’.

    attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)state: CompilerState

description of the compiler’s state

    attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)statement: [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) | None = None

The statement to compile.

    attribute [sqlalchemy.engine.Compiled.](#sqlalchemy.engine.Compiled)string: str = ''

The string representation of the `statement`

     class sqlalchemy.engine.interfaces.DBAPIConnection

*inherits from* `typing.Protocol`

protocol representing a [PEP 249](https://peps.python.org/pep-0249/) database connection.

Added in version 2.0.

See also

[Connection Objects](https://www.python.org/dev/peps/pep-0249/#connection-objects)
- in [PEP 249](https://peps.python.org/pep-0249/)

| Member Name | Description |
| --- | --- |
| close() |  |
| commit() |  |
| cursor() |  |
| rollback() |  |

   method [sqlalchemy.engine.interfaces.DBAPIConnection.](#sqlalchemy.engine.interfaces.DBAPIConnection)close() → None    method [sqlalchemy.engine.interfaces.DBAPIConnection.](#sqlalchemy.engine.interfaces.DBAPIConnection)commit() → None    method [sqlalchemy.engine.interfaces.DBAPIConnection.](#sqlalchemy.engine.interfaces.DBAPIConnection)cursor(**args:Any*, ***kwargs:Any*) → [DBAPICursor](#sqlalchemy.engine.interfaces.DBAPICursor)    method [sqlalchemy.engine.interfaces.DBAPIConnection.](#sqlalchemy.engine.interfaces.DBAPIConnection)rollback() → None     class sqlalchemy.engine.interfaces.DBAPICursor

*inherits from* `typing.Protocol`

protocol representing a [PEP 249](https://peps.python.org/pep-0249/) database cursor.

Added in version 2.0.

See also

[Cursor Objects](https://www.python.org/dev/peps/pep-0249/#cursor-objects)
- in [PEP 249](https://peps.python.org/pep-0249/)

| Member Name | Description |
| --- | --- |
| arraysize |  |
| callproc() |  |
| close() |  |
| execute() |  |
| executemany() |  |
| fetchall() |  |
| fetchmany() |  |
| fetchone() |  |
| lastrowid |  |
| nextset() |  |
| setinputsizes() |  |
| setoutputsize() |  |

   attribute [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)arraysize: int    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)callproc(*procname:str*, *parameters:Sequence[Any]=Ellipsis*) → Any    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)close() → None    property description: Sequence[Tuple[str, [DBAPIType](#sqlalchemy.engine.interfaces.DBAPIType), int | None, int | None, int | None, int | None, bool | None]]

The description attribute of the Cursor.

See also

[cursor.description](https://www.python.org/dev/peps/pep-0249/#description)
- in [PEP 249](https://peps.python.org/pep-0249/)

     method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)execute(*operation:Any*, *parameters:Sequence[Any]|Mapping[str,Any]|None=None*) → Any    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)executemany(*operation:Any*, *parameters:Sequence[Sequence[Any]]|Sequence[Mapping[str,Any]]*) → Any    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)fetchall() → Sequence[Any]    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)fetchmany(*size:int=Ellipsis*) → Sequence[Any]    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)fetchone() → Any | None    attribute [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)lastrowid: int    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)nextset() → bool | None    property rowcount: int    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)setinputsizes(*sizes:Sequence[Any]*) → None    method [sqlalchemy.engine.interfaces.DBAPICursor.](#sqlalchemy.engine.interfaces.DBAPICursor)setoutputsize(*size:Any*, *column:Any*) → None     class sqlalchemy.engine.interfaces.DBAPIType

*inherits from* `typing.Protocol`

protocol representing a [PEP 249](https://peps.python.org/pep-0249/) database type.

Added in version 2.0.

See also

[Type Objects](https://www.python.org/dev/peps/pep-0249/#type-objects)
- in [PEP 249](https://peps.python.org/pep-0249/)

     class sqlalchemy.sql.compiler.DDLCompiler

*inherits from* [sqlalchemy.sql.compiler.Compiled](#sqlalchemy.engine.Compiled)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newCompiledobject. |
| cache_key | TheCacheKeythat was generated ahead of creating thisCompiledobject. |
| compile_state | OptionalCompileStateobject that maintains additional
state used by the compiler. |
| construct_params() | Return the bind params for this compiled object. |
| define_constraint_remote_table() | Format the remote table clause of a CREATE CONSTRAINT clause. |
| dml_compile_state | OptionalCompileStateassigned at the same point that
.isinsert, .isupdate, or .isdelete is assigned. |
| execution_options | Execution options propagated from the statement.   In some cases,
sub-elements of the statement can modify these. |
| sql_compiler |  |
| state | description of the compiler’s state |
| statement | The statement to compile. |
| string | The string representation of thestatement |

   method [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)__init__(*dialect:Dialect*, *statement:ClauseElement|None*, *schema_translate_map:SchemaTranslateMapType|None=None*, *render_schema_translate:bool=False*, *compile_kwargs:Mapping[str,Any]={}*)

*inherited from the* `sqlalchemy.sql.compiler.Compiled.__init__` *method of* [Compiled](#sqlalchemy.engine.Compiled)

Construct a new [Compiled](#sqlalchemy.engine.Compiled) object.

  Parameters:

- **dialect** – [Dialect](#sqlalchemy.engine.Dialect) to compile against.
- **statement** – [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to be compiled.
- **schema_translate_map** –
  dictionary of schema names to be
  translated when forming the resultant SQL
  See also
  [Translation of Schema Names](https://docs.sqlalchemy.org/en/20/core/connections.html#schema-translating)
- **compile_kwargs** – additional kwargs that will be
  passed to the initial call to `Compiled.process()`.

      attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)cache_key = None

*inherited from the* `Compiled.cache_key` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

The [CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) that was generated ahead of creating this
[Compiled](#sqlalchemy.engine.Compiled) object.

This is used for routines that need access to the original
[CacheKey](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.CacheKey) instance generated when the [Compiled](#sqlalchemy.engine.Compiled)
instance was first cached, typically in order to reconcile
the original list of [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with a
per-statement list that’s generated on each call.

    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)compile_state = None

*inherited from the* `Compiled.compile_state` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

Optional `CompileState` object that maintains additional
state used by the compiler.

Major executable objects such as [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert),
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete),
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) will generate this
state when compiled in order to calculate additional information about the
object.   For the top level object that is to be executed, the state can be
stored here where it can also have applicability towards result set
processing.

Added in version 1.4.

     method [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)construct_params(*params:_CoreSingleExecuteParams|None=None*, *extracted_parameters:Sequence[BindParameter[Any]]|None=None*, *escape_names:bool=True*) → _MutableCoreSingleExecuteParams | None

Return the bind params for this compiled object.

  Parameters:

**params** – a dict of string/object pairs whose values will
override bind values compiled in to the
statement.

      method [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)define_constraint_remote_table(*constraint*, *table*, *preparer*)

Format the remote table clause of a CREATE CONSTRAINT clause.

    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)dml_compile_state = None

*inherited from the* `Compiled.dml_compile_state` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

Optional `CompileState` assigned at the same point that
.isinsert, .isupdate, or .isdelete is assigned.

This will normally be the same object as .compile_state, with the
exception of cases like the `ORMFromStatementCompileState`
object.

Added in version 1.4.40.

     attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)execution_options = {}

*inherited from the* `Compiled.execution_options` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

Execution options propagated from the statement.   In some cases,
sub-elements of the statement can modify these.

    property params

Return the bind params for this compiled object.

    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)sql_compiler    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)state

description of the compiler’s state

    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)statement = None

*inherited from the* `Compiled.statement` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

The statement to compile.

    attribute [sqlalchemy.sql.compiler.DDLCompiler.](#sqlalchemy.sql.compiler.DDLCompiler)string = ''

*inherited from the* `Compiled.string` *attribute of* [Compiled](#sqlalchemy.engine.Compiled)

The string representation of the `statement`

     class sqlalchemy.engine.default.DefaultDialect

*inherits from* [sqlalchemy.engine.interfaces.Dialect](#sqlalchemy.engine.Dialect)

Default implementation of Dialect

| Member Name | Description |
| --- | --- |
| bind_typing | define a means of passing typing information to the database and/or
driver for bound parameters. |
| colspecs | A dictionary of TypeEngine classes from sqlalchemy.types mapped
to subclasses that are specific to the dialect class.  This
dictionary is class-level only and is not accessed from the
dialect instance itself. |
| connect() | Establish a connection using this dialect’s DBAPI. |
| construct_arguments | Optional set of argument specifiers for various SQLAlchemy
constructs, typically schema items. |
| create_connect_args() | Build DB-API compatible connection arguments. |
| create_xid() | Create a random two-phase transaction ID. |
| cte_follows_insert | target database, when given a CTE with an INSERT statement, needs
the CTE to be below the INSERT |
| dbapi | A reference to the DBAPI module object itself. |
| dbapi_exception_translation_map | A dictionary of names that will contain as values the names of
pep-249 exceptions (“IntegrityError”, “OperationalError”, etc)
keyed to alternate class names, to support the case where a
DBAPI has exception classes that aren’t named as they are
referred to (e.g. IntegrityError = MyException).   In the vast
majority of cases this dictionary is empty. |
| ddl_compiler | alias ofDDLCompiler |
| default_isolation_level | the isolation that is implicitly present on new connections |
| default_metavalue_token | for INSERT… VALUES (DEFAULT) syntax, the token to put in the
parenthesis. |
| default_schema_name | the name of the default schema.  This value is only available for
supporting dialects, and is typically populated during the
initial connection to the database. |
| default_sequence_base | the default value that will be rendered as the “START WITH” portion of
a CREATE SEQUENCE DDL statement. |
| delete_executemany_returning | dialect supports DELETE..RETURNING with executemany. |
| delete_returning | if the dialect supports RETURNING with DELETE |
| delete_returning_multifrom | if the dialect supports RETURNING with DELETE..FROM |
| denormalize_name() | convert the given name to a case insensitive identifier
for the backend if it is an all-lowercase name. |
| detect_autocommit_setting() | Detect the current autocommit setting for a DBAPI connection. |
| div_is_floordiv | target database treats the / division operator as “floor division” |
| do_begin() | Provide an implementation ofconnection.begin(), given a
DB-API connection. |
| do_begin_twophase() | Begin a two phase transaction on the given connection. |
| do_close() | Provide an implementation ofconnection.close(), given a DBAPI
connection. |
| do_commit() | Provide an implementation ofconnection.commit(), given a
DB-API connection. |
| do_commit_twophase() | Commit a two phase transaction on the given connection. |
| do_execute() | Provide an implementation ofcursor.execute(statement,parameters). |
| do_execute_no_params() | Provide an implementation ofcursor.execute(statement). |
| do_executemany() | Provide an implementation ofcursor.executemany(statement,parameters). |
| do_ping() | ping the DBAPI connection and return True if the connection is
usable. |
| do_prepare_twophase() | Prepare a two phase transaction on the given connection. |
| do_recover_twophase() | Recover list of uncommitted prepared two phase transaction
identifiers on the given connection. |
| do_release_savepoint() | Release the named savepoint on a connection. |
| do_rollback() | Provide an implementation ofconnection.rollback(), given
a DB-API connection. |
| do_rollback_to_savepoint() | Rollback a connection to the named savepoint. |
| do_rollback_twophase() | Rollback a two phase transaction on the given connection. |
| do_savepoint() | Create a savepoint with the given name. |
| do_set_input_sizes() | invoke the cursor.setinputsizes() method with appropriate arguments |
| do_terminate() | Provide an implementation ofconnection.close()that tries as
much as possible to not block, given a DBAPI
connection. |
| driver | identifying name for the dialect’s DBAPI |
| engine_config_types | a mapping of string keys that can be in an engine config linked to
type conversion functions. |
| engine_created() | A convenience hook called before returning the finalEngine. |
| exclude_set_input_sizes | set of DBAPI type objects that should be excluded in
automatic cursor.setinputsizes() calls. |
| execute_sequence_format | alias oftuple |
| execution_ctx_cls | alias ofDefaultExecutionContext |
| favor_returning_over_lastrowid | for backends that support both a lastrowid and a RETURNING insert
strategy, favor RETURNING for simple single-int pk inserts. |
| get_async_dialect_cls() | Given a URL, return theDialectthat will be used by
an async engine. |
| get_check_constraints() | Return information about check constraints intable_name. |
| get_columns() | Return information about columns intable_name. |
| get_default_isolation_level() | Given a DBAPI connection, return its isolation level, or
a default isolation level if one cannot be retrieved. |
| get_dialect_cls() | Given a URL, return theDialectthat will be used. |
| get_dialect_pool_class() | return a Pool class to use for a given URL |
| get_driver_connection() | Returns the connection object as returned by the external driver
package. |
| get_foreign_keys() | Return information about foreign_keys intable_name. |
| get_indexes() | Return information about indexes intable_name. |
| get_isolation_level() | Given a DBAPI connection, return its isolation level. |
| get_isolation_level_values() | return a sequence of string isolation level names that are accepted
by this dialect. |
| get_materialized_view_names() | Return a list of all materialized view names available in the
database. |
| get_multi_check_constraints() | Return information about check constraints in all tables
in the givenschema. |
| get_multi_columns() | Return information about columns in all tables in the
givenschema. |
| get_multi_foreign_keys() | Return information about foreign_keys in all tables
in the givenschema. |
| get_multi_indexes() | Return information about indexes in in all tables
in the givenschema. |
| get_multi_pk_constraint() | Return information about primary key constraints in
all tables in the givenschema. |
| get_multi_table_comment() | Return information about the table comment in all tables
in the givenschema. |
| get_multi_table_options() | Return a dictionary of options specified when the tables in the
given schema were created. |
| get_multi_unique_constraints() | Return information about unique constraints in all tables
in the givenschema. |
| get_pk_constraint() | Return information about the primary key constraint on
table_name`. |
| get_schema_names() | Return a list of all schema names available in the database. |
| get_sequence_names() | Return a list of all sequence names available in the database. |
| get_table_comment() | Return the “comment” for the table identified bytable_name. |
| get_table_names() | Return a list of table names forschema. |
| get_table_options() | Return a dictionary of options specified whentable_namewas created. |
| get_temp_table_names() | Return a list of temporary table names on the given connection,
if supported by the underlying backend. |
| get_temp_view_names() | Return a list of temporary view names on the given connection,
if supported by the underlying backend. |
| get_unique_constraints() | Return information about unique constraints intable_name. |
| get_view_definition() | Return plain or materialized view definition. |
| get_view_names() | Return a list of all non-materialized view names available in the
database. |
| has_index() | Check the existence of a particular index name in the database. |
| has_schema() | Check the existence of a particular schema name in the database. |
| has_sequence() | Check the existence of a particular sequence in the database. |
| has_table() | For internal dialect use, check the existence of a particular table
or view in the database. |
| has_terminate | Whether or not this dialect has a separate “terminate” implementation
that does not block or require awaiting. |
| identifier_preparer | This element will refer to an instance ofIdentifierPrepareronce aDefaultDialecthas been constructed. |
| import_dbapi() | Import the DBAPI module that is used by this dialect. |
| include_set_input_sizes | set of DBAPI type objects that should be included in
automatic cursor.setinputsizes() calls. |
| initialize() | Called during strategized creation of the dialect with a
connection. |
| inline_comments | Indicates the dialect supports comment DDL that’s inline with the
definition of a Table or Column.  If False, this implies that ALTER must
be used to set table and column comments. |
| insert_executemany_returning | dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used. |
| insert_executemany_returning_sort_by_parameter_order | dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used
along with theInsert.returning.sort_by_parameter_orderparameter being set. |
| insert_returning | if the dialect supports RETURNING with INSERT |
| insertmanyvalues_implicit_sentinel | Options indicating the database supports a form of bulk INSERT where
the autoincrement integer primary key can be reliably used as an ordering
for INSERTed rows. |
| insertmanyvalues_max_parameters | Alternate to insertmanyvalues_page_size, will additionally limit
page size based on number of parameters total in the statement. |
| insertmanyvalues_page_size | Number of rows to render into an individual INSERT..VALUES() statement
forExecuteStyle.INSERTMANYVALUESexecutions. |
| is_async | Whether or not this dialect is intended for asyncio use. |
| is_disconnect() | Return True if the given DB-API error indicates an invalid
connection |
| label_length | optional user-defined max length for SQL labels |
| load_provisioning() | set up the provision.py module for this dialect. |
| loaded_dbapi |  |
| max_constraint_name_length | The maximum length of constraint names if different frommax_identifier_length. |
| max_identifier_length | The maximum length of identifier names. |
| max_index_name_length | The maximum length of index names if different frommax_identifier_length. |
| name | identifying name for the dialect from a DBAPI-neutral point of view
(i.e. ‘sqlite’) |
| normalize_name() | convert the given name to lowercase if it is detected as
case insensitive. |
| on_connect() | return a callable which sets up a newly created DBAPI connection. |
| on_connect_url() | return a callable which sets up a newly created DBAPI connection. |
| paramstyle | the paramstyle to be used (some DB-APIs support multiple
paramstyles). |
| positional | True if the paramstyle for this Dialect is positional. |
| preexecute_autoincrement_sequences | True if ‘implicit’ primary key functions must be executed separately
in order to get their value, if RETURNING is not used. |
| preparer | alias ofIdentifierPreparer |
| reflection_options | Sequence of string names indicating keyword arguments that can be
established on aTableobject which will be passed as
“reflection options” when usingTable.autoload_with. |
| requires_name_normalize | Indicates symbol names are returned by the database in
UPPERCASED if they are case insensitive within the database.
If this is True, the methods normalize_name()
and denormalize_name() must be provided. |
| reset_isolation_level() | Given a DBAPI connection, revert its isolation to the default. |
| returns_native_bytes | indicates if Python bytes() objects are returned natively by the
driver for SQL “binary” datatypes. |
| sequences_optional | If True, indicates if theSequence.optionalparameter on theSequenceconstruct
should signal to not generate a CREATE SEQUENCE. Applies only to
dialects that support sequences. Currently used only to allow PostgreSQL
SERIAL to be used on a column that specifies Sequence() for usage on
other backends. |
| server_side_cursors | deprecated; indicates if the dialect should attempt to use server
side cursors by default |
| server_version_info | a tuple containing a version number for the DB backend in use. |
| set_connection_execution_options() | Establish execution options for a given connection. |
| set_engine_execution_options() | Establish execution options for a given engine. |
| set_isolation_level() | Given a DBAPI connection, set its isolation level. |
| skip_autocommit_rollback | Whether or not thecreate_engine.skip_autocommit_rollbackparameter was set. |
| statement_compiler | alias ofSQLCompiler |
| supports_alter | Trueif the database supportsALTERTABLE- used only for
generating foreign key constraints in certain circumstances |
| supports_comments | Indicates the dialect supports comment DDL on tables and columns. |
| supports_constraint_comments | Indicates if the dialect supports comment DDL on constraints. |
| supports_default_metavalue | dialect supports INSERT… VALUES (DEFAULT) syntax |
| supports_default_values | dialect supports INSERT… DEFAULT VALUES syntax |
| supports_empty_insert | dialect supports INSERT () VALUES () |
| supports_identity_columns | target database supports IDENTITY |
| supports_multivalues_insert | Target database supports INSERT…VALUES with multiple value
sets, i.e. INSERT INTO table (cols) VALUES (…), (…), (…), … |
| supports_native_boolean | Indicates if the dialect supports a native boolean construct.
This will preventBooleanfrom generating a CHECK
constraint when that type is used. |
| supports_native_decimal | indicates if Decimal objects are handled and returned for precision
numeric types, or if floats are returned |
| supports_native_enum | Indicates if the dialect supports a native ENUM construct.
This will preventEnumfrom generating a CHECK
constraint when that type is used in “native” mode. |
| supports_native_uuid | indicates if Python UUID() objects are handled natively by the
driver for SQL UUID datatypes. |
| supports_sane_multi_rowcount | Indicate whether the dialect properly implements rowcount forUPDATEandDELETEstatements when executed via
executemany. |
| supports_sane_rowcount | Indicate whether the dialect properly implements rowcount forUPDATEandDELETEstatements. |
| supports_sequences | Indicates if the dialect supports CREATE SEQUENCE or similar. |
| supports_server_side_cursors | indicates if the dialect supports server side cursors |
| supports_simple_order_by_label | target database supports ORDER BY <labelname>, where <labelname>
refers to a label in the columns clause of the SELECT |
| supports_statement_cache | indicates if this dialect supports caching. |
| tuple_in_values | target database supports tuple IN, i.e. (x, y) IN ((q, p), (r, z)) |
| type_compiler | legacy; this is a TypeCompiler class at the class level, a
TypeCompiler instance at the instance level. |
| type_compiler_cls | alias ofGenericTypeCompiler |
| type_compiler_instance | instance of aCompiledclass used to compile SQL type
objects |
| type_descriptor() | Provide a database-specificTypeEngineobject, given
the generic object which comes from the types module. |
| update_executemany_returning | dialect supports UPDATE..RETURNING with executemany. |
| update_returning | if the dialect supports RETURNING with UPDATE |
| update_returning_multifrom | if the dialect supports RETURNING with UPDATE..FROM |
| use_insertmanyvalues | if True, indicates “insertmanyvalues” functionality should be used
to allow forinsert_executemany_returningbehavior, if possible. |
| use_insertmanyvalues_wo_returning | if True, and use_insertmanyvalues is also True, INSERT statements
that don’t include RETURNING will also use “insertmanyvalues”. |
| validate_identifier() | Validates an identifier name, raising an exception if invalid |

   attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)bind_typing = 1

define a means of passing typing information to the database and/or
driver for bound parameters.

See [BindTyping](#sqlalchemy.engine.BindTyping) for values.

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)colspecs: MutableMapping[Type[[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]], Type[[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]]] = {}

A dictionary of TypeEngine classes from sqlalchemy.types mapped
to subclasses that are specific to the dialect class.  This
dictionary is class-level only and is not accessed from the
dialect instance itself.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)connect(**cargs:Any*, ***cparams:Any*) → [DBAPIConnection](#sqlalchemy.engine.interfaces.DBAPIConnection)

Establish a connection using this dialect’s DBAPI.

The default implementation of this method is:

```
def connect(self, *cargs, **cparams):
    return self.dbapi.connect(*cargs, **cparams)
```

The `*cargs, **cparams` parameters are generated directly
from this dialect’s [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

This method may be used for dialects that need to perform programmatic
per-connection steps when a new connection is procured from the
DBAPI.

  Parameters:

- ***cargs** – positional parameters returned from the
  [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method
- ****cparams** – keyword parameters returned from the
  [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

  Returns:

a DBAPI connection, typically from the [PEP 249](https://peps.python.org/pep-0249/) module
level `.connect()` function.

See also

[Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args)

[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)construct_arguments = None

*inherited from the* `Dialect.construct_arguments` *attribute of* [Dialect](#sqlalchemy.engine.Dialect)

Optional set of argument specifiers for various SQLAlchemy
constructs, typically schema items.

To implement, establish as a series of tuples, as in:

```
construct_arguments = [
    (schema.Index, {"using": False, "where": None, "ops": None}),
]
```

If the above construct is established on the PostgreSQL dialect,
the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct will now accept the keyword arguments
`postgresql_using`, `postgresql_where`, nad `postgresql_ops`.
Any other argument specified to the constructor of [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
which is prefixed with `postgresql_` will raise [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError).

A dialect which does not include a `construct_arguments` member will
not participate in the argument validation system.  For such a dialect,
any argument name is accepted by all participating constructs, within
the namespace of arguments prefixed with that dialect name.  The rationale
here is so that third-party dialects that haven’t yet implemented this
feature continue to function in the old way.

See also

[DialectKWArgs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs) - implementing base class which consumes
[DefaultDialect.construct_arguments](#sqlalchemy.engine.default.DefaultDialect.construct_arguments)

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)create_connect_args(*url:URL*) → ConnectArgsType

Build DB-API compatible connection arguments.

Given a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object, returns a tuple
consisting of a `(*args, **kwargs)` suitable to send directly
to the dbapi’s connect function.   The arguments are sent to the
[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) method which then runs the DBAPI-level
`connect()` function.

The method typically makes use of the
[URL.translate_connect_args()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.translate_connect_args)
method in order to generate a dictionary of options.

The default implementation is:

```
def create_connect_args(self, url):
    opts = url.translate_connect_args()
    opts.update(url.query)
    return ([], opts)
```

   Parameters:

**url** – a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object

  Returns:

a tuple of `(*args, **kwargs)` which will be passed to the
[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) method.

See also

[URL.translate_connect_args()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.translate_connect_args)

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)create_xid()

Create a random two-phase transaction ID.

This id will be passed to do_begin_twophase(), do_rollback_twophase(),
do_commit_twophase().  Its format is unspecified.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)cte_follows_insert = False

target database, when given a CTE with an INSERT statement, needs
the CTE to be below the INSERT

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)dbapi

A reference to the DBAPI module object itself.

SQLAlchemy dialects import DBAPI modules using the classmethod
[Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi). The rationale is so that any dialect
module can be imported and used to generate SQL statements without the
need for the actual DBAPI driver to be installed.  Only when an
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is constructed using [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) does the
DBAPI get imported; at that point, the creation process will assign
the DBAPI module to this attribute.

Dialects should therefore implement [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi)
which will import the necessary module and return it, and then refer
to `self.dbapi` in dialect code in order to refer to the DBAPI module
contents.

Changed in version The: [Dialect.dbapi](#sqlalchemy.engine.Dialect.dbapi) attribute is exclusively
used as the per-[Dialect](#sqlalchemy.engine.Dialect)-instance reference to the DBAPI
module.   The previous not-fully-documented `.Dialect.dbapi()`
classmethod is deprecated and replaced by [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi).

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)dbapi_exception_translation_map = {}

*inherited from the* `Dialect.dbapi_exception_translation_map` *attribute of* [Dialect](#sqlalchemy.engine.Dialect)

A dictionary of names that will contain as values the names of
pep-249 exceptions (“IntegrityError”, “OperationalError”, etc)
keyed to alternate class names, to support the case where a
DBAPI has exception classes that aren’t named as they are
referred to (e.g. IntegrityError = MyException).   In the vast
majority of cases this dictionary is empty.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)ddl_compiler

alias of [DDLCompiler](#sqlalchemy.sql.compiler.DDLCompiler)

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)default_isolation_level

the isolation that is implicitly present on new connections

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)default_metavalue_token = 'DEFAULT'

for INSERT… VALUES (DEFAULT) syntax, the token to put in the
parenthesis.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)default_schema_name: str | None = None

the name of the default schema.  This value is only available for
supporting dialects, and is typically populated during the
initial connection to the database.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)default_sequence_base = 1

the default value that will be rendered as the “START WITH” portion of
a CREATE SEQUENCE DDL statement.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)delete_executemany_returning = False

dialect supports DELETE..RETURNING with executemany.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)delete_returning = False

if the dialect supports RETURNING with DELETE

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)delete_returning_multifrom = False

if the dialect supports RETURNING with DELETE..FROM

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)denormalize_name(*name*)

convert the given name to a case insensitive identifier
for the backend if it is an all-lowercase name.

This method is only used if the dialect defines
requires_name_normalize=True.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)detect_autocommit_setting(*dbapi_conn:DBAPIConnection*) → bool

*inherited from the* `Dialect.detect_autocommit_setting()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Detect the current autocommit setting for a DBAPI connection.

  Parameters:

**dbapi_connection** – a DBAPI connection object

  Returns:

True if autocommit is enabled, False if disabled

  Return type:

bool

This method inspects the given DBAPI connection to determine
whether autocommit mode is currently enabled. The specific
mechanism for detecting autocommit varies by database dialect
and DBAPI driver, however it should be done **without** network
round trips.

Note

Not all dialects support autocommit detection. Dialects
that do not support this feature will raise
`NotImplementedError`.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)div_is_floordiv = True

target database treats the / division operator as “floor division”

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_begin(*dbapi_connection*)

Provide an implementation of `connection.begin()`, given a
DB-API connection.

The DBAPI has no dedicated “begin” method and it is expected
that transactions are implicit.  This hook is provided for those
DBAPIs that might need additional help in this area.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_begin_twophase(*connection:Connection*, *xid:Any*) → None

*inherited from the* `Dialect.do_begin_twophase()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Begin a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_close(*dbapi_connection*)

Provide an implementation of `connection.close()`, given a DBAPI
connection.

This hook is called by the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
when a connection has been
detached from the pool, or is being returned beyond the normal
capacity of the pool.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_commit(*dbapi_connection*)

Provide an implementation of `connection.commit()`, given a
DB-API connection.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_commit_twophase(*connection:Connection*, *xid:Any*, *is_prepared:bool=True*, *recover:bool=False*) → None

*inherited from the* `Dialect.do_commit_twophase()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Commit a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid
- **is_prepared** – whether or not
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.
- **recover** – if the recover flag was passed.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_execute(*cursor*, *statement*, *parameters*, *context=None*)

Provide an implementation of `cursor.execute(statement,
parameters)`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_execute_no_params(*cursor*, *statement*, *context=None*)

Provide an implementation of `cursor.execute(statement)`.

The parameter collection should not be sent.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_executemany(*cursor*, *statement*, *parameters*, *context=None*)

Provide an implementation of `cursor.executemany(statement,
parameters)`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_ping(*dbapi_connection:DBAPIConnection*) → bool

ping the DBAPI connection and return True if the connection is
usable.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_prepare_twophase(*connection:Connection*, *xid:Any*) → None

*inherited from the* `Dialect.do_prepare_twophase()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Prepare a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_recover_twophase(*connection:Connection*) → List[Any]

*inherited from the* `Dialect.do_recover_twophase()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Recover list of uncommitted prepared two phase transaction
identifiers on the given connection.

  Parameters:

**connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_release_savepoint(*connection*, *name*)

Release the named savepoint on a connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_rollback(*dbapi_connection*)

Provide an implementation of `connection.rollback()`, given
a DB-API connection.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_rollback_to_savepoint(*connection*, *name*)

Rollback a connection to the named savepoint.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_rollback_twophase(*connection:Connection*, *xid:Any*, *is_prepared:bool=True*, *recover:bool=False*) → None

*inherited from the* `Dialect.do_rollback_twophase()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Rollback a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid
- **is_prepared** – whether or not
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.
- **recover** – if the recover flag was passed.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_savepoint(*connection*, *name*)

Create a savepoint with the given name.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_set_input_sizes(*cursor:DBAPICursor*, *list_of_tuples:_GenericSetInputSizesType*, *context:ExecutionContext*) → Any

*inherited from the* `Dialect.do_set_input_sizes()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

invoke the cursor.setinputsizes() method with appropriate arguments

This hook is called if the [Dialect.bind_typing](#sqlalchemy.engine.Dialect.bind_typing) attribute is
set to the
[BindTyping.SETINPUTSIZES](#sqlalchemy.engine.BindTyping.SETINPUTSIZES) value.
Parameter data is passed in a list of tuples (paramname, dbtype,
sqltype), where `paramname` is the key of the parameter in the
statement, `dbtype` is the DBAPI datatype and `sqltype` is the
SQLAlchemy type. The order of tuples is in the correct parameter order.

Added in version 1.4.

Changed in version 2.0: - setinputsizes mode is now enabled by
setting [Dialect.bind_typing](#sqlalchemy.engine.Dialect.bind_typing) to
[BindTyping.SETINPUTSIZES](#sqlalchemy.engine.BindTyping.SETINPUTSIZES).  Dialects which accept
a `use_setinputsizes` parameter should set this value
appropriately.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)do_terminate(*dbapi_connection*)

Provide an implementation of `connection.close()` that tries as
much as possible to not block, given a DBAPI
connection.

In the vast majority of cases this just calls .close(), however
for some asyncio dialects may call upon different API features.

This hook is called by the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
when a connection is being recycled or has been invalidated.

Added in version 1.4.41.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)driver

identifying name for the dialect’s DBAPI

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)engine_config_types: Mapping[str, Any] = {'echo': <function bool_or_str.<locals>.bool_or_value>, 'echo_pool': <function bool_or_str.<locals>.bool_or_value>, 'future': <function asbool>, 'max_overflow': <function asint>, 'pool_recycle': <function asint>, 'pool_size': <function asint>, 'pool_timeout': <function asint>}

a mapping of string keys that can be in an engine config linked to
type conversion functions.

    classmethod [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)engine_created(*engine:Engine*) → None

*inherited from the* `Dialect.engine_created()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

A convenience hook called before returning the final
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).

If the dialect returned a different class from the
[get_dialect_cls()](#sqlalchemy.engine.default.DefaultDialect.get_dialect_cls)
method, then the hook is called on both classes, first on
the dialect class returned by the [get_dialect_cls()](#sqlalchemy.engine.default.DefaultDialect.get_dialect_cls) method and
then on the class on which the method was called.

The hook should be used by dialects and/or wrappers to apply special
events to the engine or its components.   In particular, it allows
a dialect-wrapping class to apply dialect-level events.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)exclude_set_input_sizes: Set[Any] | None = None

set of DBAPI type objects that should be excluded in
automatic cursor.setinputsizes() calls.

This is only used if bind_typing is BindTyping.SET_INPUT_SIZES

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)execute_sequence_format

alias of `tuple`

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)execution_ctx_cls

alias of [DefaultExecutionContext](#sqlalchemy.engine.default.DefaultExecutionContext)

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)favor_returning_over_lastrowid = False

for backends that support both a lastrowid and a RETURNING insert
strategy, favor RETURNING for simple single-int pk inserts.

cursor.lastrowid tends to be more performant on most backends.

    property full_returning

Deprecated since version 2.0: full_returning is deprecated, please use insert_returning, update_returning, delete_returning

     classmethod [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_async_dialect_cls(*url:URL*) → Type[[Dialect](#sqlalchemy.engine.Dialect)]

*inherited from the* `Dialect.get_async_dialect_cls()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Given a URL, return the [Dialect](#sqlalchemy.engine.Dialect) that will be used by
an async engine.

By default this is an alias of [Dialect.get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls) and
just returns the cls. It may be used if a dialect provides
both a sync and async version under the same name, like the
`psycopg` driver.

Added in version 2.

See also

[Dialect.get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls)

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_check_constraints(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedCheckConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)]

*inherited from the* `Dialect.get_check_constraints()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about check constraints in `table_name`.

Given a string `table_name` and an optional string `schema`, return
check constraint information as a list of dicts corresponding
to the [ReflectedCheckConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedCheckConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints).

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_columns(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedColumn](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedColumn)]

*inherited from the* `Dialect.get_columns()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about columns in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return column
information as a list of dictionaries
corresponding to the [ReflectedColumn](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedColumn) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns).

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_default_isolation_level(*dbapi_conn*)

Given a DBAPI connection, return its isolation level, or
a default isolation level if one cannot be retrieved.

May be overridden by subclasses in order to provide a
“fallback” isolation level for databases that cannot reliably
retrieve the actual isolation level.

By default, calls the `Interfaces.get_isolation_level()`
method, propagating any exceptions raised.

Added in version 1.3.22.

     classmethod [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_dialect_cls(*url:URL*) → Type[[Dialect](#sqlalchemy.engine.Dialect)]

*inherited from the* `Dialect.get_dialect_cls()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Given a URL, return the [Dialect](#sqlalchemy.engine.Dialect) that will be used.

This is a hook that allows an external plugin to provide functionality
around an existing dialect, by allowing the plugin to be loaded
from the url based on an entrypoint, and then the plugin returns
the actual dialect to be used.

By default this just returns the cls.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_dialect_pool_class(*url:URL*) → Type[[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)]

return a Pool class to use for a given URL

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_driver_connection(*connection:DBAPIConnection*) → Any

Returns the connection object as returned by the external driver
package.

For normal dialects that use a DBAPI compliant driver this call
will just return the `connection` passed as argument.
For dialects that instead adapt a non DBAPI compliant driver, like
when adapting an asyncio driver, this call will return the
connection-like object as returned by the driver.

Added in version 1.4.24.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_foreign_keys(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)]

*inherited from the* `Dialect.get_foreign_keys()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about foreign_keys in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return foreign
key information as a list of dicts corresponding to the
[ReflectedForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint) dictionary.

This is an internal dialect method. Applications should use
`Inspector.get_foreign_keys()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_indexes(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedIndex](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedIndex)]

*inherited from the* `Dialect.get_indexes()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about indexes in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name` and an optional string `schema`, return index
information as a list of dictionaries corresponding to the
[ReflectedIndex](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedIndex) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes).

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_isolation_level(*dbapi_connection:DBAPIConnection*) → Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']

*inherited from the* `Dialect.get_isolation_level()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Given a DBAPI connection, return its isolation level.

When working with a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object,
the corresponding
DBAPI connection may be procured using the
[Connection.connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.connection) accessor.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level facilities;
these APIs should be preferred for most typical use cases.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_isolation_level_values(*dbapi_conn:DBAPIConnection*) → Sequence[Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']]

*inherited from the* `Dialect.get_isolation_level_values()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

return a sequence of string isolation level names that are accepted
by this dialect.

The available names should use the following conventions:

- use UPPERCASE names.   isolation level methods will accept lowercase
  names but these are normalized into UPPERCASE before being passed
  along to the dialect.
- separate words should be separated by spaces, not underscores, e.g.
  `REPEATABLE READ`.  isolation level names will have underscores
  converted to spaces before being passed along to the dialect.
- The names for the four standard isolation names to the extent that
  they are supported by the backend should be `READ UNCOMMITTED`,
  `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`
- if the dialect supports an autocommit option it should be provided
  using the isolation level name `AUTOCOMMIT`.
- Other isolation modes may also be present, provided that they
  are named in UPPERCASE and use spaces not underscores.

This function is used so that the default dialect can check that
a given isolation level parameter is valid, else raises an
[ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError).

A DBAPI connection is passed to the method, in the unlikely event that
the dialect needs to interrogate the connection itself to determine
this list, however it is expected that most backends will return
a hardcoded list of values.  If the dialect supports “AUTOCOMMIT”,
that value should also be present in the sequence returned.

The method raises `NotImplementedError` by default.  If a dialect
does not implement this method, then the default dialect will not
perform any checking on a given isolation level value before passing
it onto the [Dialect.set_isolation_level()](#sqlalchemy.engine.Dialect.set_isolation_level) method.  This is
to allow backwards-compatibility with third party dialects that may
not yet be implementing this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_materialized_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_materialized_view_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of all materialized view names available in the
database.

This is an internal dialect method. Applications should use
`Inspector.get_materialized_view_names()`.

  Parameters:

**schema** –

schema name to query, if not the default schema.

Added in version 2.0.

       method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_check_constraints(*connection*, ***kw*)

Return information about check constraints in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_check_constraints).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_columns(*connection*, ***kw*)

Return information about columns in all tables in the
given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_columns).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_foreign_keys(*connection*, ***kw*)

Return information about foreign_keys in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_multi_foreign_keys()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_indexes(*connection*, ***kw*)

Return information about indexes in in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_indexes).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_pk_constraint(*connection*, ***kw*)

Return information about primary key constraints in
all tables in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_pk_constraint()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_pk_constraint).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_table_comment(*connection*, ***kw*)

Return information about the table comment in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_multi_table_comment()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_table_options(*connection*, ***kw*)

Return a dictionary of options specified when the tables in the
given schema were created.

This is an internal dialect method. Applications should use
`Inspector.get_multi_table_options()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_multi_unique_constraints(*connection*, ***kw*)

Return information about unique constraints in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_unique_constraints).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by `Dialect.get_table_names()`,
`Dialect.get_view_names()` or
`Dialect.get_materialized_view_names()` depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_pk_constraint(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedPrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)

*inherited from the* `Dialect.get_pk_constraint()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about the primary key constraint on
table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return primary
key information as a dictionary corresponding to the
[ReflectedPrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_pk_constraint()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_pk_constraint).

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_schema_names(*connection:Connection*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_schema_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of all schema names available in the database.

This is an internal dialect method. Applications should use
`Inspector.get_schema_names()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_sequence_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_sequence_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of all sequence names available in the database.

This is an internal dialect method. Applications should use
`Inspector.get_sequence_names()`.

  Parameters:

**schema** – schema name to query, if not the default schema.

Added in version 1.4.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_table_comment(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedTableComment](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedTableComment)

*inherited from the* `Dialect.get_table_comment()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return the “comment” for the table identified by `table_name`.

Given a string `table_name` and an optional string `schema`, return
table comment information as a dictionary corresponding to the
[ReflectedTableComment](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedTableComment) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_table_comment()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_comment).

  Raise:

`NotImplementedError` for dialects that don’t support
comments.

Added in version 1.2.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_table_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_table_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of table names for `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_table_names()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_table_options(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → Dict[str, Any]

*inherited from the* `Dialect.get_table_options()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a dictionary of options specified when `table_name`
was created.

This is an internal dialect method. Applications should use
`Inspector.get_table_options()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_temp_table_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_temp_table_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of temporary table names on the given connection,
if supported by the underlying backend.

This is an internal dialect method. Applications should use
`Inspector.get_temp_table_names()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_temp_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_temp_view_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of temporary view names on the given connection,
if supported by the underlying backend.

This is an internal dialect method. Applications should use
`Inspector.get_temp_view_names()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_unique_constraints(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedUniqueConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)]

*inherited from the* `Dialect.get_unique_constraints()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return information about unique constraints in `table_name`.

Given a string `table_name` and an optional string `schema`, return
unique constraint information as a list of dicts corresponding
to the [ReflectedUniqueConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints).

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_view_definition(*connection:Connection*, *view_name:str*, *schema:str|None=None*, ***kw:Any*) → str

*inherited from the* `Dialect.get_view_definition()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return plain or materialized view definition.

This is an internal dialect method. Applications should use
`Inspector.get_view_definition()`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`view_name`, and an optional string `schema`, return the view
definition.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)get_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

*inherited from the* `Dialect.get_view_names()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Return a list of all non-materialized view names available in the
database.

This is an internal dialect method. Applications should use
`Inspector.get_view_names()`.

  Parameters:

**schema** – schema name to query, if not the default schema.

      method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)has_index(*connection*, *table_name*, *index_name*, *schema=None*, ***kw*)

Check the existence of a particular index name in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string
`table_name` and string index name, return `True` if an index of
the given name on the given table exists, `False` otherwise.

The [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) implements this in terms of the
[Dialect.has_table()](#sqlalchemy.engine.Dialect.has_table) and [Dialect.get_indexes()](#sqlalchemy.engine.Dialect.get_indexes) methods,
however dialects can implement a more performant version.

This is an internal dialect method. Applications should use
`Inspector.has_index()`.

Added in version 1.4.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)has_schema(*connection:Connection*, *schema_name:str*, ***kw:Any*) → bool

Check the existence of a particular schema name in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string
`schema_name`, return `True` if a schema of the
given exists, `False` otherwise.

The [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) implements this by checking
the presence of `schema_name` among the schemas returned by
[Dialect.get_schema_names()](#sqlalchemy.engine.Dialect.get_schema_names),
however dialects can implement a more performant version.

This is an internal dialect method. Applications should use
`Inspector.has_schema()`.

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)has_sequence(*connection:Connection*, *sequence_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

*inherited from the* `Dialect.has_sequence()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Check the existence of a particular sequence in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object and a string
sequence_name, return `True` if the given sequence exists in
the database, `False` otherwise.

This is an internal dialect method. Applications should use
`Inspector.has_sequence()`.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)has_table(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

*inherited from the* `Dialect.has_table()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

For internal dialect use, check the existence of a particular table
or view in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string table_name and
optional schema name, return True if the given table exists in the
database, False otherwise.

This method serves as the underlying implementation of the
public facing [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) method, and is also used
internally to implement the “checkfirst” behavior for methods like
[Table.create()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.create) and [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all).

Note

This method is used internally by SQLAlchemy, and is
published so that third-party dialects may provide an
implementation. It is **not** the public API for checking for table
presence. Please use the [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) method.

Changed in version 2.0::: [Dialect.has_table()](#sqlalchemy.engine.Dialect.has_table) now
formally supports checking for additional table-like objects:

- any type of views (plain or materialized)
- temporary tables of any kind

Previously, these two checks were not formally specified and
different dialects would vary in their behavior.   The dialect
testing suite now includes tests for all of these object types,
and dialects to the degree that the backing database supports views
or temporary tables should seek to support locating these objects
for full compliance.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)has_terminate = False

Whether or not this dialect has a separate “terminate” implementation
that does not block or require awaiting.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)identifier_preparer

This element will refer to an instance of [IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer)
once a [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) has been constructed.

    classmethod [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)import_dbapi() → DBAPIModule

*inherited from the* `Dialect.import_dbapi()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Import the DBAPI module that is used by this dialect.

The Python module object returned here will be assigned as an
instance variable to a constructed dialect under the name
`.dbapi`.

Changed in version 2.0: The [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi) class
method is renamed from the previous method `.Dialect.dbapi()`,
which would be replaced at dialect instantiation time by the
DBAPI module itself, thus using the same name in two different ways.
If a `.Dialect.dbapi()` classmethod is present on a third-party
dialect, it will be used and a deprecation warning will be emitted.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)include_set_input_sizes: Set[Any] | None = None

set of DBAPI type objects that should be included in
automatic cursor.setinputsizes() calls.

This is only used if bind_typing is BindTyping.SET_INPUT_SIZES

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)initialize(*connection:Connection*) → None

Called during strategized creation of the dialect with a
connection.

Allows dialects to configure options based on server version info or
other properties.

The connection passed here is a SQLAlchemy Connection object,
with full capabilities.

The initialize() method of the base dialect should be called via
super().

Note

as of SQLAlchemy 1.4, this method is called **before**
any [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) hooks are called.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)inline_comments = False

Indicates the dialect supports comment DDL that’s inline with the
definition of a Table or Column.  If False, this implies that ALTER must
be used to set table and column comments.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insert_executemany_returning

dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insert_executemany_returning_sort_by_parameter_order

dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used
along with the [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order)
parameter being set.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insert_returning = False

if the dialect supports RETURNING with INSERT

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insertmanyvalues_implicit_sentinel: InsertmanyvaluesSentinelOpts = symbol('NOT_SUPPORTED')

Options indicating the database supports a form of bulk INSERT where
the autoincrement integer primary key can be reliably used as an ordering
for INSERTed rows.

Added in version 2.0.10.

See also

[Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order)

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insertmanyvalues_max_parameters = 32700

Alternate to insertmanyvalues_page_size, will additionally limit
page size based on number of parameters total in the statement.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)insertmanyvalues_page_size: int = 1000

Number of rows to render into an individual INSERT..VALUES() statement
for `ExecuteStyle.INSERTMANYVALUES` executions.

The default dialect defaults this to 1000.

Added in version 2.0.

See also

[Connection.execution_options.insertmanyvalues_page_size](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.insertmanyvalues_page_size) -
execution option available on [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), statements

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)is_async = False

Whether or not this dialect is intended for asyncio use.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)is_disconnect(*e:DBAPIModule.Error*, *connection:pool.PoolProxiedConnection|interfaces.DBAPIConnection|None*, *cursor:interfaces.DBAPICursor|None*) → bool

Return True if the given DB-API error indicates an invalid
connection

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)label_length

optional user-defined max length for SQL labels

    classmethod [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)load_provisioning()

set up the provision.py module for this dialect.

For dialects that include a provision.py module that sets up
provisioning followers, this method should initiate that process.

A typical implementation would be:

```
@classmethod
def load_provisioning(cls):
    __import__("mydialect.provision")
```

The default method assumes a module named `provision.py` inside
the owning package of the current dialect, based on the `__module__`
attribute:

```
@classmethod
def load_provisioning(cls):
    package = ".".join(cls.__module__.split(".")[0:-1])
    try:
        __import__(package + ".provision")
    except ImportError:
        pass
```

Added in version 1.3.14.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)loaded_dbapi    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)max_constraint_name_length: int | None = None

The maximum length of constraint names if different from
`max_identifier_length`.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)max_identifier_length = 9999

The maximum length of identifier names.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)max_index_name_length: int | None = None

The maximum length of index names if different from
`max_identifier_length`.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)name = 'default'

identifying name for the dialect from a DBAPI-neutral point of view
(i.e. ‘sqlite’)

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)normalize_name(*name*)

convert the given name to lowercase if it is detected as
case insensitive.

This method is only used if the dialect defines
requires_name_normalize=True.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)on_connect() → Callable[[Any], None] | None

return a callable which sets up a newly created DBAPI connection.

The callable should accept a single argument “conn” which is the
DBAPI connection itself.  The inner callable has no
return value.

E.g.:

```
class MyDialect(default.DefaultDialect):
    # ...

    def on_connect(self):
        def do_on_connect(connection):
            connection.execute("SET SPECIAL FLAGS etc")

        return do_on_connect
```

This is used to set dialect-wide per-connection options such as
isolation modes, Unicode modes, etc.

The “do_on_connect” callable is invoked by using the
[PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect) event
hook, then unwrapping the DBAPI connection and passing it into the
callable.

Changed in version 1.4: the on_connect hook is no longer called twice
for the first connection of a dialect.  The on_connect hook is still
called before the [Dialect.initialize()](#sqlalchemy.engine.Dialect.initialize) method however.

Changed in version 1.4.3: the on_connect hook is invoked from a new
method on_connect_url that passes the URL that was used to create
the connect args.   Dialects can implement on_connect_url instead
of on_connect if they need the URL object that was used for the
connection in order to get additional context.

If None is returned, no event listener is generated.

  Returns:

a callable that accepts a single DBAPI connection as an
argument, or None.

See also

[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) - allows the DBAPI `connect()` sequence
itself to be controlled.

[Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url) - supersedes
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) to also receive the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object in context.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)on_connect_url(*url:URL*) → Callable[[Any], Any] | None

*inherited from the* `Dialect.on_connect_url()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

return a callable which sets up a newly created DBAPI connection.

This method is a new hook that supersedes the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method when implemented by a
dialect.   When not implemented by a dialect, it invokes the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method directly to maintain
compatibility with existing dialects.   There is no deprecation
for [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) expected.

The callable should accept a single argument “conn” which is the
DBAPI connection itself.  The inner callable has no
return value.

E.g.:

```
class MyDialect(default.DefaultDialect):
    # ...

    def on_connect_url(self, url):
        def do_on_connect(connection):
            connection.execute("SET SPECIAL FLAGS etc")

        return do_on_connect
```

This is used to set dialect-wide per-connection options such as
isolation modes, Unicode modes, etc.

This method differs from [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) in that
it is passed the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object that’s relevant to the
connect args.  Normally the only way to get this is from the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) hook is to look on the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) itself, however this URL object may have been
replaced by plugins.

Note

The default implementation of
[Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url) is to invoke the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method. Therefore if a dialect
implements this method, the [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)
method **will not be called** unless the overriding dialect calls
it directly from here.

Added in version 1.4.3: added [Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url)
which normally calls into [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect).

   Parameters:

**url** – a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object representing the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) that was passed to the
[Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

  Returns:

a callable that accepts a single DBAPI connection as an
argument, or None.

See also

[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)paramstyle

the paramstyle to be used (some DB-APIs support multiple
paramstyles).

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)positional

True if the paramstyle for this Dialect is positional.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)preexecute_autoincrement_sequences = False

True if ‘implicit’ primary key functions must be executed separately
in order to get their value, if RETURNING is not used.

This is currently oriented towards PostgreSQL when the
`implicit_returning=False` parameter is used on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)preparer

alias of [IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer)

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)reflection_options = ()

*inherited from the* `Dialect.reflection_options` *attribute of* [Dialect](#sqlalchemy.engine.Dialect)

Sequence of string names indicating keyword arguments that can be
established on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object which will be passed as
“reflection options” when using [Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with).

Current example is “oracle_resolve_synonyms” in the Oracle Database
dialects.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)requires_name_normalize = False

Indicates symbol names are returned by the database in
UPPERCASED if they are case insensitive within the database.
If this is True, the methods normalize_name()
and denormalize_name() must be provided.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)reset_isolation_level(*dbapi_conn*)

Given a DBAPI connection, revert its isolation to the default.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
isolation level facilities; these APIs should be preferred for
most typical use cases.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)returns_native_bytes = False

indicates if Python bytes() objects are returned natively by the
driver for SQL “binary” datatypes.

Added in version 2.0.11.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)sequences_optional = False

If True, indicates if the [Sequence.optional](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.optional)
parameter on the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) construct
should signal to not generate a CREATE SEQUENCE. Applies only to
dialects that support sequences. Currently used only to allow PostgreSQL
SERIAL to be used on a column that specifies Sequence() for usage on
other backends.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)server_side_cursors = False

deprecated; indicates if the dialect should attempt to use server
side cursors by default

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)server_version_info = None

a tuple containing a version number for the DB backend in use.

This value is only available for supporting dialects, and is
typically populated during the initial connection to the database.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)set_connection_execution_options(*connection:Connection*, *opts:Mapping[str,Any]*) → None

Establish execution options for a given connection.

This is implemented by [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) in order to implement
the [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
execution option.  Dialects can intercept various execution options
which may need to modify state on a particular DBAPI connection.

Added in version 1.4.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)set_engine_execution_options(*engine:Engine*, *opts:Mapping[str,Any]*) → None

Establish execution options for a given engine.

This is implemented by [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) to establish
event hooks for new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) instances created
by the given [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which will then invoke the
[Dialect.set_connection_execution_options()](#sqlalchemy.engine.Dialect.set_connection_execution_options) method for that
connection.

    method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)set_isolation_level(*dbapi_connection:DBAPIConnection*, *level:Literal['SERIALIZABLE','REPEATABLEREAD','READCOMMITTED','READUNCOMMITTED','AUTOCOMMIT']*) → None

*inherited from the* `Dialect.set_isolation_level()` *method of* [Dialect](#sqlalchemy.engine.Dialect)

Given a DBAPI connection, set its isolation level.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
isolation level facilities; these APIs should be preferred for
most typical use cases.

If the dialect also implements the
[Dialect.get_isolation_level_values()](#sqlalchemy.engine.Dialect.get_isolation_level_values) method, then the given
level is guaranteed to be one of the string names within that sequence,
and the method will not need to anticipate a lookup failure.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)skip_autocommit_rollback

Whether or not the [create_engine.skip_autocommit_rollback](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.skip_autocommit_rollback)
parameter was set.

Added in version 2.0.43.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)statement_compiler

alias of [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler)

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_alter = True

`True` if the database supports `ALTER TABLE` - used only for
generating foreign key constraints in certain circumstances

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_comments = False

Indicates the dialect supports comment DDL on tables and columns.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_constraint_comments = False

Indicates if the dialect supports comment DDL on constraints.

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_default_metavalue = False

dialect supports INSERT… VALUES (DEFAULT) syntax

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_default_values = False

dialect supports INSERT… DEFAULT VALUES syntax

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_empty_insert = True

dialect supports INSERT () VALUES ()

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_identity_columns = False

target database supports IDENTITY

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_multivalues_insert = False

Target database supports INSERT…VALUES with multiple value
sets, i.e. INSERT INTO table (cols) VALUES (…), (…), (…), …

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_native_boolean = False

Indicates if the dialect supports a native boolean construct.
This will prevent [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) from generating a CHECK
constraint when that type is used.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_native_decimal = False

indicates if Decimal objects are handled and returned for precision
numeric types, or if floats are returned

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_native_enum = False

Indicates if the dialect supports a native ENUM construct.
This will prevent [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) from generating a CHECK
constraint when that type is used in “native” mode.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_native_uuid = False

indicates if Python UUID() objects are handled natively by the
driver for SQL UUID datatypes.

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_sane_multi_rowcount = True

Indicate whether the dialect properly implements rowcount for
`UPDATE` and `DELETE` statements when executed via
executemany.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_sane_rowcount = True

Indicate whether the dialect properly implements rowcount for
`UPDATE` and `DELETE` statements.

    property supports_sane_rowcount_returning

True if this dialect supports sane rowcount even if RETURNING is
in use.

For dialects that don’t support RETURNING, this is synonymous with
`supports_sane_rowcount`.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_sequences = False

Indicates if the dialect supports CREATE SEQUENCE or similar.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_server_side_cursors = False

indicates if the dialect supports server side cursors

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_simple_order_by_label = True

target database supports ORDER BY <labelname>, where <labelname>
refers to a label in the columns clause of the SELECT

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)supports_statement_cache = True

indicates if this dialect supports caching.

All dialects that are compatible with statement caching should set this
flag to True directly on each dialect class and subclass that supports
it.  SQLAlchemy tests that this flag is locally present on each dialect
subclass before it will use statement caching.  This is to provide
safety for legacy or new dialects that are not yet fully tested to be
compliant with SQL statement caching.

Added in version 1.4.5.

See also

[Caching for Third Party Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-thirdparty-caching)

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)tuple_in_values = False

target database supports tuple IN, i.e. (x, y) IN ((q, p), (r, z))

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)type_compiler

legacy; this is a TypeCompiler class at the class level, a
TypeCompiler instance at the instance level.

Refer to type_compiler_instance instead.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)type_compiler_cls

alias of [GenericTypeCompiler](#sqlalchemy.sql.compiler.GenericTypeCompiler)

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)type_compiler_instance

instance of a [Compiled](#sqlalchemy.engine.Compiled) class used to compile SQL type
objects

Added in version 2.0.

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)type_descriptor(*typeobj*)

Provide a database-specific [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine) object, given
the generic object which comes from the types module.

This method looks for a dictionary called
`colspecs` as a class or instance-level variable,
and passes on to `adapt_type()`.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)update_executemany_returning = False

dialect supports UPDATE..RETURNING with executemany.

    attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)update_returning = False

if the dialect supports RETURNING with UPDATE

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)update_returning_multifrom = False

if the dialect supports RETURNING with UPDATE..FROM

Added in version 2.0.

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)use_insertmanyvalues: bool = False

if True, indicates “insertmanyvalues” functionality should be used
to allow for `insert_executemany_returning` behavior, if possible.

In practice, setting this to True means:

if `supports_multivalues_insert`, `insert_returning` and
`use_insertmanyvalues` are all True, the SQL compiler will produce
an INSERT that will be interpreted by the [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect)
as an `ExecuteStyle.INSERTMANYVALUES` execution that allows
for INSERT of many rows with RETURNING by rewriting a single-row
INSERT statement to have multiple VALUES clauses, also executing
the statement multiple times for a series of batches when large numbers
of rows are given.

The parameter is False for the default dialect, and is set to True for
SQLAlchemy internal dialects SQLite, MySQL/MariaDB, PostgreSQL, SQL Server.
It remains at False for Oracle Database, which provides native “executemany
with RETURNING” support and also does not support
`supports_multivalues_insert`.  For MySQL/MariaDB, those MySQL dialects
that don’t support RETURNING will not report
`insert_executemany_returning` as True.

Added in version 2.0.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

     attribute [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)use_insertmanyvalues_wo_returning: bool = False

if True, and use_insertmanyvalues is also True, INSERT statements
that don’t include RETURNING will also use “insertmanyvalues”.

Added in version 2.0.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

     method [sqlalchemy.engine.default.DefaultDialect.](#sqlalchemy.engine.default.DefaultDialect)validate_identifier(*ident:str*) → None

Validates an identifier name, raising an exception if invalid

     class sqlalchemy.engine.Dialect

*inherits from* `sqlalchemy.event.registry.EventTarget`

Define the behavior of a specific database and DB-API combination.

Any aspect of metadata definition, SQL query generation,
execution, result-set handling, or anything else which varies
between databases is defined under the general category of the
Dialect.  The Dialect acts as a factory for other
database-specific object implementations including
ExecutionContext, Compiled, DefaultGenerator, and TypeEngine.

Note

Third party dialects should not subclass [Dialect](#sqlalchemy.engine.Dialect)
directly.  Instead, subclass [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) or
descendant class.

| Member Name | Description |
| --- | --- |
| bind_typing | define a means of passing typing information to the database and/or
driver for bound parameters. |
| colspecs | A dictionary of TypeEngine classes from sqlalchemy.types mapped
to subclasses that are specific to the dialect class.  This
dictionary is class-level only and is not accessed from the
dialect instance itself. |
| connect() | Establish a connection using this dialect’s DBAPI. |
| construct_arguments | Optional set of argument specifiers for various SQLAlchemy
constructs, typically schema items. |
| create_connect_args() | Build DB-API compatible connection arguments. |
| create_xid() | Create a two-phase transaction ID. |
| cte_follows_insert | target database, when given a CTE with an INSERT statement, needs
the CTE to be below the INSERT |
| dbapi | A reference to the DBAPI module object itself. |
| dbapi_exception_translation_map | A dictionary of names that will contain as values the names of
pep-249 exceptions (“IntegrityError”, “OperationalError”, etc)
keyed to alternate class names, to support the case where a
DBAPI has exception classes that aren’t named as they are
referred to (e.g. IntegrityError = MyException).   In the vast
majority of cases this dictionary is empty. |
| ddl_compiler | aCompiledclass used to compile DDL statements |
| default_isolation_level | the isolation that is implicitly present on new connections |
| default_metavalue_token | for INSERT… VALUES (DEFAULT) syntax, the token to put in the
parenthesis. |
| default_schema_name | the name of the default schema.  This value is only available for
supporting dialects, and is typically populated during the
initial connection to the database. |
| default_sequence_base | the default value that will be rendered as the “START WITH” portion of
a CREATE SEQUENCE DDL statement. |
| delete_executemany_returning | dialect supports DELETE..RETURNING with executemany. |
| delete_returning | if the dialect supports RETURNING with DELETE |
| delete_returning_multifrom | if the dialect supports RETURNING with DELETE..FROM |
| denormalize_name() | convert the given name to a case insensitive identifier
for the backend if it is an all-lowercase name. |
| detect_autocommit_setting() | Detect the current autocommit setting for a DBAPI connection. |
| div_is_floordiv | target database treats the / division operator as “floor division” |
| do_begin() | Provide an implementation ofconnection.begin(), given a
DB-API connection. |
| do_begin_twophase() | Begin a two phase transaction on the given connection. |
| do_close() | Provide an implementation ofconnection.close(), given a DBAPI
connection. |
| do_commit() | Provide an implementation ofconnection.commit(), given a
DB-API connection. |
| do_commit_twophase() | Commit a two phase transaction on the given connection. |
| do_execute() | Provide an implementation ofcursor.execute(statement,parameters). |
| do_execute_no_params() | Provide an implementation ofcursor.execute(statement). |
| do_executemany() | Provide an implementation ofcursor.executemany(statement,parameters). |
| do_ping() | ping the DBAPI connection and return True if the connection is
usable. |
| do_prepare_twophase() | Prepare a two phase transaction on the given connection. |
| do_recover_twophase() | Recover list of uncommitted prepared two phase transaction
identifiers on the given connection. |
| do_release_savepoint() | Release the named savepoint on a connection. |
| do_rollback() | Provide an implementation ofconnection.rollback(), given
a DB-API connection. |
| do_rollback_to_savepoint() | Rollback a connection to the named savepoint. |
| do_rollback_twophase() | Rollback a two phase transaction on the given connection. |
| do_savepoint() | Create a savepoint with the given name. |
| do_set_input_sizes() | invoke the cursor.setinputsizes() method with appropriate arguments |
| do_terminate() | Provide an implementation ofconnection.close()that tries as
much as possible to not block, given a DBAPI
connection. |
| driver | identifying name for the dialect’s DBAPI |
| engine_config_types | a mapping of string keys that can be in an engine config linked to
type conversion functions. |
| engine_created() | A convenience hook called before returning the finalEngine. |
| exclude_set_input_sizes | set of DBAPI type objects that should be excluded in
automatic cursor.setinputsizes() calls. |
| execute_sequence_format | either the ‘tuple’ or ‘list’ type, depending on what cursor.execute()
accepts for the second argument (they vary). |
| execution_ctx_cls | aExecutionContextclass used to handle statement execution |
| favor_returning_over_lastrowid | for backends that support both a lastrowid and a RETURNING insert
strategy, favor RETURNING for simple single-int pk inserts. |
| get_async_dialect_cls() | Given a URL, return theDialectthat will be used by
an async engine. |
| get_check_constraints() | Return information about check constraints intable_name. |
| get_columns() | Return information about columns intable_name. |
| get_default_isolation_level() | Given a DBAPI connection, return its isolation level, or
a default isolation level if one cannot be retrieved. |
| get_dialect_cls() | Given a URL, return theDialectthat will be used. |
| get_dialect_pool_class() | return a Pool class to use for a given URL |
| get_driver_connection() | Returns the connection object as returned by the external driver
package. |
| get_foreign_keys() | Return information about foreign_keys intable_name. |
| get_indexes() | Return information about indexes intable_name. |
| get_isolation_level() | Given a DBAPI connection, return its isolation level. |
| get_isolation_level_values() | return a sequence of string isolation level names that are accepted
by this dialect. |
| get_materialized_view_names() | Return a list of all materialized view names available in the
database. |
| get_multi_check_constraints() | Return information about check constraints in all tables
in the givenschema. |
| get_multi_columns() | Return information about columns in all tables in the
givenschema. |
| get_multi_foreign_keys() | Return information about foreign_keys in all tables
in the givenschema. |
| get_multi_indexes() | Return information about indexes in in all tables
in the givenschema. |
| get_multi_pk_constraint() | Return information about primary key constraints in
all tables in the givenschema. |
| get_multi_table_comment() | Return information about the table comment in all tables
in the givenschema. |
| get_multi_table_options() | Return a dictionary of options specified when the tables in the
given schema were created. |
| get_multi_unique_constraints() | Return information about unique constraints in all tables
in the givenschema. |
| get_pk_constraint() | Return information about the primary key constraint on
table_name`. |
| get_schema_names() | Return a list of all schema names available in the database. |
| get_sequence_names() | Return a list of all sequence names available in the database. |
| get_table_comment() | Return the “comment” for the table identified bytable_name. |
| get_table_names() | Return a list of table names forschema. |
| get_table_options() | Return a dictionary of options specified whentable_namewas created. |
| get_temp_table_names() | Return a list of temporary table names on the given connection,
if supported by the underlying backend. |
| get_temp_view_names() | Return a list of temporary view names on the given connection,
if supported by the underlying backend. |
| get_unique_constraints() | Return information about unique constraints intable_name. |
| get_view_definition() | Return plain or materialized view definition. |
| get_view_names() | Return a list of all non-materialized view names available in the
database. |
| has_index() | Check the existence of a particular index name in the database. |
| has_schema() | Check the existence of a particular schema name in the database. |
| has_sequence() | Check the existence of a particular sequence in the database. |
| has_table() | For internal dialect use, check the existence of a particular table
or view in the database. |
| has_terminate | Whether or not this dialect has a separate “terminate” implementation
that does not block or require awaiting. |
| identifier_preparer | This element will refer to an instance ofIdentifierPrepareronce aDefaultDialecthas been constructed. |
| import_dbapi() | Import the DBAPI module that is used by this dialect. |
| include_set_input_sizes | set of DBAPI type objects that should be included in
automatic cursor.setinputsizes() calls. |
| initialize() | Called during strategized creation of the dialect with a
connection. |
| inline_comments | Indicates the dialect supports comment DDL that’s inline with the
definition of a Table or Column.  If False, this implies that ALTER must
be used to set table and column comments. |
| insert_executemany_returning | dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used. |
| insert_executemany_returning_sort_by_parameter_order | dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used
along with theInsert.returning.sort_by_parameter_orderparameter being set. |
| insert_returning | if the dialect supports RETURNING with INSERT |
| insertmanyvalues_implicit_sentinel | Options indicating the database supports a form of bulk INSERT where
the autoincrement integer primary key can be reliably used as an ordering
for INSERTed rows. |
| insertmanyvalues_max_parameters | Alternate to insertmanyvalues_page_size, will additionally limit
page size based on number of parameters total in the statement. |
| insertmanyvalues_page_size | Number of rows to render into an individual INSERT..VALUES() statement
forExecuteStyle.INSERTMANYVALUESexecutions. |
| is_async | Whether or not this dialect is intended for asyncio use. |
| is_disconnect() | Return True if the given DB-API error indicates an invalid
connection |
| label_length | optional user-defined max length for SQL labels |
| load_provisioning() | set up the provision.py module for this dialect. |
| loaded_dbapi | same as .dbapi, but is never None; will raise an error if no
DBAPI was set up. |
| max_constraint_name_length | The maximum length of constraint names if different frommax_identifier_length. |
| max_identifier_length | The maximum length of identifier names. |
| max_index_name_length | The maximum length of index names if different frommax_identifier_length. |
| name | identifying name for the dialect from a DBAPI-neutral point of view
(i.e. ‘sqlite’) |
| normalize_name() | convert the given name to lowercase if it is detected as
case insensitive. |
| on_connect() | return a callable which sets up a newly created DBAPI connection. |
| on_connect_url() | return a callable which sets up a newly created DBAPI connection. |
| paramstyle | the paramstyle to be used (some DB-APIs support multiple
paramstyles). |
| positional | True if the paramstyle for this Dialect is positional. |
| preexecute_autoincrement_sequences | True if ‘implicit’ primary key functions must be executed separately
in order to get their value, if RETURNING is not used. |
| preparer | aIdentifierPreparerclass used to
quote identifiers. |
| reflection_options | Sequence of string names indicating keyword arguments that can be
established on aTableobject which will be passed as
“reflection options” when usingTable.autoload_with. |
| requires_name_normalize | Indicates symbol names are returned by the database in
UPPERCASED if they are case insensitive within the database.
If this is True, the methods normalize_name()
and denormalize_name() must be provided. |
| reset_isolation_level() | Given a DBAPI connection, revert its isolation to the default. |
| returns_native_bytes | indicates if Python bytes() objects are returned natively by the
driver for SQL “binary” datatypes. |
| sequences_optional | If True, indicates if theSequence.optionalparameter on theSequenceconstruct
should signal to not generate a CREATE SEQUENCE. Applies only to
dialects that support sequences. Currently used only to allow PostgreSQL
SERIAL to be used on a column that specifies Sequence() for usage on
other backends. |
| server_side_cursors | deprecated; indicates if the dialect should attempt to use server
side cursors by default |
| server_version_info | a tuple containing a version number for the DB backend in use. |
| set_connection_execution_options() | Establish execution options for a given connection. |
| set_engine_execution_options() | Establish execution options for a given engine. |
| set_isolation_level() | Given a DBAPI connection, set its isolation level. |
| skip_autocommit_rollback | Whether or not thecreate_engine.skip_autocommit_rollbackparameter was set. |
| statement_compiler | aCompiledclass used to compile SQL statements |
| supports_alter | Trueif the database supportsALTERTABLE- used only for
generating foreign key constraints in certain circumstances |
| supports_comments | Indicates the dialect supports comment DDL on tables and columns. |
| supports_constraint_comments | Indicates if the dialect supports comment DDL on constraints. |
| supports_default_metavalue | dialect supports INSERT…(col) VALUES (DEFAULT) syntax. |
| supports_default_values | dialect supports INSERT… DEFAULT VALUES syntax |
| supports_empty_insert | dialect supports INSERT () VALUES (), i.e. a plain INSERT with no
columns in it. |
| supports_identity_columns | target database supports IDENTITY |
| supports_multivalues_insert | Target database supports INSERT…VALUES with multiple value
sets, i.e. INSERT INTO table (cols) VALUES (…), (…), (…), … |
| supports_native_boolean | Indicates if the dialect supports a native boolean construct.
This will preventBooleanfrom generating a CHECK
constraint when that type is used. |
| supports_native_decimal | indicates if Decimal objects are handled and returned for precision
numeric types, or if floats are returned |
| supports_native_enum | Indicates if the dialect supports a native ENUM construct.
This will preventEnumfrom generating a CHECK
constraint when that type is used in “native” mode. |
| supports_native_uuid | indicates if Python UUID() objects are handled natively by the
driver for SQL UUID datatypes. |
| supports_sane_multi_rowcount | Indicate whether the dialect properly implements rowcount forUPDATEandDELETEstatements when executed via
executemany. |
| supports_sane_rowcount | Indicate whether the dialect properly implements rowcount forUPDATEandDELETEstatements. |
| supports_sequences | Indicates if the dialect supports CREATE SEQUENCE or similar. |
| supports_server_side_cursors | indicates if the dialect supports server side cursors |
| supports_simple_order_by_label | target database supports ORDER BY <labelname>, where <labelname>
refers to a label in the columns clause of the SELECT |
| supports_statement_cache | indicates if this dialect supports caching. |
| tuple_in_values | target database supports tuple IN, i.e. (x, y) IN ((q, p), (r, z)) |
| type_compiler | legacy; this is a TypeCompiler class at the class level, a
TypeCompiler instance at the instance level. |
| type_compiler_cls | aCompiledclass used to compile SQL type objects |
| type_compiler_instance | instance of aCompiledclass used to compile SQL type
objects |
| type_descriptor() | Transform a generic type to a dialect-specific type. |
| update_executemany_returning | dialect supports UPDATE..RETURNING with executemany. |
| update_returning | if the dialect supports RETURNING with UPDATE |
| update_returning_multifrom | if the dialect supports RETURNING with UPDATE..FROM |
| use_insertmanyvalues | if True, indicates “insertmanyvalues” functionality should be used
to allow forinsert_executemany_returningbehavior, if possible. |
| use_insertmanyvalues_wo_returning | if True, and use_insertmanyvalues is also True, INSERT statements
that don’t include RETURNING will also use “insertmanyvalues”. |
| validate_identifier() | Validates an identifier name, raising an exception if invalid |

   attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)bind_typing = 1

define a means of passing typing information to the database and/or
driver for bound parameters.

See [BindTyping](#sqlalchemy.engine.BindTyping) for values.

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)colspecs: MutableMapping[Type[[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]], Type[[TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[Any]]]

A dictionary of TypeEngine classes from sqlalchemy.types mapped
to subclasses that are specific to the dialect class.  This
dictionary is class-level only and is not accessed from the
dialect instance itself.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)connect(**cargs:Any*, ***cparams:Any*) → [DBAPIConnection](#sqlalchemy.engine.interfaces.DBAPIConnection)

Establish a connection using this dialect’s DBAPI.

The default implementation of this method is:

```
def connect(self, *cargs, **cparams):
    return self.dbapi.connect(*cargs, **cparams)
```

The `*cargs, **cparams` parameters are generated directly
from this dialect’s [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

This method may be used for dialects that need to perform programmatic
per-connection steps when a new connection is procured from the
DBAPI.

  Parameters:

- ***cargs** – positional parameters returned from the
  [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method
- ****cparams** – keyword parameters returned from the
  [Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

  Returns:

a DBAPI connection, typically from the [PEP 249](https://peps.python.org/pep-0249/) module
level `.connect()` function.

See also

[Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args)

[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)construct_arguments: List[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[Type[[SchemaItem](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.SchemaItem) | [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)], Mapping[str, Any]]] | None = None

Optional set of argument specifiers for various SQLAlchemy
constructs, typically schema items.

To implement, establish as a series of tuples, as in:

```
construct_arguments = [
    (schema.Index, {"using": False, "where": None, "ops": None}),
]
```

If the above construct is established on the PostgreSQL dialect,
the [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index) construct will now accept the keyword arguments
`postgresql_using`, `postgresql_where`, nad `postgresql_ops`.
Any other argument specified to the constructor of [Index](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.Index)
which is prefixed with `postgresql_` will raise [ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError).

A dialect which does not include a `construct_arguments` member will
not participate in the argument validation system.  For such a dialect,
any argument name is accepted by all participating constructs, within
the namespace of arguments prefixed with that dialect name.  The rationale
here is so that third-party dialects that haven’t yet implemented this
feature continue to function in the old way.

See also

[DialectKWArgs](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.base.DialectKWArgs) - implementing base class which consumes
[DefaultDialect.construct_arguments](#sqlalchemy.engine.default.DefaultDialect.construct_arguments)

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)create_connect_args(*url:URL*) → ConnectArgsType

Build DB-API compatible connection arguments.

Given a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object, returns a tuple
consisting of a `(*args, **kwargs)` suitable to send directly
to the dbapi’s connect function.   The arguments are sent to the
[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) method which then runs the DBAPI-level
`connect()` function.

The method typically makes use of the
[URL.translate_connect_args()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.translate_connect_args)
method in order to generate a dictionary of options.

The default implementation is:

```
def create_connect_args(self, url):
    opts = url.translate_connect_args()
    opts.update(url.query)
    return ([], opts)
```

   Parameters:

**url** – a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object

  Returns:

a tuple of `(*args, **kwargs)` which will be passed to the
[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) method.

See also

[URL.translate_connect_args()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL.translate_connect_args)

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)create_xid() → Any

Create a two-phase transaction ID.

This id will be passed to do_begin_twophase(),
do_rollback_twophase(), do_commit_twophase().  Its format is
unspecified.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)cte_follows_insert: bool

target database, when given a CTE with an INSERT statement, needs
the CTE to be below the INSERT

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)dbapi: DBAPIModule | None

A reference to the DBAPI module object itself.

SQLAlchemy dialects import DBAPI modules using the classmethod
[Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi). The rationale is so that any dialect
module can be imported and used to generate SQL statements without the
need for the actual DBAPI driver to be installed.  Only when an
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) is constructed using [create_engine()](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine) does the
DBAPI get imported; at that point, the creation process will assign
the DBAPI module to this attribute.

Dialects should therefore implement [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi)
which will import the necessary module and return it, and then refer
to `self.dbapi` in dialect code in order to refer to the DBAPI module
contents.

Changed in version The: [Dialect.dbapi](#sqlalchemy.engine.Dialect.dbapi) attribute is exclusively
used as the per-[Dialect](#sqlalchemy.engine.Dialect)-instance reference to the DBAPI
module.   The previous not-fully-documented `.Dialect.dbapi()`
classmethod is deprecated and replaced by [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi).

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)dbapi_exception_translation_map: Mapping[str, str] = {}

A dictionary of names that will contain as values the names of
pep-249 exceptions (“IntegrityError”, “OperationalError”, etc)
keyed to alternate class names, to support the case where a
DBAPI has exception classes that aren’t named as they are
referred to (e.g. IntegrityError = MyException).   In the vast
majority of cases this dictionary is empty.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)ddl_compiler: Type[[DDLCompiler](#sqlalchemy.sql.compiler.DDLCompiler)]

a [Compiled](#sqlalchemy.engine.Compiled) class used to compile DDL statements

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)default_isolation_level: IsolationLevel | None

the isolation that is implicitly present on new connections

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)default_metavalue_token: str = 'DEFAULT'

for INSERT… VALUES (DEFAULT) syntax, the token to put in the
parenthesis.

E.g. for SQLite this is the keyword “NULL”.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)default_schema_name: str | None

the name of the default schema.  This value is only available for
supporting dialects, and is typically populated during the
initial connection to the database.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)default_sequence_base: int

the default value that will be rendered as the “START WITH” portion of
a CREATE SEQUENCE DDL statement.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)delete_executemany_returning: bool

dialect supports DELETE..RETURNING with executemany.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)delete_returning: bool

if the dialect supports RETURNING with DELETE

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)delete_returning_multifrom: bool

if the dialect supports RETURNING with DELETE..FROM

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)denormalize_name(*name:str*) → str

convert the given name to a case insensitive identifier
for the backend if it is an all-lowercase name.

This method is only used if the dialect defines
requires_name_normalize=True.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)detect_autocommit_setting(*dbapi_conn:DBAPIConnection*) → bool

Detect the current autocommit setting for a DBAPI connection.

  Parameters:

**dbapi_connection** – a DBAPI connection object

  Returns:

True if autocommit is enabled, False if disabled

  Return type:

bool

This method inspects the given DBAPI connection to determine
whether autocommit mode is currently enabled. The specific
mechanism for detecting autocommit varies by database dialect
and DBAPI driver, however it should be done **without** network
round trips.

Note

Not all dialects support autocommit detection. Dialects
that do not support this feature will raise
`NotImplementedError`.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)div_is_floordiv: bool

target database treats the / division operator as “floor division”

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_begin(*dbapi_connection:PoolProxiedConnection*) → None

Provide an implementation of `connection.begin()`, given a
DB-API connection.

The DBAPI has no dedicated “begin” method and it is expected
that transactions are implicit.  This hook is provided for those
DBAPIs that might need additional help in this area.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_begin_twophase(*connection:Connection*, *xid:Any*) → None

Begin a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_close(*dbapi_connection:DBAPIConnection*) → None

Provide an implementation of `connection.close()`, given a DBAPI
connection.

This hook is called by the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
when a connection has been
detached from the pool, or is being returned beyond the normal
capacity of the pool.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_commit(*dbapi_connection:PoolProxiedConnection*) → None

Provide an implementation of `connection.commit()`, given a
DB-API connection.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_commit_twophase(*connection:Connection*, *xid:Any*, *is_prepared:bool=True*, *recover:bool=False*) → None

Commit a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid
- **is_prepared** – whether or not
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.
- **recover** – if the recover flag was passed.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_execute(*cursor:DBAPICursor*, *statement:str*, *parameters:Sequence[Any]|Mapping[str,Any]|None*, *context:ExecutionContext|None=None*) → None

Provide an implementation of `cursor.execute(statement,
parameters)`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_execute_no_params(*cursor:DBAPICursor*, *statement:str*, *context:ExecutionContext|None=None*) → None

Provide an implementation of `cursor.execute(statement)`.

The parameter collection should not be sent.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_executemany(*cursor:DBAPICursor*, *statement:str*, *parameters:Sequence[Sequence[Any]]|Sequence[Mapping[str,Any]]*, *context:ExecutionContext|None=None*) → None

Provide an implementation of `cursor.executemany(statement,
parameters)`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_ping(*dbapi_connection:DBAPIConnection*) → bool

ping the DBAPI connection and return True if the connection is
usable.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_prepare_twophase(*connection:Connection*, *xid:Any*) → None

Prepare a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_recover_twophase(*connection:Connection*) → List[Any]

Recover list of uncommitted prepared two phase transaction
identifiers on the given connection.

  Parameters:

**connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_release_savepoint(*connection:Connection*, *name:str*) → None

Release the named savepoint on a connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_rollback(*dbapi_connection:PoolProxiedConnection*) → None

Provide an implementation of `connection.rollback()`, given
a DB-API connection.

  Parameters:

**dbapi_connection** – a DBAPI connection, typically
proxied within a `ConnectionFairy`.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_rollback_to_savepoint(*connection:Connection*, *name:str*) → None

Rollback a connection to the named savepoint.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_rollback_twophase(*connection:Connection*, *xid:Any*, *is_prepared:bool=True*, *recover:bool=False*) → None

Rollback a two phase transaction on the given connection.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **xid** – xid
- **is_prepared** – whether or not
  [TwoPhaseTransaction.prepare()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.TwoPhaseTransaction.prepare) was called.
- **recover** – if the recover flag was passed.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_savepoint(*connection:Connection*, *name:str*) → None

Create a savepoint with the given name.

  Parameters:

- **connection** – a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).
- **name** – savepoint name.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_set_input_sizes(*cursor:DBAPICursor*, *list_of_tuples:_GenericSetInputSizesType*, *context:ExecutionContext*) → Any

invoke the cursor.setinputsizes() method with appropriate arguments

This hook is called if the [Dialect.bind_typing](#sqlalchemy.engine.Dialect.bind_typing) attribute is
set to the
[BindTyping.SETINPUTSIZES](#sqlalchemy.engine.BindTyping.SETINPUTSIZES) value.
Parameter data is passed in a list of tuples (paramname, dbtype,
sqltype), where `paramname` is the key of the parameter in the
statement, `dbtype` is the DBAPI datatype and `sqltype` is the
SQLAlchemy type. The order of tuples is in the correct parameter order.

Added in version 1.4.

Changed in version 2.0: - setinputsizes mode is now enabled by
setting [Dialect.bind_typing](#sqlalchemy.engine.Dialect.bind_typing) to
[BindTyping.SETINPUTSIZES](#sqlalchemy.engine.BindTyping.SETINPUTSIZES).  Dialects which accept
a `use_setinputsizes` parameter should set this value
appropriately.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)do_terminate(*dbapi_connection:DBAPIConnection*) → None

Provide an implementation of `connection.close()` that tries as
much as possible to not block, given a DBAPI
connection.

In the vast majority of cases this just calls .close(), however
for some asyncio dialects may call upon different API features.

This hook is called by the [Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)
when a connection is being recycled or has been invalidated.

Added in version 1.4.41.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)driver: str

identifying name for the dialect’s DBAPI

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)engine_config_types: Mapping[str, Any]

a mapping of string keys that can be in an engine config linked to
type conversion functions.

    classmethod [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)engine_created(*engine:Engine*) → None

A convenience hook called before returning the final
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine).

If the dialect returned a different class from the
[get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls)
method, then the hook is called on both classes, first on
the dialect class returned by the [get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls) method and
then on the class on which the method was called.

The hook should be used by dialects and/or wrappers to apply special
events to the engine or its components.   In particular, it allows
a dialect-wrapping class to apply dialect-level events.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)exclude_set_input_sizes: Set[Any] | None

set of DBAPI type objects that should be excluded in
automatic cursor.setinputsizes() calls.

This is only used if bind_typing is BindTyping.SET_INPUT_SIZES

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)execute_sequence_format: Type[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[Any, ...]] | Type[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[List[Any]]]

either the ‘tuple’ or ‘list’ type, depending on what cursor.execute()
accepts for the second argument (they vary).

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)execution_ctx_cls: Type[[ExecutionContext](#sqlalchemy.engine.ExecutionContext)]

a [ExecutionContext](#sqlalchemy.engine.ExecutionContext) class used to handle statement execution

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)favor_returning_over_lastrowid: bool

for backends that support both a lastrowid and a RETURNING insert
strategy, favor RETURNING for simple single-int pk inserts.

cursor.lastrowid tends to be more performant on most backends.

    classmethod [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_async_dialect_cls(*url:URL*) → Type[[Dialect](#sqlalchemy.engine.Dialect)]

Given a URL, return the [Dialect](#sqlalchemy.engine.Dialect) that will be used by
an async engine.

By default this is an alias of [Dialect.get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls) and
just returns the cls. It may be used if a dialect provides
both a sync and async version under the same name, like the
`psycopg` driver.

Added in version 2.

See also

[Dialect.get_dialect_cls()](#sqlalchemy.engine.Dialect.get_dialect_cls)

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_check_constraints(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedCheckConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)]

Return information about check constraints in `table_name`.

Given a string `table_name` and an optional string `schema`, return
check constraint information as a list of dicts corresponding
to the [ReflectedCheckConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedCheckConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_check_constraints).

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_columns(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedColumn](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedColumn)]

Return information about columns in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return column
information as a list of dictionaries
corresponding to the [ReflectedColumn](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedColumn) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_columns).

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_default_isolation_level(*dbapi_conn:DBAPIConnection*) → Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']

Given a DBAPI connection, return its isolation level, or
a default isolation level if one cannot be retrieved.

This method may only raise NotImplementedError and
**must not raise any other exception**, as it is used implicitly upon
first connect.

The method **must return a value** for a dialect that supports
isolation level settings, as this level is what will be reverted
towards when a per-connection isolation level change is made.

The method defaults to using the [Dialect.get_isolation_level()](#sqlalchemy.engine.Dialect.get_isolation_level)
method unless overridden by a dialect.

Added in version 1.3.22.

     classmethod [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_dialect_cls(*url:URL*) → Type[[Dialect](#sqlalchemy.engine.Dialect)]

Given a URL, return the [Dialect](#sqlalchemy.engine.Dialect) that will be used.

This is a hook that allows an external plugin to provide functionality
around an existing dialect, by allowing the plugin to be loaded
from the url based on an entrypoint, and then the plugin returns
the actual dialect to be used.

By default this just returns the cls.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_dialect_pool_class(*url:URL*) → Type[[Pool](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool)]

return a Pool class to use for a given URL

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_driver_connection(*connection:DBAPIConnection*) → Any

Returns the connection object as returned by the external driver
package.

For normal dialects that use a DBAPI compliant driver this call
will just return the `connection` passed as argument.
For dialects that instead adapt a non DBAPI compliant driver, like
when adapting an asyncio driver, this call will return the
connection-like object as returned by the driver.

Added in version 1.4.24.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_foreign_keys(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)]

Return information about foreign_keys in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return foreign
key information as a list of dicts corresponding to the
[ReflectedForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint) dictionary.

This is an internal dialect method. Applications should use
`Inspector.get_foreign_keys()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_indexes(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedIndex](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedIndex)]

Return information about indexes in `table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name` and an optional string `schema`, return index
information as a list of dictionaries corresponding to the
[ReflectedIndex](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedIndex) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_indexes).

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_isolation_level(*dbapi_connection:DBAPIConnection*) → Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']

Given a DBAPI connection, return its isolation level.

When working with a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object,
the corresponding
DBAPI connection may be procured using the
[Connection.connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.connection) accessor.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level facilities;
these APIs should be preferred for most typical use cases.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_isolation_level_values(*dbapi_conn:DBAPIConnection*) → Sequence[Literal['SERIALIZABLE', 'REPEATABLE READ', 'READ COMMITTED', 'READ UNCOMMITTED', 'AUTOCOMMIT']]

return a sequence of string isolation level names that are accepted
by this dialect.

The available names should use the following conventions:

- use UPPERCASE names.   isolation level methods will accept lowercase
  names but these are normalized into UPPERCASE before being passed
  along to the dialect.
- separate words should be separated by spaces, not underscores, e.g.
  `REPEATABLE READ`.  isolation level names will have underscores
  converted to spaces before being passed along to the dialect.
- The names for the four standard isolation names to the extent that
  they are supported by the backend should be `READ UNCOMMITTED`,
  `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`
- if the dialect supports an autocommit option it should be provided
  using the isolation level name `AUTOCOMMIT`.
- Other isolation modes may also be present, provided that they
  are named in UPPERCASE and use spaces not underscores.

This function is used so that the default dialect can check that
a given isolation level parameter is valid, else raises an
[ArgumentError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.ArgumentError).

A DBAPI connection is passed to the method, in the unlikely event that
the dialect needs to interrogate the connection itself to determine
this list, however it is expected that most backends will return
a hardcoded list of values.  If the dialect supports “AUTOCOMMIT”,
that value should also be present in the sequence returned.

The method raises `NotImplementedError` by default.  If a dialect
does not implement this method, then the default dialect will not
perform any checking on a given isolation level value before passing
it onto the [Dialect.set_isolation_level()](#sqlalchemy.engine.Dialect.set_isolation_level) method.  This is
to allow backwards-compatibility with third party dialects that may
not yet be implementing this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_materialized_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of all materialized view names available in the
database.

This is an internal dialect method. Applications should use
`Inspector.get_materialized_view_names()`.

  Parameters:

**schema** –

schema name to query, if not the default schema.

Added in version 2.0.

       method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_check_constraints(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, List[[ReflectedCheckConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedCheckConstraint)]]]

Return information about check constraints in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_check_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_check_constraints).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_columns(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, List[[ReflectedColumn](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedColumn)]]]

Return information about columns in all tables in the
given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_columns()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_columns).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_foreign_keys(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, List[[ReflectedForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedForeignKeyConstraint)]]]

Return information about foreign_keys in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_multi_foreign_keys()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_indexes(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, List[[ReflectedIndex](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedIndex)]]]

Return information about indexes in in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_indexes()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_indexes).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_pk_constraint(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, [ReflectedPrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)]]

Return information about primary key constraints in
all tables in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_pk_constraint()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_pk_constraint).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_table_comment(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, [ReflectedTableComment](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedTableComment)]]

Return information about the table comment in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_multi_table_comment()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_table_options(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, Dict[str, Any]]]

Return a dictionary of options specified when the tables in the
given schema were created.

This is an internal dialect method. Applications should use
`Inspector.get_multi_table_options()`.

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_multi_unique_constraints(*connection:Connection*, ***, *schema:str|None=None*, *filter_names:Collection[str]|None=None*, ***kw:Any*) → Iterable[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[TableKey, List[[ReflectedUniqueConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)]]]

Return information about unique constraints in all tables
in the given `schema`.

This is an internal dialect method. Applications should use
[Inspector.get_multi_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_multi_unique_constraints).

Note

The `DefaultDialect` provides a default
implementation that will call the single table method for
each object returned by [Dialect.get_table_names()](#sqlalchemy.engine.Dialect.get_table_names),
[Dialect.get_view_names()](#sqlalchemy.engine.Dialect.get_view_names) or
[Dialect.get_materialized_view_names()](#sqlalchemy.engine.Dialect.get_materialized_view_names) depending on the
provided `kind`. Dialects that want to support a faster
implementation should implement this method.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_pk_constraint(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedPrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint)

Return information about the primary key constraint on
table_name`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`table_name`, and an optional string `schema`, return primary
key information as a dictionary corresponding to the
[ReflectedPrimaryKeyConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedPrimaryKeyConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_pk_constraint()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_pk_constraint).

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_schema_names(*connection:Connection*, ***kw:Any*) → List[str]

Return a list of all schema names available in the database.

This is an internal dialect method. Applications should use
`Inspector.get_schema_names()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_sequence_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of all sequence names available in the database.

This is an internal dialect method. Applications should use
`Inspector.get_sequence_names()`.

  Parameters:

**schema** – schema name to query, if not the default schema.

Added in version 1.4.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_table_comment(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → [ReflectedTableComment](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedTableComment)

Return the “comment” for the table identified by `table_name`.

Given a string `table_name` and an optional string `schema`, return
table comment information as a dictionary corresponding to the
[ReflectedTableComment](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedTableComment) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_table_comment()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_table_comment).

  Raise:

`NotImplementedError` for dialects that don’t support
comments.

Added in version 1.2.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_table_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of table names for `schema`.

This is an internal dialect method. Applications should use
`Inspector.get_table_names()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_table_options(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → Dict[str, Any]

Return a dictionary of options specified when `table_name`
was created.

This is an internal dialect method. Applications should use
`Inspector.get_table_options()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_temp_table_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of temporary table names on the given connection,
if supported by the underlying backend.

This is an internal dialect method. Applications should use
`Inspector.get_temp_table_names()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_temp_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of temporary view names on the given connection,
if supported by the underlying backend.

This is an internal dialect method. Applications should use
`Inspector.get_temp_view_names()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_unique_constraints(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → List[[ReflectedUniqueConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint)]

Return information about unique constraints in `table_name`.

Given a string `table_name` and an optional string `schema`, return
unique constraint information as a list of dicts corresponding
to the [ReflectedUniqueConstraint](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.interfaces.ReflectedUniqueConstraint) dictionary.

This is an internal dialect method. Applications should use
[Inspector.get_unique_constraints()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.get_unique_constraints).

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_view_definition(*connection:Connection*, *view_name:str*, *schema:str|None=None*, ***kw:Any*) → str

Return plain or materialized view definition.

This is an internal dialect method. Applications should use
`Inspector.get_view_definition()`.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), a string
`view_name`, and an optional string `schema`, return the view
definition.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)get_view_names(*connection:Connection*, *schema:str|None=None*, ***kw:Any*) → List[str]

Return a list of all non-materialized view names available in the
database.

This is an internal dialect method. Applications should use
`Inspector.get_view_names()`.

  Parameters:

**schema** – schema name to query, if not the default schema.

      method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)has_index(*connection:Connection*, *table_name:str*, *index_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

Check the existence of a particular index name in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string
`table_name` and string index name, return `True` if an index of
the given name on the given table exists, `False` otherwise.

The [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) implements this in terms of the
[Dialect.has_table()](#sqlalchemy.engine.Dialect.has_table) and [Dialect.get_indexes()](#sqlalchemy.engine.Dialect.get_indexes) methods,
however dialects can implement a more performant version.

This is an internal dialect method. Applications should use
`Inspector.has_index()`.

Added in version 1.4.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)has_schema(*connection:Connection*, *schema_name:str*, ***kw:Any*) → bool

Check the existence of a particular schema name in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string
`schema_name`, return `True` if a schema of the
given exists, `False` otherwise.

The [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) implements this by checking
the presence of `schema_name` among the schemas returned by
[Dialect.get_schema_names()](#sqlalchemy.engine.Dialect.get_schema_names),
however dialects can implement a more performant version.

This is an internal dialect method. Applications should use
`Inspector.has_schema()`.

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)has_sequence(*connection:Connection*, *sequence_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

Check the existence of a particular sequence in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object and a string
sequence_name, return `True` if the given sequence exists in
the database, `False` otherwise.

This is an internal dialect method. Applications should use
`Inspector.has_sequence()`.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)has_table(*connection:Connection*, *table_name:str*, *schema:str|None=None*, ***kw:Any*) → bool

For internal dialect use, check the existence of a particular table
or view in the database.

Given a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object, a string table_name and
optional schema name, return True if the given table exists in the
database, False otherwise.

This method serves as the underlying implementation of the
public facing [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) method, and is also used
internally to implement the “checkfirst” behavior for methods like
[Table.create()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.create) and [MetaData.create_all()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all).

Note

This method is used internally by SQLAlchemy, and is
published so that third-party dialects may provide an
implementation. It is **not** the public API for checking for table
presence. Please use the [Inspector.has_table()](https://docs.sqlalchemy.org/en/20/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table) method.

Changed in version 2.0::: [Dialect.has_table()](#sqlalchemy.engine.Dialect.has_table) now
formally supports checking for additional table-like objects:

- any type of views (plain or materialized)
- temporary tables of any kind

Previously, these two checks were not formally specified and
different dialects would vary in their behavior.   The dialect
testing suite now includes tests for all of these object types,
and dialects to the degree that the backing database supports views
or temporary tables should seek to support locating these objects
for full compliance.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)has_terminate: bool

Whether or not this dialect has a separate “terminate” implementation
that does not block or require awaiting.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)identifier_preparer: [IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer)

This element will refer to an instance of [IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer)
once a [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) has been constructed.

    classmethod [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)import_dbapi() → DBAPIModule

Import the DBAPI module that is used by this dialect.

The Python module object returned here will be assigned as an
instance variable to a constructed dialect under the name
`.dbapi`.

Changed in version 2.0: The [Dialect.import_dbapi()](#sqlalchemy.engine.Dialect.import_dbapi) class
method is renamed from the previous method `.Dialect.dbapi()`,
which would be replaced at dialect instantiation time by the
DBAPI module itself, thus using the same name in two different ways.
If a `.Dialect.dbapi()` classmethod is present on a third-party
dialect, it will be used and a deprecation warning will be emitted.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)include_set_input_sizes: Set[Any] | None

set of DBAPI type objects that should be included in
automatic cursor.setinputsizes() calls.

This is only used if bind_typing is BindTyping.SET_INPUT_SIZES

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)initialize(*connection:Connection*) → None

Called during strategized creation of the dialect with a
connection.

Allows dialects to configure options based on server version info or
other properties.

The connection passed here is a SQLAlchemy Connection object,
with full capabilities.

The initialize() method of the base dialect should be called via
super().

Note

as of SQLAlchemy 1.4, this method is called **before**
any [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) hooks are called.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)inline_comments: bool

Indicates the dialect supports comment DDL that’s inline with the
definition of a Table or Column.  If False, this implies that ALTER must
be used to set table and column comments.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insert_executemany_returning: bool

dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insert_executemany_returning_sort_by_parameter_order: bool

dialect / driver / database supports some means of providing
INSERT…RETURNING support when dialect.do_executemany() is used
along with the [Insert.returning.sort_by_parameter_order](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.returning.params.sort_by_parameter_order)
parameter being set.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insert_returning: bool

if the dialect supports RETURNING with INSERT

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insertmanyvalues_implicit_sentinel: InsertmanyvaluesSentinelOpts

Options indicating the database supports a form of bulk INSERT where
the autoincrement integer primary key can be reliably used as an ordering
for INSERTed rows.

Added in version 2.0.10.

See also

[Correlating RETURNING rows to parameter sets](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues-returning-order)

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insertmanyvalues_max_parameters: int

Alternate to insertmanyvalues_page_size, will additionally limit
page size based on number of parameters total in the statement.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)insertmanyvalues_page_size: int

Number of rows to render into an individual INSERT..VALUES() statement
for `ExecuteStyle.INSERTMANYVALUES` executions.

The default dialect defaults this to 1000.

Added in version 2.0.

See also

[Connection.execution_options.insertmanyvalues_page_size](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.insertmanyvalues_page_size) -
execution option available on [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection), statements

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)is_async: bool

Whether or not this dialect is intended for asyncio use.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)is_disconnect(*e:Error*, *connection:PoolProxiedConnection|DBAPIConnection|None*, *cursor:DBAPICursor|None*) → bool

Return True if the given DB-API error indicates an invalid
connection

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)label_length: int | None

optional user-defined max length for SQL labels

    classmethod [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)load_provisioning() → None

set up the provision.py module for this dialect.

For dialects that include a provision.py module that sets up
provisioning followers, this method should initiate that process.

A typical implementation would be:

```
@classmethod
def load_provisioning(cls):
    __import__("mydialect.provision")
```

The default method assumes a module named `provision.py` inside
the owning package of the current dialect, based on the `__module__`
attribute:

```
@classmethod
def load_provisioning(cls):
    package = ".".join(cls.__module__.split(".")[0:-1])
    try:
        __import__(package + ".provision")
    except ImportError:
        pass
```

Added in version 1.3.14.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)loaded_dbapi

same as .dbapi, but is never None; will raise an error if no
DBAPI was set up.

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)max_constraint_name_length: int | None

The maximum length of constraint names if different from
`max_identifier_length`.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)max_identifier_length: int

The maximum length of identifier names.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)max_index_name_length: int | None

The maximum length of index names if different from
`max_identifier_length`.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)name: str

identifying name for the dialect from a DBAPI-neutral point of view
(i.e. ‘sqlite’)

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)normalize_name(*name:str*) → str

convert the given name to lowercase if it is detected as
case insensitive.

This method is only used if the dialect defines
requires_name_normalize=True.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)on_connect() → Callable[[Any], None] | None

return a callable which sets up a newly created DBAPI connection.

The callable should accept a single argument “conn” which is the
DBAPI connection itself.  The inner callable has no
return value.

E.g.:

```
class MyDialect(default.DefaultDialect):
    # ...

    def on_connect(self):
        def do_on_connect(connection):
            connection.execute("SET SPECIAL FLAGS etc")

        return do_on_connect
```

This is used to set dialect-wide per-connection options such as
isolation modes, Unicode modes, etc.

The “do_on_connect” callable is invoked by using the
[PoolEvents.connect()](https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.PoolEvents.connect) event
hook, then unwrapping the DBAPI connection and passing it into the
callable.

Changed in version 1.4: the on_connect hook is no longer called twice
for the first connection of a dialect.  The on_connect hook is still
called before the [Dialect.initialize()](#sqlalchemy.engine.Dialect.initialize) method however.

Changed in version 1.4.3: the on_connect hook is invoked from a new
method on_connect_url that passes the URL that was used to create
the connect args.   Dialects can implement on_connect_url instead
of on_connect if they need the URL object that was used for the
connection in order to get additional context.

If None is returned, no event listener is generated.

  Returns:

a callable that accepts a single DBAPI connection as an
argument, or None.

See also

[Dialect.connect()](#sqlalchemy.engine.Dialect.connect) - allows the DBAPI `connect()` sequence
itself to be controlled.

[Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url) - supersedes
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) to also receive the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object in context.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)on_connect_url(*url:URL*) → Callable[[Any], Any] | None

return a callable which sets up a newly created DBAPI connection.

This method is a new hook that supersedes the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method when implemented by a
dialect.   When not implemented by a dialect, it invokes the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method directly to maintain
compatibility with existing dialects.   There is no deprecation
for [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) expected.

The callable should accept a single argument “conn” which is the
DBAPI connection itself.  The inner callable has no
return value.

E.g.:

```
class MyDialect(default.DefaultDialect):
    # ...

    def on_connect_url(self, url):
        def do_on_connect(connection):
            connection.execute("SET SPECIAL FLAGS etc")

        return do_on_connect
```

This is used to set dialect-wide per-connection options such as
isolation modes, Unicode modes, etc.

This method differs from [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) in that
it is passed the [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object that’s relevant to the
connect args.  Normally the only way to get this is from the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) hook is to look on the
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) itself, however this URL object may have been
replaced by plugins.

Note

The default implementation of
[Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url) is to invoke the
[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect) method. Therefore if a dialect
implements this method, the [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)
method **will not be called** unless the overriding dialect calls
it directly from here.

Added in version 1.4.3: added [Dialect.on_connect_url()](#sqlalchemy.engine.Dialect.on_connect_url)
which normally calls into [Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect).

   Parameters:

**url** – a [URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) object representing the
[URL](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.URL) that was passed to the
[Dialect.create_connect_args()](#sqlalchemy.engine.Dialect.create_connect_args) method.

  Returns:

a callable that accepts a single DBAPI connection as an
argument, or None.

See also

[Dialect.on_connect()](#sqlalchemy.engine.Dialect.on_connect)

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)paramstyle: str

the paramstyle to be used (some DB-APIs support multiple
paramstyles).

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)positional: bool

True if the paramstyle for this Dialect is positional.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)preexecute_autoincrement_sequences: bool

True if ‘implicit’ primary key functions must be executed separately
in order to get their value, if RETURNING is not used.

This is currently oriented towards PostgreSQL when the
`implicit_returning=False` parameter is used on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
object.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)preparer: Type[[IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer)]

a [IdentifierPreparer](#sqlalchemy.sql.compiler.IdentifierPreparer) class used to
quote identifiers.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)reflection_options: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[str] = ()

Sequence of string names indicating keyword arguments that can be
established on a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object which will be passed as
“reflection options” when using [Table.autoload_with](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table.params.autoload_with).

Current example is “oracle_resolve_synonyms” in the Oracle Database
dialects.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)requires_name_normalize: bool

Indicates symbol names are returned by the database in
UPPERCASED if they are case insensitive within the database.
If this is True, the methods normalize_name()
and denormalize_name() must be provided.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)reset_isolation_level(*dbapi_connection:DBAPIConnection*) → None

Given a DBAPI connection, revert its isolation to the default.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
isolation level facilities; these APIs should be preferred for
most typical use cases.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)returns_native_bytes: bool

indicates if Python bytes() objects are returned natively by the
driver for SQL “binary” datatypes.

Added in version 2.0.11.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)sequences_optional: bool

If True, indicates if the [Sequence.optional](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence.params.optional)
parameter on the [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence) construct
should signal to not generate a CREATE SEQUENCE. Applies only to
dialects that support sequences. Currently used only to allow PostgreSQL
SERIAL to be used on a column that specifies Sequence() for usage on
other backends.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)server_side_cursors: bool

deprecated; indicates if the dialect should attempt to use server
side cursors by default

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)server_version_info: [Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[Any, ...] | None

a tuple containing a version number for the DB backend in use.

This value is only available for supporting dialects, and is
typically populated during the initial connection to the database.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)set_connection_execution_options(*connection:Connection*, *opts:CoreExecuteOptionsParameter*) → None

Establish execution options for a given connection.

This is implemented by [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) in order to implement
the [Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level)
execution option.  Dialects can intercept various execution options
which may need to modify state on a particular DBAPI connection.

Added in version 1.4.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)set_engine_execution_options(*engine:Engine*, *opts:CoreExecuteOptionsParameter*) → None

Establish execution options for a given engine.

This is implemented by [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect) to establish
event hooks for new [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) instances created
by the given [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) which will then invoke the
[Dialect.set_connection_execution_options()](#sqlalchemy.engine.Dialect.set_connection_execution_options) method for that
connection.

    method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)set_isolation_level(*dbapi_connection:DBAPIConnection*, *level:Literal['SERIALIZABLE','REPEATABLEREAD','READCOMMITTED','READUNCOMMITTED','AUTOCOMMIT']*) → None

Given a DBAPI connection, set its isolation level.

Note that this is a dialect-level method which is used as part
of the implementation of the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) and
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)
isolation level facilities; these APIs should be preferred for
most typical use cases.

If the dialect also implements the
[Dialect.get_isolation_level_values()](#sqlalchemy.engine.Dialect.get_isolation_level_values) method, then the given
level is guaranteed to be one of the string names within that sequence,
and the method will not need to anticipate a lookup failure.

See also

[Connection.get_isolation_level()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.get_isolation_level)
- view current level

[Connection.default_isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level)
- view default level

[Connection.execution_options.isolation_level](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) -
set per [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) isolation level

[create_engine.isolation_level](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.isolation_level) -
set per [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) isolation level

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)skip_autocommit_rollback: bool

Whether or not the [create_engine.skip_autocommit_rollback](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.skip_autocommit_rollback)
parameter was set.

Added in version 2.0.43.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)statement_compiler: Type[[SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler)]

a [Compiled](#sqlalchemy.engine.Compiled) class used to compile SQL statements

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_alter: bool

`True` if the database supports `ALTER TABLE` - used only for
generating foreign key constraints in certain circumstances

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_comments: bool

Indicates the dialect supports comment DDL on tables and columns.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_constraint_comments: bool

Indicates if the dialect supports comment DDL on constraints.

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_default_metavalue: bool

dialect supports INSERT…(col) VALUES (DEFAULT) syntax.

Most databases support this in some way, e.g. SQLite supports it using
`VALUES (NULL)`.    MS SQL Server supports the syntax also however
is the only included dialect where we have this disabled, as
MSSQL does not support the field for the IDENTITY column, which is
usually where we like to make use of the feature.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_default_values: bool

dialect supports INSERT… DEFAULT VALUES syntax

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_empty_insert: bool

dialect supports INSERT () VALUES (), i.e. a plain INSERT with no
columns in it.

This is not usually supported; an “empty” insert is typically
suited using either “INSERT..DEFAULT VALUES” or
“INSERT … (col) VALUES (DEFAULT)”.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_identity_columns: bool

target database supports IDENTITY

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_multivalues_insert: bool

Target database supports INSERT…VALUES with multiple value
sets, i.e. INSERT INTO table (cols) VALUES (…), (…), (…), …

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_native_boolean: bool

Indicates if the dialect supports a native boolean construct.
This will prevent [Boolean](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Boolean) from generating a CHECK
constraint when that type is used.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_native_decimal: bool

indicates if Decimal objects are handled and returned for precision
numeric types, or if floats are returned

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_native_enum: bool

Indicates if the dialect supports a native ENUM construct.
This will prevent [Enum](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum) from generating a CHECK
constraint when that type is used in “native” mode.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_native_uuid: bool

indicates if Python UUID() objects are handled natively by the
driver for SQL UUID datatypes.

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_sane_multi_rowcount: bool

Indicate whether the dialect properly implements rowcount for
`UPDATE` and `DELETE` statements when executed via
executemany.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_sane_rowcount: bool

Indicate whether the dialect properly implements rowcount for
`UPDATE` and `DELETE` statements.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_sequences: bool

Indicates if the dialect supports CREATE SEQUENCE or similar.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_server_side_cursors: generic_fn_descriptor[bool] | bool

indicates if the dialect supports server side cursors

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_simple_order_by_label: bool

target database supports ORDER BY <labelname>, where <labelname>
refers to a label in the columns clause of the SELECT

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)supports_statement_cache: bool = True

indicates if this dialect supports caching.

All dialects that are compatible with statement caching should set this
flag to True directly on each dialect class and subclass that supports
it.  SQLAlchemy tests that this flag is locally present on each dialect
subclass before it will use statement caching.  This is to provide
safety for legacy or new dialects that are not yet fully tested to be
compliant with SQL statement caching.

Added in version 1.4.5.

See also

[Caching for Third Party Dialects](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-thirdparty-caching)

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)tuple_in_values: bool

target database supports tuple IN, i.e. (x, y) IN ((q, p), (r, z))

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)type_compiler: Any

legacy; this is a TypeCompiler class at the class level, a
TypeCompiler instance at the instance level.

Refer to type_compiler_instance instead.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)type_compiler_cls: ClassVar[Type[TypeCompiler]]

a [Compiled](#sqlalchemy.engine.Compiled) class used to compile SQL type objects

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)type_compiler_instance: TypeCompiler

instance of a [Compiled](#sqlalchemy.engine.Compiled) class used to compile SQL type
objects

Added in version 2.0.

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)type_descriptor(*typeobj:TypeEngine[_T]*) → [TypeEngine](https://docs.sqlalchemy.org/en/20/core/type_api.html#sqlalchemy.types.TypeEngine)[_T]

Transform a generic type to a dialect-specific type.

Dialect classes will usually use the
`adapt_type()` function in the types module to
accomplish this.

The returned result is cached *per dialect class* so can
contain no dialect-instance state.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)update_executemany_returning: bool

dialect supports UPDATE..RETURNING with executemany.

    attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)update_returning: bool

if the dialect supports RETURNING with UPDATE

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)update_returning_multifrom: bool

if the dialect supports RETURNING with UPDATE..FROM

Added in version 2.0.

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)use_insertmanyvalues: bool

if True, indicates “insertmanyvalues” functionality should be used
to allow for `insert_executemany_returning` behavior, if possible.

In practice, setting this to True means:

if `supports_multivalues_insert`, `insert_returning` and
`use_insertmanyvalues` are all True, the SQL compiler will produce
an INSERT that will be interpreted by the [DefaultDialect](#sqlalchemy.engine.default.DefaultDialect)
as an `ExecuteStyle.INSERTMANYVALUES` execution that allows
for INSERT of many rows with RETURNING by rewriting a single-row
INSERT statement to have multiple VALUES clauses, also executing
the statement multiple times for a series of batches when large numbers
of rows are given.

The parameter is False for the default dialect, and is set to True for
SQLAlchemy internal dialects SQLite, MySQL/MariaDB, PostgreSQL, SQL Server.
It remains at False for Oracle Database, which provides native “executemany
with RETURNING” support and also does not support
`supports_multivalues_insert`.  For MySQL/MariaDB, those MySQL dialects
that don’t support RETURNING will not report
`insert_executemany_returning` as True.

Added in version 2.0.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

     attribute [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)use_insertmanyvalues_wo_returning: bool

if True, and use_insertmanyvalues is also True, INSERT statements
that don’t include RETURNING will also use “insertmanyvalues”.

Added in version 2.0.

See also

[“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)

     method [sqlalchemy.engine.Dialect.](#sqlalchemy.engine.Dialect)validate_identifier(*ident:str*) → None

Validates an identifier name, raising an exception if invalid

     class sqlalchemy.engine.default.DefaultExecutionContext

*inherits from* [sqlalchemy.engine.interfaces.ExecutionContext](#sqlalchemy.engine.ExecutionContext)

| Member Name | Description |
| --- | --- |
| compiled | if passed to constructor, sqlalchemy.engine.base.Compiled object
being executed |
| connection | Connection object which can be freely used by default value
generators to execute SQL.  This Connection should reference the
same underlying connection/transactional resources of
root_connection. |
| create_cursor() | Return a new cursor generated from this ExecutionContext’s
connection. |
| current_parameters | A dictionary of parameters applied to the current row. |
| cursor | DB-API cursor procured from the connection |
| dialect | dialect which created this ExecutionContext. |
| engine | engine which the Connection is associated with |
| execute_style | the style of DBAPI cursor method that will be used to execute
a statement. |
| execution_options | Execution options associated with the current statement execution |
| fetchall_for_returning() | For a RETURNING result, deliver cursor.fetchall() from the
DBAPI cursor. |
| get_current_parameters() | Return a dictionary of parameters applied to the current row. |
| get_lastrowid() | return self.cursor.lastrowid, or equivalent, after an INSERT. |
| get_out_parameter_values() | Return a sequence of OUT parameter values from a cursor. |
| get_result_processor() | Return a ‘result processor’ for a given type as present in
cursor.description. |
| handle_dbapi_exception() | Receive a DBAPI exception which occurred upon execute, result
fetch, etc. |
| invoked_statement | The Executable statement object that was given in the first place. |
| isinsert | True if the statement is an INSERT. |
| isupdate | True if the statement is an UPDATE. |
| lastrow_has_defaults() | Return True if the last INSERT or UPDATE row contained
inlined or database-side defaults. |
| no_parameters | True if the execution style does not use parameters |
| parameters | bind parameters passed to the execute() or exec_driver_sql() methods. |
| post_exec() | Called after the execution of a compiled statement. |
| postfetch_cols | a list of Column objects for which a server-side default or
inline SQL expression value was fired off.  Applies to inserts
and updates. |
| pre_exec() | Called before an execution of a compiled statement. |
| prefetch_cols | a list of Column objects for which a client-side default
was fired off.  Applies to inserts and updates. |
| root_connection | Connection object which is the source of this ExecutionContext. |

   attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)compiled: [Compiled](#sqlalchemy.engine.Compiled) | None = None

if passed to constructor, sqlalchemy.engine.base.Compiled object
being executed

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)connection

Connection object which can be freely used by default value
generators to execute SQL.  This Connection should reference the
same underlying connection/transactional resources of
root_connection.

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)create_cursor() → [DBAPICursor](#sqlalchemy.engine.interfaces.DBAPICursor)

Return a new cursor generated from this ExecutionContext’s
connection.

Some dialects may wish to change the behavior of
connection.cursor(), such as postgresql which may return a PG
“server side” cursor.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)current_parameters: _CoreSingleExecuteParams | None = None

A dictionary of parameters applied to the current row.

This attribute is only available in the context of a user-defined default
generation function, e.g. as described at [Context-Sensitive Default Functions](https://docs.sqlalchemy.org/en/20/core/defaults.html#context-default-functions).
It consists of a dictionary which includes entries for each column/value
pair that is to be part of the INSERT or UPDATE statement. The keys of the
dictionary will be the key value of each [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
which is usually
synonymous with the name.

Note that the [DefaultExecutionContext.current_parameters](#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters) attribute
does not accommodate for the “multi-values” feature of the
[Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values) method.  The
[DefaultExecutionContext.get_current_parameters()](#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters) method should be
preferred.

See also

[DefaultExecutionContext.get_current_parameters()](#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters)

[Context-Sensitive Default Functions](https://docs.sqlalchemy.org/en/20/core/defaults.html#context-default-functions)

     attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)cursor: [DBAPICursor](#sqlalchemy.engine.interfaces.DBAPICursor)

DB-API cursor procured from the connection

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)dialect: [Dialect](#sqlalchemy.engine.Dialect)

dialect which created this ExecutionContext.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)engine

engine which the Connection is associated with

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)execute_style: ExecuteStyle = 0

the style of DBAPI cursor method that will be used to execute
a statement.

Added in version 2.0.

     property executemany    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)execution_options: _ExecuteOptions = {}

Execution options associated with the current statement execution

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)fetchall_for_returning(*cursor*)

For a RETURNING result, deliver cursor.fetchall() from the
DBAPI cursor.

This is a dialect-specific hook for dialects that have special
considerations when calling upon the rows delivered for a
“RETURNING” statement.   Default implementation is
`cursor.fetchall()`.

This hook is currently used only by the [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues)
feature.   Dialects that don’t set `use_insertmanyvalues=True`
don’t need to consider this hook.

Added in version 2.0.10.

     method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)get_current_parameters(*isolate_multiinsert_groups=True*)

Return a dictionary of parameters applied to the current row.

This method can only be used in the context of a user-defined default
generation function, e.g. as described at
[Context-Sensitive Default Functions](https://docs.sqlalchemy.org/en/20/core/defaults.html#context-default-functions). When invoked, a dictionary is
returned which includes entries for each column/value pair that is part
of the INSERT or UPDATE statement. The keys of the dictionary will be
the key value of each [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column),
which is usually synonymous
with the name.

  Parameters:

**isolate_multiinsert_groups=True** – indicates that multi-valued
INSERT constructs created using [Insert.values()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert.values)
should be
handled by returning only the subset of parameters that are local
to the current column default invocation.   When `False`, the
raw parameters of the statement are returned including the
naming convention used in the case of multi-valued INSERT.

Added in version 1.2: added
[DefaultExecutionContext.get_current_parameters()](#sqlalchemy.engine.default.DefaultExecutionContext.get_current_parameters)
which provides more functionality over the existing
[DefaultExecutionContext.current_parameters](#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters)
attribute.

See also

[DefaultExecutionContext.current_parameters](#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters)

[Context-Sensitive Default Functions](https://docs.sqlalchemy.org/en/20/core/defaults.html#context-default-functions)

     method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)get_lastrowid() → int

return self.cursor.lastrowid, or equivalent, after an INSERT.

This may involve calling special cursor functions, issuing a new SELECT
on the cursor (or a new one), or returning a stored value that was
calculated within post_exec().

This function will only be called for dialects which support “implicit”
primary key generation, keep preexecute_autoincrement_sequences set to
False, and when no explicit id value was bound to the statement.

The function is called once for an INSERT statement that would need to
return the last inserted primary key for those dialects that make use
of the lastrowid concept.  In these cases, it is called directly after
[ExecutionContext.post_exec()](#sqlalchemy.engine.ExecutionContext.post_exec).

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)get_out_parameter_values(*names*)

Return a sequence of OUT parameter values from a cursor.

For dialects that support OUT parameters, this method will be called
when there is a [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler) object which has the
[SQLCompiler.has_out_parameters](#sqlalchemy.sql.compiler.SQLCompiler.has_out_parameters) flag set.  This flag in turn
will be set to True if the statement itself has [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)
objects that have the `.isoutparam` flag set which are consumed by
the `SQLCompiler.visit_bindparam()` method.  If the dialect
compiler produces [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with `.isoutparam`
set which are not handled by `SQLCompiler.visit_bindparam()`, it
should set this flag explicitly.

The list of names that were rendered for each bound parameter
is passed to the method.  The method should then return a sequence of
values corresponding to the list of parameter objects. Unlike in
previous SQLAlchemy versions, the values can be the **raw values** from
the DBAPI; the execution context will apply the appropriate type
handler based on what’s present in self.compiled.binds and update the
values.  The processed dictionary will then be made available via the
`.out_parameters` collection on the result object.  Note that
SQLAlchemy 1.4 has multiple kinds of result object as part of the 2.0
transition.

Added in version 1.4: - added
[ExecutionContext.get_out_parameter_values()](#sqlalchemy.engine.ExecutionContext.get_out_parameter_values), which is invoked
automatically by the [DefaultExecutionContext](#sqlalchemy.engine.default.DefaultExecutionContext) when there
are [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with the `.isoutparam` flag
set.  This replaces the practice of setting out parameters within
the now-removed `get_result_proxy()` method.

     method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)get_result_processor(*type_:TypeEngine[Any]*, *colname:str*, *coltype:DBAPIType*) → _ResultProcessorType[Any] | None

Return a ‘result processor’ for a given type as present in
cursor.description.

This has a default implementation that dialects can override
for context-sensitive result type handling.

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)handle_dbapi_exception(*e*)

Receive a DBAPI exception which occurred upon execute, result
fetch, etc.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)invoked_statement: [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) | None = None

The Executable statement object that was given in the first place.

This should be structurally equivalent to compiled.statement, but not
necessarily the same object as in a caching scenario the compiled form
will have been extracted from the cache.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)isinsert = False

True if the statement is an INSERT.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)isupdate = False

True if the statement is an UPDATE.

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)lastrow_has_defaults() → bool

Return True if the last INSERT or UPDATE row contained
inlined or database-side defaults.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)no_parameters

True if the execution style does not use parameters

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)parameters: _DBAPIMultiExecuteParams

bind parameters passed to the execute() or exec_driver_sql() methods.

These are always stored as a list of parameter entries.  A single-element
list corresponds to a `cursor.execute()` call and a multiple-element
list corresponds to `cursor.executemany()`, except in the case
of `ExecuteStyle.INSERTMANYVALUES` which will use
`cursor.execute()` one or more times.

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)post_exec()

Called after the execution of a compiled statement.

If a compiled statement was passed to this ExecutionContext,
the last_insert_ids, last_inserted_params, etc.
datamembers should be available after this method completes.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)postfetch_cols

a list of Column objects for which a server-side default or
inline SQL expression value was fired off.  Applies to inserts
and updates.

    method [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)pre_exec()

Called before an execution of a compiled statement.

If a compiled statement was passed to this ExecutionContext,
the statement and parameters datamembers must be
initialized after this statement is complete.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)prefetch_cols

a list of Column objects for which a client-side default
was fired off.  Applies to inserts and updates.

    attribute [sqlalchemy.engine.default.DefaultExecutionContext.](#sqlalchemy.engine.default.DefaultExecutionContext)root_connection: [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Connection object which is the source of this ExecutionContext.

     class sqlalchemy.engine.ExecutionContext

A messenger object for a Dialect that corresponds to a single
execution.

| Member Name | Description |
| --- | --- |
| compiled | if passed to constructor, sqlalchemy.engine.base.Compiled object
being executed |
| connection | Connection object which can be freely used by default value
generators to execute SQL.  This Connection should reference the
same underlying connection/transactional resources of
root_connection. |
| create_cursor() | Return a new cursor generated from this ExecutionContext’s
connection. |
| cursor | DB-API cursor procured from the connection |
| dialect | dialect which created this ExecutionContext. |
| engine | engine which the Connection is associated with |
| execute_style | the style of DBAPI cursor method that will be used to execute
a statement. |
| executemany | True if the context has a list of more than one parameter set. |
| execution_options | Execution options associated with the current statement execution |
| fetchall_for_returning() | For a RETURNING result, deliver cursor.fetchall() from the
DBAPI cursor. |
| fire_sequence() | given aSequence, invoke it and return the next int
value |
| get_out_parameter_values() | Return a sequence of OUT parameter values from a cursor. |
| get_rowcount() | Return the DBAPIcursor.rowcountvalue, or in some
cases an interpreted value. |
| handle_dbapi_exception() | Receive a DBAPI exception which occurred upon execute, result
fetch, etc. |
| invoked_statement | The Executable statement object that was given in the first place. |
| isinsert | True if the statement is an INSERT. |
| isupdate | True if the statement is an UPDATE. |
| lastrow_has_defaults() | Return True if the last INSERT or UPDATE row contained
inlined or database-side defaults. |
| no_parameters | True if the execution style does not use parameters |
| parameters | bind parameters passed to the execute() or exec_driver_sql() methods. |
| post_exec() | Called after the execution of a compiled statement. |
| postfetch_cols | a list of Column objects for which a server-side default or
inline SQL expression value was fired off.  Applies to inserts
and updates. |
| pre_exec() | Called before an execution of a compiled statement. |
| prefetch_cols | a list of Column objects for which a client-side default
was fired off.  Applies to inserts and updates. |
| root_connection | Connection object which is the source of this ExecutionContext. |
| statement | string version of the statement to be executed.  Is either
passed to the constructor, or must be created from the
sql.Compiled object by the time pre_exec() has completed. |

   attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)compiled: [Compiled](#sqlalchemy.engine.Compiled) | None

if passed to constructor, sqlalchemy.engine.base.Compiled object
being executed

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)connection: [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Connection object which can be freely used by default value
generators to execute SQL.  This Connection should reference the
same underlying connection/transactional resources of
root_connection.

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)create_cursor() → [DBAPICursor](#sqlalchemy.engine.interfaces.DBAPICursor)

Return a new cursor generated from this ExecutionContext’s
connection.

Some dialects may wish to change the behavior of
connection.cursor(), such as postgresql which may return a PG
“server side” cursor.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)cursor: [DBAPICursor](#sqlalchemy.engine.interfaces.DBAPICursor)

DB-API cursor procured from the connection

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)dialect: [Dialect](#sqlalchemy.engine.Dialect)

dialect which created this ExecutionContext.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)engine: [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine)

engine which the Connection is associated with

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)execute_style: ExecuteStyle

the style of DBAPI cursor method that will be used to execute
a statement.

Added in version 2.0.

     attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)executemany: bool

True if the context has a list of more than one parameter set.

Historically this attribute links to whether `cursor.execute()` or
`cursor.executemany()` will be used.  It also can now mean that
“insertmanyvalues” may be used which indicates one or more
`cursor.execute()` calls.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)execution_options: _ExecuteOptions

Execution options associated with the current statement execution

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)fetchall_for_returning(*cursor:DBAPICursor*) → Sequence[Any]

For a RETURNING result, deliver cursor.fetchall() from the
DBAPI cursor.

This is a dialect-specific hook for dialects that have special
considerations when calling upon the rows delivered for a
“RETURNING” statement.   Default implementation is
`cursor.fetchall()`.

This hook is currently used only by the [insertmanyvalues](https://docs.sqlalchemy.org/en/20/glossary.html#term-insertmanyvalues)
feature.   Dialects that don’t set `use_insertmanyvalues=True`
don’t need to consider this hook.

Added in version 2.0.10.

     method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)fire_sequence(*seq:Sequence_SchemaItem*, *type_:Integer*) → int

given a [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence), invoke it and return the next int
value

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)get_out_parameter_values(*out_param_names:Sequence[str]*) → Sequence[Any]

Return a sequence of OUT parameter values from a cursor.

For dialects that support OUT parameters, this method will be called
when there is a [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler) object which has the
[SQLCompiler.has_out_parameters](#sqlalchemy.sql.compiler.SQLCompiler.has_out_parameters) flag set.  This flag in turn
will be set to True if the statement itself has [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)
objects that have the `.isoutparam` flag set which are consumed by
the `SQLCompiler.visit_bindparam()` method.  If the dialect
compiler produces [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with `.isoutparam`
set which are not handled by `SQLCompiler.visit_bindparam()`, it
should set this flag explicitly.

The list of names that were rendered for each bound parameter
is passed to the method.  The method should then return a sequence of
values corresponding to the list of parameter objects. Unlike in
previous SQLAlchemy versions, the values can be the **raw values** from
the DBAPI; the execution context will apply the appropriate type
handler based on what’s present in self.compiled.binds and update the
values.  The processed dictionary will then be made available via the
`.out_parameters` collection on the result object.  Note that
SQLAlchemy 1.4 has multiple kinds of result object as part of the 2.0
transition.

Added in version 1.4: - added
[ExecutionContext.get_out_parameter_values()](#sqlalchemy.engine.ExecutionContext.get_out_parameter_values), which is invoked
automatically by the [DefaultExecutionContext](#sqlalchemy.engine.default.DefaultExecutionContext) when there
are [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter) objects with the `.isoutparam` flag
set.  This replaces the practice of setting out parameters within
the now-removed `get_result_proxy()` method.

     method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)get_rowcount() → int | None

Return the DBAPI `cursor.rowcount` value, or in some
cases an interpreted value.

See [CursorResult.rowcount](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult.rowcount) for details on this.

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)handle_dbapi_exception(*e:BaseException*) → None

Receive a DBAPI exception which occurred upon execute, result
fetch, etc.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)invoked_statement: [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) | None

The Executable statement object that was given in the first place.

This should be structurally equivalent to compiled.statement, but not
necessarily the same object as in a caching scenario the compiled form
will have been extracted from the cache.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)isinsert: bool

True if the statement is an INSERT.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)isupdate: bool

True if the statement is an UPDATE.

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)lastrow_has_defaults() → bool

Return True if the last INSERT or UPDATE row contained
inlined or database-side defaults.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)no_parameters: bool

True if the execution style does not use parameters

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)parameters: _AnyMultiExecuteParams

bind parameters passed to the execute() or exec_driver_sql() methods.

These are always stored as a list of parameter entries.  A single-element
list corresponds to a `cursor.execute()` call and a multiple-element
list corresponds to `cursor.executemany()`, except in the case
of `ExecuteStyle.INSERTMANYVALUES` which will use
`cursor.execute()` one or more times.

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)post_exec() → None

Called after the execution of a compiled statement.

If a compiled statement was passed to this ExecutionContext,
the last_insert_ids, last_inserted_params, etc.
datamembers should be available after this method completes.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)postfetch_cols: util.generic_fn_descriptor[[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] | None]

a list of Column objects for which a server-side default or
inline SQL expression value was fired off.  Applies to inserts
and updates.

    method [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)pre_exec() → None

Called before an execution of a compiled statement.

If a compiled statement was passed to this ExecutionContext,
the statement and parameters datamembers must be
initialized after this statement is complete.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)prefetch_cols: util.generic_fn_descriptor[[Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] | None]

a list of Column objects for which a client-side default
was fired off.  Applies to inserts and updates.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)root_connection: [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Connection object which is the source of this ExecutionContext.

    attribute [sqlalchemy.engine.ExecutionContext.](#sqlalchemy.engine.ExecutionContext)statement: str

string version of the statement to be executed.  Is either
passed to the constructor, or must be created from the
sql.Compiled object by the time pre_exec() has completed.

     class sqlalchemy.sql.compiler.ExpandedState

*inherits from* `builtins.tuple`

represents state to use when producing “expanded” and
“post compile” bound parameters for a statement.

“expanded” parameters are parameters that are generated at
statement execution time to suit a number of parameters passed, the most
prominent example being the individual elements inside of an IN expression.

“post compile” parameters are parameters where the SQL literal value
will be rendered into the SQL statement at execution time, rather than
being passed as separate parameters to the driver.

To create an [ExpandedState](#sqlalchemy.sql.compiler.ExpandedState) instance, use the
[SQLCompiler.construct_expanded_state()](#sqlalchemy.sql.compiler.SQLCompiler.construct_expanded_state) method on any
[SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler) instance.

| Member Name | Description |
| --- | --- |
| parameter_expansion | Mapping representing the intermediary link from original parameter
name to list of “expanded” parameter names, for those parameters that
were expanded. |
| parameters | Parameter dictionary with parameters fully expanded. |
| positiontup | Sequence of string names indicating the order of positional
parameters |
| processors | mapping of bound value processors |
| statement | String SQL statement with parameters fully expanded |

   property additional_parameters: _CoreSingleExecuteParams

synonym for [ExpandedState.parameters](#sqlalchemy.sql.compiler.ExpandedState.parameters).

    attribute [sqlalchemy.sql.compiler.ExpandedState.](#sqlalchemy.sql.compiler.ExpandedState)parameter_expansion: Mapping[str, List[str]]

Mapping representing the intermediary link from original parameter
name to list of “expanded” parameter names, for those parameters that
were expanded.

    attribute [sqlalchemy.sql.compiler.ExpandedState.](#sqlalchemy.sql.compiler.ExpandedState)parameters: _CoreSingleExecuteParams

Parameter dictionary with parameters fully expanded.

For a statement that uses named parameters, this dictionary will map
exactly to the names in the statement.  For a statement that uses
positional parameters, the [ExpandedState.positional_parameters](#sqlalchemy.sql.compiler.ExpandedState.positional_parameters)
will yield a tuple with the positional parameter set.

    property positional_parameters: Tuple[Any, ...]

Tuple of positional parameters, for statements that were compiled
using a positional paramstyle.

    attribute [sqlalchemy.sql.compiler.ExpandedState.](#sqlalchemy.sql.compiler.ExpandedState)positiontup: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[str] | None

Sequence of string names indicating the order of positional
parameters

    attribute [sqlalchemy.sql.compiler.ExpandedState.](#sqlalchemy.sql.compiler.ExpandedState)processors: Mapping[str, _BindProcessorType[Any]]

mapping of bound value processors

    attribute [sqlalchemy.sql.compiler.ExpandedState.](#sqlalchemy.sql.compiler.ExpandedState)statement: str

String SQL statement with parameters fully expanded

     class sqlalchemy.sql.compiler.GenericTypeCompiler

*inherits from* `sqlalchemy.sql.compiler.TypeCompiler`

| Member Name | Description |
| --- | --- |
| ensure_kwarg | a regular expression that indicates method names for which the method
should accept**kwarguments. |

   attribute [sqlalchemy.sql.compiler.GenericTypeCompiler.](#sqlalchemy.sql.compiler.GenericTypeCompiler)ensure_kwarg: str = 'visit_\\w+'

*inherited from the* `TypeCompiler.ensure_kwarg` *attribute of* `TypeCompiler`

a regular expression that indicates method names for which the method
should accept `**kw` arguments.

The class will scan for methods matching the name template and decorate
them if necessary to ensure `**kw` parameters are accepted.

     class sqlalchemy.log.Identified    class sqlalchemy.sql.compiler.IdentifierPreparer

Handle quoting and case-folding of identifiers based on options.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newIdentifierPreparerobject. |
| format_column() | Prepare a quoted column name. |
| format_label_name() | Prepare a quoted column name. |
| format_schema() | Prepare a quoted schema name. |
| format_table() | Prepare a quoted table and schema name. |
| format_table_seq() | Format table name and schema as a tuple. |
| quote() | Conditionally quote an identifier. |
| quote_identifier() | Quote an identifier. |
| quote_schema() | Conditionally quote a schema name. |
| schema_for_object | Return the .schema attribute for an object. |
| unformat_identifiers() | Unpack ‘schema.table.column’-like strings into components. |
| validate_sql_phrase() | keyword sequence filter. |

   method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)__init__(*dialect:Dialect*, *initial_quote:str='"'*, *final_quote:str|None=None*, *escape_quote:str='"'*, *quote_case_sensitive_collations:bool=True*, *omit_schema:bool=False*)

Construct a new `IdentifierPreparer` object.

  initial_quote

Character that begins a delimited identifier.

  final_quote

Character that ends a delimited identifier. Defaults to
initial_quote.

  omit_schema

Prevent prepending schema name. Useful for databases that do
not support schemae.

      method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)format_column(*column:ColumnElement[Any]*, *use_table:bool=False*, *name:str|None=None*, *table_name:str|None=None*, *use_schema:bool=False*, *anon_map:Mapping[str,Any]|None=None*) → str

Prepare a quoted column name.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)format_label_name(*name*, *anon_map=None*)

Prepare a quoted column name.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)format_schema(*name*)

Prepare a quoted schema name.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)format_table(*table:FromClause*, *use_schema:bool=True*, *name:str|None=None*) → str

Prepare a quoted table and schema name.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)format_table_seq(*table*, *use_schema=True*)

Format table name and schema as a tuple.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)quote(*ident:str*, *force:Any=None*) → str

Conditionally quote an identifier.

The identifier is quoted if it is a reserved word, contains
quote-necessary characters, or is an instance of
[quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) which includes `quote` set to `True`.

Subclasses can override this to provide database-dependent
quoting behavior for identifier names.

  Parameters:

- **ident** – string identifier
- **force** –
  unused
  Deprecated since version 0.9: The [IdentifierPreparer.quote.force](#sqlalchemy.sql.compiler.IdentifierPreparer.quote.params.force)
  parameter is deprecated and will be removed in a future
  release.  This flag has no effect on the behavior of the
  [IdentifierPreparer.quote()](#sqlalchemy.sql.compiler.IdentifierPreparer.quote) method; please refer to
  [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).

      method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)quote_identifier(*value:str*) → str

Quote an identifier.

Subclasses should override this to provide database-dependent
quoting behavior.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)quote_schema(*schema:str*, *force:Any=None*) → str

Conditionally quote a schema name.

The name is quoted if it is a reserved word, contains quote-necessary
characters, or is an instance of [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name) which includes
`quote` set to `True`.

Subclasses can override this to provide database-dependent
quoting behavior for schema names.

  Parameters:

- **schema** – string schema name
- **force** –
  unused
  Deprecated since version 0.9: The [IdentifierPreparer.quote_schema.force](#sqlalchemy.sql.compiler.IdentifierPreparer.quote_schema.params.force)
  parameter is deprecated and will be removed in a future
  release.  This flag has no effect on the behavior of the
  [IdentifierPreparer.quote()](#sqlalchemy.sql.compiler.IdentifierPreparer.quote) method; please refer to
  [quoted_name](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.quoted_name).

      attribute [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)schema_for_object: _SchemaForObjectCallable = operator.attrgetter('schema')

Return the .schema attribute for an object.

For the default IdentifierPreparer, the schema for an object is always
the value of the “.schema” attribute.   if the preparer is replaced
with one that has a non-empty schema_translate_map, the value of the
“.schema” attribute is rendered a symbol that will be converted to a
real schema name from the mapping post-compile.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)unformat_identifiers(*identifiers:str*) → Sequence[str]

Unpack ‘schema.table.column’-like strings into components.

    method [sqlalchemy.sql.compiler.IdentifierPreparer.](#sqlalchemy.sql.compiler.IdentifierPreparer)validate_sql_phrase(*element*, *reg*)

keyword sequence filter.

a filter for elements that are intended to represent keyword sequences,
such as “INITIALLY”, “INITIALLY DEFERRED”, etc.   no special characters
should be present.

Added in version 1.3.

      class sqlalchemy.sql.compiler.SQLCompiler

*inherits from* [sqlalchemy.sql.compiler.Compiled](#sqlalchemy.engine.Compiled)

Default implementation of [Compiled](#sqlalchemy.engine.Compiled).

Compiles [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) objects into SQL strings.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newSQLCompilerobject. |
| ansi_bind_rules | SQL 92 doesn’t allow bind parameters to be used
in the columns clause of a SELECT, nor does it allow
ambiguous expressions like “? = ?”.  A compiler
subclass can set this flag to False if the target
driver/DB enforces this |
| bind_names | a dictionary of BindParameter instances to “compiled” names
that are actually present in the generated SQL |
| bindname_escape_characters | A mapping (e.g. dict or similar) containing a lookup of
characters keyed to replacement characters which will be applied to all
‘bind names’ used in SQL statements as a form of ‘escaping’; the given
characters are replaced entirely with the ‘replacement’ character when
rendered in the SQL statement, and a similar translation is performed
on the incoming names used in parameter dictionaries passed to methods
likeConnection.execute(). |
| binds | a dictionary of bind parameter keys to BindParameter instances. |
| bindtemplate | template to render bound parameters based on paramstyle. |
| compilation_bindtemplate | template used by compiler to render parameters before positional
paramstyle application |
| construct_expanded_state() | Return a newExpandedStatefor a given parameter set. |
| construct_params() | return a dictionary of bind parameter keys and values |
| default_from() | Called when a SELECT statement has no froms, and no FROM clause is
to be appended. |
| delete_extra_from_clause() | Provide a hook to override the generation of an
DELETE..FROM clause. |
| delete_limit_clause() | Provide a hook for MySQL to add LIMIT to the DELETE |
| effective_returning | The effective “returning” columns for INSERT, UPDATE or DELETE. |
| escaped_bind_names | Late escaping of bound parameter names that has to be converted
to the original name when looking in the parameter dictionary. |
| get_select_precolumns() | Called when building aSELECTstatement, position is just
before column list. |
| group_by_clause() | allow dialects to customize how GROUP BY is rendered. |
| has_out_parameters | if True, there are bindparam() objects that have the isoutparam
flag set. |
| implicit_returning | list of “implicit” returning columns for a toplevel INSERT or UPDATE
statement, used to receive newly generated values of columns. |
| insert_prefetch | list of columns for which default values should be evaluated before
an INSERT takes place |
| isupdate | class-level defaults which can be set at the instance
level to define if this Compiled instance represents
INSERT/UPDATE/DELETE |
| literal_execute_params | bindparameter objects that are rendered as literal values at statement
execution time. |
| order_by_clause() | allow dialects to customize how ORDER BY is rendered. |
| positiontup | for a compiled construct that uses a positional paramstyle, will be
a sequence of strings, indicating the names of bound parameters in order. |
| post_compile_params | bindparameter objects that are rendered as bound parameter placeholders
at statement execution time. |
| postfetch | list of columns that can be post-fetched after INSERT or UPDATE to
receive server-updated values |
| postfetch_lastrowid | if True, and this in insert, use cursor.lastrowid to populate
result.inserted_primary_key. |
| render_literal_value() | Render the value of a bind parameter as a quoted literal. |
| render_table_with_column_in_update_from | set to True classwide to indicate the SET clause
in a multi-table UPDATE statement should qualify
columns with the table name (i.e. MySQL only) |
| returning_precedes_values | set to True classwide to generate RETURNING
clauses before the VALUES or WHERE clause (i.e. MSSQL) |
| stack | major statements such as SELECT, INSERT, UPDATE, DELETE are
tracked in this stack using an entry format. |
| translate_select_structure | if notNone, should be a callable which accepts(select_stmt,**kw)and returns a select object.   this is used for structural changes
mostly to accommodate for LIMIT/OFFSET schemes |
| update_from_clause() | Provide a hook to override the generation of an
UPDATE..FROM clause. |
| update_limit_clause() | Provide a hook for MySQL to add LIMIT to the UPDATE |
| update_prefetch | list of columns for which onupdate default values should be evaluated
before an UPDATE takes place |
| update_tables_clause() | Provide a hook to override the initial table clause
in an UPDATE statement. |
| visit_override_binds() | SQL compile the nested element of an _OverrideBinds with
bindparams swapped out. |

   method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)__init__(*dialect:Dialect*, *statement:ClauseElement|None*, *cache_key:CacheKey|None=None*, *column_keys:Sequence[str]|None=None*, *for_executemany:bool=False*, *linting:Linting=Linting.NO_LINTING*, *_supporting_against:SQLCompiler|None=None*, ***kwargs:Any*)

Construct a new [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler) object.

  Parameters:

- **dialect** – [Dialect](#sqlalchemy.engine.Dialect) to be used
- **statement** – [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) to be compiled
- **column_keys** – a list of column names to be compiled into an
  INSERT or UPDATE statement.
- **for_executemany** – whether INSERT / UPDATE statements should
  expect that they are to be invoked in an “executemany” style,
  which may impact how the statement will be expected to return the
  values of defaults and autoincrement / sequences and similar.
  Depending on the backend and driver in use, support for retrieving
  these values may be disabled which means SQL expressions may
  be rendered inline, RETURNING may not be rendered, etc.
- **kwargs** – additional keyword arguments to be consumed by the
  superclass.

      attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)ansi_bind_rules: bool = False

SQL 92 doesn’t allow bind parameters to be used
in the columns clause of a SELECT, nor does it allow
ambiguous expressions like “? = ?”.  A compiler
subclass can set this flag to False if the target
driver/DB enforces this

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)bind_names: Dict[[BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)[Any], str]

a dictionary of BindParameter instances to “compiled” names
that are actually present in the generated SQL

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)bindname_escape_characters: ClassVar[Mapping[str, str]] = {' ': '_', '%': 'P', '(': 'A', ')': 'Z', '.': '_', ':': 'C', '[': '_', ']': '_'}

A mapping (e.g. dict or similar) containing a lookup of
characters keyed to replacement characters which will be applied to all
‘bind names’ used in SQL statements as a form of ‘escaping’; the given
characters are replaced entirely with the ‘replacement’ character when
rendered in the SQL statement, and a similar translation is performed
on the incoming names used in parameter dictionaries passed to methods
like [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute).

This allows bound parameter names used in [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) and
other constructs to have any arbitrary characters present without any
concern for characters that aren’t allowed at all on the target database.

Third party dialects can establish their own dictionary here to replace the
default mapping, which will ensure that the particular characters in the
mapping will never appear in a bound parameter name.

The dictionary is evaluated at **class creation time**, so cannot be
modified at runtime; it must be present on the class when the class
is first declared.

Note that for dialects that have additional bound parameter rules such
as additional restrictions on leading characters, the
`SQLCompiler.bindparam_string()` method may need to be augmented.
See the cx_Oracle compiler for an example of this.

Added in version 2.0.0rc1.

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)binds: Dict[str, [BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)[Any]]

a dictionary of bind parameter keys to BindParameter instances.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)bindtemplate: str

template to render bound parameters based on paramstyle.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)compilation_bindtemplate: str

template used by compiler to render parameters before positional
paramstyle application

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)construct_expanded_state(*params:_CoreSingleExecuteParams|None=None*, *escape_names:bool=True*) → [ExpandedState](#sqlalchemy.sql.compiler.ExpandedState)

Return a new [ExpandedState](#sqlalchemy.sql.compiler.ExpandedState) for a given parameter set.

For queries that use “expanding” or other late-rendered parameters,
this method will provide for both the finalized SQL string as well
as the parameters that would be used for a particular parameter set.

Added in version 2.0.0rc1.

     method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)construct_params(*params:_CoreSingleExecuteParams|None=None*, *extracted_parameters:Sequence[BindParameter[Any]]|None=None*, *escape_names:bool=True*, *_group_number:int|None=None*, *_check:bool=True*, *_no_postcompile:bool=False*) → _MutableCoreSingleExecuteParams

return a dictionary of bind parameter keys and values

    property current_executable

Return the current ‘executable’ that is being compiled.

This is currently the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select), [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert),
[Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update), [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete),
[CompoundSelect](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.CompoundSelect) object that is being compiled.
Specifically it’s assigned to the `self.stack` list of elements.

When a statement like the above is being compiled, it normally
is also assigned to the `.statement` attribute of the
`Compiler` object.   However, all SQL constructs are
ultimately nestable, and this attribute should never be consulted
by a `visit_` method, as it is not guaranteed to be assigned
nor guaranteed to correspond to the current statement being compiled.

Added in version 1.3.21: For compatibility with previous versions, use the following
recipe:

```
statement = getattr(self, "current_executable", False)
if statement is False:
    statement = self.stack[-1]["selectable"]
```

For versions 1.4 and above, ensure only .current_executable
is used; the format of “self.stack” may change.

     method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)default_from() → str

Called when a SELECT statement has no froms, and no FROM clause is
to be appended.

Gives Oracle Database a chance to tack on a `FROM DUAL` to the string
output.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)delete_extra_from_clause(*delete_stmt*, *from_table*, *extra_froms*, *from_hints*, ***kw*)

Provide a hook to override the generation of an
DELETE..FROM clause.

This can be used to implement DELETE..USING for example.

MySQL and MSSQL override this.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)delete_limit_clause(*delete_stmt*)

Provide a hook for MySQL to add LIMIT to the DELETE

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)effective_returning

The effective “returning” columns for INSERT, UPDATE or DELETE.

This is either the so-called “implicit returning” columns which are
calculated by the compiler on the fly, or those present based on what’s
present in `self.statement._returning` (expanded into individual
columns using the `._all_selected_columns` attribute) i.e. those set
explicitly using the [UpdateBase.returning()](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.UpdateBase.returning) method.

Added in version 2.0.

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)escaped_bind_names: util.immutabledict[str, str] = {}

Late escaping of bound parameter names that has to be converted
to the original name when looking in the parameter dictionary.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)get_select_precolumns(*select:Select[Any]*, ***kw:Any*) → str

Called when building a `SELECT` statement, position is just
before column list.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)group_by_clause(*select*, ***kw*)

allow dialects to customize how GROUP BY is rendered.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)has_out_parameters = False

if True, there are bindparam() objects that have the isoutparam
flag set.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)implicit_returning: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[ColumnElement](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)[Any]] | None = None

list of “implicit” returning columns for a toplevel INSERT or UPDATE
statement, used to receive newly generated values of columns.

Added in version 2.0: `implicit_returning` replaces the previous
`returning` collection, which was not a generalized RETURNING
collection and instead was in fact specific to the “implicit returning”
feature.

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)insert_prefetch: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] = ()

list of columns for which default values should be evaluated before
an INSERT takes place

    property insert_single_values_expr: str | None

When an INSERT is compiled with a single set of parameters inside
a VALUES expression, the string is assigned here, where it can be
used for insert batching schemes to rewrite the VALUES expression.

Added in version 1.3.8.

Changed in version 2.0: This collection is no longer used by
SQLAlchemy’s built-in dialects, in favor of the currently
internal `_insertmanyvalues` collection that is used only by
[SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler).

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)isupdate: bool = False

class-level defaults which can be set at the instance
level to define if this Compiled instance represents
INSERT/UPDATE/DELETE

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)literal_execute_params: FrozenSet[[BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)[Any]] = frozenset({})

bindparameter objects that are rendered as literal values at statement
execution time.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)order_by_clause(*select*, ***kw*)

allow dialects to customize how ORDER BY is rendered.

    property params

Return the bind param dictionary embedded into this
compiled object, for those values that are present.

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string) - includes a usage example for
debugging use cases.

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)positiontup: List[str] | None = None

for a compiled construct that uses a positional paramstyle, will be
a sequence of strings, indicating the names of bound parameters in order.

This is used in order to render bound parameters in their correct order,
and is combined with the `Compiled.params` dictionary to
render parameters.

This sequence always contains the unescaped name of the parameters.

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string) - includes a usage example for
debugging use cases.

     attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)post_compile_params: FrozenSet[[BindParameter](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.BindParameter)[Any]] = frozenset({})

bindparameter objects that are rendered as bound parameter placeholders
at statement execution time.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)postfetch: List[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] | None

list of columns that can be post-fetched after INSERT or UPDATE to
receive server-updated values

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)postfetch_lastrowid = False

if True, and this in insert, use cursor.lastrowid to populate
result.inserted_primary_key.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)render_literal_value(*value:Any*, *type_:TypeEngine*) → str

Render the value of a bind parameter as a quoted literal.

This is used for statement sections that do not accept bind parameters
on the target driver/database.

This should be implemented by subclasses using the quoting services
of the DBAPI.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)render_table_with_column_in_update_from: bool = False

set to True classwide to indicate the SET clause
in a multi-table UPDATE statement should qualify
columns with the table name (i.e. MySQL only)

    property returning

backwards compatibility; returns the
effective_returning collection.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)returning_precedes_values: bool = False

set to True classwide to generate RETURNING
clauses before the VALUES or WHERE clause (i.e. MSSQL)

    property sql_compiler: Self

Return a Compiled that is capable of processing SQL expressions.

If this compiler is one, it would likely just return ‘self’.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)stack: List[_CompilerStackEntry]

major statements such as SELECT, INSERT, UPDATE, DELETE are
tracked in this stack using an entry format.

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)translate_select_structure: Any = None

if not `None`, should be a callable which accepts `(select_stmt,
**kw)` and returns a select object.   this is used for structural changes
mostly to accommodate for LIMIT/OFFSET schemes

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)update_from_clause(*update_stmt*, *from_table*, *extra_froms*, *from_hints*, ***kw*)

Provide a hook to override the generation of an
UPDATE..FROM clause.

MySQL and MSSQL override this.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)update_limit_clause(*update_stmt*)

Provide a hook for MySQL to add LIMIT to the UPDATE

    attribute [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)update_prefetch: [Sequence](https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.Sequence)[[Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)[Any]] = ()

list of columns for which onupdate default values should be evaluated
before an UPDATE takes place

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)update_tables_clause(*update_stmt*, *from_table*, *extra_froms*, ***kw*)

Provide a hook to override the initial table clause
in an UPDATE statement.

MySQL overrides this.

    method [sqlalchemy.sql.compiler.SQLCompiler.](#sqlalchemy.sql.compiler.SQLCompiler)visit_override_binds(*override_binds*, ***kw*)

SQL compile the nested element of an _OverrideBinds with
bindparams swapped out.

The _OverrideBinds is not normally expected to be compiled; it
is meant to be used when an already cached statement is to be used,
the compilation was already performed, and only the bound params should
be swapped in at execution time.

However, there are test cases that exericise this object, and
additionally the ORM subquery loader is known to feed in expressions
which include this construct into new queries (discovered in #11173),
so it has to do the right thing at compile time as well.

     class sqlalchemy.sql.compiler.StrSQLCompiler

*inherits from* [sqlalchemy.sql.compiler.SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler)

A [SQLCompiler](#sqlalchemy.sql.compiler.SQLCompiler) subclass which allows a small selection
of non-standard SQL features to render into a string value.

The [StrSQLCompiler](#sqlalchemy.sql.compiler.StrSQLCompiler) is invoked whenever a Core expression
element is directly stringified without calling upon the
[ClauseElement.compile()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compile) method.
It can render a limited set
of non-standard SQL constructs to assist in basic stringification,
however for more substantial custom or dialect-specific SQL constructs,
it will be necessary to make use of
[ClauseElement.compile()](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement.compile)
directly.

See also

[How do I render SQL expressions as strings, possibly with bound parameters inlined?](https://docs.sqlalchemy.org/en/20/faq/sqlexpressions.html#faq-sql-expression-string)

| Member Name | Description |
| --- | --- |
| delete_extra_from_clause() | Provide a hook to override the generation of an
DELETE..FROM clause. |
| update_from_clause() | Provide a hook to override the generation of an
UPDATE..FROM clause. |

   method [sqlalchemy.sql.compiler.StrSQLCompiler.](#sqlalchemy.sql.compiler.StrSQLCompiler)delete_extra_from_clause(*delete_stmt*, *from_table*, *extra_froms*, *from_hints*, ***kw*)

Provide a hook to override the generation of an
DELETE..FROM clause.

This can be used to implement DELETE..USING for example.

MySQL and MSSQL override this.

    method [sqlalchemy.sql.compiler.StrSQLCompiler.](#sqlalchemy.sql.compiler.StrSQLCompiler)update_from_clause(*update_stmt*, *from_table*, *extra_froms*, *from_hints*, ***kw*)

Provide a hook to override the generation of an
UPDATE..FROM clause.

MySQL and MSSQL override this.

     class sqlalchemy.engine.AdaptedConnection

Interface of an adapted connection object to support the DBAPI protocol.

Used by asyncio dialects to provide a sync-style pep-249 facade on top
of the asyncio connection/cursor API provided by the driver.

Added in version 1.4.24.

| Member Name | Description |
| --- | --- |
| run_async() | Run the awaitable returned by the given function, which is passed
the raw asyncio driver connection. |

   property driver_connection: Any

The connection object as returned by the driver after a connect.

    method [sqlalchemy.engine.AdaptedConnection.](#sqlalchemy.engine.AdaptedConnection)run_async(*fn:Callable[[Any],Awaitable[_T]]*) → _T

Run the awaitable returned by the given function, which is passed
the raw asyncio driver connection.

This is used to invoke awaitable-only methods on the driver connection
within the context of a “synchronous” method, like a connection
pool event handler.

E.g.:

```
engine = create_async_engine(...)

@event.listens_for(engine.sync_engine, "connect")
def register_custom_types(
    dbapi_connection,  # ...
):
    dbapi_connection.run_async(
        lambda connection: connection.set_type_codec(
            "MyCustomType", encoder, decoder, ...
        )
    )
```

Added in version 1.4.30.

See also

[Using awaitable-only driver methods in connection pool and other events](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-events-run-async)
