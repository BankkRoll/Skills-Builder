# Accessibility and more

# Accessibility

> Accessibility • SvelteKit documentation

SvelteKit strives to provide an accessible platform for your app by default. Svelte’s [compile-time accessibility checks](https://kit.svelte.dev/svelte/compiler-warnings) will also apply to any SvelteKit application you build.

Here’s how SvelteKit’s built-in accessibility features work and what you need to do to help these features to work as well as possible. Keep in mind that while SvelteKit provides an accessible foundation, you are still responsible for making sure your application code is accessible. If you’re new to accessibility, see the [“further reading”](https://kit.svelte.dev/docs/accessibility#Further-reading) section of this guide for additional resources.

We recognize that accessibility can be hard to get right. If you want to suggest improvements to how SvelteKit handles accessibility, please [open a GitHub issue](https://github.com/sveltejs/kit/issues).

## Route announcements

In traditional server-rendered applications, every navigation (e.g. clicking on an `<a>` tag) triggers a full page reload. When this happens, screen readers and other assistive technology will read out the new page’s title so that users understand that the page has changed.

Since navigation between pages in SvelteKit happens without reloading the page (known as [client-side routing](https://kit.svelte.dev/docs/glossary#Routing)), SvelteKit injects a [live region](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions) onto the page that will read out the new page name after each navigation. This determines the page name to announce by inspecting the `<title>` element.

Because of this behavior, every page in your app should have a unique, descriptive title. In SvelteKit, you can do this by placing a `<svelte:head>` element on each page:

 src/routes/+page

```
<svelte:head>
	<title>Todo List</title>
</svelte:head>
```

This will allow screen readers and other assistive technology to identify the new page after a navigation occurs. Providing a descriptive title is also important for [SEO](https://kit.svelte.dev/docs/seo#Manual-setup-title-and-meta).

## Focus management

In traditional server-rendered applications, every navigation will reset focus to the top of the page. This ensures that people browsing the web with a keyboard or screen reader will start interacting with the page from the beginning.

To simulate this behavior during client-side routing, SvelteKit focuses the `<body>` element after each navigation and [enhanced form submission](https://kit.svelte.dev/docs/form-actions#Progressive-enhancement). There is one exception - if an element with the [autofocus](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autofocus) attribute is present, SvelteKit will focus that element instead. Make sure to [consider the implications for assistive technology](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autofocus#accessibility_considerations) when using that attribute.

If you want to customize SvelteKit’s focus management, you can use the `afterNavigate` hook:

```
import { function afterNavigate(callback: (navigation: import("@sveltejs/kit").AfterNavigate) => void): voidA lifecycle function that runs the supplied callback when the current component mounts, and also whenever we navigate to a URL.
afterNavigate must be called during a component initialization. It remains active as long as the component is mounted.
afterNavigate } from '$app/navigation';

function afterNavigate(callback: (navigation: import("@sveltejs/kit").AfterNavigate) => void): voidA lifecycle function that runs the supplied callback when the current component mounts, and also whenever we navigate to a URL.
afterNavigate must be called during a component initialization. It remains active as long as the component is mounted.
afterNavigate(() => {
	/** @type {HTMLElement | null} */
	const const to_focus: Element | null@type{HTMLElement | null}to_focus = var document: DocumentMDN Reference
document.ParentNode.querySelector<Element>(selectors: string): Element | null (+4 overloads)Returns the first element that is a descendant of node that matches selectors.
MDN Reference
querySelector('.focus-me');
	const to_focus: Element | null@type{HTMLElement | null}to_focus?.focus();
});
```

You can also programmatically navigate to a different page using the [goto](https://kit.svelte.dev/docs/$app-navigation#goto) function. By default, this will have the same client-side routing behavior as clicking on a link. However, `goto` also accepts a `keepFocus` option that will preserve the currently-focused element instead of resetting focus. If you enable this option, make sure the currently-focused element still exists on the page after navigation. If the element no longer exists, the user’s focus will be lost, making for a confusing experience for assistive technology users.

## The “lang” attribute

By default, SvelteKit’s page template sets the default language of the document to English. If your content is not in English, you should update the `<html>` element in `src/app.html` to have the correct [lang](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang#accessibility) attribute. This will ensure that any assistive technology reading the document uses the correct pronunciation. For example, if your content is in German, you should update `app.html` to the following:

 src/app

```
<html lang="de">
```

If your content is available in multiple languages, you should set the `lang` attribute based on the language of the current page. You can do this with SvelteKit’s [handle hook](https://kit.svelte.dev/docs/hooks#Server-hooks-handle):

 src/app

```
<html lang="%lang%">
```

src/hooks.server

```
/** @type {import('@sveltejs/kit').Handle} */
export function function handle({ event, resolve }: {
    event: any;
    resolve: any;
}): any@type{import('@sveltejs/kit').Handle}handle({ event: anyevent, resolve: anyresolve }) {
	return resolve: anyresolve(event: anyevent, {
		transformPageChunk: ({ html }: {
    html: any;
}) => anytransformPageChunk: ({ html: anyhtml }) => html: anyhtml.replace('%lang%', function get_lang(event: any): string@paramevent get_lang(event: anyevent))
	});
}
```

```
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
Handle = ({ event: RequestEvent<Record<string, string>, string | null>event, resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve }) => {
	return resolve: (event: RequestEvent, opts?: ResolveOptions) => MaybePromise<Response>resolve(event: RequestEvent<Record<string, string>, string | null>event, {
		ResolveOptions.transformPageChunk?: ((input: {
    html: string;
    done: boolean;
}) => MaybePromise<string | undefined>) | undefinedApplies custom transforms to HTML. If done is true, it’s the final chunk. Chunks are not guaranteed to be well-formed HTML
(they could include an element’s opening tag but not its closing tag, for example)
but they will always be split at sensible boundaries such as %sveltekit.head% or layout/page components.
@paraminput the html chunk and the info if this is the last chunktransformPageChunk: ({ html: stringhtml }) => html: stringhtml.String.replace(searchValue: string | RegExp, replaceValue: string): string (+3 overloads)Replaces text in a string, using a regular expression or search string.
@paramsearchValue A string or regular expression to search for.@paramreplaceValue A string containing the text to replace. When the {@linkcode searchValue} is a RegExp, all matches are replaced if the g flag is set (or only those matches at the beginning, if the y flag is also present). Otherwise, only the first match of {@linkcode searchValue} is replaced.replace('%lang%', function get_lang(event: any): string@paramevent get_lang(event: RequestEvent<Record<string, string>, string | null>event))
	});
};
```

## Further reading

For the most part, building an accessible SvelteKit app is the same as building an accessible web app. You should be able to apply information from the following general accessibility resources to any web experience you build:

- [MDN Web Docs: Accessibility](https://developer.mozilla.org/en-US/docs/Learn/Accessibility)
- [The A11y Project](https://www.a11yproject.com/)
- [How to Meet WCAG (Quick Reference)](https://www.w3.org/WAI/WCAG21/quickref/)

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/40-best-practices/10-accessibility.md) [[llms.txt](https://kit.svelte.dev/docs/kit/accessibility/llms.txt)]

 previous next [[Images](https://kit.svelte.dev/docs/kit/images)] [[SEO](https://kit.svelte.dev/docs/kit/seo)]

---

# Zero

> Zero-config deployments • SvelteKit documentation

When you create a new SvelteKit project with `npx sv create`, it installs [adapter-auto](https://github.com/sveltejs/kit/tree/main/packages/adapter-auto) by default. This adapter automatically installs and uses the correct adapter for supported environments when you deploy:

- [@sveltejs/adapter-cloudflare](https://kit.svelte.dev/docs/adapter-cloudflare) for [Cloudflare Pages](https://developers.cloudflare.com/pages/)
- [@sveltejs/adapter-netlify](https://kit.svelte.dev/docs/adapter-netlify) for [Netlify](https://netlify.com/)
- [@sveltejs/adapter-vercel](https://kit.svelte.dev/docs/adapter-vercel) for [Vercel](https://vercel.com/)
- [svelte-adapter-azure-swa](https://github.com/geoffrich/svelte-adapter-azure-swa) for [Azure Static Web Apps](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [svelte-kit-sst](https://github.com/sst/v2/tree/master/packages/svelte-kit-sst) for [AWS via SST](https://sst.dev/docs/start/aws/svelte)
- [@sveltejs/adapter-node](https://kit.svelte.dev/docs/adapter-node) for [Google Cloud Run](https://cloud.google.com/run)

It’s recommended to install the appropriate adapter to your `devDependencies` once you’ve settled on a target environment, since this will add the adapter to your lockfile and slightly improve install times on CI.

## Environment-specific configuration

To add configuration options, such as `{ edge: true }` in [adapter-vercel](https://kit.svelte.dev/docs/adapter-vercel) and [adapter-netlify](https://kit.svelte.dev/docs/adapter-netlify), you must install the underlying adapter — `adapter-auto` does not take any options.

## Adding community adapters

You can add zero-config support for additional adapters by editing [adapters.js](https://github.com/sveltejs/kit/blob/main/packages/adapter-auto/adapters.js) and opening a pull request.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/25-build-and-deploy/30-adapter-auto.md) [[llms.txt](https://kit.svelte.dev/docs/kit/adapter-auto/llms.txt)]

 previous next [[Adapters](https://kit.svelte.dev/docs/kit/adapters)] [[Node servers](https://kit.svelte.dev/docs/kit/adapter-node)]

---

# Cloudflare

> Cloudflare • SvelteKit documentation

To deploy to [Cloudflare Workers](https://workers.cloudflare.com/) or [Cloudflare Pages](https://pages.cloudflare.com/), use [adapter-cloudflare](https://github.com/sveltejs/kit/tree/main/packages/adapter-cloudflare).

This adapter will be installed by default when you use [adapter-auto](https://kit.svelte.dev/docs/adapter-auto). If you plan on staying with Cloudflare, you can switch from [adapter-auto](https://kit.svelte.dev/docs/adapter-auto) to using this adapter directly so that `event.platform` is emulated during local development, type declarations are automatically applied, and the ability to set Cloudflare-specific options is provided.

## Comparisons

- `adapter-cloudflare` – supports all SvelteKit features; builds for Cloudflare Workers Static Assets and Cloudflare Pages
- `adapter-cloudflare-workers` – deprecated. Supports all SvelteKit features; builds for Cloudflare Workers Sites
- `adapter-static` – only produces client-side static assets; compatible with Cloudflare Workers Static Assets and Cloudflare Pages

## Usage

Install with `npm i -D @sveltejs/adapter-cloudflare`, then add the adapter to your `svelte.config.js`:

 svelte.config

```
import import adapteradapter from '@sveltejs/adapter-cloudflare';

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
			// See below for an explanation of these options
			config: undefinedconfig: var undefinedundefined,
			platformProxy: {
    configPath: undefined;
    environment: undefined;
    persist: undefined;
}platformProxy: {
				configPath: undefinedconfigPath: var undefinedundefined,
				environment: undefinedenvironment: var undefinedundefined,
				persist: undefinedpersist: var undefinedundefined
			},
			fallback: stringfallback: 'plaintext',
			routes: {
    include: string[];
    exclude: string[];
}routes: {
				include: string[]include: ['/*'],
				exclude: string[]exclude: ['<all>']
			}
		})
	}
};

export default const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config;
```

## Options

### config

Path to your [Wrangler configuration file](https://developers.cloudflare.com/workers/wrangler/configuration/). If you would like to use a Wrangler configuration filename other than `wrangler.jsonc`, `wrangler.json`, or `wrangler.toml` you can specify it using this option.

### platformProxy

Preferences for the emulated `platform.env` local bindings. See the [getPlatformProxy](https://developers.cloudflare.com/workers/wrangler/api/#parameters-1) Wrangler API documentation for a full list of options.

### fallback

Whether to render a plaintext 404.html page or a rendered SPA fallback page for non-matching asset requests.

For Cloudflare Workers, the default behaviour is to return a null-body 404-status response for non-matching assets requests. However, if the [assets.not_found_handling](https://developers.cloudflare.com/workers/static-assets/routing/#2-not_found_handling) Wrangler configuration setting is set to `"404-page"`, this page will be served if a request fails to match an asset. If `assets.not_found_handling` is set to `"single-page-application"`, the adapter will render a SPA fallback `index.html` page regardless of the `fallback` option specified.

For Cloudflare Pages, this page will only be served when a request that matches an entry in `routes.exclude` fails to match an asset.

Most of the time `plaintext` is sufficient, but if you are using `routes.exclude` to manually exclude a set of prerendered pages without exceeding the 100 route limit, you may wish to use `spa` instead to avoid showing an unstyled 404 page to users.

See Cloudflare Pages’ [Not Found behaviour](https://developers.cloudflare.com/pages/configuration/serving-pages/#not-found-behavior) for more info.

### routes

Only for Cloudflare Pages. Allows you to customise the [_routes.json](https://developers.cloudflare.com/pages/functions/routing/#create-a-_routesjson-file) file generated by `adapter-cloudflare`.

- `include` defines routes that will invoke a function, and defaults to `['/*']`
- `exclude` defines routes that will *not* invoke a function — this is a faster and cheaper way to serve your app’s static assets. This array can include the following special values:
  - `<build>` contains your app’s build artifacts (the files generated by Vite)
  - `<files>` contains the contents of your `static` directory
  - `<prerendered>` contains a list of prerendered pages
  - `<all>` (the default) contains all of the above

You can have up to 100 `include` and `exclude` rules combined. Generally you can omit the `routes` options, but if (for example) your `<prerendered>` paths exceed that limit, you may find it helpful to manually create an `exclude` list that includes `'/articles/*'` instead of the auto-generated `['/articles/foo', '/articles/bar', '/articles/baz', ...]`.

## Cloudflare Workers

### Basic configuration

When building for Cloudflare Workers, this adapter expects to find a [Wrangler configuration file](https://developers.cloudflare.com/workers/configuration/sites/configuration/) in the project root. It should look something like this:

 wrangler

```
{
	"name": "<any-name-you-want>",
	"main": ".svelte-kit/cloudflare/_worker.js",
	"compatibility_date": "<YYYY-MM-DD>",
	"assets": {
		"binding": "ASSETS",
		"directory": ".svelte-kit/cloudflare",
	}
}
```

### Deployment

You can use the Wrangler CLI to deploy your application by running `npx wrangler deploy` or use the [Cloudflare Git integration](https://developers.cloudflare.com/workers/ci-cd/builds/) to enable automatic builds and deployments on push.

## Cloudflare Pages

### Deployment

Please follow the [Get Started Guide](https://developers.cloudflare.com/pages/get-started/) for Cloudflare Pages to begin.

If you’re using the [Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/), your build settings should look like this:

- Framework preset – SvelteKit
- Build command – `npm run build` or `vite build`
- Build output directory – `.svelte-kit/cloudflare`

### Further reading

You may wish to refer to [Cloudflare’s documentation for deploying a SvelteKit site on Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-a-svelte-kit-site/).

### Notes

Functions contained in the [/functionsdirectory](https://developers.cloudflare.com/pages/functions/routing/) at the project’s root will *not* be included in the deployment. Instead, functions should be implemented as [server endpoints](https://kit.svelte.dev/docs/routing#server) in your SvelteKit app, which is compiled to a [single_worker.jsfile](https://developers.cloudflare.com/pages/functions/advanced-mode/).

## Runtime APIs

The [env](https://developers.cloudflare.com/workers/runtime-apis/fetch-event#parameters) object contains your project’s [bindings](https://developers.cloudflare.com/workers/runtime-apis/bindings/), which consist of KV/DO namespaces, etc. It is passed to SvelteKit via the `platform` property, along with [ctx](https://developers.cloudflare.com/workers/runtime-apis/context/), [caches](https://developers.cloudflare.com/workers/runtime-apis/cache/), and [cf](https://developers.cloudflare.com/workers/runtime-apis/request/#incomingrequestcfproperties), meaning that you can access it in hooks and endpoints:

 +server

```
/** @type {import('./$types').RequestHandler} */
export async function POST({ request: RequestThe original request object.
request, platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform }) {
	const const x: DurableObjectId | undefinedx = platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform?.env: {
    YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace;
}env.type YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace<undefined>YOUR_DURABLE_OBJECT_NAMESPACE.DurableObjectNamespace<undefined>.idFromName(name: string): DurableObjectIdidFromName('x');
}
```

```
import type { type RequestHandler = (event: RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler } from './$types';
export const POST: type RequestHandler = (event: RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler = async ({ request: RequestThe original request object.
request, platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform }) => {
	const const x: DurableObjectId | undefinedx = platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform?.env: {
    YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace;
}env.type YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace<undefined>YOUR_DURABLE_OBJECT_NAMESPACE.DurableObjectNamespace<undefined>.idFromName(name: string): DurableObjectIdidFromName('x');
};
```

> SvelteKit’s built-in [$envmodule](https://kit.svelte.dev/docs/$env-static-private) should be preferred for environment variables.

To make these types available to your app, install [@cloudflare/workers-types](https://www.npmjs.com/package/@cloudflare/workers-types) and reference them in your `src/app.d.ts`:

 src/app.d

```
import { interface KVNamespace<Key extends string = string>KVNamespace, interface DurableObjectNamespace<T extends Rpc.DurableObjectBranded | undefined = undefined>DurableObjectNamespace } from '@cloudflare/workers-types';

declare global {
	namespace App {
		interface interface App.PlatformIf your adapter provides platform-specific context via event.platform, you can specify it here.
Platform {
			App.Platform.env: {
    YOUR_KV_NAMESPACE: KVNamespace;
    YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace;
}env: {
				type YOUR_KV_NAMESPACE: KVNamespace<string>YOUR_KV_NAMESPACE: interface KVNamespace<Key extends string = string>KVNamespace;
				type YOUR_DURABLE_OBJECT_NAMESPACE: DurableObjectNamespace<undefined>YOUR_DURABLE_OBJECT_NAMESPACE: interface DurableObjectNamespace<T extends Rpc.DurableObjectBranded | undefined = undefined>DurableObjectNamespace;
			};
		}
	}
}

export {};
```

### Testing locally

Cloudflare specific values in the `platform` property are emulated during dev and preview modes. Local [bindings](https://developers.cloudflare.com/workers/wrangler/configuration/#bindings) are created based on your [Wrangler configuration file](https://developers.cloudflare.com/workers/wrangler/) and are used to populate `platform.env` during development and preview. Use the adapter config [platformProxyoption](#Options-platformProxy) to change your preferences for the bindings.

For testing the build, you should use [Wrangler](https://developers.cloudflare.com/workers/wrangler/) version 4. Once you have built your site, run `wrangler dev .svelte-kit/cloudflare/_worker.js` if you’re testing for Cloudflare Workers or `wrangler pages dev .svelte-kit/cloudflare` for Cloudflare Pages.

## Headers and redirects

The [_headers](https://developers.cloudflare.com/pages/configuration/headers/) and [_redirects](https://developers.cloudflare.com/pages/configuration/redirects/) files, specific to Cloudflare, can be used for static asset responses (like images) by putting them into the project root folder.

However, they will have no effect on responses dynamically rendered by SvelteKit, which should return custom headers or redirect responses from [server endpoints](https://kit.svelte.dev/docs/routing#server) or with the [handle](https://kit.svelte.dev/docs/hooks#Server-hooks-handle) hook.

## Troubleshooting

### Node.js compatibility

If you would like to enable [Node.js compatibility](https://developers.cloudflare.com/workers/runtime-apis/nodejs/), you can add the `nodejs_compat` compatibility flag to your Wrangler configuration file:

 wrangler

```
{
	"compatibility_flags": ["nodejs_compat"]
}
```

### Worker size limits

When deploying your application, the server generated by SvelteKit is bundled into a single file. Wrangler will fail to publish your worker if it exceeds [the size limits](https://developers.cloudflare.com/workers/platform/limits/#worker-size) after minification. You’re unlikely to hit this limit usually, but some large libraries can cause this to happen. In that case, you can try to reduce the size of your worker by only importing such libraries on the client side. See [the FAQ](https://kit.svelte.dev/docs/faq#How-do-I-use-a-client-side-library-accessing-document-or-window) for more information.

### Accessing the file system

You can’t use `fs` in Cloudflare Workers.

Instead, use the [read](https://kit.svelte.dev/docs/$app-server#read) function from `$app/server` to access your files. It works by fetching the file from the deployed public assets location.

Alternatively, you can [prerender](https://kit.svelte.dev/docs/page-options#prerender) the routes in question.

## Migrating from Workers Sites

Cloudflare no longer recommends using [Workers Sites](https://developers.cloudflare.com/workers/configuration/sites/configuration/) and instead recommends using [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/). To migrate, replace `@sveltejs/adapter-cloudflare-workers` with `@sveltejs/adapter-cloudflare` and remove all `site` configuration settings from your Wrangler configuration file, then add the `assets.directory` and `assets.binding` configuration settings:

### svelte.config.js

svelte.config

```
import adapter from '@sveltejs/adapter-cloudflare-workers';
import import adapteradapter from '@sveltejs/adapter-cloudflare';

/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    adapter: any;
}kit: {
		adapter: anyadapter: import adapteradapter()
	}
};

export default const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config;
```

### wrangler.toml

wrangler

```
site.bucket = ".cloudflare/public"
assets.directory = ".cloudflare/public"
assets.binding = "ASSETS" # Exclude this if you don't have a `main` key configured.
```

### wrangler.jsonc

wrangler

```
{
	"site": {
		"bucket": ".cloudflare/public"
	},
	"assets": {
		"directory": ".cloudflare/public",
		"binding": "ASSETS" // Exclude this if you don't have a `main` key configured.
	}
}
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/25-build-and-deploy/60-adapter-cloudflare.md) [[llms.txt](https://kit.svelte.dev/docs/kit/adapter-cloudflare/llms.txt)]

 previous next [[Single-page apps](https://kit.svelte.dev/docs/kit/single-page-apps)] [[Cloudflare Workers](https://kit.svelte.dev/docs/kit/adapter-cloudflare-workers)]

---

# Netlify

> Netlify • SvelteKit documentation

To deploy to Netlify, use [adapter-netlify](https://github.com/sveltejs/kit/tree/main/packages/adapter-netlify).

This adapter will be installed by default when you use [adapter-auto](https://kit.svelte.dev/docs/adapter-auto), but adding it to your project allows you to specify Netlify-specific options.

## Usage

Install with `npm i -D @sveltejs/adapter-netlify`, then add the adapter to your `svelte.config.js`:

 svelte.config

```
import import adapteradapter from '@sveltejs/adapter-netlify';

/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    adapter: any;
}kit: {
		// default options are shown
		adapter: anyadapter: import adapteradapter({
			// if true, will create a Netlify Edge Function rather
			// than using standard Node-based functions
			edge: booleanedge: false,

			// if true, will split your app into multiple functions
			// instead of creating a single one for the entire app.
			// if `edge` is true, this option cannot be used
			split: booleansplit: false
		})
	}
};

export default const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config;
```

Then, make sure you have a [netlify.toml](https://docs.netlify.com/configure-builds/file-based-configuration) file in the project root. This will determine where to write static assets based on the `build.publish` settings, as per this sample configuration:

```
[build]
	command = "npm run build"
	publish = "build"
```

If the `netlify.toml` file or the `build.publish` value is missing, a default value of `"build"` will be used. Note that if you have set the publish directory in the Netlify UI to something else then you will need to set it in `netlify.toml` too, or use the default value of `"build"`.

### Node version

New projects will use the current Node LTS version by default. However, if you’re upgrading a project you created a while ago it may be stuck on an older version. See [the Netlify docs](https://docs.netlify.com/configure-builds/manage-dependencies/#node-js-and-javascript) for details on manually specifying a current Node version.

## Netlify Edge Functions

SvelteKit supports [Netlify Edge Functions](https://docs.netlify.com/build/edge-functions/overview/). If you pass the option `edge: true` to the `adapter` function, server-side rendering will happen in a Deno-based edge function that’s deployed close to the site visitor. If set to `false` (the default), the site will deploy to Node-based Netlify Functions.

 svelte.config

```
import import adapteradapter from '@sveltejs/adapter-netlify';

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
			// will create a Netlify Edge Function using Deno-based
			// rather than using standard Node-based functions
			edge: booleanedge: true
		})
	}
};

export default const config: {
    kit: {
        adapter: any;
    };
}@type{import('@sveltejs/kit').Config}config;
```

## Netlify alternatives to SvelteKit functionality

You may build your app using functionality provided directly by SvelteKit without relying on any Netlify functionality. Using the SvelteKit versions of these features will allow them to be used in dev mode, tested with integration tests, and to work with other adapters should you ever decide to switch away from Netlify. However, in some scenarios you may find it beneficial to use the Netlify versions of these features. One example would be if you’re migrating an app that’s already hosted on Netlify to SvelteKit.

### _headers and _redirects

The [_headers](https://docs.netlify.com/routing/headers/#syntax-for-the-headers-file) and [_redirects](https://docs.netlify.com/routing/redirects/redirect-options/) files specific to Netlify can be used for static asset responses (like images) by putting them into the project root folder.

### Redirect rules

During compilation, redirect rules are automatically appended to your `_redirects` file. (If it doesn’t exist yet, it will be created.) That means:

- `[[redirects]]` in `netlify.toml` will never match as `_redirects` has a [higher priority](https://docs.netlify.com/routing/redirects/#rule-processing-order). So always put your rules in the [_redirectsfile](https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file).
- `_redirects` shouldn’t have any custom “catch all” rules such as `/* /foobar/:splat`. Otherwise the automatically appended rule will never be applied as Netlify is only processing [the first matching rule](https://docs.netlify.com/routing/redirects/#rule-processing-order).

### Netlify Forms

1. Create your Netlify HTML form as described [here](https://docs.netlify.com/forms/setup/#html-forms), e.g. as `/routes/contact/+page.svelte`. (Don’t forget to add the hidden `form-name` input element!)
2. Netlify’s build bot parses your HTML files at deploy time, which means your form must be [prerendered](https://kit.svelte.dev/docs/page-options#prerender) as HTML. You can either add `export const prerender = true` to your `contact.svelte` to prerender just that page or set the `kit.prerender.force: true` option to prerender all pages.
3. If your Netlify form has a [custom success message](https://docs.netlify.com/forms/setup/#success-messages) like `<form netlify ... action="/success">` then ensure the corresponding `/routes/success/+page.svelte` exists and is prerendered.

### Netlify Functions

With this adapter, SvelteKit endpoints are hosted as [Netlify Functions](https://docs.netlify.com/functions/overview/). Netlify function handlers have additional context, including [Netlify Identity](https://docs.netlify.com/visitor-access/identity/) information. You can access this context via the `event.platform.context` field inside your hooks and `+page.server` or `+layout.server` endpoints. These are [serverless functions](https://docs.netlify.com/functions/overview/) when the `edge` property is `false` in the adapter config or [edge functions](https://docs.netlify.com/edge-functions/overview/#app) when it is `true`.

 +page.server

```
/** @type {import('./$types').PageServerLoad} */
export const const load: PageServerLoad@type{import('./$types').PageServerLoad}load = async (event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>event) => {
	const const context: anycontext = event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>event.RequestEvent<Record<string, any>, string | null>.platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform?.context;
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
@sincev0.1.100log(const context: anycontext); // shows up in your functions log in the Netlify app
};
```

```
import type { type PageServerLoad = (event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>PageServerLoad } from './$types';

export const const load: PageServerLoadload: type PageServerLoad = (event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>) => MaybePromise<void | Record<string, any>>PageServerLoad = async (event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>event) => {
	const const context: anycontext = event: ServerLoadEvent<Record<string, any>, Record<string, any>, string | null>event.RequestEvent<Record<string, any>, string | null>.platform: Readonly<App.Platform> | undefinedAdditional data made available through the adapter.
platform?.context;
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
@sincev0.1.100log(const context: anycontext); // shows up in your functions log in the Netlify app
};
```

Additionally, you can add your own Netlify functions by creating a directory for them and adding the configuration to your `netlify.toml` file. For example:

```
[build]
	command = "npm run build"
	publish = "build"

[functions]
	directory = "functions"
```

## Troubleshooting

### Accessing the file system

You can’t use `fs` in edge deployments.

You *can* use it in serverless deployments, but it won’t work as expected, since files are not copied from your project into your deployment. Instead, use the [read](https://kit.svelte.dev/docs/$app-server#read) function from `$app/server` to access your files. It also works inside edge deployments by fetching the file from the deployed public assets location.

Alternatively, you can [prerender](https://kit.svelte.dev/docs/page-options#prerender) the routes in question.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/25-build-and-deploy/80-adapter-netlify.md) [[llms.txt](https://kit.svelte.dev/docs/kit/adapter-netlify/llms.txt)]

 previous next [[Cloudflare Workers](https://kit.svelte.dev/docs/kit/adapter-cloudflare-workers)] [[Vercel](https://kit.svelte.dev/docs/kit/adapter-vercel)]
