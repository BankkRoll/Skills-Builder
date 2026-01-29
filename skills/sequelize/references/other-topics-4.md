# Transactions and more

# Transactions

> Sequelize does not use transactions by default. However, for production-ready usage of Sequelize, you should definitely configure Sequelize to use transactions.

Version: v6 - stable

Sequelize does not use [transactions](https://en.wikipedia.org/wiki/Database_transaction) by default. However, for production-ready usage of Sequelize, you should definitely configure Sequelize to use transactions.

Sequelize supports two ways of using transactions:

1. **Unmanaged transactions:** Committing and rolling back the transaction should be done manually by the user (by calling the appropriate Sequelize methods).
2. **Managed transactions**: Sequelize will automatically rollback the transaction if any error is thrown, or commit the transaction otherwise. Also, if CLS (Continuation Local Storage) is enabled, all queries within the transaction callback will automatically receive the transaction object.

## Unmanaged transactions​

Let's start with an example:

```
// First, we start a transaction from your connection and save it into a variableconst t = await sequelize.transaction();try {  // Then, we do some calls passing this transaction as an option:  const user = await User.create(    {      firstName: 'Bart',      lastName: 'Simpson',    },    { transaction: t },  );  await user.addSibling(    {      firstName: 'Lisa',      lastName: 'Simpson',    },    { transaction: t },  );  // If the execution reaches this line, no errors were thrown.  // We commit the transaction.  await t.commit();} catch (error) {  // If the execution reaches this line, an error was thrown.  // We rollback the transaction.  await t.rollback();}
```

As shown above, the *unmanaged transaction* approach requires that you commit and rollback the transaction manually, when necessary.

## Managed transactions​

Managed transactions handle committing or rolling back the transaction automatically. You start a managed transaction by passing a callback to `sequelize.transaction`. This callback can be `async` (and usually is).

The following will happen in this case:

- Sequelize will automatically start a transaction and obtain a transaction object `t`
- Then, Sequelize will execute the callback you provided, passing `t` into it
- If your callback throws an error, Sequelize will automatically rollback the transaction
- If your callback succeeds, Sequelize will automatically commit the transaction
- Only then the `sequelize.transaction` call will settle:
  - Either resolving with the resolution of your callback
  - Or, if your callback throws, rejecting with the thrown error

Example code:

```
try {  const result = await sequelize.transaction(async t => {    const user = await User.create(      {        firstName: 'Abraham',        lastName: 'Lincoln',      },      { transaction: t },    );    await user.setShooter(      {        firstName: 'John',        lastName: 'Boothe',      },      { transaction: t },    );    return user;  });  // If the execution reaches this line, the transaction has been committed successfully  // `result` is whatever was returned from the transaction callback (the `user`, in this case)} catch (error) {  // If the execution reaches this line, an error occurred.  // The transaction has already been rolled back automatically by Sequelize!}
```

Note that `t.commit()` and `t.rollback()` were not called directly (which is correct).

### Throw errors to rollback​

When using the managed transaction you should *never* commit or rollback the transaction manually. If all queries are successful (in the sense of not throwing any error), but you still want to rollback the transaction, you should throw an error yourself:

```
await sequelize.transaction(async t => {  const user = await User.create(    {      firstName: 'Abraham',      lastName: 'Lincoln',    },    { transaction: t },  );  // Woops, the query was successful but we still want to roll back!  // We throw an error manually, so that Sequelize handles everything automatically.  throw new Error();});
```

### Automatically pass transactions to all queries​

In the examples above, the transaction is still manually passed, by passing `{ transaction: t }` as the second argument. To automatically pass the transaction to all queries you must install the [cls-hooked](https://github.com/Jeff-Lewis/cls-hooked) (CLS) module and instantiate a namespace in your own code:

```
const cls = require('cls-hooked');const namespace = cls.createNamespace('my-very-own-namespace');
```

To enable CLS you must tell sequelize which namespace to use by using a static method of the sequelize constructor:

```
const Sequelize = require('sequelize');Sequelize.useCLS(namespace);new Sequelize(....);
```

Notice, that the `useCLS()` method is on the *constructor*, not on an instance of sequelize. This means that all instances will share the same namespace, and that CLS is all-or-nothing - you cannot enable it only for some instances.

CLS works like a thread-local storage for callbacks. What this means in practice is that different callback chains can access local variables by using the CLS namespace. When CLS is enabled sequelize will set the `transaction` property on the namespace when a new transaction is created. Since variables set within a callback chain are private to that chain several concurrent transactions can exist at the same time:

```
sequelize.transaction(t1 => {  namespace.get('transaction') === t1; // true});sequelize.transaction(t2 => {  namespace.get('transaction') === t2; // true});
```

In most case you won't need to access `namespace.get('transaction')` directly, since all queries will automatically look for a transaction on the namespace:

```
sequelize.transaction(t1 => {  // With CLS enabled, the user will be created inside the transaction  return User.create({ name: 'Alice' });});
```

## Concurrent/Partial transactions​

You can have concurrent transactions within a sequence of queries or have some of them excluded from any transactions. Use the `transaction` option to control which transaction a query belongs to:

**Note:** *SQLite does not support more than one transaction at the same time.*

### With CLS enabled​

```
sequelize.transaction(t1 => {  return sequelize.transaction(t2 => {    // With CLS enabled, queries here will by default use t2.    // Pass in the `transaction` option to define/alter the transaction they belong to.    return Promise.all([      User.create({ name: 'Bob' }, { transaction: null }),      User.create({ name: 'Mallory' }, { transaction: t1 }),      User.create({ name: 'John' }), // this would default to t2    ]);  });});
```

## Passing options​

The `sequelize.transaction` method accepts options.

For unmanaged transactions, just use `sequelize.transaction(options)`.

For managed transactions, use `sequelize.transaction(options, callback)`.

## Isolation levels​

The possible isolations levels to use when starting a transaction:

```
const { Transaction } = require('sequelize');// The following are valid isolation levels:Transaction.ISOLATION_LEVELS.READ_UNCOMMITTED; // "READ UNCOMMITTED"Transaction.ISOLATION_LEVELS.READ_COMMITTED; // "READ COMMITTED"Transaction.ISOLATION_LEVELS.REPEATABLE_READ; // "REPEATABLE READ"Transaction.ISOLATION_LEVELS.SERIALIZABLE; // "SERIALIZABLE"
```

By default, sequelize uses the isolation level of the database. If you want to use a different isolation level, pass in the desired level as the first argument:

```
const { Transaction } = require('sequelize');await sequelize.transaction(  {    isolationLevel: Transaction.ISOLATION_LEVELS.SERIALIZABLE,  },  async t => {    // Your code  },);
```

You can also overwrite the `isolationLevel` setting globally with an option in the Sequelize constructor:

```
const { Sequelize, Transaction } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:', {  isolationLevel: Transaction.ISOLATION_LEVELS.SERIALIZABLE,});
```

**Note for MSSQL:** *TheSET ISOLATION LEVELqueries are not logged since the specifiedisolationLevelis passed directly totedious.*

## Usage with other sequelize methods​

The `transaction` option goes with most other options, which are usually the first argument of a method.

For methods that take values, like `.create`, `.update()`, etc. `transaction` should be passed to the option in the second argument.

If unsure, refer to the API documentation for the method you are using to be sure of the signature.

Examples:

```
await User.create({ name: 'Foo Bar' }, { transaction: t });await User.findAll({  where: {    name: 'Foo Bar',  },  transaction: t,});
```

## TheafterCommithook​

A `transaction` object allows tracking if and when it is committed.

An `afterCommit` hook can be added to both managed and unmanaged transaction objects:

```
// Managed transaction:await sequelize.transaction(async t => {  t.afterCommit(() => {    // Your logic  });});// Unmanaged transaction:const t = await sequelize.transaction();t.afterCommit(() => {  // Your logic});await t.commit();
```

The callback passed to `afterCommit` can be `async`. In this case:

- For a managed transaction: the `sequelize.transaction` call will wait for it before settling;
- For an unmanaged transaction: the `t.commit` call will wait for it before settling.

Notes:

- The `afterCommit` hook is not raised if the transaction is rolled back;
- The `afterCommit` hook does not modify the return value of the transaction (unlike most hooks)

You can use the `afterCommit` hook in conjunction with model hooks to know when a instance is saved and available outside of a transaction

```
User.afterSave((instance, options) => {  if (options.transaction) {    // Save done within a transaction, wait until transaction is committed to    // notify listeners the instance has been saved    options.transaction.afterCommit(() => /* Notify */)    return;  }  // Save done outside a transaction, safe for callers to fetch the updated model  // Notify});
```

## Locks​

Queries within a `transaction` can be performed with locks:

```
return User.findAll({  limit: 1,  lock: true,  transaction: t1,});
```

Queries within a transaction can skip locked rows:

```
return User.findAll({  limit: 1,  lock: true,  skipLocked: true,  transaction: t2,});
```

---

# TypeScript

> We're working hard on making Sequelize a breeze to use in TypeScript.

Version: v6 - stableinfo

We're working hard on making Sequelize a breeze to use in TypeScript.
[Some parts](https://github.com/sequelize/sequelize/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3ARFC+label%3A%22type%3A+typescript%22) are still a work in progress. We recommend using [sequelize-typescript](https://www.npmjs.com/package/sequelize-typescript)
to bridge the gap until our improvements are ready to be released.

Sequelize provides its own TypeScript definitions.

Please note that only **TypeScript >= 4.1** is supported.
Our TypeScript support does not follow SemVer. We will support TypeScript releases for at least one year, after which they may be dropped in a SemVer MINOR release.

As Sequelize heavily relies on runtime property assignments, TypeScript won't be very useful out of the box.
A decent amount of manual type declarations are needed to make models workable.

## Installation​

In order to avoid clashes with different Node versions, the typings for Node are not included. You must install [@types/node](https://www.npmjs.com/package/@types/node) manually.

## Usage​

**Important**: You must use `declare` on your class properties typings to ensure TypeScript does not emit those class properties.
See [Caveat with Public Class Fields](https://sequelize.org/docs/v6/core-concepts/model-basics/#caveat-with-public-class-fields)

Sequelize Models accept two generic types to define what the model's Attributes & Creation Attributes are like:

```
import { Model, Optional } from 'sequelize';// We don't recommend doing this. Read on for the new way of declaring Model typings.type UserAttributes = {  id: number;  name: string;  // other attributes...};// we're telling the Model that 'id' is optional// when creating an instance of the model (such as using Model.create()).type UserCreationAttributes = Optional<UserAttributes, 'id'>;class User extends Model<UserAttributes, UserCreationAttributes> {  declare id: number;  declare name: string;  // other attributes...}
```

This solution is verbose. Sequelize >=6.14.0 provides new utility types that will drastically reduce the amount
of boilerplate necessary: `InferAttributes`, and `InferCreationAttributes`. They will extract Attribute typings
directly from the Model:

```
import { Model, InferAttributes, InferCreationAttributes, CreationOptional } from 'sequelize';// order of InferAttributes & InferCreationAttributes is important.class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  // 'CreationOptional' is a special type that marks the field as optional  // when creating an instance of the model (such as using Model.create()).  declare id: CreationOptional<number>;  declare name: string;  // other attributes...}
```

Important things to know about `InferAttributes` & `InferCreationAttributes` work: They will select all declared properties of the class except:

- Static fields and methods.
- Methods (anything whose type is a function).
- Those whose type uses the branded type `NonAttribute`.
- Those excluded by using InferAttributes like this: `InferAttributes<User, { omit: 'properties' | 'to' | 'omit' }>`.
- Those declared by the Model superclass (but not intermediary classes!).
  If one of your attributes shares the same name as one of the properties of `Model`, change its name.
  Doing this is likely to cause issues anyway.
- Getter & setters are not automatically excluded. Set their return / parameter type to `NonAttribute`,
  or add them to `omit` to exclude them.

`InferCreationAttributes` works the same way as `InferAttributes` with one exception :Properties  typed using the `CreationOptional` type
will be marked as optional.
Note that attributes that accept `null`, or `undefined` do not need to use `CreationOptional`:

```
class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  declare firstName: string;  // there is no need to use CreationOptional on lastName because nullable attributes  // are always optional in User.create()  declare lastName: string | null;}// ...await User.create({  firstName: 'Zoé',  // last name omitted, but this is still valid!});
```

You only need to use `CreationOptional` & `NonAttribute` on class instance fields or getters.

Example of a minimal TypeScript project with strict type-checking for attributes:

```
/** * Keep this file in sync with the code in the "Usage" section * in /docs/manual/other-topics/typescript.md * * Don't include this comment in the md file. */import {  Association, DataTypes, HasManyAddAssociationMixin, HasManyCountAssociationsMixin,  HasManyCreateAssociationMixin, HasManyGetAssociationsMixin, HasManyHasAssociationMixin,  HasManySetAssociationsMixin, HasManyAddAssociationsMixin, HasManyHasAssociationsMixin,  HasManyRemoveAssociationMixin, HasManyRemoveAssociationsMixin, Model, ModelDefined, Optional,  Sequelize, InferAttributes, InferCreationAttributes, CreationOptional, NonAttribute, ForeignKey,} from 'sequelize';const sequelize = new Sequelize('mysql://root:asd123@localhost:3306/mydb');// 'projects' is excluded as it's not an attribute, it's an association.class User extends Model<InferAttributes<User, { omit: 'projects' }>, InferCreationAttributes<User, { omit: 'projects' }>> {  // id can be undefined during creation when using `autoIncrement`  declare id: CreationOptional<number>;  declare name: string;  declare preferredName: string | null; // for nullable fields  // timestamps!  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;  // Since TS cannot determine model association at compile time  // we have to declare them here purely virtually  // these will not exist until `Model.init` was called.  declare getProjects: HasManyGetAssociationsMixin<Project>; // Note the null assertions!  declare addProject: HasManyAddAssociationMixin<Project, number>;  declare addProjects: HasManyAddAssociationsMixin<Project, number>;  declare setProjects: HasManySetAssociationsMixin<Project, number>;  declare removeProject: HasManyRemoveAssociationMixin<Project, number>;  declare removeProjects: HasManyRemoveAssociationsMixin<Project, number>;  declare hasProject: HasManyHasAssociationMixin<Project, number>;  declare hasProjects: HasManyHasAssociationsMixin<Project, number>;  declare countProjects: HasManyCountAssociationsMixin;  declare createProject: HasManyCreateAssociationMixin<Project, 'ownerId'>;  // You can also pre-declare possible inclusions, these will only be populated if you  // actively include a relation.  declare projects?: NonAttribute<Project[]>; // Note this is optional since it's only populated when explicitly requested in code  // getters that are not attributes should be tagged using NonAttribute  // to remove them from the model's Attribute Typings.  get fullName(): NonAttribute<string> {    return this.name;  }  declare static associations: {    projects: Association<User, Project>;  };}class Project extends Model<  InferAttributes<Project>,  InferCreationAttributes<Project>> {  // id can be undefined during creation when using `autoIncrement`  declare id: CreationOptional<number>;  // foreign keys are automatically added by associations methods (like Project.belongsTo)  // by branding them using the `ForeignKey` type, `Project.init` will know it does not need to  // display an error if ownerId is missing.  declare ownerId: ForeignKey<User['id']>;  declare name: string;  // `owner` is an eagerly-loaded association.  // We tag it as `NonAttribute`  declare owner?: NonAttribute<User>;  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;}class Address extends Model<  InferAttributes<Address>,  InferCreationAttributes<Address>> {  declare userId: ForeignKey<User['id']>;  declare address: string;  // createdAt can be undefined during creation  declare createdAt: CreationOptional<Date>;  // updatedAt can be undefined during creation  declare updatedAt: CreationOptional<Date>;}Project.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    name: {      type: new DataTypes.STRING(128),      allowNull: false    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    sequelize,    tableName: 'projects'  });User.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    name: {      type: new DataTypes.STRING(128),      allowNull: false    },    preferredName: {      type: new DataTypes.STRING(128),      allowNull: true    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    tableName: 'users',    sequelize // passing the `sequelize` instance is required  });Address.init(  {    address: {      type: new DataTypes.STRING(128),      allowNull: false    },    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  {    tableName: 'address',    sequelize // passing the `sequelize` instance is required  });// You can also define modules in a functional wayinterface NoteAttributes {  id: number;  title: string;  content: string;}// You can also set multiple attributes optional at oncetype NoteCreationAttributes = Optional<NoteAttributes, 'id' | 'title'>;// And with a functional approach defining a module looks like thisconst Note: ModelDefined<  NoteAttributes,  NoteCreationAttributes> = sequelize.define(  'Note',  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true    },    title: {      type: new DataTypes.STRING(64),      defaultValue: 'Unnamed Note'    },    content: {      type: new DataTypes.STRING(4096),      allowNull: false    }  },  {    tableName: 'notes'  });// Here we associate which actually populates out pre-declared `association` static and other methods.User.hasMany(Project, {  sourceKey: 'id',  foreignKey: 'ownerId',  as: 'projects' // this determines the name in `associations`!});Address.belongsTo(User, { targetKey: 'id' });User.hasOne(Address, { sourceKey: 'id' });async function doStuffWithUser() {  const newUser = await User.create({    name: 'Johnny',    preferredName: 'John',  });  console.log(newUser.id, newUser.name, newUser.preferredName);  const project = await newUser.createProject({    name: 'first!'  });  const ourUser = await User.findByPk(1, {    include: [User.associations.projects],    rejectOnEmpty: true // Specifying true here removes `null` from the return type!  });  // Note the `!` null assertion since TS can't know if we included  // the model or not  console.log(ourUser.projects![0].name);}(async () => {  await sequelize.sync();  await doStuffWithUser();})();
```

### The case ofModel.init​

`Model.init` requires an attribute configuration for each attribute declared in typings.

Some attributes don't actually need to be passed to `Model.init`, this is how you can make this static method aware of them:

- Methods used to define associations (`Model.belongsTo`, `Model.hasMany`, etc…) already handle
  the configuration of the necessary foreign keys attributes. It is not necessary to configure
  these foreign keys using `Model.init`.
  Use the `ForeignKey<>` branded type to make `Model.init` aware of the fact that it isn't necessary to configure the foreign key:
  ```
  import {  Model,  InferAttributes,  InferCreationAttributes,  DataTypes,  ForeignKey,} from 'sequelize';class Project extends Model<InferAttributes<Project>, InferCreationAttributes<Project>> {  id: number;  userId: ForeignKey<number>;}// this configures the `userId` attribute.Project.belongsTo(User);// therefore, `userId` doesn't need to be specified here.Project.init(  {    id: {      type: DataTypes.INTEGER,      primaryKey: true,      autoIncrement: true,    },  },  { sequelize },);
  ```
- Timestamp attributes managed by Sequelize (by default, `createdAt`, `updatedAt`, and `deletedAt`) don't need to be configured using `Model.init`,
  unfortunately `Model.init` has no way of knowing this. We recommend you use the minimum necessary configuration to silence this error:
  ```
  import { Model, InferAttributes, InferCreationAttributes, DataTypes } from 'sequelize';class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  id: number;  createdAt: Date;  updatedAt: Date;}User.init(  {    id: {      type: DataTypes.INTEGER,      primaryKey: true,      autoIncrement: true,    },    // technically, `createdAt` & `updatedAt` are added by Sequelize and don't need to be configured in Model.init    // but the typings of Model.init do not know this. Add the following to mute the typing error:    createdAt: DataTypes.DATE,    updatedAt: DataTypes.DATE,  },  { sequelize },);
  ```

### Usage without strict types for attributes​

The typings for Sequelize v5 allowed you to define models without specifying types for the attributes.
This is still possible for backwards compatibility and for cases where you feel strict typing for attributes isn't worth it.

```
/** * Keep this file in sync with the code in the "Usage without strict types for * attributes" section in /docs/manual/other-topics/typescript.md * * Don't include this comment in the md file. */import { Sequelize, Model, DataTypes } from 'sequelize';const sequelize = new Sequelize('mysql://root:asd123@localhost:3306/mydb');class User extends Model {  declare id: number;  declare name: string;  declare preferredName: string | null;}User.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true,    },    name: {      type: new DataTypes.STRING(128),      allowNull: false,    },    preferredName: {      type: new DataTypes.STRING(128),      allowNull: true,    },  },  {    tableName: 'users',    sequelize, // passing the `sequelize` instance is required  },);async function doStuffWithUserModel() {  const newUser = await User.create({    name: 'Johnny',    preferredName: 'John',  });  console.log(newUser.id, newUser.name, newUser.preferredName);  const foundUser = await User.findOne({ where: { name: 'Johnny' } });  if (foundUser === null) return;  console.log(foundUser.name);}
```

## Usage ofSequelize#define​

In Sequelize versions before v5, the default way of defining a model involved using `Sequelize#define`.
It's still possible to define models with that, and you can also add typings to these models using interfaces.

```
/** * Keep this file in sync with the code in the "Usage of `sequelize.define`" * section in /docs/manual/other-topics/typescript.md * * Don't include this comment in the md file. */import { Sequelize, Model, DataTypes, CreationOptional, InferAttributes, InferCreationAttributes } from 'sequelize';const sequelize = new Sequelize('mysql://root:asd123@localhost:3306/mydb');// We recommend you declare an interface for the attributes, for stricter typecheckinginterface UserModel extends Model<InferAttributes<UserModel>, InferCreationAttributes<UserModel>> {  // Some fields are optional when calling UserModel.create() or UserModel.build()  id: CreationOptional<number>;  name: string;}const UserModel = sequelize.define<UserModel>('User', {  id: {    primaryKey: true,    type: DataTypes.INTEGER.UNSIGNED,  },  name: {    type: DataTypes.STRING,  },});async function doStuff() {  const instance = await UserModel.findByPk(1, {    rejectOnEmpty: true,  });  console.log(instance.id);}
```

## Utility Types​

### Requesting a Model Class​

`ModelStatic` is designed to be used to type a Model *class*.

Here is an example of a utility method that requests a Model Class, and returns the list of primary keys defined in that class:

```
import {  ModelStatic,  ModelAttributeColumnOptions,  Model,  InferAttributes,  InferCreationAttributes,  CreationOptional,} from 'sequelize';/** * Returns the list of attributes that are part of the model's primary key. */export function getPrimaryKeyAttributes(model: ModelStatic<any>): ModelAttributeColumnOptions[] {  const attributes: ModelAttributeColumnOptions[] = [];  for (const attribute of Object.values(model.rawAttributes)) {    if (attribute.primaryKey) {      attributes.push(attribute);    }  }  return attributes;}class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  id: CreationOptional<number>;}User.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true,    },  },  { sequelize },);const primaryAttributes = getPrimaryKeyAttributes(User);
```

### Getting a Model's attributes​

If you need to access the list of attributes of a given model, `Attributes<Model>` and `CreationAttributes<Model>`
are what you need to use.

They will return the Attributes (and Creation Attributes) of the Model passed as a parameter.

Don't confuse them with `InferAttributes` and `InferCreationAttributes`. These two utility types should only ever be used
in the definition of a Model to automatically create the list of attributes from the model's public class fields. They only work
with class-based model definitions (When using `Model.init`).

`Attributes<Model>` and `CreationAttributes<Model>` will return the list of attributes of any model, no matter how they were created (be it `Model.init` or `Sequelize#define`).

Here is an example of a utility function that requests a Model Class, and the name of an attribute ; and returns the corresponding attribute metadata.

```
import {  ModelStatic,  ModelAttributeColumnOptions,  Model,  InferAttributes,  InferCreationAttributes,  CreationOptional,  Attributes,} from 'sequelize';export function getAttributeMetadata<M extends Model>(  model: ModelStatic<M>,  attributeName: keyof Attributes<M>,): ModelAttributeColumnOptions {  const attribute = model.rawAttributes[attributeName];  if (attribute == null) {    throw new Error(`Attribute ${attributeName} does not exist on model ${model.name}`);  }  return attribute;}class User extends Model<InferAttributes<User>, InferCreationAttributes<User>> {  id: CreationOptional<number>;}User.init(  {    id: {      type: DataTypes.INTEGER.UNSIGNED,      autoIncrement: true,      primaryKey: true,    },  },  { sequelize },);const idAttributeMeta = getAttributeMetadata(User, 'id'); // works!// @ts-expect-errorconst nameAttributeMeta = getAttributeMetadata(User, 'name'); // fails because 'name' is not an attribute of User
```

---

# Upgrade to v6

> Sequelize v6 is the next major release after v5. Below is a list of breaking changes to help you upgrade.

Version: v6 - stable

Sequelize v6 is the next major release after v5. Below is a list of breaking changes to help you upgrade.

## Breaking Changes​

### Support for Node 10 and up​

Sequelize v6 will only support Node 10 and up [#10821](https://github.com/sequelize/sequelize/issues/10821).

### CLS​

You should now use [cls-hooked](https://github.com/Jeff-Lewis/cls-hooked) package for CLS support.

```
const cls = require('cls-hooked');const namespace = cls.createNamespace('....');const Sequelize = require('sequelize');Sequelize.useCLS(namespace);
```

### Database Engine Support​

We have updated our minimum supported database engine versions. Using older database engine will show `SEQUELIZE0006` deprecation warning. Please check [the releases page](https://sequelize.org/releases/) for the version table.

### Sequelize​

- Bluebird has been removed. Internally all methods are now using async/await. Public API now returns native promises. Thanks to [Andy Edwards](https://github.com/jedwards1211) for this refactor work.
- `Sequelize.Promise` is no longer available.
- `sequelize.import` method has been removed. CLI users should update to `sequelize-cli@6`.
- All instances of QueryInterface and QueryGenerator have been renamed to their lowerCamelCase variants eg. queryInterface and queryGenerator when used as property names on Model and Dialect, the class names remain the same.

### Model​

#### options.returning​

Option `returning: true` will no longer return attributes that are not defined in the model. Old behavior can be achieved by using `returning: ['*']` instead.

#### Model.changed()​

Sequelize does not detect deep mutations. To avoid problems with `save`, you should treat each attribute as immutable and only assign new values.

Example with a deep mutation of an attribute:

```
const instance = await MyModel.findOne();// Sequelize will not detect this changeinstance.jsonField.jsonProperty = 12345;console.log(instance.changed()); // false// You can workaround this by telling Sequelize the property changed:instance.changed('jsonField', true);console.log(instance.changed()); // true
```

Example if you treat each attribute as immutable:

```
const instance = await MyModel.findOne();// Sequelize will detect this changeinstance.jsonField = {  ...instance.jsonField,  jsonProperty: 12345,};console.log(instance.changed()); // true
```

#### Model.bulkCreate()​

This method now throws `Sequelize.AggregateError` instead of `Bluebird.AggregateError`. All errors are now exposed as `errors` key.

#### Model.upsert()​

Native upsert is now supported for all dialects.

```
const [instance, created] = await MyModel.upsert({});
```

Signature for this method has been changed to `Promise<Model,boolean | null>`. First index contains upserted `instance`, second index contains a boolean (or `null`) indicating if record was created or updated. For SQLite/Postgres, `created` value will always be `null`.

- MySQL - Implemented with ON DUPLICATE KEY UPDATE
- PostgreSQL - Implemented with ON CONFLICT DO UPDATE
- SQLite - Implemented with ON CONFLICT DO UPDATE
- MSSQL - Implemented with MERGE statement

*Note for Postgres users:* If upsert payload contains PK field, then PK will be used as the conflict target. Otherwise first unique constraint will be selected as the conflict key.

### QueryInterface​

#### addConstraint​

This method now only takes 2 parameters, `tableName` and `options`. Previously the second parameter could be a list of column names to apply the constraint to, this list must now be passed as `options.fields` property.

## Changelog​

### 6.0.0-beta.7​

- docs(associations): belongs to many create with through table
- docs(query-interface): fix broken links [#12272](https://github.com/sequelize/sequelize/pull/12272)
- docs(sequelize): omitNull only works for CREATE/UPDATE queries
- docs: asyncify [#12297](https://github.com/sequelize/sequelize/pull/12297)
- docs: responsive [#12308](https://github.com/sequelize/sequelize/pull/12308)
- docs: update feature request template
- feat(postgres): native upsert [#12301](https://github.com/sequelize/sequelize/pull/12301)
- feat(sequelize): allow passing dialectOptions.options from url [#12404](https://github.com/sequelize/sequelize/pull/12404)
- fix(include): check if attributes specified for included through model [#12316](https://github.com/sequelize/sequelize/pull/12316)
- fix(model.destroy): return 0 with truncate [#12281](https://github.com/sequelize/sequelize/pull/12281)
- fix(mssql): empty order array generates invalid FETCH statement [#12261](https://github.com/sequelize/sequelize/pull/12261)
- fix(postgres): parse enums correctly when describing a table [#12409](https://github.com/sequelize/sequelize/pull/12409)
- fix(query): ensure correct return signature for QueryTypes.RAW [#12305](https://github.com/sequelize/sequelize/pull/12305)
- fix(query): preserve cls context for logger [#12328](https://github.com/sequelize/sequelize/pull/12328)
- fix(query-generator): do not generate GROUP BY clause if options.group is empty [#12343](https://github.com/sequelize/sequelize/pull/12343)
- fix(reload): include default scope [#12399](https://github.com/sequelize/sequelize/pull/12399)
- fix(types): add Association into OrderItem type [#12332](https://github.com/sequelize/sequelize/pull/12332)
- fix(types): add clientMinMessages to Options interface [#12375](https://github.com/sequelize/sequelize/pull/12375)
- fix(types): transactionType in Options [#12377](https://github.com/sequelize/sequelize/pull/12377)
- fix(types): add support for optional values in "where" clauses [#12337](https://github.com/sequelize/sequelize/pull/12337)
- fix(types): add missing fields to 'FindOrCreateType' [#12338](https://github.com/sequelize/sequelize/pull/12338)
- fix: add missing sql and parameters properties to some query errors [#12299](https://github.com/sequelize/sequelize/pull/12299)
- fix: remove custom inspect [#12262](https://github.com/sequelize/sequelize/pull/12262)
- refactor: cleanup query generators [#12304](https://github.com/sequelize/sequelize/pull/12304)

### 6.0.0-beta.6​

- docs(add-constraint): options.fields support
- docs(association): document uniqueKey for belongs to many [#12166](https://github.com/sequelize/sequelize/pull/12166)
- docs(association): options.through.where support
- docs(association): use and instead of 'a nd' [#12191](https://github.com/sequelize/sequelize/pull/12191)
- docs(association): use correct scope name [#12204](https://github.com/sequelize/sequelize/pull/12204)
- docs(manuals): avoid duplicate header ids [#12201](https://github.com/sequelize/sequelize/pull/12201)
- docs(model): correct syntax error in example code [#12137](https://github.com/sequelize/sequelize/pull/12137)
- docs(query-interface): removeIndex indexNameOrAttributes [#11947](https://github.com/sequelize/sequelize/pull/11947)
- docs(resources): add sequelize-guard library [#12235](https://github.com/sequelize/sequelize/pull/12235)
- docs(typescript): fix confusing comments [#12226](https://github.com/sequelize/sequelize/pull/12226)
- docs(v6-guide): bluebird removal API changes
- docs: database version support info [#12168](https://github.com/sequelize/sequelize/pull/12168)
- docs: remove remaining bluebird references [#12167](https://github.com/sequelize/sequelize/pull/12167)
- feat(belongs-to-many): allow creation of paranoid join tables [#12088](https://github.com/sequelize/sequelize/pull/12088)
- feat(belongs-to-many): get/has/count for paranoid join table [#12256](https://github.com/sequelize/sequelize/pull/12256)
- feat(pool): expose maxUses pool config option [#12101](https://github.com/sequelize/sequelize/pull/12101)
- feat(postgres): minify include aliases over limit [#11940](https://github.com/sequelize/sequelize/pull/11940)
- feat(sequelize): handle query string host value [#12041](https://github.com/sequelize/sequelize/pull/12041)
- fix(associations): ensure correct schema on all generated attributes [#12258](https://github.com/sequelize/sequelize/pull/12258)
- fix(docs/instances): use correct variable for increment [#12087](https://github.com/sequelize/sequelize/pull/12087)
- fix(include): separate queries are not sub-queries [#12144](https://github.com/sequelize/sequelize/pull/12144)
- fix(model): fix unchained promise in association logic in bulkCreate [#12163](https://github.com/sequelize/sequelize/pull/12163)
- fix(model): updateOnDuplicate handles composite keys [#11984](https://github.com/sequelize/sequelize/pull/11984)
- fix(model.count): distinct without any column generates invalid SQL [#11946](https://github.com/sequelize/sequelize/pull/11946)
- fix(model.reload): ignore options.where and always use this.where() [#12211](https://github.com/sequelize/sequelize/pull/12211)
- fix(mssql) insert record failure because of BOOLEAN column type [#12090](https://github.com/sequelize/sequelize/pull/12090)
- fix(mssql): cast sql_variant in query generator [#11994](https://github.com/sequelize/sequelize/pull/11994)
- fix(mssql): dont use OUTPUT INSERTED for update without returning [#12260](https://github.com/sequelize/sequelize/pull/12260)
- fix(mssql): duplicate order in FETCH/NEXT queries [#12257](https://github.com/sequelize/sequelize/pull/12257)
- fix(mssql): set correct scale for float [#11962](https://github.com/sequelize/sequelize/pull/11962)
- fix(mssql): tedious v9 requires connect call [#12182](https://github.com/sequelize/sequelize/pull/12182)
- fix(mssql): use uppercase for engine table and columns [#12212](https://github.com/sequelize/sequelize/pull/12212)
- fix(pool): show deprecation when engine is not supported [#12218](https://github.com/sequelize/sequelize/pull/12218)
- fix(postgres): addColumn support ARRAY(ENUM) [#12259](https://github.com/sequelize/sequelize/pull/12259)
- fix(query): do not bind $ used within a whole-word [#12250](https://github.com/sequelize/sequelize/pull/12250)
- fix(query-generator): handle literal for substring based operators [#12210](https://github.com/sequelize/sequelize/pull/12210)
- fix(query-interface): allow passing null for query interface insert [#11931](https://github.com/sequelize/sequelize/pull/11931)
- fix(query-interface): allow sequelize.fn and sequelize.literal in fields of IndexesOptions [#12224](https://github.com/sequelize/sequelize/pull/12224)
- fix(scope): don't modify original scope definition [#12207](https://github.com/sequelize/sequelize/pull/12207)
- fix(sqlite): multiple primary keys results in syntax error [#12237](https://github.com/sequelize/sequelize/pull/12237)
- fix(sync): pass options to all query methods [#12208](https://github.com/sequelize/sequelize/pull/12208)
- fix(typings): add type_helpers to file list [#12000](https://github.com/sequelize/sequelize/pull/12000)
- fix(typings): correct Model.init return type [#12148](https://github.com/sequelize/sequelize/pull/12148)
- fix(typings): fn is assignable to where [#12040](https://github.com/sequelize/sequelize/pull/12040)
- fix(typings): getForeignKeysForTables argument definition [#12084](https://github.com/sequelize/sequelize/pull/12084)
- fix(typings): make between operator accept date ranges [#12162](https://github.com/sequelize/sequelize/pull/12162)
- refactor(ci): improve database wait script [#12132](https://github.com/sequelize/sequelize/pull/12132)
- refactor(tsd-test-setup): add & setup dtslint [#11879](https://github.com/sequelize/sequelize/pull/11879)
- refactor: move all dialect conditional logic into subclass [#12217](https://github.com/sequelize/sequelize/pull/12217)
- refactor: remove sequelize.import helper [#12175](https://github.com/sequelize/sequelize/pull/12175)
- refactor: use native versions [#12159](https://github.com/sequelize/sequelize/pull/12159)
- refactor: use object spread instead of Object.assign [#12213](https://github.com/sequelize/sequelize/pull/12213)

### 6.0.0-beta.5​

- fix(find-all): throw on empty attributes [#11867](https://github.com/sequelize/sequelize/pull/11867)
- fix(types): `queryInterface.addIndex` [#11844](https://github.com/sequelize/sequelize/pull/11844)
- fix(types): `plain` option in `sequelize.query` [#11596](https://github.com/sequelize/sequelize/pull/11596)
- fix(types): correct overloaded method order [#11727](https://github.com/sequelize/sequelize/pull/11727)
- fix(types): `comparator` arg of `Sequelize.where` [#11843](https://github.com/sequelize/sequelize/pull/11843)
- fix(types): fix BelongsToManyGetAssociationsMixinOptions [#11818](https://github.com/sequelize/sequelize/pull/11818)
- fix(types): adds `hooks` to `CreateOptions` [#11736](https://github.com/sequelize/sequelize/pull/11736)
- fix(increment): broken queries [#11852](https://github.com/sequelize/sequelize/pull/11852)
- fix(associations): gets on many-to-many with non-primary target key [#11778](https://github.com/sequelize/sequelize11778/pull/)
- fix: properly select SRID if present [#11763](https://github.com/sequelize/sequelize/pull/11763)
- feat(sqlite): automatic path provision for `options.storage` [#11853](https://github.com/sequelize/sequelize/pull/11853)
- feat(postgres): `idle_in_transaction_session_timeout` connection option [#11775](https://github.com/sequelize/sequelize11775/pull/)
- feat(index): improve to support multiple fields with operator [#11934](https://github.com/sequelize/sequelize/pull/11934)
- docs(transactions): fix addIndex example and grammar [#11759](https://github.com/sequelize/sequelize/pull/11759)
- docs(raw-queries): remove outdated info [#11833](https://github.com/sequelize/sequelize/pull/11833)
- docs(optimistic-locking): fix missing manual [#11850](https://github.com/sequelize/sequelize/pull/11850)
- docs(model): findOne return value for empty result [#11762](https://github.com/sequelize/sequelize/pull/11762)
- docs(model-querying-basics.md): add some commas [#11891](https://github.com/sequelize/sequelize/pull/11891)
- docs(manuals): fix missing models-definition page [#11838](https://github.com/sequelize/sequelize/pull/11838)
- docs(manuals): extensive rewrite [#11825](https://github.com/sequelize/sequelize/pull/11825)
- docs(dialect-specific): add MSSQL domain auth example [#11799](https://github.com/sequelize/sequelize/pull/11799)
- docs(associations): fix typos in assocs manual [#11888](https://github.com/sequelize/sequelize/pull/11888)
- docs(associations): fix typo [#11869](https://github.com/sequelize/sequelize/pull/11869)

### 6.0.0-beta.4​

- feat(sync): allow to bypass drop statements when sync with alter enabled [#11708](https://github.com/sequelize/sequelize/pull/11708)
- fix(model): injectDependentVirtualAttrs on included models [#11713](https://github.com/sequelize/sequelize/pull/11713)
- fix(model): generate ON CONFLICT ... DO UPDATE correctly [#11666](https://github.com/sequelize/sequelize/pull/11666)
- fix(mssql): optimize formatError RegEx [#11725](https://github.com/sequelize/sequelize/pull/11725)
- fix(types): add getForeignKeyReferencesForTable type [#11738](https://github.com/sequelize/sequelize/pull/11738)
- fix(types): add 'restore' hooks to types [#11730](https://github.com/sequelize/sequelize/pull/11730)
- fix(types): added 'fieldMaps' to QueryOptions typings [#11702](https://github.com/sequelize/sequelize/pull/11702)
- fix(types): add isSoftDeleted to Model [#11628](https://github.com/sequelize/sequelize/pull/11628)
- fix(types): fix upsert typing [#11674](https://github.com/sequelize/sequelize/pull/11674)
- fix(types): specified 'this' for getters and setters in fields [#11648](https://github.com/sequelize/sequelize/pull/11648)
- fix(types): add paranoid to UpdateOptions interface [#11647](https://github.com/sequelize/sequelize/pull/11647)
- fix(types): include 'as' in IncludeThroughOptions definition [#11624](https://github.com/sequelize/sequelize/pull/11624)
- fix(types): add Includeable to IncludeOptions.include type [#11622](https://github.com/sequelize/sequelize/pull/11622)
- fix(types): transaction lock [#11620](https://github.com/sequelize/sequelize/pull/11620)
- fix(sequelize.fn): escape dollarsign (#11533) [#11606](https://github.com/sequelize/sequelize/pull/11606)
- fix(types): add nested to Includeable [#11354](https://github.com/sequelize/sequelize/pull/11354)
- fix(types): add date to where [#11612](https://github.com/sequelize/sequelize/pull/11612)
- fix(types): add getDatabaseName (#11431) [#11614](https://github.com/sequelize/sequelize/pull/11614)
- fix(types): beforeDestroy [#11618](https://github.com/sequelize/sequelize/pull/11618)
- fix(types): query-interface table schema [#11582](https://github.com/sequelize/sequelize/pull/11582)
- docs: README.md [#11698](https://github.com/sequelize/sequelize/pull/11698)
- docs(sequelize): detail options.retry usage [#11643](https://github.com/sequelize/sequelize/pull/11643)
- docs: clarify logging option in Sequelize constructor [#11653](https://github.com/sequelize/sequelize/pull/11653)
- docs(migrations): fix syntax error in example [#11626](https://github.com/sequelize/sequelize/pull/11626)
- docs: describe logging option [#11654](https://github.com/sequelize/sequelize/pull/11654)
- docs(transaction): fix typo [#11659](https://github.com/sequelize/sequelize/pull/11659)
- docs(hooks): add info about belongs-to-many [#11601](https://github.com/sequelize/sequelize/pull/11601)
- docs(associations): fix typo [#11592](https://github.com/sequelize/sequelize/pull/11592)

### 6.0.0-beta.3​

- feat: support cls-hooked / tests [#11584](https://github.com/sequelize/sequelize/pull/11584)

### 6.0.0-beta.2​

- feat(postgres): change returning option to only return model attributes [#11526](https://github.com/sequelize/sequelize/pull/11526)
- fix(associations): allow binary key for belongs-to-many [#11578](https://github.com/sequelize/sequelize/pull/11578)
- fix(postgres): always replace returning statement for upsertQuery
- fix(model): make .changed() deep aware [#10851](https://github.com/sequelize/sequelize/pull/10851)
- change: use node 10 [#11580](https://github.com/sequelize/sequelize/pull/11580)
