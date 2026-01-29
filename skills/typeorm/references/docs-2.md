# DataSource and more

# DataSource

> What is a DataSource?

## What is a DataSource?​

Your interaction with the database is only possible once you setup a `DataSource`.
TypeORM's `DataSource` holds your database connection settings and
establishes the initial database connection or connection pool depending on the RDBMS you use.

To establish the initial connection/connection pool, you must call the `initialize` method of your `DataSource` instance.

Disconnection (closing all connections in the pool) occurs when the `destroy` method is called.

Generally, you call the `initialize` method of the `DataSource` instance on the application bootstrap,
and `destroy` it after you finished working with the database.
In practice, if you are building a backend for your site and your backend server always stays running -
you never `destroy` a DataSource.

## Creating a new DataSource​

To create a new `DataSource` instance you must initialize its constructor by calling `new DataSource`
and assigning to a global variable that you'll use across your application:

```
import { DataSource } from "typeorm"const AppDataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",})try {    await AppDataSource.initialize()    console.log("Data Source has been initialized!")} catch (error) {    console.error("Error during Data Source initialization", error)}
```

It's a good idea to make `AppDataSource` globally available by `export`-ing it since you'll use this instance across your application.

`DataSource` accepts `DataSourceOptions` and those options vary depending on the database `type` you use.
For different database types, there are different options you can specify.

You can define as many data sources as you need in your application, for example:

```
import { DataSource } from "typeorm"const MysqlDataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    entities: [        // ....    ],})const PostgresDataSource = new DataSource({    type: "postgres",    host: "localhost",    port: 5432,    username: "test",    password: "test",    database: "test",    entities: [        // ....    ],})
```

## How to use DataSource?​

Once you set your `DataSource`, you can use it anywhere in your app, for example:

```
import { AppDataSource } from "./app-data-source"import { User } from "../entity/User"export class UserController {    @Get("/users")    getAll() {        return AppDataSource.manager.find(User)    }}
```

Using the `DataSource` instance you can execute database operations with your entities,
particularly using `.manager` and `.getRepository()` properties.
For more information about them see [Entity Manager](https://typeorm.io/docs/working-with-entity-manager/working-with-entity-manager) and [Repository](https://typeorm.io/docs/working-with-entity-manager/working-with-repository) documentation.

---

# Multiple data sources, databases, schemas and replication setup

> Using multiple data sources

## Using multiple data sources​

To use multiple data sources connected to different databases, simply create multiple DataSource instances:

```
import { DataSource } from "typeorm"const db1DataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "root",    password: "admin",    database: "db1",    entities: [__dirname + "/entity/*{.js,.ts}"],    synchronize: true,})const db2DataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "root",    password: "admin",    database: "db2",    entities: [__dirname + "/entity/*{.js,.ts}"],    synchronize: true,})
```

## Using multiple databases within a single data source​

To use multiple databases in a single data source,
you can specify database name per-entity:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity({ database: "secondDB" })export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity({ database: "thirdDB" })export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    url: string}
```

`User` entity will be created inside `secondDB` database and `Photo` entity inside `thirdDB` database.
All other entities will be created in a default database defined in the data source options.

If you want to select data from a different database you only need to provide an entity:

```
const users = await dataSource    .createQueryBuilder()    .select()    .from(User, "user")    .addFrom(Photo, "photo")    .andWhere("photo.userId = user.id")    .getMany() // userId is not a foreign key since its cross-database request
```

This code will produce following SQL query (depend on database type):

```
SELECT * FROM "secondDB"."user" "user", "thirdDB"."photo" "photo"    WHERE "photo"."userId" = "user"."id"
```

You can also specify a table path instead of the entity:

```
const users = await dataSource    .createQueryBuilder()    .select()    .from("secondDB.user", "user")    .addFrom("thirdDB.photo", "photo")    .andWhere("photo.userId = user.id")    .getMany() // userId is not a foreign key since its cross-database request
```

This feature is supported only in mysql and mssql databases.

## Using multiple schemas within a single data source​

To use multiple schemas in your applications, just set `schema` on each entity:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity({ schema: "secondSchema" })export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity({ schema: "thirdSchema" })export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    url: string}
```

`User` entity will be created inside `secondSchema` schema and `Photo` entity inside `thirdSchema` schema.
All other entities will be created in a default database defined in the data source options.

If you want to select data from a different schema you only need to provide an entity:

```
const users = await dataSource    .createQueryBuilder()    .select()    .from(User, "user")    .addFrom(Photo, "photo")    .andWhere("photo.userId = user.id")    .getMany() // userId is not a foreign key since its cross-database request
```

This code will produce following SQL query (depend on database type):

```
SELECT * FROM "secondSchema"."question" "question", "thirdSchema"."photo" "photo"    WHERE "photo"."userId" = "user"."id"
```

You can also specify a table path instead of entity:

```
const users = await dataSource    .createQueryBuilder()    .select()    .from("secondSchema.user", "user") // in mssql you can even specify a database: secondDB.secondSchema.user    .addFrom("thirdSchema.photo", "photo") // in mssql you can even specify a database: thirdDB.thirdSchema.photo    .andWhere("photo.userId = user.id")    .getMany()
```

This feature is supported only in postgres and mssql databases.
In mssql you can also combine schemas and databases, for example:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity({ database: "secondDB", schema: "public" })export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string}
```

## Replication​

You can set up read/write replication using TypeORM.
Example of replication options:

```
const datasource = new DataSource({    type: "mysql",    logging: true,    replication: {        master: {            host: "server1",            port: 3306,            username: "test",            password: "test",            database: "test",        },        slaves: [            {                host: "server2",                port: 3306,                username: "test",                password: "test",                database: "test",            },            {                host: "server3",                port: 3306,                username: "test",                password: "test",                database: "test",            },        ],    },})
```

With replication slaves defined, TypeORM will start sending all possible queries to slaves by default.

- all queries performed by the `find` methods or `SelectQueryBuilder` will use a random `slave` instance
- all write queries performed by `update`, `create`, `InsertQueryBuilder`, `UpdateQueryBuilder`, etc will use the `master` instance
- all raw queries performed by calling `.query()` will use the `master` instance
- all schema update operations are performed using the `master` instance

### Explicitly selecting query destinations​

By default, TypeORM will send all read queries to a random read slave, and all writes to the master. This means when you first add the `replication` settings to your configuration, any existing read query runners that don't explicitly specify a replication mode will start going to a slave. This is good for scalability, but if some of those queries *must* return up to date data, then you need to explicitly pass a replication mode when you create a query runner.

If you want to explicitly use the `master` for read queries, pass an explicit `ReplicationMode` when creating your `QueryRunner`;

```
const masterQueryRunner = dataSource.createQueryRunner("master")try {    const postsFromMaster = await dataSource        .createQueryBuilder(Post, "post", masterQueryRunner) // you can either pass QueryRunner as an optional argument with query builder        .setQueryRunner(masterQueryRunner) // or use setQueryRunner which sets or overrides query builder's QueryRunner        .getMany()} finally {    await masterQueryRunner.release()}
```

If you want to use a slave in raw queries, pass `slave` as the replication mode when creating a query runner:

```
const slaveQueryRunner = dataSource.createQueryRunner("slave")try {    const userFromSlave = await slaveQueryRunner.query(        "SELECT * FROM users WHERE id = $1",        [userId],        slaveQueryRunner,    )} finally {    return slaveQueryRunner.release()}
```

**Note**: Manually created `QueryRunner` instances must be explicitly released on their own. If you don't release your query runners, they will keep a connection checked out of the pool, and prevent other queries from using it.

### Adjusting the default destination for reads​

If you don't want all reads to go to a `slave` instance by default, you can change the default read query destination by passing `defaultMode: "master"` in your replication options:

```
const datasource = new DataSource({    type: "mysql",    logging: true,    replication: {        // set the default destination for read queries as the master instance        defaultMode: "master",        master: {            host: "server1",            port: 3306,            username: "test",            password: "test",            database: "test",        },        slaves: [            {                host: "server2",                port: 3306,                username: "test",                password: "test",                database: "test",            },        ],    },})
```

With this mode, no queries will go to the read slaves by default, and you'll have to opt-in to sending queries to read slaves with explicit `.createQueryRunner("slave")` calls.

If you're adding replication options to an existing app for the first time, this is a good option for ensuring no behavior changes right away, and instead you can slowly adopt read replicas on a query runner by query runner basis.

### Supported drivers​

Replication is supported by the MySQL, PostgreSQL, SQL Server, Cockroach, Oracle, and Spanner connection drivers.

MySQL replication supports extra configuration options:

```
{  replication: {    master: {      host: "server1",      port: 3306,      username: "test",      password: "test",      database: "test"    },    slaves: [{      host: "server2",      port: 3306,      username: "test",      password: "test",      database: "test"    }, {      host: "server3",      port: 3306,      username: "test",      password: "test",      database: "test"    }],    /**    * If true, PoolCluster will attempt to reconnect when connection fails. (Default: true)    */    canRetry: true,    /**     * If connection fails, node's errorCount increases.     * When errorCount is greater than removeNodeErrorCount, remove a node in the PoolCluster. (Default: 5)     */    removeNodeErrorCount: 5,    /**     * If connection fails, specifies the number of milliseconds before another connection attempt will be made.     * If set to 0, then node will be removed instead and never re-used. (Default: 0)     */     restoreNodeTimeout: 0,    /**     * Determines how slaves are selected:     * RR: Select one alternately (Round-Robin).     * RANDOM: Select the node by random function.     * ORDER: Select the first node available unconditionally.     */    selector: "RR"  }}
```

---

# Handling null and undefined values in where conditions

> In 'WHERE' conditions the values null and undefined are not strictly valid values in TypeORM.

In 'WHERE' conditions the values `null` and `undefined` are not strictly valid values in TypeORM.

Passing a known `null` value is disallowed by TypeScript (when you've enabled `strictNullChecks` in tsconfig.json) at compile time. But the default behavior is for `null` values encountered at runtime to be ignored. Similarly, `undefined` values are allowed by TypeScript and ignored at runtime.

The acceptance of `null` and `undefined` values can sometimes cause unexpected results and requires caution. This is especially a concern when values are passed from user input without adequate validation.

For example, calling `Repository.findOneBy({ id: undefined })` returns the first row from the table, and `Repository.findBy({ userId: null })` is unfiltered and returns all rows.

The way in which `null` and `undefined` values are handled can be customised through the `invalidWhereValuesBehavior` configuration option in your data source options. This applies to all operations that support 'WHERE' conditions, including find operations, query builders, and repository methods.

 note

The current behavior will be changing in future versions of TypeORM,
we recommend setting both `null` and `undefined` behaviors to throw to prepare for these changes

## Default Behavior​

By default, TypeORM skips both `null` and `undefined` values in where conditions. This means that if you include a property with a `null` or `undefined` value in your where clause, it will be ignored:

```
// Both queries will return all posts, ignoring the text propertyconst posts1 = await repository.find({    where: {        text: null,    },})const posts2 = await repository.find({    where: {        text: undefined,    },})
```

The correct way to match null values in where conditions is to use the `IsNull` operator (for details see [Find Options](https://typeorm.io/docs/working-with-entity-manager/find-options)):

```
const posts = await repository.find({    where: {        text: IsNull(),    },})
```

## Configuration​

You can customize how null and undefined values are handled using the `invalidWhereValuesBehavior` option in your connection configuration:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        null: "ignore" | "sql-null" | "throw",        undefined: "ignore" | "throw",    },})
```

### Null Behavior Options​

The `null` behavior can be set to one of three values:

#### 'ignore'(default)​

JavaScript `null` values in where conditions are ignored and the property is skipped:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        null: "ignore",    },})// This will return all posts, ignoring the text propertyconst posts = await repository.find({    where: {        text: null,    },})
```

#### 'sql-null'​

JavaScript `null` values are transformed into SQL `NULL` conditions:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        null: "sql-null",    },})// This will only return posts where the text column is NULL in the databaseconst posts = await repository.find({    where: {        text: null,    },})
```

#### 'throw'​

JavaScript `null` values cause a TypeORMError to be thrown:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        null: "throw",    },})// This will throw an errorconst posts = await repository.find({    where: {        text: null,    },})// Error: Null value encountered in property 'text' of a where condition.// To match with SQL NULL, the IsNull() operator must be used.// Set 'invalidWhereValuesBehavior.null' to 'ignore' or 'sql-null' in connection options to skip or handle null values.
```

### Undefined Behavior Options​

The `undefined` behavior can be set to one of two values:

#### 'ignore'(default)​

JavaScript `undefined` values in where conditions are ignored and the property is skipped:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        undefined: "ignore",    },})// This will return all posts, ignoring the text propertyconst posts = await repository.find({    where: {        text: undefined,    },})
```

#### 'throw'​

JavaScript `undefined` values cause a TypeORMError to be thrown:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        undefined: "throw",    },})// This will throw an errorconst posts = await repository.find({    where: {        text: undefined,    },})// Error: Undefined value encountered in property 'text' of a where condition.// Set 'invalidWhereValuesBehavior.undefined' to 'ignore' in connection options to skip properties with undefined values.
```

Note that this only applies to explicitly set `undefined` values, not omitted properties.

## Using Both Options Together​

You can configure both behaviors independently for comprehensive control:

```
const dataSource = new DataSource({    // ... other options    invalidWhereValuesBehavior: {        null: "sql-null",        undefined: "throw",    },})
```

This configuration will:

1. Transform JavaScript `null` values to SQL `NULL` in where conditions
2. Throw an error if any `undefined` values are encountered
3. Still ignore properties that are not provided in the where clause

This combination is useful when you want to:

- Be explicit about searching for NULL values in the database
- Catch potential programming errors where undefined values might slip into your queries

## Works with all where operations​

The `invalidWhereValuesBehavior` configuration applies to **all TypeORM operations** that support where conditions, not just repository find methods:

### Query Builders​

```
// UpdateQueryBuilderawait dataSource    .createQueryBuilder()    .update(Post)    .set({ title: "Updated" })    .where({ text: null }) // Respects invalidWhereValuesBehavior    .execute()// DeleteQueryBuilder  await dataSource    .createQueryBuilder()    .delete()    .from(Post)    .where({ text: null }) // Respects invalidWhereValuesBehavior    .execute()// SoftDeleteQueryBuilderawait dataSource    .createQueryBuilder()    .softDelete()    .from(Post)    .where({ text: null }) // Respects invalidWhereValuesBehavior    .execute()
```

### Repository Methods​

```
// Repository.update()await repository.update({ text: null }, { title: "Updated" }) // Respects invalidWhereValuesBehavior// Repository.delete()await repository.delete({ text: null }) // Respects invalidWhereValuesBehavior// EntityManager.update()await manager.update(Post, { text: null }, { title: "Updated" }) // Respects invalidWhereValuesBehavior// EntityManager.delete()await manager.delete(Post, { text: null }) // Respects invalidWhereValuesBehavior// EntityManager.softDelete()await manager.softDelete(Post, { text: null }) // Respects invalidWhereValuesBehavior
```

All these operations will consistently apply your configured `invalidWhereValuesBehavior` settings.

---

# Google Spanner

> Installation

## Installation​

```
npm install @google-cloud/spanner
```

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options.

Provide authentication credentials to your application code
by setting the environment variable `GOOGLE_APPLICATION_CREDENTIALS`:

```
# Linux/macOSexport GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"# Windowsset GOOGLE_APPLICATION_CREDENTIALS=KEY_PATH# Replace KEY_PATH with the path of the JSON file that contains your service account key.
```

To use Spanner with the emulator you should set `SPANNER_EMULATOR_HOST` environment variable:

```
# Linux/macOSexport SPANNER_EMULATOR_HOST=localhost:9010# Windowsset SPANNER_EMULATOR_HOST=localhost:9010
```

## Column Types​

`bool`, `int64`, `float64`, `numeric`, `string`, `json`, `bytes`, `date`, `timestamp`, `array`

---

# Microsoft SQLServer

> Installation

## Installation​

```
npm install mssql
```

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options.

Based on [tedious](https://tediousjs.github.io/node-mssql/) MSSQL implementation. See [SqlServerConnectionOptions.ts](https://github.com/typeorm/typeorm/tree/master/src/driver/sqlserver/SqlServerConnectionOptions.ts) for details on exposed attributes.

- `url` - Connection url where the connection is performed. Please note that other data source options will override parameters set from url.
- `host` - Database host.
- `port` - Database host port. Default mssql port is `1433`.
- `username` - Database username.
- `password` - Database password.
- `database` - Database name.
- `schema` - Schema name. Default is "dbo".
- `domain` - Once you set domain, the driver will connect to SQL Server using domain login.
- `connectionTimeout` - Connection timeout in ms (default: `15000`).
- `requestTimeout` - Request timeout in ms (default: `15000`). NOTE: msnodesqlv8 driver doesn't support
  timeouts < 1 second.
- `stream` - Stream record sets/rows instead of returning them all at once as an argument of callback (default: `false`).
  You can also enable streaming for each request independently (`request.stream = true`). Always set to `true` if you plan to
  work with a large number of rows.
- `pool.max` - The maximum number of connections there can be in the pool (default: `10`).
- `pool.min` - The minimum of connections there can be in the pool (default: `0`).
- `pool.maxWaitingClients` - maximum number of queued requests allowed, additional acquire calls will be called back with
  an error in a future cycle of the event loop.
- `pool.acquireTimeoutMillis` - max milliseconds an `acquire` call will wait for a resource before timing out.
  (default no limit), if supplied should non-zero positive integer.
- `pool.fifo` - if true the oldest resources will be first to be allocated. If false, the most recently released resources
  will be the first to be allocated. This, in effect, turns the pool's behaviour from a queue into a stack. boolean,
  (default `true`).
- `pool.priorityRange` - int between 1 and x - if set, borrowers can specify their relative priority in the queue if no
  resources are available. see example. (default `1`).
- `pool.evictionRunIntervalMillis` - How often to run eviction checks. Default: `0` (does not run).
- `pool.numTestsPerRun` - Number of resources to check each eviction run. Default: `3`.
- `pool.softIdleTimeoutMillis` - amount of time an object may sit idle in the pool before it is eligible for eviction by
  the idle object evictor (if any), with the extra condition that at least "min idle" object instances remain in the pool.
  Default `-1` (nothing can get evicted).
- `pool.idleTimeoutMillis` - the minimum amount of time that an object may sit idle in the pool before it is eligible for
  eviction due to idle time. Supersedes `softIdleTimeoutMillis`. Default: `30000`.
- `pool.errorHandler` - A function that gets called when the underlying pool emits `'error'` event. Takes a single parameter (error instance) and defaults to logging with `warn` level.
- `options.fallbackToDefaultDb` - By default, if the database requested by `options.database` cannot be accessed, the connection will fail with an error. However, if `options.fallbackToDefaultDb` is set to `true`, then the user's default database will be used instead (Default: `false`).
- `options.instanceName` - The instance name to connect to. The SQL Server Browser service must be running on the database server, and UDP port 1434 on the database server must be reachable. Mutually exclusive with `port`. (no default).
- `options.enableAnsiNullDefault` - If true, `SET ANSI_NULL_DFLT_ON ON` will be set in the initial SQL. This means new
  columns will be nullable by default. See the [T-SQL documentation](https://msdn.microsoft.com/en-us/library/ms187375.aspx)
  for more details. (Default: `true`).
- `options.cancelTimeout` - The number of milliseconds before the cancel (abort) of a request is considered failed (default: `5000`).
- `options.packetSize` - The size of TDS packets (subject to negotiation with the server). Should be a power of 2. (default: `4096`).
- `options.useUTC` - A boolean determining whether to pass time values in UTC or local time. (default: `false`).
- `options.abortTransactionOnError` - A boolean determining whether to roll back a transaction automatically if any
  error is encountered during the given transaction's execution. This sets the value for `SET XACT_ABORT` during the
  initial SQL phase of a connection ([documentation](http://msdn.microsoft.com/en-us/library/ms188792.aspx)).
- `options.localAddress` - A string indicating which network interface (ip address) to use when connecting to SQL Server.
- `options.useColumnNames` - A boolean determining whether to return rows as arrays or key-value collections. (default: `false`).
- `options.camelCaseColumns` - A boolean, controlling whether the column names returned will have the first letter
  converted to lower case (`true`) or not. This value is ignored if you provide a `columnNameReplacer`. (default: `false`).
- `options.isolationLevel` - The default isolation level that transactions will be run with. The isolation levels are
  available from `require('tedious').ISOLATION_LEVEL`.
  - `READ_UNCOMMITTED`
  - `READ_COMMITTED`
  - `REPEATABLE_READ`
  - `SERIALIZABLE`
  - `SNAPSHOT`
  (default: `READ_COMMITTED`)
- `options.connectionIsolationLevel` - The default isolation level for new connections. All out-of-transaction queries
  are executed with this setting. The isolation levels are available from `require('tedious').ISOLATION_LEVEL`.
  - `READ_UNCOMMITTED`
  - `READ_COMMITTED`
  - `REPEATABLE_READ`
  - `SERIALIZABLE`
  - `SNAPSHOT`
  (default: `READ_COMMITTED`)
- `options.readOnlyIntent` - A boolean, determining whether the connection will request read-only access from a
  SQL Server Availability Group. For more information, see here. (default: `false`).
- `options.encrypt` - A boolean determining whether the connection will be encrypted. Set to true if you're on Windows Azure. (default: `true`).
- `options.cryptoCredentialsDetails` - When encryption is used, an object may be supplied that will be used for the
  first argument when calling [tls.createSecurePair](http://nodejs.org/docs/latest/api/tls.html#tls_tls_createsecurepair_credentials_isserver_requestcert_rejectunauthorized)
  (default: `{}`).
- `options.rowCollectionOnDone` - A boolean, that when true will expose received rows in Requests' `done*` events.
  See done, [doneInProc](http://tediousjs.github.io/tedious/api-request.html#event_doneInProc)
  and [doneProc](http://tediousjs.github.io/tedious/api-request.html#event_doneProc). (default: `false`)
  Caution: If many rows are received, enabling this option could result in excessive memory usage.
- `options.rowCollectionOnRequestCompletion` - A boolean, that when true will expose received rows
  in Requests' completion callback. See [new Request](http://tediousjs.github.io/tedious/api-request.html#function_newRequest). (default: `false`)
  Caution: If many rows are received, enabling this option could result in excessive memory usage.
- `options.tdsVersion` - The version of TDS to use. If the server doesn't support the specified version, a negotiated version
  is used instead. The versions are available from `require('tedious').TDS_VERSION`.
  - `7_1`
  - `7_2`
  - `7_3_A`
  - `7_3_B`
  - `7_4`
  (default: `7_4`)
- `options.appName` - Application name used for identifying a specific application in profiling, logging or tracing tools of SQL Server. (default: `node-mssql`)
- `options.trustServerCertificate` - A boolean, controlling whether encryption occurs if there is no verifiable server certificate. (default: `false`)
- `options.multiSubnetFailover` - A boolean, controlling whether the driver should connect to all IPs returned from DNS in parallel. (default: `false`)
- `options.debug.packet` - A boolean, controlling whether `debug` events will be emitted with text describing packet
  details (default: `false`).
- `options.debug.data` - A boolean, controlling whether `debug` events will be emitted with text describing packet data
  details (default: `false`).
- `options.debug.payload` - A boolean, controlling whether `debug` events will be emitted with text describing packet
  payload details (default: `false`).
- `options.debug.token` - A boolean, controlling whether `debug` events will be emitted with text describing token stream
  tokens (default: `false`).

## Column Types​

`int`, `bigint`, `bit`, `decimal`, `money`, `numeric`, `smallint`, `smallmoney`, `tinyint`, `float`, `real`, `date`, `datetime2`, `datetime`, `datetimeoffset`, `smalldatetime`, `time`, `char`, `varchar`, `text`, `nchar`, `nvarchar`, `ntext`, `binary`, `image`, `varbinary`, `hierarchyid`, `sql_variant`, `timestamp`, `uniqueidentifier`, `xml`, `geometry`, `geography`, `rowversion`, `vector`

### Vector Type (vector)​

The `vector` data type is available in SQL Server for storing high-dimensional vectors, commonly used for:

- Semantic search with embeddings
- Recommendation systems
- Similarity matching
- Machine learning applications

NOTE: general `halfvec` type support is unavailable because this feature is still in preview. See the Microsoft docs: [Vector data type](https://learn.microsoft.com/en-us/sql/t-sql/data-types/vector-data-type).

#### Usage​

```
@Entity()export class DocumentChunk {    @PrimaryGeneratedColumn()    id: number    @Column("varchar")    content: string    // Vector column with 1998 dimensions    @Column("vector", { length: 1998 })    embedding: number[]}
```

#### Vector Similarity Search​

SQL Server provides the `VECTOR_DISTANCE` function for calculating distances between vectors:

```
const queryEmbedding = [    /* your query vector */]const results = await dataSource.query(    `    DECLARE @question AS VECTOR (1998) = @0;    SELECT TOP (10) dc.*,           VECTOR_DISTANCE('cosine', @question, embedding) AS distance    FROM document_chunk dc    ORDER BY VECTOR_DISTANCE('cosine', @question, embedding)`,    [JSON.stringify(queryEmbedding)],)
```

**Distance Metrics:**

- `'cosine'` - Cosine distance (most common for semantic search)
- `'euclidean'` - Euclidean (L2) distance
- `'dot'` - Negative dot product

**Requirements:**

- SQL Server version with vector support enabled
- Vector dimensions must be specified using the `length` option

---

# MongoDB

> MongoDB support

## MongoDB support​

TypeORM has basic MongoDB support.
Most of TypeORM functionality is RDBMS-specific,
this page contains all MongoDB-specific functionality documentation.

## Installation​

```
npm install mongodb
```

## Data Source Options​

- `url` - Connection url where the connection is performed. Please note that other data source options will override parameters set from url.
- `host` - Database host.
- `port` - Database host port. Default mongodb port is `27017`.
- `username` - Database username (replacement for `auth.user`).
- `password` - Database password (replacement for `auth.password`).
- `database` - Database name.
- `poolSize` - Set the maximum pool size for each server or proxy connection.
- `tls` - Use a TLS/SSL connection (needs a mongod server with ssl support, 2.4 or higher). Default: `false`.
- `tlsAllowInvalidCertificates` - Specifies whether the driver generates an error when the server's TLS certificate is invalid. Default: `false`.
- `tlsCAFile` - Specifies the location of a local .pem file that contains the root certificate chain from the Certificate Authority.
- `tlsCertificateKeyFile` - Specifies the location of a local .pem file that contains the client's TLS/SSL certificate and key.
- `tlsCertificateKeyFilePassword` - Specifies the password to decrypt the `tlsCertificateKeyFile`.
- `keepAlive` - The number of milliseconds to wait before initiating keepAlive on the TCP socket. Default: `30000`.
- `connectTimeoutMS` - TCP Connection timeout setting. Default: `30000`.
- `socketTimeoutMS` - TCP Socket timeout setting. Default: `360000`.
- `replicaSet` - The name of the replica set to connect to.
- `authSource` - If the database authentication is dependent on another databaseName.
- `writeConcern` - The write concern.
- `forceServerObjectId` - Force server to assign _id values instead of driver. Default: `false`.
- `serializeFunctions` - Serialize functions on any object. Default: `false`.
- `ignoreUndefined` - Specify if the BSON serializer should ignore undefined fields. Default: `false`.
- `raw` - Return document results as raw BSON buffers. Default: `false`.
- `promoteLongs` - Promotes Long values to number if they fit inside the 53-bit resolution. Default: `true`.
- `promoteBuffers` - Promotes Binary BSON values to native Node Buffers. Default: `false`.
- `promoteValues` - Promotes BSON values to native types where possible, set to false to only receive wrapper types.
  Default: `true`.
- `readPreference` - The preferred read preference.
  - `ReadPreference.PRIMARY`
  - `ReadPreference.PRIMARY_PREFERRED`
  - `ReadPreference.SECONDARY`
  - `ReadPreference.SECONDARY_PREFERRED`
  - `ReadPreference.NEAREST`
- `pkFactory` - A primary key factory object for generation of custom _id keys.
- `readConcern` - Specify a read concern for the collection. (only MongoDB 3.2 or higher supported).
- `maxStalenessSeconds` - Specify a maxStalenessSeconds value for secondary reads, minimum is 90 seconds.
- `appName` - The name of the application that created this MongoClient instance. MongoDB 3.4 and newer will print this
  value in the server log upon establishing each connection. It is also recorded in the slow query log and profile
  collections
- `authMechanism` - Sets the authentication mechanism that MongoDB will use to authenticate the connection.
- `directConnection` - Specifies whether to force-dispatch all operations to the specified host.

Additional options can be added to the `extra` object and will be passed directly to the client library. See more in `mongodb`'s documentation for [Connection Options](https://mongodb-node.netlify.app/docs/drivers/node/current/connect/connection-options/).

## Defining entities and columns​

Defining entities and columns is almost the same as in relational databases,
the main difference is that you must use `@ObjectIdColumn`
instead of `@PrimaryColumn` or `@PrimaryGeneratedColumn`.

Simple entity example:

```
import { Entity, ObjectId, ObjectIdColumn, Column } from "typeorm"@Entity()export class User {    @ObjectIdColumn()    _id: ObjectId    @Column()    firstName: string    @Column()    lastName: string}
```

And this is how you bootstrap the app:

```
import { DataSource } from "typeorm"const myDataSource = new DataSource({    type: "mongodb",    host: "localhost",    port: 27017,    database: "test",})
```

## Defining subdocuments (embed documents)​

Since MongoDB stores objects and objects inside objects (or documents inside documents), you can do the same in TypeORM:

```
import { Entity, ObjectId, ObjectIdColumn, Column } from "typeorm"export class Profile {    @Column()    about: string    @Column()    education: string    @Column()    career: string}
```

```
import { Entity, ObjectId, ObjectIdColumn, Column } from "typeorm"export class Photo {    @Column()    url: string    @Column()    description: string    @Column()    size: number    constructor(url: string, description: string, size: number) {        this.url = url        this.description = description        this.size = size    }}
```

```
import { Entity, ObjectId, ObjectIdColumn, Column } from "typeorm"@Entity()export class User {    @ObjectIdColumn()    id: ObjectId    @Column()    firstName: string    @Column()    lastName: string    @Column((type) => Profile)    profile: Profile    @Column((type) => Photo)    photos: Photo[]}
```

If you save this entity:

```
import { getMongoManager } from "typeorm"const user = new User()user.firstName = "Timber"user.lastName = "Saw"user.profile = new Profile()user.profile.about = "About Trees and Me"user.profile.education = "Tree School"user.profile.career = "Lumberjack"user.photos = [    new Photo("me-and-trees.jpg", "Me and Trees", 100),    new Photo("me-and-chakram.jpg", "Me and Chakram", 200),]const manager = getMongoManager()await manager.save(user)
```

The following document will be saved in the database:

```
{    "firstName": "Timber",    "lastName": "Saw",    "profile": {        "about": "About Trees and Me",        "education": "Tree School",        "career": "Lumberjack"    },    "photos": [        {            "url": "me-and-trees.jpg",            "description": "Me and Trees",            "size": 100        },        {            "url": "me-and-chakram.jpg",            "description": "Me and Chakram",            "size": 200        }    ]}
```

## UsingMongoEntityManagerandMongoRepository​

You can use the majority of methods inside the `EntityManager` (except for RDBMS-specific, like `query` and `transaction`).
For example:

```
const timber = await myDataSource.manager.findOneBy(User, {    firstName: "Timber",    lastName: "Saw",})
```

For MongoDB there is also a separate `MongoEntityManager` which extends `EntityManager`.

```
const timber = await myDataSource.manager.findOneBy(User, {    firstName: "Timber",    lastName: "Saw",})
```

Just like separate like `MongoEntityManager` there is a `MongoRepository` with extended `Repository`:

```
const timber = await myDataSource.getMongoRepository(User).findOneBy({    firstName: "Timber",    lastName: "Saw",})
```

Use Advanced options in find():

Equal:

```
const timber = await myDataSource.getMongoRepository(User).find({    where: {        firstName: { $eq: "Timber" },    },})
```

LessThan:

```
const timber = await myDataSource.getMongoRepository(User).find({    where: {        age: { $lt: 60 },    },})
```

In:

```
const timber = await myDataSource.getMongoRepository(User).find({    where: {        firstName: { $in: ["Timber", "Zhang"] },    },})
```

Not in:

```
const timber = await myDataSource.getMongoRepository(User).find({    where: {        firstName: { $not: { $in: ["Timber", "Zhang"] } },    },})
```

Or:

```
const timber = await myDataSource.getMongoRepository(User).find({    where: {        $or: [{ firstName: "Timber" }, { firstName: "Zhang" }],    },})
```

Querying subdocuments

```
const users = await myDataSource.getMongoRepository(User).find({    where: {        "profile.education": { $eq: "Tree School" },    },})
```

Querying Array of subdocuments

```
// Query users with photos of size less than 500const users = await myDataSource.getMongoRepository(User).find({    where: {        "photos.size": { $lt: 500 },    },})
```

Both `MongoEntityManager` and `MongoRepository` contain a lot of useful MongoDB-specific methods:

### createCursor​

Create a cursor for a query that can be used to iterate over results from MongoDB.

### createEntityCursor​

Create a cursor for a query that can be used to iterate over results from MongoDB.
This returns a modified version of the cursor that transforms each result into Entity models.

### aggregate​

Execute an aggregation framework pipeline against the collection.

### bulkWrite​

Perform a bulkWrite operation without a fluent API.

### count​

Count the number of matching documents in the db to a query.

### countDocuments​

Count the number of matching documents in the db to a query.

### createCollectionIndex​

Create an index on the db and collection.

### createCollectionIndexes​

Create multiple indexes in the collection, this method is only supported in MongoDB 2.6 or higher. Earlier versions of MongoDB will throw a "command not supported" error. Index specifications are defined at [createIndexes](http://docs.mongodb.org/manual/reference/command/createIndexes/).

### deleteMany​

Delete multiple documents on MongoDB.

### deleteOne​

Delete a document on MongoDB.

### distinct​

The distinct command returns a list of distinct values for the given key across a collection.

### dropCollectionIndex​

Drops an index from this collection.

### dropCollectionIndexes​

Drops all indexes from the collection.

### findOneAndDelete​

Find a document and delete it in one atomic operation, requires a write lock for the duration of the operation.

### findOneAndReplace​

Find a document and replace it in one atomic operation, requires a write lock for the duration of the operation.

### findOneAndUpdate​

Find a document and update it in one atomic operation, requires a write lock for the duration of the operation.

### geoHaystackSearch​

Execute a geo search using a geo haystack index on a collection.

### geoNear​

Execute the geoNear command to search for items in the collection.

### group​

Run a group command across a collection.

### collectionIndexes​

Retrieve all the indexes of the collection.

### collectionIndexExists​

Retrieve if an index exists on the collection

### collectionIndexInformation​

Retrieve this collection's index info.

### initializeOrderedBulkOp​

Initiate an In order bulk write operation; operations will be serially executed in the order they are added, creating a new operation for each switch in types.

### initializeUnorderedBulkOp​

Initiate an Out of order batch write operation. All operations will be buffered into insert/update/remove commands executed out of order.

### insertMany​

Insert an array of documents into MongoDB.

### insertOne​

Insert a single document into MongoDB.

### isCapped​

Return if the collection is a capped collection.

### listCollectionIndexes​

Get the list of all indexes information for the collection.

### parallelCollectionScan​

Return N number of parallel cursors for a collection allowing parallel reading of the entire collection. There are no ordering guarantees for returned results

### reIndex​

Reindex all indexes on the collection Warning: reIndex is a blocking operation (indexes are rebuilt in the foreground) and will be slow for large collections.

### rename​

Change the name of an existing collection.

### replaceOne​

Replace a document on MongoDB.

### stats​

Get all the collection statistics.

### updateMany​

Update multiple documents within the collection based on the filter.

### updateOne​

Update a single document within the collection based on the filter.
