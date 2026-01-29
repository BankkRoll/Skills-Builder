# Render and Commit and more

# Render and Commit

[Learn React](https://react.dev/learn)[Adding Interactivity](https://react.dev/learn/adding-interactivity)

# Render and Commit

Before your components are displayed on screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

### You will learn

- What rendering means in React
- When and why React renders a component
- The steps involved in displaying a component on screen
- Why rendering does not always produce a DOM update

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

1. **Triggering** a render (delivering the guest’s order to the kitchen)
2. **Rendering** the component (preparing the order in the kitchen)
3. **Committing** to the DOM (placing the order on the table)

1. ![React as a server in a restaurant, fetching orders from the users and delivering them to the Component Kitchen.](https://react.dev/images/docs/illustrations/i_render-and-commit1.png)Trigger
2. ![The Card Chef gives React a fresh Card component.](https://react.dev/images/docs/illustrations/i_render-and-commit2.png)Render
3. ![React delivers the Card to the user at their table.](https://react.dev/images/docs/illustrations/i_render-and-commit3.png)Commit

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Step 1: Trigger a render

There are two reasons for a component to render:

1. It’s the component’s **initial render.**
2. The component’s (or one of its ancestors’) **state has been updated.**

### Initial render

When your app starts, you need to trigger the initial render. Frameworks and sandboxes sometimes hide this code, but it’s done by calling [createRoot](https://react.dev/reference/react-dom/client/createRoot) with the target DOM node, and then calling its `render` method with your component:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Image from './Image.js';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'))
root.render(<Image />);
```

/$

Try commenting out the `root.render()` call and see the component disappear!

### Re-renders when state updates

Once the component has been initially rendered, you can trigger further renders by updating its state with the [setfunction.](https://react.dev/reference/react/useState#setstate) Updating your component’s state automatically queues a render. (You can imagine these as a restaurant guest ordering tea, dessert, and all sorts of things after putting in their first order, depending on the state of their thirst or hunger.)

1. ![React as a server in a restaurant, serving a Card UI to the user, represented as a patron with a cursor for their head. The patron expresses they want a pink card, not a black one!](https://react.dev/images/docs/illustrations/i_rerender1.png)State update...
2. ![React returns to the Component Kitchen and tells the Card Chef they need a pink Card.](https://react.dev/images/docs/illustrations/i_rerender2.png)...triggers...
3. ![The Card Chef gives React the pink Card.](https://react.dev/images/docs/illustrations/i_rerender3.png)...render!

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Step 2: React renders your components

After you trigger a render, React calls your components to figure out what to display on screen. **“Rendering” is React calling your components.**

- **On initial render,** React will call the root component.
- **For subsequent renders,** React will call the function component whose state update triggered the render.

This process is recursive: if the updated component returns some other component, React will render *that* component next, and if that component also returns something, it will render *that* component next, and so on. The process will continue until there are no more nested components and React knows exactly what should be displayed on screen.

In the following example, React will call `Gallery()` and `Image()` several times:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Gallery() {
  return (
    <section>
      <h1>Inspiring Sculptures</h1>
      <Image />
      <Image />
      <Image />
    </section>
  );
}

function Image() {
  return (
    <img
      src="https://i.imgur.com/ZF6s192.jpg"
      alt="'Floralis Genérica' by Eduardo Catalano: a gigantic metallic flower sculpture with reflective petals"
    />
  );
}
```

/$

- **During the initial render,** React will [create the DOM nodes](https://developer.mozilla.org/docs/Web/API/Document/createElement) for `<section>`, `<h1>`, and three `<img>` tags.
- **During a re-render,** React will calculate which of their properties, if any, have changed since the previous render. It won’t do anything with that information until the next step, the commit phase.

### Pitfall

Rendering must always be a [pure calculation](https://react.dev/learn/keeping-components-pure):

- **Same inputs, same output.** Given the same inputs, a component should always return the same JSX. (When someone orders a salad with tomatoes, they should not receive a salad with onions!)
- **It minds its own business.** It should not change any objects or variables that existed before rendering. (One order should not change anyone else’s order.)

Otherwise, you can encounter confusing bugs and unpredictable behavior as your codebase grows in complexity. When developing in “Strict Mode”, React calls each component’s function twice, which can help surface mistakes caused by impure functions.

##### Deep Dive

#### Optimizing performance

The default behavior of rendering all components nested within the updated component is not optimal for performance if the updated component is very high in the tree. If you run into a performance issue, there are several opt-in ways to solve it described in the [Performance](https://reactjs.org/docs/optimizing-performance.html) section. **Don’t optimize prematurely!**

## Step 3: React commits changes to the DOM

After rendering (calling) your components, React will modify the DOM.

- **For the initial render,** React will use the [appendChild()](https://developer.mozilla.org/docs/Web/API/Node/appendChild) DOM API to put all the DOM nodes it has created on screen.
- **For re-renders,** React will apply the minimal necessary operations (calculated while rendering!) to make the DOM match the latest rendering output.

**React only changes the DOM nodes if there’s a difference between renders.** For example, here is a component that re-renders with different props passed from its parent every second. Notice how you can add some text into the `<input>`, updating its `value`, but the text doesn’t disappear when the component re-renders:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Clock({ time }) {
  return (
    <>
      <h1>{time}</h1>
      <input />
    </>
  );
}
```

/$

This works because during this last step, React only updates the content of `<h1>` with the new `time`. It sees that the `<input>` appears in the JSX in the same place as last time, so React doesn’t touch the `<input>`—or its `value`!

## Epilogue: Browser paint

After rendering is done and React updated the DOM, the browser will repaint the screen. Although this process is known as “browser rendering”, we’ll refer to it as “painting” to avoid confusion throughout the docs.

 ![A browser painting 'still life with card element'.](https://react.dev/images/docs/illustrations/i_browser-paint.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Recap

- Any screen update in a React app happens in three steps:
  1. Trigger
  2. Render
  3. Commit
- You can use Strict Mode to find mistakes in your components
- React does not touch the DOM if the rendering result is the same as last time

[PreviousState: A Component's Memory](https://react.dev/learn/state-a-components-memory)[NextState as a Snapshot](https://react.dev/learn/state-as-a-snapshot)

---

# Rendering Lists

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Rendering Lists

You will often want to display multiple similar components from a collection of data. You can use the [JavaScript array methods](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array#) to manipulate an array of data. On this page, you’ll use [filter()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) and [map()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/map) with React to filter and transform your array of data into an array of components.

### You will learn

- How to render components from an array using JavaScript’s `map()`
- How to render only specific components using JavaScript’s `filter()`
- When and why to use React keys

## Rendering data from arrays

Say that you have a list of content.

 $

```
<ul>  <li>Creola Katherine Johnson: mathematician</li>  <li>Mario José Molina-Pasquel Henríquez: chemist</li>  <li>Mohammad Abdus Salam: physicist</li>  <li>Percy Lavon Julian: chemist</li>  <li>Subrahmanyan Chandrasekhar: astrophysicist</li></ul>
```

/$

The only difference among those list items is their contents, their data. You will often need to show several instances of the same component using different data when building interfaces: from lists of comments to galleries of profile images. In these situations, you can store that data in JavaScript objects and arrays and use methods like [map()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) and [filter()](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) to render lists of components from them.

Here’s a short example of how to generate a list of items from an array:

1. **Move** the data into an array:

 $

```
const people = [  'Creola Katherine Johnson: mathematician',  'Mario José Molina-Pasquel Henríquez: chemist',  'Mohammad Abdus Salam: physicist',  'Percy Lavon Julian: chemist',  'Subrahmanyan Chandrasekhar: astrophysicist'];
```

/$

1. **Map** the `people` members into a new array of JSX nodes, `listItems`:

 $

```
const listItems = people.map(person => <li>{person}</li>);
```

/$

1. **Return** `listItems` from your component wrapped in a `<ul>`:

 $

```
return <ul>{listItems}</ul>;
```

/$

Here is the result:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
const people = [
  'Creola Katherine Johnson: mathematician',
  'Mario José Molina-Pasquel Henríquez: chemist',
  'Mohammad Abdus Salam: physicist',
  'Percy Lavon Julian: chemist',
  'Subrahmanyan Chandrasekhar: astrophysicist'
];

export default function List() {
  const listItems = people.map(person =>
    <li>{person}</li>
  );
  return <ul>{listItems}</ul>;
}
```

/$

Notice the sandbox above displays a console error:

 ConsoleWarning: Each child in a list should have a unique “key” prop.

You’ll learn how to fix this error later on this page. Before we get to that, let’s add some structure to your data.

## Filtering arrays of items

This data can be structured even more.

 $

```
const people = [{  id: 0,  name: 'Creola Katherine Johnson',  profession: 'mathematician',}, {  id: 1,  name: 'Mario José Molina-Pasquel Henríquez',  profession: 'chemist',}, {  id: 2,  name: 'Mohammad Abdus Salam',  profession: 'physicist',}, {  id: 3,  name: 'Percy Lavon Julian',  profession: 'chemist',  }, {  id: 4,  name: 'Subrahmanyan Chandrasekhar',  profession: 'astrophysicist',}];
```

/$

Let’s say you want a way to only show people whose profession is `'chemist'`. You can use JavaScript’s `filter()` method to return just those people. This method takes an array of items, passes them through a “test” (a function that returns `true` or `false`), and returns a new array of only those items that passed the test (returned `true`).

You only want the items where `profession` is `'chemist'`. The “test” function for this looks like `(person) => person.profession === 'chemist'`. Here’s how to put it together:

1. **Create** a new array of just “chemist” people, `chemists`, by calling `filter()` on the `people` filtering by `person.profession === 'chemist'`:

 $

```
const chemists = people.filter(person =>  person.profession === 'chemist');
```

/$

1. Now **map** over `chemists`:

 $

```
const listItems = chemists.map(person =>  <li>     <img       src={getImageUrl(person)}       alt={person.name}     />     <p>       <b>{person.name}:</b>       {' ' + person.profession + ' '}       known for {person.accomplishment}     </p>  </li>);
```

/$

1. Lastly, **return** the `listItems` from your component:

 $

```
return <ul>{listItems}</ul>;
```

/$ $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { people } from './data.js';
import { getImageUrl } from './utils.js';

export default function List() {
  const chemists = people.filter(person =>
    person.profession === 'chemist'
  );
  const listItems = chemists.map(person =>
    <li>
      <img
        src={getImageUrl(person)}
        alt={person.name}
      />
      <p>
        <b>{person.name}:</b>
        {' ' + person.profession + ' '}
        known for {person.accomplishment}
      </p>
    </li>
  );
  return <ul>{listItems}</ul>;
}
```

/$

### Pitfall

Arrow functions implicitly return the expression right after `=>`, so you didn’t need a `return` statement:

$

```
const listItems = chemists.map(person =>  <li>...</li> // Implicit return!);
```

/$

However, **you must writereturnexplicitly if your=>is followed by a{curly brace!**

$

```
const listItems = chemists.map(person => { // Curly brace  return <li>...</li>;});
```

/$

Arrow functions containing `=> {` are said to have a [“block body”.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions#function_body) They let you write more than a single line of code, but you *have to* write a `return` statement yourself. If you forget it, nothing gets returned!

## Keeping list items in order withkey

Notice that all the sandboxes above show an error in the console:

 ConsoleWarning: Each child in a list should have a unique “key” prop.

You need to give each array item a `key` — a string or a number that uniquely identifies it among other items in that array:

 $

```
<li key={person.id}>...</li>
```

/$

### Note

JSX elements directly inside a `map()` call always need keys!

Keys tell React which array item each component corresponds to, so that it can match them up later. This becomes important if your array items can move (e.g. due to sorting), get inserted, or get deleted. A well-chosen `key` helps React infer what exactly has happened, and make the correct updates to the DOM tree.

Rather than generating keys on the fly, you should include them in your data:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export const people = [{
  id: 0, // Used in JSX as a key
  name: 'Creola Katherine Johnson',
  profession: 'mathematician',
  accomplishment: 'spaceflight calculations',
  imageId: 'MK3eW3A'
}, {
  id: 1, // Used in JSX as a key
  name: 'Mario José Molina-Pasquel Henríquez',
  profession: 'chemist',
  accomplishment: 'discovery of Arctic ozone hole',
  imageId: 'mynHUSa'
}, {
  id: 2, // Used in JSX as a key
  name: 'Mohammad Abdus Salam',
  profession: 'physicist',
  accomplishment: 'electromagnetism theory',
  imageId: 'bE7W1ji'
}, {
  id: 3, // Used in JSX as a key
  name: 'Percy Lavon Julian',
  profession: 'chemist',
  accomplishment: 'pioneering cortisone drugs, steroids and birth control pills',
  imageId: 'IOjWm71'
}, {
  id: 4, // Used in JSX as a key
  name: 'Subrahmanyan Chandrasekhar',
  profession: 'astrophysicist',
  accomplishment: 'white dwarf star mass calculations',
  imageId: 'lrWQx8l'
}];
```

/$

##### Deep Dive

#### Displaying several DOM nodes for each list item

What do you do when each item needs to render not one, but several DOM nodes?

The short [<>...</>Fragment](https://react.dev/reference/react/Fragment) syntax won’t let you pass a key, so you need to either group them into a single `<div>`, or use the slightly longer and [more explicit<Fragment>syntax:](https://react.dev/reference/react/Fragment#rendering-a-list-of-fragments)

$

```
import { Fragment } from 'react';// ...const listItems = people.map(person =>  <Fragment key={person.id}>    <h1>{person.name}</h1>    <p>{person.bio}</p>  </Fragment>);
```

/$

Fragments disappear from the DOM, so this will produce a flat list of `<h1>`, `<p>`, `<h1>`, `<p>`, and so on.

### Where to get yourkey

Different sources of data provide different sources of keys:

- **Data from a database:** If your data is coming from a database, you can use the database keys/IDs, which are unique by nature.
- **Locally generated data:** If your data is generated and persisted locally (e.g. notes in a note-taking app), use an incrementing counter, [crypto.randomUUID()](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/randomUUID) or a package like [uuid](https://www.npmjs.com/package/uuid) when creating items.

### Rules of keys

- **Keys must be unique among siblings.** However, it’s okay to use the same keys for JSX nodes in *different* arrays.
- **Keys must not change** or that defeats their purpose! Don’t generate them while rendering.

### Why does React need keys?

Imagine that files on your desktop didn’t have names. Instead, you’d refer to them by their order — the first file, the second file, and so on. You could get used to it, but once you delete a file, it would get confusing. The second file would become the first file, the third file would be the second file, and so on.

File names in a folder and JSX keys in an array serve a similar purpose. They let us uniquely identify an item between its siblings. A well-chosen key provides more information than the position within the array. Even if the *position* changes due to reordering, the `key` lets React identify the item throughout its lifetime.

### Pitfall

You might be tempted to use an item’s index in the array as its key. In fact, that’s what React will use if you don’t specify a `key` at all. But the order in which you render items will change over time if an item is inserted, deleted, or if the array gets reordered. Index as a key often leads to subtle and confusing bugs.

Similarly, do not generate keys on the fly, e.g. with `key={Math.random()}`. This will cause keys to never match up between renders, leading to all your components and DOM being recreated every time. Not only is this slow, but it will also lose any user input inside the list items. Instead, use a stable ID based on the data.

Note that your components won’t receive `key` as a prop. It’s only used as a hint by React itself. If your component needs an ID, you have to pass it as a separate prop: `<Profile key={id} userId={id} />`.

## Recap

On this page you learned:

- How to move data out of components and into data structures like arrays and objects.
- How to generate sets of similar components with JavaScript’s `map()`.
- How to create arrays of filtered items with JavaScript’s `filter()`.
- Why and how to set `key` on each component in a collection so React can keep track of each of them even if their position or data changes.

## Try out some challenges

#### Challenge1of4:Splitting a list in two

This example shows a list of all people.

Change it to show two separate lists one after another: **Chemists** and **Everyone Else.** Like previously, you can determine whether a person is a chemist by checking if `person.profession === 'chemist'`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { people } from './data.js';
import { getImageUrl } from './utils.js';

export default function List() {
  const listItems = people.map(person =>
    <li key={person.id}>
      <img
        src={getImageUrl(person)}
        alt={person.name}
      />
      <p>
        <b>{person.name}:</b>
        {' ' + person.profession + ' '}
        known for {person.accomplishment}
      </p>
    </li>
  );
  return (
    <article>
      <h1>Scientists</h1>
      <ul>{listItems}</ul>
    </article>
  );
}
```

/$[PreviousConditional Rendering](https://react.dev/learn/conditional-rendering)[NextKeeping Components Pure](https://react.dev/learn/keeping-components-pure)

---

# Responding to Events

[Learn React](https://react.dev/learn)[Adding Interactivity](https://react.dev/learn/adding-interactivity)

# Responding to Events

React lets you add *event handlers* to your JSX. Event handlers are your own functions that will be triggered in response to interactions like clicking, hovering, focusing form inputs, and so on.

### You will learn

- Different ways to write an event handler
- How to pass event handling logic from a parent component
- How events propagate and how to stop them

## Adding event handlers

To add an event handler, you will first define a function and then [pass it as a prop](https://react.dev/learn/passing-props-to-a-component) to the appropriate JSX tag. For example, here is a button that doesn’t do anything yet:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)export default function Button() { return ( <button>      I don't do anything </button> );}
/$

You can make it show a message when a user clicks by following these three steps:

1. Declare a function called `handleClick` *inside* your `Button` component.
2. Implement the logic inside that function (use `alert` to show the message).
3. Add `onClick={handleClick}` to the `<button>` JSX.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)export default function Button() { function handleClick() { alert('You clicked me!'); }
 return ( <button onClick={handleClick}>      Click me </button> );}
/$

You defined the `handleClick` function and then [passed it as a prop](https://react.dev/learn/passing-props-to-a-component) to `<button>`.  `handleClick` is an **event handler.** Event handler functions:

- Are usually defined *inside* your components.
- Have names that start with `handle`, followed by the name of the event.

By convention, it is common to name event handlers as `handle` followed by the event name. You’ll often see `onClick={handleClick}`, `onMouseEnter={handleMouseEnter}`, and so on.

Alternatively, you can define an event handler inline in the JSX:

 $

```
<button onClick={function handleClick() {  alert('You clicked me!');}}>
```

/$

Or, more concisely, using an arrow function:

 $

```
<button onClick={() => {  alert('You clicked me!');}}>
```

/$

All of these styles are equivalent. Inline event handlers are convenient for short functions.

### Pitfall

Functions passed to event handlers must be passed, not called. For example:

| passing a function (correct) | calling a function (incorrect) |
| --- | --- |
| <button onClick={handleClick}> | <button onClick={handleClick()}> |

The difference is subtle. In the first example, the `handleClick` function is passed as an `onClick` event handler. This tells React to remember it and only call your function when the user clicks the button.

In the second example, the `()` at the end of `handleClick()` fires the function *immediately* during [rendering](https://react.dev/learn/render-and-commit), without any clicks. This is because JavaScript inside the [JSX{and}](https://react.dev/learn/javascript-in-jsx-with-curly-braces) executes right away.

When you write code inline, the same pitfall presents itself in a different way:

| passing a function (correct) | calling a function (incorrect) |
| --- | --- |
| <button onClick={() => alert('...')}> | <button onClick={alert('...')}> |

Passing inline code like this won’t fire on click—it fires every time the component renders:

$

```
// This alert fires when the component renders, not when clicked!<button onClick={alert('You clicked me!')}>
```

/$

If you want to define your event handler inline, wrap it in an anonymous function like so:

$

```
<button onClick={() => alert('You clicked me!')}>
```

/$

Rather than executing the code inside with every render, this creates a function to be called later.

In both cases, what you want to pass is a function:

- `<button onClick={handleClick}>` passes the `handleClick` function.
- `<button onClick={() => alert('...')}>` passes the `() => alert('...')` function.

[Read more about arrow functions.](https://javascript.info/arrow-functions-basics)

### Reading props in event handlers

Because event handlers are declared inside of a component, they have access to the component’s props. Here is a button that, when clicked, shows an alert with its `message` prop:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function AlertButton({ message, children }) {
  return (
    <button onClick={() => alert(message)}>
      {children}
    </button>
  );
}

export default function Toolbar() {
  return (
    <div>
      <AlertButton message="Playing!">
        Play Movie
      </AlertButton>
      <AlertButton message="Uploading!">
        Upload Image
      </AlertButton>
    </div>
  );
}
```

/$

This lets these two buttons show different messages. Try changing the messages passed to them.

### Passing event handlers as props

Often you’ll want the parent component to specify a child’s event handler. Consider buttons: depending on where you’re using a `Button` component, you might want to execute a different function—perhaps one plays a movie and another uploads an image.

To do this, pass a prop the component receives from its parent as the event handler like so:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}

function PlayButton({ movieName }) {
  function handlePlayClick() {
    alert(`Playing ${movieName}!`);
  }

  return (
    <Button onClick={handlePlayClick}>
      Play "{movieName}"
    </Button>
  );
}

function UploadButton() {
  return (
    <Button onClick={() => alert('Uploading!')}>
      Upload Image
    </Button>
  );
}

export default function Toolbar() {
  return (
    <div>
      <PlayButton movieName="Kiki's Delivery Service" />
      <UploadButton />
    </div>
  );
}
```

/$

Here, the `Toolbar` component renders a `PlayButton` and an `UploadButton`:

- `PlayButton` passes `handlePlayClick` as the `onClick` prop to the `Button` inside.
- `UploadButton` passes `() => alert('Uploading!')` as the `onClick` prop to the `Button` inside.

Finally, your `Button` component accepts a prop called `onClick`. It passes that prop directly to the built-in browser `<button>` with `onClick={onClick}`. This tells React to call the passed function on click.

If you use a [design system](https://uxdesign.cc/everything-you-need-to-know-about-design-systems-54b109851969), it’s common for components like buttons to contain styling but not specify behavior. Instead, components like `PlayButton` and `UploadButton` will pass event handlers down.

### Naming event handler props

Built-in components like `<button>` and `<div>` only support [browser event names](https://react.dev/reference/react-dom/components/common#common-props) like `onClick`. However, when you’re building your own components, you can name their event handler props any way that you like.

By convention, event handler props should start with `on`, followed by a capital letter.

For example, the `Button` component’s `onClick` prop could have been called `onSmash`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Button({ onSmash, children }) {
  return (
    <button onClick={onSmash}>
      {children}
    </button>
  );
}

export default function App() {
  return (
    <div>
      <Button onSmash={() => alert('Playing!')}>
        Play Movie
      </Button>
      <Button onSmash={() => alert('Uploading!')}>
        Upload Image
      </Button>
    </div>
  );
}
```

/$

In this example, `<button onClick={onSmash}>` shows that the browser `<button>` (lowercase) still needs a prop called `onClick`, but the prop name received by your custom `Button` component is up to you!

When your component supports multiple interactions, you might name event handler props for app-specific concepts. For example, this `Toolbar` component receives `onPlayMovie` and `onUploadImage` event handlers:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function App() {
  return (
    <Toolbar
      onPlayMovie={() => alert('Playing!')}
      onUploadImage={() => alert('Uploading!')}
    />
  );
}

function Toolbar({ onPlayMovie, onUploadImage }) {
  return (
    <div>
      <Button onClick={onPlayMovie}>
        Play Movie
      </Button>
      <Button onClick={onUploadImage}>
        Upload Image
      </Button>
    </div>
  );
}

function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
```

/$

Notice how the `App` component does not need to know *what* `Toolbar` will do with `onPlayMovie` or `onUploadImage`. That’s an implementation detail of the `Toolbar`. Here, `Toolbar` passes them down as `onClick` handlers to its `Button`s, but it could later also trigger them on a keyboard shortcut. Naming props after app-specific interactions like `onPlayMovie` gives you the flexibility to change how they’re used later.

### Note

Make sure that you use the appropriate HTML tags for your event handlers. For example, to handle clicks, use [<button onClick={handleClick}>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) instead of `<div onClick={handleClick}>`. Using a real browser `<button>` enables built-in browser behaviors like keyboard navigation. If you don’t like the default browser styling of a button and want to make it look more like a link or a different UI element, you can achieve it with CSS. [Learn more about writing accessible markup.](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML)

## Event propagation

Event handlers will also catch events from any children your component might have. We say that an event “bubbles” or “propagates” up the tree: it starts with where the event happened, and then goes up the tree.

This `<div>` contains two buttons. Both the `<div>` *and* each button have their own `onClick` handlers. Which handlers do you think will fire when you click a button?

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('You clicked on the toolbar!');
    }}>
      <button onClick={() => alert('Playing!')}>
        Play Movie
      </button>
      <button onClick={() => alert('Uploading!')}>
        Upload Image
      </button>
    </div>
  );
}
```

/$

If you click on either button, its `onClick` will run first, followed by the parent `<div>`’s `onClick`. So two messages will appear. If you click the toolbar itself, only the parent `<div>`’s `onClick` will run.

### Pitfall

All events propagate in React except `onScroll`, which only works on the JSX tag you attach it to.

### Stopping propagation

Event handlers receive an **event object** as their only argument. By convention, it’s usually called `e`, which stands for “event”. You can use this object to read information about the event.

That event object also lets you stop the propagation. If you want to prevent an event from reaching parent components, you need to call `e.stopPropagation()` like this `Button` component does:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Button({ onClick, children }) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onClick();
    }}>
      {children}
    </button>
  );
}

export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('You clicked on the toolbar!');
    }}>
      <Button onClick={() => alert('Playing!')}>
        Play Movie
      </Button>
      <Button onClick={() => alert('Uploading!')}>
        Upload Image
      </Button>
    </div>
  );
}
```

/$

When you click on a button:

1. React calls the `onClick` handler passed to `<button>`.
2. That handler, defined in `Button`, does the following:
  - Calls `e.stopPropagation()`, preventing the event from bubbling further.
  - Calls the `onClick` function, which is a prop passed from the `Toolbar` component.
3. That function, defined in the `Toolbar` component, displays the button’s own alert.
4. Since the propagation was stopped, the parent `<div>`’s `onClick` handler does *not* run.

As a result of `e.stopPropagation()`, clicking on the buttons now only shows a single alert (from the `<button>`) rather than the two of them (from the `<button>` and the parent toolbar `<div>`). Clicking a button is not the same thing as clicking the surrounding toolbar, so stopping the propagation makes sense for this UI.

##### Deep Dive

#### Capture phase events

In rare cases, you might need to catch all events on child elements, *even if they stopped propagation*. For example, maybe you want to log every click to analytics, regardless of the propagation logic. You can do this by adding `Capture` at the end of the event name:

$

```
<div onClickCapture={() => { /* this runs first */ }}>  <button onClick={e => e.stopPropagation()} />  <button onClick={e => e.stopPropagation()} /></div>
```

/$

Each event propagates in three phases:

1. It travels down, calling all `onClickCapture` handlers.
2. It runs the clicked element’s `onClick` handler.
3. It travels upwards, calling all `onClick` handlers.

Capture events are useful for code like routers or analytics, but you probably won’t use them in app code.

### Passing handlers as alternative to propagation

Notice how this click handler runs a line of code *and then* calls the `onClick` prop passed by the parent:

 $

```
function Button({ onClick, children }) {  return (    <button onClick={e => {      e.stopPropagation();      onClick();    }}>      {children}    </button>  );}
```

/$

You could add more code to this handler before calling the parent `onClick` event handler, too. This pattern provides an *alternative* to propagation. It lets the child component handle the event, while also letting the parent component specify some additional behavior. Unlike propagation, it’s not automatic. But the benefit of this pattern is that you can clearly follow the whole chain of code that executes as a result of some event.

If you rely on propagation and it’s difficult to trace which handlers execute and why, try this approach instead.

### Preventing default behavior

Some browser events have default behavior associated with them. For example, a `<form>` submit event, which happens when a button inside of it is clicked, will reload the whole page by default:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Signup() {
  return (
    <form onSubmit={() => alert('Submitting!')}>
      <input />
      <button>Send</button>
    </form>
  );
}
```

/$

You can call `e.preventDefault()` on the event object to stop this from happening:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Signup() {
  return (
    <form onSubmit={e => {
      e.preventDefault();
      alert('Submitting!');
    }}>
      <input />
      <button>Send</button>
    </form>
  );
}
```

/$

Don’t confuse `e.stopPropagation()` and `e.preventDefault()`. They are both useful, but are unrelated:

- [e.stopPropagation()](https://developer.mozilla.org/docs/Web/API/Event/stopPropagation) stops the event handlers attached to the tags above from firing.
- [e.preventDefault()](https://developer.mozilla.org/docs/Web/API/Event/preventDefault) prevents the default browser behavior for the few events that have it.

## Can event handlers have side effects?

Absolutely! Event handlers are the best place for side effects.

Unlike rendering functions, event handlers don’t need to be [pure](https://react.dev/learn/keeping-components-pure), so it’s a great place to *change* something—for example, change an input’s value in response to typing, or change a list in response to a button press. However, in order to change some information, you first need some way to store it. In React, this is done by using [state, a component’s memory.](https://react.dev/learn/state-a-components-memory) You will learn all about it on the next page.

## Recap

- You can handle events by passing a function as a prop to an element like `<button>`.
- Event handlers must be passed, **not called!** `onClick={handleClick}`, not `onClick={handleClick()}`.
- You can define an event handler function separately or inline.
- Event handlers are defined inside a component, so they can access props.
- You can declare an event handler in a parent and pass it as a prop to a child.
- You can define your own event handler props with application-specific names.
- Events propagate upwards. Call `e.stopPropagation()` on the first argument to prevent that.
- Events may have unwanted default browser behavior. Call `e.preventDefault()` to prevent that.
- Explicitly calling an event handler prop from a child handler is a good alternative to propagation.

## Try out some challenges

#### Challenge1of2:Fix an event handler

Clicking this button is supposed to switch the page background between white and black. However, nothing happens when you click it. Fix the problem. (Don’t worry about the logic inside `handleClick`—that part is fine.)

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function LightSwitch() {
  function handleClick() {
    let bodyStyle = document.body.style;
    if (bodyStyle.backgroundColor === 'black') {
      bodyStyle.backgroundColor = 'white';
    } else {
      bodyStyle.backgroundColor = 'black';
    }
  }

  return (
    <button onClick={handleClick()}>
      Toggle the lights
    </button>
  );
}
```

/$[PreviousAdding Interactivity](https://react.dev/learn/adding-interactivity)[NextState: A Component's Memory](https://react.dev/learn/state-a-components-memory)
