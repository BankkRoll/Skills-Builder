# React Canaries: Enabling Incremental Feature Rollout Outside Meta and more

# React Canaries: Enabling Incremental Feature Rollout Outside Meta

[Blog](https://react.dev/blog)

# React Canaries: Enabling Incremental Feature Rollout Outside Meta

May 3, 2023 by [Dan Abramov](https://bsky.app/profile/danabra.mov), [Sophie Alpert](https://twitter.com/sophiebits), [Rick Hanlon](https://twitter.com/rickhanlonii), [Sebastian Markbåge](https://twitter.com/sebmarkbage), and [Andrew Clark](https://twitter.com/acdlite)

---

We’d like to offer the React community an option to adopt individual new features as soon as their design is close to final, before they’re released in a stable version—similar to how Meta has long used bleeding-edge versions of React internally. We are introducing a new officially supported [Canary release channel](https://react.dev/community/versioning-policy#canary-channel). It lets curated setups like frameworks decouple adoption of individual React features from the React release schedule.

---

## tl;dr

- We’re introducing an officially supported [Canary release channel](https://react.dev/community/versioning-policy#canary-channel) for React. Since it’s officially supported, if any regressions land, we’ll treat them with a similar urgency to bugs in stable releases.
- Canaries let you start using individual new React features before they land in the semver-stable releases.
- Unlike the [Experimental](https://react.dev/community/versioning-policy#experimental-channel) channel, React Canaries only include features that we reasonably believe to be ready for adoption. We encourage frameworks to consider bundling pinned Canary React releases.
- We will announce breaking changes and new features on our blog as they land in Canary releases.
- **As always, React continues to follow semver for every Stable release.**

## How React features are usually developed

Typically, every React feature has gone through the same stages:

1. We develop an initial version and prefix it with `experimental_` or `unstable_`. The feature is only available in the `experimental` release channel. At this point, the feature is expected to change significantly.
2. We find a team at Meta willing to help us test this feature and provide feedback on it. This leads to a round of changes. As the feature becomes more stable, we work with more teams at Meta to try it out.
3. Eventually, we feel confident in the design. We remove the prefix from the API name, and make the feature available on the `main` branch by default, which most Meta products use. At this point, any team at Meta can use this feature.
4. As we build confidence in the direction, we also post an RFC for the new feature. At this point we know the design works for a broad set of cases, but we might make some last minute adjustments.
5. When we are close to cutting an open source release, we write documentation for the feature and finally release the feature in a stable React release.

This playbook works well for most features we’ve released so far. However, there can be a significant gap between when the feature is generally ready to use (step 3) and when it is released in open source (step 5).

**We’d like to offer the React community an option to follow the same approach as Meta, and adopt individual new features earlier (as they become available) without having to wait for the next release cycle of React.**

As always, all React features will eventually make it into a Stable release.

## Can we just do more minor releases?

Generally, we *do* use minor releases for introducing new features.

However, this isn’t always possible. Sometimes, new features are interconnected with *other* new features which have not yet been fully completed and that we’re still actively iterating on. We can’t release them separately because their implementations are related. We can’t version them separately because they affect the same packages (for example, `react` and `react-dom`). And we need to keep the ability to iterate on the pieces that aren’t ready without a flurry of major version releases, which semver would require us to do.

At Meta, we’ve solved this problem by building React from the `main` branch, and manually updating it to a specific pinned commit every week. This is also the approach that React Native releases have been following for the last several years. Every *stable* release of React Native is pinned to a specific commit from the `main` branch of the React repository. This lets React Native include important bugfixes and incrementally adopt new React features at the framework level without getting coupled to the global React release schedule.

We would like to make this workflow available to other frameworks and curated setups. For example, it lets a framework *on top of* React include a React-related breaking change *before* this breaking change gets included into a stable React release. This is particularly useful because some breaking changes only affect framework integrations. This lets a framework release such a change in its own minor version without breaking semver.

Rolling releases with the Canaries channel will allow us to have a tighter feedback loop and ensure that new features get comprehensive testing in the community. This workflow is closer to how TC39, the JavaScript standards committee, [handles changes in numbered stages](https://tc39.es/process-document/). New React features may be available in frameworks built on React before they are in a React stable release, just as new JavaScript features ship in browsers before they are officially ratified as part of the specification.

## Why not use experimental releases instead?

Although you *can* technically use [Experimental releases](https://react.dev/community/versioning-policy#canary-channel), we recommend against using them in production because experimental APIs can undergo significant breaking changes on their way to stabilization (or can even be removed entirely). While Canaries can also contain mistakes (as with any release), going forward we plan to announce any significant breaking changes in Canaries on our blog. Canaries are the closest to the code Meta runs internally, so you can generally expect them to be relatively stable. However, you *do* need to keep the version pinned and manually scan the GitHub commit log when updating between the pinned commits.

**We expect that most people using React outside a curated setup (like a framework) will want to continue using the Stable releases.** However, if you’re building a framework, you might want to consider bundling a Canary version of React pinned to a particular commit, and update it at your own pace. The benefit of that is that it lets you ship individual completed React features and bugfixes earlier for your users and at your own release schedule, similar to how React Native has been doing it for the last few years. The downside is that you would take on additional responsibility to review which React commits are being pulled in and communicate to your users which React changes are included with your releases.

If you’re a framework author and want to try this approach, please get in touch with us.

## Announcing breaking changes and new features early

Canary releases represent our best guess of what will go into the next stable React release at any given time.

Traditionally, we’ve only announced breaking changes at the *end* of the release cycle (when doing a major release). Now that Canary releases are an officially supported way to consume React, we plan to shift towards announcing breaking changes and significant new features *as they land* in Canaries. For example, if we merge a breaking change that will go out in a Canary, we will write a post about it on the React blog, including codemods and migration instructions if necessary. Then, if you’re a framework author cutting a major release that updates the pinned React canary to include that change, you can link to our blog post from your release notes. Finally, when a stable major version of React is ready, we will link to those already published blog posts, which we hope will help our team make progress faster.

We plan to document APIs as they land in Canaries—even if these APIs are not yet available outside of them. APIs that are only available in Canaries will be marked with a special note on the corresponding pages. This will include APIs like [use](https://github.com/reactjs/rfcs/pull/229), and some others (like `cache` and `createServerContext`) which we’ll send RFCs for.

## Canaries must be pinned

If you decide to adopt the Canary workflow for your app or framework, make sure you always pin the *exact* version of the Canary you’re using. Since Canaries are pre-releases, they may still include breaking changes.

## Example: React Server Components

As we [announced in March](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components), the React Server Components conventions have been finalized, and we do not expect significant breaking changes related to their user-facing API contract. However, we can’t release support for React Server Components in a stable version of React yet because we are still working on several intertwined framework-only features (such as [asset loading](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#asset-loading)) and expect more breaking changes there.

This means that React Server Components are ready to be adopted by frameworks. However, until the next major React release, the only way for a framework to adopt them is to ship a pinned Canary version of React. (To avoid bundling two copies of React, frameworks that wish to do this would need to enforce resolution of `react` and `react-dom` to the pinned Canary they ship with their framework, and explain that to their users. As an example, this is what Next.js App Router does.)

## Testing libraries against both Stable and Canary versions

We do not expect library authors to test every single Canary release since it would be prohibitively difficult. However, just as when we [originally introduced the different React pre-release channels three years ago](https://legacy.reactjs.org/blog/2019/10/22/react-release-channels.html), we encourage libraries to run tests against *both* the latest Stable and latest Canary versions. If you see a change in behavior that wasn’t announced, please file a bug in the React repository so that we can help diagnose it. We expect that as this practice becomes widely adopted, it will reduce the amount of effort necessary to upgrade libraries to new major versions of React, since accidental regressions would be found as they land.

### Note

Strictly speaking, Canary is not a *new* release channel—it used to be called Next. However, we’ve decided to rename it to avoid confusion with Next.js. We’re announcing it as a *new* release channel to communicate the new expectations, such as Canaries being an officially supported way to use React.

## Stable releases work like before

We are not introducing any changes to stable React releases.

[PreviousReact Labs: What We've Been Working On – February 2024](https://react.dev/blog/2024/02/15/react-labs-what-we-have-been-working-on-february-2024)[NextReact Labs: What We've Been Working On – March 2023](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023)

---

# React Labs: What We've Been Working On

[Blog](https://react.dev/blog)

# React Labs: What We've Been Working On – February 2024

February 15, 2024 by [Joseph Savona](https://twitter.com/en_JS), [Ricky Hanlon](https://twitter.com/rickhanlonii), [Andrew Clark](https://twitter.com/acdlite), [Matt Carroll](https://twitter.com/mattcarrollcode), and [Dan Abramov](https://bsky.app/profile/danabra.mov).

---

In React Labs posts, we write about projects in active research and development. We’ve made significant progress since our [last update](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023), and we’d like to share our progress.

---

## React Compiler

React Compiler is no longer a research project: the compiler now powers instagram.com in production, and we are working to ship the compiler across additional surfaces at Meta and to prepare the first open source release.

As discussed in our [previous post](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-optimizing-compiler), React can *sometimes* re-render too much when state changes. Since the early days of React our solution for such cases has been manual memoization. In our current APIs, this means applying the [useMemo](https://react.dev/reference/react/useMemo), [useCallback](https://react.dev/reference/react/useCallback), and [memo](https://react.dev/reference/react/memo) APIs to manually tune how much React re-renders on state changes. But manual memoization is a compromise. It clutters up our code, is easy to get wrong, and requires extra work to keep up to date.

Manual memoization is a reasonable compromise, but we weren’t satisfied. Our vision is for React to *automatically* re-render just the right parts of the UI when state changes, *without compromising on React’s core mental model*. We believe that React’s approach — UI as a simple function of state, with standard JavaScript values and idioms — is a key part of why React has been approachable for so many developers. That’s why we’ve invested in building an optimizing compiler for React.

JavaScript is a notoriously challenging language to optimize, thanks to its loose rules and dynamic nature. React Compiler is able to compile code safely by modeling both the rules of JavaScript *and* the “rules of React”. For example, React components must be idempotent — returning the same value given the same inputs — and can’t mutate props or state values. These rules limit what developers can do and help to carve out a safe space for the compiler to optimize.

Of course, we understand that developers sometimes bend the rules a bit, and our goal is to make React Compiler work out of the box on as much code as possible. The compiler attempts to detect when code doesn’t strictly follow React’s rules and will either compile the code where safe or skip compilation if it isn’t safe. We’re testing against Meta’s large and varied codebase in order to help validate this approach.

For developers who are curious about making sure their code follows React’s rules, we recommend [enabling Strict Mode](https://react.dev/reference/react/StrictMode) and [configuring React’s ESLint plugin](https://react.dev/learn/editor-setup#linting). These tools can help to catch subtle bugs in your React code, improving the quality of your applications today, and future-proofs your applications for upcoming features such as React Compiler. We are also working on consolidated documentation of the rules of React and updates to our ESLint plugin to help teams understand and apply these rules to create more robust apps.

To see the compiler in action, you can check out our [talk from last fall](https://www.youtube.com/watch?v=qOQClO3g8-Y). At the time of the talk, we had early experimental data from trying React Compiler on one page of instagram.com. Since then, we shipped the compiler to production across instagram.com. We’ve also expanded our team to accelerate the rollout to additional surfaces at Meta and to open source. We’re excited about the path ahead and will have more to share in the coming months.

## Actions

We [previously shared](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components) that we were exploring solutions for sending data from the client to the server with Server Actions, so that you can execute database mutations and implement forms. During development of Server Actions, we extended these APIs to support data handling in client-only applications as well.

We refer to this broader collection of features as simply “Actions”. Actions allow you to pass a function to DOM elements such as [<form/>](https://react.dev/reference/react-dom/components/form):

 $

```
<form action={search}>  <input name="query" />  <button type="submit">Search</button></form>
```

/$

The `action` function can operate synchronously or asynchronously. You can define them on the client side using standard JavaScript or on the server with the  ['use server'](https://react.dev/reference/rsc/use-server) directive. When using an action, React will manage the life cycle of the data submission for you, providing hooks like [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus), and [useActionState](https://react.dev/reference/react/useActionState) to access the current state and response of the form action.

By default, Actions are submitted within a [transition](https://react.dev/reference/react/useTransition), keeping the current page interactive while the action is processing. Since Actions support async functions, we’ve also added the ability to use `async/await` in transitions. This allows you to show pending UI with the `isPending` state of a transition when an async request like `fetch` starts, and show the pending UI all the way through the update being applied.

Alongside Actions, we’re introducing a feature named [useOptimistic](https://react.dev/reference/react/useOptimistic) for managing optimistic state updates. With this hook, you can apply temporary updates that are automatically reverted once the final state commits. For Actions, this allows you to optimistically set the final state of the data on the client, assuming the submission is successful, and revert to the value for data received from the server. It works using regular `async`/`await`, so it works the same whether you’re using `fetch` on the client, or a Server Action from the server.

Library authors can implement custom `action={fn}` props in their own components with `useTransition`. Our intent is for libraries to adopt the Actions pattern when designing their component APIs, to provide a consistent experience for React developers. For example, if your library provides a `<Calendar onSelect={eventHandler}>` component, consider also exposing a `<Calendar selectAction={action}>` API, too.

While we initially focused on Server Actions for client-server data transfer, our philosophy for React is to provide the same programming model across all platforms and environments. When possible, if we introduce a feature on the client, we aim to make it also work on the server, and vice versa. This philosophy allows us to create a single set of APIs that work no matter where your app runs, making it easier to upgrade to different environments later.

Actions are now available in the Canary channel and will ship in the next release of React.

## New Features in React Canary

We introduced [React Canaries](https://react.dev/blog/2023/05/03/react-canaries) as an option to adopt individual new stable features as soon as their design is close to final, before they’re released in a stable semver version.

Canaries are a change to the way we develop React. Previously, features would be researched and built privately inside of Meta, so users would only see the final polished product when released to Stable. With Canaries, we’re building in public with the help of the community to finalize features we share in the React Labs blog series. This means you hear about new features sooner, as they’re being finalized instead of after they’re complete.

React Server Components, Asset Loading, Document Metadata, and Actions have all landed in the React Canary, and we’ve added docs for these features on react.dev:

- **Directives**: ["use client"](https://react.dev/reference/rsc/use-client) and ["use server"](https://react.dev/reference/rsc/use-server) are bundler features designed for full-stack React frameworks. They mark the “split points” between the two environments: `"use client"` instructs the bundler to generate a `<script>` tag (like [Astro Islands](https://docs.astro.build/en/concepts/islands/#creating-an-island)), while `"use server"` tells the bundler to generate a POST endpoint (like [tRPC Mutations](https://trpc.io/docs/concepts)). Together, they let you write reusable components that compose client-side interactivity with the related server-side logic.
- **Document Metadata**: we added built-in support for rendering [<title>](https://react.dev/reference/react-dom/components/title), [<meta>](https://react.dev/reference/react-dom/components/meta), and metadata [<link>](https://react.dev/reference/react-dom/components/link) tags anywhere in your component tree. These work the same way in all environments, including fully client-side code, SSR, and RSC. This provides built-in support for features pioneered by libraries like [React Helmet](https://github.com/nfl/react-helmet).
- **Asset Loading**: we integrated Suspense with the loading lifecycle of resources such as stylesheets, fonts, and scripts so that React takes them into account to determine whether the content in elements like [<style>](https://react.dev/reference/react-dom/components/style), [<link>](https://react.dev/reference/react-dom/components/link), and [<script>](https://react.dev/reference/react-dom/components/script) are ready to be displayed. We’ve also added new [Resource Loading APIs](https://react.dev/reference/react-dom#resource-preloading-apis) like `preload` and `preinit` to provide greater control for when a resource should load and initialize.
- **Actions**: As shared above, we’ve added Actions to manage sending data from the client to the server. You can add `action` to elements like [<form/>](https://react.dev/reference/react-dom/components/form), access the status with [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus), handle the result with [useActionState](https://react.dev/reference/react/useActionState), and optimistically update the UI with [useOptimistic](https://react.dev/reference/react/useOptimistic).

Since all of these features work together, it’s difficult to release them in the Stable channel individually. Releasing Actions without the complementary hooks for accessing form states would limit the practical usability of Actions. Introducing React Server Components without integrating Server Actions would complicate modifying data on the server.

Before we can release a set of features to the Stable channel, we need to ensure they work cohesively and developers have everything they need to use them in production. React Canaries allow us to develop these features individually, and release the stable APIs incrementally until the entire feature set is complete.

The current set of features in React Canary are complete and ready to release.

## The Next Major Version of React

After a couple of years of iteration, `react@canary` is now ready to ship to `react@latest`. The new features mentioned above are compatible with any environment your app runs in, providing everything needed for production use. Since Asset Loading and Document Metadata may be a breaking change for some apps, the next version of React will be a major version: **React 19**.

There’s still more to be done to prepare for release. In React 19, we’re also adding long-requested improvements which require breaking changes like support for Web Components. Our focus now is to land these changes, prepare for release, finalize docs for new features, and publish announcements for what’s included.

We’ll share more information about everything React 19 includes, how to adopt the new client features, and how to build support for React Server Components in the coming months.

## Offscreen (renamed to Activity).

Since our last update, we’ve renamed a capability we’re researching from “Offscreen” to “Activity”. The name “Offscreen” implied that it only applied to parts of the app that were not visible, but while researching the feature we realized that it’s possible for parts of the app to be visible and inactive, such as content behind a modal. The new name more closely reflects the behavior of marking certain parts of the app “active” or “inactive”.

Activity is still under research and our remaining work is to finalize the primitives that are exposed to library developers. We’ve deprioritized this area while we focus on shipping features that are more complete.

---

In addition to this update, our team has presented at conferences and made appearances on podcasts to speak more on our work and answer questions.

- [Sathya Gunasekaran](https://github.com/gsathya) spoke about the React Compiler at the [React India](https://www.youtube.com/watch?v=kjOacmVsLSE) conference
- [Dan Abramov](https://react.dev/community/team#dan-abramov) gave a talk at [RemixConf](https://www.youtube.com/watch?v=zMf_xeGPn6s) titled “React from Another Dimension” which explores an alternative history of how React Server Components and Actions could have been created
- [Dan Abramov](https://react.dev/community/team#dan-abramov) was interviewed on [the Changelog’s JS Party podcast](https://changelog.com/jsparty/311) about React Server Components
- [Matt Carroll](https://react.dev/community/team#matt-carroll) was interviewed on the [Front-End Fire podcast](https://www.buzzsprout.com/2226499/14462424-interview-the-two-reacts-with-rachel-nabors-evan-bacon-and-matt-carroll) where he discussed [The Two Reacts](https://overreacted.io/the-two-reacts/)

Thanks [Lauren Tan](https://twitter.com/potetotes), [Sophie Alpert](https://twitter.com/sophiebits), [Jason Bonta](https://threads.net/someextent), [Eli White](https://twitter.com/Eli_White), and [Sathya Gunasekaran](https://twitter.com/_gsathya) for reviewing this post.

Thanks for reading, and [see you at React Conf](https://conf.react.dev/)!

[PreviousReact 19 RC Upgrade Guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)[NextReact Canaries: Enabling Incremental Feature Rollout Outside Meta](https://react.dev/blog/2023/05/03/react-canaries)
