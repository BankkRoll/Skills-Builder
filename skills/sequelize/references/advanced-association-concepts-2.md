# Eager Loading and more

# Eager Loading

> As briefly mentioned in the associations guide, eager Loading is the act of querying data of several models at once (one 'main' model and one or more associated models). At the SQL level, this is a query with one or more joins.

Version: v6 - stable

As briefly mentioned in [the associations guide](https://sequelize.org/docs/v6/core-concepts/assocs/), eager Loading is the act of querying data of several models at once (one 'main' model and one or more associated models). At the SQL level, this is a query with one or more [joins](https://en.wikipedia.org/wiki/Join_(SQL)).

When this is done, the associated models will be added by Sequelize in appropriately named, automatically created field(s) in the returned objects.

In Sequelize, eager loading is mainly done by using the `include` option on a model finder query (such as `findOne`, `findAll`, etc).

## Basic example​

Let's assume the following setup:

```
const User = sequelize.define('user', { name: DataTypes.STRING }, { timestamps: false });const Task = sequelize.define('task', { name: DataTypes.STRING }, { timestamps: false });const Tool = sequelize.define(  'tool',  {    name: DataTypes.STRING,    size: DataTypes.STRING,  },  { timestamps: false },);User.hasMany(Task);Task.belongsTo(User);User.hasMany(Tool, { as: 'Instruments' });
```

### Fetching a single associated element​

OK. So, first of all, let's load all tasks with their associated user:

```
const tasks = await Task.findAll({ include: User });console.log(JSON.stringify(tasks, null, 2));
```

Output:

```
[  {    "name": "A Task",    "id": 1,    "userId": 1,    "user": {      "name": "John Doe",      "id": 1    }  }]
```

Here, `tasks[0].user instanceof User` is `true`. This shows that when Sequelize fetches associated models, they are added to the output object as model instances.

Above, the associated model was added to a new field called `user` in the fetched task. The name of this field was automatically chosen by Sequelize based on the name of the associated model, where its pluralized form is used when applicable (i.e., when the association is `hasMany` or `belongsToMany`). In other words, since `Task.belongsTo(User)`, a task is associated to one user, therefore the logical choice is the singular form (which Sequelize follows automatically).

### Fetching all associated elements​

Now, instead of loading the user that is associated to a given task, we will do the opposite - we will find all tasks associated to a given user.

The method call is essentially the same. The only difference is that now the extra field created in the query result uses the pluralized form (`tasks` in this case), and its value is an array of task instances (instead of a single instance, as above).

```
const users = await User.findAll({ include: Task });console.log(JSON.stringify(users, null, 2));
```

Output:

```
[  {    "name": "John Doe",    "id": 1,    "tasks": [      {        "name": "A Task",        "id": 1,        "userId": 1      }    ]  }]
```

Notice that the accessor (the `tasks` property in the resulting instance) is pluralized since the association is one-to-many.

### Fetching an Aliased association​

If an association is aliased (using the `as` option), you must specify this alias when including the model. Instead of passing the model directly to the `include` option, you should instead provide an object with two options: `model` and `as`.

Notice how the user's `Tool`s are aliased as `Instruments` above. In order to get that right you have to specify the model you want to load, as well as the alias:

```
const users = await User.findAll({  include: { model: Tool, as: 'Instruments' },});console.log(JSON.stringify(users, null, 2));
```

Output:

```
[  {    "name": "John Doe",    "id": 1,    "Instruments": [      {        "name": "Scissor",        "id": 1,        "userId": 1      }    ]  }]
```

You can also include by alias name by specifying a string that matches the association alias:

```
User.findAll({ include: 'Instruments' }); // Also worksUser.findAll({ include: { association: 'Instruments' } }); // Also works
```

### Required eager loading​

When eager loading, we can force the query to return only records which have an associated model, effectively converting the query from the default `OUTER JOIN` to an `INNER JOIN`. This is done with the `required: true` option, as follows:

```
User.findAll({  include: {    model: Task,    required: true,  },});
```

This option also works on nested includes.

### Eager loading filtered at the associated model level​

When eager loading, we can also filter the associated model using the `where` option, as in the following example:

```
User.findAll({  include: {    model: Tool,    as: 'Instruments',    where: {      size: {        [Op.ne]: 'small',      },    },  },});
```

Generated SQL:

```
SELECT  `user`.`id`,  `user`.`name`,  `Instruments`.`id` AS `Instruments.id`,  `Instruments`.`name` AS `Instruments.name`,  `Instruments`.`size` AS `Instruments.size`,  `Instruments`.`userId` AS `Instruments.userId`FROM `users` AS `user`INNER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId` AND  `Instruments`.`size` != 'small';
```

Note that the SQL query generated above will only fetch users that have at least one tool that matches the condition (of not being `small`, in this case). This is the case because, when the `where` option is used inside an `include`, Sequelize automatically sets the `required` option to `true`. This means that, instead of an `OUTER JOIN`, an `INNER JOIN` is done, returning only the parent models with at least one matching children.

Note also that the `where` option used was converted into a condition for the `ON` clause of the `INNER JOIN`. In order to obtain a *top-level* `WHERE` clause, instead of an `ON` clause, something different must be done. This will be shown next.

#### Referring to other columns​

If you want to apply a `WHERE` clause in an included model referring to a value from an associated model, you can simply use the `Sequelize.col` function, as show in the example below:

```
// Find all projects with a least one task where task.state === project.stateProject.findAll({  include: {    model: Task,    where: {      state: Sequelize.col('project.state'),    },  },});
```

### Complex where clauses at the top-level​

To obtain top-level `WHERE` clauses that involve nested columns, Sequelize provides a way to reference nested columns: the `'$nested.column$'` syntax.

It can be used, for example, to move the where conditions from an included model from the `ON` condition to a top-level `WHERE` clause.

```
User.findAll({  where: {    '$Instruments.size$': { [Op.ne]: 'small' },  },  include: [    {      model: Tool,      as: 'Instruments',    },  ],});
```

Generated SQL:

```
SELECT  `user`.`id`,  `user`.`name`,  `Instruments`.`id` AS `Instruments.id`,  `Instruments`.`name` AS `Instruments.name`,  `Instruments`.`size` AS `Instruments.size`,  `Instruments`.`userId` AS `Instruments.userId`FROM `users` AS `user`LEFT OUTER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId`WHERE `Instruments`.`size` != 'small';
```

The `$nested.column$` syntax also works for columns that are nested several levels deep, such as `$some.super.deeply.nested.column$`. Therefore, you can use this to make complex filters on deeply nested columns.

For a better understanding of all differences between the inner `where` option (used inside an `include`), with and without the `required` option, and a top-level `where` using the `$nested.column$` syntax, below we have four examples for you:

```
// Inner where, with default `required: true`await User.findAll({  include: {    model: Tool,    as: 'Instruments',    where: {      size: { [Op.ne]: 'small' },    },  },});// Inner where, `required: false`await User.findAll({  include: {    model: Tool,    as: 'Instruments',    where: {      size: { [Op.ne]: 'small' },    },    required: false,  },});// Top-level where, with default `required: false`await User.findAll({  where: {    '$Instruments.size$': { [Op.ne]: 'small' },  },  include: {    model: Tool,    as: 'Instruments',  },});// Top-level where, `required: true`await User.findAll({  where: {    '$Instruments.size$': { [Op.ne]: 'small' },  },  include: {    model: Tool,    as: 'Instruments',    required: true,  },});
```

Generated SQLs, in order:

```
-- Inner where, with default `required: true`SELECT [...] FROM `users` AS `user`INNER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId`  AND `Instruments`.`size` != 'small';-- Inner where, `required: false`SELECT [...] FROM `users` AS `user`LEFT OUTER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId`  AND `Instruments`.`size` != 'small';-- Top-level where, with default `required: false`SELECT [...] FROM `users` AS `user`LEFT OUTER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId`WHERE `Instruments`.`size` != 'small';-- Top-level where, `required: true`SELECT [...] FROM `users` AS `user`INNER JOIN `tools` AS `Instruments` ON  `user`.`id` = `Instruments`.`userId`WHERE `Instruments`.`size` != 'small';
```

### Fetching withRIGHT OUTER JOIN(MySQL, MariaDB, PostgreSQL and MSSQL only)​

By default, associations are loaded using a `LEFT OUTER JOIN` - that is to say it only includes records from the parent table. You can change this behavior to a `RIGHT OUTER JOIN` by passing the `right` option, if the dialect you are using supports it.

Currently, SQLite does not support [right joins](https://www.sqlite.org/omitted.html).

*Note:* `right` is only respected if `required` is false.

```
User.findAll({  include: [{    model: Task // will create a left join  }]});User.findAll({  include: [{    model: Task,    right: true // will create a right join  }]});User.findAll({  include: [{    model: Task,    required: true,    right: true // has no effect, will create an inner join  }]});User.findAll({  include: [{    model: Task,    where: { name: { [Op.ne]: 'empty trash' } },    right: true // has no effect, will create an inner join  }]});User.findAll({  include: [{    model: Tool,    where: { name: { [Op.ne]: 'empty trash' } },    required: false // will create a left join  }]});User.findAll({  include: [{    model: Tool,    where: { name: { [Op.ne]: 'empty trash' } },    required: false    right: true // will create a right join  }]});
```

## Multiple eager loading​

The `include` option can receive an array in order to fetch multiple associated models at once:

```
Foo.findAll({  include: [    {      model: Bar,      required: true    },    {      model: Baz,      where: /* ... */    },    Qux // Shorthand syntax for { model: Qux } also works here  ]})
```

## Eager loading with Many-to-Many relationships​

When you perform eager loading on a model with a Belongs-to-Many relationship, Sequelize will fetch the junction table data as well, by default. For example:

```
const Foo = sequelize.define('Foo', { name: DataTypes.TEXT });const Bar = sequelize.define('Bar', { name: DataTypes.TEXT });Foo.belongsToMany(Bar, { through: 'Foo_Bar' });Bar.belongsToMany(Foo, { through: 'Foo_Bar' });await sequelize.sync();const foo = await Foo.create({ name: 'foo' });const bar = await Bar.create({ name: 'bar' });await foo.addBar(bar);const fetchedFoo = await Foo.findOne({ include: Bar });console.log(JSON.stringify(fetchedFoo, null, 2));
```

Output:

```
{  "id": 1,  "name": "foo",  "Bars": [    {      "id": 1,      "name": "bar",      "Foo_Bar": {        "FooId": 1,        "BarId": 1      }    }  ]}
```

Note that every bar instance eager loaded into the `"Bars"` property has an extra property called `Foo_Bar` which is the relevant Sequelize instance of the junction model. By default, Sequelize fetches all attributes from the junction table in order to build this extra property.

However, you can specify which attributes you want fetched. This is done with the `attributes` option applied inside the `through` option of the include. For example:

```
Foo.findAll({  include: [    {      model: Bar,      through: {        attributes: [          /* list the wanted attributes here */        ],      },    },  ],});
```

If you don't want anything from the junction table, you can explicitly provide an empty array to the `attributes` option inside the `through` option of the `include` option, and in this case nothing will be fetched and the extra property will not even be created:

```
Foo.findOne({  include: {    model: Bar,    through: {      attributes: [],    },  },});
```

Output:

```
{  "id": 1,  "name": "foo",  "Bars": [    {      "id": 1,      "name": "bar"    }  ]}
```

Whenever including a model from a Many-to-Many relationship, you can also apply a filter on the junction table. This is done with the `where` option applied inside the `through` option of the include. For example:

```
User.findAll({  include: [    {      model: Project,      through: {        where: {          // Here, `completed` is a column present at the junction table          completed: true,        },      },    },  ],});
```

Generated SQL (using SQLite):

```
SELECT  `User`.`id`,  `User`.`name`,  `Projects`.`id` AS `Projects.id`,  `Projects`.`name` AS `Projects.name`,  `Projects->User_Project`.`completed` AS `Projects.User_Project.completed`,  `Projects->User_Project`.`UserId` AS `Projects.User_Project.UserId`,  `Projects->User_Project`.`ProjectId` AS `Projects.User_Project.ProjectId`FROM `Users` AS `User`LEFT OUTER JOIN `User_Projects` AS `Projects->User_Project` ON  `User`.`id` = `Projects->User_Project`.`UserId`LEFT OUTER JOIN `Projects` AS `Projects` ON  `Projects`.`id` = `Projects->User_Project`.`ProjectId` AND  `Projects->User_Project`.`completed` = 1;
```

## Including everything​

To include all associated models, you can use the `all` and `nested` options:

```
// Fetch all models associated with UserUser.findAll({ include: { all: true } });// Fetch all models associated with User and their nested associations (recursively)User.findAll({ include: { all: true, nested: true } });
```

## Including soft deleted records​

In case you want to eager load soft deleted records you can do that by setting `include.paranoid` to `false`:

```
User.findAll({  include: [    {      model: Tool,      as: 'Instruments',      where: { size: { [Op.ne]: 'small' } },      paranoid: false,    },  ],});
```

## Ordering eager loaded associations​

When you want to apply `ORDER` clauses to eager loaded models, you must use the top-level `order` option with augmented arrays, starting with the specification of the nested model you want to sort.

This is better understood with examples.

```
Company.findAll({  include: Division,  order: [    // We start the order array with the model we want to sort    [Division, 'name', 'ASC'],  ],});Company.findAll({  include: Division,  order: [[Division, 'name', 'DESC']],});Company.findAll({  // If the include uses an alias...  include: { model: Division, as: 'Div' },  order: [    // ...we use the same syntax from the include    // in the beginning of the order array    [{ model: Division, as: 'Div' }, 'name', 'DESC'],  ],});Company.findAll({  // If we have includes nested in several levels...  include: {    model: Division,    include: Department,  },  order: [    // ... we replicate the include chain of interest    // at the beginning of the order array    [Division, Department, 'name', 'DESC'],  ],});
```

In the case of many-to-many relationships, you are also able to sort by attributes in the through table. For example, assuming we have a Many-to-Many relationship between `Division` and `Department` whose junction model is `DepartmentDivision`, you can do:

```
Company.findAll({  include: {    model: Division,    include: Department,  },  order: [[Division, DepartmentDivision, 'name', 'ASC']],});
```

In all the above examples, you have noticed that the `order` option is used at the top-level. The only situation in which `order` also works inside the include option is when `separate: true` is used. In that case, the usage is as follows:

```
// This only works for `separate: true` (which in turn// only works for has-many relationships).User.findAll({  include: {    model: Post,    separate: true,    order: [['createdAt', 'DESC']],  },});
```

### Complex ordering involving sub-queries​

Take a look at the [guide on sub-queries](https://sequelize.org/docs/v6/other-topics/sub-queries/) for an example of how to use a sub-query to assist a more complex ordering.

## Nested eager loading​

You can use nested eager loading to load all related models of a related model:

```
const users = await User.findAll({  include: {    model: Tool,    as: 'Instruments',    include: {      model: Teacher,      include: [        /* etc */      ],    },  },});console.log(JSON.stringify(users, null, 2));
```

Output:

```
[  {    "name": "John Doe",    "id": 1,    "Instruments": [      {        // 1:M and N:M association        "name": "Scissor",        "id": 1,        "userId": 1,        "Teacher": {          // 1:1 association          "name": "Jimi Hendrix"        }      }    ]  }]
```

This will produce an outer join. However, a `where` clause on a related model will create an inner join and return only the instances that have matching sub-models. To return all parent instances, you should add `required: false`.

```
User.findAll({  include: [    {      model: Tool,      as: 'Instruments',      include: [        {          model: Teacher,          where: {            school: 'Woodstock Music School',          },          required: false,        },      ],    },  ],});
```

The query above will return all users, and all their instruments, but only those teachers associated with `Woodstock Music School`.

## UsingfindAndCountAllwith includes​

The `findAndCountAll` utility function supports includes. Only the includes that are marked as `required` will be considered in `count`. For example, if you want to find and count all users who have a profile:

```
User.findAndCountAll({  include: [{ model: Profile, required: true }],  limit: 3,});
```

Because the include for `Profile` has `required` set it will result in an inner join, and only the users who have a profile will be counted. If we remove `required` from the include, both users with and without profiles will be counted. Adding a `where` clause to the include automatically makes it required:

```
User.findAndCountAll({  include: [{ model: Profile, where: { active: true } }],  limit: 3,});
```

The query above will only count users who have an active profile, because `required` is implicitly set to true when you add a where clause to the include.

---

# Polymorphic Associations

> **Note:** the usage of polymorphic associations in Sequelize, as outlined in this guide, should be done with caution. Don't just copy-paste code from here, otherwise you might easily make mistakes and introduce bugs in your code. Make sure you understand what is going on.

Version: v6 - stable

*Note:the usage of polymorphic associations in Sequelize, as outlined in this guide, should be done with caution. Don't just copy-paste code from here, otherwise you might easily make mistakes and introduce bugs in your code. Make sure you understand what is going on.*

## Concept​

A **polymorphic association** consists on two (or more) associations happening with the same foreign key.

For example, consider the models `Image`, `Video` and `Comment`. The first two represent something that a user might post. We want to allow comments to be placed in both of them. This way, we immediately think of establishing the following associations:

- A One-to-Many association between `Image` and `Comment`:
  ```
  Image.hasMany(Comment);Comment.belongsTo(Image);
  ```
- A One-to-Many association between `Video` and `Comment`:
  ```
  Video.hasMany(Comment);Comment.belongsTo(Video);
  ```

However, the above would cause Sequelize to create two foreign keys on the `Comment` table: `ImageId` and `VideoId`. This is not ideal because this structure makes it look like a comment can be attached at the same time to one image and one video, which isn't true. Instead, what we really want here is precisely a polymorphic association, in which a `Comment` points to a single **Commentable**, an abstract polymorphic entity that represents one of `Image` or `Video`.

Before proceeding to how to configure such an association, let's see how using it looks like:

```
const image = await Image.create({ url: 'https://placekitten.com/408/287' });const comment = await image.createComment({ content: 'Awesome!' });console.log(comment.commentableId === image.id); // true// We can also retrieve which type of commentable a comment is associated to.// The following prints the model name of the associated commentable instance.console.log(comment.commentableType); // "Image"// We can use a polymorphic method to retrieve the associated commentable, without// having to worry whether it's an Image or a Video.const associatedCommentable = await comment.getCommentable();// In this example, `associatedCommentable` is the same thing as `image`:const isDeepEqual = require('deep-equal');console.log(isDeepEqual(image, commentable)); // true
```

## Configuring a One-to-Many polymorphic association​

To setup the polymorphic association for the example above (which is an example of One-to-Many polymorphic association), we have the following steps:

- Define a string field called `commentableType` in the `Comment` model;
- Define the `hasMany` and `belongsTo` association between `Image`/`Video` and `Comment`:
  - Disabling constraints (i.e. using `{ constraints: false }`), since the same foreign key is referencing multiple tables;
  - Specifying the appropriate [association scopes](https://sequelize.org/docs/v6/advanced-association-concepts/association-scopes/);
- To properly support lazy loading, define a new instance method on the `Comment` model called `getCommentable` which calls, under the hood, the correct mixin to fetch the appropriate commentable;
- To properly support eager loading, define an `afterFind` hook on the `Comment` model that automatically populates the `commentable` field in every instance;
- To prevent bugs/mistakes in eager loading, you can also delete the concrete fields `image` and `video` from Comment instances in the same `afterFind` hook, leaving only the abstract `commentable` field available.

Here is an example:

```
// Helper functionconst uppercaseFirst = str => `${str[0].toUpperCase()}${str.substr(1)}`;class Image extends Model {}Image.init(  {    title: DataTypes.STRING,    url: DataTypes.STRING,  },  { sequelize, modelName: 'image' },);class Video extends Model {}Video.init(  {    title: DataTypes.STRING,    text: DataTypes.STRING,  },  { sequelize, modelName: 'video' },);class Comment extends Model {  getCommentable(options) {    if (!this.commentableType) return Promise.resolve(null);    const mixinMethodName = `get${uppercaseFirst(this.commentableType)}`;    return this[mixinMethodName](options);  }}Comment.init(  {    title: DataTypes.STRING,    commentableId: DataTypes.INTEGER,    commentableType: DataTypes.STRING,  },  { sequelize, modelName: 'comment' },);Image.hasMany(Comment, {  foreignKey: 'commentableId',  constraints: false,  scope: {    commentableType: 'image',  },});Comment.belongsTo(Image, { foreignKey: 'commentableId', constraints: false });Video.hasMany(Comment, {  foreignKey: 'commentableId',  constraints: false,  scope: {    commentableType: 'video',  },});Comment.belongsTo(Video, { foreignKey: 'commentableId', constraints: false });Comment.addHook('afterFind', findResult => {  if (!Array.isArray(findResult)) findResult = [findResult];  for (const instance of findResult) {    if (instance.commentableType === 'image' && instance.image !== undefined) {      instance.commentable = instance.image;    } else if (instance.commentableType === 'video' && instance.video !== undefined) {      instance.commentable = instance.video;    }    // To prevent mistakes:    delete instance.image;    delete instance.dataValues.image;    delete instance.video;    delete instance.dataValues.video;  }});
```

Since the `commentableId` column references several tables (two in this case), we cannot add a `REFERENCES` constraint to it. This is why the `constraints: false` option was used.

Note that, in the code above:

- The *Image -> Comment* association defined an association scope: `{ commentableType: 'image' }`
- The *Video -> Comment* association defined an association scope: `{ commentableType: 'video' }`

These scopes are automatically applied when using the association functions (as explained in the [Association Scopes](https://sequelize.org/docs/v6/advanced-association-concepts/association-scopes/) guide). Some examples are below, with their generated SQL statements:

- `image.getComments()`:
  ```
  SELECT "id", "title", "commentableType", "commentableId", "createdAt", "updatedAt"FROM "comments" AS "comment"WHERE "comment"."commentableType" = 'image' AND "comment"."commentableId" = 1;
  ```
  Here we can see that ` `comment`.`commentableType` = 'image'` was automatically added to the `WHERE` clause of the generated SQL. This is exactly the behavior we want.
- `image.createComment({ title: 'Awesome!' })`:
  ```
  INSERT INTO "comments" (  "id", "title", "commentableType", "commentableId", "createdAt", "updatedAt") VALUES (  DEFAULT, 'Awesome!', 'image', 1,  '2018-04-17 05:36:40.454 +00:00', '2018-04-17 05:36:40.454 +00:00') RETURNING *;
  ```
- `image.addComment(comment)`:
  ```
  UPDATE "comments"SET "commentableId"=1, "commentableType"='image', "updatedAt"='2018-04-17 05:38:43.948 +00:00'WHERE "id" IN (1)
  ```

### Polymorphic lazy loading​

The `getCommentable` instance method on `Comment` provides an abstraction for lazy loading the associated commentable - working whether the comment belongs to an Image or a Video.

It works by simply converting the `commentableType` string into a call to the correct mixin (either `getImage` or `getVideo`).

Note that the `getCommentable` implementation above:

- Returns `null` when no association is present (which is good);
- Allows you to pass an options object to `getCommentable(options)`, just like any other standard Sequelize method. This is useful to specify where-conditions or includes, for example.

### Polymorphic eager loading​

Now, we want to perform a polymorphic eager loading of the associated commentables for one (or more) comments. We want to achieve something similar to the following idea:

```
const comment = await Comment.findOne({  include: [    /* What to put here? */  ],});console.log(comment.commentable); // This is our goal
```

The solution is to tell Sequelize to include both Images and Videos, so that our `afterFind` hook defined above will do the work, automatically adding the `commentable` field to the instance object, providing the abstraction we want.

For example:

```
const comments = await Comment.findAll({  include: [Image, Video],});for (const comment of comments) {  const message = `Found comment #${comment.id} with ${comment.commentableType} commentable:`;  console.log(message, comment.commentable.toJSON());}
```

Output example:

```
Found comment #1 with image commentable: { id: 1,  title: 'Meow',  url: 'https://placekitten.com/408/287',  createdAt: 2019-12-26T15:04:53.047Z,  updatedAt: 2019-12-26T15:04:53.047Z }
```

### Caution - possibly invalid eager/lazy loading!​

Consider a comment `Foo` whose `commentableId` is 2 and `commentableType` is `image`. Consider also that `Image A` and `Video X` both happen to have an id equal to 2. Conceptually, it is clear that `Video X` is not associated to `Foo`, because even though its id is 2, the `commentableType` of `Foo` is `image`, not `video`. However, this distinction is made by Sequelize only at the level of the abstractions performed by `getCommentable` and the hook we created above.

This means that if you call `Comment.findAll({ include: Video })` in the situation above, `Video X` will be eager loaded into `Foo`. Thankfully, our `afterFind` hook will delete it automatically, to help prevent bugs, but regardless it is important that you understand what is going on.

The best way to prevent this kind of mistake is to **avoid using the concrete accessors and mixins directly at all costs** (such as `.image`, `.getVideo()`, `.setImage()`, etc), always preferring the abstractions we created, such as `.getCommentable()` and `.commentable`. If you really need to access eager-loaded `.image` and `.video` for some reason, make sure you wrap that in a type check such as `comment.commentableType === 'image'`.

## Configuring a Many-to-Many polymorphic association​

In the above example, we had the models `Image` and `Video` being abstractly called *commentables*, with one *commentable* having many comments. However, one given comment would belong to a single *commentable* - this is why the whole situation is a One-to-Many polymorphic association.

Now, to consider a Many-to-Many polymorphic association, instead of considering comments, we will consider tags. For convenience, instead of calling Image and Video as *commentables*, we will now call them *taggables*. One *taggable* may have several tags, and at the same time one tag can be placed in several *taggables*.

The setup for this goes as follows:

- Define the junction model explicitly, specifying the two foreign keys as `tagId` and `taggableId` (this way it is a junction model for a Many-to-Many relationship between `Tag` and the abstract concept of *taggable*);
- Define a string field called `taggableType` in the junction model;
- Define the `belongsToMany` associations between the two models and `Tag`:
  - Disabling constraints (i.e. using `{ constraints: false }`), since the same foreign key is referencing multiple tables;
  - Specifying the appropriate [association scopes](https://sequelize.org/docs/v6/advanced-association-concepts/association-scopes/);
- Define a new instance method on the `Tag` model called `getTaggables` which calls, under the hood, the correct mixin to fetch the appropriate taggables.

Implementation:

```
class Tag extends Model {  async getTaggables(options) {    const images = await this.getImages(options);    const videos = await this.getVideos(options);    // Concat images and videos in a single array of taggables    return images.concat(videos);  }}Tag.init(  {    name: DataTypes.STRING,  },  { sequelize, modelName: 'tag' },);// Here we define the junction model explicitlyclass Tag_Taggable extends Model {}Tag_Taggable.init(  {    tagId: {      type: DataTypes.INTEGER,      unique: 'tt_unique_constraint',    },    taggableId: {      type: DataTypes.INTEGER,      unique: 'tt_unique_constraint',      references: null,    },    taggableType: {      type: DataTypes.STRING,      unique: 'tt_unique_constraint',    },  },  { sequelize, modelName: 'tag_taggable' },);Image.belongsToMany(Tag, {  through: {    model: Tag_Taggable,    unique: false,    scope: {      taggableType: 'image',    },  },  foreignKey: 'taggableId',  constraints: false,});Tag.belongsToMany(Image, {  through: {    model: Tag_Taggable,    unique: false,  },  foreignKey: 'tagId',  constraints: false,});Video.belongsToMany(Tag, {  through: {    model: Tag_Taggable,    unique: false,    scope: {      taggableType: 'video',    },  },  foreignKey: 'taggableId',  constraints: false,});Tag.belongsToMany(Video, {  through: {    model: Tag_Taggable,    unique: false,  },  foreignKey: 'tagId',  constraints: false,});
```

The `constraints: false` option disables references constraints, as the `taggableId` column references several tables, we cannot add a `REFERENCES` constraint to it.

Note that:

- The *Image -> Tag* association defined an association scope: `{ taggableType: 'image' }`
- The *Video -> Tag* association defined an association scope: `{ taggableType: 'video' }`

These scopes are automatically applied when using the association functions. Some examples are below, with their generated SQL statements:

- `image.getTags()`:
  ```
  SELECT  `tag`.`id`,  `tag`.`name`,  `tag`.`createdAt`,  `tag`.`updatedAt`,  `tag_taggable`.`tagId` AS `tag_taggable.tagId`,  `tag_taggable`.`taggableId` AS `tag_taggable.taggableId`,  `tag_taggable`.`taggableType` AS `tag_taggable.taggableType`,  `tag_taggable`.`createdAt` AS `tag_taggable.createdAt`,  `tag_taggable`.`updatedAt` AS `tag_taggable.updatedAt`FROM `tags` AS `tag`INNER JOIN `tag_taggables` AS `tag_taggable` ON  `tag`.`id` = `tag_taggable`.`tagId` AND  `tag_taggable`.`taggableId` = 1 AND  `tag_taggable`.`taggableType` = 'image';
  ```
  Here we can see that ` `tag_taggable`.`taggableType` = 'image'` was automatically added to the `WHERE` clause of the generated SQL. This is exactly the behavior we want.
- `tag.getTaggables()`:
  ```
  SELECT  `image`.`id`,  `image`.`url`,  `image`.`createdAt`,  `image`.`updatedAt`,  `tag_taggable`.`tagId` AS `tag_taggable.tagId`,  `tag_taggable`.`taggableId` AS `tag_taggable.taggableId`,  `tag_taggable`.`taggableType` AS `tag_taggable.taggableType`,  `tag_taggable`.`createdAt` AS `tag_taggable.createdAt`,  `tag_taggable`.`updatedAt` AS `tag_taggable.updatedAt`FROM `images` AS `image`INNER JOIN `tag_taggables` AS `tag_taggable` ON  `image`.`id` = `tag_taggable`.`taggableId` AND  `tag_taggable`.`tagId` = 1;SELECT  `video`.`id`,  `video`.`url`,  `video`.`createdAt`,  `video`.`updatedAt`,  `tag_taggable`.`tagId` AS `tag_taggable.tagId`,  `tag_taggable`.`taggableId` AS `tag_taggable.taggableId`,  `tag_taggable`.`taggableType` AS `tag_taggable.taggableType`,  `tag_taggable`.`createdAt` AS `tag_taggable.createdAt`,  `tag_taggable`.`updatedAt` AS `tag_taggable.updatedAt`FROM `videos` AS `video`INNER JOIN `tag_taggables` AS `tag_taggable` ON  `video`.`id` = `tag_taggable`.`taggableId` AND  `tag_taggable`.`tagId` = 1;
  ```

Note that the above implementation of `getTaggables()` allows you to pass an options object to `getCommentable(options)`, just like any other standard Sequelize method. This is useful to specify where-conditions or includes, for example.

### Applying scopes on the target model​

In the example above, the `scope` options (such as `scope: { taggableType: 'image' }`) were applied to the *through* model, not the *target* model, since it was used under the `through` option.

We can also apply an association scope on the target model. We can even do both at the same time.

To illustrate this, consider an extension of the above example between tags and taggables, where each tag has a status. This way, to get all pending tags of an image, we could establish another `belongsToMany` relationship between `Image` and `Tag`, this time applying a scope on the through model and another scope on the target model:

```
Image.belongsToMany(Tag, {  through: {    model: Tag_Taggable,    unique: false,    scope: {      taggableType: 'image',    },  },  scope: {    status: 'pending',  },  as: 'pendingTags',  foreignKey: 'taggableId',  constraints: false,});
```

This way, when calling `image.getPendingTags()`, the following SQL query will be generated:

```
SELECT  `tag`.`id`,  `tag`.`name`,  `tag`.`status`,  `tag`.`createdAt`,  `tag`.`updatedAt`,  `tag_taggable`.`tagId` AS `tag_taggable.tagId`,  `tag_taggable`.`taggableId` AS `tag_taggable.taggableId`,  `tag_taggable`.`taggableType` AS `tag_taggable.taggableType`,  `tag_taggable`.`createdAt` AS `tag_taggable.createdAt`,  `tag_taggable`.`updatedAt` AS `tag_taggable.updatedAt`FROM `tags` AS `tag`INNER JOIN `tag_taggables` AS `tag_taggable` ON  `tag`.`id` = `tag_taggable`.`tagId` AND  `tag_taggable`.`taggableId` = 1 AND  `tag_taggable`.`taggableType` = 'image'WHERE (  `tag`.`status` = 'pending');
```

We can see that both scopes were applied automatically:

- ` `tag_taggable`.`taggableType` = 'image'` was added automatically to the `INNER JOIN`;
- ` `tag`.`status` = 'pending'` was added automatically to an outer where clause.
