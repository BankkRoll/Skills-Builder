# use no memo and more

# use no memo

[API Reference](https://react.dev/reference/react)[Directives](https://react.dev/reference/react-compiler/directives)

# use no memo

`"use no memo"` prevents a function from being optimized by React Compiler.

- [Reference](#reference)
  - ["use no memo"](#use-no-memo)
  - [How"use no memo"opts-out of optimization](#how-use-no-memo-opts-out)
  - [When to use"use no memo"](#when-to-use)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
  - [Directive not preventing compilation](#not-preventing)
  - [Best practices](#best-practices)
  - [See also](#see-also)

---

## Reference

### "use no memo"

Add `"use no memo"` at the beginning of a function to prevent React Compiler optimization.

 $

```
function MyComponent() {  "use no memo";  // ...}
```

/$

When a function contains `"use no memo"`, the React Compiler will skip it entirely during optimization. This is useful as a temporary escape hatch when debugging or when dealing with code that doesn’t work correctly with the compiler.

#### Caveats

- `"use no memo"` must be at the very beginning of a function body, before any imports or other code (comments are OK).
- The directive must be written with double or single quotes, not backticks.
- The directive must exactly match `"use no memo"` or its alias `"use no forget"`.
- This directive takes precedence over all compilation modes and other directives.
- It’s intended as a temporary debugging tool, not a permanent solution.

### How"use no memo"opts-out of optimization

React Compiler analyzes your code at build time to apply optimizations. `"use no memo"` creates an explicit boundary that tells the compiler to skip a function entirely.

This directive takes precedence over all other settings:

- In `all` mode: The function is skipped despite the global setting
- In `infer` mode: The function is skipped even if heuristics would optimize it

The compiler treats these functions as if the React Compiler wasn’t enabled, leaving them exactly as written.

### When to use"use no memo"

`"use no memo"` should be used sparingly and temporarily. Common scenarios include:

#### Debugging compiler issues

When you suspect the compiler is causing issues, temporarily disable optimization to isolate the problem:

 $

```
function ProblematicComponent({ data }) {  "use no memo"; // TODO: Remove after fixing issue #123  // Rules of React violations that weren't statically detected  // ...}
```

/$

#### Third-party library integration

When integrating with libraries that might not be compatible with the compiler:

 $

```
function ThirdPartyWrapper() {  "use no memo";  useThirdPartyHook(); // Has side effects that compiler might optimize incorrectly  // ...}
```

/$

---

## Usage

The `"use no memo"` directive is placed at the beginning of a function body to prevent React Compiler from optimizing that function:

 $

```
function MyComponent() {  "use no memo";  // Function body}
```

/$

The directive can also be placed at the top of a file to affect all functions in that module:

 $

```
"use no memo";// All functions in this file will be skipped by the compiler
```

/$

`"use no memo"` at the function level overrides the module level directive.

---

## Troubleshooting

### Directive not preventing compilation

If `"use no memo"` isn’t working:

 $

```
// ❌ Wrong - directive after codefunction Component() {  const data = getData();  "use no memo"; // Too late!}// ✅ Correct - directive firstfunction Component() {  "use no memo";  const data = getData();}
```

/$

Also check:

- Spelling - must be exactly `"use no memo"`
- Quotes - must use single or double quotes, not backticks

### Best practices

**Always document why** you’re disabling optimization:

 $

```
// ✅ Good - clear explanation and trackingfunction DataProcessor() {  "use no memo"; // TODO: Remove after fixing rule of react violation  // ...}// ❌ Bad - no explanationfunction Mystery() {  "use no memo";  // ...}
```

/$

### See also

- ["use memo"](https://react.dev/reference/react-compiler/directives/use-memo) - Opt into compilation
- [React Compiler](https://react.dev/learn/react-compiler) - Getting started guide

[Previous"use memo"](https://react.dev/reference/react-compiler/directives/use-memo)[NextCompiling Libraries](https://react.dev/reference/react-compiler/compiling-libraries)

---

# Directives

[API Reference](https://react.dev/reference/react)

# Directives

React Compiler directives are special string literals that control whether specific functions are compiled.

 $

```
function MyComponent() {  "use memo"; // Opt this component into compilation  return <div>{/* ... */}</div>;}
```

/$

- [Overview](#overview)
  - [Available directives](#available-directives)
  - [Quick comparison](#quick-comparison)
- [Usage](#usage)
  - [Function-level directives](#function-level)
  - [Module-level directives](#module-level)
  - [Compilation modes interaction](#compilation-modes)
- [Best practices](#best-practices)
  - [Use directives sparingly](#use-sparingly)
  - [Document directive usage](#document-usage)
  - [Plan for removal](#plan-removal)
- [Common patterns](#common-patterns)
  - [Gradual adoption](#gradual-adoption)
- [Troubleshooting](#troubleshooting)
  - [Common issues](#common-issues)
- [See also](#see-also)

---

## Overview

React Compiler directives provide fine-grained control over which functions are optimized by the compiler. They are string literals placed at the beginning of a function body or at the top of a module.

### Available directives

- **"use memo"** - Opts a function into compilation
- **"use no memo"** - Opts a function out of compilation

### Quick comparison

| Directive | Purpose | When to use |
| --- | --- | --- |
| "use memo" | Force compilation | When usingannotationmode or to overrideinfermode heuristics |
| "use no memo" | Prevent compilation | Debugging issues or working with incompatible code |

---

## Usage

### Function-level directives

Place directives at the beginning of a function to control its compilation:

 $

```
// Opt into compilationfunction OptimizedComponent() {  "use memo";  return <div>This will be optimized</div>;}// Opt out of compilationfunction UnoptimizedComponent() {  "use no memo";  return <div>This won't be optimized</div>;}
```

/$

### Module-level directives

Place directives at the top of a file to affect all functions in that module:

 $

```
// At the very top of the file"use memo";// All functions in this file will be compiledfunction Component1() {  return <div>Compiled</div>;}function Component2() {  return <div>Also compiled</div>;}// Can be overridden at function levelfunction Component3() {  "use no memo"; // This overrides the module directive  return <div>Not compiled</div>;}
```

/$

### Compilation modes interaction

Directives behave differently depending on your [compilationMode](https://react.dev/reference/react-compiler/compilationMode):

- **annotationmode**: Only functions with `"use memo"` are compiled
- **infermode**: Compiler decides what to compile, directives override decisions
- **allmode**: Everything is compiled, `"use no memo"` can exclude specific functions

---

## Best practices

### Use directives sparingly

Directives are escape hatches. Prefer configuring the compiler at the project level:

 $

```
// ✅ Good - project-wide configuration{  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'infer'    }]  ]}// ⚠️ Use directives only when neededfunction SpecialCase() {  "use no memo"; // Document why this is needed  // ...}
```

/$

### Document directive usage

Always explain why a directive is used:

 $

```
// ✅ Good - clear explanationfunction DataGrid() {  "use no memo"; // TODO: Remove after fixing issue with dynamic row heights (JIRA-123)  // Complex grid implementation}// ❌ Bad - no explanationfunction Mystery() {  "use no memo";  // ...}
```

/$

### Plan for removal

Opt-out directives should be temporary:

1. Add the directive with a TODO comment
2. Create a tracking issue
3. Fix the underlying problem
4. Remove the directive

 $

```
function TemporaryWorkaround() {  "use no memo"; // TODO: Remove after upgrading ThirdPartyLib to v2.0  return <ThirdPartyComponent />;}
```

/$

---

## Common patterns

### Gradual adoption

When adopting the React Compiler in a large codebase:

 $

```
// Start with annotation mode{  compilationMode: 'annotation'}// Opt in stable componentsfunction StableComponent() {  "use memo";  // Well-tested component}// Later, switch to infer mode and opt out problematic onesfunction ProblematicComponent() {  "use no memo"; // Fix issues before removing  // ...}
```

/$

---

## Troubleshooting

For specific issues with directives, see the troubleshooting sections in:

- ["use memo"troubleshooting](https://react.dev/reference/react-compiler/directives/use-memo#troubleshooting)
- ["use no memo"troubleshooting](https://react.dev/reference/react-compiler/directives/use-no-memo#troubleshooting)

### Common issues

1. **Directive ignored**: Check placement (must be first) and spelling
2. **Compilation still happens**: Check `ignoreUseNoForget` setting
3. **Module directive not working**: Ensure it’s before all imports

---

## See also

- [compilationMode](https://react.dev/reference/react-compiler/compilationMode) - Configure how the compiler chooses what to optimize
- [Configuration](https://react.dev/reference/react-compiler/configuration) - Full compiler configuration options
- [React Compiler documentation](https://react.dev/learn/react-compiler) - Getting started guide

[Previoustarget](https://react.dev/reference/react-compiler/target)[Next"use memo"](https://react.dev/reference/react-compiler/directives/use-memo)

---

# gating

[API Reference](https://react.dev/reference/react)[Configuration](https://react.dev/reference/react-compiler/configuration)

# gating

The `gating` option enables conditional compilation, allowing you to control when optimized code is used at runtime.

 $

```
{  gating: {    source: 'my-feature-flags',    importSpecifierName: 'shouldUseCompiler'  }}
```

/$

- [Reference](#reference)
  - [gating](#gating)
- [Usage](#usage)
  - [Basic feature flag setup](#basic-setup)
- [Troubleshooting](#troubleshooting)
  - [Feature flag not working](#flag-not-working)
  - [Import errors](#import-errors)

---

## Reference

### gating

Configures runtime feature flag gating for compiled functions.

#### Type

 $

```
{  source: string;  importSpecifierName: string;} | null
```

/$

#### Default value

`null`

#### Properties

- **source**: Module path to import the feature flag from
- **importSpecifierName**: Name of the exported function to import

#### Caveats

- The gating function must return a boolean
- Both compiled and original versions increase bundle size
- The import is added to every file with compiled functions

---

## Usage

### Basic feature flag setup

1. Create a feature flag module:

 $

```
// src/utils/feature-flags.jsexport function shouldUseCompiler() {  // your logic here  return getFeatureFlag('react-compiler-enabled');}
```

/$

1. Configure the compiler:

 $

```
{  gating: {    source: './src/utils/feature-flags',    importSpecifierName: 'shouldUseCompiler'  }}
```

/$

1. The compiler generates gated code:

 $

```
// Inputfunction Button(props) {  return <button>{props.label}</button>;}// Output (simplified)import { shouldUseCompiler } from './src/utils/feature-flags';const Button = shouldUseCompiler()  ? function Button_optimized(props) { /* compiled version */ }  : function Button_original(props) { /* original version */ };
```

/$

Note that the gating function is evaluated once at module time, so once the JS bundle has been parsed and evaluated the choice of component stays static for the rest of the browser session.

---

## Troubleshooting

### Feature flag not working

Verify your flag module exports the correct function:

 $

```
// ❌ Wrong: Default exportexport default function shouldUseCompiler() {  return true;}// ✅ Correct: Named export matching importSpecifierNameexport function shouldUseCompiler() {  return true;}
```

/$

### Import errors

Ensure the source path is correct:

 $

```
// ❌ Wrong: Relative to babel.config.js{  source: './src/flags',  importSpecifierName: 'flag'}// ✅ Correct: Module resolution path{  source: '@myapp/feature-flags',  importSpecifierName: 'flag'}// ✅ Also correct: Absolute path from project root{  source: './src/utils/flags',  importSpecifierName: 'flag'}
```

/$[PreviouscompilationMode](https://react.dev/reference/react-compiler/compilationMode)[Nextlogger](https://react.dev/reference/react-compiler/logger)

---

# logger

[API Reference](https://react.dev/reference/react)[Configuration](https://react.dev/reference/react-compiler/configuration)

# logger

The `logger` option provides custom logging for React Compiler events during compilation.

 $

```
{  logger: {    logEvent(filename, event) {      console.log(`[Compiler] ${event.kind}: ${filename}`);    }  }}
```

/$

- [Reference](#reference)
  - [logger](#logger)
- [Usage](#usage)
  - [Basic logging](#basic-logging)
  - [Detailed error logging](#detailed-error-logging)

---

## Reference

### logger

Configures custom logging to track compiler behavior and debug issues.

#### Type

 $

```
{  logEvent: (filename: string | null, event: LoggerEvent) => void;} | null
```

/$

#### Default value

`null`

#### Methods

- **logEvent**: Called for each compiler event with the filename and event details

#### Event types

- **CompileSuccess**: Function successfully compiled
- **CompileError**: Function skipped due to errors
- **CompileDiagnostic**: Non-fatal diagnostic information
- **CompileSkip**: Function skipped for other reasons
- **PipelineError**: Unexpected compilation error
- **Timing**: Performance timing information

#### Caveats

- Event structure may change between versions
- Large codebases generate many log entries

---

## Usage

### Basic logging

Track compilation success and failures:

 $

```
{  logger: {    logEvent(filename, event) {      switch (event.kind) {        case 'CompileSuccess': {          console.log(`✅ Compiled: ${filename}`);          break;        }        case 'CompileError': {          console.log(`❌ Skipped: ${filename}`);          break;        }        default: {}      }    }  }}
```

/$

### Detailed error logging

Get specific information about compilation failures:

 $

```
{  logger: {    logEvent(filename, event) {      if (event.kind === 'CompileError') {        console.error(`\nCompilation failed: ${filename}`);        console.error(`Reason: ${event.detail.reason}`);        if (event.detail.description) {          console.error(`Details: ${event.detail.description}`);        }        if (event.detail.loc) {          const { line, column } = event.detail.loc.start;          console.error(`Location: Line ${line}, Column ${column}`);        }        if (event.detail.suggestions) {          console.error('Suggestions:', event.detail.suggestions);        }      }    }  }}
```

/$[Previousgating](https://react.dev/reference/react-compiler/gating)[NextpanicThreshold](https://react.dev/reference/react-compiler/panicThreshold)

---

# panicThreshold

[API Reference](https://react.dev/reference/react)[Configuration](https://react.dev/reference/react-compiler/configuration)

# panicThreshold

The `panicThreshold` option controls how the React Compiler handles errors during compilation.

 $

```
{  panicThreshold: 'none' // Recommended}
```

/$

- [Reference](#reference)
  - [panicThreshold](#panicthreshold)
- [Usage](#usage)
  - [Production configuration (recommended)](#production-configuration)
  - [Development debugging](#development-debugging)

---

## Reference

### panicThreshold

Determines whether compilation errors should fail the build or skip optimization.

#### Type

 $

```
'none' | 'critical_errors' | 'all_errors'
```

/$

#### Default value

`'none'`

#### Options

- **'none'** (default, recommended): Skip components that can’t be compiled and continue building
- **'critical_errors'**: Fail the build only on critical compiler errors
- **'all_errors'**: Fail the build on any compiler diagnostic

#### Caveats

- Production builds should always use `'none'`
- Build failures prevent your application from building
- The compiler automatically detects and skips problematic code with `'none'`
- Higher thresholds are only useful during development for debugging

---

## Usage

### Production configuration (recommended)

For production builds, always use `'none'`. This is the default value:

 $

```
{  panicThreshold: 'none'}
```

/$

This ensures:

- Your build never fails due to compiler issues
- Components that can’t be optimized run normally
- Maximum components get optimized
- Stable production deployments

### Development debugging

Temporarily use stricter thresholds to find issues:

 $

```
const isDevelopment = process.env.NODE_ENV === 'development';{  panicThreshold: isDevelopment ? 'critical_errors' : 'none',  logger: {    logEvent(filename, event) {      if (isDevelopment && event.kind === 'CompileError') {        // ...      }    }  }}
```

/$[Previouslogger](https://react.dev/reference/react-compiler/logger)[Nexttarget](https://react.dev/reference/react-compiler/target)

---

# target

[API Reference](https://react.dev/reference/react)[Configuration](https://react.dev/reference/react-compiler/configuration)

# target

The `target` option specifies which React version the compiler should generate code for.

 $

```
{  target: '19' // or '18', '17'}
```

/$

- [Reference](#reference)
  - [target](#target)
- [Usage](#usage)
  - [Targeting React 19 (default)](#targeting-react-19)
  - [Targeting React 17 or 18](#targeting-react-17-or-18)
- [Troubleshooting](#troubleshooting)
  - [Runtime errors about missing compiler runtime](#missing-runtime)
  - [Runtime package not working](#runtime-not-working)
  - [Checking compiled output](#checking-output)

---

## Reference

### target

Configures the React version compatibility for the compiled output.

#### Type

 $

```
'17' | '18' | '19'
```

/$

#### Default value

`'19'`

#### Valid values

- **'19'**: Target React 19 (default). No additional runtime required.
- **'18'**: Target React 18. Requires `react-compiler-runtime` package.
- **'17'**: Target React 17. Requires `react-compiler-runtime` package.

#### Caveats

- Always use string values, not numbers (e.g., `'17'` not `17`)
- Don’t include patch versions (e.g., use `'18'` not `'18.2.0'`)
- React 19 includes built-in compiler runtime APIs
- React 17 and 18 require installing `react-compiler-runtime@latest`

---

## Usage

### Targeting React 19 (default)

For React 19, no special configuration is needed:

 $

```
{  // defaults to target: '19'}
```

/$

The compiler will use React 19’s built-in runtime APIs:

 $

```
// Compiled output uses React 19's native APIsimport { c as _c } from 'react/compiler-runtime';
```

/$

### Targeting React 17 or 18

For React 17 and React 18 projects, you need two steps:

1. Install the runtime package:

 $

```
npm install react-compiler-runtime@latest
```

/$

1. Configure the target:

 $

```
// For React 18{  target: '18'}// For React 17{  target: '17'}
```

/$

The compiler will use the polyfill runtime for both versions:

 $

```
// Compiled output uses the polyfillimport { c as _c } from 'react-compiler-runtime';
```

/$

---

## Troubleshooting

### Runtime errors about missing compiler runtime

If you see errors like “Cannot find module ‘react/compiler-runtime’“:

1. Check your React version:
   $
  ```
  npm why react
  ```
  /$
2. If using React 17 or 18, install the runtime:
   $
  ```
  npm install react-compiler-runtime@latest
  ```
  /$
3. Ensure your target matches your React version:
   $
  ```
  {  target: '18' // Must match your React major version}
  ```
  /$

### Runtime package not working

Ensure the runtime package is:

1. Installed in your project (not globally)
2. Listed in your `package.json` dependencies
3. The correct version (`@latest` tag)
4. Not in `devDependencies` (it’s needed at runtime)

### Checking compiled output

To verify the correct runtime is being used, note the different import (`react/compiler-runtime` for builtin, `react-compiler-runtime` standalone package for 17/18):

 $

```
// For React 19 (built-in runtime)import { c } from 'react/compiler-runtime'//                      ^// For React 17/18 (polyfill runtime)import { c } from 'react-compiler-runtime'//                      ^
```

/$[PreviouspanicThreshold](https://react.dev/reference/react-compiler/panicThreshold)[NextDirectives](https://react.dev/reference/react-compiler/directives)

---

# createRoot

[API Reference](https://react.dev/reference/react)[Client APIs](https://react.dev/reference/react-dom/client)

# createRoot

`createRoot` lets you create a root to display React components inside a browser DOM node.

$

```
const root = createRoot(domNode, options?)
```

/$

- [Reference](#reference)
  - [createRoot(domNode, options?)](#createroot)
  - [root.render(reactNode)](#root-render)
  - [root.unmount()](#root-unmount)
- [Usage](#usage)
  - [Rendering an app fully built with React](#rendering-an-app-fully-built-with-react)
  - [Rendering a page partially built with React](#rendering-a-page-partially-built-with-react)
  - [Updating a root component](#updating-a-root-component)
  - [Error logging in production](#error-logging-in-production)
- [Troubleshooting](#troubleshooting)
  - [I’ve created a root, but nothing is displayed](#ive-created-a-root-but-nothing-is-displayed)
  - [I’m getting an error: “You passed a second argument to root.render”](#im-getting-an-error-you-passed-a-second-argument-to-root-render)
  - [I’m getting an error: “Target container is not a DOM element”](#im-getting-an-error-target-container-is-not-a-dom-element)
  - [I’m getting an error: “Functions are not valid as a React child.”](#im-getting-an-error-functions-are-not-valid-as-a-react-child)
  - [My server-rendered HTML gets re-created from scratch](#my-server-rendered-html-gets-re-created-from-scratch)

---

## Reference

### createRoot(domNode, options?)

Call `createRoot` to create a React root for displaying content inside a browser DOM element.

 $

```
import { createRoot } from 'react-dom/client';const domNode = document.getElementById('root');const root = createRoot(domNode);
```

/$

React will create a root for the `domNode`, and take over managing the DOM inside it. After you’ve created a root, you need to call [root.render](#root-render) to display a React component inside of it:

 $

```
root.render(<App />);
```

/$

An app fully built with React will usually only have one `createRoot` call for its root component. A page that uses “sprinkles” of React for parts of the page may have as many separate roots as needed.

[See more examples below.](#usage)

#### Parameters

- `domNode`: A [DOM element.](https://developer.mozilla.org/en-US/docs/Web/API/Element) React will create a root for this DOM element and allow you to call functions on the root, such as `render` to display rendered React content.
- **optional** `options`: An object with options for this React root.
  - **optional** `onCaughtError`: Callback called when React catches an error in an Error Boundary. Called with the `error` caught by the Error Boundary, and an `errorInfo` object containing the `componentStack`.
  - **optional** `onUncaughtError`: Callback called when an error is thrown and not caught by an Error Boundary. Called with the `error` that was thrown, and an `errorInfo` object containing the `componentStack`.
  - **optional** `onRecoverableError`: Callback called when React automatically recovers from errors. Called with an `error` React throws, and an `errorInfo` object containing the `componentStack`. Some recoverable errors may include the original error cause as `error.cause`.
  - **optional** `identifierPrefix`: A string prefix React uses for IDs generated by [useId.](https://react.dev/reference/react/useId) Useful to avoid conflicts when using multiple roots on the same page.

#### Returns

`createRoot` returns an object with two methods: [render](#root-render) and [unmount.](#root-unmount)

#### Caveats

- If your app is server-rendered, using `createRoot()` is not supported. Use [hydrateRoot()](https://react.dev/reference/react-dom/client/hydrateRoot) instead.
- You’ll likely have only one `createRoot` call in your app. If you use a framework, it might do this call for you.
- When you want to render a piece of JSX in a different part of the DOM tree that isn’t a child of your component (for example, a modal or a tooltip), use [createPortal](https://react.dev/reference/react-dom/createPortal) instead of `createRoot`.

---

### root.render(reactNode)

Call `root.render` to display a piece of [JSX](https://react.dev/learn/writing-markup-with-jsx) (“React node”) into the React root’s browser DOM node.

 $

```
root.render(<App />);
```

/$

React will display `<App />` in the `root`, and take over managing the DOM inside it.

[See more examples below.](#usage)

#### Parameters

- `reactNode`: A *React node* that you want to display. This will usually be a piece of JSX like `<App />`, but you can also pass a React element constructed with [createElement()](https://react.dev/reference/react/createElement), a string, a number, `null`, or `undefined`.

#### Returns

`root.render` returns `undefined`.

#### Caveats

- The first time you call `root.render`, React will clear all the existing HTML content inside the React root before rendering the React component into it.
- If your root’s DOM node contains HTML generated by React on the server or during the build, use [hydrateRoot()](https://react.dev/reference/react-dom/client/hydrateRoot) instead, which attaches the event handlers to the existing HTML.
- If you call `render` on the same root more than once, React will update the DOM as necessary to reflect the latest JSX you passed. React will decide which parts of the DOM can be reused and which need to be recreated by [“matching it up”](https://react.dev/learn/preserving-and-resetting-state) with the previously rendered tree. Calling `render` on the same root again is similar to calling the [setfunction](https://react.dev/reference/react/useState#setstate) on the root component: React avoids unnecessary DOM updates.
- Although rendering is synchronous once it starts, `root.render(...)` is not. This means code after `root.render()` may run before any effects (`useLayoutEffect`, `useEffect`) of that specific render are fired. This is usually fine and rarely needs adjustment. In rare cases where effect timing matters, you can wrap `root.render(...)` in [flushSync](https://react.dev/reference/react-dom/flushSync) to ensure the initial render runs fully synchronously.
   $
  ```
  const root = createRoot(document.getElementById('root'));root.render(<App />);// 🚩 The HTML will not include the rendered <App /> yet:console.log(document.body.innerHTML);
  ```
  /$

---

### root.unmount()

Call `root.unmount` to destroy a rendered tree inside a React root.

 $

```
root.unmount();
```

/$

An app fully built with React will usually not have any calls to `root.unmount`.

This is mostly useful if your React root’s DOM node (or any of its ancestors) may get removed from the DOM by some other code. For example, imagine a jQuery tab panel that removes inactive tabs from the DOM. If a tab gets removed, everything inside it (including the React roots inside) would get removed from the DOM as well. In that case, you need to tell React to “stop” managing the removed root’s content by calling `root.unmount`. Otherwise, the components inside the removed root won’t know to clean up and free up global resources like subscriptions.

Calling `root.unmount` will unmount all the components in the root and “detach” React from the root DOM node, including removing any event handlers or state in the tree.

#### Parameters

`root.unmount` does not accept any parameters.

#### Returns

`root.unmount` returns `undefined`.

#### Caveats

- Calling `root.unmount` will unmount all the components in the tree and “detach” React from the root DOM node.
- Once you call `root.unmount` you cannot call `root.render` again on the same root. Attempting to call `root.render` on an unmounted root will throw a “Cannot update an unmounted root” error. However, you can create a new root for the same DOM node after the previous root for that node has been unmounted.

---

## Usage

### Rendering an app fully built with React

If your app is fully built with React, create a single root for your entire app.

 $

```
import { createRoot } from 'react-dom/client';const root = createRoot(document.getElementById('root'));root.render(<App />);
```

/$

Usually, you only need to run this code once at startup. It will:

1. Find the browser DOM node defined in your HTML.
2. Display the React component for your app inside.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';
import App from './App.js';
import './styles.css';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

/$

**If your app is fully built with React, you shouldn’t need to create any more roots, or to callroot.renderagain.**

From this point on, React will manage the DOM of your entire app. To add more components, [nest them inside theAppcomponent.](https://react.dev/learn/importing-and-exporting-components) When you need to update the UI, each of your components can do this by [using state.](https://react.dev/reference/react/useState) When you need to display extra content like a modal or a tooltip outside the DOM node, [render it with a portal.](https://react.dev/reference/react-dom/createPortal)

### Note

When your HTML is empty, the user sees a blank page until the app’s JavaScript code loads and runs:

$

```
<div id="root"></div>
```

/$

This can feel very slow! To solve this, you can generate the initial HTML from your components [on the server or during the build.](https://react.dev/reference/react-dom/server) Then your visitors can read text, see images, and click links before any of the JavaScript code loads. We recommend [using a framework](https://react.dev/learn/creating-a-react-app#full-stack-frameworks) that does this optimization out of the box. Depending on when it runs, this is called *server-side rendering (SSR)* or *static site generation (SSG).*

### Pitfall

**Apps using server rendering or static generation must callhydrateRootinstead ofcreateRoot.** React will then *hydrate* (reuse) the DOM nodes from your HTML instead of destroying and re-creating them.

---

### Rendering a page partially built with React

If your page [isn’t fully built with React](https://react.dev/learn/add-react-to-an-existing-project#using-react-for-a-part-of-your-existing-page), you can call `createRoot` multiple times to create a root for each top-level piece of UI managed by React. You can display different content in each root by calling [root.render.](#root-render)

Here, two different React components are rendered into two DOM nodes defined in the `index.html` file:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import './styles.css';
import { createRoot } from 'react-dom/client';
import { Comments, Navigation } from './Components.js';

const navDomNode = document.getElementById('navigation');
const navRoot = createRoot(navDomNode);
navRoot.render(<Navigation />);

const commentDomNode = document.getElementById('comments');
const commentRoot = createRoot(commentDomNode);
commentRoot.render(<Comments />);
```

/$

You could also create a new DOM node with [document.createElement()](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement) and add it to the document manually.

 $

```
const domNode = document.createElement('div');const root = createRoot(domNode); root.render(<Comment />);document.body.appendChild(domNode); // You can add it anywhere in the document
```

/$

To remove the React tree from the DOM node and clean up all the resources used by it, call [root.unmount.](#root-unmount)

 $

```
root.unmount();
```

/$

This is mostly useful if your React components are inside an app written in a different framework.

---

### Updating a root component

You can call `render` more than once on the same root. As long as the component tree structure matches up with what was previously rendered, React will [preserve the state.](https://react.dev/learn/preserving-and-resetting-state) Notice how you can type in the input, which means that the updates from repeated `render` calls every second in this example are not destructive:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from 'react-dom/client';
import './styles.css';
import App from './App.js';

const root = createRoot(document.getElementById('root'));

let i = 0;
setInterval(() => {
  root.render(<App counter={i} />);
  i++;
}, 1000);
```

/$

It is uncommon to call `render` multiple times. Usually, your components will [update state](https://react.dev/reference/react/useState) instead.

### Error logging in production

By default, React will log all errors to the console. To implement your own error reporting, you can provide the optional error handler root options `onUncaughtError`, `onCaughtError` and `onRecoverableError`:

 $

```
import { createRoot } from "react-dom/client";import { reportCaughtError } from "./reportError";const container = document.getElementById("root");const root = createRoot(container, {  onCaughtError: (error, errorInfo) => {    if (error.message !== "Known error") {      reportCaughtError({        error,        componentStack: errorInfo.componentStack,      });    }  },});
```

/$

The onCaughtError option is a function called with two arguments:

1. The error that was thrown.
2. An errorInfo object that contains the componentStack of the error.

Together with `onUncaughtError` and `onRecoverableError`, you can can implement your own error reporting system:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRoot } from "react-dom/client";
import App from "./App.js";
import {
  onCaughtErrorProd,
  onRecoverableErrorProd,
  onUncaughtErrorProd,
} from "./reportError";

const container = document.getElementById("root");
const root = createRoot(container, {
  // Keep in mind to remove these options in development to leverage
  // React's default handlers or implement your own overlay for development.
  // The handlers are only specfied unconditionally here for demonstration purposes.
  onCaughtError: onCaughtErrorProd,
  onRecoverableError: onRecoverableErrorProd,
  onUncaughtError: onUncaughtErrorProd,
});
root.render(<App />);
```

/$

## Troubleshooting

### I’ve created a root, but nothing is displayed

Make sure you haven’t forgotten to actually *render* your app into the root:

 $

```
import { createRoot } from 'react-dom/client';import App from './App.js';const root = createRoot(document.getElementById('root'));root.render(<App />);
```

/$

Until you do that, nothing is displayed.

---

### I’m getting an error: “You passed a second argument to root.render”

A common mistake is to pass the options for `createRoot` to `root.render(...)`:

 ConsoleWarning: You passed a second argument to root.render(…) but it only accepts one argument.

To fix, pass the root options to `createRoot(...)`, not `root.render(...)`:

 $

```
// 🚩 Wrong: root.render only takes one argument.root.render(App, {onUncaughtError});// ✅ Correct: pass options to createRoot.const root = createRoot(container, {onUncaughtError}); root.render(<App />);
```

/$

---

### I’m getting an error: “Target container is not a DOM element”

This error means that whatever you’re passing to `createRoot` is not a DOM node.

If you’re not sure what’s happening, try logging it:

 $

```
const domNode = document.getElementById('root');console.log(domNode); // ???const root = createRoot(domNode);root.render(<App />);
```

/$

For example, if `domNode` is `null`, it means that [getElementById](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) returned `null`. This will happen if there is no node in the document with the given ID at the time of your call. There may be a few reasons for it:

1. The ID you’re looking for might differ from the ID you used in the HTML file. Check for typos!
2. Your bundle’s `<script>` tag cannot “see” any DOM nodes that appear *after* it in the HTML.

Another common way to get this error is to write `createRoot(<App />)` instead of `createRoot(domNode)`.

---

### I’m getting an error: “Functions are not valid as a React child.”

This error means that whatever you’re passing to `root.render` is not a React component.

This may happen if you call `root.render` with `Component` instead of `<Component />`:

 $

```
// 🚩 Wrong: App is a function, not a Component.root.render(App);// ✅ Correct: <App /> is a component.root.render(<App />);
```

/$

Or if you pass a function to `root.render`, instead of the result of calling it:

 $

```
// 🚩 Wrong: createApp is a function, not a component.root.render(createApp);// ✅ Correct: call createApp to return a component.root.render(createApp());
```

/$

---

### My server-rendered HTML gets re-created from scratch

If your app is server-rendered and includes the initial HTML generated by React, you might notice that creating a root and calling `root.render` deletes all that HTML, and then re-creates all the DOM nodes from scratch. This can be slower, resets focus and scroll positions, and may lose other user input.

Server-rendered apps must use [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) instead of `createRoot`:

 $

```
import { hydrateRoot } from 'react-dom/client';import App from './App.js';hydrateRoot(  document.getElementById('root'),  <App />);
```

/$

Note that its API is different. In particular, usually there will be no further `root.render` call.

[PreviousClient APIs](https://react.dev/reference/react-dom/client)[NexthydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)
