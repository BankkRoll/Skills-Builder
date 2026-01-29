# forwardRef and more

# forwardRef

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# forwardRef

### Deprecated

In React 19, `forwardRef` is no longer necessary. Pass `ref` as a prop instead.

`forwardRef` will be deprecated in a future release. Learn more [here](https://react.dev/blog/2024/04/25/react-19#ref-as-a-prop).

`forwardRef` lets your component expose a DOM node to the parent component with a [ref.](https://react.dev/learn/manipulating-the-dom-with-refs)

$

```
const SomeComponent = forwardRef(render)
```

/$

- [Reference](#reference)
  - [forwardRef(render)](#forwardref)
  - [renderfunction](#render-function)
- [Usage](#usage)
  - [Exposing a DOM node to the parent component](#exposing-a-dom-node-to-the-parent-component)
  - [Forwarding a ref through multiple components](#forwarding-a-ref-through-multiple-components)
  - [Exposing an imperative handle instead of a DOM node](#exposing-an-imperative-handle-instead-of-a-dom-node)
- [Troubleshooting](#troubleshooting)
  - [My component is wrapped inforwardRef, but therefto it is alwaysnull](#my-component-is-wrapped-in-forwardref-but-the-ref-to-it-is-always-null)

---

## Reference

### forwardRef(render)

Call `forwardRef()` to let your component receive a ref and forward it to a child component:

 $

```
import { forwardRef } from 'react';const MyInput = forwardRef(function MyInput(props, ref) {  // ...});
```

/$

[See more examples below.](#usage)

#### Parameters

- `render`: The render function for your component. React calls this function with the props and `ref` that your component received from its parent. The JSX you return will be the output of your component.

#### Returns

`forwardRef` returns a React component that you can render in JSX. Unlike React components defined as plain functions, a component returned by `forwardRef` is also able to receive a `ref` prop.

#### Caveats

- In Strict Mode, React will **call your render function twice** in order to [help you find accidental impurities.](https://react.dev/reference/react/useState#my-initializer-or-updater-function-runs-twice) This is development-only behavior and does not affect production. If your render function is pure (as it should be), this should not affect the logic of your component. The result from one of the calls will be ignored.

---

### renderfunction

`forwardRef` accepts a render function as an argument. React calls this function with `props` and `ref`:

 $

```
const MyInput = forwardRef(function MyInput(props, ref) {  return (    <label>      {props.label}      <input ref={ref} />    </label>  );});
```

/$

#### Parameters

- `props`: The props passed by the parent component.
- `ref`:  The `ref` attribute passed by the parent component. The `ref` can be an object or a function. If the parent component has not passed a ref, it will be `null`. You should either pass the `ref` you receive to another component, or pass it to [useImperativeHandle.](https://react.dev/reference/react/useImperativeHandle)

#### Returns

`forwardRef` returns a React component that you can render in JSX. Unlike React components defined as plain functions, the component returned by `forwardRef` is able to take a `ref` prop.

---

## Usage

### Exposing a DOM node to the parent component

By default, each component’s DOM nodes are private. However, sometimes it’s useful to expose a DOM node to the parent—for example, to allow focusing it. To opt in, wrap your component definition into `forwardRef()`:

 $

```
import { forwardRef } from 'react';const MyInput = forwardRef(function MyInput(props, ref) {  const { label, ...otherProps } = props;  return (    <label>      {label}      <input {...otherProps} />    </label>  );});
```

/$

You will receive a ref as the second argument after props. Pass it to the DOM node that you want to expose:

 $

```
import { forwardRef } from 'react';const MyInput = forwardRef(function MyInput(props, ref) {  const { label, ...otherProps } = props;  return (    <label>      {label}      <input {...otherProps} ref={ref} />    </label>  );});
```

/$

This lets the parent `Form` component access the `<input>` DOM node exposed by `MyInput`:

 $

```
function Form() {  const ref = useRef(null);  function handleClick() {    ref.current.focus();  }  return (    <form>      <MyInput label="Enter your name:" ref={ref} />      <button type="button" onClick={handleClick}>        Edit      </button>    </form>  );}
```

/$

This `Form` component [passes a ref](https://react.dev/reference/react/useRef#manipulating-the-dom-with-a-ref) to `MyInput`. The `MyInput` component *forwards* that ref to the `<input>` browser tag. As a result, the `Form` component can access that `<input>` DOM node and call [focus()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus) on it.

Keep in mind that exposing a ref to the DOM node inside your component makes it harder to change your component’s internals later. You will typically expose DOM nodes from reusable low-level components like buttons or text inputs, but you won’t do it for application-level components like an avatar or a comment.

#### Examples of forwarding a ref

#### Example1of2:Focusing a text input

Clicking the button will focus the input. The `Form` component defines a ref and passes it to the `MyInput` component. The `MyInput` component forwards that ref to the browser `<input>`. This lets the `Form` component focus the `<input>`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';
import MyInput from './MyInput.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
  }

  return (
    <form>
      <MyInput label="Enter your name:" ref={ref} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

/$

---

### Forwarding a ref through multiple components

Instead of forwarding a `ref` to a DOM node, you can forward it to your own component like `MyInput`:

 $

```
const FormField = forwardRef(function FormField(props, ref) {  // ...  return (    <>      <MyInput ref={ref} />      ...    </>  );});
```

/$

If that `MyInput` component forwards a ref to its `<input>`, a ref to `FormField` will give you that `<input>`:

 $

```
function Form() {  const ref = useRef(null);  function handleClick() {    ref.current.focus();  }  return (    <form>      <FormField label="Enter your name:" ref={ref} isRequired={true} />      <button type="button" onClick={handleClick}>        Edit      </button>    </form>  );}
```

/$

The `Form` component defines a ref and passes it to `FormField`. The `FormField` component forwards that ref to `MyInput`, which forwards it to a browser `<input>` DOM node. This is how `Form` accesses that DOM node.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';
import FormField from './FormField.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
  }

  return (
    <form>
      <FormField label="Enter your name:" ref={ref} isRequired={true} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

/$

---

### Exposing an imperative handle instead of a DOM node

Instead of exposing an entire DOM node, you can expose a custom object, called an *imperative handle,* with a more constrained set of methods. To do this, you’d need to define a separate ref to hold the DOM node:

 $

```
const MyInput = forwardRef(function MyInput(props, ref) {  const inputRef = useRef(null);  // ...  return <input {...props} ref={inputRef} />;});
```

/$

Pass the `ref` you received to [useImperativeHandle](https://react.dev/reference/react/useImperativeHandle) and specify the value you want to expose to the `ref`:

 $

```
import { forwardRef, useRef, useImperativeHandle } from 'react';const MyInput = forwardRef(function MyInput(props, ref) {  const inputRef = useRef(null);  useImperativeHandle(ref, () => {    return {      focus() {        inputRef.current.focus();      },      scrollIntoView() {        inputRef.current.scrollIntoView();      },    };  }, []);  return <input {...props} ref={inputRef} />;});
```

/$

If some component gets a ref to `MyInput`, it will only receive your `{ focus, scrollIntoView }` object instead of the DOM node. This lets you limit the information you expose about your DOM node to the minimum.

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

[Read more about using imperative handles.](https://react.dev/reference/react/useImperativeHandle)

### Pitfall

**Do not overuse refs.** You should only use refs for *imperative* behaviors that you can’t express as props: for example, scrolling to a node, focusing a node, triggering an animation, selecting text, and so on.

**If you can express something as a prop, you should not use a ref.** For example, instead of exposing an imperative handle like `{ open, close }` from a `Modal` component, it is better to take `isOpen` as a prop like `<Modal isOpen={isOpen} />`. [Effects](https://react.dev/learn/synchronizing-with-effects) can help you expose imperative behaviors via props.

---

## Troubleshooting

### My component is wrapped inforwardRef, but therefto it is alwaysnull

This usually means that you forgot to actually use the `ref` that you received.

For example, this component doesn’t do anything with its `ref`:

 $

```
const MyInput = forwardRef(function MyInput({ label }, ref) {  return (    <label>      {label}      <input />    </label>  );});
```

/$

To fix it, pass the `ref` down to a DOM node or another component that can accept a ref:

 $

```
const MyInput = forwardRef(function MyInput({ label }, ref) {  return (    <label>      {label}      <input ref={ref} />    </label>  );});
```

/$

The `ref` to `MyInput` could also be `null` if some of the logic is conditional:

 $

```
const MyInput = forwardRef(function MyInput({ label, showInput }, ref) {  return (    <label>      {label}      {showInput && <input ref={ref} />}    </label>  );});
```

/$

If `showInput` is `false`, then the ref won’t be forwarded to any node, and a ref to `MyInput` will remain empty. This is particularly easy to miss if the condition is hidden inside another component, like `Panel` in this example:

 $

```
const MyInput = forwardRef(function MyInput({ label, showInput }, ref) {  return (    <label>      {label}      <Panel isExpanded={showInput}>        <input ref={ref} />      </Panel>    </label>  );});
```

/$[PreviouscreateRef](https://react.dev/reference/react/createRef)[NextisValidElement](https://react.dev/reference/react/isValidElement)

---

# <Fragment> (<>...</>)

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react/components)

# <Fragment> (<>...</>)

`<Fragment>`, often used via `<>...</>` syntax, lets you group elements without a wrapper node.

### Canary

 Fragments can also accept refs, which enable interacting with underlying DOM nodes without adding wrapper elements. See reference and usage below.$

```
<>  <OneChild />  <AnotherChild /></>
```

/$

- [Reference](#reference)
  - [<Fragment>](#fragment)
  - [Canary onlyFragmentInstance](#fragmentinstance)
- [Usage](#usage)
  - [Returning multiple elements](#returning-multiple-elements)
  - [Assigning multiple elements to a variable](#assigning-multiple-elements-to-a-variable)
  - [Grouping elements with text](#grouping-elements-with-text)
  - [Rendering a list of Fragments](#rendering-a-list-of-fragments)
  - [Canary onlyUsing Fragment refs for DOM interaction](#using-fragment-refs-for-dom-interaction)
  - [Canary onlyTracking visibility with Fragment refs](#tracking-visibility-with-fragment-refs)
  - [Canary onlyFocus management with Fragment refs](#focus-management-with-fragment-refs)

---

## Reference

### <Fragment>

Wrap elements in `<Fragment>` to group them together in situations where you need a single element. Grouping elements in `Fragment` has no effect on the resulting DOM; it is the same as if the elements were not grouped. The empty JSX tag `<></>` is shorthand for `<Fragment></Fragment>` in most cases.

#### Props

- **optional** `key`: Fragments declared with the explicit `<Fragment>` syntax may have [keys.](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
- Canary only **optional** `ref`: A ref object (e.g. from [useRef](https://react.dev/reference/react/useRef)) or [callback function](https://react.dev/reference/react-dom/components/common#ref-callback). React provides a `FragmentInstance` as the ref value that implements methods for interacting with the DOM nodes wrapped by the Fragment.

### Canary onlyFragmentInstance

When you pass a ref to a fragment, React provides a `FragmentInstance` object with methods for interacting with the DOM nodes wrapped by the fragment:

**Event handling methods:**

- `addEventListener(type, listener, options?)`: Adds an event listener to all first-level DOM children of the Fragment.
- `removeEventListener(type, listener, options?)`: Removes an event listener from all first-level DOM children of the Fragment.
- `dispatchEvent(event)`: Dispatches an event to a virtual child of the Fragment to call any added listeners and can bubble to the DOM parent.

**Layout methods:**

- `compareDocumentPosition(otherNode)`: Compares the document position of the Fragment with another node.
  - If the Fragment has children, the native `compareDocumentPosition` value is returned.
  - Empty Fragments will attempt to compare positioning within the React tree and include `Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC`.
  - Elements that have a different relationship in the React tree and DOM tree due to portaling or other insertions are `Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC`.
- `getClientRects()`: Returns a flat array of `DOMRect` objects representing the bounding rectangles of all children.
- `getRootNode()`: Returns the root node containing the Fragment’s parent DOM node.

**Focus management methods:**

- `focus(options?)`: Focuses the first focusable DOM node in the Fragment. Focus is attempted on nested children depth-first.
- `focusLast(options?)`: Focuses the last focusable DOM node in the Fragment. Focus is attempted on nested children depth-first.
- `blur()`: Removes focus if `document.activeElement` is within the Fragment.

**Observer methods:**

- `observeUsing(observer)`: Starts observing the Fragment’s DOM children with an IntersectionObserver or ResizeObserver.
- `unobserveUsing(observer)`: Stops observing the Fragment’s DOM children with the specified observer.

#### Caveats

- If you want to pass `key` to a Fragment, you can’t use the `<>...</>` syntax. You have to explicitly import `Fragment` from `'react'` and render `<Fragment key={yourKey}>...</Fragment>`.
- React does not [reset state](https://react.dev/learn/preserving-and-resetting-state) when you go from rendering `<><Child /></>` to `[<Child />]` or back, or when you go from rendering `<><Child /></>` to `<Child />` and back. This only works a single level deep: for example, going from `<><><Child /></></>` to `<Child />` resets the state. See the precise semantics [here.](https://gist.github.com/clemmy/b3ef00f9507909429d8aa0d3ee4f986b)
- Canary only If you want to pass `ref` to a Fragment, you can’t use the `<>...</>` syntax. You have to explicitly import `Fragment` from `'react'` and render `<Fragment ref={yourRef}>...</Fragment>`.

---

## Usage

### Returning multiple elements

Use `Fragment`, or the equivalent `<>...</>` syntax, to group multiple elements together. You can use it to put multiple elements in any place where a single element can go. For example, a component can only return one element, but by using a Fragment you can group multiple elements together and then return them as a group:

 $

```
function Post() {  return (    <>      <PostTitle />      <PostBody />    </>  );}
```

/$

Fragments are useful because grouping elements with a Fragment has no effect on layout or styles, unlike if you wrapped the elements in another container like a DOM element. If you inspect this example with the browser tools, you’ll see that all `<h1>` and `<article>` DOM nodes appear as siblings without wrappers around them:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Blog() {
  return (
    <>
      <Post title="An update" body="It's been a while since I posted..." />
      <Post title="My new blog" body="I am starting a new blog!" />
    </>
  )
}

function Post({ title, body }) {
  return (
    <>
      <PostTitle title={title} />
      <PostBody body={body} />
    </>
  );
}

function PostTitle({ title }) {
  return <h1>{title}</h1>
}

function PostBody({ body }) {
  return (
    <article>
      <p>{body}</p>
    </article>
  );
}
```

/$

##### Deep Dive

#### How to write a Fragment without the special syntax?

The example above is equivalent to importing `Fragment` from React:

$

```
import { Fragment } from 'react';function Post() {  return (    <Fragment>      <PostTitle />      <PostBody />    </Fragment>  );}
```

/$

Usually you won’t need this unless you need to [pass akeyto yourFragment.](#rendering-a-list-of-fragments)

---

### Assigning multiple elements to a variable

Like any other element, you can assign Fragment elements to variables, pass them as props, and so on:

 $

```
function CloseDialog() {  const buttons = (    <>      <OKButton />      <CancelButton />    </>  );  return (    <AlertDialog buttons={buttons}>      Are you sure you want to leave this page?    </AlertDialog>  );}
```

/$

---

### Grouping elements with text

You can use `Fragment` to group text together with components:

 $

```
function DateRangePicker({ start, end }) {  return (    <>      From      <DatePicker date={start} />      to      <DatePicker date={end} />    </>  );}
```

/$

---

### Rendering a list of Fragments

Here’s a situation where you need to write `Fragment` explicitly instead of using the `<></>` syntax. When you [render multiple elements in a loop](https://react.dev/learn/rendering-lists), you need to assign a `key` to each element. If the elements within the loop are Fragments, you need to use the normal JSX element syntax in order to provide the `key` attribute:

 $

```
function Blog() {  return posts.map(post =>    <Fragment key={post.id}>      <PostTitle title={post.title} />      <PostBody body={post.body} />    </Fragment>  );}
```

/$

You can inspect the DOM to verify that there are no wrapper elements around the Fragment children:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Fragment } from 'react';

const posts = [
  { id: 1, title: 'An update', body: "It's been a while since I posted..." },
  { id: 2, title: 'My new blog', body: 'I am starting a new blog!' }
];

export default function Blog() {
  return posts.map(post =>
    <Fragment key={post.id}>
      <PostTitle title={post.title} />
      <PostBody body={post.body} />
    </Fragment>
  );
}

function PostTitle({ title }) {
  return <h1>{title}</h1>
}

function PostBody({ body }) {
  return (
    <article>
      <p>{body}</p>
    </article>
  );
}
```

/$

---

### Canary onlyUsing Fragment refs for DOM interaction

Fragment refs allow you to interact with the DOM nodes wrapped by a Fragment without adding extra wrapper elements. This is useful for event handling, visibility tracking, focus management, and replacing deprecated patterns like `ReactDOM.findDOMNode()`.

 $

```
import { Fragment } from 'react';function ClickableFragment({ children, onClick }) {  return (    <Fragment ref={fragmentInstance => {      fragmentInstance.addEventListener('click', handleClick);      return () => fragmentInstance.removeEventListener('click', handleClick);    }}>      {children}    </Fragment>  );}
```

/$

---

### Canary onlyTracking visibility with Fragment refs

Fragment refs are useful for visibility tracking and intersection observation. This enables you to monitor when content becomes visible without requiring the child Components to expose refs:

 $

```
import { Fragment, useRef, useLayoutEffect } from 'react';function VisibilityObserverFragment({ threshold = 0.5, onVisibilityChange, children }) {  const fragmentRef = useRef(null);  useLayoutEffect(() => {    const observer = new IntersectionObserver(      (entries) => {        onVisibilityChange(entries.some(entry => entry.isIntersecting))      },      { threshold }    );        fragmentRef.current.observeUsing(observer);    return () => fragmentRef.current.unobserveUsing(observer);  }, [threshold, onVisibilityChange]);  return (    <Fragment ref={fragmentRef}>      {children}    </Fragment>  );}function MyComponent() {  const handleVisibilityChange = (isVisible) => {    console.log('Component is', isVisible ? 'visible' : 'hidden');  };  return (    <VisibilityObserverFragment onVisibilityChange={handleVisibilityChange}>      <SomeThirdPartyComponent />      <AnotherComponent />    </VisibilityObserverFragment>  );}
```

/$

This pattern is an alternative to Effect-based visibility logging, which is an anti-pattern in most cases. Relying on Effects alone does not guarantee that the rendered Component is observable by the user.

---

### Canary onlyFocus management with Fragment refs

Fragment refs provide focus management methods that work across all DOM nodes within the Fragment:

 $

```
import { Fragment, useRef } from 'react';function FocusFragment({ children }) {  return (    <Fragment ref={(fragmentInstance) => fragmentInstance?.focus()}>      {children}    </Fragment>  );}
```

/$

The `focus()` method focuses the first focusable element within the Fragment, while `focusLast()` focuses the last focusable element.

[PreviousComponents](https://react.dev/reference/react/components)[Next<Profiler>](https://react.dev/reference/react/Profiler)

---

# Built

[API Reference](https://react.dev/reference/react)

# Built-in React Hooks

*Hooks* let you use different React features from your components. You can either use the built-in Hooks or combine them to build your own. This page lists all built-in Hooks in React.

---

## State Hooks

*State* lets a component [“remember” information like user input.](https://react.dev/learn/state-a-components-memory) For example, a form component can use state to store the input value, while an image gallery component can use state to store the selected image index.

To add state to a component, use one of these Hooks:

- [useState](https://react.dev/reference/react/useState) declares a state variable that you can update directly.
- [useReducer](https://react.dev/reference/react/useReducer) declares a state variable with the update logic inside a [reducer function.](https://react.dev/learn/extracting-state-logic-into-a-reducer)

 $

```
function ImageGallery() {  const [index, setIndex] = useState(0);  // ...
```

/$

---

## Context Hooks

*Context* lets a component [receive information from distant parents without passing it as props.](https://react.dev/learn/passing-props-to-a-component) For example, your app’s top-level component can pass the current UI theme to all components below, no matter how deep.

- [useContext](https://react.dev/reference/react/useContext) reads and subscribes to a context.

 $

```
function Button() {  const theme = useContext(ThemeContext);  // ...
```

/$

---

## Ref Hooks

*Refs* let a component [hold some information that isn’t used for rendering,](https://react.dev/learn/referencing-values-with-refs) like a DOM node or a timeout ID. Unlike with state, updating a ref does not re-render your component. Refs are an “escape hatch” from the React paradigm. They are useful when you need to work with non-React systems, such as the built-in browser APIs.

- [useRef](https://react.dev/reference/react/useRef) declares a ref. You can hold any value in it, but most often it’s used to hold a DOM node.
- [useImperativeHandle](https://react.dev/reference/react/useImperativeHandle) lets you customize the ref exposed by your component. This is rarely used.

 $

```
function Form() {  const inputRef = useRef(null);  // ...
```

/$

---

## Effect Hooks

*Effects* let a component [connect to and synchronize with external systems.](https://react.dev/learn/synchronizing-with-effects) This includes dealing with network, browser DOM, animations, widgets written using a different UI library, and other non-React code.

- [useEffect](https://react.dev/reference/react/useEffect) connects a component to an external system.

 $

```
function ChatRoom({ roomId }) {  useEffect(() => {    const connection = createConnection(roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);  // ...
```

/$

Effects are an “escape hatch” from the React paradigm. Don’t use Effects to orchestrate the data flow of your application. If you’re not interacting with an external system, [you might not need an Effect.](https://react.dev/learn/you-might-not-need-an-effect)

There are two rarely used variations of `useEffect` with differences in timing:

- [useLayoutEffect](https://react.dev/reference/react/useLayoutEffect) fires before the browser repaints the screen. You can measure layout here.
- [useInsertionEffect](https://react.dev/reference/react/useInsertionEffect) fires before React makes changes to the DOM. Libraries can insert dynamic CSS here.

---

## Performance Hooks

A common way to optimize re-rendering performance is to skip unnecessary work. For example, you can tell React to reuse a cached calculation or to skip a re-render if the data has not changed since the previous render.

To skip calculations and unnecessary re-rendering, use one of these Hooks:

- [useMemo](https://react.dev/reference/react/useMemo) lets you cache the result of an expensive calculation.
- [useCallback](https://react.dev/reference/react/useCallback) lets you cache a function definition before passing it down to an optimized component.

 $

```
function TodoList({ todos, tab, theme }) {  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  // ...}
```

/$

Sometimes, you can’t skip re-rendering because the screen actually needs to update. In that case, you can improve performance by separating blocking updates that must be synchronous (like typing into an input) from non-blocking updates which don’t need to block the user interface (like updating a chart).

To prioritize rendering, use one of these Hooks:

- [useTransition](https://react.dev/reference/react/useTransition) lets you mark a state transition as non-blocking and allow other updates to interrupt it.
- [useDeferredValue](https://react.dev/reference/react/useDeferredValue) lets you defer updating a non-critical part of the UI and let other parts update first.

---

## Other Hooks

These Hooks are mostly useful to library authors and aren’t commonly used in the application code.

- [useDebugValue](https://react.dev/reference/react/useDebugValue) lets you customize the label React DevTools displays for your custom Hook.
- [useId](https://react.dev/reference/react/useId) lets a component associate a unique ID with itself. Typically used with accessibility APIs.
- [useSyncExternalStore](https://react.dev/reference/react/useSyncExternalStore) lets a component subscribe to an external store.

- [useActionState](https://react.dev/reference/react/useActionState) allows you to manage state of actions.

---

## Your own Hooks

You can also [define your own custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks#extracting-your-own-custom-hook-from-a-component) as JavaScript functions.

[PreviousOverview](https://react.dev/reference/react)[NextuseActionState](https://react.dev/reference/react/useActionState)

---

# isValidElement

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# isValidElement

`isValidElement` checks whether a value is a React element.

$

```
const isElement = isValidElement(value)
```

/$

- [Reference](#reference)
  - [isValidElement(value)](#isvalidelement)
- [Usage](#usage)
  - [Checking if something is a React element](#checking-if-something-is-a-react-element)

---

## Reference

### isValidElement(value)

Call `isValidElement(value)` to check whether `value` is a React element.

 $

```
import { isValidElement, createElement } from 'react';// ✅ React elementsconsole.log(isValidElement(<p />)); // trueconsole.log(isValidElement(createElement('p'))); // true// ❌ Not React elementsconsole.log(isValidElement(25)); // falseconsole.log(isValidElement('Hello')); // falseconsole.log(isValidElement({ age: 42 })); // false
```

/$

[See more examples below.](#usage)

#### Parameters

- `value`: The `value` you want to check. It can be any a value of any type.

#### Returns

`isValidElement` returns `true` if the `value` is a React element. Otherwise, it returns `false`.

#### Caveats

- **OnlyJSX tagsand objects returned bycreateElementare considered to be React elements.** For example, even though a number like `42` is a valid React *node* (and can be returned from a component), it is not a valid React element. Arrays and portals created with [createPortal](https://react.dev/reference/react-dom/createPortal) are also *not* considered to be React elements.

---

## Usage

### Checking if something is a React element

Call `isValidElement` to check if some value is a *React element.*

React elements are:

- Values produced by writing a [JSX tag](https://react.dev/learn/writing-markup-with-jsx)
- Values produced by calling [createElement](https://react.dev/reference/react/createElement)

For React elements, `isValidElement` returns `true`:

 $

```
import { isValidElement, createElement } from 'react';// ✅ JSX tags are React elementsconsole.log(isValidElement(<p />)); // trueconsole.log(isValidElement(<MyComponent />)); // true// ✅ Values returned by createElement are React elementsconsole.log(isValidElement(createElement('p'))); // trueconsole.log(isValidElement(createElement(MyComponent))); // true
```

/$

Any other values, such as strings, numbers, or arbitrary objects and arrays, are not React elements.

For them, `isValidElement` returns `false`:

 $

```
// ❌ These are *not* React elementsconsole.log(isValidElement(null)); // falseconsole.log(isValidElement(25)); // falseconsole.log(isValidElement('Hello')); // falseconsole.log(isValidElement({ age: 42 })); // falseconsole.log(isValidElement([<div />, <div />])); // falseconsole.log(isValidElement(MyComponent)); // false
```

/$

It is very uncommon to need `isValidElement`. It’s mostly useful if you’re calling another API that *only* accepts elements (like [cloneElement](https://react.dev/reference/react/cloneElement) does) and you want to avoid an error when your argument is not a React element.

Unless you have some very specific reason to add an `isValidElement` check, you probably don’t need it.

##### Deep Dive

#### React elements vs React nodes

When you write a component, you can return any kind of *React node* from it:

$

```
function MyComponent() {  // ... you can return any React node ...}
```

/$

A React node can be:

- A React element created like `<div />` or `createElement('div')`
- A portal created with [createPortal](https://react.dev/reference/react-dom/createPortal)
- A string
- A number
- `true`, `false`, `null`, or `undefined` (which are not displayed)
- An array of other React nodes

**NoteisValidElementchecks whether the argument is aReact element,not whether it’s a React node.** For example, `42` is not a valid React element. However, it is a perfectly valid React node:

$

```
function MyComponent() {  return 42; // It's ok to return a number from component}
```

/$

This is why you shouldn’t use `isValidElement` as a way to check whether something can be rendered.

[PreviousforwardRef](https://react.dev/reference/react/forwardRef)[NextPureComponent](https://react.dev/reference/react/PureComponent)

---

# lazy

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# lazy

`lazy` lets you defer loading component’s code until it is rendered for the first time.

$

```
const SomeComponent = lazy(load)
```

/$

- [Reference](#reference)
  - [lazy(load)](#lazy)
  - [loadfunction](#load)
- [Usage](#usage)
  - [Lazy-loading components with Suspense](#suspense-for-code-splitting)
- [Troubleshooting](#troubleshooting)
  - [Mylazycomponent’s state gets reset unexpectedly](#my-lazy-components-state-gets-reset-unexpectedly)

---

## Reference

### lazy(load)

Call `lazy` outside your components to declare a lazy-loaded React component:

 $

```
import { lazy } from 'react';const MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));
```

/$

[See more examples below.](#usage)

#### Parameters

- `load`: A function that returns a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or another *thenable* (a Promise-like object with a `then` method). React will not call `load` until the first time you attempt to render the returned component. After React first calls `load`, it will wait for it to resolve, and then render the resolved value’s `.default` as a React component. Both the returned Promise and the Promise’s resolved value will be cached, so React will not call `load` more than once. If the Promise rejects, React will `throw` the rejection reason for the nearest Error Boundary to handle.

#### Returns

`lazy` returns a React component you can render in your tree. While the code for the lazy component is still loading, attempting to render it will *suspend.* Use [<Suspense>](https://react.dev/reference/react/Suspense) to display a loading indicator while it’s loading.

---

### loadfunction

#### Parameters

`load` receives no parameters.

#### Returns

You need to return a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) or some other *thenable* (a Promise-like object with a `then` method). It needs to eventually resolve to an object whose `.default` property is a valid React component type, such as a function, [memo](https://react.dev/reference/react/memo), or a [forwardRef](https://react.dev/reference/react/forwardRef) component.

---

## Usage

### Lazy-loading components with Suspense

Usually, you import components with the static [import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) declaration:

 $

```
import MarkdownPreview from './MarkdownPreview.js';
```

/$

To defer loading this component’s code until it’s rendered for the first time, replace this import with:

 $

```
import { lazy } from 'react';const MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));
```

/$

This code relies on [dynamicimport(),](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import) which might require support from your bundler or framework. Using this pattern requires that the lazy component you’re importing was exported as the `default` export.

Now that your component’s code loads on demand, you also need to specify what should be displayed while it is loading. You can do this by wrapping the lazy component or any of its parents into a [<Suspense>](https://react.dev/reference/react/Suspense) boundary:

 $

```
<Suspense fallback={<Loading />}>  <h2>Preview</h2>  <MarkdownPreview /></Suspense>
```

/$

In this example, the code for `MarkdownPreview` won’t be loaded until you attempt to render it. If `MarkdownPreview` hasn’t loaded yet, `Loading` will be shown in its place. Try ticking the checkbox:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, Suspense, lazy } from 'react';
import Loading from './Loading.js';

const MarkdownPreview = lazy(() => delayForDemo(import('./MarkdownPreview.js')));

export default function MarkdownEditor() {
  const [showPreview, setShowPreview] = useState(false);
  const [markdown, setMarkdown] = useState('Hello, **world**!');
  return (
    <>
      <textarea value={markdown} onChange={e => setMarkdown(e.target.value)} />
      <label>
        <input type="checkbox" checked={showPreview} onChange={e => setShowPreview(e.target.checked)} />
        Show preview
      </label>
      <hr />
      {showPreview && (
        <Suspense fallback={<Loading />}>
          <h2>Preview</h2>
          <MarkdownPreview markdown={markdown} />
        </Suspense>
      )}
    </>
  );
}

// Add a fixed delay so you can see the loading state
function delayForDemo(promise) {
  return new Promise(resolve => {
    setTimeout(resolve, 2000);
  }).then(() => promise);
}
```

/$

This demo loads with an artificial delay. The next time you untick and tick the checkbox, `Preview` will be cached, so there will be no loading state. To see the loading state again, click “Reset” on the sandbox.

[Learn more about managing loading states with Suspense.](https://react.dev/reference/react/Suspense)

---

## Troubleshooting

### Mylazycomponent’s state gets reset unexpectedly

Do not declare `lazy` components *inside* other components:

 $

```
import { lazy } from 'react';function Editor() {  // 🔴 Bad: This will cause all state to be reset on re-renders  const MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));  // ...}
```

/$

Instead, always declare them at the top level of your module:

 $

```
import { lazy } from 'react';// ✅ Good: Declare lazy components outside of your componentsconst MarkdownPreview = lazy(() => import('./MarkdownPreview.js'));function Editor() {  // ...}
```

/$[PreviouscreateContext](https://react.dev/reference/react/createContext)[Nextmemo](https://react.dev/reference/react/memo)

---

# Legacy React APIs

[API Reference](https://react.dev/reference/react)

# Legacy React APIs

These APIs are exported from the `react` package, but they are not recommended for use in newly written code. See the linked individual API pages for the suggested alternatives.

---

## Legacy APIs

- [Children](https://react.dev/reference/react/Children) lets you manipulate and transform the JSX received as the `children` prop. [See alternatives.](https://react.dev/reference/react/Children#alternatives)
- [cloneElement](https://react.dev/reference/react/cloneElement) lets you create a React element using another element as a starting point. [See alternatives.](https://react.dev/reference/react/cloneElement#alternatives)
- [Component](https://react.dev/reference/react/Component) lets you define a React component as a JavaScript class. [See alternatives.](https://react.dev/reference/react/Component#alternatives)
- [createElement](https://react.dev/reference/react/createElement) lets you create a React element. Typically, you’ll use JSX instead.
- [createRef](https://react.dev/reference/react/createRef) creates a ref object which can contain arbitrary value. [See alternatives.](https://react.dev/reference/react/createRef#alternatives)
- [forwardRef](https://react.dev/reference/react/forwardRef) lets your component expose a DOM node to parent component with a [ref.](https://react.dev/learn/manipulating-the-dom-with-refs)
- [isValidElement](https://react.dev/reference/react/isValidElement) checks whether a value is a React element. Typically used with [cloneElement.](https://react.dev/reference/react/cloneElement)
- [PureComponent](https://react.dev/reference/react/PureComponent) is similar to [Component,](https://react.dev/reference/react/Component) but it skip re-renders with same props. [See alternatives.](https://react.dev/reference/react/PureComponent#alternatives)

---

## Removed APIs

These APIs were removed in React 19:

- [createFactory](https://18.react.dev/reference/react/createFactory): use JSX instead.
- Class Components: [static contextTypes](https://18.react.dev//reference/react/Component#static-contexttypes): use [static contextType](#static-contexttype) instead.
- Class Components: [static childContextTypes](https://18.react.dev//reference/react/Component#static-childcontexttypes): use [static contextType](#static-contexttype) instead.
- Class Components: [static getChildContext](https://18.react.dev//reference/react/Component#getchildcontext): use [Context](https://react.dev/reference/react/createContext#provider) instead.
- Class Components: [static propTypes](https://18.react.dev//reference/react/Component#static-proptypes): use a type system like [TypeScript](https://www.typescriptlang.org/) instead.
- Class Components: [this.refs](https://18.react.dev//reference/react/Component#refs): use [createRef](https://react.dev/reference/react/createRef) instead.

[NextChildren](https://react.dev/reference/react/Children)
