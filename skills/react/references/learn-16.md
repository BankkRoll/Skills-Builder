# Sharing State Between Components and more

# Sharing State Between Components

[Learn React](https://react.dev/learn)[Managing State](https://react.dev/learn/managing-state)

# Sharing State Between Components

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as *lifting state up,* and it’s one of the most common things you will do writing React code.

### You will learn

- How to share state between components by lifting it up
- What are controlled and uncontrolled components

## Lifting state up by example

In this example, a parent `Accordion` component renders two separate `Panel`s:

- `Accordion`
  - `Panel`
  - `Panel`

Each `Panel` component has a boolean `isActive` state that determines whether its content is visible.

Press the Show button for both panels:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { useState } from 'react';
function Panel({ title, children }) { const [isActive, setIsActive] = useState(false); return ( <section className="panel"> <h3>{title}</h3> {isActive ? ( <p>{children}</p> ) : ( <button onClick={() => setIsActive(true)}>          Show </button> )} </section> );}
export default function Accordion() { return ( <> <h2>Almaty, Kazakhstan</h2> <Panel title="About">        With a population of about 2 million, Almaty is Kazakhstan's largest city. From 1929 to 1997, it was its capital city. </Panel> <Panel title="Etymology">        The name comes from <span lang="kk-KZ">алма</span>, the Kazakh word for "apple" and is often translated as "full of apples". In fact, the region surrounding Almaty is thought to be the ancestral home of the apple, and the wild <i lang="la">Malus sieversii</i> is considered a likely candidate for the ancestor of the modern domestic apple. </Panel> </> );}
/$

Notice how pressing one panel’s button does not affect the other panel—they are independent.

 ![Diagram showing a tree of three components, one parent labeled Accordion and two children labeled Panel. Both Panel components contain isActive with value false.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_child.dark.png&w=1080&q=75)![Diagram showing a tree of three components, one parent labeled Accordion and two children labeled Panel. Both Panel components contain isActive with value false.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_child.png&w=1080&q=75)

Initially, each `Panel`’s `isActive` state is `false`, so they both appear collapsed

![The same diagram as the previous, with the isActive of the first child Panel component highlighted indicating a click with the isActive value set to true. The second Panel component still contains value false.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_child_clicked.dark.png&w=1080&q=75)![The same diagram as the previous, with the isActive of the first child Panel component highlighted indicating a click with the isActive value set to true. The second Panel component still contains value false.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_child_clicked.png&w=1080&q=75)

Clicking either `Panel`’s button will only update that `Panel`’s `isActive` state alone

**But now let’s say you want to change it so that only one panel is expanded at any given time.** With that design, expanding the second panel should collapse the first one. How would you do that?

To coordinate these two panels, you need to “lift their state up” to a parent component in three steps:

1. **Remove** state from the child components.
2. **Pass** hardcoded data from the common parent.
3. **Add** state to the common parent and pass it down together with the event handlers.

This will allow the `Accordion` component to coordinate both `Panel`s and only expand one at a time.

### Step 1: Remove state from the child components

You will give control of the `Panel`’s `isActive` to its parent component. This means that the parent component will pass `isActive` to `Panel` as a prop instead. Start by **removing this line** from the `Panel` component:

 $

```
const [isActive, setIsActive] = useState(false);
```

/$

And instead, add `isActive` to the `Panel`’s list of props:

 $

```
function Panel({ title, children, isActive }) {
```

/$

Now the `Panel`’s parent component can *control* `isActive` by [passing it down as a prop.](https://react.dev/learn/passing-props-to-a-component) Conversely, the `Panel` component now has *no control* over the value of `isActive`—it’s now up to the parent component!

### Step 2: Pass hardcoded data from the common parent

To lift state up, you must locate the closest common parent component of *both* of the child components that you want to coordinate:

- `Accordion` *(closest common parent)*
  - `Panel`
  - `Panel`

In this example, it’s the `Accordion` component. Since it’s above both panels and can control their props, it will become the “source of truth” for which panel is currently active. Make the `Accordion` component pass a hardcoded value of `isActive` (for example, `true`) to both panels:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Accordion() {
  return (
    <>
      <h2>Almaty, Kazakhstan</h2>
      <Panel title="About" isActive={true}>
        With a population of about 2 million, Almaty is Kazakhstan's largest city. From 1929 to 1997, it was its capital city.
      </Panel>
      <Panel title="Etymology" isActive={true}>
        The name comes from <span lang="kk-KZ">алма</span>, the Kazakh word for "apple" and is often translated as "full of apples". In fact, the region surrounding Almaty is thought to be the ancestral home of the apple, and the wild <i lang="la">Malus sieversii</i> is considered a likely candidate for the ancestor of the modern domestic apple.
      </Panel>
    </>
  );
}

function Panel({ title, children, isActive }) {
  return (
    <section className="panel">
      <h3>{title}</h3>
      {isActive ? (
        <p>{children}</p>
      ) : (
        <button onClick={() => setIsActive(true)}>
          Show
        </button>
      )}
    </section>
  );
}
```

/$

Try editing the hardcoded `isActive` values in the `Accordion` component and see the result on the screen.

### Step 3: Add state to the common parent

Lifting state up often changes the nature of what you’re storing as state.

In this case, only one panel should be active at a time. This means that the `Accordion` common parent component needs to keep track of *which* panel is the active one. Instead of a `boolean` value, it could use a number as the index of the active `Panel` for the state variable:

 $

```
const [activeIndex, setActiveIndex] = useState(0);
```

/$

When the `activeIndex` is `0`, the first panel is active, and when it’s `1`, it’s the second one.

Clicking the “Show” button in either `Panel` needs to change the active index in `Accordion`. A `Panel` can’t set the `activeIndex` state directly because it’s defined inside the `Accordion`. The `Accordion` component needs to *explicitly allow* the `Panel` component to change its state by [passing an event handler down as a prop](https://react.dev/learn/responding-to-events#passing-event-handlers-as-props):

 $

```
<>  <Panel    isActive={activeIndex === 0}    onShow={() => setActiveIndex(0)}  >    ...  </Panel>  <Panel    isActive={activeIndex === 1}    onShow={() => setActiveIndex(1)}  >    ...  </Panel></>
```

/$

The `<button>` inside the `Panel` will now use the `onShow` prop as its click event handler:

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

This completes lifting state up! Moving state into the common parent component allowed you to coordinate the two panels. Using the active index instead of two “is shown” flags ensured that only one panel is active at a given time. And passing down the event handler to the child allowed the child to change the parent’s state.

 ![Diagram showing a tree of three components, one parent labeled Accordion and two children labeled Panel. Accordion contains an activeIndex value of zero which turns into isActive value of true passed to the first Panel, and isActive value of false passed to the second Panel.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_parent.dark.png&w=1080&q=75)![Diagram showing a tree of three components, one parent labeled Accordion and two children labeled Panel. Accordion contains an activeIndex value of zero which turns into isActive value of true passed to the first Panel, and isActive value of false passed to the second Panel.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_parent.png&w=1080&q=75)

Initially, `Accordion`’s `activeIndex` is `0`, so the first `Panel` receives `isActive = true`

![The same diagram as the previous, with the activeIndex value of the parent Accordion component highlighted indicating a click with the value changed to one. The flow to both of the children Panel components is also highlighted, and the isActive value passed to each child is set to the opposite: false for the first Panel and true for the second one.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_parent_clicked.dark.png&w=1080&q=75)![The same diagram as the previous, with the activeIndex value of the parent Accordion component highlighted indicating a click with the value changed to one. The flow to both of the children Panel components is also highlighted, and the isActive value passed to each child is set to the opposite: false for the first Panel and true for the second one.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fsharing_state_parent_clicked.png&w=1080&q=75)

When `Accordion`’s `activeIndex` state changes to `1`, the second `Panel` receives `isActive = true` instead

##### Deep Dive

#### Controlled and uncontrolled components

It is common to call a component with some local state “uncontrolled”. For example, the original `Panel` component with an `isActive` state variable is uncontrolled because its parent cannot influence whether the panel is active or not.

In contrast, you might say a component is “controlled” when the important information in it is driven by props rather than its own local state. This lets the parent component fully specify its behavior. The final `Panel` component with the `isActive` prop is controlled by the `Accordion` component.

Uncontrolled components are easier to use within their parents because they require less configuration. But they’re less flexible when you want to coordinate them together. Controlled components are maximally flexible, but they require the parent components to fully configure them with props.

In practice, “controlled” and “uncontrolled” aren’t strict technical terms—each component usually has some mix of both local state and props. However, this is a useful way to talk about how components are designed and what capabilities they offer.

When writing a component, consider which information in it should be controlled (via props), and which information should be uncontrolled (via state). But you can always change your mind and refactor later.

## A single source of truth for each state

In a React application, many components will have their own state. Some state may “live” close to the leaf components (components at the bottom of the tree) like inputs. Other state may “live” closer to the top of the app. For example, even client-side routing libraries are usually implemented by storing the current route in the React state, and passing it down by props!

**For each unique piece of state, you will choose the component that “owns” it.** This principle is also known as having a [“single source of truth”.](https://en.wikipedia.org/wiki/Single_source_of_truth) It doesn’t mean that all state lives in one place—but that for *each* piece of state, there is a *specific* component that holds that piece of information. Instead of duplicating shared state between components, *lift it up* to their common shared parent, and *pass it down* to the children that need it.

Your app will change as you work on it. It is common that you will move state down or back up while you’re still figuring out where each piece of the state “lives”. This is all part of the process!

To see what this feels like in practice with a few more components, read [Thinking in React.](https://react.dev/learn/thinking-in-react)

## Recap

- When you want to coordinate two components, move their state to their common parent.
- Then pass the information down through props from their common parent.
- Finally, pass the event handlers down so that the children can change the parent’s state.
- It’s useful to consider components as “controlled” (driven by props) or “uncontrolled” (driven by state).

## Try out some challenges

#### Challenge1of2:Synced inputs

These two inputs are independent. Make them stay in sync: editing one input should update the other input with the same text, and vice versa.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function SyncedInputs() {
  return (
    <>
      <Input label="First input" />
      <Input label="Second input" />
    </>
  );
}

function Input({ label }) {
  const [text, setText] = useState('');

  function handleChange(e) {
    setText(e.target.value);
  }

  return (
    <label>
      {label}
      {' '}
      <input
        value={text}
        onChange={handleChange}
      />
    </label>
  );
}
```

/$[PreviousChoosing the State Structure](https://react.dev/learn/choosing-the-state-structure)[NextPreserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)

---

# State: A Component's Memory

[Learn React](https://react.dev/learn)[Adding Interactivity](https://react.dev/learn/adding-interactivity)

# State: A Component's Memory

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” should put a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called *state*.

### You will learn

- How to add a state variable with the [useState](https://react.dev/reference/react/useState) Hook
- What pair of values the `useState` Hook returns
- How to add more than one state variable
- Why state is called local

## When a regular variable isn’t enough

Here’s a component that renders a sculpture image. Clicking the “Next” button should show the next sculpture by changing the `index` to `1`, then `2`, and so on. However, this **won’t work** (you can try it!):

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { sculptureList } from './data.js';
export default function Gallery() { let index = 0;
 function handleClick() { index = index + 1; }
 let sculpture = sculptureList[index]; return ( <> <button onClick={handleClick}>        Next </button> <h2> <i>{sculpture.name} </i>         by {sculpture.artist} </h2> <h3>         ({index + 1} of {sculptureList.length}) </h3> <img  src={sculpture.url}  alt={sculpture.alt} /> <p> {sculpture.description} </p> </> );}
/$

The `handleClick` event handler is updating a local variable, `index`. But two things prevent that change from being visible:

1. **Local variables don’t persist between renders.** When React renders this component a second time, it renders it from scratch—it doesn’t consider any changes to the local variables.
2. **Changes to local variables won’t trigger renders.** React doesn’t realize it needs to render the component again with the new data.

To update a component with new data, two things need to happen:

1. **Retain** the data between renders.
2. **Trigger** React to render the component with new data (re-rendering).

The [useState](https://react.dev/reference/react/useState) Hook provides those two things:

1. A **state variable** to retain the data between renders.
2. A **state setter function** to update the variable and trigger React to render the component again.

## Adding a state variable

To add a state variable, import `useState` from React at the top of the file:

 $

```
import { useState } from 'react';
```

/$

Then, replace this line:

 $

```
let index = 0;
```

/$

with

 $

```
const [index, setIndex] = useState(0);
```

/$

`index` is a state variable and `setIndex` is the setter function.

> The `[` and `]` syntax here is called [array destructuring](https://javascript.info/destructuring-assignment) and it lets you read values from an array. The array returned by `useState` always has exactly two items.

This is how they work together in `handleClick`:

 $

```
function handleClick() {  setIndex(index + 1);}
```

/$

Now clicking the “Next” button switches the current sculpture:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { sculptureList } from './data.js';

export default function Gallery() {
  const [index, setIndex] = useState(0);

  function handleClick() {
    setIndex(index + 1);
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleClick}>
        Next
      </button>
      <h2>
        <i>{sculpture.name} </i>
        by {sculpture.artist}
      </h2>
      <h3>
        ({index + 1} of {sculptureList.length})
      </h3>
      <img
        src={sculpture.url}
        alt={sculpture.alt}
      />
      <p>
        {sculpture.description}
      </p>
    </>
  );
}
```

/$

### Meet your first Hook

In React, `useState`, as well as any other function starting with “`use`”, is called a Hook.

*Hooks* are special functions that are only available while React is [rendering](https://react.dev/learn/render-and-commit#step-1-trigger-a-render) (which we’ll get into in more detail on the next page). They let you “hook into” different React features.

State is just one of those features, but you will meet the other Hooks later.

### Pitfall

**Hooks—functions starting withuse—can only be called at the top level of your components oryour own Hooks.** You can’t call Hooks inside conditions, loops, or other nested functions. Hooks are functions, but it’s helpful to think of them as unconditional declarations about your component’s needs. You “use” React features at the top of your component similar to how you “import” modules at the top of your file.

### Anatomy ofuseState

When you call [useState](https://react.dev/reference/react/useState), you are telling React that you want this component to remember something:

 $

```
const [index, setIndex] = useState(0);
```

/$

In this case, you want React to remember `index`.

### Note

The convention is to name this pair like `const [something, setSomething]`. You could name it anything you like, but conventions make things easier to understand across projects.

The only argument to `useState` is the **initial value** of your state variable. In this example, the `index`’s initial value is set to `0` with `useState(0)`.

Every time your component renders, `useState` gives you an array containing two values:

1. The **state variable** (`index`) with the value you stored.
2. The **state setter function** (`setIndex`) which can update the state variable and trigger React to render the component again.

Here’s how that happens in action:

 $

```
const [index, setIndex] = useState(0);
```

/$

1. **Your component renders the first time.** Because you passed `0` to `useState` as the initial value for `index`, it will return `[0, setIndex]`. React remembers `0` is the latest state value.
2. **You update the state.** When a user clicks the button, it calls `setIndex(index + 1)`. `index` is `0`, so it’s `setIndex(1)`. This tells React to remember `index` is `1` now and triggers another render.
3. **Your component’s second render.** React still sees `useState(0)`, but because React *remembers* that you set `index` to `1`, it returns `[1, setIndex]` instead.
4. And so on!

## Giving a component multiple state variables

You can have as many state variables of as many types as you like in one component. This component has two state variables, a number `index` and a boolean `showMore` that’s toggled when you click “Show details”:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { sculptureList } from './data.js';

export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);

  function handleNextClick() {
    setIndex(index + 1);
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleNextClick}>
        Next
      </button>
      <h2>
        <i>{sculpture.name} </i>
        by {sculpture.artist}
      </h2>
      <h3>
        ({index + 1} of {sculptureList.length})
      </h3>
      <button onClick={handleMoreClick}>
        {showMore ? 'Hide' : 'Show'} details
      </button>
      {showMore && <p>{sculpture.description}</p>}
      <img
        src={sculpture.url}
        alt={sculpture.alt}
      />
    </>
  );
}
```

/$

It is a good idea to have multiple state variables if their state is unrelated, like `index` and `showMore` in this example. But if you find that you often change two state variables together, it might be easier to combine them into one. For example, if you have a form with many fields, it’s more convenient to have a single state variable that holds an object than state variable per field. Read [Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure) for more tips.

##### Deep Dive

#### How does React know which state to return?

You might have noticed that the `useState` call does not receive any information about *which* state variable it refers to. There is no “identifier” that is passed to `useState`, so how does it know which of the state variables to return? Does it rely on some magic like parsing your functions? The answer is no.

Instead, to enable their concise syntax, Hooks **rely on a stable call order on every render of the same component.** This works well in practice because if you follow the rule above (“only call Hooks at the top level”), Hooks will always be called in the same order. Additionally, a [linter plugin](https://www.npmjs.com/package/eslint-plugin-react-hooks) catches most mistakes.

Internally, React holds an array of state pairs for every component. It also maintains the current pair index, which is set to `0` before rendering. Each time you call `useState`, React gives you the next state pair and increments the index. You can read more about this mechanism in [React Hooks: Not Magic, Just Arrays.](https://medium.com/@ryardley/react-hooks-not-magic-just-arrays-cd4f1857236e)

This example **doesn’t use React** but it gives you an idea of how `useState` works internally:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
let componentHooks = [];
let currentHookIndex = 0;

// How useState works inside React (simplified).
function useState(initialState) {
  let pair = componentHooks[currentHookIndex];
  if (pair) {
    // This is not the first render,
    // so the state pair already exists.
    // Return it and prepare for next Hook call.
    currentHookIndex++;
    return pair;
  }

  // This is the first time we're rendering,
  // so create a state pair and store it.
  pair = [initialState, setState];

  function setState(nextState) {
    // When the user requests a state change,
    // put the new value into the pair.
    pair[0] = nextState;
    updateDOM();
  }

  // Store the pair for future renders
  // and prepare for the next Hook call.
  componentHooks[currentHookIndex] = pair;
  currentHookIndex++;
  return pair;
}

function Gallery() {
  // Each useState() call will get the next pair.
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);

  function handleNextClick() {
    setIndex(index + 1);
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  let sculpture = sculptureList[index];
  // This example doesn't use React, so
  // return an output object instead of JSX.
  return {
    onNextClick: handleNextClick,
    onMoreClick: handleMoreClick,
    header: `${sculpture.name} by ${sculpture.artist}`,
    counter: `${index + 1} of ${sculptureList.length}`,
    more: `${showMore ? 'Hide' : 'Show'} details`,
    description: showMore ? sculpture.description : null,
    imageSrc: sculpture.url,
    imageAlt: sculpture.alt
  };
}

function updateDOM() {
  // Reset the current Hook index
  // before rendering the component.
  currentHookIndex = 0;
  let output = Gallery();

  // Update the DOM to match the output.
  // This is the part React does for you.
  nextButton.onclick = output.onNextClick;
  header.textContent = output.header;
  moreButton.onclick = output.onMoreClick;
  moreButton.textContent = output.more;
  image.src = output.imageSrc;
  image.alt = output.imageAlt;
  if (output.description !== null) {
    description.textContent = output.description;
    description.style.display = '';
  } else {
    description.style.display = 'none';
  }
}

let nextButton = document.getElementById('nextButton');
let header = document.getElementById('header');
let moreButton = document.getElementById('moreButton');
let description = document.getElementById('description');
let image = document.getElementById('image');
let sculptureList = [{
  name: 'Homenaje a la Neurocirugía',
  artist: 'Marta Colvin Andrade',
  description: 'Although Colvin is predominantly known for abstract themes that allude to pre-Hispanic symbols, this gigantic sculpture, an homage to neurosurgery, is one of her most recognizable public art pieces.',
  url: 'https://i.imgur.com/Mx7dA2Y.jpg',
  alt: 'A bronze statue of two crossed hands delicately holding a human brain in their fingertips.'
}, {
  name: 'Floralis Genérica',
  artist: 'Eduardo Catalano',
  description: 'This enormous (75 ft. or 23m) silver flower is located in Buenos Aires. It is designed to move, closing its petals in the evening or when strong winds blow and opening them in the morning.',
  url: 'https://i.imgur.com/ZF6s192m.jpg',
  alt: 'A gigantic metallic flower sculpture with reflective mirror-like petals and strong stamens.'
}, {
  name: 'Eternal Presence',
  artist: 'John Woodrow Wilson',
  description: 'Wilson was known for his preoccupation with equality, social justice, as well as the essential and spiritual qualities of humankind. This massive (7ft. or 2,13m) bronze represents what he described as "a symbolic Black presence infused with a sense of universal humanity."',
  url: 'https://i.imgur.com/aTtVpES.jpg',
  alt: 'The sculpture depicting a human head seems ever-present and solemn. It radiates calm and serenity.'
}, {
  name: 'Moai',
  artist: 'Unknown Artist',
  description: 'Located on the Easter Island, there are 1,000 moai, or extant monumental statues, created by the early Rapa Nui people, which some believe represented deified ancestors.',
  url: 'https://i.imgur.com/RCwLEoQm.jpg',
  alt: 'Three monumental stone busts with the heads that are disproportionately large with somber faces.'
}, {
  name: 'Blue Nana',
  artist: 'Niki de Saint Phalle',
  description: 'The Nanas are triumphant creatures, symbols of femininity and maternity. Initially, Saint Phalle used fabric and found objects for the Nanas, and later on introduced polyester to achieve a more vibrant effect.',
  url: 'https://i.imgur.com/Sd1AgUOm.jpg',
  alt: 'A large mosaic sculpture of a whimsical dancing female figure in a colorful costume emanating joy.'
}, {
  name: 'Ultimate Form',
  artist: 'Barbara Hepworth',
  description: 'This abstract bronze sculpture is a part of The Family of Man series located at Yorkshire Sculpture Park. Hepworth chose not to create literal representations of the world but developed abstract forms inspired by people and landscapes.',
  url: 'https://i.imgur.com/2heNQDcm.jpg',
  alt: 'A tall sculpture made of three elements stacked on each other reminding of a human figure.'
}, {
  name: 'Cavaliere',
  artist: 'Lamidi Olonade Fakeye',
  description: "Descended from four generations of woodcarvers, Fakeye's work blended traditional and contemporary Yoruba themes.",
  url: 'https://i.imgur.com/wIdGuZwm.png',
  alt: 'An intricate wood sculpture of a warrior with a focused face on a horse adorned with patterns.'
}, {
  name: 'Big Bellies',
  artist: 'Alina Szapocznikow',
  description: "Szapocznikow is known for her sculptures of the fragmented body as a metaphor for the fragility and impermanence of youth and beauty. This sculpture depicts two very realistic large bellies stacked on top of each other, each around five feet (1,5m) tall.",
  url: 'https://i.imgur.com/AlHTAdDm.jpg',
  alt: 'The sculpture reminds a cascade of folds, quite different from bellies in classical sculptures.'
}, {
  name: 'Terracotta Army',
  artist: 'Unknown Artist',
  description: 'The Terracotta Army is a collection of terracotta sculptures depicting the armies of Qin Shi Huang, the first Emperor of China. The army consisted of more than 8,000 soldiers, 130 chariots with 520 horses, and 150 cavalry horses.',
  url: 'https://i.imgur.com/HMFmH6m.jpg',
  alt: '12 terracotta sculptures of solemn warriors, each with a unique facial expression and armor.'
}, {
  name: 'Lunar Landscape',
  artist: 'Louise Nevelson',
  description: 'Nevelson was known for scavenging objects from New York City debris, which she would later assemble into monumental constructions. In this one, she used disparate parts like a bedpost, juggling pin, and seat fragment, nailing and gluing them into boxes that reflect the influence of Cubism’s geometric abstraction of space and form.',
  url: 'https://i.imgur.com/rN7hY6om.jpg',
  alt: 'A black matte sculpture where the individual elements are initially indistinguishable.'
}, {
  name: 'Aureole',
  artist: 'Ranjani Shettar',
  description: 'Shettar merges the traditional and the modern, the natural and the industrial. Her art focuses on the relationship between man and nature. Her work was described as compelling both abstractly and figuratively, gravity defying, and a "fine synthesis of unlikely materials."',
  url: 'https://i.imgur.com/okTpbHhm.jpg',
  alt: 'A pale wire-like sculpture mounted on concrete wall and descending on the floor. It appears light.'
}, {
  name: 'Hippos',
  artist: 'Taipei Zoo',
  description: 'The Taipei Zoo commissioned a Hippo Square featuring submerged hippos at play.',
  url: 'https://i.imgur.com/6o5Vuyu.jpg',
  alt: 'A group of bronze hippo sculptures emerging from the sett sidewalk as if they were swimming.'
}];

// Make UI match the initial state.
updateDOM();
```

/$

You don’t have to understand it to use React, but you might find this a helpful mental model.

## State is isolated and private

State is local to a component instance on the screen. In other words, **if you render the same component twice, each copy will have completely isolated state!** Changing one of them will not affect the other.

In this example, the `Gallery` component from earlier is rendered twice with no changes to its logic. Try clicking the buttons inside each of the galleries. Notice that their state is independent:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Gallery from './Gallery.js';

export default function Page() {
  return (
    <div className="Page">
      <Gallery />
      <Gallery />
    </div>
  );
}
```

/$

This is what makes state different from regular variables that you might declare at the top of your module. State is not tied to a particular function call or a place in the code, but it’s “local” to the specific place on the screen. You rendered two `<Gallery />` components, so their state is stored separately.

Also notice how the `Page` component doesn’t “know” anything about the `Gallery` state or even whether it has any. Unlike props, **state is fully private to the component declaring it.** The parent component can’t change it. This lets you add state to any component or remove it without impacting the rest of the components.

What if you wanted both galleries to keep their states in sync? The right way to do it in React is to *remove* state from child components and add it to their closest shared parent. The next few pages will focus on organizing state of a single component, but we will return to this topic in [Sharing State Between Components.](https://react.dev/learn/sharing-state-between-components)

## Recap

- Use a state variable when a component needs to “remember” some information between renders.
- State variables are declared by calling the `useState` Hook.
- Hooks are special functions that start with `use`. They let you “hook into” React features like state.
- Hooks might remind you of imports: they need to be called unconditionally. Calling Hooks, including `useState`, is only valid at the top level of a component or another Hook.
- The `useState` Hook returns a pair of values: the current state and the function to update it.
- You can have more than one state variable. Internally, React matches them up by their order.
- State is private to the component. If you render it in two places, each copy gets its own state.

## Try out some challenges

#### Challenge1of4:Complete the gallery

When you press “Next” on the last sculpture, the code crashes. Fix the logic to prevent the crash. You may do this by adding extra logic to event handler or by disabling the button when the action is not possible.

After fixing the crash, add a “Previous” button that shows the previous sculpture. It shouldn’t crash on the first sculpture.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { sculptureList } from './data.js';

export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);

  function handleNextClick() {
    setIndex(index + 1);
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleNextClick}>
        Next
      </button>
      <h2>
        <i>{sculpture.name} </i>
        by {sculpture.artist}
      </h2>
      <h3>
        ({index + 1} of {sculptureList.length})
      </h3>
      <button onClick={handleMoreClick}>
        {showMore ? 'Hide' : 'Show'} details
      </button>
      {showMore && <p>{sculpture.description}</p>}
      <img
        src={sculpture.url}
        alt={sculpture.alt}
      />
    </>
  );
}
```

/$[PreviousResponding to Events](https://react.dev/learn/responding-to-events)[NextRender and Commit](https://react.dev/learn/render-and-commit)
