# Built and more

# Built

[API Reference](https://react.dev/reference/react)

# Built-in React Components

React exposes a few built-in components that you can use in your JSX.

---

## Built-in components

- [<Fragment>](https://react.dev/reference/react/Fragment), alternatively written as `<>...</>`, lets you group multiple JSX nodes together.
- [<Profiler>](https://react.dev/reference/react/Profiler) lets you measure rendering performance of a React tree programmatically.
- [<Suspense>](https://react.dev/reference/react/Suspense) lets you display a fallback while the child components are loading.
- [<StrictMode>](https://react.dev/reference/react/StrictMode) enables extra development-only checks that help you find bugs early.
- [<Activity>](https://react.dev/reference/react/Activity) lets you hide and restore the UI and internal state of its children.

---

## Your own components

You can also [define your own components](https://react.dev/learn/your-first-component) as JavaScript functions.

[PrevioususeTransition](https://react.dev/reference/react/useTransition)[Next<Fragment> (<>)](https://react.dev/reference/react/Fragment)

---

# createContext

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# createContext

`createContext` lets you create a [context](https://react.dev/learn/passing-data-deeply-with-context) that components can provide or read.

$

```
const SomeContext = createContext(defaultValue)
```

/$

- [Reference](#reference)
  - [createContext(defaultValue)](#createcontext)
  - [SomeContextProvider](#provider)
  - [SomeContext.Consumer](#consumer)
- [Usage](#usage)
  - [Creating context](#creating-context)
  - [Importing and exporting context from a file](#importing-and-exporting-context-from-a-file)
- [Troubleshooting](#troubleshooting)
  - [I can’t find a way to change the context value](#i-cant-find-a-way-to-change-the-context-value)

---

## Reference

### createContext(defaultValue)

Call `createContext` outside of any components to create a context.

 $

```
import { createContext } from 'react';const ThemeContext = createContext('light');
```

/$

[See more examples below.](#usage)

#### Parameters

- `defaultValue`: The value that you want the context to have when there is no matching context provider in the tree above the component that reads context. If you don’t have any meaningful default value, specify `null`. The default value is meant as a “last resort” fallback. It is static and never changes over time.

#### Returns

`createContext` returns a context object.

**The context object itself does not hold any information.** It represents *which* context other components read or provide. Typically, you will use [SomeContext](#provider) in components above to specify the context value, and call [useContext(SomeContext)](https://react.dev/reference/react/useContext) in components below to read it. The context object has a few properties:

- `SomeContext` lets you provide the context value to components.
- `SomeContext.Consumer` is an alternative and rarely used way to read the context value.
- `SomeContext.Provider` is a legacy way to provide the context value before React 19.

---

### SomeContextProvider

Wrap your components into a context provider to specify the value of this context for all components inside:

 $

```
function App() {  const [theme, setTheme] = useState('light');  // ...  return (    <ThemeContext value={theme}>      <Page />    </ThemeContext>  );}
```

/$

### Note

Starting in React 19, you can render `<SomeContext>` as a provider.

In older versions of React, use `<SomeContext.Provider>`.

#### Props

- `value`: The value that you want to pass to all the components reading this context inside this provider, no matter how deep. The context value can be of any type. A component calling [useContext(SomeContext)](https://react.dev/reference/react/useContext) inside of the provider receives the `value` of the innermost corresponding context provider above it.

---

### SomeContext.Consumer

Before `useContext` existed, there was an older way to read context:

 $

```
function Button() {  // 🟡 Legacy way (not recommended)  return (    <ThemeContext.Consumer>      {theme => (        <button className={theme} />      )}    </ThemeContext.Consumer>  );}
```

/$

Although this older way still works, **newly written code should read context withuseContext()instead:**

 $

```
function Button() {  // ✅ Recommended way  const theme = useContext(ThemeContext);  return <button className={theme} />;}
```

/$

#### Props

- `children`: A function. React will call the function you pass with the current context value determined by the same algorithm as [useContext()](https://react.dev/reference/react/useContext) does, and render the result you return from this function. React will also re-run this function and update the UI whenever the context from the parent components changes.

---

## Usage

### Creating context

Context lets components [pass information deep down](https://react.dev/learn/passing-data-deeply-with-context) without explicitly passing props.

Call `createContext` outside any components to create one or more contexts.

 $

```
import { createContext } from 'react';const ThemeContext = createContext('light');const AuthContext = createContext(null);
```

/$

`createContext` returns a context object. Components can read context by passing it to [useContext()](https://react.dev/reference/react/useContext):

 $

```
function Button() {  const theme = useContext(ThemeContext);  // ...}function Profile() {  const currentUser = useContext(AuthContext);  // ...}
```

/$

By default, the values they receive will be the default values you have specified when creating the contexts. However, by itself this isn’t useful because the default values never change.

Context is useful because you can **provide other, dynamic values from your components:**

 $

```
function App() {  const [theme, setTheme] = useState('dark');  const [currentUser, setCurrentUser] = useState({ name: 'Taylor' });  // ...  return (    <ThemeContext value={theme}>      <AuthContext value={currentUser}>        <Page />      </AuthContext>    </ThemeContext>  );}
```

/$

Now the `Page` component and any components inside it, no matter how deep, will “see” the passed context values. If the passed context values change, React will re-render the components reading the context as well.

[Read more about reading and providing context and see examples.](https://react.dev/reference/react/useContext)

---

### Importing and exporting context from a file

Often, components in different files will need access to the same context. This is why it’s common to declare contexts in a separate file. Then you can use the [exportstatement](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export) to make context available for other files:

 $

```
// Contexts.jsimport { createContext } from 'react';export const ThemeContext = createContext('light');export const AuthContext = createContext(null);
```

/$

Components declared in other files can then use the [import](https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/import) statement to read or provide this context:

 $

```
// Button.jsimport { ThemeContext } from './Contexts.js';function Button() {  const theme = useContext(ThemeContext);  // ...}
```

/$ $

```
// App.jsimport { ThemeContext, AuthContext } from './Contexts.js';function App() {  // ...  return (    <ThemeContext value={theme}>      <AuthContext value={currentUser}>        <Page />      </AuthContext>    </ThemeContext>  );}
```

/$

This works similar to [importing and exporting components.](https://react.dev/learn/importing-and-exporting-components)

---

## Troubleshooting

### I can’t find a way to change the context value

Code like this specifies the *default* context value:

 $

```
const ThemeContext = createContext('light');
```

/$

This value never changes. React only uses this value as a fallback if it can’t find a matching provider above.

To make context change over time, [add state and wrap components in a context provider.](https://react.dev/reference/react/useContext#updating-data-passed-via-context)

[PreviouscaptureOwnerStack](https://react.dev/reference/react/captureOwnerStack)[Nextlazy](https://react.dev/reference/react/lazy)

---

# createElement

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# createElement

`createElement` lets you create a React element. It serves as an alternative to writing [JSX.](https://react.dev/learn/writing-markup-with-jsx)

$

```
const element = createElement(type, props, ...children)
```

/$

- [Reference](#reference)
  - [createElement(type, props, ...children)](#createelement)
- [Usage](#usage)
  - [Creating an element without JSX](#creating-an-element-without-jsx)

---

## Reference

### createElement(type, props, ...children)

Call `createElement` to create a React element with the given `type`, `props`, and `children`.

 $

```
import { createElement } from 'react';function Greeting({ name }) {  return createElement(    'h1',    { className: 'greeting' },    'Hello'  );}
```

/$

[See more examples below.](#usage)

#### Parameters

- `type`: The `type` argument must be a valid React component type. For example, it could be a tag name string (such as `'div'` or `'span'`), or a React component (a function, a class, or a special component like [Fragment](https://react.dev/reference/react/Fragment)).
- `props`: The `props` argument must either be an object or `null`. If you pass `null`, it will be treated the same as an empty object. React will create an element with props matching the `props` you have passed. Note that `ref` and `key` from your `props` object are special and will *not* be available as `element.props.ref` and `element.props.key` on the returned `element`. They will be available as `element.ref` and `element.key`.
- **optional** `...children`: Zero or more child nodes. They can be any React nodes, including React elements, strings, numbers, [portals](https://react.dev/reference/react-dom/createPortal), empty nodes (`null`, `undefined`, `true`, and `false`), and arrays of React nodes.

#### Returns

`createElement` returns a React element object with a few properties:

- `type`: The `type` you have passed.
- `props`: The `props` you have passed except for `ref` and `key`.
- `ref`: The `ref` you have passed. If missing, `null`.
- `key`: The `key` you have passed, coerced to a string. If missing, `null`.

Usually, you’ll return the element from your component or make it a child of another element. Although you may read the element’s properties, it’s best to treat every element as opaque after it’s created, and only render it.

#### Caveats

- You must **treat React elements and their props asimmutable** and never change their contents after creation. In development, React will [freeze](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze) the returned element and its `props` property shallowly to enforce this.
- When you use JSX, **you must start a tag with a capital letter to render your own custom component.** In other words, `<Something />` is equivalent to `createElement(Something)`, but `<something />` (lowercase) is equivalent to `createElement('something')` (note it’s a string, so it will be treated as a built-in HTML tag).
- You should only **pass children as multiple arguments tocreateElementif they are all statically known,** like `createElement('h1', {}, child1, child2, child3)`. If your children are dynamic, pass the entire array as the third argument: `createElement('ul', {}, listItems)`. This ensures that React will [warn you about missingkeys](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key) for any dynamic lists. For static lists this is not necessary because they never reorder.

---

## Usage

### Creating an element without JSX

If you don’t like [JSX](https://react.dev/learn/writing-markup-with-jsx) or can’t use it in your project, you can use `createElement` as an alternative.

To create an element without JSX, call `createElement` with some type, props, and children:

 $

```
import { createElement } from 'react';function Greeting({ name }) {  return createElement(    'h1',    { className: 'greeting' },    'Hello ',    createElement('i', null, name),    '. Welcome!'  );}
```

/$

The children are optional, and you can pass as many as you need (the example above has three children). This code will display a `<h1>` header with a greeting. For comparison, here is the same example rewritten with JSX:

 $

```
function Greeting({ name }) {  return (    <h1 className="greeting">      Hello <i>{name}</i>. Welcome!    </h1>  );}
```

/$

To render your own React component, pass a function like `Greeting` as the type instead of a string like `'h1'`:

 $

```
export default function App() {  return createElement(Greeting, { name: 'Taylor' });}
```

/$

With JSX, it would look like this:

 $

```
export default function App() {  return <Greeting name="Taylor" />;}
```

/$

Here is a complete example written with `createElement`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createElement } from 'react';

function Greeting({ name }) {
  return createElement(
    'h1',
    { className: 'greeting' },
    'Hello ',
    createElement('i', null, name),
    '. Welcome!'
  );
}

export default function App() {
  return createElement(
    Greeting,
    { name: 'Taylor' }
  );
}
```

/$

And here is the same example written using JSX:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Greeting({ name }) {
  return (
    <h1 className="greeting">
      Hello <i>{name}</i>. Welcome!
    </h1>
  );
}

export default function App() {
  return <Greeting name="Taylor" />;
}
```

/$

Both coding styles are fine, so you can use whichever one you prefer for your project. The main benefit of using JSX compared to `createElement` is that it’s easy to see which closing tag corresponds to which opening tag.

##### Deep Dive

#### What is a React element, exactly?

An element is a lightweight description of a piece of the user interface. For example, both `<Greeting name="Taylor" />` and `createElement(Greeting, { name: 'Taylor' })` produce an object like this:

$

```
// Slightly simplified{  type: Greeting,  props: {    name: 'Taylor'  },  key: null,  ref: null,}
```

/$

**Note that creating this object does not render theGreetingcomponent or create any DOM elements.**

A React element is more like a description—an instruction for React to later render the `Greeting` component. By returning this object from your `App` component, you tell React what to do next.

Creating elements is extremely cheap so you don’t need to try to optimize or avoid it.

[PreviousComponent](https://react.dev/reference/react/Component)[NextcreateRef](https://react.dev/reference/react/createRef)

---

# createFactory

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# createFactory

### Deprecated

This API will be removed in a future major version of React. [See the alternatives.](#alternatives)

`createFactory` lets you create a function that produces React elements of a given type.

$

```
const factory = createFactory(type)
```

/$

- [Reference](#reference)
  - [createFactory(type)](#createfactory)
- [Usage](#usage)
  - [Creating React elements with a factory](#creating-react-elements-with-a-factory)
- [Alternatives](#alternatives)
  - [CopyingcreateFactoryinto your project](#copying-createfactory-into-your-project)
  - [ReplacingcreateFactorywithcreateElement](#replacing-createfactory-with-createelement)
  - [ReplacingcreateFactorywith JSX](#replacing-createfactory-with-jsx)

---

## Reference

### createFactory(type)

Call `createFactory(type)` to create a factory function which produces React elements of a given `type`.

 $

```
import { createFactory } from 'react';const button = createFactory('button');
```

/$

Then you can use it to create React elements without JSX:

 $

```
export default function App() {  return button({    onClick: () => {      alert('Clicked!')    }  }, 'Click me');}
```

/$

[See more examples below.](#usage)

#### Parameters

- `type`: The `type` argument must be a valid React component type. For example, it could be a tag name string (such as `'div'` or `'span'`), or a React component (a function, a class, or a special component like [Fragment](https://react.dev/reference/react/Fragment)).

#### Returns

Returns a factory function. That factory function receives a `props` object as the first argument, followed by a list of `...children` arguments, and returns a React element with the given `type`, `props` and `children`.

---

## Usage

### Creating React elements with a factory

Although most React projects use [JSX](https://react.dev/learn/writing-markup-with-jsx) to describe the user interface, JSX is not required. In the past, `createFactory` used to be one of the ways you could describe the user interface without JSX.

Call `createFactory` to create a *factory function* for a specific element type like `'button'`:

 $

```
import { createFactory } from 'react';const button = createFactory('button');
```

/$

Calling that factory function will produce React elements with the props and children you have provided:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createFactory } from 'react';

const button = createFactory('button');

export default function App() {
  return button({
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

/$

This is how `createFactory` was used as an alternative to JSX. However, `createFactory` is deprecated, and you should not call `createFactory` in any new code. See how to migrate away from `createFactory` below.

---

## Alternatives

### CopyingcreateFactoryinto your project

If your project has many `createFactory` calls, copy this `createFactory.js` implementation into your project:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createFactory } from './createFactory.js';

const button = createFactory('button');

export default function App() {
  return button({
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

/$

This lets you keep all of your code unchanged except the imports.

---

### ReplacingcreateFactorywithcreateElement

If you have a few `createFactory` calls that you don’t mind porting manually, and you don’t want to use JSX, you can replace every call a factory function with a [createElement](https://react.dev/reference/react/createElement) call. For example, you can replace this code:

 $

```
import { createFactory } from 'react';const button = createFactory('button');export default function App() {  return button({    onClick: () => {      alert('Clicked!')    }  }, 'Click me');}
```

/$

with this code:

 $

```
import { createElement } from 'react';export default function App() {  return createElement('button', {    onClick: () => {      alert('Clicked!')    }  }, 'Click me');}
```

/$

Here is a complete example of using React without JSX:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createElement } from 'react';

export default function App() {
  return createElement('button', {
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

/$

---

### ReplacingcreateFactorywith JSX

Finally, you can use JSX instead of `createFactory`. This is the most common way to use React:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function App() {
  return (
    <button onClick={() => {
      alert('Clicked!');
    }}>
      Click me
    </button>
  );
};
```

/$

### Pitfall

Sometimes, your existing code might pass some variable as a `type` instead of a constant like `'button'`:

$

```
function Heading({ isSubheading, ...props }) {  const type = isSubheading ? 'h2' : 'h1';  const factory = createFactory(type);  return factory(props);}
```

/$

To do the same in JSX, you need to rename your variable to start with an uppercase letter like `Type`:

$

```
function Heading({ isSubheading, ...props }) {  const Type = isSubheading ? 'h2' : 'h1';  return <Type {...props} />;}
```

/$

Otherwise React will interpret `<type>` as a built-in HTML tag because it is lowercase.

[PreviouscreateElement](https://react.dev/reference/react/createElement)[NextcreateRef](https://react.dev/reference/react/createRef)

---

# createRef

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# createRef

### Pitfall

`createRef` is mostly used for [class components.](https://react.dev/reference/react/Component) Function components typically rely on [useRef](https://react.dev/reference/react/useRef) instead.

`createRef` creates a [ref](https://react.dev/learn/referencing-values-with-refs) object which can contain arbitrary value.

$

```
class MyInput extends Component {  inputRef = createRef();  // ...}
```

/$

- [Reference](#reference)
  - [createRef()](#createref)
- [Usage](#usage)
  - [Declaring a ref in a class component](#declaring-a-ref-in-a-class-component)
- [Alternatives](#alternatives)
  - [Migrating from a class withcreateRefto a function withuseRef](#migrating-from-a-class-with-createref-to-a-function-with-useref)

---

## Reference

### createRef()

Call `createRef` to declare a [ref](https://react.dev/learn/referencing-values-with-refs) inside a [class component.](https://react.dev/reference/react/Component)

 $

```
import { createRef, Component } from 'react';class MyComponent extends Component {  intervalRef = createRef();  inputRef = createRef();  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

`createRef` takes no parameters.

#### Returns

`createRef` returns an object with a single property:

- `current`: Initially, it’s set to the `null`. You can later set it to something else. If you pass the ref object to React as a `ref` attribute to a JSX node, React will set its `current` property.

#### Caveats

- `createRef` always returns a *different* object. It’s equivalent to writing `{ current: null }` yourself.
- In a function component, you probably want [useRef](https://react.dev/reference/react/useRef) instead which always returns the same object.
- `const ref = useRef()` is equivalent to `const [ref, _] = useState(() => createRef(null))`.

---

## Usage

### Declaring a ref in a class component

To declare a ref inside a [class component,](https://react.dev/reference/react/Component) call `createRef` and assign its result to a class field:

 $

```
import { Component, createRef } from 'react';class Form extends Component {  inputRef = createRef();  // ...}
```

/$

If you now pass `ref={this.inputRef}` to an `<input>` in your JSX, React will populate `this.inputRef.current` with the input DOM node. For example, here is how you make a button that focuses the input:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Component, createRef } from 'react';

export default class Form extends Component {
  inputRef = createRef();

  handleClick = () => {
    this.inputRef.current.focus();
  }

  render() {
    return (
      <>
        <input ref={this.inputRef} />
        <button onClick={this.handleClick}>
          Focus the input
        </button>
      </>
    );
  }
}
```

/$

### Pitfall

`createRef` is mostly used for [class components.](https://react.dev/reference/react/Component) Function components typically rely on [useRef](https://react.dev/reference/react/useRef) instead.

---

## Alternatives

### Migrating from a class withcreateRefto a function withuseRef

We recommend using function components instead of [class components](https://react.dev/reference/react/Component) in new code. If you have some existing class components using `createRef`, here is how you can convert them. This is the original code:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Component, createRef } from 'react';

export default class Form extends Component {
  inputRef = createRef();

  handleClick = () => {
    this.inputRef.current.focus();
  }

  render() {
    return (
      <>
        <input ref={this.inputRef} />
        <button onClick={this.handleClick}>
          Focus the input
        </button>
      </>
    );
  }
}
```

/$

When you [convert this component from a class to a function,](https://react.dev/reference/react/Component#alternatives) replace calls to `createRef` with calls to [useRef:](https://react.dev/reference/react/useRef)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

/$[PreviouscreateElement](https://react.dev/reference/react/createElement)[NextforwardRef](https://react.dev/reference/react/forwardRef)

---

# experimental_taintObjectReference

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# experimental_taintObjectReference

### Experimental Feature

**This API is experimental and is not available in a stable version of React yet.**

You can try it by upgrading React packages to the most recent experimental version:

- `react@experimental`
- `react-dom@experimental`
- `eslint-plugin-react-hooks@experimental`

Experimental versions of React may contain bugs. Don’t use them in production.

This API is only available inside React Server Components.

`taintObjectReference` lets you prevent a specific object instance from being passed to a Client Component like a `user` object.

$

```
experimental_taintObjectReference(message, object);
```

/$

To prevent passing a key, hash or token, see [taintUniqueValue](https://react.dev/reference/react/experimental_taintUniqueValue).

- [Reference](#reference)
  - [taintObjectReference(message, object)](#taintobjectreference)
- [Usage](#usage)
  - [Prevent user data from unintentionally reaching the client](#prevent-user-data-from-unintentionally-reaching-the-client)

---

## Reference

### taintObjectReference(message, object)

Call `taintObjectReference` with an object to register it with React as something that should not be allowed to be passed to the Client as is:

 $

```
import {experimental_taintObjectReference} from 'react';experimental_taintObjectReference(  'Do not pass ALL environment variables to the client.',  process.env);
```

/$

[See more examples below.](#usage)

#### Parameters

- `message`: The message you want to display if the object gets passed to a Client Component. This message will be displayed as a part of the Error that will be thrown if the object gets passed to a Client Component.
- `object`: The object to be tainted. Functions and class instances can be passed to `taintObjectReference` as `object`. Functions and classes are already blocked from being passed to Client Components but the React’s default error message will be replaced by what you defined in `message`. When a specific instance of a Typed Array is passed to `taintObjectReference` as `object`, any other copies of the Typed Array will not be tainted.

#### Returns

`experimental_taintObjectReference` returns `undefined`.

#### Caveats

- Recreating or cloning a tainted object creates a new untainted object which may contain sensitive data. For example, if you have a tainted `user` object, `const userInfo = {name: user.name, ssn: user.ssn}` or `{...user}` will create new objects which are not tainted. `taintObjectReference` only protects against simple mistakes when the object is passed through to a Client Component unchanged.

### Pitfall

**Do not rely on just tainting for security.** Tainting an object doesn’t prevent leaking of every possible derived value. For example, the clone of a tainted object will create a new untainted object. Using data from a tainted object (e.g. `{secret: taintedObj.secret}`) will create a new value or object that is not tainted. Tainting is a layer of protection; a secure app will have multiple layers of protection, well designed APIs, and isolation patterns.

---

## Usage

### Prevent user data from unintentionally reaching the client

A Client Component should never accept objects that carry sensitive data. Ideally, the data fetching functions should not expose data that the current user should not have access to. Sometimes mistakes happen during refactoring. To protect against these mistakes happening down the line we can “taint” the user object in our data API.

 $

```
import {experimental_taintObjectReference} from 'react';export async function getUser(id) {  const user = await db`SELECT * FROM users WHERE id = ${id}`;  experimental_taintObjectReference(    'Do not pass the entire user object to the client. ' +      'Instead, pick off the specific properties you need for this use case.',    user,  );  return user;}
```

/$

Now whenever anyone tries to pass this object to a Client Component, an error will be thrown with the passed in error message instead.

##### Deep Dive

#### Protecting against leaks in data fetching

If you’re running a Server Components environment that has access to sensitive data, you have to be careful not to pass objects straight through:

$

```
// api.jsexport async function getUser(id) {  const user = await db`SELECT * FROM users WHERE id = ${id}`;  return user;}
```

/$$

```
import { getUser } from 'api.js';import { InfoCard } from 'components.js';export async function Profile(props) {  const user = await getUser(props.userId);  // DO NOT DO THIS  return <InfoCard user={user} />;}
```

/$$

```
// components.js"use client";export async function InfoCard({ user }) {  return <div>{user.name}</div>;}
```

/$

Ideally, the `getUser` should not expose data that the current user should not have access to. To prevent passing the `user` object to a Client Component down the line we can “taint” the user object:

$

```
// api.jsimport {experimental_taintObjectReference} from 'react';export async function getUser(id) {  const user = await db`SELECT * FROM users WHERE id = ${id}`;  experimental_taintObjectReference(    'Do not pass the entire user object to the client. ' +      'Instead, pick off the specific properties you need for this use case.',    user,  );  return user;}
```

/$

Now if anyone tries to pass the `user` object to a Client Component, an error will be thrown with the passed in error message.

[Previoususe](https://react.dev/reference/react/use)[Nextexperimental_taintUniqueValue](https://react.dev/reference/react/experimental_taintUniqueValue)

---

# experimental_taintUniqueValue

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react/apis)

# experimental_taintUniqueValue

### Experimental Feature

**This API is experimental and is not available in a stable version of React yet.**

You can try it by upgrading React packages to the most recent experimental version:

- `react@experimental`
- `react-dom@experimental`
- `eslint-plugin-react-hooks@experimental`

Experimental versions of React may contain bugs. Don’t use them in production.

This API is only available inside [React Server Components](https://react.dev/reference/rsc/use-client).

`taintUniqueValue` lets you prevent unique values from being passed to Client Components like passwords, keys, or tokens.

$

```
taintUniqueValue(errMessage, lifetime, value)
```

/$

To prevent passing an object containing sensitive data, see [taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference).

- [Reference](#reference)
  - [taintUniqueValue(message, lifetime, value)](#taintuniquevalue)
- [Usage](#usage)
  - [Prevent a token from being passed to Client Components](#prevent-a-token-from-being-passed-to-client-components)

---

## Reference

### taintUniqueValue(message, lifetime, value)

Call `taintUniqueValue` with a password, token, key or hash to register it with React as something that should not be allowed to be passed to the Client as is:

 $

```
import {experimental_taintUniqueValue} from 'react';experimental_taintUniqueValue(  'Do not pass secret keys to the client.',  process,  process.env.SECRET_KEY);
```

/$

[See more examples below.](#usage)

#### Parameters

- `message`: The message you want to display if `value` is passed to a Client Component. This message will be displayed as a part of the Error that will be thrown if `value` is passed to a Client Component.
- `lifetime`: Any object that indicates how long `value` should be tainted. `value` will be blocked from being sent to any Client Component while this object still exists. For example, passing `globalThis` blocks the value for the lifetime of an app. `lifetime` is typically an object whose properties contains `value`.
- `value`: A string, bigint or TypedArray. `value` must be a unique sequence of characters or bytes with high entropy such as a cryptographic token, private key, hash, or a long password. `value` will be blocked from being sent to any Client Component.

#### Returns

`experimental_taintUniqueValue` returns `undefined`.

#### Caveats

- Deriving new values from tainted values can compromise tainting protection. New values created by uppercasing tainted values, concatenating tainted string values into a larger string, converting tainted values to base64, substringing tainted values, and other similar transformations are not tainted unless you explicitly call `taintUniqueValue` on these newly created values.
- Do not use `taintUniqueValue` to protect low-entropy values such as PIN codes or phone numbers. If any value in a request is controlled by an attacker, they could infer which value is tainted by enumerating all possible values of the secret.

---

## Usage

### Prevent a token from being passed to Client Components

To ensure that sensitive information such as passwords, session tokens, or other unique values do not inadvertently get passed to Client Components, the `taintUniqueValue` function provides a layer of protection. When a value is tainted, any attempt to pass it to a Client Component will result in an error.

The `lifetime` argument defines the duration for which the value remains tainted. For values that should remain tainted indefinitely, objects like [globalThis](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis) or `process` can serve as the `lifetime` argument. These objects have a lifespan that spans the entire duration of your app’s execution.

 $

```
import {experimental_taintUniqueValue} from 'react';experimental_taintUniqueValue(  'Do not pass a user password to the client.',  globalThis,  process.env.SECRET_KEY);
```

/$

If the tainted value’s lifespan is tied to a object, the `lifetime` should be the object that encapsulates the value. This ensures the tainted value remains protected for the lifetime of the encapsulating object.

 $

```
import {experimental_taintUniqueValue} from 'react';export async function getUser(id) {  const user = await db`SELECT * FROM users WHERE id = ${id}`;  experimental_taintUniqueValue(    'Do not pass a user session token to the client.',    user,    user.session.token  );  return user;}
```

/$

In this example, the `user` object serves as the `lifetime` argument. If this object gets stored in a global cache or is accessible by another request, the session token remains tainted.

### Pitfall

**Do not rely solely on tainting for security.** Tainting a value doesn’t block every possible derived value. For example, creating a new value by upper casing a tainted string will not taint the new value.

$

```
import {experimental_taintUniqueValue} from 'react';const password = 'correct horse battery staple';experimental_taintUniqueValue(  'Do not pass the password to the client.',  globalThis,  password);const uppercasePassword = password.toUpperCase() // `uppercasePassword` is not tainted
```

/$

In this example, the constant `password` is tainted. Then `password` is used to create a new value `uppercasePassword` by calling the `toUpperCase` method on `password`. The newly created `uppercasePassword` is not tainted.

Other similar ways of deriving new values from tainted values like concatenating it into a larger string, converting it to base64, or returning a substring create untained values.

Tainting only protects against simple mistakes like explicitly passing secret values to the client. Mistakes in calling the `taintUniqueValue` like using a global store outside of React, without the corresponding lifetime object, can cause the tainted value to become untainted. Tainting is a layer of protection; a secure app will have multiple layers of protection, well designed APIs, and isolation patterns.

##### Deep Dive

#### Usingserver-onlyandtaintUniqueValueto prevent leaking secrets

If you’re running a Server Components environment that has access to private keys or passwords such as database passwords, you have to be careful not to pass that to a Client Component.

$

```
export async function Dashboard(props) {  // DO NOT DO THIS  return <Overview password={process.env.API_PASSWORD} />;}
```

/$$

```
"use client";import {useEffect} from '...'export async function Overview({ password }) {  useEffect(() => {    const headers = { Authorization: password };    fetch(url, { headers }).then(...);  }, [password]);  ...}
```

/$

This example would leak the secret API token to the client. If this API token can be used to access data this particular user shouldn’t have access to, it could lead to a data breach.

Ideally, secrets like this are abstracted into a single helper file that can only be imported by trusted data utilities on the server. The helper can even be tagged with [server-only](https://www.npmjs.com/package/server-only) to ensure that this file isn’t imported on the client.

$

```
import "server-only";export function fetchAPI(url) {  const headers = { Authorization: process.env.API_PASSWORD };  return fetch(url, { headers });}
```

/$

Sometimes mistakes happen during refactoring and not all of your colleagues might know about this.
To protect against this mistakes happening down the line we can “taint” the actual password:

$

```
import "server-only";import {experimental_taintUniqueValue} from 'react';experimental_taintUniqueValue(  'Do not pass the API token password to the client. ' +    'Instead do all fetches on the server.'  process,  process.env.API_PASSWORD);
```

/$

Now whenever anyone tries to pass this password to a Client Component, or send the password to a Client Component with a Server Function, an error will be thrown with message you defined when you called `taintUniqueValue`.

---

[Previousexperimental_taintObjectReference](https://react.dev/reference/react/experimental_taintObjectReference)
