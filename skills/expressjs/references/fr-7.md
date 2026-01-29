# Serveurs proxy derrière Express and more

# Serveurs proxy derrière Express

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# Serveurs proxy derrière Express

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

The application setting `trust proxy` may be set to one of the values listed in the following table.

| Type | Valeur |
| --- | --- |
| Booléen | Si la valeur esttrue, l’adresse IP du client est interprétée comme étant l’entrée la plus à gauche dans l’en-têteX-Forwarded-*.Si la valeur estfalse, l’application est interprétée comme étant directement accessible sur Internet et l’adresse IP du client est dérivée dereq.connection.remoteAddress. Il s’agit du paramètre par défaut.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7Vous pouvez définir les adresses IP de l’une des manières suivantes :app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayS’ils sont spécifiés, les sous-réseaux ou les adresses IP sont exclus du processus d’identification d’adresse, et l’adresse IP sans confiance la plus proche du serveur d’applications est identifiée comme étant l’adresse IP du client. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| Numérique | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- La valeur de [req.hostname](https://expressjs.com/fr/api.html#req.hostname) est dérivée de l’ensemble de valeurs indiqué dans l’en-tête `X-Forwarded-Host`, qui peut être défini par le client ou par le proxy.
- `X-Forwarded-Proto` peut être défini par le proxy inverse pour indiquer à l’application s’il s’agit de `https` ou de `http`, voire d’un nom non valide. Cette valeur est reflétée par [req.protocol](https://expressjs.com/fr/api.html#req.protocol).
- Les valeurs [req.ip](https://expressjs.com/fr/api.html#req.ip) et [req.ips](https://expressjs.com/fr/api.html#req.ips) sont renseignées avec la liste des adresses provenant de `X-Forwarded-For`.

Le paramètre `trust proxy` est implémenté à l’aide du package [proxy-addr](https://www.npmjs.com/package/proxy-addr). Pour plus d’informations, consultez la documentation associée.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/behind-proxies.md          )

---

# Intégration de bases de données

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# Intégration de bases de données

L’ajout de la fonctionnalité permettant de connecter des bases de données aux applications Express consiste simplement à charger un pilote Node.js approprié pour les bases de données de votre application. Ce document explique brièvement comment ajouter et utiliser dans votre application Express certains des modules Node.js les plus populaires pour les systèmes de base de données :

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

Ces pilotes de base de données ne sont qu’une partie de ceux disponibles. Pour d’autres options,
consultez le site [npm](https://www.npmjs.com/).

## Cassandra

**Module** : [cassandra-driver](https://github.com/datastax/nodejs-driver) **Installation**

### Installation

```
$ npm install cassandra-driver
```

### Exemple

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

### Exemple

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

**Module** : [nano](https://github.com/dscape/nano) **Installation**

### Installation

```
$ npm install nano
```

### Exemple

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

**Module** : [levelup](https://github.com/rvagg/node-levelup) **Installation**

### Installation

```
$ npm install level levelup leveldown
```

### Exemple

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

**Module** : [mysql](https://github.com/felixge/node-mysql/) **Installation**

### Installation

```
$ npm install mysql
```

### Exemple

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

**Module** : [mongodb](https://github.com/mongodb/node-mongodb-native) **Installation**

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

Si vous voulez un pilote de modèle d’objet pour MongoDB, recherchez [Mongoose](https://github.com/LearnBoost/mongoose).

## Neo4j

**Module** : [apoc](https://github.com/hacksparrow/apoc) **Installation**

### Installation

```
$ npm install neo4j-driver
```

### Exemple

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

Remarque: [Voir les conditions préalables à l’installation](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### Exemple

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

**Module** : [pg-promise](https://github.com/vitaly-t/pg-promise) **Installation**

### Installation

```
$ npm install pg-promise
```

### Exemple

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

**Module** : [redis](https://github.com/mranney/node_redis) **Installation**

### Installation

```
$ npm install redis
```

### Exemple

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

### Exemple

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

**Module** : [sqlite3](https://github.com/mapbox/node-sqlite3) **Installation**

### Installation

```
$ npm install sqlite3
```

### Exemple

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

**Module** : [elasticsearch](https://github.com/elastic/elasticsearch-js) **Installation**

### Installation

```
$ npm install elasticsearch
```

### Exemple

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/database-integration.md          )

---

# Débogage d’Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Débogage d’Express

Pour afficher tous les journaux internes utilisés dans Express, affectez à la variable d’environnement `DEBUG` la valeur `express:*` lors du lancement de votre application.

```
$ DEBUG=express:* node index.js
```

Sous Windows, utilisez la commande correspondante.

```
> $env:DEBUG = "express:*"; node index.js
```

L’exécution de cette commande sur l’application par défaut générée par le [générateur express](https://expressjs.com/fr/starter/generator.html) imprime le résultat suivant :

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

Si une demande est par la suite effectuée à l’application, vous verrez les journaux spécifiés dans le code Express :

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

Pour afficher les journaux uniquement à partir de l’implémentation du routeur, affectez à la variable d’environnement `DEBUG` la valeur `express:router`. De la même façon, pour afficher les journaux uniquement à partir de l’implémentation de l’application, affectez à la variable d’environnement `DEBUG` la valeur `express:application`, et ainsi de suite.

## Applications générées par la commandeexpress

Une application générée par la commande `express` également appel au module `debug` et son espace de nom de débogage est délimité par le nom de l’application.

Ainsi, si vous avez généré l’application à l’aide de `$ express sample-app`, vous pouvez activer les instructions de débogage en exécutant la commande suivante :

```
$ DEBUG=sample-app:* node ./bin/www
```

Vous pouvez spécifier plusieurs espaces de noms de débogage en affectant une liste de noms séparés par des virgules :

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

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/debugging.md          )

---

# Traitement d’erreurs

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# Traitement d’erreurs

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## Catching Errors

It’s important to ensure that Express catches all errors that occur while
running route handlers and middleware.

Errors that occur in synchronous code inside route handlers and middleware
require no extra work. If synchronous code throws an error, then Express will
catch and process it. Par exemple :

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

Définissez les fonctions middleware de traitement d’erreurs de la même manière que les autres fonctions middleware,
à l’exception près que les fonctions de traitement d’erreurs se composent de quatre arguments et non de trois :
`(err, req, res, next)`.  Par exemple :

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

Si vous disposez d’un gestionnaire de routage avec plusieurs fonctions callback, vour pouvez utiliser le paramètre `route` pour passer au gestionnaire de routage suivant.
Par exemple :

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

If `getUserById` throws an error or rejects, `next` will be called with either
the thrown error or the rejected value. If no rejected value is provided, `next`
will be called with a default Error object provided by the Express router.

Si vous transmettez tout à la fonction `next()` (sauf la chaîne `'route'`), Express considère la demande en cours
comme étant erronée et ignorera tout routage de gestion non lié à une erreur et toute fonction middleware restants.

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
middleware and pass them to Express for processing. Par exemple :

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
that return promises.  Par exemple :

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
catching, by reducing the asynchronous code to something trivial. Par exemple :

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

## Le gestionnaire de traitement d’erreurs par défaut

Express propose un gestionnaire d’erreurs intégré, qui traite toutes les erreurs qui pourraient survenir dans l’application. Cette fonction middleware de traitement d’erreurs par défaut est ajoutée à la fin de la pile de fonctions middleware.

Si vous transmettez l’erreur à `next()` et que vous ne voulez pas la gérer dans
un gestionnaire d’erreurs, elle sera gérée par le gestionnaire d’erreurs intégré ; l’erreur sera alors écrite dans le client avec la
trace de pile. La trace de pile n’est pas incluse dans l’environnement de production.

Définissez la variable d’environnement `NODE_ENV` sur `production` afin d’exécuter l’application en mode production.

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

Si vous appelez `next()` avec une erreur après avoir démarré l’écriture de la
réponse (par exemple, si vous rencontrez une erreur lors de la diffusion en flux de la
réponse au client) le gestionnaire de traitement d’erreurs par défaut Express ferme la
connexion et met la demande en échec.

De ce fait, lorsque vous ajoutez un gestionnaire d’erreurs personnalisé, vous devriez déléguer
les mécanismes de gestion d’erreur par défaut à Express, lorsque les en-têtes
ont déjà été envoyés au client :

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/fr/resources/middleware.html).

## Writing error handlers

Define error-handling middleware functions in the same way as other middleware functions,
except error-handling functions have four arguments instead of three:
`(err, req, res, next)`. Par exemple :

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Définissez le middleware de traitement d’erreurs en dernier, après les autres appels `app.use()` et de routes ; par exemple :

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

Les réponses issues d’une fonction middleware peuvent être au format de votre choix, par exemple une page d’erreur HTML, un simple message ou une chaîne JSON.

A des fins organisationnelles (et d’infrastructure de niveau supérieur), vous pouvez définir plusieurs fonctions middleware de traitement d’erreurs, tout comme vous le feriez avec d’autres fonctions middleware ordinaires. Par exemple, si vous vouliez définir un gestionnaire d’erreurs pour les demandes réalisées avec `XHR` et pour celles réalisées sans, vous pourriez utiliser les commandes suivantes :

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

Dans cet exemple, les erreurs `logErrors` génériques pourraient écrire des informations de demande et d’erreur dans `stderr`, par exemple :

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

Egalement dans cet exemple, `clientErrorHandler` est défini comme suit ; dans ce cas, l’erreur est explicitement transmise à la fonction suivante :

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

La fonction “catch-all” `errorHandler` peut être mise en oeuvre comme suit :

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

If you have a route handler with multiple callback functions, you can use the `route` parameter to skip to the next route handler. Par exemple :

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

Dans cet exemple, le gestionnaire `getPaidContent` sera ignoré, mais tous les gestionnaires restants dans `app` pour `/a_route_behind_paywall` continueront d’être exécutés.

Les appels `next()` et `next(err)` indiquent que le gestionnaire en cours a fini et quel est son état.  `next(err)` ignorera tous les gestionnaires restants dans la chaîne, sauf ceux définis pour gérer les erreurs tel que décrit ci-dessus.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/error-handling.md          )

---

# Migration vers Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Migration vers Express 4

## Présentation

Express 4 est un changement novateur d’Express 3. Cela signifie qu’une application Express 3 existante ne fonctionnera pas si vous mettez à jour la version Express dans les dépendances.

Cet article couvre :

- [Modifications dans Express 4.](#changes)
- [Un exemple](#example-migration) de migration d'une application Express 3 vers Express 4.
- [Mise à niveau vers le générateur d'applications Express 4.](#app-gen)

## Modifications dans Express 4

De nombreuses modifications importantes ont été faites dans Express 4 :

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [Modifications du système de routage.](#routing)
- [Autres modifications diverses.](#other-changes)

Voir aussi :

- [Nouvelles fonctions dans la version 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migration de la version 3.x vers 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Modification du système principal et middleware d'Express

Express 4 ne dépend plus de Connect, et supprime tous les middleware intégrés de son noyau, sauf la fonction `express.static`. Cela signifie qu’Express
est désormais un canevas Web de routage et de middleware indépendant et que les versions et
éditions d’Express ne sont pas affectées par les mises à jour de middleware.

Sans middleware intégré, vous devez explicitement ajouter tous les
middleware requis pour exécuter votre application. Procédez comme suit :

1. Installez le module : `npm install --save <module-name>`
2. Dans votre application, demandez le module : `require('module-name')`
3. Utilisez le module en fonction de cette documentation: `app.use( ... )`

La table suivante répertorie le middelware Express 3 et ces équivalents dans Express 4.

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

Vous trouverez ici la [liste complète](https://github.com/senchalabs/connect#middleware) du middleware Express 4.

Dans la plupart des cas, il vous suffit de remplacer l’ancienne version du middelware 3 par
son équivalent Express 4. Pour plus d’informations, consultez la documentation relative au module dans
GitHub.

#### app.useaccepte les paramètres

Dans la version 4 vous pouvez utilisez un paramètre variable pour définir le chemin vers lequel les fonctions middleware sont chargées, puis lire la valeur de ce paramètre dans le gestionnaire de routage.
Par exemple :

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### Le système de routage

Les applications chargent dorénavant les middleware de routage de manière implicite, ce qui fait que vous n’avez plus à vous
soucier de l’ordre dans lequel les middleware sont chargés par rapport au middleware `router`.

La façon de définir des routes n’a pas changé mais le système de routage possède deux nouvelles fonctions
pour vous aider à organiser vos routes :

- Une nouvelle méthode, `app.route()`, permettant de créer des gestionnaires de routage sous forme de chaîne pour un chemin de routage.
- Une nouvelle classe, `express.Router`, permettant de créer des gestionnaires de routage modulaires pouvant être montés.

#### méthodeapp.route()

La nouvelle méthode `app.route()` vous permet de créer des gestionnaires de routage sous forme de chaîne pour un chemin de routage. Etant donné que le chemin est spécifié à une seul emplacement, la création de routes modulaires est utile car elle réduit la redondance et les erreurs. Pour plus d’informations sur les routes, voir la [documentationRouter()](https://expressjs.com/fr/4x/api.html#router).

Voici quelques exemples de gestionnaires de chemin de chaînage définis à l’aide de la fonction `app.route()`.

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

#### classeexpress.Router

L’autre fonction qui aide à organiser les routes est une nouvelle classe,
`express.Router`, que vous pouvez utiliser pour créer des gestionnaires de routage modulaires pouvant être
montés. Une instance `Router` est un middleware et un système de routage complet ; pour cette raison, elle est souvent appelée “mini-app”.

L’exemple suivant créé une routeur en tant que module, charge un middleware dans celui-ci, définit des routes et monte le module sur un chemin dans l’application principale.

Par exemple, créez un fichier de routage nommé `birds.js` dans le répertoire app, avec le contenu suivant :

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

Puis, chargez le module de routage dans l’application :

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

L’application pourra gérer des demandes dans les chemins `/birds` et
`/birds/about`, et appellera le middleware `timeLog` spécifique à la route.

### Autres modifications

Le tableau suivant répertorie les autres modifications mineures mais importantes dans Express 4 :

| Objet | Description |
| --- | --- |
| Node.js | Express 4 nécessite Node.js 0.10.x ou ultérieur et a abandonné la prise en charge de
Node.js 0.8.x. |
| http.createServer() | Le modulehttpn’est plus nécessaire, à moins que vous ne l’utilisiez directement (socket.io/SPDY/HTTPS). L’application peut être démarrée à l’aide de la fonctionapp.listen(). |
| app.configure() | La fonctionapp.configure()a été supprimée.  Utilisez
la fonctionprocess.env.NODE_ENVouapp.get('env')pour détecter l’environnement et configurer l’application, le cas échéant. |
| json spaces | La propriété d’applicationjson spacesest désactivée par défaut dans Express 4. |
| req.accepted() | Usereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets()etreq.acceptsLanguages(). |
| res.location() | Ne résout plus les adresses URL relatives. |
| req.params | Was an array; now an object. |
| res.locals | Anciennement une fonction ; il s’agit dorénavant d’un objet. |
| res.headerSent | A été modifié enres.headersSent. |
| app.route | Dorénavant disponible commeapp.mountpath. |
| res.on('header') | Supprimé. |
| res.charset | Supprimé. |
| res.setHeader('Set-Cookie', val) | Cette fonctionnalité se limite désormais à définir la valeur de cookie de base. Utilisezres.cookie()pour plus de fonctionnalités. |

## Exemple de migration d'application

Voici un exemple de migration d’une application Express 3 vers Express 4.
Les fichiers qui nous intéressent sont `app.js` et `package.json`.

### Application de la version 3

#### app.js

Examinons une application Express v.3 avec le fichier `app.js` suivant :

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

Voici à quoi ressemble le fichier `package.json` qui accompagne la version 3 :

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

### Processus

Commencez le processus de migration en installant le middleware requis pour l’application
Express 4 et en mettant à jour Express et Pug vers leur version la plus récente respective à l’aide de la commande suivante :

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

Apportez les modifications suivantes à `app.js` :

1. Les fonctions Express Middleware intégrées `express.favicon`,
  `express.logger`, `express.methodOverride`,
  `express.session`, `express.bodyParser` et
  `express.errorHandler` ne sont plus disponibles sur l’objet
  `express`. Vous devez installer leurs fonctions alternatives
  manuellement et les charger dans l’application.
2. Vous ne devez plus charger la fonction `app.router`.
  Il ne s’agit pas d’un objet d’application Express 4 valide. Supprimez le code
  `app.use(app.router);`.
3. Assurez-vous que les fonctions middleware sont chargées dans l’ordre correct - chargez `errorHandler` après avoir chargé les routes d’application.

### Application de la version 4

#### package.json

Le fait d’exécuter la commande `npm` ci-dessus mettra à jour `package.json` comme suit :

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

Puis, supprimez le code non valide, chargez les middleware requis et procédez aux autres changements,
le cas échéant. Voici à quoi ressemble le fichier `app.js` :

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

A mois que vous deviez utiliser le module `http` (socket.io/SPDY/HTTPS) directement, vous n’avez pas à le charger et l’application peut être démarrée comme suit :

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Exécutez l'application

Le processus de migration est terminé et l’application est désormais une application
Express 4. Pour confirmer, démarrez l’application en utilisant la commande suivante :

```
$ node .
```

Chargez [http://localhost:3000](http://localhost:3000)
et voyez comment la page d’accueil est générée par Express 4.

## Mise à niveau vers le générateur d'applications Express 4

L’outil de ligne de commande qui permet de générer une application Express est toujours
`express`, mais pour effectuer la mise à niveau vers la nouvelle version, vous devez désinstaller
le générateur d’applications Express 3 puis installer la nouvelle version d’`express-generator`.

### Installation

Si le générateur d’applications Express 3 est installé sur votre système, vous devez le désinstaller :

```
$ npm uninstall -g express
```

En fonction de la configuration de vos privilèges de fichier et de répertoire,
vous devrez exécuter cette commande avec `sudo`.A présent, installez le nouveau générateur :

Now install the new generator:

```
$ npm install -g express-generator
```

En fonction de la configuration de vos privilèges de fichier et de répertoire,
vous devrez exécuter cette commande avec `sudo`.A présent, installez le nouveau générateur :

Désormais, la commande `express` sur votre système est mise à jour vers le générateur Express 4.

### Modifications du générateur d'applications

Les options et les syntaxe de commande restent généralement identiques, avec les exceptions suivantes :

- L’option `--sessions` a été supprimée.
- L’option `--jshtml` a été supprimée.
- L’option `--hogan` a été ajoutée à la prise en charge de [Hogan.js](http://twitter.github.io/hogan.js/).

### Exemple

Exécutez la commande suivante pour créer une application Express 4 :

```
$ express app4
```

Si vous examinez le contenu du fichier `app4/app.js`, vous remarquerez que toutes
les fonctions middleware (sauf `express.static`) qui sont requises pour
l’application sont chargées en tant que modules indépendants, et le middleware `router` n’est plus chargé
explicitement dans l’application.

Vous noterez également que le fichier `app.js` est désormais un module Node.js, contrairement à l’application autonome qui a été générée par l’ancien générateur.

Après avoir installé les dépendances, démarrez l’application en utilisant la commande suivante :

```
$ npm start
```

Si vous examinez le script de démarrage npm dans le fichier `package.json`,
vous remarquerez dorénavant que la commande qui démarre l’application est
`node ./bin/www` alors qu’il s’agissait de `node app.js`
dans Express 3.

Puisque le fichier `app.js` qui a été généré par le générateur Express 4 est
désormais un module Node.js, il ne peut plus être démarré indépendamment en tant qu’application
(sauf si vous modifiez le code). Le module doit être chargé dans un fichier Node.js et démarré
via le fichier Node.js. Dans cet exemple, le fichier Node.js est `./bin/www`.

Ni le répertoire `bin` ni le fichier `www`
sans extension n’est obligatoire pour créer une application Express ou démarrer celle-ci. Ce ne sont ici que des suggestions faites par le générateur, donc n’hésitez pas à les modifier si besoin.

Pour se débarrasser du répertoire `www` et garder la présentation d’Express 3,
supprimez la ligne `module.exports = app;` à la fin du fichier
`app.js`, puis collez le code suivant à la place :

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

Assurez-vous d’avoir chargé le module `debug` en haut du fichier `app.js` à l’aide du code suivant :

```
var debug = require('debug')('app4')
```

Ensuite, modifiez `"start": "node ./bin/www"` dans le fichier `package.json` en `"start": "node app.js"`.

Vous avez à présent déplacé la fonctionnalité depuis `./bin/www` de nouveau
dans `app.js`. Cette modification n’est pas recommandée, mais l’exercice vous aide à comprendre le mode de fonctionnement
du fichier `./bin/www` et la raison pour laquelle le fichier `app.js` ne se lance plus seul.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/migrating-4.md          )
