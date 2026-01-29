# Passing Data Deeply with Context and more

# Passing Data Deeply with Context

[Learn React](https://react.dev/learn)[Managing State](https://react.dev/learn/managing-state)

# Passing Data Deeply with Context

Usually, you will pass information from a parent component to a child component via props. But passing props can become verbose and inconvenient if you have to pass them through many components in the middle, or if many components in your app need the same information. *Context* lets the parent component make some information available to any component in the tree below it—no matter how deep—without passing it explicitly through props.

### You will learn

- What “prop drilling” is
- How to replace repetitive prop passing with context
- Common use cases for context
- Common alternatives to context

## The problem with passing props

[Passing props](https://react.dev/learn/passing-props-to-a-component) is a great way to explicitly pipe data through your UI tree to the components that use it.

But passing props can become verbose and inconvenient when you need to pass some prop deeply through the tree, or if many components need the same prop. The nearest common ancestor could be far removed from the components that need data, and [lifting state up](https://react.dev/learn/sharing-state-between-components) that high can lead to a situation called “prop drilling”.

Lifting state up

![Diagram with a tree of three components. The parent contains a bubble representing a value highlighted in purple. The value flows down to each of the two children, both highlighted in purple.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_lifting_state.dark.png&w=1920&q=75)![Diagram with a tree of three components. The parent contains a bubble representing a value highlighted in purple. The value flows down to each of the two children, both highlighted in purple.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_lifting_state.png&w=1920&q=75)

Prop drilling

![Diagram with a tree of ten nodes, each node with two children or less. The root node contains a bubble representing a value highlighted in purple. The value flows down through the two children, each of which pass the value but do not contain it. The left child passes the value down to two children which are both highlighted purple. The right child of the root passes the value through to one of its two children - the right one, which is highlighted purple. That child passed the value through its single child, which passes it down to both of its two children, which are highlighted purple.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_prop_drilling.dark.png&w=1920&q=75)![Diagram with a tree of ten nodes, each node with two children or less. The root node contains a bubble representing a value highlighted in purple. The value flows down through the two children, each of which pass the value but do not contain it. The left child passes the value down to two children which are both highlighted purple. The right child of the root passes the value through to one of its two children - the right one, which is highlighted purple. That child passed the value through its single child, which passes it down to both of its two children, which are highlighted purple.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_prop_drilling.png&w=1920&q=75)

Wouldn’t it be great if there were a way to “teleport” data to the components in the tree that need it without passing props? With React’s context feature, there is!

## Context: an alternative to passing props

Context lets a parent component provide data to the entire tree below it. There are many uses for context. Here is one example. Consider this `Heading` component that accepts a `level` for its size:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function Page() {
  return (
    <Section>
      <Heading level={1}>Title</Heading>
      <Heading level={2}>Heading</Heading>
      <Heading level={3}>Sub-heading</Heading>
      <Heading level={4}>Sub-sub-heading</Heading>
      <Heading level={5}>Sub-sub-sub-heading</Heading>
      <Heading level={6}>Sub-sub-sub-sub-heading</Heading>
    </Section>
  );
}
```

/$

Let’s say you want multiple headings within the same `Section` to always have the same size:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function Page() {
  return (
    <Section>
      <Heading level={1}>Title</Heading>
      <Section>
        <Heading level={2}>Heading</Heading>
        <Heading level={2}>Heading</Heading>
        <Heading level={2}>Heading</Heading>
        <Section>
          <Heading level={3}>Sub-heading</Heading>
          <Heading level={3}>Sub-heading</Heading>
          <Heading level={3}>Sub-heading</Heading>
          <Section>
            <Heading level={4}>Sub-sub-heading</Heading>
            <Heading level={4}>Sub-sub-heading</Heading>
            <Heading level={4}>Sub-sub-heading</Heading>
          </Section>
        </Section>
      </Section>
    </Section>
  );
}
```

/$

Currently, you pass the `level` prop to each `<Heading>` separately:

 $

```
<Section>  <Heading level={3}>About</Heading>  <Heading level={3}>Photos</Heading>  <Heading level={3}>Videos</Heading></Section>
```

/$

It would be nice if you could pass the `level` prop to the `<Section>` component instead and remove it from the `<Heading>`. This way you could enforce that all headings in the same section have the same size:

 $

```
<Section level={3}>  <Heading>About</Heading>  <Heading>Photos</Heading>  <Heading>Videos</Heading></Section>
```

/$

But how can the `<Heading>` component know the level of its closest `<Section>`? **That would require some way for a child to “ask” for data from somewhere above in the tree.**

You can’t do it with props alone. This is where context comes into play. You will do it in three steps:

1. **Create** a context. (You can call it `LevelContext`, since it’s for the heading level.)
2. **Use** that context from the component that needs the data. (`Heading` will use `LevelContext`.)
3. **Provide** that context from the component that specifies the data. (`Section` will provide `LevelContext`.)

Context lets a parent—even a distant one!—provide some data to the entire tree inside of it.

Using context in close children

![Diagram with a tree of three components. The parent contains a bubble representing a value highlighted in orange which projects down to the two children, each highlighted in orange.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_context_close.dark.png&w=1920&q=75)![Diagram with a tree of three components. The parent contains a bubble representing a value highlighted in orange which projects down to the two children, each highlighted in orange.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_context_close.png&w=1920&q=75)

Using context in distant children

![Diagram with a tree of ten nodes, each node with two children or less. The root parent node contains a bubble representing a value highlighted in orange. The value projects down directly to four leaves and one intermediate component in the tree, which are all highlighted in orange. None of the other intermediate components are highlighted.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_context_far.dark.png&w=1920&q=75)![Diagram with a tree of ten nodes, each node with two children or less. The root parent node contains a bubble representing a value highlighted in orange. The value projects down directly to four leaves and one intermediate component in the tree, which are all highlighted in orange. None of the other intermediate components are highlighted.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpassing_data_context_far.png&w=1920&q=75)

### Step 1: Create the context

First, you need to create the context. You’ll need to **export it from a file** so that your components can use it:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createContext } from 'react';

export const LevelContext = createContext(1);
```

/$

The only argument to `createContext` is the *default* value. Here, `1` refers to the biggest heading level, but you could pass any kind of value (even an object). You will see the significance of the default value in the next step.

### Step 2: Use the context

Import the `useContext` Hook from React and your context:

 $

```
import { useContext } from 'react';import { LevelContext } from './LevelContext.js';
```

/$

Currently, the `Heading` component reads `level` from props:

 $

```
export default function Heading({ level, children }) {  // ...}
```

/$

Instead, remove the `level` prop and read the value from the context you just imported, `LevelContext`:

 $

```
export default function Heading({ children }) {  const level = useContext(LevelContext);  // ...}
```

/$

`useContext` is a Hook. Just like `useState` and `useReducer`, you can only call a Hook immediately inside a React component (not inside loops or conditions). **useContexttells React that theHeadingcomponent wants to read theLevelContext.**

Now that the `Heading` component doesn’t have a `level` prop, you don’t need to pass the level prop to `Heading` in your JSX like this anymore:

 $

```
<Section>  <Heading level={4}>Sub-sub-heading</Heading>  <Heading level={4}>Sub-sub-heading</Heading>  <Heading level={4}>Sub-sub-heading</Heading></Section>
```

/$

Update the JSX so that it’s the `Section` that receives it instead:

 $

```
<Section level={4}>  <Heading>Sub-sub-heading</Heading>  <Heading>Sub-sub-heading</Heading>  <Heading>Sub-sub-heading</Heading></Section>
```

/$

As a reminder, this is the markup that you were trying to get working:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function Page() {
  return (
    <Section level={1}>
      <Heading>Title</Heading>
      <Section level={2}>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Section level={3}>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Section level={4}>
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

Notice this example doesn’t quite work, yet! All the headings have the same size because **even though you’reusingthe context, you have notprovidedit yet.** React doesn’t know where to get it!

If you don’t provide the context, React will use the default value you’ve specified in the previous step. In this example, you specified `1` as the argument to `createContext`, so `useContext(LevelContext)` returns `1`, setting all those headings to `<h1>`. Let’s fix this problem by having each `Section` provide its own context.

### Step 3: Provide the context

The `Section` component currently renders its children:

 $

```
export default function Section({ children }) {  return (    <section className="section">      {children}    </section>  );}
```

/$

**Wrap them with a context provider** to provide the `LevelContext` to them:

 $

```
import { LevelContext } from './LevelContext.js';export default function Section({ level, children }) {  return (    <section className="section">      <LevelContext value={level}>        {children}      </LevelContext>    </section>  );}
```

/$

This tells React: “if any component inside this `<Section>` asks for `LevelContext`, give them this `level`.” The component will use the value of the nearest `<LevelContext>` in the UI tree above it.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function Page() {
  return (
    <Section level={1}>
      <Heading>Title</Heading>
      <Section level={2}>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Heading>Heading</Heading>
        <Section level={3}>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Heading>Sub-heading</Heading>
          <Section level={4}>
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

It’s the same result as the original code, but you did not need to pass the `level` prop to each `Heading` component! Instead, it “figures out” its heading level by asking the closest `Section` above:

1. You pass a `level` prop to the `<Section>`.
2. `Section` wraps its children into `<LevelContext value={level}>`.
3. `Heading` asks the closest value of `LevelContext` above with `useContext(LevelContext)`.

## Using and providing context from the same component

Currently, you still have to specify each section’s `level` manually:

 $

```
export default function Page() {  return (    <Section level={1}>      ...      <Section level={2}>        ...        <Section level={3}>          ...
```

/$

Since context lets you read information from a component above, each `Section` could read the `level` from the `Section` above, and pass `level + 1` down automatically. Here is how you could do it:

 $

```
import { useContext } from 'react';import { LevelContext } from './LevelContext.js';export default function Section({ children }) {  const level = useContext(LevelContext);  return (    <section className="section">      <LevelContext value={level + 1}>        {children}      </LevelContext>    </section>  );}
```

/$

With this change, you don’t need to pass the `level` prop *either* to the `<Section>` or to the `<Heading>`:

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

Now both `Heading` and `Section` read the `LevelContext` to figure out how “deep” they are. And the `Section` wraps its children into the `LevelContext` to specify that anything inside of it is at a “deeper” level.

### Note

This example uses heading levels because they show visually how nested components can override context. But context is useful for many other use cases too. You can pass down any information needed by the entire subtree: the current color theme, the currently logged in user, and so on.

## Context passes through intermediate components

You can insert as many components as you like between the component that provides context and the one that uses it. This includes both built-in components like `<div>` and components you might build yourself.

In this example, the same `Post` component (with a dashed border) is rendered at two different nesting levels. Notice that the `<Heading>` inside of it gets its level automatically from the closest `<Section>`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Heading from './Heading.js';
import Section from './Section.js';

export default function ProfilePage() {
  return (
    <Section>
      <Heading>My Profile</Heading>
      <Post
        title="Hello traveller!"
        body="Read about my adventures."
      />
      <AllPosts />
    </Section>
  );
}

function AllPosts() {
  return (
    <Section>
      <Heading>Posts</Heading>
      <RecentPosts />
    </Section>
  );
}

function RecentPosts() {
  return (
    <Section>
      <Heading>Recent Posts</Heading>
      <Post
        title="Flavors of Lisbon"
        body="...those pastéis de nata!"
      />
      <Post
        title="Buenos Aires in the rhythm of tango"
        body="I loved it!"
      />
    </Section>
  );
}

function Post({ title, body }) {
  return (
    <Section isFancy={true}>
      <Heading>
        {title}
      </Heading>
      <p><i>{body}</i></p>
    </Section>
  );
}
```

/$

You didn’t do anything special for this to work. A `Section` specifies the context for the tree inside it, so you can insert a `<Heading>` anywhere, and it will have the correct size. Try it in the sandbox above!

**Context lets you write components that “adapt to their surroundings” and display themselves differently depending onwhere(or, in other words,in which context) they are being rendered.**

How context works might remind you of [CSS property inheritance.](https://developer.mozilla.org/en-US/docs/Web/CSS/inheritance) In CSS, you can specify `color: blue` for a `<div>`, and any DOM node inside of it, no matter how deep, will inherit that color unless some other DOM node in the middle overrides it with `color: green`. Similarly, in React, the only way to override some context coming from above is to wrap children into a context provider with a different value.

In CSS, different properties like `color` and `background-color` don’t override each other. You can set all  `<div>`’s `color` to red without impacting `background-color`. Similarly, **different React contexts don’t override each other.** Each context that you make with `createContext()` is completely separate from other ones, and ties together components using and providing *that particular* context. One component may use or provide many different contexts without a problem.

## Before you use context

Context is very tempting to use! However, this also means it’s too easy to overuse it. **Just because you need to pass some props several levels deep doesn’t mean you should put that information into context.**

Here’s a few alternatives you should consider before using context:

1. **Start bypassing props.** If your components are not trivial, it’s not unusual to pass a dozen props down through a dozen components. It may feel like a slog, but it makes it very clear which components use which data! The person maintaining your code will be glad you’ve made the data flow explicit with props.
2. **Extract components andpass JSX aschildrento them.** If you pass some data through many layers of intermediate components that don’t use that data (and only pass it further down), this often means that you forgot to extract some components along the way. For example, maybe you pass data props like `posts` to visual components that don’t use them directly, like `<Layout posts={posts} />`. Instead, make `Layout` take `children` as a prop, and render `<Layout><Posts posts={posts} /></Layout>`. This reduces the number of layers between the component specifying the data and the one that needs it.

If neither of these approaches works well for you, consider context.

## Use cases for context

- **Theming:** If your app lets the user change its appearance (e.g. dark mode), you can put a context provider at the top of your app, and use that context in components that need to adjust their visual look.
- **Current account:** Many components might need to know the currently logged in user. Putting it in context makes it convenient to read it anywhere in the tree. Some apps also let you operate multiple accounts at the same time (e.g. to leave a comment as a different user). In those cases, it can be convenient to wrap a part of the UI into a nested provider with a different current account value.
- **Routing:** Most routing solutions use context internally to hold the current route. This is how every link “knows” whether it’s active or not. If you build your own router, you might want to do it too.
- **Managing state:** As your app grows, you might end up with a lot of state closer to the top of your app. Many distant components below may want to change it. It is common to [use a reducer together with context](https://react.dev/learn/scaling-up-with-reducer-and-context) to manage complex state and pass it down to distant components without too much hassle.

Context is not limited to static values. If you pass a different value on the next render, React will update all the components reading it below! This is why context is often used in combination with state.

In general, if some information is needed by distant components in different parts of the tree, it’s a good indication that context will help you.

## Recap

- Context lets a component provide some information to the entire tree below it.
- To pass context:
  1. Create and export it with `export const MyContext = createContext(defaultValue)`.
  2. Pass it to the `useContext(MyContext)` Hook to read it in any child component, no matter how deep.
  3. Wrap children into `<MyContext value={...}>` to provide it from a parent.
- Context passes through any components in the middle.
- Context lets you write components that “adapt to their surroundings”.
- Before you use context, try passing props or passing JSX as `children`.

## Try out some challenges

#### Challenge1of1:Replace prop drilling with context

In this example, toggling the checkbox changes the `imageSize` prop passed to each `<PlaceImage>`. The checkbox state is held in the top-level `App` component, but each `<PlaceImage>` needs to be aware of it.

Currently, `App` passes `imageSize` to `List`, which passes it to each `Place`, which passes it to the `PlaceImage`. Remove the `imageSize` prop, and instead pass it from the `App` component directly to `PlaceImage`.

You can declare context in `Context.js`.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { places } from './data.js';
import { getImageUrl } from './utils.js';

export default function App() {
  const [isLarge, setIsLarge] = useState(false);
  const imageSize = isLarge ? 150 : 100;
  return (
    <>
      <label>
        <input
          type="checkbox"
          checked={isLarge}
          onChange={e => {
            setIsLarge(e.target.checked);
          }}
        />
        Use large images
      </label>
      <hr />
      <List imageSize={imageSize} />
    </>
  )
}

function List({ imageSize }) {
  const listItems = places.map(place =>
    <li key={place.id}>
      <Place
        place={place}
        imageSize={imageSize}
      />
    </li>
  );
  return <ul>{listItems}</ul>;
}

function Place({ place, imageSize }) {
  return (
    <>
      <PlaceImage
        place={place}
        imageSize={imageSize}
      />
      <p>
        <b>{place.name}</b>
        {': ' + place.description}
      </p>
    </>
  );
}

function PlaceImage({ place, imageSize }) {
  return (
    <img
      src={getImageUrl(place)}
      alt={place.name}
      width={imageSize}
      height={imageSize}
    />
  );
}
```

/$[PreviousExtracting State Logic into a Reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer)[NextScaling Up with Reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context)

---

# Passing Props to a Component

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Passing Props to a Component

React components use *props* to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, and functions.

### You will learn

- How to pass props to a component
- How to read props from a component
- How to specify default values for props
- How to pass some JSX to a component
- How props change over time

## Familiar props

Props are the information that you pass to a JSX tag. For example, `className`, `src`, `alt`, `width`, and `height` are some of the props you can pass to an `<img>`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)function Avatar() { return ( <img className="avatar" src="https://i.imgur.com/1bX5QH6.jpg" alt="Lin Lanying" width={100} height={100} /> );}
export default function Profile() { return ( <Avatar /> );}
/$

The props you can pass to an `<img>` tag are predefined (ReactDOM conforms to [the HTML standard](https://www.w3.org/TR/html52/semantics-embedded-content.html#the-img-element)). But you can pass any props to *your own* components, such as `<Avatar>`, to customize them. Here’s how!

## Passing props to a component

In this code, the `Profile` component isn’t passing any props to its child component, `Avatar`:

 $

```
export default function Profile() {  return (    <Avatar />  );}
```

/$

You can give `Avatar` some props in two steps.

### Step 1: Pass props to the child component

First, pass some props to `Avatar`. For example, let’s pass two props: `person` (an object), and `size` (a number):

 $

```
export default function Profile() {  return (    <Avatar      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}      size={100}    />  );}
```

/$

### Note

If double curly braces after `person=` confuse you, recall [they’re merely an object](https://react.dev/learn/javascript-in-jsx-with-curly-braces#using-double-curlies-css-and-other-objects-in-jsx) inside the JSX curlies.

Now you can read these props inside the `Avatar` component.

### Step 2: Read props inside the child component

You can read these props by listing their names `person, size` separated by the commas inside `({` and `})` directly after `function Avatar`. This lets you use them inside the `Avatar` code, like you would with a variable.

 $

```
function Avatar({ person, size }) {  // person and size are available here}
```

/$

Add some logic to `Avatar` that uses the `person` and `size` props for rendering, and you’re done.

Now you can configure `Avatar` to render in many different ways with different props. Try tweaking the values!

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { getImageUrl } from './utils.js';

function Avatar({ person, size }) {
  return (
    <img
      className="avatar"
      src={getImageUrl(person)}
      alt={person.name}
      width={size}
      height={size}
    />
  );
}

export default function Profile() {
  return (
    <div>
      <Avatar
        size={100}
        person={{
          name: 'Katsuko Saruhashi',
          imageId: 'YfeOqp2'
        }}
      />
      <Avatar
        size={80}
        person={{
          name: 'Aklilu Lemma',
          imageId: 'OKS67lh'
        }}
      />
      <Avatar
        size={50}
        person={{
          name: 'Lin Lanying',
          imageId: '1bX5QH6'
        }}
      />
    </div>
  );
}
```

/$

Props let you think about parent and child components independently. For example, you can change the `person` or the `size` props inside `Profile` without having to think about how `Avatar` uses them. Similarly, you can change how the `Avatar` uses these props, without looking at the `Profile`.

You can think of props like “knobs” that you can adjust. They serve the same role as arguments serve for functions—in fact, props *are* the only argument to your component! React component functions accept a single argument, a `props` object:

 $

```
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

/$

Usually you don’t need the whole `props` object itself, so you destructure it into individual props.

### Pitfall

**Don’t miss the pair of{and}curlies** inside of `(` and `)` when declaring props:

$

```
function Avatar({ person, size }) {  // ...}
```

/$

This syntax is called [“destructuring”](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment#Unpacking_fields_from_objects_passed_as_a_function_parameter) and is equivalent to reading properties from a function parameter:

$

```
function Avatar(props) {  let person = props.person;  let size = props.size;  // ...}
```

/$

## Specifying a default value for a prop

If you want to give a prop a default value to fall back on when no value is specified, you can do it with the destructuring by putting `=` and the default value right after the parameter:

 $

```
function Avatar({ person, size = 100 }) {  // ...}
```

/$

Now, if `<Avatar person={...} />` is rendered with no `size` prop, the `size` will be set to `100`.

The default value is only used if the `size` prop is missing or if you pass `size={undefined}`. But if you pass `size={null}` or `size={0}`, the default value will **not** be used.

## Forwarding props with the JSX spread syntax

Sometimes, passing props gets very repetitive:

 $

```
function Profile({ person, size, isSepia, thickBorder }) {  return (    <div className="card">      <Avatar        person={person}        size={size}        isSepia={isSepia}        thickBorder={thickBorder}      />    </div>  );}
```

/$

There’s nothing wrong with repetitive code—it can be more legible. But at times you may value conciseness. Some components forward all of their props to their children, like how this `Profile` does with `Avatar`. Because they don’t use any of their props directly, it can make sense to use a more concise “spread” syntax:

 $

```
function Profile(props) {  return (    <div className="card">      <Avatar {...props} />    </div>  );}
```

/$

This forwards all of `Profile`’s props to the `Avatar` without listing each of their names.

**Use spread syntax with restraint.** If you’re using it in every other component, something is wrong. Often, it indicates that you should split your components and pass children as JSX. More on that next!

## Passing JSX as children

It is common to nest built-in browser tags:

 $

```
<div>  <img /></div>
```

/$

Sometimes you’ll want to nest your own components the same way:

 $

```
<Card>  <Avatar /></Card>
```

/$

When you nest content inside a JSX tag, the parent component will receive that content in a prop called `children`. For example, the `Card` component below will receive a `children` prop set to `<Avatar />` and render it in a wrapper div:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Avatar from './Avatar.js';

function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

export default function Profile() {
  return (
    <Card>
      <Avatar
        size={100}
        person={{
          name: 'Katsuko Saruhashi',
          imageId: 'YfeOqp2'
        }}
      />
    </Card>
  );
}
```

/$

Try replacing the `<Avatar>` inside `<Card>` with some text to see how the `Card` component can wrap any nested content. It doesn’t need to “know” what’s being rendered inside of it. You will see this flexible pattern in many places.

You can think of a component with a `children` prop as having a “hole” that can be “filled in” by its parent components with arbitrary JSX. You will often use the `children` prop for visual wrappers: panels, grids, etc.

 ![A puzzle-like Card tile with a slot for "children" pieces like text and Avatar](https://react.dev/images/docs/illustrations/i_children-prop.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## How props change over time

The `Clock` component below receives two props from its parent component: `color` and `time`. (The parent component’s code is omitted because it uses [state](https://react.dev/learn/state-a-components-memory), which we won’t dive into just yet.)

Try changing the color in the select box below:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Clock({ color, time }) {
  return (
    <h1 style={{ color: color }}>
      {time}
    </h1>
  );
}
```

/$

This example illustrates that **a component may receive different props over time.** Props are not always static! Here, the `time` prop changes every second, and the `color` prop changes when you select another color. Props reflect a component’s data at any point in time, rather than only in the beginning.

However, props are [immutable](https://en.wikipedia.org/wiki/Immutable_object)—a term from computer science meaning “unchangeable”. When a component needs to change its props (for example, in response to a user interaction or new data), it will have to “ask” its parent component to pass it *different props*—a new object! Its old props will then be cast aside, and eventually the JavaScript engine will reclaim the memory taken by them.

**Don’t try to “change props”.** When you need to respond to the user input (like changing the selected color), you will need to “set state”, which you can learn about in [State: A Component’s Memory.](https://react.dev/learn/state-a-components-memory)

## Recap

- To pass props, add them to the JSX, just like you would with HTML attributes.
- To read props, use the `function Avatar({ person, size })` destructuring syntax.
- You can specify a default value like `size = 100`, which is used for missing and `undefined` props.
- You can forward all props with `<Avatar {...props} />` JSX spread syntax, but don’t overuse it!
- Nested JSX like `<Card><Avatar /></Card>` will appear as `Card` component’s `children` prop.
- Props are read-only snapshots in time: every render receives a new version of props.
- You can’t change props. When you need interactivity, you’ll need to set state.

## Try out some challenges

#### Challenge1of3:Extract a component

This `Gallery` component contains some very similar markup for two profiles. Extract a `Profile` component out of it to reduce the duplication. You’ll need to choose what props to pass to it.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { getImageUrl } from './utils.js';

export default function Gallery() {
  return (
    <div>
      <h1>Notable Scientists</h1>
      <section className="profile">
        <h2>Maria Skłodowska-Curie</h2>
        <img
          className="avatar"
          src={getImageUrl('szV5sdG')}
          alt="Maria Skłodowska-Curie"
          width={70}
          height={70}
        />
        <ul>
          <li>
            <b>Profession: </b>
            physicist and chemist
          </li>
          <li>
            <b>Awards: 4 </b>
            (Nobel Prize in Physics, Nobel Prize in Chemistry, Davy Medal, Matteucci Medal)
          </li>
          <li>
            <b>Discovered: </b>
            polonium (chemical element)
          </li>
        </ul>
      </section>
      <section className="profile">
        <h2>Katsuko Saruhashi</h2>
        <img
          className="avatar"
          src={getImageUrl('YfeOqp2')}
          alt="Katsuko Saruhashi"
          width={70}
          height={70}
        />
        <ul>
          <li>
            <b>Profession: </b>
            geochemist
          </li>
          <li>
            <b>Awards: 2 </b>
            (Miyake Prize for geochemistry, Tanaka Prize)
          </li>
          <li>
            <b>Discovered: </b>
            a method for measuring carbon dioxide in seawater
          </li>
        </ul>
      </section>
    </div>
  );
}
```

/$[PreviousJavaScript in JSX with Curly Braces](https://react.dev/learn/javascript-in-jsx-with-curly-braces)[NextConditional Rendering](https://react.dev/learn/conditional-rendering)
