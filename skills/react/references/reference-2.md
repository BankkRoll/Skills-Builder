# set and more

# set

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# set-state-in-render

Validates against unconditionally setting state during render, which can trigger additional renders and potential infinite render loops.

## Rule Details

Calling `setState` during render unconditionally triggers another render before the current one finishes. This creates an infinite loop that crashes your app.

## Common Violations

### Invalid

 $

```
// ❌ Unconditional setState directly in renderfunction Component({value}) {  const [count, setCount] = useState(0);  setCount(value); // Infinite loop!  return <div>{count}</div>;}
```

/$

### Valid

 $

```
// ✅ Derive during renderfunction Component({items}) {  const sorted = [...items].sort(); // Just calculate it in render  return <ul>{sorted.map(/*...*/)}</ul>;}// ✅ Set state in event handlerfunction Component() {  const [count, setCount] = useState(0);  return (    <button onClick={() => setCount(count + 1)}>      {count}    </button>  );}// ✅ Derive from props instead of setting statefunction Component({user}) {  const name = user?.name || '';  const email = user?.email || '';  return <div>{name}</div>;}// ✅ Conditionally derive state from props and state from previous rendersfunction Component({ items }) {  const [isReverse, setIsReverse] = useState(false);  const [selection, setSelection] = useState(null);  const [prevItems, setPrevItems] = useState(items);  if (items !== prevItems) { // This condition makes it valid    setPrevItems(items);    setSelection(null);  }  // ...}
```

/$

## Troubleshooting

### I want to sync state to a prop

A common problem is trying to “fix” state after it renders. Suppose you want to keep a counter from exceeding a `max` prop:

 $

```
// ❌ Wrong: clamps during renderfunction Counter({max}) {  const [count, setCount] = useState(0);  if (count > max) {    setCount(max);  }  return (    <button onClick={() => setCount(count + 1)}>      {count}    </button>  );}
```

/$

As soon as `count` exceeds `max`, an infinite loop is triggered.

Instead, it’s often better to move this logic to the event (the place where the state is first set). For example, you can enforce the maximum at the moment you update state:

 $

```
// ✅ Clamp when updatingfunction Counter({max}) {  const [count, setCount] = useState(0);  const increment = () => {    setCount(current => Math.min(current + 1, max));  };  return <button onClick={increment}>{count}</button>;}
```

/$

Now the setter only runs in response to the click, React finishes the render normally, and `count` never crosses `max`.

In rare cases, you may need to adjust state based on information from previous renders. For those, follow [this pattern](https://react.dev/reference/react/useState#storing-information-from-previous-renders) of setting state conditionally.

[Previousset-state-in-effect](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect)[Nextstatic-components](https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components)

---

# static

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# static-components

Validates that components are static, not recreated every render. Components that are recreated dynamically can reset state and trigger excessive re-rendering.

## Rule Details

Components defined inside other components are recreated on every render. React sees each as a brand new component type, unmounting the old one and mounting the new one, destroying all state and DOM nodes in the process.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Component defined inside componentfunction Parent() {  const ChildComponent = () => { // New component every render!    const [count, setCount] = useState(0);    return <button onClick={() => setCount(count + 1)}>{count}</button>;  };  return <ChildComponent />; // State resets every render}// ❌ Dynamic component creationfunction Parent({type}) {  const Component = type === 'button'    ? () => <button>Click</button>    : () => <div>Text</div>;  return <Component />;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Components at module levelconst ButtonComponent = () => <button>Click</button>;const TextComponent = () => <div>Text</div>;function Parent({type}) {  const Component = type === 'button'    ? ButtonComponent  // Reference existing component    : TextComponent;  return <Component />;}
```

/$

## Troubleshooting

### I need to render different components conditionally

You might define components inside to access local state:

 $

```
// ❌ Wrong: Inner component to access parent statefunction Parent() {  const [theme, setTheme] = useState('light');  function ThemedButton() { // Recreated every render!    return (      <button className={theme}>        Click me      </button>    );  }  return <ThemedButton />;}
```

/$

Pass data as props instead:

 $

```
// ✅ Better: Pass props to static componentfunction ThemedButton({theme}) {  return (    <button className={theme}>      Click me    </button>  );}function Parent() {  const [theme, setTheme] = useState('light');  return <ThemedButton theme={theme} />;}
```

/$

### Note

If you find yourself wanting to define components inside other components to access local variables, that’s a sign you should be passing props instead. This makes components more reusable and testable.

[Previousset-state-in-render](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render)[Nextunsupported-syntax](https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax)

---

# unsupported

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# unsupported-syntax

Validates against syntax that React Compiler does not support. If you need to, you can still use this syntax outside of React, such as in a standalone utility function.

## Rule Details

React Compiler needs to statically analyze your code to apply optimizations. Features like `eval` and `with` make it impossible to statically understand what the code does at compile time, so the compiler can’t optimize components that use them.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Using eval in componentfunction Component({ code }) {  const result = eval(code); // Can't be analyzed  return <div>{result}</div>;}// ❌ Using with statementfunction Component() {  with (Math) { // Changes scope dynamically    return <div>{sin(PI / 2)}</div>;  }}// ❌ Dynamic property access with evalfunction Component({propName}) {  const value = eval(`props.${propName}`);  return <div>{value}</div>;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Use normal property accessfunction Component({propName, props}) {  const value = props[propName]; // Analyzable  return <div>{value}</div>;}// ✅ Use standard Math methodsfunction Component() {  return <div>{Math.sin(Math.PI / 2)}</div>;}
```

/$

## Troubleshooting

### I need to evaluate dynamic code

You might need to evaluate user-provided code:

 $

```
// ❌ Wrong: eval in componentfunction Calculator({expression}) {  const result = eval(expression); // Unsafe and unoptimizable  return <div>Result: {result}</div>;}
```

/$

Use a safe expression parser instead:

 $

```
// ✅ Better: Use a safe parserimport {evaluate} from 'mathjs'; // or similar libraryfunction Calculator({expression}) {  const [result, setResult] = useState(null);  const calculate = () => {    try {      // Safe mathematical expression evaluation      setResult(evaluate(expression));    } catch (error) {      setResult('Invalid expression');    }  };  return (    <div>      <button onClick={calculate}>Calculate</button>      {result && <div>Result: {result}</div>}    </div>  );}
```

/$

### Note

Never use `eval` with user input - it’s a security risk. Use dedicated parsing libraries for specific use cases like mathematical expressions, JSON parsing, or template evaluation.

[Previousstatic-components](https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components)[Nextuse-memo](https://react.dev/reference/eslint-plugin-react-hooks/lints/use-memo)

---

# use

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# use-memo

Validates that the `useMemo` hook is used with a return value. See [useMemodocs](https://react.dev/reference/react/useMemo) for more information.

## Rule Details

`useMemo` is for computing and caching expensive values, not for side effects. Without a return value, `useMemo` returns `undefined`, which defeats its purpose and likely indicates you’re using the wrong hook.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ No return valuefunction Component({ data }) {  const processed = useMemo(() => {    data.forEach(item => console.log(item));    // Missing return!  }, [data]);  return <div>{processed}</div>; // Always undefined}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Returns computed valuefunction Component({ data }) {  const processed = useMemo(() => {    return data.map(item => item * 2);  }, [data]);  return <div>{processed}</div>;}
```

/$

## Troubleshooting

### I need to run side effects when dependencies change

You might try to use `useMemo` for side effects:

   $

```
// ❌ Wrong: Side effects in useMemofunction Component({user}) {  // No return value, just side effect  useMemo(() => {    analytics.track('UserViewed', {userId: user.id});  }, [user.id]);  // Not assigned to a variable  useMemo(() => {    return analytics.track('UserViewed', {userId: user.id});  }, [user.id]);}
```

/$

If the side effect needs to happen in response to user interaction, it’s best to colocate the side effect with the event:

 $

```
// ✅ Good: Side effects in event handlersfunction Component({user}) {  const handleClick = () => {    analytics.track('ButtonClicked', {userId: user.id});    // Other click logic...  };  return <button onClick={handleClick}>Click me</button>;}
```

/$

If the side effect sychronizes React state with some external state (or vice versa), use `useEffect`:

 $

```
// ✅ Good: Synchronization in useEffectfunction Component({theme}) {  useEffect(() => {    localStorage.setItem('preferredTheme', theme);    document.body.className = theme;  }, [theme]);  return <div>Current theme: {theme}</div>;}
```

/$[Previousunsupported-syntax](https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax)

---

# eslint

[API Reference](https://react.dev/reference/react)

# eslint-plugin-react-hooks

`eslint-plugin-react-hooks` provides ESLint rules to enforce the [Rules of React](https://react.dev/reference/rules).

This plugin helps you catch violations of React’s rules at build time, ensuring your components and hooks follow React’s rules for correctness and performance. The lints cover both fundamental React patterns (exhaustive-deps and rules-of-hooks) and issues flagged by React Compiler. React Compiler diagnostics are automatically surfaced by this ESLint plugin, and can be used even if your app hasn’t adopted the compiler yet.

### Note

When the compiler reports a diagnostic, it means that the compiler was able to statically detect a pattern that is not supported or breaks the Rules of React. When it detects this, it **automatically** skips over those components and hooks, while keeping the rest of your app compiled. This ensures optimal coverage of safe optimizations that won’t break your app.

What this means for linting, is that you don’t need to fix all violations immediately. Address them at your own pace to gradually increase the number of optimized components.

## Recommended Rules

These rules are included in the `recommended` preset in `eslint-plugin-react-hooks`:

- [exhaustive-deps](https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps) - Validates that dependency arrays for React hooks contain all necessary dependencies
- [rules-of-hooks](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks) - Validates that components and hooks follow the Rules of Hooks
- [component-hook-factories](https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories) - Validates higher order functions defining nested components or hooks
- [config](https://react.dev/reference/eslint-plugin-react-hooks/lints/config) - Validates the compiler configuration options
- [error-boundaries](https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries) - Validates usage of Error Boundaries instead of try/catch for child errors
- [gating](https://react.dev/reference/eslint-plugin-react-hooks/lints/gating) - Validates configuration of gating mode
- [globals](https://react.dev/reference/eslint-plugin-react-hooks/lints/globals) - Validates against assignment/mutation of globals during render
- [immutability](https://react.dev/reference/eslint-plugin-react-hooks/lints/immutability) - Validates against mutating props, state, and other immutable values
- [incompatible-library](https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library) - Validates against usage of libraries which are incompatible with memoization
- [preserve-manual-memoization](https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization) - Validates that existing manual memoization is preserved by the compiler
- [purity](https://react.dev/reference/eslint-plugin-react-hooks/lints/purity) - Validates that components/hooks are pure by checking known-impure functions
- [refs](https://react.dev/reference/eslint-plugin-react-hooks/lints/refs) - Validates correct usage of refs, not reading/writing during render
- [set-state-in-effect](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect) - Validates against calling setState synchronously in an effect
- [set-state-in-render](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render) - Validates against setting state during render
- [static-components](https://react.dev/reference/eslint-plugin-react-hooks/lints/static-components) - Validates that components are static, not recreated every render
- [unsupported-syntax](https://react.dev/reference/eslint-plugin-react-hooks/lints/unsupported-syntax) - Validates against syntax that React Compiler does not support
- [use-memo](https://react.dev/reference/eslint-plugin-react-hooks/lints/use-memo) - Validates usage of the `useMemo` hook without a return value

[Nextexhaustive-deps](https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps)

---

# act

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# act

`act` is a test helper to apply pending React updates before making assertions.

$

```
await act(async actFn)
```

/$

To prepare a component for assertions, wrap the code rendering it and performing updates inside an `await act()` call. This makes your test run closer to how React works in the browser.

### Note

You might find using `act()` directly a bit too verbose. To avoid some of the boilerplate, you could use a library like [React Testing Library](https://testing-library.com/docs/react-testing-library/intro), whose helpers are wrapped with `act()`.

- [Reference](#reference)
  - [await act(async actFn)](#await-act-async-actfn)
- [Usage](#usage)
  - [Rendering components in tests](#rendering-components-in-tests)
  - [Dispatching events in tests](#dispatching-events-in-tests)
- [Troubleshooting](#troubleshooting)
  - [I’m getting an error: “The current testing environment is not configured to support act(…)”](#error-the-current-testing-environment-is-not-configured-to-support-act)

---

## Reference

### await act(async actFn)

When writing UI tests, tasks like rendering, user events, or data fetching can be considered as “units” of interaction with a user interface. React provides a helper called `act()` that makes sure all updates related to these “units” have been processed and applied to the DOM before you make any assertions.

The name `act` comes from the [Arrange-Act-Assert](https://wiki.c2.com/?ArrangeActAssert) pattern.

 $

```
it ('renders with button disabled', async () => {  await act(async () => {    root.render(<TestComponent />)  });  expect(container.querySelector('button')).toBeDisabled();});
```

/$

### Note

We recommend using `act` with `await` and an `async` function. Although the sync version works in many cases, it doesn’t work in all cases and due to the way React schedules updates internally, it’s difficult to predict when you can use the sync version.

We will deprecate and remove the sync version in the future.

#### Parameters

- `async actFn`: An async function wrapping renders or interactions for components being tested. Any updates triggered within the `actFn`, are added to an internal act queue, which are then flushed together to process and apply any changes to the DOM. Since it is async, React will also run any code that crosses an async boundary, and flush any updates scheduled.

#### Returns

`act` does not return anything.

## Usage

When testing a component, you can use `act` to make assertions about its output.

For example, let’s say we have this `Counter` component, the usage examples below show how to test it:

 $

```
function Counter() {  const [count, setCount] = useState(0);  const handleClick = () => {    setCount(prev => prev + 1);  }  useEffect(() => {    document.title = `You clicked ${count} times`;  }, [count]);  return (    <div>      <p>You clicked {count} times</p>      <button onClick={handleClick}>        Click me      </button>    </div>  )}
```

/$

### Rendering components in tests

To test the render output of a component, wrap the render inside `act()`:

 $

```
import {act} from 'react';import ReactDOMClient from 'react-dom/client';import Counter from './Counter';it('can render and update a counter', async () => {  container = document.createElement('div');  document.body.appendChild(container);    // ✅ Render the component inside act().  await act(() => {    ReactDOMClient.createRoot(container).render(<Counter />);  });    const button = container.querySelector('button');  const label = container.querySelector('p');  expect(label.textContent).toBe('You clicked 0 times');  expect(document.title).toBe('You clicked 0 times');});
```

/$

Here, we create a container, append it to the document, and render the `Counter` component inside `act()`. This ensures that the component is rendered and its effects are applied before making assertions.

Using `act` ensures that all updates have been applied before we make assertions.

### Dispatching events in tests

To test events, wrap the event dispatch inside `act()`:

 $

```
import {act} from 'react';import ReactDOMClient from 'react-dom/client';import Counter from './Counter';it.only('can render and update a counter', async () => {  const container = document.createElement('div');  document.body.appendChild(container);    await act( async () => {    ReactDOMClient.createRoot(container).render(<Counter />);  });    // ✅ Dispatch the event inside act().  await act(async () => {    button.dispatchEvent(new MouseEvent('click', { bubbles: true }));  });  const button = container.querySelector('button');  const label = container.querySelector('p');  expect(label.textContent).toBe('You clicked 1 times');  expect(document.title).toBe('You clicked 1 times');});
```

/$

Here, we render the component with `act`, and then dispatch the event inside another `act()`. This ensures that all updates from the event are applied before making assertions.

### Pitfall

Don’t forget that dispatching DOM events only works when the DOM container is added to the document. You can use a library like [React Testing Library](https://testing-library.com/docs/react-testing-library/intro) to reduce the boilerplate code.

## Troubleshooting

### I’m getting an error: “The current testing environment is not configured to support act(…)”

Using `act` requires setting `global.IS_REACT_ACT_ENVIRONMENT=true` in your test environment. This is to ensure that `act` is only used in the correct environment.

If you don’t set the global, you will see an error like this:

 ConsoleWarning: The current testing environment is not configured to support act(…)

To fix, add this to your global setup file for React tests:

 $

```
global.IS_REACT_ACT_ENVIRONMENT=true
```

/$

### Note

In testing frameworks like [React Testing Library](https://testing-library.com/docs/react-testing-library/intro), `IS_REACT_ACT_ENVIRONMENT` is already set for you.

[PreviousAPIs](https://react.dev/reference/react/apis)[NextaddTransitionType](https://react.dev/reference/react/addTransitionType)

---

# <Activity>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react/components)

# <Activity>

`<Activity>` lets you hide and restore the UI and internal state of its children.

$

```
<Activity mode={visibility}>  <Sidebar /></Activity>
```

/$

- [Reference](#reference)
  - [<Activity>](#activity)
- [Usage](#usage)
  - [Restoring the state of hidden components](#restoring-the-state-of-hidden-components)
  - [Restoring the DOM of hidden components](#restoring-the-dom-of-hidden-components)
  - [Pre-rendering content that’s likely to become visible](#pre-rendering-content-thats-likely-to-become-visible)
  - [Speeding up interactions during page load](#speeding-up-interactions-during-page-load)
- [Troubleshooting](#troubleshooting)
  - [My hidden components have unwanted side effects](#my-hidden-components-have-unwanted-side-effects)
  - [My hidden components have Effects that aren’t running](#my-hidden-components-have-effects-that-arent-running)

---

## Reference

### <Activity>

You can use Activity to hide part of your application:

 $

```
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

/$

When an Activity boundary is hidden, React will visually hide its children using the `display: "none"` CSS property. It will also destroy their Effects, cleaning up any active subscriptions.

While hidden, children still re-render in response to new props, albeit at a lower priority than the rest of the content.

When the boundary becomes visible again, React will reveal the children with their previous state restored, and re-create their Effects.

In this way, Activity can be thought of as a mechanism for rendering “background activity”. Rather than completely discarding content that’s likely to become visible again, you can use Activity to maintain and restore that content’s UI and internal state, while ensuring that your hidden content has no unwanted side effects.

[See more examples below.](#usage)

#### Props

- `children`: The UI you intend to show and hide.
- `mode`: A string value of either `'visible'` or `'hidden'`. If omitted, defaults to `'visible'`.

#### Caveats

- If an Activity is rendered inside of a [ViewTransition](https://react.dev/reference/react/ViewTransition), and it becomes visible as a result of an update caused by [startTransition](https://react.dev/reference/react/startTransition), it will activate the ViewTransition’s `enter` animation. If it becomes hidden, it will activate its `exit` animation.
- An Activity that just renders text will not render anything rather than rendering hidden text, because there’s no corresponding DOM element to apply visibility changes to. For example, `<Activity mode="hidden"><ComponentThatJustReturnsText /></Activity>` will not produce any output in the DOM for `const ComponentThatJustReturnsText = () => "Hello, World!"`.

---

## Usage

### Restoring the state of hidden components

In React, when you want to conditionally show or hide a component, you typically mount or unmount it based on that condition:

 $

```
{isShowingSidebar && (  <Sidebar />)}
```

/$

But unmounting a component destroys its internal state, which is not always what you want.

When you hide a component using an Activity boundary instead, React will “save” its state for later:

 $

```
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

/$

This makes it possible to hide and then later restore components in the state they were previously in.

The following example has a sidebar with an expandable section. You can press “Overview” to reveal the three subitems below it. The main app area also has a button that hides and shows the sidebar.

Try expanding the Overview section, and then toggling the sidebar closed then open:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import Sidebar from './Sidebar.js';

export default function App() {
  const [isShowingSidebar, setIsShowingSidebar] = useState(true);

  return (
    <>
      {isShowingSidebar && (
        <Sidebar />
      )}

      <main>
        <button onClick={() => setIsShowingSidebar(!isShowingSidebar)}>
          Toggle sidebar
        </button>
        <h1>Main content</h1>
      </main>
    </>
  );
}
```

/$

The Overview section always starts out collapsed. Because we unmount the sidebar when `isShowingSidebar` flips to `false`, all its internal state is lost.

This is a perfect use case for Activity. We can preserve the internal state of our sidebar, even when visually hiding it.

Let’s replace the conditional rendering of our sidebar with an Activity boundary:

 $

```
// Before{isShowingSidebar && (  <Sidebar />)}// After<Activity mode={isShowingSidebar ? 'visible' : 'hidden'}>  <Sidebar /></Activity>
```

/$

and check out the new behavior:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Activity, useState } from 'react';

import Sidebar from './Sidebar.js';

export default function App() {
  const [isShowingSidebar, setIsShowingSidebar] = useState(true);

  return (
    <>
      <Activity mode={isShowingSidebar ? 'visible' : 'hidden'}>
        <Sidebar />
      </Activity>

      <main>
        <button onClick={() => setIsShowingSidebar(!isShowingSidebar)}>
          Toggle sidebar
        </button>
        <h1>Main content</h1>
      </main>
    </>
  );
}
```

/$

Our sidebar’s internal state is now restored, without any changes to its implementation.

---

### Restoring the DOM of hidden components

Since Activity boundaries hide their children using `display: none`, their children’s DOM is also preserved when hidden. This makes them great for maintaining ephemeral state in parts of the UI that the user is likely to interact with again.

In this example, the Contact tab has a `<textarea>` where the user can enter a message. If you enter some text, change to the Home tab, then change back to the Contact tab, the draft message is lost:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Contact() {
  return (
    <div>
      <p>Send me a message!</p>

      <textarea />

      <p>You can find me online here:</p>
      <ul>
        <li>admin@mysite.com</li>
        <li>+123456789</li>
      </ul>
    </div>
  );
}
```

/$

This is because we’re fully unmounting `Contact` in `App`. When the Contact tab unmounts, the `<textarea>` element’s internal DOM state is lost.

If we switch to using an Activity boundary to show and hide the active tab, we can preserve the state of each tab’s DOM. Try entering text and switching tabs again, and you’ll see the draft message is no longer reset:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Activity, useState } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Contact from './Contact.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('contact');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'contact'}
        onClick={() => setActiveTab('contact')}
      >
        Contact
      </TabButton>

      <hr />

      <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
        <Home />
      </Activity>
      <Activity mode={activeTab === 'contact' ? 'visible' : 'hidden'}>
        <Contact />
      </Activity>
    </>
  );
}
```

/$

Again, the Activity boundary let us preserve the Contact tab’s internal state without changing its implementation.

---

### Pre-rendering content that’s likely to become visible

So far, we’ve seen how Activity can hide some content that the user has interacted with, without discarding that content’s ephemeral state.

But Activity boundaries can also be used to *prepare* content that the user has yet to see for the first time:

 $

```
<Activity mode="hidden">  <SlowComponent /></Activity>
```

/$

When an Activity boundary is hidden during its initial render, its children won’t be visible on the page — but they will *still be rendered*, albeit at a lower priority than the visible content, and without mounting their Effects.

This *pre-rendering* allows the children to load any code or data they need ahead of time, so that later, when the Activity boundary becomes visible, the children can appear faster with reduced loading times.

Let’s look at an example.

In this demo, the Posts tab loads some data. If you press it, you’ll see a Suspense fallback displayed while the data is being fetched:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, Suspense } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Posts from './Posts.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'posts'}
        onClick={() => setActiveTab('posts')}
      >
        Posts
      </TabButton>

      <hr />

      <Suspense fallback={<h1>🌀 Loading...</h1>}>
        {activeTab === 'home' && <Home />}
        {activeTab === 'posts' && <Posts />}
      </Suspense>
    </>
  );
}
```

/$

This is because `App` doesn’t mount `Posts` until its tab is active.

If we update `App` to use an Activity boundary to show and hide the active tab, `Posts` will be pre-rendered when the app first loads, allowing it to fetch its data before it becomes visible.

Try clicking the Posts tab now:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Activity, useState, Suspense } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Posts from './Posts.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'posts'}
        onClick={() => setActiveTab('posts')}
      >
        Posts
      </TabButton>

      <hr />

      <Suspense fallback={<h1>🌀 Loading...</h1>}>
        <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
          <Home />
        </Activity>
        <Activity mode={activeTab === 'posts' ? 'visible' : 'hidden'}>
          <Posts />
        </Activity>
      </Suspense>
    </>
  );
}
```

/$

`Posts` was able to prepare itself for a faster render, thanks to the hidden Activity boundary.

---

Pre-rendering components with hidden Activity boundaries is a powerful way to reduce loading times for parts of the UI that the user is likely to interact with next.

### Note

**Only Suspense-enabled data sources will be fetched during pre-rendering.** They include:

- Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming#streaming-with-suspense)
- Lazy-loading component code with [lazy](https://react.dev/reference/react/lazy)
- Reading the value of a cached Promise with [use](https://react.dev/reference/react/use)

Activity **does not** detect data that is fetched inside an Effect.

The exact way you would load data in the `Posts` component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

---

### Speeding up interactions during page load

React includes an under-the-hood performance optimization called Selective Hydration. It works by hydrating your app’s initial HTML *in chunks*, enabling some components to become interactive even if other components on the page haven’t loaded their code or data yet.

Suspense boundaries participate in Selective Hydration, because they naturally divide your component tree into units that are independent from one another:

 $

```
function Page() {  return (    <>      <MessageComposer />      <Suspense fallback="Loading chats...">        <Chats />      </Suspense>    </>  )}
```

/$

Here, `MessageComposer` can be fully hydrated during the initial render of the page, even before `Chats` is mounted and starts to fetch its data.

So by breaking up your component tree into discrete units, Suspense allows React to hydrate your app’s server-rendered HTML in chunks, enabling parts of your app to become interactive as fast as possible.

But what about pages that don’t use Suspense?

Take this tabs example:

 $

```
function Page() {  const [activeTab, setActiveTab] = useState('home');  return (    <>      <TabButton onClick={() => setActiveTab('home')}>        Home      </TabButton>      <TabButton onClick={() => setActiveTab('video')}>        Video      </TabButton>      {activeTab === 'home' && (        <Home />      )}      {activeTab === 'video' && (        <Video />      )}    </>  )}
```

/$

Here, React must hydrate the entire page all at once. If `Home` or `Video` are slower to render, they could make the tab buttons feel unresponsive during hydration.

Adding Suspense around the active tab would solve this:

 $

```
function Page() {  const [activeTab, setActiveTab] = useState('home');  return (    <>      <TabButton onClick={() => setActiveTab('home')}>        Home      </TabButton>      <TabButton onClick={() => setActiveTab('video')}>        Video      </TabButton>      <Suspense fallback={<Placeholder />}>        {activeTab === 'home' && (          <Home />        )}        {activeTab === 'video' && (          <Video />        )}      </Suspense>    </>  )}
```

/$

…but it would also change the UI, since the `Placeholder` fallback would be displayed on the initial render.

Instead, we can use Activity. Since Activity boundaries show and hide their children, they already naturally divide the component tree into independent units. And just like Suspense, this feature allows them to participate in Selective Hydration.

Let’s update our example to use Activity boundaries around the active tab:

 $

```
function Page() {  const [activeTab, setActiveTab] = useState('home');  return (    <>      <TabButton onClick={() => setActiveTab('home')}>        Home      </TabButton>      <TabButton onClick={() => setActiveTab('video')}>        Video      </TabButton>      <Activity mode={activeTab === "home" ? "visible" : "hidden"}>        <Home />      </Activity>      <Activity mode={activeTab === "video" ? "visible" : "hidden"}>        <Video />      </Activity>    </>  )}
```

/$

Now our initial server-rendered HTML looks the same as it did in the original version, but thanks to Activity, React can hydrate the tab buttons first, before it even mounts `Home` or `Video`.

---

Thus, in addition to hiding and showing content, Activity boundaries help improve your app’s performance during hydration by letting React know which parts of your page can become interactive in isolation.

And even if your page doesn’t ever hide part of its content, you can still add always-visible Activity boundaries to improve hydration performance:

 $

```
function Page() {  return (    <>      <Post />      <Activity>        <Comments />      </Activity>    </>  );}
```

/$

---

## Troubleshooting

### My hidden components have unwanted side effects

An Activity boundary hides its content by setting `display: none` on its children and cleaning up any of their Effects. So, most well-behaved React components that properly clean up their side effects will already be robust to being hidden by Activity.

But there *are* some situations where a hidden component behaves differently than an unmounted one. Most notably, since a hidden component’s DOM is not destroyed, any side effects from that DOM will persist, even after the component is hidden.

As an example, consider a `<video>` tag. Typically it doesn’t require any cleanup, because even if you’re playing a video, unmounting the tag stops the video and audio from playing in the browser. Try playing the video and then pressing Home in this demo:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Video from './Video.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('video');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'video'}
        onClick={() => setActiveTab('video')}
      >
        Video
      </TabButton>

      <hr />

      {activeTab === 'home' && <Home />}
      {activeTab === 'video' && <Video />}
    </>
  );
}
```

/$

The video stops playing as expected.

Now, let’s say we wanted to preserve the timecode where the user last watched, so that when they tab back to the video, it doesn’t start over from the beginning again.

This is a great use case for Activity!

Let’s update `App` to hide the inactive tab with a hidden Activity boundary instead of unmounting it, and see how the demo behaves this time:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Activity, useState } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Video from './Video.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('video');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'video'}
        onClick={() => setActiveTab('video')}
      >
        Video
      </TabButton>

      <hr />

      <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
        <Home />
      </Activity>
      <Activity mode={activeTab === 'video' ? 'visible' : 'hidden'}>
        <Video />
      </Activity>
    </>
  );
}
```

/$

Whoops! The video and audio continue to play even after it’s been hidden, because the tab’s `<video>` element is still in the DOM.

To fix this, we can add an Effect with a cleanup function that pauses the video:

 $

```
export default function VideoTab() {  const ref = useRef();  useLayoutEffect(() => {    const videoRef = ref.current;    return () => {      videoRef.pause()    }  }, []);  return (    <video      ref={ref}      controls      playsInline      src="..."    />  );}
```

/$

We call `useLayoutEffect` instead of `useEffect` because conceptually the clean-up code is tied to the component’s UI being visually hidden. If we used a regular effect, the code could be delayed by (say) a re-suspending Suspense boundary or a View Transition.

Let’s see the new behavior. Try playing the video, switching to the Home tab, then back to the Video tab:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Activity, useState } from 'react';
import TabButton from './TabButton.js';
import Home from './Home.js';
import Video from './Video.js';

export default function App() {
  const [activeTab, setActiveTab] = useState('video');

  return (
    <>
      <TabButton
        isActive={activeTab === 'home'}
        onClick={() => setActiveTab('home')}
      >
        Home
      </TabButton>
      <TabButton
        isActive={activeTab === 'video'}
        onClick={() => setActiveTab('video')}
      >
        Video
      </TabButton>

      <hr />

      <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
        <Home />
      </Activity>
      <Activity mode={activeTab === 'video' ? 'visible' : 'hidden'}>
        <Video />
      </Activity>
    </>
  );
}
```

/$

It works great! Our cleanup function ensures that the video stops playing if it’s ever hidden by an Activity boundary, and even better, because the `<video>` tag is never destroyed, the timecode is preserved, and the video itself doesn’t need to be initialized or downloaded again when the user switches back to keep watching it.

This is a great example of using Activity to preserve ephemeral DOM state for parts of the UI that become hidden, but the user is likely to interact with again soon.

---

Our example illustrates that for certain tags like `<video>`, unmounting and hiding have different behavior. If a component renders DOM that has a side effect, and you want to prevent that side effect when an Activity boundary hides it, add an Effect with a return function to clean it up.

The most common cases of this will be from the following tags:

- `<video>`
- `<audio>`
- `<iframe>`

Typically, though, most of your React components should already be robust to being hidden by an Activity boundary. And conceptually, you should think of “hidden” Activities as being unmounted.

To eagerly discover other Effects that don’t have proper cleanup, which is important not only for Activity boundaries but for many other behaviors in React, we recommend using [<StrictMode>](https://react.dev/reference/react/StrictMode).

---

### My hidden components have Effects that aren’t running

When an `<Activity>` is “hidden”, all its children’s Effects are cleaned up. Conceptually, the children are unmounted, but React saves their state for later. This is a feature of Activity because it means subscriptions won’t be active for hidden parts of the UI, reducing the amount of work needed for hidden content.

If you’re relying on an Effect mounting to clean up a component’s side effects, refactor the Effect to do the work in the returned cleanup function instead.

To eagerly find problematic Effects, we recommend adding [<StrictMode>](https://react.dev/reference/react/StrictMode) which will eagerly perform Activity unmounts and mounts to catch any unexpected side-effects.

[Previous<Suspense>](https://react.dev/reference/react/Suspense)[Next<ViewTransition>](https://react.dev/reference/react/ViewTransition)

---

# addTransitionType

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# addTransitionType

### Canary

**TheaddTransitionTypeAPI is currently only available in React’s Canary and Experimental channels.**

[Learn more about React’s release channels here.](https://react.dev/community/versioning-policy#all-release-channels)

`addTransitionType` lets you specify the cause of a transition.

$

```
startTransition(() => {  addTransitionType('my-transition-type');  setState(newState);});
```

/$

- [Reference](#reference)
  - [addTransitionType](#addtransitiontype)
- [Usage](#usage)
  - [Adding the cause of a transition](#adding-the-cause-of-a-transition)
  - [Customize animations using browser view transition types](#customize-animations-using-browser-view-transition-types)
  - [Customize animations usingView TransitionClass](#customize-animations-using-view-transition-class)
  - [Customize animations usingViewTransitionevents](#customize-animations-using-viewtransition-events)

---

## Reference

### addTransitionType

#### Parameters

- `type`: The type of transition to add. This can be any string.

#### Returns

`addTransitionType` does not return anything.

#### Caveats

- If multiple transitions are combined, all Transition Types are collected. You can also add more than one type to a Transition.
- Transition Types are reset after each commit. This means a `<Suspense>` fallback will associate the types after a `startTransition`, but revealing the content does not.

---

## Usage

### Adding the cause of a transition

Call `addTransitionType` inside of `startTransition` to indicate the cause of a transition:

 $

```
import { startTransition, addTransitionType } from 'react';function Submit({action) {  function handleClick() {    startTransition(() => {      addTransitionType('submit-click');      action();    });  }  return <button onClick={handleClick}>Click me</button>;}
```

/$

When you call addTransitionType inside the scope of startTransition, React will associate submit-click as one of the causes for the Transition.

Currently, Transition Types can be used to customize different animations based on what caused the Transition. You have three different ways to choose from for how to use them:

- [Customize animations using browser view transition types](#customize-animations-using-browser-view-transition-types)
- [Customize animations usingView TransitionClass](#customize-animations-using-view-transition-class)
- [Customize animations usingViewTransitionevents](#customize-animations-using-viewtransition-events)

In the future, we plan to support more use cases for using the cause of a transition.

---

### Customize animations using browser view transition types

When a [ViewTransition](https://react.dev/reference/react/ViewTransition) activates from a transition, React adds all the Transition Types as browser [view transition types](https://www.w3.org/TR/css-view-transitions-2/#active-view-transition-pseudo-examples) to the element.

This allows you to customize different animations based on CSS scopes:

 $

```
function Component() {  return (    <ViewTransition>      <div>Hello</div>    </ViewTransition>  );}startTransition(() => {  addTransitionType('my-transition-type');  setShow(true);});
```

/$ $

```
:root:active-view-transition-type(my-transition-type) {  &::view-transition-...(...) {    ...  }}
```

/$

---

### Customize animations usingView TransitionClass

You can customize animations for an activated `ViewTransition` based on type by passing an object to the View Transition Class:

 $

```
function Component() {  return (    <ViewTransition enter={{      'my-transition-type': 'my-transition-class',    }}>      <div>Hello</div>    </ViewTransition>  );}// ...startTransition(() => {  addTransitionType('my-transition-type');  setState(newState);});
```

/$

If multiple types match, then they’re joined together. If no types match then the special “default” entry is used instead. If any type has the value “none” then that wins and the ViewTransition is disabled (not assigned a name).

These can be combined with enter/exit/update/layout/share props to match based on kind of trigger and Transition Type.

 $

```
<ViewTransition enter={{  'navigation-back': 'enter-right',  'navigation-forward': 'enter-left',}}exit={{  'navigation-back': 'exit-right',  'navigation-forward': 'exit-left',}}>
```

/$

---

### Customize animations usingViewTransitionevents

You can imperatively customize animations for an activated `ViewTransition` based on type using View Transition events:

 $

```
<ViewTransition onUpdate={(inst, types) => {  if (types.includes('navigation-back')) {    ...  } else if (types.includes('navigation-forward')) {    ...  } else {    ...  }}}>
```

/$

This allows you to pick different imperative Animations based on the cause.

[Previousact](https://react.dev/reference/react/act)[Nextcache](https://react.dev/reference/react/cache)

---

# Built

[API Reference](https://react.dev/reference/react)

# Built-in React APIs

In addition to [Hooks](https://react.dev/reference/react/hooks) and [Components](https://react.dev/reference/react/components), the `react` package exports a few other APIs that are useful for defining components. This page lists all the remaining modern React APIs.

---

- [createContext](https://react.dev/reference/react/createContext) lets you define and provide context to the child components. Used with [useContext.](https://react.dev/reference/react/useContext)
- [lazy](https://react.dev/reference/react/lazy) lets you defer loading a component’s code until it’s rendered for the first time.
- [memo](https://react.dev/reference/react/memo) lets your component skip re-renders with same props. Used with [useMemo](https://react.dev/reference/react/useMemo) and [useCallback.](https://react.dev/reference/react/useCallback)
- [startTransition](https://react.dev/reference/react/startTransition) lets you mark a state update as non-urgent. Similar to [useTransition.](https://react.dev/reference/react/useTransition)
- [act](https://react.dev/reference/react/act) lets you wrap renders and interactions in tests to ensure updates have processed before making assertions.

---

## Resource APIs

*Resources* can be accessed by a component without having them as part of their state. For example, a component can read a message from a Promise or read styling information from a context.

To read a value from a resource, use this API:

- [use](https://react.dev/reference/react/use) lets you read the value of a resource like a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or [context](https://react.dev/learn/passing-data-deeply-with-context).

 $

```
function MessageComponent({ messagePromise }) {  const message = use(messagePromise);  const theme = use(ThemeContext);  // ...}
```

/$[Previous<ViewTransition>](https://react.dev/reference/react/ViewTransition)[Nextact](https://react.dev/reference/react/act)
