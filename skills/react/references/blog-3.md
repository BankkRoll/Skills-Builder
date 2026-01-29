# Introducing react.dev and more

# Introducing react.dev

[Blog](https://react.dev/blog)

# Introducing react.dev

March 16, 2023 by [Dan Abramov](https://bsky.app/profile/danabra.mov) and [Rachel Nabors](https://twitter.com/rachelnabors)

---

Today we are thrilled to launch [react.dev](https://react.dev), the new home for React and its documentation. In this post, we would like to give you a tour of the new site.

---

## tl;dr

- The new React site ([react.dev](https://react.dev)) teaches modern React with function components and Hooks.
- We’ve included diagrams, illustrations, challenges, and over 600 new interactive examples.
- The previous React documentation site has now moved to [legacy.reactjs.org](https://legacy.reactjs.org).

## New site, new domain, new homepage

First, a little bit of housekeeping.

To celebrate the launch of the new docs and, more importantly, to clearly separate the old and the new content, we’ve moved to the shorter [react.dev](https://react.dev) domain. The old [reactjs.org](https://reactjs.org) domain will now redirect here.

The old React docs are now archived at [legacy.reactjs.org](https://legacy.reactjs.org). All existing links to the old content will automatically redirect there to avoid “breaking the web”, but the legacy site will not get many more updates.

Believe it or not, React will soon be ten years old. In JavaScript years, it’s like a whole century! We’ve [refreshed the React homepage](https://react.dev) to reflect why we think React is a great way to create user interfaces today, and updated the getting started guides to more prominently mention modern React-based frameworks.

If you haven’t seen the new homepage yet, check it out!

## Going all-in on modern React with Hooks

When we released React Hooks in 2018, the Hooks docs assumed the reader is familiar with class components. This helped the community adopt Hooks very swiftly, but after a while the old docs failed to serve the new readers. New readers had to learn React twice: once with class components and then once again with Hooks.

**The new docs teach React with Hooks from the beginning.** The docs are divided in two main sections:

- **Learn React** is a self-paced course that teaches React from scratch.
- **API Reference** provides the details and usage examples for every React API.

Let’s have a closer look at what you can find in each section.

### Note

There are still a few rare class component use cases that do not yet have a Hook-based equivalent. Class components remain supported, and are documented in the [Legacy API](https://react.dev/reference/react/legacy) section of the new site.

## Quick start

The Learn section begins with the [Quick Start](https://react.dev/learn) page. It is a short introductory tour of React. It introduces the syntax for concepts like components, props, and state, but doesn’t go into much detail on how to use them.

If you like to learn by doing, we recommend checking out the [Tic-Tac-Toe Tutorial](https://react.dev/learn/tutorial-tic-tac-toe) next. It walks you through building a little game with React, while teaching the skills you’ll use every day. Here’s what you’ll build:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board({ xIsNext, squares, onPlay }) {
  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    onPlay(nextSquares);
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = 'Go to move #' + move;
    } else {
      description = 'Go to game start';
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <ol>{moves}</ol>
      </div>
    </div>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
```

/$

We’d also like to highlight [Thinking in React](https://react.dev/learn/thinking-in-react)—that’s the tutorial that made React “click” for many of us. **We’ve updated both of these classic tutorials to use function components and Hooks,** so they’re as good as new.

### Note

The example above is a *sandbox*. We’ve added a lot of sandboxes—over 600!—everywhere throughout the site. You can edit any sandbox, or press “Fork” in the upper right corner to open it in a separate tab. Sandboxes let you quickly play with the React APIs, explore your ideas, and check your understanding.

## Learn React step by step

We’d like everyone in the world to have an equal opportunity to learn React for free on their own.

This is why the Learn section is organized like a self-paced course split into chapters. The first two chapters describe the fundamentals of React. If you’re new to React, or want to refresh it in your memory, start here:

- **Describing the UI** teaches how to display information with components.
- **Adding Interactivity** teaches how to update the screen in response to user input.

The next two chapters are more advanced, and will give you a deeper insight into the trickier parts:

- **Managing State** teaches how to organize your logic as your app grows in complexity.
- **Escape Hatches** teaches how you can “step outside” React, and when it makes most sense to do so.

Every chapter consists of several related pages. Most of these pages teach a specific skill or a technique—for example, [Writing Markup with JSX](https://react.dev/learn/writing-markup-with-jsx), [Updating Objects in State](https://react.dev/learn/updating-objects-in-state), or [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components). Some of the pages focus on explaining an idea—like [Render and Commit](https://react.dev/learn/render-and-commit), or [State as a Snapshot](https://react.dev/learn/state-as-a-snapshot). And there are a few, like [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), that share our suggestions based on what we’ve learned over these years.

You don’t have to read these chapters as a sequence. Who has the time for this?! But you could. Pages in the Learn section only rely on concepts introduced by the earlier pages. If you want to read it like a book, go for it!

### Check your understanding with challenges

Most pages in the Learn section end with a few challenges to check your understanding. For example, here are a few challenges from the page about [Conditional Rendering](https://react.dev/learn/conditional-rendering#challenges).

You don’t have to solve them right now! Unless you *really* want to.

#### Challenge1of2:Show an icon for incomplete items with? :

Use the conditional operator (`cond ? a : b`) to render a ❌ if `isPacked` isn’t `true`.

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

Notice the “Show solution” button in the left bottom corner. It’s handy if you want to check yourself!

### Build an intuition with diagrams and illustrations

When we couldn’t figure out how to explain something with code and words alone, we’ve added diagrams that help provide some intuition. For example, here is one of the diagrams from [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state):

 ![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a React component labeled 'div' with a single child labeled 'section', which has a single child labeled 'Counter' containing a state bubble labeled 'count' with value 3. The middle section has the same 'div' parent, but the child components have now been deleted, indicated by a yellow 'proof' image. The third section has the same 'div' parent again, now with a new child labeled 'div', highlighted in yellow, also with a new child labeled 'Counter' containing a state bubble labeled 'count' with value 0, all highlighted in yellow.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpreserving_state_diff_same_pt1.dark.png&w=1920&q=75)![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a React component labeled 'div' with a single child labeled 'section', which has a single child labeled 'Counter' containing a state bubble labeled 'count' with value 3. The middle section has the same 'div' parent, but the child components have now been deleted, indicated by a yellow 'proof' image. The third section has the same 'div' parent again, now with a new child labeled 'div', highlighted in yellow, also with a new child labeled 'Counter' containing a state bubble labeled 'count' with value 0, all highlighted in yellow.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fpreserving_state_diff_same_pt1.png&w=1920&q=75)

When `section` changes to `div`, the `section` is deleted and the new `div` is added

You’ll also see some illustrations throughout the docs—here’s one of the [browser painting the screen](https://react.dev/learn/render-and-commit#epilogue-browser-paint):

 ![A browser painting 'still life with card element'.](https://react.dev/images/docs/illustrations/i_browser-paint.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

We’ve confirmed with the browser vendors that this depiction is 100% scientifically accurate.

## A new, detailed API Reference

In the [API Reference](https://react.dev/reference/react), every React API now has a dedicated page. This includes all kinds of APIs:

- Built-in Hooks like [useState](https://react.dev/reference/react/useState).
- Built-in components like [<Suspense>](https://react.dev/reference/react/Suspense).
- Built-in browser components like [<input>](https://react.dev/reference/react-dom/components/input).
- Framework-oriented APIs like [renderToPipeableStream](https://react.dev/reference/react-dom/server/renderToReadableStream).
- Other React APIs like [memo](https://react.dev/reference/react/memo).

You’ll notice that every API page is split into at least two segments: *Reference* and *Usage*.

[Reference](https://react.dev/reference/react/useState#reference) describes the formal API signature by listing its arguments and return values. It’s concise, but it can feel a bit abstract if you’re not familiar with that API. It describes what an API does, but not how to use it.

[Usage](https://react.dev/reference/react/useState#usage) shows why and how you would use this API in practice, like a colleague or a friend might explain. It shows the **canonical scenarios for how each API was meant to be used by the React team.** We’ve added color-coded snippets, examples of using different APIs together, and recipes that you can copy and paste from:

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

Some API pages also include [Troubleshooting](https://react.dev/reference/react/useEffect#troubleshooting) (for common problems) and [Alternatives](https://react.dev/reference/react-dom/findDOMNode#alternatives) (for deprecated APIs).

We hope that this approach will make the API reference useful not only as a way to look up an argument, but as a way to see all the different things you can do with any given API—and how it connects to the other ones.

## What’s next?

That’s a wrap for our little tour! Have a look around the new website, see what you like or don’t like, and keep the feedback coming in our [issue tracker](https://github.com/reactjs/react.dev/issues).

We acknowledge this project has taken a long time to ship. We wanted to maintain a high quality bar that the React community deserves. While writing these docs and creating all of the examples, we found mistakes in some of our own explanations, bugs in React, and even gaps in the React design that we are now working to address. We hope that the new documentation will help us hold React itself to a higher bar in the future.

We’ve heard many of your requests to expand the content and functionality of the website, for example:

- Providing a TypeScript version for all examples;
- Creating the updated performance, testing, and accessibility guides;
- Documenting React Server Components independently from the frameworks that support them;
- Working with our international community to get the new docs translated;
- Adding missing features to the new website (for example, RSS for this blog).

Now that [react.dev](https://react.dev/) is out, we will be able to shift our focus from “catching up” with the third-party React educational resources to adding new information and further improving our new website.

We think there’s never been a better time to learn React.

## Who worked on this?

On the React team, [Rachel Nabors](https://twitter.com/rachelnabors/) led the project (and provided the illustrations), and [Dan Abramov](https://bsky.app/profile/danabra.mov) designed the curriculum. They co-authored most of the content together as well.

Of course, no project this large happens in isolation. We have a lot of people to thank!

[Sylwia Vargas](https://twitter.com/SylwiaVargas) overhauled our examples to go beyond “foo/bar/baz” and kittens, and feature scientists, artists and cities from around the world. [Maggie Appleton](https://twitter.com/Mappletons) turned our doodles into a clear diagram system.

Thanks to [David McCabe](https://twitter.com/mcc_abe), [Sophie Alpert](https://twitter.com/sophiebits), [Rick Hanlon](https://twitter.com/rickhanlonii), [Andrew Clark](https://twitter.com/acdlite), and [Matt Carroll](https://twitter.com/mattcarrollcode) for additional writing contributions. We’d also like to thank [Natalia Tepluhina](https://twitter.com/n_tepluhina) and [Sebastian Markbåge](https://twitter.com/sebmarkbage) for their ideas and feedback.

Thanks to [Dan Lebowitz](https://twitter.com/lebo) for the site design and [Razvan Gradinar](https://dribbble.com/GradinarRazvan) for the sandbox design.

On the development front, thanks to [Jared Palmer](https://twitter.com/jaredpalmer) for prototype development. Thanks to [Dane Grant](https://twitter.com/danecando) and [Dustin Goodman](https://twitter.com/dustinsgoodman) from [ThisDotLabs](https://www.thisdot.co/) for their support on UI development. Thanks to [Ives van Hoorne](https://twitter.com/CompuIves), [Alex Moldovan](https://twitter.com/alexnmoldovan), [Jasper De Moor](https://twitter.com/JasperDeMoor), and [Danilo Woznica](https://twitter.com/danilowoz) from [CodeSandbox](https://codesandbox.io/) for their work with sandbox integration. Thanks to [Rick Hanlon](https://twitter.com/rickhanlonii) for spot development and design work, finessing our colors and finer details. Thanks to [Harish Kumar](https://www.strek.in/) and [Luna Ruan](https://twitter.com/lunaruan) for adding new features to the site and helping maintain it.

Huge thanks to the folks who volunteered their time to participate in the alpha and beta testing program. Your enthusiasm and invaluable feedback helped us shape these docs. A special shout out to our beta tester, [Debbie O’Brien](https://twitter.com/debs_obrien), who gave a talk about her experience using the React docs at React Conf 2021.

Finally, thanks to the React community for being the inspiration behind this effort. You are the reason we do this, and we hope that the new docs will help you use React to build any user interface that you want.

[PreviousReact Labs: What We've Been Working On – March 2023](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023)[NextReact Labs: What We've Been Working On – June 2022](https://react.dev/blog/2022/06/15/react-labs-what-we-have-been-working-on-june-2022)

---

# React Labs: What We've Been Working On

[Blog](https://react.dev/blog)

# React Labs: What We've Been Working On – March 2023

March 22, 2023 by [Joseph Savona](https://twitter.com/en_JS), [Josh Story](https://twitter.com/joshcstory), [Lauren Tan](https://twitter.com/potetotes), [Mengdi Chen](https://twitter.com/mengdi_en), [Samuel Susla](https://twitter.com/SamuelSusla), [Sathya Gunasekaran](https://twitter.com/_gsathya), [Sebastian Markbåge](https://twitter.com/sebmarkbage), and [Andrew Clark](https://twitter.com/acdlite)

---

In React Labs posts, we write about projects in active research and development. We’ve made significant progress on them since our [last update](https://react.dev/blog/2022/06/15/react-labs-what-we-have-been-working-on-june-2022), and we’d like to share what we learned.

---

## React Server Components

React Server Components (or RSC) is a new application architecture designed by the React team.

We’ve first shared our research on RSC in an [introductory talk](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components) and an [RFC](https://github.com/reactjs/rfcs/pull/188). To recap them, we are introducing a new kind of component—Server Components—that run ahead of time and are excluded from your JavaScript bundle. Server Components can run during the build, letting you read from the filesystem or fetch static content. They can also run on the server, letting you access your data layer without having to build an API. You can pass data by props from Server Components to the interactive Client Components in the browser.

RSC combines the simple “request/response” mental model of server-centric Multi-Page Apps with the seamless interactivity of client-centric Single-Page Apps, giving you the best of both worlds.

Since our last update, we have merged the [React Server Components RFC](https://github.com/reactjs/rfcs/blob/main/text/0188-server-components.md) to ratify the proposal. We resolved outstanding issues with the [React Server Module Conventions](https://github.com/reactjs/rfcs/blob/main/text/0227-server-module-conventions.md) proposal, and reached consensus with our partners to go with the `"use client"` convention. These documents also act as specification for what an RSC-compatible implementation should support.

The biggest change is that we introduced [async/await](https://github.com/reactjs/rfcs/pull/229) as the primary way to do data fetching from Server Components. We also plan to support data loading from the client by introducing a new Hook called `use` that unwraps Promises. Although we can’t support `async / await` in arbitrary components in client-only apps, we plan to add support for it when you structure your client-only app similar to how RSC apps are structured.

Now that we have data fetching pretty well sorted, we’re exploring the other direction: sending data from the client to the server, so that you can execute database mutations and implement forms. We’re doing this by letting you pass Server Action functions across the server/client boundary, which the client can then call, providing seamless RPC. Server Actions also give you progressively enhanced forms before JavaScript loads.

React Server Components has shipped in [Next.js App Router](https://react.dev/learn/creating-a-react-app#nextjs-app-router). This showcases a deep integration of a router that really buys into RSC as a primitive, but it’s not the only way to build a RSC-compatible router and framework. There’s a clear separation for features provided by the RSC spec and implementation. React Server Components is meant as a spec for components that work across compatible React frameworks.

We generally recommend using an existing framework, but if you need to build your own custom framework, it is possible. Building your own RSC-compatible framework is not as easy as we’d like it to be, mainly due to the deep bundler integration needed. The current generation of bundlers are great for use on the client, but they weren’t designed with first-class support for splitting a single module graph between the server and the client. This is why we’re now partnering directly with bundler developers to get the primitives for RSC built-in.

## Asset Loading

[Suspense](https://react.dev/reference/react/Suspense) lets you specify what to display on the screen while the data or code for your components is still being loaded. This lets your users progressively see more content while the page is loading as well as during the router navigations that load more data and code. However, from the user’s perspective, data loading and rendering do not tell the whole story when considering whether new content is ready. By default, browsers load stylesheets, fonts, and images independently, which can lead to UI jumps and consecutive layout shifts.

We’re working to fully integrate Suspense with the loading lifecycle of stylesheets, fonts, and images, so that React takes them into account to determine whether the content is ready to be displayed. Without any change to the way you author your React components, updates will behave in a more coherent and pleasing manner. As an optimization, we will also provide a manual way to preload assets like fonts directly from components.

We are currently implementing these features and will have more to share soon.

## Document Metadata

Different pages and screens in your app may have different metadata like the `<title>` tag, description, and other `<meta>` tags specific to this screen. From the maintenance perspective, it’s more scalable to keep this information close to the React component for that page or screen. However, the HTML tags for this metadata need to be in the document `<head>` which is typically rendered in a component at the very root of your app.

Today, people solve this problem with one of the two techniques.

One technique is to render a special third-party component that moves `<title>`, `<meta>`, and other tags inside it into the document `<head>`. This works for major browsers but there are many clients which do not run client-side JavaScript, such as Open Graph parsers, and so this technique is not universally suitable.

Another technique is to server-render the page in two parts. First, the main content is rendered and all such tags are collected. Then, the `<head>` is rendered with these tags. Finally, the `<head>` and the main content are sent to the browser. This approach works, but it prevents you from taking advantage of the [React 18’s Streaming Server Renderer](https://react.dev/reference/react-dom/server/renderToReadableStream) because you’d have to wait for all content to render before sending the `<head>`.

This is why we’re adding built-in support for rendering `<title>`, `<meta>`, and metadata `<link>` tags anywhere in your component tree out of the box. It would work the same way in all environments, including fully client-side code, SSR, and in the future, RSC. We will share more details about this soon.

## React Optimizing Compiler

Since our previous update we’ve been actively iterating on the design of [React Forget](https://react.dev/blog/2022/06/15/react-labs-what-we-have-been-working-on-june-2022#react-compiler), an optimizing compiler for React. We’ve previously talked about it as an “auto-memoizing compiler”, and that is true in some sense. But building the compiler has helped us understand React’s programming model even more deeply. A better way to understand React Forget is as an automatic *reactivity* compiler.

The core idea of React is that developers define their UI as a function of the current state. You work with plain JavaScript values — numbers, strings, arrays, objects — and use standard JavaScript idioms — if/else, for, etc — to describe your component logic. The mental model is that React will re-render whenever the application state changes. We believe this simple mental model and keeping close to JavaScript semantics is an important principle in React’s programming model.

The catch is that React can sometimes be *too* reactive: it can re-render too much. For example, in JavaScript we don’t have cheap ways to compare if two objects or arrays are equivalent (having the same keys and values), so creating a new object or array on each render may cause React to do more work than it strictly needs to. This means developers have to explicitly memoize components so as to not over-react to changes.

Our goal with React Forget is to ensure that React apps have just the right amount of reactivity by default: that apps re-render only when state values *meaningfully* change. From an implementation perspective this means automatically memoizing, but we believe that the reactivity framing is a better way to understand React and Forget. One way to think about this is that React currently re-renders when object identity changes. With Forget, React re-renders when the semantic value changes — but without incurring the runtime cost of deep comparisons.

In terms of concrete progress, since our last update we have substantially iterated on the design of the compiler to align with this automatic reactivity approach and to incorporate feedback from using the compiler internally. After some significant refactors to the compiler starting late last year, we’ve now begun using the compiler in production in limited areas at Meta. We plan to open-source it once we’ve proved it in production.

Finally, a lot of people have expressed interest in how the compiler works. We’re looking forward to sharing a lot more details when we prove the compiler and open-source it. But there are a few bits we can share now:

The core of the compiler is almost completely decoupled from Babel, and the core compiler API is (roughly) old AST in, new AST out (while retaining source location data). Under the hood we use a custom code representation and transformation pipeline in order to do low-level semantic analysis. However, the primary public interface to the compiler will be via Babel and other build system plugins. For ease of testing we currently have a Babel plugin which is a very thin wrapper that calls the compiler to generate a new version of each function and swap it in.

As we refactored the compiler over the last few months, we wanted to focus on refining the core compilation model to ensure we could handle complexities such as conditionals, loops, reassignment, and mutation. However, JavaScript has a lot of ways to express each of those features: if/else, ternaries, for, for-in, for-of, etc. Trying to support the full language up-front would have delayed the point where we could validate the core model. Instead, we started with a small but representative subset of the language: let/const, if/else, for loops, objects, arrays, primitives, function calls, and a few other features. As we gained confidence in the core model and refined our internal abstractions, we expanded the supported language subset. We’re also explicit about syntax we don’t yet support, logging diagnostics and skipping compilation for unsupported input. We have utilities to try the compiler on Meta’s codebases and see what unsupported features are most common so we can prioritize those next. We’ll continue incrementally expanding towards supporting the whole language.

Making plain JavaScript in React components reactive requires a compiler with a deep understanding of semantics so that it can understand exactly what the code is doing. By taking this approach, we’re creating a system for reactivity within JavaScript that lets you write product code of any complexity with the full expressivity of the language, instead of being limited to a domain specific language.

## Offscreen Rendering

Offscreen rendering is an upcoming capability in React for rendering screens in the background without additional performance overhead. You can think of it as a version of the [content-visibilityCSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility) that works not only for DOM elements but React components, too. During our research, we’ve discovered a variety of use cases:

- A router can prerender screens in the background so that when a user navigates to them, they’re instantly available.
- A tab switching component can preserve the state of hidden tabs, so the user can switch between them without losing their progress.
- A virtualized list component can prerender additional rows above and below the visible window.
- When opening a modal or popup, the rest of the app can be put into “background” mode so that events and updates are disabled for everything except the modal.

Most React developers will not interact with React’s offscreen APIs directly. Instead, offscreen rendering will be integrated into things like routers and UI libraries, and then developers who use those libraries will automatically benefit without additional work.

The idea is that you should be able to render any React tree offscreen without changing the way you write your components. When a component is rendered offscreen, it does not actually *mount* until the component becomes visible — its effects are not fired. For example, if a component uses `useEffect` to log analytics when it appears for the first time, prerendering won’t mess up the accuracy of those analytics. Similarly, when a component goes offscreen, its effects are unmounted, too. A key feature of offscreen rendering is that you can toggle the visibility of a component without losing its state.

Since our last update, we’ve tested an experimental version of prerendering internally at Meta in our React Native apps on Android and iOS, with positive performance results. We’ve also improved how offscreen rendering works with Suspense — suspending inside an offscreen tree will not trigger Suspense fallbacks. Our remaining work involves finalizing the primitives that are exposed to library developers. We expect to publish an RFC later this year, alongside an experimental API for testing and feedback.

## Transition Tracing

The Transition Tracing API lets you detect when [React Transitions](https://react.dev/reference/react/useTransition) become slower and investigate why they may be slow. Following our last update, we have completed the initial design of the API and published an [RFC](https://github.com/reactjs/rfcs/pull/238). The basic capabilities have also been implemented. The project is currently on hold. We welcome feedback on the RFC and look forward to resuming its development to provide a better performance measurement tool for React. This will be particularly useful with routers built on top of React Transitions, like the [Next.js App Router](https://react.dev/learn/creating-a-react-app#nextjs-app-router).

---

In addition to this update, our team has made recent guest appearances on community podcasts and livestreams to speak more on our work and answer questions.

- [Dan Abramov](https://bsky.app/profile/danabra.mov) and [Joe Savona](https://twitter.com/en_JS) were interviewed by [Kent C. Dodds on his YouTube channel](https://www.youtube.com/watch?v=h7tur48JSaw), where they discussed concerns around React Server Components.
- [Dan Abramov](https://bsky.app/profile/danabra.mov) and [Joe Savona](https://twitter.com/en_JS) were guests on the [JSParty podcast](https://jsparty.fm/267) and shared their thoughts about the future of React.

Thanks to [Andrew Clark](https://twitter.com/acdlite), [Dan Abramov](https://bsky.app/profile/danabra.mov), [Dave McCabe](https://twitter.com/mcc_abe), [Luna Wei](https://twitter.com/lunaleaps), [Matt Carroll](https://twitter.com/mattcarrollcode), [Sean Keegan](https://twitter.com/DevRelSean), [Sebastian Silbermann](https://twitter.com/sebsilbermann), [Seth Webster](https://twitter.com/sethwebster), and [Sophie Alpert](https://twitter.com/sophiebits) for reviewing this post.

Thanks for reading, and see you in the next update!

[PreviousReact Canaries: Enabling Incremental Feature Rollout Outside Meta](https://react.dev/blog/2023/05/03/react-canaries)[NextIntroducing react.dev](https://react.dev/blog/2023/03/16/introducing-react-dev)
