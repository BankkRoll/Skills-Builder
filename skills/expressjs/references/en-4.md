# Production best practices: performance and reliability and more

# Production best practices: performance and reliability

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# Production best practices: performance and reliability

This article discusses performance and reliability best practices for Express applications deployed to production.

This topic clearly falls into the “devops” world, spanning both traditional development and operations. Accordingly, the information is divided into two parts:

- Things to do in your code (the dev part):
  - [Use gzip compression](#use-gzip-compression)
  - [Don’t use synchronous functions](#dont-use-synchronous-functions)
  - [Do logging correctly](#do-logging-correctly)
  - [Handle exceptions properly](#handle-exceptions-properly)
- Things to do in your environment / setup (the ops part):
  - [Set NODE_ENV to “production”](#set-node_env-to-production)
  - [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts)
  - [Run your app in a cluster](#run-your-app-in-a-cluster)
  - [Cache request results](#cache-request-results)
  - [Use a load balancer](#use-a-load-balancer)
  - [Use a reverse proxy](#use-a-reverse-proxy)

## Things to do in your code

Here are some things you can do in your code to improve your application’s performance:

- [Use gzip compression](#use-gzip-compression)
- [Don’t use synchronous functions](#dont-use-synchronous-functions)
- [Do logging correctly](#do-logging-correctly)
- [Handle exceptions properly](#handle-exceptions-properly)

### Use gzip compression

Gzip compressing can greatly decrease the size of the response body and hence increase the speed of a web app. Use the [compression](https://www.npmjs.com/package/compression) middleware for gzip compression in your Express app. For example:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

For a high-traffic website in production, the best way to put compression in place is to implement it at a reverse proxy level (see [Use a reverse proxy](#use-a-reverse-proxy)). In that case, you do not need to use compression middleware. For details on enabling gzip compression in Nginx, see [Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) in the Nginx documentation.

### Don’t use synchronous functions

Synchronous functions and methods tie up the executing process until they return. A single call to a synchronous function might return in a few microseconds or milliseconds, however in high-traffic websites, these calls add up and reduce the performance of the app. Avoid their use in production.

Although Node and many modules provide synchronous and asynchronous versions of their functions, always use the asynchronous version in production. The only time when a synchronous function can be justified is upon initial startup.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Of course, you wouldn’t want to use this in production, but rather to ensure that your code is ready for production. See the [node command-line options documentation](https://nodejs.org/api/cli.html#cli_trace_sync_io) for more information.

### Do logging correctly

In general, there are two reasons for logging from your app: For debugging and for logging app activity (essentially, everything else). Using `console.log()` or `console.error()` to print log messages to the terminal is common practice in development. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### For debugging

If you’re logging for purposes of debugging, then instead of using `console.log()`, use a special debugging module like [debug](https://www.npmjs.com/package/debug). This module enables you to use the DEBUG environment variable to control what debug messages are sent to `console.error()`, if any. To keep your app purely asynchronous, you’d still want to pipe `console.error()` to another program. But then, you’re not really going to debug in production, are you?

#### For app activity

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Handle exceptions properly

Node apps crash when they encounter an uncaught exception. Not handling exceptions and taking appropriate actions will make your Express app crash and go offline. If you follow the advice in [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts) below, then your app will recover from a crash. Fortunately, Express apps typically have a short startup time. Nevertheless, you want to avoid crashing in the first place, and to do that, you need to handle exceptions properly.

To ensure you handle all exceptions, use the following techniques:

- [Use try-catch](#use-try-catch)
- [Use promises](#use-promises)

Before diving into these topics, you should have a basic understanding of Node/Express error handling: using error-first callbacks, and propagating errors in middleware. Node uses an “error-first callback” convention for returning errors from asynchronous functions, where the first parameter to the callback function is the error object, followed by result data in succeeding parameters. To indicate no error, pass null as the first parameter. The callback function must correspondingly follow the error-first callback convention to meaningfully handle the error. And in Express, the best practice is to use the next() function to propagate errors through the middleware chain.

For more on the fundamentals of error handling, see:

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Use try-catch

Try-catch is a JavaScript language construct that you can use to catch exceptions in synchronous code. Use try-catch, for example, to handle JSON parsing errors as shown below.

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

However, try-catch works only for synchronous code. Because the Node platform is primarily asynchronous (particularly in a production environment), try-catch won’t catch a lot of exceptions.

#### Use promises

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

Additionally, using `uncaughtException` is officially recognized as [crude](https://nodejs.org/api/process.html#process_event_uncaughtexception). So listening for `uncaughtException` is just a bad idea. This is why we recommend things like multiple processes and supervisors: crashing and restarting is often the most reliable way to recover from an error.

We also don’t recommend using [domains](https://nodejs.org/api/domain.html). It generally doesn’t solve the problem and is a deprecated module.

## Things to do in your environment / setup

Here are some things you can do in your system environment to improve your app’s performance:

- [Set NODE_ENV to “production”](#set-node_env-to-production)
- [Ensure your app automatically restarts](#ensure-your-app-automatically-restarts)
- [Run your app in a cluster](#run-your-app-in-a-cluster)
- [Cache request results](#cache-request-results)
- [Use a load balancer](#use-a-load-balancer)
- [Use a reverse proxy](#use-a-reverse-proxy)

### Set NODE_ENV to “production”

The NODE_ENV environment variable specifies the environment in which an application is running (usually, development or production). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

Setting NODE_ENV to “production” makes Express:

- Cache view templates.
- Cache CSS files generated from CSS extensions.
- Generate less verbose error messages.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

If you need to write environment-specific code, you can check the value of NODE_ENV with `process.env.NODE_ENV`. Be aware that checking the value of any environment variable incurs a performance penalty, and so should be done sparingly.

In development, you typically set environment variables in your interactive shell, for example by using `export` or your `.bash_profile` file. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). The next section provides more details about using your init system in general, but setting `NODE_ENV` is so important for performance (and easy to do), that it’s highlighted here.

With systemd, use the `Environment` directive in your unit file. For example:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### Ensure your app automatically restarts

In production, you don’t want your application to be offline, ever. This means you need to make sure it restarts both if the app crashes and if the server itself crashes. Although you hope that neither of those events occurs, realistically you must account for both eventualities by:

- Using a process manager to restart the app (and Node) when it crashes.
- Using the init system provided by your OS to restart the process manager when the OS crashes. It’s also possible to use the init system without a process manager.

Node applications crash if they encounter an uncaught exception. The foremost thing you need to do is to ensure your app is well-tested and handles all exceptions (see [handle exceptions properly](#handle-exceptions-properly) for details). But as a fail-safe, put a mechanism in place to ensure that if and when your app crashes, it will automatically restart.

#### Use a process manager

In development, you started your app simply from the command line with `node server.js` or something similar. But doing this in production is a recipe for disaster. If the app crashes, it will be offline until you restart it. To ensure your app restarts if it crashes, use a process manager. A process manager is a “container” for applications that facilitates deployment, provides high availability, and enables you to manage the application at runtime.

In addition to restarting your app when it crashes, a process manager can enable you to:

- Gain insights into runtime performance and resource consumption.
- Modify settings dynamically to improve performance.
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### Use an init system

The next layer of reliability is to ensure that your app restarts when the server restarts. Systems can still go down for a variety of reasons. To ensure that your app restarts if the server crashes, use the init system built into your OS. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

There are two ways to use init systems with your Express app:

- Run your app in a process manager, and install the process manager as a service with the init system. The process manager will restart your app when the app crashes, and the init system will restart the process manager when the OS restarts. This is the recommended approach.
- Run your app (and Node) directly with the init system. This is somewhat simpler, but you don’t get the additional advantages of using a process manager.

##### Systemd

Systemd is a Linux system and service manager. Most major Linux distributions have adopted systemd as their default init system.

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

For more information on systemd, see the [systemd reference (man page)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html).

### Run your app in a cluster

In a multi-core system, you can increase the performance of a Node app by many times by launching a cluster of processes. A cluster runs multiple instances of the app, ideally one instance on each CPU core, thereby distributing the load and tasks among the instances.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANT: Since the app instances run as separate processes, they do not share the same memory space. That is, objects are local to each instance of the app. Therefore, you cannot maintain state in the application code. However, you can use an in-memory datastore like [Redis](http://redis.io/) to store session-related data and state. This caveat applies to essentially all forms of horizontal scaling, whether clustering with multiple processes or multiple physical servers.

In clustered apps, worker processes can crash individually without affecting the rest of the processes. Apart from performance advantages, failure isolation is another reason to run a cluster of app processes. Whenever a worker process crashes, always make sure to log the event and spawn a new process using cluster.fork().

#### Using Node’s cluster module

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

### Cache request results

Another strategy to improve the performance in production is to cache the result of requests, so that your app does not repeat the operation to serve the same request repeatedly.

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### Use a load balancer

No matter how optimized an app is, a single instance can handle only a limited amount of load and traffic. One way to scale an app is to run multiple instances of it and distribute the traffic via a load balancer. Setting up a load balancer can improve your app’s performance and speed, and enable it to scale more than is possible with a single instance.

A load balancer is usually a reverse proxy that orchestrates traffic to and from multiple application instances and servers. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

With load balancing, you might have to ensure that requests that are associated with a particular session ID connect to the process that originated them. This is known as *session affinity*, or *sticky sessions*, and may be addressed by the suggestion above to use a data store such as Redis for session data (depending on your application). For a discussion, see [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### Use a reverse proxy

A reverse proxy sits in front of a web app and performs supporting operations on the requests, apart from directing requests to the app. It can handle error pages, compression, caching, serving files, and load balancing among other things.

Handing over tasks that do not require knowledge of application state to a reverse proxy frees up Express to perform specialized application tasks. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/advanced/best-practice-performance.md          )

---

# Production Best Practices: Security

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# Production Best Practices: Security

## Overview

The term *“production”* refers to the stage in the software lifecycle when an application or API is generally available to its end-users or consumers. In contrast, in the *“development”* stage, you’re still actively writing and testing code, and the application is not open to external access. The corresponding system environments are known as *production* and *development* environments, respectively.

Development and production environments are usually set up differently and have vastly different requirements. What’s fine in development may not be acceptable in production. For example, in a development environment you may want verbose logging of errors for debugging, while the same behavior can become a security concern in a production environment. And in development, you don’t need to worry about scalability, reliability, and performance, while those concerns become critical in production.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

Security best practices for Express applications in production include:

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [Use TLS](#use-tls)
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [Use Helmet](#use-helmet)
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - [Use cookies securely](#use-cookies-securely)
    - [Don’t use the default session cookie name](#dont-use-the-default-session-cookie-name)
    - [Set cookie security options](#set-cookie-security-options)
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - [Avoid other known vulnerabilities](#avoid-other-known-vulnerabilities)
  - [Additional considerations](#additional-considerations)

## Don’t use deprecated or vulnerable versions of Express

Express 2.x and 3.x are no longer maintained. Security and performance issues in these versions won’t be fixed. Do not use them! If you haven’t moved to version 4, follow the [migration guide](https://expressjs.com/en/guide/migrating-4.html) or consider [Commercial Support Options](https://expressjs.com/en/support#commercial-support-options).

Also ensure you are not using any of the vulnerable Express versions listed on the [Security updates page](https://expressjs.com/en/advanced/security-updates.html). If you are, update to one of the stable releases, preferably the latest.

## Use TLS

If your app deals with or transmits sensitive data, use [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) to secure the connection and the data. This technology encrypts data before it is sent from the client to the server, thus preventing some common (and easy) hacks. Although Ajax and POST requests might not be visibly obvious and seem “hidden” in browsers, their network traffic is vulnerable to [packet sniffing](https://en.wikipedia.org/wiki/Packet_analyzer) and [man-in-the-middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

You may be familiar with Secure Socket Layer (SSL) encryption. [TLS is simply the next progression of SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515(v=vs.85).aspx). In other words, if you were using SSL before, consider upgrading to TLS. In general, we recommend Nginx to handle TLS. For a good reference to configure TLS on Nginx (and other servers), see [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

Also, a handy tool to get a free TLS certificate is [Let’s Encrypt](https://letsencrypt.org/about/), a free, automated, and open certificate authority (CA) provided by the [Internet Security Research Group (ISRG)](https://www.abetterinternet.org/).

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

## Use Helmet

[Helmet](https://helmetjs.github.io/) can help protect your app from some well-known web vulnerabilities by setting HTTP headers appropriately.

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://helmetjs.github.io/).

Install Helmet like any other module:

```
$ npm install helmet
```

Then to use it in your code:

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

## Use cookies securely

To ensure cookies don’t open your app to exploits, don’t use the default session cookie name and set cookie security options appropriately.

There are two main middleware cookie session modules:

- [express-session](https://www.npmjs.com/package/express-session) that replaces `express.session` middleware built-in to Express 3.x.
- [cookie-session](https://www.npmjs.com/package/cookie-session) that replaces `express.cookieSession` middleware built-in to Express 3.x.

The main difference between these two modules is how they save cookie session data. The [express-session](https://www.npmjs.com/package/express-session) middleware stores session data on the server; it only saves the session ID in the cookie itself, not session data. By default, it uses in-memory storage and is not designed for a production environment. In production, you’ll need to set up a scalable session-store; see the list of [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

In contrast, [cookie-session](https://www.npmjs.com/package/cookie-session) middleware implements cookie-backed storage: it serializes the entire session to the cookie, rather than just a session key. Only use it when session data is relatively small and easily encoded as primitive values (rather than objects). Although browsers are supposed to support at least 4096 bytes per cookie, to ensure you don’t exceed the limit, don’t exceed a size of 4093 bytes per domain. Also, be aware that the cookie data will be visible to the client, so if there is any reason to keep it secure or obscure, then `express-session` may be a better choice.

### Don’t use the default session cookie name

Using the default session cookie name can open your app to attacks. The security issue posed is similar to `X-Powered-By`: a potential attacker can use it to fingerprint the server and target attacks accordingly.

To avoid this problem, use generic cookie names; for example using [express-session](https://www.npmjs.com/package/express-session) middleware:

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Set cookie security options

Set the following cookie options to enhance security:

- `secure` - Ensures the browser only sends the cookie over HTTPS.
- `httpOnly` - Ensures the cookie is sent only over HTTP(S), not client JavaScript, helping to protect against cross-site scripting attacks.
- `domain` - indicates the domain of the cookie; use it to compare against the domain of the server in which the URL is being requested. If they match, then check the path attribute next.
- `path` - indicates the path of the cookie; use it to compare against the request path. If this and domain match, then send the cookie in the request.
- `expires` - use to set expiration date for persistent cookies.

Here is an example using [cookie-session](https://www.npmjs.com/package/cookie-session) middleware:

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

### Avoid other known vulnerabilities

Keep an eye out for [Node Security Project](https://npmjs.com/advisories) or [Snyk](https://snyk.io/vuln/) advisories that may affect Express or other modules that your app uses. In general, these databases are excellent resources for knowledge and tools about Node security.

Finally, Express apps—like any other web apps—can be vulnerable to a variety of web-based attacks. Familiarize yourself with known [web vulnerabilities](https://www.owasp.org/www-project-top-ten/) and take precautions to avoid them.

## Additional considerations

Here are some further recommendations from the excellent [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/). Refer to that blog post for all the details on these recommendations:

- Always filter and sanitize user input to protect against cross-site scripting (XSS) and command injection attacks.
- Defend against SQL injection attacks by using parameterized queries or prepared statements.
- Use the open-source [sqlmap](http://sqlmap.org/) tool to detect SQL injection vulnerabilities in your app.
- Use the [nmap](https://nmap.org/) and [sslyze](https://github.com/nabla-c0d3/sslyze) tools to test the configuration of your SSL ciphers, keys, and renegotiation as well as the validity of your certificate.
- Use [safe-regex](https://www.npmjs.com/package/safe-regex) to ensure your regular expressions are not susceptible to [regular expression denial of service](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS) attacks.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/advanced/best-practice-security.md          )

---

# Developing template engines for Express

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Developing template engines for Express

Use the `app.engine(ext, callback)` method to create your own template engine. `ext` refers to the file extension, and `callback` is the template engine function, which accepts the following items as parameters: the location of the file, the options object, and the callback function.

The following code is an example of implementing a very simple template engine for rendering `.ntl` files.

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

Your app will now be able to render `.ntl` files. Create a file named `index.ntl` in the `views` directory with the following content.

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

When you make a request to the home page, `index.ntl` will be rendered as HTML.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### Example

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/advanced/healthcheck-graceful-shutdown.md          )

---

# Security updates

> Review the latest security updates and patches for Express.js, including detailed vulnerability lists for different versions to help maintain a secure application.

# Security updates

Node.js vulnerabilities directly affect Express. Therefore, [keep a watch on Node.js vulnerabilities](https://nodejs.org/en/blog/vulnerability/) and make sure you are using the latest stable version of Node.js.

The list below enumerates the Express vulnerabilities that were fixed in the specified version update.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

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
  - Fixed root path disclosure vulnerability in `express.static`, `res.sendfile`, and `res.sendFile`
- 4.10.7
  - Fixed open redirect vulnerability in `express.static` ([advisory](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)).
- 4.8.8
  - Fixed directory traversal vulnerabilities in `express.static` ([advisory](http://npmjs.com/advisories/32) , [CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394)).
- 4.8.4
  - Node.js 0.10 can leak `fd`s in certain situations that affect `express.static` and `res.sendfile`. Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 4.8.0
  - Sparse arrays that have extremely high indexes in the query string could cause the process to run out of memory and crash the server.
  - Extremely nested query string objects could cause the process to block and make the server unresponsive temporarily.

## 3.x

**Express 3.x IS END-OF-LIFE AND NO LONGER MAINTAINED**

Known and unknown security and performance issues in 3.x have not been addressed since the last update (1 August, 2015). It is highly recommended to use the latest version of Express.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/en/support#commercial-support-options).

- 3.19.1
  - Fixed root path disclosure vulnerability in `express.static`, `res.sendfile`, and `res.sendFile`
- 3.19.0
  - Fixed open redirect vulnerability in `express.static` ([advisory](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)).
- 3.16.10
  - Fixed directory traversal vulnerabilities in `express.static`.
- 3.16.6
  - Node.js 0.10 can leak `fd`s in certain situations that affect `express.static` and `res.sendfile`. Malicious requests could cause `fd`s to leak and eventually lead to `EMFILE` errors and server unresponsiveness.
- 3.16.0
  - Sparse arrays that have extremely high indexes in query string could cause the process to run out of memory and crash the server.
  - Extremely nested query string objects could cause the process to block and make the server unresponsive temporarily.
- 3.3.0
  - The 404 response of an unsupported method override attempt was susceptible to cross-site scripting attacks.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/en/advanced/security-updates.md          )
