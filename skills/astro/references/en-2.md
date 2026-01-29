# Islands architecture and more

# Islands architecture

> Learn about how Astro's islands architecture helps keep sites fast.

# Islands architecture

Astro helped pioneer and popularize a new frontend architecture pattern called **Islands Architecture.** Islands architecture works by rendering the majority of your page to fast, static HTML with smaller “islands” of JavaScript added when interactivity or personalization is needed on the page (an image carousel, for example). This avoids the monolithic JavaScript payloads that slow down the responsiveness of many other, modern JavaScript web frameworks.

## A brief history

[Section titled “A brief history”](#a-brief-history)

The term “component island” was first coined by Etsy’s frontend architect [Katie Sylor-Miller](https://sylormiller.com/) in 2019. This idea was then expanded on and documented in [this post](https://jasonformat.com/islands-architecture/) by Preact creator Jason Miller on August 11, 2020.

> The general idea of an “Islands” architecture is deceptively simple: render HTML pages on the server, and inject placeholders or slots around highly dynamic regions […] that can then be “hydrated” on the client into small self-contained widgets, reusing their server-rendered initial HTML.
>
> — Jason Miller, Creator of Preact

The technique that this architectural pattern builds on is also known as **partial** or **selective hydration.**

In contrast, most JavaScript-based web frameworks hydrate & render an entire website as one large JavaScript application (also known as a single-page application, or SPA). SPAs provide simplicity and power but suffer from page-load performance problems due to heavy client-side JavaScript usage.

SPAs have their place, even [embedded inside an Astro page](https://docs.astro.build/en/guides/migrate-to-astro/from-create-react-app/). But, SPAs lack the native ability to selectively and strategically hydrate, making them a heavy-handed choice for most projects on the web today.

Astro became popular as the first mainstream JavaScript web framework with selective hydration built-in, using that same component islands pattern first coined by Sylor-Miller. We’ve since expanded and evolved on Sylor-Miller’s original work, which helped to inspire a similar component island approach to dynamically server-rendered content.

## What is an island?

[Section titled “What is an island?”](#what-is-an-island)

In Astro, an island is an enhanced UI component on an otherwise static page of HTML.

A [client island](#client-islands) is an interactive JavaScript UI component that is hydrated separately from the rest of the page, while a [server island](#server-islands) is a UI component that server-renders its dynamic content separately from the rest of the page.

Both islands run expensive or slower processes independently, on a per-component basis, for optimized page loads.

## Island components

[Section titled “Island components”](#island-components)

Astro components are the building blocks of your page template. They render to static HTML with no client-side runtime.

Think of a client island as an interactive widget floating in a sea of otherwise static, lightweight, server-rendered HTML. Server islands can be added for personalized or dynamic server-rendered elements, such as a logged in visitor’s profile picture.

  Header (interactive island)

Static content like text, images, etc.

 Image carousel (interactive island) Footer (static HTML)

Source: [Islands Architecture: Jason Miller](https://jasonformat.com/islands-architecture/)

An island always runs in isolation from other islands on the page, and multiple islands can exist on a page. Client islands can still share state and communicate with each other, even though they run in different component contexts.

This flexibility allows Astro to support multiple UI frameworks like [React](https://react.dev/), [Preact](https://preactjs.com/), [Svelte](https://svelte.dev/), [Vue](https://vuejs.org/), and [SolidJS](https://www.solidjs.com/). Because they are independent, you can even mix several frameworks on each page.

## Client Islands

[Section titled “Client Islands”](#client-islands)

By default, Astro will automatically render every UI component to just HTML & CSS, **stripping out all client-side JavaScript automatically.**

 src/pages/index.astro

```
<MyReactComponent />
```

This may sound strict, but this behavior is what keeps Astro websites fast by default and protects developers from accidentally sending unnecessary or unwanted JavaScript that might slow down their website.

Turning any static UI component into an interactive island requires only a `client:*` directive. Astro then automatically builds and bundles your client-side JavaScript for optimized performance.

 src/pages/index.astro

```
<MyReactComponent client:load />
```

With islands, client-side JavaScript is only loaded for the explicit interactive components that you mark using `client:*` directives.

And because interaction is configured at the component-level, you can handle different loading priorities for each component based on its usage. For example, `client:idle` tells a component to load when the browser becomes idle, and `client:visible` tells a component to load only once it enters the viewport.

### Benefits of client islands

The most obvious benefit of building with Astro Islands is performance: the majority of your website is converted to fast, static HTML and JavaScript is only loaded for the individual components that need it. JavaScript is one of the slowest assets that you can load per-byte, so every byte counts.

Another benefit is parallel loading. In the example illustration above, the low-priority “image carousel” island doesn’t need to block the high-priority “header” island. The two load in parallel and hydrate in isolation, meaning that the header becomes interactive immediately without having to wait for the heavier carousel lower down the page.

Even better, you can tell Astro exactly how and when to render each component. If that image carousel is really expensive to load, you can attach a special [client directive](https://docs.astro.build/en/reference/directives-reference/#client-directives) that tells Astro to only load the carousel when it becomes visible on the page. If the user never sees it, it never loads.

In Astro, it’s up to you as the developer to explicitly tell Astro which components on the page need to also run in the browser. Astro will only hydrate exactly what’s needed on the page and leave the rest of your site as static HTML.

**Client islands are the secret to Astro’s fast-by-default performance story!**

   Read more about [using JavaScript framework components](https://docs.astro.build/en/guides/framework-components/) in your project.

## Server islands

[Section titled “Server islands”](#server-islands)

Server islands are a way to move expensive or slow server-side code out of the way of the main rendering process, making it easy to combine high-performance static HTML and dynamic server-generated components.

Add the [server:deferdirective](https://docs.astro.build/en/reference/directives-reference/#server-directives) to any Astro component on your page to turn it into its own server island:

 src/pages/index.astro

```
---import Avatar from "../components/Avatar.astro";---<Avatar server:defer />
```

This breaks up your page with smaller areas of server-rendered content that each load in parallel.

Your page’s main content can be rendered immediately with placeholder content, such as a generic avatar until your island’s own content is available. With server islands, having small components of personalized content does not delay the rendering of an otherwise static page.

This rendering pattern was built to be portable. It does not depend on any server infrastructure so it will work with any host, from a Node.js server in a Docker container to the serverless provider of your choice.

### Benefits of server islands

One benefit of server islands is the ability to render the more highly dynamic parts of your page on the fly. This allows the outer shell and main content to be more aggressively cached, providing faster performance.

Another benefit is providing a great visitor experience. Server islands are optimized and load quickly, often even before the browser has even painted the page. But in the short time it takes for your islands to render, you can display custom fallback content and prevent any layout shift.

An example of a site that benefits from Astro’s server islands is an e-commerce storefront. Although the main content of product pages change infrequently, these pages typically have some dynamic pieces:

- The user’s avatar in the header.
- Special deals and sales for the product.
- User reviews.

Using server islands for these elements, your visitor will see the most important part of the page, your product, immediately. Generic avatars, loading spinners, and store announcements can be displayed as fallback content until the personalized parts are available.

   Read more about [using server islands](https://docs.astro.build/en/guides/server-islands/) in your project.  Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Why Astro?

> Astro is the web framework for building content-driven websites like blogs, marketing, and e-commerce. Learn why Astro might be a good choice for your next website.

# Why Astro?

**Astro** is the web framework for building **content-driven websites** like blogs, marketing, and e-commerce. Astro is best-known for pioneering a new [frontend architecture](https://docs.astro.build/en/concepts/islands/) to reduce JavaScript overhead and complexity compared to other frameworks. If you need a website that loads fast and has great SEO, then Astro is for you.

## Features

[Section titled “Features”](#features)

**Astro is an all-in-one web framework.** It includes everything you need to create a website, built-in. There are also hundreds of different [integrations](https://astro.build/integrations/) and [API hooks](https://docs.astro.build/en/reference/integrations-reference/) available to customize a project to your exact use case and needs.

Some highlights include:

- **Islands:** A component-based web architecture optimized for content-driven websites.
- **UI-agnostic:** Supports React, Preact, Svelte, Vue, Solid, HTMX, web components, and more.
- **Server-first:** Moves expensive rendering off of your visitors’ devices.
- **Zero JS, by default:** Less client-side JavaScript to slow your site down.
- **Content collections:** Organize, validate, and provide TypeScript type-safety for your Markdown content.
- **Customizable:** Partytown, MDX, and hundreds of integrations to choose from.

## Design Principles

[Section titled “Design Principles”](#design-principles)

Here are five core design principles to help explain why we built Astro, the problems that it exists to solve, and why Astro may be the best choice for your project or team.

Astro is…

1. **Content-driven:** Astro was designed to showcase your content.
2. **Server-first:** Websites run faster when they render HTML on the server.
3. **Fast by default:** It should be impossible to build a slow website in Astro.
4. **Easy to use:** You don’t need to be an expert to build something with Astro.
5. **Developer-focused:** You should have the resources you need to be successful.

### Content-driven

[Section titled “Content-driven”](#content-driven)

**Astro was designed for building content-rich websites.** This includes marketing sites, publishing sites, documentation sites, blogs, portfolios, landing pages, community sites, and e-commerce sites. If you have content to show, it needs to reach your reader quickly.

By contrast, most modern web frameworks were designed for building *web applications*. These frameworks excel at building more complex, application-like experiences in the browser: logged-in admin dashboards, inboxes, social networks, todo lists, and even native-like applications like [Figma](https://figma.com/) and [Ping](https://ping.gg/). However with that complexity, they can struggle to provide great performance when delivering your content.

Astro’s focus on content from its beginnings as a static site builder have allowed Astro to **sensibly scale up to performant, powerful, dynamic web applications** that still respect your content and your audience. Astro’s unique focus on content lets Astro make tradeoffs and deliver unmatched performance features that wouldn’t make sense for more application-focused web frameworks to implement.

### Server-first

[Section titled “Server-first”](#server-first)

**Astro leverages server rendering over client-side rendering in the browser as much as possible.** This is the same approach that traditional server-side frameworks -- PHP, WordPress, Laravel, Ruby on Rails, etc. -- have been using for decades. But you don’t need to learn a second server-side language to unlock it. With Astro, everything is still just HTML, CSS, and JavaScript (or TypeScript, if you prefer).

This approach stands in contrast to other modern JavaScript web frameworks like Next.js, SvelteKit, Nuxt, Remix, and others. These frameworks were built for client-side rendering of your entire website and include server-side rendering mainly to address performance concerns. This approach has been dubbed the **Single-Page App (SPA)**, in contrast with Astro’s **Multi-Page App (MPA)** approach.

The SPA model has its benefits. However, these come at the expense of additional complexity and performance tradeoffs. These tradeoffs harm page performance -- critical metrics like [Time to Interactive (TTI)](https://web.dev/interactive/) -- which doesn’t make much sense for content-focused websites where first-load performance is essential.

Astro’s server-first approach allows you to opt in to client-side rendering only if, and exactly as, necessary. You can choose to add UI framework components that run on the client. You can take advantage of Astro’s view transitions router for finer control over select page transitions and animations. Astro’s server-first rendering, either pre-rendered or on-demand, provides performant defaults that you can enhance and extend.

### Fast by default

[Section titled “Fast by default”](#fast-by-default)

Good performance is always important, but it is *especially* critical for websites whose success depends on displaying your content. It has been well-proven that poor performance loses you engagement, conversions, and money. For example:

- Every 100ms faster → 1% more conversions ([Mobify](https://web.dev/why-speed-matters/), earning +$380,000/yr)
- 50% faster → 12% more sales ([AutoAnything](https://www.digitalcommerce360.com/2010/08/19/web-accelerator-revs-conversion-and-sales-autoanything/))
- 20% faster → 10% more conversions ([Furniture Village](https://www.thinkwithgoogle.com/intl/en-gb/marketing-strategies/app-and-mobile/furniture-village-and-greenlight-slash-page-load-times-boosting-user-experience/))
- 40% faster → 15% more sign-ups ([Pinterest](https://medium.com/pinterest-engineering/driving-user-growth-with-performance-improvements-cfc50dafadd7))
- 850ms faster → 7% more conversions ([COOK](https://web.dev/why-speed-matters/))
- Every 1 second slower → 10% fewer users ([BBC](https://www.creativebloq.com/features/how-the-bbc-builds-websites-that-scale))

In many web frameworks, it is easy to build a website that looks great during development only to load painfully slow once deployed. JavaScript is often the culprit, since many phones and lower-powered devices rarely match the speed of a developer’s laptop.

Astro’s magic is in how it combines the two values explained above -- a content focus with a server-first architecture -- to make tradeoffs and deliver features that other frameworks cannot. The result is amazing web performance for every website, out of the box. Our goal: **It should be nearly impossible to build a slow website with Astro.**

An Astro website can [load 40% faster with 90% less JavaScript](https://twitter.com/t3dotgg/status/1437195415439360003) than the same site built with the most popular React web framework. But don’t take our word for it: watch Astro’s performance leave Ryan Carniato (creator of Solid.js and Marko) [speechless](https://youtu.be/2ZEMb_H-LYE?t=8163).

### Easy to use

[Section titled “Easy to use”](#easy-to-use)

**Astro’s goal is to be accessible to every web developer.** Astro was designed to feel familiar and approachable regardless of skill level or past experience with web development.

The `.astro` UI language is a superset of HTML: any valid HTML is valid Astro templating syntax! So, if you can write HTML, you can write Astro components! But, it also combines some of our favorite features borrowed from other component languages like JSX expressions (React) and CSS scoping by default (Svelte and Vue). This closeness to HTML also makes it easier to use progressive enhancement and common accessibility patterns without any overhead.

We then made sure that you could also use your favorite UI component languages that you already know, and even reuse components you might already have. React, Preact, Svelte, Vue, Solid, and others, including web components, are all supported for authoring UI components in an Astro project.

Astro was designed to be less complex than other UI frameworks and languages. One big reason for this is that Astro was designed to render on the server, not in the browser. That means that you don’t need to worry about hooks (React), stale closures (also React), refs (Vue), observables (Svelte), atoms, selectors, reactions, or derivations. There is no reactivity on the server, so all of that complexity melts away.

One of our favorite sayings is **opt in to complexity.** We designed Astro to remove as much “required complexity” as possible from the developer experience, especially as you onboard for the first time. You can build a “Hello World” example website in Astro with just HTML and CSS. Then, when you need to build something more powerful, you can incrementally reach for new features and APIs as you go.

### Developer-focused

[Section titled “Developer-focused”](#developer-focused)

We strongly believe that Astro is only a successful project if people love using it. Astro has everything you need to support you as you build with Astro.

Astro invests in developer tools like a great CLI experience from the moment you open your terminal, an official VS Code extension for syntax highlighting, TypeScript and Intellisense, and documentation actively maintained by hundreds of community contributors and available in 14 languages.

Our welcoming, respectful, inclusive community on Discord is ready to provide support, motivation, and encouragement. Open a `#support` thread to get help with your project. Visit our dedicated `#showcase` channel for sharing your Astro sites, blog posts, videos, and even work-in-progress for safe feedback and constructive criticism. Participate in regular live events such as our weekly community call, “Talking and Doc’ing,” and API/bug bashes.

As an open-source project, we welcome contributions of all types and sizes from community members of all experience levels. You are invited to join in roadmap discussions to shape the future of Astro, and we hope you’ll contribute fixes and features to the core codebase, compiler, docs, language tools, websites, and other projects.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Contribute to Astro

> How to get involved and contribute to Astro.

# Contribute to Astro

We welcome contributions of any size and contributors of any skill level. As an open-source project, we believe in giving back to our contributors. We are happy to help with guidance on PRs, technical writing, and turning any feature idea into a reality.

Want to get even more involved? See our [Governance doc](https://github.com/withastro/.github/blob/main/GOVERNANCE.md) for detailed descriptions of different roles, maintainer nomination processes, code review processes, and Code of Conduct enforcement.

## Ways to Contribute

[Section titled “Ways to Contribute”](#ways-to-contribute)

### Project repositories

[Section titled “Project repositories”](#project-repositories)

There are lots of ways to contribute to the Astro Project! Every Astro repository has a README with a link to a `CONTRIBUTING.md` file in the root of the project.

Visit [Astro’s GitHub profile](https://github.com/withastro) to find the repositories for:

- The [main Astro codebase](https://github.com/withastro/astro), including official integrations and starter templates.
- [Astro Docs](https://github.com/withastro/docs), an entire Astro website! Contribute not just written content, but also Astro code addressing a11y, CSS, UI, and UX concerns. We also make our documentation available in several languages, so we need help translating the entire site.
- The [Astro compiler](https://github.com/withastro/compiler), written in Go, distributed as WASM.
- Astro’s [language tools](https://github.com/withastro/language-tools), the editor tooling required for the Astro language (`.astro` files).
- [Starlight](https://github.com/withastro/starlight), Astro’s official documentation framework.
- The [Astro Roadmap](https://github.com/withastro/roadmap) where the future of Astro is shaped! Ideas, suggestions, and formal RFC proposals for the Astro project.

### Types of contributions

[Section titled “Types of contributions”](#types-of-contributions)

In addition to contributing your own code or content, you can also make a huge contribution by getting involved by leaving review comments on PRs, adding ideas in existing GitHub Issues and Discussions, and participating in our “Pinned” issue maintenance tasks!

Every PR, especially translation PRs, needs reviewers! Reviewing PRs and leaving comments, suggestions, or an approving “LGTM!” (“Looks Good To Me!”) is a great way to get started in any repository, and to learn more about Astro.

We also have a very active [Discord](https://astro.build/chat) community! We value the contributions of those who welcome new members, answer support questions, and share what they have built with and for Astro! Beyond traditional GitHub contributions, Astro recognizes and supports community members who engage with our community, share Astro in blog posts, videos and conference talks, and help maintain the health of our community.

## Contributing to Docs

[Section titled “Contributing to Docs”](#contributing-to-docs)

We have several guides available to assist you with contributing to Astro Docs.

Whether it’s your very first contribution to open-source, or you need to add docs for the new Astro feature you just built, or you’re an experienced translator looking for the next page to translate, or you’d like to learn more about helping as a PR reviewer… we’ve got you covered!

Please visit our dedicated site [Astro DocsDocs](https://contribute.docs.astro.build), where you’ll find our documentation to help you contribute to Astro Docs as a typo-fixer, a writer, a translator, a feature-builder, and even as a PR reviewer.

## Our contributors

[Section titled “Our contributors”](#our-contributors)

These docs are brought to you by all these helpful people. [Join us on GitHub!](https://github.com/withastro/docs)

  Thanks to @5t3ph for https://smolcss.dev/#smol-avatar-list!

-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-

  Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Develop and build

> How to start working on a new project.

# Develop and build

Once you have an Astro project, now you’re ready to build with Astro! 🚀

## Edit your project

[Section titled “Edit your project”](#edit-your-project)

To make changes to your project, open your project folder in your code editor. Working in development mode with the dev server running allows you to see updates to your site as you edit the code.

You can also [customize aspects of your development environment](#configure-your-dev-environment) such as configuring TypeScript or installing the official Astro editor extensions.

### Start the Astro dev server

[Section titled “Start the Astro dev server”](#start-the-astro-dev-server)

Astro comes with a built-in development server that has everything you need for project development. The `astro dev` CLI command will start the local development server so that you can see your new website in action for the very first time.

Every starter template comes with a pre-configured script that will run `astro dev` for you. After navigating into your project directory, use your favorite package manager to run this command and start the Astro development server.

- [npm](#tab-panel-1395)
- [pnpm](#tab-panel-1396)
- [Yarn](#tab-panel-1397)

   Terminal window

```
npm run dev
```

   Terminal window

```
pnpm run dev
```

   Terminal window

```
yarn run dev
```

If all goes well, Astro will now be serving your project on [http://localhost:4321/](http://localhost:4321/). Visit that link in your browser and see your new site!

### Work in development mode

[Section titled “Work in development mode”](#work-in-development-mode)

Astro will listen for live file changes in your `src/` directory and update your site preview as you build, so you will not need to restart the server as you make changes during development. You will always be able to see an up-to-date version of your site in your browser when the dev server is running.

When viewing your site in the browser, you’ll have access to the [Astro dev toolbar](https://docs.astro.build/en/guides/dev-toolbar/). As you build, it will help you inspect your [islands](https://docs.astro.build/en/concepts/islands/), spot accessibility issues, and more.

If you aren’t able to open your project in the browser after starting the dev server, go back to the terminal where you ran the `dev` command and check the message displayed. It should tell you if an error occurred, or if your project is being served at a different URL than [http://localhost:4321/](http://localhost:4321/).

## Build and preview your site

[Section titled “Build and preview your site”](#build-and-preview-your-site)

To check the version of your site that will be created at build time, quit the dev server (Ctrl + C) and run the appropriate build command for your package manager in your terminal:

- [npm](#tab-panel-1398)
- [pnpm](#tab-panel-1399)
- [Yarn](#tab-panel-1400)

   Terminal window

```
npm run build
```

   Terminal window

```
pnpm build
```

   Terminal window

```
yarn run build
```

Astro will build a deploy-ready version of your site in a separate folder (`dist/` by default) and you can watch its progress in the terminal. This will alert you to any build errors in your project before you deploy to production. If TypeScript is configured to `strict` or `strictest`, the `build` script will also check your project for type errors.

When the build is finished, run the appropriate `preview` command (e.g. `npm run preview`) in your terminal and you can view the built version of your site locally in the same browser preview window.

Note that this previews your code as it existed when the build command was last run. This is meant to give you a preview of how your site will look when it is deployed to the web. Any later changes you make to your code after building will **not** be reflected while you preview your site until you run the build command again.

Use (Ctrl + C) to quit the preview and run another terminal command, such as restarting the dev server to go back to [working in development mode](#work-in-development-mode) which does update as you edit to show a live preview of your code changes.

   Read more about [the Astro CLI](https://docs.astro.build/en/reference/cli-reference/) and the terminal commands you will use as you build with Astro.

## Next Steps

[Section titled “Next Steps”](#next-steps)

Success! You are now ready to start building with Astro! 🥳

Here are a few things that we recommend exploring next. You can read them in any order. You can even leave our documentation for a bit and go play in your new Astro project codebase, coming back here whenever you run into trouble or have a question.

### Configure your dev environment

[Section titled “Configure your dev environment”](#configure-your-dev-environment)

Explore the guides below to customize your development experience.

   [Editor Setup](https://docs.astro.build/en/editor-setup/) Customize your code editor to improve the Astro developer experience and unlock new features.     [Dev Toolbar](https://docs.astro.build/en/guides/dev-toolbar/) Explore the helpful features of the dev toolbar.     [TypeScript Configuration](https://docs.astro.build/en/guides/typescript/) Configure options for type-checking, IntelliSense, and more.

### Explore Astro’s Features

[Section titled “Explore Astro’s Features”](#explore-astros-features)   [Understand your codebase](https://docs.astro.build/en/basics/project-structure/) Learn about Astro’s file structure in our Project Structure guide.     [Create content collections](https://docs.astro.build/en/guides/content-collections/) Add content to your new site with frontmatter validation and automatic type-safety.     [Add view transitions](https://docs.astro.build/en/guides/view-transitions/) Create seamless page transitions and animations.     [Learn about Islands](https://docs.astro.build/en/concepts/islands/) Read about Astro's islands architecture.

### Take the introductory tutorial

[Section titled “Take the introductory tutorial”](#take-the-introductory-tutorial)

Build a fully functional Astro blog starting from a single blank page in our [introductory tutorial](https://docs.astro.build/en/tutorial/0-introduction/).

This is a great way to see how Astro works and walks you through the basics of pages, layouts, components, routing, islands, and more. It also includes an optional, beginner-friendly unit for those newer to web development concepts in general, which will guide you through installing the necessary applications on your computer, creating a GitHub account, and deploying your site.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Editor setup

> Set up your code editor to build with Astro.

# Editor setup

Customize your code editor to improve the Astro developer experience and unlock new features.

## VS Code

[Section titled “VS Code”](#vs-code)

[VS Code](https://code.visualstudio.com/) is a popular code editor for web developers, built by Microsoft. The VS Code engine also powers popular in-browser code editors like [GitHub Codespaces](https://github.com/features/codespaces).

Astro works with any code editor. However, VS Code is our recommended editor for Astro projects. We maintain an official [Astro VS Code Extension](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode) that unlocks several key features and developer experience improvements for Astro projects.

- Syntax highlighting for `.astro` files.
- TypeScript type information for `.astro` files.
- [VS Code Intellisense](https://code.visualstudio.com/docs/editor/intellisense) for code completion, hints and more.

To get started, install the [Astro VS Code Extension](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode) today.

   See how to [set up TypeScript](https://docs.astro.build/en/guides/typescript/) in your Astro project.

## Zed

[Section titled “Zed”](#zed)

[Zed](https://zed.dev/) is a high-performance, multiplayer code editor that is optimized for speed and large projects. Their [Astro extension](https://zed.dev/extensions/astro) includes features like syntax highlighting for `.astro` files, code completion, formatting, diagnostics, and go-to-definition.

## JetBrains IDEs

[Section titled “JetBrains IDEs”](#jetbrains-ides)

[Webstorm](https://www.jetbrains.com/webstorm/) is a JavaScript and TypeScript IDE that added support for the Astro Language Server in version 2024.2. This update brings features like syntax highlighting, code completion, and formatting.

Install the official plugin through [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/20959-astro) or by searching for “Astro” in the IDE’s Plugins tab. You can toggle the language server in `Settings | Languages & Frameworks | TypeScript | Astro`.

For more information on Astro support in Webstorm, check out [the official Webstorm Astro Documentation](https://www.jetbrains.com/help/webstorm/astro.html).

## Other Code Editors

[Section titled “Other Code Editors”](#other-code-editors)

Our amazing community maintains several extensions for other popular editors, including:

- [VS Code Extension on Open VSX](https://open-vsx.org/extension/astro-build/astro-vscode) Official  - The official Astro VS Code Extension, available on the Open VSX registry for editors like [Cursor](https://cursor.com) or [VSCodium](https://vscodium.com/).
- [Vim Plugin](https://github.com/wuelnerdotexe/vim-astro) Community  - Provides syntax highlighting, indentation, and code folding support for Astro inside of Vim or Neovim
- Neovim [LSP](https://github.com/neovim/nvim-lspconfig/blob/master/doc/configs.md#astro) and [TreeSitter](https://github.com/virchau13/tree-sitter-astro) Plugins Community  - Provides syntax highlighting, treesitter parsing, and code completion for Astro inside of Neovim
- Emacs - See instructions for [Configuring Emacs and Eglot](https://medium.com/@jrmjrm/configuring-emacs-and-eglot-to-work-with-astro-language-server-9408eb709ab0) Community  to work with Astro
- [Astro syntax highlighting for Sublime Text](https://packagecontrol.io/packages/Astro) Community  - The Astro package for Sublime Text, available on the Sublime Text package manager.
- [Nova Extension](https://extensions.panic.com/extensions/sciencefidelity/sciencefidelity.astro/) Community  - Provides syntax highlighting and code completion for Astro inside of Nova

## In-Browser Editors

[Section titled “In-Browser Editors”](#in-browser-editors)

In addition to local editors, Astro also runs well on in-browser hosted editors, including:

- [StackBlitz](https://stackblitz.com/) and [CodeSandbox](https://codesandbox.io/) - online editors that run in your browser, with built-in syntax highlighting support for `.astro` files. No installation or configuration required!
- [GitHub.dev](https://github.dev/) - allows you to install the Astro VS Code extension as a [web extension](https://code.visualstudio.com/api/extension-guides/web-extensions), which gives you access to only some of the full extension features. Currently, only syntax highlighting is supported.
- [Firebase Studio](https://firebase.studio/) - a full dev environment in the cloud that can install the official Astro VS Code Extension from Open VSX.

## Other tools

[Section titled “Other tools”](#other-tools)

### ESLint

[Section titled “ESLint”](#eslint)

[ESLint](https://eslint.org/) is a popular linter for JavaScript and JSX. For Astro support, [a community maintained plugin](https://github.com/ota-meshi/eslint-plugin-astro) can be installed.

See [the project’s User Guide](https://ota-meshi.github.io/eslint-plugin-astro/user-guide/) for more information on how to install and set up ESLint for your project.

### Stylelint

[Section titled “Stylelint”](#stylelint)

[Stylelint](https://stylelint.io/) is a popular linter for CSS. [A community maintained Stylelint configuration](https://github.com/ota-meshi/stylelint-config-html) provides Astro support.

Installation instructions, editor integration, and additional information can be found in the project’s README.

### Biome

[Section titled “Biome”](#biome)

[Biome](https://biomejs.dev/) is an all-in-one linter and formatter for the web. [Biome currently has experimental support for.astrofiles](https://biomejs.dev/internals/language-support/#html-super-languages-support), and can be used to lint and format the frontmatter in `.astro` files.

### Prettier

[Section titled “Prettier”](#prettier)

[Prettier](https://prettier.io/) is a popular formatter for JavaScript, HTML, CSS, and more. If you’re using the [Astro VS Code Extension](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode), code formatting with Prettier is included.

To add support for formatting `.astro` files outside of the editor (e.g. CLI) or inside editors that don’t support our editor tooling, install [the official Astro Prettier plugin](https://github.com/withastro/prettier-plugin-astro).

1. Install `prettier` and `prettier-plugin-astro`.
  - [npm](#tab-panel-1401)
  - [pnpm](#tab-panel-1402)
  - [Yarn](#tab-panel-1403)
     Terminal window
  ```
  npm install --save-dev --save-exact prettier prettier-plugin-astro
  ```
     Terminal window
  ```
  pnpm add --save-dev --save-exact prettier prettier-plugin-astro
  ```
     Terminal window
  ```
  yarn add --dev --exact prettier prettier-plugin-astro
  ```
2. Create a `.prettierrc` configuration file (or `.prettierrc.json`, `.prettierrc.mjs`, or [other supported formats](https://prettier.io/docs/configuration)) in the root of your project and add `prettier-plugin-astro` to it.
  In this file, also manually specify the parser for Astro files.
   .prettierrc
  ```
  {  "plugins": ["prettier-plugin-astro"],  "overrides": [    {      "files": "*.astro",      "options": {        "parser": "astro"      }    }  ]}
  ```
3. Optionally, install other Prettier plugins for your project, and add them to the configuration file. These additional plugins may need to be listed in a specific order. For example, if you use Tailwind, `prettier-plugin-tailwindcss` must be [the last Prettier plugin in the plugins array](https://github.com/tailwindlabs/prettier-plugin-tailwindcss#compatibility-with-other-prettier-plugins).
   .prettierrc
  ```
  {  "plugins": [    "prettier-plugin-astro",    "prettier-plugin-tailwindcss" // needs to be last  ],  "overrides": [    {      "files": "*.astro",      "options": {        "parser": "astro"      }    }  ]}
  ```
4. Run the following command in your terminal to format your files.
  - [npm](#tab-panel-1404)
  - [pnpm](#tab-panel-1405)
  - [Yarn](#tab-panel-1406)
     Terminal window
  ```
  npx prettier . --write
  ```
     Terminal window
  ```
  pnpm exec prettier . --write
  ```
     Terminal window
  ```
  yarn exec prettier . --write
  ```

See the [Prettier plugin’s README](https://github.com/withastro/prettier-plugin-astro/blob/main/README.md) for more information about its supported options, how to set up Prettier inside VS Code, and more.

### dprint

[Section titled “dprint”](#dprint)

[dprint](https://dprint.dev/) is a highly-configurable code formatter that supports many languages, including JavaScript, TypeScript, CSS, and more. Support for `.astro` files can be added using the [markup_fmt plugin](https://github.com/g-plane/markup_fmt).

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Astro Docs

> Guides, resources, and API references to help you build with Astro — the web framework for content-driven websites.

What will you build with Astro?

Explore [Astro starter themes](https://astro.build/themes/) for blogs, portfolios, docs, landing pages, SaaS, marketing, ecommerce sites, and more!
