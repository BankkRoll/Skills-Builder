# Images and more

# Images

> Images • SvelteKit documentation

Images can have a big impact on your app’s performance. For best results, you should optimize them by doing the following:

- generate optimal formats like `.avif` and `.webp`
- create different sizes for different screens
- ensure that assets can be cached effectively

Doing this manually is tedious. There are a variety of techniques you can use, depending on your needs and preferences.

## Vite’s built-in handling

[Vite will automatically process imported assets](https://vitejs.dev/guide/assets.html) for improved performance. This includes assets referenced via the CSS `url()` function. Hashes will be added to the filenames so that they can be cached, and assets smaller than `assetsInlineLimit` will be inlined. Vite’s asset handling is most often used for images, but is also useful for video, audio, etc.

```
<script>
	import logo from '$lib/assets/logo.png';
</script>

<img alt="The project logo" src={logo} />
```

## @sveltejs/enhanced-img

`@sveltejs/enhanced-img` is a plugin offered on top of Vite’s built-in asset handling. It provides plug and play image processing that serves smaller file formats like `avif` or `webp`, automatically sets the intrinsic `width` and `height` of the image to avoid layout shift, creates images of multiple sizes for various devices, and strips EXIF data for privacy. It will work in any Vite-based project including, but not limited to, SvelteKit projects.

> As a build plugin, `@sveltejs/enhanced-img` can only optimize files located on your machine during the build process. If you have an image located elsewhere (such as a path served from your database, CMS, or backend), please read about [loading images dynamically from a CDN](#Loading-images-dynamically-from-a-CDN).

### Setup

Install:

```
npm i -D @sveltejs/enhanced-img
```

Adjust `vite.config.js`:

```
import { function sveltekit(): Promise<Plugin$1<any>[]>Returns the SvelteKit Vite plugins.
sveltekit } from '@sveltejs/kit/vite';
import { function enhancedImages(): Promise<Plugin$1[]>enhancedImages } from '@sveltejs/enhanced-img';
import { function defineConfig(config: UserConfig): UserConfig (+5 overloads)Type helper to make it easier to use vite.config.ts
accepts a direct
{@link
UserConfig
}
 object, or a function that returns it.
The function receives a
{@link
ConfigEnv
}
 object.
defineConfig } from 'vite';

export default function defineConfig(config: UserConfig): UserConfig (+5 overloads)Type helper to make it easier to use vite.config.ts
accepts a direct
{@link
UserConfig
}
 object, or a function that returns it.
The function receives a
{@link
ConfigEnv
}
 object.
defineConfig({
	UserConfig.plugins?: PluginOption[] | undefinedArray of vite plugins to use.
plugins: [
		function enhancedImages(): Promise<Plugin$1[]>enhancedImages(), // must come before the SvelteKit plugin
		function sveltekit(): Promise<Plugin$1<any>[]>Returns the SvelteKit Vite plugins.
sveltekit()
	]
});
```

Building will take longer on the first build due to the computational expense of transforming images. However, the build output will be cached in `./node_modules/.cache/imagetools` so that subsequent builds will be fast.

### Basic usage

Use in your `.svelte` components by using `<enhanced:img>` rather than `<img>` and referencing the image file with a [Vite asset import](https://vitejs.dev/guide/assets.html#static-asset-handling) path:

```
<enhanced:img src="./path/to/your/image.jpg" alt="An alt text" />
```

At build time, your `<enhanced:img>` tag will be replaced with an `<img>` wrapped by a `<picture>` providing multiple image types and sizes. It’s only possible to downscale images without losing quality, which means that you should provide the highest resolution image that you need — smaller versions will be generated for the various device types that may request an image.

You should provide your image at 2x resolution for HiDPI displays (a.k.a. retina displays). `<enhanced:img>` will automatically take care of serving smaller versions to smaller devices.

> if you wish to use a [tag name CSS selector](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Basic_selectors#type_selectors) in your `<style>` block you will need to write `enhanced\:img` to escape the colon in the tag name.

### Dynamically choosing an image

You can also manually import an image asset and pass it to an `<enhanced:img>`. This is useful when you have a collection of static images and would like to dynamically choose one or [iterate over them](https://github.com/sveltejs/kit/blob/0ab1733e394b6310895a1d3bf0f126ce34531170/sites/kit.svelte.dev/src/routes/home/Showcase.svelte). In this case you will need to update both the `import` statement and `<img>` element as shown below to indicate you’d like process them.

```
<script>
	import MyImage from './path/to/your/image.jpg?enhanced';
</script>

<enhanced:img src={MyImage} alt="some alt text" />
```

You can also use [Vite’simport.meta.glob](https://vitejs.dev/guide/features.html#glob-import). Note that you will have to specify `enhanced` via a [custom query](https://vitejs.dev/guide/features.html#custom-queries):

```
<script>
	const imageModules = import.meta.glob(
		'/path/to/assets/*.{avif,gif,heif,jpeg,jpg,png,tiff,webp}',
		{
			eager: true,
			query: {
				enhanced: true
			}
		}
	)
</script>

{#each Object.entries(imageModules) as [_path, module]}
	<enhanced:img src={module.default} alt="some alt text" />
{/each}
```

> svg images are currently only supported statically

### Intrinsic Dimensions

`width` and `height` are optional as they can be inferred from the source image and will be automatically added when the `<enhanced:img>` tag is preprocessed. With these attributes, the browser can reserve the correct amount of space, preventing [layout shift](https://web.dev/articles/cls). If you’d like to use a different `width` and `height` you can style the image with CSS. Because the preprocessor adds a `width` and `height` for you, if you’d like one of the dimensions to be automatically calculated then you will need to specify that:

```
<style>
	.hero-image img {
		width: var(--size);
		height: auto;
	}
</style>
```

### srcset and sizes

If you have a large image, such as a hero image taking the width of the design, you should specify `sizes` so that smaller versions are requested on smaller devices. E.g. if you have a 1280px image you may want to specify something like:

```
<enhanced:img src="./image.png" sizes="min(1280px, 100vw)"/>
```

If `sizes` is specified, `<enhanced:img>` will generate small images for smaller devices and populate the `srcset` attribute.

The smallest picture generated automatically will have a width of 540px. If you’d like smaller images or would otherwise like to specify custom widths, you can do that with the `w` query parameter:

```
<enhanced:img
  src="./image.png?w=1280;640;400"
  sizes="(min-width:1920px) 1280px, (min-width:1080px) 640px, (min-width:768px) 400px"
/>
```

If `sizes` is not provided, then a HiDPI/Retina image and a standard resolution image will be generated. The image you provide should be 2x the resolution you wish to display so that the browser can display that image on devices with a high [device pixel ratio](https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio).

### Per-image transforms

By default, enhanced images will be transformed to more efficient formats. However, you may wish to apply other transforms such as a blur, quality, flatten, or rotate operation. You can run per-image transforms by appending a query string:

```
<enhanced:img src="./path/to/your/image.jpg?blur=15" alt="An alt text" />
```

[See the imagetools repo for the full list of directives](https://github.com/JonasKruckenberg/imagetools/blob/main/docs/directives.md).

## Loading images dynamically from a CDN

In some cases, the images may not be accessible at build time — e.g. they may live inside a content management system or elsewhere.

Using a content delivery network (CDN) can allow you to optimize these images dynamically, and provides more flexibility with regards to sizes, but it may involve some setup overhead and usage costs. Depending on caching strategy, the browser may not be able to use a cached copy of the asset until a [304 response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) is received from the CDN. Building HTML to target CDNs allows using an `<img>` tag since the CDN can serve the appropriate format based on the `User-Agent` header, whereas build-time optimizations must produce `<picture>` tags with multiple sources. Finally, some CDNs may generate images lazily, which could have a negative performance impact for sites with low traffic and frequently changing images.

CDNs can generally be used without any need for a library. However, there are a number of libraries with Svelte support that make it easier. [@unpic/svelte](https://unpic.pics/img/svelte/) is a CDN-agnostic library with support for a large number of providers. You may also find that specific CDNs like [Cloudinary](https://svelte.cloudinary.dev/) have Svelte support. Finally, some content management systems (CMS) which support Svelte (such as [Contentful](https://www.contentful.com/sveltekit-starter-guide/), [Storyblok](https://github.com/storyblok/storyblok-svelte), and [Contentstack](https://www.contentstack.com/docs/developers/sample-apps/build-a-starter-website-with-sveltekit-and-contentstack)) have built-in support for image handling.

## Best practices

- For each image type, use the appropriate solution from those discussed above. You can mix and match all three solutions in one project. For example, you may use Vite’s built-in handling to provide images for `<meta>` tags, display images on your homepage with `@sveltejs/enhanced-img`, and display user-submitted content with a dynamic approach.
- Consider serving all images via CDN regardless of the image optimization types you use. CDNs reduce latency by distributing copies of static assets globally.
- Your original images should have a good quality/resolution and should have 2x the width it will be displayed at to serve HiDPI devices. Image processing can size images down to save bandwidth when serving smaller screens, but it would be a waste of bandwidth to invent pixels to size images up.
- For images which are much larger than the width of a mobile device (roughly 400px), such as a hero image taking the width of the page design, specify `sizes` so that smaller images can be served on smaller devices.
- For important images, such as the [largest contentful paint (LCP)](https://web.dev/articles/lcp) image, set `fetchpriority="high"` and avoid `loading="lazy"` to prioritize loading as early as possible.
- Give the image a container or styling so that it is constrained and does not jump around while the page is loading affecting your [cumulative layout shift (CLS)](https://web.dev/articles/cls). `width` and `height` help the browser to reserve space while the image is still loading, so `@sveltejs/enhanced-img` will add a `width` and `height` for you.
- Always provide a good `alt` text. The Svelte compiler will warn you if you don’t do this.
- Do not use `em` or `rem` in `sizes` and change the default size of these measures. When used in `sizes` or `@media` queries, `em` and `rem` are both defined to mean the user’s default `font-size`. For a `sizes` declaration like `sizes="(min-width: 768px) min(100vw, 108rem), 64rem"`, the actual `em` or `rem` that controls how the image is laid out on the page can be different if changed by CSS. For example, do not do something like `html { font-size: 62.5%; }` as the slot reserved by the browser preloader will now end up being larger than the actual slot of the CSS object model once it has been created.

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/40-best-practices/07-images.md) [[llms.txt](https://kit.svelte.dev/docs/kit/images/llms.txt)]

 previous next [[Icons](https://kit.svelte.dev/docs/kit/icons)] [[Accessibility](https://kit.svelte.dev/docs/kit/accessibility)]

---

# Introduction

> Introduction • SvelteKit documentation

## Before we begin

> If you’re new to Svelte or SvelteKit we recommend checking out the [interactive tutorial](https://kit.svelte.dev/tutorial/kit).
>
>
>
> If you get stuck, reach out for help in the [Discord chatroom](https://kit.svelte.dev/chat).

## What is SvelteKit?

SvelteKit is a framework for rapidly developing robust, performant web applications using [Svelte](https://kit.svelte.dev/svelte). If you’re coming from React, SvelteKit is similar to Next. If you’re coming from Vue, SvelteKit is similar to Nuxt.

To learn more about the kinds of applications you can build with SvelteKit, see the [documentation regarding project types](https://kit.svelte.dev/docs/project-types).

## What is Svelte?

In short, Svelte is a way of writing user interface components — like a navigation bar, comment section, or contact form — that users see and interact with in their browsers. The Svelte compiler converts your components to JavaScript that can be run to render the HTML for the page and to CSS that styles the page. You don’t need to know Svelte to understand the rest of this guide, but it will help. If you’d like to learn more, check out [the Svelte tutorial](https://kit.svelte.dev/tutorial).

## SvelteKit vs Svelte

Svelte renders UI components. You can compose these components and render an entire page with just Svelte, but you need more than just Svelte to write an entire app.

SvelteKit helps you build web apps while following modern best practices and providing solutions to common development challenges. It offers everything from basic functionalities — like a [router](https://kit.svelte.dev/docs/glossary#Routing) that updates your UI when a link is clicked — to more advanced capabilities. Its extensive list of features includes [build optimizations](https://vitejs.dev/guide/features.html#build-optimizations) to load only the minimal required code; [offline support](https://kit.svelte.dev/docs/service-workers); [preloading](https://kit.svelte.dev/docs/link-options#data-sveltekit-preload-data) pages before user navigation; [configurable rendering](https://kit.svelte.dev/docs/page-options) to handle different parts of your app on the server via [SSR](https://kit.svelte.dev/docs/glossary#SSR), in the browser through [client-side rendering](https://kit.svelte.dev/docs/glossary#CSR), or at build-time with [prerendering](https://kit.svelte.dev/docs/glossary#Prerendering); [image optimization](https://kit.svelte.dev/docs/images); and much more. Building an app with all the modern best practices is fiendishly complicated, but SvelteKit does all the boring stuff for you so that you can get on with the creative part.

It reflects changes to your code in the browser instantly to provide a lightning-fast and feature-rich development experience by leveraging [Vite](https://vitejs.dev/) with a [Svelte plugin](https://github.com/sveltejs/vite-plugin-svelte) to do [Hot Module Replacement (HMR)](https://github.com/sveltejs/vite-plugin-svelte/blob/main/docs/config.md#hot).

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/10-getting-started/10-introduction.md) [[llms.txt](https://kit.svelte.dev/docs/kit/introduction/llms.txt)]

 previous next [!] [[Creating a project](https://kit.svelte.dev/docs/kit/creating-a-project)]

---

# Not found!

[! [[

# Not found!

If you were expecting to find something here, please drop by the [Discord chatroom](https://kit.svelte.dev/chat) and let us know, or raise an issue on [GitHub](https://github.com/sveltejs/svelte.dev/issues). Thanks!

]] ]

---

# Link options

> Link options • SvelteKit documentation

In SvelteKit, `<a>` elements (rather than framework-specific `<Link>` components) are used to navigate between the routes of your app. If the user clicks on a link whose `href` is ‘owned’ by the app (as opposed to, say, a link to an external site) then SvelteKit will navigate to the new page by importing its code and then calling any `load` functions it needs to fetch data.

You can customise the behaviour of links with `data-sveltekit-*` attributes. These can be applied to the `<a>` itself, or to a parent element.

These options also apply to `<form>` elements with [method="GET"](https://kit.svelte.dev/docs/form-actions#GET-vs-POST).

## data-sveltekit-preload-data

Before the browser registers that the user has clicked on a link, we can detect that they’ve hovered the mouse over it (on desktop) or that a `touchstart` or `mousedown` event was triggered. In both cases, we can make an educated guess that a `click` event is coming.

SvelteKit can use this information to get a head start on importing the code and fetching the page’s data, which can give us an extra couple of hundred milliseconds — the difference between a user interface that feels laggy and one that feels snappy.

We can control this behaviour with the `data-sveltekit-preload-data` attribute, which can have one of two values:

- `"hover"` means that preloading will start if the mouse comes to a rest over a link. On mobile, preloading begins on `touchstart`
- `"tap"` means that preloading will start as soon as a `touchstart` or `mousedown` event is registered

The default project template has a `data-sveltekit-preload-data="hover"` attribute applied to the `<body>` element in `src/app.html`, meaning that every link is preloaded on hover by default:

```
<body data-sveltekit-preload-data="hover">
	<div style="display: contents">%sveltekit.body%</div>
</body>
```

Sometimes, calling `load` when the user hovers over a link might be undesirable, either because it’s likely to result in false positives (a click needn’t follow a hover) or because data is updating very quickly and a delay could mean staleness.

In these cases, you can specify the `"tap"` value, which causes SvelteKit to call `load` only when the user taps or clicks on a link:

```
<a data-sveltekit-preload-data="tap" href="/stonks">
	Get current stonk values
</a>
```

> You can also programmatically invoke `preloadData` from `$app/navigation`.

Data will never be preloaded if the user has chosen reduced data usage, meaning [navigator.connection.saveData](https://developer.mozilla.org/en-US/docs/Web/API/NetworkInformation/saveData) is `true`.

## data-sveltekit-preload-code

Even in cases where you don’t want to preload *data* for a link, it can be beneficial to preload the *code*. The `data-sveltekit-preload-code` attribute works similarly to `data-sveltekit-preload-data`, except that it can take one of four values, in decreasing ‘eagerness’:

- `"eager"` means that links will be preloaded straight away
- `"viewport"` means that links will be preloaded once they enter the viewport
- `"hover"` - as above, except that only code is preloaded
- `"tap"` - as above, except that only code is preloaded

Note that `viewport` and `eager` only apply to links that are present in the DOM immediately following navigation — if a link is added later (in an `{#if ...}` block, for example) it will not be preloaded until triggered by `hover` or `tap`. This is to avoid performance pitfalls resulting from aggressively observing the DOM for changes.

> Since preloading code is a prerequisite for preloading data, this attribute will only have an effect if it specifies a more eager value than any `data-sveltekit-preload-data` attribute that is present.

As with `data-sveltekit-preload-data`, this attribute will be ignored if the user has chosen reduced data usage.

## data-sveltekit-reload

Occasionally, we need to tell SvelteKit not to handle a link, but allow the browser to handle it. Adding a `data-sveltekit-reload` attribute to a link...

```
<a data-sveltekit-reload href="/path">Path</a>
```

...will cause a full-page navigation when the link is clicked.

Links with a `rel="external"` attribute will receive the same treatment. In addition, they will be ignored during [prerendering](https://kit.svelte.dev/docs/page-options#prerender).

## data-sveltekit-replacestate

Sometimes you don’t want navigation to create a new entry in the browser’s session history. Adding a `data-sveltekit-replacestate` attribute to a link...

```
<a data-sveltekit-replacestate href="/path">Path</a>
```

...will replace the current `history` entry rather than creating a new one with `pushState` when the link is clicked.

## data-sveltekit-keepfocus

Sometimes you don’t want [focus to be reset](https://kit.svelte.dev/docs/accessibility#Focus-management) after navigation. For example, maybe you have a search form that submits as the user is typing, and you want to keep focus on the text input.  Adding a `data-sveltekit-keepfocus` attribute to it...

```
<form data-sveltekit-keepfocus>
	<input type="text" name="query">
</form>
```

...will cause the currently focused element to retain focus after navigation. In general, avoid using this attribute on links, since the focused element would be the `<a>` tag (and not a previously focused element) and screen reader and other assistive technology users often expect focus to be moved after a navigation. You should also only use this attribute on elements that still exist after navigation. If the element no longer exists, the user’s focus will be lost, making for a confusing experience for assistive technology users.

## data-sveltekit-noscroll

When navigating to internal links, SvelteKit mirrors the browser’s default navigation behaviour: it will change the scroll position to 0,0 so that the user is at the very top left of the page (unless the link includes a `#hash`, in which case it will scroll to the element with a matching ID).

In certain cases, you may wish to disable this behaviour. Adding a `data-sveltekit-noscroll` attribute to a link...

```
<a href="path" data-sveltekit-noscroll>Path</a>
```

...will prevent scrolling after the link is clicked.

## Disabling options

To disable any of these options inside an element where they have been enabled, use the `"false"` value:

```
<div data-sveltekit-preload-data>
	
	<a href="/a">a</a>
	<a href="/b">b</a>
	<a href="/c">c</a>

	<div data-sveltekit-preload-data="false">
		
		<a href="/d">d</a>
		<a href="/e">e</a>
		<a href="/f">f</a>
	</div>
</div>
```

To apply an attribute to an element conditionally, do this:

```
<div data-sveltekit-preload-data={condition ? 'hover' : false}>
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/30-advanced/30-link-options.md) [[llms.txt](https://kit.svelte.dev/docs/kit/link-options/llms.txt)]

 previous next [[Errors](https://kit.svelte.dev/docs/kit/errors)] [[Service workers](https://kit.svelte.dev/docs/kit/service-workers)]
