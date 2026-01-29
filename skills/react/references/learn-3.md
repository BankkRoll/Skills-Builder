# Creating a React App and more

# Creating a React App

[Learn React](https://react.dev/learn)[Installation](https://react.dev/learn/installation)

# Creating a React App

If you want to build a new app or website with React, we recommend starting with a framework.

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, you can [build a React app from scratch](https://react.dev/learn/build-a-react-app-from-scratch).

## Full-stack frameworks

These recommended frameworks support all the features you need to deploy and scale your app in production. They have integrated the latest React features and take advantage of React’s architecture.

### Note

#### Full-stack frameworks do not require a server.

All the frameworks on this page support client-side rendering ([CSR](https://developer.mozilla.org/en-US/docs/Glossary/CSR)), single-page apps ([SPA](https://developer.mozilla.org/en-US/docs/Glossary/SPA)), and static-site generation ([SSG](https://developer.mozilla.org/en-US/docs/Glossary/SSG)). These apps can be deployed to a [CDN](https://developer.mozilla.org/en-US/docs/Glossary/CDN) or static hosting service without a server. Additionally, these frameworks allow you to add server-side rendering on a per-route basis, when it makes sense for your use case.

This allows you to start with a client-only app, and if your needs change later, you can opt-in to using server features on individual routes without rewriting your app. See your framework’s documentation for configuring the rendering strategy.

### Next.js (App Router)

**Next.js’s App Routeris a React framework that takes full advantage of React’s architecture to enable full-stack React apps.**

  Terminal

```
npx create-next-app@latest
```

Next.js is maintained by [Vercel](https://vercel.com/). You can [deploy a Next.js app](https://nextjs.org/docs/app/building-your-application/deploying) to any hosting provider that supports Node.js or Docker containers, or to your own server. Next.js also supports [static export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports) which doesn’t require a server.

### React Router (v7)

**React Routeris the most popular routing library for React and can be paired with Vite to create a full-stack React framework**. It emphasizes standard Web APIs and has several [ready to deploy templates](https://github.com/remix-run/react-router-templates) for various JavaScript runtimes and platforms.

To create a new React Router framework project, run:

  Terminal

```
npx create-react-router@latest
```

React Router is maintained by [Shopify](https://www.shopify.com).

### Expo (for native apps)

**Expois a React framework that lets you create universal Android, iOS, and web apps with truly native UIs.** It provides an SDK for [React Native](https://reactnative.dev/) that makes the native parts easier to use. To create a new Expo project, run:

  Terminal

```
npx create-expo-app@latest
```

If you’re new to Expo, check out the [Expo tutorial](https://docs.expo.dev/tutorial/introduction/).

Expo is maintained by [Expo (the company)](https://expo.dev/about). Building apps with Expo is free, and you can submit them to the Google and Apple app stores without restrictions. Expo additionally provides opt-in paid cloud services.

## Other frameworks

There are other up-and-coming frameworks that are working towards our full stack React vision:

- [TanStack Start (Beta)](https://tanstack.com/start/): TanStack Start is a full-stack React framework powered by TanStack Router. It provides a full-document SSR, streaming, server functions, bundling, and more using tools like Nitro and Vite.
- [RedwoodSDK](https://rwsdk.com/): Redwood is a full stack React framework with lots of pre-installed packages and configuration that makes it easy to build full-stack web applications.

##### Deep Dive

#### Which features make up the React team’s full-stack architecture vision?

Next.js’s App Router bundler fully implements the official [React Server Components specification](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md). This lets you mix build-time, server-only, and interactive components in a single React tree.

For example, you can write a server-only React component as an `async` function that reads from a database or from a file. Then you can pass data down from it to your interactive components:

$

```
// This component runs *only* on the server (or during the build).async function Talks({ confId }) {  // 1. You're on the server, so you can talk to your data layer. API endpoint not required.  const talks = await db.Talks.findAll({ confId });  // 2. Add any amount of rendering logic. It won't make your JavaScript bundle larger.  const videos = talks.map(talk => talk.video);  // 3. Pass the data down to the components that will run in the browser.  return <SearchableVideoList videos={videos} />;}
```

/$

Next.js’s App Router also integrates [data fetching with Suspense](https://react.dev/blog/2022/03/29/react-v18#suspense-in-data-frameworks). This lets you specify a loading state (like a skeleton placeholder) for different parts of your user interface directly in your React tree:

$

```
<Suspense fallback={<TalksLoading />}>  <Talks confId={conf.id} /></Suspense>
```

/$

Server Components and Suspense are React features rather than Next.js features. However, adopting them at the framework level requires buy-in and non-trivial implementation work. At the moment, the Next.js App Router is the most complete implementation. The React team is working with bundler developers to make these features easier to implement in the next generation of frameworks.

## Start From Scratch

If your app has constraints not well-served by existing frameworks, you prefer to build your own framework, or you just want to learn the basics of a React app, there are other options available for starting a React project from scratch.

Starting from scratch gives you more flexibility, but does require that you make choices on which tools to use for routing, data fetching, and other common usage patterns.  It’s a lot like building your own framework, instead of using a framework that already exists. The [frameworks we recommend](#full-stack-frameworks) have built-in solutions for these problems.

If you want to build your own solutions, see our guide to [build a React app from Scratch](https://react.dev/learn/build-a-react-app-from-scratch) for instructions on how to set up a new React project starting with a build tool like [Vite](https://vite.dev/), [Parcel](https://parceljs.org/), or [RSbuild](https://rsbuild.dev/).

---

*If you’re a framework author interested in being included on this page,please let us know.*

[PreviousInstallation](https://react.dev/learn/installation)[NextBuild a React App from Scratch](https://react.dev/learn/build-a-react-app-from-scratch)

---

# Describing the UI

[Learn React](https://react.dev/learn)

# Describing the UI

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable *components.* From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you’ll learn to create, customize, and conditionally display React components.

### In this chapter

- [How to write your first React component](https://react.dev/learn/your-first-component)
- [When and how to create multi-component files](https://react.dev/learn/importing-and-exporting-components)
- [How to add markup to JavaScript with JSX](https://react.dev/learn/writing-markup-with-jsx)
- [How to use curly braces with JSX to access JavaScript functionality from your components](https://react.dev/learn/javascript-in-jsx-with-curly-braces)
- [How to configure components with props](https://react.dev/learn/passing-props-to-a-component)
- [How to conditionally render components](https://react.dev/learn/conditional-rendering)
- [How to render multiple components at a time](https://react.dev/learn/rendering-lists)
- [How to avoid confusing bugs by keeping components pure](https://react.dev/learn/keeping-components-pure)
- [Why understanding your UI as trees is useful](https://react.dev/learn/understanding-your-ui-as-a-tree)

## Your first component

React applications are built from isolated pieces of UI called *components*. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button, or as large as an entire page. Here is a `Gallery` component rendering three `Profile` components:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)function Profile() { return ( <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" /> );}
export default function Gallery() { return ( <section> <h1>Amazing scientists</h1> <Profile /> <Profile /> <Profile /> </section> );}
/$

## Ready to learn this topic?

Read **Your First Component** to learn how to declare and use React components.

[Read More](https://react.dev/learn/your-first-component)

---

## Importing and exporting components

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can *export* a component into its own file, and then *import* that component from another file:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Profile from './Profile.js';

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

## Ready to learn this topic?

Read **Importing and Exporting Components** to learn how to split components into their own files.

[Read More](https://react.dev/learn/importing-and-exporting-components)

---

## Writing markup with JSX

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If we paste existing HTML markup into a React component, it won’t always work:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  return (
    // This doesn't quite work!
    <h1>Hedy Lamarr's Todos</h1>
    <img
      src="https://i.imgur.com/yXOvdOSs.jpg"
      alt="Hedy Lamarr"
      class="photo"
    >
    <ul>
      <li>Invent new traffic lights
      <li>Rehearse a movie scene
      <li>Improve spectrum technology
    </ul>
```

/$

If you have existing HTML like this, you can fix it using a [converter](https://transform.tools/html-to-jsx):

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  return (
    <>
      <h1>Hedy Lamarr's Todos</h1>
      <img
        src="https://i.imgur.com/yXOvdOSs.jpg"
        alt="Hedy Lamarr"
        className="photo"
      />
      <ul>
        <li>Invent new traffic lights</li>
        <li>Rehearse a movie scene</li>
        <li>Improve spectrum technology</li>
      </ul>
    </>
  );
}
```

/$

## Ready to learn this topic?

Read **Writing Markup with JSX** to learn how to write valid JSX.

[Read More](https://react.dev/learn/writing-markup-with-jsx)

---

## JavaScript in JSX with curly braces

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to “open a window” to JavaScript:

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

## Ready to learn this topic?

Read **JavaScript in JSX with Curly Braces** to learn how to access JavaScript data from JSX.

[Read More](https://react.dev/learn/javascript-in-jsx-with-curly-braces)

---

## Passing props to a component

React components use *props* to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { getImageUrl } from './utils.js'

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

function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}
```

/$

## Ready to learn this topic?

Read **Passing Props to a Component** to learn how to pass and read props.

[Read More](https://react.dev/learn/passing-props-to-a-component)

---

## Conditional rendering

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like `if` statements, `&&`, and `? :` operators.

In this example, the JavaScript `&&` operator is used to conditionally render a checkmark:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Item({ name, isPacked }) {
  return (
    <li className="item">
      {name} {isPacked && '✅'}
    </li>
  );
}

export default function PackingList() {
  return (
    <section>
      <h1>Sally Ride's Packing List</h1>
      <ul>
        <Item
          isPacked={true}
          name="Space suit"
        />
        <Item
          isPacked={true}
          name="Helmet with a golden leaf"
        />
        <Item
          isPacked={false}
          name="Photo of Tam"
        />
      </ul>
    </section>
  );
}
```

/$

## Ready to learn this topic?

Read **Conditional Rendering** to learn the different ways to render content conditionally.

[Read More](https://react.dev/learn/conditional-rendering)

---

## Rendering lists

You will often want to display multiple similar components from a collection of data. You can use JavaScript’s `filter()` and `map()` with React to filter and transform your array of data into an array of components.

For each array item, you will need to specify a `key`. Usually, you will want to use an ID from the database as a `key`. Keys let React keep track of each item’s place in the list even if the list changes.

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

/$

## Ready to learn this topic?

Read **Rendering Lists** to learn how to render a list of components, and how to choose a key.

[Read More](https://react.dev/learn/rendering-lists)

---

## Keeping components pure

Some JavaScript functions are *pure.* A pure function:

- **Minds its own business.** It does not change any objects or variables that existed before it was called.
- **Same inputs, same output.** Given the same inputs, a pure function should always return the same result.

By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. Here is an example of an impure component:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
let guest = 0;

function Cup() {
  // Bad: changing a preexisting variable!
  guest = guest + 1;
  return <h2>Tea cup for guest #{guest}</h2>;
}

export default function TeaSet() {
  return (
    <>
      <Cup />
      <Cup />
      <Cup />
    </>
  );
}
```

/$

You can make this component pure by passing a prop instead of modifying a preexisting variable:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Cup({ guest }) {
  return <h2>Tea cup for guest #{guest}</h2>;
}

export default function TeaSet() {
  return (
    <>
      <Cup guest={1} />
      <Cup guest={2} />
      <Cup guest={3} />
    </>
  );
}
```

/$

## Ready to learn this topic?

Read **Keeping Components Pure** to learn how to write components as pure, predictable functions.

[Read More](https://react.dev/learn/keeping-components-pure)

---

## Your UI as a tree

React uses trees to model the relationships between components and modules.

A React render tree is a representation of the parent and child relationship between components.

 ![A tree graph with five nodes, with each node representing a component. The root node is located at the top the tree graph and is labelled 'Root Component'. It has two arrows extending down to two nodes labelled 'Component A' and 'Component C'. Each of the arrows is labelled with 'renders'. 'Component A' has a single 'renders' arrow to a node labelled 'Component B'. 'Component C' has a single 'renders' arrow to a node labelled 'Component D'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fgeneric_render_tree.dark.png&w=1080&q=75)![A tree graph with five nodes, with each node representing a component. The root node is located at the top the tree graph and is labelled 'Root Component'. It has two arrows extending down to two nodes labelled 'Component A' and 'Component C'. Each of the arrows is labelled with 'renders'. 'Component A' has a single 'renders' arrow to a node labelled 'Component B'. 'Component C' has a single 'renders' arrow to a node labelled 'Component D'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fgeneric_render_tree.png&w=1080&q=75)

An example React render tree.

Components near the top of the tree, near the root component, are considered top-level components. Components with no child components are leaf components. This categorization of components is useful for understanding data flow and rendering performance.

Modelling the relationship between JavaScript modules is another useful way to understand your app. We refer to it as a module dependency tree.

 ![A tree graph with five nodes. Each node represents a JavaScript module. The top-most node is labelled 'RootModule.js'. It has three arrows extending to the nodes: 'ModuleA.js', 'ModuleB.js', and 'ModuleC.js'. Each arrow is labelled as 'imports'. 'ModuleC.js' node has a single 'imports' arrow that points to a node labelled 'ModuleD.js'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fgeneric_dependency_tree.dark.png&w=1080&q=75)![A tree graph with five nodes. Each node represents a JavaScript module. The top-most node is labelled 'RootModule.js'. It has three arrows extending to the nodes: 'ModuleA.js', 'ModuleB.js', and 'ModuleC.js'. Each arrow is labelled as 'imports'. 'ModuleC.js' node has a single 'imports' arrow that points to a node labelled 'ModuleD.js'.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fgeneric_dependency_tree.png&w=1080&q=75)

An example module dependency tree.

A dependency tree is often used by build tools to bundle all the relevant JavaScript code for the client to download and render. A large bundle size regresses user experience for React apps. Understanding the module dependency tree is helpful to debug such issues.

## Ready to learn this topic?

Read **Your UI as a Tree** to learn how to create a render and module dependency trees for a React app and how they’re useful mental models for improving user experience and performance.

[Read More](https://react.dev/learn/understanding-your-ui-as-a-tree)

---

## What’s next?

Head over to [Your First Component](https://react.dev/learn/your-first-component) to start reading this chapter page by page!

Or, if you’re already familiar with these topics, why not read about [Adding Interactivity](https://react.dev/learn/adding-interactivity)?

[NextYour First Component](https://react.dev/learn/your-first-component)

---

# Editor Setup

[Learn React](https://react.dev/learn)[Setup](https://react.dev/learn/setup)

# Editor Setup

A properly configured editor can make code clearer to read and faster to write. It can even help you catch bugs as you write them! If this is your first time setting up an editor or you’re looking to tune up your current editor, we have a few recommendations.

### You will learn

- What the most popular editors are
- How to format your code automatically

## Your editor

[VS Code](https://code.visualstudio.com/) is one of the most popular editors in use today. It has a large marketplace of extensions and integrates well with popular services like GitHub. Most of the features listed below can be added to VS Code as extensions as well, making it highly configurable!

Other popular text editors used in the React community include:

- [WebStorm](https://www.jetbrains.com/webstorm/) is an integrated development environment designed specifically for JavaScript.
- [Sublime Text](https://www.sublimetext.com/) has support for JSX and TypeScript, [syntax highlighting](https://stackoverflow.com/a/70960574/458193) and autocomplete built in.
- [Vim](https://www.vim.org/) is a highly configurable text editor built to make creating and changing any kind of text very efficient. It is included as “vi” with most UNIX systems and with Apple OS X.

## Recommended text editor features

Some editors come with these features built in, but others might require adding an extension. Check to see what support your editor of choice provides to be sure!

### Linting

Code linters find problems in your code as you write, helping you fix them early. [ESLint](https://eslint.org/) is a popular, open source linter for JavaScript.

- [Install ESLint with the recommended configuration for React](https://www.npmjs.com/package/eslint-config-react-app) (be sure you have [Node installed!](https://nodejs.org/en/download/current/))
- [Integrate ESLint in VSCode with the official extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

**Make sure that you’ve enabled all theeslint-plugin-react-hooksrules for your project.** They are essential and catch the most severe bugs early. The recommended [eslint-config-react-app](https://www.npmjs.com/package/eslint-config-react-app) preset already includes them.

### Formatting

The last thing you want to do when sharing your code with another contributor is get into a discussion about [tabs vs spaces](https://www.google.com/search?q=tabs+vs+spaces)! Fortunately, [Prettier](https://prettier.io/) will clean up your code by reformatting it to conform to preset, configurable rules. Run Prettier, and all your tabs will be converted to spaces—and your indentation, quotes, etc will also all be changed to conform to the configuration. In the ideal setup, Prettier will run when you save your file, quickly making these edits for you.

You can install the [Prettier extension in VSCode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) by following these steps:

1. Launch VS Code
2. Use Quick Open (press Ctrl/Cmd+P)
3. Paste in `ext install esbenp.prettier-vscode`
4. Press Enter

#### Formatting on save

Ideally, you should format your code on every save. VS Code has settings for this!

1. In VS Code, press `CTRL/CMD + SHIFT + P`.
2. Type “settings”
3. Hit Enter
4. In the search bar, type “format on save”
5. Be sure the “format on save” option is ticked!

> If your ESLint preset has formatting rules, they may conflict with Prettier. We recommend disabling all formatting rules in your ESLint preset using [eslint-config-prettier](https://github.com/prettier/eslint-config-prettier) so that ESLint is *only* used for catching logical mistakes. If you want to enforce that files are formatted before a pull request is merged, use [prettier --check](https://prettier.io/docs/en/cli.html#--check) for your continuous integration.

[PreviousSetup](https://react.dev/learn/setup)[NextUsing TypeScript](https://react.dev/learn/typescript)

---

# Escape Hatches

[Learn React](https://react.dev/learn)

# Escape Hatches

Advanced

Some of your components may need to control and synchronize with systems outside of React. For example, you might need to focus an input using the browser API, play and pause a video player implemented without React, or connect and listen to messages from a remote server. In this chapter, you’ll learn the escape hatches that let you “step outside” React and connect to external systems. Most of your application logic and data flow should not rely on these features.

### In this chapter

- [How to “remember” information without re-rendering](https://react.dev/learn/referencing-values-with-refs)
- [How to access DOM elements managed by React](https://react.dev/learn/manipulating-the-dom-with-refs)
- [How to synchronize components with external systems](https://react.dev/learn/synchronizing-with-effects)
- [How to remove unnecessary Effects from your components](https://react.dev/learn/you-might-not-need-an-effect)
- [How an Effect’s lifecycle is different from a component’s](https://react.dev/learn/lifecycle-of-reactive-effects)
- [How to prevent some values from re-triggering Effects](https://react.dev/learn/separating-events-from-effects)
- [How to make your Effect re-run less often](https://react.dev/learn/removing-effect-dependencies)
- [How to share logic between components](https://react.dev/learn/reusing-logic-with-custom-hooks)

## Referencing values with refs

When you want a component to “remember” some information, but you don’t want that information to [trigger new renders](https://react.dev/learn/render-and-commit), you can use a *ref*:

 $

```
const ref = useRef(0);
```

/$

Like state, refs are retained by React between re-renders. However, setting state re-renders a component. Changing a ref does not! You can access the current value of that ref through the `ref.current` property.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { useRef } from 'react';
export default function Counter() { let ref = useRef(0);
 function handleClick() { ref.current = ref.current + 1; alert('You clicked ' + ref.current + ' times!'); }
 return ( <button onClick={handleClick}>      Click me! </button> );}
/$

A ref is like a secret pocket of your component that React doesn’t track. For example, you can use refs to store [timeout IDs](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout#return_value), [DOM elements](https://developer.mozilla.org/en-US/docs/Web/API/Element), and other objects that don’t impact the component’s rendering output.

## Ready to learn this topic?

Read **Referencing Values with Refs** to learn how to use refs to remember information.

[Read More](https://react.dev/learn/referencing-values-with-refs)

---

## Manipulating the DOM with refs

React automatically updates the DOM to match your render output, so your components won’t often need to manipulate it. However, sometimes you might need access to the DOM elements managed by React—for example, to focus a node, scroll to it, or measure its size and position. There is no built-in way to do those things in React, so you will need a ref to the DOM node. For example, clicking the button will focus the input using a ref:

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

## Ready to learn this topic?

Read **Manipulating the DOM with Refs** to learn how to access DOM elements managed by React.

[Read More](https://react.dev/learn/manipulating-the-dom-with-refs)

---

## Synchronizing with Effects

Some components need to synchronize with external systems. For example, you might want to control a non-React component based on the React state, set up a server connection, or send an analytics log when a component appears on the screen. Unlike event handlers, which let you handle particular events, *Effects* let you run some code after rendering. Use them to synchronize your component with a system outside of React.

Press Play/Pause a few times and see how the video player stays synchronized to the `isPlaying` prop value:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  }, [isPlaying]);

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <>
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

/$

Many Effects also “clean up” after themselves. For example, an Effect that sets up a connection to a chat server should return a *cleanup function* that tells React how to disconnect your component from that server:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom() {
  useEffect(() => {
    const connection = createConnection();
    connection.connect();
    return () => connection.disconnect();
  }, []);
  return <h1>Welcome to the chat!</h1>;
}
```

/$

In development, React will immediately run and clean up your Effect one extra time. This is why you see `"✅ Connecting..."` printed twice. This ensures that you don’t forget to implement the cleanup function.

## Ready to learn this topic?

Read **Synchronizing with Effects** to learn how to synchronize components with external systems.

[Read More](https://react.dev/learn/synchronizing-with-effects)

---

## You Might Not Need An Effect

Effects are an escape hatch from the React paradigm. They let you “step outside” of React and synchronize your components with some external system. If there is no external system involved (for example, if you want to update a component’s state when some props or state change), you shouldn’t need an Effect. Removing unnecessary Effects will make your code easier to follow, faster to run, and less error-prone.

There are two common cases in which you don’t need Effects:

- **You don’t need Effects to transform data for rendering.**
- **You don’t need Effects to handle user events.**

For example, you don’t need an Effect to adjust some state based on other state:

 $

```
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // 🔴 Avoid: redundant state and unnecessary Effect  const [fullName, setFullName] = useState('');  useEffect(() => {    setFullName(firstName + ' ' + lastName);  }, [firstName, lastName]);  // ...}
```

/$

Instead, calculate as much as you can while rendering:

 $

```
function Form() {  const [firstName, setFirstName] = useState('Taylor');  const [lastName, setLastName] = useState('Swift');  // ✅ Good: calculated during rendering  const fullName = firstName + ' ' + lastName;  // ...}
```

/$

However, you *do* need Effects to synchronize with external systems.

## Ready to learn this topic?

Read **You Might Not Need an Effect** to learn how to remove unnecessary Effects.

[Read More](https://react.dev/learn/you-might-not-need-an-effect)

---

## Lifecycle of reactive effects

Effects have a different lifecycle from components. Components may mount, update, or unmount. An Effect can only do two things: to start synchronizing something, and later to stop synchronizing it. This cycle can happen multiple times if your Effect depends on props and state that change over time.

This Effect depends on the value of the `roomId` prop. Props are *reactive values,* which means they can change on a re-render. Notice that the Effect *re-synchronizes* (and re-connects to the server) if `roomId` changes:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return <h1>Welcome to the {roomId} room!</h1>;
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

/$

React provides a linter rule to check that you’ve specified your Effect’s dependencies correctly. If you forget to specify `roomId` in the list of dependencies in the above example, the linter will find that bug automatically.

## Ready to learn this topic?

Read **Lifecycle of Reactive Events** to learn how an Effect’s lifecycle is different from a component’s.

[Read More](https://react.dev/learn/lifecycle-of-reactive-effects)

---

## Separating events from Effects

Event handlers only re-run when you perform the same interaction again. Unlike event handlers, Effects re-synchronize if any of the values they read, like props or state, are different than during last render. Sometimes, you want a mix of both behaviors: an Effect that re-runs in response to some values but not others.

All code inside Effects is *reactive.* It will run again if some reactive value it reads has changed due to a re-render. For example, this Effect will re-connect to the chat if either `roomId` or `theme` have changed:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { createConnection, sendMessage } from './chat.js';
import { showNotification } from './notifications.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      showNotification('Connected!', theme);
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, theme]);

  return <h1>Welcome to the {roomId} room!</h1>
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  const [isDark, setIsDark] = useState(false);
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <label>
        <input
          type="checkbox"
          checked={isDark}
          onChange={e => setIsDark(e.target.checked)}
        />
        Use dark theme
      </label>
      <hr />
      <ChatRoom
        roomId={roomId}
        theme={isDark ? 'dark' : 'light'}
      />
    </>
  );
}
```

/$

This is not ideal. You want to re-connect to the chat only if the `roomId` has changed. Switching the `theme` shouldn’t re-connect to the chat! Move the code reading `theme` out of your Effect into an *Effect Event*:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { useEffectEvent } from 'react';
import { createConnection, sendMessage } from './chat.js';
import { showNotification } from './notifications.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return <h1>Welcome to the {roomId} room!</h1>
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  const [isDark, setIsDark] = useState(false);
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <label>
        <input
          type="checkbox"
          checked={isDark}
          onChange={e => setIsDark(e.target.checked)}
        />
        Use dark theme
      </label>
      <hr />
      <ChatRoom
        roomId={roomId}
        theme={isDark ? 'dark' : 'light'}
      />
    </>
  );
}
```

/$

Code inside Effect Events isn’t reactive, so changing the `theme` no longer makes your Effect re-connect.

## Ready to learn this topic?

Read **Separating Events from Effects** to learn how to prevent some values from re-triggering Effects.

[Read More](https://react.dev/learn/separating-events-from-effects)

---

## Removing Effect dependencies

When you write an Effect, the linter will verify that you’ve included every reactive value (like props and state) that the Effect reads in the list of your Effect’s dependencies. This ensures that your Effect remains synchronized with the latest props and state of your component. Unnecessary dependencies may cause your Effect to run too often, or even create an infinite loop. The way you remove them depends on the case.

For example, this Effect depends on the `options` object which gets re-created every time you edit the input:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');

  const options = {
    serverUrl: serverUrl,
    roomId: roomId
  };

  useEffect(() => {
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [options]);

  return (
    <>
      <h1>Welcome to the {roomId} room!</h1>
      <input value={message} onChange={e => setMessage(e.target.value)} />
    </>
  );
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

/$

You don’t want the chat to re-connect every time you start typing a message in that chat. To fix this problem, move creation of the `options` object inside the Effect so that the Effect only depends on the `roomId` string:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const options = {
      serverUrl: serverUrl,
      roomId: roomId
    };
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return (
    <>
      <h1>Welcome to the {roomId} room!</h1>
      <input value={message} onChange={e => setMessage(e.target.value)} />
    </>
  );
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

/$

Notice that you didn’t start by editing the dependency list to remove the `options` dependency. That would be wrong. Instead, you changed the surrounding code so that the dependency became *unnecessary.* Think of the dependency list as a list of all the reactive values used by your Effect’s code. You don’t intentionally choose what to put on that list. The list describes your code. To change the dependency list, change the code.

## Ready to learn this topic?

Read **Removing Effect Dependencies** to learn how to make your Effect re-run less often.

[Read More](https://react.dev/learn/removing-effect-dependencies)

---

## Reusing logic with custom Hooks

React comes with built-in Hooks like `useState`, `useContext`, and `useEffect`. Sometimes, you’ll wish that there was a Hook for some more specific purpose: for example, to fetch data, to keep track of whether the user is online, or to connect to a chat room. To do this, you can create your own Hooks for your application’s needs.

In this example, the `usePointerPosition` custom Hook tracks the cursor position, while `useDelayedValue` custom Hook returns a value that’s “lagging behind” the value you passed by a certain number of milliseconds. Move the cursor over the sandbox preview area to see a moving trail of dots following the cursor:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { usePointerPosition } from './usePointerPosition.js';
import { useDelayedValue } from './useDelayedValue.js';

export default function Canvas() {
  const pos1 = usePointerPosition();
  const pos2 = useDelayedValue(pos1, 100);
  const pos3 = useDelayedValue(pos2, 200);
  const pos4 = useDelayedValue(pos3, 100);
  const pos5 = useDelayedValue(pos4, 50);
  return (
    <>
      <Dot position={pos1} opacity={1} />
      <Dot position={pos2} opacity={0.8} />
      <Dot position={pos3} opacity={0.6} />
      <Dot position={pos4} opacity={0.4} />
      <Dot position={pos5} opacity={0.2} />
    </>
  );
}

function Dot({ position, opacity }) {
  return (
    <div style={{
      position: 'absolute',
      backgroundColor: 'pink',
      borderRadius: '50%',
      opacity,
      transform: `translate(${position.x}px, ${position.y}px)`,
      pointerEvents: 'none',
      left: -20,
      top: -20,
      width: 40,
      height: 40,
    }} />
  );
}
```

/$

You can create custom Hooks, compose them together, pass data between them, and reuse them between components. As your app grows, you will write fewer Effects by hand because you’ll be able to reuse custom Hooks you already wrote. There are also many excellent custom Hooks maintained by the React community.

## Ready to learn this topic?

Read **Reusing Logic with Custom Hooks** to learn how to share logic between components.

[Read More](https://react.dev/learn/reusing-logic-with-custom-hooks)

---

## What’s next?

Head over to [Referencing Values with Refs](https://react.dev/learn/referencing-values-with-refs) to start reading this chapter page by page!

[PreviousScaling Up with Reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context)[NextReferencing Values with Refs](https://react.dev/learn/referencing-values-with-refs)
