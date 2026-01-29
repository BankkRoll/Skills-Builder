# Alibaba Cloud Function Compute​ and more

# Alibaba Cloud Function Compute​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Alibaba Cloud Function Compute​

[Alibaba Cloud Function Compute](https://www.alibabacloud.com/en/product/function-compute) is a fully managed, event-driven compute service. Function Compute allows you to focus on writing and uploading code without having to manage infrastructure such as servers.

This guide uses a third-party adapter [rwv/hono-alibaba-cloud-fc3-adapter](https://github.com/rwv/hono-alibaba-cloud-fc3-adapter) to run Hono on Alibaba Cloud Function Compute.

## 1. Setup​

npmyarnpnpmbunsh

```
mkdir my-app
cd my-app
npm i hono hono-alibaba-cloud-fc3-adapter
npm i -D @serverless-devs/s esbuild
mkdir src
touch src/index.ts
```

sh

```
mkdir my-app
cd my-app
yarn add hono hono-alibaba-cloud-fc3-adapter
yarn add -D @serverless-devs/s esbuild
mkdir src
touch src/index.ts
```

sh

```
mkdir my-app
cd my-app
pnpm add hono hono-alibaba-cloud-fc3-adapter
pnpm add -D @serverless-devs/s esbuild
mkdir src
touch src/index.ts
```

sh

```
mkdir my-app
cd my-app
bun add hono hono-alibaba-cloud-fc3-adapter
bun add -D esbuild @serverless-devs/s
mkdir src
touch src/index.ts
```

## 2. Hello World​

Edit `src/index.ts`.

ts

```
import { Hono } from 'hono'
import { handle } from 'hono-alibaba-cloud-fc3-adapter'

const app = new Hono()

app.get('/', (c) => c.text('Hello Hono!'))

export const handler = handle(app)
```

## 3. Setup serverless-devs​

> [serverless-devs](https://github.com/Serverless-Devs/Serverless-Devs) is an open source and open serverless developer platform dedicated to providing developers with a powerful tool chain system. Through this platform, developers can not only experience multi cloud serverless products with one click and rapidly deploy serverless projects, but also manage projects in the whole life cycle of serverless applications, and combine serverless devs with other tools / platforms very simply and quickly to further improve the efficiency of R & D, operation and maintenance.

Add the Alibaba Cloud AccessKeyID & AccessKeySecret

sh

```
npx s config add
# Please select a provider: Alibaba Cloud (alibaba)
# Input your AccessKeyID & AccessKeySecret
```

Edit `s.yaml`

yaml

```
edition: 3.0.0
name: my-app
access: 'default'

vars:
  region: 'us-west-1'

resources:
  my-app:
    component: fc3
    props:
      region: ${vars.region}
      functionName: 'my-app'
      description: 'Hello World by Hono'
      runtime: 'nodejs20'
      code: ./dist
      handler: index.handler
      memorySize: 1024
      timeout: 300
```

Edit `scripts` section in `package.json`:

json

```
{
  "scripts": {
    "build": "esbuild --bundle --outfile=./dist/index.js --platform=node --target=node20 ./src/index.ts",
    "deploy": "s deploy -y"
  }
}
```

## 4. Deploy​

Finally, run the command to deploy:

sh

```
npm run build # Compile the TypeScript code to JavaScript
npm run deploy # Deploy the function to Alibaba Cloud Function Compute
```

---

# AWS Lambda​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# AWS Lambda​

AWS Lambda is a serverless platform by Amazon Web Services. You can run your code in response to events and automatically manages the underlying compute resources for you.

Hono works on AWS Lambda with the Node.js 18+ environment.

## 1. Setup​

When creating the application on AWS Lambda, [CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) is useful to setup the functions such as IAM Role, API Gateway, and others.

Initialize your project with the `cdk` CLI.

npmyarnpnpmbunsh

```
mkdir my-app
cd my-app
cdk init app -l typescript
npm i hono
npm i -D esbuild
mkdir lambda
touch lambda/index.ts
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
yarn add hono
yarn add -D esbuild
mkdir lambda
touch lambda/index.ts
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
pnpm add hono
pnpm add -D esbuild
mkdir lambda
touch lambda/index.ts
```

sh

```
mkdir my-app
cd my-app
cdk init app -l typescript
bun add hono
bun add -D esbuild
mkdir lambda
touch lambda/index.ts
```

## 2. Hello World​

Edit `lambda/index.ts`.

ts

```
import { Hono } from 'hono'
import { handle } from 'hono/aws-lambda'

const app = new Hono()

app.get('/', (c) => c.text('Hello Hono!'))

export const handler = handle(app)
```

## 3. Deploy​

Edit `lib/my-app-stack.ts`.

ts

```
import * as cdk from 'aws-cdk-lib'
import { Construct } from 'constructs'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs'

export class MyAppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props)

    const fn = new NodejsFunction(this, 'lambda', {
      entry: 'lambda/index.ts',
      handler: 'handler',
      runtime: lambda.Runtime.NODEJS_22_X,
    })
    const fnUrl = fn.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
    })
    new cdk.CfnOutput(this, 'lambdaUrl', {
      value: fnUrl.url!,
    })
  }
}
```

Finally, run the command to deploy:

sh

```
cdk deploy
```

## Serve Binary data​

Hono supports binary data as a response. In Lambda, base64 encoding is required to return binary data. Once binary type is set to `Content-Type` header, Hono automatically encodes data to base64.

ts

```
app.get('/binary', async (c) => {
  // ...
  c.status(200)
  c.header('Content-Type', 'image/png') // means binary data
  return c.body(buffer) // supports `ArrayBufferLike` type, encoded to base64.
})
```

## Access AWS Lambda Object​

In Hono, you can access the AWS Lambda Events and Context by binding the `LambdaEvent`, `LambdaContext` type and using `c.env`

ts

```
import { Hono } from 'hono'
import type { LambdaEvent, LambdaContext } from 'hono/aws-lambda'
import { handle } from 'hono/aws-lambda'

type Bindings = {
  event: LambdaEvent
  lambdaContext: LambdaContext
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/aws-lambda-info/', (c) => {
  return c.json({
    isBase64Encoded: c.env.event.isBase64Encoded,
    awsRequestId: c.env.lambdaContext.awsRequestId,
  })
})

export const handler = handle(app)
```

## Access RequestContext​

In Hono, you can access the AWS Lambda request context by binding the `LambdaEvent` type and using `c.env.event.requestContext`.

ts

```
import { Hono } from 'hono'
import type { LambdaEvent } from 'hono/aws-lambda'
import { handle } from 'hono/aws-lambda'

type Bindings = {
  event: LambdaEvent
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/custom-context/', (c) => {
  const lambdaContext = c.env.event.requestContext
  return c.json(lambdaContext)
})

export const handler = handle(app)
```

### Before v3.10.0 (deprecated)​

you can access the AWS Lambda request context by binding the `ApiGatewayRequestContext` type and using `c.env.`

ts

```
import { Hono } from 'hono'
import type { ApiGatewayRequestContext } from 'hono/aws-lambda'
import { handle } from 'hono/aws-lambda'

type Bindings = {
  requestContext: ApiGatewayRequestContext
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/custom-context/', (c) => {
  const lambdaContext = c.env.requestContext
  return c.json(lambdaContext)
})

export const handler = handle(app)
```

## Lambda response streaming​

By changing the invocation mode of AWS Lambda, you can achieve [Streaming Response](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-response-streaming/).

diff

```
fn.addFunctionUrl({
  authType: lambda.FunctionUrlAuthType.NONE,
+  invokeMode: lambda.InvokeMode.RESPONSE_STREAM,
})
```

Typically, the implementation requires writing chunks to NodeJS.WritableStream using awslambda.streamifyResponse, but with the AWS Lambda Adaptor, you can achieve the traditional streaming response of Hono by using streamHandle instead of handle.

ts

```
import { Hono } from 'hono'
import { streamHandle } from 'hono/aws-lambda'
import { streamText } from 'hono/streaming'

const app = new Hono()

app.get('/stream', async (c) => {
  return streamText(c, async (stream) => {
    for (let i = 0; i < 3; i++) {
      await stream.writeln(`${i}`)
      await stream.sleep(1)
    }
  })
})

export const handler = streamHandle(app)
```

---

# Azure Functions​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Azure Functions​

[Azure Functions](https://azure.microsoft.com/en-us/products/functions) is a serverless platform from Microsoft Azure. You can run your code in response to events, and it automatically manages the underlying compute resources for you.

Hono was not designed for Azure Functions at first. But with [Azure Functions Adapter](https://github.com/Marplex/hono-azurefunc-adapter) it can run on it as well.

It works with Azure Functions **V4** running on Node.js 18 or above.

## 1. Install CLI​

To create an Azure Function, you must first install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-typescript?pivots=nodejs-model-v4#install-the-azure-functions-core-tools).

On macOS

sh

```
brew tap azure/functions
brew install azure-functions-core-tools@4
```

Follow this link for other OS:

- [Install the Azure Functions Core Tools | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-typescript?pivots=nodejs-model-v4#install-the-azure-functions-core-tools)

## 2. Setup​

Create a TypeScript Node.js V4 project in the current folder.

sh

```
func init --typescript
```

Change the default route prefix of the host. Add this property to the root json object of `host.json`:

json

```
"extensions": {
    "http": {
        "routePrefix": ""
    }
}
```

INFO

The default Azure Functions route prefix is `/api`. If you don't change it as shown above, be sure to start all your Hono routes with `/api`

Now you are ready to install Hono and the Azure Functions Adapter with:

npmyarnpnpmbunsh

```
npm i @marplex/hono-azurefunc-adapter hono
```

sh

```
yarn add @marplex/hono-azurefunc-adapter hono
```

sh

```
pnpm add @marplex/hono-azurefunc-adapter hono
```

sh

```
bun add @marplex/hono-azurefunc-adapter hono
```

## 3. Hello World​

Create `src/app.ts`:

ts

```
// src/app.ts
import { Hono } from 'hono'
const app = new Hono()

app.get('/', (c) => c.text('Hello Azure Functions!'))

export default app
```

Create `src/functions/httpTrigger.ts`:

ts

```
// src/functions/httpTrigger.ts
import { app } from '@azure/functions'
import { azureHonoHandler } from '@marplex/hono-azurefunc-adapter'
import honoApp from '../app'

app.http('httpTrigger', {
  methods: [
    //Add all your supported HTTP methods here
    'GET',
    'POST',
    'DELETE',
    'PUT',
  ],
  authLevel: 'anonymous',
  route: '{*proxy}',
  handler: azureHonoHandler(honoApp.fetch),
})
```

## 4. Run​

Run the development server locally. Then, access `http://localhost:7071` in your Web browser.

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
pnpm start
```

sh

```
bun run start
```

## 5. Deploy​

INFO

Before you can deploy to Azure, you need to create some resources in your cloud infrastructure. Please visit the Microsoft documentation on [Create supporting Azure resources for your function](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-typescript?pivots=nodejs-model-v4&tabs=windows%2Cazure-cli%2Cbrowser#create-supporting-azure-resources-for-your-function)

Build the project for deployment:

npmyarnpnpmbunsh

```
npm run build
```

sh

```
yarn build
```

sh

```
pnpm build
```

sh

```
bun run build
```

Deploy your project to the function app in Azure Cloud. Replace `<YourFunctionAppName>` with the name of your app.

sh

```
func azure functionapp publish <YourFunctionAppName>
```

---

# Getting Started​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Getting Started​

Using Hono is super easy. We can set up the project, write code, develop with a local server, and deploy quickly. The same code will work on any runtime, just with different entry points. Let's look at the basic usage of Hono.

## Starter​

Starter templates are available for each platform. Use the following "create-hono" command.

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
pnpm create hono@latest my-app
```

sh

```
bun create hono@latest my-app
```

sh

```
deno init --npm hono@latest my-app
```

Then you will be asked which template you would like to use. Let's select Cloudflare Workers for this example.

```
? Which template do you want to use?
    aws-lambda
    bun
    cloudflare-pages
❯   cloudflare-workers
    deno
    fastly
    nextjs
    nodejs
    vercel
```

The template will be pulled into `my-app`, so go to it and install the dependencies.

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

Once the package installation is complete, run the following command to start up a local server.

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

## Hello World​

You can write code in TypeScript with the Cloudflare Workers development tool "Wrangler", Deno, Bun, or others without being aware of transpiling.

Write your first application with Hono in `src/index.ts`. The example below is a starter Hono application.

The `import` and the final `export default` parts may vary from runtime to runtime, but all of the application code will run the same code everywhere.

ts

```
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.text('Hello Hono!')
})

export default app
```

Start the development server and access `http://localhost:8787` with your browser.

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

## Return JSON​

Returning JSON is also easy. The following is an example of handling a GET Request to `/api/hello` and returning an `application/json` Response.

ts

```
app.get('/api/hello', (c) => {
  return c.json({
    ok: true,
    message: 'Hello Hono!',
  })
})
```

## Request and Response​

Getting a path parameter, URL query value, and appending a Response header is written as follows.

ts

```
app.get('/posts/:id', (c) => {
  const page = c.req.query('page')
  const id = c.req.param('id')
  c.header('X-Message', 'Hi!')
  return c.text(`You want to see ${page} of ${id}`)
})
```

We can easily handle POST, PUT, and DELETE not only GET.

ts

```
app.post('/posts', (c) => c.text('Created!', 201))
app.delete('/posts/:id', (c) =>
  c.text(`${c.req.param('id')} is deleted!`)
)
```

## Return HTML​

You can write HTML with [the html Helper](https://hono.dev/docs/helpers/html) or using [JSX](https://hono.dev/docs/guides/jsx) syntax. If you want to use JSX, rename the file to `src/index.tsx` and configure it (check with each runtime as it is different). Below is an example using JSX.

tsx

```
const View = () => {
  return (
    <html>
      <body>
        <h1>Hello Hono!</h1>
      </body>
    </html>
  )
}

app.get('/page', (c) => {
  return c.html(<View />)
})
```

## Return raw Response​

You can also return the raw [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response).

ts

```
app.get('/', () => {
  return new Response('Good morning!')
})
```

## Using Middleware​

Middleware can do the hard work for you. For example, add in Basic Authentication.

ts

```
import { basicAuth } from 'hono/basic-auth'

// ...

app.use(
  '/admin/*',
  basicAuth({
    username: 'admin',
    password: 'secret',
  })
)

app.get('/admin', (c) => {
  return c.text('You are authorized!')
})
```

There are useful built-in middleware including Bearer and authentication using JWT, CORS and ETag. Hono also provides third-party middleware using external libraries such as GraphQL Server and Firebase Auth. And, you can make your own middleware.

## Adapter​

There are Adapters for platform-dependent functions, e.g., handling static files or WebSocket. For example, to handle WebSocket in Cloudflare Workers, import `hono/cloudflare-workers`.

ts

```
import { upgradeWebSocket } from 'hono/cloudflare-workers'

app.get(
  '/ws',
  upgradeWebSocket((c) => {
    // ...
  })
)
```

## Next step​

Most code will work on any platform, but there are guides for each. For instance, how to set up projects or how to deploy. Please see the page for the exact platform you want to use to create your application!

---

# Bun​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Bun​

[Bun](https://bun.com) is another JavaScript runtime. It's not Node.js or Deno. Bun includes a trans compiler, we can write the code with TypeScript. Hono also works on Bun.

## 1. Install Bun​

To install `bun` command, follow the instruction in [the official web site](https://bun.com).

## 2. Setup​

### 2.1. Setup a new project​

A starter for Bun is available. Start your project with "bun create" command. Select `bun` template for this example.

sh

```
bun create hono@latest my-app
```

Move into my-app and install the dependencies.

sh

```
cd my-app
bun install
```

### 2.2. Setup an existing project​

On an existing Bun project, we only need to install `hono` dependencies on the project root directory via

sh

```
bun add hono
```

Then add the `dev` command to your existing `package.json`.

json

```
{
  "scripts": {
    "dev": "bun run --hot src/index.ts"
  }
}
```

See the [Bun starter template](https://github.com/honojs/starter/tree/main/templates/bun) for a minimal example setup. This is the output of running `bun create hono@latest`.

## 3. Hello World​

"Hello World" script is below. Almost the same as writing on other platforms.

ts

```
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Bun!'))

export default app
```

If you are setting up Hono on an existing project, the `bun run dev` command expects the "Hello World" script to be placed in `src/index.tx`

## 4. Run​

Run the command.

sh

```
bun run dev
```

Then, access `http://localhost:3000` in your browser.

## Change port number​

You can specify the port number with exporting the `port`.

ts

```
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Bun!'))

export default app
export default {
  port: 3000,
  fetch: app.fetch,
}
```

## Serve static files​

To serve static files, use `serveStatic` imported from `hono/bun`.

ts

```
import { serveStatic } from 'hono/bun'

const app = new Hono()

app.use('/static/*', serveStatic({ root: './' }))
app.use('/favicon.ico', serveStatic({ path: './favicon.ico' }))
app.get('/', (c) => c.text('You can access: /static/hello.txt'))
app.get('*', serveStatic({ path: './static/fallback.txt' }))
```

For the above code, it will work well with the following directory structure.

```
./
├── favicon.ico
├── src
└── static
    ├── demo
    │   └── index.html
    ├── fallback.txt
    ├── hello.txt
    └── images
        └── dinotocat.png
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

### mimes​

You can add MIME types with `mimes`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    mimes: {
      m3u8: 'application/vnd.apple.mpegurl',
      ts: 'video/mp2t',
    },
  })
)
```

### onFound​

You can specify handling when the requested file is found with `onFound`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    // ...
    onFound: (_path, c) => {
      c.header('Cache-Control', `public, immutable, max-age=31536000`)
    },
  })
)
```

### onNotFound​

You can specify handling when the requested file is not found with `onNotFound`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    onNotFound: (path, c) => {
      console.log(`${path} is not found, you access ${c.req.path}`)
    },
  })
)
```

### precompressed​

The `precompressed` option checks if files with extensions like `.br` or `.gz` are available and serves them based on the `Accept-Encoding` header. It prioritizes Brotli, then Zstd, and Gzip. If none are available, it serves the original file.

ts

```
app.get(
  '/static/*',
  serveStatic({
    precompressed: true,
  })
)
```

## Testing​

You can use `bun:test` for testing on Bun.

ts

```
import { describe, expect, it } from 'bun:test'
import app from '.'

describe('My first test', () => {
  it('Should return 200 Response', async () => {
    const req = new Request('http://localhost/')
    const res = await app.fetch(req)
    expect(res.status).toBe(200)
  })
})
```

Then, run the command.

sh

```
bun test index.test.ts
```

---

# Cloudflare Pages​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Cloudflare Pages​

[Cloudflare Pages](https://pages.cloudflare.com) is an edge platform for full-stack web applications. It serves static files and dynamic content provided by Cloudflare Workers.

Hono fully supports Cloudflare Pages. It introduces a delightful developer experience. Vite's dev server is fast, and deploying with Wrangler is super quick.

## 1. Setup​

A starter for Cloudflare Pages is available. Start your project with "create-hono" command. Select `cloudflare-pages` template for this example.

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

Below is a basic directory structure.

text

```
./
├── package.json
├── public
│   └── static // Put your static files.
│       └── style.css // You can refer to it as `/static/style.css`.
├── src
│   ├── index.tsx // The entry point for server-side.
│   └── renderer.tsx
├── tsconfig.json
└── vite.config.ts
```

## 2. Hello World​

Edit `src/index.tsx` like the following:

tsx

```
import { Hono } from 'hono'
import { renderer } from './renderer'

const app = new Hono()

app.get('*', renderer)

app.get('/', (c) => {
  return c.render(<h1>Hello, Cloudflare Pages!</h1>)
})

export default app
```

## 3. Run​

Run the development server locally. Then, access `http://localhost:5173` in your Web browser.

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

## 4. Deploy​

If you have a Cloudflare account, you can deploy to Cloudflare. In `package.json`, `$npm_execpath` needs to be changed to your package manager of choice.

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

### Deploy via the Cloudflare dashboard with GitHub​

1. Log in to the [Cloudflare dashboard](https://dash.cloudflare.com) and select your account.
2. In Account Home, select Workers & Pages > Create application > Pages > Connect to Git.
3. Authorize your GitHub account, and select the repository. In Set up builds and deployments, provide the following information:

| Configuration option | Value |
| --- | --- |
| Production branch | main |
| Build command | npm run build |
| Build directory | dist |

## Bindings​

You can use Cloudflare Bindings like Variables, KV, D1, and others. In this section, let's use Variables and KV.

### Createwrangler.toml​

First, create `wrangler.toml` for local Bindings:

sh

```
touch wrangler.toml
```

Edit `wrangler.toml`. Specify Variable with the name `MY_NAME`.

toml

```
[vars]
MY_NAME = "Hono"
```

### Create KV​

Next, make the KV. Run the following `wrangler` command:

sh

```
wrangler kv namespace create MY_KV --preview
```

Note down the `preview_id` as the following output:

```
{ binding = "MY_KV", preview_id = "abcdef" }
```

Specify `preview_id` with the name of Bindings, `MY_KV`:

toml

```
[[kv_namespaces]]
binding = "MY_KV"
id = "abcdef"
```

### Editvite.config.ts​

Edit the `vite.config.ts`:

ts

```
import devServer from '@hono/vite-dev-server'
import adapter from '@hono/vite-dev-server/cloudflare'
import build from '@hono/vite-cloudflare-pages'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    devServer({
      entry: 'src/index.tsx',
      adapter, // Cloudflare Adapter
    }),
    build(),
  ],
})
```

### Use Bindings in your application​

Use Variable and KV in your application. Set the types.

ts

```
type Bindings = {
  MY_NAME: string
  MY_KV: KVNamespace
}

const app = new Hono<{ Bindings: Bindings }>()
```

Use them:

tsx

```
app.get('/', async (c) => {
  await c.env.MY_KV.put('name', c.env.MY_NAME)
  const name = await c.env.MY_KV.get('name')
  return c.render(<h1>Hello! {name}</h1>)
})
```

### In production​

For Cloudflare Pages, you will use `wrangler.toml` for local development, but for production, you will set up Bindings in the dashboard.

## Client-side​

You can write client-side scripts and import them into your application using Vite's features. If `/src/client.ts` is the entry point for the client, simply write it in the script tag. Additionally, `import.meta.env.PROD` is useful for detecting whether it's running on a dev server or in the build phase.

tsx

```
app.get('/', (c) => {
  return c.html(
    <html>
      <head>
        {import.meta.env.PROD ? (
          <script type='module' src='/static/client.js'></script>
        ) : (
          <script type='module' src='/src/client.ts'></script>
        )}
      </head>
      <body>
        <h1>Hello</h1>
      </body>
    </html>
  )
})
```

In order to build the script properly, you can use the example config file `vite.config.ts` as shown below.

ts

```
import pages from '@hono/vite-cloudflare-pages'
import devServer from '@hono/vite-dev-server'
import { defineConfig } from 'vite'

export default defineConfig(({ mode }) => {
  if (mode === 'client') {
    return {
      build: {
        rollupOptions: {
          input: './src/client.ts',
          output: {
            entryFileNames: 'static/client.js',
          },
        },
      },
    }
  } else {
    return {
      plugins: [
        pages(),
        devServer({
          entry: 'src/index.tsx',
        }),
      ],
    }
  }
})
```

You can run the following command to build the server and client script.

sh

```
vite build --mode client && vite build
```

## Cloudflare Pages Middleware​

Cloudflare Pages uses its own [middleware](https://developers.cloudflare.com/pages/functions/middleware/) system that is different from Hono's middleware. You can enable it by exporting `onRequest` in a file named `_middleware.ts` like this:

ts

```
// functions/_middleware.ts
export async function onRequest(pagesContext) {
  console.log(`You are accessing ${pagesContext.request.url}`)
  return await pagesContext.next()
}
```

Using `handleMiddleware`, you can use Hono's middleware as Cloudflare Pages middleware.

ts

```
// functions/_middleware.ts
import { handleMiddleware } from 'hono/cloudflare-pages'

export const onRequest = handleMiddleware(async (c, next) => {
  console.log(`You are accessing ${c.req.url}`)
  await next()
})
```

You can also use built-in and 3rd party middleware for Hono. For example, to add Basic Authentication, you can use [Hono's Basic Authentication Middleware](https://hono.dev/docs/middleware/builtin/basic-auth).

ts

```
// functions/_middleware.ts
import { handleMiddleware } from 'hono/cloudflare-pages'
import { basicAuth } from 'hono/basic-auth'

export const onRequest = handleMiddleware(
  basicAuth({
    username: 'hono',
    password: 'acoolproject',
  })
)
```

If you want to apply multiple middleware, you can write it like this:

ts

```
import { handleMiddleware } from 'hono/cloudflare-pages'

// ...

export const onRequest = [
  handleMiddleware(middleware1),
  handleMiddleware(middleware2),
  handleMiddleware(middleware3),
]
```

### AccessingEventContext​

You can access [EventContext](https://developers.cloudflare.com/pages/functions/api-reference/#eventcontext) object via `c.env` in `handleMiddleware`.

ts

```
// functions/_middleware.ts
import { handleMiddleware } from 'hono/cloudflare-pages'

export const onRequest = [
  handleMiddleware(async (c, next) => {
    c.env.eventContext.data.user = 'Joe'
    await next()
  }),
]
```

Then, you can access the data value in via `c.env.eventContext` in the handler:

ts

```
// functions/api/[[route]].ts
import type { EventContext } from 'hono/cloudflare-pages'
import { handle } from 'hono/cloudflare-pages'

// ...

type Env = {
  Bindings: {
    eventContext: EventContext
  }
}

const app = new Hono<Env>().basePath('/api')

app.get('/hello', (c) => {
  return c.json({
    message: `Hello, ${c.env.eventContext.data.user}!`, // 'Joe'
  })
})

export const onRequest = handle(app)
```

---

# Cloudflare Workers​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Cloudflare Workers​

[Cloudflare Workers](https://workers.cloudflare.com) is a JavaScript edge runtime on Cloudflare CDN.

You can develop the application locally and publish it with a few commands using [Wrangler](https://developers.cloudflare.com/workers/wrangler/). Wrangler includes trans compiler, so we can write the code with TypeScript.

Let’s make your first application for Cloudflare Workers with Hono.

## 1. Setup​

A starter for Cloudflare Workers is available. Start your project with "create-hono" command. Select `cloudflare-workers` template for this example.

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

Edit `src/index.ts` like below.

ts

```
import { Hono } from 'hono'
const app = new Hono()

app.get('/', (c) => c.text('Hello Cloudflare Workers!'))

export default app
```

## 3. Run​

Run the development server locally. Then, access `http://localhost:8787` in your web browser.

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

### Change port number​

If you need to change the port number you can follow the instructions here to update `wrangler.toml` / `wrangler.json` / `wrangler.jsonc` files: [Wrangler Configuration](https://developers.cloudflare.com/workers/wrangler/configuration/#local-development-settings)

Or, you can follow the instructions here to set CLI options: [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/commands/#dev)

## 4. Deploy​

If you have a Cloudflare account, you can deploy to Cloudflare. In `package.json`, `$npm_execpath` needs to be changed to your package manager of choice.

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

That's all!

## Using Hono with other event handlers​

You can integrate Hono with other event handlers (such as `scheduled`) in *Module Worker mode*.

To do this, export `app.fetch` as the module's `fetch` handler, and then implement other handlers as needed:

ts

```
const app = new Hono()

export default {
  fetch: app.fetch,
  scheduled: async (batch, env) => {},
}
```

## Serve static files​

If you want to serve static files, you can use [the Static Assets feature](https://developers.cloudflare.com/workers/static-assets/) of Cloudflare Workers. Specify the directory for the files in `wrangler.toml`:

toml

```
assets = { directory = "public" }
```

Then create the `public` directory and place the files there. For instance, `./public/static/hello.txt` will be served as `/static/hello.txt`.

```
.
├── package.json
├── public
│   ├── favicon.ico
│   └── static
│       └── hello.txt
├── src
│   └── index.ts
└── wrangler.toml
```

## Types​

You have to install `@cloudflare/workers-types` if you want to have workers types.

npmyarnpnpmbunsh

```
npm i --save-dev @cloudflare/workers-types
```

sh

```
yarn add -D @cloudflare/workers-types
```

sh

```
pnpm add -D @cloudflare/workers-types
```

sh

```
bun add --dev @cloudflare/workers-types
```

## Testing​

For testing, we recommend using `@cloudflare/vitest-pool-workers`. Refer to [examples](https://github.com/honojs/examples) for setting it up.

If there is the application below.

ts

```
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Please test me!'))
```

We can test if it returns "*200 OK*" Response with this code.

ts

```
describe('Test the application', () => {
  it('Should return 200 response', async () => {
    const res = await app.request('http://localhost/')
    expect(res.status).toBe(200)
  })
})
```

## Bindings​

In the Cloudflare Workers, we can bind the environment values, KV namespace, R2 bucket, or Durable Object. You can access them in `c.env`. It will have the types if you pass the "*type struct*" for the bindings to the `Hono` as generics.

ts

```
type Bindings = {
  MY_BUCKET: R2Bucket
  USERNAME: string
  PASSWORD: string
}

const app = new Hono<{ Bindings: Bindings }>()

// Access to environment values
app.put('/upload/:key', async (c, next) => {
  const key = c.req.param('key')
  await c.env.MY_BUCKET.put(key, c.req.body)
  return c.text(`Put ${key} successfully!`)
})
```

## Using Variables in Middleware​

This is the only case for Module Worker mode. If you want to use Variables or Secret Variables in Middleware, for example, "username" or "password" in Basic Authentication Middleware, you need to write like the following.

ts

```
import { basicAuth } from 'hono/basic-auth'

type Bindings = {
  USERNAME: string
  PASSWORD: string
}

const app = new Hono<{ Bindings: Bindings }>()

//...

app.use('/auth/*', async (c, next) => {
  const auth = basicAuth({
    username: c.env.USERNAME,
    password: c.env.PASSWORD,
  })
  return auth(c, next)
})
```

The same is applied to Bearer Authentication Middleware, JWT Authentication, or others.

## Deploy from GitHub Actions​

Before deploying code to Cloudflare via CI, you need a Cloudflare token. You can manage it from [User API Tokens](https://dash.cloudflare.com/profile/api-tokens).

If it's a newly created token, select the **Edit Cloudflare Workers** template, if you already have another token, make sure the token has the corresponding permissions(No, token permissions are not shared between Cloudflare Pages and Cloudflare Workers).

then go to your GitHub repository settings dashboard: `Settings->Secrets and variables->Actions->Repository secrets`, and add a new secret with the name `CLOUDFLARE_API_TOKEN`.

then create `.github/workflows/deploy.yml` in your Hono project root folder, paste the following code:

yml

```
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deploy
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

then edit `wrangler.toml`, and add this code after `compatibility_date` line.

toml

```
main = "src/index.ts"
minify = true
```

Everything is ready! Now push the code and enjoy it.

## Load env when local development​

To configure the environment variables for local development, create a `.dev.vars` file or a `.env` file in the root directory of the project. These files should be formatted using the [dotenv](https://hexdocs.pm/dotenvy/dotenv-file-format.html) syntax. For example:

```
SECRET_KEY=value
API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

> For more about this section you can find in the Cloudflare documentation: [https://developers.cloudflare.com/workers/wrangler/configuration/#secrets](https://developers.cloudflare.com/workers/wrangler/configuration/#secrets)

Then we use the `c.env.*` to get the environment variables in our code.

INFO

By default, `process.env` is not available in Cloudflare Workers, so it is recommended to get environment variables from `c.env`. If you want to use it, you need to enable [nodejs_compat_populate_process_env](https://developers.cloudflare.com/workers/configuration/compatibility-flags/#enable-auto-populating-processenv) flag. You can also import `env` from `cloudflare:workers`. For details, please see [How to accessenvon Cloudflare docs](https://developers.cloudflare.com/workers/runtime-apis/bindings/#how-to-access-env)

ts

```
type Bindings = {
  SECRET_KEY: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/env', (c) => {
  const SECRET_KEY = c.env.SECRET_KEY
  return c.text(SECRET_KEY)
})
```

Before you deploy your project to Cloudflare, remember to set the environment variable/secrets in the Cloudflare Workers project's configuration.

> For more about this section you can find in the Cloudflare documentation: [https://developers.cloudflare.com/workers/configuration/environment-variables/#add-environment-variables-via-the-dashboard](https://developers.cloudflare.com/workers/configuration/environment-variables/#add-environment-variables-via-the-dashboard)

---

# Deno​

> Web framework built on Web Standards for Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel, Node.js, and others. Fast, but not only fast.

# Deno​

[Deno](https://deno.com/) is a JavaScript runtime built on V8. It's not Node.js. Hono also works on Deno.

You can use Hono, write the code with TypeScript, run the application with the `deno` command, and deploy it to "Deno Deploy".

## 1. Install Deno​

First, install `deno` command. Please refer to [the official document](https://docs.deno.com/runtime/getting_started/installation/).

## 2. Setup​

A starter for Deno is available. Start your project with the [deno init](https://docs.deno.com/runtime/reference/cli/init/) command.

sh

```
deno init --npm hono --template=deno my-app
```

Move into `my-app`. For Deno, you don't have to install Hono explicitly.

sh

```
cd my-app
```

## 3. Hello World​

Edit `main.ts`:

main.tsts

```
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hello Deno!'))

Deno.serve(app.fetch)
```

## 4. Run​

Run the development server locally. Then, access `http://localhost:8000` in your Web browser.

sh

```
deno task start
```

## Change port number​

You can specify the port number by updating the arguments of `Deno.serve` in `main.ts`:

ts

```
Deno.serve(app.fetch)
Deno.serve({ port: 8787 }, app.fetch)
```

## Serve static files​

To serve static files, use `serveStatic` imported from `hono/deno`.

ts

```
import { Hono } from 'hono'
import { serveStatic } from 'hono/deno'

const app = new Hono()

app.use('/static/*', serveStatic({ root: './' }))
app.use('/favicon.ico', serveStatic({ path: './favicon.ico' }))
app.get('/', (c) => c.text('You can access: /static/hello.txt'))
app.get('*', serveStatic({ path: './static/fallback.txt' }))

Deno.serve(app.fetch)
```

For the above code, it will work well with the following directory structure.

```
./
├── favicon.ico
├── index.ts
└── static
    ├── demo
    │   └── index.html
    ├── fallback.txt
    ├── hello.txt
    └── images
        └── dinotocat.png
```

### rewriteRequestPath​

If you want to map `http://localhost:8000/static/*` to `./statics`, you can use the `rewriteRequestPath` option:

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

### mimes​

You can add MIME types with `mimes`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    mimes: {
      m3u8: 'application/vnd.apple.mpegurl',
      ts: 'video/mp2t',
    },
  })
)
```

### onFound​

You can specify handling when the requested file is found with `onFound`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    // ...
    onFound: (_path, c) => {
      c.header('Cache-Control', `public, immutable, max-age=31536000`)
    },
  })
)
```

### onNotFound​

You can specify handling when the requested file is not found with `onNotFound`:

ts

```
app.get(
  '/static/*',
  serveStatic({
    onNotFound: (path, c) => {
      console.log(`${path} is not found, you access ${c.req.path}`)
    },
  })
)
```

### precompressed​

The `precompressed` option checks if files with extensions like `.br` or `.gz` are available and serves them based on the `Accept-Encoding` header. It prioritizes Brotli, then Zstd, and Gzip. If none are available, it serves the original file.

ts

```
app.get(
  '/static/*',
  serveStatic({
    precompressed: true,
  })
)
```

## Deno Deploy​

Deno Deploy is a serverless platform for running JavaScript and TypeScript applications in the cloud. It provides a management plane for deploying and running applications through integrations like GitHub deployment.

Hono also works on Deno Deploy. Please refer to [the official document](https://docs.deno.com/deploy/manual/).

## Testing​

Testing the application on Deno is easy. You can write with `Deno.test` and use `assert` or `assertEquals` from [@std/assert](https://jsr.io/@std/assert).

sh

```
deno add jsr:@std/assert
```

hello.tsts

```
import { Hono } from 'hono'
import { assertEquals } from '@std/assert'

Deno.test('Hello World', async () => {
  const app = new Hono()
  app.get('/', (c) => c.text('Please test me'))

  const res = await app.request('http://localhost/')
  assertEquals(res.status, 200)
})
```

Then run the command:

sh

```
deno test hello.ts
```

## npm and JSR​

Hono is available on both [npm](https://www.npmjs.com/package/hono) and [JSR](https://jsr.io/@hono/hono) (the JavaScript Registry). You can use either `npm:hono` or `jsr:@hono/hono` in your `deno.json`:

json

```
{
  "imports": {
    "hono": "jsr:@hono/hono"
    "hono": "npm:hono"
  }
}
```

To use middleware you need to use the [Deno directory](https://docs.deno.com/runtime/fundamentals/configuration/#custom-path-mappings) syntaxt in the import

json

```
{
  "imports": {
    "hono/": "npm:/hono/"
  }
}
```

When using third-party middleware, you may need to use Hono from the same registry as the middleware for proper TypeScript type inference. For example, if using the middleware from npm, you should also use Hono from npm:

json

```
{
  "imports": {
    "hono": "npm:hono",
    "zod": "npm:zod",
    "@hono/zod-validator": "npm:@hono/zod-validator"
  }
}
```

We also provide many third-party middleware packages on [JSR](https://jsr.io/@hono). When using the middleware on JSR, use Hono from JSR:

json

```
{
  "imports": {
    "hono": "jsr:@hono/hono",
    "zod": "npm:zod",
    "@hono/zod-validator": "jsr:@hono/zod-validator"
  }
}
```
