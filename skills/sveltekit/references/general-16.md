# Page options and more

# Page options

> Page options • SvelteKit documentation

By default, SvelteKit will render (or [prerender](https://kit.svelte.dev/docs/glossary#Prerendering)) any component first on the server and send it to the client as HTML. It will then render the component again in the browser to make it interactive in a process called [hydration](https://kit.svelte.dev/docs/glossary#Hydration). For this reason, you need to ensure that components can run in both places. SvelteKit will then initialize a [router](https://kit.svelte.dev/docs/routing) that takes over subsequent navigations.

You can control each of these on a page-by-page basis by exporting options from [+page.js](https://kit.svelte.dev/docs/routing#page-page.js) or [+page.server.js](https://kit.svelte.dev/docs/routing#page-page.server.js), or for groups of pages using a shared [+layout.js](https://kit.svelte.dev/docs/routing#layout-layout.js) or [+layout.server.js](https://kit.svelte.dev/docs/routing#layout-layout.server.js). To define an option for the whole app, export it from the root layout. Child layouts and pages override values set in parent layouts, so — for example — you can enable prerendering for your entire app then disable it for pages that need to be dynamically rendered.

You can mix and match these options in different areas of your app. For example, you could prerender your marketing page for maximum speed, server-render your dynamic pages for SEO and accessibility and turn your admin section into an SPA by rendering it on the client only. This makes SvelteKit very versatile.

## prerender

It’s likely that at least some routes of your app can be represented as a simple HTML file generated at build time. These routes can be [prerendered](https://kit.svelte.dev/docs/glossary#Prerendering).

 +page.js/+page.server.js/+server

```
export const const prerender: trueprerender = true;
```

Alternatively, you can set `export const prerender = true` in your root `+layout.js` or `+layout.server.js` and prerender everything except pages that are explicitly marked as *not* prerenderable:

 +page.js/+page.server.js/+server

```
export const const prerender: falseprerender = false;
```

Routes with `prerender = true` will be excluded from manifests used for dynamic SSR, making your server (or serverless/edge functions) smaller. In some cases you might want to prerender a route but also include it in the manifest (for example, with a route like `/blog/[slug]` where you want to prerender your most recent/popular content but server-render the long tail) — for these cases, there’s a third option, ‘auto’:

 +page.js/+page.server.js/+server

```
export const const prerender: "auto"prerender = 'auto';
```

> If your entire app is suitable for prerendering, you can use [adapter-static](https://kit.svelte.dev/docs/adapter-static), which will output files suitable for use with any static webserver.

The prerenderer will start at the root of your app and generate files for any prerenderable pages or `+server.js` routes it finds. Each page is scanned for `<a>` elements that point to other pages that are candidates for prerendering — because of this, you generally don’t need to specify which pages should be accessed. If you *do* need to specify which pages should be accessed by the prerenderer, you can do so with [config.kit.prerender.entries](https://kit.svelte.dev/docs/configuration#prerender), or by exporting an [entries](#entries) function from your dynamic route.

While prerendering, the value of `building` imported from [$app/environment](https://kit.svelte.dev/docs/$app-environment) will be `true`.

### Prerendering server routes

Unlike the other page options, `prerender` also applies to `+server.js` files. These files are *not* affected by layouts, but will inherit default values from the pages that fetch data from them, if any. For example if a `+page.js` contains this `load` function...

 +page

```
export const const prerender: trueprerender = true;

/** @type {import('./$types').PageLoad} */
export async function function load({ fetch }: {
    fetch: any;
}): Promise<any>@type{import('./$types').PageLoad}load({ fetch: anyfetch }) {
	const const res: anyres = await fetch: anyfetch('/my-server-route.json');
	return await const res: anyres.json();
}
```

```
import type { type PageLoad = (event: Kit.LoadEvent<Record<string, any>, Record<string, any> | null, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>
type PageLoad = (event: Kit.LoadEvent<Record<string, any>, Record<string, any> | null, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>PageLoad } from './$types';
export const const prerender: trueprerender = true;

export const const load: PageLoadload: type PageLoad = (event: Kit.LoadEvent<Record<string, any>, Record<string, any> | null, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>
type PageLoad = (event: Kit.LoadEvent<Record<string, any>, Record<string, any> | null, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>PageLoad = async ({ fetch: {
    (input: RequestInfo | URL, init?: RequestInit): Promise<Response>;
    (input: string | URL | globalThis.Request, init?: RequestInit): Promise<Response>;
}fetch is equivalent to the native fetch web API, with a few additional features:

It can be used to make credentialed requests on the server, as it inherits the cookie and authorization headers for the page request.
It can make relative requests on the server (ordinarily, fetch requires a URL with an origin when used in a server context).
Internal requests (e.g. for +server.js routes) go directly to the handler function when running on the server, without the overhead of an HTTP call.
During server-side rendering, the response will be captured and inlined into the rendered HTML by hooking into the text and json methods of the Response object. Note that headers will not be serialized, unless explicitly included via filterSerializedResponseHeaders
During hydration, the response will be read from the HTML, guaranteeing consistency and preventing an additional network request.

You can learn more about making credentialed requests with cookies here
fetch }) => {
	const const res: Responseres = await fetch: (input: string | URL | globalThis.Request, init?: RequestInit) => Promise<Response> (+1 overload)MDN Reference
fetch('/my-server-route.json');
	return await const res: Responseres.Body.json(): Promise<any>MDN Reference
json();
};
```

...then `src/routes/my-server-route.json/+server.js` will be treated as prerenderable if it doesn’t contain its own `export const prerender = false`.

### When not to prerender

The basic rule is this: for a page to be prerenderable, any two users hitting it directly must get the same content from the server.

> Not all pages are suitable for prerendering. Any content that is prerendered will be seen by all users. You can of course fetch personalized data in `onMount` in a prerendered page, but this may result in a poorer user experience since it will involve blank initial content or loading indicators.

Note that you can still prerender pages that load data based on the page’s parameters, such as a `src/routes/blog/[slug]/+page.svelte` route.

Accessing [url.searchParams](https://kit.svelte.dev/docs/load#Using-URL-data-url) during prerendering is forbidden. If you need to use it, ensure you are only doing so in the browser (for example in `onMount`).

Pages with [actions](https://kit.svelte.dev/docs/form-actions) cannot be prerendered, because a server must be able to handle the action `POST` requests.

### Route conflicts

Because prerendering writes to the filesystem, it isn’t possible to have two endpoints that would cause a directory and a file to have the same name. For example, `src/routes/foo/+server.js` and `src/routes/foo/bar/+server.js` would try to create `foo` and `foo/bar`, which is impossible.

For that reason among others, it’s recommended that you always include a file extension — `src/routes/foo.json/+server.js` and `src/routes/foo/bar.json/+server.js` would result in `foo.json` and `foo/bar.json` files living harmoniously side-by-side.

For *pages*, we skirt around this problem by writing `foo/index.html` instead of `foo`.

### Troubleshooting

If you encounter an error like ‘The following routes were marked as prerenderable, but were not prerendered’ it’s because the route in question (or a parent layout, if it’s a page) has `export const prerender = true` but the page wasn’t reached by the prerendering crawler and thus wasn’t prerendered.

Since these routes cannot be dynamically server-rendered, this will cause errors when people try to access the route in question. There are a few ways to fix it:

- Ensure that SvelteKit can find the route by following links from [config.kit.prerender.entries](https://kit.svelte.dev/docs/configuration#prerender) or the [entries](#entries) page option. Add links to dynamic routes (i.e. pages with `[parameters]` ) to this option if they are not found through crawling the other entry points, else they are not prerendered because SvelteKit doesn’t know what value the parameters should have. Pages not marked as prerenderable will be ignored and their links to other pages will not be crawled, even if some of them would be prerenderable.
- Ensure that SvelteKit can find the route by discovering a link to it from one of your other prerendered pages that have server-side rendering enabled.
- Change `export const prerender = true` to `export const prerender = 'auto'`. Routes with `'auto'` can be dynamically server rendered

## entries

SvelteKit will discover pages to prerender automatically, by starting at *entry points* and crawling them. By default, all your non-dynamic routes are considered entry points — for example, if you have these routes...

```
/    # non-dynamic
/blog# non-dynamic
/blog/[slug]  # dynamic, because of `[slug]`
```

...SvelteKit will prerender `/` and `/blog`, and in the process discover links like `<a href="/blog/hello-world">` which give it new pages to prerender.

Most of the time, that’s enough. In some situations, links to pages like `/blog/hello-world` might not exist (or might not exist on prerendered pages), in which case we need to tell SvelteKit about their existence.

This can be done with [config.kit.prerender.entries](https://kit.svelte.dev/docs/configuration#prerender), or by exporting an `entries` function from a `+page.js`, a `+page.server.js` or a `+server.js` belonging to a dynamic route:

 src/routes/blog/[slug]/+page.server

```
/** @type {import('./$types').EntryGenerator} */
export function function entries(): {
    slug: string;
}[]@type{import('./$types').EntryGenerator}entries() {
	return [
		{ slug: stringslug: 'hello-world' },
		{ slug: stringslug: 'another-blog-post' }
	];
}

export const const prerender: trueprerender = true;
```

```
import type { type EntryGenerator = () => Promise<Array<Record<string, any>>> | Array<Record<string, any>>
type EntryGenerator = () => Promise<Array<Record<string, any>>> | Array<Record<string, any>>EntryGenerator } from './$types';

export const const entries: EntryGeneratorentries: type EntryGenerator = () => Promise<Array<Record<string, any>>> | Array<Record<string, any>>
type EntryGenerator = () => Promise<Array<Record<string, any>>> | Array<Record<string, any>>EntryGenerator = () => {
	return [
		{ slug: stringslug: 'hello-world' },
		{ slug: stringslug: 'another-blog-post' }
	];
};

export const const prerender: trueprerender = true;
```

`entries` can be an `async` function, allowing you to (for example) retrieve a list of posts from a CMS or database, in the example above.

## ssr

Normally, SvelteKit renders your page on the server first and sends that HTML to the client where it’s [hydrated](https://kit.svelte.dev/docs/glossary#Hydration). If you set `ssr` to `false`, it renders an empty ‘shell’ page instead. This is useful if your page is unable to be rendered on the server (because you use browser-only globals like `document` for example), but in most situations it’s not recommended ([see appendix](https://kit.svelte.dev/docs/glossary#SSR)).

 +page

```
export const const ssr: falsessr = false;
// If both `ssr` and `csr` are `false`, nothing will be rendered!
```

If you add `export const ssr = false` to your root `+layout.js`, your entire app will only be rendered on the client — which essentially means you turn your app into an SPA.

> If all your page options are boolean or string literal values, SvelteKit will evaluate them statically. If not, it will import your `+page.js` or `+layout.js` file on the server (both at build time, and at runtime if your app isn’t fully static) so it can evaluate the options. In the second case, browser-only code must not run when the module is loaded. In practice, this means you should import browser-only code in your `+page.svelte` or `+layout.svelte` file instead.

## csr

Ordinarily, SvelteKit [hydrates](https://kit.svelte.dev/docs/glossary#Hydration) your server-rendered HTML into an interactive client-side-rendered (CSR) page. Some pages don’t require JavaScript at all — many blog posts and ‘about’ pages fall into this category. In these cases you can disable CSR:

 +page

```
export const const csr: falsecsr = false;
// If both `csr` and `ssr` are `false`, nothing will be rendered!
```

Disabling CSR does not ship any JavaScript to the client. This means:

- The webpage should work with HTML and CSS only.
- `<script>` tags inside all Svelte components are removed.
- `<form>` elements cannot be [progressively enhanced](https://kit.svelte.dev/docs/form-actions#Progressive-enhancement).
- Links are handled by the browser with a full-page navigation.
- Hot Module Replacement (HMR) will be disabled.

You can enable `csr` during development (for example to take advantage of HMR) like so:

 +page

```
import { const dev: booleanWhether the dev server is running. This is not guaranteed to correspond to NODE_ENV or MODE.
dev } from '$app/environment';

export const const csr: booleancsr = const dev: booleanWhether the dev server is running. This is not guaranteed to correspond to NODE_ENV or MODE.
dev;
```

## trailingSlash

By default, SvelteKit will remove trailing slashes from URLs — if you visit `/about/`, it will respond with a redirect to `/about`. You can change this behaviour with the `trailingSlash` option, which can be one of `'never'` (the default), `'always'`, or `'ignore'`.

As with other page options, you can export this value from a `+layout.js` or a `+layout.server.js` and it will apply to all child pages. You can also export the configuration from `+server.js` files.

 src/routes/+layout

```
export const const trailingSlash: "always"trailingSlash = 'always';
```

This option also affects [prerendering](#prerender). If `trailingSlash` is `always`, a route like `/about` will result in an `about/index.html` file, otherwise it will create `about.html`, mirroring static webserver conventions.

> Ignoring trailing slashes is not recommended — the semantics of relative paths differ between the two cases (`./y` from `/x` is `/y`, but from `/x/` is `/x/y`), and `/x` and `/x/` are treated as separate URLs which is harmful to SEO.

## config

With the concept of [adapters](https://kit.svelte.dev/docs/adapters), SvelteKit is able to run on a variety of platforms. Each of these might have specific configuration to further tweak the deployment — for example on Vercel you could choose to deploy some parts of your app on the edge and others on serverless environments.

`config` is an object with key-value pairs at the top level. Beyond that, the concrete shape is dependent on the adapter you’re using. Every adapter should provide a `Config` interface to import for type safety. Consult the documentation of your adapter for more information.

 src/routes/+page

```
/** @type {import('some-adapter').Config} */
export const const config: Config@type{import('some-adapter').Config}config = {
	Config.runtime: stringruntime: 'edge'
};
```

```
import type { Config } from 'some-adapter';

export const const config: Configconfig: Config = {
	Config.runtime: stringruntime: 'edge'
};
```

`config` objects are merged at the top level (but *not* deeper levels). This means you don’t need to repeat all the values in a `+page.js` if you want to only override some of the values in the upper `+layout.js`. For example this layout configuration...

 src/routes/+layout

```
export const const config: {
    runtime: string;
    regions: string;
    foo: {
        bar: boolean;
    };
}config = {
	runtime: stringruntime: 'edge',
	regions: stringregions: 'all',
	foo: {
    bar: boolean;
}foo: {
		bar: booleanbar: true
	}
}
```

...is overridden by this page configuration...

 src/routes/+page

```
export const const config: {
    regions: string[];
    foo: {
        baz: boolean;
    };
}config = {
	regions: string[]regions: ['us1', 'us2'],
	foo: {
    baz: boolean;
}foo: {
		baz: booleanbaz: true
	}
}
```

...which results in the config value `{ runtime: 'edge', regions: ['us1', 'us2'], foo: { baz: true } }` for that page.

## Further reading

- [Tutorial: Page options](https://kit.svelte.dev/tutorial/kit/page-options)

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/20-core-concepts/40-page-options.md) [[llms.txt](https://kit.svelte.dev/docs/kit/page-options/llms.txt)]

 previous next [[Form actions](https://kit.svelte.dev/docs/kit/form-actions)] [[State management](https://kit.svelte.dev/docs/kit/state-management)]

---

# Performance

> Performance • SvelteKit documentation

Out of the box, SvelteKit does a lot of work to make your applications as performant as possible:

- Code-splitting, so that only the code you need for the current page is loaded
- Asset preloading, so that ‘waterfalls’ (of files requesting other files) are prevented
- File hashing, so that your assets can be cached forever
- Request coalescing, so that data fetched from separate server `load` functions is grouped into a single HTTP request
- Parallel loading, so that separate universal `load` functions fetch data simultaneously
- Data inlining, so that requests made with `fetch` during server rendering can be replayed in the browser without issuing a new request
- Conservative invalidation, so that `load` functions are only re-run when necessary
- Prerendering (configurable on a per-route basis, if necessary) so that pages without dynamic data can be served instantaneously
- Link preloading, so that data and code requirements for a client-side navigation are eagerly anticipated

Nevertheless, we can’t (yet) eliminate all sources of slowness. To eke out maximum performance, you should be mindful of the following tips.

## Diagnosing issues

Google’s [PageSpeed Insights](https://pagespeed.web.dev/) and (for more advanced analysis) [WebPageTest](https://www.webpagetest.org/) are excellent ways to understand the performance characteristics of a site that is already deployed to the internet.

Your browser also includes useful developer tools for analysing your site, whether deployed or running locally:

- Chrome - [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview#devtools), [Network](https://developer.chrome.com/docs/devtools/network), and [Performance](https://developer.chrome.com/docs/devtools/performance) devtools
- Edge - [Lighthouse](https://learn.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/lighthouse/lighthouse-tool), [Network](https://learn.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/network/), and [Performance](https://learn.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/evaluate-performance/) devtools
- Firefox - [Network](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/) and [Performance](https://hacks.mozilla.org/2022/03/performance-tool-in-firefox-devtools-reloaded/) devtools
- Safari - [enhancing the performance of your webpage](https://developer.apple.com/library/archive/documentation/NetworkingInternetWeb/Conceptual/Web_Inspector_Tutorial/EnhancingyourWebpagesPerformance/EnhancingyourWebpagesPerformance.html)

Note that your site running locally in `dev` mode will exhibit different behaviour than your production app, so you should do performance testing in [preview](https://kit.svelte.dev/docs/building-your-app#Preview-your-app) mode after building.

### Instrumenting

If you see in the network tab of your browser that an API call is taking a long time and you’d like to understand why, you may consider instrumenting your backend with a tool like [OpenTelemetry](https://opentelemetry.io/) or [Server-Timing headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing).

## Optimizing assets

### Images

Reducing the size of image files is often one of the most impactful changes you can make to a site’s performance. Svelte provides the `@sveltejs/enhanced-img` package, detailed on the [images](https://kit.svelte.dev/docs/images) page, for making this easier. Additionally, Lighthouse is useful for identifying the worst offenders.

### Videos

Video files can be very large, so extra care should be taken to ensure that they’re optimized:

- Compress videos with tools such as [Handbrake](https://handbrake.fr/). Consider converting the videos to web-friendly formats such as `.webm` or `.mp4`.
- You can [lazy-load videos](https://web.dev/articles/lazy-loading-video) located below the fold with `preload="none"` (though note that this will slow down playback when the user *does* initiate it).
- Strip the audio track out of muted videos using a tool like [FFmpeg](https://ffmpeg.org/).

### Fonts

SvelteKit automatically preloads critical `.js` and `.css` files when the user visits a page, but it does *not* preload fonts by default, since this may cause unnecessary files (such as font weights that are referenced by your CSS but not actually used on the current page) to be downloaded. Having said that, preloading fonts correctly can make a big difference to how fast your site feels. In your [handle](https://kit.svelte.dev/docs/hooks#Server-hooks-handle) hook, you can call `resolve` with a `preload` filter that includes your fonts.

You can reduce the size of font files by [subsetting](https://web.dev/learn/performance/optimize-web-fonts#subset_your_web_fonts) your fonts.

## Reducing code size

### Svelte version

We recommend running the latest version of Svelte. Svelte 5 is smaller and faster than Svelte 4, which is smaller and faster than Svelte 3.

### Packages

[rollup-plugin-visualizer](https://www.npmjs.com/package/rollup-plugin-visualizer) can be helpful for identifying which packages are contributing the most to the size of your site. You may also find opportunities to remove code by manually inspecting the build output (use `build: { minify: false }` in your [Vite config](https://vitejs.dev/config/build-options.html#build-minify) to make the output readable, but remember to undo that before deploying your app), or via the network tab of your browser’s devtools.

### External scripts

Try to minimize the number of third-party scripts running in the browser. For example, instead of using JavaScript-based analytics consider using server-side implementations, such as those offered by many platforms with SvelteKit adapters including [Cloudflare](https://www.cloudflare.com/web-analytics/), [Netlify](https://docs.netlify.com/monitor-sites/site-analytics/), and [Vercel](https://vercel.com/docs/analytics).

To run third party scripts in a web worker (which avoids blocking the main thread), use [Partytown’s SvelteKit integration](https://partytown.builder.io/sveltekit).

### Selective loading

Code imported with static `import` declarations will be automatically bundled with the rest of your page. If there is a piece of code you need only when some condition is met, use the dynamic `import(...)` form to selectively lazy-load the component.

## Navigation

### Preloading

You can speed up client-side navigations by eagerly preloading the necessary code and data, using [link options](https://kit.svelte.dev/docs/link-options). This is configured by default on the `<body>` element when you create a new SvelteKit app.

### Non-essential data

For slow-loading data that isn’t needed immediately, the object returned from your `load` function can contain promises rather than the data itself. For server `load` functions, this will cause the data to [stream](https://kit.svelte.dev/docs/load#Streaming-with-promises) in after the navigation (or initial page load).

### Preventing waterfalls

One of the biggest performance killers is what is referred to as a *waterfall*, which is a series of requests that is made sequentially. This can happen on the server or in the browser, but is especially costly when dealing with data that has to travel further or across slower networks, such as a mobile user making a call to a distant server.

In the browser, waterfalls can occur when your HTML kicks off request chains such as requesting JS which requests CSS which requests a background image and web font. SvelteKit will largely solve this class of problems for you by adding [modulepreload](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/modulepreload) tags or headers, but you should view [the network tab in your devtools](#Diagnosing-issues) to check whether additional resources need to be preloaded.

- Pay special attention to this if you use [web fonts](#Optimizing-assets-Fonts) since they need to be handled manually.
- Enabling [single page app (SPA) mode](https://kit.svelte.dev/docs/single-page-apps) will cause such waterfalls. With SPA mode, an empty page is generated, which fetches JavaScript, which ultimately loads and renders the page. This results in extra network round trips before a single pixel can be displayed.

Waterfalls can also occur on calls to the backend whether made from the browser or server. E.g. if a universal `load` function makes an API call to fetch the current user, then uses the details from that response to fetch a list of saved items, and then uses *that* response to fetch the details for each item, the browser will end up making multiple sequential requests. This is deadly for performance, especially for users that are physically located far from your backend.

- Avoid this issue by using [serverloadfunctions](https://kit.svelte.dev/docs/load#Universal-vs-server) to make requests to backend services that are dependencies from the server rather than from the browser. Note, however, that server `load` functions are also not immune to waterfalls (though they are much less costly since they rarely involve round trips with high latency). For example, if you query a database to get the current user and then use that data to make a second query for a list of saved items, it will typically be more performant to issue a single query with a database join.

## Hosting

Your frontend should be located in the same data center as your backend to minimize latency. For sites with no central backend, many SvelteKit adapters support deploying to the *edge*, which means handling each user’s requests from a nearby server. This can reduce load times significantly. Some adapters even support [configuring deployment on a per-route basis](https://kit.svelte.dev/docs/page-options#config). You should also consider serving images from a CDN (which are typically edge networks) — the hosts for many SvelteKit adapters will do this automatically.

Ensure your host uses HTTP/2 or newer. Vite’s code splitting creates numerous small files for improved cacheability, which results in excellent performance, but this does assume that your files can be loaded in parallel with HTTP/2.

## Further reading

For the most part, building a performant SvelteKit app is the same as building any performant web app. You should be able to apply information from general performance resources such as [Core Web Vitals](https://web.dev/explore/learn-core-web-vitals) to any web experience you build.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/40-best-practices/05-performance.md) [[llms.txt](https://kit.svelte.dev/docs/kit/performance/llms.txt)]

 previous next [[Auth](https://kit.svelte.dev/docs/kit/auth)] [[Icons](https://kit.svelte.dev/docs/kit/icons)]

---

# Project structure

> Project structure • SvelteKit documentation

A typical SvelteKit project looks like this:

```
my-project/
├ src/
│ ├ lib/
│ │ ├ server/
│ │ │ └ [your server-only lib files]
│ │ └ [your lib files]
│ ├ params/
│ │ └ [your param matchers]
│ ├ routes/
│ │ └ [your routes]
│ ├ app.html
│ ├ error.html
│ ├ hooks.client.js
│ ├ hooks.server.js
│ ├ service-worker.js
│ └ tracing.server.js
├ static/
│ └ [your static assets]
├ tests/
│ └ [your tests]
├ package.json
├ svelte.config.js
├ tsconfig.json
└ vite.config.js
```

You’ll also find common files like `.gitignore` and `.npmrc` (and `.prettierrc` and `eslint.config.js` and so on, if you chose those options when running `npx sv create`).

## Project files

### src

The `src` directory contains the meat of your project. Everything except `src/routes` and `src/app.html` is optional.

- `lib` contains your library code (utilities and components), which can be imported via the [$lib](https://kit.svelte.dev/docs/$lib) alias, or packaged up for distribution using [svelte-package](https://kit.svelte.dev/docs/packaging)
  - `server` contains your server-only library code. It can be imported by using the [$lib/server](https://kit.svelte.dev/docs/server-only-modules) alias. SvelteKit will prevent you from importing these in client code.
- `params` contains any [param matchers](https://kit.svelte.dev/docs/advanced-routing#Matching) your app needs
- `routes` contains the [routes](https://kit.svelte.dev/docs/routing) of your application. You can also colocate other components that are only used within a single route here
- `app.html` is your page template — an HTML document containing the following placeholders:
  - `%sveltekit.head%` — `<link>` and `<script>` elements needed by the app, plus any `<svelte:head>` content
  - `%sveltekit.body%` — the markup for a rendered page. This should live inside a `<div>` or other element, rather than directly inside `<body>`, to prevent bugs caused by browser extensions injecting elements that are then destroyed by the hydration process. SvelteKit will warn you in development if this is not the case
  - `%sveltekit.assets%` — either [paths.assets](https://kit.svelte.dev/docs/configuration#paths), if specified, or a relative path to [paths.base](https://kit.svelte.dev/docs/configuration#paths)
  - `%sveltekit.nonce%` — a [CSP](https://kit.svelte.dev/docs/configuration#csp) nonce for manually included links and scripts, if used
  - `%sveltekit.env.[NAME]%` - this will be replaced at render time with the `[NAME]` environment variable, which must begin with the [publicPrefix](https://kit.svelte.dev/docs/configuration#env) (usually `PUBLIC_`). It will fallback to `''` if not matched.
  - `%sveltekit.version%` — the app version, which can be specified with the [version](https://kit.svelte.dev/docs/configuration#version) configuration
- `error.html` is the page that is rendered when everything else fails. It can contain the following placeholders:
  - `%sveltekit.status%` — the HTTP status
  - `%sveltekit.error.message%` — the error message
- `hooks.client.js` contains your client [hooks](https://kit.svelte.dev/docs/hooks)
- `hooks.server.js` contains your server [hooks](https://kit.svelte.dev/docs/hooks)
- `service-worker.js` contains your [service worker](https://kit.svelte.dev/docs/service-workers)
- `instrumentation.server.js` contains your [observability](https://kit.svelte.dev/docs/observability) setup and instrumentation code
  - Requires adapter support. If your adapter supports it, it is guaranteed to run prior to loading and running your application code.

(Whether the project contains `.js` or `.ts` files depends on whether you opt to use TypeScript when you create your project.)

If you added [Vitest](https://vitest.dev) when you set up your project, your unit tests will live in the `src` directory with a `.test.js` extension.

### static

Any static assets that should be served without any alteration to the name — such as `robots.txt` — go in here. It’s generally preferable to minimize the number of assets in `static/` and instead `import` them. Using an `import` allows [Vite’s built-in handling](https://kit.svelte.dev/docs/images#Vite's-built-in-handling) to give a unique name to an asset based on a hash of its contents so that it can be cached.

### tests

If you added [Playwright](https://playwright.dev/) for browser testing when you set up your project, the tests will live in this directory.

### package.json

Your `package.json` file must include `@sveltejs/kit`, `svelte` and `vite` as `devDependencies`.

When you create a project with `npx sv create`, you’ll also notice that `package.json` includes `"type": "module"`. This means that `.js` files are interpreted as native JavaScript modules with `import` and `export` keywords. Legacy CommonJS files need a `.cjs` file extension.

### svelte.config.js

This file contains your Svelte and SvelteKit [configuration](https://kit.svelte.dev/docs/configuration).

### tsconfig.json

This file (or `jsconfig.json`, if you prefer type-checked `.js` files over `.ts` files) configures TypeScript, if you added typechecking during `npx sv create`. Since SvelteKit relies on certain configuration being set a specific way, it generates its own `.svelte-kit/tsconfig.json` file which your own config `extends`. To make changes to top-level options such as `include` and `exclude`, we recommend extending the generated config; see the [typescript.configsetting](https://kit.svelte.dev/docs/configuration#typescript) for more details.

### vite.config.js

A SvelteKit project is really just a [Vite](https://vitejs.dev) project that uses the [@sveltejs/kit/vite](https://kit.svelte.dev/docs/@sveltejs-kit-vite) plugin, along with any other [Vite configuration](https://vitejs.dev/config/).

## Other files

### .svelte-kit

As you develop and build your project, SvelteKit will generate files in a `.svelte-kit` directory (configurable as [outDir](https://kit.svelte.dev/docs/configuration#outDir)). You can ignore its contents, and delete them at any time (they will be regenerated when you next `dev` or `build`).

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/10-getting-started/30-project-structure.md) [[llms.txt](https://kit.svelte.dev/docs/kit/project-structure/llms.txt)]

 previous next [[Project types](https://kit.svelte.dev/docs/kit/project-types)] [[Web standards](https://kit.svelte.dev/docs/kit/web-standards)]

---

# Project types

> Project types • SvelteKit documentation

SvelteKit offers configurable rendering, which allows you to build and deploy your project in several different ways. You can build all of the below types of applications and more with SvelteKit. Rendering settings are not mutually exclusive and you may choose the optimal manner with which to render different parts of your application.

If you don’t have a particular way you’d like to build your application in mind, don’t worry! The way your application is built, deployed, and rendered is controlled by which adapter you’ve chosen and a small amount of configuration and these can always be changed later. The [project structure](https://kit.svelte.dev/docs/project-structure) and [routing](https://kit.svelte.dev/docs/glossary#Routing) will be the same regardless of the project type that you choose.

## Default rendering

By default, when a user visits a site, SvelteKit will render the first page with [server-side rendering (SSR)](https://kit.svelte.dev/docs/glossary#SSR) and subsequent pages with [client-side rendering (CSR)](https://kit.svelte.dev/docs/glossary#CSR). Using SSR for the initial render improves SEO and perceived performance of the initial page load. Client-side rendering then takes over and updates the page without having to rerender common components, which is typically faster and eliminates a flash when navigating between pages. Apps built with this hybrid rendering approach have also been called [transitional apps](https://www.youtube.com/watch?v=860d8usGC0o).

## Static site generation

You can use SvelteKit as a [static site generator (SSG)](https://kit.svelte.dev/docs/glossary#SSG) that fully [prerenders](https://kit.svelte.dev/docs/glossary#Prerendering) your site with static rendering using [adapter-static](https://kit.svelte.dev/docs/adapter-static). You may also use [the prerender option](https://kit.svelte.dev/docs/page-options#prerender) to prerender only some pages and then choose a different adapter with which to dynamically server-render other pages.

Tools built solely to do static site generation may scale the prerendering process more efficiently during build when rendering a very large number of pages. When working with very large statically generated sites, you can avoid long build times with [Incremental Static Regeneration (ISR) if usingadapter-vercel](https://kit.svelte.dev/docs/adapter-vercel#Incremental-Static-Regeneration). And in contrast to purpose-built SSGs, SvelteKit allows for nicely mixing and matching different rendering types on different pages.

## Single-page app

[Single-page apps (SPAs)](https://kit.svelte.dev/docs/glossary#SPA) exclusively use [client-side rendering (CSR)](https://kit.svelte.dev/docs/glossary#CSR). You can [build single-page apps (SPAs)](https://kit.svelte.dev/docs/single-page-apps) with SvelteKit. As with all types of SvelteKit applications, you can write your backend in SvelteKit or [another language or framework](#Separate-backend). If you are building an application with no backend or a [separate backend](#Separate-backend), you can simply skip over and ignore the parts of the docs talking about `server` files.

## Multi-page app

SvelteKit isn’t typically used to build [traditional multi-page apps](https://kit.svelte.dev/docs/glossary#MPA). However, in SvelteKit you can remove all JavaScript on a page with [csr = false](https://kit.svelte.dev/docs/page-options#csr), which will render subsequent links on the server, or you can use [data-sveltekit-reload](https://kit.svelte.dev/docs/link-options#data-sveltekit-reload) to render specific links on the server.

## Separate backend

If your backend is written in another language such as Go, Java, PHP, Ruby, Rust, or C#, there are a couple of ways that you can deploy your application. The most recommended way would be to deploy your SvelteKit frontend separately from your backend utilizing `adapter-node` or a serverless adapter. Some users prefer not to have a separate process to manage and decide to deploy their application as a [single-page app (SPA)](https://kit.svelte.dev/docs/single-page-apps) served by their backend server, but note that single-page apps have worse SEO and performance characteristics.

If you are using an external backend, you can simply skip over and ignore the parts of the docs talking about `server` files. You may also want to reference [the FAQ about how to make calls to a separate backend](https://kit.svelte.dev/docs/faq#How-do-I-use-a-different-backend-API-server).

## Serverless app

SvelteKit apps are simple to run on serverless platforms. [The default zero config adapter](https://kit.svelte.dev/docs/adapter-auto) will automatically run your app on a number of supported platforms or you can use [adapter-vercel](https://kit.svelte.dev/docs/adapter-vercel), [adapter-netlify](https://kit.svelte.dev/docs/adapter-netlify), or [adapter-cloudflare](https://kit.svelte.dev/docs/adapter-cloudflare) to provide platform-specific configuration. And [community adapters](https://kit.svelte.dev/packages#sveltekit-adapters) allow you to deploy your application to almost any serverless environment. Some of these adapters such as [adapter-vercel](https://kit.svelte.dev/docs/adapter-vercel) and [adapter-netlify](https://kit.svelte.dev/docs/adapter-netlify) offer an `edge` option, to support [edge rendering](https://kit.svelte.dev/docs/glossary#Edge) for improved latency.

## Your own server

You can deploy to your own server or VPS using [adapter-node](https://kit.svelte.dev/docs/adapter-node).

## Container

You can use [adapter-node](https://kit.svelte.dev/docs/adapter-node) to run a SvelteKit app within a container such as Docker or LXC.

## Library

You can create a library to be used by other Svelte apps with the [@sveltejs/package](https://kit.svelte.dev/docs/packaging) add-on to SvelteKit by choosing the library option when running [sv create](https://kit.svelte.dev/docs/cli/sv-create).

## Offline app

SvelteKit has full support for [service workers](https://kit.svelte.dev/docs/service-workers) allowing you to build many types of applications such as offline apps and [progressive web apps](https://kit.svelte.dev/docs/glossary#PWA).

## Mobile app

You can turn a [SvelteKit SPA](https://kit.svelte.dev/docs/single-page-apps) into a mobile app with [Tauri](https://v2.tauri.app/start/frontend/sveltekit/) or [Capacitor](https://capacitorjs.com/solution/svelte). Mobile features like the camera, geolocation, and push notifications are available via plugins for both platforms.

These mobile development platforms work by starting a local web server and then serving your application like a static host on your phone. You may find [bundleStrategy: 'single'](https://kit.svelte.dev/docs/configuration#output) to be a helpful option to limit the number of requests made. E.g. at the time of writing, the Capacitor local server uses HTTP/1, which limits the number of concurrent connections.

## Desktop app

You can turn a [SvelteKit SPA](https://kit.svelte.dev/docs/single-page-apps) into a desktop app with [Tauri](https://v2.tauri.app/start/frontend/sveltekit/), [Wails](https://wails.io/docs/guides/sveltekit/), or [Electron](https://www.electronjs.org/).

## Browser extension

You can build browser extensions using either [adapter-static](https://kit.svelte.dev/docs/adapter-static) or [community adapters](https://kit.svelte.dev/packages#sveltekit-adapters) specifically tailored towards browser extensions.

## Embedded device

Because of its efficient rendering, Svelte can be run on low power devices. Embedded devices like microcontrollers and TVs may limit the number of concurrent connections. In order to reduce the number of concurrent requests, you may find [bundleStrategy: 'single'](https://kit.svelte.dev/docs/configuration#output) to be a helpful option in this deployment configuration.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/10-getting-started/25-project-types.md) [[llms.txt](https://kit.svelte.dev/docs/kit/project-types/llms.txt)]

 previous next [[Creating a project](https://kit.svelte.dev/docs/kit/creating-a-project)] [[Project structure](https://kit.svelte.dev/docs/kit/project-structure)]
