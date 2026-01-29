# Supabase & Astro and more

# Supabase & Astro

> Add a backend to your project with Supabase

# Supabase & Astro

[Supabase](https://supabase.com/) is an open source Firebase alternative. It provides a Postgres database, authentication, edge functions, realtime subscriptions, and storage.

## Initializing Supabase in Astro

[Section titled “Initializing Supabase in Astro”](#initializing-supabase-in-astro)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- A Supabase project. If you don’t have one, you can sign up for free at [supabase.com](https://supabase.com/) and create a new project.
- An Astro project with [output: 'server'for on-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/) enabled.
- Supabase credentials for your project. You can find these in the **Settings > API** tab of your Supabase project.
  - `SUPABASE_URL`: The URL of your Supabase project.
  - `SUPABASE_ANON_KEY`: The anonymous key for your Supabase project.

### Adding Supabase credentials

[Section titled “Adding Supabase credentials”](#adding-supabase-credentials)

To add your Supabase credentials to your Astro project, add the following to your `.env` file:

 .env

```
SUPABASE_URL=YOUR_SUPABASE_URLSUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
```

Now, these environment variables are available in your project.

If you would like to have IntelliSense for your environment variables, edit or create the `env.d.ts` in your `src/` directory and add the following:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly SUPABASE_URL: string  readonly SUPABASE_ANON_KEY: string}
interface ImportMeta {  readonly env: ImportMetaEnv}
```

Your project should now include these files:

- Directorysrc/
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json

### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

To connect to Supabase, you will need to install `@supabase/supabase-js` in your project.

- [npm](#tab-panel-2741)
- [pnpm](#tab-panel-2742)
- [Yarn](#tab-panel-2743)

   Terminal window

```
npm install @supabase/supabase-js
```

   Terminal window

```
pnpm add @supabase/supabase-js
```

   Terminal window

```
yarn add @supabase/supabase-js
```

Next, create a folder named `lib` in your `src/` directory. This is where you will add your Supabase client.

In `supabase.ts`, add the following to initialize your Supabase client:

 src/lib/supabase.ts

```
import { createClient } from "@supabase/supabase-js";
export const supabase = createClient(  import.meta.env.SUPABASE_URL,  import.meta.env.SUPABASE_ANON_KEY,);
```

Now, your project should include these files:

- Directorysrc/
  - Directorylib/
    - **supabase.ts**
  - env.d.ts
- .env
- astro.config.mjs
- package.json

## Adding authentication with Supabase

[Section titled “Adding authentication with Supabase”](#adding-authentication-with-supabase)

Supabase provides authentication out of the box. It supports email/password authentication and OAuth authentication with many providers including GitHub, Google, and several others.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

- An Astro project [initialized with Supabase](#initializing-supabase-in-astro).
- A Supabase project with email/password authentication enabled. You can enable this in the **Authentication > Providers** tab of your Supabase project.

### Creating auth server endpoints

[Section titled “Creating auth server endpoints”](#creating-auth-server-endpoints)

To add authentication to your project, you will need to create a few server endpoints. These endpoints will be used to register, sign in, and sign out users.

- `POST /api/auth/register`: to register a new user.
- `POST /api/auth/signin`: to sign in a user.
- `GET /api/auth/signout`: to sign out a user.

Create these endpoints in the `src/pages/api/auth` directory of your project. If you are using `static` rendering mode, you must specify `export const prerender = false` at the top of each file to render these endpoints on demand. Your project should now include these new files:

- Directorysrc/
  - Directorylib/
    - supabase.ts
  - Directorypages/
    - Directoryapi/
      - Directoryauth/
        - **signin.ts**
        - **signout.ts**
        - **register.ts**
  - env.d.ts
- .env
- astro.config.mjs
- package.json

`register.ts` creates a new user in Supabase. It accepts a `POST` request with the an email and password. It then uses the Supabase SDK to create a new user.

 src/pages/api/auth/register.ts

```
// With `output: 'static'` configured:// export const prerender = false;import type { APIRoute } from "astro";import { supabase } from "../../../lib/supabase";
export const POST: APIRoute = async ({ request, redirect }) => {  const formData = await request.formData();  const email = formData.get("email")?.toString();  const password = formData.get("password")?.toString();
  if (!email || !password) {    return new Response("Email and password are required", { status: 400 });  }
  const { error } = await supabase.auth.signUp({    email,    password,  });
  if (error) {    return new Response(error.message, { status: 500 });  }
  return redirect("/signin");};
```

`signin.ts` signs in a user. It accepts a `POST` request with the an email and password. It then uses the Supabase SDK to sign in the user.

 src/pages/api/auth/signin.ts

```
// With `output: 'static'` configured:// export const prerender = false;import type { APIRoute } from "astro";import { supabase } from "../../../lib/supabase";
export const POST: APIRoute = async ({ request, cookies, redirect }) => {  const formData = await request.formData();  const email = formData.get("email")?.toString();  const password = formData.get("password")?.toString();
  if (!email || !password) {    return new Response("Email and password are required", { status: 400 });  }
  const { data, error } = await supabase.auth.signInWithPassword({    email,    password,  });
  if (error) {    return new Response(error.message, { status: 500 });  }
  const { access_token, refresh_token } = data.session;  cookies.set("sb-access-token", access_token, {    path: "/",  });  cookies.set("sb-refresh-token", refresh_token, {    path: "/",  });  return redirect("/dashboard");};
```

`signout.ts` signs out a user. It accepts a `GET` request and removes the user’s access and refresh tokens.

 src/pages/api/auth/signout.ts

```
// With `output: 'static'` configured:// export const prerender = false;import type { APIRoute } from "astro";
export const GET: APIRoute = async ({ cookies, redirect }) => {  cookies.delete("sb-access-token", { path: "/" });  cookies.delete("sb-refresh-token", { path: "/" });  return redirect("/signin");};
```

### Creating auth pages

[Section titled “Creating auth pages”](#creating-auth-pages)

Now that you have created your server endpoints, create the pages that will use them.

- `src/pages/register`: contains a form to register a new user.
- `src/pages/signin`: contains a form to sign in a user.
- `src/pages/dashboard`: contains a page that is only accessible to authenticated users.

Create these pages in the `src/pages` directory. Your project should now include these new files:

- Directorysrc/
  - Directorylib/
    - supabase.ts
  - Directorypages/
    - Directoryapi/
      - Directoryauth/
        - signin.ts
        - signout.ts
        - register.ts
    - **register.astro**
    - **signin.astro**
    - **dashboard.astro**
  - env.d.ts
- .env
- astro.config.mjs
- package.json

`register.astro` contains a form to register a new user. It accepts an email and password and sends a `POST` request to `/api/auth/register`.

 src/pages/register.astro

```
---import Layout from "../layouts/Layout.astro";---
<Layout title="Register">  <h1>Register</h1>  <p>Already have an account? <a href="/signin">Sign in</a></p>  <form action="/api/auth/register" method="post">    <label for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Register</button>  </form></Layout>
```

`signin.astro` contains a form to sign in a user. It accepts an email and password and sends a `POST` request to `/api/auth/signin`. It also checks for the presence of the access and refresh tokens. If they are present, it redirects to the dashboard.

 src/pages/signin.astro

```
---import Layout from "../layouts/Layout.astro";
const { cookies, redirect } = Astro;
const accessToken = cookies.get("sb-access-token");const refreshToken = cookies.get("sb-refresh-token");
if (accessToken && refreshToken) {  return redirect("/dashboard");}---
<Layout title="Sign in">  <h1>Sign in</h1>  <p>New here? <a href="/register">Create an account</a></p>  <form action="/api/auth/signin" method="post">    <label for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Login</button>  </form></Layout>
```

`dashboard.astro` contains a page that is only accessible to authenticated users. It checks for the presence of the access and refresh tokens. If they are not present or are invalid, it redirects to the sign in page.

 src/pages/dashboard.astro

```
---import Layout from "../layouts/Layout.astro";import { supabase } from "../lib/supabase";
const accessToken = Astro.cookies.get("sb-access-token");const refreshToken = Astro.cookies.get("sb-refresh-token");
if (!accessToken || !refreshToken) {  return Astro.redirect("/signin");}
let session;try {  session = await supabase.auth.setSession({    refresh_token: refreshToken.value,    access_token: accessToken.value,  });  if (session.error) {    Astro.cookies.delete("sb-access-token", {      path: "/",    });    Astro.cookies.delete("sb-refresh-token", {      path: "/",    });    return Astro.redirect("/signin");  }} catch (error) {  Astro.cookies.delete("sb-access-token", {    path: "/",  });  Astro.cookies.delete("sb-refresh-token", {    path: "/",  });  return Astro.redirect("/signin");}
const email = session.data.user?.email;---<Layout title="dashboard">  <h1>Welcome {email}</h1>  <p>We are happy to see you here</p>  <form action="/api/auth/signout">    <button type="submit">Sign out</button>  </form></Layout>
```

### Adding OAuth authentication

[Section titled “Adding OAuth authentication”](#adding-oauth-authentication)

To add OAuth authentication to your project, you will need to edit your Supabase client to enable authentication flow with `"pkce"`. You can read more about authentication flows in the [Supabase documentation](https://supabase.com/docs/guides/auth/server-side-rendering#understanding-the-authentication-flow).

 src/lib/supabase.ts

```
import { createClient } from "@supabase/supabase-js";
export const supabase = createClient(  import.meta.env.SUPABASE_URL,  import.meta.env.SUPABASE_ANON_KEY,  {    auth: {      flowType: "pkce",    },  },);
```

Next, in the Supabase dashboard, enable the OAuth provider you would like to use. You can find the list of supported providers in the **Authentication > Providers** tab of your Supabase project.

The following example uses GitHub as the OAuth provider. To connect your project to GitHub, follow the steps in the [Supabase documentation](https://supabase.com/docs/guides/auth/social-login/auth-github).

Then, create a new server endpoint to handle the OAuth callback at `src/pages/api/auth/callback.ts`. This endpoint will be used to exchange the OAuth code for an access and refresh token.

 src/pages/api/auth/callback.ts

```
import type { APIRoute } from "astro";import { supabase } from "../../../lib/supabase";
export const GET: APIRoute = async ({ url, cookies, redirect }) => {  const authCode = url.searchParams.get("code");
  if (!authCode) {    return new Response("No code provided", { status: 400 });  }
  const { data, error } = await supabase.auth.exchangeCodeForSession(authCode);
  if (error) {    return new Response(error.message, { status: 500 });  }
  const { access_token, refresh_token } = data.session;
  cookies.set("sb-access-token", access_token, {    path: "/",  });  cookies.set("sb-refresh-token", refresh_token, {    path: "/",  });
  return redirect("/dashboard");};
```

Next, edit the sign in page to include a new button to sign in with the OAuth provider. This button should send a `POST` request to `/api/auth/signin` with the `provider` set to the name of the OAuth provider.

 src/pages/signin.astro

```
---import Layout from "../layouts/Layout.astro";
const { cookies, redirect } = Astro;
const accessToken = cookies.get("sb-access-token");const refreshToken = cookies.get("sb-refresh-token");
if (accessToken && refreshToken) {  return redirect("/dashboard");}---
<Layout title="Sign in">  <h1>Sign in</h1>  <p>New here? <a href="/register">Create an account</a></p>  <form action="/api/auth/signin" method="post">    <label for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Login</button>    <button value="github" name="provider" type="submit">Sign in with GitHub</button>  </form></Layout>
```

Finally, edit the sign in server endpoint to handle the OAuth provider. If the `provider` is present, it will redirect to the OAuth provider. Otherwise, it will sign in the user with the email and password.

 src/pages/api/auth/signin.ts

```
import type { APIRoute } from "astro";import { supabase } from "../../../lib/supabase";import type { Provider } from "@supabase/supabase-js";
export const POST: APIRoute = async ({ request, cookies, redirect }) => {  const formData = await request.formData();  const email = formData.get("email")?.toString();  const password = formData.get("password")?.toString();  const provider = formData.get("provider")?.toString();
  const validProviders = ["google", "github", "discord"];
  if (provider && validProviders.includes(provider)) {    const { data, error } = await supabase.auth.signInWithOAuth({      provider: provider as Provider,      options: {        redirectTo: "http://localhost:4321/api/auth/callback"      },    });
    if (error) {      return new Response(error.message, { status: 500 });    }
    return redirect(data.url);  }
  if (!email || !password) {    return new Response("Email and password are required", { status: 400 });  }
  const { data, error } = await supabase.auth.signInWithPassword({    email,    password,  });
  if (error) {    return new Response(error.message, { status: 500 });  }
  const { access_token, refresh_token } = data.session;  cookies.set("sb-access-token", access_token, {    path: "/",  });  cookies.set("sb-refresh-token", refresh_token, {    path: "/",  });  return redirect("/dashboard");};
```

After creating the OAuth callback endpoint and editing the sign in page and server endpoint, your project should have the following file structure:

- Directorysrc/
  - Directorylib/
    - supabase.ts
  - Directorypages/
    - Directoryapi/
      - Directoryauth/
        - signin.ts
        - signout.ts
        - register.ts
        - callback.ts
    - register.astro
    - signin.astro
    - dashboard.astro
  - env.d.ts
- .env
- astro.config.mjs
- package.json

## Community Resources

[Section titled “Community Resources”](#community-resources)

- [Getting into the holiday spirit with Astro, React, and Supabase](https://www.aleksandra.codes/astro-supabase)
- [Astro and Supabase auth demo](https://github.com/kevinzunigacuellar/astro-supabase)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Turso & Astro

> Build locally with a SQLite file and deploy globally using Turso.

# Turso & Astro

[Turso](https://turso.tech) is a distributed database built on libSQL, a fork of SQLite. It is optimized for low query latency, making it suitable for global applications.

## Initializing Turso in Astro

[Section titled “Initializing Turso in Astro”](#initializing-turso-in-astro)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- The [Turso CLI](https://docs.turso.tech/cli/introduction) installed and signed in
- A [Turso](https://turso.tech) Database with schema
- Your Database URL
- An Access Token

### Configure environment variables

[Section titled “Configure environment variables”](#configure-environment-variables)

Obtain your database URL using the following command:

 Terminal window

```
turso db show <database-name> --url
```

Create an auth token for the database:

 Terminal window

```
turso db tokens create <database-name>
```

Add the output from both commands above into your `.env` file at the root of your project. If this file does not exist, create one.

 .env

```
TURSO_DATABASE_URL=libsql://...TURSO_AUTH_TOKEN=
```

### Install LibSQL Client

[Section titled “Install LibSQL Client”](#install-libsql-client)

Install the `@libsql/client` to connect Turso to Astro:

- [npm](#tab-panel-2744)
- [pnpm](#tab-panel-2745)
- [Yarn](#tab-panel-2746)

   Terminal window

```
npm install @libsql/client
```

   Terminal window

```
pnpm add @libsql/client
```

   Terminal window

```
yarn add @libsql/client
```

### Initialize a new client

[Section titled “Initialize a new client”](#initialize-a-new-client)

Create a file `turso.ts` in the `src` folder and invoke `createClient`, passing it `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`:

 src/turso.ts

```
import { createClient } from "@libsql/client/web";
export const turso = createClient({  url: import.meta.env.TURSO_DATABASE_URL,  authToken: import.meta.env.TURSO_AUTH_TOKEN,});
```

## Querying your database

[Section titled “Querying your database”](#querying-your-database)

To access information from your database, import `turso` and [execute a SQL query](https://docs.turso.tech/sdk/ts/reference#simple-query) inside any `.astro` component.

The following example fetches all `posts` from your table, then displays a list of titles in a `<BlogIndex />` component:

 src/components/BlogIndex.astro

```
---import { turso } from '../turso'
const { rows } = await turso.execute('SELECT * FROM posts')---
<ul>  {rows.map((post) => (    <li>{post.title}</li>  ))}</ul>
```

### SQL Placeholders

[Section titled “SQL Placeholders”](#sql-placeholders)

The `execute()` method can take [an object to pass variables to the SQL statement](https://docs.turso.tech/sdk/ts/reference#placeholders), such as `slug`, or pagination.

The following example fetches a single entry from the `posts` table `WHERE` the `slug` is the retrieved value from `Astro.params`, then displays the title of the post.

 src/pages/index.astro

```
---import { turso } from '../turso'
const { slug } = Astro.params
const { rows } = await turso.execute({  sql: 'SELECT * FROM posts WHERE slug = ?',  args: [slug!]})---
<h1>{rows[0].title}</h1>
```

## Turso Resources

[Section titled “Turso Resources”](#turso-resources)

- [Turso Docs](https://docs.turso.tech)
- [Turso on GitHub](https://github.com/tursodatabase)
- [Using Turso to serve a Server-side Rendered Astro blog’s content](https://blog.turso.tech/using-turso-to-serve-a-server-side-rendered-astro-blogs-content-58caa6188bd5)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Xata & Astro

> Add a serverless database with full-text search to your project with Xata

# Xata & Astro

[Xata](https://xata.io) is a **Serverless Data Platform** that combines the features of a relational database, a search engine, and an analytics engine by exposing a single consistent REST API.

## Adding a database with Xata

[Section titled “Adding a database with Xata”](#adding-a-database-with-xata)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- A [Xata](https://app.xata.io/signin) account with a created database. (You can use the sample database from the Web UI.)
- An Access Token (`XATA_API_KEY`).
- Your Database URL.

After you update and initialize the [Xata CLI](https://xata.io/docs/getting-started/installation), you will have your API token in your `.env` file and database URL defined.

By the end of the setup, you should have:

 .env

```
XATA_API_KEY=hash_key
# Xata branch that will be used# if there's not a xata branch with# the same name as your git branchXATA_BRANCH=main
```

And the `databaseURL` defined:

 .xatarc

```
{  "databaseUrl": "https://your-database-url"}
```

### Environment configuration

[Section titled “Environment configuration”](#environment-configuration)

To have IntelliSense and type safety for your environment variables, edit or create the file `env.d.ts` in your `src/` directory:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly XATA_API_KEY: string;  readonly XATA_BRANCH?: string;}
interface ImportMeta {  readonly env: ImportMetaEnv;}
```

Using the code generation from the Xata CLI and choosing the TypeScript option, generated an instance of the SDK for you, with types tailored to your database schema. Additionally, `@xata.io/client` was added to your `package.json`.

Your Xata environment variables and database url were automatically pulled by the SDK instance, so there’s no more setup work needed.

Now, your project should have the following structure:

- Directorysrc/
  - **xata.ts**
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json
- **.xatarc**

## Create your queries

[Section titled “Create your queries”](#create-your-queries)

To query your posts, import and use `XataClient` class in a `.astro` file. The example below queries the first 50 posts from Xata’s Sample Blog Database.

 src/pages/blog/index.astro

```
---import { XataClient } from '../../xata';
const xata = new XataClient({  apiKey: import.meta.env.XATA_API_KEY,  branch: import.meta.env.XATA_BRANCH});
const { records } = await xata.db.Posts.getPaginated({  pagination: {    size: 50  }})---
<ul>  {records.map((post) => (    <li>{post.title}</li>  ))}</ul>
```

It’s important to note the SDK needs to be regenerated every time your schema changes. So, avoid making changes to the generated files the Xata CLI creates because once schema updates, your changes will be overwritten.

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [Xata Astro Starter](https://github.com/xataio/examples/tree/main/apps/getting-started-astro)
- [Xata Docs: Quick Start Guide](https://xata.io/docs/getting-started/quickstart-astro)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Use a backend service with Astro

> How to use a backend service to add authentication, storage and data

# Use a backend service with Astro

**Ready to add features like authentication, monitoring, storage, or data to your Astro project?** Follow one of our guides to integrate a backend service.

## Backend service guides

[Section titled “Backend service guides”](#backend-service-guides)

Note that many of these pages are **stubs**: they’re collections of resources waiting for your contribution!

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

## What is a backend service?

[Section titled “What is a backend service?”](#what-is-a-backend-service)

A backend service is a cloud-based system that helps you build and manage your backend infrastructure. It provides a set of tools and services for managing databases, user authentication, and other server-side functionality. This enables you to focus on building your applications without having to worry about managing the underlying infrastructure.

## Why would I use a backend service?

[Section titled “Why would I use a backend service?”](#why-would-i-use-a-backend-service)

You might want to consider a backend service if your project has complex server-side needs, for example:

- user sign-ups and authentication
- persistent data storage
- user-uploaded asset storage
- API generation
- realtime communication
- application monitoring

 Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Building Astro sites with AI tools

> Resources and tips for building Astro sites with AI assistance

# Building Astro sites with AI tools

AI-powered editors and agentic coding tools generally have good knowledge of Astro’s core APIs and concepts. However, some may use older APIs and may not be aware of newer features or recent changes to the framework.

This guide covers how to enhance AI tools with up-to-date Astro knowledge and provides best practices for building Astro sites with AI assistance.

## Context files

[Section titled “Context files”](#context-files)

Astro provides [llms.txt](https://docs.astro.build/llms.txt) and [llms-full.txt](https://docs.astro.build/llms-full.txt) files that contains the full docs content in a format optimized for AI consumption. These are static files of the Astro Docs content in a streamlined Markdown format. Some AI tools can auto-discover these files if you provide `https://docs.astro.build` as a docs source.

While these files provide a minimal, easy-to-parse version of Astro’s documentation, they are large files that will use a lot of tokens if used directly in context and will need to be updated regularly to stay current. They are best used as a fallback when the AI tool does not have access to the latest documentation in other ways. [The MCP server](#astro-docs-mcp-server) provides more efficient access to the full documentation with real-time search capabilities, making it the preferred option when available.

## Astro Docs MCP Server

[Section titled “Astro Docs MCP Server”](#astro-docs-mcp-server)

You can ensure your AI tools have current Astro knowledge through the Astro Docs MCP (Model Context Protocol) server. This provides real-time access to the latest documentation, helping AI tools avoid outdated recommendations and ensuring they understand current best practices.

Unlike AI models trained on static data, the MCP server provides access to the latest Astro documentation. The server is free, open-source, and runs remotely with nothing to install locally.

The Astro Docs MCP server uses the [kapa.ai](https://www.kapa.ai/) API to maintain an up-to-date index of the Astro documentation.

### Server Details

[Section titled “Server Details”](#server-details)

- **Name**: Astro Docs
- **URL**: `https://mcp.docs.astro.build/mcp`
- **Transport**: Streamable HTTP

### Installation

[Section titled “Installation”](#installation)

The setup process varies depending on your AI development tool. You may see some tools refer to MCP servers as connectors, adapters, extensions, or plugins.

#### Manual setup

[Section titled “Manual setup”](#manual-setup)

Many tools support a common JSON configuration format for MCP servers. If there are not specific instructions for your chosen tool, you may be able to add the Astro Docs MCP server by including the following configuration in your tool’s MCP settings:

- [Streamable HTTP](#tab-panel-1822)
- [Local Proxy](#tab-panel-1823)

   mcp.json

```
{  "mcpServers": {    "Astro docs": {      "type": "http",      "url": "https://mcp.docs.astro.build/mcp"    }  }}
```

  mcp.json

```
{  "mcpServers": {    "Astro docs": {      "type": "stdio",      "command": "npx",      "args": ["-y", "mcp-remote", "https://mcp.docs.astro.build/mcp"]    }  }}
```

#### Claude Code CLI

[Section titled “Claude Code CLI”](#claude-code-cli)

[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) is an agentic coding tool that runs on the command line. Enabling the Astro Docs MCP server allows it to access the latest documentation while generating Astro code.

Install using the terminal command:

 Terminal window

```
claude mcp add --transport http astro-docs https://mcp.docs.astro.build/mcp
```

[More info on using MCP servers with Claude Code](https://docs.anthropic.com/en/docs/claude-code/mcp)

#### Claude Code GitHub Action

[Section titled “Claude Code GitHub Action”](#claude-code-github-action)

Claude Code also provides a GitHub Action that can be used to run commands in response to GitHub events. Enabling the Astro Docs MCP server allows it to access the latest documentation while answering questions in comments or generating Astro code.

You can configure it to use the Astro Docs MCP server for documentation access by adding the following to the workflow file:

 .github/workflows/claude.yml

```
# ...rest of your workflow configuration- uses: anthropics/claude-code-action@beta  with:    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}    mcp_config: |      {        "mcpServers": {          "astro-docs": {            "type": "http",            "url": "https://mcp.docs.astro.build/mcp"          }        }      }    allowed_tools: "mcp__astro-docs__search_astro_docs"
```

[More info on using MCP servers with the Claude Code GitHub Action](https://github.com/anthropics/claude-code-action?tab=readme-ov-file#using-custom-mcp-configuration)

#### Cursor

[Section titled “Cursor”](#cursor)

[Cursor](https://cursor.com) is an AI code editor. Adding the Astro Docs MCP server allows Cursor to access the latest Astro documentation while performing development tasks.

Install by clicking the button below:

 [Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=Astro%20docs&config=eyJ1cmwiOiJodHRwczovL21jcC5kb2NzLmFzdHJvLmJ1aWxkL21jcCJ9)

[More info on using MCP servers with Cursor](https://docs.cursor.com/context/mcp)

#### Visual Studio Code

[Section titled “Visual Studio Code”](#visual-studio-code)

[Visual Studio Code](https://code.visualstudio.com) supports MCP servers when using Copilot Chat. Adding the Astro Docs MCP server allows VS Code to access the latest Astro documentation when answering questions or performing coding tasks.

Install by clicking the button below:

 [Add to VS Code](vscode:mcp/install?%7B%22name%22%3A%22Astro%20docs%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.docs.astro.build%2Fmcp%22%7D)

[More info on using MCP servers with VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server)

#### Warp

[Section titled “Warp”](#warp)

[Warp](https://warp.dev) (formerly Warp Terminal) is an agent development environment built for coding with multiple AI agents. Adding the Astro Docs MCP server allows Warp to access the latest Astro documentation when answering questions or performing coding tasks.

1. Open your Warp settings and go to AI > MCP Servers > Manage MCP Servers.
2. Click “Add”.
3. Enter the following configuration. You can optionally configure the Astro MCP server to activate on startup using the `start_on_launch` flag:
  MCP Configuration
  ```
  {  "mcpServers": {    "Astro docs": {      "command": "npx",      "args": ["-y", "mcp-remote", "https://mcp.docs.astro.build/mcp"],      "env": {},      "working_directory": null,      "start_on_launch": true    }  }}
  ```
4. Click “Save”.

[More info on using MCP servers with Warp](https://docs.warp.dev/knowledge-and-collaboration/mcp)

#### Claude.ai / Claude Desktop

[Section titled “Claude.ai / Claude Desktop”](#claudeai--claude-desktop)

[Claude.ai](https://claude.ai) is a general-purpose AI assistant. Adding the Astro Docs MCP server allows it to access the latest documentation when answering Astro questions or generating Astro code.

1. Navigate to the [Claude.ai connector settings](https://claude.ai/settings/connectors).
2. Click “Add custom connector”. You may need to scroll down to find this option.
3. Enter the server URL: `https://mcp.docs.astro.build/mcp`.
4. Set the name to “Astro docs”.

[More info on using MCP servers with Claude.ai](https://support.anthropic.com/en/articles/10168395-setting-up-integrations-on-claude-ai#h_cda40ecb32)

#### Windsurf

[Section titled “Windsurf”](#windsurf)

[Windsurf](https://windsurf.com/) is an AI-powered agentic coding tool, available as editor plugins or a standalone editor. It can use the Astro Docs MCP server to access documentation while performing coding tasks.

Windsurf doesn’t support streaming HTTP, so it requires a local proxy configuration:

1. Open `~/.codeium/windsurf/mcp_config.json` in your editor.
2. Add the following configuration to your Windsurf MCP settings:
   MCP Configuration
  ```
  {  "mcpServers": {    "Astro docs": {      "command": "npx",      "args": ["-y", "mcp-remote", "https://mcp.docs.astro.build/mcp"]    }  }}
  ```
3. Save the configuration and restart Windsurf.

[More info on using MCP servers with Windsurf](https://docs.windsurf.com/windsurf/cascade/mcp#mcp-config-json)

#### Gemini CLI

[Section titled “Gemini CLI”](#gemini-cli)

Gemini CLI is a command-line AI coding tool that can use the Astro Docs MCP server to access documentation while generating Astro code.

You can configure MCP servers at the global level in the `~/.gemini/settings.json` file, or in a `.gemini/settings.json` file in a project root.

 .gemini/settings.json

```
{  "mcpServers": {    "Astro docs": {      "httpUrl": "https://mcp.docs.astro.build/mcp",    }  }}
```

[More info on using MCP servers with Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)

#### Google Antigravity

[Section titled “Google Antigravity”](#google-antigravity)

[Google Antigravity](https://antigravity.google/) is an agentic development platform.

1. Open `~/.gemini/antigravity/mcp_config.json` by following the [Connecting Custom MCP Servers guide](https://antigravity.google/docs/mcp#connecting-custom-mcp-servers).
2. Add the following configuration to `mcp_config.json`:
  mcp_config.json
  ```
  {  "mcpServers": {    "astro-docs": {      "serverUrl": "https://mcp.docs.astro.build/mcp"    }  }}
  ```
3. Save the file and click “Refresh” in the “Manage MCPs” tab.

#### Zed

[Section titled “Zed”](#zed)

[Zed](https://zed.dev) supports MCP servers when using its AI capabilities. It can use the Astro Docs MCP server to access documentation while performing coding tasks.

Zed doesn’t support streaming HTTP, so it requires a local proxy configuration:

1. Open `~/.config/zed/settings.json` in your editor.
2. Add the following configuration to your Zed MCP settings:
   MCP Configuration
  ```
  {  "context_servers": {    "Astro docs": {      "command": "npx",      "args": ["-y", "mcp-remote", "https://mcp.docs.astro.build/mcp"]    }  }}
  ```
3. Save the configuration.

[More info on using MCP servers with Zed](https://zed.dev/docs/ai/mcp)

#### ChatGPT

[Section titled “ChatGPT”](#chatgpt)

Refer to the [OpenAI MCP documentation](https://platform.openai.com/docs/mcp#test-and-connect-your-mcp-server) for specific setup instructions.

#### Raycast

[Section titled “Raycast”](#raycast)

[Raycast](https://www.raycast.com/) can connect to MCP servers to enhance its AI capabilities. AI features such as MCP require a [Raycast Pro](https://www.raycast.com/pro) account, so ensure you have upgraded before trying to install. Adding the Astro Docs MCP server allows Raycast to access the latest Astro documentation while answering questions.

Install by clicking the button below:

 [Add to Raycast](raycast://mcp/install?%7B%22name%22%3A%22Astro%20docs%22%2C%22type%22%3A%22stdio%22%2C%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%20%22mcp-remote%22%2C%20%22https%3A%2F%2Fmcp.docs.astro.build%2Fmcp%22%5D%7D)

[More info on using MCP servers with Raycast](https://manual.raycast.com/model-context-protocol)

#### Opencode AI

[Section titled “Opencode AI”](#opencode-ai)

[Opencode AI](https://opencode.ai/) is an open-source, terminal-based AI coding tool that can use the Astro Docs MCP server to access documentation while generating Astro code.

You can configure MCP servers in your Opencode configuration file, typically named `opencode.json`, located in your project root or your global configuration directory (e.g. `~/.config/opencode/opencode.json`).

 MCP Configuration

```
{  "$schema": "https://opencode.ai/config.json",  "mcp": {    "Astro docs": {      "type": "remote",      "url": "https://mcp.docs.astro.build/mcp",      "enabled": true    }  }}
```

[More info on using Opencode AI](https://opencode.ai/)

#### GitHub Copilot Coding Agent

[Section titled “GitHub Copilot Coding Agent”](#github-copilot-coding-agent)

[GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent) can be used as a coding agent powered by GitHub Actions. Enabling the Astro Docs MCP server allows it to access the latest Astro documentation when answering questions or performing coding tasks.

You can configure it to use the Astro Docs MCP server for documentation access by adding the following to your repository’s Copilot coding agent settings available at `https://github.com/<your-org>/<your-repo>/settings/copilot/coding_agent`:

 MCP Configuration

```
{  "mcpServers": {    "astro-docs": {      "type": "http",      "url": "https://mcp.docs.astro.build/mcp",      "tools": ["mcp__astro-docs__search_astro_docs"]    }  }}
```

Learn more about [extending GitHub Copilot coding agent with MCP servers](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp).

### Usage

[Section titled “Usage”](#usage)

Once configured, you can ask your AI tool questions about Astro, and it will retrieve information directly from the latest docs. Coding agents will be able to consult the latest documentation when performing coding tasks, and chatbots will be able to accurately answer questions about Astro features, APIs, and best practices.

### Troubleshooting

[Section titled “Troubleshooting”](#troubleshooting)

If you encounter issues:

- Verify that your tool supports streamable HTTP transport.
- Check that the server URL is correct: `https://mcp.docs.astro.build/mcp`.
- Ensure your tool has proper internet access.
- Consult your specific tool’s MCP integration documentation.

If you are still having problems, open an issue in the [Astro Docs MCP Server repository](https://github.com/withastro/docs-mcp/issues).

## Discord AI Support

[Section titled “Discord AI Support”](#discord-ai-support)

The same technology that powers Astro’s MCP server is also available as a chatbot in the [Astro Discord](https://astro.build/chat) for self-serve support. Visit the `#support-ai` channel to ask questions about Astro or your project code in natural language. Your conversation is automatically threaded, and you can ask an unlimited number of follow-up questions.

**Conversations with the chatbot are public, and are subject to the same server rules for language and behavior as the rest of our channels**, but they are not actively visited by our volunteer support members. For assistance from the community, please create a thread in our regular `#support` channel.

## Tips for AI-Powered Astro Development

[Section titled “Tips for AI-Powered Astro Development”](#tips-for-ai-powered-astro-development)

- **Start with templates**: Rather than building from scratch, ask AI tools to start with an existing [Astro template](https://astro.build/themes/) or use `npm create astro@latest` with a template option.
- **Useastro addfor integrations**: Ask AI tools to use `astro add` for official integrations (e.g. `astro add tailwind`, `astro add react`). For other packages, install using the command for your preferred package manager rather than editing `package.json` directly.
- **Verify current APIs**: AI tools may use outdated patterns. Ask them to check the latest documentation, especially for newer features like sessions and actions. This is also important for features that have seen significant changes since their initial launch, such as content collections, or previously experimental features that may no longer be experimental.
- **Use project rules**: If your AI tool supports it, set up project rules to enforce best practices and coding standards, such as the ones listed above.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)
