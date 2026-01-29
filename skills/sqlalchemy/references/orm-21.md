# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Working with Large Collections

The default behavior of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) is to fully load
the contents of collections into memory, based on a configured
[loader strategy](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#orm-queryguide-relationship-loaders) that controls
when and how these contents are loaded from the database.  Related collections
may be loaded into memory not just when they are accessed, or eagerly loaded,
but in most cases will require population when the collection
itself is mutated, as well as in cases where the owning object is to be
deleted by the unit of work system.

When a related collection is potentially very large, it may not be feasible
for such a collection to be populated into memory under any circumstances,
as the operation may be overly consuming of time, network and memory
resources.

This section includes API features intended to allow [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
to be used with large collections while maintaining adequate performance.

## Write Only Relationships

The **write only** loader strategy is the primary means of configuring a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) that will remain writeable, but will not load
its contents into memory.  A write-only ORM configuration in modern
type-annotated Declarative form is illustrated below:

```
>>> from decimal import Decimal
>>> from datetime import datetime

>>> from sqlalchemy import ForeignKey
>>> from sqlalchemy import func
>>> from sqlalchemy.orm import DeclarativeBase
>>> from sqlalchemy.orm import Mapped
>>> from sqlalchemy.orm import mapped_column
>>> from sqlalchemy.orm import relationship
>>> from sqlalchemy.orm import Session
>>> from sqlalchemy.orm import WriteOnlyMapped

>>> class Base(DeclarativeBase):
...     pass

>>> class Account(Base):
...     __tablename__ = "account"
...     id: Mapped[int] = mapped_column(primary_key=True)
...     identifier: Mapped[str]
...
...     account_transactions: WriteOnlyMapped["AccountTransaction"] = relationship(
...         cascade="all, delete-orphan",
...         passive_deletes=True,
...         order_by="AccountTransaction.timestamp",
...     )
...
...     def __repr__(self):
...         return f"Account(identifier={self.identifier!r})"

>>> class AccountTransaction(Base):
...     __tablename__ = "account_transaction"
...     id: Mapped[int] = mapped_column(primary_key=True)
...     account_id: Mapped[int] = mapped_column(
...         ForeignKey("account.id", ondelete="cascade")
...     )
...     description: Mapped[str]
...     amount: Mapped[Decimal]
...     timestamp: Mapped[datetime] = mapped_column(default=func.now())
...
...     def __repr__(self):
...         return (
...             f"AccountTransaction(amount={self.amount:.2f}, "
...             f"timestamp={self.timestamp.isoformat()!r})"
...         )
...
...     __mapper_args__ = {"eager_defaults": True}
```

Above, the `account_transactions` relationship is configured not using the
ordinary [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation, but instead
using the [WriteOnlyMapped](#sqlalchemy.orm.WriteOnlyMapped) type annotation, which at runtime will
assign the [loader strategy](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#orm-queryguide-relationship-loaders) of
`lazy="write_only"` to the target [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
The [WriteOnlyMapped](#sqlalchemy.orm.WriteOnlyMapped) annotation is an
alternative form of the [Mapped](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Mapped) annotation which indicate the use
of the [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) collection type on instances of the
object.

The above [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) configuration also includes several
elements that are specific to what action to take when `Account` objects
are deleted, as well as when `AccountTransaction` objects are removed from the
`account_transactions` collection.  These elements are:

- `passive_deletes=True` - allows the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) to forego having
  to load the collection when `Account` is deleted; see
  [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes).
- `ondelete="cascade"` configured on the [ForeignKey](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey) constraint.
  This is also detailed at [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes).
- `cascade="all, delete-orphan"` - instructs the [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) to
  delete `AccountTransaction` objects when they are removed from the
  collection.  See [delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-orphan) in the [Cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades)
  document.

Added in version 2.0: Added “Write only” relationship loaders.

### Creating and Persisting New Write Only Collections

The write-only collection allows for direct assignment of the collection
as a whole **only** for [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) or [pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending) objects.
With our above mapping, this indicates we can create a new `Account`
object with a sequence of `AccountTransaction` objects to be added
to a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).   Any Python iterable may be used as the
source of objects to start, where below we use a Python `list`:

```
>>> new_account = Account(
...     identifier="account_01",
...     account_transactions=[
...         AccountTransaction(description="initial deposit", amount=Decimal("500.00")),
...         AccountTransaction(description="transfer", amount=Decimal("1000.00")),
...         AccountTransaction(description="withdrawal", amount=Decimal("-29.50")),
...     ],
... )

>>> with Session(engine) as session:
...     session.add(new_account)
...     session.commit()
BEGIN (implicit)
INSERT INTO account (identifier) VALUES (?)
[...] ('account_01',)
INSERT INTO account_transaction (account_id, description, amount, timestamp)
VALUES (?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, timestamp
[... (insertmanyvalues) 1/3 (ordered; batch not supported)] (1, 'initial deposit', 500.0)
INSERT INTO account_transaction (account_id, description, amount, timestamp)
VALUES (?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, timestamp
[insertmanyvalues 2/3 (ordered; batch not supported)] (1, 'transfer', 1000.0)
INSERT INTO account_transaction (account_id, description, amount, timestamp)
VALUES (?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, timestamp
[insertmanyvalues 3/3 (ordered; batch not supported)] (1, 'withdrawal', -29.5)
COMMIT
```

Once an object is database-persisted (i.e. in the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) or
[detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) state), the collection has the ability to be extended with new
items as well as the ability for individual items to be removed. However, the
collection may **no longer be re-assigned with a full replacement collection**,
as such an operation requires that the previous collection is fully
loaded into memory in order to reconcile the old entries with the new ones:

```
>>> new_account.account_transactions = [
...     AccountTransaction(description="some transaction", amount=Decimal("10.00"))
... ]
Traceback (most recent call last):
...
sqlalchemy.exc.InvalidRequestError: Collection "Account.account_transactions" does not
support implicit iteration; collection replacement operations can't be used
```

### Adding New Items to an Existing Collection

For write-only collections of persistent objects,
modifications to the collection using [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) processes may proceed
only by using the [WriteOnlyCollection.add()](#sqlalchemy.orm.WriteOnlyCollection.add),
[WriteOnlyCollection.add_all()](#sqlalchemy.orm.WriteOnlyCollection.add_all) and [WriteOnlyCollection.remove()](#sqlalchemy.orm.WriteOnlyCollection.remove)
methods:

```
>>> from sqlalchemy import select
>>> session = Session(engine, expire_on_commit=False)
>>> existing_account = session.scalar(select(Account).filter_by(identifier="account_01"))
BEGIN (implicit)
SELECT account.id, account.identifier
FROM account
WHERE account.identifier = ?
[...] ('account_01',)
>>> existing_account.account_transactions.add_all(
...     [
...         AccountTransaction(description="paycheck", amount=Decimal("2000.00")),
...         AccountTransaction(description="rent", amount=Decimal("-800.00")),
...     ]
... )
>>> session.commit()
INSERT INTO account_transaction (account_id, description, amount, timestamp)
VALUES (?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, timestamp
[... (insertmanyvalues) 1/2 (ordered; batch not supported)] (1, 'paycheck', 2000.0)
INSERT INTO account_transaction (account_id, description, amount, timestamp)
VALUES (?, ?, ?, CURRENT_TIMESTAMP) RETURNING id, timestamp
[insertmanyvalues 2/2 (ordered; batch not supported)] (1, 'rent', -800.0)
COMMIT
```

The items added above are held in a pending queue within the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) until the next flush, at which point they are INSERTed
into the database, assuming the added objects were previously [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient).

### Querying Items

The [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) does not at any point store a reference
to the current contents of the collection, nor does it have any behavior where
it would directly emit a SELECT to the database in order to load them; the
overriding assumption is that the collection may contain many thousands or
millions of rows, and should never be fully loaded into memory as a side effect
of any other operation.

Instead, the [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) includes SQL-generating helpers
such as [WriteOnlyCollection.select()](#sqlalchemy.orm.WriteOnlyCollection.select), which will generate
a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct pre-configured with the correct WHERE / FROM
criteria for the current parent row, which can then be further modified in
order to SELECT any range of rows desired, as well as invoked using features
like [server side cursors](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-yield-per) for processes that
wish to iterate through the full collection in a memory-efficient manner.

The statement generated is illustrated below. Note it also includes ORDER BY
criteria, indicated in the example mapping by the
[relationship.order_by](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.order_by) parameter of [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship);
this criteria would be omitted if the parameter were not configured:

```
>>> print(existing_account.account_transactions.select())
SELECT account_transaction.id, account_transaction.account_id, account_transaction.description,
account_transaction.amount, account_transaction.timestamp
FROM account_transaction
WHERE :param_1 = account_transaction.account_id ORDER BY account_transaction.timestamp
```

We may use this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct along with the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
in order to query for `AccountTransaction` objects, most easily using the
[Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars) method that will return a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) that
yields ORM objects directly. It’s typical, though not required, that the
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) would be modified further to limit the records returned; in
the example below, additional WHERE criteria to load only “debit” account
transactions is added, along with “LIMIT 10” to retrieve only the first ten
rows:

```
>>> account_transactions = session.scalars(
...     existing_account.account_transactions.select()
...     .where(AccountTransaction.amount < 0)
...     .limit(10)
... ).all()
BEGIN (implicit)
SELECT account_transaction.id, account_transaction.account_id, account_transaction.description,
account_transaction.amount, account_transaction.timestamp
FROM account_transaction
WHERE ? = account_transaction.account_id AND account_transaction.amount < ?
ORDER BY account_transaction.timestamp  LIMIT ? OFFSET ?
[...] (1, 0, 10, 0)
>>> print(account_transactions)
[AccountTransaction(amount=-29.50, timestamp='...'), AccountTransaction(amount=-800.00, timestamp='...')]
```

### Removing Items

Individual items that are loaded in the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent)
state against the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) may be marked for removal
from the collection using the [WriteOnlyCollection.remove()](#sqlalchemy.orm.WriteOnlyCollection.remove) method.
The flush process will implicitly consider the object to be already part
of the collection when the operation proceeds.   The example below
illustrates removal of an individual `AccountTransaction` item,
which per [cascade](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) settings results in a
DELETE of that row:

```
>>> existing_transaction = account_transactions[0]
>>> existing_account.account_transactions.remove(existing_transaction)
>>> session.commit()
DELETE FROM account_transaction WHERE account_transaction.id = ?
[...] (3,)
COMMIT
```

As with any ORM-mapped collection, object removal may proceed either to
de-associate the object from the collection while leaving the object present in
the database, or may issue a DELETE for its row, based on the
[delete-orphan](https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-orphan) configuration of the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

Collection removal without deletion involves setting foreign key columns to
NULL for a [one-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns-o2m) relationship, or
deleting the corresponding association row for a
[many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many) relationship.

### Bulk INSERT of New Items

The [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) can generate DML constructs such as
[Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) objects, which may be used in an ORM context to
produce bulk insert behavior.  See the section
[ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) for an overview of ORM bulk inserts.

#### One to Many Collections

For a **regular one to many collection only**, the [WriteOnlyCollection.insert()](#sqlalchemy.orm.WriteOnlyCollection.insert)
method will produce an [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) construct which is pre-established with
VALUES criteria corresponding to the parent object.  As this VALUES criteria
is entirely against the related table, the statement can be used to
INSERT new rows that will at the same time become new records in the
related collection:

```
>>> session.execute(
...     existing_account.account_transactions.insert(),
...     [
...         {"description": "transaction 1", "amount": Decimal("47.50")},
...         {"description": "transaction 2", "amount": Decimal("-501.25")},
...         {"description": "transaction 3", "amount": Decimal("1800.00")},
...         {"description": "transaction 4", "amount": Decimal("-300.00")},
...     ],
... )
BEGIN (implicit)
INSERT INTO account_transaction (account_id, description, amount, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
[...] [(1, 'transaction 1', 47.5), (1, 'transaction 2', -501.25), (1, 'transaction 3', 1800.0), (1, 'transaction 4', -300.0)]
<...>
>>> session.commit()
COMMIT
```

See also

[ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[One To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns-o2m) - at [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns)

#### Many to Many Collections

For a **many to many collection**, the relationship between two classes
involves a third table that is configured using the
[relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) parameter of [relationship](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).
To bulk insert rows into a collection of this type using
[WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection), the new records may be bulk-inserted separately
first, retrieved using RETURNING, and those records then passed to the
[WriteOnlyCollection.add_all()](#sqlalchemy.orm.WriteOnlyCollection.add_all) method where the unit of work process
will proceed to persist them as part of the collection.

Supposing a class `BankAudit` referred to many `AccountTransaction`
records using a many-to-many table:

```
>>> from sqlalchemy import Table, Column
>>> audit_to_transaction = Table(
...     "audit_transaction",
...     Base.metadata,
...     Column("audit_id", ForeignKey("audit.id", ondelete="CASCADE"), primary_key=True),
...     Column(
...         "transaction_id",
...         ForeignKey("account_transaction.id", ondelete="CASCADE"),
...         primary_key=True,
...     ),
... )
>>> class BankAudit(Base):
...     __tablename__ = "audit"
...     id: Mapped[int] = mapped_column(primary_key=True)
...     account_transactions: WriteOnlyMapped["AccountTransaction"] = relationship(
...         secondary=audit_to_transaction, passive_deletes=True
...     )
```

To illustrate the two operations, we add more `AccountTransaction` objects
using bulk insert, which we retrieve using RETURNING by adding
`returning(AccountTransaction)` to the bulk INSERT statement (note that
we could just as easily use existing `AccountTransaction` objects as well):

```
>>> new_transactions = session.scalars(
...     existing_account.account_transactions.insert().returning(AccountTransaction),
...     [
...         {"description": "odd trans 1", "amount": Decimal("50000.00")},
...         {"description": "odd trans 2", "amount": Decimal("25000.00")},
...         {"description": "odd trans 3", "amount": Decimal("45.00")},
...     ],
... ).all()
BEGIN (implicit)
INSERT INTO account_transaction (account_id, description, amount, timestamp) VALUES
(?, ?, ?, CURRENT_TIMESTAMP), (?, ?, ?, CURRENT_TIMESTAMP), (?, ?, ?, CURRENT_TIMESTAMP)
RETURNING id, account_id, description, amount, timestamp
[...] (1, 'odd trans 1', 50000.0, 1, 'odd trans 2', 25000.0, 1, 'odd trans 3', 45.0)
```

With a list of `AccountTransaction` objects ready, the
[WriteOnlyCollection.add_all()](#sqlalchemy.orm.WriteOnlyCollection.add_all) method is used to associate many rows
at once with a new `BankAudit` object:

```
>>> bank_audit = BankAudit()
>>> session.add(bank_audit)
>>> bank_audit.account_transactions.add_all(new_transactions)
>>> session.commit()
INSERT INTO audit DEFAULT VALUES
[...] ()
INSERT INTO audit_transaction (audit_id, transaction_id) VALUES (?, ?)
[...] [(1, 10), (1, 11), (1, 12)]
COMMIT
```

See also

[ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) - in the [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Many To Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationships-many-to-many) - at [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns)

### Bulk UPDATE and DELETE of Items

In a similar way in which [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) can generate
[Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) constructs with WHERE criteria pre-established, it can
also generate [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) and [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) constructs with that
same WHERE criteria, to allow criteria-oriented UPDATE and DELETE statements
against the elements in a large collection.

#### One To Many Collections

As is the case with INSERT, this feature is most straightforward with **one
to many collections**.

In the example below, the [WriteOnlyCollection.update()](#sqlalchemy.orm.WriteOnlyCollection.update) method is used
to generate an UPDATE statement is emitted against the elements
in the collection, locating rows where the “amount” is equal to `-800` and
adding the amount of `200` to them:

```
>>> session.execute(
...     existing_account.account_transactions.update()
...     .values(amount=AccountTransaction.amount + 200)
...     .where(AccountTransaction.amount == -800),
... )
BEGIN (implicit)
UPDATE account_transaction SET amount=(account_transaction.amount + ?)
WHERE ? = account_transaction.account_id AND account_transaction.amount = ?
[...] (200, 1, -800)
<...>
```

In a similar way, [WriteOnlyCollection.delete()](#sqlalchemy.orm.WriteOnlyCollection.delete) will produce a
DELETE statement that is invoked in the same way:

```
>>> session.execute(
...     existing_account.account_transactions.delete().where(
...         AccountTransaction.amount.between(0, 30)
...     ),
... )
DELETE FROM account_transaction WHERE ? = account_transaction.account_id
AND account_transaction.amount BETWEEN ? AND ? RETURNING id
[...] (1, 0, 30)
<...>
```

#### Many to Many Collections

Tip

The techniques here involve multi-table UPDATE expressions, which are
slightly more advanced.

For bulk UPDATE and DELETE of **many to many collections**, in order for
an UPDATE or DELETE statement to relate to the primary key of the
parent object, the association table must be explicitly part of the
UPDATE/DELETE statement, which requires
either that the backend includes supports for non-standard SQL syntaxes,
or extra explicit steps when constructing the UPDATE or DELETE statement.

For backends that support multi-table versions of UPDATE, the
[WriteOnlyCollection.update()](#sqlalchemy.orm.WriteOnlyCollection.update) method should work without extra steps
for a many-to-many collection, as in the example below where an UPDATE
is emitted against `AccountTransaction` objects in terms of the
many-to-many `BankAudit.account_transactions` collection:

```
>>> session.execute(
...     bank_audit.account_transactions.update().values(
...         description=AccountTransaction.description + " (audited)"
...     )
... )
UPDATE account_transaction SET description=(account_transaction.description || ?)
FROM audit_transaction WHERE ? = audit_transaction.audit_id
AND account_transaction.id = audit_transaction.transaction_id RETURNING id
[...] (' (audited)', 1)
<...>
```

The above statement automatically makes use of “UPDATE..FROM” syntax,
supported by SQLite and others, to name the additional `audit_transaction`
table in the WHERE clause.

To UPDATE or DELETE a many-to-many collection where multi-table syntax is
not available, the many-to-many criteria may be moved into SELECT that
for example may be combined with IN to match rows.
The [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) still helps us here, as we use the
[WriteOnlyCollection.select()](#sqlalchemy.orm.WriteOnlyCollection.select) method to generate this SELECT for
us, making use of the [Select.with_only_columns()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_only_columns) method to
produce a [scalar subquery](https://docs.sqlalchemy.org/en/20/glossary.html#term-scalar-subquery):

```
>>> from sqlalchemy import update
>>> subq = bank_audit.account_transactions.select().with_only_columns(AccountTransaction.id)
>>> session.execute(
...     update(AccountTransaction)
...     .values(description=AccountTransaction.description + " (audited)")
...     .where(AccountTransaction.id.in_(subq))
... )
UPDATE account_transaction SET description=(account_transaction.description || ?)
WHERE account_transaction.id IN (SELECT account_transaction.id
FROM audit_transaction
WHERE ? = audit_transaction.audit_id AND account_transaction.id = audit_transaction.transaction_id)
RETURNING id
[...] (' (audited)', 1)
<...>
```

### Write Only Collections - API Documentation

| Object Name | Description |
| --- | --- |
| WriteOnlyCollection | Write-only collection which can synchronize changes into the
attribute event system. |
| WriteOnlyMapped | Represent the ORM mapped attribute type for a “write only” relationship. |

   class sqlalchemy.orm.WriteOnlyCollection

*inherits from* `sqlalchemy.orm.writeonly.AbstractCollectionWriter`

Write-only collection which can synchronize changes into the
attribute event system.

The [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) is used in a mapping by
using the `"write_only"` lazy loading strategy with
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).     For background on this configuration,
see [Write Only Relationships](#write-only-relationship).

Added in version 2.0.

See also

[Write Only Relationships](#write-only-relationship)

| Member Name | Description |
| --- | --- |
| add() | Add an item to thisWriteOnlyCollection. |
| add_all() | Add an iterable of items to thisWriteOnlyCollection. |
| delete() | Produce aDeletewhich will refer to rows in terms
of this instance-localWriteOnlyCollection. |
| insert() | For one-to-many collections, produce aInsertwhich
will insert new rows in terms of this this instance-localWriteOnlyCollection. |
| remove() | Remove an item from thisWriteOnlyCollection. |
| select() | Produce aSelectconstruct that represents the
rows within this instance-localWriteOnlyCollection. |
| update() | Produce aUpdatewhich will refer to rows in terms
of this instance-localWriteOnlyCollection. |

   method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)add(*item:_T*) → None

Add an item to this [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

The given item will be persisted to the database in terms of
the parent instance’s collection on the next flush.

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)add_all(*iterator:Iterable[_T]*) → None

Add an iterable of items to this [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

The given items will be persisted to the database in terms of
the parent instance’s collection on the next flush.

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)delete() → [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete)

Produce a [Delete](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Delete) which will refer to rows in terms
of this instance-local [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)insert() → [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert)

For one-to-many collections, produce a [Insert](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Insert) which
will insert new rows in terms of this this instance-local
[WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

This construct is only supported for a [Relationship](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.Relationship)
that does **not** include the [relationship.secondary](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary)
parameter.  For relationships that refer to a many-to-many table,
use ordinary bulk insert techniques to produce new objects, then
use `AbstractCollectionWriter.add_all()` to associate them
with the collection.

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)remove(*item:_T*) → None

Remove an item from this [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

The given item will be removed from the parent instance’s collection on
the next flush.

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)select() → [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)[[Tuple](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.Tuple)[_T]]

Produce a [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) construct that represents the
rows within this instance-local [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

    method [sqlalchemy.orm.WriteOnlyCollection.](#sqlalchemy.orm.WriteOnlyCollection)update() → [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update)

Produce a [Update](https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.Update) which will refer to rows in terms
of this instance-local [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection).

     class sqlalchemy.orm.WriteOnlyMapped

*inherits from* `sqlalchemy.orm.base._MappedAnnotationBase`

Represent the ORM mapped attribute type for a “write only” relationship.

The [WriteOnlyMapped](#sqlalchemy.orm.WriteOnlyMapped) type annotation may be used in an
[Annotated Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column) mapping
to indicate that the `lazy="write_only"` loader strategy should be used
for a particular [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

E.g.:

```
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: WriteOnlyMapped[Address] = relationship(
        cascade="all,delete-orphan"
    )
```

See the section [Write Only Relationships](#write-only-relationship) for background.

Added in version 2.0.

See also

[Write Only Relationships](#write-only-relationship) - complete background

[DynamicMapped](#sqlalchemy.orm.DynamicMapped) - includes legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) support

## Dynamic Relationship Loaders

Legacy Feature

The “dynamic” lazy loader strategy is the legacy form of what is
now the “write_only” strategy described in the section
[Write Only Relationships](#write-only-relationship).

The “dynamic” strategy produces a legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object from the
related collection. However, a major drawback of “dynamic” relationships is
that there are several cases where the collection will fully iterate, some
of which are non-obvious, which can only be prevented with careful
programming and testing on a case-by-case basis. Therefore, for truly large
collection management, the [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) should be
preferred.

The dynamic loader is also not compatible with the [Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
extension. It can be used with some limitations, as indicated in
[Asyncio dynamic guidelines](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#dynamic-asyncio), but again the
[WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection), which is fully compatible with asyncio,
should be preferred.

The dynamic relationship strategy allows configuration of a
[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) which when accessed on an instance will return a
legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object in place of the collection. The
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) can then be modified further so that the database
collection may be iterated based on filtering criteria. The returned
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object is an instance of [AppenderQuery](#sqlalchemy.orm.AppenderQuery), which
combines the loading and iteration behavior of [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) along with
rudimentary collection mutation methods such as
[AppenderQuery.append()](#sqlalchemy.orm.AppenderQuery.append) and [AppenderQuery.remove()](#sqlalchemy.orm.AppenderQuery.remove).

The “dynamic” loader strategy may be configured with
type-annotated Declarative form using the [DynamicMapped](#sqlalchemy.orm.DynamicMapped)
annotation class:

```
from sqlalchemy.orm import DynamicMapped

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    posts: DynamicMapped[Post] = relationship()
```

Above, the `User.posts` collection on an individual `User` object
will return the [AppenderQuery](#sqlalchemy.orm.AppenderQuery) object, which is a subclass
of [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that also supports basic collection mutation
operations:

```
jack = session.get(User, id)

# filter Jack's blog posts
posts = jack.posts.filter(Post.headline == "this is a post")

# apply array slices
posts = jack.posts[5:20]
```

The dynamic relationship supports limited write operations, via the
[AppenderQuery.append()](#sqlalchemy.orm.AppenderQuery.append) and [AppenderQuery.remove()](#sqlalchemy.orm.AppenderQuery.remove) methods:

```
oldpost = jack.posts.filter(Post.headline == "old post").one()
jack.posts.remove(oldpost)

jack.posts.append(Post("new post"))
```

Since the read side of the dynamic relationship always queries the
database, changes to the underlying collection will not be visible
until the data has been flushed.  However, as long as “autoflush” is
enabled on the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in use, this will occur
automatically each time the collection is about to emit a
query.

### Dynamic Relationship Loaders - API

| Object Name | Description |
| --- | --- |
| AppenderQuery | A dynamic query that supports basic collection storage operations. |
| DynamicMapped | Represent the ORM mapped attribute type for a “dynamic” relationship. |

   class sqlalchemy.orm.AppenderQuery

*inherits from* `sqlalchemy.orm.dynamic.AppenderMixin`, [sqlalchemy.orm.Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)

A dynamic query that supports basic collection storage operations.

Methods on [AppenderQuery](#sqlalchemy.orm.AppenderQuery) include all methods of
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query), plus additional methods used for collection
persistence.

| Member Name | Description |
| --- | --- |
| add() | Add an item to thisAppenderQuery. |
| add_all() | Add an iterable of items to thisAppenderQuery. |
| append() | Append an item to thisAppenderQuery. |
| count() | Return a count of rows this the SQL formed by thisQuerywould return. |
| extend() | Add an iterable of items to thisAppenderQuery. |
| get_children() | Return immediate childHasTraverseInternalselements of thisHasTraverseInternals. |
| prefix_with() | Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative. |
| remove() | Remove an item from thisAppenderQuery. |
| suffix_with() | Add one or more expressions following the statement as a whole. |
| with_hint() | Add an indexing or other executional context hint for the given
selectable to thisSelector other selectable
object. |
| with_statement_hint() | Add a statement hint to thisSelector
other selectable object. |

   method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)add(*item:_T*) → None

*inherited from the* `AppenderMixin.add()` *method of* `AppenderMixin`

Add an item to this [AppenderQuery](#sqlalchemy.orm.AppenderQuery).

The given item will be persisted to the database in terms of
the parent instance’s collection on the next flush.

This method is provided to assist in delivering forwards-compatibility
with the [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) collection class.

Added in version 2.0.

     method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)add_all(*iterator:Iterable[_T]*) → None

*inherited from the* `AppenderMixin.add_all()` *method of* `AppenderMixin`

Add an iterable of items to this [AppenderQuery](#sqlalchemy.orm.AppenderQuery).

The given items will be persisted to the database in terms of
the parent instance’s collection on the next flush.

This method is provided to assist in delivering forwards-compatibility
with the [WriteOnlyCollection](#sqlalchemy.orm.WriteOnlyCollection) collection class.

Added in version 2.0.

     method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)append(*item:_T*) → None

*inherited from the* `AppenderMixin.append()` *method of* `AppenderMixin`

Append an item to this [AppenderQuery](#sqlalchemy.orm.AppenderQuery).

The given item will be persisted to the database in terms of
the parent instance’s collection on the next flush.

    method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)count() → int

*inherited from the* `AppenderMixin.count()` *method of* `AppenderMixin`

Return a count of rows this the SQL formed by this [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
would return.

This generates the SQL for this Query as follows:

```
SELECT count(1) AS count_1 FROM (
    SELECT <rest of query follows...>
) AS anon_1
```

The above SQL returns a single row, which is the aggregate value
of the count function; the [Query.count()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.count)
method then returns
that single integer value.

Warning

It is important to note that the value returned by
count() is **not the same as the number of ORM objects that this
Query would return from a method such as the .all() method**.
The [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object,
when asked to return full entities,
will **deduplicate entries based on primary key**, meaning if the
same primary key value would appear in the results more than once,
only one object of that primary key would be present.  This does
not apply to a query that is against individual columns.

See also

[My Query does not return the same number of objects as query.count() tells me - why?](https://docs.sqlalchemy.org/en/20/faq/sessions.html#faq-query-deduplicating)

For fine grained control over specific columns to count, to skip the
usage of a subquery or otherwise control of the FROM clause, or to use
other aggregate functions, use [expression.func](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func)
expressions in conjunction with [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query), i.e.:

```
from sqlalchemy import func

# count User records, without
# using a subquery.
session.query(func.count(User.id))

# return count of user "id" grouped
# by "name"
session.query(func.count(User.id)).group_by(User.name)

from sqlalchemy import distinct

# count distinct "name" values
session.query(func.count(distinct(User.name)))
```

See also

[2.0 Migration - ORM Usage](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage)

     method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)extend(*iterator:Iterable[_T]*) → None

*inherited from the* `AppenderMixin.extend()` *method of* `AppenderMixin`

Add an iterable of items to this [AppenderQuery](#sqlalchemy.orm.AppenderQuery).

The given items will be persisted to the database in terms of
the parent instance’s collection on the next flush.

    method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)get_children(***, *omit_attrs:Tuple[str,...]=()*, ***kw:Any*) → Iterable[HasTraverseInternals]

*inherited from the* `HasTraverseInternals.get_children()` *method of* `HasTraverseInternals`

Return immediate child `HasTraverseInternals`
elements of this `HasTraverseInternals`.

This is used for visit traversal.

**kw may contain flags that change the collection that is
returned, for example to return a subset of items in order to
cut down on larger traversals, or to return child items from a
different context (such as schema-level collections instead of
clause-level).

    method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)prefix_with(**prefixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasPrefixes.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with) *method of* [HasPrefixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes)

Add one or more expressions following the statement keyword, i.e.
SELECT, INSERT, UPDATE, or DELETE. Generative.

This is used to support backend-specific prefix keywords such as those
provided by MySQL.

E.g.:

```
stmt = table.insert().prefix_with("LOW_PRIORITY", dialect="mysql")

# MySQL 5.7 optimizer hints
stmt = select(table).prefix_with("/*+ BKA(t1) */", dialect="mysql")
```

Multiple prefixes can be specified by multiple calls
to [HasPrefixes.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasPrefixes.prefix_with).

  Parameters:

- ***prefixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the INSERT, UPDATE, or DELETE
  keyword.
- **dialect** – optional string dialect name which will
  limit rendering of this prefix to only that dialect.

      method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)remove(*item:_T*) → None

*inherited from the* `AppenderMixin.remove()` *method of* `AppenderMixin`

Remove an item from this [AppenderQuery](#sqlalchemy.orm.AppenderQuery).

The given item will be removed from the parent instance’s collection on
the next flush.

    method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)suffix_with(**suffixes:_TextCoercedExpressionArgument[Any]*, *dialect:str='*'*) → Self

*inherited from the* [HasSuffixes.suffix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes.suffix_with) *method of* [HasSuffixes](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes)

Add one or more expressions following the statement as a whole.

This is used to support backend-specific suffix keywords on
certain constructs.

E.g.:

```
stmt = (
    select(col1, col2)
    .cte()
    .suffix_with(
        "cycle empno set y_cycle to 1 default 0", dialect="oracle"
    )
)
```

Multiple suffixes can be specified by multiple calls
to [HasSuffixes.suffix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.HasSuffixes.suffix_with).

  Parameters:

- ***suffixes** – textual or [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement)
  construct which
  will be rendered following the target clause.
- **dialect** – Optional string dialect name which will
  limit rendering of this suffix to only that dialect.

      method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)with_hint(*selectable:_FromClauseArgument*, *text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_hint()` *method of* `HasHints`

Add an indexing or other executional context hint for the given
selectable to this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or other selectable
object.

Tip

The [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) method adds hints that are
**specific to a single table** to a statement, in a location that
is **dialect-specific**.  To add generic optimizer hints to the
**beginning** of a statement ahead of the SELECT keyword such as
for MySQL or Oracle Database, use the
[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) method.  To add optimizer
hints to the **end** of a statement such as for PostgreSQL, use the
[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) method.

The text of the hint is rendered in the appropriate
location for the database backend in use, relative
to the given [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or [Alias](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Alias)
passed as the
`selectable` argument. The dialect implementation
typically uses Python string substitution syntax
with the token `%(name)s` to render the name of
the table or alias. E.g. when using Oracle Database, the
following:

```
select(mytable).with_hint(mytable, "index(%(name)s ix_mytable)")
```

Would render SQL as:

```
select /*+ index(mytable ix_mytable) */ ... from mytable
```

The `dialect_name` option will limit the rendering of a particular
hint to a particular backend. Such as, to add hints for both Oracle
Database and MSSql simultaneously:

```
select(mytable).with_hint(
    mytable, "index(%(name)s ix_mytable)", "oracle"
).with_hint(mytable, "WITH INDEX ix_mytable", "mssql")
```

See also

[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint)

[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

     method [sqlalchemy.orm.AppenderQuery.](#sqlalchemy.orm.AppenderQuery)with_statement_hint(*text:str*, *dialect_name:str='*'*) → Self

*inherited from the* `HasHints.with_statement_hint()` *method of* `HasHints`

Add a statement hint to this [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) or
other selectable object.

Tip

[Select.with_statement_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_statement_hint) generally adds hints
**at the trailing end** of a SELECT statement.  To place
dialect-specific hints such as optimizer hints at the **front** of
the SELECT statement after the SELECT keyword, use the
[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) method for an open-ended
space, or for table-specific hints the
[Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) may be used, which places
hints in a dialect-specific location.

This method is similar to [Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint) except
that it does not require an individual table, and instead applies to
the statement as a whole.

Hints here are specific to the backend database and may include
directives such as isolation levels, file directives, fetch directives,
etc.

See also

[Select.with_hint()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.with_hint)

[Select.prefix_with()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.prefix_with) - generic SELECT prefixing
which also can suit some database-specific HINT syntaxes such as
MySQL or Oracle Database optimizer hints

      class sqlalchemy.orm.DynamicMapped

*inherits from* `sqlalchemy.orm.base._MappedAnnotationBase`

Represent the ORM mapped attribute type for a “dynamic” relationship.

The [DynamicMapped](#sqlalchemy.orm.DynamicMapped) type annotation may be used in an
[Annotated Declarative Table](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column) mapping
to indicate that the `lazy="dynamic"` loader strategy should be used
for a particular [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship).

Legacy Feature

The “dynamic” lazy loader strategy is the legacy form of what
is now the “write_only” strategy described in the section
[Write Only Relationships](#write-only-relationship).

E.g.:

```
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: DynamicMapped[Address] = relationship(
        cascade="all,delete-orphan"
    )
```

See the section [Dynamic Relationship Loaders](#dynamic-relationship) for background.

Added in version 2.0.

See also

[Dynamic Relationship Loaders](#dynamic-relationship) - complete background

[WriteOnlyMapped](#sqlalchemy.orm.WriteOnlyMapped) - fully 2.0 style version

## Setting RaiseLoad

A “raise”-loaded relationship will raise an
[InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) where the attribute would normally
emit a lazy load:

```
class MyClass(Base):
    __tablename__ = "some_table"

    # ...

    children: Mapped[List[MyRelatedClass]] = relationship(lazy="raise")
```

Above, attribute access on the `children` collection will raise an exception
if it was not previously populated.  This includes read access but for
collections will also affect write access, as collections can’t be mutated
without first loading them.  The rationale for this is to ensure that an
application is not emitting any unexpected lazy loads within a certain context.
Rather than having to read through SQL logs to determine that all necessary
attributes were eager loaded, the “raise” strategy will cause unloaded
attributes to raise immediately if accessed.  The raise strategy is
also available on a query option basis using the [raiseload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.raiseload)
loader option.

See also

[Preventing unwanted lazy loads using raiseload](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#prevent-lazy-with-raiseload)

## Using Passive Deletes

An important aspect of collection management in SQLAlchemy is that when an
object that refers to a collection is deleted, SQLAlchemy needs to consider the
objects that are inside this collection. Those objects will need to be
de-associated from the parent, which for a one-to-many collection would mean
that foreign key columns are set to NULL, or based on
[cascade](https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades) settings, may instead want to emit a
DELETE for these rows.

The [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) process only considers objects on a row-by-row basis,
meaning a DELETE operation implies that all rows within a collection must be
fully loaded into memory inside the flush process. This is not feasible for
large collections, so we instead seek to rely upon the database’s own
capability to update or delete the rows automatically using foreign key ON
DELETE rules, instructing the unit of work to forego actually needing to load
these rows in order to handle them. The unit of work can be instructed to work
in this manner by configuring [relationship.passive_deletes](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship.params.passive_deletes) on
the [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) construct; the foreign key constraints in use
must also be correctly configured.

For further detail on a complete “passive delete” configuration, see the
section [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/20/orm/cascades.html#passive-deletes).
