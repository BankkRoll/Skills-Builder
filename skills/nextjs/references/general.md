# App Router and more

# App Router

> The App Router is a file-system based router that uses React's latest features such as Server Components, Suspense, Server Functions, and more.

[Next.js Docs](https://nextjs.org/docs)App Router

# App Router

Last updated  July 30, 2025

The **App Router** is a file-system based router that uses React's latest features such as [Server Components](https://react.dev/reference/rsc/server-components), [Suspense](https://react.dev/reference/react/Suspense), and [Server Functions](https://react.dev/reference/rsc/server-functions).

## Next Steps

Learn the fundamentals of building an App Router project, from installation to layouts, navigation, server and client components.[InstallationLearn how to create a new Next.js application with the `create-next-app` CLI, and set up TypeScript, ESLint, and Module Path Aliases.](https://nextjs.org/docs/app/getting-started/installation)[Project StructureLearn the folder and file conventions in Next.js, and how to organize your project.](https://nextjs.org/docs/app/getting-started/project-structure)[Layouts and PagesLearn how to create your first pages and layouts, and link between them with the Link component.](https://nextjs.org/docs/app/getting-started/layouts-and-pages)[Linking and NavigatingLearn how the built-in navigation optimizations work, including prefetching, prerendering, and client-side navigation, and how to optimize navigation for dynamic routes and slow networks.](https://nextjs.org/docs/app/getting-started/linking-and-navigating)[Server and Client ComponentsLearn how you can use React Server and Client Components to render parts of your application on the server or the client.](https://nextjs.org/docs/app/getting-started/server-and-client-components)

Was this helpful?

supported.

---

# Architecture

> How Next.js Works

[Next.js Docs](https://nextjs.org/docs)Architecture

# Architecture

Last updated  November 6, 2024

Learn about the Next.js architecture and how it works under the hood.

[AccessibilityThe built-in accessibility features of Next.js.](https://nextjs.org/docs/architecture/accessibility)[Fast RefreshFast Refresh is a hot module reloading experience that gives you instantaneous feedback on edits made to your React components.](https://nextjs.org/docs/architecture/fast-refresh)[Next.js CompilerNext.js Compiler, written in Rust, which transforms and minifies your Next.js application.](https://nextjs.org/docs/architecture/nextjs-compiler)[Supported BrowsersBrowser support and which JavaScript features are supported by Next.js.](https://nextjs.org/docs/architecture/supported-browsers)

Was this helpful?

supported.

---

# Next.js Community

> Get involved in the Next.js community.

[Next.js Docs](https://nextjs.org/docs)Community

# Next.js Community

Last updated  December 9, 2025

With over 5 million weekly downloads, Next.js has a large and active community of developers across the world. Here's how you can get involved in our community:

## Contributing

There are a couple of ways you can contribute to the development of Next.js:

- [Documentation](https://nextjs.org/docs/community/contribution-guide): Suggest improvements or even write new sections to help our users understand how to use Next.js.
- [Examples](https://github.com/vercel/next.js/tree/canary/examples): Help developers integrate Next.js with other tools and services by creating a new example or improving an existing one.
- [Codebase](https://github.com/vercel/next.js/tree/canary/contributing/core): Learn more about the underlying architecture, contribute to bug fixes, errors, and suggest new features.

## Discussions

If you have a question about Next.js, or want to help others, you're always welcome to join the conversation:

- [GitHub Discussions](https://github.com/vercel/next.js/discussions)
- [Discord](https://discord.com/invite/bUG2bvbtHy)
- [Reddit](https://www.reddit.com/r/nextjs)

## Social Media

Follow Next.js on [Twitter](https://x.com/nextjs) for the latest updates, and subscribe to the [Vercel YouTube channel](https://www.youtube.com/@VercelHQ) for Next.js videos.

## Code of Conduct

We believe in creating an inclusive, welcoming community. As such, we ask all members to adhere to our [Code of Conduct](https://github.com/vercel/next.js/blob/canary/CODE_OF_CONDUCT.md). This document outlines our expectations for participant behavior. We invite you to read it and help us maintain a safe and respectful environment.

[Contribution GuideLearn how to contribute to Next.js Documentation](https://nextjs.org/docs/community/contribution-guide)[RspackUse the `next-rspack` plugin to bundle your Next.js with Rspack.](https://nextjs.org/docs/community/rspack)

Was this helpful?

supported.

---

# Next.js Docs

> Welcome to the Next.js Documentation.

# Next.js Docs

Welcome to the Next.js documentation!

## What is Next.js?

Next.js is a React framework for building full-stack web applications. You use React Components to build user interfaces, and Next.js for additional features and optimizations.

It also automatically configures lower-level tools like bundlers and compilers. You can instead focus on building your product and shipping quickly.

Whether you're an individual developer or part of a larger team, Next.js can help you build interactive, dynamic, and fast React applications.

## How to use the docs

The docs are organized into 3 sections:

- [Getting Started](https://nextjs.org/docs/app/getting-started): Step-by-step tutorials to help you create a new application and learn the core Next.js features.
- [Guides](https://nextjs.org/docs/app/guides): Tutorials on specific use cases, choose what's relevant to you.
- [API Reference](https://nextjs.org/docs/app/api-reference): Detailed technical reference for every feature.

Use the sidebar to navigate through the sections, or search (`Ctrl+K` or `Cmd+K`) to quickly find a page.

## App Router and Pages Router

Next.js has two different routers:

- **App Router**: The newer router that supports new React features like Server Components.
- **Pages Router**: The original router, still supported and being improved.

At the top of the sidebar, you'll notice a dropdown menu that allows you to switch between the [App Router](https://nextjs.org/docs/app) and the [Pages Router](https://nextjs.org/docs/pages) docs.

### React version handling

The App Router and Pages Router handle React versions differently:

- **App Router**: Uses [React canary releases](https://react.dev/blog/2023/05/03/react-canaries) built-in, which include all the stable React 19 changes, as well as newer features being validated in frameworks, prior to a new React release.
- **Pages Router**: Uses the React version installed in your project's `package.json`.

This approach ensures new React features work reliably in the App Router while maintaining backwards compatibility for existing Pages Router applications.

## Pre-requisite knowledge

Our documentation assumes some familiarity with web development. Before getting started, it'll help if you're comfortable with:

- HTML
- CSS
- JavaScript
- React

If you're new to React or need a refresher, we recommend starting with our [React Foundations course](https://nextjs.org/learn/react-foundations), and the [Next.js Foundations course](https://nextjs.org/learn/dashboard-app) that has you building an application as you learn.

## Accessibility

For the best experience when using a screen reader, we recommend using Firefox and NVDA, or Safari and VoiceOver.

## Join our Community

If you have questions about anything related to Next.js, you're always welcome to ask our community on [GitHub Discussions](https://github.com/vercel/next.js/discussions), [Discord](https://discord.com/invite/bUG2bvbtHy), [X (Twitter)](https://x.com/nextjs), and [Reddit](https://www.reddit.com/r/nextjs).

## Next Steps

Create your first application and learn the core Next.js features.[Getting StartedLearn how to create full-stack web applications with the Next.js App Router.](https://nextjs.org/docs/app/getting-started)

Was this helpful?

supported.

---

# Pages Router

> Before Next.js 13, the Pages Router was the main way to create routes in Next.js with an intuitive file-system router.

[Next.js Docs](https://nextjs.org/docs)Pages RouterYou are currently viewing the documentation for Pages Router.

# Pages Router

Last updated  April 15, 2025

> You're viewing the documentation for the Pages Router. See the [App Router](https://nextjs.org/docs/app) documentation for the latest features.

The **Pages Router** uses an intuitive file-system router to map each file to a route.

Before Next.js 13, the Pages Router was the main way to create routes in Next.js. It's still supported in newer versions of Next.js, but we recommend migrating to the new [App Router](https://nextjs.org/docs/app) to leverage React's latest features.

[Getting StartedLearn how to create full-stack web applications with Next.js with the Pages Router.](https://nextjs.org/docs/pages/getting-started)[GuidesLearn how to implement common UI patterns and use cases using Next.js](https://nextjs.org/docs/pages/guides)[Building Your ApplicationLearn how to use Next.js features to build your application.](https://nextjs.org/docs/pages/building-your-application)[API ReferenceNext.js API Reference for the Pages Router.](https://nextjs.org/docs/pages/api-reference)

Was this helpful?

supported.
