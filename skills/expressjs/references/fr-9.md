# Utilisation de middleware and more

# Utilisation de middleware

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# Utilisation de middleware

Express est une infrastructure web middleware et de routage, qui a des fonctions propres minimes : une application Express n’est ni plus ni moins qu’une succession d’appels de fonctions middleware.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/fr/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/fr/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. La fonction middleware suivant est couramment désignée par une variable nommée `next`.

Les fonctions middleware effectuent les tâches suivantes :

- Exécuter tout type de code.
- Apporter des modifications aux objets de demande et de réponse.
- Terminer le cycle de demande-réponse.
- Appeler la fonction middleware suivant dans la pile.

Si la fonction middleware en cours ne termine pas le cycle de demande-réponse, elle doit appeler la fonction `next()` pour transmettre le contrôle à la fonction middleware suivant. Sinon, la demande restera bloquée.

Une application Express peut utiliser les types de middleware suivants :

- [Middleware niveau application](#middleware.application)
- [Middleware niveau routeur](#middleware.router)
- [Middleware de traitement d’erreurs](#middleware.error-handling)
- [Middleware intégré](#middleware.built-in)
- [Middleware tiers](#middleware.third-party)

Vous pouvez charger le middleware niveau application et niveau routeur à l’aide d’un chemin de montage facultatif.
Vous pouvez également charger une série de fonctions middleware ensemble, ce qui crée une sous-pile du système de middleware à un point de montage.

## Middleware niveau application

Bind application-level middleware to an instance of the [app object](https://expressjs.com/fr/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

Cet exemple illustre une fonction middleware sans chemin de montage. La fonction est exécutée à chaque fois que l’application reçoit une demande.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

Cet exemple illustre une fonction middleware montée sur le chemin `/user/:id`. La fonction est exécutée pour tout type de
demande HTTP sur le chemin`/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Cet exemple illustre une route et sa fonction de gestionnaire (système de middleware). La fonction gère les demandes GET adressées au chemin `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

Voici un exemple de chargement d’une série de fonctions middleware sur un point de montage, avec un chemin de montage.
Il illustre une sous-pile de middleware qui imprime les infos de demande pour tout type de demande HTTP adressée au chemin `/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Les gestionnaires de routage vous permettent de définir plusieurs routes pour un chemin. L’exemple ci-dessous définit deux routes pour les demandes GET adressées au chemin `/user/:id`. La deuxième route ne causera aucun problème, mais ne sera jamais appelée puisque la première route boucle le cycle demande-réponse.

Cet exemple illustre une sous-pile de middleware qui gère les demandes GET adressées au chemin `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  console.log('ID:', req.params.id)
  next()
}, (req, res, next) => {
  res.send('User Info')
})

// handler for the /user/:id path, which prints the user ID
app.get('/user/:id', (req, res, next) => {
  res.send(req.params.id)
})
```

Pour ignorer les fonctions middleware issues d’une pile de middleware de routeur, appelez `next('route')` pour passer le contrôle à la prochaine route.

Note

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

Cet exemple illustre une sous-pile de middleware qui gère les demandes GET adressées au chemin `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next route
  if (req.params.id === '0') next('route')
  // otherwise pass the control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // send a regular response
  res.send('regular')
})

// handler for the /user/:id path, which sends a special response
app.get('/user/:id', (req, res, next) => {
  res.send('special')
})
```

Middleware can also be declared in an array for reusability.

Voici un exemple d’utilisation de la fonction middleware `express.static` avec un objet options élaboré :

```
function logOriginalUrl (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}

function logMethod (req, res, next) {
  console.log('Request Type:', req.method)
  next()
}

const logStuff = [logOriginalUrl, logMethod]
app.get('/user/:id', logStuff, (req, res, next) => {
  res.send('User Info')
})
```

## Middleware niveau routeur

Le middleware niveau routeur fonctionne de la même manière que le middleware niveau application, à l’exception près qu’il est lié à une instance de `express.Router()`.

```
const router = express.Router()
```

Chargez le middleware niveau routeur par le biais des fonctions `router.use()` et `router.METHOD()`.

Le code d’exemple suivant réplique le système de middleware illustré ci-dessus pour le middleware niveau application, en utilisant un middleware niveau routeur :

```
const express = require('express')
const app = express()
const router = express.Router()

// a middleware function with no mount path. This code is executed for every request to the router
router.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})

// a middleware sub-stack shows request info for any type of HTTP request to the /user/:id path
router.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})

// a middleware sub-stack that handles GET requests to the /user/:id path
router.get('/user/:id', (req, res, next) => {
  // if the user ID is 0, skip to the next router
  if (req.params.id === '0') next('route')
  // otherwise pass control to the next middleware function in this stack
  else next()
}, (req, res, next) => {
  // render a regular page
  res.render('regular')
})

// handler for the /user/:id path, which renders a special page
router.get('/user/:id', (req, res, next) => {
  console.log(req.params.id)
  res.render('special')
})

// mount the router on the app
app.use('/', router)
```

Pour obtenir plus de détails sur la fonction `serve-static` et ses options, reportez-vous à la documentation [serve-static](https://github.com/expressjs/serve-static).

Cet exemple illustre une sous-pile de middleware qui gère les demandes GET adressées au chemin `/user/:id`.

```
const express = require('express')
const app = express()
const router = express.Router()

// predicate the router with a check and bail out when needed
router.use((req, res, next) => {
  if (!req.headers['x-auth']) return next('router')
  next()
})

router.get('/user/:id', (req, res) => {
  res.send('hello, user!')
})

// use the router and 401 anything falling through
app.use('/admin', router, (req, res) => {
  res.sendStatus(401)
})
```

## Middleware de traitement d'erreurs

Le middleware de traitement d’erreurs comporte toujours *quatre* arguments. Vous devez fournir quatre arguments pour l’identifier comme une fonction middleware de traitement d’erreurs. Même si vous n’avez pas besoin d’utiliser l’objet `next`, vous devez le spécifier pour maintenir la signature. Sinon, l’objet `next` sera interprété comme un middleware ordinaire et n’arrivera pas à gérer les erreurs.

Définissez les fonctions middleware de traitement d’erreurs de la même façon que d’autres fonctions middleware, à l’exception près qu’il faudra 4 arguments au lieu de 3, et plus particulièrement avec la signature `(err, req, res, next)`) :

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Pour obtenir des détails sur le middleware de traitement d’erreurs, reportez-vous à : [Traitement d’erreurs](https://expressjs.com/fr/guide/error-handling.html).

## Middleware intégré

Depuis la version 4.x, Express ne dépend plus de [Connect](https://github.com/senchalabs/connect). A l’exception de `express.static`, toutes les fonctions middleware
précédemment incluses à Express’ font désormais partie de modules distincts. Veuillez vous reporter à [la liste des fonctions middleware](https://github.com/senchalabs/connect#middleware).

La seule fonction middleware intégrée dans Express est `express.static`.

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Middleware tiers

Utilisez un middleware tiers pour ajouter des fonctionnalités à des applications Express.

Installez le module Node.js pour la fonctionnalité requise, puis chargez-le dans votre application au niveau application ou au niveau router.

L’exemple suivant illustre l’installation et le chargement de la fonction middleware d’analyse de cookie `cookie-parser`.

```
$ npm install cookie-parser
```

```
const express = require('express')
const app = express()
const cookieParser = require('cookie-parser')

// load the cookie-parsing middleware
app.use(cookieParser())
```

Pour obtenir une liste non exhaustive des fonctions middleware tiers utilisées couramment avec Express, reportez-vous à : [Middleware tiers](https://expressjs.com/fr/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/using-middleware.md          )

---

# Utilisation de moteurs de modèles avec Express

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Utilisation de moteurs de modèles avec Express

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/fr/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/fr/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, le répertoire dans lequel se trouvent les fichiers modèles. Par exemple : `app.set('views', './views')`
  This defaults to the `views` directory in the application root directory.
- `view engine`, le moteur de modèle à utiliser. Par exemple : `app.set('view engine', 'pug')`

Ensuite, installez le package npm du moteur de modèle correspondant :

```
$ npm install pug --save
```

Les moteurs de modèles conformes à Express tels que Pug exportent une fonction nommée `__express(filePath, options, callback)`, qui est appelée par la fonction `res.render()` pour générer le code de modèle.

Certaines moteurs de modèles ne suivent pas cette convention. La bibliothèque [Consolidate.js](https://www.npmjs.org/package/consolidate) suit cette convention en mappant tous les moteurs de modèles Node.js répandus, et fonctionne donc parfaitement avec Express.

Une fois le moteur de vue défini, vous n’avez pas à spécifier le moteur ou à charger le module de moteur de modèles dans votre application ; Express charge le module en interne, comme indiqué ci-dessous (pour l’exemple ci-dessus).

```
app.set('view engine', 'pug')
```

Créez un fichier de modèle Pug nommé `index.pug` dans le répertoire `views`, avec le contenu suivant :

```pug
html
  head
    title= title
  body
    h1= message
```

Puis, créez une route pour générer le fichier `index.pug`. Si la propriété `view engine` n’est pas définie, vous devez spécifier l’extension du fichier `view`. Sinon, vous pouvez l’omettre.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Lorsque vous faites une demande vers la page d’accueil, le fichier `index.pug` est généré en HTML.

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/using-template-engines.md          )

---

# Ecriture de middleware utilisable dans les applications Express

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Ecriture de middleware utilisable dans les applications Express

## Présentation

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/fr/5x/api.html#req) (`req`), the [response object](https://expressjs.com/fr/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. La fonction middleware suivant est couramment désignée par une variable nommée `next`.

Les fonctions middleware effectuent les tâches suivantes :

- Exécuter tout type de code.
- Apporter des modifications aux objets de demande et de réponse.
- Terminer le cycle de demande-réponse.
- Appeler le middleware suivant dans la pile.

Si la fonction middleware en cours ne termine pas le cycle de demande-réponse, elle doit appeler la fonction `next()` pour transmettre le contrôle à la fonction middleware suivant. Sinon, la demande restera bloquée.

L’exemple suivant montre les éléments d’un appel de fonction middleware:

|  | Méthode HTTP à laquelle la fonction middleware s'applique.</tbody>Chemin (route) auquel la fonction middleware s'applique.Fonction de middleware.Argument de rappel à la fonction middleware, appelée "next" par convention.HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/guide/writing-middleware.md          )

---

# Communauté

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# Communauté

## Technical committee

The Express technical committee meets online every two weeks (as needed) to discuss development and maintenance of Express,
and other issues relevant to the Express project. Each meeting is typically announced in an
[expressjs/discussions issue](https://github.com/expressjs/discussions/issues) with a link to join or view the meeting, which is
open to all observers.

The meetings are recorded; for a list of the recordings, see the [Express.js YouTube channel](https://www.youtube.com/channel/UCYjxjAeH6TRik9Iwy5nXw7g).

Members of the Express technical committee are:

**Active:**

- [@blakeembrey](https://github.com/blakeembrey) - Blake Embrey
- [@crandmck](https://github.com/crandmck) - Rand McKinney
- [@LinusU](https://github.com/LinusU) - Linus Unnebäck
- [@ulisesgascon](https://github.com/ulisesGascon) - Ulises Gascón
- [@sheplu](https://github.com/sheplu) - Jean Burellier
- [@wesleytodd](https://github.com/wesleytodd) - Wes Todd
- [@jonchurch](https://github.com/jonchurch) - Jon Church
- [@ctcpip](https://github.com/ctcpip/) - Chris de Almeida

**Inactive:**

- [@dougwilson](https://github.com/dougwilson) - Douglas Wilson
- [@hacksparrow](https://github.com/hacksparrow) - Hage Yaapa
- [@jonathanong](https://github.com/jonathanong) - jongleberry
- [@niftylettuce](https://github.com/niftylettuce) - niftylettuce
- [@troygoode](https://github.com/troygoode) - Troy Goode

## Express is made of many modules

Notre communauté si animée a créé une large gamme d’extensions,
[modules middleware](https://expressjs.com/fr/resources/middleware.html) et des
infrastructures de niveau supérieur.

Additionally, the Express community maintains modules in these two GitHub orgs:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/fr/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

To keep up with what is going on in the whole community, check out the [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## Problèmes

Si vous êtes tombé sur ce que vous pensez être un bug, ou si vous voulez seulement faire une demande
de fonctionnalité, ouvrez un ticket dans la [file d’attente d’incidents](https://github.com/expressjs/express/issues).

## Exemples

Regardez des douzaines d’[exemples](https://github.com/expressjs/express/tree/master/examples) d’applications Express dans le référentiel qui couvre tous les sujets, en allant de l’authentification et la conception de l’interface de
programme d’application jusqu’à l’intégration du moteur modèle.

## Github Discussions

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Branding of Express.js

## Express.js Logo

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotype

### Logomark

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/fr/resources/community.md          )
