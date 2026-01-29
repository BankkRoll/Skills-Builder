# React v19 and more

# React v19

[Blog](https://react.dev/blog)

# React v19

December 05, 2024 by [The React Team](https://react.dev/community/team)

---

### Note

### React 19 is now stable!

Additions since this post was originally shared with the React 19 RC in April:

- **Pre-warming for suspended trees**: see [Improvements to Suspense](https://react.dev/blog/2024/04/25/react-19-upgrade-guide#improvements-to-suspense).
- **React DOM static APIs**: see [New React DOM Static APIs](#new-react-dom-static-apis).

*The date for this post has been updated to reflect the stable release date.*

React v19 is now available on npm!

In our [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide), we shared step-by-step instructions for upgrading your app to React 19. In this post, we’ll give an overview of the new features in React 19, and how you can adopt them.

- [What’s new in React 19](#whats-new-in-react-19)
- [Improvements in React 19](#improvements-in-react-19)
- [How to upgrade](#how-to-upgrade)

For a list of breaking changes, see the [Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide).

---

## What’s new in React 19

### Actions

A common use case in React apps is to perform a data mutation and then update state in response. For example, when a user submits a form to change their name, you will make an API request, and then handle the response. In the past, you would need to handle pending states, errors, optimistic updates, and sequential requests manually.

For example, you could handle the pending and error state in `useState`:

 $

```
// Before Actionsfunction UpdateName({}) {  const [name, setName] = useState("");  const [error, setError] = useState(null);  const [isPending, setIsPending] = useState(false);  const handleSubmit = async () => {    setIsPending(true);    const error = await updateName(name);    setIsPending(false);    if (error) {      setError(error);      return;    }     redirect("/path");  };  return (    <div>      <input value={name} onChange={(event) => setName(event.target.value)} />      <button onClick={handleSubmit} disabled={isPending}>        Update      </button>      {error && <p>{error}</p>}    </div>  );}
```

/$

In React 19, we’re adding support for using async functions in transitions to handle pending states, errors, forms, and optimistic updates automatically.

For example, you can use `useTransition` to handle the pending state for you:

 $

```
// Using pending state from Actionsfunction UpdateName({}) {  const [name, setName] = useState("");  const [error, setError] = useState(null);  const [isPending, startTransition] = useTransition();  const handleSubmit = () => {    startTransition(async () => {      const error = await updateName(name);      if (error) {        setError(error);        return;      }       redirect("/path");    })  };  return (    <div>      <input value={name} onChange={(event) => setName(event.target.value)} />      <button onClick={handleSubmit} disabled={isPending}>        Update      </button>      {error && <p>{error}</p>}    </div>  );}
```

/$

The async transition will immediately set the `isPending` state to true, make the async request(s), and switch `isPending` to false after any transitions. This allows you to keep the current UI responsive and interactive while the data is changing.

### Note

#### By convention, functions that use async transitions are called “Actions”.

Actions automatically manage submitting data for you:

- **Pending state**: Actions provide a pending state that starts at the beginning of a request and automatically resets when the final state update is committed.
- **Optimistic updates**: Actions support the new [useOptimistic](#new-hook-optimistic-updates) hook so you can show users instant feedback while the requests are submitting.
- **Error handling**: Actions provide error handling so you can display Error Boundaries when a request fails, and revert optimistic updates to their original value automatically.
- **Forms**: `<form>` elements now support passing functions to the `action` and `formAction` props. Passing functions to the `action` props use Actions by default and reset the form automatically after submission.

Building on top of Actions, React 19 introduces [useOptimistic](#new-hook-optimistic-updates) to manage optimistic updates, and a new hook [React.useActionState](#new-hook-useactionstate) to handle common cases for Actions. In `react-dom` we’re adding [<form>Actions](#form-actions) to manage forms automatically and [useFormStatus](#new-hook-useformstatus) to support the common cases for Actions in forms.

In React 19, the above example can be simplified to:

 $

```
// Using <form> Actions and useActionStatefunction ChangeName({ name, setName }) {  const [error, submitAction, isPending] = useActionState(    async (previousState, formData) => {      const error = await updateName(formData.get("name"));      if (error) {        return error;      }      redirect("/path");      return null;    },    null,  );  return (    <form action={submitAction}>      <input type="text" name="name" />      <button type="submit" disabled={isPending}>Update</button>      {error && <p>{error}</p>}    </form>  );}
```

/$

In the next section, we’ll break down each of the new Action features in React 19.

### New hook:useActionState

To make the common cases easier for Actions, we’ve added a new hook called `useActionState`:

 $

```
const [error, submitAction, isPending] = useActionState(  async (previousState, newName) => {    const error = await updateName(newName);    if (error) {      // You can return any result of the action.      // Here, we return only the error.      return error;    }    // handle success    return null;  },  null,);
```

/$

`useActionState` accepts a function (the “Action”), and returns a wrapped Action to call. This works because Actions compose. When the wrapped Action is called, `useActionState` will return the last result of the Action as `data`, and the pending state of the Action as `pending`.

### Note

`React.useActionState` was previously called `ReactDOM.useFormState` in the Canary releases, but we’ve renamed it and deprecated `useFormState`.

See [#28491](https://github.com/facebook/react/pull/28491) for more info.

For more information, see the docs for [useActionState](https://react.dev/reference/react/useActionState).

### React DOM:<form>Actions

Actions are also integrated with React 19’s new `<form>` features for `react-dom`. We’ve added support for passing functions as the `action` and `formAction` props of `<form>`, `<input>`, and `<button>` elements to automatically submit forms with Actions:

 $

```
<form action={actionFunction}>
```

/$

When a `<form>` Action succeeds, React will automatically reset the form for uncontrolled components. If you need to reset the `<form>` manually, you can call the new `requestFormReset` React DOM API.

For more information, see the `react-dom` docs for [<form>](https://react.dev/reference/react-dom/components/form), [<input>](https://react.dev/reference/react-dom/components/input), and `<button>`.

### React DOM: New hook:useFormStatus

In design systems, it’s common to write design components that need access to information about the `<form>` they’re in, without drilling props down to the component. This can be done via Context, but to make the common case easier, we’ve added a new hook `useFormStatus`:

 $

```
import {useFormStatus} from 'react-dom';function DesignButton() {  const {pending} = useFormStatus();  return <button type="submit" disabled={pending} />}
```

/$

`useFormStatus` reads the status of the parent `<form>` as if the form was a Context provider.

For more information, see the `react-dom` docs for [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus).

### New hook:useOptimistic

Another common UI pattern when performing a data mutation is to show the final state optimistically while the async request is underway. In React 19, we’re adding a new hook called `useOptimistic` to make this easier:

 $

```
function ChangeName({currentName, onUpdateName}) {  const [optimisticName, setOptimisticName] = useOptimistic(currentName);  const submitAction = async formData => {    const newName = formData.get("name");    setOptimisticName(newName);    const updatedName = await updateName(newName);    onUpdateName(updatedName);  };  return (    <form action={submitAction}>      <p>Your name is: {optimisticName}</p>      <p>        <label>Change Name:</label>        <input          type="text"          name="name"          disabled={currentName !== optimisticName}        />      </p>    </form>  );}
```

/$

The `useOptimistic` hook will immediately render the `optimisticName` while the `updateName` request is in progress. When the update finishes or errors, React will automatically switch back to the `currentName` value.

For more information, see the docs for [useOptimistic](https://react.dev/reference/react/useOptimistic).

### New API:use

In React 19 we’re introducing a new API to read resources in render: `use`.

For example, you can read a promise with `use`, and React will Suspend until the promise resolves:

 $

```
import {use} from 'react';function Comments({commentsPromise}) {  // `use` will suspend until the promise resolves.  const comments = use(commentsPromise);  return comments.map(comment => <p key={comment.id}>{comment}</p>);}function Page({commentsPromise}) {  // When `use` suspends in Comments,  // this Suspense boundary will be shown.  return (    <Suspense fallback={<div>Loading...</div>}>      <Comments commentsPromise={commentsPromise} />    </Suspense>  )}
```

/$

### Note

#### usedoes not support promises created in render.

If you try to pass a promise created in render to `use`, React will warn:

ConsoleA component was suspended by an uncached promise. Creating promises inside a Client Component or hook is not yet supported, except via a Suspense-compatible library or framework.

To fix, you need to pass a promise from a Suspense powered library or framework that supports caching for promises. In the future we plan to ship features to make it easier to cache promises in render.

You can also read context with `use`, allowing you to read Context conditionally such as after early returns:

 $

```
import {use} from 'react';import ThemeContext from './ThemeContext'function Heading({children}) {  if (children == null) {    return null;  }    // This would not work with useContext  // because of the early return.  const theme = use(ThemeContext);  return (    <h1 style={{color: theme.color}}>      {children}    </h1>  );}
```

/$

The `use` API can only be called in render, similar to hooks. Unlike hooks, `use` can be called conditionally. In the future we plan to support more ways to consume resources in render with `use`.

For more information, see the docs for [use](https://react.dev/reference/react/use).

## New React DOM Static APIs

We’ve added two new APIs to `react-dom/static` for static site generation:

- [prerender](https://react.dev/reference/react-dom/static/prerender)
- [prerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream)

These new APIs improve on `renderToString` by waiting for data to load for static HTML generation. They are designed to work with streaming environments like Node.js Streams and Web Streams. For example, in a Web Stream environment, you can prerender a React tree to static HTML with `prerender`:

 $

```
import { prerender } from 'react-dom/static';async function handler(request) {  const {prelude} = await prerender(<App />, {    bootstrapScripts: ['/main.js']  });  return new Response(prelude, {    headers: { 'content-type': 'text/html' },  });}
```

/$

Prerender APIs will wait for all data to load before returning the static HTML stream. Streams can be converted to strings, or sent with a streaming response. They do not support streaming content as it loads, which is supported by the existing [React DOM server rendering APIs](https://react.dev/reference/react-dom/server).

For more information, see [React DOM Static APIs](https://react.dev/reference/react-dom/static).

## React Server Components

### Server Components

Server Components are a new option that allows rendering components ahead of time, before bundling, in an environment separate from your client application or SSR server. This separate environment is the “server” in React Server Components. Server Components can run once at build time on your CI server, or they can be run for each request using a web server.

React 19 includes all of the React Server Components features included from the Canary channel. This means libraries that ship with Server Components can now target React 19 as a peer dependency with a `react-server` [export condition](https://github.com/reactjs/rfcs/blob/main/text/0227-server-module-conventions.md#react-server-conditional-exports) for use in frameworks that support the [Full-stack React Architecture](https://react.dev/learn/creating-a-react-app#which-features-make-up-the-react-teams-full-stack-architecture-vision).

### Note

#### How do I build support for Server Components?

While React Server Components in React 19 are stable and will not break between minor versions, the underlying APIs used to implement a React Server Components bundler or framework do not follow semver and may break between minors in React 19.x.

To support React Server Components as a bundler or framework, we recommend pinning to a specific React version, or using the Canary release. We will continue working with bundlers and frameworks to stabilize the APIs used to implement React Server Components in the future.

For more, see the docs for [React Server Components](https://react.dev/reference/rsc/server-components).

### Server Actions

Server Actions allow Client Components to call async functions executed on the server.

When a Server Action is defined with the `"use server"` directive, your framework will automatically create a reference to the server function, and pass that reference to the Client Component. When that function is called on the client, React will send a request to the server to execute the function, and return the result.

### Note

#### There is no directive for Server Components.

A common misunderstanding is that Server Components are denoted by `"use server"`, but there is no directive for Server Components. The `"use server"` directive is used for Server Actions.

For more info, see the docs for [Directives](https://react.dev/reference/rsc/directives).

Server Actions can be created in Server Components and passed as props to Client Components, or they can be imported and used in Client Components.

For more, see the docs for [React Server Actions](https://react.dev/reference/rsc/server-actions).

## Improvements in React 19

### refas a prop

Starting in React 19, you can now access `ref` as a prop for function components:

 $

```
function MyInput({placeholder, ref}) {  return <input placeholder={placeholder} ref={ref} />}//...<MyInput ref={ref} />
```

/$

New function components will no longer need `forwardRef`, and we will be publishing a codemod to automatically update your components to use the new `ref` prop. In future versions we will deprecate and remove `forwardRef`.

### Note

`ref`s passed to classes are not passed as props since they reference the component instance.

### Diffs for hydration errors

We also improved error reporting for hydration errors in `react-dom`. For example, instead of logging multiple errors in DEV without any information about the mismatch:

 ConsoleWarning: Text content did not match. Server: “Server” Client: “Client”
   at span
   at AppWarning: An error occurred during hydration. The server HTML was replaced with client content in <div>.Warning: Text content did not match. Server: “Server” Client: “Client”
   at span
   at AppWarning: An error occurred during hydration. The server HTML was replaced with client content in <div>.Uncaught Error: Text content does not match server-rendered HTML.
   at checkForUnmatchedText
   …

We now log a single message with a diff of the mismatch:

 ConsoleUncaught Error: Hydration failed because the server rendered HTML didn’t match the client. As a result this tree will be regenerated on the client. This can happen if an SSR-ed Client Component used:
- A server/client branch `if (typeof window !== 'undefined')`.
- Variable input such as `Date.now()` or `Math.random()` which changes each time it’s called.
- Date formatting in a user’s locale which doesn’t match the server.
- External changing data without sending a snapshot of it along with the HTML.
- Invalid HTML tag nesting.
It can also happen if the client has a browser extension installed which messes with the HTML before React loaded.    [https://react.dev/link/hydration-mismatch](https://react.dev/link/hydration-mismatch)        <App>
   <span>
 +     Client
 -     Server       at throwOnHydrationMismatch
   …

### <Context>as a provider

In React 19, you can render `<Context>` as a provider instead of `<Context.Provider>`:

 $

```
const ThemeContext = createContext('');function App({children}) {  return (    <ThemeContext value="dark">      {children}    </ThemeContext>  );  }
```

/$

New Context providers can use `<Context>` and we will be publishing a codemod to convert existing providers. In future versions we will deprecate `<Context.Provider>`.

### Cleanup functions for refs

We now support returning a cleanup function from `ref` callbacks:

 $

```
<input  ref={(ref) => {    // ref created    // NEW: return a cleanup function to reset    // the ref when element is removed from DOM.    return () => {      // ref cleanup    };  }}/>
```

/$

When the component unmounts, React will call the cleanup function returned from the `ref` callback. This works for DOM refs, refs to class components, and `useImperativeHandle`.

### Note

Previously, React would call `ref` functions with `null` when unmounting the component. If your `ref` returns a cleanup function, React will now skip this step.

In future versions, we will deprecate calling refs with `null` when unmounting components.

Due to the introduction of ref cleanup functions, returning anything else from a `ref` callback will now be rejected by TypeScript. The fix is usually to stop using implicit returns, for example:

 $

```
- <div ref={current => (instance = current)} />+ <div ref={current => {instance = current}} />
```

/$

The original code returned the instance of the `HTMLDivElement` and TypeScript wouldn’t know if this was *supposed* to be a cleanup function or if you didn’t want to return a cleanup function.

You can codemod this pattern with [no-implicit-ref-callback-return](https://github.com/eps1lon/types-react-codemod/#no-implicit-ref-callback-return).

### useDeferredValueinitial value

We’ve added an `initialValue` option to `useDeferredValue`:

 $

```
function Search({deferredValue}) {  // On initial render the value is ''.  // Then a re-render is scheduled with the deferredValue.  const value = useDeferredValue(deferredValue, '');    return (    <Results query={value} />  );}
```

/$

When initialValue is provided, `useDeferredValue` will return it as `value` for the initial render of the component, and schedules a re-render in the background with the deferredValue returned.

For more, see [useDeferredValue](https://react.dev/reference/react/useDeferredValue).

### Support for Document Metadata

In HTML, document metadata tags like `<title>`, `<link>`, and `<meta>` are reserved for placement in the `<head>` section of the document. In React, the component that decides what metadata is appropriate for the app may be very far from the place where you render the `<head>` or React does not render the `<head>` at all. In the past, these elements would need to be inserted manually in an effect, or by libraries like [react-helmet](https://github.com/nfl/react-helmet), and required careful handling when server rendering a React application.

In React 19, we’re adding support for rendering document metadata tags in components natively:

 $

```
function BlogPost({post}) {  return (    <article>      <h1>{post.title}</h1>      <title>{post.title}</title>      <meta name="author" content="Josh" />      <link rel="author" href="https://twitter.com/joshcstory/" />      <meta name="keywords" content={post.keywords} />      <p>        Eee equals em-see-squared...      </p>    </article>  );}
```

/$

When React renders this component, it will see the `<title>` `<link>` and `<meta>` tags, and automatically hoist them to the `<head>` section of document. By supporting these metadata tags natively, we’re able to ensure they work with client-only apps, streaming SSR, and Server Components.

### Note

#### You may still want a Metadata library

For simple use cases, rendering Document Metadata as tags may be suitable, but libraries can offer more powerful features like overriding generic metadata with specific metadata based on the current route. These features make it easier for frameworks and libraries like [react-helmet](https://github.com/nfl/react-helmet) to support metadata tags, rather than replace them.

For more info, see the docs for [<title>](https://react.dev/reference/react-dom/components/title), [<link>](https://react.dev/reference/react-dom/components/link), and [<meta>](https://react.dev/reference/react-dom/components/meta).

### Support for stylesheets

Stylesheets, both externally linked (`<link rel="stylesheet" href="...">`) and inline (`<style>...</style>`), require careful positioning in the DOM due to style precedence rules. Building a stylesheet capability that allows for composability within components is hard, so users often end up either loading all of their styles far from the components that may depend on them, or they use a style library which encapsulates this complexity.

In React 19, we’re addressing this complexity and providing even deeper integration into Concurrent Rendering on the Client and Streaming Rendering on the Server with built in support for stylesheets. If you tell React the `precedence` of your stylesheet it will manage the insertion order of the stylesheet in the DOM and ensure that the stylesheet (if external) is loaded before revealing content that depends on those style rules.

 $

```
function ComponentOne() {  return (    <Suspense fallback="loading...">      <link rel="stylesheet" href="foo" precedence="default" />      <link rel="stylesheet" href="bar" precedence="high" />      <article class="foo-class bar-class">        {...}      </article>    </Suspense>  )}function ComponentTwo() {  return (    <div>      <p>{...}</p>      <link rel="stylesheet" href="baz" precedence="default" />  <-- will be inserted between foo & bar    </div>  )}
```

/$

During Server Side Rendering React will include the stylesheet in the `<head>`, which ensures that the browser will not paint until it has loaded. If the stylesheet is discovered late after we’ve already started streaming, React will ensure that the stylesheet is inserted into the `<head>` on the client before revealing the content of a Suspense boundary that depends on that stylesheet.

During Client Side Rendering React will wait for newly rendered stylesheets to load before committing the render. If you render this component from multiple places within your application React will only include the stylesheet once in the document:

 $

```
function App() {  return <>    <ComponentOne />    ...    <ComponentOne /> // won't lead to a duplicate stylesheet link in the DOM  </>}
```

/$

For users accustomed to loading stylesheets manually this is an opportunity to locate those stylesheets alongside the components that depend on them allowing for better local reasoning and an easier time ensuring you only load the stylesheets that you actually depend on.

Style libraries and style integrations with bundlers can also adopt this new capability so even if you don’t directly render your own stylesheets, you can still benefit as your tools are upgraded to use this feature.

For more details, read the docs for [<link>](https://react.dev/reference/react-dom/components/link) and [<style>](https://react.dev/reference/react-dom/components/style).

### Support for async scripts

In HTML normal scripts (`<script src="...">`) and deferred scripts (`<script defer="" src="...">`) load in document order which makes rendering these kinds of scripts deep within your component tree challenging. Async scripts (`<script async="" src="...">`) however will load in arbitrary order.

In React 19 we’ve included better support for async scripts by allowing you to render them anywhere in your component tree, inside the components that actually depend on the script, without having to manage relocating and deduplicating script instances.

 $

```
function MyComponent() {  return (    <div>      <script async={true} src="..." />      Hello World    </div>  )}function App() {  <html>    <body>      <MyComponent>      ...      <MyComponent> // won't lead to duplicate script in the DOM    </body>  </html>}
```

/$

In all rendering environments, async scripts will be deduplicated so that React will only load and execute the script once even if it is rendered by multiple different components.

In Server Side Rendering, async scripts will be included in the `<head>` and prioritized behind more critical resources that block paint such as stylesheets, fonts, and image preloads.

For more details, read the docs for [<script>](https://react.dev/reference/react-dom/components/script).

### Support for preloading resources

During initial document load and on client side updates, telling the Browser about resources that it will likely need to load as early as possible can have a dramatic effect on page performance.

React 19 includes a number of new APIs for loading and preloading Browser resources to make it as easy as possible to build great experiences that aren’t held back by inefficient resource loading.

 $

```
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom'function MyComponent() {  preinit('https://.../path/to/some/script.js', {as: 'script' }) // loads and executes this script eagerly  preload('https://.../path/to/font.woff', { as: 'font' }) // preloads this font  preload('https://.../path/to/stylesheet.css', { as: 'style' }) // preloads this stylesheet  prefetchDNS('https://...') // when you may not actually request anything from this host  preconnect('https://...') // when you will request something but aren't sure what}
```

/$ $

```
<html>  <head>        <link rel="prefetch-dns" href="https://...">    <link rel="preconnect" href="https://...">    <link rel="preload" as="font" href="https://.../path/to/font.woff">    <link rel="preload" as="style" href="https://.../path/to/stylesheet.css">    <script async="" src="https://.../path/to/some/script.js"></script>  </head>  <body>    ...  </body></html>
```

/$

These APIs can be used to optimize initial page loads by moving discovery of additional resources like fonts out of stylesheet loading. They can also make client updates faster by prefetching a list of resources used by an anticipated navigation and then eagerly preloading those resources on click or even on hover.

For more details see [Resource Preloading APIs](https://react.dev/reference/react-dom#resource-preloading-apis).

### Compatibility with third-party scripts and extensions

We’ve improved hydration to account for third-party scripts and browser extensions.

When hydrating, if an element that renders on the client doesn’t match the element found in the HTML from the server, React will force a client re-render to fix up the content. Previously, if an element was inserted by third-party scripts or browser extensions, it would trigger a mismatch error and client render.

In React 19, unexpected tags in the `<head>` and `<body>` will be skipped over, avoiding the mismatch errors. If React needs to re-render the entire document due to an unrelated hydration mismatch, it will leave in place stylesheets inserted by third-party scripts and browser extensions.

### Better error reporting

We improved error handling in React 19 to remove duplication and provide options for handling caught and uncaught errors. For example, when there’s an error in render caught by an Error Boundary, previously React would throw the error twice (once for the original error, then again after failing to automatically recover), and then call `console.error` with info about where the error occurred.

This resulted in three errors for every caught error:

 ConsoleUncaught Error: hit
   at Throws
   at renderWithHooks
   …Uncaught Error: hit    <--  Duplicate    at Throws
   at renderWithHooks
   …The above error occurred in the Throws component:
   at Throws
   at ErrorBoundary
   at App
React will try to recreate this component tree from scratch using the error boundary you provided, ErrorBoundary.

In React 19, we log a single error with all the error information included:

 ConsoleError: hit
   at Throws
   at renderWithHooks
   …
The above error occurred in the Throws component:
   at Throws
   at ErrorBoundary
   at App
React will try to recreate this component tree from scratch using the error boundary you provided, ErrorBoundary.
   at ErrorBoundary
   at App

Additionally, we’ve added two new root options to complement `onRecoverableError`:

- `onCaughtError`: called when React catches an error in an Error Boundary.
- `onUncaughtError`: called when an error is thrown and not caught by an Error Boundary.
- `onRecoverableError`: called when an error is thrown and automatically recovered.

For more info and examples, see the docs for [createRoot](https://react.dev/reference/react-dom/client/createRoot) and [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot).

### Support for Custom Elements

React 19 adds full support for custom elements and passes all tests on [Custom Elements Everywhere](https://custom-elements-everywhere.com/).

In past versions, using Custom Elements in React has been difficult because React treated unrecognized props as attributes rather than properties. In React 19, we’ve added support for properties that works on the client and during SSR with the following strategy:

- **Server Side Rendering**: props passed to a custom element will render as attributes if their type is a primitive value like `string`, `number`, or the value is `true`. Props with non-primitive types like `object`, `symbol`, `function`, or value `false` will be omitted.
- **Client Side Rendering**: props that match a property on the Custom Element instance will be assigned as properties, otherwise they will be assigned as attributes.

Thanks to [Joey Arhar](https://github.com/josepharhar) for driving the design and implementation of Custom Element support in React.

#### How to upgrade

See the [React 19 Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) for step-by-step instructions and a full list of breaking and notable changes.

*Note: this post was originally published 04/25/2024 and has been updated to 12/05/2024 with the stable release.*

[PreviousSunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app)[NextReact Compiler Beta Release and Roadmap](https://react.dev/blog/2024/10/21/react-compiler-beta-release)

---

# React Conf 2024 Recap

[Blog](https://react.dev/blog)

# React Conf 2024 Recap

May 22, 2024 by [Ricky Hanlon](https://twitter.com/rickhanlonii).

---

Last week we hosted React Conf 2024, a two-day conference in Henderson, Nevada where 700+ attendees gathered in-person to discuss the latest in UI engineering. This was our first in-person conference since 2019, and we were thrilled to be able to bring the community together again.

---

At React Conf 2024, we announced the [React 19 RC](https://react.dev/blog/2024/12/05/react-19), the [React Native New Architecture Beta](https://github.com/reactwg/react-native-new-architecture/discussions/189), and an experimental release of the [React Compiler](https://react.dev/learn/react-compiler). The community also took the stage to announce [React Router v7](https://remix.run/blog/merging-remix-and-react-router), [Universal Server Components](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=20765s) in Expo Router, React Server Components in [RedwoodJS](https://redwoodjs.com/blog/rsc-now-in-redwoodjs), and much more.

The entire [day 1](https://www.youtube.com/watch?v=T8TZQ6k4SLE) and [day 2](https://www.youtube.com/watch?v=0ckOUBiuxVY) streams are available online. In this post, we’ll summarize the talks and announcements from the event.

## Day 1

*Watch the full day 1 stream here.*

To kick off day 1, Meta CTO [Andrew “Boz” Bosworth](https://www.threads.net/@boztank) shared a welcome message followed by an introduction by [Seth Webster](https://twitter.com/sethwebster), who manages the React Org at Meta, and our MC [Ashley Narcisse](https://twitter.com/_darkfadr).

In the day 1 keynote, [Joe Savona](https://twitter.com/en_JS) shared our goals and vision for React to make it easy for anyone to build great user experiences. [Lauren Tan](https://twitter.com/potetotes) followed with a State of React, where she shared that React was downloaded over 1 billion times in 2023, and that 37% of new developers learn to program with React. Finally, she highlighted the work of the React community to make React, React.

For more, check out these talks from the community later in the conference:

- [Vanilla React](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=5542s) by [Ryan Florence](https://twitter.com/ryanflorence)
- [React Rhythm & Blues](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=12728s) by [Lee Robinson](https://twitter.com/leeerob)
- [RedwoodJS, now with React Server Components](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=26815s) by [Amy Dutton](https://twitter.com/selfteachme)
- [Introducing Universal React Server Components in Expo Router](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=20765s) by [Evan Bacon](https://twitter.com/Baconbrix)

Next in the keynote, [Josh Story](https://twitter.com/joshcstory) and [Andrew Clark](https://twitter.com/acdlite) shared new features coming in React 19, and announced the React 19 RC which is ready for testing in production. Check out all the features in the [React 19 release post](https://react.dev/blog/2024/12/05/react-19), and see these talks for deep dives on the new features:

- [What’s new in React 19](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=8880s) by [Lydia Hallie](https://twitter.com/lydiahallie)
- [React Unpacked: A Roadmap to React 19](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=10112s) by [Sam Selikoff](https://twitter.com/samselikoff)
- [React 19 Deep Dive: Coordinating HTML](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=24916s) by [Josh Story](https://twitter.com/joshcstory)
- [Enhancing Forms with React Server Components](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=25280s) by [Aurora Walberg Scharff](https://twitter.com/aurorascharff)
- [React for Two Computers](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=18825s) by [Dan Abramov](https://bsky.app/profile/danabra.mov)
- [And Now You Understand React Server Components](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=11256s) by [Kent C. Dodds](https://twitter.com/kentcdodds)

Finally, we ended the keynote with [Joe Savona](https://twitter.com/en_JS), [Sathya Gunasekaran](https://twitter.com/_gsathya), and [Mofei Zhang](https://twitter.com/zmofei) announcing that the React Compiler is now [Open Source](https://github.com/facebook/react/pull/29061), and sharing an experimental version of the React Compiler to try out.

For more information on using the Compiler and how it works, check out [the docs](https://react.dev/learn/react-compiler) and these talks:

- [Forget About Memo](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=12020s) by [Lauren Tan](https://twitter.com/potetotes)
- [React Compiler Deep Dive](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=9313s) by [Sathya Gunasekaran](https://twitter.com/_gsathya) and [Mofei Zhang](https://twitter.com/zmofei)

Watch the full day 1 keynote here:

## Day 2

*Watch the full day 2 stream here.*

To kick off day 2, [Seth Webster](https://twitter.com/sethwebster) shared a welcome message, followed by a Thank You from [Eli White](https://x.com/Eli_White) and an introduction by our Chief Vibes Officer [Ashley Narcisse](https://twitter.com/_darkfadr).

In the day 2 keynote, [Nicola Corti](https://twitter.com/cortinico) shared the State of React Native, including 78 million downloads in 2023. He also highlighted apps using React Native including 2000+ screens used inside of Meta; the product details page in Facebook Marketplace, which is visited more than 2 billion times per day; and part of the Microsoft Windows Start Menu and some features in almost every Microsoft Office product across mobile and desktop.

Nicola also highlighted all the work the community does to support React Native including libraries, frameworks, and multiple platforms. For more, check out these talks from the community:

- [Extending React Native beyond Mobile and Desktop Apps](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=5798s) by [Chris Traganos](https://twitter.com/chris_trag) and [Anisha Malde](https://twitter.com/anisha_malde)
- [Spatial computing with React](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=22525s) by [Michał Pierzchała](https://twitter.com/thymikee)

[Riccardo Cipolleschi](https://twitter.com/cipolleschir) continued the day 2 keynote by announcing that the React Native New Architecture is now in Beta and ready for apps to adopt in production. He shared new features and improvements in the new architecture, and shared the roadmap for the future of React Native. For more check out:

- [Cross Platform React](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=26569s) by [Olga Zinoveva](https://github.com/SlyCaptainFlint) and [Naman Goel](https://twitter.com/naman34)

Next in the keynote, Nicola announced that we are now recommending starting with a framework like Expo for all new apps created with React Native. With the change, he also announced a new React Native homepage and new Getting Started docs. You can view the new Getting Started guide in the [React Native docs](https://reactnative.dev/docs/next/environment-setup).

Finally, to end the keynote, [Kadi Kraman](https://twitter.com/kadikraman) shared the latest features and improvements in Expo, and how to get started developing with React Native using Expo.

Watch the full day 2 keynote here:

## Q&A

The React and React Native teams also ended each day with a Q&A session:

- [React Q&A](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=27518s) hosted by [Michael Chan](https://twitter.com/chantastic)
- [React Native Q&A](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=27935s) hosted by [Jamon Holmgren](https://twitter.com/jamonholmgren)

## And more…

We also heard talks on accessibility, error reporting, css, and more:

- [Demystifying accessibility in React apps](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=20655s) by [Kateryna Porshnieva](https://twitter.com/krambertech)
- [Pigment CSS, CSS in the server component age](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=21696s) by [Olivier Tassinari](https://twitter.com/olivtassinari)
- [Real-time React Server Components](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=24070s) by [Sunil Pai](https://twitter.com/threepointone)
- [Let’s break React Rules](https://www.youtube.com/watch?v=T8TZQ6k4SLE&t=25862s) by [Charlotte Isambert](https://twitter.com/c_isambert)
- [Solve 100% of your errors](https://www.youtube.com/watch?v=0ckOUBiuxVY&t=19881s) by [Ryan Albrecht](https://github.com/ryan953)

## Thank you

Thank you to all the staff, speakers, and participants who made React Conf 2024 possible. There are too many to list, but we want to thank a few in particular.

Thank you to [Barbara Markiewicz](https://twitter.com/barbara_markie), the team at [Callstack](https://www.callstack.com/), and our React Team Developer Advocate [Matt Carroll](https://twitter.com/mattcarrollcode) for helping to plan the entire event; and to [Sunny Leggett](https://zeroslopeevents.com/about) and everyone from [Zero Slope](https://zeroslopeevents.com) for helping to organize the event.

Thank you [Ashley Narcisse](https://twitter.com/_darkfadr) for being our MC and Chief Vibes Officer; and to [Michael Chan](https://twitter.com/chantastic) and [Jamon Holmgren](https://twitter.com/jamonholmgren) for hosting the Q&A sessions.

Thank you [Seth Webster](https://twitter.com/sethwebster) and [Eli White](https://x.com/Eli_White) for welcoming us each day and providing direction on structure and content; and to [Tom Occhino](https://twitter.com/tomocchino) for joining us with a special message during the after-party.

Thank you [Ricky Hanlon](https://www.youtube.com/watch?v=FxTZL2U-uKg&t=1263s) for providing detailed feedback on talks, working on slide designs, and generally filling in the gaps to sweat the details.

Thank you [Callstack](https://www.callstack.com/) for building the conference website; and to [Kadi Kraman](https://twitter.com/kadikraman) and the [Expo](https://expo.dev/) team for building the conference mobile app.

Thank you to all the sponsors who made the event possible: [Remix](https://remix.run/), [Amazon](https://developer.amazon.com/apps-and-games?cmp=US_2024_05_3P_React-Conf-2024&ch=prtnr&chlast=prtnr&pub=ref&publast=ref&type=org&typelast=org), [MUI](https://mui.com/), [Sentry](https://sentry.io/for/react/?utm_source=sponsored-conf&utm_medium=sponsored-event&utm_campaign=frontend-fy25q2-evergreen&utm_content=logo-reactconf2024-learnmore), [Abbott](https://www.jobs.abbott/software), [Expo](https://expo.dev/), [RedwoodJS](https://rwsdk.com/), and [Vercel](https://vercel.com).

Thank you to the AV Team for the visuals, stage, and sound; and to the Westin Hotel for hosting us.

Thank you to all the speakers who shared their knowledge and experiences with the community.

Finally, thank you to everyone who attended in person and online to show what makes React, React. React is more than a library, it is a community, and it was inspiring to see everyone come together to share and learn together.

See you next time!

[PreviousReact Compiler Beta Release and Roadmap](https://react.dev/blog/2024/10/21/react-compiler-beta-release)[NextReact 19 RC](https://react.dev/blog/2024/04/25/react-19)
