# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Special Relationship Persistence Patterns

## Rows that point to themselves / Mutually Dependent Rows

This is a very specific case where relationship() must perform an INSERT and a
second UPDATE in order to properly populate a row (and vice versa an UPDATE
and DELETE in order to delete without violating foreign key constraints). The
two use cases are:

- A table contains a foreign key to itself, and a single row will
  have a foreign key value pointing to its own primary key.
- Two tables each contain a foreign key referencing the other
  table, with a row in each table referencing the other.

For example:

```
user
---------------------------------
user_id    name   related_user_id
   1       'ed'          1
```

Or:

```
widget                                                  entry
-------------------------------------------             ---------------------------------
widget_id     name        favorite_entry_id             entry_id      name      widget_id
   1       'somewidget'          5                         5       'someentry'     1
```

In the first case, a row points to itself. Technically, a database that uses
sequences such as PostgreSQL or Oracle Database can INSERT the row at once
using a previously generated value, but databases which rely upon
autoincrement-style primary key identifiers cannot. The
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) always assumes a “parent/child” model of
row population during flush, so unless you are populating the primary
key/foreign key columns directly, [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) needs to
use two statements.

In the second case, the “widget” row must be inserted before any referring
“entry” rows, but then the “favorite_entry_id” column of that “widget” row
cannot be set until the “entry” rows have been generated. In this case, it’s
typically impossible to insert the “widget” and “entry” rows using just two
INSERT statements; an UPDATE must be performed in order to keep foreign key
constraints fulfilled. The exception is if the foreign keys are configured as
“deferred until commit” (a feature some databases support) and if the
identifiers were populated manually (again essentially bypassing
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)).

To enable the usage of a supplementary UPDATE statement,
we use the [relationship.post_update](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.post_update) option
of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).  This specifies that the linkage between the
two rows should be created using an UPDATE statement after both rows
have been INSERTED; it also causes the rows to be de-associated with
each other via UPDATE before a DELETE is emitted.  The flag should
be placed on just *one* of the relationships, preferably the
many-to-one side.  Below we illustrate
a complete example, including two [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) constructs:

```
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Entry(Base):
    __tablename__ = "entry"
    entry_id = mapped_column(Integer, primary_key=True)
    widget_id = mapped_column(Integer, ForeignKey("widget.widget_id"))
    name = mapped_column(String(50))

class Widget(Base):
    __tablename__ = "widget"

    widget_id = mapped_column(Integer, primary_key=True)
    favorite_entry_id = mapped_column(
        Integer, ForeignKey("entry.entry_id", name="fk_favorite_entry")
    )
    name = mapped_column(String(50))

    entries = relationship(Entry, primaryjoin=widget_id == Entry.widget_id)
    favorite_entry = relationship(
        Entry, primaryjoin=favorite_entry_id == Entry.entry_id, post_update=True
    )
```

When a structure against the above configuration is flushed, the “widget” row will be
INSERTed minus the “favorite_entry_id” value, then all the “entry” rows will
be INSERTed referencing the parent “widget” row, and then an UPDATE statement
will populate the “favorite_entry_id” column of the “widget” table (it’s one
row at a time for the time being):

```
>>> w1 = Widget(name="somewidget")
>>> e1 = Entry(name="someentry")
>>> w1.favorite_entry = e1
>>> w1.entries = [e1]
>>> session.add_all([w1, e1])
>>> session.commit()
BEGIN (implicit)
INSERT INTO widget (favorite_entry_id, name) VALUES (?, ?)
(None, 'somewidget')
INSERT INTO entry (widget_id, name) VALUES (?, ?)
(1, 'someentry')
UPDATE widget SET favorite_entry_id=? WHERE widget.widget_id = ?
(1, 1)
COMMIT
```

An additional configuration we can specify is to supply a more
comprehensive foreign key constraint on `Widget`, such that
it’s guaranteed that `favorite_entry_id` refers to an `Entry`
that also refers to this `Widget`.  We can use a composite foreign key,
as illustrated below:

```
from sqlalchemy import (
    Integer,
    ForeignKey,
    String,
    UniqueConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Entry(Base):
    __tablename__ = "entry"
    entry_id = mapped_column(Integer, primary_key=True)
    widget_id = mapped_column(Integer, ForeignKey("widget.widget_id"))
    name = mapped_column(String(50))
    __table_args__ = (UniqueConstraint("entry_id", "widget_id"),)

class Widget(Base):
    __tablename__ = "widget"

    widget_id = mapped_column(Integer, autoincrement="ignore_fk", primary_key=True)
    favorite_entry_id = mapped_column(Integer)

    name = mapped_column(String(50))

    __table_args__ = (
        ForeignKeyConstraint(
            ["widget_id", "favorite_entry_id"],
            ["entry.widget_id", "entry.entry_id"],
            name="fk_favorite_entry",
        ),
    )

    entries = relationship(
        Entry, primaryjoin=widget_id == Entry.widget_id, foreign_keys=Entry.widget_id
    )
    favorite_entry = relationship(
        Entry,
        primaryjoin=favorite_entry_id == Entry.entry_id,
        foreign_keys=favorite_entry_id,
        post_update=True,
    )
```

The above mapping features a composite [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
bridging the `widget_id` and `favorite_entry_id` columns.  To ensure
that `Widget.widget_id` remains an “autoincrementing” column we specify
[Column.autoincrement](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.autoincrement) to the value `"ignore_fk"`
on [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column), and additionally on each
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) we must limit those columns considered as part of
the foreign key for the purposes of joining and cross-population.

## Mutable Primary Keys / Update Cascades

When the primary key of an entity changes, related items
which reference the primary key must also be updated as
well. For databases which enforce referential integrity,
the best strategy is to use the database’s ON UPDATE CASCADE
functionality in order to propagate primary key changes
to referenced foreign keys - the values cannot be out
of sync for any moment unless the constraints are marked as “deferrable”,
that is, not enforced until the transaction completes.

It is **highly recommended** that an application which seeks to employ
natural primary keys with mutable values to use the `ON UPDATE CASCADE`
capabilities of the database.   An example mapping which
illustrates this is:

```
class User(Base):
    __tablename__ = "user"
    __table_args__ = {"mysql_engine": "InnoDB"}

    username = mapped_column(String(50), primary_key=True)
    fullname = mapped_column(String(100))

    addresses = relationship("Address")

class Address(Base):
    __tablename__ = "address"
    __table_args__ = {"mysql_engine": "InnoDB"}

    email = mapped_column(String(50), primary_key=True)
    username = mapped_column(
        String(50), ForeignKey("user.username", onupdate="cascade")
    )
```

Above, we illustrate `onupdate="cascade"` on the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)
object, and we also illustrate the `mysql_engine='InnoDB'` setting
which, on a MySQL backend, ensures that the `InnoDB` engine supporting
referential integrity is used.  When using SQLite, referential integrity
should be enabled, using the configuration described at
[Foreign Key Support](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-foreign-keys).

See also

[Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes) - supporting ON DELETE CASCADE with relationships

`mapper.passive_updates` - similar feature on [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)

### Simulating limited ON UPDATE CASCADE without foreign key support

In those cases when a database that does not support referential integrity
is used, and natural primary keys with mutable values are in play,
SQLAlchemy offers a feature in order to allow propagation of primary key
values to already-referenced foreign keys to a **limited** extent,
by emitting an UPDATE statement against foreign key columns that immediately
reference a primary key column whose value has changed.
The primary platforms without referential integrity features are
MySQL when the `MyISAM` storage engine is used, and SQLite when the
`PRAGMA foreign_keys=ON` pragma is not used.  Oracle Database also
has no support for `ON UPDATE CASCADE`, but because it still enforces
referential integrity, needs constraints to be marked as deferrable
so that SQLAlchemy can emit UPDATE statements.

The feature is enabled by setting the
[relationship.passive_updates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.passive_updates) flag to `False`,
most preferably on a one-to-many or
many-to-many [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).  When “updates” are no longer
“passive” this indicates that SQLAlchemy will
issue UPDATE statements individually for
objects referenced in the collection referred to by the parent object
with a changing primary key value.  This also implies that collections
will be fully loaded into memory if not already locally present.

Our previous mapping using `passive_updates=False` looks like:

```
class User(Base):
    __tablename__ = "user"

    username = mapped_column(String(50), primary_key=True)
    fullname = mapped_column(String(100))

    # passive_updates=False *only* needed if the database
    # does not implement ON UPDATE CASCADE
    addresses = relationship("Address", passive_updates=False)

class Address(Base):
    __tablename__ = "address"

    email = mapped_column(String(50), primary_key=True)
    username = mapped_column(String(50), ForeignKey("user.username"))
```

Key limitations of `passive_updates=False` include:

- it performs much more poorly than direct database ON UPDATE CASCADE,
  because it needs to fully pre-load affected collections using SELECT
  and also must emit  UPDATE statements against those values, which it
  will attempt to run  in “batches” but still runs on a per-row basis
  at the DBAPI level.
- the feature cannot “cascade” more than one level.  That is,
  if mapping X has a foreign key which refers to the primary key
  of mapping Y, but then mapping Y’s primary key is itself a foreign key
  to mapping Z, `passive_updates=False` cannot cascade a change in
  primary key value from `Z` to `X`.
- Configuring `passive_updates=False` only on the many-to-one
  side of a relationship will not have a full effect, as the
  unit of work searches only through the current identity
  map for objects that may be referencing the one with a
  mutating primary key, not throughout the database.

As virtually all databases other than Oracle Database now support `ON UPDATE
CASCADE`, it is highly recommended that traditional `ON UPDATE CASCADE`
support be used in the case that natural and mutable primary key values are in
use.

---

# SQLAlchemy 2.0 Documentation

# Relationship Configuration

This section describes the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) function and in depth discussion
of its usage.   For an introduction to relationships, start with
[Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial).

- [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
  - [Declarative vs. Imperative Forms](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#declarative-vs-imperative-forms)
  - [One To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many)
    - [Using Sets, Lists, or other Collection Types for One To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-sets-lists-or-other-collection-types-for-one-to-many)
    - [Configuring Delete Behavior for One to Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#configuring-delete-behavior-for-one-to-many)
  - [Many To One](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one)
    - [Nullable Many-to-One](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#nullable-many-to-one)
  - [One To One](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-one)
    - [Setting uselist=False for non-annotated configurations](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-uselist-false-for-non-annotated-configurations)
  - [Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many)
    - [Setting Bi-Directional Many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many)
    - [Using a late-evaluated form for the “secondary” argument](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-a-late-evaluated-form-for-the-secondary-argument)
    - [Using Sets, Lists, or other Collection Types for Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-sets-lists-or-other-collection-types-for-many-to-many)
    - [Deleting Rows from the Many to Many Table](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table)
  - [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object)
    - [Combining Association Object with Many-to-Many Access Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#combining-association-object-with-many-to-many-access-patterns)
  - [Late-Evaluation of Relationship Arguments](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#late-evaluation-of-relationship-arguments)
    - [Adding Relationships to Mapped Classes After Declaration](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#adding-relationships-to-mapped-classes-after-declaration)
    - [Using a late-evaluated form for the “secondary” argument of many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-a-late-evaluated-form-for-the-secondary-argument-of-many-to-many)
- [Adjacency List Relationships](https://docs.sqlalchemy.org/en/20/orm/self_referential.html)
  - [Composite Adjacency Lists](https://docs.sqlalchemy.org/en/20/orm/self_referential.html#composite-adjacency-lists)
  - [Self-Referential Query Strategies](https://docs.sqlalchemy.org/en/20/orm/self_referential.html#self-referential-query-strategies)
  - [Configuring Self-Referential Eager Loading](https://docs.sqlalchemy.org/en/20/orm/self_referential.html#configuring-self-referential-eager-loading)
- [Configuring how Relationship Joins](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html)
  - [Handling Multiple Join Paths](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#handling-multiple-join-paths)
  - [Specifying Alternate Join Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#specifying-alternate-join-conditions)
  - [Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#creating-custom-foreign-conditions)
  - [Using custom operators in join conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#using-custom-operators-in-join-conditions)
  - [Custom operators based on SQL functions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#custom-operators-based-on-sql-functions)
  - [Overlapping Foreign Keys](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#overlapping-foreign-keys)
  - [Non-relational Comparisons / Materialized Path](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#non-relational-comparisons-materialized-path)
  - [Self-Referential Many-to-Many Relationship](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#self-referential-many-to-many-relationship)
  - [Composite “Secondary” Joins](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#composite-secondary-joins)
  - [Relationship to Aliased Class](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-to-aliased-class)
    - [Integrating AliasedClass Mappings with Typing and Avoiding Early Mapper Configuration](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#integrating-aliasedclass-mappings-with-typing-and-avoiding-early-mapper-configuration)
    - [Using the AliasedClass target in Queries](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#using-the-aliasedclass-target-in-queries)
  - [Row-Limited Relationships with Window Functions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#row-limited-relationships-with-window-functions)
  - [Building Query-Enabled Properties](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#building-query-enabled-properties)
  - [Notes on using the viewonly relationship parameter](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#notes-on-using-the-viewonly-relationship-parameter)
    - [In-Python mutations including backrefs are not appropriate with viewonly=True](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#in-python-mutations-including-backrefs-are-not-appropriate-with-viewonly-true)
    - [viewonly=True collections / attributes do not get re-queried until expired](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#viewonly-true-collections-attributes-do-not-get-re-queried-until-expired)
- [Working with Large Collections](https://docs.sqlalchemy.org/en/20/orm/large_collections.html)
  - [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationships)
    - [Creating and Persisting New Write Only Collections](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#creating-and-persisting-new-write-only-collections)
    - [Adding New Items to an Existing Collection](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#adding-new-items-to-an-existing-collection)
    - [Querying Items](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#querying-items)
    - [Removing Items](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#removing-items)
    - [Bulk INSERT of New Items](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#bulk-insert-of-new-items)
    - [Bulk UPDATE and DELETE of Items](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#bulk-update-and-delete-of-items)
    - [Write Only Collections - API Documentation](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-collections-api-documentation)
  - [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship-loaders)
    - [Dynamic Relationship Loaders - API](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship-loaders-api)
  - [Setting RaiseLoad](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#setting-raiseload)
  - [Using Passive Deletes](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#using-passive-deletes)
- [Collection Customization and API Details](https://docs.sqlalchemy.org/en/20/orm/collection_api.html)
  - [Customizing Collection Access](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#customizing-collection-access)
    - [Dictionary Collections](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#dictionary-collections)
  - [Custom Collection Implementations](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-collection-implementations)
    - [Annotating Custom Collections via Decorators](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#annotating-custom-collections-via-decorators)
    - [Custom Dictionary-Based Collections](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-dictionary-based-collections)
    - [Instrumentation and Custom Types](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#instrumentation-and-custom-types)
  - [Collection API](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#collection-api)
    - [attribute_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_keyed_dict)
    - [column_keyed_dict()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_keyed_dict)
    - [keyfunc_mapping()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.keyfunc_mapping)
    - [attribute_mapped_collection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.attribute_mapped_collection)
    - [column_mapped_collection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.column_mapped_collection)
    - [mapped_collection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.mapped_collection)
    - [KeyFuncDict](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.KeyFuncDict)
    - [MappedCollection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.MappedCollection)
  - [Collection Internals](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#collection-internals)
    - [bulk_replace()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.bulk_replace)
    - [collection](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.collection)
    - [collection_adapter](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.collection_adapter)
    - [CollectionAdapter](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.CollectionAdapter)
    - [InstrumentedDict](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.InstrumentedDict)
    - [InstrumentedList](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.InstrumentedList)
    - [InstrumentedSet](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.InstrumentedSet)
    - [prepare_instrumentation()](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#sqlalchemy.orm.collections.prepare_instrumentation)
- [Special Relationship Persistence Patterns](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html)
  - [Rows that point to themselves / Mutually Dependent Rows](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#rows-that-point-to-themselves-mutually-dependent-rows)
  - [Mutable Primary Keys / Update Cascades](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#mutable-primary-keys-update-cascades)
    - [Simulating limited ON UPDATE CASCADE without foreign key support](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#simulating-limited-on-update-cascade-without-foreign-key-support)
- [Using the legacy ‘backref’ relationship parameter](https://docs.sqlalchemy.org/en/20/orm/backref.html)
  - [Backref Default Arguments](https://docs.sqlalchemy.org/en/20/orm/backref.html#backref-default-arguments)
  - [Specifying Backref Arguments](https://docs.sqlalchemy.org/en/20/orm/backref.html#specifying-backref-arguments)
- [Relationships API](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html)
  - [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
  - [backref()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.backref)
  - [dynamic_loader()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.dynamic_loader)
  - [foreign()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.foreign)
  - [remote()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.remote)

---

# SQLAlchemy 2.0 Documentation

Release: 2.0.46 current release

        | Release Date: January 21, 2026

# SQLAlchemy 2.0 Documentation

### SQLAlchemy 2.0 Documentation

current release

[Home](https://docs.sqlalchemy.org/en/20/index.html)
                | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

### SQLAlchemy ORM

- [ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html)
  - [ORM Mapped Class Overview](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
  - [Mapping Classes with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html)
  - [Integration with dataclasses and attrs](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html)
  - [SQL Expressions as Mapped Attributes](https://docs.sqlalchemy.org/en/20/orm/mapped_sql_expr.html)
  - [Changing Attribute Behavior](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html)
  - [Composite Column Types](https://docs.sqlalchemy.org/en/20/orm/composites.html)
  - [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html)
  - [Non-Traditional Mappings](https://docs.sqlalchemy.org/en/20/orm/nonstandard_mappings.html)
  - [Configuring a Version Counter](https://docs.sqlalchemy.org/en/20/orm/versioning.html)
  - [Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
  - **Mapping SQL Expressions**
    - [Mapping Table Columns](https://docs.sqlalchemy.org/en/20/orm/mapping_columns.html)
- [Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [Using the Session](https://docs.sqlalchemy.org/en/20/orm/session.html)
- [Events and Internals](https://docs.sqlalchemy.org/en/20/orm/extending.html)
- [ORM Extensions](https://docs.sqlalchemy.org/en/20/orm/extensions/index.html)
- [ORM Examples](https://docs.sqlalchemy.org/en/20/orm/examples.html)

#### Project Versions

- [2.0.46](https://docs.sqlalchemy.org/en/20/index.html)

[Home](https://docs.sqlalchemy.org/en/20/index.html)
        | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

- **Previous:** [Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
- **Next:** [Mapping Table Columns](https://docs.sqlalchemy.org/en/20/orm/mapping_columns.html)
- **Up:** [Home](https://docs.sqlalchemy.org/en/20/index.html)
- **On this page:**

# Mapping SQL Expressions

This page has been merged into the
[ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html) index.

        Previous:
        [Class Mapping API](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
        Next:
        [Mapping Table Columns](https://docs.sqlalchemy.org/en/20/orm/mapping_columns.html)
        © [Copyright](https://docs.sqlalchemy.org/en/20/copyright.html) 2007-2026, the SQLAlchemy authors and contributors.

**flambé!** the dragon and **The Alchemist** image designs created and generously donated by [Rotem Yaari](https://github.com/vmalloc).

        Created using [Sphinx](https://www.sphinx-doc.org) 9.1.0.

    Documentation last generated: Thu 29 Jan 2026 03:06:31 PM  EST

---

# SQLAlchemy 2.0 Documentation

# Adjacency List Relationships

The **adjacency list** pattern is a common relational pattern whereby a table
contains a foreign key reference to itself, in other words is a
**self referential relationship**. This is the most common
way to represent hierarchical data in flat tables.  Other methods
include **nested sets**, sometimes called “modified preorder”,
as well as **materialized path**.  Despite the appeal that modified preorder
has when evaluated for its fluency within SQL queries, the adjacency list model is
probably the most appropriate pattern for the large majority of hierarchical
storage needs, for reasons of concurrency, reduced complexity, and that
modified preorder has little advantage over an application which can fully
load subtrees into the application space.

See also

This section details the single-table version of a self-referential
relationship. For a self-referential relationship that uses a second table
as an association table, see the section
[Self-Referential Many-to-Many Relationship](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#self-referential-many-to-many).

In this example, we’ll work with a single mapped
class called `Node`, representing a tree structure:

```
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    children = relationship("Node")
```

With this structure, a graph such as the following:

```
root --+---> child1
       +---> child2 --+--> subchild1
       |              +--> subchild2
       +---> child3
```

Would be represented with data such as:

```
id       parent_id     data
---      -------       ----
1        NULL          root
2        1             child1
3        1             child2
4        3             subchild1
5        3             subchild2
6        1             child3
```

The [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) configuration here works in the
same way as a “normal” one-to-many relationship, with the
exception that the “direction”, i.e. whether the relationship
is one-to-many or many-to-one, is assumed by default to
be one-to-many.   To establish the relationship as many-to-one,
an extra directive is added known as [relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side), which
is a [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) or collection of [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects
that indicate those which should be considered to be “remote”:

```
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    parent = relationship("Node", remote_side=[id])
```

Where above, the `id` column is applied as the [relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side)
of the `parent` [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship), thus establishing
`parent_id` as the “local” side, and the relationship
then behaves as a many-to-one.

As always, both directions can be combined into a bidirectional
relationship using two [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs linked by
[relationship.back_populates](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates):

```
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    children = relationship("Node", back_populates="parent")
    parent = relationship("Node", back_populates="children", remote_side=[id])
```

See also

[Adjacency List](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-adjacencylist) - working example, updated for SQLAlchemy 2.0

## Composite Adjacency Lists

A sub-category of the adjacency list relationship is the rare
case where a particular column is present on both the “local” and
“remote” side of the join condition.  An example is the `Folder`
class below; using a composite primary key, the `account_id`
column refers to itself, to indicate sub folders which are within
the same account as that of the parent; while `folder_id` refers
to a specific folder within that account:

```
class Folder(Base):
    __tablename__ = "folder"
    __table_args__ = (
        ForeignKeyConstraint(
            ["account_id", "parent_id"], ["folder.account_id", "folder.folder_id"]
        ),
    )

    account_id = mapped_column(Integer, primary_key=True)
    folder_id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer)
    name = mapped_column(String)

    parent_folder = relationship(
        "Folder", back_populates="child_folders", remote_side=[account_id, folder_id]
    )

    child_folders = relationship("Folder", back_populates="parent_folder")
```

Above, we pass `account_id` into the [relationship.remote_side](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side) list.
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) recognizes that the `account_id` column here
is on both sides, and aligns the “remote” column along with the
`folder_id` column, which it recognizes as uniquely present on
the “remote” side.

## Self-Referential Query Strategies

Querying of self-referential structures works like any other query:

```
# get all nodes named 'child2'
session.scalars(select(Node).where(Node.data == "child2"))
```

However extra care is needed when attempting to join along
the foreign key from one level of the tree to the next.  In SQL,
a join from a table to itself requires that at least one side of the
expression be “aliased” so that it can be unambiguously referred to.

Recall from [Selecting ORM Aliases](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-orm-aliases) in the ORM tutorial that the
[aliased()](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#sqlalchemy.orm.aliased) construct is normally used to provide an “alias” of
an ORM entity.  Joining from `Node` to itself using this technique
looks like:

```
from sqlalchemy.orm import aliased

nodealias = aliased(Node)
session.scalars(
    select(Node)
    .where(Node.data == "subchild1")
    .join(Node.parent.of_type(nodealias))
    .where(nodealias.data == "child2")
).all()
SELECT node.id AS node_id,
        node.parent_id AS node_parent_id,
        node.data AS node_data
FROM node JOIN node AS node_1
    ON node.parent_id = node_1.id
WHERE node.data = ?
    AND node_1.data = ?
['subchild1', 'child2']
```

## Configuring Self-Referential Eager Loading

Eager loading of relationships occurs using joins or outerjoins from parent to
child table during a normal query operation, such that the parent and its
immediate child collection or reference can be populated from a single SQL
statement, or a second statement for all immediate child collections.
SQLAlchemy’s joined and subquery eager loading use aliased tables in all cases
when joining to related items, so are compatible with self-referential
joining. However, to use eager loading with a self-referential relationship,
SQLAlchemy needs to be told how many levels deep it should join and/or query;
otherwise the eager load will not take place at all. This depth setting is
configured via [relationships.join_depth](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.relationships.params.join_depth):

```
class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    children = relationship("Node", lazy="joined", join_depth=2)

session.scalars(select(Node)).all()
SELECT node_1.id AS node_1_id,
        node_1.parent_id AS node_1_parent_id,
        node_1.data AS node_1_data,
        node_2.id AS node_2_id,
        node_2.parent_id AS node_2_parent_id,
        node_2.data AS node_2_data,
        node.id AS node_id,
        node.parent_id AS node_parent_id,
        node.data AS node_data
FROM node
    LEFT OUTER JOIN node AS node_2
        ON node.id = node_2.parent_id
    LEFT OUTER JOIN node AS node_1
        ON node_2.id = node_1.parent_id
[]
```

---

# SQLAlchemy 2.0 Documentation

# Using the Session

The declarative base and ORM mapping functions described at
[ORM Mapped Class Configuration](https://docs.sqlalchemy.org/en/20/orm/mapper_config.html) are the primary configurational interface for the
ORM. Once mappings are configured, the primary usage interface for
persistence operations is the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

- [Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
  - [What does the Session do ?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#what-does-the-session-do)
  - [Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#basics-of-using-a-session)
    - [Opening and Closing a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#opening-and-closing-a-session)
    - [Framing out a begin / commit / rollback block](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block)
    - [Using a sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker)
    - [Querying](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#querying)
    - [Adding New or Existing Items](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#adding-new-or-existing-items)
    - [Deleting](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#deleting)
    - [Flushing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#flushing)
    - [Get by Primary Key](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#get-by-primary-key)
    - [Expiring / Refreshing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#expiring-refreshing)
    - [UPDATE and DELETE with arbitrary WHERE clause](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#update-and-delete-with-arbitrary-where-clause)
    - [Auto Begin](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#auto-begin)
    - [Committing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#committing)
    - [Rolling Back](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#rolling-back)
    - [Closing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#closing)
  - [Session Frequently Asked Questions](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-frequently-asked-questions)
    - [When do I make asessionmaker?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-make-a-sessionmaker)
    - [When do I construct aSession, when do I commit it, and when do I close it?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it)
    - [Is the Session a cache?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-a-cache)
    - [How can I get theSessionfor a certain object?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#how-can-i-get-the-session-for-a-certain-object)
    - [Is the Session thread-safe?  Is AsyncSession safe to share in concurrent tasks?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks)
- [State Management](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html)
  - [Quickie Intro to Object States](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#quickie-intro-to-object-states)
    - [Getting the Current State of an Object](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#getting-the-current-state-of-an-object)
  - [Session Attributes](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-attributes)
  - [Session Referencing Behavior](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-referencing-behavior)
  - [Merging](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#merging)
    - [Merge Tips](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#merge-tips)
  - [Expunging](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#expunging)
  - [Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#refreshing-expiring)
    - [What Actually Loads](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#what-actually-loads)
    - [When to Expire or Refresh](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#when-to-expire-or-refresh)
- [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html)
  - [save-update](https://docs.sqlalchemy.org/en/20/orm/cascades.html#save-update)
    - [Behavior of save-update cascade with bi-directional relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#behavior-of-save-update-cascade-with-bi-directional-relationships)
  - [delete](https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete)
    - [Using delete cascade with many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-delete-cascade-with-many-to-many-relationships)
    - [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-foreign-key-on-delete-cascade-with-orm-relationships)
    - [Using foreign key ON DELETE with many-to-many relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#using-foreign-key-on-delete-with-many-to-many-relationships)
  - [delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete-orphan)
  - [merge](https://docs.sqlalchemy.org/en/20/orm/cascades.html#merge)
  - [refresh-expire](https://docs.sqlalchemy.org/en/20/orm/cascades.html#refresh-expire)
  - [expunge](https://docs.sqlalchemy.org/en/20/orm/cascades.html#expunge)
  - [Notes on Delete - Deleting Objects Referenced from Collections and Scalar Relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#notes-on-delete-deleting-objects-referenced-from-collections-and-scalar-relationships)
- [Transactions and Connection Management](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)
  - [Managing Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#managing-transactions)
    - [Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#using-savepoint)
    - [Session-level vs. Engine level transaction control](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-level-vs-engine-level-transaction-control)
    - [Explicit Begin](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#explicit-begin)
    - [Enabling Two-Phase Commit](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#enabling-two-phase-commit)
    - [Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#setting-transaction-isolation-levels-dbapi-autocommit)
    - [Tracking Transaction State with Events](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#tracking-transaction-state-with-events)
  - [Joining a Session into an External Transaction (such as for test suites)](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [Additional Persistence Techniques](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html)
  - [Embedding SQL Insert/Update Expressions into a Flush](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#embedding-sql-insert-update-expressions-into-a-flush)
  - [Using SQL Expressions with Sessions](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#using-sql-expressions-with-sessions)
  - [Forcing NULL on a column with a default](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#forcing-null-on-a-column-with-a-default)
  - [Fetching Server-Generated Defaults](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#fetching-server-generated-defaults)
    - [Case 1: non primary key, RETURNING or equivalent is supported](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#case-1-non-primary-key-returning-or-equivalent-is-supported)
    - [Case 2: Table includes trigger-generated values which are not compatible with RETURNING](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#case-2-table-includes-trigger-generated-values-which-are-not-compatible-with-returning)
    - [Case 3: non primary key, RETURNING or equivalent is not supported or not needed](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#case-3-non-primary-key-returning-or-equivalent-is-not-supported-or-not-needed)
    - [Case 4: primary key, RETURNING or equivalent is supported](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#case-4-primary-key-returning-or-equivalent-is-supported)
    - [Case 5: primary key, RETURNING or equivalent is not supported](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#case-5-primary-key-returning-or-equivalent-is-not-supported)
    - [Notes on eagerly fetching client invoked SQL expressions used for INSERT or UPDATE](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#notes-on-eagerly-fetching-client-invoked-sql-expressions-used-for-insert-or-update)
  - [Using INSERT, UPDATE and ON CONFLICT (i.e. upsert) to return ORM Objects](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#using-insert-update-and-on-conflict-i-e-upsert-to-return-orm-objects)
    - [Using PostgreSQL ON CONFLICT with RETURNING to return upserted ORM objects](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#using-postgresql-on-conflict-with-returning-to-return-upserted-orm-objects)
  - [Partitioning Strategies (e.g. multiple database backends per Session)](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session)
    - [Simple Vertical Partitioning](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#simple-vertical-partitioning)
    - [Coordination of Transactions for a multiple-engine Session](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#coordination-of-transactions-for-a-multiple-engine-session)
    - [Custom Vertical Partitioning](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#custom-vertical-partitioning)
    - [Horizontal Partitioning](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#horizontal-partitioning)
  - [Bulk Operations](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#bulk-operations)
- [Contextual/Thread-local Sessions](https://docs.sqlalchemy.org/en/20/orm/contextual.html)
  - [Implicit Method Access](https://docs.sqlalchemy.org/en/20/orm/contextual.html#implicit-method-access)
  - [Thread-Local Scope](https://docs.sqlalchemy.org/en/20/orm/contextual.html#thread-local-scope)
  - [Using Thread-Local Scope with Web Applications](https://docs.sqlalchemy.org/en/20/orm/contextual.html#using-thread-local-scope-with-web-applications)
  - [Using Custom Created Scopes](https://docs.sqlalchemy.org/en/20/orm/contextual.html#using-custom-created-scopes)
  - [Contextual Session API](https://docs.sqlalchemy.org/en/20/orm/contextual.html#contextual-session-api)
    - [scoped_session](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.scoped_session)
    - [ScopedRegistry](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.util.ScopedRegistry)
    - [ThreadLocalRegistry](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.util.ThreadLocalRegistry)
    - [QueryPropertyDescriptor](https://docs.sqlalchemy.org/en/20/orm/contextual.html#sqlalchemy.orm.QueryPropertyDescriptor)
- [Tracking queries, object and Session Changes with Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html)
  - [Execute Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#execute-events)
    - [Basic Query Interception](https://docs.sqlalchemy.org/en/20/orm/session_events.html#basic-query-interception)
    - [Adding global WHERE / ON criteria](https://docs.sqlalchemy.org/en/20/orm/session_events.html#adding-global-where-on-criteria)
    - [Re-Executing Statements](https://docs.sqlalchemy.org/en/20/orm/session_events.html#re-executing-statements)
  - [Persistence Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#persistence-events)
    - [before_flush()](https://docs.sqlalchemy.org/en/20/orm/session_events.html#before-flush)
    - [after_flush()](https://docs.sqlalchemy.org/en/20/orm/session_events.html#after-flush)
    - [after_flush_postexec()](https://docs.sqlalchemy.org/en/20/orm/session_events.html#after-flush-postexec)
    - [Mapper-level Flush Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#mapper-level-flush-events)
  - [Object Lifecycle Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#object-lifecycle-events)
    - [Transient](https://docs.sqlalchemy.org/en/20/orm/session_events.html#transient)
    - [Transient to Pending](https://docs.sqlalchemy.org/en/20/orm/session_events.html#transient-to-pending)
    - [Pending to Persistent](https://docs.sqlalchemy.org/en/20/orm/session_events.html#pending-to-persistent)
    - [Pending to Transient](https://docs.sqlalchemy.org/en/20/orm/session_events.html#pending-to-transient)
    - [Loaded as Persistent](https://docs.sqlalchemy.org/en/20/orm/session_events.html#loaded-as-persistent)
    - [Persistent to Transient](https://docs.sqlalchemy.org/en/20/orm/session_events.html#persistent-to-transient)
    - [Persistent to Deleted](https://docs.sqlalchemy.org/en/20/orm/session_events.html#persistent-to-deleted)
    - [Deleted to Detached](https://docs.sqlalchemy.org/en/20/orm/session_events.html#deleted-to-detached)
    - [Persistent to Detached](https://docs.sqlalchemy.org/en/20/orm/session_events.html#persistent-to-detached)
    - [Detached to Persistent](https://docs.sqlalchemy.org/en/20/orm/session_events.html#detached-to-persistent)
    - [Deleted to Persistent](https://docs.sqlalchemy.org/en/20/orm/session_events.html#deleted-to-persistent)
  - [Transaction Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#transaction-events)
  - [Attribute Change Events](https://docs.sqlalchemy.org/en/20/orm/session_events.html#attribute-change-events)
- [Session API](https://docs.sqlalchemy.org/en/20/orm/session_api.html)
  - [Session and sessionmaker()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#session-and-sessionmaker)
    - [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker)
    - [ORMExecuteState](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState)
    - [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
    - [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
    - [SessionTransactionOrigin](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransactionOrigin)
  - [Session Utilities](https://docs.sqlalchemy.org/en/20/orm/session_api.html#session-utilities)
    - [close_all_sessions()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.close_all_sessions)
    - [make_transient()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient)
    - [make_transient_to_detached()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient_to_detached)
    - [object_session()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.object_session)
    - [was_deleted()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.util.was_deleted)
  - [Attribute and State Management Utilities](https://docs.sqlalchemy.org/en/20/orm/session_api.html#attribute-and-state-management-utilities)
    - [object_state()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.util.object_state)
    - [del_attribute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.del_attribute)
    - [get_attribute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_attribute)
    - [get_history()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_history)
    - [init_collection()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.init_collection)
    - [flag_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_modified)
    - [flag_dirty()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.flag_dirty)
    - [instance_state()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.instance_state)
    - [is_instrumented()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.instrumentation.is_instrumented)
    - [set_attribute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.set_attribute)
    - [set_committed_value()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.set_committed_value)
    - [History](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.History)
