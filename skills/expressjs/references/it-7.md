# Express con i proxy and more

# Express con i proxy

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# Express con i proxy

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

Quando si esegue un’applicazione Express con un proxy, impostare (utilizzando [app.set()](https://expressjs.com/it/4x/api.html#app.set)) la variabile dell’applicazione `trust proxy` su uno dei valori elencati nella seguente tabella.

| Tipo | Valore |
| --- | --- |
| Booleano | Se impostato sutrue, l’indirizzo IP del client viene considerato come la voce a sinistra dell’intestazioneX-Forwarded-*.Se impostato sufalse, significa che l’applicazione abbia una connessione diretta a Internet e l’indirizzo IP del client sia arrivato dareq.connection.remoteAddress. Questa è l’impostazione predefinita.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7È possibile impostare gli indirizzi IP in uno dei seguenti modi:app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayQuando specificati, gli indirizzi IP o le subnet vengono esclusi dal processo di determinazione dell’indirizzo e l’indirizzo IP non attendibile più vicino al server delle applicazioni viene considerato come indirizzo IP del client. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| Numero | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- Il valore di [req.hostname](https://expressjs.com/it/api.html#req.hostname) viene rilevato dalla serie di valori nell’intestazione `X-Forwarded-Host`, la quale può essere impostata dal client o dal proxy.
- `X-Forwarded-Proto` può essere impostata dal proxy inverso per far capire all’applicazione se si tratta di `https` o `http` oppure di un nome non valido. Questo valore viene riportato da [req.protocol](https://expressjs.com/it/api.html#req.protocol).
- I valori [req.ip](https://expressjs.com/it/api.html#req.ip) e [req.ips](https://expressjs.com/it/api.html#req.ips) vengono popolati con l’elenco di indirizzi da `X-Forwarded-For`.

L’impostazione `trust proxy` viene implementata utilizzando il pacchetto [proxy-addr](https://www.npmjs.com/package/proxy-addr). Per ulteriori informazioni, consultare la relativa documentazione.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/behind-proxies.md          )

---

# Integrazione database

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# Integrazione database

L’aggiunta della funzionalità che consente di connettere i database alle applicazioni Express è solo un modo per caricare un driver Node.js appropriato per il database nell’applicazione. Questo documento spiega brevemente come aggiungere e utilizzare alcuni dei moduli Node.js più noti per i sistemi database nell’applicazione Express:

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

Questi driver di database sono tra quelli più disponibili. Per altre opzioni,
effettuare una ricerca nel sito [npm](https://www.npmjs.com/).

## Cassandra

**Modulo**: **Installazione** [cassandra-driver](https://github.com/datastax/nodejs-driver)

```
$ npm install cassandra-driver
```

### Esempio

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

```
$ npm install couchbase
```

### Esempio

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

**Modulo**: **Installazione** [nano](https://github.com/dscape/nano)

```
$ npm install nano
```

### Esempio

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

**Modulo**: **Installazione** [levelup](https://github.com/rvagg/node-levelup)

```
$ npm install level levelup leveldown
```

### Esempio

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

**Modulo**: **Installazione** [mysql](https://github.com/felixge/node-mysql/)

```
$ npm install mysql
```

### Esempio

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

**Modulo**: **Installazione** [mongodb](https://github.com/mongodb/node-mongodb-native)

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

Se si desidera un driver del modello oggetto per MongoDB, consultare [Mongoose](https://github.com/LearnBoost/mongoose).

## Neo4j

`
var apoc = require('apoc');apoc.query('match (n) return n').exec().then(
function (response) {
console.log(response);
},
function (fail) {
console.log(fail);
}
); `

```
$ npm install neo4j-driver
```

### Esempio

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

**Modulo**: [oracledb](https://github.com/oracle/node-oracledb)

NOTA: [Vedi i prerequisiti di installazione](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### Esempio

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

```
$ npm install pg-promise
```

### Esempio

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

**Modulo**: **Installazione** [redis](https://github.com/mranney/node_redis)

```
$ npm install redis
```

### Esempio

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

```
$ npm install tedious
```

### Esempio

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

**Modulo**: **Installazione** [sqlite3](https://github.com/mapbox/node-sqlite3)

```
$ npm install sqlite3
```

### Esempio

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

**Modulo**: **Installazione** [elasticsearch](https://github.com/elastic/elasticsearch-js)

```
$ npm install elasticsearch
```

### Esempio

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/database-integration.md          )

---

# Debug di Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Debug di Express

Per visualizzare tutti i log interni utilizzati in Express, impostare la variabile di ambiente `DEBUG` su
`express:*` quando si avvia l’applicazione.

```
$ DEBUG=express:* node index.js
```

Su Windows, utilizzare il comando corrispondente.

```
> $env:DEBUG = "express:*"; node index.js
```

L’esecuzione di questo comando sull’applicazione predefinita generata da [Programma di creazione express](https://expressjs.com/it/starter/generator.html) consentirà di stampare il seguente output:

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

Quando successivamente viene effettuata una richiesta all’applicazione, verranno visualizzati i log specificati nel codice Express:

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

Per visualizzare i log solo dall’implementazione router impostare il valore `DEBUG` su `express:router`. In modo simile, per visualizzare i log solo dall’implementazione dell’applicazione impostare il valore `DEBUG` su `express:application` e così via.

## Applicazioni generate daexpress

Un’applicazione generata dal comando `express` utilizza inoltre il modulo `debug` e il relativo spazio dei nomi di debug viene associato al nome dell’applicazione.

Ad esempio, se l’applicazione è stata generata con `$ express sample-app`, è possibile abilitare le istruzioni di debug con il seguente comando:

```
$ DEBUG=sample-app:* node ./bin/www
```

È possibile specificare più di uno spazio dei nomi di debug assegnando un elenco di nomi separati da virgola:

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

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/debugging.md          )

---

# Gestione degli errori

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# Gestione degli errori

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## Catching Errors

It’s important to ensure that Express catches all errors that occur while
running route handlers and middleware.

Errors that occur in synchronous code inside route handlers and middleware
require no extra work. If synchronous code throws an error, then Express will
catch and process it. Ad esempio:

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

Definire le funzioni middleware di gestione degli errori nello stesso modo in cui si definiscono altre funzioni middleware,
ad eccezione delle funzioni di gestione degli errori che hanno quattro argomenti invece di tre:
`(err, req, res, next)`.  Ad esempio:

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

Se si dispone di un gestore route con più funzioni di callback, è possibile utilizzare il parametro `route` per passare al successivo gestore route.
Ad esempio:

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

If `getUserById` throws an error or rejects, `next` will be called with either
the thrown error or the rejected value. If no rejected value is provided, `next`
will be called with a default Error object provided by the Express router.

Se si trasmette qualsiasi cosa alla funzione `next()` (ad eccezione della stringa `'route'`), Express considera la richiesta corrente come se contenesse errori e ignorerà qualsiasi altra funzione middleware e routing di non gestione degli errori restante.

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
middleware and pass them to Express for processing. Ad esempio:

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
that return promises.  Ad esempio:

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
catching, by reducing the asynchronous code to something trivial. Ad esempio:

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

## Il gestore errori predefinito

Express viene fornito insieme a un gestore degli errori integrato, il quale gestisce gli errori che potrebbero verificarsi nell’applicazione. Questa funzione middleware di gestione degli errori viene aggiunta alla fine dello stack della funzione middleware.

Se un errore viene ignorato e passato a `next()` e non viene gestito in un gestore
degli errori, verrà gestito dal gestore errori integrato; l’errore verrà scritto sul client con la traccia
stack. La traccia stack non viene inclusa nell’ambiente di produzione.

Impostare la variabile di ambiente `NODE_ENV` su `production`, per eseguire l’applicazione nella modalità di produzione.

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

Se si chiama `next()` con un errore dopo che si è iniziato a scrivere la risposta
(ad esempio, se si riscontra un errore mentre si esegue lo streaming della
risposta al client) il gestore degli errori predefinito di Express chiude la connessione
e rifiuta la richiesta.

Pertanto, quando si aggiunge un gestore degli errori personalizzato, si consiglia di associarlo al meccanismo
di gestione degli errori predefinito in Express, quando le intestazioni
sono state già inviate al client:

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/it/resources/middleware.html).

## Writing error handlers

Define error-handling middleware functions in the same way as other middleware functions,
except error-handling functions have four arguments instead of three:
`(err, req, res, next)`. Ad esempio:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Si definisce il middleware di gestione degli errori per ultimo, successivamente `app.use()` e altre chiamate route; ad esempio:

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

Le risposte dall’interno delle funzione middleware possono essere in qualsiasi formato desiderato, ad esempio una pagina di errore HTML, un messaggio semplice o una stringa JSON.

Per motivi organizzativi (e framework di livello più alto), è possibile definire
diverse funzioni middleware di gestione degli errori, come solitamente si fa con
le funzioni middleware normali. Ad esempio, se si desidera definire un programma di gestione errori per le richieste
effettuate utilizzando `XHR` e quelle senza, è necessario utilizzare i seguenti comandi:

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

In questo esempio, il `logErrors` generico potrebbe scrivere le richieste e le informazioni sull’errore
su `stderr`, ad esempio:

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

Inoltre, in questo esempio, `clientErrorHandler` viene definito come segue; in questo caso, l’errore viene chiaramente tramandato al successivo:

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

La funzione “catch-all” `errorHandler` potrebbe essere implementata come segue:

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

If you have a route handler with multiple callback functions, you can use the `route` parameter to skip to the next route handler. Ad esempio:

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

In questo esempio, il gestore `getPaidContent` verrà ignorato ma qualsiasi altro gestore rimanente in `app` per `/a_route_behind_paywall` verrà eseguito senza interruzione.

Le chiamate a `next()` e `next(err)` indicano che il gestore corrente è completo e in che stato si trova.  `next(err)` ignorerà tutti gli handler rimanenti nella catena ad eccezione degli handler configurati per gestire gli errori come descritto sopra.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/error-handling.md          )

---

# Passaggio a Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Passaggio a Express 4

## Panoramica

Express 4 è stato modificato rispetto a Express 3. Ciò significa che un’applicazione Express 3 esistente non funzionerà se si aggiornano le dipendenze della versione Express.

Argomenti di questo articolo:

- [Modifiche in Express 4.](#changes)
- [Un esempio](#example-migration) di migrazione di un'applicazione Express 3 a Express 4.
- [Aggiornamento al programma di creazione dell'applicazione Express 4.](#app-gen)

## Modifiche in Express 4

Sono state apportate diverse modifiche importanti alla versione Express 4:

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [Modifiche al sistema di routing.](#routing)
- [Altre modifiche.](#other-changes)

Consultare inoltre:

- [Nuove funzioni in 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migrazione da 3.x a 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Modifiche al sistema middleware e al core di Express

Express 4 non dipende più da Connect e non ha più il middleware integrato nel core,
ad eccezione della funzione `express.static`. Ciò significa che ora
Express è un framework web middleware e routing indipendente
i release e le versioni di Express non vengono influenzate dagli aggiornamenti middleware.

Senza un middleware integrato, è necessario aggiungere esplicitamente tutto il
middleware richiesto per eseguire l’applicazione. Seguire semplicemente questi passaggi:

1. Installare il modulo: `npm install --save <module-name>`
2. Nell’applicazione, richiedere il modulo: `require('module-name')`
3. Utilizzare il modulo relativamente alla propria documentazione: `app.use( ... )`

La seguente tabella elenca il middleware Express 3 e le relative controparti in Express 4.

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

Segue l’[elenco completo](https://github.com/senchalabs/connect#middleware) di middleware Express 4.

In molti casi, è possibile semplicemente sostituire il middleware della versione 3 meno recente con la relativa controparte
Express 4. Per dettagli, consultare la documentazione del modulo in
GitHub.

#### app.useaccetta i parametri

Nella versione 4 è possibile utilizzare un parametro di variabile per definire il percorso in cui vengono caricate le funzioni middleware, quindi leggere il valore del parametro dal programma di gestione route.
Ad esempio:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### Il sistema di routing

Le applicazioni ora sono in grado di caricare il middleware di routing, pertanto non sarà più necessario
pensare all’ordine in cui è caricato il middleware rispetto al middleware
`router`.

Il modo in cui viene definita la route non è cambiato ma il sistema di routing dispone di due nuove
funzioni utili per organizzare le route:

- Un nuovo metodo, `app.route()`, per creare handler di route a catena per un percorso route.
- Un nuova classe, `express.Router`, per creare handler di route assemblabili in modo modulare.

#### Metodoapp.route()

Il nuovo metodo `app.route()` consente di creare handler di route a catena
per un percorso route. Poiché il percorso è specificato in una singola ubicazione, la creazione di route modulari è utile, poiché riduce le possibilità di riscontrare errori tipografici e di ridondanza. Per ulteriori informazioni
sulle route, consultare la documentazione [Router()](https://expressjs.com/it/4x/api.html#router).

Segue un esempio di handler di route a catena definiti utilizzando la funzione `app.route()`.

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

#### Classeexpress.Router

L’altra funzione che risulta utile per organizzare le route in una nuova classe,
`express.Router`, che è possibile utilizzare per creare handler di route assemblabili in modo modulare. Un’istanza `Router` è un sistema di routing e middleware completo;
per questo motivo spesso viene fatto riferimento a questo come “mini-app”.

Nel seguente esempio si crea un router come modulo, si carica il middleware all’interno di esso,
si definiscono alcune route e si caricano su un percorso nell’applicazione principale.

Ad esempio, creare un file router denominato `birds.js` nella directory dell’applicazione,
con i seguenti contenuti:

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

Successivamente, caricare il modulo router nell’applicazione:

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

L’applicazione sarà ora in grado di gestire le richieste per i percorsi `/birds` e
`/birds/about` e chiamerà il middleware `timeLog`
specifico per la route.

### Altre modifiche

La seguente tabella elenca altre piccole ma importanti modifiche applicate a Express 4:

| Oggetto | Descrizione |
| --- | --- |
| Node.js | Express 4 richiede Node.js 0.10.x o versione successiva e non esiste più supporto per
Node.js 0.8.x. |
| http.createServer() | Il modulohttpnon è più necessario, a meno che non sia necessario utilizzarlo (socket.io/SPDY/HTTPS). L’applicazione può essere avviata utilizzando
la funzioneapp.listen(). |
| app.configure() | La funzioneapp.configure()è stata rimossa.  Utilizzare la funzioneprocess.env.NODE_ENVoapp.get('env')per rilevare l’ambiente e configurare l’applicazione in modo appropriato. |
| json spaces | La proprietà dell’applicazionejson spacesè disattivata per impostazione predefinita in Express 4. |
| req.accepted() | Utilizzarereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets()ereq.acceptsLanguages(). |
| res.location() | Non risolve più le URL relative. |
| req.params | Era un array; ora è un oggetto. |
| res.locals | Era una funzione; ora è un oggetto. |
| res.headerSent | Modificato inres.headersSent. |
| app.route | Ora disponibile comeapp.mountpath. |
| res.on('header') | Rimosso. |
| res.charset | Rimosso. |
| res.setHeader('Set-Cookie', val) | La funzionalità ora è limitata alla sola impostazione del valore cookie di base. Utilizzareres.cookie()per aggiungere altre funzionalità. |

## Esempio di migrazione dell'applicazione

Segue un esempio di migrazione dell’applicazione da Express 3 a Express 4.
I file da considerare sono `app.js` e `package.json`.

### Applicazione con la versione 3

#### app.js

Prendere in considerazione l’applicazione Express v.3 con il seguente file `app.js`:

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

Il file `package.json` della versione 3 associata deve
apparire come segue:

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

### Processo

Iniziare il processo di migrazione installando il middleware richiesto per l’applicazione
Express 4 e aggiornando Express e Pug alla versione aggiornata
con il seguente comando:

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

Apportare le seguenti modifiche a `app.js`:

1. Le funzioni middleware di Express integrate `express.favicon`,
  `express.logger`, `express.methodOverride`,
  `express.session`, `express.bodyParser` e
  `express.errorHandler` non sono più disponibili nell’oggetto
  `express`. È necessario installare le funzioni alternative
  manualmente e caricarle sull’applicazione.
2. Non è più necessario caricare la funzione `app.router`.
  Non è un oggetto applicazione Express 4 valido, pertanto rimuovere il codice
  `app.use(app.router);`.
3. Assicurarsi che le funzioni middleware siano state caricate nell’ordine corretto - caricare `errorHandler` dopo aver caricato le route dell’applicazione.

### Applicazione con la versione 4

#### package.json

L’esecuzione del comando `npm` aggiornerà `package.json` come segue:

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

Successivamente, rimuovere il codice non valido, caricare il middleware richiesto e apportare le modifiche
necessarie. Il file `app.js` apparirà come segue:

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

A meno che non sia necessario gestire direttamente il modulo `http` (socket.io/SPDY/HTTPS), il relativo caricamento non è richiesto e l’applicazione può essere avviata semplicemente come segue:

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Eseguire l'applicazione

Il processo di migrazione è stato completato e ora l’applicazione
è stata aggiornata a Express 4. Per confermare, avviare l’applicazione utilizzando il seguente comando:

```
$ node .
```

Caricare [http://localhost:3000](http://localhost:3000)
e visualizzare la home page sottoposta a rendering da Express 4.

## Aggiornamento al programma di creazione dell'applicazione Express 4

Lo strumento della riga comandi per generare un’applicazione Express è sempre
`express` ma per effettuare l’aggiornamento alla nuova versione è necessario disinstallare
il programma di creazione dell’applicazione di Express 3 e successivamente installare il nuovo
`express-generator`.

### Installazione

Se il programma di creazione dell’applicazione di Express 3 è già installato sul sistema,
è necessario disinstallarlo:

```
$ npm uninstall -g express
```

A seconda di come sono configurati i privilegi del file e della directory,
potrebbe essere necessario eseguire questo comando con `sudo`.

Ora, installare il nuovo programma di creazione:

```
$ npm install -g express-generator
```

A seconda di come sono configurati i privilegi del file e della directory,
potrebbe essere necessario eseguire questo comando con `sudo`.

Ora, il comando `express` sul sistema è aggiornato al programma di creazione
di Express 4.

### Modifiche al programma di creazione dell'applicazione

L’utilizzo e le opzioni del comando sono rimaste quasi gli stessi, con le seguenti eccezioni:

- È stata rimossa l’opzione `--sessions`.
- È stata rimossa l’opzione `--jshtml`.
- È stata aggiunta l’opzione `--hogan` per supportare [Hogan.js](http://twitter.github.io/hogan.js/).

### Esempio

Eseguire il seguente comando per creare un’applicazione Express 4:

```
$ express app4
```

Se si visualizzano i contenuti del file `app4/app.js`, si noterà che tutte le funzioni
middleware (ad eccezione di `express.static`) richieste per l’applicazione,
sono caricate come moduli indipendenti e il middleware `router`
non viene più caricato in modo esplicito sull’applicazione.

Si noterà inoltre che il file `app.js` è ora un modulo Node.js, diversamente dall’applicazione autonoma che era stata generate dal vecchio programma di creazione.

Dopo aver installato le dipendenze, avviare l’applicazione utilizzando il seguente comando:

```
$ npm start
```

Se si visualizza lo script di avvio npm nel file `package.json`,
si noterà che il comando effettivo che avvia l’applicazione è
`node ./bin/www`, il quale era `node app.js`
in Express 3.

Poiché il file `app.js` generato dal programma di creazione di Express 4
è ora un modulo Node.js, non può essere più avviato individualmente come un’applicazione
(a meno che non venga modificato il codice). Il modulo deve essere caricato in un file Node.js
e avviato tramite il file Node.js. Il file Node.js è `./bin/www`
in questo caso.

La directory `bin` e il file senza estensione `www`
non sono obbligatori per la creazione di un’applicazione Express o per avviare l’applicazione. Sono solo consigli
creati dal programma di creazione, pertanto è possibile modificarli a seconda delle
necessità.

Per rimuovere la directory `www` e conservare le cose “come farebbe Express 3”,
cancellare la riga in cui viene riportata la dicitura `module.exports = app;` alla fine del file
`app.js`, quindi incollare il seguente codice al proprio posto:

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

Assicurarsi di caricare il modulo `debug` all’inizio del file `app.js` utilizzando il seguente codice:

```
var debug = require('debug')('app4')
```

Successivamente, modificare `"start": "node ./bin/www"` nel file `package.json` in `"start": "node app.js"`.

È stata spostata la funzionalità di `./bin/www` di nuovo in
`app.js`. Questa modifica non è consigliata, ma questa prova consente di comprendere in che modo funziona
il file `./bin/www` e perché il file `app.js`
non si avvia più in modo autonomo.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/guide/migrating-4.md          )
