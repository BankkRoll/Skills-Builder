# 'use server' and more

# 'use server'

[API Reference](https://react.dev/reference/react)[Directives](https://react.dev/reference/rsc/directives)

# 'use server'

### React Server Components

`'use server'` is for use with [using React Server Components](https://react.dev/reference/rsc/server-components).

`'use server'` marks server-side functions that can be called from client-side code.

- [Reference](#reference)
  - ['use server'](#use-server)
  - [Security considerations](#security)
  - [Serializable arguments and return values](#serializable-parameters-and-return-values)
- [Usage](#usage)
  - [Server Functions in forms](#server-functions-in-forms)
  - [Calling a Server Function outside of<form>](#calling-a-server-function-outside-of-form)

---

## Reference

### 'use server'

Add `'use server'` at the top of an async function body to mark the function as callable by the client. We call these functions [Server Functions](https://react.dev/reference/rsc/server-functions).

 $

```
async function addToCart(data) {  'use server';  // ...}
```

/$

When calling a Server Function on the client, it will make a network request to the server that includes a serialized copy of any arguments passed. If the Server Function returns a value, that value will be serialized and returned to the client.

Instead of individually marking functions with `'use server'`, you can add the directive to the top of a file to mark all exports within that file as Server Functions that can be used anywhere, including imported in client code.

#### Caveats

- `'use server'` must be at the very beginning of their function or module; above any other code including imports (comments above directives are OK). They must be written with single or double quotes, not backticks.
- `'use server'` can only be used in server-side files. The resulting Server Functions can be passed to Client Components through props. See supported [types for serialization](#serializable-parameters-and-return-values).
- To import a Server Functions from [client code](https://react.dev/reference/rsc/use-client), the directive must be used on a module level.
- Because the underlying network calls are always asynchronous, `'use server'` can only be used on async functions.
- Always treat arguments to Server Functions as untrusted input and authorize any mutations. See [security considerations](#security).
- Server Functions should be called in a [Transition](https://react.dev/reference/react/useTransition). Server Functions passed to [<form action>](https://react.dev/reference/react-dom/components/form#props) or [formAction](https://react.dev/reference/react-dom/components/input#props) will automatically be called in a transition.
- Server Functions are designed for mutations that update server-side state; they are not recommended for data fetching. Accordingly, frameworks implementing Server Functions typically process one action at a time and do not have a way to cache the return value.

### Security considerations

Arguments to Server Functions are fully client-controlled. For security, always treat them as untrusted input, and make sure to validate and escape arguments as appropriate.

In any Server Function, make sure to validate that the logged-in user is allowed to perform that action.

### Under Construction

To prevent sending sensitive data from a Server Function, there are experimental taint APIs to prevent unique values and objects from being passed to client code.

See [experimental_taintUniqueValue](https://react.dev/reference/react/experimental_taintUniqueValue) and [experimental_taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference).

### Serializable arguments and return values

Since client code calls the Server Function over the network, any arguments passed will need to be serializable.

Here are supported types for Server Function arguments:

- Primitives
  - [string](https://developer.mozilla.org/en-US/docs/Glossary/String)
  - [number](https://developer.mozilla.org/en-US/docs/Glossary/Number)
  - [bigint](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt)
  - [boolean](https://developer.mozilla.org/en-US/docs/Glossary/Boolean)
  - [undefined](https://developer.mozilla.org/en-US/docs/Glossary/Undefined)
  - [null](https://developer.mozilla.org/en-US/docs/Glossary/Null)
  - [symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol), only symbols registered in the global Symbol registry via [Symbol.for](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/for)
- Iterables containing serializable values
  - [String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String)
  - [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)
  - [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
  - [Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
  - [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) and [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)
- [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)
- [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) instances
- Plain [objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object): those created with [object initializers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer), with serializable properties
- Functions that are Server Functions
- [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Notably, these are not supported:

- React elements, or [JSX](https://react.dev/learn/writing-markup-with-jsx)
- Functions, including component functions or any other function that is not a Server Function
- [Classes](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/Classes_in_JavaScript)
- Objects that are instances of any class (other than the built-ins mentioned) or objects with [a null prototype](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)
- Symbols not registered globally, ex. `Symbol('my new symbol')`
- Events from event handlers

Supported serializable return values are the same as [serializable props](https://react.dev/reference/rsc/use-client#serializable-types) for a boundary Client Component.

## Usage

### Server Functions in forms

The most common use case of Server Functions will be calling functions that mutate data. On the browser, the [HTML form element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) is the traditional approach for a user to submit a mutation. With React Server Components, React introduces first-class support for Server Functions as Actions in [forms](https://react.dev/reference/react-dom/components/form).

Here is a form that allows a user to request a username.

 $

```
// App.jsasync function requestUsername(formData) {  'use server';  const username = formData.get('username');  // ...}export default function App() {  return (    <form action={requestUsername}>      <input type="text" name="username" />      <button type="submit">Request</button>    </form>  );}
```

/$

In this example `requestUsername` is a Server Function passed to a `<form>`. When a user submits this form, there is a network request to the server function `requestUsername`. When calling a Server Function in a form, React will supply the form’s [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) as the first argument to the Server Function.

By passing a Server Function to the form `action`, React can [progressively enhance](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement) the form. This means that forms can be submitted before the JavaScript bundle is loaded.

#### Handling return values in forms

In the username request form, there might be the chance that a username is not available. `requestUsername` should tell us if it fails or not.

To update the UI based on the result of a Server Function while supporting progressive enhancement, use [useActionState](https://react.dev/reference/react/useActionState).

 $

```
// requestUsername.js'use server';export default async function requestUsername(formData) {  const username = formData.get('username');  if (canRequest(username)) {    // ...    return 'successful';  }  return 'failed';}
```

/$ $

```
// UsernameForm.js'use client';import { useActionState } from 'react';import requestUsername from './requestUsername';function UsernameForm() {  const [state, action] = useActionState(requestUsername, null, 'n/a');  return (    <>      <form action={action}>        <input type="text" name="username" />        <button type="submit">Request</button>      </form>      <p>Last submission request returned: {state}</p>    </>  );}
```

/$

Note that like most Hooks, `useActionState` can only be called in [client code](https://react.dev/reference/rsc/use-client).

### Calling a Server Function outside of<form>

Server Functions are exposed server endpoints and can be called anywhere in client code.

When using a Server Function outside a [form](https://react.dev/reference/react-dom/components/form), call the Server Function in a [Transition](https://react.dev/reference/react/useTransition), which allows you to display a loading indicator, show [optimistic state updates](https://react.dev/reference/react/useOptimistic), and handle unexpected errors. Forms will automatically wrap Server Functions in transitions.

 $

```
import incrementLike from './actions';import { useState, useTransition } from 'react';function LikeButton() {  const [isPending, startTransition] = useTransition();  const [likeCount, setLikeCount] = useState(0);  const onClick = () => {    startTransition(async () => {      const currentCount = await incrementLike();      setLikeCount(currentCount);    });  };  return (    <>      <p>Total Likes: {likeCount}</p>      <button onClick={onClick} disabled={isPending}>Like</button>;    </>  );}
```

/$ $

```
// actions.js'use server';let likeCount = 0;export default async function incrementLike() {  likeCount++;  return likeCount;}
```

/$

To read a Server Function return value, you’ll need to `await` the promise returned.

[Previous'use client'](https://react.dev/reference/rsc/use-client)

---

# Components and Hooks must be pure

[API Reference](https://react.dev/reference/react)[Overview](https://react.dev/reference/rules)

# Components and Hooks must be pure

Pure functions only perform a calculation and nothing more. It makes your code easier to understand, debug, and allows React to automatically optimize your components and Hooks correctly.

### Note

This reference page covers advanced topics and requires familiarity with the concepts covered in the [Keeping Components Pure](https://react.dev/learn/keeping-components-pure) page.

- [Why does purity matter?](#why-does-purity-matter)
- [Components and Hooks must be idempotent](#components-and-hooks-must-be-idempotent)
- [Side effects must run outside of render](#side-effects-must-run-outside-of-render)
  - [When is it okay to have mutation?](#mutation)
- [Props and state are immutable](#props-and-state-are-immutable)
  - [Don’t mutate Props](#props)
  - [Don’t mutate State](#state)
- [Return values and arguments to Hooks are immutable](#return-values-and-arguments-to-hooks-are-immutable)
- [Values are immutable after being passed to JSX](#values-are-immutable-after-being-passed-to-jsx)

### Why does purity matter?

One of the key concepts that makes React, *React* is *purity*. A pure component or hook is one that is:

- **Idempotent** – You [always get the same result every time](https://react.dev/learn/keeping-components-pure#purity-components-as-formulas) you run it with the same inputs – props, state, context for component inputs; and arguments for hook inputs.
- **Has no side effects in render** – Code with side effects should run [separately from rendering](#how-does-react-run-your-code). For example as an [event handler](https://react.dev/learn/responding-to-events) – where the user interacts with the UI and causes it to update; or as an [Effect](https://react.dev/reference/react/useEffect) – which runs after render.
- **Does not mutate non-local values**: Components and Hooks should [never modify values that aren’t created locally](#mutation) in render.

When render is kept pure, React can understand how to prioritize which updates are most important for the user to see first. This is made possible because of render purity: since components don’t have side effects [in render](#how-does-react-run-your-code), React can pause rendering components that aren’t as important to update, and only come back to them later when it’s needed.

Concretely, this means that rendering logic can be run multiple times in a way that allows React to give your user a pleasant user experience. However, if your component has an untracked side effect – like modifying the value of a global variable [during render](#how-does-react-run-your-code) – when React runs your rendering code again, your side effects will be triggered in a way that won’t match what you want. This often leads to unexpected bugs that can degrade how your users experience your app. You can see an [example of this in the Keeping Components Pure page](https://react.dev/learn/keeping-components-pure#side-effects-unintended-consequences).

#### How does React run your code?

React is declarative: you tell React *what* to render, and React will figure out *how* best to display it to your user. To do this, React has a few phases where it runs your code. You don’t need to know about all of these phases to use React well. But at a high level, you should know about what code runs in *render*, and what runs outside of it.

*Rendering* refers to calculating what the next version of your UI should look like. After rendering, [Effects](https://react.dev/reference/react/useEffect) are *flushed* (meaning they are run until there are no more left) and may update the calculation if the Effects have impacts on layout. React takes this new calculation and compares it to the calculation used to create the previous version of your UI, then *commits* just the minimum changes needed to the [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) (what your user actually sees) to catch it up to the latest version.

##### Deep Dive

#### How to tell if code runs in render

One quick heuristic to tell if code runs during render is to examine where it is: if it’s written at the top level like in the example below, there’s a good chance it runs during render.

$

```
function Dropdown() {  const selectedItems = new Set(); // created during render  // ...}
```

/$

Event handlers and Effects don’t run in render:

$

```
function Dropdown() {  const selectedItems = new Set();  const onSelect = (item) => {    // this code is in an event handler, so it's only run when the user triggers this    selectedItems.add(item);  }}
```

/$$

```
function Dropdown() {  const selectedItems = new Set();  useEffect(() => {    // this code is inside of an Effect, so it only runs after rendering    logForAnalytics(selectedItems);  }, [selectedItems]);}
```

/$

---

## Components and Hooks must be idempotent

Components must always return the same output with respect to their inputs – props, state, and context. This is known as *idempotency*. [Idempotency](https://en.wikipedia.org/wiki/Idempotence) is a term popularized in functional programming. It refers to the idea that you [always get the same result every time](https://react.dev/learn/keeping-components-pure) you run that piece of code with the same inputs.

This means that *all* code that runs [during render](#how-does-react-run-your-code) must also be idempotent in order for this rule to hold. For example, this line of code is not idempotent (and therefore, neither is the component):

 $

```
function Clock() {  const time = new Date(); // 🔴 Bad: always returns a different result!  return <span>{time.toLocaleString()}</span>}
```

/$

`new Date()` is not idempotent as it always returns the current date and changes its result every time it’s called. When you render the above component, the time displayed on the screen will stay stuck on the time that the component was rendered. Similarly, functions like `Math.random()` also aren’t idempotent, because they return different results every time they’re called, even when the inputs are the same.

This doesn’t mean you shouldn’t use non-idempotent functions like `new Date()` *at all* – you should just avoid using them [during render](#how-does-react-run-your-code). In this case, we can *synchronize* the latest date to this component using an [Effect](https://react.dev/reference/react/useEffect):

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';

function useTime() {
  // 1. Keep track of the current date's state. `useState` receives an initializer function as its
  //    initial state. It only runs once when the hook is called, so only the current date at the
  //    time the hook is called is set first.
  const [time, setTime] = useState(() => new Date());

  useEffect(() => {
    // 2. Update the current date every second using `setInterval`.
    const id = setInterval(() => {
      setTime(new Date()); // ✅ Good: non-idempotent code no longer runs in render
    }, 1000);
    // 3. Return a cleanup function so we don't leak the `setInterval` timer.
    return () => clearInterval(id);
  }, []);

  return time;
}

export default function Clock() {
  const time = useTime();
  return <span>{time.toLocaleString()}</span>;
}
```

/$

By wrapping the non-idempotent `new Date()` call in an Effect, it moves that calculation [outside of rendering](#how-does-react-run-your-code).

If you don’t need to synchronize some external state with React, you can also consider using an [event handler](https://react.dev/learn/responding-to-events) if it only needs to be updated in response to a user interaction.

---

## Side effects must run outside of render

[Side effects](https://react.dev/learn/keeping-components-pure#side-effects-unintended-consequences) should not run [in render](#how-does-react-run-your-code), as React can render components multiple times to create the best possible user experience.

### Note

Side effects are a broader term than Effects. Effects specifically refer to code that’s wrapped in `useEffect`, while a side effect is a general term for code that has any observable effect other than its primary result of returning a value to the caller.

Side effects are typically written inside of [event handlers](https://react.dev/learn/responding-to-events) or Effects. But never during render.

While render must be kept pure, side effects are necessary at some point in order for your app to do anything interesting, like showing something on the screen! The key point of this rule is that side effects should not run [in render](#how-does-react-run-your-code), as React can render components multiple times. In most cases, you’ll use [event handlers](https://react.dev/learn/responding-to-events) to handle side effects. Using an event handler explicitly tells React that this code doesn’t need to run during render, keeping render pure. If you’ve exhausted all options – and only as a last resort – you can also handle side effects using `useEffect`.

### When is it okay to have mutation?

#### Local mutation

One common example of a side effect is mutation, which in JavaScript refers to changing the value of a non-[primitive](https://developer.mozilla.org/en-US/docs/Glossary/Primitive) value. In general, while mutation is not idiomatic in React, *local* mutation is absolutely fine:

 $

```
function FriendList({ friends }) {  const items = []; // ✅ Good: locally created  for (let i = 0; i < friends.length; i++) {    const friend = friends[i];    items.push(      <Friend key={friend.id} friend={friend} />    ); // ✅ Good: local mutation is okay  }  return <section>{items}</section>;}
```

/$

There is no need to contort your code to avoid local mutation. [Array.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) could also be used here for brevity, but there is nothing wrong with creating a local array and then pushing items into it [during render](#how-does-react-run-your-code).

Even though it looks like we are mutating `items`, the key point to note is that this code only does so *locally* – the mutation isn’t “remembered” when the component is rendered again. In other words, `items` only stays around as long as the component does. Because `items` is always *recreated* every time `<FriendList />` is rendered, the component will always return the same result.

On the other hand, if `items` was created outside of the component, it holds on to its previous values and remembers changes:

 $

```
const items = []; // 🔴 Bad: created outside of the componentfunction FriendList({ friends }) {  for (let i = 0; i < friends.length; i++) {    const friend = friends[i];    items.push(      <Friend key={friend.id} friend={friend} />    ); // 🔴 Bad: mutates a value created outside of render  }  return <section>{items}</section>;}
```

/$

When `<FriendList />` runs again, we will continue appending `friends` to `items` every time that component is run, leading to multiple duplicated results. This version of `<FriendList />` has observable side effects [during render](#how-does-react-run-your-code) and **breaks the rule**.

#### Lazy initialization

Lazy initialization is also fine despite not being fully “pure”:

 $

```
function ExpenseForm() {  SuperCalculator.initializeIfNotReady(); // ✅ Good: if it doesn't affect other components  // Continue rendering...}
```

/$

#### Changing the DOM

Side effects that are directly visible to the user are not allowed in the render logic of React components. In other words, merely calling a component function shouldn’t by itself produce a change on the screen.

 $

```
function ProductDetailPage({ product }) {  document.title = product.title; // 🔴 Bad: Changes the DOM}
```

/$

One way to achieve the desired result of updating `document.title` outside of render is to [synchronize the component withdocument](https://react.dev/learn/synchronizing-with-effects).

As long as calling a component multiple times is safe and doesn’t affect the rendering of other components, React doesn’t care if it’s 100% pure in the strict functional programming sense of the word. It is more important that [components must be idempotent](https://react.dev/reference/rules/components-and-hooks-must-be-pure).

---

## Props and state are immutable

A component’s props and state are immutable [snapshots](https://react.dev/learn/state-as-a-snapshot). Never mutate them directly. Instead, pass new props down, and use the setter function from `useState`.

You can think of the props and state values as snapshots that are updated after rendering. For this reason, you don’t modify the props or state variables directly: instead you pass new props, or use the setter function provided to you to tell React that state needs to update the next time the component is rendered.

### Don’t mutate Props

Props are immutable because if you mutate them, the application will produce inconsistent output, which can be hard to debug as it may or may not work depending on the circumstances.

 $

```
function Post({ item }) {  item.url = new Url(item.url, base); // 🔴 Bad: never mutate props directly  return <Link url={item.url}>{item.title}</Link>;}
```

/$ $

```
function Post({ item }) {  const url = new Url(item.url, base); // ✅ Good: make a copy instead  return <Link url={url}>{item.title}</Link>;}
```

/$

### Don’t mutate State

`useState` returns the state variable and a setter to update that state.

 $

```
const [stateVariable, setter] = useState(0);
```

/$

Rather than updating the state variable in-place, we need to update it using the setter function that is returned by `useState`. Changing values on the state variable doesn’t cause the component to update, leaving your users with an outdated UI. Using the setter function informs React that the state has changed, and that we need to queue a re-render to update the UI.

 $

```
function Counter() {  const [count, setCount] = useState(0);  function handleClick() {    count = count + 1; // 🔴 Bad: never mutate state directly  }  return (    <button onClick={handleClick}>      You pressed me {count} times    </button>  );}
```

/$ $

```
function Counter() {  const [count, setCount] = useState(0);  function handleClick() {    setCount(count + 1); // ✅ Good: use the setter function returned by useState  }  return (    <button onClick={handleClick}>      You pressed me {count} times    </button>  );}
```

/$

---

## Return values and arguments to Hooks are immutable

Once values are passed to a hook, you should not modify them. Like props in JSX, values become immutable when passed to a hook.

 $

```
function useIconStyle(icon) {  const theme = useContext(ThemeContext);  if (icon.enabled) {    icon.className = computeStyle(icon, theme); // 🔴 Bad: never mutate hook arguments directly  }  return icon;}
```

/$ $

```
function useIconStyle(icon) {  const theme = useContext(ThemeContext);  const newIcon = { ...icon }; // ✅ Good: make a copy instead  if (icon.enabled) {    newIcon.className = computeStyle(icon, theme);  }  return newIcon;}
```

/$

One important principle in React is *local reasoning*: the ability to understand what a component or hook does by looking at its code in isolation. Hooks should be treated like “black boxes” when they are called. For example, a custom hook might have used its arguments as dependencies to memoize values inside it:

 $

```
function useIconStyle(icon) {  const theme = useContext(ThemeContext);  return useMemo(() => {    const newIcon = { ...icon };    if (icon.enabled) {      newIcon.className = computeStyle(icon, theme);    }    return newIcon;  }, [icon, theme]);}
```

/$

If you were to mutate the Hook’s arguments, the custom hook’s memoization will become incorrect,  so it’s important to avoid doing that.

 $

```
style = useIconStyle(icon);         // `style` is memoized based on `icon`icon.enabled = false;               // Bad: 🔴 never mutate hook arguments directlystyle = useIconStyle(icon);         // previously memoized result is returned
```

/$ $

```
style = useIconStyle(icon);         // `style` is memoized based on `icon`icon = { ...icon, enabled: false }; // Good: ✅ make a copy insteadstyle = useIconStyle(icon);         // new value of `style` is calculated
```

/$

Similarly, it’s important to not modify the return values of Hooks, as they may have been memoized.

---

## Values are immutable after being passed to JSX

Don’t mutate values after they’ve been used in JSX. Move the mutation to before the JSX is created.

When you use JSX in an expression, React may eagerly evaluate the JSX before the component finishes rendering. This means that mutating values after they’ve been passed to JSX can lead to outdated UIs, as React won’t know to update the component’s output.

 $

```
function Page({ colour }) {  const styles = { colour, size: "large" };  const header = <Header styles={styles} />;  styles.size = "small"; // 🔴 Bad: styles was already used in the JSX above  const footer = <Footer styles={styles} />;  return (    <>      {header}      <Content />      {footer}    </>  );}
```

/$ $

```
function Page({ colour }) {  const headerStyles = { colour, size: "large" };  const header = <Header styles={headerStyles} />;  const footerStyles = { colour, size: "small" }; // ✅ Good: we created a new value  const footer = <Footer styles={footerStyles} />;  return (    <>      {header}      <Content />      {footer}    </>  );}
```

/$[PreviousOverview](https://react.dev/reference/rules)[NextReact calls Components and Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks)

---

# React calls Components and Hooks

[API Reference](https://react.dev/reference/react)[Overview](https://react.dev/reference/rules)

# React calls Components and Hooks

React is responsible for rendering components and Hooks when necessary to optimize the user experience. It is declarative: you tell React what to render in your component’s logic, and React will figure out how best to display it to your user.

- [Never call component functions directly](#never-call-component-functions-directly)
- [Never pass around Hooks as regular values](#never-pass-around-hooks-as-regular-values)
  - [Don’t dynamically mutate a Hook](#dont-dynamically-mutate-a-hook)
  - [Don’t dynamically use Hooks](#dont-dynamically-use-hooks)

---

## Never call component functions directly

Components should only be used in JSX. Don’t call them as regular functions. React should call it.

React must decide when your component function is called [during rendering](https://react.dev/reference/rules/components-and-hooks-must-be-pure#how-does-react-run-your-code). In React, you do this using JSX.

 $

```
function BlogPost() {  return <Layout><Article /></Layout>; // ✅ Good: Only use components in JSX}
```

/$ $

```
function BlogPost() {  return <Layout>{Article()}</Layout>; // 🔴 Bad: Never call them directly}
```

/$

If a component contains Hooks, it’s easy to violate the [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) when components are called directly in a loop or conditionally.

Letting React orchestrate rendering also allows a number of benefits:

- **Components become more than functions.** React can augment them with features like *local state* through Hooks that are tied to the component’s identity in the tree.
- **Component types participate in reconciliation.** By letting React call your components, you also tell it more about the conceptual structure of your tree. For example, when you move from rendering `<Feed>` to the `<Profile>` page, React won’t attempt to re-use them.
- **React can enhance your user experience.** For example, it can let the browser do some work between component calls so that re-rendering a large component tree doesn’t block the main thread.
- **A better debugging story.** If components are first-class citizens that the library is aware of, we can build rich developer tools for introspection in development.
- **More efficient reconciliation.** React can decide exactly which components in the tree need re-rendering and skip over the ones that don’t. That makes your app faster and more snappy.

---

## Never pass around Hooks as regular values

Hooks should only be called inside of components or Hooks. Never pass it around as a regular value.

Hooks allow you to augment a component with React features. They should always be called as a function, and never passed around as a regular value. This enables *local reasoning*, or the ability for developers to understand everything a component can do by looking at that component in isolation.

Breaking this rule will cause React to not automatically optimize your component.

### Don’t dynamically mutate a Hook

Hooks should be as “static” as possible. This means you shouldn’t dynamically mutate them. For example, this means you shouldn’t write higher order Hooks:

 $

```
function ChatInput() {  const useDataWithLogging = withLogging(useData); // 🔴 Bad: don't write higher order Hooks  const data = useDataWithLogging();}
```

/$

Hooks should be immutable and not be mutated. Instead of mutating a Hook dynamically, create a static version of the Hook with the desired functionality.

 $

```
function ChatInput() {  const data = useDataWithLogging(); // ✅ Good: Create a new version of the Hook}function useDataWithLogging() {  // ... Create a new version of the Hook and inline the logic here}
```

/$

### Don’t dynamically use Hooks

Hooks should also not be dynamically used: for example, instead of doing dependency injection in a component by passing a Hook as a value:

 $

```
function ChatInput() {  return <Button useData={useDataWithLogging} /> // 🔴 Bad: don't pass Hooks as props}
```

/$

You should always inline the call of the Hook into that component and handle any logic in there.

 $

```
function ChatInput() {  return <Button />}function Button() {  const data = useDataWithLogging(); // ✅ Good: Use the Hook directly}function useDataWithLogging() {  // If there's any conditional logic to change the Hook's behavior, it should be inlined into  // the Hook}
```

/$

This way, `<Button />` is much easier to understand and debug. When Hooks are used in dynamic ways, it increases the complexity of your app greatly and inhibits local reasoning, making your team less productive in the long term. It also makes it easier to accidentally break the [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) that Hooks should not be called conditionally. If you find yourself needing to mock components for tests, it’s better to mock the server instead to respond with canned data. If possible, it’s also usually more effective to test your app with end-to-end tests.

[PreviousComponents and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure)[NextRules of Hooks](https://react.dev/reference/rules/rules-of-hooks)

---

# Rules of Hooks

[API Reference](https://react.dev/reference/react)[Overview](https://react.dev/reference/rules)

# Rules of Hooks

Hooks are defined using JavaScript functions, but they represent a special type of reusable UI logic with restrictions on where they can be called.

- [Only call Hooks at the top level](#only-call-hooks-at-the-top-level)
- [Only call Hooks from React functions](#only-call-hooks-from-react-functions)

---

## Only call Hooks at the top level

Functions whose names start with `use` are called [Hooks](https://react.dev/reference/react) in React.

**Don’t call Hooks inside loops, conditions, nested functions, ortry/catch/finallyblocks.** Instead, always use Hooks at the top level of your React function, before any early returns. You can only call Hooks while React is rendering a function component:

- ✅ Call them at the top level in the body of a [function component](https://react.dev/learn/your-first-component).
- ✅ Call them at the top level in the body of a [custom Hook](https://react.dev/learn/reusing-logic-with-custom-hooks).

 $

```
function Counter() {  // ✅ Good: top-level in a function component  const [count, setCount] = useState(0);  // ...}function useWindowWidth() {  // ✅ Good: top-level in a custom Hook  const [width, setWidth] = useState(window.innerWidth);  // ...}
```

/$

It’s **not** supported to call Hooks (functions starting with `use`) in any other cases, for example:

- 🔴 Do not call Hooks inside conditions or loops.
- 🔴 Do not call Hooks after a conditional `return` statement.
- 🔴 Do not call Hooks in event handlers.
- 🔴 Do not call Hooks in class components.
- 🔴 Do not call Hooks inside functions passed to `useMemo`, `useReducer`, or `useEffect`.
- 🔴 Do not call Hooks inside `try`/`catch`/`finally` blocks.

If you break these rules, you might see this error.

 $

```
function Bad({ cond }) {  if (cond) {    // 🔴 Bad: inside a condition (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad() {  for (let i = 0; i < 10; i++) {    // 🔴 Bad: inside a loop (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad({ cond }) {  if (cond) {    return;  }  // 🔴 Bad: after a conditional return (to fix, move it before the return!)  const theme = useContext(ThemeContext);  // ...}function Bad() {  function handleClick() {    // 🔴 Bad: inside an event handler (to fix, move it outside!)    const theme = useContext(ThemeContext);  }  // ...}function Bad() {  const style = useMemo(() => {    // 🔴 Bad: inside useMemo (to fix, move it outside!)    const theme = useContext(ThemeContext);    return createStyle(theme);  });  // ...}class Bad extends React.Component {  render() {    // 🔴 Bad: inside a class component (to fix, write a function component instead of a class!)    useEffect(() => {})    // ...  }}function Bad() {  try {    // 🔴 Bad: inside try/catch/finally block (to fix, move it outside!)    const [x, setX] = useState(0);  } catch {    const [x, setX] = useState(1);  }}
```

/$

You can use the [eslint-plugin-react-hooksplugin](https://www.npmjs.com/package/eslint-plugin-react-hooks) to catch these mistakes.

### Note

[Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) *may* call other Hooks (that’s their whole purpose). This works because custom Hooks are also supposed to only be called while a function component is rendering.

---

## Only call Hooks from React functions

Don’t call Hooks from regular JavaScript functions. Instead, you can:

✅ Call Hooks from React function components.
✅ Call Hooks from [custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks#extracting-your-own-custom-hook-from-a-component).

By following this rule, you ensure that all stateful logic in a component is clearly visible from its source code.

 $

```
function FriendList() {  const [onlineStatus, setOnlineStatus] = useOnlineStatus(); // ✅}function setOnlineStatus() { // ❌ Not a component or custom Hook!  const [onlineStatus, setOnlineStatus] = useOnlineStatus();}
```

/$[PreviousReact calls Components and Hooks](https://react.dev/reference/rules/react-calls-components-and-hooks)

---

# Rules of React

[API Reference](https://react.dev/reference/react)

# Rules of React

Just as different programming languages have their own ways of expressing concepts, React has its own idioms — or rules — for how to express patterns in a way that is easy to understand and yields high-quality applications.

- [Components and Hooks must be pure](#components-and-hooks-must-be-pure)
- [React calls Components and Hooks](#react-calls-components-and-hooks)
- [Rules of Hooks](#rules-of-hooks)

---

### Note

To learn more about expressing UIs with React, we recommend reading [Thinking in React](https://react.dev/learn/thinking-in-react).

This section describes the rules you need to follow to write idiomatic React code. Writing idiomatic React code can help you write well organized, safe, and composable applications. These properties make your app more resilient to changes and makes it easier to work with other developers, libraries, and tools.

These rules are known as the **Rules of React**. They are rules – and not just guidelines – in the sense that if they are broken, your app likely has bugs. Your code also becomes unidiomatic and harder to understand and reason about.

We strongly recommend using [Strict Mode](https://react.dev/reference/react/StrictMode) alongside React’s [ESLint plugin](https://www.npmjs.com/package/eslint-plugin-react-hooks) to help your codebase follow the Rules of React. By following the Rules of React, you’ll be able to find and address these bugs and keep your application maintainable.

---

## Components and Hooks must be pure

[Purity in Components and Hooks](https://react.dev/reference/rules/components-and-hooks-must-be-pure) is a key rule of React that makes your app predictable, easy to debug, and allows React to automatically optimize your code.

- [Components must be idempotent](https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent) – React components are assumed to always return the same output with respect to their inputs – props, state, and context.
- [Side effects must run outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#side-effects-must-run-outside-of-render) – Side effects should not run in render, as React can render components multiple times to create the best possible user experience.
- [Props and state are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#props-and-state-are-immutable) – A component’s props and state are immutable snapshots with respect to a single render. Never mutate them directly.
- [Return values and arguments to Hooks are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#return-values-and-arguments-to-hooks-are-immutable) – Once values are passed to a Hook, you should not modify them. Like props in JSX, values become immutable when passed to a Hook.
- [Values are immutable after being passed to JSX](https://react.dev/reference/rules/components-and-hooks-must-be-pure#values-are-immutable-after-being-passed-to-jsx) – Don’t mutate values after they’ve been used in JSX. Move the mutation before the JSX is created.

---

## React calls Components and Hooks

[React is responsible for rendering components and hooks when necessary to optimize the user experience.](https://react.dev/reference/rules/react-calls-components-and-hooks) It is declarative: you tell React what to render in your component’s logic, and React will figure out how best to display it to your user.

- [Never call component functions directly](https://react.dev/reference/rules/react-calls-components-and-hooks#never-call-component-functions-directly) – Components should only be used in JSX. Don’t call them as regular functions.
- [Never pass around hooks as regular values](https://react.dev/reference/rules/react-calls-components-and-hooks#never-pass-around-hooks-as-regular-values) – Hooks should only be called inside of components. Never pass it around as a regular value.

---

## Rules of Hooks

Hooks are defined using JavaScript functions, but they represent a special type of reusable UI logic with restrictions on where they can be called. You need to follow the [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) when using them.

- [Only call Hooks at the top level](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-at-the-top-level) – Don’t call Hooks inside loops, conditions, or nested functions. Instead, always use Hooks at the top level of your React function, before any early returns.
- [Only call Hooks from React functions](https://react.dev/reference/rules/rules-of-hooks#only-call-hooks-from-react-functions) – Don’t call Hooks from regular JavaScript functions.

[NextComponents and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure)
