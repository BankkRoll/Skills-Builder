# Caching queries and more

# Caching queries

> You can cache results selected by these QueryBuilder methods: getMany, getOne, getRawMany, getRawOne and getCount.

You can cache results selected by these `QueryBuilder` methods: `getMany`, `getOne`, `getRawMany`, `getRawOne` and `getCount`.

You can also cache results selected by `find*` and `count*` methods of the `Repository` and `EntityManager`.

To enable caching you need to explicitly enable it in data source options:

```
{    type: "mysql",    host: "localhost",    username: "test",    ...    cache: true}
```

When you enable cache for the first time,
you must synchronize your database schema (using CLI, migrations or the `synchronize` data source option).

Then in `QueryBuilder` you can enable query cache for any query:

```
const users = await dataSource    .createQueryBuilder(User, "user")    .where("user.isAdmin = :isAdmin", { isAdmin: true })    .cache(true)    .getMany()
```

Equivalent `Repository` query:

```
const users = await dataSource.getRepository(User).find({    where: { isAdmin: true },    cache: true,})
```

This will execute a query to fetch all admin users and cache the results.
Next time you execute the same code, it will get all admin users from the cache.
Default cache lifetime is equal to `1000 ms`, e.g. 1 second.
This means the cache will be invalid 1 second after the query builder code is called.
In practice, this means that if users open the user page 150 times within 3 seconds, only three queries will be executed during this period.
Any users inserted during the 1 second cache window won't be returned to the user.

You can change cache time manually via `QueryBuilder`:

```
const users = await dataSource    .createQueryBuilder(User, "user")    .where("user.isAdmin = :isAdmin", { isAdmin: true })    .cache(60000) // 1 minute    .getMany()
```

Or via `Repository`:

```
const users = await dataSource.getRepository(User).find({    where: { isAdmin: true },    cache: 60000,})
```

Or globally in data source options:

```
{    type: "mysql",    host: "localhost",    username: "test",    ...    cache: {        duration: 30000 // 30 seconds    }}
```

Also, you can set a "cache id" via `QueryBuilder`:

```
const users = await dataSource    .createQueryBuilder(User, "user")    .where("user.isAdmin = :isAdmin", { isAdmin: true })    .cache("users_admins", 25000)    .getMany()
```

Or with `Repository`:

```
const users = await dataSource.getRepository(User).find({    where: { isAdmin: true },    cache: {        id: "users_admins",        milliseconds: 25000,    },})
```

This gives you granular control of your cache,
for example, clearing cached results when you insert a new user:

```
await dataSource.queryResultCache.remove(["users_admins"])
```

By default, TypeORM uses a separate table called `query-result-cache` and stores all queries and results there.
Table name is configurable, so you could change it by specifying a different value in the tableName property.
Example:

```
{    type: "mysql",    host: "localhost",    username: "test",    ...    cache: {        type: "database",        tableName: "configurable-table-query-result-cache"    }}
```

If storing cache in a single database table is not effective for you,
you can change the cache type to "redis" or "ioredis" and TypeORM will store all cached records in redis instead.
Example:

```
{    type: "mysql",    host: "localhost",    username: "test",    ...    cache: {        type: "redis",        options: {            socket: {                host: "localhost",                port: 6379            }        }    }}
```

"options" can be [node_redis specific options](https://github.com/redis/node-redis/blob/master/docs/client-configuration.md) or [ioredis specific options](https://github.com/luin/ioredis/blob/master/API.md#new-redisport-host-options) depending on what type you're using.

In case you want to connect to a redis-cluster using IORedis's cluster functionality, you can do that as well by doing the following:

```
{    type: "mysql",    host: "localhost",    username: "test",    cache: {        type: "ioredis/cluster",        options: {            startupNodes: [                {                    host: 'localhost',                    port: 7000,                },                {                    host: 'localhost',                    port: 7001,                },                {                    host: 'localhost',                    port: 7002,                }            ],            options: {                scaleReads: 'all',                clusterRetryStrategy: function (times) { return null },                redisOptions: {                    maxRetriesPerRequest: 1                }            }        }    }}
```

Note that, you can still use options as the first argument of IORedis's cluster constructor.

```
{    ...    cache: {        type: "ioredis/cluster",        options: [            {                host: 'localhost',                port: 7000,            },            {                host: 'localhost',                port: 7001,            },            {                host: 'localhost',                port: 7002,            }        ]    },    ...}
```

If none of the built-in cache providers satisfy your demands, then you can also specify your own cache provider by using a `provider` factory function which needs to return a new object that implements the `QueryResultCache` interface:

```
class CustomQueryResultCache implements QueryResultCache {    constructor(private dataSource: DataSource) {}    ...}
```

```
{    ...    cache: {        provider(dataSource) {            return new CustomQueryResultCache(dataSource);        }    }}
```

If you wish to ignore cache errors and want the queries to pass through to database in case of cache errors, you can use ignoreErrors option.
Example:

```
{    type: "mysql",    host: "localhost",    username: "test",    ...    cache: {        type: "redis",        options: {            socket: {                host: "localhost",                port: 6379            }        },        ignoreErrors: true    }}
```

You can use `typeorm cache:clear` to clear everything stored in the cache.

---

# Delete using Query Builder

> Delete

## Delete​

You can create `DELETE` queries using `QueryBuilder`.
Examples:

```
await myDataSource    .createQueryBuilder()    .delete()    .from(User)    .where("id = :id", { id: 1 })    .execute()
```

This is the most efficient way in terms of performance to delete entities from your database.

## Soft-Delete​

Applying Soft Delete to QueryBuilder

```
await dataSource.getRepository(Entity).createQueryBuilder().softDelete()
```

Examples:

```
await myDataSource    .getRepository(User)    .createQueryBuilder()    .softDelete()    .where("id = :id", { id: 1 })    .execute()
```

## Restore-Soft-Delete​

Alternatively, You can recover the soft deleted rows by using the `restore()` method:

```
await dataSource.getRepository(Entity).createQueryBuilder().restore()
```

Examples:

```
await myDataSource    .getRepository(User)    .createQueryBuilder()    .restore()    .where("id = :id", { id: 1 })    .execute()
```

---

# Insert using Query Builder

> You can create INSERT queries using QueryBuilder.

You can create `INSERT` queries using `QueryBuilder`.
Examples:

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values([        { firstName: "Timber", lastName: "Saw" },        { firstName: "Phantom", lastName: "Lancer" },    ])    .execute()
```

This is the most efficient way in terms of performance to insert rows into your database.
You can also perform bulk insertions this way.

## Raw SQL support​

In some cases when you need to execute SQL queries you need to use function style value:

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: () => "CONCAT('S', 'A', 'W')",    })    .execute()
```

> Warning: When using raw SQL, ensure that values are properly sanitized to prevent SQL injection.

## Update values ON CONFLICT​

If the values you are trying to insert conflict due to existing data the `orUpdate` function can be used to update specific values on the conflicted target.

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: "Saw",        externalId: "abc123",    })    .orUpdate(["firstName", "lastName"], ["externalId"])    .execute()
```

## Update values ON CONFLICT with condition (Postgres, Oracle, MSSQL, SAP HANA)​

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: "Saw",        externalId: "abc123",    })    .orUpdate(["firstName", "lastName"], ["externalId"], {        overwriteCondition: {            where: {                firstName: Equal("Phantom"),            },        },    })    .execute()
```

## IGNORE error (MySQL) or DO NOTHING (Postgres, Oracle, MSSQL, SAP HANA) during insert​

If the values you are trying to insert conflict due to existing data or containing invalid data, the `orIgnore` function can be used to suppress errors and insert only rows that contain valid data.

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: "Saw",        externalId: "abc123",    })    .orIgnore()    .execute()
```

## Skip data update if values have not changed (Postgres, Oracle, MSSQL, SAP HANA)​

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: "Saw",        externalId: "abc123",    })    .orUpdate(["firstName", "lastName"], ["externalId"], {        skipUpdateIfNoValuesChanged: true,    })    .execute()
```

## Use partial index (Postgres)​

```
await dataSource    .createQueryBuilder()    .insert()    .into(User)    .values({        firstName: "Timber",        lastName: "Saw",        externalId: "abc123",    })    .orUpdate(["firstName", "lastName"], ["externalId"], {        skipUpdateIfNoValuesChanged: true,        indexPredicate: "date > 2020-01-01",    })    .execute()
```

---

# Working with Relations

> RelationQueryBuilder is a special type of QueryBuilder which allows you to work with your relations.

`RelationQueryBuilder` is a special type of `QueryBuilder` which allows you to work with your relations.
Using it, you can bind entities to each other in the database without the need to load any entities,
or you can load related entities easily.

For example, we have a `Post` entity and it has a many-to-many relation to `Category` called `categories`.
Let's add a new category to this many-to-many relation:

```
await dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of(post)    .add(category)
```

This code is equivalent to doing this:

```
const postRepository = dataSource.manager.getRepository(Post)const post = await postRepository.findOne({    where: {        id: 1,    },    relations: {        categories: true,    },})post.categories.push(category)await postRepository.save(post)
```

But more efficient, because it does a minimal number of operations, and binds entities in the database,
unlike calling a bulky `save` method call.

Also, another benefit of such an approach is that you don't need to load every related entity before pushing into it.
For example, if you have ten thousand categories inside a single post, adding new posts to this list may become problematic for you,
because the standard way of doing this is to load the post with all ten thousand categories, push a new category,
and save it. This results in very heavy performance costs and is basically inapplicable in production results.
However, using `RelationQueryBuilder` solves this problem.

Also, there is no real need to use entities when you "bind" things, since you can use entity ids instead.
For example, let's add a category with id = 3 into post with id = 1:

```
await dataSource.createQueryBuilder().relation(Post, "categories").of(1).add(3)
```

If you are using composite primary keys, you have to pass them as an id map, for example:

```
await dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of({ firstPostId: 1, secondPostId: 3 })    .add({ firstCategoryId: 2, secondCategoryId: 4 })
```

You can remove entities the same way you add them:

```
// this code removes a category from a given postawait dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of(post) // you can use just post id as well    .remove(category) // you can use just category id as well
```

Adding and removing related entities works in `many-to-many` and `one-to-many` relations.
For `one-to-one` and `many-to-one` relations use `set` instead:

```
// this code sets category of a given postawait dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of(post) // you can use just post id as well    .set(category) // you can use just category id as well
```

If you want to unset a relation (set it to null), simply pass `null` to a `set` method:

```
// this code unsets category of a given postawait dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of(post) // you can use just post id as well    .set(null)
```

Besides updating relations, the relational query builder also allows you to load relational entities.
For example, lets say inside a `Post` entity we have a many-to-many `categories` relation and a many-to-one `user` relation,
to load those relations you can use following code:

```
const post = await dataSource.manager.findOneBy(Post, {    id: 1,})post.categories = await dataSource    .createQueryBuilder()    .relation(Post, "categories")    .of(post) // you can use just post id as well    .loadMany()post.author = await dataSource    .createQueryBuilder()    .relation(Post, "user")    .of(post) // you can use just post id as well    .loadOne()
```
