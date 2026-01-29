# Getting Started and more

# Getting Started

> TypeORM is an ORM

TypeORM is an [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping)
that can run in Node.js, Browser, Cordova, Ionic, React Native, NativeScript, Expo, and Electron platforms
and can be used with TypeScript and JavaScript (ES2021).

Its goal is to always support the latest JavaScript features and provide additional features
that help you to develop any kind of application that uses databases - from
small applications with a few tables to large-scale enterprise applications
with multiple databases.

TypeORM supports more databases than any other JS/TS ORM: [Google Spanner](https://typeorm.io/docs/drivers/google-spanner), [Microsoft SqlServer](https://typeorm.io/docs/drivers/microsoft-sqlserver), [MongoDB](https://typeorm.io/docs/drivers/mongodb), [MySQL/MariaDB](https://typeorm.io/docs/drivers/mysql), [Oracle](https://typeorm.io/docs/drivers/oracle), [Postgres](https://typeorm.io/docs/drivers/postgres), [SAP HANA](https://typeorm.io/docs/drivers/sap) and [SQLite](https://typeorm.io/docs/drivers/sqlite), as well we derived databases and different drivers.

TypeORM supports both [Active Record](https://typeorm.io/docs/guides/active-record-data-mapper#what-is-the-active-record-pattern) and [Data Mapper](https://typeorm.io/docs/guides/active-record-data-mapper#what-is-the-data-mapper-pattern) patterns,
unlike all other JavaScript ORMs currently in existence,
which means you can write high-quality, loosely coupled, scalable,
maintainable applications in the most productive way.

TypeORM is highly influenced by other ORMs, such as [Hibernate](http://hibernate.org/orm/),
[Doctrine](http://www.doctrine-project.org/) and [Entity Framework](https://www.asp.net/entity-framework).

## Features​

- Supports both [DataMapper](https://typeorm.io/docs/guides/active-record-data-mapper#what-is-the-data-mapper-pattern) and [ActiveRecord](https://typeorm.io/docs/guides/active-record-data-mapper#what-is-the-active-record-pattern) (your choice).
- Entities and columns.
- Database-specific column types.
- Entity manager.
- Repositories and custom repositories.
- Clean object-relational model.
- Associations (relations).
- Eager and lazy relations.
- Unidirectional, bidirectional, and self-referenced relations.
- Supports multiple inheritance patterns.
- Cascades.
- Indices.
- Transactions.
- [Migrations](https://typeorm.io/docs/migrations/why) with automatic generation.
- Connection pooling.
- Replication.
- Using multiple database instances.
- Working with multiple database types.
- Cross-database and cross-schema queries.
- Elegant-syntax, flexible and powerful QueryBuilder.
- Left and inner joins.
- Proper pagination for queries using joins.
- Query caching.
- Streaming raw results.
- Logging.
- Listeners and subscribers (hooks).
- Supports closure table pattern.
- Schema declaration in models or separate configuration files.
- Supports MySQL / MariaDB / Postgres / CockroachDB / SQLite / Microsoft SQL Server / Oracle / SAP Hana / sql.js.
- Supports MongoDB NoSQL database.
- Works in Node.js / Browser / Ionic / Cordova / React Native / NativeScript / Expo / Electron platforms.
- TypeScript and JavaScript support.
- ESM and CommonJS support.
- Produced code is performant, flexible, clean, and maintainable.
- Follows all possible best practices.
- CLI.

And more...

With TypeORM, your models look like this:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    age: number}
```

And your domain logic looks like this:

```
const userRepository = AppDataSource.getRepository(User)const user = new User()user.firstName = "Timber"user.lastName = "Saw"user.age = 25await userRepository.save(user)const allUsers = await userRepository.find()const firstUser = await userRepository.findOneBy({    id: 1,}) // find by idconst timber = await userRepository.findOneBy({    firstName: "Timber",    lastName: "Saw",}) // find by firstName and lastNameawait userRepository.remove(timber)
```

Alternatively, if you prefer to use the `ActiveRecord` implementation, you can use it as well:

```
import { Entity, PrimaryGeneratedColumn, Column, BaseEntity } from "typeorm"@Entity()export class User extends BaseEntity {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    age: number}
```

And your domain logic will look this way:

```
const user = new User()user.firstName = "Timber"user.lastName = "Saw"user.age = 25await user.save()const allUsers = await User.find()const firstUser = await User.findOneBy({    id: 1,})const timber = await User.findOneBy({    firstName: "Timber",    lastName: "Saw",})await timber.remove()
```

## Installation​

1. Install the npm package:
  `npm install typeorm`
2. You need to install `reflect-metadata` shim:
  `npm install reflect-metadata`
  and import it somewhere in the global place of your app (for example in `app.ts`):
  `import "reflect-metadata"`
3. You may need to install node typings:
  `npm install @types/node --save-dev`
4. Install a database driver: see the documentation for each particular driver: [mongodb](https://typeorm.io/docs/drivers/mongodb#installation), [mssql](https://typeorm.io/docs/drivers/microsoft-sqlserver#installation), [mysql/mariadb](https://typeorm.io/docs/drivers/mysql#installation), [oracle](https://typeorm.io/docs/drivers/oracle#installation), [postgres](https://typeorm.io/docs/drivers/postgres#installation), [sap](https://typeorm.io/docs/drivers/sap#installation), [spanner](https://typeorm.io/docs/drivers/google-spanner#installation), [sqlite](https://typeorm.io/docs/drivers/sqlite#installation).

### TypeScript configuration​

Also, make sure you are using TypeScript version **4.5** or higher,
and you have enabled the following settings in `tsconfig.json`:

```
"emitDecoratorMetadata": true,"experimentalDecorators": true,
```

## Quick Start​

The quickest way to get started with TypeORM is to use its CLI commands to generate a starter project.
Quick start works only if you are using TypeORM in a Node.js application.
If you are using other platforms, proceed to the [step-by-step guide](#step-by-step-guide).

To create a new project using CLI, run the following command:

```
npx typeorm init --name MyProject --database postgres
```

Where `name` is the name of your project and `database` is the database you'll use.
Database can be one of the following values: `mysql`, `mariadb`, `postgres`, `cockroachdb`, `sqlite`, `mssql`, `sap`, `spanner`, `oracle`, `mongodb`,
`cordova`, `react-native`, `expo`, `nativescript`.

This command will generate a new project in the `MyProject` directory with the following files:

```
MyProject├── src                   // place of your TypeScript code│   ├── entity            // place where your entities (database models) are stored│   │   └── User.ts       // sample entity│   ├── migration         // place where your migrations are stored│   ├── data-source.ts    // data source and all connection configuration│   └── index.ts          // start point of your application├── .gitignore            // standard gitignore file├── package.json          // node module dependencies├── README.md             // simple readme file└── tsconfig.json         // TypeScript compiler options
```

> You can also run `typeorm init` on an existing node project, but be careful - it may override some files you already have.

The next step is to install new project dependencies:

```
cd MyProjectnpm install
```

After you have all dependencies installed, edit the `data-source.ts` file and put your own database connection configuration options in there:

```
export const AppDataSource = new DataSource({    type: "postgres",    host: "localhost",    port: 5432,    username: "test",    password: "test",    database: "test",    synchronize: true,    logging: true,    entities: [Post, Category],    subscribers: [],    migrations: [],})
```

Particularly, most of the time you'll only need to configure
`host`, `username`, `password`, `database` and maybe `port` options.

Once you finish with configuration and all node modules are installed, you can run your application:

```
npm start
```

That's it, your application should successfully run and insert a new user into the database.
You can continue to work with this project and integrate other modules you need and start
creating more entities.

> You can generate an ESM project by running
> `npx typeorm init --name MyProject --database postgres --module esm` command.

> You can generate an even more advanced project with express installed by running
> `npx typeorm init --name MyProject --database mysql --express` command.

> You can generate a docker-compose file by running
> `npx typeorm init --name MyProject --database postgres --docker` command.

## Step-by-Step Guide​

What are you expecting from ORM?
First, you are expecting it will create database tables for you
and find / insert / update / delete your data without the pain of
having to write lots of hardly maintainable SQL queries.
This guide will show you how to set up TypeORM from scratch and make it do what you are expecting from an ORM.

### Create a model​

Working with a database starts with creating tables.
How do you tell TypeORM to create a database table?
The answer is - through the models.
Your models in your app are your database tables.

For example, you have a `Photo` model:

```
export class Photo {    id: number    name: string    description: string    filename: string    views: number    isPublished: boolean}
```

And you want to store photos in your database.
To store things in the database, first, you need a database table,
and database tables are created from your models.
Not all models, but only those you define as *entities*.

### Create an entity​

*Entity* is your model decorated by an `@Entity` decorator.
A database table will be created for such models.
You work with entities everywhere in TypeORM.
You can load/insert/update/remove and perform other operations with them.

Let's make our `Photo` model an entity:

```
import { Entity } from "typeorm"@Entity()export class Photo {    id: number    name: string    description: string    filename: string    views: number    isPublished: boolean}
```

Now, a database table will be created for the `Photo` entity, and we'll be able to work with it anywhere in our app.
We have created a database table, however, what table can exist without columns?
Let's create a few columns in our database table.

### Adding table columns​

To add database columns, you need to decorate an entity's properties you want to make into a column
with a `@Column` decorator.

```
import { Entity, Column } from "typeorm"@Entity()export class Photo {    @Column()    id: number    @Column()    name: string    @Column()    description: string    @Column()    filename: string    @Column()    views: number    @Column()    isPublished: boolean}
```

Now `id`, `name`, `description`, `filename`, `views`, and `isPublished` columns will be added to the `photo` table.
Column types in the database are inferred from the property types you used, e.g.
`number` will be converted into `integer`, `string` into `varchar`, `boolean` into `bool`, etc.
But you can use any column type your database supports by explicitly specifying a column type into the `@Column` decorator.

We generated a database table with columns, but there is one thing left.
Each database table must have a column with a primary key.

### Creating a primary column​

Each entity **must** have at least one primary key column.
This is a requirement, and you can't avoid it.
To make a column a primary key, you need to use the `@PrimaryColumn` decorator.

```
import { Entity, Column, PrimaryColumn } from "typeorm"@Entity()export class Photo {    @PrimaryColumn()    id: number    @Column()    name: string    @Column()    description: string    @Column()    filename: string    @Column()    views: number    @Column()    isPublished: boolean}
```

### Creating an auto-generated column​

Now, let's say you want your id column to be auto-generated (this is known as auto-increment / sequence / serial / generated identity column).
To do that, you need to change the `@PrimaryColumn` decorator to a `@PrimaryGeneratedColumn` decorator:

```
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm"@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @Column()    description: string    @Column()    filename: string    @Column()    views: number    @Column()    isPublished: boolean}
```

### Column data types​

Next, let's fix our data types. By default, the string is mapped to a varchar(255)-like type (depending on the database type).
The number is mapped to an integer-like type (depending on the database type).
We don't want all our columns to be limited to varchars or integers.
Let's set up the correct data types:

```
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm"@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column({        length: 100,    })    name: string    @Column("text")    description: string    @Column()    filename: string    @Column("double")    views: number    @Column()    isPublished: boolean}
```

Column types are database-specific.
You can set any column type your database supports.
More information on supported column types can be found [here](https://typeorm.io/docs/entity/entities#column-types).

### Creating a newDataSource​

Now, when our entity is created, let's create `index.ts` file and set up our `DataSource` there:

```
import "reflect-metadata"import { DataSource } from "typeorm"import { Photo } from "./entity/Photo"const AppDataSource = new DataSource({    type: "postgres",    host: "localhost",    port: 5432,    username: "root",    password: "admin",    database: "test",    entities: [Photo],    synchronize: true,    logging: false,})// to initialize the initial connection with the database, register all entities// and "synchronize" database schema, call "initialize()" method of a newly created database// once in your application bootstraptry {    await AppDataSource.initialize()} catch (error) {    console.log(error)}
```

We are using Postgres in this example, but you can use any other supported database.
To use another database, change the `type` in the options to the database type you are using:
`mysql`, `mariadb`, `postgres`, `cockroachdb`, `sqlite`, `mssql`, `oracle`, `sap`, `spanner`, `cordova`, `nativescript`, `react-native`,
`expo`, or `mongodb`.
Also make sure to use your own host, port, username, password, and database settings.

We added our Photo entity to the list of entities for this data source.
Each entity you are using in your connection must be listed there.

Setting `synchronize` makes sure your entities will be synced with the database, every time you run the application.

### Running the application​

Now if you run your `index.ts`, a connection with the database will be initialized and a database table for your photos will be created.

```
+-------------+--------------+----------------------------+|                         photo                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(100) |                            || description | text         |                            || filename    | varchar(255) |                            || views       | int          |                            || isPublished | boolean      |                            |+-------------+--------------+----------------------------+
```

### Creating and inserting a photo into the database​

Now let's create a new photo to save it in the database:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const photo = new Photo()photo.name = "Me and Bears"photo.description = "I am near polar bears"photo.filename = "photo-with-bears.jpg"photo.views = 1photo.isPublished = trueawait AppDataSource.manager.save(photo)console.log("Photo has been saved. Photo id is", photo.id)
```

Once your entity is saved, it will get a newly generated id.
`save` method returns an instance of the same object you pass to it.
It's not a new copy of the object, it modifies its "id" and returns it.

### Using Entity Manager​

We just created a new photo and saved it in the database.
We used `EntityManager` to save it.
Using entity manager, you can manipulate any entity in your app.
For example, let's load our saved entity:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const savedPhotos = await AppDataSource.manager.find(Photo)console.log("All photos from the db: ", savedPhotos)
```

`savedPhotos` will be an array of Photo objects with the data loaded from the database.

Learn more about [EntityManager](https://typeorm.io/docs/working-with-entity-manager/working-with-entity-manager).

### Using Repositories​

Now let's refactor our code and use `Repository` instead of `EntityManager`.
Each entity has its own repository which handles all operations with its entity.
When you deal with entities a lot, Repositories are more convenient to use than EntityManagers:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const photo = new Photo()photo.name = "Me and Bears"photo.description = "I am near polar bears"photo.filename = "photo-with-bears.jpg"photo.views = 1photo.isPublished = trueconst photoRepository = AppDataSource.getRepository(Photo)await photoRepository.save(photo)console.log("Photo has been saved")const savedPhotos = await photoRepository.find()console.log("All photos from the db: ", savedPhotos)
```

Learn more about Repository [here](https://typeorm.io/docs/working-with-entity-manager/working-with-repository).

### Loading from the database​

Let's try more load operations using the Repository:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const photoRepository = AppDataSource.getRepository(Photo)const allPhotos = await photoRepository.find()console.log("All photos from the db: ", allPhotos)const firstPhoto = await photoRepository.findOneBy({    id: 1,})console.log("First photo from the db: ", firstPhoto)const meAndBearsPhoto = await photoRepository.findOneBy({    name: "Me and Bears",})console.log("Me and Bears photo from the db: ", meAndBearsPhoto)const allViewedPhotos = await photoRepository.findBy({ views: 1 })console.log("All viewed photos: ", allViewedPhotos)const allPublishedPhotos = await photoRepository.findBy({ isPublished: true })console.log("All published photos: ", allPublishedPhotos)const [photos, photosCount] = await photoRepository.findAndCount()console.log("All photos: ", photos)console.log("Photos count: ", photosCount)
```

### Updating in the database​

Now let's load a single photo from the database, update it, and save it:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const photoRepository = AppDataSource.getRepository(Photo)const photoToUpdate = await photoRepository.findOneBy({    id: 1,})photoToUpdate.name = "Me, my friends and polar bears"await photoRepository.save(photoToUpdate)
```

Now photo with `id = 1` will be updated in the database.

### Removing from the database​

Now let's remove our photo from the database:

```
import { Photo } from "./entity/Photo"import { AppDataSource } from "./index"const photoRepository = AppDataSource.getRepository(Photo)const photoToRemove = await photoRepository.findOneBy({    id: 1,})await photoRepository.remove(photoToRemove)
```

Now photo with `id = 1` will be removed from the database.

### Creating a one-to-one relation​

Let's create a one-to-one relationship with another class.
Let's create a new class in `PhotoMetadata.ts`. This PhotoMetadata class is supposed to contain our photo's additional meta-information:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    OneToOne,    JoinColumn,} from "typeorm"import { Photo } from "./Photo"@Entity()export class PhotoMetadata {    @PrimaryGeneratedColumn()    id: number    @Column("int")    height: number    @Column("int")    width: number    @Column()    orientation: string    @Column()    compressed: boolean    @Column()    comment: string    @OneToOne(() => Photo)    @JoinColumn()    photo: Photo}
```

Here, we are using a new decorator called `@OneToOne`. It allows us to create a one-to-one relationship between two entities. We also add a `@JoinColumn` decorator, which indicates that this side of the relationship will own the relationship.
Relations can be unidirectional or bidirectional.
Only one side of the relation can be the owner.
Using `@JoinColumn` decorator is required on the owner side of the relationship.

If you run the app, you'll see a newly generated table, and it will contain a column with a foreign key for the photo relation:

```
+-------------+--------------+----------------------------+|                     photo_metadata                      |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || height      | int          |                            || width       | int          |                            || comment     | varchar(255) |                            || compressed  | boolean      |                            || orientation | varchar(255) |                            || photoId     | int          | FOREIGN KEY                |+-------------+--------------+----------------------------+
```

### Save a one-to-one relation​

Now let's save a photo and its metadata and attach them to each other.

```
import { Photo } from "./entity/Photo"import { PhotoMetadata } from "./entity/PhotoMetadata"// Create a photoconst photo = new Photo()photo.name = "Me and Bears"photo.description = "I am near polar bears"photo.filename = "photo-with-bears.jpg"photo.views = 1photo.isPublished = true// Create a photo metadataconst metadata = new PhotoMetadata()metadata.height = 640metadata.width = 480metadata.compressed = truemetadata.comment = "cybershoot"metadata.orientation = "portrait"metadata.photo = photo // this way we connect them// Get entity repositoriesconst photoRepository = AppDataSource.getRepository(Photo)const metadataRepository = AppDataSource.getRepository(PhotoMetadata)// First we should save a photoawait photoRepository.save(photo)// The Photo is saved. Now we need to save a photo metadataawait metadataRepository.save(metadata)// Doneconsole.log(    "Metadata is saved, and the relation between metadata and photo is created in the database too",)
```

### Inverse side of the relationship​

Relations can be unidirectional or bidirectional.
Currently, our relation between PhotoMetadata and Photo is unidirectional.
The owner of the relation is PhotoMetadata, and Photo doesn't know anything about PhotoMetadata.
This makes it complicated to access PhotoMetadata from the Photo side.
To fix this issue, we should add an inverse relation, and make relations between PhotoMetadata and Photo bidirectional.
Let's modify our entities:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    OneToOne,    JoinColumn,} from "typeorm"import { Photo } from "./Photo"@Entity()export class PhotoMetadata {    /* ... other columns */    @OneToOne(() => Photo, (photo) => photo.metadata)    @JoinColumn()    photo: Photo}
```

```
import { Entity, Column, PrimaryGeneratedColumn, OneToOne } from "typeorm"import { PhotoMetadata } from "./PhotoMetadata"@Entity()export class Photo {    /* ... other columns */    @OneToOne(() => PhotoMetadata, (photoMetadata) => photoMetadata.photo)    metadata: PhotoMetadata}
```

`photo => photo.metadata` is a function that returns the name of the inverse side of the relation.
Here we show that the metadata property of the Photo class is where we store PhotoMetadata in the Photo class.
Instead of passing a function that returns a property of the photo, you could alternatively spass a string to `@OneToOne` decorator, like `"metadata"`.
But we used this function-typed approach to make our refactoring easier.

Note that we should use the `@JoinColumn` decorator only on one side of a relation.
Whichever side you put this decorator on will be the owning side of the relationship.
The owning side of a relationship contains a column with a foreign key in the database.

### Relations in ESM projects​

If you use ESM in your TypeScript project, you should use the `Relation` wrapper type in relation properties to avoid circular dependency issues.
Let's modify our entities:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    OneToOne,    JoinColumn,    Relation,} from "typeorm"import { Photo } from "./Photo"@Entity()export class PhotoMetadata {    /* ... other columns */    @OneToOne(() => Photo, (photo) => photo.metadata)    @JoinColumn()    photo: Relation<Photo>}
```

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    OneToOne,    Relation,} from "typeorm"import { PhotoMetadata } from "./PhotoMetadata"@Entity()export class Photo {    /* ... other columns */    @OneToOne(() => PhotoMetadata, (photoMetadata) => photoMetadata.photo)    metadata: Relation<PhotoMetadata>}
```

### Loading objects with their relations​

Now let's load our photo and its photo metadata in a single query.
There are two ways to do it - using `find*` methods or using `QueryBuilder` functionality.
Let's use `find*` method first.
`find*` methods allow you to specify an object with the `FindOneOptions` / `FindManyOptions` interface.

```
import { Photo } from "./entity/Photo"import { PhotoMetadata } from "./entity/PhotoMetadata"import { AppDataSource } from "./index"const photoRepository = AppDataSource.getRepository(Photo)const photos = await photoRepository.find({    relations: {        metadata: true,    },})
```

Here, photos will contain an array of photos from the database, and each photo will contain its photo metadata.
Learn more about Find Options in [this documentation](https://typeorm.io/docs/working-with-entity-manager/find-options).

Using find options is good and dead simple, but if you need a more complex query, you should use `QueryBuilder` instead.
`QueryBuilder` allows more complex queries to be used elegantly:

```
import { Photo } from "./entity/Photo"import { PhotoMetadata } from "./entity/PhotoMetadata"import { AppDataSource } from "./index"const photos = await AppDataSource.getRepository(Photo)    .createQueryBuilder("photo")    .innerJoinAndSelect("photo.metadata", "metadata")    .getMany()
```

`QueryBuilder` allows the creation and execution of SQL queries of almost any complexity.
When you work with `QueryBuilder`, think like you are creating an SQL query.
In this example, "photo" and "metadata" are aliases applied to selected photos.
You use aliases to access columns and properties of the selected data.

### Using cascades to automatically save related objects​

We can set up cascade options in our relations, in the cases when we want our related object to be saved whenever the other object is saved.
Let's change our photo's `@OneToOne` decorator a bit:

```
export class Photo {    // ... other columns    @OneToOne(() => PhotoMetadata, (metadata) => metadata.photo, {        cascade: true,    })    metadata: PhotoMetadata}
```

Using `cascade` allows us not to separately save photos and separately save metadata objects now.
Now we can simply save a photo object, and the metadata object will be saved automatically because of cascade options.

```
import { AppDataSource } from "./index"// create photo objectconst photo = new Photo()photo.name = "Me and Bears"photo.description = "I am near polar bears"photo.filename = "photo-with-bears.jpg"photo.isPublished = true// create photo metadata objectconst metadata = new PhotoMetadata()metadata.height = 640metadata.width = 480metadata.compressed = truemetadata.comment = "cybershoot"metadata.orientation = "portrait"photo.metadata = metadata // this way we connect them// get repositoryconst photoRepository = AppDataSource.getRepository(Photo)// saving a photo also save the metadataawait photoRepository.save(photo)console.log("Photo is saved, photo metadata is saved too.")
```

Notice that we now set the photo's `metadata` property, instead of the metadata's `photo` property as before. The `cascade` feature only works if you connect the photo to its metadata from the photo's side. If you set the metadata side, the metadata would not be saved automatically.

### Creating a many-to-one / one-to-many relation​

Let's create a many-to-one/one-to-many relation.
Let's say a photo has one author, and each author can have many photos.
First, let's create an `Author` class:

```
import {    Entity,    Column,    PrimaryGeneratedColumn,    OneToMany,    JoinColumn,} from "typeorm"import { Photo } from "./Photo"@Entity()export class Author {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToMany(() => Photo, (photo) => photo.author) // note: we will create author property in the Photo class below    photos: Photo[]}
```

`Author` contains an inverse side of a relation.
`OneToMany` is always an inverse side of the relation, and it can't exist without `ManyToOne` on the other side of the relation.

Now let's add the owner side of the relation into the Photo entity:

```
import { Entity, Column, PrimaryGeneratedColumn, ManyToOne } from "typeorm"import { PhotoMetadata } from "./PhotoMetadata"import { Author } from "./Author"@Entity()export class Photo {    /* ... other columns */    @ManyToOne(() => Author, (author) => author.photos)    author: Author}
```

In many-to-one / one-to-many relations, the owner side is always many-to-one.
It means that the class that uses `@ManyToOne` will store the id of the related object.

After you run the application, the ORM will create the `author` table:

```
+-------------+--------------+----------------------------+|                          author                         |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(255) |                            |+-------------+--------------+----------------------------+
```

It will also modify the `photo` table, adding a new `author` column and creating a foreign key for it:

```
+-------------+--------------+----------------------------+|                         photo                           |+-------------+--------------+----------------------------+| id          | int          | PRIMARY KEY AUTO_INCREMENT || name        | varchar(255) |                            || description | varchar(255) |                            || filename    | varchar(255) |                            || isPublished | boolean      |                            || authorId    | int          | FOREIGN KEY                |+-------------+--------------+----------------------------+
```

### Creating a many-to-many relation​

Let's create a many-to-many relation.
Let's say a photo can be in many albums, and each album can contain many photos.
Let's create an `Album` class:

```
import {    Entity,    PrimaryGeneratedColumn,    Column,    ManyToMany,    JoinTable,} from "typeorm"@Entity()export class Album {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @ManyToMany(() => Photo, (photo) => photo.albums)    @JoinTable()    photos: Photo[]}
```

`@JoinTable` is required to specify that this is the owner side of the relationship.

Now let's add the inverse side of our relation to the `Photo` class:

```
export class Photo {    // ... other columns    @ManyToMany(() => Album, (album) => album.photos)    albums: Album[]}
```

After you run the application, the ORM will create an **album_photos_photo_albums** *junction table*:

```
+-------------+--------------+----------------------------+|                album_photos_photo_albums                |+-------------+--------------+----------------------------+| album_id    | int          | PRIMARY KEY FOREIGN KEY    || photo_id    | int          | PRIMARY KEY FOREIGN KEY    |+-------------+--------------+----------------------------+
```

Remember to register the `Album` class with your connection in the ORM:

```
const options: DataSourceOptions = {    // ... other options    entities: [Photo, PhotoMetadata, Author, Album],}
```

Now let's insert albums and photos into our database:

```
import { AppDataSource } from "./index"// create a few albumsconst album1 = new Album()album1.name = "Bears"await AppDataSource.manager.save(album1)const album2 = new Album()album2.name = "Me"await AppDataSource.manager.save(album2)// create a few photosconst photo = new Photo()photo.name = "Me and Bears"photo.description = "I am near polar bears"photo.filename = "photo-with-bears.jpg"photo.views = 1photo.isPublished = truephoto.albums = [album1, album2]await AppDataSource.manager.save(photo)// now our photo is saved and albums are attached to it// now lets load them:const loadedPhoto = await AppDataSource.getRepository(Photo).findOne({    where: {        id: 1,    },    relations: {        albums: true,    },})
```

`loadedPhoto` will be equal to:

```
{    id: 1,    name: "Me and Bears",    description: "I am near polar bears",    filename: "photo-with-bears.jpg",    albums: [{        id: 1,        name: "Bears"    }, {        id: 2,        name: "Me"    }]}
```

### Using QueryBuilder​

You can use QueryBuilder to build SQL queries of almost any complexity. For example, you can do this:

```
const photos = await AppDataSource.getRepository(Photo)    .createQueryBuilder("photo") // First argument is an alias. Alias is what you are selecting - photos. You must specify it.    .innerJoinAndSelect("photo.metadata", "metadata")    .leftJoinAndSelect("photo.albums", "album")    .where("photo.isPublished = true")    .andWhere("(photo.name = :photoName OR photo.name = :bearName)")    .orderBy("photo.id", "DESC")    .skip(5)    .take(10)    .setParameters({ photoName: "My", bearName: "Mishka" })    .getMany()
```

This query selects all published photos with "My" or "Mishka" names.
It will select results from position 5 (pagination offset)
and will select only 10 results (pagination limit).
The selection result will be ordered by id in descending order.
The photo albums will be left joined and their metadata will be inner-joined.

You'll use the query builder in your application a lot.
Learn more about QueryBuilder [here](https://typeorm.io/docs/query-builder/select-query-builder).

## Samples​

Take a look at the samples in [sample](https://github.com/typeorm/typeorm/tree/master/sample) for examples of usage.

There are a few repositories that you can clone and start with:

- [Example how to use TypeORM with TypeScript](https://github.com/typeorm/typescript-example)
- [Example how to use TypeORM with JavaScript](https://github.com/typeorm/javascript-example)
- [Example how to use TypeORM with JavaScript and Babel](https://github.com/typeorm/babel-example)
- [Example how to use TypeORM with TypeScript and SystemJS in Browser](https://github.com/typeorm/browser-example)
- [Example how to use TypeORM with TypeScript and React in Browser](https://github.com/ItayGarin/typeorm-react-swc)
- [Example how to use Express and TypeORM](https://github.com/typeorm/typescript-express-example)
- [Example how to use Koa and TypeORM](https://github.com/typeorm/typescript-koa-example)
- [Example how to use TypeORM with MongoDB](https://github.com/typeorm/mongo-typescript-example)
- [Example how to use TypeORM in a Cordova app](https://github.com/typeorm/cordova-example)
- [Example how to use TypeORM with an Ionic app](https://github.com/typeorm/ionic-example)
- [Example how to use TypeORM with React Native](https://github.com/typeorm/react-native-example)
- [Example how to use TypeORM with Nativescript-Vue](https://github.com/typeorm/nativescript-vue-typeorm-sample)
- [Example how to use TypeORM with Nativescript-Angular](https://github.com/betov18x/nativescript-angular-typeorm-example)
- [Example how to use TypeORM with Electron using JavaScript](https://github.com/typeorm/electron-javascript-example)
- [Example how to use TypeORM with Electron using TypeScript](https://github.com/typeorm/electron-typescript-example)

## Extensions​

There are several extensions that simplify working with TypeORM and integrating it with other modules:

- [TypeORM integration](https://github.com/typeorm/typeorm-typedi-extensions) with [TypeDI](https://github.com/pleerock/typedi)
- [TypeORM integration](https://github.com/typeorm/typeorm-routing-controllers-extensions) with [routing-controllers](https://github.com/pleerock/routing-controllers)
- Models generation from the existing database - [typeorm-model-generator](https://github.com/Kononnable/typeorm-model-generator)
- Fixtures loader - [typeorm-fixtures-cli](https://github.com/RobinCK/typeorm-fixtures)
- ER Diagram generator - [typeorm-uml](https://github.com/eugene-manuilov/typeorm-uml/)
- another ER Diagram generator - [erdia](https://www.npmjs.com/package/erdia/)
- Create, drop and seed database - [typeorm-extension](https://github.com/tada5hi/typeorm-extension)
- Automatically update `data-source.ts` after generating [migrations](https://typeorm.io/docs/migrations/why)/entities - [typeorm-codebase-sync](https://www.npmjs.com/package/typeorm-codebase-sync)
- Easy manipulation of `relations` objects - [typeorm-relations](https://npmjs.com/package/typeorm-relations)
- Automatically generate `relations` based on a GraphQL query - [typeorm-relations-graphql](https://npmjs.com/package/typeorm-relations-graphql)

## Contributing​

Learn about contribution [here](https://github.com/typeorm/typeorm/blob/master/CONTRIBUTING.md) and how to set up your development environment [here](https://github.com/typeorm/typeorm/blob/master/DEVELOPER.md).

This project exists thanks to all the people who contribute:

## Sponsors​

Open source is hard and time-consuming. If you want to invest in TypeORM's future, you can become a sponsor and allow our core team to spend more time on TypeORM's improvements and new features. [Become a sponsor](https://opencollective.com/typeorm)

## Gold Sponsors​

Become a gold sponsor and get premium technical support from our core contributors. [Become a gold sponsor](https://opencollective.com/typeorm)

---

# Active Record vs Data Mapper

> What is the Active Record pattern?

## What is the Active Record pattern?​

In TypeORM you can use both the Active Record and the Data Mapper patterns.

Using the Active Record approach, you define all your query methods inside the model itself, and you save, remove, and load objects using model methods.

Simply said, the Active Record pattern is an approach to access your database within your models.
You can read more about the Active Record pattern on [Wikipedia](https://en.wikipedia.org/wiki/Active_record_pattern).

Example:

```
import { BaseEntity, Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User extends BaseEntity {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    isActive: boolean}
```

All active-record entities must extend the `BaseEntity` class, which provides methods to work with the entity.
Example of how to work with such entity:

```
// example how to save AR entityconst user = new User()user.firstName = "Timber"user.lastName = "Saw"user.isActive = trueawait user.save()// example how to remove AR entityawait user.remove()// example how to load AR entitiesconst users = await User.find({ skip: 2, take: 5 })const newUsers = await User.findBy({ isActive: true })const timber = await User.findOneBy({ firstName: "Timber", lastName: "Saw" })
```

`BaseEntity` has most of the methods of the standard `Repository`.
Most of the time you don't need to use `Repository` or `EntityManager` with active record entities.

Now let's say we want to create a function that returns users by first and last name.
We can create such functions as a static method in a `User` class:

```
import { BaseEntity, Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User extends BaseEntity {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    isActive: boolean    static findByName(firstName: string, lastName: string) {        return this.createQueryBuilder("user")            .where("user.firstName = :firstName", { firstName })            .andWhere("user.lastName = :lastName", { lastName })            .getMany()    }}
```

And use it just like other methods:

```
const timber = await User.findByName("Timber", "Saw")
```

## What is the Data Mapper pattern?​

In TypeORM you can use both the Active Record and Data Mapper patterns.

Using the Data Mapper approach, you define all your query methods in separate classes called "repositories",
and you save, remove, and load objects using repositories.
In data mapper your entities are very dumb - they just define their properties and may have some "dummy" methods.

Simply said, data mapper is an approach to access your database within repositories instead of models.
You can read more about data mapper on [Wikipedia](https://en.wikipedia.org/wiki/Data_mapper_pattern).

Example:

```
import { Entity, PrimaryGeneratedColumn, Column } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string    @Column()    isActive: boolean}
```

Example of how to work with such entity:

```
const userRepository = dataSource.getRepository(User)// example how to save DM entityconst user = new User()user.firstName = "Timber"user.lastName = "Saw"user.isActive = trueawait userRepository.save(user)// example how to remove DM entityawait userRepository.remove(user)// example how to load DM entitiesconst users = await userRepository.find({ skip: 2, take: 5 })const newUsers = await userRepository.findBy({ isActive: true })const timber = await userRepository.findOneBy({    firstName: "Timber",    lastName: "Saw",})
```

In order to extend standard repository with custom methods, use [custom repository pattern](https://typeorm.io/docs/working-with-entity-manager/custom-repository).

## Which one should I choose?​

The decision is up to you.
Both strategies have their own cons and pros.

One thing we should always keep in mind with software development is how we are going to maintain our applications.
The `Data Mapper` approach helps with maintainability, which is more effective in larger apps.
The `Active Record` approach helps keep things simple which works well in smaller apps.

---

# Example using TypeORM with Express

> Initial setup

## Initial setup​

Let's create a simple application called "user" which stores users in the database
and allows us to create, update, remove, and get a list of all users, as well as a single user by id
within web api.

First, create a directory called "user":

```
mkdir user
```

Then switch to the directory and create a new project:

```
cd usernpm init
```

Finish the init process by filling in all required application information.

Now we need to install and setup a TypeScript compiler. Lets install it first:

```
npm i typescript --save-dev
```

Then let's create a `tsconfig.json` file which contains the configuration required for the application to
compile and run. Create it using your favorite editor and put the following configuration:

```
{    "compilerOptions": {        "lib": ["es5", "es6", "dom"],        "target": "es5",        "module": "commonjs",        "moduleResolution": "node",        "emitDecoratorMetadata": true,        "experimentalDecorators": true    }}
```

Now let's create a main application endpoint - `app.ts` inside the `src` directory:

```
mkdir srccd srctouch app.ts
```

Let's add a simple `console.log` inside it:

```
console.log("Application is up and running")
```

Now it's time to run our application.
To run it, you need to compile your typescript project first:

```
tsc
```

Once you compile it, you should have a `src/app.js` file generated.
You can run it using:

```
node src/app.js
```

You should see the, "Application is up and running" message in your console right after you run the application.

You must compile your files each time you make a change.
Alternatively, you can set up watcher or install [ts-node](https://github.com/TypeStrong/ts-node) to avoid manual compilation each time.

## Adding Express to the application​

Let's add Express to our application. First, let's install the packages we need:

```
npm install expressnpm install @types/express --save-dev
```

- `express` is the express engine itself. It allows us to create a web api
- `@types/express` is used to have a type information when using express

Let's edit the `src/app.ts` file and add express-related logic:

```
import * as express from "express"import { Request, Response } from "express"// create and setup express appconst app = express()app.use(express.json())// register routesapp.get("/users", function (req: Request, res: Response) {    // here we will have logic to return all users})app.get("/users/:id", function (req: Request, res: Response) {    // here we will have logic to return user by id})app.post("/users", function (req: Request, res: Response) {    // here we will have logic to save a user})app.put("/users/:id", function (req: Request, res: Response) {    // here we will have logic to update a user by a given user id})app.delete("/users/:id", function (req: Request, res: Response) {    // here we will have logic to delete a user by a given user id})// start express serverapp.listen(3000)
```

Now you can compile and run your project.
You should have an express server running now with working routes.
However, those routes do not return any content yet.

## Adding TypeORM to the application​

Finally, let's add TypeORM to the application.
In this example, we will use `mysql` driver.
Setup process for other drivers is similar.

Let's install the required packages first:

```
npm install typeorm reflect-metadata mysql
```

- `typeorm` is the typeorm package itself
- `reflect-metadata` is required to make decorators to work properly. Remember to import it before your TypeORM code.
- `mysql` is the underlying database driver. If you are using a different database system, you must install the appropriate package

Let's create `app-data-source.ts` where we set up initial database connection options:

```
import { DataSource } from "typeorm"export const myDataSource = new DataSource({    type: "mysql",    host: "localhost",    port: 3306,    username: "test",    password: "test",    database: "test",    entities: ["src/entity/*.js"],    logging: true,    synchronize: true,})
```

Configure each option as you need.
Learn more about options [here](https://typeorm.io/docs/data-source/data-source-options).

Let's create a `user.entity.ts` entity inside `src/entity`:

```
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm"@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    firstName: string    @Column()    lastName: string}
```

Let's change `src/app.ts` to establish database connection and start using `myDataSource`:

```
import "reflect-metadata"import * as express from "express"import { Request, Response } from "express"import { User } from "./entity/User"import { myDataSource } from "./app-data-source.ts"// establish database connectiontry {    await myDataSource.initialize()    console.log("Data Source has been initialized!")} catch (error) {    console.error("Error during Data Source initialization:", error)}// create and setup express appconst app = express()app.use(express.json())// register routesapp.get("/users", async function (req: Request, res: Response) {    const users = await myDataSource.getRepository(User).find()    res.json(users)})app.get("/users/:id", async function (req: Request, res: Response) {    const results = await myDataSource.getRepository(User).findOneBy({        id: req.params.id,    })    return res.send(results)})app.post("/users", async function (req: Request, res: Response) {    const user = await myDataSource.getRepository(User).create(req.body)    const results = await myDataSource.getRepository(User).save(user)    return res.send(results)})app.put("/users/:id", async function (req: Request, res: Response) {    const user = await myDataSource.getRepository(User).findOneBy({        id: req.params.id,    })    myDataSource.getRepository(User).merge(user, req.body)    const results = await myDataSource.getRepository(User).save(user)    return res.send(results)})app.delete("/users/:id", async function (req: Request, res: Response) {    const results = await myDataSource.getRepository(User).delete(req.params.id)    return res.send(results)})// start express serverapp.listen(3000)
```

Now you should have a basic express application connected to MySQL database up and running.
