# Best Practices in Produktionsumgebungen: Leistung und Zuverlässigkeit and more

# Best Practices in Produktionsumgebungen: Leistung und Zuverlässigkeit

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# Best Practices in Produktionsumgebungen: Leistung und Zuverlässigkeit

In diesem Beitrag werden Best Practices in Bezug auf Leistung und Zuverlässigkeit für Express-Anwendungen behandelt, die in der Produktionsumgebung bereitgestellt werden.

Dieses Thema gehört sicherlich zur “DevOps”-Welt und deckt traditionelle Entwicklungs- und Betriebsprozesse ab. Entsprechend sind die Informationen hier in zwei Teile unterteilt:

- Things to do in your code (the dev part):
  - Für statische Dateien Middleware verwenden
  - Keine synchronen Funktionen verwenden
  - [Do logging correctly](#do-logging-correctly)
  - [Handle exceptions properly](#handle-exceptions-properly)
- Things to do in your environment / setup (the ops part):
  - NODE_ENV auf “production” festlegen
  - Automatischen Neustart Ihrer Anwendung sicherstellen
  - Anwendung in einem Cluster ausführen
  - Anforderungsergebnisse im Cache speichern
  - Load Balancer verwenden
  - Reverse Proxy verwenden

## Things to do in your code

Dies sind einige Beispiele für Maßnahmen, die Sie an Ihrem Code vornehmen können, um die Anwendungsleistung zu verbessern:

- Für statische Dateien Middleware verwenden
- Keine synchronen Funktionen verwenden
- [Do logging correctly](#do-logging-correctly)
- [Handle exceptions properly](#handle-exceptions-properly)

### GZIP-Komprimierung verwenden

Mit der GZIP-Komprimierung lässt sich die Größe des Antworthauptteils deutlich verringern und somit die Geschwindigkeit der Webanwendung erhöhen. Verwenden Sie die Middleware [compression](https://www.npmjs.com/package/compression) für die GZIP-Komprimierung in Ihrer Express-Anwendung. Beispiel:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

Bei Websites mit hohem Datenverkehr in Produktionsumgebungen lässt sich die Komprimierung am besten installieren, indem sie auf Reverse Proxy-Ebene implementiert wird (siehe [Reverse Proxy verwenden](#proxy)). In diesem Fall wird die Middleware “compression” nicht benötigt. Details zur Aktivierung der GZIP-Komprimierung in Nginx siehe [Modul ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) in der Nginx-Dokumentation.

### Keine synchronen Funktionen verwenden

Synchrone Funktionen und Methoden belasten den Ausführungsprozess, bis sie zurückgegeben werden. Ein einzelner Aufruf für eine synchrone Funktion kann in wenigen Mikrosekunden oder Millisekunden zurückgegeben werden. Bei Websites mit hohem Datenverkehr hingegen summieren sich diese Aufrufe und verringern die Leistung der Anwendung. Sie sollten also deren Verwendung in Produktionsumgebungen vermeiden.

Auch wenn Node und viele andere Module synchrone und asynchrone Versionen ihrer Funktionen bieten, sollten Sie in Produktionsumgebungen immer die asynchrone Version verwenden. Nur beim ersten Systemstart ist die Verwendung einer synchronen Funktion begründet.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Auch wenn Sie diese natürlich nicht in der Produktionsumgebung verwenden werden, soll dadurch trotzdem sichergestellt werden, dass Ihr Code in der Produktionsumgebung eingesetzt werden kann. Weitere Informationen hierzu siehe [Wöchentliches Update für io.js 2.1.0](https://nodejs.org/en/blog/weekly-updates/weekly-update.2015-05-22/#2-1-0).

### Do logging correctly

Im Allgemeinen gibt es für die Protokollierung Ihrer Anwendung zwei Gründe: 1) Debugging und 2) Protokollierung von Anwendungsaktivitäten (im Wesentlichen alles andere, außer Debugging). Die Verwendung von`console.log()` oder `console.err()` zur Ausgabe von Protokollnachrichten an das Terminal ist in der Entwicklung gängige Praxis. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### Für Debuggingzwecke

Wenn Sie die Protokollierung für Debuggingzwecke nutzen, sollten Sie statt `console.log()` besser ein spezielles Debuggingmodul wie [debug](https://www.npmjs.com/package/debug) verwenden. Mit einem solchen Modul können Sie über die Umgebungsvariable DEBUG steuern, welche Debugnachrichten an `console.err()` gesendet werden (falls vorhanden). Um Ihre Anwendung rein asynchron zu halten, können Sie trotzdem `console.err()` per Pipe zu einem anderen Programm umleiten. Sie nehmen dann aber kein Debugging in der Produktionsumgebung vor, richtig?

#### Für Anwendungsaktivitäten

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Ausnahmebedingungen ordnungsgemäß handhaben

Node-Anwendungen stürzen ab, wenn eine nicht abgefangene Ausnahmebedingung vorkommt. Wenn diese Ausnahmebedingungen nicht behandelt und entsprechende Maßnahmen eingeleitet werden, stürzt Ihre Express-Anwendung ab und geht offline. Wenn Sie dem nachfolgenden Rat in [Sicherstellen, dass Ihre Anwendung automatisch neu gestartet wird](#restart) folgen, wird Ihre Anwendung nach einem Absturz wiederhergestellt. Glücklicherweise haben Express-Anwendungen nur eine kurze Initialisierungszeit. Nevertheless, you want to avoid crashing in the first place, and to do that, you need to handle exceptions properly.

Mit folgenden Verfahren stellen Sie sicher, dass alle Ausnahmebedingungen gehandhabt werden:

- [“try-catch” verwenden](#try-catch)
- [“Promises” verwenden](#promises)

Um näher auf diese Themen eingehen zu können, müssen Sie sich ein grundlegendes Verständnis der Fehlerbehandlung in Node und Express aneignen: Verwendung von Error-first-Callbacks und Propagieren von Fehlern in Middleware. Node verwendet die Konvention “Error-first-Callback” für die Rückgabe von Fehlern von asynchronen Funktionen, bei denen der erste Parameter zur Callback-Funktion das Fehlerobjekt ist, gefolgt von Ergebnisdaten in den nachfolgenden Parametern. Um anzugeben, dass kein Fehler vorliegt, müssen Sie “null” als ersten Parameter übergeben. Die Callback-Funktion muss der Konvention “Error-first-Callback” folgen, um den Fehler sinnvoll bearbeiten zu können. In Express hat sich bewährt, die Funktion “next()” zu verwenden, um Fehler über die Middleware-Chain zu propagieren.

Weitere Informationen zu den Grundlagen der Fehlerbehandlung siehe:

- [Fehlerbehandlung in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### “try-catch” verwenden

“try-catch” ist ein JavaScript-Sprachkonstrukt, mit dem Sie Ausnahmebedingungen in synchronem Code abfangen können. Verwenden Sie “try-catch” beispielsweise, um JSON-Parsing-Fehler wie unten gezeigt zu bearbeiten.

Dies ist ein Beispiel zur Verwendung von “try-catch”, um eine potenzielle “process-crashing”-Ausnahmebedingung zu handhaben.
Diese Middlewarefunktion akzeptiert einen Abfragefeldparameter mit dem Namen “params”, der ein JSON-Objekt ist.

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

“try-catch” funktioniert jedoch nur in synchronem Code. Da die Node-Plattform primär asynchron ist (insbesondere in einer Produktionsumgebung), lassen sich mit “try-catch” nicht besonders viele Ausnahmebedingungen abfangen.

#### “Promises” verwenden

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

Sie sollten *auf keinen* Fall per Listener das Ereignis `uncaughtException` überwachen, das ausgegeben wird, wenn eine Ausnahmebedingung bis zurück zur Ereignisschleife bestehen bleibt. Durch das Hinzufügen eines Ereignislisteners für `uncaughtException` verändert sich das Standardverhalten des Prozesses, über das eine Ausnahmebedingung festgestellt wird. Das Ausführen einer Anwendung nach einer nicht abgefangenen Ausnahmebedingung ist aber eine durchaus riskante Vorgehensweise und wird nicht empfohlen, da der Prozessstatus störanfällig und unvorhersehbar wird.

Außerdem wird die Verwendung von `uncaughtException` offiziell als [grobes Vorgehen](https://nodejs.org/api/process.html#process_event_uncaughtexception) angesehen, sodass es den [Vorschlag](https://github.com/nodejs/node-v0.x-archive/issues/2582) gibt, die Funktion aus dem Kern zu entfernen. Das Überwachen von `uncaughtException` per Listener ist also keine gute Idee. Daher empfehlen wir Dinge wie Mehrfachprozesse und Supervisoren: Ein Absturz und anschließender Neustart ist häufig die zuverlässigste Art der Fehlerbehebung.

Zudem empfehlen wir, [domains](https://nodejs.org/api/domain.html) nicht zu verwenden. Mit diesem Modul, das zudem veraltet ist, lässt sich das Problem in der Regel nicht lösen.

## Things to do in your environment / setup

Dies sind einige Beispiele für Maßnahmen, die Sie an Ihrer Systemumgebung vornehmen können, um die Anwendungsleistung zu verbessern:

- NODE_ENV auf “production” festlegen
- Automatischen Neustart Ihrer Anwendung sicherstellen
- Anwendung in einem Cluster ausführen
- Anforderungsergebnisse im Cache speichern
- Load Balancer verwenden
- Reverse Proxy verwenden

### NODE_ENV auf “production” festlegen

In der Umgebungsvariablen NODE_ENV wird die Umgebung angegeben, in der eine Anwendung ausgeführt wird (in der Regel ist dies die Entwicklungs- oder Produktionsumgebung). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

Durch das Festlegen von NODE_ENV auf “production” führt Express Folgendes aus:

- Speichern von Anzeigevorlagen im Cache.
- Speichern von CSS-Dateien, die aus CSS-Erweiterungen generiert wurden, im Cache.
- Generieren von weniger ausführlichen Fehlernachrichten.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

Wenn Sie umgebungsspezifischen Code schreiben müssen, können Sie den Wert von NODE_ENV mit `process.env.NODE_ENV` überprüfen. Beachten Sie, dass die Überprüfung des Werts seiner Umgebungsvariablen eine leistungsbezogene Penalisierung nach sich zieht.

In einer Entwicklungsumgebung wird die Umgebungsvariable in der Regel in Ihrer interaktiven Shell festgelegt, indem Sie beispielsweise `export` oder Ihre Datei `.bash_profile` verwenden. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). Der nächste Abschnitt enthält weitere Details zur Verwendung des Init-Systems im Allgemeinen. Die Festlegung von NODE_ENV ist jedoch für das Leistungsverhalten so wichtig (und so einfach durchzuführen), dass hier besonders darauf eingegangen wird.

Verwenden Sie bei systemd die Anweisung `Environment` in Ihrer Einheitendatei. Beispiel:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### Automatischen Neustart Ihrer Anwendung sicherstellen

In der Produktionsumgebung sollte die Anwendung nie offline sein. Das bedeutet, dass Sie sicherstellen müssen, dass die Anwendung bei einem Absturz der Anwendung oder des Servers immer wieder neu gestartet wird. Auch wenn man hofft, das keines dieser Ereignisse jemals eintritt, muss man doch mit beiden Möglichkeiten rechnen und:

- einen Prozessmanager verwenden, um die Anwendung (und Node) bei einem Absturz neu zu starten.
- das Init-System Ihres Betriebssystems verwenden, um den Prozessmanager bei einem Absturz des Betriebssystems neu zu starten. Außerdem kann das Init-System auch ohne einen Prozessmanager verwendet werden.

Node-Anwendungen stürzen ab, wenn eine nicht abgefangene Ausnahmebedingung auftritt. Als Erstes müssen Sie in einem solchen Fall sicherstellen, dass Ihre Anwendung ausreichend getestet wurde und in der Lage ist, alle Ausnahmebedingungen zu handhaben (weitere Informationen siehe [Ausnahmebedingungen ordnungsgemäß handhaben](#exceptions)). Die sicherste Maßnahme ist jedoch, einen Mechanismus zu implementieren, über den bei einem Absturz der Anwendung ein automatischer Neustart der Anwendung ausgeführt wird.

#### Prozessmanager verwenden

In Entwicklungumgebungen wird die Anwendung einfach über die Befehlszeile mit `node server.js` oder einer vergleichbaren Datei gestartet. In der Produktionsumgebung hingegen ist durch diese Vorgehensweise die Katastrophe bereits vorprogrammiert. Wenn die Anwendung abstürzt, ist sie solange offline, bis Sie sie erneut starten. Um sicherzustellen, dass Ihre Anwendung nach einem Absturz neu gestartet wird, sollten Sie einen Prozessmanager verwenden. Ein Prozessmanager ist ein “Container” für Anwendungen, der die Bereitstellung erleichtert, eine hohe Verfügbarkeit sicherstellt und  die Verwaltung der Anwendung zur Laufzeit ermöglicht.

Neben einem Neustart der Anwendung nach einem Absturz bietet ein Prozessmanager noch weitere Möglichkeiten:

- Einblicke in die Laufzeitleistung und die Ressourcennutzung
- Dynamische Änderung der Einstellungen zur Verbesserung des Leistungsverhaltens
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### Init-System verwenden

Als nächste Ebene der Zuverlässigkeit müssen Sie sicherstellen, dass Ihre Anwendung bei einem Serverneustart neu gestartet wird. Systeme können immer wieder aus verschiedenen Gründen abstürzen. Um sicherzustellen, dass Ihre Anwendung bei einem Serverabsturz neu gestartet wird, können Sie das in Ihr Betriebssystem integrierte Init-System verwenden. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

Es gibt zwei Möglichkeiten, Init-Systeme mit Ihrer Express-Anwendung zu verwenden:

- Ausführung Ihrer Anwendung in einem Prozessmanager und Installation des Prozessmanagers als Service mit dem Init-System. Der Prozessmanager wird neu gestartet, wenn Ihre Anwendung abstürzt. Dies ist die empfohlene Vorgehensweise.
- Ausführung Ihrer Anwendung (und von Node) direkt mit dem Init-System. Diese Vorgehensweise ist zwar etwas einfacher, Sie profitieren jedoch nicht von den zusätzlichen Vorteilen des Einsatzes eines Prozessmanagers.

##### systemd

“systemd” ist ein Linux-System und Service-Manager. Die meisten wichtigen Linux-Distributionen haben “systemd” als Init-Standardsystem übernommen.

Eine “systemd”-Servicekonfigurationsdatei wird als *Einheitendatei* bezeichnet, die die Endung “.service” hat. Dies ist ein Beispiel für eine Einheitendatei zur direkten Verwaltung einer Node-Anwendung (ersetzen Sie den Text in Fettdruck durch Werte für Ihr System und Ihre Anwendung): Replace the values enclosed in `<angle brackets>` for your system and app:

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

Weitere Informationen zu “systemd” siehe [systemd-Referenz (Man-Page)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html).

### Anwendung in einem Cluster ausführen

In einem Multi-Core-System können Sie die Leistung einer Node-Anwendung mehrmals erhöhen, indem Sie einen Cluster von Prozessen starten. Ein Cluster führt mehrere Instanzen der Anwendung aus, idealerweise eine Instanz auf jedem CPU-Core.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

Wichtig. Da die Anwendungsinstanzen als separate Prozesse ausgeführt werden, nutzen sie nicht dieselbe Hauptspeicherkapazität gemeinsam. Das heißt, Objekte befinden sich für jede Instanz der Anwendung auf lokaler Ebene. Daher kann der Status im Anwendungscode nicht beibehalten werden. Sie können jedoch einen speicherinternen Datenspeicher wie [Redis](http://redis.io/) verwenden, um sitzungsrelevante Daten und Statusinformationen zu speichern. Diese Einschränkung trifft im Wesentlichen auf alle Formen der horizontalen Skalierung zu, unabhängig davon, ob es sich um Clustering mit mehreren Prozessen oder mehreren physischen Servern handelt.

Bei in Gruppen zusammengefassten Anwendungen (geclusterte Anwendungen) können Verarbeitungsprozesse einzeln ausfallen, ohne dass sich dies auf die restlichen Prozesse auswirkt. Neben den Leistungsvorteilen ist die Fehlerisolierung ein weiterer Grund, einen Cluster von Anwendungsprozessen auszuführen. Wenn ein Verarbeitungsprozess abstürzt, müssen Sie sicherstellen, dass das Ereignis protokolliert und ein neuer Prozess mithilfe von “cluster.fork()” gestartet wird.

#### Clustermodule von Node verwenden

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). Dadurch wird ein Masterprozess eingeleitet, um Verarbeitungsprozesse zu starten und eingehende Verbindungen auf die Verarbeitungsprozesse zu verteilen.

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

### Anforderungsergebnisse im Cache speichern

Eine weitere Strategie zur Verbesserung des Leistungsverhaltens in Produktionsumgebungen ist das Speichern von Anforderungergebnissen im Cache. Ihre Anwendung muss also diese Operation nicht wiederholt ausführen, um dieselbe Anforderung wiederholt zu bedienen.

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### Load Balancer verwenden

Unabhängig davon, wie gut eine Anwendung optimiert wurde, kann eine Einzelinstanz nur eine begrenzte Arbeitslast oder einen begrenzten Datenverkehr handhaben. Eine Möglichkeit, eine Anwendung zu skalieren, ist die Ausführung mehrerer Instanzen dieser Anwendung und die Verteilung des Datenverkehrs über eine Lastausgleichsfunktion (Load Balancer) vorzunehmen. Die Einrichtung eines solchen Load Balancer kann helfen, Leistung und Geschwindigkeit Ihrer Anwendung zu verbessern.

Ein Load Balancer ist in der Regel ein Reverse Proxy, der den Datenverkehr zu und von mehreren Anwendungsinstanzen und Servern koordiniert. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

Bei einer solchen Lastverteilung müssen Sie sicherstellen, dass Anforderungen, die einer bestimmten Sitzungs-ID zugeordnet sind, mit dem Prozess verbunden sind, von dem sie ursprünglich stammen. Dies wird auch als *Sitzungsaffinität* oder *Affine Sitzungen* bezeichnet und kann durch den obigen Vorschlag, einen Datenspeicher wie Redis für Sitzungsdaten zu verwenden (je nach Anwendung), umgesetzt werden. Eine Beschreibung hierzu siehe [Mehrere Knoten verwenden](https://socket.io/docs/v4/using-multiple-nodes/).

### Reverse Proxy verwenden

Ein Reverse Proxy befindet sich vor einer Webanwendung und führt Unterstützungsoperationen für die Anforderungen aus (außer das Weiterleiten von Anforderungen an die Anwendung). Fehlerseiten, Komprimierungen und Caching bearbeiten, Dateien bereitstellen und Lastverteilungen vornehmen.

Durch die Übergabe von Tasks, die keine Kenntnis des Anwendungsstatus erfordern, an einen Reverse Proxy muss Express keine speziellen Anwendungstasks mehr ausführen. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/advanced/best-practice-performance.md          )

---

# Best Practices in Produktionsumgebungen: Sicherheit

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# Best Practices in Produktionsumgebungen: Sicherheit

## Überblick

Der Begriff *“Produktion”* bezieht sich auf die Phase im Softwarelebenszyklus, in der eine Anwendung oder API für Endbenutzer oder Verbraucher allgemein verfügbar ist. Im Gegensatz dazu wird in der Phase *“Entwicklung”* noch aktiv Code geschrieben und getestet. Die Anwendung ist in dieser Phase noch nicht für externen Zugriff verfügbar. Die entsprechenden Systemumgebungen werden als *Produktionsumgebungen* und *Entwicklungsumgebungen* bezeichnet.

Entwicklungs- und Produktionsumgebungen werden in der Regel unterschiedlich konfiguriert und weisen deutliche Unterschiede bei den Anforderungen auf. Was in der Entwicklung funktioniert, muss in der Produktion nicht unbedingt akzeptabel sein. Beispiel: In einer Entwicklungsumgebung ist eine ausführliche Protokollierung von Fehlern für Debuggingzwecke sinnvoll. Dieselbe Vorgehensweise kann in einer Produktionsumgebung jedoch zu einem Sicherheitsproblem führen. In einer Entwicklungsumgebung müssen Sie sich keine Gedanken zu Themen wie Skalierbarkeit, Zuverlässigkeit und Leistung machen, während dies in einer Produktionsumgebung kritische Faktoren sind.

Hinweis

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

In diesem Beitrag werden einige der Best Practices in Bezug auf das Thema Sicherheit für Express-Anwendungen behandelt, die in der Produktionsumgebung bereitgestellt werden.

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - Über [hsts](https://github.com/helmetjs/hsts) werden `Strict-Transport-Security`-Header festgelegt, über die sichere (HTTP over SSL/TLS) Verbindungen zum Server durchgesetzt werden.
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - “Helmet” ist eine Ansammlung von neun kleineren Middlewarefunktionen, über die sicherheitsrelevante HTTP-Header festgelegt werden.
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - Über [xssFilter](https://github.com/helmetjs/x-xss-protection) werden `X-XSS-Protection`-Header festgelegt, um XSS-Filter (Cross-site Scripting) in den meisten aktuellen Web-Browsern zu aktivieren.
    - Über [noCache](https://github.com/helmetjs/nocache) werden `Cache-Control`- und Pragma-Header festgelegt, um clientseitiges Caching zu deaktivieren.
    - Über [ieNoOpen](https://github.com/helmetjs/ienoopen) werden `X-Download-Options`-Header für IE8+ festgelegt.
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - [Avoid other known vulnerabilities](#avoid-other-known-vulnerabilities)
  - [Additional considerations](#additional-considerations)

## Verwenden Sie keine veralteten oder anfälligen Versionen von Express

Express 2.x und 3.x werden nicht mehr gepflegt. Sicherheits- und Leistungsprobleme in diesen Versionen werden nicht mehr behoben. Verwenden Sie diese Versionen nicht! Wenn Sie noch nicht auf Version 4 umgestellt haben, befolgen Sie die Anweisungen im [Migrationshandbuch](https://expressjs.com/de/guide/migrating-4.html).

Stellen Sie außerdem sicher, dass Sie keine anfälligen Express-Versionen verwenden, die auf der [Seite mit den Sicherheitsupdates](https://expressjs.com/de/advanced/security-updates.html) aufgelistet sind. Falls doch, führen Sie ein Update auf eines der stabileren Releases durch, bevorzugt das aktuelle Release.

## TLS verwenden

Wenn über Ihre Anwendung vertrauliche Daten bearbeitet oder übertragen werden, sollten Sie [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) verwenden, um die Verbindung und die Daten zu schützen. Diese Technologie verschlüsselt Daten, bevor sie vom Client zum Server gesendet werden. Dadurch lassen sich einige gängige (und einfache) Hackerattacken vermeiden. Auch wenn Ajax- und POST-Anforderungen nicht sofort offensichtlich und in Browsern “versteckt” zu sein scheinen, ist deren Netzverkehr anfällig für das [Ausspionieren von Paketen](https://en.wikipedia.org/wiki/Packet_analyzer) und [Man-in-the-Middle-Attacken](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

Möglicherweise sind Sie mit SSL-Verschlüsselung (Secure Socket Layer) bereits vertraut. [TLS ist einfach der nächste Entwicklungsschritt bei SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). In anderen Worten: Wenn Sie bisher SSL verwendet haben, sollten Sie ein Upgrade auf TLS in Erwägung ziehen. Generell empfehlen wir für TLS den Nginx-Server. Eine gute Referenz zum Konfigurieren von TLS auf Nginx (und anderen Servern) ist [Empfohlene Serverkonfigurationen (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

Ein handliches Tool zum Abrufen eines kostenloses TLS-Zertifikats ist außerdem [Let’s Encrypt](https://letsencrypt.org/about/), eine kostenlose, automatisierte und offene Zertifizierungsstelle der [Internet Security Research Group (ISRG)](https://letsencrypt.org/isrg/).

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

## “Helmet” verwenden

[Helmet](https://www.npmjs.com/package/helmet) kann beim Schutz Ihrer Anwendung gegen einige gängige Schwachstellen hilfreiche Dienste leisten, indem die HTTP-Header entsprechend konfiguriert werden.

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/de/advanced/Wenn Sie `helmet.js` verwenden, kümmert sich das Tool darum.).

Installieren Sie “Helmet” wie alle anderen Module:

```
$ npm install helmet
```

So verwenden Sie “Helmet” in Ihrem Code:

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

Ein bewährtes Verfahren ist also, diesen Header mit der Methode `app.disable()` zu deaktivieren:

```
app.disable('x-powered-by')
```

Hinweis

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

## Cookies sicher verwenden

Um sicherzustellen, dass Cookies Ihre Anwendung nicht für Angriffsmöglichkeiten öffnen, sollten Sie den standardmäßigen Namen des Sitzungscookies nicht verwenden und die Cookie-Sicherheitsoptionen entsprechend festlegen.

Es gibt zwei wesentliche Middleware-Cookie-Sitzungsmodule:

- [express-session](https://www.npmjs.com/package/express-session), das in Express 3.x integrierte `express.session`-Middleware ersetzt.
- [cookie-session](https://www.npmjs.com/package/cookie-session), das in Express 3.x integrierte `express.cookieSession`-Middleware ersetzt.

Der Hauptunterschied zwischen diesen beiden Modulen liegt darin, wie die Cookie-Sitzungsdaten gespeichert werden. Die [express-session](https://www.npmjs.com/package/express-session)-Middleware speichert Sitzungsdaten auf dem Server. Sie speichert nur die Sitzungs-ID im Cookie und nicht die Sitzungsdaten. Standardmäßig wird dabei der speicherinterne Speicher verwendet. Eine Verwendung der Middleware in der Produktionsumgebung ist nicht vorgesehen. In der Produktionsumgebung müssen Sie einen skalierbaren “Session-Store” einrichten. Siehe hierzu die Liste der [kompatiblen Session-Stores](https://github.com/expressjs/session#compatible-session-stores).

Im Gegensatz dazu implementiert die [cookie-session](https://www.npmjs.com/package/cookie-session)-Middleware cookiegestützten Speicher: Sie serialisiert die gesamte Sitzung zum Cookie und nicht nur einen Sitzungsschlüssel. Diese Middleware sollten Sie nur verwenden, wenn Sitzungsdaten relativ klein sind und einfach als primitive Werte (und nicht als Objekte) codiert sind. Auch wenn Browser mindestens 4096 Byte pro Cookie unterstützen sollten, müssen Sie sicherstellen, dass dieses Limit nicht überschritten wird. Überschreiten Sie auf keinen Fall die Größe von 4093 Byte pro Domäne. Achten Sie zudem darauf, dass die Cookiedaten für den Client sichtbar sind. Wenn also ein Grund vorliegt, die Daten sicher oder unkenntlich zu machen, ist “express-session” möglicherweise die bessere Wahl.

### Verwenden Sie nicht den standardmäßigen Namen des Sitzungscookies

Die Verwendung des standardmäßigen Namens des Sitzungscookies kann Ihre Anwendung anfällig für Attacken machen. Das mögliche Sicherheitsproblem ist vergleichbar mit `X-Powered-By`: ein potenzieller Angreifer kann diesen Header verwenden, um einen elektronischen Fingerabdruck des Servers zu erstellen und Attacken entsprechend zu platzieren.

Über [noSniff](https://github.com/helmetjs/dont-sniff-mimetype) werden `X-Content-Type-Options`-Header festgelegt, um bei Browsern MIME-Sniffing von Antworten weg vom deklarierten Inhaltstyp (declared content-type) vorzubeugen.

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Cookie-Sicherheitsoptionen festlegen

Legen Sie die folgenden Cookieoptionen fest, um die Sicherheit zu erhöhen:

- `secure` - Stellt sicher, dass der Browser das Cookie nur über HTTPS sendet.
- `httpOnly` - Stellt sicher, dass das Cookie nur über HTTP(S) und nicht über das Client-JavaScript gesendet wird und dadurch Schutz gegen Cross-Site Scripting-Attacken besteht.
- `domain` - Gibt die Domäne des Cookies an, die für den Vergleich mit der Domäne des Servers verwendet wird, in der die URL angefordert wird. Stimmen diese beiden überein, müssen Sie das Pfadattribut überprüfen.
- `path` - Gibt den Pfad des Cookies an, der für den Vergleich mit dem Anforderungspfad verwendet wird. Wenn dieser Pfad und die Domäne übereinstimmen, können Sie das Cookie in der Anforderung senden.
- `expires` - Wird verwendet, um das Ablaufdatum für persistente Cookies festzulegen.

Dies ist ein Beispiel zur Verwendung der [cookie-session](https://www.npmjs.com/package/cookie-session)-Middleware:

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

### Vermeiden Sie andere Schwachstellen

Achten Sie auf [Node Security Project](https://npmjs.com/advisories)-Empfehlungen, die Express oder andere Module, die Ihre Anwendung nutzt, beeinträchtigen können. Im Allgemeinen ist Node Security Project aber eine exzellente Ressource mit Wissen und Tools zur Sicherheit von Node.

Letztendlich können Express-Anwendungen – wie viele andere Webanwendungen auch – anfällig für eine Vielzahl webbasierter Attacken sein. Machen Sie sich deshalb mit bekannten [webspezifischen Schwachstellen](https://www.owasp.org/www-project-top-ten/) vertraut und treffen Sie die geeigneten Vorkehrungen, um diese zu vermeiden.

## Weitere Überlegungen

Dies sind einige weitere Empfehlungen aus der hervorragenden [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/). In diesem Blogbeitrag finden Sie alle Details zu diesen Empfehlungen:

- Filtern und bereinigen Sie immer Benutzereingaben, um sich gegen XS-Angriffe (Cross-Site Scripting) und Befehlsinjektionsattacken zu schützen.
- Implementieren Sie Verteidungsmaßnahmen gegen SQL-Injection-Attacken, indem sie parametrisierte Abfragen oder vorbereitete Anweisungen einsetzen.
- Nutzen Sie das Open-Source-Tool [sqlmap](http://sqlmap.org/), um SQL-Injection-Schwachstellen in Ihrer Anwendung zu erkennen.
- Verwenden Sie die Tools [nmap](https://nmap.org/) und [sslyze](https://github.com/nabla-c0d3/sslyze), um die Konfiguration Ihrer SSL-Verschlüsselungen, -Schlüssel und Neuvereinbarungen sowie die Gültigkeit Ihres Zertifikats zu testen.
- Verwenden Sie [safe-regex](https://www.npmjs.com/package/safe-regex), um sicherzustellen, dass Ihre regulären Ausdrücke nicht für [Denial-of-Service-Attacken](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS) anfällig sind.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/advanced/best-practice-security.md          )

---

# Template

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Template-Engines für Express entwickeln

Verwenden Sie die Methode `app.engine(ext, callback)`, um Ihre eigene Template-Engine zu erstellen. `ext` bezieht sich auf die Dateierweiterung, `callback` ist die Template-Engine-Funktion, die die folgenden Elemente als Parameter akzeptiert: die Position der Datei, das Optionsobjekt und die Callback-Funktion.

Der folgende Code ist ein Beispiel für die Implementierung einer sehr einfachen Template-Engine für die Ausgabe von `.ntl`-Dateien.

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

Ihre Anwendung ist jetzt in der Lage, `.ntl`-Dateien auszugeben. Erstellen Sie im Verzeichnis `views` eine Datei namens `index.ntl` mit dem folgenden Inhalt.

```pug
#title#
#message#
```

Erstellen Sie dann in Ihrer Anwendung die folgende Route.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Wenn Sie eine Anforderung zur Homepage einleiten, wird `index.ntl` im HTML-Format ausgegeben.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### Beispiel

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/advanced/healthcheck-graceful-shutdown.md          )

---

# Sicherheitsupdates

> Review the latest security updates and patches for Express.js, including detailed vulnerability lists for different versions to help maintain a secure application.

# Sicherheitsupdates

Schwachstellen bei Node.js wirken sich direkt auf Express aus. Daher sollten Sie [ein Auge auf Schwachstellen bei Node.js haben](https://nodejs.org
/en/blog/vulnerability/) und sicherstellen, dass Sie die aktuelle stabile Version von Node.js haben.

Die folgende Liste enthält die Express-Schwachstellen, die im angegebenen Versionsupdate behoben wurden.

Hinweis

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/de/resources/contributing.html#security-policies-and-procedures).

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
  - Offenlegungsgefahr beim Rootpfad in `express.static`, `res.sendfile` und `res.sendFile` behoben.
- 4.10.7
  - Offene Umadressierungsschwachstelle in `express.static` ([Empfehlung](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)) behoben.
- 4.8.8
  - Schwachstellen durch Directory-Traversal-Technik in `express.static` ([Empfehlung](http://npmjs.com/advisories/32) , [CVE-2014-6394](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6394)) behoben.
- 4.8.4
  - Node.js 0.10 kann in bestimmten Situationen Lecks bei `fd` aufweisen, die sich auf `express.static` und `res.sendfile` auswirken. Böswillige Anforderungen können zu Lecks bei `fd` führen und letztendlich `EMFILE`-Fehler nach sich ziehen und bewirken, dass Server nicht antworten.
- 4.8.0
  - Sparse-Arrays mit extrem hohen Indizes in der Abfragezeichenfolge können bewirken, dass für die Prozessausführung nicht genügend Arbeitsspeicher zur Verfügung steht und es zu einem Serverabsturz kommt.
  - Extrem verschachtelte Abfragezeichenfolgenobjekte können bewirken, dass der Prozess blockiert und der Server dadurch vorübergehend nicht antwortet.

## 3.x

**Express 3.x WIRD NICHT MEHR GEWARTET**

Bekannte und unbekannte Probleme bei Sicherheit und Leistung in 3.x wurden seit dem letzten Update (1. August 2015) noch nicht behoben. Es wird dringend empfohlen, die aktuelle Version von Express zu verwenden.

If you are unable to upgrade past 3.x, please consider [Commercial Support Options](https://expressjs.com/de/support#commercial-support-options).

- 3.19.1
  - Offenlegungsgefahr beim Rootpfad in `express.static`, `res.sendfile` und `res.sendFile` behoben.
- 3.19.0
  - Offene Umadressierungsschwachstelle in `express.static` ([Empfehlung](https://npmjs.com/advisories/35), [CVE-2015-1164](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-1164)) behoben.
- 3.16.10
  - Schwachstellen durch Directory-Traversal-Technik in `express.static` behoben.
- 3.16.6
  - Node.js 0.10 kann in bestimmten Situationen Lecks bei `fd` aufweisen, die sich auf `express.static` und `res.sendfile` auswirken. Böswillige Anforderungen können zu Lecks bei `fd` führen und letztendlich `EMFILE`-Fehler nach sich ziehen und bewirken, dass Server nicht antworten.
- 3.16.0
  - Sparse-Arrays mit extrem hohen Indizes in der Abfragezeichenfolge können bewirken, dass für die Prozessausführung nicht genügend Arbeitsspeicher zur Verfügung steht und es zu einem Serverabsturz kommt.
  - Extrem verschachtelte Abfragezeichenfolgenobjekte können bewirken, dass der Prozess blockiert und der Server dadurch vorübergehend nicht antwortet.
- 3.3.0
  - Die Antwort 404 bei einem nicht unterstützten Überschreibungsversuch war anfällig gegen Cross-Site Scripting-Attacken.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/de/advanced/security-updates.md          )
