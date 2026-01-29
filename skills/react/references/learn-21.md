# Using TypeScript and more

# Using TypeScript

[Learn React](https://react.dev/learn)[Setup](https://react.dev/learn/setup)

# Using TypeScript

TypeScript is a popular way to add type definitions to JavaScript codebases. Out of the box, TypeScript [supports JSX](https://react.dev/learn/writing-markup-with-jsx) and you can get full React Web support by adding [@types/react](https://www.npmjs.com/package/@types/react) and [@types/react-dom](https://www.npmjs.com/package/@types/react-dom) to your project.

### You will learn

- [TypeScript with React Components](https://react.dev/learn/typescript#typescript-with-react-components)
- [Examples of typing with Hooks](https://react.dev/learn/typescript#example-hooks)
- [Common types from@types/react](https://react.dev/learn/typescript#useful-types)
- [Further learning locations](https://react.dev/learn/typescript#further-learning)

## Installation

All [production-grade React frameworks](https://react.dev/learn/creating-a-react-app#full-stack-frameworks) offer support for using TypeScript. Follow the framework specific guide for installation:

- [Next.js](https://nextjs.org/docs/app/building-your-application/configuring/typescript)
- [Remix](https://remix.run/docs/en/1.19.2/guides/typescript)
- [Gatsby](https://www.gatsbyjs.com/docs/how-to/custom-configuration/typescript/)
- [Expo](https://docs.expo.dev/guides/typescript/)

### Adding TypeScript to an existing React project

To install the latest version of React’s type definitions:

  Terminal

```
npm install --save-dev @types/react @types/react-dom
```

The following compiler options need to be set in your `tsconfig.json`:

1. `dom` must be included in [lib](https://www.typescriptlang.org/tsconfig/#lib) (Note: If no `lib` option is specified, `dom` is included by default).
2. [jsx](https://www.typescriptlang.org/tsconfig/#jsx) must be set to one of the valid options. `preserve` should suffice for most applications.
  If you’re publishing a library, consult the [jsxdocumentation](https://www.typescriptlang.org/tsconfig/#jsx) on what value to choose.

## TypeScript with React Components

### Note

Every file containing JSX must use the `.tsx` file extension. This is a TypeScript-specific extension that tells TypeScript that this file contains JSX.

Writing TypeScript with React is very similar to writing JavaScript with React. The key difference when working with a component is that you can provide types for your component’s props. These types can be used for correctness checking and providing inline documentation in editors.

Taking the [MyButtoncomponent](https://react.dev/learn#components) from the [Quick Start](https://react.dev/learn) guide, we can add a type describing the `title` for the button:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Afunction%20MyButton(%7B%20title%20%7D%3A%20%7B%20title%3A%20string%20%7D)%20%7B%0A%20%20return%20(%0A%20%20%20%20%3Cbutton%3E%7Btitle%7D%3C%2Fbutton%3E%0A%20%20)%3B%0A%7D%0A%0Aexport%20default%20function%20MyApp()%20%7B%0A%20%20return%20(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20app%3C%2Fh1%3E%0A%20%20%20%20%20%20%3CMyButton%20title%3D%22I'm%20a%20button%22%20%2F%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20)%3B%0A%7D%0A)

```
function MyButton({ title }: { title: string }) {
  return (
    <button>{title}</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton title="I'm a button" />
    </div>
  );
}
```

/$

### Note

These sandboxes can handle TypeScript code, but they do not run the type-checker. This means you can amend the TypeScript sandboxes to learn, but you won’t get any type errors or warnings. To get type-checking, you can use the [TypeScript Playground](https://www.typescriptlang.org/play) or use a more fully-featured online sandbox.

This inline syntax is the simplest way to provide types for a component, though once you start to have a few fields to describe it can become unwieldy. Instead, you can use an `interface` or `type` to describe the component’s props:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Ainterface%20MyButtonProps%20%7B%0A%20%20%2F**%20The%20text%20to%20display%20inside%20the%20button%20*%2F%0A%20%20title%3A%20string%3B%0A%20%20%2F**%20Whether%20the%20button%20can%20be%20interacted%20with%20*%2F%0A%20%20disabled%3A%20boolean%3B%0A%7D%0A%0Afunction%20MyButton(%7B%20title%2C%20disabled%20%7D%3A%20MyButtonProps)%20%7B%0A%20%20return%20(%0A%20%20%20%20%3Cbutton%20disabled%3D%7Bdisabled%7D%3E%7Btitle%7D%3C%2Fbutton%3E%0A%20%20)%3B%0A%7D%0A%0Aexport%20default%20function%20MyApp()%20%7B%0A%20%20return%20(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20app%3C%2Fh1%3E%0A%20%20%20%20%20%20%3CMyButton%20title%3D%22I'm%20a%20disabled%20button%22%20disabled%3D%7Btrue%7D%2F%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20)%3B%0A%7D%0A)

```
interface MyButtonProps {
  /** The text to display inside the button */
  title: string;
  /** Whether the button can be interacted with */
  disabled: boolean;
}

function MyButton({ title, disabled }: MyButtonProps) {
  return (
    <button disabled={disabled}>{title}</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton title="I'm a disabled button" disabled={true}/>
    </div>
  );
}
```

/$

The type describing your component’s props can be as simple or as complex as you need, though they should be an object type described with either a `type` or `interface`. You can learn about how TypeScript describes objects in [Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) but you may also be interested in using [Union Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types) to describe a prop that can be one of a few different types and the [Creating Types from Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html) guide for more advanced use cases.

## Example Hooks

The type definitions from `@types/react` include types for the built-in Hooks, so you can use them in your components without any additional setup. They are built to take into account the code you write in your component, so you will get [inferred types](https://www.typescriptlang.org/docs/handbook/type-inference.html) a lot of the time and ideally do not need to handle the minutiae of providing the types.

However, we can look at a few examples of how to provide types for Hooks.

### useState

The [useStateHook](https://react.dev/reference/react/useState) will re-use the value passed in as the initial state to determine what the type of the value should be. For example:

 $

```
// Infer the type as "boolean"const [enabled, setEnabled] = useState(false);
```

/$

This will assign the type of `boolean` to `enabled`, and `setEnabled` will be a function accepting either a `boolean` argument, or a function that returns a `boolean`. If you want to explicitly provide a type for the state, you can do so by providing a type argument to the `useState` call:

 $

```
// Explicitly set the type to "boolean"const [enabled, setEnabled] = useState<boolean>(false);
```

/$

This isn’t very useful in this case, but a common case where you may want to provide a type is when you have a union type. For example, `status` here can be one of a few different strings:

 $

```
type Status = "idle" | "loading" | "success" | "error";const [status, setStatus] = useState<Status>("idle");
```

/$

Or, as recommended in [Principles for structuring state](https://react.dev/learn/choosing-the-state-structure#principles-for-structuring-state), you can group related state as an object and describe the different possibilities via object types:

 $

```
type RequestState =  | { status: 'idle' }  | { status: 'loading' }  | { status: 'success', data: any }  | { status: 'error', error: Error };const [requestState, setRequestState] = useState<RequestState>({ status: 'idle' });
```

/$

### useReducer

The [useReducerHook](https://react.dev/reference/react/useReducer) is a more complex Hook that takes a reducer function and an initial state. The types for the reducer function are inferred from the initial state. You can optionally provide a type argument to the `useReducer` call to provide a type for the state, but it is often better to set the type on the initial state instead:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7BuseReducer%7D%20from%20'react'%3B%0A%0Ainterface%20State%20%7B%0A%20%20%20count%3A%20number%0A%7D%3B%0A%0Atype%20CounterAction%20%3D%0A%20%20%7C%20%7B%20type%3A%20%22reset%22%20%7D%0A%20%20%7C%20%7B%20type%3A%20%22setCount%22%3B%20value%3A%20State%5B%22count%22%5D%20%7D%0A%0Aconst%20initialState%3A%20State%20%3D%20%7B%20count%3A%200%20%7D%3B%0A%0Afunction%20stateReducer(state%3A%20State%2C%20action%3A%20CounterAction)%3A%20State%20%7B%0A%20%20switch%20(action.type)%20%7B%0A%20%20%20%20case%20%22reset%22%3A%0A%20%20%20%20%20%20return%20initialState%3B%0A%20%20%20%20case%20%22setCount%22%3A%0A%20%20%20%20%20%20return%20%7B%20...state%2C%20count%3A%20action.value%20%7D%3B%0A%20%20%20%20default%3A%0A%20%20%20%20%20%20throw%20new%20Error(%22Unknown%20action%22)%3B%0A%20%20%7D%0A%7D%0A%0Aexport%20default%20function%20App()%20%7B%0A%20%20const%20%5Bstate%2C%20dispatch%5D%20%3D%20useReducer(stateReducer%2C%20initialState)%3B%0A%0A%20%20const%20addFive%20%3D%20()%20%3D%3E%20dispatch(%7B%20type%3A%20%22setCount%22%2C%20value%3A%20state.count%20%2B%205%20%7D)%3B%0A%20%20const%20reset%20%3D%20()%20%3D%3E%20dispatch(%7B%20type%3A%20%22reset%22%20%7D)%3B%0A%0A%20%20return%20(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20counter%3C%2Fh1%3E%0A%0A%20%20%20%20%20%20%3Cp%3ECount%3A%20%7Bstate.count%7D%3C%2Fp%3E%0A%20%20%20%20%20%20%3Cbutton%20onClick%3D%7BaddFive%7D%3EAdd%205%3C%2Fbutton%3E%0A%20%20%20%20%20%20%3Cbutton%20onClick%3D%7Breset%7D%3EReset%3C%2Fbutton%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20)%3B%0A%7D%0A%0A)

```
import {useReducer} from 'react';

interface State {
   count: number
};

type CounterAction =
  | { type: "reset" }
  | { type: "setCount"; value: State["count"] }

const initialState: State = { count: 0 };

function stateReducer(state: State, action: CounterAction): State {
  switch (action.type) {
    case "reset":
      return initialState;
    case "setCount":
      return { ...state, count: action.value };
    default:
      throw new Error("Unknown action");
  }
}

export default function App() {
  const [state, dispatch] = useReducer(stateReducer, initialState);

  const addFive = () => dispatch({ type: "setCount", value: state.count + 5 });
  const reset = () => dispatch({ type: "reset" });

  return (
    <div>
      <h1>Welcome to my counter</h1>

      <p>Count: {state.count}</p>
      <button onClick={addFive}>Add 5</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

/$

We are using TypeScript in a few key places:

- `interface State` describes the shape of the reducer’s state.
- `type CounterAction` describes the different actions which can be dispatched to the reducer.
- `const initialState: State` provides a type for the initial state, and also the type which is used by `useReducer` by default.
- `stateReducer(state: State, action: CounterAction): State` sets the types for the reducer function’s arguments and return value.

A more explicit alternative to setting the type on `initialState` is to provide a type argument to `useReducer`:

 $

```
import { stateReducer, State } from './your-reducer-implementation';const initialState = { count: 0 };export default function App() {  const [state, dispatch] = useReducer<State>(stateReducer, initialState);}
```

/$

### useContext

The [useContextHook](https://react.dev/reference/react/useContext) is a technique for passing data down the component tree without having to pass props through components. It is used by creating a provider component and often by creating a Hook to consume the value in a child component.

The type of the value provided by the context is inferred from the value passed to the `createContext` call:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7B%20createContext%2C%20useContext%2C%20useState%20%7D%20from%20'react'%3B%0A%0Atype%20Theme%20%3D%20%22light%22%20%7C%20%22dark%22%20%7C%20%22system%22%3B%0Aconst%20ThemeContext%20%3D%20createContext%3CTheme%3E(%22system%22)%3B%0A%0Aconst%20useGetTheme%20%3D%20()%20%3D%3E%20useContext(ThemeContext)%3B%0A%0Aexport%20default%20function%20MyApp()%20%7B%0A%20%20const%20%5Btheme%2C%20setTheme%5D%20%3D%20useState%3CTheme%3E('light')%3B%0A%0A%20%20return%20(%0A%20%20%20%20%3CThemeContext%20value%3D%7Btheme%7D%3E%0A%20%20%20%20%20%20%3CMyComponent%20%2F%3E%0A%20%20%20%20%3C%2FThemeContext%3E%0A%20%20)%0A%7D%0A%0Afunction%20MyComponent()%20%7B%0A%20%20const%20theme%20%3D%20useGetTheme()%3B%0A%0A%20%20return%20(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Cp%3ECurrent%20theme%3A%20%7Btheme%7D%3C%2Fp%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20)%0A%7D%0A)

```
import { createContext, useContext, useState } from 'react';

type Theme = "light" | "dark" | "system";
const ThemeContext = createContext<Theme>("system");

const useGetTheme = () => useContext(ThemeContext);

export default function MyApp() {
  const [theme, setTheme] = useState<Theme>('light');

  return (
    <ThemeContext value={theme}>
      <MyComponent />
    </ThemeContext>
  )
}

function MyComponent() {
  const theme = useGetTheme();

  return (
    <div>
      <p>Current theme: {theme}</p>
    </div>
  )
}
```

/$

This technique works when you have a default value which makes sense - but there are occasionally cases when you do not, and in those cases `null` can feel reasonable as a default value. However, to allow the type-system to understand your code, you need to explicitly set `ContextShape | null` on the `createContext`.

This causes the issue that you need to eliminate the `| null` in the type for context consumers. Our recommendation is to have the Hook do a runtime check for it’s existence and throw an error when not present:

 $

```
import { createContext, useContext, useState, useMemo } from 'react';// This is a simpler example, but you can imagine a more complex object heretype ComplexObject = {  kind: string};// The context is created with `| null` in the type, to accurately reflect the default value.const Context = createContext<ComplexObject | null>(null);// The `| null` will be removed via the check in the Hook.const useGetComplexObject = () => {  const object = useContext(Context);  if (!object) { throw new Error("useGetComplexObject must be used within a Provider") }  return object;}export default function MyApp() {  const object = useMemo(() => ({ kind: "complex" }), []);  return (    <Context value={object}>      <MyComponent />    </Context>  )}function MyComponent() {  const object = useGetComplexObject();  return (    <div>      <p>Current object: {object.kind}</p>    </div>  )}
```

/$

### useMemo

### Note

[React Compiler](https://react.dev/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useMemo` calls. You can use the compiler to handle memoization automatically.

The [useMemo](https://react.dev/reference/react/useMemo) Hooks will create/re-access a memorized value from a function call, re-running the function only when dependencies passed as the 2nd parameter are changed. The result of calling the Hook is inferred from the return value from the function in the first parameter. You can be more explicit by providing a type argument to the Hook.

 $

```
// The type of visibleTodos is inferred from the return value of filterTodosconst visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);
```

/$

### useCallback

### Note

[React Compiler](https://react.dev/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useCallback` calls. You can use the compiler to handle memoization automatically.

The [useCallback](https://react.dev/reference/react/useCallback) provide a stable reference to a function as long as the dependencies passed into the second parameter are the same. Like `useMemo`, the function’s type is inferred from the return value of the function in the first parameter, and you can be more explicit by providing a type argument to the Hook.

 $

```
const handleClick = useCallback(() => {  // ...}, [todos]);
```

/$

When working in TypeScript strict mode `useCallback` requires adding types for the parameters in your callback. This is because the type of the callback is inferred from the return value of the function, and without parameters the type cannot be fully understood.

Depending on your code-style preferences, you could use the `*EventHandler` functions from the React types to provide the type for the event handler at the same time as defining the callback:

 $

```
import { useState, useCallback } from 'react';export default function Form() {  const [value, setValue] = useState("Change me");  const handleChange = useCallback<React.ChangeEventHandler<HTMLInputElement>>((event) => {    setValue(event.currentTarget.value);  }, [setValue])  return (    <>      <input value={value} onChange={handleChange} />      <p>Value: {value}</p>    </>  );}
```

/$

## Useful Types

There is quite an expansive set of types which come from the `@types/react` package, it is worth a read when you feel comfortable with how React and TypeScript interact. You can find them [in React’s folder in DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/react/index.d.ts). We will cover a few of the more common types here.

### DOM Events

When working with DOM events in React, the type of the event can often be inferred from the event handler. However, when you want to extract a function to be passed to an event handler, you will need to explicitly set the type of the event.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7B%20useState%20%7D%20from%20'react'%3B%0A%0Aexport%20default%20function%20Form()%20%7B%0A%20%20const%20%5Bvalue%2C%20setValue%5D%20%3D%20useState(%22Change%20me%22)%3B%0A%0A%20%20function%20handleChange(event%3A%20React.ChangeEvent%3CHTMLInputElement%3E)%20%7B%0A%20%20%20%20setValue(event.currentTarget.value)%3B%0A%20%20%7D%0A%0A%20%20return%20(%0A%20%20%20%20%3C%3E%0A%20%20%20%20%20%20%3Cinput%20value%3D%7Bvalue%7D%20onChange%3D%7BhandleChange%7D%20%2F%3E%0A%20%20%20%20%20%20%3Cp%3EValue%3A%20%7Bvalue%7D%3C%2Fp%3E%0A%20%20%20%20%3C%2F%3E%0A%20%20)%3B%0A%7D%0A)

```
import { useState } from 'react';

export default function Form() {
  const [value, setValue] = useState("Change me");

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setValue(event.currentTarget.value);
  }

  return (
    <>
      <input value={value} onChange={handleChange} />
      <p>Value: {value}</p>
    </>
  );
}
```

/$

There are many types of events provided in the React types - the full list can be found [here](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/b580df54c0819ec9df62b0835a315dd48b8594a9/types/react/index.d.ts#L1247C1-L1373) which is based on the [most popular events from the DOM](https://developer.mozilla.org/en-US/docs/Web/Events).

When determining the type you are looking for you can first look at the hover information for the event handler you are using, which will show the type of the event.

If you need to use an event that is not included in this list, you can use the `React.SyntheticEvent` type, which is the base type for all events.

### Children

There are two common paths to describing the children of a component. The first is to use the `React.ReactNode` type, which is a union of all the possible types that can be passed as children in JSX:

 $

```
interface ModalRendererProps {  title: string;  children: React.ReactNode;}
```

/$

This is a very broad definition of children. The second is to use the `React.ReactElement` type, which is only JSX elements and not JavaScript primitives like strings or numbers:

 $

```
interface ModalRendererProps {  title: string;  children: React.ReactElement;}
```

/$

Note, that you cannot use TypeScript to describe that the children are a certain type of JSX elements, so you cannot use the type-system to describe a component which only accepts `<li>` children.

You can see an example of both `React.ReactNode` and `React.ReactElement` with the type-checker in [this TypeScript playground](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgIilQ3wChSB6CxYmAOmXRgDkIATJOdNJMGAZzgwAFpxAR+8YADswAVwGkZMJFEzpOjDKw4AFHGEEBvUnDhphwADZsi0gFw0mDWjqQBuUgF9yaCNMlENzgAXjgACjADfkctFnYkfQhDAEpQgD44AB42YAA3dKMo5P46C2tbJGkvLIpcgt9-QLi3AEEwMFCItJDMrPTTbIQ3dKywdIB5aU4kKyQQKpha8drhhIGzLLWODbNs3b3s8YAxKBQAcwXpAThMaGWDvbH0gFloGbmrgQfBzYpd1YjQZbEYARkB6zMwO2SHSAAlZlYIBCdtCRkZpHIrFYahQYQD8UYYFA5EhcfjyGYqHAXnJAsIUHlOOUbHYhMIIHJzsI0Qk4P9SLUBuRqXEXEwAKKfRZcNA8PiCfxWACecAAUgBlAAacFm80W-CU11U6h4TgwUv11yShjgJjMLMqDnN9Dilq+nh8pD8AXgCHdMrCkWisVoAet0R6fXqhWKhjKllZVVxMcavpd4Zg7U6Qaj+2hmdG4zeRF10uu-Aeq0LBfLMEe-V+T2L7zLVu+FBWLdLeq+lc7DYFf39deFVOotMCACNOCh1dq219a+30uC8YWoZsRyuEdjkevR8uvoVMdjyTWt4WiSSydXD4NqZP4AymeZE072ZzuUeZQKheQgA).

### Style Props

When using inline styles in React, you can use `React.CSSProperties` to describe the object passed to the `style` prop. This type is a union of all the possible CSS properties, and is a good way to ensure you are passing valid CSS properties to the `style` prop, and to get auto-complete in your editor.

 $

```
interface MyComponentProps {  style: React.CSSProperties;}
```

/$

## Further learning

This guide has covered the basics of using TypeScript with React, but there is a lot more to learn.
Individual API pages on the docs may contain more in-depth documentation on how to use them with TypeScript.

We recommend the following resources:

- [The TypeScript handbook](https://www.typescriptlang.org/docs/handbook/) is the official documentation for TypeScript, and covers most key language features.
- [The TypeScript release notes](https://devblogs.microsoft.com/typescript/) cover new features in depth.
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/) is a community-maintained cheatsheet for using TypeScript with React, covering a lot of useful edge cases and providing more breadth than this document.
- [TypeScript Community Discord](https://discord.com/invite/typescript) is a great place to ask questions and get help with TypeScript and React issues.

[PreviousEditor Setup](https://react.dev/learn/editor-setup)[NextReact Developer Tools](https://react.dev/learn/react-developer-tools)

---

# Understanding Your UI as a Tree

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Understanding Your UI as a Tree

Your React app is taking shape with many components being nested within each other. How does React keep track of your app’s component structure?

React, and many other UI libraries, model UI as a tree. Thinking of your app as a tree is useful for understanding the relationship between components. This understanding will help you debug future concepts like performance and state management.

### You will learn

- How React “sees” component structures
- What a render tree is and what it is useful for
- What a module dependency tree is and what it is useful for

## Your UI as a tree

Trees are a relationship model between items. The UI is often represented using tree structures. For example, browsers use tree structures to model HTML ([DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model/Introduction)) and CSS ([CSSOM](https://developer.mozilla.org/docs/Web/API/CSS_Object_Model)). Mobile platforms also use trees to represent their view hierarchy.

 ![Diagram with three sections arranged horizontally. In the first section, there are three rectangles stacked vertically, with labels 'Component A', 'Component B', and 'Component C'. Transitioning to the next pane is an arrow with the React logo on top labeled 'React'. The middle section contains a tree of components, with the root labeled 'A' and two children labeled 'B' and 'C'. The next section is again transitioned using an arrow with the React logo on top labeled 'React DOM'. The third and final section is a wireframe of a browser, containing a tree of 8 nodes, which has only a subset highlighted (indicating the subtree from the middle section).](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpreserving_state_dom_tree.dark.png&w=1920&q=75)![Diagram with three sections arranged horizontally. In the first section, there are three rectangles stacked vertically, with labels 'Component A', 'Component B', and 'Component C'. Transitioning to the next pane is an arrow with the React logo on top labeled 'React'. The middle section contains a tree of components, with the root labeled 'A' and two children labeled 'B' and 'C'. The next section is again transitioned using an arrow with the React logo on top labeled 'React DOM'. The third and final section is a wireframe of a browser, containing a tree of 8 nodes, which has only a subset highlighted (indicating the subtree from the middle section).](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpreserving_state_dom_tree.png&w=1920&q=75)

React creates a UI tree from your components. In this example, the UI tree is then used to render to the DOM.

Like browsers and mobile platforms, React also uses tree structures to manage and model the relationship between components in a React app. These trees are useful tools to understand how data flows through a React app and how to optimize rendering and app size.

## The Render Tree

A major feature of components is the ability to compose components of other components. As we [nest components](https://react.dev/learn/your-first-component#nesting-and-organizing-components), we have the concept of parent and child components, where each parent component may itself be a child of another component.

When we render a React app, we can model this relationship in a tree, known as the render tree.

Here is a React app that renders inspirational quotes.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import FancyText from './FancyText';
import InspirationGenerator from './InspirationGenerator';
import Copyright from './Copyright';

export default function App() {
  return (
    <>
      <FancyText title text="Get Inspired App" />
      <InspirationGenerator>
        <Copyright year={2004} />
      </InspirationGenerator>
    </>
  );
}
```

/$ ![Tree graph with five nodes. Each node represents a component. The root of the tree is App, with two arrows extending from it to 'InspirationGenerator' and 'FancyText'. The arrows are labelled with the word 'renders'. 'InspirationGenerator' node also has two arrows pointing to nodes 'FancyText' and 'Copyright'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Frender_tree.dark.png&w=1080&q=75)![Tree graph with five nodes. Each node represents a component. The root of the tree is App, with two arrows extending from it to 'InspirationGenerator' and 'FancyText'. The arrows are labelled with the word 'renders'. 'InspirationGenerator' node also has two arrows pointing to nodes 'FancyText' and 'Copyright'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Frender_tree.png&w=1080&q=75)

React creates a *render tree*, a UI tree, composed of the rendered components.

From the example app, we can construct the above render tree.

The tree is composed of nodes, each of which represents a component. `App`, `FancyText`, `Copyright`, to name a few, are all nodes in our tree.

The root node in a React render tree is the [root component](https://react.dev/learn/importing-and-exporting-components#the-root-component-file) of the app. In this case, the root component is `App` and it is the first component React renders. Each arrow in the tree points from a parent component to a child component.

##### Deep Dive

#### Where are the HTML tags in the render tree?

You’ll notice in the above render tree, there is no mention of the HTML tags that each component renders. This is because the render tree is only composed of React [components](https://react.dev/learn/your-first-component#components-ui-building-blocks).

React, as a UI framework, is platform agnostic. On react.dev, we showcase examples that render to the web, which uses HTML markup as its UI primitives. But a React app could just as likely render to a mobile or desktop platform, which may use different UI primitives like [UIView](https://developer.apple.com/documentation/uikit/uiview) or [FrameworkElement](https://learn.microsoft.com/en-us/dotnet/api/system.windows.frameworkelement?view=windowsdesktop-7.0).

These platform UI primitives are not a part of React. React render trees can provide insight to our React app regardless of what platform your app renders to.

A render tree represents a single render pass of a React application. With [conditional rendering](https://react.dev/learn/conditional-rendering), a parent component may render different children depending on the data passed.

We can update the app to conditionally render either an inspirational quote or color.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import FancyText from './FancyText';
import InspirationGenerator from './InspirationGenerator';
import Copyright from './Copyright';

export default function App() {
  return (
    <>
      <FancyText title text="Get Inspired App" />
      <InspirationGenerator>
        <Copyright year={2004} />
      </InspirationGenerator>
    </>
  );
}
```

/$ ![Tree graph with six nodes. The top node of the tree is labelled 'App' with two arrows extending to nodes labelled 'InspirationGenerator' and 'FancyText'. The arrows are solid lines and are labelled with the word 'renders'. 'InspirationGenerator' node also has three arrows. The arrows to nodes 'FancyText' and 'Color' are dashed and labelled with 'renders?'. The last arrow points to the node labelled 'Copyright' and is solid and labelled with 'renders'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fconditional_render_tree.dark.png&w=1200&q=75)![Tree graph with six nodes. The top node of the tree is labelled 'App' with two arrows extending to nodes labelled 'InspirationGenerator' and 'FancyText'. The arrows are solid lines and are labelled with the word 'renders'. 'InspirationGenerator' node also has three arrows. The arrows to nodes 'FancyText' and 'Color' are dashed and labelled with 'renders?'. The last arrow points to the node labelled 'Copyright' and is solid and labelled with 'renders'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fconditional_render_tree.png&w=1200&q=75)

With conditional rendering, across different renders, the render tree may render different components.

In this example, depending on what `inspiration.type` is, we may render `<FancyText>` or `<Color>`. The render tree may be different for each render pass.

Although render trees may differ across render passes, these trees are generally helpful for identifying what the *top-level* and *leaf components* are in a React app. Top-level components are the components nearest to the root component and affect the rendering performance of all the components beneath them and often contain the most complexity. Leaf components are near the bottom of the tree and have no child components and are often frequently re-rendered.

Identifying these categories of components are useful for understanding data flow and performance of your app.

## The Module Dependency Tree

Another relationship in a React app that can be modeled with a tree are an app’s module dependencies. As we [break up our components](https://react.dev/learn/importing-and-exporting-components#exporting-and-importing-a-component) and logic into separate files, we create [JS modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) where we may export components, functions, or constants.

Each node in a module dependency tree is a module and each branch represents an `import` statement in that module.

If we take the previous Inspirations app, we can build a module dependency tree, or dependency tree for short.

 ![A tree graph with seven nodes. Each node is labelled with a module name. The top level node of the tree is labelled 'App.js'. There are three arrows pointing to the modules 'InspirationGenerator.js', 'FancyText.js' and 'Copyright.js' and the arrows are labelled with 'imports'. From the 'InspirationGenerator.js' node, there are three arrows that extend to three modules: 'FancyText.js', 'Color.js', and 'inspirations.js'. The arrows are labelled with 'imports'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fmodule_dependency_tree.dark.png&w=1920&q=75)![A tree graph with seven nodes. Each node is labelled with a module name. The top level node of the tree is labelled 'App.js'. There are three arrows pointing to the modules 'InspirationGenerator.js', 'FancyText.js' and 'Copyright.js' and the arrows are labelled with 'imports'. From the 'InspirationGenerator.js' node, there are three arrows that extend to three modules: 'FancyText.js', 'Color.js', and 'inspirations.js'. The arrows are labelled with 'imports'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fmodule_dependency_tree.png&w=1920&q=75)

The module dependency tree for the Inspirations app.

The root node of the tree is the root module, also known as the entrypoint file. It often is the module that contains the root component.

Comparing to the render tree of the same app, there are similar structures but some notable differences:

- The nodes that make-up the tree represent modules, not components.
- Non-component modules, like `inspirations.js`, are also represented in this tree. The render tree only encapsulates components.
- `Copyright.js` appears under `App.js` but in the render tree, `Copyright`, the component, appears as a child of `InspirationGenerator`. This is because `InspirationGenerator` accepts JSX as [children props](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children), so it renders `Copyright` as a child component but does not import the module.

Dependency trees are useful to determine what modules are necessary to run your React app. When building a React app for production, there is typically a build step that will bundle all the necessary JavaScript to ship to the client. The tool responsible for this is called a [bundler](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Overview#the_modern_tooling_ecosystem), and bundlers will use the dependency tree to determine what modules should be included.

As your app grows, often the bundle size does too. Large bundle sizes are expensive for a client to download and run. Large bundle sizes can delay the time for your UI to get drawn. Getting a sense of your app’s dependency tree may help with debugging these issues.

## Recap

- Trees are a common way to represent the relationship between entities. They are often used to model UI.
- Render trees represent the nested relationship between React components across a single render.
- With conditional rendering, the render tree may change across different renders. With different prop values, components may render different children components.
- Render trees help identify what the top-level and leaf components are. Top-level components affect the rendering performance of all components beneath them and leaf components are often re-rendered frequently. Identifying them is useful for understanding and debugging rendering performance.
- Dependency trees represent the module dependencies in a React app.
- Dependency trees are used by build tools to bundle the necessary code to ship an app.
- Dependency trees are useful for debugging large bundle sizes that slow time to paint and expose opportunities for optimizing what code is bundled.

[PreviousKeeping Components Pure](https://react.dev/learn/keeping-components-pure)[NextAdding Interactivity](https://react.dev/learn/adding-interactivity)
