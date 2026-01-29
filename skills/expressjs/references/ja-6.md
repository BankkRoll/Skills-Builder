# プロキシーの背後の Express and more

# プロキシーの背後の Express

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# プロキシーの背後の Express

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

The application setting `trust proxy` may be set to one of the values listed in the following table.

| 型 | 値 |
| --- | --- |
| Boolean | trueの場合、クライアントの IP アドレスは、X-Forwarded-*ヘッダーの左端の項目として理解されます。falseの場合、アプリケーションはインターネットに直接接続されているものとして理解され、クライアントの IP アドレスはreq.connection.remoteAddressから導き出されます。これはデフォルトの設定値です。 This is the default setting.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8、::1/128linklocal -169.254.0.0/16、fe80::/10uniquelocal -10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、fc00::/7以下のどの方法でも IP アドレスを設定できます。app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayIP アドレスまたはサブネットは、指定されると、アドレス決定プロセスから除外されます。アプリケーション・サーバーに最も近い信頼できない IP アドレスがクライアントの IP アドレスに決定されます。 This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| 数字 | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

`trust proxy`を有効にすると、次の3つの重要な変更が起こります。

- [req.hostname](https://expressjs.com/ja/api.html#req.hostname) の値は、クライアントまたはプロキシーが設定できる `X-Forwarded-Host` ヘッダーに設定された値から導き出されます。</li>
- `X-Forwarded-Proto` は、`https` と `http` のどちらであるか、または無効な名前であるかをアプリケーションに通知するためにリバース・プロキシーによって設定できます。この値は、[req.protocol](https://expressjs.com/ja/api.html#req.protocol) に反映されます。 This value is reflected by [req.protocol](https://expressjs.com/ja/api.html#req.protocol).
- [req.ip](https://expressjs.com/ja/api.html#req.ip) および [req.ips](https://expressjs.com/ja/api.html#req.ips) の値は、`X-Forwarded-For` のアドレス・リストから取り込まれます。</li>
  </ul>
  `trust proxy` 設定は、[proxy-addr](https://www.npmjs.com/package/proxy-addr) パッケージを使用して実装されます。詳細については、資料を参照してください。 For more information, see its documentation.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/behind-proxies.md          )

---

# データベースの統合

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# データベースの統合

Adding the capability to connect databases to Express apps is just a matter of loading an appropriate Node.js driver for the database in your app. This document briefly explains how to add and use some of the most popular Node.js modules for database systems in your Express app:

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
- [ElasticSearch](#elasticsearch)

These database drivers are among many that are available. For other options,
search on the [npm](https://www.npmjs.com/) site.

## Cassandra

**モジュール**: [cassandra-driver](https://github.com/datastax/nodejs-driver)

### インストール

```
$ npm install cassandra-driver
```

### 例

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

### インストール

```
$ npm install couchbase
```

### 例

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

**モジュール**: [nano](https://github.com/dscape/nano)

### インストール

```
$ npm install nano
```

### 例

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

**モジュール**: [levelup](https://github.com/rvagg/node-levelup)

### インストール

```
$ npm install level levelup leveldown
```

### 例

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

**モジュール**: [mysql](https://github.com/felixge/node-mysql/)

### インストール

```
$ npm install mysql
```

### 例

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

**モジュール**: [mongodb](https://github.com/mongodb/node-mongodb-native)

### インストール

```
$ npm install mongodb
```

### 例 (v3.*)

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

### 例 (v2.*)

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

MongoDB 用のオブジェクト・モデル・ドライバーが必要な場合は、[Mongoose](https://github.com/LearnBoost/mongoose) を参照してください。

## Neo4j

データベースを Express アプリケーションに接続できるようにするには、単にデータベースに適切な Node.js ドライバーをアプリケーションにロードするだけですみます。本書では、データベース・システム用の最も一般的な Node.js モジュールを Express アプリケーションに追加して使用する方法について簡単に説明します。

### インストール

```
$ npm install neo4j-driver
```

### 例

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

**モジュール**: [oracledb](https://github.com/oracle/node-oracledb)

### インストール

NOTE: [See installation prerequisites](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### 例

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

**モジュール**: [pg-promise](https://github.com/vitaly-t/pg-promise)

### インストール

```
$ npm install pg-promise
```

### 例

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

**モジュール**: [redis](https://github.com/mranney/node_redis)

### インストール

```
$ npm install redis
```

### 例

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

**モジュール**: [tedious](https://github.com/tediousjs/tedious)

### インストール

```
$ npm install tedious
```

### 例

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

**モジュール**: [sqlite3](https://github.com/mapbox/node-sqlite3)

### インストール

```
$ npm install sqlite3
```

### 例

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

**モジュール**: [elasticsearch](https://github.com/elastic/elasticsearch-js)

### インストール

```
$ npm install elasticsearch
```

### 例

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/database-integration.md          )

---

# Express のデバッグ

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Express のデバッグ

Express で使用されているすべての内部ログを表示するには、アプリケーションの起動時に `DEBUG` 環境変数を `express:*` に設定します。

```
$ DEBUG=express:* node index.js
```

Windows では、対応するコマンドを使用します。

```
> $env:DEBUG = "express:*"; node index.js
```

[express ジェネレーター](https://expressjs.com/ja/starter/generator.html) で生成されるデフォルトのアプリケーションでこのコマンドを実行すると、以下の出力が表示されます。

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

その後、アプリケーションに対して要求が出されると、Express コードで指定された次のログが表示されます。

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

ルーター実装からのログのみを表示するには、`DEBUG` の値を `express:router` に設定します。同様に、アプリケーション実装からのログのみを表示するには、`DEBUG` を `express:application` に設定します。その他についても同様に設定します。 Likewise, to see logs only from the application implementation, set the value of `DEBUG` to `express:application`, and so on.

## expressによって生成されるアプリケーション

`express` コマンドによって生成されるアプリケーションも `debug` モジュールを使用します。そのデバッグ名前空間はアプリケーションの名前に設定されます。

例えば、`$ express sample-app` を使用してアプリケーションを生成する場合、次のコマンドを使用してデバッグ・ステートメントを有効にすることができます。

```
$ DEBUG=sample-app:* node ./bin/www
```

名前のコンマ区切りリストを割り当てることで、複数のデバッグ名前空間を指定できます。

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

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/debugging.md          )

---

# エラー処理

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# エラー処理

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## エラーのキャッチ

Expressがルート・ハンドラとミドルウェアの実行中に発生するすべてのエラーを確実にキャッチすることが重要です。

ルート・ハンドラとミドルウェア内の同期コードで発生するエラーは、余分な作業を必要としません。同期コードがエラーをスローすると、Expressはそれをキャッチして処理します。 例えば： If synchronous code throws an error, then Express will
catch and process it. For example:

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

ルート・ハンドラとミドルウェアによって呼び出された非同期関数から返されたエラーについては、それらを`next()`関数に渡す必要があります。ここでExpressはそれらをキャッチして処理します。例えば：  For example:

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

`next()` 関数に (ストリング `'route'` を除く) 何らかを渡すと、Express は、現在のリクエストでエラーが発生したと想定して、エラーが発生していない残りのすべての処理のルーティングとミドルウェア関数をスキップします。そのエラーを何らかの方法で渡す場合は、次のセクションで説明するようにエラー処理ルートを作成する必要があります。

シーケンス内のコールバックにデータがなく、エラーのみが発生する場合は、次のようにこのコードを単純化できます。

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

上記の例では`fs.writeFile`のコールバックとして`next`が提供されています。これはエラーの有無にかかわらず呼び出されます。エラーがなければ、2番目のハンドラが実行されます。それ以外の場合、Expressはエラーをキャッチして処理します。 If there is no error, the second
handler is executed, otherwise Express catches and processes the error.

ルート・ハンドラまたはミドルウェアによって呼び出された非同期コードで発生したエラーをキャッチして、Expressに渡して処理する必要があります。例えば： For example:

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

上記の例では、`try ... catch`ブロックを使用して非同期コードのエラーを捕捉してExpressに渡しています。`try ... catch`ブロックが省略された場合、Expressは同期ハンドラ・コードの一部ではないため、エラーをキャッチしません。

Promiseを使って`try..catch`ブロックのオーバーヘッドを避けるか、Promiseを返す関数を使うとき。例えば：  For example:

```
app.get('/', (req, res, next) => {
  Promise.resolve().then(() => {
    throw new Error('BROKEN')
  }).catch(next) // Errors will be passed to Express.
})
```

Promiseは自動的に同期エラーと拒否されたPromiseをキャッチするので、catchハンドラに最初の引数としてエラーが与えられ、最終的なcatchハンドラとして`next`を指定するだけで、Expressはエラーをキャッチします。

また、非同期コードを単純なものに減らすことで、同期エラーのキャッチに依存する一連のハンドラを使用することもできます。例えば： For example:

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
call. 上の例は`readFile`呼び出しからの簡単なステートメントをいくつか持っています。`readFile`でエラーが発生した場合、エラーをExpressに渡します。そうでなければ、チェーン内の次のハンドラで同期エラー処理の世界に素早く戻ります。次に、上記の例ではデータを処理しようとしています。これが失敗すると、同期エラーハンドラはそれをキャッチします。 この処理を`readFile`コールバックの中で行った場合、アプリケーションは終了し、Expressのエラーハンドラは実行されません。 Then, the example above tries to process the data. If this fails, then the
synchronous error handler will catch it. If you had done this processing inside
the `readFile` callback, then the application might exit and the Express error
handlers would not run.

どちらの方法を使用しても、Expressのエラーハンドラを呼び出す場合や、アプリケーションを存続させる場合は、Expressがエラーを受け取るようにする必要があります。

## デフォルトのエラー処理

Expressには、アプリケーションで発生する可能性のあるエラーを処理するビルトインエラーハンドラが付属しています。 このデフォルトのエラー処理ミドルウェア関数は、ミドルウェア関数スタックの最後に追加されます。 This default error-handling middleware function is added at the end of the middleware function stack.

`next()`にエラーを渡し、カスタムエラーハンドラでそれを処理しない場合、それは組み込みのエラーハンドラによって処理されます。エラーはスタックトレースを使用してクライアントに書き込まれます。スタックトレースは本番環境には含まれていません。 The stack trace is not included
in the production environment.

プロダクションモードでアプリケーションを実行するには、環境変数`NODE_ENV`を` production`に設定します。</div>

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

レスポンスの記述を開始した後でエラーを伴って`next()`を呼び出すと（例えば、クライアントへの応答をストリーミング中にエラーが発生した場合）、Expressのデフォルトエラーハンドラは接続を閉じてリクエストを失敗します。

したがって、カスタムエラーハンドラを追加するときは、ヘッダーがすでにクライアントに送信されているときに、デフォルトのExpressエラーハンドラに委任する必要があります。

```
function errorHandler (err, req, res, next) {
  if (res.headersSent) {
    return next(err)
  }
  res.status(500)
  res.render('error', { error: err })
}
```

カスタムエラー処理ミドルウェアが存在していても、コード内でエラーが2回以上発生したときに`next()`を呼び出すと、デフォルトのエラーハンドラがトリガされることに注意してください。

Other error handling middleware can be found at [Express middleware](https://expressjs.com/ja/resources/middleware.html).

## エラー処理を記述する

エラー処理ミドルウェア関数は、その他のミドルウェア関数と同じ方法で定義しますが、エラー処理関数の引数が3つではなく、4つ `(err、req、res、next)` であることが例外です。次に例を示します。 For example:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

エラー処理ミドルウェアは、その他の `app.use()` およびルート呼び出しの後で最後に定義します。次に例を示します。

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

ミドルウェア関数の中からの応答は、HTML エラー・ページ、単純なメッセージ、または JSON ストリングなど、任意の形式にすることができます。

組織的な (および高水準フレームワークの) 目的で、通常のミドルウェア関数と同じように、複数のエラー処理のミドルウェア関数を定義できます。例えば、`XHR` を使用する要求と、使用しない要求のためのエラー・ハンドラーを定義するには、以下のコマンドを使用します。 For example, to define an error-handler
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

この例では、汎用の `logErrors` が要求とエラーの情報を `stderr` に書き込む可能性があります。次に例を示します。

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

また、この例では、`clientErrorHandler` は次のように定義されます。この場合、エラーは明示的に次のエラーに渡されます。

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

「catch-all」`errorHandler` 関数は、次のように実装されます。

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

複数のコールバック関数を使用するルート・ハンドラーがある場合、`route` パラメーターを使用して、次のルート・ハンドラーまでスキップできます。次に例を示します。 For example:

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

この例では、`getPaidContent` ハンドラーはスキップされますが、`/a_route_behind_paywall` の `app` にある残りのハンドラーはすべて引き続き実行されます。

Calls to `next()` and `next(err)` indicate that the current handler is complete and in what state.  `next()` および `next(err)` の呼び出しは、現在のハンドラーが完了したことと、その状態を示します。`next(err)` は、上記のようにエラーを処理するようにセットアップされたハンドラーを除き、チェーン内の残りのハンドラーをすべてスキップします。

    [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/error-handling.md          )

---

# Express 4 への移行

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Express 4 への移行

## 概説

Express 4 では、Express 3 とは互換性の *ない* 変更が行われています。つまり、依存関係にある Express のバージョンを更新すると、既存の Express 3 アプリケーションは機能しません。 That means an existing Express 3 app will *not* work if you update the Express version in its dependencies.

この記事では以下の内容を扱います。

- [Express 4 における変更点](#changes)
- Express 3 アプリケーションを Express 4 に移行する[例](#example-migration)
- [Express 4 アプリケーション・ジェネレーターへのアップグレード](#app-gen)

## Express 4 における変更点

Express 4 では、いくつかの大きな変更が行われています。

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [ルーティング・システムの変更。](#routing)
- [その他の各種変更。](#other-changes)

以下も参照してください。

- [4.x の新機能](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [3.x から 4.x への移行](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Express コアおよびミドルウェア・システムの変更

Express 4 は、Connect に依存しなくなり、`express.static` 関数を除くすべての標準装備ミドルウェアをコアから削除しました。つまり、Express は独立したルーティングおよびミドルウェアの Web フレームワークになり、Express のバージョン管理とリリースはミドルウェア更新の影響を受けません。 This means that
Express is now an independent routing and middleware web framework, and
Express versioning and releases are not affected by middleware updates.

標準装備ミドルウェアがないため、アプリケーションの実行に必要なすべてのミドルウェアを明示的に追加する必要があります。そのためには、単に以下のステップを実行してください。 Simply follow these steps:

1. モジュールをインストールします。`npm install --save <module-name>`
2. アプリケーションでモジュールを要求します。`require('module-name')`
3. モジュールの資料に従ってモジュールを使用します。`app.use( ... )`

次の表に、Express 3 のミドルウェアと、それぞれに対応する Express 4 のミドルウェアをリストします。

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

Express 4 のミドルウェアの完全なリストは、[ここ](https://github.com/senchalabs/connect#middleware)を参照してください。

ほとんどの場合、旧バージョン 3 のミドルウェアを単に Express 4 のミドルウェアに置き換えるだけですみます。詳細については、GitHub でモジュールの資料を参照してください。 For details, see the module documentation in
GitHub.

#### app.useがパラメーターを受け入れます

バージョン 4 では、変数パラメーターを使用して、ミドルウェア関数がロードされるパスを定義し、ルート・ハンドラーからパラメーターの値を読み取ることができます。
次に例を示します。
For example:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### ルーティング・システム

アプリケーションがルーティング・ミドルウェアを暗黙的にロードするようになったため、`router` ミドルウェアに関してミドルウェアがロードされる順序を考慮する必要がなくなりました。

ルートの定義方法は変わりませんが、ルーティング・システムには、ルートの編成に役立つ 2 つの新機能があります。

- 新しいメソッド `app.route()` は、ルート・パスのチェーン可能なルート・ハンドラーを作成します。
- 新しいクラス `express.Router` は、モジュール式のマウント可能なルート・ハンドラーを作成します。

#### app.route()メソッド

新しい `app.route()` メソッドを使用すると、ルート・パスのチェーン可能なルート・ハンドラーを作成できます。パスは単一の場所で指定されるため、モジュール式のルートを作成すると、便利であるほか、冗長性とタイプミスを減らすことができます。ルートについて詳しくは、[Router()資料](https://expressjs.com/ja/4x/api.html#router)を参照してください。 Because the path is specified in a single location, creating modular routes is helpful, as is reducing redundancy and typos. For more
information about routes, see [Router()documentation](https://expressjs.com/ja/4x/api.html#router).

次に、`app.route()` 関数を使用して定義された、チェーニングされたルート・ハンドラーの例を示します。

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

#### express.Routerクラス

ルートの編成に役立つもう 1 つの機能は、新しいクラス `express.Router` です。これを使用すると、モジュール式のマウント可能なルート・ハンドラーを作成できます。`Router` インスタンスは、完全なミドルウェアおよびルーティング・システムです。そのため、よく「ミニアプリケーション」と呼ばれます。 A `Router` instance is a complete middleware and
routing system; for this reason it is often referred to as a “mini-app”.

次の例では、ルーターをモジュールとして作成し、その中にミドルウェアをロードして、いくつかのルートを定義し、それをメインアプリケーションのパスにマウントします。

例えば、アプリケーション・ディレクトリーに次の内容で `birds.js` というルーター・ファイルを作成します。

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

次に、ルーター・モジュールをアプリケーションにロードします。

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

これで、アプリケーションは、`/birds` および `/birds/about` のパスに対する要求を処理できるようになり、ルートに固有の `timeLog` ミドルウェアを呼び出します。

### その他の変更点

次の表に、Express 4 におけるその他の小規模ながらも重要な変更点をリストします。

| オブジェクト | 説明 |
| --- | --- |
| Node.js | Express 4 には、Node.js 0.10.x 以降が必要です。Node.js 0.8.x に対するサポートは除去されました。 |
| http.createServer() | httpモジュールは、このモジュールを直接処理する必要がある場合を除き、不要になりました (socket.io/SPDY/HTTPS)。アプリケーションは、app.listen()関数を使用して開始できます。
 The app can be started by using theapp.listen()function. |
| app.configure() | Theapp.configure()function has been removed.app.configure()関数は削除されました。環境を検出して、アプリケーションを適宜に構成するには、process.env.NODE_ENV関数またはapp.get('env')関数を使用してください。 |
| json spaces | json spacesアプリケーション・プロパティーは、Express 4 ではデフォルトで無効になっています。 |
| req.accepted() | req.accepts()、req.acceptsEncodings()、req.acceptsCharsets()、およびreq.acceptsLanguages()を使用してください。 |
| res.location() | 相対 URL を解決しなくなりました。 |
| req.params | 以前は配列でしたが、現在ではオブジェクトになりました。 |
| res.locals | 以前は関数でしたが、現在ではオブジェクトになりました。 |
| res.headerSent | res.headersSentに変更されました。 |
| app.route | 今後はapp.mountpathとして使用できます。 |
| res.on('header') | 削除されました。 |
| res.charset | 削除されました。 |
| res.setHeader('Set-Cookie', val) | Functionality is now limited to setting the basic cookie value.
機能が基本的な Cookie 値の設定に限定されるようになりました。機能を追加するには、res.cookie()を使用してください。 |

## 移行の例

次に、Express 3 アプリケーションを Express 4 に移行する例を示します。
使用しているファイルは、`app.js` および `package.json` です。
The files of interest are `app.js` and `package.json`.

### バージョン 3 アプリケーション

#### app.js

次の `app.js` ファイルを使用する Express v.3 アプリケーションがあるとします。

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

付随するバージョン 3 の `package.json` ファイルの内容は次のようになります。

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

### プロセス

移行プロセスを開始するには、次のコマンドを使用して、Express 4 アプリケーションに必要なミドルウェアをインストールし、Express と Pug をそれぞれの最新バージョンに更新します。

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

`app.js` に以下の変更を加えます。

1. 標準装備の Express ミドルウェア関数 `express.favicon`、`express.logger`、`express.methodOverride`、`express.session`、`express.bodyParser`、および `express.errorHandler` は `express` オブジェクトで使用できなくなりました。代わりの関数を手動でインストールして、アプリケーションにロードする必要があります。 You must install their alternatives
  manually and load them in the app.
2. You no longer need to load the `app.router` function.
  `app.router` 関数をロードする必要がなくなりました。この関数は有効な Express 4 アプリケーション・オブジェクトではないため、`app.use(app.router);` コードを削除してください。
3. ミドルウェア関数が正しい順序でロードされていることを確認してください。つまり、アプリケーション・ルートをロードした後で `errorHandler` をロードしてください。

### バージョン 4 アプリケーション

#### package.json

上記の `npm` コマンドを実行すると、`package.json` が次のように更新されます。

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

Then, remove invalid code, load the required middleware, and make other
changes as necessary. The `app.js` file will look like this:

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

`http` モジュール (socket.io/SPDY/HTTPS) を直接処理する必要がある場合を除き、このモジュールをロードする必要はありません。次のようにして、アプリケーションを簡単に開始できます。

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### アプリケーションの実行

これで移行プロセスは完了して、アプリケーションは Express 4 アプリケーションになりました。確認するには、次のコマンドを使用してアプリケーションを開始します。 To confirm, start the app by using the following command:

```
$ node .
```

[http://localhost:3000](http://localhost:3000) をロードして、Express 4 によってレンダリングされるホーム・ページを確認します。

## Express 4 アプリケーション・ジェネレーターへのアップグレード

Express アプリケーションを生成するためのコマンド・ライン・ツールは引き続き `express` ですが、新規バージョンにアップグレードするには、Express 3 アプリケーション・ジェネレーターをアンインストールしてから、新しい `express-generator` をインストールする必要があります。

### インストール

システムに Express 3 アプリケーション・ジェネレーターがインストールされている場合は、次のようにしてアンインストールする必要があります。

```
$ npm uninstall -g express
```

ファイルおよびディレクトリーの特権が構成されている方法によっては、このコマンドを `sudo` で実行することが必要になる場合があります。

次に、新しいジェネレーターをインストールします。

```
$ npm install -g express-generator
```

ファイルおよびディレクトリーの特権が構成されている方法によっては、このコマンドを `sudo` で実行することが必要になる場合があります。

これで、システム上の `express` コマンドは Express 4 ジェネレーターに更新されました。

### アプリケーション・ジェネレーターの変更

コマンドのオプションと使用法の大部分は以前と同じですが、以下の例外があります。

- `--sessions` オプションを削除しました。
- `--jshtml` オプションを削除しました。
- [Hogan.js](http://twitter.github.io/hogan.js/) をサポートするために `--hogan` オプションを追加しました。

### 例

次のコマンドを実行して、Express 4 アプリケーションを作成します。

```
$ express app4
```

`app4/app.js` ファイルの内容を見ると、アプリケーションに必要な (`express.static` を除く) すべてのミドルウェア関数が独立したモジュールとしてロードされており、`router` ミドルウェアがアプリケーションに明示的にロードされなくなったことが分かります。

また、`app.js` ファイルが Node.js モジュールになったことも分かります。対照的に以前はジェネレーターによって生成されるスタンドアロン・モジュールでした。

依存関係をインストールした後、次のコマンドを使用してアプリケーションを開始します。

```
$ npm start
```

`package.json` ファイルで npm start スクリプトを見ると、アプリケーションを開始する実際のコマンドは `node ./bin/www` であることが分かります。これは、Express 3 では `node app.js` でした。

Express 4 ジェネレーターによって生成される `app.js` ファイルが Node.js モジュールになったため、(コードを変更しない限り) アプリケーションとして単独では開始できなくなりました。モジュールを Node.js ファイルにロードして、Node.js ファイルから開始する必要があります。この場合、Node.js ファイルは `./bin/www` です。 The module must be loaded in a Node.js file
and started via the Node.js file. The Node.js file is `./bin/www`
in this case.

Express アプリケーションの作成またはアプリケーションの開始のために、`bin` ディレクトリーも、拡張子のない `www` ファイルも必須ではありません。これらは単にジェネレーターが推奨するものであるため、ニーズに合わせて自由に変更してください。 They are
just suggestions made by the generator, so feel free to modify them to suit your
needs.

`www` ディレクトリーを削除して、処理を「Express 3 の方法」で実行するには、`app.js` ファイルの最後にある `module.exports = app;` という行を削除して、その場所に以下のコードを貼り付けます。

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

次のコードを使用して `debug` モジュールを `app.js` ファイルの先頭にロードしたことを確認します。

```
var debug = require('debug')('app4')
```

次に、`package.json` ファイル内の `"start": "node ./bin/www"` を `"start": "node app.js"` に変更します。

You have now moved the functionality of `./bin/www` back to
`app.js`. これで、`./bin/www` の機能を `app.js` に戻しました。この変更は推奨されるものではありませんが、この演習により、`./bin/www` ファイルの仕組みと、`app.js` ファイルが単独で開始されなくなった理由を理解できます。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/guide/migrating-4.md          )
