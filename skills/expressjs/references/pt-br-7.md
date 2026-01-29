# Express atrás de proxies and more

# Express atrás de proxies

> Learn how to configure Express.js applications to work correctly behind reverse proxies, including using the trust proxy setting to handle client IP addresses.

# Express atrás de proxies

When running an Express app behind a reverse proxy, some of the Express APIs may return different values than expected. In order to adjust for this, the `trust proxy` application setting may be used to expose information provided by the reverse proxy in the Express APIs. The most common issue is express APIs that expose the client’s IP address may instead show an internal IP address of the reverse proxy.

When configuring the `trust proxy` setting, it is important to understand the exact setup of the reverse proxy. Since this setting will trust values provided in the request, it is important that the combination of the setting in Express matches how the reverse proxy operates.

Ao executar um aplicativo do Express atrás de um proxy,
configure (usando [app.set()](https://expressjs.com/pt-br/4x/api.html#app.set)) a variável do
aplicativo `trust proxy` para um dos valores
listados na seguinte tabela.

| Tipo | Valor |
| --- | --- |
| Booleano | Setrue, o endereço de IP do cliente será
compreendido como a entrada mais a esquerda no cabeçalhoX-Forwarded-*.Sefalse, o aplicativo é compreendido como
exposto diretamente à Internet e o endereço de IP do cliente é
derivado a partir doreq.connection.remoteAddress. Esta
é a configuração padrão.When setting totrue, it is important to ensure that the last reverse proxy trusted is removing/overwriting all of the following HTTP headers:X-Forwarded-For,X-Forwarded-Host, andX-Forwarded-Proto, otherwise it may be possible for the client to provide any value. |
| IP addresses | An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7É possível configurar endereços de IP de qualquer uma das
formas a seguir:app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayQuando especificados, os endereços de IP ou sub-redes são
excluídos do processo de determinação de endereço, e o endereço de
IP não confiável mais próximos do servidor de aplicativos é
determinado como o endereço de IP do cliente. This works by checking ifreq.socket.remoteAddressis trusted. If so, then each address inX-Forwarded-Foris checked from right to left until the first non-trusted address. |
| Número | Use the address that is at mostnnumber of hops away from the Express application.req.socket.remoteAddressis the first hop, and the rest are looked for in theX-Forwarded-Forheader from right to left. A value of0means that the first untrusted address would bereq.socket.remoteAddress, i.e. there is no reverse proxy.When using this setting, it is important to ensure there are not multiple, different-length paths to the Express application such that the client can be less than the configured number of hops away, otherwise it may be possible for the client to provide any value. |
| Function | Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse}) |

Enabling `trust proxy` will have the following impact:

- O valor de [req.hostname](https://expressjs.com/pt-br/api.html#req.hostname) é
  derivado do valor configurado no cabeçalho
  `X-Forwarded-Host`, que pode ser configurado pelo
  cliente ou pelo proxy.
- `X-Forwarded-Proto` pode ser
  configurado pelo proxy reverso para dizer ao aplicativo se ele é
  `https` ou `http` ou até um nome
  inválido. Este valor é refletido pelo [req.protocol](https://expressjs.com/pt-br/api.html#req.protocol).
- Os valores [req.ip](https://expressjs.com/pt-br/api.html#req.ip) e
  [req.ips](https://expressjs.com/pt-br/api.html#req.ips) são populados com a lista de
  endereços do `X-Forwarded-For`.

A configuração do `trust proxy` é
implementada usando o pacote
[proxy-addr](https://www.npmjs.com/package/proxy-addr). Para
obter mais informações, consulte a documentação.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/behind-proxies.md          )

---

# Integração de Banco de dados

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# Integração de Banco de dados

A inclusão da capacidade de se conectar à banco de dados em aplicativos do Express é apenas uma questão de se carregar um driver
Node.js apropriado para o banco de dados no seu aplicativo. Este documento explica brevemente como incluir e utilizar alguns dos mais
populares módulos do Node.js para sistemas de bancos de dados no seu aplicativo do Express:

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

Estes drivers de banco de dados estão entre os muitos que estão
disponíveis. Para obter outras opções, procure no site [npm](https://www.npmjs.com/).

## Cassandra

**Módulo**: [cassandra-driver](https://github.com/datastax/nodejs-driver) **Instalação**

### Installation

```
$ npm install cassandra-driver
```

### Exemplo

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

### Exemplo

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

**Módulo**: [nano](https://github.com/dscape/nano) **Instalação**

### Installation

```
$ npm install nano
```

### Exemplo

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

**Módulo**: [levelup](https://github.com/rvagg/node-levelup) **Instalação**

### Installation

```
$ npm install level levelup leveldown
```

### Exemplo

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

**Módulo**: [mysql](https://github.com/felixge/node-mysql/) **Instalação**

### Installation

```
$ npm install mysql
```

### Exemplo

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

**Módulo**: [mongodb](https://github.com/mongodb/node-mongodb-native) **Instalação**

### Installation

```
$ npm install mongodb
```

### Exemplos.*)

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

### Exemplos (v3.*)

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

Se desejar um driver de modelo de objeto para o MongoDB,
consulte em [Mongoose](https://github.com/LearnBoost/mongoose).

## Neo4j

**Módulo**: [apoc](https://github.com/hacksparrow/apoc) **Instalação**

### Installation

```
$ npm install neo4j-driver
```

### Exemplo

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

**Módulo**: [pg](https://github.com/brianc/node-postgres) **Instalação**

### Installation

NOTA: [Ver pré-requisitos de instalação](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### Exemplo

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

**Módulo**: [pg-promise](https://github.com/vitaly-t/pg-promise)

### Installation

```
$ npm install pg-promise
```

### Exemplo

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

**Módulo**: [redis](https://github.com/mranney/node_redis) **Instalação**

### Installation

```
$ npm install redis
```

### Exemplo

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

**Módulo**: [redis](https://github.com/tediousjs/tedious) **Instalação**

### Installation

```
$ npm install tedious
```

### Exemplo

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

**Módulo**: [sqlite3](https://github.com/mapbox/node-sqlite3) **Instalação**

### Installation

```
$ npm install sqlite3
```

### Exemplo

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

**Módulo**: [elasticsearch](https://github.com/elastic/elasticsearch-js) **Instalação**

### Installation

```
$ npm install elasticsearch
```

### Exemplo

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/database-integration.md          )

---

# Depurando o Express

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Depurando o Express

Para ver todos os logs interno usados no Express, configure a
variável de ambiente `DEBUG` para
`express:*` ao ativar seu aplicativo.

```
$ DEBUG=express:* node index.js
```

No Windows, use o comando correspondente.

```
> $env:DEBUG = "express:*"; node index.js
```

Executar este comando no aplicativo padrão gerado pelo
[express generator](https://expressjs.com/pt-br/starter/generator.html) imprime a seguinte saída:

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

Quando uma solicitação é feita em seguida para o aplicativo,
você verá os logs especificados no código do Express:

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

Para ver os logs apenas da implementação do roteador configure
o valor de `DEBUG` para
`express:router`. Do mesmo modo, para ver os logs
apenas da implementação do aplicativo configure o valor de
`DEBUG` para `express:application`,
e assim por diante.

## Aplicativos gerados peloexpress

Um aplicativo gerado pelo comando `express`
também usa o módulo de `debug` e o seu namespace de
depuração está com o escopo definido para o nome do aplicativo.

Por exemplo, se você gerou o aplicativo com o `$ express
sample-app`, é possível ativar as instruções de depuração
com o seguinte comando:

```
$ DEBUG=sample-app:* node ./bin/www
```

É possível especificar mais do que um namespace de depuração
designando uma lista de nomes separados por vírgulas:

```
$ DEBUG=http,mail,express:* node index.js
```

## Advanced options

When running through Node.js, you can set a few environment variables that will change the behavior of the debug logging:

| Nome | Objetivo |
| --- | --- |
| DEBUG | Enables/disables specific debugging namespaces. |
| DEBUG_COLORS | Whether or not to use colors in the debug output. |
| DEBUG_DEPTH | Object inspection depth. |
| DEBUG_FD | File descriptor to write debug output to. |
| DEBUG_SHOW_HIDDEN | Shows hidden properties on inspected objects. |

Observação

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[util.inspect()](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/debugging.md          )

---

# Manipulação de erros

> Understand how Express.js handles errors in synchronous and asynchronous code, and learn to implement custom error handling middleware for your applications.

# Manipulação de erros

*Error Handling* refers to how Express catches and processes errors that
occur both synchronously and asynchronously. Express comes with a default error
handler so you don’t need to write your own to get started.

## Catching Errors

It’s important to ensure that Express catches all errors that occur while
running route handlers and middleware.

Errors that occur in synchronous code inside route handlers and middleware
require no extra work. If synchronous code throws an error, then Express will
catch and process it. Por exemplo:

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

Defina funções de middleware de manipulação de erros da mesma
forma que outras funções de middleware, exceto que funções de
manipulação de erros possuem quatro argumentos ao invés de três:
`(err, req, res, next)`.  Por exemplo:

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

Se você tiver um manipulador de rota com as funções de retorno
de chamada é possível usar o parâmetro `route`
para ignorar o próximo manipulador de rota.
Por exemplo:

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

If `getUserById` throws an error or rejects, `next` will be called with either
the thrown error or the rejected value. If no rejected value is provided, `next`
will be called with a default Error object provided by the Express router.

Se passar qualquer coisa para a função `next()`
(exceto a sequência de caracteres `'route'`),
o Express considera a solicitação atual como estando em erro e irá
ignorar quaisquer funções restantes de roteamento e middleware que
não sejam de manipulação de erros.

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
middleware and pass them to Express for processing. Por exemplo:

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
that return promises.  Por exemplo:

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
catching, by reducing the asynchronous code to something trivial. Por exemplo:

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

## O Manipulador de Erros Padrão

O Express vem com um manipulador de erros integrado, que cuida
de qualquer erro que possa ser encontrado no aplicativo. Essa função
de middleware de manipulação de erros padrão é incluída no final da
pilha de funções de middleware.

se você passar um erro para o `next()` e você
não manipulá-lo com um manipulador de erros, ele irá ser manipulado
por um manipulador de erros integrado; o erro será escrito no cliente
com o rastreio de pilha. O rastreio de pilha não será incluído no
ambiente de produção.

Configura a variável de ambiente `NODE_ENV` para
`production`, para executar o aplicativo em modo de
produção.

When an error is written, the following information is added to the
response:

- The `res.statusCode` is set from `err.status` (or `err.statusCode`). If
  this value is outside the 4xx or 5xx range, it will be set to 500.
- The `res.statusMessage` is set according to the status code.
- The body will be the HTML of the status code message when in production
  environment, otherwise will be `err.stack`.
- Any headers specified in an `err.headers` object.

Se você chamar o `next()` com um erro após ter
inicializado escrevendo a resposta (por exemplo, se encontrar um erro
enquanto passa a resposta ao cliente) o manipulador de erros padrão do
Express fecha a conexão e falha a solicitação.

Portanto ao incluir um manipulador de erro customizado, você
desejará delegar para o mecanismo de manipulação de erros padrão no
Express, quando os cabeçalhos já tiverem sido enviados para o cliente:

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

Other error handling middleware can be found at [Express middleware](https://expressjs.com/pt-br/resources/middleware.html).

## Writing error handlers

Define error-handling middleware functions in the same way as other middleware functions,
except error-handling functions have four arguments instead of three:
`(err, req, res, next)`. Por exemplo:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Você define os middlewares de manipulação de erros por
último, após outros `app.use()` e chamads de rota; por
exemplo:

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

Repostas de dentro de uma função de middleware podem estar em
qualquer formato que preferir, como uma página HTML de erros, uma
mensagem simples, ou uma sequência de caracteres JSON.

Para propósitos organizacionais (e estrutura de alto nível), é
possível definir várias funções de middleware de manipulação de
erros, de forma muito parecida como você faria com funções de
middleware comuns. Por exemplo, se desejar definir um manipulador de
erros para solicitações feitas usando o `XHR`, e
aqueles sem, você pode usar os seguintes comandos:

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

Neste exemplo, o `logErrors` genérico pode
escrever informações de solicitações e erros no
`stderr`, por exemplo:

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

Também neste exemplo, o `clientErrorHandler` é
definido como segue; neste caso, o erro é explicitamente passado para
o próximo:

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

A função “catch-all” `errorHandler` pode ser implementada como segue:

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

If you have a route handler with multiple callback functions, you can use the `route` parameter to skip to the next route handler. Por exemplo:

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

Neste exemplo, o manipulador `getPaidContent`
será ignorado mas qualquer manipulador remanescente no
`app` para
`/a_route_behind_paywall` continuariam sendo
executados.

Chamadas para `next()` e `next(err)`
indicam que o manipulador atual está completo e em qual estado.  `next(err)` irá ignorar todos os manipuladores
remanescentes na cadeia exceto por aqueles que estão configurados
para manipular erros como descrito acima.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/error-handling.md          )

---

# Migrando para o Express 4

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Migrando para o Express 4

## Visão Geral

Express 4 é uma alteração de ruptura do Express 3. Isso significa que um aplicativo Express 3 existente não irá funcionar
se você atualizar a versão do Express nas suas dependências.

Este artigo cobre:

- [Mudanças no Express 4.](#changes)
- [Um exemplo](#example-migration) de migração de um aplicativo do Express 3 para o Express 4.
- [Fazendo o upgrade para o gerador de aplicativos do Express 4.](#app-gen)

## Mudanças no Express 4

Existem várias mudanças significativas no Express 4:

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [Mudanças no sistema de roteamento.](#routing)
- [Várias outras mudanças.](#other-changes)

Consulte também:

- [Novos recursos no 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migrando do 3.x para o 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Mudanças no núcleo e sistemas middleware do Express

O Express 4 não depende mais do Connect, e remove todos os
middlewares integrados do seu núcleo, exceto pela função
`express.static`. Isso significa que o
Express é agora um framework web de middleware e roteamento
independente, e que o versionamento e as liberações do Express não
são mais afetadas por atualizações nos middlewares.

Sem os middlewares integrados, você deve incluir explicitamente todos os middlewares necessários para a execução do seu aplicativo. Simplesmente siga esses passos:

1. Instale o módulo: `npm install --save <module-name>`
2. No seu aplicativo, solicite o módulo: `require('module-name')`
3. Use o módulo de acordo com sua documentação: `app.use( ... )`

A tabela a seguir lista os middlewares do Express 3 e suas contrapartes no Express 4.

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

Aqui está a [lista completa](https://github.com/senchalabs/connect#middleware) de middlewares do Express 4.

Na maioria dos casos, é possível simplesmente substituir a antiga versão 3 do middleware pela sua contraparte do Express4. Para obter detalhes, consulte a documentação do módulo no GitHub.

#### Oapp.useaceita parâmetros

Na versão 4 é possível utilizar uma variável de parâmetro para
definir o caminho onde as funções do middleware estão carregadas, e
em seguida ler o valor do parâmetro a partir do manipulador de rota.
Por exemplo:

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### O sistema de roteamento

Os aplicativos agora carregam implicitamente middlewares de
roteamento, para que não seja mais necessário se preocupar com a
ordem em que os middlewares são carregados no que diz respeito ao
middleware `router`.

A forma como as rotas são definidas são as mesmas, mas  o
sistema de roteamento possui dois novos recursos para ajudá-lo a
organizar suas rotas:

- Um novo método, `app.route()`, para criar
  manipuladores de rotas encadeáveis para um caminho de rota.
- Uma nova classe, `express.Router`, para
  criar manipuladores de rotas modulares montáveis

#### O métodoapp.route()

O novo método `app.route()` permite que sejam
criados manipuladores de rotas encadeáveis para um caminho de rota. Como o caminho é especificado em uma localização única, criar rotas
modulares é útil, já que reduz redundâncias e erros tipográficos. Para
obter mais informações sobre rotas, consulte a [documentação do Router()](https://expressjs.com/pt-br/4x/api.html#router).

Aqui está um exemplo de manipuladores de rotas encadeáveis que
são definidos usando a função `app.route()`.

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

O outro recurso que ajuda na organização das rotas é uma nova
classe, `express.Router`, que pode ser usada para
criar manipuladores de rotas modulares montáveis. Uma instância de `Router` é um middleware e sistema
de roteamento completo; por essa razão ela é frequentemente referida
como um “mini-aplicativo”

O seguinte exemplo cria um roteador como um módulo, carrega o
middleware nele, define algumas rotas, e monta-o em um caminho no
aplicativo principal.

Por exemplo, cria um arquivo roteador chamado
`birds.js` no diretório do aplicativo, com o
conteúdo a seguir:

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

Em seguida, carregue o módulo roteador no aplicativo:

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

O aplicativo será agora capaz de manipular solicitações aos
caminhos `/birds` e `/birds/about`,
e irá chamar o middleware `timeLog`
que é específico para a rota.

### Outras mudanças

A seguinte tabela lista outras pequenas, porém importantes, mudanças no Express 4:

| Objeto | Descrição |
| --- | --- |
| Node.js | O Express 4 requer o Node.js 0.10.x ou posterior e descartou o
suporte ao Node.js 0.8.x. |
| http.createServer() | O módulohttpnão é mais necessário, a não ser
que você precise trabalhar diretamente com ele (socket.io/SPDY/HTTPS). O
aplicativo pode ser iniciado usando a funçãoapp.listen(). |
| app.configure() | A funçãoapp.configure()foi removida.  Use a funçãoprocess.env.NODE_ENVouapp.get('env')para detectar o ambiente e
configurar o aplicativo de acordo com ele. |
| json spaces | A propriedade de aplicativojson spacesestá
desativada por padrão no Express 4. |
| req.accepted() | Usereq.accepts(),req.acceptsEncodings(),req.acceptsCharsets(), ereq.acceptsLanguages(). |
| res.location() | Não resolve mais URLs relativas. |
| req.params | Era uma matriz; agora é um objeto. |
| res.locals | Era uma função; agora é um objeto. |
| res.headerSent | Mudado parares.headersSent. |
| app.route | Agora disponível comoapp.mountpath. |
| res.on('header') | Removido. |
| res.charset | Removido. |
| res.setHeader('Set-Cookie', val) | A funcionalidade é agora limitada a configurar o valor básico do
cookie. Useres.cookie()para funcionalidades
adicionais. |

## Exemplo de migração de aplicativo

Aqui está um eemplo de migração de um aplicativo Express 3 para
o Express 4.
Os arquivos de interesse são `app.js` e `package.json`.

### Aplicativo da Versão 3

#### app.js

Considere um aplicativo do Express v.3 com o seguinte arquivo `app.js`:

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

O arquivo `package.json` que acompanha a
versão 3 pode parecer com algo assim:

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

Comece o processo de migração instalando os middlewares
necessários para o aplicativo Express 4 e atualizando o Express e o
Pug para as suas respectivas versões mais recentes com o seguinte
comando:

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

Faça as seguintes alterações no `app.js`:

1. As funções de middleware integradas do Express `express.favicon`,
  `express.logger`, `express.methodOverride`,
  `express.session`, `express.bodyParser` e
  `express.errorHandler` não estão mais disponíveis no objeto `express`. É
  preciso instalar manualmente as alternativas e carregá-las no aplicativo.
2. Não é mais necessário carregar a função `app.router`.
  Ela não é um objeto válido para aplicativos Express 4, portanto
  remova o código do `app.use(app.router);`.
3. Certifique-se deque as funções de middleware sejam carregadas na ordem correta - carregar a
  `errorHandler` após carregar as rotas de aplicativo.

### Aplicativo da Versão 4

#### package.json

A execução do comando `npm` acima irá
atualizar o `package.json` como a seguir:

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

Em seguida, remova o código inválido, carregue o middleware
necessário e faça outras alterações conforme necessárias. O arquivo `app.js` irá parecer com isso:

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

A não ser que precise trabalhar diretamente com
o módulo `http` (socket.io/SPDY/HTTPS),
carregá-lo não é necessário, e o aplicativo pode ser iniciado
simplesmente desta forma:

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Execute o aplicativo

O processo de migração está concluído, e o aplicativo é agora
um aplicativo Express 4. Para confirmar, inicie o aplicativo usando o
seguinte comando:

```
$ node .
```

Carregue [http://localhost:3000](http://localhost:3000)
e veja a página inicial sendo renderizada pelo Express 4.

## Fazendo o upgrade para o gerador de aplicativos do
Express 4

A ferramenta de linha de comandos para gerar um aplicativo
Express ainda é a `express`, mas para fazer o
upgrade para a nova versão , é preciso desinstalar o gerador de
aplicativos Express 3 e, em seguida, instalar o novo `express-generator`.

### Instalação

Se já tiver o gerador de aplicativos do Express 3 instalado no
seu sistema, é preciso desinstalá-lo:

```
$ npm uninstall -g express
```

Dependendo de como os seus privilégios de arquivos e diretórios estão
configurados, pode ser necessário executar este comando com `sudo`.

Agora instale o novo gerador:

```
$ npm install -g express-generator
```

Dependendo de como os seus privilégios de arquivos e diretórios estão
configurados, pode ser necessário executar este comando com `sudo`.

Agora o comando `express` no seu sistema está
atualizado para o gerador do Express 4.

### Mudanças no gerador de aplicativos

As opções e o uso do comando permanecem em grande parte as
mesmas, com as seguintes exceções:

- Foi removida a opção `--sessions`.
- Foi removida a opção `--jshtml`.
- Foi incluída a opção `--hogan` para
  suportar o [Hogan.js](http://twitter.github.io/hogan.js/).

### Exemplo

Execute o seguinte comando para criar um aplicativo do Express 4:

```
$ express app4
```

Se olhar o conteúdo do arquivo `app4/app.js`,
você verá que todas as funções de middleware (exceto
`express.static`) que são requeridas pelo aplicativo
estão a carregadas como módulos independentes, e o middleware de
`router` não está mais explicitamente carregado no
aplicativo.

Você irá também notar que o arquivo `app.js` é
agora um módulo do Node.js, ao invés do aplicativo independente
gerado pelo antigo gerador.

Após instalar as dependências, inicie o aplicativo usando o
seguinte comando:

```
$ npm start
```

Se olhar o script de inicialização npm no arquivo
`package.json`, você irá notar que o comando real
que inicia o aplicativo é o `node ./bin/www`, que
antes era `node app.js` no Express 3.

Como o arquivo `app.js` que foi gerado pelo
gerador do Express 4 é agora um módulo do Node.js, ele não pode mais
ser iniciado independentemente como um aplicativo
(a não ser que modifique o código). O módulo deve ser carregado em um
arquivo Node.js e iniciado através do arquivo Node.js. O arquivo
Node.js é `./bin/www`
neste caso.

Nem o diretório `bin` e nem o arquivo sem
extensão `www` são obrigatórios para a criação ou
inicialização de um aplicativo Express. Eles são apenas sugestões
feitas pelo gerador, portanto fique a vontade para modificá-los para
adequá-los às suas necessidades.

Se livre do diretório `www` e mantenha as
coisas “da maneira do Express 3”, exclua a linha que diz
`module.exports = app;` no final do arquivo
`app.js`, em seguida cole o seguinte código em seu
lugar:

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

Assegure-se de carregar o módulo `debug` em
cima do arquivo `app.js` usando o seguinte código:

```
var debug = require('debug')('app4')
```

Em seguida, mude o `"start": "node ./bin/www"`
no arquivo `package.json` para `"start": "node
app.js"`.

Você agora moveu a funcionalidade do
`./bin/www` de volta para o
`app.js`. Esta mudança não é recomendada, mas o
exercício ajuda você a entender como o arquivo
`./bin/www` funciona, e porque o arquivo
`app.js` não é mais iniciado por conta própria.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/migrating-4.md          )
