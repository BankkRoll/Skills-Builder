# Fastly Compute​ and more

# Fastly Compute​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Fastly Compute​

[Fastly Compute](https://www.fastly.com/products/edge-compute) is an advanced edge computing system that runs your code, in your favorite language, on Fastly's global edge network. Hono also works on Fastly Compute.

You can develop the application locally and publish it with a few commands using [Fastly CLI](https://www.fastly.com/documentation/reference/tools/cli/), which is installed locally automatically as part of the template.

## 1. Setup​

A starter for Fastly Compute is available. Start your project with "create-hono" command. Select `fastly` template for this example.

npmyarnpnpmbundenosh

```
npm create hono@latest my-app
```

sh

```
yarn create hono my-app
```

sh

```
pnpm create hono my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono my-app
```

Move to `my-app` and install the dependencies.

npmyarnpnpmbunsh

```
cd my-app
npm i
```

sh

```
cd my-app
yarn
```

sh

```
cd my-app
pnpm i
```

sh

```
cd my-app
bun i
```

## 2. Hello World​

Edit `src/index.ts`:

ts

```
// src/index.ts
import { Hono } from 'hono'
import { fire } from '@fastly/hono-fastly-compute'

const app = new Hono()

app.get('/', (c) => c.text('Hello Fastly!'))

fire(app)
```

NOTE

When using `fire` (or `buildFire()`) from `@fastly/hono-fastly-compute'` at the top level of your application, it is suitable to use `Hono` from `'hono'` rather than `'hono/quick'`, because `fire` causes its router to build its internal data during the application initialization phase.

## 3. Run​

Run the development server locally. Then, access `http://localhost:7676` in your Web browser.

npmyarnpnpmbunsh

```
npm run start
```

sh

```
yarn start
```

sh

```
pnpm run start
```

sh

```
bun run start
```

## 4. Deploy​

To build and deploy your application to your Fastly account, type the following command. The first time you deploy the application, you will be prompted to create a new service in your account.

If you don't have an account yet, you must [create your Fastly account](https://www.fastly.com/signup/).

npmyarnpnpmbunsh

```
npm run deploy
```

sh

```
yarn deploy
```

sh

```
pnpm run deploy
```

sh

```
bun run deploy
```

## Bindings​

In Fastly Compute, you can bind Fastly platform resources, such as KV Stores, Config Stores, Secret Stores, Backends, Access Control Lists, Named Log Streams, and Environment Variables. You can access them through `c.env`, and will have their individual SDK types.

To use these bindings, import `buildFire` instead of `fire` from `@fastly/hono-fastly-compute`. Define your [bindings](https://github.com/fastly/compute-js-context?tab=readme-ov-file#typed-bindings-with-buildcontextproxy) and pass them to [buildFire()](https://github.com/fastly/hono-fastly-compute?tab=readme-ov-file#basic-example) to obtain `fire`. Then use `fire.Bindings` to define your `Env` type as you construct `Hono`.

ts

```
// src/index.ts
import { buildFire } from '@fastly/hono-fastly-compute'

const fire = buildFire({
  siteData: 'KVStore:site-data', // I have a KV Store named "site-data"
})

const app = new Hono<{ Bindings: typeof fire.Bindings }>()

app.put('/upload/:key', async (c, next) => {
  // e.g., Access the KV Store
  const key = c.req.param('key')
  await c.env.siteData.put(key, c.req.body)
  return c.text(`Put ${key} successfully!`)
})

fire(app)
```

---

# Google Cloud Run​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Google Cloud Run​

[Google Cloud Run](https://cloud.google.com/run) is a serverless platform built by Google Cloud. You can run your code in response to events and Google automatically manages the underlying compute resources for you.

Google Cloud Run uses containers to run your service. This means you can use any runtime you like (E.g., Deno or Bun) by providing a Dockerfile. If no Dockerfile is provided Google Cloud Run will use the default Nodejs buildpack.

This guide assumes you already have a Google Cloud account and a billing account.

## 1. Install the CLI​

When working with Google Cloud Platform it is easiest to work with the [gcloud CLI](https://cloud.google.com/sdk/docs/install).

For example, on MacOS using Homebrew:

sh

```
brew install --cask gcloud-cli
```

Authenticate with the CLI.

sh

```
gcloud auth login
```

## 2. Project setup​

Create a project. Accept the auto-generated project ID at the prompt.

sh

```
gcloud projects create --set-as-default --name="my app"
```

Create environment variables for your project ID and project number for easy reuse. It may take ~30 seconds before the project successfully returns with the `gcloud projects list` command.

sh

```
PROJECT_ID=$(gcloud projects list \
    --format='value(projectId)' \
    --filter='name="my app"')

PROJECT_NUMBER=$(gcloud projects list \
    --format='value(projectNumber)' \
    --filter='name="my app"')

echo $PROJECT_ID $PROJECT_NUMBER
```

Find your billing account ID.

sh

```
gcloud billing accounts list
```

Add your billing account from the prior command to the project.

sh

```
gcloud billing projects link $PROJECT_ID \
    --billing-account=[billing_account_id]
```

Enable the required APIs.

sh

```
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com
```

Update the service account permissions to have access to Cloud Build.

sh

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/run.builder
```

## 3. Hello World​

Start your project with "create-hono" command. Select `nodejs`.

sh

```
npm create hono@latest my-app
```

Move to `my-app` and install the dependencies.

sh

```
cd my-app
npm i
```

Update the port in `src/index.ts` to be `8080`.

ts

```
import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

serve({
  fetch: app.fetch,
  port: 3000
  port: 8080
}, (info) => {
  console.log(`Server is running on http://localhost:${info.port}`)
})
```

Run the development server locally. Then, access [http://localhost:8080](http://localhost:8080) in your Web browser.

sh

```
npm run dev
```

## 4. Deploy​

Start the deployment and follow the interactive prompts (E.g., select a region).

sh

```
gcloud run deploy my-app --source . --allow-unauthenticated
```

## Changing runtimes​

If you want to deploy using Deno or Bun runtimes (or a customised Nodejs container), add a `Dockerfile` (and optionally `.dockerignore`) with your desired environment.

For information on containerizing please refer to:

- [Nodejs](https://hono.dev/docs/getting-started/nodejs#building-deployment)
- [Bun](https://bun.com/guides/ecosystem/docker)
- [Deno](https://docs.deno.com/examples/google_cloud_run_tutorial)

---

# Lambda@Edge​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Lambda@Edge​

[Lambda@Edge](https://aws.amazon.com/lambda/edge/) is a serverless platform by Amazon Web Services. It allows you to run Lambda functions at Amazon CloudFront's edge locations, enabling you to customize behaviors for HTTP requests/responses.

Hono supports Lambda@Edge with the Node.js 18+ environment.

## 1. Setup​

When creating the application on Lambda@Edge, [CDK](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-cdk.html) is useful to setup the functions such as CloudFront, IAM Role, API Gateway, and others.

Initialize your project with the `cdk` CLI.

npmyarnpnpmbunsh

```
mkdir my-app
cd my-app
cdk init app -l typescript
npm i hono
mkdir lambda
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
yarn add hono
mkdir lambda
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
pnpm add hono
mkdir lambda
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
bun add hono
mkdir lambda
```

## 2. Hello World​

Edit `lambda/index_edge.ts`.

ts

```
import { Hono } from 'hono'
import { handle } from 'hono/lambda-edge'

const app = new Hono()

app.get('/', (c) => c.text('Hello Hono on Lambda@Edge!'))

export const handler = handle(app)
```

## 3. Deploy​

Edit `bin/my-app.ts`.

ts

```
#!/usr/bin/env node
import 'source-map-support/register'
import * as cdk from 'aws-cdk-lib'
import { MyAppStack } from '../lib/my-app-stack'

const app = new cdk.App()
new MyAppStack(app, 'MyAppStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'us-east-1',
  },
})
```

Edit `lambda/cdk-stack.ts`.

ts

```
import { Construct } from 'constructs'
import * as cdk from 'aws-cdk-lib'
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront'
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs'
import * as s3 from 'aws-cdk-lib/aws-s3'

export class MyAppStack extends cdk.Stack {
  public readonly edgeFn: lambda.Function

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props)
    const edgeFn = new NodejsFunction(this, 'edgeViewer', {
      entry: 'lambda/index_edge.ts',
      handler: 'handler',
      runtime: lambda.Runtime.NODEJS_20_X,
    })

    // Upload any html
    const originBucket = new s3.Bucket(this, 'originBucket')

    new cloudfront.Distribution(this, 'Cdn', {
      defaultBehavior: {
        origin: new origins.S3Origin(originBucket),
        edgeLambdas: [
          {
            functionVersion: edgeFn.currentVersion,
            eventType: cloudfront.LambdaEdgeEventType.VIEWER_REQUEST,
          },
        ],
      },
    })
  }
}
```

Finally, run the command to deploy:

sh

```
cdk deploy
```

## Callback​

If you want to add Basic Auth and continue with request processing after verification, you can use `c.env.callback()`

ts

```
import { Hono } from 'hono'
import { basicAuth } from 'hono/basic-auth'
import type { Callback, CloudFrontRequest } from 'hono/lambda-edge'
import { handle } from 'hono/lambda-edge'

type Bindings = {
  callback: Callback
  request: CloudFrontRequest
}

const app = new Hono<{ Bindings: Bindings }>()

app.get(
  '*',
  basicAuth({
    username: 'hono',
    password: 'acoolproject',
  })
)

app.get('/', async (c, next) => {
  await next()
  c.env.callback(null, c.env.request)
})

export const handler = handle(app)
```

---

# Netlify​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Netlify​

Netlify provides static site hosting and serverless backend services. [Edge Functions](https://docs.netlify.com/edge-functions/overview/) enables us to make the web pages dynamic.

Edge Functions support writing in Deno and TypeScript, and deployment is made easy through the [Netlify CLI](https://docs.netlify.com/cli/get-started/). With Hono, you can create the application for Netlify Edge Functions.

## 1. Setup​

A starter for Netlify is available. Start your project with "create-hono" command. Select `netlify` template for this example.

npmyarnpnpmbundenosh

```
npm create hono@latest my-app
```

sh

```
yarn create hono my-app
```

sh

```
pnpm create hono my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono my-app
```

Move into `my-app`.

## 2. Hello World​

Edit `netlify/edge-functions/index.ts`:

ts

```
import { Hono } from 'jsr:@hono/hono'
import { handle } from 'jsr:@hono/hono/netlify'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

export default handle(app)
```

## 3. Run​

Run the development server with Netlify CLI. Then, access `http://localhost:8888` in your Web browser.

sh

```
netlify dev
```

## 4. Deploy​

You can deploy with a `netlify deploy` command.

sh

```
netlify deploy --prod
```

## Context​

You can access the Netlify's `Context` through `c.env`:

ts

```
import { Hono } from 'jsr:@hono/hono'
import { handle } from 'jsr:@hono/hono/netlify'

// Import the type definition
import type { Context } from 'https://edge.netlify.com/'

export type Env = {
  Bindings: {
    context: Context
  }
}

const app = new Hono<Env>()

app.get('/country', (c) =>
  c.json({
    'You are in': c.env.context.geo.country?.name,
  })
)

export default handle(app)
```

---

# Next.js​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Next.js​

Next.js is a flexible React framework that gives you building blocks to create fast web applications.

You can run Hono on Next.js when using the Node.js runtime.
 On Vercel, deploying Hono with Next.js is easy by using Vercel Functions.

## 1. Setup​

A starter for Next.js is available. Start your project with "create-hono" command. Select `nextjs` template for this example.

npmyarnpnpmbundenosh

```
npm create hono@latest my-app
```

sh

```
yarn create hono my-app
```

sh

```
pnpm create hono my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono my-app
```

Move into `my-app` and install the dependencies.

npmyarnpnpmbunsh

```
cd my-app
npm i
```

sh

```
cd my-app
yarn
```

sh

```
cd my-app
pnpm i
```

sh

```
cd my-app
bun i
```

## 2. Hello World​

If you use the App Router, Edit `app/api/[[...route]]/route.ts`. Refer to the [Supported HTTP Methods](https://nextjs.org/docs/app/building-your-application/routing/route-handlers#supported-http-methods) section for more options.

ts

```
import { Hono } from 'hono'
import { handle } from 'hono/vercel'

const app = new Hono().basePath('/api')

app.get('/hello', (c) => {
  return c.json({
    message: 'Hello Next.js!',
  })
})

export const GET = handle(app)
export const POST = handle(app)
```

## 3. Run​

Run the development server locally. Then, access `http://localhost:3000` in your Web browser.

npmyarnpnpmbunsh

```
npm run dev
```

sh

```
yarn dev
```

sh

```
pnpm dev
```

sh

```
bun run dev
```

Now, `/api/hello` just returns JSON, but if you build React UIs, you can create a full-stack application with Hono.

## 4. Deploy​

If you have a Vercel account, you can deploy by linking the Git repository.

## Pages Router​

If you use the Pages Router, you'll need to install the Node.js adapter first.

npmyarnpnpmbunsh

```
npm i @hono/node-server
```

sh

```
yarn add @hono/node-server
```

sh

```
pnpm add @hono/node-server
```

sh

```
bun add @hono/node-server
```

Then, you can utilize the `handle` function imported from `@hono/node-server/vercel` in `pages/api/[[...route]].ts`.

ts

```
import { Hono } from 'hono'
import { handle } from '@hono/node-server/vercel'
import type { PageConfig } from 'next'

export const config: PageConfig = {
  api: {
    bodyParser: false,
  },
}

const app = new Hono().basePath('/api')

app.get('/hello', (c) => {
  return c.json({
    message: 'Hello Next.js!',
  })
})

export default handle(app)
```

In order for this to work with the Pages Router, it's important to disable Vercel Node.js helpers by setting up an environment variable in your project dashboard or in your `.env` file.

text

```
NODEJS_HELPERS=0
```

---

# Node.js​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Node.js​

[Node.js](https://nodejs.org/) is an open-source, cross-platform JavaScript runtime environment.

Hono was not designed for Node.js at first. But with a [Node.js Adapter](https://github.com/honojs/node-server) it can run on Node.js as well.

INFO

It works on Node.js versions greater than 18.x. The specific required Node.js versions are as follows:

- 18.x => 18.14.1+
- 19.x => 19.7.0+
- 20.x => 20.0.0+

Essentially, you can simply use the latest version of each major release.

## 1. Setup​

A starter for Node.js is available. Start your project with "create-hono" command. Select `nodejs` template for this example.

npmyarnpnpmbundenosh

```
npm create hono@latest my-app
```

sh

```
yarn create hono my-app
```

sh

```
pnpm create hono my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono my-app
```

Move to `my-app` and install the dependencies.

npmyarnpnpmbunsh

```
cd my-app
npm i
```

sh

```
cd my-app
yarn
```

sh

```
cd my-app
pnpm i
```

sh

```
cd my-app
bun i
```

## 2. Hello World​

Edit `src/index.ts`:

ts

```
import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Node.js!'))

serve(app)
```

If you want to gracefully shut down the server, write it like this:

ts

```
const server = serve(app)

// graceful shutdown
process.on('SIGINT', () => {
  server.close()
  process.exit(0)
})
process.on('SIGTERM', () => {
  server.close((err) => {
    if (err) {
      console.error(err)
      process.exit(1)
    }
    process.exit(0)
  })
})
```

## 3. Run​

Run the development server locally. Then, access `http://localhost:3000` in your Web browser.

npmyarnpnpmsh

```
npm run dev
```

sh

```
yarn dev
```

sh

```
pnpm dev
```

## Change port number​

You can specify the port number with the `port` option.

ts

```
serve({
  fetch: app.fetch,
  port: 8787,
})
```

## Access the raw Node.js APIs​

You can access the Node.js APIs from `c.env.incoming` and `c.env.outgoing`.

ts

```
import { Hono } from 'hono'
import { serve, type HttpBindings } from '@hono/node-server'
// or `Http2Bindings` if you use HTTP2

type Bindings = HttpBindings & {
  /* ... */
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/', (c) => {
  return c.json({
    remoteAddress: c.env.incoming.socket.remoteAddress,
  })
})

serve(app)
```

## Serve static files​

You can use `serveStatic` to serve static files from the local file system. For example, suppose the directory structure is as follows:

sh

```
./
├── favicon.ico
├── index.ts
└── static
    ├── hello.txt
    └── image.png
```

If a request to the path `/static/*` comes in and you want to return a file under `./static`, you can write the following:

ts

```
import { serveStatic } from '@hono/node-server/serve-static'

app.use('/static/*', serveStatic({ root: './' }))
```

Use the `path` option to serve `favicon.ico` in the directory root:

ts

```
app.use('/favicon.ico', serveStatic({ path: './favicon.ico' }))
```

If a request to the path `/hello.txt` or `/image.png` comes in and you want to return a file named `./static/hello.txt` or `./static/image.png`, you can use the following:

ts

```
app.use('*', serveStatic({ root: './static' }))
```

### rewriteRequestPath​

If you want to map `http://localhost:3000/static/*` to `./statics`, you can use the `rewriteRequestPath` option:

ts

```
app.get(
  '/static/*',
  serveStatic({
    root: './',
    rewriteRequestPath: (path) =>
      path.replace(/^\/static/, '/statics'),
  })
)
```

## http2​

You can run hono on a [Node.js http2 Server](https://nodejs.org/api/http2.html).

### unencrypted http2​

ts

```
import { createServer } from 'node:http2'

const server = serve({
  fetch: app.fetch,
  createServer,
})
```

### encrypted http2​

ts

```
import { createSecureServer } from 'node:http2'
import { readFileSync } from 'node:fs'

const server = serve({
  fetch: app.fetch,
  createServer: createSecureServer,
  serverOptions: {
    key: readFileSync('localhost-privkey.pem'),
    cert: readFileSync('localhost-cert.pem'),
  },
})
```

## Building & Deployment​

npmyarnpnpmbunsh

```
npm run build
```

sh

```
yarn run build
```

sh

```
pnpm run build
```

sh

```
bun run build
```

INFO

Apps with a front-end framework may need to use [Hono's Vite plugins](https://github.com/honojs/vite-plugins).

### Dockerfile​

Here is an example of a nodejs Dockerfile.

Dockerfile

```
FROM node:22-alpine AS base

FROM base AS builder

RUN apk add --no-cache gcompat
WORKDIR /app

COPY package*json tsconfig.json src ./

RUN npm ci && \
    npm run build && \
    npm prune --production

FROM base AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 hono

COPY --from=builder --chown=hono:nodejs /app/node_modules /app/node_modules
COPY --from=builder --chown=hono:nodejs /app/dist /app/dist
COPY --from=builder --chown=hono:nodejs /app/package.json /app/package.json

USER hono
EXPOSE 3000

CMD ["node", "/app/dist/index.js"]
```

---

# Service Worker​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Service Worker​

[Service Worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) is a script that runs in the background of the browser to handle tasks like caching and push notifications. Using a Service Worker adapter, you can run applications made with Hono as [FetchEvent](https://developer.mozilla.org/en-US/docs/Web/API/FetchEvent) handler within the browser.

This page shows an example of creating a project using [Vite](https://vitejs.dev/).

## 1. Setup​

First, create and move to your project directory:

sh

```
mkdir my-app
cd my-app
```

Create the necessary files for the project. Make a `package.json` file with the following:

json

```
{
  "name": "my-app",
  "private": true,
  "scripts": {
    "dev": "vite dev"
  },
  "type": "module"
}
```

Similarly, create a `tsconfig.json` file with the following:

json

```
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "WebWorker"],
    "moduleResolution": "bundler"
  },
  "include": ["./"],
  "exclude": ["node_modules"]
}
```

Next, install the necessary modules.

npmyarnpnpmbunsh

```
npm i hono
npm i -D vite
```

sh

```
yarn add hono
yarn add -D vite
```

sh

```
pnpm add hono
pnpm add -D vite
```

sh

```
bun add hono
bun add -D vite
```

## 2. Hello World​

Edit `index.html`:

html

```
<!doctype html>
<html>
  <body>
    <a href="/sw">Hello World by Service Worker</a>
    <script type="module" src="/main.ts"></script>
  </body>
</html>
```

`main.ts` is a script to register the Service Worker:

ts

```
function register() {
  navigator.serviceWorker
    .register('/sw.ts', { scope: '/sw', type: 'module' })
    .then(
      function (_registration) {
        console.log('Register Service Worker: Success')
      },
      function (_error) {
        console.log('Register Service Worker: Error')
      }
    )
}
function start() {
  navigator.serviceWorker
    .getRegistrations()
    .then(function (registrations) {
      for (const registration of registrations) {
        console.log('Unregister Service Worker')
        registration.unregister()
      }
      register()
    })
}
start()
```

In `sw.ts`, create an application using Hono and register it to the `fetch` event with the Service Worker adapter’s `handle` function. This allows the Hono application to intercept access to `/sw`.

ts

```
// To support types
// https://github.com/microsoft/TypeScript/issues/14877
declare const self: ServiceWorkerGlobalScope

import { Hono } from 'hono'
import { handle } from 'hono/service-worker'

const app = new Hono().basePath('/sw')
app.get('/', (c) => c.text('Hello World'))

self.addEventListener('fetch', handle(app))
```

### Usingfire()​

The `fire()` function automatically calls `addEventListener('fetch', handle(app))` for you, making the code more concise.

ts

```
import { Hono } from 'hono'
import { fire } from 'hono/service-worker'

const app = new Hono().basePath('/sw')
app.get('/', (c) => c.text('Hello World'))

fire(app)
```

## 3. Run​

Start the development server.

npmyarnpnpmbunsh

```
npm run dev
```

sh

```
yarn dev
```

sh

```
pnpm run dev
```

sh

```
bun run dev
```

By default, the development server will run on port `5173`. Access `http://localhost:5173/` in your browser to complete the Service Worker registration. Then, access `/sw` to see the response from the Hono application.

---

# Supabase Edge Functions​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Supabase Edge Functions​

[Supabase](https://supabase.com/) is an open-source alternative to Firebase, offering a suite of tools similar to Firebase's capabilities, including database, authentication, storage, and now, serverless functions.

Supabase Edge Functions are server-side TypeScript functions that are distributed globally, running closer to your users for improved performance. These functions are developed using [Deno](https://deno.com/), which brings several benefits, including improved security and a modern JavaScript/TypeScript runtime.

Here's how you can get started with Supabase Edge Functions:

## 1. Setup​

### Prerequisites​

Before you begin, make sure you have the Supabase CLI installed. If you haven't installed it yet, follow the instructions in the [official documentation](https://supabase.com/docs/guides/cli/getting-started).

### Creating a New Project​

1. Open your terminal or command prompt.
2. Create a new Supabase project in a directory on your local machine by running:

bash

```
supabase init
```

This command initializes a new Supabase project in the current directory.

### Adding an Edge Function​

1. Inside your Supabase project, create a new Edge Function named `hello-world`:

bash

```
supabase functions new hello-world
```

This command creates a new Edge Function with the specified name in your project.

## 2. Hello World​

Edit the `hello-world` function by modifying the file `supabase/functions/hello-world/index.ts`:

ts

```
import { Hono } from 'jsr:@hono/hono'

// change this to your function name
const functionName = 'hello-world'
const app = new Hono().basePath(`/${functionName}`)

app.get('/hello', (c) => c.text('Hello from hono-server!'))

Deno.serve(app.fetch)
```

## 3. Run​

To run the function locally, use the following command:

1. Use the following command to serve the function:

bash

```
supabase start # start the supabase stack
supabase functions serve --no-verify-jwt # start the Functions watcher
```

The `--no-verify-jwt` flag allows you to bypass JWT verification during local development.

1. Make a GET request using cURL or Postman to `http://127.0.0.1:54321/functions/v1/hello-world/hello`:

bash

```
curl  --location  'http://127.0.0.1:54321/functions/v1/hello-world/hello'
```

This request should return the text "Hello from hono-server!".

## 4. Deploy​

You can deploy all of your Edge Functions in Supabase with a single command:

bash

```
supabase functions deploy
```

Alternatively, you can deploy individual Edge Functions by specifying the name of the function in the deploy command:

bash

```
supabase functions deploy hello-world
```

For more deployment methods, visit the Supabase documentation on [Deploying to Production](https://supabase.com/docs/guides/functions/deploy).

---

# Vercel​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Vercel​

Vercel is the AI cloud, providing the developer tools and cloud infrastructure to build, scale, and secure a faster, more personalized web.

Hono can be deployed to Vercel with zero-configuration.

## 1. Setup​

A starter for Vercel is available. Start your project with "create-hono" command. Select `vercel` template for this example.

npmyarnpnpmbundenosh

```
npm create hono@latest my-app
```

sh

```
yarn create hono my-app
```

sh

```
pnpm create hono my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono my-app
```

Move into `my-app` and install the dependencies.

npmyarnpnpmbunsh

```
cd my-app
npm i
```

sh

```
cd my-app
yarn
```

sh

```
cd my-app
pnpm i
```

sh

```
cd my-app
bun i
```

We will use Vercel CLI to work on the app locally in the next step. If you haven't already, install it globally following [the Vercel CLI documentation](https://vercel.com/docs/cli).

## 2. Hello World​

In the `index.ts` or `src/index.ts` of your project, export the Hono application as a default export.

ts

```
import { Hono } from 'hono'

const app = new Hono()

const welcomeStrings = [
  'Hello Hono!',
  'To learn more about Hono on Vercel, visit https://vercel.com/docs/frameworks/backend/hono',
]

app.get('/', (c) => {
  return c.text(welcomeStrings.join('\n\n'))
})

export default app
```

If you started with the `vercel` template, this is already set up for you.

## 3. Run​

To run the development server locally:

sh

```
vercel dev
```

Visiting `localhost:3000` will respond with a text response.

## 4. Deploy​

Deploy to Vercel using `vc deploy`.

sh

```
vercel deploy
```

## Further reading​

[Learn more about Hono in the Vercel documentation](https://vercel.com/docs/frameworks/backend/hono).

---

# WebAssembly (w/ WASI)​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# WebAssembly (w/ WASI)​

[WebAssembly](https://webassembly.org/) is a secure, sandboxed, portable runtime that runs inside and outside web browsers.

In practice:

- Languages (like Javascript) *compile to* WebAssembly (`.wasm` files)
- WebAssembly runtimes (like [wasmtime](https://wasmtime.dev) or [jco](https://github.com/bytecodealliance/jco)) enable *running* WebAssembly binaries

While core WebAssembly has *no* access to things like the local filesystem or sockets, the [WebAssembly System Interface](https://wasi.dev/) steps in to enable defining a platform under WebAssebly workloads.

This means that *with* WASI, WebAssembly can operate on files, sockets, and much more.

INFO

Want to peek at the WASI interface yourself? check out [wasi:http](https://github.com/WebAssembly/wasi-http)

Support for WebAssembly w/ WASI in JS is powered by [StarlingMonkey](https://github.com/bytecodealliance/StarlingMonkey), and thanks to the focus on Web standards in both StarlingMonkey and Hono, **Hono works *out of the box with WASI-enabled WebAssembly ecosystems.**

## 1. Setup​

The WebAssembly JS ecosystem provides tooling to make it easy to get started building WASI-enabled WebAssembly components:

- [StarlingMonkey](https://github.com/bytecodealliance/StarlingMonkey) is a fork of [SpiderMonkey](https://spidermonkey.dev/) that compiles to WebAssembly and enables components
- [componentize-js](https://github.com/bytecodealliance/componentize-js) turns Javascript ES modules into WebAssembly components
- [jco](https://github.com/bytecodealliance/jco) is a multi-tool that builds components, generates types, and runs components in environments like NodeJS or the browser

INFO

Webassembly has an open ecosystem and is open source, with core projects stewarded primarily by the [Bytecode Alliance](https://bytecodealliance.org/) and it's members.

New features, issues, pull requests and other types of contributions are always welcome.

While a starter for Hono on WebAssembly is not yet available, you can start a WebAssembly Hono project just like any other:

npmyarnbunsh

```
mkdir my-app
cd my-app
npm init
npm i hono
npm i -D @bytecodealliance/jco @bytecodealliance/componentize-js @bytecodealliance/jco-std
npm i -D rolldown
```

sh

```
mkdir my-app
cd my-app
npm init
yarn add hono
yarn add -D @bytecodealliance/jco @bytecodealliance/componentize-js @bytecodealliance/jco-std
yarn add -D rolldown
G```

```sh [pnpm]
mkdir my-app
cd my-app
pnpm init --init-type module
pnpm add hono
pnpm add -D @bytecodealliance/jco @bytecodealliance/componentize-js @bytecodealliance/jco-std
pnpm add -D rolldown
```

sh

```
mkdir my-app
cd my-app
npm init
bun add hono
bun add -D @bytecodealliance/jco @bytecodealliance/componentize-js @bytecodealliance/jco-std
```

INFO

To ensure your project uses ES modules, ensure `type` is set to `"module"` in `package.json`

After entering the `my-app` folder, install dependencies, and initialize Typescript:

npmyarnpnpmbunsh

```
npm i
npx tsc --init
```

sh

```
yarn
yarn tsc --init
```

sh

```
pnpm i
pnpm exec --init
```

sh

```
bun i
```

Once you have a basic typescript configuration file (`tsconfig.json`), please ensure it has the following configuration:

- `compilerOptions.module` set to `"nodenext"`

Since `componentize-js` (and `jco` which re-uses it) supports only single JS files, bundling is necessary, so [rolldown](https://rolldown.rs) can be used to create a single file bundle.

A Rolldown configuration (`rolldown.config.mjs`) like the following can be used:

js

```
import { defineConfig } from 'rolldown'

export default defineConfig({
  input: 'src/component.ts',
  external: /wasi:.*/,
  output: {
    file: 'dist/component.js',
    format: 'esm',
  },
})
```

INFO

Feel free to use any other bundlers that you're more comfortable with (`rolldown`, `esbuild`, `rollup`, etc)

## 2. Set up WIT interface & dependencies​

[WebAssembly Inteface Types (WIT)](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md) is an Interface Definition Language ("IDL") that governs what functionality a WebAssembly component uses ("imports"), and what it provides ("exports").

Amongst the standardized WIT interfaces, [wasi:http](https://github.com/WebAssembly/wasi-http) is for dealing with HTTP requests (whether it's receiving them or sending them out), and since we intend to make a web server, our component must declare the use of `wasi:http/incoming-handler` in it's [WIT world](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md#wit-worlds):

First, let's set up the component's WIT world in a file called `wit/component.wit`:

txt

```
package example:hono;

world component {
    export wasi:http/incoming-handler@0.2.6;
}
```

Put simply, the WIT file above means that our component "providers" the functionality of "receiving"/"handling incoming" HTTP requests.

The `wasi:http/incoming-handler` interface relies on upstream standardized WIT interfaces (specifications on how requests are structured, etc).

To pull those third party (Bytecode Alliance maintained) WIT interaces, one tool we can use is [wkg](https://github.com/bytecodealliance/wasm-pkg-tools):

sh

```
wkg wit fetch
```

Once `wkg` has finished running, you should find your `wit` folder populated with a new `deps` folder alongside `component.wit`:

```
wit
├── component.wit
└── deps
    ├── wasi-cli-0.2.6
    │   └── package.wit
    ├── wasi-clocks-0.2.6
    │   └── package.wit
    ├── wasi-http-0.2.6
    │   └── package.wit
    ├── wasi-io-0.2.6
    │   └── package.wit
    └── wasi-random-0.2.6
        └── package.wit
```

## 3. Hello Wasm​

To build a HTTP server in WebAssembly, we can make use of the [`jco-std`][jco-std] project, which contains helpers that make the experience very similar to the standard Hono experience.

Let's fulfill our `component` world with a basic Hono application as a WebAssembly component in a file called `src/component.ts`:

ts

```
import { Hono } from 'hono'
import { fire } from '@bytecodealliance/jco-std/wasi/0.2.6/http/adapters/hono/server'

const app = new Hono()

app.get('/hello', (c) => {
  return c.json({ message: 'Hello from WebAssembly!' })
})

fire(app)

// Although we've called `fire()` with wasi HTTP configured for use above,
// we still need to actually export the `wasi:http/incoming-handler` interface object,
// as jco and componentize-js will be looking for the ES module export that matches the WASI interface.
export { incomingHandler } from '@bytecodealliance/jco-std/wasi/0.2.6/http/adapters/hono/server'
```

## 4. Build​

Since we're using Rolldown (and it's configured to handle Typescript compilation), we can use it to build and bundle:

npmyarnpnpmbunsh

```
npx rolldown -c
```

sh

```
yarn rolldown -c
```

sh

```
pnpm exec rolldown -c
```

sh

```
bun build --target=bun --outfile=dist/component.js ./src/component.ts
```

INFO

The bundling step is necessary because WebAssembly JS ecosystem tooling only currently supports a single JS file, and we'd like to include Hono along with related libraries.

For components with simpler requirements, bundlers are not necessary.

To build your WebAssembly component, use `jco` (and indirectly `componentize-js`):

npmyarnpnpmbunsh

```
npx jco componentize -w wit -o dist/component.wasm dist/component.js
```

sh

```
yarn jco componentize -w wit -o dist/component.wasm dist/component.js
```

sh

```
pnpm exec jco componentize -w wit -o dist/component.wasm dist/component.js
```

sh

```
bun run jco componentize -w wit -o dist/component.wasm dist/component.js
```

## 3. Run​

To run your Hono WebAssembly HTTP server, you can use any WASI-enabled WebAssembly runtime:

- [wasmtime](https://wasmtime.dev)
- `jco` (runs in NodeJS)

In this guide, we'll use `jco serve` since it's already installed.

WARNING

`jco serve` is meant for development, and is not recommended for production use.

npmyarnpnpmbunsh

```
npx jco serve dist/component.wasm
```

sh

```
yarn jco serve dist/component.wasm
```

sh

```
pnpm exec jco serve dist/component.wasm
```

sh

```
bun run jco serve dist/component.wasm
```

You should see output like the following:

```
$ npx jco serve dist/component.wasm
Server listening @ localhost:8000...
```

Sending a request to `localhost:8000/hello` will produce the JSON output you've specified in your Hono application.

You should see output like the following:

json

```
{ "message": "Hello from WebAssembly!" }
```

INFO

`jco serve` works by converting the WebAssembly component into a basic WebAssembly coremodule, so that it can be run in runtimes like NodeJS and the browser.

This process is normally run via `jco transpile`, and is the way we can use JS engines like NodeJS and the browser (which may use V8 or other Javascript engines) as WebAssembly Component runtimes.

How `jco transpile` is outside the scope of this guide, you can read more about it in [the Jco book](https://bytecodealliance.github.io/jco/)

## More information​

To learn more about WASI, WebAssembly components and more, see the following resources:

- [BytecodeAlliance Component Model book](https://component-model.bytecodealliance.org/)
- [jcocodebase](https://github.com/bytecodealliance/jco)
  - [jcoexample components](https://github.com/bytecodealliance/jco/tree/main/examples/components) (in particular the [Hono example](https://github.com/bytecodealliance/jco/tree/main/examples/components/http-server-hono))
- [Jco book](https://bytecodealliance.github.io/jco/)
- [componentize-jscodebase](https://github.com/bytecodealliance/componentize-js)
- [StarlingMonkey codebase](https://github.com/bytecodealliance/StarlingMonkey)

To reach out to the WebAssembly community with questions, comments, contributions or to file issues:

- [Bytecode Alliance Zulip](https://bytecodealliance.zulipchat.com) (consider posting in the [#jco channel](https://bytecodealliance.zulipchat.com/#narrow/channel/409526-jco))
- [Jco repository](https://github.com/bytecodealliance/jco)
- [componentize-js repository](https://github.com/bytecodealliance/componentize-js)
