# SEO and more

# SEO

> SEO • SvelteKit documentation

The most important aspect of SEO is to create high-quality content that is widely linked to from around the web. However, there are a few technical considerations for building sites that rank well.

## Out of the box

### SSR

While search engines have got better in recent years at indexing content that was rendered with client-side JavaScript, server-side rendered content is indexed more frequently and reliably. SvelteKit employs SSR by default, and while you can disable it in [handle](https://kit.svelte.dev/docs/hooks#Server-hooks-handle), you should leave it on unless you have a good reason not to.

> SvelteKit’s rendering is highly configurable and you can implement [dynamic rendering](https://developers.google.com/search/docs/advanced/javascript/dynamic-rendering) if necessary. It’s not generally recommended, since SSR has other benefits beyond SEO.

### Performance

Signals such as [Core Web Vitals](https://web.dev/vitals/#core-web-vitals) impact search engine ranking. Because Svelte and SvelteKit introduce minimal overhead, they make it easier to build high performance sites. You can test your site’s performance using Google’s [PageSpeed Insights](https://pagespeed.web.dev/) or [Lighthouse](https://developers.google.com/web/tools/lighthouse). With just a few key actions like using SvelteKit’s default [hybrid rendering](https://kit.svelte.dev/docs/glossary#Hybrid-app) mode and [optimizing your images](https://kit.svelte.dev/docs/images), you can greatly improve your site’s speed. Read [the performance page](https://kit.svelte.dev/docs/performance) for more details.

### Normalized URLs

SvelteKit redirects pathnames with trailing slashes to ones without (or vice versa depending on your [configuration](https://kit.svelte.dev/docs/page-options#trailingSlash)), as duplicate URLs are bad for SEO.

## Manual setup

### <title> and <meta>

Every page should have well-written and unique `<title>` and `<meta name="description">` elements inside a [<svelte:head>](https://kit.svelte.dev/svelte/svelte-head). Guidance on how to write descriptive titles and descriptions, along with other suggestions on making content understandable by search engines, can be found on Google’s [Lighthouse SEO audits](https://web.dev/lighthouse-seo/) documentation.

> A common pattern is to return SEO-related `data` from page [load](https://kit.svelte.dev/docs/load) functions, then use it (as [page.data](https://kit.svelte.dev/docs/$app-state)) in a `<svelte:head>` in your root [layout](https://kit.svelte.dev/docs/routing#layout).

### Sitemaps

[Sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap) help search engines prioritize pages within your site, particularly when you have a large amount of content. You can create a sitemap dynamically using an endpoint:

 src/routes/sitemap.xml/+server

```
export async function function GET(): Promise<Response>GET() {
	return new var Response: new (body?: BodyInit | null, init?: ResponseInit) => ResponseThis Fetch API interface represents the response to a request.
MDN Reference
Response(
		`
		<?xml version="1.0" encoding="UTF-8" ?>
		<urlset
			xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
			xmlns:xhtml="http://www.w3.org/1999/xhtml"
			xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
			xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
			xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
			xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
		>
			
		</urlset>`.String.trim(): stringRemoves the leading and trailing white space and line terminator characters from a string.
trim(),
		{
			ResponseInit.headers?: HeadersInit | undefinedheaders: {
				'Content-Type': 'application/xml'
			}
		}
	);
}
```

### AMP

An unfortunate reality of modern web development is that it is sometimes necessary to create an [Accelerated Mobile Pages (AMP)](https://amp.dev/) version of your site. In SvelteKit this can be done by setting the [inlineStyleThreshold](https://kit.svelte.dev/docs/configuration#inlineStyleThreshold) option...

 svelte.config

```
/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        inlineStyleThreshold: number;
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    inlineStyleThreshold: number;
}kit: {
		// since <link rel="stylesheet"> isn't
		// allowed, inline all styles
		inlineStyleThreshold: numberinlineStyleThreshold: var Infinity: numberInfinity
	}
};

export default const config: {
    kit: {
        inlineStyleThreshold: number;
    };
}@type{import('@sveltejs/kit').Config}config;
```

...disabling `csr` in your root `+layout.js` / `+layout.server.js`...

 src/routes/+layout.server

```
export const const csr: falsecsr = false;
```

...adding `amp` to your `app.html`

```
<html amp>
...
```

...and transforming the HTML using `transformPageChunk` along with `transform` imported from `@sveltejs/amp`:

 src/hooks.server

```
import * as import ampamp from '@sveltejs/amp';

/** @type {import('@sveltejs/kit').Handle} */
export async function function handle({ event, resolve }: {
    event: any;
    resolve: any;
}): Promise<any>@type{import('@sveltejs/kit').Handle}handle({ event: anyevent, resolve: anyresolve }) {
	let let buffer: stringbuffer = '';
	return await resolve: anyresolve(event: anyevent, {
		transformPageChunk: ({ html, done }: {
    html: any;
    done: any;
}) => string | undefinedtransformPageChunk: ({ html: anyhtml, done: anydone }) => {
			let buffer: stringbuffer += html: anyhtml;
			if (done: anydone) return import ampamp.function transform(html: string): stringtransform(let buffer: stringbuffer);
		}
	});
}
```

```
import * as import ampamp from '@sveltejs/amp';
import type { type Handle = (input: {
    event: RequestEvent;
    resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>;
}) => MaybePromise<...>The handle hook runs every time the SvelteKit server receives a request and
determines the response.
It receives an event object representing the request and a function called resolve, which renders the route and generates a Response.
This allows you to modify response headers or bodies, or bypass SvelteKit entirely (for implementing routes programmatically, for example).
Handle } from '@sveltejs/kit';

export const const handle: Handlehandle: type Handle = (input: {
    event: RequestEvent;
    resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>;
}) => MaybePromise<...>The handle hook runs every time the SvelteKit server receives a request and
determines the response.
It receives an event object representing the request and a function called resolve, which renders the route and generates a Response.
This allows you to modify response headers or bodies, or bypass SvelteKit entirely (for implementing routes programmatically, for example).
Handle = async ({ event: RequestEvent<Record<string, string>, string | null>event, resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve }) => {
	let let buffer: stringbuffer = '';
	return await resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve(event: RequestEvent<Record<string, string>, string | null>event, {
		ResolveOptions.transformPageChunk?: ((input: {
    html: string;
    done: boolean;
}) => MaybePromise<string | undefined>) | undefinedApplies custom transforms to HTML. If done is true, it’s the final chunk. Chunks are not guaranteed to be well-formed HTML
(they could include an element’s opening tag but not its closing tag, for example)
but they will always be split at sensible boundaries such as %sveltekit.head% or layout/page components.
@paraminput the html chunk and the info if this is the last chunktransformPageChunk: ({ html: stringhtml, done: booleandone }) => {
			let buffer: stringbuffer += html: stringhtml;
			if (done: booleandone) return import ampamp.function transform(html: string): stringtransform(let buffer: stringbuffer);
		}
	});
};
```

To prevent shipping any unused CSS as a result of transforming the page to amp, we can use [dropcss](https://www.npmjs.com/package/dropcss):

 src/hooks.server

```
import * as import ampamp from '@sveltejs/amp';
import module "dropcss"dropcss from 'dropcss';

/** @type {import('@sveltejs/kit').Handle} */
export async function function handle(input: {
    event: RequestEvent;
    resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>;
}): MaybePromise<...>@type{import('@sveltejs/kit').Handle}handle({ event: RequestEvent<Record<string, string>, string | null>event, resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve }) {
	let let buffer: stringbuffer = '';

	return await resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve(event: RequestEvent<Record<string, string>, string | null>event, {
		ResolveOptions.transformPageChunk?: ((input: {
    html: string;
    done: boolean;
}) => MaybePromise<string | undefined>) | undefinedApplies custom transforms to HTML. If done is true, it’s the final chunk. Chunks are not guaranteed to be well-formed HTML
(they could include an element’s opening tag but not its closing tag, for example)
but they will always be split at sensible boundaries such as %sveltekit.head% or layout/page components.
@paraminput the html chunk and the info if this is the last chunktransformPageChunk: ({ html: stringhtml, done: booleandone }) => {
			let buffer: stringbuffer += html: stringhtml;

			if (done: booleandone) {
				let let css: stringcss = '';
				const const markup: stringmarkup = import ampamp
					.function transform(html: string): stringtransform(let buffer: stringbuffer)
					.String.replace(searchValue: string | RegExp, replaceValue: string): string (+3 overloads)Replaces text in a string, using a regular expression or search string.
@paramsearchValue A string or regular expression to search for.@paramreplaceValue A string containing the text to replace. When the {@linkcode searchValue} is a RegExp, all matches are replaced if the g flag is set (or only those matches at the beginning, if the y flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced.replace('⚡', 'amp') // dropcss can't handle this character
					.String.replace(searchValue: {
    [Symbol.replace](string: string, replacer: (substring: string, ...args: any[]) => string): string;
}, replacer: (substring: string, ...args: any[]) => string): string (+3 overloads)Replaces text in a string, using an object that supports replacement within a string.
@paramsearchValue A object can search for and replace matches within a string.@paramreplacer A function that returns the replacement text.replace(/<style amp-custom([^>]*?)>([^]+?)<\/style>/, (match: stringmatch, attributes: anyattributes, contents: anycontents) => {
						let css: stringcss = contents: anycontents;
						return `<style amp-custom${attributes: anyattributes}></style>`;
					});

				let css: stringcss = module "dropcss"dropcss({ css: stringcss, html: stringhtml: const markup: stringmarkup }).css;
				return const markup: stringmarkup.String.replace(searchValue: string | RegExp, replaceValue: string): string (+3 overloads)Replaces text in a string, using a regular expression or search string.
@paramsearchValue A string or regular expression to search for.@paramreplaceValue A string containing the text to replace. When the {@linkcode searchValue} is a RegExp, all matches are replaced if the g flag is set (or only those matches at the beginning, if the y flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced.replace('</style>', `${let css: stringcss}</style>`);
			}
		}
	});
}
```

```
import * as import ampamp from '@sveltejs/amp';
import module "dropcss"dropcss from 'dropcss';
import type { type Handle = (input: {
    event: RequestEvent;
    resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>;
}) => MaybePromise<...>The handle hook runs every time the SvelteKit server receives a request and
determines the response.
It receives an event object representing the request and a function called resolve, which renders the route and generates a Response.
This allows you to modify response headers or bodies, or bypass SvelteKit entirely (for implementing routes programmatically, for example).
Handle } from '@sveltejs/kit';

export const const handle: Handlehandle: type Handle = (input: {
    event: RequestEvent;
    resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>;
}) => MaybePromise<...>The handle hook runs every time the SvelteKit server receives a request and
determines the response.
It receives an event object representing the request and a function called resolve, which renders the route and generates a Response.
This allows you to modify response headers or bodies, or bypass SvelteKit entirely (for implementing routes programmatically, for example).
Handle = async ({ event: RequestEvent<Record<string, string>, string | null>event, resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve }) => {
	let let buffer: stringbuffer = '';

	return await resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve(event: RequestEvent<Record<string, string>, string | null>event, {
		ResolveOptions.transformPageChunk?: ((input: {
    html: string;
    done: boolean;
}) => MaybePromise<string | undefined>) | undefinedApplies custom transforms to HTML. If done is true, it’s the final chunk. Chunks are not guaranteed to be well-formed HTML
(they could include an element’s opening tag but not its closing tag, for example)
but they will always be split at sensible boundaries such as %sveltekit.head% or layout/page components.
@paraminput the html chunk and the info if this is the last chunktransformPageChunk: ({ html: stringhtml, done: booleandone }) => {
			let buffer: stringbuffer += html: stringhtml;

			if (done: booleandone) {
				let let css: stringcss = '';
				const const markup: stringmarkup = import ampamp
					.function transform(html: string): stringtransform(let buffer: stringbuffer)
					.String.replace(searchValue: string | RegExp, replaceValue: string): string (+3 overloads)Replaces text in a string, using a regular expression or search string.
@paramsearchValue A string or regular expression to search for.@paramreplaceValue A string containing the text to replace. When the {@linkcode searchValue} is a RegExp, all matches are replaced if the g flag is set (or only those matches at the beginning, if the y flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced.replace('⚡', 'amp') // dropcss can't handle this character
					.String.replace(searchValue: {
    [Symbol.replace](string: string, replacer: (substring: string, ...args: any[]) => string): string;
}, replacer: (substring: string, ...args: any[]) => string): string (+3 overloads)Replaces text in a string, using an object that supports replacement within a string.
@paramsearchValue A object can search for and replace matches within a string.@paramreplacer A function that returns the replacement text.replace(/<style amp-custom([^>]*?)>([^]+?)<\/style>/, (match: stringmatch, attributes: anyattributes, contents: anycontents) => {
						let css: stringcss = contents: anycontents;
						return `<style amp-custom${attributes: anyattributes}></style>`;
					});

				let css: stringcss = module "dropcss"dropcss({ css: stringcss, html: stringhtml: const markup: stringmarkup }).css;
				return const markup: stringmarkup.String.replace(searchValue: string | RegExp, replaceValue: string): string (+3 overloads)Replaces text in a string, using a regular expression or search string.
@paramsearchValue A string or regular expression to search for.@paramreplaceValue A string containing the text to replace. When the {@linkcode searchValue} is a RegExp, all matches are replaced if the g flag is set (or only those matches at the beginning, if the y flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced.replace('</style>', `${let css: stringcss}</style>`);
			}
		}
	});
};
```

> It’s a good idea to use the `handle` hook to validate the transformed HTML using `amphtml-validator`, but only if you’re prerendering pages since it’s very slow.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/40-best-practices/20-seo.md) [[llms.txt](https://kit.svelte.dev/docs/kit/seo/llms.txt)]

 previous next [[Accessibility](https://kit.svelte.dev/docs/kit/accessibility)] [[Frequently asked questions](https://kit.svelte.dev/docs/kit/faq)]

---

# Server

> Server-only modules • SvelteKit documentation

Like a good friend, SvelteKit keeps your secrets. When writing your backend and frontend in the same repository, it can be easy to accidentally import sensitive data into your front-end code (environment variables containing API keys, for example). SvelteKit provides a way to prevent this entirely: server-only modules.

## Private environment variables

The [$env/static/private](https://kit.svelte.dev/docs/$env-static-private) and [$env/dynamic/private](https://kit.svelte.dev/docs/$env-dynamic-private) modules can only be imported into modules that only run on the server, such as [hooks.server.js](https://kit.svelte.dev/docs/hooks#Server-hooks) or [+page.server.js](https://kit.svelte.dev/docs/routing#page-page.server.js).

## Server-only utilities

The [$app/server](https://kit.svelte.dev/docs/$app-server) module, which contains a [read](https://kit.svelte.dev/docs/$app-server#read) function for reading assets from the filesystem, can likewise only be imported by code that runs on the server.

## Your modules

You can make your own modules server-only in two ways:

- adding `.server` to the filename, e.g. `secrets.server.js`
- placing them in `$lib/server`, e.g. `$lib/server/secrets.js`

## How it works

Any time you have public-facing code that imports server-only code (whether directly or indirectly)...

 $lib/server/secrets

```
export const atlantisCoordinates = [/* redacted */];
```

src/routes/utils

```
export { export atlantisCoordinatesatlantisCoordinates } from '$lib/server/secrets.js';

export const const add: (a: any, b: any) => anyadd = (a, b) => a: anya + b: anyb;
```

src/routes/+page

```
<script>
	import { add } from './utils.js';
</script>
```

...SvelteKit will error:

```
Cannot import $lib/server/secrets.ts into code that runs in the browser, as this could leak sensitive information.

 src/routes/+page.svelte imports
  src/routes/utils.js imports
   $lib/server/secrets.ts

If you're only using the import as a type, change it to `import type`.
```

Even though the public-facing code — `src/routes/+page.svelte` — only uses the `add` export and not the secret `atlantisCoordinates` export, the secret code could end up in JavaScript that the browser downloads, and so the import chain is considered unsafe.

This feature also works with dynamic imports, even interpolated ones like `await import(`./${foo}.js`)`.

> Unit testing frameworks like Vitest do not distinguish between server-only and public-facing code. For this reason, illegal import detection is disabled when running tests, as determined by `process.env.TEST === 'true'`.

## Further reading

- [Tutorial: Environment variables](https://kit.svelte.dev/tutorial/kit/env-static-private)

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/50-server-only-modules.md) [[llms.txt](https://kit.svelte.dev/docs/kit/server-only-modules/llms.txt)]

 previous next [[Service workers](https://kit.svelte.dev/docs/kit/service-workers)] [[Snapshots](https://kit.svelte.dev/docs/kit/snapshots)]

---

# Service workers

> Service workers • SvelteKit documentation

Service workers act as proxy servers that handle network requests inside your app. This makes it possible to make your app work offline, but even if you don’t need offline support (or can’t realistically implement it because of the type of app you’re building), it’s often worth using service workers to speed up navigation by precaching your built JS and CSS.

In SvelteKit, if you have a `src/service-worker.js` file (or `src/service-worker/index.js`) it will be bundled and automatically registered. You can change the [location of your service worker](https://kit.svelte.dev/docs/configuration#files) if you need to.

You can [disable automatic registration](https://kit.svelte.dev/docs/configuration#serviceWorker) if you need to register the service worker with your own logic or use another solution. The default registration looks something like this:

```
if ('serviceWorker' in var navigator: NavigatorMDN Reference
navigator) {
	function addEventListener<"load">(type: "load", listener: (this: Window, ev: Event) => any, options?: boolean | AddEventListenerOptions): void (+1 overload)addEventListener('load', function () {
		var navigator: NavigatorMDN Reference
navigator.Navigator.serviceWorker: ServiceWorkerContainerAvailable only in secure contexts.
MDN Reference
serviceWorker.ServiceWorkerContainer.register(scriptURL: string | URL, options?: RegistrationOptions): Promise<ServiceWorkerRegistration>MDN Reference
register('./path/to/service-worker.js');
	});
}
```

## Inside the service worker

Inside the service worker you have access to the [$service-workermodule](https://kit.svelte.dev/docs/$service-worker), which provides you with the paths to all static assets, build files and prerendered pages. You’re also provided with an app version string, which you can use for creating a unique cache name, and the deployment’s `base` path. If your Vite config specifies `define` (used for global variable replacements), this will be applied to service workers as well as your server/client builds.

The following example caches the built app and any files in `static` eagerly, and caches all other requests as they happen. This would make each page work offline once visited.

 src/service-worker

```
// Disables access to DOM typings like `HTMLElement` which are not available
// inside a service worker and instantiates the correct globals
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />

// Ensures that the `$service-worker` import has proper type definitions
/// <reference types="@sveltejs/kit" />

// Only necessary if you have an import from `$env/static/public`
/// <reference types="../.svelte-kit/ambient.d.ts" />

import { const build: string[]An array of URL strings representing the files generated by Vite, suitable for caching with cache.addAll(build).
During development, this is an empty array.
build, const files: string[]An array of URL strings representing the files in your static directory, or whatever directory is specified by config.kit.files.assets. You can customize which files are included from static directory using config.kit.serviceWorker.files
files, const version: stringSee config.kit.version. It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.
version } from '$service-worker';

// This gives `self` the correct types
const const self: Window & typeof globalThisself = /** @type {ServiceWorkerGlobalScope} */ (/** @type {unknown} */ (module globalThisglobalThis.var self: Window & typeof globalThisMDN Reference
self));

// Create a unique cache name for this deployment
const const CACHE: stringCACHE = `cache-${const version: stringSee config.kit.version. It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.
version}`;

const const ASSETS: string[]ASSETS = [
	...const build: string[]An array of URL strings representing the files generated by Vite, suitable for caching with cache.addAll(build).
During development, this is an empty array.
build, // the app itself
	...const files: string[]An array of URL strings representing the files in your static directory, or whatever directory is specified by config.kit.files.assets. You can customize which files are included from static directory using config.kit.serviceWorker.files
files  // everything in `static`
];

const self: Window & typeof globalThisself.function addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions): void (+1 overload)Appends an event listener for events whose type attribute value is type. The callback argument sets the callback that will be invoked when the event is dispatched.
The options argument sets listener-specific options. For compatibility this can be a boolean, in which case the method behaves exactly as if the value was specified as options’s capture.
When set to true, options’s capture prevents callback from being invoked when the event’s eventPhase attribute value is BUBBLING_PHASE. When false (or not present), callback will not be invoked when event’s eventPhase attribute value is CAPTURING_PHASE. Either way, callback will be invoked if event’s eventPhase attribute value is AT_TARGET.
When set to true, options’s passive indicates that the callback will not cancel the event by invoking preventDefault(). This is used to enable performance optimizations described in § 2.8 Observing event listeners.
When set to true, options’s once indicates that the callback will only be invoked once after which the event listener will be removed.
If an AbortSignal is passed for options’s signal, then the event listener will be removed when signal is aborted.
The event listener is appended to target’s event listener list and is not appended if it has the same type, callback, and capture.
MDN Reference
addEventListener('install', (event: Eventevent) => {
	// Create a new cache and add all files to it
	async function function (local function) addFilesToCache(): Promise<void>addFilesToCache() {
		const const cache: Cachecache = await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.open(cacheName: string): Promise<Cache>MDN Reference
open(const CACHE: stringCACHE);
		await const cache: Cachecache.Cache.addAll(requests: Iterable<RequestInfo>): Promise<void> (+1 overload)MDN Reference
addAll(const ASSETS: string[]ASSETS);
	}

	event: Eventevent.waitUntil(function (local function) addFilesToCache(): Promise<void>addFilesToCache());
});

const self: Window & typeof globalThisself.function addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions): void (+1 overload)Appends an event listener for events whose type attribute value is type. The callback argument sets the callback that will be invoked when the event is dispatched.
The options argument sets listener-specific options. For compatibility this can be a boolean, in which case the method behaves exactly as if the value was specified as options’s capture.
When set to true, options’s capture prevents callback from being invoked when the event’s eventPhase attribute value is BUBBLING_PHASE. When false (or not present), callback will not be invoked when event’s eventPhase attribute value is CAPTURING_PHASE. Either way, callback will be invoked if event’s eventPhase attribute value is AT_TARGET.
When set to true, options’s passive indicates that the callback will not cancel the event by invoking preventDefault(). This is used to enable performance optimizations described in § 2.8 Observing event listeners.
When set to true, options’s once indicates that the callback will only be invoked once after which the event listener will be removed.
If an AbortSignal is passed for options’s signal, then the event listener will be removed when signal is aborted.
The event listener is appended to target’s event listener list and is not appended if it has the same type, callback, and capture.
MDN Reference
addEventListener('activate', (event: Eventevent) => {
	// Remove previous cached data from disk
	async function function (local function) deleteOldCaches(): Promise<void>deleteOldCaches() {
		for (const const key: stringkey of await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.keys(): Promise<string[]>MDN Reference
keys()) {
			if (const key: stringkey !== const CACHE: stringCACHE) await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.delete(cacheName: string): Promise<boolean>MDN Reference
delete(const key: stringkey);
		}
	}

	event: Eventevent.waitUntil(function (local function) deleteOldCaches(): Promise<void>deleteOldCaches());
});

const self: Window & typeof globalThisself.function addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions): void (+1 overload)Appends an event listener for events whose type attribute value is type. The callback argument sets the callback that will be invoked when the event is dispatched.
The options argument sets listener-specific options. For compatibility this can be a boolean, in which case the method behaves exactly as if the value was specified as options’s capture.
When set to true, options’s capture prevents callback from being invoked when the event’s eventPhase attribute value is BUBBLING_PHASE. When false (or not present), callback will not be invoked when event’s eventPhase attribute value is CAPTURING_PHASE. Either way, callback will be invoked if event’s eventPhase attribute value is AT_TARGET.
When set to true, options’s passive indicates that the callback will not cancel the event by invoking preventDefault(). This is used to enable performance optimizations described in § 2.8 Observing event listeners.
When set to true, options’s once indicates that the callback will only be invoked once after which the event listener will be removed.
If an AbortSignal is passed for options’s signal, then the event listener will be removed when signal is aborted.
The event listener is appended to target’s event listener list and is not appended if it has the same type, callback, and capture.
MDN Reference
addEventListener('fetch', (event: Eventevent) => {
	// ignore POST requests etc
	if (event: Eventevent.request.method !== 'GET') return;

	async function function (local function) respond(): Promise<Response>respond() {
		const const url: URLurl = new var URL: new (url: string | URL, base?: string | URL) => URLThe URL interface represents an object providing static methods used for creating object URLs.
MDN Reference
URL class is a global reference for import { URL } from 'node:url'
https://nodejs.org/api/url.html#the-whatwg-url-api
@sincev10.0.0URL(event: Eventevent.request.url);
		const const cache: Cachecache = await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.open(cacheName: string): Promise<Cache>MDN Reference
open(const CACHE: stringCACHE);

		// `build`/`files` can always be served from the cache
		if (const ASSETS: string[]ASSETS.Array<string>.includes(searchElement: string, fromIndex?: number): booleanDetermines whether an array includes a certain element, returning true or false as appropriate.
@paramsearchElement The element to search for.@paramfromIndex The position in this array at which to begin searching for searchElement.includes(const url: URLurl.URL.pathname: stringMDN Reference
pathname)) {
			const const response: Response | undefinedresponse = await const cache: Cachecache.Cache.match(request: RequestInfo | URL, options?: CacheQueryOptions): Promise<Response | undefined>MDN Reference
match(const url: URLurl.URL.pathname: stringMDN Reference
pathname);

			if (const response: Response | undefinedresponse) {
				return const response: Responseresponse;
			}
		}

		// for everything else, try the network first, but
		// fall back to the cache if we're offline
		try {
			const const response: Responseresponse = await function fetch(input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response> (+1 overload)MDN Reference
fetch(event: Eventevent.request);

			// if we're offline, fetch can return a value that is not a Response
			// instead of throwing - and we can't pass this non-Response to respondWith
			if (!(const response: Responseresponse instanceof var Response: {
    new (body?: BodyInit | null, init?: ResponseInit): Response;
    prototype: Response;
    error(): Response;
    json(data: any, init?: ResponseInit): Response;
    redirect(url: string | URL, status?: number): Response;
}This Fetch API interface represents the response to a request.
MDN Reference
Response)) {
				throw new var Error: ErrorConstructor
new (message?: string, options?: ErrorOptions) => Error (+1 overload)Error('invalid response from fetch');
			}

			if (const response: Responseresponse.Response.status: numberMDN Reference
status === 200) {
				const cache: Cachecache.Cache.put(request: RequestInfo | URL, response: Response): Promise<void>MDN Reference
put(event: Eventevent.request, const response: Responseresponse.Response.clone(): ResponseMDN Reference
clone());
			}

			return const response: Responseresponse;
		} catch (function (local var) err: unknownerr) {
			const const response: Response | undefinedresponse = await const cache: Cachecache.Cache.match(request: RequestInfo | URL, options?: CacheQueryOptions): Promise<Response | undefined>MDN Reference
match(event: Eventevent.request);

			if (const response: Response | undefinedresponse) {
				return const response: Responseresponse;
			}

			// if there's no cache, then just error out
			// as there is nothing we can do to respond to this request
			throw function (local var) err: unknownerr;
		}
	}

	event: Eventevent.respondWith(function (local function) respond(): Promise<Response>respond());
});
```

```
// Disables access to DOM typings like `HTMLElement` which are not available
// inside a service worker and instantiates the correct globals
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />

// Ensures that the `$service-worker` import has proper type definitions
/// <reference types="@sveltejs/kit" />

// Only necessary if you have an import from `$env/static/public`
/// <reference types="../.svelte-kit/ambient.d.ts" />

import { const build: string[]An array of URL strings representing the files generated by Vite, suitable for caching with cache.addAll(build).
During development, this is an empty array.
build, const files: string[]An array of URL strings representing the files in your static directory, or whatever directory is specified by config.kit.files.assets. You can customize which files are included from static directory using config.kit.serviceWorker.files
files, const version: stringSee config.kit.version. It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.
version } from '$service-worker';

// This gives `self` the correct types
const const self: ServiceWorkerGlobalScopeself = module globalThisglobalThis.var self: Window & typeof globalThisMDN Reference
self as unknown as type ServiceWorkerGlobalScope = /*unresolved*/ anyServiceWorkerGlobalScope;

// Create a unique cache name for this deployment
const const CACHE: stringCACHE = `cache-${const version: stringSee config.kit.version. It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.
version}`;

const const ASSETS: string[]ASSETS = [
	...const build: string[]An array of URL strings representing the files generated by Vite, suitable for caching with cache.addAll(build).
During development, this is an empty array.
build, // the app itself
	...const files: string[]An array of URL strings representing the files in your static directory, or whatever directory is specified by config.kit.files.assets. You can customize which files are included from static directory using config.kit.serviceWorker.files
files  // everything in `static`
];

const self: ServiceWorkerGlobalScopeself.addEventListener('install', (event: anyevent) => {
	// Create a new cache and add all files to it
	async function function (local function) addFilesToCache(): Promise<void>addFilesToCache() {
		const const cache: Cachecache = await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.open(cacheName: string): Promise<Cache>MDN Reference
open(const CACHE: stringCACHE);
		await const cache: Cachecache.Cache.addAll(requests: Iterable<RequestInfo>): Promise<void> (+1 overload)MDN Reference
addAll(const ASSETS: string[]ASSETS);
	}

	event: anyevent.waitUntil(function (local function) addFilesToCache(): Promise<void>addFilesToCache());
});

const self: ServiceWorkerGlobalScopeself.addEventListener('activate', (event: anyevent) => {
	// Remove previous cached data from disk
	async function function (local function) deleteOldCaches(): Promise<void>deleteOldCaches() {
		for (const const key: stringkey of await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.keys(): Promise<string[]>MDN Reference
keys()) {
			if (const key: stringkey !== const CACHE: stringCACHE) await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.delete(cacheName: string): Promise<boolean>MDN Reference
delete(const key: stringkey);
		}
	}

	event: anyevent.waitUntil(function (local function) deleteOldCaches(): Promise<void>deleteOldCaches());
});

const self: ServiceWorkerGlobalScopeself.addEventListener('fetch', (event: anyevent) => {
	// ignore POST requests etc
	if (event: anyevent.request.method !== 'GET') return;

	async function function (local function) respond(): Promise<Response>respond() {
		const const url: URLurl = new var URL: new (url: string | URL, base?: string | URL) => URLThe URL interface represents an object providing static methods used for creating object URLs.
MDN Reference
URL class is a global reference for import { URL } from 'node:url'
https://nodejs.org/api/url.html#the-whatwg-url-api
@sincev10.0.0URL(event: anyevent.request.url);
		const const cache: Cachecache = await var caches: CacheStorageAvailable only in secure contexts.
MDN Reference
caches.CacheStorage.open(cacheName: string): Promise<Cache>MDN Reference
open(const CACHE: stringCACHE);

		// `build`/`files` can always be served from the cache
		if (const ASSETS: string[]ASSETS.Array<string>.includes(searchElement: string, fromIndex?: number): booleanDetermines whether an array includes a certain element, returning true or false as appropriate.
@paramsearchElement The element to search for.@paramfromIndex The position in this array at which to begin searching for searchElement.includes(const url: URLurl.URL.pathname: stringMDN Reference
pathname)) {
			const const response: Response | undefinedresponse = await const cache: Cachecache.Cache.match(request: RequestInfo | URL, options?: CacheQueryOptions): Promise<Response | undefined>MDN Reference
match(const url: URLurl.URL.pathname: stringMDN Reference
pathname);

			if (const response: Response | undefinedresponse) {
				return const response: Responseresponse;
			}
		}

		// for everything else, try the network first, but
		// fall back to the cache if we're offline
		try {
			const const response: Responseresponse = await function fetch(input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response> (+1 overload)MDN Reference
fetch(event: anyevent.request);

			// if we're offline, fetch can return a value that is not a Response
			// instead of throwing - and we can't pass this non-Response to respondWith
			if (!(const response: Responseresponse instanceof var Response: {
    new (body?: BodyInit | null, init?: ResponseInit): Response;
    prototype: Response;
    error(): Response;
    json(data: any, init?: ResponseInit): Response;
    redirect(url: string | URL, status?: number): Response;
}This Fetch API interface represents the response to a request.
MDN Reference
Response)) {
				throw new var Error: ErrorConstructor
new (message?: string, options?: ErrorOptions) => Error (+1 overload)Error('invalid response from fetch');
			}

			if (const response: Responseresponse.Response.status: numberMDN Reference
status === 200) {
				const cache: Cachecache.Cache.put(request: RequestInfo | URL, response: Response): Promise<void>MDN Reference
put(event: anyevent.request, const response: Responseresponse.Response.clone(): ResponseMDN Reference
clone());
			}

			return const response: Responseresponse;
		} catch (function (local var) err: unknownerr) {
			const const response: Response | undefinedresponse = await const cache: Cachecache.Cache.match(request: RequestInfo | URL, options?: CacheQueryOptions): Promise<Response | undefined>MDN Reference
match(event: anyevent.request);

			if (const response: Response | undefinedresponse) {
				return const response: Responseresponse;
			}

			// if there's no cache, then just error out
			// as there is nothing we can do to respond to this request
			throw function (local var) err: unknownerr;
		}
	}

	event: anyevent.respondWith(function (local function) respond(): Promise<Response>respond());
});
```

> Be careful when caching! In some cases, stale data might be worse than data that’s unavailable while offline. Since browsers will empty caches if they get too full, you should also be careful about caching large assets like video files.

## During development

The service worker is bundled for production, but not during development. For that reason, only browsers that support [modules in service workers](https://web.dev/es-modules-in-sw) will be able to use them at dev time. If you are manually registering your service worker, you will need to pass the `{ type: 'module' }` option in development:

```
import { const dev: booleanWhether the dev server is running. This is not guaranteed to correspond to NODE_ENV or MODE.
dev } from '$app/environment';

var navigator: NavigatorMDN Reference
navigator.Navigator.serviceWorker: ServiceWorkerContainerAvailable only in secure contexts.
MDN Reference
serviceWorker.ServiceWorkerContainer.register(scriptURL: string | URL, options?: RegistrationOptions): Promise<ServiceWorkerRegistration>MDN Reference
register('/service-worker.js', {
	RegistrationOptions.type?: WorkerType | undefinedtype: const dev: booleanWhether the dev server is running. This is not guaranteed to correspond to NODE_ENV or MODE.
dev ? 'module' : 'classic'
});
```

> `build` and `prerendered` are empty arrays during development

## Other solutions

SvelteKit’s service worker implementation is designed to be easy to work with and is probably a good solution for most users. However, outside of SvelteKit, many PWA applications leverage the [Workbox](https://web.dev/learn/pwa/workbox) library. If you’re used to using Workbox you may prefer [Vite PWA plugin](https://vite-pwa-org.netlify.app/frameworks/sveltekit.html).

## References

For more general information on service workers, we recommend [the MDN web docs](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers).

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/40-service-workers.md) [[llms.txt](https://kit.svelte.dev/docs/kit/service-workers/llms.txt)]

 previous next [[Link options](https://kit.svelte.dev/docs/kit/link-options)] [[Server-only modules](https://kit.svelte.dev/docs/kit/server-only-modules)]
