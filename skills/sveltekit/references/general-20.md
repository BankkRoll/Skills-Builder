# Shallow routing and more

# Shallow routing

> Shallow routing • SvelteKit documentation

As you navigate around a SvelteKit app, you create *history entries*. Clicking the back and forward buttons traverses through this list of entries, re-running any `load` functions and replacing page components as necessary.

Sometimes, it’s useful to create history entries *without* navigating. For example, you might want to show a modal dialog that the user can dismiss by navigating back. This is particularly valuable on mobile devices, where swipe gestures are often more natural than interacting directly with the UI. In these cases, a modal that is *not* associated with a history entry can be a source of frustration, as a user may swipe backwards in an attempt to dismiss it and find themselves on the wrong page.

SvelteKit makes this possible with the [pushState](https://kit.svelte.dev/docs/$app-navigation#pushState) and [replaceState](https://kit.svelte.dev/docs/$app-navigation#replaceState) functions, which allow you to associate state with a history entry without navigating. For example, to implement a history-driven modal:

 +page

```
<script>
	import { pushState } from '$app/navigation';
	import { page } from '$app/state';
	import Modal from './Modal.svelte';

	function showModal() {
		pushState('', {
			showModal: true
		});
	}
</script>

{#if page.state.showModal}
	<Modal close={() => history.back()} />
{/if}
```

```
<script lang="ts">
	import { pushState } from '$app/navigation';
	import { page } from '$app/state';
	import Modal from './Modal.svelte';

	function showModal() {
		pushState('', {
			showModal: true
		});
	}
</script>

{#if page.state.showModal}
	<Modal close={() => history.back()} />
{/if}
```

The modal can be dismissed by navigating back (unsetting `page.state.showModal`) or by interacting with it in a way that causes the `close` callback to run, which will navigate back programmatically.

## API

The first argument to `pushState` is the URL, relative to the current URL. To stay on the current URL, use `''`.

The second argument is the new page state, which can be accessed via the [page object](https://kit.svelte.dev/docs/$app-state#page) as `page.state`. You can make page state type-safe by declaring an [App.PageState](https://kit.svelte.dev/docs/types#PageState) interface (usually in `src/app.d.ts`).

To set page state without creating a new history entry, use `replaceState` instead of `pushState`.

> Legacy mode
>
> `page.state` from `$app/state` was added in SvelteKit 2.12. If you’re using an earlier version or are using Svelte 4, use `$page.state` from `$app/stores` instead.

## Loading data for a route

When shallow routing, you may want to render another `+page.svelte` inside the current page. For example, clicking on a photo thumbnail could pop up the detail view without navigating to the photo page.

For this to work, you need to load the data that the `+page.svelte` expects. A convenient way to do this is to use [preloadData](https://kit.svelte.dev/docs/$app-navigation#preloadData) inside the `click` handler of an `<a>` element. If the element (or a parent) uses [data-sveltekit-preload-data](https://kit.svelte.dev/docs/link-options#data-sveltekit-preload-data), the data will have already been requested, and `preloadData` will reuse that request.

 src/routes/photos/+page

```
<script>
	import { preloadData, pushState, goto } from '$app/navigation';
	import { page } from '$app/state';
	import Modal from './Modal.svelte';
	import PhotoPage from './[id]/+page.svelte';

	let { data } = $props();
</script>

{#each data.thumbnails as thumbnail}
	<a
		href="/photos/{thumbnail.id}"
		onclick={async (e) => {
			if (innerWidth < 640        // bail if the screen is too small
				|| e.shiftKey             // or the link is opened in a new window
				|| e.metaKey || e.ctrlKey // or a new tab (mac: metaKey, win/linux: ctrlKey)
				// should also consider clicking with a mouse scroll wheel
			) return;

			// prevent navigation
			e.preventDefault();

			const { href } = e.currentTarget;

			// run `load` functions (or rather, get the result of the `load` functions
			// that are already running because of `data-sveltekit-preload-data`)
			const result = await preloadData(href);

			if (result.type === 'loaded' && result.status === 200) {
				pushState(href, { selected: result.data });
			} else {
				// something bad happened! try navigating
				goto(href);
			}
		}}
	>
		<img alt={thumbnail.alt} src={thumbnail.src} />
	</a>
{/each}

{#if page.state.selected}
	<Modal onclose={() => history.back()}>
		
		<PhotoPage data={page.state.selected} />
	</Modal>
{/if}
```

```
<script lang="ts">
	import { preloadData, pushState, goto } from '$app/navigation';
	import { page } from '$app/state';
	import Modal from './Modal.svelte';
	import PhotoPage from './[id]/+page.svelte';

	let { data } = $props();
</script>

{#each data.thumbnails as thumbnail}
	<a
		href="/photos/{thumbnail.id}"
		onclick={async (e) => {
			if (innerWidth < 640        // bail if the screen is too small
				|| e.shiftKey             // or the link is opened in a new window
				|| e.metaKey || e.ctrlKey // or a new tab (mac: metaKey, win/linux: ctrlKey)
				// should also consider clicking with a mouse scroll wheel
			) return;

			// prevent navigation
			e.preventDefault();

			const { href } = e.currentTarget;

			// run `load` functions (or rather, get the result of the `load` functions
			// that are already running because of `data-sveltekit-preload-data`)
			const result = await preloadData(href);

			if (result.type === 'loaded' && result.status === 200) {
				pushState(href, { selected: result.data });
			} else {
				// something bad happened! try navigating
				goto(href);
			}
		}}
	>
		<img alt={thumbnail.alt} src={thumbnail.src} />
	</a>
{/each}

{#if page.state.selected}
	<Modal onclose={() => history.back()}>
		
		<PhotoPage data={page.state.selected} />
	</Modal>
{/if}
```

## Caveats

During server-side rendering, `page.state` is always an empty object. The same is true for the first page the user lands on — if the user reloads the page (or returns from another document), state will *not* be applied until they navigate.

Shallow routing is a feature that requires JavaScript to work. Be mindful when using it and try to think of sensible fallback behavior in case JavaScript isn’t available.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/67-shallow-routing.md) [[llms.txt](https://kit.svelte.dev/docs/kit/shallow-routing/llms.txt)]

 previous next [[Snapshots](https://kit.svelte.dev/docs/kit/snapshots)] [[Observability](https://kit.svelte.dev/docs/kit/observability)]

---

# Single

> Single-page apps • SvelteKit documentation

You can turn a SvelteKit app into a fully client-rendered single-page app (SPA) by specifying a *fallback page*. This page will be served for any URLs that can’t be served by other means such as returning a prerendered page.

> SPA mode has a large negative performance impact by forcing multiple network round trips (for the blank HTML document, then for the JavaScript, and then for any data needed for the page) before content can be shown. Unless you are serving the app from a local network (e.g. a mobile app that wraps a locally-served SPA) this will delay startup, especially when considering the latency of mobile devices. It also harms SEO by often causing sites to be downranked for performance (SPAs are much more likely to fail [Core Web Vitals](https://web.dev/explore/learn-core-web-vitals)), excluding search engines that don’t render JS, and causing your site to receive less frequent updates from those that do. And finally, it makes your app inaccessible to users if JavaScript fails or is disabled (which happens [more often than you probably think](https://kryogenix.org/code/browser/everyonehasjs.html)).
>
>
>
> You can avoid these drawbacks by [prerendering](#Prerendering-individual-pages) as many pages as possible when using SPA mode (especially your homepage). If you can prerender all pages, you can simply use [static site generation](https://kit.svelte.dev/docs/adapter-static) rather than a SPA. Otherwise, you should strongly consider using an adapter which supports server side rendering. SvelteKit has officially supported adapters for various providers with generous free tiers.

## Usage

First, disable SSR for the pages you don’t want to prerender. These pages will be served via the fallback page; for example, to serve all pages via the fallback by default, you can update the root layout as shown below. You should [opt back into prerendering individual pages and directories](#Prerendering-individual-pages) where possible.

 src/routes/+layout

```
export const const ssr: falsessr = false;
```

If you don’t have any server-side logic (i.e. `+page.server.js`, `+layout.server.js` or `+server.js` files) you can use [adapter-static](https://kit.svelte.dev/docs/adapter-static) to create your SPA. Install `adapter-static` with `npm i -D @sveltejs/adapter-static` and add it to your `svelte.config.js` with the `fallback` option:

 svelte.config

```
import import adapteradapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    adapter: any;
}kit: {
		adapter: anyadapter: import adapteradapter({
			fallback: stringfallback: '200.html' // may differ from host to host
		})
	}
};

export default const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config;
```

The `fallback` page is an HTML page created by SvelteKit from your page template (e.g. `app.html`) that loads your app and navigates to the correct route. For example [Surge](https://surge.sh/help/adding-a-200-page-for-client-side-routing), a static web host, lets you add a `200.html` file that will handle any requests that don’t correspond to static assets or prerendered pages.

On some hosts it may be something else entirely — consult your platform’s documentation. We recommend avoiding `index.html` if possible as it may conflict with prerendering.

> Note that the fallback page will always contain absolute asset paths (i.e. beginning with `/` rather than `.`) regardless of the value of [paths.relative](https://kit.svelte.dev/docs/configuration#paths), since it is used to respond to requests for arbitrary paths.

## Prerendering individual pages

If you want certain pages to be prerendered, you can re-enable `ssr` alongside `prerender` for just those parts of your app:

 src/routes/my-prerendered-page/+page

```
export const const prerender: trueprerender = true;
export const const ssr: truessr = true;
```

You won’t need a Node server or server capable of running JavaScript to deploy this page. It will only server render your page while building your project for the purposes of outputting an `.html` page that can be served from any static web host.

## Apache

To run an SPA on [Apache](https://httpd.apache.org/), you should add a `static/.htaccess` file to route requests to the fallback page:

```
<IfModule mod_rewrite.c>
	RewriteEngine On
	RewriteBase /
	RewriteRule ^200\.html$ - [L]
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule . /200.html [L]
</IfModule>
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/25-build-and-deploy/55-single-page-apps.md) [[llms.txt](https://kit.svelte.dev/docs/kit/single-page-apps/llms.txt)]

 previous next [[Static site generation](https://kit.svelte.dev/docs/kit/adapter-static)] [[Cloudflare](https://kit.svelte.dev/docs/kit/adapter-cloudflare)]

---

# Not found!

[! [[

# Not found!

If you were expecting to find something here, please drop by the [Discord chatroom](https://kit.svelte.dev/chat) and let us know, or raise an issue on [GitHub](https://github.com/sveltejs/svelte.dev/issues). Thanks!

]] ]
