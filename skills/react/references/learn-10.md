# Queueing a Series of State Updates and more

# Queueing a Series of State Updates

[Learn React](https://react.dev/learn)[Adding Interactivity](https://react.dev/learn/adding-interactivity)

# Queueing a Series of State Updates

Setting a state variable will queue another render. But sometimes you might want to perform multiple operations on the value before queueing the next render. To do this, it helps to understand how React batches state updates.

### You will learn

- What “batching” is and how React uses it to process multiple state updates
- How to apply several updates to the same state variable in a row

## React batches state updates

You might expect that clicking the “+3” button will increment the counter three times because it calls `setNumber(number + 1)` three times:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)import { useState } from 'react';
export default function Counter() { const [number, setNumber] = useState(0);
 return ( <> <h1>{number}</h1> <button onClick={() => { setNumber(number + 1); setNumber(number + 1); setNumber(number + 1); }}>+3</button> </> )}
/$

However, as you might recall from the previous section, [each render’s state values are fixed](https://react.dev/learn/state-as-a-snapshot#rendering-takes-a-snapshot-in-time), so the value of `number` inside the first render’s event handler is always `0`, no matter how many times you call `setNumber(1)`:

 $

```
setNumber(0 + 1);setNumber(0 + 1);setNumber(0 + 1);
```

/$

But there is one other factor at play here. **React waits untilallcode in the event handlers has run before processing your state updates.** This is why the re-render only happens *after* all these `setNumber()` calls.

This might remind you of a waiter taking an order at the restaurant. A waiter doesn’t run to the kitchen at the mention of your first dish! Instead, they let you finish your order, let you make changes to it, and even take orders from other people at the table.

 ![An elegant cursor at a restaurant places and order multiple times with React, playing the part of the waiter. After she calls setState() multiple times, the waiter writes down the last one she requested as her final order.](https://react.dev/images/docs/illustrations/i_react-batching.png)

Illustrated by  [Rachel Lee Nabors](https://nearestnabors.com/)

This lets you update multiple state variables—even from multiple components—without triggering too many [re-renders.](https://react.dev/learn/render-and-commit#re-renders-when-state-updates) But this also means that the UI won’t be updated until *after* your event handler, and any code in it, completes. This behavior, also known as **batching,** makes your React app run much faster. It also avoids dealing with confusing “half-finished” renders where only some of the variables have been updated.

**React does not batch acrossmultipleintentional events like clicks**—each click is handled separately. Rest assured that React only does batching when it’s generally safe to do. This ensures that, for example, if the first button click disables a form, the second click would not submit it again.

## Updating the same state multiple times before the next render

It is an uncommon use case, but if you would like to update the same state variable multiple times before the next render, instead of passing the *next state value* like `setNumber(number + 1)`, you can pass a *function* that calculates the next state based on the previous one in the queue, like `setNumber(n => n + 1)`. It is a way to tell React to “do something with the state value” instead of just replacing it.

Try incrementing the counter now:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(n => n + 1);
        setNumber(n => n + 1);
        setNumber(n => n + 1);
      }}>+3</button>
    </>
  )
}
```

/$

Here, `n => n + 1` is called an **updater function.** When you pass it to a state setter:

1. React queues this function to be processed after all the other code in the event handler has run.
2. During the next render, React goes through the queue and gives you the final updated state.

 $

```
setNumber(n => n + 1);setNumber(n => n + 1);setNumber(n => n + 1);
```

/$

Here’s how React works through these lines of code while executing the event handler:

1. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.
3. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.

When you call `useState` during the next render, React goes through the queue. The previous `number` state was `0`, so that’s what React passes to the first updater function as the `n` argument. Then React takes the return value of your previous updater function and passes it to the next updater as `n`, and so on:

| queued update | n | returns |
| --- | --- | --- |
| n => n + 1 | 0 | 0 + 1 = 1 |
| n => n + 1 | 1 | 1 + 1 = 2 |
| n => n + 1 | 2 | 2 + 1 = 3 |

React stores `3` as the final result and returns it from `useState`.

This is why clicking “+3” in the above example correctly increments the value by 3.

### What happens if you update state after replacing it

What about this event handler? What do you think `number` will be in the next render?

 $

```
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);}}>
```

/$ $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
      }}>Increase the number</button>
    </>
  )
}
```

/$

Here’s what this event handler tells React to do:

1. `setNumber(number + 5)`: `number` is `0`, so `setNumber(0 + 5)`. React adds *“replace with5”* to its queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is an updater function. React adds *that function* to its queue.

During the next render, React goes through the state queue:

| queued update | n | returns |
| --- | --- | --- |
| ”replace with5” | 0(unused) | 5 |
| n => n + 1 | 5 | 5 + 1 = 6 |

React stores `6` as the final result and returns it from `useState`.

### Note

You may have noticed that `setState(5)` actually works like `setState(n => 5)`, but `n` is unused!

### What happens if you replace state after updating it

Let’s try one more example. What do you think `number` will be in the next render?

 $

```
<button onClick={() => {  setNumber(number + 5);  setNumber(n => n + 1);  setNumber(42);}}>
```

/$ $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
        setNumber(42);
      }}>Increase the number</button>
    </>
  )
}
```

/$

Here’s how React works through these lines of code while executing this event handler:

1. `setNumber(number + 5)`: `number` is `0`, so `setNumber(0 + 5)`. React adds *“replace with5”* to its queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is an updater function. React adds *that function* to its queue.
3. `setNumber(42)`: React adds *“replace with42”* to its queue.

During the next render, React goes through the state queue:

| queued update | n | returns |
| --- | --- | --- |
| ”replace with5” | 0(unused) | 5 |
| n => n + 1 | 5 | 5 + 1 = 6 |
| ”replace with42” | 6(unused) | 42 |

Then React stores `42` as the final result and returns it from `useState`.

To summarize, here’s how you can think of what you’re passing to the `setNumber` state setter:

- **An updater function** (e.g. `n => n + 1`) gets added to the queue.
- **Any other value** (e.g. number `5`) adds “replace with `5`” to the queue, ignoring what’s already queued.

After the event handler completes, React will trigger a re-render. During the re-render, React will process the queue. Updater functions run during rendering, so **updater functions must bepure** and only *return* the result. Don’t try to set state from inside of them or run other side effects. In Strict Mode, React will run each updater function twice (but discard the second result) to help you find mistakes.

### Naming conventions

It’s common to name the updater function argument by the first letters of the corresponding state variable:

 $

```
setEnabled(e => !e);setLastName(ln => ln.reverse());setFriendCount(fc => fc * 2);
```

/$

If you prefer more verbose code, another common convention is to repeat the full state variable name, like `setEnabled(enabled => !enabled)`, or to use a prefix like `setEnabled(prevEnabled => !prevEnabled)`.

## Recap

- Setting state does not change the variable in the existing render, but it requests a new render.
- React processes state updates after event handlers have finished running. This is called batching.
- To update some state multiple times in one event, you can use `setNumber(n => n + 1)` updater function.

## Try out some challenges

#### Challenge1of2:Fix a request counter

You’re working on an art marketplace app that lets the user submit multiple orders for an art item at the same time. Each time the user presses the “Buy” button, the “Pending” counter should increase by one. After three seconds, the “Pending” counter should decrease, and the “Completed” counter should increase.

However, the “Pending” counter does not behave as intended. When you press “Buy”, it decreases to `-1` (which should not be possible!). And if you click fast twice, both counters seem to behave unpredictably.

Why does this happen? Fix both counters.

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function RequestTracker() {
  const [pending, setPending] = useState(0);
  const [completed, setCompleted] = useState(0);

  async function handleClick() {
    setPending(pending + 1);
    await delay(3000);
    setPending(pending - 1);
    setCompleted(completed + 1);
  }

  return (
    <>
      <h3>
        Pending: {pending}
      </h3>
      <h3>
        Completed: {completed}
      </h3>
      <button onClick={handleClick}>
        Buy
      </button>
    </>
  );
}

function delay(ms) {
  return new Promise(resolve => {
    setTimeout(resolve, ms);
  });
}
```

/$[PreviousState as a Snapshot](https://react.dev/learn/state-as-a-snapshot)[NextUpdating Objects in State](https://react.dev/learn/updating-objects-in-state)

---

# Debugging and Troubleshooting

[Learn React](https://react.dev/learn)[React Compiler](https://react.dev/learn/react-compiler)

# Debugging and Troubleshooting

This guide helps you identify and fix issues when using React Compiler. Learn how to debug compilation problems and resolve common issues.

### You will learn

- The difference between compiler errors and runtime issues
- Common patterns that break compilation
- Step-by-step debugging workflow

## Understanding Compiler Behavior

React Compiler is designed to handle code that follows the [Rules of React](https://react.dev/reference/rules). When it encounters code that might break these rules, it safely skips optimization rather than risk changing your app’s behavior.

### Compiler Errors vs Runtime Issues

**Compiler errors** occur at build time and prevent your code from compiling. These are rare because the compiler is designed to skip problematic code rather than fail.

**Runtime issues** occur when compiled code behaves differently than expected. Most of the time, if you encounter an issue with React Compiler, it’s a runtime issue. This typically happens when your code violates the Rules of React in subtle ways that the compiler couldn’t detect, and the compiler mistakenly compiled a component it should have skipped.

When debugging runtime issues, focus your efforts on finding Rules of React violations in the affected components that were not detected by the ESLint rule. The compiler relies on your code following these rules, and when they’re broken in ways it can’t detect, that’s when runtime problems occur.

## Common Breaking Patterns

One of the main ways React Compiler can break your app is if your code was written to rely on memoization for correctness. This means your app depends on specific values being memoized to work properly. Since the compiler may memoize differently than your manual approach, this can lead to unexpected behavior like effects over-firing, infinite loops, or missing updates.

Common scenarios where this occurs:

- **Effects that rely on referential equality** - When effects depend on objects or arrays maintaining the same reference across renders
- **Dependency arrays that need stable references** - When unstable dependencies cause effects to fire too often or create infinite loops
- **Conditional logic based on reference checks** - When code uses referential equality checks for caching or optimization

## Debugging Workflow

Follow these steps when you encounter issues:

### Compiler Build Errors

If you encounter a compiler error that unexpectedly breaks your build, this is likely a bug in the compiler. Report it to the [facebook/react](https://github.com/facebook/react/issues) repository with:

- The error message
- The code that caused the error
- Your React and compiler versions

### Runtime Issues

For runtime behavior issues:

### 1. Temporarily Disable Compilation

Use `"use no memo"` to isolate whether an issue is compiler-related:

 $

```
function ProblematicComponent() {  "use no memo"; // Skip compilation for this component  // ... rest of component}
```

/$

If the issue disappears, it’s likely related to a Rules of React violation.

You can also try removing manual memoization (useMemo, useCallback, memo) from the problematic component to verify that your app works correctly without any memoization. If the bug still occurs when all memoization is removed, you have a Rules of React violation that needs to be fixed.

### 2. Fix Issues Step by Step

1. Identify the root cause (often memoization-for-correctness)
2. Test after each fix
3. Remove `"use no memo"` once fixed
4. Verify the component shows the ✨ badge in React DevTools

## Reporting Compiler Bugs

If you believe you’ve found a compiler bug:

1. **Verify it’s not a Rules of React violation** - Check with ESLint
2. **Create a minimal reproduction** - Isolate the issue in a small example
3. **Test without the compiler** - Confirm the issue only occurs with compilation
4. **File anissue**:
  - React and compiler versions
  - Minimal reproduction code
  - Expected vs actual behavior
  - Any error messages

## Next Steps

- Review the [Rules of React](https://react.dev/reference/rules) to prevent issues
- Check the [incremental adoption guide](https://react.dev/learn/react-compiler/incremental-adoption) for gradual rollout strategies

[PreviousIncremental Adoption](https://react.dev/learn/react-compiler/incremental-adoption)

---

# Incremental Adoption

[Learn React](https://react.dev/learn)[React Compiler](https://react.dev/learn/react-compiler)

# Incremental Adoption

React Compiler can be adopted incrementally, allowing you to try it on specific parts of your codebase first. This guide shows you how to gradually roll out the compiler in existing projects.

### You will learn

- Why incremental adoption is recommended
- Using Babel overrides for directory-based adoption
- Using the “use memo” directive for opt-in compilation
- Using the “use no memo” directive to exclude components
- Runtime feature flags with gating
- Monitoring your adoption progress

## Why Incremental Adoption?

React Compiler is designed to optimize your entire codebase automatically, but you don’t have to adopt it all at once. Incremental adoption gives you control over the rollout process, letting you test the compiler on small parts of your app before expanding to the rest.

Starting small helps you build confidence in the compiler’s optimizations. You can verify that your app behaves correctly with compiled code, measure performance improvements, and identify any edge cases specific to your codebase. This approach is especially valuable for production applications where stability is critical.

Incremental adoption also makes it easier to address any Rules of React violations the compiler might find. Instead of fixing violations across your entire codebase at once, you can tackle them systematically as you expand compiler coverage. This keeps the migration manageable and reduces the risk of introducing bugs.

By controlling which parts of your code get compiled, you can also run A/B tests to measure the real-world impact of the compiler’s optimizations. This data helps you make informed decisions about full adoption and demonstrates the value to your team.

## Approaches to Incremental Adoption

There are three main approaches to adopt React Compiler incrementally:

1. **Babel overrides** - Apply the compiler to specific directories
2. **Opt-in with “use memo”** - Only compile components that explicitly opt in
3. **Runtime gating** - Control compilation with feature flags

All approaches allow you to test the compiler on specific parts of your application before full rollout.

## Directory-Based Adoption with Babel Overrides

Babel’s `overrides` option lets you apply different plugins to different parts of your codebase. This is ideal for gradually adopting React Compiler directory by directory.

### Basic Configuration

Start by applying the compiler to a specific directory:

 $

```
// babel.config.jsmodule.exports = {  plugins: [    // Global plugins that apply to all files  ],  overrides: [    {      test: './src/modern/**/*.{js,jsx,ts,tsx}',      plugins: [        'babel-plugin-react-compiler'      ]    }  ]};
```

/$

### Expanding Coverage

As you gain confidence, add more directories:

 $

```
// babel.config.jsmodule.exports = {  plugins: [    // Global plugins  ],  overrides: [    {      test: ['./src/modern/**/*.{js,jsx,ts,tsx}', './src/features/**/*.{js,jsx,ts,tsx}'],      plugins: [        'babel-plugin-react-compiler'      ]    },    {      test: './src/legacy/**/*.{js,jsx,ts,tsx}',      plugins: [        // Different plugins for legacy code      ]    }  ]};
```

/$

### With Compiler Options

You can also configure compiler options per override:

 $

```
// babel.config.jsmodule.exports = {  plugins: [],  overrides: [    {      test: './src/experimental/**/*.{js,jsx,ts,tsx}',      plugins: [        ['babel-plugin-react-compiler', {          // options ...        }]      ]    },    {      test: './src/production/**/*.{js,jsx,ts,tsx}',      plugins: [        ['babel-plugin-react-compiler', {          // options ...        }]      ]    }  ]};
```

/$

## Opt-in Mode with “use memo”

For maximum control, you can use `compilationMode: 'annotation'` to only compile components and hooks that explicitly opt in with the `"use memo"` directive.

### Note

This approach gives you fine-grained control over individual components and hooks. It’s useful when you want to test the compiler on specific components without affecting entire directories.

### Annotation Mode Configuration

 $

```
// babel.config.jsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'annotation',    }],  ],};
```

/$

### Using the Directive

Add `"use memo"` at the beginning of functions you want to compile:

 $

```
function TodoList({ todos }) {  "use memo"; // Opt this component into compilation  const sortedTodos = todos.slice().sort();  return (    <ul>      {sortedTodos.map(todo => (        <TodoItem key={todo.id} todo={todo} />      ))}    </ul>  );}function useSortedData(data) {  "use memo"; // Opt this hook into compilation  return data.slice().sort();}
```

/$

With `compilationMode: 'annotation'`, you must:

- Add `"use memo"` to every component you want optimized
- Add `"use memo"` to every custom hook
- Remember to add it to new components

This gives you precise control over which components are compiled while you evaluate the compiler’s impact.

## Runtime Feature Flags with Gating

The `gating` option enables you to control compilation at runtime using feature flags. This is useful for running A/B tests or gradually rolling out the compiler based on user segments.

### How Gating Works

The compiler wraps optimized code in a runtime check. If the gate returns `true`, the optimized version runs. Otherwise, the original code runs.

### Gating Configuration

 $

```
// babel.config.jsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      gating: {        source: 'ReactCompilerFeatureFlags',        importSpecifierName: 'isCompilerEnabled',      },    }],  ],};
```

/$

### Implementing the Feature Flag

Create a module that exports your gating function:

 $

```
// ReactCompilerFeatureFlags.jsexport function isCompilerEnabled() {  // Use your feature flag system  return getFeatureFlag('react-compiler-enabled');}
```

/$

## Troubleshooting Adoption

If you encounter issues during adoption:

1. Use `"use no memo"` to temporarily exclude problematic components
2. Check the [debugging guide](https://react.dev/learn/react-compiler/debugging) for common issues
3. Fix Rules of React violations identified by the ESLint plugin
4. Consider using `compilationMode: 'annotation'` for more gradual adoption

## Next Steps

- Read the [configuration guide](https://react.dev/reference/react-compiler/configuration) for more options
- Learn about [debugging techniques](https://react.dev/learn/react-compiler/debugging)
- Check the [API reference](https://react.dev/reference/react-compiler/configuration) for all compiler options

[PreviousInstallation](https://react.dev/learn/react-compiler/installation)[NextDebugging and Troubleshooting](https://react.dev/learn/react-compiler/debugging)

---

# Installation

[Learn React](https://react.dev/learn)[React Compiler](https://react.dev/learn/react-compiler)

# Installation

This guide will help you install and configure React Compiler in your React application.

### You will learn

- How to install React Compiler
- Basic configuration for different build tools
- How to verify your setup is working

## Prerequisites

React Compiler is designed to work best with React 19, but it also supports React 17 and 18. Learn more about [React version compatibility](https://react.dev/reference/react-compiler/target).

## Installation

Install React Compiler as a `devDependency`:

  Terminal

```
npm install -D babel-plugin-react-compiler@latest
```

Or with Yarn:

  Terminal

```
yarn add -D babel-plugin-react-compiler@latest
```

Or with pnpm:

  Terminal

```
pnpm install -D babel-plugin-react-compiler@latest
```

## Basic Setup

React Compiler is designed to work by default without any configuration. However, if you need to configure it in special circumstances (for example, to target React versions below 19), refer to the [compiler options reference](https://react.dev/reference/react-compiler/configuration).

The setup process depends on your build tool. React Compiler includes a Babel plugin that integrates with your build pipeline.

### Pitfall

React Compiler must run **first** in your Babel plugin pipeline. The compiler needs the original source information for proper analysis, so it must process your code before other transformations.

### Babel

Create or update your `babel.config.js`:

 $

```
module.exports = {  plugins: [    'babel-plugin-react-compiler', // must run first!    // ... other plugins  ],  // ... other config};
```

/$

### Vite

If you use Vite, you can add the plugin to vite-plugin-react:

 $

```
// vite.config.jsimport { defineConfig } from 'vite';import react from '@vitejs/plugin-react';export default defineConfig({  plugins: [    react({      babel: {        plugins: ['babel-plugin-react-compiler'],      },    }),  ],});
```

/$

Alternatively, if you prefer a separate Babel plugin for Vite:

  Terminal

```
npm install -D vite-plugin-babel
```

 $

```
// vite.config.jsimport babel from 'vite-plugin-babel';import { defineConfig } from 'vite';import react from '@vitejs/plugin-react';export default defineConfig({  plugins: [    react(),    babel({      babelConfig: {        plugins: ['babel-plugin-react-compiler'],      },    }),  ],});
```

/$

### Next.js

Please refer to the [Next.js docs](https://nextjs.org/docs/app/api-reference/next-config-js/reactCompiler) for more information.

### React Router

Install `vite-plugin-babel`, and add the compiler’s Babel plugin to it:

  Terminal

```
npm install vite-plugin-babel
```

 $

```
// vite.config.jsimport { defineConfig } from "vite";import babel from "vite-plugin-babel";import { reactRouter } from "@react-router/dev/vite";const ReactCompilerConfig = { /* ... */ };export default defineConfig({  plugins: [    reactRouter(),    babel({      filter: /\.[jt]sx?$/,      babelConfig: {        presets: ["@babel/preset-typescript"], // if you use TypeScript        plugins: [          ["babel-plugin-react-compiler", ReactCompilerConfig],        ],      },    }),  ],});
```

/$

### Webpack

A community webpack loader is [now available here](https://github.com/SukkaW/react-compiler-webpack).

### Expo

Please refer to [Expo’s docs](https://docs.expo.dev/guides/react-compiler/) to enable and use the React Compiler in Expo apps.

### Metro (React Native)

React Native uses Babel via Metro, so refer to the [Usage with Babel](#babel) section for installation instructions.

### Rspack

Please refer to [Rspack’s docs](https://rspack.dev/guide/tech/react#react-compiler) to enable and use the React Compiler in Rspack apps.

### Rsbuild

Please refer to [Rsbuild’s docs](https://rsbuild.dev/guide/framework/react#react-compiler) to enable and use the React Compiler in Rsbuild apps.

## ESLint Integration

React Compiler includes an ESLint rule that helps identify code that can’t be optimized. When the ESLint rule reports an error, it means the compiler will skip optimizing that specific component or hook. This is safe: the compiler will continue optimizing other parts of your codebase. You don’t need to fix all violations immediately. Address them at your own pace to gradually increase the number of optimized components.

Install the ESLint plugin:

  Terminal

```
npm install -D eslint-plugin-react-hooks@latest
```

If you haven’t already configured eslint-plugin-react-hooks, follow the [installation instructions in the readme](https://github.com/facebook/react/blob/main/packages/eslint-plugin-react-hooks/README.md#installation). The compiler rules are available in the `recommended-latest` preset.

The ESLint rule will:

- Identify violations of the [Rules of React](https://react.dev/reference/rules)
- Show which components can’t be optimized
- Provide helpful error messages for fixing issues

## Verify Your Setup

After installation, verify that React Compiler is working correctly.

### Check React DevTools

Components optimized by React Compiler will show a “Memo ✨” badge in React DevTools:

1. Install the [React Developer Tools](https://react.dev/learn/react-developer-tools) browser extension
2. Open your app in development mode
3. Open React DevTools
4. Look for the ✨ emoji next to component names

If the compiler is working:

- Components will show a “Memo ✨” badge in React DevTools
- Expensive calculations will be automatically memoized
- No manual `useMemo` is required

### Check Build Output

You can also verify the compiler is running by checking your build output. The compiled code will include automatic memoization logic that the compiler adds automatically.

 $

```
import { c as _c } from "react/compiler-runtime";export default function MyApp() {  const $ = _c(1);  let t0;  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {    t0 = <div>Hello World</div>;    $[0] = t0;  } else {    t0 = $[0];  }  return t0;}
```

/$

## Troubleshooting

### Opting out specific components

If a component is causing issues after compilation, you can temporarily opt it out using the `"use no memo"` directive:

 $

```
function ProblematicComponent() {  "use no memo";  // Component code here}
```

/$

This tells the compiler to skip optimization for this specific component. You should fix the underlying issue and remove the directive once resolved.

For more troubleshooting help, see the [debugging guide](https://react.dev/learn/react-compiler/debugging).

## Next Steps

Now that you have React Compiler installed, learn more about:

- [React version compatibility](https://react.dev/reference/react-compiler/target) for React 17 and 18
- [Configuration options](https://react.dev/reference/react-compiler/configuration) to customize the compiler
- [Incremental adoption strategies](https://react.dev/learn/react-compiler/incremental-adoption) for existing codebases
- [Debugging techniques](https://react.dev/learn/react-compiler/debugging) for troubleshooting issues
- [Compiling Libraries guide](https://react.dev/reference/react-compiler/compiling-libraries) for compiling your React library

[PreviousIntroduction](https://react.dev/learn/react-compiler/introduction)[NextIncremental Adoption](https://react.dev/learn/react-compiler/incremental-adoption)

---

# Introduction

[Learn React](https://react.dev/learn)[React Compiler](https://react.dev/learn/react-compiler)

# Introduction

React Compiler is a new build-time tool that automatically optimizes your React app. It works with plain JavaScript, and understands the [Rules of React](https://react.dev/reference/rules), so you don’t need to rewrite any code to use it.

### You will learn

- What React Compiler does
- Getting started with the compiler
- Incremental adoption strategies
- Debugging and troubleshooting when things go wrong
- Using the compiler on your React library

## What does React Compiler do?

React Compiler automatically optimizes your React application at build time. React is often fast enough without optimization, but sometimes you need to manually memoize components and values to keep your app responsive. This manual memoization is tedious, easy to get wrong, and adds extra code to maintain. React Compiler does this optimization automatically for you, freeing you from this mental burden so you can focus on building features.

### Before React Compiler

Without the compiler, you need to manually memoize components and values to optimize re-renders:

 $

```
import { useMemo, useCallback, memo } from 'react';const ExpensiveComponent = memo(function ExpensiveComponent({ data, onClick }) {  const processedData = useMemo(() => {    return expensiveProcessing(data);  }, [data]);  const handleClick = useCallback((item) => {    onClick(item.id);  }, [onClick]);  return (    <div>      {processedData.map(item => (        <Item key={item.id} onClick={() => handleClick(item)} />      ))}    </div>  );});
```

/$

### Note

This manual memoization has a subtle bug that breaks memoization:

$

```
<Item key={item.id} onClick={() => handleClick(item)} />
```

/$

Even though `handleClick` is wrapped in `useCallback`, the arrow function `() => handleClick(item)` creates a new function every time the component renders. This means that `Item` will always receive a new `onClick` prop, breaking memoization.

React Compiler is able to optimize this correctly with or without the arrow function, ensuring that `Item` only re-renders when `props.onClick` changes.

### After React Compiler

With React Compiler, you write the same code without manual memoization:

 $

```
function ExpensiveComponent({ data, onClick }) {  const processedData = expensiveProcessing(data);  const handleClick = (item) => {    onClick(item.id);  };  return (    <div>      {processedData.map(item => (        <Item key={item.id} onClick={() => handleClick(item)} />      ))}    </div>  );}
```

/$

*See this example in the React Compiler Playground*

React Compiler automatically applies the optimal memoization, ensuring your app only re-renders when necessary.

##### Deep Dive

#### What kind of memoization does React Compiler add?

React Compiler’s automatic memoization is primarily focused on **improving update performance** (re-rendering existing components), so it focuses on these two use cases:

1. **Skipping cascading re-rendering of components**
  - Re-rendering `<Parent />` causes many components in its component tree to re-render, even though only `<Parent />` has changed
2. **Skipping expensive calculations from outside of React**
  - For example, calling `expensivelyProcessAReallyLargeArrayOfObjects()` inside of your component or hook that needs that data

#### Optimizing Re-renders

React lets you express your UI as a function of their current state (more concretely: their props, state, and context). In its current implementation, when a component’s state changes, React will re-render that component *and all of its children* — unless you have applied some form of manual memoization with `useMemo()`, `useCallback()`, or `React.memo()`. For example, in the following example, `<MessageButton>` will re-render whenever `<FriendList>`’s state changes:

$

```
function FriendList({ friends }) {  const onlineCount = useFriendOnlineCount();  if (friends.length === 0) {    return <NoFriends />;  }  return (    <div>      <span>{onlineCount} online</span>      {friends.map((friend) => (        <FriendListCard key={friend.id} friend={friend} />      ))}      <MessageButton />    </div>  );}
```

/$

[See this example in the React Compiler Playground](https://playground.react.dev/#N4Igzg9grgTgxgUxALhAMygOzgFwJYSYAEAYjHgpgCYAyeYOAFMEWuZVWEQL4CURwADrEicQgyKEANnkwIAwtEw4iAXiJQwCMhWoB5TDLmKsTXgG5hRInjRFGbXZwB0UygHMcACzWr1ABn4hEWsYBBxYYgAeADkIHQ4uAHoAPksRbisiMIiYYkYs6yiqPAA3FMLrIiiwAAcAQ0wU4GlZBSUcbklDNqikusaKkKrgR0TnAFt62sYHdmp+VRT7SqrqhOo6Bnl6mCoiAGsEAE9VUfmqZzwqLrHqM7ubolTVol5eTOGigFkEMDB6u4EAAhKA4HCEZ5DNZ9ErlLIWYTcEDcIA)

React Compiler automatically applies the equivalent of manual memoization, ensuring that only the relevant parts of an app re-render as state changes, which is sometimes referred to as “fine-grained reactivity”. In the above example, React Compiler determines that the return value of `<FriendListCard />` can be reused even as `friends` changes, and can avoid recreating this JSX *and* avoid re-rendering `<MessageButton>` as the count changes.

#### Expensive calculations also get memoized

React Compiler can also automatically memoize expensive calculations used during rendering:

$

```
// **Not** memoized by React Compiler, since this is not a component or hookfunction expensivelyProcessAReallyLargeArrayOfObjects() { /* ... */ }// Memoized by React Compiler since this is a componentfunction TableContainer({ items }) {  // This function call would be memoized:  const data = expensivelyProcessAReallyLargeArrayOfObjects(items);  // ...}
```

/$

[See this example in the React Compiler Playground](https://playground.react.dev/#N4Igzg9grgTgxgUxALhAejQAgFTYHIQAuumAtgqRAJYBeCAJpgEYCemASggIZyGYDCEUgAcqAGwQwANJjBUAdokyEAFlTCZ1meUUxdMcIcIjyE8vhBiYVECAGsAOvIBmURYSonMCAB7CzcgBuCGIsAAowEIhgYACCnFxioQAyXDAA5gixMDBcLADyzvlMAFYIvGAAFACUmMCYaNiYAHStOFgAvk5OGJgAshTUdIysHNy8AkbikrIKSqpaWvqGIiZmhE6u7p7ymAAqXEwSguZcCpKV9VSEFBodtcBOmAYmYHz0XIT6ALzefgFUYKhCJRBAxeLcJIsVIZLI5PKFYplCqVa63aoAbm6u0wMAQhFguwAPPRAQA+YAfL4dIloUmBMlODogDpAA)

However, if `expensivelyProcessAReallyLargeArrayOfObjects` is truly an expensive function, you may want to consider implementing its own memoization outside of React, because:

- React Compiler only memoizes React components and hooks, not every function
- React Compiler’s memoization is not shared across multiple components or hooks

So if `expensivelyProcessAReallyLargeArrayOfObjects` was used in many different components, even if the same exact items were passed down, that expensive calculation would be run repeatedly. We recommend [profiling](https://react.dev/reference/react/useMemo#how-to-tell-if-a-calculation-is-expensive) first to see if it really is that expensive before making code more complicated.

## Should I try out the compiler?

We encourage everyone to start using React Compiler. While the compiler is still an optional addition to React today, in the future some features may require the compiler in order to fully work.

### Is it safe to use?

React Compiler is now stable and has been tested extensively in production. While it has been used in production at companies like Meta, rolling out the compiler to production for your app will depend on the health of your codebase and how well you’ve followed the [Rules of React](https://react.dev/reference/rules).

## What build tools are supported?

React Compiler can be installed across [several build tools](https://react.dev/learn/react-compiler/installation) such as Babel, Vite, Metro, and Rsbuild.

React Compiler is primarily a light Babel plugin wrapper around the core compiler, which was designed to be decoupled from Babel itself. While the initial stable version of the compiler will remain primarily a Babel plugin, we are working with the swc and [oxc](https://github.com/oxc-project/oxc/issues/10048) teams to build first class support for React Compiler so you won’t have to add Babel back to your build pipelines in the future.

Next.js users can enable the swc-invoked React Compiler by using [v15.3.1](https://github.com/vercel/next.js/releases/tag/v15.3.1) and up.

## What should I do about useMemo, useCallback, and React.memo?

By default, React Compiler will memoize your code based on its analysis and heuristics. In most cases, this memoization will be as precise, or moreso, than what you may have written.

However, in some cases developers may need more control over memoization. The `useMemo` and `useCallback` hooks can continue to be used with React Compiler as an escape hatch to provide control over which values are memoized. A common use-case for this is if a memoized value is used as an effect dependency, in order to ensure that an effect does not fire repeatedly even when its dependencies do not meaningfully change.

For new code, we recommend relying on the compiler for memoization and using `useMemo`/`useCallback` where needed to achieve precise control.

For existing code, we recommend either leaving existing memoization in place (removing it can change compilation output) or carefully testing before removing the memoization.

## Try React Compiler

This section will help you get started with React Compiler and understand how to use it effectively in your projects.

- **Installation** - Install React Compiler and configure it for your build tools
- **React Version Compatibility** - Support for React 17, 18, and 19
- **Configuration** - Customize the compiler for your specific needs
- **Incremental Adoption** - Strategies for gradually rolling out the compiler in existing codebases
- **Debugging and Troubleshooting** - Identify and fix issues when using the compiler
- **Compiling Libraries** - Best practices for shipping compiled code
- **API Reference** - Detailed documentation of all configuration options

## Additional resources

In addition to these docs, we recommend checking the [React Compiler Working Group](https://github.com/reactwg/react-compiler) for additional information and discussion about the compiler.

[PreviousReact Compiler](https://react.dev/learn/react-compiler)[NextInstallation](https://react.dev/learn/react-compiler/installation)

---

# React Compiler

[Learn React](https://react.dev/learn)

# React Compiler

## Introduction

Learn [what React Compiler does](https://react.dev/learn/react-compiler/introduction) and how it automatically optimizes your React application by handling memoization for you, eliminating the need for manual `useMemo`, `useCallback`, and `React.memo`.

## Installation

Get started with [installing React Compiler](https://react.dev/learn/react-compiler/installation) and learn how to configure it with your build tools.

## Incremental Adoption

Learn [strategies for gradually adopting React Compiler](https://react.dev/learn/react-compiler/incremental-adoption) in your existing codebase if you’re not ready to enable it everywhere yet.

## Debugging and Troubleshooting

When things don’t work as expected, use our [debugging guide](https://react.dev/learn/react-compiler/debugging) to understand the difference between compiler errors and runtime issues, identify common breaking patterns, and follow a systematic debugging workflow.

## Configuration and Reference

For detailed configuration options and API reference:

- [Configuration Options](https://react.dev/reference/react-compiler/configuration) - All compiler configuration options including React version compatibility
- [Directives](https://react.dev/reference/react-compiler/directives) - Function-level compilation control
- [Compiling Libraries](https://react.dev/reference/react-compiler/compiling-libraries) - Shipping pre-compiled libraries

## Additional resources

In addition to these docs, we recommend checking the [React Compiler Working Group](https://github.com/reactwg/react-compiler) for additional information and discussion about the compiler.

[PreviousReact Developer Tools](https://react.dev/learn/react-developer-tools)[NextIntroduction](https://react.dev/learn/react-compiler/introduction)

---

# React Developer Tools

[Learn React](https://react.dev/learn)[Setup](https://react.dev/learn/setup)

# React Developer Tools

Use React Developer Tools to inspect React [components](https://react.dev/learn/your-first-component), edit [props](https://react.dev/learn/passing-props-to-a-component) and [state](https://react.dev/learn/state-a-components-memory), and identify performance problems.

### You will learn

- How to install React Developer Tools

## Browser extension

The easiest way to debug websites built with React is to install the React Developer Tools browser extension. It is available for several popular browsers:

- [Install forChrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en)
- [Install forFirefox](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)
- [Install forEdge](https://microsoftedge.microsoft.com/addons/detail/react-developer-tools/gpphkfbcpidddadnkolkpfckpihlkkil)

Now, if you visit a website **built with React,** you will see the *Components* and *Profiler* panels.

 ![React Developer Tools extension](https://react.dev/images/docs/react-devtools-extension.png)

### Safari and other browsers

For other browsers (for example, Safari), install the [react-devtools](https://www.npmjs.com/package/react-devtools) npm package:

 $

```
# Yarnyarn global add react-devtools# Npmnpm install -g react-devtools
```

/$

Next open the developer tools from the terminal:

 $

```
react-devtools
```

/$

Then connect your website by adding the following `<script>` tag to the beginning of your website’s `<head>`:

 $

```
<html>  <head>    <script src="http://localhost:8097"></script>
```

/$

Reload your website in the browser now to view it in developer tools.

 ![React Developer Tools standalone](https://react.dev/images/docs/react-devtools-standalone.png)

## Mobile (React Native)

To inspect apps built with [React Native](https://reactnative.dev/), you can use [React Native DevTools](https://reactnative.dev/docs/react-native-devtools), the built-in debugger that deeply integrates React Developer Tools. All features work identically to the browser extension, including native element highlighting and selection.

[Learn more about debugging in React Native.](https://reactnative.dev/docs/debugging)

> For versions of React Native earlier than 0.76, please use the standalone build of React DevTools by following the [Safari and other browsers](#safari-and-other-browsers) guide above.

[PreviousUsing TypeScript](https://react.dev/learn/typescript)[NextReact Compiler](https://react.dev/learn/react-compiler)
