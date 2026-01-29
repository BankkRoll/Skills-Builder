# Entity Inheritance and more

# Entity Inheritance

> Concrete Table Inheritance

## Concrete Table Inheritance​

You can reduce duplication in your code by using entity inheritance patterns.
The simplest and the most effective is concrete table inheritance.

For example, you have `Photo`, `Question`, `Post` entities:

```
@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    size: string}
```

```
@Entity()export class Question {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    answersCount: number}
```

```
@Entity()export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string    @Column()    viewCount: number}
```

As you can see all those entities have common columns: `id`, `title`, `description`.
To reduce duplication and produce a better abstraction we can create a base class called `Content` for them:

```
export abstract class Content {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string}
```

```
@Entity()export class Photo extends Content {    @Column()    size: string}
```

```
@Entity()export class Question extends Content {    @Column()    answersCount: number}
```

```
@Entity()export class Post extends Content {    @Column()    viewCount: number}
```

All columns (relations, embeds, etc.) from parent entities (parent can extend other entity as well)
will be inherited and created in final entities.

This example will create 3 tables - `photo`, `question` and `post`.

## Single Table Inheritance​

TypeORM also supports single table inheritance.
Single table inheritance is a pattern when you have multiple classes with their own properties,
but in the database they are stored in the same table.

```
@Entity()@TableInheritance({ column: { type: "varchar", name: "type" } })export class Content {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    description: string}
```

```
@ChildEntity()export class Photo extends Content {    @Column()    size: string}
```

```
@ChildEntity()export class Question extends Content {    @Column()    answersCount: number}
```

```
@ChildEntity()export class Post extends Content {    @Column()    viewCount: number}
```

This will create a single table called `content` and all instances of photos, questions and posts
will be saved into this table.

## Using embeddeds​

There is an amazing way to reduce duplication in your app (using composition over inheritance) by using `embedded columns`.
Read more about embedded entities [here](https://typeorm.io/docs/entity/embedded-entities).

---

# Separating Entity Definition

> Defining Schemas

## Defining Schemas​

You can define an entity and its columns right in the model, using decorators.
But some people prefer to define an entity and its columns inside separate files
which are called "entity schemas" in TypeORM.

Simple definition example:

```
import { EntitySchema } from "typeorm"export const CategoryEntity = new EntitySchema({    name: "category",    columns: {        id: {            type: Number,            primary: true,            generated: true,        },        name: {            type: String,        },    },})
```

Example with relations:

```
import { EntitySchema } from "typeorm"export const PostEntity = new EntitySchema({    name: "post",    columns: {        id: {            type: Number,            primary: true,            generated: true,        },        title: {            type: String,        },        text: {            type: String,        },    },    relations: {        categories: {            type: "many-to-many",            target: "category", // CategoryEntity        },    },})
```

Complex example:

```
import { EntitySchema } from "typeorm"export const PersonSchema = new EntitySchema({    name: "person",    columns: {        id: {            primary: true,            type: "int",            generated: "increment",        },        firstName: {            type: String,            length: 30,        },        lastName: {            type: String,            length: 50,            nullable: false,        },        age: {            type: Number,            nullable: false,        },        countryCode: {            type: String,            length: 2,            foreignKey: {                target: "countries", // CountryEntity                inverseSide: "code",            },        },        cityId: {            type: Number,            foreignKey: {                target: "cities", // CityEntity            },        },    },    checks: [        { expression: `"firstName" <> 'John' AND "lastName" <> 'Doe'` },        { expression: `"age" > 18` },    ],    indices: [        {            name: "IDX_TEST",            unique: true,            columns: ["firstName", "lastName"],        },    ],    uniques: [        {            name: "UNIQUE_TEST",            columns: ["firstName", "lastName"],        },    ],    foreignKeys: [        {            target: "cities", // CityEntity            columnNames: ["cityId", "countryCode"],            referencedColumnNames: ["id", "countryCode"],        },    ],})
```

If you want to make your entity typesafe, you can define a model and specify it in schema definition:

```
import { EntitySchema } from "typeorm"export interface Category {    id: number    name: string}export const CategoryEntity = new EntitySchema<Category>({    name: "category",    columns: {        id: {            type: Number,            primary: true,            generated: true,        },        name: {            type: String,        },    },})
```

## Extending Schemas​

When using the `Decorator` approach it is easy to `extend` basic columns to an abstract class and simply extend this.
For example, your `id`, `createdAt` and `updatedAt` columns may be defined in such a `BaseEntity`. For more details, see
the documentation on [concrete table inheritance](https://typeorm.io/docs/entity/entity-inheritance#concrete-table-inheritance).

When using the `EntitySchema` approach, this is not possible. However, you can use the `Spread Operator` (`...`) to your
advantage.

Reconsider the `Category` example from above. You may want to `extract` basic column descriptions and reuse it across
your other schemas. This may be done in the following way:

```
import { EntitySchemaColumnOptions } from "typeorm"export const BaseColumnSchemaPart = {    id: {        type: Number,        primary: true,        generated: true,    } as EntitySchemaColumnOptions,    createdAt: {        name: "created_at",        type: "timestamp with time zone",        createDate: true,    } as EntitySchemaColumnOptions,    updatedAt: {        name: "updated_at",        type: "timestamp with time zone",        updateDate: true,    } as EntitySchemaColumnOptions,}
```

Now you can use the `BaseColumnSchemaPart` in your other schema models, like this:

```
export const CategoryEntity = new EntitySchema<Category>({    name: "category",    columns: {        ...BaseColumnSchemaPart,        // the CategoryEntity now has the defined id, createdAt, updatedAt columns!        // in addition, the following NEW fields are defined        name: {            type: String,        },    },})
```

You can use embedded entities in schema models, like this:

```
export interface Name {    first: string    last: string}export const NameEntitySchema = new EntitySchema<Name>({    name: "name",    columns: {        first: {            type: "varchar",        },        last: {            type: "varchar",        },    },})export interface User {    id: string    name: Name    isActive: boolean}export const UserEntitySchema = new EntitySchema<User>({    name: "user",    columns: {        id: {            primary: true,            generated: "uuid",            type: "uuid",        },        isActive: {            type: "boolean",        },    },    embeddeds: {        name: {            schema: NameEntitySchema,            prefix: "name_",        },    },})
```

Be sure to add the `extended` columns also to the `Category` interface (e.g., via `export interface Category extend BaseEntity`).

### Single Table Inheritance​

In order to use [Single Table Inheritance](https://typeorm.io/docs/entity/entity-inheritance#single-table-inheritance):

1. Add the `inheritance` option to the **parent** class schema, specifying the inheritance pattern ("STI") and the
  **discriminator** column, which will store the name of the *child* class on each row
2. Set the `type: "entity-child"` option for all **children** classes' schemas, while extending the *parent* class
  columns using the spread operator syntax described above

```
// entity.tsexport abstract class Base {    id!: number    type!: string    createdAt!: Date    updatedAt!: Date}export class A extends Base {    constructor(public a: boolean) {        super()    }}export class B extends Base {    constructor(public b: number) {        super()    }}export class C extends Base {    constructor(public c: string) {        super()    }}
```

```
// schema.tsconst BaseSchema = new EntitySchema<Base>({    target: Base,    name: "Base",    columns: {        id: {            type: Number,            primary: true,            generated: "increment",        },        type: {            type: String,        },        createdAt: {            type: Date,            createDate: true,        },        updatedAt: {            type: Date,            updateDate: true,        },    },    // NEW: Inheritance options    inheritance: {        pattern: "STI",        column: "type",    },})const ASchema = new EntitySchema<A>({    target: A,    name: "A",    type: "entity-child",    // When saving instances of 'A', the "type" column will have the value    // specified on the 'discriminatorValue' property    discriminatorValue: "my-custom-discriminator-value-for-A",    columns: {        ...BaseSchema.options.columns,        a: {            type: Boolean,        },    },})const BSchema = new EntitySchema<B>({    target: B,    name: "B",    type: "entity-child",    discriminatorValue: undefined, // Defaults to the class name (e.g. "B")    columns: {        ...BaseSchema.options.columns,        b: {            type: Number,        },    },})const CSchema = new EntitySchema<C>({    target: C,    name: "C",    type: "entity-child",    discriminatorValue: "my-custom-discriminator-value-for-C",    columns: {        ...BaseSchema.options.columns,        c: {            type: String,        },    },})
```

## Using Schemas to Query / Insert Data​

Of course, you can use the defined schemas in your repositories or entity manager as you would use the decorators.
Consider the previously defined `Category` example (with its `Interface` and `CategoryEntity` schema) in order to get
some data or manipulate the database.

```
// request dataconst categoryRepository = dataSource.getRepository<Category>(CategoryEntity)const category = await categoryRepository.findOneBy({    id: 1,}) // category is properly typed!// insert a new category into the databaseconst categoryDTO = {    // note that the ID is autogenerated; see the schema above    name: "new category",}const newCategory = await categoryRepository.save(categoryDTO)
```

---

# Tree Entities

> TypeORM supports the Adjacency list and Closure table patterns for storing tree structures.

TypeORM supports the Adjacency list and Closure table patterns for storing tree structures.
To learn more about the hierarchy table take a look at [this awesome presentation by Bill Karwin](https://www.slideshare.net/billkarwin/models-for-hierarchical-data).

## Adjacency list​

Adjacency list is a simple model with self-referencing.
Note that TreeRepository doesn't support Adjacency list.
The benefit of this approach is simplicity,
a drawback is that you can't load big trees all at once because of join limitations.
To learn more about the benefits and use of Adjacency Lists look at [this article by Matthew Schinckel](http://schinckel.net/2014/09/13/long-live-adjacency-lists/).
Example:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    ManyToOne,    OneToMany,} from "typeorm"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column()    description: string    @ManyToOne((type) => Category, (category) => category.children)    parent: Category    @OneToMany((type) => Category, (category) => category.parent)    children: Category[]}
```

## Nested set​

Nested set is another pattern of storing tree structures in the database.
It is very efficient for reads, but bad for writes.
You cannot have multiple roots in the nested set.
Example:

```
import {    Entity,    Tree,    Column,    PrimaryGeneratedColumn,    TreeChildren,    TreeParent,    TreeLevelColumn,} from "typeorm"@Entity()@Tree("nested-set")export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @TreeChildren()    children: Category[]    @TreeParent()    parent: Category}
```

## Materialized Path (aka Path Enumeration)​

Materialized Path (also called Path Enumeration) is another pattern of storing tree structures in the database.
It is simple and effective.
Example:

```
import {    Entity,    Tree,    Column,    PrimaryGeneratedColumn,    TreeChildren,    TreeParent,    TreeLevelColumn,} from "typeorm"@Entity()@Tree("materialized-path")export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @TreeChildren()    children: Category[]    @TreeParent()    parent: Category}
```

## Closure table​

Closure table stores relations between parent and child in a separate table in a special way.
It's efficient in both reading and writing.
Example:

```
import {    Entity,    Tree,    Column,    PrimaryGeneratedColumn,    TreeChildren,    TreeParent,    TreeLevelColumn,} from "typeorm"@Entity()@Tree("closure-table")export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @TreeChildren()    children: Category[]    @TreeParent()    parent: Category}
```

You can specify the closure table name and/or closure table column names by setting optional parameter `options` into `@Tree("closure-table", options)`. `ancestorColumnName` and `descandantColumnName` are callback functions, which receive the primary column's metadata and return the column's name.

```
@Tree("closure-table", {    closureTableName: "category_closure",    ancestorColumnName: (column) => "ancestor_" + column.propertyName,    descendantColumnName: (column) => "descendant_" + column.propertyName,})
```

## Working with tree entities​

To bind tree entities to each other, it is required to set the parent in the child entity and then save them.
for example:

```
const a1 = new Category()a1.name = "a1"await dataSource.manager.save(a1)const a11 = new Category()a11.name = "a11"a11.parent = a1await dataSource.manager.save(a11)const a12 = new Category()a12.name = "a12"a12.parent = a1await dataSource.manager.save(a12)const a111 = new Category()a111.name = "a111"a111.parent = a11await dataSource.manager.save(a111)const a112 = new Category()a112.name = "a112"a112.parent = a11await dataSource.manager.save(a112)
```

To load such a tree use `TreeRepository`:

```
const trees = await dataSource.manager.getTreeRepository(Category).findTrees()
```

`trees` will be the following:

```
[    {        "id": 1,        "name": "a1",        "children": [            {                "id": 2,                "name": "a11",                "children": [                    {                        "id": 4,                        "name": "a111"                    },                    {                        "id": 5,                        "name": "a112"                    }                ]            },            {                "id": 3,                "name": "a12"            }        ]    }]
```

There are other special methods to work with tree entities through `TreeRepository`:

- `findTrees` - Returns all trees in the database with all their children, children of children, etc.

```
const treeCategories = await dataSource.manager    .getTreeRepository(Category)    .findTrees()// returns root categories with sub categories insideconst treeCategoriesWithLimitedDepth = await dataSource.manager    .getTreeRepository(Category)    .findTrees({ depth: 2 })// returns root categories with sub categories inside, up to depth 2
```

- `findRoots` - Roots are entities that have no ancestors. Finds them all.
  Does not load children's leaves.

```
const rootCategories = await dataSource.manager    .getTreeRepository(Category)    .findRoots()// returns root categories without sub categories inside
```

- `findDescendants` - Gets all children (descendants) of the given entity. Returns them all in a flat array.

```
const children = await dataSource.manager    .getTreeRepository(Category)    .findDescendants(parentCategory)// returns all direct subcategories (without its nested categories) of a parentCategory
```

- `findDescendantsTree` - Gets all children (descendants) of the given entity. Returns them in a tree - nested into each other.

```
const childrenTree = await repository.findDescendantsTree(parentCategory)// returns all direct subcategories (with its nested categories) of a parentCategoryconst childrenTreeWithLimitedDepth = await repository.findDescendantsTree(    parentCategory,    { depth: 2 },)// returns all direct subcategories (with its nested categories) of a parentCategory, up to depth 2
```

- `createDescendantsQueryBuilder` - Creates a query builder used to get descendants of the entities in a tree.

```
const children = await repository    .createDescendantsQueryBuilder(        "category",        "categoryClosure",        parentCategory,    )    .andWhere("category.type = 'secondary'")    .getMany()
```

- `countDescendants` - Gets the number of descendants of the entity.

```
const childrenCount = await dataSource.manager    .getTreeRepository(Category)    .countDescendants(parentCategory)
```

- `findAncestors` - Gets all parents (ancestors) of the given entity. Returns them all in a flat array.

```
const parents = await repository.findAncestors(childCategory)// returns all direct childCategory's parent categories (without "parent of parents")
```

- `findAncestorsTree` - Gets all parents (ancestors) of the given entity. Returns them in a tree - nested into each other.

```
const parentsTree = await dataSource.manager    .getTreeRepository(Category)    .findAncestorsTree(childCategory)// returns all direct childCategory's parent categories (with "parent of parents")
```

- `createAncestorsQueryBuilder` - Creates a query builder used to get the ancestors of the entities in a tree.

```
const parents = await repository    .createAncestorsQueryBuilder("category", "categoryClosure", childCategory)    .andWhere("category.type = 'secondary'")    .getMany()
```

- `countAncestors` - Gets the number of ancestors of the entity.

```
const parentsCount = await dataSource.manager    .getTreeRepository(Category)    .countAncestors(childCategory)
```

For the following methods, options can be passed:

- findTrees
- findRoots
- findDescendants
- findDescendantsTree
- findAncestors
- findAncestorsTree

The following options are available:

- `relations` - Indicates what relations of entity should be loaded (simplified left join form).

Examples:

```
const treeCategoriesWithRelations = await dataSource.manager    .getTreeRepository(Category)    .findTrees({        relations: ["sites"],    })// automatically joins the sites relationconst parentsWithRelations = await dataSource.manager    .getTreeRepository(Category)    .findAncestors(childCategory, {        relations: ["members"],    })// returns all direct childCategory's parent categories (without "parent of parents") and joins the 'members' relation
```

---

# View Entities

> What is a ViewEntity?

## What is a ViewEntity?​

View entity is a class that maps to a database view.
You can create a view entity by defining a new class and mark it with `@ViewEntity()`:

`@ViewEntity()` accepts following options:

- `name` - view name. If not specified, then view name is generated from entity class name.
- `database` - database name in selected DB server.
- `schema` - schema name.
- `expression` - view definition. **Required parameter**.
- `dependsOn` - List of other views on which the current views depends. If your view uses another view in its definition, you can add it here so that [migrations](https://typeorm.io/docs/migrations/why) are generated in the correct order.

`expression` can be string with properly escaped columns and tables, depend on database used (postgres in example):

```
@ViewEntity({    expression: `        SELECT "post"."id" AS "id", "post"."name" AS "name", "category"."name" AS "categoryName"        FROM "post" "post"        LEFT JOIN "category" "category" ON "post"."categoryId" = "category"."id"    `})
```

or an instance of QueryBuilder

```
@ViewEntity({    expression: (dataSource: DataSource) => dataSource        .createQueryBuilder()        .select("post.id", "id")        .addSelect("post.name", "name")        .addSelect("category.name", "categoryName")        .from(Post, "post")        .leftJoin(Category, "category", "category.id = post.categoryId")})
```

**Note:** parameter binding is not supported due to drivers limitations. Use the literal parameters instead.

```
@ViewEntity({    expression: (dataSource: DataSource) => dataSource        .createQueryBuilder()        .select("post.id", "id")        .addSelect("post.name", "name")        .addSelect("category.name", "categoryName")        .from(Post, "post")        .leftJoin(Category, "category", "category.id = post.categoryId")        .where("category.name = :name", { name: "Cars" })  // <-- this is wrong        .where("category.name = 'Cars'")                   // <-- and this is right})
```

Each view entity must be registered in your data source options:

```
import { DataSource } from "typeorm"import { UserView } from "./entity/UserView"const dataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    entities: [UserView],})
```

## View Entity columns​

To map data from view into the correct entity columns you must mark entity columns with `@ViewColumn()`
decorator and specify these columns as select statement aliases.

example with string expression definition:

```
import { ViewEntity, ViewColumn } from "typeorm"@ViewEntity({    expression: `        SELECT "post"."id" AS "id", "post"."name" AS "name", "category"."name" AS "categoryName"        FROM "post" "post"        LEFT JOIN "category" "category" ON "post"."categoryId" = "category"."id"    `,})export class PostCategory {    @ViewColumn()    id: number    @ViewColumn()    name: string    @ViewColumn()    categoryName: string}
```

example using QueryBuilder:

```
import { ViewEntity, ViewColumn } from "typeorm"@ViewEntity({    expression: (dataSource: DataSource) =>        dataSource            .createQueryBuilder()            .select("post.id", "id")            .addSelect("post.name", "name")            .addSelect("category.name", "categoryName")            .from(Post, "post")            .leftJoin(Category, "category", "category.id = post.categoryId"),})export class PostCategory {    @ViewColumn()    id: number    @ViewColumn()    name: string    @ViewColumn()    categoryName: string}
```

## View Column options​

View Column options define additional options for your view entity columns, similar to [column options](https://typeorm.io/docs/entity/entities#column-options) for regular entities.

You can specify view column options in `@ViewColumn`:

```
@ViewColumn({    name: "postName",    // ...})name: string;
```

List of available options in `ViewColumnOptions`:

- `name: string` - Column name in the database view.
- `transformer: { from(value: DatabaseType): EntityType, to(value: EntityType): DatabaseType }` - Used to unmarshal properties of arbitrary type `DatabaseType` supported by the database into a type `EntityType`. Arrays of transformers are also supported and are applied in reverse order when reading. Note that because database views are read-only, `transformer.to(value)` will never be used.

## Materialized View Indices​

There's support for creation of indices for materialized views if using `PostgreSQL`.

```
@ViewEntity({    materialized: true,    expression: (dataSource: DataSource) =>        dataSource            .createQueryBuilder()            .select("post.id", "id")            .addSelect("post.name", "name")            .addSelect("category.name", "categoryName")            .from(Post, "post")            .leftJoin(Category, "category", "category.id = post.categoryId"),})export class PostCategory {    @ViewColumn()    id: number    @Index()    @ViewColumn()    name: string    @Index("catname-idx")    @ViewColumn()    categoryName: string}
```

However, `unique` is currently the only supported option for indices in materialized views. The rest of the indices options will be ignored.

```
@Index("name-idx", { unique: true })@ViewColumn()name: string
```

## Complete example​

Lets create two entities and a view containing aggregated data from these entities:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class Category {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string}
```

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToOne,    JoinColumn,} from "typeorm"import { Category } from "./Category"@Entity()export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column()    categoryId: number    @ManyToOne(() => Category)    @JoinColumn({ name: "categoryId" })    category: Category}
```

```
import { ViewEntity, ViewColumn, DataSource } from "typeorm"@ViewEntity({    expression: (dataSource: DataSource) =>        dataSource            .createQueryBuilder()            .select("post.id", "id")            .addSelect("post.name", "name")            .addSelect("category.name", "categoryName")            .from(Post, "post")            .leftJoin(Category, "category", "category.id = post.categoryId"),})export class PostCategory {    @ViewColumn()    id: number    @ViewColumn()    name: string    @ViewColumn()    categoryName: string}
```

then fill these tables with data and request all data from PostCategory view:

```
import { Category } from "./entity/Category"import { Post } from "./entity/Post"import { PostCategory } from "./entity/PostCategory"const category1 = new Category()category1.name = "Cars"await dataSource.manager.save(category1)const category2 = new Category()category2.name = "Airplanes"await dataSource.manager.save(category2)const post1 = new Post()post1.name = "About BMW"post1.categoryId = category1.idawait dataSource.manager.save(post1)const post2 = new Post()post2.name = "About Boeing"post2.categoryId = category2.idawait dataSource.manager.save(post2)const postCategories = await dataSource.manager.find(PostCategory)const postCategory = await dataSource.manager.findOneBy(PostCategory, { id: 1 })
```

the result in `postCategories` will be:

```
[ PostCategory { id: 1, name: 'About BMW', categoryName: 'Cars' },  PostCategory { id: 2, name: 'About Boeing', categoryName: 'Airplanes' } ]
```

and in `postCategory`:

```
PostCategory { id: 1, name: 'About BMW', categoryName: 'Cars' }
```

---

# The Future of TypeORM

> By David Hoeck (@dlhck) and Michael Bromley (@michaelbromley)

> By [David Hoeck (@dlhck)](https://github.com/dlhck) and [Michael Bromley (@michaelbromley)](https://github.com/michaelbromley)

TypeORM is one of the most high-performance, feature-rich, and battle-tested ORMs in the Node.js ecosystem, relied upon by hundreds of thousands of projects and companies worldwide. With nearly 2 million downloads each week, it powers countless applications as a critical dependency. However, over the past few years, maintenance has slowed significantly, leading to growing uncertainty about the project's future among its dedicated community.

We're thrilled to announce that Michael Bromley and David Hoeck, under the umbrella of our parent company [Elevantiq](https://elevantiq.com/), are
stepping up to lead TypeORM into its next chapter. At Elevantiq, where we
specialize in enterprise digital commerce solutions, TypeORM is a critical dependency—not
only for [Vendure](https://vendure.io/), our flagship open-source project, but also for many of our other solutions.
With our reliance on TypeORM and the growing needs of its vibrant community, we saw an
opportunity to contribute back and ensure the project remains active, maintained, and secure.

After discussions with TypeORM's original maintainers, Umed and Dmitry, we've reached an agreement to take on the project's maintenance, inspired by successful, community-centric open-source projects. One standout model is [the Tauri project](https://github.com/tauri-apps/tauri), a self-governing open-source initiative co-founded by [Daniel](https://github.com/denjell-crabnebula), who we already collaborate with through Michael and Vendure. Our discussions with Tauri have set the foundation for the organizational structure we envision.

## Our Vision for TypeORM's Future​

To ensure long-term stability and governance, we plan to establish a non-profit
foundation for TypeORM, likely under the [Commons Conservancy](https://commonsconservancy.org/) in the Netherlands.
This foundation will be led by a board of seven members: Michael and David,
along with five additional board members dedicated to the project's success.
The board will work closely with a **Working Group** comprising companies, contributors,
and other community members who heavily rely on TypeORM. This collaborative setup will help guide
strategic decisions that align with the needs and goals of TypeORM's ecosystem.

## Organizational Structure​

To drive TypeORM forward, we'll introduce three core domains:

- **Development**: Led by core developers with expertise across various database engines and adapters, this team will focus on TypeORM's architecture and ongoing technical maintenance and advancements.
- **Operations**: Handling day-to-day needs, from documentation to sponsorship accounting, this team will keep the project running smoothly.
- **Community**: Dedicated to engaging, moderating, and supporting our growing community, this team will foster collaboration through platforms like Discord.

## Scaling Sponsorships and Full-Time Development​

A significant part of our strategy is to increase sponsorships, reaching out to
companies and collaborating with organizations like [OSS Pledge](https://opensourcepledge.com/). Our goal is to fund and
employ two full-time developers who will lead the Development team, ensuring ongoing progress
and project maintenance.

We're confident that, with this structure, we can build a sustainable future for TypeORM. But the
*success of this vision depends on the support of the community*.
We'll also remain in close contact with [Umed](https://github.com/pleerock) to keep his insights and vision connected to the project's evolution.

## Join Us in Supporting TypeORM​

If your company is interested in starting or expanding its sponsorship with TypeORM, we encourage you to reach out to us directly [via e-mail](mailto:typeorm@elevantiq.com).

Thank you for your support, and we're excited to embark on this journey with the TypeORM community!

---

## Join the Conversation​

Have questions or want to get involved? Join our [Discord community](https://discord.gg/cC9hkmUgNa) or check out our [GitHub repository](https://github.com/typeorm/typeorm).
