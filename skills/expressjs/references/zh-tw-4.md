# 正式作業最佳作法：效能和可靠性 and more

# 正式作業最佳作法：效能和可靠性

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# 正式作業最佳作法：效能和可靠性

本文討論部署至正式作業之 Express 應用程式的效能與可靠性最佳作法。

This topic clearly falls into the “devops” world, spanning both traditional development and operations. Accordingly, the information is divided into two parts:

- Things to do in your code (the dev part):
  - 採用 gzip 壓縮
  - [Don’t use synchronous functions](#dont-use-synchronous-functions)
  - [Do logging correctly](#do-logging-correctly)
  - [Handle exceptions properly](#handle-exceptions-properly)
- Things to do in your environment / setup (the ops part):
  - 將 NODE_ENV 設為 “production”
  - 確定您的應用程式自動重新啟動
  - [Run your app in a cluster](#run-your-app-in-a-cluster)
  - [Cache request results](#cache-request-results)
  - 負載平衡器通常是一個反向 Proxy，負責協調與多個應用程式實例和伺服器之間的資料流量。利用 [Nginx](http://nginx.org/en/docs/http/load_balancing.html) 或 [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts)，就能輕鬆設定您應用程式的負載平衡器。
  - 反向 Proxy 位於 Web 應用程式前面，除了將要求引導至應用程式，也會對要求執行支援的作業。除此之外，它還可以處理錯誤頁面、壓縮、快取、提供的檔案，以及負載平衡。

## Things to do in your code

以下是您可以在程式碼中執行的一些作法，藉以改良您應用程式的效能：

- 採用 gzip 壓縮
- [Don’t use synchronous functions](#dont-use-synchronous-functions)
- [Do logging correctly](#do-logging-correctly)
- [Handle exceptions properly](#handle-exceptions-properly)

### 採用 gzip 壓縮

Gzip compressing can greatly decrease the size of the response body and hence increase the speed of a web app. Use the [compression](https://www.npmjs.com/package/compression) middleware for gzip compression in your Express app. For example:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

For a high-traffic website in production, the best way to put compression in place is to implement it at a reverse proxy level (see [Use a reverse proxy](#use-a-reverse-proxy)). In that case, you do not need to use compression middleware. 在正式作業中，如果網站的資料流量極高，落實執行壓縮最好的作法是在反向 Proxy 層次實作它（請參閱[使用反向 Proxy](#proxy)）。在該情況下，就不需使用壓縮中介軟體。如需在 Nginx 中啟用 gzip 壓縮的詳細資料，請參閱 Nginx 說明文件中的 [ngx_http_gzip_module 模組](http://nginx.org/en/docs/http/ngx_http_gzip_module.html)。

### 不使用同步函數

Synchronous functions and methods tie up the executing process until they return. A single call to a synchronous function might return in a few microseconds or milliseconds, however in high-traffic websites, these calls add up and reduce the performance of the app. Avoid their use in production.

雖然 Node 和許多模組會提供其函數的同步與非同步版本，在正式作業中，請一律使用非同步版本。唯一有理由使用同步函數的時機是在最初啟動之時。 The only time when a synchronous function can be justified is upon initial startup.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Of course, you wouldn’t want to use this in production, but rather to ensure that your code is ready for production. See the [node command-line options documentation](https://nodejs.org/api/cli.html#cli_trace_sync_io) for more information.

### Do logging correctly

In general, there are two reasons for logging from your app: For debugging and for logging app activity (essentially, everything else). Using `console.log()` or `console.error()` to print log messages to the terminal is common practice in development. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### For debugging

如果您為了除錯而記載，則不要使用 `console.log()`，請改用 [debug](https://www.npmjs.com/package/debug) 之類的特殊除錯模組。這個模組可讓您使用 DEBUG 環境變數，來控制哪些除錯訊息（若有的話）要送往 `console.err()`。為了讓應用程式完全維持非同步，您仍得將 `console.err()` 引導至另一個程式。但之後在正式作業中，實際上您並不會進行除錯，不是嗎？ This module enables you to use the DEBUG environment variable to control what debug messages are sent to `console.error()`, if any. To keep your app purely asynchronous, you’d still want to pipe `console.error()` to another program. But then, you’re not really going to debug in production, are you?

#### 為了應用程式活動

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Handle exceptions properly

Node apps crash when they encounter an uncaught exception. Not handling exceptions and taking appropriate actions will make your Express app crash and go offline. If you follow the advice in [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts) below, then your app will recover from a crash. Fortunately, Express apps typically have a short startup time. Nevertheless, you want to avoid crashing in the first place, and to do that, you need to handle exceptions properly.

為了確保您能處理所有的異常狀況，請使用下列技術：

- [使用 try-catch](#try-catch)
- [使用 promise](#promises)

Before diving into these topics, you should have a basic understanding of Node/Express error handling: using error-first callbacks, and propagating errors in middleware. Node uses an “error-first callback” convention for returning errors from asynchronous functions, where the first parameter to the callback function is the error object, followed by result data in succeeding parameters. To indicate no error, pass null as the first parameter. The callback function must correspondingly follow the error-first callback convention to meaningfully handle the error. And in Express, the best practice is to use the next() function to propagate errors through the middleware chain.

如需進一步瞭解錯誤處理的基本概念，請參閱：

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### 使用 try-catch

try-catch 是一種 JavaScript 語言建構，可用來捕捉同步程式碼中的異常狀況。例如，如以下所示，利用 try-catch 來處理 JSON 剖析錯誤。 Use try-catch, for example, to handle JSON parsing errors as shown below.

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

However, try-catch works only for synchronous code. 不過，try-catch 只適用於同步程式碼。由於 Node 平台主要是非同步（尤其是在正式作業環境），try-catch 不會捕捉大量的異常狀況。

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

One thing you should *not* do is to listen for the `uncaughtException` event, emitted when an exception bubbles all the way back to the event loop. Adding an event listener for `uncaughtException` will change the default behavior of the process that is encountering an exception; the process will continue to run despite the exception. This might sound like a good way of preventing your app from crashing, but continuing to run the app after an uncaught exception is a dangerous practice and is not recommended, because the state of the process becomes unreliable and unpredictable.

此外，使用 `uncaughtException` 被公認為[拙劣作法](https://nodejs.org/api/process.html#process_event_uncaughtexception)，這裡有一份[提案](https://github.com/nodejs/node-v0.x-archive/issues/2582)，指出如何將它從核心移除。因此，接聽 `uncaughtException` 並不可取。這是我們建議採取多重程序和監督程式等事項的原因：當機再重新啟動，通常是從錯誤回復最可靠的作法。 So listening for `uncaughtException` is just a bad idea. This is why we recommend things like multiple processes and supervisors: crashing and restarting is often the most reliable way to recover from an error.

我們也不建議使用 [domains](https://nodejs.org/api/domain.html)。它通常不能解決問題，並且是個已淘汰的模組。 It generally doesn’t solve the problem and is a deprecated module.

## 在環境 / 設定中的作法

以下是您可以在系統環境中執行的一些作法，藉以改良您應用程式的效能：

- 將 NODE_ENV 設為 “production”
- 確定您的應用程式自動重新啟動
- [Run your app in a cluster](#run-your-app-in-a-cluster)
- [Cache request results](#cache-request-results)
- 負載平衡器通常是一個反向 Proxy，負責協調與多個應用程式實例和伺服器之間的資料流量。利用 [Nginx](http://nginx.org/en/docs/http/load_balancing.html) 或 [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts)，就能輕鬆設定您應用程式的負載平衡器。
- 反向 Proxy 位於 Web 應用程式前面，除了將要求引導至應用程式，也會對要求執行支援的作業。除此之外，它還可以處理錯誤頁面、壓縮、快取、提供的檔案，以及負載平衡。

### 將 NODE_ENV 設為 “production”

The NODE_ENV environment variable specifies the environment in which an application is running (usually, development or production). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

將 NODE_ENV 設為 “production”，可讓 Express：

- Cache view templates.
- 快取從 CSS 延伸項目產生的 CSS 檔案。
- Generate less verbose error messages.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

如果您需要撰寫環境特定的程式碼，您可以使用 `process.env.NODE_ENV` 來檢查 NODE_ENV 的值。請注意，檢查任何環境變數的值都會影響效能，因此請慎行。 Be aware that checking the value of any environment variable incurs a performance penalty, and so should be done sparingly.

In development, you typically set environment variables in your interactive shell, for example by using `export` or your `.bash_profile` file. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). The next section provides more details about using your init system in general, but setting `NODE_ENV` is so important for performance (and easy to do), that it’s highlighted here.

採用 systemd 時，請在單位檔案中使用 `Environment` 指引。例如： For example:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### 確定您的應用程式自動重新啟動

In production, you don’t want your application to be offline, ever. This means you need to make sure it restarts both if the app crashes and if the server itself crashes. Although you hope that neither of those events occurs, realistically you must account for both eventualities by:

- 當應用程式（和 Node）當機時，使用程序管理程式重新啟動它。
- Using the init system provided by your OS to restart the process manager when the OS crashes. It’s also possible to use the init system without a process manager.

Node applications crash if they encounter an uncaught exception. The foremost thing you need to do is to ensure your app is well-tested and handles all exceptions (see [handle exceptions properly](#handle-exceptions-properly) for details). But as a fail-safe, put a mechanism in place to ensure that if and when your app crashes, it will automatically restart.

#### 使用程序管理程式

在開發中，只需從指令行使用 `node server.js` 或類似指令，就會啟動應用程式。但在正式作業中這樣做，卻會成為禍因。如果應用程式當機，就會離線直到您重新啟動它為止。為了確保應用程式會在當機時重新啟動，請使用程序管理程式。程序管理程式是一個應用程式的「儲存器」，有助於部署、提供高可用性，並可讓您在執行時期管理應用程式。 But doing this in production is a recipe for disaster. If the app crashes, it will be offline until you restart it. To ensure your app restarts if it crashes, use a process manager. A process manager is a “container” for applications that facilitates deployment, provides high availability, and enables you to manage the application at runtime.

除了在應用程式當機時重新啟動它，程序管理程式還可讓您：

- 洞察執行時期效能和資源的耗用情況。
- 動態修改設定，以改良效能。
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### 使用 init 系統

The next layer of reliability is to ensure that your app restarts when the server restarts. Systems can still go down for a variety of reasons. To ensure that your app restarts if the server crashes, use the init system built into your OS. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

init 系統若要與 Express 應用程式搭配使用，其作法有二：

- Run your app in a process manager, and install the process manager as a service with the init system. The process manager will restart your app when the app crashes, and the init system will restart the process manager when the OS restarts. This is the recommended approach.
- Run your app (and Node) directly with the init system. This is somewhat simpler, but you don’t get the additional advantages of using a process manager.

##### Systemd

Systemd 是一個 Linux 系統和服務管理程式。大部分主要的 Linux 發行套件已採用 systemd 作為其預設 init 系統。 Most major Linux distributions have adopted systemd as their default init system.

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

如需 systemd 的相關資訊，請參閱 [systemd 參照（線上指令說明）](http://www.freedesktop.org/software/systemd/man/systemd.unit.html)。

### Run your app in a cluster

In a multi-core system, you can increase the performance of a Node app by many times by launching a cluster of processes. A cluster runs multiple instances of the app, ideally one instance on each CPU core, thereby distributing the load and tasks among the instances.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANT: Since the app instances run as separate processes, they do not share the same memory space. That is, objects are local to each instance of the app. Therefore, you cannot maintain state in the application code. However, you can use an in-memory datastore like [Redis](http://redis.io/) to store session-related data and state. This caveat applies to essentially all forms of horizontal scaling, whether clustering with multiple processes or multiple physical servers.

In clustered apps, worker processes can crash individually without affecting the rest of the processes. Apart from performance advantages, failure isolation is another reason to run a cluster of app processes. Whenever a worker process crashes, always make sure to log the event and spawn a new process using cluster.fork().

#### 使用 Node 的叢集模組

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

### 快取要求結果

在正式作業中改良效能的另一項策略是快取要求的結果，這樣您的應用程式就不會重複執行作業而反覆處理相同的要求。

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### 使用負載平衡器

No matter how optimized an app is, a single instance can handle only a limited amount of load and traffic. One way to scale an app is to run multiple instances of it and distribute the traffic via a load balancer. Setting up a load balancer can improve your app’s performance and speed, and enable it to scale more than is possible with a single instance.

A load balancer is usually a reverse proxy that orchestrates traffic to and from multiple application instances and servers. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

With load balancing, you might have to ensure that requests that are associated with a particular session ID connect to the process that originated them. This is known as *session affinity*, or *sticky sessions*, and may be addressed by the suggestion above to use a data store such as Redis for session data (depending on your application). For a discussion, see [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### 使用反向 Proxy

A reverse proxy sits in front of a web app and performs supporting operations on the requests, apart from directing requests to the app. It can handle error pages, compression, caching, serving files, and load balancing among other things.

Handing over tasks that do not require knowledge of application state to a reverse proxy frees up Express to perform specialized application tasks. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/advanced/best-practice-performance.md          )

---

# 正式作業最佳作法：安全

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# 正式作業最佳作法：安全

## 概觀

The term *“production”* refers to the stage in the software lifecycle when an application or API is generally available to its end-users or consumers. In contrast, in the *“development”* stage, you’re still actively writing and testing code, and the application is not open to external access. The corresponding system environments are known as *production* and *development* environments, respectively.

Development and production environments are usually set up differently and have vastly different requirements. What’s fine in development may not be acceptable in production. For example, in a development environment you may want verbose logging of errors for debugging, while the same behavior can become a security concern in a production environment. And in development, you don’t need to worry about scalability, reliability, and performance, while those concerns become critical in production.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

Security best practices for Express applications in production include:

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - 您可能熟悉 Secure Socket Layer (SSL) 加密。[TLS 就是 SSL 後繼的演進](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx)。換句話說，如果您之前使用 SSL，請考量升級至 TLS。一般而言，我們建議由 Nginx 來處理 TLS。如需有關在 Nginx（和其他伺服器）上配置 TLS 的適當參考資料，請參閱 [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations)。
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [hidePoweredBy](https://github.com/helmetjs/hide-powered-by) 會移除 `X-Powered-By` 標頭。
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - `domain` - 指出 Cookie 的網域；用來與發出 URL 要求之伺服器的網域相互比較。如果相符，接著會檢查路徑屬性。
    - 相對地，[cookie-session](https://www.npmjs.com/package/cookie-session) 中介軟體會實作以 Cookie 為基礎的儲存體：它會將整個階段作業序列化為 Cookie，而非只是一個階段作業金鑰。只有在階段作業資料相對較小，且易於編碼成基本值（而非物件）時，才使用此項。雖然瀏覽器對於每個 Cookie 理應可以支援至少
      4096 個位元組，為了確保您不會超出限制，對於每一個網域，請勿超過 4093 個位元組大小。此外要留意的是，用戶端可以看見 Cookie 資料，因此，若有任何原因需要保護該資料的安全或加以遮蔽，最好選擇 express-session。
    - 使用預設階段作業 Cookie 名稱可能開放您的應用程式遭受攻擊。引發的安全問題類似於 `X-Powered-By`：潛在的攻擊者可能用它來對伺服器進行指紋辨識，從而發動目標攻擊。
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - 最後，如同其他任何的 Web 應用程式，Express 應用程式仍可能遭到各種 Web 型攻擊。請多加熟悉已知的 [Web 漏洞](https://www.owasp.org/www-project-top-ten/)，並採取預防措施，來避免這些攻擊。
  - [Additional considerations](#additional-considerations)

## 請勿使用已淘汰或有漏洞的 Express 版本

Express 2.x and 3.x are no longer maintained. Security and performance issues in these versions won’t be fixed. Do not use them! If you haven’t moved to version 4, follow the [migration guide](https://expressjs.com/zh-tw/guide/migrating-4.html) or consider [Commercial Support Options](https://expressjs.com/zh-tw/support#commercial-support-options).

另請確定您沒有使用[「安全更新」頁面](https://expressjs.com/zh-tw/advanced/security-updates.html)中列出的任何有漏洞的 Express 版本。若有使用，請更新為其中一個穩定版本，最好是最新版本。 If you are, update to one of the stable releases, preferably the latest.

## 使用 TLS

If your app deals with or transmits sensitive data, use [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) to secure the connection and the data. This technology encrypts data before it is sent from the client to the server, thus preventing some common (and easy) hacks. Although Ajax and POST requests might not be visibly obvious and seem “hidden” in browsers, their network traffic is vulnerable to [packet sniffing](https://en.wikipedia.org/wiki/Packet_analyzer) and [man-in-the-middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

You may be familiar with Secure Socket Layer (SSL) encryption. [TLS is simply the next progression of SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). In other words, if you were using SSL before, consider upgrading to TLS. In general, we recommend Nginx to handle TLS. For a good reference to configure TLS on Nginx (and other servers), see [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

此外，可方便您取得免費 TLS 憑證的工具是 [Let’s Encrypt](https://letsencrypt.org/about/)，這是一個免費的自動化開放憑證管理中心 (CA)，由 [Internet Security Research Group (ISRG)](https://letsencrypt.org/isrg/) 提供。

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

[Helmet](https://www.npmjs.com/package/helmet) 會適當設定 HTTP 標頭，有助於防範您的應用程式出現已知的 Web 漏洞。

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/zh-tw/advanced/如果您使用 `helmet.js`，自會為您處理此事。).

安裝 Helmet 等之類的其他任何模組：

```
$ npm install helmet
```

然後在您的程式碼中使用它：

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

## 安全地使用 Cookie

為了確保 Cookie 不會開啟您的應用程式進行惡意探索，請勿使用預設階段作業 Cookie 名稱，並適當設定 Cookie 安全選項。

以下是兩個主要的中介軟體 Cookie 階段作業模組：

- [express-session](https://www.npmjs.com/package/express-session)，取代了 Express 3.x 內建的 `express.session` 中介軟體。
- [cookie-session](https://www.npmjs.com/package/cookie-session)，取代了 Express 3.x 內建的 `express.cookieSession` 中介軟體。

這兩個模組之間的主要差異是它們儲存 Cookie 階段作業資料的方式。[express-session](https://www.npmjs.com/package/express-session) 中介軟體會將階段作業資料儲存在伺服器上；
它只將階段作業 ID（而非階段作業資料）儲存在 Cookie 本身中。依預設，它使用記憶體內儲存體，且並非設計成用於正式作業環境。在正式作業中，您需要設定可調式階段作業儲存庫；
請參閱[相容的階段作業儲存庫](https://github.com/expressjs/session#compatible-session-stores)清單。 The [express-session](https://www.npmjs.com/package/express-session) middleware stores session data on the server; it only saves the session ID in the cookie itself, not session data. By default, it uses in-memory storage and is not designed for a production environment. In production, you’ll need to set up a scalable session-store; see the list of [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

In contrast, [cookie-session](https://www.npmjs.com/package/cookie-session) middleware implements cookie-backed storage: it serializes the entire session to the cookie, rather than just a session key. Only use it when session data is relatively small and easily encoded as primitive values (rather than objects). Although browsers are supposed to support at least 4096 bytes per cookie, to ensure you don’t exceed the limit, don’t exceed a size of 4093 bytes per domain. Also, be aware that the cookie data will be visible to the client, so if there is any reason to keep it secure or obscure, then `express-session` may be a better choice.

### 請勿使用預設階段作業 Cookie 名稱

Using the default session cookie name can open your app to attacks. The security issue posed is similar to `X-Powered-By`: a potential attacker can use it to fingerprint the server and target attacks accordingly.

為了避免發生此問題，請使用通用 Cookie 名稱；
例如，使用 [express-session](https://www.npmjs.com/package/express-session) 中介軟體：

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### 設定 Cookie 安全選項

設定下列 Cookie 選項來加強安全：

- `secure` - 確保瀏覽器只透過 HTTPS 傳送 Cookie。
- `httpOnly` - 確保只透過 HTTP(S) 傳送 Cookie，而不透過用戶端 JavaScript 傳送，如此有助於防範跨網站 Scripting 攻擊。
- `domain` - indicates the domain of the cookie; use it to compare against the domain of the server in which the URL is being requested. If they match, then check the path attribute next.
- `path` - 指出 Cookie 的路徑；用來與要求路徑相互比較。如果此項與網域相符，則會傳送要求中的 Cookie。 If this and domain match, then send the cookie in the request.
- `expires` - 用來設定持續性 Cookie 的到期日。

下列範例使用 [cookie-session](https://www.npmjs.com/package/cookie-session) 中介軟體：

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

Keep an eye out for [Node Security Project](https://npmjs.com/advisories) or [Snyk](https://snyk.io/vuln/) advisories that may affect Express or other modules that your app uses. In general, these databases are excellent resources for knowledge and tools about Node security.

Finally, Express apps—like any other web apps—can be vulnerable to a variety of web-based attacks. Familiarize yourself with known [web vulnerabilities](https://www.owasp.org/www-project-top-ten/) and take precautions to avoid them.

## 其他注意事項

以下是優異的 [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/) 所提供的進一步建議。如需這些建議的所有詳細資料，請參閱該部落格文章： Refer to that blog post for all the details on these recommendations:

- 一律對使用者輸入進行過濾和消毒，來防範跨網站 Scripting (XSS) 和指令注入攻擊。
- 使用參數化查詢或備妥陳述式，來防禦 SQL 注入攻擊。
- 使用開放程式碼 [sqlmap](http://sqlmap.org/) 工具，來偵測您應用程式中的 SQL 注入漏洞。
- 使用 [nmap](https://nmap.org/) 和 [sslyze](https://github.com/nabla-c0d3/sslyze) 工具，來測試您 SSL 密碼、金鑰和重新協議的配置，以及測試您憑證的有效性。
- 使用 [safe-regex](https://www.npmjs.com/package/safe-regex)，確定您的正規表示式不易受到[正規表示式阻斷服務](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS)攻擊。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/advanced/best-practice-security.md          )

---

# 開發 Express 範本引擎

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# 開發 Express 範本引擎

利用 `app.engine(ext, callback)` 方法，來建立您自己的範本引擎。`ext` 是指副檔名，`callback` 是範本引擎函數，它可接受下列項目作為參數：檔案的位置、options 物件，以及回呼函數。 `ext` refers to the file extension, and `callback` is the template engine function, which accepts the following items as parameters: the location of the file, the options object, and the callback function.

下列程式碼範例說明如何實作一個相當簡單的範本引擎，以呈現 `.ntl` 檔。

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

Your app will now be able to render `.ntl` files. 現在，您的應用程式能夠呈現 `.ntl` 檔。請在 `views` 目錄中建立一個名稱是 `index.ntl` 的檔案，內含下列內容。

```pug
#title#
#message#
```

Then, create the following route in your app.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

當您向首頁提出要求時，`index.ntl` 會呈現成 HTML。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### 範例

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/advanced/healthcheck-graceful-shutdown.md          )

---

# 安全更新

> Review the latest security updates and patches for Express.js, including detailed vulnerability lists for different versions to help maintain a secure application.

# 安全更新

Node.js 的漏洞會直接影響 Express。因此，請[隨時監看 Node.js 漏洞](https://nodejs.org
/en/blog/vulnerability/)，並確保您所用的是最新的 Node.js 穩定版本。
 Therefore, [keep a watch on Node.js vulnerabilities](https://nodejs.org/en/blog/vulnerability/) and make sure you are using the latest stable version of Node.js.

以下列舉已在指定的版本更新中修正的 Express 漏洞。

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/zh-tw/resources/contributing.html#security-policies-and-procedures).

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
  - 已修正 `express.static`、`res.sendfile` 和 `res.sendFile` 中的根路徑揭露漏洞
- 4.10.7
  - 已修正 `express.static`（[諮詢](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)）中的開放重新導向漏洞。
- 4.8.8
  - 已修正 `express.static`（[諮詢](http://npmjs.com/advisories/32)、[CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394)）中的目錄遍訪漏洞。
- 4.8.4
  - 在某些情況下，Node.js 0.10 可能洩漏 `fd`，而影響 `express.static` 和 `res.sendfile`。惡意的要求可能造成 `fd` 洩漏，最後導致 `EMFILE` 錯誤和伺服器無回應。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 4.8.0
  - 如果稀疏陣列在查詢字串中的索引過多，可能導致程序耗盡記憶體，而使伺服器當機。
  - Extremely nested query string objects could cause the process to block and make the server unresponsive temporarily.

## 3.x

**Express 3.x 已不再維護**

Known and unknown security and performance issues in 3.x have not been addressed since the last update (1 August, 2015). It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/zh-tw/support#commercial-support-options).

- 3.19.1
  - 已修正 `express.static`、`res.sendfile` 和 `res.sendFile` 中的根路徑揭露漏洞
- 3.19.0
  - 已修正 `express.static`（[諮詢](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)）中的開放重新導向漏洞。
- 3.16.10
  - 已修正 `express.static` 中的目錄遍訪漏洞。
- 3.16.6
  - 在某些情況下，Node.js 0.10 可能洩漏 `fd`，而影響 `express.static` 和 `res.sendfile`。惡意的要求可能造成 `fd` 洩漏，最後導致 `EMFILE` 錯誤和伺服器無回應。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 3.16.0
  - 如果稀疏陣列在查詢字串中的索引過多，可能導致程序耗盡記憶體，而使伺服器當機。
  - Extremely nested query string objects could cause the process to block and make the server unresponsive temporarily.
- 3.3.0
  - 404 回應（試圖進行不支援的方法置換）容易受到跨網站 Scripting 攻擊。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/zh-tw/advanced/security-updates.md          )
