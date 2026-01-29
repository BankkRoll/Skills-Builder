# Usando middlewares and more

# Usando middlewares

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# Usando middlewares

O Express é uma estrutura web de roteamento e middlewares que
tem uma funcionalidade mínima por si só: Um aplicativo do Express é
essencialmente uma série de chamadas de funções de middleware.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/pt-br/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/pt-br/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. A próxima função middleware é
comumente denotada por uma variável chamada `next`.

Funções de middleware podem executar as seguintes tarefas:

- Executar qualquer código.
- Fazer mudanças nos objetos de solicitação e resposta.
- Encerrar o ciclo de solicitação-resposta.
- Chamar a próxima função de middleware na pilha.

Se a atual função de middleware não terminar o ciclo de
solicitação-resposta, ela precisa chamar `next()`
para passar o controle para a próxima função de middleware. Caso
contrário, a solicitação ficará suspensa.

Um aplicativo Express pode usar os seguintes tipos de middleware:

- [Middleware de nível do aplicativo](#middleware.application)
- [Middleware de nível de roteador](#middleware.router)
- [Middleware de manipulação de erros](#middleware.error-handling)
- [Middleware integrado](#middleware.built-in)
- [Middleware de Terceiros](#middleware.third-party)

É possível carregar middlewares de nível de roteador e de nível do aplicativo com um caminho de montagem opcional.
É possível também carregar uma série de funções de middleware juntas, o que cria uma sub-pilha do sistema de middleware em um ponto de montagem.

## Middleware de nível do aplicativo

Bind application-level middleware to an instance of the [app object](https://expressjs.com/pt-br/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

Este exemplo mostra uma função de middleware sem um caminho de
montagem. A função é executada sempre que o aplicativo receber uma
solicitação.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

Este exemplo mostra uma função de middleware montada no caminho
`/user/:id`. A função é executada para qualquer tipo
de solicitação HTTP no caminho `/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Este exemplo mostra uma rota e sua função
manipuladora (sistema de middleware). A função manipula solicitações
GET ao caminho `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

Aqui está um exemplo de carregamento de um série de funções de
middleware em um ponto de montagem, com um caminho de montagem.
Ele
ilustra uma sub-pilha de middleware que imprime informações de
solicitação para qualquer tipo de solicitação HTTP no caminho `/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Manipuladores de rota permitem a você definir várias rotas para
um caminho. O exemplo abaixo define duas rotas para solicitações GET
no caminho `/user/:id`. A segunda rota não irá
causar nenhum problema, mas ela nunca será chamada pois a primeira
rota termina o ciclo solicitação-resposta.

Este exemplo mostra uma sub-pilha de middleware que manipula
solicitações GET no caminho `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
}, (req, res, next) => {
  res.send('User Info')
})

// handler for the /user/:id path, which prints the user ID
app.get('/user/:id', (req, res, next) => {
  res.send(req.params.id)
})
```

`redirect`

Observação

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

Este exemplo mostra uma sub-pilha de middleware que manipula
solicitações GET no caminho `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next route
  if (req.params.id === '0') next('route')
  // otherwise pass the control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // send a regular response
  res.send('regular')
})

// handler for the /user/:id path, which sends a special response
app.get('/user/:id', (req, res, next) => {
  res.send('special')
})
```

Middleware can also be declared in an array for reusability.

É possível ter mais do que um diretório estático por aplicativo:

```
function logOriginalUrl (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}

function logMethod (req, res, next) {
  console.log('Request Type:', req.method)
  next()
}

const logStuff = [logOriginalUrl, logMethod]
app.get('/user/:id', logStuff, (req, res, next) => {
  res.send('User Info')
})
```

## Middleware de nível de roteador

Middlewares de nível de roteador funcionam da mesma forma que
os middlewares de nível do aplicativo, mas estão vinculados a uma
instância do `express.Router()`.

```
const router = express.Router()
```

Carregue os middlewares de nível de roteador usando as funções `router.use()` e `router.METHOD()`.

O seguinte código de exemplo replica o sistema de middleware
que é mostrado acima para o middleware de nível do aplicativo, usando
um middleware de nível de roteador:

```
const express = require('express')
const app = express()
const router = express.Router()

// a middleware function with no mount path. This code is executed for every request to the router
router.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})

// a middleware sub-stack shows request info for any type of HTTP request to the /user/:id path
router.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})

// a middleware sub-stack that handles GET requests to the /user/:id path
router.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next router
  if (req.params.id === '0') next('route')
  // otherwise pass control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // render a regular page
  res.render('regular')
})

// handler for the /user/:id path, which renders a special page
router.get('/user/:id', (req, res, next) => {
  console.log(req.params.id)
  res.render('special')
})

// mount the router on the app
app.use('/', router)
```

Para obter mais detalhes sobre a função `serve-static` e suas opções, consulte: documentação do[serve-static](https://github.com/expressjs/serve-static).

Este exemplo mostra uma sub-pilha de middleware que manipula
solicitações GET no caminho `/user/:id`.

```
const express = require('express')
const app = express()
const router = express.Router()

// predicate the router with a check and bail out when needed
router.use((req, res, next) => {
  if (!req.headers['x-auth']) return next('router')
  next()
})

router.get('/user/:id', (req, res) => {
  res.send('hello, user!')
})

// use the router and 401 anything falling through
app.use('/admin', router, (req, res) => {
  res.sendStatus(401)
})
```

## Middleware de manipulação de erros

Middlewares de manipulação de erros sempre levam *quatro* argumentos. Você deve fornecer quatro argumentos para identificá-lo como uma
função de middleware de manipulação de erros. Mesmo se você não
precisar usar o objeto `next`, você deve
especificá-lo para manter a assinatura. Caso contrário, o objeto
`next` será interpretado como um middleware comum e
a manipulação de erros falhará.

Defina funções de middleware de manipulação de
erros da mesma forma que outras funções de middleware, exceto que com
quatro argumentos ao invés de três, especificamente com a assinatura
`(err, req, res, next)`):

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Para obter detalhes sobre middleware de manipulação de erros,
consulte [Manipulação de erros](https://expressjs.com/pt-br/guide/error-handling.html).

## Middleware integrado

Desde a versão 4.x, o Express não depende mais do [Connect](https://github.com/senchalabs/connect). Com
exceção da `express.static`, todas as funções de
middleware que eram previamente incluídas com o Express estão agora
em módulos separados. Visualize  a lista
de funções de middleware.

Aqui está um exemplo de uso da função de middleware `express.static` com um objeto options elaborado:

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Middleware de Terceiros

Use middlewares de terceiros para incluir funcionalidades aos aplicativos do Express

Instale o módulo Node.js para a funcionalidade requerida, em seguida carregue-a no seu aplicativo no nível do aplicativo ou no nível de roteador.

O exemplo a seguir ilustra a instalação e carregamento da
função de middleware para análise sintática de cookies `cookie-parser`.

```
$ npm install cookie-parser
```

```
const express = require('express')
const app = express()
const cookieParser = require('cookie-parser')

// load the cookie-parsing middleware
app.use(cookieParser())
```

Para obter uma lista parcial de funções de middleware de
terceiros que são comumente utilizadas com o Express, consulte:
[Middleware de Terceiros](https://expressjs.com/pt-br/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/using-middleware.md          )

---

# Usando mecanismos de modelo com o Express

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Usando mecanismos de modelo com o Express

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/pt-br/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/pt-br/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, é o diretório onde os arquivos de
  modelo estão localizados. Por exemplo: `app.set('views',
  './views')`
  This defaults to the `views` directory in the application root directory.
- `view engine`, o mecanismo de modelo a ser
  usado. Por Exemplo: `app.set('view engine', 'pug')`

Em seguida instale o pacote npm correspondente ao mecanismo de modelo:

```
$ npm install pug --save
```

Mecanismos de modelo compatíveis com o Express como o Pug exportam
uma função chamada `__express(filePath, options,
callback)`, que é chamada pela função
`res.render()` para renderizar o código de modelo.

Alguns mecanismos de modelo não seguem esta convenção. A
biblioteca [Consolidate.js](https://www.npmjs.org/package/consolidate)
segue esta convenção mapeando todos os mecanismos de modelo populares
do Node.js, e portanto funciona de forma harmoniosa com o Express.

Após o mecanismo de visualização estar configurado, você não
precisa especificar o mecanismo ou carregar o módulo do mecanismo de
modelo no seu aplicativo; o Express carrega o módulo internamente,
como mostrado abaixo (para o exemplo acima).

```
app.set('view engine', 'pug')
```

Crie um arquivo de modelo do Pug
chamado `index.pug` no diretório
`views`, com o seguinte conteúdo:

```pug
html
  head
    title= title
  body
    h1= message
```

Em seguida crie uma rota para renderizar o arquivo
`index.pug`. Se a propriedade `view
engine` não estiver configurada, é preciso especificar a
extensão do arquivo `view`. Caso contrário, é
possível omití-la.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Ao fazer uma solicitação à página inicial, o arquivo `index.pug` será renderizado como HTML.

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/using-template-engines.md          )

---

# Escrevendo middlewares para uso em aplicativos do Express

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Escrevendo middlewares para uso em aplicativos do Express

## Visão Geral

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/pt-br/5x/api.html#req) (`req`), the [response object](https://expressjs.com/pt-br/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. A próxima função middleware é
comumente denotada por uma variável chamada `next`.

Funções de middleware podem executar as seguintes tarefas:

- Executar qualquer código.
- Fazer mudanças nos objetos de solicitação e resposta.
- Encerrar o ciclo de solicitação-resposta.
- Chamar o próximo middleware na pilha.

Se a atual função de middleware não terminar o ciclo de
solicitação-resposta, ela precisa chamar `next()`
para passar o controle para a próxima função de middleware. Caso
contrário, a solicitação ficará suspensa.

O exemplo a seguir mostra os elementos de uma chamada de função de middleware:

|  | O método HTTP para o qual a função de middleware é aplicada.</tbody>Caminho (rota) para o qual a função de middleware é aplicada.A função de middleware.Argumento de retorno de chamada para a função de middleware, chamado de "next" por convenção.HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/writing-middleware.md          )

---

# Comunidade

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# Comunidade

## Comitê técnico

O comitê técnico do Express se reúne on-line a cada duas semanas (conforme necessário) para discutir o desenvolvimento e a manutenção do Express,
e outras questões relevantes para o projeto Express. Cada reunião é normalmente anunciada em um
[expressjs/discussions issue](https://github.com/expressjs/discussions/issues) com um link para participar ou visualizar a reunião, que é
aberto a todos os observadores.

As reuniões são gravadas; para obter uma lista das gravações, consulte o [canal no YouTube do Express.js](https://www.youtube.com/channel/UCYjxjAeH6TRik9Iwy5nXw7g).

Os membros do comitê técnico do Express são:

**Ativo:**

- [@blakeembrey](https://github.com/blakeembrey) - Blake Embrey
- [@crandmck](https://github.com/crandmck) - Rand McKinney
- [@LinusU](https://github.com/LinusU) - Linus Unnebäck
- [@ulisesgascon](https://github.com/ulisesGascon) - Ulises Gascón
- [@sheplu](https://github.com/sheplu) - Jean Burellier
- [@wesleytodd](https://github.com/wesleytodd) - Wes Todd
- [@jonchurch](https://github.com/jonchurch) - Jon Church
- [@ctcpip](https://github.com/ctcpip/) - Chris de Almeida

**Inativo:**

- [@dougwilson](https://github.com/dougwilson) - Douglas Wilson
- [@hacksparrow](https://github.com/hacksparrow) - Hage Yaapa
- [@jonathanong](https://github.com/jonathanong) - jongleberry
- [@niftylettuce](https://github.com/niftylettuce) - niftylettuce
- [@troygoode](https://github.com/troygoode) - Troy Goode

## Express é feito de vários módulos

Nossa vibrante comunidade criou uma grande variedade de extensões,
[middleware módulos](https://expressjs.com/pt-br/resources/middleware.html) e frameworks de alto nível.

Além disso, a comunidade Express mantém módulos nestes duas organizações no GitHub:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/pt-br/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

Para acompanhar o que está acontecendo em toda a comunidade, Confira a [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## Questões

Se você se deparou com o que acha que é um bug ou apenas deseja fazer
uma solicitação de recurso abre um ticket no [issue queue](https://github.com/expressjs/express/issues).

## Exemplos

Veja dezenas de aplicativos Express [exemplos](https://github.com/expressjs/express/tree/master/examples)
no repositório temos de tudo, desde design de API e autenticação até integração de mecanismo de template.

## Discussões no GitHub

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Marca do Expres.js

## Logo Express.js

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotipo

### Logomarca

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/resources/community.md          )
