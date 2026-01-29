# Reacting to Input with State and more

# Reacting to Input with State

[Learn React](https://react.dev/learn)[Managing State](https://react.dev/learn/managing-state)

# Reacting to Input with State

React provides a declarative way to manipulate the UI. Instead of manipulating individual pieces of the UI directly, you describe the different states that your component can be in, and switch between them in response to the user input. This is similar to how designers think about the UI.

### You will learn

- How declarative UI programming differs from imperative UI programming
- How to enumerate the different visual states your component can be in
- How to trigger the changes between the different visual states from code

## How declarative UI compares to imperative

When you design UI interactions, you probably think about how the UI *changes* in response to user actions. Consider a form that lets the user submit an answer:

- When you type something into the form, the “Submit” button **becomes enabled.**
- When you press “Submit”, both the form and the button **become disabled,** and a spinner **appears.**
- If the network request succeeds, the form **gets hidden,** and the “Thank you” message **appears.**
- If the network request fails, an error message **appears,** and the form **becomes enabled** again.

In **imperative programming,** the above corresponds directly to how you implement interaction. You have to write the exact instructions to manipulate the UI depending on what just happened. Here’s another way to think about this: imagine riding next to someone in a car and telling them turn by turn where to go.

 ![In a car driven by an anxious-looking person representing JavaScript, a passenger orders the driver to execute a sequence of complicated turn by turn navigations.](https://react.dev/images/docs/illustrations/i_imperative-ui-programming.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

They don’t know where you want to go, they just follow your commands. (And if you get the directions wrong, you end up in the wrong place!) It’s called *imperative* because you have to “command” each element, from the spinner to the button, telling the computer *how* to update the UI.

In this example of imperative UI programming, the form is built *without* React. It only uses the browser [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model):

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
async function handleFormSubmit(e) {
  e.preventDefault();
  disable(textarea);
  disable(button);
  show(loadingMessage);
  hide(errorMessage);
  try {
    await submitForm(textarea.value);
    show(successMessage);
    hide(form);
  } catch (err) {
    show(errorMessage);
    errorMessage.textContent = err.message;
  } finally {
    hide(loadingMessage);
    enable(textarea);
    enable(button);
  }
}

function handleTextareaChange() {
  if (textarea.value.length === 0) {
    disable(button);
  } else {
    enable(button);
  }
}

function hide(el) {
  el.style.display = 'none';
}

function show(el) {
  el.style.display = '';
}

function enable(el) {
  el.disabled = false;
}

function disable(el) {
  el.disabled = true;
}

function submitForm(answer) {
  // Pretend it's hitting the network.
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (answer.toLowerCase() === 'istanbul') {
        resolve();
      } else {
        reject(new Error('Good guess but a wrong answer. Try again!'));
      }
    }, 1500);
  });
}

let form = document.getElementById('form');
let textarea = document.getElementById('textarea');
let button = document.getElementById('button');
let loadingMessage = document.getElementById('loading');
let errorMessage = document.getElementById('error');
let successMessage = document.getElementById('success');
form.onsubmit = handleFormSubmit;
textarea.oninput = handleTextareaChange;
```

/$

Manipulating the UI imperatively works well enough for isolated examples, but it gets exponentially more difficult to manage in more complex systems. Imagine updating a page full of different forms like this one. Adding a new UI element or a new interaction would require carefully checking all existing code to make sure you haven’t introduced a bug (for example, forgetting to show or hide something).

React was built to solve this problem.

In React, you don’t directly manipulate the UI—meaning you don’t enable, disable, show, or hide components directly. Instead, you **declare what you want to show,** and React figures out how to update the UI. Think of getting into a taxi and telling the driver where you want to go instead of telling them exactly where to turn. It’s the driver’s job to get you there, and they might even know some shortcuts you haven’t considered!

 ![In a car driven by React, a passenger asks to be taken to a specific place on the map. React figures out how to do that.](https://react.dev/images/docs/illustrations/i_declarative-ui-programming.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Thinking about UI declaratively

You’ve seen how to implement a form imperatively above. To better understand how to think in React, you’ll walk through reimplementing this UI in React below:

1. **Identify** your component’s different visual states
2. **Determine** what triggers those state changes
3. **Represent** the state in memory using `useState`
4. **Remove** any non-essential state variables
5. **Connect** the event handlers to set the state

### Step 1: Identify your component’s different visual states

In computer science, you may hear about a [“state machine”](https://en.wikipedia.org/wiki/Finite-state_machine) being in one of several “states”. If you work with a designer, you may have seen mockups for different “visual states”. React stands at the intersection of design and computer science, so both of these ideas are sources of inspiration.

First, you need to visualize all the different “states” of the UI the user might see:

- **Empty**: Form has a disabled “Submit” button.
- **Typing**: Form has an enabled “Submit” button.
- **Submitting**: Form is completely disabled. Spinner is shown.
- **Success**: “Thank you” message is shown instead of a form.
- **Error**: Same as Typing state, but with an extra error message.

Just like a designer, you’ll want to “mock up” or create “mocks” for the different states before you add logic. For example, here is a mock for just the visual part of the form. This mock is controlled by a prop called `status` with a default value of `'empty'`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Form({
  status = 'empty'
}) {
  if (status === 'success') {
    return <h1>That's right!</h1>
  }
  return (
    <>
      <h2>City quiz</h2>
      <p>
        In which city is there a billboard that turns air into drinkable water?
      </p>
      <form>
        <textarea />
        <br />
        <button>
          Submit
        </button>
      </form>
    </>
  )
}
```

/$

You could call that prop anything you like, the naming is not important. Try editing `status = 'empty'` to `status = 'success'` to see the success message appear. Mocking lets you quickly iterate on the UI before you wire up any logic. Here is a more fleshed out prototype of the same component, still “controlled” by the `status` prop:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Form({
  // Try 'submitting', 'error', 'success':
  status = 'empty'
}) {
  if (status === 'success') {
    return <h1>That's right!</h1>
  }
  return (
    <>
      <h2>City quiz</h2>
      <p>
        In which city is there a billboard that turns air into drinkable water?
      </p>
      <form>
        <textarea disabled={
          status === 'submitting'
        } />
        <br />
        <button disabled={
          status === 'empty' ||
          status === 'submitting'
        }>
          Submit
        </button>
        {status === 'error' &&
          <p className="Error">
            Good guess but a wrong answer. Try again!
          </p>
        }
      </form>
      </>
  );
}
```

/$

##### Deep Dive

#### Displaying many visual states at once

If a component has a lot of visual states, it can be convenient to show them all on one page:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Form from './Form.js';

let statuses = [
  'empty',
  'typing',
  'submitting',
  'success',
  'error',
];

export default function App() {
  return (
    <>
      {statuses.map(status => (
        <section key={status}>
          <h4>Form ({status}):</h4>
          <Form status={status} />
        </section>
      ))}
    </>
  );
}
```

/$

Pages like this are often called “living styleguides” or “storybooks”.

### Step 2: Determine what triggers those state changes

You can trigger state updates in response to two kinds of inputs:

- **Human inputs,** like clicking a button, typing in a field, navigating a link.
- **Computer inputs,** like a network response arriving, a timeout completing, an image loading.

 ![A finger.](https://react.dev/images/docs/illustrations/i_inputs1.png)Human inputs![Ones and zeroes.](https://react.dev/images/docs/illustrations/i_inputs2.png)Computer inputs

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

In both cases, **you must setstate variablesto update the UI.** For the form you’re developing, you will need to change state in response to a few different inputs:

- **Changing the text input** (human) should switch it from the *Empty* state to the *Typing* state or back, depending on whether the text box is empty or not.
- **Clicking the Submit button** (human) should switch it to the *Submitting* state.
- **Successful network response** (computer) should switch it to the *Success* state.
- **Failed network response** (computer) should switch it to the *Error* state with the matching error message.

### Note

Notice that human inputs often require [event handlers](https://react.dev/learn/responding-to-events)!

To help visualize this flow, try drawing each state on paper as a labeled circle, and each change between two states as an arrow. You can sketch out many flows this way and sort out bugs long before implementation.

 ![Flow chart moving left to right with 5 nodes. The first node labeled 'empty' has one edge labeled 'start typing' connected to a node labeled 'typing'. That node has one edge labeled 'press submit' connected to a node labeled 'submitting', which has two edges. The left edge is labeled 'network error' connecting to a node labeled 'error'. The right edge is labeled 'network success' connecting to a node labeled 'success'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fresponding_to_input_flow.dark.png&w=1920&q=75)![Flow chart moving left to right with 5 nodes. The first node labeled 'empty' has one edge labeled 'start typing' connected to a node labeled 'typing'. That node has one edge labeled 'press submit' connected to a node labeled 'submitting', which has two edges. The left edge is labeled 'network error' connecting to a node labeled 'error'. The right edge is labeled 'network success' connecting to a node labeled 'success'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fresponding_to_input_flow.png&w=1920&q=75)

Form states

### Step 3: Represent the state in memory withuseState

Next you’ll need to represent the visual states of your component in memory with [useState.](https://react.dev/reference/react/useState) Simplicity is key: each piece of state is a “moving piece”, and **you want as few “moving pieces” as possible.** More complexity leads to more bugs!

Start with the state that *absolutely must* be there. For example, you’ll need to store the `answer` for the input, and the `error` (if it exists) to store the last error:

 $

```
const [answer, setAnswer] = useState('');const [error, setError] = useState(null);
```

/$

Then, you’ll need a state variable representing which one of the visual states that you want to display. There’s usually more than a single way to represent that in memory, so you’ll need to experiment with it.

If you struggle to think of the best way immediately, start by adding enough state that you’re *definitely* sure that all the possible visual states are covered:

 $

```
const [isEmpty, setIsEmpty] = useState(true);const [isTyping, setIsTyping] = useState(false);const [isSubmitting, setIsSubmitting] = useState(false);const [isSuccess, setIsSuccess] = useState(false);const [isError, setIsError] = useState(false);
```

/$

Your first idea likely won’t be the best, but that’s ok—refactoring state is a part of the process!

### Step 4: Remove any non-essential state variables

You want to avoid duplication in the state content so you’re only tracking what is essential. Spending a little time on refactoring your state structure will make your components easier to understand, reduce duplication, and avoid unintended meanings. Your goal is to **prevent the cases where the state in memory doesn’t represent any valid UI that you’d want a user to see.** (For example, you never want to show an error message and disable the input at the same time, or the user won’t be able to correct the error!)

Here are some questions you can ask about your state variables:

- **Does this state cause a paradox?** For example, `isTyping` and `isSubmitting` can’t both be `true`. A paradox usually means that the state is not constrained enough. There are four possible combinations of two booleans, but only three correspond to valid states. To remove the “impossible” state, you can combine these into a `status` that must be one of three values: `'typing'`, `'submitting'`, or `'success'`.
- **Is the same information available in another state variable already?** Another paradox: `isEmpty` and `isTyping` can’t be `true` at the same time. By making them separate state variables, you risk them going out of sync and causing bugs. Fortunately, you can remove `isEmpty` and instead check `answer.length === 0`.
- **Can you get the same information from the inverse of another state variable?** `isError` is not needed because you can check `error !== null` instead.

After this clean-up, you’re left with 3 (down from 7!) *essential* state variables:

 $

```
const [answer, setAnswer] = useState('');const [error, setError] = useState(null);const [status, setStatus] = useState('typing'); // 'typing', 'submitting', or 'success'
```

/$

You know they are essential, because you can’t remove any of them without breaking the functionality.

##### Deep Dive

#### Eliminating “impossible” states with a reducer

These three variables are a good enough representation of this form’s state. However, there are still some intermediate states that don’t fully make sense. For example, a non-null `error` doesn’t make sense when `status` is `'success'`. To model the state more precisely, you can [extract it into a reducer.](https://react.dev/learn/extracting-state-logic-into-a-reducer) Reducers let you unify multiple state variables into a single object and consolidate all the related logic!

### Step 5: Connect the event handlers to set state

Lastly, create event handlers that update the state. Below is the final form, with all event handlers wired up:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('typing');

  if (status === 'success') {
    return <h1>That's right!</h1>
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus('submitting');
    try {
      await submitForm(answer);
      setStatus('success');
    } catch (err) {
      setStatus('typing');
      setError(err);
    }
  }

  function handleTextareaChange(e) {
    setAnswer(e.target.value);
  }

  return (
    <>
      <h2>City quiz</h2>
      <p>
        In which city is there a billboard that turns air into drinkable water?
      </p>
      <form onSubmit={handleSubmit}>
        <textarea
          value={answer}
          onChange={handleTextareaChange}
          disabled={status === 'submitting'}
        />
        <br />
        <button disabled={
          answer.length === 0 ||
          status === 'submitting'
        }>
          Submit
        </button>
        {error !== null &&
          <p className="Error">
            {error.message}
          </p>
        }
      </form>
    </>
  );
}

function submitForm(answer) {
  // Pretend it's hitting the network.
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      let shouldError = answer.toLowerCase() !== 'lima'
      if (shouldError) {
        reject(new Error('Good guess but a wrong answer. Try again!'));
      } else {
        resolve();
      }
    }, 1500);
  });
}
```

/$

Although this code is longer than the original imperative example, it is much less fragile. Expressing all interactions as state changes lets you later introduce new visual states without breaking existing ones. It also lets you change what should be displayed in each state without changing the logic of the interaction itself.

## Recap

- Declarative programming means describing the UI for each visual state rather than micromanaging the UI (imperative).
- When developing a component:
  1. Identify all its visual states.
  2. Determine the human and computer triggers for state changes.
  3. Model the state with `useState`.
  4. Remove non-essential state to avoid bugs and paradoxes.
  5. Connect the event handlers to set state.

## Try out some challenges

#### Challenge1of3:Add and remove a CSS class

Make it so that clicking on the picture *removes* the `background--active` CSS class from the outer `<div>`, but *adds* the `picture--active` class to the `<img>`. Clicking the background again should restore the original CSS classes.

Visually, you should expect that clicking on the picture removes the purple background and highlights the picture border. Clicking outside the picture highlights the background, but removes the picture border highlight.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Picture() {
  return (
    <div className="background background--active">
      <img
        className="picture"
        alt="Rainbow houses in Kampung Pelangi, Indonesia"
        src="https://i.imgur.com/5qwVYb1.jpeg"
      />
    </div>
  );
}
```

/$[PreviousManaging State](https://react.dev/learn/managing-state)[NextChoosing the State Structure](https://react.dev/learn/choosing-the-state-structure)

---

# Referencing Values with Refs

[Learn React](https://react.dev/learn)[Escape Hatches](https://react.dev/learn/escape-hatches)

# Referencing Values with Refs

When you want a component to “remember” some information, but you don’t want that information to [trigger new renders](https://react.dev/learn/render-and-commit), you can use a *ref*.

### You will learn

- How to add a ref to your component
- How to update a ref’s value
- How refs are different from state
- How to use refs safely

## Adding a ref to your component

You can add a ref to your component by importing the `useRef` Hook from React:

 $

```
import { useRef } from 'react';
```

/$

Inside your component, call the `useRef` Hook and pass the initial value that you want to reference as the only argument. For example, here is a ref to the value `0`:

 $

```
const ref = useRef(0);
```

/$

`useRef` returns an object like this:

 $

```
{   current: 0 // The value you passed to useRef}
```

/$ ![An arrow with 'current' written on it stuffed into a pocket with 'ref' written on it.](https://react.dev/images/docs/illustrations/i_ref.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

You can access the current value of that ref through the `ref.current` property. This value is intentionally mutable, meaning you can both read and write to it. It’s like a secret pocket of your component that React doesn’t track. (This is what makes it an “escape hatch” from React’s one-way data flow—more on that below!)

Here, a button will increment `ref.current` on every click:

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

The ref points to a number, but, like [state](https://react.dev/learn/state-a-components-memory), you could point to anything: a string, an object, or even a function. Unlike state, ref is a plain JavaScript object with the `current` property that you can read and modify.

Note that **the component doesn’t re-render with every increment.** Like state, refs are retained by React between re-renders. However, setting state re-renders a component. Changing a ref does not!

## Example: building a stopwatch

You can combine refs and state in a single component. For example, let’s make a stopwatch that the user can start or stop by pressing a button. In order to display how much time has passed since the user pressed “Start”, you will need to keep track of when the Start button was pressed and what the current time is. **This information is used for rendering, so you’ll keep it in state:**

 $

```
const [startTime, setStartTime] = useState(null);const [now, setNow] = useState(null);
```

/$

When the user presses “Start”, you’ll use [setInterval](https://developer.mozilla.org/docs/Web/API/setInterval) in order to update the time every 10 milliseconds:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Stopwatch() {
  const [startTime, setStartTime] = useState(null);
  const [now, setNow] = useState(null);

  function handleStart() {
    // Start counting.
    setStartTime(Date.now());
    setNow(Date.now());

    setInterval(() => {
      // Update the current time every 10ms.
      setNow(Date.now());
    }, 10);
  }

  let secondsPassed = 0;
  if (startTime != null && now != null) {
    secondsPassed = (now - startTime) / 1000;
  }

  return (
    <>
      <h1>Time passed: {secondsPassed.toFixed(3)}</h1>
      <button onClick={handleStart}>
        Start
      </button>
    </>
  );
}
```

/$

When the “Stop” button is pressed, you need to cancel the existing interval so that it stops updating the `now` state variable. You can do this by calling [clearInterval](https://developer.mozilla.org/en-US/docs/Web/API/clearInterval), but you need to give it the interval ID that was previously returned by the `setInterval` call when the user pressed Start. You need to keep the interval ID somewhere. **Since the interval ID is not used for rendering, you can keep it in a ref:**

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef } from 'react';

export default function Stopwatch() {
  const [startTime, setStartTime] = useState(null);
  const [now, setNow] = useState(null);
  const intervalRef = useRef(null);

  function handleStart() {
    setStartTime(Date.now());
    setNow(Date.now());

    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setNow(Date.now());
    }, 10);
  }

  function handleStop() {
    clearInterval(intervalRef.current);
  }

  let secondsPassed = 0;
  if (startTime != null && now != null) {
    secondsPassed = (now - startTime) / 1000;
  }

  return (
    <>
      <h1>Time passed: {secondsPassed.toFixed(3)}</h1>
      <button onClick={handleStart}>
        Start
      </button>
      <button onClick={handleStop}>
        Stop
      </button>
    </>
  );
}
```

/$

When a piece of information is used for rendering, keep it in state. When a piece of information is only needed by event handlers and changing it doesn’t require a re-render, using a ref may be more efficient.

## Differences between refs and state

Perhaps you’re thinking refs seem less “strict” than state—you can mutate them instead of always having to use a state setting function, for instance. But in most cases, you’ll want to use state. Refs are an “escape hatch” you won’t need often. Here’s how state and refs compare:

| refs | state |
| --- | --- |
| useRef(initialValue)returns{ current: initialValue } | useState(initialValue)returns the current value of a state variable and a state setter function ([value, setValue]) |
| Doesn’t trigger re-render when you change it. | Triggers re-render when you change it. |
| Mutable—you can modify and updatecurrent’s value outside of the rendering process. | ”Immutable”—you must use the state setting function to modify state variables to queue a re-render. |
| You shouldn’t read (or write) thecurrentvalue during rendering. | You can read state at any time. However, each render has its ownsnapshotof state which does not change. |

Here is a counter button that’s implemented with state:

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
      You clicked {count} times
    </button>
  );
}
```

/$

Because the `count` value is displayed, it makes sense to use a state value for it. When the counter’s value is set with `setCount()`, React re-renders the component and the screen updates to reflect the new count.

If you tried to implement this with a ref, React would never re-render the component, so you’d never see the count change! See how clicking this button **does not update its text**:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef } from 'react';

export default function Counter() {
  let countRef = useRef(0);

  function handleClick() {
    // This doesn't re-render the component!
    countRef.current = countRef.current + 1;
  }

  return (
    <button onClick={handleClick}>
      You clicked {countRef.current} times
    </button>
  );
}
```

/$

This is why reading `ref.current` during render leads to unreliable code. If you need that, use state instead.

##### Deep Dive

#### How does useRef work inside?

Although both `useState` and `useRef` are provided by React, in principle `useRef` could be implemented *on top of* `useState`. You can imagine that inside of React, `useRef` is implemented like this:

$

```
// Inside of Reactfunction useRef(initialValue) {  const [ref, unused] = useState({ current: initialValue });  return ref;}
```

/$

During the first render, `useRef` returns `{ current: initialValue }`. This object is stored by React, so during the next render the same object will be returned. Note how the state setter is unused in this example. It is unnecessary because `useRef` always needs to return the same object!

React provides a built-in version of `useRef` because it is common enough in practice. But you can think of it as a regular state variable without a setter. If you’re familiar with object-oriented programming, refs might remind you of instance fields—but instead of `this.something` you write `somethingRef.current`.

## When to use refs

Typically, you will use a ref when your component needs to “step outside” React and communicate with external APIs—often a browser API that won’t impact the appearance of the component. Here are a few of these rare situations:

- Storing [timeout IDs](https://developer.mozilla.org/docs/Web/API/setTimeout)
- Storing and manipulating [DOM elements](https://developer.mozilla.org/docs/Web/API/Element), which we cover on [the next page](https://react.dev/learn/manipulating-the-dom-with-refs)
- Storing other objects that aren’t necessary to calculate the JSX.

If your component needs to store some value, but it doesn’t impact the rendering logic, choose refs.

## Best practices for refs

Following these principles will make your components more predictable:

- **Treat refs as an escape hatch.** Refs are useful when you work with external systems or browser APIs. If much of your application logic and data flow relies on refs, you might want to rethink your approach.
- **Don’t read or writeref.currentduring rendering.** If some information is needed during rendering, use [state](https://react.dev/learn/state-a-components-memory) instead. Since React doesn’t know when `ref.current` changes, even reading it while rendering makes your component’s behavior difficult to predict. (The only exception to this is code like `if (!ref.current) ref.current = new Thing()` which only sets the ref once during the first render.)

Limitations of React state don’t apply to refs. For example, state acts like a [snapshot for every render](https://react.dev/learn/state-as-a-snapshot) and [doesn’t update synchronously.](https://react.dev/learn/queueing-a-series-of-state-updates) But when you mutate the current value of a ref, it changes immediately:

 $

```
ref.current = 5;console.log(ref.current); // 5
```

/$

This is because **the ref itself is a regular JavaScript object,** and so it behaves like one.

You also don’t need to worry about [avoiding mutation](https://react.dev/learn/updating-objects-in-state) when you work with a ref. As long as the object you’re mutating isn’t used for rendering, React doesn’t care what you do with the ref or its contents.

## Refs and the DOM

You can point a ref to any value. However, the most common use case for a ref is to access a DOM element. For example, this is handy if you want to focus an input programmatically. When you pass a ref to a `ref` attribute in JSX, like `<div ref={myRef}>`, React will put the corresponding DOM element into `myRef.current`. Once the element is removed from the DOM, React will update `myRef.current` to be `null`. You can read more about this in [Manipulating the DOM with Refs.](https://react.dev/learn/manipulating-the-dom-with-refs)

## Recap

- Refs are an escape hatch to hold onto values that aren’t used for rendering. You won’t need them often.
- A ref is a plain JavaScript object with a single property called `current`, which you can read or set.
- You can ask React to give you a ref by calling the `useRef` Hook.
- Like state, refs let you retain information between re-renders of a component.
- Unlike state, setting the ref’s `current` value does not trigger a re-render.
- Don’t read or write `ref.current` during rendering. This makes your component hard to predict.

## Try out some challenges

#### Challenge1of4:Fix a broken chat input

Type a message and click “Send”. You will notice there is a three second delay before you see the “Sent!” alert. During this delay, you can see an “Undo” button. Click it. This “Undo” button is supposed to stop the “Sent!” message from appearing. It does this by calling [clearTimeout](https://developer.mozilla.org/en-US/docs/Web/API/clearTimeout) for the timeout ID saved during `handleSend`. However, even after “Undo” is clicked, the “Sent!” message still appears. Find why it doesn’t work, and fix it.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Chat() {
  const [text, setText] = useState('');
  const [isSending, setIsSending] = useState(false);
  let timeoutID = null;

  function handleSend() {
    setIsSending(true);
    timeoutID = setTimeout(() => {
      alert('Sent!');
      setIsSending(false);
    }, 3000);
  }

  function handleUndo() {
    setIsSending(false);
    clearTimeout(timeoutID);
  }

  return (
    <>
      <input
        disabled={isSending}
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <button
        disabled={isSending}
        onClick={handleSend}>
        {isSending ? 'Sending...' : 'Send'}
      </button>
      {isSending &&
        <button onClick={handleUndo}>
          Undo
        </button>
      }
    </>
  );
}
```

/$[PreviousEscape Hatches](https://react.dev/learn/escape-hatches)[NextManipulating the DOM with Refs](https://react.dev/learn/manipulating-the-dom-with-refs)
