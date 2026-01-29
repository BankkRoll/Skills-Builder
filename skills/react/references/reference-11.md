# useContext and more

# useContext

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useContext

`useContext` is a React Hook that lets you read and subscribe to [context](https://react.dev/learn/passing-data-deeply-with-context) from your component.

$

```
const value = useContext(SomeContext)
```

/$

- [Reference](#reference)
  - [useContext(SomeContext)](#usecontext)
- [Usage](#usage)
  - [Passing data deeply into the tree](#passing-data-deeply-into-the-tree)
  - [Updating data passed via context](#updating-data-passed-via-context)
  - [Specifying a fallback default value](#specifying-a-fallback-default-value)
  - [Overriding context for a part of the tree](#overriding-context-for-a-part-of-the-tree)
  - [Optimizing re-renders when passing objects and functions](#optimizing-re-renders-when-passing-objects-and-functions)
- [Troubleshooting](#troubleshooting)
  - [My component doesn’t see the value from my provider](#my-component-doesnt-see-the-value-from-my-provider)
  - [I am always gettingundefinedfrom my context although the default value is different](#i-am-always-getting-undefined-from-my-context-although-the-default-value-is-different)

---

## Reference

### useContext(SomeContext)

Call `useContext` at the top level of your component to read and subscribe to [context.](https://react.dev/learn/passing-data-deeply-with-context)

 $

```
import { useContext } from 'react';function MyComponent() {  const theme = useContext(ThemeContext);  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

- `SomeContext`: The context that you’ve previously created with [createContext](https://react.dev/reference/react/createContext). The context itself does not hold the information, it only represents the kind of information you can provide or read from components.

#### Returns

`useContext` returns the context value for the calling component. It is determined as the `value` passed to the closest `SomeContext` above the calling component in the tree. If there is no such provider, then the returned value will be the `defaultValue` you have passed to [createContext](https://react.dev/reference/react/createContext) for that context. The returned value is always up-to-date. React automatically re-renders components that read some context if it changes.

#### Caveats

- `useContext()` call in a component is not affected by providers returned from the *same* component. The corresponding `<Context>` **needs to beabove** the component doing the `useContext()` call.
- React **automatically re-renders** all the children that use a particular context starting from the provider that receives a different `value`. The previous and the next values are compared with the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. Skipping re-renders with [memo](https://react.dev/reference/react/memo) does not prevent the children receiving fresh context values.
- If your build system produces duplicates modules in the output (which can happen with symlinks), this can break context. Passing something via context only works if `SomeContext` that you use to provide context and `SomeContext` that you use to read it are **exactlythe same object**, as determined by a `===` comparison.

---

## Usage

### Passing data deeply into the tree

Call `useContext` at the top level of your component to read and subscribe to [context.](https://react.dev/learn/passing-data-deeply-with-context)

 $

```
import { useContext } from 'react';function Button() {  const theme = useContext(ThemeContext);  // ...
```

/$

`useContext` returns the context value for the context you passed. To determine the context value, React searches the component tree and finds **the closest context provider above** for that particular context.

To pass context to a `Button`, wrap it or one of its parent components into the corresponding context provider:

 $

```
function MyPage() {  return (    <ThemeContext value="dark">      <Form />    </ThemeContext>  );}function Form() {  // ... renders buttons inside ...}
```

/$

It doesn’t matter how many layers of components there are between the provider and the `Button`. When a `Button` *anywhere* inside of `Form` calls `useContext(ThemeContext)`, it will receive `"dark"` as the value.

### Pitfall

`useContext()` always looks for the closest provider *above* the component that calls it. It searches upwards and **does not** consider providers in the component from which you’re calling `useContext()`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext, useContext } from 'react';

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
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ children }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className}>
      {children}
    </button>
  );
}
```

/$

---

### Updating data passed via context

Often, you’ll want the context to change over time. To update context, combine it with [state.](https://react.dev/reference/react/useState) Declare a state variable in the parent component, and pass the current state down as the context value to the provider.

 $

```
function MyPage() {  const [theme, setTheme] = useState('dark');  return (    <ThemeContext value={theme}>      <Form />      <Button onClick={() => {        setTheme('light');      }}>        Switch to light theme      </Button>    </ThemeContext>  );}
```

/$

Now any `Button` inside of the provider will receive the current `theme` value. If you call `setTheme` to update the `theme` value that you pass to the provider, all `Button` components will re-render with the new `'light'` value.

#### Examples of updating context

#### Example1of5:Updating a value via context

In this example, the `MyApp` component holds a state variable which is then passed to the `ThemeContext` provider. Checking the “Dark mode” checkbox updates the state. Changing the provided value re-renders all the components using that context.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext(null);

export default function MyApp() {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext value={theme}>
      <Form />
      <label>
        <input
          type="checkbox"
          checked={theme === 'dark'}
          onChange={(e) => {
            setTheme(e.target.checked ? 'dark' : 'light')
          }}
        />
        Use dark mode
      </label>
    </ThemeContext>
  )
}

function Form({ children }) {
  return (
    <Panel title="Welcome">
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ children }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className}>
      {children}
    </button>
  );
}
```

/$

Note that `value="dark"` passes the `"dark"` string, but `value={theme}` passes the value of the JavaScript `theme` variable with [JSX curly braces.](https://react.dev/learn/javascript-in-jsx-with-curly-braces) Curly braces also let you pass context values that aren’t strings.

---

### Specifying a fallback default value

If React can’t find any providers of that particular context in the parent tree, the context value returned by `useContext()` will be equal to the default value that you specified when you [created that context](https://react.dev/reference/react/createContext):

 $

```
const ThemeContext = createContext(null);
```

/$

The default value **never changes**. If you want to update context, use it with state as [described above.](#updating-data-passed-via-context)

Often, instead of `null`, there is some more meaningful value you can use as a default, for example:

 $

```
const ThemeContext = createContext('light');
```

/$

This way, if you accidentally render some component without a corresponding provider, it won’t break. This also helps your components work well in a test environment without setting up a lot of providers in the tests.

In the example below, the “Toggle theme” button is always light because it’s **outside any theme context provider** and the default context theme value is `'light'`. Try editing the default theme to be `'dark'`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext('light');

export default function MyApp() {
  const [theme, setTheme] = useState('light');
  return (
    <>
      <ThemeContext value={theme}>
        <Form />
      </ThemeContext>
      <Button onClick={() => {
        setTheme(theme === 'dark' ? 'light' : 'dark');
      }}>
        Toggle theme
      </Button>
    </>
  )
}

function Form({ children }) {
  return (
    <Panel title="Welcome">
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ children, onClick }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className} onClick={onClick}>
      {children}
    </button>
  );
}
```

/$

---

### Overriding context for a part of the tree

You can override the context for a part of the tree by wrapping that part in a provider with a different value.

 $

```
<ThemeContext value="dark">  ...  <ThemeContext value="light">    <Footer />  </ThemeContext>  ...</ThemeContext>
```

/$

You can nest and override providers as many times as you need.

#### Examples of overriding context

#### Example1of2:Overriding a theme

Here, the button *inside* the `Footer` receives a different context value (`"light"`) than the buttons outside (`"dark"`).

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext, useContext } from 'react';

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
      <Button>Sign up</Button>
      <Button>Log in</Button>
      <ThemeContext value="light">
        <Footer />
      </ThemeContext>
    </Panel>
  );
}

function Footer() {
  return (
    <footer>
      <Button>Settings</Button>
    </footer>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      {title && <h1>{title}</h1>}
      {children}
    </section>
  )
}

function Button({ children }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className}>
      {children}
    </button>
  );
}
```

/$

---

### Optimizing re-renders when passing objects and functions

You can pass any values via context, including objects and functions.

 $

```
function MyApp() {  const [currentUser, setCurrentUser] = useState(null);  function login(response) {    storeCredentials(response.credentials);    setCurrentUser(response.user);  }  return (    <AuthContext value={{ currentUser, login }}>      <Page />    </AuthContext>  );}
```

/$

Here, the context value is a JavaScript object with two properties, one of which is a function. Whenever `MyApp` re-renders (for example, on a route update), this will be a *different* object pointing at a *different* function, so React will also have to re-render all components deep in the tree that call `useContext(AuthContext)`.

In smaller apps, this is not a problem. However, there is no need to re-render them if the underlying data, like `currentUser`, has not changed. To help React take advantage of that fact, you may wrap the `login` function with [useCallback](https://react.dev/reference/react/useCallback) and wrap the object creation into [useMemo](https://react.dev/reference/react/useMemo). This is a performance optimization:

 $

```
import { useCallback, useMemo } from 'react';function MyApp() {  const [currentUser, setCurrentUser] = useState(null);  const login = useCallback((response) => {    storeCredentials(response.credentials);    setCurrentUser(response.user);  }, []);  const contextValue = useMemo(() => ({    currentUser,    login  }), [currentUser, login]);  return (    <AuthContext value={contextValue}>      <Page />    </AuthContext>  );}
```

/$

As a result of this change, even if `MyApp` needs to re-render, the components calling `useContext(AuthContext)` won’t need to re-render unless `currentUser` has changed.

Read more about [useMemo](https://react.dev/reference/react/useMemo#skipping-re-rendering-of-components) and [useCallback.](https://react.dev/reference/react/useCallback#skipping-re-rendering-of-components)

---

## Troubleshooting

### My component doesn’t see the value from my provider

There are a few common ways that this can happen:

1. You’re rendering `<SomeContext>` in the same component (or below) as where you’re calling `useContext()`. Move `<SomeContext>` *above and outside* the component calling `useContext()`.
2. You may have forgotten to wrap your component with `<SomeContext>`, or you might have put it in a different part of the tree than you thought. Check whether the hierarchy is right using [React DevTools.](https://react.dev/learn/react-developer-tools)
3. You might be running into some build issue with your tooling that causes `SomeContext` as seen from the providing component and `SomeContext` as seen by the reading component to be two different objects. This can happen if you use symlinks, for example. You can verify this by assigning them to globals like `window.SomeContext1` and `window.SomeContext2` and then checking whether `window.SomeContext1 === window.SomeContext2` in the console. If they’re not the same, fix that issue on the build tool level.

### I am always gettingundefinedfrom my context although the default value is different

You might have a provider without a `value` in the tree:

 $

```
// 🚩 Doesn't work: no value prop<ThemeContext>   <Button /></ThemeContext>
```

/$

If you forget to specify `value`, it’s like passing `value={undefined}`.

You may have also mistakingly used a different prop name by mistake:

 $

```
// 🚩 Doesn't work: prop should be called "value"<ThemeContext theme={theme}>   <Button /></ThemeContext>
```

/$

In both of these cases you should see a warning from React in the console. To fix them, call the prop `value`:

 $

```
// ✅ Passing the value prop<ThemeContext value={theme}>   <Button /></ThemeContext>
```

/$

Note that the [default value from yourcreateContext(defaultValue)call](#specifying-a-fallback-default-value) is only used **if there is no matching provider above at all.** If there is a `<SomeContext value={undefined}>` component somewhere in the parent tree, the component calling `useContext(SomeContext)` *will* receive `undefined` as the context value.

[PrevioususeCallback](https://react.dev/reference/react/useCallback)[NextuseDebugValue](https://react.dev/reference/react/useDebugValue)

---

# useDebugValue

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useDebugValue

`useDebugValue` is a React Hook that lets you add a label to a custom Hook in [React DevTools.](https://react.dev/learn/react-developer-tools)

$

```
useDebugValue(value, format?)
```

/$

- [Reference](#reference)
  - [useDebugValue(value, format?)](#usedebugvalue)
- [Usage](#usage)
  - [Adding a label to a custom Hook](#adding-a-label-to-a-custom-hook)
  - [Deferring formatting of a debug value](#deferring-formatting-of-a-debug-value)

---

## Reference

### useDebugValue(value, format?)

Call `useDebugValue` at the top level of your [custom Hook](https://react.dev/learn/reusing-logic-with-custom-hooks) to display a readable debug value:

 $

```
import { useDebugValue } from 'react';function useOnlineStatus() {  // ...  useDebugValue(isOnline ? 'Online' : 'Offline');  // ...}
```

/$

[See more examples below.](#usage)

#### Parameters

- `value`: The value you want to display in React DevTools. It can have any type.
- **optional** `format`: A formatting function. When the component is inspected, React DevTools will call the formatting function with the `value` as the argument, and then display the returned formatted value (which may have any type). If you don’t specify the formatting function, the original `value` itself will be displayed.

#### Returns

`useDebugValue` does not return anything.

## Usage

### Adding a label to a custom Hook

Call `useDebugValue` at the top level of your [custom Hook](https://react.dev/learn/reusing-logic-with-custom-hooks) to display a readable debug value for [React DevTools.](https://react.dev/learn/react-developer-tools)

 $

```
import { useDebugValue } from 'react';function useOnlineStatus() {  // ...  useDebugValue(isOnline ? 'Online' : 'Offline');  // ...}
```

/$

This gives components calling `useOnlineStatus` a label like `OnlineStatus: "Online"` when you inspect them:

 ![A screenshot of React DevTools showing the debug value](https://react.dev/images/docs/react-devtools-usedebugvalue.png)

Without the `useDebugValue` call, only the underlying data (in this example, `true`) would be displayed.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useSyncExternalStore, useDebugValue } from 'react';

export function useOnlineStatus() {
  const isOnline = useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}

function subscribe(callback) {
  window.addEventListener('online', callback);
  window.addEventListener('offline', callback);
  return () => {
    window.removeEventListener('online', callback);
    window.removeEventListener('offline', callback);
  };
}
```

/$

### Note

Don’t add debug values to every custom Hook. It’s most valuable for custom Hooks that are part of shared libraries and that have a complex internal data structure that’s difficult to inspect.

---

### Deferring formatting of a debug value

You can also pass a formatting function as the second argument to `useDebugValue`:

 $

```
useDebugValue(date, date => date.toDateString());
```

/$

Your formatting function will receive the debug value as a parameter and should return a formatted display value. When your component is inspected, React DevTools will call this function and display its result.

This lets you avoid running potentially expensive formatting logic unless the component is actually inspected. For example, if `date` is a Date value, this avoids calling `toDateString()` on it for every render.

[PrevioususeContext](https://react.dev/reference/react/useContext)[NextuseDeferredValue](https://react.dev/reference/react/useDeferredValue)

---

# useDeferredValue

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useDeferredValue

`useDeferredValue` is a React Hook that lets you defer updating a part of the UI.

$

```
const deferredValue = useDeferredValue(value)
```

/$

- [Reference](#reference)
  - [useDeferredValue(value, initialValue?)](#usedeferredvalue)
- [Usage](#usage)
  - [Showing stale content while fresh content is loading](#showing-stale-content-while-fresh-content-is-loading)
  - [Indicating that the content is stale](#indicating-that-the-content-is-stale)
  - [Deferring re-rendering for a part of the UI](#deferring-re-rendering-for-a-part-of-the-ui)

---

## Reference

### useDeferredValue(value, initialValue?)

Call `useDeferredValue` at the top level of your component to get a deferred version of that value.

 $

```
import { useState, useDeferredValue } from 'react';function SearchPage() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  // ...}
```

/$

[See more examples below.](#usage)

#### Parameters

- `value`: The value you want to defer. It can have any type.
- **optional** `initialValue`: A value to use during the initial render of a component. If this option is omitted, `useDeferredValue` will not defer during the initial render, because there’s no previous version of `value` that it can render instead.

#### Returns

- `currentValue`: During the initial render, the returned deferred value will be the `initialValue`, or the same as the value you provided. During updates, React will first attempt a re-render with the old value (so it will return the old value), and then try another re-render in the background with the new value (so it will return the updated value).

#### Caveats

- When an update is inside a Transition, `useDeferredValue` always returns the new `value` and does not spawn a deferred render, since the update is already deferred.
- The values you pass to `useDeferredValue` should either be primitive values (like strings and numbers) or objects created outside of rendering. If you create a new object during rendering and immediately pass it to `useDeferredValue`, it will be different on every render, causing unnecessary background re-renders.
- When `useDeferredValue` receives a different value (compared with [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), in addition to the current render (when it still uses the previous value), it schedules a re-render in the background with the new value. The background re-render is interruptible: if there’s another update to the `value`, React will restart the background re-render from scratch. For example, if the user is typing into an input faster than a chart receiving its deferred value can re-render, the chart will only re-render after the user stops typing.
- `useDeferredValue` is integrated with [<Suspense>.](https://react.dev/reference/react/Suspense) If the background update caused by a new value suspends the UI, the user will not see the fallback. They will see the old deferred value until the data loads.
- `useDeferredValue` does not by itself prevent extra network requests.
- There is no fixed delay caused by `useDeferredValue` itself. As soon as React finishes the original re-render, React will immediately start working on the background re-render with the new deferred value. Any updates caused by events (like typing) will interrupt the background re-render and get prioritized over it.
- The background re-render caused by `useDeferredValue` does not fire Effects until it’s committed to the screen. If the background re-render suspends, its Effects will run after the data loads and the UI updates.

---

## Usage

### Showing stale content while fresh content is loading

Call `useDeferredValue` at the top level of your component to defer updating some part of your UI.

 $

```
import { useState, useDeferredValue } from 'react';function SearchPage() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  // ...}
```

/$

During the initial render, the deferred value will be the same as the value you provided.

During updates, the deferred value will “lag behind” the latest value. In particular, React will first re-render *without* updating the deferred value, and then try to re-render with the newly received value in the background.

**Let’s walk through an example to see when this is useful.**

### Note

This example assumes you use a Suspense-enabled data source:

- Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/app/getting-started/fetching-data#with-suspense)
- Lazy-loading component code with [lazy](https://react.dev/reference/react/lazy)
- Reading the value of a Promise with [use](https://react.dev/reference/react/use)

[Learn more about Suspense and its limitations.](https://react.dev/reference/react/Suspense)

In this example, the `SearchResults` component [suspends](https://react.dev/reference/react/Suspense#displaying-a-fallback-while-content-is-loading) while fetching the search results. Try typing `"a"`, waiting for the results, and then editing it to `"ab"`. The results for `"a"` get replaced by the loading fallback.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <SearchResults query={query} />
      </Suspense>
    </>
  );
}
```

/$

A common alternative UI pattern is to *defer* updating the list of results and to keep showing the previous results until the new results are ready. Call `useDeferredValue` to pass a deferred version of the query down:

 $

```
export default function App() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  return (    <>      <label>        Search albums:        <input value={query} onChange={e => setQuery(e.target.value)} />      </label>      <Suspense fallback={<h2>Loading...</h2>}>        <SearchResults query={deferredQuery} />      </Suspense>    </>  );}
```

/$

The `query` will update immediately, so the input will display the new value. However, the `deferredQuery` will keep its previous value until the data has loaded, so `SearchResults` will show the stale results for a bit.

Enter `"a"` in the example below, wait for the results to load, and then edit the input to `"ab"`. Notice how instead of the Suspense fallback, you now see the stale result list until the new results have loaded:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState, useDeferredValue } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <SearchResults query={deferredQuery} />
      </Suspense>
    </>
  );
}
```

/$

##### Deep Dive

#### How does deferring a value work under the hood?

You can think of it as happening in two steps:

1. **First, React re-renders with the newquery("ab") but with the olddeferredQuery(still"a").** The `deferredQuery` value, which you pass to the result list, is *deferred:* it “lags behind” the `query` value.
2. **In the background, React tries to re-render withbothqueryanddeferredQueryupdated to"ab".** If this re-render completes, React will show it on the screen. However, if it suspends (the results for `"ab"` have not loaded yet), React will abandon this rendering attempt, and retry this re-render again after the data has loaded. The user will keep seeing the stale deferred value until the data is ready.

The deferred “background” rendering is interruptible. For example, if you type into the input again, React will abandon it and restart with the new value. React will always use the latest provided value.

Note that there is still a network request per each keystroke. What’s being deferred here is displaying results (until they’re ready), not the network requests themselves. Even if the user continues typing, responses for each keystroke get cached, so pressing Backspace is instant and doesn’t fetch again.

---

### Indicating that the content is stale

In the example above, there is no indication that the result list for the latest query is still loading. This can be confusing to the user if the new results take a while to load. To make it more obvious to the user that the result list does not match the latest query, you can add a visual indication when the stale result list is displayed:

 $

```
<div style={{  opacity: query !== deferredQuery ? 0.5 : 1,}}>  <SearchResults query={deferredQuery} /></div>
```

/$

With this change, as soon as you start typing, the stale result list gets slightly dimmed until the new result list loads. You can also add a CSS transition to delay dimming so that it feels gradual, like in the example below:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState, useDeferredValue } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <div style={{
          opacity: isStale ? 0.5 : 1,
          transition: isStale ? 'opacity 0.2s 0.2s linear' : 'opacity 0s 0s linear'
        }}>
          <SearchResults query={deferredQuery} />
        </div>
      </Suspense>
    </>
  );
}
```

/$

---

### Deferring re-rendering for a part of the UI

You can also apply `useDeferredValue` as a performance optimization. It is useful when a part of your UI is slow to re-render, there’s no easy way to optimize it, and you want to prevent it from blocking the rest of the UI.

Imagine you have a text field and a component (like a chart or a long list) that re-renders on every keystroke:

 $

```
function App() {  const [text, setText] = useState('');  return (    <>      <input value={text} onChange={e => setText(e.target.value)} />      <SlowList text={text} />    </>  );}
```

/$

First, optimize `SlowList` to skip re-rendering when its props are the same. To do this, [wrap it inmemo:](https://react.dev/reference/react/memo#skipping-re-rendering-when-props-are-unchanged)

 $

```
const SlowList = memo(function SlowList({ text }) {  // ...});
```

/$

However, this only helps if the `SlowList` props are *the same* as during the previous render. The problem you’re facing now is that it’s slow when they’re *different,* and when you actually need to show different visual output.

Concretely, the main performance problem is that whenever you type into the input, the `SlowList` receives new props, and re-rendering its entire tree makes the typing feel janky. In this case, `useDeferredValue` lets you prioritize updating the input (which must be fast) over updating the result list (which is allowed to be slower):

 $

```
function App() {  const [text, setText] = useState('');  const deferredText = useDeferredValue(text);  return (    <>      <input value={text} onChange={e => setText(e.target.value)} />      <SlowList text={deferredText} />    </>  );}
```

/$

This does not make re-rendering of the `SlowList` faster. However, it tells React that re-rendering the list can be deprioritized so that it doesn’t block the keystrokes. The list will “lag behind” the input and then “catch up”. Like before, React will attempt to update the list as soon as possible, but will not block the user from typing.

#### The difference between useDeferredValue and unoptimized re-rendering

#### Example1of2:Deferred re-rendering of the list

In this example, each item in the `SlowList` component is **artificially slowed down** so that you can see how `useDeferredValue` lets you keep the input responsive. Type into the input and notice that typing feels snappy while the list “lags behind” it.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useDeferredValue } from 'react';
import SlowList from './SlowList.js';

export default function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <SlowList text={deferredText} />
    </>
  );
}
```

/$

### Pitfall

This optimization requires `SlowList` to be wrapped in [memo.](https://react.dev/reference/react/memo) This is because whenever the `text` changes, React needs to be able to re-render the parent component quickly. During that re-render, `deferredText` still has its previous value, so `SlowList` is able to skip re-rendering (its props have not changed). Without [memo,](https://react.dev/reference/react/memo) it would have to re-render anyway, defeating the point of the optimization.

##### Deep Dive

#### How is deferring a value different from debouncing and throttling?

There are two common optimization techniques you might have used before in this scenario:

- *Debouncing* means you’d wait for the user to stop typing (e.g. for a second) before updating the list.
- *Throttling* means you’d update the list every once in a while (e.g. at most once a second).

While these techniques are helpful in some cases, `useDeferredValue` is better suited to optimizing rendering because it is deeply integrated with React itself and adapts to the user’s device.

Unlike debouncing or throttling, it doesn’t require choosing any fixed delay. If the user’s device is fast (e.g. powerful laptop), the deferred re-render would happen almost immediately and wouldn’t be noticeable. If the user’s device is slow, the list would “lag behind” the input proportionally to how slow the device is.

Also, unlike with debouncing or throttling, deferred re-renders done by `useDeferredValue` are interruptible by default. This means that if React is in the middle of re-rendering a large list, but the user makes another keystroke, React will abandon that re-render, handle the keystroke, and then start rendering in the background again. By contrast, debouncing and throttling still produce a janky experience because they’re *blocking:* they merely postpone the moment when rendering blocks the keystroke.

If the work you’re optimizing doesn’t happen during rendering, debouncing and throttling are still useful. For example, they can let you fire fewer network requests. You can also use these techniques together.

[PrevioususeDebugValue](https://react.dev/reference/react/useDebugValue)[NextuseEffect](https://react.dev/reference/react/useEffect)
