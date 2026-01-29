# 代理背后的 Express and more

# 代理背后的 Express

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# 代理背后的 Express

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

在代理背后运行 Express 应用程序时，可使用 [app.set()](https://expressjs.com/zh-cn/4x/api.html#app.set) 将应用程序变量 `trust proxy` 设置为下表中所列的某个值。

| 类型 | 值 |
| --- | --- |
| 布尔 | 如果为true，那么客户机的 IP 地址将用作X-Forwarded-*头中最左侧的条目。
如果为false，那么该应用程序将被视为直接面对因特网，而客户机的 IP 地址则派生自req.connection.remoteAddress。这是缺省设置。Iffalse, the app is understood as directly facing the client and the client’s IP address is derived fromreq.socket.remoteAddress. This is the default setting.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7您可以按以下某种方法设置 IP 地址：app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an array如果指定 IP 地址或子网，那么会在地址确定过程中排除这些项，而将最接近应用程序服务器的不受信任的 IP 地址确定为客户机的 IP 地址。 This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| 数字 | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- [req.hostname](https://expressjs.com/zh-cn/api.html#req.hostname) 的值派生自 `X-Forwarded-Host` 头中设置的值（可以由客户机或代理设置此值）。
- `X-Forwarded-Proto` 可以由逆向代理设置，以告知应用程序：它是 `https` 还是 `http`，或者甚至是无效名称。该值由 [req.protocol](https://expressjs.com/zh-cn/api.html#req.protocol) 反映。
     This value is reflected by [req.protocol](https://expressjs.com/zh-cn/api.html#req.protocol).
- [req.ip](https://expressjs.com/zh-cn/api.html#req.ip) 和 [req.ips](https://expressjs.com/zh-cn/api.html#req.ips) 值由 `X-Forwarded-For` 的地址列表填充。

`trust proxy` 设置由使用 [proxy-addr](https://www.npmjs.com/package/proxy-addr) 包实现。有关更多信息，请参阅其文档。 For more information, see its documentation.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/behind-proxies.md          )

---

# 数据库集成

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# 数据库集成

要将数据库连接到 Express 应用程序，只需在该应用程序中为数据库装入相应的 Node.js 驱动程序。本文档简要说明如何在 Express 应用程序中为数据库系统添加和使用某些最流行的 Node.js 模块： This document briefly explains how to add and use some of the most popular Node.js modules for database systems in your Express app:

- [Cassandra](#cassandra)
- [Couchbase](#couchbase)
- [CouchDB](#couchdb)
- [LevelDB](#leveldb)
- [MySQL](#mysql)
- [MongoDB](#mongodb)
- [Neo4j](#neo4j)
- [Oracle](#oracle)
- [PostgreSQL](#postgresql)
- [Redis](#redis)
- [SQL Server](#sql-server)
- [SQLite](#sqlite)
- [Elasticsearch](#elasticsearch)

这些数据库驱动程序是众多可用数据库驱动程序的一部分。要了解其他选项，请在 [npm](https://www.npmjs.com/) 站点上搜索。
 For other options,
search on the [npm](https://www.npmjs.com/) site.

## Cassandra

**模块**：[cassandra-driver](https://github.com/datastax/nodejs-driver)

### 安装

```
$ npm install cassandra-driver
```

### 示例

```
const cassandra = require('cassandra-driver')
const client = new cassandra.Client({ contactPoints: ['localhost'] })

client.execute('select key from system.local', (err, result) => {
  if (err) throw err
  console.log(result.rows[0])
})
```

## Couchbase

**模块**: [couchnode](https://github.com/couchbase/couchnode)

### 安装

```
$ npm install couchbase
```

### 示例

```
const couchbase = require('couchbase')
const bucket = (new couchbase.Cluster('http://localhost:8091')).openBucket('bucketName')

// add a document to a bucket
bucket.insert('document-key', { name: 'Matt', shoeSize: 13 }, (err, result) => {
  if (err) {
    console.log(err)
  } else {
    console.log(result)
  }
})

// get all documents with shoe size 13
const n1ql = 'SELECT d.* FROM `bucketName` d WHERE shoeSize = $1'
const query = N1qlQuery.fromString(n1ql)
bucket.query(query, [13], (err, result) => {
  if (err) {
    console.log(err)
  } else {
    console.log(result)
  }
})
```

## CouchDB

**模块**：[nano](https://github.com/dscape/nano)

### 安装

```
$ npm install nano
```

### 示例

```
const nano = require('nano')('http://localhost:5984')
nano.db.create('books')
const books = nano.db.use('books')

// Insert a book document in the books database
books.insert({ name: 'The Art of war' }, null, (err, body) => {
  if (err) {
    console.log(err)
  } else {
    console.log(body)
  }
})

// Get a list of all books
books.list((err, body) => {
  if (err) {
    console.log(err)
  } else {
    console.log(body.rows)
  }
})
```

## LevelDB

**模块**：[levelup](https://github.com/rvagg/node-levelup)

### 安装

```
$ npm install level levelup leveldown
```

### 示例

```
const levelup = require('levelup')
const db = levelup('./mydb')

db.put('name', 'LevelUP', (err) => {
  if (err) return console.log('Ooops!', err)

  db.get('name', (err, value) => {
    if (err) return console.log('Ooops!', err)

    console.log(`name=${value}`)
  })
})
```

## MySQL

**模块**：[mysql](https://github.com/felixge/node-mysql/)

### 安装

```
$ npm install mysql
```

### 示例

```
const mysql = require('mysql')
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'dbuser',
  password: 's3kreee7',
  database: 'my_db'
})

connection.connect()

connection.query('SELECT 1 + 1 AS solution', (err, rows, fields) => {
  if (err) throw err

  console.log('The solution is: ', rows[0].solution)
})

connection.end()
```

## MongoDB

**模块**：[mongodb](https://github.com/mongodb/node-mongodb-native)

### 安装

```
$ npm install mongodb
```

### 示例（v2.*）

```
const MongoClient = require('mongodb').MongoClient

MongoClient.connect('mongodb://localhost:27017/animals', (err, db) => {
  if (err) throw err

  db.collection('mammals').find().toArray((err, result) => {
    if (err) throw err

    console.log(result)
  })
})
```

### 示例（v3.*）

```
const MongoClient = require('mongodb').MongoClient

MongoClient.connect('mongodb://localhost:27017/animals', (err, client) => {
  if (err) throw err

  const db = client.db('animals')

  db.collection('mammals').find().toArray((err, result) => {
    if (err) throw err

    console.log(result)
  })
})
```

如果您需要 MongoDB 的对象模型驱动程序，请查看 [Mongoose](https://github.com/LearnBoost/mongoose)。

## Neo4j

**Module**: [neo4j-driver](https://github.com/neo4j/neo4j-javascript-driver)

### 安装

```
$ npm install neo4j-driver
```

### 示例

```
const neo4j = require('neo4j-driver')
const driver = neo4j.driver('neo4j://localhost:7687', neo4j.auth.basic('neo4j', 'letmein'))

const session = driver.session()

session.readTransaction((tx) => {
  return tx.run('MATCH (n) RETURN count(n) AS count')
    .then((res) => {
      console.log(res.records[0].get('count'))
    })
    .catch((error) => {
      console.log(error)
    })
})
```

## Oracle

**模块**: [oracledb](https://github.com/oracle/node-oracledb)

### 安装

注意: [See installation prerequisites](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### 示例

```
const oracledb = require('oracledb')
const config = {
  user: '<your db user>',
  password: '<your db password>',
  connectString: 'localhost:1521/orcl'
}

async function getEmployee (empId) {
  let conn

  try {
    conn = await oracledb.getConnection(config)

    const result = await conn.execute(
      'select * from employees where employee_id = :id',
      [empId]
    )

    console.log(result.rows[0])
  } catch (err) {
    console.log('Ouch!', err)
  } finally {
    if (conn) { // conn assignment worked, need to close
      await conn.close()
    }
  }
}

getEmployee(101)
```

## PostgreSQL

**Module**: [pg-promise](https://github.com/vitaly-t/pg-promise)

### 安装

```
$ npm install pg-promise
```

### 示例

```
const pgp = require('pg-promise')(/* options */)
const db = pgp('postgres://username:password@host:port/database')

db.one('SELECT $1 AS value', 123)
  .then((data) => {
    console.log('DATA:', data.value)
  })
  .catch((error) => {
    console.log('ERROR:', error)
  })
```

## Redis

**模块**：[redis](https://github.com/mranney/node_redis)

### 安装

```
$ npm install redis
```

### 示例

```
const redis = require('redis')
const client = redis.createClient()

client.on('error', (err) => {
  console.log(`Error ${err}`)
})

client.set('string key', 'string val', redis.print)
client.hset('hash key', 'hashtest 1', 'some value', redis.print)
client.hset(['hash key', 'hashtest 2', 'some other value'], redis.print)

client.hkeys('hash key', (err, replies) => {
  console.log(`${replies.length} replies:`)

  replies.forEach((reply, i) => {
    console.log(`    ${i}: ${reply}`)
  })

  client.quit()
})
```

## SQL Server

**模块**: [tedious](https://github.com/tediousjs/tedious)

### 安装

```
$ npm install tedious
```

### 示例

```
const Connection = require('tedious').Connection
const Request = require('tedious').Request

const config = {
  server: 'localhost',
  authentication: {
    type: 'default',
    options: {
      userName: 'your_username', // update me
      password: 'your_password' // update me
    }
  }
}

const connection = new Connection(config)

connection.on('connect', (err) => {
  if (err) {
    console.log(err)
  } else {
    executeStatement()
  }
})

function executeStatement () {
  request = new Request("select 123, 'hello world'", (err, rowCount) => {
    if (err) {
      console.log(err)
    } else {
      console.log(`${rowCount} rows`)
    }
    connection.close()
  })

  request.on('row', (columns) => {
    columns.forEach((column) => {
      if (column.value === null) {
        console.log('NULL')
      } else {
        console.log(column.value)
      }
    })
  })

  connection.execSql(request)
}
```

## SQLite

**模块**：[sqlite3](https://github.com/mapbox/node-sqlite3)

### 安装

```
$ npm install sqlite3
```

### 示例

```
const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database(':memory:')

db.serialize(() => {
  db.run('CREATE TABLE lorem (info TEXT)')
  const stmt = db.prepare('INSERT INTO lorem VALUES (?)')

  for (let i = 0; i < 10; i++) {
    stmt.run(`Ipsum ${i}`)
  }

  stmt.finalize()

  db.each('SELECT rowid AS id, info FROM lorem', (err, row) => {
    console.log(`${row.id}: ${row.info}`)
  })
})

db.close()
```

## ElasticSearch

**模块**：[elasticsearch](https://github.com/elastic/elasticsearch-js)

### 安装

```
$ npm install elasticsearch
```

### 示例

```
const elasticsearch = require('elasticsearch')
const client = elasticsearch.Client({
  host: 'localhost:9200'
})

client.search({
  index: 'books',
  type: 'book',
  body: {
    query: {
      multi_match: {
        query: 'express js',
        fields: ['title', 'description']
      }
    }
  }
}).then((response) => {
  const hits = response.hits.hits
}, (error) => {
  console.trace(error.message)
})
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/database-integration.md          )

---

# 调试 Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# 调试 Express

要查看 Express 中使用的所有内部日志，在启动应用程序时，请将 `DEBUG` 环境变量设置为 `express:*`。

```
$ DEBUG=express:* node index.js
```

在 Windows 上，使用对应的命令。

```
> $env:DEBUG = "express:*"; node index.js
```

在 [Express 生成器](https://expressjs.com/zh-cn/starter/generator.html)所生成的缺省应用程序上运行此命令将显示以下输出：

```
$ DEBUG=express:* node ./bin/www
  express:router:route new / +0ms
  express:router:layer new / +1ms
  express:router:route get / +1ms
  express:router:layer new / +0ms
  express:router:route new / +1ms
  express:router:layer new / +0ms
  express:router:route get / +0ms
  express:router:layer new / +0ms
  express:application compile etag weak +1ms
  express:application compile query parser extended +0ms
  express:application compile trust proxy false +0ms
  express:application booting in development mode +1ms
  express:router use / query +0ms
  express:router:layer new / +0ms
  express:router use / expressInit +0ms
  express:router:layer new / +0ms
  express:router use / favicon +1ms
  express:router:layer new / +0ms
  express:router use / logger +0ms
  express:router:layer new / +0ms
  express:router use / jsonParser +0ms
  express:router:layer new / +1ms
  express:router use / urlencodedParser +0ms
  express:router:layer new / +0ms
  express:router use / cookieParser +0ms
  express:router:layer new / +0ms
  express:router use / stylus +90ms
  express:router:layer new / +0ms
  express:router use / serveStatic +0ms
  express:router:layer new / +0ms
  express:router use / router +0ms
  express:router:layer new / +1ms
  express:router use /users router +0ms
  express:router:layer new /users +0ms
  express:router use / &amp;lt;anonymous&amp;gt; +0ms
  express:router:layer new / +0ms
  express:router use / &amp;lt;anonymous&amp;gt; +0ms
  express:router:layer new / +0ms
  express:router use / &amp;lt;anonymous&amp;gt; +0ms
  express:router:layer new / +0ms
```

向应用程序发出请求时，可以看到 Express 代码中指定的日志：

```
express:router dispatching GET / +4h
  express:router query  : / +2ms
  express:router expressInit  : / +0ms
  express:router favicon  : / +0ms
  express:router logger  : / +1ms
  express:router jsonParser  : / +0ms
  express:router urlencodedParser  : / +1ms
  express:router cookieParser  : / +0ms
  express:router stylus  : / +0ms
  express:router serveStatic  : / +2ms
  express:router router  : / +2ms
  express:router dispatching GET / +1ms
  express:view lookup "index.pug" +338ms
  express:view stat "/projects/example/views/index.pug" +0ms
  express:view render "/projects/example/views/index.pug" +1ms
```

要仅查看来自路由器实现的日志，请将 `DEBUG` 的值设置为 `express:router`。与此类似，要仅查看来自应用程序实现的日志，请将 `DEBUG` 的值设置为 `express:application`，以此类推。 Likewise, to see logs only from the application implementation, set the value of `DEBUG` to `express:application`, and so on.

## express生成的应用程序

`express` 命令生成的应用程序还使用 `debug` 模块，其调试名称空间范围限定为应用程序的名称。

例如，如果您以 `$ express sample-app` 生成应用程序，那么可以使用以下命令来启用调试语句：

```
$ DEBUG=sample-app:* node ./bin/www
```

可以通过分配逗号分隔的名称列表来指定多个调试名称空间：

```
$ DEBUG=http,mail,express:* node index.js
```

## Advanced options

When running through Node.js, you can set a few environment variables that will change the behavior of the debug logging:

| Name | Purpose |
| --- | --- |
| DEBUG | Enables/disables specific debugging namespaces. |
| DEBUG_COLORS | Whether or not to use colors in the debug output. |
| DEBUG_DEPTH | Object inspection depth. |
| DEBUG_FD | File descriptor to write debug output to. |
| DEBUG_SHOW_HIDDEN | Shows hidden properties on inspected objects. |

Note

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[util.inspect()](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/debugging.md          )

---

# 错误处理

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# 错误处理

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## 如果将错误传递到next()且未在错误处理程序中进行处理，那么该错误将由内置的错误处理程序处理；错误将写入客户机的堆栈跟踪内。堆栈跟踪不包含在生产环境中。

It’s important to ensure that Express catches all errors that occur while
running route handlers and middleware.

Errors that occur in synchronous code inside route handlers and middleware
require no extra work. If synchronous code throws an error, then Express will
catch and process it. For example:

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

For errors returned from asynchronous functions invoked by route handlers
and middleware, you must pass them to the `next()` function, where Express will
catch and process them.  For example:

```
app.get('/', (req, res, next) => {
  fs.readFile('/file-does-not-exist', (err, data) => {
    if (err) {
      next(err) // Pass errors to Express.
    } else {
      res.send(data)
    }
  })
})
```

Starting with Express 5, route handlers and middleware that return a Promise
will call `next(value)` automatically when they reject or throw an error.
For example:

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

If `getUserById` throws an error or rejects, `next` will be called with either
the thrown error or the rejected value. If no rejected value is provided, `next`
will be called with a default Error object provided by the Express router.

如果将任何项传递到 `next()` 函数（除了字符串 `'route'`），那么 Express 会将当前请求视为处于错误状态，并跳过所有剩余的非错误处理路由和中间件函数。如果您希望以某种方式处理此错误，必须如下一节中所述创建一个错误处理路由。

If the callback in a sequence provides no data, only errors, you can simplify
this code as follows:

```
app.get('/', [
  function (req, res, next) {
    fs.writeFile('/inaccessible-path', 'data', next)
  },
  function (req, res) {
    res.send('OK')
  }
])
```

In the above example, `next` is provided as the callback for `fs.writeFile`,
which is called with or without errors. If there is no error, the second
handler is executed, otherwise Express catches and processes the error.

You must catch errors that occur in asynchronous code invoked by route handlers or
middleware and pass them to Express for processing. For example:

```
app.get('/', (req, res, next) => {
  setTimeout(() => {
    try {
      throw new Error('BROKEN')
    } catch (err) {
      next(err)
    }
  }, 100)
})
```

The above example uses a `try...catch` block to catch errors in the
asynchronous code and pass them to Express. If the `try...catch`
block were omitted, Express would not catch the error since it is not part of the synchronous
handler code.

Use promises to avoid the overhead of the `try...catch` block or when using functions
that return promises.  For example:

```
app.get('/', (req, res, next) => {
  Promise.resolve().then(() => {
    throw new Error('BROKEN')
  }).catch(next) // Errors will be passed to Express.
})
```

Since promises automatically catch both synchronous errors and rejected promises,
you can simply provide `next` as the final catch handler and Express will catch errors,
because the catch handler is given the error as the first argument.

You could also use a chain of handlers to rely on synchronous error
catching, by reducing the asynchronous code to something trivial. For example:

```
app.get('/', [
  function (req, res, next) {
    fs.readFile('/maybe-valid-file', 'utf-8', (err, data) => {
      res.locals.data = data
      next(err)
    })
  },
  function (req, res) {
    res.locals.data = res.locals.data.split(',')[1]
    res.send(res.locals.data)
  }
])
```

The above example has a couple of trivial statements from the `readFile`
call. If `readFile` causes an error, then it passes the error to Express, otherwise you
quickly return to the world of synchronous error handling in the next handler
in the chain. Then, the example above tries to process the data. If this fails, then the
synchronous error handler will catch it. If you had done this processing inside
the `readFile` callback, then the application might exit and the Express error
handlers would not run.

Whichever method you use, if you want Express error handlers to be called in and the
application to survive, you must ensure that Express receives the error.

## 缺省错误处理程序

Express 随附一个内置的错误处理程序，负责处理应用程序中可能遇到的任何错误。这个缺省的错误处理中间件函数添加在中间件函数集的末尾。 This default error-handling middleware function is added at the end of the middleware function stack.

If you pass an error to `next()` and you do not handle it in a custom error
handler, it will be handled by the built-in error handler; the error will be
written to the client with the stack trace. The stack trace is not included
in the production environment.

将环境变量 `NODE_ENV` 设置为 `production`，以生产方式运行此应用程序。

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

如果在开始写响应之后调用 `next()` 时出错（例如，如果在以流式方式将响应传输到客户机时遇到错误），Express 缺省错误处理程序会关闭连接并使请求失败。

因此，在添加定制错误处理程序时，如果头已发送到客户机，您可能希望委托给 Express 中的缺省错误处理机制处理：

```
function errorHandler (err, req, res, next) {
  if (res.headersSent) {
    return next(err)
  }
  res.status(500)
  res.render('error', { error: err })
}
```

Note that the default error handler can get triggered if you call `next()` with an error
in your code more than once, even if custom error handling middleware is in place.

Other error handling middleware can be found at [Express middleware](https://expressjs.com/zh-cn/resources/middleware.html).

## Writing error handlers

错误处理中间件函数的定义方式与其他中间件函数基本相同，差别在于错误处理函数有四个自变量而不是三个：`(err, req, res, next)`：例如： For example:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

请在其他 `app.use()` 和路由调用之后，最后定义错误处理中间件，例如：

```
const bodyParser = require('body-parser')
const methodOverride = require('method-override')

app.use(bodyParser.urlencoded({
  extended: true
}))
app.use(bodyParser.json())
app.use(methodOverride())
app.use((err, req, res, next) => {
  // logic
})
```

中间件函数中的响应可以采用您首选的任何格式，例如，HTML 错误页、简单消息或 JSON 字符串。

For organizational (and higher-level framework) purposes, you can define
several error-handling middleware functions, much as you would with
regular middleware functions. For example, to define an error-handler
for requests made by using `XHR` and those without:

```
const bodyParser = require('body-parser')
const methodOverride = require('method-override')

app.use(bodyParser.urlencoded({
  extended: true
}))
app.use(bodyParser.json())
app.use(methodOverride())
app.use(logErrors)
app.use(clientErrorHandler)
app.use(errorHandler)
```

在此示例中，通用 `logErrors` 可能将请求和错误信息写入 `stderr`，例如：

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

也是在此示例中，`clientErrorHandler` 定义如下，错误会显式传递到下一项：

Notice that when *not* calling “next” in an error-handling function, you are responsible for writing (and ending) the response. Otherwise, those requests will “hang” and will not be eligible for garbage collection.

```
function clientErrorHandler (err, req, res, next) {
  if (req.xhr) {
    res.status(500).send({ error: 'Something failed!' })
  } else {
    next(err)
  }
}
```

“catch-all”`errorHandler` 函数可以如下实现：

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

如果一个路由处理程序具有多个回调函数，那么可以使用 `route` 参数跳至下一个路由处理程序。例如： For example:

```
app.get('/a_route_behind_paywall',
  (req, res, next) => {
    if (!req.user.hasPaid) {
      // continue handling this request
      next('route')
    } else {
      next()
    }
  }, (req, res, next) => {
    PaidContent.find((err, doc) => {
      if (err) return next(err)
      res.json(doc)
    })
  })
```

在此示例中，将跳过 `getPaidContent` 处理程序，而将继续执行 `/a_route_behind_paywall` 的 `app` 中所有剩余的处理程序。

对 `next()` 和 `next(err)` 的调用会表明当前处理程序是否完整以及处于何种状态。`next(err)` 将跳过链中所有剩余的处理程序（设置为按上述方式处理错误的处理程序除外）。
  `next(err)` will skip all remaining handlers in the chain except for those that are set up to handle errors as described above.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/error-handling.md          )

---

# 迁移到 Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# 迁移到 Express 4

## 概述

Express 4 is a breaking change from Express 3. Express 4 对 Express 3 进行了重大更改，这意味着，如果您在现有 Express 3 应用程序的依赖项中更新了 Express 版本，那么该应用程序将无法工作。

本文讲述：

- [Express 4 中的更改。](#changes)
- 将 Express 3 应用程序迁移到 Express 4 的[示例](#example-migration)。
- [升级到 Express 4 应用程序生成器。](#app-gen)

## Express 4 中的更改

Express 4 中进行了若干重大更改：

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [对路由系统进行了更改。](#routing)
- [其他各种更改。](#other-changes)

另请参阅：

- [New features in 4.x](https://github.com/expressjs/express/wiki/New-features-in-4.x)。
- [Migrating from 3.x to 4.x](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)。

### 对 Express 核心和中间件系统的更改。

Express 4 不再依赖于 Connect，从其核心移除了所有内置的中间件（除了 `express.static` 函数）。这意味着 Express 现在是独立的路由和中间件 Web 框架，Express 的版本控制和发行不受中间件更新的影响。 This means that
Express is now an independent routing and middleware web framework, and
Express versioning and releases are not affected by middleware updates.

由于没有内置中间件，因此您必须显式添加所需的所有中间件才能运行应用程序。只需执行以下步骤： Simply follow these steps:

1. 安装模块：`npm install --save <module-name>`
2. 在应用程序中需要此模块：`require('module-name')`
3. 根据文档使用模块：`app.use( ... )`

下表列出了 Express 3 中间件及其在 Express 4 中的对应组件。

| Express 3 | Express 4 |
| --- | --- |
| express.bodyParser | body-parser+multer |
| express.compress | compression |
| express.cookieSession | cookie-session |
| express.cookieParser | cookie-parser |
| express.logger | morgan |
| express.session | express-session |
| express.favicon | serve-favicon |
| express.responseTime | response-time |
| express.errorHandler | errorhandler |
| express.methodOverride | method-override |
| express.timeout | connect-timeout |
| express.vhost | vhost |
| express.csrf | csurf |
| express.directory | serve-index |
| express.static | serve-static |

可参考 Express 4 中间件的[完整列表](https://github.com/senchalabs/connect#middleware)。

在大多数情况下，可以将旧的 V3 中间件替换为 Express 4 的对应组件。有关详细信息，请参阅 GitHub 中的模块文档。 For details, see the module documentation in
GitHub.

#### app.use可以使用参数

在 V4 中，您可以使用变量参数来定义装入中间件函数的路径，然后从路由处理程序读取参数的值。
例如：
For example:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### 路由系统

应用程序现在隐式装入路由中间件，所以您不再需要担心其他中间件相对于`路由`中间件的装入顺序。

定义路由的方式并未改变，但是路由系统新增了两个功能，用于帮助组织路由：

- 一个新方法 `app.route()`，用于为路由路径创建可链接的路由处理程序。
- 一个新类 `express.Router`，用于创建可安装的模块化路由处理程序。

#### app.route()方法

新的 `app.route()` 方法使您可以为路由路径创建可链接的路由处理程序。创建模块化路由很有帮助，因为在单一位置指定路径，所以可以减少冗余和输入错误。有关路由的更多信息，请参阅 [Router()文档](https://expressjs.com/zh-cn/4x/api.html#router)。 Because the path is specified in a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more
information about routes, see [Router()documentation](https://expressjs.com/zh-cn/4x/api.html#router).

以下是使用 `app.route()` 函数定义的链式路由处理程序的示例。

```
app.route('/book')
  .get((req, res) => {
    res.send('Get a random book')
  })
  .post((req, res) => {
    res.send('Add a book')
  })
  .put((req, res) => {
    res.send('Update the book')
  })
```

#### express.Router类

The other feature that helps to organize routes is a new class,
`express.Router`, that you can use to create modular mountable
route handlers. 有助于组织路由的另一个功能是新类 `express.Router`，可用于创建可安装的模块化路由处理程序。`Router` 实例是完整的中间件和路由系统；因此，常常将其称为“微型应用程序”。

以下示例将路由器创建为模块，在其中装入中间件，定义一些路由，然后安装在主应用程序的路径中。

例如，在应用程序目录中创建名为 `birds.js` 的路由器文件，其中包含以下内容：

```
var express = require('express')
var router = express.Router()

// middleware specific to this router
router.use((req, res, next) => {
  console.log('Time: ', Date.now())
  next()
})
// define the home page route
router.get('/', (req, res) => {
  res.send('Birds home page')
})
// define the about route
router.get('/about', (req, res) => {
  res.send('About birds')
})

module.exports = router
```

接着，在应用程序中装入路由器模块：

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

此应用程序现在可处理针对 `/birds` 和 `/birds/about` 路径的请求，调用特定于此路由的 `timeLog` 中间件。

### 其他更改

下表列出 Express 4 中虽小但重要的其他更改：

| 对象 | 描述 |
| --- | --- |
| Node.js | Express 4 需要 Node.js 0.10.x 或更高版本，已取消对 Node.js 0.8.x 的支持。 |
| http.createServer() | 不再需要http模块，除非您要直接使用它 (socket.io/SPDY/HTTPS)。可以使用app.listen()函数来启动此应用程序。
 The app can be started by using theapp.listen()function. |
| app.configure() | Theapp.configure()function has been removed.已移除app.configure()函数。使用process.env.NODE_ENV或app.get('env')功能来检测环境并相应配置该应用程序。 |
| json spaces | 在 Express 4 中，缺省情况下，已禁用json spaces应用程序属性。 |
| req.accepted() | 使用req.accepts()、req.acceptsEncodings()、req.acceptsCharsets()和req.acceptsLanguages()。 |
| res.location() | 不再解析相对 URL。 |
| req.params | 原来是数组；现在是对象。 |
| res.locals | 原来是函数；现在是对象。 |
| res.headerSent | 更改为res.headersSent。 |
| app.route | 现在可作为app.mountpath使用。 |
| res.on('header') | 已移除。 |
| res.charset | 已移除。 |
| res.setHeader('Set-Cookie', val) | Functionality is now limited to setting the basic cookie value.
功能现在已限制为设置基本 cookie 值。将res.cookie()用于增添的功能。 |

## 应用程序迁移示例

以下是将 Express 3 应用程序迁移到 Express 4 的示例。
涉及的文件包括 `app.js` 和 `package.json`。
下一步，将 `package.json` 文件中的 `"start": "node ./bin/www"` 更改为 `"start": "node app.js"`。

### V3 应用程序

#### app.js

考虑具有以下 `app.js` 文件的 Express V3 应用程序：

```
var express = require('express')
var routes = require('./routes')
var user = require('./routes/user')
var http = require('http')
var path = require('path')

var app = express()

// all environments
app.set('port', process.env.PORT || 3000)
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')
app.use(express.favicon())
app.use(express.logger('dev'))
app.use(express.methodOverride())
app.use(express.session({ secret: 'your secret here' }))
app.use(express.bodyParser())
app.use(app.router)
app.use(express.static(path.join(__dirname, 'public')))

// development only
if (app.get('env') === 'development') {
  app.use(express.errorHandler())
}

app.get('/', routes.index)
app.get('/users', user.list)

http.createServer(app).listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

#### package.json

随附的 V3 `package.json` 文件可能具有类似于以下的内容：

```
{
  "name": "application-name",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "3.12.0",
    "pug": "*"
  }
}
```

### 进程

使用以下命令安装 Express 4 应用程序的必需中间件并将 Express 和 Pug 分别更新到其最新版本，从而开始迁移过程：

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

对 `app.js` 进行以下更改：

1. Express 内置中间件函数 `express.favicon`、`express.logger`、`express.methodOverride`、`express.session`、`express.bodyParser` 和 `express.errorHandler` 不再可用于 `express` 对象。您必须手动安装其替代项，然后在应用程序中装入。 You must install their alternatives
  manually and load them in the app.
2. You no longer need to load the `app.router` function.
  不再需要装入 `app.router` 函数。它不是有效的 Express 4 应用程序对象，所以移除了 `app.use(app.router);` 代码。
3. 确保以正确顺序装入中间件函数 - 在装入应用程序路由之后装入 `errorHandler`。

### V4 应用程序

#### package.json

运行以上 `npm` 命令会更新 `package.json`，如下所示：

```
{
  "name": "application-name",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "body-parser": "^1.5.2",
    "errorhandler": "^1.1.1",
    "express": "^4.8.0",
    "express-session": "^1.7.2",
    "pug": "^2.0.0",
    "method-override": "^2.1.2",
    "morgan": "^1.2.2",
    "multer": "^0.1.3",
    "serve-favicon": "^2.0.1"
  }
}
```

#### app.js

随后，移除无效代码，装入所需中间件，并根据需要进行其他更改。`app.js` 文件如下： The `app.js` file will look like this:

```
var http = require('http')
var express = require('express')
var routes = require('./routes')
var user = require('./routes/user')
var path = require('path')

var favicon = require('serve-favicon')
var logger = require('morgan')
var methodOverride = require('method-override')
var session = require('express-session')
var bodyParser = require('body-parser')
var multer = require('multer')
var errorHandler = require('errorhandler')

var app = express()

// all environments
app.set('port', process.env.PORT || 3000)
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')
app.use(favicon(path.join(__dirname, '/public/favicon.ico')))
app.use(logger('dev'))
app.use(methodOverride())
app.use(session({
  resave: true,
  saveUninitialized: true,
  secret: 'uwotm8'
}))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(multer())
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', routes.index)
app.get('/users', user.list)

// error handling middleware should be loaded after the loading the routes
if (app.get('env') === 'development') {
  app.use(errorHandler())
}

var server = http.createServer(app)
server.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

除非您需要直接使用 `http` 模块 (socket.io/SPDY/HTTPS)，否则不需要将其装入，可按以下方式启动此应用程序：

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### 运行应用程序

迁移过程完成，此应用程序现在是 Express 4 版本。要进行确认，可使用以下命令启动此应用程序： To confirm, start the app by using the following command:

```
$ node .
```

装入 [http://localhost:3000](http://localhost:3000)，然后查看 Express 4 呈现的主页。

## 升级到 Express 4 应用程序生成器

用于生成 Express 应用程序的命令行工具仍然是 `express`，但是要升级到新版本，您必须卸载 Express 3 应用程序生成器，然后安装新的 `express-generator`。

### 安装

如果您已经在系统上安装了 Express 3 应用程序生成器，必须将其卸载：

```
$ npm uninstall -g express
```

根据您的文件和目录特权的配置方式，可能需要使用 `sudo` 来运行此命令。
立即安装新的生成器：

Now install the new generator:

```
$ npm install -g express-generator
```

根据您的文件和目录特权的配置方式，可能需要使用 `sudo` 来运行此命令。
立即安装新的生成器：

现在，系统上的 `express` 命令已更新到 Express 4 生成器。

### 对应用程序生成器的更改

命令选项和用法大体保持相同，但也存在以下例外：

- 已移除 `--sessions` 选项。
- 已移除 `--jshtml` 选项。
- 已添加 `--hogan` 选项来支持 [Hogan.js](http://twitter.github.io/hogan.js/)。

### 示例

执行以下命令来创建 Express 4 应用程序：

```
$ express app4
```

如果查看 `app4/app.js` 文件的内容，那么会注意到应用程序所需的所有中间件函数（除了 `express.static`）都作为独立模块装入，而在应用程序中不再显式装入 `router` 中间件。

还可以注意到，与旧生成器生成的独立应用程序相反，`app.js` 文件现在是 Node.js 模块。

在安装依赖项之后，可使用以下命令来启动此应用程序：

```
$ npm start
```

如果查看 `package.json` 文件中的 npm 启动脚本，可以注意到启动应用程序的实际命令是 `node ./bin/www`，而过去在 Express 3 中，该命令是 `node app.js`。

因为 Express 4 生成器生成的 `app.js` 文件现在是 Node.js 模块，所以不再能够将其作为应用程序独立启动（除非修改代码）。必须在 Node.js 文件中加载此模块，并通过 Node.js 文件启动。在此情况下，Node.js 文件是 `./bin/www`。 The module must be loaded in a Node.js file
and started via the Node.js file. The Node.js file is `./bin/www`
in this case.

对于创建 Express 应用程序或启动此应用程序，`bin` 目录或无扩展名的 `www` 文件都不是必需的。它们只是生成器提出的建议，可随意根据自己的需求进行修改。 They are
just suggestions made by the generator, so feel free to modify them to suit your
needs.

如果不想使用 `www` 目录，而是保持“Express 3 风格”，请删除 `app.js` 文件末尾的 `module.exports = app;` 行，然后将以下代码粘贴在到该位置：

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

确保使用以下代码在 `app.js` 文件之上装入 `debug` 模块：

```
var debug = require('debug')('app4')
```

现在，您已将 `./bin/www` 的功能恢复为 `app.js`。不建议进行此更改，但是此练习可以帮助您理解 `./bin/www` 文件的工作方式，以及为何 `app.js` 文件不再自行启动。

You have now moved the functionality of `./bin/www` back to
`app.js`. This change is not recommended, but the exercise helps you
to understand how the `./bin/www` file works, and why the `app.js` file
no longer starts on its own.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/guide/migrating-4.md          )
