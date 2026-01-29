# Introduction​ and more

# Introduction​

> Vue.js - The Progressive JavaScript Framework

# Introduction​

You are reading the documentation for Vue 3!

- Vue 2 support has ended on **Dec 31, 2023**. Learn more about [Vue 2 EOL](https://v2.vuejs.org/eol/).
- Upgrading from Vue 2? Check out the [Migration Guide](https://v3-migration.vuejs.org/).

[Learn Vue with video tutorials onVueMastery.com](https://www.vuemastery.com/courses/)

## What is Vue?​

Vue (pronounced /vjuː/, like **view**) is a JavaScript framework for building user interfaces. It builds on top of standard HTML, CSS, and JavaScript and provides a declarative, component-based programming model that helps you efficiently develop user interfaces of any complexity.

Here is a minimal example:

js

```
import { createApp } from 'vue'

createApp({
  data() {
    return {
      count: 0
    }
  }
}).mount('#app')
```

js

```
import { createApp, ref } from 'vue'

createApp({
  setup() {
    return {
      count: ref(0)
    }
  }
}).mount('#app')
```

template

```
<div id="app">
  <button @click="count++">
    Count is: {{ count }}
  </button>
</div>
```

**Result**

The above example demonstrates the two core features of Vue:

- **Declarative Rendering**: Vue extends standard HTML with a template syntax that allows us to declaratively describe HTML output based on JavaScript state.
- **Reactivity**: Vue automatically tracks JavaScript state changes and efficiently updates the DOM when changes happen.

You may already have questions - don't worry. We will cover every little detail in the rest of the documentation. For now, please read along so you can have a high-level understanding of what Vue offers.

Prerequisites

The rest of the documentation assumes basic familiarity with HTML, CSS, and JavaScript. If you are totally new to frontend development, it might not be the best idea to jump right into a framework as your first step - grasp the basics and then come back! You can check your knowledge level with these overviews for [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript), [HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML) and [CSS](https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps) if needed. Prior experience with other frameworks helps, but is not required.

## The Progressive Framework​

Vue is a framework and ecosystem that covers most of the common features needed in frontend development. But the web is extremely diverse - the things we build on the web may vary drastically in form and scale. With that in mind, Vue is designed to be flexible and incrementally adoptable. Depending on your use case, Vue can be used in different ways:

- Enhancing static HTML without a build step
- Embedding as Web Components on any page
- Single-Page Application (SPA)
- Fullstack / Server-Side Rendering (SSR)
- Jamstack / Static Site Generation (SSG)
- Targeting desktop, mobile, WebGL, and even the terminal

If you find these concepts intimidating, don't worry! The tutorial and guide only require basic HTML and JavaScript knowledge, and you should be able to follow along without being an expert in any of these.

If you are an experienced developer interested in how to best integrate Vue into your stack, or you are curious about what these terms mean, we discuss them in more detail in [Ways of Using Vue](https://vuejs.org/guide/extras/ways-of-using-vue).

Despite the flexibility, the core knowledge about how Vue works is shared across all these use cases. Even if you are just a beginner now, the knowledge gained along the way will stay useful as you grow to tackle more ambitious goals in the future. If you are a veteran, you can pick the optimal way to leverage Vue based on the problems you are trying to solve, while retaining the same productivity. This is why we call Vue "The Progressive Framework": it's a framework that can grow with you and adapt to your needs.

## Single-File Components​

In most build-tool-enabled Vue projects, we author Vue components using an HTML-like file format called **Single-File Component** (also known as `*.vue` files, abbreviated as **SFC**). A Vue SFC, as the name suggests, encapsulates the component's logic (JavaScript), template (HTML), and styles (CSS) in a single file. Here's the previous example, written in SFC format:

vue

```
<script>
export default {
  data() {
    return {
      count: 0
    }
  }
}
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

vue

```
<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">Count is: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

SFC is a defining feature of Vue and is the recommended way to author Vue components **if** your use case warrants a build setup. You can learn more about the [how and why of SFC](https://vuejs.org/guide/scaling-up/sfc) in its dedicated section - but for now, just know that Vue will handle all the build tools setup for you.

## API Styles​

Vue components can be authored in two different API styles: **Options API** and **Composition API**.

### Options API​

With Options API, we define a component's logic using an object of options such as `data`, `methods`, and `mounted`. Properties defined by options are exposed on `this` inside functions, which points to the component instance:

vue

```
<script>
export default {
  // Properties returned from data() become reactive state
  // and will be exposed on `this`.
  data() {
    return {
      count: 0
    }
  },

  // Methods are functions that mutate state and trigger updates.
  // They can be bound as event handlers in templates.
  methods: {
    increment() {
      this.count++
    }
  },

  // Lifecycle hooks are called at different stages
  // of a component's lifecycle.
  // This function will be called when the component is mounted.
  mounted() {
    console.log(`The initial count is ${this.count}.`)
  }
}
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNptkMFqxCAQhl9lkB522ZL0HNKlpa/Qo4e1ZpLIGhUdl5bgu9es2eSyIMio833zO7NP56pbRNawNkivHJ25wV9nPUGHvYiaYOYGoK7Bo5CkbgiBBOFy2AkSh2N5APmeojePCkDaaKiBt1KnZUuv3Ky0PppMsyYAjYJgigu0oEGYDsirYUAP0WULhqVrQhptF5qHQhnpcUJD+wyQaSpUd/Xp9NysVY/yT2qE0dprIS/vsds5Mg9mNVbaDofL94jZpUgJXUKBCvAy76ZUXY53CTd5tfX2k7kgnJzOCXIF0P5EImvgQ2olr++cbRE4O3+t6JxvXj0ptXVpye1tvbFY+ge/NJZt)

### Composition API​

With Composition API, we define a component's logic using imported API functions. In SFCs, Composition API is typically used with [<script setup>](https://vuejs.org/api/sfc-script-setup). The `setup` attribute is a hint that makes Vue perform compile-time transforms that allow us to use Composition API with less boilerplate. For example, imports and top-level variables / functions declared in `<script setup>` are directly usable in the template.

Here is the same component, with the exact same template, but using Composition API and `<script setup>` instead:

vue

```
<script setup>
import { ref, onMounted } from 'vue'

// reactive state
const count = ref(0)

// functions that mutate state and trigger updates
function increment() {
  count.value++
}

// lifecycle hooks
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNpNkMFqwzAQRH9lMYU4pNg9Bye09NxbjzrEVda2iLwS0spQjP69a+yYHnRYad7MaOfiw/tqSliciybqYDxDRE7+qsiM3gWGGQJ2r+DoyyVivEOGLrgRDkIdFCmqa1G0ms2EELllVKQdRQa9AHBZ+PLtuEm7RCKVd+ChZRjTQqwctHQHDqbvMUDyd7mKip4AGNIBRyQujzArgtW/mlqb8HRSlLcEazrUv9oiDM49xGGvXgp5uT5his5iZV1f3r4HFHvDprVbaxPhZf4XkKub/CDLaep1T7IhGRhHb6WoTADNT2KWpu/aGv24qGKvrIrr5+Z7hnneQnJu6hURvKl3ryL/ARrVkuI=)

### Which to Choose?​

Both API styles are fully capable of covering common use cases. They are different interfaces powered by the exact same underlying system. In fact, the Options API is implemented on top of the Composition API! The fundamental concepts and knowledge about Vue are shared across the two styles.

The Options API is centered around the concept of a "component instance" (`this` as seen in the example), which typically aligns better with a class-based mental model for users coming from OOP language backgrounds. It is also more beginner-friendly by abstracting away the reactivity details and enforcing code organization via option groups.

The Composition API is centered around declaring reactive state variables directly in a function scope and composing state from multiple functions together to handle complexity. It is more free-form and requires an understanding of how reactivity works in Vue to be used effectively. In return, its flexibility enables more powerful patterns for organizing and reusing logic.

You can learn more about the comparison between the two styles and the potential benefits of Composition API in the [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq).

If you are new to Vue, here's our general recommendation:

- For learning purposes, go with the style that looks easier to understand to you. Again, most of the core concepts are shared between the two styles. You can always pick up the other style later.
- For production use:
  - Go with Options API if you are not using build tools, or plan to use Vue primarily in low-complexity scenarios, e.g. progressive enhancement.
  - Go with Composition API + Single-File Components if you plan to build full applications with Vue.

You don't have to commit to only one style during the learning phase. The rest of the documentation will provide code samples in both styles where applicable, and you can toggle between them at any time using the **API Preference switches** at the top of the left sidebar.

## Still Got Questions?​

Check out our [FAQ](https://vuejs.org/about/faq).

## Pick Your Learning Path​

Different developers have different learning styles. Feel free to pick a learning path that suits your preference - although we do recommend going over all of the content, if possible!

[Try the TutorialFor those who prefer learning things hands-on.](https://vuejs.org/tutorial/)[Read the GuideThe guide walks you through every aspect of the framework in full detail.](https://vuejs.org/guide/quick-start)[Check out the ExamplesExplore examples of core features and common UI tasks.](https://vuejs.org/examples/)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/introduction.md)

---

# Quick Start​

> Vue.js - The Progressive JavaScript Framework

# Quick Start​

## Try Vue Online​

- To quickly get a taste of Vue, you can try it directly in our [Playground](https://play.vuejs.org/#eNo9jcEKwjAMhl/lt5fpQYfXUQfefAMvvRQbddC1pUuHUPrudg4HIcmXjyRZXEM4zYlEJ+T0iEPgXjn6BB8Zhp46WUZWDjCa9f6w9kAkTtH9CRinV4fmRtZ63H20Ztesqiylphqy3R5UYBqD1UyVAPk+9zkvV1CKbCv9poMLiTEfR2/IXpSoXomqZLtti/IFwVtA9A==).
- If you prefer a plain HTML setup without any build steps, you can use this [JSFiddle](https://jsfiddle.net/yyx990803/2ke1ab0z/) as your starting point.
- If you are already familiar with Node.js and the concept of build tools, you can also try a complete build setup right within your browser on [StackBlitz](https://vite.new/vue).
- To get a walkthrough of the recommended setup, watch this interactive [Scrimba](http://scrimba.com/links/vue-quickstart) tutorial that shows you how to run, edit, and deploy your first Vue app.

## Creating a Vue Application​

Prerequisites

- Familiarity with the command line
- Install [Node.js](https://nodejs.org/) version `^20.19.0 || >=22.12.0`

In this section we will introduce how to scaffold a Vue [Single Page Application](https://vuejs.org/guide/extras/ways-of-using-vue#single-page-application-spa) on your local machine. The created project will be using a build setup based on [Vite](https://vitejs.dev) and allow us to use Vue [Single-File Components](https://vuejs.org/guide/scaling-up/sfc) (SFCs).

Make sure you have an up-to-date version of [Node.js](https://nodejs.org/) installed and your current working directory is the one where you intend to create a project. Run the following command in your command line (without the `$` sign):

npmpnpmyarnbunsh

```
$ npm create vue@latest
```

sh

```
$ pnpm create vue@latest
```

sh

```
# For Yarn (v1+)
$ yarn create vue

# For Yarn Modern (v2+)
$ yarn create vue@latest

# For Yarn ^v4.11
$ yarn dlx create-vue@latest
```

sh

```
$ bun create vue@latest
```

This command will install and execute [create-vue](https://github.com/vuejs/create-vue), the official Vue project scaffolding tool. You will be presented with prompts for several optional features such as TypeScript and testing support:

```
✔ Project name: … <your-project-name>
✔ Add TypeScript? … No / Yes
✔ Add JSX Support? … No / Yes
✔ Add Vue Router for Single Page Application development? … No / Yes
✔ Add Pinia for state management? … No / Yes
✔ Add Vitest for Unit testing? … No / Yes
✔ Add an End-to-End Testing Solution? … No / Cypress / Nightwatch / Playwright
✔ Add ESLint for code quality? … No / Yes
✔ Add Prettier for code formatting? … No / Yes
✔ Add Vue DevTools 7 extension for debugging? (experimental) … No / Yes

Scaffolding project in ./<your-project-name>...
Done.
```

If you are unsure about an option, simply choose `No` by hitting enter for now. Once the project is created, follow the instructions to install dependencies and start the dev server:

npmpnpmyarnbunsh

```
$ cd <your-project-name>
$ npm install
$ npm run dev
```

sh

```
$ cd <your-project-name>
$ pnpm install
$ pnpm run dev
```

sh

```
$ cd <your-project-name>
$ yarn
$ yarn dev
```

sh

```
$ cd <your-project-name>
$ bun install
$ bun run dev
```

You should now have your first Vue project running! Note that the example components in the generated project are written using the [Composition API](https://vuejs.org/guide/introduction#composition-api) and `<script setup>`, rather than the [Options API](https://vuejs.org/guide/introduction#options-api). Here are some additional tips:

- The recommended IDE setup is [Visual Studio Code](https://code.visualstudio.com/) + [Vue - Official extension](https://marketplace.visualstudio.com/items?itemName=Vue.volar). If you use other editors, check out the [IDE support section](https://vuejs.org/guide/scaling-up/tooling#ide-support).
- More tooling details, including integration with backend frameworks, are discussed in the [Tooling Guide](https://vuejs.org/guide/scaling-up/tooling).
- To learn more about the underlying build tool Vite, check out the [Vite docs](https://vite.dev).
- If you choose to use TypeScript, check out the [TypeScript Usage Guide](https://vuejs.org/guide/typescript/overview).

When you are ready to ship your app to production, run the following:

npmpnpmyarnbunsh

```
$ npm run build
```

sh

```
$ pnpm run build
```

sh

```
$ yarn build
```

sh

```
$ bun run build
```

This will create a production-ready build of your app in the project's `./dist` directory. Check out the [Production Deployment Guide](https://vuejs.org/guide/best-practices/production-deployment) to learn more about shipping your app to production.

[Next Steps >](#next-steps)

## Using Vue from CDN​

You can use Vue directly from a CDN via a script tag:

html

```
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

Here we are using [unpkg](https://unpkg.com/), but you can also use any CDN that serves npm packages, for example [jsdelivr](https://www.jsdelivr.com/package/npm/vue) or [cdnjs](https://cdnjs.com/libraries/vue). Of course, you can also download this file and serve it yourself.

When using Vue from a CDN, there is no "build step" involved. This makes the setup a lot simpler, and is suitable for enhancing static HTML or integrating with a backend framework. However, you won't be able to use the Single-File Component (SFC) syntax.

### Using the Global Build​

The above link loads the *global build* of Vue, where all top-level APIs are exposed as properties on the global `Vue` object. Here is a full example using the global build:

html

```
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>

<div id="app">{{ message }}</div>

<script>
  const { createApp } = Vue

  createApp({
    data() {
      return {
        message: 'Hello Vue!'
      }
    }
  }).mount('#app')
</script>
```

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/QWJwJLp)

html

```
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>

<div id="app">{{ message }}</div>

<script>
  const { createApp, ref } = Vue

  createApp({
    setup() {
      const message = ref('Hello vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/eYQpQEG)

TIP

Many of the examples for Composition API throughout the guide will be using the `<script setup>` syntax, which requires build tools. If you intend to use Composition API without a build step, consult the usage of the [setup()option](https://vuejs.org/api/composition-api-setup).

### Using the ES Module Build​

Throughout the rest of the documentation, we will be primarily using [ES modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) syntax. Most modern browsers now support ES modules natively, so we can use Vue from a CDN via native ES modules like this:

html

```
<div id="app">{{ message }}</div>

<script type="module">
  import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

  createApp({
    data() {
      return {
        message: 'Hello Vue!'
      }
    }
  }).mount('#app')
</script>
```

html

```
<div id="app">{{ message }}</div>

<script type="module">
  import { createApp, ref } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

Notice that we are using `<script type="module">`, and the imported CDN URL is pointing to the **ES modules build** of Vue instead.

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/VwVYVZO)

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/MWzazEv)

### Enabling Import maps​

In the above example, we are importing from the full CDN URL, but in the rest of the documentation you will see code like this:

js

```
import { createApp } from 'vue'
```

We can teach the browser where to locate the `vue` import by using [Import Maps](https://caniuse.com/import-maps):

html

```
<script type="importmap">
  {
    "imports": {
      "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
    }
  }
</script>

<div id="app">{{ message }}</div>

<script type="module">
  import { createApp } from 'vue'

  createApp({
    data() {
      return {
        message: 'Hello Vue!'
      }
    }
  }).mount('#app')
</script>
```

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/wvQKQyM)

html

```
<script type="importmap">
  {
    "imports": {
      "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
    }
  }
</script>

<div id="app">{{ message }}</div>

<script type="module">
  import { createApp, ref } from 'vue'

  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

[CodePen Demo >](https://codepen.io/vuejs-examples/pen/YzRyRYM)

You can also add entries for other dependencies to the import map - but make sure they point to the ES modules version of the library you intend to use.

Import Maps Browser Support

Import Maps is a relatively new browser feature. Make sure to use a browser within its [support range](https://caniuse.com/import-maps). In particular, it is only supported in Safari 16.4+.

Notes on Production Use

The examples so far are using the development build of Vue - if you intend to use Vue from a CDN in production, make sure to check out the [Production Deployment Guide](https://vuejs.org/guide/best-practices/production-deployment#without-build-tools).

While it is possible to use Vue without a build system, an alternative approach to consider is using [vuejs/petite-vue](https://github.com/vuejs/petite-vue) that could better suit the context where [jquery/jquery](https://github.com/jquery/jquery) (in the past) or [alpinejs/alpine](https://github.com/alpinejs/alpine) (in the present) might be used instead.

### Splitting Up the Modules​

As we dive deeper into the guide, we may need to split our code into separate JavaScript files so that they are easier to manage. For example:

index.htmlhtml

```
<div id="app"></div>

<script type="module">
  import { createApp } from 'vue'
  import MyComponent from './my-component.js'

  createApp(MyComponent).mount('#app')
</script>
```

my-component.jsjs

```
export default {
  data() {
    return { count: 0 }
  },
  template: `<div>Count is: {{ count }}</div>`
}
```

my-component.jsjs

```
import { ref } from 'vue'
export default {
  setup() {
    const count = ref(0)
    return { count }
  },
  template: `<div>Count is: {{ count }}</div>`
}
```

If you directly open the above `index.html` in your browser, you will find that it throws an error because ES modules cannot work over the `file://` protocol, which is the protocol the browser uses when you open a local file.

Due to security reasons, ES modules can only work over the `http://` protocol, which is what the browsers use when opening pages on the web. In order for ES modules to work on our local machine, we need to serve the `index.html` over the `http://` protocol, with a local HTTP server.

To start a local HTTP server, first make sure you have [Node.js](https://nodejs.org/en/) installed, then run `npx serve` from the command line in the same directory where your HTML file is. You can also use any other HTTP server that can serve static files with the correct MIME types.

You may have noticed that the imported component's template is inlined as a JavaScript string. If you are using VS Code, you can install the [es6-string-html](https://marketplace.visualstudio.com/items?itemName=Tobermory.es6-string-html) extension and prefix the strings with a `/*html*/` comment to get syntax highlighting for them.

## Next Steps​

If you skipped the [Introduction](https://vuejs.org/guide/introduction), we strongly recommend reading it before moving on to the rest of the documentation.

[Continue with the GuideThe guide walks you through every aspect of the framework in full detail.](https://vuejs.org/guide/essentials/application)[Try the TutorialFor those who prefer learning things hands-on.](https://vuejs.org/tutorial/)[Check out the ExamplesExplore examples of core features and common UI tasks.](https://vuejs.org/examples/)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/quick-start.md)
