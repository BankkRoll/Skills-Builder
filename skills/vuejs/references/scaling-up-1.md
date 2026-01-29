# Routing​ and more

# Routing​

> Vue.js - The Progressive JavaScript Framework

# Routing​

## Client-Side vs. Server-Side Routing​

Routing on the server side means the server is sending a response based on the URL path that the user is visiting. When we click on a link in a traditional server-rendered web app, the browser receives an HTML response from the server and reloads the entire page with the new HTML.

In a [Single-Page Application](https://developer.mozilla.org/en-US/docs/Glossary/SPA) (SPA), however, the client-side JavaScript can intercept the navigation, dynamically fetch new data, and update the current page without full page reloads. This typically results in a more snappy user experience, especially for use cases that are more like actual "applications", where the user is expected to perform many interactions over a long period of time.

In such SPAs, the "routing" is done on the client side, in the browser. A client-side router is responsible for managing the application's rendered view using browser APIs such as [History API](https://developer.mozilla.org/en-US/docs/Web/API/History) or the [hashchangeevent](https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event).

## Official Router​

[Watch a Free Video Course on Vue School](https://vueschool.io/courses/vue-router-4-for-everyone?friend=vuejs)

Vue is well-suited for building SPAs. For most SPAs, it's recommended to use the officially-supported [Vue Router library](https://github.com/vuejs/router). For more details, see Vue Router's [documentation](https://router.vuejs.org/).

## Simple Routing from Scratch​

If you only need very simple routing and do not wish to involve a full-featured router library, you can do so with [Dynamic Components](https://vuejs.org/guide/essentials/component-basics#dynamic-components) and update the current component state by listening to browser [hashchangeevents](https://developer.mozilla.org/en-US/docs/Web/API/Window/hashchange_event) or using the [History API](https://developer.mozilla.org/en-US/docs/Web/API/History).

Here's a bare-bone example:

vue

```
<script setup>
import { ref, computed } from 'vue'
import Home from './Home.vue'
import About from './About.vue'
import NotFound from './NotFound.vue'

const routes = {
  '/': Home,
  '/about': About
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/'] || NotFound
})
</script>

<template>
  <a href="#/">Home</a> |
  <a href="#/about">About</a> |
  <a href="#/non-existent-path">Broken Link</a>
  <component :is="currentView" />
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNptUk1vgkAQ/SsTegAThZp4MmhikzY9mKanXkoPWxjLRpgly6JN1P/eWb5Eywlm572ZN2/m5GyKwj9U6CydsIy1LAyUaKpiHZHMC6UNnEDjbgqxyovKYAIX2GmVg8sktwe9qhzbdz+wga15TW++VWX6fB3dAt6UeVEVJT2me2hhEcWKSgOamVjCCk4RAbiBu6xbT5tI2ML8VDeI6HLlxZXWSOZdmJTJPJB3lJSoo5+pWBipyE9FmU4soU2IJHk+MGUrS4OE2nMtIk4F/aA7BW8Cq3WjYlDbP4isQu4wVp0F1Q1uFH1IPDK+c9cb1NW8B03tyJ//uvhlJmP05hM4n60TX/bb2db0CoNmpbxMDgzmRSYMcgQQCkjZhlXkPASRs7YmhoFYw/k+WXvKiNrTcQgpmuFv7ZOZFSyQ4U9a7ZFgK2lvSTXFDqmIQbCUJTMHFkQOBAwKg16kM3W6O7K3eSs+nbeK+eee1V/XKK0dY4Q3vLhR6uJxMUK8/AFKaB6k)

vue

```
<script>
import Home from './Home.vue'
import About from './About.vue'
import NotFound from './NotFound.vue'

const routes = {
  '/': Home,
  '/about': About
}

export default {
  data() {
    return {
      currentPath: window.location.hash
    }
  },
  computed: {
    currentView() {
      return routes[this.currentPath.slice(1) || '/'] || NotFound
    }
  },
  mounted() {
    window.addEventListener('hashchange', () => {
		  this.currentPath = window.location.hash
		})
  }
}
</script>

<template>
  <a href="#/">Home</a> |
  <a href="#/about">About</a> |
  <a href="#/non-existent-path">Broken Link</a>
  <component :is="currentView" />
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNptUstO6zAQ/ZVR7iKtVJKLxCpKK3Gli1ggxIoNZmGSKbFoxpEzoUi0/87YeVBKNonHPmfOmcdndN00yXuHURblbeFMwxtFpm6sY7i1NcLW2RriJPWBB8bT8/WL7Xh6D9FPwL3lG9tROWHGiwGmqLDUMjhhYgtr+FQEEKdxFqRXfaR9YrkKAoqOnocfQaDEre523PNKzXqx7M8ADrlzNEYAReccEj9orjLYGyrtPtnZQrOxlFS6rXqgZJdPUC5s3YivMhuTDCkeDe6/dSalvognrkybnIgl7c4UuLhcwuHgS3v2/7EPvzRruRXJ7/SDU12W/98l451pGQndIvaWi0rTK8YrEPx64ymKFQOce5DOzlfs4cdlkA+NzdNpBSRgrJudZpQIINdQOdyuVfQnVdHGzydP9QYO549hXIII45qHkKUL/Ail8EUjBgX+z9k3JLgz9OZJgeInYElAkJlWmCcDUBGkAsrTyWS0isYV9bv803x1OTiWwzlrWtxZ2lDGDO90mWepV3+vZojHL3QQKQE=)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/routing.md)

---

# Single

> Vue.js - The Progressive JavaScript Framework

# Single-File Components​

## Introduction​

Vue Single-File Components (a.k.a. `*.vue` files, abbreviated as **SFC**) is a special file format that allows us to encapsulate the template, logic, **and** styling of a Vue component in a single file. Here's an example SFC:

vue

```
<script>
export default {
  data() {
    return {
      greeting: 'Hello World!'
    }
  }
}
</script>

<template>
  <p class="greeting">{{ greeting }}</p>
</template>

<style>
.greeting {
  color: red;
  font-weight: bold;
}
</style>
```

vue

```
<script setup>
import { ref } from 'vue'
const greeting = ref('Hello World!')
</script>

<template>
  <p class="greeting">{{ greeting }}</p>
</template>

<style>
.greeting {
  color: red;
  font-weight: bold;
}
</style>
```

As we can see, Vue SFC is a natural extension of the classic trio of HTML, CSS and JavaScript. The `<template>`, `<script>`, and `<style>` blocks encapsulate and colocate the view, logic and styling of a component in the same file. The full syntax is defined in the [SFC Syntax Specification](https://vuejs.org/api/sfc-spec).

## Why SFC​

While SFCs require a build step, there are numerous benefits in return:

- Author modularized components using familiar HTML, CSS and JavaScript syntax
- [Colocation of inherently coupled concerns](#what-about-separation-of-concerns)
- Pre-compiled templates without runtime compilation cost
- [Component-scoped CSS](https://vuejs.org/api/sfc-css-features)
- [More ergonomic syntax when working with Composition API](https://vuejs.org/api/sfc-script-setup)
- More compile-time optimizations by cross-analyzing template and script
- [IDE support](https://vuejs.org/guide/scaling-up/tooling#ide-support) with auto-completion and type-checking for template expressions
- Out-of-the-box Hot-Module Replacement (HMR) support

SFC is a defining feature of Vue as a framework, and is the recommended approach for using Vue in the following scenarios:

- Single-Page Applications (SPA)
- Static Site Generation (SSG)
- Any non-trivial frontend where a build step can be justified for better development experience (DX).

That said, we do realize there are scenarios where SFCs can feel like overkill. This is why Vue can still be used via plain JavaScript without a build step. If you are just looking for enhancing largely static HTML with light interactions, you can also check out [petite-vue](https://github.com/vuejs/petite-vue), a 6 kB subset of Vue optimized for progressive enhancement.

## How It Works​

Vue SFC is a framework-specific file format and must be pre-compiled by [@vue/compiler-sfc](https://github.com/vuejs/core/tree/main/packages/compiler-sfc) into standard JavaScript and CSS. A compiled SFC is a standard JavaScript (ES) module - which means with proper build setup you can import an SFC like a module:

js

```
import MyComponent from './MyComponent.vue'

export default {
  components: {
    MyComponent
  }
}
```

`<style>` tags inside SFCs are typically injected as native `<style>` tags during development to support hot updates. For production they can be extracted and merged into a single CSS file.

You can play with SFCs and explore how they are compiled in the [Vue SFC Playground](https://play.vuejs.org/).

In actual projects, we typically integrate the SFC compiler with a build tool such as [Vite](https://vitejs.dev/) or [Vue CLI](http://cli.vuejs.org/) (which is based on [webpack](https://webpack.js.org/)), and Vue provides official scaffolding tools to get you started with SFCs as fast as possible. Check out more details in the [SFC Tooling](https://vuejs.org/guide/scaling-up/tooling) section.

## What About Separation of Concerns?​

Some users coming from a traditional web development background may have the concern that SFCs are mixing different concerns in the same place - which HTML/CSS/JS were supposed to separate!

To answer this question, it is important for us to agree that **separation of concerns is not equal to the separation of file types**. The ultimate goal of engineering principles is to improve the maintainability of codebases. Separation of concerns, when applied dogmatically as separation of file types, does not help us reach that goal in the context of increasingly complex frontend applications.

In modern UI development, we have found that instead of dividing the codebase into three huge layers that interweave with one another, it makes much more sense to divide them into loosely-coupled components and compose them. Inside a component, its template, logic, and styles are inherently coupled, and colocating them actually makes the component more cohesive and maintainable.

Note even if you don't like the idea of Single-File Components, you can still leverage its hot-reloading and pre-compilation features by separating your JavaScript and CSS into separate files using [Src Imports](https://vuejs.org/api/sfc-spec#src-imports).

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/sfc.md)

---

# Server

> Vue.js - The Progressive JavaScript Framework

# Server-Side Rendering (SSR)​

## Overview​

### What is SSR?​

Vue.js is a framework for building client-side applications. By default, Vue components produce and manipulate DOM in the browser as output. However, it is also possible to render the same components into HTML strings on the server, send them directly to the browser, and finally "hydrate" the static markup into a fully interactive app on the client.

A server-rendered Vue.js app can also be considered "isomorphic" or "universal", in the sense that the majority of your app's code runs on both the server **and** the client.

### Why SSR?​

Compared to a client-side Single-Page Application (SPA), the advantage of SSR primarily lies in:

- **Faster time-to-content**: this is more prominent on slow internet or slow devices. Server-rendered markup doesn't need to wait until all JavaScript has been downloaded and executed to be displayed, so your user will see a fully-rendered page sooner. In addition, data fetching is done on the server-side for the initial visit, which likely has a faster connection to your database than the client. This generally results in improved [Core Web Vitals](https://web.dev/vitals/) metrics, better user experience, and can be critical for applications where time-to-content is directly associated with conversion rate.
- **Unified mental model**: you get to use the same language and the same declarative, component-oriented mental model for developing your entire app, instead of jumping back and forth between a backend templating system and a frontend framework.
- **Better SEO**: the search engine crawlers will directly see the fully rendered page.
  TIP
  As of now, Google and Bing can index synchronous JavaScript applications just fine. Synchronous being the key word there. If your app starts with a loading spinner, then fetches content via Ajax, the crawler will not wait for you to finish. This means if you have content fetched asynchronously on pages where SEO is important, SSR might be necessary.

There are also some trade-offs to consider when using SSR:

- Development constraints. Browser-specific code can only be used inside certain lifecycle hooks; some external libraries may need special treatment to be able to run in a server-rendered app.
- More involved build setup and deployment requirements. Unlike a fully static SPA that can be deployed on any static file server, a server-rendered app requires an environment where a Node.js server can run.
- More server-side load. Rendering a full app in Node.js is going to be more CPU-intensive than just serving static files, so if you expect high traffic, be prepared for corresponding server load and wisely employ caching strategies.

Before using SSR for your app, the first question you should ask is whether you actually need it. It mostly depends on how important time-to-content is for your app. For example, if you are building an internal dashboard where an extra few hundred milliseconds on initial load doesn't matter that much, SSR would be an overkill. However, in cases where time-to-content is absolutely critical, SSR can help you achieve the best possible initial load performance.

### SSR vs. SSG​

**Static Site Generation (SSG)**, also referred to as pre-rendering, is another popular technique for building fast websites. If the data needed to server-render a page is the same for every user, then instead of rendering the page every time a request comes in, we can render it only once, ahead of time, during the build process. Pre-rendered pages are generated and served as static HTML files.

SSG retains the same performance characteristics of SSR apps: it provides great time-to-content performance. At the same time, it is cheaper and easier to deploy than SSR apps because the output is static HTML and assets. The keyword here is **static**: SSG can only be applied to pages providing static data, i.e. data that is known at build time and can not change between requests. Every time the data changes, a new deployment is needed.

If you're only investigating SSR to improve the SEO of a handful of marketing pages (e.g. `/`, `/about`, `/contact`, etc.), then you probably want SSG instead of SSR. SSG is also great for content-based websites such as documentation sites or blogs. In fact, this website you are reading right now is statically generated using [VitePress](https://vitepress.dev/), a Vue-powered static site generator.

## Basic Tutorial​

### Rendering an App​

Let's take a look at the most bare-bones example of Vue SSR in action.

1. Create a new directory and `cd` into it
2. Run `npm init -y`
3. Add `"type": "module"` in `package.json` so that Node.js runs in [ES modules mode](https://nodejs.org/api/esm.html#modules-ecmascript-modules).
4. Run `npm install vue`
5. Create an `example.js` file:

js

```
// this runs in Node.js on the server.
import { createSSRApp } from 'vue'
// Vue's server-rendering API is exposed under `vue/server-renderer`.
import { renderToString } from 'vue/server-renderer'

const app = createSSRApp({
  data: () => ({ count: 1 }),
  template: `<button @click="count++">{{ count }}</button>`
})

renderToString(app).then((html) => {
  console.log(html)
})
```

Then run:

sh

```
> node example.js
```

It should print the following to the command line:

```
<button>1</button>
```

[renderToString()](https://vuejs.org/api/ssr#rendertostring) takes a Vue app instance and returns a Promise that resolves to the rendered HTML of the app. It is also possible to stream rendering using the [Node.js Stream API](https://nodejs.org/api/stream.html) or [Web Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API). Check out the [SSR API Reference](https://vuejs.org/api/ssr) for full details.

We can then move the Vue SSR code into a server request handler, which wraps the application markup with the full page HTML. We will be using [express](https://expressjs.com/) for the next steps:

- Run `npm install express`
- Create the following `server.js` file:

js

```
import express from 'express'
import { createSSRApp } from 'vue'
import { renderToString } from 'vue/server-renderer'

const server = express()

server.get('/', (req, res) => {
  const app = createSSRApp({
    data: () => ({ count: 1 }),
    template: `<button @click="count++">{{ count }}</button>`
  })

  renderToString(app).then((html) => {
    res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Vue SSR Example</title>
      </head>
      <body>
        <div id="app">${html}</div>
      </body>
    </html>
    `)
  })
})

server.listen(3000, () => {
  console.log('ready')
})
```

Finally, run `node server.js` and visit `http://localhost:3000`. You should see the page working with the button.

[Try it on StackBlitz](https://stackblitz.com/fork/vue-ssr-example-basic?file=index.js)

### Client Hydration​

If you click the button, you'll notice the number doesn't change. The HTML is completely static on the client since we are not loading Vue in the browser.

To make the client-side app interactive, Vue needs to perform the **hydration** step. During hydration, it creates the same Vue application that was run on the server, matches each component to the DOM nodes it should control, and attaches DOM event listeners.

To mount an app in hydration mode, we need to use [createSSRApp()](https://vuejs.org/api/application#createssrapp) instead of `createApp()`:

js

```
// this runs in the browser.
import { createSSRApp } from 'vue'

const app = createSSRApp({
  // ...same app as on server
})

// mounting an SSR app on the client assumes
// the HTML was pre-rendered and will perform
// hydration instead of mounting new DOM nodes.
app.mount('#app')
```

### Code Structure​

Notice how we need to reuse the same app implementation as on the server. This is where we need to start thinking about code structure in an SSR app - how do we share the same application code between the server and the client?

Here we will demonstrate the most bare-bones setup. First, let's split the app creation logic into a dedicated file, `app.js`:

app.jsjs

```
// (shared between server and client)
import { createSSRApp } from 'vue'

export function createApp() {
  return createSSRApp({
    data: () => ({ count: 1 }),
    template: `<button @click="count++">{{ count }}</button>`
  })
}
```

This file and its dependencies are shared between the server and the client - we call them **universal code**. There are a number of things you need to pay attention to when writing universal code, as we will [discuss below](#writing-ssr-friendly-code).

Our client entry imports the universal code, creates the app, and performs the mount:

client.jsjs

```
import { createApp } from './app.js'

createApp().mount('#app')
```

And the server uses the same app creation logic in the request handler:

server.jsjs

```
// (irrelevant code omitted)
import { createApp } from './app.js'

server.get('/', (req, res) => {
  const app = createApp()
  renderToString(app).then(html => {
    // ...
  })
})
```

In addition, in order to load the client files in the browser, we also need to:

1. Serve client files by adding `server.use(express.static('.'))` in `server.js`.
2. Load the client entry by adding `<script type="module" src="/client.js"></script>` to the HTML shell.
3. Support usage like `import * from 'vue'` in the browser by adding an [Import Map](https://github.com/WICG/import-maps) to the HTML shell.

[Try the completed example on StackBlitz](https://stackblitz.com/fork/vue-ssr-example?file=index.js). The button is now interactive!

## Higher Level Solutions​

Moving from the example to a production-ready SSR app involves a lot more. We will need to:

- Support Vue SFCs and other build step requirements. In fact, we will need to coordinate two builds for the same app: one for the client, and one for the server.
  TIP
  Vue components are compiled differently when used for SSR - templates are compiled into string concatenations instead of Virtual DOM render functions for more efficient rendering performance.
- In the server request handler, render the HTML with the correct client-side asset links and optimal resource hints. We may also need to switch between SSR and SSG mode, or even mix both in the same app.
- Manage routing, data fetching, and state management stores in a universal manner.

A complete implementation would be quite complex and depends on the build toolchain you have chosen to work with. Therefore, we highly recommend going with a higher-level, opinionated solution that abstracts away the complexity for you. Below we will introduce a few recommended SSR solutions in the Vue ecosystem.

### Nuxt​

[Nuxt](https://nuxt.com/) is a higher-level framework built on top of the Vue ecosystem which provides a streamlined development experience for writing universal Vue applications. Better yet, you can also use it as a static site generator! We highly recommend giving it a try.

### Quasar​

[Quasar](https://quasar.dev) is a complete Vue-based solution that allows you to target SPA, SSR, PWA, mobile app, desktop app, and browser extension all using one codebase. It not only handles the build setup, but also provides a full collection of Material Design compliant UI components.

### Vite SSR​

Vite provides built-in [support for Vue server-side rendering](https://vitejs.dev/guide/ssr.html), but it is intentionally low-level. If you wish to go directly with Vite, check out [vite-plugin-ssr](https://vite-plugin-ssr.com/), a community plugin that abstracts away many challenging details for you.

You can also find an example Vue + Vite SSR project using manual setup [here](https://github.com/vitejs/vite-plugin-vue/tree/main/playground/ssr-vue), which can serve as a base to build upon. Note this is only recommended if you are experienced with SSR / build tools and really want to have complete control over the higher-level architecture.

## Writing SSR-friendly Code​

Regardless of your build setup or higher-level framework choice, there are some principles that apply in all Vue SSR applications.

### Reactivity on the Server​

During SSR, each request URL maps to a desired state of our application. There is no user interaction and no DOM updates, so reactivity is unnecessary on the server. By default, reactivity is disabled during SSR for better performance.

### Component Lifecycle Hooks​

Since there are no dynamic updates, lifecycle hooks such as `mounted``onMounted` or `updated``onUpdated` will **NOT** be called during SSR and will only be executed on the client. The only hooks that are called during SSR are `beforeCreate` and `created`

You should avoid code that produces side effects that need cleanup in `beforeCreate` and `created``setup()` or the root scope of `<script setup>`. An example of such side effects is setting up timers with `setInterval`. In client-side only code we may setup a timer and then tear it down in `beforeUnmount``onBeforeUnmount` or `unmounted``onUnmounted`. However, because the unmount hooks will never be called during SSR, the timers will stay around forever. To avoid this, move your side-effect code into `mounted``onMounted` instead.

### Access to Platform-Specific APIs​

Universal code cannot assume access to platform-specific APIs, so if your code directly uses browser-only globals like `window` or `document`, they will throw errors when executed in Node.js, and vice-versa.

For tasks that are shared between server and client but with different platform APIs, it's recommended to wrap the platform-specific implementations inside a universal API, or use libraries that do this for you. For example, you can use [node-fetch](https://github.com/node-fetch/node-fetch) to use the same fetch API on both server and client.

For browser-only APIs, the common approach is to lazily access them inside client-only lifecycle hooks such as `mounted``onMounted`.

Note that if a third-party library is not written with universal usage in mind, it could be tricky to integrate it into a server-rendered app. You *might* be able to get it working by mocking some of the globals, but it would be hacky and may interfere with the environment detection code of other libraries.

### Cross-Request State Pollution​

In the State Management chapter, we introduced a [simple state management pattern using Reactivity APIs](https://vuejs.org/guide/scaling-up/state-management#simple-state-management-with-reactivity-api). In an SSR context, this pattern requires some additional adjustments.

The pattern declares shared state in a JavaScript module's root scope. This makes them **singletons** - i.e. there is only one instance of the reactive object throughout the entire lifecycle of our application. This works as expected in a pure client-side Vue application, since the modules in our application are initialized fresh for each browser page visit.

However, in an SSR context, the application modules are typically initialized only once on the server, when the server boots up. The same module instances will be reused across multiple server requests, and so will our singleton state objects. If we mutate the shared singleton state with data specific to one user, it can be accidentally leaked to a request from another user. We call this **cross-request state pollution.**

We can technically re-initialize all the JavaScript modules on each request, just like we do in browsers. However, initializing JavaScript modules can be costly, so this would significantly affect server performance.

The recommended solution is to create a new instance of the entire application - including the router and global stores - on each request. Then, instead of directly importing it in our components, we provide the shared state using [app-level provide](https://vuejs.org/guide/components/provide-inject#app-level-provide) and inject it in components that need it:

app.jsjs

```
// (shared between server and client)
import { createSSRApp } from 'vue'
import { createStore } from './store.js'

// called on each request
export function createApp() {
  const app = createSSRApp(/* ... */)
  // create new instance of store per request
  const store = createStore(/* ... */)
  // provide store at the app level
  app.provide('store', store)
  // also expose store for hydration purposes
  return { app, store }
}
```

State Management libraries like Pinia are designed with this in mind. Consult [Pinia's SSR guide](https://pinia.vuejs.org/ssr/) for more details.

### Hydration Mismatch​

If the DOM structure of the pre-rendered HTML does not match the expected output of the client-side app, there will be a hydration mismatch error. Hydration mismatch is most commonly introduced by the following causes:

1. The template contains invalid HTML nesting structure, and the rendered HTML got "corrected" by the browser's native HTML parsing behavior. For example, a common gotcha is that [<div>cannot be placed inside<p>](https://stackoverflow.com/questions/8397852/why-cant-the-p-tag-contain-a-div-tag-inside-it):
  html
  ```
  <p><div>hi</div></p>
  ```
  If we produce this in our server-rendered HTML, the browser will terminate the first `<p>` when `<div>` is encountered and parse it into the following DOM structure:
  html
  ```
  <p></p>
  <div>hi</div>
  <p></p>
  ```
2. The data used during render contains randomly generated values. Since the same application will run twice - once on the server, and once on the client - the random values are not guaranteed to be the same between the two runs. There are two ways to avoid random-value-induced mismatches:
  1. Use `v-if` + `onMounted` to render the part that depends on random values only on the client. Your framework may also have built-in features to make this easier, for example the `<ClientOnly>` component in VitePress.
  2. Use a random number generator library that supports generating with seeds, and guarantee the server run and the client run are using the same seed (e.g. by including the seed in serialized state and retrieving it on the client).
3. The server and the client are in different time zones. Sometimes, we may want to convert a timestamp into the user's local time. However, the timezone during the server run and the timezone during the client run are not always the same, and we may not reliably know the user's timezone during the server run. In such cases, the local time conversion should also be performed as a client-only operation.

When Vue encounters a hydration mismatch, it will attempt to automatically recover and adjust the pre-rendered DOM to match the client-side state. This will lead to some rendering performance loss due to incorrect nodes being discarded and new nodes being mounted, but in most cases, the app should continue to work as expected. That said, it is still best to eliminate hydration mismatches during development.

#### Suppressing Hydration Mismatches​

In Vue 3.5+, it is possible to selectively suppress inevitable hydration mismatches by using the [data-allow-mismatch](https://vuejs.org/api/ssr#data-allow-mismatch) attribute.

### Custom Directives​

Since most custom directives involve direct DOM manipulation, they are ignored during SSR. However, if you want to specify how a custom directive should be rendered (i.e. what attributes it should add to the rendered element), you can use the `getSSRProps` directive hook:

js

```
const myDirective = {
  mounted(el, binding) {
    // client-side implementation:
    // directly update the DOM
    el.id = binding.value
  },
  getSSRProps(binding) {
    // server-side implementation:
    // return the props to be rendered.
    // getSSRProps only receives the directive binding.
    return {
      id: binding.value
    }
  }
}
```

### Teleports​

Teleports require special handling during SSR. If the rendered app contains Teleports, the teleported content will not be part of the rendered string. An easier solution is to conditionally render the Teleport on mount.

If you do need to hydrate teleported content, they are exposed under the `teleports` property of the ssr context object:

js

```
const ctx = {}
const html = await renderToString(app, ctx)

console.log(ctx.teleports) // { '#teleported': 'teleported content' }
```

You need to inject the teleport markup into the correct location in your final page HTML similar to how you need to inject the main app markup.

TIP

Avoid targeting `body` when using Teleports and SSR together - usually, `<body>` will contain other server-rendered content which makes it impossible for Teleports to determine the correct starting location for hydration.

Instead, prefer a dedicated container, e.g. `<div id="teleported"></div>` which contains only teleported content.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/ssr.md)

---

# State Management​

> Vue.js - The Progressive JavaScript Framework

# State Management​

## What is State Management?​

Technically, every Vue component instance already "manages" its own reactive state. Take a simple counter component as an example:

vue

```
<script setup>
import { ref } from 'vue'

// state
const count = ref(0)

// actions
function increment() {
  count.value++
}
</script>

<template>{{ count }}</template>
```

vue

```
<script>
export default {
  // state
  data() {
    return {
      count: 0
    }
  },
  // actions
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>

<template>{{ count }}</template>
```

It is a self-contained unit with the following parts:

- The **state**, the source of truth that drives our app;
- The **view**, a declarative mapping of the **state**;
- The **actions**, the possible ways the state could change in reaction to user inputs from the **view**.

This is a simple representation of the concept of "one-way data flow":

![state flow diagram](https://vuejs.org/assets/state-flow.Cd6No79V.png)

However, the simplicity starts to break down when we have **multiple components that share a common state**:

1. Multiple views may depend on the same piece of state.
2. Actions from different views may need to mutate the same piece of state.

For case one, a possible workaround is by "lifting" the shared state up to a common ancestor component, and then pass it down as props. However, this quickly gets tedious in component trees with deep hierarchies, leading to another problem known as [Prop Drilling](https://vuejs.org/guide/components/provide-inject#prop-drilling).

For case two, we often find ourselves resorting to solutions such as reaching for direct parent / child instances via template refs, or trying to mutate and synchronize multiple copies of the state via emitted events. Both of these patterns are brittle and quickly lead to unmaintainable code.

A simpler and more straightforward solution is to extract the shared state out of the components, and manage it in a global singleton. With this, our component tree becomes a big "view", and any component can access the state or trigger actions, no matter where they are in the tree!

## Simple State Management with Reactivity API​

In Options API, reactive data is declared using the `data()` option. Internally, the object returned by `data()` is made reactive via the [reactive()](https://vuejs.org/api/reactivity-core#reactive) function, which is also available as a public API.

If you have a piece of state that should be shared by multiple instances, you can use [reactive()](https://vuejs.org/api/reactivity-core#reactive) to create a reactive object, and then import it into multiple components:

store.jsjs

```
import { reactive } from 'vue'

export const store = reactive({
  count: 0
})
```

ComponentA.vuevue

```
<script setup>
import { store } from './store.js'
</script>

<template>From A: {{ store.count }}</template>
```

ComponentB.vuevue

```
<script setup>
import { store } from './store.js'
</script>

<template>From B: {{ store.count }}</template>
```

ComponentA.vuevue

```
<script>
import { store } from './store.js'

export default {
  data() {
    return {
      store
    }
  }
}
</script>

<template>From A: {{ store.count }}</template>
```

ComponentB.vuevue

```
<script>
import { store } from './store.js'

export default {
  data() {
    return {
      store
    }
  }
}
</script>

<template>From B: {{ store.count }}</template>
```

Now whenever the `store` object is mutated, both `<ComponentA>` and `<ComponentB>` will update their views automatically - we have a single source of truth now.

However, this also means any component importing `store` can mutate it however they want:

template

```
<template>
  <button @click="store.count++">
    From B: {{ store.count }}
  </button>
</template>
```

While this works in simple cases, global state that can be arbitrarily mutated by any component is not going to be very maintainable in the long run. To ensure the state-mutating logic is centralized like the state itself, it is recommended to define methods on the store with names that express the intention of the actions:

store.jsjs

```
import { reactive } from 'vue'

export const store = reactive({
  count: 0,
  increment() {
    this.count++
  }
})
```

template

```
<template>
  <button @click="store.increment()">
    From B: {{ store.count }}
  </button>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNrNkk1uwyAQha8yYpNEiUzXllPVrtRTeJNSqtLGgGBsVbK4ewdwnT9FWWSTFczwmPc+xMhqa4uhl6xklRdOWQQvsbfPrVadNQ7h1dCqpcYaPp3pYFHwQyteXVxKm0tpM0krnm3IgAqUnd3vUFIFUB1Z8bNOkzoVny+wDTuNcZ1gBI/GSQhzqlQX3/5Gng81pA1t33tEo+FF7JX42bYsT1BaONlRguWqZZMU4C261CWMk3EhTK8RQphm8Twse/BscoUsvdqDkTX3kP3nI6aZwcmdQDUcMPJPabX8TQphtCf0RLqd1csxuqQAJTxtYnEUGtIpAH4pn1Ou17FDScOKhT+QNAVM)

[Try it in the Playground](https://play.vuejs.org/#eNrdU8FqhDAU/JVHLruyi+lZ3FIt9Cu82JilaTWR5CkF8d8bE5O1u1so9FYQzAyTvJnRTKTo+3QcOMlIbpgWPT5WUnS90gjPyr4ll1jAWasOdim9UMum3a20vJWWqxSgkvzTyRt+rocWYVpYFoQm8wRsJh+viHLBcyXtk9No2ALkXd/WyC0CyDfW6RVTOiancQM5ku+x7nUxgUGlOcwxn8Ppu7HJ7udqaqz3SYikOQ5aBgT+OA9slt9kasToFnb5OiAqCU+sFezjVBHvRUimeWdT7JOKrFKAl8VvYatdI6RMDRJhdlPtWdQf5mdQP+SHdtyX/IftlH9pJyS1vcQ2NK8ZivFSiL8BsQmmpMG1s1NU79frYA1k8OD+/I3pUA6+CeNdHg6hmoTMX9pPSnk=)

TIP

Note the click handler uses `store.increment()` with parentheses - this is necessary to call the method with the proper `this` context since it's not a component method.

Although here we are using a single reactive object as a store, you can also share reactive state created using other [Reactivity APIs](https://vuejs.org/api/reactivity-core) such as `ref()` or `computed()`, or even return global state from a [Composable](https://vuejs.org/guide/reusability/composables):

js

```
import { ref } from 'vue'

// global state, created in module scope
const globalCount = ref(1)

export function useCount() {
  // local state, created per-component
  const localCount = ref(1)

  return {
    globalCount,
    localCount
  }
}
```

The fact that Vue's reactivity system is decoupled from the component model makes it extremely flexible.

## SSR Considerations​

If you are building an application that leverages [Server-Side Rendering (SSR)](https://vuejs.org/guide/scaling-up/ssr), the above pattern can lead to issues due to the store being a singleton shared across multiple requests. This is discussed in [more details](https://vuejs.org/guide/scaling-up/ssr#cross-request-state-pollution) in the SSR guide.

## Pinia​

While our hand-rolled state management solution will suffice in simple scenarios, there are many more things to consider in large-scale production applications:

- Stronger conventions for team collaboration
- Integrating with the Vue DevTools, including timeline, in-component inspection, and time-travel debugging
- Hot Module Replacement
- Server-Side Rendering support

[Pinia](https://pinia.vuejs.org) is a state management library that implements all of the above. It is maintained by the Vue core team, and works with both Vue 2 and Vue 3.

Existing users may be familiar with [Vuex](https://vuex.vuejs.org/), the previous official state management library for Vue. With Pinia serving the same role in the ecosystem, Vuex is now in maintenance mode. It still works, but will no longer receive new features. It is recommended to use Pinia for new applications.

Pinia started out as an exploration of what the next iteration of Vuex could look like, incorporating many ideas from core team discussions for Vuex 5. Eventually, we realized that Pinia already implements most of what we wanted in Vuex 5, and decided to make it the new recommendation instead.

Compared to Vuex, Pinia provides a simpler API with less ceremony, offers Composition-API-style APIs, and most importantly, has solid type inference support when used with TypeScript.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/state-management.md)
