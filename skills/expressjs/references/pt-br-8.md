# Migrando para o Express 5 and more

# Migrando para o Express 5

> A comprehensive guide to migrating your Express.js applications from version 4 to 5, detailing breaking changes, deprecated methods, and new improvements.

# Migrando para o Express 5

## Visão Geral

O Express 5 não é muito diferente do Express 4: As mudanças na
API não são tão significantes quanto as do 3.0 para o 4.0. Apesar de
a API básica permanecer a mesma, ainda existem mudanças disruptivas;
em outras palavras um programa do Express 4 existente pode não
funcionar se você atualizá-lo para usar o Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```
npm install "express@5"
```

É possível em seguida executar seus testes automatizados para
verificar o que falha, e corrigir os problemas de acordo com as
atualizações abaixo. Após endereçar as falhas nos testes, execute o
seu aplicativo para verificar quais erros ocorrem. Você descobrirá
imediatamente se o aplicativo utiliza quaisquer métodos ou
propriedades que não são suportados.

## Express 5 Codemods

To help you migrate your express server, we have created a set of codemods that will help you automatically update your code to the latest version of Express.

Run the following command for run all the codemods available:

```
npx codemod@latest @expressjs/v5-migration-recipe
```

If you want to run a specific codemod, you can run the following command:

```
npx codemod@latest @expressjs/name-of-the-codemod
```

You can find the list of available codemods [here](https://codemod.link/express).

## Mudanças no Express 5

**Métodos e propriedades removidas**

- [app.del()](#app.del)
- [app.param(fn)](#app.param)
- [Nomes de métodos pluralizados](#plural)
- [Vírgula no início no argumento nome para o  app.param(name, fn)](#leading)
- [req.param(name)](#req.param)
- [res.json(obj, status)](#res.json)
- [res.jsonp(obj, status)](#res.jsonp)
- [res.redirect('back') and res.location('back')](#magic-redirect)
- [res.redirect(url, status)](#res.redirect)
- [res.send(body, status)](#res.send.body)
- [res.send(status)](#res.send.status)
- [res.sendfile()](#res.sendfile)
- [router.param(fn)](#router.param)
- [express.static.mime](#express.static.mime)
- [express:router debug logs](#express:router-debug-logs)

**Melhorias**

- [Rota correspondente à sintaxe](#path-syntax)
- [Rejected promises handled from middleware and handlers](#rejected-promises)
- [express.urlencoded](#express.urlencoded)
- [express.static dotfiles](#express.static.dotfiles)
- [app.listen](#app.listen)
- [app.router](#app.router)
- [req.body](#req.body)
- [req.host](#req.host)
- [req.params](#req.params)
- [req.query](#req.query)
- [res.clearCookie](#res.clearCookie)
- [res.status](#res.status)
- [res.vary](#res.vary)

**Mudadas**

- [res.render()](#res.render)
- [Brotli encoding support](#brotli-support)

## Métodos e propriedades removidas

Se estiver usando qualquer um desses métodos ou propriedades
no seu aplicativo, ele irá quebrar. Portanto, será necessário alterar
o seu aplicativo após fazer a atualização para a versão 5.

### app.del()

O Express 5 não suporta mais a função `app.del()`. Se
você usas esta função um erro será lançado. Para registrar rotas HTTP DELETE, use a função `app.delete()` ao invés disso.

Inicialmente `del` era usada ao invés de
`delete`, porque `delete` é uma
palavra-chave reservada no JavaScript. Entretanto, a partir do ECMAScript 6,
`delete` e outras palavras-chave reservadas podem
legalmente ser usadas como nomes de propriedades.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/route-del-to-delete
```

```
// v4
app.del('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})

// v5
app.delete('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})
```

### app.param(fn)

A assinatura `app.param(fn)` foi usada para
modificar o comportamento da função `app.param(name, fn)`. Ela
foi descontinuada desde a v4.11.0, e o Express 5 não a suporta mais de nenhuma forma.

### Nomes de métodos pluralizados

Os seguintes nomes de métodos podem ser pluralizados. No
Express 4, o uso dos métodos antigos resultava em um aviso de
descontinuação.  O Express 5 não os suporta mais de forma nenhuma: Express 5 no longer supports them at all:

`req.acceptsLanguage()` é substituído por `req.acceptsLanguages()`.

`req.acceptsCharset()` é substituído por `req.acceptsCharsets()`.

`req.acceptsEncoding()` é substituído por `req.acceptsEncodings()`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/pluralize-method-names
```

```
// v4
app.all('/', (req, res) => {
  req.acceptsCharset('utf-8')
  req.acceptsEncoding('br')
  req.acceptsLanguage('en')

  // ...
})

// v5
app.all('/', (req, res) => {
  req.acceptsCharsets('utf-8')
  req.acceptsEncodings('br')
  req.acceptsLanguages('en')

  // ...
})
```

### Dois pontos no começo (:) do nome do app.param(name, fn)

Um caractere de dois pontos (:) no início do nome para a função
`app.param(name, fn)` é um remanescente do Express
3, e para fins de compatibilidade com versões anteriores, o Express 4
suportava-o com um aviso de descontinuação. O Express 5 irá
silenciosamente ignorá-lo e usar o nome do parâmetro sem prefixá-lo
com os dois pontos.

Isso não deve afetar o seu código se você seguiu a documentação
do Express 4 do [app.param](https://expressjs.com/pt-br/4x/api.html#app.param), já que ela não
menciona os dois pontos no início.

### req.param(name)

Este é um método potencialmente confuso e perigoso de recuperação de dados de formulário foi removido. Você precisará agora especificamente olhar para o nome do parâmetro enviado no objeto `req.params`,
`req.body`, ou `req.query`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/explicit-request-params
```

```
// v4
app.post('/user', (req, res) => {
  const id = req.param('id')
  const body = req.param('body')
  const query = req.param('query')

  // ...
})

// v5
app.post('/user', (req, res) => {
  const id = req.params.id
  const body = req.body
  const query = req.query

  // ...
})
```

### res.json(obj, status)

O Express 5 não suporta mais a assinatura `res.json(obj, status)`. Ao
invés disso, configure o status e então encadeie-o ao método `res.json()` assim:
`res.status(status).json(obj)`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.post('/user', (req, res) => {
  res.json({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).json({ name: 'Ruben' })
})
```

### res.jsonp(obj, status)

O Express 5 não suporta mais a assinatura `res.jsonp(obj, status)`. Ao invés disso, configure o status e então encadeie-o ao método
`res.jsonp()` assim: `res.status(status).jsonp(obj)`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.post('/user', (req, res) => {
  res.jsonp({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).jsonp({ name: 'Ruben' })
})
```

### res.redirect(url, status)

O Express 5 não suporta mais a assinatura `res.send(obj, status)`. Ao invés disso, configure o status e então encadeie-o ao método
`res.send()` assim: `res.status(status).send(obj)`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/redirect-arg-order
```

```
// v4
app.get('/user', (req, res) => {
  res.redirect('/users', 301)
})

// v5
app.get('/user', (req, res) => {
  res.redirect(301, '/users')
})
```

### res.redirect('back') and res.location('back')

Express 5 no longer supports the magic string `back` in the `res.redirect()` and `res.location()` methods. Instead, use the `req.get('Referrer') || '/'` value to redirect back to the previous page. In Express 4, the `res.redirect('back')` and `res.location('back')` methods were deprecated.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/back-redirect-deprecated
```

```
// v4
app.get('/user', (req, res) => {
  res.redirect('back')
})

// v5
app.get('/user', (req, res) => {
  res.redirect(req.get('Referrer') || '/')
})
```

### res.send(body, status)

Express 5 no longer supports the signature `res.send(obj, status)`. Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.get('/user', (req, res) => {
  res.send({ name: 'Ruben' }, 200)
})

// v5
app.get('/user', (req, res) => {
  res.status(200).send({ name: 'Ruben' })
})
```

### res.send(status)

O Express 5 não suporta mais a assinatura `res.send(status)`, onde *status*
é um número. Ao invés disso, use a função
`res.sendStatus(statusCode)`, que configura o código
do status do cabeçalho de resposta HTTP  e envia a versão de texto do
código: “Não Encontrado”, “Erro Interno de Servidor”, e assim por
diante.
Se precisar enviar um número usando a função
`res.send()`, coloque o número entre aspas para
converte-lo para um sequência de caracteres, para que o Express não o
interprete como uma tentativa de usar a assinatura antiga não
suportada.

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```

```
// v4
app.get('/user', (req, res) => {
  res.send(200)
})

// v5
app.get('/user', (req, res) => {
  res.sendStatus(200)
})
```

### res.sendfile()

A função `res.sendfile()` foi substituída pela
versão em formato camel-case `res.sendFile()` no
Express 5.

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now “text/javascript” instead of “application/javascript”
- JSON files (.json): now “application/json” instead of “text/json”
- CSS files (.css): now “text/css” instead of “text/plain”
- XML files (.xml): now “application/xml” instead of “text/xml”
- Font files (.woff): now “font/woff” instead of “application/font-woff”
- SVG files (.svg): now “image/svg+xml” instead of “application/svg+xml”

Observação

You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/camelcase-sendfile
```

```
// v4
app.get('/user', (req, res) => {
  res.sendfile('/path/to/file')
})

// v5
app.get('/user', (req, res) => {
  res.sendFile('/path/to/file')
})
```

### router.param(fn)

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. Ela
foi descontinuada desde a v4.11.0, e o Express 5 não a suporta mais de nenhuma forma.

### express.static.mime

In Express 5, `mime` is no longer an exported property of the `static` field.
Use the [mime-typespackage](https://github.com/jshttp/mime-types) to work with MIME type values.

**Important:** This change affects not only direct usage of `express.static.mime` but also other Express methods that rely on MIME type detection, such as `res.sendFile()`. The following MIME types have changed from Express 4:

- JavaScript files (.js): now served as “text/javascript” instead of “application/javascript”
- JSON files (.json): now served as “application/json” instead of “text/json”
- CSS files (.css): now served as “text/css” instead of “text/plain”
- HTML files (.html): now served as “text/html; charset=utf-8” instead of just “text/html”
- XML files (.xml): now served as “application/xml” instead of “text/xml”
- Font files (.woff): now served as “font/woff” instead of “application/font-woff”

```
// v4
express.static.mime.lookup('json')

// v5
const mime = require('mime-types')
mime.lookup('json')
```

### express:router debug logs

In Express 5, router handling logic is performed by a dependency. Therefore, the
debug logs for the router are no longer available under the `express:` namespace.
In v4, the logs were available under the namespaces `express:router`, `express:router:layer`,
and `express:router:route`. All of these were included under the namespace `express:*`.
In v5.1+, the logs are available under the namespaces `router`, `router:layer`, and `router:route`.
The logs from `router:layer` and `router:route` are included in the namespace `router:*`.
To achieve the same detail of debug logging when using `express:*` in v4, use a conjunction of
`express:*`, `router`, and `router:*`.

```
# v4
DEBUG=express:* node index.js

# v5
DEBUG=express:*,router,router:* node index.js
```

## Mudadas

### Path route matching syntax

Path route matching syntax is when a string is supplied as the first parameter to the `app.all()`, `app.use()`, `app.METHOD()`, `router.all()`, `router.METHOD()`, and `router.use()` APIs. The following changes have been made to how the path string is matched to an incoming request:

- The wildcard `*` must have a name, matching the behavior of parameters `:`, use `/*splat` instead of `/*`

```
// v4
app.get('/*', async (req, res) => {
  res.send('ok')
})

// v5
app.get('/*splat', async (req, res) => {
  res.send('ok')
})
```

Observação

`*splat` matches any path without the root path. If you need to match the root path as well `/`, you can use `/{*splat}`, wrapping the wildcard in braces.

```
// v5
app.get('/{*splat}', async (req, res) => {
  res.send('ok')
})
```

- The optional character `?` is no longer supported, use braces instead.

```
// v4
app.get('/:file.:ext?', async (req, res) => {
  res.send('ok')
})

// v5
app.get('/:file{.:ext}', async (req, res) => {
  res.send('ok')
})
```

- Regexp characters are not supported. Por exemplo:

```
app.get('/[discussion|page]/:slug', async (req, res) => {
  res.status(200).send('ok')
})
```

should be changed to:

```
app.get(['/discussion/:slug', '/page/:slug'], async (req, res) => {
  res.status(200).send('ok')
})
```

- Some characters have been reserved to avoid confusion during upgrade (`()[]?+!`), use `\` to escape them.
- Parameter names now support valid JavaScript identifiers, or quoted like `:"this"`.

### Rejected promises handled from middleware and handlers

Request middleware and handlers that return rejected promises are now handled by forwarding the rejected value as an `Error` to the error handling middleware. This means that using `async` functions as middleware and handlers are easier than ever. When an error is thrown in an `async` function or a rejected promise is `await`ed inside an async function, those errors will be passed to the error handler as if calling `next(err)`.

Details of how Express handles errors is covered in the [error handling documentation](https://expressjs.com/en/guide/error-handling.html).

### express.urlencoded

The `express.urlencoded` method makes the `extended` option `false` by default.

### express.static dotfiles

In Express 5, the `express.static` middleware’s `dotfiles` option now defaults to `"ignore"`. This is a change from Express 4, where dotfiles were served by default. As a result, files inside a directory that starts with a dot (`.`), such as `.well-known`, will no longer be accessible and will return a **404 Not Found** error. This can break functionality that depends on serving dot-directories, such as Android App Links, and Apple Universal Links.

Example of breaking code:

```
// v4
app.use(express.static('public'))
```

After migrating to Express 5, a request to `/.well-known/assetlinks.json` will result in a **404 Not Found**.

To fix this, serve specific dot-directories explicitly using the `dotfiles: "allow"` option:

```
// v5
app.use('/.well-known', express.static('public/.well-known', { dotfiles: 'allow' }))
app.use(express.static('public'))
```

This approach allows you to safely serve only the intended dot-directories while keeping the default secure behavior for other dotfiles, which remain inaccessible.

### app.listen

In Express 5, the `app.listen` method will invoke the user-provided callback function (if provided) when the server receives an error event. In Express 4, such errors would be thrown. This change shifts error-handling responsibility to the callback function in Express 5. If there is an error, it will be passed to the callback as an argument.
Por exemplo:

```
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`)
})
```

### app.router

O objeto `app.router`, que foi removido no
Express 4, está de volta no Express 5. Na nove versão, este objeto é
apenas uma referência para o roteador Express base, diferentemente do
Express 3, onde um aplicativo tinha que carregá-lo explicitamente.

### req.body

The `req.body` property returns `undefined` when the body has not been parsed. In Express 4, it returns `{}` by default.

### req.host

No Express 4, a função `req.host`
incorretamente removia o número da porta caso estivesse presente. No
Express 5 o número da porta é mantido.

### req.params

The `req.params` object now has a **null prototype** when using string paths. However, if the path is defined with a regular expression, `req.params` remains a standard object with a normal prototype. Additionally, there are two important behavioral changes:

**Wildcard parameters are now arrays:**

Wildcards (e.g., `/*splat`) capture path segments as an array instead of a single string.

```
app.get('/*splat', (req, res) => {
  // GET /foo/bar
  console.dir(req.params)
  // => [Object: null prototype] { splat: [ 'foo', 'bar' ] }
})
```

**Unmatched parameters are omitted:**

In Express 4, unmatched wildcards were empty strings (`''`) and optional `:` parameters (using `?`) had a key with value `undefined`. In Express 5, unmatched parameters are completely omitted from `req.params`.

```
// v4: unmatched wildcard is empty string
app.get('/*', (req, res) => {
  // GET /
  console.dir(req.params)
  // => { '0': '' }
})

// v4: unmatched optional param is undefined
app.get('/:file.:ext?', (req, res) => {
  // GET /image
  console.dir(req.params)
  // => { file: 'image', ext: undefined }
})

// v5: unmatched optional param is omitted
app.get('/:file{.:ext}', (req, res) => {
  // GET /image
  console.dir(req.params)
  // => [Object: null prototype] { file: 'image' }
})
```

### req.query

The `req.query` property is no longer a writable property and is instead a getter. The default query parser has been changed from “extended” to “simple”.

### res.clearCookie

The `res.clearCookie` method ignores the `maxAge` and `expires` options provided by the user.

### res.status

The `res.status` method only accepts integers in the range of `100` to `999`, following the behavior defined by Node.js, and it returns an error when the status code is not an integer.

### res.vary

The `res.vary` throws an error when the `field` argument is missing. In Express 4, if the argument was omitted, it gave a warning in the console

## Melhorias

### res.render()

Este método agora impinge comportamento assíncrono  para todos
os mecanismos de visualização, evitando erros causados pelos
mecanismos de visualização que tinham uma implementação síncrona e
que violavam a interface recomendada.

### Brotli encoding support

Express 5 supports Brotli encoding for requests received from clients that support it.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/migrating-5.md          )

---

# Overriding the Express API

> Discover how to customize and extend the Express.js API by overriding methods and properties on the request and response objects using prototypes.

# Overriding the Express API

The Express API consists of various methods and properties on the request and response objects. These are inherited by prototype. There are two extension points for the Express API:

1. The global prototypes at `express.request` and `express.response`.
2. App-specific prototypes at `app.request` and `app.response`.

Altering the global prototypes will affect all loaded Express apps in the same process. If desired, alterations can be made app-specific by only altering the app-specific prototypes after creating a new app.

## Methods

You can override the signature and behavior of existing methods with your own, by assigning a custom function.

Following is an example of overriding the behavior of [res.sendStatus](https://expressjs.com/4x/api.html#res.sendStatus).

```
app.response.sendStatus = function (statusCode, type, message) {
  // code is intentionally kept simple for demonstration purpose
  return this.contentType(type)
    .status(statusCode)
    .send(message)
}
```

The above implementation completely changes the original signature of `res.sendStatus`. It now accepts a status code, encoding type, and the message to be sent to the client.

The overridden method may now be used this way:

```
res.sendStatus(404, 'application/json', '{"error":"resource not found"}')
```

## Properties

Properties in the Express API are either:

1. Assigned properties (ex: `req.baseUrl`, `req.originalUrl`)
2. Defined as getters (ex: `req.secure`, `req.ip`)

Since properties under category 1 are dynamically assigned on the `request` and `response` objects in the context of the current request-response cycle, their behavior cannot be overridden.

Properties under category 2 can be overwritten using the Express API extensions API.

The following code rewrites how the value of `req.ip` is to be derived. Now, it simply returns the value of the `Client-IP` request header.

```
Object.defineProperty(app.request, 'ip', {
  configurable: true,
  enumerable: true,
  get () { return this.get('Client-IP') }
})
```

## Prototype

In order to provide the Express API, the request/response objects passed to Express (via `app(req, res)`, for example) need to inherit from the same prototype chain. By default, this is `http.IncomingRequest.prototype` for the request and `http.ServerResponse.prototype` for the response.

Unless necessary, it is recommended that this be done only at the application level, rather than globally. Also, take care that the prototype that is being used matches the functionality as closely as possible to the default prototypes.

```
// Use FakeRequest and FakeResponse in place of http.IncomingRequest and http.ServerResponse
// for the given app reference
Object.setPrototypeOf(Object.getPrototypeOf(app.request), FakeRequest.prototype)
Object.setPrototypeOf(Object.getPrototypeOf(app.response), FakeResponse.prototype)
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/overriding-express-api.md          )

---

# Roteamento

> Learn how to define and use routes in Express.js applications, including route methods, route paths, parameters, and using Router for modular routing.

# Roteamento

O *Roteamento* refere-se a como os *endpoints* de uma aplicação (URIs) respondem às requisições do cliente.
Para uma introdução ao roteamento, consulte [Roteamento básico](https://expressjs.com/pt-br/starter/basic-routing.html).

Rotas são definidas utilizando métodos do objeto `app` do Express que correspondem aos métodos HTTP;
por exemplo, `app.get()` para lidar com requisições GET e `app.post()` para requisições POST. Para a lista completa, veja [app.METHOD](https://expressjs.com/pt-br/4x/api.html#app.METHOD). Você também pode utilizar [app.all()](https://expressjs.com/pt-br/4x/api.html#app.all) para lidar com todos os métodos HTTP
e [app.use()](https://expressjs.com/pt-br/4x/api.html#app.use) para especificar middleware como funções *callback*
(Veja [Usando middlewares](https://expressjs.com/pt-br/guide/using-middleware.html) para mais detalhes).

Esses métodos de roteamento especificam uma função *callback* a ser chamada quando a aplicação
recebe uma requisição à rota e método HTTP especificados. Em outras palavras, a aplicação “escuta”
requisições que se encaixam nas rotas e métodos especificados e, quando há alguma correspondência,
chama a função *callback* especificada.

Na realidade, métodos de roteamento podem possuir mais de uma função *callback* como argumento.
Com múltiplas funções, é importante passar `next` como argumento da função e chamar `next()` para passar o controle para a próxima.

O código a seguir é um exemplo de uma rota muito básica.

```
const express = require('express')
const app = express()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  res.send('hello world')
})
```

## Métodos de roteamento

Um método de roteamento é derivado a partir de um dos métodos
HTTP, e é anexado a uma instância da classe `express`.

o código a seguir é um exemplo de rotas para a raiz do
aplicativo que estão definidas para os
métodos GET e POST.

```
// GET method route
app.get('/', (req, res) => {
  res.send('GET request to the homepage')
})

// POST method route
app.post('/', (req, res) => {
  res.send('POST request to the homepage')
})
```

O Express suporta métodos que correspondem a todos os métodos de requisição HTTP: `get`, `post`, etc.
Pra uma lista completa, veja [app.METHOD](https://expressjs.com/pt-br/4x/api.html#app.METHOD).

Existe um método de roteamento especial,
`app.all()`, que não é derivado de nenhum método
HTTP. Este método é usado para carregar funções de middleware em um
caminho para todos os métodos de solicitação. For example, the following handler is executed for requests to the route `"/secret"` whether using `GET`, `POST`, `PUT`, `DELETE`, or any other HTTP request method supported in the [http module](https://nodejs.org/api/http.html#http_http_methods).

```
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```

## Caminhos de rota

Caminhos de rota, em combinação com os métodos de solicitação,
definem os terminais em que as solicitações podem ser feitas. Caminhos
de rota podem ser sequências de caracteres, padrões de sequência, ou
expressões regulares.

Atenção

In express 5, the characters `?`, `+`, `*`, `[]`, and `()` are handled differently than in version 4, please review the [migration guide](https://expressjs.com/pt-br/guide/migrating-5.html#path-syntax) for more information.

Atenção

In express 4, regular expression characters such as `$` need to be escaped with a `\`.

Observação

Express uses [path-to-regexp](https://www.npmjs.com/package/path-to-regexp) for matching the route paths; see the path-to-regexp documentation for all the possibilities in defining route paths. O Express
Route Tester é uma ferramenta útil para testar rotas básicas do Express, apesar de não suportar a correspondência de padrões.

Atenção

Query strings are not part of the route path.

### Aqui estão alguns exemplos de caminhos de rota baseados em sequências de caracteres

Este caminho de rota irá corresponder a solicitações ao `/qualquer.texto`.

```
app.get('/', (req, res) => {
  res.send('root')
})
```

Este caminho de rota irá corresponder a solicitações ao `/ajuda`.

```
app.get('/about', (req, res) => {
  res.send('about')
})
```

Este caminho de rota corresponde a solicitações à rota raiz, `/`.

```
app.get('/random.text', (req, res) => {
  res.send('random.text')
})
```

### Aqui estão alguns exemplos de caminhos de rota baseados em padrões de sequência

Atenção

The string patterns in Express 5 no longer work. Please refer to the [migration guide](https://expressjs.com/pt-br/guide/migrating-5.html#path-syntax) for more information.

Este caminho de rota irá corresponder ao `/abe` e `/abcde`.

```
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

Este caminho de rota irá corresponder ao `abcd`, `abbcd`, `abbbcd`, e assim por diante.

```
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

Este caminho de rota irá corresponder ao `abcd`, `abxcd`, `abRANDOMcd`, `ab123cd`, e assim por diante.

```
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

Este caminho de rota irá corresponder ao `acd` e `abcd`.

```
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```

### Exemplos de caminhos de rota baseados em expressões regulares:

Este caminho de rota irá corresponder a qualquer coisa com um
“a” no nome.

```
app.get(/a/, (req, res) => {
  res.send('/a/')
})
```

Este caminho de rota irá corresponder a `butterfly` e
`dragonfly`, mas não a `butterflyman`,
`dragonfly man`, e assim por diante.

```
app.get(/.*fly$/, (req, res) => {
  res.send('/.*fly$/')
})
```

## Sequências de consulta não fazem parte dos caminhos de rota.

Route parameters are named URL segments that are used to capture the values specified at their position in the URL. The captured values are populated in the `req.params` object, with the name of the route parameter specified in the path as their respective keys.

```
Route path: /users/:userId/books/:bookId
Request URL: http://localhost:3000/users/34/books/8989
req.params: { "userId": "34", "bookId": "8989" }
```

To define routes with route parameters, simply specify the route parameters in the path of the route as shown below.

```
app.get('/users/:userId/books/:bookId', (req, res) => {
  res.send(req.params)
})
```

The name of route parameters must be made up of “word characters” ([A-Za-z0-9_]).

Since the hyphen (`-`) and the dot (`.`) are interpreted literally, they can be used along with route parameters for useful purposes.

```
Route path: /flights/:from-:to
Request URL: http://localhost:3000/flights/LAX-SFO
req.params: { "from": "LAX", "to": "SFO" }
```

```
Route path: /plantae/:genus.:species
Request URL: http://localhost:3000/plantae/Prunus.persica
req.params: { "genus": "Prunus", "species": "persica" }
```

Atenção

In express 5, Regexp characters are not supported in route paths, for more information please refer to the [migration guide](https://expressjs.com/pt-br/guide/migrating-5.html#path-syntax).

To have more control over the exact string that can be matched by a route parameter, you can append a regular expression in parentheses (`()`):

```
Route path: /user/:userId(\d+)
Request URL: http://localhost:3000/user/42
req.params: {"userId": "42"}
```

Atenção

Because the regular expression is usually part of a literal string, be sure to escape any `\` characters with an additional backslash, for example `\\d+`.

Atenção

In Express 4.x, [the*character in regular expressions is not interpreted in the usual way](https://github.com/expressjs/express/issues/2495). As a workaround, use `{0,}` instead of `*`. This will likely be fixed in Express 5.

## Manipuladores de rota

É possível fornecer várias funções *callback*
que se comportam como [middleware](https://expressjs.com/pt-br/guide/using-middleware.html) para
manipular uma solicitação. A única exceção é que estes *callbacks* podem chamar `next('route')` para efetuar um
bypass nos *callbacks* restantes. É possível usar
este mecanismo para impor pré-condições em uma rota, e em seguida
passar o controle para rotas subsequentes se não houveram razões para
continuar com a rota atual.

```
app.get('/user/:id', (req, res, next) => {
  if (req.params.id === '0') {
    return next('route')
  }
  res.send(`User ${req.params.id}`)
})

app.get('/user/:id', (req, res) => {
  res.send('Special handler for user ID 0')
})
```

In this example:

- `GET /user/5` → handled by first route → sends “User 5”
- `GET /user/0` → first route calls `next('route')`, skipping to the next matching `/user/:id` route

Manipuladores de rota podem estar na forma de uma função, uma
matriz de funções, ou combinações de ambas, como mostrado nos
seguintes exemplos.

Uma única função *callback* pode manipular uma rota. Por exemplo:

```
app.get('/example/a', (req, res) => {
  res.send('Hello from A!')
})
```

Mais de uma função *callback* pode manipular uma
rota (certifique-se de especificar o objeto `next`). Por exemplo:

```
app.get('/example/b', (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from B!')
})
```

Uma matriz de funções *callback* podem manipular uma
rota. Por exemplo:

```
const cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

const cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

const cb2 = function (req, res) {
  res.send('Hello from C!')
}

app.get('/example/c', [cb0, cb1, cb2])
```

Uma combinação de funções independentes e matrizes de funções
podem manipular uma rota. Por exemplo:

```
const cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

const cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

app.get('/example/d', [cb0, cb1], (req, res, next) => {
  console.log('the response will be sent by the next function ...')
  next()
}, (req, res) => {
  res.send('Hello from D!')
})
```

## Métodos de resposta

Os métodos do objeto de resposta (`res`) na
seguinte tabela  podem enviar uma resposta ao cliente, e finalizar o
ciclo solicitação-resposta. Se nenhum destes métodos forem chamados a
partir de um manipulador de rota, a solicitação do cliente será
deixada em suspenso.

| Método | Descrição |
| --- | --- |
| res.download() | Solicita que seja efetuado o download de um arquivo |
| res.end() | Termina o processo de resposta. |
| res.json() | Envia uma resposta JSON. |
| res.jsonp() | Envia uma resposta JSON com suporta ao JSONP. |
| res.redirect() | Redireciona uma solicitação. |
| res.render() | Renderiza um modelo de visualização. |
| res.send() | Envia uma resposta de vários tipos. |
| res.sendFile | Envia um arquivo como um fluxo de octeto. |
| res.sendStatus() | Configura o código do status de resposta e envia a sua representação em sequência de caracteres como o corpo de resposta. |

## app.route()

É possível criar manipuladores de rota encadeáveis para um caminho de rota usando o `app.route()`.
Como o caminho é especificado em uma localização única, criar rotas modulares é útil, já que reduz redundâncias e erros tipográficos. Para obter mais informações sobre rotas, consulte: [documentação do Router()](https://expressjs.com/pt-br/4x/api.html#router).

Aqui está um exemplo de manipuladores de rotas encadeáveis que são definidos usando `app.route()`.

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

## express.Router

Use a classe `express.Router` para criar
manipuladores de rota modulares e montáveis. Uma instância de
`Router` é um middleware e sistema de roteamento
completo; por essa razão, ela é frequentemente referida como um
“mini-aplicativo”

O seguinte exemplo cria um roteador como um módulo, carrega uma
função de middleware nele, define algumas rotas, e monta o módulo
router em um caminho no aplicativo principal.

Crie um arquivo de roteador com um arquivo chamado
`passaros.js` no diretório do aplicativo, com o
seguinte conteúdo:

```
const express = require('express')
const router = express.Router()

// middleware that is specific to this router
const timeLog = (req, res, next) => {
  console.log('Time: ', Date.now())
  next()
}
router.use(timeLog)

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
const birds = require('./birds')

// ...

app.use('/birds', birds)
```

O aplicativo será agora capaz de manipular solicitações aos
caminhos `/passaros` e `/passaros/ajuda`,
assim como chamar a função de middleware `timeLog` que
é específica para a rota.

But if the parent route `/birds` has path parameters, it will not be accessible by default from the sub-routes. To make it accessible, you will need to pass the `mergeParams` option to the Router constructor [reference](https://expressjs.com/pt-br/5x/api.html#app.use).

```
const router = express.Router({ mergeParams: true })
```

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/guide/routing.md          )
