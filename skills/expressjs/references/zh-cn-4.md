# 生产环境最佳实践：性能和可靠性 and more

# 生产环境最佳实践：性能和可靠性

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# 生产环境最佳实践：性能和可靠性

本文讨论了部署到生产环境的 Express 应用程序的性能和可靠性最佳实践。

This topic clearly falls into the “devops” world, spanning both traditional development and operations. Accordingly, the information is divided into two parts:

- [代码中的注意事项](#code)（开发部分）。
  - 通过 Gzip 压缩，有助于显著降低响应主体的大小，从而提高 Web 应用程序的速度。可使用[压缩](https://www.npmjs.com/package/compression)中间件进行 Express 应用程序中的 gzip 压缩。例如：
  - 不使用同步函数
  - 正确进行日志记录
  - [Handle exceptions properly](#handle-exceptions-properly)
- Things to do in your environment / setup (the ops part):
  - 将 NODE_ENV 设置为“production”
  - Node 应用程序在遇到未捕获的异常时会崩溃。您需要确保应用程序经过彻底测试，能够处理所有异常，这一点最为重要（请参阅[正确处理异常](#exceptions)以了解详细信息）。但是，作为一种防故障措施，请实施一种机制，确保应用程序崩溃后可以自动重新启动。
  - 在集群应用程序中，个别工作进程的崩溃并不会影响其余的进程。除了性能优势，故障隔离是运行应用程序进程集群的另一原因。每当工作进程崩溃时，请确保始终使用 cluster.fork() 来记录事件并生成新进程。
  - 高速缓存请求结果
  - 使用负载均衡器
  - 逆向代理位于 Web 应用程序之前，除了将请求转发给应用程序外，还对请求执行支持性操作。它还可以处理错误页、压缩、高速缓存、文件服务和负载均衡等功能。

## Things to do in your code

以下是为改进应用程序性能而在代码中要注意的事项：

- 通过 Gzip 压缩，有助于显著降低响应主体的大小，从而提高 Web 应用程序的速度。可使用[压缩](https://www.npmjs.com/package/compression)中间件进行 Express 应用程序中的 gzip 压缩。例如：
- 不使用同步函数
- 正确进行日志记录
- [Handle exceptions properly](#handle-exceptions-properly)

### 使用 gzip 压缩

Gzip compressing can greatly decrease the size of the response body and hence increase the speed of a web app. Use the [compression](https://www.npmjs.com/package/compression) middleware for gzip compression in your Express app. For example:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

For a high-traffic website in production, the best way to put compression in place is to implement it at a reverse proxy level (see [Use a reverse proxy](#use-a-reverse-proxy)). In that case, you do not need to use compression middleware. 对于生产环境中的大流量网站，实施压缩的最佳位置是在反向代理层级（请参阅[使用反向代理](#proxy)）。在此情况下，不需要使用压缩中间件。有关在 Nginx 中启用 gzip 压缩的详细信息，请参阅 Nginx 文档中的 [ngx_http_gzip_module 模块](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)。

### 不使用同步函数

Synchronous functions and methods tie up the executing process until they return. A single call to a synchronous function might return in a few microseconds or milliseconds, however in high-traffic websites, these calls add up and reduce the performance of the app. Avoid their use in production.

虽然 Node 和许多模块提供函数的同步和异步版本，但是在生产环境中请始终使用异步版本。只有在初始启动时才适合使用同步函数。 The only time when a synchronous function can be justified is upon initial startup.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Of course, you wouldn’t want to use this in production, but rather to ensure that your code is ready for production. See the [node command-line options documentation](https://nodejs.org/api/cli.html#cli_trace_sync_io) for more information.

### 正确处理异常

In general, there are two reasons for logging from your app: For debugging and for logging app activity (essentially, everything else). Using `console.log()` or `console.error()` to print log messages to the terminal is common practice in development. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### For debugging

如果您出于调试目的进行日志记录，请使用 [debug](https://www.npmjs.com/package/debug) 这样的特殊调试模块，而不要使用 `console.log()`。此模块支持您使用 DEBUG 环境变量来控制将哪些调试消息（如果有）发送到 `console.err()`。为了确保应用程序完全采用异步方式，仍需要将 `console.err()` 通过管道传到另一个程序。但您并不会真的希望在生产环境中进行调试，对吧？ This module enables you to use the DEBUG environment variable to control what debug messages are sent to `console.error()`, if any. To keep your app purely asynchronous, you’d still want to pipe `console.error()` to another program. But then, you’re not really going to debug in production, are you?

#### 出于应用程序活动目的

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### 正确处理异常

Node 应用程序在遇到未捕获的异常时会崩溃。不处理异常并采取相应的措施会导致 Express 应用程序崩溃并脱机。如果您按照以下[确保应用程序自动重新启动](#restart)中的建议执行，那么应用程序可以从崩溃中恢复。幸运的是，Express 应用程序的启动时间一般很短。然而，应当首先立足于避免崩溃，为此，需要正确处理异常。 Not handling exceptions and taking appropriate actions will make your Express app crash and go offline. If you follow the advice in [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts) below, then your app will recover from a crash. Fortunately, Express apps typically have a short startup time. Nevertheless, you want to avoid crashing in the first place, and to do that, you need to handle exceptions properly.

要确保处理所有异常，请使用以下方法：

- [使用 try-catch](#try-catch)
- [使用 promise](#promises)

在深入了解这些主题之前，应该对 Node/Express 错误处理有基本的了解：使用 error-first 回调并在中间件中传播错误。Node 将“error-first 回调”约定用于从异步函数返回错误，回调函数的第一个参数是错误对象，后续参数中包含结果数据。为了表明没有错误，可将 null 值作为第一个参数传递。回调函数必须相应地遵循“error-first”回调约定，以便有意义地处理错误。在 Express 中，最佳做法是使用 next() 函数，通过中间件链来传播错误。 Node uses an “error-first callback” convention for returning errors from asynchronous functions, where the first parameter to the callback function is the error object, followed by result data in succeeding parameters. To indicate no error, pass null as the first parameter. The callback function must correspondingly follow the error-first callback convention to meaningfully handle the error. And in Express, the best practice is to use the next() function to propagate errors through the middleware chain.

有关错误处理基本知识的更多信息，请参阅：

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### 使用 try-catch

Try-catch 是一种 JavaScript 语言构造，可用于捕获同步代码中的异常。例如，使用 try-catch 来处理 JSON 解析错误（如下所示）。 Use try-catch, for example, to handle JSON parsing errors as shown below.

Here is an example of using try-catch to handle a potential process-crashing exception.
This middleware function accepts a query field parameter named “params” that is a JSON object.

```
app.get('/search', (req, res) => {
  // Simulating async operation
  setImmediate(() => {
    const jsonStr = req.query.params
    try {
      const jsonObj = JSON.parse(jsonStr)
      res.send('Success')
    } catch (e) {
      res.status(400).send('Invalid JSON string')
    }
  })
})
```

However, try-catch works only for synchronous code. 然而，try-catch 仅适用于同步代码。而由于 Node 平台主要采用异步方式（尤其在生产环境中），因此 try-catch 不会捕获大量异常。

#### 使用 promise

When an error is thrown in an `async` function or a rejected promise is awaited inside an `async` function, those errors will be passed to the error handler as if calling `next(err)`

```
app.get('/', async (req, res, next) => {
  const data = await userData() // If this promise fails, it will automatically call `next(err)` to handle the error.

  res.send(data)
})

app.use((err, req, res, next) => {
  res.status(err.status ?? 500).send({ error: err.message })
})
```

Also, you can use asynchronous functions for your middleware, and the router will handle errors if the promise fails, for example:

```
app.use(async (req, res, next) => {
  req.locals.user = await getUser(req)

  next() // This will be called if the promise does not throw an error.
})
```

Best practice is to handle errors as close to the site as possible. So while this is now handled in the router, it’s best to catch the error in the middleware and handle it without relying on separate error-handling middleware.

#### What not to do

_请勿_侦听 `uncaughtException` 事件，当异常像气泡一样在事件循环中一路回溯时，就会发出该事件。为 `uncaughtException` 添加事件侦听器将改变进程遇到异常时的缺省行为；进程将继续运行而不理会异常。这貌似是防止应用程序崩溃的好方法，但是在遇到未捕获的异常之后仍继续运行应用程序是一种危险的做法，不建议这么做，因为进程状态可能会变得不可靠和不可预测。 Adding an event listener for `uncaughtException` will change the default behavior of the process that is encountering an exception; the process will continue to run despite the exception. This might sound like a good way of preventing your app from crashing, but continuing to run the app after an uncaught exception is a dangerous practice and is not recommended, because the state of the process becomes unreliable and unpredictable.

此外，`uncaughtException` 被公认为[比较粗糙](https://nodejs.org/api/process.html#process_event_uncaughtexception)，[建议](https://github.com/nodejs/node-v0.x-archive/issues/2582)从内核中将其移除。所以侦听 `uncaughtException` 并不是个好主意。这就是为何我们推荐诸如多个进程和虚拟机管理器之类的方案：崩溃后重新启动通常是从错误中恢复的最可靠方法。 So listening for `uncaughtException` is just a bad idea. This is why we recommend things like multiple processes and supervisors: crashing and restarting is often the most reliable way to recover from an error.

我们也不建议使用[域](https://nodejs.org/api/domain.html)。它一般并不能解决问题，是一种不推荐使用的模块。 It generally doesn’t solve the problem and is a deprecated module.

## 环境/设置中的注意事项

以下是为改进应用程序性能而在系统环境中要注意的事项：

- 将 NODE_ENV 设置为“production”
- Node 应用程序在遇到未捕获的异常时会崩溃。您需要确保应用程序经过彻底测试，能够处理所有异常，这一点最为重要（请参阅[正确处理异常](#exceptions)以了解详细信息）。但是，作为一种防故障措施，请实施一种机制，确保应用程序崩溃后可以自动重新启动。
- 在集群应用程序中，个别工作进程的崩溃并不会影响其余的进程。除了性能优势，故障隔离是运行应用程序进程集群的另一原因。每当工作进程崩溃时，请确保始终使用 cluster.fork() 来记录事件并生成新进程。
- 高速缓存请求结果
- 使用负载均衡器
- 逆向代理位于 Web 应用程序之前，除了将请求转发给应用程序外，还对请求执行支持性操作。它还可以处理错误页、压缩、高速缓存、文件服务和负载均衡等功能。

### 将 NODE_ENV 设置为“production”

The NODE_ENV environment variable specifies the environment in which an application is running (usually, development or production). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

将 NODE_ENV 设置为“production”会使 Express：

- 高速缓存视图模板。
- 高速缓存从 CSS 扩展生成的 CSS 文件。
- 生成简短的错误消息。

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

如果您需要编写特定于环境的代码，可以使用 `process.env.NODE_ENV` 来检查 NODE_ENV 的值。请注意，检查任何环境变量的值都会导致性能下降，所以应该三思而行。 Be aware that checking the value of any environment variable incurs a performance penalty, and so should be done sparingly.

在开发中，通常会在交互式 shell 中设置环境变量，例如，使用 `export` 或者 `.bash_profile` 文件。但是一般而言，您不应在生产服务器上执行此操作；而是应当使用操作系统的初始化系统（systemd 或 Upstart）。下一节提供如何使用初始化系统的常规详细信息，但是设置 NODE_ENV 对于性能非常重要（且易于操作），所以会在此重点介绍。 But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). The next section provides more details about using your init system in general, but setting `NODE_ENV` is so important for performance (and easy to do), that it’s highlighted here.

对于 systemd，请使用单元文件中的 `Environment` 伪指令。例如： For example:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### 确保应用程序能够自动重新启动

In production, you don’t want your application to be offline, ever. This means you need to make sure it restarts both if the app crashes and if the server itself crashes. Although you hope that neither of those events occurs, realistically you must account for both eventualities by:

- 使用进程管理器在应用程序（和 Node）崩溃时将其重新启动。
- 在操作系统崩溃时，使用操作系统提供的初始化系统重新启动进程管理器。还可以在没有进程管理器的情况下使用初始化系统。 It’s also possible to use the init system without a process manager.

Node applications crash if they encounter an uncaught exception. The foremost thing you need to do is to ensure your app is well-tested and handles all exceptions (see [handle exceptions properly](#handle-exceptions-properly) for details). But as a fail-safe, put a mechanism in place to ensure that if and when your app crashes, it will automatically restart.

#### 使用进程管理器

在开发中，只需在命令行从 `node server.js` 或类似项启动应用程序。但是在生产环境中执行此操作会导致灾难。如果应用程序崩溃，它会脱机，直到其重新启动为止。为了确保应用程序在崩溃后可以重新启动，请使用进程管理器。进程管理器是一种应用程序“容器”，用于促进部署，提供高可用性，并支持用户在运行时管理应用程序。 But doing this in production is a recipe for disaster. If the app crashes, it will be offline until you restart it. To ensure your app restarts if it crashes, use a process manager. A process manager is a “container” for applications that facilitates deployment, provides high availability, and enables you to manage the application at runtime.

除了在应用程序崩溃时将其重新启动外，进程管理器还可以执行以下操作：

- 获得对运行时性能和资源消耗的洞察。
- 动态修改设置以改善性能。
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### 使用初始化系统

下一层的可靠性是确保在服务器重新启动时应用程序可以重新启动。系统仍然可能由于各种原因而宕机。为了确保在服务器崩溃后应用程序可以重新启动，请使用内置于操作系统的初始化系统。目前主要使用两种初始化系统：[systemd](https://wiki.debian.org/systemd) 和 [Upstart](http://upstart.ubuntu.com/)。 Systems can still go down for a variety of reasons. To ensure that your app restarts if the server crashes, use the init system built into your OS. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

有两种方法将初始化系统用于 Express 应用程序：

- 在进程管理器中运行应用程序，使用初始化系统将进程管理器安装为服务。进程管理器将在应用程序崩溃时将其重新启动，初始化系统则在操作系统重新启动时重新启动进程管理器。这是建议使用的方法。 The process manager will restart your app when the app crashes, and the init system will restart the process manager when the OS restarts. This is the recommended approach.
- Run your app (and Node) directly with the init system. This is somewhat simpler, but you don’t get the additional advantages of using a process manager.

##### Systemd

Systemd 是一个 Linux 系统和服务管理器。大多数主要 Linux 分发版采用 systemd 作为其缺省初始化系统。 Most major Linux distributions have adopted systemd as their default init system.

A systemd service configuration file is called a *unit file*, with a filename ending in `.service`. Here’s an example unit file to manage a Node app directly. Replace the values enclosed in `<angle brackets>` for your system and app:

```
[Unit]
Description=<Awesome Express App>

[Service]
Type=simple
ExecStart=/usr/local/bin/node </projects/myapp/index.js>
WorkingDirectory=</projects/myapp>

User=nobody
Group=nogroup

# Environment variables:
Environment=NODE_ENV=production

# Allow many incoming connections
LimitNOFILE=infinity

# Allow core dumps for debugging
LimitCORE=infinity

StandardInput=null
StandardOutput=syslog
StandardError=syslog
Restart=always

[Install]
WantedBy=multi-user.target
```

有关 systemd 的更多信息，请参阅 [systemd 参考（联机帮助页）](http://www.freedesktop.org/software/systemd/man/systemd.unit.html)。

### 在集群中运行应用程序

在多核系统中，可以通过启动进程的集群，将 Node 应用程序的性能提升多倍。一个集群运行此应用程序的多个实例，理想情况下一个 CPU 核心上运行一个实例，从而在实例之间分担负载和任务。 A cluster runs multiple instances of the app, ideally one instance on each CPU core, thereby distributing the load and tasks among the instances.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANT: Since the app instances run as separate processes, they do not share the same memory space. That is, objects are local to each instance of the app. Therefore, you cannot maintain state in the application code. However, you can use an in-memory datastore like [Redis](http://redis.io/) to store session-related data and state. This caveat applies to essentially all forms of horizontal scaling, whether clustering with multiple processes or multiple physical servers.

In clustered apps, worker processes can crash individually without affecting the rest of the processes. Apart from performance advantages, failure isolation is another reason to run a cluster of app processes. Whenever a worker process crashes, always make sure to log the event and spawn a new process using cluster.fork().

#### 使用 Node 的集群模块

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). This enables a master process to spawn worker processes and distribute incoming connections among the workers.

#### Using PM2

If you deploy your application with PM2, then you can take advantage of clustering *without* modifying your application code. You should ensure your [application is stateless](https://pm2.keymetrics.io/docs/usage/specifics/#stateless-apps) first, meaning no local data is stored in the process (such as sessions, websocket connections and the like).

When running an application with PM2, you can enable **cluster mode** to run it in a cluster with a number of instances of your choosing, such as the matching the number of available CPUs on the machine. You can manually change the number of processes in the cluster using the `pm2` command line tool without stopping the app.

To enable cluster mode, start your application like so:

```
# Start 4 worker processes
$ pm2 start npm --name my-app -i 4 -- start
# Auto-detect number of available CPUs and start that many worker processes
$ pm2 start npm --name my-app -i max -- start
```

This can also be configured within a PM2 process file (`ecosystem.config.js` or similar) by setting `exec_mode` to `cluster` and `instances` to the number of workers to start.

Once running, the application can be scaled like so:

```
# Add 3 more workers
$ pm2 scale my-app +3
# Scale to a specific number of workers
$ pm2 scale my-app 2
```

For more information on clustering with PM2, see [Cluster Mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/) in the PM2 documentation.

### 高速缓存请求结果

提高生产环境性能的另一种策略是对请求的结果进行高速缓存，以便应用程序不需要为满足同一请求而重复执行操作。

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### 使用负载均衡器

无论应用程序如何优化，单个实例都只能处理有限的负载和流量。扩展应用程序的一种方法是运行此应用程序的多个实例，并通过负载均衡器分配流量。设置负载均衡器可以提高应用程序的性能和速度，并使可扩展性远超单个实例可以达到的水平。 One way to scale an app is to run multiple instances of it and distribute the traffic via a load balancer. Setting up a load balancer can improve your app’s performance and speed, and enable it to scale more than is possible with a single instance.

A load balancer is usually a reverse proxy that orchestrates traffic to and from multiple application instances and servers. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

对于负载均衡功能，可能必须确保与特定会话标识关联的请求连接到产生请求的进程。这称为_会话亲缘关系_或者_粘性会话_，可通过以上的建议来做到这一点：将 Redis 之类的数据存储器用于会话数据（取决于您的应用程序）。要了解相关讨论，请参阅 [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/)。 This is known as *session affinity*, or *sticky sessions*, and may be addressed by the suggestion above to use a data store such as Redis for session data (depending on your application). For a discussion, see [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### 使用逆向代理

A reverse proxy sits in front of a web app and performs supporting operations on the requests, apart from directing requests to the app. It can handle error pages, compression, caching, serving files, and load balancing among other things.

通过将无需了解应用程序状态的任务移交给逆向代理，可以使 Express 腾出资源来执行专门的应用程序任务。因此，建议在生产环境中，在 [Nginx](https://www.nginx.com/) 或 [HAProxy](http://www.haproxy.org/) 之类的逆向代理背后运行 Express。 For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/advanced/best-practice-performance.md          )

---

# 生产环境最佳实践：安全

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# 生产环境最佳实践：安全

## 概述

术语*“生产”*表示软件生命周期中应用程序或 API 可供最终用户或使用者正常使用的阶段。而在*“开发”*阶段中，您仍然积极编写和测试代码，应用程序并未对外部开发访问。对应的系统环境分别被称为_生产_和_开发*环境。 In contrast, in the _“development”* stage, you’re still actively writing and testing code, and the application is not open to external access. The corresponding system environments are known as *production* and *development* environments, respectively.

Development and production environments are usually set up differently and have vastly different requirements. What’s fine in development may not be acceptable in production. For example, in a development environment you may want verbose logging of errors for debugging, while the same behavior can become a security concern in a production environment. And in development, you don’t need to worry about scalability, reliability, and performance, while those concerns become critical in production.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

本文讨论了部署到生产环境的 Express 应用程序的一些安全最佳实践。

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [hsts](https://github.com/helmetjs/hsts) 用于设置 `Strict-Transport-Security` 头，实施安全的服务器连接 (HTTP over SSL/TLS)。
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [hidePoweredBy](https://github.com/helmetjs/hide-powered-by) 用于移除 `X-Powered-By` 头。
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - `domain` - 表示 cookie 的域；用于和请求 URL 的服务器的域进行比较。如果匹配，那么接下来检查路径属性。
    - 相反，[cookie-session](https://www.npmjs.com/package/cookie-session) 中间件实现 cookie 支持的存储：它将整个会话序列化到 cookie 中，而不只是会话键。仅当会话数据相对较小，且易于编码为原语值（而不是对象）时，才使用此中间件。尽管假设浏览器支持每个 cookie 至少 4096 字节以确保不会超过限制，但是每个域的大小不会超过 4093 字节。另外请注意，客户机可以访问 cookie 数据，所以，如果有任何理由将其保持安全或隐藏状态，那么 express-session 可能是更好的选择。
    - 使用缺省会话 cookie 名称会使应用程序对攻击敞开大门。`X-Powered-By` 之类的值会造成问题：潜在攻击者可以利用这样的值对服务器采集“指纹”，并相应地确定攻击目标。
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - 最后说明一点，和任何其他 Web 应用程序一样，Express 应用程序也容易受到各种基于 Web 的攻击。请熟悉已知的 [Web 漏洞](https://www.owasp.org/www-project-top-ten/)并采取相应的预防措施。
  - [Additional considerations](#additional-considerations)

## 请勿使用不推荐或者存在漏洞的 Express 版本

Express 2.x and 3.x are no longer maintained. Security and performance issues in these versions won’t be fixed. Do not use them! If you haven’t moved to version 4, follow the [migration guide](https://expressjs.com/zh-cn/guide/migrating-4.html) or consider [Commercial Support Options](https://expressjs.com/zh-cn/support#commercial-support-options).

Also ensure you are not using any of the vulnerable Express versions listed on the [Security updates page](https://expressjs.com/zh-cn/advanced/security-updates.html). If you are, update to one of the stable releases, preferably the latest.

## 使用 TLS

If your app deals with or transmits sensitive data, use [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) to secure the connection and the data. This technology encrypts data before it is sent from the client to the server, thus preventing some common (and easy) hacks. Although Ajax and POST requests might not be visibly obvious and seem “hidden” in browsers, their network traffic is vulnerable to [packet sniffing](https://en.wikipedia.org/wiki/Packet_analyzer) and [man-in-the-middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

You may be familiar with Secure Socket Layer (SSL) encryption. [TLS is simply the next progression of SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). In other words, if you were using SSL before, consider upgrading to TLS. In general, we recommend Nginx to handle TLS. For a good reference to configure TLS on Nginx (and other servers), see [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

此外，可以使用一种方便的 [Let’s Encrypt](https://letsencrypt.org/about/) 工具来获取免费的 TLS 证书，这是由[因特网安全研究组 (ISRG)](https://letsencrypt.org/isrg/) 提供的免费、自动化的开放式认证中心 (CA)。

## Do not trust user input

For web applications, one of the most critical security requirements is proper user input validation and handling. This comes in many forms and we will not cover all of them here.
Ultimately, the responsibility for validating and correctly handling the types of user input your application accepts is yours.

### Prevent open redirects

An example of potentially dangerous user input is an *open redirect*, where an application accepts a URL as user input (often in the URL query, for example `?url=https://example.com`) and uses `res.redirect` to set the `location` header and
return a 3xx status.

An application must validate that it supports redirecting to the incoming URL to avoid sending users to malicious links such as phishing websites, among other risks.

Here is an example of checking URLs before using `res.redirect` or `res.location`:

```
app.use((req, res) => {
  try {
    if (new Url(req.query.url).host !== 'example.com') {
      return res.status(400).end(`Unsupported redirect to host: ${req.query.url}`)
    }
  } catch (e) {
    return res.status(400).end(`Invalid url: ${req.query.url}`)
  }
  res.redirect(req.query.url)
})
```

## 使用 Helmet

[Helmet](https://www.npmjs.com/package/helmet) 通过适当地设置 HTTP 头，帮助您保护应用程序避免一些众所周知的 Web 漏洞。

Helmet is a middleware function that sets security-related HTTP response headers. Helmet sets the following headers by default:

- `Content-Security-Policy`: A powerful allow-list of what can happen on your page which mitigates many attacks
- `Cross-Origin-Opener-Policy`: Helps process-isolate your page
- `Cross-Origin-Resource-Policy`: Blocks others from loading your resources cross-origin
- `Origin-Agent-Cluster`: Changes process isolation to be origin-based
- `Referrer-Policy`: Controls the [Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer) header
- `Strict-Transport-Security`: Tells browsers to prefer HTTPS
- `X-Content-Type-Options`: Avoids [MIME sniffing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#mime_sniffing)
- `X-DNS-Prefetch-Control`: Controls DNS prefetching
- `X-Download-Options`: Forces downloads to be saved (Internet Explorer only)
- `X-Frame-Options`: Legacy header that mitigates [Clickjacking](https://en.wikipedia.org/wiki/Clickjacking) attacks
- `X-Permitted-Cross-Domain-Policies`: Controls cross-domain behavior for Adobe products, like Acrobat
- `X-Powered-By`: Info about the web server. Removed because it could be used in simple attacks
- `X-XSS-Protection`: Legacy header that tries to mitigate [XSS attacks](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting), but makes things worse, so Helmet disables it

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/zh-cn/advanced/如果使用 `helmet.js`，它会为您执行此功能。).

像安装其他模块一样安装 Helmet：

```
$ npm install helmet
```

然后将其用于您的代码：

```
// ...

const helmet = require('helmet')
app.use(helmet())

// ...
```

## Reduce fingerprinting

It can help to provide an extra layer of security to reduce the ability of attackers to determine
the software that a server uses, known as “fingerprinting.” Though not a security issue itself,
reducing the ability to fingerprint an application improves its overall security posture.
Server software can be fingerprinted by quirks in how it responds to specific requests, for example in
the HTTP response headers.

By default, Express sends the `X-Powered-By` response header that you can
disable using the `app.disable()` method:

```
app.disable('x-powered-by')
```

Note

Disabling the `X-Powered-By header` does not prevent
a sophisticated attacker from determining that an app is running Express. It may
discourage a casual exploit, but there are other ways to determine an app is running
Express.

Express also sends its own formatted “404 Not Found” messages and formatter error
response messages. These can be changed by
[adding your own not found handler](https://expressjs.com/en/starter/faq.html#how-do-i-handle-404-responses)
and
[writing your own error handler](https://expressjs.com/en/guide/error-handling.html#writing-error-handlers):

```
// last app.use calls right before app.listen():

// custom 404
app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})

// custom error handler
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

## 安全地使用 cookie

要确保 cookie 不会打开应用程序使其暴露在风险之中，请勿使用缺省会话 cookie 名称并相应地设置 cookie 安全选项。

有两个主要的中间件 cookie 会话模块：

- [express-session](https://www.npmjs.com/package/express-session)，用于替换 Express 3.x 内置的 `express.session` 中间件。
- [cookie-session](https://www.npmjs.com/package/cookie-session)，用于替换 Express 3.x 内置的 `express.cookieSession` 中间件。

The main difference between these two modules is how they save cookie session data. 这两个模块之间的主要差异是它们保存 cookie 会话数据的方式。[express-session](https://www.npmjs.com/package/express-session) 中间件将会话数据存储在服务器上；它仅将会话标识（而非会话数据）保存在 cookie 中。缺省情况下，它使用内存中存储，并不旨在用于生产环境。在生产环境中，需要设置可扩展的会话存储；请参阅[兼容的会话存储](https://github.com/expressjs/session#compatible-session-stores)列表。 By default, it uses in-memory storage and is not designed for a production environment. In production, you’ll need to set up a scalable session-store; see the list of [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

In contrast, [cookie-session](https://www.npmjs.com/package/cookie-session) middleware implements cookie-backed storage: it serializes the entire session to the cookie, rather than just a session key. Only use it when session data is relatively small and easily encoded as primitive values (rather than objects). Although browsers are supposed to support at least 4096 bytes per cookie, to ensure you don’t exceed the limit, don’t exceed a size of 4093 bytes per domain. Also, be aware that the cookie data will be visible to the client, so if there is any reason to keep it secure or obscure, then `express-session` may be a better choice.

### 请勿使用缺省会话 cookie 名称

Using the default session cookie name can open your app to attacks. The security issue posed is similar to `X-Powered-By`: a potential attacker can use it to fingerprint the server and target attacks accordingly.

为避免此问题，请使用通用 cookie 名称；例如，使用 [express-session](https://www.npmjs.com/package/express-session) 中间件：

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### 设置 cookie 安全性选项

设置以下 cookie 选项来增强安全性：

- `secure` - 确保浏览器只通过 HTTPS 发送 cookie。
- `httpOnly` - 确保 cookie 只通过 HTTP(S)（而不是客户机 JavaScript）发送，这有助于防御跨站点脚本编制攻击。
- `domain` - indicates the domain of the cookie; use it to compare against the domain of the server in which the URL is being requested. If they match, then check the path attribute next.
- `path` - 表示 cookie 的路径；用于和请求路径进行比较。如果路径和域都匹配，那么在请求中发送 cookie。 If this and domain match, then send the cookie in the request.
- `expires` - 用于为持久性 cookie 设置到期日期。

以下是使用 [cookie-session](https://www.npmjs.com/package/cookie-session) 中间件的示例：

```
const session = require('cookie-session')
const express = require('express')
const app = express()

const expiryDate = new Date(Date.now() + 60 * 60 * 1000) // 1 hour
app.use(session({
  name: 'session',
  keys: ['key1', 'key2'],
  cookie: {
    secure: true,
    httpOnly: true,
    domain: 'example.com',
    path: 'foo/bar',
    expires: expiryDate
  }
}))
```

## Prevent brute-force attacks against authorization

Make sure login endpoints are protected to make private data more secure.

A simple and powerful technique is to block authorization attempts using two metrics:

1. The number of consecutive failed attempts by the same user name and IP address.
2. The number of failed attempts from an IP address over some long period of time. For example, block an IP address if it makes 100 failed attempts in one day.

[rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible) package provides tools to make this technique easy and fast. You can find [an example of brute-force protection in the documentation](https://github.com/animir/node-rate-limiter-flexible/wiki/Overall-example#login-endpoint-protection)

## Ensure your dependencies are secure

Using npm to manage your application’s dependencies is powerful and convenient. But the packages that you use may contain critical security vulnerabilities that could also affect your application. The security of your app is only as strong as the “weakest link” in your dependencies.

Since npm@6, npm automatically reviews every install request. Also, you can use `npm audit` to analyze your dependency tree.

```
$ npm audit
```

If you want to stay more secure, consider [Snyk](https://snyk.io/).

Snyk offers both a [command-line tool](https://www.npmjs.com/package/snyk) and a [Github integration](https://snyk.io/docs/github) that checks your application against [Snyk’s open source vulnerability database](https://snyk.io/vuln/) for any known vulnerabilities in your dependencies. Install the CLI as follows:

```
$ npm install -g snyk
$ cd your-app
```

Use this command to test your application for vulnerabilities:

```
$ snyk test
```

### 避免其他已知的漏洞

关注 [Node 安全项目](https://npmjs.com/advisories)公告，这可能会影响 Express 或应用程序使用的其他模块。一般而言，Node 安全项目是有关 Node 安全性的知识和工具的出色资源。 In general, these databases are excellent resources for knowledge and tools about Node security.

Finally, Express apps—like any other web apps—can be vulnerable to a variety of web-based attacks. Familiarize yourself with known [web vulnerabilities](https://www.owasp.org/www-project-top-ten/) and take precautions to avoid them.

## 其他注意事项

以下是来自非常出色的 [Node.js 安全核对表](https://blog.risingstack.com/node-js-security-checklist/)的一些进一步建议。请参阅此博客帖子以了解关于这些建议的所有详细信息： Refer to that blog post for all the details on these recommendations:

- 始终过滤和净化用户输入，防御跨站点脚本编制 (XSS) 和命令注入攻击。
- 使用参数化查询或预编译的语句来防御 SQL 注入攻击。
- 使用开源的 [sqlmap](http://sqlmap.org/) 工具来检测应用程序中的 SQL 注入漏洞。
- 使用 [nmap](https://nmap.org/) 和 [sslyze](https://github.com/nabla-c0d3/sslyze) 工具来测试 SSL 密码、密钥和重新协商的配置以及证书的有效性。
- 使用 [safe-regex](https://www.npmjs.com/package/safe-regex) 来确保正则表达式不易受到[正则表达式拒绝服务](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS)攻击。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/advanced/best-practice-security.md          )

---

# 为 Express 开发模板引擎

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# 为 Express 开发模板引擎

可以使用 `app.engine(ext, callback)` 方法创建自己的模板引擎。`ext` 表示文件扩展名，而 `callback` 表示模板引擎函数，它接受以下项作为参数：文件位置、选项对象和回调函数。 `ext` refers to the file extension, and `callback` is the template engine function, which accepts the following items as parameters: the location of the file, the options object, and the callback function.

以下代码示例实现非常简单的模板引擎以呈现 `.ntl` 文件。

```
const fs = require('fs') // this engine requires the fs module
app.engine('ntl', (filePath, options, callback) => { // define the template engine
  fs.readFile(filePath, (err, content) => {
    if (err) return callback(err)
    // this is an extremely simple template engine
    const rendered = content.toString()
      .replace('#title#', `<title>${options.title}</title>`)
      .replace('#message#', `<h1>${options.message}</h1>`)
    return callback(null, rendered)
  })
})
app.set('views', './views') // specify the views directory
app.set('view engine', 'ntl') // register the template engine
```

Your app will now be able to render `.ntl` files. 应用程序现在能够呈现 `.ntl` 文件。在 `views` 目录中创建名为 `index.ntl` 且包含以下内容的文件：

```pug
#title#
#message#
```

然后，在应用程序中创建以下路径：

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

您向主页发出请求时，`index.ntl` 将呈现为 HTML。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### 示例

```
const server = app.listen(port)

process.on('SIGTERM', () => {
  debug('SIGTERM signal received: closing HTTP server')
  server.close(() => {
    debug('HTTP server closed')
  })
})
```

## Health checks

A load balancer uses health checks to determine if an application instance is healthy and can accept requests. For example, [Kubernetes has two health checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/):

- `liveness`, that determines when to restart a container.
- `readiness`, that determines when a container is ready to start accepting traffic. When a pod is not ready, it is removed from the service load balancers.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/advanced/healthcheck-graceful-shutdown.md          )

---

# 安全更新

> Review the latest security updates and patches for Express.js, including detailed vulnerability lists for different versions to help maintain a secure application.

# 安全更新

Node.js vulnerabilities directly affect Express.
Node.js 漏洞直接影响 Express。因此，请[监视 Node.js 漏洞](https://nodejs.org
/en/blog/vulnerability/)并确保使用最新稳定版的 Node.js。

以下列举了在指定版本更新中修复的 Express 漏洞。

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/zh-cn/resources/contributing.html#security-policies-and-procedures).

## 4.x

- 4.21.2
  - The dependency `path-to-regexp` has been updated to address a [vulnerability](https://github.com/pillarjs/path-to-regexp/security/advisories/GHSA-rhx6-c78j-4q9w).
- 4.21.1
  - The dependency `cookie` has been updated to address a [vulnerability](https://github.com/jshttp/cookie/security/advisories/GHSA-pxg6-pf52-xh8x), This may affect your application if you use `res.cookie`.
- 4.20.0
  - Fixed XSS vulnerability in `res.redirect` ([advisory](https://github.com/expressjs/express/security/advisories/GHSA-qw6h-vgh9-j6wx), [CVE-2024-43796](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-43796)).
  - The dependency `serve-static` has been updated to address a [vulnerability](https://github.com/advisories/GHSA-cm22-4g7w-348p).
  - The dependency `send` has been updated to address a [vulnerability](https://github.com/advisories/GHSA-m6fv-jmcg-4jfg).
  - The dependency `path-to-regexp` has been updated to address a [vulnerability](https://github.com/pillarjs/path-to-regexp/security/advisories/GHSA-9wv6-86v2-598j).
  - The dependency `body-parser` has been updated to addres a [vulnerability](https://github.com/advisories/GHSA-qwcr-r2fm-qrc7), This may affect your application if you had url enconding activated.
- 4.19.0, 4.19.1
  - Fixed open redirect vulnerability in `res.location` and `res.redirect` ([advisory](https://github.com/expressjs/express/security/advisories/GHSA-rv95-896h-c2vc), [CVE-2024-29041](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-29041)).
- 4.17.3
  - The dependency `qs` has been updated to address a [vulnerability](https://github.com/advisories/GHSA-hrpp-h998-j3pp). This may affect your application if the following APIs are used: `req.query`, `req.body`, `req.param`.
- 4.16.0
  - The dependency `forwarded` has been updated to address a [vulnerability](https://npmjs.com/advisories/527). This may affect your application if the following APIs are used: `req.host`, `req.hostname`, `req.ip`, `req.ips`, `req.protocol`.
  - The dependency `mime` has been updated to address a [vulnerability](https://npmjs.com/advisories/535), but this issue does not impact Express.
  - The dependency `send` has been updated to provide a protection against a [Node.js 8.5.0 vulnerability](https://nodejs.org/en/blog/vulnerability/september-2017-path-validation/). This only impacts running Express on the specific Node.js version 8.5.0.
- 4.15.5
  - The dependency `debug` has been updated to address a [vulnerability](https://snyk.io/vuln/npm:debug:20170905), but this issue does not impact Express.
  - The dependency `fresh` has been updated to address a [vulnerability](https://npmjs.com/advisories/526). This will affect your application if the following APIs are used: `express.static`, `req.fresh`, `res.json`, `res.jsonp`, `res.send`, `res.sendfile` `res.sendFile`, `res.sendStatus`.
- 4.15.3
  - The dependency `ms` has been updated to address a [vulnerability](https://snyk.io/vuln/npm:ms:20170412). This may affect your application if untrusted string input is passed to the `maxAge` option in the following APIs: `express.static`, `res.sendfile`, and `res.sendFile`.
- 4.15.2
  - The dependency `qs` has been updated to address a [vulnerability](https://snyk.io/vuln/npm:qs:20170213), but this issue does not impact Express. Updating to 4.15.2 is a good practice, but not required to address the vulnerability.
- 4.11.1
  - 修复了 `express.static`、`res.sendfile` 和 `res.sendFile` 中的根路径披露漏洞
- 4.10.7
  - 在 `express.static`（[公告](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)）中修复了开放重定向漏洞。
- 4.8.8
  - 在 `express.static`（[公告](http://npmjs.com/advisories/32)、[CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394)）中修复了目录遍历漏洞。
- 4.8.4
  - Node.js 0.10 在某些情况下可能会泄漏 `fd`，这会影响 `express.static` 和 `res.sendfile`。恶意请求会导致 `fd` 泄漏并最终导致 `EMFILE` 错误和服务器无响应。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 4.8.0
  - 查询字符串中具有极高数量索引的稀疏数组会导致进程耗尽内存并使服务器崩溃。
  - 极端嵌套查询字符串对象会导致进程阻塞并使服务器暂时无响应。

## 3.x

**Express 3.x 不再受到维护**

Known and unknown security and performance issues in 3.x have not been addressed since the last update (1 August, 2015). It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/zh-cn/support#commercial-support-options).

- 3.19.1
  - 修复了 `express.static`、`res.sendfile` 和 `res.sendFile` 中的根路径披露漏洞
- 3.19.0
  - 在 `express.static`（[公告](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)）中修复了开放重定向漏洞。
- 3.16.10
  - 在 `express.static` 中修复了目录遍历漏洞。
- 3.16.6
  - Node.js 0.10 在某些情况下可能会泄漏 `fd`，这会影响 `express.static` 和 `res.sendfile`。恶意请求会导致 `fd` 泄漏并最终导致 `EMFILE` 错误和服务器无响应。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 3.16.0
  - 查询字符串中具有极高数量索引的稀疏数组会导致进程耗尽内存并使服务器崩溃。
  - 极端嵌套查询字符串对象会导致进程阻塞并使服务器暂时无响应。
- 3.3.0
  - 不受支持的方法覆盖尝试的 404 响应易于受到跨站点脚本编制攻击。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-cn/advanced/security-updates.md          )
