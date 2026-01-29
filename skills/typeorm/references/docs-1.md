# Indices and more

# Indices

> Column indices

## Column indices​

You can create a database index for a specific column by using `@Index` on a column you want to make an index.
You can create indices for any columns of your entity.
Example:

```
import { Entity, PrimaryGeneratedColumn, Column, Index } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Index()    @Column()    firstName: string    @Column()    @Index()    lastName: string}
```

You can also specify an index name:

```
import { Entity, PrimaryGeneratedColumn, Column, Index } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Index("name1-idx")    @Column()    firstName: string    @Column()    @Index("name2-idx")    lastName: string}
```

## Unique indices​

To create a unique index you need to specify `{ unique: true }` in the index options:

> Note: CockroachDB stores unique indices as `UNIQUE` constraints

```
import { Entity, PrimaryGeneratedColumn, Column, Index } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Index({ unique: true })    @Column()    firstName: string    @Column()    @Index({ unique: true })    lastName: string}
```

## Indices with multiple columns​

To create an index with multiple columns you need to put `@Index` on the entity itself
and specify all column property names which should be included in the index.
Example:

```
import { Entity, PrimaryGeneratedColumn, Column, Index } from "typeorm"@Entity()@Index(["firstName", "lastName"])@Index(["firstName", "middleName", "lastName"], { unique: true })export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    middleName: string    @Column()    lastName: string}
```

## Spatial Indices​

MySQL, CockroachDB and PostgreSQL (when PostGIS is available) supports spatial indices.

To create a spatial index on a column in MySQL, add an `Index` with `spatial: true` on a column that uses a spatial type (`geometry`, `point`, `linestring`,
`polygon`, `multipoint`, `multilinestring`, `multipolygon`,
`geometrycollection`):

```
@Entity()export class Thing {    @Column("point")    @Index({ spatial: true })    point: string}
```

To create a spatial index on a column add an `Index` with `spatial: true` on a column that uses a spatial type (`geometry`, `geography`):

```
export interface Geometry {    type: "Point"    coordinates: [Number, Number]}@Entity()export class Thing {    @Column("geometry", {        spatialFeatureType: "Point",        srid: 4326,    })    @Index({ spatial: true })    point: Geometry}
```

## Concurrent creation​

In order to avoid having to obtain an ACCESS EXCLUSIVE lock when creating and dropping indexes in Postgres, you may create them using the CONCURRENTLY modifier.
If you want to use the concurrent option, you need to set `migrationsTransactionMode: none` in your data source options.

TypeORM supports generating SQL with this option when the concurrent option is specified on the index.

```
@Index(["firstName", "middleName", "lastName"], { concurrent: true })
```

For more information see the [Postgres documentation](https://www.postgresql.org/docs/current/sql-createindex.html).

## Disabling synchronization​

TypeORM does not support some index options and definitions (e.g. `lower`, `pg_trgm`) due to many database-specific differences and multiple
issues with getting information about existing database indices and synchronizing them automatically. In such cases you should create the index manually
(for example, in [the migrations](https://typeorm.io/docs/migrations/why)) with any index signature you want. To make TypeORM ignore these indices during synchronization, use `synchronize: false`
option on the `@Index` decorator.

For example, you create an index with case-insensitive comparison:

```
CREATE INDEX "POST_NAME_INDEX" ON "post" (lower("name"))
```

after that, you should disable synchronization for this index to avoid deletion on next schema sync:

```
@Entity()@Index("POST_NAME_INDEX", { synchronize: false })export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string}
```

---

# Entity Listeners and Subscribers

> What is an Entity Listener?

## What is an Entity Listener?​

Any of your entities can have methods with custom logic that listen to specific entity events.
You must mark those methods with special decorators depending on what event you want to listen to.

**Note:** Do not make any database calls within a listener, opt for [subscribers](#what-is-a-subscriber) instead.

### @AfterLoad​

You can define a method with any name in entity and mark it with `@AfterLoad`
and TypeORM will call it each time the entity
is loaded using `QueryBuilder` or repository/manager find methods.
Example:

```
@Entity()export class Post {    @AfterLoad()    updateCounters() {        if (this.likesCount === undefined) this.likesCount = 0    }}
```

### @BeforeInsert​

You can define a method with any name in entity and mark it with `@BeforeInsert`
and TypeORM will call it before the entity is inserted using repository/manager `save`.
Example:

```
@Entity()export class Post {    @BeforeInsert()    updateDates() {        this.createdDate = new Date()    }}
```

### @AfterInsert​

You can define a method with any name in entity and mark it with `@AfterInsert`
and TypeORM will call it after the entity is inserted using repository/manager `save`.
Example:

```
@Entity()export class Post {    @AfterInsert()    resetCounters() {        this.counters = 0    }}
```

### @BeforeUpdate​

You can define a method with any name in the entity and mark it with `@BeforeUpdate`
and TypeORM will call it before an existing entity is updated using repository/manager `save`. Keep in mind, however, that this will occur only when information is changed in the model. If you run `save` without modifying anything from the model, `@BeforeUpdate` and `@AfterUpdate` will not run.
Example:

```
@Entity()export class Post {    @BeforeUpdate()    updateDates() {        this.updatedDate = new Date()    }}
```

### @AfterUpdate​

You can define a method with any name in the entity and mark it with `@AfterUpdate`
and TypeORM will call it after an existing entity is updated using repository/manager `save`.
Example:

```
@Entity()export class Post {    @AfterUpdate()    updateCounters() {        this.counter = 0    }}
```

### @BeforeRemove​

You can define a method with any name in the entity and mark it with `@BeforeRemove`
and TypeORM will call it before an entity is removed using repository/manager `remove`.
Example:

```
@Entity()export class Post {    @BeforeRemove()    updateStatus() {        this.status = "removed"    }}
```

### @AfterRemove​

You can define a method with any name in the entity and mark it with `@AfterRemove`
and TypeORM will call it after the entity is removed using repository/manager `remove`.
Example:

```
@Entity()export class Post {    @AfterRemove()    updateStatus() {        this.status = "removed"    }}
```

### @BeforeSoftRemove​

You can define a method with any name in the entity and mark it with `@BeforeSoftRemove`
and TypeORM will call it before an entity is soft removed using repository/manager `softRemove`.
Example:

```
@Entity()export class Post {    @BeforeSoftRemove()    updateStatus() {        this.status = "soft-removed"    }}
```

### @AfterSoftRemove​

You can define a method with any name in the entity and mark it with `@AfterSoftRemove`
and TypeORM will call it after the entity is soft removed using repository/manager `softRemove`.
Example:

```
@Entity()export class Post {    @AfterSoftRemove()    updateStatus() {        this.status = "soft-removed"    }}
```

### @BeforeRecover​

You can define a method with any name in the entity and mark it with `@BeforeRecover`
and TypeORM will call it before an entity is recovered using repository/manager `recover`.
Example:

```
@Entity()export class Post {    @BeforeRecover()    updateStatus() {        this.status = "recovered"    }}
```

### @AfterRecover​

You can define a method with any name in the entity and mark it with `@AfterRecover`
and TypeORM will call it after the entity is recovered using repository/manager `recover`.
Example:

```
@Entity()export class Post {    @AfterRecover()    updateStatus() {        this.status = "recovered"    }}
```

## What is a Subscriber?​

Marks a class as an event subscriber which can listen to specific entity events or any entity events.
Events are firing using `QueryBuilder` and repository/manager methods.
Example:

```
@EventSubscriber()export class PostSubscriber implements EntitySubscriberInterface<Post> {    /**     * Indicates that this subscriber only listen to Post events.     */    listenTo() {        return Post    }    /**     * Called before post insertion.     */    beforeInsert(event: InsertEvent<Post>) {        console.log(`BEFORE POST INSERTED: `, event.entity)    }}
```

You can implement any method from `EntitySubscriberInterface`.
To listen to any entity you just omit `listenTo` method and use `any`:

```
@EventSubscriber()export class PostSubscriber implements EntitySubscriberInterface {    /**     * Called after entity is loaded.     */    afterLoad(entity: any) {        console.log(`AFTER ENTITY LOADED: `, entity)    }    /**     * Called before query execution.     */    beforeQuery(event: BeforeQueryEvent<any>) {        console.log(`BEFORE QUERY: `, event.query)    }    /**     * Called after query execution.     */    afterQuery(event: AfterQueryEvent<any>) {        console.log(`AFTER QUERY: `, event.query)    }    /**     * Called before entity insertion.     */    beforeInsert(event: InsertEvent<any>) {        console.log(`BEFORE ENTITY INSERTED: `, event.entity)    }    /**     * Called after entity insertion.     */    afterInsert(event: InsertEvent<any>) {        console.log(`AFTER ENTITY INSERTED: `, event.entity)    }    /**     * Called before entity update.     */    beforeUpdate(event: UpdateEvent<any>) {        console.log(`BEFORE ENTITY UPDATED: `, event.entity)    }    /**     * Called after entity update.     */    afterUpdate(event: UpdateEvent<any>) {        console.log(`AFTER ENTITY UPDATED: `, event.entity)    }    /**     * Called before entity removal.     */    beforeRemove(event: RemoveEvent<any>) {        console.log(            `BEFORE ENTITY WITH ID ${event.entityId} REMOVED: `,            event.entity,        )    }    /**     * Called after entity removal.     */    afterRemove(event: RemoveEvent<any>) {        console.log(            `AFTER ENTITY WITH ID ${event.entityId} REMOVED: `,            event.entity,        )    }    /**     * Called before entity removal.     */    beforeSoftRemove(event: SoftRemoveEvent<any>) {        console.log(            `BEFORE ENTITY WITH ID ${event.entityId} SOFT REMOVED: `,            event.entity,        )    }    /**     * Called after entity removal.     */    afterSoftRemove(event: SoftRemoveEvent<any>) {        console.log(            `AFTER ENTITY WITH ID ${event.entityId} SOFT REMOVED: `,            event.entity,        )    }    /**     * Called before entity recovery.     */    beforeRecover(event: RecoverEvent<any>) {        console.log(            `BEFORE ENTITY WITH ID ${event.entityId} RECOVERED: `,            event.entity,        )    }    /**     * Called after entity recovery.     */    afterRecover(event: RecoverEvent<any>) {        console.log(            `AFTER ENTITY WITH ID ${event.entityId} RECOVERED: `,            event.entity,        )    }    /**     * Called before transaction start.     */    beforeTransactionStart(event: TransactionStartEvent) {        console.log(`BEFORE TRANSACTION STARTED: `, event)    }    /**     * Called after transaction start.     */    afterTransactionStart(event: TransactionStartEvent) {        console.log(`AFTER TRANSACTION STARTED: `, event)    }    /**     * Called before transaction commit.     */    beforeTransactionCommit(event: TransactionCommitEvent) {        console.log(`BEFORE TRANSACTION COMMITTED: `, event)    }    /**     * Called after transaction commit.     */    afterTransactionCommit(event: TransactionCommitEvent) {        console.log(`AFTER TRANSACTION COMMITTED: `, event)    }    /**     * Called before transaction rollback.     */    beforeTransactionRollback(event: TransactionRollbackEvent) {        console.log(`BEFORE TRANSACTION ROLLBACK: `, event)    }    /**     * Called after transaction rollback.     */    afterTransactionRollback(event: TransactionRollbackEvent) {        console.log(`AFTER TRANSACTION ROLLBACK: `, event)    }}
```

Make sure your `subscribers` property is set in your [DataSourceOptions](https://typeorm.io/docs/data-source/data-source-options#common-data-source-options) so TypeORM loads your subscriber.

### Event Object​

Excluding `listenTo`, all `EntitySubscriberInterface` methods are passed an event object that has the following base properties:

- `dataSource: DataSource` - DataSource used in the event.
- `queryRunner: QueryRunner` - QueryRunner used in the event transaction.
- `manager: EntityManager` - EntityManager used in the event transaction.

See each [Event's interface](https://github.com/typeorm/typeorm/tree/master/src/subscriber/event) for additional properties.

Note that `event.entity` may not necessarily contain primary key(s) when `Repository.update()` is used. Only the values provided as the entity partial will be available. In order to make primary keys available in the subscribers, you can explicitly pass primary key value(s) in the partial entity object literal or use `Repository.save()`, which performs re-fetching.

```
await postRepository.update(post.id, { description: "Bacon ipsum dolor amet cow" })// post.subscriber.tsafterUpdate(event: UpdateEvent<Post>) {  console.log(event.entity) // outputs { description: 'Bacon ipsum dolor amet cow' }}
```

**Note:** All database operations in the subscribed event listeners should be performed using the event object's `queryRunner` or `manager` instance.

---

# Logging

> Enabling logging

## Enabling logging​

You can enable logging of all queries and errors by simply setting `logging: true` in data source options:

```
{    name: "mysql",    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    ...    logging: true}
```

## Logging options​

You can enable different types of logging in data source options:

```
{    host: "localhost",    ...    logging: ["query", "error"]}
```

If you want to enable logging of failed queries only then only add `error`:

```
{    host: "localhost",    ...    logging: ["error"]}
```

There are other options you can use:

- `query` - logs all queries.
- `error` - logs all failed queries and errors.
- `schema` - logs the schema build process.
- `warn` - logs internal orm warnings.
- `info` - logs internal orm informative messages.
- `log` - logs internal orm log messages.

You can specify as many options as needed.
If you want to enable all logging you can simply specify `logging: "all"`:

```
{    host: "localhost",    ...    logging: "all"}
```

## Log long-running queries​

If you have performance issues, you can log queries that take too much time to execute
by setting `maxQueryExecutionTime` in data source options:

```
{    host: "localhost",    ...    maxQueryExecutionTime: 1000}
```

This code will log all queries which run for more than `1 second`.

## Changing default logger​

TypeORM ships with 4 different types of logger:

- `advanced-console` - this is the default logger which logs all messages into the console using color
  and sql syntax highlighting.
- `simple-console` - this is a simple console logger which is exactly the same as the advanced logger, but it does not use any color highlighting.
  This logger can be used if you have problems / or don't like colorized logs.
- `formatted-console` - this is almost the same as the advanced logger, but it formats sql queries to
  be more readable (using [@sqltools/formatter](https://github.com/mtxr/vscode-sqltools)).
- `file` - this logger writes all logs into `ormlogs.log` in the root folder of your project (near `package.json`).
- `debug` - this logger uses [debug package](https://github.com/visionmedia/debug), to turn on logging set your env variable `DEBUG=typeorm:*` (note logging option has no effect on this logger).

You can enable any of them in data source options:

```
{    host: "localhost",    ...    logging: true,    logger: "file"}
```

## Using custom logger​

You can create your own logger class by implementing the `Logger` interface:

```
import { Logger } from "typeorm"export class MyCustomLogger implements Logger {    // implement all methods from logger class}
```

Or you can extend the `AbstractLogger` class:

```
import { AbstractLogger } from "typeorm"export class MyCustomLogger extends AbstractLogger {    /**     * Write log to specific output.     */    protected writeLog(        level: LogLevel,        logMessage: LogMessage | LogMessage[],        queryRunner?: QueryRunner,    ) {        const messages = this.prepareLogMessages(logMessage, {            highlightSql: false,        }, queryRunner)        for (let message of messages) {            switch (message.type ?? level) {                case "log":                case "schema-build":                case "migration":                    console.log(message.message)                    break                case "info":                case "query":                    if (message.prefix) {                        console.info(message.prefix, message.message)                    } else {                        console.info(message.message)                    }                    break                case "warn":                case "query-slow":                    if (message.prefix) {                        console.warn(message.prefix, message.message)                    } else {                        console.warn(message.message)                    }                    break                case "error":                case "query-error":                    if (message.prefix) {                        console.error(message.prefix, message.message)                    } else {                        console.error(message.message)                    }                    break            }        }    }}
```

And specify it in data source options:

```
import { DataSource } from "typeorm"import { MyCustomLogger } from "./logger/MyCustomLogger"const dataSource = new DataSource({    name: "mysql",    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    logger: new MyCustomLogger(),})
```

Logger methods can accept `QueryRunner` when it's available. It's helpful if you want to log additional data.
Also, via query runner, you can get access to additional data passed during to persist/remove. For example:

```
// user sends request during entity savepostRepository.save(post, { data: { request: request } });// in logger you can access it this way:logQuery(query: string, parameters?: any[], queryRunner?: QueryRunner) {    const requestUrl = queryRunner && queryRunner.data["request"] ? "(" + queryRunner.data["request"].url + ") " : "";    console.log(requestUrl + "executing query: " + query);}
```

---

# Performance and optimization in TypeORM

> 1. Introduction to performance optimization

## 1. Introduction to performance optimization​

- In applications using ORM like TypeORM, performance optimization is crucial to ensure the system runs smoothly, minimizes latency, and uses resources efficiently.
- Common challenges when using ORM include unnecessary data retrieval, N+1 query problems, and not leveraging optimization tools such as indexing or caching.
- The main goals of optimization include:
  - Reducing the number of SQL queries sent to the database.
  - Optimizing complex queries to run faster.
  - Using caching and indexing to speed up data retrieval.
  - Ensuring efficient data retrieval using appropriate loading methods (Lazy vs. Eager loading).

## 2. Efficient use of Query Builder​

### 2.1. Avoiding the N+1 Query Problem​

- The N+1 Query Problem occurs when the system executes too many sub-queries for each row of data retrieved.
- To avoid this, you can use `leftJoinAndSelect` or `innerJoinAndSelect` to combine tables in a single query instead of executing multiple queries.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.posts", "post")    .getMany()
```

- Here, `leftJoinAndSelect` helps retrieve all user posts in a single query rather than many small queries.

### 2.2. UsegetRawMany()when only raw data is needed​

- In cases where full objects aren't required, you can use `getRawMany()` to fetch raw data and avoid TypeORM processing too much information.

```
const rawPosts = await dataSource    .getRepository(Post)    .createQueryBuilder("post")    .select("post.title, post.createdAt")    .getRawMany()
```

### 2.3. Limit fields usingselect​

- To optimize memory usage and reduce unnecessary data, select only the required fields using `select`.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select(["user.name", "user.email"])    .getMany()
```

## 3. Using indices​

- Indexes speed up query performance in the database by reducing the amount of data scanned. TypeORM supports creating indexes on table columns using the `@Index` decorator.

### 3.1. Creating an index​

- Indexes can be created directly in entities using the `@Index` decorator.

```
import { Entity, Column, Index } from "typeorm"@Entity()@Index(["firstName", "lastName"]) // Composite indexexport class User {    @Column()    firstName: string    @Column()    lastName: string}
```

### 3.2. Unique index​

- You can create unique indexes to ensure no duplicate values in a column.

```
@Index(["email"], { unique: true })
```

## 4. Lazy loading and Eager Loading​

TypeORM provides two main methods for loading data relations: Lazy Loading and Eager Loading. Each has a different impact on the performance of your application.

### 4.1. Lazy loading​

- Lazy loading loads the relation data only when needed, reducing database load when all related data isn't always necessary.

```
@Entity()export class User {    @OneToMany(() => Post, (post) => post.user, { lazy: true })    posts: Promise<Post[]>}
```

- When you need to retrieve the data, simply call

```
const user = await userRepository.findOne(userId)const posts = await user.posts
```

- Advantages:
  - Resource efficiency: Only loads the necessary data when actually required, reducing query costs and memory usage.
  - Ideal for selective data usage: Suitable for scenarios where not all related data is needed.
- Disadvantages:
  - Increased query complexity: Each access to related data triggers an additional query to the database, which may increase latency if not managed properly.
  - Difficult to track: Can lead to the n+1 query problem if used carelessly.

### 4.2. Eager Loading​

- Eager loading automatically retrieves all related data when the main query is executed. This can be convenient but may cause performance issues if there are too many complex relations.

```
@Entity()export class User {    @OneToMany(() => Post, (post) => post.user, { eager: true })    posts: Post[]}
```

- In this case, posts will be loaded as soon as user data is retrieved.
- Advantages:
  - Automatically loads related data, making it easier to access relationships without additional queries.
  - Avoids the n+1 query problem: Since all data is fetched in a single query, there's no risk of generating unnecessary multiple queries.
- Disadvantages:
  - Fetching all related data at once may result in large queries, even if not all data is needed.
  - Not suitable for scenarios where only a subset of related data is required, as it can lead to inefficient data usage.
- To explore more details and examples of how to configure and use lazy and eager relations, visit the official TypeORM documentation: [Eager and Lazy Relations](https://typeorm.io/docs/relations/eager-and-lazy-relations)

## 5. Advanced optimization​

### 5.1. Using Query Hints​

- Query Hints are instructions sent along with SQL queries, helping the database decide on more efficient execution strategies.
- Different RDBMS systems support different kinds of hints, such as suggesting index usage or choosing the appropriate JOIN type.

```
await dataSource.query(`    SELECT /*+ MAX_EXECUTION_TIME(1000) */ *    FROM user    WHERE email = 'example@example.com'`)
```

- In the example above, `MAX_EXECUTION_TIME(1000)` instructs MySQL to stop the query if it takes more than 1 second.

### 5.2. Pagination​

- Pagination is a crucial technique for improving performance when retrieving large amounts of data. Instead of fetching all data at once, pagination divides data into smaller pages, reducing database load and optimizing memory usage.
- In TypeORM, you can use `limit` and `offset` for pagination.

```
const users = await userRepository    .createQueryBuilder("user")    .limit(10) // Number of records to fetch per page    .offset(20) // Skip the first 20 records    .getMany()
```

- Pagination helps prevent fetching large amounts of data at once, minimizing latency and optimizing memory usage. When implementing pagination, consider using pagination cursors for more efficient handling of dynamic data.

### 5.3. Caching​

- Caching is the technique of temporarily storing query results or data for use in future requests without querying the database each time.
- TypeORM has built-in caching support, and you can customize how caching is used.

```
const users = await userRepository    .createQueryBuilder("user")    .cache(true) // Enable caching    .getMany()
```

- Additionally, you can configure cache duration or use external caching tools like Redis for better efficiency.

```
const dataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    cache: {        type: "redis",        options: {            host: "localhost",            port: 6379        }    }});
```

---

# Transactions

> Creating and using transactions

## Creating and using transactions​

Transactions are created using `DataSource` or `EntityManager`.
Examples:

```
await myDataSource.transaction(async (transactionalEntityManager) => {    // execute queries using transactionalEntityManager})
```

or

```
await myDataSource.manager.transaction(async (transactionalEntityManager) => {    // execute queries using transactionalEntityManager})
```

Everything you want to run in a transaction must be executed in a callback:

```
await myDataSource.manager.transaction(async (transactionalEntityManager) => {    await transactionalEntityManager.save(users)    await transactionalEntityManager.save(photos)    // ...})
```

The most important restriction when working in a transaction is to **ALWAYS** use the provided instance of entity manager -
`transactionalEntityManager` in this example. DO NOT USE GLOBAL ENTITY MANAGER.
All operations **MUST** be executed using the provided transactional entity manager.

### Specifying Isolation Levels​

Specifying the isolation level for the transaction can be done by supplying it as the first parameter:

```
await myDataSource.manager.transaction(    "SERIALIZABLE",    (transactionalEntityManager) => {},)
```

Isolation level implementations are *not* agnostic across all databases.

The following database drivers support the standard isolation levels (`READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`):

- MySQL
- Postgres
- SQL Server

**SQLite** defaults transactions to `SERIALIZABLE`, but if *shared cache mode* is enabled, a transaction can use the `READ UNCOMMITTED` isolation level.

**Oracle** only supports the `READ COMMITTED` and `SERIALIZABLE` isolation levels.

## UsingQueryRunnerto create and control state of single database connection​

`QueryRunner` provides a single database connection.
Transactions are organized using query runners.
Single transactions can only be established on a single query runner.
You can manually create a query runner instance and use it to manually control transaction state.
Example:

```
// create a new query runnerconst queryRunner = dataSource.createQueryRunner()// establish real database connection using our new query runnerawait queryRunner.connect()// now we can execute any queries on a query runner, for example:await queryRunner.query("SELECT * FROM users")// we can also access entity manager that works with connection created by a query runner:const users = await queryRunner.manager.find(User)// lets now open a new transaction:await queryRunner.startTransaction()try {    // execute some operations on this transaction:    await queryRunner.manager.save(user1)    await queryRunner.manager.save(user2)    await queryRunner.manager.save(photos)    // commit transaction now:    await queryRunner.commitTransaction()} catch (err) {    // since we have errors let's rollback changes we made    await queryRunner.rollbackTransaction()} finally {    // you need to release query runner which is manually created:    await queryRunner.release()}
```

There are 3 methods to control transactions in `QueryRunner`:

- `startTransaction` - starts a new transaction inside the query runner instance.
- `commitTransaction` - commits all changes made using the query runner instance.
- `rollbackTransaction` - rolls all changes made using the query runner instance back.

Learn more about [Query Runner](https://typeorm.io/docs/query-runner).

---

# Using CLI

> Installing CLI

## Installing CLI​

### If entities files are in javascript​

If you have a local typeorm version, make sure it matches the global version we are going to install.

You can install typeorm globally with `npm i -g typeorm`.
You can also choose to use `npx typeorm <params>` for each command if you prefer not having to install it.

### If entities files are in typescript​

This CLI tool is written in javascript and to be run on node. If your entity files are in typescript, you will need to transpile them to javascript before using CLI. You may skip this section if you only use javascript.

You may setup ts-node in your project to ease the operation as follows:

Install ts-node:

```
npm install ts-node --save-dev
```

Add typeorm command under scripts section in package.json

```
"scripts": {    ...    "typeorm": "typeorm-ts-node-commonjs"}
```

For ESM projects add this instead:

```
"scripts": {    ...    "typeorm": "typeorm-ts-node-esm"}
```

If you want to load more modules like [module-alias](https://github.com/ilearnio/module-alias) you can add more `--require my-module-supporting-register`

Then you may run the command like this:

```
npm run typeorm migration:run -- -d path-to-datasource-config
```

### How to read the documentation?​

To reduce verbosity of the documentation, the following sections are using a globally installed typeorm CLI. Depending on how you installed the CLI, you may replace `typeorm` at the start of the command, by either `npx typeorm` or `npm run typeorm`.

## Initialize a new TypeORM project​

You can create a new project with everything already setup:

```
typeorm init
```

It creates all files needed for a basic project with TypeORM:

- .gitignore
- package.json
- README.md
- tsconfig.json
- src/entity/User.ts
- src/index.ts

Then you can run `npm install` to install all dependencies.
After that, you can run your application by running `npm start`.

All files are generated in the current directory.
If you want to generate them in a special directory you can use `--name`:

```
typeorm init --name my-project
```

To specify a specific database you use you can use `--database`:

```
typeorm init --database mssql
```

To generate an ESM base project you can use `--module esm`:

```
typeorm init --name my-project --module esm
```

You can also generate a base project with Express:

```
typeorm init --name my-project --express
```

If you are using docker you can generate a `docker-compose.yml` file using:

```
typeorm init --docker
```

`typeorm init` is the easiest and fastest way to setup a TypeORM project.

## Create a new entity​

You can create a new entity using CLI:

```
typeorm entity:create path-to-entity-dir/entity
```

Learn more about [entities](https://typeorm.io/docs/entity/entities).

## Create a new subscriber​

You can create a new subscriber using CLI:

```
typeorm subscriber:create path-to-subscriber-dir/subscriber
```

Learn more about [Subscribers](https://typeorm.io/docs/advanced-topics/listeners-and-subscribers).

## Manage migrations​

- `typeorm migration:create` - [create](https://typeorm.io/docs/migrations/creating) empty migration
- `typeorm migration:generate` - [generate](https://typeorm.io/docs/migrations/generating) migration comparing entities with actual database schema
- `typeorm migration:run` - [execute](https://typeorm.io/docs/migrations/executing) all migrations
- `typeorm migration:revert` - [revert](https://typeorm.io/docs/migrations/reverting) last migration
- `typeorm migration:show` - [list](https://typeorm.io/docs/migrations/status) all migrations with their execution status

Learn more about [Migrations](https://typeorm.io/docs/migrations/why).

## Sync database schema​

To synchronize a database schema use:

```
typeorm schema:sync
```

Be careful running this command in production -
schema sync may cause data loss if you don't use it wisely.
Check which sql queries it will run before running on production.

## Log sync database schema queries without actual running them​

To check what sql queries `schema:sync` is going to run use:

```
typeorm schema:log
```

## Drop database schema​

To completely drop a database schema use:

```
typeorm schema:drop -- -d path-to-datasource-config
```

Be careful with this command on production since it completely removes data from your database.

## Run any SQL query​

You can execute any SQL query you want directly in the database using:

```
typeorm query "SELECT * FROM USERS"
```

## Clear cache​

If you are using `QueryBuilder` caching, sometimes you may want to clear everything stored in the cache.
You can do it using the following command:

```
typeorm cache:clear
```

## Check version​

You can check what typeorm version you have installed (both local and global) by running:

```
typeorm version
```

---

# DataSource API

> -   options - Options used to create this dataSource.

- `options` - Options used to create this dataSource.
  Learn more about [Data Source Options](https://typeorm.io/docs/data-source/data-source-options).

```
const dataSourceOptions: DataSourceOptions = dataSource.options
```

- `isInitialized` - Indicates if DataSource was initialized and initial connection / connection pool with database was established or not.

```
const isInitialized: boolean = dataSource.isInitialized
```

- `driver` - Underlying database driver used in this dataSource.

```
const driver: Driver = dataSource.driver
```

- `manager` - `EntityManager` used to work with entities.
  Learn more about [Entity Manager](https://typeorm.io/docs/working-with-entity-manager/working-with-entity-manager) and [Repository](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

```
const manager: EntityManager = dataSource.manager// you can call manager methods, for example find:const users = await manager.find()
```

- `mongoManager` - `MongoEntityManager` used to work with entities for mongodb data source.
  For more information about MongoEntityManager see [MongoDB](https://typeorm.io/docs/drivers/mongodb) documentation.

```
const manager: MongoEntityManager = dataSource.mongoManager// you can call manager or mongodb-manager specific methods, for example find:const users = await manager.find()
```

- `initialize` - Initializes data source and opens connection pool to the database.

```
await dataSource.initialize()
```

- `destroy` - Destroys the DataSource and closes all database connections.
  Usually, you call this method when your application is shutting down.

```
await dataSource.destroy()
```

- `synchronize` - Synchronizes database schema. When `synchronize: true` is set in data source options it calls this method.
  Usually, you call this method when your application is starting.

```
await dataSource.synchronize()
```

- `dropDatabase` - Drops the database and all its data.
  Be careful with this method on production since this method will erase all your database tables and their data.
  Can be used only after connection to the database is established.

```
await dataSource.dropDatabase()
```

- `runMigrations` - Runs all pending migrations.

```
await dataSource.runMigrations()
```

- `undoLastMigration` - Reverts last executed migration.

```
await dataSource.undoLastMigration()
```

- `hasMetadata` - Checks if metadata for a given entity is registered.

```
if (dataSource.hasMetadata(User))    const userMetadata = dataSource.getMetadata(User)
```

- `getMetadata` - Gets `EntityMetadata` of the given entity.
  You can also specify a table name and if entity metadata with such table name is found it will be returned.

```
const userMetadata = dataSource.getMetadata(User)// now you can get any information about User entity
```

- `getRepository` - Gets `Repository` of the given entity.
  You can also specify a table name and if repository for given table is found it will be returned.
  Learn more about [Repositories](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

```
const repository = dataSource.getRepository(User)// now you can call repository methods, for example find:const users = await repository.find()
```

- `getTreeRepository` - Gets `TreeRepository` of the given entity.
  You can also specify a table name and if repository for given table is found it will be returned.
  Learn more about [Repositories](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

```
const repository = dataSource.getTreeRepository(Category)// now you can call tree repository methods, for example findTrees:const categories = await repository.findTrees()
```

- `getMongoRepository` - Gets `MongoRepository` of the given entity.
  This repository is used for entities in MongoDB dataSource.
  Learn more about [MongoDB support](https://typeorm.io/docs/drivers/mongodb).

```
const repository = dataSource.getMongoRepository(User)// now you can call mongodb-specific repository methods, for example createEntityCursor:const categoryCursor = repository.createEntityCursor()const category1 = await categoryCursor.next()const category2 = await categoryCursor.next()
```

- `transaction` - Provides a single transaction where multiple database requests will be executed in a single database transaction.
  Learn more about [Transactions](https://typeorm.io/docs/advanced-topics/transactions).

```
await dataSource.transaction(async (manager) => {    // NOTE: you must perform all database operations using given manager instance    // its a special instance of EntityManager working with this transaction    // and don't forget to await things here})
```

- `query` - Executes a raw SQL query.

```
const rawData = await dataSource.query(`SELECT * FROM USERS`)// You can also use parameters to avoid SQL injection// The syntax differs between the drivers// aurora-mysql, better-sqlite3, capacitor, cordova,// expo, mariadb, mysql, nativescript, react-native,// sap, sqlite, sqljsconst rawData = await dataSource.query(    "SELECT * FROM USERS WHERE name = ? and age = ?",    ["John", 24],)// aurora-postgres, cockroachdb, postgresconst rawData = await dataSource.query(    "SELECT * FROM USERS WHERE name = $1 and age = $2",    ["John", 24],)// oracleconst rawData = await dataSource.query(    "SELECT * FROM USERS WHERE name = :1 and age = :2",    ["John", 24],)// spannerconst rawData = await dataSource.query(    "SELECT * FROM USERS WHERE name = @param0 and age = @param1",    ["John", 24],)// mssqlconst rawData = await dataSource.query(    "SELECT * FROM USERS WHERE name = @0 and age = @1",    ["John", 24],)
```

- `sql` - Executes a raw SQL query using template literals.

```
const rawData =    await dataSource.sql`SELECT * FROM USERS WHERE name = ${"John"} and age = ${24}`
```

Learn more about using the [SQL Tag syntax](https://typeorm.io/docs/guides/sql-tag).

- `createQueryBuilder` - Creates a query builder, which can be used to build queries.
  Learn more about [QueryBuilder](https://typeorm.io/docs/query-builder/select-query-builder).

```
const users = await dataSource    .createQueryBuilder()    .select()    .from(User, "user")    .where("user.name = :name", { name: "John" })    .getMany()
```

- `createQueryRunner` - Creates a query runner used to manage and work with a single real database dataSource.
  Learn more about [QueryRunner](https://typeorm.io/docs/query-runner).

```
const queryRunner = dataSource.createQueryRunner()// you can use its methods only after you call connect// which performs real database connectionawait queryRunner.connect()// .. now you can work with query runner and call its methods// very important - don't forget to release query runner once you finished working with itawait queryRunner.release()
```

---

# Data Source Options

> What is DataSourceOptions?

## What is DataSourceOptions?​

`DataSourceOptions` is a data source configuration you pass when you create a new `DataSource` instance.
Different RDBMS-es have their own specific options.

## Common data source options​

- `type` - RDBMS type. You must specify what database engine you use.
  Possible values are:
  "mysql", "postgres", "cockroachdb", "sap", "spanner", "mariadb", "sqlite", "cordova", "react-native", "nativescript", "sqljs", "oracle", "mssql", "mongodb", "aurora-mysql", "aurora-postgres", "expo", "better-sqlite3", "capacitor".
  This option is **required**.
- `extra` - Extra options to be passed to the underlying driver.
  Use it if you want to pass extra settings to the underlying database driver.
- `entities` - Entities, or Entity Schemas, to be loaded and used for this data source.
  It accepts entity classes, entity schema classes, and directory paths from which to load.
  Directories support glob patterns.
  Example: `entities: [Post, Category, "entity/*.js", "modules/**/entity/*.js"]`.
  Learn more about [Entities](https://typeorm.io/docs/entity/entities).
  Learn more about [Entity Schemas](https://typeorm.io/docs/entity/separating-entity-definition).
- `subscribers` - Subscribers to be loaded and used for this data source.
  It accepts both entity classes and directories from which to load.
  Directories support glob patterns.
  Example: `subscribers: [PostSubscriber, AppSubscriber, "subscriber/*.js", "modules/**/subscriber/*.js"]`.
  Learn more about [Subscribers](https://typeorm.io/docs/advanced-topics/listeners-and-subscribers).
- `logging` - Indicates if logging is enabled or not.
  If set to `true` then query and error logging will be enabled.
  You can also specify different types of logging to be enabled, for example `["query", "error", "schema"]`.
  Learn more about [Logging](https://typeorm.io/docs/advanced-topics/logging).
- `logger` - Logger to be used for logging purposes. Possible values are "advanced-console", "formatted-console", "simple-console" and "file".
  Default is "advanced-console". You can also specify a logger class that implements `Logger` interface.
  Learn more about [Logging](https://typeorm.io/docs/advanced-topics/logging).
- `maxQueryExecutionTime` - If query execution time exceed this given max execution time (in milliseconds)
  then logger will log this query.
- `poolSize` - Configure maximum number of active connections is the pool.
- `namingStrategy` - Naming strategy to be used to name tables and columns in the database.
- `entityPrefix` - Prefixes with the given string all tables (or collections) on this data source.
- `entitySkipConstructor` - Indicates if TypeORM should skip constructors when deserializing entities
  from the database. Note that when you do not call the constructor both private properties and default
  properties will not operate as expected.
- `dropSchema` - Drops the schema each time data source is being initialized.
  Be careful with this option and don't use this in production - otherwise you'll lose all production data.
  This option is useful during debug and development.
- `synchronize` - Indicates if database schema should be auto created on every application launch.
  Be careful with this option and don't use this in production - otherwise you can lose production data.
  This option is useful during debug and development.
  As an alternative to it, you can use CLI and run schema :sync  command.
  Note that for MongoDB database it does not create schema, because MongoDB is schemaless.
  Instead, it syncs just by creating indices.
- `migrations` - [Migrations](https://typeorm.io/docs/migrations/why) to be loaded and used for this data source
- `migrationsRun` - Indicates if [migrations](https://typeorm.io/docs/migrations/why) should be auto-run on every application launch.
- `migrationsTableName` - Name of the table in the database which is going to contain information about executed [migrations](https://typeorm.io/docs/migrations/why).
- `migrationsTransactionMode` - Controls transaction mode when running [migrations](https://typeorm.io/docs/migrations/why).
- `metadataTableName` - Name of the table in the database which is going to contain information about table metadata.
  By default, this table is called "typeorm_metadata".
- `cache` - Enables entity result caching. You can also configure cache type and other cache options here.
  Read more about caching [here](https://typeorm.io/docs/query-builder/caching).
- `isolateWhereStatements` - Enables where statement isolation, wrapping each where clause in brackets automatically.
  eg. `.where("user.firstName = :search OR user.lastName = :search")` becomes `WHERE (user.firstName = ? OR user.lastName = ?)` instead of `WHERE user.firstName = ? OR user.lastName = ?`
- `invalidWhereValuesBehavior` - Controls how null and undefined values are handled in where conditions across all TypeORM operations (find operations, query builders, repository methods).
  - `null` behavior options:
    - `'ignore'` (default) - skips null properties
    - `'sql-null'` - transforms null to SQL NULL
    - `'throw'` - throws an error
  - `undefined` behavior options:
    - `'ignore'` (default) - skips undefined properties
    - `'throw'` - throws an error
  Example: `invalidWhereValuesBehavior: { null: 'sql-null', undefined: 'throw' }`.
  Learn more about [Null and Undefined Handling](https://typeorm.io/docs/data-source/null-and-undefined-handling).

## Data Source Options example​

Here is a small example of data source options for mysql:

```
{    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    logging: true,    synchronize: true,    entities: [        "entity/*.js"    ],    subscribers: [        "subscriber/*.js"    ],    entitySchemas: [        "schema/*.json"    ],    migrations: [        "migration/*.js"    ]}
```
