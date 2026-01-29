# Best practice sulla produzione: prestazioni e affidabilità and more

# Best practice sulla produzione: prestazioni e affidabilità

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# Best practice sulla produzione: prestazioni e affidabilità

In questo articolo vengono descritte le best practice sulle prestazioni e sull’affidabilità per le applicazioni Express implementate per la produzione.

Questo argomento entra nel mondo di “devops”, coprendo sia le operazioni che lo sviluppo tradizionale. Di conseguenza, le informazioni sono divise in due parti:

- Things to do in your code (the dev part):
  - Utilizzare la compressione gzip
  - [Asynchronous Error Handling in Express with Promises, Generators and ES7](https://web.archive.org/web/20240000000000/https://strongloop.com/strongblog/async-error-handling-expressjs-es7-promises-generators/)
  - Gestire in modo appropriato le eccezioni
  - [Handle exceptions properly](#handle-exceptions-properly)
- [Operazioni da effettuare nell’ambiente / configurazione](#env) (la parte delle operazioni).
  - Impostare NODE_ENV su “produzione”
  - Al contrario, utilizzare il middleware [serve-static](https://www.npmjs.com/package/serve-static) (o qualcosa di equivalente), ottimizzato per servire i file per le applicazioni Express.
  - Eseguire l’applicazione in un cluster
  -
  - Utilizzare un servizio di bilanciamento del carico
  - Utilizzare un proxy inverso

## Things to do in your code

Di seguito sono elencate alcune operazioni che è possibile effettuare nel codice per migliorare le prestazioni dell’applicazione:

- Utilizzare la compressione gzip
- [Asynchronous Error Handling in Express with Promises, Generators and ES7](https://web.archive.org/web/20240000000000/https://strongloop.com/strongblog/async-error-handling-expressjs-es7-promises-generators/)
- Gestire in modo appropriato le eccezioni
- [Handle exceptions properly](#handle-exceptions-properly)

### Utilizzare la compressione gzip

La compressione gzip è in grado di ridurre notevolmente la dimensione del contenuto della risposta e di conseguenza aumentare la velocità di un’applicazione web. Utilizzare il middleware di [compressione](https://www.npmjs.com/package/compression) per la compressione gzip nell’applicazione Express. Ad esempio:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

Per un sito web ad elevato traffico nella produzione, il miglior modo per utilizzare la compressione è quello di implementarla ad un livello di proxy inverso (consultare [Utilizzare un proxy inverso](#proxy)). In questo caso, non è necessario utilizzare il middleware di compressione. Per dettagli su come abilitare la compressione gzip in Nginx, consultare [Modulo ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) nella documentazione Nginx.

### Non utilizzare funzioni sincrone

I metodi e le funzioni sincrone ostacolano il processo di esecuzione finché non restituiscono un risultato. Una chiamata singola a una funzione sincrona potrebbe restituire un risultato in pochi microsecondi o millisecondi, tuttavia in siti web ad elevato traffico, queste chiamate aggiungono e riducono le prestazioni di un’applicazione. Evitarne l’utilizzo in produzione.

Poiché Node e molti moduli forniscono versioni sicrone e asincrone delle relative funzioni, utilizzare sempre la versione asincrona nella produzione. L’unico caso in cui l’utilizzo di una funzione sincrona è giustificato, è allo startup iniziale.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Naturalmente, non si consiglia di utilizzarlo nella produzione, ma solo per assicurare che il codice sia pronto per la produzione. Consultare l’[aggiornamento settimanale per io.js 2.1.0](https://nodejs.org/en/blog/weekly-updates/weekly-update.2015-05-22/#2-1-0) per ulteriori informazioni.

### Effettuare correttamente la registrazione

Solitamente, esistono due motivi per effettuare la registrazione dall’applicazione: per il debug e la registrazione dell’attività dell’applicazione (sostanzialmente, qualsiasi altra cosa). L’utilizzo di `console.log()` o `console.err()` per stampare i messaggi di log sul terminale, è un’operazione comune nello sviluppo. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### Per il debug

Se si sta effettuando la registrazione per motivi di debug, allora invece di utilizzare `console.log()`, utilizzare un modulo di debug speciale quale [debug](https://www.npmjs.com/package/debug). Questo modulo consente di utilizzare la variabile di ambiente DEBUG per controllare quali messaggi di debug vengono inviati a `console.err()`, se presenti. Per fare in modo che l’applicazione resti strettamente asincrona, è necessario instradare `console.err()` a un altro programma. Però a questo punto, non andrai ad effettuare il debug in fase di produzione giusto?

#### Per l’attività dell’applicazione

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Handle exceptions properly

Le applicazioni Node danno origine a errori quando riscontrano eccezioni non rilevate. Se tali eccezioni non vengono gestite o se non si effettuano operazioni appropriate, l’applicazione Express si arresterà in modo anomalo. Seguendo i consigli descritti in [Riavvio automatico dell’applicazione](#restart), sarà possibile recuperare l’applicazione dopo un arresto anomalo. Fortunatamente, le applicazioni Express solitamente hanno tempi di avvio molto brevi. Tuttavia, per prima cosa è necessario evitare che si verifichino arresti anomali, e per effettuare ciò, è necessario gestire in modo appropriato le eccezioni.

Per essere sicuri di gestire al meglio tutte le eccezioni, utilizzare le seguenti tecniche:

- [Utilizzare try-catch](#try-catch)
- [Utilizzare promises](#promises)

Prima di leggere questi argomenti, è necessario avere una conoscenza base della gestione degli errori di Node/Express: utilizzo di error-first callback e diffusione degli errori al middleware. Node utilizza la convenzione “error-first callback” per restituire gli errori da funzioni asincrone, dove il primo parametro per la funzione callback è l’oggetto dell’errore, seguito dai dati nei parametri successivi. Per indicare un errore, indicare null come primo parametro. La funzione callback deve seguire in modo corrispondente la convenzione error-first callback per gestire l’errore in modo significativo. In Express, il miglior modo è quello di utilizzare la funzione next() per diffondere gli errori attraverso la catena middleware.

Per ulteriori informazioni sulle nozioni di base della gestione degli errori, consultare:

- [Gestione degli errori in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Utilizzare try-catch

Try-catch è un linguaggio JavaScript che è possibile utilizzare per rilevare eccezioni in codice sincrono. Ad esempio, utilizzare try-catch, per gestire errori di analisi JSON come mostrato di seguito.

Di seguito viene riportato un esempio di utilizzo di try-catch per la gestione di un’eccezione che dà origine a un arresto anomalo del processo.
Questa funzione middleware accetta un parametro del campo query denominato “params” che è un oggetto JSON.

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

Tuttavia, try-catch funziona solo per il codice sincrono. Poiché la piattaforma Node è principalmente asincrona (nello specifico in un ambiente di produzione), try-catch non sarà in grado di rilevare molte eccezioni.

#### Utilizzare promises

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

#### Cosa non fare

Una cosa da *non* fare è quella di stare in ascolto per un evento `uncaughtException`, emesso quando un’eccezione si verifica ed è costante nel loop degli eventi. Se si aggiunge un programma di ascolto dell’evento per `uncaughtException` si cambierà il funzionamento predefinito del processo che sta riscontrando un’eccezione; il processo continuerà ad operare malgrado l’eccezione. Questo potrebbe risultare un ottimo modo per prevenire un arresto anomalo dell’applicazione, ma continuare ad utilizzare un’applicazione dopo che si è verificata un’eccezione non rilevata è pericoloso e non è consigliato, poiché lo stato del processo diventa non affidabile e non prevedibile.

Inoltre, l’utilizzo di `uncaughtException` è ufficialmente riconosciuto come [non conforme](https://nodejs.org/api/process.html#process_event_uncaughtexception) ed esiste una [proposta](https://github.com/nodejs/node-v0.x-archive/issues/2582) per la relativa rimozione dal core. Quindi continuare a visualizzare un evento `uncaughtException` non è un buon segno. Ecco perché consigliamo di usufruire di più processi e supervisori: l’arresto anomalo e il riavvio sono spesso il modo più affidabile per ripristinare una situazione dopo un errore.

Inoltre, non si consiglia di utilizzare l’opzione [domini](https://nodejs.org/api/domain.html). Solitamente non risolve il problema ed è considerato un modulo obsoleto.

## Operazioni da effettuare nell’ambiente / configurazione

Di seguito sono elencate alcune operazioni che è possibile effettuare nell’ambiente del sistema per migliorare le prestazioni dell’applicazione:

- Impostare NODE_ENV su “produzione”
- Al contrario, utilizzare il middleware [serve-static](https://www.npmjs.com/package/serve-static) (o qualcosa di equivalente), ottimizzato per servire i file per le applicazioni Express.
- Eseguire l’applicazione in un cluster
-
- Utilizzare un servizio di bilanciamento del carico
- Utilizzare un proxy inverso

### Impostare NODE_ENV su “produzione”

La variabile di ambiente NODE_ENV indica l’ambiente in cui è in esecuzione un’applicazione (solitamente, sviluppo o applicazione). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

L’impostazione di NODE_ENV su “produzione” consente ad Express di:

- Memorizzare in cache i template di visualizzazione.
- Memorizzare in cache i file CSS generati da stensioni CSS.
- Generare meno messaggi di errore ridondanti.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

Se si ha la necessità di scrivere codice specifico dell’ambiente, è possibile selezionare il valore di NODE_ENV con `process.env.NODE_ENV`. Notare che la selezione del valore di qualsiasi variabile di ambiente influisce sulle prestazioni in modo negativo, quindi questa operazione deve essere effettuata con moderazione.

Nello sviluppo, solitamente si impostano le variabili di ambiente nella shell interattiva, ad esempio utilizzando `export` o il file `.bash_profile`. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). La sezione successiva fornisce ulteriori dettagli sull’utilizzo in generale del sistema init, però anche impostare NODE_ENV è molto importante per le prestazioni (ed è facile da fare), evidenziato di seguito.

Con systemd, utilizzare la direttiva `Environment` nel file unit. Ad esempio:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### Verificare che l’applicazione sia in grado di riavviarsi automaticamente

In fase di produzione, l’applicazione non deve mai andare offline. Ciò significa che deve riavviarsi nel caso in cui sia l’applicazione che il server terminino in modo anomalo. Anche se ovviamente si spera che entrambe queste situazioni non si verifichino mai, realisticamente è necessario considerare l’eventualità di:

- Utilizzare un process manager per riavviare l’applicazione (e Node) quando termina in modo anomalo.
- Utilizzare il sistema init fornito dal sistema operativo per riavviare il process manager quando il sistema operativo termina in modo anomalo. È inoltre possibile utilizzare il sistema init senza un process manager.

Le applicazioni Node terminano in modo anomalo se riscontrano eccezioni non rilevate. La prima cosa da fare è verificare che l’applicazione sia stata verificata e che sia in grado di gestire tutte le eccezioni (consultare [Gestire in modo appropriato le eccezioni](#exceptions) per dettagli). Come prevenzione, attivare un meccanismo che assicuri che applicazione si riavvii automaticamente in caso di arresto anomalo.

#### Utilizzare un process manager

Nello sviluppo, l’applicazione è stata avviata semplicemente dalla riga comandi con `node server.js` o qualcosa di simile. Ma se si effettua questa stessa operazione in campo di produzione si andrà incontro a situazioni pericolose. Se l’applicazione termina in modo anomalo, sarà offline finché non viene riavviata. Per fare in modo che l’applicazione si riavvii nel caso in cui termini in modo anomalo, utilizzare un process manager. Un process manager è un “contenitore” per le applicazioni che facilita lo sviluppo, fornisce un’elevata disponibilità e consente di gestire l’applicazione al momento del runtime.

Oltre a fare in modo di riavviare l’applicazione in caso di arresto anomalo, un process manager consente di:

- Ottenere insight relativi alle prestazioni di runtime e al consumo delle risorse.
- Modificare le impostazioni in modo dinamico per migliorare le prestazioni.
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### Utilizzare un sistema init

Il successivo livello di affidabilità è quello di assicurare che l’applicazione venga riavviata quando si riavvia il server. I sistemi possono ancora arrestarsi per moltissimi motivi. Per fare in modo che l’applicazione si riavvii nel caso in cui un server si arresti in modo anomalo, utilizzare il sistema init integrato al sistema operativo. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

Esistono due modi per utilizzare i sistemi init con l’applicazione Express:

- Far eseguire l’applicazione in un process manager e installare il process manager come servizio con il sistema init. Il process manager riavvierà l’applicazione nel caso in cui termini in modo anomalo e il sistema init riavvierà il process manager quando si riavvia il sistema operativo. Questa è la procedura consigliata.
- Far eseguire l’applicazione (e Node) direttamente con il sistema init. Questa operazione risulta più semplice ma non si hanno gli stessi vantaggi dell’utilizzo di un process manager.

##### Systemd

Systemd è un sistema Linux e un service manager. Le più importanti distribuzioni Linux hanno utilizzato systemd come sistema init predefinito.

Un file di configurazione del servizio systemd è denominato *unit file*, con un nome file che termina con .service. Segue un unit file di esempio per gestire un’applicazione Node direttamente (sostituire il testo in grassetto con i valori appropriati per il proprio sistema e applicazione): Replace the values enclosed in `<angle brackets>` for your system and app:

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

Per ulteriori informazioni su systemd, consultare [systemd reference (man page)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html).

### Eseguire l’applicazione in un cluster

In un sistema multicore, è possibile aumentare le prestazioni di un’applicazione Node di molte volte avviando un cluster di processi. Un cluster esegue molte istanze di un’applicazione, nel caso ideale, un’istanza su ciascun core CPU, quindi, distribuendo il carico e le attività tra le istanze.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANTE: poiché le istanze dell’applicazione vengono eseguite come processi separati, non condividono lo stesso spazio di memoria. Ossia, gli oggetti sono locali rispetto a ciascuna istanza dell’applicazione. Pertanto, non è possibile conservare lo stato nel codice dell’applicazione. Tuttavia, è possibile utilizzare un datastore in-memory, ad esempio [Redis](http://redis.io/) per memorizzare lo stato e i dati relativi alla sessione. Questa condizione si applica fondamentalmente a tutti i moduli di scaling orizzontale, se il processo di clustering viene effettuato con più processi o più server fisici.

Nelle applicazioni sottoposte a cluster, i processi di lavoro possono ternare in modo anomalo individualmente senza influenzare gli altri processi. Oltre ai vantaggi che si possono ottenere dalle prestazioni, l’isolamento dell’errore è un altro motivo che spinge a eseguire un cluster di processi di applicazioni. Quando un processo di lavoro termina in modo anomalo, ricordarsi sempre di registrare l’evento e di dare origine a un nuovo processo utilizzando cluster.fork().

#### Utilizzo del modulo cluster di Node

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). Ciò consente a un processo principale di dare origine a processi di lavoro e di distribuire le connessioni in entrata tra i processi di lavoro.

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

### Memorizzare in cache i risultati della richiesta

Un’altra strategia per migliorare le prestazioni in fase di produzione è quella di memorizzare in cache i risultati delle richieste, in modo tale che l’applicazione non debba gestire nuovamente la stessa richiesta.

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### Utilizzare un servizio di bilanciamento del carico

A prescindere da quanto sia ottimizzata un’applicazione, una singola istanza è in grado di gestire solo una quantità limitata di carico e traffico. Un modo per scalare un’applicazione è quello di eseguire più delle proprie istanze e distribuire il traffico tramite un servizio di bilanciamento del carico. L’impostazione di un servizio di bilanciamento del carico può migliorare la velocità e le prestazioni dell’applicazione e abilitarla a scalare di più di quanto sia possibile fare con una singola istanza.

Un servizio di bilanciamento del carico è solitamente un proxy inverso che gestisce il traffico a e d più istanze di applicazione e server. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

Con il servizio di bilanciamento del carico, è possibile che sia necessario garantire che le richieste associate a un ID sessione particolare si connettano al processo che le ha originate. Questo processo è noto come *affinità sessione* o *sessioni delicate*. Si consiglia di utilizzare un data store, ad esempio Redis, per i dati sessione (a seconda dell’applicazione). Per informazioni, consultare [Utilizzo di più nodi](https://socket.io/docs/v4/using-multiple-nodes/).

### Utilizzare un proxy inverso

Un proxy inverso si trova davanti a un’applicazione web ed esegue le operazioni di supporto sulle richieste, oltre a indirizzare le richieste all’applicazione. Inoltre, è in grado di gestire pagine di errore, compressioni, memorizzazioni in cache e il bilanciamento del carico.

Le attività di gestione che non richiedono la conoscenza dello stato dell’applicazione per un proxy inverso consentono ad Express di eseguire attività dell’applicazione specializzate. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/advanced/best-practice-performance.md          )

---

# Best Practice sulla produzione: Sicurezza

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# Best Practice sulla produzione: Sicurezza

## Panoramica

Il termine *“produzione”* si riferisce alla fase nel ciclo di vita del software quando un’applicazione o API è solitamente disponibile per gli utenti finali o i consumatori. Al contrario, nella fase *“sviluppo”*, si sta ancora scrivendo e verificando il codice e l’applicazione non è aperta ad accessi esterni. Gli ambienti di sistema corrispondenti sono noti rispettivamente come ambienti di *produzione* e di *sviluppo*.

Gli ambienti di sviluppo e produzione sono solitamente configurati diversamente e hanno requisiti molto differenti. Ciò che potrebbe andare bene nello sviluppo potrebbe non essere accettato nella produzione. Ad esempio, in un ambiente di sviluppo è possibile che si richieda una registrazione degli errori ridondante per il processo di debug, mentre la stessa richiesta in un ambiente di produzione potrebbe mettere a rischio la sicurezza. Inoltre, in un ambiente di sviluppo non è necessario preoccuparsi della scalabilità, dell’affidabilità e delle prestazioni, mentre nella produzione è fondamentale tenerne conto.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

In questo articolo vengono descritte alcune best practice sulla sicurezza per le applicazioni Express distribuite per la produzione.

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [hsts](https://github.com/helmetjs/hsts) imposta l’intestazione `Strict-Transport-Security` che rafforza connessioni (HTTP su SSL/TLS) sicure per il server.
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - Se si utilizza `helmet.js`, questa operazione sarà effettuata per conto dell’utente.
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - [xssFilter](https://github.com/helmetjs/x-xss-protection) imposta `X-XSS-Protection` per abilitare il filtro XSS (Cross-site scripting) nei browser web più recenti.
    - [noCache](https://github.com/helmetjs/nocache) imposta le intestazioni `Cache-Control` e Pragma per disabilitare la memorizzazione in cache della parte client.
    - [ieNoOpen](https://github.com/helmetjs/ienoopen) imposta `X-Download-Options` per IE8+.
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - [hidePoweredBy](https://github.com/helmetjs/hide-powered-by) rimuove l’intestazione `X-Powered-By`.
  - [Additional considerations](#additional-considerations)

## Non utilizzare versioni obsolete o vulnerabili di Express

Express 2.x e 3.x non sono più supportati. I problemi relativi alla sicurezza e alle prestazioni in queste versioni non verranno risolti. Non utilizzare queste versioni! Se non è stato effettuato l’aggiornamento alla versione 4, consultare la [guida alla migrazione](https://expressjs.com/it/guide/migrating-4.html).

Inoltre, assicurarsi che non si stia utilizzando nessuna delle versioni vulnerabili di Express elencate nella [pagina Aggiornamenti sulla sicurezza](https://expressjs.com/it/advanced/security-updates.html). Nel caso si stia utilizzando una di queste versioni, effettuare l’aggiornamento a una versione aggiornata, preferibilmente l’ultima.

## Utilizzare TLS

Se l’applicazione utilizza o trasmette dati riservati, utilizzare [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) per proteggere la connessione e i dati. Questa tecnologia codifica i dati prima che vengano inviati dal client al server, proteggendo i dati da alcuni attacchi comuni (e facili) da parte di hacker. Anche se le richieste Ajax e POST possono non essere visibili e “nascoste” nei browser, il relativo traffico di rete è vulnerabile agli attacchi [packet sniffing](https://en.wikipedia.org/wiki/Packet_analyzer) e [man-in-the-middle](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

Sicuramente si conosce la crittografia SSL (Secure Socket Layer). [TLS non è altro che un miglioramento di SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). In altre parole, se prima si utilizzava SSL, considerare l’opportunità di passare a TLS. Consigliamo di utilizzare Nginx per gestire la TLS. Per informazioni su come configurare correttamente TLS su Nginx (e altri server), consultare [Recommended Server Configurations (Mozilla Wiki)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

Inoltre, uno strumento molto semplice da utilizzare per ottenere un certificato gratuito TLS è [Let’s Encrypt](https://letsencrypt.org/about/), un CA (certificate authority) gratuito, automatizzato e open fornito da [Internet Security Research Group (ISRG)](https://letsencrypt.org/isrg/).

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

## Utilizzare Helmet

[Helmet](https://www.npmjs.com/package/helmet) è utile per proteggere l’applicazione da alcune vulnerabilità web note configurando le intestazioni HTTP in modo appropriato.

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

Installare Helmet come qualsiasi altro modulo:

```
$ npm install helmet
```

Successivamente, per utilizzarlo nel codice:

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

## Utilizzare i cookie in modo sicuro

Per fare in modo che i cookie non espongano a rischi l’applicazione, non utilizzare il nome cookie della sessione predefinita e impostare le opzioni di sicurezza dei cookie in modo appropriato.

Esistono due moduli di sessione cookie middleware principali:

- [express-session](https://www.npmjs.com/package/express-session) che sostituisce il middleware `express.session` integrato a Express 3.x.
- [cookie-session](https://www.npmjs.com/package/cookie-session) che sostituisce il middleware `express.cookieSession` integrato a Express 3.x.

La differenza principale tra questi due moduli è nel modo in cui salvano i dati di sessione dei cookie. Il middleware [express-session](https://www.npmjs.com/package/express-session) memorizza i dati di sessione sul server; salva l’ID sessione nello stesso cookie e non nei dati di sessione. Per impostazione predefinita, utilizza il processo di memorizzazione in-memory e non è progettato per un ambiente di produzione. Nella produzione, sarà necessario configurare un processo di memorizzazione della sessione scalabile; consultare l’elenco di [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

Al contrario, il middleware [cookie-session](https://www.npmjs.com/package/cookie-session) implementa la memorizzazione di backup dei cookie: suddivide in serie l’intera sessione per il cookie, piuttosto che una chiave di sessione. Utilizzarlo solo quando i dati di sessione sono relativamente piccoli e facilmente codificati come valori primitivi (piuttosto che oggetti). Poiché si presuppone che i browser supportino almeno 4096 byte per cookie, per non superare il limite, non superare la dimensione di 4093 byte per dominio. Inoltre, fare attenzione perché i dati dei cookie saranno visibili al cliente, quindi, se per qualche motivo devono rimanere sicuri o non visibili, la scelta di utilizzare express-session potrebbe essere quella giusta.

### Non utilizzare il nome del cookie della sessione predefinito

L’utilizzo del nome del cookie della sessione predefinito potrebbe esporre l’applicazione ad attacchi da parte di hacker. Il problema di sicurezza messo in discussione è simile a quello di `X-Powered-By`: un potenziale hacker potrebbe utilizzarlo per individuare il server e indirizzare gli attacchi di conseguenza.

Per evitare questo problema, utilizzare i nomi dei cookie predefiniti; ad esempio, utilizzando il middleware [express-session](https://www.npmjs.com/package/express-session):

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Impostare le opzioni di sicurezza dei cookie

Impostare le seguenti opzioni per i cookie per aumentare la sicurezza:

- `secure` - Assicura che il browser invii il cookie solo tramite HTTPS.
- `httpOnly` - Assicura che il cookie venga inviato solo tramite HTTP, non JavaScript del client, questa procedura consentirà una protezione da attacchi XSS (cross-site scripting).
- `domain` - Indica il dominio del cookie; utilizzarlo per fare un confronto con il dominio del server in cui è stato richiesto l’URL. Se corrispondono, come fase successiva verificare l’attributo del percorso.
- `path` - Indica il percorso del cookie; utilizzarlo per fare un confronto con il percorso di richiesta. Se questo e il dominio corrispondono, inviare il cookie nella richiesta.
- `expires` - Utilizzarlo per impostare la data di scadenza per i cookie permanenti.

Esempio di utilizzo del middleware [cookie-session](https://www.npmjs.com/package/cookie-session):

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

### Evitare altre vulnerabilità note

Prestare attenzione alle avvertenze [Node Security Project](https://npmjs.com/advisories) che potrebbero influenzare Express o altri moduli utilizzati dall’applicazione. Solitamente, il Node Security Project è una risorsa eccellente per questioni di apprendimento e per gli strumenti sulla sicurezza di Node.

Infine, le applicazioni Express, come anche altre applicazioni web, possono essere vulnerabili ad una vasta gamma di attacchi basati su web. Cercare di comprendere al meglio le [vulnerabilità web](https://www.owasp.org/www-project-top-ten/) note e prendere precauzioni per evitarle.

## Additional considerations

Ecco alcuni consigli sull’eccellente [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/). Fare riferimento a quel post del blog per tutti i dettagli su questi consigli:

- Filtrare sempre e verificare gli input utente come protezione contro attacchi XSS (cross-site scripting) e command injection.
- Creare una difesa contro attacchi SQL injection utilizzando query con parametri o istruzioni preparate.
- Utilizzare lo strumento [sqlmap](http://sqlmap.org/) open source per rilevare le vulnerabilità SQL injection nell’applicazione.
- Utilizzare gli strumenti [nmap](https://nmap.org/) e [sslyze](https://github.com/nabla-c0d3/sslyze) per verificare la configurazione delle crittografie SSL, delle chiavi e della rinegoziazione come anche la validità del certificato.
- Utilizzare [safe-regex](https://www.npmjs.com/package/safe-regex) per assicurarsi che le espressioni regolari non siano suscettibili ad attacchi [regular expression denial of service](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/advanced/best-practice-security.md          )

---

# Sviluppo dei motori di template per Express

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Sviluppo dei motori di template per Express

Utilizzare il metodo `app.engine(ext, callback)` per creare il proprio motore di template. `ext` è l’estensione file e `callback` è la funzione del motore di template, la quale accetta le seguenti voci come parametri: l’ubicazione del file, l’oggetto delle opzioni e la funzione callback.

Il seguente codice è un esempio di implementazione di un motore di template molto semplice per il rendering del file `.ntl`.

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

L’applicazione sarà ora in grado di effettuare il rendering dei file `.ntl`. Creare un file denominato `index.ntl` nella directory `views` con il seguente contenuto.

```pug
#title#
#message#
```

Successivamente, creare il seguente percorso nell’applicazione.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Quando si effettua una richiesta per la home page, `index.ntl` verrà visualizzato come HTML.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### Esempio

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/it/advanced/healthcheck-graceful-shutdown.md          )
