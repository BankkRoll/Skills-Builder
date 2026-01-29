# Extracting State Logic into a Reducer and more

# Extracting State Logic into a Reducer

[Learn React](https://react.dev/learn)[Managing State](https://react.dev/learn/managing-state)

# Extracting State Logic into a Reducer

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called a *reducer.*

### You will learn

- What a reducer function is
- How to refactor `useState` to `useReducer`
- When to use a reducer
- How to write one well

## Consolidate state logic with a reducer

As your components grow in complexity, it can get harder to see at a glance all the different ways in which a component’s state gets updated. For example, the `TaskApp` component below holds an array of `tasks` in state and uses three different event handlers to add, remove, and edit tasks:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { useState } from 'react';import AddTask from './AddTask.js';import TaskList from './TaskList.js';
export default function TaskApp() { const [tasks, setTasks] = useState(initialTasks);
 function handleAddTask(text) { setTasks([ ...tasks, { id: nextId++, text: text, done: false, }, ]); }
 function handleChangeTask(task) { setTasks( tasks.map((t) => { if (t.id === task.id) { return task; } else { return t; } }) ); }
 function handleDeleteTask(taskId) { setTasks(tasks.filter((t) => t.id !== taskId)); }
 return ( <>/$

Each of its event handlers calls `setTasks` in order to update the state. As this component grows, so does the amount of state logic sprinkled throughout it. To reduce this complexity and keep all your logic in one easy-to-access place, you can move that state logic into a single function outside your component, **called a “reducer”.**

Reducers are a different way to handle state. You can migrate from `useState` to `useReducer` in three steps:

1. **Move** from setting state to dispatching actions.
2. **Write** a reducer function.
3. **Use** the reducer from your component.

### Step 1: Move from setting state to dispatching actions

Your event handlers currently specify *what to do* by setting state:

 $

```
function handleAddTask(text) {  setTasks([    ...tasks,    {      id: nextId++,      text: text,      done: false,    },  ]);}function handleChangeTask(task) {  setTasks(    tasks.map((t) => {      if (t.id === task.id) {        return task;      } else {        return t;      }    })  );}function handleDeleteTask(taskId) {  setTasks(tasks.filter((t) => t.id !== taskId));}
```

/$

Remove all the state setting logic. What you are left with are three event handlers:

- `handleAddTask(text)` is called when the user presses “Add”.
- `handleChangeTask(task)` is called when the user toggles a task or presses “Save”.
- `handleDeleteTask(taskId)` is called when the user presses “Delete”.

Managing state with reducers is slightly different from directly setting state. Instead of telling React “what to do” by setting state, you specify “what the user just did” by dispatching “actions” from your event handlers. (The state update logic will live elsewhere!) So instead of “setting `tasks`” via an event handler, you’re dispatching an “added/changed/deleted a task” action. This is more descriptive of the user’s intent.

 $

```
function handleAddTask(text) {  dispatch({    type: 'added',    id: nextId++,    text: text,  });}function handleChangeTask(task) {  dispatch({    type: 'changed',    task: task,  });}function handleDeleteTask(taskId) {  dispatch({    type: 'deleted',    id: taskId,  });}
```

/$

The object you pass to `dispatch` is called an “action”:

 $

```
function handleDeleteTask(taskId) {  dispatch(    // "action" object:    {      type: 'deleted',      id: taskId,    }  );}
```

/$

It is a regular JavaScript object. You decide what to put in it, but generally it should contain the minimal information about *what happened*. (You will add the `dispatch` function itself in a later step.)

### Note

An action object can have any shape.

By convention, it is common to give it a string `type` that describes what happened, and pass any additional information in other fields. The `type` is specific to a component, so in this example either `'added'` or `'added_task'` would be fine. Choose a name that says what happened!

$

```
dispatch({  // specific to component  type: 'what_happened',  // other fields go here});
```

/$

### Step 2: Write a reducer function

A reducer function is where you will put your state logic. It takes two arguments, the current state and the action object, and it returns the next state:

 $

```
function yourReducer(state, action) {  // return next state for React to set}
```

/$

React will set the state to what you return from the reducer.

To move your state setting logic from your event handlers to a reducer function in this example, you will:

1. Declare the current state (`tasks`) as the first argument.
2. Declare the `action` object as the second argument.
3. Return the *next* state from the reducer (which React will set the state to).

Here is all the state setting logic migrated to a reducer function:

 $

```
function tasksReducer(tasks, action) {  if (action.type === 'added') {    return [      ...tasks,      {        id: action.id,        text: action.text,        done: false,      },    ];  } else if (action.type === 'changed') {    return tasks.map((t) => {      if (t.id === action.task.id) {        return action.task;      } else {        return t;      }    });  } else if (action.type === 'deleted') {    return tasks.filter((t) => t.id !== action.id);  } else {    throw Error('Unknown action: ' + action.type);  }}
```

/$

Because the reducer function takes state (`tasks`) as an argument, you can **declare it outside of your component.** This decreases the indentation level and can make your code easier to read.

### Note

The code above uses if/else statements, but it’s a convention to use [switch statements](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/switch) inside reducers. The result is the same, but it can be easier to read switch statements at a glance.

We’ll be using them throughout the rest of this documentation like so:

$

```
function tasksReducer(tasks, action) {  switch (action.type) {    case 'added': {      return [        ...tasks,        {          id: action.id,          text: action.text,          done: false,        },      ];    }    case 'changed': {      return tasks.map((t) => {        if (t.id === action.task.id) {          return action.task;        } else {          return t;        }      });    }    case 'deleted': {      return tasks.filter((t) => t.id !== action.id);    }    default: {      throw Error('Unknown action: ' + action.type);    }  }}
```

/$

We recommend wrapping each `case` block into the `{` and `}` curly braces so that variables declared inside of different `case`s don’t clash with each other. Also, a `case` should usually end with a `return`. If you forget to `return`, the code will “fall through” to the next `case`, which can lead to mistakes!

If you’re not yet comfortable with switch statements, using if/else is completely fine.

##### Deep Dive

#### Why are reducers called this way?

Although reducers can “reduce” the amount of code inside your component, they are actually named after the [reduce()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce) operation that you can perform on arrays.

The `reduce()` operation lets you take an array and “accumulate” a single value out of many:

$

```
const arr = [1, 2, 3, 4, 5];const sum = arr.reduce(  (result, number) => result + number); // 1 + 2 + 3 + 4 + 5
```

/$

The function you pass to `reduce` is known as a “reducer”. It takes the *result so far* and the *current item,* then it returns the *next result.* React reducers are an example of the same idea: they take the *state so far* and the *action*, and return the *next state.* In this way, they accumulate actions over time into state.

You could even use the `reduce()` method with an `initialState` and an array of `actions` to calculate the final state by passing your reducer function to it:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import tasksReducer from './tasksReducer.js';

let initialState = [];
let actions = [
  {type: 'added', id: 1, text: 'Visit Kafka Museum'},
  {type: 'added', id: 2, text: 'Watch a puppet show'},
  {type: 'deleted', id: 1},
  {type: 'added', id: 3, text: 'Lennon Wall pic'},
];

let finalState = actions.reduce(tasksReducer, initialState);

const output = document.getElementById('output');
output.textContent = JSON.stringify(finalState, null, 2);
```

/$

You probably won’t need to do this yourself, but this is similar to what React does!

### Step 3: Use the reducer from your component

Finally, you need to hook up the `tasksReducer` to your component. Import the `useReducer` Hook from React:

 $

```
import { useReducer } from 'react';
```

/$

Then you can replace `useState`:

 $

```
const [tasks, setTasks] = useState(initialTasks);
```

/$

with `useReducer` like so:

 $

```
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

/$

The `useReducer` Hook is similar to `useState`—you must pass it an initial state and it returns a stateful value and a way to set state (in this case, the dispatch function). But it’s a little different.

The `useReducer` Hook takes two arguments:

1. A reducer function
2. An initial state

And it returns:

1. A stateful value
2. A dispatch function (to “dispatch” user actions to the reducer)

Now it’s fully wired up! Here, the reducer is declared at the bottom of the component file:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...tasks,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }
    case 'changed': {
      return tasks.map((t) => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: 'Visit Kafka Museum', done: true},
  {id: 1, text: 'Watch a puppet show', done: false},
  {id: 2, text: 'Lennon Wall pic', done: false},
];
```

/$

If you want, you can even move the reducer to a different file:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import tasksReducer from './tasksReducer.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: 'Visit Kafka Museum', done: true},
  {id: 1, text: 'Watch a puppet show', done: false},
  {id: 2, text: 'Lennon Wall pic', done: false},
];
```

/$

Component logic can be easier to read when you separate concerns like this. Now the event handlers only specify *what happened* by dispatching actions, and the reducer function determines *how the state updates* in response to them.

## ComparinguseStateanduseReducer

Reducers are not without downsides! Here’s a few ways you can compare them:

- **Code size:** Generally, with `useState` you have to write less code upfront. With `useReducer`, you have to write both a reducer function *and* dispatch actions. However, `useReducer` can help cut down on the code if many event handlers modify state in a similar way.
- **Readability:** `useState` is very easy to read when the state updates are simple. When they get more complex, they can bloat your component’s code and make it difficult to scan. In this case, `useReducer` lets you cleanly separate the *how* of update logic from the *what happened* of event handlers.
- **Debugging:** When you have a bug with `useState`, it can be difficult to tell *where* the state was set incorrectly, and *why*. With `useReducer`, you can add a console log into your reducer to see every state update, and *why* it happened (due to which `action`). If each `action` is correct, you’ll know that the mistake is in the reducer logic itself. However, you have to step through more code than with `useState`.
- **Testing:** A reducer is a pure function that doesn’t depend on your component. This means that you can export and test it separately in isolation. While generally it’s best to test components in a more realistic environment, for complex state update logic it can be useful to assert that your reducer returns a particular state for a particular initial state and action.
- **Personal preference:** Some people like reducers, others don’t. That’s okay. It’s a matter of preference. You can always convert between `useState` and `useReducer` back and forth: they are equivalent!

We recommend using a reducer if you often encounter bugs due to incorrect state updates in some component, and want to introduce more structure to its code. You don’t have to use reducers for everything: feel free to mix and match! You can even `useState` and `useReducer` in the same component.

## Writing reducers well

Keep these two tips in mind when writing reducers:

- **Reducers must be pure.** Similar to [state updater functions](https://react.dev/learn/queueing-a-series-of-state-updates), reducers run during rendering! (Actions are queued until the next render.) This means that reducers [must be pure](https://react.dev/learn/keeping-components-pure)—same inputs always result in the same output. They should not send requests, schedule timeouts, or perform any side effects (operations that impact things outside the component). They should update [objects](https://react.dev/learn/updating-objects-in-state) and [arrays](https://react.dev/learn/updating-arrays-in-state) without mutations.
- **Each action describes a single user interaction, even if that leads to multiple changes in the data.** For example, if a user presses “Reset” on a form with five fields managed by a reducer, it makes more sense to dispatch one `reset_form` action rather than five separate `set_field` actions. If you log every action in a reducer, that log should be clear enough for you to reconstruct what interactions or responses happened in what order. This helps with debugging!

## Writing concise reducers with Immer

Just like with [updating objects](https://react.dev/learn/updating-objects-in-state#write-concise-update-logic-with-immer) and [arrays](https://react.dev/learn/updating-arrays-in-state#write-concise-update-logic-with-immer) in regular state, you can use the Immer library to make reducers more concise. Here, [useImmerReducer](https://github.com/immerjs/use-immer#useimmerreducer) lets you mutate the state with `push` or `arr[i] =` assignment:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
{
  "dependencies": {
    "immer": "1.7.3",
    "react": "latest",
    "react-dom": "latest",
    "react-scripts": "latest",
    "use-immer": "0.5.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --env=jsdom",
    "eject": "react-scripts eject"
  },
  "devDependencies": {}
}
```

/$

Reducers must be pure, so they shouldn’t mutate state. But Immer provides you with a special `draft` object which is safe to mutate. Under the hood, Immer will create a copy of your state with the changes you made to the `draft`. This is why reducers managed by `useImmerReducer` can mutate their first argument and don’t need to return state.

## Recap

- To convert from `useState` to `useReducer`:
  1. Dispatch actions from event handlers.
  2. Write a reducer function that returns the next state for a given state and action.
  3. Replace `useState` with `useReducer`.
- Reducers require you to write a bit more code, but they help with debugging and testing.
- Reducers must be pure.
- Each action describes a single user interaction.
- Use Immer if you want to write reducers in a mutating style.

## Try out some challenges

#### Challenge1of4:Dispatch actions from event handlers

Currently, the event handlers in `ContactList.js` and `Chat.js` have `// TODO` comments. This is why typing into the input doesn’t work, and clicking on the buttons doesn’t change the selected recipient.

Replace these two `// TODO`s with the code to `dispatch` the corresponding actions. To see the expected shape and the type of the actions, check the reducer in `messengerReducer.js`. The reducer is already written so you won’t need to change it. You only need to dispatch the actions in `ContactList.js` and `Chat.js`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';
import { initialState, messengerReducer } from './messengerReducer';

export default function Messenger() {
  const [state, dispatch] = useReducer(messengerReducer, initialState);
  const message = state.message;
  const contact = contacts.find((c) => c.id === state.selectedId);
  return (
    <div>
      <ContactList
        contacts={contacts}
        selectedId={state.selectedId}
        dispatch={dispatch}
      />
      <Chat
        key={contact.id}
        message={message}
        contact={contact}
        dispatch={dispatch}
      />
    </div>
  );
}

const contacts = [
  {id: 0, name: 'Taylor', email: 'taylor@mail.com'},
  {id: 1, name: 'Alice', email: 'alice@mail.com'},
  {id: 2, name: 'Bob', email: 'bob@mail.com'},
];
```

/$[PreviousPreserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)[NextPassing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)

---

# Importing and Exporting Components

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Importing and Exporting Components

The magic of components lies in their reusability: you can create components that are composed of other components. But as you nest more and more components, it often makes sense to start splitting them into different files. This lets you keep your files easy to scan and reuse components in more places.

### You will learn

- What a root component file is
- How to import and export a component
- When to use default and named imports and exports
- How to import and export multiple components from one file
- How to split components into multiple files

## The root component file

In [Your First Component](https://react.dev/learn/your-first-component), you made a `Profile` component and a `Gallery` component that renders it:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)function Profile() { return ( <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" /> );}
export default function Gallery() { return ( <section> <h1>Amazing scientists</h1> <Profile /> <Profile /> <Profile /> </section> );}
/$

These currently live in a **root component file,** named `App.js` in this example. Depending on your setup, your root component could be in another file, though. If you use a framework with file-based routing, such as Next.js, your root component will be different for every page.

## Exporting and importing a component

What if you want to change the landing screen in the future and put a list of science books there? Or place all the profiles somewhere else? It makes sense to move `Gallery` and `Profile` out of the root component file. This will make them more modular and reusable in other files. You can move a component in three steps:

1. **Make** a new JS file to put the components in.
2. **Export** your function component from that file (using either [default](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/export#using_the_default_export) or [named](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/export#using_named_exports) exports).
3. **Import** it in the file where you’ll use the component (using the corresponding technique for importing [default](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import#importing_defaults) or [named](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import#import_a_single_export_from_a_module) exports).

Here both `Profile` and `Gallery` have been moved out of `App.js` into a new file called `Gallery.js`. Now you can change `App.js` to import `Gallery` from `Gallery.js`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Gallery from './Gallery.js';

export default function App() {
  return (
    <Gallery />
  );
}
```

/$

Notice how this example is broken down into two component files now:

1. `Gallery.js`:
  - Defines the `Profile` component which is only used within the same file and is not exported.
  - Exports the `Gallery` component as a **default export.**
2. `App.js`:
  - Imports `Gallery` as a **default import** from `Gallery.js`.
  - Exports the root `App` component as a **default export.**

### Note

You may encounter files that leave off the `.js` file extension like so:

$

```
import Gallery from './Gallery';
```

/$

Either `'./Gallery.js'` or `'./Gallery'` will work with React, though the former is closer to how [native ES Modules](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Modules) work.

##### Deep Dive

#### Default vs named exports

There are two primary ways to export values with JavaScript: default exports and named exports. So far, our examples have only used default exports. But you can use one or both of them in the same file. **A file can have no more than onedefaultexport, but it can have as manynamedexports as you like.**

![Default and named exports](https://react.dev/images/docs/illustrations/i_import-export.svg)

How you export your component dictates how you must import it. You will get an error if you try to import a default export the same way you would a named export! This chart can help you keep track:

| Syntax | Export statement | Import statement |
| --- | --- | --- |
| Default | export default function Button() {} | import Button from './Button.js'; |
| Named | export function Button() {} | import { Button } from './Button.js'; |

When you write a *default* import, you can put any name you want after `import`. For example, you could write `import Banana from './Button.js'` instead and it would still provide you with the same default export. In contrast, with named imports, the name has to match on both sides. That’s why they are called *named* imports!

**People often use default exports if the file exports only one component, and use named exports if it exports multiple components and values.** Regardless of which coding style you prefer, always give meaningful names to your component functions and the files that contain them. Components without names, like `export default () => {}`, are discouraged because they make debugging harder.

## Exporting and importing multiple components from the same file

What if you want to show just one `Profile` instead of a gallery? You can export the `Profile` component, too. But `Gallery.js` already has a *default* export, and you can’t have *two* default exports. You could create a new file with a default export, or you could add a *named* export for `Profile`. **A file can only have one default export, but it can have numerous named exports!**

### Note

To reduce the potential confusion between default and named exports, some teams choose to only stick to one style (default or named), or avoid mixing them in a single file. Do what works best for you!

First, **export** `Profile` from `Gallery.js` using a named export (no `default` keyword):

 $

```
export function Profile() {  // ...}
```

/$

Then, **import** `Profile` from `Gallery.js` to `App.js` using a named import (with the curly braces):

 $

```
import { Profile } from './Gallery.js';
```

/$

Finally, **render** `<Profile />` from the `App` component:

 $

```
export default function App() {  return <Profile />;}
```

/$

Now `Gallery.js` contains two exports: a default `Gallery` export, and a named `Profile` export. `App.js` imports both of them. Try editing `<Profile />` to `<Gallery />` and back in this example:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Gallery from './Gallery.js';
import { Profile } from './Gallery.js';

export default function App() {
  return (
    <Profile />
  );
}
```

/$

Now you’re using a mix of default and named exports:

- `Gallery.js`:
  - Exports the `Profile` component as a **named export calledProfile.**
  - Exports the `Gallery` component as a **default export.**
- `App.js`:
  - Imports `Profile` as a **named import calledProfile** from `Gallery.js`.
  - Imports `Gallery` as a **default import** from `Gallery.js`.
  - Exports the root `App` component as a **default export.**

## Recap

On this page you learned:

- What a root component file is
- How to import and export a component
- When and how to use default and named imports and exports
- How to export multiple components from the same file

## Try out some challenges

#### Challenge1of1:Split the components further

Currently, `Gallery.js` exports both `Profile` and `Gallery`, which is a bit confusing.

Move the `Profile` component to its own `Profile.js`, and then change the `App` component to render both `<Profile />` and `<Gallery />` one after another.

You may use either a default or a named export for `Profile`, but make sure that you use the corresponding import syntax in both `App.js` and `Gallery.js`! You can refer to the table from the deep dive above:

| Syntax | Export statement | Import statement |
| --- | --- | --- |
| Default | export default function Button() {} | import Button from './Button.js'; |
| Named | export function Button() {} | import { Button } from './Button.js'; |

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
// Move me to Profile.js!
export function Profile() {
  return (
    <img
      src="https://i.imgur.com/QIrZWGIs.jpg"
      alt="Alan L. Hart"
    />
  );
}

export default function Gallery() {
  return (
    <section>
      <h1>Amazing scientists</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

/$

After you get it working with one kind of exports, make it work with the other kind.

[PreviousYour First Component](https://react.dev/learn/your-first-component)[NextWriting Markup with JSX](https://react.dev/learn/writing-markup-with-jsx)

---

# Installation

[Learn React](https://react.dev/learn)

# Installation

React has been designed from the start for gradual adoption. You can use as little or as much React as you need. Whether you want to get a taste of React, add some interactivity to an HTML page, or start a complex React-powered app, this section will help you get started.

## Try React

You don’t need to install anything to play with React. Try editing this sandbox!

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)function Greeting({ name }) { return <h1>Hello, {name}</h1>;}
export default function App() { return <Greeting name="world" />}
/$

You can edit it directly or open it in a new tab by pressing the “Fork” button in the upper right corner.

Most pages in the React documentation contain sandboxes like this. Outside of the React documentation, there are many online sandboxes that support React: for example, [CodeSandbox](https://codesandbox.io/s/new), [StackBlitz](https://stackblitz.com/fork/react), or [CodePen.](https://codepen.io/pen?template=QWYVwWN)

To try React locally on your computer, [download this HTML page.](https://gist.githubusercontent.com/gaearon/0275b1e1518599bbeafcde4722e79ed1/raw/db72dcbf3384ee1708c4a07d3be79860db04bff0/example.html) Open it in your editor and in your browser!

## Creating a React App

If you want to start a new React app, you can [create a React app](https://react.dev/learn/creating-a-react-app) using a recommended framework.

## Build a React App from Scratch

If a framework is not a good fit for your project, you prefer to build your own framework, or you just want to learn the basics of a React app you can [build a React app from scratch](https://react.dev/learn/build-a-react-app-from-scratch).

## Add React to an existing project

If want to try using React in your existing app or a website, you can [add React to an existing project.](https://react.dev/learn/add-react-to-an-existing-project)

### Note

#### Should I use Create React App?

No. Create React App has been deprecated. For more information, see [Sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app).

## Next steps

Head to the [Quick Start](https://react.dev/learn) guide for a tour of the most important React concepts you will encounter every day.

[PreviousThinking in React](https://react.dev/learn/thinking-in-react)[NextCreating a React App](https://react.dev/learn/creating-a-react-app)

---

# JavaScript in JSX with Curly Braces

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# JavaScript in JSX with Curly Braces

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to open a window to JavaScript.

### You will learn

- How to pass strings with quotes
- How to reference a JavaScript variable inside JSX with curly braces
- How to call a JavaScript function inside JSX with curly braces
- How to use a JavaScript object inside JSX with curly braces

## Passing strings with quotes

When you want to pass a string attribute to JSX, you put it in single or double quotes:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)export default function Avatar() { return ( <img className="avatar" src="https://i.imgur.com/7vQD0fPs.jpg" alt="Gregorio Y. Zara" /> );}
/$

Here, `"https://i.imgur.com/7vQD0fPs.jpg"` and `"Gregorio Y. Zara"` are being passed as strings.

But what if you want to dynamically specify the `src` or `alt` text? You could **use a value from JavaScript by replacing"and"with{and}**:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Avatar() {
  const avatar = 'https://i.imgur.com/7vQD0fPs.jpg';
  const description = 'Gregorio Y. Zara';
  return (
    <img
      className="avatar"
      src={avatar}
      alt={description}
    />
  );
}
```

/$

Notice the difference between `className="avatar"`, which specifies an `"avatar"` CSS class name that makes the image round, and `src={avatar}` that reads the value of the JavaScript variable called `avatar`. That’s because curly braces let you work with JavaScript right there in your markup!

## Using curly braces: A window into the JavaScript world

JSX is a special way of writing JavaScript. That means it’s possible to use JavaScript inside it—with curly braces `{ }`. The example below first declares a name for the scientist, `name`, then embeds it with curly braces inside the `<h1>`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  const name = 'Gregorio Y. Zara';
  return (
    <h1>{name}'s To Do List</h1>
  );
}
```

/$

Try changing the `name`’s value from `'Gregorio Y. Zara'` to `'Hedy Lamarr'`. See how the list title changes?

Any JavaScript expression will work between curly braces, including function calls like `formatDate()`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
const today = new Date();

function formatDate(date) {
  return new Intl.DateTimeFormat(
    'en-US',
    { weekday: 'long' }
  ).format(date);
}

export default function TodoList() {
  return (
    <h1>To Do List for {formatDate(today)}</h1>
  );
}
```

/$

### Where to use curly braces

You can only use curly braces in two ways inside JSX:

1. **As text** directly inside a JSX tag: `<h1>{name}'s To Do List</h1>` works, but `<{tag}>Gregorio Y. Zara's To Do List</{tag}>`  will not.
2. **As attributes** immediately following the `=` sign: `src={avatar}` will read the `avatar` variable, but `src="{avatar}"` will pass the string `"{avatar}"`.

## Using “double curlies”: CSS and other objects in JSX

In addition to strings, numbers, and other JavaScript expressions, you can even pass objects in JSX. Objects are also denoted with curly braces, like `{ name: "Hedy Lamarr", inventions: 5 }`. Therefore, to pass a JS object in JSX, you must wrap the object in another pair of curly braces: `person={{ name: "Hedy Lamarr", inventions: 5 }}`.

You may see this with inline CSS styles in JSX. React does not require you to use inline styles (CSS classes work great for most cases). But when you need an inline style, you pass an object to the `style` attribute:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  return (
    <ul style={{
      backgroundColor: 'black',
      color: 'pink'
    }}>
      <li>Improve the videophone</li>
      <li>Prepare aeronautics lectures</li>
      <li>Work on the alcohol-fuelled engine</li>
    </ul>
  );
}
```

/$

Try changing the values of `backgroundColor` and `color`.

You can really see the JavaScript object inside the curly braces when you write it like this:

 $

```
<ul style={  {    backgroundColor: 'black',    color: 'pink'  }}>
```

/$

The next time you see `{{` and `}}` in JSX, know that it’s nothing more than an object inside the JSX curlies!

### Pitfall

Inline `style` properties are written in camelCase. For example, HTML `<ul style="background-color: black">` would be written as `<ul style={{ backgroundColor: 'black' }}>`  in your component.

## More fun with JavaScript objects and curly braces

You can move several expressions into one object, and reference them in your JSX inside curly braces:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person.name}'s Todos</h1>
      <img
        className="avatar"
        src="https://i.imgur.com/7vQD0fPs.jpg"
        alt="Gregorio Y. Zara"
      />
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
        <li>Work on the alcohol-fuelled engine</li>
      </ul>
    </div>
  );
}
```

/$

In this example, the `person` JavaScript object contains a `name` string and a `theme` object:

 $

```
const person = {  name: 'Gregorio Y. Zara',  theme: {    backgroundColor: 'black',    color: 'pink'  }};
```

/$

The component can use these values from `person` like so:

 $

```
<div style={person.theme}>  <h1>{person.name}'s Todos</h1>
```

/$

JSX is very minimal as a templating language because it lets you organize data and logic using JavaScript.

## Recap

Now you know almost everything about JSX:

- JSX attributes inside quotes are passed as strings.
- Curly braces let you bring JavaScript logic and variables into your markup.
- They work inside the JSX tag content or immediately after `=` in attributes.
- `{{` and `}}` is not special syntax: it’s a JavaScript object tucked inside JSX curly braces.

## Try out some challenges

#### Challenge1of3:Fix the mistake

This code crashes with an error saying `Objects are not valid as a React child`:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person}'s Todos</h1>
      <img
        className="avatar"
        src="https://i.imgur.com/7vQD0fPs.jpg"
        alt="Gregorio Y. Zara"
      />
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
        <li>Work on the alcohol-fuelled engine</li>
      </ul>
    </div>
  );
}
```

/$

Can you find the problem?

[PreviousWriting Markup with JSX](https://react.dev/learn/writing-markup-with-jsx)[NextPassing Props to a Component](https://react.dev/learn/passing-props-to-a-component)
