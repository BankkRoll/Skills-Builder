# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Expression Serializer Extension

Serializer/Deserializer objects for usage with SQLAlchemy query structures,
allowing “contextual” deserialization.

Legacy Feature

The serializer extension is **legacy** and should not be used for
new development.

Any SQLAlchemy query structure, either based on sqlalchemy.sql.*
or sqlalchemy.orm.* can be used.  The mappers, Tables, Columns, Session
etc. which are referenced by the structure are not persisted in serialized
form, but are instead re-associated with the query structure
when it is deserialized.

Warning

The serializer extension uses pickle to serialize and
deserialize objects, so the same security consideration mentioned
in the [python documentation](https://docs.python.org/3/library/pickle.html) apply.

Usage is nearly the same as that of the standard Python pickle module:

```
from sqlalchemy.ext.serializer import loads, dumps

metadata = MetaData(bind=some_engine)
Session = scoped_session(sessionmaker())

# ... define mappers

query = (
    Session.query(MyClass)
    .filter(MyClass.somedata == "foo")
    .order_by(MyClass.sortkey)
)

# pickle the query
serialized = dumps(query)

# unpickle.  Pass in metadata + scoped_session
query2 = loads(serialized, metadata, Session)

print(query2.all())
```

Similar restrictions as when using raw pickle apply; mapped classes must be
themselves be pickleable, meaning they are importable from a module-level
namespace.

The serializer module is only appropriate for query structures.  It is not
needed for:

- instances of user-defined classes.   These contain no references to engines,
  sessions or expression constructs in the typical case and can be serialized
  directly.
- Table metadata that is to be loaded entirely from the serialized structure
  (i.e. is not already declared in the application).   Regular
  pickle.loads()/dumps() can be used to fully dump any `MetaData` object,
  typically one which was reflected from an existing database at some previous
  point in time.  The serializer module is specifically for the opposite case,
  where the Table metadata is already present in memory.

| Object Name | Description |
| --- | --- |
| Deserializer |  |
| dumps(obj[, protocol]) |  |
| loads(data[, metadata, scoped_session, engine]) |  |
| Serializer |  |

   class sqlalchemy.ext.serializer.Deserializer

*inherits from* `_pickle.Unpickler`

| Member Name | Description |
| --- | --- |
| get_engine() |  |
| persistent_load() |  |

   method [sqlalchemy.ext.serializer.Deserializer.](#sqlalchemy.ext.serializer.Deserializer)get_engine()    method [sqlalchemy.ext.serializer.Deserializer.](#sqlalchemy.ext.serializer.Deserializer)persistent_load(*id_*)     class sqlalchemy.ext.serializer.Serializer

*inherits from* `_pickle.Pickler`

| Member Name | Description |
| --- | --- |
| persistent_id() |  |

   method [sqlalchemy.ext.serializer.Serializer.](#sqlalchemy.ext.serializer.Serializer)persistent_id(*obj*)     function sqlalchemy.ext.serializer.dumps(*obj*, *protocol=5*)    function sqlalchemy.ext.serializer.loads(*data*, *metadata=None*, *scoped_session=None*, *engine=None*)
