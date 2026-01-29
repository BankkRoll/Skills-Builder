# Express examples and more

# Express examples

> Explore uma coleção de exemplos de aplicações em Express.js cobrindo diversos casos de uso, integrações e configurações avançadas para te ajudar a aprender e construir seus projetos.

# Express examples

This page contains list of examples using Express.

- [auth](https://github.com/expressjs/express/tree/master/examples/auth) - Authentication with login and password
- [content-negotiation](https://github.com/expressjs/express/tree/master/examples/content-negotiation) - HTTP content negotiation
- [cookie-sessions](https://github.com/expressjs/express/tree/master/examples/cookie-sessions) - Working with cookie-based sessions
- [cookies](https://github.com/expressjs/express/tree/master/examples/cookies) - Working with cookies
- [downloads](https://github.com/expressjs/express/tree/master/examples/downloads) - Transferring files to client
- [ejs](https://github.com/expressjs/express/tree/master/examples/ejs) - Working with Embedded JavaScript templating (ejs)
- [error-pages](https://github.com/expressjs/express/tree/master/examples/error-pages) - Creating error pages
- [error](https://github.com/expressjs/express/tree/master/examples/error) - Working with error middleware
- [hello-world](https://github.com/expressjs/express/tree/master/examples/hello-world) - Simple request handler
- [markdown](https://github.com/expressjs/express/tree/master/examples/markdown) - Markdown as template engine
- [multi-router](https://github.com/expressjs/express/tree/master/examples/multi-router) - Working with multiple Express routers
- [mvc](https://github.com/expressjs/express/tree/master/examples/mvc) - MVC-style controllers
- [online](https://github.com/expressjs/express/tree/master/examples/online) - Tracking online user activity with `online` and `redis` packages
- [params](https://github.com/expressjs/express/tree/master/examples/params) - Working with route parameters
- [resource](https://github.com/expressjs/express/tree/master/examples/resource) - Multiple HTTP operations on the same resource
- [route-map](https://github.com/expressjs/express/tree/master/examples/route-map) - Organizing routes using a map
- [route-middleware](https://github.com/expressjs/express/tree/master/examples/route-middleware) - Working with route middleware
- [route-separation](https://github.com/expressjs/express/tree/master/examples/route-separation) - Organizing routes per each resource
- [search](https://github.com/expressjs/express/tree/master/examples/search) - Search API
- [session](https://github.com/expressjs/express/tree/master/examples/session) - User sessions
- [static-files](https://github.com/expressjs/express/tree/master/examples/static-files) - Serving static files
- [vhost](https://github.com/expressjs/express/tree/master/examples/vhost) - Working with virtual hosts
- [view-constructor](https://github.com/expressjs/express/tree/master/examples/view-constructor) - Rendering views dynamically
- [view-locals](https://github.com/expressjs/express/tree/master/examples/view-locals) - Saving data in request object between middleware calls
- [web-service](https://github.com/expressjs/express/tree/master/examples/web-service) - Simple API service

## Exemplos adicionais

Estes são alguns exemplos adicionais com integrações mais extensas.

Atenção

Esta informação refere-se a sites de terceiros, produtos ou módulos que não são mantidos pela equipe do Expressjs. A listagem aqui não constitui um endosso ou recomendação da equipe de projeto Expressjs.

- [prisma-fullstack](https://github.com/prisma/prisma-examples/tree/latest/pulse/fullstack-simple-chat) - Aplicativo Fullstack com Express e Next.js utilizando [Prisma](https://www.npmjs.com/package/prisma) como ORM
- [prisma-rest-api-ts](https://github.com/prisma/prisma-examples/tree/latest/orm/express) - API REST com Express em TypeScript utilizando [Prisma](https://www.npmjs.com/package/prisma) como ORM

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/examples.md          )

---

# Perguntas mais frequentes

> Find answers to frequently asked questions about Express.js, including topics on application structure, models, authentication, template engines, error handling, and more.

# Perguntas mais frequentes

## Como eu devo estruturar meu aplicativo?

Não existe uma resposta definitiva para esta questão. A
resposta depende da escala do seu aplicativo e o time que está
envolvido. Para ser o mais flexível possível, o Express não faz
suposições em termos de estrutura.

Rotas e outras lógicas específicas do aplicativo podem ficar em
quantos arquivos quiser, em qualquer estrutura de diretórios que
preferir. Visualize os seguintes exemplos para obter inspiração:

- [Listagens de rota](https://github.com/expressjs/express/blob/4.13.1/examples/route-separation/index.js#L32-47)
- [Mapa de rota](https://github.com/expressjs/express/blob/4.13.1/examples/route-map/index.js#L52-L66)
- [Controladores com estilo MVC](https://github.com/expressjs/express/tree/master/examples/mvc)

Além disso, existem extensões de terceiros para o Express, que
simplificam alguns desses padrões:

- [Resourceful routing](https://github.com/expressjs/express-resource)

## Como eu defino modelos?

O Express não tem noção de banco de dados. Este conceito é
deixado para módulos do Node de terceiros, permitindo que você faça
a interface com praticamente qualquer banco de dados.

Consulte [LoopBack](http://loopback.io) para
uma estrutura baseada no Express que é centrada em modelos.

## Como posso autenticar usuários?

Autenticação é outra área muito opinada que o Express não
se arrisca a entrar. Você pode usar qualquer esquema que desejar.
Para um esquema simples com nome de usuário / senha, consulte
este
exemplo.

## Quais mecanismos de modelo o Express suporta?

O Express suporta qualquer mecanismo de modelo que esteja em
conformidade com a assinatura `(path, locals,
callback)`.
Para normalizar interfaces e o armazenamento em
cache de mecanismo de modelo, consulte o projeto
[consolidate.js](https://github.com/visionmedia/consolidate.js)
para obter suporte. Mecanismos de modelo não listados podem ainda
assim suportar a assinatura do Express.

[Roteamento engenhoso](https://github.com/expressjs/express-resource)

## Como manipulo respostas 404?

No Express, respostas 404 não são o resultado de um erro,
portanto o middleware manipulador de erros não irá capturá-las. Este comportamento é porque uma resposta 404 simplesmente indicam a
ausência de trabalho adicional para fazer; em outras palavras, o
Express executou todas as funções de middleware e rotas, e descobriu
que nenhuma delas respondeu. Tudo que você precisa fazer é incluir
uma função de middleware no final da pilha (abaixo de todas as outras
funções) para manipular uma resposta 404:

```
app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})
```

Add routes dynamically at runtime on an instance of `express.Router()`
so the routes are not superseded by a middleware function.

## Como configuro um manipulador de erros?

Você define middlewares de manipulação de erros da mesma forma
que outros middlewares, exceto que com quatro argumentos ao invés de
três; especificamente com a assinatura `(err, req, res, next)`:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Para obter mais informações, consulte [Manipulação de erros](https://expressjs.com/pt-br/guide/error-handling.html).

## Como renderizar um HTML simples?

Você não faz! Não há necessidade de se “renderizar” HTML com a
função `res.render()`.
se você tiver um arquivo
específico, use a função `res.sendFile()`.
Se estiver entregando muitos ativos a partir de um diretório, use a
função de middleware `express.static()`.

## What version of Node.js does Express require?

- [Express 4.x](https://expressjs.com/pt-br/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/pt-br/5x/api.html) requires Node.js 18 or higher.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/faq.md          )

---

# Gerador de aplicativos do Express

> Learn how to use the Express application generator tool to quickly create a skeleton for your Express.js applications, streamlining setup and configuration.

# Gerador de aplicativos do Express

Use a ferramenta geradora de aplicativos, `express`,
para rapidamente criar uma estrutura básica de aplicativo.

You can run the application generator with the `npx` command (available in Node.js 8.2.0).

```
$ npx express-generator
```

For earlier Node versions, install the application generator as a global npm package and then launch it:

```
$ npm install -g express-generator
$ express
```

Exiba as opções de comando com a opção `-h`:

```
$ express -h

  Usage: express [options] [dir]

  Options:

    -h, --help          output usage information
        --version       output the version number
    -e, --ejs           add ejs engine support
        --hbs           add handlebars engine support
        --pug           add pug engine support
    -H, --hogan         add hogan.js engine support
        --no-view       generate without view engine
    -v, --view <engine> add view <engine> support (ejs|hbs|hjs|jade|pug|twig|vash) (defaults to jade)
    -c, --css <engine>  add stylesheet <engine> support (less|stylus|compass|sass) (defaults to plain css)
        --git           add .gitignore
    -f, --force         force on non-empty directory
```

Por exemplo, o seguinte cria um aplicativo do Express chamado *myapp*
no diretório atualmente em funcionamento: The app will be created in a folder named *myapp* in the current working directory and the view engine will be set to [Pug](https://pugjs.org/):

```
$ express --view=pug myapp

   create : myapp
   create : myapp/package.json
   create : myapp/app.js
   create : myapp/public
   create : myapp/public/javascripts
   create : myapp/public/images
   create : myapp/routes
   create : myapp/routes/index.js
   create : myapp/routes/users.js
   create : myapp/public/stylesheets
   create : myapp/public/stylesheets/style.css
   create : myapp/views
   create : myapp/views/index.pug
   create : myapp/views/layout.pug
   create : myapp/views/error.pug
   create : myapp/bin
   create : myapp/bin/www
```

Em seguida instale as dependências:

```
$ cd myapp
$ npm install
```

No MacOS ou Linux, execute o aplicativo com este comando:

```
$ DEBUG=myapp:* npm start
```

No Windows, use este comando:

```
> set DEBUG=myapp:* & npm start
```

Instale o `express` com o comando a seguir:

```
PS> $env:DEBUG='myapp:*'; npm start
```

Em seguida carregue `http://localhost:3000/` no seu navegador para acessar o aplicativo.

O aplicativo gerado possui a seguinte estrutura de diretórios:

```
.
├── app.js
├── bin
│   └── www
├── package.json
├── public
│   ├── images
│   ├── javascripts
│   └── stylesheets
│       └── style.css
├── routes
│   ├── index.js
│   └── users.js
└── views
    ├── error.pug
    ├── index.pug
    └── layout.pug

7 directories, 9 files
```

A estrutura de aplicativo criada pelo gerador é apenas uma das várias maneiras de estruturar aplicativos do Express. É possível utilizar esta estrutura ou modificá-la para melhor se adequar às suas necessidades.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/generator.md          )

---

# Exemplo Hello World

> Get started with Express.js by building a simple 'Hello World' application, demonstrating the basic setup and server creation for beginners.

# Exemplo Hello World

Este é essencialmente o aplicativo mais simples do Express que é possível criar. Ele
é um aplicativo de arquivo único — *não* é o que você iria obter usando o [Gerador Express](https://expressjs.com/pt-br/starter/generator.html),
que cria a estrutura para um aplicativo completo com inúmeros arquivos JavaScript, modelos Jade, e subdiretórios para vários
propósitos.

```
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
```

O aplicativo inicia um servidor e escuta a porta 3000 por
conexões. O aplicativo responde com “Hello World!” à solicitações
para a URL raiz (`/`) ou *rota*. Para
todos os outros caminhos, ele irá responder com um **404 Não Encontrado**.

### Running Locally

Primeiro crie um diretório chamado `myapp`,
mude para ele e execute o `npm init`. Em seguida
instale o `express` como uma dependência, de acordo com o [guia de instalação](https://expressjs.com/pt-br/starter/installing.html).

No diretório `myapp`, crie um arquivo chamado `app.js` e inclua o seguinte código:

O `req` (solicitação) e `res`
(resposta) são os mesmos objetos que o Node fornece, para que seja
possível chamar o `req.pipe()`,
`req.on('data', callback)`, e qualquer outra coisa
que desejaria fazer sem o envolvimento do Express.

Execute o aplicativo com o seguinte comando:

```
$ node app.js
```

Em seguida, carregue [http://localhost:3000/](http://localhost:3000/) em
um navegador para visualizar a saída

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/hello-world.md          )

---

# Instalação

> Learn how to install Express.js in your Node.js environment, including setting up your project directory and managing dependencies with npm.

# Instalação

Assumindo que já tenha instalado o [Node.js](https://nodejs.org/), crie um diretório
para conter o seu aplicativo, e torne-o seu diretório ativo.

- [Express 4.x](https://expressjs.com/pt-br/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/pt-br/5x/api.html) requires Node.js 18 or higher.

```
$ mkdir myapp
$ cd myapp
```

Use o comando `npm init` para criar um arquivo `package.json` para o seu aplicativo.
Para obter mais informações sobre como o `package.json` funciona,
consulte [Detalhes do tratamento de package.json do npm](https://docs.npmjs.com/files/package.json).

```
$ npm init
```

Este comando solicita por várias coisas, como o nome e versão do seu aplicativo.
Por enquanto, é possível simplesmente pressionar RETURN para aceitar
os padrões para a maioria deles, com as seguintes exceções:

```
entry point: (index.js)
```

Insira `app.js`, ou qualquer nome que deseje
para o arquivo principal. Se desejar que seja `index.js`, pressione RETURN para aceitar o nome de
arquivo padrão sugerido.

Agora instale o Express no diretório `myapp`
e salve-o na lista de dependências. Por exemplo:

```
$ npm install express
```

Para instalar o Express temporariamente não o inclua na lista
de dependências, omita a opção `--save`:

```
$ npm install express --no-save
```

Módulos do Node instalados com a opção `--save`
são incluídas na lista `dependencies` no arquivo
`package.json`. Posteriormente, executando `npm install` no diretório
`app` irá automaticamente instalar os módulos na
lista de dependências.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/installing.md          )

---

# Entregando arquivos estáticos no Express

> Understand how to serve static files like images, CSS, and JavaScript in Express.js applications using the built-in 'static' middleware.

# Entregando arquivos estáticos no Express

Para entregar arquivos estáticos como imagens, arquivos CSS, e
arquivos JavaScript, use a função de middleware `express.static`
integrada no Express.

The function signature is:

```
express.static(root, [options])
```

The `root` argument specifies the root directory from which to serve static assets.
For more information on the `options` argument, see [express.static](https://expressjs.com/pt-br/5x/api.html#express.static).

Por exemplo, use o código a seguir
para entregar imagens, arquivos CSS, e arquivos JavaScript em um
diretório chamado `public`:

```
app.use(express.static('public'))
```

Agora, é possível carregar os arquivos que estão no diretório `public`:

```
http://localhost:3000/images/kitten.jpg
http://localhost:3000/css/style.css
http://localhost:3000/js/app.js
http://localhost:3000/images/bg.png
http://localhost:3000/hello.html
```

O Express consulta os arquivos em relação ao diretório estático, para
que o nome do diretório estático não faça parte da URL.

Para usar vários diretórios de ativos estáticos, chame a função
de middleware `express.static` várias vezes:

```
app.use(express.static('public'))
app.use(express.static('files'))
```

O Express consulta os arquivos na ordem em que você configurar
os diretórios estáticos com a função de middleware
`express.static`.

Observação

For best results, [use a reverse proxy](https://expressjs.com/pt-br/advanced/best-practice-performance.html#use-a-reverse-proxy) cache to improve performance of serving static assets.

To create a virtual path prefix (where the path does not actually exist in the file system) for files that are served by the `express.static` function, [specify a mount path](https://expressjs.com/pt-br/5x/api.html#app.use) for the static directory, as shown below:

```
app.use('/static', express.static('public'))
```

Agora, é possível carregar os arquivos que estão no diretório
`public` a partir do prefixo do caminho `/static`.

```
http://localhost:3000/static/images/kitten.jpg
http://localhost:3000/static/css/style.css
http://localhost:3000/static/js/app.js
http://localhost:3000/static/images/bg.png
http://localhost:3000/static/hello.html
```

Entretanto, o caminho fornecido para a função
`express.static` é relativa ao diretório a partir do
qual você inicia o seu `node` de processo. Se você
executar o aplicativo express a partir de outro diretório, é mais
seguro utilizar o caminho absoluto do diretório para o qual deseja
entregar.

```
const path = require('path')
app.use('/static', express.static(path.join(__dirname, 'public')))
```

For more details about the `serve-static` function and its options, see  [serve-static](https://expressjs.com/resources/middleware/serve-static.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/starter/static-files.md          )

---

# Suporte à Versão

> Encontre informações sobre o cronograma de suporte para diferentes versões do Express.js, incluindo quais versões são atualmente mantidas e antigas políticas.

# Suporte à Versão

Somente a última versão de qualquer linha de lançamento é suportada.

Versões que são EOL (fim de vida) podem receber atualizações de vulnerabilidades de segurança críticas, mas a equipe Express não oferece garantia e não planeja endereçar ou liberar correções para quaisquer problemas encontrados.

| Versão Principal | Versão mínima do Node.js | Início Suporte | Término Suporte |
| --- | --- | --- | --- |
| v5.x | 18 | Setembro de 2024 | ongoing |
| v4.x | 0.10.0 | Abril de 2014 | ongoing |
| v3.x | 0.8.0 | Outubro de 2012 | Julho de 2015 |
| v2.x | 0.4.1 | Março de 2011 | Julho de 2012 |
| v1.x | 0.2.0 | Dezembro de 2010 | Março de 2011 |
| v0.14.x | 0.1.98 | Dezembro de 2010 | Dezembro de 2010 |

## Opções de Suporte Comercial

Se você não puder atualizar para uma versão suportada do Express, entre em contato com um de nossos parceiros para receber atualizações de segurança:

- [HeroDevs Never-Ending Support](http://www.herodevs.com/support/express-nes?utm_source=expressjs&utm_medium=link&utm_campaign=express_eol_page)

 [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/support/index.md          )
