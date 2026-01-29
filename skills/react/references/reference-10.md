# use and more

# use

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# use

`use` is a React API that lets you read the value of a resource like a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or [context](https://react.dev/learn/passing-data-deeply-with-context).

$

```
const value = use(resource);
```

/$

- [Reference](#reference)
  - [use(resource)](#use)
- [Usage](#usage)
  - [Reading context withuse](#reading-context-with-use)
  - [Streaming data from the server to the client](#streaming-data-from-server-to-client)
  - [Dealing with rejected Promises](#dealing-with-rejected-promises)
- [Troubleshooting](#troubleshooting)
  - [“Suspense Exception: This is not a real error!”](#suspense-exception-error)

---

## Reference

### use(resource)

Call `use` in your component to read the value of a resource like a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or [context](https://react.dev/learn/passing-data-deeply-with-context).

 $

```
import { use } from 'react';function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...
```

/$

Unlike React Hooks, `use` can be called within loops and conditional statements like `if`. Like React Hooks, the function that calls `use` must be a Component or Hook.

When called with a Promise, the `use` API integrates with [Suspense](https://react.dev/reference/react/Suspense) and [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary). The component calling `use` *suspends* while the Promise passed to `use` is pending. If the component that calls `use` is wrapped in a Suspense boundary, the fallback will be displayed.  Once the Promise is resolved, the Suspense fallback is replaced by the rendered components using the data returned by the `use` API. If the Promise passed to `use` is rejected, the fallback of the nearest Error Boundary will be displayed.

[See more examples below.](#usage)

#### Parameters

- `resource`: this is the source of the data you want to read a value from. A resource can be a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or a [context](https://react.dev/learn/passing-data-deeply-with-context).

#### Returns

The `use` API returns the value that was read from the resource like the resolved value of a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or [context](https://react.dev/learn/passing-data-deeply-with-context).

#### Caveats

- The `use` API must be called inside a Component or a Hook.
- When fetching data in a [Server Component](https://react.dev/reference/rsc/server-components), prefer `async` and `await` over `use`. `async` and `await` pick up rendering from the point where `await` was invoked, whereas `use` re-renders the component after the data is resolved.
- Prefer creating Promises in [Server Components](https://react.dev/reference/rsc/server-components) and passing them to [Client Components](https://react.dev/reference/rsc/use-client) over creating Promises in Client Components. Promises created in Client Components are recreated on every render. Promises passed from a Server Component to a Client Component are stable across re-renders. [See this example](#streaming-data-from-server-to-client).

---

## Usage

### Reading context withuse

When a [context](https://react.dev/learn/passing-data-deeply-with-context) is passed to `use`, it works similarly to [useContext](https://react.dev/reference/react/useContext). While `useContext` must be called at the top level of your component, `use` can be called inside conditionals like `if` and loops like `for`. `use` is preferred over `useContext` because it is more flexible.

 $

```
import { use } from 'react';function Button() {  const theme = use(ThemeContext);  // ...
```

/$

`use` returns the context value for the context you passed. To determine the context value, React searches the component tree and finds **the closest context provider above** for that particular context.

To pass context to a `Button`, wrap it or one of its parent components into the corresponding context provider.

 $

```
function MyPage() {  return (    <ThemeContext value="dark">      <Form />    </ThemeContext>  );}function Form() {  // ... renders buttons inside ...}
```

/$

It doesn’t matter how many layers of components there are between the provider and the `Button`. When a `Button` *anywhere* inside of `Form` calls `use(ThemeContext)`, it will receive `"dark"` as the value.

Unlike [useContext](https://react.dev/reference/react/useContext), `use` can be called in conditionals and loops like `if`.

 $

```
function HorizontalRule({ show }) {  if (show) {    const theme = use(ThemeContext);    return <hr className={theme} />;  }  return false;}
```

/$

`use` is called from inside a `if` statement, allowing you to conditionally read values from a Context.

### Pitfall

Like `useContext`, `use(context)` always looks for the closest context provider *above* the component that calls it. It searches upwards and **does not** consider context providers in the component from which you’re calling `use(context)`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext, use } from 'react';

const ThemeContext = createContext(null);

export default function MyApp() {
  return (
    <ThemeContext value="dark">
      <Form />
    </ThemeContext>
  )
}

function Form() {
  return (
    <Panel title="Welcome">
      <Button show={true}>Sign up</Button>
      <Button show={false}>Log in</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = use(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ show, children }) {
  if (show) {
    const theme = use(ThemeContext);
    const className = 'button-' + theme;
    return (
      <button className={className}>
        {children}
      </button>
    );
  }
  return false
}
```

/$

### Streaming data from the server to the client

Data can be streamed from the server to the client by passing a Promise as a prop from a Server Component to a Client Component.

 $

```
import { fetchMessage } from './lib.js';import { Message } from './message.js';export default function App() {  const messagePromise = fetchMessage();  return (    <Suspense fallback={<p>waiting for message...</p>}>      <Message messagePromise={messagePromise} />    </Suspense>  );}
```

/$

The Client Component then takes the Promise it received as a prop and passes it to the `use` API. This allows the Client Component to read the value from the Promise that was initially created by the Server Component.

 $

```
// message.js'use client';import { use } from 'react';export function Message({ messagePromise }) {  const messageContent = use(messagePromise);  return <p>Here is the message: {messageContent}</p>;}
```

/$

Because `Message` is wrapped in [Suspense](https://react.dev/reference/react/Suspense), the fallback will be displayed until the Promise is resolved. When the Promise is resolved, the value will be read by the `use` API and the `Message` component will replace the Suspense fallback.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
"use client";

import { use, Suspense } from "react";

function Message({ messagePromise }) {
  const messageContent = use(messagePromise);
  return <p>Here is the message: {messageContent}</p>;
}

export function MessageContainer({ messagePromise }) {
  return (
    <Suspense fallback={<p>⌛Downloading message...</p>}>
      <Message messagePromise={messagePromise} />
    </Suspense>
  );
}
```

/$

### Note

When passing a Promise from a Server Component to a Client Component, its resolved value must be serializable to pass between server and client. Data types like functions aren’t serializable and cannot be the resolved value of such a Promise.

##### Deep Dive

#### Should I resolve a Promise in a Server or Client Component?

A Promise can be passed from a Server Component to a Client Component and resolved in the Client Component with the `use` API. You can also resolve the Promise in a Server Component with `await` and pass the required data to the Client Component as a prop.

$

```
export default async function App() {  const messageContent = await fetchMessage();  return <Message messageContent={messageContent} />}
```

/$

But using `await` in a [Server Component](https://react.dev/reference/rsc/server-components) will block its rendering until the `await` statement is finished. Passing a Promise from a Server Component to a Client Component prevents the Promise from blocking the rendering of the Server Component.

### Dealing with rejected Promises

In some cases a Promise passed to `use` could be rejected. You can handle rejected Promises by either:

1. [Displaying an error to users with an Error Boundary.](#displaying-an-error-to-users-with-error-boundary)
2. [Providing an alternative value withPromise.catch](#providing-an-alternative-value-with-promise-catch)

### Pitfall

`use` cannot be called in a try-catch block. Instead of a try-catch block [wrap your component in an Error Boundary](#displaying-an-error-to-users-with-error-boundary), or [provide an alternative value to use with the Promise’s.catchmethod](#providing-an-alternative-value-with-promise-catch).

#### Displaying an error to users with an Error Boundary

If you’d like to display an error to your users when a Promise is rejected, you can use an [Error Boundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary). To use an Error Boundary, wrap the component where you are calling the `use` API in an Error Boundary. If the Promise passed to `use` is rejected the fallback for the Error Boundary will be displayed.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
"use client";

import { use, Suspense } from "react";
import { ErrorBoundary } from "react-error-boundary";

export function MessageContainer({ messagePromise }) {
  return (
    <ErrorBoundary fallback={<p>⚠️Something went wrong</p>}>
      <Suspense fallback={<p>⌛Downloading message...</p>}>
        <Message messagePromise={messagePromise} />
      </Suspense>
    </ErrorBoundary>
  );
}

function Message({ messagePromise }) {
  const content = use(messagePromise);
  return <p>Here is the message: {content}</p>;
}
```

/$

#### Providing an alternative value withPromise.catch

If you’d like to provide an alternative value when the Promise passed to `use` is rejected you can use the Promise’s [catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch) method.

 $

```
import { Message } from './message.js';export default function App() {  const messagePromise = new Promise((resolve, reject) => {    reject();  }).catch(() => {    return "no new message found.";  });  return (    <Suspense fallback={<p>waiting for message...</p>}>      <Message messagePromise={messagePromise} />    </Suspense>  );}
```

/$

To use the Promise’s `catch` method, call `catch` on the Promise object. `catch` takes a single argument: a function that takes an error message as an argument. Whatever is returned by the function passed to `catch` will be used as the resolved value of the Promise.

---

## Troubleshooting

### “Suspense Exception: This is not a real error!”

You are either calling `use` outside of a React Component or Hook function, or calling `use` in a try–catch block. If you are calling `use` inside a try–catch block, wrap your component in an Error Boundary, or call the Promise’s `catch` to catch the error and resolve the Promise with another value. [See these examples](#dealing-with-rejected-promises).

If you are calling `use` outside a React Component or Hook function, move the `use` call to a React Component or Hook function.

 $

```
function MessageComponent({messagePromise}) {  function download() {    // ❌ the function calling `use` is not a Component or Hook    const message = use(messagePromise);    // ...
```

/$

Instead, call `use` outside any component closures, where the function that calls `use` is a Component or Hook.

 $

```
function MessageComponent({messagePromise}) {  // ✅ `use` is being called from a component.   const message = use(messagePromise);  // ...
```

/$[PreviousstartTransition](https://react.dev/reference/react/startTransition)[Nextexperimental_taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference)

---

# useActionState

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useActionState

`useActionState` is a Hook that allows you to update state based on the result of a form action.

$

```
const [state, formAction, isPending] = useActionState(fn, initialState, permalink?);
```

/$

### Note

In earlier React Canary versions, this API was part of React DOM and called `useFormState`.

- [Reference](#reference)
  - [useActionState(action, initialState, permalink?)](#useactionstate)
- [Usage](#usage)
  - [Using information returned by a form action](#using-information-returned-by-a-form-action)
- [Troubleshooting](#troubleshooting)
  - [My action can no longer read the submitted form data](#my-action-can-no-longer-read-the-submitted-form-data)

---

## Reference

### useActionState(action, initialState, permalink?)

Call `useActionState` at the top level of your component to create component state that is updated [when a form action is invoked](https://react.dev/reference/react-dom/components/form). You pass `useActionState` an existing form action function as well as an initial state, and it returns a new action that you use in your form, along with the latest form state and whether the Action is still pending. The latest form state is also passed to the function that you provided.

 $

```
import { useActionState } from "react";async function increment(previousState, formData) {  return previousState + 1;}function StatefulForm({}) {  const [state, formAction] = useActionState(increment, 0);  return (    <form>      {state}      <button formAction={formAction}>Increment</button>    </form>  )}
```

/$

The form state is the value returned by the action when the form was last submitted. If the form has not yet been submitted, it is the initial state that you pass.

If used with a Server Function, `useActionState` allows the server’s response from submitting the form to be shown even before hydration has completed.

[See more examples below.](#usage)

#### Parameters

- `fn`: The function to be called when the form is submitted or button pressed. When the function is called, it will receive the previous state of the form (initially the `initialState` that you pass, subsequently its previous return value) as its initial argument, followed by the arguments that a form action normally receives.
- `initialState`: The value you want the state to be initially. It can be any serializable value. This argument is ignored after the action is first invoked.
- **optional** `permalink`: A string containing the unique page URL that this form modifies. For use on pages with dynamic content (eg: feeds) in conjunction with progressive enhancement: if `fn` is a [server function](https://react.dev/reference/rsc/server-functions) and the form is submitted before the JavaScript bundle loads, the browser will navigate to the specified permalink URL, rather than the current page’s URL. Ensure that the same form component is rendered on the destination page (including the same action `fn` and `permalink`) so that React knows how to pass the state through. Once the form has been hydrated, this parameter has no effect.

#### Returns

`useActionState` returns an array with the following values:

1. The current state. During the first render, it will match the `initialState` you have passed. After the action is invoked, it will match the value returned by the action.
2. A new action that you can pass as the `action` prop to your `form` component or `formAction` prop to any `button` component within the form. The action can also be called manually within [startTransition](https://react.dev/reference/react/startTransition).
3. The `isPending` flag that tells you whether there is a pending Transition.

#### Caveats

- When used with a framework that supports React Server Components, `useActionState` lets you make forms interactive before JavaScript has executed on the client. When used without Server Components, it is equivalent to component local state.
- The function passed to `useActionState` receives an extra argument, the previous or initial state, as its first argument. This makes its signature different than if it were used directly as a form action without using `useActionState`.

---

## Usage

### Using information returned by a form action

Call `useActionState` at the top level of your component to access the return value of an action from the last time a form was submitted.

 $

```
import { useActionState } from 'react';import { action } from './actions.js';function MyComponent() {  const [state, formAction] = useActionState(action, null);  // ...  return (    <form action={formAction}>      {/* ... */}    </form>  );}
```

/$

`useActionState` returns an array with the following items:

1. The current state of the form, which is initially set to the initial state you provided, and after the form is submitted is set to the return value of the action you provided.
2. A new action that you pass to `<form>` as its `action` prop or call manually within `startTransition`.
3. A pending state that you can utilise while your action is processing.

When the form is submitted, the action function that you provided will be called. Its return value will become the new current state of the form.

The action that you provide will also receive a new first argument, namely the current state of the form. The first time the form is submitted, this will be the initial state you provided, while with subsequent submissions, it will be the return value from the last time the action was called. The rest of the arguments are the same as if `useActionState` had not been used.

 $

```
function action(currentState, formData) {  // ...  return 'next state';}
```

/$

#### Display information after submitting a form

#### Example1of2:Display form errors

To display messages such as an error message or toast that’s returned by a Server Function, wrap the action in a call to `useActionState`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useActionState, useState } from "react";
import { addToCart } from "./actions.js";

function AddToCartForm({itemID, itemTitle}) {
  const [message, formAction, isPending] = useActionState(addToCart, null);
  return (
    <form action={formAction}>
      <h2>{itemTitle}</h2>
      <input type="hidden" name="itemID" value={itemID} />
      <button type="submit">Add to Cart</button>
      {isPending ? "Loading..." : message}
    </form>
  );
}

export default function App() {
  return (
    <>
      <AddToCartForm itemID="1" itemTitle="JavaScript: The Definitive Guide" />
      <AddToCartForm itemID="2" itemTitle="JavaScript: The Good Parts" />
    </>
  )
}
```

/$

## Troubleshooting

### My action can no longer read the submitted form data

When you wrap an action with `useActionState`, it gets an extra argument *as its first argument*. The submitted form data is therefore its *second* argument instead of its first as it would usually be. The new first argument that gets added is the current state of the form.

 $

```
function action(currentState, formData) {  // ...}
```

/$[PreviousHooks](https://react.dev/reference/react/hooks)[NextuseCallback](https://react.dev/reference/react/useCallback)

---

# useCallback

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useCallback

`useCallback` is a React Hook that lets you cache a function definition between re-renders.

$

```
const cachedFn = useCallback(fn, dependencies)
```

/$

### Note

[React Compiler](https://react.dev/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useCallback` calls. You can use the compiler to handle memoization automatically.

- [Reference](#reference)
  - [useCallback(fn, dependencies)](#usecallback)
- [Usage](#usage)
  - [Skipping re-rendering of components](#skipping-re-rendering-of-components)
  - [Updating state from a memoized callback](#updating-state-from-a-memoized-callback)
  - [Preventing an Effect from firing too often](#preventing-an-effect-from-firing-too-often)
  - [Optimizing a custom Hook](#optimizing-a-custom-hook)
- [Troubleshooting](#troubleshooting)
  - [Every time my component renders,useCallbackreturns a different function](#every-time-my-component-renders-usecallback-returns-a-different-function)
  - [I need to calluseCallbackfor each list item in a loop, but it’s not allowed](#i-need-to-call-usememo-for-each-list-item-in-a-loop-but-its-not-allowed)

---

## Reference

### useCallback(fn, dependencies)

Call `useCallback` at the top level of your component to cache a function definition between re-renders:

 $

```
import { useCallback } from 'react';export default function ProductPage({ productId, referrer, theme }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]);
```

/$

[See more examples below.](#usage)

#### Parameters

- `fn`: The function value that you want to cache. It can take any arguments and return any values. React will return (not call!) your function back to you during the initial render. On next renders, React will give you the same function again if the `dependencies` have not changed since the last render. Otherwise, it will give you the function that you have passed during the current render, and store it in case it can be reused later. React will not call your function. The function is returned to you so you can decide when and whether to call it.
- `dependencies`: The list of all reactive values referenced inside of the `fn` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](https://react.dev/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison algorithm.

#### Returns

On the initial render, `useCallback` returns the `fn` function you have passed.

During subsequent renders, it will either return an already stored `fn` function from the last render (if the dependencies haven’t changed), or return the `fn` function you have passed during this render.

#### Caveats

- `useCallback` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.
- React **will not throw away the cached function unless there is a specific reason to do that.** For example, in development, React throws away the cache when you edit the file of your component. Both in development and in production, React will throw away the cache if your component suspends during the initial mount. In the future, React may add more features that take advantage of throwing away the cache—for example, if React adds built-in support for virtualized lists in the future, it would make sense to throw away the cache for items that scroll out of the virtualized table viewport. This should match your expectations if you rely on `useCallback` as a performance optimization. Otherwise, a [state variable](https://react.dev/reference/react/useState#im-trying-to-set-state-to-a-function-but-it-gets-called-instead) or a [ref](https://react.dev/reference/react/useRef#avoiding-recreating-the-ref-contents) may be more appropriate.

---

## Usage

### Skipping re-rendering of components

When you optimize rendering performance, you will sometimes need to cache the functions that you pass to child components. Let’s first look at the syntax for how to do this, and then see in which cases it’s useful.

To cache a function between re-renders of your component, wrap its definition into the `useCallback` Hook:

 $

```
import { useCallback } from 'react';function ProductPage({ productId, referrer, theme }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]);  // ...
```

/$

You need to pass two things to `useCallback`:

1. A function definition that you want to cache between re-renders.
2. A list of dependencies including every value within your component that’s used inside your function.

On the initial render, the returned function you’ll get from `useCallback` will be the function you passed.

On the following renders, React will compare the dependencies with the dependencies you passed during the previous render. If none of the dependencies have changed (compared with [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), `useCallback` will return the same function as before. Otherwise, `useCallback` will return the function you passed on *this* render.

In other words, `useCallback` caches a function between re-renders until its dependencies change.

**Let’s walk through an example to see when this is useful.**

Say you’re passing a `handleSubmit` function down from the `ProductPage` to the `ShippingForm` component:

 $

```
function ProductPage({ productId, referrer, theme }) {  // ...  return (    <div className={theme}>      <ShippingForm onSubmit={handleSubmit} />    </div>  );
```

/$

You’ve noticed that toggling the `theme` prop freezes the app for a moment, but if you remove `<ShippingForm />` from your JSX, it feels fast. This tells you that it’s worth trying to optimize the `ShippingForm` component.

**By default, when a component re-renders, React re-renders all of its children recursively.** This is why, when `ProductPage` re-renders with a different `theme`, the `ShippingForm` component *also* re-renders. This is fine for components that don’t require much calculation to re-render. But if you verified a re-render is slow, you can tell `ShippingForm` to skip re-rendering when its props are the same as on last render by wrapping it in [memo:](https://react.dev/reference/react/memo)

 $

```
import { memo } from 'react';const ShippingForm = memo(function ShippingForm({ onSubmit }) {  // ...});
```

/$

**With this change,ShippingFormwill skip re-rendering if all of its props are thesameas on the last render.** This is when caching a function becomes important! Let’s say you defined `handleSubmit` without `useCallback`:

 $

```
function ProductPage({ productId, referrer, theme }) {  // Every time the theme changes, this will be a different function...  function handleSubmit(orderDetails) {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }  return (    <div className={theme}>      {/* ... so ShippingForm's props will never be the same, and it will re-render every time */}      <ShippingForm onSubmit={handleSubmit} />    </div>  );}
```

/$

**In JavaScript, afunction () {}or() => {}always creates adifferentfunction,** similar to how the `{}` object literal always creates a new object. Normally, this wouldn’t be a problem, but it means that `ShippingForm` props will never be the same, and your [memo](https://react.dev/reference/react/memo) optimization won’t work. This is where `useCallback` comes in handy:

 $

```
function ProductPage({ productId, referrer, theme }) {  // Tell React to cache your function between re-renders...  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]); // ...so as long as these dependencies don't change...  return (    <div className={theme}>      {/* ...ShippingForm will receive the same props and can skip re-rendering */}      <ShippingForm onSubmit={handleSubmit} />    </div>  );}
```

/$

**By wrappinghandleSubmitinuseCallback, you ensure that it’s thesamefunction between the re-renders** (until dependencies change). You don’t *have to* wrap a function in `useCallback` unless you do it for some specific reason. In this example, the reason is that you pass it to a component wrapped in [memo,](https://react.dev/reference/react/memo) and this lets it skip re-rendering. There are other reasons you might need `useCallback` which are described further on this page.

### Note

**You should only rely onuseCallbackas a performance optimization.** If your code doesn’t work without it, find the underlying problem and fix it first. Then you may add `useCallback` back.

##### Deep Dive

#### How is useCallback related to useMemo?

You will often see [useMemo](https://react.dev/reference/react/useMemo) alongside `useCallback`. They are both useful when you’re trying to optimize a child component. They let you [memoize](https://en.wikipedia.org/wiki/Memoization) (or, in other words, cache) something you’re passing down:

$

```
import { useMemo, useCallback } from 'react';function ProductPage({ productId, referrer }) {  const product = useData('/product/' + productId);  const requirements = useMemo(() => { // Calls your function and caches its result    return computeRequirements(product);  }, [product]);  const handleSubmit = useCallback((orderDetails) => { // Caches your function itself    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]);  return (    <div className={theme}>      <ShippingForm requirements={requirements} onSubmit={handleSubmit} />    </div>  );}
```

/$

The difference is in *what* they’re letting you cache:

- **useMemocaches theresultof calling your function.** In this example, it caches the result of calling `computeRequirements(product)` so that it doesn’t change unless `product` has changed. This lets you pass the `requirements` object down without unnecessarily re-rendering `ShippingForm`. When necessary, React will call the function you’ve passed during rendering to calculate the result.
- **useCallbackcachesthe function itself.** Unlike `useMemo`, it does not call the function you provide. Instead, it caches the function you provided so that `handleSubmit` *itself* doesn’t change unless `productId` or `referrer` has changed. This lets you pass the `handleSubmit` function down without unnecessarily re-rendering `ShippingForm`. Your code won’t run until the user submits the form.

If you’re already familiar with [useMemo,](https://react.dev/reference/react/useMemo) you might find it helpful to think of `useCallback` as this:

$

```
// Simplified implementation (inside React)function useCallback(fn, dependencies) {  return useMemo(() => fn, dependencies);}
```

/$

[Read more about the difference betweenuseMemoanduseCallback.](https://react.dev/reference/react/useMemo#memoizing-a-function)

##### Deep Dive

#### Should you add useCallback everywhere?

If your app is like this site, and most interactions are coarse (like replacing a page or an entire section), memoization is usually unnecessary. On the other hand, if your app is more like a drawing editor, and most interactions are granular (like moving shapes), then you might find memoization very helpful.

Caching a function with `useCallback` is only valuable in a few cases:

- You pass it as a prop to a component wrapped in [memo.](https://react.dev/reference/react/memo) You want to skip re-rendering if the value hasn’t changed. Memoization lets your component re-render only if dependencies changed.
- The function you’re passing is later used as a dependency of some Hook. For example, another function wrapped in `useCallback` depends on it, or you depend on this function from [useEffect.](https://react.dev/reference/react/useEffect)

There is no benefit to wrapping a function in `useCallback` in other cases. There is no significant harm to doing that either, so some teams choose to not think about individual cases, and memoize as much as possible. The downside is that code becomes less readable. Also, not all memoization is effective: a single value that’s “always new” is enough to break memoization for an entire component.

Note that `useCallback` does not prevent *creating* the function. You’re always creating a function (and that’s fine!), but React ignores it and gives you back a cached function if nothing changed.

**In practice, you can make a lot of memoization unnecessary by following a few principles:**

1. When a component visually wraps other components, let it [accept JSX as children.](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) Then, if the wrapper component updates its own state, React knows that its children don’t need to re-render.
2. Prefer local state and don’t [lift state up](https://react.dev/learn/sharing-state-between-components) any further than necessary. Don’t keep transient state like forms and whether an item is hovered at the top of your tree or in a global state library.
3. Keep your [rendering logic pure.](https://react.dev/learn/keeping-components-pure) If re-rendering a component causes a problem or produces some noticeable visual artifact, it’s a bug in your component! Fix the bug instead of adding memoization.
4. Avoid [unnecessary Effects that update state.](https://react.dev/learn/you-might-not-need-an-effect) Most performance problems in React apps are caused by chains of updates originating from Effects that cause your components to render over and over.
5. Try to [remove unnecessary dependencies from your Effects.](https://react.dev/learn/removing-effect-dependencies) For example, instead of memoization, it’s often simpler to move some object or a function inside an Effect or outside the component.

If a specific interaction still feels laggy, [use the React Developer Tools profiler](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html) to see which components benefit the most from memoization, and add memoization where needed. These principles make your components easier to debug and understand, so it’s good to follow them in any case. In long term, we’re researching [doing memoization automatically](https://www.youtube.com/watch?v=lGEMwh32soc) to solve this once and for all.

#### The difference between useCallback and declaring a function directly

#### Example1of2:Skipping re-rendering withuseCallbackandmemo

In this example, the `ShippingForm` component is **artificially slowed down** so that you can see what happens when a React component you’re rendering is genuinely slow. Try incrementing the counter and toggling the theme.

Incrementing the counter feels slow because it forces the slowed down `ShippingForm` to re-render. That’s expected because the counter has changed, and so you need to reflect the user’s new choice on the screen.

Next, try toggling the theme. **Thanks touseCallbacktogether withmemo, it’s fast despite the artificial slowdown!** `ShippingForm` skipped re-rendering because the `handleSubmit` function has not changed. The `handleSubmit` function has not changed because both `productId` and `referrer` (your `useCallback` dependencies) haven’t changed since last render.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useCallback } from 'react';
import ShippingForm from './ShippingForm.js';

export default function ProductPage({ productId, referrer, theme }) {
  const handleSubmit = useCallback((orderDetails) => {
    post('/product/' + productId + '/buy', {
      referrer,
      orderDetails,
    });
  }, [productId, referrer]);

  return (
    <div className={theme}>
      <ShippingForm onSubmit={handleSubmit} />
    </div>
  );
}

function post(url, data) {
  // Imagine this sends a request...
  console.log('POST /' + url);
  console.log(data);
}
```

/$

---

### Updating state from a memoized callback

Sometimes, you might need to update state based on previous state from a memoized callback.

This `handleAddTodo` function specifies `todos` as a dependency because it computes the next todos from it:

 $

```
function TodoList() {  const [todos, setTodos] = useState([]);  const handleAddTodo = useCallback((text) => {    const newTodo = { id: nextId++, text };    setTodos([...todos, newTodo]);  }, [todos]);  // ...
```

/$

You’ll usually want memoized functions to have as few dependencies as possible. When you read some state only to calculate the next state, you can remove that dependency by passing an [updater function](https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state) instead:

 $

```
function TodoList() {  const [todos, setTodos] = useState([]);  const handleAddTodo = useCallback((text) => {    const newTodo = { id: nextId++, text };    setTodos(todos => [...todos, newTodo]);  }, []); // ✅ No need for the todos dependency  // ...
```

/$

Here, instead of making `todos` a dependency and reading it inside, you pass an instruction about *how* to update the state (`todos => [...todos, newTodo]`) to React. [Read more about updater functions.](https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state)

---

### Preventing an Effect from firing too often

Sometimes, you might want to call a function from inside an [Effect:](https://react.dev/learn/synchronizing-with-effects)

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  function createOptions() {    return {      serverUrl: 'https://localhost:1234',      roomId: roomId    };  }  useEffect(() => {    const options = createOptions();    const connection = createConnection(options);    connection.connect();    // ...
```

/$

This creates a problem. [Every reactive value must be declared as a dependency of your Effect.](https://react.dev/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency) However, if you declare `createOptions` as a dependency, it will cause your Effect to constantly reconnect to the chat room:

 $

```
useEffect(() => {    const options = createOptions();    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [createOptions]); // 🔴 Problem: This dependency changes on every render  // ...
```

/$

To solve this, you can wrap the function you need to call from an Effect into `useCallback`:

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  const createOptions = useCallback(() => {    return {      serverUrl: 'https://localhost:1234',      roomId: roomId    };  }, [roomId]); // ✅ Only changes when roomId changes  useEffect(() => {    const options = createOptions();    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [createOptions]); // ✅ Only changes when createOptions changes  // ...
```

/$

This ensures that the `createOptions` function is the same between re-renders if the `roomId` is the same. **However, it’s even better to remove the need for a function dependency.** Move your function *inside* the Effect:

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  useEffect(() => {    function createOptions() { // ✅ No need for useCallback or function dependencies!      return {        serverUrl: 'https://localhost:1234',        roomId: roomId      };    }    const options = createOptions();    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ Only changes when roomId changes  // ...
```

/$

Now your code is simpler and doesn’t need `useCallback`. [Learn more about removing Effect dependencies.](https://react.dev/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)

---

### Optimizing a custom Hook

If you’re writing a [custom Hook,](https://react.dev/learn/reusing-logic-with-custom-hooks) it’s recommended to wrap any functions that it returns into `useCallback`:

 $

```
function useRouter() {  const { dispatch } = useContext(RouterStateContext);  const navigate = useCallback((url) => {    dispatch({ type: 'navigate', url });  }, [dispatch]);  const goBack = useCallback(() => {    dispatch({ type: 'back' });  }, [dispatch]);  return {    navigate,    goBack,  };}
```

/$

This ensures that the consumers of your Hook can optimize their own code when needed.

---

## Troubleshooting

### Every time my component renders,useCallbackreturns a different function

Make sure you’ve specified the dependency array as a second argument!

If you forget the dependency array, `useCallback` will return a new function every time:

 $

```
function ProductPage({ productId, referrer }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }); // 🔴 Returns a new function every time: no dependency array  // ...
```

/$

This is the corrected version passing the dependency array as a second argument:

 $

```
function ProductPage({ productId, referrer }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails,    });  }, [productId, referrer]); // ✅ Does not return a new function unnecessarily  // ...
```

/$

If this doesn’t help, then the problem is that at least one of your dependencies is different from the previous render. You can debug this problem by manually logging your dependencies to the console:

 $

```
const handleSubmit = useCallback((orderDetails) => {    // ..  }, [productId, referrer]);  console.log([productId, referrer]);
```

/$

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as `temp1` and the second one got saved as `temp2`, you can then use the browser console to check whether each dependency in both arrays is the same:

 $

```
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

/$

When you find which dependency is breaking memoization, either find a way to remove it, or [memoize it as well.](https://react.dev/reference/react/useMemo#memoizing-a-dependency-of-another-hook)

---

### I need to calluseCallbackfor each list item in a loop, but it’s not allowed

Suppose the `Chart` component is wrapped in [memo](https://react.dev/reference/react/memo). You want to skip re-rendering every `Chart` in the list when the `ReportList` component re-renders. However, you can’t call `useCallback` in a loop:

 $

```
function ReportList({ items }) {  return (    <article>      {items.map(item => {        // 🔴 You can't call useCallback in a loop like this:        const handleClick = useCallback(() => {          sendReport(item)        }, [item]);        return (          <figure key={item.id}>            <Chart onClick={handleClick} />          </figure>        );      })}    </article>  );}
```

/$

Instead, extract a component for an individual item, and put `useCallback` there:

 $

```
function ReportList({ items }) {  return (    <article>      {items.map(item =>        <Report key={item.id} item={item} />      )}    </article>  );}function Report({ item }) {  // ✅ Call useCallback at the top level:  const handleClick = useCallback(() => {    sendReport(item)  }, [item]);  return (    <figure>      <Chart onClick={handleClick} />    </figure>  );}
```

/$

Alternatively, you could remove `useCallback` in the last snippet and instead wrap `Report` itself in [memo.](https://react.dev/reference/react/memo) If the `item` prop does not change, `Report` will skip re-rendering, so `Chart` will skip re-rendering too:

 $

```
function ReportList({ items }) {  // ...}const Report = memo(function Report({ item }) {  function handleClick() {    sendReport(item);  }  return (    <figure>      <Chart onClick={handleClick} />    </figure>  );});
```

/$[PrevioususeActionState](https://react.dev/reference/react/useActionState)[NextuseContext](https://react.dev/reference/react/useContext)
