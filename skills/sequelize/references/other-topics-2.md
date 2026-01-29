# Extending Data Types and more

# Extending Data Types

> Most likely the type you are trying to implement is already included in DataTypes. If a new datatype is not included, this manual will show how to write it yourself.

Version: v6 - stable

Most likely the type you are trying to implement is already included in [DataTypes](https://sequelize.org/docs/v6/other-topics/other-data-types/). If a new datatype is not included, this manual will show how to write it yourself.

Sequelize doesn't create new datatypes in the database. This tutorial explains how to make Sequelize recognize new datatypes and assumes that those new datatypes are already created in the database.

To extend Sequelize datatypes, do it before any Sequelize instance is created.

## Example​

In this example, we will create a type called `SOMETYPE` that replicates the built-in datatype `DataTypes.INTEGER(11).ZEROFILL.UNSIGNED`.

```
const { Sequelize, DataTypes, Utils } = require('Sequelize');createTheNewDataType();const sequelize = new Sequelize('sqlite::memory:');function createTheNewDataType() {  class SOMETYPE extends DataTypes.ABSTRACT {    // Mandatory: complete definition of the new type in the database    toSql() {      return 'INTEGER(11) UNSIGNED ZEROFILL';    }    // Optional: validator function    validate(value, options) {      return typeof value === 'number' && !Number.isNaN(value);    }    // Optional: sanitizer    _sanitize(value) {      // Force all numbers to be positive      return value < 0 ? 0 : Math.round(value);    }    // Optional: value stringifier before sending to database    _stringify(value) {      return value.toString();    }    // Optional: parser for values received from the database    static parse(value) {      return Number.parseInt(value);    }  }  // Mandatory: set the type key  SOMETYPE.prototype.key = SOMETYPE.key = 'SOMETYPE';  // Mandatory: add the new type to DataTypes. Optionally wrap it on `Utils.classToInvokable` to  // be able to use this datatype directly without having to call `new` on it.  DataTypes.SOMETYPE = Utils.classToInvokable(SOMETYPE);  // Optional: disable escaping after stringifier. Do this at your own risk, since this opens opportunity for SQL injections.  // DataTypes.SOMETYPE.escape = false;}
```

After creating this new datatype, you need to map this datatype in each database dialect and make some adjustments.

## PostgreSQL​

Let's say the name of the new datatype is `pg_new_type` in the postgres database. That name has to be mapped to `DataTypes.SOMETYPE`. Additionally, it is required to create a child postgres-specific datatype.

```
function createTheNewDataType() {  // [...]  const PgTypes = DataTypes.postgres;  // Mandatory: map postgres datatype name  DataTypes.SOMETYPE.types.postgres = ['pg_new_type'];  // Mandatory: create a postgres-specific child datatype with its own parse  // method. The parser will be dynamically mapped to the OID of pg_new_type.  PgTypes.SOMETYPE = function SOMETYPE() {    if (!(this instanceof PgTypes.SOMETYPE)) {      return new PgTypes.SOMETYPE();    }    DataTypes.SOMETYPE.apply(this, arguments);  }  const util = require('util'); // Built-in Node package  util.inherits(PgTypes.SOMETYPE, DataTypes.SOMETYPE);  // Mandatory: create, override or reassign a postgres-specific parser  // PgTypes.SOMETYPE.parse = value => value;  PgTypes.SOMETYPE.parse = DataTypes.SOMETYPE.parse || x => x;  // Optional: add or override methods of the postgres-specific datatype  // like toSql, escape, validate, _stringify, _sanitize...}
```

### Ranges​

After a new range type has been [defined in postgres](https://www.postgresql.org/docs/current/static/rangetypes.html#RANGETYPES-DEFINING), it is trivial to add it to Sequelize.

In this example the name of the postgres range type is `SOMETYPE_range` and the name of the underlying postgres datatype is `pg_new_type`. The key of `subtypes` and `castTypes` is the key of the Sequelize datatype `DataTypes.SOMETYPE.key`, in lower case.

```
function createTheNewDataType() {  // [...]  // Add postgresql range, SOMETYPE comes from DataType.SOMETYPE.key in lower case  DataTypes.RANGE.types.postgres.subtypes.SOMETYPE = 'SOMETYPE_range';  DataTypes.RANGE.types.postgres.castTypes.SOMETYPE = 'pg_new_type';}
```

The new range can be used in model definitions as `DataTypes.RANGE(DataTypes.SOMETYPE)` or `DataTypes.RANGE(DataTypes.SOMETYPE)`.

---

# Hooks

> Hooks (also known as lifecycle events), are functions which are called before and after calls in sequelize are executed. For example, if you want to always set a value on a model before saving it, you can add a beforeUpdate hook.

Version: v6 - stable

Hooks (also known as lifecycle events), are functions which are called before and after calls in sequelize are executed. For example, if you want to always set a value on a model before saving it, you can add a `beforeUpdate` hook.

**Note:** *You can't use hooks with instances. Hooks are used with models.*

## Available hooks​

Sequelize provides a lot of hooks. The full list can be found in directly in the [source code - src/hooks.js](https://github.com/sequelize/sequelize/blob/v6/src/hooks.js#L7).

## Hooks firing order​

The diagram below shows the firing order for the most common hooks.

*Note:this list is not exhaustive.*

```
(1)  beforeBulkCreate(instances, options)  beforeBulkDestroy(options)  beforeBulkUpdate(options)(2)  beforeValidate(instance, options)[... validation happens ...](3)  afterValidate(instance, options)  validationFailed(instance, options, error)(4)  beforeCreate(instance, options)  beforeDestroy(instance, options)  beforeUpdate(instance, options)  beforeSave(instance, options)  beforeUpsert(values, options)[... creation/update/destruction happens ...](5)  afterCreate(instance, options)  afterDestroy(instance, options)  afterUpdate(instance, options)  afterSave(instance, options)  afterUpsert(created, options)(6)  afterBulkCreate(instances, options)  afterBulkDestroy(options)  afterBulkUpdate(options)
```

## Declaring Hooks​

Arguments to hooks are passed by reference. This means, that you can change the values, and this will be reflected in the insert / update statement. A hook may contain async actions - in this case the hook function should return a promise.

There are currently three ways to programmatically add hooks:

```
// Method 1 via the .init() methodclass User extends Model {}User.init(  {    username: DataTypes.STRING,    mood: {      type: DataTypes.ENUM,      values: ['happy', 'sad', 'neutral'],    },  },  {    hooks: {      beforeValidate: (user, options) => {        user.mood = 'happy';      },      afterValidate: (user, options) => {        user.username = 'Toni';      },    },    sequelize,  },);// Method 2 via the .addHook() methodUser.addHook('beforeValidate', (user, options) => {  user.mood = 'happy';});User.addHook('afterValidate', 'someCustomName', (user, options) => {  return Promise.reject(new Error("I'm afraid I can't let you do that!"));});// Method 3 via the direct methodUser.beforeCreate(async (user, options) => {  const hashedPassword = await hashPassword(user.password);  user.password = hashedPassword;});User.afterValidate('myHookAfter', (user, options) => {  user.username = 'Toni';});
```

## Removing hooks​

Only a hook with name param can be removed.

```
class Book extends Model {}Book.init(  {    title: DataTypes.STRING,  },  { sequelize },);Book.addHook('afterCreate', 'notifyUsers', (book, options) => {  // ...});Book.removeHook('afterCreate', 'notifyUsers');
```

You can have many hooks with same name. Calling `.removeHook()` will remove all of them.

## Global / universal hooks​

Global hooks are hooks that are run for all models. They are especially useful for plugins and can define behaviours that you want for all your models, for example to allow customization on timestamps using `sequelize.define` on your models:

```
const User = sequelize.define(  'User',  {},  {    tableName: 'users',    hooks: {      beforeCreate: (record, options) => {        record.dataValues.createdAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');        record.dataValues.updatedAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');      },      beforeUpdate: (record, options) => {        record.dataValues.updatedAt = new Date()          .toISOString()          .replace(/T/, ' ')          .replace(/\..+/g, '');      },    },  },);
```

They can be defined in many ways, which have slightly different semantics:

### Default Hooks (on Sequelize constructor options)​

```
const sequelize = new Sequelize(..., {  define: {    hooks: {      beforeCreate() {        // Do stuff      }    }  }});
```

This adds a default hook to all models, which is run if the model does not define its own `beforeCreate` hook:

```
const User = sequelize.define('User', {});const Project = sequelize.define(  'Project',  {},  {    hooks: {      beforeCreate() {        // Do other stuff      },    },  },);await User.create({}); // Runs the global hookawait Project.create({}); // Runs its own hook (because the global hook is overwritten)
```

### Permanent Hooks (withsequelize.addHook)​

```
sequelize.addHook('beforeCreate', () => {  // Do stuff});
```

This hook is always run, whether or not the model specifies its own `beforeCreate` hook. Local hooks are always run before global hooks:

```
const User = sequelize.define('User', {});const Project = sequelize.define(  'Project',  {},  {    hooks: {      beforeCreate() {        // Do other stuff      },    },  },);await User.create({}); // Runs the global hookawait Project.create({}); // Runs its own hook, followed by the global hook
```

Permanent hooks may also be defined in the options passed to the Sequelize constructor:

```
new Sequelize(..., {  hooks: {    beforeCreate() {      // do stuff    }  }});
```

Note that the above is not the same as the *Default Hooks* mentioned above. That one uses the `define` option of the constructor. This one does not.

### Connection Hooks​

Sequelize provides four hooks that are executed immediately before and after a database connection is obtained or released:

- `sequelize.beforeConnect(callback)`
  - The callback has the form `async (config) => /* ... */`
- `sequelize.afterConnect(callback)`
  - The callback has the form `async (connection, config) => /* ... */`
- `sequelize.beforeDisconnect(callback)`
  - The callback has the form `async (connection) => /* ... */`
- `sequelize.afterDisconnect(callback)`
  - The callback has the form `async (connection) => /* ... */`

These hooks can be useful if you need to asynchronously obtain database credentials, or need to directly access the low-level database connection after it has been created.

For example, we can asynchronously obtain a database password from a rotating token store, and mutate Sequelize's configuration object with the new credentials:

```
sequelize.beforeConnect(async config => {  config.password = await getAuthToken();});
```

You can also use two hooks that are executed immediately before and after a pool connection is acquired:

- `sequelize.beforePoolAcquire(callback)`
  - The callback has the form `async (config) => /* ... */`
- `sequelize.afterPoolAcquire(callback)`
  - The callback has the form `async (connection, config) => /* ... */`

These hooks may *only* be declared as a permanent global hook, as the connection pool is shared by all models.

## Instance hooks​

The following hooks will emit whenever you're editing a single object:

- `beforeValidate`
- `afterValidate` / `validationFailed`
- `beforeCreate` / `beforeUpdate` / `beforeSave` / `beforeDestroy`
- `afterCreate` / `afterUpdate` / `afterSave` / `afterDestroy`

```
User.beforeCreate(user => {  if (user.accessLevel > 10 && user.username !== 'Boss') {    throw new Error("You can't grant this user an access level above 10!");  }});
```

The following example will throw an error:

```
try {  await User.create({ username: 'Not a Boss', accessLevel: 20 });} catch (error) {  console.log(error); // You can't grant this user an access level above 10!}
```

The following example will be successful:

```
const user = await User.create({ username: 'Boss', accessLevel: 20 });console.log(user); // user object with username 'Boss' and accessLevel of 20
```

### Model hooks​

Sometimes you'll be editing more than one record at a time by using methods like `bulkCreate`, `update` and `destroy`. The following hooks will emit whenever you're using one of those methods:

- `YourModel.beforeBulkCreate(callback)`
  - The callback has the form `(instances, options) => /* ... */`
- `YourModel.beforeBulkUpdate(callback)`
  - The callback has the form `(options) => /* ... */`
- `YourModel.beforeBulkDestroy(callback)`
  - The callback has the form `(options) => /* ... */`
- `YourModel.afterBulkCreate(callback)`
  - The callback has the form `(instances, options) => /* ... */`
- `YourModel.afterBulkUpdate(callback)`
  - The callback has the form `(options) => /* ... */`
- `YourModel.afterBulkDestroy(callback)`
  - The callback has the form `(options) => /* ... */`

Note: methods like `bulkCreate` do not emit individual hooks by default - only the bulk hooks. However, if you want individual hooks to be emitted as well, you can pass the `{ individualHooks: true }` option to the query call. However, this can drastically impact performance, depending on the number of records involved (since, among other things, all instances will be loaded into memory). Examples:

```
await Model.destroy({  where: { accessLevel: 0 },  individualHooks: true,});// This will select all records that are about to be deleted and emit `beforeDestroy` and `afterDestroy` on each instance.await Model.update(  { username: 'Tony' },  {    where: { accessLevel: 0 },    individualHooks: true,  },);// This will select all records that are about to be updated and emit `beforeUpdate` and `afterUpdate` on each instance.
```

If you use `Model.bulkCreate(...)` with the `updateOnDuplicate` option, changes made in the hook to fields that aren't given in the `updateOnDuplicate` array will not be persisted to the database. However it is possible to change the `updateOnDuplicate` option inside the hook if this is what you want.

```
User.beforeBulkCreate((users, options) => {  for (const user of users) {    if (user.isMember) {      user.memberSince = new Date();    }  }  // Add `memberSince` to updateOnDuplicate otherwise it won't be persisted  if (options.updateOnDuplicate && !options.updateOnDuplicate.includes('memberSince')) {    options.updateOnDuplicate.push('memberSince');  }});// Bulk updating existing users with updateOnDuplicate optionawait Users.bulkCreate(  [    { id: 1, isMember: true },    { id: 2, isMember: false },  ],  {    updateOnDuplicate: ['isMember'],  },);
```

## Exceptions​

Only **Model methods** trigger hooks. This means there are a number of cases where Sequelize will interact with the database without triggering hooks.
These include but are not limited to:

- Instances being deleted by the database because of an `ON DELETE CASCADE` constraint, [except if thehooksoption is true](#hooks-for-cascade-deletes).
- Instances being updated by the database because of a `SET NULL` or `SET DEFAULT` constraint.
- [Raw queries](https://sequelize.org/docs/v6/core-concepts/raw-queries/).
- All QueryInterface methods.

If you need to react to these events, consider using your database's native triggers and notification system instead.

## Hooks for cascade deletes​

As indicated in [Exceptions](#exceptions), Sequelize will not trigger hooks when instances are deleted by the database because of an `ON DELETE CASCADE` constraint.

However, if you set the `hooks` option to `true` when defining your association, Sequelize will trigger the `beforeDestroy` and `afterDestroy` hooks for the deleted instances.

 caution

Using this option is discouraged for the following reasons:

- This option requires many extra queries. The `destroy` method normally executes a single query.
  If this option is enabled, an extra `SELECT` query, as well as an extra `DELETE` query for each row returned by the select will be executed.
- If you do not run this query in a transaction, and an error occurs, you may end up with some rows deleted and some not deleted.
- This option only works when the *instance* version of `destroy` is used. The static version will not trigger the hooks, even with `individualHooks`.
- This option will not work in `paranoid` mode.
- This option will not work if you only define the association on the model that owns the foreign key. You need to define the reverse association as well.

This option is considered legacy. We highly recommend using your database's triggers and notification system if you need to be notified of database changes.

Here is an example of how to use this option:

```
import { Model } from 'sequelize';const sequelize = new Sequelize({  /* options */});class User extends Model {}User.init({}, { sequelize });class Post extends Model {}Post.init({}, { sequelize });Post.beforeDestroy(() => {  console.log('Post has been destroyed');});// This "hooks" option will cause the "beforeDestroy" and "afterDestroy"User.hasMany(Post, { onDelete: 'cascade', hooks: true });await sequelize.sync({ force: true });const user = await User.create();const post = await Post.create({ userId: user.id });// this will log "Post has been destroyed"await user.destroy();
```

## Associations​

For the most part hooks will work the same for instances when being associated.

### One-to-One and One-to-Many associations​

- When using `add`/`set` mixin methods the `beforeUpdate` and `afterUpdate` hooks will run.

### Many-to-Many associations​

- When using `add` mixin methods for `belongsToMany` relationships (that will add one or more records to the junction table) the `beforeBulkCreate` and `afterBulkCreate` hooks in the junction model will run.
  - If `{ individualHooks: true }` was passed to the call, then each individual hook will also run.
- When using `remove` mixin methods for `belongsToMany` relationships (that will remove one or more records to the junction table) the `beforeBulkDestroy` and `afterBulkDestroy` hooks in the junction model will run.
  - If `{ individualHooks: true }` was passed to the call, then each individual hook will also run.

If your association is Many-to-Many, you may be interested in firing hooks on the through model when using the `remove` call. Internally, sequelize is using `Model.destroy` resulting in calling the `bulkDestroy` instead of the `before/afterDestroy` hooks on each through instance.

## Hooks and Transactions​

Many model operations in Sequelize allow you to specify a transaction in the options parameter of the method. If a transaction *is* specified in the original call, it will be present in the options parameter passed to the hook function. For example, consider the following snippet:

```
User.addHook('afterCreate', async (user, options) => {  // We can use `options.transaction` to perform some other call  // using the same transaction of the call that triggered this hook  await User.update(    { mood: 'sad' },    {      where: {        id: user.id,      },      transaction: options.transaction,    },  );});await sequelize.transaction(async t => {  await User.create(    {      username: 'someguy',      mood: 'happy',    },    {      transaction: t,    },  );});
```

If we had not included the transaction option in our call to `User.update` in the preceding code, no change would have occurred, since our newly created user does not exist in the database until the pending transaction has been committed.

### Internal Transactions​

It is very important to recognize that sequelize may make use of transactions internally for certain operations such as `Model.findOrCreate`. If your hook functions execute read or write operations that rely on the object's presence in the database, or modify the object's stored values like the example in the preceding section, you should always specify `{ transaction: options.transaction }`:

- If a transaction was used, then `{ transaction: options.transaction }` will ensure it is used again;
- Otherwise, `{ transaction: options.transaction }` will be equivalent to `{ transaction: undefined }`, which won't use a transaction (which is ok).

This way your hooks will always behave correctly.

---

# Indexes

> Sequelize supports adding indexes to the model definition which will be created on sequelize.sync().

Version: v6 - stable

Sequelize supports adding indexes to the model definition which will be created on [sequelize.sync()](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-method-sync).

```
const User = sequelize.define(  'User',  {    /* attributes */  },  {    indexes: [      // Create a unique index on email      {        unique: true,        fields: ['email'],      },      // Creates a gin index on data with the jsonb_path_ops operator      {        fields: ['data'],        using: 'gin',        operator: 'jsonb_path_ops',      },      // By default index name will be [table]_[fields]      // Creates a multi column partial index      {        name: 'public_by_author',        fields: ['author', 'status'],        where: {          status: 'public',        },      },      // A BTREE index with an ordered field      {        name: 'title_index',        using: 'BTREE',        fields: [          'author',          {            name: 'title',            collate: 'en_US',            order: 'DESC',            length: 5,          },        ],      },    ],  },);
```

---

# Working with Legacy Tables

> While out of the box Sequelize will seem a bit opinionated it's easy to work legacy tables and forward proof your application by defining (otherwise generated) table and field names.

Version: v6 - stable

While out of the box Sequelize will seem a bit opinionated it's easy to work legacy tables and forward proof your application by defining (otherwise generated) table and field names.

## Tables​

```
class User extends Model {}User.init(  {    // ...  },  {    modelName: 'user',    tableName: 'users',    sequelize,  },);
```

## Fields​

```
class MyModel extends Model {}MyModel.init(  {    userId: {      type: DataTypes.INTEGER,      field: 'user_id',    },  },  { sequelize },);
```

## Primary keys​

Sequelize will assume your table has a `id` primary key property by default.

To define your own primary key:

```
class Collection extends Model {}Collection.init(  {    uid: {      type: DataTypes.INTEGER,      primaryKey: true,      autoIncrement: true, // Automatically gets converted to SERIAL for postgres    },  },  { sequelize },);class Collection extends Model {}Collection.init(  {    uuid: {      type: DataTypes.UUID,      primaryKey: true,    },  },  { sequelize },);
```

And if your model has no primary key at all you can use `Model.removeAttribute('id');`

Instances without primary keys can still be retrieved using `Model.findOne` and `Model.findAll`.
  While it's currently possible to use their instance methods (`instance.save`, `instance.update`, etc…), doing this will lead to subtle bugs,
and is planned for removal in a future major update.

 info

If your model has no primary keys, you need to use the static equivalent of the following instance methods, and provide your own `where` parameter:

- `instance.save`: `Model.update`
- `instance.update`: `Model.update`
- `instance.reload`: `Model.findOne`
- `instance.destroy`: `Model.destroy`
- `instance.restore`: `Model.restore`
- `instance.decrement`: `Model.decrement`
- `instance.increment`: `Model.increment`

## Foreign keys​

```
// 1:1Organization.belongsTo(User, { foreignKey: 'owner_id' });User.hasOne(Organization, { foreignKey: 'owner_id' });// 1:MProject.hasMany(Task, { foreignKey: 'tasks_pk' });Task.belongsTo(Project, { foreignKey: 'tasks_pk' });// N:MUser.belongsToMany(Role, {  through: 'user_has_roles',  foreignKey: 'user_role_user_id',});Role.belongsToMany(User, {  through: 'user_has_roles',  foreignKey: 'roles_identifier',});
```

---

# Legal Notice

> License

Version: v6 - stable

## License​

Sequelize library is distributed with MIT license. You can find original license [here.](https://github.com/sequelize/sequelize/blob/main/LICENSE)

```
MIT LicenseCopyright (c) 2014-present Sequelize contributorsPermission is hereby granted, free of charge, to any person obtaining a copyof this software and associated documentation files (the "Software"), to dealin the Software without restriction, including without limitation the rightsto use, copy, modify, merge, publish, distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software isfurnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in allcopies or substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THESOFTWARE.
```

## AUTHOR(S)​

```
Main author:Sascha DepoldUhlandstr. 16010719 Berlinsascha [at] depold [dot] com[plus] 49 152 [slash] 03878582
```

## INHALTLICHE VERANTWORTUNG​

```
Ich übernehme keine Haftung für ausgehende Links.Daher musst du dich bei Problemen an deren Betreiber wenden!
```

---

# Migrations

> Just like you use version control systems such as Git to manage changes in your source code, you can use migrations to keep track of changes to the database. With migrations you can transfer your existing database into another state and vice versa: Those state transitions are saved in migration files, which describe how to get to the new state and how to revert the changes in order to get back to the old state.

Version: v6 - stable

Just like you use [version control](https://en.wikipedia.org/wiki/Version_control) systems such as [Git](https://en.wikipedia.org/wiki/Git) to manage changes in your source code, you can use **migrations** to keep track of changes to the database. With migrations you can transfer your existing database into another state and vice versa: Those state transitions are saved in migration files, which describe how to get to the new state and how to revert the changes in order to get back to the old state.

You will need the [Sequelize Command-Line Interface (CLI)](https://github.com/sequelize/cli). The CLI ships support for migrations and project bootstrapping.

A Migration in Sequelize is a javascript file which exports two functions, `up` and `down`, that dictates how to perform the migration and undo it. You define those functions manually, but you don't call them manually; they will be called automatically by the CLI. In these functions, you should simply perform whatever queries you need, with the help of `sequelize.query` and whichever other methods Sequelize provides to you. There is no extra magic beyond that.

## Installing the CLI​

To install the Sequelize CLI:

```
npm install --save-dev sequelize-cli
```

For details see the [CLI GitHub repository](https://github.com/sequelize/cli).

## Project bootstrapping​

To create an empty project you will need to execute `init` command

```
npx sequelize-cli init
```

This will create following folders

- `config`, contains config file, which tells CLI how to connect with database
- `models`, contains all models for your project
- `migrations`, contains all migration files
- `seeders`, contains all seed files

### Configuration​

Before continuing further we will need to tell the CLI how to connect to the database. To do that let's open default config file `config/config.json`. It looks something like this:

```
{  "development": {    "username": "root",    "password": null,    "database": "database_development",    "host": "127.0.0.1",    "dialect": "mysql"  },  "test": {    "username": "root",    "password": null,    "database": "database_test",    "host": "127.0.0.1",    "dialect": "mysql"  },  "production": {    "username": "root",    "password": null,    "database": "database_production",    "host": "127.0.0.1",    "dialect": "mysql"  }}
```

Note that the Sequelize CLI assumes mysql by default. If you're using another dialect, you need to change the content of the `"dialect"` option.

Now edit this file and set correct database credentials and dialect. The keys of the objects (e.g. "development") are used on `model/index.js` for matching `process.env.NODE_ENV` (When undefined, "development" is a default value).

Sequelize will use the default connection port for each dialect (for example, for postgres, it is port 5432). If you need to specify a different port, use the `"port"` field (it is not present by default in `config/config.js` but you can simply add it).

**Note:** *If your database doesn't exist yet, you can just calldb:createcommand. With proper access it will create that database for you.*

## Creating the first Model (and Migration)​

Once you have properly configured CLI config file you are ready to create your first migration. It's as simple as executing a simple command.

We will use `model:generate` command. This command requires two options:

- `name`: the name of the model;
- `attributes`: the list of model attributes.

Let's create a model named `User`.

```
npx sequelize-cli model:generate --name User --attributes firstName:string,lastName:string,email:string
```

This will:

- Create a model file `user` in `models` folder;
- Create a migration file with name like `XXXXXXXXXXXXXX-create-user.js` in `migrations` folder.

**Note:** *Sequelize will only use Model files, it's the table representation. On the other hand, the migration file is a change in that model or more specifically that table, used by CLI. Treat migrations like a commit or a log for some change in database.*

## Running Migrations​

Until this step, we haven't inserted anything into the database. We have just created the required model and migration files for our first model, `User`. Now to actually create that table in the database you need to run `db:migrate` command.

```
npx sequelize-cli db:migrate
```

This command will execute these steps:

- Will ensure a table called `SequelizeMeta` in database. This table is used to record which migrations have run on the current database
- Start looking for any migration files which haven't run yet. This is possible by checking `SequelizeMeta` table. In this case it will run `XXXXXXXXXXXXXX-create-user.js` migration, which we created in last step.
- Creates a table called `Users` with all columns as specified in its migration file.

## Undoing Migrations​

Now our table has been created and saved in the database. With migration you can revert to old state by just running a command.

You can use `db:migrate:undo`, this command will revert the most recent migration.

```
npx sequelize-cli db:migrate:undo
```

You can revert back to the initial state by undoing all migrations with the `db:migrate:undo:all` command. You can also revert back to a specific migration by passing its name with the `--to` option.

```
npx sequelize-cli db:migrate:undo:all --to XXXXXXXXXXXXXX-create-posts.js
```

## Creating the first Seed​

Suppose we want to insert some data into a few tables by default. If we follow up on the previous example we can consider creating a demo user for the `User` table.

To manage all data migrations you can use seeders. Seed files are some change in data that can be used to populate database tables with sample or test data.

Let's create a seed file which will add a demo user to our `User` table.

```
npx sequelize-cli seed:generate --name demo-user
```

This command will create a seed file in `seeders` folder. File name will look something like `XXXXXXXXXXXXXX-demo-user.js`. It follows the same `up / down` semantics as the migration files.

Now we should edit this file to insert demo user to `User` table.

```
module.exports = {  up: (queryInterface, Sequelize) => {    return queryInterface.bulkInsert('Users', [      {        firstName: 'John',        lastName: 'Doe',        email: 'example@example.com',        createdAt: new Date(),        updatedAt: new Date(),      },    ]);  },  down: (queryInterface, Sequelize) => {    return queryInterface.bulkDelete('Users', null, {});  },};
```

## Running Seeds​

In last step you created a seed file; however, it has not been committed to the database. To do that we run a simple command.

```
npx sequelize-cli db:seed:all
```

This will execute that seed file and a demo user will be inserted into the `User` table.

**Note:** *Seeder execution history is not stored anywhere, unlike migrations, which use theSequelizeMetatable. If you wish to change this behavior, please read theStoragesection.*

## Undoing Seeds​

Seeders can be undone if they are using any storage. There are two commands available for that:

If you wish to undo the most recent seed:

```
npx sequelize-cli db:seed:undo
```

If you wish to undo a specific seed:

```
npx sequelize-cli db:seed:undo --seed name-of-seed-as-in-data
```

If you wish to undo all seeds:

```
npx sequelize-cli db:seed:undo:all
```

## Migration Skeleton​

The following skeleton shows a typical migration file.

```
module.exports = {  up: (queryInterface, Sequelize) => {    // logic for transforming into the new state  },  down: (queryInterface, Sequelize) => {    // logic for reverting the changes  },};
```

We can generate this file using `migration:generate`. This will create `xxx-migration-skeleton.js` in your migration folder.

```
npx sequelize-cli migration:generate --name migration-skeleton
```

The passed `queryInterface` object can be used to modify the database. The `Sequelize` object stores the available data types such as `STRING` or `INTEGER`. Function `up` or `down` should return a `Promise`. Let's look at an example:

```
module.exports = {  up: (queryInterface, Sequelize) => {    return queryInterface.createTable('Person', {      name: Sequelize.DataTypes.STRING,      isBetaMember: {        type: Sequelize.DataTypes.BOOLEAN,        defaultValue: false,        allowNull: false,      },    });  },  down: (queryInterface, Sequelize) => {    return queryInterface.dropTable('Person');  },};
```

The following is an example of a migration that performs two changes in the database, using an automatically-managed transaction to ensure that all instructions are successfully executed or rolled back in case of failure:

```
module.exports = {  up: (queryInterface, Sequelize) => {    return queryInterface.sequelize.transaction(t => {      return Promise.all([        queryInterface.addColumn(          'Person',          'petName',          {            type: Sequelize.DataTypes.STRING,          },          { transaction: t },        ),        queryInterface.addColumn(          'Person',          'favoriteColor',          {            type: Sequelize.DataTypes.STRING,          },          { transaction: t },        ),      ]);    });  },  down: (queryInterface, Sequelize) => {    return queryInterface.sequelize.transaction(t => {      return Promise.all([        queryInterface.removeColumn('Person', 'petName', { transaction: t }),        queryInterface.removeColumn('Person', 'favoriteColor', {          transaction: t,        }),      ]);    });  },};
```

The next example is of a migration that has a foreign key. You can use references to specify a foreign key:

```
module.exports = {  up: (queryInterface, Sequelize) => {    return queryInterface.createTable('Person', {      name: Sequelize.DataTypes.STRING,      isBetaMember: {        type: Sequelize.DataTypes.BOOLEAN,        defaultValue: false,        allowNull: false,      },      userId: {        type: Sequelize.DataTypes.INTEGER,        references: {          model: {            tableName: 'users',            schema: 'schema',          },          key: 'id',        },        allowNull: false,      },    });  },  down: (queryInterface, Sequelize) => {    return queryInterface.dropTable('Person');  },};
```

The next example is of a migration that uses async/await where you create an unique index on a new column, with a manually-managed transaction:

```
module.exports = {  async up(queryInterface, Sequelize) {    const transaction = await queryInterface.sequelize.transaction();    try {      await queryInterface.addColumn(        'Person',        'petName',        {          type: Sequelize.DataTypes.STRING,        },        { transaction },      );      await queryInterface.addIndex('Person', 'petName', {        fields: 'petName',        unique: true,        transaction,      });      await transaction.commit();    } catch (err) {      await transaction.rollback();      throw err;    }  },  async down(queryInterface, Sequelize) {    const transaction = await queryInterface.sequelize.transaction();    try {      await queryInterface.removeColumn('Person', 'petName', { transaction });      await transaction.commit();    } catch (err) {      await transaction.rollback();      throw err;    }  },};
```

The next example is of a migration that creates an unique index composed of multiple fields with a condition, which allows a relation to exist multiple times but only one can satisfy the condition:

```
module.exports = {  up: (queryInterface, Sequelize) => {    queryInterface      .createTable('Person', {        name: Sequelize.DataTypes.STRING,        bool: {          type: Sequelize.DataTypes.BOOLEAN,          defaultValue: false,        },      })      .then((queryInterface, Sequelize) => {        queryInterface.addIndex('Person', ['name', 'bool'], {          indicesType: 'UNIQUE',          where: { bool: 'true' },        });      });  },  down: (queryInterface, Sequelize) => {    return queryInterface.dropTable('Person');  },};
```

### The.sequelizercfile​

This is a special configuration file. It lets you specify the following options that you would usually pass as arguments to CLI:

- `env`: The environment to run the command in
- `config`: The path to the config file
- `options-path`: The path to a JSON file with additional options
- `migrations-path`: The path to the migrations folder
- `seeders-path`: The path to the seeders folder
- `models-path`: The path to the models folder
- `url`: The database connection string to use. Alternative to using --config files
- `debug`: When available show various debug information

Some scenarios where you can use it:

- You want to override default path to `migrations`, `models`, `seeders` or `config` folder.
- You want to rename `config.json` to something else like `database.json`

And a whole lot more. Let's see how you can use this file for custom configuration.

To begin, let's create the `.sequelizerc` file in the root directory of your project, with the following content:

```
// .sequelizercconst path = require('path');module.exports = {  config: path.resolve('config', 'database.json'),  'models-path': path.resolve('db', 'models'),  'seeders-path': path.resolve('db', 'seeders'),  'migrations-path': path.resolve('db', 'migrations'),};
```

With this config you are telling the CLI to:

- Use `config/database.json` file for config settings;
- Use `db/models` as models folder;
- Use `db/seeders` as seeders folder;
- Use `db/migrations` as migrations folder.

### Dynamic configuration​

The configuration file is by default a JSON file called `config.json`. But sometimes you need a dynamic configuration, for example to access environment variables or execute some other code to determine the configuration.

Thankfully, the Sequelize CLI can read from both `.json` and `.js` files. This can be setup with `.sequelizerc` file. You just have to provide the path to your `.js` file as the `config` option of your exported object:

```
const path = require('path');module.exports = {  config: path.resolve('config', 'config.js'),};
```

Now the Sequelize CLI will load `config/config.js` for getting configuration options.

An example of `config/config.js` file:

```
const fs = require('fs');module.exports = {  development: {    username: 'database_dev',    password: 'database_dev',    database: 'database_dev',    host: '127.0.0.1',    port: 3306,    dialect: 'mysql',    dialectOptions: {      bigNumberStrings: true,    },  },  test: {    username: process.env.CI_DB_USERNAME,    password: process.env.CI_DB_PASSWORD,    database: process.env.CI_DB_NAME,    host: '127.0.0.1',    port: 3306,    dialect: 'mysql',    dialectOptions: {      bigNumberStrings: true,    },  },  production: {    username: process.env.PROD_DB_USERNAME,    password: process.env.PROD_DB_PASSWORD,    database: process.env.PROD_DB_NAME,    host: process.env.PROD_DB_HOSTNAME,    port: process.env.PROD_DB_PORT,    dialect: 'mysql',    dialectOptions: {      bigNumberStrings: true,      ssl: {        ca: fs.readFileSync(__dirname + '/mysql-ca-main.crt'),      },    },  },};
```

The example above also shows how to add custom dialect options to the configuration.

### Using Babel​

To enable more modern constructions in your migrations and seeders, you can simply install `babel-register` and require it at the beginning of `.sequelizerc`:

```
npm i --save-dev babel-register
```

```
// .sequelizercrequire('babel-register');const path = require('path');module.exports = {  config: path.resolve('config', 'config.json'),  'models-path': path.resolve('models'),  'seeders-path': path.resolve('seeders'),  'migrations-path': path.resolve('migrations'),};
```

Of course, the outcome will depend upon your babel configuration (such as in a `.babelrc` file). Learn more at [babeljs.io](https://babeljs.io).

### Security tip​

Use environment variables for config settings. This is because secrets such as passwords should never be part of the source code (and especially not committed to version control).

### Storage​

There are three types of storage that you can use: `sequelize`, `json`, and `none`.

- `sequelize` : stores migrations and seeds in a table on the sequelize database
- `json` : stores migrations and seeds on a json file
- `none` : does not store any migration/seed

#### Migration Storage​

By default the CLI will create a table in your database called `SequelizeMeta` containing an entry for each executed migration. To change this behavior, there are three options you can add to the configuration file. Using `migrationStorage`, you can choose the type of storage to be used for migrations. If you choose `json`, you can specify the path of the file using `migrationStoragePath` or the CLI will write to the file `sequelize-meta.json`. If you want to keep the information in the database, using `sequelize`, but want to use a different table, you can change the table name using `migrationStorageTableName`. Also you can define a different schema for the `SequelizeMeta` table by providing the `migrationStorageTableSchema` property.

```
{  "development": {    "username": "root",    "password": null,    "database": "database_development",    "host": "127.0.0.1",    "dialect": "mysql",    // Use a different storage type. Default: sequelize    "migrationStorage": "json",    // Use a different file name. Default: sequelize-meta.json    "migrationStoragePath": "sequelizeMeta.json",    // Use a different table name. Default: SequelizeMeta    "migrationStorageTableName": "sequelize_meta",    // Use a different schema for the SequelizeMeta table    "migrationStorageTableSchema": "custom_schema"  }}
```

**Note:** *Thenonestorage is not recommended as a migration storage. If you decide to use it, be aware of the implications of having no record of what migrations did or didn't run.*

#### Seed Storage​

By default the CLI will not save any seed that is executed. If you choose to change this behavior (!), you can use `seederStorage` in the configuration file to change the storage type. If you choose `json`, you can specify the path of the file using `seederStoragePath` or the CLI will write to the file `sequelize-data.json`. If you want to keep the information in the database, using `sequelize`, you can specify the table name using `seederStorageTableName`, or it will default to `SequelizeData`.

```
{  "development": {    "username": "root",    "password": null,    "database": "database_development",    "host": "127.0.0.1",    "dialect": "mysql",    // Use a different storage. Default: none    "seederStorage": "json",    // Use a different file name. Default: sequelize-data.json    "seederStoragePath": "sequelizeData.json",    // Use a different table name. Default: SequelizeData    "seederStorageTableName": "sequelize_data"  }}
```

### Configuration Connection String​

As an alternative to the `--config` option with configuration files defining your database, you can use the `--url` option to pass in a connection string. For example:

```
npx sequelize-cli db:migrate --url 'mysql://root:password@mysql_host.com/database_name'
```

If utilizing `package.json` scripts with npm, make sure to use the extra `--` in your command when using flags.
For example:

```
// package.json...  "scripts": {    "migrate:up": "npx sequelize-cli db:migrate",    "migrate:undo": "npx sequelize-cli db:migrate:undo"  },...
```

Use the command like so: `npm run migrate:up -- --url <url>`

### Programmatic usage​

Sequelize has a sister library called [umzug](https://github.com/sequelize/umzug) for programmatically handling execution and logging of migration tasks.
