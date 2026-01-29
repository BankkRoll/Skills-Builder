# Express detrás de proxies and more

# Express detrás de proxies

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# Express detrás de proxies

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

The application setting `trust proxy` may be set to one of the values listed in the following table.

| Type | Value |
| --- | --- |
| Booleano | Si estrue, la dirección IP del cliente se entiende como la entrada más a la izquierda en la cabeceraX-Forwarded-*.Si esfalse, la aplicación se entiende como orientada directamente a Internet, y la dirección IP del cliente se obtiene dereq.connection.remoteAddress. Este es el valor predeterminado.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7Puede establecer direcciones IP de varias formas:app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayCuando se especifican, las direcciones IP o las subredes se excluyen del proceso de determinación de direcciones, y la dirección IP no de confianza más próxima al servidor de aplicaciones se establece como la dirección IP del cliente. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| Number | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- El valor de [req.hostname](https://expressjs.com/es/api.html#req.hostname) se obtiene del valor definido en la cabecera `X-Forwarded-Host`, que puede estar establecido por el cliente o el proxy.
- El proxy inverso puede establecer `X-Forwarded-Proto` para indicar a la aplicación si es `https`, `http` o incluso un nombre no válido. [req.protocol](https://expressjs.com/es/api.html#req.protocol) refleja este valor.
- Los valores [req.ip](https://expressjs.com/es/api.html#req.ip) y [req.ips](https://expressjs.com/es/api.html#req.ips) se rellenan con la lista de direcciones de `X-Forwarded-For`.

El valor `trust proxy` se implementa utilizando el paquete [proxy-addr](https://www.npmjs.com/package/proxy-addr). For more information, see its documentation.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/behind-proxies.md          )

---

# Integración de la base de datos

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# Integración de la base de datos

La adición de la funcionalidad de conectar bases de datos a las aplicaciones Express se consigue simplemente cargando el controlador de Node.js adecuado para la base de datos en la aplicación. En este documento se describe brevemente cómo añadir y utilizar algunos de los módulos de Node.js más conocidos para los sistemas de base de datos en la aplicación Express:

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

Estos son algunos de los muchos controladores de base de datos que hay disponibles. Para ver otras opciones, realice búsquedas en el sitio [npm](https://www.npmjs.com/).

## Cassandra

**Módulo**: [cassandra-driver](https://github.com/datastax/nodejs-driver) **Instalación**

```
$ npm install cassandra-driver
```

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

**Módulo**: [nano](https://github.com/dscape/nano) **Instalación**

```
$ npm install nano
```

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

**Módulo**: [levelup](https://github.com/rvagg/node-levelup) **Instalación**

```
$ npm install level levelup leveldown
```

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

**Módulo**: [mysql](https://github.com/felixge/node-mysql/) **Instalación**

```
$ npm install mysql
```

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

**Módulo**: [mongodb](https://github.com/mongodb/node-mongodb-native) **Instalación**

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

Si desea un controlador de modelo de objeto para MongoDB, consulte [Mongoose](https://github.com/LearnBoost/mongoose).

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

NOTA: [Vea los requisitos previos de instalación](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

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

**Módulo**: [pg-promise](https://github.com/vitaly-t/pg-promise) **Instalación**

```
$ npm install pg-promise
```

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

**Módulo**: [redis](https://github.com/mranney/node_redis) **Instalación**

```
$ npm install redis
```

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

**Módulo**: [sqlite3](https://github.com/mapbox/node-sqlite3) **Instalación**

```
$ npm install sqlite3
```

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

**Módulo**: [elasticsearch](https://github.com/elastic/elasticsearch-js) **Instalación**

```
$ npm install elasticsearch
```

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/database-integration.md          )

---

# Depuración de Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Depuración de Express

Para ver todos los registros internos utilizados en Express, establezca la variable de entorno `DEBUG` en `express:*` cuando inicie la aplicación.

```
$ DEBUG=express:* node index.js
```

En Windows, utilice el mandato correspondiente.

```
> $env:DEBUG = "express:*"; node index.js
```

La ejecución de este mandato en la aplicación predeterminada generada por el [generador de Express](https://expressjs.com/es/starter/generator.html) imprime la siguiente salida:

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

Cuando se realiza una solicitud a la aplicación, verá los registros especificados en el código de Express:

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

Para ver sólo los registros de la implementación de direccionador, establezca el valor de `DEBUG` en `express:router`. De la misma forma, para ver sólo los registros de la implementación de aplicación, establezca el valor de `DEBUG` en `express:application`, etc.

## Applications generated byexpress

Una aplicación generada por el mandato `express` utiliza el módulo `debug`, y el ámbito de su espacio de nombres de depuración se establece en el nombre de la aplicación.

Por ejemplo, si ha generado la aplicación con `$ express sample-app`, puede habilitar las sentencias de depuración con el siguiente mandato:

```
$ DEBUG=sample-app:* node ./bin/www
```

Puede especificar más de un espacio de nombres de depuración asignando una lista separada por comas de nombres:

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

Nota

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[util.inspect()](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/debugging.md          )

---

# Error Handling

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# Error Handling

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

Defina las funciones de middleware de manejo de errores de la misma forma que otras funciones de middleware, excepto que las funciones de manejo de errores tienen cuatro argumentos en lugar de tres: `(err, req, res, next)`.  For example:

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

Si tiene un manejador de rutas con varias funciones de devolución de llamada, puede utilizar el parámetro `route` para omitir el siguiente manejador de rutas.
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

Si pasa cualquier valor a la función `next()` (excepto la serie `'route'`), Express considera que la solicitud actual tiene un error y omitirá las restantes funciones de middleware y direccionamiento que no son de manejo de errores.

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

## El manejador de errores predeterminado

Express se suministra con un manejador de errores incorporado, que se encarga de los errores que aparecen en la aplicación. Esta función de middleware de manejo de errores predeterminada se añade al final de la pila de funciones de middleware.

Si pasa un error a `next()` y no lo maneja en el manejador de errores, lo manejará el manejador de errores incorporado; el error se escribirá en el cliente con el seguimiento de la pila. El seguimiento de la pila no se incluye en el entorno de producción.

Establezca la variable de entorno `NODE_ENV` en `production`, para ejecutar la aplicación en modalidad de producción.

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

Si invoca `next()` con un error después de haber empezado a escribir la respuesta (por ejemplo, si encuentra un error mientras se envía la respuesta en modalidad continua al cliente), el manejador de errores predeterminado de Express cierra la conexión y falla la solicitud.

Por lo tanto, cuando añade un manejador de errores personalizado, se recomienda delegar en los mecanismos de manejo de errores predeterminados de Express, cuando las cabeceras ya se han enviado al cliente:

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/es/resources/middleware.html).

## Writing error handlers

Define error-handling middleware functions in the same way as other middleware functions,
except error-handling functions have four arguments instead of three:
`(err, req, res, next)`. For example:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

El middleware de manejo de errores se define al final, después de otras llamadas de rutas y `app.use()`; por ejemplo:

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

Las respuestas desde una función de middleware pueden estar en el formato que prefiera, por ejemplo, una página de errores HTML, un mensaje simple o una serie JSON.

A efectos de la organización (y de infraestructura de nivel superior), puede definir varias funciones de middleware de manejo de errores, de la misma forma que con las funciones de middleware normales. Por ejemplo, si desea definir un manejador de errores para las solicitudes realizadas utilizando `XHR`, y las que no lo tienen, puede utilizar los siguientes mandatos:

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

En este ejemplo, los `logErrors` genéricos pueden escribir información de solicitudes y errores en `stderr`, por ejemplo:

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

También en este ejemplo, `clientErrorHandler` se define de la siguiente manera; en este caso, el error se pasa de forma explícita al siguiente:

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

La función que detecta todos los errores de `errorHandler` puede implementarse de la siguiente manera:

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

En este ejemplo, se omitirá el manejador `getPaidContent`, pero los restantes manejadores en `app` para `/a_route_behind_paywall` continuarán ejecutándose.

Las llamadas a `next()` y `next(err)` indican que el manejador actual está completo y en qué estado.  `next(err)` omitirá los demás manejadores de la cadena, excepto los que se hayan configurado para manejar errores como se ha descrito anteriormente.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/error-handling.md          )

---

# Migración a Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Migración a Express 4

## Overview

Express 4 es un cambio que rompe el código existente de Express 3, etc. Esto implica que una aplicación Express 3 existente no funcionará si actualiza la versión de Express en sus dependencias.

En este artículo se describen:

- [Los cambios en Express 4.](#changes)
- [Un ejemplo](#example-migration) de migración de una aplicación Express 3 a Express 4.
- [La actualización al generador de aplicaciones Express 4.</li>
  </ul>Los cambios en Express 4Se han realizado varios cambios importantes en Express 4:Changes to Express core and middleware system.The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.Cambios en el sistema de direccionamiento.Otros cambios.Vea también:
  - [New features in 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
  - [Migrating from 3.x to 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)Cambios en el sistema principal y de middleware de ExpressExpress 4 ya no depende de Connect y elimina todo el middleware incorporado de su núcleo, excepto la función `express.static`. Esto significa que ahora Express es una infraestructura web de middleware y direccionamiento independiente, y que los releases y las versiones de Express no se ven afectados por las actualizaciones de middleware.
  Sin el middleware incorporado, debe añadir explícitamente todo el
  middleware necesario para ejecutar la aplicación. Sólo tiene que seguir estos pasos:
  1. Instalar el módulo: `npm install --save`
  2. En su aplicación, requerir el módulo: `require('module-name')`
  3. Utilizar el módulo según su documentación: `app.use( ... )`
  En la tabla siguiente se lista el middleware de Express 3 y su contrapartida en Express 4.Express 3Express 4express.bodyParserbody-parser+multerexpress.compresscompressionexpress.cookieSessioncookie-sessionexpress.cookieParsercookie-parserexpress.loggermorganexpress.sessionexpress-sessionexpress.faviconserve-faviconexpress.responseTimeresponse-timeexpress.errorHandlererrorhandlerexpress.methodOverridemethod-overrideexpress.timeoutconnect-timeoutexpress.vhostvhostexpress.csrfcsurfexpress.directoryserve-indexexpress.staticserve-staticEsta es la [lista completa](https://github.com/senchalabs/connect#middleware) de middleware de Express 4.
  En la mayoría de los casos, sólo tiene que sustituir el middleware de la versión 3 antigua por su contrapartida de Express 4. Para obtener detalles, consulte la documentación del módulo en GitHub.app.useaccepts parametersEn la versión 4, puede utilizar un parámetro de variable para definir la vía de acceso donde se cargan las funciones de middleware y, a continuación, leer el valor del parámetro en el manejador de rutas.
  For example:
  ```js
  app.use('/book/:id', (req, res, next) => {
    console.log('ID:', req.params.id)
    next()
  })
  ```El sistema de direccionamientoAhora las aplicaciones cargan implícitamente el middleware de direccionamiento, por lo que ya no tiene que preocuparse del orden con el que se carga el middleware respecto al middleware de `router`.
  La forma en que define las rutas no varía, pero el sistema de direccionamiento tiene dos nuevas características que permiten organizar las rutas:
  {: .doclist }
  - Un nuevo método, `app.route()`, para crear manejadores de rutas encadenables para una vía de acceso de ruta.
  - Una nueva clase, `express.Router`, para crear manejadores de rutas montables modulares.app.route()methodEl nuevo método `app.route()` permite crear manejadores de rutas encadenables para una vía de acceso de ruta. Como la vía de acceso se especifica en una única ubicación, la creación de rutas modulares es muy útil, al igual que la reducción de redundancia y errores tipográficos. Para obtener más información sobre las rutas, consulte la [`documentación` de Router()](/es/4x/api.html#router).
  A continuación, se muestra un ejemplo de manejadores de rutas encadenados que se definen utilizando la función `app.route()`.
  ```js
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
  ```express.RouterclassLa otra característica que permite organizar las rutas es una nueva clase, `express.Router`, que puede utilizar para crear manejadores de rutas montables modulares. Una instancia `Router` es un sistema de middleware y direccionamiento completo; por este motivo, a menudo se conoce como una "miniaplicación".
  El siguiente ejemplo crea un direccionador como un módulo, carga el middleware en él, define algunas rutas y lo monta en una vía de acceso en la aplicación principal.
  Por ejemplo, cree un archivo de direccionador denominado `birds.js` en el directorio de la aplicación, con el siguiente contenido:
  ```js
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
  A continuación, cargue el módulo de direccionador en la aplicación:
  ```js
  var birds = require('./birds')
  // ...
  app.use('/birds', birds)
  ```
  La aplicación ahora podrá manejar solicitudes a las vías de acceso `/birds` y `/birds/about`, e invocará el middleware `timeLog` que es específico de la ruta.Other changesEn la tabla siguiente se muestran otros cambios pequeños pero importantes en Express 4:ObjectDescriptionNode.jsExpress 4 requiere Node.js 0.10.x o posterior y deja de dar soporte a
  Node.js 0.8.x.http.createServer()Thehttpmodule is no longer needed, unless you need to directly work with it (socket.io/SPDY/HTTPS). La aplicación puede iniciarse utilizando la funciónapp.listen().app.configure()La funciónapp.configure()se ha eliminado.  Utilice la funciónprocess.env.NODE_ENVoapp.get('env')para detectar el entorno y configure la aplicación según corresponda.json spacesLa propiedad de aplicaciónjson spacesestá inhabilitada de forma predeterminada en Express 4.req.accepted()Utilicereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets()yreq.acceptsLanguages().res.location()Ya no resuelve los URL relativos.req.paramsEra una matriz, ahora es un objeto.res.localsEra una función, ahora es un objeto.res.headerSentSe ha cambiado porres.headersSent.app.routeAhora está disponible comoapp.mountpath.res.on('header')Se ha eliminado.res.charsetSe ha eliminado.res.setHeader('Set-Cookie', val)La funcionalidad está ahora limitada a establecer el valor de cookie básico. Utiliceres.cookie()para obtener la funcionalidad adicional.Migración de aplicación de ejemploA continuación, se muestra un ejemplo de migración de una aplicación Express 3 a Express 4.
  The files of interest are `app.js` and `package.json`.Aplicación versión 3app.jsConsider an Express v.3 application with the following `app.js` file:
  ```js
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
  ```package.jsonEl archivo `package.json` de la versión 3 correspondiente será similar al siguiente:
  ```json
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
  ```ProcesoPara empezar el proceso de migración, instale el middleware necesario para la aplicación Express 4 y actualice Express y Pug a su versión respectiva más reciente con el siguiente mandato:
  ```bash
  $ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
  ```
  Realice los cambios siguientes en `app.js`:
  1. Las funciones de middleware de Express incorporadas `express.favicon`,
     `express.logger`, `express.methodOverride`,
     `express.session`, `express.bodyParser` y
     `express.errorHandler` ya no están disponibles en el objeto `express`. Debe instalar sus alternativas manualmente y cargarlas en la aplicación.
  2. Ya no es necesario cargar la función `app.router`.
     No es un objeto de aplicación Express 4 válido, por lo que debe eliminar el código `app.use(app.router);`.
  3. Asegúrese de que las funciones de middleware se cargan en el orden correcto: cargue `errorHandler` después de cargar las rutas de aplicación.Aplicación versión 4package.jsonLa ejecución del mandato `npm` anterior actualizará `package.json` de la siguiente manera:
  ```json
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
  ```app.jsA continuación, elimine el código no válido, cargue el middleware necesario y realice otros cambios según sea necesario. El archivo `app.js` será parecido al siguiente:
  ```js
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
  ```A menos que necesite trabajar directamente con el módulohttp(socket.io/SPDY/HTTPS), no es necesario cargarlo y la aplicación puede iniciarse simplemente de la siguiente manera:app.listen(app.get('port'),()=>{console.log('Express server listening on port'+app.get('port'))})Run the appEl proceso de migración está completo y la aplicación es ahora una aplicación
  Express 4. Para confirmarlo, inicie la aplicación utilizando el siguiente mandato:
  ```bash
  $ node .
  ```
  Cargue [http://localhost:3000](http://localhost:3000) y vea la página de inicio que representa Express 4.La actualización al generador de aplicaciones Express 4La herramienta de línea de mandatos para generar una aplicación Express continúa siendo `express`, pero para actualizar a la nueva versión, debe desinstalar el generador de aplicaciones Express 3 e instalar el nuevo `express-generator`.InstalaciónSi ya ha instalado el generador de aplicaciones Express 3 en el sistema, debe desinstalarlo:
  ```bash
  $ npm uninstall -g express
  ```
  Dependiendo de cómo se configuren los privilegios de archivos y directorios, deberá ejecutar este mandato con `sudo`.
  A continuación, instale el nuevo generador:
  ```bash
  $ npm install -g express-generator
  ```
  Dependiendo de cómo se configuren los privilegios de archivos y directorios, deberá ejecutar este mandato con `sudo`.
  Ahora el mandato `express` en el sistema se actualiza al generador de Express 4.Cambios en el generador de aplicacionesLas opciones de mandato y el uso continúan prácticamente iguales, con las siguientes excepciones:
  {: .doclist }
  - Removed the `--sessions` option.
  - Removed the `--jshtml` option.
  - Se ha añadido la opción `--hogan` para dar soporte a [Hogan.js](http://twitter.github.io/hogan.js/).Ejecute el siguiente mandato para crear una aplicación Express 4:
  ```bash
  $ express app4
  ```
  Si consulta el contenido del archivo `app4/app.js`, observará que todas las funciones de middleware (excepto `express.static`) que son necesarias para la aplicación se cargan como módulos independientes y que el middleware de `router` ya no se carga de forma explícita en la aplicación.
  También observará que el archivo `app.js` es ahora un módulo Node.js, a diferencia de la aplicación autónoma que generaba el antiguo generador.
  Después de instalar las dependencias, inicie la aplicación utilizando el siguiente mandato:
  ```bash
  $ npm start
  ```
  Si consulta el script de inicio npm en el archivo `package.json`, observará que el mandato que inicia la aplicación es `node ./bin/www`, que antes era `node app.js` en Express 3.
  Como el archivo `app.js` que generaba el generador de Express 4 ahora es un módulo Node.js, ya no puede iniciarse independientemente como una aplicación (a menos que modifique el código). El módulo debe cargarse en un archivo Node.js e iniciarse utilizando el archivo Node.js. El archivo Node.js es `./bin/www` en este caso.
  Ni el directorio `bin` ni el archivo `www`
  sin extensión son obligatorios para crear una aplicación Express o iniciar la aplicación. Son sólo sugerencias realizadas por el generador, por lo que puede modificarlos según sus necesidades.
  Para eliminar el directorio `www` y dejarlo todo como en "Express 3",
  suprima la línea `module.exports = app;` al final del archivo `app.js` y pegue el siguiente código en su lugar:
  ```js
  app.set('port', process.env.PORT || 3000)
  var server = app.listen(app.get('port'), () => {
    debug('Express server listening on port ' + server.address().port)
  })
  ```
  Asegúrese de cargar el módulo `debug` encima del archivo `app.js` utilizando el código siguiente:
  ```js
  var debug = require('debug')('app4')
  ```
  A continuación, cambie `"start": "node ./bin/www"` en el archivo `package.json` por `"start": "node app.js"`.
  Ahora ha devuelto la funcionalidad de `./bin/www` a `app.js`. Este cambio no se recomienda, pero el ejercicio permite entender cómo funciona el archivo `./bin/www` y por qué el archivo `app.js` ya no se inicia solo.](#app-gen)

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/migrating-4.md          )
