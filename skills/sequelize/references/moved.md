# Associations and more

# Associations

> The contents of this page were moved to other specialized guides.

Version: v6 - stable

The contents of this page were moved to other specialized guides.

If you're here, you might be looking for these topics:

- **Core Concepts**
  - [Associations](https://sequelize.org/docs/v6/core-concepts/assocs/)
- **Advanced Association Concepts**
  - [Eager Loading](https://sequelize.org/docs/v6/advanced-association-concepts/eager-loading/)
  - [Creating with Associations](https://sequelize.org/docs/v6/advanced-association-concepts/creating-with-associations/)
  - [Advanced M:NAssociations](https://sequelize.org/docs/v6/advanced-association-concepts/advanced-many-to-many/)
  - [Polymorphism & Scopes](https://sequelize.org/docs/v6/advanced-association-concepts/polymorphic-associations/)
- **Other Topics**
  - [Naming Strategies](https://sequelize.org/docs/v6/other-topics/naming-strategies/)
  - [Constraints & Circularities](https://sequelize.org/docs/v6/other-topics/constraints-and-circularities/)

---

# Data Types

> The contents of this page were moved to other specialized guides.

Version: v6 - stable

The contents of this page were moved to other specialized guides.

If you're here, you might be looking for these topics:

- **Core Concepts**
  - [Model Basics: Data Types](https://sequelize.org/docs/v6/core-concepts/model-basics/#data-types)
- **Other Topics**
  - [Other Data Types](https://sequelize.org/docs/v6/other-topics/other-data-types/)
  - [Extending Data Types](https://sequelize.org/docs/v6/other-topics/extending-data-types/)
  - [Dialect-Specific Things](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/)

---

# Models Definition

> The contents of this page were moved to Model Basics.

Version: v6 - stable

The contents of this page were moved to [Model Basics](https://sequelize.org/docs/v6/core-concepts/model-basics/).

The only exception is the guide on `sequelize.import`, which is deprecated and was removed from the docs. However, if you really need it, it was kept here.

---

## Deprecated:sequelize.import​

> *Note:You should not usesequelize.import. Please just useimport,import(), orrequireinstead.*
>
>
>
> *This documentation has been kept just in case you really need to maintain old code that uses it.*

`sequelize.import` can only load [CommonJS](https://nodejs.org/api/modules.html) files, and is not capable of loading [ecmascript modules](https://nodejs.org/api/esm.html). Use native `import` if you need to load ecmascript modules.

You can store your model definitions in a single file using the `sequelize.import` method. The returned object is exactly the same as defined in the imported file's function. The import is cached, just like `require`, so you won't run into trouble if importing a file more than once.

```
// in your server file - e.g. app.jsconst Project = sequelize.import(__dirname + '/path/to/models/project');// The model definition is done in /path/to/models/project.jsmodule.exports = (sequelize, DataTypes) => {  return sequelize.define('project', {    name: DataTypes.STRING,    description: DataTypes.TEXT,  });};
```

The `import` method can also accept a callback as an argument.

```
sequelize.import('project', (sequelize, DataTypes) => {  return sequelize.define('project', {    name: DataTypes.STRING,    description: DataTypes.TEXT,  });});
```

This extra capability is useful when, for example, `Error: Cannot find module` is thrown even though `/path/to/models/project` seems to be correct. Some frameworks, such as Meteor, overload `require`, and might raise an error such as:

```
Error: Cannot find module '/home/you/meteorApp/.meteor/local/build/programs/server/app/path/to/models/project.js'
```

This can be worked around by passing in Meteor's version of `require`:

```
// If this fails...const AuthorModel = db.import('./path/to/models/project');// Try this instead!const AuthorModel = db.import('project', require('./path/to/models/project'));
```

---

# Models Usage

> The contents of this page were moved to other specialized guides.

Version: v6 - stable

The contents of this page were moved to other specialized guides.

If you're here, you might be looking for these topics:

- **Core Concepts**
  - [Model Querying - Basics](https://sequelize.org/docs/v6/core-concepts/model-querying-basics/)
  - [Model Querying - Finders](https://sequelize.org/docs/v6/core-concepts/model-querying-finders/)
  - [Raw Queries](https://sequelize.org/docs/v6/core-concepts/raw-queries/)
- **Advanced Association Concepts**
  - [Eager Loading](https://sequelize.org/docs/v6/advanced-association-concepts/eager-loading/)

---

# Querying

> The contents of this page were moved to other specialized guides.

Version: v6 - stable

The contents of this page were moved to other specialized guides.

If you're here, you might be looking for these topics:

- **Core Concepts**
  - [Model Querying - Basics](https://sequelize.org/docs/v6/core-concepts/model-querying-basics/)
  - [Model Querying - Finders](https://sequelize.org/docs/v6/core-concepts/model-querying-finders/)
  - [Raw Queries](https://sequelize.org/docs/v6/core-concepts/raw-queries/)
  - [Associations](https://sequelize.org/docs/v6/core-concepts/assocs/)
- **Other Topics**
  - [Dialect-Specific Things](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/)
