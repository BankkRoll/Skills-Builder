# FAQ and more

# FAQ

> How do I update a database schema?

## How do I update a database schema?​

One of the main responsibilities of TypeORM is to keep your database tables in sync with your entities.
There are two ways that help you achieve this:

- Use `synchronize: true` in data source options:
  ```
  import { DataSource } from "typeorm"const myDataSource = new DataSource({    // ...    synchronize: true,})
  ```
  This option automatically syncs your database tables with the given entities each time you run this code.
  This option is perfect during development, but in production you may not want this option to be enabled.
- Use command line tools and run schema sync manually in the command line:
  ```
  typeorm schema:sync
  ```
  This command will execute schema synchronization.

Schema sync is extremely fast.
If you are considering to disable synchronize option during development because of performance issues,
first check how fast it is.

## How do I change a column name in the database?​

By default, column names are generated from property names.
You can simply change it by specifying a `name` column option:

```
@Column({ name: "is_active" })isActive: boolean;
```

## How can I set the default value to some function, for exampleNOW()?​

`default` column option supports a function.
If you are passing a function which returns a string,
it will use that string as a default value without escaping it.
For example:

```
@Column({ default: () => "NOW()" })date: Date;
```

## How to do validation?​

Validation is not part of TypeORM because validation is a separate process
not really related to what TypeORM does.
If you want to use validation use [class-validator](https://github.com/pleerock/class-validator) - it works perfectly with TypeORM.

## What does "owner side" in a relations mean or why we need to use@JoinColumnand@JoinTable?​

Let's start with `one-to-one` relation.
Let's say we have two entities: `User` and `Photo`:

```
@Entity()export class User {    @PrimaryGeneratedColumn()    id: number    @Column()    name: string    @OneToOne()    photo: Photo}
```

```
@Entity()export class Photo {    @PrimaryGeneratedColumn()    id: number    @Column()    url: string    @OneToOne()    user: User}
```

This example does not have a `@JoinColumn` which is incorrect.
Why? Because to make a real relation, we need to create a column in the database.
We need to create a column `userId` in `photo` or `photoId` in `user`.
But which column should be created - `userId` or `photoId`?
TypeORM cannot decide for you.
To make a decision, you must use `@JoinColumn` on one of the sides.
If you put `@JoinColumn` in `Photo` then a column called `userId` will be created in the `photo` table.
If you put `@JoinColumn` in `User` then a column called `photoId` will be created in the `user` table.
The side with `@JoinColumn` will be called the "owner side of the relationship".
The other side of the relation, without `@JoinColumn`, is called the "inverse (non-owner) side of relationship".

It is the same in a `@ManyToMany` relation. You use `@JoinTable` to show the owner side of the relation.

In `@ManyToOne` or `@OneToMany` relations, `@JoinColumn` is not necessary because
both decorators are different, and the table where you put the `@ManyToOne` decorator will have the relational column.

`@JoinColumn` and `@JoinTable` decorators can also be used to specify additional
join column / junction table settings, like join column name or junction table name.

## How do I add extra columns into many-to-many (junction) table?​

It's not possible to add extra columns into a table created by a many-to-many relation.
You'll need to create a separate entity and bind it using two many-to-one relations with the target entities
(the effect will be same as creating a many-to-many table),
and add extra columns in there. You can read more about this in [Many-to-Many relations](https://typeorm.io/docs/relations/many-to-many-relations#many-to-many-relations-with-custom-properties).

## How to handle outDir TypeScript compiler option?​

When you are using the `outDir` compiler option, don't forget to copy assets and resources your app is using into the output directory.
Otherwise, make sure to setup correct paths to those assets.

One important thing to know is that when you remove or move entities, the old entities are left untouched inside the output directory.
For example, you create a `Post` entity and rename it to `Blog`,
you no longer have `Post.ts` in your project. However, `Post.js` is left inside the output directory.
Now, when TypeORM reads entities from your output directory, it sees two entities - `Post` and `Blog`.
This may be a source of bugs.
That's why when you remove and move entities with `outDir` enabled, it's strongly recommended to remove your output directory and recompile the project again.

## How to use TypeORM with ts-node?​

You can prevent compiling files each time using [ts-node](https://github.com/TypeStrong/ts-node).
If you are using ts-node, you can specify `ts` entities inside data source options:

```
{    entities: ["src/entity/*.ts"],    subscribers: ["src/subscriber/*.ts"]}
```

Also, if you are compiling js files into the same folder where your typescript files are,
make sure to use the `outDir` compiler option to prevent
[this issue](https://github.com/TypeStrong/ts-node/issues/432).

Also, if you want to use the ts-node CLI, you can execute TypeORM the following way:

```
npx typeorm-ts-node-commonjs schema:sync
```

For ESM projects use this instead:

```
npx typeorm-ts-node-esm schema:sync
```

## How to use Webpack for the backend?​

Webpack produces warnings due to what it views as missing require statements -- require statements for all drivers supported by TypeORM. To suppress these warnings for unused drivers, you will need to edit your webpack config file.

```
const FilterWarningsPlugin = require('webpack-filter-warnings-plugin');module.exports = {    ...    plugins: [        //ignore the drivers you don't want. This is the complete list of all drivers -- remove the suppressions for drivers you want to use.        new FilterWarningsPlugin({            exclude: [/mongodb/, /mssql/, /mysql/, /mysql2/, /oracledb/, /pg/, /pg-native/, /pg-query-stream/, /react-native-sqlite-storage/, /redis/, /sqlite3/, /sql.js/, /typeorm-aurora-data-api-driver/]        })    ]};
```

### Bundling Migration Files​

By default Webpack tries to bundle everything into one file. This can be problematic when your project has migration files which are meant to be executed after bundled code is deployed to production. To make sure all your [migrations](https://typeorm.io/docs/migrations/why) can be recognized and executed by TypeORM, you may need to use "Object Syntax" for the `entry` configuration for the migration files only.

```
const glob = require("glob")const path = require("path")module.exports = {    // ... your webpack configurations here...    // Dynamically generate a `{ [name]: sourceFileName }` map for the `entry` option    // change `src/db/migrations` to the relative path to your migration folder    entry: glob        .sync(path.resolve("src/db/migrations/*.ts"))        .reduce((entries, filename) => {            const migrationName = path.basename(filename, ".ts")            return Object.assign({}, entries, {                [migrationName]: filename,            })        }, {}),    resolve: {        // assuming all your migration files are written in TypeScript        extensions: [".ts"],    },    output: {        // change `path` to where you want to put transpiled migration files.        path: __dirname + "/dist/db/migrations",        // this is important - we want UMD (Universal Module Definition) for migration files.        libraryTarget: "umd",        filename: "[name].js",    },}
```

Also, since Webpack 4, when using `mode: 'production'`, files are optimized by default which includes mangling your code in order to minimize file sizes. This breaks the [migrations](https://typeorm.io/docs/migrations/why) because TypeORM relies on their names to determine which has already been executed. You may disable minimization completely by adding:

```
module.exports = {    // ... other Webpack configurations here    optimization: {        minimize: false,    },}
```

Alternatively, if you are using the `UglifyJsPlugin`, you can tell it to not change class or function names like so:

```
const UglifyJsPlugin = require("uglifyjs-webpack-plugin")module.exports = {    // ... other Webpack configurations here    optimization: {        minimizer: [            new UglifyJsPlugin({                uglifyOptions: {                    keep_classnames: true,                    keep_fnames: true,                },            }),        ],    },}
```

Lastly, make sure in your data source options, the transpiled migration files are included:

```
// TypeORM Configurationsmodule.exports = {    // ...    migrations: [        // this is the relative path to the transpiled migration files in production        "db/migrations/**/*.js",        // your source migration files, used in development mode        "src/db/migrations/**/*.ts",    ],}
```

## How to use TypeORM in ESM projects?​

Make sure to add `"type": "module"` in the `package.json` of your project so TypeORM will know to use `import( ... )` on files.

To avoid circular dependency import issues use the `Relation` wrapper type for relation type definitions in entities:

```
@Entity()export class User {    @OneToOne(() => Profile, (profile) => profile.user)    profile: Relation<Profile>}
```

Doing this prevents the type of the property from being saved in the transpiled code in the property metadata, preventing circular dependency issues.

Since the type of the column is already defined using the `@OneToOne` decorator, there's no use of the additional type metadata saved by TypeScript.

> Important: Do not use `Relation` on non-relation column types

---

# Support

> Found a bug or want to propose a new feature?

## Found a bug or want to propose a new feature?​

If you found a bug, issue, or you just want to propose a new feature, create [an issue on GitHub](https://github.com/typeorm/typeorm/issues).

## Have a question?​

If you have a question, you can ask it on [StackOverflow](https://stackoverflow.com/questions/tagged/typeorm) or other community support channels.

## Want community support?​

If you want community support, or simply want to chat with friendly TypeORM enthusiasts and users, you can do it on [Discord](https://discord.gg/cC9hkmUgNa).

## Want professional commercial support?​

The TypeORM core team is always ready to provide professional commercial support.
We are ready to work with any team in any part of the world.
Feel free to [contact us](mailto:support@typeorm.io).

---

# Supported platforms

> NodeJS

## NodeJS​

TypeORM is compatible with Node.js 16+ and currently each commit is tested on Node.js 18 and 20.

## Browser​

You can use [sql.js](https://sql.js.org) in the browser.

### Webpack configuration​

In the `browser` folder the package also includes a version compiled as a ES2015 module. If you want to use a different loader this is the point to start. Prior to TypeORM 0.1.7, the package is setup in a way that loaders like webpack will automatically use the `browser` folder. With 0.1.7 this was dropped to support Webpack usage in Node.js projects. This means, that the `NormalModuleReplacementPlugin` has to be used to insure that the correct version is loaded for browser projects. The configuration in your webpack config file, for this plugin looks like this:

```
plugins: [    ..., // any existing plugins that you already have    new webpack.NormalModuleReplacementPlugin(/typeorm$/, function (result) {        result.request = result.request.replace(/typeorm/, "typeorm/browser");    }),    new webpack.ProvidePlugin({      'window.SQL': 'sql.js/dist/sql-wasm.js'    })]
```

and make sure [sql-wasm.wasm file](https://github.com/sql-js/sql.js/blob/master/README.md#downloadingusing) exists in your public path.

### Example of configuration​

```
new DataSource({    type: "sqljs",    entities: [Photo],    synchronize: true,})
```

### Don't forget to include reflect-metadata​

In your main html page, you need to include reflect-metadata:

```
<script src="./node_modules/reflect-metadata/Reflect.js"></script>
```

## Capacitor​

See [Using TypeORM with the Capacitor driver type](https://github.com/capacitor-community/sqlite/blob/master/docs/TypeORM-Usage-From-5.6.0.md) in the official Capacitor docs.

## Cordova / Ionic apps​

TypeORM is able to run on Cordova/Ionic apps using the
[cordova-sqlite-storage](https://github.com/litehelpers/Cordova-sqlite-storage) plugin
You have the option to choose between module loaders just like in browser package.
For an example how to use TypeORM in Cordova see [typeorm/cordova-example](https://github.com/typeorm/cordova-example) and for Ionic see [typeorm/ionic-example](https://github.com/typeorm/ionic-example). **Important**: For use with Ionic, a custom webpack config file is needed! Please checkout the example to see the needed changes. Note that there is currently no support for transactions when using the [cordova-sqlite-storage](https://github.com/litehelpers/Cordova-sqlite-storage) plugin. See [Cordova SQLite limitations](https://github.com/storesafe/cordova-sqlite-storage#other-limitations) for more information.

## Expo​

TypeORM is able to run on Expo apps using the [Expo SQLite API](https://docs.expo.io/versions/latest/sdk/sqlite/). For an example how to use TypeORM in Expo see [typeorm/expo-example](https://github.com/typeorm/expo-example).

## NativeScript​

1. `tns install webpack` (read below why webpack is required)
2. `tns plugin add nativescript-sqlite`
3. Create a DataSource in your app's entry point
  ```
  import driver from "nativescript-sqlite"const dataSource = new DataSource({    database: "test.db",    type: "nativescript",    driver,    entities: [        Todo, //... whatever entities you have    ],    logging: true,})
  ```

Note: This works only with NativeScript 4.x and above

*When using with NativeScript,using webpack is compulsory.
Thetypeorm/browserpackage is raw ES7 code withimport/exportwhich willNOTrun as it is. It has to be bundled.
Please use thetns run --bundlemethod*

Checkout example [here](https://github.com/championswimmer/nativescript-vue-typeorm-sample)!

## React Native​

TypeORM is able to run on React Native apps using the [react-native-sqlite-storage](https://github.com/andpor/react-native-sqlite-storage) plugin. For an example see [typeorm/react-native-example](https://github.com/typeorm/react-native-example).

---

# Query Runner API

> In order to use an API to change a database schema you can use QueryRunner.

In order to use an API to change a database schema you can use `QueryRunner`.

```
import {    MigrationInterface,    QueryRunner,    Table,    TableIndex,    TableColumn,    TableForeignKey,} from "typeorm"export class QuestionRefactoringTIMESTAMP implements MigrationInterface {    async up(queryRunner: QueryRunner): Promise<void> {        await queryRunner.createTable(            new Table({                name: "question",                columns: [                    {                        name: "id",                        type: "int",                        isPrimary: true,                    },                    {                        name: "name",                        type: "varchar",                    },                ],            }),            true,        )        await queryRunner.createIndex(            "question",            new TableIndex({                name: "IDX_QUESTION_NAME",                columnNames: ["name"],            }),        )        await queryRunner.createTable(            new Table({                name: "answer",                columns: [                    {                        name: "id",                        type: "int",                        isPrimary: true,                    },                    {                        name: "name",                        type: "varchar",                    },                    {                        name: "created_at",                        type: "timestamp",                        default: "now()",                    },                ],            }),            true,        )        await queryRunner.addColumn(            "answer",            new TableColumn({                name: "questionId",                type: "int",            }),        )        await queryRunner.createForeignKey(            "answer",            new TableForeignKey({                columnNames: ["questionId"],                referencedColumnNames: ["id"],                referencedTableName: "question",                onDelete: "CASCADE",            }),        )    }    async down(queryRunner: QueryRunner): Promise<void> {        const table = await queryRunner.getTable("answer")        const foreignKey = table.foreignKeys.find(            (fk) => fk.columnNames.indexOf("questionId") !== -1,        )        await queryRunner.dropForeignKey("answer", foreignKey)        await queryRunner.dropColumn("answer", "questionId")        await queryRunner.dropTable("answer")        await queryRunner.dropIndex("question", "IDX_QUESTION_NAME")        await queryRunner.dropTable("question")    }}
```

---

```
getDatabases(): Promise<string[]>
```

Returns all available database names including system databases.

---

```
getSchemas(database?: string): Promise<string[]>
```

- `database` - If database parameter specified, returns schemas of that database

Returns all available schema names including system schemas. Useful for SQLServer and Postgres only.

---

```
getTable(tableName: string): Promise<Table|undefined>
```

- `tableName` - name of a table to be loaded

Loads a table by a given name from the database.

---

```
getTables(tableNames: string[]): Promise<Table[]>
```

- `tableNames` - name of a tables to be loaded

Loads a tables by a given names from the database.

---

```
hasDatabase(database: string): Promise<boolean>
```

- `database` - name of a database to be checked

Checks if database with the given name exist.

---

```
hasSchema(schema: string): Promise<boolean>
```

- `schema` - name of a schema to be checked

Checks if schema with the given name exist. Used only for SqlServer and Postgres.

---

```
hasTable(table: Table|string): Promise<boolean>
```

- `table` - Table object or name

Checks if table exist.

---

```
hasColumn(table: Table|string, columnName: string): Promise<boolean>
```

- `table` - Table object or name
- `columnName` - name of a column to be checked

Checks if column exist in the table.

---

```
createDatabase(database: string, ifNotExist?: boolean): Promise<void>
```

- `database` - database name
- `ifNotExist` - skips creation if `true`, otherwise throws error if database already exist

Creates a new database.

---

```
dropDatabase(database: string, ifExist?: boolean): Promise<void>
```

- `database` - database name
- `ifExist` - skips deletion if `true`, otherwise throws error if database was not found

Drops database.

---

```
createSchema(schemaPath: string, ifNotExist?: boolean): Promise<void>
```

- `schemaPath` - schema name. For SqlServer can accept schema path (e.g. 'dbName.schemaName') as parameter.
  If schema path passed, it will create schema in specified database
- `ifNotExist` - skips creation if `true`, otherwise throws error if schema already exist

Creates a new table schema.

---

```
dropSchema(schemaPath: string, ifExist?: boolean, isCascade?: boolean): Promise<void>
```

- `schemaPath` - schema name. For SqlServer can accept schema path (e.g. 'dbName.schemaName') as parameter.
  If schema path passed, it will drop schema in specified database
- `ifExist` - skips deletion if `true`, otherwise throws error if schema was not found
- `isCascade` - If `true`, automatically drop objects (tables, functions, etc.) that are contained in the schema.
  Used only in Postgres.

Drops a table schema.

---

```
createTable(table: Table, ifNotExist?: boolean, createForeignKeys?: boolean, createIndices?: boolean): Promise<void>
```

- `table` - Table object.
- `ifNotExist` - skips creation if `true`, otherwise throws error if table already exist. Default `false`
- `createForeignKeys` - indicates whether foreign keys will be created on table creation. Default `true`
- `createIndices` - indicates whether indices will be created on table creation. Default `true`

Creates a new table.

---

```
dropTable(table: Table|string, ifExist?: boolean, dropForeignKeys?: boolean, dropIndices?: boolean): Promise<void>
```

- `table` - Table object or table name to be dropped
- `ifExist` - skips dropping if `true`, otherwise throws error if table does not exist
- `dropForeignKeys` - indicates whether foreign keys will be dropped on table deletion. Default `true`
- `dropIndices` - indicates whether indices will be dropped on table deletion. Default `true`

Drops a table.

---

```
renameTable(oldTableOrName: Table|string, newTableName: string): Promise<void>
```

- `oldTableOrName` - old Table object or name to be renamed
- `newTableName` - new table name

Renames a table.

---

```
addColumn(table: Table|string, column: TableColumn): Promise<void>
```

- `table` - Table object or name
- `column` - new column

Adds a new column.

---

```
addColumns(table: Table|string, columns: TableColumn[]): Promise<void>
```

- `table` - Table object or name
- `columns` - new columns

Adds a new column.

---

```
renameColumn(table: Table|string, oldColumnOrName: TableColumn|string, newColumnOrName: TableColumn|string): Promise<void>
```

- `table` - Table object or name
- `oldColumnOrName` - old column. Accepts TableColumn object or column name
- `newColumnOrName` - new column. Accepts TableColumn object or column name

Renames a column.

---

```
changeColumn(table: Table|string, oldColumn: TableColumn|string, newColumn: TableColumn): Promise<void>
```

- `table` - Table object or name
- `oldColumn` - old column. Accepts TableColumn object or column name
- `newColumn` - new column. Accepts TableColumn object

Changes a column in the table.

---

```
changeColumns(table: Table|string, changedColumns: { oldColumn: TableColumn, newColumn: TableColumn }[]): Promise<void>
```

- `table` - Table object or name
- `changedColumns` - array of changed columns.
  - `oldColumn` - old TableColumn object
  - `newColumn` - new TableColumn object

Changes a columns in the table.

---

```
dropColumn(table: Table|string, column: TableColumn|string): Promise<void>
```

- `table` - Table object or name
- `column` - TableColumn object or column name to be dropped

Drops a column in the table.

---

```
dropColumns(table: Table|string, columns: TableColumn[]|string[]): Promise<void>
```

- `table` - Table object or name
- `columns` - array of TableColumn objects or column names to be dropped

Drops a columns in the table.

---

```
createPrimaryKey(table: Table|string, columnNames: string[]): Promise<void>
```

- `table` - Table object or name
- `columnNames` - array of column names which will be primary

Creates a new primary key.

---

```
updatePrimaryKeys(table: Table|string, columns: TableColumn[]): Promise<void>
```

- `table` - Table object or name
- `columns` - array of TableColumn objects which will be updated

Updates composite primary keys.

---

```
dropPrimaryKey(table: Table|string): Promise<void>
```

- `table` - Table object or name

Drops a primary key.

---

```
createUniqueConstraint(table: Table|string, uniqueConstraint: TableUnique): Promise<void>
```

- `table` - Table object or name
- `uniqueConstraint` - TableUnique object to be created

Creates new unique constraint.

> Note: does not work for MySQL, because MySQL stores unique constraints as unique indices. Use `createIndex()` method instead.

---

```
createUniqueConstraints(table: Table|string, uniqueConstraints: TableUnique[]): Promise<void>
```

- `table` - Table object or name
- `uniqueConstraints` - array of TableUnique objects to be created

Creates new unique constraints.

> Note: does not work for MySQL, because MySQL stores unique constraints as unique indices. Use `createIndices()` method instead.

---

```
dropUniqueConstraint(table: Table|string, uniqueOrName: TableUnique|string): Promise<void>
```

- `table` - Table object or name
- `uniqueOrName` - TableUnique object or unique constraint name to be dropped

Drops a unique constraint.

> Note: does not work for MySQL, because MySQL stores unique constraints as unique indices. Use `dropIndex()` method instead.

---

```
dropUniqueConstraints(table: Table|string, uniqueConstraints: TableUnique[]): Promise<void>
```

- `table` - Table object or name
- `uniqueConstraints` - array of TableUnique objects to be dropped

Drops unique constraints.

> Note: does not work for MySQL, because MySQL stores unique constraints as unique indices. Use `dropIndices()` method instead.

---

```
createCheckConstraint(table: Table|string, checkConstraint: TableCheck): Promise<void>
```

- `table` - Table object or name
- `checkConstraint` - TableCheck object

Creates a new check constraint.

> Note: MySQL does not support check constraints.

---

```
createCheckConstraints(table: Table|string, checkConstraints: TableCheck[]): Promise<void>
```

- `table` - Table object or name
- `checkConstraints` - array of TableCheck objects

Creates a new check constraint.

> Note: MySQL does not support check constraints.

---

```
dropCheckConstraint(table: Table|string, checkOrName: TableCheck|string): Promise<void>
```

- `table` - Table object or name
- `checkOrName` - TableCheck object or check constraint name

Drops check constraint.

> Note: MySQL does not support check constraints.

---

```
dropCheckConstraints(table: Table|string, checkConstraints: TableCheck[]): Promise<void>
```

- `table` - Table object or name
- `checkConstraints` - array of TableCheck objects

Drops check constraints.

> Note: MySQL does not support check constraints.

---

```
createForeignKey(table: Table|string, foreignKey: TableForeignKey): Promise<void>
```

- `table` - Table object or name
- `foreignKey` - TableForeignKey object

Creates a new foreign key.

---

```
createForeignKeys(table: Table|string, foreignKeys: TableForeignKey[]): Promise<void>
```

- `table` - Table object or name
- `foreignKeys` - array of TableForeignKey objects

Creates a new foreign keys.

---

```
dropForeignKey(table: Table|string, foreignKeyOrName: TableForeignKey|string): Promise<void>
```

- `table` - Table object or name
- `foreignKeyOrName` - TableForeignKey object or foreign key name

Drops a foreign key.

---

```
dropForeignKeys(table: Table|string, foreignKeys: TableForeignKey[]): Promise<void>
```

- `table` - Table object or name
- `foreignKeys` - array of TableForeignKey objects

Drops a foreign keys.

---

```
createIndex(table: Table|string, index: TableIndex): Promise<void>
```

- `table` - Table object or name
- `index` - TableIndex object

Creates a new index.

---

```
createIndices(table: Table|string, indices: TableIndex[]): Promise<void>
```

- `table` - Table object or name
- `indices` - array of TableIndex objects

Creates a new indices.

---

```
dropIndex(table: Table|string, index: TableIndex|string): Promise<void>
```

- `table` - Table object or name
- `index` - TableIndex object or index name

Drops an index.

---

```
dropIndices(table: Table|string, indices: TableIndex[]): Promise<void>
```

- `table` - Table object or name
- `indices` - array of TableIndex objects

Drops an indices.

---

```
clearTable(tableName: string): Promise<void>
```

- `tableName` - table name

Clears all table contents.

> Note: this operation uses SQL's TRUNCATE query which cannot be reverted in transactions.

---

```
enableSqlMemory(): void
```

Enables special query runner mode in which sql queries won't be executed, instead they will be memorized into a special variable inside query runner.
You can get memorized sql using `getMemorySql()` method.

---

```
disableSqlMemory(): void
```

Disables special query runner mode in which sql queries won't be executed. Previously memorized sql will be flushed.

---

```
clearSqlMemory(): void
```

Flushes all memorized sql statements.

---

```
getMemorySql(): SqlInMemory
```

- returns `SqlInMemory` object with array of `upQueries` and `downQueries` sql statements

Gets sql stored in the memory. Parameters in the sql are already replaced.

---

```
executeMemoryUpSql(): Promise<void>
```

Executes memorized up sql queries.

---

```
executeMemoryDownSql(): Promise<void>
```

Executes memorized down sql queries.

---

---

# Creating manually

> You can create a new migration using CLI by specifying the name and location of the migration:

You can create a new migration using CLI by specifying the name and location of the migration:

```
npx typeorm migration:create <path/to/migrations>/<migration-name>
```

For example:

```
npx typeorm migration:create src/db/migrations/post-refactoring
```

After you run the command you can see a new file generated in the `src/db/migrations` directory named `{TIMESTAMP}-post-refactoring.ts` where `{TIMESTAMP}` is the current timestamp when the migration was generated.

Now you can open the file and add your migration sql queries there. You should see the following content inside your migration:

```
import { MigrationInterface, QueryRunner } from "typeorm"export class PostRefactoringTIMESTAMP implements MigrationInterface {    async up(queryRunner: QueryRunner): Promise<void> {}    async down(queryRunner: QueryRunner): Promise<void> {}}
```

There are two methods you must fill with your migration code: `up` and `down`.
`up` has to contain the code you need to perform the migration.
`down` has to revert whatever `up` changed.
`down` method is used to revert the last migration.

Inside both `up` and `down` you have a `QueryRunner` object.
All database operations are executed using this object.
Learn more about [query runner](https://typeorm.io/docs/query-runner).

Let's see what the migration looks like with our `Post` changes:

```
import { MigrationInterface, QueryRunner } from "typeorm"export class PostRefactoringTIMESTAMP implements MigrationInterface {    async up(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(            `ALTER TABLE "post" RENAME COLUMN "title" TO "name"`,        )    }    async down(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(            `ALTER TABLE "post" RENAME COLUMN "name" TO "title"`,        ) // reverts things made in "up" method    }}
```

---

# Executing and reverting

> Once you have a migration to run on production, you can run them using a CLI command:

Once you have a migration to run on production, you can run them using a CLI command:

```
typeorm migration:run -- -d path-to-datasource-config
```

**typeorm migration:createandtypeorm migration:generatewill create.tsfiles, unless you use theoflag (see more inGenerating migrations). Themigration:runandmigration:revertcommands only work on.jsfiles. Thus the typescript files need to be compiled before running the commands.** Alternatively, you can use `ts-node` with `typeorm` to run `.ts` migration files.

Example with `ts-node`:

```
npx typeorm-ts-node-commonjs migration:run -- -d path-to-datasource-config
```

Example with `ts-node` in ESM projects:

```
npx typeorm-ts-node-esm migration:run -- -d path-to-datasource-config
```

```
npx typeorm-ts-node-esm migration:generate ./src/migrations/update-post-table -d ./src/data-source.ts
```

This command will execute all pending migrations and run them in a sequence ordered by their timestamps.
This means all sql queries written in the `up` methods of your created migrations will be executed.
That's all! Now you have your database schema up-to-date.

---

# Extra options

> Timestamp

## Timestamp​

If you need to specify a timestamp for the migration name, use the `-t` (alias for `--timestamp`) and pass the timestamp (should be a non-negative number)

```
typeorm -t <specific-timestamp> migration:{create|generate}
```

You can get a timestamp from:

```
Date.now()/* OR */ new Date().getTime()
```

---

# Faking Migrations and Rollbacks

> You can also fake run a migration using the --fake flag (-f for short). This will add the migration

You can also fake run a migration using the `--fake` flag (`-f` for short). This will add the migration
to the migrations table without running it. This is useful for migrations created after manual changes
have already been made to the database or when migrations have been run externally
(e.g. by another tool or application), and you still would like to keep a consistent migration history.

```
typeorm migration:run -d path-to-datasource-config --fake
```

This is also possible with rollbacks.

```
typeorm migration:revert -d path-to-datasource-config --fake
```

### Transaction modes​

By default, TypeORM will run all your migrations within a single wrapping transaction.
This corresponds to the `--transaction all` flag.
If you require more fine grained transaction control, you can use the `--transaction each` flag to wrap every migration individually, or the `--transaction none` flag to opt out of wrapping the migrations in transactions altogether.

In addition to these flags, you can also override the transaction behavior on a per-migration basis by setting the `transaction` property on the `MigrationInterface` to `true` or `false`. This only works in the `each` or `none` transaction mode.

```
import { MigrationInterface, QueryRunner } from "typeorm"export class AddIndexTIMESTAMP implements MigrationInterface {    transaction = false    async up(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(            `CREATE INDEX CONCURRENTLY post_names_idx ON post(name)`,        )    }    async down(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(`DROP INDEX CONCURRENTLY post_names_idx`)    }}
```

---

# Generating

> TypeORM is able to automatically generate migration files based on the changes you made to the entities, comparing them with existing database schema on the server.

TypeORM is able to automatically generate migration files based on the changes you made to the entities, comparing them with existing database schema on the server.

Automatic migration generation creates a new migration file and writes all sql queries that must be executed to update the database. If no changes are detected, the command will exit with code `1`.

Let's say you have a `Post` entity with a `title` column, and you have changed the name `title` to `name`.

You can generate migration with of the following command:

```
typeorm migration:generate -d <path/to/datasource> <migration-name>
```

The `-d` argument value should specify the path where your [DataSource](https://typeorm.io/docs/data-source/data-source) instance is defined.

Alternatively you can also specify name with `--name` param

```
typeorm migration:generate -- -d <path/to/datasource> --name=<migration-name>
```

or use a full path:

```
typeorm migration:generate -d <path/to/datasource> <path/to/migrations>/<migration-name>
```

Assuming you used `post-refactoring` as a name, it will generate a new file called `{TIMESTAMP}-post-refactoring.ts` with the following content:

```
import { MigrationInterface, QueryRunner } from "typeorm"export class PostRefactoringTIMESTAMP implements MigrationInterface {    async up(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "title" RENAME TO "name"`,        )    }    async down(queryRunner: QueryRunner): Promise<void> {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "name" RENAME TO "title"`,        )    }}
```

Alternatively, you can also output your migrations as Javascript files using the `o` (alias for `--outputJs`) flag. This is useful for Javascript only projects in which TypeScript additional packages are not installed. This command, will generate a new migration file `{TIMESTAMP}-PostRefactoring.js` with the following content:

```
/** * @typedef {import('typeorm').MigrationInterface} MigrationInterface * @typedef {import('typeorm').QueryRunner} QueryRunner *//** * @class * @implements {MigrationInterface} */module.exports = class PostRefactoringTIMESTAMP {    /**     * @param {QueryRunner} queryRunner     */    async up(queryRunner) {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "title" RENAME TO "name"`,        )    }    /**     * @param {QueryRunner} queryRunner     */    async down(queryRunner) {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "name" RENAME TO "title"`,        )    }}
```

By default, it generates CommonJS JavaScript code with the `o` (alias for `--outputJs`) flag, but you can also generate ESM code with the `esm` flag. This is useful for Javascript projects that use ESM:

```
/** * @typedef {import('typeorm').MigrationInterface} MigrationInterface * @typedef {import('typeorm').QueryRunner} QueryRunner *//** * @class * @implements {MigrationInterface} */export class PostRefactoringTIMESTAMP {    /**     * @param {QueryRunner} queryRunner     */    async up(queryRunner) {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "title" RENAME TO "name"`,        )    }    /**     * @param {QueryRunner} queryRunner     */    async down(queryRunner) {        await queryRunner.query(            `ALTER TABLE "post" ALTER COLUMN "name" RENAME TO "title"`,        )    }}
```

See, you don't need to write the queries on your own.

The rule of thumb for generating migrations is that you generate them after **each** change you made to your models. To apply multi-line formatting to your generated migration queries, use the `p` (alias for `--pretty`) flag.

---

# Reverting

> If for some reason you want to revert the changes, you can run:

If for some reason you want to revert the changes, you can run:

```
typeorm migration:revert -- -d path-to-datasource-config
```

This command will execute `down` in the latest executed migration.

If you need to revert multiple migrations you must call this command multiple times.

---

# Setup

> Before working with migrations you need to setup your DataSource options properly:

Before working with migrations you need to setup your [DataSource](https://typeorm.io/docs/data-source/data-source) options properly:

```
export default new DataSource({    // basic setup    synchronize: false,    migrations: [ /*...*/ ],    // optional    migrationsRun: false,    migrationsTableName: 'migrations',    migrationsTransactionMode: 'all'    // other options...})
```

## synchronise​

Turning off automatic schema synchronisation is essential for working with migrations. Otherwise they would make no sense.

## migrations​

Defines list of migrations that need to be loaded by TypeORM. It accepts both migration classes and directories from which to load.

The easiest is to specify the directory where your migration files are located (glob patterns are supported):

```
migrations: [__dirname + '/migration/**/*{.js,.ts}']
```

Defining both `.js` and `.ts` extensions would allow you to run migrations in development and from compiled to JavaScript for production (eg. from Docker image).

Alternatively you could also specify exact classes to get more fine grained control:

```
import FirstMigration from 'migrations/TIMESTAMP-first-migration'import SecondMigration from 'migrations/TIMESTAMP-second-migration'export default new DataSource({  migrations: [FirstMigration, SecondMigration]})
```

but it also requires more manual work and can be error prone.

- `migrationsRun` - Indicates if [migrations](https://typeorm.io/docs/migrations/why) should be auto-run on every application launch.

## Optional settings​

### migrationsRun​

Indicates if migrations should be auto-run on every application launch. Default: `false`

### migrationsTableName​

You might want to specify the name of the table that will store information about executed migrations. By default it is called `'migrations'`.

```
migrationsTableName: 'some_custom_migrations_table'
```

### migrationsTransactionMode​

Controls transaction mode when running migrations. Possible options are:

- `all` (*default*) - wraps migrations run into a single transaction
- `none`
- `each`

---

# Status

> To show all migrations and whether they've been run or not use following command:

To show all migrations and whether they've been run or not use following command:

```
typeorm migration:show  -- -d path-to-datasource-config
```

[X] = Migration has been ran

[ ] = Migration is pending/unapplied

---

# Vite

> Using TypeORM in a Vite project is pretty straight forward. However, when you use migrations, you will run into "...migration name is wrong. Migration class name should have a

Using TypeORM in a [Vite](https://vite.dev) project is pretty straight forward. However, when you use [migrations](https://typeorm.io/docs/migrations/why), you will run into "...migration name is wrong. Migration class name should have a
JavaScript timestamp appended." errors when running the production build.
On production builds, files are [optimized by default](https://vite.dev/config/build-options#build-minify) which includes mangling your code in order to minimize file sizes.

You have 3 options to mitigate this. The 3 options are shown below as diff to this basic `vite.config.ts`

```
import legacy from "@vitejs/plugin-legacy"import vue from "@vitejs/plugin-vue"import path from "path"import { defineConfig } from "vite"// https://vitejs.dev/config/export default defineConfig({    build: {        sourcemap: true,    },    plugins: [vue(), legacy()],    resolve: {        alias: {            "@": path.resolve(__dirname, "./src"),        },    },})
```

## Option 1: Disable minify​

This is the most crude option and will result in significantly larger files. Add `build.minify = false` to your config.

```
--- basic vite.config.ts+++ disable minify vite.config.ts@@ -7,6 +7,7 @@ export default defineConfig({   build: {     sourcemap: true,+    minify: false,   },   plugins: [vue(), legacy()],   resolve: {
```

## Option 2: Disable esbuild minify identifiers​

Vite uses esbuild as the default minifier. You can disable mangling of identifiers by adding `esbuild.minifyIdentifiers = false` to your config.
This will result in smaller file sizes, but depending on your code base you will get diminishing returns as all identifiers will be kept at full length.

```
--- basic vite.config.ts+++ disable esbuild minify identifiers vite.config.ts@@ -8,6 +8,7 @@   build: {     sourcemap: true,   },+  esbuild: { minifyIdentifiers: false },   plugins: [vue(), legacy()],   resolve: {
```

## Option 3: Use terser as minifier while keeping only the migration class names​

Vite supports using terser as minifier. Terser is slower then esbuild, but offers more fine grained control over what to minify.
Add `minify: 'terser'` with `terserOptions.mangle.keep_classnames: /^Migrations\d+$/` and `terserOptions.compress.keep_classnames: /^Migrations\d+$/` to your config.
These options will make sure classnames that start with "Migrations" and end with numbers are not renamed during minification.

Make sure terser is available as dev dependency in your project: `npm add -D terser`.

```
--- basic vite.config.ts+++ terser keep migration class names vite.config.ts@@ -7,6 +7,11 @@ export default defineConfig({   build: {     sourcemap: true,+    minify: 'terser',+    terserOptions: {+      mangle: { keep_classnames: /^Migrations\d+$/ },+      compress: { keep_classnames: /^Migrations\d+$/ },+    },   },   plugins: [vue(), legacy()],   resolve: {
```

---

# How migrations work?

> Once you get into production you'll need to synchronize model changes into the database.

Once you get into production you'll need to synchronize model changes into the database.
Typically, it is unsafe to use `synchronize: true` for schema synchronization on production once
you get data in your database. Here is where migrations come to help.

A migration is just a single file with SQL queries to update a database schema
and apply new changes to an existing database.

Let's say you already have a database and a `Post` entity:

```
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm"@Entity()export class Post {    @PrimaryGeneratedColumn()    id: number    @Column()    title: string    @Column()    text: string}
```

And your entity worked in production for months without any changes.
You have thousands of posts in your database.

Now you need to make a new release and rename `title` to `name`.
What would you do?

You need to create a new migration with the following SQL query (PostgreSQL dialect):

```
ALTER TABLE "post" RENAME COLUMN "title" TO "name";
```

Once you run this SQL query your database schema is ready to work with your new codebase.
TypeORM provides a place where you can write such sql queries and run them when needed.
This place is called "migrations".
