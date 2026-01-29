# 位於 Proxy 背後的 Express and more

# 位於 Proxy 背後的 Express

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# 位於 Proxy 背後的 Express

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

The application setting `trust proxy` may be set to one of the values listed in the following table.

| 類型 | 值 |
| --- | --- |
| 布林 | 若為true，會將用戶端的 IP 位址視為X-Forwarded-*標頭中的最左側項目。若為false，會將應用程式視為直接面對網際網路，且用戶端的 IP 位址衍生自req.connection.remoteAddress。這是預設值。 This is the default setting.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8、::1/128linklocal -169.254.0.0/16、fe80::/10uniquelocal -10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、fc00::/7您可以採下列任何方式來設定 IP 位址：app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayWhen specified, the IP addresses or the subnets are excluded from the address determination process, and the untrusted IP address nearest to the application server is determined as the client’s IP address. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| 號碼 | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- [req.hostname](https://expressjs.com/zh-tw/api.html#req.hostname) 值會衍生自 `X-Forwarded-Host` 標頭中所設定的值，且該值可能由用戶端或 Proxy 所設定。
- 反向 Proxy 可能設定 `X-Forwarded-Proto`，以告知應用程式它是 `https` 或 `http` 或甚至是無效的名稱。[req.protocol](https://expressjs.com/zh-tw/api.html#req.protocol) 會反映此值。
     This value is reflected by [req.protocol](https://expressjs.com/zh-tw/api.html#req.protocol).
- [req.ip](https://expressjs.com/zh-tw/api.html#req.ip) 和 [req.ips](https://expressjs.com/zh-tw/api.html#req.ips) 值中會移入 `X-Forwarded-For` 中的位址清單。

會使用 [proxy-addr](https://www.npmjs.com/package/proxy-addr) 套件來實作 `trust proxy` 設定。如需相關資訊，請參閱其說明文件。 For more information, see its documentation.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/behind-proxies.md          )

---

# 資料庫整合

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# 資料庫整合

Adding the capability to connect databases to Express apps is just a matter of loading an appropriate Node.js driver for the database in your app. This document briefly explains how to add and use some of the most popular Node.js modules for database systems in your Express app:

- [Cassandra](#cassandra)
- [Couchbase](#couchbase)
- [CouchDB](#couchdb)
- [LevelDB](#leveldb)
- [MySQL](#mysql)
- [MongoDB](#mongo)
- [Neo4j](#neo4j)
- [Oracle](#oracle)
- [PostgreSQL](#postgres)
- [Redis](#redis)
-
- [SQLite](#sqlite)
- [ElasticSearch](#elasticsearch)

These database drivers are among many that are available. For other options,
search on the [npm](https://www.npmjs.com/) site.

## Cassandra

**模組**：[cassandra-driver](https://github.com/datastax/nodejs-driver) **安裝**

### Installation

```
$ npm install cassandra-driver
```

### 範例

```
const cassandra = require('cassandra-driver')
const client = new cassandra.Client({ contactPoints: ['localhost'] })

client.execute('select key from system.local', (err, result) => {
  if (err) throw err
  console.log(result.rows[0])
})
```

## Couchbase

**Module**: [couchnode](https://github.com/couchbase/couchnode)

### Installation

```
$ npm install couchbase
```

### 範例

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

**模組**：[nano](https://github.com/dscape/nano) **安裝**

### Installation

```
$ npm install nano
```

### 範例

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

**模組**：[levelup](https://github.com/rvagg/node-levelup) **安裝**

### Installation

```
$ npm install level levelup leveldown
```

### 範例

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

**模組**：[mysql](https://github.com/felixge/node-mysql/) **安裝**

### Installation

```
$ npm install mysql
```

### 範例

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

**模組**：[mongodb](https://github.com/mongodb/node-mongodb-native) **安裝**

### Installation

```
$ npm install mongodb
```

### Example (v2.*)

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

### Example (v3.*)

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

如果您需要 MongoDB 物件模型驅動程式，請查看 [Mongoose](https://github.com/LearnBoost/mongoose)。

## Neo4j

這些資料庫驅動程式只是眾多可用驅動程式中的一部分。如需其他選項，請在 [npm](https://www.npmjs.com/) 網站中搜尋。

### Installation

```
$ npm install neo4j-driver
```

### 範例

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

**Module**: [oracledb](https://github.com/oracle/node-oracledb)

### Installation

NOTE: [See installation prerequisites](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### 範例

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

**模組**：[pg-promise](https://github.com/vitaly-t/pg-promise) **安裝**

### Installation

```
$ npm install pg-promise
```

### 範例

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

**模組**：[redis](https://github.com/mranney/node_redis) **安裝**

### Installation

```
$ npm install redis
```

### 範例

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

**Module**: [tedious](https://github.com/tediousjs/tedious)

### Installation

```
$ npm install tedious
```

### 範例

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

**模組**：[sqlite3](https://github.com/mapbox/node-sqlite3) **安裝**

### Installation

```
$ npm install sqlite3
```

### 範例

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

**模組**：[elasticsearch](https://github.com/elastic/elasticsearch-js) **安裝**

### Installation

```
$ npm install elasticsearch
```

### 範例

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/database-integration.md          )

---

# 對 Express 除錯

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# 對 Express 除錯

如果要查看 Express 中使用的所有內部日誌，在您啟動應用程式時，請將 `DEBUG` 環境變數設為 `express:*`。

```
$ DEBUG=express:* node index.js
```

在 Windows 中，使用對應指令。

```
> $env:DEBUG = "express:*"; node index.js
```

對 [express generator](https://expressjs.com/zh-tw/starter/generator.html) 產生的預設應用程式執行這個指令，會列印下列輸出：

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

當對應用程式發出要求時，您會看到 Express 程式碼中指定的日誌：

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

如果只想查看來自路由器實作的日誌，請將 `DEBUG` 的值設為 `express:router`。同樣地，如果只想查看來自應用程式實作的日誌，請將 `DEBUG` 的值設為 `express:application`，以此類推。 Likewise, to see logs only from the application implementation, set the value of `DEBUG` to `express:application`, and so on.

## express產生的應用程式

`express` 指令產生的應用程式也會使用 `debug` 模組，且其除錯名稱空間的範圍限於應用程式的名稱。

舉例來說，如果您使用 `$ express sample-app` 來產生應用程式，您可以利用下列指令來啟用除錯陳述式：

```
$ DEBUG=sample-app:* node ./bin/www
```

您可以指派以逗點區隔的名稱清單，來指定多個除錯名稱空間：

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

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/debugging.md          )

---

# 錯誤處理

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# 錯誤處理

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## Catching Errors

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

If you pass anything to the `next()` function (except the string `'route'`),
Express regards the current request as being an error and will skip any
remaining non-error handling routing and middleware functions.

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

## The default error handler

Express comes with a built-in error handler that takes care of any errors that might be encountered in the app. This default error-handling middleware function is added at the end of the middleware function stack.

如果您傳遞錯誤至 `next()`，且您沒有在錯誤處理常式中處理它，將會交由內建錯誤處理常式處理；該錯誤會連同堆疊追蹤寫入至用戶端。在正式作業環境中，則不包含堆疊追蹤。 The stack trace is not included
in the production environment.

將 `NODE_ENV` 環境變數設為 `production`，以便在正式作業模式下執行應用程式。

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

在您開始撰寫回應之後，一旦在呼叫 `next()` 時才發生錯誤（例如，當您將回應串流輸出至用戶端時遇到錯誤），Express 的預設錯誤處理程式會關閉連線，並使要求失敗。

So when you add a custom error handler, you must delegate to
the default Express error handler, when the headers
have already been sent to the client:

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/zh-tw/resources/middleware.html).

## Writing error handlers

錯誤處理中介軟體函數的定義方式，與其他中介軟體函數相同，差別在於錯誤處理函數的引數是四個而非三個：`(err, req, res, next)`。例如： For example:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

您是在定義其他 `app.use()` 和路由呼叫之後，最後才定義錯誤處理中介軟體；例如：

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

Responses from within a middleware function can be in any format, such as an HTML error page, a simple message, or a JSON string.

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

在本例中，通用的 `logErrors` 可能將要求和錯誤資訊寫入至 `stderr`，例如：

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

此外在本例中，`clientErrorHandler` 定義成如下；在此情況下，會將錯誤明確傳遞給下一個：

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

“catch-all” `errorHandler` 函數的實作方式如下：

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

If you have a route handler with multiple callback functions, you can use the `route` parameter to skip to the next route handler. For example:

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

在本例中，會跳過 `getPaidContent` 處理程式，但是會繼續執行 `app` 中 `/a_route_behind_paywall` 的其餘處理程式。

Calls to `next()` and `next(err)` indicate that the current handler is complete and in what state.  `next(err)` will skip all remaining handlers in the chain except for those that are set up to handle errors as described above.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/error-handling.md          )

---

# 移至 Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# 移至 Express 4

## 概觀

Express 4 是對 Express 3 的突破性變更。也就是說，如果您在其相依關係中更新 Express 版本，現有的 Express 3 應用程式將無法運作。 That means an existing Express 3 app will *not* work if you update the Express version in its dependencies.

本文涵蓋：

- [Express 4 中的變更。](#changes)
- 將 Express 3 應用程式移轉至 Express 4 的[範例](#example-migration)。
- [升級至 Express 4 應用程式產生器。](#app-gen)

## Express 4 中的變更

Express 4 有數項明顯的變更：

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [路由系統的變更。](#routing)
- [其他各項變更。](#other-changes)

另請參閱：

- [New features in 4.x](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migrating from 3.x to 4.x](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Express 核心和中介軟體系統的變更

Express 4 不再相依於 Connect，除了 `express.static` 函數，其他所有的內建中介軟體皆已從其核心移除。也就是說，Express 現在是一個獨立的路由與中介軟體 Web 架構，Express 的版本化與版次不受中介軟體更新的影響。 This means that
Express is now an independent routing and middleware web framework, and
Express versioning and releases are not affected by middleware updates.

由於沒有內建中介軟體，您必須明確新增執行您應用程式所需的所有中介軟體。只需遵循下列步驟： Simply follow these steps:

1. 安裝模組：`npm install --save <module-name>`
2. 在您的應用程式中，需要模組：`require('module-name')`
3. 遵循模組的說明文件來使用該模組：`app.use( ... )`

下表列出 Express 3 中介軟體和其在 Express 4 中的對應項目。

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

以下是 Express 4 中介軟體的[完整清單](https://github.com/senchalabs/connect#middleware)。

In most cases, you can simply replace the old version 3 middleware with
its Express 4 counterpart. For details, see the module documentation in
GitHub.

#### app.use接受參數

In version 4 you can use a variable parameter to define the path where middleware functions are loaded, then read the value of the parameter from the route handler.
For example:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### 路由系統

Apps 現在隱含地載入了路由中介軟體，因此您不用再擔心該中介軟體相對於 `router` 中介軟體的載入順序。

路由的定義方式不變，但是路由系統多了兩個新特性，可協助您組織路由：

- 新方法 `app.route()`，用來為路由路徑建立可鏈接的路由處理程式。
- 新類別 `express.Router`，用來建立可裝載的模組路由處理程式。

#### app.route()方法

新的 `app.route()` 方法可讓您為路由路徑建立可鏈接的路由處理程式。由於是在單一位置指定路徑，建立模組路由很有用，因為它可減少冗餘和打錯字的情況。如需路由的相關資訊，請參閱 [Router()說明文件](https://expressjs.com/zh-tw/4x/api.html#router)。 Because the path is specified in a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more
information about routes, see [Router()documentation](https://expressjs.com/zh-tw/4x/api.html#router).

下列範例顯示利用 `app.route()` 函數所定義的路由處理程式鏈。

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

#### express.Router類別

The other feature that helps to organize routes is a new class,
`express.Router`, that you can use to create modular mountable
route handlers. A `Router` instance is a complete middleware and
routing system; for this reason it is often referred to as a “mini-app”.

下列範例是將路由器建立成模組、
在其中載入中介軟體、定義一些路由，並將它裝載在主要應用程式中的路徑。

例如，在應用程式目錄中建立一個名為 `birds.js` 的路由器檔案，內含下列內容：

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

然後將路由器模組載入應用程式中：

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

現在，應用程式就能夠處理發給 `/birds` 和 `/birds/about` 路徑的要求，並且會呼叫該路由特定的 `timeLog` 中介軟體。

### 其他變更

下表列出 Express 4 其他小幅卻很重要的變更：

| Object | Description |
| --- | --- |
| Node.js | Express 4 需要 Node.js 0.10.x 或更新版本，且不再支援 Node.js 0.8.x。 |
| http.createServer() | 不再需要http模組，除非您需要直接使用它 (socket.io/SPDY/HTTPS)。應用程式可藉由使用app.listen()函數來啟動。
 The app can be started by using theapp.listen()function. |
| app.configure() | Theapp.configure()function has been removed.app.configure()函數已移除。請使用process.env.NODE_ENV或app.get('env')函數來偵測環境，並據以配置應用程式。 |
| json spaces | Express 4 中依預設會停用json spaces應用程式內容。 |
| req.accepted() | 使用req.accepts()、req.acceptsEncodings()、req.acceptsCharsets()和req.acceptsLanguages()。</td>
</tr> |
| res.location() | 不再解析相對 URL。 |
| req.params | Was an array; now an object. |
| res.locals | Was a function; now an object. |
| res.headerSent | 已變更為res.headersSent。 |
| app.route | 現在以app.mountpath形式提供。 |
| res.on('header') | 已移除。 |
| res.charset | 已移除。 |
| res.setHeader('Set-Cookie', val) | Functionality is now limited to setting the basic cookie value.
現在功能僅限於設定基本 Cookie 值。請使用res.cookie()來取得新增的功能。 |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/guide/migrating-4.md          )
