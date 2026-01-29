# $app/environment and more

# $app/environment

> $app/environment • SvelteKit documentation

```
import { const browser: booleantrue if the app is running in the browser.
browser, const building: booleanSvelteKit analyses your app during the build step by running it. During this process, building is true. This also applies during prerendering.
building, const dev: booleanWhether the dev server is running. This is not guaranteed to correspond to NODE_ENV or MODE.
dev, const version: stringThe value of config.kit.version.name.
version } from '$app/environment';
```

## browser

`true` if the app is running in the browser.

```
const browser: boolean;
```

## building

SvelteKit analyses your app during the `build` step by running it. During this process, `building` is `true`. This also applies during prerendering.

```
const building: boolean;
```

## dev

Whether the dev server is running. This is not guaranteed to correspond to `NODE_ENV` or `MODE`.

```
const dev: boolean;
```

## version

The value of `config.kit.version.name`.

```
const version: string;
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/20-$app-environment.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$app-environment/llms.txt)]

 previous next [[@sveltejs/kit/vite](https://kit.svelte.dev/docs/kit/@sveltejs-kit-vite)] [[$app/forms](https://kit.svelte.dev/docs/kit/$app-forms)]

---

# $app/navigation

> $app/navigation • SvelteKit documentation

```
import {
	function afterNavigate(callback: (navigation: import("@sveltejs/kit").AfterNavigate) => void): voidA lifecycle function that runs the supplied callback when the current component mounts, and also whenever we navigate to a URL.
afterNavigate must be called during a component initialization. It remains active as long as the component is mounted.
afterNavigate,
	function beforeNavigate(callback: (navigation: import("@sveltejs/kit").BeforeNavigate) => void): voidA navigation interceptor that triggers before we navigate to a URL, whether by clicking a link, calling goto(...), or using the browser back/forward controls.
Calling cancel() will prevent the navigation from completing. If navigation.type === 'leave' — meaning the user is navigating away from the app (or closing the tab) — calling cancel will trigger the native browser unload confirmation dialog. In this case, the navigation may or may not be cancelled depending on the user’s response.
When a navigation isn’t to a SvelteKit-owned route (and therefore controlled by SvelteKit’s client-side router), navigation.to.route.id will be null.
If the navigation will (if not cancelled) cause the document to unload — in other words 'leave' navigations and 'link' navigations where navigation.to.route === null — navigation.willUnload is true.
beforeNavigate must be called during a component initialization. It remains active as long as the component is mounted.
beforeNavigate,
	function disableScrollHandling(): voidIf called when the page is being updated following a navigation (in onMount or afterNavigate or an action, for example), this disables SvelteKit’s built-in scroll handling.
This is generally discouraged, since it breaks user expectations.
disableScrollHandling,
	function goto(url: string | URL, opts?: {
    replaceState?: boolean | undefined;
    noScroll?: boolean | undefined;
    keepFocus?: boolean | undefined;
    invalidateAll?: boolean | undefined;
    invalidate?: (string | URL | ((url: URL) => boolean))[] | undefined;
    state?: App.PageState | undefined;
}): Promise<void>Allows you to navigate programmatically to a given route, with options such as keeping the current element focused.
Returns a Promise that resolves when SvelteKit navigates (or fails to navigate, in which case the promise rejects) to the specified url.
For external URLs, use window.location = url instead of calling goto(url).
@paramurl Where to navigate to. Note that if you've set config.kit.paths.base and the URL is root-relative, you need to prepend the base path if you want to navigate within the app.@paramopts Options related to the navigationgoto,
	function invalidate(resource: string | URL | ((url: URL) => boolean)): Promise<void>Causes any load functions belonging to the currently active page to re-run if they depend on the url in question, via fetch or depends. Returns a Promise that resolves when the page is subsequently updated.
If the argument is given as a string or URL, it must resolve to the same URL that was passed to fetch or depends (including query parameters).
To create a custom identifier, use a string beginning with [a-z]+: (e.g. custom:state) — this is a valid URL.
The function argument can be used define a custom predicate. It receives the full URL and causes load to rerun if true is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.
// Example: Match '/path' regardless of the query parameters
import { function invalidate(resource: string | URL | ((url: URL) => boolean)): Promise<void>Causes any load functions belonging to the currently active page to re-run if they depend on the url in question, via fetch or depends. Returns a Promise that resolves when the page is subsequently updated.
If the argument is given as a string or URL, it must resolve to the same URL that was passed to fetch or depends (including query parameters).
To create a custom identifier, use a string beginning with [a-z]+: (e.g. custom:state) — this is a valid URL.
The function argument can be used define a custom predicate. It receives the full URL and causes load to rerun if true is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.
// Example: Match '/path' regardless of the query parameters
import { invalidate } from '$app/navigation';

invalidate((url) => url.pathname === '/path');@paramresource The invalidated URLinvalidate } from '$app/navigation';

function invalidate(resource: string | URL | ((url: URL) => boolean)): Promise<void>Causes any load functions belonging to the currently active page to re-run if they depend on the url in question, via fetch or depends. Returns a Promise that resolves when the page is subsequently updated.
If the argument is given as a string or URL, it must resolve to the same URL that was passed to fetch or depends (including query parameters).
To create a custom identifier, use a string beginning with [a-z]+: (e.g. custom:state) — this is a valid URL.
The function argument can be used define a custom predicate. It receives the full URL and causes load to rerun if true is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.
// Example: Match '/path' regardless of the query parameters
import { invalidate } from '$app/navigation';

invalidate((url) => url.pathname === '/path');@paramresource The invalidated URLinvalidate((url: URLurl) => url: URLurl.URL.pathname: stringMDN Reference
pathname === '/path');@paramresource The invalidated URLinvalidate,
	function invalidateAll(): Promise<void>Causes all load functions belonging to the currently active page to re-run. Returns a Promise that resolves when the page is subsequently updated.
invalidateAll,
	function onNavigate(callback: (navigation: import("@sveltejs/kit").OnNavigate) => MaybePromise<void | (() => void)>): voidA lifecycle function that runs the supplied callback immediately before we navigate to a new URL except during full-page navigations.
If you return a Promise, SvelteKit will wait for it to resolve before completing the navigation. This allows you to — for example — use document.startViewTransition. Avoid promises that are slow to resolve, since navigation will appear stalled to the user.
If a function (or a Promise that resolves to a function) is returned from the callback, it will be called once the DOM has updated.
onNavigate must be called during a component initialization. It remains active as long as the component is mounted.
onNavigate,
	function preloadCode(pathname: string): Promise<void>Programmatically imports the code for routes that haven’t yet been fetched.
Typically, you might call this to speed up subsequent navigation.
You can specify routes by any matching pathname such as /about (to match src/routes/about/+page.svelte) or /blog/* (to match src/routes/blog/[slug]/+page.svelte).
Unlike preloadData, this won’t call load functions.
Returns a Promise that resolves when the modules have been imported.
preloadCode,
	function preloadData(href: string): Promise<{
    type: "loaded";
    status: number;
    data: Record<string, any>;
} | {
    type: "redirect";
    location: string;
}>Programmatically preloads the given page, which means

ensuring that the code for the page is loaded, and
calling the page’s load function with the appropriate options.

This is the same behaviour that SvelteKit triggers when the user taps or mouses over an &#x3C;a> element with data-sveltekit-preload-data.
If the next navigation is to href, the values returned from load will be used, making navigation instantaneous.
Returns a Promise that resolves with the result of running the new route’s load functions once the preload is complete.
@paramhref Page to preloadpreloadData,
	function pushState(url: string | URL, state: App.PageState): voidProgrammatically create a new history entry with the given page.state. To use the current URL, you can pass '' as the first argument. Used for shallow routing.
pushState,
	function refreshAll({ includeLoadFunctions }?: {
    includeLoadFunctions?: boolean;
}): Promise<void>Causes all currently active remote functions to refresh, and all load functions belonging to the currently active page to re-run (unless disabled via the option argument).
Returns a Promise that resolves when the page is subsequently updated.
refreshAll,
	function replaceState(url: string | URL, state: App.PageState): voidProgrammatically replace the current history entry with the given page.state. To use the current URL, you can pass '' as the first argument. Used for shallow routing.
replaceState
} from '$app/navigation';
```

## afterNavigate

A lifecycle function that runs the supplied `callback` when the current component mounts, and also whenever we navigate to a URL.

`afterNavigate` must be called during a component initialization. It remains active as long as the component is mounted.

```
function afterNavigate(
	callback: (
		navigation: import('@sveltejs/kit').AfterNavigate
	) => void
): void;
```

## beforeNavigate

A navigation interceptor that triggers before we navigate to a URL, whether by clicking a link, calling `goto(...)`, or using the browser back/forward controls.

Calling `cancel()` will prevent the navigation from completing. If `navigation.type === 'leave'` — meaning the user is navigating away from the app (or closing the tab) — calling `cancel` will trigger the native browser unload confirmation dialog. In this case, the navigation may or may not be cancelled depending on the user’s response.

When a navigation isn’t to a SvelteKit-owned route (and therefore controlled by SvelteKit’s client-side router), `navigation.to.route.id` will be `null`.

If the navigation will (if not cancelled) cause the document to unload — in other words `'leave'` navigations and `'link'` navigations where `navigation.to.route === null` — `navigation.willUnload` is `true`.

`beforeNavigate` must be called during a component initialization. It remains active as long as the component is mounted.

```
function beforeNavigate(
	callback: (
		navigation: import('@sveltejs/kit').BeforeNavigate
	) => void
): void;
```

## disableScrollHandling

If called when the page is being updated following a navigation (in `onMount` or `afterNavigate` or an action, for example), this disables SvelteKit’s built-in scroll handling.
This is generally discouraged, since it breaks user expectations.

```
function disableScrollHandling(): void;
```

## goto

Allows you to navigate programmatically to a given route, with options such as keeping the current element focused.
Returns a Promise that resolves when SvelteKit navigates (or fails to navigate, in which case the promise rejects) to the specified `url`.

For external URLs, use `window.location = url` instead of calling `goto(url)`.

```
function goto(
	url: string | URL,
	opts?: {
		replaceState?: boolean | undefined;
		noScroll?: boolean | undefined;
		keepFocus?: boolean | undefined;
		invalidateAll?: boolean | undefined;
		invalidate?:
			| (string | URL | ((url: URL) => boolean))[]
			| undefined;
		state?: App.PageState | undefined;
	}
): Promise<void>;
```

## invalidate

Causes any `load` functions belonging to the currently active page to re-run if they depend on the `url` in question, via `fetch` or `depends`. Returns a `Promise` that resolves when the page is subsequently updated.

If the argument is given as a `string` or `URL`, it must resolve to the same URL that was passed to `fetch` or `depends` (including query parameters).
To create a custom identifier, use a string beginning with `[a-z]+:` (e.g. `custom:state`) — this is a valid URL.

The `function` argument can be used define a custom predicate. It receives the full `URL` and causes `load` to rerun if `true` is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.

```
// Example: Match '/path' regardless of the query parameters
import { function invalidate(resource: string | URL | ((url: URL) => boolean)): Promise<void>Causes any load functions belonging to the currently active page to re-run if they depend on the url in question, via fetch or depends. Returns a Promise that resolves when the page is subsequently updated.
If the argument is given as a string or URL, it must resolve to the same URL that was passed to fetch or depends (including query parameters).
To create a custom identifier, use a string beginning with [a-z]+: (e.g. custom:state) — this is a valid URL.
The function argument can be used define a custom predicate. It receives the full URL and causes load to rerun if true is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.
// Example: Match '/path' regardless of the query parameters
import { invalidate } from '$app/navigation';

invalidate((url) => url.pathname === '/path');@paramresource The invalidated URLinvalidate } from '$app/navigation';

function invalidate(resource: string | URL | ((url: URL) => boolean)): Promise<void>Causes any load functions belonging to the currently active page to re-run if they depend on the url in question, via fetch or depends. Returns a Promise that resolves when the page is subsequently updated.
If the argument is given as a string or URL, it must resolve to the same URL that was passed to fetch or depends (including query parameters).
To create a custom identifier, use a string beginning with [a-z]+: (e.g. custom:state) — this is a valid URL.
The function argument can be used define a custom predicate. It receives the full URL and causes load to rerun if true is returned.
This can be useful if you want to invalidate based on a pattern instead of a exact match.
// Example: Match '/path' regardless of the query parameters
import { invalidate } from '$app/navigation';

invalidate((url) => url.pathname === '/path');@paramresource The invalidated URLinvalidate((url: URLurl) => url: URLurl.URL.pathname: stringMDN Reference
pathname === '/path');
```

```
function invalidate(
	resource: string | URL | ((url: URL) => boolean)
): Promise<void>;
```

## invalidateAll

Causes all `load` and `query` functions belonging to the currently active page to re-run. Returns a `Promise` that resolves when the page is subsequently updated.

```
function invalidateAll(): Promise<void>;
```

## onNavigate

A lifecycle function that runs the supplied `callback` immediately before we navigate to a new URL except during full-page navigations.

If you return a `Promise`, SvelteKit will wait for it to resolve before completing the navigation. This allows you to — for example — use `document.startViewTransition`. Avoid promises that are slow to resolve, since navigation will appear stalled to the user.

If a function (or a `Promise` that resolves to a function) is returned from the callback, it will be called once the DOM has updated.

`onNavigate` must be called during a component initialization. It remains active as long as the component is mounted.

```
function onNavigate(
	callback: (
		navigation: import('@sveltejs/kit').OnNavigate
	) => MaybePromise<(() => void) | void>
): void;
```

## preloadCode

Programmatically imports the code for routes that haven’t yet been fetched.
Typically, you might call this to speed up subsequent navigation.

You can specify routes by any matching pathname such as `/about` (to match `src/routes/about/+page.svelte`) or `/blog/*` (to match `src/routes/blog/[slug]/+page.svelte`).

Unlike `preloadData`, this won’t call `load` functions.
Returns a Promise that resolves when the modules have been imported.

```
function preloadCode(pathname: string): Promise<void>;
```

## preloadData

Programmatically preloads the given page, which means

1. ensuring that the code for the page is loaded, and
2. calling the page’s load function with the appropriate options.

This is the same behaviour that SvelteKit triggers when the user taps or mouses over an `<a>` element with `data-sveltekit-preload-data`.
If the next navigation is to `href`, the values returned from load will be used, making navigation instantaneous.
Returns a Promise that resolves with the result of running the new route’s `load` functions once the preload is complete.

```
function preloadData(href: string): Promise<
	| {
			type: 'loaded';
			status: number;
			data: Record<string, any>;
	  }
	| {
			type: 'redirect';
			location: string;
	  }
>;
```

## pushState

Programmatically create a new history entry with the given `page.state`. To use the current URL, you can pass `''` as the first argument. Used for [shallow routing](https://kit.svelte.dev/docs/kit/shallow-routing).

```
function pushState(
	url: string | URL,
	state: App.PageState
): void;
```

## refreshAll

Causes all currently active remote functions to refresh, and all `load` functions belonging to the currently active page to re-run (unless disabled via the option argument).
Returns a `Promise` that resolves when the page is subsequently updated.

```
function refreshAll({
	includeLoadFunctions
}?: {
	includeLoadFunctions?: boolean;
}): Promise<void>;
```

## replaceState

Programmatically replace the current history entry with the given `page.state`. To use the current URL, you can pass `''` as the first argument. Used for [shallow routing](https://kit.svelte.dev/docs/kit/shallow-routing).

```
function replaceState(
	url: string | URL,
	state: App.PageState
): void;
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/20-$app-navigation.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$app-navigation/llms.txt)]

 previous next [[$app/forms](https://kit.svelte.dev/docs/kit/$app-forms)] [[$app/paths](https://kit.svelte.dev/docs/kit/$app-paths)]

---

# $app/server

> $app/server • SvelteKit documentation

```
import {
	function command<Output>(fn: () => Output): RemoteCommand<void, Output> (+2 overloads)Creates a remote command. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27command,
	function form<Output>(fn: () => MaybePromise<Output>): RemoteForm<void, Output> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form,
	function getRequestEvent(): RequestEventReturns the current RequestEvent. Can be used inside server hooks, server load functions, actions, and endpoints (and functions called by them).
In environments without AsyncLocalStorage, this must be called synchronously (i.e. not after an await).
@since2.20.0getRequestEvent,
	function prerender<Output>(fn: () => MaybePromise<Output>, options?: {
    inputs?: RemotePrerenderInputsGenerator<void>;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<void, Output> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender,
	function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query,
	function read(asset: string): ResponseRead the contents of an imported asset from the filesystem
@examplejs import { read } from '$app/server'; import somefile from './somefile.txt';  const asset = read(somefile); const text = await asset.text(); @since2.4.0read
} from '$app/server';
```

## command

> Available since 2.27

Creates a remote command. When called from the browser, the function will be invoked on the server via a `fetch` call.

See [Remote functions](https://kit.svelte.dev/docs/kit/remote-functions#command) for full documentation.

```
function command<Output>(
	fn: () => Output
): RemoteCommand<void, Output>;
```

```
function command<Input, Output>(
	validate: 'unchecked',
	fn: (arg: Input) => Output
): RemoteCommand<Input, Output>;
```

```
function command<Schema extends StandardSchemaV1, Output>(
	validate: Schema,
	fn: (arg: StandardSchemaV1.InferOutput<Schema>) => Output
): RemoteCommand<
	StandardSchemaV1.InferInput<Schema>,
	Output
>;
```

## form

> Available since 2.27

Creates a form object that can be spread onto a `<form>` element.

See [Remote functions](https://kit.svelte.dev/docs/kit/remote-functions#form) for full documentation.

```
function form<Output>(
	fn: () => MaybePromise<Output>
): RemoteForm<void, Output>;
```

```
function form<Input extends RemoteFormInput, Output>(
	validate: 'unchecked',
	fn: (
		data: Input,
		issue: InvalidField<Input>
	) => MaybePromise<Output>
): RemoteForm<Input, Output>;
```

```
function form<
	Schema extends StandardSchemaV1<
		RemoteFormInput,
		Record<string, any>
	>,
	Output
>(
	validate: Schema,
	fn: (
		data: StandardSchemaV1.InferOutput<Schema>,
		issue: InvalidField<StandardSchemaV1.InferInput<Schema>>
	) => MaybePromise<Output>
): RemoteForm<StandardSchemaV1.InferInput<Schema>, Output>;
```

## getRequestEvent

> Available since 2.20.0

Returns the current `RequestEvent`. Can be used inside server hooks, server `load` functions, actions, and endpoints (and functions called by them).

In environments without [AsyncLocalStorage](https://nodejs.org/api/async_context.html#class-asynclocalstorage), this must be called synchronously (i.e. not after an `await`).

```
function getRequestEvent(): RequestEvent;
```

## prerender

> Available since 2.27

Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a `fetch` call.

See [Remote functions](https://kit.svelte.dev/docs/kit/remote-functions#prerender) for full documentation.

```
function prerender<Output>(
	fn: () => MaybePromise<Output>,
	options?:
		| {
				inputs?: RemotePrerenderInputsGenerator<void>;
				dynamic?: boolean;
		  }
		| undefined
): RemotePrerenderFunction<void, Output>;
```

```
function prerender<Input, Output>(
	validate: 'unchecked',
	fn: (arg: Input) => MaybePromise<Output>,
	options?:
		| {
				inputs?: RemotePrerenderInputsGenerator<Input>;
				dynamic?: boolean;
		  }
		| undefined
): RemotePrerenderFunction<Input, Output>;
```

```
function prerender<Schema extends StandardSchemaV1, Output>(
	schema: Schema,
	fn: (
		arg: StandardSchemaV1.InferOutput<Schema>
	) => MaybePromise<Output>,
	options?:
		| {
				inputs?: RemotePrerenderInputsGenerator<
					StandardSchemaV1.InferInput<Schema>
				>;
				dynamic?: boolean;
		  }
		| undefined
): RemotePrerenderFunction<
	StandardSchemaV1.InferInput<Schema>,
	Output
>;
```

## query

> Available since 2.27

Creates a remote query. When called from the browser, the function will be invoked on the server via a `fetch` call.

See [Remote functions](https://kit.svelte.dev/docs/kit/remote-functions#query) for full documentation.

```
function query<Output>(
	fn: () => MaybePromise<Output>
): RemoteQueryFunction<void, Output>;
```

```
function query<Input, Output>(
	validate: 'unchecked',
	fn: (arg: Input) => MaybePromise<Output>
): RemoteQueryFunction<Input, Output>;
```

```
function query<Schema extends StandardSchemaV1, Output>(
	schema: Schema,
	fn: (
		arg: StandardSchemaV1.InferOutput<Schema>
	) => MaybePromise<Output>
): RemoteQueryFunction<
	StandardSchemaV1.InferInput<Schema>,
	Output
>;
```

## read

> Available since 2.4.0

Read the contents of an imported asset from the filesystem

```
import { function read(asset: string): ResponseRead the contents of an imported asset from the filesystem
@examplejs import { read } from '$app/server'; import somefile from './somefile.txt';  const asset = read(somefile); const text = await asset.text(); @since2.4.0read } from '$app/server';
import const somefile: stringsomefile from './somefile.txt';

const const asset: Responseasset = function read(asset: string): ResponseRead the contents of an imported asset from the filesystem
@examplejs import { read } from '$app/server'; import somefile from './somefile.txt';  const asset = read(somefile); const text = await asset.text(); @since2.4.0read(const somefile: stringsomefile);
const const text: stringtext = await const asset: Responseasset.Body.text(): Promise<string>MDN Reference
text();
```

```
function read(asset: string): Response;
```

## query

```
namespace query {
	/**
	 * Creates a batch query function that collects multiple calls and executes them in a single request
	 *
	 * See [Remote functions](https://svelte.dev/docs/kit/remote-functions#query.batch) for full documentation.
	 *
	 * @since 2.35
	 */
	function batch<Input, Output>(
		validate: 'unchecked',
		fn: (
			args: Input[]
		) => MaybePromise<(arg: Input, idx: number) => Output>
	): RemoteQueryFunction<Input, Output>;
	/**
	 * Creates a batch query function that collects multiple calls and executes them in a single request
	 *
	 * See [Remote functions](https://svelte.dev/docs/kit/remote-functions#query.batch) for full documentation.
	 *
	 * @since 2.35
	 */
	function batch<Schema extends StandardSchemaV1, Output>(
		schema: Schema,
		fn: (
			args: StandardSchemaV1.InferOutput<Schema>[]
		) => MaybePromise<
			(
				arg: StandardSchemaV1.InferOutput<Schema>,
				idx: number
			) => Output
		>
	): RemoteQueryFunction<
		StandardSchemaV1.InferInput<Schema>,
		Output
	>;
}
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/20-$app-server.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$app-server/llms.txt)]

 previous next [[$app/paths](https://kit.svelte.dev/docs/kit/$app-paths)] [[$app/state](https://kit.svelte.dev/docs/kit/$app-state)]

---

# $app/state

> $app/state • SvelteKit documentation

SvelteKit makes three read-only state objects available via the `$app/state` module — `page`, `navigating` and `updated`.

> This module was added in 2.12. If you’re using an earlier version of SvelteKit, use [$app/stores](https://kit.svelte.dev/docs/$app-stores) instead.

```
import { const navigating: Navigation | {
    from: null;
    to: null;
    type: null;
    willUnload: null;
    delta: null;
    complete: null;
}A read-only object representing an in-progress navigation, with from, to, type and (if type === 'popstate') delta properties.
Values are null when no navigation is occurring, or during server rendering.
navigating, const page: Page<Record<string, string>, string | null>A read-only reactive object with information about the current page, serving several use cases:

retrieving the combined data of all pages/layouts anywhere in your component tree (also see loading data)
retrieving the current value of the form prop anywhere in your component tree (also see form actions)
retrieving the page state that was set through goto, pushState or replaceState (also see goto and shallow routing)
retrieving metadata such as the URL you’re on, the current route and its parameters, and whether or not there was an error

&#x3C;! file: +layout.svelte >
&#x3C;script>
	import { page } from '$app/state';
&#x3C;/script>

&#x3C;p>Currently at {page.url.pathname}&#x3C;/p>

{#if page.error}
	&#x3C;span class="red">Problem detected&#x3C;/span>
{:else}
	&#x3C;span class="small">All systems operational&#x3C;/span>
{/if}Changes to page are available exclusively with runes. (The legacy reactivity syntax will not reflect any changes)
&#x3C;! file: +page.svelte >
&#x3C;script>
	import { page } from '$app/state';
	const id = $derived(page.params.id); // This will correctly update id for usage on this page
	$: badId = page.params.id; // Do not use; will never update after initial load
&#x3C;/script>On the server, values can only be read during rendering (in other words not in e.g. load functions). In the browser, the values can be read at any time.
page, const updated: {
    readonly current: boolean;
    check(): Promise<boolean>;
}A read-only reactive value that’s initially false. If version.pollInterval is a non-zero value, SvelteKit will poll for new versions of the app and update current to true when it detects one. updated.check() will force an immediate check, regardless of polling.
updated } from '$app/state';
```

## navigating

A read-only object representing an in-progress navigation, with `from`, `to`, `type` and (if `type === 'popstate'`) `delta` properties.
Values are `null` when no navigation is occurring, or during server rendering.

```
const navigating:
	| import('@sveltejs/kit').Navigation
	| {
			from: null;
			to: null;
			type: null;
			willUnload: null;
			delta: null;
			complete: null;
	  };
```

## page

A read-only reactive object with information about the current page, serving several use cases:

- retrieving the combined `data` of all pages/layouts anywhere in your component tree (also see [loading data](https://kit.svelte.dev/docs/kit/load))
- retrieving the current value of the `form` prop anywhere in your component tree (also see [form actions](https://kit.svelte.dev/docs/kit/form-actions))
- retrieving the page state that was set through `goto`, `pushState` or `replaceState` (also see [goto](https://kit.svelte.dev/docs/kit/$app-navigation#goto) and [shallow routing](https://kit.svelte.dev/docs/kit/shallow-routing))
- retrieving metadata such as the URL you’re on, the current route and its parameters, and whether or not there was an error

 +layout

```
<script>
	import { page } from '$app/state';
</script>

<p>Currently at {page.url.pathname}</p>

{#if page.error}
	<span class="red">Problem detected</span>
{:else}
	<span class="small">All systems operational</span>
{/if}
```

```
<script lang="ts">
	import { page } from '$app/state';
</script>

<p>Currently at {page.url.pathname}</p>

{#if page.error}
	<span class="red">Problem detected</span>
{:else}
	<span class="small">All systems operational</span>
{/if}
```

Changes to `page` are available exclusively with runes. (The legacy reactivity syntax will not reflect any changes)

 +page

```
<script>
	import { page } from '$app/state';
	const id = $derived(page.params.id); // This will correctly update id for usage on this page
	$: badId = page.params.id; // Do not use; will never update after initial load
</script>
```

```
<script lang="ts">
	import { page } from '$app/state';
	const id = $derived(page.params.id); // This will correctly update id for usage on this page
	$: badId = page.params.id; // Do not use; will never update after initial load
</script>
```

On the server, values can only be read during rendering (in other words *not* in e.g. `load` functions). In the browser, the values can be read at any time.

```
const page: import('@sveltejs/kit').Page;
```

## updated

A read-only reactive value that’s initially `false`. If [version.pollInterval](https://kit.svelte.dev/docs/kit/configuration#version) is a non-zero value, SvelteKit will poll for new versions of the app and update `current` to `true` when it detects one. `updated.check()` will force an immediate check, regardless of polling.

```
const updated: {
	get current(): boolean;
	check(): Promise<boolean>;
};
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/20-$app-state.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$app-state/llms.txt)]

 previous next [[$app/server](https://kit.svelte.dev/docs/kit/$app-server)] [[$app/stores](https://kit.svelte.dev/docs/kit/$app-stores)]

---

# $app/stores

> $app/stores • SvelteKit documentation

This module contains store-based equivalents of the exports from [$app/state](https://kit.svelte.dev/docs/$app-state). If you’re using SvelteKit 2.12 or later, use that module instead.

```
import { function getStores(): {
    page: typeof page;
    navigating: typeof navigating;
    updated: typeof updated;
}getStores, const navigating: Readable<Navigation | null>A readable store.
When navigating starts, its value is a Navigation object with from, to, type and (if type === 'popstate') delta properties.
When navigating finishes, its value reverts to null.
On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.
@deprecatedUse navigating from $app/state instead (requires Svelte 5, see docs for more info)navigating, const page: Readable<Page<Record<string, string>, string | null>>A readable store whose value contains page data.
On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.
@deprecatedUse page from $app/state instead (requires Svelte 5, see docs for more info)page, const updated: Readable<boolean> & {
    check(): Promise<boolean>;
}A readable store whose initial value is false. If version.pollInterval is a non-zero value, SvelteKit will poll for new versions of the app and update the store value to true when it detects one. updated.check() will force an immediate check, regardless of polling.
On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.
@deprecatedUse updated from $app/state instead (requires Svelte 5, see docs for more info)updated } from '$app/stores';
```

## getStores

```
function getStores(): {
	page: typeof page;

	navigating: typeof navigating;

	updated: typeof updated;
};
```

## navigating

> Use `navigating` from `$app/state` instead (requires Svelte 5, [see docs for more info](https://kit.svelte.dev/docs/kit/migrating-to-sveltekit-2#SvelteKit-2.12:-$app-stores-deprecated))

A readable store.
When navigating starts, its value is a `Navigation` object with `from`, `to`, `type` and (if `type === 'popstate'`) `delta` properties.
When navigating finishes, its value reverts to `null`.

On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.

```
const navigating: import('svelte/store').Readable<
	import('@sveltejs/kit').Navigation | null
>;
```

## page

> Use `page` from `$app/state` instead (requires Svelte 5, [see docs for more info](https://kit.svelte.dev/docs/kit/migrating-to-sveltekit-2#SvelteKit-2.12:-$app-stores-deprecated))

A readable store whose value contains page data.

On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.

```
const page: import('svelte/store').Readable<
	import('@sveltejs/kit').Page
>;
```

## updated

> Use `updated` from `$app/state` instead (requires Svelte 5, [see docs for more info](https://kit.svelte.dev/docs/kit/migrating-to-sveltekit-2#SvelteKit-2.12:-$app-stores-deprecated))

A readable store whose initial value is `false`. If [version.pollInterval](https://kit.svelte.dev/docs/kit/configuration#version) is a non-zero value, SvelteKit will poll for new versions of the app and update the store value to `true` when it detects one. `updated.check()` will force an immediate check, regardless of polling.

On the server, this store can only be subscribed to during component initialization. In the browser, it can be subscribed to at any time.

```
const updated: import('svelte/store').Readable<boolean> & {
	check(): Promise<boolean>;
};
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/20-$app-stores.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$app-stores/llms.txt)]

 previous next [[$app/state](https://kit.svelte.dev/docs/kit/$app-state)] [[$app/types](https://kit.svelte.dev/docs/kit/$app-types)]

---

# $env/dynamic/private

> $env/dynamic/private • SvelteKit documentation

This module provides access to runtime environment variables, as defined by the platform you’re running on. For example if you’re using [adapter-node](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [vite preview](https://kit.svelte.dev/docs/kit/cli)), this is equivalent to `process.env`. This module only includes variables that *do not* begin with [config.kit.env.publicPrefix](https://kit.svelte.dev/docs/kit/configuration#env) *and do* start with [config.kit.env.privatePrefix](https://kit.svelte.dev/docs/kit/configuration#env) (if configured).

This module cannot be imported into client-side code.

```
import { import envenv } from '$env/dynamic/private';
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
@sincev0.1.100log(import envenv.DEPLOYMENT_SPECIFIC_VARIABLE);
```

> In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/25-$env-dynamic-private.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$env-dynamic-private/llms.txt)]

 previous next [[$app/types](https://kit.svelte.dev/docs/kit/$app-types)] [[$env/dynamic/public](https://kit.svelte.dev/docs/kit/$env-dynamic-public)]

---

# $env/static/private

> $env/static/private • SvelteKit documentation

Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [$env/dynamic/private](https://kit.svelte.dev/docs/kit/$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that *do not* begin with [config.kit.env.publicPrefix](https://kit.svelte.dev/docs/kit/configuration#env) *and do* start with [config.kit.env.privatePrefix](https://kit.svelte.dev/docs/kit/configuration#env) (if configured).

*Unlike* [$env/dynamic/private](https://kit.svelte.dev/docs/kit/$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.

```
import { import API_KEYAPI_KEY } from '$env/static/private';
```

Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don’t have a value until the app is deployed:

```
MY_FEATURE_FLAG=""
```

You can override `.env` values from the command line like so:

```
MY_FEATURE_FLAG="enabled" npm run dev
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/25-$env-static-private.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$env-static-private/llms.txt)]

 previous next [[$env/dynamic/public](https://kit.svelte.dev/docs/kit/$env-dynamic-public)] [[$env/static/public](https://kit.svelte.dev/docs/kit/$env-static-public)]

---

# $lib

> $lib • SvelteKit documentation

SvelteKit automatically makes files under `src/lib` available using the `$lib` import alias.

 src/lib/Component

```
A reusable component
```

src/routes/+page

```
<script>
	import Component from '$lib/Component.svelte';
</script>

<Component />
```

```
<script lang="ts">
	import Component from '$lib/Component.svelte';
</script>

<Component />
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/26-$lib.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$lib/llms.txt)]

 previous next [[$env/static/public](https://kit.svelte.dev/docs/kit/$env-static-public)] [[$service-worker](https://kit.svelte.dev/docs/kit/$service-worker)]

---

# $service

> $service-worker • SvelteKit documentation

```
import { const base: stringThe base path of the deployment. Typically this is equivalent to config.kit.paths.base, but it is calculated from location.pathname meaning that it will continue to work correctly if the site is deployed to a subdirectory.
Note that there is a base but no assets, since service workers cannot be used if config.kit.paths.assets is specified.
base, const build: string[]An array of URL strings representing the files generated by Vite, suitable for caching with cache.addAll(build).
During development, this is an empty array.
build, const files: string[]An array of URL strings representing the files in your static directory, or whatever directory is specified by config.kit.files.assets. You can customize which files are included from static directory using config.kit.serviceWorker.files
files, const prerendered: string[]An array of pathnames corresponding to prerendered pages and endpoints.
During development, this is an empty array.
prerendered, const version: stringSee config.kit.version. It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.
version } from '$service-worker';
```

This module is only available to [service workers](https://kit.svelte.dev/docs/kit/service-workers).

## base

The `base` path of the deployment. Typically this is equivalent to `config.kit.paths.base`, but it is calculated from `location.pathname` meaning that it will continue to work correctly if the site is deployed to a subdirectory.
Note that there is a `base` but no `assets`, since service workers cannot be used if `config.kit.paths.assets` is specified.

```
const base: string;
```

## build

An array of URL strings representing the files generated by Vite, suitable for caching with `cache.addAll(build)`.
During development, this is an empty array.

```
const build: string[];
```

## files

An array of URL strings representing the files in your static directory, or whatever directory is specified by `config.kit.files.assets`. You can customize which files are included from `static` directory using [config.kit.serviceWorker.files](https://kit.svelte.dev/docs/kit/configuration#serviceWorker)

```
const files: string[];
```

## prerendered

An array of pathnames corresponding to prerendered pages and endpoints.
During development, this is an empty array.

```
const prerendered: string[];
```

## version

See [config.kit.version](https://kit.svelte.dev/docs/kit/configuration#version). It’s useful for generating unique cache names inside your service worker, so that a later deployment of your app can invalidate old caches.

```
const version: string;
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/98-reference/27-$service-worker.md) [[llms.txt](https://kit.svelte.dev/docs/kit/$service-worker/llms.txt)]

 previous next [[$lib](https://kit.svelte.dev/docs/kit/$lib)] [[Configuration](https://kit.svelte.dev/docs/kit/configuration)]
