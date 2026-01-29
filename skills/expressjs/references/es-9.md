# Utilización del middleware and more

# Utilización del middleware

> Learn how to use middleware in Express.js applications, including application-level and router-level middleware, error handling, and integrating third-party middleware.

# Utilización del middleware

Express es una infraestructura web de direccionamiento y middleware que tiene una funcionalidad mínima propia: una aplicación Express es fundamentalmente una serie de llamadas a funciones de middleware.

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/es/5x/api.html#req)  (`req`), the [response object](https://expressjs.com/es/5x/api.html#res) (`res`), and the next middleware function in the application’s request-response cycle. La siguiente función de middleware se denota normalmente con una variable denominada `next`.

Las funciones de middleware pueden realizar las siguientes tareas:

- Execute any code.
- Realizar cambios en la solicitud y los objetos de respuesta.
- Finalizar el ciclo de solicitud/respuestas.
- Invocar la siguiente función de middleware en la pila.

Si la función de middleware actual no finaliza el ciclo de solicitud/respuestas, debe invocar `next()` para pasar el control a la siguiente función de middleware. Otherwise, the request will be left hanging.

An Express application can use the following types of middleware:

- [Application-level middleware](#middleware.application)
- [Middleware de nivel de direccionador](#middleware.router)
- [Error-handling middleware](#middleware.error-handling)
- [Built-in middleware](#middleware.built-in)
- [Third-party middleware](#middleware.third-party)

Puede cargar middleware de nivel de aplicación y de nivel de direccionador con una vía de acceso de montaje opcional.
También puede cargar una serie de funciones de middleware a la vez, lo que crea una subpila del sistema de middleware en un punto de montaje.

## Application-level middleware

Bind application-level middleware to an instance of the [app object](https://expressjs.com/es/5x/api.html#app) by using the `app.use()` and `app.METHOD()` functions, where `METHOD` is the HTTP method of the request that the middleware function handles (such as GET, PUT, or POST) in lowercase.

Este ejemplo muestra una función de middleware sin ninguna vía de acceso de montaje. The function is executed every time the app receives a request.

```
const express = require('express')
const app = express()

app.use((req, res, next) => {
  console.log('Time:', Date.now())
  next()
})
```

Este ejemplo muestra una función de middleware montada en la vía de acceso `/user/:id`. La función se ejecuta para cualquier tipo de solicitud HTTP en la vía de acceso `/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Este ejemplo muestra una ruta y su función de manejador (sistema de middleware). La función maneja las solicitudes GET a la vía de acceso `/user/:id`.

```
app.get('/user/:id', (req, res, next) => {
  res.send('USER')
})
```

A continuación, se muestra un ejemplo de carga de una serie de funciones de middleware en un punto de montaje, con una vía de acceso de montaje.
Ilustra una subpila de middleware que imprime información de solicitud para cualquier tipo de solicitud HTTP en la vía de acceso `/user/:id`.

```
app.use('/user/:id', (req, res, next) => {
  console.log('Request URL:', req.originalUrl)
  next()
}, (req, res, next) => {
  console.log('Request Type:', req.method)
  next()
})
```

Los manejadores de rutas permiten definir varias rutas para una vía de acceso. El ejemplo siguiente define dos rutas para las solicitudes GET a la vía de acceso `/user/:id`. La segunda ruta no dará ningún problema, pero nunca se invocará, ya que la primera ruta finaliza el ciclo de solicitud/respuestas.

Este ejemplo muestra una subpila de middleware que maneja solicitudes GET a la vía de acceso `/user/:id`.

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

Para omitir el resto de las funciones de middleware de una pila de middleware de direccionador, invoque `next('route')` para pasar el control a la siguiente ruta.

Nota

`next('route')` will work only in middleware functions that were loaded by using the `app.METHOD()` or `router.METHOD()` functions.

Este ejemplo muestra una subpila de middleware que maneja solicitudes GET a la vía de acceso `/user/:id`.

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

A continuación, se muestra un ejemplo de uso de la función de middleware `express.static` con un objeto de opciones elaboradas:

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

## Middleware de nivel de direccionador

El middleware de nivel de direccionador funciona de la misma manera que el middleware de nivel de aplicación, excepto que está enlazado a una instancia de `express.Router()`.

```
const router = express.Router()
```

Cargue el middleware de nivel de direccionador utilizando las funciones `router.use()` y `router.METHOD()`.

El siguiente código de ejemplo replica el sistema de middleware que se ha mostrado anteriormente para el middleware de nivel de aplicación, utilizando el middleware de nivel de direccionador:

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

Para obtener más detalles sobre la función `serve-static` y sus opciones, consulte la documentación de [serve-static](https://github.com/expressjs/serve-static).

Este ejemplo muestra una subpila de middleware que maneja solicitudes GET a la vía de acceso `/user/:id`.

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

## Error-handling middleware

El middleware de manejo de errores siempre utiliza *cuatro* argumentos. Debe proporcionar cuatro argumentos para identificarlo como una función de middleware de manejo de errores. Aunque no necesite utilizar el objeto `next`, debe especificarlo para mantener la firma. De lo contrario, el objeto `next` se interpretará como middleware normal y no podrá manejar errores.

Defina las funciones de middleware de manejo de errores de la misma forma que otras funciones de middleware, excepto con cuatro argumentos en lugar de tres, específicamente con la firma `(err, req, res, next)`:

```
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

Para obtener detalles sobre el middleware de manejo de errores, consulte: [Manejo de errores](https://expressjs.com/es/guide/error-handling.html).

## Built-in middleware

Desde la versión 4.x, Express ya no depende de [Connect](https://github.com/senchalabs/connect). Excepto `express.static`, todas las funciones de middleware que se incluían previamente con Express están ahora en módulos diferentes. Consulte [la lista de funciones de middleware](https://github.com/senchalabs/connect#middleware).

La única función de middleware incorporado en Express es `express.static`.

- [express.static](https://expressjs.com/en/5x/api.html#express.static) serves static assets such as HTML files, images, and so on.
- [express.json](https://expressjs.com/en/5x/api.html#express.json) parses incoming requests with JSON payloads. **NOTE: Available with Express 4.16.0+**
- [express.urlencoded](https://expressjs.com/en/5x/api.html#express.urlencoded) parses incoming requests with URL-encoded payloads.  **NOTE: Available with Express 4.16.0+**

## Third-party middleware

Utilice el middleware de terceros para añadir funcionalidad a las aplicaciones Express.

Instale el módulo Node.js para la funcionalidad necesaria y cárguelo en la aplicación a nivel de aplicación o a nivel de direccionador.

El siguiente ejemplo ilustra la instalación y carga de la función de middleware de análisis de cookies `cookie-parser`.

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

Para ver una lista parcial de las funciones de middleware de terceros que más se utilizan con Express, consulte: [Middleware de terceros](https://expressjs.com/es/resources/middleware.html).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/using-middleware.md          )

---

# Utilización de motores de plantilla con Express

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Utilización de motores de plantilla con Express

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/es/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/es/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, el directorio donde se encuentran los archivos de plantilla. Ejemplo: `app.set('views', './views')`
  This defaults to the `views` directory in the application root directory.
- `view engine`, el motor de plantilla que se utiliza. Ejemplo: `app.set('view engine', 'pug')`

A continuación, instale el paquete npm de motor de plantilla correspondiente:

```
$ npm install pug --save
```

Express-compliant template engines such as Pug export a function named `__express(filePath, options, callback)`,
which `res.render()` calls to render the template code.

Some template engines do not follow this convention. The [@ladjs/consolidate](https://www.npmjs.com/package/@ladjs/consolidate)
library follows this convention by mapping all of the popular Node.js template engines, and therefore works seamlessly within Express.

After the view engine is set, you don’t have to specify the engine or load the template engine module in your app;
Express loads the module internally, for example:

```
app.set('view engine', 'pug')
```

Cree un archivo de plantilla Pug denominado `index.pug` en el directorio `views`, con el siguiente contenido:

```pug
html
  head
    title= title
  body
    h1= message
```

A continuación, cree una ruta para representar el archivo `index.pug`. Si la propiedad `view engine` no se establece, debe especificar la extensión del archivo `view`. De lo contrario, puede omitirla.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Cuando realice una solicitud a la página de inicio, el archivo `index.pug` se representará como HTML.

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/using-template-engines.md          )

---

# Escritura de middleware para su uso en aplicaciones Express

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Escritura de middleware para su uso en aplicaciones Express

## Overview

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/es/5x/api.html#req) (`req`), the [response object](https://expressjs.com/es/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. La siguiente función de middleware se denota normalmente con una variable denominada `next`.

Las funciones de middleware pueden realizar las siguientes tareas:

- Execute any code.
- Realizar cambios en la solicitud y los objetos de respuesta.
- Finalizar el ciclo de solicitud/respuestas.
- Invocar el siguiente middleware en la pila.

Si la función de middleware actual no finaliza el ciclo de solicitud/respuestas, debe invocar `next()` para pasar el control a la siguiente función de middleware. Otherwise, the request will be left hanging.

El siguiente ejemplo muestra los elementos de una llamada a función de middleware:

|  | Método HTTP para el que se aplica la función de middleware.</tbody>Vía de acceso (ruta) para la que se aplica la función de middleware.La función de middleware.Argumento de devolución de llamada a la función de middleware, denominado "next" por convención.HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/guide/writing-middleware.md          )

---

# Comunidad

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# Comunidad

## Technical committee

El comité técnico de Express se reúne en línea cada dos semanas (según sea necesario) para discutir el desarrollo y el mantenimiento de Express, entre otros problemas relevantes para el proyecto Express. Cada reunión se anuncia normalmente en un [problema de expressjs/discussions](https://github.com/expressjs/discussions/issues) con un enlace para unirse o ver la reunión, que está abierta a todos los observadores.

Las reuniones son grabadas; para ver la lista de las grabaciones, consulte el [canal de YouTube de Express.js](https://www.youtube.com/channel/UCYjxjAeH6TRik9Iwy5nXw7g).

Los miembros del comité técnico de Express son:

**Activos:**

- [@blakeembrey](https://github.com/blakeembrey) - Blake Embrey
- [@crandmck](https://github.com/crandmck) - Rand McKinney
- [@LinusU](https://github.com/LinusU) - Linus Unnebäck
- [@ulisesgascon](https://github.com/ulisesGascon) - Ulises Gascón
- [@sheplu](https://github.com/sheplu) - Jean Burellier
- [@wesleytodd](https://github.com/wesleytodd) - Wes Todd
- [@jonchurch](https://github.com/jonchurch) - Jon Church
- [@ctcpip](https://github.com/ctcpip/) - Chris de Almeida

**Inactivos:**

- [@dougwilson](https://github.com/dougwilson) - Douglas Wilson
- [@hacksparrow](https://github.com/hacksparrow) - Hage Yaapa
- [@jonathanong](https://github.com/jonathanong) - jongleberry
- [@niftylettuce](https://github.com/niftylettuce) - niftylettuce
- [@troygoode](https://github.com/troygoode) - Troy Goode

## Express is made of many modules

Nuestra vibrante comunidad ha creado una larga variedad de extensiones, [módulos intermedios](https://expressjs.com/es/resources/middleware.html) y frameworks de nivel superior.

Además, la comunidad de Express mantiene módulos en estas dos organizaciones de GitHub:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/es/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

Para mantenerse al tanto de lo que está sucediendo en toda la comunidad, consulte [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## Issues

Si ha encontrado lo que cree que es un error, o simplemente quiere hacer una solicitud de función, abre un ticket en la [cola de problemas](https://github.com/expressjs/express/issues).

## Examples

Mire docenas de [ejemplos](https://github.com/expressjs/express/tree/master/examples) de aplicaciones Express en el repositorio que cubren todo, desde el diseño y la autenticación de API hasta la integración del motor de plantillas.

## Discusiones de Github

La sección de [Discusiones de GitHub](https://github.com/expressjs/discussions) es un excelente espacio para participar en conversaciones sobre el desarrollo y mantenimiento de Express, así como para compartir ideas y debatir temas relacionados con su uso.

# Branding of Express.js

## Logo de Express.js

Express is a project of the OpenJS Foundation. Por favor, revise la [política de marcas registradas](https://trademark-policy.openjsf.org/) para obtener información sobre el uso permitido de los logotipos y marcas de Express.js.

### Logotype

### Logo de Marca

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/resources/community.md          )
