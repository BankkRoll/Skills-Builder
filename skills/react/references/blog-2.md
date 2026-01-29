# React v18.0 and more

# React v18.0

[Blog](https://react.dev/blog)

# React v18.0

March 29, 2022 by [The React Team](https://react.dev/community/team)

---

React 18 is now available on npm! In our last post, we shared step-by-step instructions for [upgrading your app to React 18](https://react.dev/blog/2022/03/08/react-18-upgrade-guide). In this post, we’ll give an overview of what’s new in React 18, and what it means for the future.

---

Our latest major version includes out-of-the-box improvements like automatic batching, new APIs like startTransition, and streaming server-side rendering with support for Suspense.

Many of the features in React 18 are built on top of our new concurrent renderer, a behind-the-scenes change that unlocks powerful new capabilities. Concurrent React is opt-in — it’s only enabled when you use a concurrent feature — but we think it will have a big impact on the way people build applications.

We’ve spent years researching and developing support for concurrency in React, and we’ve taken extra care to provide a gradual adoption path for existing users. Last summer, [we formed the React 18 Working Group](https://react.dev/blog/2021/06/08/the-plan-for-react-18) to gather feedback from experts in the community and ensure a smooth upgrade experience for the entire React ecosystem.

In case you missed it, we shared a lot of this vision at React Conf 2021:

- In [the keynote](https://www.youtube.com/watch?v=FZ0cG47msEk&list=PLNG_1j3cPCaZZ7etkzWA7JfdmKWT0pMsa), we explain how React 18 fits into our mission to make it easy for developers to build great user experiences
- [Shruti Kapoor](https://twitter.com/shrutikapoor08) [demonstrated how to use the new features in React 18](https://www.youtube.com/watch?v=ytudH8je5ko&list=PLNG_1j3cPCaZZ7etkzWA7JfdmKWT0pMsa&index=2)
- [Shaundai Person](https://twitter.com/shaundai) gave us an overview of [streaming server rendering with Suspense](https://www.youtube.com/watch?v=pj5N-Khihgc&list=PLNG_1j3cPCaZZ7etkzWA7JfdmKWT0pMsa&index=3)

Below is a full overview of what to expect in this release, starting with Concurrent Rendering.

### Note

For React Native users, React 18 will ship in React Native with the New React Native Architecture. For more information, see the [React Conf keynote here](https://www.youtube.com/watch?v=FZ0cG47msEk&t=1530s).

## What is Concurrent React?

The most important addition in React 18 is something we hope you never have to think about: concurrency. We think this is largely true for application developers, though the story may be a bit more complicated for library maintainers.

Concurrency is not a feature, per se. It’s a new behind-the-scenes mechanism that enables React to prepare multiple versions of your UI at the same time. You can think of concurrency as an implementation detail — it’s valuable because of the features that it unlocks. React uses sophisticated techniques in its internal implementation, like priority queues and multiple buffering. But you won’t see those concepts anywhere in our public APIs.

When we design APIs, we try to hide implementation details from developers. As a React developer, you focus on *what* you want the user experience to look like, and React handles *how* to deliver that experience. So we don’t expect React developers to know how concurrency works under the hood.

However, Concurrent React is more important than a typical implementation detail — it’s a foundational update to React’s core rendering model. So while it’s not super important to know how concurrency works, it may be worth knowing what it is at a high level.

A key property of Concurrent React is that rendering is interruptible. When you first upgrade to React 18, before adding any concurrent features, updates are rendered the same as in previous versions of React — in a single, uninterrupted, synchronous transaction. With synchronous rendering, once an update starts rendering, nothing can interrupt it until the user can see the result on screen.

In a concurrent render, this is not always the case. React may start rendering an update, pause in the middle, then continue later. It may even abandon an in-progress render altogether. React guarantees that the UI will appear consistent even if a render is interrupted. To do this, it waits to perform DOM mutations until the end, once the entire tree has been evaluated. With this capability, React can prepare new screens in the background without blocking the main thread. This means the UI can respond immediately to user input even if it’s in the middle of a large rendering task, creating a fluid user experience.

Another example is reusable state. Concurrent React can remove sections of the UI from the screen, then add them back later while reusing the previous state. For example, when a user tabs away from a screen and back, React should be able to restore the previous screen in the same state it was in before. In an upcoming minor, we’re planning to add a new component called `<Offscreen>` that implements this pattern. Similarly, you’ll be able to use Offscreen to prepare new UI in the background so that it’s ready before the user reveals it.

Concurrent rendering is a powerful new tool in React and most of our new features are built to take advantage of it, including Suspense, transitions, and streaming server rendering. But React 18 is just the beginning of what we aim to build on this new foundation.

## Gradually Adopting Concurrent Features

Technically, concurrent rendering is a breaking change. Because concurrent rendering is interruptible, components behave slightly differently when it is enabled.

In our testing, we’ve upgraded thousands of components to React 18. What we’ve found is that nearly all existing components “just work” with concurrent rendering, without any changes. However, some of them may require some additional migration effort. Although the changes are usually small, you’ll still have the ability to make them at your own pace. The new rendering behavior in React 18 is **only enabled in the parts of your app that use new features.**

The overall upgrade strategy is to get your application running on React 18 without breaking existing code. Then you can gradually start adding concurrent features at your own pace. You can use [<StrictMode>](https://react.dev/reference/react/StrictMode) to help surface concurrency-related bugs during development. Strict Mode doesn’t affect production behavior, but during development it will log extra warnings and double-invoke functions that are expected to be idempotent. It won’t catch everything, but it’s effective at preventing the most common types of mistakes.

After you upgrade to React 18, you’ll be able to start using concurrent features immediately. For example, you can use startTransition to navigate between screens without blocking user input. Or useDeferredValue to throttle expensive re-renders.

However, long term, we expect the main way you’ll add concurrency to your app is by using a concurrent-enabled library or framework. In most cases, you won’t interact with concurrent APIs directly. For example, instead of developers calling startTransition whenever they navigate to a new screen, router libraries will automatically wrap navigations in startTransition.

It may take some time for libraries to upgrade to be concurrent compatible. We’ve provided new APIs to make it easier for libraries to take advantage of concurrent features. In the meantime, please be patient with maintainers as we work to gradually migrate the React ecosystem.

For more info, see our previous post: [How to upgrade to React 18](https://react.dev/blog/2022/03/08/react-18-upgrade-guide).

## Suspense in Data Frameworks

In React 18, you can start using [Suspense](https://react.dev/reference/react/Suspense) for data fetching in opinionated frameworks like Relay, Next.js, Hydrogen, or Remix. Ad hoc data fetching with Suspense is technically possible, but still not recommended as a general strategy.

In the future, we may expose additional primitives that could make it easier to access your data with Suspense, perhaps without the use of an opinionated framework. However, Suspense works best when it’s deeply integrated into your application’s architecture: your router, your data layer, and your server rendering environment. So even long term, we expect that libraries and frameworks will play a crucial role in the React ecosystem.

As in previous versions of React, you can also use Suspense for code splitting on the client with React.lazy. But our vision for Suspense has always been about much more than loading code — the goal is to extend support for Suspense so that eventually, the same declarative Suspense fallback can handle any asynchronous operation (loading code, data, images, etc).

## Server Components is Still in Development

[Server Components](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components) is an upcoming feature that allows developers to build apps that span the server and client, combining the rich interactivity of client-side apps with the improved performance of traditional server rendering. Server Components is not inherently coupled to Concurrent React, but it’s designed to work best with concurrent features like Suspense and streaming server rendering.

Server Components is still experimental, but we expect to release an initial version in a minor 18.x release. In the meantime, we’re working with frameworks like Next.js, Hydrogen, and Remix to advance the proposal and get it ready for broad adoption.

## What’s New in React 18

### New Feature: Automatic Batching

Batching is when React groups multiple state updates into a single re-render for better performance. Without automatic batching, we only batched updates inside React event handlers. Updates inside of promises, setTimeout, native event handlers, or any other event were not batched in React by default. With automatic batching, these updates will be batched automatically:

 $

```
// Before: only React events were batched.setTimeout(() => {  setCount(c => c + 1);  setFlag(f => !f);  // React will render twice, once for each state update (no batching)}, 1000);// After: updates inside of timeouts, promises,// native event handlers or any other event are batched.setTimeout(() => {  setCount(c => c + 1);  setFlag(f => !f);  // React will only re-render once at the end (that's batching!)}, 1000);
```

/$

For more info, see this post for [Automatic batching for fewer renders in React 18](https://github.com/reactwg/react-18/discussions/21).

### New Feature: Transitions

A transition is a new concept in React to distinguish between urgent and non-urgent updates.

- **Urgent updates** reflect direct interaction, like typing, clicking, pressing, and so on.
- **Transition updates** transition the UI from one view to another.

Urgent updates like typing, clicking, or pressing, need immediate response to match our intuitions about how physical objects behave. Otherwise they feel “wrong”. However, transitions are different because the user doesn’t expect to see every intermediate value on screen.

For example, when you select a filter in a dropdown, you expect the filter button itself to respond immediately when you click. However, the actual results may transition separately. A small delay would be imperceptible and often expected. And if you change the filter again before the results are done rendering, you only care to see the latest results.

Typically, for the best user experience, a single user input should result in both an urgent update and a non-urgent one. You can use startTransition API inside an input event to inform React which updates are urgent and which are “transitions”:

 $

```
import { startTransition } from 'react';// Urgent: Show what was typedsetInputValue(input);// Mark any state updates inside as transitionsstartTransition(() => {  // Transition: Show the results  setSearchQuery(input);});
```

/$

Updates wrapped in startTransition are handled as non-urgent and will be interrupted if more urgent updates like clicks or key presses come in. If a transition gets interrupted by the user (for example, by typing multiple characters in a row), React will throw out the stale rendering work that wasn’t finished and render only the latest update.

- `useTransition`: a Hook to start transitions, including a value to track the pending state.
- `startTransition`: a method to start transitions when the Hook cannot be used.

Transitions will opt in to concurrent rendering, which allows the update to be interrupted. If the content re-suspends, transitions also tell React to continue showing the current content while rendering the transition content in the background (see the [Suspense RFC](https://github.com/reactjs/rfcs/blob/main/text/0213-suspense-in-react-18.md) for more info).

[See docs for transitions here](https://react.dev/reference/react/useTransition).

### New Suspense Features

Suspense lets you declaratively specify the loading state for a part of the component tree if it’s not yet ready to be displayed:

 $

```
<Suspense fallback={<Spinner />}>  <Comments /></Suspense>
```

/$

Suspense makes the “UI loading state” a first-class declarative concept in the React programming model. This lets us build higher-level features on top of it.

We introduced a limited version of Suspense several years ago. However, the only supported use case was code splitting with React.lazy, and it wasn’t supported at all when rendering on the server.

In React 18, we’ve added support for Suspense on the server and expanded its capabilities using concurrent rendering features.

Suspense in React 18 works best when combined with the transition API. If you suspend during a transition, React will prevent already-visible content from being replaced by a fallback. Instead, React will delay the render until enough data has loaded to prevent a bad loading state.

For more, see the RFC for [Suspense in React 18](https://github.com/reactjs/rfcs/blob/main/text/0213-suspense-in-react-18.md).

### New Client and Server Rendering APIs

In this release we took the opportunity to redesign the APIs we expose for rendering on the client and server. These changes allow users to continue using the old APIs in React 17 mode while they upgrade to the new APIs in React 18.

#### React DOM Client

These new APIs are now exported from `react-dom/client`:

- `createRoot`: New method to create a root to `render` or `unmount`. Use it instead of `ReactDOM.render`. New features in React 18 don’t work without it.
- `hydrateRoot`: New method to hydrate a server rendered application. Use it instead of  `ReactDOM.hydrate` in conjunction with the new React DOM Server APIs. New features in React 18 don’t work without it.

Both `createRoot` and `hydrateRoot` accept a new option called `onRecoverableError` in case you want to be notified when React recovers from errors during rendering or hydration for logging. By default, React will use [reportError](https://developer.mozilla.org/en-US/docs/Web/API/reportError), or `console.error` in the older browsers.

[See docs for React DOM Client here](https://react.dev/reference/react-dom/client).

#### React DOM Server

These new APIs are now exported from `react-dom/server` and have full support for streaming Suspense on the server:

- `renderToPipeableStream`: for streaming in Node environments.
- `renderToReadableStream`: for modern edge runtime environments, such as Deno and Cloudflare workers.

The existing `renderToString` method keeps working but is discouraged.

[See docs for React DOM Server here](https://react.dev/reference/react-dom/server).

### New Strict Mode Behaviors

In the future, we’d like to add a feature that allows React to add and remove sections of the UI while preserving state. For example, when a user tabs away from a screen and back, React should be able to immediately show the previous screen. To do this, React would unmount and remount trees using the same component state as before.

This feature will give React apps better performance out-of-the-box, but requires components to be resilient to effects being mounted and destroyed multiple times. Most effects will work without any changes, but some effects assume they are only mounted or destroyed once.

To help surface these issues, React 18 introduces a new development-only check to Strict Mode. This new check will automatically unmount and remount every component, whenever a component mounts for the first time, restoring the previous state on the second mount.

Before this change, React would mount the component and create the effects:

 $

```
* React mounts the component.  * Layout effects are created.  * Effects are created.
```

/$

With Strict Mode in React 18, React will simulate unmounting and remounting the component in development mode:

 $

```
* React mounts the component.  * Layout effects are created.  * Effects are created.* React simulates unmounting the component.  * Layout effects are destroyed.  * Effects are destroyed.* React simulates mounting the component with the previous state.  * Layout effects are created.  * Effects are created.
```

/$

[See docs for ensuring reusable state here](https://react.dev/reference/react/StrictMode#fixing-bugs-found-by-re-running-effects-in-development).

### New Hooks

#### useId

`useId` is a new Hook for generating unique IDs on both the client and server, while avoiding hydration mismatches. It is primarily useful for component libraries integrating with accessibility APIs that require unique IDs. This solves an issue that already exists in React 17 and below, but it’s even more important in React 18 because of how the new streaming server renderer delivers HTML out-of-order. [See docs here](https://react.dev/reference/react/useId).

> Note
>
>
>
> `useId` is **not** for generating [keys in a list](https://react.dev/learn/rendering-lists#where-to-get-your-key). Keys should be generated from your data.

#### useTransition

`useTransition` and `startTransition` let you mark some state updates as not urgent. Other state updates are considered urgent by default. React will allow urgent state updates (for example, updating a text input) to interrupt non-urgent state updates (for example, rendering a list of search results). [See docs here](https://react.dev/reference/react/useTransition).

#### useDeferredValue

`useDeferredValue` lets you defer re-rendering a non-urgent part of the tree. It is similar to debouncing, but has a few advantages compared to it. There is no fixed time delay, so React will attempt the deferred render right after the first render is reflected on the screen. The deferred render is interruptible and doesn’t block user input. [See docs here](https://react.dev/reference/react/useDeferredValue).

#### useSyncExternalStore

`useSyncExternalStore` is a new Hook that allows external stores to support concurrent reads by forcing updates to the store to be synchronous. It removes the need for useEffect when implementing subscriptions to external data sources, and is recommended for any library that integrates with state external to React. [See docs here](https://react.dev/reference/react/useSyncExternalStore).

> Note
>
>
>
> `useSyncExternalStore` is intended to be used by libraries, not application code.

#### useInsertionEffect

`useInsertionEffect` is a new Hook that allows CSS-in-JS libraries to address performance issues of injecting styles in render. Unless you’ve already built a CSS-in-JS library we don’t expect you to ever use this. This Hook will run after the DOM is mutated, but before layout effects read the new layout. This solves an issue that already exists in React 17 and below, but is even more important in React 18 because React yields to the browser during concurrent rendering, giving it a chance to recalculate layout. [See docs here](https://react.dev/reference/react/useInsertionEffect).

> Note
>
>
>
> `useInsertionEffect` is intended to be used by libraries, not application code.

## How to Upgrade

See [How to Upgrade to React 18](https://react.dev/blog/2022/03/08/react-18-upgrade-guide) for step-by-step instructions and a full list of breaking and notable changes.

## Changelog

### React

- Add `useTransition` and `useDeferredValue` to separate urgent updates from transitions. ([#10426](https://github.com/facebook/react/pull/10426), [#10715](https://github.com/facebook/react/pull/10715), [#15593](https://github.com/facebook/react/pull/15593), [#15272](https://github.com/facebook/react/pull/15272), [#15578](https://github.com/facebook/react/pull/15578), [#15769](https://github.com/facebook/react/pull/15769), [#17058](https://github.com/facebook/react/pull/17058), [#18796](https://github.com/facebook/react/pull/18796), [#19121](https://github.com/facebook/react/pull/19121), [#19703](https://github.com/facebook/react/pull/19703), [#19719](https://github.com/facebook/react/pull/19719), [#19724](https://github.com/facebook/react/pull/19724), [#20672](https://github.com/facebook/react/pull/20672), [#20976](https://github.com/facebook/react/pull/20976) by [@acdlite](https://github.com/acdlite), [@lunaruan](https://github.com/lunaruan), [@rickhanlonii](https://github.com/rickhanlonii), and [@sebmarkbage](https://github.com/sebmarkbage))
- Add `useId` for generating unique IDs. ([#17322](https://github.com/facebook/react/pull/17322), [#18576](https://github.com/facebook/react/pull/18576), [#22644](https://github.com/facebook/react/pull/22644), [#22672](https://github.com/facebook/react/pull/22672), [#21260](https://github.com/facebook/react/pull/21260) by [@acdlite](https://github.com/acdlite), [@lunaruan](https://github.com/lunaruan), and [@sebmarkbage](https://github.com/sebmarkbage))
- Add `useSyncExternalStore` to help external store libraries integrate with React. ([#15022](https://github.com/facebook/react/pull/15022), [#18000](https://github.com/facebook/react/pull/18000), [#18771](https://github.com/facebook/react/pull/18771), [#22211](https://github.com/facebook/react/pull/22211), [#22292](https://github.com/facebook/react/pull/22292), [#22239](https://github.com/facebook/react/pull/22239), [#22347](https://github.com/facebook/react/pull/22347), [#23150](https://github.com/facebook/react/pull/23150) by [@acdlite](https://github.com/acdlite), [@bvaughn](https://github.com/bvaughn), and [@drarmstr](https://github.com/drarmstr))
- Add `startTransition` as a version of `useTransition` without pending feedback. ([#19696](https://github.com/facebook/react/pull/19696)  by [@rickhanlonii](https://github.com/rickhanlonii))
- Add `useInsertionEffect` for CSS-in-JS libraries. ([#21913](https://github.com/facebook/react/pull/21913)  by [@rickhanlonii](https://github.com/rickhanlonii))
- Make Suspense remount layout effects when content reappears.  ([#19322](https://github.com/facebook/react/pull/19322), [#19374](https://github.com/facebook/react/pull/19374), [#19523](https://github.com/facebook/react/pull/19523), [#20625](https://github.com/facebook/react/pull/20625), [#21079](https://github.com/facebook/react/pull/21079) by [@acdlite](https://github.com/acdlite), [@bvaughn](https://github.com/bvaughn), and [@lunaruan](https://github.com/lunaruan))
- Make `<StrictMode>` re-run effects to check for restorable state. ([#19523](https://github.com/facebook/react/pull/19523) , [#21418](https://github.com/facebook/react/pull/21418)  by [@bvaughn](https://github.com/bvaughn) and [@lunaruan](https://github.com/lunaruan))
- Assume Symbols are always available. ([#23348](https://github.com/facebook/react/pull/23348)  by [@sebmarkbage](https://github.com/sebmarkbage))
- Remove `object-assign` polyfill. ([#23351](https://github.com/facebook/react/pull/23351)  by [@sebmarkbage](https://github.com/sebmarkbage))
- Remove unsupported `unstable_changedBits` API.  ([#20953](https://github.com/facebook/react/pull/20953)  by [@acdlite](https://github.com/acdlite))
- Allow components to render undefined. ([#21869](https://github.com/facebook/react/pull/21869)  by [@rickhanlonii](https://github.com/rickhanlonii))
- Flush `useEffect` resulting from discrete events like clicks synchronously. ([#21150](https://github.com/facebook/react/pull/21150)  by [@acdlite](https://github.com/acdlite))
- Suspense `fallback={undefined}` now behaves the same as `null` and isn’t ignored. ([#21854](https://github.com/facebook/react/pull/21854)  by [@rickhanlonii](https://github.com/rickhanlonii))
- Consider all `lazy()` resolving to the same component equivalent. ([#20357](https://github.com/facebook/react/pull/20357)  by [@sebmarkbage](https://github.com/sebmarkbage))
- Don’t patch console during first render. ([#22308](https://github.com/facebook/react/pull/22308)  by [@lunaruan](https://github.com/lunaruan))
- Improve memory usage. ([#21039](https://github.com/facebook/react/pull/21039)  by [@bgirard](https://github.com/bgirard))
- Improve messages if string coercion throws (Temporal.*, Symbol, etc.) ([#22064](https://github.com/facebook/react/pull/22064)  by [@justingrant](https://github.com/justingrant))
- Use `setImmediate` when available over `MessageChannel`. ([#20834](https://github.com/facebook/react/pull/20834)  by [@gaearon](https://github.com/gaearon))
- Fix context failing to propagate inside suspended trees. ([#23095](https://github.com/facebook/react/pull/23095)  by [@gaearon](https://github.com/gaearon))
- Fix `useReducer` observing incorrect props by removing the eager bailout mechanism. ([#22445](https://github.com/facebook/react/pull/22445)  by [@josephsavona](https://github.com/josephsavona))
- Fix `setState` being ignored in Safari when appending iframes. ([#23111](https://github.com/facebook/react/pull/23111)  by [@gaearon](https://github.com/gaearon))
- Fix a crash when rendering `ZonedDateTime` in the tree. ([#20617](https://github.com/facebook/react/pull/20617)  by [@dimaqq](https://github.com/dimaqq))
- Fix a crash when document is set to `null` in tests. ([#22695](https://github.com/facebook/react/pull/22695)  by [@SimenB](https://github.com/SimenB))
- Fix `onLoad` not triggering when concurrent features are on. ([#23316](https://github.com/facebook/react/pull/23316)  by [@gnoff](https://github.com/gnoff))
- Fix a warning when a selector returns `NaN`.  ([#23333](https://github.com/facebook/react/pull/23333)  by [@hachibeeDI](https://github.com/hachibeeDI))
- Fix a crash when document is set to `null` in tests. ([#22695](https://github.com/facebook/react/pull/22695) by [@SimenB](https://github.com/SimenB))
- Fix the generated license header. ([#23004](https://github.com/facebook/react/pull/23004)  by [@vitaliemiron](https://github.com/vitaliemiron))
- Add `package.json` as one of the entry points. ([#22954](https://github.com/facebook/react/pull/22954)  by [@Jack](https://github.com/Jack-Works))
- Allow suspending outside a Suspense boundary. ([#23267](https://github.com/facebook/react/pull/23267)  by [@acdlite](https://github.com/acdlite))
- Log a recoverable error whenever hydration fails. ([#23319](https://github.com/facebook/react/pull/23319)  by [@acdlite](https://github.com/acdlite))

### React DOM

- Add `createRoot` and `hydrateRoot`. ([#10239](https://github.com/facebook/react/pull/10239), [#11225](https://github.com/facebook/react/pull/11225), [#12117](https://github.com/facebook/react/pull/12117), [#13732](https://github.com/facebook/react/pull/13732), [#15502](https://github.com/facebook/react/pull/15502), [#15532](https://github.com/facebook/react/pull/15532), [#17035](https://github.com/facebook/react/pull/17035), [#17165](https://github.com/facebook/react/pull/17165), [#20669](https://github.com/facebook/react/pull/20669), [#20748](https://github.com/facebook/react/pull/20748), [#20888](https://github.com/facebook/react/pull/20888), [#21072](https://github.com/facebook/react/pull/21072), [#21417](https://github.com/facebook/react/pull/21417), [#21652](https://github.com/facebook/react/pull/21652), [#21687](https://github.com/facebook/react/pull/21687), [#23207](https://github.com/facebook/react/pull/23207), [#23385](https://github.com/facebook/react/pull/23385) by [@acdlite](https://github.com/acdlite), [@bvaughn](https://github.com/bvaughn), [@gaearon](https://github.com/gaearon), [@lunaruan](https://github.com/lunaruan), [@rickhanlonii](https://github.com/rickhanlonii), [@trueadm](https://github.com/trueadm), and [@sebmarkbage](https://github.com/sebmarkbage))
- Add selective hydration. ([#14717](https://github.com/facebook/react/pull/14717), [#14884](https://github.com/facebook/react/pull/14884), [#16725](https://github.com/facebook/react/pull/16725), [#16880](https://github.com/facebook/react/pull/16880), [#17004](https://github.com/facebook/react/pull/17004), [#22416](https://github.com/facebook/react/pull/22416), [#22629](https://github.com/facebook/react/pull/22629), [#22448](https://github.com/facebook/react/pull/22448), [#22856](https://github.com/facebook/react/pull/22856), [#23176](https://github.com/facebook/react/pull/23176) by [@acdlite](https://github.com/acdlite), [@gaearon](https://github.com/gaearon), [@salazarm](https://github.com/salazarm), and [@sebmarkbage](https://github.com/sebmarkbage))
- Add `aria-description` to the list of known ARIA attributes. ([#22142](https://github.com/facebook/react/pull/22142)  by [@mahyareb](https://github.com/mahyareb))
- Add `onResize` event to video elements. ([#21973](https://github.com/facebook/react/pull/21973)  by [@rileyjshaw](https://github.com/rileyjshaw))
- Add `imageSizes` and `imageSrcSet` to known props. ([#22550](https://github.com/facebook/react/pull/22550)  by [@eps1lon](https://github.com/eps1lon))
- Allow non-string `<option>` children if `value` is provided.  ([#21431](https://github.com/facebook/react/pull/21431)  by [@sebmarkbage](https://github.com/sebmarkbage))
- Fix `aspectRatio` style not being applied. ([#21100](https://github.com/facebook/react/pull/21100)  by [@gaearon](https://github.com/gaearon))
- Warn if `renderSubtreeIntoContainer` is called. ([#23355](https://github.com/facebook/react/pull/23355)  by [@acdlite](https://github.com/acdlite))

### React DOM Server

- Add the new streaming renderer. ([#14144](https://github.com/facebook/react/pull/14144), [#20970](https://github.com/facebook/react/pull/20970), [#21056](https://github.com/facebook/react/pull/21056), [#21255](https://github.com/facebook/react/pull/21255), [#21200](https://github.com/facebook/react/pull/21200), [#21257](https://github.com/facebook/react/pull/21257), [#21276](https://github.com/facebook/react/pull/21276), [#22443](https://github.com/facebook/react/pull/22443), [#22450](https://github.com/facebook/react/pull/22450), [#23247](https://github.com/facebook/react/pull/23247), [#24025](https://github.com/facebook/react/pull/24025), [#24030](https://github.com/facebook/react/pull/24030) by [@sebmarkbage](https://github.com/sebmarkbage))
- Fix context providers in SSR when handling multiple requests. ([#23171](https://github.com/facebook/react/pull/23171)  by [@frandiox](https://github.com/frandiox))
- Revert to client render on text mismatch. ([#23354](https://github.com/facebook/react/pull/23354)  by [@acdlite](https://github.com/acdlite))
- Deprecate `renderToNodeStream`. ([#23359](https://github.com/facebook/react/pull/23359)  by [@sebmarkbage](https://github.com/sebmarkbage))
- Fix a spurious error log in the new server renderer. ([#24043](https://github.com/facebook/react/pull/24043)  by [@eps1lon](https://github.com/eps1lon))
- Fix a bug in the new server renderer. ([#22617](https://github.com/facebook/react/pull/22617)  by [@shuding](https://github.com/shuding))
- Ignore function and symbol values inside custom elements on the server. ([#21157](https://github.com/facebook/react/pull/21157)  by [@sebmarkbage](https://github.com/sebmarkbage))

### React DOM Test Utils

- Throw when `act` is used in production. ([#21686](https://github.com/facebook/react/pull/21686)  by [@acdlite](https://github.com/acdlite))
- Support disabling spurious act warnings with `global.IS_REACT_ACT_ENVIRONMENT`. ([#22561](https://github.com/facebook/react/pull/22561)  by [@acdlite](https://github.com/acdlite))
- Expand act warning to cover all APIs that might schedule React work. ([#22607](https://github.com/facebook/react/pull/22607)  by [@acdlite](https://github.com/acdlite))
- Make `act` batch updates. ([#21797](https://github.com/facebook/react/pull/21797)  by [@acdlite](https://github.com/acdlite))
- Remove warning for dangling passive effects. ([#22609](https://github.com/facebook/react/pull/22609)  by [@acdlite](https://github.com/acdlite))

### React Refresh

- Track late-mounted roots in Fast Refresh. ([#22740](https://github.com/facebook/react/pull/22740)  by [@anc95](https://github.com/anc95))
- Add `exports` field to `package.json`. ([#23087](https://github.com/facebook/react/pull/23087)  by [@otakustay](https://github.com/otakustay))

### Server Components (Experimental)

- Add Server Context support. ([#23244](https://github.com/facebook/react/pull/23244)  by [@salazarm](https://github.com/salazarm))
- Add `lazy` support. ([#24068](https://github.com/facebook/react/pull/24068)  by [@gnoff](https://github.com/gnoff))
- Update webpack plugin for webpack 5 ([#22739](https://github.com/facebook/react/pull/22739)  by [@michenly](https://github.com/michenly))
- Fix a mistake in the Node loader. ([#22537](https://github.com/facebook/react/pull/22537)  by [@btea](https://github.com/btea))
- Use `globalThis` instead of `window` for edge environments. ([#22777](https://github.com/facebook/react/pull/22777)  by [@huozhi](https://github.com/huozhi))

[PreviousReact Labs: What We've Been Working On – June 2022](https://react.dev/blog/2022/06/15/react-labs-what-we-have-been-working-on-june-2022)[NextHow to Upgrade to React 18](https://react.dev/blog/2022/03/08/react-18-upgrade-guide)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# React Labs: What We've Been Working On

[Blog](https://react.dev/blog)

# React Labs: What We've Been Working On – June 2022

June 15, 2022 by [Andrew Clark](https://twitter.com/acdlite), [Dan Abramov](https://bsky.app/profile/danabra.mov), [Jan Kassens](https://twitter.com/kassens), [Joseph Savona](https://twitter.com/en_JS), [Josh Story](https://twitter.com/joshcstory), [Lauren Tan](https://twitter.com/potetotes), [Luna Ruan](https://twitter.com/lunaruan), [Mengdi Chen](https://twitter.com/mengdi_en), [Rick Hanlon](https://twitter.com/rickhanlonii), [Robert Zhang](https://twitter.com/jiaxuanzhang01), [Sathya Gunasekaran](https://twitter.com/_gsathya), [Sebastian Markbåge](https://twitter.com/sebmarkbage), and [Xuan Huang](https://twitter.com/Huxpro)

---

[React 18](https://react.dev/blog/2022/03/29/react-v18) was years in the making, and with it brought valuable lessons for the React team. Its release was the result of many years of research and exploring many paths. Some of those paths were successful; many more were dead-ends that led to new insights. One lesson we’ve learned is that it’s frustrating for the community to wait for new features without having insight into these paths that we’re exploring.

---

We typically have a number of projects being worked on at any time, ranging from the more experimental to the clearly defined. Looking ahead, we’d like to start regularly sharing more about what we’ve been working on with the community across these projects.

To set expectations, this is not a roadmap with clear timelines. Many of these projects are under active research and are difficult to put concrete ship dates on. They may possibly never even ship in their current iteration depending on what we learn. Instead, we want to share with you the problem spaces we’re actively thinking about, and what we’ve learned so far.

## Server Components

We announced an [experimental demo of React Server Components](https://legacy.reactjs.org/blog/2020/12/21/data-fetching-with-react-server-components.html) (RSC) in December 2020. Since then we’ve been finishing up its dependencies in React 18, and working on changes inspired by experimental feedback.

In particular, we’re abandoning the idea of having forked I/O libraries (eg react-fetch), and instead adopting an async/await model for better compatibility. This doesn’t technically block RSC’s release because you can also use routers for data fetching. Another change is that we’re also moving away from the file extension approach in favor of [annotating boundaries](https://github.com/reactjs/rfcs/pull/189#issuecomment-1116482278).

We’re working together with Vercel and Shopify to unify bundler support for shared semantics in both webpack and Vite. Before launch, we want to make sure that the semantics of RSCs are the same across the whole React ecosystem. This is the major blocker for reaching stable.

## Asset Loading

Currently, assets like scripts, external styles, fonts, and images are typically preloaded and loaded using external systems. This can make it tricky to coordinate across new environments like streaming, Server Components, and more.
We’re looking at adding APIs to preload and load deduplicated external assets through React APIs that work in all React environments.

We’re also looking at having these support Suspense so you can have images, CSS, and fonts that block display until they’re loaded but don’t block streaming and concurrent rendering. This can help avoid [“popcorning“](https://twitter.com/sebmarkbage/status/1516852731251724293) as the visuals pop and layout shifts.

## Static Server Rendering Optimizations

Static Site Generation (SSG) and Incremental Static Regeneration (ISR) are great ways to get performance for cacheable pages, but we think we can add features to improve performance of dynamic Server Side Rendering (SSR) – especially when most but not all of the content is cacheable. We’re exploring ways to optimize server rendering utilizing compilation and static passes.

## React Optimizing Compiler

We gave an [early preview](https://www.youtube.com/watch?v=lGEMwh32soc) of React Forget at React Conf 2021. It’s a compiler that automatically generates the equivalent of `useMemo` and `useCallback` calls to minimize the cost of re-rendering, while retaining React’s programming model.

Recently, we finished a rewrite of the compiler to make it more reliable and capable. This new architecture allows us to analyze and memoize more complex patterns such as the use of [local mutations](https://react.dev/learn/keeping-components-pure#local-mutation-your-components-little-secret), and opens up many new compile-time optimization opportunities beyond just being on par with memoization Hooks.

We’re also working on a playground for exploring many aspects of the compiler. While the goal of the playground is to make development of the compiler easier, we think that it will make it easier to try it out and build intuition for what the compiler does. It reveals various insights into how it works under the hood, and live renders the compiler’s outputs as you type. This will be shipped together with the compiler when it’s released.

## Offscreen

Today, if you want to hide and show a component, you have two options. One is to add or remove it from the tree completely. The problem with this approach is that the state of your UI is lost each time you unmount, including state stored in the DOM, like scroll position.

The other option is to keep the component mounted and toggle the appearance visually using CSS. This preserves the state of your UI, but it comes at a performance cost, because React must keep rendering the hidden component and all of its children whenever it receives new updates.

Offscreen introduces a third option: hide the UI visually, but deprioritize its content. The idea is similar in spirit to the `content-visibility` CSS property: when content is hidden, it doesn’t need to stay in sync with the rest of the UI. React can defer the rendering work until the rest of the app is idle, or until the content becomes visible again.

Offscreen is a low level capability that unlocks high level features. Similar to React’s other concurrent features like `startTransition`, in most cases you won’t interact with the Offscreen API directly, but instead via an opinionated framework to implement patterns like:

- **Instant transitions.** Some routing frameworks already prefetch data to speed up subsequent navigations, like when hovering over a link. With Offscreen, they’ll also be able to prerender the next screen in the background.
- **Reusable state.** Similarly, when navigating between routes or tabs, you can use Offscreen to preserve the state of the previous screen so you can switch back and pick up where you left off.
- **Virtualized list rendering.** When displaying large lists of items, virtualized list frameworks will prerender more rows than are currently visible. You can use Offscreen to prerender the hidden rows at a lower priority than the visible items in the list.
- **Backgrounded content.** We’re also exploring a related feature for deprioritizing content in the background without hiding it, like when displaying a modal overlay.

## Transition Tracing

Currently, React has two profiling tools. The [original Profiler](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html) shows an overview of all the commits in a profiling session. For each commit, it also shows all components that rendered and the amount of time it took for them to render. We also have a beta version of a [Timeline Profiler](https://github.com/reactwg/react-18/discussions/76) introduced in React 18 that shows when components schedule updates and when React works on these updates. Both of these profilers help developers identify performance problems in their code.

We’ve realized that developers don’t find knowing about individual slow commits or components out of context that useful. It’s more useful to know about what actually causes the slow commits. And that developers want to be able to track specific interactions (eg a button click, an initial load, or a page navigation) to watch for performance regressions and to understand why an interaction was slow and how to fix it.

We previously tried to solve this issue by creating an [Interaction Tracing API](https://gist.github.com/bvaughn/8de925562903afd2e7a12554adcdda16), but it had some fundamental design flaws that reduced the accuracy of tracking why an interaction was slow and sometimes resulted in interactions never ending. We ended up [removing this API](https://github.com/facebook/react/pull/20037) because of these issues.

We are working on a new version for the Interaction Tracing API (tentatively called Transition Tracing because it is initiated via `startTransition`) that solves these problems.

## New React Docs

Last year, we announced the beta version of the new React documentation website ([later shipped as react.dev](https://react.dev/blog/2023/03/16/introducing-react-dev)) of the new React documentation website. The new learning materials teach Hooks first and has new diagrams, illustrations, as well as many interactive examples and challenges. We took a break from that work to focus on the React 18 release, but now that React 18 is out, we’re actively working to finish and ship the new documentation.

We are currently writing a detailed section about effects, as we’ve heard that is one of the more challenging topics for both new and experienced React users. [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) is the first published page in the series, and there are more to come in the following weeks. When we first started writing a detailed section about effects, we’ve realized that many common effect patterns can be simplified by adding a new primitive to React. We’ve shared some initial thoughts on that in the [useEvent RFC](https://github.com/reactjs/rfcs/pull/220). It is currently in early research, and we are still iterating on the idea. We appreciate the community’s comments on the RFC so far, as well as the [feedback](https://github.com/reactjs/react.dev/issues/3308) and contributions to the ongoing documentation rewrite. We’d specifically like to thank [Harish Kumar](https://github.com/harish-sethuraman) for submitting and reviewing many improvements to the new website implementation.

*Thanks toSophie Alpertfor reviewing this blog post!*

[PreviousIntroducing react.dev](https://react.dev/blog/2023/03/16/introducing-react-dev)[NextReact v18.0](https://react.dev/blog/2022/03/29/react-v18)
