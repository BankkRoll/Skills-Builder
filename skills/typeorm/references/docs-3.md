# MySQL / MariaDB and more

# MySQL / MariaDB

> MySQL, MariaDB and Amazon Aurora MySQL are supported as TypeORM drivers.

MySQL, MariaDB and Amazon Aurora MySQL are supported as TypeORM drivers.

## Installation​

Either `mysql` or `mysql2` are required to connect to a MySQL/MariaDB data source. Only `mysql2` can connect to MySQL 8.0 or later and is recommended because it is still maintained. See more about [mysql2](https://sidorares.github.io/node-mysql2/docs/history-and-why-mysq2).

```
npm install mysql
```

or:

```
npm install mysql2
```

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options. You can use the data source types `mysql`, `mariadb` and `aurora-mysql` to connect to the respective databases.

- `connectorPackage` - The database client, either `mysql` or `mysql2`. If the specified client cannot be loaded, it will fall back to the alternative. (Current default: `mysql`)
- `url` - Connection url where the connection is performed. Please note that other data source options will override parameters set from url.
- `host` - Database host.
- `port` - Database host port. Default mysql port is `3306`.
- `username` - Database username.
- `password` - Database password.
- `database` - Database name.
- `socketPath` - Database socket path.
- `poolSize` - Maximum number of clients the pool should contain for each connection.
- `charset` and `collation` - The charset/collation for the connection. If an SQL-level charset is specified (like utf8mb4) then the default collation for that charset is used.
- `timezone` - the timezone configured on the MySQL server. This is used to typecast server date/time
  values to JavaScript Date object and vice versa. This can be `local`, `Z`, or an offset in the form
  `+HH:MM` or `-HH:MM`. (Default: `local`)
- `connectTimeout` - The milliseconds before a timeout occurs during the initial connection to the MySQL server.
  (Default: `10000`)
- `acquireTimeout` - The milliseconds before a timeout occurs during the initial connection to the MySQL server. It differs from `connectTimeout` as it governs the TCP connection timeout whereas connectTimeout does not. (default: `10000`)
- `insecureAuth` - Allow connecting to MySQL instances that ask for the old (insecure) authentication method.
  (Default: `false`)
- `supportBigNumbers` - When dealing with big numbers (`BIGINT` and `DECIMAL` columns) in the database,
  you should enable this option (Default: `true`)
- `bigNumberStrings` - Enabling both `supportBigNumbers` and `bigNumberStrings` forces big numbers
  (`BIGINT` and `DECIMAL` columns) to be always returned as JavaScript String objects (Default: `true`).
  Enabling `supportBigNumbers` but leaving `bigNumberStrings` disabled will return big numbers as String
  objects only when they cannot be accurately represented with
  [JavaScript Number objects](http://ecma262-5.com/ELS5_HTML.htm#Section_8.5)
  (which happens when they exceed the `[-2^53, +2^53]` range), otherwise they will be returned as
  Number objects. This option is ignored if `supportBigNumbers` is disabled.
- `dateStrings` - Force date types (`TIMESTAMP`, `DATETIME`, `DATE`) to be returned as strings rather than
  inflated into JavaScript Date objects. Can be true/false or an array of type names to keep as strings.
  (Default: `false`)
- `debug` - Prints protocol details to stdout. Can be true/false or an array of packet type names that
  should be printed. (Default: `false`)
- `trace` - Generates stack traces on Error to include call site of library entrance ("long stack traces").
  Slight performance penalty for most calls. (Default: `true`)
- `multipleStatements` - Allow multiple mysql statements per query. Be careful with this, it could increase the scope
  of SQL injection attacks. (Default: `false`)
- `legacySpatialSupport` - Use legacy spatial functions like `GeomFromText` and `AsText` which have been replaced by the standard-compliant `ST_GeomFromText` or `ST_AsText` in MySQL 8.0. (Current default: true)
- `flags` - List of connection flags to use other than the default ones. It is also possible to blacklist default ones.
  For more information, check [Connection Flags](https://github.com/mysqljs/mysql#connection-flags).
- `ssl` - object with SSL parameters or a string containing the name of the SSL profile.
  See [SSL options](https://github.com/mysqljs/mysql#ssl-options).
- `enableQueryTimeout` - If a value is specified for maxQueryExecutionTime, in addition to generating a warning log when a query exceeds this time limit, the specified maxQueryExecutionTime value is also used as the timeout for the query. For more information, check [mysql timeouts](https://github.com/mysqljs/mysql#timeouts).

Additional options can be added to the `extra` object and will be passed directly to the client library. See more in the [mysql connection options](https://github.com/mysqljs/mysql#connection-options) or the [mysql2 documentation](https://sidorares.github.io/node-mysql2/docs).

## Column Types​

`bit`, `int`, `integer`, `tinyint`, `smallint`, `mediumint`, `bigint`, `float`, `double`, `double precision`, `dec`, `decimal`, `numeric`, `fixed`, `bool`, `boolean`, `date`, `datetime`, `timestamp`, `time`, `year`, `char`, `nchar`, `national char`, `varchar`, `nvarchar`, `national varchar`, `text`, `tinytext`, `mediumtext`, `blob`, `longtext`, `tinyblob`, `mediumblob`, `longblob`, `enum`, `set`, `json`, `binary`, `varbinary`, `geometry`, `point`, `linestring`, `polygon`, `multipoint`, `multilinestring`, `multipolygon`, `geometrycollection`, `uuid`, `inet4`, `inet6`

> Note: `uuid`, `inet4`, and `inet6` are only available for MariaDB and for the respective versions that made them available.

### enumcolumn type​

See [enum column type](https://typeorm.io/docs/entity/entities#enum-column-type).

### setcolumn type​

`set` column type is supported by `mariadb` and `mysql`. There are various possible column definitions:

Using TypeScript enums:

```
export enum UserRole {    ADMIN = "admin",    EDITOR = "editor",    GHOST = "ghost",}@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column({        type: "set",        enum: UserRole,        default: [UserRole.GHOST, UserRole.EDITOR],    })    roles: UserRole[]}
```

Using an array with `set` values:

```
export type UserRoleType = "admin" | "editor" | "ghost"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column({        type: "set",        enum: ["admin", "editor", "ghost"],        default: ["ghost", "editor"],    })    roles: UserRoleType[]}
```

### Vector Types​

MySQL supports the [VECTOR type](https://dev.mysql.com/doc/refman/en/vector.html) since version 9.0, while in MariaDB, [vectors](https://mariadb.com/docs/server/reference/sql-structure/vectors/vector-overview) are available since 11.7.

---

# Oracle

> Installation

## Installation​

```
npm install oracledb
```

By default, the [oracledb](https://github.com/oracle/node-oracledb) uses the "thin mode" to connect. To enable the "thick mode", you need to follow the installation instructions from
their [user guide](https://node-oracledb.readthedocs.io/en/latest/user_guide/installation.html).

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options.

- `sid` - The System Identifier (SID) identifies a specific database instance. For example, "sales".
- `serviceName` - The Service Name is an identifier of a database service. For example, `sales.us.example.com`.

## Column Types​

`char`, `nchar`, `nvarchar2`, `varchar2`, `long`, `raw`, `long raw`, `number`, `numeric`, `float`, `dec`, `decimal`, `integer`, `int`, `smallint`, `real`, `double precision`, `date`, `timestamp`, `timestamp with time zone`, `timestamp with local time zone`, `interval year to month`, `interval day to second`, `bfile`, `blob`, `clob`, `nclob`, `rowid`, `urowid`

---

# Postgres / CockroachDB

> PostgreSQL, CockroachDB and Amazon Aurora Postgres are supported as TypeORM drivers.

PostgreSQL, CockroachDB and Amazon Aurora Postgres are supported as TypeORM drivers.

Databases that are PostgreSQL-compatible can also be used with TypeORM via the `postgres` data source type.

To use YugabyteDB, refer to [their ORM docs](https://docs.yugabyte.com/stable/drivers-orms/nodejs/typeorm/) to get started. Note that because some Postgres features are [not supported](https://docs.yugabyte.com/stable/develop/postgresql-compatibility/#unsupported-postgresql-features) by YugabyteDB, some TypeORM functionality may be limited.

## Installation​

```
npm install pg
```

For streaming support:

```
npm install pg-query-stream
```

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options. You can use the data source type `postgres`, `cockroachdb` or `aurora-postgres` to connect to the respective databases.

- `url` - Connection url where the connection is performed. Please note that other data source options will override parameters set from url.
- `host` - Database host.
- `port` - Database host port. The default Postgres port is `5432`.
- `username` - Database username.
- `password` - Database password.
- `database` - Database name.
- `schema` - Schema name. Default is "public".
- `connectTimeoutMS` - The milliseconds before a timeout occurs during the initial connection to the postgres server. If `undefined`, or set to `0`, there is no timeout. Defaults to `undefined`.
- `ssl` - Object with ssl parameters. See [TLS/SSL](https://node-postgres.com/features/ssl).
- `uuidExtension` - The Postgres extension to use when generating UUIDs. Defaults to `uuid-ossp`. It can be changed to `pgcrypto` if the `uuid-ossp` extension is unavailable.
- `poolErrorHandler` - A function that gets called when the underlying pool emits `'error'` event. Takes a single parameter (error instance) and defaults to logging with `warn` level.
- `maxTransactionRetries` - A maximum number of transaction retries in case of a 40001 error. Defaults to 5.
- `logNotifications` - A boolean to determine whether postgres server [notice messages](https://www.postgresql.org/docs/current/plpgsql-errors-and-messages.html) and [notification events](https://www.postgresql.org/docs/current/sql-notify.html) should be included in client's logs with `info` level (default: `false`).
- `installExtensions` - A boolean to control whether to install necessary postgres extensions automatically or not (default: `true`)
- `applicationName` - A string visible in statistics and logs to help referencing an application to a connection (default: `undefined`)
- `parseInt8` - A boolean to enable parsing 64-bit integers (int8) as JavaScript numbers. By default, `int8` (bigint) values are returned as strings to avoid overflows. JavaScript numbers are IEEE-754 and lose precision over the maximum safe integer (`Number.MAX_SAFE_INTEGER = +2^53`). If you require the full 64-bit range consider working with the returned strings or converting them to native `bigint` instead of using this option.

Additional options can be added to the `extra` object and will be passed directly to the client library. See more in `pg`'s documentation for [Pool](https://node-postgres.com/apis/pool#new-pool) and [Client](https://node-postgres.com/apis/client#new-client).

## Column Types​

### Column types forpostgres​

`int`, `int2`, `int4`, `int8`, `smallint`, `integer`, `bigint`, `decimal`, `numeric`, `real`, `float`, `float4`, `float8`, `double precision`, `money`, `character varying`, `varchar`, `character`, `char`, `text`, `citext`, `hstore`, `bytea`, `bit`, `varbit`, `bit varying`, `timetz`, `timestamptz`, `timestamp`, `timestamp without time zone`, `timestamp with time zone`, `date`, `time`, `time without time zone`, `time with time zone`, `interval`, `bool`, `boolean`, `enum`, `point`, `line`, `lseg`, `box`, `path`, `polygon`, `circle`, `cidr`, `inet`, `macaddr`, `macaddr8`, `tsvector`, `tsquery`, `uuid`, `xml`, `json`, `jsonb`, `jsonpath`, `int4range`, `int8range`, `numrange`, `tsrange`, `tstzrange`, `daterange`, `int4multirange`, `int8multirange`, `nummultirange`, `tsmultirange`, `tstzmultirange`, `multidaterange`, `geometry`, `geography`, `cube`, `ltree`, `vector`, `halfvec`.

### Column types forcockroachdb​

`array`, `bool`, `boolean`, `bytes`, `bytea`, `blob`, `date`, `numeric`, `decimal`, `dec`, `float`, `float4`, `float8`, `double precision`, `real`, `inet`, `int`, `integer`, `int2`, `int8`, `int64`, `smallint`, `bigint`, `interval`, `string`, `character varying`, `character`, `char`, `char varying`, `varchar`, `text`, `time`, `time without time zone`, `timestamp`, `timestamptz`, `timestamp without time zone`, `timestamp with time zone`, `json`, `jsonb`, `uuid`

Note: CockroachDB returns all numeric data types as `string`. However, if you omit the column type and define your property as `number` ORM will `parseInt` string into number.

### Vector columns​

Vector columns can be used for similarity searches using PostgreSQL's vector operators:

```
// L2 distance (Euclidean) - <->const results = await dataSource.sql`    SELECT id, embedding    FROM post    ORDER BY embedding <-> ${"[1,2,3]"}    LIMIT 5`// Cosine distance - <=>const results = await dataSource.sql`    SELECT id, embedding    FROM post    ORDER BY embedding <=> ${"[1,2,3]"}    LIMIT 5`// Inner product - <#>const results = await dataSource.sql`    SELECT id, embedding    FROM post    ORDER BY embedding <#> ${"[1,2,3]"}    LIMIT 5`
```

### Spatial columns​

TypeORM's PostgreSQL and CockroachDB support uses [GeoJSON](http://geojson.org/) as an interchange format, so geometry columns should be tagged either as `object` or `Geometry` (or subclasses, e.g. `Point`) after importing [geojsontypes](https://www.npmjs.com/package/@types/geojson) or using the TypeORM built-in GeoJSON types:

```
import {    Entity,    PrimaryColumn,    Column,    Point,    LineString,    MultiPoint} from "typeorm"@Entity()export class Thing {    @PrimaryColumn()    id: number    @Column("geometry")    point: Point    @Column("geometry")    linestring: LineString    @Column("geometry", {        spatialFeatureType: "MultiPoint",        srid: 4326,    })    multiPointWithSRID: MultiPoint}...const thing = new Thing()thing.point = {    type: "Point",    coordinates: [116.443987, 39.920843],}thing.linestring = {    type: "LineString",    coordinates: [        [-87.623177, 41.881832],        [-90.199402, 38.627003],        [-82.446732, 38.413651],        [-87.623177, 41.881832],    ],}thing.multiPointWithSRID = {    type: "MultiPoint",    coordinates: [        [100.0, 0.0],        [101.0, 1.0],    ],}
```

TypeORM tries to do the right thing, but it's not always possible to determine
when a value being inserted or the result of a PostGIS function should be
treated as a geometry. As a result, you may find yourself writing code similar
to the following, where values are converted into PostGIS `geometry`s from
GeoJSON and into GeoJSON as `json`:

```
import { Point } from "typeorm"const origin: Point = {    type: "Point",    coordinates: [0, 0],}await dataSource.manager    .createQueryBuilder(Thing, "thing")    // convert stringified GeoJSON into a geometry with an SRID that matches the    // table specification    .where(        "ST_Distance(geom, ST_SetSRID(ST_GeomFromGeoJSON(:origin), ST_SRID(geom))) > 0",    )    .orderBy(        "ST_Distance(geom, ST_SetSRID(ST_GeomFromGeoJSON(:origin), ST_SRID(geom)))",        "ASC",    )    .setParameters({        // stringify GeoJSON        origin: JSON.stringify(origin),    })    .getMany()await dataSource.manager    .createQueryBuilder(Thing, "thing")    // convert geometry result into GeoJSON, treated as JSON (so that TypeORM    // will know to deserialize it)    .select("ST_AsGeoJSON(ST_Buffer(geom, 0.1))::json geom")    .from("thing")    .getMany()
```

---

# SAP HANA

> Installation

## Installation​

TypeORM relies on `@sap/hana-client` for establishing the database connection:

```
npm install @sap/hana-client
```

If you are using TypeORM 0.3.25 or earlier, `hdb-pool` is also required for managing the pool.

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options.

- `host` - The hostname of the SAP HANA server. For example, `"localhost"`.
- `port` - The port number of the SAP HANA server. For example, `30015`.
- `username` - The username to connect to the SAP HANA server. For example, `"SYSTEM"`.
- `password` - The password to connect to the SAP HANA server. For example, `"password"`.
- `database` - The name of the database to connect to. For example, `"HXE"`.
- `encrypt` - Whether to encrypt the connection. For example, `true`.
- `sslValidateCertificate` - Whether to validate the SSL certificate. For example, `true`.
- `key`, `cert` and `ca` - Private key, public certificate and certificate authority for the encrypted connection.
- `pool` — Connection pool configuration object:
  - `maxConnectedOrPooled` (number) — Max active or idle connections in the pool (default: 10).
  - `maxPooledIdleTime` (seconds) — Time before an idle connection is closed (default: 30).
  - `maxWaitTimeoutIfPoolExhausted` (milliseconds) - Time to wait for a connection to become available (default: 0, no wait). Requires `@sap/hana-client` version `2.27` or later.
  - `pingCheck` (boolean) — Whether to validate connections before use (default: false).
  - `poolCapacity` (number) — Maximum number of connections to be kept available (default: no limit).

See the official documentation of SAP HANA Client for more details as well as the `extra` properties: [Node.js Connection Properties](https://help.sap.com/docs/SAP_HANA_CLIENT/f1b440ded6144a54ada97ff95dac7adf/4fe9978ebac44f35b9369ef5a4a26f4c.html).

## Column Types​

SAP HANA 2.0 and SAP HANA Cloud support slightly different data types. Check the SAP Help pages for more information:

- [SAP HANA 2.0 Data Types](https://help.sap.com/docs/SAP_HANA_PLATFORM/4fe29514fd584807ac9f2a04f6754767/20a1569875191014b507cf392724b7eb.html?locale=en-US)
- [SAP HANA Cloud Data Types](https://help.sap.com/docs/hana-cloud-database/sap-hana-cloud-sap-hana-database-sql-reference-guide/data-types)

TypeORM's `SapDriver` supports `tinyint`, `smallint`, `integer`, `bigint`, `smalldecimal`, `decimal`, `real`, `double`, `date`, `time`, `seconddate`, `timestamp`, `boolean`, `char`, `nchar`, `varchar`, `nvarchar`, `text`, `alphanum`, `shorttext`, `array`, `varbinary`, `blob`, `clob`, `nclob`, `st_geometry`, `st_point`, `real_vector` and `half_vector`. Some of these data types have been deprecated or removed in SAP HANA Cloud, and will be converted to the closest available alternative when connected to a Cloud database.

### Vector Types​

The `real_vector` and `half_vector` data types were introduced in SAP HANA Cloud (2024Q1 and 2025Q2 respectively), and require a supported version of `@sap/hana-client` as well.

For consistency with PostgreSQL's vector support, TypeORM also provides aliases:

- `vector` (alias for `real_vector`) - stores vectors as 4-byte floats
- `halfvec` (alias for `half_vector`) - stores vectors as 2-byte floats for memory efficiency

```
@Entity()export class Document {    @PrimaryGeneratedColumn()    id: number    // Using SAP HANA native type names    @Column("real_vector", { length: 1536 })    embedding: Buffer | number[]    @Column("half_vector", { length: 768 })    reduced_embedding: Buffer | number[]    // Using cross-database aliases (recommended)    @Column("vector", { length: 1536 })    universal_embedding: Buffer | number[]    @Column("halfvec", { length: 768 })    universal_reduced_embedding: Buffer | number[]}
```

By default, the client will return a `Buffer` in the `fvecs`/`hvecs` format, which is more efficient. It is possible to let the driver convert the values to a `number[]` by adding `{ extra: { vectorOutputType: "Array" } }` to the connection options. Check the SAP HANA Client documentation for more information about [REAL_VECTOR](https://help.sap.com/docs/SAP_HANA_CLIENT/f1b440ded6144a54ada97ff95dac7adf/0d197e4389c64e6b9cf90f6f698f62fe.html) or [HALF_VECTOR](https://help.sap.com/docs/SAP_HANA_CLIENT/f1b440ded6144a54ada97ff95dac7adf/8bb854b4ce4a4299bed27c365b717e91.html).

Use the appropriate [vector functions](https://help.sap.com/docs/hana-cloud-database/sap-hana-cloud-sap-hana-database-sql-reference-guide/vector-functions) for similarity searches.

---

# SQLite

> Installation

## Installation​

- for **SQLite**:

```
npm install sqlite3
```

- for **Better SQLite**:

```
npm install better-sqlite3
```

- for **sql.js**:

```
npm install sql.js
```

- for **Capacitor**, **Cordova**, **Expo**, **NativeScript** and **React Native**, check the [supported platforms](https://typeorm.io/docs/help/supported-platforms).

## Data Source Options​

See [Data Source Options](https://typeorm.io/docs/data-source/data-source-options) for the common data source options.

### sqlitedata source options​

- `database` - Database path. For example, "mydb.sql"

### better-sqlite3data source options​

- `database` - Database path. For example, "mydb.sql"
- `statementCacheSize` - Cache size of the SQLite statement to speed up queries (default 100).
- `prepareDatabase` - Function to run before a database is used in typeorm. You can access the original better-sqlite3 Database object here.
- `nativeBinding` - Relative or absolute path to the native addon (better_sqlite3.node).

### sql.jsdata source options​

- `database`: The raw UInt8Array database that should be imported.
- `sqlJsConfig`: Optional initialize config for sql.js.
- `autoSave`: Enable automatic persistence of database changes, requires either `location` or `autoSaveCallback`. When set to `true`, every change is saved to the file system (Node.js) or to `localStorage`/`indexedDB` (browser) if `location` is specified, or the `autoSaveCallback` is invoked otherwise.
- `autoSaveCallback`: A function that gets called when changes to the database are made and `autoSave` is enabled. The function gets a `UInt8Array` that represents the database.
- `location`: The file location to load and save the database to.
- `useLocalForage`: Enables the usage of the [localforage library](https://github.com/localForage/localForage) to save and load the database asynchronously from the indexedDB instead of using the synchrony local storage methods in a browser environment. The localforage node module needs to be added to your project, and the localforage.js should be imported in your page.

### capacitordata source options​

- `database` - Database name (capacitor-sqlite will add the suffix `SQLite.db`)
- `driver` - The capacitor-sqlite instance. For example, `new SQLiteConnection(CapacitorSQLite)`.
- `mode` - Set the mode for database encryption: "no-encryption" | "encryption" | "secret" | "newsecret"
- `version` - Database version
- `journalMode` - The SQLite journal mode (optional)

### cordovadata source options​

- `database` - Database name
- `location` - Where to save the database. See [cordova-sqlite-storage](https://github.com/litehelpers/Cordova-sqlite-storage#opening-a-database) for options.

### expodata source options​

- `database` - Name of the database. For example, "mydb".
- `driver` - The Expo SQLite module. For example, `require('expo-sqlite')`.

### nativescriptdata source options​

- `database` - Database name

### react-nativedata source options​

- `database` - Database name
- `location` - Where to save the database. See [react-native-sqlite-storage](https://github.com/andpor/react-native-sqlite-storage#opening-a-database) for options.

## Column Types​

`int`, `int2`, `int8`, `integer`, `tinyint`, `smallint`, `mediumint`, `bigint`, `decimal`, `numeric`, `float`, `double`, `real`, `double precision`, `datetime`, `varying character`, `character`, `native character`, `varchar`, `nchar`, `nvarchar2`, `unsigned big int`, `boolean`, `blob`, `text`, `clob`, `date`

---

# Embedded Entities

> There is an amazing way to reduce duplication in your app (using composition over inheritance) by using embedded columns.

There is an amazing way to reduce duplication in your app (using composition over inheritance) by using `embedded columns`.
Embedded column is a column which accepts a class with its own columns and merges those columns into the current entity's database table.
Example:

Let's say we have `User`, `Employee` and `Student` entities.
All those entities have few things in common - `first name` and `last name` properties

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: string    @Column()    firstName: string    @Column()    lastName: string    @Column()    isActive: boolean}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Employee {    @PrimaryGeneratedColumn()    id: string    @Column()    firstName: string    @Column()    lastName: string    @Column()    salary: string}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Student {    @PrimaryGeneratedColumn()    id: string    @Column()    firstName: string    @Column()    lastName: string    @Column()    faculty: string}
```

What we can do is to reduce `firstName` and `lastName` duplication by creating a new class with those columns:

```
import { Column } from "typeorm"export class Name {    @Column()    first: string    @Column()    last: string}
```

Then you can "connect" those columns in your entities:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"import { Name } from "./Name"@Entity()export class User {    @PrimaryGeneratedColumn()    id: string    @Column(() => Name)    name: Name    @Column()    isActive: boolean}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"import { Name } from "./Name"@Entity()export class Employee {    @PrimaryGeneratedColumn()    id: string    @Column(() => Name)    name: Name    @Column()    salary: number}
```

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"import { Name } from "./Name"@Entity()export class Student {    @PrimaryGeneratedColumn()    id: string    @Column(() => Name)    name: Name    @Column()    faculty: string}
```

All columns defined in the `Name` entity will be merged into `user`, `employee` and `student`:

```
+-------------+--------------+----------------------------+|                          user                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || nameFirst   | varchar(255) |                            || nameLast    | varchar(255) |                            || isActive    | boolean      |                            |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|                        employee                         |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || nameFirst   | varchar(255) |                            || nameLast    | varchar(255) |                            || salary      | int          |                            |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|                         student                         |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || nameFirst   | varchar(255) |                            || nameLast    | varchar(255) |                            || faculty     | varchar(255) |                            |+-------------+--------------+----------------------------+
```

This way code duplication in the entity classes is reduced.
You can use as many columns (or relations) in embedded classes as you need.
You even can have nested embedded columns inside embedded classes.

---

# Entities

> What is an Entity?

## What is an Entity?​

Entity is a class that maps to a database table (or collection when using MongoDB).
You can create an entity by defining a new class and mark it with `@Entity()`:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    isActive: boolean}
```

This will create following database table:

```
+-------------+--------------+----------------------------+|                          user                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || firstName   | varchar(255) |                            || lastName    | varchar(255) |                            || isActive    | boolean      |                            |+-------------+--------------+----------------------------+
```

Basic entities consist of columns and relations.
Each entity **MUST** have a primary column (or ObjectId column if are using MongoDB).

Each entity must be registered in your data source options:

```
import { DataSource } from "typeorm"import { User } from "./entity/User"const myDataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    entities: [User],})
```

Or you can specify the whole directory with all entities inside - and all of them will be loaded:

```
import { DataSource } from "typeorm"const dataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    entities: ["entity/*.js"],})
```

If you want to use an alternative table name for the `User` entity you can specify it in `@Entity`: `@Entity("my_users")`.
If you want to set a base prefix for all database tables in your application you can specify `entityPrefix` in data source options.

When using an entity constructor its arguments **must be optional**. Since ORM creates instances of entity classes when loading from the database, therefore it is not aware of your constructor arguments.

Learn more about parameters `@Entity` in [Decorators reference](https://typeorm.io/docs/help/decorator-reference).

## Entity columns​

Since database tables consist of columns your entities must consist of columns too.
Each entity class property you marked with `@Column` will be mapped to a database table column.

### Primary columns​

Each entity must have at least one primary column.
There are several types of primary columns:

- `@PrimaryColumn()` creates a primary column which takes any value of any type. You can specify the column type. If you don't specify a column type it will be inferred from the property type. The example below will create id with `int` as type which you must manually assign before save.

```
import { Entity, PrimaryColumn } from "typeorm"@Entity()export class User {    @PrimaryColumn()    id: number}
```

- `@PrimaryGeneratedColumn()` creates a primary column which value will be automatically generated with an auto-increment value. It will create `int` column with `auto-increment`/`serial`/`sequence`/`identity` (depend on the database and configuration provided). You don't have to manually assign its value before save - value will be automatically generated.

```
import { Entity, PrimaryGeneratedColumn } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number}
```

- `@PrimaryGeneratedColumn("uuid")` creates a primary column which value will be automatically generated with `uuid`. Uuid is a unique string id. You don't have to manually assign its value before save - value will be automatically generated.

```
import { Entity, PrimaryGeneratedColumn } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn("uuid")    id: string}
```

You can have composite primary columns as well:

```
import { Entity, PrimaryColumn } from "typeorm"@Entity()export class User {    @PrimaryColumn()    firstName: string    @PrimaryColumn()    lastName: string}
```

When you save entities using `save` it always tries to find an entity in the database with the given entity id (or ids).
If id/ids are found then it will update this row in the database.
If there is no row with the id/ids, a new row will be inserted.

To find an entity by id you can use `manager.findOneBy` or `repository.findOneBy`. Example:

```
// find one by id with single primary keyconst person = await dataSource.manager.findOneBy(Person, { id: 1 })const person = await dataSource.getRepository(Person).findOneBy({ id: 1 })// find one by id with composite primary keysconst user = await dataSource.manager.findOneBy(User, {    firstName: "Timber",    lastName: "Saw",})const user = await dataSource.getRepository(User).findOneBy({    firstName: "Timber",    lastName: "Saw",})
```

### Special columns​

There are several special column types with additional functionality available:

- `@CreateDateColumn` is a special column that is automatically set to the entity's insertion date.
  You don't need to set this column - it will be automatically set.
- `@UpdateDateColumn` is a special column that is automatically set to the entity's update time
  each time you call `save` of entity manager or repository, or during `upsert` operations when an update occurs.
  You don't need to set this column - it will be automatically set.
- `@DeleteDateColumn` is a special column that is automatically set to the entity's delete time each time you call soft-delete of entity manager or repository. You don't need to set this column - it will be automatically set. If the @DeleteDateColumn is set, the default scope will be "non-deleted".
- `@VersionColumn` is a special column that is automatically set to the version of the entity (incremental number)
  each time you call `save` of entity manager or repository, or during `upsert` operations when an update occurs.
  You don't need to set this column - it will be automatically set.

## Column types​

TypeORM supports all of the most commonly used database-supported column types.
Column types are database-type specific - this provides more flexibility on how your database schema will look like.

You can specify column type as first parameter of `@Column`
or in the column options of `@Column`, for example:

```
@Column("int")
```

or

```
@Column({ type: "int" })
```

If you want to specify additional type parameters you can do it via column options.
For example:

```
@Column("varchar", { length: 200 })
```

> Note about `bigint` type: `bigint` column type, used in SQL databases, doesn't fit into the regular `number` type and maps property to a `string` instead.

### enumcolumn type​

`enum` column type is supported by `postgres` and `mysql`. There are various possible column definitions:

Using typescript enums:

```
export enum UserRole {    ADMIN = "admin",    EDITOR = "editor",    GHOST = "ghost",}@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column({        type: "enum",        enum: UserRole,        default: UserRole.GHOST,    })    role: UserRole}
```

> Note: String, numeric and heterogeneous enums are supported.

Using array with enum values:

```
export type UserRoleType = "admin" | "editor" | "ghost",@Entity()export class User {    @PrimaryGeneratedColumn()    id: number;    @Column({        type: "enum",        enum: ["admin", "editor", "ghost"],        default: "ghost"    })    role: UserRoleType}
```

### simple-arraycolumn type​

There is a special column type called `simple-array` which can store primitive array values in a single string column.
All values are separated by a comma. For example:

```
@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column("simple-array")    names: string[]}
```

```
const user = new User()user.names = ["Alexander", "Alex", "Sasha", "Shurik"]
```

Will be stored in a single database column as `Alexander,Alex,Sasha,Shurik` value.
When you'll load data from the database, the names will be returned as an array of names,
just like you stored them.

Note you **MUST NOT** have any comma in values you write.

### simple-jsoncolumn type​

There is a special column type called `simple-json` which can store any values which can be stored in database
via JSON.stringify.
Very useful when you do not have json type in your database and you want to store and load object
without any hassle.
For example:

```
@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column("simple-json")    profile: { name: string; nickname: string }}
```

```
const user = new User()user.profile = { name: "John", nickname: "Malkovich" }
```

Will be stored in a single database column as `{"name":"John","nickname":"Malkovich"}` value.
When you'll load data from the database, you will have your object/array/primitive back via JSON.parse

### Columns with generated values​

You can create column with generated value using `@Generated` decorator. For example:

```
@Entity()export class User {    @PrimaryColumn()    id: number    @Column()    @Generated("uuid")    uuid: string}
```

`uuid` value will be automatically generated and stored into the database.

Besides "uuid" there is also "increment", "identity" (Postgres 10+ only) and "rowid" (CockroachDB only) generated types, however there are some limitations
on some database platforms with this type of generation (for example some databases can only have one increment column,
or some of them require increment to be a primary key).

### Vector columns​

Vector columns are supported on MariaDB/MySQL, Microsoft SQL Server, PostgreSQL (via [pgvector](https://github.com/pgvector/pgvector) extension) and SAP HANA Cloud, enabling storing and querying vector embeddings for similarity search and machine learning applications.

TypeORM supports both `vector` and `halfvec` column types across databases:

- `vector` - stores vectors as 4-byte floats (single precision)
  - MariaDB/MySQL: native `vector` type
  - Microsoft SQL Server: native `vector` type
  - PostgreSQL: `vector` type, available via `pgvector` extension
  - SAP HANA Cloud: alias for `real_vector` type
- `halfvec` - stores vectors as 2-byte floats (half precision) for memory efficiency
  - PostgreSQL: `halfvec` type, available via `pgvector` extension
  - SAP HANA Cloud: alias for `half_vector` type

You can specify the number of vector dimensions using the `length` option:

```
@Entity()export class Post {    @PrimaryGeneratedColumn()    id: number    // Vector without specified dimensions    @Column("vector")    embedding: number[] | Buffer    // Vector with 3 dimensions: vector(3)    @Column("vector", { length: 3 })    embedding_3d: number[] | Buffer    // Half-precision vector with 4 dimensions: halfvec(4) (works on PostgreSQL and SAP HANA only)    @Column("halfvec", { length: 4 })    halfvec_embedding: number[] | Buffer}
```

> **Note**:
>
>
>
> - **MariaDB/MySQL**: Vectors are supported since MariaDB 11.7 and MySQL 9
> - **Microsoft SQL Server**: Vector type support requires SQL Server 2025 (17.x) or newer.
> - **PostgreSQL**: Vector columns require the `pgvector` extension to be installed. The extension provides the vector data types and similarity operators.
> - **SAP HANA**: Vector columns require SAP HANA Cloud (2024Q1+) and a supported version of `@sap/hana-client`.

### Spatial columns​

Microsoft SQLServer, MySQL/MariaDB, PostgreSQL/CockroachDB and SAP HANA all support spatial columns. TypeORM's support for each varies slightly between databases, particularly as the column names vary between databases.

MS SQL, MySQL/MariaDB and SAP HANA use geometries in the [well-known text
(WKT)](https://en.wikipedia.org/wiki/Well-known_text) format, so geometry columns
should be tagged with the `string` type.

```
import { Entity, PrimaryColumn, Column } from "typeorm"@Entity()export class Thing {    @PrimaryColumn()    id: number    @Column("point")    point: string    @Column("linestring")    linestring: string}...const thing = new Thing()thing.point = "POINT(1 1)"thing.linestring = "LINESTRING(0 0,1 1,2 2)"
```

For Postgres/CockroachDB, see [Postgis Data Types](https://typeorm.io/docs/drivers/postgres#spatial-columns)

## Column options​

Column options defines additional options for your entity columns.
You can specify column options on `@Column`:

```
@Column({    type: "varchar",    length: 150,    unique: true,    // ...})name: string;
```

List of available options in `ColumnOptions`:

- `type: ColumnType` - Column type. One of the type listed [above](#column-types).
- `name: string` - Column name in the database table.
  By default the column name is generated from the name of the property.
  You can change it by specifying your own name.
- `length: number` - Column type's length. For example if you want to create `varchar(150)` type you specify column type and length options.
- `onUpdate: string` - `ON UPDATE` trigger. Used only in [MySQL](https://dev.mysql.com/doc/refman/5.7/en/timestamp-initialization.html).
- `nullable: boolean` - Makes column `NULL` or `NOT NULL` in the database. By default column is `nullable: false`.
- `update: boolean` - Indicates if column value is updated by "save" operation. If false, you'll be able to write this value only when you first time insert the object. Default value is `true`.
- `insert: boolean` - Indicates if column value is set the first time you insert the object. Default value is `true`.
- `select: boolean` - Defines whether or not to hide this column by default when making queries. When set to `false`, the column data will not show with a standard query. By default column is `select: true`
- `default: string` - Adds database-level column's `DEFAULT` value.
- `primary: boolean` - Marks column as primary. Same if you use `@PrimaryColumn`.
- `unique: boolean` - Marks column as unique column (creates unique constraint).
- `comment: string` - Database's column comment. Not supported by all database types.
- `precision: number` - The precision for a decimal (exact numeric) column (applies only for decimal column), which is the maximum
  number of digits that are stored for the values. Used in some column types.
- `scale: number` - The scale for a decimal (exact numeric) column (applies only for decimal column), which represents the number of digits to the right of the decimal point and must not be greater than precision. Used in some column types.
- `unsigned: boolean` - Puts `UNSIGNED` attribute on to a numeric column. Used only in MySQL.
- `charset: string` - Defines a column character set. Not supported by all database types.
- `collation: string` - Defines a column collation.
- `enum: string[]|AnyEnum` - Used in `enum` column type to specify list of allowed enum values. You can specify array of values or specify a enum class.
- `enumName: string` - Defines the name for the used enum.
- `asExpression: string` - Generated column expression. Used only in [MySQL](https://dev.mysql.com/doc/refman/5.7/en/create-table-generated-columns.html).
- `generatedType: "VIRTUAL"|"STORED"` - Generated column type. Used only in [MySQL](https://dev.mysql.com/doc/refman/5.7/en/create-table-generated-columns.html).
- `hstoreType: "object"|"string"` - Return type of `HSTORE` column. Returns value as string or as object. Used only in [Postgres](https://www.postgresql.org/docs/9.6/static/hstore.html).
- `array: boolean` - Used for postgres and cockroachdb column types which can be array (for example int[])
- `transformer: { from(value: DatabaseType): EntityType, to(value: EntityType): DatabaseType }` - Used to marshal properties of arbitrary type `EntityType` into a type `DatabaseType` supported by the database. Array of transformers are also supported and will be applied in natural order when writing, and in reverse order when reading. e.g. `[lowercase, encrypt]` will first lowercase the string then encrypt it when writing, and will decrypt then do nothing when reading.
- `utc: boolean` - Indicates if date values should be stored and retrieved in UTC timezone instead of local timezone. Only applies to `date` column type. Default value is `false` (uses local timezone for backward compatibility).

Note: most of those column options are RDBMS-specific and aren't available in `MongoDB`.

## Entity inheritance​

You can reduce duplication in your code by using entity inheritance.

For example, you have `Photo`, `Question`, `Post` entities:

```
@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    size: string}@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    answersCount: number}@Entity()export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    viewCount: number}
```

As you can see all those entities have common columns: `id`, `title`, `description`. To reduce duplication and produce a better abstraction we can create a base class called `Content` for them:

```
export abstract class Content {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string}@Entity()export class Photo extends Content {    @Column()    size: string}@Entity()export class Question extends Content {    @Column()    answersCount: number}@Entity()export class Post extends Content {    @Column()    viewCount: number}
```

All columns (relations, embeds, etc.) from parent entities (parent can extend other entity as well)
will be inherited and created in final entities.

## Tree entities​

TypeORM supports the Adjacency list and Closure table patterns of storing tree structures.

### Adjacency list​

Adjacency list is a simple model with self-referencing.
Benefit of this approach is simplicity,
drawback is you can't load a big tree at once because of join limitations.
Example:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    ManyToOne,    OneToMany,} from "typeorm"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column()    description: string    @ManyToOne((type) => Category, (category) => category.children)    parent: Category    @OneToMany((type) => Category, (category) => category.parent)    children: Category[]}
```

### Closure table​

A closure table stores relations between parent and child in a separate table in a special way.
It's efficient in both reads and writes.
To learn more about closure table take a look at [this awesome presentation by Bill Karwin](https://www.slideshare.net/billkarwin/models-for-hierarchical-data).
Example:

```
import {    Entity,    Tree,    Column,    PrimaryGeneratedColumn,    TreeChildren,    TreeParent,    TreeLevelColumn,} from "typeorm"@Entity()@Tree("closure-table")export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column()    description: string    @TreeChildren()    children: Category[]    @TreeParent()    parent: Category    @TreeLevelColumn()    level: number}
```
