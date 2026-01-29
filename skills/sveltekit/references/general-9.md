# Frequently asked questions

# Frequently asked questions

> Frequently asked questions • SvelteKit documentation

## Other resources

Please see [the Svelte FAQ](https://kit.svelte.dev/svelte/faq) and [vite-plugin-svelteFAQ](https://github.com/sveltejs/vite-plugin-svelte/blob/main/docs/faq.md) as well for the answers to questions deriving from those libraries.

## What can I make with SvelteKit?

See [the documentation regarding project types](https://kit.svelte.dev/docs/project-types) for more details.

## How do I include details from package.json in my application?

If you’d like to include your application’s version number or other information from `package.json` in your application, you can load JSON like so:

 svelte.config

```
import import pkgpkg from './package.json' with { type: 'json' };
```

## How do I fix the error I’m getting trying to include a package?

Most issues related to including a library are due to incorrect packaging. You can check if a library’s packaging is compatible with Node.js by entering it into [the publint website](https://publint.dev/).

Here are a few things to keep in mind when checking if a library is packaged correctly:

- `exports` takes precedence over the other entry point fields such as `main` and `module`. Adding an `exports` field may not be backwards-compatible as it prevents deep imports.
- ESM files should end with `.mjs` unless `"type": "module"` is set in which any case CommonJS files should end with `.cjs`.
- `main` should be defined if `exports` is not. It should be either a CommonJS or ESM file and adhere to the previous bullet. If a `module` field is defined, it should refer to an ESM file.
- Svelte components should be distributed as uncompiled `.svelte` files with any JS in the package written as ESM only. Custom script and style languages, like TypeScript and SCSS, should be preprocessed as vanilla JS and CSS respectively. We recommend using [svelte-package](https://kit.svelte.dev/docs/packaging) for packaging Svelte libraries, which will do this for you.

Libraries work best in the browser with Vite when they distribute an ESM version, especially if they are dependencies of a Svelte component library. You may wish to suggest to library authors that they provide an ESM version. However, CommonJS (CJS) dependencies should work as well since, by default, [vite-plugin-sveltewill ask Vite to pre-bundle them](https://github.com/sveltejs/vite-plugin-svelte/blob/main/docs/faq.md#what-is-going-on-with-vite-and-pre-bundling-dependencies) using `esbuild` to convert them to ESM.

If you are still encountering issues we recommend searching both [the Vite issue tracker](https://github.com/vitejs/vite/issues) and the issue tracker of the library in question. Sometimes issues can be worked around by fiddling with the [optimizeDeps](https://vitejs.dev/config/#dep-optimization-options) or [ssr](https://vitejs.dev/config/#ssr-options) config values though we recommend this as only a short-term workaround in favor of fixing the library in question.

## How do I use the view transitions API?

While SvelteKit does not have any specific integration with [view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/), you can call `document.startViewTransition` in [onNavigate](https://kit.svelte.dev/docs/$app-navigation#onNavigate) to trigger a view transition on every client-side navigation.

```
import { function onNavigate(callback: (navigation: import("@sveltejs/kit").OnNavigate) => MaybePromise<void | (() => void)>): voidA lifecycle function that runs the supplied callback immediately before we navigate to a new URL except during full-page navigations.
If you return a Promise, SvelteKit will wait for it to resolve before completing the navigation. This allows you to — for example — use document.startViewTransition. Avoid promises that are slow to resolve, since navigation will appear stalled to the user.
If a function (or a Promise that resolves to a function) is returned from the callback, it will be called once the DOM has updated.
onNavigate must be called during a component initialization. It remains active as long as the component is mounted.
onNavigate } from '$app/navigation';

function onNavigate(callback: (navigation: import("@sveltejs/kit").OnNavigate) => MaybePromise<void | (() => void)>): voidA lifecycle function that runs the supplied callback immediately before we navigate to a new URL except during full-page navigations.
If you return a Promise, SvelteKit will wait for it to resolve before completing the navigation. This allows you to — for example — use document.startViewTransition. Avoid promises that are slow to resolve, since navigation will appear stalled to the user.
If a function (or a Promise that resolves to a function) is returned from the callback, it will be called once the DOM has updated.
onNavigate must be called during a component initialization. It remains active as long as the component is mounted.
onNavigate((navigation: OnNavigatenavigation) => {
	if (!var document: DocumentMDN Reference
document.Document.startViewTransition(callbackOptions?: ViewTransitionUpdateCallback): ViewTransitionMDN Reference
startViewTransition) return;

	return new var Promise: PromiseConstructor
new <void | (() => void)>(executor: (resolve: (value: void | (() => void) | PromiseLike<void | (() => void)>) => void, reject: (reason?: any) => void) => void) => Promise<void | (() => void)>Creates a new Promise.
@paramexecutor A callback used to initialize the promise. This callback is passed two arguments:
a resolve callback used to resolve the promise with a value or the result of another promise,
and a reject callback used to reject the promise with a provided reason or error.Promise((resolve: (value: void | (() => void) | PromiseLike<void | (() => void)>) => voidresolve) => {
		var document: DocumentMDN Reference
document.Document.startViewTransition(callbackOptions?: ViewTransitionUpdateCallback): ViewTransitionMDN Reference
startViewTransition(async () => {
			resolve: (value: void | (() => void) | PromiseLike<void | (() => void)>) => voidresolve();
			await navigation: OnNavigatenavigation.NavigationBase.complete: Promise<void>A promise that resolves once the navigation is complete, and rejects if the navigation
fails or is aborted. In the case of a willUnload navigation, the promise will never resolve
complete;
		});
	});
});
```

For more, see [“Unlocking view transitions”](https://kit.svelte.dev/blog/view-transitions) on the Svelte blog.

## How do I set up a database?

Put the code to query your database in a [server route](https://kit.svelte.dev/docs/routing#server) - don’t query the database in .svelte files. You can create a `db.js` or similar that sets up a connection immediately and makes the client accessible throughout the app as a singleton. You can execute any one-time setup code in `hooks.server.js` and import your database helpers into any endpoint that needs them.

You can use [the Svelte CLI](https://kit.svelte.dev/docs/cli/overview) to automatically set up database integrations.

## How do I use a client-side library accessing document or window?

If you need access to the `document` or `window` variables or otherwise need code to run only on the client-side you can wrap it in a `browser` check:

```
import { const browser: booleantrue if the app is running in the browser.
browser } from '$app/environment';

if (const browser: booleantrue if the app is running in the browser.
browser) {
	// client-only code here
}
```

You can also run code in `onMount` if you’d like to run it after the component has been first rendered to the DOM:

```
import { function onMount<T>(fn: () => NotFunction<T> | Promise<NotFunction<T>> | (() => any)): voidonMount, like $effect, schedules a function to run as soon as the component has been mounted to the DOM.
Unlike $effect, the provided function only runs once.
It must be called during the component’s initialisation (but doesn’t need to live inside the component;
it can be called from an external module). If a function is returned synchronously from onMount,
it will be called when the component is unmounted.
onMount functions do not run during server-side rendering.
onMount } from 'svelte';

onMount<void>(fn: () => void | (() => any) | Promise<void>): voidonMount, like $effect, schedules a function to run as soon as the component has been mounted to the DOM.
Unlike $effect, the provided function only runs once.
It must be called during the component’s initialisation (but doesn’t need to live inside the component;
it can be called from an external module). If a function is returned synchronously from onMount,
it will be called when the component is unmounted.
onMount functions do not run during server-side rendering.
onMount(async () => {
	const { const method: anymethod } = await import('some-browser-only-library');
	const method: anymethod('hello world');
});
```

If the library you’d like to use is side-effect free you can also statically import it and it will be tree-shaken out in the server-side build where `onMount` will be automatically replaced with a no-op:

```
import { function onMount<T>(fn: () => NotFunction<T> | Promise<NotFunction<T>> | (() => any)): voidonMount, like $effect, schedules a function to run as soon as the component has been mounted to the DOM.
Unlike $effect, the provided function only runs once.
It must be called during the component’s initialisation (but doesn’t need to live inside the component;
it can be called from an external module). If a function is returned synchronously from onMount,
it will be called when the component is unmounted.
onMount functions do not run during server-side rendering.
onMount } from 'svelte';
import { module "some-browser-only-library"method } from 'some-browser-only-library';

onMount<void>(fn: () => void | (() => any) | Promise<void>): voidonMount, like $effect, schedules a function to run as soon as the component has been mounted to the DOM.
Unlike $effect, the provided function only runs once.
It must be called during the component’s initialisation (but doesn’t need to live inside the component;
it can be called from an external module). If a function is returned synchronously from onMount,
it will be called when the component is unmounted.
onMount functions do not run during server-side rendering.
onMount(() => {
	module "some-browser-only-library"method('hello world');
});
```

Finally, you may also consider using an `{#await}` block:

 index

```
<script>
	import { browser } from '$app/environment';

	const ComponentConstructor = browser ?
		import('some-browser-only-library').then((module) => module.Component) :
		new Promise(() => {});
</script>

{#await ComponentConstructor}
	<p>Loading...</p>
{:then component}
	<svelte:component this={component} />
{:catch error}
	<p>Something went wrong: {error.message}</p>
{/await}
```

```
<script lang="ts">
	import { browser } from '$app/environment';

	const ComponentConstructor = browser ?
		import('some-browser-only-library').then((module) => module.Component) :
		new Promise(() => {});
</script>

{#await ComponentConstructor}
	<p>Loading...</p>
{:then component}
	<svelte:component this={component} />
{:catch error}
	<p>Something went wrong: {error.message}</p>
{/await}
```

## How do I use a different backend API server?

You can use [event.fetch](https://kit.svelte.dev/docs/load#Making-fetch-requests) to request data from an external API server, but be aware that you would need to deal with [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), which will result in complications such as generally requiring requests to be preflighted resulting in higher latency. Requests to a separate subdomain may also increase latency due to an additional DNS lookup, TLS setup, etc. If you wish to use this method, you may find [handleFetch](https://kit.svelte.dev/docs/hooks#Server-hooks-handleFetch) helpful.

Another approach is to set up a proxy to bypass CORS headaches. In production, you would rewrite a path like `/api` to the API server; for local development, use Vite’s [server.proxy](https://vitejs.dev/config/server-options.html#server-proxy) option.

How to setup rewrites in production will depend on your deployment platform. If rewrites aren’t an option, you could alternatively add an [API route](https://kit.svelte.dev/docs/routing#server):

 src/routes/api/[...path]/+server

```
/** @type {import('./$types').RequestHandler} */
export function function GET({ params, url }: {
    params: any;
    url: any;
}): Promise<Response>@type{import('./$types').RequestHandler}GET({ params: anyparams, url: anyurl }) {
	return function fetch(input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response> (+1 overload)MDN Reference
fetch(`https://example.com/${params: anyparams.path + url: anyurl.search}`);
}
```

```
import type { type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler } from './$types';

export const const GET: RequestHandlerGET: type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler = ({ params: Record<string, any>The parameters of the current route - e.g. for a route like /blog/[slug], a { slug: string } object.
params, url: URLThe requested URL.
url }) => {
	return function fetch(input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response> (+1 overload)MDN Reference
fetch(`https://example.com/${params: Record<string, any>The parameters of the current route - e.g. for a route like /blog/[slug], a { slug: string } object.
params.path + url: URLThe requested URL.
url.URL.search: stringMDN Reference
search}`);
};
```

(Note that you may also need to proxy `POST` / `PATCH` etc requests, and forward `request.headers`, depending on your needs.)

## How do I use middleware?

`adapter-node` builds a middleware that you can use with your own server for production mode. In dev, you can add middleware to Vite by using a Vite plugin. For example:

```
import { module "@sveltejs/kit/vite"sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').Plugin} */
const const myPlugin: Plugin$1<any>@type{import('vite').Plugin}myPlugin = {
	OutputPlugin.name: stringname: 'log-request-middleware',
	Plugin$1<any>.configureServer?: ObjectHook<ServerHook> | undefinedConfigure the vite server. The hook receives the
{@link
ViteDevServer
}
instance. This can also be used to store a reference to the server
for use in other hooks.
The hooks will be called before internal middlewares are applied. A hook
can return a post hook that will be called after internal middlewares
are applied. Hook can be async functions and will be called in series.
configureServer(server: ViteDevServerserver) {
		server: ViteDevServerserver.ViteDevServer.middlewares: Connect.ServerA connect app instance.

Can be used to attach custom middlewares to the dev server.
Can also be used as the handler function of a custom http server
or as a middleware in any connect-style Node.js frameworks

https://github.com/senchalabs/connect#use-middleware
middlewares.Connect.Server.use(fn: Connect.NextHandleFunction): Connect.Server (+3 overloads)Utilize the given middleware handle to the given route,
defaulting to /. This “route” is the mount-point for the
middleware, when given a value other than / the middleware
is only effective when that segment is present in the request’s
pathname.
For example if we were to mount a function at /admin, it would
be invoked on /admin, and /admin/settings, however it would
not be invoked for /, or /posts.
use((req: Connect.IncomingMessagereq, res: ServerResponse<IncomingMessage>res, next: Connect.NextFunctionnext) => {
			var console: ConsoleThe console module provides a simple debugging console that is similar to the
JavaScript console mechanism provided by web browsers.
The module exports two specific components:

A Console class with methods such as console.log(), console.error() and console.warn() that can be used to write to any Node.js stream.
A global console instance configured to write to process.stdout and
process.stderr. The global console can be used without importing the node:console module.

Warning: The global console object’s methods are neither consistently
synchronous like the browser APIs they resemble, nor are they consistently
asynchronous like all other Node.js streams. See the note on process I/O for
more information.
Example using the global console:
console.log('hello world');
// Prints: hello world, to stdout
console.log('hello %s', 'world');
// Prints: hello world, to stdout
console.error(new Error('Whoops, something bad happened'));
// Prints error message and stack trace to stderr:
//   Error: Whoops, something bad happened
//     at [eval]:5:15
//     at Script.runInThisContext (node:vm:132:18)
//     at Object.runInThisContext (node:vm:309:38)
//     at node:internal/process/execution:77:19
//     at [eval]-wrapper:6:22
//     at evalScript (node:internal/process/execution:76:60)
//     at node:internal/main/eval_string:23:3

const name = 'Will Robinson';
console.warn(`Danger ${name}! Danger!`);
// Prints: Danger Will Robinson! Danger!, to stderrExample using the Console class:
const out = getStreamSomehow();
const err = getStreamSomehow();
const myConsole = new console.Console(out, err);

myConsole.log('hello world');
// Prints: hello world, to out
myConsole.log('hello %s', 'world');
// Prints: hello world, to out
myConsole.error(new Error('Whoops, something bad happened'));
// Prints: [Error: Whoops, something bad happened], to err

const name = 'Will Robinson';
myConsole.warn(`Danger ${name}! Danger!`);
// Prints: Danger Will Robinson! Danger!, to err@seesourceconsole.Console.log(message?: any, ...optionalParams: any[]): void (+1 overload)Prints to stdout with newline. Multiple arguments can be passed, with the
first used as the primary message and all additional used as substitution
values similar to printf(3)
(the arguments are all passed to util.format()).
const count = 5;
console.log('count: %d', count);
// Prints: count: 5, to stdout
console.log('count:', count);
// Prints: count: 5, to stdoutSee util.format() for more information.
@sincev0.1.100log(`Got request ${req: Connect.IncomingMessagereq.IncomingMessage.url?: string | undefinedOnly valid for request obtained from
{@link
Server
}
.
Request URL string. This contains only the URL that is present in the actual
HTTP request. Take the following request:
GET /status?name=ryan HTTP/1.1
Accept: text/plainTo parse the URL into its parts:
new URL(`http://${process.env.HOST ?? 'localhost'}${request.url}`);When request.url is '/status?name=ryan' and process.env.HOST is undefined:
$ node
> new URL(`http://${process.env.HOST ?? 'localhost'}${request.url}`);
URL {
  href: 'http://localhost/status?name=ryan',
  origin: 'http://localhost',
  protocol: 'http:',
  username: '',
  password: '',
  host: 'localhost',
  hostname: 'localhost',
  port: '',
  pathname: '/status',
  search: '?name=ryan',
  searchParams: URLSearchParams { 'name' => 'ryan' },
  hash: ''
}Ensure that you set process.env.HOST to the server’s host name, or consider replacing this part entirely. If using req.headers.host, ensure proper
validation is used, as clients may specify a custom Host header.
@sincev0.1.90url}`);
			next: (err?: any) => voidnext();
		});
	}
};

/** @type {import('vite').UserConfig} */
const const config: UserConfig@type{import('vite').UserConfig}config = {
	UserConfig.plugins?: PluginOption[] | undefinedArray of vite plugins to use.
plugins: [const myPlugin: Plugin$1<any>@type{import('vite').Plugin}myPlugin, module "@sveltejs/kit/vite"sveltekit()]
};

export default const config: UserConfig@type{import('vite').UserConfig}config;
```

See [Vite’sconfigureServerdocs](https://vitejs.dev/guide/api-plugin.html#configureserver) for more details including how to control ordering.

## How do I use Yarn?

### Does it work with Yarn 2?

Sort of. The Plug’n'Play feature, aka ‘pnp’, is broken (it deviates from the Node module resolution algorithm, and [doesn’t yet work with native JavaScript modules](https://github.com/yarnpkg/berry/issues/638) which SvelteKit — along with an [increasing number of packages](https://blog.sindresorhus.com/get-ready-for-esm-aa53530b3f77) — uses). You can use `nodeLinker: 'node-modules'` in your [.yarnrc.yml](https://yarnpkg.com/configuration/yarnrc#nodeLinker) file to disable pnp, but it’s probably easier to just use npm or [pnpm](https://pnpm.io/), which is similarly fast and efficient but without the compatibility headaches.

### How do I use with Yarn 3?

Currently ESM Support within the latest Yarn (version 3) is considered [experimental](https://github.com/yarnpkg/berry/pull/2161).

The below seems to work although your results may vary. First create a new application:

```
yarn create svelte myapp
cd myapp
```

And enable Yarn Berry:

```
yarn set version berry
yarn install
```

One of the more interesting features of Yarn Berry is the ability to have a single global cache for packages, instead of having multiple copies for each project on the disk. However, setting `enableGlobalCache` to true causes building to fail, so it is recommended to add the following to the `.yarnrc.yml` file:

```
nodeLinker: node-modules
```

This will cause packages to be downloaded into a local node_modules directory but avoids the above problem and is your best bet for using version 3 of Yarn at this point in time.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/60-appendix/10-faq.md) [[llms.txt](https://kit.svelte.dev/docs/kit/faq/llms.txt)]

 previous next [[SEO](https://kit.svelte.dev/docs/kit/seo)] [[Integrations](https://kit.svelte.dev/docs/kit/integrations)]
