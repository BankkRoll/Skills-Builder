# Express hinter Proxys and more

# Express hinter Proxys

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# Express hinter Proxys

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

Bei der Ausführung einer Express-Anwendung hinter einem Proxy legen Sie die Anwendungsvariable `trust proxy` (mithilfe von [app.set()](https://expressjs.com/de/4x/api.html#app.set)) auf einen der in der folgenden Tabelle enthaltenen Werte fest:

| Typ | Wert |
| --- | --- |
| Boolesch | Wenntrueangegeben wird, wird die IP-Adresse des Clients als der äußerst rechte Eintrag im HeaderX-Forwarded-*interpretiert.Wennfalseangegeben wird, wird die Anwendung als direkte Verbindung zum Internet gesehen. Die IP-Adresse des Clients wird dann vonreq.connection.remoteAddressabgeleitet. Dies ist die Standardeinstellung.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7Sie können IP-Adressen wie folgt festlegen:app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arraySobald die Werte angegeben wurden, werden die betreffenden IP-Adressen und Teilnetze aus dem Adressfeststellungsprozess ausgeschlossen. Die nicht vertrauenswürdige IP-Adresse, die am nächsten zum Anwendungsserver liegt, wird als IP-Adresse des Clients festgelegt. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| Zahl | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- Der Wert für [req.hostname](https://expressjs.com/de/api.html#req.hostname) wird vom Wert abgeleitet, der im Header `X-Forwarded-Host` festgelegt wurde. Dieser Wert kann vom Client oder Proxy festgelegt werden.</li>
- `X-Forwarded-Proto` kann vom Reverse Proxy festgelegt werden, um der Anwendung mitzuteilen, ob es sich um `https` oder `http` oder sogar um einen ungültigen Namen handelt. Dieser Wert wird durch [req.protocol](https://expressjs.com/de/api.html#req.protocol) abgebildet.
- Als Werte für [req.ip](https://expressjs.com/de/api.html#req.ip) und [req.ips](https://expressjs.com/de/api.html#req.ips) wird die Liste der Adressen aus `X-Forwarded-For` herangezogen.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/behind-proxies.md          )

---

# Datenbankintegration

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# Datenbankintegration

Die Herstellung einer Verbindung zwischen Datenbanken und Express-Anwendungen erfolgt einfach durch Laden eines geeigneten Node.js-Treibers für die Datenbank in Ihre Anwendung. In diesem Dokument wird in Kurzform beschrieben, wie einige der gängigsten Node.js-Module für Datenbanksysteme Ihrer Express-Anwendung hinzugefügt und verwendet werden:

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

Diese Datenbanktreiber sind neben zahlreichen anderen Treibern verfügbar. Weitere Optionen finden Sie auf der [npm](https://www.npmjs.com/)-Site.

## Cassandra

**Modul**: [cassandra-driver](https://github.com/datastax/nodejs-driver) **Installation**

### Installation

```
$ npm install cassandra-driver
```

### Beispiel

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

### Beispiel

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

**Modul**: [nano](https://github.com/dscape/nano) **Installation**

### Installation

```
$ npm install nano
```

### Beispiel

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

**Modul**: [levelup](https://github.com/rvagg/node-levelup) **Installation**

### Installation

```
$ npm install level levelup leveldown
```

### Beispiel

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

**Modul**: [mysql](https://github.com/felixge/node-mysql/) **Installation**

### Installation

```
$ npm install mysql
```

### Beispiel

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

**Modul**: [mongodb](https://github.com/mongodb/node-mongodb-native) **Installation**

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

Wenn Sie nach einem Objektmodelltreiber für MongoDB suchen, schauen Sie unter [Mongoose](https://github.com/LearnBoost/mongoose) nach.

## Neo4j

**Module**: [neo4j-driver](https://github.com/neo4j/neo4j-javascript-driver)

### Installation

```
$ npm install neo4j-driver
```

### Beispiel

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

**Modul**: [oracledb](https://github.com/oracle/node-oracledb)

### Installation

Anmerkung: [Siehe Installations-Voraussetzungen](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### Beispiel

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

**Modul**: [pg-promise](https://github.com/vitaly-t/pg-promise) **Installation**

### Installation

```
$ npm install pg-promise
```

### Beispiel

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

**Modul**: [redis](https://github.com/mranney/node_redis) **Installation**

### Installation

```
$ npm install redis
```

### Beispiel

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

### Beispiel

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

**Modul**: [sqlite3](https://github.com/mapbox/node-sqlite3) **Installation**

### Installation

```
$ npm install sqlite3
```

### Beispiel

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

**Modul**: [elasticsearch](https://github.com/elastic/elasticsearch-js) **Installation**

### Installation

```
$ npm install elasticsearch
```

### Beispiel

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/database-integration.md          )

---

# Debugging bei Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Debugging bei Express

Wenn Sie alle in Express verwendeten internen Protokolle anzeigen wollen, legen Sie beim Starten Ihrer Anwendung die Umgebungsvariable `DEBUG` auf `express:*` fest.

```
$ DEBUG=express:* node index.js
```

Verwenden Sie unter Windows den entsprechenden Befehl.

```
> $env:DEBUG = "express:*"; node index.js
```

Die Ausführung dieses Befehls für die durch [express generator](https://expressjs.com/de/starter/generator.html) generierte Standardanwendung resultiert in folgender Ausgabe:

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

Bei einer Anforderung an die Anwendung sind die Protokolle im Express-Code angegeben:

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

Wenn Sie nur die Protokolle von der Routerimplementierung sehen wollen, legen Sie den Wert für `DEBUG` auf `express:router` fest. Gleichermaßen gilt: Wenn Sie nur die Protokolle von der Anwendungsimplementierung sehen wollen, legen Sie den Wert für `DEBUG` auf `express:application` fest, usw.

## Vonexpressgenerierte Anwendungen

An application generated by the `express` command uses the `debug` module and its debug namespace is scoped to the name of the application.

Beispiel: Wenn Sie die Anwendung mit `$ express sample-app` generiert haben, können Sie die Debuganweisungen mit dem folgenden Befehl aktivieren:

```
$ DEBUG=sample-app:* node ./bin/www
```

Sie können mehrere Debug-Namespaces in einer durch Kommas getrennten Namensliste angeben:

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

Hinweis

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[util.inspect()](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/debugging.md          )

---

# Fehlerbehandlung

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# Fehlerbehandlung

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## Catching Errors

It’s important to ensure that Express catches all errors that occur while
running route handlers and middleware.

Errors that occur in synchronous code inside route handlers and middleware
require no extra work. If synchronous code throws an error, then Express will
catch and process it. Beispiel:

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

Middlewarefunktionen für die Fehlerbehandlung werden in derselben Weise definiert wie andere Middlewarefunktionen, nur, dass Fehlerbehandlungsfunktionen vier anstatt drei Argumente aufweisen:
`(err, req, res, next)`.  Beispiel:

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

Middleware für die Fehlerbehandlung wird ganz zuletzt nach allen anderen `app.use()`- und Weiterleitungsaufrufen definiert.
Beispiel:

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

If `getUserById` throws an error or rejects, `next` will be called with either
the thrown error or the rejected value. If no rejected value is provided, `next`
will be called with a default Error object provided by the Express router.

Wenn Sie Übergaben an die Funktion `next()` vornehmen (außer die Zeichenfolge `'route'`), sieht Express die aktuelle Anforderung als Fehler an und überspringt alle verbleibenden fehlerfreien Behandlungsroutinen und Middlewarefunktionen.

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

Bei einem Routenhandler mit mehreren Callback-Funktionen können Sie den Parameter `route` verwenden, um den nächsten Routenhandler zu überspringen. Beispiel:

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
that return promises.  Beispiel:

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
catching, by reducing the asynchronous code to something trivial. Beispiel:

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

## Die Standardfehlerbehandlungsroutine (Default Error Handler)

Express ist bereits mit einer integrierten Fehlerbehandlungsroutine ausgestattet, mit der alle in der Anwendung festgestellten Fehler gehandhabt werden können. Diese Middleware für die Fehlerbehandlung wird am Ende des Middleware-Funktionsstack hinzugefügt.

Wenn Sie einen Fehler an `next()` übergeben und diesen nicht mit einem Error-Handler bearbeiten, wird dieser über den integrierten Error-Handler bearbeitet. Der Fehler wird mit dem Stack-Trace zum Client geschrieben. Der Stack-Trace ist in der Produktionsumgebung nicht verfügbar.

Legen Sie die Umgebungsvariable `NODE_ENV` auf `production` fest, um die Anwendung im Produktionsmodus auszuführen.

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

Wenn `next()` mit einem Fehler aufgerufen wird, nachdem Sie mit dem Schreiben der Antwort begonnen haben (z. B., wenn Sie beim Streamen der Antwort zum Client einen Fehler feststellen), schließt die Standardfehlerbehandlungsroutine in Express die Verbindung, und die Anforderung schlägt fehl.

Wenn Sie also einen angepassten Error-Handler hinzufügen, empfiehlt es sich, eine Delegierung zur Standardfehlerbehandlungsroutine in Express vorzunehmen, wenn die Header bereits an den Client gesendet wurden:

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/de/resources/middleware.html).

## Writing error handlers

Define error-handling middleware functions in the same way as other middleware functions,
except error-handling functions have four arguments instead of three:
`(err, req, res, next)`. Beispiel:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

You define error-handling middleware last, after other `app.use()` and routes calls; for example:

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

Antworten von der Middlewarefunktion können das von Ihnen gewünschte Format aufweisen wie beispielsweise eine Fehlerseite im HTML-Format, eine einfache Nachricht oder eine JSON-Zeichenfolge.

Für organisatorische Zwecke (und Frameworks der höheren Ebene) können Sie mehrere Middlewarefunktionen für die Fehlerbehandlung definieren, wie Sie dies bei regulären Middlewarefunktionen auch tun würden. Wenn Sie beispielsweise eine Fehlerbehandlungsroutine (Error-Handler) für Anforderungen über `XHR` und andere Anforderungen definieren wollen, können Sie die folgenden Befehle verwenden:

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

In diesem Beispiel kann die generische `logErrors`-Funktion Anforderungs- und Fehlerinformationen in `stderr` schreiben:

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

In diesem Beispiel wird `clientErrorHandler` wie folgt definiert. In diesem Fall wird der Fehler explizit an den nächsten Error-Handler übergeben:

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

Die `errorHandler`-Funktion “catch-all” kann wie folgt implementiert werden:

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

If you have a route handler with multiple callback functions, you can use the `route` parameter to skip to the next route handler. Beispiel:

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

In diesem Beispiel wird der Handler `getPaidContent` übersprungen. Alle verbleibenden Handler in `app` für `/a_route_behind_paywall` werden jedoch weiter ausgeführt.

Aufrufe zu `next()` und `next(err)` geben an, dass der aktuelle Handler abgeschlossen ist und welchen Status er aufweist.  Durch `next(err)` werden alle verbleibenden Handler in der Kette übersprungen. Ausgenommen hiervor sind die Handler, die konfiguriert sind, um Fehler wie oben beschrieben zu behandeln.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/error-handling.md          )

---

# Wechsel zu Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Wechsel zu Express 4

## Überblick

Express 4 bietet grundlegende Veränderungen im Vergleich zu Express 3. Das bedeutet, dass eine Express 3-Anwendung nicht funktioniert, wenn Sie die Express-Version in ihren Abhängigkeiten aktualisieren.

In diesem Beitrag werden folgende Themen behandelt:

- [Änderungen in Express 4](#changes)
- [Beispiel](#example-migration) für die Migration einer Express 3-Anwendung auf Express 4
- [Upgrade auf den Express 4 App Generator](#app-gen)

## Änderungen in Express 4

In Express 4 wurden einige signifikante Änderungen vorgenommen:

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [Änderungen am Weiterleitungssystem (Routingsystem).](#routing)
- [Weitere Änderungen.](#other-changes)

Siehe hierzu auch:

- [Neue Features/Funktionen in 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migration von 3.x auf 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Änderungen am Express-Core- und Middlewaresystem

In Express 4 bestehen keine Abhängigkeiten mehr zu Connect. Alle integrierten Middlewarefunktionen werden aus dem Core entfernt. Ausgenommen hiervon ist die Funktion `express.static`. Das bedeutet, dass Express nun ein unabhängiges Routing- und Middleware-Web-Framework ist und Express-Versionierung und -Releases von Middleware-Updates nicht betroffen sind.

Ohne integrierte Middleware müssen Sie explizit alle Middlewarefunktionen hinzufügen, die für die Ausführung Ihrer Anwendung erforderlich sind. Befolgen Sie einfach diese Schritte:

1. Installieren des Moduls: `npm install --save <modulname>`
2. Anfordern des Moduls in Ihrer Anwendung: `require('modulname')`
3. Verwendung des Moduls gemäß Dokumentation: `app.use( ... )`

In der folgenden Tabelle sind Express 3-Middlewarefunktionen und deren Entsprechungen in Express 4 aufgelistet.

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

Hier finden Sie die [komplette Liste](https://github.com/senchalabs/connect#middleware) der Express 4-Middleware.

In den meisten Fällen können Sie einfach nur die Middleware der alten Version 3 durch deren Entsprechung in Express 4 ersetzen. Details hierzu finden Sie in der modulspezifischen Dokumentation in GitHub.

#### app.useakzeptiert Parameter.

In Version 4 können Sie über einen Variablenparameter den Pfad definieren, in den Middlewarefunktionen geladen werden. Dann können Sie den Wert des Parameters aus dem Routenhandler laden.
Beispiel:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### Das Routingsystem

Anwendungen laden nun implizit Routing-Middleware. Sie müssen sich also keine Gedanken mehr über die Reihenfolge machen, in der die Middleware in Bezug auf die `router`-Middleware geladen wird.

Das Routingsystem verfügt jedoch über zwei neue Funktionen, die beim Organisieren Ihrer Weiterleitungen helfen:

- Die neue Methode `app.route()` zum Erstellen verkettbarer Routenhandler für einen Weiterleitungspfad
- Die neue Klasse `express.Router` zum Erstellen modular einbindbarer Routenhandler

#### Die Methodeapp.route()

Die neue Methode `app.route()` hilft beim Erstellen verkettbarer Routenhandler für einen Weiterleitungspfad. Da der Pfad an einer einzelnen Position angegeben wird, ist das Erstellen modularer Weiterleitungen hilfreich, da Redundanzen und Schreibfehler reduziert werden. Weitere Informationen zu Weiterleitungen finden Sie in der Dokumentation zu [Router()](https://expressjs.com/de/4x/api.html#router).

Dies ist ein Beispiel für verkettete Routenhandler, die mit der Funktion `app.route()` definiert werden.

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

#### Die Klasseexpress.Router

Eine weitere Funktion, die beim Organisieren von Weiterleitungen hilft, ist die neue Klasse `express.Router`. Über diese Klasse können Sie modular einbindbare Routenhandler erstellen. Eine `Router`-Instanz ist ein vollständiges Middleware- und Routingsystem. Aus diesem Grund wird diese Instanz oft auch als “Mini-App” bezeichnet.

Im folgenden Beispiel wird ein Router als Modul erstellt, Middleware in das Modul geladen, es werden Weiterleitungen definiert und das Modul letztendlich in einen Pfad in der Hauptanwendung eingebunden.

Beispiel: Erstellen Sie eine Routerdatei namens `birds.js` mit dem folgenden Inhalt im Anwendungsverzeichnis:

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

Laden Sie dann das Routermodul in die Anwendung:

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

Die Anwendung kann nun Anforderungen an die Pfade `/birds` und `/birds/about` bearbeiten und ruft die Middleware `timeLog` auf, die speziell für diese Weiterleitung bestimmt ist.

### Weitere Änderungen

In der folgenden Tabelle sind andere kleinere, aber trotzdem wichtige Änderungen in Express 4 aufgeführt:

| Objekt | Beschreibung |
| --- | --- |
| Node.js | Express 4 erfordert Node.js 0.10.x oder höher und unterstützt nicht mehr Node.js 0.8.x. |
| http.createServer() | Das Modulhttpwird nicht mehr benötigt, es sei denn, Sie müssen direkt mit dem Modul arbeiten (socket.io/SPDY/HTTPS). Die Anwendung kann mithilfe der Funktionapp.listen()gestartet werden. |
| app.configure() | Die Funktionapp.configure()wurde entfernt.  Verwenden Sie die Funktionprocess.env.NODE_ENVoderapp.get('env'), um die Umgebung zu erkennen und die Anwendung entsprechend zu konfigurieren. |
| json spaces | Die Anwendungseigenschaftjson spacesist in Express 4 standardmäßig inaktiviert. |
| req.accepted() | Verwenden Siereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets()undreq.acceptsLanguages(). |
| res.location() | Löst keine relativen URLs mehr auf. |
| req.params | War bisher ein Array, ist nun ein Objekt. |
| res.locals | War bisher eine Funktion, ist nun ein Objekt. |
| res.headerSent | Geändert inres.headersSent. |
| app.route | Nun verfügbar alsapp.mountpath. |
| res.on('header') | Entfernt. |
| res.charset | Entfernt. |
| res.setHeader('Set-Cookie', val) | Die Funktionalität ist nun auf die Einstellung des Basis-Cookiewerts begrenzt. Verwenden Sieres.cookie(), um weitere Funktionalität zu erhalten. |

## Beispiel für eine Anwendungsmigration

Dies ist ein Beispiel für die Migration einer Express 3-Anwendung auf Express 4.
Die dabei interessanten Dateien sind `app.js` und `package.json`.

### Anwendung der Version 3

#### app.js

Es wird eine Express v.3-Anwendung mit der folgenden Datei `app.js` angenommen:

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

Die zugehörige `package.json`-Datei der Version 3 sieht in etwa wie folgt aus:

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

### Prozess

Beginnen Sie den Migrationsprozess mit der Installation der erforderlichen Middleware für die Express 4-Anwendung und der Aktualisierung von Express und Pug auf die aktuellen Versionen. Verwenden Sie hierzu den folgenden Befehl:

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

Nehmen Sie an `app.js` die folgenden Änderungen vor:

1. Die integrierten Express-Middlewarefunktionen `express.favicon`,
  `express.logger`, `express.methodOverride`,
  `express.session`, `express.bodyParser` und
  `express.errorHandler` sind im Objekt `express` nicht mehr verfügbar. Sie müssen deren Alternativen manuell installieren und in die Anwendung laden.
2. Sie müssen die Funktion `app.router` nicht mehr laden.
  Sie ist kein gültiges Express 4-Anwendungsobjekt. Entfernen Sie also den Code `app.use(app.router);`.
3. Stellen Sie sicher, dass die Middlewarefunktionen in der richtigen Reihenfolge geladen werden – laden Sie `errorHandler` nach dem Laden der Anwendungsweiterleitungen.

### Anwendung der Version 4

#### package.json

Durch Ausführung des Befehls `npm` wird `package.json` wie folgt aktualisiert:

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

Entfernen Sie dann ungültigen Code, laden Sie die erforderliche Middleware und nehmen Sie andere Änderungen nach Bedarf vor. Die Datei `app.js` sieht dann wie folgt aus:

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

Wenn Sie nicht direkt mit dem Modul `http` arbeiten müssen (socket.io/SPDY/HTTPS), ist das Laden des Moduls nicht erforderlich. Die Anwendung kann dann einfach wie folgt gestartet werden:

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Anwendung ausführen

Der Migrationsprozess ist abgeschlossen und die Anwendung ist nun eine Express 4-Anwendung. Zum Bestätigen starten Sie die Anwendung mit dem folgenden Befehl:

```
$ node .
```

Laden Sie [http://localhost:3000](http://localhost:3000) und sehen Sie, wie die Homepage von Express 4 wiedergegeben wird.

## Upgrade auf den Express 4 App Generator

Das Befehlszeilentool zum Generieren einer Express-Anwendung ist nach wie vor `express`. Für ein Upgrade auf die neue Version müssen Sie jedoch den Express 3 App Generator deinstallieren und dann den neuen Generator `express-generator` installieren.

### Installation

Wenn der Express 3 App Generator bereits auf Ihrem System installiert ist, müssen Sie diesen deinstallieren:

```
$ npm uninstall -g express
```

Abhängig davon, wie Ihre Datei- und Verzeichnissberechtigungen konfiguriert sind, müssen Sie diesen Befehl möglicherweise mit `sudo` ausführen.

Installieren Sie nun den neuen Generator:

```
$ npm install -g express-generator
```

Abhängig davon, wie Ihre Datei- und Verzeichnissberechtigungen konfiguriert sind, müssen Sie diesen Befehl möglicherweise mit `sudo` ausführen.

Nun wird der Befehl `express` auf Ihrem System auf den Express 4 App Generator aktualisiert.

### Änderungen am App Generator

Befehlsoptionen und -nutzung bleiben größtenteils unverändert. Es gelten jedoch folgende Ausnahmen:

- Option `--sessions` wurde entfernt.
- Option `--jshtml` wurde entfernt.
- Option `--hogan` wurde hinzugefügt, um [Hogan.js](http://twitter.github.io/hogan.js/) zu unterstützen.

### Beispiel

Führen Sie den folgenden Befehl aus, um eine Express 4-Anwendung zu erstellen:

```
$ express app4
```

Wenn Sie sich den Inhalt der Datei `app4/app.js` ansehen, werden Sie feststellen, dass alle Middlewarefunktionen (außer `express.static`), die für die Anwendung  erforderlich sind, als unabhängige Module geladen werden und die Middleware `router` nicht mehr explizit in die Anwendung geladen wird.

Sie werden auch feststellen, dass die Datei `app.js` nun ein Node.js-Modul ist – im Gegensatz zur eigenständigen Anwendung, die vom bisherigen Generator generiert wurde.

Starten Sie nach der Installation der Abhängigkeiten die Anwendung mit dem folgenden Befehl:

```
$ npm start
```

Wenn Sie sich das npm-Startscript in der Datei `package.json` näher ansehen, werden Sie feststellen, dass der eigentliche Befehl, der die Anwendung startet, `node ./bin/www` heißt. Dieser Befehl lautete in Express 3 `node app.js`.

Da die Datei `app.js`, die vom Express 4 Generator erstellt wurde, nun ein Node.js-Modul ist, kann dieses nicht mehr wie bisher unabhängig als Anwendung gestartet werden (es sei denn, Sie ändern den Code). Das Modul muss in eine Node.js-Datei geladen und über die Node.js-Datei gestartet werden. Die Node.js-Datei ist in diesem Fall `./bin/www`.

Weder das Verzeichnis `bin` noch die erweiterungslose Datei `www` ist für das Erstellen einer Express-Anwendung oder das Starten der Anwendung zwingend erforderlich. Dies sind lediglich Vorschläge des Generators. Sie können diese also je nach Ihren Anforderungen ändern.

Um das Verzeichnis `www` zu löschen und alles im “Express 3-Stil” zu belassen, löschen Sie die Zeile mit dem Eintrag `module.exports = app;` am Ende der Datei `app.js`. Fügen Sie dann stattdessen den folgenden Code an derselben Position ein:

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

Stellen Sie sicher, dass Sie das Modul `debug` am Anfang der Datei `app.js` laden. Verwenden Sie dazu den folgenden Code:

```
var debug = require('debug')('app4')
```

Ändern Sie als Nächstes `"start": "node ./bin/www"` in der Datei `package.json` in `"start": "node app.js"`.

Sie haben nun die Funktionalität von `./bin/www` wieder in `app.js` verschoben. Diese Änderung wird nicht empfohlen. Die Übung hat Ihnen jedoch geholfen, zu verstehen, wie die Datei `./bin/www` funktioniert und warum die Datei `app.js` nicht mehr automatisch gestartet wird.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/guide/migrating-4.md          )
