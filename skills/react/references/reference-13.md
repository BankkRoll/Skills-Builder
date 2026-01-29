# useEffectEvent and more

# useEffectEvent

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useEffectEvent

`useEffectEvent` is a React Hook that lets you extract non-reactive logic from your Effects into a reusable function called an [Effect Event](https://react.dev/learn/separating-events-from-effects#declaring-an-effect-event).

$

```
const onSomething = useEffectEvent(callback)
```

/$

- [Reference](#reference)
  - [useEffectEvent(callback)](#useeffectevent)
- [Usage](#usage)
  - [Reading the latest props and state](#reading-the-latest-props-and-state)

## Reference

### useEffectEvent(callback)

Call `useEffectEvent` at the top level of your component to declare an Effect Event. Effect Events are functions you can call inside Effects, such as `useEffect`:

 $

```
import { useEffectEvent, useEffect } from 'react';function ChatRoom({ roomId, theme }) {  const onConnected = useEffectEvent(() => {    showNotification('Connected!', theme);  });  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.on('connected', () => {      onConnected();    });    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...}
```

/$

[See more examples below.](#usage)

#### Parameters

- `callback`: A function containing the logic for your Effect Event. When you define an Effect Event with `useEffectEvent`, the `callback` always accesses the latest values from props and state when it is invoked. This helps avoid issues with stale closures.

#### Returns

Returns an Effect Event function. You can call this function inside `useEffect`, `useLayoutEffect`, or `useInsertionEffect`.

#### Caveats

- **Only call inside Effects:** Effect Events should only be called within Effects. Define them just before the Effect that uses them. Do not pass them to other components or hooks. The [eslint-plugin-react-hooks](https://react.dev/reference/eslint-plugin-react-hooks) linter (version 6.1.1 or higher) will enforce this restriction to prevent calling Effect Events in the wrong context.
- **Not a dependency shortcut:** Do not use `useEffectEvent` to avoid specifying dependencies in your Effect’s dependency array. This can hide bugs and make your code harder to understand. Prefer explicit dependencies or use refs to compare previous values if needed.
- **Use for non-reactive logic:** Only use `useEffectEvent` to extract logic that does not depend on changing values.

---

## Usage

### Reading the latest props and state

Typically, when you access a reactive value inside an Effect, you must include it in the dependency array. This makes sure your Effect runs again whenever that value changes, which is usually the desired behavior.

But in some cases, you may want to read the most recent props or state inside an Effect without causing the Effect to re-run when those values change.

To [read the latest props or state](https://react.dev/learn/separating-events-from-effects#reading-latest-props-and-state-with-effect-events) in your Effect, without making those values reactive, include them in an Effect Event.

 $

```
import { useEffect, useContext, useEffectEvent } from 'react';function Page({ url }) {  const { items } = useContext(ShoppingCartContext);  const numberOfItems = items.length;  const onNavigate = useEffectEvent((visitedUrl) => {    logVisit(visitedUrl, numberOfItems);  });  useEffect(() => {    onNavigate(url);  }, [url]);  // ...}
```

/$

In this example, the Effect should re-run after a render when `url` changes (to log the new page visit), but it should **not** re-run when `numberOfItems` changes. By wrapping the logging logic in an Effect Event, `numberOfItems` becomes non-reactive. It’s always read from the latest value without triggering the Effect.

You can pass reactive values like `url` as arguments to the Effect Event to keep them reactive while accessing the latest non-reactive values inside the event.

[PrevioususeEffect](https://react.dev/reference/react/useEffect)[NextuseId](https://react.dev/reference/react/useId)

---

# useId

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useId

`useId` is a React Hook for generating unique IDs that can be passed to accessibility attributes.

$

```
const id = useId()
```

/$

- [Reference](#reference)
  - [useId()](#useid)
- [Usage](#usage)
  - [Generating unique IDs for accessibility attributes](#generating-unique-ids-for-accessibility-attributes)
  - [Generating IDs for several related elements](#generating-ids-for-several-related-elements)
  - [Specifying a shared prefix for all generated IDs](#specifying-a-shared-prefix-for-all-generated-ids)
  - [Using the same ID prefix on the client and the server](#using-the-same-id-prefix-on-the-client-and-the-server)

---

## Reference

### useId()

Call `useId` at the top level of your component to generate a unique ID:

 $

```
import { useId } from 'react';function PasswordField() {  const passwordHintId = useId();  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

`useId` does not take any parameters.

#### Returns

`useId` returns a unique ID string associated with this particular `useId` call in this particular component.

#### Caveats

- `useId` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.
- `useId` **should not be used to generate cache keys** for [use()](https://react.dev/reference/react/use). The ID is stable when a component is mounted but may change during rendering. Cache keys should be generated from your data.
- `useId` **should not be used to generate keys** in a list. [Keys should be generated from your data.](https://react.dev/learn/rendering-lists#where-to-get-your-key)
- `useId` currently cannot be used in [async Server Components](https://react.dev/reference/rsc/server-components#async-components-with-server-components).

---

## Usage

### Pitfall

**Do not calluseIdto generate keys in a list.** [Keys should be generated from your data.](https://react.dev/learn/rendering-lists#where-to-get-your-key)

### Generating unique IDs for accessibility attributes

Call `useId` at the top level of your component to generate a unique ID:

 $

```
import { useId } from 'react';function PasswordField() {  const passwordHintId = useId();  // ...
```

/$

You can then pass the generated ID to different attributes:

 $

```
<>  <input type="password" aria-describedby={passwordHintId} />  <p id={passwordHintId}></>
```

/$

**Let’s walk through an example to see when this is useful.**

[HTML accessibility attributes](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) like [aria-describedby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-describedby) let you specify that two tags are related to each other. For example, you can specify that an element (like an input) is described by another element (like a paragraph).

In regular HTML, you would write it like this:

 $

```
<label>  Password:  <input    type="password"    aria-describedby="password-hint"  /></label><p id="password-hint">  The password should contain at least 18 characters</p>
```

/$

However, hardcoding IDs like this is not a good practice in React. A component may be rendered more than once on the page—but IDs have to be unique! Instead of hardcoding an ID, generate a unique ID with `useId`:

 $

```
import { useId } from 'react';function PasswordField() {  const passwordHintId = useId();  return (    <>      <label>        Password:        <input          type="password"          aria-describedby={passwordHintId}        />      </label>      <p id={passwordHintId}>        The password should contain at least 18 characters      </p>    </>  );}
```

/$

Now, even if `PasswordField` appears multiple times on the screen, the generated IDs won’t clash.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useId } from 'react';

function PasswordField() {
  const passwordHintId = useId();
  return (
    <>
      <label>
        Password:
        <input
          type="password"
          aria-describedby={passwordHintId}
        />
      </label>
      <p id={passwordHintId}>
        The password should contain at least 18 characters
      </p>
    </>
  );
}

export default function App() {
  return (
    <>
      <h2>Choose password</h2>
      <PasswordField />
      <h2>Confirm password</h2>
      <PasswordField />
    </>
  );
}
```

/$

[Watch this video](https://www.youtube.com/watch?v=0dNzNcuEuOo) to see the difference in the user experience with assistive technologies.

### Pitfall

With [server rendering](https://react.dev/reference/react-dom/server), **useIdrequires an identical component tree on the server and the client**. If the trees you render on the server and the client don’t match exactly, the generated IDs won’t match.

##### Deep Dive

#### Why is useId better than an incrementing counter?

You might be wondering why `useId` is better than incrementing a global variable like `nextId++`.

The primary benefit of `useId` is that React ensures that it works with [server rendering.](https://react.dev/reference/react-dom/server) During server rendering, your components generate HTML output. Later, on the client, [hydration](https://react.dev/reference/react-dom/client/hydrateRoot) attaches your event handlers to the generated HTML. For hydration to work, the client output must match the server HTML.

This is very difficult to guarantee with an incrementing counter because the order in which the Client Components are hydrated may not match the order in which the server HTML was emitted. By calling `useId`, you ensure that hydration will work, and the output will match between the server and the client.

Inside React, `useId` is generated from the “parent path” of the calling component. This is why, if the client and the server tree are the same, the “parent path” will match up regardless of rendering order.

---

### Generating IDs for several related elements

If you need to give IDs to multiple related elements, you can call `useId` to generate a shared prefix for them:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useId } from 'react';

export default function Form() {
  const id = useId();
  return (
    <form>
      <label htmlFor={id + '-firstName'}>First Name:</label>
      <input id={id + '-firstName'} type="text" />
      <hr />
      <label htmlFor={id + '-lastName'}>Last Name:</label>
      <input id={id + '-lastName'} type="text" />
    </form>
  );
}
```

/$

This lets you avoid calling `useId` for every single element that needs a unique ID.

---

### Specifying a shared prefix for all generated IDs

If you render multiple independent React applications on a single page, pass `identifierPrefix` as an option to your [createRoot](https://react.dev/reference/react-dom/client/createRoot#parameters) or [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) calls. This ensures that the IDs generated by the two different apps never clash because every identifier generated with `useId` will start with the distinct prefix you’ve specified.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';
import App from './App.js';
import './styles.css';

const root1 = createRoot(document.getElementById('root1'), {
  identifierPrefix: 'my-first-app-'
});
root1.render(<App />);

const root2 = createRoot(document.getElementById('root2'), {
  identifierPrefix: 'my-second-app-'
});
root2.render(<App />);
```

/$

---

### Using the same ID prefix on the client and the server

If you [render multiple independent React apps on the same page](#specifying-a-shared-prefix-for-all-generated-ids), and some of these apps are server-rendered, make sure that the `identifierPrefix` you pass to the [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) call on the client side is the same as the `identifierPrefix` you pass to the [server APIs](https://react.dev/reference/react-dom/server) such as [renderToPipeableStream.](https://react.dev/reference/react-dom/server/renderToPipeableStream)

 $

```
// Serverimport { renderToPipeableStream } from 'react-dom/server';const { pipe } = renderToPipeableStream(  <App />,  { identifierPrefix: 'react-app1' });
```

/$ $

```
// Clientimport { hydrateRoot } from 'react-dom/client';const domNode = document.getElementById('root');const root = hydrateRoot(  domNode,  reactNode,  { identifierPrefix: 'react-app1' });
```

/$

You do not need to pass `identifierPrefix` if you only have one React app on the page.

[PrevioususeEffectEvent](https://react.dev/reference/react/useEffectEvent)[NextuseImperativeHandle](https://react.dev/reference/react/useImperativeHandle)

---

# useImperativeHandle

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useImperativeHandle

`useImperativeHandle` is a React Hook that lets you customize the handle exposed as a [ref.](https://react.dev/learn/manipulating-the-dom-with-refs)

$

```
useImperativeHandle(ref, createHandle, dependencies?)
```

/$

- [Reference](#reference)
  - [useImperativeHandle(ref, createHandle, dependencies?)](#useimperativehandle)
- [Usage](#usage)
  - [Exposing a custom ref handle to the parent component](#exposing-a-custom-ref-handle-to-the-parent-component)
  - [Exposing your own imperative methods](#exposing-your-own-imperative-methods)

---

## Reference

### useImperativeHandle(ref, createHandle, dependencies?)

Call `useImperativeHandle` at the top level of your component to customize the ref handle it exposes:

 $

```
import { useImperativeHandle } from 'react';function MyInput({ ref }) {  useImperativeHandle(ref, () => {    return {      // ... your methods ...    };  }, []);  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

- `ref`: The `ref` you received as a prop to the `MyInput` component.
- `createHandle`: A function that takes no arguments and returns the ref handle you want to expose. That ref handle can have any type. Usually, you will return an object with the methods you want to expose.
- **optional** `dependencies`: The list of all reactive values referenced inside of the `createHandle` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](https://react.dev/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. If a re-render resulted in a change to some dependency, or if you omitted this argument, your `createHandle` function will re-execute, and the newly created handle will be assigned to the ref.

### Note

Starting with React 19, [refis available as a prop.](https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop) In React 18 and earlier, it was necessary to get the `ref` from [forwardRef.](https://react.dev/reference/react/forwardRef)

#### Returns

`useImperativeHandle` returns `undefined`.

---

## Usage

### Exposing a custom ref handle to the parent component

To expose a DOM node to the parent element, pass in the `ref` prop to the node.

 $

```
function MyInput({ ref }) {  return <input ref={ref} />;};
```

/$

With the code above, [a ref toMyInputwill receive the<input>DOM node.](https://react.dev/learn/manipulating-the-dom-with-refs) However, you can expose a custom value instead. To customize the exposed handle, call `useImperativeHandle` at the top level of your component:

 $

```
import { useImperativeHandle } from 'react';function MyInput({ ref }) {  useImperativeHandle(ref, () => {    return {      // ... your methods ...    };  }, []);  return <input />;};
```

/$

Note that in the code above, the `ref` is no longer passed to the `<input>`.

For example, suppose you don’t want to expose the entire `<input>` DOM node, but you want to expose two of its methods: `focus` and `scrollIntoView`. To do this, keep the real browser DOM in a separate ref. Then use `useImperativeHandle` to expose a handle with only the methods that you want the parent component to call:

 $

```
import { useRef, useImperativeHandle } from 'react';function MyInput({ ref }) {  const inputRef = useRef(null);  useImperativeHandle(ref, () => {    return {      focus() {        inputRef.current.focus();      },      scrollIntoView() {        inputRef.current.scrollIntoView();      },    };  }, []);  return <input ref={inputRef} />;};
```

/$

Now, if the parent component gets a ref to `MyInput`, it will be able to call the `focus` and `scrollIntoView` methods on it. However, it will not have full access to the underlying `<input>` DOM node.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';
import MyInput from './MyInput.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
    // This won't work because the DOM node isn't exposed:
    // ref.current.style.opacity = 0.5;
  }

  return (
    <form>
      <MyInput placeholder="Enter your name" ref={ref} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

/$

---

### Exposing your own imperative methods

The methods you expose via an imperative handle don’t have to match the DOM methods exactly. For example, this `Post` component exposes a `scrollAndFocusAddComment` method via an imperative handle. This lets the parent `Page` scroll the list of comments *and* focus the input field when you click the button:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';
import Post from './Post.js';

export default function Page() {
  const postRef = useRef(null);

  function handleClick() {
    postRef.current.scrollAndFocusAddComment();
  }

  return (
    <>
      <button onClick={handleClick}>
        Write a comment
      </button>
      <Post ref={postRef} />
    </>
  );
}
```

/$

### Pitfall

**Do not overuse refs.** You should only use refs for *imperative* behaviors that you can’t express as props: for example, scrolling to a node, focusing a node, triggering an animation, selecting text, and so on.

**If you can express something as a prop, you should not use a ref.** For example, instead of exposing an imperative handle like `{ open, close }` from a `Modal` component, it is better to take `isOpen` as a prop like `<Modal isOpen={isOpen} />`. [Effects](https://react.dev/learn/synchronizing-with-effects) can help you expose imperative behaviors via props.

[PrevioususeId](https://react.dev/reference/react/useId)[NextuseInsertionEffect](https://react.dev/reference/react/useInsertionEffect)

---

# useInsertionEffect

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useInsertionEffect

### Pitfall

`useInsertionEffect` is for CSS-in-JS library authors. Unless you are working on a CSS-in-JS library and need a place to inject the styles, you probably want [useEffect](https://react.dev/reference/react/useEffect) or [useLayoutEffect](https://react.dev/reference/react/useLayoutEffect) instead.

`useInsertionEffect` allows inserting elements into the DOM before any layout Effects fire.

$

```
useInsertionEffect(setup, dependencies?)
```

/$

- [Reference](#reference)
  - [useInsertionEffect(setup, dependencies?)](#useinsertioneffect)
- [Usage](#usage)
  - [Injecting dynamic styles from CSS-in-JS libraries](#injecting-dynamic-styles-from-css-in-js-libraries)

---

## Reference

### useInsertionEffect(setup, dependencies?)

Call `useInsertionEffect` to insert styles before any Effects fire that may need to read layout:

 $

```
import { useInsertionEffect } from 'react';// Inside your CSS-in-JS libraryfunction useCSS(rule) {  useInsertionEffect(() => {    // ... inject <style> tags here ...  });  return rule;}
```

/$

[See more examples below.](#usage)

#### Parameters

- `setup`: The function with your Effect’s logic. Your setup function may also optionally return a *cleanup* function. When your component is added to the DOM, but before any layout Effects fire, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. When your component is removed from the DOM, React will run your cleanup function.
- **optional** `dependencies`: The list of all reactive values referenced inside of the `setup` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](https://react.dev/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison algorithm. If you don’t specify the dependencies at all, your Effect will re-run after every re-render of the component.

#### Returns

`useInsertionEffect` returns `undefined`.

#### Caveats

- Effects only run on the client. They don’t run during server rendering.
- You can’t update state from inside `useInsertionEffect`.
- By the time `useInsertionEffect` runs, refs are not attached yet.
- `useInsertionEffect` may run either before or after the DOM has been updated. You shouldn’t rely on the DOM being updated at any particular time.
- Unlike other types of Effects, which fire cleanup for every Effect and then setup for every Effect, `useInsertionEffect` will fire both cleanup and setup one component at a time. This results in an “interleaving” of the cleanup and setup functions.

---

## Usage

### Injecting dynamic styles from CSS-in-JS libraries

Traditionally, you would style React components using plain CSS.

 $

```
// In your JS file:<button className="success" />// In your CSS file:.success { color: green; }
```

/$

Some teams prefer to author styles directly in JavaScript code instead of writing CSS files. This usually requires using a CSS-in-JS library or a tool. There are three common approaches to CSS-in-JS:

1. Static extraction to CSS files with a compiler
2. Inline styles, e.g. `<div style={{ opacity: 1 }}>`
3. Runtime injection of `<style>` tags

If you use CSS-in-JS, we recommend a combination of the first two approaches (CSS files for static styles, inline styles for dynamic styles). **We don’t recommend runtime<style>tag injection for two reasons:**

1. Runtime injection forces the browser to recalculate the styles a lot more often.
2. Runtime injection can be very slow if it happens at the wrong time in the React lifecycle.

The first problem is not solvable, but `useInsertionEffect` helps you solve the second problem.

Call `useInsertionEffect` to insert the styles before any layout Effects fire:

 $

```
// Inside your CSS-in-JS librarylet isInserted = new Set();function useCSS(rule) {  useInsertionEffect(() => {    // As explained earlier, we don't recommend runtime injection of <style> tags.    // But if you have to do it, then it's important to do in useInsertionEffect.    if (!isInserted.has(rule)) {      isInserted.add(rule);      document.head.appendChild(getStyleForRule(rule));    }  });  return rule;}function Button() {  const className = useCSS('...');  return <div className={className} />;}
```

/$

Similarly to `useEffect`, `useInsertionEffect` does not run on the server. If you need to collect which CSS rules have been used on the server, you can do it during rendering:

 $

```
let collectedRulesSet = new Set();function useCSS(rule) {  if (typeof window === 'undefined') {    collectedRulesSet.add(rule);  }  useInsertionEffect(() => {    // ...  });  return rule;}
```

/$

[Read more about upgrading CSS-in-JS libraries with runtime injection touseInsertionEffect.](https://github.com/reactwg/react-18/discussions/110)

##### Deep Dive

#### How is this better than injecting styles during rendering or useLayoutEffect?

If you insert styles during rendering and React is processing a [non-blocking update,](https://react.dev/reference/react/useTransition#perform-non-blocking-updates-with-actions) the browser will recalculate the styles every single frame while rendering a component tree, which can be **extremely slow.**

`useInsertionEffect` is better than inserting styles during [useLayoutEffect](https://react.dev/reference/react/useLayoutEffect) or [useEffect](https://react.dev/reference/react/useEffect) because it ensures that by the time other Effects run in your components, the `<style>` tags have already been inserted. Otherwise, layout calculations in regular Effects would be wrong due to outdated styles.

[PrevioususeImperativeHandle](https://react.dev/reference/react/useImperativeHandle)[NextuseLayoutEffect](https://react.dev/reference/react/useLayoutEffect)

---

# useLayoutEffect

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useLayoutEffect

### Pitfall

`useLayoutEffect` can hurt performance. Prefer [useEffect](https://react.dev/reference/react/useEffect) when possible.

`useLayoutEffect` is a version of [useEffect](https://react.dev/reference/react/useEffect) that fires before the browser repaints the screen.

$

```
useLayoutEffect(setup, dependencies?)
```

/$

- [Reference](#reference)
  - [useLayoutEffect(setup, dependencies?)](#useinsertioneffect)
- [Usage](#usage)
  - [Measuring layout before the browser repaints the screen](#measuring-layout-before-the-browser-repaints-the-screen)
- [Troubleshooting](#troubleshooting)
  - [I’m getting an error: “useLayoutEffectdoes nothing on the server”](#im-getting-an-error-uselayouteffect-does-nothing-on-the-server)

---

## Reference

### useLayoutEffect(setup, dependencies?)

Call `useLayoutEffect` to perform the layout measurements before the browser repaints the screen:

 $

```
import { useState, useRef, useLayoutEffect } from 'react';function Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0);  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height);  }, []);  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

- `setup`: The function with your Effect’s logic. Your setup function may also optionally return a *cleanup* function. Before your [component commits](https://react.dev/learn/render-and-commit#step-3-react-commits-changes-to-the-dom), React will run your setup function. After every commit with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. Before your component is removed from the DOM, React will run your cleanup function.
- **optional** `dependencies`: The list of all reactive values referenced inside of the `setup` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](https://react.dev/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. If you omit this argument, your Effect will re-run after every commit of the component.

#### Returns

`useLayoutEffect` returns `undefined`.

#### Caveats

- `useLayoutEffect` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a component and move the Effect there.
- When Strict Mode is on, React will **run one extra development-only setup+cleanup cycle** before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, [implement the cleanup function.](https://react.dev/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development)
- If some of your dependencies are objects or functions defined inside the component, there is a risk that they will **cause the Effect to re-run more often than needed.** To fix this, remove unnecessary [object](https://react.dev/reference/react/useEffect#removing-unnecessary-object-dependencies) and [function](https://react.dev/reference/react/useEffect#removing-unnecessary-function-dependencies) dependencies. You can also [extract state updates](https://react.dev/reference/react/useEffect#updating-state-based-on-previous-state-from-an-effect) and [non-reactive logic](https://react.dev/reference/react/useEffect#reading-the-latest-props-and-state-from-an-effect) outside of your Effect.
- Effects **only run on the client.** They don’t run during server rendering.
- The code inside `useLayoutEffect` and all state updates scheduled from it **block the browser from repainting the screen.** When used excessively, this makes your app slow. When possible, prefer [useEffect.](https://react.dev/reference/react/useEffect)
- If you trigger a state update inside `useLayoutEffect`, React will execute all remaining Effects immediately including `useEffect`.

---

## Usage

### Measuring layout before the browser repaints the screen

Most components don’t need to know their position and size on the screen to decide what to render. They only return some JSX. Then the browser calculates their *layout* (position and size) and repaints the screen.

Sometimes, that’s not enough. Imagine a tooltip that appears next to some element on hover. If there’s enough space, the tooltip should appear above the element, but if it doesn’t fit, it should appear below. In order to render the tooltip at the right final position, you need to know its height (i.e. whether it fits at the top).

To do this, you need to render in two passes:

1. Render the tooltip anywhere (even with a wrong position).
2. Measure its height and decide where to place the tooltip.
3. Render the tooltip *again* in the correct place.

**All of this needs to happen before the browser repaints the screen.** You don’t want the user to see the tooltip moving. Call `useLayoutEffect` to perform the layout measurements before the browser repaints the screen:

 $

```
function Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0); // You don't know real height yet  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height); // Re-render now that you know the real height  }, []);  // ...use tooltipHeight in the rendering logic below...}
```

/$

Here’s how this works step by step:

1. `Tooltip` renders with the initial `tooltipHeight = 0`  (so the tooltip may be wrongly positioned).
2. React places it in the DOM and runs the code in `useLayoutEffect`.
3. Your `useLayoutEffect` [measures the height](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) of the tooltip content and triggers an immediate re-render.
4. `Tooltip` renders again with the real `tooltipHeight` (so the tooltip is correctly positioned).
5. React updates it in the DOM, and the browser finally displays the tooltip.

Hover over the buttons below and see how the tooltip adjusts its position depending on whether it fits:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useLayoutEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import TooltipContainer from './TooltipContainer.js';

export default function Tooltip({ children, targetRect }) {
  const ref = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  useLayoutEffect(() => {
    const { height } = ref.current.getBoundingClientRect();
    setTooltipHeight(height);
    console.log('Measured tooltip height: ' + height);
  }, []);

  let tooltipX = 0;
  let tooltipY = 0;
  if (targetRect !== null) {
    tooltipX = targetRect.left;
    tooltipY = targetRect.top - tooltipHeight;
    if (tooltipY < 0) {
      // It doesn't fit above, so place below.
      tooltipY = targetRect.bottom;
    }
  }

  return createPortal(
    <TooltipContainer x={tooltipX} y={tooltipY} contentRef={ref}>
      {children}
    </TooltipContainer>,
    document.body
  );
}
```

/$

Notice that even though the `Tooltip` component has to render in two passes (first, with `tooltipHeight` initialized to `0` and then with the real measured height), you only see the final result. This is why you need `useLayoutEffect` instead of [useEffect](https://react.dev/reference/react/useEffect) for this example. Let’s look at the difference in detail below.

#### useLayoutEffect vs useEffect

#### Example1of2:useLayoutEffectblocks the browser from repainting

React guarantees that the code inside `useLayoutEffect` and any state updates scheduled inside it will be processed **before the browser repaints the screen.** This lets you render the tooltip, measure it, and re-render the tooltip again without the user noticing the first extra render. In other words, `useLayoutEffect` blocks the browser from painting.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useLayoutEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import TooltipContainer from './TooltipContainer.js';

export default function Tooltip({ children, targetRect }) {
  const ref = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  useLayoutEffect(() => {
    const { height } = ref.current.getBoundingClientRect();
    setTooltipHeight(height);
  }, []);

  let tooltipX = 0;
  let tooltipY = 0;
  if (targetRect !== null) {
    tooltipX = targetRect.left;
    tooltipY = targetRect.top - tooltipHeight;
    if (tooltipY < 0) {
      // It doesn't fit above, so place below.
      tooltipY = targetRect.bottom;
    }
  }

  return createPortal(
    <TooltipContainer x={tooltipX} y={tooltipY} contentRef={ref}>
      {children}
    </TooltipContainer>,
    document.body
  );
}
```

/$

### Note

Rendering in two passes and blocking the browser hurts performance. Try to avoid this when you can.

---

## Troubleshooting

### I’m getting an error: “useLayoutEffectdoes nothing on the server”

The purpose of `useLayoutEffect` is to let your component [use layout information for rendering:](#measuring-layout-before-the-browser-repaints-the-screen)

1. Render the initial content.
2. Measure the layout *before the browser repaints the screen.*
3. Render the final content using the layout information you’ve read.

When you or your framework uses [server rendering](https://react.dev/reference/react-dom/server), your React app renders to HTML on the server for the initial render. This lets you show the initial HTML before the JavaScript code loads.

The problem is that on the server, there is no layout information.

In the [earlier example](#measuring-layout-before-the-browser-repaints-the-screen), the `useLayoutEffect` call in the `Tooltip` component lets it position itself correctly (either above or below content) depending on the content height. If you tried to render `Tooltip` as a part of the initial server HTML, this would be impossible to determine. On the server, there is no layout yet! So, even if you rendered it on the server, its position would “jump” on the client after the JavaScript loads and runs.

Usually, components that rely on layout information don’t need to render on the server anyway. For example, it probably doesn’t make sense to show a `Tooltip` during the initial render. It is triggered by a client interaction.

However, if you’re running into this problem, you have a few different options:

- Replace `useLayoutEffect` with [useEffect.](https://react.dev/reference/react/useEffect) This tells React that it’s okay to display the initial render result without blocking the paint (because the original HTML will become visible before your Effect runs).
- Alternatively, [mark your component as client-only.](https://react.dev/reference/react/Suspense#providing-a-fallback-for-server-errors-and-client-only-content) This tells React to replace its content up to the closest [<Suspense>](https://react.dev/reference/react/Suspense) boundary with a loading fallback (for example, a spinner or a glimmer) during server rendering.
- Alternatively, you can render a component with `useLayoutEffect` only after hydration. Keep a boolean `isMounted` state that’s initialized to `false`, and set it to `true` inside a `useEffect` call. Your rendering logic can then be like `return isMounted ? <RealContent /> : <FallbackContent />`. On the server and during the hydration, the user will see `FallbackContent` which should not call `useLayoutEffect`. Then React will replace it with `RealContent` which runs on the client only and can include `useLayoutEffect` calls.
- If you synchronize your component with an external data store and rely on `useLayoutEffect` for different reasons than measuring layout, consider [useSyncExternalStore](https://react.dev/reference/react/useSyncExternalStore) instead which [supports server rendering.](https://react.dev/reference/react/useSyncExternalStore#adding-support-for-server-rendering)

[PrevioususeInsertionEffect](https://react.dev/reference/react/useInsertionEffect)[NextuseMemo](https://react.dev/reference/react/useMemo)
