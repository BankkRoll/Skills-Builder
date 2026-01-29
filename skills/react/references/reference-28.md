# Server React DOM APIs and more

# Server React DOM APIs

[API Reference](https://react.dev/reference/react)

# Server React DOM APIs

The `react-dom/server` APIs let you server-side render React components to HTML. These APIs are only used on the server at the top level of your app to generate the initial HTML. A [framework](https://react.dev/learn/creating-a-react-app#full-stack-frameworks) may call them for you. Most of your components don’t need to import or use them.

---

## Server APIs for Web Streams

These methods are only available in the environments with [Web Streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API), which includes browsers, Deno, and some modern edge runtimes:

- [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream) renders a React tree to a [Readable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)
- [resume](https://react.dev/reference/react-dom/server/renderToPipeableStream) resumes [prerender](https://react.dev/reference/react-dom/static/prerender) to a [Readable Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream).

### Note

Node.js also includes these methods for compatibility, but they are not recommended due to worse performance. Use the [dedicated Node.js APIs](#server-apis-for-nodejs-streams) instead.

---

## Server APIs for Node.js Streams

These methods are only available in the environments with [Node.js Streams:](https://nodejs.org/api/stream.html)

- [renderToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream) renders a React tree to a pipeable [Node.js Stream.](https://nodejs.org/api/stream.html)
- [resumeToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream) resumes [prerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream) to a pipeable [Node.js Stream.](https://nodejs.org/api/stream.html)

---

## Legacy Server APIs for non-streaming environments

These methods can be used in the environments that don’t support streams:

- [renderToString](https://react.dev/reference/react-dom/server/renderToString) renders a React tree to a string.
- [renderToStaticMarkup](https://react.dev/reference/react-dom/server/renderToStaticMarkup) renders a non-interactive React tree to a string.

They have limited functionality compared to the streaming APIs.

[PrevioushydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)[NextrenderToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# prerender

[API Reference](https://react.dev/reference/react)[Static APIs](https://react.dev/reference/react-dom/static)

# prerender

`prerender` renders a React tree to a static HTML string using a [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API).

$

```
const {prelude, postponed} = await prerender(reactNode, options?)
```

/$

- [Reference](#reference)
  - [prerender(reactNode, options?)](#prerender)
- [Usage](#usage)
  - [Rendering a React tree to a stream of static HTML](#rendering-a-react-tree-to-a-stream-of-static-html)
  - [Rendering a React tree to a string of static HTML](#rendering-a-react-tree-to-a-string-of-static-html)
  - [Waiting for all data to load](#waiting-for-all-data-to-load)
  - [Aborting prerendering](#aborting-prerendering)
- [Troubleshooting](#troubleshooting)
  - [My stream doesn’t start until the entire app is rendered](#my-stream-doesnt-start-until-the-entire-app-is-rendered)

### Note

This API depends on [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) For Node.js, use [prerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream) instead.

---

## Reference

### prerender(reactNode, options?)

Call `prerender` to render your app to static HTML.

 $

```
import { prerender } from 'react-dom/static';async function handler(request, response) {  const {prelude} = await prerender(<App />, {    bootstrapScripts: ['/main.js']  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

On the client, call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to make the server-generated HTML interactive.

[See more examples below.](#usage)

#### Parameters

- `reactNode`: A React node you want to render to HTML. For example, a JSX node like `<App />`. It is expected to represent the entire document, so the App component should render the `<html>` tag.
- **optional** `options`: An object with static generation options.
  - **optional** `bootstrapScriptContent`: If specified, this string will be placed in an inline `<script>` tag.
  - **optional** `bootstrapScripts`: An array of string URLs for the `<script>` tags to emit on the page. Use this to include the `<script>` that calls [hydrateRoot.](https://react.dev/reference/react-dom/client/hydrateRoot) Omit it if you don’t want to run React on the client at all.
  - **optional** `bootstrapModules`: Like `bootstrapScripts`, but emits [<script type="module">](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) instead.
  - **optional** `identifierPrefix`: A string prefix React uses for IDs generated by [useId.](https://react.dev/reference/react/useId) Useful to avoid conflicts when using multiple roots on the same page. Must be the same prefix as passed to [hydrateRoot.](https://react.dev/reference/react-dom/client/hydrateRoot#parameters)
  - **optional** `namespaceURI`: A string with the root [namespace URI](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElementNS#important_namespace_uris) for the stream. Defaults to regular HTML. Pass `'http://www.w3.org/2000/svg'` for SVG or `'http://www.w3.org/1998/Math/MathML'` for MathML.
  - **optional** `onError`: A callback that fires whenever there is a server error, whether [recoverable](https://react.dev/reference/react-dom/server/renderToReadableStream#recovering-from-errors-outside-the-shell) or [not.](https://react.dev/reference/react-dom/server/renderToReadableStream#recovering-from-errors-inside-the-shell) By default, this only calls `console.error`. If you override it to [log crash reports,](https://react.dev/reference/react-dom/server/renderToReadableStream#logging-crashes-on-the-server) make sure that you still call `console.error`. You can also use it to [adjust the status code](https://react.dev/reference/react-dom/server/renderToReadableStream#setting-the-status-code) before the shell is emitted.
  - **optional** `progressiveChunkSize`: The number of bytes in a chunk. [Read more about the default heuristic.](https://github.com/facebook/react/blob/14c2be8dac2d5482fda8a0906a31d239df8551fc/packages/react-server/src/ReactFizzServer.js#L210-L225)
  - **optional** `signal`: An [abort signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) that lets you [abort prerendering](#aborting-prerendering) and render the rest on the client.

#### Returns

`prerender` returns a Promise:

- If rendering the is successful, the Promise will resolve to an object containing:
  - `prelude`: a [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) of HTML. You can use this stream to send a response in chunks, or you can read the entire stream into a string.
  - `postponed`: a JSON-serializeable, opaque object that can be passed to [resume](https://react.dev/reference/react-dom/server/resume) if `prerender` did not finish. Otherwise `null` indicating that the `prelude` contains all the content and no resume is necessary.
- If rendering fails, the Promise will be rejected. [Use this to output a fallback shell.](https://react.dev/reference/react-dom/server/renderToReadableStream#recovering-from-errors-inside-the-shell)

#### Caveats

`nonce` is not an available option when prerendering. Nonces must be unique per request and if you use nonces to secure your application with [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) it would be inappropriate and insecure to include the nonce value in the prerender itself.

### Note

### When should I useprerender?

The static `prerender` API is used for static server-side generation (SSG). Unlike `renderToString`, `prerender` waits for all data to load before resolving. This makes it suitable for generating static HTML for a full page, including data that needs to be fetched using Suspense. To stream content as it loads, use a streaming server-side render (SSR) API like [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).

`prerender` can be aborted and later either continued with `resumeAndPrerender` or resumed with `resume` to support partial pre-rendering.

---

## Usage

### Rendering a React tree to a stream of static HTML

Call `prerender` to render your React tree to static HTML into a [Readable Web Stream:](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream):

 $

```
import { prerender } from 'react-dom/static';async function handler(request) {  const {prelude} = await prerender(<App />, {    bootstrapScripts: ['/main.js']  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

Along with the root component, you need to provide a list of bootstrap `<script>` paths. Your root component should return **the entire document including the root<html>tag.**

For example, it might look like this:

 $

```
export default function App() {  return (    <html>      <head>        <meta charSet="utf-8" />        <meta name="viewport" content="width=device-width, initial-scale=1" />        <link rel="stylesheet" href="/styles.css"></link>        <title>My app</title>      </head>      <body>        <Router />      </body>    </html>  );}
```

/$

React will inject the [doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) and your bootstrap `<script>` tags into the resulting HTML stream:

 $

```
<!DOCTYPE html><html>  </html><script src="/main.js" async=""></script>
```

/$

On the client, your bootstrap script should [hydrate the entiredocumentwith a call tohydrateRoot:](https://react.dev/reference/react-dom/client/hydrateRoot#hydrating-an-entire-document)

 $

```
import { hydrateRoot } from 'react-dom/client';import App from './App.js';hydrateRoot(document, <App />);
```

/$

This will attach event listeners to the static server-generated HTML and make it interactive.

##### Deep Dive

#### Reading CSS and JS asset paths from the build output

The final asset URLs (like JavaScript and CSS files) are often hashed after the build. For example, instead of `styles.css` you might end up with `styles.123456.css`. Hashing static asset filenames guarantees that every distinct build of the same asset will have a different filename. This is useful because it lets you safely enable long-term caching for static assets: a file with a certain name would never change content.

However, if you don’t know the asset URLs until after the build, there’s no way for you to put them in the source code. For example, hardcoding `"/styles.css"` into JSX like earlier wouldn’t work. To keep them out of your source code, your root component can read the real filenames from a map passed as a prop:

$

```
export default function App({ assetMap }) {  return (    <html>      <head>        <title>My app</title>        <link rel="stylesheet" href={assetMap['styles.css']}></link>      </head>      ...    </html>  );}
```

/$

On the server, render `<App assetMap={assetMap} />` and pass your `assetMap` with the asset URLs:

$

```
// You'd need to get this JSON from your build tooling, e.g. read it from the build output.const assetMap = {  'styles.css': '/styles.123456.css',  'main.js': '/main.123456.js'};async function handler(request) {  const {prelude} = await prerender(<App assetMap={assetMap} />, {    bootstrapScripts: [assetMap['/main.js']]  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

Since your server is now rendering `<App assetMap={assetMap} />`, you need to render it with `assetMap` on the client too to avoid hydration errors. You can serialize and pass `assetMap` to the client like this:

$

```
// You'd need to get this JSON from your build tooling.const assetMap = {  'styles.css': '/styles.123456.css',  'main.js': '/main.123456.js'};async function handler(request) {  const {prelude} = await prerender(<App assetMap={assetMap} />, {    // Careful: It's safe to stringify() this because this data isn't user-generated.    bootstrapScriptContent: `window.assetMap = ${JSON.stringify(assetMap)};`,    bootstrapScripts: [assetMap['/main.js']],  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

In the example above, the `bootstrapScriptContent` option adds an extra inline `<script>` tag that sets the global `window.assetMap` variable on the client. This lets the client code read the same `assetMap`:

$

```
import { hydrateRoot } from 'react-dom/client';import App from './App.js';hydrateRoot(document, <App assetMap={window.assetMap} />);
```

/$

Both client and server render `App` with the same `assetMap` prop, so there are no hydration errors.

---

### Rendering a React tree to a string of static HTML

Call `prerender` to render your app to a static HTML string:

 $

```
import { prerender } from 'react-dom/static';async function renderToString() {  const {prelude} = await prerender(<App />, {    bootstrapScripts: ['/main.js']  });  const reader = prelude.getReader();  let content = '';  while (true) {    const {done, value} = await reader.read();    if (done) {      return content;    }    content += Buffer.from(value).toString('utf8');  }}
```

/$

This will produce the initial non-interactive HTML output of your React components. On the client, you will need to call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to *hydrate* that server-generated HTML and make it interactive.

---

### Waiting for all data to load

`prerender` waits for all data to load before finishing the static HTML generation and resolving. For example, consider a profile page that shows a cover, a sidebar with friends and photos, and a list of posts:

 $

```
function ProfilePage() {  return (    <ProfileLayout>      <ProfileCover />      <Sidebar>        <Friends />        <Photos />      </Sidebar>      <Suspense fallback={<PostsGlimmer />}>        <Posts />      </Suspense>    </ProfileLayout>  );}
```

/$

Imagine that `<Posts />` needs to load some data, which takes some time. Ideally, you’d want wait for the posts to finish so it’s included in the HTML. To do this, you can use Suspense to suspend on the data, and `prerender` will wait for the suspended content to finish before resolving to the static HTML.

### Note

**Only Suspense-enabled data sources will activate the Suspense component.** They include:

- Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/getting-started/react-essentials)
- Lazy-loading component code with [lazy](https://react.dev/reference/react/lazy)
- Reading the value of a Promise with [use](https://react.dev/reference/react/use)

Suspense **does not** detect when data is fetched inside an Effect or event handler.

The exact way you would load data in the `Posts` component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

---

### Aborting prerendering

You can force the prerender to “give up” after a timeout:

 $

```
async function renderToString() {  const controller = new AbortController();  setTimeout(() => {    controller.abort()  }, 10000);  try {    // the prelude will contain all the HTML that was prerendered    // before the controller aborted.    const {prelude} = await prerender(<App />, {      signal: controller.signal,    });    //...
```

/$

Any Suspense boundaries with incomplete children will be included in the prelude in the fallback state.

This can be used for partial prerendering together with [resume](https://react.dev/reference/react-dom/server/resume) or [resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender).

## Troubleshooting

### My stream doesn’t start until the entire app is rendered

The `prerender` response waits for the entire app to finish rendering, including waiting for all Suspense boundaries to resolve, before resolving. It is designed for static site generation (SSG) ahead of time and does not support streaming more content as it loads.

To stream content as it loads, use a streaming server render API like [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).

[PreviousStatic APIs](https://react.dev/reference/react-dom/static)[NextprerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream)

---

# prerenderToNodeStream

[API Reference](https://react.dev/reference/react)[Static APIs](https://react.dev/reference/react-dom/static)

# prerenderToNodeStream

`prerenderToNodeStream` renders a React tree to a static HTML string using a [Node.js Stream.](https://nodejs.org/api/stream.html)

$

```
const {prelude, postponed} = await prerenderToNodeStream(reactNode, options?)
```

/$

- [Reference](#reference)
  - [prerenderToNodeStream(reactNode, options?)](#prerender)
- [Usage](#usage)
  - [Rendering a React tree to a stream of static HTML](#rendering-a-react-tree-to-a-stream-of-static-html)
  - [Rendering a React tree to a string of static HTML](#rendering-a-react-tree-to-a-string-of-static-html)
  - [Waiting for all data to load](#waiting-for-all-data-to-load)
  - [Aborting prerendering](#aborting-prerendering)
- [Troubleshooting](#troubleshooting)
  - [My stream doesn’t start until the entire app is rendered](#my-stream-doesnt-start-until-the-entire-app-is-rendered)

### Note

This API is specific to Node.js. Environments with [Web Streams,](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) like Deno and modern edge runtimes, should use [prerender](https://react.dev/reference/react-dom/static/prerender) instead.

---

## Reference

### prerenderToNodeStream(reactNode, options?)

Call `prerenderToNodeStream` to render your app to static HTML.

 $

```
import { prerenderToNodeStream } from 'react-dom/static';// The route handler syntax depends on your backend frameworkapp.use('/', async (request, response) => {  const { prelude } = await prerenderToNodeStream(<App />, {    bootstrapScripts: ['/main.js'],  });  response.setHeader('Content-Type', 'text/plain');  prelude.pipe(response);});
```

/$

On the client, call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to make the server-generated HTML interactive.

[See more examples below.](#usage)

#### Parameters

- `reactNode`: A React node you want to render to HTML. For example, a JSX node like `<App />`. It is expected to represent the entire document, so the App component should render the `<html>` tag.
- **optional** `options`: An object with static generation options.
  - **optional** `bootstrapScriptContent`: If specified, this string will be placed in an inline `<script>` tag.
  - **optional** `bootstrapScripts`: An array of string URLs for the `<script>` tags to emit on the page. Use this to include the `<script>` that calls [hydrateRoot.](https://react.dev/reference/react-dom/client/hydrateRoot) Omit it if you don’t want to run React on the client at all.
  - **optional** `bootstrapModules`: Like `bootstrapScripts`, but emits [<script type="module">](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) instead.
  - **optional** `identifierPrefix`: A string prefix React uses for IDs generated by [useId.](https://react.dev/reference/react/useId) Useful to avoid conflicts when using multiple roots on the same page. Must be the same prefix as passed to [hydrateRoot.](https://react.dev/reference/react-dom/client/hydrateRoot#parameters)
  - **optional** `namespaceURI`: A string with the root [namespace URI](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElementNS#important_namespace_uris) for the stream. Defaults to regular HTML. Pass `'http://www.w3.org/2000/svg'` for SVG or `'http://www.w3.org/1998/Math/MathML'` for MathML.
  - **optional** `onError`: A callback that fires whenever there is a server error, whether [recoverable](https://react.dev/reference/react-dom/server/renderToPipeableStream#recovering-from-errors-outside-the-shell) or [not.](https://react.dev/reference/react-dom/server/renderToPipeableStream#recovering-from-errors-inside-the-shell) By default, this only calls `console.error`. If you override it to [log crash reports,](https://react.dev/reference/react-dom/server/renderToPipeableStream#logging-crashes-on-the-server) make sure that you still call `console.error`. You can also use it to [adjust the status code](https://react.dev/reference/react-dom/server/renderToPipeableStream#setting-the-status-code) before the shell is emitted.
  - **optional** `progressiveChunkSize`: The number of bytes in a chunk. [Read more about the default heuristic.](https://github.com/facebook/react/blob/14c2be8dac2d5482fda8a0906a31d239df8551fc/packages/react-server/src/ReactFizzServer.js#L210-L225)
  - **optional** `signal`: An [abort signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) that lets you [abort prerendering](#aborting-prerendering) and render the rest on the client.

#### Returns

`prerenderToNodeStream` returns a Promise:

- If rendering the is successful, the Promise will resolve to an object containing:
  - `prelude`: a [Node.js Stream.](https://nodejs.org/api/stream.html) of HTML. You can use this stream to send a response in chunks, or you can read the entire stream into a string.
  - `postponed`: a JSON-serializeable, opaque object that can be passed to [resumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream) if `prerenderToNodeStream` did not finish. Otherwise `null` indicating that the `prelude` contains all the content and no resume is necessary.
- If rendering fails, the Promise will be rejected. [Use this to output a fallback shell.](https://react.dev/reference/react-dom/server/renderToPipeableStream#recovering-from-errors-inside-the-shell)

#### Caveats

`nonce` is not an available option when prerendering. Nonces must be unique per request and if you use nonces to secure your application with [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) it would be inappropriate and insecure to include the nonce value in the prerender itself.

### Note

### When should I useprerenderToNodeStream?

The static `prerenderToNodeStream` API is used for static server-side generation (SSG). Unlike `renderToString`, `prerenderToNodeStream` waits for all data to load before resolving. This makes it suitable for generating static HTML for a full page, including data that needs to be fetched using Suspense. To stream content as it loads, use a streaming server-side render (SSR) API like [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).

`prerenderToNodeStream` can be aborted and resumed later with `resumeToPipeableStream` to support partial pre-rendering.

---

## Usage

### Rendering a React tree to a stream of static HTML

Call `prerenderToNodeStream` to render your React tree to static HTML into a [Node.js Stream](https://nodejs.org/api/stream.html):

 $

```
import { prerenderToNodeStream } from 'react-dom/static';// The route handler syntax depends on your backend frameworkapp.use('/', async (request, response) => {  const { prelude } = await prerenderToNodeStream(<App />, {    bootstrapScripts: ['/main.js'],  });  response.setHeader('Content-Type', 'text/plain');  prelude.pipe(response);});
```

/$

Along with the root component, you need to provide a list of bootstrap `<script>` paths. Your root component should return **the entire document including the root<html>tag.**

For example, it might look like this:

 $

```
export default function App() {  return (    <html>      <head>        <meta charSet="utf-8" />        <meta name="viewport" content="width=device-width, initial-scale=1" />        <link rel="stylesheet" href="/styles.css"></link>        <title>My app</title>      </head>      <body>        <Router />      </body>    </html>  );}
```

/$

React will inject the [doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) and your bootstrap `<script>` tags into the resulting HTML stream:

 $

```
<!DOCTYPE html><html>  </html><script src="/main.js" async=""></script>
```

/$

On the client, your bootstrap script should [hydrate the entiredocumentwith a call tohydrateRoot:](https://react.dev/reference/react-dom/client/hydrateRoot#hydrating-an-entire-document)

 $

```
import { hydrateRoot } from 'react-dom/client';import App from './App.js';hydrateRoot(document, <App />);
```

/$

This will attach event listeners to the static server-generated HTML and make it interactive.

##### Deep Dive

#### Reading CSS and JS asset paths from the build output

The final asset URLs (like JavaScript and CSS files) are often hashed after the build. For example, instead of `styles.css` you might end up with `styles.123456.css`. Hashing static asset filenames guarantees that every distinct build of the same asset will have a different filename. This is useful because it lets you safely enable long-term caching for static assets: a file with a certain name would never change content.

However, if you don’t know the asset URLs until after the build, there’s no way for you to put them in the source code. For example, hardcoding `"/styles.css"` into JSX like earlier wouldn’t work. To keep them out of your source code, your root component can read the real filenames from a map passed as a prop:

$

```
export default function App({ assetMap }) {  return (    <html>      <head>        <title>My app</title>        <link rel="stylesheet" href={assetMap['styles.css']}></link>      </head>      ...    </html>  );}
```

/$

On the server, render `<App assetMap={assetMap} />` and pass your `assetMap` with the asset URLs:

$

```
// You'd need to get this JSON from your build tooling, e.g. read it from the build output.const assetMap = {  'styles.css': '/styles.123456.css',  'main.js': '/main.123456.js'};app.use('/', async (request, response) => {  const { prelude } = await prerenderToNodeStream(<App />, {    bootstrapScripts: [assetMap['/main.js']]  });  response.setHeader('Content-Type', 'text/html');  prelude.pipe(response);});
```

/$

Since your server is now rendering `<App assetMap={assetMap} />`, you need to render it with `assetMap` on the client too to avoid hydration errors. You can serialize and pass `assetMap` to the client like this:

$

```
// You'd need to get this JSON from your build tooling.const assetMap = {  'styles.css': '/styles.123456.css',  'main.js': '/main.123456.js'};app.use('/', async (request, response) => {  const { prelude } = await prerenderToNodeStream(<App />, {    // Careful: It's safe to stringify() this because this data isn't user-generated.    bootstrapScriptContent: `window.assetMap = ${JSON.stringify(assetMap)};`,    bootstrapScripts: [assetMap['/main.js']],  });  response.setHeader('Content-Type', 'text/html');  prelude.pipe(response);});
```

/$

In the example above, the `bootstrapScriptContent` option adds an extra inline `<script>` tag that sets the global `window.assetMap` variable on the client. This lets the client code read the same `assetMap`:

$

```
import { hydrateRoot } from 'react-dom/client';import App from './App.js';hydrateRoot(document, <App assetMap={window.assetMap} />);
```

/$

Both client and server render `App` with the same `assetMap` prop, so there are no hydration errors.

---

### Rendering a React tree to a string of static HTML

Call `prerenderToNodeStream` to render your app to a static HTML string:

 $

```
import { prerenderToNodeStream } from 'react-dom/static';async function renderToString() {  const {prelude} = await prerenderToNodeStream(<App />, {    bootstrapScripts: ['/main.js']  });  return new Promise((resolve, reject) => {    let data = '';    prelude.on('data', chunk => {      data += chunk;    });    prelude.on('end', () => resolve(data));    prelude.on('error', reject);  });}
```

/$

This will produce the initial non-interactive HTML output of your React components. On the client, you will need to call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to *hydrate* that server-generated HTML and make it interactive.

---

### Waiting for all data to load

`prerenderToNodeStream` waits for all data to load before finishing the static HTML generation and resolving. For example, consider a profile page that shows a cover, a sidebar with friends and photos, and a list of posts:

 $

```
function ProfilePage() {  return (    <ProfileLayout>      <ProfileCover />      <Sidebar>        <Friends />        <Photos />      </Sidebar>      <Suspense fallback={<PostsGlimmer />}>        <Posts />      </Suspense>    </ProfileLayout>  );}
```

/$

Imagine that `<Posts />` needs to load some data, which takes some time. Ideally, you’d want wait for the posts to finish so it’s included in the HTML. To do this, you can use Suspense to suspend on the data, and `prerenderToNodeStream` will wait for the suspended content to finish before resolving to the static HTML.

### Note

**Only Suspense-enabled data sources will activate the Suspense component.** They include:

- Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/getting-started/react-essentials)
- Lazy-loading component code with [lazy](https://react.dev/reference/react/lazy)
- Reading the value of a Promise with [use](https://react.dev/reference/react/use)

Suspense **does not** detect when data is fetched inside an Effect or event handler.

The exact way you would load data in the `Posts` component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

---

### Aborting prerendering

You can force the prerender to “give up” after a timeout:

 $

```
async function renderToString() {  const controller = new AbortController();  setTimeout(() => {    controller.abort()  }, 10000);  try {    // the prelude will contain all the HTML that was prerendered    // before the controller aborted.    const {prelude} = await prerenderToNodeStream(<App />, {      signal: controller.signal,    });    //...
```

/$

Any Suspense boundaries with incomplete children will be included in the prelude in the fallback state.

This can be used for partial prerendering together with [resumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream) or [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream).

## Troubleshooting

### My stream doesn’t start until the entire app is rendered

The `prerenderToNodeStream` response waits for the entire app to finish rendering, including waiting for all Suspense boundaries to resolve, before resolving. It is designed for static site generation (SSG) ahead of time and does not support streaming more content as it loads.

To stream content as it loads, use a streaming server render API like [renderToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream).

[Previousprerender](https://react.dev/reference/react-dom/static/prerender)[NextresumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender)

---

# resumeAndPrerender

[API Reference](https://react.dev/reference/react)[Static APIs](https://react.dev/reference/react-dom/static)

# resumeAndPrerender

`resumeAndPrerender` continues a prerendered React tree to a static HTML string using a [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API).

$

```
const { prelude,postpone } = await resumeAndPrerender(reactNode, postponedState, options?)
```

/$

- [Reference](#reference)
  - [resumeAndPrerender(reactNode, postponedState, options?)](#resumeandprerender)
- [Usage](#usage)
  - [Further reading](#further-reading)

### Note

This API depends on [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) For Node.js, use [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream) instead.

---

## Reference

### resumeAndPrerender(reactNode, postponedState, options?)

Call `resumeAndPrerender` to continue a prerendered React tree to a static HTML string.

 $

```
import { resumeAndPrerender } from 'react-dom/static';import { getPostponedState } from 'storage';async function handler(request, response) {  const postponedState = getPostponedState(request);  const { prelude } = await resumeAndPrerender(<App />, postponedState, {    bootstrapScripts: ['/main.js']  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

On the client, call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to make the server-generated HTML interactive.

[See more examples below.](#usage)

#### Parameters

- `reactNode`: The React node you called `prerender` (or a previous `resumeAndPrerender`) with. For example, a JSX element like `<App />`. It is expected to represent the entire document, so the `App` component should render the `<html>` tag.
- `postponedState`: The opaque `postpone` object returned from a [prerender API](https://react.dev/reference/react-dom/static/index), loaded from wherever you stored it (e.g. redis, a file, or S3).
- **optional** `options`: An object with streaming options.
  - **optional** `signal`: An [abort signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) that lets you [abort server rendering](#aborting-server-rendering) and render the rest on the client.
  - **optional** `onError`: A callback that fires whenever there is a server error, whether [recoverable](#recovering-from-errors-outside-the-shell) or [not.](#recovering-from-errors-inside-the-shell) By default, this only calls `console.error`. If you override it to [log crash reports,](#logging-crashes-on-the-server) make sure that you still call `console.error`.

#### Returns

`prerender` returns a Promise:

- If rendering the is successful, the Promise will resolve to an object containing:
  - `prelude`: a [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) of HTML. You can use this stream to send a response in chunks, or you can read the entire stream into a string.
  - `postponed`: an JSON-serializeable, opaque object that can be passed to [resume](https://react.dev/reference/react-dom/server/resume) or [resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender) if `prerender` is aborted.
- If rendering fails, the Promise will be rejected. [Use this to output a fallback shell.](https://react.dev/reference/react-dom/server/renderToReadableStream#recovering-from-errors-inside-the-shell)

#### Caveats

`nonce` is not an available option when prerendering. Nonces must be unique per request and if you use nonces to secure your application with [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) it would be inappropriate and insecure to include the nonce value in the prerender itself.

### Note

### When should I useresumeAndPrerender?

The static `resumeAndPrerender` API is used for static server-side generation (SSG). Unlike `renderToString`, `resumeAndPrerender` waits for all data to load before resolving. This makes it suitable for generating static HTML for a full page, including data that needs to be fetched using Suspense. To stream content as it loads, use a streaming server-side render (SSR) API like [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).

`resumeAndPrerender` can be aborted and later either continued with another `resumeAndPrerender` or resumed with `resume` to support partial pre-rendering.

---

## Usage

### Further reading

`resumeAndPrerender` behaves similarly to [prerender](https://react.dev/reference/react-dom/static/prerender) but can be used to continue a previously started prerendering process that was aborted.
For more information about resuming a prerendered tree, see the [resume documentation](https://react.dev/reference/react-dom/server/resume#resuming-a-prerender).

[PreviousprerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream)[NextresumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream)

---

# resumeAndPrerenderToNodeStream

[API Reference](https://react.dev/reference/react)[Static APIs](https://react.dev/reference/react-dom/static)

# resumeAndPrerenderToNodeStream

`resumeAndPrerenderToNodeStream` continues a prerendered React tree to a static HTML string using a a [Node.js Stream.](https://nodejs.org/api/stream.html).

$

```
const {prelude, postponed} = await resumeAndPrerenderToNodeStream(reactNode, postponedState, options?)
```

/$

- [Reference](#reference)
  - [resumeAndPrerenderToNodeStream(reactNode, postponedState, options?)](#resumeandprerendertolnodestream)
- [Usage](#usage)
  - [Further reading](#further-reading)

### Note

This API is specific to Node.js. Environments with [Web Streams,](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) like Deno and modern edge runtimes, should use [prerender](https://react.dev/reference/react-dom/static/prerender) instead.

---

## Reference

### resumeAndPrerenderToNodeStream(reactNode, postponedState, options?)

Call `resumeAndPrerenderToNodeStream` to continue a prerendered React tree to a static HTML string.

 $

```
import { resumeAndPrerenderToNodeStream } from 'react-dom/static';import { getPostponedState } from 'storage';async function handler(request, writable) {  const postponedState = getPostponedState(request);  const { prelude } = await resumeAndPrerenderToNodeStream(<App />, JSON.parse(postponedState));  prelude.pipe(writable);}
```

/$

On the client, call [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) to make the server-generated HTML interactive.

[See more examples below.](#usage)

#### Parameters

- `reactNode`: The React node you called `prerender` (or a previous `resumeAndPrerenderToNodeStream`) with. For example, a JSX element like `<App />`. It is expected to represent the entire document, so the `App` component should render the `<html>` tag.
- `postponedState`: The opaque `postpone` object returned from a [prerender API](https://react.dev/reference/react-dom/static/index), loaded from wherever you stored it (e.g. redis, a file, or S3).
- **optional** `options`: An object with streaming options.
  - **optional** `signal`: An [abort signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) that lets you [abort server rendering](#aborting-server-rendering) and render the rest on the client.
  - **optional** `onError`: A callback that fires whenever there is a server error, whether [recoverable](#recovering-from-errors-outside-the-shell) or [not.](#recovering-from-errors-inside-the-shell) By default, this only calls `console.error`. If you override it to [log crash reports,](#logging-crashes-on-the-server) make sure that you still call `console.error`.

#### Returns

`resumeAndPrerenderToNodeStream` returns a Promise:

- If rendering the is successful, the Promise will resolve to an object containing:
  - `prelude`: a [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) of HTML. You can use this stream to send a response in chunks, or you can read the entire stream into a string.
  - `postponed`: an JSON-serializeable, opaque object that can be passed to [resumeToNodeStream](https://react.dev/reference/react-dom/server/resume) or [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream) if `resumeAndPrerenderToNodeStream` is aborted.
- If rendering fails, the Promise will be rejected. [Use this to output a fallback shell.](https://react.dev/reference/react-dom/server/renderToReadableStream#recovering-from-errors-inside-the-shell)

#### Caveats

`nonce` is not an available option when prerendering. Nonces must be unique per request and if you use nonces to secure your application with [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) it would be inappropriate and insecure to include the nonce value in the prerender itself.

### Note

### When should I useresumeAndPrerenderToNodeStream?

The static `resumeAndPrerenderToNodeStream` API is used for static server-side generation (SSG). Unlike `renderToString`, `resumeAndPrerenderToNodeStream` waits for all data to load before resolving. This makes it suitable for generating static HTML for a full page, including data that needs to be fetched using Suspense. To stream content as it loads, use a streaming server-side render (SSR) API like [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).

`resumeAndPrerenderToNodeStream` can be aborted and later either continued with another `resumeAndPrerenderToNodeStream` or resumed with `resume` to support partial pre-rendering.

---

## Usage

### Further reading

`resumeAndPrerenderToNodeStream` behaves similarly to [prerender](https://react.dev/reference/react-dom/static/prerender) but can be used to continue a previously started prerendering process that was aborted.
For more information about resuming a prerendered tree, see the [resume documentation](https://react.dev/reference/react-dom/server/resume#resuming-a-prerender).

[PreviousresumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender)

---

# Static React DOM APIs

[API Reference](https://react.dev/reference/react)

# Static React DOM APIs

The `react-dom/static` APIs let you generate static HTML for React components. They have limited functionality compared to the streaming APIs. A [framework](https://react.dev/learn/creating-a-react-app#full-stack-frameworks) may call them for you. Most of your components don’t need to import or use them.

---

## Static APIs for Web Streams

These methods are only available in the environments with [Web Streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API), which includes browsers, Deno, and some modern edge runtimes:

- [prerender](https://react.dev/reference/react-dom/static/prerender) renders a React tree to static HTML with a [Readable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)
- Experimental only [resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender) continues a prerendered React tree to static HTML with a [Readable Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream).

Node.js also includes these methods for compatibility, but they are not recommended due to worse performance. Use the [dedicated Node.js APIs](#static-apis-for-nodejs-streams) instead.

---

## Static APIs for Node.js Streams

These methods are only available in the environments with [Node.js Streams](https://nodejs.org/api/stream.html):

- [prerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream) renders a React tree to static HTML with a [Node.js Stream.](https://nodejs.org/api/stream.html)
- Experimental only [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream) continues a prerendered React tree to static HTML with a [Node.js Stream.](https://nodejs.org/api/stream.html)

[PreviousresumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream)[Nextprerender](https://react.dev/reference/react-dom/static/prerender)

---

# unmountComponentAtNode

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react-dom)

# unmountComponentAtNode

### Deprecated

This API will be removed in a future major version of React.

In React 18, `unmountComponentAtNode` was replaced by [root.unmount()](https://react.dev/reference/react-dom/client/createRoot#root-unmount).

`unmountComponentAtNode` removes a mounted React component from the DOM.

$

```
unmountComponentAtNode(domNode)
```

/$

- [Reference](#reference)
  - [unmountComponentAtNode(domNode)](#unmountcomponentatnode)
- [Usage](#usage)
  - [Removing a React app from a DOM element](#removing-a-react-app-from-a-dom-element)

---

## Reference

### unmountComponentAtNode(domNode)

Call `unmountComponentAtNode` to remove a mounted React component from the DOM and clean up its event handlers and state.

 $

```
import { unmountComponentAtNode } from 'react-dom';const domNode = document.getElementById('root');render(<App />, domNode);unmountComponentAtNode(domNode);
```

/$

[See more examples below.](#usage)

#### Parameters

- `domNode`: A [DOM element.](https://developer.mozilla.org/en-US/docs/Web/API/Element) React will remove a mounted React component from this element.

#### Returns

`unmountComponentAtNode` returns `true` if a component was unmounted and `false` otherwise.

---

## Usage

Call `unmountComponentAtNode` to remove a mounted React component from a browser DOM node and clean up its event handlers and state.

 $

```
import { render, unmountComponentAtNode } from 'react-dom';import App from './App.js';const rootNode = document.getElementById('root');render(<App />, rootNode);// ...unmountComponentAtNode(rootNode);
```

/$

### Removing a React app from a DOM element

Occasionally, you may want to “sprinkle” React on an existing page, or a page that is not fully written in React. In those cases, you may need to “stop” the React app, by removing all of the UI, state, and listeners from the DOM node it was rendered to.

In this example, clicking “Render React App” will render a React app. Click “Unmount React App” to destroy it:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import './styles.css';
import { render, unmountComponentAtNode } from 'react-dom';
import App from './App.js';

const domNode = document.getElementById('root');

document.getElementById('render').addEventListener('click', () => {
  render(<App />, domNode);
});

document.getElementById('unmount').addEventListener('click', () => {
  unmountComponentAtNode(domNode);
});
```

/$[Previousrender](https://react.dev/reference/react-dom/render)[NextClient APIs](https://react.dev/reference/react-dom/client)

---

# React DOM APIs

[API Reference](https://react.dev/reference/react)

# React DOM APIs

The `react-dom` package contains methods that are only supported for the web applications (which run in the browser DOM environment). They are not supported for React Native.

---

## APIs

These APIs can be imported from your components. They are rarely used:

- [createPortal](https://react.dev/reference/react-dom/createPortal) lets you render child components in a different part of the DOM tree.
- [flushSync](https://react.dev/reference/react-dom/flushSync) lets you force React to flush a state update and update the DOM synchronously.

## Resource Preloading APIs

These APIs can be used to make apps faster by pre-loading resources such as scripts, stylesheets, and fonts as soon as you know you need them, for example before navigating to another page where the resources will be used.

[React-based frameworks](https://react.dev/learn/creating-a-react-app) frequently handle resource loading for you, so you might not have to call these APIs yourself. Consult your framework’s documentation for details.

- [prefetchDNS](https://react.dev/reference/react-dom/prefetchDNS) lets you prefetch the IP address of a DNS domain name that you expect to connect to.
- [preconnect](https://react.dev/reference/react-dom/preconnect) lets you connect to a server you expect to request resources from, even if you don’t know what resources you’ll need yet.
- [preload](https://react.dev/reference/react-dom/preload) lets you fetch a stylesheet, font, image, or external script that you expect to use.
- [preloadModule](https://react.dev/reference/react-dom/preloadModule) lets you fetch an ESM module that you expect to use.
- [preinit](https://react.dev/reference/react-dom/preinit) lets you fetch and evaluate an external script or fetch and insert a stylesheet.
- [preinitModule](https://react.dev/reference/react-dom/preinitModule) lets you fetch and evaluate an ESM module.

---

## Entry points

The `react-dom` package provides two additional entry points:

- [react-dom/client](https://react.dev/reference/react-dom/client) contains APIs to render React components on the client (in the browser).
- [react-dom/server](https://react.dev/reference/react-dom/server) contains APIs to render React components on the server.

---

## Removed APIs

These APIs were removed in React 19:

- [findDOMNode](https://18.react.dev/reference/react-dom/findDOMNode): see [alternatives](https://18.react.dev/reference/react-dom/findDOMNode#alternatives).
- [hydrate](https://18.react.dev/reference/react-dom/hydrate): use [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) instead.
- [render](https://18.react.dev/reference/react-dom/render): use [createRoot](https://react.dev/reference/react-dom/client/createRoot) instead.
- [unmountComponentAtNode](https://react.dev/reference/react-dom/unmountComponentAtNode): use [root.unmount()](https://react.dev/reference/react-dom/client/createRoot#root-unmount) instead.
- [renderToNodeStream](https://18.react.dev/reference/react-dom/server/renderToNodeStream): use [react-dom/server](https://react.dev/reference/react-dom/server) APIs instead.
- [renderToStaticNodeStream](https://18.react.dev/reference/react-dom/server/renderToStaticNodeStream): use [react-dom/server](https://react.dev/reference/react-dom/server) APIs instead.

[Previous<title>](https://react.dev/reference/react-dom/components/title)[NextcreatePortal](https://react.dev/reference/react-dom/createPortal)

---

# React Reference Overview

[API Reference](https://react.dev/reference/react)

# React Reference Overview

This section provides detailed reference documentation for working with React. For an introduction to React, please visit the [Learn](https://react.dev/learn) section.

The React reference documentation is broken down into functional subsections:

## React

Programmatic React features:

- [Hooks](https://react.dev/reference/react/hooks) - Use different React features from your components.
- [Components](https://react.dev/reference/react/components) - Built-in components that you can use in your JSX.
- [APIs](https://react.dev/reference/react/apis) - APIs that are useful for defining components.
- [Directives](https://react.dev/reference/rsc/directives) - Provide instructions to bundlers compatible with React Server Components.

## React DOM

React DOM contains features that are only supported for web applications (which run in the browser DOM environment). This section is broken into the following:

- [Hooks](https://react.dev/reference/react-dom/hooks) - Hooks for web applications which run in the browser DOM environment.
- [Components](https://react.dev/reference/react-dom/components) - React supports all of the browser built-in HTML and SVG components.
- [APIs](https://react.dev/reference/react-dom) - The `react-dom` package contains methods supported only in web applications.
- [Client APIs](https://react.dev/reference/react-dom/client) - The `react-dom/client` APIs let you render React components on the client (in the browser).
- [Server APIs](https://react.dev/reference/react-dom/server) - The `react-dom/server` APIs let you render React components to HTML on the server.
- [Static APIs](https://react.dev/reference/react-dom/static) - The `react-dom/static` APIs let you generate static HTML for React components.

## React Compiler

The React Compiler is a build-time optimization tool that automatically memoizes your React components and values:

- [Configuration](https://react.dev/reference/react-compiler/configuration) - Configuration options for React Compiler.
- [Directives](https://react.dev/reference/react-compiler/directives) - Function-level directives to control compilation.
- [Compiling Libraries](https://react.dev/reference/react-compiler/compiling-libraries) - Guide for shipping pre-compiled library code.

## ESLint Plugin React Hooks

The [ESLint plugin for React Hooks](https://react.dev/reference/eslint-plugin-react-hooks) helps enforce the Rules of React:

- [Lints](https://react.dev/reference/eslint-plugin-react-hooks) - Detailed documentation for each lint with examples.

## Rules of React

React has idioms — or rules — for how to express patterns in a way that is easy to understand and yields high-quality applications:

- [Components and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure) – Purity makes your code easier to understand, debug, and allows React to automatically optimize your components and hooks correctly.
- [React calls Components and Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks) – React is responsible for rendering components and hooks when necessary to optimize the user experience.
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) – Hooks are defined using JavaScript functions, but they represent a special type of reusable UI logic with restrictions on where they can be called.

## Legacy APIs

- [Legacy APIs](https://react.dev/reference/react/legacy) - Exported from the `react` package, but not recommended for use in newly written code.

[NextHooks](https://react.dev/reference/react/hooks)

---

# Directives

[API Reference](https://react.dev/reference/react)

# Directives

### React Server Components

Directives are for use in [React Server Components](https://react.dev/reference/rsc/server-components).

Directives provide instructions to [bundlers compatible with React Server Components](https://react.dev/learn/creating-a-react-app#full-stack-frameworks).

---

## Source code directives

- ['use client'](https://react.dev/reference/rsc/use-client) lets you mark what code runs on the client.
- ['use server'](https://react.dev/reference/rsc/use-server) marks server-side functions that can be called from client-side code.

[PreviousServer Functions](https://react.dev/reference/rsc/server-functions)[Next'use client'](https://react.dev/reference/rsc/use-client)
