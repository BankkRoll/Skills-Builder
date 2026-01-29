# Express examples and more

# Express examples

> Explore a collection of Express.js application examples covering various use cases, integrations, and advanced configurations to help you learn and build your projects.

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

## Additional examples

These are some additional examples with more extensive integrations.

Warning

This information refers to third-party sites, products, or modules that are not maintained by the Expressjs team. Listing here does not constitute an endorsement or recommendation from the Expressjs project team.

- [prisma-fullstack](https://github.com/prisma/prisma-examples/tree/latest/pulse/fullstack-simple-chat) - Fullstack app with Express and Next.js using [Prisma](https://www.npmjs.com/package/prisma) as an ORM
- [prisma-rest-api-ts](https://github.com/prisma/prisma-examples/tree/latest/orm/express) - REST API with Express in TypeScript using [Prisma](https://www.npmjs.com/package/prisma) as an ORM

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/examples.md          )

---

# 常見問題 (FAQ)

> Find answers to frequently asked questions about Express.js, including topics on application structure, models, authentication, template engines, error handling, and more.

# 常見問題 (FAQ)

## 我該如何建立我的應用程式結構？

There is no definitive answer to this question. The answer depends
on the scale of your application and the team that is involved. To be as
flexible as possible, Express makes no assumptions in terms of structure.

Routes and other application-specific logic can live in as many files
as you wish, in any directory structure you prefer. View the following
examples for inspiration:

- [路由清單](https://github.com/expressjs/express/blob/4.13.1/examples/route-separation/index.js#L32-47)
- [路由對映](https://github.com/expressjs/express/blob/4.13.1/examples/route-map/index.js#L52-L66)
- [MVC 樣式控制器](https://github.com/expressjs/express/tree/master/examples/mvc)

此外，Express 有一些協力廠商延伸，可簡化部分這些型樣：

- [express-resource 路由](https://github.com/expressjs/express-resource)

## 如何定義模型？

Express has no notion of a database. This concept is
left up to third-party Node modules, allowing you to
interface with nearly any database.

請參閱 [LoopBack](http://loopback.io)，取得以模組為中心的 Express 型架構。

## 如何鑑別使用者？

Authentication is another opinionated area that Express does not
venture into. You may use any authentication scheme you wish.
For a simple username / password scheme, see [this example](https://github.com/expressjs/express/tree/master/examples/auth).

## Express 支援哪些範本引擎？

Express 支援符合 `(path, locals, callback)` 簽章的任何範本引擎。若要使範本引擎介面和快取正規化，請參閱 [consolidate.js](https://github.com/visionmedia/consolidate.js) 專案，以取得支援。未列出的範本引擎可能仍支援 Express 簽章。
To normalize template engine interfaces and caching, see the
[consolidate.js](https://github.com/visionmedia/consolidate.js)
project for support. Unlisted template engines might still support the Express signature.

For more information, see [Using template engines with Express](https://expressjs.com/zh-tw/guide/using-template-engines.html).

## 如何處理 404 回應？

In Express, 404 responses are not the result of an error, so
the error-handler middleware will not capture them. This behavior is
because a 404 response simply indicates the absence of additional work to do;
in other words, Express has executed all middleware functions and routes,
and found that none of them responded. All you need to
do is add a middleware function at the very bottom of the stack (below all other functions)
to handle a 404 response:

```
app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})
```

Add routes dynamically at runtime on an instance of `express.Router()`
so the routes are not superseded by a middleware function.

## 如何設定錯誤處理程式？

錯誤處理中介軟體的定義方式，與其他中介軟體相同，差別在於引數是四個而非三個，具體來說，就是使用 `(err, req, res, next)` 簽章：

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

如需相關資訊，請參閱[錯誤處理](https://expressjs.com/zh-tw/guide/error-handling.html)。

## 如何呈現一般 HTML？

You don’t! 不需要！不需要用 `res.render()` 函數來「呈現」HTML。如果您有特定的檔案，請使用 `res.sendFile()` 函數。如果您會從目錄提供許多資產，請使用 `express.static()` 中介軟體函數。
If you have a specific file, use the `res.sendFile()` function.
If you are serving many assets from a directory, use the `express.static()`
middleware function.

## What version of Node.js does Express require?

- [Express 4.x](https://expressjs.com/zh-tw/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/zh-tw/5x/api.html) requires Node.js 18 or higher.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/faq.md          )

---

# Express 應用程式產生器

> Learn how to use the Express application generator tool to quickly create a skeleton for your Express.js applications, streamlining setup and configuration.

# Express 應用程式產生器

Use the application generator tool, `express-generator`, to quickly create an application skeleton.

You can run the application generator with the `npx` command (available in Node.js 8.2.0).

```
$ npx express-generator
```

For earlier Node versions, install the application generator as a global npm package and then launch it:

```
$ npm install -g express-generator
$ express
```

使用 `-h` 選項來顯示指令選項：

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

舉例來說，以下是在現行工作目錄中建立一個名為 *myapp* 的 Express 應用程式： The app will be created in a folder named *myapp* in the current working directory and the view engine will be set to [Pug](https://pugjs.org/):

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

然後安裝相依項目：

```
$ cd myapp
$ npm install
```

在 MacOS 或 Linux 中，使用下列指令來執行應用程式：

```
$ DEBUG=myapp:* npm start
```

在 Windows 中，使用下列指令：

```
> set DEBUG=myapp:* & npm start
```

On Windows PowerShell, use this command:

```
PS> $env:DEBUG='myapp:*'; npm start
```

Then, load `http://localhost:3000/` in your browser to access the app.

The generated app has the following directory structure:

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

The app structure created by the generator is just one of many ways to structure Express apps. Feel free to use this structure or modify it to best suit your needs.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/generator.md          )

---

# Hello world 範例

> Get started with Express.js by building a simple 'Hello World' application, demonstrating the basic setup and server creation for beginners.

# Hello world 範例

Embedded below is essentially the simplest Express app you can create.
本質上，這是您所能建立的最簡易 Express 應用程式。它是單一檔案應用程式 — 與您使用 [Express 產生器](https://expressjs.com/zh-tw/starter/generator.html)所產生的結果*不同*，Express 產生器會建立完整應用程式框架，其中含有眾多 JavaScript 檔案、Jade 範本，以及各種用途的子目錄。

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

This app starts a server and listens on port 3000 for connections. 應用程式會啟動伺服器，並在埠 3000 接聽連線。應用程式對指向根 URL (`/`) 或_路由_的要求，以 “Hello World!” 回應。對於其他每一個路徑，它的回應是 **404 找不到**。

### Running Locally

首先請建立一個名為 `myapp` 的目錄，切換至該目錄，並執行 `npm init`。然後按照[安裝手冊](https://expressjs.com/zh-tw/starter/installing.html)，將 `express` 安裝成一個相依關係。 Then, install `express` as a dependency, as per the [installation guide](https://expressjs.com/zh-tw/starter/installing.html).

在 `myapp` 目錄中，建立名為 `app.js` 的檔案，並新增下列程式碼：

`req`（要求）和 `res`（回應）與 Node 提供的物件完全相同，因此您可以呼叫 `req.pipe()`、`req.on('data', callback)`，以及任何您要執行的項目，而不需要 Express 涉及。

使用下列指令來執行應用程式：

```
$ node app.js
```

然後在瀏覽器中載入 [http://localhost:3000/](http://localhost:3000/)，以查看輸出。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/hello-world.md          )

---

# 安裝

> Learn how to install Express.js in your Node.js environment, including setting up your project directory and managing dependencies with npm.

# 安裝

假設您已安裝 [Node.js](https://nodejs.org/)，請建立目錄來保留您的應用程式，並使它成為您的工作目錄。

- [Express 4.x](https://expressjs.com/zh-tw/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/zh-tw/5x/api.html) requires Node.js 18 or higher.

```
$ mkdir myapp
$ cd myapp
```

Use the `npm init` command to create a `package.json` file for your application.
使用 `npm init` 指令，為您的應用程式建立 `package.json` 檔。如需 `package.json` 如何運作的相關資訊，請參閱 [Specifics of npm’s package.json handling](https://docs.npmjs.com/files/package.json)。

```
$ npm init
```

This command prompts you for a number of things, such as the name and version of your application.
For now, you can simply hit RETURN to accept the defaults for most of them, with the following exception:

```
entry point: (index.js)
```

輸入 `app.js`，或您所要的主要檔名稱。如果您希望其名稱是 `index.js`，請按 RETURN 鍵，接受建議的預設檔名。 If you want it to be `index.js`, hit RETURN to accept the suggested default file name.

現在，將 Express 安裝在 `myapp` 目錄中，並儲存在相依關係清單中。例如： For example:

```
$ npm install express
```

如果只想暫時安裝 Express，而不新增至相依關係清單，請省略 `--save` 選項：

```
$ npm install express --no-save
```

安裝 Node 模組時，如果指定了 `--save` 選項，則會將這些模組新增至 `package.json` 檔中的 `dependencies` 清單。之後，當您在 `app` 目錄中執行 `npm install` 時，就會自動安裝相依關係清單中的模組。
 Then, afterwards, running `npm install` in the app directory will automatically install modules in the dependencies list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/installing.md          )

---

# 在 Express 中提供靜態檔案

> Understand how to serve static files like images, CSS, and JavaScript in Express.js applications using the built-in 'static' middleware.

# 在 Express 中提供靜態檔案

To serve static files such as images, CSS files, and JavaScript files, use the `express.static` built-in middleware function in Express.

The function signature is:

```
express.static(root, [options])
```

The `root` argument specifies the root directory from which to serve static assets.
For more information on the `options` argument, see [express.static](https://expressjs.com/zh-tw/5x/api.html#express.static).

For example, use the following code to serve images, CSS files, and JavaScript files in a directory named `public`:

```
app.use(express.static('public'))
```

現在，您可以載入位於 `public` 目錄中的檔案：

```
http://localhost:3000/images/kitten.jpg
http://localhost:3000/css/style.css
http://localhost:3000/js/app.js
http://localhost:3000/images/bg.png
http://localhost:3000/hello.html
```

Express 會查閱靜態目錄的相對檔案，因此靜態目錄的名稱不是 URL 的一部分。

To use multiple static assets directories, call the `express.static` middleware function multiple times:

```
app.use(express.static('public'))
app.use(express.static('files'))
```

Express looks up the files in the order in which you set the static directories with the `express.static` middleware function.

Note

For best results, [use a reverse proxy](https://expressjs.com/zh-tw/advanced/best-practice-performance.html#use-a-reverse-proxy) cache to improve performance of serving static assets.

To create a virtual path prefix (where the path does not actually exist in the file system) for files that are served by the `express.static` function, [specify a mount path](https://expressjs.com/zh-tw/5x/api.html#app.use) for the static directory, as shown below:

```
app.use('/static', express.static('public'))
```

現在，您可以透過 `/static` 路徑字首，來載入 `public` 目錄中的檔案。

```
http://localhost:3000/static/images/kitten.jpg
http://localhost:3000/static/css/style.css
http://localhost:3000/static/js/app.js
http://localhost:3000/static/images/bg.png
http://localhost:3000/static/hello.html
```

不過，您提供給 `express.static` 函數的路徑，是相對於您從中啟動 `node` 程序的目錄。如果您是從另一個目錄執行 Express 應用程式，保險作法是使用您想提供之目錄的絕對路徑： If you run the express app from another directory, it’s safer to use the absolute path of the directory that you want to serve:

```
const path = require('path')
app.use('/static', express.static(path.join(__dirname, 'public')))
```

For more details about the `serve-static` function and its options, see  [serve-static](https://expressjs.com/resources/middleware/serve-static.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/starter/static-files.md          )

---

# Version Support

> Find information about the support schedule for different Express.js versions, including which versions are currently maintained and end-of-life policies.

# Version Support

Only the latest version of any given major release line is supported.

Versions that are EOL (end-of-life) *may* receive updates for critical security vulnerabilities, but the Express team offers no guarantee and does not plan to address or release fixes for any issues found.

| Major Version | Minimum Node.js Version | Support Start Date | Support End Date |
| --- | --- | --- | --- |
| v5.x | 18 | September 2024 | ongoing |
| v4.x | 0.10.0 | April 2014 | ongoing |
| v3.x | 0.8.0 | October 2012 | July 2015 |
| v2.x | 0.4.1 | March 2011 | July 2012 |
| v1.x | 0.2.0 | December 2010 | March 2011 |
| v0.14.x | 0.1.98 | December 2010 | December 2010 |

## Commercial Support Options

If you are unable to update to a supported version of Express, please contact one of our partners to receive security updates:

- [HeroDevs Never-Ending Support](http://www.herodevs.com/support/express-nes?utm_source=expressjs&utm_medium=link&utm_campaign=express_eol_page)

 [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/support/index.md          )
