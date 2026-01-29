# <StrictMode> and more

# <StrictMode>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react/components)

# <StrictMode>

`<StrictMode>` lets you find common bugs in your components early during development.

$

```
<StrictMode>  <App /></StrictMode>
```

/$

- [Reference](#reference)
  - [<StrictMode>](#strictmode)
- [Usage](#usage)
  - [Enabling Strict Mode for entire app](#enabling-strict-mode-for-entire-app)
  - [Enabling Strict Mode for a part of the app](#enabling-strict-mode-for-a-part-of-the-app)
  - [Fixing bugs found by double rendering in development](#fixing-bugs-found-by-double-rendering-in-development)
  - [Fixing bugs found by re-running Effects in development](#fixing-bugs-found-by-re-running-effects-in-development)
  - [Fixing bugs found by re-running ref callbacks in development](#fixing-bugs-found-by-re-running-ref-callbacks-in-development)
  - [Fixing deprecation warnings enabled by Strict Mode](#fixing-deprecation-warnings-enabled-by-strict-mode)

---

## Reference

### <StrictMode>

Use `StrictMode` to enable additional development behaviors and warnings for the component tree inside:

 $

```
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

/$

[See more examples below.](#usage)

Strict Mode enables the following development-only behaviors:

- Your components will [re-render an extra time](#fixing-bugs-found-by-double-rendering-in-development) to find bugs caused by impure rendering.
- Your components will [re-run Effects an extra time](#fixing-bugs-found-by-re-running-effects-in-development) to find bugs caused by missing Effect cleanup.
- Your components will [re-run refs callbacks an extra time](#fixing-bugs-found-by-re-running-ref-callbacks-in-development) to find bugs caused by missing ref cleanup.
- Your components will [be checked for usage of deprecated APIs.](#fixing-deprecation-warnings-enabled-by-strict-mode)

#### Props

`StrictMode` accepts no props.

#### Caveats

- There is no way to opt out of Strict Mode inside a tree wrapped in `<StrictMode>`. This gives you confidence that all components inside `<StrictMode>` are checked. If two teams working on a product disagree whether they find the checks valuable, they need to either reach consensus or move `<StrictMode>` down in the tree.

---

## Usage

### Enabling Strict Mode for entire app

Strict Mode enables extra development-only checks for the entire component tree inside the `<StrictMode>` component. These checks help you find common bugs in your components early in the development process.

To enable Strict Mode for your entire app, wrap your root component with `<StrictMode>` when you render it:

 $

```
import { StrictMode } from 'react';import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(  <StrictMode>    <App />  </StrictMode>);
```

/$

We recommend wrapping your entire app in Strict Mode, especially for newly created apps. If you use a framework that calls [createRoot](https://react.dev/reference/react-dom/client/createRoot) for you, check its documentation for how to enable Strict Mode.

Although the Strict Mode checks **only run in development,** they help you find bugs that already exist in your code but can be tricky to reliably reproduce in production. Strict Mode lets you fix bugs before your users report them.

### Note

Strict Mode enables the following checks in development:

- Your components will [re-render an extra time](#fixing-bugs-found-by-double-rendering-in-development) to find bugs caused by impure rendering.
- Your components will [re-run Effects an extra time](#fixing-bugs-found-by-re-running-effects-in-development) to find bugs caused by missing Effect cleanup.
- Your components will [re-run ref callbacks an extra time](#fixing-bugs-found-by-re-running-ref-callbacks-in-development) to find bugs caused by missing ref cleanup.
- Your components will [be checked for usage of deprecated APIs.](#fixing-deprecation-warnings-enabled-by-strict-mode)

**All of these checks are development-only and do not impact the production build.**

---

### Enabling Strict Mode for a part of the app

You can also enable Strict Mode for any part of your application:

 $

```
import { StrictMode } from 'react';function App() {  return (    <>      <Header />      <StrictMode>        <main>          <Sidebar />          <Content />        </main>      </StrictMode>      <Footer />    </>  );}
```

/$

In this example, Strict Mode checks will not run against the `Header` and `Footer` components. However, they will run on `Sidebar` and `Content`, as well as all of the components inside them, no matter how deep.

### Note

When `StrictMode` is enabled for a part of the app, React will only enable behaviors that are possible in production. For example, if `<StrictMode>` is not enabled at the root of the app, it will not [re-run Effects an extra time](#fixing-bugs-found-by-re-running-effects-in-development) on initial mount, since this would cause child effects to double fire without the parent effects, which cannot happen in production.

---

### Fixing bugs found by double rendering in development

[React assumes that every component you write is a pure function.](https://react.dev/learn/keeping-components-pure) This means that React components you write must always return the same JSX given the same inputs (props, state, and context).

Components breaking this rule behave unpredictably and cause bugs. To help you find accidentally impure code, Strict Mode calls some of your functions (only the ones that should be pure) **twice in development.** This includes:

- Your component function body (only top-level logic, so this doesn’t include code inside event handlers)
- Functions that you pass to [useState](https://react.dev/reference/react/useState), [setfunctions](https://react.dev/reference/react/useState#setstate), [useMemo](https://react.dev/reference/react/useMemo), or [useReducer](https://react.dev/reference/react/useReducer)
- Some class component methods like [constructor](https://react.dev/reference/react/Component#constructor), [render](https://react.dev/reference/react/Component#render), [shouldComponentUpdate](https://react.dev/reference/react/Component#shouldcomponentupdate) ([see the whole list](https://reactjs.org/docs/strict-mode.html#detecting-unexpected-side-effects))

If a function is pure, running it twice does not change its behavior because a pure function produces the same result every time. However, if a function is impure (for example, it mutates the data it receives), running it twice tends to be noticeable (that’s what makes it impure!) This helps you spot and fix the bug early.

**Here is an example to illustrate how double rendering in Strict Mode helps you find bugs early.**

This `StoryTray` component takes an array of `stories` and adds one last “Create Story” item at the end:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function StoryTray({ stories }) {
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul>
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

/$

There is a mistake in the code above. However, it is easy to miss because the initial output appears correct.

This mistake will become more noticeable if the `StoryTray` component re-renders multiple times. For example, let’s make the `StoryTray` re-render with a different background color whenever you hover over it:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function StoryTray({ stories }) {
  const [isHover, setIsHover] = useState(false);
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul
      onPointerEnter={() => setIsHover(true)}
      onPointerLeave={() => setIsHover(false)}
      style={{
        backgroundColor: isHover ? '#ddd' : '#fff'
      }}
    >
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

/$

Notice how every time you hover over the `StoryTray` component, “Create Story” gets added to the list again. The intention of the code was to add it once at the end. But `StoryTray` directly modifies the `stories` array from the props. Every time `StoryTray` renders, it adds “Create Story” again at the end of the same array. In other words, `StoryTray` is not a pure function—running it multiple times produces different results.

To fix this problem, you can make a copy of the array, and modify that copy instead of the original one:

 $

```
export default function StoryTray({ stories }) {  const items = stories.slice(); // Clone the array  // ✅ Good: Pushing into a new array  items.push({ id: 'create', label: 'Create Story' });
```

/$

This would [make theStoryTrayfunction pure.](https://react.dev/learn/keeping-components-pure) Each time it is called, it would only modify a new copy of the array, and would not affect any external objects or variables. This solves the bug, but you had to make the component re-render more often before it became obvious that something is wrong with its behavior.

**In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in<StrictMode>:**

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function StoryTray({ stories }) {
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul>
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

/$

**Strict Modealwayscalls your rendering function twice, so you can see the mistake right away** (“Create Story” appears twice). This lets you notice such mistakes early in the process. When you fix your component to render in Strict Mode, you *also* fix many possible future production bugs like the hover functionality from before:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function StoryTray({ stories }) {
  const [isHover, setIsHover] = useState(false);
  const items = stories.slice(); // Clone the array
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul
      onPointerEnter={() => setIsHover(true)}
      onPointerLeave={() => setIsHover(false)}
      style={{
        backgroundColor: isHover ? '#ddd' : '#fff'
      }}
    >
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

/$

Without Strict Mode, it was easy to miss the bug until you added more re-renders. Strict Mode made the same bug appear right away. Strict Mode helps you find bugs before you push them to your team and to your users.

[Read more about keeping components pure.](https://react.dev/learn/keeping-components-pure)

### Note

If you have [React DevTools](https://react.dev/learn/react-developer-tools) installed, any `console.log` calls during the second render call will appear slightly dimmed. React DevTools also offers a setting (off by default) to suppress them completely.

---

### Fixing bugs found by re-running Effects in development

Strict Mode can also help find bugs in [Effects.](https://react.dev/learn/synchronizing-with-effects)

Every Effect has some setup code and may have some cleanup code. Normally, React calls setup when the component *mounts* (is added to the screen) and calls cleanup when the component *unmounts* (is removed from the screen). React then calls cleanup and setup again if its dependencies changed since the last render.

When Strict Mode is on, React will also run **one extra setup+cleanup cycle in development for every Effect.** This may feel surprising, but it helps reveal subtle bugs that are hard to catch manually.

**Here is an example to illustrate how re-running Effects in Strict Mode helps you find bugs early.**

Consider this example that connects a component to a chat:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

/$

There is an issue with this code, but it might not be immediately clear.

To make the issue more obvious, let’s implement a feature. In the example below, `roomId` is not hardcoded. Instead, the user can select the `roomId` that they want to connect to from a dropdown. Click “Open chat” and then select different chat rooms one by one. Keep track of the number of active connections in the console:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

/$

You’ll notice that the number of open connections always keeps growing. In a real app, this would cause performance and network problems. The issue is that [your Effect is missing a cleanup function:](https://react.dev/learn/synchronizing-with-effects#step-3-add-cleanup-if-needed)

 $

```
useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.connect();    return () => connection.disconnect();  }, [roomId]);
```

/$

Now that your Effect “cleans up” after itself and destroys the outdated connections, the leak is solved. However, notice that the problem did not become visible until you’ve added more features (the select box).

**In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in<StrictMode>:**

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

/$

**With Strict Mode, you immediately see that there is a problem** (the number of active connections jumps to 2). Strict Mode runs an extra setup+cleanup cycle for every Effect. This Effect has no cleanup logic, so it creates an extra connection but doesn’t destroy it. This is a hint that you’re missing a cleanup function.

Strict Mode lets you notice such mistakes early in the process. When you fix your Effect by adding a cleanup function in Strict Mode, you *also* fix many possible future production bugs like the select box from before:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

/$

Notice how the active connection count in the console doesn’t keep growing anymore.

Without Strict Mode, it was easy to miss that your Effect needed cleanup. By running *setup → cleanup → setup* instead of *setup* for your Effect in development, Strict Mode made the missing cleanup logic more noticeable.

[Read more about implementing Effect cleanup.](https://react.dev/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development)

---

### Fixing bugs found by re-running ref callbacks in development

Strict Mode can also help find bugs in [callbacks refs.](https://react.dev/learn/manipulating-the-dom-with-refs)

Every callback `ref` has some setup code and may have some cleanup code. Normally, React calls setup when the element is *created* (is added to the DOM) and calls cleanup when the element is *removed* (is removed from the DOM).

When Strict Mode is on, React will also run **one extra setup+cleanup cycle in development for every callbackref.** This may feel surprising, but it helps reveal subtle bugs that are hard to catch manually.

Consider this example, which allows you to select an animal and then scroll to one of them. Notice when you switch from “Cats” to “Dogs”, the console logs show that the number of animals in the list keeps growing, and the “Scroll to” buttons stop working:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useState } from "react";

export default function CatFriends() {
  const itemsRef = useRef([]);
  const [catList, setCatList] = useState(setupCatList);
  const [cat, setCat] = useState('neo');

  function scrollToCat(index) {
    const list = itemsRef.current;
    const {node} = list[index];
    node.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  const cats = catList.filter(c => c.type === cat)

  return (
    <>
      <nav>
        <button onClick={() => setCat('neo')}>Neo</button>
        <button onClick={() => setCat('millie')}>Millie</button>
      </nav>
      <hr />
      <nav>
        <span>Scroll to:</span>{cats.map((cat, index) => (
          <button key={cat.src} onClick={() => scrollToCat(index)}>
            {index}
          </button>
        ))}
      </nav>
      <div>
        <ul>
          {cats.map((cat) => (
            <li
              key={cat.src}
              ref={(node) => {
                const list = itemsRef.current;
                const item = {cat: cat, node};
                list.push(item);
                console.log(`✅ Adding cat to the map. Total cats: ${list.length}`);
                if (list.length > 10) {
                  console.log('❌ Too many cats in the list!');
                }
                return () => {
                  // 🚩 No cleanup, this is a bug!
                }
              }}
            >
              <img src={cat.src} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function setupCatList() {
  const catList = [];
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'neo', src: "https://placecats.com/neo/320/240?" + i});
  }
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'millie', src: "https://placecats.com/millie/320/240?" + i});
  }

  return catList;
}
```

/$

**This is a production bug!** Since the ref callback doesn’t remove animals from the list in the cleanup, the list of animals keeps growing. This is a memory leak that can cause performance problems in a real app, and breaks the behavior of the app.

The issue is the ref callback doesn’t cleanup after itself:

 $

```
<li  ref={node => {    const list = itemsRef.current;    const item = {animal, node};    list.push(item);    return () => {      // 🚩 No cleanup, this is a bug!    }  }}</li>
```

/$

Now let’s wrap the original (buggy) code in `<StrictMode>`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useState } from "react";

export default function CatFriends() {
  const itemsRef = useRef([]);
  const [catList, setCatList] = useState(setupCatList);
  const [cat, setCat] = useState('neo');

  function scrollToCat(index) {
    const list = itemsRef.current;
    const {node} = list[index];
    node.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  const cats = catList.filter(c => c.type === cat)

  return (
    <>
      <nav>
        <button onClick={() => setCat('neo')}>Neo</button>
        <button onClick={() => setCat('millie')}>Millie</button>
      </nav>
      <hr />
      <nav>
        <span>Scroll to:</span>{cats.map((cat, index) => (
          <button key={cat.src} onClick={() => scrollToCat(index)}>
            {index}
          </button>
        ))}
      </nav>
      <div>
        <ul>
          {cats.map((cat) => (
            <li
              key={cat.src}
              ref={(node) => {
                const list = itemsRef.current;
                const item = {cat: cat, node};
                list.push(item);
                console.log(`✅ Adding cat to the map. Total cats: ${list.length}`);
                if (list.length > 10) {
                  console.log('❌ Too many cats in the list!');
                }
                return () => {
                  // 🚩 No cleanup, this is a bug!
                }
              }}
            >
              <img src={cat.src} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function setupCatList() {
  const catList = [];
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'neo', src: "https://placecats.com/neo/320/240?" + i});
  }
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'millie', src: "https://placecats.com/millie/320/240?" + i});
  }

  return catList;
}
```

/$

**With Strict Mode, you immediately see that there is a problem**. Strict Mode runs an extra setup+cleanup cycle for every callback ref. This callback ref has no cleanup logic, so it adds refs but doesn’t remove them. This is a hint that you’re missing a cleanup function.

Strict Mode lets you eagerly find mistakes in callback refs. When you fix your callback by adding a cleanup function in Strict Mode, you *also* fix many possible future production bugs like the “Scroll to” bug from before:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useState } from "react";

export default function CatFriends() {
  const itemsRef = useRef([]);
  const [catList, setCatList] = useState(setupCatList);
  const [cat, setCat] = useState('neo');

  function scrollToCat(index) {
    const list = itemsRef.current;
    const {node} = list[index];
    node.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
      inline: "center",
    });
  }

  const cats = catList.filter(c => c.type === cat)

  return (
    <>
      <nav>
        <button onClick={() => setCat('neo')}>Neo</button>
        <button onClick={() => setCat('millie')}>Millie</button>
      </nav>
      <hr />
      <nav>
        <span>Scroll to:</span>{cats.map((cat, index) => (
          <button key={cat.src} onClick={() => scrollToCat(index)}>
            {index}
          </button>
        ))}
      </nav>
      <div>
        <ul>
          {cats.map((cat) => (
            <li
              key={cat.src}
              ref={(node) => {
                const list = itemsRef.current;
                const item = {cat: cat, node};
                list.push(item);
                console.log(`✅ Adding cat to the map. Total cats: ${list.length}`);
                if (list.length > 10) {
                  console.log('❌ Too many cats in the list!');
                }
                return () => {
                  list.splice(list.indexOf(item), 1);
                  console.log(`❌ Removing cat from the map. Total cats: ${itemsRef.current.length}`);
                }
              }}
            >
              <img src={cat.src} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function setupCatList() {
  const catList = [];
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'neo', src: "https://placecats.com/neo/320/240?" + i});
  }
  for (let i = 0; i < 10; i++) {
    catList.push({type: 'millie', src: "https://placecats.com/millie/320/240?" + i});
  }

  return catList;
}
```

/$

Now on inital mount in StrictMode, the ref callbacks are all setup, cleaned up, and setup again:

 $

```
...✅ Adding animal to the map. Total animals: 10...❌ Removing animal from the map. Total animals: 0...✅ Adding animal to the map. Total animals: 10
```

/$

**This is expected.** Strict Mode confirms that the ref callbacks are cleaned up correctly, so the size never grows above the expected amount. After the fix, there are no memory leaks, and all the features work as expected.

Without Strict Mode, it was easy to miss the bug until you clicked around to app to notice broken features. Strict Mode made the bugs appear right away, before you push them to production.

---

### Fixing deprecation warnings enabled by Strict Mode

React warns if some component anywhere inside a `<StrictMode>` tree uses one of these deprecated APIs:

- `UNSAFE_` class lifecycle methods like [UNSAFE_componentWillMount](https://react.dev/reference/react/Component#unsafe_componentwillmount). [See alternatives.](https://reactjs.org/blog/2018/03/27/update-on-async-rendering.html#migrating-from-legacy-lifecycles)

These APIs are primarily used in older [class components](https://react.dev/reference/react/Component) so they rarely appear in modern apps.

[Previous<Profiler>](https://react.dev/reference/react/Profiler)[Next<Suspense>](https://react.dev/reference/react/Suspense)

---

# <Suspense>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react/components)

# <Suspense>

`<Suspense>` lets you display a fallback until its children have finished loading.

$

```
<Suspense fallback={<Loading />}>  <SomeComponent /></Suspense>
```

/$

- [Reference](#reference)
  - [<Suspense>](#suspense)
- [Usage](#usage)
  - [Displaying a fallback while content is loading](#displaying-a-fallback-while-content-is-loading)
  - [Revealing content together at once](#revealing-content-together-at-once)
  - [Revealing nested content as it loads](#revealing-nested-content-as-it-loads)
  - [Showing stale content while fresh content is loading](#showing-stale-content-while-fresh-content-is-loading)
  - [Preventing already revealed content from hiding](#preventing-already-revealed-content-from-hiding)
  - [Indicating that a Transition is happening](#indicating-that-a-transition-is-happening)
  - [Resetting Suspense boundaries on navigation](#resetting-suspense-boundaries-on-navigation)
  - [Providing a fallback for server errors and client-only content](#providing-a-fallback-for-server-errors-and-client-only-content)
- [Troubleshooting](#troubleshooting)
  - [How do I prevent the UI from being replaced by a fallback during an update?](#preventing-unwanted-fallbacks)

---

## Reference

### <Suspense>

#### Props

- `children`: The actual UI you intend to render. If `children` suspends while rendering, the Suspense boundary will switch to rendering `fallback`.
- `fallback`: An alternate UI to render in place of the actual UI if it has not finished loading. Any valid React node is accepted, though in practice, a fallback is a lightweight placeholder view, such as a loading spinner or skeleton. Suspense will automatically switch to `fallback` when `children` suspends, and back to `children` when the data is ready. If `fallback` suspends while rendering, it will activate the closest parent Suspense boundary.

#### Caveats

- React does not preserve any state for renders that got suspended before they were able to mount for the first time. When the component has loaded, React will retry rendering the suspended tree from scratch.
- If Suspense was displaying content for the tree, but then it suspended again, the `fallback` will be shown again unless the update causing it was caused by [startTransition](https://react.dev/reference/react/startTransition) or [useDeferredValue](https://react.dev/reference/react/useDeferredValue).
- If React needs to hide the already visible content because it suspended again, it will clean up [layout Effects](https://react.dev/reference/react/useLayoutEffect) in the content tree. When the content is ready to be shown again, React will fire the layout Effects again. This ensures that Effects measuring the DOM layout don’t try to do this while the content is hidden.
- React includes under-the-hood optimizations like *Streaming Server Rendering* and *Selective Hydration* that are integrated with Suspense. Read [an architectural overview](https://github.com/reactwg/react-18/discussions/37) and watch [a technical talk](https://www.youtube.com/watch?v=pj5N-Khihgc) to learn more.

---

## Usage

### Displaying a fallback while content is loading

You can wrap any part of your application with a Suspense boundary:

 $

```
<Suspense fallback={<Loading />}>  <Albums /></Suspense>
```

/$

React will display your loading fallback until all the code and data needed by the children has been loaded.

In the example below, the `Albums` component *suspends* while fetching the list of albums. Until it’s ready to render, React switches the closest Suspense boundary above to show the fallback—your `Loading` component. Then, when the data loads, React hides the `Loading` fallback and renders the `Albums` component with data.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense } from 'react';
import Albums from './Albums.js';

export default function ArtistPage({ artist }) {
  return (
    <>
      <h1>{artist.name}</h1>
      <Suspense fallback={<Loading />}>
        <Albums artistId={artist.id} />
      </Suspense>
    </>
  );
}

function Loading() {
  return <h2>🌀 Loading...</h2>;
}
```

/$

### Note

**Only Suspense-enabled data sources will activate the Suspense component.** They include:

- Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming#streaming-with-suspense)
- Lazy-loading component code with [lazy](https://react.dev/reference/react/lazy)
- Reading the value of a cached Promise with [use](https://react.dev/reference/react/use)

Suspense **does not** detect when data is fetched inside an Effect or event handler.

The exact way you would load data in the `Albums` component above depends on your framework. If you use a Suspense-enabled framework, you’ll find the details in its data fetching documentation.

Suspense-enabled data fetching without the use of an opinionated framework is not yet supported. The requirements for implementing a Suspense-enabled data source are unstable and undocumented. An official API for integrating data sources with Suspense will be released in a future version of React.

---

### Revealing content together at once

By default, the whole tree inside Suspense is treated as a single unit. For example, even if *only one* of these components suspends waiting for some data, *all* of them together will be replaced by the loading indicator:

 $

```
<Suspense fallback={<Loading />}>  <Biography />  <Panel>    <Albums />  </Panel></Suspense>
```

/$

Then, after all of them are ready to be displayed, they will all appear together at once.

In the example below, both `Biography` and `Albums` fetch some data. However, because they are grouped under a single Suspense boundary, these components always “pop in” together at the same time.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense } from 'react';
import Albums from './Albums.js';
import Biography from './Biography.js';
import Panel from './Panel.js';

export default function ArtistPage({ artist }) {
  return (
    <>
      <h1>{artist.name}</h1>
      <Suspense fallback={<Loading />}>
        <Biography artistId={artist.id} />
        <Panel>
          <Albums artistId={artist.id} />
        </Panel>
      </Suspense>
    </>
  );
}

function Loading() {
  return <h2>🌀 Loading...</h2>;
}
```

/$

Components that load data don’t have to be direct children of the Suspense boundary. For example, you can move `Biography` and `Albums` into a new `Details` component. This doesn’t change the behavior. `Biography` and `Albums` share the same closest parent Suspense boundary, so their reveal is coordinated together.

 $

```
<Suspense fallback={<Loading />}>  <Details artistId={artist.id} /></Suspense>function Details({ artistId }) {  return (    <>      <Biography artistId={artistId} />      <Panel>        <Albums artistId={artistId} />      </Panel>    </>  );}
```

/$

---

### Revealing nested content as it loads

When a component suspends, the closest parent Suspense component shows the fallback. This lets you nest multiple Suspense components to create a loading sequence. Each Suspense boundary’s fallback will be filled in as the next level of content becomes available. For example, you can give the album list its own fallback:

 $

```
<Suspense fallback={<BigSpinner />}>  <Biography />  <Suspense fallback={<AlbumsGlimmer />}>    <Panel>      <Albums />    </Panel>  </Suspense></Suspense>
```

/$

With this change, displaying the `Biography` doesn’t need to “wait” for the `Albums` to load.

The sequence will be:

1. If `Biography` hasn’t loaded yet, `BigSpinner` is shown in place of the entire content area.
2. Once `Biography` finishes loading, `BigSpinner` is replaced by the content.
3. If `Albums` hasn’t loaded yet, `AlbumsGlimmer` is shown in place of `Albums` and its parent `Panel`.
4. Finally, once `Albums` finishes loading, it replaces `AlbumsGlimmer`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense } from 'react';
import Albums from './Albums.js';
import Biography from './Biography.js';
import Panel from './Panel.js';

export default function ArtistPage({ artist }) {
  return (
    <>
      <h1>{artist.name}</h1>
      <Suspense fallback={<BigSpinner />}>
        <Biography artistId={artist.id} />
        <Suspense fallback={<AlbumsGlimmer />}>
          <Panel>
            <Albums artistId={artist.id} />
          </Panel>
        </Suspense>
      </Suspense>
    </>
  );
}

function BigSpinner() {
  return <h2>🌀 Loading...</h2>;
}

function AlbumsGlimmer() {
  return (
    <div className="glimmer-panel">
      <div className="glimmer-line" />
      <div className="glimmer-line" />
      <div className="glimmer-line" />
    </div>
  );
}
```

/$

Suspense boundaries let you coordinate which parts of your UI should always “pop in” together at the same time, and which parts should progressively reveal more content in a sequence of loading states. You can add, move, or delete Suspense boundaries in any place in the tree without affecting the rest of your app’s behavior.

Don’t put a Suspense boundary around every component. Suspense boundaries should not be more granular than the loading sequence that you want the user to experience. If you work with a designer, ask them where the loading states should be placed—it’s likely that they’ve already included them in their design wireframes.

---

### Showing stale content while fresh content is loading

In this example, the `SearchResults` component suspends while fetching the search results. Type `"a"`, wait for the results, and then edit it to `"ab"`. The results for `"a"` will get replaced by the loading fallback.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <SearchResults query={query} />
      </Suspense>
    </>
  );
}
```

/$

A common alternative UI pattern is to *defer* updating the list and to keep showing the previous results until the new results are ready. The [useDeferredValue](https://react.dev/reference/react/useDeferredValue) Hook lets you pass a deferred version of the query down:

 $

```
export default function App() {  const [query, setQuery] = useState('');  const deferredQuery = useDeferredValue(query);  return (    <>      <label>        Search albums:        <input value={query} onChange={e => setQuery(e.target.value)} />      </label>      <Suspense fallback={<h2>Loading...</h2>}>        <SearchResults query={deferredQuery} />      </Suspense>    </>  );}
```

/$

The `query` will update immediately, so the input will display the new value. However, the `deferredQuery` will keep its previous value until the data has loaded, so `SearchResults` will show the stale results for a bit.

To make it more obvious to the user, you can add a visual indication when the stale result list is displayed:

 $

```
<div style={{  opacity: query !== deferredQuery ? 0.5 : 1 }}>  <SearchResults query={deferredQuery} /></div>
```

/$

Enter `"a"` in the example below, wait for the results to load, and then edit the input to `"ab"`. Notice how instead of the Suspense fallback, you now see the dimmed stale result list until the new results have loaded:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState, useDeferredValue } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <div style={{ opacity: isStale ? 0.5 : 1 }}>
          <SearchResults query={deferredQuery} />
        </div>
      </Suspense>
    </>
  );
}
```

/$

### Note

Both deferred values and [Transitions](#preventing-already-revealed-content-from-hiding) let you avoid showing Suspense fallback in favor of inline indicators. Transitions mark the whole update as non-urgent so they are typically used by frameworks and router libraries for navigation. Deferred values, on the other hand, are mostly useful in application code where you want to mark a part of UI as non-urgent and let it “lag behind” the rest of the UI.

---

### Preventing already revealed content from hiding

When a component suspends, the closest parent Suspense boundary switches to showing the fallback. This can lead to a jarring user experience if it was already displaying some content. Try pressing this button:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState } from 'react';
import IndexPage from './IndexPage.js';
import ArtistPage from './ArtistPage.js';
import Layout from './Layout.js';

export default function App() {
  return (
    <Suspense fallback={<BigSpinner />}>
      <Router />
    </Suspense>
  );
}

function Router() {
  const [page, setPage] = useState('/');

  function navigate(url) {
    setPage(url);
  }

  let content;
  if (page === '/') {
    content = (
      <IndexPage navigate={navigate} />
    );
  } else if (page === '/the-beatles') {
    content = (
      <ArtistPage
        artist={{
          id: 'the-beatles',
          name: 'The Beatles',
        }}
      />
    );
  }
  return (
    <Layout>
      {content}
    </Layout>
  );
}

function BigSpinner() {
  return <h2>🌀 Loading...</h2>;
}
```

/$

When you pressed the button, the `Router` component rendered `ArtistPage` instead of `IndexPage`. A component inside `ArtistPage` suspended, so the closest Suspense boundary started showing the fallback. The closest Suspense boundary was near the root, so the whole site layout got replaced by `BigSpinner`.

To prevent this, you can mark the navigation state update as a *Transition* with [startTransition:](https://react.dev/reference/react/startTransition)

 $

```
function Router() {  const [page, setPage] = useState('/');  function navigate(url) {    startTransition(() => {      setPage(url);          });  }  // ...
```

/$

This tells React that the state transition is not urgent, and it’s better to keep showing the previous page instead of hiding any already revealed content. Now clicking the button “waits” for the `Biography` to load:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, startTransition, useState } from 'react';
import IndexPage from './IndexPage.js';
import ArtistPage from './ArtistPage.js';
import Layout from './Layout.js';

export default function App() {
  return (
    <Suspense fallback={<BigSpinner />}>
      <Router />
    </Suspense>
  );
}

function Router() {
  const [page, setPage] = useState('/');

  function navigate(url) {
    startTransition(() => {
      setPage(url);
    });
  }

  let content;
  if (page === '/') {
    content = (
      <IndexPage navigate={navigate} />
    );
  } else if (page === '/the-beatles') {
    content = (
      <ArtistPage
        artist={{
          id: 'the-beatles',
          name: 'The Beatles',
        }}
      />
    );
  }
  return (
    <Layout>
      {content}
    </Layout>
  );
}

function BigSpinner() {
  return <h2>🌀 Loading...</h2>;
}
```

/$

A Transition doesn’t wait for *all* content to load. It only waits long enough to avoid hiding already revealed content. For example, the website `Layout` was already revealed, so it would be bad to hide it behind a loading spinner. However, the nested `Suspense` boundary around `Albums` is new, so the Transition doesn’t wait for it.

### Note

Suspense-enabled routers are expected to wrap the navigation updates into Transitions by default.

---

### Indicating that a Transition is happening

In the above example, once you click the button, there is no visual indication that a navigation is in progress. To add an indicator, you can replace [startTransition](https://react.dev/reference/react/startTransition) with [useTransition](https://react.dev/reference/react/useTransition) which gives you a boolean `isPending` value. In the example below, it’s used to change the website header styling while a Transition is happening:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Suspense, useState, useTransition } from 'react';
import IndexPage from './IndexPage.js';
import ArtistPage from './ArtistPage.js';
import Layout from './Layout.js';

export default function App() {
  return (
    <Suspense fallback={<BigSpinner />}>
      <Router />
    </Suspense>
  );
}

function Router() {
  const [page, setPage] = useState('/');
  const [isPending, startTransition] = useTransition();

  function navigate(url) {
    startTransition(() => {
      setPage(url);
    });
  }

  let content;
  if (page === '/') {
    content = (
      <IndexPage navigate={navigate} />
    );
  } else if (page === '/the-beatles') {
    content = (
      <ArtistPage
        artist={{
          id: 'the-beatles',
          name: 'The Beatles',
        }}
      />
    );
  }
  return (
    <Layout isPending={isPending}>
      {content}
    </Layout>
  );
}

function BigSpinner() {
  return <h2>🌀 Loading...</h2>;
}
```

/$

---

### Resetting Suspense boundaries on navigation

During a Transition, React will avoid hiding already revealed content. However, if you navigate to a route with different parameters, you might want to tell React it is *different* content. You can express this with a `key`:

 $

```
<ProfilePage key={queryParams.id} />
```

/$

Imagine you’re navigating within a user’s profile page, and something suspends. If that update is wrapped in a Transition, it will not trigger the fallback for already visible content. That’s the expected behavior.

However, now imagine you’re navigating between two different user profiles. In that case, it makes sense to show the fallback. For example, one user’s timeline is *different content* from another user’s timeline. By specifying a `key`, you ensure that React treats different users’ profiles as different components, and resets the Suspense boundaries during navigation. Suspense-integrated routers should do this automatically.

---

### Providing a fallback for server errors and client-only content

If you use one of the [streaming server rendering APIs](https://react.dev/reference/react-dom/server) (or a framework that relies on them), React will also use your `<Suspense>` boundaries to handle errors on the server. If a component throws an error on the server, React will not abort the server render. Instead, it will find the closest `<Suspense>` component above it and include its fallback (such as a spinner) into the generated server HTML. The user will see a spinner at first.

On the client, React will attempt to render the same component again. If it errors on the client too, React will throw the error and display the closest [Error Boundary.](https://react.dev/reference/react/Component#static-getderivedstatefromerror) However, if it does not error on the client, React will not display the error to the user since the content was eventually displayed successfully.

You can use this to opt out some components from rendering on the server. To do this, throw an error in the server environment and then wrap them in a `<Suspense>` boundary to replace their HTML with fallbacks:

 $

```
<Suspense fallback={<Loading />}>  <Chat /></Suspense>function Chat() {  if (typeof window === 'undefined') {    throw Error('Chat should only render on the client.');  }  // ...}
```

/$

The server HTML will include the loading indicator. It will be replaced by the `Chat` component on the client.

---

## Troubleshooting

### How do I prevent the UI from being replaced by a fallback during an update?

Replacing visible UI with a fallback creates a jarring user experience. This can happen when an update causes a component to suspend, and the nearest Suspense boundary is already showing content to the user.

To prevent this from happening, [mark the update as non-urgent usingstartTransition](#preventing-already-revealed-content-from-hiding). During a Transition, React will wait until enough data has loaded to prevent an unwanted fallback from appearing:

 $

```
function handleNextPageClick() {  // If this update suspends, don't hide the already displayed content  startTransition(() => {    setCurrentPage(currentPage + 1);  });}
```

/$

This will avoid hiding existing content. However, any newly rendered `Suspense` boundaries will still immediately display fallbacks to avoid blocking the UI and let the user see the content as it becomes available.

**React will only prevent unwanted fallbacks during non-urgent updates**. It will not delay a render if it’s the result of an urgent update. You must opt in with an API like [startTransition](https://react.dev/reference/react/startTransition) or [useDeferredValue](https://react.dev/reference/react/useDeferredValue).

If your router is integrated with Suspense, it should wrap its updates into [startTransition](https://react.dev/reference/react/startTransition) automatically.

[Previous<StrictMode>](https://react.dev/reference/react/StrictMode)[Next<Activity>](https://react.dev/reference/react/Activity)
