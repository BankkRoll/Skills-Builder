# Production best practices: performance and reliability and more

# Production best practices: performance and reliability

> Discover performance and reliability best practices for Express apps in production, covering code optimizations and environment setups for optimal performance.

# Production best practices: performance and reliability

En este artículo se describen las mejores prácticas de rendimiento y fiabilidad para las aplicaciones Express desplegadas en producción.

Este tema entra claramente dentro del área de “DevOps”, que abarca operaciones y desarrollos tradicionales. Por lo tanto, la información se divide en dos partes:

- Cosas que hacer en el código (la parte de desarrollo):
  - [Utilizar la compresión de gzip](#utilizar-la-compresión-de-gzip)
  - [No utilizar funciones síncronas](#no-utilizar-funciones-síncronas)
  - [Realizar un registro correcto](#realizar-un-registro-correcto)
  - [Manejar las excepciones correctamente](#manejar-las-excepciones-correctamente)
- Cosas que hacer en el entorno / configuración (la parte de operaciones):
  - [Establecer NODE_ENV en “production”](#establecer-node_env-en-production)
  - [Asegurarse de que la aplicación se reinicia automáticamente](#asegurarse-de-que-la-aplicación-se-reinicia-automáticamente)
  - [Ejecutar la aplicación en un clúster](#ejecutar-la-aplicación-en-un-clúster)
  - [Almacenar en la caché los resultados de la solicitud](#almacenar-en-la-caché-los-resultados-de-la-solicitud)
  - [Utilizar un equilibrador de carga](#utilizar-un-equilibrador-de-carga)
  - [Utilizar un proxy inverso](#utilizar-un-proxy-inverso)

## Cosas que hacer en el código

Estas son algunas de las cosas que puede hacer en el código para mejorar el rendimiento de la aplicación:

- [Utilizar la compresión de gzip](#utilizar-la-compresión-de-gzip)
- [No utilizar funciones síncronas](#no-utilizar-funciones-síncronas)
- [Realizar un registro correcto](#realizar-un-registro-correcto)
- [Manejar las excepciones correctamente](#manejar-las-excepciones-correctamente)

### Utilizar la compresión de gzip

La compresión de gzip puede disminuir significativamente el tamaño del cuerpo de respuesta y, por lo tanto, aumentar la velocidad de una aplicación web. Utilice el middleware de [compresión](https://www.npmjs.com/package/compression) para la compresión de gzip en la aplicación Express. For example:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

Para un sitio web con un tráfico elevado en producción, la mejor forma de aplicar la compresión es implementarla como un nivel de proxy inverso (consulte [Utilizar un proxy inverso](#proxy)). En este caso, no es necesario utilizar el middleware de compresión. Para obtener detalles sobre cómo habilitar la compresión de gzip en Nginx, consulte [Module ngx_http_gzip_module](http://nginx.org/en/docs/http/ngx_http_gzip_module.html) en la documentación de Nginx.

### No utilizar funciones síncronas

Las funciones síncronas y los métodos impiden el avance del proceso de ejecución hasta que vuelven. Una llamada individual a una función síncrona puede volver en pocos microsegundos o milisegundos, aunque en sitios web de tráfico elevado, estas llamadas se suman y reducen el rendimiento de la aplicación. Evite su uso en producción.

Aunque Node y muchos módulos proporcionan versiones síncronas y asíncronas de las funciones, utilice siempre la versión asíncrona en producción. La única vez que está justificado utilizar una función síncrona es en el arranque inicial.

You can use the `--trace-sync-io` command-line flag to print a warning and a stack trace whenever your application uses a synchronous API. Desde luego, no deseará utilizarlo en producción, sólo para garantizar que el código está listo para producción. Consulte [Weekly update for io.js 2.1.0](https://nodejs.org/en/blog/weekly-updates/weekly-update.2015-05-22/#2-1-0) para obtener más información.

### Realizar un registro correcto

En general, hay dos motivos para realizar un registro desde la aplicación: a efectos de depuración o para registrar la actividad de la aplicación (básicamente, todo lo demás). El uso de `console.log()` o `console.err()` para imprimir mensajes de registro en el terminal es una práctica común en el desarrollo. But [these functions are synchronous](https://nodejs.org/api/console.html#console) when the destination is a terminal or a file, so they are not suitable for production, unless you pipe the output to another program.

#### For debugging

Si realiza el registro a efectos de depuración, en lugar de utilizar `console.log()`, utilice un módulo de depuración especial como [debug](https://www.npmjs.com/package/debug). Este módulo permite utilizar la variable de entorno DEBUG para controlar qué mensajes de depuración se envían a `console.err()`, si se envía alguno. Para mantener la aplicación básicamente asíncrona, deberá canalizar `console.err()` a otro programa. Pero en este caso, realmente no va a depurar en producción, ¿no?

#### Para la actividad de la aplicación

If you’re logging app activity (for example, tracking traffic or API calls), instead of using `console.log()`, use a logging library like [Pino](https://www.npmjs.com/package/pino), which is the fastest and most efficient option available.

### Manejar las excepciones correctamente

Las aplicaciones Node se bloquean cuando encuentran una excepción no capturada. Si no maneja las excepciones ni realiza las acciones necesarias, la aplicación Express se bloqueará y quedará fuera de línea. Si sigue el consejo de [Asegurarse de que la aplicación se reinicia automáticamente](#restart) más abajo, la aplicación se recuperará de un bloqueo. Afortunadamente, las aplicaciones Express normalmente necesitan un breve tiempo de arranque. No obstante, desea evitar el bloqueo en primer lugar y, para ello, deberá manejar correctamente las excepciones.

Para asegurarse de manejar todas las excepciones, siga estas técnicas:

- [Utilizar try-catch](#try-catch)
- [Utilizar promesas](#utilizar-promesas)

Antes de profundizar en estos temas, deberá tener unos conocimientos básicos del manejo de errores de Node/Express: el uso de devoluciones de llamada error-first y la propagación de errores en el middleware. Node utiliza un convenio de “devolución de llamada error-first” para devolver los errores de las funciones asíncronas, donde el primer parámetro en la función de devolución de llamada es el objeto de error, seguido de los datos de resultados en los parámetros posteriores. Para indicar que no hay ningún error, pase null como el primer parámetro. La función de devolución de llamada debe seguir por lo tanto el convenio de devolución de llamada error-first para manejar correctamente el error. En Express, la práctica recomendada es utilizar la función next() para propagar los errores a través de la cadena de middleware.

Para obtener más información sobre los aspectos básicos del manejo de errores, consulte:

- [Error Handling in Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Utilizar try-catch

Try-catch es una construcción de lenguaje JavaScript que puede utilizar para capturar excepciones en código síncrono. Por ejemplo, utilice try-catch para manejar los errores de análisis de JSON, como se muestra a continuación.

A continuación, se muestra un ejemplo de uso de try-catch para manejar una posible excepción de bloqueo de proceso.
Esta función de middleware acepta un parámetro de campo de consulta denominado “params” que es un objeto JSON.

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

No obstante, try-catch sólo funciona para el código síncrono. Como la plataforma de Node es principalmente asíncrona (particularmente en un entorno de producción), try-catch no capturará muchas excepciones.

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

#### Qué no debe hacer

Algo que *no* debe hacer es escuchar el suceso `uncaughtException`, que se emite cuando una excepción se reproduce hacia atrás en el bucle de sucesos. La adición de un escucha de sucesos para `uncaughtException` cambiará el comportamiento predeterminado del proceso que se encuentra con la excepción; el proceso continuará ejecutándose a pesar de la excepción. Esto puede parecer una buena forma de evitar el bloqueo de la aplicación, pero continuar ejecutando la aplicación después de una excepción no capturada es una práctica peligrosa y no se recomienda, ya que el estado del proceso se vuelve imprevisible y poco fiable.

Asimismo, el uso de `uncaughtException` se reconoce oficialmente como un mecanismo [arduo](https://nodejs.org/api/process.html#process_event_uncaughtexception) y hay una [propuesta](https://github.com/nodejs/node-v0.x-archive/issues/2582) para eliminarlo del núcleo. Por lo tanto, la escucha `uncaughtException` no es una buena idea. Es por esto por lo que se recomiendan varios procesos y supervisores; el bloqueo y el reinicio es a menudo la forma más fiable de recuperarse de un error.

Tampoco se recomienda el uso de [dominios](https://nodejs.org/api/domain.html). Generalmente no soluciona el problema y es un módulo en desuso.

## Cosas que hacer en el entorno / configuración

Estas son algunas de las cosas que puede hacer en el entorno del sistema para mejorar el rendimiento de la aplicación:

- [Establecer NODE_ENV en “production”](#establecer-node_env-en-production)
- [Asegurarse de que la aplicación se reinicia automáticamente](#asegurarse-de-que-la-aplicación-se-reinicia-automáticamente)
- [Ejecutar la aplicación en un clúster](#ejecutar-la-aplicación-en-un-clúster)
- [Almacenar en la caché los resultados de la solicitud](#almacenar-en-la-caché-los-resultados-de-la-solicitud)
- [Utilizar un equilibrador de carga](#utilizar-un-equilibrador-de-carga)
- [Utilizar un proxy inverso](#utilizar-un-proxy-inverso)

### Establecer NODE_ENV en “production”

La variable de entorno NODE_ENV especifica el entorno en el que se ejecuta una aplicación (normalmente, desarrollo o producción). One of the simplest things you can do to improve performance is to set NODE_ENV to `production`.

Si establece NODE_ENV en “production”, Express:

- Almacena en la caché las plantillas de vistas.
- Almacena en la caché los archivos CSS generados en las extensiones CSS.
- Genera menos mensajes de error detallados.

[Tests indicate](https://www.dynatrace.com/news/blog/the-drastic-effects-of-omitting-node-env-in-your-express-js-applications/) that just doing this can improve app performance by a factor of three!

If you need to write environment-specific code, you can check the value of NODE_ENV with `process.env.NODE_ENV`. Tenga en cuenta que comprobar el valor de una variable de entorno supone una reducción de rendimiento, por lo que debe hacerse moderadamente.

En el desarrollo, normalmente establece las variables de entorno en el shell interactivo, por ejemplo, utilizando `export` o su archivo `.bash_profile`. But in general, you shouldn’t do that on a production server; instead, use your OS’s init system (systemd). En la siguiente sección se proporcionan más detalles sobre el uso del sistema init en general, pero el establecimiento de NODE_ENV es tan importante (y fácil de hacer) para el rendimiento, que se resalta aquí.

Con systemd, utilice la directiva `Environment` en el archivo unit. For example:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

For more information, see [Using Environment Variables In systemd Units](https://www.flatcar.org/docs/latest/setup/systemd/environment-variables/).

### Asegurarse de que la aplicación se reinicia automáticamente

En la producción, no desea que la aplicación esté nunca fuera de línea. Esto significa que debe asegurarse de que se reinicia si la aplicación o el servidor se bloquean. Aunque espera que no se produzca ninguno de estos sucesos, si somos realistas, debe tener en cuenta ambas eventualidades de la siguiente manera:

- Utilizando un gestor de procesos para reiniciar la aplicación (y Node) cuando se bloquea.
- Utilizando el sistema init que proporciona su sistema operativo para reiniciar el gestor de procesos cuando se bloquea el sistema operativo. También puede utilizar el sistema init sin un gestor de procesos.

Las aplicaciones Node se bloquean si encuentran una excepción no capturada. Lo primero que debe hacer es asegurarse de que se realizan las pruebas correctas en la aplicación y que se manejan todas las excepciones (consulte [Manejar correctamente las excepciones](#exceptions) para obtener detalles). No obstante, para estar libre de errores, aplique un mecanismo para garantizar que cuando se bloquee la aplicación, se reinicie automáticamente.

#### Utilizar un gestor de procesos

En el desarrollo, la aplicación se inicia simplemente desde la línea de mandatos con `node server.js` o algo similar. Pero hacer esto en la producción es sinónimo de desastre. Si la aplicación se bloquea, estará fuera de línea hasta que la reinicie. Para garantizar el reinicio de la aplicación si se bloquea, utilice un gestor de procesos. Un gestor de procesos es un “contenedor” de aplicaciones que facilita el despliegue, proporciona una alta disponibilidad y permite gestionar la aplicación en el tiempo de ejecución.

Además de reiniciar la aplicación cuando se bloquea, un gestor de procesos permite:

- Obtener información útil sobre el rendimiento en tiempo de ejecución y el consumo de recursos.
- Modificar dinámicamente los valores para mejorar el rendimiento.
- Control clustering (pm2).

Historically, it was popular to use a Node.js process manager like [PM2](https://github.com/Unitech/pm2). See their documentation if you wish to do this. However, we recommend using your init system for process management.

#### Utilizar un sistema init

La siguiente capa de fiabilidad es garantizar que la aplicación se reinicie cuando se reinicie el servidor. Los sistemas pueden bloquearse por una amplia variedad de motivos. Para garantizar que la aplicación se reinicie si se bloquea el servidor, utilice el sistema init incorporado en su sistema operativo. The main init system in use today is [systemd](https://wiki.debian.org/systemd).

Hay dos formas de utilizar los sistemas init con la aplicación Express:

- Ejecutar la aplicación en un gestor de procesos e instalar el gestor de procesos como un servicio con el sistema init. El gestor de procesos reiniciará la aplicación cuando esta se bloquee y el sistema init reiniciará el gestor de procesos cuando se reinicie el sistema operativo. This is the recommended approach.
- Ejecutar la aplicación (y Node) directamente con el sistema init. Esta opción parece más simple, pero no tiene las ventajas adicionales de utilizar el gestor de procesos.

##### Systemd

Systemd es un administrador de servicios y sistemas Linux. La mayoría de las principales distribuciones Linux han adoptado systemd como su sistema init predeterminado.

Un archivo de configuración de servicio de systemd se denomina un *archivo unit*, con un nombre de archivo terminado en .service. A continuación, se muestra un archivo unit de ejemplo para gestionar directamente una aplicación Node (sustituya el texto en negrita por los valores de su sistema y su aplicación): Replace the values enclosed in `<angle brackets>` for your system and app:

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

Para obtener más información sobre systemd, consulte [systemd reference (man page)](http://www.freedesktop.org/software/systemd/man/systemd.unit.html).

### Ejecutar la aplicación en un clúster

En un sistema multinúcleo, puede multiplicar el rendimiento de una aplicación Node iniciando un clúster de procesos. Un clúster ejecuta varias instancias de la aplicación, idealmente una instancia en cada núcleo de CPU, lo que permite distribuir la carga y las tareas entre las instancias.

![Balancing between application instances using the cluster API](https://expressjs.com/images/clustering.png)

IMPORTANTE: como las instancias de aplicación se ejecutan como procesos independientes, no comparten el mismo espacio de memoria. Es decir, los objetos son locales para cada instancia de la aplicación. Por lo tanto, no puede mantener el estado en el código de aplicación. No obstante, puede utilizar un almacén de datos en memoria como [Redis](http://redis.io/) para almacenar los datos y los estados relacionados con la sesión. Esta advertencia se aplica básicamente a todas las formas de escalado horizontal, ya sean clústeres con varios procesos o varios servidores físicos.

En las aplicaciones en clúster, los procesos de trabajador pueden bloquearse individualmente sin afectar al resto de los procesos. Aparte de las ventajas de rendimiento, el aislamiento de errores es otro motivo para ejecutar un clúster de procesos de aplicación. Siempre que se bloquee un proceso de trabajador, asegúrese de registrar el suceso y generar un nuevo proceso utilizando cluster.fork().

#### Mediante el módulo de clúster de Node

Clustering is made possible with Node’s [cluster module](https://nodejs.org/api/cluster.html). Esto permite al proceso maestro generar procesos de trabajador y distribuir las conexiones entrantes entre los trabajadores.

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

### Almacenar en la caché los resultados de la solicitud

Otra estrategia para mejorar el rendimiento en la producción es almacenar en la caché el resultado de las solicitudes, para que la aplicación no repita la operación de dar servicio a la misma solicitud repetidamente.

Use a caching server like [Varnish](https://www.varnish-cache.org/) or [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (see also [Nginx Caching](https://serversforhackers.com/nginx-caching/)) to greatly improve the speed and performance of your app.

### Utilizar un equilibrador de carga

Independientemente de lo optimizada que esté una aplicación, una única instancia sólo puede manejar una cantidad limitada de carga y tráfico. Una forma de escalar una aplicación es ejecutar varias instancias de la misma y distribuir el tráfico utilizando un equilibrador de carga. La configuración de un equilibrador de carga puede mejorar el rendimiento y la velocidad de la aplicación, lo que permite escalarla más que con una única instancia.

Un equilibrador de carga normalmente es un proxy inverso que orquesta el tráfico hacia y desde los servidores y las instancias de aplicación. You can easily set up a load balancer for your app by using [Nginx](https://nginx.org/en/docs/http/load_balancing.html) or [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

Con el equilibrio de carga, deberá asegurarse de que las solicitudes asociadas con un determinado ID de sesión se conecten al proceso que las ha originado. Esto se conoce como *afinidad de sesiones* o *sesiones adhesivas*, y puede solucionarse con la recomendación anterior de utilizar un almacén de datos como, por ejemplo, Redis para los datos de sesión (dependiendo de la aplicación). Para obtener más información, consulte [Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/).

### Utilizar un proxy inverso

Un proxy inverso se coloca delante de una aplicación web y realiza operaciones de soporte en las solicitudes, aparte de dirigir las solicitudes a la aplicación. Puede manejar las páginas de errores, la compresión, el almacenamiento en memoria caché, el servicio de archivos y el equilibrio de carga, entre otros.

La entrega de tareas que no necesitan saber el estado de la aplicación a un proxy inverso permite a Express realizar tareas de aplicación especializadas. For this reason, it is recommended to run Express behind a reverse proxy like [Nginx](https://www.nginx.org/) or [HAProxy](https://www.haproxy.org/) in production.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/advanced/best-practice-performance.md          )

---

# Production Best Practices: Security

> Discover crucial security best practices for Express apps in production, including using TLS, input validation, secure cookies, and preventing vulnerabilities.

# Production Best Practices: Security

## Overview

El término *“producción”* hace referencia a la etapa del ciclo de vida del software donde una aplicación o una API tiene disponibilidad general para sus consumidores o usuarios finales. Por su parte, en la etapa de *“desarrollo”*, todavía estás escribiendo y probando activamente el código, y la aplicación no está abierta para el acceso externo. Los correspondientes entornos del sistema se conocen como los entornos de *producción* y *desarrollo*, respectivamente.

Los entornos de desarrollo y producción se configuran normalmente de forma diferente y tiene requisitos también muy diferentes. Lo que funciona en el desarrollo puede que no sea aceptable en la producción. Por ejemplo, en un entorno de desarrollo, puede que desee el registro detallado de errores a efecto de depuración, mientras que el mismo comportamiento puede suponer un problema de seguridad en un entorno de producción. De la misma forma, en el desarrollo, no es necesario preocuparse por la escalabilidad, la fiabilidad y el rendimiento, mientras que estos son clave en la producción.

Nota

If you believe you have discovered a security vulnerability in Express, please see
[Security Policies and Procedures](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

Security best practices for Express applications in production include:

- [Production Best Practices: Security](#production-best-practices-security)
  - [Overview](#overview)
  - [Don’t use deprecated or vulnerable versions of Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [Utilizar TLS](#utilizar-tls)
  - [Do not trust user input](#do-not-trust-user-input)
    - [Prevent open redirects](#prevent-open-redirects)
  - [Utilizar Helmet](#utilizar-helmet)
  - [Reduce fingerprinting](#reduce-fingerprinting)
  - [Utilizar cookies de forma segura](#utilizar-cookies-de-forma-segura)
    - [noCache](https://github.com/helmetjs/nocache) establece cabeceras `Cache-Control` y Pragma para inhabilitar el almacenamiento en memoria caché del lado de cliente.
    - [ieNoOpen](https://github.com/helmetjs/ienoopen) establece `X-Download-Options` para IE8+.
  - [Prevenir ataques de fuerza bruta a la autenticación](#prevenir-ataques-de-fuerza-bruta-a-la-autenticación)
  - [Asegurarse de que las dependencias sean seguras](#asegurarse-de-que-las-dependencias-sean-seguras)
    - [Evitar otras vulnerabilidades conocidas](#evitar-otras-vulnerabilidades-conocidas)
  - [Consideraciones adicionales](#consideraciones-adicionales)

## No utilizar versiones en desuso o vulnerables de Express

Express 2.x y 3.x ya no se mantienen. Los problemas de seguridad y rendimiento en estas versiones no se solucionarán. No las utilice. Si no ha cambiado todavía a la versión 4, siga la [guía de migración](https://expressjs.com/es/guide/migrating-4.html).

Asimismo, asegúrese de que no está utilizando ninguna de las versiones vulnerables de Express que se listan en la [página Actualizaciones de seguridad](https://expressjs.com/es/advanced/security-updates.html). Si las utiliza, actualícese a uno de los releases estables, preferiblemente el más reciente.

## Utilizar TLS

Si la aplicación maneja o transmite datos confidenciales, utilice [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (TLS) para proteger la conexión y los datos. Esta tecnología cifra los datos antes de enviarlos desde el cliente al servidor, lo que evita algunos de los ataques de pirateo más comunes (y sencillos). Aunque las solicitudes Ajax y POST no sean obvias visiblemente y parezca que están “ocultas” en los navegadores, su tráfico de red es vulnerable para los [rastreos de paquetes](https://en.wikipedia.org/wiki/Packet_analyzer) y los [ataques de intermediarios](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

Es posible que esté familiarizado con el cifrado SSL (Secure Socket Layer). [TLS es simplemente el siguiente paso después de SSL](https://msdn.microsoft.com/en-us/library/windows/desktop/aa380515\(v=vs.85\).aspx). Es decir, si antes utilizaba SSL, se recomienda actualizar a TLS. En general, se recomienda Nginx para manejar TLS. Encontrará una buena referencia para configurar TLS en Nginx (y otros servidores) en [la wiki de Mozilla Recommended Server Configurations](https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_Server_Configurations).

Asimismo, una herramienta muy útil para obtener un certificado de TLS gratis es [Let’s Encrypt](https://letsencrypt.org/about/), una entidad emisora de certificados (CA) abierta, automatizada y gratuita proporcionada por [Internet Security Research Group (ISRG)](https://letsencrypt.org/isrg/).

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

## Utilizar Helmet

[Helmet](https://www.npmjs.com/package/helmet) ayuda a proteger la aplicación de algunas vulnerabilidades web conocidas mediante el establecimiento correcto de cabeceras HTTP.

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

Each header can be configured or disabled. To read more about it please go to [its documentation website](https://expressjs.com/es/advanced/Si utiliza `helmet.js`, lo hace automáticamente.).

Instale Helmet como cualquier otro módulo:

```
$ npm install helmet
```

A continuación, utilícelo en el código:

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

Por lo tanto, se recomienda desactivar la cabecera con el método `app.disable()`:

```
app.disable('x-powered-by')
```

Nota

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

## Establecer las opciones de seguridad de las cookies

Para garantizar que las cookies no abran la aplicación para ataques, no utilice el nombre de cookie de sesión predeterminado y establezca las opciones de seguridad de las cookies correctamente.

Hay dos módulos de sesión de cookies de middleware principales:

- [express-session](https://www.npmjs.com/package/express-session), que sustituye el middleware `express.session` incorporado en Express 3.x.
- [cookie-session](https://www.npmjs.com/package/cookie-session), que sustituye el middleware `express.cookieSession` incorporado en Express 3.x.

La principal diferencia entre los dos módulos es cómo guardan los datos de sesión de las cookies. El middleware [express-session](https://www.npmjs.com/package/express-session) almacena los datos de sesión en el servidor; sólo guarda el ID de sesión en la propia cookie, no los datos de sesión. De forma predeterminada, utiliza el almacenamiento en memoria y no está diseñado para un entorno de producción. En la producción, deberá configurar un almacenamiento de sesión escalable; consulte la lista de [almacenes de sesión compatibles](https://github.com/expressjs/session#compatible-session-stores).

Por su parte, el middleware [cookie-session](https://www.npmjs.com/package/cookie-session) implementa un almacenamiento basado en cookies: serializa la sesión completa en la cookie, en lugar de sólo una clave de sesión. Utilícelo sólo cuando los datos de sesión sean relativamente pequeños y fácilmente codificables como valores primitivos (en lugar de objetos). Aunque se supone que los navegadores pueden dar soporte a 4096 bytes por cookie como mínimo, para no exceder el límite, no supere un tamaño de 4093 bytes por dominio. Asimismo, asegúrese de que los datos de la cookie estén visibles para el cliente, para que si se deben proteger u ocultar por cualquier motivo, se utilice mejor la opción express-session.

### No utilizar el nombre de cookie de sesión predeterminado

Si utiliza el nombre de cookie de sesión predeterminado, la aplicación puede quedar abierta a los ataques. El problema de seguridad que supone es similar a `X-Powered-By`: un posible atacante puede utilizarlo para firmar digitalmente el servidor y dirigir los ataques en consecuencia.

Para evitar este problema, utilice nombres de cookie genéricos, por ejemplo, con el middleware [express-session](https://www.npmjs.com/package/express-session):

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Utilizar cookies de forma segura

Establezca las siguientes opciones de cookies para mejorar la seguridad:

- `secure` - Garantiza que el navegador sólo envíe la cookie a través de HTTPS.
- `httpOnly` - Garantiza que la cookie sólo se envíe a través de HTTP(S), no a través de JavaScript de cliente, para la protección contra ataques de scripts entre sitios.
- `domain` - Indica el dominio de la cookie; utilícelo para compararlo con el dominio del servidor donde se está solicitando el URL. Si coinciden, compruebe el atributo de vía de acceso a continuación.
- `path` - Indica la vía de acceso de la cookie; utilícela para compararla con la vía de acceso de la solicitud. Si esta y el dominio coinciden, envíe la cookie en la solicitud.
- `expires` - Se utiliza para establecer la fecha de caducidad de las cookies persistentes.

A continuación, se muestra un ejemplo de uso del middleware [cookie-session](https://www.npmjs.com/package/cookie-session):

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

## Prevenir ataques de fuerza bruta a la autenticación

Asegurate de que los puntos finales del inicio de sesión están protegidos para convertir los datos privados más seguros.

Una simple y potente técnica es bloquear intentos de autorización usando dos métricas:

1. Según el número de intentos fallidos consecutivos por el mismo nombre de usuario y dirección IP.
2. Según el número fallido de intentos desde una dirección IP a lo largo de un cierto período de tiempo. Por ejemplo, bloquear una dirección IP si realiza 100 intentos fallidos en un día.

El paquete [rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible) ofrece herramientas para realizar esta técnica de forma fácil y rápida. Aquí puedes encontrar un [ejemplo de protección de fuerza bruta en la documentación](https://github.com/animir/node-rate-limiter-flexible/wiki/Overall-example#login-endpoint-protection).

## Asegurarse de que las dependencias sean seguras

El uso de npm para gestionar las dependencias de la aplicación es muy útil y cómodo. No obstante, los paquetes que utiliza pueden contener vulnerabilidades de seguridad críticas que también pueden afectar a la aplicación. La seguridad de la aplicación sólo es tan fuerte como el “enlace más débil” de las dependencias.

Since npm@6, npm automatically reviews every install request. También puedes utilizar ‘npm audit’ para analizar tu árbol de dependencias.

```
$ npm audit
```

Si quieres mantener más seguro, considera [Snyk](https://snyk.io/).

Snyk ofrece tanto [herramienta de línea de comandos](https://www.npmjs.com/package/snyk) como una [integración de Github](https://snyk.io/docs/github) que comprueba tu aplicación contra [la base de datos de código abierto sobre vulnerabilidades de Snyk](https://snyk.io/vuln/) por cualquier vulnerabilidad conocida en tus dependencias. Instala la interfaz de línea de comandos:

```
$ npm install -g snyk
$ cd your-app
```

Usa este comando para comprobar tu aplicación contra vulnerabilidades:

```
$ snyk test
```

### Avoid other known vulnerabilities

Esté atento a las advertencias de [Node Security Project](https://npmjs.com/advisories) que puedan afectar a Express u otros módulos que utilice la aplicación. En general, Node Security Project es un excelente recurso de herramientas e información sobre la seguridad de Node.

Por último, las aplicaciones de Express, como cualquier otra aplicación web, son vulnerables a una amplia variedad de ataques basados en web. Familiarícese con las [vulnerabilidades web](https://www.owasp.org/www-project-top-ten/) conocidas y tome precauciones para evitarlas.

## Additional considerations

A continuación, se muestran algunas recomendaciones para la excelente lista de comprobación [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/). Consulte el post de este blog para ver todos los detalles de estas recomendaciones:

- Filtre y sanee siempre la entrada de usuario para protegerse contra los ataques de scripts entre sitios (XSS) e inyección de mandatos.
- Defiéndase contra los ataques de inyección de SQL utilizando consultas parametrizadas o sentencias preparadas.
- Utilice la herramienta [sqlmap](http://sqlmap.org/) de código abierto para detectar vulnerabilidades de inyección de SQL en la aplicación.
- Utilice las herramientas [nmap](https://nmap.org/) y [sslyze](https://github.com/nabla-c0d3/sslyze) para probar la configuración de los cifrados SSL, las claves y la renegociación, así como la validez del certificado.
- Utilice [safe-regex](https://www.npmjs.com/package/safe-regex) para asegurarse de que las expresiones regulares no sean susceptibles de ataques de [denegación de servicio de expresiones regulares](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/advanced/best-practice-security.md          )

---

# Desarrollo de motores de plantilla para Express

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Desarrollo de motores de plantilla para Express

Utilice el método `app.engine(ext, callback)` para crear su propio motor de plantilla. `ext` hace referencia a la extensión de archivo y `callback` es la función de motor de plantilla, que acepta los siguientes elementos como parámetros: la ubicación del archivo, el objeto options y la función callback.

El siguiente código es un ejemplo de implementación de un motor de plantilla muy simple para la representación de archivos `.ntl`.

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

La aplicación ahora podrá representar archivos `.ntl`. Cree un archivo denominado `index.ntl` en el directorio `views` con el siguiente contenido.

```pug
#title#
#message#
```

A continuación, cree la ruta siguiente en la aplicación.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Cuando realice una solicitud a la página de inicio, `index.ntl` se representará como HTML.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

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

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/es/advanced/healthcheck-graceful-shutdown.md          )
