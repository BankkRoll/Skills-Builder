# Web standards

# Web standards

> Web standards • SvelteKit documentation

Throughout this documentation, you’ll see references to the standard [Web APIs](https://developer.mozilla.org/en-US/docs/Web/API) that SvelteKit builds on top of. Rather than reinventing the wheel, we *use the platform*, which means your existing web development skills are applicable to SvelteKit. Conversely, time spent learning SvelteKit will help you be a better web developer elsewhere.

These APIs are available in all modern browsers and in many non-browser environments like Cloudflare Workers, Deno, and Vercel Functions. During development, and in [adapters](https://kit.svelte.dev/docs/adapters) for Node-based environments (including AWS Lambda), they’re made available via polyfills where necessary (for now, that is — Node is rapidly adding support for more web standards).

In particular, you’ll get comfortable with the following:

## Fetch APIs

SvelteKit uses [fetch](https://developer.mozilla.org/en-US/docs/Web/API/fetch) for getting data from the network. It’s available in [hooks](https://kit.svelte.dev/docs/hooks) and [server routes](https://kit.svelte.dev/docs/routing#server) as well as in the browser.

> A special version of `fetch` is available in [load](https://kit.svelte.dev/docs/load) functions, [server hooks](https://kit.svelte.dev/docs/hooks#Server-hooks) and [API routes](https://kit.svelte.dev/docs/routing#server) for invoking endpoints directly during server-side rendering, without making an HTTP call, while preserving credentials. (To make credentialled fetches in server-side code outside `load`, you must explicitly pass `cookie` and/or `authorization` headers.) It also allows you to make relative requests, whereas server-side `fetch` normally requires a fully qualified URL.

Besides `fetch` itself, the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) includes the following interfaces:

### Request

An instance of [Request](https://developer.mozilla.org/en-US/docs/Web/API/Request) is accessible in [hooks](https://kit.svelte.dev/docs/hooks) and [server routes](https://kit.svelte.dev/docs/routing#server) as `event.request`. It contains useful methods like `request.json()` and `request.formData()` for getting data that was posted to an endpoint.

### Response

An instance of [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) is returned from `await fetch(...)` and handlers in `+server.js` files. Fundamentally, a SvelteKit app is a machine for turning a `Request` into a `Response`.

### Headers

The [Headers](https://developer.mozilla.org/en-US/docs/Web/API/Headers) interface allows you to read incoming `request.headers` and set outgoing `response.headers`. For example, you can get the `request.headers` as shown below, and use the [jsonconvenience function](https://kit.svelte.dev/docs/@sveltejs-kit#json) to send modified `response.headers`:

 src/routes/what-is-my-user-agent/+server

```
import { function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export function function GET({ request }: {
    request: any;
}): Response@type{import('./$types').RequestHandler}GET({ request: anyrequest }) {
	// log all headers
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
@sincev0.1.100log(...request: anyrequest.headers);

	// create a JSON Response using a header we received
	return function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json({
		// retrieve a specific header
		userAgent: anyuserAgent: request: anyrequest.headers.get('user-agent')
	}, {
		// set a header on the response
		ResponseInit.headers?: HeadersInit | undefinedheaders: { 'x-custom-header': 'potato' }
	});
}
```

```
import { function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json } from '@sveltejs/kit';
import type { type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler } from './$types';

export const const GET: RequestHandlerGET: type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler = ({ request: RequestThe original request object.
request }) => {
	// log all headers
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
@sincev0.1.100log(...request: RequestThe original request object.
request.Request.headers: HeadersReturns a Headers object consisting of the headers associated with request. Note that headers added in the network layer by the user agent will not be accounted for in this object, e.g., the “Host” header.
MDN Reference
headers);

	// create a JSON Response using a header we received
	return function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json({
		// retrieve a specific header
		userAgent: string | nulluserAgent: request: RequestThe original request object.
request.Request.headers: HeadersReturns a Headers object consisting of the headers associated with request. Note that headers added in the network layer by the user agent will not be accounted for in this object, e.g., the “Host” header.
MDN Reference
headers.Headers.get(name: string): string | nullMDN Reference
get('user-agent')
	}, {
		// set a header on the response
		ResponseInit.headers?: HeadersInit | undefinedheaders: { 'x-custom-header': 'potato' }
	});
};
```

## FormData

When dealing with HTML native form submissions you’ll be working with [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) objects.

 src/routes/hello/+server

```
import { function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function function POST(event: any): Promise<Response>@type{import('./$types').RequestHandler}POST(event: anyevent) {
	const const body: anybody = await event: anyevent.request.formData();

	// log all fields
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
@sincev0.1.100log([...const body: anybody]);

	return function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json({
		// get a specific field's value
		name: anyname: const body: anybody.get('name') ?? 'world'
	});
}
```

```
import { function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json } from '@sveltejs/kit';
import type { type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler } from './$types';

export const const POST: RequestHandlerPOST: type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>
type RequestHandler = (event: Kit.RequestEvent<Record<string, any>, string | null>) => MaybePromise<Response>RequestHandler = async (event: Kit.RequestEvent<Record<string, any>, string | null>event) => {
	const const body: FormDatabody = await event: Kit.RequestEvent<Record<string, any>, string | null>event.RequestEvent<Record<string, any>, string | null>.request: RequestThe original request object.
request.Body.formData(): Promise<FormData>MDN Reference
formData();

	// log all fields
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
@sincev0.1.100log([...const body: FormDatabody]);

	return function json(data: any, init?: ResponseInit): ResponseCreate a JSON Response object from the supplied data.
@paramdata The value that will be serialized as JSON.@paraminit Options such as status and headers that will be added to the response. Content-Type: application/json and Content-Length headers will be added automatically.json({
		// get a specific field's value
		name: FormDataEntryValuename: const body: FormDatabody.FormData.get(name: string): FormDataEntryValue | nullMDN Reference
get('name') ?? 'world'
	});
};
```

## Stream APIs

Most of the time, your endpoints will return complete data, as in the `userAgent` example above. Sometimes, you may need to return a response that’s too large to fit in memory in one go, or is delivered in chunks, and for this the platform provides [streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) — [ReadableStream](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream), [WritableStream](https://developer.mozilla.org/en-US/docs/Web/API/WritableStream) and [TransformStream](https://developer.mozilla.org/en-US/docs/Web/API/TransformStream).

## URL APIs

URLs are represented by the [URL](https://developer.mozilla.org/en-US/docs/Web/API/URL) interface, which includes useful properties like `origin` and `pathname` (and, in the browser, `hash`). This interface shows up in various places — `event.url` in [hooks](https://kit.svelte.dev/docs/hooks) and [server routes](https://kit.svelte.dev/docs/routing#server), [page.url](https://kit.svelte.dev/docs/$app-state) in [pages](https://kit.svelte.dev/docs/routing#page), `from` and `to` in [beforeNavigateandafterNavigate](https://kit.svelte.dev/docs/$app-navigation) and so on.

### URLSearchParams

Wherever you encounter a URL, you can access query parameters via `url.searchParams`, which is an instance of [URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams):

```
const const foo: string | nullfoo = const url: URLurl.URL.searchParams: URLSearchParamsMDN Reference
searchParams.URLSearchParams.get(name: string): string | nullReturns the first value associated to the given search parameter.
MDN Reference
get('foo');
```

## Web Crypto

The [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API) is made available via the `crypto` global. It’s used internally for [Content Security Policy](https://kit.svelte.dev/docs/configuration#csp) headers, but you can also use it for things like generating UUIDs:

```
const const uuid: `${string}-${string}-${string}-${string}-${string}`uuid = var crypto: CryptoMDN Reference
crypto.Crypto.randomUUID(): `${string}-${string}-${string}-${string}-${string}`Available only in secure contexts.
MDN Reference
randomUUID();
```

[Edit this page on GitHub](https://github.com/sveltejs/kit/edit/main/documentation/docs/10-getting-started/40-web-standards.md) [[llms.txt](https://kit.svelte.dev/docs/kit/web-standards/llms.txt)]

 previous next [[Project structure](https://kit.svelte.dev/docs/kit/project-structure)] [[Routing](https://kit.svelte.dev/docs/kit/routing)]
