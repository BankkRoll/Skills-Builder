# 프록시 환경에서 Express 사용 and more

# 프록시 환경에서 Express 사용

> Express.js 애플리케이션을 리버스 프록시 뒤에서 올바르게 작동하도록 설정하는 방법을 알아보십시오. 클라이언트 IP 주소를 처리하기 위해 `trust proxy` 설정을 사용하는 것을 포함합니다.

# 프록시 환경에서 Express 사용

Express 앱이 리버스 프록시 뒤에서 실행될 때, 일부 Express API는 예상과 다른 값을 반환할 수 있습니다. 이를 조정하기 위해 `trust proxy` 애플리케이션 설정을 사용하여, Express API에서 리버스 프록시가 제공한 정보를 노출하도록 할 수 있습니다. 가장 흔한 문제는 클라이언트의 IP 주소를 반환하는 Express API가 리버스 프록시의 내부 IP 주소를 대신 보여주는 경우입니다.

`trust proxy` 설정을 구성할 때, 리버스 프록시의 정확한 구성 방식을 이해하는 것이 중요합니다. 이 설정은 요청에 포함된 값을 신뢰하게 만들기 때문에, Express의 설정이 리버스 프록시의 동작 방식과 일치해야 합니다.

프록시 뒤에서 Express 앱을 실행할 때는, ([app.set()](https://expressjs.com/ko/4x/api.html#app.set)을 이용하여) 애플리케이션 변수 `trust proxy`를 다음 표에 나열된 값 중 하나로 설정하십시오.

| 유형 | 값 |
| --- | --- |
| 부울 | true인 경우, 클라이언트의 IP 주소는X-Forwarded-*내의 가장 왼쪽 입력 항목인 것으로 인식됩니다.false인 경우, 앱이 직접 인터넷에 연결되는 것으로 인식되며 클라이언트의 IP 주소는req.connection.remoteAddress로부터 도출됩니다. 이 설정이 기본 설정입니다.trust proxy를true로 설정할 경우, 마지막으로 신뢰할 수 있는 리버스 프록시가 다음의 HTTP 헤더들을 제거하거나 덮어쓰는지 반드시 확인해야 합니다:X-Forwarded-For,X-Forwarded-Host,X-Forwarded-Proto. 그렇지 않으면 클라이언트가 임의의 값을 제공하는 것이 가능해질 수 있습니다.</div>
</td>
    </tr>
    <tr>
      <td>IP addresses</td>An IP address, subnet, or an array of IP addresses and subnets to trust as being a reverse proxy. The following list shows the pre-configured subnet names:loopback -127.0.0.1/8,::1/128linklocal -169.254.0.0/16,fe80::/10uniquelocal -10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7다음의 방법 중 하나로 IP 주소를 설정할 수 있습니다.app.set('trust proxy','loopback')// specify a single subnetapp.set('trust proxy','loopback, 123.123.123.123')// specify a subnet and an addressapp.set('trust proxy','loopback, linklocal, uniquelocal')// specify multiple subnets as CSVapp.set('trust proxy',['loopback','linklocal','uniquelocal'])// specify multiple subnets as an arrayIP 주소 또는 서브넷이 지정되는 경우, 해당 IP 주소 또는 서브넷은 주소 결정 프로세스에서 제외되며, 신뢰할 수 있는 것으로 지정되지 않은 IP 주소 중 애플리케이션 서버에서 가장 가까운 IP 주소가 클라이언트의 IP 주소로 결정됩니다. 이 설정은req.socket.remoteAddress가 신뢰된 주소인지 확인하는 방식으로 작동합니다. 신뢰된 경우,X-Forwarded-For헤더에 있는 각 IP 주소를 오른쪽에서 왼쪽으로 검사하며, 처음으로 신뢰되지 않은 주소를 만날 때까지 확인합니다.</tr>
<tr>
  <td>숫자</td>Express 애플리케이션으로부터 최대n홉(hop) 떨어진 위치에 있는 주소를 사용하게 됩니다.req.socket.remoteAddress는 첫 번째 홉이며, 그 외의 주소들은X-Forwarded-For헤더에서 오른쪽에서 왼쪽 방향으로 조회됩니다.0값을 설정하면, 첫 번째로 신뢰되지 않은 주소는req.socket.remoteAddress가 되며, 이는 리버스 프록시가 없는 상태를 의미합니다.이 설정을 사용할 때는 Express 애플리케이션까지 도달하는 경로가 하나 이상 존재하지 않도록, 즉 서로 다른 홉 수의 경로가 존재하지 않도록 주의해야 합니다. 그렇지 않으면 클라이언트가 설정된 홉 수보다 가까운 위치에서 접근할 수 있게 되어, 임의의 값을 제공하는 것이 가능해질 수 있습니다.</div>
</td>
    </tr>
    <tr>
      <td>Function</td>Custom trust implementation.app.set('trust proxy',(ip)=>{if(ip==='127.0.0.1'||ip==='123.123.123.123')returntrue// trusted IPselsereturnfalse})</tr></tbody>
</table>trust proxy를 활성화하면 다음과 같은 영향을 미칩니다:req.hostname의 값은X-Forwarded-Host헤더에 설정된 값으로부터 도출되며, 이 값은 클라이언트 또는 프록시에 의해 설정될 수 있습니다.https인지,http인지, 또는 잘못된 이름인지의 여부를 앱에 알리기 위하여 역방향 프록시가X-Forwarded-Proto를 설정할 수 있습니다. 이 값에는req.protocol이 반영됩니다.req.ip값 및req.ips값에는X-Forwarded-For의 주소 목록이 입력됩니다.trust proxy설정은proxy-addr패키지를 이용해 구현됩니다. 자세한 정보는 해당 문서를 참조하십시오. |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/behind-proxies.md          )

---

# 데이터베이스 통합

> Discover how to integrate various databases with Express.js applications, including setup examples for MongoDB, MySQL, PostgreSQL, and more.

# 데이터베이스 통합

데이터베이스를 Express 앱에 연결하는 기능을 추가하려면 앱에 포함된 데이터베이스를 위한 적절한 Node.js 드라이버를 로드해야 합니다. 이 문서에서는 Express 앱의 데이터베이스 시스템에 가장 널리 이용되고 있는 Node.js 모듈 중 다음과 같은 몇 개의 모듈을 추가 및 사용하는 방법을 설명합니다.

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

위의 데이터베이스 드라이버는 사용 가능한 여러 데이터베이스 드라이버 중 일부입니다. 다른 옵션을 확인하려면,
[npm](https://www.npmjs.com/) 사이트에서 검색하십시오.

## Cassandra

**모듈**: [cassandra-driver](https://github.com/datastax/nodejs-driver) **설치**

### 설치

```
$ npm install cassandra-driver
```

### Example

```
const cassandra = require('cassandra-driver')
const client = new cassandra.Client({ contactPoints: ['localhost'] })

client.execute('select key from system.local', (err, result) => {
  if (err) throw err
  console.log(result.rows[0])
})
```

## Couchbase

**모듈**: [couchnode](https://github.com/couchbase/couchnode)

### 설치

```
$ npm install couchbase
```

### Example

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

**모듈**: [nano](https://github.com/dscape/nano) **설치**

### 설치

```
$ npm install nano
```

### Example

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

**모듈**: [levelup](https://github.com/rvagg/node-levelup) **설치**

### 설치

```
$ npm install level levelup leveldown
```

### Example

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

**모듈**: [mysql](https://github.com/felixge/node-mysql/) **설치**

### 설치

```
$ npm install mysql
```

### Example

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

**모듈**: [mongodb](https://github.com/mongodb/node-mongodb-native) **설치**

### 설치

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

MongoDB용 오브젝트 모델 드라이버가 필요한 경우에는 [Mongoose](https://github.com/LearnBoost/mongoose)를 확인하십시오.

## Neo4j

**모듈**: [neo4j-driver](https://github.com/neo4j/neo4j-javascript-driver)

### 설치

```
$ npm install neo4j-driver
```

### Example

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

**모듈**: [oracledb](https://github.com/oracle/node-oracledb)

### 설치

참고: [설치 전제 조건 참조](https://github.com/oracle/node-oracledb#-installation).

```
$ npm install oracledb
```

### Example

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

**모듈**: [pg-promise](https://github.com/vitaly-t/pg-promise) **설치**

### 설치

```
$ npm install pg-promise
```

### Example

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

**모듈**: [redis](https://github.com/mranney/node_redis) **설치**

### 설치

```
$ npm install redis
```

### Example

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

## SQL 서버

**모듈**: [tedious](https://github.com/tediousjs/tedious)

### 설치

```
$ npm install tedious
```

### Example

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

**모듈**: [sqlite3](https://github.com/mapbox/node-sqlite3) **설치**

### 설치

```
$ npm install sqlite3
```

### Example

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

**모듈**: [elasticsearch](https://github.com/elastic/elasticsearch-js) **설치**

### 설치

```
$ npm install elasticsearch
```

### Example

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/database-integration.md          )

---

# Express 디버깅

> Learn how to enable and use debugging logs in Express.js applications by setting the DEBUG environment variable for enhanced troubleshooting.

# Express 디버깅

Express에서 사용되는 모든 내부 로그를 확인하려면, 앱을 실행할 때 `DEBUG` 환경 변수를
`express:*`로 설정하십시오.

```
$ DEBUG=express:* node index.js
```

Windows에서는 다음과 같은 명령을 사용하십시오.

```
> $env:DEBUG = "express:*"; node index.js
```

[Express 생성기](https://expressjs.com/ko/starter/generator.html)가 생성한 기본 앱에 대해 이 명령을 실행하면 다음과 같이 인쇄됩니다.

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

이후 앱에 대한 요청이 이루어지면, Express 코드에 지정된 로그를 확인할 수 있습니다.

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

라우터 구현의 로그만 확인하려면 `DEBUG`의 값을 `express:router`로 설정하십시오. 마찬가지로, 애플리케이션 구현의 로그만 확인하려면 `DEBUG`의 값을 `express:application`으로 설정하십시오. 나머지도 이와 같습니다.

## express를 통해 생성된 애플케이션

`express` 명령을 통해 생성된 애플리케이션 또한 `debug` 모듈을 사용하며, 이러한 애플리케이션의 디버그 네임스페이스의 범위는 애플리케이션의 이름으로 한정됩니다.

예를 들어 `$ express sample-app`을 통해 앱을 생성하는 경우에는 다음과 같은 명령을 통해 디버그 명령문을 사용할 수 있습니다.

```
$ DEBUG=sample-app:* node ./bin/www
```

다음과 같이 쉼표로 구분된 이름 목록을 지정하면 2개 이상의 디버그 네임스페이스를 지정할 수 있습니다.

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

참고

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[util.inspect()](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/debugging.md          )

---

# 오류 처리

> Express.js가 동기 및 비동기 코드에서 오류를 처리하는 방식을 이해하고, 애플리케이션에 맞는 사용자 정의 오류 처리 미들웨어를 구현하는 방법을 알아보세요.

# 오류 처리

에러 처리란 Express가 동기 및 비동기적으로 발생하는 에러를 포착하고 처리하는 방식을 의미합니다. Express는 기본 에러 처리기를 제공하므로 시작하기 위해 직접 작성할 필요가 없습니다.

## 에러 포착하기

Express가 라우트 핸들러와 미들웨어 실행 중 발생하는 모든 에러를 포착하는 것이 중요합니다.

라우트 핸들러 및 미들웨어 내부의 동기 코드에서 발생하는 에러는 추가 작업이 필요하지 않습니다. 동기 코드에서 에러가 발생하면 Express가 에러를 감지하여 처리합니다. 예를 들면 다음과 같습니다.

```
app.get('/', (req, res) => {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

여러 콜백 함수를 갖는 라우트 핸들러가 있는 경우에는 `route` 매개변수를 사용하여 그 다음의 라우트 핸들러로 건너뛸 수 있습니다.  예를 들면 다음과 같습니다.

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

다른 미들웨어 함수와 동일한 방법으로 오류 처리 미들웨어 함수를 정의할 수 있지만,
오류 처리 함수는 3개가 아닌 4개의 인수, 즉 `(err, req, res, next)`를
갖는다는 점이 다릅니다.
예를 들면 다음과 같습니다.

```
app.get('/user/:id', async (req, res, next) => {
  const user = await getUserById(req.params.id)
  res.send(user)
})
```

`getUserById`에서 에러가 발생하거나 거부(reject)되면, `next`는 발생한 에러 또는 거부된 값을 사용하여 호출됩니다. 만약 거부된 값(rejected value)이 제공되지 않으면 `next`는 Express 라우터가 제공하는 기본 에러 객체와 함께 호출됩니다.

`next()` 함수로 어떠한 내용을 전달하는 경우(`'route'`라는 문자열 제외), Express는 현재의 요청에 오류가 있는 것으로 간주하며, 오류 처리와 관련되지 않은 나머지 라우팅 및 미들웨어 함수를 건너뜁니다.

만약 연속적인 과정(sequence)에서 콜백이 데이터는 제공하지 않고 에러만 제공한다면 다음과 같이 코드를 간소화할 수 있습니다:

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

위 예제에서, `next`는 `fs.writeFile`의 콜백으로 제공되며 이 콜백은 에러 발생 여부와 관계없이 호출됩니다. 에러가 없으면 두 번째 핸들러가 실행되고, 그렇지 않으면 Express에서 에러를 포착하여 처리합니다.

라우트 핸들러나 미들웨어에서 호출하는 비동기 코드에서 발생하는 에러는 반드시 포착하여 Express에 전달하여 처리해야 합니다. 예를 들면 다음과 같습니다.

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

위 예제는 `try...catch` 블록을 사용하여 비동기 코드의 에러를 포착하여 Express에 전달합니다. 만약 `try...catch` 블록이 생략되면, Express는 해당 에러가 동기 핸들러 코드의 일부가 아니므로 에러를 포착하지 못할 것입니다.

프로미스를 사용하면 `try...catch` 블록의 오버헤드를 피하거나 프로미스를 반환하는 함수를 사용할 때 유용합니다. 예를 들면 다음과 같습니다.  예를 들면 다음과 같습니다.

```
app.get('/', (req, res, next) => {
  Promise.resolve().then(() => {
    throw new Error('BROKEN')
  }).catch(next) // Errors will be passed to Express.
})
```

프로미스는 동기 에러와 거부된 프로미스를 모두 자동으로 포착하므로, `next`를 최종 catch 핸들러로 제공하기만 해도 Express가 에러를 포착합니다. 이는 catch 핸들러가 에러를 첫 번째 인자로 받기 때문입니다.

또한 비동기 코드를 최소화하여 동기 에러 감지에 의존하는 핸들러 체인을 사용할 수도 있습니다. 예를 들면 다음과 같습니다.

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

위 예제에는 `readFile` 호출에서 몇 가지 간단한 내용을 포함합니다. 만약 `readFile`에서 에러가 발생한다면 Express로 해당 에러가 전달되고, 그렇지 않으면 체인의 다음 핸들러로 넘어가면서 동기적인 에러 처리 흐름으로 복귀하게 됩니다.  그런 다음 위 예제에서는 데이터 처리를 시도합니다. 만약 이 과정이 실패하면 동기 에러 핸들러가 에러를 포착합니다. 만약 이 처리를 `readFile` 콜백 내부에서 했다면 애플리케이션이 비정상 종료되어 Express 에러 핸들러가 실행되지 못할 수도 있습니다.

어떤 방법을 사용하든, Express 에러 핸들러가 호출되고 애플리케이션이 정상적으로 작동하게 하려면 Express가 에러를 받도록 해야 합니다.

## 기본 오류 핸들러

Express는 내장된 오류 핸들러와 함께 제공되며, 내장 오류 핸들러는 앱에서 발생할 수 있는 모든 오류를 처리합니다. 이러한 기본 오류 처리 미들웨어 함수는 미들웨어 함수 스택의 끝에 추가됩니다.

`next()`로 오류를 전달하지만 오류 핸들러에서 해당 오류를
처리하지 않는 경우, 기본 제공 오류 핸들러가 해당 오류를 처리하며, 해당 오류는
클라이언트에 스택 추적과 함께 기록됩니다. 스택 추적은 프로덕션 환경에 포함되어 있지 않습니다.

프로덕션 모드에서 앱을 실행하려면 환경 변수 `NODE_ENV`를 `production`으로 설정하십시오.

에러가 기록되면 다음 정보가 응답에 추가됩니다:

- `res.statusCode`는 `err.status` 또는 `err.statusCode`값으로 설정됩니다. 이 값이 4xx 또는 5xx 범위를 벗어나면 500 으로 설정됩니다.
- `res.statusMessage`는 상태 코드에 따라 설정됩니다.
- body는 프로덕션 환경일 경우 상태 코드 메시지의 HTML이 되고, 그렇지 않은 경우 `err.stack`이 됩니다.
- `err.headers` 객체에 지정된 모든 헤더가 포함됩니다.

응답의 기록을 시작한 후에 오류가 있는 `next()`를
호출하는 경우(예: 응답을 클라이언트로 스트리밍하는 중에 오류가
발생하는 경우), Express의 기본 오류 핸들러는 해당 연결을 닫고
해당 요청을 처리하지 않습니다.

따라서 사용자 정의 오류 핸들러를 추가할 때, 헤더가 이미 클라이언트로 전송된 경우에는
다음과 같이 Express 내의 기본 오류 처리 메커니즘에 위임해야 합니다:

```
function errorHandler (err, req, res, next) {
  if (res.headersSent) {
    return next(err)
  }
  res.status(500)
  res.render('error', { error: err })
}
```

만약 `next()`를 여러분의 코드에서 여러 번 호출한다면, 사용자 정의 오류 핸들러가 있음에도 불구하고 기본 오류 핸들러가 발동될 수 있음에 주의하십시오.

다른 에러 핸들링 미들웨어는 [Express middleware](https://expressjs.com/ko/resources/middleware.html) 에서 확인할 수 있습니다.

## 에러 핸들러 작성하기

에러 핸들링 미들웨어 함수는 다른 미들웨어 함수와 동일한 방식으로 정의합니다. 단, 에러 핸들링 함수는 세 개가 아닌 네 개의 인수(`err`, `req`, `res`, `next`)를 받는다는 점이 다릅니다. 예를 들면 다음과 같습니다.

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

오류 처리 미들웨어는 다른 `app.use()` 및 라우트 호출을 정의한 후에 마지막으로 정의해야 하며, 예를 들면 다음과 같습니다.

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

미들웨어 함수 내부로부터의 응답은 HTML 오류 페이지, 단순한 메시지 또는 JSON 문자열 등 여러분이 선호하는 모든 형식일 수 있습니다.

조직적(및 상위 레벨 프레임워크) 목적을 위해, 여러 오류 처리
미들웨어 함수를 정의할 수 있으며, 이는 일반적인 미들웨어 함수를 정의할 때와
매우 비슷합니다. 예를 들어 `XHR`를 이용한 요청 및
그렇지 않은 요청에 대한 오류 처리를 정의하려는 경우, 다음과 같은 명령을 사용할 수 있습니다.

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

이 예에서 일반 `logErrors`는 요청 및 오류 정보를 `stderr`에
기록할 수도 있으며, 예를 들면 다음과 같습니다.

```
function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}
```

또한 이 예에서 `clientErrorHandler`는 다음과 같이 정의되며, 이 경우 오류는 명시적으로 그 다음 항목으로 전달됩니다.

에러 핸들링 함수에서 “next”를 호출하지 **않을** 경우, response를 작성하고 종료해야 합니다. 그렇지 않으면 해당 request는 “중단(hang)”되어 가비지 컬렉션 대상이 되지 않습니다.

```
function clientErrorHandler (err, req, res, next) {
  if (req.xhr) {
    res.status(500).send({ error: 'Something failed!' })
  } else {
    next(err)
  }
}
```

“모든 오류를 처리하는(catch-all)” `errorHandler` 함수는 다음과 같이 구현될 수 있습니다.

```
function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

만약 여러개의 콜백 함수가 있는 라우트 핸들러가 있다면 `route` 매개변수를 사용하여 다음 라우트 핸들러로 건너뛸 수 있습니다. 예를 들면 다음과 같습니다.

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

이 예에서 `getPaidContent` 핸들러의 실행은 건너뛰지만, `/a_route_behind_paywall`에 대한 `app` 내의 나머지 핸들러는 계속하여 실행됩니다.

`next()` 및 `next(err)`에 대한 호출은 현재의 핸들러가 완료되었다는 것과 해당 핸들러의 상태를 표시합니다.  `next(err)`는 위에 설명된 것과 같이 오류를 처리하도록 설정된 핸들러를 제외한 체인 내의 나머지 모든 핸들러를 건너뜁니다.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/error-handling.md          )

---

# Express 4로의 이전

> A guide to migrating your Express.js applications from version 3 to 4, covering changes in middleware, routing, and how to update your codebase effectively.

# Express 4로의 이전

## 개요

Express 4는 Express 3로부터 근본적으로 변경되었습니다. 따라서 기존 Express 3 앱의 종속 항목의 Express 버전을 업데이트하면 기존 Express 3 앱은 작동하지 않습니다.

이 문서에서는 다음을 다룹니다.

- [Express 4에서의 변경사항.](#changes)
- Express 3 앱의 Express 4로의 마이그레이션의 [예](#example-migration).
- [Express 4 생성기로의 업그레이드.](#app-gen)

## Express 4에서의 변경사항

Express 4에서는 여러 중요한 부분이 변경되었습니다.

- [Changes to Express core and middleware system.](#core-changes) The dependencies on Connect and built-in middleware were removed, so you must add middleware yourself.
- [라우팅 시스템에 대한 변경.](#routing)
- [기타 다양한 변경사항.](#other-changes)

또한 다음을 참조하십시오.

- [New features in 4.x.](https://github.com/expressjs/express/wiki/New-features-in-4.x)
- [Migrating from 3.x to 4.x.](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x)

### Express 코어 및 미들웨어 시스템에 대한 변경

Express 4는 더 이상 Connect에 종속되지 않으며, `express.static` 함수를
제외한 모든 기본 제공 미들웨어가 Express 4 코어에서 제거되었습니다. 따라서 Express는
이제 독립적인 라우팅 및 미들웨어 웹 프레임워크가 되었으며, Express 버전화 및 릴리스는
미들웨어 업데이트의 영향을 받지 않게 되었습니다.

기본 제공 미들웨어가 없으므로 사용자는 앱을 실행하는 데 필요한
모든 미들웨어를 명시적으로 추가해야 합니다. 이를 위해서는 다음 단계를 따르기만 하면 됩니다.

1. 모듈 설치: `npm install --save <module-name>`
2. 앱 내에서, 모듈 요청: `require('module-name')`
3. 해당 모듈의 문서에 따라 모듈 사용: `app.use( ... )`

다음 표에는 Express 3의 미들웨어 및 그에 대응하는 Express 4의 미들웨어가 나열되어 있습니다.

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

Express 4 미들웨어의 [전체 목록](https://github.com/senchalabs/connect#middleware)을 참조하십시오.

대부분의 경우 구버전인 버전 3의 미들웨어를 Express 4의 대응하는
미들웨어로 대체할 수 있습니다. 상세 정보는 GitHub 모듈 문서를
참조하십시오.

#### app.use가 매개변수를 수락

버전 4에서는 미들웨어 함수가 로드되는 경로를 정의하기 위하여 가변 매개변수를 사용할 수 있으며, 이후 라우트 핸들러로부터 매개변수의 값을 읽을 수 있습니다.
예를 들면 다음과 같습니다.

```
app.use('/book/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
})
```

### 라우팅 시스템

이제 앱은 라우팅 미들웨어를 암시적으로 로드하므로, 더 이상
`router` 미들웨어에 대한 미들웨어 로드 순서에 대해
걱정할 필요가 없습니다.

라우트를 정의하는 방법은 변경되지 않았지만, 라우트의 구성을 돕기 위하여
라우팅 시스템에는 다음과 같은 2개의 새로운 기능이 추가되었습니다.

- 라우트 경로에 대하여 체인 가능한 라우트 핸들러를 작성할 수 있는 새로운 메소드인 `app.route()`.
- 모듈식 마운팅 가능한 라우트 핸들러를 작성할 수 있는 새로운 클래스인 `express.Router`.

#### app.route()메소드

새롭게 추가된 `app.route()` 메소드를 이용하면 라우트 경로에 대하여 체인 가능한
라우트 핸들러를 작성할 수 있습니다. 경로는 한 곳에 지정되어 있으므로, 모듈식 라우트를 작성하면 중복성과 오타가 감소하여 도움이 됩니다. 라우트에 대한
자세한 정보는 [Router()문서](https://expressjs.com/ko/4x/api.html#router)를 참조하십시오.

`app.route()` 함수를 사용하여 정의된 체인 라우트 핸들러의 예는 다음과 같습니다.

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

#### express.Router클래스

라우트의 구성을 돕는 다른 기능은 새롭게 추가된 클래스인
`express.Router`이며, 이를 이용해 모듈식 마운팅 가능한
라우트 핸들러를 작성할 수 있습니다. `Router` 인스턴스는 완전한 미들웨어이자
라우팅 시스템이며, 따라서 “미니 앱(mini-app)”이라고 불리는 경우가 많습니다.

다음 예에서는 라우터를 모듈로서 작성하고, 라우터 모듈에서 미들웨어를 로드하고,
몇몇 라우트를 정의하고, 기본 앱의 한 경로에 라우터 모듈을 마운트합니다.

예를 들면, 다음의 내용이 입력된 `birds.js`라는 이름의 라우터 파일을
앱 디렉토리에 작성할 수 있습니다.

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

이후 앱 내에서 다음과 같이 라우터 모듈을 로드하십시오.

```
var birds = require('./birds')

// ...

app.use('/birds', birds)
```

앱은 이제 `/birds` 및 `/birds/about` 경로에 대한
요청을 처리할 수 있게 되었으며, 해당 라우트에 대한 특정한 미들웨어인
`timeLog`를 로드할 것입니다.

### 기타 변경사항

다음 표에는 Express 4의 작지만 중요한 다른 변경사항이 나열되어 있습니다.

| 오브젝트 | 설명 |
| --- | --- |
| Node.js | Express 4에는 Node.js 0.10.x 이상이 필요하며 Node.js 0.8.x에 대한 지원은
중단되었습니다. |
| http.createServer() | http모듈을 이용해 직접 작업해야 하는 경우(socket.io/SPDY/HTTPS)를 제외하면,http모듈이 더 이상 필요하지 않습니다.app.listen()함수를 이용해 앱을 시작할 수 있습니다. |
| app.configure() | app.configure()함수가 제거되었습니다.  환경을 발견하고
그에 따라 앱을 구성하려면process.env.NODE_ENV또는app.get('env')함수를 사용하십시오. |
| json spaces | Express 4에서는 기본적으로json spaces애플리케이션 특성을 사용하지 않습니다. |
| req.accepted() | req.accepts(),req.acceptsEncodings(),req.acceptsCharsets()및req.acceptsLanguages()를 사용하십시오. |
| res.location() | 더 이상 상대 URL을 분석하지 않습니다. |
| req.params | 이전에는 배열이었지만 이제 오브젝트가 되었습니다. |
| res.locals | 이전에는 함수였지만 이제 오브젝트가 되었습니다. |
| res.headerSent | res.headersSent로 변경되었습니다. |
| app.route | 이제app.mountpath로 사용 가능합니다. |
| res.on('header') | 제거되었습니다. |
| res.charset | 제거되었습니다. |
| res.setHeader('Set-Cookie', val) | 이제 기능이 기본 쿠키 값의 설정으로 제한되었습니다. 추가적인
기능을 위해서는res.cookie()를 사용하십시오. |

## 앱 마이그레이션의 예

여기서는 Express 3 애플리케이션을 Express 4로 마이그레이션하는 예를 살펴보겠습니다.
대상 파일은 `app.js` 및 `package.json`입니다.

### 버전 3 앱

#### app.js

다음과 같은 `app.js` 파일을 갖는 Express 버전 3 애플리케이션을 가정합니다.

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

동반되는 버전 3의 `package.json` 파일의 내용은
다음과 같을 수 있습니다.

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

### 프로세스

다음의 명령을 통해 Express 4에 필요한 미들웨어를 설치하고 Express 및 Pug를
각각 최신 버전으로 업데이트하여 마이그레이션 프로세스를
시작하십시오.

```
$ npm install serve-favicon morgan method-override express-session body-parser multer errorhandler express@latest pug@latest --save
```

`app.js`를 다음과 같이 변경하십시오.

1. 기본 제공 Express 미들웨어 함수인 `express.favicon`,
  `express.logger`, `express.methodOverride`,
  `express.session`, `express.bodyParser` 및
  `express.errorHandler`는 더 이상 `express`
  오브젝트에 사용할 수 없습니다. 이들 함수의 대체 함수를 수동으로
  설치한 후 앱에서 로드해야 합니다.
2. `app.router` 함수는 이제 로드할 필요가 없습니다.
  이 함수는 유효한 Express 4 앱 오브젝트가 아니므로
  `app.use(app.router);` 코드를 제거하십시오.
3. 미들웨어 함수들이 올바른 순서로 로드되는지 확인하십시오(앱 라우트를 로드한 후 `errorHandler`를 로드).

### 버전 4 앱

#### package.json

위의 `npm` 명령을 실행하면 `package.json`이 다음과 같이 업데이트됩니다.

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

이후 올바르지 않은 코드를 제거하고, 필요한 미들웨어를 로드하고,
필요에 따라 다른 변경을 실행하십시오. `app.js` 파일의 내용은 다음과 같습니다.

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

`http` 모듈을 이용해 직접 작업해야 하는 경우(socket.io/SPDY/HTTPS)를 제외하면 `http` 모듈을 로드할 필요가 없으며, 다음과 같은 방법으로 간단히 앱을 시작할 수 있습니다.

```
app.listen(app.get('port'), () => {
  console.log('Express server listening on port ' + app.get('port'))
})
```

### Run the app

마이그레이션 프로세스가 완료되었으며, 이제 앱은
Express 4 앱이 되었습니다. 확인을 위하여, 다음의 명령을 이용해 앱을 시작하십시오.

```
$ node .
```

[http://localhost:3000](http://localhost:3000)을
로드한 후 홈 페이지가 Express 4에 의해 렌더링되는 것을 확인하십시오.

## Express 4 앱 생성기로의 업그레이드

Express 앱을 생성하기 위한 명령행 도구는 여전히
`express`이지만, 새 버전으로 업그레이드하려면
Express 3 앱 생성기의 설치를 제거한 후 새로운
`express-generator`를 설치해야 합니다.

### 설치

Express 3 앱 생성기가 이미 시스템에 설치되어 있는 경우, 다음과 같이
Express 3 앱 생성기의 설치를 제거해야 합니다.

```
$ npm uninstall -g express
```

파일 및 디렉토리 권한이 구성된 방식에 따라서, 위의 명령은
`sudo`를 이용해 실행해야 할 수도 있습니다.

이제 다음과 같이 새 생성기를 설치하십시오.

```
$ npm install -g express-generator
```

파일 및 디렉토리 권한이 구성된 방식에 따라서, 위의 명령은
`sudo`를 이용해 실행해야 할 수도 있습니다.

이제 시스템의 `express` 명령이 Express 4 생성기로
업데이트되었습니다.

### 앱 생성기에 대한 변경사항

다음을 제외하면, 명령의 옵션 및 용도는 대체로 동일하게 유지되었습니다.

- `--sessions` 옵션이 제거되었습니다.
- `--jshtml` 옵션이 제거되었습니다.
- [Hogan.js](http://twitter.github.io/hogan.js/)를 지원하기 위한 `--hogan` 옵션이 추가되었습니다.

### Example

Express 4 앱을 작성하기 위하여 다음의 명령을 실행하십시오.

```
$ express app4
```

`app4/app.js` 파일의 내용을 살펴보면, 앱에 필요한 모든 미들웨어
함수(`express.static` 제외)가 독립적인 모듈로서 로드되며
`router` 미들웨어는 이제 앱에 명시적으로 로드되지 않는다는 것을
알 수 있습니다.

또한 이전에 `app.js` 파일은 구버전의 생성기에 의해 생성되는 독립형 앱이었지만, 이제는 Node.js의 모듈이 되었다는 것을 알 수 있습니다.

종속 항목을 설치한 후, 다음의 명령을 이용해 앱을 시작하십시오.

```
$ npm start
```

`package.json` 파일 내의 npm 시작 스크립트를 살펴보면,
Express 3에서는 `node app.js`를 이용해 앱을 시작했지만,
이제 앱을 시작하는 실제 명령은 `node ./bin/www`라는 것을
알 수 있습니다.

Express 4 생성기에 의해 생성된 `app.js` 파일은 이제 Node.js의 모듈이므로,
`app.js` 파일은 더 이상 하나의 앱으로서 독립적으로 시작될 수
없습니다(코드를 수정하는 경우 제외). 이러한 모듈은 Node.js 파일에서 로드되어야 하며
Node.js 파일을 통해 시작되어야 합니다. 이 경우에서 Node.js 파일은
`./bin/www`입니다.

이제는 Express 앱을 작성하거나 앱을 시작하는 데 있어 `bin` 디렉토리 또는
확장자 없는 `www` 파일이 필수가 아닙니다. 이들은
단지 생성기에 의한 추천사항이며, 따라서 필요사항에 맞추어 수정해도
좋습니다.

`www` 디렉토리를 제거하고 “Express 3의 방식”을 유지하려면,
`app.js` 파일의 끝에 있는 `module.exports = app;`가
포함된 행을 삭제한 후 그 자리에 다음의 코드를 붙여넣으십시오.

```
app.set('port', process.env.PORT || 3000)

var server = app.listen(app.get('port'), () => {
  debug('Express server listening on port ' + server.address().port)
})
```

`debug` 모듈은 다음의 코드를 이용하여 `app.js` 파일의 맨 위에서 로드되어야 합니다.

```
var debug = require('debug')('app4')
```

다음으로, `package.json` 파일의 `"start": "node ./bin/www"`를 `"start": "node app.js"`로 변경하십시오.

이제 `./bin/www`의 기능이 다시 `app.js`로
이전되었습니다. 이러한 변경은 권장되지 않지만, 이러한 연습을 통해
`./bin/www` 파일의 작동 원리를 이해하고 `app.js` 파일이
더 이상 자체적으로 시작되지 않는 이유를 이해할 수 있습니다.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/migrating-4.md          )
