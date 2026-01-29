# useState and more

# useState

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useState

`useState` is a React Hook that lets you add a [state variable](https://react.dev/learn/state-a-components-memory) to your component.

$

```
const [state, setState] = useState(initialState)
```

/$

- [Reference](#reference)
  - [useState(initialState)](#usestate)
  - [setfunctions, likesetSomething(nextState)](#setstate)
- [Usage](#usage)
  - [Adding state to a component](#adding-state-to-a-component)
  - [Updating state based on the previous state](#updating-state-based-on-the-previous-state)
  - [Updating objects and arrays in state](#updating-objects-and-arrays-in-state)
  - [Avoiding recreating the initial state](#avoiding-recreating-the-initial-state)
  - [Resetting state with a key](#resetting-state-with-a-key)
  - [Storing information from previous renders](#storing-information-from-previous-renders)
- [Troubleshooting](#troubleshooting)
  - [I’ve updated the state, but logging gives me the old value](#ive-updated-the-state-but-logging-gives-me-the-old-value)
  - [I’ve updated the state, but the screen doesn’t update](#ive-updated-the-state-but-the-screen-doesnt-update)
  - [I’m getting an error: “Too many re-renders”](#im-getting-an-error-too-many-re-renders)
  - [My initializer or updater function runs twice](#my-initializer-or-updater-function-runs-twice)
  - [I’m trying to set state to a function, but it gets called instead](#im-trying-to-set-state-to-a-function-but-it-gets-called-instead)

---

## Reference

### useState(initialState)

Call `useState` at the top level of your component to declare a [state variable.](https://react.dev/learn/state-a-components-memory)

 $

```
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(28);  const [name, setName] = useState('Taylor');  const [todos, setTodos] = useState(() => createTodos());  // ...
```

/$

The convention is to name state variables like `[something, setSomething]` using [array destructuring.](https://javascript.info/destructuring-assignment)

[See more examples below.](#usage)

#### Parameters

- `initialState`: The value you want the state to be initially. It can be a value of any type, but there is a special behavior for functions. This argument is ignored after the initial render.
  - If you pass a function as `initialState`, it will be treated as an *initializer function*. It should be pure, should take no arguments, and should return a value of any type. React will call your initializer function when initializing the component, and store its return value as the initial state. [See an example below.](#avoiding-recreating-the-initial-state)

#### Returns

`useState` returns an array with exactly two values:

1. The current state. During the first render, it will match the `initialState` you have passed.
2. The [setfunction](#setstate) that lets you update the state to a different value and trigger a re-render.

#### Caveats

- `useState` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.
- In Strict Mode, React will **call your initializer function twice** in order to [help you find accidental impurities.](#my-initializer-or-updater-function-runs-twice) This is development-only behavior and does not affect production. If your initializer function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

---

### setfunctions, likesetSomething(nextState)

The `set` function returned by `useState` lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

 $

```
const [name, setName] = useState('Edward');function handleClick() {  setName('Taylor');  setAge(a => a + 1);  // ...
```

/$

#### Parameters

- `nextState`: The value that you want the state to be. It can be a value of any type, but there is a special behavior for functions.
  - If you pass a function as `nextState`, it will be treated as an *updater function*. It must be pure, should take the pending state as its only argument, and should return the next state. React will put your updater function in a queue and re-render your component. During the next render, React will calculate the next state by applying all of the queued updaters to the previous state. [See an example below.](#updating-state-based-on-the-previous-state)

#### Returns

`set` functions do not have a return value.

#### Caveats

- The `set` function **only updates the state variable for thenextrender**. If you read the state variable after calling the `set` function, [you will still get the old value](#ive-updated-the-state-but-logging-gives-me-the-old-value) that was on the screen before your call.
- If the new value you provide is identical to the current `state`, as determined by an [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison, React will **skip re-rendering the component and its children.** This is an optimization. Although in some cases React may still need to call your component before skipping the children, it shouldn’t affect your code.
- React [batches state updates.](https://react.dev/learn/queueing-a-series-of-state-updates) It updates the screen **after all the event handlers have run** and have called their `set` functions. This prevents multiple re-renders during a single event. In the rare case that you need to force React to update the screen earlier, for example to access the DOM, you can use [flushSync.](https://react.dev/reference/react-dom/flushSync)
- The `set` function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. [Learn more about removing Effect dependencies.](https://react.dev/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)
- Calling the `set` function *during rendering* is only allowed from within the currently rendering component. React will discard its output and immediately attempt to render it again with the new state. This pattern is rarely needed, but you can use it to **store information from the previous renders**. [See an example below.](#storing-information-from-previous-renders)
- In Strict Mode, React will **call your updater function twice** in order to [help you find accidental impurities.](#my-initializer-or-updater-function-runs-twice) This is development-only behavior and does not affect production. If your updater function is pure (as it should be), this should not affect the behavior. The result from one of the calls will be ignored.

---

## Usage

### Adding state to a component

Call `useState` at the top level of your component to declare one or more [state variables.](https://react.dev/learn/state-a-components-memory)

 $

```
import { useState } from 'react';function MyComponent() {  const [age, setAge] = useState(42);  const [name, setName] = useState('Taylor');  // ...
```

/$

The convention is to name state variables like `[something, setSomething]` using [array destructuring.](https://javascript.info/destructuring-assignment)

`useState` returns an array with exactly two items:

1. The current state of this state variable, initially set to the initial state you provided.
2. The `set` function that lets you change it to any other value in response to interaction.

To update what’s on the screen, call the `set` function with some next state:

 $

```
function handleClick() {  setName('Robin');}
```

/$

React will store the next state, render your component again with the new values, and update the UI.

### Pitfall

Calling the `set` function [does notchange the current state in the already executing code](#ive-updated-the-state-but-logging-gives-me-the-old-value):

$

```
function handleClick() {  setName('Robin');  console.log(name); // Still "Taylor"!}
```

/$

It only affects what `useState` will return starting from the *next* render.

#### Basic useState examples

#### Example1of4:Counter (number)

In this example, the `count` state variable holds a number. Clicking the button increments it.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      You pressed me {count} times
    </button>
  );
}
```

/$

---

### Updating state based on the previous state

Suppose the `age` is `42`. This handler calls `setAge(age + 1)` three times:

 $

```
function handleClick() {  setAge(age + 1); // setAge(42 + 1)  setAge(age + 1); // setAge(42 + 1)  setAge(age + 1); // setAge(42 + 1)}
```

/$

However, after one click, `age` will only be `43` rather than `45`! This is because calling the `set` function [does not update](https://react.dev/learn/state-as-a-snapshot) the `age` state variable in the already running code. So each `setAge(age + 1)` call becomes `setAge(43)`.

To solve this problem, **you may pass anupdater function** to `setAge` instead of the next state:

 $

```
function handleClick() {  setAge(a => a + 1); // setAge(42 => 43)  setAge(a => a + 1); // setAge(43 => 44)  setAge(a => a + 1); // setAge(44 => 45)}
```

/$

Here, `a => a + 1` is your updater function. It takes the pending state and calculates the next state from it.

React puts your updater functions in a [queue.](https://react.dev/learn/queueing-a-series-of-state-updates) Then, during the next render, it will call them in the same order:

1. `a => a + 1` will receive `42` as the pending state and return `43` as the next state.
2. `a => a + 1` will receive `43` as the pending state and return `44` as the next state.
3. `a => a + 1` will receive `44` as the pending state and return `45` as the next state.

There are no other queued updates, so React will store `45` as the current state in the end.

By convention, it’s common to name the pending state argument for the first letter of the state variable name, like `a` for `age`. However, you may also call it like `prevAge` or something else that you find clearer.

React may [call your updaters twice](#my-initializer-or-updater-function-runs-twice) in development to verify that they are [pure.](https://react.dev/learn/keeping-components-pure)

##### Deep Dive

#### Is using an updater always preferred?

You might hear a recommendation to always write code like `setAge(a => a + 1)` if the state you’re setting is calculated from the previous state. There is no harm in it, but it is also not always necessary.

In most cases, there is no difference between these two approaches. React always makes sure that for intentional user actions, like clicks, the `age` state variable would be updated before the next click. This means there is no risk of a click handler seeing a “stale” `age` at the beginning of the event handler.

However, if you do multiple updates within the same event, updaters can be helpful. They’re also helpful if accessing the state variable itself is inconvenient (you might run into this when optimizing re-renders).

If you prefer consistency over slightly more verbose syntax, it’s reasonable to always write an updater if the state you’re setting is calculated from the previous state. If it’s calculated from the previous state of some *other* state variable, you might want to combine them into one object and [use a reducer.](https://react.dev/learn/extracting-state-logic-into-a-reducer)

#### The difference between passing an updater and passing the next state directly

#### Example1of2:Passing the updater function

This example passes the updater function, so the “+3” button works.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [age, setAge] = useState(42);

  function increment() {
    setAge(a => a + 1);
  }

  return (
    <>
      <h1>Your age: {age}</h1>
      <button onClick={() => {
        increment();
        increment();
        increment();
      }}>+3</button>
      <button onClick={() => {
        increment();
      }}>+1</button>
    </>
  );
}
```

/$

---

### Updating objects and arrays in state

You can put objects and arrays into state. In React, state is considered read-only, so **you shouldreplaceit rather thanmutateyour existing objects**. For example, if you have a `form` object in state, don’t mutate it:

 $

```
// 🚩 Don't mutate an object in state like this:form.firstName = 'Taylor';
```

/$

Instead, replace the whole object by creating a new one:

 $

```
// ✅ Replace state with a new objectsetForm({  ...form,  firstName: 'Taylor'});
```

/$

Read [updating objects in state](https://react.dev/learn/updating-objects-in-state) and [updating arrays in state](https://react.dev/learn/updating-arrays-in-state) to learn more.

#### Examples of objects and arrays in state

#### Example1of4:Form (object)

In this example, the `form` state variable holds an object. Each input has a change handler that calls `setForm` with the next state of the entire form. The `{ ...form }` spread syntax ensures that the state object is replaced rather than mutated.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [form, setForm] = useState({
    firstName: 'Barbara',
    lastName: 'Hepworth',
    email: 'bhepworth@sculpture.com',
  });

  return (
    <>
      <label>
        First name:
        <input
          value={form.firstName}
          onChange={e => {
            setForm({
              ...form,
              firstName: e.target.value
            });
          }}
        />
      </label>
      <label>
        Last name:
        <input
          value={form.lastName}
          onChange={e => {
            setForm({
              ...form,
              lastName: e.target.value
            });
          }}
        />
      </label>
      <label>
        Email:
        <input
          value={form.email}
          onChange={e => {
            setForm({
              ...form,
              email: e.target.value
            });
          }}
        />
      </label>
      <p>
        {form.firstName}{' '}
        {form.lastName}{' '}
        ({form.email})
      </p>
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
function TodoList() {  const [todos, setTodos] = useState(createInitialTodos());  // ...
```

/$

Although the result of `createInitialTodos()` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating large arrays or performing expensive calculations.

To solve this, you may **pass it as aninitializerfunction** to `useState` instead:

 $

```
function TodoList() {  const [todos, setTodos] = useState(createInitialTodos);  // ...
```

/$

Notice that you’re passing `createInitialTodos`, which is the *function itself*, and not `createInitialTodos()`, which is the result of calling it. If you pass a function to `useState`, React will only call it during initialization.

React may [call your initializers twice](#my-initializer-or-updater-function-runs-twice) in development to verify that they are [pure.](https://react.dev/learn/keeping-components-pure)

#### The difference between passing an initializer and passing the initial state directly

#### Example1of2:Passing the initializer function

This example passes the initializer function, so the `createInitialTodos` function only runs during initialization. It does not run when component re-renders, such as when you type into the input.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

function createInitialTodos() {
  const initialTodos = [];
  for (let i = 0; i < 50; i++) {
    initialTodos.push({
      id: i,
      text: 'Item ' + (i + 1)
    });
  }
  return initialTodos;
}

export default function TodoList() {
  const [todos, setTodos] = useState(createInitialTodos);
  const [text, setText] = useState('');

  return (
    <>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <button onClick={() => {
        setText('');
        setTodos([{
          id: todos.length,
          text: text
        }, ...todos]);
      }}>Add</button>
      <ul>
        {todos.map(item => (
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

### Resetting state with a key

You’ll often encounter the `key` attribute when [rendering lists.](https://react.dev/learn/rendering-lists) However, it also serves another purpose.

You can **reset a component’s state by passing a differentkeyto a component.** In this example, the Reset button changes the `version` state variable, which we pass as a `key` to the `Form`. When the `key` changes, React re-creates the `Form` component (and all of its children) from scratch, so its state gets reset.

Read [preserving and resetting state](https://react.dev/learn/preserving-and-resetting-state) to learn more.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function App() {
  const [version, setVersion] = useState(0);

  function handleReset() {
    setVersion(version + 1);
  }

  return (
    <>
      <button onClick={handleReset}>Reset</button>
      <Form key={version} />
    </>
  );
}

function Form() {
  const [name, setName] = useState('Taylor');

  return (
    <>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <p>Hello, {name}.</p>
    </>
  );
}
```

/$

---

### Storing information from previous renders

Usually, you will update state in event handlers. However, in rare cases you might want to adjust state in response to rendering — for example, you might want to change a state variable when a prop changes.

In most cases, you don’t need this:

- **If the value you need can be computed entirely from the current props or other state,remove that redundant state altogether.** If you’re worried about recomputing too often, the [useMemoHook](https://react.dev/reference/react/useMemo) can help.
- If you want to reset the entire component tree’s state, [pass a differentkeyto your component.](#resetting-state-with-a-key)
- If you can, update all the relevant state in the event handlers.

In the rare case that none of these apply, there is a pattern you can use to update state based on the values that have been rendered so far, by calling a `set` function while your component is rendering.

Here’s an example. This `CountLabel` component displays the `count` prop passed to it:

 $

```
export default function CountLabel({ count }) {  return <h1>{count}</h1>}
```

/$

Say you want to show whether the counter has *increased or decreased* since the last change. The `count` prop doesn’t tell you this — you need to keep track of its previous value. Add the `prevCount` state variable to track it. Add another state variable called `trend` to hold whether the count has increased or decreased. Compare `prevCount` with `count`, and if they’re not equal, update both `prevCount` and `trend`. Now you can show both the current count prop and *how it has changed since the last render*.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function CountLabel({ count }) {
  const [prevCount, setPrevCount] = useState(count);
  const [trend, setTrend] = useState(null);
  if (prevCount !== count) {
    setPrevCount(count);
    setTrend(count > prevCount ? 'increasing' : 'decreasing');
  }
  return (
    <>
      <h1>{count}</h1>
      {trend && <p>The count is {trend}</p>}
    </>
  );
}
```

/$

Note that if you call a `set` function while rendering, it must be inside a condition like `prevCount !== count`, and there must be a call like `setPrevCount(count)` inside of the condition. Otherwise, your component would re-render in a loop until it crashes. Also, you can only update the state of the *currently rendering* component like this. Calling the `set` function of *another* component during rendering is an error. Finally, your `set` call should still [update state without mutation](#updating-objects-and-arrays-in-state) — this doesn’t mean you can break other rules of [pure functions.](https://react.dev/learn/keeping-components-pure)

This pattern can be hard to understand and is usually best avoided. However, it’s better than updating state in an effect. When you call the `set` function during render, React will re-render that component immediately after your component exits with a `return` statement, and before rendering the children. This way, children don’t need to render twice. The rest of your component function will still execute (and the result will be thrown away). If your condition is below all the Hook calls, you may add an early `return;` to restart rendering earlier.

---

## Troubleshooting

### I’ve updated the state, but logging gives me the old value

Calling the `set` function **does not change state in the running code**:

 $

```
function handleClick() {  console.log(count);  // 0  setCount(count + 1); // Request a re-render with 1  console.log(count);  // Still 0!  setTimeout(() => {    console.log(count); // Also 0!  }, 5000);}
```

/$

This is because [states behaves like a snapshot.](https://react.dev/learn/state-as-a-snapshot) Updating state requests another render with the new state value, but does not affect the `count` JavaScript variable in your already-running event handler.

If you need to use the next state, you can save it in a variable before passing it to the `set` function:

 $

```
const nextCount = count + 1;setCount(nextCount);console.log(count);     // 0console.log(nextCount); // 1
```

/$

---

### I’ve updated the state, but the screen doesn’t update

React will **ignore your update if the next state is equal to the previous state,** as determined by an [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. This usually happens when you change an object or an array in state directly:

 $

```
obj.x = 10;  // 🚩 Wrong: mutating existing objectsetObj(obj); // 🚩 Doesn't do anything
```

/$

You mutated an existing `obj` object and passed it back to `setObj`, so React ignored the update. To fix this, you need to ensure that you’re always [replacingobjects and arrays in state instead ofmutatingthem](#updating-objects-and-arrays-in-state):

 $

```
// ✅ Correct: creating a new objectsetObj({  ...obj,  x: 10});
```

/$

---

### I’m getting an error: “Too many re-renders”

You might get an error that says: `Too many re-renders. React limits the number of renders to prevent an infinite loop.` Typically, this means that you’re unconditionally setting state *during render*, so your component enters a loop: render, set state (which causes a render), render, set state (which causes a render), and so on. Very often, this is caused by a mistake in specifying an event handler:

 $

```
// 🚩 Wrong: calls the handler during renderreturn <button onClick={handleClick()}>Click me</button>// ✅ Correct: passes down the event handlerreturn <button onClick={handleClick}>Click me</button>// ✅ Correct: passes down an inline functionreturn <button onClick={(e) => handleClick(e)}>Click me</button>
```

/$

If you can’t find the cause of this error, click on the arrow next to the error in the console and look through the JavaScript stack to find the specific `set` function call responsible for the error.

---

### My initializer or updater function runs twice

In [Strict Mode](https://react.dev/reference/react/StrictMode), React will call some of your functions twice instead of once:

 $

```
function TodoList() {  // This component function will run twice for every render.  const [todos, setTodos] = useState(() => {    // This initializer function will run twice during initialization.    return createTodos();  });  function handleClick() {    setTodos(prevTodos => {      // This updater function will run twice for every click.      return [...prevTodos, createTodo()];    });  }  // ...
```

/$

This is expected and shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](https://react.dev/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component, initializer, and updater functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice the mistakes.

For example, this impure updater function mutates an array in state:

 $

```
setTodos(prevTodos => {  // 🚩 Mistake: mutating state  prevTodos.push(createTodo());});
```

/$

Because React calls your updater function twice, you’ll see the todo was added twice, so you’ll know that there is a mistake. In this example, you can fix the mistake by [replacing the array instead of mutating it](#updating-objects-and-arrays-in-state):

 $

```
setTodos(prevTodos => {  // ✅ Correct: replacing with new state  return [...prevTodos, createTodo()];});
```

/$

Now that this updater function is pure, calling it an extra time doesn’t make a difference in behavior. This is why React calling it twice helps you find mistakes. **Only component, initializer, and updater functions need to be pure.** Event handlers don’t need to be pure, so React will never call your event handlers twice.

Read [keeping components pure](https://react.dev/learn/keeping-components-pure) to learn more.

---

### I’m trying to set state to a function, but it gets called instead

You can’t put a function into state like this:

 $

```
const [fn, setFn] = useState(someFunction);function handleClick() {  setFn(someOtherFunction);}
```

/$

Because you’re passing a function, React assumes that `someFunction` is an [initializer function](#avoiding-recreating-the-initial-state), and that `someOtherFunction` is an [updater function](#updating-state-based-on-the-previous-state), so it tries to call them and store the result. To actually *store* a function, you have to put `() =>` before them in both cases. Then React will store the functions you pass.

 $

```
const [fn, setFn] = useState(() => someFunction);function handleClick() {  setFn(() => someOtherFunction);}
```

/$[PrevioususeRef](https://react.dev/reference/react/useRef)[NextuseSyncExternalStore](https://react.dev/reference/react/useSyncExternalStore)

---

# useSyncExternalStore

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useSyncExternalStore

`useSyncExternalStore` is a React Hook that lets you subscribe to an external store.

$

```
const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)
```

/$

- [Reference](#reference)
  - [useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)](#usesyncexternalstore)
- [Usage](#usage)
  - [Subscribing to an external store](#subscribing-to-an-external-store)
  - [Subscribing to a browser API](#subscribing-to-a-browser-api)
  - [Extracting the logic to a custom Hook](#extracting-the-logic-to-a-custom-hook)
  - [Adding support for server rendering](#adding-support-for-server-rendering)
- [Troubleshooting](#troubleshooting)
  - [I’m getting an error: “The result ofgetSnapshotshould be cached”](#im-getting-an-error-the-result-of-getsnapshot-should-be-cached)
  - [Mysubscribefunction gets called after every re-render](#my-subscribe-function-gets-called-after-every-re-render)

---

## Reference

### useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)

Call `useSyncExternalStore` at the top level of your component to read a value from an external data store.

 $

```
import { useSyncExternalStore } from 'react';import { todosStore } from './todoStore.js';function TodosApp() {  const todos = useSyncExternalStore(todosStore.subscribe, todosStore.getSnapshot);  // ...}
```

/$

It returns the snapshot of the data in the store. You need to pass two functions as arguments:

1. The `subscribe` function should subscribe to the store and return a function that unsubscribes.
2. The `getSnapshot` function should read a snapshot of the data from the store.

[See more examples below.](#usage)

#### Parameters

- `subscribe`: A function that takes a single `callback` argument and subscribes it to the store. When the store changes, it should invoke the provided `callback`, which will cause React to re-call `getSnapshot` and (if needed) re-render the component. The `subscribe` function should return a function that cleans up the subscription.
- `getSnapshot`: A function that returns a snapshot of the data in the store that’s needed by the component. While the store has not changed, repeated calls to `getSnapshot` must return the same value. If the store changes and the returned value is different (as compared by [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), React re-renders the component.
- **optional** `getServerSnapshot`: A function that returns the initial snapshot of the data in the store. It will be used only during server rendering and during hydration of server-rendered content on the client. The server snapshot must be the same between the client and the server, and is usually serialized and passed from the server to the client. If you omit this argument, rendering the component on the server will throw an error.

#### Returns

The current snapshot of the store which you can use in your rendering logic.

#### Caveats

- The store snapshot returned by `getSnapshot` must be immutable. If the underlying store has mutable data, return a new immutable snapshot if the data has changed. Otherwise, return a cached last snapshot.
- If a different `subscribe` function is passed during a re-render, React will re-subscribe to the store using the newly passed `subscribe` function. You can prevent this by declaring `subscribe` outside the component.
- If the store is mutated during a [non-blocking Transition update](https://react.dev/reference/react/useTransition), React will fall back to performing that update as blocking. Specifically, for every Transition update, React will call `getSnapshot` a second time just before applying changes to the DOM. If it returns a different value than when it was called originally, React will restart the update from scratch, this time applying it as a blocking update, to ensure that every component on screen is reflecting the same version of the store.
- It’s not recommended to *suspend* a render based on a store value returned by `useSyncExternalStore`. The reason is that mutations to the external store cannot be marked as [non-blocking Transition updates](https://react.dev/reference/react/useTransition), so they will trigger the nearest [Suspensefallback](https://react.dev/reference/react/Suspense), replacing already-rendered content on screen with a loading spinner, which typically makes a poor UX.
  For example, the following are discouraged:
   $
  ```
  const LazyProductDetailPage = lazy(() => import('./ProductDetailPage.js'));function ShoppingApp() {  const selectedProductId = useSyncExternalStore(...);  // ❌ Calling `use` with a Promise dependent on `selectedProductId`  const data = use(fetchItem(selectedProductId))  // ❌ Conditionally rendering a lazy component based on `selectedProductId`  return selectedProductId != null ? <LazyProductDetailPage /> : <FeaturedProducts />;}
  ```
  /$

---

## Usage

### Subscribing to an external store

Most of your React components will only read data from their [props,](https://react.dev/learn/passing-props-to-a-component) [state,](https://react.dev/reference/react/useState) and [context.](https://react.dev/reference/react/useContext) However, sometimes a component needs to read some data from some store outside of React that changes over time. This includes:

- Third-party state management libraries that hold state outside of React.
- Browser APIs that expose a mutable value and events to subscribe to its changes.

Call `useSyncExternalStore` at the top level of your component to read a value from an external data store.

 $

```
import { useSyncExternalStore } from 'react';import { todosStore } from './todoStore.js';function TodosApp() {  const todos = useSyncExternalStore(todosStore.subscribe, todosStore.getSnapshot);  // ...}
```

/$

It returns the snapshot of the data in the store. You need to pass two functions as arguments:

1. The `subscribe` function should subscribe to the store and return a function that unsubscribes.
2. The `getSnapshot` function should read a snapshot of the data from the store.

React will use these functions to keep your component subscribed to the store and re-render it on changes.

For example, in the sandbox below, `todosStore` is implemented as an external store that stores data outside of React. The `TodosApp` component connects to that external store with the `useSyncExternalStore` Hook.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useSyncExternalStore } from 'react';
import { todosStore } from './todoStore.js';

export default function TodosApp() {
  const todos = useSyncExternalStore(todosStore.subscribe, todosStore.getSnapshot);
  return (
    <>
      <button onClick={() => todosStore.addTodo()}>Add todo</button>
      <hr />
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </>
  );
}
```

/$

### Note

When possible, we recommend using built-in React state with [useState](https://react.dev/reference/react/useState) and [useReducer](https://react.dev/reference/react/useReducer) instead. The `useSyncExternalStore` API is mostly useful if you need to integrate with existing non-React code.

---

### Subscribing to a browser API

Another reason to add `useSyncExternalStore` is when you want to subscribe to some value exposed by the browser that changes over time. For example, suppose that you want your component to display whether the network connection is active. The browser exposes this information via a property called [navigator.onLine.](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine)

This value can change without React’s knowledge, so you should read it with `useSyncExternalStore`.

 $

```
import { useSyncExternalStore } from 'react';function ChatIndicator() {  const isOnline = useSyncExternalStore(subscribe, getSnapshot);  // ...}
```

/$

To implement the `getSnapshot` function, read the current value from the browser API:

 $

```
function getSnapshot() {  return navigator.onLine;}
```

/$

Next, you need to implement the `subscribe` function. For example, when `navigator.onLine` changes, the browser fires the [online](https://developer.mozilla.org/en-US/docs/Web/API/Window/online_event) and [offline](https://developer.mozilla.org/en-US/docs/Web/API/Window/offline_event) events on the `window` object. You need to subscribe the `callback` argument to the corresponding events, and then return a function that cleans up the subscriptions:

 $

```
function subscribe(callback) {  window.addEventListener('online', callback);  window.addEventListener('offline', callback);  return () => {    window.removeEventListener('online', callback);    window.removeEventListener('offline', callback);  };}
```

/$

Now React knows how to read the value from the external `navigator.onLine` API and how to subscribe to its changes. Disconnect your device from the network and notice that the component re-renders in response:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useSyncExternalStore } from 'react';

export default function ChatIndicator() {
  const isOnline = useSyncExternalStore(subscribe, getSnapshot);
  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;
}

function getSnapshot() {
  return navigator.onLine;
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

---

### Extracting the logic to a custom Hook

Usually you won’t write `useSyncExternalStore` directly in your components. Instead, you’ll typically call it from your own custom Hook. This lets you use the same external store from different components.

For example, this custom `useOnlineStatus` Hook tracks whether the network is online:

 $

```
import { useSyncExternalStore } from 'react';export function useOnlineStatus() {  const isOnline = useSyncExternalStore(subscribe, getSnapshot);  return isOnline;}function getSnapshot() {  // ...}function subscribe(callback) {  // ...}
```

/$

Now different components can call `useOnlineStatus` without repeating the underlying implementation:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useOnlineStatus } from './useOnlineStatus.js';

function StatusBar() {
  const isOnline = useOnlineStatus();
  return <h1>{isOnline ? '✅ Online' : '❌ Disconnected'}</h1>;
}

function SaveButton() {
  const isOnline = useOnlineStatus();

  function handleSaveClick() {
    console.log('✅ Progress saved');
  }

  return (
    <button disabled={!isOnline} onClick={handleSaveClick}>
      {isOnline ? 'Save progress' : 'Reconnecting...'}
    </button>
  );
}

export default function App() {
  return (
    <>
      <SaveButton />
      <StatusBar />
    </>
  );
}
```

/$

---

### Adding support for server rendering

If your React app uses [server rendering,](https://react.dev/reference/react-dom/server) your React components will also run outside the browser environment to generate the initial HTML. This creates a few challenges when connecting to an external store:

- If you’re connecting to a browser-only API, it won’t work because it does not exist on the server.
- If you’re connecting to a third-party data store, you’ll need its data to match between the server and client.

To solve these issues, pass a `getServerSnapshot` function as the third argument to `useSyncExternalStore`:

 $

```
import { useSyncExternalStore } from 'react';export function useOnlineStatus() {  const isOnline = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);  return isOnline;}function getSnapshot() {  return navigator.onLine;}function getServerSnapshot() {  return true; // Always show "Online" for server-generated HTML}function subscribe(callback) {  // ...}
```

/$

The `getServerSnapshot` function is similar to `getSnapshot`, but it runs only in two situations:

- It runs on the server when generating the HTML.
- It runs on the client during [hydration](https://react.dev/reference/react-dom/client/hydrateRoot), i.e. when React takes the server HTML and makes it interactive.

This lets you provide the initial snapshot value which will be used before the app becomes interactive. If there is no meaningful initial value for the server rendering, omit this argument to [force rendering on the client.](https://react.dev/reference/react/Suspense#providing-a-fallback-for-server-errors-and-client-only-content)

### Note

Make sure that `getServerSnapshot` returns the same exact data on the initial client render as it returned on the server. For example, if `getServerSnapshot` returned some prepopulated store content on the server, you need to transfer this content to the client. One way to do this is to emit a `<script>` tag during server rendering that sets a global like `window.MY_STORE_DATA`, and read from that global on the client in `getServerSnapshot`. Your external store should provide instructions on how to do that.

---

## Troubleshooting

### I’m getting an error: “The result ofgetSnapshotshould be cached”

This error means your `getSnapshot` function returns a new object every time it’s called, for example:

 $

```
function getSnapshot() {  // 🔴 Do not return always different objects from getSnapshot  return {    todos: myStore.todos  };}
```

/$

React will re-render the component if `getSnapshot` return value is different from the last time. This is why, if you always return a different value, you will enter an infinite loop and get this error.

Your `getSnapshot` object should only return a different object if something has actually changed. If your store contains immutable data, you can return that data directly:

 $

```
function getSnapshot() {  // ✅ You can return immutable data  return myStore.todos;}
```

/$

If your store data is mutable, your `getSnapshot` function should return an immutable snapshot of it. This means it *does* need to create new objects, but it shouldn’t do this for every single call. Instead, it should store the last calculated snapshot, and return the same snapshot as the last time if the data in the store has not changed. How you determine whether mutable data has changed depends on your mutable store.

---

### Mysubscribefunction gets called after every re-render

This `subscribe` function is defined *inside* a component so it is different on every re-render:

 $

```
function ChatIndicator() {  // 🚩 Always a different function, so React will resubscribe on every re-render  function subscribe() {    // ...  }    const isOnline = useSyncExternalStore(subscribe, getSnapshot);  // ...}
```

/$

React will resubscribe to your store if you pass a different `subscribe` function between re-renders. If this causes performance issues and you’d like to avoid resubscribing, move the `subscribe` function outside:

 $

```
// ✅ Always the same function, so React won't need to resubscribefunction subscribe() {  // ...}function ChatIndicator() {  const isOnline = useSyncExternalStore(subscribe, getSnapshot);  // ...}
```

/$

Alternatively, wrap `subscribe` into [useCallback](https://react.dev/reference/react/useCallback) to only resubscribe when some argument changes:

 $

```
function ChatIndicator({ userId }) {  // ✅ Same function as long as userId doesn't change  const subscribe = useCallback(() => {    // ...  }, [userId]);    const isOnline = useSyncExternalStore(subscribe, getSnapshot);  // ...}
```

/$[PrevioususeState](https://react.dev/reference/react/useState)[NextuseTransition](https://react.dev/reference/react/useTransition)
