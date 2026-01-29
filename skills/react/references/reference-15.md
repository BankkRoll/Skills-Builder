# useReducer and more

# useReducer

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useReducer

`useReducer` is a React Hook that lets you add a [reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer) to your component.

$

```
const [state, dispatch] = useReducer(reducer, initialArg, init?)
```

/$

- [Reference](#reference)
  - [useReducer(reducer, initialArg, init?)](#usereducer)
  - [dispatchfunction](#dispatch)
- [Usage](#usage)
  - [Adding a reducer to a component](#adding-a-reducer-to-a-component)
  - [Writing the reducer function](#writing-the-reducer-function)
  - [Avoiding recreating the initial state](#avoiding-recreating-the-initial-state)
- [Troubleshooting](#troubleshooting)
  - [I’ve dispatched an action, but logging gives me the old state value](#ive-dispatched-an-action-but-logging-gives-me-the-old-state-value)
  - [I’ve dispatched an action, but the screen doesn’t update](#ive-dispatched-an-action-but-the-screen-doesnt-update)
  - [A part of my reducer state becomes undefined after dispatching](#a-part-of-my-reducer-state-becomes-undefined-after-dispatching)
  - [My entire reducer state becomes undefined after dispatching](#my-entire-reducer-state-becomes-undefined-after-dispatching)
  - [I’m getting an error: “Too many re-renders”](#im-getting-an-error-too-many-re-renders)
  - [My reducer or initializer function runs twice](#my-reducer-or-initializer-function-runs-twice)

---

## Reference

### useReducer(reducer, initialArg, init?)

Call `useReducer` at the top level of your component to manage its state with a [reducer.](https://react.dev/learn/extracting-state-logic-into-a-reducer)

 $

```
import { useReducer } from 'react';function reducer(state, action) {  // ...}function MyComponent() {  const [state, dispatch] = useReducer(reducer, { age: 42 });  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

- `reducer`: The reducer function that specifies how the state gets updated. It must be pure, should take the state and action as arguments, and should return the next state. State and action can be of any types.
- `initialArg`: The value from which the initial state is calculated. It can be a value of any type. How the initial state is calculated from it depends on the next `init` argument.
- **optional** `init`: The initializer function that should return the initial state. If it’s not specified, the initial state is set to `initialArg`. Otherwise, the initial state is set to the result of calling `init(initialArg)`.

#### Returns

`useReducer` returns an array with exactly two values:

1. The current state. During the first render, it’s set to `init(initialArg)` or `initialArg` (if there’s no `init`).
2. The [dispatchfunction](#dispatch) that lets you update the state to a different value and trigger a re-render.

#### Caveats

- `useReducer` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.
- The `dispatch` function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. [Learn more about removing Effect dependencies.](https://react.dev/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)
- In Strict Mode, React will **call your reducer and initializer twice** in order to [help you find accidental impurities.](#my-reducer-or-initializer-function-runs-twice) This is development-only behavior and does not affect production. If your reducer and initializer are pure (as they should be), this should not affect your logic. The result from one of the calls is ignored.

---

### dispatchfunction

The `dispatch` function returned by `useReducer` lets you update the state to a different value and trigger a re-render. You need to pass the action as the only argument to the `dispatch` function:

 $

```
const [state, dispatch] = useReducer(reducer, { age: 42 });function handleClick() {  dispatch({ type: 'incremented_age' });  // ...
```

/$

React will set the next state to the result of calling the `reducer` function you’ve provided with the current `state` and the action you’ve passed to `dispatch`.

#### Parameters

- `action`: The action performed by the user. It can be a value of any type. By convention, an action is usually an object with a `type` property identifying it and, optionally, other properties with additional information.

#### Returns

`dispatch` functions do not have a return value.

#### Caveats

- The `dispatch` function **only updates the state variable for thenextrender**. If you read the state variable after calling the `dispatch` function, [you will still get the old value](#ive-dispatched-an-action-but-logging-gives-me-the-old-state-value) that was on the screen before your call.
- If the new value you provide is identical to the current `state`, as determined by an [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison, React will **skip re-rendering the component and its children.** This is an optimization. React may still need to call your component before ignoring the result, but it shouldn’t affect your code.
- React [batches state updates.](https://react.dev/learn/queueing-a-series-of-state-updates) It updates the screen **after all the event handlers have run** and have called their `set` functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use [flushSync.](https://react.dev/reference/react-dom/flushSync)

---

## Usage

### Adding a reducer to a component

Call `useReducer` at the top level of your component to manage state with a [reducer.](https://react.dev/learn/extracting-state-logic-into-a-reducer)

 $

```
import { useReducer } from 'react';function reducer(state, action) {  // ...}function MyComponent() {  const [state, dispatch] = useReducer(reducer, { age: 42 });  // ...
```

/$

`useReducer` returns an array with exactly two items:

1. The current state of this state variable, initially set to the initial state you provided.
2. The `dispatch` function that lets you change it in response to interaction.

To update what’s on the screen, call `dispatch` with an object representing what the user did, called an *action*:

 $

```
function handleClick() {  dispatch({ type: 'incremented_age' });}
```

/$

React will pass the current state and the action to your reducer function. Your reducer will calculate and return the next state. React will store that next state, render your component with it, and update the UI.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';

function reducer(state, action) {
  if (action.type === 'incremented_age') {
    return {
      age: state.age + 1
    };
  }
  throw Error('Unknown action.');
}

export default function Counter() {
  const [state, dispatch] = useReducer(reducer, { age: 42 });

  return (
    <>
      <button onClick={() => {
        dispatch({ type: 'incremented_age' })
      }}>
        Increment age
      </button>
      <p>Hello! You are {state.age}.</p>
    </>
  );
}
```

/$

`useReducer` is very similar to [useState](https://react.dev/reference/react/useState), but it lets you move the state update logic from event handlers into a single function outside of your component. Read more about [choosing betweenuseStateanduseReducer.](https://react.dev/learn/extracting-state-logic-into-a-reducer#comparing-usestate-and-usereducer)

---

### Writing the reducer function

A reducer function is declared like this:

 $

```
function reducer(state, action) {  // ...}
```

/$

Then you need to fill in the code that will calculate and return the next state. By convention, it is common to write it as a [switchstatement.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/switch) For each `case` in the `switch`, calculate and return some next state.

 $

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      return {        name: state.name,        age: state.age + 1      };    }    case 'changed_name': {      return {        name: action.nextName,        age: state.age      };    }  }  throw Error('Unknown action: ' + action.type);}
```

/$

Actions can have any shape. By convention, it’s common to pass objects with a `type` property identifying the action. It should include the minimal necessary information that the reducer needs to compute the next state.

 $

```
function Form() {  const [state, dispatch] = useReducer(reducer, { name: 'Taylor', age: 42 });    function handleButtonClick() {    dispatch({ type: 'incremented_age' });  }  function handleInputChange(e) {    dispatch({      type: 'changed_name',      nextName: e.target.value    });  }  // ...
```

/$

The action type names are local to your component. [Each action describes a single interaction, even if that leads to multiple changes in data.](https://react.dev/learn/extracting-state-logic-into-a-reducer#writing-reducers-well) The shape of the state is arbitrary, but usually it’ll be an object or an array.

Read [extracting state logic into a reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer) to learn more.

### Pitfall

State is read-only. Don’t modify any objects or arrays in state:

$

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      // 🚩 Don't mutate an object in state like this:      state.age = state.age + 1;      return state;    }
```

/$

Instead, always return new objects from your reducer:

$

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      // ✅ Instead, return a new object      return {        ...state,        age: state.age + 1      };    }
```

/$

Read [updating objects in state](https://react.dev/learn/updating-objects-in-state) and [updating arrays in state](https://react.dev/learn/updating-arrays-in-state) to learn more.

#### Basic useReducer examples

#### Example1of3:Form (object)

In this example, the reducer manages a state object with two fields: `name` and `age`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'incremented_age': {
      return {
        name: state.name,
        age: state.age + 1
      };
    }
    case 'changed_name': {
      return {
        name: action.nextName,
        age: state.age
      };
    }
  }
  throw Error('Unknown action: ' + action.type);
}

const initialState = { name: 'Taylor', age: 42 };

export default function Form() {
  const [state, dispatch] = useReducer(reducer, initialState);

  function handleButtonClick() {
    dispatch({ type: 'incremented_age' });
  }

  function handleInputChange(e) {
    dispatch({
      type: 'changed_name',
      nextName: e.target.value
    });
  }

  return (
    <>
      <input
        value={state.name}
        onChange={handleInputChange}
      />
      <button onClick={handleButtonClick}>
        Increment age
      </button>
      <p>Hello, {state.name}. You are {state.age}.</p>
    </>
  );
}
```

/$

---

### Avoiding recreating the initial state

React saves the initial state once and ignores it on the next renders.

 $

```
function createInitialState(username) {  // ...}function TodoList({ username }) {  const [state, dispatch] = useReducer(reducer, createInitialState(username));  // ...
```

/$

Although the result of `createInitialState(username)` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating large arrays or performing expensive calculations.

To solve this, you may **pass it as aninitializerfunction** to `useReducer` as the third argument instead:

 $

```
function createInitialState(username) {  // ...}function TodoList({ username }) {  const [state, dispatch] = useReducer(reducer, username, createInitialState);  // ...
```

/$

Notice that you’re passing `createInitialState`, which is the *function itself*, and not `createInitialState()`, which is the result of calling it. This way, the initial state does not get re-created after initialization.

In the above example, `createInitialState` takes a `username` argument. If your initializer doesn’t need any information to compute the initial state, you may pass `null` as the second argument to `useReducer`.

#### The difference between passing an initializer and passing the initial state directly

#### Example1of2:Passing the initializer function

This example passes the initializer function, so the `createInitialState` function only runs during initialization. It does not run when component re-renders, such as when you type into the input.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';

function createInitialState(username) {
  const initialTodos = [];
  for (let i = 0; i < 50; i++) {
    initialTodos.push({
      id: i,
      text: username + "'s task #" + (i + 1)
    });
  }
  return {
    draft: '',
    todos: initialTodos,
  };
}

function reducer(state, action) {
  switch (action.type) {
    case 'changed_draft': {
      return {
        draft: action.nextDraft,
        todos: state.todos,
      };
    };
    case 'added_todo': {
      return {
        draft: '',
        todos: [{
          id: state.todos.length,
          text: state.draft
        }, ...state.todos]
      }
    }
  }
  throw Error('Unknown action: ' + action.type);
}

export default function TodoList({ username }) {
  const [state, dispatch] = useReducer(
    reducer,
    username,
    createInitialState
  );
  return (
    <>
      <input
        value={state.draft}
        onChange={e => {
          dispatch({
            type: 'changed_draft',
            nextDraft: e.target.value
          })
        }}
      />
      <button onClick={() => {
        dispatch({ type: 'added_todo' });
      }}>Add</button>
      <ul>
        {state.todos.map(item => (
          <li key={item.id}>
            {item.text}
          </li>
        ))}
      </ul>
    </>
  );
}
```

/$

---

## Troubleshooting

### I’ve dispatched an action, but logging gives me the old state value

Calling the `dispatch` function **does not change state in the running code**:

 $

```
function handleClick() {  console.log(state.age);  // 42  dispatch({ type: 'incremented_age' }); // Request a re-render with 43  console.log(state.age);  // Still 42!  setTimeout(() => {    console.log(state.age); // Also 42!  }, 5000);}
```

/$

This is because [states behaves like a snapshot.](https://react.dev/learn/state-as-a-snapshot) Updating state requests another render with the new state value, but does not affect the `state` JavaScript variable in your already-running event handler.

If you need to guess the next state value, you can calculate it manually by calling the reducer yourself:

 $

```
const action = { type: 'incremented_age' };dispatch(action);const nextState = reducer(state, action);console.log(state);     // { age: 42 }console.log(nextState); // { age: 43 }
```

/$

---

### I’ve dispatched an action, but the screen doesn’t update

React will **ignore your update if the next state is equal to the previous state,** as determined by an [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. This usually happens when you change an object or an array in state directly:

 $

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      // 🚩 Wrong: mutating existing object      state.age++;      return state;    }    case 'changed_name': {      // 🚩 Wrong: mutating existing object      state.name = action.nextName;      return state;    }    // ...  }}
```

/$

You mutated an existing `state` object and returned it, so React ignored the update. To fix this, you need to ensure that you’re always [updating objects in state](https://react.dev/learn/updating-objects-in-state) and [updating arrays in state](https://react.dev/learn/updating-arrays-in-state) instead of mutating them:

 $

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      // ✅ Correct: creating a new object      return {        ...state,        age: state.age + 1      };    }    case 'changed_name': {      // ✅ Correct: creating a new object      return {        ...state,        name: action.nextName      };    }    // ...  }}
```

/$

---

### A part of my reducer state becomes undefined after dispatching

Make sure that every `case` branch **copies all of the existing fields** when returning the new state:

 $

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      return {        ...state, // Don't forget this!        age: state.age + 1      };    }    // ...
```

/$

Without `...state` above, the returned next state would only contain the `age` field and nothing else.

---

### My entire reducer state becomes undefined after dispatching

If your state unexpectedly becomes `undefined`, you’re likely forgetting to `return` state in one of the cases, or your action type doesn’t match any of the `case` statements. To find why, throw an error outside the `switch`:

 $

```
function reducer(state, action) {  switch (action.type) {    case 'incremented_age': {      // ...    }    case 'edited_name': {      // ...    }  }  throw Error('Unknown action: ' + action.type);}
```

/$

You can also use a static type checker like TypeScript to catch such mistakes.

---

### I’m getting an error: “Too many re-renders”

You might get an error that says: `Too many re-renders. React limits the number of renders to prevent an infinite loop.` Typically, this means that you’re unconditionally dispatching an action *during render*, so your component enters a loop: render, dispatch (which causes a render), render, dispatch (which causes a render), and so on. Very often, this is caused by a mistake in specifying an event handler:

 $

```
// 🚩 Wrong: calls the handler during renderreturn <button onClick={handleClick()}>Click me</button>// ✅ Correct: passes down the event handlerreturn <button onClick={handleClick}>Click me</button>// ✅ Correct: passes down an inline functionreturn <button onClick={(e) => handleClick(e)}>Click me</button>
```

/$

If you can’t find the cause of this error, click on the arrow next to the error in the console and look through the JavaScript stack to find the specific `dispatch` function call responsible for the error.

---

### My reducer or initializer function runs twice

In [Strict Mode](https://react.dev/reference/react/StrictMode), React will call your reducer and initializer functions twice. This shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](https://react.dev/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component, initializer, and reducer functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice the mistakes.

For example, this impure reducer function mutates an array in state:

 $

```
function reducer(state, action) {  switch (action.type) {    case 'added_todo': {      // 🚩 Mistake: mutating state      state.todos.push({ id: nextId++, text: action.text });      return state;    }    // ...  }}
```

/$

Because React calls your reducer function twice, you’ll see the todo was added twice, so you’ll know that there is a mistake. In this example, you can fix the mistake by [replacing the array instead of mutating it](https://react.dev/learn/updating-arrays-in-state#adding-to-an-array):

 $

```
function reducer(state, action) {  switch (action.type) {    case 'added_todo': {      // ✅ Correct: replacing with new state      return {        ...state,        todos: [          ...state.todos,          { id: nextId++, text: action.text }        ]      };    }    // ...  }}
```

/$

Now that this reducer function is pure, calling it an extra time doesn’t make a difference in behavior. This is why React calling it twice helps you find mistakes. **Only component, initializer, and reducer functions need to be pure.** Event handlers don’t need to be pure, so React will never call your event handlers twice.

Read [keeping components pure](https://react.dev/learn/keeping-components-pure) to learn more.

[PrevioususeOptimistic](https://react.dev/reference/react/useOptimistic)[NextuseRef](https://react.dev/reference/react/useRef)

---

# useRef

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useRef

`useRef` is a React Hook that lets you reference a value that’s not needed for rendering.

$

```
const ref = useRef(initialValue)
```

/$

- [Reference](#reference)
  - [useRef(initialValue)](#useref)
- [Usage](#usage)
  - [Referencing a value with a ref](#referencing-a-value-with-a-ref)
  - [Manipulating the DOM with a ref](#manipulating-the-dom-with-a-ref)
  - [Avoiding recreating the ref contents](#avoiding-recreating-the-ref-contents)
- [Troubleshooting](#troubleshooting)
  - [I can’t get a ref to a custom component](#i-cant-get-a-ref-to-a-custom-component)

---

## Reference

### useRef(initialValue)

Call `useRef` at the top level of your component to declare a [ref.](https://react.dev/learn/referencing-values-with-refs)

 $

```
import { useRef } from 'react';function MyComponent() {  const intervalRef = useRef(0);  const inputRef = useRef(null);  // ...
```

/$

[See more examples below.](#usage)

#### Parameters

- `initialValue`: The value you want the ref object’s `current` property to be initially. It can be a value of any type. This argument is ignored after the initial render.

#### Returns

`useRef` returns an object with a single property:

- `current`: Initially, it’s set to the `initialValue` you have passed. You can later set it to something else. If you pass the ref object to React as a `ref` attribute to a JSX node, React will set its `current` property.

On the next renders, `useRef` will return the same object.

#### Caveats

- You can mutate the `ref.current` property. Unlike state, it is mutable. However, if it holds an object that is used for rendering (for example, a piece of your state), then you shouldn’t mutate that object.
- When you change the `ref.current` property, React does not re-render your component. React is not aware of when you change it because a ref is a plain JavaScript object.
- Do not write *or read* `ref.current` during rendering, except for [initialization.](#avoiding-recreating-the-ref-contents) This makes your component’s behavior unpredictable.
- In Strict Mode, React will **call your component function twice** in order to [help you find accidental impurities.](https://react.dev/reference/react/useState#my-initializer-or-updater-function-runs-twice) This is development-only behavior and does not affect production. Each ref object will be created twice, but one of the versions will be discarded. If your component function is pure (as it should be), this should not affect the behavior.

---

## Usage

### Referencing a value with a ref

Call `useRef` at the top level of your component to declare one or more [refs.](https://react.dev/learn/referencing-values-with-refs)

 $

```
import { useRef } from 'react';function Stopwatch() {  const intervalRef = useRef(0);  // ...
```

/$

`useRef` returns a ref object with a single `current` property initially set to the initial value you provided.

On the next renders, `useRef` will return the same object. You can change its `current` property to store information and read it later. This might remind you of [state](https://react.dev/reference/react/useState), but there is an important difference.

**Changing a ref does not trigger a re-render.** This means refs are perfect for storing information that doesn’t affect the visual output of your component. For example, if you need to store an [interval ID](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) and retrieve it later, you can put it in a ref. To update the value inside the ref, you need to manually change its `current` property:

 $

```
function handleStartClick() {  const intervalId = setInterval(() => {    // ...  }, 1000);  intervalRef.current = intervalId;}
```

/$

Later, you can read that interval ID from the ref so that you can call [clear that interval](https://developer.mozilla.org/en-US/docs/Web/API/clearInterval):

 $

```
function handleStopClick() {  const intervalId = intervalRef.current;  clearInterval(intervalId);}
```

/$

By using a ref, you ensure that:

- You can **store information** between re-renders (unlike regular variables, which reset on every render).
- Changing it **does not trigger a re-render** (unlike state variables, which trigger a re-render).
- The **information is local** to each copy of your component (unlike the variables outside, which are shared).

Changing a ref does not trigger a re-render, so refs are not appropriate for storing information you want to display on the screen. Use state for that instead. Read more about [choosing betweenuseRefanduseState.](https://react.dev/learn/referencing-values-with-refs#differences-between-refs-and-state)

#### Examples of referencing a value with useRef

#### Example1of2:Click counter

This component uses a ref to keep track of how many times the button was clicked. Note that it’s okay to use a ref instead of state here because the click count is only read and written in an event handler.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';

export default function Counter() {
  let ref = useRef(0);

  function handleClick() {
    ref.current = ref.current + 1;
    alert('You clicked ' + ref.current + ' times!');
  }

  return (
    <button onClick={handleClick}>
      Click me!
    </button>
  );
}
```

/$

If you show `{ref.current}` in the JSX, the number won’t update on click. This is because setting `ref.current` does not trigger a re-render. Information that’s used for rendering should be state instead.

### Pitfall

**Do not writeor readref.currentduring rendering.**

React expects that the body of your component [behaves like a pure function](https://react.dev/learn/keeping-components-pure):

- If the inputs ([props](https://react.dev/learn/passing-props-to-a-component), [state](https://react.dev/learn/state-a-components-memory), and [context](https://react.dev/learn/passing-data-deeply-with-context)) are the same, it should return exactly the same JSX.
- Calling it in a different order or with different arguments should not affect the results of other calls.

Reading or writing a ref **during rendering** breaks these expectations.

$

```
function MyComponent() {  // ...  // 🚩 Don't write a ref during rendering  myRef.current = 123;  // ...  // 🚩 Don't read a ref during rendering  return <h1>{myOtherRef.current}</h1>;}
```

/$

You can read or write refs **from event handlers or effects instead**.

$

```
function MyComponent() {  // ...  useEffect(() => {    // ✅ You can read or write refs in effects    myRef.current = 123;  });  // ...  function handleClick() {    // ✅ You can read or write refs in event handlers    doSomething(myOtherRef.current);  }  // ...}
```

/$

If you *have to* read [or write](https://react.dev/reference/react/useState#storing-information-from-previous-renders) something during rendering, [use state](https://react.dev/reference/react/useState) instead.

When you break these rules, your component might still work, but most of the newer features we’re adding to React will rely on these expectations. Read more about [keeping your components pure.](https://react.dev/learn/keeping-components-pure#where-you-_can_-cause-side-effects)

---

### Manipulating the DOM with a ref

It’s particularly common to use a ref to manipulate the [DOM.](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API) React has built-in support for this.

First, declare a ref object with an initial value of `null`:

 $

```
import { useRef } from 'react';function MyComponent() {  const inputRef = useRef(null);  // ...
```

/$

Then pass your ref object as the `ref` attribute to the JSX of the DOM node you want to manipulate:

 $

```
// ...  return <input ref={inputRef} />;
```

/$

After React creates the DOM node and puts it on the screen, React will set the `current` property of your ref object to that DOM node. Now you can access the `<input>`’s DOM node and call methods like [focus()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus):

 $

```
function handleClick() {    inputRef.current.focus();  }
```

/$

React will set the `current` property back to `null` when the node is removed from the screen.

Read more about [manipulating the DOM with refs.](https://react.dev/learn/manipulating-the-dom-with-refs)

#### Examples of manipulating the DOM with useRef

#### Example1of4:Focusing a text input

In this example, clicking the button will focus the input:

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

/$

---

### Avoiding recreating the ref contents

React saves the initial ref value once and ignores it on the next renders.

 $

```
function Video() {  const playerRef = useRef(new VideoPlayer());  // ...
```

/$

Although the result of `new VideoPlayer()` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating expensive objects.

To solve it, you may initialize the ref like this instead:

 $

```
function Video() {  const playerRef = useRef(null);  if (playerRef.current === null) {    playerRef.current = new VideoPlayer();  }  // ...
```

/$

Normally, writing or reading `ref.current` during render is not allowed. However, it’s fine in this case because the result is always the same, and the condition only executes during initialization so it’s fully predictable.

##### Deep Dive

#### How to avoid null checks when initializing useRef later

If you use a type checker and don’t want to always check for `null`, you can try a pattern like this instead:

$

```
function Video() {  const playerRef = useRef(null);  function getPlayer() {    if (playerRef.current !== null) {      return playerRef.current;    }    const player = new VideoPlayer();    playerRef.current = player;    return player;  }  // ...
```

/$

Here, the `playerRef` itself is nullable. However, you should be able to convince your type checker that there is no case in which `getPlayer()` returns `null`. Then use `getPlayer()` in your event handlers.

---

## Troubleshooting

### I can’t get a ref to a custom component

If you try to pass a `ref` to your own component like this:

 $

```
const inputRef = useRef(null);return <MyInput ref={inputRef} />;
```

/$

You might get an error in the console:

 ConsoleTypeError: Cannot read properties of null

By default, your own components don’t expose refs to the DOM nodes inside them.

To fix this, find the component that you want to get a ref to:

 $

```
export default function MyInput({ value, onChange }) {  return (    <input      value={value}      onChange={onChange}    />  );}
```

/$

And then add `ref` to the list of props your component accepts and pass `ref` as a prop to the relevant child [built-in component](https://react.dev/reference/react-dom/components/common) like this:

 $

```
function MyInput({ value, onChange, ref }) {  return (    <input      value={value}      onChange={onChange}      ref={ref}    />  );};export default MyInput;
```

/$

Then the parent component can get a ref to it.

Read more about [accessing another component’s DOM nodes.](https://react.dev/learn/manipulating-the-dom-with-refs#accessing-another-components-dom-nodes)

[PrevioususeReducer](https://react.dev/reference/react/useReducer)[NextuseState](https://react.dev/reference/react/useState)
