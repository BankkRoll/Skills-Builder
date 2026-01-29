# React Compiler Beta Release and more

# React Compiler Beta Release

[Blog](https://react.dev/blog)

# React Compiler Beta Release

October 21, 2024 by [Lauren Tan](https://twitter.com/potetotes).

---

### Note

### React Compiler is now stable!

Please see the [stable release blog post](https://react.dev/blog/2025/10/07/react-compiler-1) for details.

The React team is excited to share new updates:

1. We’re publishing React Compiler Beta today, so that early adopters and library maintainers can try it and provide feedback.
2. We’re officially supporting React Compiler for apps on React 17+, through an optional `react-compiler-runtime` package.
3. We’re opening up public membership of the [React Compiler Working Group](https://github.com/reactwg/react-compiler) to prepare the community for gradual adoption of the compiler.

---

At [React Conf 2024](https://react.dev/blog/2024/05/22/react-conf-2024-recap), we announced the experimental release of React Compiler, a build-time tool that optimizes your React app through automatic memoization. [You can find an introduction to React Compiler here](https://react.dev/learn/react-compiler).

Since the first release, we’ve fixed numerous bugs reported by the React community, received several high quality bug fixes and contributions[1](#user-content-fn-1) to the compiler, made the compiler more resilient to the broad diversity of JavaScript patterns, and have continued to roll out the compiler more widely at Meta.

In this post, we want to share what’s next for React Compiler.

## Try React Compiler Beta today

At [React India 2024](https://www.youtube.com/watch?v=qd5yk2gxbtg), we shared an update on React Compiler. Today, we are excited to announce a new Beta release of React Compiler and ESLint plugin. New betas are published to npm using the `@beta` tag.

To install React Compiler Beta:

  Terminal

```
npm install -D babel-plugin-react-compiler@beta eslint-plugin-react-compiler@beta
```

Or, if you’re using Yarn:

  Terminal

```
yarn add -D babel-plugin-react-compiler@beta eslint-plugin-react-compiler@beta
```

You can watch [Sathya Gunasekaran’s](https://twitter.com/_gsathya) talk at React India here:

## We recommend everyone use the React Compiler linter today

React Compiler’s ESLint plugin helps developers proactively identify and correct [Rules of React](https://react.dev/reference/rules) violations. **We strongly recommend everyone use the linter today**. The linter does not require that you have the compiler installed, so you can use it independently, even if you are not ready to try out the compiler.

To install the linter only:

  Terminal

```
npm install -D eslint-plugin-react-compiler@beta
```

Or, if you’re using Yarn:

  Terminal

```
yarn add -D eslint-plugin-react-compiler@beta
```

After installation you can enable the linter by [adding it to your ESLint config](https://react.dev/learn/react-compiler/installation#eslint-integration). Using the linter helps identify Rules of React breakages, making it easier to adopt the compiler when it’s fully released.

## Backwards Compatibility

React Compiler produces code that depends on runtime APIs added in React 19, but we’ve since added support for the compiler to also work with React 17 and 18. If you are not on React 19 yet, in the Beta release you can now try out React Compiler by specifying a minimum `target` in your compiler config, and adding `react-compiler-runtime` as a dependency. [You can find docs on this here](https://react.dev/reference/react-compiler/configuration#react-17-18).

## Using React Compiler in libraries

Our initial release was focused on identifying major issues with using the compiler in applications. We’ve gotten great feedback and have substantially improved the compiler since then. We’re now ready for broad feedback from the community, and for library authors to try out the compiler to improve performance and the developer experience of maintaining your library.

React Compiler can also be used to compile libraries. Because React Compiler needs to run on the original source code prior to any code transformations, it is not possible for an application’s build pipeline to compile the libraries they use. Hence, our recommendation is for library maintainers to independently compile and test their libraries with the compiler, and ship compiled code to npm.

Because your code is pre-compiled, users of your library will not need to have the compiler enabled in order to benefit from the automatic memoization applied to your library. If your library targets apps not yet on React 19, specify a minimum `target` and add `react-compiler-runtime` as a direct dependency. The runtime package will use the correct implementation of APIs depending on the application’s version, and polyfill the missing APIs if necessary.

[You can find more docs on this here.](https://react.dev/reference/react-compiler/compiling-libraries)

## Opening up React Compiler Working Group to everyone

We previously announced the invite-only [React Compiler Working Group](https://github.com/reactwg/react-compiler) at React Conf to provide feedback, ask questions, and collaborate on the compiler’s experimental release.

From today, together with the Beta release of React Compiler, we are opening up Working Group membership to everyone. The goal of the React Compiler Working Group is to prepare the ecosystem for a smooth, gradual adoption of React Compiler by existing applications and libraries. Please continue to file bug reports in the [React repo](https://github.com/facebook/react), but please leave feedback, ask questions, or share ideas in the [Working Group discussion forum](https://github.com/reactwg/react-compiler/discussions).

The core team will also use the discussions repo to share our research findings. As the Stable Release gets closer, any important information will also be posted on this forum.

## React Compiler at Meta

At [React Conf](https://react.dev/blog/2024/05/22/react-conf-2024-recap), we shared that our rollout of the compiler on Quest Store and Instagram were successful. Since then, we’ve deployed React Compiler across several more major web apps at Meta, including [Facebook](https://www.facebook.com) and [Threads](https://www.threads.net). That means if you’ve used any of these apps recently, you may have had your experience powered by the compiler. We were able to onboard these apps onto the compiler with few code changes required, in a monorepo with more than 100,000 React components.

We’ve seen notable performance improvements across all of these apps. As we’ve rolled out, we’re continuing to see results on the order of [the wins we shared previously at ReactConf](https://youtu.be/lyEKhv8-3n0?t=3223). These apps have already been heavily hand tuned and optimized by Meta engineers and React experts over the years, so even improvements on the order of a few percent are a huge win for us.

We also expected developer productivity wins from React Compiler. To measure this, we collaborated with our data science partners at Meta[2](#user-content-fn-2) to conduct a thorough statistical analysis of the impact of manual memoization on productivity. Before rolling out the compiler at Meta, we discovered that only about 8% of React pull requests used manual memoization and that these pull requests took 31-46% longer to author[3](#user-content-fn-3). This confirmed our intuition that manual memoization introduces cognitive overhead, and we anticipate that React Compiler will lead to more efficient code authoring and review. Notably, React Compiler also ensures that *all* code is memoized by default, not just the (in our case) 8% where developers explicitly apply memoization.

## Roadmap to Stable

*This is not a final roadmap, and is subject to change.*

We intend to ship a Release Candidate of the compiler in the near future following the Beta release, when the majority of apps and libraries that follow the Rules of React have been proven to work well with the compiler. After a period of final feedback from the community, we plan on a Stable Release for the compiler. The Stable Release will mark the beginning of a new foundation for React, and all apps and libraries will be strongly recommended to use the compiler and ESLint plugin.

- ✅ Experimental: Released at React Conf 2024, primarily for feedback from early adopters.
- ✅ Public Beta: Available today, for feedback from the wider community.
- 🚧 Release Candidate (RC): React Compiler works for the majority of rule-following apps and libraries without issue.
- 🚧 General Availability: After final feedback period from the community.

These releases also include the compiler’s ESLint plugin, which surfaces diagnostics statically analyzed by the compiler. We plan to combine the existing eslint-plugin-react-hooks plugin with the compiler’s ESLint plugin, so only one plugin needs to be installed.

Post-Stable, we plan to add more compiler optimizations and improvements. This includes both continual improvements to automatic memoization, and new optimizations altogether, with minimal to no change of product code. Upgrading to each new release of the compiler is aimed to be straightforward, and each upgrade will continue to improve performance and add better handling of diverse JavaScript and React patterns.

Throughout this process, we also plan to prototype an IDE extension for React. It is still very early in research, so we expect to be able to share more of our findings with you in a future React Labs blog post.

---

Thanks to [Sathya Gunasekaran](https://twitter.com/_gsathya), [Joe Savona](https://twitter.com/en_JS), [Ricky Hanlon](https://twitter.com/rickhanlonii), [Alex Taylor](https://github.com/alexmckenley), [Jason Bonta](https://twitter.com/someextent), and [Eli White](https://twitter.com/Eli_White) for reviewing and editing this post.

---

## Footnotes

1. Thanks [@nikeee](https://github.com/facebook/react/pulls?q=is%3Apr+author%3Anikeee), [@henryqdineen](https://github.com/facebook/react/pulls?q=is%3Apr+author%3Ahenryqdineen), [@TrickyPi](https://github.com/facebook/react/pulls?q=is%3Apr+author%3ATrickyPi), and several others for their contributions to the compiler. [↩](#user-content-fnref-1)
2. Thanks [Vaishali Garg](https://www.linkedin.com/in/vaishaligarg09) for leading this study on React Compiler at Meta, and for reviewing this post. [↩](#user-content-fnref-2)
3. After controlling on author tenure, diff length/complexity, and other potential confounding factors. [↩](#user-content-fnref-3)

 [PreviousReact 19](https://react.dev/blog/2024/12/05/react-19)[NextReact Conf 2024 Recap](https://react.dev/blog/2024/05/22/react-conf-2024-recap)

---

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
