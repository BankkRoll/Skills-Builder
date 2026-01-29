# Not Found and more

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# Introducing Zero

[Blog](https://react.dev/blog)

# Introducing Zero-Bundle-Size React Server Components

December 21, 2020 by [Dan Abramov](https://bsky.app/profile/danabra.mov), [Lauren Tan](https://twitter.com/potetotes), [Joseph Savona](https://twitter.com/en_JS), and [Sebastian Markbåge](https://twitter.com/sebmarkbage)

---

2020 has been a long year. As it comes to an end we wanted to share a special Holiday Update on our research into zero-bundle-size **React Server Components**.

---

To introduce React Server Components, we have prepared a talk and a demo. If you want, you can check them out during the holidays, or later when work picks back up in the new year.

**React Server Components are still in research and development.** We are sharing this work in the spirit of transparency and to get initial feedback from the React community. There will be plenty of time for that, so **don’t feel like you have to catch up right now!**

If you want to check them out, we recommend going in the following order:

1. **Watch the talk** to learn about React Server Components and see the demo.
2. **Clone the demo** to play with React Server Components on your computer.
3. **Read the RFC (with FAQ at the end)** for a deeper technical breakdown and to provide feedback.

We are excited to hear from you on the RFC or in replies to the [@reactjs](https://twitter.com/reactjs) Twitter handle. Happy holidays, stay safe, and see you next year!

[PreviousThe Plan for React 18](https://react.dev/blog/2021/06/08/the-plan-for-react-18)[NextOlder posts](https://reactjs.org/blog/all.html)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# The Plan for React 18

[Blog](https://react.dev/blog)

# The Plan for React 18

June 8, 2021 by [Andrew Clark](https://twitter.com/acdlite), [Brian Vaughn](https://github.com/bvaughn), [Christine Abernathy](https://twitter.com/abernathyca), [Dan Abramov](https://bsky.app/profile/danabra.mov), [Rachel Nabors](https://twitter.com/rachelnabors), [Rick Hanlon](https://twitter.com/rickhanlonii), [Sebastian Markbåge](https://twitter.com/sebmarkbage), and [Seth Webster](https://twitter.com/sethwebster)

---

The React team is excited to share a few updates:

1. We’ve started work on the React 18 release, which will be our next major version.
2. We’ve created a Working Group to prepare the community for gradual adoption of new features in React 18.
3. We’ve published a React 18 Alpha so that library authors can try it and provide feedback.

These updates are primarily aimed at maintainers of third-party libraries. If you’re learning, teaching, or using React to build user-facing applications, you can safely ignore this post. But you are welcome to follow the discussions in the React 18 Working Group if you’re curious!

---

## What’s coming in React 18

When it’s released, React 18 will include out-of-the-box improvements (like [automatic batching](https://github.com/reactwg/react-18/discussions/21)), new APIs (like [startTransition](https://github.com/reactwg/react-18/discussions/41)), and a [new streaming server renderer](https://github.com/reactwg/react-18/discussions/37) with built-in support for `React.lazy`.

These features are possible thanks to a new opt-in mechanism we’re adding in React 18. It’s called “concurrent rendering” and it lets React prepare multiple versions of the UI at the same time. This change is mostly behind-the-scenes, but it unlocks new possibilities to improve both real and perceived performance of your app.

If you’ve been following our research into the future of React (we don’t expect you to!), you might have heard of something called “concurrent mode” or that it might break your app. In response to this feedback from the community, we’ve redesigned the upgrade strategy for gradual adoption. Instead of an all-or-nothing “mode”, concurrent rendering will only be enabled for updates triggered by one of the new features. In practice, this means **you will be able to adopt React 18 without rewrites and try the new features at your own pace.**

## A gradual adoption strategy

Since concurrency in React 18 is opt-in, there are no significant out-of-the-box breaking changes to component behavior. **You can upgrade to React 18 with minimal or no changes to your application code, with a level of effort comparable to a typical major React release**. Based on our experience converting several apps to React 18, we expect that many users will be able to upgrade within a single afternoon.

We successfully shipped concurrent features to tens of thousands of components at Facebook, and in our experience, we’ve found that most React components “just work” without additional changes. We’re committed to making sure this is a smooth upgrade for the entire community, so today we’re announcing the React 18 Working Group.

## Working with the community

We’re trying something new for this release: We’ve invited a panel of experts, developers, library authors, and educators from across the React community to participate in our [React 18 Working Group](https://github.com/reactwg/react-18) to provide feedback, ask questions, and collaborate on the release. We couldn’t invite everyone we wanted to this initial, small group, but if this experiment works out, we hope there will be more in the future!

**The goal of the React 18 Working Group is to prepare the ecosystem for a smooth, gradual adoption of React 18 by existing applications and libraries.** The Working Group is hosted on [GitHub Discussions](https://github.com/reactwg/react-18/discussions) and is available for the public to read. Members of the working group can leave feedback, ask questions, and share ideas. The core team will also use the discussions repo to share our research findings. As the stable release gets closer, any important information will also be posted on this blog.

For more information on upgrading to React 18, or additional resources about the release, see the [React 18 announcement post](https://github.com/reactwg/react-18/discussions/4).

## Accessing the React 18 Working Group

Everyone can read the discussions in the [React 18 Working Group repo](https://github.com/reactwg/react-18).

Because we expect an initial surge of interest in the Working Group, only invited members will be allowed to create or comment on threads. However, the threads are fully visible to the public, so everyone has access to the same information. We believe this is a good compromise between creating a productive environment for working group members, while maintaining transparency with the wider community.

As always, you can submit bug reports, questions, and general feedback to our [issue tracker](https://github.com/facebook/react/issues).

## How to try React 18 Alpha today

New alphas are [regularly published to npm using the@alphatag](https://github.com/reactwg/react-18/discussions/9). These releases are built using the most recent commit to our main repo. When a feature or bugfix is merged, it will appear in an alpha the following weekday.

There may be significant behavioral or API changes between alpha releases. Please remember that **alpha releases are not recommended for user-facing, production applications**.

## Projected React 18 release timeline

We don’t have a specific release date scheduled, but we expect it will take several months of feedback and iteration before React 18 is ready for most production applications.

- Library Alpha: Available today
- Public Beta: At least several months
- Release Candidate (RC): At least several weeks after Beta
- General Availability: At least several weeks after RC

More details about our projected release timeline are [available in the Working Group](https://github.com/reactwg/react-18/discussions/9). We’ll post updates on this blog when we’re closer to a public release.

[PreviousReact Conf 2021 Recap](https://react.dev/blog/2021/12/17/react-conf-2021-recap)[NextIntroducing Server Components](https://react.dev/blog/2020/12/21/data-fetching-with-react-server-components)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# React Conf 2021 Recap

[Blog](https://react.dev/blog)

# React Conf 2021 Recap

December 17, 2021 by [Jesslyn Tannady](https://twitter.com/jtannady) and [Rick Hanlon](https://twitter.com/rickhanlonii)

---

Last week we hosted our 6th React Conf. In previous years, we’ve used the React Conf stage to deliver industry changing announcements such as [React Native](https://engineering.fb.com/2015/03/26/android/react-native-bringing-modern-web-techniques-to-mobile/) and [React Hooks](https://reactjs.org/docs/hooks-intro.html). This year, we shared our multi-platform vision for React, starting with the release of React 18 and gradual adoption of concurrent features.

---

This was the first time React Conf was hosted online, and it was streamed for free, translated to 8 different languages. Participants from all over the world joined our conference Discord and the replay event for accessibility in all timezones. Over 50,000 people registered, with over 60,000 views of 19 talks, and 5,000 participants in Discord across both events.

All the talks are [available to stream online](https://www.youtube.com/watch?v=FZ0cG47msEk&list=PLNG_1j3cPCaZZ7etkzWA7JfdmKWT0pMsa).

Here’s a summary of what was shared on stage:

## React 18 and concurrent features

In the keynote, we shared our vision for the future of React starting with React 18.

React 18 adds the long-awaited concurrent renderer and updates to Suspense without any major breaking changes. Apps can upgrade to React 18 and begin gradually adopting concurrent features with the amount of effort on par with any other major release.

**This means there is no concurrent mode, only concurrent features.**

In the keynote, we also shared our vision for Suspense, Server Components, new React working groups, and our long-term many-platform vision for React Native.

Watch the full keynote from [Andrew Clark](https://twitter.com/acdlite), [Juan Tejada](https://twitter.com/_jstejada), [Lauren Tan](https://twitter.com/potetotes), and [Rick Hanlon](https://twitter.com/rickhanlonii) here:

## React 18 for Application Developers

In the keynote, we also announced that the React 18 RC is available to try now. Pending further feedback, this is the exact version of React that we will publish to stable early next year.

To try the React 18 RC, upgrade your dependencies:

 $

```
npm install react@rc react-dom@rc
```

/$

and switch to the new `createRoot` API:

 $

```
// beforeconst container = document.getElementById('root');ReactDOM.render(<App />, container);// afterconst container = document.getElementById('root');const root = ReactDOM.createRoot(container);root.render(<App/>);
```

/$

For a demo of upgrading to React 18, see [Shruti Kapoor](https://twitter.com/shrutikapoor08)’s talk here:

## Streaming Server Rendering with Suspense

React 18 also includes improvements to server-side rendering performance using Suspense.

Streaming server rendering lets you generate HTML from React components on the server, and stream that HTML to your users. In React 18, you can use `Suspense` to break down your app into smaller independent units which can be streamed independently of each other without blocking the rest of the app. This means users will see your content sooner and be able to start interacting with it much faster.

For a deep dive, see [Shaundai Person](https://twitter.com/shaundai)’s talk here:

## The first React working group

For React 18, we created our first Working Group to collaborate with a panel of experts, developers, library maintainers, and educators. Together we worked to create our gradual adoption strategy and refine new APIs such as `useId`, `useSyncExternalStore`, and `useInsertionEffect`.

For an overview of this work, see [Aakansha’ Doshi](https://twitter.com/aakansha1216)’s talk:

## React Developer Tooling

To support the new features in this release, we also announced the newly formed React DevTools team and a new Timeline Profiler to help developers debug their React apps.

For more information and a demo of new DevTools features, see [Brian Vaughn](https://twitter.com/brian_d_vaughn)’s talk:

## React without memo

Looking further into the future, [Xuan Huang (黄玄)](https://twitter.com/Huxpro) shared an update from our React Labs research into an auto-memoizing compiler. Check out this talk for more information and a demo of the compiler prototype:

## React docs keynote

[Rachel Nabors](https://twitter.com/rachelnabors) kicked off a section of talks about learning and designing with React with a keynote about our investment in React’s new docs ([now shipped as react.dev](https://react.dev/blog/2023/03/16/introducing-react-dev)):

## And more…

**We also heard talks on learning and designing with React:**

- Debbie O’Brien: [Things I learnt from the new React docs](https://youtu.be/-7odLW_hG7s).
- Sarah Rainsberger: [Learning in the Browser](https://youtu.be/5X-WEQflCL0).
- Linton Ye: [The ROI of Designing with React](https://youtu.be/7cPWmID5XAk).
- Delba de Oliveira: [Interactive playgrounds with React](https://youtu.be/zL8cz2W0z34).

**Talks from the Relay, React Native, and PyTorch teams:**

- Robert Balicki: [Re-introducing Relay](https://youtu.be/lhVGdErZuN4).
- Eric Rozell and Steven Moyes: [React Native Desktop](https://youtu.be/9L4FFrvwJwY).
- Roman Rädle: [On-device Machine Learning for React Native](https://youtu.be/NLj73vrc2I8)

**And talks from the community on accessibility, tooling, and Server Components:**

- Daishi Kato: [React 18 for External Store Libraries](https://youtu.be/oPfSC5bQPR8).
- Diego Haz: [Building Accessible Components in React 18](https://youtu.be/dcm8fjBfro8).
- Tafu Nakazaki: [Accessible Japanese Form Components with React](https://youtu.be/S4a0QlsH0pU).
- Lyle Troxell: [UI tools for artists](https://youtu.be/b3l4WxipFsE).
- Helen Lin: [Hydrogen + React 18](https://youtu.be/HS6vIYkSNks).

## Thank you

This was our first year planning a conference ourselves, and we have a lot of people to thank.

First, thanks to all of our speakers [Aakansha Doshi](https://twitter.com/aakansha1216), [Andrew Clark](https://twitter.com/acdlite), [Brian Vaughn](https://twitter.com/brian_d_vaughn), [Daishi Kato](https://twitter.com/dai_shi), [Debbie O’Brien](https://twitter.com/debs_obrien), [Delba de Oliveira](https://twitter.com/delba_oliveira), [Diego Haz](https://twitter.com/diegohaz), [Eric Rozell](https://twitter.com/EricRozell), [Helen Lin](https://twitter.com/wizardlyhel), [Juan Tejada](https://twitter.com/_jstejada), [Lauren Tan](https://twitter.com/potetotes), [Linton Ye](https://twitter.com/lintonye), [Lyle Troxell](https://twitter.com/lyle), [Rachel Nabors](https://twitter.com/rachelnabors), [Rick Hanlon](https://twitter.com/rickhanlonii), [Robert Balicki](https://twitter.com/StatisticsFTW), [Roman Rädle](https://twitter.com/raedle), [Sarah Rainsberger](https://twitter.com/sarah11918), [Shaundai Person](https://twitter.com/shaundai), [Shruti Kapoor](https://twitter.com/shrutikapoor08), [Steven Moyes](https://twitter.com/moyessa), [Tafu Nakazaki](https://twitter.com/hawaiiman0), and  [Xuan Huang (黄玄)](https://twitter.com/Huxpro).

Thanks to everyone who helped provide feedback on talks including [Andrew Clark](https://twitter.com/acdlite), [Dan Abramov](https://bsky.app/profile/danabra.mov), [Dave McCabe](https://twitter.com/mcc_abe), [Eli White](https://twitter.com/Eli_White), [Joe Savona](https://twitter.com/en_JS),  [Lauren Tan](https://twitter.com/potetotes), [Rachel Nabors](https://twitter.com/rachelnabors), and [Tim Yung](https://twitter.com/yungsters).

Thanks to [Lauren Tan](https://twitter.com/potetotes) for setting up the conference Discord and serving as our Discord admin.

Thanks to [Seth Webster](https://twitter.com/sethwebster) for feedback on overall direction and making sure we were focused on diversity and inclusion.

Thanks to [Rachel Nabors](https://twitter.com/rachelnabors) for spearheading our moderation effort, and [Aisha Blake](https://twitter.com/AishaBlake) for creating our moderation guide, leading our moderation team, training the translators and moderators, and helping to moderate both events.

Thanks to our moderators [Jesslyn Tannady](https://twitter.com/jtannady), [Suzie Grange](https://twitter.com/missuze), [Becca Bailey](https://twitter.com/beccaliz), [Luna Wei](https://twitter.com/lunaleaps), [Joe Previte](https://twitter.com/jsjoeio), [Nicola Corti](https://twitter.com/Cortinico), [Gijs Weterings](https://twitter.com/gweterings), [Claudio Procida](https://twitter.com/claudiopro), Julia Neumann, Mengdi Chen, Jean Zhang, Ricky Li, and [Xuan Huang (黄玄)](https://twitter.com/Huxpro).

Thanks to [Manjula Dube](https://twitter.com/manjula_dube), [Sahil Mhapsekar](https://twitter.com/apheri0), and Vihang Patel from [React India](https://www.reactindia.io/), and [Jasmine Xie](https://twitter.com/jasmine_xby), [QiChang Li](https://twitter.com/QCL15), and [YanLun Li](https://twitter.com/anneincoding) from [React China](https://twitter.com/ReactChina) for helping moderate our replay event and keep it engaging for the community.

Thanks to Vercel for publishing their [Virtual Event Starter Kit](https://vercel.com/virtual-event-starter-kit), which the conference website was built on, and to [Lee Robinson](https://twitter.com/leeerob) and [Delba de Oliveira](https://twitter.com/delba_oliveira) for sharing their experience running Next.js Conf.

Thanks to [Leah Silber](https://twitter.com/wifelette) for sharing her experience running conferences, learnings from running [RustConf](https://rustconf.com/), and for her book [Event Driven](https://leanpub.com/eventdriven/) and the advice it contains for running conferences.

Thanks to [Kevin Lewis](https://twitter.com/_phzn) and [Rachel Nabors](https://twitter.com/rachelnabors) for sharing their experience running Women of React Conf.

Thanks to [Aakansha Doshi](https://twitter.com/aakansha1216), [Laurie Barth](https://twitter.com/laurieontech), [Michael Chan](https://twitter.com/chantastic), and [Shaundai Person](https://twitter.com/shaundai) for their advice and ideas throughout planning.

Thanks to [Dan Lebowitz](https://twitter.com/lebo) for help designing and building the conference website and tickets.

Thanks to Laura Podolak Waddell, Desmond Osei-Acheampong, Mark Rossi, Josh Toberman and others on the Facebook Video Productions team for recording the videos for the Keynote and Meta employee talks.

Thanks to our partner HitPlay for helping to organize the conference, editing all the videos in the stream, translating all the talks, and moderating the Discord in multiple languages.

Finally, thanks to all of our participants for making this a great React Conf!

[PreviousHow to Upgrade to React 18](https://react.dev/blog/2022/03/08/react-18-upgrade-guide)[NextThe Plan for React 18](https://react.dev/blog/2021/06/08/the-plan-for-react-18)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!

---

# How to Upgrade to React 18

[Blog](https://react.dev/blog)

# How to Upgrade to React 18

March 08, 2022 by [Rick Hanlon](https://twitter.com/rickhanlonii)

---

As we shared in the [release post](https://react.dev/blog/2022/03/29/react-v18), React 18 introduces features powered by our new concurrent renderer, with a gradual adoption strategy for existing applications. In this post, we will guide you through the steps for upgrading to React 18.

Please [report any issues](https://github.com/facebook/react/issues/new/choose) you encounter while upgrading to React 18.

### Note

For React Native users, React 18 will ship in a future version of React Native. This is because React 18 relies on the New React Native Architecture to benefit from the new capabilities presented in this blogpost. For more information, see the [React Conf keynote here](https://www.youtube.com/watch?v=FZ0cG47msEk&t=1530s).

---

## Installing

To install the latest version of React:

 $

```
npm install react react-dom
```

/$

Or if you’re using yarn:

 $

```
yarn add react react-dom
```

/$

## Updates to Client Rendering APIs

When you first install React 18, you will see a warning in the console:

 ConsoleReactDOM.render is no longer supported in React 18. Use createRoot instead. Until you switch to the new API, your app will behave as if it’s running React 17. Learn more: [https://reactjs.org/link/switch-to-createroot](https://reactjs.org/link/switch-to-createroot)

React 18 introduces a new root API which provides better ergonomics for managing roots. The new root API also enables the new concurrent renderer, which allows you to opt-into concurrent features.

 $

```
// Beforeimport { render } from 'react-dom';const container = document.getElementById('app');render(<App tab="home" />, container);// Afterimport { createRoot } from 'react-dom/client';const container = document.getElementById('app');const root = createRoot(container); // createRoot(container!) if you use TypeScriptroot.render(<App tab="home" />);
```

/$

We’ve also changed `unmountComponentAtNode` to `root.unmount`:

 $

```
// BeforeunmountComponentAtNode(container);// Afterroot.unmount();
```

/$

We’ve also removed the callback from render, since it usually does not have the expected result when using Suspense:

 $

```
// Beforeconst container = document.getElementById('app');render(<App tab="home" />, container, () => {  console.log('rendered');});// Afterfunction AppWithCallbackAfterRender() {  useEffect(() => {    console.log('rendered');  });  return <App tab="home" />}const container = document.getElementById('app');const root = createRoot(container);root.render(<AppWithCallbackAfterRender />);
```

/$

### Note

There is no one-to-one replacement for the old render callback API — it depends on your use case. See the working group post for [Replacing render with createRoot](https://github.com/reactwg/react-18/discussions/5) for more information.

Finally, if your app uses server-side rendering with hydration, upgrade `hydrate` to `hydrateRoot`:

 $

```
// Beforeimport { hydrate } from 'react-dom';const container = document.getElementById('app');hydrate(<App tab="home" />, container);// Afterimport { hydrateRoot } from 'react-dom/client';const container = document.getElementById('app');const root = hydrateRoot(container, <App tab="home" />);// Unlike with createRoot, you don't need a separate root.render() call here.
```

/$

For more information, see the [working group discussion here](https://github.com/reactwg/react-18/discussions/5).

### Note

**If your app doesn’t work after upgrading, check whether it’s wrapped in<StrictMode>.** [Strict Mode has gotten stricter in React 18](#updates-to-strict-mode), and not all your components may be resilient to the new checks it adds in development mode. If removing Strict Mode fixes your app, you can remove it during the upgrade, and then add it back (either at the top or for a part of the tree) after you fix the issues that it’s pointing out.

## Updates to Server Rendering APIs

In this release, we’re revamping our `react-dom/server` APIs to fully support Suspense on the server and Streaming SSR. As part of these changes, we’re deprecating the old Node streaming API, which does not support incremental Suspense streaming on the server.

Using this API will now warn:

- `renderToNodeStream`: **Deprecated ⛔️️**

Instead, for streaming in Node environments, use:

- `renderToPipeableStream`: **New ✨**

We’re also introducing a new API to support streaming SSR with Suspense for modern edge runtime environments, such as Deno and Cloudflare workers:

- `renderToReadableStream`: **New ✨**

The following APIs will continue working, but with limited support for Suspense:

- `renderToString`: **Limited** ⚠️
- `renderToStaticMarkup`: **Limited** ⚠️

Finally, this API will continue to work for rendering e-mails:

- `renderToStaticNodeStream`

For more information on the changes to server rendering APIs, see the working group post on [Upgrading to React 18 on the server](https://github.com/reactwg/react-18/discussions/22), a [deep dive on the new Suspense SSR Architecture](https://github.com/reactwg/react-18/discussions/37), and [Shaundai Person’s](https://twitter.com/shaundai) talk on [Streaming Server Rendering with Suspense](https://www.youtube.com/watch?v=pj5N-Khihgc) at React Conf 2021.

## Updates to TypeScript definitions

If your project uses TypeScript, you will need to update your `@types/react` and `@types/react-dom` dependencies to the latest versions. The new types are safer and catch issues that used to be ignored by the type checker. The most notable change is that the `children` prop now needs to be listed explicitly when defining props, for example:

 $

```
interface MyButtonProps {  color: string;  children?: React.ReactNode;}
```

/$

See the [React 18 typings pull request](https://github.com/DefinitelyTyped/DefinitelyTyped/pull/56210) for a full list of type-only changes. It links to example fixes in library types so you can see how to adjust your code. You can use the [automated migration script](https://github.com/eps1lon/types-react-codemod) to help port your application code to the new and safer typings faster.

If you find a bug in the typings, please [file an issue](https://github.com/DefinitelyTyped/DefinitelyTyped/discussions/new?category=issues-with-a-types-package) in the DefinitelyTyped repo.

## Automatic Batching

React 18 adds out-of-the-box performance improvements by doing more batching by default. Batching is when React groups multiple state updates into a single re-render for better performance. Before React 18, we only batched updates inside React event handlers. Updates inside of promises, setTimeout, native event handlers, or any other event were not batched in React by default:

 $

```
// Before React 18 only React events were batchedfunction handleClick() {  setCount(c => c + 1);  setFlag(f => !f);  // React will only re-render once at the end (that's batching!)}setTimeout(() => {  setCount(c => c + 1);  setFlag(f => !f);  // React will render twice, once for each state update (no batching)}, 1000);
```

/$

Starting in React 18 with `createRoot`, all updates will be automatically batched, no matter where they originate from. This means that updates inside of timeouts, promises, native event handlers or any other event will batch the same way as updates inside of React events:

 $

```
// After React 18 updates inside of timeouts, promises,// native event handlers or any other event are batched.function handleClick() {  setCount(c => c + 1);  setFlag(f => !f);  // React will only re-render once at the end (that's batching!)}setTimeout(() => {  setCount(c => c + 1);  setFlag(f => !f);  // React will only re-render once at the end (that's batching!)}, 1000);
```

/$

This is a breaking change, but we expect this to result in less work rendering, and therefore better performance in your applications. To opt-out of automatic batching, you can use `flushSync`:

 $

```
import { flushSync } from 'react-dom';function handleClick() {  flushSync(() => {    setCounter(c => c + 1);  });  // React has updated the DOM by now  flushSync(() => {    setFlag(f => !f);  });  // React has updated the DOM by now}
```

/$

For more information, see the [Automatic batching deep dive](https://github.com/reactwg/react-18/discussions/21).

## New APIs for Libraries

In the React 18 Working Group we worked with library maintainers to create new APIs needed to support concurrent rendering for use cases specific to their use case in areas like styles, and external stores. To support React 18, some libraries may need to switch to one of the following APIs:

- `useSyncExternalStore` is a new Hook that allows external stores to support concurrent reads by forcing updates to the store to be synchronous. This new API is recommended for any library that integrates with state external to React. For more information, see the [useSyncExternalStore overview post](https://github.com/reactwg/react-18/discussions/70) and [useSyncExternalStore API details](https://github.com/reactwg/react-18/discussions/86).
- `useInsertionEffect` is a new Hook that allows CSS-in-JS libraries to address performance issues of injecting styles in render. Unless you’ve already built a CSS-in-JS library we don’t expect you to ever use this. This Hook will run after the DOM is mutated, but before layout effects read the new layout. This solves an issue that already exists in React 17 and below, but is even more important in React 18 because React yields to the browser during concurrent rendering, giving it a chance to recalculate layout. For more information, see the [Library Upgrade Guide for<style>](https://github.com/reactwg/react-18/discussions/110).

React 18 also introduces new APIs for concurrent rendering such as `startTransition`, `useDeferredValue` and `useId`, which we share more about in the [release post](https://react.dev/blog/2022/03/29/react-v18).

## Updates to Strict Mode

In the future, we’d like to add a feature that allows React to add and remove sections of the UI while preserving state. For example, when a user tabs away from a screen and back, React should be able to immediately show the previous screen. To do this, React would unmount and remount trees using the same component state as before.

This feature will give React better performance out-of-the-box, but requires components to be resilient to effects being mounted and destroyed multiple times. Most effects will work without any changes, but some effects assume they are only mounted or destroyed once.

To help surface these issues, React 18 introduces a new development-only check to Strict Mode. This new check will automatically unmount and remount every component, whenever a component mounts for the first time, restoring the previous state on the second mount.

Before this change, React would mount the component and create the effects:

 $

```
* React mounts the component.    * Layout effects are created.    * Effect effects are created.
```

/$

With Strict Mode in React 18, React will simulate unmounting and remounting the component in development mode:

 $

```
* React mounts the component.    * Layout effects are created.    * Effect effects are created.* React simulates unmounting the component.    * Layout effects are destroyed.    * Effects are destroyed.* React simulates mounting the component with the previous state.    * Layout effect setup code runs    * Effect setup code runs
```

/$

For more information, see the Working Group posts for [Adding Reusable State to StrictMode](https://github.com/reactwg/react-18/discussions/19) and [How to support Reusable State in Effects](https://github.com/reactwg/react-18/discussions/18).

## Configuring Your Testing Environment

When you first update your tests to use `createRoot`, you may see this warning in your test console:

 ConsoleThe current testing environment is not configured to support act(…)

To fix this, set `globalThis.IS_REACT_ACT_ENVIRONMENT` to `true` before running your test:

 $

```
// In your test setup fileglobalThis.IS_REACT_ACT_ENVIRONMENT = true;
```

/$

The purpose of the flag is to tell React that it’s running in a unit test-like environment. React will log helpful warnings if you forget to wrap an update with `act`.

You can also set the flag to `false` to tell React that `act` isn’t needed. This can be useful for end-to-end tests that simulate a full browser environment.

Eventually, we expect testing libraries will configure this for you automatically. For example, the [next version of React Testing Library has built-in support for React 18](https://github.com/testing-library/react-testing-library/issues/509#issuecomment-917989936) without any additional configuration.

[More background on theacttesting API and related changes](https://github.com/reactwg/react-18/discussions/102) is available in the working group.

## Dropping Support for Internet Explorer

In this release, React is dropping support for Internet Explorer, which is [going out of support on June 15, 2022](https://blogs.windows.com/windowsexperience/2021/05/19/the-future-of-internet-explorer-on-windows-10-is-in-microsoft-edge). We’re making this change now because new features introduced in React 18 are built using modern browser features such as microtasks which cannot be adequately polyfilled in IE.

If you need to support Internet Explorer we recommend you stay with React 17.

## Deprecations

- `react-dom`: `ReactDOM.render` has been deprecated. Using it will warn and run your app in React 17 mode.
- `react-dom`: `ReactDOM.hydrate` has been deprecated. Using it will warn and run your app in React 17 mode.
- `react-dom`: `ReactDOM.unmountComponentAtNode` has been deprecated.
- `react-dom`: `ReactDOM.renderSubtreeIntoContainer` has been deprecated.
- `react-dom/server`: `ReactDOMServer.renderToNodeStream` has been deprecated.

## Other Breaking Changes

- **Consistent useEffect timing**: React now always synchronously flushes effect functions if the update was triggered during a discrete user input event such as a click or a keydown event. Previously, the behavior wasn’t always predictable or consistent.
- **Stricter hydration errors**: Hydration mismatches due to missing or extra text content are now treated like errors instead of warnings. React will no longer attempt to “patch up” individual nodes by inserting or deleting a node on the client in an attempt to match the server markup, and will revert to client rendering up to the closest `<Suspense>` boundary in the tree. This ensures the hydrated tree is consistent and avoids potential privacy and security holes that can be caused by hydration mismatches.
- **Suspense trees are always consistent:** If a component suspends before it’s fully added to the tree, React will not add it to the tree in an incomplete state or fire its effects. Instead, React will throw away the new tree completely, wait for the asynchronous operation to finish, and then retry rendering again from scratch. React will render the retry attempt concurrently, and without blocking the browser.
- **Layout Effects with Suspense**: When a tree re-suspends and reverts to a fallback, React will now clean up layout effects, and then re-create them when the content inside the boundary is shown again. This fixes an issue which prevented component libraries from correctly measuring layout when used with Suspense.
- **New JS Environment Requirements**: React now depends on modern browsers features including `Promise`, `Symbol`, and `Object.assign`. If you support older browsers and devices such as Internet Explorer which do not provide modern browser features natively or have non-compliant implementations, consider including a global polyfill in your bundled application.

## Other Notable Changes

### React

- **Components can now renderundefined:** React no longer warns if you return `undefined` from a component. This makes the allowed component return values consistent with values that are allowed in the middle of a component tree. We suggest to use a linter to prevent mistakes like forgetting a `return` statement before JSX.
- **In tests,actwarnings are now opt-in:** If you’re running end-to-end tests, the `act` warnings are unnecessary. We’ve introduced an [opt-in](https://github.com/reactwg/react-18/discussions/102) mechanism so you can enable them only for unit tests where they are useful and beneficial.
- **No warning aboutsetStateon unmounted components:** Previously, React warned about memory leaks when you call `setState` on an unmounted component. This warning was added for subscriptions, but people primarily run into it in scenarios where setting state is fine, and workarounds make the code worse. We’ve [removed](https://github.com/facebook/react/pull/22114) this warning.
- **No suppression of console logs:** When you use Strict Mode, React renders each component twice to help you find unexpected side effects. In React 17, we’ve suppressed console logs for one of the two renders to make the logs easier to read. In response to [community feedback](https://github.com/facebook/react/issues/21783) about this being confusing, we’ve removed the suppression. Instead, if you have React DevTools installed, the second log’s renders will be displayed in grey, and there will be an option (off by default) to suppress them completely.
- **Improved memory usage:** React now cleans up more internal fields on unmount, making the impact from unfixed memory leaks that may exist in your application code less severe.

### React DOM Server

- **renderToString:** Will no longer error when suspending on the server. Instead, it will emit the fallback HTML for the closest `<Suspense>` boundary and then retry rendering the same content on the client. It is still recommended that you switch to a streaming API like `renderToPipeableStream` or `renderToReadableStream` instead.
- **renderToStaticMarkup:** Will no longer error when suspending on the server. Instead, it will emit the fallback HTML for the closest `<Suspense>` boundary.

## Changelog

You can view the [full changelog here](https://github.com/facebook/react/blob/main/CHANGELOG.md).

[PreviousReact v18.0](https://react.dev/blog/2022/03/29/react-v18)[NextReact Conf 2021 Recap](https://react.dev/blog/2021/12/17/react-conf-2021-recap)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!
