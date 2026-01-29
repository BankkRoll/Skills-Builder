# useMemo and more

# useMemo

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useMemo

`useMemo` is a React Hook that lets you cache the result of a calculation between re-renders.

$

```
const cachedValue = useMemo(calculateValue, dependencies)
```

/$

### Note

[React Compiler](https://react.dev/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useMemo` calls. You can use the compiler to handle memoization automatically.

- [Reference](#reference)
  - [useMemo(calculateValue, dependencies)](#usememo)
- [Usage](#usage)
  - [Skipping expensive recalculations](#skipping-expensive-recalculations)
  - [Skipping re-rendering of components](#skipping-re-rendering-of-components)
  - [Preventing an Effect from firing too often](#preventing-an-effect-from-firing-too-often)
  - [Memoizing a dependency of another Hook](#memoizing-a-dependency-of-another-hook)
  - [Memoizing a function](#memoizing-a-function)
- [Troubleshooting](#troubleshooting)
  - [My calculation runs twice on every re-render](#my-calculation-runs-twice-on-every-re-render)
  - [MyuseMemocall is supposed to return an object, but returns undefined](#my-usememo-call-is-supposed-to-return-an-object-but-returns-undefined)
  - [Every time my component renders, the calculation inuseMemore-runs](#every-time-my-component-renders-the-calculation-in-usememo-re-runs)
  - [I need to calluseMemofor each list item in a loop, but it’s not allowed](#i-need-to-call-usememo-for-each-list-item-in-a-loop-but-its-not-allowed)

---

## Reference

### useMemo(calculateValue, dependencies)

Call `useMemo` at the top level of your component to cache a calculation between re-renders:

 $

```
import { useMemo } from 'react';function TodoList({ todos, tab }) {  const visibleTodos = useMemo(    () => filterTodos(todos, tab),    [todos, tab]  );  // ...}
```

/$

[See more examples below.](#usage)

#### Parameters

- `calculateValue`: The function calculating the value that you want to cache. It should be pure, should take no arguments, and should return a value of any type. React will call your function during the initial render. On next renders, React will return the same value again if the `dependencies` have not changed since the last render. Otherwise, it will call `calculateValue`, return its result, and store it so it can be reused later.
- `dependencies`: The list of all reactive values referenced inside of the `calculateValue` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](https://react.dev/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison.

#### Returns

On the initial render, `useMemo` returns the result of calling `calculateValue` with no arguments.

During next renders, it will either return an already stored value from the last render (if the dependencies haven’t changed), or call `calculateValue` again, and return the result that `calculateValue` has returned.

#### Caveats

- `useMemo` is a Hook, so you can only call it **at the top level of your component** or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.
- In Strict Mode, React will **call your calculation function twice** in order to [help you find accidental impurities.](#my-calculation-runs-twice-on-every-re-render) This is development-only behavior and does not affect production. If your calculation function is pure (as it should be), this should not affect your logic. The result from one of the calls will be ignored.
- React **will not throw away the cached value unless there is a specific reason to do that.** For example, in development, React throws away the cache when you edit the file of your component. Both in development and in production, React will throw away the cache if your component suspends during the initial mount. In the future, React may add more features that take advantage of throwing away the cache—for example, if React adds built-in support for virtualized lists in the future, it would make sense to throw away the cache for items that scroll out of the virtualized table viewport. This should be fine if you rely on `useMemo` solely as a performance optimization. Otherwise, a [state variable](https://react.dev/reference/react/useState#avoiding-recreating-the-initial-state) or a [ref](https://react.dev/reference/react/useRef#avoiding-recreating-the-ref-contents) may be more appropriate.

### Note

Caching return values like this is also known as [memoization,](https://en.wikipedia.org/wiki/Memoization) which is why this Hook is called `useMemo`.

---

## Usage

### Skipping expensive recalculations

To cache a calculation between re-renders, wrap it in a `useMemo` call at the top level of your component:

 $

```
import { useMemo } from 'react';function TodoList({ todos, tab, theme }) {  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  // ...}
```

/$

You need to pass two things to `useMemo`:

1. A calculation function that takes no arguments, like `() =>`, and returns what you wanted to calculate.
2. A list of dependencies including every value within your component that’s used inside your calculation.

On the initial render, the value you’ll get from `useMemo` will be the result of calling your calculation.

On every subsequent render, React will compare the dependencies with the dependencies you passed during the last render. If none of the dependencies have changed (compared with [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)), `useMemo` will return the value you already calculated before. Otherwise, React will re-run your calculation and return the new value.

In other words, `useMemo` caches a calculation result between re-renders until its dependencies change.

**Let’s walk through an example to see when this is useful.**

By default, React will re-run the entire body of your component every time that it re-renders. For example, if this `TodoList` updates its state or receives new props from its parent, the `filterTodos` function will re-run:

 $

```
function TodoList({ todos, tab, theme }) {  const visibleTodos = filterTodos(todos, tab);  // ...}
```

/$

Usually, this isn’t a problem because most calculations are very fast. However, if you’re filtering or transforming a large array, or doing some expensive computation, you might want to skip doing it again if data hasn’t changed. If both `todos` and `tab` are the same as they were during the last render, wrapping the calculation in `useMemo` like earlier lets you reuse `visibleTodos` you’ve already calculated before.

This type of caching is called *memoization.*

### Note

**You should only rely onuseMemoas a performance optimization.** If your code doesn’t work without it, find the underlying problem and fix it first. Then you may add `useMemo` to improve performance.

##### Deep Dive

#### How to tell if a calculation is expensive?

In general, unless you’re creating or looping over thousands of objects, it’s probably not expensive. If you want to get more confidence, you can add a console log to measure the time spent in a piece of code:

$

```
console.time('filter array');const visibleTodos = filterTodos(todos, tab);console.timeEnd('filter array');
```

/$

Perform the interaction you’re measuring (for example, typing into the input). You will then see logs like `filter array: 0.15ms` in your console. If the overall logged time adds up to a significant amount (say, `1ms` or more), it might make sense to memoize that calculation. As an experiment, you can then wrap the calculation in `useMemo` to verify whether the total logged time has decreased for that interaction or not:

$

```
console.time('filter array');const visibleTodos = useMemo(() => {  return filterTodos(todos, tab); // Skipped if todos and tab haven't changed}, [todos, tab]);console.timeEnd('filter array');
```

/$

`useMemo` won’t make the *first* render faster. It only helps you skip unnecessary work on updates.

Keep in mind that your machine is probably faster than your users’ so it’s a good idea to test the performance with an artificial slowdown. For example, Chrome offers a [CPU Throttling](https://developer.chrome.com/blog/new-in-devtools-61/#throttling) option for this.

Also note that measuring performance in development will not give you the most accurate results. (For example, when [Strict Mode](https://react.dev/reference/react/StrictMode) is on, you will see each component render twice rather than once.) To get the most accurate timings, build your app for production and test it on a device like your users have.

##### Deep Dive

#### Should you add useMemo everywhere?

If your app is like this site, and most interactions are coarse (like replacing a page or an entire section), memoization is usually unnecessary. On the other hand, if your app is more like a drawing editor, and most interactions are granular (like moving shapes), then you might find memoization very helpful.

Optimizing with `useMemo`  is only valuable in a few cases:

- The calculation you’re putting in `useMemo` is noticeably slow, and its dependencies rarely change.
- You pass it as a prop to a component wrapped in [memo.](https://react.dev/reference/react/memo) You want to skip re-rendering if the value hasn’t changed. Memoization lets your component re-render only when dependencies aren’t the same.
- The value you’re passing is later used as a dependency of some Hook. For example, maybe another `useMemo` calculation value depends on it. Or maybe you are depending on this value from [useEffect.](https://react.dev/reference/react/useEffect)

There is no benefit to wrapping a calculation in `useMemo` in other cases. There is no significant harm to doing that either, so some teams choose to not think about individual cases, and memoize as much as possible. The downside of this approach is that code becomes less readable. Also, not all memoization is effective: a single value that’s “always new” is enough to break memoization for an entire component.

**In practice, you can make a lot of memoization unnecessary by following a few principles:**

1. When a component visually wraps other components, let it [accept JSX as children.](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) This way, when the wrapper component updates its own state, React knows that its children don’t need to re-render.
2. Prefer local state and don’t [lift state up](https://react.dev/learn/sharing-state-between-components) any further than necessary. For example, don’t keep transient state like forms and whether an item is hovered at the top of your tree or in a global state library.
3. Keep your [rendering logic pure.](https://react.dev/learn/keeping-components-pure) If re-rendering a component causes a problem or produces some noticeable visual artifact, it’s a bug in your component! Fix the bug instead of adding memoization.
4. Avoid [unnecessary Effects that update state.](https://react.dev/learn/you-might-not-need-an-effect) Most performance problems in React apps are caused by chains of updates originating from Effects that cause your components to render over and over.
5. Try to [remove unnecessary dependencies from your Effects.](https://react.dev/learn/removing-effect-dependencies) For example, instead of memoization, it’s often simpler to move some object or a function inside an Effect or outside the component.

If a specific interaction still feels laggy, [use the React Developer Tools profiler](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html) to see which components would benefit the most from memoization, and add memoization where needed. These principles make your components easier to debug and understand, so it’s good to follow them in any case. In the long term, we’re researching [doing granular memoization automatically](https://www.youtube.com/watch?v=lGEMwh32soc) to solve this once and for all.

#### The difference between useMemo and calculating a value directly

#### Example1of2:Skipping recalculation withuseMemo

In this example, the `filterTodos` implementation is **artificially slowed down** so that you can see what happens when some JavaScript function you’re calling during rendering is genuinely slow. Try switching the tabs and toggling the theme.

Switching the tabs feels slow because it forces the slowed down `filterTodos` to re-execute. That’s expected because the `tab` has changed, and so the entire calculation *needs* to re-run. (If you’re curious why it runs twice, it’s explained [here.](#my-calculation-runs-twice-on-every-re-render))

Toggle the theme. **Thanks touseMemo, it’s fast despite the artificial slowdown!** The slow `filterTodos` call was skipped because both `todos` and `tab` (which you pass as dependencies to `useMemo`) haven’t changed since the last render.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useMemo } from 'react';
import { filterTodos } from './utils.js'

export default function TodoList({ todos, theme, tab }) {
  const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
  );
  return (
    <div className={theme}>
      <p><b>Note: <code>filterTodos</code> is artificially slowed down!</b></p>
      <ul>
        {visibleTodos.map(todo => (
          <li key={todo.id}>
            {todo.completed ?
              <s>{todo.text}</s> :
              todo.text
            }
          </li>
        ))}
      </ul>
    </div>
  );
}
```

/$

---

### Skipping re-rendering of components

In some cases, `useMemo` can also help you optimize performance of re-rendering child components. To illustrate this, let’s say this `TodoList` component passes the `visibleTodos` as a prop to the child `List` component:

 $

```
export default function TodoList({ todos, tab, theme }) {  // ...  return (    <div className={theme}>      <List items={visibleTodos} />    </div>  );}
```

/$

You’ve noticed that toggling the `theme` prop freezes the app for a moment, but if you remove `<List />` from your JSX, it feels fast. This tells you that it’s worth trying to optimize the `List` component.

**By default, when a component re-renders, React re-renders all of its children recursively.** This is why, when `TodoList` re-renders with a different `theme`, the `List` component *also* re-renders. This is fine for components that don’t require much calculation to re-render. But if you’ve verified that a re-render is slow, you can tell `List` to skip re-rendering when its props are the same as on last render by wrapping it in [memo:](https://react.dev/reference/react/memo)

 $

```
import { memo } from 'react';const List = memo(function List({ items }) {  // ...});
```

/$

**With this change,Listwill skip re-rendering if all of its props are thesameas on the last render.** This is where caching the calculation becomes important! Imagine that you calculated `visibleTodos` without `useMemo`:

 $

```
export default function TodoList({ todos, tab, theme }) {  // Every time the theme changes, this will be a different array...  const visibleTodos = filterTodos(todos, tab);  return (    <div className={theme}>      {/* ... so List's props will never be the same, and it will re-render every time */}      <List items={visibleTodos} />    </div>  );}
```

/$

**In the above example, thefilterTodosfunction always creates adifferentarray,** similar to how the `{}` object literal always creates a new object. Normally, this wouldn’t be a problem, but it means that `List` props will never be the same, and your [memo](https://react.dev/reference/react/memo) optimization won’t work. This is where `useMemo` comes in handy:

 $

```
export default function TodoList({ todos, tab, theme }) {  // Tell React to cache your calculation between re-renders...  const visibleTodos = useMemo(    () => filterTodos(todos, tab),    [todos, tab] // ...so as long as these dependencies don't change...  );  return (    <div className={theme}>      {/* ...List will receive the same props and can skip re-rendering */}      <List items={visibleTodos} />    </div>  );}
```

/$

**By wrapping thevisibleTodoscalculation inuseMemo, you ensure that it has thesamevalue between the re-renders** (until dependencies change). You don’t *have to* wrap a calculation in `useMemo` unless you do it for some specific reason. In this example, the reason is that you pass it to a component wrapped in [memo,](https://react.dev/reference/react/memo) and this lets it skip re-rendering. There are a few other reasons to add `useMemo` which are described further on this page.

##### Deep Dive

#### Memoizing individual JSX nodes

Instead of wrapping `List` in [memo](https://react.dev/reference/react/memo), you could wrap the `<List />` JSX node itself in `useMemo`:

$

```
export default function TodoList({ todos, tab, theme }) {  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  const children = useMemo(() => <List items={visibleTodos} />, [visibleTodos]);  return (    <div className={theme}>      {children}    </div>  );}
```

/$

The behavior would be the same. If the `visibleTodos` haven’t changed, `List` won’t be re-rendered.

A JSX node like `<List items={visibleTodos} />` is an object like `{ type: List, props: { items: visibleTodos } }`. Creating this object is very cheap, but React doesn’t know whether its contents is the same as last time or not. This is why by default, React will re-render the `List` component.

However, if React sees the same exact JSX as during the previous render, it won’t try to re-render your component. This is because JSX nodes are [immutable.](https://en.wikipedia.org/wiki/Immutable_object) A JSX node object could not have changed over time, so React knows it’s safe to skip a re-render. However, for this to work, the node has to *actually be the same object*, not merely look the same in code. This is what `useMemo` does in this example.

Manually wrapping JSX nodes into `useMemo` is not convenient. For example, you can’t do this conditionally. This is usually why you would wrap components with [memo](https://react.dev/reference/react/memo) instead of wrapping JSX nodes.

#### The difference between skipping re-renders and always re-rendering

#### Example1of2:Skipping re-rendering withuseMemoandmemo

In this example, the `List` component is **artificially slowed down** so that you can see what happens when a React component you’re rendering is genuinely slow. Try switching the tabs and toggling the theme.

Switching the tabs feels slow because it forces the slowed down `List` to re-render. That’s expected because the `tab` has changed, and so you need to reflect the user’s new choice on the screen.

Next, try toggling the theme. **Thanks touseMemotogether withmemo, it’s fast despite the artificial slowdown!** The `List` skipped re-rendering because the `visibleTodos` array has not changed since the last render. The `visibleTodos` array has not changed because both `todos` and `tab` (which you pass as dependencies to `useMemo`) haven’t changed since the last render.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useMemo } from 'react';
import List from './List.js';
import { filterTodos } from './utils.js'

export default function TodoList({ todos, theme, tab }) {
  const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
  );
  return (
    <div className={theme}>
      <p><b>Note: <code>List</code> is artificially slowed down!</b></p>
      <List items={visibleTodos} />
    </div>
  );
}
```

/$

---

### Preventing an Effect from firing too often

Sometimes, you might want to use a value inside an [Effect:](https://react.dev/learn/synchronizing-with-effects)

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  const options = {    serverUrl: 'https://localhost:1234',    roomId: roomId  }  useEffect(() => {    const connection = createConnection(options);    connection.connect();    // ...
```

/$

This creates a problem. [Every reactive value must be declared as a dependency of your Effect.](https://react.dev/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency) However, if you declare `options` as a dependency, it will cause your Effect to constantly reconnect to the chat room:

 $

```
useEffect(() => {    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [options]); // 🔴 Problem: This dependency changes on every render  // ...
```

/$

To solve this, you can wrap the object you need to call from an Effect in `useMemo`:

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  const options = useMemo(() => {    return {      serverUrl: 'https://localhost:1234',      roomId: roomId    };  }, [roomId]); // ✅ Only changes when roomId changes  useEffect(() => {    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [options]); // ✅ Only changes when options changes  // ...
```

/$

This ensures that the `options` object is the same between re-renders if `useMemo` returns the cached object.

However, since `useMemo` is performance optimization, not a semantic guarantee, React may throw away the cached value if [there is a specific reason to do that](#caveats). This will also cause the effect to re-fire, **so it’s even better to remove the need for a function dependency** by moving your object *inside* the Effect:

 $

```
function ChatRoom({ roomId }) {  const [message, setMessage] = useState('');  useEffect(() => {    const options = { // ✅ No need for useMemo or object dependencies!      serverUrl: 'https://localhost:1234',      roomId: roomId    }    const connection = createConnection(options);    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ Only changes when roomId changes  // ...
```

/$

Now your code is simpler and doesn’t need `useMemo`. [Learn more about removing Effect dependencies.](https://react.dev/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)

### Memoizing a dependency of another Hook

Suppose you have a calculation that depends on an object created directly in the component body:

 $

```
function Dropdown({ allItems, text }) {  const searchOptions = { matchMode: 'whole-word', text };  const visibleItems = useMemo(() => {    return searchItems(allItems, searchOptions);  }, [allItems, searchOptions]); // 🚩 Caution: Dependency on an object created in the component body  // ...
```

/$

Depending on an object like this defeats the point of memoization. When a component re-renders, all of the code directly inside the component body runs again. **The lines of code creating thesearchOptionsobject will also run on every re-render.** Since `searchOptions` is a dependency of your `useMemo` call, and it’s different every time, React knows the dependencies are different, and recalculate `searchItems` every time.

To fix this, you could memoize the `searchOptions` object *itself* before passing it as a dependency:

 $

```
function Dropdown({ allItems, text }) {  const searchOptions = useMemo(() => {    return { matchMode: 'whole-word', text };  }, [text]); // ✅ Only changes when text changes  const visibleItems = useMemo(() => {    return searchItems(allItems, searchOptions);  }, [allItems, searchOptions]); // ✅ Only changes when allItems or searchOptions changes  // ...
```

/$

In the example above, if the `text` did not change, the `searchOptions` object also won’t change. However, an even better fix is to move the `searchOptions` object declaration *inside* of the `useMemo` calculation function:

 $

```
function Dropdown({ allItems, text }) {  const visibleItems = useMemo(() => {    const searchOptions = { matchMode: 'whole-word', text };    return searchItems(allItems, searchOptions);  }, [allItems, text]); // ✅ Only changes when allItems or text changes  // ...
```

/$

Now your calculation depends on `text` directly (which is a string and can’t “accidentally” become different).

---

### Memoizing a function

Suppose the `Form` component is wrapped in [memo.](https://react.dev/reference/react/memo) You want to pass a function to it as a prop:

 $

```
export default function ProductPage({ productId, referrer }) {  function handleSubmit(orderDetails) {    post('/product/' + productId + '/buy', {      referrer,      orderDetails    });  }  return <Form onSubmit={handleSubmit} />;}
```

/$

Just as `{}` creates a different object, function declarations like `function() {}` and expressions like `() => {}` produce a *different* function on every re-render. By itself, creating a new function is not a problem. This is not something to avoid! However, if the `Form` component is memoized, presumably you want to skip re-rendering it when no props have changed. A prop that is *always* different would defeat the point of memoization.

To memoize a function with `useMemo`, your calculation function would have to return another function:

 $

```
export default function Page({ productId, referrer }) {  const handleSubmit = useMemo(() => {    return (orderDetails) => {      post('/product/' + productId + '/buy', {        referrer,        orderDetails      });    };  }, [productId, referrer]);  return <Form onSubmit={handleSubmit} />;}
```

/$

This looks clunky! **Memoizing functions is common enough that React has a built-in Hook specifically for that. Wrap your functions intouseCallbackinstead ofuseMemo** to avoid having to write an extra nested function:

 $

```
export default function Page({ productId, referrer }) {  const handleSubmit = useCallback((orderDetails) => {    post('/product/' + productId + '/buy', {      referrer,      orderDetails    });  }, [productId, referrer]);  return <Form onSubmit={handleSubmit} />;}
```

/$

The two examples above are completely equivalent. The only benefit to `useCallback` is that it lets you avoid writing an extra nested function inside. It doesn’t do anything else. [Read more aboutuseCallback.](https://react.dev/reference/react/useCallback)

---

## Troubleshooting

### My calculation runs twice on every re-render

In [Strict Mode](https://react.dev/reference/react/StrictMode), React will call some of your functions twice instead of once:

 $

```
function TodoList({ todos, tab }) {  // This component function will run twice for every render.  const visibleTodos = useMemo(() => {    // This calculation will run twice if any of the dependencies change.    return filterTodos(todos, tab);  }, [todos, tab]);  // ...
```

/$

This is expected and shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](https://react.dev/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component and calculation functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice and fix the mistake.

For example, this impure calculation function mutates an array you received as a prop:

 $

```
const visibleTodos = useMemo(() => {    // 🚩 Mistake: mutating a prop    todos.push({ id: 'last', text: 'Go for a walk!' });    const filtered = filterTodos(todos, tab);    return filtered;  }, [todos, tab]);
```

/$

React calls your function twice, so you’d notice the todo is added twice. Your calculation shouldn’t change any existing objects, but it’s okay to change any *new* objects you created during the calculation. For example, if the `filterTodos` function always returns a *different* array, you can mutate *that* array instead:

 $

```
const visibleTodos = useMemo(() => {    const filtered = filterTodos(todos, tab);    // ✅ Correct: mutating an object you created during the calculation    filtered.push({ id: 'last', text: 'Go for a walk!' });    return filtered;  }, [todos, tab]);
```

/$

Read [keeping components pure](https://react.dev/learn/keeping-components-pure) to learn more about purity.

Also, check out the guides on [updating objects](https://react.dev/learn/updating-objects-in-state) and [updating arrays](https://react.dev/learn/updating-arrays-in-state) without mutation.

---

### MyuseMemocall is supposed to return an object, but returns undefined

This code doesn’t work:

 $

```
// 🔴 You can't return an object from an arrow function with () => {  const searchOptions = useMemo(() => {    matchMode: 'whole-word',    text: text  }, [text]);
```

/$

In JavaScript, `() => {` starts the arrow function body, so the `{` brace is not a part of your object. This is why it doesn’t return an object, and leads to mistakes. You could fix it by adding parentheses like `({` and `})`:

 $

```
// This works, but is easy for someone to break again  const searchOptions = useMemo(() => ({    matchMode: 'whole-word',    text: text  }), [text]);
```

/$

However, this is still confusing and too easy for someone to break by removing the parentheses.

To avoid this mistake, write a `return` statement explicitly:

 $

```
// ✅ This works and is explicit  const searchOptions = useMemo(() => {    return {      matchMode: 'whole-word',      text: text    };  }, [text]);
```

/$

---

### Every time my component renders, the calculation inuseMemore-runs

Make sure you’ve specified the dependency array as a second argument!

If you forget the dependency array, `useMemo` will re-run the calculation every time:

 $

```
function TodoList({ todos, tab }) {  // 🔴 Recalculates every time: no dependency array  const visibleTodos = useMemo(() => filterTodos(todos, tab));  // ...
```

/$

This is the corrected version passing the dependency array as a second argument:

 $

```
function TodoList({ todos, tab }) {  // ✅ Does not recalculate unnecessarily  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  // ...
```

/$

If this doesn’t help, then the problem is that at least one of your dependencies is different from the previous render. You can debug this problem by manually logging your dependencies to the console:

 $

```
const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);  console.log([todos, tab]);
```

/$

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as `temp1` and the second one got saved as `temp2`, you can then use the browser console to check whether each dependency in both arrays is the same:

 $

```
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

/$

When you find which dependency breaks memoization, either find a way to remove it, or [memoize it as well.](#memoizing-a-dependency-of-another-hook)

---

### I need to calluseMemofor each list item in a loop, but it’s not allowed

Suppose the `Chart` component is wrapped in [memo](https://react.dev/reference/react/memo). You want to skip re-rendering every `Chart` in the list when the `ReportList` component re-renders. However, you can’t call `useMemo` in a loop:

 $

```
function ReportList({ items }) {  return (    <article>      {items.map(item => {        // 🔴 You can't call useMemo in a loop like this:        const data = useMemo(() => calculateReport(item), [item]);        return (          <figure key={item.id}>            <Chart data={data} />          </figure>        );      })}    </article>  );}
```

/$

Instead, extract a component for each item and memoize data for individual items:

 $

```
function ReportList({ items }) {  return (    <article>      {items.map(item =>        <Report key={item.id} item={item} />      )}    </article>  );}function Report({ item }) {  // ✅ Call useMemo at the top level:  const data = useMemo(() => calculateReport(item), [item]);  return (    <figure>      <Chart data={data} />    </figure>  );}
```

/$

Alternatively, you could remove `useMemo` and instead wrap `Report` itself in [memo.](https://react.dev/reference/react/memo) If the `item` prop does not change, `Report` will skip re-rendering, so `Chart` will skip re-rendering too:

 $

```
function ReportList({ items }) {  // ...}const Report = memo(function Report({ item }) {  const data = calculateReport(item);  return (    <figure>      <Chart data={data} />    </figure>  );});
```

/$[PrevioususeLayoutEffect](https://react.dev/reference/react/useLayoutEffect)[NextuseOptimistic](https://react.dev/reference/react/useOptimistic)

---

# useOptimistic

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react/hooks)

# useOptimistic

`useOptimistic` is a React Hook that lets you optimistically update the UI.

$

```
const [optimisticState, addOptimistic] = useOptimistic(state, updateFn);
```

/$

- [Reference](#reference)
  - [useOptimistic(state, updateFn)](#use)
- [Usage](#usage)
  - [Optimistically updating forms](#optimistically-updating-with-forms)

---

## Reference

### useOptimistic(state, updateFn)

`useOptimistic` is a React Hook that lets you show a different state while an async action is underway. It accepts some state as an argument and returns a copy of that state that can be different during the duration of an async action such as a network request. You provide a function that takes the current state and the input to the action, and returns the optimistic state to be used while the action is pending.

This state is called the “optimistic” state because it is usually used to immediately present the user with the result of performing an action, even though the action actually takes time to complete.

 $

```
import { useOptimistic } from 'react';function AppContainer() {  const [optimisticState, addOptimistic] = useOptimistic(    state,    // updateFn    (currentState, optimisticValue) => {      // merge and return new state      // with optimistic value    }  );}
```

/$

[See more examples below.](#usage)

#### Parameters

- `state`: the value to be returned initially and whenever no action is pending.
- `updateFn(currentState, optimisticValue)`: a function that takes the current state and the optimistic value passed to `addOptimistic` and returns the resulting optimistic state. It must be a pure function. `updateFn` takes in two parameters. The `currentState` and the `optimisticValue`. The return value will be the merged value of the `currentState` and `optimisticValue`.

#### Returns

- `optimisticState`: The resulting optimistic state. It is equal to `state` unless an action is pending, in which case it is equal to the value returned by `updateFn`.
- `addOptimistic`: `addOptimistic` is the dispatching function to call when you have an optimistic update. It takes one argument, `optimisticValue`, of any type and will call the `updateFn` with `state` and `optimisticValue`.

---

## Usage

### Optimistically updating forms

The `useOptimistic` Hook provides a way to optimistically update the user interface before a background operation, like a network request, completes. In the context of forms, this technique helps to make apps feel more responsive. When a user submits a form, instead of waiting for the server’s response to reflect the changes, the interface is immediately updated with the expected outcome.

For example, when a user types a message into the form and hits the “Send” button, the `useOptimistic` Hook allows the message to immediately appear in the list with a “Sending…” label, even before the message is actually sent to a server. This “optimistic” approach gives the impression of speed and responsiveness. The form then attempts to truly send the message in the background. Once the server confirms the message has been received, the “Sending…” label is removed.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useOptimistic, useState, useRef, startTransition } from "react";
import { deliverMessage } from "./actions.js";

function Thread({ messages, sendMessageAction }) {
  const formRef = useRef();
  function formAction(formData) {
    addOptimisticMessage(formData.get("message"));
    formRef.current.reset();
    startTransition(async () => {
      await sendMessageAction(formData);
    });
  }
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [
      {
        text: newMessage,
        sending: true
      },
      ...state,
    ]
  );

  return (
    <>
      <form action={formAction} ref={formRef}>
        <input type="text" name="message" placeholder="Hello!" />
        <button type="submit">Send</button>
      </form>
      {optimisticMessages.map((message, index) => (
        <div key={index}>
          {message.text}
          {!!message.sending && <small> (Sending...)</small>}
        </div>
      ))}

    </>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    { text: "Hello there!", sending: false, key: 1 }
  ]);
  async function sendMessageAction(formData) {
    const sentMessage = await deliverMessage(formData.get("message"));
    startTransition(() => {
      setMessages((messages) => [{ text: sentMessage }, ...messages]);
    })
  }
  return <Thread messages={messages} sendMessageAction={sendMessageAction} />;
}
```

/$[PrevioususeMemo](https://react.dev/reference/react/useMemo)[NextuseReducer](https://react.dev/reference/react/useReducer)
