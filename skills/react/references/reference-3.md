# cache and more

# cache

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# cache

### React Server Components

`cache` is only for use with [React Server Components](https://react.dev/reference/rsc/server-components).

`cache` lets you cache the result of a data fetch or computation.

$

```
const cachedFn = cache(fn);
```

/$

- [Reference](#reference)
  - [cache(fn)](#cache)
- [Usage](#usage)
  - [Cache an expensive computation](#cache-expensive-computation)
  - [Share a snapshot of data](#take-and-share-snapshot-of-data)
  - [Preload data](#preload-data)
- [Troubleshooting](#troubleshooting)
  - [My memoized function still runs even though I’ve called it with the same arguments](#memoized-function-still-runs)

---

## Reference

### cache(fn)

Call `cache` outside of any components to create a version of the function with caching.

 $

```
import {cache} from 'react';import calculateMetrics from 'lib/metrics';const getMetrics = cache(calculateMetrics);function Chart({data}) {  const report = getMetrics(data);  // ...}
```

/$

When `getMetrics` is first called with `data`, `getMetrics` will call `calculateMetrics(data)` and store the result in cache. If `getMetrics` is called again with the same `data`, it will return the cached result instead of calling `calculateMetrics(data)` again.

[See more examples below.](#usage)

#### Parameters

- `fn`: The function you want to cache results for. `fn` can take any arguments and return any value.

#### Returns

`cache` returns a cached version of `fn` with the same type signature. It does not call `fn` in the process.

When calling `cachedFn` with given arguments, it first checks if a cached result exists in the cache. If a cached result exists, it returns the result. If not, it calls `fn` with the arguments, stores the result in the cache, and returns the result. The only time `fn` is called is when there is a cache miss.

### Note

The optimization of caching return values based on inputs is known as [memoization](https://en.wikipedia.org/wiki/Memoization). We refer to the function returned from `cache` as a memoized function.

#### Caveats

- React will invalidate the cache for all memoized functions for each server request.
- Each call to `cache` creates a new function. This means that calling `cache` with the same function multiple times will return different memoized functions that do not share the same cache.
- `cachedFn` will also cache errors. If `fn` throws an error for certain arguments, it will be cached, and the same error is re-thrown when `cachedFn` is called with those same arguments.
- `cache` is for use in [Server Components](https://react.dev/reference/rsc/server-components) only.

---

## Usage

### Cache an expensive computation

Use `cache` to skip duplicate work.

 $

```
import {cache} from 'react';import calculateUserMetrics from 'lib/user';const getUserMetrics = cache(calculateUserMetrics);function Profile({user}) {  const metrics = getUserMetrics(user);  // ...}function TeamReport({users}) {  for (let user in users) {    const metrics = getUserMetrics(user);    // ...  }  // ...}
```

/$

If the same `user` object is rendered in both `Profile` and `TeamReport`, the two components can share work and only call `calculateUserMetrics` once for that `user`.

Assume `Profile` is rendered first. It will call `getUserMetrics`, and check if there is a cached result. Since it is the first time `getUserMetrics` is called with that `user`, there will be a cache miss. `getUserMetrics` will then call `calculateUserMetrics` with that `user` and write the result to cache.

When `TeamReport` renders its list of `users` and reaches the same `user` object, it will call `getUserMetrics` and read the result from cache.

If `calculateUserMetrics` can be aborted by passing an [AbortSignal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal), you can use [cacheSignal()](https://react.dev/reference/react/cacheSignal) to cancel the expensive computation if React has finished rendering. `calculateUserMetrics` may already handle cancellation internally by using `cacheSignal` directly.

### Pitfall

##### Calling different memoized functions will read from different caches.

To access the same cache, components must call the same memoized function.

$

```
// Temperature.jsimport {cache} from 'react';import {calculateWeekReport} from './report';export function Temperature({cityData}) {  // 🚩 Wrong: Calling `cache` in component creates new `getWeekReport` for each render  const getWeekReport = cache(calculateWeekReport);  const report = getWeekReport(cityData);  // ...}
```

/$$

```
// Precipitation.jsimport {cache} from 'react';import {calculateWeekReport} from './report';// 🚩 Wrong: `getWeekReport` is only accessible for `Precipitation` component.const getWeekReport = cache(calculateWeekReport);export function Precipitation({cityData}) {  const report = getWeekReport(cityData);  // ...}
```

/$

In the above example, `Precipitation` and `Temperature` each call `cache` to create a new memoized function with their own cache look-up. If both components render for the same `cityData`, they will do duplicate work to call `calculateWeekReport`.

In addition, `Temperature` creates a new memoized function each time the component is rendered which doesn’t allow for any cache sharing.

To maximize cache hits and reduce work, the two components should call the same memoized function to access the same cache. Instead, define the memoized function in a dedicated module that can be [import-ed](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) across components.

$

```
// getWeekReport.jsimport {cache} from 'react';import {calculateWeekReport} from './report';export default cache(calculateWeekReport);
```

/$$

```
// Temperature.jsimport getWeekReport from './getWeekReport';export default function Temperature({cityData}) {	const report = getWeekReport(cityData);  // ...}
```

/$$

```
// Precipitation.jsimport getWeekReport from './getWeekReport';export default function Precipitation({cityData}) {  const report = getWeekReport(cityData);  // ...}
```

/$

Here, both components call the same memoized function exported from `./getWeekReport.js` to read and write to the same cache.

### Share a snapshot of data

To share a snapshot of data between components, call `cache` with a data-fetching function like `fetch`. When multiple components make the same data fetch, only one request is made and the data returned is cached and shared across components. All components refer to the same snapshot of data across the server render.

 $

```
import {cache} from 'react';import {fetchTemperature} from './api.js';const getTemperature = cache(async (city) => {	return await fetchTemperature(city);});async function AnimatedWeatherCard({city}) {	const temperature = await getTemperature(city);	// ...}async function MinimalWeatherCard({city}) {	const temperature = await getTemperature(city);	// ...}
```

/$

If `AnimatedWeatherCard` and `MinimalWeatherCard` both render for the same city, they will receive the same snapshot of data from the memoized function.

If `AnimatedWeatherCard` and `MinimalWeatherCard` supply different city arguments to `getTemperature`, then `fetchTemperature` will be called twice and each call site will receive different data.

The city acts as a cache key.

### Note

Asynchronous rendering is only supported for Server Components.

$

```
async function AnimatedWeatherCard({city}) {	const temperature = await getTemperature(city);	// ...}
```

/$

To render components that use asynchronous data in Client Components, see [use()documentation](https://react.dev/reference/react/use).

### Preload data

By caching a long-running data fetch, you can kick off asynchronous work prior to rendering the component.

 $

```
const getUser = cache(async (id) => {  return await db.user.query(id);});async function Profile({id}) {  const user = await getUser(id);  return (    <section>      <img src={user.profilePic} />      <h2>{user.name}</h2>    </section>  );}function Page({id}) {  // ✅ Good: start fetching the user data  getUser(id);  // ... some computational work  return (    <>      <Profile id={id} />    </>  );}
```

/$

When rendering `Page`, the component calls `getUser` but note that it doesn’t use the returned data. This early `getUser` call kicks off the asynchronous database query that occurs while `Page` is doing other computational work and rendering children.

When rendering `Profile`, we call `getUser` again. If the initial `getUser` call has already returned and cached the user data, when `Profile` asks and waits for this data, it can simply read from the cache without requiring another remote procedure call. If the  initial data request hasn’t been completed, preloading data in this pattern reduces delay in data-fetching.

##### Deep Dive

#### Caching asynchronous work

When evaluating an [asynchronous function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function), you will receive a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) for that work. The promise holds the state of that work (*pending*, *fulfilled*, *failed*) and its eventual settled result.

In this example, the asynchronous function `fetchData` returns a promise that is awaiting the `fetch`.

$

```
async function fetchData() {  return await fetch(`https://...`);}const getData = cache(fetchData);async function MyComponent() {  getData();  // ... some computational work  await getData();  // ...}
```

/$

In calling `getData` the first time, the promise returned from `fetchData` is cached. Subsequent look-ups will then return the same promise.

Notice that the first `getData` call does not `await` whereas the second does. [await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await) is a JavaScript operator that will wait and return the settled result of the promise. The first `getData` call simply initiates the `fetch` to cache the promise for the second `getData` to look-up.

If by the second call the promise is still *pending*, then `await` will pause for the result. The optimization is that while we wait on the `fetch`, React can continue with computational work, thus reducing the wait time for the second call.

If the promise is already settled, either to an error or the *fulfilled* result, `await` will return that value immediately. In both outcomes, there is a performance benefit.

### Pitfall

##### Calling a memoized function outside of a component will not use the cache.

$

```
import {cache} from 'react';const getUser = cache(async (userId) => {  return await db.user.query(userId);});// 🚩 Wrong: Calling memoized function outside of component will not memoize.getUser('demo-id');async function DemoProfile() {  // ✅ Good: `getUser` will memoize.  const user = await getUser('demo-id');  return <Profile user={user} />;}
```

/$

React only provides cache access to the memoized function in a component. When calling `getUser` outside of a component, it will still evaluate the function but not read or update the cache.

This is because cache access is provided through a [context](https://react.dev/learn/passing-data-deeply-with-context) which is only accessible from a component.

##### Deep Dive

#### When should I usecache,memo, oruseMemo?

All mentioned APIs offer memoization but the difference is what they’re intended to memoize, who can access the cache, and when their cache is invalidated.

#### useMemo

In general, you should use [useMemo](https://react.dev/reference/react/useMemo) for caching an expensive computation in a Client Component across renders. As an example, to memoize a transformation of data within a component.

$

```
'use client';function WeatherReport({record}) {  const avgTemp = useMemo(() => calculateAvg(record), record);  // ...}function App() {  const record = getRecord();  return (    <>      <WeatherReport record={record} />      <WeatherReport record={record} />    </>  );}
```

/$

In this example, `App` renders two `WeatherReport`s with the same record. Even though both components do the same work, they cannot share work. `useMemo`’s cache is only local to the component.

However, `useMemo` does ensure that if `App` re-renders and the `record` object doesn’t change, each component instance would skip work and use the memoized value of `avgTemp`. `useMemo` will only cache the last computation of `avgTemp` with the given dependencies.

#### cache

In general, you should use `cache` in Server Components to memoize work that can be shared across components.

$

```
const cachedFetchReport = cache(fetchReport);function WeatherReport({city}) {  const report = cachedFetchReport(city);  // ...}function App() {  const city = "Los Angeles";  return (    <>      <WeatherReport city={city} />      <WeatherReport city={city} />    </>  );}
```

/$

Re-writing the previous example to use `cache`, in this case the second instance of `WeatherReport` will be able to skip duplicate work and read from the same cache as the first `WeatherReport`. Another difference from the previous example is that `cache` is also recommended for memoizing data fetches, unlike `useMemo` which should only be used for computations.

At this time, `cache` should only be used in Server Components and the cache will be invalidated across server requests.

#### memo

You should use [memo](https://react.dev/reference/react/memo) to prevent a component re-rendering if its props are unchanged.

$

```
'use client';function WeatherReport({record}) {  const avgTemp = calculateAvg(record);  // ...}const MemoWeatherReport = memo(WeatherReport);function App() {  const record = getRecord();  return (    <>      <MemoWeatherReport record={record} />      <MemoWeatherReport record={record} />    </>  );}
```

/$

In this example, both `MemoWeatherReport` components will call `calculateAvg` when first rendered. However, if `App` re-renders, with no changes to `record`, none of the props have changed and `MemoWeatherReport` will not re-render.

Compared to `useMemo`, `memo` memoizes the component render based on props vs. specific computations. Similar to `useMemo`, the memoized component only caches the last render with the last prop values. Once the props change, the cache invalidates and the component re-renders.

---

## Troubleshooting

### My memoized function still runs even though I’ve called it with the same arguments

See prior mentioned pitfalls

- [Calling different memoized functions will read from different caches.](#pitfall-different-memoized-functions)
- [Calling a memoized function outside of a component will not use the cache.](#pitfall-memoized-call-outside-component)

If none of the above apply, it may be a problem with how React checks if something exists in cache.

If your arguments are not [primitives](https://developer.mozilla.org/en-US/docs/Glossary/Primitive) (ex. objects, functions, arrays), ensure you’re passing the same object reference.

When calling a memoized function, React will look up the input arguments to see if a result is already cached. React will use shallow equality of the arguments to determine if there is a cache hit.

 $

```
import {cache} from 'react';const calculateNorm = cache((vector) => {  // ...});function MapMarker(props) {  // 🚩 Wrong: props is an object that changes every render.  const length = calculateNorm(props);  // ...}function App() {  return (    <>      <MapMarker x={10} y={10} z={10} />      <MapMarker x={10} y={10} z={10} />    </>  );}
```

/$

In this case the two `MapMarker`s look like they’re doing the same work and calling `calculateNorm` with the same value of `{x: 10, y: 10, z:10}`. Even though the objects contain the same values, they are not the same object reference as each component creates its own `props` object.

React will call [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) on the input to verify if there is a cache hit.

 $

```
import {cache} from 'react';const calculateNorm = cache((x, y, z) => {  // ...});function MapMarker(props) {  // ✅ Good: Pass primitives to memoized function  const length = calculateNorm(props.x, props.y, props.z);  // ...}function App() {  return (    <>      <MapMarker x={10} y={10} z={10} />      <MapMarker x={10} y={10} z={10} />    </>  );}
```

/$

One way to address this could be to pass the vector dimensions to `calculateNorm`. This works because the dimensions themselves are primitives.

Another solution may be to pass the vector object itself as a prop to the component. We’ll need to pass the same object to both component instances.

 $

```
import {cache} from 'react';const calculateNorm = cache((vector) => {  // ...});function MapMarker(props) {  // ✅ Good: Pass the same `vector` object  const length = calculateNorm(props.vector);  // ...}function App() {  const vector = [10, 10, 10];  return (    <>      <MapMarker vector={vector} />      <MapMarker vector={vector} />    </>  );}
```

/$[PreviousaddTransitionType](https://react.dev/reference/react/addTransitionType)[NextcacheSignal](https://react.dev/reference/react/cacheSignal)

---

# cacheSignal

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# cacheSignal

### React Server Components

`cacheSignal` is currently only used with [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components).

`cacheSignal` allows you to know when the `cache()` lifetime is over.

$

```
const signal = cacheSignal();
```

/$

- [Reference](#reference)
  - [cacheSignal](#cachesignal)
- [Usage](#usage)
  - [Cancel in-flight requests](#cancel-in-flight-requests)
  - [Ignore errors after React has finished rendering](#ignore-errors-after-react-has-finished-rendering)

---

## Reference

### cacheSignal

Call `cacheSignal` to get an `AbortSignal`.

 $

```
import {cacheSignal} from 'react';async function Component() {  await fetch(url, { signal: cacheSignal() });}
```

/$

When React has finished rendering, the `AbortSignal` will be aborted. This allows you to cancel any in-flight work that is no longer needed.
Rendering is considered finished when:

- React has successfully completed rendering
- the render was aborted
- the render has failed

#### Parameters

This function does not accept any parameters.

#### Returns

`cacheSignal` returns an `AbortSignal` if called during rendering. Otherwise `cacheSignal()` returns `null`.

#### Caveats

- `cacheSignal` is currently for use in [React Server Components](https://react.dev/reference/rsc/server-components) only. In Client Components, it will always return `null`. In the future it will also be used for Client Component when a client cache refreshes or invalidates. You should not assume it’ll always be null on the client.
- If called outside of rendering, `cacheSignal` will return `null` to make it clear that the current scope isn’t cached forever.

---

## Usage

### Cancel in-flight requests

Call `cacheSignal` to abort in-flight requests.

 $

```
import {cache, cacheSignal} from 'react';const dedupedFetch = cache(fetch);async function Component() {  await dedupedFetch(url, { signal: cacheSignal() });}
```

/$

### Pitfall

You can’t use `cacheSignal` to abort async work that was started outside of rendering e.g.

$

```
import {cacheSignal} from 'react';// 🚩 Pitfall: The request will not actually be aborted if the rendering of `Component` is finished.const response = fetch(url, { signal: cacheSignal() });async function Component() {  await response;}
```

/$

### Ignore errors after React has finished rendering

If a function throws, it may be due to cancellation (e.g. the Database connection has been closed). You can use the `aborted` property to check if the error was due to cancellation or a real error. You may want to ignore errors that were due to cancellation.

 $

```
import {cacheSignal} from "react";import {queryDatabase, logError} from "./database";async function getData(id) {  try {     return await queryDatabase(id);  } catch (x) {     if (!cacheSignal()?.aborted) {        // only log if it's a real error and not due to cancellation       logError(x);     }     return null;  }}async function Component({id}) {  const data = await getData(id);  if (data === null) {    return <div>No data available</div>;  }  return <div>{data.name}</div>;}
```

/$[Previouscache](https://react.dev/reference/react/cache)[NextcaptureOwnerStack](https://react.dev/reference/react/captureOwnerStack)

---

# captureOwnerStack

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# captureOwnerStack

`captureOwnerStack` reads the current Owner Stack in development and returns it as a string if available.

$

```
const stack = captureOwnerStack();
```

/$

- [Reference](#reference)
  - [captureOwnerStack()](#captureownerstack)
- [Usage](#usage)
  - [Enhance a custom error overlay](#enhance-a-custom-error-overlay)
- [Troubleshooting](#troubleshooting)
  - [The Owner Stack isnull](#the-owner-stack-is-null)
  - [captureOwnerStackis not available](#captureownerstack-is-not-available)

---

## Reference

### captureOwnerStack()

Call `captureOwnerStack` to get the current Owner Stack.

 $

```
import * as React from 'react';function Component() {  if (process.env.NODE_ENV !== 'production') {    const ownerStack = React.captureOwnerStack();    console.log(ownerStack);  }}
```

/$

#### Parameters

`captureOwnerStack` does not take any parameters.

#### Returns

`captureOwnerStack` returns `string | null`.

Owner Stacks are available in

- Component render
- Effects (e.g. `useEffect`)
- React’s event handlers (e.g. `<button onClick={...} />`)
- React error handlers ([React Root options](https://react.dev/reference/react-dom/client/createRoot#parameters) `onCaughtError`, `onRecoverableError`, and `onUncaughtError`)

If no Owner Stack is available, `null` is returned (see [Troubleshooting: The Owner Stack isnull](#the-owner-stack-is-null)).

#### Caveats

- Owner Stacks are only available in development. `captureOwnerStack` will always return `null` outside of development.

##### Deep Dive

#### Owner Stack vs Component Stack

The Owner Stack is different from the Component Stack available in React error handlers like [errorInfo.componentStackinonUncaughtError](https://react.dev/reference/react-dom/client/hydrateRoot#error-logging-in-production).

For example, consider the following code:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {captureOwnerStack} from 'react';
import {createRoot} from 'react-dom/client';
import App, {Component} from './App.js';
import './styles.css';

createRoot(document.createElement('div'), {
  onUncaughtError: (error, errorInfo) => {
    // The stacks are logged instead of showing them in the UI directly to
    // highlight that browsers will apply sourcemaps to the logged stacks.
    // Note that sourcemapping is only applied in the real browser console not
    // in the fake one displayed on this page.
    // Press "fork" to be able to view the sourcemapped stack in a real console.
    console.log(errorInfo.componentStack);
    console.log(captureOwnerStack());
  },
}).render(
  <App>
    <Component label="disabled" />
  </App>
);
```

/$

`SubComponent` would throw an error.
The Component Stack of that error would be

$

```
at SubComponentat fieldsetat Componentat mainat React.Suspenseat App
```

/$

However, the Owner Stack would only read

$

```
at Component
```

/$

Neither `App` nor the DOM components (e.g. `fieldset`) are considered Owners in this Stack since they didn’t contribute to “creating” the node containing `SubComponent`. `App` and DOM components only forwarded the node. `App` just rendered the `children` node as opposed to `Component` which created a node containing `SubComponent` via `<SubComponent />`.

Neither `Navigation` nor `legend` are in the stack at all since it’s only a sibling to a node containing `<SubComponent />`.

`SubComponent` is omitted because it’s already part of the callstack.

## Usage

### Enhance a custom error overlay

 $

```
import { captureOwnerStack } from "react";import { instrumentedConsoleError } from "./errorOverlay";const originalConsoleError = console.error;console.error = function patchedConsoleError(...args) {  originalConsoleError.apply(console, args);  const ownerStack = captureOwnerStack();  onConsoleError({    // Keep in mind that in a real application, console.error can be    // called with multiple arguments which you should account for.    consoleMessage: args[0],    ownerStack,  });};
```

/$

If you intercept `console.error` calls to highlight them in an error overlay, you can call `captureOwnerStack` to include the Owner Stack.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { captureOwnerStack } from "react";
import { createRoot } from "react-dom/client";
import App from './App';
import { onConsoleError } from "./errorOverlay";
import './styles.css';

const originalConsoleError = console.error;
console.error = function patchedConsoleError(...args) {
  originalConsoleError.apply(console, args);
  const ownerStack = captureOwnerStack();
  onConsoleError({
    // Keep in mind that in a real application, console.error can be
    // called with multiple arguments which you should account for.
    consoleMessage: args[0],
    ownerStack,
  });
};

const container = document.getElementById("root");
createRoot(container).render(<App />);
```

/$

## Troubleshooting

### The Owner Stack isnull

The call of `captureOwnerStack` happened outside of a React controlled function e.g. in a `setTimeout` callback, after a `fetch` call or in a custom DOM event handler. During render, Effects, React event handlers, and React error handlers (e.g. `hydrateRoot#options.onCaughtError`) Owner Stacks should be available.

In the example below, clicking the button will log an empty Owner Stack because `captureOwnerStack` was called during a custom DOM event handler. The Owner Stack must be captured earlier e.g. by moving the call of `captureOwnerStack` into the Effect body.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {captureOwnerStack, useEffect} from 'react';

export default function App() {
  useEffect(() => {
    // Should call `captureOwnerStack` here.
    function handleEvent() {
      // Calling it in a custom DOM event handler is too late.
      // The Owner Stack will be `null` at this point.
      console.log('Owner Stack: ', captureOwnerStack());
    }

    document.addEventListener('click', handleEvent);

    return () => {
      document.removeEventListener('click', handleEvent);
    }
  })

  return <button>Click me to see that Owner Stacks are not available in custom DOM event handlers</button>;
}
```

/$

### captureOwnerStackis not available

`captureOwnerStack` is only exported in development builds. It will be `undefined` in production builds. If `captureOwnerStack` is used in files that are bundled for production and development, you should conditionally access it from a namespace import.

 $

```
// Don't use named imports of `captureOwnerStack` in files that are bundled for development and production.import {captureOwnerStack} from 'react';// Use a namespace import instead and access `captureOwnerStack` conditionally.import * as React from 'react';if (process.env.NODE_ENV !== 'production') {  const ownerStack = React.captureOwnerStack();  console.log('Owner Stack', ownerStack);}
```

/$[PreviouscacheSignal](https://react.dev/reference/react/cacheSignal)[NextcreateContext](https://react.dev/reference/react/createContext)
