# Using sequelize in AWS Lambda and more

# Using sequelize in AWS Lambda

> AWS Lambda is a serverless computing service that allows customers

Version: v6 - stable

[AWS Lambda](https://aws.amazon.com/lambda/) is a serverless computing service that allows customers
to run code without having to worry about the underlying servers. Using `sequelize` in AWS Lambda
can be tricky if certain concepts are not properly understood and an appropriate configuration is
not used. This guide seeks to clarify some of these concepts so users of the library can properly
configure `sequelize` for AWS Lambda and troubleshoot issues.

## TL;DR​

If you just want to learn how to properly configure `sequelize` [connection pooling](https://sequelize.org/docs/v6/other-topics/connection-pool/) for AWS Lambda, all you need to know is that
`sequelize` connection pooling does not get along well with AWS Lambda's Node.js runtime and it ends
up causing more problems than it solves. Therefore, the most appropriate configuration is to **use
pooling within the same invocation** and **avoid pooling across invocations** (i.e. close all
connections at the end):

```
const { Sequelize } = require("sequelize");let sequelize = null;async function loadSequelize() {  const sequelize = new Sequelize(/* (...) */, {    // (...)    pool: {      /*       * Lambda functions process one request at a time but your code may issue multiple queries       * concurrently. Be wary that `sequelize` has methods that issue 2 queries concurrently       * (e.g. `Model.findAndCountAll()`). Using a value higher than 1 allows concurrent queries to       * be executed in parallel rather than serialized. Careful with executing too many queries in       * parallel per Lambda function execution since that can bring down your database with an       * excessive number of connections.       *       * Ideally you want to choose a `max` number where this holds true:       * max * EXPECTED_MAX_CONCURRENT_LAMBDA_INVOCATIONS < MAX_ALLOWED_DATABASE_CONNECTIONS * 0.8       */      max: 2,      /*       * Set this value to 0 so connection pool eviction logic eventually cleans up all connections       * in the event of a Lambda function timeout.       */      min: 0,      /*       * Set this value to 0 so connections are eligible for cleanup immediately after they're       * returned to the pool.       */      idle: 0,      // Choose a small enough value that fails fast if a connection takes too long to be established.      acquire: 3000,      /*       * Ensures the connection pool attempts to be cleaned up automatically on the next Lambda       * function invocation, if the previous invocation timed out.       */      evict: CURRENT_LAMBDA_FUNCTION_TIMEOUT    }  });  // or `sequelize.sync()`  await sequelize.authenticate();  return sequelize;}module.exports.handler = async function (event, callback) {  // re-use the sequelize instance across invocations to improve performance  if (!sequelize) {    sequelize = await loadSequelize();  } else {    // restart connection pool to ensure connections are not re-used across invocations    sequelize.connectionManager.initPools();    // restore `getConnection()` if it has been overwritten by `close()`    if (sequelize.connectionManager.hasOwnProperty("getConnection")) {      delete sequelize.connectionManager.getConnection;    }  }  try {    return await doSomethingWithSequelize(sequelize);  } finally {    // close any opened connections during the invocation    // this will wait for any in-progress queries to finish before closing the connections    await sequelize.connectionManager.close();  }};
```

### Using AWS RDS Proxy​

If your are using [AWS RDS](https://aws.amazon.com/rds/) and you are using
[Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html) or a
[supported database engine](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html),
then connect to your database using [AWS RDS Proxy](https://aws.amazon.com/rds/proxy/). This will
make sure that opening/closing connections on each invocation is not an expensive operation for
your underlying database server.

---

If you want to understand why you must use sequelize this way in AWS Lambda, continue reading the
rest of this document:

## The Node.js event loop​

The [Node.js event loop](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/) is:

> what allows Node.js to perform non-blocking I/O operations — despite the fact that JavaScript is
> single-threaded —

While the event loop implementation is in C++, here's a simplified JavaScript pseudo-implementation
that illustrates how Node.js would execute a script named `index.js`:

```
// see: https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/// see: https://www.youtube.com/watch?v=P9csgxBgaZ8// see: https://www.youtube.com/watch?v=PNa9OMajw9wconst process = require('process');/* * counter of pending events * * reference counter is increased for every: * * 1. scheduled timer: `setTimeout()`, `setInterval()`, etc. * 2. scheduled immediate: `setImmediate()`. * 3. syscall of non-blocking IO: `require('net').Server.listen()`, etc. * 4. scheduled task to the thread pool: `require('fs').WriteStream.write()`, etc. * * reference counter is decreased for every: * * 1. elapsed timer * 2. executed immediate * 3. completed non-blocking IO * 4. completed thread pool task * * references can be explicitly decreased by invoking `.unref()` on some * objects like: `require('net').Socket.unref()` */let refs = 0;/* * a heap of timers, sorted by next ocurrence * * whenever `setTimeout()` or `setInterval()` is invoked, a timer gets added here */const timersHeap = /* (...) */;/* * a FIFO queue of immediates * * whenever `setImmediate()` is invoked, it gets added here */const immediates = /* (...) */;/* * a FIFO queue of next tick callbacks * * whenever `require('process').nextTick()` is invoked, the callback gets added here */const nextTickCallbacks = [];/* * a heap of Promise-related callbacks, sorted by promise constructors callbacks first, * and then resolved/rejected callbacks * * whenever a new Promise instance is created via `new Promise` or a promise resolves/rejects * the appropriate callback (if any) gets added here */const promiseCallbacksHeap = /* ... */;function execTicksAndPromises() {  while (nextTickCallbacks.length || promiseCallbacksHeap.size()) {    // execute all callbacks scheduled with `process.nextTick()`    while (nextTickCallbacks.length) {      const callback = nextTickCallbacks.shift();      callback();    }    // execute all promise-related callbacks    while (promiseCallbacksHeap.size()) {      const callback = promiseCallbacksHeap.pop();      callback();    }  }}try {  // execute index.js  require('./index');  execTicksAndPromises();  do {    // timers phase: executes all elapsed timers    getElapsedTimerCallbacks(timersHeap).forEach(callback => {      callback();      execTicksAndPromises();    });    // pending callbacks phase: executes some system operations (like `TCP errors`) that are not    //                          executed in the poll phase    getPendingCallbacks().forEach(callback => {      callback();      execTicksAndPromises();    })    // poll phase: gets completed non-blocking I/O events or thread pool tasks and invokes the    //             corresponding callbacks; if there are none and there's no pending immediates,    //             it blocks waiting for events/completed tasks for a maximum of `maxWait`    const maxWait = computeWhenNextTimerElapses(timersHeap);    pollForEventsFromKernelOrThreadPool(maxWait, immediates).forEach(callback => {      callback();      execTicksAndPromises();    });    // check phase: execute available immediates; if an immediate callback invokes `setImmediate()`    //              it will be invoked on the next event loop iteration    getImmediateCallbacks(immediates).forEach(callback => {      callback();      execTicksAndPromises();    });    // close callbacks phase: execute special `.on('close')` callbacks    getCloseCallbacks().forEach(callback => {      callback();      execTicksAndPromises();    });    if (refs === 0) {      // listeners of this event may execute code that increments `refs`      process.emit('beforeExit');    }  } while (refs > 0);} catch (err) {  if (!process.listenerCount('uncaughtException')) {    // default behavior: print stack and exit with status code 1    console.error(err.stack);    process.exit(1);  } else {    // there are listeners: emit the event and exit using `process.exitCode || 0`    process.emit('uncaughtException');    process.exit();  }}
```

## AWS Lambda function handler types in Node.js​

AWS Lambda handlers come in two flavors in Node.js:

[Non-async handlers](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html#nodejs-handler-sync)
(i.e. `callback`):

```
module.exports.handler = function (event, context, callback) {  try {    doSomething();    callback(null, 'Hello World!'); // Lambda returns "Hello World!"  } catch (err) {    // try/catch is not required, uncaught exceptions invoke `callback(err)` implicitly    callback(err); // Lambda fails with `err`  }};
```

[Async handlers](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html#nodejs-handler-async)
(i.e. use `async`/`await` or `Promise`s):

```
// async/awaitmodule.exports.handler = async function (event, context) {  try {    await doSomethingAsync();    return 'Hello World!'; // equivalent of: callback(null, "Hello World!");  } catch (err) {    // try/cath is not required, async functions always return a Promise    throw err; // equivalent of: callback(err);  }};// Promisemodule.exports.handler = function (event, context) {  /*   * must return a `Promise` to be considered an async handler   *   * an uncaught exception that prevents a `Promise` to be returned   * by the handler will "downgrade" the handler to non-async   */  return Promise.resolve()    .then(() => doSomethingAsync())    .then(() => 'Hello World!');};
```

While at first glance it seems like async VS non-async handlers are simply a code styling choice,
there is a fundamental difference between the two:

- In async handlers, a Lambda function execution finishes when the `Promise` returned by the handler
  resolves or rejects, regardless of whether the event loop is empty or not.
- In non-async handlers, a Lambda function execution finishes when one of the following conditions
  occur:
  - The event loop is empty
    ([process'beforeExit'event](https://nodejs.org/dist/latest-v12.x/docs/api/process.html#process_event_beforeexit)
    is used to detect this).
  - The `callback` argument is invoked and
    [context.callbackWaitsForEmptyEventLoop](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-context.html)
    is set to `false`.

This fundamental difference is very important to understand in order to rationalize how `sequelize`
may be affected by it. Here are a few examples to illustrate the difference:

```
// no callback invokedmodule.exports.handler = function () {  // Lambda finishes AFTER `doSomething()` is invoked  setTimeout(() => doSomething(), 1000);};// callback invokedmodule.exports.handler = function (event, context, callback) {  // Lambda finishes AFTER `doSomething()` is invoked  setTimeout(() => doSomething(), 1000);  callback(null, 'Hello World!');};// callback invoked, context.callbackWaitsForEmptyEventLoop = falsemodule.exports.handler = function (event, context, callback) {  // Lambda finishes BEFORE `doSomething()` is invoked  context.callbackWaitsForEmptyEventLoop = false;  setTimeout(() => doSomething(), 2000);  setTimeout(() => callback(null, 'Hello World!'), 1000);};// async/awaitmodule.exports.handler = async function () {  // Lambda finishes BEFORE `doSomething()` is invoked  setTimeout(() => doSomething(), 1000);  return 'Hello World!';};// Promisemodule.exports.handler = function () {  // Lambda finishes BEFORE `doSomething()` is invoked  setTimeout(() => doSomething(), 1000);  return Promise.resolve('Hello World!');};
```

## AWS Lambda execution environments (i.e. containers)​

AWS Lambda function handlers are invoked by built-in or custom
[runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html) which run in
execution environments (i.e. containers) that
[may or may not be re-used](https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/)
across invocations. Containers can only process
[one request at a time](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html).
Concurrent invocations of a Lambda function means that a container instance will be created for each
concurrent request.

In practice, this means that Lambda functions should be designed to be stateless but developers can
use state for caching purposes:

```
let sequelize = null;module.exports.handler = async function () {  /*   * sequelize will already be loaded if the container is re-used   *   * containers are never re-used when a Lambda function's code change   *   * while the time elapsed between Lambda invocations is used as a factor to determine whether   * a container is re-used, no assumptions should be made of when a container is actually re-used   *   * AWS does not publicly document the rules of container re-use "by design" since containers   * can be recycled in response to internal AWS Lambda events (e.g. a Lambda function container   * may be recycled even if the function is constanly invoked)   */  if (!sequelize) {    sequelize = await loadSequelize();  }  return await doSomethingWithSequelize(sequelize);};
```

When a Lambda function doesn't wait for the event loop to be empty and a container is re-used,
the event loop will be "paused" until the next invocation occurs. For example:

```
let counter = 0;module.exports.handler = function (event, context, callback) {  /*   * The first invocation (i.e. container initialized) will:   * - log:   *   - Fast timeout invoked. Request id: 00000000-0000-0000-0000-000000000000 | Elapsed ms: 5XX   * - return: 1   *   * Wait 3 seconds and invoke the Lambda again. The invocation (i.e. container re-used) will:   * - log:   *   - Slow timeout invoked. Request id: 00000000-0000-0000-0000-000000000000 | Elapsed ms: 3XXX   *   - Fast timeout invoked. Request id: 11111111-1111-1111-1111-111111111111 | Elapsed ms: 5XX   * - return: 3   */  const now = Date.now();  context.callbackWaitsForEmptyEventLoop = false;  setTimeout(() => {    console.log(      'Slow timeout invoked. Request id:',      context.awsRequestId,      '| Elapsed ms:',      Date.now() - now,    );    counter++;  }, 1000);  setTimeout(() => {    console.log(      'Fast timeout invoked. Request id:',      context.awsRequestId,      '| Elapsed ms:',      Date.now() - now,    );    counter++;    callback(null, counter);  }, 500);};
```

## Sequelize connection pooling in AWS Lambda​

`sequelize` uses connection pooling for optimizing usage of database connections. The connection
pool used by `sequelize` is implemented using `setTimeout()` callbacks (which are processed by the
Node.js event loop).

Given the fact that AWS Lambda containers process one request at a time, one would be tempted to
configure `sequelize` as follows:

```
const { Sequelize } = require('sequelize');const sequelize = new Sequelize(/* (...) */, {  // (...)  pool: { min: 1, max: 1 }});
```

This configuration prevents Lambda containers from overwhelming the database server with an
excessive number of connections (since each container takes at most 1 connection). It also makes
sure that the container's connection is not garbage collected when idle so the connection does not
need to be re-established when the Lambda container is re-used. Unfortunately, this configuration
presents a set of issues:

1. Lambdas that wait for the event loop to be empty will always time out. `sequelize` connection
  pools schedule a `setTimeout` every
  [options.pool.evict](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-constructor-constructor)
  ms until **all idle connections have been closed**. However, since `min` is set to `1`, there
  will always be at least one idle connection in the pool, resulting in an infinite event loop.
2. Some operations like
  [Model.findAndCountAll()](https://sequelize.org/api/v6/class/src/model.js~model#static-method-findAndCountAll)
  execute multiple queries asynchronously (e.g.
  [Model.count()](https://sequelize.org/api/v6/class/src/model.js~model#static-method-count) and
  [Model.findAll()](https://sequelize.org/api/v6/class/src/model.js~model#static-method-findAll)). Using a maximum of
  one connection forces the queries to be executed serially (rather than in parallel using two
  connections). While this may be an acceptable performance compromise in order to
  maintain a manageable number of database connections, long running queries may result in
  [ConnectionAcquireTimeoutError](https://sequelize.org/api/v6/class/src/errors/connection/connection-acquire-timeout-error.js~ConnectionAcquireTimeoutError.html)
  if a query takes more than the default or configured
  [options.pool.acquire](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-constructor-constructor)
  timeout to complete. This is because the serialized query will be stuck waiting on the pool until
  the connection used by the other query is released.
3. If the AWS Lambda function times out (i.e. the configured AWS Lambda timeout is exceeded), the
  Node.js event loop will be "paused" regardless of its state. This can cause race conditions that
  result in connection errors. For example, you may encounter situations where a very expensive
  query causes a Lambda function to time out, the event loop is "paused" before the expensive query
  finishes and the connection is released back to the pool, and subsequent Lambda invocations fail
  with a `ConnectionAcquireTimeoutError` if the container is re-used and the connection has not
  been returned after `options.pool.acquire` ms.

You can attempt to mitigate issue **#2** by using `{ min: 1, max: 2 }`. However, this will still
suffer from issues **#1** and **#3** whilst introducing additional ones:

1. Race conditions may occur where the even loop "pauses" before a connection pool eviction callback
  executes or more than `options.pool.evict` time elapses between Lambda invocations. This can
  result in timeout errors, handshake errors, and other connection-related errors.
2. If you use an operation like `Model.findAndCountAll()` and either the underlying `Model.count()`
  or `Model.findAll()` queries fail, you won't be able to ensure that the other query has finished
  executing (and the connection is put back into the pool) before the Lambda function execution
  finishes and the event loop is "paused". This can leave connections in a stale state which can
  result in prematurely closed TCP connections and other connection-related errors.

Using `{ min: 2, max: 2 }` mitigates additional issue **#1**. However, the configuration still
suffers from all the other issues (original **#1**, **#3**, and additional **#2**).

### Detailed race condition example​

In order to make sense of the example, you'll need a bit more context of how certain parts of
Lambda and `sequelize` are implemented.

The built-in AWS Lambda runtime for `nodejs.12x` is implemented in Node.js. You can access the
entire source code of the runtime by reading the contents of `/var/runtime/` inside a Node.js Lambda
function. The relevant subset of the code is as follows:

**runtime/Runtime.js**

```
class Runtime {  // (...)  // each iteration is executed in the event loop `check` phase  scheduleIteration() {    setImmediate(() => this.handleOnce().then(/* (...) */));  }  async handleOnce() {    // get next invocation. see: https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html#runtimes-api-next    let { bodyJson, headers } = await this.client.nextInvocation();    // prepare `context` handler parameter    let invokeContext = new InvokeContext(headers);    invokeContext.updateLoggingContext();    // prepare `callback` handler parameter    let [callback, callbackContext] = CallbackContext.build(      this.client,      invokeContext.invokeId,      this.scheduleIteration.bind(this),    );    try {      // this listener is subscribed to process.on('beforeExit')      // so that when when `context.callbackWaitsForEmptyEventLoop === true`      // the Lambda execution finishes after the event loop is empty      this._setDefaultExitListener(invokeContext.invokeId);      // execute handler      const result = this.handler(        JSON.parse(bodyJson),        invokeContext.attachEnvironmentData(callbackContext),        callback,      );      // finish the execution if the handler is async      if (_isPromise(result)) {        result.then(callbackContext.succeed, callbackContext.fail).catch(callbackContext.fail);      }    } catch (err) {      callback(err);    }  }}
```

The runtime schedules an iteration at the end of the initialization code:

**runtime/index.js**

```
// (...)new Runtime(client, handler, errorCallbacks).scheduleIteration();
```

All SQL queries invoked by a Lambda handler using `sequelize` are ultimately executed using
[Sequelize.prototype.query()](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-method-query).
This method is responsible for obtaining a connection from the pool, executing the query, and
releasing the connection back to the pool when the query completes. The following snippet shows
a simplification of the method's logic for queries without transactions:

**sequelize.js**

```
class Sequelize {  // (...)  query(sql, options) {    // (...)    const connection = await this.connectionManager.getConnection(options);    const query = new this.dialect.Query(connection, this, options);    try {      return await query.run(sql, bindParameters);    } finally {      await this.connectionManager.releaseConnection(connection);    }  }}
```

The field `this.connectionManager` is an instance of a dialect-specific `ConnectionManager` class.
All dialect-specific managers inherit from an abstract `ConnectionManager` class which initializes
the connection pool and configures it to invoke the dialect-specific class' `connect()` method
everytime a new connection needs to be created. The following snippet shows a simplification of the
`mysql` dialect `connect()` method:

**mysql/connection-manager.js**

```
class ConnectionManager {  // (...)  async connect(config) {    // (...)    return await new Promise((resolve, reject) => {      // uses mysql2's `new Connection()`      const connection = this.lib.createConnection(connectionConfig);      const errorHandler = e => {        connection.removeListener('connect', connectHandler);        connection.removeListener('error', connectHandler);        reject(e);      };      const connectHandler = () => {        connection.removeListener('error', errorHandler);        resolve(connection);      };      connection.on('error', errorHandler);      connection.once('connect', connectHandler);    });  }}
```

The field `this.lib` refers to [mysql2](https://www.npmjs.com/package/mysql2) and the function
`createConnection()` creates a connection by creating an instance of a `Connection` class. The
relevant subset of this class is as follows:

**mysql2/connection.js**

```
class Connection extends EventEmitter {  constructor(opts) {    // (...)    // create Socket    this.stream = /* (...) */;    // when data is received, clear timeout    this.stream.on('data', data => {      if (this.connectTimeout) {        Timers.clearTimeout(this.connectTimeout);        this.connectTimeout = null;      }      this.packetParser.execute(data);    });    // (...)    // when handshake is completed, emit the 'connect' event    handshakeCommand.on('end', () => {      this.emit('connect', handshakeCommand.handshake);    });    // set a timeout to trigger if no data is received on the socket    if (this.config.connectTimeout) {      const timeoutHandler = this._handleTimeoutError.bind(this);      this.connectTimeout = Timers.setTimeout(        timeoutHandler,        this.config.connectTimeout      );    }  }  // (...)  _handleTimeoutError() {    if (this.connectTimeout) {      Timers.clearTimeout(this.connectTimeout);      this.connectTimeout = null;    }    this.stream.destroy && this.stream.destroy();    const err = new Error('connect ETIMEDOUT');    err.errorno = 'ETIMEDOUT';    err.code = 'ETIMEDOUT';    err.syscall = 'connect';    // this will emit the 'error' event    this._handleNetworkError(err);  }}
```

Based on the previous code, the following sequence of events shows how a connection pooling
race condition with `{ min: 1, max: 1 }` can result with in a `ETIMEDOUT` error:

1. A Lambda invocation is received (new container):
  1. The event loop enters the `check` phase and `runtime/Runtime.js`'s `handleOnce()` method is
    invoked.
    1. The `handleOnce()` method invokes `await this.client.nextInvocation()` and waits.
  2. The event loop skips the `timers` phase since there no pending timers.
  3. The event loop enters the `poll` phase and the `handleOnce()` method continues.
  4. The Lambda handler is invoked.
  5. The Lambda handler invokes `Model.count()` which invokes `sequelize.js`'s `query()` which
    invokes `connectionManager.getConnection()`.
  6. The connection pool initializes a `setTimeout(..., config.pool.acquire)` for `Model.count()`
    and invokes `mysql/connection-manager.js`'s `connect()` to create a new connection.
  7. `mysql2/connection.js` creates the TCP socket and initializes a `setTimeout()` for failing
    the connection with `ETIMEDOUT`.
  8. The promise returned by the handler rejects (for reasons not detailed here) so the Lambda
    function execution finishes and the Node.js event loop is "paused".
2. Enough time elapses between invocations so that:
  1. `config.pool.acquire` timer elapses.
  2. `mysql2` connection timer has not elapsed yet but has almost elapsed (i.e. race condition).
3. A second Lambda invocation is received (container re-used):
  1. The event loop is "resumed".
  2. The event loop enters the `check` phase and `runtime/Runtime.js`'s `handleOnce()` method is
    invoked.
  3. The event loop enters the `timers` phase and the `config.pool.acquire` timer elapses, causing
    the previous invocation's `Model.count()` promise to reject with
    `ConnectionAcquireTimeoutError`.
  4. The event loop enters the `poll` phase and the `handleOnce()` method continues.
  5. The Lambda handler is invoked.
  6. The Lambda handler invokes `Model.count()` which invokes `sequelize.js`'s `query()` which
    invokes `connectionManager.getConnection()`.
  7. The connection pool initializes a `setTimeout(..., config.pool.acquire)` for `Model.count()`
    and since `{ max : 1 }` it waits for the pending `connect()` promise to complete.
  8. The event loop skips the `check` phase since there are no pending immediates.
  9. **Race condition:** The event loop enters the `timers` phase and the `mysql2` connection
    timeout elapses, resulting in a `ETIMEDOUT` error that is emitted using
    `connection.emit('error')`.
  10. The emitted event rejects the promise in `mysql/connection-manager.js`'s `connect()` which
    in turn forwards the rejected promise to the `Model.count()` query's promise.
  11. The lambda function fails with an `ETIMEDOUT` error.

---

# Connection Pool

> If you're connecting to the database from a single process, you should create only one Sequelize instance. Sequelize will set up a connection pool on initialization. This connection pool can be configured through the constructor's options parameter (using options.pool), as is shown in the following example:

Version: v6 - stable

If you're connecting to the database from a single process, you should create only one Sequelize instance. Sequelize will set up a connection pool on initialization. This connection pool can be configured through the constructor's `options` parameter (using `options.pool`), as is shown in the following example:

```
const sequelize = new Sequelize(/* ... */, {  // ...  pool: {    max: 5,    min: 0,    acquire: 30000,    idle: 10000  }});
```

Learn more in the [API Reference for the Sequelize constructor](https://sequelize.org/api/v6/class/src/sequelize.js~sequelize#instance-constructor-constructor). If you're connecting to the database from multiple processes, you'll have to create one instance per process, but each instance should have a maximum connection pool size of such that the total maximum size is respected. For example, if you want a max connection pool size of 90 and you have three processes, the Sequelize instance of each process should have a max connection pool size of 30.

---

# Constraints & Circularities

> Adding constraints between tables means that tables must be created in the database in a certain order, when using sequelize.sync. If Task has a reference to User, the User table must be created before the Task table can be created. This can sometimes lead to circular references, where Sequelize cannot find an order in which to sync. Imagine a scenario of documents and versions. A document can have multiple versions, and for convenience, a document has a reference to its current version.

Version: v6 - stable

Adding constraints between tables means that tables must be created in the database in a certain order, when using `sequelize.sync`. If `Task` has a reference to `User`, the `User` table must be created before the `Task` table can be created. This can sometimes lead to circular references, where Sequelize cannot find an order in which to sync. Imagine a scenario of documents and versions. A document can have multiple versions, and for convenience, a document has a reference to its current version.

```
const { Sequelize, Model, DataTypes } = require('sequelize');class Document extends Model {}Document.init(  {    author: DataTypes.STRING,  },  { sequelize, modelName: 'document' },);class Version extends Model {}Version.init(  {    timestamp: DataTypes.DATE,  },  { sequelize, modelName: 'version' },);Document.hasMany(Version); // This adds documentId attribute to versionDocument.belongsTo(Version, {  as: 'Current',  foreignKey: 'currentVersionId',}); // This adds currentVersionId attribute to document
```

However, unfortunately the code above will result in the following error:

```
Cyclic dependency found. documents is dependent of itself. Dependency chain: documents -> versions => documents
```

In order to alleviate that, we can pass `constraints: false` to one of the associations:

```
Document.hasMany(Version);Document.belongsTo(Version, {  as: 'Current',  foreignKey: 'currentVersionId',  constraints: false,});
```

Which will allow us to sync the tables correctly:

```
CREATE TABLE IF NOT EXISTS "documents" (  "id" SERIAL,  "author" VARCHAR(255),  "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "currentVersionId" INTEGER,  PRIMARY KEY ("id"));CREATE TABLE IF NOT EXISTS "versions" (  "id" SERIAL,  "timestamp" TIMESTAMP WITH TIME ZONE,  "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL,  "documentId" INTEGER REFERENCES "documents" ("id") ON DELETE  SET    NULL ON UPDATE CASCADE,    PRIMARY KEY ("id"));
```

## Enforcing a foreign key reference without constraints​

Sometimes you may want to reference another table, without adding any constraints, or associations. In that case you can manually add the reference attributes to your schema definition, and mark the relations between them.

```
class Trainer extends Model {}Trainer.init(  {    firstName: Sequelize.STRING,    lastName: Sequelize.STRING,  },  { sequelize, modelName: 'trainer' },);// Series will have a trainerId = Trainer.id foreign reference key// after we call Trainer.hasMany(series)class Series extends Model {}Series.init(  {    title: Sequelize.STRING,    subTitle: Sequelize.STRING,    description: Sequelize.TEXT,    // Set FK relationship (hasMany) with `Trainer`    trainerId: {      type: DataTypes.INTEGER,      references: {        model: Trainer,        key: 'id',      },    },  },  { sequelize, modelName: 'series' },);// Video will have seriesId = Series.id foreign reference key// after we call Series.hasOne(Video)class Video extends Model {}Video.init(  {    title: Sequelize.STRING,    sequence: Sequelize.INTEGER,    description: Sequelize.TEXT,    // set relationship (hasOne) with `Series`    seriesId: {      type: DataTypes.INTEGER,      references: {        model: Series, // Can be both a string representing the table name or a Sequelize model        key: 'id',      },    },  },  { sequelize, modelName: 'video' },);Series.hasOne(Video);Trainer.hasMany(Series);
```

---

# Dialect

> Underlying Connector Libraries

Version: v6 - stable

## Underlying Connector Libraries​

### MySQL​

The underlying connector library used by Sequelize for MySQL is the [mysql2](https://www.npmjs.com/package/mysql2) npm package (version 1.5.2 or higher).

You can provide custom options to it using the `dialectOptions` in the Sequelize constructor:

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'mysql',  dialectOptions: {    // Your mysql2 options here  },});
```

`dialectOptions` are passed directly to the MySQL connection constructor. A full list of options can be found in the [MySQL docs](https://www.npmjs.com/package/mysql#connection-options).

### MariaDB​

The underlying connector library used by Sequelize for MariaDB is the [mariadb](https://www.npmjs.com/package/mariadb) npm package.

You can provide custom options to it using the `dialectOptions` in the Sequelize constructor:

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'mariadb',  dialectOptions: {    // Your mariadb options here    // connectTimeout: 1000  },});
```

`dialectOptions` are passed directly to the MariaDB connection constructor. A full list of options can be found in the [MariaDB docs](https://mariadb.com/kb/en/nodejs-connection-options/).

### SQLite​

The underlying connector library used by Sequelize for SQLite is the [sqlite3](https://www.npmjs.com/package/sqlite3) npm package (version 4.0.0 or above).
  Due to security vulnerabilities with sqlite3@^4 it is recommended to use the [@vscode/sqlite3](https://www.npmjs.com/package/@vscode/sqlite3) fork if updating to sqlite3@^5.0.3 is not possible.

You specify the storage file in the Sequelize constructor with the `storage` option (use `:memory:` for an in-memory SQLite instance).

You can provide custom options to it using the `dialectOptions` in the Sequelize constructor:

```
import { Sequelize } from 'sequelize';import SQLite from 'sqlite3';const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'sqlite',  storage: 'path/to/database.sqlite', // or ':memory:'  dialectOptions: {    // Your sqlite3 options here    // for instance, this is how you can configure the database opening mode:    mode: SQLite.OPEN_READWRITE | SQLite.OPEN_CREATE | SQLite.OPEN_FULLMUTEX,  },});
```

The following fields may be passed to SQLite `dialectOptions`:

- `mode`: Set the opening mode for the SQLite connection. Potential values are provided by the `sqlite3` package,
  and can include `SQLite.OPEN_READONLY`, `SQLite.OPEN_READWRITE`, or `SQLite.OPEN_CREATE`.
    See [sqlite3's API reference](https://github.com/TryGhost/node-sqlite3/wiki/API) and the [SQLite C interface documentation](https://www.sqlite.org/c3ref/open.html) for more details.

### PostgreSQL​

The underlying connector library used by Sequelize for PostgreSQL is the [pg](https://www.npmjs.com/package/pg) package (for Node 10 & 12, use pg version 7.0.0 or above. For Node 14 and above you need to use pg version 8.2.x or above, as per [the pg documentation](https://node-postgres.com/#version-compatibility)). The module [pg-hstore](https://www.npmjs.com/package/pg-hstore) is also necessary.

You can provide custom options to it using the `dialectOptions` in the Sequelize constructor:

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'postgres',  dialectOptions: {    // Your pg options here  },});
```

The following fields may be passed to Postgres `dialectOptions`:

- `application_name`: Name of application in pg_stat_activity. See the [Postgres docs](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-APPLICATION-NAME) for details.
- `ssl`: SSL options. See the [pgdocs](https://node-postgres.com/features/ssl) for details.
- `client_encoding`: // Setting 'auto' determines locale based on the client LC_CTYPE environment variable. See the [Postgres docs](https://www.postgresql.org/docs/current/multibyte.html) for details.
- `keepAlive`: Boolean to enable TCP KeepAlive. See the [pgchangelog](https://github.com/brianc/node-postgres/blob/master/CHANGELOG.md#v600) for details.
- `statement_timeout`: Times out queries after a set time in milliseconds. Added in pg v7.3. See the [Postgres docs](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-STATEMENT-TIMEOUT) for details.
- `idle_in_transaction_session_timeout`: Terminate any session with an open transaction that has been idle for longer than the specified duration in milliseconds. See the [Postgres docs](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) for details.

To connect over a unix domain socket, specify the path to the socket directory in the `host` option. The socket path must start with `/`.

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'postgres',  host: '/path/to/socket_directory',});
```

The default `client_min_messages` config in sequelize is `WARNING`.

### Redshift​

Most configuration is same as PostgreSQL above.

Redshift doesn't support `client_min_messages`, 'ignore' is needed to skip the configuration:

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'postgres',  dialectOptions: {    // Your pg options here    // ...    clientMinMessages: 'ignore', // case insensitive  },});
```

### Microsoft SQL Server (MSSQL)​

The underlying connector library used by Sequelize for MSSQL is the [tedious](https://www.npmjs.com/package/tedious) npm package (version 6.0.0 or above).

You can provide custom options to it using `dialectOptions.options` in the Sequelize constructor:

```
const sequelize = new Sequelize('database', 'username', 'password', {  dialect: 'mssql',  dialectOptions: {    // Observe the need for this nested `options` field for MSSQL    options: {      // Your tedious options here      useUTC: false,      dateFirst: 1,    },  },});
```

A full list of options can be found in the [tedious docs](https://tediousjs.github.io/tedious/api-connection.html#function_newConnection).

#### MSSQL Domain Account​

In order to connect with a domain account, use the following format.

```
const sequelize = new Sequelize('database', null, null, {  dialect: 'mssql',  dialectOptions: {    authentication: {      type: 'ntlm',      options: {        domain: 'yourDomain',        userName: 'username',        password: 'password',      },    },    options: {      instanceName: 'SQLEXPRESS',    },  },});
```

### Snowflake (Experimental)​

The underlying connector library used by Sequelize for Snowflake is the [snowflake-sdk](https://www.npmjs.com/package/snowflake-sdk) npm package.

In order to connect with an account, use the following format:

```
const sequelize = new Sequelize('database', null, null, {  dialect: 'snowflake',  dialectOptions: {    // put your snowflake account here,    account: 'myAccount', // my-app.us-east-1    // below option should be optional    role: 'myRole',    warehouse: 'myWarehouse',    schema: 'mySchema',  },  // same as other dialect  username: 'myUserName',  password: 'myPassword',  database: 'myDatabaseName',});
```

**NOTE** There is no test sandbox provided so the snowflake integration test is not part of the pipeline. Also it is difficult for core team to triage and debug. This dialect needs to be maintained by the snowflake user/community for now.

For running integration test:

```
SEQ_ACCOUNT=myAccount SEQ_USER=myUser SEQ_PW=myPassword SEQ_ROLE=myRole SEQ_DB=myDatabaseName SEQ_SCHEMA=mySchema SEQ_WH=myWareHouse npm run test-integration-snowflake
```

### Oracle Database​

The underlying connector library used by Sequelize for Oracle is the [node-oracledb](https://www.npmjs.com/package/oracledb) package.
  See [Releases](https://sequelize.org/releases/#oracle-database-support-table) to see which versions of Oracle Database & node-oracledb are supported.

node-oracledb needs [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html) to work. You can use the node-oracledb [quick start](https://oracle.github.io/node-oracledb/INSTALL.html#quickstart) link for installations.

Below is a Sequelize constructor with parameters related to Oracle Database.

```
const sequelize = new Sequelize('servicename', 'username', 'password', {  dialect: 'oracle',  host: 'hostname',  port: 'port number', //optional});
```

The default port number for Oracle database is 1521.

Sequelize also lets you pass credentials in URL format:

```
const sequelize = new Sequelize('oracle://user:pass@hostname:port/servicename');
```

You can pass an Easy Connect String, a Net Service Name, or a Connect Descriptor to the Sequelize constructor using `dialectOptions.connectString`:

```
const sequelize = new Sequelize({  dialect: 'oracle',  username: 'user',  password: 'password',  dialectOptions: {    connectString: 'inst1',  },});
```

Note that the `database`, `host` and `port` will be overriden and the values in connectString will be used for authentication.

Please refer to [Connect String](https://node-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html#connectionstrings) for more about connect strings.

## Data type: TIMESTAMP WITHOUT TIME ZONE - PostgreSQL only​

If you are working with the PostgreSQL `TIMESTAMP WITHOUT TIME ZONE` and you need to parse it to a different timezone, please use the pg library's own parser:

```
require('pg').types.setTypeParser(1114, stringValue => {  return new Date(stringValue + '+0000');  // e.g., UTC offset. Use any offset that you would like.});
```

## Data type: ARRAY(ENUM) - PostgreSQL only​

Array(Enum) type requireS special treatment. Whenever Sequelize will talk to the database, it has to typecast array values with ENUM name.

So this enum name must follow this pattern `enum_<table_name>_<col_name>`. If you are using `sync` then correct name will automatically be generated.

## Table Hints - MSSQL only​

The `tableHint` option can be used to define a table hint. The hint must be a value from `TableHints` and should only be used when absolutely necessary. Only a single table hint is currently supported per query.

Table hints override the default behavior of MSSQL query optimizer by specifying certain options. They only affect the table or view referenced in that clause.

```
const { TableHints } = require('sequelize');Project.findAll({  // adding the table hint NOLOCK  tableHint: TableHints.NOLOCK,  // this will generate the SQL 'WITH (NOLOCK)'});
```

## Index Hints - MySQL/MariaDB only​

The `indexHints` option can be used to define index hints. The hint type must be a value from `IndexHints` and the values should reference existing indexes.

Index hints [override the default behavior of the MySQL query optimizer](https://dev.mysql.com/doc/refman/5.7/en/index-hints.html).

```
const { IndexHints } = require('sequelize');Project.findAll({  indexHints: [{ type: IndexHints.USE, values: ['index_project_on_name'] }],  where: {    id: {      [Op.gt]: 623,    },    name: {      [Op.like]: 'Foo %',    },  },});
```

The above will generate a MySQL query that looks like this:

```
SELECT * FROM Project USE INDEX (index_project_on_name) WHERE name LIKE 'FOO %' AND id > 623;
```

`Sequelize.IndexHints` includes `USE`, `FORCE`, and `IGNORE`.

See [Issue #9421](https://github.com/sequelize/sequelize/issues/9421) for the original API proposal.

## Engines - MySQL/MariaDB only​

The default engine for a model is InnoDB.

You can change the engine for a model with the `engine` option (e.g., to MyISAM):

```
const Person = sequelize.define(  'person',  {    /* attributes */  },  {    engine: 'MYISAM',  },);
```

Like every option for the definition of a model, this setting can also be changed globally with the `define` option of the Sequelize constructor:

```
const sequelize = new Sequelize(db, user, pw, {  define: { engine: 'MYISAM' },});
```

## Table comments - MySQL/MariaDB/PostgreSQL only​

You can specify a comment for a table when defining the model:

```
class Person extends Model {}Person.init(  {    /* attributes */  },  {    comment: "I'm a table comment!",    sequelize,  },);
```

The comment will be set when calling `sync()`.
