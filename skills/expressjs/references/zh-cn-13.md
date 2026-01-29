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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/examples.md          )

---

# 常见问题及解答

> Find answers to frequently asked questions about Express.js, including topics on application structure, models, authentication, template engines, error handling, and more.

# 常见问题及解答

## 如何构造自己的应用程序？

There is no definitive answer to this question. 这个问题没有固定答案。具体取决于您的应用程序以及参与团队的规模。为了实现尽可能的灵活性，Express 在结构方面不作任何假设。 To be as
flexible as possible, Express makes no assumptions in terms of structure.

路由和其他特定于应用程序的逻辑可以存在于您首选的任何目录结构的任意数量的文件中。请查看以下示例以获取灵感： View the following
examples for inspiration:

- [路由列表](https://github.com/expressjs/express/blob/4.13.1/examples/route-separation/index.js#L32-47)
- [路由图](https://github.com/expressjs/express/blob/4.13.1/examples/route-map/index.js#L52-L66)
- [MVC 样式控制器](https://github.com/expressjs/express/tree/master/examples/mvc)

另外还有针对 Express 的第三方扩展，这有助于简化某些模式：

- [资源丰富的路由](https://github.com/expressjs/express-resource)

## 如何定义模型？

Express 没有数据库概念。此概念留给第三方 Node 模块实现，因此可以接入几乎任何数据库。 This concept is
left up to third-party Node modules, allowing you to
interface with nearly any database.

请参阅 [LoopBack](http://loopback.io) 以了解处于模型中心的基于 Express 的框架。

## 如何对用户进行认证？

Authentication is another opinionated area that Express does not
venture into. You may use any authentication scheme you wish.
认证是 Express 没有涉足的另一严格领域。您可使用所希望的任何认证方案。
要了解简单的“用户名/密码”方案，请参阅[此示例](https://github.com/expressjs/express/tree/master/examples/auth)。

## Express 支持哪些模板引擎？

Express 支持符合 `(path, locals, callback)` 特征符的任何模板引擎。
为了使模板引擎接口和高速缓存实现标准化，请参阅 [consolidate.js](https://github.com/visionmedia/consolidate.js) 项目以获得支持。未列出的模板引擎可能也支持 Express 特征符。
To normalize template engine interfaces and caching, see the
[consolidate.js](https://github.com/visionmedia/consolidate.js)
project for support. Unlisted template engines might still support the Express signature.

For more information, see [Using template engines with Express](https://expressjs.com/zh-cn/guide/using-template-engines.html).

## 如何处理 404 响应？

在 Express 中，404 响应不是错误的结果，所以错误处理程序中间件不会将其捕获。此行为是因为 404 响应只是表明缺少要执行的其他工作；换言之，Express 执行了所有中间件函数和路由，且发现它们都没有响应。您需要做的只是在堆栈的最底部（在其他所有函数之下）添加一个中间件函数来处理 404 响应： This behavior is
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

## 如何设置错误处理程序？

错误处理中间件的定义方式与其他中间件基本相同，差别在于错误处理中间件有四个自变量而不是三个，专门具有特征符 `(err, req, res, next)`：

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

有关更多信息，请参阅[错误处理](https://expressjs.com/zh-cn/guide/error-handling.html)。

## 如何呈现纯 HTML？

You don’t! 您不必这么做！无需使用 `res.render()` 函数来“呈现”HTML。
如果您具有特定文件，请使用 `res.sendFile()` 函数。
如果您希望从目录提供许多资产，请使用 `express.static()` 中间件函数。
If you have a specific file, use the `res.sendFile()` function.
If you are serving many assets from a directory, use the `express.static()`
middleware function.

## What version of Node.js does Express require?

- [Express 4.x](https://expressjs.com/zh-cn/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/zh-cn/5x/api.html) requires Node.js 18 or higher.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/faq.md          )

---

# Express 应用程序生成器

> Learn how to use the Express application generator tool to quickly create a skeleton for your Express.js applications, streamlining setup and configuration.

# Express 应用程序生成器

可使用应用程序生成器工具 (`express-generator`) 快速创建应用程序框架。

您可以使用 `npx` 命令（在 Node.js 8.2.0 中可用）运行应用程序生成器。

```
$ npx express-generator
```

对于早期的 Node 版本，可将应用程序生成器作为全局 npm 软件包安装，然后启动它。

```
$ npm install -g express-generator
$ express
```

使用 `-h` 选项显示命令选项：

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

For example, the following creates an Express app named *myapp*. 例如，以下语句在当前工作目录中创建名为 *myapp* 的 Express 应用程序并将视图引擎将设置为 [Pug](https://pugjs.org/) ：

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

然后安装依赖项：

```
$ cd myapp
$ npm install
```

在 MacOS 或 Linux 上，采用以下命令运行此应用程序：

```
$ DEBUG=myapp:* npm start
```

在 Windows 命令提示符上，使用以下命令：

```
> set DEBUG=myapp:* & npm start
```

在 Windows PowerShell 上，使用以下命令：

```
PS> $env:DEBUG='myapp:*'; npm start
```

然后在浏览器中输入 `http://localhost:3000/` 以访问此应用程序。

生成的应用程序具有以下目录结构：

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

生成器创建的应用程序结构只是构造 Express 应用程序的众多方法之一。请随意使用此结构或者对其进行修改以最大程度满足自己的需求。
 Feel free to use this structure or modify it to best suit your needs.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/generator.md          )

---

# Hello world 示例

> Get started with Express.js by building a simple 'Hello World' application, demonstrating the basic setup and server creation for beginners.

# Hello world 示例

Embedded below is essentially the simplest Express app you can create. It is a single file app — *not* what you’d get if you use the [Express generator](https://expressjs.com/zh-cn/starter/generator.html), which creates the scaffolding for a full app with numerous JavaScript files, Jade templates, and sub-directories for various purposes.

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

This app starts a server and listens on port 3000 for connections. 应用程序会启动服务器，并在端口 3000 上侦听连接。此应用程序以“Hello World!”响应针对根 URL (`/`) 或_路由_的请求。对于其他所有路径，它将以 **404 Not Found** 进行响应。 For every other path, it will respond with a **404 Not Found**.

### Running Locally

首先创建名为 `myapp` 的目录，切换到此目录，然后运行 `npm init`。根据[安装指南](https://expressjs.com/zh-cn/starter/installing.html)将 `express` 安装为依赖项。 Then, install `express` as a dependency, as per the [installation guide](https://expressjs.com/zh-cn/starter/installing.html).

在 `myapp` 目录中，创建名为 `app.js` 的文件，然后添加以下代码：

`req`（请求）和 `res`（响应）与 Node 提供的对象完全相同，所以您可以在不涉及 Express 的情况下调用 `req.pipe()`、`req.on('data', callback)` 和要执行的其他任何函数。

使用以下命令运行应用程序：

```
$ node app.js
```

然后，在浏览器中输入 [http://localhost:3000/](http://localhost:3000/) 以查看输出。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/hello-world.md          )

---

# 安装

> Learn how to install Express.js in your Node.js environment, including setting up your project directory and managing dependencies with npm.

# 安装

假设您已经安装了 [Node.js](https://nodejs.org/)，创建目录以保存应用程序，并将其设置为工作目录。

- [Express 4.x](https://expressjs.com/zh-cn/4x/api.html) requires Node.js 0.10 or higher.
- [Express 5.x](https://expressjs.com/zh-cn/5x/api.html) requires Node.js 18 or higher.

```
$ mkdir myapp
$ cd myapp
```

使用 `npm init` 命令为应用程序创建 `package.json` 文件。
有关 `package.json` 工作方式的更多信息，请参阅 [Specifics of npm’s package.json handling](https://docs.npmjs.com/files/package.json)。
For more information on how `package.json` works, see [Specifics of npm’s package.json handling](https://docs.npmjs.com/files/package.json).

```
$ npm init
```

This command prompts you for a number of things, such as the name and version of your application.
For now, you can simply hit RETURN to accept the defaults for most of them, with the following exception:

```
entry point: (index.js)
```

输入 `app.js`，或者您希望使用的任何主文件名称。如果希望文件名为 `index.js`，请按回车键以接受建议的缺省文件名。 If you want it to be `index.js`, hit RETURN to accept the suggested default file name.

在 `myapp` 目录中安装 Express，然后将其保存在依赖项列表中。例如： For example:

```
$ npm install express
```

要暂时安装 Express 而不将其添加到依赖项列表中：

```
$ npm install express --no-save
```

默认情况下，版本为 npm 5.0+ 的 npm install 将模块添加到 `package.json` 文件中的 `dependencies` 列表；对于较早版本的 npm，必须显式指定 `--save` 选项。
今后运行 `app` 目录中的 `npm install` 将自动安装依赖项列表中的模块。
 Then, afterwards, running `npm install` in the app directory will automatically install modules in the dependencies list.

   [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/installing.md          )

---

# 在 Express 中提供静态文件

> Understand how to serve static files like images, CSS, and JavaScript in Express.js applications using the built-in 'static' middleware.

# 在 Express 中提供静态文件

为了提供诸如图像、CSS 文件和 JavaScript 文件之类的静态文件，请使用 Express 中的 `express.static` 内置中间件函数。

The function signature is:

```
express.static(root, [options])
```

The `root` argument specifies the root directory from which to serve static assets.
For more information on the `options` argument, see [express.static](https://expressjs.com/zh-cn/5x/api.html#express.static).

For example, use the following code to serve images, CSS files, and JavaScript files in a directory named `public`:

```
app.use(express.static('public'))
```

现在，可以访问位于 `public` 目录中的文件：

```
http://localhost:3000/images/kitten.jpg
http://localhost:3000/css/style.css
http://localhost:3000/js/app.js
http://localhost:3000/images/bg.png
http://localhost:3000/hello.html
```

Express 相对于静态目录查找文件，因此静态目录的名称不是此 URL 的一部分。

要使用多个静态资源目录，请多次调用 `express.static` 中间件函数：

```
app.use(express.static('public'))
app.use(express.static('files'))
```

Express 以您使用 `express.static` 中间件函数设置静态目录的顺序来查找文件。

Note

For best results, [use a reverse proxy](https://expressjs.com/zh-cn/advanced/best-practice-performance.html#use-a-reverse-proxy) cache to improve performance of serving static assets.

To create a virtual path prefix (where the path does not actually exist in the file system) for files that are served by the `express.static` function, [specify a mount path](https://expressjs.com/zh-cn/5x/api.html#app.use) for the static directory, as shown below:

```
app.use('/static', express.static('public'))
```

现在，可以访问具有 `/static` 路径前缀的 `public` 目录中的文件。

```
http://localhost:3000/static/images/kitten.jpg
http://localhost:3000/static/css/style.css
http://localhost:3000/static/js/app.js
http://localhost:3000/static/images/bg.png
http://localhost:3000/static/hello.html
```

然而，向 `express.static` 函数提供的路径相对于您在其中启动 `node` 进程的目录。如果从另一个目录运行 Express 应用程序，那么对于提供资源的目录使用绝对路径会更安全： If you run the express app from another directory, it’s safer to use the absolute path of the directory that you want to serve:

```
const path = require('path')
app.use('/static', express.static(path.join(__dirname, 'public')))
```

For more details about the `serve-static` function and its options, see  [serve-static](https://expressjs.com/resources/middleware/serve-static.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/starter/static-files.md          )

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

 [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/support/index.md          )
