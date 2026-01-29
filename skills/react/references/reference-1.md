# React Performance tracks and more

# React Performance tracks

[API Reference](https://react.dev/reference/react)

# React Performance tracks

React Performance tracks are specialized custom entries that appear on the Performance panel’s timeline in your browser developer tools.

These tracks are designed to provide developers with comprehensive insights into their React application’s performance by visualizing React-specific events and metrics alongside other critical data sources such as network requests, JavaScript execution, and event loop activity, all synchronized on a unified timeline within the Performance panel for a complete understanding of application behavior.

 ![React Performance Tracks](https://react.dev/images/docs/performance-tracks/overview.png)![React Performance Tracks](https://react.dev/images/docs/performance-tracks/overview.dark.png)

- [Usage](#usage)
  - [Using profiling builds](#using-profiling-builds)
- [Tracks](#tracks)
  - [Scheduler](#scheduler)
  - [Components](#components)
  - [Server](#server)

---

## Usage

React Performance tracks are only available in development and profiling builds of React:

- **Development**: enabled by default.
- **Profiling**: Only Scheduler tracks are enabled by default. The Components track only lists Components that are in subtrees wrapped with [<Profiler>](https://react.dev/reference/react/Profiler). If you have [React Developer Tools extension](https://react.dev/learn/react-developer-tools) enabled, all Components are included in the Components track even if they’re not wrapped in `<Profiler>`. Server tracks are not available in profiling builds.

If enabled, tracks should appear automatically in the traces you record with the Performance panel of browsers that provide [extensibility APIs](https://developer.chrome.com/docs/devtools/performance/extension).

### Pitfall

The profiling instrumentation that powers React Performance tracks adds some additional overhead, so it is disabled in production builds by default.
Server Components and Server Requests tracks are only available in development builds.

### Using profiling builds

In addition to production and development builds, React also includes a special profiling build.
To use profiling builds, you have to use `react-dom/profiling` instead of `react-dom/client`.
We recommend that you alias `react-dom/client` to `react-dom/profiling` at build time via bundler aliases instead of manually updating each `react-dom/client` import.
Your framework might have built-in support for enabling React’s profiling build.

---

## Tracks

### Scheduler

The Scheduler is an internal React concept used for managing tasks with different priorities. This track consists of 4 subtracks, each representing work of a specific priority:

- **Blocking** - The synchronous updates, which could’ve been initiated by user interactions.
- **Transition** - Non-blocking work that happens in the background, usually initiated via [startTransition](https://react.dev/reference/react/startTransition).
- **Suspense** - Work related to Suspense boundaries, such as displaying fallbacks or revealing content.
- **Idle** - The lowest priority work that is done when there are no other tasks with higher priority.

 ![Scheduler track](https://react.dev/images/docs/performance-tracks/scheduler.png)![Scheduler track](https://react.dev/images/docs/performance-tracks/scheduler.dark.png)

#### Renders

Every render pass consists of multiple phases that you can see on a timeline:

- **Update** - this is what caused a new render pass.
- **Render** - React renders the updated subtree by calling render functions of components. You can see the rendered components subtree on [Components track](#components), which follows the same color scheme.
- **Commit** - After rendering components, React will submit the changes to the DOM and run layout effects, like [useLayoutEffect](https://react.dev/reference/react/useLayoutEffect).
- **Remaining Effects** - React runs passive effects of a rendered subtree. This usually happens after the paint, and this is when React runs hooks like [useEffect](https://react.dev/reference/react/useEffect). One known exception is user interactions, like clicks, or other discrete events. In this scenario, this phase could run before the paint.

 ![Scheduler track: updates](https://react.dev/images/docs/performance-tracks/scheduler-update.png)![Scheduler track: updates](https://react.dev/images/docs/performance-tracks/scheduler-update.dark.png)

[Learn more about renders and commits](https://react.dev/learn/render-and-commit).

#### Cascading updates

Cascading updates is one of the patterns for performance regressions. If an update was scheduled during a render pass, React could discard completed work and start a new pass.

In development builds, React can show you which Component scheduled a new update. This includes both general updates and cascading ones. You can see the enhanced stack trace by clicking on the “Cascading update” entry, which should also display the name of the method that scheduled an update.

 ![Scheduler track: cascading updates](https://react.dev/images/docs/performance-tracks/scheduler-cascading-update.png)![Scheduler track: cascading updates](https://react.dev/images/docs/performance-tracks/scheduler-cascading-update.dark.png)

[Learn more about Effects](https://react.dev/learn/you-might-not-need-an-effect).

### Components

The Components track visualizes the durations of React components. They are displayed as a flamegraph, where each entry represents the duration of the corresponding component render and all its descendant children components.

 ![Components track: render durations](https://react.dev/images/docs/performance-tracks/components-render.png)![Components track: render durations](https://react.dev/images/docs/performance-tracks/components-render.dark.png)

Similar to render durations, effect durations are also represented as a flamegraph, but with a different color scheme that aligns with the corresponding phase on the Scheduler track.

 ![Components track: effects durations](https://react.dev/images/docs/performance-tracks/components-effects.png)![Components track: effects durations](https://react.dev/images/docs/performance-tracks/components-effects.dark.png)

### Note

Unlike renders, not all effects are shown on the Components track by default.

To maintain performance and prevent UI clutter, React will only display those effects, which had a duration of 0.05ms or longer, or triggered an update.

Additional events may be displayed during the render and effects phases:

- Mount - A corresponding subtree of component renders or effects was mounted.
- Unmount - A corresponding subtree of component renders or effects was unmounted.
- Reconnect - Similar to Mount, but limited to cases when [<Activity>](https://react.dev/reference/react/Activity) is used.
- Disconnect - Similar to Unmount, but limited to cases when [<Activity>](https://react.dev/reference/react/Activity) is used.

#### Changed props

In development builds, when you click on a component render entry, you can inspect potential changes in props. You can use this information to identify unnecessary renders.

 ![Components track: changed props](https://react.dev/images/docs/performance-tracks/changed-props.png)![Components track: changed props](https://react.dev/images/docs/performance-tracks/changed-props.dark.png)

### Server

 ![React Server Performance Tracks](https://react.dev/images/docs/performance-tracks/server-overview.png)![React Server Performance Tracks](https://react.dev/images/docs/performance-tracks/server-overview.dark.png)

#### Server Requests

The Server Requests track visualized all Promises that eventually end up in a React Server Component. This includes any `async` operations like calling `fetch` or async Node.js file operations.

React will try to combine Promises that are started from inside third-party code into a single span representing the the duration of the entire operation blocking 1st party code.
For example, a third party library method called `getUser` that calls `fetch` internally multiple times will be represented as a single span called `getUser`, instead of showing multiple `fetch` spans.

Clicking on spans will show you a stack trace of where the Promise was created as well as a view of the value that the Promise resolved to, if available.

Rejected Promises are displayed as red with their rejected value.

#### Server Components

The Server Components tracks visualize the durations of React Server Components Promises they awaited. Timings are displayed as a flamegraph, where each entry represents the duration of the corresponding component render and all its descendant children components.

If you await a Promise, React will display duration of that Promise. To see all I/O operations, use the Server Requests track.

Different colors are used to indicate the duration of the component render. The darker the color, the longer the duration.

The Server Components track group will always contain a “Primary” track. If React is able to render Server Components concurrently, it will display addititional “Parallel” tracks.
If more than 8 Server Components are rendered concurrently, React will associate them with the last “Parallel” track instead of adding more tracks.

---

# component

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# component-hook-factories

Validates against higher order functions defining nested components or hooks. Components and hooks should be defined at the module level.

## Rule Details

Defining components or hooks inside other functions creates new instances on every call. React treats each as a completely different component, destroying and recreating the entire component tree, losing all state, and causing performance problems.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Factory function creating componentsfunction createComponent(defaultValue) {  return function Component() {    // ...  };}// ❌ Component defined inside componentfunction Parent() {  function Child() {    // ...  }  return <Child />;}// ❌ Hook factory functionfunction createCustomHook(endpoint) {  return function useData() {    // ...  };}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Component defined at module levelfunction Component({ defaultValue }) {  // ...}// ✅ Custom hook at module levelfunction useData(endpoint) {  // ...}
```

/$

## Troubleshooting

### I need dynamic component behavior

You might think you need a factory to create customized components:

 $

```
// ❌ Wrong: Factory patternfunction makeButton(color) {  return function Button({children}) {    return (      <button style={{backgroundColor: color}}>        {children}      </button>    );  };}const RedButton = makeButton('red');const BlueButton = makeButton('blue');
```

/$

Pass [JSX as children](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) instead:

 $

```
// ✅ Better: Pass JSX as childrenfunction Button({color, children}) {  return (    <button style={{backgroundColor: color}}>      {children}    </button>  );}function App() {  return (    <>      <Button color="red">Red</Button>      <Button color="blue">Blue</Button>    </>  );}
```

/$[Previousrules-of-hooks](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks)[Nextconfig](https://react.dev/reference/eslint-plugin-react-hooks/lints/config)

---

# config

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# config

Validates the compiler [configuration options](https://react.dev/reference/react-compiler/configuration).

## Rule Details

React Compiler accepts various [configuration options](https://react.dev/reference/react-compiler/configuration)  to control its behavior. This rule validates that your configuration uses correct option names and value types, preventing silent failures from typos or incorrect settings.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Unknown option namemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compileMode: 'all' // Typo: should be compilationMode    }]  ]};// ❌ Invalid option valuemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'everything' // Invalid: use 'all' or 'infer'    }]  ]};
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Valid compiler configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'infer',      panicThreshold: 'critical_errors'    }]  ]};
```

/$

## Troubleshooting

### Configuration not working as expected

Your compiler configuration might have typos or incorrect values:

 $

```
// ❌ Wrong: Common configuration mistakesmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      // Typo in option name      compilationMod: 'all',      // Wrong value type      panicThreshold: true,      // Unknown option      optimizationLevel: 'max'    }]  ]};
```

/$

Check the [configuration documentation](https://react.dev/reference/react-compiler/configuration) for valid options:

 $

```
// ✅ Better: Valid configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'all', // or 'infer'      panicThreshold: 'none', // or 'critical_errors', 'all_errors'      // Only use documented options    }]  ]};
```

/$[Previouscomponent-hook-factories](https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories)[Nexterror-boundaries](https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries)

---

# error

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# error-boundaries

Validates usage of Error Boundaries instead of try/catch for errors in child components.

## Rule Details

Try/catch blocks can’t catch errors that happen during React’s rendering process. Errors thrown in rendering methods or hooks bubble up through the component tree. Only [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) can catch these errors.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Try/catch won't catch render errorsfunction Parent() {  try {    return <ChildComponent />; // If this throws, catch won't help  } catch (error) {    return <div>Error occurred</div>;  }}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Using error boundaryfunction Parent() {  return (    <ErrorBoundary>      <ChildComponent />    </ErrorBoundary>  );}
```

/$

## Troubleshooting

### Why is the linter telling me not to wrapuseintry/catch?

The `use` hook doesn’t throw errors in the traditional sense, it suspends component execution. When `use` encounters a pending promise, it suspends the component and lets React show a fallback. Only Suspense and Error Boundaries can handle these cases. The linter warns against `try`/`catch` around `use` to prevent confusion as the `catch` block would never run.

 $

```
// ❌ Try/catch around `use` hookfunction Component({promise}) {  try {    const data = use(promise); // Won't catch - `use` suspends, not throws    return <div>{data}</div>;  } catch (error) {    return <div>Failed to load</div>; // Unreachable  }}// ✅ Error boundary catches `use` errorsfunction App() {  return (    <ErrorBoundary fallback={<div>Failed to load</div>}>      <Suspense fallback={<div>Loading...</div>}>        <DataComponent promise={fetchData()} />      </Suspense>    </ErrorBoundary>  );}
```

/$[Previousconfig](https://react.dev/reference/eslint-plugin-react-hooks/lints/config)[Nextgating](https://react.dev/reference/eslint-plugin-react-hooks/lints/gating)

---

# exhaustive

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# exhaustive-deps

Validates that dependency arrays for React hooks contain all necessary dependencies.

## Rule Details

React hooks like `useEffect`, `useMemo`, and `useCallback` accept dependency arrays. When a value referenced inside these hooks isn’t included in the dependency array, React won’t re-run the effect or recalculate the value when that dependency changes. This causes stale closures where the hook uses outdated values.

## Common Violations

This error often happens when you try to “trick” React about dependencies to control when an effect runs. Effects should synchronize your component with external systems. The dependency array tells React which values the effect uses, so React knows when to re-synchronize.

If you find yourself fighting with the linter, you likely need to restructure your code. See [Removing Effect Dependencies](https://react.dev/learn/removing-effect-dependencies) to learn how.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Missing dependencyuseEffect(() => {  console.log(count);}, []); // Missing 'count'// ❌ Missing propuseEffect(() => {  fetchUser(userId);}, []); // Missing 'userId'// ❌ Incomplete dependenciesuseMemo(() => {  return items.sort(sortOrder);}, [items]); // Missing 'sortOrder'
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ All dependencies includeduseEffect(() => {  console.log(count);}, [count]);// ✅ All dependencies includeduseEffect(() => {  fetchUser(userId);}, [userId]);
```

/$

## Troubleshooting

### Adding a function dependency causes infinite loops

You have an effect, but you’re creating a new function on every render:

 $

```
// ❌ Causes infinite loopconst logItems = () => {  console.log(items);};useEffect(() => {  logItems();}, [logItems]); // Infinite loop!
```

/$

In most cases, you don’t need the effect. Call the function where the action happens instead:

 $

```
// ✅ Call it from the event handlerconst logItems = () => {  console.log(items);};return <button onClick={logItems}>Log</button>;// ✅ Or derive during render if there's no side effectitems.forEach(item => {  console.log(item);});
```

/$

If you genuinely need the effect (for example, to subscribe to something external), make the dependency stable:

 $

```
// ✅ useCallback keeps the function reference stableconst logItems = useCallback(() => {  console.log(items);}, [items]);useEffect(() => {  logItems();}, [logItems]);// ✅ Or move the logic straight into the effectuseEffect(() => {  console.log(items);}, [items]);
```

/$

### Running an effect only once

You want to run an effect once on mount, but the linter complains about missing dependencies:

 $

```
// ❌ Missing dependencyuseEffect(() => {  sendAnalytics(userId);}, []); // Missing 'userId'
```

/$

Either include the dependency (recommended) or use a ref if you truly need to run once:

 $

```
// ✅ Include dependencyuseEffect(() => {  sendAnalytics(userId);}, [userId]);// ✅ Or use a ref guard inside an effectconst sent = useRef(false);useEffect(() => {  if (sent.current) {    return;  }  sent.current = true;  sendAnalytics(userId);}, [userId]);
```

/$

## Options

You can configure custom effect hooks using shared ESLint settings (available in `eslint-plugin-react-hooks` 6.1.1 and later):

 $

```
{  "settings": {    "react-hooks": {      "additionalEffectHooks": "(useMyEffect|useCustomEffect)"    }  }}
```

/$

- `additionalEffectHooks`: Regex pattern matching custom hooks that should be checked for exhaustive dependencies. This configuration is shared across all `react-hooks` rules.

For backward compatibility, this rule also accepts a rule-level option:

 $

```
{  "rules": {    "react-hooks/exhaustive-deps": ["warn", {      "additionalHooks": "(useMyCustomHook|useAnotherHook)"    }]  }}
```

/$

- `additionalHooks`: Regex for hooks that should be checked for exhaustive dependencies. **Note:** If this rule-level option is specified, it takes precedence over the shared `settings` configuration.

[PreviousLints](https://react.dev/reference/eslint-plugin-react-hooks)[Nextrules-of-hooks](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks)

---

# gating

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# gating

Validates configuration of [gating mode](https://react.dev/reference/react-compiler/gating).

## Rule Details

Gating mode lets you gradually adopt React Compiler by marking specific components for optimization. This rule ensures your gating configuration is valid so the compiler knows which components to process.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Missing required fieldsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: {        importSpecifierName: '__experimental_useCompiler'        // Missing 'source' field      }    }]  ]};// ❌ Invalid gating typemodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: '__experimental_useCompiler' // Should be object    }]  ]};
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Complete gating configurationmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: {        importSpecifierName: 'isCompilerEnabled', // exported function name        source: 'featureFlags' // module name      }    }]  ]};// featureFlags.jsexport function isCompilerEnabled() {  // ...}// ✅ No gating (compile everything)module.exports = {  plugins: [    ['babel-plugin-react-compiler', {      // No gating field - compiles all components    }]  ]};
```

/$[Previouserror-boundaries](https://react.dev/reference/eslint-plugin-react-hooks/lints/error-boundaries)[Nextglobals](https://react.dev/reference/eslint-plugin-react-hooks/lints/globals)

---

# globals

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# globals

Validates against assignment/mutation of globals during render, part of ensuring that [side effects must run outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#side-effects-must-run-outside-of-render).

## Rule Details

Global variables exist outside React’s control. When you modify them during render, you break React’s assumption that rendering is pure. This can cause components to behave differently in development vs production, break Fast Refresh, and make your app impossible to optimize with features like React Compiler.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Global counterlet renderCount = 0;function Component() {  renderCount++; // Mutating global  return <div>Count: {renderCount}</div>;}// ❌ Modifying window propertiesfunction Component({userId}) {  window.currentUser = userId; // Global mutation  return <div>User: {userId}</div>;}// ❌ Global array pushconst events = [];function Component({event}) {  events.push(event); // Mutating global array  return <div>Events: {events.length}</div>;}// ❌ Cache manipulationconst cache = {};function Component({id}) {  if (!cache[id]) {    cache[id] = fetchData(id); // Modifying cache during render  }  return <div>{cache[id]}</div>;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Use state for countersfunction Component() {  const [clickCount, setClickCount] = useState(0);  const handleClick = () => {    setClickCount(c => c + 1);  };  return (    <button onClick={handleClick}>      Clicked: {clickCount} times    </button>  );}// ✅ Use context for global valuesfunction Component() {  const user = useContext(UserContext);  return <div>User: {user.id}</div>;}// ✅ Synchronize external state with Reactfunction Component({title}) {  useEffect(() => {    document.title = title; // OK in effect  }, [title]);  return <div>Page: {title}</div>;}
```

/$[Previousgating](https://react.dev/reference/eslint-plugin-react-hooks/lints/gating)[Nextimmutability](https://react.dev/reference/eslint-plugin-react-hooks/lints/immutability)

---

# immutability

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# immutability

Validates against mutating props, state, and other values that [are immutable](https://react.dev/reference/rules/components-and-hooks-must-be-pure#props-and-state-are-immutable).

## Rule Details

A component’s props and state are immutable snapshots. Never mutate them directly. Instead, pass new props down, and use the setter function from `useState`.

## Common Violations

### Invalid

 $

```
// ❌ Array push mutationfunction Component() {  const [items, setItems] = useState([1, 2, 3]);  const addItem = () => {    items.push(4); // Mutating!    setItems(items); // Same reference, no re-render  };}// ❌ Object property assignmentfunction Component() {  const [user, setUser] = useState({name: 'Alice'});  const updateName = () => {    user.name = 'Bob'; // Mutating!    setUser(user); // Same reference  };}// ❌ Sort without spreadingfunction Component() {  const [items, setItems] = useState([3, 1, 2]);  const sortItems = () => {    setItems(items.sort()); // sort mutates!  };}
```

/$

### Valid

 $

```
// ✅ Create new arrayfunction Component() {  const [items, setItems] = useState([1, 2, 3]);  const addItem = () => {    setItems([...items, 4]); // New array  };}// ✅ Create new objectfunction Component() {  const [user, setUser] = useState({name: 'Alice'});  const updateName = () => {    setUser({...user, name: 'Bob'}); // New object  };}
```

/$

## Troubleshooting

### I need to add items to an array

Mutating arrays with methods like `push()` won’t trigger re-renders:

 $

```
// ❌ Wrong: Mutating the arrayfunction TodoList() {  const [todos, setTodos] = useState([]);  const addTodo = (id, text) => {    todos.push({id, text});    setTodos(todos); // Same array reference!  };  return (    <ul>      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}    </ul>  );}
```

/$

Create a new array instead:

 $

```
// ✅ Better: Create a new arrayfunction TodoList() {  const [todos, setTodos] = useState([]);  const addTodo = (id, text) => {    setTodos([...todos, {id, text}]);    // Or: setTodos(todos => [...todos, {id: Date.now(), text}])  };  return (    <ul>      {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}    </ul>  );}
```

/$

### I need to update nested objects

Mutating nested properties doesn’t trigger re-renders:

 $

```
// ❌ Wrong: Mutating nested objectfunction UserProfile() {  const [user, setUser] = useState({    name: 'Alice',    settings: {      theme: 'light',      notifications: true    }  });  const toggleTheme = () => {    user.settings.theme = 'dark'; // Mutation!    setUser(user); // Same object reference  };}
```

/$

Spread at each level that needs updating:

 $

```
// ✅ Better: Create new objects at each levelfunction UserProfile() {  const [user, setUser] = useState({    name: 'Alice',    settings: {      theme: 'light',      notifications: true    }  });  const toggleTheme = () => {    setUser({      ...user,      settings: {        ...user.settings,        theme: 'dark'      }    });  };}
```

/$[Previousglobals](https://react.dev/reference/eslint-plugin-react-hooks/lints/globals)[Nextincompatible-library](https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library)

---

# incompatible

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# incompatible-library

Validates against usage of libraries which are incompatible with memoization (manual or automatic).

### Note

These libraries were designed before React’s memoization rules were fully documented. They made the correct choices at the time to optimize for ergonomic ways to keep components just the right amount of reactive as app state changes. While these legacy patterns worked, we have since discovered that it’s incompatible with React’s programming model. We will continue working with library authors to migrate these libraries to use patterns that follow the Rules of React.

## Rule Details

Some libraries use patterns that aren’t supported by React. When the linter detects usages of these APIs from a [known list](https://github.com/facebook/react/blob/main/compiler/packages/babel-plugin-react-compiler/src/HIR/DefaultModuleTypeProvider.ts), it flags them under this rule. This means that React Compiler can automatically skip over components that use these incompatible APIs, in order to avoid breaking your app.

 $

```
// Example of how memoization breaks with these librariesfunction Form() {  const { watch } = useForm();  // ❌ This value will never update, even when 'name' field changes  const name = useMemo(() => watch('name'), [watch]);  return <div>Name: {name}</div>; // UI appears "frozen"}
```

/$

React Compiler automatically memoizes values following the Rules of React. If something breaks with manual `useMemo`, it will also break the compiler’s automatic optimization. This rule helps identify these problematic patterns.

##### Deep Dive

#### Designing APIs that follow the Rules of React

One question to think about when designing a library API or hook is whether calling the API can be safely memoized with `useMemo`. If it can’t, then both manual and React Compiler memoizations will break your user’s code.

For example, one such incompatible pattern is “interior mutability”. Interior mutability is when an object or function keeps its own hidden state that changes over time, even though the reference to it stays the same. Think of it like a box that looks the same on the outside but secretly rearranges its contents. React can’t tell anything changed because it only checks if you gave it a different box, not what’s inside. This breaks memoization, since React relies on the outer object (or function) changing if part of its value has changed.

As a rule of thumb, when designing React APIs, think about whether `useMemo` would break it:

$

```
function Component() {  const { someFunction } = useLibrary();  // it should always be safe to memoize functions like this  const result = useMemo(() => someFunction(), [someFunction]);}
```

/$

Instead, design APIs that return immutable state and use explicit update functions:

$

```
// ✅ Good: Return immutable state that changes reference when updatedfunction Component() {  const { field, updateField } = useLibrary();  // this is always safe to memo  const greeting = useMemo(() => `Hello, ${field.name}!`, [field.name]);  return (    <div>      <input        value={field.name}        onChange={(e) => updateField('name', e.target.value)}      />      <p>{greeting}</p>    </div>  );}
```

/$

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ react-hook-form `watch`function Component() {  const {watch} = useForm();  const value = watch('field'); // Interior mutability  return <div>{value}</div>;}// ❌ TanStack Table `useReactTable`function Component({data}) {  const table = useReactTable({    data,    columns,    getCoreRowModel: getCoreRowModel(),  });  // table instance uses interior mutability  return <Table table={table} />;}
```

/$

### Pitfall

#### MobX

MobX patterns like `observer` also break memoization assumptions, but the linter does not yet detect them. If you rely on MobX and find that your app doesn’t work with React Compiler, you may need to use the `"use no memo" directive`.

$

```
// ❌ MobX `observer`const Component = observer(() => {  const [timer] = useState(() => new Timer());  return <span>Seconds passed: {timer.secondsPassed}</span>;});
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ For react-hook-form, use `useWatch`:function Component() {  const {register, control} = useForm();  const watchedValue = useWatch({    control,    name: 'field'  });  return (    <>      <input {...register('field')} />      <div>Current value: {watchedValue}</div>    </>  );}
```

/$

Some other libraries do not yet have alternative APIs that are compatible with React’s memoization model. If the linter doesn’t automatically skip over your components or hooks that call these APIs, please [file an issue](https://github.com/facebook/react/issues) so we can add it to the linter.

[Previousimmutability](https://react.dev/reference/eslint-plugin-react-hooks/lints/immutability)[Nextpreserve-manual-memoization](https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization)

---

# preserve

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# preserve-manual-memoization

Validates that existing manual memoization is preserved by the compiler. React Compiler will only compile components and hooks if its inference [matches or exceeds the existing manual memoization](https://react.dev/learn/react-compiler/introduction#what-should-i-do-about-usememo-usecallback-and-reactmemo).

## Rule Details

React Compiler preserves your existing `useMemo`, `useCallback`, and `React.memo` calls. If you’ve manually memoized something, the compiler assumes you had a good reason and won’t remove it. However, incomplete dependencies prevent the compiler from understanding your code’s data flow and applying further optimizations.

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Missing dependencies in useMemofunction Component({ data, filter }) {  const filtered = useMemo(    () => data.filter(filter),    [data] // Missing 'filter' dependency  );  return <List items={filtered} />;}// ❌ Missing dependencies in useCallbackfunction Component({ onUpdate, value }) {  const handleClick = useCallback(() => {    onUpdate(value);  }, [onUpdate]); // Missing 'value'  return <button onClick={handleClick}>Update</button>;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Complete dependenciesfunction Component({ data, filter }) {  const filtered = useMemo(    () => data.filter(filter),    [data, filter] // All dependencies included  );  return <List items={filtered} />;}// ✅ Or let the compiler handle itfunction Component({ data, filter }) {  // No manual memoization needed  const filtered = data.filter(filter);  return <List items={filtered} />;}
```

/$

## Troubleshooting

### Should I remove my manual memoization?

You might wonder if React Compiler makes manual memoization unnecessary:

 $

```
// Do I still need this?function Component({items, sortBy}) {  const sorted = useMemo(() => {    return [...items].sort((a, b) => {      return a[sortBy] - b[sortBy];    });  }, [items, sortBy]);  return <List items={sorted} />;}
```

/$

You can safely remove it if using React Compiler:

 $

```
// ✅ Better: Let the compiler optimizefunction Component({items, sortBy}) {  const sorted = [...items].sort((a, b) => {    return a[sortBy] - b[sortBy];  });  return <List items={sorted} />;}
```

/$[Previousincompatible-library](https://react.dev/reference/eslint-plugin-react-hooks/lints/incompatible-library)[Nextpurity](https://react.dev/reference/eslint-plugin-react-hooks/lints/purity)

---

# purity

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# purity

Validates that [components/hooks are pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure) by checking that they do not call known-impure functions.

## Rule Details

React components must be pure functions - given the same props, they should always return the same JSX. When components use functions like `Math.random()` or `Date.now()` during render, they produce different output each time, breaking React’s assumptions and causing bugs like hydration mismatches, incorrect memoization, and unpredictable behavior.

## Common Violations

In general, any API that returns a different value for the same inputs violates this rule. Usual examples include:

- `Math.random()`
- `Date.now()` / `new Date()`
- `crypto.randomUUID()`
- `performance.now()`

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Math.random() in renderfunction Component() {  const id = Math.random(); // Different every render  return <div key={id}>Content</div>;}// ❌ Date.now() for valuesfunction Component() {  const timestamp = Date.now(); // Changes every render  return <div>Created at: {timestamp}</div>;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Stable IDs from initial statefunction Component() {  const [id] = useState(() => crypto.randomUUID());  return <div key={id}>Content</div>;}
```

/$

## Troubleshooting

### I need to show the current time

Calling `Date.now()` during render makes your component impure:

 $

```
// ❌ Wrong: Time changes every renderfunction Clock() {  return <div>Current time: {Date.now()}</div>;}
```

/$

Instead, [move the impure function outside of render](https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent):

 $

```
function Clock() {  const [time, setTime] = useState(() => Date.now());  useEffect(() => {    const interval = setInterval(() => {      setTime(Date.now());    }, 1000);    return () => clearInterval(interval);  }, []);  return <div>Current time: {time}</div>;}
```

/$[Previouspreserve-manual-memoization](https://react.dev/reference/eslint-plugin-react-hooks/lints/preserve-manual-memoization)[Nextrefs](https://react.dev/reference/eslint-plugin-react-hooks/lints/refs)

---

# refs

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# refs

Validates correct usage of refs, not reading/writing during render. See the “pitfalls” section in [useRef()usage](https://react.dev/reference/react/useRef#usage).

## Rule Details

Refs hold values that aren’t used for rendering. Unlike state, changing a ref doesn’t trigger a re-render. Reading or writing `ref.current` during render breaks React’s expectations. Refs might not be initialized when you try to read them, and their values can be stale or inconsistent.

## How It Detects Refs

The lint only applies these rules to values it knows are refs. A value is inferred as a ref when the compiler sees any of the following patterns:

- Returned from `useRef()` or `React.createRef()`.
   $
  ```
  const scrollRef = useRef(null);
  ```
  /$
- An identifier named `ref` or ending in `Ref` that reads from or writes to `.current`.
   $
  ```
  buttonRef.current = node;
  ```
  /$
- Passed through a JSX `ref` prop (for example `<div ref={someRef} />`).
   $
  ```
  <input ref={inputRef} />
  ```
  /$

Once something is marked as a ref, that inference follows the value through assignments, destructuring, or helper calls. This lets the lint surface violations even when `ref.current` is accessed inside another function that received the ref as an argument.

## Common Violations

- Reading `ref.current` during render
- Updating `refs` during render
- Using `refs` for values that should be state

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Reading ref during renderfunction Component() {  const ref = useRef(0);  const value = ref.current; // Don't read during render  return <div>{value}</div>;}// ❌ Modifying ref during renderfunction Component({value}) {  const ref = useRef(null);  ref.current = value; // Don't modify during render  return <div />;}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ Read ref in effects/handlersfunction Component() {  const ref = useRef(null);  useEffect(() => {    if (ref.current) {      console.log(ref.current.offsetWidth); // OK in effect    }  });  return <div ref={ref} />;}// ✅ Use state for UI valuesfunction Component() {  const [count, setCount] = useState(0);  return (    <button onClick={() => setCount(count + 1)}>      {count}    </button>  );}// ✅ Lazy initialization of ref valuefunction Component() {  const ref = useRef(null);  // Initialize only once on first use  if (ref.current === null) {    ref.current = expensiveComputation(); // OK - lazy initialization  }  const handleClick = () => {    console.log(ref.current); // Use the initialized value  };  return <button onClick={handleClick}>Click</button>;}
```

/$

## Troubleshooting

### The lint flagged my plain object with.current

The name heuristic intentionally treats `ref.current` and `fooRef.current` as real refs. If you’re modeling a custom container object, pick a different name (for example, `box`) or move the mutable value into state. Renaming avoids the lint because the compiler stops inferring it as a ref.

[Previouspurity](https://react.dev/reference/eslint-plugin-react-hooks/lints/purity)[Nextset-state-in-effect](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect)

---

# rules

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# rules-of-hooks

Validates that components and hooks follow the [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks).

## Rule Details

React relies on the order in which hooks are called to correctly preserve state between renders. Each time your component renders, React expects the exact same hooks to be called in the exact same order. When hooks are called conditionally or in loops, React loses track of which state corresponds to which hook call, leading to bugs like state mismatches and “Rendered fewer/more hooks than expected” errors.

## Common Violations

These patterns violate the Rules of Hooks:

- **Hooks in conditions** (`if`/`else`, ternary, `&&`/`||`)
- **Hooks in loops** (`for`, `while`, `do-while`)
- **Hooks after early returns**
- **Hooks in callbacks/event handlers**
- **Hooks in async functions**
- **Hooks in class methods**
- **Hooks at module level**

### Note

### usehook

The `use` hook is different from other React hooks. You can call it conditionally and in loops:

$

```
// ✅ `use` can be conditionalif (shouldFetch) {  const data = use(fetchPromise);}// ✅ `use` can be in loopsfor (const promise of promises) {  results.push(use(promise));}
```

/$

However, `use` still has restrictions:

- Can’t be wrapped in try/catch
- Must be called inside a component or hook

Learn more: [useAPI Reference](https://react.dev/reference/react/use)

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Hook in conditionif (isLoggedIn) {  const [user, setUser] = useState(null);}// ❌ Hook after early returnif (!data) return <Loading />;const [processed, setProcessed] = useState(data);// ❌ Hook in callback<button onClick={() => {  const [clicked, setClicked] = useState(false);}}/>// ❌ `use` in try/catchtry {  const data = use(promise);} catch (e) {  // error handling}// ❌ Hook at module levelconst globalState = useState(0); // Outside component
```

/$

### Valid

Examples of correct code for this rule:

 $

```
function Component({ isSpecial, shouldFetch, fetchPromise }) {  // ✅ Hooks at top level  const [count, setCount] = useState(0);  const [name, setName] = useState('');  if (!isSpecial) {    return null;  }  if (shouldFetch) {    // ✅ `use` can be conditional    const data = use(fetchPromise);    return <div>{data}</div>;  }  return <div>{name}: {count}</div>;}
```

/$

## Troubleshooting

### I want to fetch data based on some condition

You’re trying to conditionally call useEffect:

 $

```
// ❌ Conditional hookif (isLoggedIn) {  useEffect(() => {    fetchUserData();  }, []);}
```

/$

Call the hook unconditionally, check condition inside:

 $

```
// ✅ Condition inside hookuseEffect(() => {  if (isLoggedIn) {    fetchUserData();  }}, [isLoggedIn]);
```

/$

### Note

There are better ways to fetch data rather than in a useEffect. Consider using TanStack Query, useSWR, or React Router 6.4+ for data fetching. These solutions handle deduplicating requests, caching responses, and avoiding network waterfalls.

Learn more: [Fetching Data](https://react.dev/learn/synchronizing-with-effects#fetching-data)

### I need different state for different scenarios

You’re trying to conditionally initialize state:

 $

```
// ❌ Conditional stateif (userType === 'admin') {  const [permissions, setPermissions] = useState(adminPerms);} else {  const [permissions, setPermissions] = useState(userPerms);}
```

/$

Always call useState, conditionally set the initial value:

 $

```
// ✅ Conditional initial valueconst [permissions, setPermissions] = useState(  userType === 'admin' ? adminPerms : userPerms);
```

/$

## Options

You can configure custom effect hooks using shared ESLint settings (available in `eslint-plugin-react-hooks` 6.1.1 and later):

 $

```
{  "settings": {    "react-hooks": {      "additionalEffectHooks": "(useMyEffect|useCustomEffect)"    }  }}
```

/$

- `additionalEffectHooks`: Regex pattern matching custom hooks that should be treated as effects. This allows `useEffectEvent` and similar event functions to be called from your custom effect hooks.

This shared configuration is used by both `rules-of-hooks` and `exhaustive-deps` rules, ensuring consistent behavior across all hook-related linting.

[Previousexhaustive-deps](https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps)[Nextcomponent-hook-factories](https://react.dev/reference/eslint-plugin-react-hooks/lints/component-hook-factories)

---

# set

[API Reference](https://react.dev/reference/react)[Lints](https://react.dev/reference/eslint-plugin-react-hooks)

# set-state-in-effect

Validates against calling setState synchronously in an effect, which can lead to re-renders that degrade performance.

## Rule Details

Setting state immediately inside an effect forces React to restart the entire render cycle. When you update state in an effect, React must re-render your component, apply changes to the DOM, and then run effects again. This creates an extra render pass that could have been avoided by transforming data directly during render or deriving state from props. Transform data at the top level of your component instead. This code will naturally re-run when props or state change without triggering additional render cycles.

Synchronous `setState` calls in effects trigger immediate re-renders before the browser can paint, causing performance issues and visual jank. React has to render twice: once to apply the state update, then again after effects run. This double rendering is wasteful when the same result could be achieved with a single render.

In many cases, you may also not need an effect at all. Please see [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) for more information.

## Common Violations

This rule catches several patterns where synchronous setState is used unnecessarily:

- Setting loading state synchronously
- Deriving state from props in effects
- Transforming data in effects instead of render

### Invalid

Examples of incorrect code for this rule:

 $

```
// ❌ Synchronous setState in effectfunction Component({data}) {  const [items, setItems] = useState([]);  useEffect(() => {    setItems(data); // Extra render, use initial state instead  }, [data]);}// ❌ Setting loading state synchronouslyfunction Component() {  const [loading, setLoading] = useState(false);  useEffect(() => {    setLoading(true); // Synchronous, causes extra render    fetchData().then(() => setLoading(false));  }, []);}// ❌ Transforming data in effectfunction Component({rawData}) {  const [processed, setProcessed] = useState([]);  useEffect(() => {    setProcessed(rawData.map(transform)); // Should derive in render  }, [rawData]);}// ❌ Deriving state from propsfunction Component({selectedId, items}) {  const [selected, setSelected] = useState(null);  useEffect(() => {    setSelected(items.find(i => i.id === selectedId));  }, [selectedId, items]);}
```

/$

### Valid

Examples of correct code for this rule:

 $

```
// ✅ setState in an effect is fine if the value comes from a reffunction Tooltip() {  const ref = useRef(null);  const [tooltipHeight, setTooltipHeight] = useState(0);  useLayoutEffect(() => {    const { height } = ref.current.getBoundingClientRect();    setTooltipHeight(height);  }, []);}// ✅ Calculate during renderfunction Component({selectedId, items}) {  const selected = items.find(i => i.id === selectedId);  return <div>{selected?.name}</div>;}
```

/$

**When something can be calculated from the existing props or state, don’t put it in state.** Instead, calculate it during rendering. This makes your code faster, simpler, and less error-prone. Learn more in [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect).

[Previousrefs](https://react.dev/reference/eslint-plugin-react-hooks/lints/refs)[Nextset-state-in-render](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render)
