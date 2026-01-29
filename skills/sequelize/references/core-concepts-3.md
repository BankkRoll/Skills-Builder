# Model Querying and more

# Model Querying

> Sequelize provides various methods to assist querying your database for data.

Version: v6 - stable

Sequelize provides various methods to assist querying your database for data.

*Important notice: to perform production-ready queries with Sequelize, make sure you have read theTransactions guideas well. Transactions are important to ensure data integrity and to provide other benefits.*

This guide will show how to make the standard [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) queries.

## Simple INSERT queries​

First, a simple example:

```
// Create a new userconst jane = await User.create({ firstName: 'Jane', lastName: 'Doe' });console.log("Jane's auto-generated ID:", jane.id);
```

The [Model.create()](https://sequelize.org/api/v6/class/src/model.js~model#static-method-create) method is a shorthand for building an unsaved instance with [Model.build()](https://sequelize.org/api/v6/class/src/model.js~model#static-method-build) and saving the instance with [instance.save()](https://sequelize.org/api/v6/class/src/model.js~model#instance-method-save).

It is also possible to define which attributes can be set in the `create` method. This can be especially useful if you create database entries based on a form which can be filled by a user. Using that would, for example, allow you to restrict the `User` model to set only a username but not an admin flag (i.e., `isAdmin`):

```
const user = await User.create(  {    username: 'alice123',    isAdmin: true,  },  { fields: ['username'] },);// let's assume the default of isAdmin is falseconsole.log(user.username); // 'alice123'console.log(user.isAdmin); // false
```

## Simple SELECT queries​

You can read the whole table from the database with the [findAll](https://sequelize.org/api/v6/class/src/model.js~model#static-method-findAll) method:

```
// Find all usersconst users = await User.findAll();console.log(users.every(user => user instanceof User)); // trueconsole.log('All users:', JSON.stringify(users, null, 2));
```

```
SELECT * FROM ...
```

## Specifying attributes for SELECT queries​

To select only some attributes, you can use the `attributes` option:

```
Model.findAll({  attributes: ['foo', 'bar'],});
```

```
SELECT foo, bar FROM ...
```

Attributes can be renamed using a nested array:

```
Model.findAll({  attributes: ['foo', ['bar', 'baz'], 'qux'],});
```

```
SELECT foo, bar AS baz, qux FROM ...
```

You can use [sequelize.fn](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#static-method-fn) to do aggregations:

```
Model.findAll({  attributes: ['foo', [sequelize.fn('COUNT', sequelize.col('hats')), 'n_hats'], 'bar'],});
```

```
SELECT foo, COUNT(hats) AS n_hats, bar FROM ...
```

When using aggregation function, you must give it an alias to be able to access it from the model. In the example above you can get the number of hats with `instance.n_hats`.

Sometimes it may be tiresome to list all the attributes of the model if you only want to add an aggregation:

```
// This is a tiresome way of getting the number of hats (along with every column)Model.findAll({  attributes: [    'id',    'foo',    'bar',    'baz',    'qux',    'hats', // We had to list all attributes...    [sequelize.fn('COUNT', sequelize.col('hats')), 'n_hats'], // To add the aggregation...  ],});// This is shorter, and less error prone because it still works if you add / remove attributes from your model laterModel.findAll({  attributes: {    include: [[sequelize.fn('COUNT', sequelize.col('hats')), 'n_hats']],  },});
```

```
SELECT id, foo, bar, baz, qux, hats, COUNT(hats) AS n_hats FROM ...
```

Similarly, it's also possible to remove a selected few attributes:

```
Model.findAll({  attributes: { exclude: ['baz'] },});
```

```
-- Assuming all columns are 'id', 'foo', 'bar', 'baz' and 'qux'SELECT id, foo, bar, qux FROM ...
```

## Applying WHERE clauses​

The `where` option is used to filter the query. There are lots of operators to use for the `where` clause, available as Symbols from [Op](https://sequelize.org/api/v6/variable/#static-variable-Op).

### The basics​

```
Post.findAll({  where: {    authorId: 2,  },});// SELECT * FROM post WHERE authorId = 2;
```

Observe that no operator (from `Op`) was explicitly passed, so Sequelize assumed an equality comparison by default. The above code is equivalent to:

```
const { Op } = require('sequelize');Post.findAll({  where: {    authorId: {      [Op.eq]: 2,    },  },});// SELECT * FROM post WHERE authorId = 2;
```

Multiple checks can be passed:

```
Post.findAll({  where: {    authorId: 12,    status: 'active',  },});// SELECT * FROM post WHERE authorId = 12 AND status = 'active';
```

Just like Sequelize inferred the `Op.eq` operator in the first example, here Sequelize inferred that the caller wanted an `AND` for the two checks. The code above is equivalent to:

```
const { Op } = require('sequelize');Post.findAll({  where: {    [Op.and]: [{ authorId: 12 }, { status: 'active' }],  },});// SELECT * FROM post WHERE authorId = 12 AND status = 'active';
```

An `OR` can be easily performed in a similar way:

```
const { Op } = require('sequelize');Post.findAll({  where: {    [Op.or]: [{ authorId: 12 }, { authorId: 13 }],  },});// SELECT * FROM post WHERE authorId = 12 OR authorId = 13;
```

Since the above was an `OR` involving the same field, Sequelize allows you to use a slightly different structure which is more readable and generates the same behavior:

```
const { Op } = require('sequelize');Post.destroy({  where: {    authorId: {      [Op.or]: [12, 13],    },  },});// DELETE FROM post WHERE authorId = 12 OR authorId = 13;
```

### Operators​

Sequelize provides several operators.

```
const { Op } = require("sequelize");Post.findAll({  where: {    [Op.and]: [{ a: 5 }, { b: 6 }],            // (a = 5) AND (b = 6)    [Op.or]: [{ a: 5 }, { b: 6 }],             // (a = 5) OR (b = 6)    someAttribute: {      // Basics      [Op.eq]: 3,                              // = 3      [Op.ne]: 20,                             // != 20      [Op.is]: null,                           // IS NULL      [Op.not]: true,                          // IS NOT TRUE      [Op.or]: [5, 6],                         // (someAttribute = 5) OR (someAttribute = 6)      // Using dialect specific column identifiers (PG in the following example):      [Op.col]: 'user.organization_id',        // = "user"."organization_id"      // Number comparisons      [Op.gt]: 6,                              // > 6      [Op.gte]: 6,                             // >= 6      [Op.lt]: 10,                             // < 10      [Op.lte]: 10,                            // <= 10      [Op.between]: [6, 10],                   // BETWEEN 6 AND 10      [Op.notBetween]: [11, 15],               // NOT BETWEEN 11 AND 15      // Other operators      [Op.all]: sequelize.literal('SELECT 1'), // > ALL (SELECT 1)      [Op.in]: [1, 2],                         // IN [1, 2]      [Op.notIn]: [1, 2],                      // NOT IN [1, 2]      [Op.like]: '%hat',                       // LIKE '%hat'      [Op.notLike]: '%hat',                    // NOT LIKE '%hat'      [Op.startsWith]: 'hat',                  // LIKE 'hat%'      [Op.endsWith]: 'hat',                    // LIKE '%hat'      [Op.substring]: 'hat',                   // LIKE '%hat%'      [Op.iLike]: '%hat',                      // ILIKE '%hat' (case insensitive) (PG only)      [Op.notILike]: '%hat',                   // NOT ILIKE '%hat'  (PG only)      [Op.regexp]: '^[h|a|t]',                 // REGEXP/~ '^[h|a|t]' (MySQL/PG only)      [Op.notRegexp]: '^[h|a|t]',              // NOT REGEXP/!~ '^[h|a|t]' (MySQL/PG only)      [Op.iRegexp]: '^[h|a|t]',                // ~* '^[h|a|t]' (PG only)      [Op.notIRegexp]: '^[h|a|t]',             // !~* '^[h|a|t]' (PG only)      [Op.any]: [2, 3],                        // ANY (ARRAY[2, 3]::INTEGER[]) (PG only)      [Op.match]: Sequelize.fn('to_tsquery', 'fat & rat') // match text search for strings 'fat' and 'rat' (PG only)      // In Postgres, Op.like/Op.iLike/Op.notLike can be combined to Op.any:      [Op.like]: { [Op.any]: ['cat', 'hat'] }  // LIKE ANY (ARRAY['cat', 'hat'])      // There are more postgres-only range operators, see below    }  }});
```

#### Shorthand syntax forOp.in​

Passing an array directly to the `where` option will implicitly use the `IN` operator:

```
Post.findAll({  where: {    id: [1, 2, 3], // Same as using `id: { [Op.in]: [1,2,3] }`  },});// SELECT ... FROM "posts" AS "post" WHERE "post"."id" IN (1, 2, 3);
```

### Logical combinations with operators​

The operators `Op.and`, `Op.or` and `Op.not` can be used to create arbitrarily complex nested logical comparisons.

#### Examples withOp.andandOp.or​

```
const { Op } = require("sequelize");Foo.findAll({  where: {    rank: {      [Op.or]: {        [Op.lt]: 1000,        [Op.eq]: null      }    },    // rank < 1000 OR rank IS NULL    {      createdAt: {        [Op.lt]: new Date(),        [Op.gt]: new Date(new Date() - 24 * 60 * 60 * 1000)      }    },    // createdAt < [timestamp] AND createdAt > [timestamp]    {      [Op.or]: [        {          title: {            [Op.like]: 'Boat%'          }        },        {          description: {            [Op.like]: '%boat%'          }        }      ]    }    // title LIKE 'Boat%' OR description LIKE '%boat%'  }});
```

#### Examples withOp.not​

```
Project.findAll({  where: {    name: 'Some Project',    [Op.not]: [      { id: [1, 2, 3] },      {        description: {          [Op.like]: 'Hello%',        },      },    ],  },});
```

The above will generate:

```
SELECT *FROM `Projects`WHERE (  `Projects`.`name` = 'Some Project'  AND NOT (    `Projects`.`id` IN (1,2,3)    AND    `Projects`.`description` LIKE 'Hello%'  ))
```

### Advanced queries with functions (not just columns)​

What if you wanted to obtain something like `WHERE char_length("content") = 7`?

```
Post.findAll({  where: sequelize.where(sequelize.fn('char_length', sequelize.col('content')), 7),});// SELECT ... FROM "posts" AS "post" WHERE char_length("content") = 7
```

Note the usage of the [sequelize.fn](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#static-method-fn) and [sequelize.col](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#static-method-col) methods, which should be used to specify an SQL function call and a table column, respectively. These methods should be used instead of passing a plain string (such as `char_length(content)`) because Sequelize needs to treat this situation differently (for example, using other symbol escaping approaches).

What if you need something even more complex?

```
Post.findAll({  where: {    [Op.or]: [      sequelize.where(sequelize.fn('char_length', sequelize.col('content')), 7),      {        content: {          [Op.like]: 'Hello%',        },      },      {        [Op.and]: [          { status: 'draft' },          sequelize.where(sequelize.fn('char_length', sequelize.col('content')), {            [Op.gt]: 10,          }),        ],      },    ],  },});
```

The above generates the following SQL:

```
SELECT  ...FROM "posts" AS "post"WHERE (  char_length("content") = 7  OR  "post"."content" LIKE 'Hello%'  OR (    "post"."status" = 'draft'    AND    char_length("content") > 10  ))
```

### Postgres-only Range Operators​

Range types can be queried with all supported operators.

Keep in mind, the provided range value can [define the bound inclusion/exclusion](https://sequelize.org/docs/v6/other-topics/other-data-types/#ranges-postgresql-only) as well.

```
[Op.contains]: 2,            // @> '2'::integer  (PG range contains element operator)[Op.contains]: [1, 2],       // @> [1, 2)        (PG range contains range operator)[Op.contained]: [1, 2],      // <@ [1, 2)        (PG range is contained by operator)[Op.overlap]: [1, 2],        // && [1, 2)        (PG range overlap (have points in common) operator)[Op.adjacent]: [1, 2],       // -|- [1, 2)       (PG range is adjacent to operator)[Op.strictLeft]: [1, 2],     // << [1, 2)        (PG range strictly left of operator)[Op.strictRight]: [1, 2],    // >> [1, 2)        (PG range strictly right of operator)[Op.noExtendRight]: [1, 2],  // &< [1, 2)        (PG range does not extend to the right of operator)[Op.noExtendLeft]: [1, 2],   // &> [1, 2)        (PG range does not extend to the left of operator)
```

### Deprecated: Operator Aliases​

In Sequelize v4, it was possible to specify strings to refer to operators, instead of using Symbols. This is now deprecated and heavily discouraged, and will probably be removed in the next major version. If you really need it, you can pass the `operatorAliases` option in the Sequelize constructor.

For example:

```
const { Sequelize, Op } = require('sequelize');const sequelize = new Sequelize('sqlite::memory:', {  operatorsAliases: {    $gt: Op.gt,  },});// Now we can use `$gt` instead of `[Op.gt]` in where clauses:Foo.findAll({  where: {    $gt: 6, // Works like using [Op.gt]  },});
```

## Simple UPDATE queries​

Update queries also accept the `where` option, just like the read queries shown above.

```
// Change everyone without a last name to "Doe"await User.update(  { lastName: 'Doe' },  {    where: {      lastName: null,    },  },);
```

## Simple DELETE queries​

Delete queries also accept the `where` option, just like the read queries shown above.

```
// Delete everyone named "Jane"await User.destroy({  where: {    firstName: 'Jane',  },});
```

To destroy everything the `TRUNCATE` SQL can be used:

```
// Truncate the tableawait User.destroy({  truncate: true,});
```

## Creating in bulk​

Sequelize provides the `Model.bulkCreate` method to allow creating multiple records at once, with only one query.

The usage of `Model.bulkCreate` is very similar to `Model.create`, by receiving an array of objects instead of a single object.

```
const captains = await Captain.bulkCreate([{ name: 'Jack Sparrow' }, { name: 'Davy Jones' }]);console.log(captains.length); // 2console.log(captains[0] instanceof Captain); // trueconsole.log(captains[0].name); // 'Jack Sparrow'console.log(captains[0].id); // 1 // (or another auto-generated value)
```

However, by default, `bulkCreate` does not run validations on each object that is going to be created (which `create` does). To make `bulkCreate` run these validations as well, you must pass the `validate: true` option. This will decrease performance. Usage example:

```
const Foo = sequelize.define('foo', {  name: {    type: DataTypes.TEXT,    validate: {      len: [4, 6],    },  },});// This will not throw an error, both instances will be createdawait Foo.bulkCreate([{ name: 'abc123' }, { name: 'name too long' }]);// This will throw an error, nothing will be createdawait Foo.bulkCreate([{ name: 'abc123' }, { name: 'name too long' }], {  validate: true,});
```

If you are accepting values directly from the user, it might be beneficial to limit the columns that you want to actually insert. To support this, `bulkCreate()` accepts a `fields` option, an array defining which fields must be considered (the rest will be ignored).

```
await User.bulkCreate([{ username: 'foo' }, { username: 'bar', admin: true }], {  fields: ['username'],});// Neither foo nor bar are admins.
```

## Ordering and Grouping​

Sequelize provides the `order` and `group` options to work with `ORDER BY` and `GROUP BY`.

### Ordering​

The `order` option takes an array of items to order the query by or a sequelize method. These *items* are themselves arrays in the form `[column, direction]`. The column will be escaped correctly and the direction will be checked in a whitelist of valid directions (such as `ASC`, `DESC`, `NULLS FIRST`, etc).

```
Subtask.findAll({  order: [    // Will escape title and validate DESC against a list of valid direction parameters    ['title', 'DESC'],    // Will order by max(age)    sequelize.fn('max', sequelize.col('age')),    // Will order by max(age) DESC    [sequelize.fn('max', sequelize.col('age')), 'DESC'],    // Will order by  otherfunction(`col1`, 12, 'lalala') DESC    [sequelize.fn('otherfunction', sequelize.col('col1'), 12, 'lalala'), 'DESC'],    // Will order an associated model's createdAt using the model name as the association's name.    [Task, 'createdAt', 'DESC'],    // Will order through an associated model's createdAt using the model names as the associations' names.    [Task, Project, 'createdAt', 'DESC'],    // Will order by an associated model's createdAt using the name of the association.    ['Task', 'createdAt', 'DESC'],    // Will order by a nested associated model's createdAt using the names of the associations.    ['Task', 'Project', 'createdAt', 'DESC'],    // Will order by an associated model's createdAt using an association object. (preferred method)    [Subtask.associations.Task, 'createdAt', 'DESC'],    // Will order by a nested associated model's createdAt using association objects. (preferred method)    [Subtask.associations.Task, Task.associations.Project, 'createdAt', 'DESC'],    // Will order by an associated model's createdAt using a simple association object.    [{ model: Task, as: 'Task' }, 'createdAt', 'DESC'],    // Will order by a nested associated model's createdAt simple association objects.    [{ model: Task, as: 'Task' }, { model: Project, as: 'Project' }, 'createdAt', 'DESC'],  ],  // Will order by max age descending  order: sequelize.literal('max(age) DESC'),  // Will order by max age ascending assuming ascending is the default order when direction is omitted  order: sequelize.fn('max', sequelize.col('age')),  // Will order by age ascending assuming ascending is the default order when direction is omitted  order: sequelize.col('age'),  // Will order randomly based on the dialect (instead of fn('RAND') or fn('RANDOM'))  order: sequelize.random(),});Foo.findOne({  order: [    // will return `name`    ['name'],    // will return `username` DESC    ['username', 'DESC'],    // will return max(`age`)    sequelize.fn('max', sequelize.col('age')),    // will return max(`age`) DESC    [sequelize.fn('max', sequelize.col('age')), 'DESC'],    // will return otherfunction(`col1`, 12, 'lalala') DESC    [sequelize.fn('otherfunction', sequelize.col('col1'), 12, 'lalala'), 'DESC'],    // will return otherfunction(awesomefunction(`col`)) DESC, This nesting is potentially infinite!    [sequelize.fn('otherfunction', sequelize.fn('awesomefunction', sequelize.col('col'))), 'DESC'],  ],});
```

To recap, the elements of the order array can be the following:

- A string (which will be automatically quoted)
- An array, whose first element will be quoted, second will be appended verbatim
- An object with a `raw` field:
  - The content of `raw` will be added verbatim without quoting
  - Everything else is ignored, and if raw is not set, the query will fail
- A call to `Sequelize.fn` (which will generate a function call in SQL)
- A call to `Sequelize.col` (which will quote the column name)

### Grouping​

The syntax for grouping and ordering are equal, except that grouping does not accept a direction as last argument of the array (there is no `ASC`, `DESC`, `NULLS FIRST`, etc).

You can also pass a string directly to `group`, which will be included directly (verbatim) into the generated SQL. Use with caution and don't use with user generated content.

```
Project.findAll({ group: 'name' });// yields 'GROUP BY name'
```

## Limits and Pagination​

The `limit` and `offset` options allow you to work with limiting / pagination:

```
// Fetch 10 instances/rowsProject.findAll({ limit: 10 });// Skip 8 instances/rowsProject.findAll({ offset: 8 });// Skip 5 instances and fetch the 5 after thatProject.findAll({ offset: 5, limit: 5 });
```

Usually these are used alongside the `order` option.

## Utility methods​

Sequelize also provides a few utility methods.

### count​

The `count` method simply counts the occurrences of elements in the database.

```
console.log(`There are ${await Project.count()} projects`);const amount = await Project.count({  where: {    id: {      [Op.gt]: 25,    },  },});console.log(`There are ${amount} projects with an id greater than 25`);
```

### max,minandsum​

Sequelize also provides the `max`, `min` and `sum` convenience methods.

Let's assume we have three users, whose ages are 10, 5, and 40.

```
await User.max('age'); // 40await User.max('age', { where: { age: { [Op.lt]: 20 } } }); // 10await User.min('age'); // 5await User.min('age', { where: { age: { [Op.gt]: 5 } } }); // 10await User.sum('age'); // 55await User.sum('age', { where: { age: { [Op.gt]: 5 } } }); // 50
```

### increment,decrement​

Sequelize also provides the `increment` convenience method.

Let's assume we have a user, whose age is 10.

```
await User.increment({ age: 5 }, { where: { id: 1 } }); // Will increase age to 15await User.increment({ age: -5 }, { where: { id: 1 } }); // Will decrease age to 5
```

---

# Model Querying

> Finder methods are the ones that generate SELECT queries.

Version: v6 - stable

Finder methods are the ones that generate `SELECT` queries.

By default, the results of all finder methods are instances of the model class (as opposed to being just plain JavaScript objects). This means that after the database returns the results, Sequelize automatically wraps everything in proper instance objects. In a few cases, when there are too many results, this wrapping can be inefficient. To disable this wrapping and receive a plain response instead, pass `{ raw: true }` as an option to the finder method.

## findAll​

The `findAll` method is already known from the previous tutorial. It generates a standard `SELECT` query which will retrieve all entries from the table (unless restricted by something like a `where` clause, for example).

## findByPk​

The `findByPk` method obtains only a single entry from the table, using the provided primary key.

```
const project = await Project.findByPk(123);if (project === null) {  console.log('Not found!');} else {  console.log(project instanceof Project); // true  // Its primary key is 123}
```

## findOne​

The `findOne` method obtains the first entry it finds (that fulfills the optional query options, if provided).

```
const project = await Project.findOne({ where: { title: 'My Title' } });if (project === null) {  console.log('Not found!');} else {  console.log(project instanceof Project); // true  console.log(project.title); // 'My Title'}
```

## findOrCreate​

The method `findOrCreate` will create an entry in the table unless it can find one fulfilling the query options. In both cases, it will return an instance (either the found instance or the created instance) and a boolean indicating whether that instance was created or already existed.

The `where` option is considered for finding the entry, and the `defaults` option is used to define what must be created in case nothing was found. If the `defaults` do not contain values for every column, Sequelize will take the values given to `where` (if present).

Let's assume we have an empty database with a `User` model which has a `username` and a `job`.

```
const [user, created] = await User.findOrCreate({  where: { username: 'sdepold' },  defaults: {    job: 'Technical Lead JavaScript',  },});console.log(user.username); // 'sdepold'console.log(user.job); // This may or may not be 'Technical Lead JavaScript'console.log(created); // The boolean indicating whether this instance was just createdif (created) {  console.log(user.job); // This will certainly be 'Technical Lead JavaScript'}
```

## findAndCountAll​

The `findAndCountAll` method is a convenience method that combines `findAll` and `count`. This is useful when dealing with queries related to pagination where you want to retrieve data with a `limit` and `offset` but also need to know the total number of records that match the query.

When `group` is not provided, the `findAndCountAll` method returns an object with two properties:

- `count` - an integer - the total number records matching the query
- `rows` - an array of objects - the obtained records

When `group` is provided, the `findAndCountAll` method returns an object with two properties:

- `count` - an array of objects - contains the count in each group and the projected attributes
- `rows` - an array of objects - the obtained records

```
const { count, rows } = await Project.findAndCountAll({  where: {    title: {      [Op.like]: 'foo%',    },  },  offset: 10,  limit: 2,});console.log(count);console.log(rows);
```

---

# Paranoid

> Sequelize supports the concept of paranoid tables. A paranoid table is one that, when told to delete a record, it will not truly delete it. Instead, a special column called deletedAt will have its value set to the timestamp of that deletion request.

Version: v6 - stable

Sequelize supports the concept of *paranoid* tables. A *paranoid* table is one that, when told to delete a record, it will not truly delete it. Instead, a special column called `deletedAt` will have its value set to the timestamp of that deletion request.

This means that paranoid tables perform a *soft-deletion* of records, instead of a *hard-deletion*.

## Defining a model as paranoid​

To make a model paranoid, you must pass the `paranoid: true` option to the model definition. Paranoid requires timestamps to work (i.e. it won't work if you also pass `timestamps: false`).

You can also change the default column name (which is `deletedAt`) to something else.

```
class Post extends Model {}Post.init(  {    /* attributes here */  },  {    sequelize,    paranoid: true,    // If you want to give a custom name to the deletedAt column    deletedAt: 'destroyTime',  },);
```

## Deleting​

When you call the `destroy` method, a soft-deletion will happen:

```
await Post.destroy({  where: {    id: 1,  },});// UPDATE "posts" SET "deletedAt"=[timestamp] WHERE "deletedAt" IS NULL AND "id" = 1
```

If you really want a hard-deletion and your model is paranoid, you can force it using the `force: true` option:

```
await Post.destroy({  where: {    id: 1,  },  force: true,});// DELETE FROM "posts" WHERE "id" = 1
```

The above examples used the static `destroy` method as an example (`Post.destroy`), but everything works in the same way with the instance method:

```
const post = await Post.create({ title: 'test' });console.log(post instanceof Post); // trueawait post.destroy(); // Would just set the `deletedAt` flagawait post.destroy({ force: true }); // Would really delete the record
```

## Restoring​

To restore soft-deleted records, you can use the `restore` method, which comes both in the static version as well as in the instance version:

```
// Example showing the instance `restore` method// We create a post, soft-delete it and then restore it backconst post = await Post.create({ title: 'test' });console.log(post instanceof Post); // trueawait post.destroy();console.log('soft-deleted!');await post.restore();console.log('restored!');// Example showing the static `restore` method.// Restoring every soft-deleted post with more than 100 likesawait Post.restore({  where: {    likes: {      [Op.gt]: 100,    },  },});
```

## Behavior with other queries​

Every query performed by Sequelize will automatically ignore soft-deleted records (except raw queries, of course).

This means that, for example, the `findAll` method will not see the soft-deleted records, fetching only the ones that were not deleted.

Even if you simply call `findByPk` providing the primary key of a soft-deleted record, the result will be `null` as if that record didn't exist.

If you really want to let the query see the soft-deleted records, you can pass the `paranoid: false` option to the query method. For example:

```
await Post.findByPk(123); // This will return `null` if the record of id 123 is soft-deletedawait Post.findByPk(123, { paranoid: false }); // This will retrieve the recordawait Post.findAll({  where: { foo: 'bar' },}); // This will not retrieve soft-deleted recordsawait Post.findAll({  where: { foo: 'bar' },  paranoid: false,}); // This will also retrieve soft-deleted records
```

---

# Raw Queries

> As there are often use cases in which it is just easier to execute raw / already prepared SQL queries, you can use the sequelize.query method.

Version: v6 - stable

As there are often use cases in which it is just easier to execute raw / already prepared SQL queries, you can use the [sequelize.query](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-method-query) method.

By default the function will return two arguments - a results array, and an object containing metadata (such as amount of affected rows, etc). Note that since this is a raw query, the metadata are dialect specific. Some dialects return the metadata "within" the results object (as properties on an array). However, two arguments will always be returned, but for MSSQL and MySQL it will be two references to the same object.

```
const [results, metadata] = await sequelize.query('UPDATE users SET y = 42 WHERE x = 12');// Results will be an empty array and metadata will contain the number of affected rows.
```

In cases where you don't need to access the metadata you can pass in a query type to tell sequelize how to format the results. For example, for a simple select query you could do:

```
const { QueryTypes } = require('sequelize');const users = await sequelize.query('SELECT * FROM `users`', {  type: QueryTypes.SELECT,});// We didn't need to destructure the result here - the results were returned directly
```

Several other query types are available. [Peek into the source for details](https://github.com/sequelize/sequelize/blob/v6/src/query-types.js).

A second option is the model. If you pass a model the returned data will be instances of that model.

```
// Callee is the model definition. This allows you to easily map a query to a predefined modelconst projects = await sequelize.query('SELECT * FROM projects', {  model: Projects,  mapToModel: true, // pass true here if you have any mapped fields});// Each element of `projects` is now an instance of Project
```

See more options in the [query API reference](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-method-query). Some examples:

```
const { QueryTypes } = require('sequelize');await sequelize.query('SELECT 1', {  // A function (or false) for logging your queries  // Will get called for every SQL query that gets sent  // to the server.  logging: console.log,  // If plain is true, then sequelize will only return the first  // record of the result set. In case of false it will return all records.  plain: false,  // Set this to true if you don't have a model definition for your query.  raw: false,  // The type of query you are executing. The query type affects how results are formatted before they are passed back.  type: QueryTypes.SELECT,});// Note the second argument being null!// Even if we declared a callee here, the raw: true would// supersede and return a raw object.console.log(await sequelize.query('SELECT * FROM projects', { raw: true }));
```

## "Dotted" attributes and thenestoption​

If an attribute name of the table contains dots, the resulting objects can become nested objects by setting the `nest: true` option. This is achieved with [dottie.js](https://github.com/mickhansen/dottie.js/) under the hood. See below:

- Without `nest: true`:
  ```
  const { QueryTypes } = require('sequelize');const records = await sequelize.query('select 1 as `foo.bar.baz`', {  type: QueryTypes.SELECT,});console.log(JSON.stringify(records[0], null, 2));
  ```
  ```
  {  "foo.bar.baz": 1}
  ```
- With `nest: true`:
  ```
  const { QueryTypes } = require('sequelize');const records = await sequelize.query('select 1 as `foo.bar.baz`', {  nest: true,  type: QueryTypes.SELECT,});console.log(JSON.stringify(records[0], null, 2));
  ```
  ```
  {  "foo": {    "bar": {      "baz": 1    }  }}
  ```

## Replacements​

Replacements in a query can be done in two different ways, either using named parameters (starting with `:`), or unnamed, represented by a `?`. Replacements are passed in the options object.

- If an array is passed, `?` will be replaced in the order that they appear in the array
- If an object is passed, `:key` will be replaced with the keys from that object. If the object contains keys not found in the query or vice versa, an exception will be thrown.

```
const { QueryTypes } = require('sequelize');await sequelize.query('SELECT * FROM projects WHERE status = ?', {  replacements: ['active'],  type: QueryTypes.SELECT,});await sequelize.query('SELECT * FROM projects WHERE status = :status', {  replacements: { status: 'active' },  type: QueryTypes.SELECT,});
```

Array replacements will automatically be handled, the following query searches for projects where the status matches an array of values.

```
const { QueryTypes } = require('sequelize');await sequelize.query('SELECT * FROM projects WHERE status IN(:status)', {  replacements: { status: ['active', 'inactive'] },  type: QueryTypes.SELECT,});
```

To use the wildcard operator `%`, append it to your replacement. The following query matches users with names that start with 'ben'.

```
const { QueryTypes } = require('sequelize');await sequelize.query('SELECT * FROM users WHERE name LIKE :search_name', {  replacements: { search_name: 'ben%' },  type: QueryTypes.SELECT,});
```

## Bind Parameter​

Bind parameters are like replacements. Except replacements are escaped and inserted into the query by sequelize before the query is sent to the database, while bind parameters are sent to the database outside the SQL query text. A query can have either bind parameters or replacements. Bind parameters are referred to by either $1, $2, ... (numeric) or $key (alpha-numeric). This is independent of the dialect.

- If an array is passed, `$1` is bound to the 1st element in the array (`bind[0]`)
- If an object is passed, `$key` is bound to `object['key']`. Each key must begin with a non-numeric char. `$1` is not a valid key, even if `object['1']` exists.
- In either case `$$` can be used to escape a literal `$` sign.

The array or object must contain all bound values or Sequelize will throw an exception. This applies even to cases in which the database may ignore the bound parameter.

The database may add further restrictions to this. Bind parameters cannot be SQL keywords, nor table or column names. They are also ignored in quoted text or data. In PostgreSQL it may also be needed to typecast them, if the type cannot be inferred from the context `$1::varchar`.

```
const { QueryTypes } = require('sequelize');await sequelize.query(  'SELECT *, "text with literal $$1 and literal $$status" as t FROM projects WHERE status = $1',  {    bind: ['active'],    type: QueryTypes.SELECT,  },);await sequelize.query(  'SELECT *, "text with literal $$1 and literal $$status" as t FROM projects WHERE status = $status',  {    bind: { status: 'active' },    type: QueryTypes.SELECT,  },);
```
