# Not found! and more

# Not found!

[! [[

# Not found!

If you were expecting to find something here, please drop by the [Discord chatroom](https://kit.svelte.dev/chat) and let us know, or raise an issue on [GitHub](https://github.com/sveltejs/svelte.dev/issues). Thanks!

]] ]

---

# Migrating to SvelteKit v2

> Migrating to SvelteKit v2 • SvelteKit documentation

Upgrading from SvelteKit version 1 to version 2 should be mostly seamless. There are a few breaking changes to note, which are listed here. You can use `npx sv migrate sveltekit-2` to migrate some of these changes automatically.

We highly recommend upgrading to the most recent 1.x version before upgrading to 2.0, so that you can take advantage of targeted deprecation warnings. We also recommend [updating to Svelte 4](https://kit.svelte.dev/svelte/v4-migration-guide) first: Later versions of SvelteKit 1.x support it, and SvelteKit 2.0 requires it.

## redirect and error are no longer thrown by you

Previously, you had to `throw` the values returned from `error(...)` and `redirect(...)` yourself. In SvelteKit 2 this is no longer the case — calling the functions is sufficient.

```
import { function error(status: number, body: App.Error): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error } from '@sveltejs/kit'

// ...
throw error(500, 'something went wrong');
function error(status: number, body?: {
    message: string;
} extends App.Error ? App.Error | string | undefined : never): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error(500, 'something went wrong');
```

`svelte-migrate` will do these changes automatically for you.

If the error or redirect is thrown inside a `try {...}` block (hint: don’t do this!), you can distinguish them from unexpected errors using [isHttpError](https://kit.svelte.dev/docs/@sveltejs-kit#isHttpError) and [isRedirect](https://kit.svelte.dev/docs/@sveltejs-kit#isRedirect) imported from `@sveltejs/kit`.

## path is required when setting cookies

When receiving a `Set-Cookie` header that doesn’t specify a `path`, browsers will [set the cookie path](https://www.rfc-editor.org/rfc/rfc6265#section-5.1.4) to the parent of the resource in question. This behaviour isn’t particularly helpful or intuitive, and frequently results in bugs because the developer expected the cookie to apply to the domain as a whole.

As of SvelteKit 2.0, you need to set a `path` when calling `cookies.set(...)`, `cookies.delete(...)` or `cookies.serialize(...)` so that there’s no ambiguity. Most of the time, you probably want to use `path: '/'`, but you can set it to whatever you like, including relative paths — `''` means ‘the current path’, `'.'` means ‘the current directory’.

```
/** @type {import('./$types').PageServerLoad} */
export function function load({ cookies }: {
    cookies: any;
}): {
    response: any;
}@type{import('./$types').PageServerLoad}load({ cookies: anycookies }) {
	cookies: anycookies.set(const name: void@deprecatedname, value, { path: stringpath: '/' });
	return { response: anyresponse }
}
```

`svelte-migrate` will add comments highlighting the locations that need to be adjusted.

## Top-level promises are no longer awaited

In SvelteKit version 1, if the top-level properties of the object returned from a `load` function were promises, they were automatically awaited. With the introduction of [streaming](https://kit.svelte.dev/blog/streaming-snapshots-sveltekit) this behavior became a bit awkward as it forces you to nest your streamed data one level deep.

As of version 2, SvelteKit no longer differentiates between top-level and non-top-level promises. To get back the blocking behavior, use `await` (with `Promise.all` to prevent waterfalls, where appropriate):

```
// If you have a single promise
/** @type {import('./$types').PageServerLoad} */
export async function function load(event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>): MaybePromise<void | Record<string, any>>@type{import('./$types').PageServerLoad}load({ fetch: {
    (input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
    (input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response>;
}fetch is equivalent to the native fetch web API, with a few additional features:

It can be used to make credentialed requests on the server, as it inherits the cookie and authorization headers for the page request.
It can make relative requests on the server (ordinarily, fetch requires a URL with an origin when used in a server context).
Internal requests (e.g. for +server.js routes) go directly to the handler function when running on the server, without the overhead of an HTTP call.
During server-side rendering, the response will be captured and inlined into the rendered HTML by hooking into the text and json methods of the Response object. Note that headers will not be serialized, unless explicitly included via filterSerializedResponseHeaders
During hydration, the response will be read from the HTML, guaranteeing consistency and preventing an additional network request.

You can learn more about making credentialed requests with cookies here.
fetch }) {
	const const response: anyresponse = await fetch: (input: string | URL | globalThis.Request, init?: RequestInit) => Promise<Response> (+1 overload)MDN Reference
fetch(const url: stringurl).Promise<Response>.then<any, never>(onfulfilled?: ((value: Response) => any) | null | undefined, onrejected?: ((reason: any) => PromiseLike<never>) | null | undefined): Promise<any>Attaches callbacks for the resolution and/or rejection of the Promise.
@paramonfulfilled The callback to execute when the Promise is resolved.@paramonrejected The callback to execute when the Promise is rejected.@returnsA Promise for the completion of which ever callback is executed.then(r: Responser => r: Responser.Body.json(): Promise<any>MDN Reference
json());
	return { response: anyresponse }
}
```

```
// If you have multiple promises
/** @type {import('./$types').PageServerLoad} */
export async function function load(event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>): MaybePromise<void | Record<string, any>>@type{import('./$types').PageServerLoad}load({ fetch: {
    (input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
    (input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response>;
}fetch is equivalent to the native fetch web API, with a few additional features:

It can be used to make credentialed requests on the server, as it inherits the cookie and authorization headers for the page request.
It can make relative requests on the server (ordinarily, fetch requires a URL with an origin when used in a server context).
Internal requests (e.g. for +server.js routes) go directly to the handler function when running on the server, without the overhead of an HTTP call.
During server-side rendering, the response will be captured and inlined into the rendered HTML by hooking into the text and json methods of the Response object. Note that headers will not be serialized, unless explicitly included via filterSerializedResponseHeaders
During hydration, the response will be read from the HTML, guaranteeing consistency and preventing an additional network request.

You can learn more about making credentialed requests with cookies here.
fetch }) {
	const a = fetch(url1).then(r => r.json());
	const b = fetch(url2).then(r => r.json());
	const [const a: anya, const b: anyb] = await var Promise: PromiseConstructorRepresents the completion of an asynchronous operation
Promise.PromiseConstructor.all<[Promise<any>, Promise<any>]>(values: [Promise<any>, Promise<any>]): Promise<[any, any]> (+1 overload)Creates a Promise that is resolved with an array of results when all of the provided Promises
resolve, or rejected when any Promise is rejected.
@paramvalues An array of Promises.@returnsA new Promise.all([
	  fetch: (input: string | URL | globalThis.Request, init?: RequestInit) => Promise<Response> (+1 overload)MDN Reference
fetch(const url1: stringurl1).Promise<Response>.then<any, never>(onfulfilled?: ((value: Response) => any) | null | undefined, onrejected?: ((reason: any) => PromiseLike<never>) | null | undefined): Promise<any>Attaches callbacks for the resolution and/or rejection of the Promise.
@paramonfulfilled The callback to execute when the Promise is resolved.@paramonrejected The callback to execute when the Promise is rejected.@returnsA Promise for the completion of which ever callback is executed.then(r: Responser => r: Responser.Body.json(): Promise<any>MDN Reference
json()),
	  fetch: (input: string | URL | globalThis.Request, init?: RequestInit) => Promise<Response> (+1 overload)MDN Reference
fetch(const url2: stringurl2).Promise<Response>.then<any, never>(onfulfilled?: ((value: Response) => any) | null | undefined, onrejected?: ((reason: any) => PromiseLike<never>) | null | undefined): Promise<any>Attaches callbacks for the resolution and/or rejection of the Promise.
@paramonfulfilled The callback to execute when the Promise is resolved.@paramonrejected The callback to execute when the Promise is rejected.@returnsA Promise for the completion of which ever callback is executed.then(r: Responser => r: Responser.Body.json(): Promise<any>MDN Reference
json()),
	]);
	return { a: anya, b: anyb };
}
```

## goto(...) changes

`goto(...)` no longer accepts external URLs. To navigate to an external URL, use `window.location.href = url`. The `state` object now determines `$page.state` and must adhere to the `App.PageState` interface, if declared. See [shallow routing](https://kit.svelte.dev/docs/shallow-routing) for more details.

## paths are now relative by default

In SvelteKit 1, `%sveltekit.assets%` in your `app.html` was replaced with a relative path by default (i.e. `.` or `..` or `../..` etc, depending on the path being rendered) during server-side rendering unless the [paths.relative](https://kit.svelte.dev/docs/configuration#paths) config option was explicitly set to `false`. The same was true for `base` and `assets` imported from `$app/paths`, but only if the `paths.relative` option was explicitly set to `true`.

This inconsistency is fixed in version 2. Paths are either always relative or always absolute, depending on the value of [paths.relative](https://kit.svelte.dev/docs/configuration#paths). It defaults to `true` as this results in more portable apps: if the `base` is something other than the app expected (as is the case when viewed on the [Internet Archive](https://archive.org/), for example) or unknown at build time (as is the case when deploying to [IPFS](https://ipfs.tech/) and so on), fewer things are likely to break.

## Server fetches are not trackable anymore

Previously it was possible to track URLs from `fetch`es on the server in order to rerun load functions. This poses a possible security risk (private URLs leaking), and for this reason it was behind the `dangerZone.trackServerFetches` setting, which is now removed.

## preloadCode arguments must be prefixed with base

SvelteKit exposes two functions, [preloadCode](https://kit.svelte.dev/docs/$app-navigation#preloadCode) and [preloadData](https://kit.svelte.dev/docs/$app-navigation#preloadData), for programmatically loading the code and data associated with a particular path. In version 1, there was a subtle inconsistency — the path passed to `preloadCode` did not need to be prefixed with the `base` path (if set), while the path passed to `preloadData` did.

This is fixed in SvelteKit 2 — in both cases, the path should be prefixed with `base` if it is set.

Additionally, `preloadCode` now takes a single argument rather than *n* arguments.

## resolvePath has been removed

SvelteKit 1 included a function called `resolvePath` which allows you to resolve a route ID (like `/blog/[slug]`) and a set of parameters (like `{ slug: 'hello' }`) to a pathname. Unfortunately the return value didn’t include the `base` path, limiting its usefulness in cases where `base` was set.

For this reason, SvelteKit 2 replaces `resolvePath` with a (slightly better named) function called `resolveRoute`, which is imported from `$app/paths` and which takes `base` into account.

```
import { resolvePath } from '@sveltejs/kit';
import { base } from '$app/paths';
import { function resolveRoute<T extends RouteId | Pathname>(...args: ResolveArgs<T>): ResolvedPathname@deprecatedUse resolve(...) insteadresolveRoute } from '$app/paths';

const path = base + resolvePath('/blog/[slug]', { slug });
const const path: stringpath = resolveRoute<"/blog/[slug]">(route: "/blog/[slug]", params: Record<string, string>): ResolvedPathname@deprecatedUse resolve(...) insteadresolveRoute('/blog/[slug]', { slug: anyslug });
```

`svelte-migrate` will do the method replacement for you, though if you later prepend the result with `base`, you need to remove that yourself.

## Improved error handling

Errors are handled inconsistently in SvelteKit 1. Some errors trigger the `handleError` hook but there is no good way to discern their status (for example, the only way to tell a 404 from a 500 is by seeing if `event.route.id` is `null`), while others (such as 405 errors for `POST` requests to pages without actions) don’t trigger `handleError` at all, but should. In the latter case, the resulting `$page.error` will deviate from the [App.Error](https://kit.svelte.dev/docs/types#Error) type, if it is specified.

SvelteKit 2 cleans this up by calling `handleError` hooks with two new properties: `status` and `message`. For errors thrown from your code (or library code called by your code) the status will be `500` and the message will be `Internal Error`. While `error.message` may contain sensitive information that should not be exposed to users, `message` is safe.

## Dynamic environment variables cannot be used during prerendering

The `$env/dynamic/public` and `$env/dynamic/private` modules provide access to *run time* environment variables, as opposed to the *build time* environment variables exposed by `$env/static/public` and `$env/static/private`.

During prerendering in SvelteKit 1, they are one and the same. This means that prerendered pages that make use of ‘dynamic’ environment variables are really ‘baking in’ build time values, which is incorrect. Worse, `$env/dynamic/public` is populated in the browser with these stale values if the user happens to land on a prerendered page before navigating to dynamically-rendered pages.

Because of this, dynamic environment variables can no longer be read during prerendering in SvelteKit 2 — you should use the `static` modules instead. If the user lands on a prerendered page, SvelteKit will request up-to-date values for `$env/dynamic/public` from the server (by default from a module called `/_app/env.js`) instead of reading them from the server-rendered HTML.

## form and data have been removed from use:enhance callbacks

If you provide a callback to [use:enhance](https://kit.svelte.dev/docs/form-actions#Progressive-enhancement-use:enhance), it will be called with an object containing various useful properties.

In SvelteKit 1, those properties included `form` and `data`. These were deprecated some time ago in favour of `formElement` and `formData`, and have been removed altogether in SvelteKit 2.

## Forms containing file inputs must use multipart/form-data

If a form contains an `<input type="file">` but does not have an `enctype="multipart/form-data"` attribute, non-JS submissions will omit the file. SvelteKit 2 will throw an error if it encounters a form like this during a `use:enhance` submission to ensure that your forms work correctly when JavaScript is not present.

## Generated tsconfig.json is more strict

Previously, the generated `tsconfig.json` was trying its best to still produce a somewhat valid config when your `tsconfig.json` included `paths` or `baseUrl`. In SvelteKit 2, the validation is more strict and will warn when you use either `paths` or `baseUrl` in your `tsconfig.json`. These settings are used to generate path aliases and you should use [thealiasconfig](https://kit.svelte.dev/docs/configuration#alias) option in your `svelte.config.js` instead, to also create a corresponding alias for the bundler.

## getRequest no longer throws errors

The `@sveltejs/kit/node` module exports helper functions for use in Node environments, including `getRequest` which turns a Node [ClientRequest](https://nodejs.org/api/http.html#class-httpclientrequest) into a standard [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) object.

In SvelteKit 1, `getRequest` could throw if the `Content-Length` header exceeded the specified size limit. In SvelteKit 2, the error will not be thrown until later, when the request body (if any) is being read. This enables better diagnostics and simpler code.

## vitePreprocess is no longer exported from @sveltejs/kit/vite

Since `@sveltejs/vite-plugin-svelte` is now a peer dependency, SvelteKit 2 no longer re-exports `vitePreprocess`. You should import it directly from `@sveltejs/vite-plugin-svelte`.

## Updated dependency requirements

SvelteKit 2 requires Node `18.13` or higher, and the following minimum dependency versions:

- `svelte@4`
- `vite@5`
- `typescript@5`
- `@sveltejs/vite-plugin-svelte@3` (this is now required as a `peerDependency` of SvelteKit — previously it was directly depended upon)
- `@sveltejs/adapter-cloudflare@3` (if you’re using these adapters)
- `@sveltejs/adapter-cloudflare-workers@2`
- `@sveltejs/adapter-netlify@3`
- `@sveltejs/adapter-node@2`
- `@sveltejs/adapter-static@3`
- `@sveltejs/adapter-vercel@4`

`svelte-migrate` will update your `package.json` for you.

As part of the TypeScript upgrade, the generated `tsconfig.json` (the one your `tsconfig.json` extends from) now uses `"moduleResolution": "bundler"` (which is recommended by the TypeScript team, as it properly resolves types from packages with an `exports` map in package.json) and `verbatimModuleSyntax` (which replaces the existing `importsNotUsedAsValues ` and `preserveValueImports` flags — if you have those in your `tsconfig.json`, remove them. `svelte-migrate` will do this for you).

## SvelteKit 2.12: $app/stores deprecated

SvelteKit 2.12 introduced `$app/state` based on the [Svelte 5 runes API](https://kit.svelte.dev/docs/svelte/what-are-runes). `$app/state` provides everything that `$app/stores` provides but with more flexibility as to where and how you use it. Most importantly, the `page` object is now fine-grained, e.g. updates to `page.state` will not invalidate `page.data` and vice-versa.

As a consequence, `$app/stores` is deprecated and subject to be removed in SvelteKit 3. We recommend [upgrading to Svelte 5](https://kit.svelte.dev/docs/svelte/v5-migration-guide), if you haven’t already, and then migrate away from `$app/stores`. Most of the replacements should be pretty simple: Replace the `$app/stores` import with `$app/state` and remove the `$` prefixes from the usage sites.

```
<script>
	import { page } from '$app/stores';
	import { page } from '$app/state';
</script>

{$page.data}
{page.data}
```

Use `npx sv migrate app-state` to auto-migrate most of your `$app/stores` usages inside `.svelte` components.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/60-appendix/30-migrating-to-sveltekit-2.md) [[llms.txt](https://kit.svelte.dev/docs/kit/migrating-to-sveltekit-2/llms.txt)]

 previous next [[Breakpoint Debugging](https://kit.svelte.dev/docs/kit/debugging)] [[Migrating from Sapper](https://kit.svelte.dev/docs/kit/migrating)]

---

# Observability

> Observability • SvelteKit documentation

> Available since 2.31

Sometimes, you may need to observe how your application is behaving in order to improve performance or find the root cause of a pesky bug. To help with this, SvelteKit can emit server-side [OpenTelemetry](https://opentelemetry.io) spans for the following:

- The [handle](https://kit.svelte.dev/docs/hooks#Server-hooks-handle) hook and `handle` functions running in a [sequence](https://kit.svelte.dev/docs/@sveltejs-kit-hooks#sequence) (these will show up as children of each other and the root `handle` hook)
- Server [load](https://kit.svelte.dev/docs/load) functions and universal `load` functions when they’re run on the server
- [Form actions](https://kit.svelte.dev/docs/form-actions)
- [Remote functions](https://kit.svelte.dev/docs/remote-functions)

Just telling SvelteKit to emit spans won’t get you far, though — you need to actually collect them somewhere to be able to view them. SvelteKit provides `src/instrumentation.server.ts` as a place to write your tracing setup and instrumentation code. It’s guaranteed to be run prior to your application code being imported, providing your deployment platform supports it and your adapter is aware of it.

Both of these features are currently experimental, meaning they are likely to contain bugs and are subject to change without notice. You must opt in by adding the `kit.experimental.tracing.server` and `kit.experimental.instrumentation.server` option in your `svelte.config.js`:

 svelte.config

```
/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        experimental: {
 tracing: {
   server: boolean;
 };
 instrumentation: {
   server: boolean;
 };
        };
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    experimental: {
        tracing: {
 server: boolean;
        };
        instrumentation: {
 server: boolean;
        };
    };
}kit: {
		experimental: {
    tracing: {
        server: boolean;
    };
    instrumentation: {
        server: boolean;
    };
}experimental: {
			tracing: {
    server: boolean;
}tracing: {
				server: booleanserver: true
			},
			instrumentation: {
    server: boolean;
}instrumentation: {
				server: booleanserver: true
			}
		}
	}
};

export default const config: {
    kit: {
        experimental: {
 tracing: {
   server: boolean;
 };
 instrumentation: {
   server: boolean;
 };
        };
    };
}@type{import('@sveltejs/kit').Config}config;
```

> Tracing — and more significantly, observability instrumentation — can have a nontrivial overhead. Before you go all-in on tracing, consider whether or not you really need it, or if it might be more appropriate to turn it on in development and preview environments only.

## Augmenting the built-in tracing

SvelteKit provides access to the `root` span and the `current` span on the request event. The root span is the one associated with your root `handle` function, and the current span could be associated with `handle`, `load`, a form action, or a remote function, depending on the context. You can annotate these spans with any attributes you wish to record:

 $lib/authenticate

```
import { function getRequestEvent(): RequestEventReturns the current RequestEvent. Can be used inside server hooks, server load functions, actions, and endpoints (and functions called by them).
In environments without AsyncLocalStorage, this must be called synchronously (i.e. not after an await).
@since2.20.0getRequestEvent } from '$app/server';
import { function getAuthenticatedUser(): Promise<{
    id: string;
}>getAuthenticatedUser } from '$lib/auth-core';

async function function authenticate(): Promise<void>authenticate() {
	const const user: {
    id: string;
}user = await function getAuthenticatedUser(): Promise<{
    id: string;
}>getAuthenticatedUser();
	const const event: RequestEvent<Record<string, string>, string | null>event = function getRequestEvent(): RequestEventReturns the current RequestEvent. Can be used inside server hooks, server load functions, actions, and endpoints (and functions called by them).
In environments without AsyncLocalStorage, this must be called synchronously (i.e. not after an await).
@since2.20.0getRequestEvent();
	const event: RequestEvent<Record<string, string>, string | null>event.RequestEvent<Record<string, string>, string | null>.tracing: {
    enabled: boolean;
    root: Span;
    current: Span;
}Access to spans for tracing. If tracing is not enabled, these spans will do nothing.
@since2.31.0tracing.root: SpanThe root span for the request. This span is named sveltekit.handle.root.
root.setAttribute('userId', const user: {
    id: string;
}user.id: stringid);
}
```

## Development quickstart

To view your first trace, you’ll need to set up a local collector. We’ll use [Jaeger](https://www.jaegertracing.io/docs/getting-started/) in this example, as they provide an easy-to-use quickstart command. Once your collector is running locally:

- Turn on the experimental flags mentioned earlier in your `svelte.config.js` file
- Use your package manager to install the dependencies you’ll need:
  ```
  npm i @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-proto import-in-the-middle
  ```
- Create `src/instrumentation.server.js` with the following:

 src/instrumentation.server

```
import { import NodeSDKNodeSDK } from '@opentelemetry/sdk-node';
import { import getNodeAutoInstrumentationsgetNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { import OTLPTraceExporterOTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { import createAddHookMessageChannelcreateAddHookMessageChannel } from 'import-in-the-middle';
import { function register<Data = any>(specifier: string | URL, parentURL?: string | URL, options?: Module.RegisterOptions<Data>): void (+1 overload)Register a module that exports hooks that customize Node.js module
resolution and loading behavior. See
Customization hooks.
@sincev20.6.0, v18.19.0@paramspecifier Customization hooks to be registered; this should be
the same string that would be passed to import(), except that if it is
relative, it is resolved relative to parentURL.@paramparentURL f you want to resolve specifier relative to a base
URL, such as import.meta.url, you can pass that URL here.register } from 'node:module';

const { const registerOptions: anyregisterOptions } = import createAddHookMessageChannelcreateAddHookMessageChannel();
register<any>(specifier: string | URL, parentURL?: string | URL, options?: Module.RegisterOptions<any> | undefined): void (+1 overload)Register a module that exports hooks that customize Node.js module
resolution and loading behavior. See
Customization hooks.
@sincev20.6.0, v18.19.0@paramspecifier Customization hooks to be registered; this should be
the same string that would be passed to import(), except that if it is
relative, it is resolved relative to parentURL.@paramparentURL f you want to resolve specifier relative to a base
URL, such as import.meta.url, you can pass that URL here.register('import-in-the-middle/hook.mjs', import.meta.ImportMeta.url: stringThe absolute file: URL of the module.
url, const registerOptions: anyregisterOptions);

const const sdk: anysdk = new import NodeSDKNodeSDK({
	serviceName: stringserviceName: 'test-sveltekit-tracing',
	traceExporter: anytraceExporter: new import OTLPTraceExporterOTLPTraceExporter(),
	instrumentations: any[]instrumentations: [import getNodeAutoInstrumentationsgetNodeAutoInstrumentations()]
});

const sdk: anysdk.start();
```

Now, server-side requests will begin generating traces, which you can view in Jaeger’s web console at [localhost:16686](http://localhost:16686).

## @opentelemetry/api

SvelteKit uses `@opentelemetry/api` to generate its spans. This is declared as an optional peer dependency so that users not needing traces see no impact on install size or runtime performance. In most cases, if you’re configuring your application to collect SvelteKit’s spans, you’ll end up installing a library like `@opentelemetry/sdk-node` or `@vercel/otel`, which in turn depend on `@opentelemetry/api`, which will satisfy SvelteKit’s dependency as well. If you see an error from SvelteKit telling you it can’t find `@opentelemetry/api`, it may just be because you haven’t set up your trace collection yet. If you *have* done that and are still seeing the error, you can install `@opentelemetry/api` yourself.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/68-observability.md) [[llms.txt](https://kit.svelte.dev/docs/kit/observability/llms.txt)]

 previous next [[Shallow routing](https://kit.svelte.dev/docs/kit/shallow-routing)] [[Packaging](https://kit.svelte.dev/docs/kit/packaging)]

---

# Packaging

> Packaging • SvelteKit documentation

You can use SvelteKit to build apps as well as component libraries, using the `@sveltejs/package` package (`npx sv create` has an option to set this up for you).

When you’re creating an app, the contents of `src/routes` is the public-facing stuff; [src/lib](https://kit.svelte.dev/docs/$lib) contains your app’s internal library.

A component library has the exact same structure as a SvelteKit app, except that `src/lib` is the public-facing bit, and your root `package.json` is used to publish the package. `src/routes` might be a documentation or demo site that accompanies the library, or it might just be a sandbox you use during development.

Running the `svelte-package` command from `@sveltejs/package` will take the contents of `src/lib` and generate a `dist` directory (which can be [configured](#Options)) containing the following:

- All the files in `src/lib`. Svelte components will be preprocessed, TypeScript files will be transpiled to JavaScript.
- Type definitions (`d.ts` files) which are generated for Svelte, JavaScript and TypeScript files. You need to install `typescript >= 4.0.0` for this. Type definitions are placed next to their implementation, hand-written `d.ts` files are copied over as is. You can [disable generation](#Options), but we strongly recommend against it — people using your library might use TypeScript, for which they require these type definition files.

> `@sveltejs/package` version 1 generated a `package.json`. This is no longer the case and it will now use the `package.json` from your project and validate that it is correct instead. If you’re still on version 1, see [this PR](https://github.com/sveltejs/kit/pull/8922) for migration instructions.

## Anatomy of a package.json

Since you’re now building a library for public use, the contents of your `package.json` will become more important. Through it, you configure the entry points of your package, which files are published to npm, and which dependencies your library has. Let’s go through the most important fields one by one.

### name

This is the name of your package. It will be available for others to install using that name, and visible on `https://npmjs.com/package/<name>`.

```
{
	"name": "your-library"
}
```

Read more about it [here](https://docs.npmjs.com/cli/v9/configuring-npm/package-json#name).

### license

Every package should have a license field so people know how they are allowed to use it. A very popular license which is also very permissive in terms of distribution and reuse without warranty is `MIT`.

```
{
	"license": "MIT"
}
```

Read more about it [here](https://docs.npmjs.com/cli/v9/configuring-npm/package-json#license). Note that you should also include a `LICENSE` file in your package.

### files

This tells npm which files it will pack up and upload to npm. It should contain your output folder (`dist` by default). Your `package.json` and `README` and `LICENSE` will always be included, so you don’t need to specify them.

```
{
	"files": ["dist"]
}
```

To exclude unnecessary files (such as unit tests, or modules that are only imported from `src/routes` etc) you can add them to an `.npmignore` file. This will result in smaller packages that are faster to install.

Read more about it [here](https://docs.npmjs.com/cli/v9/configuring-npm/package-json#files).

### exports

The `"exports"` field contains the package’s entry points. If you set up a new library project through `npx sv create`, it’s set to a single export, the package root:

```
{
	"exports": {
		".": {
			"types": "./dist/index.d.ts",
			"svelte": "./dist/index.js"
		}
	}
}
```

This tells bundlers and tooling that your package only has one entry point, the root, and everything should be imported through that, like this:

```
import { import SomethingSomething } from 'your-library';
```

The `types` and `svelte` keys are [export conditions](https://nodejs.org/api/packages.html#conditional-exports). They tell tooling what file to import when they look up the `your-library` import:

- TypeScript sees the `types` condition and looks up the type definition file. If you don’t publish type definitions, omit this condition.
- Svelte-aware tooling sees the `svelte` condition and knows this is a Svelte component library. If you publish a library that does not export any Svelte components and that could also work in non-Svelte projects (for example a Svelte store library), you can replace this condition with `default`.

> Previous versions of `@sveltejs/package` also added a `package.json` export. This is no longer part of the template because all tooling can now deal with a `package.json` not being explicitly exported.

You can adjust `exports` to your liking and provide more entry points. For example, if instead of a `src/lib/index.js` file that re-exported components you wanted to expose a `src/lib/Foo.svelte` component directly, you could create the following export map...

```
{
	"exports": {
		"./Foo.svelte": {
			"types": "./dist/Foo.svelte.d.ts",
			"svelte": "./dist/Foo.svelte"
		}
	}
}
```

...and a consumer of your library could import the component like so:

```
import module "your-library/Foo.svelte"Foo from 'your-library/Foo.svelte';
```

> Beware that doing this will need additional care if you provide type definitions. Read more about the caveat [here](#TypeScript)

In general, each key of the exports map is the path the user will have to use to import something from your package, and the value is the path to the file that will be imported or a map of export conditions which in turn contains these file paths.

Read more about `exports` [here](https://nodejs.org/docs/latest-v18.x/api/packages.html#package-entry-points).

### svelte

This is a legacy field that enabled tooling to recognise Svelte component libraries. It’s no longer necessary when using the `svelte` [export condition](#Anatomy-of-a-package.json-exports), but for backwards compatibility with outdated tooling that doesn’t yet know about export conditions it’s good to keep it around. It should point towards your root entry point.

```
{
	"svelte": "./dist/index.js"
}
```

### sideEffects

The `sideEffects` field in `package.json` is used by bundlers to determine if a module may contain code that has side effects. A module is considered to have side effects if it makes changes that are observable from other scripts outside the module when it’s imported. For example, side effects include modifying global variables or the prototype of built-in JavaScript objects. Because a side effect could potentially affect the behavior of other parts of the application, these files/modules will be included in the final bundle regardless of whether their exports are used in the application. It is a best practice to avoid side effects in your code.

Setting the `sideEffects` field in `package.json` can help the bundler to be more aggressive in eliminating unused exports from the final bundle, a process known as tree-shaking. This results in smaller and more efficient bundles. Different bundlers handle `sideEffects` in various manners. While not necessary for Vite, we recommend that libraries state that all CSS files have side effects so that your library will be [compatible with webpack](https://webpack.js.org/guides/tree-shaking/#mark-the-file-as-side-effect-free). This is the configuration that comes with newly created projects:

 package

```
{
	"sideEffects": ["**/*.css"]
}
```

> If the scripts in your library have side effects, ensure that you update the `sideEffects` field. All scripts are marked as side effect free by default in newly created projects. If a file with side effects is incorrectly marked as having no side effects, it can result in broken functionality.

If your package has files with side effects, you can specify them in an array:

 package

```
{
	"sideEffects": [
		"**/*.css",
		"./dist/sideEffectfulFile.js"
	]
}
```

This will treat only the specified files as having side effects.

## TypeScript

You should ship type definitions for your library even if you don’t use TypeScript yourself so that people who do get proper intellisense when using your library. `@sveltejs/package` makes the process of generating types mostly opaque to you. By default, when packaging your library, type definitions are auto-generated for JavaScript, TypeScript and Svelte files. All you need to ensure is that the `types` condition in the [exports](#Anatomy-of-a-package.json-exports) map points to the correct files. When initialising a library project through `npx sv create`, this is automatically setup for the root export.

If you have something else than a root export however — for example providing a `your-library/foo` import — you need to take additional care for providing type definitions. Unfortunately, TypeScript by default will *not* resolve the `types` condition for an export like `{ "./foo": { "types": "./dist/foo.d.ts", ... }}`. Instead, it will search for a `foo.d.ts` relative to the root of your library (i.e. `your-library/foo.d.ts` instead of `your-library/dist/foo.d.ts`). To fix this, you have two options:

The first option is to require people using your library to set the `moduleResolution` option in their `tsconfig.json` (or `jsconfig.json`) to `bundler` (available since TypeScript 5, the best and recommended option in the future), `node16` or `nodenext`. This opts TypeScript into actually looking at the exports map and resolving the types correctly.

The second option is to (ab)use the `typesVersions` feature from TypeScript to wire up the types. This is a field inside `package.json` TypeScript uses to check for different type definitions depending on the TypeScript version, and also contains a path mapping feature for that. We leverage that path mapping feature to get what we want. For the mentioned `foo` export above, the corresponding `typesVersions` looks like this:

```
{
	"exports": {
		"./foo": {
			"types": "./dist/foo.d.ts",
			"svelte": "./dist/foo.js"
		}
	},
	"typesVersions": {
		">4.0": {
			"foo": ["./dist/foo.d.ts"]
		}
	}
}
```

`>4.0` tells TypeScript to check the inner map if the used TypeScript version is greater than 4 (which should in practice always be true). The inner map tells TypeScript that the typings for `your-library/foo` are found within `./dist/foo.d.ts`, which essentially replicates the `exports` condition. You also have `*` as a wildcard at your disposal to make many type definitions at once available without repeating yourself. Note that if you opt into `typesVersions` you have to declare all type imports through it, including the root import (which is defined as `"index.d.ts": [..]`).

You can read more about that feature [here](https://www.typescriptlang.org/docs/handbook/declaration-files/publishing.html#version-selection-with-typesversions).

## Best practices

You should avoid using SvelteKit-specific modules like `$app/environment` in your packages unless you intend for them to only be consumable by other SvelteKit projects. E.g. rather than using `import { browser } from '$app/environment'` you could use `import { BROWSER } from 'esm-env'` ([see esm-env docs](https://github.com/benmccann/esm-env)). You may also wish to pass in things like the current URL or a navigation action as a prop rather than relying directly on `$app/state`, `$app/navigation`, etc. Writing your app in this more generic fashion will also make it easier to setup tools for testing, UI demos and so on.

Ensure that you add [aliases](https://kit.svelte.dev/docs/configuration#alias) via `svelte.config.js` (not `vite.config.js` or `tsconfig.json`), so that they are processed by `svelte-package`.

You should think carefully about whether or not the changes you make to your package are a bug fix, a new feature, or a breaking change, and update the package version accordingly. Note that if you remove any paths from `exports` or any `export` conditions inside them from your existing library, that should be regarded as a breaking change.

```
{
	"exports": {
		".": {
			"types": "./dist/index.d.ts",
// changing `svelte` to `default` is a breaking change:
			"svelte": "./dist/index.js"
			"default": "./dist/index.js"
		},
// removing this is a breaking change:
		"./foo": {
			"types": "./dist/foo.d.ts",
			"svelte": "./dist/foo.js",
			"default": "./dist/foo.js"
		},
// adding this is ok:
		"./bar": {
			"types": "./dist/bar.d.ts",
			"svelte": "./dist/bar.js",
			"default": "./dist/bar.js"
		}
	}
}
```

## Source maps

You can create so-called declaration maps (`d.ts.map` files) by setting `"declarationMap": true` in your `tsconfig.json`. This will allow editors such as VS Code to go to the original `.ts` or `.svelte` file when using features like *Go to Definition*. This means you also need to publish your source files alongside your dist folder in a way that the relative path inside the declaration files leads to a file on disk. Assuming that you have all your library code inside `src/lib` as suggested by Svelte’s CLI, this is as simple as adding `src/lib` to `files` in your `package.json`:

```
{
	"files": [
		"dist",
		"!dist/**/*.test.*",
		"!dist/**/*.spec.*",
		"src/lib",
		"!src/lib/**/*.test.*",
		"!src/lib/**/*.spec.*"
	]
}
```

## Options

`svelte-package` accepts the following options:

- `-w` / `--watch` — watch files in `src/lib` for changes and rebuild the package
- `-i` / `--input` — the input directory which contains all the files of the package. Defaults to `src/lib`
- `-o` / `--output` — the output directory where the processed files are written to. Your `package.json`’s `exports` should point to files inside there, and the `files` array should include that folder. Defaults to `dist`
- `-p` / `--preserve-output` — prevent deletion of the output directory before packaging. Defaults to `false`, which means that the output directory will be emptied first
- `-t` / `--types` — whether or not to create type definitions (`d.ts` files). We strongly recommend doing this as it fosters ecosystem library quality. Defaults to `true`
- `--tsconfig` - the path to a tsconfig or jsconfig. When not provided, searches for the next upper tsconfig/jsconfig in the workspace path.

## Publishing

To publish the generated package:

```
npm publish
```

## Caveats

All relative file imports need to be fully specified, adhering to Node’s ESM algorithm. This means that for a file like `src/lib/something/index.js`, you must include the filename with the extension:

```
import { import somethingsomething } from './something/index.js';
```

If you are using TypeScript, you need to import `.ts` files the same way, but using a `.js` file ending, *not* a `.ts` file ending. (This is a TypeScript design decision outside our control.) Setting `"moduleResolution": "NodeNext"` in your `tsconfig.json` or `jsconfig.json` will help you with this.

All files except Svelte files (preprocessed) and TypeScript files (transpiled to JavaScript) are copied across as-is.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/70-packaging.md) [[llms.txt](https://kit.svelte.dev/docs/kit/packaging/llms.txt)]

 previous next [[Observability](https://kit.svelte.dev/docs/kit/observability)] [[Auth](https://kit.svelte.dev/docs/kit/auth)]
