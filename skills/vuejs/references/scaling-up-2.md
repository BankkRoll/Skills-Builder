# Testing​ and more

# Testing​

> Vue.js - The Progressive JavaScript Framework

# Testing​

## Why Test?​

Automated tests help you and your team build complex Vue applications quickly and confidently by preventing regressions and encouraging you to break apart your application into testable functions, modules, classes, and components. As with any application, your new Vue app can break in many ways, and it's important that you can catch these issues and fix them before releasing.

In this guide, we'll cover basic terminology and provide our recommendations on which tools to choose for your Vue 3 application.

There is one Vue-specific section covering composables. See [Testing Composables](#testing-composables) below for more details.

## When to Test​

Start testing early! We recommend you begin writing tests as soon as you can. The longer you wait to add tests to your application, the more dependencies your application will have, and the harder it will be to start.

## Testing Types​

When designing your Vue application's testing strategy, you should leverage the following testing types:

- **Unit**: Checks that inputs to a given function, class, or composable are producing the expected output or side effects.
- **Component**: Checks that your component mounts, renders, can be interacted with, and behaves as expected. These tests import more code than unit tests, are more complex, and require more time to execute.
- **End-to-end**: Checks features that span multiple pages and makes real network requests against your production-built Vue application. These tests often involve standing up a database or other backend.

Each testing type plays a role in your application's testing strategy, and each will protect you against different types of issues.

## Overview​

We will briefly discuss what each of these are, how they can be implemented for Vue applications, and provide some general recommendations.

## Unit Testing​

Unit tests are written to verify that small, isolated units of code are working as expected. A unit test usually covers a single function, class, composable, or module. Unit tests focus on logical correctness and only concern themselves with a small portion of the application's overall functionality. They may mock large parts of your application's environment (e.g. initial state, complex classes, 3rd party modules, and network requests).

In general, unit tests will catch issues with a function's business logic and logical correctness.

Take for example this `increment` function:

helpers.jsjs

```
export function increment(current, max = 10) {
  if (current < max) {
    return current + 1
  }
  return current
}
```

Because it's very self-contained, it'll be easy to invoke the increment function and assert that it returns what it's supposed to, so we'll write a Unit Test.

If any of these assertions fail, it's clear that the issue is contained within the `increment` function.

helpers.spec.jsjs

```
import { increment } from './helpers'

describe('increment', () => {
  test('increments the current number by 1', () => {
    expect(increment(0, 10)).toBe(1)
  })

  test('does not increment the current number over the max', () => {
    expect(increment(10, 10)).toBe(10)
  })

  test('has a default max of 10', () => {
    expect(increment(10)).toBe(10)
  })
})
```

As mentioned previously, unit testing is typically applied to self-contained business logic, components, classes, modules, or functions that do not involve UI rendering, network requests, or other environmental concerns.

These are typically plain JavaScript / TypeScript modules unrelated to Vue. In general, writing unit tests for business logic in Vue applications does not differ significantly from applications using other frameworks.

There are two instances where you DO unit test Vue-specific features:

1. Composables
2. Components

### Composables​

One category of functions specific to Vue applications is [Composables](https://vuejs.org/guide/reusability/composables), which may require special handling during tests. See [Testing Composables](#testing-composables) below for more details.

### Unit Testing Components​

A component can be tested in two ways:

1. Whitebox: Unit Testing
  Tests that are "Whitebox tests" are aware of the implementation details and dependencies of a component. They are focused on **isolating** the component under test. These tests will usually involve mocking some, if not all of your component's children, as well as setting up plugin state and dependencies (e.g. Pinia).
2. Blackbox: Component Testing
  Tests that are "Blackbox tests" are unaware of the implementation details of a component. These tests mock as little as possible to test the integration of your component and the entire system. They usually render all child components and are considered more of an "integration test". See the [Component Testing recommendations](#component-testing) below.

### Recommendation​

- [Vitest](https://vitest.dev/)
  Since the official setup created by `create-vue` is based on [Vite](https://vitejs.dev/), we recommend using a unit testing framework that can leverage the same configuration and transform pipeline directly from Vite. [Vitest](https://vitest.dev/) is a unit testing framework designed specifically for this purpose, created and maintained by Vue / Vite team members. It integrates with Vite-based projects with minimal effort, and is blazing fast.

### Other Options​

- [Jest](https://jestjs.io/) is a popular unit testing framework. However, we only recommend Jest if you have an existing Jest test suite that needs to be migrated over to a Vite-based project, as Vitest offers a more seamless integration and better performance.

## Component Testing​

In Vue applications, components are the main building blocks of the UI. Components are therefore the natural unit of isolation when it comes to validating your application's behavior. From a granularity perspective, component testing sits somewhere above unit testing and can be considered a form of integration testing. Much of your Vue Application should be covered by a component test and we recommend that each Vue component has its own spec file.

Component tests should catch issues relating to your component's props, events, slots that it provides, styles, classes, lifecycle hooks, and more.

Component tests should not mock child components, but instead test the interactions between your component and its children by interacting with the components as a user would. For example, a component test should click on an element like a user would instead of programmatically interacting with the component.

Component tests should focus on the component's public interfaces rather than internal implementation details. For most components, the public interface is limited to: events emitted, props, and slots. When testing, remember to **test what a component does, not how it does it**.

**DO**

- For **Visual** logic: assert correct render output based on inputted props and slots.
- For **Behavioral** logic: assert correct render updates or emitted events in response to user input events.
  In the below example, we demonstrate a Stepper component that has a DOM element labeled "increment" and can be clicked. We pass a prop called `max` that prevents the Stepper from being incremented past `2`, so if we click the button 3 times, the UI should still say `2`.
  We know nothing about the implementation of Stepper, only that the "input" is the `max` prop and the "output" is the state of the DOM as the user will see it.

Vue Test UtilsCypressTesting Libraryjs

```
const valueSelector = '[data-testid=stepper-value]'
const buttonSelector = '[data-testid=increment]'

const wrapper = mount(Stepper, {
  props: {
    max: 1
  }
})

expect(wrapper.find(valueSelector).text()).toContain('0')

await wrapper.find(buttonSelector).trigger('click')

expect(wrapper.find(valueSelector).text()).toContain('1')
```

js

```
const valueSelector = '[data-testid=stepper-value]'
const buttonSelector = '[data-testid=increment]'

mount(Stepper, {
  props: {
    max: 1
  }
})

cy.get(valueSelector)
  .should('be.visible')
  .and('contain.text', '0')
  .get(buttonSelector)
  .click()
  .get(valueSelector)
  .should('contain.text', '1')
```

js

```
const { getByText } = render(Stepper, {
  props: {
    max: 1
  }
})

getByText('0') // Implicit assertion that "0" is within the component

const button = getByRole('button', { name: /increment/i })

// Dispatch a click event to our increment button.
await fireEvent.click(button)

getByText('1')

await fireEvent.click(button)
```

**DON'T**

- Don't assert the private state of a component instance or test the private methods of a component. Testing implementation details makes the tests brittle, as they are more likely to break and require updates when the implementation changes.
  The component's ultimate job is rendering the correct DOM output, so tests focusing on the DOM output provide the same level of correctness assurance (if not more) while being more robust and resilient to change.
  Don't rely exclusively on snapshot tests. Asserting HTML strings does not describe correctness. Write tests with intentionality.
  If a method needs to be tested thoroughly, consider extracting it into a standalone utility function and write a dedicated unit test for it. If it cannot be extracted cleanly, it may be tested as a part of a component, integration, or end-to-end test that covers it.

### Recommendation​

- [Vitest](https://vitest.dev/) for components or composables that render headlessly (e.g. the [useFavicon](https://vueuse.org/core/useFavicon/#usefavicon) function in VueUse). Components and DOM can be tested using [@vue/test-utils](https://github.com/vuejs/test-utils).
- [Cypress Component Testing](https://on.cypress.io/component) for components whose expected behavior depends on properly rendering styles or triggering native DOM events. It can be used with Testing Library via [@testing-library/cypress](https://testing-library.com/docs/cypress-testing-library/intro).

The main differences between Vitest and browser-based runners are speed and execution context. In short, browser-based runners, like Cypress, can catch issues that node-based runners, like Vitest, cannot (e.g. style issues, real native DOM events, cookies, local storage, and network failures), but browser-based runners are *orders of magnitude slower than Vitest* because they do open a browser, compile your stylesheets, and more. Cypress is a browser-based runner that supports component testing. Please read [Vitest's comparison page](https://vitest.dev/guide/comparisons.html#cypress) for the latest information comparing Vitest and Cypress.

### Mounting Libraries​

Component testing often involves mounting the component being tested in isolation, triggering simulated user input events, and asserting on the rendered DOM output. There are dedicated utility libraries that make these tasks simpler.

- [@vue/test-utils](https://github.com/vuejs/test-utils) is the official low-level component testing library that was written to provide users access to Vue specific APIs. It's also the lower-level library `@testing-library/vue` is built on top of.
- [@testing-library/vue](https://github.com/testing-library/vue-testing-library) is a Vue testing library focused on testing components without relying on implementation details. Its guiding principle is that the more tests resemble the way software is used, the more confidence they can provide.

We recommend using `@vue/test-utils` for testing components in applications. `@testing-library/vue` has issues with testing asynchronous component with Suspense, so it should be used with caution.

### Other Options​

- [Nightwatch](https://nightwatchjs.org/) is an E2E test runner with Vue Component Testing support. ([Example Project](https://github.com/nightwatchjs-community/todo-vue))
- [WebdriverIO](https://webdriver.io/docs/component-testing/vue) for cross-browser component testing that relies on native user interaction based on standardized automation. It can also be used with Testing Library.

## E2E Testing​

While unit tests provide developers with some degree of confidence, unit and component tests are limited in their abilities to provide holistic coverage of an application when deployed to production. As a result, end-to-end (E2E) tests provide coverage on what is arguably the most important aspect of an application: what happens when users actually use your applications.

End-to-end tests focus on multi-page application behavior that makes network requests against your production-built Vue application. They often involve standing up a database or other backend and may even be run against a live staging environment.

End-to-end tests will often catch issues with your router, state management library, top-level components (e.g. an App or Layout), public assets, or any request handling. As stated above, they catch critical issues that may be impossible to catch with unit tests or component tests.

End-to-end tests do not import any of your Vue application's code but instead rely completely on testing your application by navigating through entire pages in a real browser.

End-to-end tests validate many of the layers in your application. They can either target your locally built application or even a live Staging environment. Testing against your Staging environment not only includes your frontend code and static server but all associated backend services and infrastructure.

> The more your tests resemble how your software is used, the more confidence they can give you. - [Kent C. Dodds](https://x.com/kentcdodds/status/977018512689455106) - Author of the Testing Library

By testing how user actions impact your application, E2E tests are often the key to higher confidence in whether an application is functioning properly or not.

### Choosing an E2E Testing Solution​

While end-to-end (E2E) testing on the web has gained a negative reputation for unreliable (flaky) tests and slowing down development processes, modern E2E tools have made strides forward to create more reliable, interactive, and useful tests. When choosing an E2E testing framework, the following sections provide some guidance on things to keep in mind when choosing a testing framework for your application.

#### Cross-browser testing​

One of the primary benefits that end-to-end (E2E) testing is known for is its ability to test your application across multiple browsers. While it may seem desirable to have 100% cross-browser coverage, it is important to note that cross browser testing has diminishing returns on a team's resources due to the additional time and machine power required to run them consistently. As a result, it is important to be mindful of this trade-off when choosing the amount of cross-browser testing your application needs.

#### Faster feedback loops​

One of the primary problems with end-to-end (E2E) tests and development is that running the entire suite takes a long time. Typically, this is only done in continuous integration and deployment (CI/CD) pipelines. Modern E2E testing frameworks have helped to solve this by adding features like parallelization, which allows for CI/CD pipelines to often run magnitudes faster than before. In addition, when developing locally, the ability to selectively run a single test for the page you are working on while also providing hot reloading of tests can help boost a developer's workflow and productivity.

#### First-class debugging experience​

While developers have traditionally relied on scanning logs in a terminal window to help determine what went wrong in a test, modern end-to-end (E2E) test frameworks allow developers to leverage tools they are already familiar with, e.g. browser developer tools.

#### Visibility in headless mode​

When end-to-end (E2E) tests are run in continuous integration/deployment pipelines, they are often run in headless browsers (i.e., no visible browser is opened for the user to watch). A critical feature of modern E2E testing frameworks is the ability to see snapshots and/or videos of the application during testing, providing some insight into why errors are happening. Historically, it was tedious to maintain these integrations.

### Recommendation​

- [Playwright](https://playwright.dev/) is a great E2E testing solution that supports Chromium, WebKit, and Firefox. Test on Windows, Linux, and macOS, locally or on CI, headless or headed with native mobile emulation of Google Chrome for Android and Mobile Safari. It has an informative UI, excellent debuggability, built-in assertions, parallelization, traces and is designed to eliminate flaky tests. Support for [Component Testing](https://playwright.dev/docs/test-components) is available, but marked experimental. Playwright is open source and maintained by Microsoft.
- [Cypress](https://www.cypress.io/) has an informative graphical interface, excellent debuggability, built-in assertions, stubs, flake-resistance, and snapshots. As mentioned above, it provides stable support for [Component Testing](https://docs.cypress.io/guides/component-testing/introduction). Cypress supports Chromium-based browsers, Firefox, and Electron. WebKit support is available, but marked experimental. Cypress is MIT-licensed, but some features like parallelization require a subscription to Cypress Cloud.

[Testing SponsorLambdatest is a cloud platform for running E2E, accessibility, and visual regression tests across all major browsers and real devices, with AI assisted test generation!](https://lambdatest.com)

### Other Options​

- [Nightwatch](https://nightwatchjs.org/) is an E2E testing solution based on [Selenium WebDriver](https://www.npmjs.com/package/selenium-webdriver). This gives it the widest browser support range, including native mobile testing. Selenium-based solutions will be slower than Playwright or Cypress.
- [WebdriverIO](https://webdriver.io/) is a test automation framework for web and mobile testing based on the WebDriver protocol.

## Recipes​

### Adding Vitest to a Project​

In a Vite-based Vue project, run:

sh

```
> npm install -D vitest happy-dom @testing-library/vue
```

Next, update the Vite configuration to add the `test` option block:

vite.config.jsjs

```
import { defineConfig } from 'vite'

export default defineConfig({
  // ...
  test: {
    // enable jest-like global test APIs
    globals: true,
    // simulate DOM with happy-dom
    // (requires installing happy-dom as a peer dependency)
    environment: 'happy-dom'
  }
})
```

TIP

If you use TypeScript, add `vitest/globals` to the `types` field in your `tsconfig.json`.

tsconfig.jsonjson

```
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

Then, create a file ending in `*.test.js` in your project. You can place all test files in a test directory in the project root or in test directories next to your source files. Vitest will automatically search for them using the naming convention.

MyComponent.test.jsjs

```
import { render } from '@testing-library/vue'
import MyComponent from './MyComponent.vue'

test('it should work', () => {
  const { getByText } = render(MyComponent, {
    props: {
      /* ... */
    }
  })

  // assert output
  getByText('...')
})
```

Finally, update `package.json` to add the test script and run it:

package.jsonjson

```
{
  // ...
  "scripts": {
    "test": "vitest"
  }
}
```

sh

```
> npm test
```

### Testing Composables​

> This section assumes you have read the [Composables](https://vuejs.org/guide/reusability/composables) section.

When it comes to testing composables, we can divide them into two categories: composables that do not rely on a host component instance, and composables that do.

A composable depends on a host component instance when it uses the following APIs:

- Lifecycle hooks
- Provide / Inject

If a composable only uses Reactivity APIs, then it can be tested by directly invoking it and asserting its returned state/methods:

counter.jsjs

```
import { ref } from 'vue'

export function useCounter() {
  const count = ref(0)
  const increment = () => count.value++

  return {
    count,
    increment
  }
}
```

counter.test.jsjs

```
import { useCounter } from './counter.js'

test('useCounter', () => {
  const { count, increment } = useCounter()
  expect(count.value).toBe(0)

  increment()
  expect(count.value).toBe(1)
})
```

A composable that relies on lifecycle hooks or Provide / Inject needs to be wrapped in a host component to be tested. We can create a helper like the following:

test-utils.jsjs

```
import { createApp } from 'vue'

export function withSetup(composable) {
  let result
  const app = createApp({
    setup() {
      result = composable()
      // suppress missing template warning
      return () => {}
    }
  })
  app.mount(document.createElement('div'))
  // return the result and the app instance
  // for testing provide/unmount
  return [result, app]
}
```

foo.test.jsjs

```
import { withSetup } from './test-utils'
import { useFoo } from './foo'

test('useFoo', () => {
  const [result, app] = withSetup(() => useFoo(123))
  // mock provide for testing injections
  app.provide(...)
  // run assertions
  expect(result.foo.value).toBe(1)
  // trigger onUnmounted hook if needed
  app.unmount()
})
```

For more complex composables, it could also be easier to test it by writing tests against the wrapper component using [Component Testing](#component-testing) techniques.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/testing.md)

---

# Tooling​

> Vue.js - The Progressive JavaScript Framework

# Tooling​

## Try It Online​

You don't need to install anything on your machine to try out Vue SFCs - there are online playgrounds that allow you to do so right in the browser:

- [Vue SFC Playground](https://play.vuejs.org)
  - Always deployed from latest commit
  - Designed for inspecting component compilation results
- [Vue + Vite on StackBlitz](https://vite.new/vue)
  - IDE-like environment running actual Vite dev server in the browser
  - Closest to local setup

It is also recommended to use these online playgrounds to provide reproductions when reporting bugs.

## Project Scaffolding​

### Vite​

[Vite](https://vitejs.dev/) is a lightweight and fast build tool with first-class Vue SFC support. It is created by Evan You, who is also the author of Vue!

To get started with Vite + Vue, simply run:

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
# For Yarn Modern (v2+)
$ yarn create vue@latest

# For Yarn ^v4.11
$ yarn dlx create-vue@latest
```

sh

```
$ bun create vue@latest
```

This command will install and execute [create-vue](https://github.com/vuejs/create-vue), the official Vue project scaffolding tool.

- To learn more about Vite, check out the [Vite docs](https://vitejs.dev).
- To configure Vue-specific behavior in a Vite project, for example passing options to the Vue compiler, check out the docs for [@vitejs/plugin-vue](https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue#readme).

Both online playgrounds mentioned above also support downloading files as a Vite project.

### Vue CLI​

[Vue CLI](https://cli.vuejs.org/) is the official webpack-based toolchain for Vue. It is now in maintenance mode and we recommend starting new projects with Vite unless you rely on specific webpack-only features. Vite will provide superior developer experience in most cases.

For information on migrating from Vue CLI to Vite:

- [Vue CLI -> Vite Migration Guide from VueSchool.io](https://vueschool.io/articles/vuejs-tutorials/how-to-migrate-from-vue-cli-to-vite/)
- [Tools / Plugins that help with auto migration](https://github.com/vitejs/awesome-vite#vue-cli)

### Note on In-Browser Template Compilation​

When using Vue without a build step, component templates are written either directly in the page's HTML or as inlined JavaScript strings. In such cases, Vue needs to ship the template compiler to the browser in order to perform on-the-fly template compilation. On the other hand, the compiler would be unnecessary if we pre-compile the templates with a build step. To reduce client bundle size, Vue provides [different "builds"](https://unpkg.com/browse/vue@3/dist/) optimized for different use cases.

- Build files that start with `vue.runtime.*` are **runtime-only builds**: they do not include the compiler. When using these builds, all templates must be pre-compiled via a build step.
- Build files that do not include `.runtime` are **full builds**: they include the compiler and support compiling templates directly in the browser. However, they will increase the payload by ~14kb.

Our default tooling setups use the runtime-only build since all templates in SFCs are pre-compiled. If, for some reason, you need in-browser template compilation even with a build step, you can do so by configuring the build tool to alias `vue` to `vue/dist/vue.esm-bundler.js` instead.

If you are looking for a lighter-weight alternative for no-build-step usage, check out [petite-vue](https://github.com/vuejs/petite-vue).

## IDE Support​

- The recommended IDE setup is [VS Code](https://code.visualstudio.com/) + the [Vue - Official extension](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar). The extension provides syntax highlighting, TypeScript support, and intellisense for template expressions and component props.
  TIP
  Vue - Official replaces [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur), our previous official VS Code extension for Vue 2. If you have Vetur currently installed, make sure to disable it in Vue 3 projects.
- [WebStorm](https://www.jetbrains.com/webstorm/) also provides great built-in support for Vue SFCs.
- Other IDEs that support the [Language Service Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) can also leverage Volar's core functionalities via LSP:
  - Sublime Text support via [LSP-Volar](https://github.com/sublimelsp/LSP-volar).
  - vim / Neovim support via [coc-volar](https://github.com/yaegassy/coc-volar).
  - emacs support via [lsp-mode](https://emacs-lsp.github.io/lsp-mode/page/lsp-volar/)

## Browser Devtools​

The Vue browser devtools extension allows you to explore a Vue app's component tree, inspect the state of individual components, track state management events, and profile performance.

![devtools screenshot](https://vuejs.org/assets/devtools.FLNVb-AR.png)

- [Documentation](https://devtools.vuejs.org/)
- [Chrome Extension](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
- [Vite Plugin](https://devtools.vuejs.org/guide/vite-plugin)
- [Standalone Electron app](https://devtools.vuejs.org/guide/standalone)

## TypeScript​

Main article: [Using Vue with TypeScript](https://vuejs.org/guide/typescript/overview).

- [Vue - Official extension](https://github.com/vuejs/language-tools) provides type checking for SFCs using `<script lang="ts">` blocks, including template expressions and cross-component props validation.
- Use [vue-tsc](https://github.com/vuejs/language-tools/tree/master/packages/tsc) for performing the same type checking from the command line, or for generating `d.ts` files for SFCs.

## Testing​

Main article: [Testing Guide](https://vuejs.org/guide/scaling-up/testing).

- [Cypress](https://www.cypress.io/) is recommended for E2E tests. It can also be used for component testing for Vue SFCs via the [Cypress Component Test Runner](https://docs.cypress.io/guides/component-testing/introduction).
- [Vitest](https://vitest.dev/) is a test runner created by Vue / Vite team members that focuses on speed. It is specifically designed for Vite-based applications to provide the same instant feedback loop for unit / component testing.
- [Jest](https://jestjs.io/) can be made to work with Vite via [vite-jest](https://github.com/sodatea/vite-jest). However, this is only recommended if you have existing Jest-based test suites that you need to migrate over to a Vite-based setup, as Vitest provides similar functionalities with a much more efficient integration.

## Linting​

The Vue team maintains [eslint-plugin-vue](https://github.com/vuejs/eslint-plugin-vue), an [ESLint](https://eslint.org/) plugin that supports SFC-specific linting rules.

Users previously using Vue CLI may be used to having linters configured via webpack loaders. However when using a Vite-based build setup, our general recommendation is:

1. `npm install -D eslint eslint-plugin-vue`, then follow `eslint-plugin-vue`'s [configuration guide](https://eslint.vuejs.org/user-guide/#usage).
2. Setup ESLint IDE extensions, for example [ESLint for VS Code](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint), so you get linter feedback right in your editor during development. This also avoids unnecessary linting cost when starting the dev server.
3. Run ESLint as part of the production build command, so you get full linter feedback before shipping to production.
4. (Optional) Setup tools like [lint-staged](https://github.com/okonet/lint-staged) to automatically lint modified files on git commit.

## Formatting​

- The [Vue - Official](https://github.com/vuejs/language-tools) VS Code extension provides formatting for Vue SFCs out of the box.
- Alternatively, [Prettier](https://prettier.io/) provides built-in Vue SFC formatting support.

## SFC Custom Block Integrations​

Custom blocks are compiled into imports to the same Vue file with different request queries. It is up to the underlying build tool to handle these import requests.

- If using Vite, a custom Vite plugin should be used to transform matched custom blocks into executable JavaScript. [Example](https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue#example-for-transforming-custom-blocks)
- If using Vue CLI or plain webpack, a webpack loader should be configured to transform the matched blocks. [Example](https://vue-loader.vuejs.org/guide/custom-blocks.html)

## Lower-Level Packages​

### @vue/compiler-sfc​

- [Docs](https://github.com/vuejs/core/tree/main/packages/compiler-sfc)

This package is part of the Vue core monorepo and is always published with the same version as the main `vue` package. It is included as a dependency of the main `vue` package and proxied under `vue/compiler-sfc` so you don't need to install it individually.

The package itself provides lower-level utilities for processing Vue SFCs and is only meant for tooling authors that need to support Vue SFCs in custom tools.

TIP

Always prefer using this package via the `vue/compiler-sfc` deep import since this ensures its version is in sync with the Vue runtime.

### @vitejs/plugin-vue​

- [Docs](https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue)

Official plugin that provides Vue SFC support in Vite.

### vue-loader​

- [Docs](https://vue-loader.vuejs.org/)

The official loader that provides Vue SFC support in webpack. If you are using Vue CLI, also see [docs on modifyingvue-loaderoptions in Vue CLI](https://cli.vuejs.org/guide/webpack.html#modifying-options-of-a-loader).

## Other Online Playgrounds​

- [VueUse Playground](https://play.vueuse.org)
- [Vue + Vite on Repl.it](https://replit.com/@templates/VueJS-with-Vite)
- [Vue on CodeSandbox](https://codesandbox.io/p/devbox/github/codesandbox/sandbox-templates/tree/main/vue-vite)
- [Vue on Codepen](https://codepen.io/pen/editor/vue)
- [Vue on WebComponents.dev](https://webcomponents.dev/create/cevue)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/scaling-up/tooling.md)
