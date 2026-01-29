# SQLAlchemy 2.0 Documentation and more

# SQLAlchemy 2.0 Documentation

# Baked Queries

`baked` provides an alternative creational pattern for
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, which allows for caching of the object’s
construction and string-compilation steps.  This means that for a
particular [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) building scenario that is used more than
once, all of the Python function invocation involved in building the query
from its initial construction up through generating a SQL string will only
occur **once**, rather than for each time that query is built up and executed.

The rationale for this system is to greatly reduce Python interpreter
overhead for everything that occurs **before the SQL is emitted**.
The caching of the “baked” system does **not** in any way reduce SQL calls or
cache the **return results** from the database.  A technique that demonstrates
the caching of the SQL calls and result sets themselves is available in
[Dogpile Caching](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-caching).

Deprecated since version 1.4: SQLAlchemy 1.4 and 2.0 feature an all-new direct query
caching system that removes the need for the [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) system.
Caching is now transparently active for all Core and ORM queries with no
action taken by the user, using the system described at [SQL Compilation Caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching).

Deep Alchemy

The [sqlalchemy.ext.baked](#module-sqlalchemy.ext.baked) extension is **not for beginners**.  Using
it correctly requires a good high level understanding of how SQLAlchemy, the
database driver, and the backend database interact with each other.  This
extension presents a very specific kind of optimization that is not ordinarily
needed.  As noted above, it **does not cache queries**, only the string
formulation of the SQL itself.

## Synopsis

Usage of the baked system starts by producing a so-called “bakery”, which
represents storage for a particular series of query objects:

```
from sqlalchemy.ext import baked

bakery = baked.bakery()
```

The above “bakery” will store cached data in an LRU cache that defaults
to 200 elements, noting that an ORM query will typically contain one entry
for the ORM query as invoked, as well as one entry per database dialect for
the SQL string.

The bakery allows us to build up a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object by specifying
its construction as a series of Python callables, which are typically lambdas.
For succinct usage, it overrides the `+=` operator so that a typical
query build-up looks like the following:

```
from sqlalchemy import bindparam

def search_for_user(session, username, email=None):
    baked_query = bakery(lambda session: session.query(User))
    baked_query += lambda q: q.filter(User.name == bindparam("username"))

    baked_query += lambda q: q.order_by(User.id)

    if email:
        baked_query += lambda q: q.filter(User.email == bindparam("email"))

    result = baked_query(session).params(username=username, email=email).all()

    return result
```

Following are some observations about the above code:

1. The `baked_query` object is an instance of [BakedQuery](#sqlalchemy.ext.baked.BakedQuery).  This
  object is essentially the “builder” for a real orm [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  object, but it is not itself the *actual* [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  object.
2. The actual [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object is not built at all, until the
  very end of the function when `Result.all()` is called.
3. The steps that are added to the `baked_query` object are all expressed
  as Python functions,  typically lambdas.  The first lambda given
  to the [bakery()](#sqlalchemy.ext.baked.bakery) function receives a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) as its
  argument.  The remaining lambdas each receive a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
  as their argument.
4. In the above code, even though our application may call upon
  `search_for_user()` many times, and even though within each invocation
  we build up an entirely new [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) object,
  *all of the lambdas are only called once*.   Each lambda is **never** called
  a second time for as long as this query is cached in the bakery.
5. The caching is achieved by storing references to the **lambda objects
  themselves** in order to formulate a cache key; that is, the fact that the
  Python interpreter assigns an in-Python identity to these functions is
  what determines how to identify the query on successive runs. For
  those invocations of `search_for_user()` where the `email` parameter
  is specified, the callable `lambda q: q.filter(User.email == bindparam('email'))`
  will be part of the cache key that’s retrieved; when `email` is
  `None`, this callable is not part of the cache key.
6. Because the lambdas are all called only once, it is essential that no
  variables which may change across calls are referenced **within** the
  lambdas; instead, assuming these are values to be bound into the
  SQL string, we use [bindparam()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam) to construct named parameters,
  where we apply their actual values later using `Result.params()`.

## Performance

The baked query probably looks a little odd, a little bit awkward and
a little bit verbose.   However, the savings in
Python performance for a query which is invoked lots of times in an
application are very dramatic.   The example suite `short_selects`
demonstrated in [Performance](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-performance) illustrates a comparison
of queries which each return only one row, such as the following regular
query:

```
session = Session(bind=engine)
for id_ in random.sample(ids, n):
    session.query(Customer).filter(Customer.id == id_).one()
```

compared to the equivalent “baked” query:

```
bakery = baked.bakery()
s = Session(bind=engine)
for id_ in random.sample(ids, n):
    q = bakery(lambda s: s.query(Customer))
    q += lambda q: q.filter(Customer.id == bindparam("id"))
    q(s).params(id=id_).one()
```

The difference in Python function call count for an iteration of 10000
calls to each block are:

```
test_baked_query : test a baked query of the full entity.
                   (10000 iterations); total fn calls 1951294

test_orm_query :   test a straight ORM query of the full entity.
                   (10000 iterations); total fn calls 7900535
```

In terms of number of seconds on a powerful laptop, this comes out as:

```
test_baked_query : test a baked query of the full entity.
                   (10000 iterations); total time 2.174126 sec

test_orm_query :   test a straight ORM query of the full entity.
                   (10000 iterations); total time 7.958516 sec
```

Note that this test very intentionally features queries that only return one row.
For queries that return many rows, the performance advantage of the baked query will have
less and less of an impact, proportional to the time spent fetching rows.
It is critical to keep in mind that the **baked query feature only applies to
building the query itself, not the fetching of results**.  Using the
baked feature is by no means a guarantee to a much faster application; it is
only a potentially useful feature for those applications that have been measured
as being impacted by this particular form of overhead.

Measure twice, cut once

For background on how to profile a SQLAlchemy application, please see
the section [Performance](https://docs.sqlalchemy.org/en/20/faq/performance.html#faq-performance).  It is essential that performance
measurement techniques are used when attempting to improve the performance
of an application.

## Rationale

The “lambda” approach above is a superset of what would be a more
traditional “parameterized” approach.   Suppose we wished to build
a simple system where we build a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) just once, then
store it in a dictionary for reuse.   This is possible right now by
just building up the query, and removing its [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) by calling
`my_cached_query = query.with_session(None)`:

```
my_simple_cache = {}

def lookup(session, id_argument):
    if "my_key" not in my_simple_cache:
        query = session.query(Model).filter(Model.id == bindparam("id"))
        my_simple_cache["my_key"] = query.with_session(None)
    else:
        query = my_simple_cache["my_key"].with_session(session)

    return query.params(id=id_argument).all()
```

The above approach gets us a very minimal performance benefit.
By reusing a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query), we save on the Python work within
the `session.query(Model)` constructor as well as calling upon
`filter(Model.id == bindparam('id'))`, which will skip for us the building
up of the Core expression as well as sending it to [Query.filter()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter).
However, the approach still regenerates the full [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select)
object every time when [Query.all()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.all) is called and additionally this
brand new [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) is sent off to the string compilation step every
time, which for a simple case like the above is probably about 70% of the
overhead.

To reduce the additional overhead, we need some more specialized logic,
some way to memoize the construction of the select object and the
construction of the SQL.  There is an example of this on the wiki
in the section [BakedQuery](https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/BakedQuery),
a precursor to this feature, however in that system, we aren’t caching
the *construction* of the query.  In order to remove all the overhead,
we need to cache both the construction of the query as well as the SQL
compilation.  Let’s assume we adapted the recipe in this way
and made ourselves a method `.bake()` that pre-compiles the SQL for the
query, producing a new object that can be invoked with minimal overhead.
Our example becomes:

```
my_simple_cache = {}

def lookup(session, id_argument):
    if "my_key" not in my_simple_cache:
        query = session.query(Model).filter(Model.id == bindparam("id"))
        my_simple_cache["my_key"] = query.with_session(None).bake()
    else:
        query = my_simple_cache["my_key"].with_session(session)

    return query.params(id=id_argument).all()
```

Above, we’ve fixed the performance situation, but we still have this
string cache key to deal with.

We can use the “bakery” approach to re-frame the above in a way that
looks less unusual than the “building up lambdas” approach, and more like
a simple improvement upon the simple “reuse a query” approach:

```
bakery = baked.bakery()

def lookup(session, id_argument):
    def create_model_query(session):
        return session.query(Model).filter(Model.id == bindparam("id"))

    parameterized_query = bakery.bake(create_model_query)
    return parameterized_query(session).params(id=id_argument).all()
```

Above, we use the “baked” system in a manner that is
very similar to the simplistic “cache a query” system.  However, it
uses two fewer lines of code, does not need to manufacture a cache key of
“my_key”, and also includes the same feature as our custom “bake” function
that caches 100% of the Python invocation work from the
constructor of the query, to the filter call, to the production
of the [Select](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select) object, to the string compilation step.

From the above, if we ask ourselves, “what if lookup needs to make conditional decisions
as to the structure of the query?”, this is where hopefully it becomes apparent
why “baked” is the way it is.   Instead of a parameterized query building
off from exactly one function (which is how we thought baked might work
originally), we can build it from *any number* of functions.  Consider
our naive example, if we needed to have an additional clause in our
query on a conditional basis:

```
my_simple_cache = {}

def lookup(session, id_argument, include_frobnizzle=False):
    if include_frobnizzle:
        cache_key = "my_key_with_frobnizzle"
    else:
        cache_key = "my_key_without_frobnizzle"

    if cache_key not in my_simple_cache:
        query = session.query(Model).filter(Model.id == bindparam("id"))
        if include_frobnizzle:
            query = query.filter(Model.frobnizzle == True)

        my_simple_cache[cache_key] = query.with_session(None).bake()
    else:
        query = my_simple_cache[cache_key].with_session(session)

    return query.params(id=id_argument).all()
```

Our “simple” parameterized system must now be tasked with generating
cache keys which take into account whether or not the “include_frobnizzle”
flag was passed, as the presence of this flag means that the generated
SQL would be entirely different.   It should be apparent that as the
complexity of query building goes up, the task of caching these queries
becomes burdensome very quickly.   We can convert the above example
into a direct use of “bakery” as follows:

```
bakery = baked.bakery()

def lookup(session, id_argument, include_frobnizzle=False):
    def create_model_query(session):
        return session.query(Model).filter(Model.id == bindparam("id"))

    parameterized_query = bakery.bake(create_model_query)

    if include_frobnizzle:

        def include_frobnizzle_in_query(query):
            return query.filter(Model.frobnizzle == True)

        parameterized_query = parameterized_query.with_criteria(
            include_frobnizzle_in_query
        )

    return parameterized_query(session).params(id=id_argument).all()
```

Above, we again cache not just the query object but all the work it needs
to do in order to generate SQL.  We also no longer need to deal with
making sure we generate a cache key that accurately takes into account
all of the structural modifications we’ve made; this is now handled
automatically and without the chance of mistakes.

This code sample is a few lines shorter than the naive example, removes
the need to deal with cache keys, and has the vast performance benefits
of the full so-called “baked” feature.  But
still a little verbose!  Hence we take methods like [BakedQuery.add_criteria()](#sqlalchemy.ext.baked.BakedQuery.add_criteria)
and [BakedQuery.with_criteria()](#sqlalchemy.ext.baked.BakedQuery.with_criteria) and shorten them into operators, and
encourage (though certainly not require!) using simple lambdas, only as a
means to reduce verbosity:

```
bakery = baked.bakery()

def lookup(session, id_argument, include_frobnizzle=False):
    parameterized_query = bakery.bake(
        lambda s: s.query(Model).filter(Model.id == bindparam("id"))
    )

    if include_frobnizzle:
        parameterized_query += lambda q: q.filter(Model.frobnizzle == True)

    return parameterized_query(session).params(id=id_argument).all()
```

Where above, the approach is simpler to implement and much more similar
in code flow to what a non-cached querying function would look like,
hence making code easier to port.

The above description is essentially a summary of the design process used
to arrive at the current “baked” approach.   Starting from the
“normal” approaches, the additional issues of cache key construction and
management,  removal of all redundant Python execution, and queries built up
with conditionals needed to be addressed, leading to the final approach.

## Special Query Techniques

This section will describe some techniques for specific query situations.

### Using IN expressions

The [ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_) method in SQLAlchemy historically renders
a variable set of bound parameters based on the list of items that’s passed
to the method.   This doesn’t work for baked queries as the length of that
list can change on different calls.  To solve this problem, the
[bindparam.expanding](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam.params.expanding) parameter supports a late-rendered IN
expression that is safe to be cached inside of baked query.  The actual list
of elements is rendered at statement execution time, rather than at
statement compilation time:

```
bakery = baked.bakery()

baked_query = bakery(lambda session: session.query(User))
baked_query += lambda q: q.filter(User.name.in_(bindparam("username", expanding=True)))

result = baked_query.with_session(session).params(username=["ed", "fred"]).all()
```

See also

[bindparam.expanding](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.bindparam.params.expanding)

[ColumnOperators.in_()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.ColumnOperators.in_)

### Using Subqueries

When using [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects, it is often needed that one [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object is used to generate a subquery within another.   In the case where the
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) is currently in baked form, an interim method may be used to
retrieve the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, using the [BakedQuery.to_query()](#sqlalchemy.ext.baked.BakedQuery.to_query)
method.  This method is passed the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) or [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) that is
the argument to the lambda callable used to generate a particular step
of the baked query:

```
bakery = baked.bakery()

# a baked query that will end up being used as a subquery
my_subq = bakery(lambda s: s.query(User.id))
my_subq += lambda q: q.filter(User.id == Address.user_id)

# select a correlated subquery in the top columns list,
# we have the "session" argument, pass that
my_q = bakery(lambda s: s.query(Address.id, my_subq.to_query(s).as_scalar()))

# use a correlated subquery in some of the criteria, we have
# the "query" argument, pass that.
my_q += lambda q: q.filter(my_subq.to_query(q).exists())
```

Added in version 1.3.

### Using the before_compile event

As of SQLAlchemy 1.3.11, the use of the [QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile)
event against a particular [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) will disallow the baked query
system from caching the query, if the event hook returns a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object that is different from the one passed in.  This is so that the
[QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) hook may be invoked against a particular
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) every time it is used, to accommodate for hooks that
alter the query differently each time.    To allow a
[QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) to alter a [sqlalchemy.orm.Query()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object, but
still to allow the result to be cached, the event can be registered
passing the `bake_ok=True` flag:

```
@event.listens_for(Query, "before_compile", retval=True, bake_ok=True)
def my_event(query):
    for desc in query.column_descriptions:
        if desc["type"] is User:
            entity = desc["entity"]
            query = query.filter(entity.deleted == False)
    return query
```

The above strategy is appropriate for an event that will modify a
given [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) in exactly the same way every time, not dependent
on specific parameters or external state that changes.

Added in version 1.3.11: - added the “bake_ok” flag to the
[QueryEvents.before_compile()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.QueryEvents.before_compile) event and disallowed caching via
the “baked” extension from occurring for event handlers that
return  a new [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object if this flag is not set.

## Disabling Baked Queries Session-wide

The flag [Session.enable_baked_queries](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.enable_baked_queries) may be set to False,
causing all baked queries to not use the cache when used against that
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session):

```
session = Session(engine, enable_baked_queries=False)
```

Like all session flags, it is also accepted by factory objects like
[sessionmaker](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker) and methods like [sessionmaker.configure()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker.configure).

The immediate rationale for this flag is so that an application
which is seeing issues potentially due to cache key conflicts from user-defined
baked queries or other baked query issues can turn the behavior off, in
order to identify or eliminate baked queries as the cause of an issue.

Added in version 1.2.

## Lazy Loading Integration

Changed in version 1.4: As of SQLAlchemy 1.4, the “baked query” system is no
longer part of the relationship loading system.
The [native caching](https://docs.sqlalchemy.org/en/20/core/connections.html#sql-caching) system is used instead.

## API Documentation

| Object Name | Description |
| --- | --- |
| BakedQuery | A builder object forQueryobjects. |
| bakery | Construct a new bakery. |
| Bakery | Callable which returns aBakedQuery. |

   function sqlalchemy.ext.baked.bakery(*size=200*, *_size_alert=None*)

Construct a new bakery.

  Returns:

an instance of [Bakery](#sqlalchemy.ext.baked.Bakery)

      class sqlalchemy.ext.baked.BakedQuery

A builder object for [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) objects.

| Member Name | Description |
| --- | --- |
| add_criteria() | Add a criteria function to thisBakedQuery. |
| bakery() | Construct a new bakery. |
| for_session() | Return aResultobject for thisBakedQuery. |
| spoil() | Cancel any query caching that will occur on this BakedQuery object. |
| to_query() | Return theQueryobject for use as a subquery. |
| with_criteria() | Add a criteria function to aBakedQuerycloned from this
one. |

   method [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)add_criteria(*fn*, **args*)

Add a criteria function to this [BakedQuery](#sqlalchemy.ext.baked.BakedQuery).

This is equivalent to using the `+=` operator to
modify a [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) in-place.

    classmethod [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)bakery(*size=200*, *_size_alert=None*)

Construct a new bakery.

  Returns:

an instance of [Bakery](#sqlalchemy.ext.baked.Bakery)

      method [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)for_session(*session*)

Return a `Result` object for this
[BakedQuery](#sqlalchemy.ext.baked.BakedQuery).

This is equivalent to calling the [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) as a
Python callable, e.g. `result = my_baked_query(session)`.

    method [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)spoil(*full=False*)

Cancel any query caching that will occur on this BakedQuery object.

The BakedQuery can continue to be used normally, however additional
creational functions will not be cached; they will be called
on every invocation.

This is to support the case where a particular step in constructing
a baked query disqualifies the query from being cacheable, such
as a variant that relies upon some uncacheable value.

  Parameters:

**full** – if False, only functions added to this
[BakedQuery](#sqlalchemy.ext.baked.BakedQuery) object subsequent to the spoil step will be
non-cached; the state of the [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) up until
this point will be pulled from the cache.   If True, then the
entire [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object is built from scratch each
time, with all creational functions being called on each
invocation.

      method [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)to_query(*query_or_session*)

Return the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object for use as a subquery.

This method should be used within the lambda callable being used
to generate a step of an enclosing [BakedQuery](#sqlalchemy.ext.baked.BakedQuery).   The
parameter should normally be the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object that
is passed to the lambda:

```
sub_bq = self.bakery(lambda s: s.query(User.name))
sub_bq += lambda q: q.filter(User.id == Address.user_id).correlate(Address)

main_bq = self.bakery(lambda s: s.query(Address))
main_bq += lambda q: q.filter(sub_bq.to_query(q).exists())
```

In the case where the subquery is used in the first callable against
a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), the [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is also accepted:

```
sub_bq = self.bakery(lambda s: s.query(User.name))
sub_bq += lambda q: q.filter(User.id == Address.user_id).correlate(Address)

main_bq = self.bakery(
    lambda s: s.query(Address.id, sub_bq.to_query(q).scalar_subquery())
)
```

   Parameters:

**query_or_session** –

a [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object or a class
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) object, that is assumed to be within the context
of an enclosing [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) callable.

Added in version 1.3.

       method [sqlalchemy.ext.baked.BakedQuery.](#sqlalchemy.ext.baked.BakedQuery)with_criteria(*fn*, **args*)

Add a criteria function to a [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) cloned from this
one.

This is equivalent to using the `+` operator to
produce a new [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) with modifications.

     class sqlalchemy.ext.baked.Bakery

Callable which returns a [BakedQuery](#sqlalchemy.ext.baked.BakedQuery).

This object is returned by the class method
[BakedQuery.bakery()](#sqlalchemy.ext.baked.BakedQuery.bakery).  It exists as an object
so that the “cache” can be easily inspected.

Added in version 1.2.

     class sqlalchemy.ext.baked.Result

Invokes a [BakedQuery](#sqlalchemy.ext.baked.BakedQuery) against a [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session).

The `Result` object is where the actual [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object gets created, or retrieved from the cache,
against a target [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session), and is then invoked for results.

   method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)all()

Return all rows.

Equivalent to [Query.all()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.all).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)count()

return the ‘count’.

Equivalent to [Query.count()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.count).

Note this uses a subquery to ensure an accurate count regardless
of the structure of the original statement.

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)first()

Return the first row.

Equivalent to [Query.first()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.first).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)get(*ident*)

Retrieve an object based on identity.

Equivalent to [Query.get()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.get).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)one()

Return exactly one result or raise an exception.

Equivalent to [Query.one()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.one).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)one_or_none()

Return one or zero results, or raise an exception for multiple
rows.

Equivalent to [Query.one_or_none()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.one_or_none).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)params(**args*, ***kw*)

Specify parameters to be replaced into the string SQL statement.

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)scalar()

Return the first element of the first result or None
if no rows present.  If multiple rows are returned,
raises MultipleResultsFound.

Equivalent to [Query.scalar()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.scalar).

    method [sqlalchemy.ext.baked.Result.](#sqlalchemy.ext.baked.Result)with_post_criteria(*fn*)

Add a criteria function that will be applied post-cache.

This adds a function that will be run against the
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) object after it is retrieved from the
cache.    This currently includes **only** the
[Query.params()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.params) and [Query.execution_options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.execution_options)
methods.

Warning

`Result.with_post_criteria()`
functions are applied
to the [Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)
object **after** the query’s SQL statement
object has been retrieved from the cache.   Only
[Query.params()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.params) and
[Query.execution_options()](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.execution_options)
methods should be used.

Added in version 1.2.

---

# SQLAlchemy 2.0 Documentation

# Declarative API

## API Reference

Changed in version 1.4: The fundamental structures of the declarative
system are now part of SQLAlchemy ORM directly.   For these components
see:

- [declarative_base()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declarative_base)
- [declared_attr](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.declared_attr)
- [has_inherited_table()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.has_inherited_table)
- [synonym_for()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.synonym_for)
- [sqlalchemy.orm.as_declarative()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.as_declarative)

See [Declarative Extensions](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/index.html) for the remaining Declarative extension
classes.

---

# SQLAlchemy 2.0 Documentation

# Declarative Extensions

Extensions specific to the [Declarative](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping)
mapping API.

Changed in version 1.4: The vast majority of the Declarative extension is now
integrated into the SQLAlchemy ORM and is importable from the
`sqlalchemy.orm` namespace.  See the documentation at
[Declarative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping) for new documentation.
For an overview of the change, see [Declarative is now integrated into the ORM with new features](https://docs.sqlalchemy.org/en/20/changelog/migration_14.html#change-5508).

| Object Name | Description |
| --- | --- |
| AbstractConcreteBase | A helper class for ‘concrete’ declarative mappings. |
| ConcreteBase | A helper class for ‘concrete’ declarative mappings. |
| DeferredReflection | A helper class for construction of mappings based on
a deferred reflection step. |

   class sqlalchemy.ext.declarative.AbstractConcreteBase

*inherits from* [sqlalchemy.ext.declarative.extensions.ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase)

A helper class for ‘concrete’ declarative mappings.

[AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase) will use the [polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union)
function automatically, against all tables mapped as a subclass
to this class.   The function is called via the
`__declare_first__()` function, which is essentially
a hook for the [before_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.before_configured) event.

[AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase) applies [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) for its
immediately inheriting class, as would occur for any other
declarative mapped class. However, the [Mapper](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.Mapper) is not
mapped to any particular [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object.  Instead, it’s
mapped directly to the “polymorphic” selectable produced by
[polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union), and performs no persistence operations on its
own.  Compare to [ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase), which maps its
immediately inheriting class to an actual
[Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) that stores rows directly.

Note

The [AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase) delays the mapper creation of the
base class until all the subclasses have been defined,
as it needs to create a mapping against a selectable that will include
all subclass tables.  In order to achieve this, it waits for the
**mapper configuration event** to occur, at which point it scans
through all the configured subclasses and sets up a mapping that will
query against all subclasses at once.

While this event is normally invoked automatically, in the case of
[AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase), it may be necessary to invoke it
explicitly after **all** subclass mappings are defined, if the first
operation is to be a query against this base class. To do so, once all
the desired classes have been configured, the
[registry.configure()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry.configure) method on the [registry](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.registry)
in use can be invoked, which is available in relation to a particular
declarative base class:

```
Base.registry.configure()
```

Example:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import AbstractConcreteBase

class Base(DeclarativeBase):
    pass

class Employee(AbstractConcreteBase, Base):
    pass

class Manager(Employee):
    __tablename__ = "manager"
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    manager_data = Column(String(40))

    __mapper_args__ = {
        "polymorphic_identity": "manager",
        "concrete": True,
    }

Base.registry.configure()
```

The abstract base class is handled by declarative in a special way;
at class configuration time, it behaves like a declarative mixin
or an `__abstract__` base class.   Once classes are configured
and mappings are produced, it then gets mapped itself, but
after all of its descendants.  This is a very unique system of mapping
not found in any other SQLAlchemy API feature.

Using this approach, we can specify columns and properties
that will take place on mapped subclasses, in the way that
we normally do as in [Mixin and Custom Base Classes](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/mixins.html#declarative-mixins):

```
from sqlalchemy.ext.declarative import AbstractConcreteBase

class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)

class Employee(AbstractConcreteBase, Base):
    strict_attrs = True

    employee_id = Column(Integer, primary_key=True)

    @declared_attr
    def company_id(cls):
        return Column(ForeignKey("company.id"))

    @declared_attr
    def company(cls):
        return relationship("Company")

class Manager(Employee):
    __tablename__ = "manager"

    name = Column(String(50))
    manager_data = Column(String(40))

    __mapper_args__ = {
        "polymorphic_identity": "manager",
        "concrete": True,
    }

Base.registry.configure()
```

When we make use of our mappings however, both `Manager` and
`Employee` will have an independently usable `.company` attribute:

```
session.execute(select(Employee).filter(Employee.company.has(id=5)))
```

   Parameters:

**strict_attrs** –

when specified on the base class, “strict” attribute
mode is enabled which attempts to limit ORM mapped attributes on the
base class to only those that are immediately present, while still
preserving “polymorphic” loading behavior.

Added in version 2.0.

See also

[ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase)

[Concrete Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#concrete-inheritance)

[Abstract Concrete Classes](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#abstract-concrete-base)

     class sqlalchemy.ext.declarative.ConcreteBase

A helper class for ‘concrete’ declarative mappings.

[ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase) will use the [polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union)
function automatically, against all tables mapped as a subclass
to this class.   The function is called via the
`__declare_last__()` function, which is essentially
a hook for the [after_configured()](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.MapperEvents.after_configured) event.

[ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase) produces a mapped
table for the class itself.  Compare to [AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase),
which does not.

Example:

```
from sqlalchemy.ext.declarative import ConcreteBase

class Employee(ConcreteBase, Base):
    __tablename__ = "employee"
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "concrete": True,
    }

class Manager(Employee):
    __tablename__ = "manager"
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    manager_data = Column(String(40))
    __mapper_args__ = {
        "polymorphic_identity": "manager",
        "concrete": True,
    }
```

The name of the discriminator column used by [polymorphic_union()](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.polymorphic_union)
defaults to the name `type`.  To suit the use case of a mapping where an
actual column in a mapped table is already named `type`, the
discriminator name can be configured by setting the
`_concrete_discriminator_name` attribute:

```
class Employee(ConcreteBase, Base):
    _concrete_discriminator_name = "_concrete_discriminator"
```

Added in version 1.3.19: Added the `_concrete_discriminator_name`
attribute to [ConcreteBase](#sqlalchemy.ext.declarative.ConcreteBase) so that the
virtual discriminator column name can be customized.

Changed in version 1.4.2: The `_concrete_discriminator_name` attribute
need only be placed on the basemost class to take correct effect for
all subclasses.   An explicit error message is now raised if the
mapped column names conflict with the discriminator name, whereas
in the 1.3.x series there would be some warnings and then a non-useful
query would be generated.

See also

[AbstractConcreteBase](#sqlalchemy.ext.declarative.AbstractConcreteBase)

[Concrete Table Inheritance](https://docs.sqlalchemy.org/en/20/orm/inheritance.html#concrete-inheritance)

     class sqlalchemy.ext.declarative.DeferredReflection

A helper class for construction of mappings based on
a deferred reflection step.

Normally, declarative can be used with reflection by
setting a [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) object using autoload_with=engine
as the `__table__` attribute on a declarative class.
The caveat is that the [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) must be fully
reflected, or at the very least have a primary key column,
at the point at which a normal declarative mapping is
constructed, meaning the [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) must be available
at class declaration time.

The [DeferredReflection](#sqlalchemy.ext.declarative.DeferredReflection) mixin moves the construction
of mappers to be at a later point, after a specific
method is called which first reflects all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table)
objects created so far.   Classes can define it as such:

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeferredReflection

Base = declarative_base()

class MyClass(DeferredReflection, Base):
    __tablename__ = "mytable"
```

Above, `MyClass` is not yet mapped.   After a series of
classes have been defined in the above fashion, all tables
can be reflected and mappings created using
[prepare()](#sqlalchemy.ext.declarative.DeferredReflection.prepare):

```
engine = create_engine("someengine://...")
DeferredReflection.prepare(engine)
```

The [DeferredReflection](#sqlalchemy.ext.declarative.DeferredReflection) mixin can be applied to individual
classes, used as the base for the declarative base itself,
or used in a custom abstract class.   Using an abstract base
allows that only a subset of classes to be prepared for a
particular prepare step, which is necessary for applications
that use more than one engine.  For example, if an application
has two engines, you might use two bases, and prepare each
separately, e.g.:

```
class ReflectedOne(DeferredReflection, Base):
    __abstract__ = True

class ReflectedTwo(DeferredReflection, Base):
    __abstract__ = True

class MyClass(ReflectedOne):
    __tablename__ = "mytable"

class MyOtherClass(ReflectedOne):
    __tablename__ = "myothertable"

class YetAnotherClass(ReflectedTwo):
    __tablename__ = "yetanothertable"

# ... etc.
```

Above, the class hierarchies for `ReflectedOne` and
`ReflectedTwo` can be configured separately:

```
ReflectedOne.prepare(engine_one)
ReflectedTwo.prepare(engine_two)
```

See also

[Using DeferredReflection](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected-deferred-reflection) - in the
[Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html) section.

| Member Name | Description |
| --- | --- |
| prepare() | Reflect allTableobjects for all currentDeferredReflectionsubclasses |

   classmethod [sqlalchemy.ext.declarative.DeferredReflection.](#sqlalchemy.ext.declarative.DeferredReflection)prepare(*bind:Engine|Connection*, ***reflect_kw:Any*) → None

Reflect all [Table](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Table) objects for all current
[DeferredReflection](#sqlalchemy.ext.declarative.DeferredReflection) subclasses

  Parameters:

- **bind** –
  [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) or [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)
  instance
  ..versionchanged:: 2.0.16 a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) is also
  accepted.
- ****reflect_kw** –
  additional keyword arguments passed to
  [MetaData.reflect()](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect), such as
  [MetaData.reflect.views](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.reflect.params.views).
  Added in version 2.0.16.

---

# SQLAlchemy 2.0 Documentation

Release: 2.0.46 current release

        | Release Date: January 21, 2026

# SQLAlchemy 2.0 Documentation

### SQLAlchemy 2.0 Documentation

current release

[Home](https://docs.sqlalchemy.org/en/20/index.html)
                | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

### SQLAlchemy 2.0 Documentation

- [Overview](https://docs.sqlalchemy.org/en/20/intro.html)
- [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQLAlchemy Core](https://docs.sqlalchemy.org/en/20/core/index.html)
- [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)
- [Frequently Asked Questions](https://docs.sqlalchemy.org/en/20/faq/index.html)
- [Error Messages](https://docs.sqlalchemy.org/en/20/errors.html)
- [Changes and Migration](https://docs.sqlalchemy.org/en/20/changelog/index.html)

#### Project Versions

- [2.0.46](https://docs.sqlalchemy.org/en/20/index.html)

[Home](https://docs.sqlalchemy.org/en/20/index.html)
        | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

- **Up:** [Home](https://docs.sqlalchemy.org/en/20/index.html)
- **On this page:**

# Declarative Inheritance

See [Mapping Class Inheritance Hierarchies](https://docs.sqlalchemy.org/en/20/orm/inheritance.html) for this section.

        © [Copyright](https://docs.sqlalchemy.org/en/20/copyright.html) 2007-2026, the SQLAlchemy authors and contributors.

**flambé!** the dragon and **The Alchemist** image designs created and generously donated by [Rotem Yaari](https://github.com/vmalloc).

        Created using [Sphinx](https://www.sphinx-doc.org) 9.1.0.

    Documentation last generated: Thu 29 Jan 2026 03:06:31 PM  EST

---

# SQLAlchemy 2.0 Documentation

Release: 2.0.46 current release

        | Release Date: January 21, 2026

# SQLAlchemy 2.0 Documentation

### SQLAlchemy 2.0 Documentation

current release

[Home](https://docs.sqlalchemy.org/en/20/index.html)
                | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

### SQLAlchemy 2.0 Documentation

- [Overview](https://docs.sqlalchemy.org/en/20/intro.html)
- [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQLAlchemy Core](https://docs.sqlalchemy.org/en/20/core/index.html)
- [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)
- [Frequently Asked Questions](https://docs.sqlalchemy.org/en/20/faq/index.html)
- [Error Messages](https://docs.sqlalchemy.org/en/20/errors.html)
- [Changes and Migration](https://docs.sqlalchemy.org/en/20/changelog/index.html)

#### Project Versions

- [2.0.46](https://docs.sqlalchemy.org/en/20/index.html)

[Home](https://docs.sqlalchemy.org/en/20/index.html)
        | [Download this Documentation](https://docs.sqlalchemy.org/20/sqlalchemy_20.zip)

- **Up:** [Home](https://docs.sqlalchemy.org/en/20/index.html)
- **On this page:**

# Mixin and Custom Base Classes

See [Composing Mapped Hierarchies with Mixins](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html) for this section.

        © [Copyright](https://docs.sqlalchemy.org/en/20/copyright.html) 2007-2026, the SQLAlchemy authors and contributors.

**flambé!** the dragon and **The Alchemist** image designs created and generously donated by [Rotem Yaari](https://github.com/vmalloc).

        Created using [Sphinx](https://www.sphinx-doc.org) 9.1.0.

    Documentation last generated: Thu 29 Jan 2026 03:06:31 PM  EST

---

# SQLAlchemy 2.0 Documentation

# Configuring Relationships

This section is covered by [Defining Mapped Properties with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#orm-declarative-properties).

## Evaluation of relationship arguments

This section is moved to [Late-Evaluation of Relationship Arguments](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#orm-declarative-relationship-eval).

## Configuring Many-to-Many Relationships

This section is moved to [Using a late-evaluated form for the “secondary” argument of many-to-many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#orm-declarative-relationship-secondary-eval).

---

# SQLAlchemy 2.0 Documentation

# Table Configuration

This section has moved; see [Declarative Table Configuration](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-table-configuration).

## Using a Hybrid Approach with __table__

This section has moved; see [Declarative with Imperative Table (a.k.a. Hybrid Declarative)](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-imperative-table-configuration).

## Using Reflection with Declarative

This section has moved to [Mapping Declaratively with Reflected Tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-reflected).

---

# SQLAlchemy 2.0 Documentation

# Horizontal Sharding

Horizontal sharding support.

Defines a rudimental ‘horizontal sharding’ system which allows a Session to
distribute queries and persistence operations across multiple databases.

For a usage example, see the [Horizontal Sharding](https://docs.sqlalchemy.org/en/20/orm/examples.html#examples-sharding) example included in
the source distribution.

Deep Alchemy

The horizontal sharding extension is an advanced feature,
involving a complex statement -> database interaction as well as
use of semi-public APIs for non-trivial cases.   Simpler approaches to
referring to multiple database “shards”, most commonly using a distinct
[Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) per “shard”, should always be considered first
before using this more complex and less-production-tested system.

## API Documentation

| Object Name | Description |
| --- | --- |
| set_shard_id | a loader option for statements to apply a specific shard id to the
primary query as well as for additional relationship and column
loaders. |
| ShardedQuery | Query class used withShardedSession. |
| ShardedSession |  |

   class sqlalchemy.ext.horizontal_shard.ShardedSession

*inherits from* [sqlalchemy.orm.session.Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session)

| Member Name | Description |
| --- | --- |
| __init__() | Construct a ShardedSession. |
| connection_callable() | Provide aConnectionto use in the unit of work
flush process. |
| get_bind() | Return a “bind” to which thisSessionis bound. |

   method [sqlalchemy.ext.horizontal_shard.ShardedSession.](#sqlalchemy.ext.horizontal_shard.ShardedSession)__init__(*shard_chooser:ShardChooser,identity_chooser:Optional[IdentityChooser]=None,execute_chooser:Optional[Callable[[ORMExecuteState],Iterable[Any]]]=None,shards:Optional[Dict[str,Any]]=None,query_cls:Type[Query[_T]]=<class'sqlalchemy.ext.horizontal_shard.ShardedQuery'>,*,id_chooser:Optional[Callable[[Query[_T],Iterable[_T]],Iterable[Any]]]=None,query_chooser:Optional[Callable[[Executable],Iterable[Any]]]=None,**kwargs:Any*) → None

Construct a ShardedSession.

  Parameters:

- **shard_chooser** – A callable which, passed a Mapper, a mapped
  instance, and possibly a SQL clause, returns a shard ID.  This id
  may be based off of the attributes present within the object, or on
  some round-robin scheme. If the scheme is based on a selection, it
  should set whatever state on the instance to mark it in the future as
  participating in that shard.
- **identity_chooser** –
  A callable, passed a Mapper and primary key
  argument, which should return a list of shard ids where this
  primary key might reside.
  > Changed in version 2.0: The `identity_chooser` parameter
  > supersedes the `id_chooser` parameter.
- **execute_chooser** –
  For a given [ORMExecuteState](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.ORMExecuteState),
  returns the list of shard_ids
  where the query should be issued.  Results from all shards returned
  will be combined together into a single listing.
  Changed in version 1.4: The `execute_chooser` parameter
  supersedes the `query_chooser` parameter.
- **shards** – A dictionary of string shard names
  to [Engine](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Engine) objects.

      method [sqlalchemy.ext.horizontal_shard.ShardedSession.](#sqlalchemy.ext.horizontal_shard.ShardedSession)connection_callable(*mapper:Mapper[_T]|None=None*, *instance:Any|None=None*, *shard_id:ShardIdentifier|None=None*, ***kw:Any*) → [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection)

Provide a [Connection](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection) to use in the unit of work
flush process.

    method [sqlalchemy.ext.horizontal_shard.ShardedSession.](#sqlalchemy.ext.horizontal_shard.ShardedSession)get_bind(*mapper:_EntityBindKey[_O]|None=None*, ***, *shard_id:ShardIdentifier|None=None*, *instance:Any|None=None*, *clause:ClauseElement|None=None*, ***kw:Any*) → _SessionBind

Return a “bind” to which this [Session](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session) is bound.

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

      class sqlalchemy.ext.horizontal_shard.set_shard_id

*inherits from* `sqlalchemy.orm.ORMOption`

a loader option for statements to apply a specific shard id to the
primary query as well as for additional relationship and column
loaders.

The [set_shard_id](#sqlalchemy.ext.horizontal_shard.set_shard_id) option may be applied using
the [Executable.options()](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Executable.options) method of any executable statement:

```
stmt = (
    select(MyObject)
    .where(MyObject.name == "some name")
    .options(set_shard_id("shard1"))
)
```

Above, the statement when invoked will limit to the “shard1” shard
identifier for the primary query as well as for all relationship and
column loading strategies, including eager loaders such as
[selectinload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.selectinload), deferred column loaders like [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer),
and the lazy relationship loader [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload).

In this way, the [set_shard_id](#sqlalchemy.ext.horizontal_shard.set_shard_id) option has much wider
scope than using the “shard_id” argument within the
[Session.execute.bind_arguments](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute.params.bind_arguments) dictionary.

Added in version 2.0.0.

| Member Name | Description |
| --- | --- |
| __init__() | Construct aset_shard_idoption. |
| propagate_to_loaders | if True, indicate this option should be carried along
to “secondary” SELECT statements that occur for relationship
lazy loaders as well as attribute load / refresh operations. |

   method [sqlalchemy.ext.horizontal_shard.set_shard_id.](#sqlalchemy.ext.horizontal_shard.set_shard_id)__init__(*shard_id:str*, *propagate_to_loaders:bool=True*)

Construct a [set_shard_id](#sqlalchemy.ext.horizontal_shard.set_shard_id) option.

  Parameters:

- **shard_id** – shard identifier
- **propagate_to_loaders** – if left at its default of `True`, the
  shard option will take place for lazy loaders such as
  [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload) and [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer); if False, the option
  will not be propagated to loaded objects. Note that [defer()](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html#sqlalchemy.orm.defer)
  always limits to the shard_id of the parent row in any case, so the
  parameter only has a net effect on the behavior of the
  [lazyload()](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.lazyload) strategy.

      attribute [sqlalchemy.ext.horizontal_shard.set_shard_id.](#sqlalchemy.ext.horizontal_shard.set_shard_id)propagate_to_loaders

if True, indicate this option should be carried along
to “secondary” SELECT statements that occur for relationship
lazy loaders as well as attribute load / refresh operations.

     class sqlalchemy.ext.horizontal_shard.ShardedQuery

*inherits from* [sqlalchemy.orm.Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query)

Query class used with [ShardedSession](#sqlalchemy.ext.horizontal_shard.ShardedSession).

Legacy Feature

The [ShardedQuery](#sqlalchemy.ext.horizontal_shard.ShardedQuery) is a subclass of the legacy
[Query](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query) class.   The [ShardedSession](#sqlalchemy.ext.horizontal_shard.ShardedSession) now supports
2.0 style execution via the `ShardedSession.execute()` method.

| Member Name | Description |
| --- | --- |
| set_shard() | Return a new query, limited to a single shard ID. |

   method [sqlalchemy.ext.horizontal_shard.ShardedQuery.](#sqlalchemy.ext.horizontal_shard.ShardedQuery)set_shard(*shard_id:str*) → Self

Return a new query, limited to a single shard ID.

All subsequent operations with the returned query will
be against the single shard regardless of other state.

The shard_id can be passed for a 2.0 style execution to the
bind_arguments dictionary of [Session.execute()](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.execute):

```
results = session.execute(stmt, bind_arguments={"shard_id": "my_shard"})
```
