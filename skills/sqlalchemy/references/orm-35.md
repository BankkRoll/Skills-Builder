# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Relationships API

| Object Name | Description |
| --- | --- |
| backref(name, **kwargs) | When using therelationship.backrefparameter,
provides specific parameters to be used when the newrelationship()is generated. |
| dynamic_loader([argument], **kw) | Construct a dynamically-loading mapper property. |
| foreign(expr) | Annotate a portion of a primaryjoin expression
with a ‘foreign’ annotation. |
| relationship([argument, secondary], *, [uselist, collection_class, primaryjoin, secondaryjoin, back_populates, order_by, backref, overlaps, post_update, cascade, viewonly, init, repr, default, default_factory, compare, kw_only, hash, lazy, passive_deletes, passive_updates, active_history, enable_typechecks, foreign_keys, remote_side, join_depth, comparator_factory, single_parent, innerjoin, distinct_target_key, load_on_pending, query_class, info, omit_join, sync_backref, dataclass_metadata], **kw) | Provide a relationship between two mapped classes. |
| remote(expr) | Annotate a portion of a primaryjoin expression
with a ‘remote’ annotation. |

   function sqlalchemy.orm.relationship(*argument:_RelationshipArgumentType[Any]|None=None*, *secondary:_RelationshipSecondaryArgument|None=None*, ***, *uselist:bool|None=None*, *collection_class:Type[Collection[Any]]|Callable[[],Collection[Any]]|None=None*, *primaryjoin:_RelationshipJoinConditionArgument|None=None*, *secondaryjoin:_RelationshipJoinConditionArgument|None=None*, *back_populates:str|None=None*, *order_by:_ORMOrderByArgument=False*, *backref:ORMBackrefArgument|None=None*, *overlaps:str|None=None*, *post_update:bool=False*, *cascade:str='save-update,merge'*, *viewonly:bool=False*, *init:_NoArg|bool=_NoArg.NO_ARG*, *repr:_NoArg|bool=_NoArg.NO_ARG*, *default:_NoArg|_T=_NoArg.NO_ARG*, *default_factory:_NoArg|Callable[[],_T]=_NoArg.NO_ARG*, *compare:_NoArg|bool=_NoArg.NO_ARG*, *kw_only:_NoArg|bool=_NoArg.NO_ARG*, *hash:_NoArg|bool|None=_NoArg.NO_ARG*, *lazy:_LazyLoadArgumentType='select'*, *passive_deletes:Literal['all']|bool=False*, *passive_updates:bool=True*, *active_history:bool=False*, *enable_typechecks:bool=True*, *foreign_keys:_ORMColCollectionArgument|None=None*, *remote_side:_ORMColCollectionArgument|None=None*, *join_depth:int|None=None*, *comparator_factory:Type[RelationshipProperty.Comparator[Any]]|None=None*, *single_parent:bool=False*, *innerjoin:bool=False*, *distinct_target_key:bool|None=None*, *load_on_pending:bool=False*, *query_class:Type[Query[Any]]|None=None*, *info:_InfoType|None=None*, *omit_join:Literal[None,False]=None*, *sync_backref:bool|None=None*, *dataclass_metadata:_NoArg|Mapping[Any,Any]|None=_NoArg.NO_ARG*, ***kw:Any*) → _RelationshipDeclared[Any]

Provide a relationship between two mapped classes.

This corresponds to a parent-child or associative table relationship.
The constructed class is an instance of [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship).

See also

[Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) - tutorial introduction
to [relationship()](#sqlalchemy.orm.relationship) in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[Relationship Configuration](https://docs.sqlalchemy.org/en/20/orm/relationships.html) - narrative documentation

   Parameters:

- **argument** –
  This parameter refers to the class that is to be related.   It
  accepts several forms, including a direct reference to the target
  class itself, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) instance for the target class,
  a Python callable / lambda that will return a reference to the
  class or [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) when called, and finally a string
  name for the class, which will be resolved from the
  [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry) in use in order to locate the class, e.g.:
  ```
  class SomeClass(Base):
      # ...
      related = relationship("RelatedClass")
  ```
  The [relationship.argument](#sqlalchemy.orm.relationship.params.argument) may also be omitted from the
  [relationship()](#sqlalchemy.orm.relationship) construct entirely, and instead placed inside
  a [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation on the left side, which should
  include a Python collection type if the relationship is expected
  to be a collection, such as:
  ```
  class SomeClass(Base):
      # ...
      related_items: Mapped[List["RelatedItem"]] = relationship()
  ```
  Or for a many-to-one or one-to-one relationship:
  ```
  class SomeClass(Base):
      # ...
      related_item: Mapped["RelatedItem"] = relationship()
  ```
  See also
  [Defining Mapped Properties with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-properties) - further detail
  on relationship configuration when using Declarative.
- **secondary** –
  For a many-to-many relationship, specifies the intermediary
  table, and is typically an instance of [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  In less common circumstances, the argument may also be specified
  as an [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias) construct, or even a
  [Join](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Join) construct.
  [relationship.secondary](#sqlalchemy.orm.relationship.params.secondary) may
  also be passed as a callable function which is evaluated at
  mapper initialization time.  When using Declarative, it may also
  be a string argument noting the name of a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  that is
  present in the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData)
  collection associated with the
  parent-mapped [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table).
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
  The [relationship.secondary](#sqlalchemy.orm.relationship.params.secondary) keyword argument is
  typically applied in the case where the intermediary
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  is not otherwise expressed in any direct class mapping. If the
  “secondary” table is also explicitly mapped elsewhere (e.g. as in
  [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-pattern)), one should consider applying the
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly) flag so that this
  [relationship()](#sqlalchemy.orm.relationship)
  is not used for persistence operations which
  may conflict with those of the association object pattern.
  See also
  [Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many) - Reference example of “many
  to many”.
  [Self-Referential Many-to-Many Relationship](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#self-referential-many-to-many) - Specifics on using
  many-to-many in a self-referential case.
  [Configuring Many-to-Many Relationships](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-many-to-many) - Additional options when using
  Declarative.
  [Association Object](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-pattern) - an alternative to
  [relationship.secondary](#sqlalchemy.orm.relationship.params.secondary)
  when composing association
  table relationships, allowing additional attributes to be
  specified on the association table.
  [Composite “Secondary” Joins](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#composite-secondary-join) - a lesser-used pattern which
  in some cases can enable complex [relationship()](#sqlalchemy.orm.relationship) SQL
  conditions to be used.
- **active_history=False** – When `True`, indicates that the “previous” value for a
  many-to-one reference should be loaded when replaced, if
  not already loaded. Normally, history tracking logic for
  simple many-to-ones only needs to be aware of the “new”
  value in order to perform a flush. This flag is available
  for applications that make use of
  [get_history()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.attributes.get_history) which also need to know
  the “previous” value of the attribute.
- **backref** –
  A reference to a string relationship name, or a [backref()](#sqlalchemy.orm.backref)
  construct, which will be used to automatically generate a new
  [relationship()](#sqlalchemy.orm.relationship) on the related class, which then refers to this
  one using a bi-directional [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates)
  configuration.
  In modern Python, explicit use of [relationship()](#sqlalchemy.orm.relationship)
  with [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates) should be preferred,
  as it is more robust in terms of mapper configuration as well as
  more conceptually straightforward.  It also integrates with
  new [PEP 484](https://peps.python.org/pep-0484/) typing features introduced in SQLAlchemy 2.0 which
  is not possible with dynamically generated attributes.
  See also
  [Using the legacy ‘backref’ relationship parameter](https://docs.sqlalchemy.org/en/20/orm/backref.html#relationships-backref) - notes on using
  [relationship.backref](#sqlalchemy.orm.relationship.params.backref)
  [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial),
  presents an overview of bi-directional relationship configuration
  and behaviors using [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates)
  [backref()](#sqlalchemy.orm.backref) - allows control over [relationship()](#sqlalchemy.orm.relationship)
  configuration when using [relationship.backref](#sqlalchemy.orm.relationship.params.backref).
- **back_populates** –
  Indicates the name of a [relationship()](#sqlalchemy.orm.relationship) on the related
  class that will be synchronized with this one.   It is usually
  expected that the [relationship()](#sqlalchemy.orm.relationship) on the related class
  also refer to this one.  This allows objects on both sides of
  each [relationship()](#sqlalchemy.orm.relationship) to synchronize in-Python state
  changes and also provides directives to the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work)
  flush process how changes along these relationships should
  be persisted.
  See also
  [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects) - in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial),
  presents an overview of bi-directional relationship configuration
  and behaviors.
  [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns) - includes many examples of
  [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates).
  [relationship.backref](#sqlalchemy.orm.relationship.params.backref) - legacy form which allows
  more succinct configuration, but does not support explicit typing
- **overlaps** –
  A string name or comma-delimited set of names of other relationships
  on either this mapper, a descendant mapper, or a target mapper with
  which this relationship may write to the same foreign keys upon
  persistence.   The only effect this has is to eliminate the
  warning that this relationship will conflict with another upon
  persistence.   This is used for such relationships that are truly
  capable of conflicting with each other on write, but the application
  will ensure that no such conflicts occur.
  Added in version 1.4.
  See also
  [relationship X will copy column Q to column P, which conflicts with relationship(s): ‘Y’](https://docs.sqlalchemy.org/en/20/errors.html#error-qzyx) - usage example
- **cascade** –
  A comma-separated list of cascade rules which determines how
  Session operations should be “cascaded” from parent to child.
  This defaults to `False`, which means the default cascade
  should be used - this default cascade is `"save-update, merge"`.
  The available cascades are `save-update`, `merge`,
  `expunge`, `delete`, `delete-orphan`, and `refresh-expire`.
  An additional option, `all` indicates shorthand for
  `"save-update, merge, refresh-expire,
  expunge, delete"`, and is often used as in `"all, delete-orphan"`
  to indicate that related objects should follow along with the
  parent object in all cases, and be deleted when de-associated.
  See also
  [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) - Full detail on each of the available
  cascade options.
- **cascade_backrefs=False** –
  Legacy; this flag is always False.
  Changed in version 2.0: “cascade_backrefs” functionality has been
  removed.
- **collection_class** –
  A class or callable that returns a new list-holding object. will
  be used in place of a plain list for storing elements.
  See also
  [Customizing Collection Access](https://docs.sqlalchemy.org/en/20/orm/collection_api.html#custom-collections) - Introductory documentation and
  examples.
- **comparator_factory** –
  A class which extends `Comparator`
  which provides custom SQL clause generation for comparison
  operations.
  See also
  [PropComparator](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.PropComparator) - some detail on redefining comparators
  at this level.
  [Operator Customization](https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#custom-comparators) - Brief intro to this feature.
- **distinct_target_key=None** –
  Indicate if a “subquery” eager load should apply the DISTINCT
  keyword to the innermost SELECT statement.  When left as `None`,
  the DISTINCT keyword will be applied in those cases when the target
  columns do not comprise the full primary key of the target table.
  When set to `True`, the DISTINCT keyword is applied to the
  innermost SELECT unconditionally.
  It may be desirable to set this flag to False when the DISTINCT is
  reducing performance of the innermost subquery beyond that of what
  duplicate innermost rows may be causing.
  See also
  [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html) - includes an introduction to subquery
  eager loading.
- **doc** – Docstring which will be applied to the resulting descriptor.
- **foreign_keys** –
  A list of columns which are to be used as “foreign key”
  columns, or columns which refer to the value in a remote
  column, within the context of this [relationship()](#sqlalchemy.orm.relationship)
  object’s [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin) condition.
  That is, if the [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin)
  condition of this [relationship()](#sqlalchemy.orm.relationship) is `a.id ==
  b.a_id`, and the values in `b.a_id` are required to be
  present in `a.id`, then the “foreign key” column of this
  [relationship()](#sqlalchemy.orm.relationship) is `b.a_id`.
  In normal cases, the [relationship.foreign_keys](#sqlalchemy.orm.relationship.params.foreign_keys)
  parameter is **not required.** [relationship()](#sqlalchemy.orm.relationship) will
  automatically determine which columns in the
  [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin) condition are to be
  considered “foreign key” columns based on those
  [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column) objects that specify
  [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey),
  or are otherwise listed as referencing columns in a
  [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint) construct.
  [relationship.foreign_keys](#sqlalchemy.orm.relationship.params.foreign_keys) is only needed when:
  > 1. There is more than one way to construct a join from the local
  >   table to the remote table, as there are multiple foreign key
  >   references present.  Setting `foreign_keys` will limit the
  >   [relationship()](#sqlalchemy.orm.relationship)
  >   to consider just those columns specified
  >   here as “foreign”.
  > 2. The [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) being mapped does not actually have
  >   [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) or
  >   [ForeignKeyConstraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKeyConstraint)
  >   constructs present, often because the table
  >   was reflected from a database that does not support foreign key
  >   reflection (MySQL MyISAM).
  > 3. The [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin)
  >   argument is used to
  >   construct a non-standard join condition, which makes use of
  >   columns or expressions that do not normally refer to their
  >   “parent” column, such as a join condition expressed by a
  >   complex comparison using a SQL function.
  The [relationship()](#sqlalchemy.orm.relationship) construct will raise informative
  error messages that suggest the use of the
  [relationship.foreign_keys](#sqlalchemy.orm.relationship.params.foreign_keys) parameter when
  presented with an ambiguous condition.   In typical cases,
  if [relationship()](#sqlalchemy.orm.relationship) doesn’t raise any exceptions, the
  [relationship.foreign_keys](#sqlalchemy.orm.relationship.params.foreign_keys) parameter is usually
  not needed.
  [relationship.foreign_keys](#sqlalchemy.orm.relationship.params.foreign_keys) may also be passed as a
  callable function which is evaluated at mapper initialization time,
  and may be passed as a Python-evaluable string when using
  Declarative.
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
  See also
  [Handling Multiple Join Paths](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-foreign-keys)
  [Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-foreign)
  [foreign()](#sqlalchemy.orm.foreign) - allows direct annotation of the “foreign”
  columns within a [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin)
  condition.
- **info** – Optional data dictionary which will be populated into the
  [MapperProperty.info](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.MapperProperty.info) attribute of this object.
- **innerjoin=False** –
  When `True`, joined eager loads will use an inner join to join
  against related tables instead of an outer join.  The purpose
  of this option is generally one of performance, as inner joins
  generally perform better than outer joins.
  This flag can be set to `True` when the relationship references an
  object via many-to-one using local foreign keys that are not
  nullable, or when the reference is one-to-one or a collection that
  is guaranteed to have one or at least one entry.
  The option supports the same “nested” and “unnested” options as
  that of [joinedload.innerjoin](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload.params.innerjoin).  See that flag
  for details on nested / unnested behaviors.
  See also
  [joinedload.innerjoin](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload.params.innerjoin) - the option as specified by
  loader option, including detail on nesting behavior.
  [What Kind of Loading to Use ?](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#what-kind-of-loading) - Discussion of some details of
  various loader options.
- **join_depth** –
  When non-`None`, an integer value indicating how many levels
  deep “eager” loaders should join on a self-referring or cyclical
  relationship.  The number counts how many times the same Mapper
  shall be present in the loading condition along a particular join
  branch.  When left at its default of `None`, eager loaders
  will stop chaining when they encounter a the same target mapper
  which is already higher up in the chain.  This option applies
  both to joined- and subquery- eager loaders.
  See also
  [Configuring Self-Referential Eager Loading](https://docs.sqlalchemy.org/en/20/orm/self_referential.html#self-referential-eager-loading) - Introductory documentation
  and examples.
- **lazy='select'** –
  specifies
  How the related items should be loaded.  Default value is
  `select`.  Values include:
  - `select` - items should be loaded lazily when the property is
    first accessed, using a separate SELECT statement, or identity map
    fetch for simple many-to-one references.
  - `immediate` - items should be loaded as the parents are loaded,
    using a separate SELECT statement, or identity map fetch for
    simple many-to-one references.
  - `joined` - items should be loaded “eagerly” in the same query as
    that of the parent, using a JOIN or LEFT OUTER JOIN.  Whether
    the join is “outer” or not is determined by the
    [relationship.innerjoin](#sqlalchemy.orm.relationship.params.innerjoin) parameter.
  - `subquery` - items should be loaded “eagerly” as the parents are
    loaded, using one additional SQL statement, which issues a JOIN to
    a subquery of the original statement, for each collection
    requested.
  - `selectin` - items should be loaded “eagerly” as the parents
    are loaded, using one or more additional SQL statements, which
    issues a JOIN to the immediate parent object, specifying primary
    key identifiers using an IN clause.
  - `noload` - no loading should occur at any time.  The related
    collection will remain empty.   The `noload` strategy is not
    recommended for general use.  For a general use “never load”
    approach, see [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship)
  - `raise` - lazy loading is disallowed; accessing
    the attribute, if its value were not already loaded via eager
    loading, will raise an [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError).
    This strategy can be used when objects are to be detached from
    their attached [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) after they are loaded.
  - `raise_on_sql` - lazy loading that emits SQL is disallowed;
    accessing the attribute, if its value were not already loaded via
    eager loading, will raise an
    [InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError), **if the lazy load
    needs to emit SQL**.  If the lazy load can pull the related value
    from the identity map or determine that it should be None, the
    value is loaded.  This strategy can be used when objects will
    remain associated with the attached [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), however
    additional SELECT statements should be blocked.
  - `write_only` - the attribute will be configured with a special
    “virtual collection” that may receive
    [WriteOnlyCollection.add()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.add) and
    [WriteOnlyCollection.remove()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.remove) commands to add or remove
    individual objects, but will not under any circumstances load or
    iterate the full set of objects from the database directly. Instead,
    methods such as [WriteOnlyCollection.select()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.select),
    [WriteOnlyCollection.insert()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.insert),
    [WriteOnlyCollection.update()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.update) and
    [WriteOnlyCollection.delete()](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyCollection.delete) are provided which generate SQL
    constructs that may be used to load and modify rows in bulk. Used for
    large collections that are never appropriate to load at once into
    memory.
    The `write_only` loader style is configured automatically when
    the [WriteOnlyMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.WriteOnlyMapped) annotation is provided on the
    left hand side within a Declarative mapping.  See the section
    [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship) for examples.
    Added in version 2.0.
    See also
    [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
  - `dynamic` - the attribute will return a pre-configured
    [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object for all read
    operations, onto which further filtering operations can be
    applied before iterating the results.
    The `dynamic` loader style is configured automatically when
    the [DynamicMapped](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#sqlalchemy.orm.DynamicMapped) annotation is provided on the
    left hand side within a Declarative mapping.  See the section
    [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship) for examples.
    Legacy Feature
    The “dynamic” lazy loader strategy is the legacy form of
    what is now the “write_only” strategy described in the section
    [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship).
    See also
    [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
    [Write Only Relationships](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#write-only-relationship) - more generally useful approach
    for large collections that should not fully load into memory
  - True - a synonym for ‘select’
  - False - a synonym for ‘joined’
  - None - a synonym for ‘noload’
  See also
  [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#orm-queryguide-relationship-loaders) - Full documentation on
  relationship loader configuration in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).
- **load_on_pending=False** –
  Indicates loading behavior for transient or pending parent objects.
  When set to `True`, causes the lazy-loader to
  issue a query for a parent object that is not persistent, meaning it
  has never been flushed.  This may take effect for a pending object
  when autoflush is disabled, or for a transient object that has been
  “attached” to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) but is not part of its pending
  collection.
  The [relationship.load_on_pending](#sqlalchemy.orm.relationship.params.load_on_pending)
  flag does not improve
  behavior when the ORM is used normally - object references should be
  constructed at the object level, not at the foreign key level, so
  that they are present in an ordinary way before a flush proceeds.
  This flag is not not intended for general use.
  See also
  [Session.enable_relationship_loading()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.enable_relationship_loading) - this method
  establishes “load on pending” behavior for the whole object, and
  also allows loading on objects that remain transient or
  detached.
- **order_by** –
  Indicates the ordering that should be applied when loading these
  items.  [relationship.order_by](#sqlalchemy.orm.relationship.params.order_by)
  is expected to refer to
  one of the [Column](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)
  objects to which the target class is
  mapped, or the attribute itself bound to the target class which
  refers to the column.
  [relationship.order_by](#sqlalchemy.orm.relationship.params.order_by)
  may also be passed as a callable
  function which is evaluated at mapper initialization time, and may
  be passed as a Python-evaluable string when using Declarative.
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
- **passive_deletes=False** –
  Indicates loading behavior during delete operations.
  A value of True indicates that unloaded child items should not
  be loaded during a delete operation on the parent.  Normally,
  when a parent item is deleted, all child items are loaded so
  that they can either be marked as deleted, or have their
  foreign key to the parent set to NULL.  Marking this flag as
  True usually implies an ON DELETE <CASCADE|SET NULL> rule is in
  place which will handle updating/deleting child rows on the
  database side.
  Additionally, setting the flag to the string value ‘all’ will
  disable the “nulling out” of the child foreign keys, when the parent
  object is deleted and there is no delete or delete-orphan cascade
  enabled.  This is typically used when a triggering or error raise
  scenario is in place on the database side.  Note that the foreign
  key attributes on in-session child objects will not be changed after
  a flush occurs so this is a very special use-case setting.
  Additionally, the “nulling out” will still occur if the child
  object is de-associated with the parent.
  See also
  [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes) - Introductory documentation
  and examples.
- **passive_updates=True** –
  Indicates the persistence behavior to take when a referenced
  primary key value changes in place, indicating that the referencing
  foreign key columns will also need their value changed.
  When True, it is assumed that `ON UPDATE CASCADE` is configured on
  the foreign key in the database, and that the database will
  handle propagation of an UPDATE from a source column to
  dependent rows.  When False, the SQLAlchemy
  [relationship()](#sqlalchemy.orm.relationship)
  construct will attempt to emit its own UPDATE statements to
  modify related targets.  However note that SQLAlchemy **cannot**
  emit an UPDATE for more than one level of cascade.  Also,
  setting this flag to False is not compatible in the case where
  the database is in fact enforcing referential integrity, unless
  those constraints are explicitly “deferred”, if the target backend
  supports it.
  It is highly advised that an application which is employing
  mutable primary keys keeps `passive_updates` set to True,
  and instead uses the referential integrity features of the database
  itself in order to handle the change efficiently and fully.
  See also
  [Mutable Primary Keys / Update Cascades](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#passive-updates) - Introductory documentation and
  examples.
  [mapper.passive_updates](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.mapper.params.passive_updates) - a similar flag which
  takes effect for joined-table inheritance mappings.
- **post_update** –
  This indicates that the relationship should be handled by a
  second UPDATE statement after an INSERT or before a
  DELETE. This flag is used to handle saving bi-directional
  dependencies between two individual rows (i.e. each row
  references the other), where it would otherwise be impossible to
  INSERT or DELETE both rows fully since one row exists before the
  other. Use this flag when a particular mapping arrangement will
  incur two rows that are dependent on each other, such as a table
  that has a one-to-many relationship to a set of child rows, and
  also has a column that references a single child row within that
  list (i.e. both tables contain a foreign key to each other). If
  a flush operation returns an error that a “cyclical
  dependency” was detected, this is a cue that you might want to
  use [relationship.post_update](#sqlalchemy.orm.relationship.params.post_update) to “break” the cycle.
  See also
  [Rows that point to themselves / Mutually Dependent Rows](https://docs.sqlalchemy.org/en/20/orm/relationship_persistence.html#post-update) - Introductory documentation and examples.
- **primaryjoin** –
  A SQL expression that will be used as the primary
  join of the child object against the parent object, or in a
  many-to-many relationship the join of the parent object to the
  association table. By default, this value is computed based on the
  foreign key relationships of the parent and child tables (or
  association table).
  [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin) may also be passed as a
  callable function which is evaluated at mapper initialization time,
  and may be passed as a Python-evaluable string when using
  Declarative.
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
  See also
  [Specifying Alternate Join Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-primaryjoin)
- **remote_side** –
  Used for self-referential relationships, indicates the column or
  list of columns that form the “remote side” of the relationship.
  [relationship.remote_side](#sqlalchemy.orm.relationship.params.remote_side) may also be passed as a
  callable function which is evaluated at mapper initialization time,
  and may be passed as a Python-evaluable string when using
  Declarative.
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
  See also
  [Adjacency List Relationships](https://docs.sqlalchemy.org/en/20/orm/self_referential.html#self-referential) - in-depth explanation of how
  [relationship.remote_side](#sqlalchemy.orm.relationship.params.remote_side)
  is used to configure self-referential relationships.
  [remote()](#sqlalchemy.orm.remote) - an annotation function that accomplishes the
  same purpose as [relationship.remote_side](#sqlalchemy.orm.relationship.params.remote_side),
  typically
  when a custom [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin) condition
  is used.
- **query_class** –
  A [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  subclass that will be used internally by the
  `AppenderQuery` returned by a “dynamic” relationship, that
  is, a relationship that specifies `lazy="dynamic"` or was
  otherwise constructed using the [dynamic_loader()](#sqlalchemy.orm.dynamic_loader)
  function.
  See also
  [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship) - Introduction to “dynamic”
  relationship loaders.
- **secondaryjoin** –
  A SQL expression that will be used as the join of
  an association table to the child object. By default, this value is
  computed based on the foreign key relationships of the association
  and child tables.
  [relationship.secondaryjoin](#sqlalchemy.orm.relationship.params.secondaryjoin) may also be passed as a
  callable function which is evaluated at mapper initialization time,
  and may be passed as a Python-evaluable string when using
  Declarative.
  Warning
  When passed as a Python-evaluable string, the
  argument is interpreted using Python’s `eval()` function.
  **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
  See [Evaluation of relationship arguments](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/relationships.html#declarative-relationship-eval) for details on
  declarative evaluation of [relationship()](#sqlalchemy.orm.relationship) arguments.
  See also
  [Specifying Alternate Join Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-primaryjoin)
- **single_parent** –
  When True, installs a validator which will prevent objects
  from being associated with more than one parent at a time.
  This is used for many-to-one or many-to-many relationships that
  should be treated either as one-to-one or one-to-many.  Its usage
  is optional, except for [relationship()](#sqlalchemy.orm.relationship) constructs which
  are many-to-one or many-to-many and also
  specify the `delete-orphan` cascade option.  The
  [relationship()](#sqlalchemy.orm.relationship) construct itself will raise an error
  instructing when this option is required.
  See also
  [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) - includes detail on when the
  [relationship.single_parent](#sqlalchemy.orm.relationship.params.single_parent)
  flag may be appropriate.
- **uselist** –
  A boolean that indicates if this property should be loaded as a
  list or a scalar. In most cases, this value is determined
  automatically by [relationship()](#sqlalchemy.orm.relationship) at mapper configuration
  time.  When using explicit [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotations,
  [relationship.uselist](#sqlalchemy.orm.relationship.params.uselist) may be derived from the
  whether or not the annotation within [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) contains
  a collection class.
  Otherwise, [relationship.uselist](#sqlalchemy.orm.relationship.params.uselist) may be derived from
  the type and direction
  of the relationship - one to many forms a list, many to one
  forms a scalar, many to many is a list. If a scalar is desired
  where normally a list would be present, such as a bi-directional
  one-to-one relationship, use an appropriate [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped)
  annotation or set [relationship.uselist](#sqlalchemy.orm.relationship.params.uselist) to False.
  The [relationship.uselist](#sqlalchemy.orm.relationship.params.uselist)
  flag is also available on an
  existing [relationship()](#sqlalchemy.orm.relationship)
  construct as a read-only attribute,
  which can be used to determine if this [relationship()](#sqlalchemy.orm.relationship)
  deals
  with collections or scalar attributes:
  ```
  >>> User.addresses.property.uselist
  True
  ```
  See also
  [One To One](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-one-to-one) - Introduction to the “one to
  one” relationship pattern, which is typically when an alternate
  setting for [relationship.uselist](#sqlalchemy.orm.relationship.params.uselist) is involved.
- **viewonly=False** –
  When set to `True`, the relationship is used only for loading
  objects, and not for any persistence operation.  A
  [relationship()](#sqlalchemy.orm.relationship) which specifies
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly) can work
  with a wider range of SQL operations within the
  [relationship.primaryjoin](#sqlalchemy.orm.relationship.params.primaryjoin) condition, including
  operations that feature the use of a variety of comparison operators
  as well as SQL functions such as [cast()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.cast).  The
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly)
  flag is also of general use when defining any kind of
  [relationship()](#sqlalchemy.orm.relationship) that doesn’t represent
  the full set of related objects, to prevent modifications of the
  collection from resulting in persistence operations.
  See also
  [Notes on using the viewonly relationship parameter](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-viewonly-notes) - more details on best practices
  when using [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly).
- **sync_backref** –
  A boolean that enables the events used to synchronize the in-Python
  attributes when this relationship is target of either
  [relationship.backref](#sqlalchemy.orm.relationship.params.backref) or
  [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates).
  Defaults to `None`, which indicates that an automatic value should
  be selected based on the value of the
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly) flag.  When left at its
  default, changes in state will be back-populated only if neither
  sides of a relationship is viewonly.
  Added in version 1.3.17.
  Changed in version 1.4: - A relationship that specifies
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly) automatically implies
  that [relationship.sync_backref](#sqlalchemy.orm.relationship.params.sync_backref) is `False`.
  See also
  [relationship.viewonly](#sqlalchemy.orm.relationship.params.viewonly)
- **omit_join** –
  Allows manual control over the “selectin” automatic join
  optimization.  Set to `False` to disable the “omit join” feature
  added in SQLAlchemy 1.3; or leave as `None` to leave automatic
  optimization in place.
  Note
  This flag may only be set to `False`.   It is not
  necessary to set it to `True` as the “omit_join” optimization is
  automatically detected; if it is not detected, then the
  optimization is not supported.
  Changed in version 1.3.11: setting `omit_join` to True will now
  emit a warning as this was not the intended use of this flag.
  Added in version 1.3.
- **init** – Specific to [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  specifies if the mapped attribute should be part of the `__init__()`
  method as generated by the dataclass process.
- **repr** – Specific to [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  specifies if the mapped attribute should be part of the `__repr__()`
  method as generated by the dataclass process.
- **default_factory** – Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses),
  specifies a default-value generation function that will take place
  as part of the `__init__()`
  method as generated by the dataclass process.
- **compare** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), indicates if this field
  should be included in comparison operations when generating the
  `__eq__()` and `__ne__()` methods for the mapped class.
  Added in version 2.0.0b4.
- **kw_only** – Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), indicates if this field
  should be marked as keyword-only when generating the `__init__()`.
- **hash** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), controls if this field
  is included when generating the `__hash__()` method for the mapped
  class.
  Added in version 2.0.36.
- **dataclass_metadata** –
  Specific to
  [Declarative Dataclass Mapping](https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses), supplies metadata
  to be attached to the generated dataclass field.
  Added in version 2.0.42.

      function sqlalchemy.orm.backref(*name:str*, ***kwargs:Any*) → ORMBackrefArgument

When using the [relationship.backref](#sqlalchemy.orm.relationship.params.backref) parameter,
provides specific parameters to be used when the new
[relationship()](#sqlalchemy.orm.relationship) is generated.

E.g.:

```
"items": relationship(SomeItem, backref=backref("parent", lazy="subquery"))
```

The [relationship.backref](#sqlalchemy.orm.relationship.params.backref) parameter is generally
considered to be legacy; for modern applications, using
explicit [relationship()](#sqlalchemy.orm.relationship) constructs linked together using
the [relationship.back_populates](#sqlalchemy.orm.relationship.params.back_populates) parameter should be
preferred.

See also

[Using the legacy ‘backref’ relationship parameter](https://docs.sqlalchemy.org/en/20/orm/backref.html#relationships-backref) - background on backrefs

     function sqlalchemy.orm.dynamic_loader(*argument:_RelationshipArgumentType[Any]|None=None*, ***kw:Any*) → [RelationshipProperty](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.RelationshipProperty)[Any]

Construct a dynamically-loading mapper property.

This is essentially the same as
using the `lazy='dynamic'` argument with [relationship()](#sqlalchemy.orm.relationship):

```
dynamic_loader(SomeClass)

# is the same as

relationship(SomeClass, lazy="dynamic")
```

See the section [Dynamic Relationship Loaders](https://docs.sqlalchemy.org/en/20/orm/large_collections.html#dynamic-relationship) for more details
on dynamic loading.

    function sqlalchemy.orm.foreign(*expr:_CEA*) → _CEA

Annotate a portion of a primaryjoin expression
with a ‘foreign’ annotation.

See the section [Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-foreign) for a
description of use.

See also

[Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-foreign)

[remote()](#sqlalchemy.orm.remote)

     function sqlalchemy.orm.remote(*expr:_CEA*) → _CEA

Annotate a portion of a primaryjoin expression
with a ‘remote’ annotation.

See the section [Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-foreign) for a
description of use.

See also

[Creating Custom Foreign Conditions](https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#relationship-custom-foreign)

[foreign()](#sqlalchemy.orm.foreign)
