# Meilleures pratiques en production : performances et fiabilité and more

# Meilleures pratiques en production : performances et fiabilité

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# Meilleures pratiques en production : performances et fiabilité

Cet article traite des meilleures pratiques en termes de performances et de fiabilité pour les applications Express déployées en production.

La présente rubrique s’inscrit clairement dans le concept “devops”, qui couvre à la fois le développement traditionnel et l’exploitation. Ainsi, les informations se divisent en deux parties :

- Things to do in your code (the dev part):
  - Utiliser le middleware pour exploiter les fichiers statiques
  - [Asynchronous Error Handling in Express with Promises, Generators and ES7](https://web.archive.org/web/20240000000000/https://strongloop.com/strongblog/async-error-handling-expressjs-es7-promises-generators/)
  - [Do logging correctly](#do-logging-correctly)
  - Traiter correctement les exceptions
- [A faire dans votre environnement/configuration](#env) (partie exploitation, “ops”).
  - Définir NODE_ENV sur “production”
  - Vérifier que votre application redémarre automatiquement
  - Exécuter votre application dans un cluster
  - [Cache request results](#cache-request-results)
  - Utilisation de StrongLoop PM avec un équilibreur de charge Nginx
  - Encore mieux, utilisez un proxy inverse pour exploiter les fichiers statiques ; pour plus d’informations, voir [Utiliser un proxy inverse](#proxy).

## A faire dans votre code

Les actions suivantes peuvent être réalisées dans votre code afin d’améliorer les performances de votre application :

- Utiliser le middleware pour exploiter les fichiers statiques
- [Asynchronous Error Handling in Express with Promises, Generators and ES7](https://web.archive.org/web/20240000000000/https://strongloop.com/strongblog/async-error-handling-expressjs-es7-promises-generators/)
- [Do logging correctly](#do-logging-correctly)
- Traiter correctement les exceptions

### Utiliser la compression gzip

La compression Gzip peut considérablement réduire la taille du corps de réponse et ainsi augmenter la vitesse d’une application Web. Utilisez le middleware [compression](https://www.npmjs.com/package/compression) pour la compression gzip dans votre application Express. Par exemple :

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

Pour un site Web en production dont le trafic est élevé, la meilleure méthode pour mettre en place la compression consiste à l’implémenter au niveau d’un proxy inverse (voir [Utiliser un proxy inverse](#proxy)). Dans ce cas, vous n’avez pas besoin d’utiliser le middleware compression. Pour plus de détails sur l’activation de la compression gzip dans Nginx, voir [Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) dans la documentation Nginx.

### Ne pas utiliser les fonctions synchrones

Les fonctions et les méthodes synchrones ralentissent le processus d’exécution jusqu’à leur retour. Un simple appel à une fonction synchrone peut revenir en quelques microsecondes ou millisecondes ; pour les sites Web dont le trafic est élevé, ces appels s’additionnent et réduisent les performances de l’application. Evitez de les utiliser en production.

Bien que Node et plusieurs modules mettent à disposition les versions synchrone et asynchrone de leurs fonctions, utilisez toujours la version asynchrone en production. L’utilisation d’une fonction synchrone n’est justifiée que lors du démarrage initial.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Bien entendu vous n’utiliserez pas réellement cette option en production, mais plutôt pour vérifier que votre code est prêt pour la phase production. Pour plus d’informations, voir [Weekly update for io.js 2.1.0](https://nodejs.org/en/blog/weekly-updates/weekly-update.2015-05-22/#2-1-0).

### Procéder à une journalisation correcte

En règle générale, vous utilisez la journalisation à partir de votre application à deux fins : le débogage et la journalisation de l’activité de votre application (principalement tout le reste). L’utilisation de `console.log()` ou de `console.err()` pour imprimer des messages de journal sur le terminal est une pratique courante en développement. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### Pour le débogage

Si vous utilisez la journalisation à des fins de débogage, utilisez un module de débogage spécial tel que [debug](https://www.npmjs.com/package/debug) plutôt que d’utiliser `console.log()`. Ce module vous permet d’utiliser la variable d’environnement DEBUG pour contrôler les messages de débogage envoyés à `console.err()`, le cas échéant. Pour que votre application reste exclusivement asynchrone, vous devrez toujours diriger `console.err()` vers un autre programme. Mais bon, vous n’allez pas vraiment procéder à un débogage en production, n’est-ce pas ?

#### Pour journaliser l’activité de votre application

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Traiter correctement les exceptions

Les applications Node plantent lorsqu’elles tombent sur une exception non interceptée. Si vous ne traitez pas les exceptions et ne prenez pas les décisions appropriées, votre application Express plantera et sera déconnectée. Si vous suivez les conseils de la rubrique ci-dessous intitulée [Vérifier que votre application redémarre automatiquement](#restart), votre application pourra être restaurée suite à un plantage. Le délai de démarrage des applications Express est heureusement court en règle générale. Vous souhaitez toutefois éviter tout plantage en priorité et pour ce faire, vous devez traiter les exceptions correctement.

Pour vérifier que vous traitez toutes les exceptions, procédez comme suit :

- [Utiliser try-catch](#try-catch)
- [Utiliser des promesses](#promises)

Avant de s’immerger dans les rubriques qui suivent, il est conseillé de posséder des connaissances de base concernant le traitement des erreurs Node/Express, à savoir l’utilisation des rappels “error-first” et la propagation des erreurs dans le middleware. Node utilise la convention de “rappel error-first” pour renvoyer les erreurs issues des fonctions asynchrones, dans laquelle le premier paramètre de la fonction callback est l’objet error, suivi par les données de résultat dans les paramètres suivants. Pour n’indiquer aucune erreur, indiquez null comme premier paramètre. La fonction de rappel doit suivre la convention de rappel “error-first” de sorte à traiter l’erreur de manière significative. Dans Express, la meilleure pratique consiste à utiliser la fonction next() pour propager les erreurs via la chaîne du middleware.

Pour plus d’informations sur les bases du traitement des erreurs, voir :

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Utiliser try-catch

Try-catch est un élément de langage JavaScript que vous pouvez utiliser pour intercepter les exceptions dans le code synchrone. Utilisez try-catch pour traiter les erreurs d’analyse JSON, comme indiqué ci-dessous, par exemple.

Voici un exemple d’utilisation de try-catch pour traiter une exception potentielle de plantage de processus.
Cette fonction middleware accepte un paramètre de zone de requête nommé “params” qui est un objet JSON.

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

Toutefois, try-catch ne fonctionne que dans le code synchrone. Etant donné que la plateforme Node est principalement asynchrone (en particulier dans un environnement de production), try-catch n’interceptera pas beaucoup d’exceptions.

#### Utiliser des promesses

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

#### A ne pas faire

Vous ne devriez *pas* écouter l’événement `uncaughtException`, émis lorsqu’une exception remonte vers la boucle d’événements. L’ajout d’un programme d’écoute d’événement pour `uncaughtException` va modifier le comportement par défaut du processus qui rencontre une exception ; le processus va continuer à s’exécuter malgré l’exception. Cela pourrait être un bon moyen d’empêcher votre application de planter, mais continuer à exécuter l’application après une exception non interceptée est une pratique dangereuse qui n’est pas recommandée, étant donné que l’état du processus devient peu fiable et imprévisible.

De plus, l’utilisation d’`uncaughtException` est officiellement reconnue comme étant [rudimentaire](https://nodejs.org/api/process.html#process_event_uncaughtexception) et il a été [proposé](https://github.com/nodejs/node-v0.x-archive/issues/2582) de le supprimer. Ecouter `uncaughtException` n’est qu’une mauvaise idée. Voilà pourquoi nous recommandons d’utiliser plusieurs processus et superviseurs à la place : faire planter son application et la redémarrer est souvent plus sûr que de la restaurer après une erreur.

L’utilisation de [domain](https://nodejs.org/api/domain.html) n’est également pas recommandée. Ce module obsolète ne résout globalement pas le problème.

## A faire dans votre environnement/configuration

Les actions suivantes peuvent être réalisées dans votre environnement système afin d’améliorer les performances de votre application :

- Définir NODE_ENV sur “production”
- Vérifier que votre application redémarre automatiquement
- Exécuter votre application dans un cluster
- [Cache request results](#cache-request-results)
- Utilisation de StrongLoop PM avec un équilibreur de charge Nginx
- Encore mieux, utilisez un proxy inverse pour exploiter les fichiers statiques ; pour plus d’informations, voir [Utiliser un proxy inverse](#proxy).

### Définir NODE_ENV sur “production”

La variable d’environnement NODE_ENV spécifie l’environnement dans lequel une application s’exécute (en règle générale, développement ou production). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

En définissant NODE_ENV sur “production”, Express :

- Met en cache les modèles d’affichage.
- Met en cache les fichiers CSS générés à partir d’extensions CSS.
- Génère moins de messages d’erreur prolixes.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

Si vous avez besoin d’écrire du code spécifique à un environnement, vous pouvez vérifier la valeur de NODE_ENV avec `process.env.NODE_ENV`. Sachez que la vérification de la valeur de n’importe quelle variable d’environnement pénalise les performances et devrait donc être effectuée avec modération.

En développement, vous définissez généralement les variables d’environnement dans votre shell interactif, à l’aide de `export` ou de votre fichier `.bash_profile` par exemple. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). La section qui suit fournit des détails sur l’utilisation de votre système init en général, mais la définition de NODE_ENV est tellement importante pour les performances (et facile à réaliser), qu’elle est mise en évidence ici.

Avec systemd, utilisez la directive `Environment` dans votre fichier d’unité. Par exemple :

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### Vérifier que votre application redémarre automatiquement

En production, vous ne souhaitez jamais que votre application soit déconnectée. Vous devez donc veiller à ce qu’elle redémarre si elle plante et si le serveur plante. Même si vous espérez que cela n’arrive pas, vous devez en réalité considérer ces deux éventualités en :

- Utilisant un gestionnaire de processus pour redémarrer l’application (et Node) lorsqu’elle plante.
- Utilisant le système init fourni par votre système d’exploitation pour redémarrer le gestionnaire de processus lorsque le système d’exploitation plante. Vous pouvez également utiliser le système init sans gestionnaire de processus.

Les applications Node plantent si elles tombent sur une exception non interceptée. Avant toute chose, vérifiez que votre application est correctement testée et qu’elle traite toutes les exceptions (voir [Traiter correctement les exceptions](#exceptions) pour plus de détails). En cas d’échec, mettez en place un mécanisme qui garantit que si et lorsque votre application plante, elle redémarre automatiquement.

#### Utiliser un gestionnaire de processus

En développement, vous avez simplement démarré votre application à partir de la ligne de commande avec `node server.js` ou une instruction similaire. En production, cela vous mènera droit au désastre. Si l’application plante, elle sera déconnectée tant que vous ne la redémarrerez pas. Pour garantir que votre application redémarre si elle plante, utilisez un gestionnaire de processus. Un gestionnaire de processus est un “conteneur” d’applications qui facilite le déploiement, offre une haute disponibilité et vous permet de gérer l’application lors de son exécution.

En plus de redémarrer votre application lorsqu’elle plante, un gestionnaire de processus peut vous permettre :

- De vous informer sur les performances d’exécution et la consommation des ressources.
- De modifier les paramètres de manière dynamique afin d’améliorer les performances.
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### Utiliser un système init

Le niveau de fiabilité suivant consiste à garantir que votre application redémarre lorsque le serveur redémarre. Les systèmes peuvent toujours tomber en panne pour divers motifs. Pour garantir que votre application redémarre si le serveur plante, utilisez le système init intégré à votre système d’exploitation. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

Vous pouvez utiliser les systèmes init de deux manières dans votre application Express :

- Exécutez votre application dans un gestionnaire de processus, puis installez le gestionnaire de processus en tant que service avec le système init. Le gestionnaire de processus va redémarrer votre application lorsqu’elle plantera et le système init va redémarrer le gestionnaire de processus lorsque le système d’exploitation redémarrera. Il s’agit de la méthode recommandée.
- Exécutez votre application (et Node) directement avec le système init. Cette méthode est plus simple, mais vous ne profitez pas des avantages d’un gestionnaire de processus.

##### Systemd

Systemd est un système Linux et un gestionnaire de services. La plupart des distributions Linux principales ont adopté systemd comme leur système init par défaut.

Un fichier de configuration de service systemd est appelé *fichier d’unité* et porte l’extension .service. Voici un exemple de fichier d’unité permettant de gérer une application Node directement (remplacez le texte en gras par les valeurs appropriées à votre système et votre application) : Replace the values enclosed in `<angle brackets>` for your system and app:

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

Pour plus d’informations sur systemd, voir la [page d’aide de systemd](http://www.freedesktop.org/software/systemd/man/systemd.unit.html).

### Exécuter votre application dans un cluster

Dans un système multicoeur, vous pouvez augmenter les performances d’une application Node en lançant un cluster de processus. Un cluster exécute plusieurs instances de l’application, idéalement une instance sur chaque coeur d’UC, répartissant ainsi la charge et les tâches entre les instances.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANT : étant donné que les instances d’application s’exécutent en tant que processus distincts, elles ne partagent pas le même espace mémoire. Autrement dit, les objets sont en local sur chaque instance de l’application. Par conséquent, vous ne pouvez pas conserver l’état dans le code de l’application. Vous pouvez toutefois utiliser un magasin de données en mémoire tel que [Redis](http://redis.io/) pour stocker les données de session et l’état. Cette fonctionnalité s’applique essentiellement à toutes les formes de mise à l’échelle horizontale, que la mise en cluster soit effectuée avec plusieurs processus ou avec plusieurs serveurs physiques.

Dans les applications mises en cluster, les processus de traitement peuvent planter individuellement sans impacter le reste des processus. Outre les avantages en termes de performance, l’isolement des pannes constitue une autre raison d’exécuter un cluster de processus d’application. Chaque fois qu’un processus de traitement plante, veillez toujours à consigner l’événement et à génération un nouveau processus à l’aide de cluster.fork().

#### Utilisation du module cluster de Node

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). Ce module permet à un processus maître de générer des processus de traitement et de répartir les connexions entrantes parmi ces processus.

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

### Mettre en cache les résultats d’une demande

Pour améliorer les performances en production, vous pouvez également mettre en cache le résultat des demandes, de telle sorte que votre application ne répète pas l’opération de traitement de la même demande plusieurs fois.

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### Utiliser un équilibreur de charge

Quel que soit le niveau d’optimisation d’une application, une instance unique ne peut traiter qu’un volume limité de charge et de trafic. Pour faire évoluer une application, vous pouvez exécuter plusieurs instances de cette application et répartir le trafic en utilisant un équilibreur de charge. La configuration d’un équilibreur de charge peut améliorer les performances et la vitesse de votre application et lui permettre d’évoluer plus largement qu’avec une seule instance.

Un équilibreur de charge est généralement un proxy inverse qui orchestre le trafic entrant et sortant de plusieurs instances d’application et serveurs. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

Avec l’équilibrage de charge, vous devrez peut-être vérifier que les demandes associées à un ID de session spécifique sont connectées au processus dont elles sont issues. Ce procédé est appelé *affinité de session* (ou *sessions persistantes*) et peut être effectué en utilisant un magasin de données tel que Redis pour les données de session (en fonction de votre application), comme décrit ci-dessus. Pour en savoir plus, voir [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### Utiliser un proxy inverse

Un proxy inverse accompagne une application Web et exécute des opérations de prise en charge sur les demandes, en plus de diriger les demandes vers l’application. Il peut gérer les pages d’erreur, la compression, la mise en cache, le dépôt de fichiers et l’équilibrage de charge entre autres.

La transmission de tâches qui ne requièrent aucune connaissance de l’état d’application à un proxy inverse permet à Express de réaliser des tâches d’application spécialisées. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/advanced/best-practice-performance.md          )

---

# Meilleures pratiques en production : Sécurité

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# Meilleures pratiques en production : Sécurité

## Présentation

Le terme *“production”* fait référence à la phase du cycle de vie du logiciel au cours de laquelle une application ou une API est généralement disponible pour ses consommateurs ou utilisateurs finaux. En revanche, en phase de *“développement”*, l’écriture et le test de code se poursuivent activement et l’application n’est pas ouverte pour un accès externe. Les environnements système correspondants sont respectivement appelés environnement de *production* et environnement de *développement*.

Les environnements de développement et de production sont généralement configurés différemment et leurs exigences divergent grandement. Ce qui convient parfaitement en développement peut être inacceptable en production. Par exemple, dans un environnement de développement, vous pouvez souhaiter une consignation prolixe des erreurs en vue du débogage, alors que ce type de comportement présente des risques au niveau de sécurité en environnement de production. De plus, en environnement de développement, vous n’avez pas à vous soucier de l’extensibilité, de la fiabilité et des performances, tandis que ces éléments sont essentiels en environnement de production.

Note

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

Cet article traite des meilleures pratiques en terme de sécurité pour les applications Express déployées en production.

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [hsts](https://github.com/helmetjs/hsts) définit l’en-tête `Strict-Transport-Security` qui impose des connexions (HTTP sur SSL/TLS) sécurisées au serveur.
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [hidePoweredBy](https://github.com/helmetjs/hide-powered-by) supprime l’en-tête `X-Powered-By`.
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - [xssFilter](https://github.com/helmetjs/x-xss-protection) définit `X-XSS-Protection` afin d’activer le filtre de script intersites (XSS) dans les navigateurs Web les plus récents.
    - [noCache](https://github.com/helmetjs/nocache) définit des en-têtes `Cache-Control` et Pragma pour désactiver la mise en cache côté client.
    - [ieNoOpen](https://github.com/helmetjs/ienoopen) définit `X-Download-Options` pour IE8+.
  - [Prevent brute-force attacks against authorization](#prevent-brute-force-attacks-against-authorization)
  - [Ensure your dependencies are secure](#ensure-your-dependencies-are-secure)
    - Désactivez au minimum l’en-tête X-Powered-By
  - [Additional considerations](#additional-considerations)

## N’utilisez pas de versions obsolètes ou vulnérables d’Express

Les versions 2.x et 3.x d’Express ne sont plus prises en charge. Les problèmes liés à la sécurité et aux performances dans ces versions ne seront pas corrigés. Ne les utilisez pas ! Si vous êtes passé à la version 4, suivez le [guide de migration](https://expressjs.com/fr/guide/migrating-4.html).

Vérifiez également que vous n’utilisez aucune des versions vulnérables d’Express répertoriées sur la [page Mises à jour de sécurité](https://expressjs.com/fr/advanced/security-updates.html). Si tel est le cas, procédez à une mise à jour vers une version stable, de préférence la plus récente.

## Utilisez TLS

Si votre application traite ou transmet des données sensibles, utilisez [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) (Transport Layer Security) afin de sécuriser la connexion et les données. Cette technologie de l’information chiffre les données avant de les envoyer du client au serveur, ce qui vous préserve des risques d’hameçonnage les plus communs (et faciles). Même si les requêtes Ajax et POST ne sont pas clairement visibles et semblent “masquées” dans les navigateurs, leur trafic réseau n’est pas à l’abri d’une [détection de paquet](https://en.wikipedia.org/wiki/Packet_analyzer) ni des [attaques d’intercepteur](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

Vous connaissez sans doute le chiffrement SSL (Secure Socket Layer). [TLS est simplement une évolution de SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). En d’autres termes, si vous utilisiez SSL auparavant, envisagez de passer à TLS. Nous recommandons généralement Nginx pour gérer TLS. Pour des informations de référence fiables concernant la configuration de TLS sur Nginx (et d’autres serveurs), voir [Configurations de serveur recommandées (wiki Mozilla)](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

Par ailleurs, un outil très pratique, [Let’s Encrypt](https://letsencrypt.org/about/), autorité de certification gratuite, automatisée et ouverte fournie par le groupe de recherche sur la sécurité sur Internet, [ISRG (Internet Security Research Group)](https://letsencrypt.org/isrg/), vous permet de vous procurer gratuitement un certificat TLS.

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

## Utilisez Helmet

[Helmet](https://www.npmjs.com/package/helmet) vous aide à protéger votre application de certaines des vulnérabilités bien connues du Web en configurant de manière appropriée des en-têtes HTTP.

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/fr/advanced/Si vous utilisez `helmet.js`, cette opération s'effectue automatiquement.).

Installez Helmet comme n’importe quel autre module :

```
$ npm install helmet
```

Puis, pour l’utiliser dans votre code :

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

## Utilisez les cookies de manière sécurisée

Pour garantir que les cookies n’ouvrent pas votre application aux attaques, n’utilisez pas le nom du cookie de session par défaut et définissez de manière appropriée des options de sécurité des cookies.

Il existe deux modules principaux de session de cookie de middleware :

- [express-session](https://www.npmjs.com/package/express-session) qui remplace le middleware `express.session` intégré à Express 3.x.
- [cookie-session](https://www.npmjs.com/package/cookie-session) qui remplace le middleware `express.cookieSession` intégré à Express 3.x.

La principale différence entre ces deux modules tient à la manière dont ils sauvegardent les données de session des cookies. Le middleware [express-session](https://www.npmjs.com/package/express-session) stocke les données de session sur le serveur ; il ne sauvegarde que l’ID session dans le cookie lui-même, mais pas les données de session. Par défaut, il utilise le stockage en mémoire et n’est pas conçu pour un environnement de production. En production, vous devrez configurer un magasin de sessions évolutif (voir la liste des [magasins de sessions compatibles](https://github.com/expressjs/session#compatible-session-stores)).

En revanche, le middleware [cookie-session](https://www.npmjs.com/package/cookie-session) implémente un stockage sur cookie, c’est-à-dire qu’il sérialise l’intégralité de la session sur le cookie, et non simplement une clé de session. Utilisez-le uniquement lorsque les données de session sont relativement peu nombreuses et faciles à coder sous forme de valeurs primitives (au lieu d’objets). Même si les navigateurs sont censés prendre en charge au moins 4096 octets par cookie, pour ne pas risquer de dépasser cette limite, limitez-vous à 4093 octets par domaine. De plus, n’oubliez pas que les données de cookie seront visibles du client et que s’il n’est pas nécessaire qu’elles soient sécurisées ou illisibles, express-session est probablement la meilleure solution.

### N’utilisez pas de nom de cookie de session par défaut

L’utilisation d’un nom de cookie de session par défaut risque d’ouvrir votre application aux attaques. Le problème de sécurité qui en découle est similaire à `X-Powered-By` : une personne potentiellement malveillante peut l’utiliser pour s’identifier auprès du serveur et cibler ses attaques en conséquence.

Pour éviter ce problème, utilisez des noms de cookie génériques, par exemple à l’aide du middleware [express-session](https://www.npmjs.com/package/express-session) :

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Définissez des options de sécurité de cookie

Définissez les options de cookie suivantes pour accroître la sécurité :

- `secure` - Garantit que le navigateur n’envoie le cookie que sur HTTPS.
- `httpOnly` - Garantit que le cookie n’est envoyé que sur HTTP(S), pas au JavaScript du client, ce qui renforce la protection contre les attaques de type cross-site scripting.
- `domain` - Indique le domaine du cookie ; utilisez cette option pour une comparaison avec le domaine du serveur dans lequel l’URL est demandée. S’ils correspondent, vérifiez ensuite l’attribut de chemin.
- `path` - Indique le chemin du cookie ; utilisez cette option pour une comparaison avec le chemin demandé. Si le chemin et le domaine correspondent, envoyez le cookie dans la demande.
- `expires` - Utilisez cette option pour définir la date d’expiration des cookies persistants.

Exemple d’utilisation du middleware [cookie-session](https://www.npmjs.com/package/cookie-session) :

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

## Implémentez la limitation de débit pour empêcher les attaques de force brute liées à l’authentification.

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

### Eviter les autres vulnérabilités connues

Gardez un oeil sur les recommandations [Node Security Project](https://npmjs.com/advisories) qui peuvent concerner Express ou d’autres modules utilisés par votre application. En règle générale, Node Security Project est une excellente ressource de connaissances et d’outils sur la sécurité de Node.

Pour finir, les applications Express - comme toutes les autres applications Web - peuvent être vulnérables à une variété d’attaques Web. Familiarisez vous avec les [vulnérabilités Web](https://www.owasp.org/www-project-top-ten/) connues et prenez des précautions pour les éviter.

## Autres considérations

Voici d’autres recommandations issues de l’excellente [liste de contrôle de sécurité Node.js](https://blog.risingstack.com/node-js-security-checklist/). Pour tous les détails sur ces recommandations, reportez-vous à cet article de blogue :

- Filtrez et nettoyez toujours les entrées utilisateur pour vous protéger contre les attaques de cross-site scripting (XSS) et d’injection de commande.
- Défendez-vous contre les attaques par injection SQL en utilisant des requêtes paramétrées ou des instructions préparées.
- Utilisez l’outil [sqlmap](http://sqlmap.org/) à code source ouvert pour détecter les vulnérabilités par injection SQL dans votre application.
- Utilisez les outils [nmap](https://nmap.org/) et [sslyze](https://github.com/nabla-c0d3/sslyze) pour tester la configuration de vos chiffrements, clés et renégociations SSL, ainsi que la validité de votre certificat.
- Utilisez [safe-regex](https://www.npmjs.com/package/safe-regex) pour s’assurer que vos expressions régulières ne sont pas exposées à des attaques ReDoS ([regular expression denial of service](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS)).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/advanced/best-practice-security.md          )

---

# Développement de moteurs de modèles pour Express

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Développement de moteurs de modèles pour Express

Utilisez la méthode `app.engine(ext, callback)` pour créer votre propre moteur de modèle. `ext` fait référence à l’extension de fichier et `callback` est la fonction du moteur de modèle, qui accepte les éléments suivants en tant que paramètres : l’emplacement du fichier, l’objet options et la fonction callback.

Le code suivant est un exemple d’implémentation d’un moteur de modèle très simple qui permet d’afficher le rendu des fichiers `.ntl`.

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

Votre application est désormais en mesure d’afficher le rendu des fichiers `.ntl`. Créez un fichier nommé  `index.ntl` dans le répertoire `views` avec le contenu suivant.

```pug
#title#
#message#
```

ENsuite, créez la route suivante dans votre application.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Lorsque vous effectuerez une demande à la page d’accueil, `index.ntl` sera rendu au format HTML.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### Exemple

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/advanced/healthcheck-graceful-shutdown.md          )
