# Managing State and more

# Managing State

[Learn React](https://react.dev/learn)

# Managing State

Intermediate

As your application grows, it helps to be more intentional about how your state is organized and how the data flows between your components. Redundant or duplicate state is a common source of bugs. In this chapter, you’ll learn how to structure your state well, how to keep your state update logic maintainable, and how to share state between distant components.

### In this chapter

- [How to think about UI changes as state changes](https://react.dev/learn/reacting-to-input-with-state)
- [How to structure state well](https://react.dev/learn/choosing-the-state-structure)
- [How to “lift state up” to share it between components](https://react.dev/learn/sharing-state-between-components)
- [How to control whether the state gets preserved or reset](https://react.dev/learn/preserving-and-resetting-state)
- [How to consolidate complex state logic in a function](https://react.dev/learn/extracting-state-logic-into-a-reducer)
- [How to pass information without “prop drilling”](https://react.dev/learn/passing-data-deeply-with-context)
- [How to scale state management as your app grows](https://react.dev/learn/scaling-up-with-reducer-and-context)

## Reacting to input with state

With React, you won’t modify the UI from code directly. For example, you won’t write commands like “disable the button”, “enable the button”, “show the success message”, etc. Instead, you will describe the UI you want to see for the different visual states of your component (“initial state”, “typing state”, “success state”), and then trigger the state changes in response to user input. This is similar to how designers think about UI.

Here is a quiz form built using React. Note how it uses the `status` state variable to determine whether to enable or disable the submit button, and whether to show the success message instead.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { useState } from 'react';
export default function Form() { const [answer, setAnswer] = useState(''); const [error, setError] = useState(null); const [status, setStatus] = useState('typing');
 if (status === 'success') { return <h1>That's right!</h1> }
 async function handleSubmit(e) { e.preventDefault(); setStatus('submitting'); try { await submitForm(answer); setStatus('success'); } catch (err) { setStatus('typing'); setError(err); } }
 function handleTextareaChange(e) { setAnswer(e.target.value); }
 return ( <> <h2>City quiz</h2> <p>        In which city is there a billboard that turns air into drinkable water? </p> <form onSubmit={handleSubmit}> <textarea value={answer}/$

## Ready to learn this topic?

Read **Reacting to Input with State** to learn how to approach interactions with a state-driven mindset.

[Read More](https://react.dev/learn/reacting-to-input-with-state)

---

## Choosing the state structure

Structuring state well can make a difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. The most important principle is that state shouldn’t contain redundant or duplicated information. If there’s unnecessary state, it’s easy to forget to update it, and introduce bugs!

For example, this form has a **redundant** `fullName` state variable:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [fullName, setFullName] = useState('');

  function handleFirstNameChange(e) {
    setFirstName(e.target.value);
    setFullName(e.target.value + ' ' + lastName);
  }

  function handleLastNameChange(e) {
    setLastName(e.target.value);
    setFullName(firstName + ' ' + e.target.value);
  }

  return (
    <>
      <h2>Let’s check you in</h2>
      <label>
        First name:{' '}
        <input
          value={firstName}
          onChange={handleFirstNameChange}
        />
      </label>
      <label>
        Last name:{' '}
        <input
          value={lastName}
          onChange={handleLastNameChange}
        />
      </label>
      <p>
        Your ticket will be issued to: <b>{fullName}</b>
      </p>
    </>
  );
}
```

/$

You can remove it and simplify the code by calculating `fullName` while the component is rendering:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  const fullName = firstName + ' ' + lastName;

  function handleFirstNameChange(e) {
    setFirstName(e.target.value);
  }

  function handleLastNameChange(e) {
    setLastName(e.target.value);
  }

  return (
    <>
      <h2>Let’s check you in</h2>
      <label>
        First name:{' '}
        <input
          value={firstName}
          onChange={handleFirstNameChange}
        />
      </label>
      <label>
        Last name:{' '}
        <input
          value={lastName}
          onChange={handleLastNameChange}
        />
      </label>
      <p>
        Your ticket will be issued to: <b>{fullName}</b>
      </p>
    </>
  );
}
```

/$

This might seem like a small change, but many bugs in React apps are fixed this way.

## Ready to learn this topic?

Read **Choosing the State Structure** to learn how to design the state shape to avoid bugs.

[Read More](https://react.dev/learn/choosing-the-state-structure)

---

## Sharing state between components

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as “lifting state up”, and it’s one of the most common things you will do writing React code.

In this example, only one panel should be active at a time. To achieve this, instead of keeping the active state inside each individual panel, the parent component holds the state and specifies the props for its children.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Accordion() {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <>
      <h2>Almaty, Kazakhstan</h2>
      <Panel
        title="About"
        isActive={activeIndex === 0}
        onShow={() => setActiveIndex(0)}
      >
        With a population of about 2 million, Almaty is Kazakhstan's largest city. From 1929 to 1997, it was its capital city.
      </Panel>
      <Panel
        title="Etymology"
        isActive={activeIndex === 1}
        onShow={() => setActiveIndex(1)}
      >
        The name comes from <span lang="kk-KZ">алма</span>, the Kazakh word for "apple" and is often translated as "full of apples". In fact, the region surrounding Almaty is thought to be the ancestral home of the apple, and the wild <i lang="la">Malus sieversii</i> is considered a likely candidate for the ancestor of the modern domestic apple.
      </Panel>
    </>
  );
}

function Panel({
  title,
  children,
  isActive,
  onShow
}) {
  return (
    <section className="panel">
      <h3>{title}</h3>
      {isActive ? (
        <p>{children}</p>
      ) : (
        <button onClick={onShow}>
          Show
        </button>
      )}
    </section>
  );
}
```

/$

## Ready to learn this topic?

Read **Sharing State Between Components** to learn how to lift state up and keep components in sync.

[Read More](https://react.dev/learn/sharing-state-between-components)

---

## Preserving and resetting state

When you re-render a component, React needs to decide which parts of the tree to keep (and update), and which parts to discard or re-create from scratch. In most cases, React’s automatic behavior works well enough. By default, React preserves the parts of the tree that “match up” with the previously rendered component tree.

However, sometimes this is not what you want. In this chat app, typing a message and then switching the recipient does not reset the input. This can make the user accidentally send a message to the wrong person:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';

export default function Messenger() {
  const [to, setTo] = useState(contacts[0]);
  return (
    <div>
      <ContactList
        contacts={contacts}
        selectedContact={to}
        onSelect={contact => setTo(contact)}
      />
      <Chat contact={to} />
    </div>
  )
}

const contacts = [
  { name: 'Taylor', email: 'taylor@mail.com' },
  { name: 'Alice', email: 'alice@mail.com' },
  { name: 'Bob', email: 'bob@mail.com' }
];
```

/$

React lets you override the default behavior, and *force* a component to reset its state by passing it a different `key`, like `<Chat key={email} />`. This tells React that if the recipient is different, it should be considered a *different* `Chat` component that needs to be re-created from scratch with the new data (and UI like inputs). Now switching between the recipients resets the input field—even though you render the same component.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';

export default function Messenger() {
  const [to, setTo] = useState(contacts[0]);
  return (
    <div>
      <ContactList
        contacts={contacts}
        selectedContact={to}
        onSelect={contact => setTo(contact)}
      />
      <Chat key={to.email} contact={to} />
    </div>
  )
}

const contacts = [
  { name: 'Taylor', email: 'taylor@mail.com' },
  { name: 'Alice', email: 'alice@mail.com' },
  { name: 'Bob', email: 'bob@mail.com' }
];
```

/$

## Ready to learn this topic?

Read **Preserving and Resetting State** to learn the lifetime of state and how to control it.

[Read More](https://react.dev/learn/preserving-and-resetting-state)

---

## Extracting state logic into a reducer

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called “reducer”. Your event handlers become concise because they only specify the user “actions”. At the bottom of the file, the reducer function specifies how the state should update in response to each action!

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(
    tasksReducer,
    initialTasks
  );

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
      task: task
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask
        onAddTask={handleAddTask}
      />
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
      return [...tasks, {
        id: action.id,
        text: action.text,
        done: false
      }];
    }
    case 'changed': {
      return tasks.map(t => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

let nextId = 3;
const initialTasks = [
  { id: 0, text: 'Visit Kafka Museum', done: true },
  { id: 1, text: 'Watch a puppet show', done: false },
  { id: 2, text: 'Lennon Wall pic', done: false }
];
```

/$

## Ready to learn this topic?

Read **Extracting State Logic into a Reducer** to learn how to consolidate logic in the reducer function.

[Read More](https://react.dev/learn/extracting-state-logic-into-a-reducer)

---

## Passing data deeply with context

Usually, you will pass information from a parent component to a child component via props. But passing props can become inconvenient if you need to pass some prop through many components, or if many components need the same information. Context lets the parent component make some information available to any component in the tree below it—no matter how deep it is—without passing it explicitly through props.

Here, the `Heading` component determines its heading level by “asking” the closest `Section` for its level. Each `Section` tracks its own level by asking the parent `Section` and adding one to it. Every `Section` provides information to all components below it without passing props—it does that through context.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function Page() {
  return (
    <Section>
      <Heading>Title</Heading>
      <Section>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Section>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Section>
            <Heading>Sub-sub-heading</Heading>
            <Heading>Sub-sub-heading</Heading>
            <Heading>Sub-sub-heading</Heading>
          </Section>
        </Section>
      </Section>
    </Section>
  );
}
```

/$

## Ready to learn this topic?

Read **Passing Data Deeply with Context** to learn about using context as an alternative to passing props.

[Read More](https://react.dev/learn/passing-data-deeply-with-context)

---

## Scaling up with reducer and context

Reducers let you consolidate a component’s state update logic. Context lets you pass information deep down to other components. You can combine reducers and context together to manage state of a complex screen.

With this approach, a parent component with complex state manages it with a reducer. Other components anywhere deep in the tree can read its state via context. They can also dispatch actions to update that state.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import { TasksProvider } from './TasksContext.js';

export default function TaskApp() {
  return (
    <TasksProvider>
      <h1>Day off in Kyoto</h1>
      <AddTask />
      <TaskList />
    </TasksProvider>
  );
}
```

/$

## Ready to learn this topic?

Read **Scaling Up with Reducer and Context** to learn how state management scales in a growing app.

[Read More](https://react.dev/learn/scaling-up-with-reducer-and-context)

---

## What’s next?

Head over to [Reacting to Input with State](https://react.dev/learn/reacting-to-input-with-state) to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about [Escape Hatches](https://react.dev/learn/escape-hatches)?

[PreviousUpdating Arrays in State](https://react.dev/learn/updating-arrays-in-state)[NextReacting to Input with State](https://react.dev/learn/reacting-to-input-with-state)

---

# Manipulating the DOM with Refs

[Learn React](https://react.dev/learn)[Escape Hatches](https://react.dev/learn/escape-hatches)

# Manipulating the DOM with Refs

React automatically updates the [DOM](https://developer.mozilla.org/docs/Web/API/Document_Object_Model/Introduction) to match your render output, so your components won’t often need to manipulate it. However, sometimes you might need access to the DOM elements managed by React—for example, to focus a node, scroll to it, or measure its size and position. There is no built-in way to do those things in React, so you will need a *ref* to the DOM node.

### You will learn

- How to access a DOM node managed by React with the `ref` attribute
- How the `ref` JSX attribute relates to the `useRef` Hook
- How to access another component’s DOM node
- In which cases it’s safe to modify the DOM managed by React

## Getting a ref to the node

To access a DOM node managed by React, first, import the `useRef` Hook:

 $

```
import { useRef } from 'react';
```

/$

Then, use it to declare a ref inside your component:

 $

```
const myRef = useRef(null);
```

/$

Finally, pass your ref as the `ref` attribute to the JSX tag for which you want to get the DOM node:

 $

```
<div ref={myRef}>
```

/$

The `useRef` Hook returns an object with a single property called `current`. Initially, `myRef.current` will be `null`. When React creates a DOM node for this `<div>`, React will put a reference to this node into `myRef.current`. You can then access this DOM node from your [event handlers](https://react.dev/learn/responding-to-events) and use the built-in [browser APIs](https://developer.mozilla.org/docs/Web/API/Element) defined on it.

 $

```
// You can use any browser APIs, for example:myRef.current.scrollIntoView();
```

/$

### Example: Focusing a text input

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

To implement this:

1. Declare `inputRef` with the `useRef` Hook.
2. Pass it as `<input ref={inputRef}>`. This tells React to **put this<input>’s DOM node intoinputRef.current.**
3. In the `handleClick` function, read the input DOM node from `inputRef.current` and call [focus()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus) on it with `inputRef.current.focus()`.
4. Pass the `handleClick` event handler to `<button>` with `onClick`.

While DOM manipulation is the most common use case for refs, the `useRef` Hook can be used for storing other things outside React, like timer IDs. Similarly to state, refs remain between renders. Refs are like state variables that don’t trigger re-renders when you set them. Read about refs in [Referencing Values with Refs.](https://react.dev/learn/referencing-values-with-refs)

### Example: Scrolling to an element

You can have more than a single ref in a component. In this example, there is a carousel of three images. Each button centers an image by calling the browser [scrollIntoView()](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView) method on the corresponding DOM node:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';

export default function CatFriends() {
  const firstCatRef = useRef(null);
  const secondCatRef = useRef(null);
  const thirdCatRef = useRef(null);

  function handleScrollToFirstCat() {
    firstCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

  function handleScrollToSecondCat() {
    secondCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

  function handleScrollToThirdCat() {
    thirdCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

  return (
    <>
      <nav>
        <button onClick={handleScrollToFirstCat}>
          Neo
        </button>
        <button onClick={handleScrollToSecondCat}>
          Millie
        </button>
        <button onClick={handleScrollToThirdCat}>
          Bella
        </button>
      </nav>
      <div>
        <ul>
          <li>
            <img
              src="https://placecats.com/neo/300/200"
              alt="Neo"
              ref={firstCatRef}
            />
          </li>
          <li>
            <img
              src="https://placecats.com/millie/200/200"
              alt="Millie"
              ref={secondCatRef}
            />
          </li>
          <li>
            <img
              src="https://placecats.com/bella/199/200"
              alt="Bella"
              ref={thirdCatRef}
            />
          </li>
        </ul>
      </div>
    </>
  );
}
```

/$

##### Deep Dive

#### How to manage a list of refs using a ref callback

In the above examples, there is a predefined number of refs. However, sometimes you might need a ref to each item in the list, and you don’t know how many you will have. Something like this **wouldn’t work**:

$

```
<ul>  {items.map((item) => {    // Doesn't work!    const ref = useRef(null);    return <li ref={ref} />;  })}</ul>
```

/$

This is because **Hooks must only be called at the top-level of your component.** You can’t call `useRef` in a loop, in a condition, or inside a `map()` call.

One possible way around this is to get a single ref to their parent element, and then use DOM manipulation methods like [querySelectorAll](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll) to “find” the individual child nodes from it. However, this is brittle and can break if your DOM structure changes.

Another solution is to **pass a function to therefattribute.** This is called a [refcallback.](https://react.dev/reference/react-dom/components/common#ref-callback) React will call your ref callback with the DOM node when it’s time to set the ref, and call the cleanup function returned from the callback when it’s time to clear it. This lets you maintain your own array or a [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map), and access any ref by its index or some kind of ID.

This example shows how you can use this approach to scroll to an arbitrary node in a long list:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useState } from "react";

export default function CatFriends() {
  const itemsRef = useRef(null);
  const [catList, setCatList] = useState(setupCatList);

  function scrollToCat(cat) {
    const map = getMap();
    const node = map.get(cat);
    node.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  function getMap() {
    if (!itemsRef.current) {
      // Initialize the Map on first usage.
      itemsRef.current = new Map();
    }
    return itemsRef.current;
  }

  return (
    <>
      <nav>
        <button onClick={() => scrollToCat(catList[0])}>Neo</button>
        <button onClick={() => scrollToCat(catList[5])}>Millie</button>
        <button onClick={() => scrollToCat(catList[8])}>Bella</button>
      </nav>
      <div>
        <ul>
          {catList.map((cat) => (
            <li
              key={cat.id}
              ref={(node) => {
                const map = getMap();
                map.set(cat, node);

                return () => {
                  map.delete(cat);
                };
              }}
            >
              <img src={cat.imageUrl} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function setupCatList() {
  const catCount = 10;
  const catList = new Array(catCount)
  for (let i = 0; i < catCount; i++) {
    let imageUrl = '';
    if (i < 5) {
      imageUrl = "https://placecats.com/neo/320/240";
    } else if (i < 8) {
      imageUrl = "https://placecats.com/millie/320/240";
    } else {
      imageUrl = "https://placecats.com/bella/320/240";
    }
    catList[i] = {
      id: i,
      imageUrl,
    };
  }
  return catList;
}
```

/$

In this example, `itemsRef` doesn’t hold a single DOM node. Instead, it holds a [Map](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map) from item ID to a DOM node. ([Refs can hold any values!](https://react.dev/learn/referencing-values-with-refs)) The [refcallback](https://react.dev/reference/react-dom/components/common#ref-callback) on every list item takes care to update the Map:

$

```
<li  key={cat.id}  ref={node => {    const map = getMap();    // Add to the Map    map.set(cat, node);    return () => {      // Remove from the Map      map.delete(cat);    };  }}>
```

/$

This lets you read individual DOM nodes from the Map later.

### Note

When Strict Mode is enabled, ref callbacks will run twice in development.

Read more about [how this helps find bugs](https://react.dev/reference/react/StrictMode#fixing-bugs-found-by-re-running-ref-callbacks-in-development) in callback refs.

## Accessing another component’s DOM nodes

### Pitfall

Refs are an escape hatch. Manually manipulating *another* component’s DOM nodes can make your code fragile.

You can pass refs from parent component to child components [just like any other prop](https://react.dev/learn/passing-props-to-a-component).

 $

```
import { useRef } from 'react';function MyInput({ ref }) {  return <input ref={ref} />;}function MyForm() {  const inputRef = useRef(null);  return <MyInput ref={inputRef} />}
```

/$

In the above example, a ref is created in the parent component, `MyForm`, and is passed to the child component, `MyInput`. `MyInput` then passes the ref to `<input>`. Because `<input>` is a [built-in component](https://react.dev/reference/react-dom/components/common) React sets the `.current` property of the ref to the `<input>` DOM element.

The `inputRef` created in `MyForm` now points to the `<input>` DOM element returned by `MyInput`. A click handler created in `MyForm` can access `inputRef` and call `focus()` to set the focus on `<input>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';

function MyInput({ ref }) {
  return <input ref={ref} />;
}

export default function MyForm() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

/$

##### Deep Dive

#### Exposing a subset of the API with an imperative handle

In the above example, the ref passed to `MyInput` is passed on to the original DOM input element. This lets the parent component call `focus()` on it. However, this also lets the parent component do something else—for example, change its CSS styles. In uncommon cases, you may want to restrict the exposed functionality. You can do that with [useImperativeHandle](https://react.dev/reference/react/useImperativeHandle):

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useImperativeHandle } from "react";

function MyInput({ ref }) {
  const realInputRef = useRef(null);
  useImperativeHandle(ref, () => ({
    // Only expose focus and nothing else
    focus() {
      realInputRef.current.focus();
    },
  }));
  return <input ref={realInputRef} />;
};

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <MyInput ref={inputRef} />
      <button onClick={handleClick}>Focus the input</button>
    </>
  );
}
```

/$

Here, `realInputRef` inside `MyInput` holds the actual input DOM node. However, [useImperativeHandle](https://react.dev/reference/react/useImperativeHandle) instructs React to provide your own special object as the value of a ref to the parent component. So `inputRef.current` inside the `Form` component will only have the `focus` method. In this case, the ref “handle” is not the DOM node, but the custom object you create inside [useImperativeHandle](https://react.dev/reference/react/useImperativeHandle) call.

## When React attaches the refs

In React, every update is split in [two phases](https://react.dev/learn/render-and-commit#step-3-react-commits-changes-to-the-dom):

- During **render,** React calls your components to figure out what should be on the screen.
- During **commit,** React applies changes to the DOM.

In general, you [don’t want](https://react.dev/learn/referencing-values-with-refs#best-practices-for-refs) to access refs during rendering. That goes for refs holding DOM nodes as well. During the first render, the DOM nodes have not yet been created, so `ref.current` will be `null`. And during the rendering of updates, the DOM nodes haven’t been updated yet. So it’s too early to read them.

React sets `ref.current` during the commit. Before updating the DOM, React sets the affected `ref.current` values to `null`. After updating the DOM, React immediately sets them to the corresponding DOM nodes.

**Usually, you will access refs from event handlers.** If you want to do something with a ref, but there is no particular event to do it in, you might need an Effect. We will discuss Effects on the next pages.

##### Deep Dive

#### Flushing state updates synchronously with flushSync

Consider code like this, which adds a new todo and scrolls the screen down to the last child of the list. Notice how, for some reason, it always scrolls to the todo that was *just before* the last added one:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef } from 'react';

export default function TodoList() {
  const listRef = useRef(null);
  const [text, setText] = useState('');
  const [todos, setTodos] = useState(
    initialTodos
  );

  function handleAdd() {
    const newTodo = { id: nextId++, text: text };
    setText('');
    setTodos([ ...todos, newTodo]);
    listRef.current.lastChild.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest'
    });
  }

  return (
    <>
      <button onClick={handleAdd}>
        Add
      </button>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <ul ref={listRef}>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </>
  );
}

let nextId = 0;
let initialTodos = [];
for (let i = 0; i < 20; i++) {
  initialTodos.push({
    id: nextId++,
    text: 'Todo #' + (i + 1)
  });
}
```

/$

The issue is with these two lines:

$

```
setTodos([ ...todos, newTodo]);listRef.current.lastChild.scrollIntoView();
```

/$

In React, [state updates are queued.](https://react.dev/learn/queueing-a-series-of-state-updates) Usually, this is what you want. However, here it causes a problem because `setTodos` does not immediately update the DOM. So the time you scroll the list to its last element, the todo has not yet been added. This is why scrolling always “lags behind” by one item.

To fix this issue, you can force React to update (“flush”) the DOM synchronously. To do this, import `flushSync` from `react-dom` and **wrap the state update** into a `flushSync` call:

$

```
flushSync(() => {  setTodos([ ...todos, newTodo]);});listRef.current.lastChild.scrollIntoView();
```

/$

This will instruct React to update the DOM synchronously right after the code wrapped in `flushSync` executes. As a result, the last todo will already be in the DOM by the time you try to scroll to it:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef } from 'react';
import { flushSync } from 'react-dom';

export default function TodoList() {
  const listRef = useRef(null);
  const [text, setText] = useState('');
  const [todos, setTodos] = useState(
    initialTodos
  );

  function handleAdd() {
    const newTodo = { id: nextId++, text: text };
    flushSync(() => {
      setText('');
      setTodos([ ...todos, newTodo]);
    });
    listRef.current.lastChild.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest'
    });
  }

  return (
    <>
      <button onClick={handleAdd}>
        Add
      </button>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <ul ref={listRef}>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </>
  );
}

let nextId = 0;
let initialTodos = [];
for (let i = 0; i < 20; i++) {
  initialTodos.push({
    id: nextId++,
    text: 'Todo #' + (i + 1)
  });
}
```

/$

## Best practices for DOM manipulation with refs

Refs are an escape hatch. You should only use them when you have to “step outside React”. Common examples of this include managing focus, scroll position, or calling browser APIs that React does not expose.

If you stick to non-destructive actions like focusing and scrolling, you shouldn’t encounter any problems. However, if you try to **modify** the DOM manually, you can risk conflicting with the changes React is making.

To illustrate this problem, this example includes a welcome message and two buttons. The first button toggles its presence using [conditional rendering](https://react.dev/learn/conditional-rendering) and [state](https://react.dev/learn/state-a-components-memory), as you would usually do in React. The second button uses the [remove()DOM API](https://developer.mozilla.org/en-US/docs/Web/API/Element/remove) to forcefully remove it from the DOM outside of React’s control.

Try pressing “Toggle with setState” a few times. The message should disappear and appear again. Then press “Remove from the DOM”. This will forcefully remove it. Finally, press “Toggle with setState”:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef } from 'react';

export default function Counter() {
  const [show, setShow] = useState(true);
  const ref = useRef(null);

  return (
    <div>
      <button
        onClick={() => {
          setShow(!show);
        }}>
        Toggle with setState
      </button>
      <button
        onClick={() => {
          ref.current.remove();
        }}>
        Remove from the DOM
      </button>
      {show && <p ref={ref}>Hello world</p>}
    </div>
  );
}
```

/$

After you’ve manually removed the DOM element, trying to use `setState` to show it again will lead to a crash. This is because you’ve changed the DOM, and React doesn’t know how to continue managing it correctly.

**Avoid changing DOM nodes managed by React.** Modifying, adding children to, or removing children from elements that are managed by React can lead to inconsistent visual results or crashes like above.

However, this doesn’t mean that you can’t do it at all. It requires caution. **You can safely modify parts of the DOM that React hasno reasonto update.** For example, if some `<div>` is always empty in the JSX, React won’t have a reason to touch its children list. Therefore, it is safe to manually add or remove elements there.

## Recap

- Refs are a generic concept, but most often you’ll use them to hold DOM elements.
- You instruct React to put a DOM node into `myRef.current` by passing `<div ref={myRef}>`.
- Usually, you will use refs for non-destructive actions like focusing, scrolling, or measuring DOM elements.
- A component doesn’t expose its DOM nodes by default. You can opt into exposing a DOM node by using the `ref` prop.
- Avoid changing DOM nodes managed by React.
- If you do modify DOM nodes managed by React, modify parts that React has no reason to update.

## Try out some challenges

#### Challenge1of4:Play and pause the video

In this example, the button toggles a state variable to switch between a playing and a paused state. However, in order to actually play or pause the video, toggling state is not enough. You also need to call [play()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play) and [pause()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/pause) on the DOM element for the `<video>`. Add a ref to it, and make the button work.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef } from 'react';

export default function VideoPlayer() {
  const [isPlaying, setIsPlaying] = useState(false);

  function handleClick() {
    const nextIsPlaying = !isPlaying;
    setIsPlaying(nextIsPlaying);
  }

  return (
    <>
      <button onClick={handleClick}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <video width="250">
        <source
          src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
          type="video/mp4"
        />
      </video>
    </>
  )
}
```

/$

For an extra challenge, keep the “Play” button in sync with whether the video is playing even if the user right-clicks the video and plays it using the built-in browser media controls. You might want to listen to `onPlay` and `onPause` on the video to do that.

[PreviousReferencing Values with Refs](https://react.dev/learn/referencing-values-with-refs)[NextSynchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
