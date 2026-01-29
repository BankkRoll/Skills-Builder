# Many and more

# Many

> Many-to-one / one-to-many is a relation where A contains multiple instances of B, but B contains only one instance of A.

Many-to-one / one-to-many is a relation where A contains multiple instances of B, but B contains only one instance of A.
Let's take for example `User` and `Photo` entities.
User can have multiple photos, but each photo is owned by only one single user.

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToOne } from "typeorm"import { User } from "./User"@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    url: string    @ManyToOne(() => User, (user) => user.photos)    user: User}
```

```
import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from "typeorm"import { Photo } from "./Photo"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToMany(() => Photo, (photo) => photo.user)    photos: Photo[]}
```

Here we added `@OneToMany` to the `photos` property and specified the target relation type to be `Photo`.
You can omit `@JoinColumn` in a `@ManyToOne` / `@OneToMany` relation.
`@OneToMany` cannot exist without `@ManyToOne`.
If you want to use `@OneToMany`, `@ManyToOne` is required. However, the inverse is not required: If you only care about the `@ManyToOne` relationship, you can define it without having `@OneToMany` on the related entity.
Where you set `@ManyToOne` - its related entity will have "relation id" and foreign key.

This example will produce following tables:

```
+-------------+--------------+----------------------------+|                         photo                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || url         | varchar(255) |                            || userId      | int          | FOREIGN KEY                |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|                          user                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(255) |                            |+-------------+--------------+----------------------------+
```

Example how to save such relation:

```
const photo1 = new Photo()photo1.url = "me.jpg"await dataSource.manager.save(photo1)const photo2 = new Photo()photo2.url = "me-and-bears.jpg"await dataSource.manager.save(photo2)const user = new User()user.name = "John"user.photos = [photo1, photo2]await dataSource.manager.save(user)
```

or alternatively you can do:

```
const user = new User()user.name = "Leo"await dataSource.manager.save(user)const photo1 = new Photo()photo1.url = "me.jpg"photo1.user = userawait dataSource.manager.save(photo1)const photo2 = new Photo()photo2.url = "me-and-bears.jpg"photo2.user = userawait dataSource.manager.save(photo2)
```

With [cascades](https://typeorm.io/docs/relations/relations#cascades) enabled you can save this relation with only one `save` call.

To load a user with photos inside you must specify the relation in `FindOptions`:

```
const userRepository = dataSource.getRepository(User)const users = await userRepository.find({    relations: {        photos: true,    },})// or from inverse sideconst photoRepository = dataSource.getRepository(Photo)const photos = await photoRepository.find({    relations: {        user: true,    },})
```

Or using `QueryBuilder` you can join them:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.photos", "photo")    .getMany()// or from inverse sideconst photos = await dataSource    .getRepository(Photo)    .createQueryBuilder("photo")    .leftJoinAndSelect("photo.user", "user")    .getMany()
```

With eager loading enabled on a relation, you don't have to specify relations in the find command as it will ALWAYS be loaded automatically.
If you use QueryBuilder eager relations are disabled, you have to use `leftJoinAndSelect` to load the relation.

---

# One

> One-to-one is a relation where A contains only one instance of B, and B contains only one instance of A.

One-to-one is a relation where A contains only one instance of B, and B contains only one instance of A.
Let's take for example `User` and `Profile` entities.
User can have only a single profile, and a single profile is owned by only a single user.

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Profile {    @PrimaryGeneratedColumn()    id: number    @Column()    gender: string    @Column()    photo: string}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    OneToOne,    JoinColumn,} from "typeorm"import { Profile } from "./Profile"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToOne(() => Profile)    @JoinColumn()    profile: Profile}
```

Here we added `@OneToOne` to the `user` and specified the target relation type to be `Profile`.
We also added `@JoinColumn` which is required and must be set only on one side of the relation.
The side you set `@JoinColumn` on, that side's table will contain a "relation id" and foreign keys to the target entity table.

This example will produce the following tables:

```
+-------------+--------------+----------------------------+|                        profile                          |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || gender      | varchar(255) |                            || photo       | varchar(255) |                            |+-------------+--------------+----------------------------++-------------+--------------+----------------------------+|                          user                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(255) |                            || profileId   | int          | FOREIGN KEY                |+-------------+--------------+----------------------------+
```

Again, `@JoinColumn` must be set only on one side of the relation - the side that must have the foreign key in the database table.

Example how to save such a relation:

```
const profile = new Profile()profile.gender = "male"profile.photo = "me.jpg"await dataSource.manager.save(profile)const user = new User()user.name = "Joe Smith"user.profile = profileawait dataSource.manager.save(user)
```

With [cascades](https://typeorm.io/docs/relations/relations#cascades) enabled you can save this relation with only one `save` call.

To load user with profile inside you must specify relation in `FindOptions`:

```
const users = await dataSource.getRepository(User).find({    relations: {        profile: true,    },})
```

Or using `QueryBuilder` you can join them:

```
const users = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.profile", "profile")    .getMany()
```

With eager loading enabled on a relation, you don't have to specify relations in the find command as it will ALWAYS be loaded automatically. If you use QueryBuilder eager relations are disabled, you have to use `leftJoinAndSelect` to load the relation.

Relations can be uni-directional and bi-directional.
Uni-directional are relations with a relation decorator only on one side.
Bi-directional are relations with decorators on both sides of a relation.

We just created a uni-directional relation. Let's make it bi-directional:

```
import { Entity, PrimaryGeneratedColumn, Column, OneToOne } from "typeorm"import { User } from "./User"@Entity()export class Profile {    @PrimaryGeneratedColumn()    id: number    @Column()    gender: string    @Column()    photo: string    @OneToOne(() => User, (user) => user.profile) // specify inverse side as a second parameter    user: User}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    OneToOne,    JoinColumn,} from "typeorm"import { Profile } from "./Profile"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToOne(() => Profile, (profile) => profile.user) // specify inverse side as a second parameter    @JoinColumn()    profile: Profile}
```

We just made our relation bi-directional. Note, inverse relation does not have a `@JoinColumn`.
`@JoinColumn` must only be on one side of the relation - on the table that will own the foreign key.

Bi-directional relations allow you to join relations from both sides using `QueryBuilder`:

```
const profiles = await dataSource    .getRepository(Profile)    .createQueryBuilder("profile")    .leftJoinAndSelect("profile.user", "user")    .getMany()
```

---

# Relations FAQ

> How to create self referencing relation?

## How to create self referencing relation?​

Self-referencing relations are relations which have a relation to themselves.
This is useful when you are storing entities in a tree-like structures.
Also, "adjacency list" pattern is implemented using self-referenced relations.
For example, you want to create categories tree in your application.
Categories can nest categories, nested categories can nest other categories, etc.
Self-referencing relations come handy here.
Basically self-referencing relations are just regular relations that targets entity itself.
Example:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToOne,    OneToMany,} from "typeorm"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToOne((type) => Category, (category) => category.childCategories)    parentCategory: Category    @OneToMany((type) => Category, (category) => category.parentCategory)    childCategories: Category[]}
```

## How to use relation id without joining relation?​

Sometimes you want to have, in your object, the id of the related object without loading it.
For example:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Profile {    @PrimaryGeneratedColumn()    id: number    @Column()    gender: string    @Column()    photo: string}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    OneToOne,    JoinColumn,} from "typeorm"import { Profile } from "./Profile"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToOne((type) => Profile)    @JoinColumn()    profile: Profile}
```

When you load a user without `profile` joined you won't have any information about profile in your user object,
even profile id:

```
User {  id: 1,  name: "Umed"}
```

But sometimes you want to know what is the "profile id" of this user without loading the whole profile for this user.
To do this you just need to add another property to your entity with `@Column`
named exactly as the column created by your relation. Example:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    OneToOne,    JoinColumn,} from "typeorm"import { Profile } from "./Profile"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column({ nullable: true })    profileId: number    @OneToOne((type) => Profile)    @JoinColumn()    profile: Profile}
```

That's all. Next time you load a user object it will contain a profile id:

```
User {  id: 1,  name: "Umed",  profileId: 1}
```

## How to load relations in entities?​

The easiest way to load your entity relations is to use `relations` option in `FindOptions`:

```
const users = await dataSource.getRepository(User).find({    relations: {        profile: true,        photos: true,        videos: true,    },})
```

Alternative and more flexible way is to use `QueryBuilder`:

```
const user = await dataSource    .getRepository(User)    .createQueryBuilder("user")    .leftJoinAndSelect("user.profile", "profile")    .leftJoinAndSelect("user.photos", "photo")    .leftJoinAndSelect("user.videos", "video")    .getMany()
```

Using `QueryBuilder` you can do `innerJoinAndSelect` instead of `leftJoinAndSelect`
(to learn the difference between `LEFT JOIN` and `INNER JOIN` refer to your SQL documentation),
you can join relation data by a condition, make ordering, etc.

Learn more about [QueryBuilder](https://typeorm.io/docs/query-builder/select-query-builder).

## Avoid relation property initializers​

Sometimes it is useful to initialize your relation properties, for example:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany((type) => Category, (category) => category.questions)    @JoinTable()    categories: Category[] = [] // see = [] initialization here}
```

However, in TypeORM entities it may cause problems.
To understand the problem, let's first try to load a Question entity WITHOUT the initializer set.
When you load a question it will return an object like this:

```
Question {    id: 1,    title: "Question about ..."}
```

Now when you save this object `categories` inside it won't be touched - because it is unset.

But if you have an initializer, the loaded object will look as follows:

```
Question {    id: 1,    title: "Question about ...",    categories: []}
```

When you save the object it will check if there are any categories in the database bind to the question -
and it will detach all of them. Why? Because relation equal to `[]` or any items inside it will be considered
like something was removed from it, there is no other way to check if an object was removed from entity or not.

Therefore, saving an object like this will bring you problems - it will remove all previously set categories.

How to avoid this behaviour? Simply don't initialize arrays in your entities.
Same rule applies to a constructor - don't initialize it in a constructor as well.

## Avoid foreign key constraint creation​

Sometimes for performance reasons you might want to have a relation between entities, but without foreign key constraint.
You can define if foreign key constraint should be created with `createForeignKeyConstraints` option (default: true).

```
import { Entity, PrimaryColumn, Column, ManyToOne } from "typeorm"import { Person } from "./Person"@Entity()export class ActionLog {    @PrimaryColumn()    id: number    @Column()    date: Date    @Column()    action: string    @ManyToOne((type) => Person, {        createForeignKeyConstraints: false,    })    person: Person}
```

## Avoid circular import errors​

Here is an example if you want to define your entities, and you don't want those to cause errors in some environments.
In this situation we have Action.ts and Person.ts importing each other for a many-to-many relationship.
We use import type so that we can use the type information without any JavaScript code being generated.

```
import { Entity, PrimaryColumn, Column, ManytoMany } from "typeorm"import type { Person } from "./Person"@Entity()export class ActionLog {    @PrimaryColumn()    id: number    @Column()    date: Date    @Column()    action: string    @ManyToMany("Person", (person: Person) => person.id)    person: Person}
```

```
import { Entity, PrimaryColumn, ManytoMany } from "typeorm"import type { ActionLog } from "./Action"@Entity()export class Person {    @PrimaryColumn()    id: number    @ManyToMany("ActionLog", (actionLog: ActionLog) => actionLog.id)    log: ActionLog}
```

---

# Relations

> What are relations?

## What are relations?​

Relations helps you to work with related entities easily.
There are several types of relations:

- [one-to-one](https://typeorm.io/docs/relations/one-to-one-relations) using `@OneToOne`
- [many-to-one](https://typeorm.io/docs/relations/many-to-one-one-to-many-relations) using `@ManyToOne`
- [one-to-many](https://typeorm.io/docs/relations/many-to-one-one-to-many-relations) using `@OneToMany`
- [many-to-many](https://typeorm.io/docs/relations/many-to-many-relations) using `@ManyToMany`

## Relation options​

There are several options you can specify for relations:

- `eager: boolean` (default: `false`) - If set to true, the relation will always be loaded with the main entity when using `find*` methods or `QueryBuilder` on this entity
- `cascade: boolean | ("insert" | "update")[]` (default: `false`) - If set to true, the related object will be inserted and updated in the database. You can also specify an array of [cascade options](#cascade-options).
- `onDelete: "RESTRICT"|"CASCADE"|"SET NULL"` (default: `RESTRICT`) - specifies how foreign key should behave when referenced object is deleted
- `nullable: boolean` (default: `true`) - Indicates whether this relation's column is nullable or not. By default it is nullable.
- `orphanedRowAction: "nullify" | "delete" | "soft-delete" | "disable"` (default: `disable`) - When a parent is saved (cascading enabled) without a child/children that still exists in database, this will control what shall happen to them.
  - *delete* will remove these children from database.
  - *soft-delete* will mark children as soft-deleted.
  - *nullify* will remove the relation key.
  - *disable* will keep the relation intact. To delete, one has to use their own repository.

## Cascades​

Cascades example:

```
import { Entity, PrimaryGeneratedColumn, Column, ManyToMany } from "typeorm"import { Question } from "./Question"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @ManyToMany((type) => Question, (question) => question.categories)    questions: Question[]}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"import { Category } from "./Category"@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    @ManyToMany((type) => Category, (category) => category.questions, {        cascade: true,    })    @JoinTable()    categories: Category[]}
```

```
const category1 = new Category()category1.name = "ORMs"const category2 = new Category()category2.name = "Programming"const question = new Question()question.title = "How to ask questions?"question.text = "Where can I ask TypeORM-related questions?"question.categories = [category1, category2]await dataSource.manager.save(question)
```

As you can see in this example we did not call `save` for `category1` and `category2`.
They will be automatically inserted, because we set `cascade` to true.

Keep in mind - great power comes with great responsibility.
Cascades may seem like a good and easy way to work with relations,
but they may also bring bugs and security issues when some undesired object is being saved into the database.
Also, they provide a less explicit way of saving new objects into the database.

### Cascade Options​

The `cascade` option can be set as a `boolean` or an array of cascade options `("insert" | "update" | "remove" | "soft-remove" | "recover")[]`.

It will default to `false`, meaning no cascades. Setting `cascade: true` will enable full cascades. You can also specify options by providing an array.

For example:

```
@Entity(Post)export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string    // Full cascades on categories.    @ManyToMany((type) => PostCategory, {        cascade: true,    })    @JoinTable()    categories: PostCategory[]    // Cascade insert here means if there is a new PostDetails instance set    // on this relation, it will be inserted automatically to the db when you save this Post entity    @ManyToMany((type) => PostDetails, (details) => details.posts, {        cascade: ["insert"],    })    @JoinTable()    details: PostDetails[]    // Cascade update here means if there are changes to an existing PostImage, it    // will be updated automatically to the db when you save this Post entity    @ManyToMany((type) => PostImage, (image) => image.posts, {        cascade: ["update"],    })    @JoinTable()    images: PostImage[]    // Cascade insert & update here means if there are new PostInformation instances    // or an update to an existing one, they will be automatically inserted or updated    // when you save this Post entity    @ManyToMany((type) => PostInformation, (information) => information.posts, {        cascade: ["insert", "update"],    })    @JoinTable()    informations: PostInformation[]}
```

## @JoinColumnoptions​

`@JoinColumn` not only defines which side of the relation contains the join column with a foreign key,
but also allows you to customize join column name and referenced column name.

When we set `@JoinColumn`, it automatically creates a column in the database named `propertyName + referencedColumnName`.
For example:

```
@ManyToOne(type => Category)@JoinColumn() // this decorator is optional for @ManyToOne, but required for @OneToOnecategory: Category;
```

This code will create a `categoryId` column in the database.
If you want to change this name in the database you can specify a custom join column name:

```
@ManyToOne(type => Category)@JoinColumn({ name: "cat_id" })category: Category;
```

Join columns are always a reference to some other columns (using a foreign key).
By default your relation always refers to the primary column of the related entity.
If you want to create relation with other columns of the related entity -
you can specify them in `@JoinColumn` as well:

```
@ManyToOne(type => Category)@JoinColumn({ referencedColumnName: "name" })category: Category;
```

The relation now refers to `name` of the `Category` entity, instead of `id`.
Column name for that relation will become `categoryName`.

You can also join multiple columns. Note that they do not reference the primary column of the related entity by default: you must provide the referenced column name.

```
@ManyToOne(type => Category)@JoinColumn([    { name: "category_id", referencedColumnName: "id" },    { name: "locale_id", referencedColumnName: "locale_id" }])category: Category;
```

## @JoinTableoptions​

`@JoinTable` is used for `many-to-many` relations and describes join columns of the "junction" table.
A junction table is a special separate table created automatically by TypeORM with columns that refer to the related entities.
You can change column names inside junction tables and their referenced columns with `@JoinColumn`:
You can also change the name of the generated "junction" table.

```
@ManyToMany(type => Category)@JoinTable({    name: "question_categories", // table name for the junction table of this relation    joinColumn: {        name: "question",        referencedColumnName: "id"    },    inverseJoinColumn: {        name: "category",        referencedColumnName: "id"    }})categories: Category[];
```

If the destination table has composite primary keys,
then an array of properties must be sent to `@JoinTable`.

---

# Custom repositories

> You can create a custom repository which should contain methods to work with your database.

You can create a custom repository which should contain methods to work with your database.
For example, let's say we want to have a method called `findByName(firstName: string, lastName: string)`
which will search for users by a given first and last names.
The best place for this method is a `Repository`,
so we could call it like `userRepository.findByName(...)`.
You can achieve this using custom repositories.

There are several ways how custom repositories can be created.

- [How to create custom repository](#how-to-create-custom-repository)
- [Using custom repositories in transactions](#using-custom-repositories-in-transactions)

## How to create custom repository?​

It's common practice assigning a repository instance to a globally exported variable,
and use this variable across your app, for example:

```
// user.repository.tsexport const UserRepository = dataSource.getRepository(User)// user.controller.tsexport class UserController {    users() {        return UserRepository.find()    }}
```

In order to extend `UserRepository` functionality you can use `.extend` method of `Repository` class:

```
// user.repository.tsexport const UserRepository = dataSource.getRepository(User).extend({    findByName(firstName: string, lastName: string) {        return this.createQueryBuilder("user")            .where("user.firstName = :firstName", { firstName })            .andWhere("user.lastName = :lastName", { lastName })            .getMany()    },})// user.controller.tsexport class UserController {    users() {        return UserRepository.findByName("Timber", "Saw")    }}
```

## Using custom repositories in transactions​

Transactions have their own scope of execution: they have their own query runner, entity manager and repository instances.
That's why using global (data source's) entity manager and repositories won't work in transactions.
In order to execute queries properly in scope of transaction you **must** use provided entity manager
and its `getRepository` method. In order to use custom repositories within transaction,
you must use `withRepository` method of the provided entity manager instance:

```
await connection.transaction(async (manager) => {    // in transactions you MUST use manager instance provided by a transaction,    // you cannot use global entity managers or repositories,    // because this manager is exclusive and transactional    const userRepository = manager.withRepository(UserRepository)    await userRepository.createAndSave("Timber", "Saw")    const timber = await userRepository.findByName("Timber", "Saw")})
```

---

# EntityManagerAPI

> -   dataSource - The DataSource used by EntityManager.

- `dataSource` - The DataSource used by `EntityManager`.

```
const dataSource = manager.dataSource
```

- `queryRunner` - The query runner used by `EntityManager`.
  Used only in transactional instances of EntityManager.

```
const queryRunner = manager.queryRunner
```

- `transaction` - Provides a transaction where multiple database requests will be executed in a single database transaction.
  Learn more [Transactions](https://typeorm.io/docs/advanced-topics/transactions).

```
await manager.transaction(async (manager) => {    // NOTE: you must perform all database operations using the given manager instance    // it's a special instance of EntityManager working with this transaction    // and don't forget to await things here})
```

- `query` - Executes a raw SQL query.

```
const rawData = await manager.query(`SELECT * FROM USERS`)// You can also use parameters to avoid SQL injection// The syntax differs between the drivers// aurora-mysql, better-sqlite3, capacitor, cordova,// expo, mariadb, mysql, nativescript, react-native,// sap, sqlite, sqljsconst rawData = await manager.query(    "SELECT * FROM USERS WHERE name = ? and age = ?",    ["John", 24],)// aurora-postgres, cockroachdb, postgresconst rawData = await manager.query(    "SELECT * FROM USERS WHERE name = $1 and age = $2",    ["John", 24],)// oracleconst rawData = await manager.query(    "SELECT * FROM USERS WHERE name = :1 and age = :2",    ["John", 24],)// spannerconst rawData = await manager.query(    "SELECT * FROM USERS WHERE name = @param0 and age = @param1",    ["John", 24],)// mssqlconst rawData = await manager.query(    "SELECT * FROM USERS WHERE name = @0 and age = @1",    ["John", 24],)
```

- `sql` - Executes a raw SQL query using template literals.

```
const rawData =    await manager.sql`SELECT * FROM USERS WHERE name = ${"John"} and age = ${24}`
```

Learn more about using the [SQL Tag syntax](https://typeorm.io/docs/guides/sql-tag).

- `createQueryBuilder` - Creates a query builder use to build SQL queries.
  Learn more about [QueryBuilder](https://typeorm.io/docs/query-builder/select-query-builder).

```
const users = await manager    .createQueryBuilder()    .select()    .from(User, "user")    .where("user.name = :name", { name: "John" })    .getMany()
```

- `hasId` - Checks if given entity has its primary column property defined.

```
if (manager.hasId(user)) {    // ... do something}
```

- `getId` - Gets given entity's primary column property value.
  If the entity has composite primary keys then the returned value will be an object with names and values of primary columns.

```
const userId = manager.getId(user) // userId === 1
```

- `create` - Creates a new instance of `User`. Optionally accepts an object literal with user properties
  which will be written into newly created user object.

```
const user = manager.create(User) // same as const user = new User();const user = manager.create(User, {    id: 1,    firstName: "Timber",    lastName: "Saw",}) // same as const user = new User(); user.firstName = "Timber"; user.lastName = "Saw";
```

- `merge` - Merges multiple entities into a single entity.

```
const user = new User()manager.merge(User, user, { firstName: "Timber" }, { lastName: "Saw" }) // same as user.firstName = "Timber"; user.lastName = "Saw";
```

- `preload` - Creates a new entity from the given plain javascript object. If the entity already exist in the database, then
  it loads it (and everything related to it), replaces all values with the new ones from the given object,
  and returns the new entity. The new entity is actually loaded from the database entity with all properties
  replaced from the new object.

```
const partialUser = {    id: 1,    firstName: "Rizzrak",    profile: {        id: 1,    },}const user = await manager.preload(User, partialUser)// user will contain all missing data from partialUser with partialUser property values:// { id: 1, firstName: "Rizzrak", lastName: "Saw", profile: { id: 1, ... } }
```

- `save` - Saves a given entity or array of entities.
  If the entity already exists in the database, then it's updated.
  If the entity does not exist in the database yet, it's inserted.
  It saves all given entities in a single transaction (in the case of entity manager is not transactional).
  Also supports partial updating since all undefined properties are skipped. In order to make a value `NULL`, you must manually set the property to equal `null`.

```
await manager.save(user)await manager.save([category1, category2, category3])
```

- `remove` - Removes a given entity or array of entities.
  It removes all given entities in a single transaction (in the case of entity, manager is not transactional).

```
await manager.remove(user)await manager.remove([category1, category2, category3])
```

- `insert` - Inserts a new entity, or array of entities.

```
await manager.insert(User, {    firstName: "Timber",    lastName: "Timber",})await manager.insert(User, [    {        firstName: "Foo",        lastName: "Bar",    },    {        firstName: "Rizz",        lastName: "Rak",    },])
```

- `update` - Updates entities by entity id, ids or given conditions. Sets fields from supplied partial entity.

```
await manager.update(User, { age: 18 }, { category: "ADULT" })// executes UPDATE user SET category = ADULT WHERE age = 18await manager.update(User, 1, { firstName: "Rizzrak" })// executes UPDATE user SET firstName = Rizzrak WHERE id = 1
```

- `updateAll` - Updates *all* entities of target type (without WHERE clause). Sets fields from supplied partial entity.

```
await manager.updateAll(User, { category: "ADULT" })// executes UPDATE user SET category = ADULT
```

- `upsert` - Inserts a new entity or array of entities unless they already exist in which case they are updated instead. Supported by AuroraDataApi, Cockroach, Mysql, Postgres, and Sqlite database drivers.

When an upsert operation results in an update (due to a conflict), special columns like `@UpdateDateColumn` and `@VersionColumn` are automatically updated to their current values.

```
await manager.upsert(    User,    [        { externalId: "abc123", firstName: "Rizzrak" },        { externalId: "bca321", firstName: "Karzzir" },    ],    ["externalId"],)/** executes *  INSERT INTO user *  VALUES *      (externalId = abc123, firstName = Rizzrak), *      (externalId = cba321, firstName = Karzzir), *  ON CONFLICT (externalId) DO UPDATE firstName = EXCLUDED.firstName **/
```

- `delete` - Deletes entities by entity id, ids or given conditions.

```
await manager.delete(User, 1)await manager.delete(User, [1, 2, 3])await manager.delete(User, { firstName: "Timber" })
```

- `deleteAll` - Deletes *all* entities of target type (without WHERE clause).

```
await manager.deleteAll(User)// executes DELETE FROM user
```

Refer also to the `clear` method, which performs database `TRUNCATE TABLE` operation instead.

- `increment` - Increments some column by provided value of entities that match given options.

```
await manager.increment(User, { firstName: "Timber" }, "age", 3)
```

- `decrement` - Decrements some column by provided value that match given options.

```
await manager.decrement(User, { firstName: "Timber" }, "age", 3)
```

- `exists` - Check whether any entity exists that matches `FindOptions`.

```
const exists = await manager.exists(User, {    where: {        firstName: "Timber",    },})
```

- `existsBy` - Checks whether any entity exists that matches `FindOptionsWhere`.

```
const exists = await manager.existsBy(User, { firstName: "Timber" })
```

- `count` - Counts entities that match `FindOptions`. Useful for pagination.

```
const count = await manager.count(User, {    where: {        firstName: "Timber",    },})
```

- `countBy` - Counts entities that match `FindOptionsWhere`. Useful for pagination.

```
const count = await manager.countBy(User, { firstName: "Timber" })
```

- `find` - Finds entities that match given `FindOptions`.

```
const timbers = await manager.find(User, {    where: {        firstName: "Timber",    },})
```

- `findBy` - Finds entities that match given `FindWhereOptions`.

```
const timbers = await manager.findBy(User, {    firstName: "Timber",})
```

- `findAndCount` - Finds entities that match given `FindOptions`.
  Also counts all entities that match given conditions,
  but ignores pagination settings (from and take options).

```
const [timbers, timbersCount] = await manager.findAndCount(User, {    where: {        firstName: "Timber",    },})
```

- `findAndCountBy` - Finds entities that match given `FindOptionsWhere`.
  Also counts all entities that match given conditions,
  but ignores pagination settings (from and take options).

```
const [timbers, timbersCount] = await manager.findAndCountBy(User, {    firstName: "Timber",})
```

- `findOne` - Finds the first entity that matches given `FindOptions`.

```
const timber = await manager.findOne(User, {    where: {        firstName: "Timber",    },})
```

- `findOneBy` - Finds the first entity that matches given `FindOptionsWhere`.

```
const timber = await manager.findOneBy(User, { firstName: "Timber" })
```

- `findOneOrFail` - Finds the first entity that matches some id or find options.
  Rejects the returned promise if nothing matches.

```
const timber = await manager.findOneOrFail(User, {    where: {        firstName: "Timber",    },})
```

- `findOneByOrFail` - Finds the first entity that matches given `FindOptions`.
  Rejects the returned promise if nothing matches.

```
const timber = await manager.findOneByOrFail(User, { firstName: "Timber" })
```

- `clear` - Clears all the data from the given table (truncates/drops it).

```
await manager.clear(User)
```

- `getRepository` - Gets `Repository` to perform operations on a specific entity.
  Learn more about [Repositories](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

```
const userRepository = manager.getRepository(User)
```

- `getTreeRepository` - Gets `TreeRepository` to perform operations on a specific entity.
  Learn more about [Repositories](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

```
const categoryRepository = manager.getTreeRepository(Category)
```

- `getMongoRepository` - Gets `MongoRepository` to perform operations on a specific entity.
  Learn more about [MongoDB](https://typeorm.io/docs/drivers/mongodb).

```
const userRepository = manager.getMongoRepository(User)
```

- `withRepository` - Gets custom repository instance used in a transaction.
  Learn more about [Custom repositories](https://typeorm.io/docs/working-with-entity-manager/custom-repository).

```
const myUserRepository = manager.withRepository(UserRepository)
```

- `release` - Releases query runner of an entity manager.
  Used only when query runner was created and managed manually.

```
await manager.release()
```
