# React 19.2 and more

# React 19.2

[Blog](https://react.dev/blog)

# React 19.2

October 1, 2025 by [The React Team](https://react.dev/community/team)

---

React 19.2 is now available on npm!

This is our third release in the last year, following React 19 in December and React 19.1 in June. In this post, we’ll give an overview of the new features in React 19.2, and highlight some notable changes.

- [New React Features](#new-react-features)
  - [<Activity />](#activity)
  - [useEffectEvent](#use-effect-event)
  - [cacheSignal](#cache-signal)
  - [Performance Tracks](#performance-tracks)
- [New React DOM Features](#new-react-dom-features)
  - [Partial Pre-rendering](#partial-pre-rendering)
- [Notable Changes](#notable-changes)
  - [Batching Suspense Boundaries for SSR](#batching-suspense-boundaries-for-ssr)
  - [SSR: Web Streams support for Node](#ssr-web-streams-support-for-node)
  - [eslint-plugin-react-hooksv6](#eslint-plugin-react-hooks)
  - [Update the defaultuseIdprefix](#update-the-default-useid-prefix)
- [Changelog](#changelog)

---

## New React Features

### <Activity />

`<Activity>` lets you break your app into “activities” that can be controlled and prioritized.

You can use Activity as an alternative to conditionally rendering parts of your app:

 $

```
// Before{isVisible && <Page />}// After<Activity mode={isVisible ? 'visible' : 'hidden'}>  <Page /></Activity>
```

/$

In React 19.2, Activity supports two modes: `visible` and `hidden`.

- `hidden`: hides the children, unmounts effects, and defers all updates until React has nothing left to work on.
- `visible`: shows the children, mounts effects, and allows updates to be processed normally.

This means you can pre-render and keep rendering hidden parts of the app without impacting the performance of anything visible on screen.

You can use Activity to render hidden parts of the app that a user is likely to navigate to next, or to save the state of parts the user navigates away from. This helps make navigations quicker by loading data, css, and images in the background, and allows back navigations to maintain state such as input fields.

In the future, we plan to add more modes to Activity for different use cases.

For examples on how to use Activity, check out the [Activity docs](https://react.dev/reference/react/Activity).

---

### useEffectEvent

One common pattern with `useEffect` is to notify the app code about some kind of “events” from an external system. For example, when a chat room gets connected, you might want to display a notification:

 $

```
function ChatRoom({ roomId, theme }) {  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.on('connected', () => {      showNotification('Connected!', theme);    });    connection.connect();    return () => {      connection.disconnect()    };  }, [roomId, theme]);  // ...
```

/$

The problem with the code above is that a change to any values used inside such an “event” will cause the surrounding Effect to re-run. For example, changing the `theme` will cause the chat room to reconnect. This makes sense for values related to the Effect logic itself, like `roomId`, but it doesn’t make sense for `theme`.

To solve this, most users just disable the lint rule and exclude the dependency. But that can lead to bugs since the linter can no longer help you keep the dependencies up to date if you need to update the Effect later.

With `useEffectEvent`, you can split the “event” part of this logic out of the Effect that emits it:

 $

```
function ChatRoom({ roomId, theme }) {  const onConnected = useEffectEvent(() => {    showNotification('Connected!', theme);  });  useEffect(() => {    const connection = createConnection(serverUrl, roomId);    connection.on('connected', () => {      onConnected();    });    connection.connect();    return () => connection.disconnect();  }, [roomId]); // ✅ All dependencies declared (Effect Events aren't dependencies)  // ...
```

/$

Similar to DOM events, Effect Events always “see” the latest props and state.

**Effect Events shouldnotbe declared in the dependency array**. You’ll need to upgrade to `eslint-plugin-react-hooks@latest` so that the linter doesn’t try to insert them as dependencies. Note that Effect Events can only be declared in the same component or Hook as “their” Effect. These restrictions are verified by the linter.

### Note

#### When to useuseEffectEvent

You should use `useEffectEvent` for functions that are conceptually “events” that happen to be fired from an Effect instead of a user event (that’s what makes it an “Effect Event”). You don’t need to wrap everything in `useEffectEvent`, or to use it just to silence the lint error, as this can lead to bugs.

For a deep dive on how to think about Event Effects, see: [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects#extracting-non-reactive-logic-out-of-effects).

---

### cacheSignal

### React Server Components

`cacheSignal` is only for use with [React Server Components](https://react.dev/reference/rsc/server-components).

`cacheSignal` allows you to know when the [cache()](https://react.dev/reference/react/cache) lifetime is over:

 $

```
import {cache, cacheSignal} from 'react';const dedupedFetch = cache(fetch);async function Component() {  await dedupedFetch(url, { signal: cacheSignal() });}
```

/$

This allows you to clean up or abort work when the result will no longer be used in the cache, such as:

- React has successfully completed rendering
- The render was aborted
- The render has failed

For more info, see the [cacheSignaldocs](https://react.dev/reference/react/cacheSignal).

---

### Performance Tracks

React 19.2 adds a new set of [custom tracks](https://developer.chrome.com/docs/devtools/performance/extension) to Chrome DevTools performance profiles to provide more information about the performance of your React app:

 ![image](https://react.dev/images/blog/react-labs-april-2025/perf_tracks.webp)![image](https://react.dev/images/blog/react-labs-april-2025/perf_tracks_dark.webp)

The [React Performance Tracks docs](https://react.dev/reference/dev-tools/react-performance-tracks) explain everything included in the tracks, but here is a high-level overview.

#### Scheduler ⚛

The Scheduler track shows what React is working on for different priorities such as “blocking” for user interactions, or “transition” for updates inside startTransition. Inside each track, you will see the type of work being performed such as the event that scheduled an update, and when the render for that update happened.

We also show information such as when an update is blocked waiting for a different priority, or when React is waiting for paint before continuing. The Scheduler track helps you understand how React splits your code into different priorities, and the order it completed the work.

See the [Scheduler track](https://react.dev/reference/dev-tools/react-performance-tracks#scheduler) docs to see everything included.

#### Components ⚛

The Components track shows the tree of components that React is working on either to render or run effects. Inside you’ll see labels such as “Mount” for when children mount or effects are mounted, or “Blocked” for when rendering is blocked due to yielding to work outside React.

The Components track helps you understand when components are rendered or run effects, and the time it takes to complete that work to help identify performance problems.

See the [Components track docs](https://react.dev/reference/dev-tools/react-performance-tracks#components) for see everything included.

---

## New React DOM Features

### Partial Pre-rendering

In 19.2 we’re adding a new capability to pre-render part of the app ahead of time, and resume rendering it later.

This feature is called “Partial Pre-rendering”, and allows you to pre-render the static parts of your app and serve it from a CDN, and then resume rendering the shell to fill it in with dynamic content later.

To pre-render an app to resume later, first call `prerender` with an `AbortController`:

 $

```
const {prelude, postponed} = await prerender(<App />, {  signal: controller.signal,});// Save the postponed state for laterawait savePostponedState(postponed);// Send prelude to client or CDN.
```

/$

Then, you can return the `prelude` shell to the client, and later call `resume` to “resume” to a SSR stream:

 $

```
const postponed = await getPostponedState(request);const resumeStream = await resume(<App />, postponed);// Send stream to client.
```

/$

Or you can call `resumeAndPrerender` to resume to get static HTML for SSG:

 $

```
const postponedState = await getPostponedState(request);const { prelude } = await resumeAndPrerender(<App />, postponedState);// Send complete HTML prelude to CDN.
```

/$

For more info, see the docs for the new APIs:

- `react-dom/server`
  - [resume](https://react.dev/reference/react-dom/server/resume): for Web Streams.
  - [resumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream) for Node Streams.
- `react-dom/static`
  - [resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender) for Web Streams.
  - [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream) for Node Streams.

Additionally, the prerender apis now return a `postpone` state to pass to the `resume` apis.

---

## Notable Changes

### Batching Suspense Boundaries for SSR

We fixed a behavioral bug where Suspense boundaries would reveal differently depending on if they were rendered on the client or when streaming from server-side rendering.

Starting in 19.2, React will batch reveals of server-rendered Suspense boundaries for a short time, to allow more content to be revealed together and align with the client-rendered behavior.

 ![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a page rectangle showing a glimmer loading state with faded bars. The second panel shows the top half of the page revealed and highlighted in blue. The third panel shows the entire the page revealed and highlighted in blue.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2F19_2_batching_before.dark.png&w=3840&q=75)![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a page rectangle showing a glimmer loading state with faded bars. The second panel shows the top half of the page revealed and highlighted in blue. The third panel shows the entire the page revealed and highlighted in blue.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2F19_2_batching_before.png&w=3840&q=75)

Previously, during streaming server-side rendering, suspense content would immediately replace fallbacks.

 ![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a page rectangle showing a glimmer loading state with faded bars. The second panel shows the same page. The third panel shows the entire the page revealed and highlighted in blue.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2F19_2_batching_after.dark.png&w=3840&q=75)![Diagram with three sections, with an arrow transitioning each section in between. The first section contains a page rectangle showing a glimmer loading state with faded bars. The second panel shows the same page. The third panel shows the entire the page revealed and highlighted in blue.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2F19_2_batching_after.png&w=3840&q=75)

In React 19.2, suspense boundaries are batched for a small amount of time, to allow revealing more content together.

This fix also prepares apps for supporting `<ViewTransition>` for Suspense during SSR. By revealing more content together, animations can run in larger batches of content, and avoid chaining animations of content that stream in close together.

### Note

React uses heuristics to ensure throttling does not impact core web vitals and search ranking.

For example, if the total page load time is approaching 2.5s (which is the time considered “good” for [LCP](https://web.dev/articles/lcp)), React will stop batching and reveal content immediately so that the throttling is not the reason to miss the metric.

---

### SSR: Web Streams support for Node

React 19.2 adds support for Web Streams for streaming SSR in Node.js:

- [renderToReadableStream](https://react.dev/reference/react-dom/server/renderToReadableStream) is now available for Node.js
- [prerender](https://react.dev/reference/react-dom/static/prerender) is now available for Node.js

As well as the new `resume` APIs:

- [resume](https://react.dev/reference/react-dom/server/resume) is available for Node.js.
- [resumeAndPrerender](https://react.dev/reference/react-dom/static/resumeAndPrerender) is available for Node.js.

### Pitfall

#### Prefer Node Streams for server-side rendering in Node.js

In Node.js environments, we still highly recommend using the Node Streams APIs:

- [renderToPipeableStream](https://react.dev/reference/react-dom/server/renderToPipeableStream)
- [resumeToPipeableStream](https://react.dev/reference/react-dom/server/resumeToPipeableStream)
- [prerenderToNodeStream](https://react.dev/reference/react-dom/static/prerenderToNodeStream)
- [resumeAndPrerenderToNodeStream](https://react.dev/reference/react-dom/static/resumeAndPrerenderToNodeStream)

This is because Node Streams are much faster than Web Streams in Node, and Web Streams do not support compression by default, leading to users accidentally missing the benefits of streaming.

---

### eslint-plugin-react-hooksv6

We also published `eslint-plugin-react-hooks@latest` with flat config by default in the `recommended` preset, and opt-in for new React Compiler powered rules.

To continue using the legacy config, you can change to `recommended-legacy`:

 $

```
- extends: ['plugin:react-hooks/recommended']+ extends: ['plugin:react-hooks/recommended-legacy']
```

/$

For a full list of compiler enabled rules, [check out the linter docs](https://react.dev/reference/eslint-plugin-react-hooks#recommended).

Check out the `eslint-plugin-react-hooks` [changelog for a full list of changes](https://github.com/facebook/react/blob/main/packages/eslint-plugin-react-hooks/CHANGELOG.md#610).

---

### Update the defaultuseIdprefix

In 19.2, we’re updating the default `useId` prefix from `:r:` (19.0.0) or `«r»` (19.1.0) to `_r_`.

The original intent of using a special character that was not valid for CSS selectors was that it would be unlikely to collide with IDs written by users. However, to support View Transitions, we need to ensure that IDs generated by `useId` are valid for `view-transition-name` and XML 1.0 names.

---

## Changelog

Other notable changes

- `react-dom`: Allow nonce to be used on hoistable styles [#32461](https://github.com/facebook/react/pull/32461)
- `react-dom`: Warn for using a React owned node as a Container if it also has text content [#32774](https://github.com/facebook/react/pull/32774)

Notable bug fixes

- `react`: Stringify context as “SomeContext” instead of “SomeContext.Provider” [#33507](https://github.com/facebook/react/pull/33507)
- `react`: Fix infinite useDeferredValue loop in popstate event [#32821](https://github.com/facebook/react/pull/32821)
- `react`: Fix a bug when an initial value was passed to useDeferredValue [#34376](https://github.com/facebook/react/pull/34376)
- `react`: Fix a crash when submitting forms with Client Actions [#33055](https://github.com/facebook/react/pull/33055)
- `react`: Hide/unhide the content of dehydrated suspense boundaries if they resuspend [#32900](https://github.com/facebook/react/pull/32900)
- `react`: Avoid stack overflow on wide trees during Hot Reload [#34145](https://github.com/facebook/react/pull/34145)
- `react`: Improve component stacks in various places [#33629](https://github.com/facebook/react/pull/33629), [#33724](https://github.com/facebook/react/pull/33724), [#32735](https://github.com/facebook/react/pull/32735), [#33723](https://github.com/facebook/react/pull/33723)
- `react`: Fix a bug with React.use inside React.lazy-ed Component [#33941](https://github.com/facebook/react/pull/33941)
- `react-dom`: Stop warning when ARIA 1.3 attributes are used [#34264](https://github.com/facebook/react/pull/34264)
- `react-dom`: Fix a bug with deeply nested Suspense inside Suspense fallbacks [#33467](https://github.com/facebook/react/pull/33467)
- `react-dom`: Avoid hanging when suspending after aborting while rendering [#34192](https://github.com/facebook/react/pull/34192)

For a full list of changes, please see the [Changelog](https://github.com/facebook/react/blob/main/CHANGELOG.md).

---

*Thanks toRicky Hanlonforwriting this post,Dan Abramov,Matt Carroll,Jack Pope, andJoe Savonafor reviewing this post.*

[PreviousIntroducing the React Foundation](https://react.dev/blog/2025/10/07/introducing-the-react-foundation)[NextReact Labs: View Transitions, Activity, and more](https://react.dev/blog/2025/04/23/react-labs-view-transitions-activity-and-more)

---

# Introducing the React Foundation

[Blog](https://react.dev/blog)

# Introducing the React Foundation

October 7, 2025 by [Seth Webster](https://x.com/sethwebster), [Matt Carroll](https://x.com/mattcarrollcode), [Joe Savona](https://x.com/en_JS), [Sophie Alpert](https://x.com/sophiebits)

---

 ![image](https://react.dev/images/blog/react-foundation/react_foundation_logo.webp)![image](https://react.dev/images/blog/react-foundation/react_foundation_logo_dark.webp)

Today, we’re announcing our plans to create the React Foundation and a new technical governance structure.

---

We open sourced React over a decade ago to help developers build great user experiences. From its earliest days, React has received substantial contributions from contributors outside of Meta. Over time, the number of contributors and the scope of their contributions has grown significantly. What started out as a tool developed for Meta has expanded into a project that spans multiple companies with regular contributions from across the ecosystem. React has outgrown the confines of any one company.

To better serve the React community, we are announcing our plans to move React and React Native from Meta to a new React Foundation. As a part of this change, we will also be implementing a new independent technical governance structure. We believe these changes will enable us to give React ecosystem projects more resources.

## The React Foundation

We will make the React Foundation the new home for React, React Native, and some supporting projects like JSX. The React Foundation’s mission will be to support the React community and ecosystem. Once implemented, the React Foundation will

- Maintain React’s infrastructure like GitHub, CI, and trademarks
- Organize React Conf
- Create initiatives to support the React ecosystem like financial support of ecosystem projects, issuing grants, and creating programs

The React Foundation will be governed by a board of directors, with Seth Webster serving as the executive director. This board will direct funds and resources to support React’s development, community, and ecosystem. We believe that this is the best structure to ensure that the React Foundation is vendor-neutral and reflects the best interests of the community.

The founding corporate members of the React Foundation will be Amazon, Callstack, Expo, Meta, Microsoft, Software Mansion, and Vercel. These companies have had a major impact on the React and React Native ecosystems and we are grateful for their support. We are excited to welcome even more members in the future.

 ![image](https://react.dev/images/blog/react-foundation/react_foundation_member_logos.webp)![image](https://react.dev/images/blog/react-foundation/react_foundation_member_logos_dark.webp)

## React’s technical governance

We believe that React’s technical direction should be set by the people who contribute to and maintain React. As React moves to a foundation, it is important that no single company or organization is overrepresented. To achieve this, we plan to define a new technical governance structure for React that is independent from the React Foundation.

As a part of creating React’s new technical governance structure we will reach out to the community for feedback. Once finalized, we will share details in a future post.

## Thank you

React’s incredible growth is thanks to the thousands of people, companies, and projects that have shaped React. The creation of the React Foundation is a testament to the strength and vibrancy of the React community. Together, the React Foundation and React’s new technical governance will ensure that React’s future is secure for years to come.

[PreviousReact Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1)[NextReact 19.2](https://react.dev/blog/2025/10/01/react-19-2)

---

# React Compiler v1.0

[Blog](https://react.dev/blog)

# React Compiler v1.0

Oct 7, 2025 by [Lauren Tan](https://x.com/potetotes), [Joe Savona](https://x.com/en_JS), and [Mofei Zhang](https://x.com/zmofei).

---

The React team is excited to share new updates:

1. React Compiler 1.0 is available today.
2. Compiler-powered lint rules ship in `eslint-plugin-react-hooks`’s `recommended` and `recommended-latest` preset.
3. We’ve published an incremental adoption guide, and partnered with Expo, Vite, and Next.js so new apps can start with the compiler enabled.

---

We are releasing the compiler’s first stable release today. React Compiler works on both React and React Native, and automatically optimizes components and hooks without requiring rewrites. The compiler has been battle tested on major apps at Meta and is fully production-ready.

[React Compiler](https://react.dev/learn/react-compiler) is a build-time tool that optimizes your React app through automatic memoization. Last year, we published React Compiler’s [first beta](https://react.dev/blog/2024/10/21/react-compiler-beta-release) and received lots of great feedback and contributions. We’re excited about the wins we’ve seen from folks adopting the compiler (see case studies from [Sanity Studio](https://github.com/reactwg/react-compiler/discussions/33) and [Wakelet](https://github.com/reactwg/react-compiler/discussions/52)) and are excited to bring the compiler to more users in the React community.

This release is the culmination of a huge and complex engineering effort spanning almost a decade. The React team’s first exploration into compilers started with [Prepack](https://github.com/facebookarchive/prepack) in 2017. While this project was eventually shut down, there were many learnings that informed the team on the design of Hooks, which were designed with a future compiler in mind. In 2021, [Xuan Huang](https://x.com/Huxpro) demoed the [first iteration](https://www.youtube.com/watch?v=lGEMwh32soc) of a new take on React Compiler.

Although this first version of the new React Compiler was eventually rewritten, the first prototype gave us increased confidence that this was a tractable problem, and the learnings that an alternative compiler architecture could precisely give us the memoization characteristics we wanted. [Joe Savona](https://x.com/en_JS), [Sathya Gunasekaran](https://x.com/_gsathya), [Mofei Zhang](https://x.com/zmofei), and [Lauren Tan](https://x.com/potetotes) worked through our first rewrite, moving the compiler’s architecture into a Control Flow Graph (CFG) based High-Level Intermediate Representation (HIR). This paved the way for much more precise analysis and even type inference within React Compiler. Since then, many significant portions of the compiler have been rewritten, with each rewrite informed by our learnings from the previous attempt. And we have received significant help and contributions from many members of the [React team](https://react.dev/community/team) along the way.

This stable release is our first of many. The compiler will continue to evolve and improve, and we expect to see it become a new foundation and era for the next decade and more of React.

You can jump straight to the [quickstart](https://react.dev/learn/react-compiler), or read on for the highlights from React Conf 2025.

##### Deep Dive

#### How does React Compiler work?

React Compiler is an optimizing compiler that optimizes components and hooks through automatic memoization. While it is implemented as a Babel plugin currently, the compiler is largely decoupled from Babel and lowers the Abstract Syntax Tree (AST) provided by Babel into its own novel HIR, and through multiple compiler passes, carefully understands data-flow and mutability of your React code. This allows the compiler to granularly memoize values used in rendering, including the ability to memoize conditionally, which is not possible through manual memoization.

$

```
import { use } from 'react';export default function ThemeProvider(props) {  if (!props.children) {    return null;  }  // The compiler can still memoize code after a conditional return  const theme = mergeTheme(props.theme, use(ThemeContext));  return (    <ThemeContext value={theme}>      {props.children}    </ThemeContext>  );}
```

/$

*See this example in theReact Compiler Playground*

In addition to automatic memoization, React Compiler also has validation passes that run on your React code. These passes encode the [Rules of React](https://react.dev/reference/rules), and uses the compiler’s understanding of data-flow and mutability to provide diagnostics where the Rules of React are broken. These diagnostics often expose latent bugs hiding in React code, and are primarily surfaced through `eslint-plugin-react-hooks`.

To learn more about how the compiler optimizes your code, visit the [Playground](https://playground.react.dev).

## Use React Compiler Today

To install the compiler:

npm

  Terminal

```
npm install --save-dev --save-exact babel-plugin-react-compiler@latest
```

pnpm

  Terminal

```
pnpm add --save-dev --save-exact babel-plugin-react-compiler@latest
```

yarn

  Terminal

```
yarn add --dev --exact babel-plugin-react-compiler@latest
```

As part of the stable release, we’ve been making React Compiler easier to add to your projects and added optimizations to how the compiler generates memoization. React Compiler now supports optional chains and array indices as dependencies. These improvements ultimately result in fewer re-renders and more responsive UIs, while letting you keep writing idiomatic declarative code.

You can find more details on using the Compiler in [our docs](https://react.dev/learn/react-compiler).

## What we’re seeing in production

[The compiler has already shipped in apps like Meta Quest Store](https://youtu.be/lyEKhv8-3n0?t=3002). We’ve seen initial loads and cross-page navigations improve by up to 12%, while certain interactions are more than 2.5× faster. Memory usage stays neutral even with these wins. Although your mileage may vary, we recommend experimenting with the compiler in your app to see similar performance gains.

## Backwards Compatibility

As noted in the Beta announcement, React Compiler is compatible with React 17 and up. If you are not yet on React 19, you can use React Compiler by specifying a minimum target in your compiler config, and adding `react-compiler-runtime` as a dependency. You can find docs on this [here](https://react.dev/reference/react-compiler/target#targeting-react-17-or-18).

## Enforce the Rules of React with compiler-powered linting

React Compiler includes an ESLint rule that helps identify code that breaks the [Rules of React](https://react.dev/reference/rules). The linter does not require the compiler to be installed, so there’s no risk in upgrading eslint-plugin-react-hooks. We recommend everyone upgrade today.

If you have already installed `eslint-plugin-react-compiler`, you can now remove it and use `eslint-plugin-react-hooks@latest`. Many thanks to [@michaelfaith](https://bsky.app/profile/michael.faith) for contributing to this improvement!

To install:

npm

  Terminal

```
npm install --save-dev eslint-plugin-react-hooks@latest
```

pnpm

  Terminal

```
pnpm add --save-dev eslint-plugin-react-hooks@latest
```

yarn

  Terminal

```
yarn add --dev eslint-plugin-react-hooks@latest
```

 $

```
// eslint.config.js (Flat Config)import reactHooks from 'eslint-plugin-react-hooks';import { defineConfig } from 'eslint/config';export default defineConfig([  reactHooks.configs.flat.recommended,]);
```

/$ $

```
// eslintrc.json (Legacy Config){  "extends": ["plugin:react-hooks/recommended"],  // ...}
```

/$

To enable React Compiler rules, we recommend using the `recommended` preset. You can also check out the [README](https://github.com/facebook/react/blob/main/packages/eslint-plugin-react-hooks/README.md) for more instructions. Here are a few examples we featured at React Conf:

- Catching `setState` patterns that cause render loops with [set-state-in-render](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-render).
- Flagging expensive work inside effects via [set-state-in-effect](https://react.dev/reference/eslint-plugin-react-hooks/lints/set-state-in-effect).
- Preventing unsafe ref access during render with [refs](https://react.dev/reference/eslint-plugin-react-hooks/lints/refs).

## What should I do about useMemo, useCallback, and React.memo?

By default, React Compiler will memoize your code based on its analysis and heuristics. In most cases, this memoization will be as precise, or moreso, than what you may have written — and as noted above, the compiler can memoize even in cases where `useMemo`/`useCallback` cannot be used, such as after an early return.

However, in some cases developers may need more control over memoization. The `useMemo` and `useCallback` hooks can continue to be used with React Compiler as an escape hatch to provide control over which values are memoized. A common use-case for this is if a memoized value is used as an effect dependency, in order to ensure that an effect does not fire repeatedly even when its dependencies do not meaningfully change.

For new code, we recommend relying on the compiler for memoization and using `useMemo`/`useCallback` where needed to achieve precise control.

For existing code, we recommend either leaving existing memoization in place (removing it can change compilation output) or carefully testing before removing the memoization.

## New apps should use React Compiler

We have partnered with the Expo, Vite, and Next.js teams to add the compiler to the new app experience.

[Expo SDK 54](https://docs.expo.dev/guides/react-compiler/) and up has the compiler enabled by default, so new apps will automatically be able to take advantage of the compiler from the start.

  Terminal

```
npx create-expo-app@latest
```

[Vite](https://vite.dev/guide/) and [Next.js](https://nextjs.org/docs/app/api-reference/cli/create-next-app) users can choose the compiler enabled templates in `create-vite` and `create-next-app`.

  Terminal

```
npm create vite@latest
```

  Terminal

```
npx create-next-app@latest
```

## Adopt React Compiler incrementally

If you’re maintaining an existing application, you can roll out the compiler at your own pace. We published a step-by-step [incremental adoption guide](https://react.dev/learn/react-compiler/incremental-adoption) that covers gating strategies, compatibility checks, and rollout tooling so you can enable the compiler with confidence.

## swc support (experimental)

React Compiler can be installed across [several build tools](https://react.dev/learn/react-compiler#installation) such as Babel, Vite, and Rsbuild.

In addition to those tools, we have been collaborating with Kang Dongyoon ([@kdy1dev](https://x.com/kdy1dev)) from the [swc](https://swc.rs/) team on adding additional support for React Compiler as an swc plugin. While this work isn’t done, Next.js build performance should now be considerably faster when the [React Compiler is enabled in your Next.js app](https://nextjs.org/docs/app/api-reference/config/next-config-js/reactCompiler).

We recommend using Next.js [15.3.1](https://github.com/vercel/next.js/releases/tag/v15.3.1) or greater to get the best build performance.

Vite users can continue to use [vite-plugin-react](https://github.com/vitejs/vite-plugin-react) to enable the compiler, by adding it as a [Babel plugin](https://react.dev/learn/react-compiler/installation#vite). We are also working with the [oxc](https://oxc.rs/) team to [add support for the compiler](https://github.com/oxc-project/oxc/issues/10048). Once [rolldown](https://github.com/rolldown/rolldown) is officially released and supported in Vite and oxc support is added for React Compiler, we’ll update the docs with information on how to migrate.

## Upgrading React Compiler

React Compiler works best when the auto-memoization applied is strictly for performance. Future versions of the compiler may change how memoization is applied, for example it could become more granular and precise.

However, because product code may sometimes break the [rules of React](https://react.dev/reference/rules) in ways that aren’t always statically detectable in JavaScript, changing memoization can occasionally have unexpected results. For example, a previously memoized value might be used as a dependency for a `useEffect` somewhere in the component tree. Changing how or whether this value is memoized can cause over or under-firing of that `useEffect`. While we encourage [useEffect only for synchronization](https://react.dev/learn/synchronizing-with-effects), your codebase may have `useEffect`s that cover other use cases, such as effects that needs to only run in response to specific values changing.

In other words, changing memoization may under rare circumstances cause unexpected behavior. For this reason, we recommend following the Rules of React and employing continuous end-to-end testing of your app so you can upgrade the compiler with confidence and identify any rules of React violations that might cause issues.

If you don’t have good test coverage, we recommend pinning the compiler to an exact version (eg `1.0.0`) rather than a SemVer range (eg `^1.0.0`). You can do this by passing the `--save-exact` (npm/pnpm) or `--exact` flags (yarn) when upgrading the compiler. You should then do any upgrades of the compiler manually, taking care to check that your app still works as expected.

---

Thanks to [Jason Bonta](https://x.com/someextent), [Jimmy Lai](https://x.com/feedthejim), [Kang Dongyoon](https://x.com/kdy1dev) (@kdy1dev), and [Dan Abramov](https://bsky.app/profile/danabra.mov) for reviewing and editing this post.

[PreviousReact Conf 2025 Recap](https://react.dev/blog/2025/10/16/react-conf-2025-recap)[NextIntroducing the React Foundation](https://react.dev/blog/2025/10/07/introducing-the-react-foundation)

---

# React Conf 2025 Recap

[Blog](https://react.dev/blog)

# React Conf 2025 Recap

Oct 16, 2025 by [Matt Carroll](https://x.com/mattcarrollcode) and [Ricky Hanlon](https://bsky.app/profile/ricky.fm)

---

Last week we hosted React Conf 2025 where we announced the [React Foundation](https://react.dev/blog/2025/10/07/introducing-the-react-foundation) and showcased new features coming to React and React Native.

---

React Conf 2025 was held on October 7-8, 2025, in Henderson, Nevada.

The entire [day 1](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=1067s) and [day 2](https://www.youtube.com/watch?v=p9OcztRyDl0&t=2299s) streams are available online, and you can view photos from the event [here](https://conf.react.dev/photos).

In this post, we’ll summarize the talks and announcements from the event.

## Day 1 Keynote

*Watch the full day 1 streamhere.*

In the day 1 keynote, Joe Savona shared the updates from the team and community since the last React Conf and highlights from React 19.0 and 19.1.

Mofei Zhang highlighted the new features in React 19.2 including:

- [<Activity />](https://react.dev/reference/react/Activity)  — a new component to manage visibility.
- [useEffectEvent](https://react.dev/reference/react/useEffectEvent) to fire events from Effects.
- [Performance Tracks](https://react.dev/reference/dev-tools/react-performance-tracks) — a new profiling tool in DevTools.
- [Partial Pre-Rendering](https://react.dev/blog/2025/10/01/react-19-2#partial-pre-rendering) to pre-render part of an app ahead of time, and resume rendering it later.

Jack Pope announced new features in Canary including:

- [<ViewTransition />](https://react.dev/reference/react/ViewTransition) — a new component to animate page transitions.
- [Fragment Refs](https://react.dev/reference/react/Fragment#fragmentinstance) — a new way to interact with the DOM nodes wrapped by a Fragment.

Lauren Tan announced [React Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1) and recommended all apps use React Compiler for benefits like:

- [Automatic memoization](https://react.dev/learn/react-compiler/introduction#what-does-react-compiler-do) that understands React code.
- [New lint rules](https://react.dev/learn/react-compiler/installation#eslint-integration) powered by React Compiler to teach best practices.
- [Default support](https://react.dev/learn/react-compiler/installation#basic-setup) for new apps in Vite, Next.js, and Expo.
- [Migration guides](https://react.dev/learn/react-compiler/incremental-adoption) for existing apps migrating to React Compiler.

Finally, Seth Webster announced the [React Foundation](https://react.dev/blog/2025/10/07/introducing-the-react-foundation) to steward React’s open source development and community.

Watch day 1 here:

## Day 2 Keynote

*Watch the full day 2 streamhere.*

Jorge Cohen and Nicola Corti kicked off day 2 highlighting React Native’s incredible growth with 4M weekly downloads (100% growth YoY), and some notable app migrations from Shopify, Zalando, and HelloFresh, award-winning apps like RISE, RUNNA, and Partyful, and AI apps from Mistral, Replit, and v0.

Riccardo Cipolleschi shared two major announcements for React Native:

- [React Native 0.82 will be New Architecture only](https://reactnative.dev/blog/2025/10/08/react-native-0.82#new-architecture-only)
- [Experimental Hermes V1 support](https://reactnative.dev/blog/2025/10/08/react-native-0.82#experimental-hermes-v1)

Ruben Norte and Alex Hunt finished out the keynote by announcing:

- [New web-aligned DOM APIs](https://reactnative.dev/blog/2025/10/08/react-native-0.82#dom-node-apis) for improved compatibility with React on the web.
- [New Performance APIs](https://reactnative.dev/blog/2025/10/08/react-native-0.82#web-performance-apis-canary) with a new network panel and desktop app.

Watch day 2 here:

## React team talks

Throughout the conference, there were talks from the React team including:

- [Async React Part I](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=10907s) and [Part II](https://www.youtube.com/watch?v=p9OcztRyDl0&t=29073s) [(Ricky Hanlon)](https://x.com/rickhanlonii) showed what’s possible using the last 10 years of innovation.
- [Exploring React Performance](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=20274s) [(Joe Savona)](https://x.com/en_js) showed the results of our React performance research.
- [Reimagining Lists in React Native](https://www.youtube.com/watch?v=p9OcztRyDl0&t=10382s) [(Luna Wei)](https://x.com/lunaleaps) introduced Virtual View, a new primitive for lists that manages visibility with mode-based rendering (hidden/pre-render/visible).
- [Profiling with React Performance tracks](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=8276s) [(Ruslan Lesiutin)](https://x.com/ruslanlesiutin) showed how to use the new React Performance Tracks to debug performance issues and build great apps.
- [React Strict DOM](https://www.youtube.com/watch?v=p9OcztRyDl0&t=9026s) [(Nicolas Gallagher)](https://nicolasgallagher.com/) talked about Meta’s approach to using web code on native.
- [View Transitions and Activity](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=4870s) [(Chance Strickland)](https://x.com/chancethedev) — Chance worked with the React team to showcase how to use `<Activity />` and `<ViewTransition />` to build fast, native-feeling animations.
- [In case you missed the memo](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=9525s) [(Cody Olsen)](https://bsky.app/profile/codey.bsky.social) - Cody worked with the React team to adopt the Compiler at Sanity Studio, and shared how it went.

## React framework talks

The second half of day 2 had a series of talks from React Framework teams including:

- [React Native, Amplified](https://www.youtube.com/watch?v=p9OcztRyDl0&t=5737s) by [Giovanni Laquidara](https://x.com/giolaq) and [Eric Fahsl](https://x.com/efahsl).
- [React Everywhere: Bringing React Into Native Apps](https://www.youtube.com/watch?v=p9OcztRyDl0&t=18213s) by [Mike Grabowski](https://x.com/grabbou).
- [How Parcel Bundles React Server Components](https://www.youtube.com/watch?v=p9OcztRyDl0&t=19538s) by [Devon Govett](https://x.com/devonovett).
- [Designing Page Transitions](https://www.youtube.com/watch?v=p9OcztRyDl0&t=20640s) by [Delba de Oliveira](https://x.com/delba_oliveira).
- [Build Fast, Deploy Faster — Expo in 2025](https://www.youtube.com/watch?v=p9OcztRyDl0&t=21350s) by [Evan Bacon](https://x.com/baconbrix).
- [The React Router’s take on RSC](https://www.youtube.com/watch?v=p9OcztRyDl0&t=22367s) by [Kent C. Dodds](https://x.com/kentcdodds).
- [RedwoodSDK: Web Standards Meet Full-Stack React](https://www.youtube.com/watch?v=p9OcztRyDl0&t=24992s) by [Peter Pistorius](https://x.com/appfactory) and [Aurora Scharff](https://x.com/aurorascharff).
- [TanStack Start](https://www.youtube.com/watch?v=p9OcztRyDl0&t=26065s) by [Tanner Linsley](https://x.com/tannerlinsley).

## Q&A

There were three Q&A panels during the conference:

- [React Team at Meta Q&A](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=26304s) hosted by [Shruti Kapoor](https://x.com/shrutikapoor08)
- [React Frameworks Q&A](https://www.youtube.com/watch?v=p9OcztRyDl0&t=26812s) hosted by [Jack Herrington](https://x.com/jherr)
- [React and AI Panel](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=18741s) hosted by [Lee Robinson](https://x.com/leerob)

## And more…

We also heard talks from the community including:

- [Building an MCP Server](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=24204s) by [James Swinton](https://x.com/JamesSwintonDev) ([AG Grid](https://www.ag-grid.com/?utm_source=react-conf&utm_medium=react-conf-homepage&utm_campaign=react-conf-sponsorship-2025))
- [Modern Emails using React](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=25521s) by [Zeno Rocha](https://x.com/zenorocha) ([Resend](https://resend.com/))
- [Why React Native Apps Make All the Money](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=24917s) by [Perttu Lähteenlahti](https://x.com/plahteenlahti) ([RevenueCat](https://www.revenuecat.com/))
- [The invisible craft of great UX](https://www.youtube.com/watch?v=zyVRg2QR6LA&t=23400s) by [Michał Dudak](https://x.com/michaldudak) ([MUI](https://mui.com/))

## Thanks

Thank you to all the staff, speakers, and participants, who made React Conf 2025 possible. There are too many to list, but we want to thank a few in particular.

Thank you to [Matt Carroll](https://x.com/mattcarrollcode) for planning the entire event and building the conference website.

Thank you to [Michael Chan](https://x.com/chantastic) for MCing React Conf with incredible dedication and energy, delivering thoughtful speaker intros, fun jokes, and genuine enthusiasm throughout the event. Thank you to [Jorge Cohen](https://x.com/JorgeWritesCode) for hosting the livestream, interviewing each speaker, and bringing the in-person React Conf experience online.

Thank you to [Mateusz Kornacki](https://x.com/mat_kornacki), [Mike Grabowski](https://x.com/grabbou), [Kris Lis](https://www.linkedin.com/in/krzysztoflisakakris/) and the team at [Callstack](https://www.callstack.com/) for co-organizing React Conf and providing design, engineering, and marketing support. Thank you to the [ZeroSlope team](https://zeroslopeevents.com/contact-us/): Sunny Leggett, Tracey Harrison, Tara Larish, Whitney Pogue, and Brianne Smythia for helping to organize the event.

Thank you to [Jorge Cabiedes Acosta](https://github.com/jorge-cab), [Gijs Weterings](https://x.com/gweterings), [Tim Yung](https://x.com/yungsters), and [Jason Bonta](https://x.com/someextent) for bringing questions from the Discord to the livestream. Thank you to [Lynn Yu](https://github.com/lynnshaoyu) for leading the moderation of the Discord. Thank you to [Seth Webster](https://x.com/sethwebster) for welcoming us each day; and to [Christopher Chedeau](https://x.com/vjeux), [Kevin Gozali](https://x.com/fkgozali), and [Pieter De Baets](https://x.com/Javache) for joining us with a special message during the after-party.

Thank you to [Kadi Kraman](https://x.com/kadikraman), [Beto](https://x.com/betomoedano) and [Nicolas Solerieu](https://www.linkedin.com/in/nicolas-solerieu/) for building the conference mobile app. Thank you [Wojtek Szafraniec](https://x.com/wojteg1337) for help with the conference website. Thank you to [Mustache](https://www.mustachepower.com/) & [Cornerstone](https://cornerstoneav.com/) for the visuals, stage, and sound; and to the Westin Hotel for hosting us.

Thank you to all the sponsors who made the event possible: [Amazon](https://www.developer.amazon.com), [MUI](https://mui.com/), [Vercel](https://vercel.com/), [Expo](https://expo.dev/), [RedwoodSDK](https://rwsdk.com), [Ag Grid](https://www.ag-grid.com), [RevenueCat](https://www.revenuecat.com/), [Resend](https://resend.com), [Mux](https://www.mux.com/), [Old Mission](https://www.oldmissioncapital.com/), [Arcjet](https://arcjet.com), [Infinite Red](https://infinite.red/), and [RenderATL](https://renderatl.com).

Thank you to all the speakers who shared their knowledge and experience with the community.

Finally, thank you to everyone who attended in person and online to show what makes React, React. React is more than a library, it is a community, and it was inspiring to see everyone come together to share and learn together.

See you next time!

[PreviousCritical Security Vulnerability in React Server Components](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components)[NextReact Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
