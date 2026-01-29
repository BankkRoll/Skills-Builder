# Find Options and more

# Find Options

> Basic options

## Basic options​

All repository and manager `.find*` methods accept special options you can use to query data you need without using `QueryBuilder`:

- `select` - indicates which properties of the main object must be selected

```
userRepository.find({    select: {        firstName: true,        lastName: true,    },})
```

will execute following query:

```
SELECT "firstName", "lastName" FROM "user"
```

- `relations` - relations needs to be loaded with the main entity. Sub-relations can also be loaded (shorthand for `join` and `leftJoinAndSelect`)

```
userRepository.find({    relations: {        profile: true,        photos: true,        videos: true,    },})userRepository.find({    relations: {        profile: true,        photos: true,        videos: {            videoAttributes: true,        },    },})
```

will execute following queries:

```
SELECT * FROM "user"LEFT JOIN "profile" ON "profile"."id" = "user"."profileId"LEFT JOIN "photos" ON "photos"."id" = "user"."photoId"LEFT JOIN "videos" ON "videos"."id" = "user"."videoId"SELECT * FROM "user"LEFT JOIN "profile" ON "profile"."id" = "user"."profileId"LEFT JOIN "photos" ON "photos"."id" = "user"."photoId"LEFT JOIN "videos" ON "videos"."id" = "user"."videoId"LEFT JOIN "video_attributes" ON "video_attributes"."id" = "videos"."video_attributesId"
```

- `where` - simple conditions by which entity should be queried.

```
userRepository.find({    where: {        firstName: "Timber",        lastName: "Saw",    },})
```

will execute following query:

```
SELECT * FROM "user"WHERE "firstName" = 'Timber' AND "lastName" = 'Saw'
```

Querying a column from an embedded entity should be done with respect to the hierarchy in which it was defined. Example:

```
userRepository.find({    relations: {        project: true,    },    where: {        project: {            name: "TypeORM",            initials: "TORM",        },    },})
```

will execute following query:

```
SELECT * FROM "user"LEFT JOIN "project" ON "project"."id" = "user"."projectId"WHERE "project"."name" = 'TypeORM' AND "project"."initials" = 'TORM'
```

Querying with OR operator:

```
userRepository.find({    where: [        { firstName: "Timber", lastName: "Saw" },        { firstName: "Stan", lastName: "Lee" },    ],})
```

will execute following query:

```
SELECT * FROM "user" WHERE ("firstName" = 'Timber' AND "lastName" = 'Saw') OR ("firstName" = 'Stan' AND "lastName" = 'Lee')
```

- `order` - selection order.

```
userRepository.find({    order: {        name: "ASC",        id: "DESC",    },})
```

will execute following query:

```
SELECT * FROM "user"ORDER BY "name" ASC, "id" DESC
```

- `withDeleted` - include entities which have been soft deleted with `softDelete` or `softRemove`, e.g. have their `@DeleteDateColumn` column set. By default, soft deleted entities are not included.

```
userRepository.find({    withDeleted: true,})
```

`find*` methods which return multiple entities (`find`, `findBy`, `findAndCount`, `findAndCountBy`) also accept following options:

- `skip` - offset (paginated) from where entities should be taken.

```
userRepository.find({    skip: 5,})
```

```
SELECT * FROM "user"OFFSET 5
```

- `take` - limit (paginated) - max number of entities that should be taken.

```
userRepository.find({    take: 10,})
```

will execute following query:

```
SELECT * FROM "user"LIMIT 10
```

** `skip` and `take` should be used together

** If you are using typeorm with MSSQL, and want to use `take` or `limit`, you need to use order as well or you will receive the following error: `'Invalid usage of the option NEXT in the FETCH statement.'`

```
userRepository.find({    order: {        columnName: "ASC",    },    skip: 0,    take: 10,})
```

will execute following query:

```
SELECT * FROM "user"ORDER BY "columnName" ASCLIMIT 10 OFFSET 0
```

- `cache` - Enables or disables query result caching. See [caching](https://typeorm.io/docs/query-builder/caching) for more information and options.

```
userRepository.find({    cache: true,})
```

- `lock` - Enables locking mechanism for query. Can be used only in `findOne` and `findOneBy` methods.
  `lock` is an object which can be defined as:

```
{ mode: "optimistic", version: number | Date }
```

or

```
{    mode: "pessimistic_read" |        "pessimistic_write" |        "dirty_read" |        /*            "pessimistic_partial_write" and "pessimistic_write_or_fail" are deprecated and            will be removed in a future version.            Use onLocked instead.         */        "pessimistic_partial_write" |        "pessimistic_write_or_fail" |        "for_no_key_update" |        "for_key_share",    tables: string[],    onLocked: "nowait" | "skip_locked"}
```

for example:

```
userRepository.findOne({    where: {        id: 1,    },    lock: { mode: "optimistic", version: 1 },})
```

See [lock modes](https://typeorm.io/docs/query-builder/select-query-builder#lock-modes) for more information

Complete example of find options:

```
userRepository.find({    select: {        firstName: true,        lastName: true,    },    relations: {        profile: true,        photos: true,        videos: true,    },    where: {        firstName: "Timber",        lastName: "Saw",        profile: {            userName: "tshaw",        },    },    order: {        name: "ASC",        id: "DESC",    },    skip: 5,    take: 10,    cache: true,})
```

Find without arguments:

```
userRepository.find()
```

will execute following query:

```
SELECT * FROM "user"
```

## Advanced options​

TypeORM provides a lot of built-in operators that can be used to create more complex comparisons:

- `Not`

```
import { Not } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Not("About #1"),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" != 'About #1'
```

- `LessThan`

```
import { LessThan } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: LessThan(10),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" < 10
```

- `LessThanOrEqual`

```
import { LessThanOrEqual } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: LessThanOrEqual(10),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" <= 10
```

- `MoreThan`

```
import { MoreThan } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: MoreThan(10),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" > 10
```

- `MoreThanOrEqual`

```
import { MoreThanOrEqual } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: MoreThanOrEqual(10),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" >= 10
```

- `Equal`

```
import { Equal } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Equal("About #2"),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" = 'About #2'
```

- `Like`

```
import { Like } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Like("%out #%"),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" LIKE '%out #%'
```

- `ILike`

```
import { ILike } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: ILike("%out #%"),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" ILIKE '%out #%'
```

- `Between`

```
import { Between } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: Between(1, 10),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" BETWEEN 1 AND 10
```

- `In`

```
import { In } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: In(["About #2", "About #3"]),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" IN ('About #2','About #3')
```

- `Any`

```
import { Any } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Any(["About #2", "About #3"]),})
```

will execute following query (Postgres notation):

```
SELECT * FROM "post" WHERE "title" = ANY(['About #2','About #3'])
```

- `IsNull`

```
import { IsNull } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: IsNull(),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" IS NULL
```

- `ArrayContains`

```
import { ArrayContains } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    categories: ArrayContains(["TypeScript"]),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "categories" @> '{TypeScript}'
```

- `ArrayContainedBy`

```
import { ArrayContainedBy } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    categories: ArrayContainedBy(["TypeScript"]),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "categories" <@ '{TypeScript}'
```

- `ArrayOverlap`

```
import { ArrayOverlap } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    categories: ArrayOverlap(["TypeScript"]),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "categories" && '{TypeScript}'
```

- `Raw`

```
import { Raw } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: Raw("dislikes - 4"),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "likes" = "dislikes" - 4
```

In the simplest case, a raw query is inserted immediately after the equal symbol.
But you can also completely rewrite the comparison logic using the function.

```
import { Raw } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    currentDate: Raw((alias) => `${alias} > NOW()`),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "currentDate" > NOW()
```

If you need to provide user input, you should not include the user input directly in your query as this may create a SQL injection vulnerability. Instead, you can use the second argument of the `Raw` function to provide a list of parameters to bind to the query.

```
import { Raw } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    currentDate: Raw((alias) => `${alias} > :date`, { date: "2020-10-06" }),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "currentDate" > '2020-10-06'
```

If you need to provide user input that is an array, you can bind them as a list of values in the SQL statement by using the special expression syntax:

```
import { Raw } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Raw((alias) => `${alias} IN (:...titles)`, {        titles: [            "Go To Statement Considered Harmful",            "Structured Programming",        ],    }),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" IN ('Go To Statement Considered Harmful', 'Structured Programming')
```

## Combining Advanced Options​

Also you can combine these operators with below:

- `Not`

```
import { Not, MoreThan, Equal } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    likes: Not(MoreThan(10)),    title: Not(Equal("About #2")),})
```

will execute following query:

```
SELECT * FROM "post" WHERE NOT("likes" > 10) AND NOT("title" = 'About #2')
```

- `Or`

```
import { Or, Equal, ILike } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: Or(Equal("About #2"), ILike("About%")),})
```

will execute following query:

```
SELECT * FROM "post" WHERE "title" = 'About #2' OR "title" ILIKE 'About%'
```

- `And`

```
import { And, Not, Equal, ILike } from "typeorm"const loadedPosts = await dataSource.getRepository(Post).findBy({    title: And(Not(Equal("About #2")), ILike("%About%")),})
```

will execute following query:

```
SELECT * FROM "post" WHERE NOT("title" = 'About #2') AND "title" ILIKE '%About%'
```

---

# Repository APIs

> Repository API

## RepositoryAPI​

- `manager` - The `EntityManager` used by this repository.

```
const manager = repository.manager
```

- `metadata` - The `EntityMetadata` of the entity managed by this repository.

```
const metadata = repository.metadata
```

- `queryRunner` - The query runner used by `EntityManager`.
  Used only in transactional instances of EntityManager.

```
const queryRunner = repository.queryRunner
```

- `target` - The target entity class managed by this repository.
  Used only in transactional instances of EntityManager.

```
const target = repository.target
```

- `createQueryBuilder` - Creates a query builder use to build SQL queries.
  Learn more about [QueryBuilder](https://typeorm.io/docs/query-builder/select-query-builder).

```
const users = await repository    .createQueryBuilder("user")    .where("user.name = :name", { name: "John" })    .getMany()
```

- `hasId` - Checks if the given entity's primary column property is defined.

```
if (repository.hasId(user)) {    // ... do something}
```

- `getId` - Gets the primary column property values of the given entity.
  If entity has composite primary keys then the returned value will be an object with names and values of primary columns.

```
const userId = repository.getId(user) // userId === 1
```

- `create` - Creates a new instance of `User`. Optionally accepts an object literal with user properties
  which will be written into newly created user object

```
const user = repository.create() // same as const user = new User();const user = repository.create({    id: 1,    firstName: "Timber",    lastName: "Saw",}) // same as const user = new User(); user.firstName = "Timber"; user.lastName = "Saw";
```

- `merge` - Merges multiple entities into a single entity.

```
const user = new User()repository.merge(user, { firstName: "Timber" }, { lastName: "Saw" }) // same as user.firstName = "Timber"; user.lastName = "Saw";
```

- `preload` - Creates a new entity from the given plain javascript object. If the entity already exists in the database, then
  it loads it (and everything related to it), replaces all values with the new ones from the given object,
  and returns the new entity. The new entity is actually an entity loaded from the database with all properties
  replaced from the new object.
  > Note that given entity-like object must have an entity id / primary key to find entity by. Returns undefined if entity with given id was not found.

```
const partialUser = {    id: 1,    firstName: "Rizzrak",    profile: {        id: 1,    },}const user = await repository.preload(partialUser)// user will contain all missing data from partialUser with partialUser property values:// { id: 1, firstName: "Rizzrak", lastName: "Saw", profile: { id: 1, ... } }
```

- `save` - Saves a given entity or array of entities.
  If the entity already exist in the database, it is updated.
  If the entity does not exist in the database, it is inserted.
  It saves all given entities in a single transaction (in the case of entity, manager is not transactional).
  Also supports partial updating since all undefined properties are skipped.
  Returns the saved entity/entities.

```
await repository.save(user)await repository.save([category1, category2, category3])
```

- `remove` - Removes a given entity or array of entities.
  It removes all given entities in a single transaction (in the case of entity, manager is not transactional).
  Returns the removed entity/entities.

```
await repository.remove(user)await repository.remove([category1, category2, category3])
```

- `insert` - Inserts a new entity, or array of entities.

```
await repository.insert({    firstName: "Timber",    lastName: "Timber",})await repository.insert([    {        firstName: "Foo",        lastName: "Bar",    },    {        firstName: "Rizz",        lastName: "Rak",    },])
```

- `update` - Updates entities by entity id, ids or given conditions. Sets fields from supplied partial entity.

```
await repository.update({ age: 18 }, { category: "ADULT" })// executes UPDATE user SET category = ADULT WHERE age = 18await repository.update(1, { firstName: "Rizzrak" })// executes UPDATE user SET firstName = Rizzrak WHERE id = 1// optionally request RETURNING / OUTPUT values (supported drivers only)const result = await repository.update(    1,    { firstName: "Rizzrak" },    { returning: ["id", "firstName"] },)console.log(result.raw) // [{ id: 1, firstName: "Rizzrak" }]
```

- `updateAll` - Updates *all* entities of target type (without WHERE clause). Sets fields from supplied partial entity.

```
await repository.updateAll({ category: "ADULT" })// executes UPDATE user SET category = ADULTawait repository.updateAll(    { category: "ADULT" },    { returning: "*" }, // limited to drivers that support returning clauses)
```

- `upsert` - Inserts a new entity or array of entities unless they already exist in which case they are updated instead. Supported by AuroraDataApi, Cockroach, Mysql, Postgres, and Sqlite database drivers.

When an upsert operation results in an update (due to a conflict), special columns like `@UpdateDateColumn` and `@VersionColumn` are automatically updated to their current values.

```
await repository.upsert(    [        { externalId: "abc123", firstName: "Rizzrak" },        { externalId: "bca321", firstName: "Karzzir" },    ],    ["externalId"],)/** executes *  INSERT INTO user *  VALUES *      (externalId = abc123, firstName = Rizzrak), *      (externalId = cba321, firstName = Karzzir), *  ON CONFLICT (externalId) DO UPDATE  *  SET firstName = EXCLUDED.firstName, *      updatedDate = CURRENT_TIMESTAMP, *      version = version + 1 **/
```

You can also request values to be returned from an upsert (supported on drivers with RETURNING / OUTPUT support):

```
const { raw } = await repository.upsert(    { externalId: "abc123", firstName: "Rizzrak" },    {        conflictPaths: ["externalId"],        returning: ["externalId", "firstName"],    },)console.log(raw) // [{ externalId: "abc123", firstName: "Rizzrak" }]
```

```
await repository.upsert(    [        { externalId: "abc123", firstName: "Rizzrak" },        { externalId: "bca321", firstName: "Karzzir" },    ],    {        conflictPaths: ["externalId"],        skipUpdateIfNoValuesChanged: true, // supported by postgres, skips update if it would not change row values        upsertType: "upsert", //  "on-conflict-do-update" | "on-duplicate-key-update" | "upsert" - optionally provide an UpsertType - 'upsert' is currently only supported by CockroachDB    },)/** executes *  INSERT INTO user *  VALUES *      (externalId = abc123, firstName = Rizzrak), *      (externalId = cba321, firstName = Karzzir), *  ON CONFLICT (externalId) DO UPDATE *  SET firstName = EXCLUDED.firstName *  WHERE user.firstName IS DISTINCT FROM EXCLUDED.firstName **/
```

```
await repository.upsert(    [        { externalId: "abc123", firstName: "Rizzrak", dateAdded: "2020-01-01" },        { externalId: "bca321", firstName: "Karzzir", dateAdded: "2022-01-01" },    ],    {        conflictPaths: ["externalId"],        skipUpdateIfNoValuesChanged: true, // supported by postgres, skips update if it would not change row values        indexPredicate: "dateAdded > 2020-01-01", // supported by postgres, allows for partial indexes    },)/** executes *  INSERT INTO user *  VALUES *      (externalId = abc123, firstName = Rizzrak, dateAdded = 2020-01-01), *      (externalId = cba321, firstName = Karzzir, dateAdded = 2022-01-01), *  ON CONFLICT (externalId) WHERE ( dateAdded > 2021-01-01 ) DO UPDATE *  SET firstName = EXCLUDED.firstName, *  SET dateAdded = EXCLUDED.dateAdded, *  WHERE user.firstName IS DISTINCT FROM EXCLUDED.firstName OR user.dateAdded IS DISTINCT FROM EXCLUDED.dateAdded **/
```

- `delete` - Deletes entities by entity id, ids or given conditions:

```
await repository.delete(1)await repository.delete([1, 2, 3])await repository.delete({ firstName: "Timber" })
```

- `deleteAll` - Deletes *all* entities of target type (without WHERE clause).

```
await repository.deleteAll()// executes DELETE FROM user
```

Refer also to the `clear` method, which performs database `TRUNCATE TABLE` operation instead.

- `softDelete` and `restore` - Soft deleting and restoring a row by id, ids, or given conditions:

```
const repository = dataSource.getRepository(Entity)// Soft delete an entityawait repository.softDelete(1)// And you can restore it using restore;await repository.restore(1)// Soft delete multiple entitiesawait repository.softDelete([1, 2, 3])// Or soft delete by other attributeawait repository.softDelete({ firstName: "Jake" })
```

- `softRemove` and `recover` - This is alternative to `softDelete` and `restore`.

```
// You can soft-delete them using softRemoveconst entities = await repository.find()const entitiesAfterSoftRemove = await repository.softRemove(entities)// And You can recover them using recover;await repository.recover(entitiesAfterSoftRemove)
```

- `increment` - Increments some column by provided value of entities that match given options.

```
await repository.increment({ firstName: "Timber" }, "age", 3)
```

- `decrement` - Decrements some column by provided value that match given options.

```
await repository.decrement({ firstName: "Timber" }, "age", 3)
```

- `exists` - Check whether any entity exists that matches `FindOptions`.

```
const exists = await repository.exists({    where: {        firstName: "Timber",    },})
```

- `existsBy` - Checks whether any entity exists that matches `FindOptionsWhere`.

```
const exists = await repository.existsBy({ firstName: "Timber" })
```

- `count` - Counts entities that match `FindOptions`. Useful for pagination.

```
const count = await repository.count({    where: {        firstName: "Timber",    },})
```

- `countBy` - Counts entities that match `FindOptionsWhere`. Useful for pagination.

```
const count = await repository.countBy({ firstName: "Timber" })
```

- `sum` - Returns the sum of a numeric field for all entities that match `FindOptionsWhere`.

```
const sum = await repository.sum("age", { firstName: "Timber" })
```

- `average` - Returns the average of a numeric field for all entities that match `FindOptionsWhere`.

```
const average = await repository.average("age", { firstName: "Timber" })
```

- `minimum` - Returns the minimum of a numeric field for all entities that match `FindOptionsWhere`.

```
const minimum = await repository.minimum("age", { firstName: "Timber" })
```

- `maximum` - Returns the maximum of a numeric field for all entities that match `FindOptionsWhere`.

```
const maximum = await repository.maximum("age", { firstName: "Timber" })
```

- `find` - Finds entities that match given `FindOptions`.

```
const timbers = await repository.find({    where: {        firstName: "Timber",    },})
```

- `findBy` - Finds entities that match given `FindWhereOptions`.

```
const timbers = await repository.findBy({    firstName: "Timber",})
```

- `findAndCount` - Finds entities that match given `FindOptions`.
  Also counts all entities that match given conditions,
  but ignores pagination settings (from and take options).

```
const [timbers, timbersCount] = await repository.findAndCount({    where: {        firstName: "Timber",    },})
```

- `findAndCountBy` - Finds entities that match given `FindOptionsWhere`.
  Also counts all entities that match given conditions,
  but ignores pagination settings (from and take options).

```
const [timbers, timbersCount] = await repository.findAndCountBy({    firstName: "Timber",})
```

- `findOne` - Finds the first entity that matches given `FindOptions`.

```
const timber = await repository.findOne({    where: {        firstName: "Timber",    },})
```

- `findOneBy` - Finds the first entity that matches given `FindOptionsWhere`.

```
const timber = await repository.findOneBy({ firstName: "Timber" })
```

- `findOneOrFail` - Finds the first entity that matches some id or find options.
  Rejects the returned promise if nothing matches.

```
const timber = await repository.findOneOrFail({    where: {        firstName: "Timber",    },})
```

- `findOneByOrFail` - Finds the first entity that matches given `FindOptions`.
  Rejects the returned promise if nothing matches.

```
const timber = await repository.findOneByOrFail({ firstName: "Timber" })
```

- `query` - Executes a raw SQL query.

```
const rawData = await repository.query(`SELECT * FROM USERS`)// You can also use parameters to avoid SQL injection// The syntax differs between the drivers// aurora-mysql, better-sqlite3, capacitor, cordova,// expo, mariadb, mysql, nativescript, react-native,// sap, sqlite, sqljsconst rawData = await repository.query(    "SELECT * FROM USERS WHERE name = ? and age = ?",    ["John", 24],)// aurora-postgres, cockroachdb, postgresconst rawData = await repository.query(    "SELECT * FROM USERS WHERE name = $1 and age = $2",    ["John", 24],)// oracleconst rawData = await repository.query(    "SELECT * FROM USERS WHERE name = :1 and age = :2",    ["John", 24],)// spannerconst rawData = await repository.query(    "SELECT * FROM USERS WHERE name = @param0 and age = @param1",    ["John", 24],)// mssqlconst rawData = await repository.query(    "SELECT * FROM USERS WHERE name = @0 and age = @1",    ["John", 24],)
```

- `clear` - Clears all the data from the given table (truncates/drops it).

```
await repository.clear()
```

### Additional Options​

Optional `SaveOptions` can be passed as parameter for `save`.

- `data` - Additional data to be passed with persist method. This data can be used in subscribers then.
- `listeners`: boolean - Indicates if listeners and subscribers are called for this operation. By default they are enabled, you can disable them by setting `{ listeners: false }` in save/remove options.
- `transaction`: boolean - By default transactions are enabled and all queries in persistence operation are wrapped into the transaction. You can disable this behaviour by setting `{ transaction: false }` in the persistence options.
- `chunk`: number - Breaks save execution into multiple groups of chunks. For example, if you want to save 100.000 objects but you have issues with saving them, you can break them into 10 groups of 10.000 objects (by setting `{ chunk: 10000 }`) and save each group separately. This option is needed to perform very big insertions when you have issues with underlying driver parameter number limitation.
- `reload`: boolean - Flag to determine whether the entity that is being persisted should be reloaded during the persistence operation. It will work only on databases which do not support RETURNING / OUTPUT statement. Enabled by default.

Example:

```
userRepository.save(users, { chunk: 1000 })
```

Optional `RemoveOptions` can be passed as parameter for `remove` and `delete`.

- `data` - Additional data to be passed with remove method. This data can be used in subscribers then.
- `listeners`: boolean - Indicates if listeners and subscribers are called for this operation. By default they are enabled, you can disable them by setting `{ listeners: false }` in save/remove options.
- `transaction`: boolean - By default transactions are enabled and all queries in persistence operation are wrapped into the transaction. You can disable this behaviour by setting `{ transaction: false }` in the persistence options.
- `chunk`: number - Breaks removal execution into multiple groups of chunks. For example, if you want to remove 100.000 objects but you have issues doing so, you can break them into 10 groups of 10.000 objects, by setting `{ chunk: 10000 }`, and remove each group separately. This option is needed to perform very big deletions when you have issues with underlying driver parameter number limitation.

Example:

```
userRepository.remove(users, { chunk: 1000 })
```

## TreeRepositoryAPI​

For `TreeRepository` API refer to [the Tree Entities documentation](https://typeorm.io/docs/entity/tree-entities#working-with-tree-entities).

## MongoRepositoryAPI​

For `MongoRepository` API refer to [the MongoDB documentation](https://typeorm.io/docs/drivers/mongodb).

---

# EntityManager

> Using EntityManager you can manage (insert, update, delete, load, etc.) any entity.

Using `EntityManager` you can manage (insert, update, delete, load, etc.) any entity.
EntityManager is just like a collection of all entity repositories in a single place.

You can access the entity manager via DataSource.
Example how to use it:

```
import { DataSource } from "typeorm"import { User } from "./entity/User"const myDataSource = new DataSource(/*...*/)const user = await myDataSource.manager.findOneBy(User, {    id: 1,})user.name = "Umed"await myDataSource.manager.save(user)
```

---

# Repository

> Repository is just like EntityManager but its operations are limited to a concrete entity.

`Repository` is just like `EntityManager` but its operations are limited to a concrete entity.
You can access the repository via EntityManager.

Example:

```
import { User } from "./entity/User"const userRepository = dataSource.getRepository(User)const user = await userRepository.findOneBy({    id: 1,})user.name = "Umed"await userRepository.save(user)
```

There are 3 types of repositories:

- `Repository` - Regular repository for any entity.
- `TreeRepository` - Repository, extensions of `Repository` used for tree-entities
  (like entities marked with `@Tree` decorator).
  Has special methods to work with tree structures.
- `MongoRepository` - Repository with special functions used only with MongoDB.
