# Add React to an Existing Project and more

# Add React to an Existing Project

[Learn React](https://react.dev/learn)[Installation](https://react.dev/learn/installation)

# Add React to an Existing Project

If you want to add some interactivity to your existing project, you don’t have to rewrite it in React. Add React to your existing stack, and render interactive React components anywhere.

### Note

**You need to installNode.jsfor local development.** Although you can [try React](https://react.dev/learn/installation#try-react) online or with a simple HTML page, realistically most JavaScript tooling you’ll want to use for development requires Node.js.

## Using React for an entire subroute of your existing website

Let’s say you have an existing web app at `example.com` built with another server technology (like Rails), and you want to implement all routes starting with `example.com/some-app/` fully with React.

Here’s how we recommend to set it up:

1. **Build the React part of your app** using one of the [React-based frameworks](https://react.dev/learn/creating-a-react-app).
2. **Specify/some-appas thebase path** in your framework’s configuration (here’s how: [Next.js](https://nextjs.org/docs/app/api-reference/config/next-config-js/basePath), [Gatsby](https://www.gatsbyjs.com/docs/how-to/previews-deploys-hosting/path-prefix/)).
3. **Configure your server or a proxy** so that all requests under `/some-app/` are handled by your React app.

This ensures the React part of your app can [benefit from the best practices](https://react.dev/learn/build-a-react-app-from-scratch#consider-using-a-framework) baked into those frameworks.

Many React-based frameworks are full-stack and let your React app take advantage of the server. However, you can use the same approach even if you can’t or don’t want to run JavaScript on the server. In that case, serve the HTML/CSS/JS export ([next exportoutput](https://nextjs.org/docs/advanced-features/static-html-export) for Next.js, default for Gatsby) at `/some-app/` instead.

## Using React for a part of your existing page

Let’s say you have an existing page built with another technology (either a server one like Rails, or a client one like Backbone), and you want to render interactive React components somewhere on that page. That’s a common way to integrate React—in fact, it’s how most React usage looked at Meta for many years!

You can do this in two steps:

1. **Set up a JavaScript environment** that lets you use the [JSX syntax](https://react.dev/learn/writing-markup-with-jsx), split your code into modules with the [import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) / [export](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export) syntax, and use packages (for example, React) from the [npm](https://www.npmjs.com/) package registry.
2. **Render your React components** where you want to see them on the page.

The exact approach depends on your existing page setup, so let’s walk through some details.

### Step 1: Set up a modular JavaScript environment

A modular JavaScript environment lets you write your React components in individual files, as opposed to writing all of your code in a single file. It also lets you use all the wonderful packages published by other developers on the [npm](https://www.npmjs.com/) registry—including React itself! How you do this depends on your existing setup:

- **If your app is already split into files that useimportstatements,** try to use the setup you already have. Check whether writing `<div />` in your JS code causes a syntax error. If it causes a syntax error, you might need to [transform your JavaScript code with Babel](https://babeljs.io/setup), and enable the [Babel React preset](https://babeljs.io/docs/babel-preset-react) to use JSX.
- **If your app doesn’t have an existing setup for compiling JavaScript modules,** set it up with [Vite](https://vite.dev/). The Vite community maintains [many integrations with backend frameworks](https://github.com/vitejs/awesome-vite#integrations-with-backends), including Rails, Django, and Laravel. If your backend framework is not listed, [follow this guide](https://vite.dev/guide/backend-integration.html) to manually integrate Vite builds with your backend.

To check whether your setup works, run this command in your project folder:

  Terminal

```
npm install react react-dom
```

Then add these lines of code at the top of your main JavaScript file (it might be called `index.js` or `main.js`):

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';

// Clear the existing HTML content
document.body.innerHTML = '<div id="app"></div>';

// Render your React component instead
const root = createRoot(document.getElementById('app'));
root.render(<h1>Hello, world</h1>);
```

/$

If the entire content of your page was replaced by a “Hello, world!”, everything worked! Keep reading.

### Note

Integrating a modular JavaScript environment into an existing project for the first time can feel intimidating, but it’s worth it! If you get stuck, try our [community resources](https://react.dev/community) or the [Vite Chat](https://chat.vite.dev/).

### Step 2: Render React components anywhere on the page

In the previous step, you put this code at the top of your main file:

 $

```
import { createRoot } from 'react-dom/client';// Clear the existing HTML contentdocument.body.innerHTML = '<div id="app"></div>';// Render your React component insteadconst root = createRoot(document.getElementById('app'));root.render(<h1>Hello, world</h1>);
```

/$

Of course, you don’t actually want to clear the existing HTML content!

Delete this code.

Instead, you probably want to render your React components in specific places in your HTML. Open your HTML page (or the server templates that generate it) and add a unique [id](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id) attribute to any tag, for example:

 $

```
<nav id="navigation"></nav>
```

/$

This lets you find that HTML element with [document.getElementById](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) and pass it to [createRoot](https://react.dev/reference/react-dom/client/createRoot) so that you can render your own React component inside:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';

function NavigationBar() {
  // TODO: Actually implement a navigation bar
  return <h1>Hello from React!</h1>;
}

const domNode = document.getElementById('navigation');
const root = createRoot(domNode);
root.render(<NavigationBar />);
```

/$

Notice how the original HTML content from `index.html` is preserved, but your own `NavigationBar` React component now appears inside the `<nav id="navigation">` from your HTML. Read the [createRootusage documentation](https://react.dev/reference/react-dom/client/createRoot#rendering-a-page-partially-built-with-react) to learn more about rendering React components inside an existing HTML page.

When you adopt React in an existing project, it’s common to start with small interactive components (like buttons), and then gradually keep “moving upwards” until eventually your entire page is built with React. If you ever reach that point, we recommend migrating to [a React framework](https://react.dev/learn/creating-a-react-app) right after to get the most out of React.

## Using React Native in an existing native mobile app

[React Native](https://reactnative.dev/) can also be integrated into existing native apps incrementally. If you have an existing native app for Android (Java or Kotlin) or iOS (Objective-C or Swift), [follow this guide](https://reactnative.dev/docs/integration-with-existing-apps) to add a React Native screen to it.

[PreviousBuild a React App from Scratch](https://react.dev/learn/build-a-react-app-from-scratch)[NextSetup](https://react.dev/learn/setup)

---

# Adding Interactivity

[Learn React](https://react.dev/learn)

# Adding Interactivity

Some things on the screen update in response to user input. For example, clicking an image gallery switches the active image. In React, data that changes over time is called *state.* You can add state to any component, and update it as needed. In this chapter, you’ll learn how to write components that handle interactions, update their state, and display different output over time.

### In this chapter

- [How to handle user-initiated events](https://react.dev/learn/responding-to-events)
- [How to make components “remember” information with state](https://react.dev/learn/state-a-components-memory)
- [How React updates the UI in two phases](https://react.dev/learn/render-and-commit)
- [Why state doesn’t update right after you change it](https://react.dev/learn/state-as-a-snapshot)
- [How to queue multiple state updates](https://react.dev/learn/queueing-a-series-of-state-updates)
- [How to update an object in state](https://react.dev/learn/updating-objects-in-state)
- [How to update an array in state](https://react.dev/learn/updating-arrays-in-state)

## Responding to events

React lets you add *event handlers* to your JSX. Event handlers are your own functions that will be triggered in response to user interactions like clicking, hovering, focusing on form inputs, and so on.

Built-in components like `<button>` only support built-in browser events like `onClick`. However, you can also create your own components, and give their event handler props any application-specific names that you like.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)export default function App() { return ( <Toolbar onPlayMovie={() => alert('Playing!')} onUploadImage={() => alert('Uploading!')} /> );}
function Toolbar({ onPlayMovie, onUploadImage }) { return ( <div> <Button onClick={onPlayMovie}>        Play Movie </Button> <Button onClick={onUploadImage}>        Upload Image </Button> </div> );}
function Button({ onClick, children }) { return ( <button onClick={onClick}> {children} </button> );}
/$

## Ready to learn this topic?

Read **Responding to Events** to learn how to add event handlers.

[Read More](https://react.dev/learn/responding-to-events)

---

## State: a component’s memory

Components often need to change what’s on the screen as a result of an interaction. Typing into the form should update the input field, clicking “next” on an image carousel should change which image is displayed, clicking “buy” puts a product in the shopping cart. Components need to “remember” things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called *state.*

You can add state to a component with a [useState](https://react.dev/reference/react/useState) Hook. *Hooks* are special functions that let your components use React features (state is one of those features). The `useState` Hook lets you declare a state variable. It takes the initial state and returns a pair of values: the current state, and a state setter function that lets you update it.

 $

```
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

/$

Here is how an image gallery uses and updates state on click:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { sculptureList } from './data.js';

export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);
  const hasNext = index < sculptureList.length - 1;

  function handleNextClick() {
    if (hasNext) {
      setIndex(index + 1);
    } else {
      setIndex(0);
    }
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

## Ready to learn this topic?

Read **State: A Component’s Memory** to learn how to remember a value and update it on interaction.

[Read More](https://react.dev/learn/state-a-components-memory)

---

## Render and commit

Before your components are displayed on the screen, they must be rendered by React. Understanding the steps in this process will help you think about how your code executes and explain its behavior.

Imagine that your components are cooks in the kitchen, assembling tasty dishes from ingredients. In this scenario, React is the waiter who puts in requests from customers and brings them their orders. This process of requesting and serving UI has three steps:

1. **Triggering** a render (delivering the diner’s order to the kitchen)
2. **Rendering** the component (preparing the order in the kitchen)
3. **Committing** to the DOM (placing the order on the table)

1. ![React as a server in a restaurant, fetching orders from the users and delivering them to the Component Kitchen.](https://react.dev/images/docs/illustrations/i_render-and-commit1.png)Trigger
2. ![The Card Chef gives React a fresh Card component.](https://react.dev/images/docs/illustrations/i_render-and-commit2.png)Render
3. ![React delivers the Card to the user at their table.](https://react.dev/images/docs/illustrations/i_render-and-commit3.png)Commit

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Ready to learn this topic?

Read **Render and Commit** to learn the lifecycle of a UI update.

[Read More](https://react.dev/learn/render-and-commit)

---

## State as a snapshot

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already have, but instead triggers a re-render. This can be surprising at first!

 $

```
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

/$

This behavior helps you avoid subtle bugs. Here is a little chat app. Try to guess what happens if you press “Send” first and *then* change the recipient to Bob. Whose name will appear in the `alert` five seconds later?

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [to, setTo] = useState('Alice');
  const [message, setMessage] = useState('Hello');

  function handleSubmit(e) {
    e.preventDefault();
    setTimeout(() => {
      alert(`You said ${message} to ${to}`);
    }, 5000);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        To:{' '}
        <select
          value={to}
          onChange={e => setTo(e.target.value)}>
          <option value="Alice">Alice</option>
          <option value="Bob">Bob</option>
        </select>
      </label>
      <textarea
        placeholder="Message"
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <button type="submit">Send</button>
    </form>
  );
}
```

/$

## Ready to learn this topic?

Read **State as a Snapshot** to learn why state appears “fixed” and unchanging inside the event handlers.

[Read More](https://react.dev/learn/state-as-a-snapshot)

---

## Queueing a series of state updates

This component is buggy: clicking “+3” increments the score only once.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [score, setScore] = useState(0);

  function increment() {
    setScore(score + 1);
  }

  return (
    <>
      <button onClick={() => increment()}>+1</button>
      <button onClick={() => {
        increment();
        increment();
        increment();
      }}>+3</button>
      <h1>Score: {score}</h1>
    </>
  )
}
```

/$

[State as a Snapshot](https://react.dev/learn/state-as-a-snapshot) explains why this is happening. Setting state requests a new re-render, but does not change it in the already running code. So `score` continues to be `0` right after you call `setScore(score + 1)`.

 $

```
console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0setScore(score + 1); // setScore(0 + 1);console.log(score);  // 0
```

/$

You can fix this by passing an *updater function* when setting state. Notice how replacing `setScore(score + 1)` with `setScore(s => s + 1)` fixes the “+3” button. This lets you queue multiple state updates.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [score, setScore] = useState(0);

  function increment() {
    setScore(s => s + 1);
  }

  return (
    <>
      <button onClick={() => increment()}>+1</button>
      <button onClick={() => {
        increment();
        increment();
        increment();
      }}>+3</button>
      <h1>Score: {score}</h1>
    </>
  )
}
```

/$

## Ready to learn this topic?

Read **Queueing a Series of State Updates** to learn how to queue a sequence of state updates.

[Read More](https://react.dev/learn/queueing-a-series-of-state-updates)

---

## Updating objects in state

State can hold any kind of JavaScript value, including objects. But you shouldn’t change objects and arrays that you hold in the React state directly. Instead, when you want to update an object and array, you need to create a new one (or make a copy of an existing one), and then update the state to use that copy.

Usually, you will use the `...` spread syntax to copy objects and arrays that you want to change. For example, updating a nested object could look like this:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [person, setPerson] = useState({
    name: 'Niki de Saint Phalle',
    artwork: {
      title: 'Blue Nana',
      city: 'Hamburg',
      image: 'https://i.imgur.com/Sd1AgUOm.jpg',
    }
  });

  function handleNameChange(e) {
    setPerson({
      ...person,
      name: e.target.value
    });
  }

  function handleTitleChange(e) {
    setPerson({
      ...person,
      artwork: {
        ...person.artwork,
        title: e.target.value
      }
    });
  }

  function handleCityChange(e) {
    setPerson({
      ...person,
      artwork: {
        ...person.artwork,
        city: e.target.value
      }
    });
  }

  function handleImageChange(e) {
    setPerson({
      ...person,
      artwork: {
        ...person.artwork,
        image: e.target.value
      }
    });
  }

  return (
    <>
      <label>
        Name:
        <input
          value={person.name}
          onChange={handleNameChange}
        />
      </label>
      <label>
        Title:
        <input
          value={person.artwork.title}
          onChange={handleTitleChange}
        />
      </label>
      <label>
        City:
        <input
          value={person.artwork.city}
          onChange={handleCityChange}
        />
      </label>
      <label>
        Image:
        <input
          value={person.artwork.image}
          onChange={handleImageChange}
        />
      </label>
      <p>
        <i>{person.artwork.title}</i>
        {' by '}
        {person.name}
        <br />
        (located in {person.artwork.city})
      </p>
      <img
        src={person.artwork.image}
        alt={person.artwork.title}
      />
    </>
  );
}
```

/$

If copying objects in code gets tedious, you can use a library like [Immer](https://github.com/immerjs/use-immer) to reduce repetitive code:

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

## Ready to learn this topic?

Read **Updating Objects in State** to learn how to update objects correctly.

[Read More](https://react.dev/learn/updating-objects-in-state)

---

## Updating arrays in state

Arrays are another type of mutable JavaScript objects you can store in state and should treat as read-only. Just like with objects, when you want to update an array stored in state, you need to create a new one (or make a copy of an existing one), and then set state to use the new array:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

const initialList = [
  { id: 0, title: 'Big Bellies', seen: false },
  { id: 1, title: 'Lunar Landscape', seen: false },
  { id: 2, title: 'Terracotta Army', seen: true },
];

export default function BucketList() {
  const [list, setList] = useState(
    initialList
  );

  function handleToggle(artworkId, nextSeen) {
    setList(list.map(artwork => {
      if (artwork.id === artworkId) {
        return { ...artwork, seen: nextSeen };
      } else {
        return artwork;
      }
    }));
  }

  return (
    <>
      <h1>Art Bucket List</h1>
      <h2>My list of art to see:</h2>
      <ItemList
        artworks={list}
        onToggle={handleToggle} />
    </>
  );
}

function ItemList({ artworks, onToggle }) {
  return (
    <ul>
      {artworks.map(artwork => (
        <li key={artwork.id}>
          <label>
            <input
              type="checkbox"
              checked={artwork.seen}
              onChange={e => {
                onToggle(
                  artwork.id,
                  e.target.checked
                );
              }}
            />
            {artwork.title}
          </label>
        </li>
      ))}
    </ul>
  );
}
```

/$

If copying arrays in code gets tedious, you can use a library like [Immer](https://github.com/immerjs/use-immer) to reduce repetitive code:

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

## Ready to learn this topic?

Read **Updating Arrays in State** to learn how to update arrays correctly.

[Read More](https://react.dev/learn/updating-arrays-in-state)

---

## What’s next?

Head over to [Responding to Events](https://react.dev/learn/responding-to-events) to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about [Managing State](https://react.dev/learn/managing-state)?

[PreviousYour UI as a Tree](https://react.dev/learn/understanding-your-ui-as-a-tree)[NextResponding to Events](https://react.dev/learn/responding-to-events)

---

# Build a React app from Scratch

[Learn React](https://react.dev/learn)[Installation](https://react.dev/learn/installation)

# Build a React app from Scratch

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can build a React app from scratch.

##### Deep Dive

#### Consider using a framework

Starting from scratch is an easy way to get started using React, but a major tradeoff to be aware of is that going this route is often the same as building your own adhoc framework. As your requirements evolve, you may need to solve more framework-like problems that our recommended frameworks already have well developed and supported solutions for.

For example, if in the future your app needs support for server-side rendering (SSR), static site generation (SSG), and/or React Server Components (RSC), you will have to implement those on your own. Similarly, future React features that require integrating at the framework level will have to be implemented on your own if you want to use them.

Our recommended frameworks also help you build better performing apps. For example, reducing or eliminating waterfalls from network requests makes for a better user experience. This might not be a high priority when you are building a toy project, but if your app gains users you may want to improve its performance.

Going this route also makes it more difficult to get support, since the way you develop routing, data-fetching, and other features will be unique to your situation. You should only choose this option if you are comfortable tackling these problems on your own, or if you’re confident that you will never need these features.

For a list of recommended frameworks, check out [Creating a React App](https://react.dev/learn/creating-a-react-app).

## Step 1: Install a build tool

The first step is to install a build tool like `vite`, `parcel`, or `rsbuild`. These build tools provide features to package and run source code, provide a development server for local development and a build command to deploy your app to a production server.

### Vite

[Vite](https://vite.dev/) is a build tool that aims to provide a faster and leaner development experience for modern web projects.

  Terminal

```
npm create vite@latest my-app -- --template react-ts
```

Vite is opinionated and comes with sensible defaults out of the box. Vite has a rich ecosystem of plugins to support fast refresh, JSX,  Babel/SWC, and other common features. See Vite’s [React plugin](https://vite.dev/plugins/#vitejs-plugin-react) or [React SWC plugin](https://vite.dev/plugins/#vitejs-plugin-react-swc) and [React SSR example project](https://vite.dev/guide/ssr.html#example-projects) to get started.

Vite is already being used as a build tool in one of our [recommended frameworks](https://react.dev/learn/creating-a-react-app): [React Router](https://reactrouter.com/start/framework/installation).

### Parcel

[Parcel](https://parceljs.org/) combines a great out-of-the-box development experience with a scalable architecture that can take your project from just getting started to massive production applications.

  Terminal

```
npm install --save-dev parcel
```

Parcel supports fast refresh, JSX, TypeScript, Flow, and styling out of the box. See [Parcel’s React recipe](https://parceljs.org/recipes/react/#getting-started) to get started.

### Rsbuild

[Rsbuild](https://rsbuild.dev/) is an Rspack-powered build tool that provides a seamless development experience for React applications. It comes with carefully tuned defaults and performance optimizations ready to use.

  Terminal

```
npx create-rsbuild --template react
```

Rsbuild includes built-in support for React features like fast refresh, JSX, TypeScript, and styling. See [Rsbuild’s React guide](https://rsbuild.dev/guide/framework/react) to get started.

### Note

#### Metro for React Native

If you’re starting from scratch with React Native you’ll need to use [Metro](https://metrobundler.dev/), the JavaScript bundler for React Native. Metro supports bundling for platforms like iOS and Android, but lacks many features when compared to the tools here. We recommend starting with Vite, Parcel, or Rsbuild unless your project requires React Native support.

## Step 2: Build Common Application Patterns

The build tools listed above start off with a client-only, single-page app (SPA), but don’t include any further solutions for common functionality like routing, data fetching, or styling.

The React ecosystem includes many tools for these problems. We’ve listed a few that are widely used as a starting point, but feel free to choose other tools if those work better for you.

### Routing

Routing determines what content or pages to display when a user visits a particular URL. You need to set up a router to map URLs to different parts of your app. You’ll also need to handle nested routes, route parameters, and query parameters.  Routers can be configured within your code, or defined based on your component folder and file structures.

Routers are a core part of modern applications, and are usually integrated with data fetching (including prefetching data for a whole page for faster loading), code splitting (to minimize client bundle sizes), and page rendering approaches (to decide how each page gets generated).

We suggest using:

- [React Router](https://reactrouter.com/start/data/custom)
- [Tanstack Router](https://tanstack.com/router/latest)

### Data Fetching

Fetching data from a server or other data source is a key part of most applications. Doing this properly requires handling loading states, error states, and caching the fetched data, which can be complex.

Purpose-built data fetching libraries do the hard work of fetching and caching the data for you, letting you focus on what data your app needs and how to display it.  These libraries are typically used directly in your components, but can also be integrated into routing loaders for faster pre-fetching and better performance, and in server rendering as well.

Note that fetching data directly in components can lead to slower loading times due to network request waterfalls, so we recommend prefetching data in router loaders or on the server as much as possible!  This allows a page’s data to be fetched all at once as the page is being displayed.

If you’re fetching data from most backends or REST-style APIs, we suggest using:

- [TanStack Query](https://tanstack.com/query/)
- [SWR](https://swr.vercel.app/)
- [RTK Query](https://redux-toolkit.js.org/rtk-query/overview)

If you’re fetching data from a GraphQL API, we suggest using:

- [Apollo](https://www.apollographql.com/docs/react)
- [Relay](https://relay.dev/)

### Code-splitting

Code-splitting is the process of breaking your app into smaller bundles that can be loaded on demand. An app’s code size increases with every new feature and additional dependency. Apps can become slow to load because all of the code for the entire app needs to be sent before it can be used. Caching, reducing features/dependencies, and moving some code to run on the server can help mitigate slow loading but are incomplete solutions that can sacrifice functionality if overused.

Similarly, if you rely on the apps using your framework to split the code, you might encounter situations where loading becomes slower than if no code splitting were happening at all. For example, [lazily loading](https://react.dev/reference/react/lazy) a chart delays sending the code needed to render the chart, splitting the chart code from the rest of the app. [Parcel supports code splitting with React.lazy](https://parceljs.org/recipes/react/#code-splitting). However, if the chart loads its data *after* it has been initially rendered you are now waiting twice. This is a waterfall: rather than fetching the data for the chart and sending the code to render it simultaneously, you must wait for each step to complete one after the other.

Splitting code by route, when integrated with bundling and data fetching, can reduce the initial load time of your app and the time it takes for the largest visible content of the app to render ([Largest Contentful Paint](https://web.dev/articles/lcp)).

For code-splitting instructions, see your build tool docs:

- [Vite build optimizations](https://vite.dev/guide/features.html#build-optimizations)
- [Parcel code splitting](https://parceljs.org/features/code-splitting/)
- [Rsbuild code splitting](https://rsbuild.dev/guide/optimization/code-splitting)

### Improving Application Performance

Since the build tool you select only supports single page apps (SPAs), you’ll need to implement other [rendering patterns](https://www.patterns.dev/vanilla/rendering-patterns) like server-side rendering (SSR), static site generation (SSG), and/or React Server Components (RSC). Even if you don’t need these features at first, in the future there may be some routes that would benefit SSR, SSG or RSC.

- **Single-page apps (SPA)** load a single HTML page and dynamically updates the page as the user interacts with the app. SPAs are easier to get started with, but they can have slower initial load times. SPAs are the default architecture for most build tools.
- **Streaming Server-side rendering (SSR)** renders a page on the server and sends the fully rendered page to the client. SSR can improve performance, but it can be more complex to set up and maintain than a single-page app. With the addition of streaming, SSR can be very complex to set up and maintain. See [Vite’s SSR guide](https://vite.dev/guide/ssr).
- **Static site generation (SSG)** generates static HTML files for your app at build time. SSG can improve performance, but it can be more complex to set up and maintain than server-side rendering. See [Vite’s SSG guide](https://vite.dev/guide/ssr.html#pre-rendering-ssg).
- **React Server Components (RSC)** lets you mix build-time, server-only, and interactive components in a single React tree. RSC can improve performance, but it currently requires deep expertise to set up and maintain. See [Parcel’s RSC examples](https://github.com/parcel-bundler/rsc-examples).

Your rendering strategies need to integrate with your router so apps built with your framework can choose the rendering strategy on a per-route level. This will enable different rendering strategies without having to rewrite your whole app. For example, the landing page for your app might benefit from being statically generated (SSG), while a page with a content feed might perform best with server-side rendering.

Using the right rendering strategy for the right routes can decrease the time it takes for the first byte of content to be loaded ([Time to First Byte](https://web.dev/articles/ttfb)), the first piece of content to render ([First Contentful Paint](https://web.dev/articles/fcp)), and the largest visible content of the app to render ([Largest Contentful Paint](https://web.dev/articles/lcp)).

### And more…

These are just a few examples of the features a new app will need to consider when building from scratch. Many limitations you’ll hit can be difficult to solve as each problem is interconnected with the others and can require deep expertise in problem areas you may not be familiar with.

If you don’t want to solve these problems on your own, you can [get started with a framework](https://react.dev/learn/creating-a-react-app) that provides these features out of the box.

[PreviousCreating a React App](https://react.dev/learn/creating-a-react-app)[NextAdd React to an Existing Project](https://react.dev/learn/add-react-to-an-existing-project)
