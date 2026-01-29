# 実稼働環境におけるベスト・プラクティス: パフォーマンスと信頼性 and more

# 実稼働環境におけるベスト・プラクティス: パフォーマンスと信頼性

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# 実稼働環境におけるベスト・プラクティス: パフォーマンスと信頼性

この記事では、実稼働環境にデプロイされた Express アプリケーションのパフォーマンスと信頼性に関するベスト・プラクティスについて説明します。

This topic clearly falls into the “devops” world, spanning both traditional development and operations. Accordingly, the information is divided into two parts:

- コードで実行する処理 (開発部分)
  - [gzip 圧縮を使用する](#use-gzip-compression)
  - [同期関数を使用しない](#dont-use-synchronous-functions)
  - [ロギングを正確に実行する](#do-logging-correctly)
  - [例外を適切に処理する](#handle-exceptions-properly)
- 環境/セットアップで実行する処理 (運用部分)
  - [Set NODE_ENV to “production”](#set-node_env-to-production)
  - [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts)
  - [Run your app in a cluster](#run-your-app-in-a-cluster)
  - [Cache request results](#cache-request-results)
  - [Use a load balancer](#use-a-load-balancer)
  - [Use a reverse proxy](#use-a-reverse-proxy)

## コードで実行する処理

以下に、アプリケーションのパフォーマンスを向上させるためにコードで実行できる処理をいくつか挙げます。

- [gzip 圧縮を使用する](#use-gzip-compression)
- [同期関数を使用しない](#dont-use-synchronous-functions)
- [ロギングを正確に実行する](#do-logging-correctly)
- [例外を適切に処理する](#handle-exceptions-properly)

### gzip 圧縮を使用する

Gzip compressing can greatly decrease the size of the response body and hence increase the speed of a web app. Gzip 圧縮により、応答本体のサイズを大幅に縮小できるため、Web アプリケーションの速度が高くなります。Express アプリケーションで gzip 圧縮として [compression](https://www.npmjs.com/package/compression) ミドルウェアを使用してください。次に例を示します。 For example:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

For a high-traffic website in production, the best way to put compression in place is to implement it at a reverse proxy level (see [Use a reverse proxy](#use-a-reverse-proxy)). In that case, you do not need to use compression middleware. トラフィックが多い実稼働環境の Web サイトでは、圧縮を適用する最適な方法は、リバース・プロキシー・レベルで実装することです ([リバース・プロキシーの使用](#proxy)を参照)。その場合は、compression ミドルウェアを使用する必要はありません。Nginx で gzip 圧縮を有効にする方法について詳しくは、Nginx 資料の [Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) を参照してください。

### 同期関数を使用しない

同期の関数とメソッドは、返されるまで実行中のプロセスを結合します。同期関数に対する 1 回の呼び出しは数マイクロ秒から数ミリ秒で返される可能性がありますが、トラフィックが多い Web サイトでは、これらの呼び出しを合計すると、アプリケーションのパフォーマンスが低下します。実稼働環境では、これらを使用しないでください。 A single call to a synchronous function might return in a few microseconds or milliseconds, however in high-traffic websites, these calls add up and reduce the performance of the app. Avoid their use in production.

ノードおよび多くのモジュールは、同期版と非同期版の関数を提供していますが、実稼働環境では必ず非同期版を使用してください。同期関数を使用しても構わないのは、初期始動時のみです。 The only time when a synchronous function can be justified is upon initial startup.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Of course, you wouldn’t want to use this in production, but rather to ensure that your code is ready for production. See the [node command-line options documentation](https://nodejs.org/api/cli.html#cli_trace_sync_io) for more information.

### ロギングを正確に実行する

In general, there are two reasons for logging from your app: For debugging and for logging app activity (essentially, everything else). Using `console.log()` or `console.error()` to print log messages to the terminal is common practice in development. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### For debugging

デバッグの目的でロギングを実行する場合は、`console.log()` を使用するのではなく、[debug](https://www.npmjs.com/package/debug) などの特殊なデバッグ・モジュールを使用します。このモジュールでは、DEBUG 環境変数を使用して、`console.err()` に送信されるデバッグ・メッセージを制御できます。アプリケーションを純粋に非同期的にしておくために、`console.err()` を別のプログラムにパイプ接続することもできます。しかし、実稼働環境ではデバッグを実行することはお勧めしません。 This module enables you to use the DEBUG environment variable to control what debug messages are sent to `console.error()`, if any. To keep your app purely asynchronous, you’d still want to pipe `console.error()` to another program. But then, you’re not really going to debug in production, are you?

#### アプリケーション・アクティビティー

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### 例外を適切に処理する

Node apps crash when they encounter an uncaught exception. Not handling exceptions and taking appropriate actions will make your Express app crash and go offline. [アプリケーションが確実に自動再始動するようにする](#ensure-your-app-automatically-restarts) Fortunately, Express apps typically have a short startup time. Nevertheless, you want to avoid crashing in the first place, and to do that, you need to handle exceptions properly.

確実にすべての例外を処理するには、以下の技法を使用します。

- [Try-catch の使用](#try-catch)
- [Promise の使用](#promises)

Before diving into these topics, you should have a basic understanding of Node/Express error handling: using error-first callbacks, and propagating errors in middleware. 上記のトピックを読む前に、error-first コールバックの使用と、ミドルウェアへのエラーの伝搬という Node/Express エラー処理の基礎を理解しておく必要があります。Node は、非同期関数からエラーを返すために「error-first コールバック」という規則を使用します。この場合、コールバック関数への最初のパラメーターがエラー・オブジェクトで、その後に続くパラメーターに結果データがあります。エラーがないことを示すには、最初のパラメーターとして `null` を渡します。コールバック関数は、エラーを有意に処理するには、error-first コールバック規則に対応して従う必要があります。Express におけるベスト・プラクティスは、next() 関数を使用して、ミドルウェア・チェーンを介してエラーを伝搬することです。 To indicate no error, pass null as the first parameter. The callback function must correspondingly follow the error-first callback convention to meaningfully handle the error. And in Express, the best practice is to use the next() function to propagate errors through the middleware chain.

エラー処理のその他の基礎については、下記を参照してください。

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Try-catch の使用

Try-catch は、同期コードで例外をキャッチするために使用できる JavaScript 言語構造体です。Try-catch は、例えば、下記のように JSON 構文解析エラーを処理するために使用します。 Use try-catch, for example, to handle JSON parsing errors as shown below.

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

However, try-catch works only for synchronous code. ただし、Try-catch は同期コードでのみ機能します。Node プラットフォームは主に (特に実稼働環境で) 非同期的であるため、Try-catch は多くの例外をキャッチしません。

#### Promise の使用

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

#### 実行してはならないこと

One thing you should *not* do is to listen for the `uncaughtException` event, emitted when an exception bubbles all the way back to the event loop. Adding an event listener for `uncaughtException` will change the default behavior of the process that is encountering an exception; the process will continue to run despite the exception. This might sound like a good way of preventing your app from crashing, but continuing to run the app after an uncaught exception is a dangerous practice and is not recommended, because the state of the process becomes unreliable and unpredictable.

さらに、`uncaughtException` の使用は、正式に[粗雑なもの](https://nodejs.org/api/process.html#process_event_uncaughtexception)として認められており、これをコアから削除するための[提案](https://github.com/nodejs/node-v0.x-archive/issues/2582)が出されています。したがって、`uncaughtException` を listen するのは悪い方法です。この理由から複数のプロセスとスーパーバイザーなどの使用をお勧めしています。異常終了と再始動は、場合によってはエラーから復旧するための最も信頼できる方法となります。 So listening for `uncaughtException` is just a bad idea. This is why we recommend things like multiple processes and supervisors: crashing and restarting is often the most reliable way to recover from an error.

また、[domain](https://nodejs.org/api/domain.html) の使用もお勧めしません。このモジュールは概して問題を解決しないため、推奨されていません。 It generally doesn’t solve the problem and is a deprecated module.

## 環境/セットアップで実行する処理

以下に、アプリケーションのパフォーマンスを向上させるためにシステム環境で実行できる処理をいくつか挙げます。

- [Set NODE_ENV to “production”](#set-node_env-to-production)
- [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts)
- [Run your app in a cluster](#run-your-app-in-a-cluster)
- [Cache request results](#cache-request-results)
- [Use a load balancer](#use-a-load-balancer)
- [Use a reverse proxy](#use-a-reverse-proxy)

### NODE_ENV を「production」に設定する

NODE_ENV 環境変数は、アプリケーションが実行される環境 (通常は開発または実稼働) を指定します。パフォーマンスを向上させるために実行できる最も単純な処理の 1 つは、NODE_ENV を「production」に設定することです。 One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

NODE_ENV を「production」に設定すると、Express は次のようになります。

- ビュー・テンプレートをキャッシュに入れる。
- CSS 拡張から生成された CSS ファイルをキャッシュに入れる。
- 詳細度の低いエラー・メッセージを生成する。

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

環境固有のコードを作成する必要がある場合は、`process.env.NODE_ENV` を使用して NODE_ENV の値を確認できます。どの環境変数の値を確認する場合でもパフォーマンスに悪影響が及ぶため、慎重に行ってください。 Be aware that checking the value of any environment variable incurs a performance penalty, and so should be done sparingly.

開発環境では、通常、対話式シェルで環境変数を設定します。例えば、`export` または `.bash_profile` ファイルを使用します。しかし、一般的には実動サーバーではそうしません。代わりに、OS の init システム (systemd または Upstart) を使用します。次のセクションでは、init システムの一般的な使用法について詳しく説明しています。ここで重点的に説明したのは、NODE_ENV の設定がパフォーマンスにとって極めて重要であるため (かつ簡単に実行できるため) です。 But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). The next section provides more details about using your init system in general, but setting `NODE_ENV` is so important for performance (and easy to do), that it’s highlighted here.

systemd では、unit ファイルで `Environment` ディレクティブを使用します。次に例を示します。 For example:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### アプリケーションが確実に自動再始動するようにする

In production, you don’t want your application to be offline, ever. This means you need to make sure it restarts both if the app crashes and if the server itself crashes. Although you hope that neither of those events occurs, realistically you must account for both eventualities by:

- アプリケーション (および Node) が異常終了した場合にプロセス・マネージャーを使用してそれらを再始動する。
- Using the init system provided by your OS to restart the process manager when the OS crashes. It’s also possible to use the init system without a process manager.

Node applications crash if they encounter an uncaught exception. The foremost thing you need to do is to ensure your app is well-tested and handles all exceptions (see [handle exceptions properly](#handle-exceptions-properly) for details). But as a fail-safe, put a mechanism in place to ensure that if and when your app crashes, it will automatically restart.

#### プロセス・マネージャーを使用する

開発環境では、単にコマンド・ラインから `node server.js` などを使用してアプリケーションを開始しています。ただし、この方法を実稼働環境で実行すると、危険を招くことになります。アプリケーションが異常終了した場合、アプリケーションは再始動されるまでオフラインになります。アプリケーションが異常終了した場合に確実に再始動するようにするには、プロセス・マネージャーを使用します。プロセス・マネージャーは、デプロイメントを容易に行えるようにして、高可用性を実現し、アプリケーションを実行時に管理できるようにする、アプリケーションの「コンテナー」です。 But doing this in production is a recipe for disaster. If the app crashes, it will be offline until you restart it. To ensure your app restarts if it crashes, use a process manager. A process manager is a “container” for applications that facilitates deployment, provides high availability, and enables you to manage the application at runtime.

アプリケーションを異常終了時に再始動することに加えて、プロセス・マネージャーでは以下が可能になります。

- ランタイム・パフォーマンスとリソース使用量に関するインサイトを得る。
- パフォーマンスを向上させるために設定を動的に変更する。
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### init システムの使用

The next layer of reliability is to ensure that your app restarts when the server restarts. Systems can still go down for a variety of reasons. To ensure that your app restarts if the server crashes, use the init system built into your OS. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

Express アプリケーションで init システムを使用する方法は 2 つあります。

- Run your app in a process manager, and install the process manager as a service with the init system. The process manager will restart your app when the app crashes, and the init system will restart the process manager when the OS restarts. This is the recommended approach.
- init システムで直接、アプリケーション (および Node) を実行します。この方法の方が単純ですが、プロセス・マネージャーを使用する場合に得られる利点は得られません。 This is somewhat simpler, but you don’t get the additional advantages of using a process manager.

##### Systemd

Systemd は、Linux システムとサービス・マネージャーです。大半の主要な Linux ディストリビューションでは、Systemd がデフォルトの init システムとして採用されています。 Most major Linux distributions have adopted systemd as their default init system.

Systemd サービス構成ファイルは、*unit ファイル* という名前で、ファイル名の末尾は .service です。次に、Node アプリケーションを直接管理するための unit ファイルの例を示します (太字のテキストを、ご使用のシステムとアプリケーションの値に置き換えてください)。 Here’s an example unit file to manage a Node app directly. Replace the values enclosed in `<angle brackets>` for your system and app:

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

Systemd について詳しくは、[systemd の解説 (man ページ)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html) を参照してください。

### アプリケーションをクラスターで実行する

マルチコア・システムでは、プロセスのクラスターを起動することで、Node アプリケーションのパフォーマンスを数倍も向上させることができます。クラスターは、アプリケーションの複数インスタンスを実行して (理想的には CPU コアごとに 1 つのインスタンス)、負荷とタスクをインスタンス間で分散させます。 A cluster runs multiple instances of the app, ideally one instance on each CPU core, thereby distributing the load and tasks among the instances.

![クラスター API を使用したアプリケーション・インスタンス間のバランシング](https://expressjs.com/images/clustering.png)

IMPORTANT: Since the app instances run as separate processes, they do not share the same memory space. That is, objects are local to each instance of the app. Therefore, you cannot maintain state in the application code. However, you can use an in-memory datastore like [Redis](http://redis.io/) to store session-related data and state. This caveat applies to essentially all forms of horizontal scaling, whether clustering with multiple processes or multiple physical servers.

In clustered apps, worker processes can crash individually without affecting the rest of the processes. Apart from performance advantages, failure isolation is another reason to run a cluster of app processes. クラスター・アプリケーションでは、ワーカー・プロセスは、残りのプロセスに影響を与えることなく、個々に異常終了することがあります。パフォーマンス上の利点の他に障害分離は、アプリケーション・プロセスのクラスターを実行するもう 1 つの理由です。ワーカー・プロセスが異常終了するたびに、必ず、イベントをログに記録して、cluster.fork() を使用して新規プロセスを作成してください。

#### Node のクラスター・モジュールの使用

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). This enables a master process to spawn worker processes and distribute incoming connections among the workers.

#### PM2 の使用

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

Once running, a given application with the name `app` can be scaled like so:

```
# Add 3 more workers
$ pm2 scale my-app +3
# Scale to a specific number of workers
$ pm2 scale my-app 2
```

For more information on clustering with PM2, see [Cluster Mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/) in the PM2 documentation.

### 要求の結果をキャッシュに入れる

実稼働環境のパフォーマンスを向上させるもう 1 つの戦略は、アプリケーションが同じ要求に何回も対応するために操作を繰り返すことがないように、要求の結果をキャッシュに入れることです。

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### ロード・バランサーを使用する

アプリケーションがどれだけ最適化されていても、単一インスタンスは、限られた量の負荷とトラフィックしか処理できません。アプリケーションを拡張する 1 つの方法は、複数インスタンスを実行して、ロード・バランサーを使用してトラフィックを分散させることです。ロード・バランサーをセットアップすると、アプリケーションのパフォーマンスと速度を向上させることができ、単一インスタンスよりも大規模に拡張できます。 One way to scale an app is to run multiple instances of it and distribute the traffic via a load balancer. Setting up a load balancer can improve your app’s performance and speed, and enable it to scale more than is possible with a single instance.

A load balancer is usually a reverse proxy that orchestrates traffic to and from multiple application instances and servers. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

With load balancing, you might have to ensure that requests that are associated with a particular session ID connect to the process that originated them. This is known as *session affinity*, or *sticky sessions*, and may be addressed by the suggestion above to use a data store such as Redis for session data (depending on your application). For a discussion, see [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### リバース・プロキシーを使用する

A reverse proxy sits in front of a web app and performs supporting operations on the requests, apart from directing requests to the app. It can handle error pages, compression, caching, serving files, and load balancing among other things.

アプリケーションの状態を知る必要のないタスクをリバース・プロキシーに引き渡すことで、Express が解放されて、特殊なアプリケーション・タスクを実行できるようになります。この理由から、実稼働環境で Express を [Nginx](https://www.nginx.com/) や [HAProxy](http://www.haproxy.org/) などのリバース・プロキシーの背後で実行することをお勧めします。 For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/advanced/best-practice-performance.md          )

---

# 実稼働環境におけるベスト・プラクティス: セキュリティー

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# 実稼働環境におけるベスト・プラクティス: セキュリティー

## 概説

The term *“production”* refers to the stage in the software lifecycle when an application or API is generally available to its end-users or consumers. In contrast, in the *“development”* stage, you’re still actively writing and testing code, and the application is not open to external access. The corresponding system environments are known as *production* and *development* environments, respectively.

Development and production environments are usually set up differently and have vastly different requirements. What’s fine in development may not be acceptable in production. For example, in a development environment you may want verbose logging of errors for debugging, while the same behavior can become a security concern in a production environment. And in development, you don’t need to worry about scalability, reliability, and performance, while those concerns become critical in production.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

本番環境でのExpressアプリケーションのセキュリティのベスト・プラクティスは次のとおりです。

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [TLS を使用する](#use-tls)
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [Helmet を使用する](#use-helmet)
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - [Cookie をセキュアに使用する](#use-cookies-securely)
    - 対照的に、[cookie-session](https://www.npmjs.com/package/cookie-session) ミドルウェアは、Cookie が支持するストレージを実装します。セッション・キーだけでなく、セッション全体を Cookie に対して直列化します。これは、セッション・データが比較的小規模で、(オブジェクトではなく) プリミティブ値として容易にエンコードできる場合にのみ使用してください。ブラウザーは Cookie 当たり最小 4096 バイトをサポートすることが想定されますが、その制限を必ず超えないようにするために、ドメイン当たり 4093 バイトのサイズを超えないようにしてください。また、Cookie データがクライアントに対して可視になることに注意してください。何らかの理由でデータを保護したり覆い隠したりする必要がある場合は、express-session を使用することをお勧めします。
    - デフォルトのセッション Cookie 名を使用すると、アプリケーションが攻撃を受けやすくなります。提起されているセキュリティー問題は `X-Powered-By` と似ています。潜在的なアタッカーがこれを使用して、サーバーに対して指紋認証し、攻撃の標的にする可能性があります。
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [依存関係がセキュアであることを確認する](#ensure-your-dependencies-are-secure)
    - [その他の既知の脆弱性を回避する](#avoid-other-known-vulnerabilities)
  - [その他の考慮事項](#additional-considerations)

## 非推奨バージョンや脆弱なバージョンの Express を使用しない

Express 2.x and 3.x are no longer maintained. Security and performance issues in these versions won’t be fixed. Do not use them! If you haven’t moved to version 4, follow the [migration guide](https://expressjs.com/ja/guide/migrating-4.html) or consider [Commercial Support Options](https://expressjs.com/ja/support#commercial-support-options).

また、[セキュリティー更新ページ](https://expressjs.com/ja/advanced/security-updates.html)にリストされている脆弱な Express バージョンを使用していないことを確認してください。使用している場合は、安定しているリリース (最新を推奨します) に更新してください。 If you are, update to one of the stable releases, preferably the latest.

## TLS を使用する

If your app deals with or transmits sensitive data, use [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) to secure the connection and the data. This technology encrypts data before it is sent from the client to the server, thus preventing some common (and easy) hacks. Although Ajax and POST requests might not be visibly obvious and seem “hidden” in browsers, their network traffic is vulnerable to [packet sniffing](https://en.wikipedia.org/wiki/Packet_analyzer) and [man-in-the-middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

You may be familiar with Secure Socket Layer (SSL) encryption. Secure Socket Layer (SSL) 暗号化については理解されていると思います。[TLS は、単に SSL が進化したものです](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx)。つまり、以前に SSL を使用していた場合は、TLS へのアップグレードを検討してください。一般に、TLS を処理するために Nginx を使用することをお勧めします。Nginx (およびその他のサーバー) で TLS を構成するための解説については、[Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations) を参照してください。 In other words, if you were using SSL before, consider upgrading to TLS. In general, we recommend Nginx to handle TLS. For a good reference to configure TLS on Nginx (and other servers), see [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

また、[Let’s Encrypt](https://letsencrypt.org/about/) は、無料の TLS 証明書を取得するための便利なツールです。このツールは、[Internet Security Research Group (ISRG)](https://letsencrypt.org/isrg/) が提供する、無料の自動的かつオープンな認証局 (CA) です。

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

## Helmet を使用する

[Helmet](https://www.npmjs.com/package/helmet) は、HTTP ヘッダーを適切に設定することによって、いくつかの既知の Web の脆弱性からアプリケーションを保護します。

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/ja/advanced/`helmet.js` を使用する場合は、この操作が自動的に実行されます。).

その他のモジュールと同様に Helmet をインストールします。

```
$ npm install helmet
```

次に、コードで使用します。

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

そのため、`app.disable()` メソッドを使用してこのヘッダーをオフにすることがベスト・プラクティスです。

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

## Cookie をセキュアに使用する

Cookie を介してアプリケーションが悪用されないように、デフォルトの セッション Cookie 名を使用しないでください。また、Cookie のセキュリティー・オプションを適切に設定してください。

主なミドルウェア Cookie セッション・モジュールが 2 つあります。

- [express-session](https://www.npmjs.com/package/express-session) は、Express 3.x に組み込まれていた `express.session` ミドルウェアに取って代わります。
- [cookie-session](https://www.npmjs.com/package/cookie-session) は、Express 3.x に組み込まれていた `express.cookieSession` ミドルウェアに取って代わります。

The main difference between these two modules is how they save cookie session data. これらの 2 つのモジュールの主な違いは、Cookie セッション・データの保存方法です。[express-session](https://www.npmjs.com/package/express-session) ミドルウェアは、セッション・データをサーバーに保管します。セッション・データではなく、Cookie 自体の中にあるセッション ID のみを保存します。デフォルトで、メモリー内のストレージを使用し、実稼働環境向けには設計されていません。実稼働環境では、スケーラブルなセッション・ストアをセットアップする必要があります。[互換性のあるセッション・ストア](https://github.com/expressjs/session#compatible-session-stores)のリストを参照してください。 By default, it uses in-memory storage and is not designed for a production environment. In production, you’ll need to set up a scalable session-store; see the list of [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

In contrast, [cookie-session](https://www.npmjs.com/package/cookie-session) middleware implements cookie-backed storage: it serializes the entire session to the cookie, rather than just a session key. Only use it when session data is relatively small and easily encoded as primitive values (rather than objects). Although browsers are supposed to support at least 4096 bytes per cookie, to ensure you don’t exceed the limit, don’t exceed a size of 4093 bytes per domain. Also, be aware that the cookie data will be visible to the client, so if there is any reason to keep it secure or obscure, then `express-session` may be a better choice.

### デフォルトのセッション Cookie 名を使用しない

Using the default session cookie name can open your app to attacks. The security issue posed is similar to `X-Powered-By`: a potential attacker can use it to fingerprint the server and target attacks accordingly.

この問題を回避するには、汎用な Cookie 名を使用します。例えば、[express-session](https://www.npmjs.com/package/express-session) ミドルウェアを使用します。

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Cookie のセキュリティー・オプションを設定する

セキュリティーを強化するために、以下の Cookie オプションを設定します。

- `secure` - ブラウザーが確実に HTTPS のみを介して Cookie を送信するようにします。
- `httpOnly` - Cookie がクライアント JavaScript ではなく、HTTP(S) のみを介して送信されるようにして、クロスサイト・スクリプティング攻撃から保護します。
- `domain` - Cookie のドメインを指定します。URL が要求されているサーバーのドメインとの比較に使用します。一致する場合は、次にパス属性を確認します。 If they match, then check the path attribute next.
- `path` - Cookie のパスを指定します。要求パスとの比較に使用します。このパスがドメインと一致する場合は、要求の Cookie を送信します。 If this and domain match, then send the cookie in the request.
- `expires` - 永続的な Cookie の有効期限を設定するために使用します。

次に、[cookie-session](https://www.npmjs.com/package/cookie-session) ミドルウェアの使用例を示します。

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

## 依存関係がセキュアであることを確認する

npm を使用したアプリケーションの依存関係の管理は、強力で便利な方法です。ただし、使用するパッケージに、アプリケーションにも影響を与える可能性がある重大なセキュリティーの脆弱性が含まれている可能性があります。アプリケーションのセキュリティーの強さは、依存関係の中で「最も弱いリンク」程度でしかありません。 But the packages that you use may contain critical security vulnerabilities that could also affect your application. The security of your app is only as strong as the “weakest link” in your dependencies.

Since npm@6, npm automatically reviews every install request. npm@6以降、npmはすべてのインストール要求を自動的に確認します。また、’npm audit’を使用して依存関係ツリーを分析することもできます。

```
$ npm audit
```

よりセキュアな状態を保ちたい場合は、[Snyk](https://snyk.io/)を検討してください。

Snykは、[Snykのオープンソース脆弱性データベース](https://snyk.io/vuln/)に対して、依存関係の既知の脆弱性に対するアプリケーションをチェックする[コマンドラインツール](https://www.npmjs.com/package/snyk)と[Github integration](https://snyk.io/docs/github)を提供しています。 次のようにCLIをインストールします。 Install the CLI as follows:

```
$ npm install -g snyk
$ cd your-app
```

このコマンドを使用して、アプリケーションの脆弱性をテストします。

```
$ snyk test
```

### その他の既知の脆弱性を回避する

アプリケーションで使用する Express やその他のモジュールに影響を与える可能性がある [Node Security Project](https://npmjs.com/advisories) のアドバイザリーに常に注意してください。一般に、Node Security Project は、Node のセキュリティーに関する知識とツールの優れたリソースです。 In general, these databases are excellent resources for knowledge and tools about Node security.

最後に、Express アプリケーションは、その他の Web アプリケーションと同様、さまざまな Web ベースの攻撃に対して脆弱になりえます。既知の [Web の脆弱性](https://www.owasp.org/www-project-top-ten/)をよく理解して、それらを回避するための予防措置を取ってください。 Familiarize yourself with known [web vulnerabilities](https://www.owasp.org/www-project-top-ten/) and take precautions to avoid them.

## その他の考慮事項

次に、優れた [Node.js セキュリティー・チェックリスト](https://blog.risingstack.com/node-js-security-checklist/)に記載されているその他の推奨事項をリストします。これらの推奨事項の詳細については、ブログの投稿を参照してください。 Refer to that blog post for all the details on these recommendations:

- クロスサイト・スクリプティング (XSS) とコマンド・インジェクション攻撃から保護するために、必ず、ユーザー入力のフィルタリングとサニタイズを実行してください。
- パラメーター化照会または作成済みステートメントを使用して、SQL インジェクション攻撃に対して防衛してください。
- オープン・ソースの [sqlmap](http://sqlmap.org/) ツールを使用して、アプリケーションの SQL インジェクションに対する脆弱性を検出してください。
- [nmap](https://nmap.org/) ツールと [sslyze](https://github.com/nabla-c0d3/sslyze) ツールを使用して、SSL 暗号、鍵、再交渉の構成のほか、証明書の妥当性をテストしてください。
- [safe-regex](https://www.npmjs.com/package/safe-regex) を使用して、使用している正規表現が[正規表現サービス妨害](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS)攻撃を受けやすくなっていないことを確認してください。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/advanced/best-practice-security.md          )

---

# Express 用のテンプレート・エンジンの開発

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Express 用のテンプレート・エンジンの開発

独自のテンプレート・エンジンを作成するには、`app.engine(ext, callback)` メソッドを使用します。`ext` はファイル拡張子を表し、`callback` はテンプレート・エンジン関数です。この関数は、ファイルのロケーション、options オブジェクト、およびコールバック関数の項目をパラメーターとして受け入れます。 `ext` refers to the file extension, and `callback` is the template engine function, which accepts the following items as parameters: the location of the file, the options object, and the callback function.

次のコードは、`.ntl` ファイルをレンダリングするための極めて単純なテンプレート・エンジンを実装する例です。

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

Your app will now be able to render `.ntl` files. これで、アプリケーションは `.ntl` ファイルをレンダリングできるようになります。以下のコンテンツで `index.ntl` というファイルを `views` ディレクトリーに作成します。

```pug
#title#
#message#
```

次に、アプリケーションで次のルートを作成します。

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

ホーム・ページに要求すると、`index.ntl` ファイルは HTML としてレンダリングされます。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### 例

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/advanced/healthcheck-graceful-shutdown.md          )

---

# セキュリティー更新

> Review the latest security updates and patches for Express.js, including detailed vulnerability lists for different versions to help maintain a secure application.

# セキュリティー更新

Node.js の脆弱性は Express に直接影響を与えます。そのため、[Node.js の脆弱性の監視を続けて](https://nodejs.org
/en/blog/vulnerability/)、必ず、安定した最新バージョンの Node.js を使用してください。 Therefore, [keep a watch on Node.js vulnerabilities](https://nodejs.org/en/blog/vulnerability/) and make sure you are using the latest stable version of Node.js.

次のリストに、示されているバージョンの更新で修正された Express の脆弱性を列挙します。

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/ja/resources/contributing.html#security-policies-and-procedures).

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
  - The dependency `forwarded` has been updated to address a [vulnerability](https://npmjs.com/advisories/527). 依存関係`forwarded`は、[脆弱性](https://npmjs.com/advisories/527)に対処するために更新されました。これは、`req.host`、`req.hostname`、`req.ip`、`req.ips`、`req.protocol`のAPIが使用されている場合、アプリケーションに影響を与える可能性があります。
  - 依存関係`mime`は[脆弱性](https://npmjs.com/advisories/535)に対処するために更新されましたが、この問題はExpressには影響しません。
  - 依存関係`send`が更新され、[Node.js 8.5.0の脆弱性](https://nodejs.org/en/blog/vulnerability/september-2017-path-validation/)に対する保護が提供されています。これは特定のNode.jsバージョン8.5.0でExpressを実行する場合にのみ影響します。 This only impacts running Express on the specific Node.js version 8.5.0.
- 4.15.5
  - 依存関係`debug`は[脆弱性](https://snyk.io/vuln/npm:debug:20170905)に対処するために更新されましたが、この問題はExpressには影響しません。
  - The dependency `fresh` has been updated to address a [vulnerability](https://npmjs.com/advisories/526). 依存関係`fresh`は、[脆弱性](https://npmjs.com/advisories/526)に対処するために更新されました。これは、次のAPIが使用されている場合、アプリケーションに影響します：`express.static`、`req.fresh`、`res.json`、`res.jsonp`、`res.send`、`res.sendfile`、`res.sendFile`、`res.sendStatus`
- 4.15.3
  - The dependency `ms` has been updated to address a [vulnerability](https://snyk.io/vuln/npm:ms:20170412). 依存関係`ms`は、[脆弱性](https://snyk.io/vuln/npm:ms:20170412)に対処するために更新されました。`express.static`、`res.sendfile`、および`res.sendFile`のAPIで、信頼できない文字列が入力され`maxAge`オプションに渡されると、アプリケーションに影響を与える可能性があります。
- 4.15.2
  - 依存関係`qs`は[脆弱性](https://snyk.io/vuln/npm:qs:20170213)に対処するために更新されましたが、この問題はExpressには影響しません。4.15.2へのアップデートは良い習慣ですが、この脆弱性に対処する必要はありません。 Updating to 4.15.2 is a good practice, but not required to address the vulnerability.
- 4.11.1
  - `express.static`、`res.sendfile`、および `res.sendFile` のルート・パス開示の脆弱性を修正しました。
- 4.10.7
  - `express.static` のオープン・リダイレクトの脆弱性を修正しました ([アドバイザリー](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164))。
- 4.8.8
  - `express.static` のディレクトリー・トラバーサルの脆弱性を修正しました ([アドバイザリー](http://npmjs.com/advisories/32)、[CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394))。
- 4.8.4
  - Node.js 0.10 は、特定の状況で `fd` をリークして、`express.static` および `res.sendfile` に影響を及ぼす可能性があります。悪意ある要求によって `fd` がリークされ、最終的に `EMFILE` エラーが発生したり、サーバーが応答しなくなったりする可能性があります。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 4.8.0
  - クエリストリングに極めて多数の索引が含まれる疎配列により、プロセスがメモリー不足になり、サーバーが異常終了する可能性があります。
  - 過度にネストされたクエリストリング・オブジェクトにより、プロセスがサーバーをブロックして、サーバーが一時的に応答できなくなる可能性があります。

## 3.x

**Express 3.x は保守されなくなりました**

3.xの既知および未知のセキュリティ問題は、最終更新（2015年8月1日）以降は対処されていません。3.x系を使用することは安全であると見なされるべきではありません。 It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/ja/support#commercial-support-options).

- 3.19.1
  - `express.static`、`res.sendfile`、および `res.sendFile` のルート・パス開示の脆弱性を修正しました。
- 3.19.0
  - `express.static` のオープン・リダイレクトの脆弱性を修正しました ([アドバイザリー](https://npmjs.com/advisories/35)、[CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164))。
- 3.16.10
  - `express.static` のディレクトリー・トラバーサルの脆弱性を修正しました。
- 3.16.6
  - Node.js 0.10 は、特定の状況で `fd` をリークして、`express.static` および `res.sendfile` に影響を及ぼす可能性があります。悪意ある要求によって `fd` がリークされ、最終的に `EMFILE` エラーが発生したり、サーバーが応答しなくなったりする可能性があります。 Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 3.16.0
  - クエリストリングに極めて多数の索引が含まれる疎な配列により、プロセスがメモリー不足になり、サーバーが異常終了する可能性があります。
  - 過度にネストされたクエリストリング・オブジェクトにより、プロセスがサーバーをブロックして、サーバーが一時的に応答できなくなる可能性があります。
- 3.3.0
  - サポートされていないメソッドのオーバーライドの 404 応答は、クロスサイト・スクリプティングの攻撃を受ける可能性がありました。

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ja/advanced/security-updates.md          )
