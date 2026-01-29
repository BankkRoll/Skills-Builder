# Keeping Components Pure

# Keeping Components Pure

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Keeping Components Pure

Some JavaScript functions are *pure.* Pure functions only perform a calculation and nothing more. By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. To get these benefits, though, there are a few rules you must follow.

### You will learn

- What purity is and how it helps you avoid bugs
- How to keep components pure by keeping changes out of the render phase
- How to use Strict Mode to find mistakes in your components

## Purity: Components as formulas

In computer science (and especially the world of functional programming), [a pure function](https://wikipedia.org/wiki/Pure_function) is a function with the following characteristics:

- **It minds its own business.** It does not change any objects or variables that existed before it was called.
- **Same inputs, same output.** Given the same inputs, a pure function should always return the same result.

You might already be familiar with one example of pure functions: formulas in math.

Consider this math formula: y = 2x.

If x = 2 then y = 4. Always.

If x = 3 then y = 6. Always.

If x = 3, y won’t sometimes be 9 or –1 or 2.5 depending on the time of day or the state of the stock market.

If y = 2x and x = 3, y will *always* be 6.

If we made this into a JavaScript function, it would look like this:

 $

```
function double(number) {  return 2 * number;}
```

/$

In the above example, `double` is a **pure function.** If you pass it `3`, it will return `6`. Always.

React is designed around this concept. **React assumes that every component you write is a pure function.** This means that React components you write must always return the same JSX given the same inputs:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Recipe({ drinkers }) {
  return (
    <ol>
      <li>Boil {drinkers} cups of water.</li>
      <li>Add {drinkers} spoons of tea and {0.5 * drinkers} spoons of spice.</li>
      <li>Add {0.5 * drinkers} cups of milk to boil and sugar to taste.</li>
    </ol>
  );
}

export default function App() {
  return (
    <section>
      <h1>Spiced Chai Recipe</h1>
      <h2>For two</h2>
      <Recipe drinkers={2} />
      <h2>For a gathering</h2>
      <Recipe drinkers={4} />
    </section>
  );
}
```

/$

When you pass `drinkers={2}` to `Recipe`, it will return JSX containing `2 cups of water`. Always.

If you pass `drinkers={4}`, it will return JSX containing `4 cups of water`. Always.

Just like a math formula.

You could think of your components as recipes: if you follow them and don’t introduce new ingredients during the cooking process, you will get the same dish every time. That “dish” is the JSX that the component serves to React to [render.](https://react.dev/learn/render-and-commit)

 ![A tea recipe for x people: take x cups of water, add x spoons of tea and 0.5x spoons of spices, and 0.5x cups of milk](https://react.dev/images/docs/illustrations/i_puritea-recipe.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

## Side Effects: (un)intended consequences

React’s rendering process must always be pure. Components should only *return* their JSX, and not *change* any objects or variables that existed before rendering—that would make them impure!

Here is a component that breaks this rule:

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

This component is reading and writing a `guest` variable declared outside of it. This means that **calling this component multiple times will produce different JSX!** And what’s more, if *other* components read `guest`, they will produce different JSX, too, depending on when they were rendered! That’s not predictable.

Going back to our formula y = 2x, now even if x = 2, we cannot trust that y = 4. Our tests could fail, our users would be baffled, planes would fall out of the sky—you can see how this would lead to confusing bugs!

You can fix this component by [passingguestas a prop instead](https://react.dev/learn/passing-props-to-a-component):

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

Now your component is pure, as the JSX it returns only depends on the `guest` prop.

In general, you should not expect your components to be rendered in any particular order. It doesn’t matter if you call y = 2x before or after y = 5x: both formulas will resolve independently of each other. In the same way, each component should only “think for itself”, and not attempt to coordinate with or depend upon others during rendering. Rendering is like a school exam: each component should calculate JSX on their own!

##### Deep Dive

#### Detecting impure calculations with StrictMode

Although you might not have used them all yet, in React there are three kinds of inputs that you can read while rendering: [props](https://react.dev/learn/passing-props-to-a-component), [state](https://react.dev/learn/state-a-components-memory), and [context.](https://react.dev/learn/passing-data-deeply-with-context) You should always treat these inputs as read-only.

When you want to *change* something in response to user input, you should [set state](https://react.dev/learn/state-a-components-memory) instead of writing to a variable. You should never change preexisting variables or objects while your component is rendering.

React offers a “Strict Mode” in which it calls each component’s function twice during development. **By calling the component functions twice, Strict Mode helps find components that break these rules.**

Notice how the original example displayed “Guest #2”, “Guest #4”, and “Guest #6” instead of “Guest #1”, “Guest #2”, and “Guest #3”. The original function was impure, so calling it twice broke it. But the fixed pure version works even if the function is called twice every time. **Pure functions only calculate, so calling them twice won’t change anything**—just like calling `double(2)` twice doesn’t change what’s returned, and solving y = 2x twice doesn’t change what y is. Same inputs, same outputs. Always.

Strict Mode has no effect in production, so it won’t slow down the app for your users. To opt into Strict Mode, you can wrap your root component into `<React.StrictMode>`. Some frameworks do this by default.

### Local mutation: Your component’s little secret

In the above example, the problem was that the component changed a *preexisting* variable while rendering. This is often called a **“mutation”** to make it sound a bit scarier. Pure functions don’t mutate variables outside of the function’s scope or objects that were created before the call—that makes them impure!

However, **it’s completely fine to change variables and objects that you’vejustcreated while rendering.** In this example, you create an `[]` array, assign it to a `cups` variable, and then `push` a dozen cups into it:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
function Cup({ guest }) {
  return <h2>Tea cup for guest #{guest}</h2>;
}

export default function TeaGathering() {
  const cups = [];
  for (let i = 1; i <= 12; i++) {
    cups.push(<Cup key={i} guest={i} />);
  }
  return cups;
}
```

/$

If the `cups` variable or the `[]` array were created outside the `TeaGathering` function, this would be a huge problem! You would be changing a *preexisting* object by pushing items into that array.

However, it’s fine because you’ve created them *during the same render*, inside `TeaGathering`. No code outside of `TeaGathering` will ever know that this happened. This is called **“local mutation”**—it’s like your component’s little secret.

## Where youcancause side effects

While functional programming relies heavily on purity, at some point, somewhere, *something* has to change. That’s kind of the point of programming! These changes—updating the screen, starting an animation, changing the data—are called **side effects.** They’re things that happen *“on the side”*, not during rendering.

In React, **side effects usually belong insideevent handlers.** Event handlers are functions that React runs when you perform some action—for example, when you click a button. Even though event handlers are defined *inside* your component, they don’t run *during* rendering! **So event handlers don’t need to be pure.**

If you’ve exhausted all other options and can’t find the right event handler for your side effect, you can still attach it to your returned JSX with a [useEffect](https://react.dev/reference/react/useEffect) call in your component. This tells React to execute it later, after rendering, when side effects are allowed. **However, this approach should be your last resort.**

When possible, try to express your logic with rendering alone. You’ll be surprised how far this can take you!

##### Deep Dive

#### Why does React care about purity?

Writing pure functions takes some habit and discipline. But it also unlocks marvelous opportunities:

- Your components could run in a different environment—for example, on the server! Since they return the same result for the same inputs, one component can serve many user requests.
- You can improve performance by [skipping rendering](https://react.dev/reference/react/memo) components whose inputs have not changed. This is safe because pure functions always return the same results, so they are safe to cache.
- If some data changes in the middle of rendering a deep component tree, React can restart rendering without wasting time to finish the outdated render. Purity makes it safe to stop calculating at any time.

Every new React feature we’re building takes advantage of purity. From data fetching to animations to performance, keeping components pure unlocks the power of the React paradigm.

## Recap

- A component must be pure, meaning:
  - **It minds its own business.** It should not change any objects or variables that existed before rendering.
  - **Same inputs, same output.** Given the same inputs, a component should always return the same JSX.
- Rendering can happen at any time, so components should not depend on each others’ rendering sequence.
- You should not mutate any of the inputs that your components use for rendering. That includes props, state, and context. To update the screen, [“set” state](https://react.dev/learn/state-a-components-memory) instead of mutating preexisting objects.
- Strive to express your component’s logic in the JSX you return. When you need to “change things”, you’ll usually want to do it in an event handler. As a last resort, you can `useEffect`.
- Writing pure functions takes a bit of practice, but it unlocks the power of React’s paradigm.

## Try out some challenges

#### Challenge1of3:Fix a broken clock

This component tries to set the `<h1>`’s CSS class to `"night"` during the time from midnight to six hours in the morning, and `"day"` at all other times. However, it doesn’t work. Can you fix this component?

You can verify whether your solution works by temporarily changing the computer’s timezone. When the current time is between midnight and six in the morning, the clock should have inverted colors!

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Clock({ time }) {
  const hours = time.getHours();
  if (hours >= 0 && hours <= 6) {
    document.getElementById('time').className = 'night';
  } else {
    document.getElementById('time').className = 'day';
  }
  return (
    <h1 id="time">
      {time.toLocaleTimeString()}
    </h1>
  );
}
```

/$[PreviousRendering Lists](https://react.dev/learn/rendering-lists)[NextYour UI as a Tree](https://react.dev/learn/understanding-your-ui-as-a-tree)
