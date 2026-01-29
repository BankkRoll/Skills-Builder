# Remote functions

# Remote functions

> Remote functions • SvelteKit documentation

> Available since 2.27

Remote functions are a tool for type-safe communication between client and server. They can be *called* anywhere in your app, but always *run* on the server, meaning they can safely access [server-only modules](https://kit.svelte.dev/docs/server-only-modules) containing things like environment variables and database clients.

Combined with Svelte’s experimental support for [await](https://kit.svelte.dev/docs/svelte/await-expressions), it allows you to load and manipulate data directly inside your components.

This feature is currently experimental, meaning it is likely to contain bugs and is subject to change without notice. You must opt in by adding the `kit.experimental.remoteFunctions` option in your `svelte.config.js` and optionally, the `compilerOptions.experimental.async` option to use `await` in components:

 svelte.config

```
/** @type {import('@sveltejs/kit').Config} */
const const config: {
    kit: {
        experimental: {
 remoteFunctions: boolean;
        };
    };
    compilerOptions: {
        experimental: {
 async: boolean;
        };
    };
}@type{import('@sveltejs/kit').Config}config = {
	kit: {
    experimental: {
        remoteFunctions: boolean;
    };
}kit: {
		experimental: {
    remoteFunctions: boolean;
}experimental: {
			remoteFunctions: booleanremoteFunctions: true
		}
	},
	compilerOptions: {
    experimental: {
        async: boolean;
    };
}compilerOptions: {
		experimental: {
    async: boolean;
}experimental: {
			async: booleanasync: true
		}
	}
};

export default const config: {
    kit: {
        experimental: {
 remoteFunctions: boolean;
        };
    };
    compilerOptions: {
        experimental: {
 async: boolean;
        };
    };
}@type{import('@sveltejs/kit').Config}config;
```

## Overview

Remote functions are exported from a `.remote.js` or `.remote.ts` file, and come in four flavours: `query`, `form`, `command` and `prerender`. On the client, the exported functions are transformed to `fetch` wrappers that invoke their counterparts on the server via a generated HTTP endpoint. Remote files can be placed anywhere in your `src` directory (except inside the `src/lib/server` directory), and third party libraries can provide them, too.

## query

The `query` function allows you to read dynamic data from the server (for *static* data, consider using [prerender](#prerender) instead):

 src/routes/blog/data.remote

```
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getPosts: RemoteQueryFunction<void, any[]>getPosts = query<any[]>(fn: () => MaybePromise<any[]>): RemoteQueryFunction<void, any[]> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => {
	const const posts: any[]posts = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT title, slug
		FROM post
		ORDER BY published_at
		DESC
	`;

	return const posts: any[]posts;
});
```

> Throughout this page, you’ll see imports from fictional modules like `$lib/server/database` and `$lib/server/auth`. These are purely for illustrative purposes — you can use whatever database client and auth setup you like.
>
>
>
> The `db.sql` function above is a [tagged template function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates) that escapes any interpolated values.

The query returned from `getPosts` works as a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) that resolves to `posts`:

 src/routes/blog/+page

```
<script>
	import { getPosts } from './data.remote';
</script>

<h1>Recent posts</h1>

<ul>
	{#each await getPosts() as { title, slug }}
		<li><a href="/blog/{slug}">{title}</a></li>
	{/each}
</ul>
```

```
<script lang="ts">
	import { getPosts } from './data.remote';
</script>

<h1>Recent posts</h1>

<ul>
	{#each await getPosts() as { title, slug }}
		<li><a href="/blog/{slug}">{title}</a></li>
	{/each}
</ul>
```

Until the promise resolves — and if it errors — the nearest [<svelte:boundary>](https://kit.svelte.dev/svelte/svelte-boundary) will be invoked.

While using `await` is recommended, as an alternative the query also has `loading`, `error` and `current` properties:

 src/routes/blog/+page

```
<script>
	import { getPosts } from './data.remote';

	const query = getPosts();
</script>

<h1>Recent posts</h1>

{#if query.error}
	<p>oops!</p>
{:else if query.loading}
	<p>loading...</p>
{:else}
	<ul>
		{#each query.current as { title, slug }}
			<li><a href="/blog/{slug}">{title}</a></li>
		{/each}
	</ul>
{/if}
```

```
<script lang="ts">
	import { getPosts } from './data.remote';

	const query = getPosts();
</script>

<h1>Recent posts</h1>

{#if query.error}
	<p>oops!</p>
{:else if query.loading}
	<p>loading...</p>
{:else}
	<ul>
		{#each query.current as { title, slug }}
			<li><a href="/blog/{slug}">{title}</a></li>
		{/each}
	</ul>
{/if}
```

> For the rest of this document, we’ll use the `await` form.

### Query arguments

Query functions can accept an argument, such as the `slug` of an individual post:

 src/routes/blog/[slug]/+page

```
<script>
	import { getPost } from '../data.remote';

	let { params } = $props();

	const post = $derived(await getPost(params.slug));
</script>

<h1>{post.title}</h1>
<div>{@html post.content}</div>
```

```
<script lang="ts">
	import { getPost } from '../data.remote';

	let { params } = $props();

	const post = $derived(await getPost(params.slug));
</script>

<h1>{post.title}</h1>
<div>{@html post.content}</div>
```

Since `getPost` exposes an HTTP endpoint, it’s important to validate this argument to be sure that it’s the correct type. For this, we can use any [Standard Schema](https://standardschema.dev/) validation library such as [Zod](https://zod.dev/) or [Valibot](https://valibot.dev/):

 src/routes/blog/data.remote

```
import * as import vv from 'valibot';
import { function error(status: number, body: App.Error): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error } from '@sveltejs/kit';
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getPosts: RemoteQueryFunction<void, void>getPosts = query<void>(fn: () => MaybePromise<void>): RemoteQueryFunction<void, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => { /* ... */ });

export const const getPost: RemoteQueryFunction<string, any>getPost = query<v.StringSchema<undefined>, any>(schema: v.StringSchema<undefined>, fn: (arg: string) => any): RemoteQueryFunction<string, any> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (slug: stringslug) => {
	const [const post: anypost] = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT * FROM post
		WHERE slug = ${slug: stringslug}
	`;

	if (!const post: anypost) function error(status: number, body?: {
    message: string;
} extends App.Error ? App.Error | string | undefined : never): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error(404, 'Not found');
	return const post: anypost;
});
```

Both the argument and the return value are serialized with [devalue](https://github.com/sveltejs/devalue), which handles types like `Date` and `Map` (and custom types defined in your [transport hook](https://kit.svelte.dev/docs/hooks#Universal-hooks-transport)) in addition to JSON.

### Refreshing queries

Any query can be re-fetched via its `refresh` method, which retrieves the latest value from the server:

```
<button onclick={() => getPosts().refresh()}>
	Check for new posts
</button>
```

> Queries are cached while they’re on the page, meaning `getPosts() === getPosts()`. This means you don’t need a reference like `const posts = getPosts()` in order to update the query.

## query.batch

`query.batch` works like `query` except that it batches requests that happen within the same macrotask. This solves the so-called n+1 problem: rather than each query resulting in a separate database call (for example), simultaneous queries are grouped together.

On the server, the callback receives an array of the arguments the function was called with. It must return a function of the form `(input: Input, index: number) => Output`. SvelteKit will then call this with each of the input arguments to resolve the individual calls with their results.

 weather.remote

```
import * as import vv from 'valibot';
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getWeather: RemoteQueryFunction<string, any>getWeather = function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query.function query.batch<v.StringSchema<undefined>, any>(schema: v.StringSchema<undefined>, fn: (args: string[]) => MaybePromise<(arg: string, idx: number) => any>): RemoteQueryFunction<string, any> (+1 overload)Creates a batch query function that collects multiple calls and executes them in a single request
See Remote functions for full documentation.
@since2.35batch(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (cities: string[]cities) => {
	const const weather: any[]weather = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT * FROM weather
		WHERE city = ANY(${cities: string[]cities})
	`;
	const const lookup: Map<any, any>lookup = new var Map: MapConstructor
new <any, any>(iterable?: Iterable<readonly [any, any]> | null | undefined) => Map<any, any> (+3 overloads)Map(const weather: any[]weather.Array<any>.map<[any, any]>(callbackfn: (value: any, index: number, array: any[]) => [any, any], thisArg?: any): [any, any][]Calls a defined callback function on each element of an array, and returns an array that contains the results.
@paramcallbackfn A function that accepts up to three arguments. The map method calls the callbackfn function one time for each element in the array.@paramthisArg An object to which the this keyword can refer in the callbackfn function. If thisArg is omitted, undefined is used as the this value.map(w: anyw => [w: anyw.city, w: anyw]));

	return (city: stringcity) => const lookup: Map<any, any>lookup.Map<any, any>.get(key: any): anyReturns a specified element from the Map object. If the value that is associated to the provided key is an object, then you will get a reference to that object and any change made to that object will effectively modify it inside the Map.
@returnsReturns the element associated with the specified key. If no element is associated with the specified key, undefined is returned.get(city: stringcity);
});
```

Weather

```
<script>
	import CityWeather from './CityWeather.svelte';
	import { getWeather } from './weather.remote.js';

	let { cities } = $props();
	let limit = $state(5);
</script>

<h2>Weather</h2>

{#each cities.slice(0, limit) as city}
	<h3>{city.name}</h3>
	<CityWeather weather={await getWeather(city.id)} />
{/each}

{#if cities.length > limit}
	<button onclick={() => limit += 5}>
		Load more
	</button>
{/if}
```

```
<script lang="ts">
	import CityWeather from './CityWeather.svelte';
	import { getWeather } from './weather.remote.js';

	let { cities } = $props();
	let limit = $state(5);
</script>

<h2>Weather</h2>

{#each cities.slice(0, limit) as city}
	<h3>{city.name}</h3>
	<CityWeather weather={await getWeather(city.id)} />
{/each}

{#if cities.length > limit}
	<button onclick={() => limit += 5}>
		Load more
	</button>
{/if}
```

## form

The `form` function makes it easy to write data to the server. It takes a callback that receives `data` constructed from the submitted [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData)...

 src/routes/blog/data.remote

```
import * as import vv from 'valibot';
import { function error(status: number, body: App.Error): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error, function redirect(status: 300 | 301 | 302 | 303 | 304 | 305 | 306 | 307 | 308 | ({} & number), location: string | URL): neverRedirect a request. When called during request handling, SvelteKit will return a redirect response.
Make sure you’re not catching the thrown redirect, which would prevent SvelteKit from handling it.
Most common status codes:

303 See Other: redirect as a GET request (often used after a form POST request)
307 Temporary Redirect: redirect will keep the request method
308 Permanent Redirect: redirect will keep the request method, SEO will be transferred to the new page

See all redirect status codes
@paramstatus The HTTP status code. Must be in the range 300-308.@paramlocation The location to redirect to.@throwsRedirect This error instructs SvelteKit to redirect to the specified location.@throwsError If the provided status is invalid.redirect } from '@sveltejs/kit';
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query, function form<Output>(fn: () => MaybePromise<Output>): RemoteForm<void, Output> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';
import * as module "$lib/server/auth"auth from '$lib/server/auth';

export const const getPosts: RemoteQueryFunction<void, void>getPosts = query<void>(fn: () => MaybePromise<void>): RemoteQueryFunction<void, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => { /* ... */ });

export const const getPost: RemoteQueryFunction<string, void>getPost = query<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>): RemoteQueryFunction<string, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (slug: stringslug) => { /* ... */ });

export const const createPost: RemoteForm<{
    title: string;
    content: string;
}, never>createPost = form<v.ObjectSchema<{
    readonly title: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
    readonly content: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
}, undefined>, never>(validate: v.ObjectSchema<...>, fn: (data: {
    ...;
}) => Promise<...>): RemoteForm<...> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{
    readonly title: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
    readonly content: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
}>(entries: {
    readonly title: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
    readonly content: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		title: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>title: import vv.pipe<v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>>(schema: v.StringSchema<undefined>, item1: v.NonEmptyAction<string, undefined> | v.PipeAction<string, string, v.NonEmptyIssue<...>>): v.SchemaWithPipe<...> (+20 overloads)
export pipeAdds a pipeline to a schema, that can validate and transform its input.
@paramschema The root schema.@paramitem1 The first pipe item.@returnsA schema with a pipeline.pipe(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), import vv.nonEmpty<string>(): v.NonEmptyAction<string, undefined> (+1 overload)
export nonEmptyCreates a non-empty validation action.
@returnsA non-empty action.nonEmpty()),
		content: v.SchemaWithPipe<readonly [v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>]>content:import vv.pipe<v.StringSchema<undefined>, v.NonEmptyAction<string, undefined>>(schema: v.StringSchema<undefined>, item1: v.NonEmptyAction<string, undefined> | v.PipeAction<string, string, v.NonEmptyIssue<...>>): v.SchemaWithPipe<...> (+20 overloads)
export pipeAdds a pipeline to a schema, that can validate and transform its input.
@paramschema The root schema.@paramitem1 The first pipe item.@returnsA schema with a pipeline.pipe(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), import vv.nonEmpty<string>(): v.NonEmptyAction<string, undefined> (+1 overload)
export nonEmptyCreates a non-empty validation action.
@returnsA non-empty action.nonEmpty())
	}),
	async ({ title: stringtitle, content: stringcontent }) => {
		// Check the user is logged in
		const const user: auth.User | nulluser = await module "$lib/server/auth"auth.function getUser(): Promise<auth.User | null>Gets a user’s info from their cookies, using getRequestEvent
getUser();
		if (!const user: auth.User | nulluser) function error(status: number, body?: {
    message: string;
} extends App.Error ? App.Error | string | undefined : never): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error(401, 'Unauthorized');

		const const slug: stringslug = title: stringtitle.String.toLowerCase(): stringConverts all the alphabetic characters in a string to lowercase.
toLowerCase().String.replace(searchValue: {
    [Symbol.replace](string: string, replaceValue: string): string;
}, replaceValue: string): string (+3 overloads)Passes a string and
{@linkcode
replaceValue
}
 to the [Symbol.replace] method on
{@linkcode
searchValue
}
. This method is expected to implement its own replacement algorithm.
@paramsearchValue An object that supports searching for and replacing matches within a string.@paramreplaceValue The replacement text.replace(/ /g, '-');

		// Insert into the database
		await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
			INSERT INTO post (slug, title, content)
			VALUES (${const slug: stringslug}, ${title: stringtitle}, ${content: stringcontent})
		`;

		// Redirect to the newly created page
		function redirect(status: 300 | 301 | 302 | 303 | 304 | 305 | 306 | 307 | 308 | ({} & number), location: string | URL): neverRedirect a request. When called during request handling, SvelteKit will return a redirect response.
Make sure you’re not catching the thrown redirect, which would prevent SvelteKit from handling it.
Most common status codes:

303 See Other: redirect as a GET request (often used after a form POST request)
307 Temporary Redirect: redirect will keep the request method
308 Permanent Redirect: redirect will keep the request method, SEO will be transferred to the new page

See all redirect status codes
@paramstatus The HTTP status code. Must be in the range 300-308.@paramlocation The location to redirect to.@throwsRedirect This error instructs SvelteKit to redirect to the specified location.@throwsError If the provided status is invalid.redirect(303, `/blog/${const slug: stringslug}`);
	}
);
```

...and returns an object that can be spread onto a `<form>` element. The callback is called whenever the form is submitted.

 src/routes/blog/new/+page

```
<script>
	import { createPost } from '../data.remote';
</script>

<h1>Create a new post</h1>

<form {...createPost}>
	

	<button>Publish!</button>
</form>
```

```
<script lang="ts">
	import { createPost } from '../data.remote';
</script>

<h1>Create a new post</h1>

<form {...createPost}>
	

	<button>Publish!</button>
</form>
```

The form object contains `method` and `action` properties that allow it to work without JavaScript (i.e. it submits data and reloads the page). It also has an [attachment](https://kit.svelte.dev/docs/svelte/@attach) that progressively enhances the form when JavaScript is available, submitting data *without* reloading the entire page.

As with `query`, if the callback uses the submitted `data`, it should be [validated](#query-Query-arguments) by passing a [Standard Schema](https://standardschema.dev) as the first argument to `form`.

### Fields

A form is composed of a set of *fields*, which are defined by the schema. In the case of `createPost`, we have two fields, `title` and `content`, which are both strings. To get the attributes for a field, call its `.as(...)` method, specifying which [input type](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input#input_types) to use:

```
<form {...createPost}>
	<label>
		<h2>Title</h2>
		<input {...createPost.fields.title.as('text')} />
	</label>

	<label>
		<h2>Write your post</h2>
		<textarea {...createPost.fields.content.as('text')}></textarea>
	</label>

	<button>Publish!</button>
</form>
```

These attributes allow SvelteKit to set the correct input type, set a `name` that is used to construct the `data` passed to the handler, populate the `value` of the form (for example following a failed submission, to save the user having to re-enter everything), and set the [aria-invalid](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid) state.

> The generated `name` attribute uses JS object notation (e.g. `nested.array[0].value`). String keys that require quotes such as `object['nested-array'][0].value` are not supported. Under the hood, boolean checkbox and number field names are prefixed with `b:` and `n:`, respectively, to signal SvelteKit to coerce the values from strings prior to validation.

Fields can be nested in objects and arrays, and their values can be strings, numbers, booleans or `File` objects. For example, if your schema looked like this...

 data.remote

```
const const datingProfile: v.ObjectSchema<{
    readonly name: v.StringSchema<undefined>;
    readonly photo: v.FileSchema<undefined>;
    readonly info: v.ObjectSchema<{
        readonly height: v.NumberSchema<undefined>;
        readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
    }, undefined>;
    readonly attributes: v.ArraySchema<...>;
}, undefined>datingProfile = import vv.object<{
    readonly name: v.StringSchema<undefined>;
    readonly photo: v.FileSchema<undefined>;
    readonly info: v.ObjectSchema<{
        readonly height: v.NumberSchema<undefined>;
        readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
    }, undefined>;
    readonly attributes: v.ArraySchema<...>;
}>(entries: {
    readonly name: v.StringSchema<undefined>;
    readonly photo: v.FileSchema<undefined>;
    readonly info: v.ObjectSchema<{
        readonly height: v.NumberSchema<undefined>;
        readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
    }, undefined>;
    readonly attributes: v.ArraySchema<...>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
	name: v.StringSchema<undefined>name: import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
	photo: v.FileSchema<undefined>photo: import vv.function file(): v.FileSchema<undefined> (+1 overload)
export fileCreates a file schema.
@returnsA file schema.file(),
	info: v.ObjectSchema<{
    readonly height: v.NumberSchema<undefined>;
    readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
}, undefined>info: import vv.object<{
    readonly height: v.NumberSchema<undefined>;
    readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
}>(entries: {
    readonly height: v.NumberSchema<undefined>;
    readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		height: v.NumberSchema<undefined>height: import vv.function number(): v.NumberSchema<undefined> (+1 overload)
export numberCreates a number schema.
@returnsA number schema.number(),
		likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>likesDogs: import vv.optional<v.BooleanSchema<undefined>, false>(wrapped: v.BooleanSchema<undefined>, default_: false): v.OptionalSchema<v.BooleanSchema<undefined>, false> (+1 overload)
export optionalCreates an optional schema.
@paramwrapped The wrapped schema.@paramdefault_ The default value.@returnsAn optional schema.optional(import vv.function boolean(): v.BooleanSchema<undefined> (+1 overload)
export booleanCreates a boolean schema.
@returnsA boolean schema.boolean(), false)
	}),
	attributes: v.ArraySchema<v.StringSchema<undefined>, undefined>attributes: import vv.array<v.StringSchema<undefined>>(item: v.StringSchema<undefined>): v.ArraySchema<v.StringSchema<undefined>, undefined> (+1 overload)
export arrayCreates an array schema.
@paramitem The item schema.@returnsAn array schema.array(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string())
});

export const const createProfile: RemoteForm<{
    name: string;
    photo: File;
    info: {
        height: number;
        likesDogs?: boolean | undefined;
    };
    attributes: string[];
}, void>createProfile = form<v.ObjectSchema<{
    readonly name: v.StringSchema<undefined>;
    readonly photo: v.FileSchema<undefined>;
    readonly info: v.ObjectSchema<{
        readonly height: v.NumberSchema<undefined>;
        readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
    }, undefined>;
    readonly attributes: v.ArraySchema<...>;
}, undefined>, void>(validate: v.ObjectSchema<...>, fn: (data: {
    ...;
}) => MaybePromise<...>): RemoteForm<...> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(const datingProfile: v.ObjectSchema<{
    readonly name: v.StringSchema<undefined>;
    readonly photo: v.FileSchema<undefined>;
    readonly info: v.ObjectSchema<{
        readonly height: v.NumberSchema<undefined>;
        readonly likesDogs: v.OptionalSchema<v.BooleanSchema<undefined>, false>;
    }, undefined>;
    readonly attributes: v.ArraySchema<...>;
}, undefined>datingProfile, (data: {
    name: string;
    photo: File;
    info: {
        height: number;
        likesDogs: boolean;
    };
    attributes: string[];
}data) => { /* ... */ });
```

...your form could look like this:

```
<script>
	import { createProfile } from './data.remote';

	const { name, photo, info, attributes } = createProfile.fields;
</script>

<form {...createProfile} enctype="multipart/form-data">
	<label>
		<input {...name.as('text')} /> Name
	</label>

	<label>
		<input {...photo.as('file')} /> Photo
	</label>

	<label>
		<input {...info.height.as('number')} /> Height (cm)
	</label>

	<label>
		<input {...info.likesDogs.as('checkbox')} /> I like dogs
	</label>

	<h2>My best attributes</h2>
	<input {...attributes[0].as('text')} />
	<input {...attributes[1].as('text')} />
	<input {...attributes[2].as('text')} />

	<button>submit</button>
</form>
```

Because our form contains a `file` input, we’ve added an `enctype="multipart/form-data"` attribute. The values for `info.height` and `info.likesDogs` are coerced to a number and a boolean respectively.

> If a `checkbox` input is unchecked, the value is not included in the [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) object that SvelteKit constructs the data from. As such, we have to make the value optional in our schema. In Valibot that means using `v.optional(v.boolean(), false)` instead of just `v.boolean()`, whereas in Zod it would mean using `z.coerce.boolean<boolean>()`.

In the case of `radio` and `checkbox` inputs that all belong to the same field, the `value` must be specified as a second argument to `.as(...)`:

 data.remote

```
export const const operatingSystems: readonly ["windows", "mac", "linux"]operatingSystems = /** @type {const} */ (['windows', 'mac', 'linux']);
export const const languages: readonly ["html", "css", "js"]languages = /** @type {const} */ (['html', 'css', 'js']);

export const const survey: RemoteForm<{
    operatingSystem: "windows" | "mac" | "linux";
    languages?: ("html" | "css" | "js")[] | undefined;
}, void>survey = form<v.ObjectSchema<{
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}, undefined>, void>(validate: v.ObjectSchema<...>, fn: (data: {
    ...;
}) => MaybePromise<...>): RemoteForm<...> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}>(entries: {
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>operatingSystem: import vv.picklist<readonly ["windows", "mac", "linux"]>(options: readonly ["windows", "mac", "linux"]): v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined> (+1 overload)
export picklistCreates a picklist schema.
@paramoptions The picklist options.@returnsA picklist schema.picklist(const operatingSystems: readonly ["windows", "mac", "linux"]operatingSystems),
		languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>languages: import vv.optional<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>(wrapped: v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, default_: readonly []): v.OptionalSchema<...> (+1 overload)
export optionalCreates an optional schema.
@paramwrapped The wrapped schema.@paramdefault_ The default value.@returnsAn optional schema.optional(import vv.array<v.PicklistSchema<readonly ["html", "css", "js"], undefined>>(item: v.PicklistSchema<readonly ["html", "css", "js"], undefined>): v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined> (+1 overload)
export arrayCreates an array schema.
@paramitem The item schema.@returnsAn array schema.array(import vv.picklist<readonly ["html", "css", "js"]>(options: readonly ["html", "css", "js"]): v.PicklistSchema<readonly ["html", "css", "js"], undefined> (+1 overload)
export picklistCreates a picklist schema.
@paramoptions The picklist options.@returnsA picklist schema.picklist(const languages: readonly ["html", "css", "js"]languages)), []),
	}),
	(data: {
    operatingSystem: "windows" | "mac" | "linux";
    languages: ("html" | "css" | "js")[];
}data) => { /* ... */ },
);
```

```
export const const operatingSystems: readonly ["windows", "mac", "linux"]operatingSystems = ['windows', 'mac', 'linux'] as type const = readonly ["windows", "mac", "linux"]const;
export const const languages: readonly ["html", "css", "js"]languages = ['html', 'css', 'js'] as type const = readonly ["html", "css", "js"]const;

export const const survey: RemoteForm<{
    operatingSystem: "windows" | "mac" | "linux";
    languages?: ("html" | "css" | "js")[] | undefined;
}, void>survey = form<v.ObjectSchema<{
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}, undefined>, void>(validate: v.ObjectSchema<...>, fn: (data: {
    ...;
}) => MaybePromise<...>): RemoteForm<...> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}>(entries: {
    readonly operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>;
    readonly languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		operatingSystem: v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined>operatingSystem: import vv.picklist<readonly ["windows", "mac", "linux"]>(options: readonly ["windows", "mac", "linux"]): v.PicklistSchema<readonly ["windows", "mac", "linux"], undefined> (+1 overload)
export picklistCreates a picklist schema.
@paramoptions The picklist options.@returnsA picklist schema.picklist(const operatingSystems: readonly ["windows", "mac", "linux"]operatingSystems),
		languages: v.OptionalSchema<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>languages: import vv.optional<v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, readonly []>(wrapped: v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined>, default_: readonly []): v.OptionalSchema<...> (+1 overload)
export optionalCreates an optional schema.
@paramwrapped The wrapped schema.@paramdefault_ The default value.@returnsAn optional schema.optional(import vv.array<v.PicklistSchema<readonly ["html", "css", "js"], undefined>>(item: v.PicklistSchema<readonly ["html", "css", "js"], undefined>): v.ArraySchema<v.PicklistSchema<readonly ["html", "css", "js"], undefined>, undefined> (+1 overload)
export arrayCreates an array schema.
@paramitem The item schema.@returnsAn array schema.array(import vv.picklist<readonly ["html", "css", "js"]>(options: readonly ["html", "css", "js"]): v.PicklistSchema<readonly ["html", "css", "js"], undefined> (+1 overload)
export picklistCreates a picklist schema.
@paramoptions The picklist options.@returnsA picklist schema.picklist(const languages: readonly ["html", "css", "js"]languages)), []),
	}),
	(data: {
    operatingSystem: "windows" | "mac" | "linux";
    languages: ("html" | "css" | "js")[];
}data) => { /* ... */ },
);
```

```
<form {...survey}>
	<h2>Which operating system do you use?</h2>

	{#each operatingSystems as os}
		<label>
			<input {...survey.fields.operatingSystem.as('radio', os)}>
			{os}
		</label>
	{/each}

	<h2>Which languages do you write code in?</h2>

	{#each languages as language}
		<label>
			<input {...survey.fields.languages.as('checkbox', language)}>
			{language}
		</label>
	{/each}

	<button>submit</button>
</form>
```

Alternatively, you could use `select` and `select multiple`:

```
<form {...survey}>
	<h2>Which operating system do you use?</h2>

	<select {...survey.fields.operatingSystem.as('select')}>
		{#each operatingSystems as os}
			<option>{os}</option>
		{/each}
	</select>

	<h2>Which languages do you write code in?</h2>

	<select {...survey.fields.languages.as('select multiple')}>
		{#each languages as language}
			<option>{language}</option>
		{/each}
	</select>

	<button>submit</button>
</form>
```

> As with unchecked `checkbox` inputs, if no selections are made then the data will be `undefined`. For this reason, the `languages` field uses `v.optional(v.array(...), [])` rather than just `v.array(...)`.

### Programmatic validation

In addition to declarative schema validation, you can programmatically mark fields as invalid inside the form handler using the `invalid` helper from `@sveltejs/kit`. This is useful for cases where you can’t know if something is valid until you try to perform some action.

- It throws just like `redirect` or `error`
- It accepts multiple arguments that can be strings (for issues relating to the form as a whole — these will only show up in `fields.allIssues()`) or standard-schema-compliant issues (for those relating to a specific field). Use the `issue` parameter for type-safe creation of such issues:

 src/routes/shop/data.remote

```
import * as import vv from 'valibot';
import { import invalidinvalid } from '@sveltejs/kit';
import { function form<Output>(fn: () => MaybePromise<Output>): RemoteForm<void, Output> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form } from '$app/server';
import * as import dbdb from '$lib/server/database';

export const const buyHotcakes: RemoteForm<RemoteFormInput, unknown>buyHotcakes = form<RemoteFormInput, unknown>(validate: "unchecked", fn: (data: RemoteFormInput) => unknown): RemoteForm<RemoteFormInput, unknown> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{
    readonly qty: v.SchemaWithPipe<readonly [v.NumberSchema<undefined>, v.MinValueAction<number, 1, "you must buy at least one hotcake">]>;
}>(entries: {
    readonly qty: v.SchemaWithPipe<readonly [v.NumberSchema<undefined>, v.MinValueAction<number, 1, "you must buy at least one hotcake">]>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		qty: v.SchemaWithPipe<readonly [v.NumberSchema<undefined>, v.MinValueAction<number, 1, "you must buy at least one hotcake">]>qty: import vv.pipe<v.NumberSchema<undefined>, v.MinValueAction<number, 1, "you must buy at least one hotcake">>(schema: v.NumberSchema<undefined>, item1: v.MinValueAction<number, 1, "you must buy at least one hotcake"> | v.PipeAction<...>): v.SchemaWithPipe<...> (+20 overloads)
export pipeAdds a pipeline to a schema, that can validate and transform its input.
@paramschema The root schema.@paramitem1 The first pipe item.@returnsA schema with a pipeline.pipe(
			import vv.function number(): v.NumberSchema<undefined> (+1 overload)
export numberCreates a number schema.
@returnsA number schema.number(),
			import vv.minValue<number, 1, "you must buy at least one hotcake">(requirement: 1, message: "you must buy at least one hotcake"): v.MinValueAction<number, 1, "you must buy at least one hotcake"> (+1 overload)
export minValueCreates a min value validation action.
@paramrequirement The minimum value.@parammessage The error message.@returnsA min value action.minValue(1, 'you must buy at least one hotcake')
		)
	}),
	async (data: anydata, issue: anyissue) => {
		try {
			await import dbdb.buy(data: anydata.qty);
		} catch (function (local var) e: unknowne) {
			if (function (local var) e: unknowne.code === 'OUT_OF_STOCK') {
				import invalidinvalid(
					issue: anyissue.qty(`we don't have enough hotcakes`)
				);
			}
		}
	}
);
```

### Validation

If the submitted data doesn’t pass the schema, the callback will not run. Instead, each invalid field’s `issues()` method will return an array of `{ message: string }` objects, and the `aria-invalid` attribute (returned from `as(...)`) will be set to `true`:

```
<form {...createPost}>
	<label>
		<h2>Title</h2>

		{#each createPost.fields.title.issues() as issue}
			<p class="issue">{issue.message}</p>
		{/each}

		<input {...createPost.fields.title.as('text')} />
	</label>

	<label>
		<h2>Write your post</h2>

		{#each createPost.fields.content.issues() as issue}
			<p class="issue">{issue.message}</p>
		{/each}

		<textarea {...createPost.fields.content.as('text')}></textarea>
	</label>

	<button>Publish!</button>
</form>
```

You don’t need to wait until the form is submitted to validate the data — you can call `validate()` programmatically, for example in an `oninput` callback (which will validate the data on every keystroke) or an `onchange` callback:

```
<form {...createPost} oninput={() => createPost.validate()}>
	
</form>
```

By default, issues will be ignored if they belong to form controls that haven’t yet been interacted with. To validate *all* inputs, call `validate({ includeUntouched: true })`.

For client-side validation, you can specify a *preflight* schema which will populate `issues()` and prevent data being sent to the server if the data doesn’t validate:

```
<script>
	import * as v from 'valibot';
	import { createPost } from '../data.remote';

	const schema = v.object({
		title: v.pipe(v.string(), v.nonEmpty()),
		content: v.pipe(v.string(), v.nonEmpty())
	});
</script>

<h1>Create a new post</h1>

<form {...createPost.preflight(schema)}>
	
</form>
```

> The preflight schema can be the same object as your server-side schema, if appropriate, though it won’t be able to do server-side checks like ‘this value already exists in the database’. Note that you cannot export a schema from a `.remote.ts` or `.remote.js` file, so the schema must either be exported from a shared module, or from a `<script module>` block in the component containing the `<form>`.

To get a list of *all* issues, rather than just those belonging to a single field, you can use the `fields.allIssues()` method:

```
{#each createPost.fields.allIssues() as issue}
	<p>{issue.message}</p>
{/each}
```

### Getting/setting inputs

Each field has a `value()` method that reflects its current value. As the user interacts with the form, it is automatically updated:

```
<form {...createPost}>
	
</form>

<div class="preview">
	<h2>{createPost.fields.title.value()}</h2>
	<div>{@html render(createPost.fields.content.value())}</div>
</div>
```

Alternatively, `createPost.fields.value()` would return a `{ title, content }` object.

You can update a field (or a collection of fields) via the `set(...)` method:

```
<script>
	import { createPost } from '../data.remote';

	// this...
	createPost.fields.set({
		title: 'My new blog post',
		content: 'Lorem ipsum dolor sit amet...'
	});

	// ...is equivalent to this:
	createPost.fields.title.set('My new blog post');
	createPost.fields.content.set('Lorem ipsum dolor sit amet');
</script>
```

### Handling sensitive data

In the case of a non-progressively-enhanced form submission (i.e. where JavaScript is unavailable, for whatever reason) `value()` is also populated if the submitted data is invalid, so that the user does not need to fill the entire form out from scratch.

You can prevent sensitive data (such as passwords and credit card numbers) from being sent back to the user by using a name with a leading underscore:

```
<form {...register}>
	<label>
		Username
		<input {...register.fields.username.as('text')} />
	</label>

	<label>
		Password
		<input {...register.fields._password.as('password')} />
	</label>

	<button>Sign up!</button>
</form>
```

In this example, if the data does not validate, only the first `<input>` will be populated when the page reloads.

### Single-flight mutations

By default, all queries used on the page (along with any `load` functions) are automatically refreshed following a successful form submission. This ensures that everything is up-to-date, but it’s also inefficient: many queries will be unchanged, and it requires a second trip to the server to get the updated data.

Instead, we can specify which queries should be refreshed in response to a particular form submission. This is called a *single-flight mutation*, and there are two ways to achieve it. The first is to refresh the query on the server, inside the form handler:

```
export const const getPosts: RemoteQueryFunction<void, void>getPosts = query<void>(fn: () => MaybePromise<void>): RemoteQueryFunction<void, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => { /* ... */ });

export const const getPost: RemoteQueryFunction<string, void>getPost = query<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>): RemoteQueryFunction<string, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (slug: stringslug) => { /* ... */ });

export const const createPost: RemoteForm<{}, never>createPost = form<v.ObjectSchema<{}, undefined>, never>(validate: v.ObjectSchema<{}, undefined>, fn: (data: {}) => Promise<never>): RemoteForm<{}, never> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{}>(entries: {}): v.ObjectSchema<{}, undefined> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({/* ... */}),
	async (data: {}data) => {
		// form logic goes here...

		// Refresh `getPosts()` on the server, and send
		// the data back with the result of `createPost`
		await const getPosts: (arg: void) => RemoteQuery<void>getPosts().function refresh(): Promise<void>On the client, this function will re-fetch the query from the server.
On the server, this can be called in the context of a command or form and the refreshed data will accompany the action response back to the client.
This prevents SvelteKit needing to refresh all queries on the page in a second server round-trip.
refresh();

		// Redirect to the newly created page
		function redirect(status: 300 | 301 | 302 | 303 | 304 | 305 | 306 | 307 | 308 | ({} & number), location: string | URL): neverRedirect a request. When called during request handling, SvelteKit will return a redirect response.
Make sure you’re not catching the thrown redirect, which would prevent SvelteKit from handling it.
Most common status codes:

303 See Other: redirect as a GET request (often used after a form POST request)
307 Temporary Redirect: redirect will keep the request method
308 Permanent Redirect: redirect will keep the request method, SEO will be transferred to the new page

See all redirect status codes
@paramstatus The HTTP status code. Must be in the range 300-308.@paramlocation The location to redirect to.@throwsRedirect This error instructs SvelteKit to redirect to the specified location.@throwsError If the provided status is invalid.redirect(303, `/blog/${const slug: ""slug}`);
	}
);

export const const updatePost: RemoteForm<{}, void>updatePost = form<v.ObjectSchema<{}, undefined>, void>(validate: v.ObjectSchema<{}, undefined>, fn: (data: {}) => MaybePromise<void>): RemoteForm<{}, void> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{}>(entries: {}): v.ObjectSchema<{}, undefined> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({/* ... */}),
	async (data: {}data) => {
		// form logic goes here...
		const const result: anyresult = const externalApi: any@type{any}externalApi.update(const post: {
    id: string;
}post);

		// The API already gives us the updated post,
		// no need to refresh it, we can set it directly
		await const getPost: (arg: string) => RemoteQuery<void>getPost(const post: {
    id: string;
}post.id: stringid).function set(value: void): voidOn the client, this function will update the value of the query without re-fetching it.
On the server, this can be called in the context of a command or form and the specified data will accompany the action response back to the client.
This prevents SvelteKit needing to refresh all queries on the page in a second server round-trip.
set(const result: anyresult);
	}
);
```

The second is to drive the single-flight mutation from the client, which we’ll see in the section on [enhance](#form-enhance).

### Returns and redirects

The example above uses [redirect(...)](https://kit.svelte.dev/docs/@sveltejs-kit#redirect), which sends the user to the newly created page. Alternatively, the callback could return data, in which case it would be available as `createPost.result`:

 src/routes/blog/data.remote

```
export const const createPost: RemoteForm<{}, {
    success: boolean;
}>createPost = form<v.ObjectSchema<{}, undefined>, {
    success: boolean;
}>(validate: v.ObjectSchema<{}, undefined>, fn: (data: {}) => MaybePromise<{
    success: boolean;
}>): RemoteForm<{}, {
    success: boolean;
}> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{}>(entries: {}): v.ObjectSchema<{}, undefined> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({/* ... */}),
	async (data: {}data) => {
		// ...

		return { success: booleansuccess: true };
	}
);
```

src/routes/blog/new/+page

```
<script>
	import { createPost } from '../data.remote';
</script>

<h1>Create a new post</h1>

<form {...createPost}>
	
</form>

{#if createPost.result?.success}
	<p>Successfully published!</p>
{/if}
```

```
<script lang="ts">
	import { createPost } from '../data.remote';
</script>

<h1>Create a new post</h1>

<form {...createPost}>
	
</form>

{#if createPost.result?.success}
	<p>Successfully published!</p>
{/if}
```

This value is *ephemeral* — it will vanish if you resubmit, navigate away, or reload the page.

> The `result` value need not indicate success — it can also contain validation errors, along with any data that should repopulate the form on page reload.

If an error occurs during submission, the nearest `+error.svelte` page will be rendered.

### enhance

We can customize what happens when the form is submitted with the `enhance` method:

 src/routes/blog/new/+page

```
<script>
	import { createPost } from '../data.remote';
	import { showToast } from '$lib/toast';
</script>

<h1>Create a new post</h1>

<form {...createPost.enhance(async ({ form, data, submit }) => {
	try {
		await submit();
		form.reset();

		showToast('Successfully published!');
	} catch (error) {
		showToast('Oh no! Something went wrong');
	}
})}>
	
</form>
```

```
<script lang="ts">
	import { createPost } from '../data.remote';
	import { showToast } from '$lib/toast';
</script>

<h1>Create a new post</h1>

<form {...createPost.enhance(async ({ form, data, submit }) => {
	try {
		await submit();
		form.reset();

		showToast('Successfully published!');
	} catch (error) {
		showToast('Oh no! Something went wrong');
	}
})}>
	
</form>
```

> When using `enhance`, the `<form>` is not automatically reset — you must call `form.reset()` if you want to clear the inputs.

The callback receives the `form` element, the `data` it contains, and a `submit` function.

To enable client-driven [single-flight mutations](#form-Single-flight-mutations), use `submit().updates(...)`. For example, if the `getPosts()` query was used on this page, we could refresh it like so:

```
await function submit(): Promise<any> & {
    updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<any>;
}submit().function updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<any>updates(function getPosts(): RemoteQuery<Post[]>getPosts());
```

We can also *override* the current data while the submission is ongoing:

```
await function submit(): Promise<any> & {
    updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<any>;
}submit().function updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<any>updates(
	function getPosts(): RemoteQuery<Post[]>getPosts().function withOverride(update: (current: Post[]) => Post[]): RemoteQueryOverrideTemporarily override the value of a query. This is used with the updates method of a command or enhanced form submission to provide optimistic updates.
&#x3C;script>
  import { getTodos, addTodo } from './todos.remote.js';
  const todos = getTodos();
&#x3C;/script>

&#x3C;form {...addTodo.enhance(async ({ data, submit }) => {
  await submit().updates(
	todos.withOverride((todos) => [...todos, { text: data.get('text') }])
  );
})}>
  &#x3C;input type="text" name="text" />
  &#x3C;button type="submit">Add Todo&#x3C;/button>
&#x3C;/form>withOverride((posts: Post[]posts) => [const newPost: PostnewPost, ...posts: Post[]posts])
);
```

The override will be applied immediately, and released when the submission completes (or fails).

### Multiple instances of a form

Some forms may be repeated as part of a list. In this case you can create separate instances of a form function via `for(id)` to achieve isolation.

 src/routes/todos/+page

```
<script>
	import { getTodos, modifyTodo } from '../data.remote';
</script>

<h1>Todos</h1>

{#each await getTodos() as todo}
	{@const modify = modifyTodo.for(todo.id)}
	<form {...modify}>
		
		<button disabled={!!modify.pending}>save changes</button>
	</form>
{/each}
```

```
<script lang="ts">
	import { getTodos, modifyTodo } from '../data.remote';
</script>

<h1>Todos</h1>

{#each await getTodos() as todo}
	{@const modify = modifyTodo.for(todo.id)}
	<form {...modify}>
		
		<button disabled={!!modify.pending}>save changes</button>
	</form>
{/each}
```

### Multiple submit buttons

It’s possible for a `<form>` to have multiple submit buttons. For example, you might have a single form that allows you to log in or register depending on which button was clicked.

To accomplish this, add a field to your schema for the button value, and use `as('submit', value)` to bind it:

 src/routes/login/+page

```
<script>
	import { loginOrRegister } from '$lib/auth';
</script>

<form {...loginOrRegister}>
	<label>
		Your username
		<input {...loginOrRegister.fields.username.as('text')} />
	</label>

	<label>
		Your password
		<input {...loginOrRegister.fields._password.as('password')} />
	</label>

	<button {...loginOrRegister.fields.action.as('submit', 'login')}>login</button>
	<button {...loginOrRegister.fields.action.as('submit', 'register')}>register</button>
</form>
```

```
<script lang="ts">
	import { loginOrRegister } from '$lib/auth';
</script>

<form {...loginOrRegister}>
	<label>
		Your username
		<input {...loginOrRegister.fields.username.as('text')} />
	</label>

	<label>
		Your password
		<input {...loginOrRegister.fields._password.as('password')} />
	</label>

	<button {...loginOrRegister.fields.action.as('submit', 'login')}>login</button>
	<button {...loginOrRegister.fields.action.as('submit', 'register')}>register</button>
</form>
```

In your form handler, you can check which button was clicked:

 $lib/auth

```
import * as import vv from 'valibot';
import { function form<Output>(fn: () => MaybePromise<Output>): RemoteForm<void, Output> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form } from '$app/server';

export const const loginOrRegister: RemoteForm<{
    username: string;
    _password: string;
    action: "login" | "register";
}, void>loginOrRegister = form<v.ObjectSchema<{
    readonly username: v.StringSchema<undefined>;
    readonly _password: v.StringSchema<undefined>;
    readonly action: v.PicklistSchema<["login", "register"], undefined>;
}, undefined>, void>(validate: v.ObjectSchema<...>, fn: (data: {
    ...;
}) => MaybePromise<...>): RemoteForm<...> (+2 overloads)Creates a form object that can be spread onto a &#x3C;form> element.
See Remote functions for full documentation.
@since2.27form(
	import vv.object<{
    readonly username: v.StringSchema<undefined>;
    readonly _password: v.StringSchema<undefined>;
    readonly action: v.PicklistSchema<["login", "register"], undefined>;
}>(entries: {
    readonly username: v.StringSchema<undefined>;
    readonly _password: v.StringSchema<undefined>;
    readonly action: v.PicklistSchema<["login", "register"], undefined>;
}): v.ObjectSchema<...> (+1 overload)
export objectCreates an object schema.
Hint: This schema removes unknown entries. The output will only include the
entries you specify. To include unknown entries, use looseObject. To
return an issue for unknown entries, use strictObject. To include and
validate unknown entries, use objectWithRest.
@paramentries The entries schema.@returnsAn object schema.object({
		username: v.StringSchema<undefined>username: import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
		_password: v.StringSchema<undefined>_password: import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
		action: v.PicklistSchema<["login", "register"], undefined>action: import vv.picklist<["login", "register"]>(options: ["login", "register"]): v.PicklistSchema<["login", "register"], undefined> (+1 overload)
export picklistCreates a picklist schema.
@paramoptions The picklist options.@returnsA picklist schema.picklist(['login', 'register'])
	}),
	async ({ username: stringusername, _password: string_password, action: "login" | "register"action }) => {
		if (action: "login" | "register"action === 'login') {
			// handle login
		} else {
			// handle registration
		}
	}
);
```

## command

The `command` function, like `form`, allows you to write data to the server. Unlike `form`, it’s not specific to an element and can be called from anywhere.

> Prefer `form` where possible, since it gracefully degrades if JavaScript is disabled or fails to load.

As with `query` and `form`, if the function accepts an argument, it should be [validated](#query-Query-arguments) by passing a [Standard Schema](https://standardschema.dev) as the first argument to `command`.

 likes.remote

```
import * as import vv from 'valibot';
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query, function command<Output>(fn: () => Output): RemoteCommand<void, Output> (+2 overloads)Creates a remote command. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27command } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getLikes: RemoteQueryFunction<string, any>getLikes = query<v.StringSchema<undefined>, any>(schema: v.StringSchema<undefined>, fn: (arg: string) => any): RemoteQueryFunction<string, any> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (id: stringid) => {
	const [const row: anyrow] = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT likes
		FROM item
		WHERE id = ${id: stringid}
	`;

	return const row: anyrow.likes;
});

export const const addLike: RemoteCommand<string, Promise<void>>addLike = command<v.StringSchema<undefined>, Promise<void>>(validate: v.StringSchema<undefined>, fn: (arg: string) => Promise<void>): RemoteCommand<string, Promise<void>> (+2 overloads)Creates a remote command. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27command(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (id: stringid) => {
	await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		UPDATE item
		SET likes = likes + 1
		WHERE id = ${id: stringid}
	`;
});
```

Now simply call `addLike`, from (for example) an event handler:

 +page

```
<script>
	import { getLikes, addLike } from './likes.remote';
	import { showToast } from '$lib/toast';

	let { item } = $props();
</script>

<button
	onclick={async () => {
		try {
			await addLike(item.id);
		} catch (error) {
			showToast('Something went wrong!');
		}
	}}
>
	add like
</button>

<p>likes: {await getLikes(item.id)}</p>
```

```
<script lang="ts">
	import { getLikes, addLike } from './likes.remote';
	import { showToast } from '$lib/toast';

	let { item } = $props();
</script>

<button
	onclick={async () => {
		try {
			await addLike(item.id);
		} catch (error) {
			showToast('Something went wrong!');
		}
	}}
>
	add like
</button>

<p>likes: {await getLikes(item.id)}</p>
```

> Commands cannot be called during render.

### Updating queries

To update `getLikes(item.id)`, or any other query, we need to tell SvelteKit *which* queries need to be refreshed (unlike `form`, which by default invalidates everything, to approximate the behaviour of a native form submission).

We either do that inside the command itself...

 likes.remote

```
export const const getLikes: RemoteQueryFunction<string, void>getLikes = query<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>): RemoteQueryFunction<string, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (id: stringid) => { /* ... */ });

export const const addLike: RemoteCommand<string, Promise<void>>addLike = command<v.StringSchema<undefined>, Promise<void>>(validate: v.StringSchema<undefined>, fn: (arg: string) => Promise<void>): RemoteCommand<string, Promise<void>> (+2 overloads)Creates a remote command. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27command(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (id: stringid) => {
	await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		UPDATE item
		SET likes = likes + 1
		WHERE id = ${id: stringid}
	`;

	const getLikes: (arg: string) => RemoteQuery<void>getLikes(id: stringid).function refresh(): Promise<void>On the client, this function will re-fetch the query from the server.
On the server, this can be called in the context of a command or form and the refreshed data will accompany the action response back to the client.
This prevents SvelteKit needing to refresh all queries on the page in a second server round-trip.
refresh();
	// Just like within form functions you can also do
	// getLikes(id).set(...)
	// in case you have the result already
});
```

...or when we call it:

```
try {
	await const addLike: (arg: string) => Promise<void> & {
    updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<...>;
}addLike(const item: Itemitem.Item.id: stringid).function updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<void>updates(const getLikes: (arg: string) => RemoteQuery<number>getLikes(const item: Itemitem.Item.id: stringid));
} catch (var error: unknownerror) {
	function showToast(message: string): voidshowToast('Something went wrong!');
}
```

As before, we can use `withOverride` for optimistic updates:

```
try {
	await const addLike: (arg: string) => Promise<void> & {
    updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<...>;
}addLike(const item: Itemitem.Item.id: stringid).function updates(...queries: Array<RemoteQuery<any> | RemoteQueryOverride>): Promise<void>updates(
		const getLikes: (arg: string) => RemoteQuery<number>getLikes(const item: Itemitem.Item.id: stringid).function withOverride(update: (current: number) => number): RemoteQueryOverrideTemporarily override the value of a query. This is used with the updates method of a command or enhanced form submission to provide optimistic updates.
&#x3C;script>
  import { getTodos, addTodo } from './todos.remote.js';
  const todos = getTodos();
&#x3C;/script>

&#x3C;form {...addTodo.enhance(async ({ data, submit }) => {
  await submit().updates(
	todos.withOverride((todos) => [...todos, { text: data.get('text') }])
  );
})}>
  &#x3C;input type="text" name="text" />
  &#x3C;button type="submit">Add Todo&#x3C;/button>
&#x3C;/form>withOverride((n: numbern) => n: numbern + 1)
	);
} catch (var error: unknownerror) {
	function showToast(message: string): voidshowToast('Something went wrong!');
}
```

## prerender

The `prerender` function is similar to `query`, except that it will be invoked at build time to prerender the result. Use this for data that changes at most once per redeployment.

 src/routes/blog/data.remote

```
import { function prerender<Output>(fn: () => MaybePromise<Output>, options?: {
    inputs?: RemotePrerenderInputsGenerator<void>;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<void, Output> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getPosts: RemotePrerenderFunction<void, any[]>getPosts = prerender<any[]>(fn: () => MaybePromise<any[]>, options?: {
    inputs?: RemotePrerenderInputsGenerator<void>;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(async () => {
	const const posts: any[]posts = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT title, slug
		FROM post
		ORDER BY published_at
		DESC
	`;

	return const posts: any[]posts;
});
```

You can use `prerender` functions on pages that are otherwise dynamic, allowing for partial prerendering of your data. This results in very fast navigation, since prerendered data can live on a CDN along with your other static assets.

In the browser, prerendered data is saved using the [Cache](https://developer.mozilla.org/en-US/docs/Web/API/Cache) API. This cache survives page reloads, and will be cleared when the user first visits a new deployment of your app.

> When the entire page has `export const prerender = true`, you cannot use queries, as they are dynamic.

### Prerender arguments

As with queries, prerender functions can accept an argument, which should be [validated](#query-Query-arguments) with a [Standard Schema](https://standardschema.dev/):

 src/routes/blog/data.remote

```
import * as import vv from 'valibot';
import { function error(status: number, body: App.Error): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error } from '@sveltejs/kit';
import { function prerender<Output>(fn: () => MaybePromise<Output>, options?: {
    inputs?: RemotePrerenderInputsGenerator<void>;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<void, Output> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender } from '$app/server';
import * as module "$lib/server/database"db from '$lib/server/database';

export const const getPosts: RemotePrerenderFunction<void, void>getPosts = prerender<void>(fn: () => MaybePromise<void>, options?: {
    inputs?: RemotePrerenderInputsGenerator<void>;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(async () => { /* ... */ });

export const const getPost: RemotePrerenderFunction<string, any>getPost = prerender<v.StringSchema<undefined>, any>(schema: v.StringSchema<undefined>, fn: (arg: string) => any, options?: {
    inputs?: RemotePrerenderInputsGenerator<string> | undefined;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(), async (slug: stringslug) => {
	const [const post: anypost] = await module "$lib/server/database"db.function sql(strings: TemplateStringsArray, ...values: any[]): Promise<any[]>sql`
		SELECT * FROM post
		WHERE slug = ${slug: stringslug}
	`;

	if (!const post: anypost) function error(status: number, body?: {
    message: string;
} extends App.Error ? App.Error | string | undefined : never): never (+1 overload)Throws an error with a HTTP status code and an optional message.
When called during request handling, this will cause SvelteKit to
return an error response without invoking handleError.
Make sure you’re not catching the thrown error, which would prevent SvelteKit from handling it.
@paramstatus The HTTP status code. Must be in the range 400-599.@parambody An object that conforms to the App.Error type. If a string is passed, it will be used as the message property.@throwsHttpError This error instructs SvelteKit to initiate HTTP error handling.@throwsError If the provided status is invalid (not between 400 and 599).error(404, 'Not found');
	return const post: anypost;
});
```

Any calls to `getPost(...)` found by SvelteKit’s crawler while [prerendering pages](https://kit.svelte.dev/docs/page-options#prerender) will be saved automatically, but you can also specify which values it should be called with using the `inputs` option:

 src/routes/blog/data.remote

```
export const const getPost: RemotePrerenderFunction<string, void>getPost = prerender<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>, options?: {
    inputs?: RemotePrerenderInputsGenerator<string> | undefined;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(
	import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
	async (slug: stringslug) => { /* ... */ },
	{
		inputs?: RemotePrerenderInputsGenerator<string> | undefinedinputs: () => [
			'first-post',
			'second-post',
			'third-post'
		]
	}
);
```

```
export const const getPost: RemotePrerenderFunction<string, void>getPost = prerender<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>, options?: {
    inputs?: RemotePrerenderInputsGenerator<string> | undefined;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(
	import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
	async (slug: stringslug) => { /* ... */ },
	{
		inputs?: RemotePrerenderInputsGenerator<string> | undefinedinputs: () => [
			'first-post',
			'second-post',
			'third-post'
		]
	}
);
```

By default, prerender functions are excluded from your server bundle, which means that you cannot call them with any arguments that were *not* prerendered. You can set `dynamic: true` to change this behaviour:

 src/routes/blog/data.remote

```
export const const getPost: RemotePrerenderFunction<string, void>getPost = prerender<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>, options?: {
    inputs?: RemotePrerenderInputsGenerator<string> | undefined;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(
	import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
	async (slug: stringslug) => { /* ... */ },
	{
		dynamic?: boolean | undefineddynamic: true,
		inputs?: RemotePrerenderInputsGenerator<string> | undefinedinputs: () => [
			'first-post',
			'second-post',
			'third-post'
		]
	}
);
```

```
export const const getPost: RemotePrerenderFunction<string, void>getPost = prerender<v.StringSchema<undefined>, void>(schema: v.StringSchema<undefined>, fn: (arg: string) => MaybePromise<void>, options?: {
    inputs?: RemotePrerenderInputsGenerator<string> | undefined;
    dynamic?: boolean;
} | undefined): RemotePrerenderFunction<...> (+2 overloads)Creates a remote prerender function. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27prerender(
	import vv.function string(): v.StringSchema<undefined> (+1 overload)
export stringCreates a string schema.
@returnsA string schema.string(),
	async (slug: stringslug) => { /* ... */ },
	{
		dynamic?: boolean | undefineddynamic: true,
		inputs?: RemotePrerenderInputsGenerator<string> | undefinedinputs: () => [
			'first-post',
			'second-post',
			'third-post'
		]
	}
);
```

## Handling validation errors

As long as *you’re* not passing invalid data to your remote functions, there are only two reasons why the argument passed to a `command`, `query` or `prerender` function would fail validation:

- the function signature changed between deployments, and some users are currently on an older version of your app
- someone is trying to attack your site by poking your exposed endpoints with bad data

In the second case, we don’t want to give the attacker any help, so SvelteKit will generate a generic [400 Bad Request](https://http.dog/400) response. You can control the message by implementing the [handleValidationError](https://kit.svelte.dev/docs/hooks#Server-hooks-handleValidationError) server hook, which, like [handleError](https://kit.svelte.dev/docs/hooks#Shared-hooks-handleError), must return an [App.Error](https://kit.svelte.dev/docs/errors#Type-safety) (which defaults to `{ message: string }`):

 src/hooks.server

```
/** @type {import('@sveltejs/kit').HandleValidationError} */
export function function handleValidationError({ event, issues }: {
    event: any;
    issues: any;
}): {
    message: string;
}@type{import('@sveltejs/kit').HandleValidationError}handleValidationError({ event: anyevent, issues: anyissues }) {
	return {
		message: stringmessage: 'Nice try, hacker!'
	};
}
```

```
import type { type HandleValidationError<Issue extends StandardSchemaV1.Issue = StandardSchemaV1.Issue> = (input: {
    issues: Issue[];
    event: RequestEvent;
}) => MaybePromise<App.Error>The handleValidationError hook runs when the argument to a remote function fails validation.
It will be called with the validation issues and the event, and must return an object shape that matches App.Error.
HandleValidationError } from '@sveltejs/kit';

export const const handleValidationError: HandleValidationErrorhandleValidationError: type HandleValidationError<Issue extends StandardSchemaV1.Issue = StandardSchemaV1.Issue> = (input: {
    issues: Issue[];
    event: RequestEvent;
}) => MaybePromise<App.Error>The handleValidationError hook runs when the argument to a remote function fails validation.
It will be called with the validation issues and the event, and must return an object shape that matches App.Error.
HandleValidationError = ({ event: RequestEvent<Record<string, string>, string | null>event, issues: StandardSchemaV1.Issue[]issues }) => {
	return {
		App.Error.message: stringmessage: 'Nice try, hacker!'
	};
};
```

If you know what you’re doing and want to opt out of validation, you can pass the string `'unchecked'` in place of a schema:

 data.remote

```
import { function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query } from '$app/server';

export const const getStuff: RemoteQueryFunction<{
    id: string;
}, void>getStuff = query<{
    id: string;
}, void>(validate: "unchecked", fn: (arg: {
    id: string;
}) => MaybePromise<void>): RemoteQueryFunction<{
    id: string;
}, void> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query('unchecked', async ({ id: stringid }: { id: stringid: string }) => {
	// the shape might not actually be what TypeScript thinks
	// since bad actors might call this function with other arguments
});
```

## Using getRequestEvent

Inside `query`, `form` and `command` you can use [getRequestEvent](https://kit.svelte.dev/docs/$app-server#getRequestEvent) to get the current [RequestEvent](https://kit.svelte.dev/docs/@sveltejs-kit#RequestEvent) object. This makes it easy to build abstractions for interacting with cookies, for example:

 user.remote

```
import { function getRequestEvent(): RequestEventReturns the current RequestEvent. Can be used inside server hooks, server load functions, actions, and endpoints (and functions called by them).
In environments without AsyncLocalStorage, this must be called synchronously (i.e. not after an await).
@since2.20.0getRequestEvent, function query<Output>(fn: () => MaybePromise<Output>): RemoteQueryFunction<void, Output> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query } from '$app/server';
import { import findUserfindUser } from '$lib/server/database';

export const const getProfile: RemoteQueryFunction<void, {
    name: any;
    avatar: any;
}>getProfile = query<{
    name: any;
    avatar: any;
}>(fn: () => MaybePromise<{
    name: any;
    avatar: any;
}>): RemoteQueryFunction<void, {
    name: any;
    avatar: any;
}> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => {
	const const user: anyuser = await const getUser: (arg: void) => RemoteQuery<any>getUser();

	return {
		name: anyname: const user: anyuser.name,
		avatar: anyavatar: const user: anyuser.avatar
	};
});

// this query could be called from multiple places, but
// the function will only run once per request
const const getUser: RemoteQueryFunction<void, any>getUser = query<any>(fn: () => any): RemoteQueryFunction<void, any> (+2 overloads)Creates a remote query. When called from the browser, the function will be invoked on the server via a fetch call.
See Remote functions for full documentation.
@since2.27query(async () => {
	const { const cookies: CookiesGet or set cookies related to the current request
cookies } = function getRequestEvent(): RequestEventReturns the current RequestEvent. Can be used inside server hooks, server load functions, actions, and endpoints (and functions called by them).
In environments without AsyncLocalStorage, this must be called synchronously (i.e. not after an await).
@since2.20.0getRequestEvent();

	return await import findUserfindUser(const cookies: CookiesGet or set cookies related to the current request
cookies.Cookies.get: (name: string, opts?: CookieParseOptions) => string | undefinedGets a cookie that was previously set with cookies.set, or from the request headers.
@paramname the name of the cookie@paramopts the options, passed directly to cookie.parse. See documentation hereget('session_id'));
});
```

Note that some properties of `RequestEvent` are different inside remote functions:

- you cannot set headers (other than writing cookies, and then only inside `form` and `command` functions)
- `route`, `params` and `url` relate to the page the remote function was called from, *not* the URL of the endpoint SvelteKit creates for the remote function. Queries are not re-run when the user navigates (unless the argument to the query changes as a result of navigation), and so you should be mindful of how you use these values. In particular, never use them to determine whether or not a user is authorized to access certain data.

## Redirects

Inside `query`, `form` and `prerender` functions it is possible to use the [redirect(...)](https://kit.svelte.dev/docs/@sveltejs-kit#redirect) function. It is *not* possible inside `command` functions, as you should avoid redirecting here. (If you absolutely have to, you can return a `{ redirect: location }` object and deal with it in the client.)

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/20-core-concepts/60-remote-functions.md) [[llms.txt](https://kit.svelte.dev/docs/kit/remote-functions/llms.txt)]

 previous next [[State management](https://kit.svelte.dev/docs/kit/state-management)] [[Building your app](https://kit.svelte.dev/docs/kit/building-your-app)]
