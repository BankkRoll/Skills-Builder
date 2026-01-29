# SQLAlchemy 2.0 Documentation

# SQLAlchemy 2.0 Documentation

# Contextual/Thread-local Sessions

Recall from the section [When do I construct a Session, when do I commit it, and when do I close it?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-whentocreate), the concept of
“session scopes” was introduced, with an emphasis on web applications
and the practice of linking the scope of a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with that
of a web request.   Most modern web frameworks include integration tools
so that the scope of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) can be managed automatically,
and these tools should be used as they are available.

SQLAlchemy includes its own helper object, which helps with the establishment
of user-defined [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) scopes.  It is also used by third-party
integration systems to help construct their integration schemes.

The object is the [scoped_session](#sqlalchemy.orm.scoped_session) object, and it represents a
**registry** of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects.  If you’re not familiar with the
registry pattern, a good introduction can be found in [Patterns of Enterprise
Architecture](https://martinfowler.com/eaaCatalog/registry.html).

Warning

The [scoped_session](#sqlalchemy.orm.scoped_session) registry by default uses a Python
`threading.local()`
in order to track [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) instances.   **This is not
necessarily compatible with all application servers**, particularly those
which make use of greenlets or other alternative forms of concurrency
control, which may lead to race conditions (e.g. randomly occurring
failures) when used in moderate to high concurrency scenarios.
Please read [Thread-Local Scope](#unitofwork-contextual-threadlocal) and
[Using Thread-Local Scope with Web Applications](#session-lifespan) below to more fully understand the implications
of using `threading.local()` to track [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects
and consider more explicit means of scoping when using application servers
which are not based on traditional threads.

Note

The [scoped_session](#sqlalchemy.orm.scoped_session) object is a very popular and useful object
used by many SQLAlchemy applications.  However, it is important to note
that it presents **only one approach** to the issue of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
management.  If you’re new to SQLAlchemy, and especially if the
term “thread-local variable” seems strange to you, we recommend that
if possible you familiarize first with an off-the-shelf integration
system such as [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
or [zope.sqlalchemy](https://pypi.org/project/zope.sqlalchemy).

A [scoped_session](#sqlalchemy.orm.scoped_session) is constructed by calling it, passing it a
**factory** which can create new [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects.   A factory
is just something that produces a new object when called, and in the
case of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), the most common factory is the [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker),
introduced earlier in this section.  Below we illustrate this usage:

```
>>> from sqlalchemy.orm import scoped_session
>>> from sqlalchemy.orm import sessionmaker

>>> session_factory = sessionmaker(bind=some_engine)
>>> Session = scoped_session(session_factory)
```

The [scoped_session](#sqlalchemy.orm.scoped_session) object we’ve created will now call upon the
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) when we “call” the registry:

```
>>> some_session = Session()
```

Above, `some_session` is an instance of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), which we
can now use to talk to the database.   This same [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is also
present within the [scoped_session](#sqlalchemy.orm.scoped_session) registry we’ve created.   If
we call upon the registry a second time, we get back the **same** [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session):

```
>>> some_other_session = Session()
>>> some_session is some_other_session
True
```

This pattern allows disparate sections of the application to call upon a global
[scoped_session](#sqlalchemy.orm.scoped_session), so that all those areas may share the same session
without the need to pass it explicitly.   The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) we’ve established
in our registry will remain, until we explicitly tell our registry to dispose of it,
by calling [scoped_session.remove()](#sqlalchemy.orm.scoped_session.remove):

```
>>> Session.remove()
```

The [scoped_session.remove()](#sqlalchemy.orm.scoped_session.remove) method first calls [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) on
the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), which has the effect of releasing any connection/transactional
resources owned by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) first, then discarding the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
itself.  “Releasing” here means that connections are returned to their connection pool and any transactional state is rolled back, ultimately using the `rollback()` method of the underlying DBAPI connection.

At this point, the [scoped_session](#sqlalchemy.orm.scoped_session) object is “empty”, and will create
a **new** [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) when called again.  As illustrated below, this
is not the same [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) we had before:

```
>>> new_session = Session()
>>> new_session is some_session
False
```

The above series of steps illustrates the idea of the “registry” pattern in a
nutshell.  With that basic idea in hand, we can discuss some of the details
of how this pattern proceeds.

## Implicit Method Access

The job of the [scoped_session](#sqlalchemy.orm.scoped_session) is simple; hold onto a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
for all who ask for it.  As a means of producing more transparent access to this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), the [scoped_session](#sqlalchemy.orm.scoped_session) also includes **proxy behavior**,
meaning that the registry itself can be treated just like a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
directly; when methods are called on this object, they are **proxied** to the
underlying [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) being maintained by the registry:

```
Session = scoped_session(some_factory)

# equivalent to:
#
# session = Session()
# print(session.scalars(select(MyClass)).all())
#
print(Session.scalars(select(MyClass)).all())
```

The above code accomplishes the same task as that of acquiring the current
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) by calling upon the registry, then using that [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

## Thread-Local Scope

Users who are familiar with multithreaded programming will note that representing
anything as a global variable is usually a bad idea, as it implies that the
global object will be accessed by many threads concurrently.   The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
object is entirely designed to be used in a **non-concurrent** fashion, which
in terms of multithreading means “only in one thread at a time”.   So our
above example of [scoped_session](#sqlalchemy.orm.scoped_session) usage, where the same [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
object is maintained across multiple calls, suggests that some process needs
to be in place such that multiple calls across many threads don’t actually get
a handle to the same session.   We call this notion **thread local storage**,
which means, a special object is used that will maintain a distinct object
per each application thread.   Python provides this via the
[threading.local()](https://docs.python.org/library/threading.html#threading.local)
construct.  The [scoped_session](#sqlalchemy.orm.scoped_session) object by default uses this object
as storage, so that a single [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is maintained for all who call
upon the [scoped_session](#sqlalchemy.orm.scoped_session) registry, but only within the scope of a single
thread.   Callers who call upon the registry in a different thread get a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) instance that is local to that other thread.

Using this technique, the [scoped_session](#sqlalchemy.orm.scoped_session) provides a quick and relatively
simple (if one is familiar with thread-local storage) way of providing
a single, global object in an application that is safe to be called upon
from multiple threads.

The [scoped_session.remove()](#sqlalchemy.orm.scoped_session.remove) method, as always, removes the current
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) associated with the thread, if any.  However, one advantage of the
`threading.local()` object is that if the application thread itself ends, the
“storage” for that thread is also garbage collected.  So it is in fact “safe” to
use thread local scope with an application that spawns and tears down threads,
without the need to call [scoped_session.remove()](#sqlalchemy.orm.scoped_session.remove).  However, the scope
of transactions themselves, i.e. ending them via [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) or
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback), will usually still be something that must be explicitly
arranged for at the appropriate time, unless the application actually ties the
lifespan of a thread to the lifespan of a transaction.

## Using Thread-Local Scope with Web Applications

As discussed in the section [When do I construct a Session, when do I commit it, and when do I close it?](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-faq-whentocreate), a web application
is architected around the concept of a **web request**, and integrating
such an application with the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) usually implies that the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
will be associated with that request.  As it turns out, most Python web frameworks,
with notable exceptions such as the asynchronous frameworks Twisted and
Tornado, use threads in a simple way, such that a particular web request is received,
processed, and completed within the scope of a single *worker thread*.  When
the request ends, the worker thread is released to a pool of workers where it
is available to handle another request.

This simple correspondence of web request and thread means that to associate a
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with a thread implies it is also associated with the web request
running within that thread, and vice versa, provided that the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is
created only after the web request begins and torn down just before the web request ends.
So it is a common practice to use [scoped_session](#sqlalchemy.orm.scoped_session) as a quick way
to integrate the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with a web application.  The sequence
diagram below illustrates this flow:

```
Web Server          Web Framework        SQLAlchemy ORM Code
--------------      --------------       ------------------------------
startup        ->   Web framework        # Session registry is established
                    initializes          Session = scoped_session(sessionmaker())

incoming
web request    ->   web request     ->   # The registry is *optionally*
                    starts               # called upon explicitly to create
                                         # a Session local to the thread and/or request
                                         Session()

                                         # the Session registry can otherwise
                                         # be used at any time, creating the
                                         # request-local Session() if not present,
                                         # or returning the existing one
                                         Session.execute(select(MyClass)) # ...

                                         Session.add(some_object) # ...

                                         # if data was modified, commit the
                                         # transaction
                                         Session.commit()

                    web request ends  -> # the registry is instructed to
                                         # remove the Session
                                         Session.remove()

                    sends output      <-
outgoing web    <-
response
```

Using the above flow, the process of integrating the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with the
web application has exactly two requirements:

1. Create a single [scoped_session](#sqlalchemy.orm.scoped_session) registry when the web application
  first starts, ensuring that this object is accessible by the rest of the
  application.
2. Ensure that [scoped_session.remove()](#sqlalchemy.orm.scoped_session.remove) is called when the web request ends,
  usually by integrating with the web framework’s event system to establish
  an “on request end” event.

As noted earlier, the above pattern is **just one potential way** to integrate a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
with a web framework, one which in particular makes the significant assumption
that the **web framework associates web requests with application threads**.  It is
however **strongly recommended that the integration tools provided with the web framework
itself be used, if available**, instead of [scoped_session](#sqlalchemy.orm.scoped_session).

In particular, while using a thread local can be convenient, it is preferable that the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) be
associated **directly with the request**, rather than with
the current thread.   The next section on custom scopes details a more advanced configuration
which can combine the usage of [scoped_session](#sqlalchemy.orm.scoped_session) with direct request based scope, or
any kind of scope.

## Using Custom Created Scopes

The [scoped_session](#sqlalchemy.orm.scoped_session) object’s default behavior of “thread local” scope is only
one of many options on how to “scope” a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).   A custom scope can be defined
based on any existing system of getting at “the current thing we are working with”.

Suppose a web framework defines a library function `get_current_request()`.  An application
built using this framework can call this function at any time, and the result will be
some kind of `Request` object that represents the current request being processed.
If the `Request` object is hashable, then this function can be easily integrated with
[scoped_session](#sqlalchemy.orm.scoped_session) to associate the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) with the request.  Below we illustrate
this in conjunction with a hypothetical event marker provided by the web framework
`on_request_end`, which allows code to be invoked whenever a request ends:

```
from my_web_framework import get_current_request, on_request_end
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker(bind=some_engine), scopefunc=get_current_request)

@on_request_end
def remove_session(req):
    Session.remove()
```

Above, we instantiate [scoped_session](#sqlalchemy.orm.scoped_session) in the usual way, except that we pass
our request-returning function as the “scopefunc”.  This instructs [scoped_session](#sqlalchemy.orm.scoped_session)
to use this function to generate a dictionary key whenever the registry is called upon
to return the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).   In this case it is particularly important
that we ensure a reliable “remove” system is implemented, as this dictionary is not
otherwise self-managed.

## Contextual Session API

| Object Name | Description |
| --- | --- |
| QueryPropertyDescriptor | Describes the type applied to a class-levelscoped_session.query_property()attribute. |
| scoped_session | Provides scoped management ofSessionobjects. |
| ScopedRegistry | A Registry that can store one or multiple instances of a single
class on the basis of a “scope” function. |
| ThreadLocalRegistry | AScopedRegistrythat uses athreading.local()variable for storage. |

   class sqlalchemy.orm.scoped_session

*inherits from* `typing.Generic`

Provides scoped management of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects.

See [Contextual/Thread-local Sessions](#unitofwork-contextual) for a tutorial.

Note

When using [Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html), the async-compatible
[async_scoped_session](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session) class should be
used in place of [scoped_session](#sqlalchemy.orm.scoped_session).

| Member Name | Description |
| --- | --- |
| __call__() | Return the currentSession, creating it
using thescoped_session.session_factoryif not present. |
| __init__() | Construct a newscoped_session. |
| add() | Place an object into thisSession. |
| add_all() | Add the given collection of instances to thisSession. |
| begin() | Begin a transaction, or nested transaction,
on thisSession, if one is not already begun. |
| begin_nested() | Begin a “nested” transaction on this Session, e.g. SAVEPOINT. |
| bulk_insert_mappings() | Perform a bulk insert of the given list of mapping dictionaries. |
| bulk_save_objects() | Perform a bulk save of the given list of objects. |
| bulk_update_mappings() | Perform a bulk update of the given list of mapping dictionaries. |
| close() | Close out the transactional resources and ORM objects used by thisSession. |
| close_all() | Closeallsessions in memory. |
| commit() | Flush pending changes and commit the current transaction. |
| configure() | reconfigure thesessionmakerused by thisscoped_session. |
| connection() | Return aConnectionobject corresponding to thisSessionobject’s transactional state. |
| delete() | Mark an instance as deleted. |
| execute() | Execute a SQL expression construct. |
| expire() | Expire the attributes on an instance. |
| expire_all() | Expires all persistent instances within this Session. |
| expunge() | Remove theinstancefrom thisSession. |
| expunge_all() | Remove all object instances from thisSession. |
| flush() | Flush all the object changes to the database. |
| get() | Return an instance based on the given primary key identifier,
orNoneif not found. |
| get_bind() | Return a “bind” to which thisSessionis bound. |
| get_one() | Return exactly one instance based on the given primary key
identifier, or raise an exception if not found. |
| identity_key() | Return an identity key. |
| is_modified() | ReturnTrueif the given instance has locally
modified attributes. |
| merge() | Copy the state of a given instance into a corresponding instance
within thisSession. |
| object_session() | Return theSessionto which an object belongs. |
| query() | Return a newQueryobject corresponding to thisSession. |
| query_property() | return a class property which produces a legacyQueryobject against the class and the currentSessionwhen called. |
| refresh() | Expire and refresh attributes on the given instance. |
| remove() | Dispose of the currentSession, if present. |
| reset() | Close out the transactional resources and ORM objects used by thisSession, resetting the session to its initial state. |
| rollback() | Rollback the current transaction in progress. |
| scalar() | Execute a statement and return a scalar result. |
| scalars() | Execute a statement and return the results as scalars. |
| session_factory | Thesession_factoryprovided to__init__is stored in this
attribute and may be accessed at a later time.  This can be useful when
a new non-scopedSessionis needed. |

   method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)__call__(***kw:Any*) → _S

Return the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), creating it
using the [scoped_session.session_factory](#sqlalchemy.orm.scoped_session.session_factory) if not present.

  Parameters:

****kw** – Keyword arguments will be passed to the
[scoped_session.session_factory](#sqlalchemy.orm.scoped_session.session_factory) callable, if an existing
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is not present.  If the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is present
and keyword arguments have been passed,
[InvalidRequestError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.InvalidRequestError) is raised.

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)__init__(*session_factory:sessionmaker[_S]*, *scopefunc:Callable[[],Any]|None=None*)

Construct a new [scoped_session](#sqlalchemy.orm.scoped_session).

  Parameters:

- **session_factory** – a factory to create new [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  instances. This is usually, but not necessarily, an instance
  of [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker).
- **scopefunc** – optional function which defines
  the current scope.   If not passed, the [scoped_session](#sqlalchemy.orm.scoped_session)
  object assumes “thread-local” scope, and will use
  a Python `threading.local()` in order to maintain the current
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).  If passed, the function should return
  a hashable token; this token will be used as the key in a
  dictionary in order to store and retrieve the current
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)add(*instance:object*, *_warn:bool=True*) → None

Place an object into this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Objects that are in the [transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) state when passed to the
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) method will move to the
[pending](https://docs.sqlalchemy.org/en/20/glossary.html#term-pending) state, until the next flush, at which point they
will move to the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) state.

Objects that are in the [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) state when passed to the
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) method will move to the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent)
state directly.

If the transaction used by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is rolled back,
objects which were transient when they were passed to
[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) will be moved back to the
[transient](https://docs.sqlalchemy.org/en/20/glossary.html#term-transient) state, and will no longer be present within this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[Session.add_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add_all)

[Adding New or Existing Items](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-adding) - at [Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)add_all(*instances:Iterable[object]*) → None

Add the given collection of instances to this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

See the documentation for [Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add) for a general
behavioral description.

See also

[Session.add()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add)

[Adding New or Existing Items](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-adding) - at [Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

     property autoflush: bool

Proxy for the `Session.autoflush` attribute
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)begin(*nested:bool=False*) → [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)

Begin a transaction, or nested transaction,
on this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), if one is not already begun.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object features **autobegin** behavior,
so that normally it is not necessary to call the
[Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin)
method explicitly. However, it may be used in order to control
the scope of when the transactional state is begun.

When used to begin the outermost transaction, an error is raised
if this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is already inside of a transaction.

  Parameters:

**nested** – if True, begins a SAVEPOINT transaction and is
equivalent to calling [Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested). For
documentation on SAVEPOINT transactions, please see
[Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested).

  Returns:

the [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) object.  Note that
[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)
acts as a Python context manager, allowing [Session.begin()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin)
to be used in a “with” block.  See [Explicit Begin](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-explicit-begin) for
an example.

See also

[Auto Begin](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-autobegin)

[Managing Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#unitofwork-transaction)

[Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)begin_nested() → [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction)

Begin a “nested” transaction on this Session, e.g. SAVEPOINT.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The target database(s) and associated drivers must support SQL
SAVEPOINT for this method to function correctly.

For documentation on SAVEPOINT
transactions, please see [Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested).

  Returns:

the [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) object.  Note that
[SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) acts as a context manager, allowing
[Session.begin_nested()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.begin_nested) to be used in a “with” block.
See [Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested) for a usage example.

See also

[Using SAVEPOINT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-begin-nested)

[Serializable isolation / Savepoints / Transactional DDL](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-serializable) - special workarounds required
with the SQLite driver in order for SAVEPOINT to work
correctly. For asyncio use cases, see the section
[Serializable isolation / Savepoints / Transactional DDL (asyncio version)](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#aiosqlite-serializable).

     property bind: [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) | [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) | None

Proxy for the `Session.bind` attribute
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)bulk_insert_mappings(*mapper:Mapper[Any]*, *mappings:Iterable[Dict[str,Any]]*, *return_defaults:bool=False*, *render_nulls:bool=False*) → None

Perform a bulk insert of the given list of mapping dictionaries.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Legacy Feature

This method is a legacy feature as of the 2.0 series of
SQLAlchemy.   For modern bulk INSERT and UPDATE, see
the sections [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) and
[ORM Bulk UPDATE by Primary Key](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update).  The 2.0 API shares
implementation details with this method and adds new features
as well.

   Parameters:

- **mapper** – a mapped class, or the actual [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
  object,
  representing the single kind of object represented within the mapping
  list.
- **mappings** – a sequence of dictionaries, each one containing the
  state of the mapped row to be inserted, in terms of the attribute
  names on the mapped class.   If the mapping refers to multiple tables,
  such as a joined-inheritance mapping, each dictionary must contain all
  keys to be populated into all tables.
- **return_defaults** –
  when True, the INSERT process will be altered
  to ensure that newly generated primary key values will be fetched.
  The rationale for this parameter is typically to enable
  [Joined Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-inheritance) mappings to
  be bulk inserted.
  Note
  for backends that don’t support RETURNING, the
  [Session.bulk_insert_mappings.return_defaults](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings.params.return_defaults)
  parameter can significantly decrease performance as INSERT
  statements can no longer be batched.   See
  [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues)
  for background on which backends are affected.
- **render_nulls** –
  When True, a value of `None` will result
  in a NULL value being included in the INSERT statement, rather
  than the column being omitted from the INSERT.   This allows all
  the rows being INSERTed to have the identical set of columns which
  allows the full set of rows to be batched to the DBAPI.  Normally,
  each column-set that contains a different combination of NULL values
  than the previous row must omit a different series of columns from
  the rendered INSERT statement, which means it must be emitted as a
  separate statement.   By passing this flag, the full set of rows
  are guaranteed to be batchable into one batch; the cost however is
  that server-side defaults which are invoked by an omitted column will
  be skipped, so care must be taken to ensure that these are not
  necessary.
  Warning
  When this flag is set, **server side default SQL values will
  not be invoked** for those columns that are inserted as NULL;
  the NULL value will be sent explicitly.   Care must be taken
  to ensure that no server-side default functions need to be
  invoked for the operation as a whole.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html)

[Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects)

[Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)bulk_save_objects(*objects:Iterable[object]*, *return_defaults:bool=False*, *update_changed_only:bool=True*, *preserve_order:bool=True*) → None

Perform a bulk save of the given list of objects.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Legacy Feature

This method is a legacy feature as of the 2.0 series of
SQLAlchemy.   For modern bulk INSERT and UPDATE, see
the sections [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) and
[ORM Bulk UPDATE by Primary Key](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update).

For general INSERT and UPDATE of existing ORM mapped objects,
prefer standard [unit of work](https://docs.sqlalchemy.org/en/20/glossary.html#term-unit-of-work) data management patterns,
introduced in the [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial) at
[Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation).  SQLAlchemy 2.0
now uses [“Insert Many Values” Behavior for INSERT statements](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-insertmanyvalues) with modern dialects
which solves previous issues of bulk INSERT slowness.

   Parameters:

- **objects** –
  a sequence of mapped object instances.  The mapped
  objects are persisted as is, and are **not** associated with the
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) afterwards.
  For each object, whether the object is sent as an INSERT or an
  UPDATE is dependent on the same rules used by the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  in traditional operation; if the object has the
  `InstanceState.key`
  attribute set, then the object is assumed to be “detached” and
  will result in an UPDATE.  Otherwise, an INSERT is used.
  In the case of an UPDATE, statements are grouped based on which
  attributes have changed, and are thus to be the subject of each
  SET clause.  If `update_changed_only` is False, then all
  attributes present within each object are applied to the UPDATE
  statement, which may help in allowing the statements to be grouped
  together into a larger executemany(), and will also reduce the
  overhead of checking history on attributes.
- **return_defaults** – when True, rows that are missing values which
  generate defaults, namely integer primary key defaults and sequences,
  will be inserted **one at a time**, so that the primary key value
  is available.  In particular this will allow joined-inheritance
  and other multi-table mappings to insert correctly without the need
  to provide primary key values ahead of time; however,
  [Session.bulk_save_objects.return_defaults](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects.params.return_defaults) **greatly
  reduces the performance gains** of the method overall.  It is strongly
  advised to please use the standard [Session.add_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add_all)
  approach.
- **update_changed_only** – when True, UPDATE statements are rendered
  based on those attributes in each state that have logged changes.
  When False, all attributes present are rendered into the SET clause
  with the exception of primary key attributes.
- **preserve_order** – when True, the order of inserts and updates
  matches exactly the order in which the objects are given.   When
  False, common types of objects are grouped into inserts
  and updates, to allow for more batching opportunities.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html)

[Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings)

[Session.bulk_update_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_update_mappings)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)bulk_update_mappings(*mapper:Mapper[Any]*, *mappings:Iterable[Dict[str,Any]]*) → None

Perform a bulk update of the given list of mapping dictionaries.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Legacy Feature

This method is a legacy feature as of the 2.0 series of
SQLAlchemy.   For modern bulk INSERT and UPDATE, see
the sections [ORM Bulk INSERT Statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert) and
[ORM Bulk UPDATE by Primary Key](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update).  The 2.0 API shares
implementation details with this method and adds new features
as well.

   Parameters:

- **mapper** – a mapped class, or the actual [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper)
  object,
  representing the single kind of object represented within the mapping
  list.
- **mappings** – a sequence of dictionaries, each one containing the
  state of the mapped row to be updated, in terms of the attribute names
  on the mapped class.   If the mapping refers to multiple tables, such
  as a joined-inheritance mapping, each dictionary may contain keys
  corresponding to all tables.   All those keys which are present and
  are not part of the primary key are applied to the SET clause of the
  UPDATE statement; the primary key values, which are required, are
  applied to the WHERE clause.

See also

[ORM-Enabled INSERT, UPDATE, and DELETE statements](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html)

[Session.bulk_insert_mappings()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_insert_mappings)

[Session.bulk_save_objects()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bulk_save_objects)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)close() → None

Close out the transactional resources and ORM objects used by this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This expunges all ORM objects associated with this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), ends any transaction in progress and
[releases](https://docs.sqlalchemy.org/en/20/glossary.html#term-releases) any [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) objects which this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) itself has checked out from associated
[Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) objects. The operation then leaves the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) in a state which it may be used again.

Tip

In the default running mode the [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close)
method **does not prevent the Session from being used again**.
The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) itself does not actually have a
distinct “closed” state; it merely means
the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will release all database connections
and ORM objects.

Setting the parameter [Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only)
to `False` will instead make the `close` final, meaning that
any further action on the session will be forbidden.

Changed in version 1.4: The [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) method does not
immediately create a new [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) object;
instead, the new [SessionTransaction](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.SessionTransaction) is created only if
the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is used again for a database operation.

See also

[Closing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-closing) - detail on the semantics of
[Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) and [Session.reset()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.reset).

[Session.reset()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.reset) - a similar method that behaves like
`close()` with  the parameter
[Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only) set to `True`.

     classmethod [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)close_all() → None

Close *all* sessions in memory.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Deprecated since version 1.3: The [Session.close_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close_all) method is deprecated and will be removed in a future release.  Please refer to `close_all_sessions()`.

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)commit() → None

Flush pending changes and commit the current transaction.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

When the COMMIT operation is complete, all objects are fully
[expired](https://docs.sqlalchemy.org/en/20/glossary.html#term-expired), erasing their internal contents, which will be
automatically re-loaded when the objects are next accessed. In the
interim, these objects are in an expired state and will not function if
they are [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) from the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session). Additionally,
this re-load operation is not supported when using asyncio-oriented
APIs. The [Session.expire_on_commit](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.expire_on_commit) parameter may be used
to disable this behavior.

When there is no transaction in place for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
indicating that no operations were invoked on this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
since the previous call to [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit), the method will
begin and commit an internal-only “logical” transaction, that does not
normally affect the database unless pending flush changes were
detected, but will still invoke event handlers and object expiration
rules.

The outermost database transaction is committed unconditionally,
automatically releasing any SAVEPOINTs in effect.

See also

[Committing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-committing)

[Managing Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#unitofwork-transaction)

[Preventing Implicit IO when Using AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)configure(***kwargs:Any*) → None

reconfigure the [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) used by this
[scoped_session](#sqlalchemy.orm.scoped_session).

See [sessionmaker.configure()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.configure).

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)connection(*bind_arguments:_BindArguments|None=None*, *execution_options:CoreExecuteOptionsParameter|None=None*) → [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Return a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) object corresponding to this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s transactional state.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Either the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) corresponding to the current
transaction is returned, or if no transaction is in progress, a new
one is begun and the [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
returned (note that no
transactional state is established with the DBAPI until the first
SQL statement is emitted).

Ambiguity in multi-bind or unbound [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects can be
resolved through any of the optional keyword arguments.   This
ultimately makes usage of the [get_bind()](#sqlalchemy.orm.scoped_session.get_bind) method for resolution.

  Parameters:

- **bind_arguments** – dictionary of bind arguments.  May include
  “mapper”, “bind”, “clause”, other custom arguments that are passed
  to [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind).
- **execution_options** –
  a dictionary of execution options that will
  be passed to [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options), **when the
  connection is first procured only**.   If the connection is already
  present within the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), a warning is emitted and
  the arguments are ignored.
  See also
  [Setting Transaction Isolation Levels / DBAPI AUTOCOMMIT](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#session-transaction-isolation)

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)delete(*instance:object*) → None

Mark an instance as deleted.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The object is assumed to be either [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) or
[detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) when passed; after the method is called, the
object will remain in the [persistent](https://docs.sqlalchemy.org/en/20/glossary.html#term-persistent) state until the next
flush proceeds.  During this time, the object will also be a member
of the [Session.deleted](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.deleted) collection.

When the next flush proceeds, the object will move to the
[deleted](https://docs.sqlalchemy.org/en/20/glossary.html#term-deleted) state, indicating a `DELETE` statement was emitted
for its row within the current transaction.   When the transaction
is successfully committed,
the deleted object is moved to the [detached](https://docs.sqlalchemy.org/en/20/glossary.html#term-detached) state and is
no longer present within this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

See also

[Deleting](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-deleting) - at [Basics of Using a Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

     property deleted: Any

The set of all instances marked as ‘deleted’ within this `Session`

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

     property dirty: Any

The set of all persistent instances considered dirty.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

E.g.:

```
some_mapped_object in session.dirty
```

Instances are considered dirty when they were modified but not
deleted.

Note that this ‘dirty’ calculation is ‘optimistic’; most
attribute-setting or collection modification operations will
mark an instance as ‘dirty’ and place it in this set, even if
there is no net change to the attribute’s value.  At flush
time, the value of each attribute is compared to its
previously saved value, and if there’s no net change, no SQL
operation will occur (this is a more expensive operation so
it’s only done at flush time).

To check if an instance has actionable net changes to its
attributes, use the [Session.is_modified()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_modified) method.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)execute(*statement:Executable*, *params:_CoreAnyExecuteParams|None=None*, ***, *execution_options:OrmExecuteOptionsParameter={}*, *bind_arguments:_BindArguments|None=None*, *_parent_execute_state:Any|None=None*, *_add_event:Any|None=None*) → [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result)[Any]

Execute a SQL expression construct.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Returns a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object representing
results of the statement execution.

E.g.:

```
from sqlalchemy import select

result = session.execute(select(User).where(User.id == 5))
```

The API contract of [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) is similar to that
of [Connection.execute()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute), the [2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) version
of [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

Changed in version 1.4: the [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) method is
now the primary point of ORM statement execution when using
[2.0 style](https://docs.sqlalchemy.org/en/20/glossary.html#term-2.0-style) ORM usage.

   Parameters:

- **statement** – An executable statement (i.e. an [Executable](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable) expression
  such as [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select)).
- **params** – Optional dictionary, or list of dictionaries, containing
  bound parameter values.   If a single dictionary, single-row
  execution occurs; if a list of dictionaries, an
  “executemany” will be invoked.  The keys in each dictionary
  must correspond to parameter names present in the statement.
- **execution_options** –
  optional dictionary of execution options,
  which will be associated with the statement execution.  This
  dictionary can provide a subset of the options that are accepted
  by [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options), and may also
  provide additional options understood only in an ORM context.
  See also
  [ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - ORM-specific execution
  options
- **bind_arguments** – dictionary of additional arguments to determine
  the bind.  May include “mapper”, “bind”, or other custom arguments.
  Contents of this dictionary are passed to the
  [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) method.

  Returns:

a [Result](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) object.

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)expire(*instance:object*, *attribute_names:Iterable[str]|None=None*) → None

Expire the attributes on an instance.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Marks the attributes of an instance as out of date. When an expired
attribute is next accessed, a query will be issued to the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s current transactional context in order to
load all expired attributes for the given instance.   Note that
a highly isolated transaction will return the same values as were
previously read in that same transaction, regardless of changes
in database state outside of that transaction.

To expire all objects in the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) simultaneously,
use [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all).

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s default behavior is to
expire all state whenever the [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback)
or [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) methods are called, so that new
state can be loaded for the new transaction.   For this reason,
calling [Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire) only makes sense for the specific
case that a non-ORM SQL statement was emitted in the current
transaction.

  Parameters:

- **instance** – The instance to be refreshed.
- **attribute_names** – optional list of string attribute names
  indicating a subset of attributes to be expired.

See also

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire) - introductory material

[Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire)

[Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh)

[Query.populate_existing()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.populate_existing)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)expire_all() → None

Expires all persistent instances within this Session.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

When any attributes on a persistent instance is next accessed,
a query will be issued using the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s current transactional context in order to
load all expired attributes for the given instance.   Note that
a highly isolated transaction will return the same values as were
previously read in that same transaction, regardless of changes
in database state outside of that transaction.

To expire individual objects and individual attributes
on those objects, use [Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire).

The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object’s default behavior is to
expire all state whenever the [Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback)
or [Session.commit()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.commit) methods are called, so that new
state can be loaded for the new transaction.   For this reason,
calling [Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all) is not usually needed,
assuming the transaction is isolated.

See also

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire) - introductory material

[Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire)

[Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh)

[Query.populate_existing()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.populate_existing)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)expunge(*instance:object*) → None

Remove the instance from this `Session`.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This will free all internal references to the instance.  Cascading
will be applied according to the *expunge* cascade rule.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)expunge_all() → None

Remove all object instances from this `Session`.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This is equivalent to calling `expunge(obj)` on all objects in this
`Session`.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)flush(*objects:Sequence[Any]|None=None*) → None

Flush all the object changes to the database.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Writes out all pending object creations, deletions and modifications
to the database as INSERTs, DELETEs, UPDATEs, etc.  Operations are
automatically ordered by the Session’s unit of work dependency
solver.

Database operations will be issued in the current transactional
context and do not affect the state of the transaction, unless an
error occurs, in which case the entire transaction is rolled back.
You may flush() as often as you like within a transaction to move
changes from Python to the database’s transaction buffer.

  Parameters:

**objects** –

Optional; restricts the flush operation to operate
only on elements that are in the given collection.

This feature is for an extremely narrow set of use cases where
particular objects may need to be operated upon before the
full flush() occurs.  It is not intended for general use.

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)get(*entity:_EntityBindKey[_O]*, *ident:_PKIdentityArgument*, ***, *options:Sequence[ORMOption]|None=None*, *populate_existing:bool=False*, *with_for_update:ForUpdateParameter=None*, *identity_token:Any|None=None*, *execution_options:OrmExecuteOptionsParameter={}*, *bind_arguments:_BindArguments|None=None*) → _O | None

Return an instance based on the given primary key identifier,
or `None` if not found.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

E.g.:

```
my_user = session.get(User, 5)

some_object = session.get(VersionedFoo, (5, 10))

some_object = session.get(VersionedFoo, {"id": 5, "version_id": 10})
```

Added in version 1.4: Added [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get), which is moved
from the now legacy [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get) method.

[Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) is special in that it provides direct
access to the identity map of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).
If the given primary key identifier is present
in the local identity map, the object is returned
directly from this collection and no SQL is emitted,
unless the object has been marked fully expired.
If not present,
a SELECT is performed in order to locate the object.

[Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) also will perform a check if
the object is present in the identity map and
marked as expired - a SELECT
is emitted to refresh the object as well as to
ensure that the row is still present.
If not, [ObjectDeletedError](https://docs.sqlalchemy.org/en/20/orm/exceptions.html#sqlalchemy.orm.exc.ObjectDeletedError) is raised.

  Parameters:

- **entity** – a mapped class or [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) indicating the
  type of entity to be loaded.
- **ident** –
  A scalar, tuple, or dictionary representing the
  primary key.  For a composite (e.g. multiple column) primary key,
  a tuple or dictionary should be passed.
  For a single-column primary key, the scalar calling form is typically
  the most expedient.  If the primary key of a row is the value “5”,
  the call looks like:
  ```
  my_object = session.get(SomeClass, 5)
  ```
  The tuple form contains primary key values typically in
  the order in which they correspond to the mapped
  [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  object’s primary key columns, or if the
  [Mapper.primary_key](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper.params.primary_key) configuration parameter were
  used, in
  the order used for that parameter. For example, if the primary key
  of a row is represented by the integer
  digits “5, 10” the call would look like:
  ```
  my_object = session.get(SomeClass, (5, 10))
  ```
  The dictionary form should include as keys the mapped attribute names
  corresponding to each element of the primary key.  If the mapped class
  has the attributes `id`, `version_id` as the attributes which
  store the object’s primary key value, the call would look like:
  ```
  my_object = session.get(SomeClass, {"id": 5, "version_id": 10})
  ```
- **options** – optional sequence of loader options which will be
  applied to the query, if one is emitted.
- **populate_existing** – causes the method to unconditionally emit
  a SQL query and refresh the object with the newly loaded data,
  regardless of whether or not the object is already present.
- **with_for_update** – optional boolean `True` indicating FOR UPDATE
  should be used, or may be a dictionary containing flags to
  indicate a more specific set of FOR UPDATE flags for the SELECT;
  flags should match the parameters of
  [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update).
  Supersedes the [Session.refresh.lockmode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh.params.lockmode) parameter.
- **execution_options** –
  optional dictionary of execution options,
  which will be associated with the query execution if one is emitted.
  This dictionary can provide a subset of the options that are
  accepted by [Connection.execution_options()](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execution_options), and may
  also provide additional options understood only in an ORM context.
  Added in version 1.4.29.
  See also
  [ORM Execution Options](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-execution-options) - ORM-specific execution
  options
- **bind_arguments** –
  dictionary of additional arguments to determine
  the bind.  May include “mapper”, “bind”, or other custom arguments.
  Contents of this dictionary are passed to the
  [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) method.

  Returns:

The object instance, or `None`.

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)get_bind(*mapper:_EntityBindKey[_O]|None=None*, ***, *clause:ClauseElement|None=None*, *bind:_SessionBind|None=None*, *_sa_skip_events:bool|None=None*, *_sa_skip_for_implicit_returning:bool=False*, ***kw:Any*) → [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) | [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Return a “bind” to which this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is bound.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The “bind” is usually an instance of [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine),
except in the case where the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has been
explicitly bound directly to a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection).

For a multiply-bound or unbound [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), the
`mapper` or `clause` arguments are used to determine the
appropriate bind to return.

Note that the “mapper” argument is usually present
when [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) is called via an ORM
operation such as a [Session.query()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.query), each
individual INSERT/UPDATE/DELETE operation within a
[Session.flush()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.flush), call, etc.

The order of resolution is:

1. if mapper given and [Session.binds](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.binds) is present,
  locate a bind based first on the mapper in use, then
  on the mapped class in use, then on any base classes that are
  present in the `__mro__` of the mapped class, from more specific
  superclasses to more general.
2. if clause given and `Session.binds` is present,
  locate a bind based on [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects
  found in the given clause present in `Session.binds`.
3. if `Session.binds` is present, return that.
4. if clause given, attempt to return a bind
  linked to the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) ultimately
  associated with the clause.
5. if mapper given, attempt to return a bind
  linked to the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) ultimately
  associated with the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) or other
  selectable to which the mapper is mapped.
6. No bind can be found, [UnboundExecutionError](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.UnboundExecutionError)
  is raised.

Note that the [Session.get_bind()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get_bind) method can be overridden on
a user-defined subclass of [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to provide any kind
of bind resolution scheme.  See the example at
[Custom Vertical Partitioning](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#session-custom-partitioning).

  Parameters:

- **mapper** – Optional mapped class or corresponding [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) instance.
  The bind can be derived from a [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) first by
  consulting the “binds” map associated with this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session),
  and secondly by consulting the [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData) associated
  with the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) to which the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) is
  mapped for a bind.
- **clause** – A [ClauseElement](https://docs.sqlalchemy.org/en/20/core/foundation.html#sqlalchemy.sql.expression.ClauseElement) (i.e.
  [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select),
  [text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text),
  etc.).  If the `mapper` argument is not present or could not
  produce a bind, the given expression construct will be searched
  for a bound element, typically a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
  associated with
  bound [MetaData](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData).

See also

[Partitioning Strategies (e.g. multiple database backends per Session)](https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#session-partitioning)

[Session.binds](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.binds)

[Session.bind_mapper()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_mapper)

[Session.bind_table()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.bind_table)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)get_one(*entity:_EntityBindKey[_O]*, *ident:_PKIdentityArgument*, ***, *options:Sequence[ORMOption]|None=None*, *populate_existing:bool=False*, *with_for_update:ForUpdateParameter=None*, *identity_token:Any|None=None*, *execution_options:OrmExecuteOptionsParameter={}*, *bind_arguments:_BindArguments|None=None*) → _O

Return exactly one instance based on the given primary key
identifier, or raise an exception if not found.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Raises [NoResultFound](https://docs.sqlalchemy.org/en/20/core/exceptions.html#sqlalchemy.exc.NoResultFound) if the query selects no rows.

For a detailed documentation of the arguments see the
method [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get).

Added in version 2.0.22.

   Returns:

The object instance.

See also

  [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) - equivalent method that instead

returns `None` if no row was found with the provided primary
key

       classmethod [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)identity_key(*class_:Type[Any]|None=None*, *ident:Any|Tuple[Any,...]=None*, ***, *instance:Any|None=None*, *row:Row[Any]|RowMapping|None=None*, *identity_token:Any|None=None*) → _IdentityKeyType[Any]

Return an identity key.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This is an alias of [identity_key()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.util.identity_key).

    property identity_map: [IdentityMap](https://docs.sqlalchemy.org/en/20/orm/internals.html#sqlalchemy.orm.IdentityMap)

Proxy for the [Session.identity_map](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.identity_map) attribute
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

    property info: Any

A user-modifiable dictionary.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The initial value of this dictionary can be populated using the
`info` argument to the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) constructor or
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) constructor or factory methods.  The dictionary
here is always local to this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) and can be modified
independently of all other [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects.

    property is_active: Any

True if this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) not in “partial rollback” state.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Changed in version 1.4: The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) no longer begins
a new transaction immediately, so this attribute will be False
when the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is first instantiated.

“partial rollback” state typically indicates that the flush process
of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) has failed, and that the
[Session.rollback()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.rollback) method must be emitted in order to
fully roll back the transaction.

If this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is not in a transaction at all, the
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) will autobegin when it is first used, so in this
case [Session.is_active](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_active) will return True.

Otherwise, if this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is within a transaction,
and that transaction has not been rolled back internally, the
[Session.is_active](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_active) will also return True.

See also

[“This Session’s transaction has been rolled back due to a previous exception during flush.” (or similar)](https://docs.sqlalchemy.org/en/20/faq/sessions.html#faq-session-rollback)

[Session.in_transaction()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.in_transaction)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)is_modified(*instance:object*, *include_collections:bool=True*) → bool

Return `True` if the given instance has locally
modified attributes.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This method retrieves the history for each instrumented
attribute on the instance and performs a comparison of the current
value to its previously flushed or committed value, if any.

It is in effect a more expensive and accurate
version of checking for the given instance in the
[Session.dirty](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.dirty) collection; a full test for
each attribute’s net “dirty” status is performed.

E.g.:

```
return session.is_modified(someobject)
```

A few caveats to this method apply:

- Instances present in the [Session.dirty](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.dirty) collection may
  report `False` when tested with this method.  This is because
  the object may have received change events via attribute mutation,
  thus placing it in [Session.dirty](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.dirty), but ultimately the state
  is the same as that loaded from the database, resulting in no net
  change here.
- Scalar attributes may not have recorded the previously set
  value when a new value was applied, if the attribute was not loaded,
  or was expired, at the time the new value was received - in these
  cases, the attribute is assumed to have a change, even if there is
  ultimately no net change against its database value. SQLAlchemy in
  most cases does not need the “old” value when a set event occurs, so
  it skips the expense of a SQL call if the old value isn’t present,
  based on the assumption that an UPDATE of the scalar value is
  usually needed, and in those few cases where it isn’t, is less
  expensive on average than issuing a defensive SELECT.
  The “old” value is fetched unconditionally upon set only if the
  attribute container has the `active_history` flag set to `True`.
  This flag is set typically for primary key attributes and scalar
  object references that are not a simple many-to-one.  To set this
  flag for any arbitrary mapped column, use the `active_history`
  argument with [column_property()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.column_property).

  Parameters:

- **instance** – mapped instance to be tested for pending changes.
- **include_collections** – Indicates if multivalued collections
  should be included in the operation.  Setting this to `False` is a
  way to detect only local-column based properties (i.e. scalar columns
  or many-to-one foreign keys) that would result in an UPDATE for this
  instance upon flush.

      method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)merge(*instance:_O*, ***, *load:bool=True*, *options:Sequence[ORMOption]|None=None*) → _O

Copy the state of a given instance into a corresponding instance
within this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

[Session.merge()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.merge) examines the primary key attributes of the
source instance, and attempts to reconcile it with an instance of the
same primary key in the session.   If not found locally, it attempts
to load the object from the database based on primary key, and if
none can be located, creates a new instance.  The state of each
attribute on the source instance is then copied to the target
instance.  The resulting target instance is then returned by the
method; the original source instance is left unmodified, and
un-associated with the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) if not already.

This operation cascades to associated instances if the association is
mapped with `cascade="merge"`.

See [Merging](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#unitofwork-merging) for a detailed discussion of merging.

  Parameters:

- **instance** – Instance to be merged.
- **load** –
  Boolean, when False, [merge()](#sqlalchemy.orm.scoped_session.merge) switches into
  a “high performance” mode which causes it to forego emitting history
  events as well as all database access.  This flag is used for
  cases such as transferring graphs of objects into a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)
  from a second level cache, or to transfer just-loaded objects
  into the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) owned by a worker thread or process
  without re-querying the database.
  The `load=False` use case adds the caveat that the given
  object has to be in a “clean” state, that is, has no pending changes
  to be flushed - even if the incoming object is detached from any
  [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).   This is so that when
  the merge operation populates local attributes and
  cascades to related objects and
  collections, the values can be “stamped” onto the
  target object as is, without generating any history or attribute
  events, and without the need to reconcile the incoming data with
  any existing related objects or collections that might not
  be loaded.  The resulting objects from `load=False` are always
  produced as “clean”, so it is only appropriate that the given objects
  should be “clean” as well, else this suggests a mis-use of the
  method.
- **options** –
  optional sequence of loader options which will be
  applied to the [Session.get()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get) method when the merge
  operation loads the existing version of the object from the database.
  Added in version 1.4.24.

See also

[make_transient_to_detached()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.make_transient_to_detached) - provides for an alternative
means of “merging” a single object into the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)

     property new: Any

The set of all instances marked as ‘new’ within this `Session`.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

     property no_autoflush: Any

Return a context manager that disables autoflush.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class
on behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

e.g.:

```
with session.no_autoflush:

    some_object = SomeClass()
    session.add(some_object)
    # won't autoflush
    some_object.related_thing = session.query(SomeRelated).first()
```

Operations that proceed within the `with:` block
will not be subject to flushes occurring upon query
access.  This is useful when initializing a series
of objects which involve existing database queries,
where the uncompleted object should not yet be flushed.

    classmethod [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)object_session(*instance:object*) → [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) | None

Return the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) to which an object belongs.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This is an alias of [object_session()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.object_session).

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)query(**entities:_ColumnsClauseArgument[Any]*, ***kwargs:Any*) → [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)[Any]

Return a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object corresponding to this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Note that the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object is legacy as of
SQLAlchemy 2.0; the [select()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.select) construct is now used
to construct ORM queries.

See also

[SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial)

[ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

[Legacy Query API](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html) - legacy API doc

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)query_property(*query_cls:Type[Query[_T]]|None=None*) → [QueryPropertyDescriptor](#sqlalchemy.orm.QueryPropertyDescriptor)

return a class property which produces a legacy
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object against the class and the current
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) when called.

Legacy Feature

The [scoped_session.query_property()](#sqlalchemy.orm.scoped_session.query_property) accessor
is specific to the legacy [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object and is not
considered to be part of [2.0-style](https://docs.sqlalchemy.org/en/20/glossary.html#term-1) ORM use.

e.g.:

```
from sqlalchemy.orm import QueryPropertyDescriptor
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Session = scoped_session(sessionmaker())

class MyClass:
    query: QueryPropertyDescriptor = Session.query_property()

# after mappers are defined
result = MyClass.query.filter(MyClass.name == "foo").all()
```

Produces instances of the session’s configured query class by
default.  To override and use a custom implementation, provide
a `query_cls` callable.  The callable will be invoked with
the class’s mapper as a positional argument and a session
keyword argument.

There is no limit to the number of query properties placed on
a class.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)refresh(*instance:object*, *attribute_names:Iterable[str]|None=None*, *with_for_update:ForUpdateParameter=None*) → None

Expire and refresh attributes on the given instance.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

The selected attributes will first be expired as they would when using
[Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire); then a SELECT statement will be issued to
the database to refresh column-oriented attributes with the current
value available in the current transaction.

[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) oriented attributes will also be immediately
loaded if they were already eagerly loaded on the object, using the
same eager loading strategy that they were loaded with originally.

Added in version 1.4: - the [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method
can also refresh eagerly loaded attributes.

[relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) oriented attributes that would normally
load using the `select` (or “lazy”) loader strategy will also
load **if they are named explicitly in the attribute_names
collection**, emitting a SELECT statement for the attribute using the
`immediate` loader strategy.  If lazy-loaded relationships are not
named in [Session.refresh.attribute_names](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh.params.attribute_names), then
they remain as “lazy loaded” attributes and are not implicitly
refreshed.

Changed in version 2.0.4: The [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method
will now refresh lazy-loaded [relationship()](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship) oriented
attributes for those which are named explicitly in the
[Session.refresh.attribute_names](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh.params.attribute_names) collection.

Tip

While the [Session.refresh()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh) method is capable of
refreshing both column and relationship oriented attributes, its
primary focus is on refreshing of local column-oriented attributes
on a single instance. For more open ended “refresh” functionality,
including the ability to refresh the attributes on many objects at
once while having explicit control over relationship loader
strategies, use the
[populate existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) feature
instead.

Note that a highly isolated transaction will return the same values as
were previously read in that same transaction, regardless of changes
in database state outside of that transaction.   Refreshing
attributes usually only makes sense at the start of a transaction
where database rows have not yet been accessed.

  Parameters:

- **attribute_names** – optional.  An iterable collection of
  string attribute names indicating a subset of attributes to
  be refreshed.
- **with_for_update** – optional boolean `True` indicating FOR UPDATE
  should be used, or may be a dictionary containing flags to
  indicate a more specific set of FOR UPDATE flags for the SELECT;
  flags should match the parameters of
  [Query.with_for_update()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.with_for_update).
  Supersedes the [Session.refresh.lockmode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.refresh.params.lockmode) parameter.

See also

[Refreshing / Expiring](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#session-expire) - introductory material

[Session.expire()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire)

[Session.expire_all()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.expire_all)

[Populate Existing](https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#orm-queryguide-populate-existing) - allows any ORM query
to refresh objects as they would be loaded normally.

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)remove() → None

Dispose of the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), if present.

This will first call [Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) method
on the current [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), which releases any existing
transactional/connection resources still being held; transactions
specifically are rolled back.  The [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is then
discarded.   Upon next usage within the same scope,
the [scoped_session](#sqlalchemy.orm.scoped_session) will produce a new
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)reset() → None

Close out the transactional resources and ORM objects used by this
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), resetting the session to its initial state.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

This method provides for same “reset-only” behavior that the
[Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) method has provided historically, where the
state of the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is reset as though the object were
brand new, and ready to be used again.
This method may then be useful for [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) objects
which set [Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only) to `False`,
so that “reset only” behavior is still available.

Added in version 2.0.22.

See also

[Closing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-closing) - detail on the semantics of
[Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) and [Session.reset()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.reset).

[Session.close()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.close) - a similar method will additionally
prevent reuse of the Session when the parameter
[Session.close_resets_only](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.close_resets_only) is set to `False`.

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)rollback() → None

Rollback the current transaction in progress.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

If no transaction is in progress, this method is a pass-through.

The method always rolls back
the topmost database transaction, discarding any nested
transactions that may be in progress.

See also

[Rolling Back](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-rollback)

[Managing Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#unitofwork-transaction)

     method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)scalar(*statement:Executable*, *params:_CoreSingleExecuteParams|None=None*, ***, *execution_options:OrmExecuteOptionsParameter={}*, *bind_arguments:_BindArguments|None=None*, ***kw:Any*) → Any

Execute a statement and return a scalar result.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Usage and parameters are the same as that of
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute); the return result is a scalar Python
value.

    method [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)scalars(*statement:Executable*, *params:_CoreAnyExecuteParams|None=None*, ***, *execution_options:OrmExecuteOptionsParameter={}*, *bind_arguments:_BindArguments|None=None*, ***kw:Any*) → [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult)[Any]

Execute a statement and return the results as scalars.

Proxied for the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) class on
behalf of the [scoped_session](#sqlalchemy.orm.scoped_session) class.

Usage and parameters are the same as that of
[Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute); the return result is a
[ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) filtering object which
will return single elements rather than [Row](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row) objects.

  Returns:

a [ScalarResult](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult) object

Added in version 1.4.24: Added [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars)

Added in version 1.4.26: Added [scoped_session.scalars()](#sqlalchemy.orm.scoped_session.scalars)

See also

[Selecting ORM Entities](https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#orm-queryguide-select-orm-entities) - contrasts the behavior
of [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute) to [Session.scalars()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.scalars)

     attribute [sqlalchemy.orm.scoped_session.](#sqlalchemy.orm.scoped_session)session_factory: [sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker)[_S]

The session_factory provided to __init__ is stored in this
attribute and may be accessed at a later time.  This can be useful when
a new non-scoped [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is needed.

     class sqlalchemy.util.ScopedRegistry

*inherits from* `typing.Generic`

A Registry that can store one or multiple instances of a single
class on the basis of a “scope” function.

The object implements `__call__` as the “getter”, so by
calling `myregistry()` the contained object is returned
for the current scope.

  Parameters:

- **createfunc** – a callable that returns a new object to be placed in the registry
- **scopefunc** – a callable that will return a key to store/retrieve an object.

| Member Name | Description |
| --- | --- |
| __init__() | Construct a newScopedRegistry. |
| clear() | Clear the current scope, if any. |
| has() | Return True if an object is present in the current scope. |
| set() | Set the value for the current scope. |

   method [sqlalchemy.util.ScopedRegistry.](#sqlalchemy.util.ScopedRegistry)__init__(*createfunc:Callable[[],_T]*, *scopefunc:Callable[[],Any]*)

Construct a new [ScopedRegistry](#sqlalchemy.util.ScopedRegistry).

  Parameters:

- **createfunc** – A creation function that will generate
  a new value for the current scope, if none is present.
- **scopefunc** – A function that returns a hashable
  token representing the current scope (such as, current
  thread identifier).

      method [sqlalchemy.util.ScopedRegistry.](#sqlalchemy.util.ScopedRegistry)clear() → None

Clear the current scope, if any.

    method [sqlalchemy.util.ScopedRegistry.](#sqlalchemy.util.ScopedRegistry)has() → bool

Return True if an object is present in the current scope.

    method [sqlalchemy.util.ScopedRegistry.](#sqlalchemy.util.ScopedRegistry)set(*obj:_T*) → None

Set the value for the current scope.

     class sqlalchemy.util.ThreadLocalRegistry

*inherits from* [sqlalchemy.util.ScopedRegistry](#sqlalchemy.util.ScopedRegistry)

A [ScopedRegistry](#sqlalchemy.util.ScopedRegistry) that uses a `threading.local()`
variable for storage.

    class sqlalchemy.orm.QueryPropertyDescriptor

*inherits from* `typing.Protocol`

Describes the type applied to a class-level
[scoped_session.query_property()](#sqlalchemy.orm.scoped_session.query_property) attribute.

Added in version 2.0.5.
