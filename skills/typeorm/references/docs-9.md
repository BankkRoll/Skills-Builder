# Select using Query Builder and more

# Select using Query Builder

> What is a QueryBuilder?

## What is a QueryBuilder?​

`QueryBuilder` is one of the most powerful features of TypeORM -
it allows you to build SQL queries using elegant and convenient syntax,
execute them and get automatically transformed entities.

Simple example of `QueryBuilder`:

```
const firstUser = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id", { id: 1 })    .getOne()
```

It builds the following SQL query:

```
SELECT    user.id as userId,    user.firstName as userFirstName,    user.lastName as userLastNameFROM users userWHERE user.id = 1
```

and returns you an instance of `User`:

```
User {    id: 1,    firstName: "Timber",    lastName: "Saw"}
```

## Important note when using theQueryBuilder​

When using the `QueryBuilder`, you need to provide unique parameters in your `WHERE` expressions. **This will not work**:

```
const result = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.linkedSheep", "linkedSheep")    .leftJoinAndSelect("user.linkedCow", "linkedCow")    .where("user.linkedSheep = :id", { id: sheepId })    .andWhere("user.linkedCow = :id", { id: cowId })
```

... but this will:

```
const result = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.linkedSheep", "linkedSheep")    .leftJoinAndSelect("user.linkedCow", "linkedCow")    .where("user.linkedSheep = :sheepId", { sheepId })    .andWhere("user.linkedCow = :cowId", { cowId })
```

Note that we uniquely named `:sheepId` and `:cowId` instead of using `:id` twice for different parameters.

## How to create and use a QueryBuilder?​

There are several ways how you can create a `Query Builder`:

- Using DataSource:
  ```
  const user = await dataSource    .createQueryBuilder()    .select("user")    .from(User, "user")    .where("user.id = :id", { id: 1 })    .getOne()
  ```
- Using entity manager:
  ```
  const user = await dataSource.manager    .createQueryBuilder(User, "user")    .where("user.id = :id", { id: 1 })    .getOne()
  ```
- Using repository:
  ```
  const user = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id", { id: 1 })    .getOne()
  ```

There are 5 different `QueryBuilder` types available:

- `SelectQueryBuilder` - used to build and execute `SELECT` queries. Example:
  ```
  const user = await dataSource    .createQueryBuilder()    .select("user")    .from(User, "user")    .where("user.id = :id", { id: 1 })    .getOne()
  ```
- `InsertQueryBuilder` - used to build and execute `INSERT` queries. Example:
  ```
  await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values([        { firstName: "Timber", lastName: "Saw" },        { firstName: "Phantom", lastName: "Lancer" },    ])    .execute()
  ```
- `UpdateQueryBuilder` - used to build and execute `UPDATE` queries. Example:
  ```
  await dataSource    .createQueryBuilder()    .update(User)    .set({ firstName: "Timber", lastName: "Saw" })    .where("id = :id", { id: 1 })    .execute()
  ```
- `DeleteQueryBuilder` - used to build and execute `DELETE` queries. Example:
  ```
  await dataSource    .createQueryBuilder()    .delete()    .from(User)    .where("id = :id", { id: 1 })    .execute()
  ```
- `RelationQueryBuilder` - used to build and execute relation-specific operations [TBD].
  Example:
  ```
  await dataSource    .createQueryBuilder()    .relation(User, "photos")    .of(id)    .loadMany()
  ```

You can switch between different types of query builder within any of them,
once you do, you will get a new instance of query builder (unlike all other methods).

## Getting values usingQueryBuilder​

To get a single result from the database,
for example to get a user by id or name, you must use `getOne`:

```
const timber = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id OR user.name = :name", { id: 1, name: "Timber" })    .getOne()
```

`getOneOrFail` will get a single result from the database, but if
no result exists it will throw an `EntityNotFoundError`:

```
const timber = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id OR user.name = :name", { id: 1, name: "Timber" })    .getOneOrFail()
```

To get multiple results from the database,
for example, to get all users from the database, use `getMany`:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .getMany()
```

There are two types of results you can get using select query builder: **entities** or **raw results**.
Most of the time, you need to select real entities from your database, for example, users.
For this purpose, you use `getOne` and `getMany`.
But sometimes you need to select some specific data, let's say the *sum of all user photos*.
This data is not an entity, it's called raw data.
To get raw data, you use `getRawOne` and `getRawMany`.
Examples:

```
const { sum } = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("SUM(user.photosCount)", "sum")    .where("user.id = :id", { id: 1 })    .getRawOne()
```

```
const photosSums = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("user.id")    .addSelect("SUM(user.photosCount)", "sum")    .groupBy("user.id")    .getRawMany()// result will be like this: [{ id: 1, sum: 25 }, { id: 2, sum: 13 }, ...]
```

## Getting a count​

You can get the count on the number of rows a query will return by using `getCount()`. This will return the count as a number rather than an Entity result.

```
const count = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.name = :name", { name: "Timber" })    .getCount()
```

Which produces the following SQL query:

```
SELECT count(*) FROM users user WHERE user.name = 'Timber'
```

## What are aliases for?​

We used `createQueryBuilder("user")`. But what is "user"?
It's just a regular SQL alias.
We use aliases everywhere, except when we work with selected data.

`createQueryBuilder("user")` is equivalent to:

```
createQueryBuilder().select("user").from(User, "user")
```

Which will result in the following SQL query:

```
SELECT ... FROM users user
```

In this SQL query, `users` is the table name, and `user` is an alias we assign to this table.
Later we use this alias to access the table:

```
createQueryBuilder()    .select("user")    .from(User, "user")    .where("user.name = :name", { name: "Timber" })
```

Which produces the following SQL query:

```
SELECT ... FROM users user WHERE user.name = 'Timber'
```

See, we used the users table by using the `user` alias we assigned when we created a query builder.

One query builder is not limited to one alias, they can have multiple aliases.
Each select can have its own alias,
you can select from multiple tables each with its own alias,
you can join multiple tables each with its own alias.
You can use those aliases to access tables you are selecting (or data you are selecting).

## Using parameters to escape data​

We used `where("user.name = :name", { name: "Timber" })`.
What does `{ name: "Timber" }` stand for? It's a parameter we used to prevent SQL injection.
We could have written: `where("user.name = '" + name + "')`,
however this is not safe, as it opens the code to SQL injections.
The safe way is to use this special syntax: `where("user.name = :name", { name: "Timber" })`,
where `:name` is a parameter name and the value is specified in an object: `{ name: "Timber" }`.

```
.where("user.name = :name", { name: "Timber" })
```

is a shortcut for:

```
.where("user.name = :name").setParameter("name", "Timber")
```

Note: do not use the same parameter name for different values across the query builder. Values will be overridden if you set them multiple times.

You can also supply an array of values, and have them transformed into a list of values in the SQL
statement, by using the special expansion syntax:

```
.where("user.name IN (:...names)", { names: [ "Timber", "Crystal", "Lina" ] })
```

Which becomes:

```
WHERE user.name IN ('Timber', 'Crystal', 'Lina')
```

## AddingWHEREexpression​

Adding a `WHERE` expression is as easy as:

```
createQueryBuilder("user").where("user.name = :name", { name: "Timber" })
```

Which will produce:

```
SELECT ... FROM users user WHERE user.name = 'Timber'
```

You can add `AND` into an existing `WHERE` expression:

```
createQueryBuilder("user")    .where("user.firstName = :firstName", { firstName: "Timber" })    .andWhere("user.lastName = :lastName", { lastName: "Saw" })
```

Which will produce the following SQL query:

```
SELECT ... FROM users user WHERE user.firstName = 'Timber' AND user.lastName = 'Saw'
```

You can add `OR` into an existing `WHERE` expression:

```
createQueryBuilder("user")    .where("user.firstName = :firstName", { firstName: "Timber" })    .orWhere("user.lastName = :lastName", { lastName: "Saw" })
```

Which will produce the following SQL query:

```
SELECT ... FROM users user WHERE user.firstName = 'Timber' OR user.lastName = 'Saw'
```

You can do an `IN` query with the `WHERE` expression:

```
createQueryBuilder("user").where("user.id IN (:...ids)", { ids: [1, 2, 3, 4] })
```

Which will produce the following SQL query:

```
SELECT ... FROM users user WHERE user.id IN (1, 2, 3, 4)
```

You can add a complex `WHERE` expression into an existing `WHERE` using `Brackets`

```
createQueryBuilder("user")    .where("user.registered = :registered", { registered: true })    .andWhere(        new Brackets((qb) => {            qb.where("user.firstName = :firstName", {                firstName: "Timber",            }).orWhere("user.lastName = :lastName", { lastName: "Saw" })        }),    )
```

Which will produce the following SQL query:

```
SELECT ... FROM users user WHERE user.registered = true AND (user.firstName = 'Timber' OR user.lastName = 'Saw')
```

You can add a negated complex `WHERE` expression into an existing `WHERE` using `NotBrackets`

```
createQueryBuilder("user")    .where("user.registered = :registered", { registered: true })    .andWhere(        new NotBrackets((qb) => {            qb.where("user.firstName = :firstName", {                firstName: "Timber",            }).orWhere("user.lastName = :lastName", { lastName: "Saw" })        }),    )
```

Which will produce the following SQL query:

```
SELECT ... FROM users user WHERE user.registered = true AND NOT((user.firstName = 'Timber' OR user.lastName = 'Saw'))
```

You can combine as many `AND` and `OR` expressions as you need.
If you use `.where` more than once you'll override all previous `WHERE` expressions.

Note: be careful with `orWhere` - if you use complex expressions with both `AND` and `OR` expressions,
keep in mind that they are stacked without any pretences.
Sometimes you'll need to create a where string instead, and avoid using `orWhere`.

## AddingHAVINGexpression​

Adding a `HAVING` expression is easy as:

```
createQueryBuilder("user").having("user.name = :name", { name: "Timber" })
```

Which will produce following SQL query:

```
SELECT ... FROM users user HAVING user.name = 'Timber'
```

You can add `AND` into an exist `HAVING` expression:

```
createQueryBuilder("user")    .having("user.firstName = :firstName", { firstName: "Timber" })    .andHaving("user.lastName = :lastName", { lastName: "Saw" })
```

Which will produce the following SQL query:

```
SELECT ... FROM users user HAVING user.firstName = 'Timber' AND user.lastName = 'Saw'
```

You can add `OR` into a exist `HAVING` expression:

```
createQueryBuilder("user")    .having("user.firstName = :firstName", { firstName: "Timber" })    .orHaving("user.lastName = :lastName", { lastName: "Saw" })
```

Which will produce the following SQL query:

```
SELECT ... FROM users user HAVING user.firstName = 'Timber' OR user.lastName = 'Saw'
```

You can combine as many `AND` and `OR` expressions as you need.
If you use `.having` more than once you'll override all previous `HAVING` expressions.

## AddingORDER BYexpression​

Adding an `ORDER BY` expression is easy as:

```
createQueryBuilder("user").orderBy("user.id")
```

Which will produce:

```
SELECT ... FROM users user ORDER BY user.id
```

You can change the ordering direction from ascending to descending (or versa):

```
createQueryBuilder("user").orderBy("user.id", "DESC")createQueryBuilder("user").orderBy("user.id", "ASC")
```

You can add multiple order-by criteria:

```
createQueryBuilder("user").orderBy("user.name").addOrderBy("user.id")
```

You can also use a map of order-by fields:

```
createQueryBuilder("user").orderBy({    "user.name": "ASC",    "user.id": "DESC",})
```

If you use `.orderBy` more than once you'll override all previous `ORDER BY` expressions.

## AddingDISTINCT ONexpression (Postgres only)​

When using both distinct-on with an order-by expression, the distinct-on expression must match the leftmost order-by.
The distinct-on expressions are interpreted using the same rules as order-by. Please note that, using distinct-on without an order-by expression means that the first row of each set is unpredictable.

Adding a `DISTINCT ON` expression is easy as:

```
createQueryBuilder("user").distinctOn(["user.id"]).orderBy("user.id")
```

Which will produce:

```
SELECT DISTINCT ON (user.id) ... FROM users user ORDER BY user.id
```

## AddingGROUP BYexpression​

Adding a `GROUP BY` expression is easy as:

```
createQueryBuilder("user").groupBy("user.id")
```

Which will produce the following SQL query:

```
SELECT ... FROM users user GROUP BY user.id
```

To add more group-by criteria use `addGroupBy`:

```
createQueryBuilder("user").groupBy("user.name").addGroupBy("user.id")
```

If you use `.groupBy` more than once you'll override all previous `GROUP BY` expressions.

## AddingLIMITexpression​

Adding a `LIMIT` expression is easy as:

```
createQueryBuilder("user").limit(10)
```

Which will produce the following SQL query:

```
SELECT ... FROM users user LIMIT 10
```

The resulting SQL query depends on the type of database (SQL, mySQL, Postgres, etc).
Note: LIMIT may not work as you may expect if you are using complex queries with joins or subqueries.
If you are using pagination, it's recommended to use `take` instead.

## AddingOFFSETexpression​

Adding an SQL `OFFSET` expression is easy as:

```
createQueryBuilder("user").offset(10)
```

Which will produce the following SQL query:

```
SELECT ... FROM users user OFFSET 10
```

The resulting SQL query depends on the type of database (SQL, mySQL, Postgres, etc).
Note: OFFSET may not work as you may expect if you are using complex queries with joins or subqueries.
If you are using pagination, it's recommended to use `skip` instead.

## Joining relations​

Let's say you have the following entities:

```
import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from "typeorm"import { Photo } from "./Photo"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToMany((type) => Photo, (photo) => photo.user)    photos: Photo[]}
```

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from "typeorm"import { User } from "./User"@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    url: string    @ManyToOne((type) => User, (user) => user.photos)    user: User}
```

Now let's say you want to load user "Timber" with all of his photos:

```
const user = await createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .where("user.name = :name", { name: "Timber" })    .getOne()
```

You'll get the following result:

```
{    id: 1,    name: "Timber",    photos: [{        id: 1,        url: "me-with-chakram.jpg"    }, {        id: 2,        url: "me-with-trees.jpg"    }]}
```

As you can see `leftJoinAndSelect` automatically loaded all of Timber's photos.
The first argument is the relation you want to load and the second argument is an alias you assign to this relation's table.
You can use this alias anywhere in query builder.
For example, let's take all Timber's photos which aren't removed.

```
const user = await createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .where("user.name = :name", { name: "Timber" })    .andWhere("photo.isRemoved = :isRemoved", { isRemoved: false })    .getOne()
```

This will generate following SQL query:

```
SELECT user.*, photo.* FROM users user    LEFT JOIN photos photo ON photo.user = user.id    WHERE user.name = 'Timber' AND photo.isRemoved = FALSE
```

You can also add conditions to the join expression instead of using "where":

```
const user = await createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo", "photo.isRemoved = :isRemoved", {        isRemoved: false,    })    .where("user.name = :name", { name: "Timber" })    .getOne()
```

This will generate the following SQL query:

```
SELECT user.*, photo.* FROM users user    LEFT JOIN photos photo ON photo.user = user.id AND photo.isRemoved = FALSE    WHERE user.name = 'Timber'
```

## Inner and left joins​

If you want to use `INNER JOIN` instead of `LEFT JOIN` just use `innerJoinAndSelect` instead:

```
const user = await createQueryBuilder("user")    .innerJoinAndSelect(        "user.photos",        "photo",        "photo.isRemoved = :isRemoved",        { isRemoved: false },    )    .where("user.name = :name", { name: "Timber" })    .getOne()
```

This will generate:

```
SELECT user.*, photo.* FROM users user    INNER JOIN photos photo ON photo.user = user.id AND photo.isRemoved = FALSE    WHERE user.name = 'Timber'
```

The difference between `LEFT JOIN` and `INNER JOIN` is that `INNER JOIN` won't return a user if it does not have any photos.
`LEFT JOIN` will return you the user even if it doesn't have photos.
To learn more about different join types, refer to the [SQL documentation](https://msdn.microsoft.com/en-us/library/zt8wzxy4.aspx).

## Join without selection​

You can join data without its selection.
To do that, use `leftJoin` or `innerJoin`:

```
const user = await createQueryBuilder("user")    .innerJoin("user.photos", "photo")    .where("user.name = :name", { name: "Timber" })    .getOne()
```

This will generate:

```
SELECT user.* FROM users user    INNER JOIN photos photo ON photo.user = user.id    WHERE user.name = 'Timber'
```

This will select Timber if he has photos, but won't return his photos.

## Joining any entity or table​

You can join not only relations, but also other unrelated entities or tables.
Examples:

```
const user = await createQueryBuilder("user")    .leftJoinAndSelect(Photo, "photo", "photo.userId = user.id")    .getMany()
```

```
const user = await createQueryBuilder("user")    .leftJoinAndSelect("photos", "photo", "photo.userId = user.id")    .getMany()
```

## Joining and mapping functionality​

Add `profilePhoto` to `User` entity, and you can map any data into that property using `QueryBuilder`:

```
export class User {    /// ...    profilePhoto: Photo}
```

```
const user = await createQueryBuilder("user")    .leftJoinAndMapOne(        "user.profilePhoto",        "user.photos",        "photo",        "photo.isForProfile = TRUE",    )    .where("user.name = :name", { name: "Timber" })    .getOne()
```

This will load Timber's profile photo and set it to `user.profilePhoto`.
If you want to load and map a single entity use `leftJoinAndMapOne`.
If you want to load and map multiple entities use `leftJoinAndMapMany`.

## Getting the generated query​

Sometimes you may want to get the SQL query generated by `QueryBuilder`.
To do so, use `getSql`:

```
const sql = createQueryBuilder("user")    .where("user.firstName = :firstName", { firstName: "Timber" })    .orWhere("user.lastName = :lastName", { lastName: "Saw" })    .getSql()
```

For debugging purposes you can use `printSql`:

```
const users = await createQueryBuilder("user")    .where("user.firstName = :firstName", { firstName: "Timber" })    .orWhere("user.lastName = :lastName", { lastName: "Saw" })    .printSql()    .getMany()
```

This query will return users and print the used sql statement to the console.

## Getting raw results​

There are two types of results you can get using select query builder: **entities** and **raw results**.
Most of the time, you need to select real entities from your database, for example, users.
For this purpose, you use `getOne` and `getMany`.
However, sometimes you need to select specific data, like the *sum of all user photos*.
Such data is not an entity, it's called raw data.
To get raw data, you use `getRawOne` and `getRawMany`.
Examples:

```
const { sum } = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("SUM(user.photosCount)", "sum")    .where("user.id = :id", { id: 1 })    .getRawOne()
```

```
const photosSums = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("user.id")    .addSelect("SUM(user.photosCount)", "sum")    .groupBy("user.id")    .getRawMany()// result will be like this: [{ id: 1, sum: 25 }, { id: 2, sum: 13 }, ...]
```

## Streaming result data​

You can use `stream` which returns you a stream.
Streaming returns you raw data, and you must handle entity transformation manually:

```
const stream = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id", { id: 1 })    .stream()
```

## Using pagination​

Most of the time when you develop an application, you need pagination functionality.
This is used if you have pagination, page slider, or infinite scroll components in your application.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .take(10)    .getMany()
```

This will give you the first 10 users with their photos.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .skip(10)    .getMany()
```

This will give you all except the first 10 users with their photos.
You can combine those methods:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .skip(5)    .take(10)    .getMany()
```

This will skip the first 5 users and take 10 users after them.

`take` and `skip` may look like we are using `limit` and `offset`, but they aren't.
`limit` and `offset` may not work as you expect once you have more complicated queries with joins or subqueries.
Using `take` and `skip` will prevent those issues.

## Set locking​

QueryBuilder supports both optimistic and pessimistic locking.

### Lock modes​

Support of lock modes, and SQL statements they translate to, are listed in the table below (blank cell denotes unsupported). When specified lock mode is not supported, a `LockNotSupportedOnGivenDriverError` error will be thrown.

```
|                 | pessimistic_read                  | pessimistic_write       | dirty_read    | pessimistic_partial_write (Deprecated, use onLocked instead)   | pessimistic_write_or_fail (Deprecated, use onLocked instead)   | for_no_key_update   | for_key_share || --------------- | --------------------------------- | ----------------------- | ------------- | -------------------------------------------------------------- | -------------------------------------------------------------- | ------------------- | ------------- || MySQL           | FOR SHARE (8+)/LOCK IN SHARE MODE | FOR UPDATE              | (nothing)     | FOR UPDATE SKIP LOCKED                                         | FOR UPDATE NOWAIT                                              |                     |               || Postgres        | FOR SHARE                         | FOR UPDATE              | (nothing)     | FOR UPDATE SKIP LOCKED                                         | FOR UPDATE NOWAIT                                              | FOR NO KEY UPDATE   | FOR KEY SHARE || Oracle          | FOR UPDATE                        | FOR UPDATE              | (nothing)     |                                                                |                                                                |                     |               || SQL Server      | WITH (HOLDLOCK, ROWLOCK)          | WITH (UPDLOCK, ROWLOCK) | WITH (NOLOCK) |                                                                |                                                                |                     |               || AuroraDataApi   | LOCK IN SHARE MODE                | FOR UPDATE              | (nothing)     |                                                                |                                                                |                     |               || CockroachDB     |                                   | FOR UPDATE              | (nothing)     |                                                                | FOR UPDATE NOWAIT                                              | FOR NO KEY UPDATE   |               |
```

To use pessimistic read locking use the following method:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("pessimistic_read")    .getMany()
```

To use pessimistic write locking use the following method:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("pessimistic_write")    .getMany()
```

To use dirty read locking use the following method:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("dirty_read")    .getMany()
```

To use optimistic locking use the following method:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("optimistic", existUser.version)    .getMany()
```

Optimistic locking works in conjunction with both `@Version` and `@UpdatedDate` decorators.

### Lock tables​

You can also lock tables using the following method:

```
const users = await dataSource    .getRepository(Post)    .createQueryBuilder("post")    .leftJoin("post.author", "user")    .setLock("pessimistic_write", undefined, ["post"])    .getMany()
```

If the Lock Tables argument is provided, only the table that is locked in the FOR UPDATE OF clause is specified.

### setOnLocked​

Allows you to control what happens when a row is locked. By default, the database will wait for the lock.
You can control that behavior by using `setOnLocked`

To not wait:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("pessimistic_write")    .setOnLocked("nowait")    .getMany()
```

To skip the row:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .setLock("pessimistic_write")    .setOnLocked("skip_locked")    .getMany()
```

Database support for `setOnLocked` based on [lock mode](#lock-modes):

- Postgres: `pessimistic_read`, `pessimistic_write`, `for_no_key_update`, `for_key_share`
- MySQL 8+: `pessimistic_read`, `pessimistic_write`
- MySQL < 8, Maria DB: `pessimistic_write`
- Cockroach: `pessimistic_write` (`nowait` only)

## Use custom index​

You can provide a certain index for database server to use in some cases. This feature is only supported in MySQL.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .useIndex("my_index") // name of index    .getMany()
```

## Max execution time​

We can drop slow query to avoid crashing the server.

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .maxExecutionTime(1000) // milliseconds.    .getMany()
```

## Partial selection​

If you want to select only some entity properties, you can use the following syntax:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select(["user.id", "user.name"])    .getMany()
```

This will only select the `id` and `name` of `User`.

## Using subqueries​

You can easily create subqueries. Subqueries are supported in `FROM`, `WHERE` and `JOIN` expressions.
Example:

```
const qb = await dataSource.getRepository(Post).createQueryBuilder("post")const posts = qb    .where(        "post.title IN " +            qb                .subQuery()                .select("user.name")                .from(User, "user")                .where("user.registered = :registered")                .getQuery(),    )    .setParameter("registered", true)    .getMany()
```

A more elegant way to do the same:

```
const posts = await dataSource    .getRepository(Post)    .createQueryBuilder("post")    .where((qb) => {        const subQuery = qb            .subQuery()            .select("user.name")            .from(User, "user")            .where("user.registered = :registered")            .getQuery()        return "post.title IN " + subQuery    })    .setParameter("registered", true)    .getMany()
```

Alternatively, you can create a separate query builder and use its generated SQL:

```
const userQb = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("user.name")    .where("user.registered = :registered", { registered: true })const posts = await dataSource    .getRepository(Post)    .createQueryBuilder("post")    .where("post.title IN (" + userQb.getQuery() + ")")    .setParameters(userQb.getParameters())    .getMany()
```

You can create subqueries in `FROM` like this:

```
const userQb = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .select("user.name", "name")    .where("user.registered = :registered", { registered: true })const posts = await dataSource    .createQueryBuilder()    .select("user.name", "name")    .from("(" + userQb.getQuery() + ")", "user")    .setParameters(userQb.getParameters())    .getRawMany()
```

or using a more elegant syntax:

```
const posts = await dataSource    .createQueryBuilder()    .select("user.name", "name")    .from((subQuery) => {        return subQuery            .select("user.name", "name")            .from(User, "user")            .where("user.registered = :registered", { registered: true })    }, "user")    .getRawMany()
```

If you want to add a subselect as a "second from" use `addFrom`.

You can use subselects in `SELECT` statements as well:

```
const posts = await dataSource    .createQueryBuilder()    .select("post.id", "id")    .addSelect((subQuery) => {        return subQuery.select("user.name", "name").from(User, "user").limit(1)    }, "name")    .from(Post, "post")    .getRawMany()
```

## Hidden Columns​

If the model you are querying has a column with a `select: false` column, you must use the `addSelect` function in order to retrieve the information from the column.

Let's say you have the following entity:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column({ select: false })    password: string}
```

Using a standard `find` or query, you will not receive the `password` property for the model. However, if you do the following:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder()    .select("user.id", "id")    .addSelect("user.password")    .getMany()
```

You will get the property `password` in your query.

## Querying Deleted rows​

If the model you are querying has a column with the attribute `@DeleteDateColumn` set, the query builder will automatically query rows which are 'soft deleted'.

Let's say you have the following entity:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    DeleteDateColumn,} from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @DeleteDateColumn()    deletedAt?: Date}
```

Using a standard `find` or query, you will not receive the rows which have a value in that column. However, if you do the following:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder()    .select("user.id", "id")    .withDeleted()    .getMany()
```

You will get all the rows, including the ones which are deleted.

## Common table expressions​

`QueryBuilder` instances
support [common table expressions](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL#Common_table_expression)
, if minimal supported version of your database supports them. Common table expressions aren't supported for Oracle yet.

```
const users = await connection    .getRepository(User)    .createQueryBuilder("user")    .select("user.id", "id")    .addCommonTableExpression(        `      SELECT "userId" FROM "post"    `,        "post_users_ids",    )    .where(`user.id IN (SELECT "userId" FROM 'post_users_ids')`)    .getMany()
```

Result values of `InsertQueryBuilder` or `UpdateQueryBuilder` can be used in Postgres:

```
const insertQueryBuilder = connection    .getRepository(User)    .createQueryBuilder()    .insert({        name: "John Smith",    })    .returning(["id"])const users = await connection    .getRepository(User)    .createQueryBuilder("user")    .addCommonTableExpression(insertQueryBuilder, "insert_results")    .where(`user.id IN (SELECT "id" FROM 'insert_results')`)    .getMany()
```

## Time Travel Queries​

[Time Travel Queries](https://www.cockroachlabs.com/blog/time-travel-queries-select-witty_subtitle-the_future/)
currently supported only in `CockroachDB` database.

```
const repository = connection.getRepository(Account)// create a new accountconst account = new Account()account.name = "John Smith"account.balance = 100await repository.save(account)// imagine we update the account balance 1 hour after creationaccount.balance = 200await repository.save(account)// outputs { name: "John Smith", balance: "200" }console.log(account)// load account state on 1 hour backaccount = await repository    .createQueryBuilder("account")    .timeTravelQuery(`'-1h'`)    .getOneOrFail()// outputs { name: "John Smith", balance: "100" }console.log(account)
```

By default `timeTravelQuery()` uses `follower_read_timestamp()` function if no arguments passed.
For another supported timestamp arguments and additional information please refer to
[CockroachDB](https://www.cockroachlabs.com/docs/stable/as-of-system-time.html) docs.

## Debugging​

You can get the generated SQL from the query builder by calling `getQuery()` or `getQueryAndParameters()`.

If you just want the query you can use `getQuery()`

```
const sql = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id", { id: 1 })    .getQuery()
```

Which results in:

```
SELECT `user`.`id` as `userId`, `user`.`firstName` as `userFirstName`, `user`.`lastName` as `userLastName` FROM `users` `user` WHERE `user`.`id` = ?
```

Or if you want the query and the parameters you can get an array back using `getQueryAndParameters()`

```
const queryAndParams = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .where("user.id = :id", { id: 1 })    .getQueryAndParameters()
```

Which results in:

```
;[    "SELECT `user`.`id` as `userId`, `user`.`firstName` as `userFirstName`, `user`.`lastName` as `userLastName` FROM `users` `user` WHERE `user`.`id` = ?",    [1],]
```

---

# Update using Query Builder

> You can create UPDATE queries using QueryBuilder.

You can create `UPDATE` queries using `QueryBuilder`.
Examples:

```
await dataSource    .createQueryBuilder()    .update(User)    .set({ firstName: "Timber", lastName: "Saw" })    .where("id = :id", { id: 1 })    .execute()
```

This is the most efficient way in terms of performance to update entities in your database.

## Raw SQL support​

In some cases when you need to execute SQL queries you need to use function style value:

```
await dataSource    .createQueryBuilder()    .update(User)    .set({        firstName: "Timber",        lastName: "Saw",        age: () => "age + 1",    })    .where("id = :id", { id: 1 })    .execute()
```

> Warning: When using raw SQL, ensure that values are properly sanitized to prevent SQL injection.

---

# Query Runner

> What is a QueryRunner?

## What is a QueryRunner?​

Each new `QueryRunner` instance takes a single connection from the connection pool, if the RDBMS supports connection pooling.
For databases that do not support connection pools, it uses the same connection across the entire data source.

## Creating a newQueryRunnerinstance​

Use the `createQueryRunner` method to create a new `QueryRunner`:

```
const queryRunner = dataSource.createQueryRunner()
```

## UsingQueryRunner​

After you create a new instance of `QueryRunner`, use the `connect` method to get a connection from the connection pool:

```
const queryRunner = dataSource.createQueryRunner()await queryRunner.connect()
```

**Important**: Make sure to release it when it is no longer needed to make it available to the connection pool again:

```
await queryRunner.release()
```

After the connection is released, you cannot use the query runner's methods.

`QueryRunner` has a bunch of methods you can use, it also has its own `EntityManager` instance,
which you can use through `manager` property to run `EntityManager` methods on a particular database connection
used by `QueryRunner` instance:

```
const queryRunner = dataSource.createQueryRunner()// take a connection from the connection poolawait queryRunner.connect()// use this particular connection to execute queriesconst users = await queryRunner.manager.find(User)// remember to release the connection after you are done using itawait queryRunner.release()
```

---

# Eager and Lazy Relations

> Eager relations

## Eager relations​

Eager relations are loaded automatically each time you load entities from the database.
For example:

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm"import { Question } from "./Question"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @ManyToMany((type) => Question, (question) => question.categories)    questions: Question[]}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany((type) => Category, (category) => category.questions, {        eager: true,    })    @JoinTable()    categories: Category[]}
```

Now when you load questions you don't need to join or specify relations you want to load.
They will be loaded automatically:

```
const questionRepository = dataSource.getRepository(Question)// questions will be loaded with its categoriesconst questions = await questionRepository.find()
```

Eager relations only work when you use `find*` methods.
If you use `QueryBuilder` eager relations are disabled and have to use `leftJoinAndSelect` to load the relation.
Eager relations can only be used on one side of the relationship,
using `eager: true` on both sides of relationship is disallowed.

## Lazy relations​

Entities in lazy relations are loaded once you access them.
Such relations must have `Promise` as type - you store your value in a promise,
and when you load them a promise is returned as well. Example:

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm"import { Question } from "./Question"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @ManyToMany((type) => Question, (question) => question.categories)    questions: Promise<Question[]>}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany((type) => Category, (category) => category.questions)    @JoinTable()    categories: Promise<Category[]>}
```

`categories` is a Promise. It means it is lazy and it can store only a promise with a value inside.
Example how to save such relation:

```
const category1 = new Category()category1.name = "animals"await dataSource.manager.save(category1)const category2 = new Category()category2.name = "zoo"await dataSource.manager.save(category2)const question = new Question()question.categories = Promise.resolve([category1, category2])await dataSource.manager.save(question)
```

Example how to load objects inside lazy relations:

```
const [question] = await dataSource.getRepository(Question).find()const categories = await question.categories// you'll have all question's categories inside "categories" variable now
```

Note: if you come from other languages (Java, PHP, etc.) and are used to using lazy relations everywhere - be careful.
Those languages aren't asynchronous, and lazy loading is achieved in a different way, without the use of promises.
In JavaScript and Node.JS, you have to use promises if you want to have lazy-loaded relations.
This is a non-standard technique and considered experimental in TypeORM.

---

# Many

> What are many-to-many relations?

## What are many-to-many relations?​

Many-to-many is a relation where A contains multiple instances of B, and B contains multiple instances of A.
Let's take for example `Question` and `Category` entities.
A question can have multiple categories, and each category can have multiple questions.

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany(() => Category)    @JoinTable()    categories: Category[]}
```

`@JoinTable()` is required for `@ManyToMany` relations.
You must put `@JoinTable` on one (owning) side of relation.

This example will produce following tables:

```
+-------------+--------------+----------------------------+|                        category                         |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(255) |                            |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|                        question                         |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || title       | varchar(255) |                            || text        | varchar(255) |                            |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|              question_categories_category               |+-------------+--------------+----------------------------+| questionId  | int          | PRIMARY KEY FOREIGN KEY    || categoryId  | int          | PRIMARY KEY FOREIGN KEY    |+-------------+--------------+----------------------------+
```

## Saving many-to-many relations​

With [cascades](https://typeorm.io/docs/relations/relations#cascades) enabled, you can save this relation with only one `save` call.

```
const category1 = new Category()category1.name = "animals"await dataSource.manager.save(category1)const category2 = new Category()category2.name = "zoo"await dataSource.manager.save(category2)const question = new Question()question.title = "dogs"question.text = "who let the dogs out?"question.categories = [category1, category2]await dataSource.manager.save(question)
```

## Deleting many-to-many relations​

With [cascades](https://typeorm.io/docs/relations/relations#cascades) enabled, you can delete this relation with only one `save` call.

To delete a many-to-many relationship between two records, remove it from the corresponding field and save the record.

```
const question = await dataSource.getRepository(Question).findOne({    relations: {        categories: true,    },    where: { id: 1 },})question.categories = question.categories.filter((category) => {    return category.id !== categoryToRemove.id})await dataSource.manager.save(question)
```

This will only remove the record in the join table. The `question` and `categoryToRemove` records will still exist.

## Soft Deleting a relationship with cascade​

This example shows how the cascading soft delete behaves:

```
const category1 = new Category()category1.name = "animals"const category2 = new Category()category2.name = "zoo"const question = new Question()question.categories = [category1, category2]const newQuestion = await dataSource.manager.save(question)await dataSource.manager.softRemove(newQuestion)
```

In this example we did not call save or softRemove for category1 and category2, but they will be automatically saved and soft-deleted when the cascade of relation options is set to true like this:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @ManyToMany(() => Category, (category) => category.questions, {        cascade: true,    })    @JoinTable()    categories: Category[]}
```

## Loading many-to-many relations​

To load questions with categories inside you must specify the relation in `FindOptions`:

```
const questionRepository = dataSource.getRepository(Question)const questions = await questionRepository.find({    relations: {        categories: true,    },})
```

Or using `QueryBuilder` you can join them:

```
const questions = await dataSource    .getRepository(Question)    .createQueryBuilder("question")    .leftJoinAndSelect("question.categories", "category")    .getMany()
```

With eager loading enabled on a relation, you don't have to specify relations in the find command as it will ALWAYS be loaded automatically. If you use QueryBuilder eager relations are disabled, you have to use `leftJoinAndSelect` to load the relation.

## Bi-directional relations​

Relations can be uni-directional and bi-directional.
Uni-directional relations are relations with a relation decorator only on one side.
Bi-directional relations are relations with decorators on both sides of a relation.

We just created a uni-directional relation. Let's make it bi-directional:

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm"import { Question } from "./Question"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @ManyToMany(() => Question, (question) => question.categories)    questions: Question[]}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany(() => Category, (category) => category.questions)    @JoinTable()    categories: Category[]}
```

We just made our relation bi-directional. Note that the inverse relation does not have a `@JoinTable`.
`@JoinTable` must be only on one side of the relation.

Bi-directional relations allow you to join relations from both sides using `QueryBuilder`:

```
const categoriesWithQuestions = await dataSource    .getRepository(Category)    .createQueryBuilder("category")    .leftJoinAndSelect("category.questions", "question")    .getMany()
```

## Many-to-many relations with custom properties​

In case you need to have additional properties in your many-to-many relationship, you have to create a new entity yourself.
For example, if you would like entities `Question` and `Category` to have a many-to-many relationship with an additional `order` column, then you need to create an entity `QuestionToCategory` with two `ManyToOne` relations pointing in both directions and with custom columns in it:

```
import { Entity, Column, ManyToOne, PrimaryGeneratedColumn } from "typeorm"import { Question } from "./question"import { Category } from "./category"@Entity()export class QuestionToCategory {    @PrimaryGeneratedColumn()    public questionToCategoryId: number    @Column()    public questionId: number    @Column()    public categoryId: number    @Column()    public order: number    @ManyToOne(() => Question, (question) => question.questionToCategories)    public question: Question    @ManyToOne(() => Category, (category) => category.questionToCategories)    public category: Category}
```

Additionally you will have to add a relationship like the following to `Question` and `Category`:

```
// category.ts...@OneToMany(() => QuestionToCategory, questionToCategory => questionToCategory.category)public questionToCategories: QuestionToCategory[];// question.ts...@OneToMany(() => QuestionToCategory, questionToCategory => questionToCategory.question)public questionToCategories: QuestionToCategory[];
```
