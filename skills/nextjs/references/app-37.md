# How to set up Jest with Next.js and more

# How to set up Jest with Next.js

> Learn how to set up Jest with Next.js for Unit Testing and Snapshot Testing.

[Guides](https://nextjs.org/docs/app/guides)[Testing](https://nextjs.org/docs/app/guides/testing)Jest

# How to set up Jest with Next.js

Last updated  May 7, 2025

Jest and React Testing Library are frequently used together for **Unit Testing** and **Snapshot Testing**. This guide will show you how to set up Jest with Next.js and write your first tests.

> **Good to know:** Since `async` Server Components are new to the React ecosystem, Jest currently does not support them. While you can still run **unit tests** for synchronous Server and Client Components, we recommend using an **E2E tests** for `async` components.

## Quickstart

You can use `create-next-app` with the Next.js [with-jest](https://github.com/vercel/next.js/tree/canary/examples/with-jest) example to quickly get started:

 Terminal

```
npx create-next-app@latest --example with-jest with-jest-app
```

## Manual setup

Since the release of [Next.js 12](https://nextjs.org/blog/next-12), Next.js now has built-in configuration for Jest.

To set up Jest, install `jest` and the following packages as dev dependencies:

 Terminal

```
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
# or
yarn add -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
# or
pnpm install -D jest jest-environment-jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom ts-node @types/jest
```

Generate a basic Jest configuration file by running the following command:

 Terminal

```
npm init jest@latest
# or
yarn create jest@latest
# or
pnpm create jest@latest
```

This will take you through a series of prompts to setup Jest for your project, including automatically creating a `jest.config.ts|js` file.

Update your config file to use `next/jest`. This transformer has all the necessary configuration options for Jest to work with Next.js:

 jest.config.tsJavaScriptTypeScript

```
import type { Config } from 'jest'
import nextJest from 'next/jest.js'

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const config: Config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  // Add more setup options before each test is run
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
export default createJestConfig(config)
```

Under the hood, `next/jest` is automatically configuring Jest for you, including:

- Setting up `transform` using the [Next.js Compiler](https://nextjs.org/docs/architecture/nextjs-compiler).
- Auto mocking stylesheets (`.css`, `.module.css`, and their scss variants), image imports and [next/font](https://nextjs.org/docs/app/api-reference/components/font).
- Loading `.env` (and all variants) into `process.env`.
- Ignoring `node_modules` from test resolving and transforms.
- Ignoring `.next` from test resolving.
- Loading `next.config.js` for flags that enable SWC transforms.

> **Good to know**: To test environment variables directly, load them manually in a separate setup script or in your `jest.config.ts` file. For more information, please see [Test Environment Variables](https://nextjs.org/docs/app/guides/environment-variables#test-environment-variables).

## Optional: Handling Absolute Imports and Module Path Aliases

If your project is using [Module Path Aliases](https://nextjs.org/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases), you will need to configure Jest to resolve the imports by matching the paths option in the `jsconfig.json` file with the `moduleNameMapper` option in the `jest.config.js` file. For example:

 tsconfig.json or jsconfig.json

```
{
  "compilerOptions": {
    "module": "esnext",
    "moduleResolution": "bundler",
    "baseUrl": "./",
    "paths": {
      "@/components/*": ["components/*"]
    }
  }
}
```

 jest.config.js

```
moduleNameMapper: {
  // ...
  '^@/components/(.*)$': '<rootDir>/components/$1',
}
```

## Optional: Extend Jest with custom matchers

`@testing-library/jest-dom` includes a set of convenient [custom matchers](https://github.com/testing-library/jest-dom#custom-matchers) such as `.toBeInTheDocument()` making it easier to write tests. You can import the custom matchers for every test by adding the following option to the Jest configuration file:

 jest.config.tsJavaScriptTypeScript

```
setupFilesAfterEnv: ['<rootDir>/jest.setup.ts']
```

Then, inside `jest.setup`, add the following import:

 jest.setup.tsJavaScriptTypeScript

```
import '@testing-library/jest-dom'
```

> **Good to know:** [extend-expectwas removed inv6.0](https://github.com/testing-library/jest-dom/releases/tag/v6.0.0), so if you are using `@testing-library/jest-dom` before version 6, you will need to import `@testing-library/jest-dom/extend-expect` instead.

If you need to add more setup options before each test, you can add them to the `jest.setup` file above.

## Add a test script topackage.json

Finally, add a Jest `test` script to your `package.json` file:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

`jest --watch` will re-run tests when a file is changed. For more Jest CLI options, please refer to the [Jest Docs](https://jestjs.io/docs/cli#reference).

### Creating your first test

Your project is now ready to run tests. Create a folder called `__tests__` in your project's root directory.

For example, we can add a test to check if the `<Page />` component successfully renders a heading:

app/page.js

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/about">About</Link>
    </div>
  )
}
```

__tests__/page.test.jsx

```
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import Page from '../app/page'

describe('Page', () => {
  it('renders a heading', () => {
    render(<Page />)

    const heading = screen.getByRole('heading', { level: 1 })

    expect(heading).toBeInTheDocument()
  })
})
```

Optionally, add a [snapshot test](https://jestjs.io/docs/snapshot-testing) to keep track of any unexpected changes in your component:

   __tests__/snapshot.js

```
import { render } from '@testing-library/react'
import Page from '../app/page'

it('renders homepage unchanged', () => {
  const { container } = render(<Page />)
  expect(container).toMatchSnapshot()
})
```

## Running your tests

Then, run the following command to run your tests:

 Terminal

```
npm run test
# or
yarn test
# or
pnpm test
```

## Additional Resources

For further reading, you may find these resources helpful:

- [Next.js with Jest example](https://github.com/vercel/next.js/tree/canary/examples/with-jest)
- [Jest Docs](https://jestjs.io/docs/getting-started)
- [React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Playground](https://testing-playground.com/) - use good testing practices to match elements.

Was this helpful?

supported.

---

# How to set up Playwright with Next.js

> Learn how to set up Playwright with Next.js for End-to-End (E2E) Testing.

[Guides](https://nextjs.org/docs/app/guides)[Testing](https://nextjs.org/docs/app/guides/testing)Playwright

# How to set up Playwright with Next.js

Last updated  April 24, 2025

Playwright is a testing framework that lets you automate Chromium, Firefox, and WebKit with a single API. You can use it to write **End-to-End (E2E)** testing. This guide will show you how to set up Playwright with Next.js and write your first tests.

## Quickstart

The fastest way to get started is to use `create-next-app` with the [with-playwright example](https://github.com/vercel/next.js/tree/canary/examples/with-playwright). This will create a Next.js project complete with Playwright configured.

 Terminal

```
npx create-next-app@latest --example with-playwright with-playwright-app
```

## Manual setup

To install Playwright, run the following command:

 Terminal

```
npm init playwright
# or
yarn create playwright
# or
pnpm create playwright
```

This will take you through a series of prompts to setup and configure Playwright for your project, including adding a `playwright.config.ts` file. Please refer to the [Playwright installation guide](https://playwright.dev/docs/intro#installation) for the step-by-step guide.

## Creating your first Playwright E2E test

Create two new Next.js pages:

 app/page.tsx

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/about">About</Link>
    </div>
  )
}
```

app/about/page.tsx

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>About</h1>
      <Link href="/">Home</Link>
    </div>
  )
}
```

Then, add a test to verify that your navigation is working correctly:

 tests/example.spec.ts

```
import { test, expect } from '@playwright/test'

test('should navigate to the about page', async ({ page }) => {
  // Start from the index page (the baseURL is set via the webServer in the playwright.config.ts)
  await page.goto('http://localhost:3000/')
  // Find an element with the text 'About' and click on it
  await page.click('text=About')
  // The new URL should be "/about" (baseURL is used there)
  await expect(page).toHaveURL('http://localhost:3000/about')
  // The new page should contain an h1 with "About"
  await expect(page.locator('h1')).toContainText('About')
})
```

> **Good to know**: You can use `page.goto("/")` instead of `page.goto("http://localhost:3000/")`, if you add ["baseURL": "http://localhost:3000"](https://playwright.dev/docs/api/class-testoptions#test-options-base-url) to the `playwright.config.ts` [configuration file](https://playwright.dev/docs/test-configuration).

### Running your Playwright tests

Playwright will simulate a user navigating your application using three browsers: Chromium, Firefox and Webkit, this requires your Next.js server to be running. We recommend running your tests against your production code to more closely resemble how your application will behave.

Run `npm run build` and `npm run start`, then run `npx playwright test` in another terminal window to run the Playwright tests.

> **Good to know**: Alternatively, you can use the [webServer](https://playwright.dev/docs/test-webserver/) feature to let Playwright start the development server and wait until it's fully available.

### Running Playwright on Continuous Integration (CI)

Playwright will by default run your tests in the [headless mode](https://playwright.dev/docs/ci#running-headed). To install all the Playwright dependencies, run `npx playwright install-deps`.

You can learn more about Playwright and Continuous Integration from these resources:

- [Next.js with Playwright example](https://github.com/vercel/next.js/tree/canary/examples/with-playwright)
- [Playwright on your CI provider](https://playwright.dev/docs/ci)
- [Playwright Discord](https://discord.com/invite/playwright-807756831384403968)

Was this helpful?

supported.

---

# How to set up Vitest with Next.js

> Learn how to set up Vitest with Next.js for Unit Testing.

[Guides](https://nextjs.org/docs/app/guides)[Testing](https://nextjs.org/docs/app/guides/testing)Vitest

# How to set up Vitest with Next.js

Last updated  August 15, 2025

Vitest and React Testing Library are frequently used together for **Unit Testing**. This guide will show you how to setup Vitest with Next.js and write your first tests.

> **Good to know:** Since `async` Server Components are new to the React ecosystem, Vitest currently does not support them. While you can still run **unit tests** for synchronous Server and Client Components, we recommend using **E2E tests** for `async` components.

## Quickstart

You can use `create-next-app` with the Next.js [with-vitest](https://github.com/vercel/next.js/tree/canary/examples/with-vitest) example to quickly get started:

 Terminal

```
npx create-next-app@latest --example with-vitest with-vitest-app
```

## Manual Setup

To manually set up Vitest, install `vitest` and the following packages as dev dependencies:

 Terminal

```
# Using TypeScript
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths
# Using JavaScript
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom
```

Create a `vitest.config.mts|js` file in the root of your project, and add the following options:

 vitest.config.mtsJavaScriptTypeScript

```
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
  },
})
```

For more information on configuring Vitest, please refer to the [Vitest Configuration](https://vitest.dev/config/#configuration) docs.

Then, add a `test` script to your `package.json`:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest"
  }
}
```

When you run `npm run test`, Vitest will **watch** for changes in your project by default.

## Creating your first Vitest Unit Test

Check that everything is working by creating a test to check if the `<Page />` component successfully renders a heading:

 app/page.tsxJavaScriptTypeScript

```
import Link from 'next/link'

export default function Page() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/about">About</Link>
    </div>
  )
}
```

__tests__/page.test.tsxJavaScriptTypeScript

```
import { expect, test } from 'vitest'
import { render, screen } from '@testing-library/react'
import Page from '../app/page'

test('Page', () => {
  render(<Page />)
  expect(screen.getByRole('heading', { level: 1, name: 'Home' })).toBeDefined()
})
```

> **Good to know**: The example above uses the common `__tests__` convention, but test files can also be colocated inside the `app` router.

## Running your tests

Then, run the following command to run your tests:

 Terminal

```
npm run test
# or
yarn test
# or
pnpm test
# or
bun test
```

## Additional Resources

You may find these resources helpful:

- [Next.js with Vitest example](https://github.com/vercel/next.js/tree/canary/examples/with-vitest)
- [Vitest Docs](https://vitest.dev/guide/)
- [React Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)

Was this helpful?

supported.

---

# Testing

> Learn how to set up Next.js with four commonly used testing tools — Cypress, Playwright, Vitest, and Jest.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Testing

# Testing

Last updated  April 24, 2025

In React and Next.js, there are a few different types of tests you can write, each with its own purpose and use cases. This page provides an overview of types and commonly used tools you can use to test your application.

## Types of tests

- **Unit Testing** involves testing individual units (or blocks of code) in isolation. In React, a unit can be a single function, hook, or component.
  - **Component Testing** is a more focused version of unit testing where the primary subject of the tests is React components. This may involve testing how components are rendered, their interaction with props, and their behavior in response to user events.
  - **Integration Testing** involves testing how multiple units work together. This can be a combination of components, hooks, and functions.
- **End-to-End (E2E) Testing** involves testing user flows in an environment that simulates real user scenarios, like the browser. This means testing specific tasks (e.g. signup flow) in a production-like environment.
- **Snapshot Testing** involves capturing the rendered output of a component and saving it to a snapshot file. When tests run, the current rendered output of the component is compared against the saved snapshot. Changes in the snapshot are used to indicate unexpected changes in behavior.

## Async Server Components

Since `async` Server Components are new to the React ecosystem, some tools do not fully support them. In the meantime, we recommend using **End-to-End Testing** over **Unit Testing** for `async` components.

## Guides

See the guides below to learn how to set up Next.js with these commonly used testing tools:

[CypressLearn how to set up Cypress with Next.js for End-to-End (E2E) and Component Testing.](https://nextjs.org/docs/app/guides/testing/cypress)[JestLearn how to set up Jest with Next.js for Unit Testing and Snapshot Testing.](https://nextjs.org/docs/app/guides/testing/jest)[PlaywrightLearn how to set up Playwright with Next.js for End-to-End (E2E) Testing.](https://nextjs.org/docs/app/guides/testing/playwright)[VitestLearn how to set up Vitest with Next.js for Unit Testing.](https://nextjs.org/docs/app/guides/testing/vitest)

Was this helpful?

supported.

---

# How to optimize third

> Optimize the performance of third-party libraries in your application with the `@next/third-parties` package.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Third Party Libraries

# How to optimize third-party libraries

Last updated  October 29, 2025

**@next/third-parties** is a library that provides a collection of components and utilities that improve the performance and developer experience of loading popular third-party libraries in your Next.js application.

All third-party integrations provided by `@next/third-parties` have been optimized for performance and ease of use.

## Getting Started

To get started, install the `@next/third-parties` library:

 Terminal

```
npm install @next/third-parties@latest next@latest
```

`@next/third-parties` is currently an **experimental** library under active development. We recommend installing it with the **latest** or **canary** flags while we work on adding more third-party integrations.

## Google Third-Parties

All supported third-party libraries from Google can be imported from `@next/third-parties/google`.

### Google Tag Manager

The `GoogleTagManager` component can be used to instantiate a [Google Tag Manager](https://developers.google.com/tag-platform/tag-manager) container to your page. By default, it fetches the original inline script after hydration occurs on the page.

To load Google Tag Manager for all routes, include the component directly in your root layout and pass in your GTM container ID:

app/layout.tsxJavaScriptTypeScript

```
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <GoogleTagManager gtmId="GTM-XYZ" />
      <body>{children}</body>
    </html>
  )
}
```

To load Google Tag Manager for a single route, include the component in your page file:

 app/page.js

```
import { GoogleTagManager } from '@next/third-parties/google'

export default function Page() {
  return <GoogleTagManager gtmId="GTM-XYZ" />
}
```

#### Sending Events

The `sendGTMEvent` function can be used to track user interactions on your page by sending events
using the `dataLayer` object. For this function to work, the `<GoogleTagManager />` component must be
included in either a parent layout, page, or component, or directly in the same file.

 app/page.js

```
'use client'

import { sendGTMEvent } from '@next/third-parties/google'

export function EventButton() {
  return (
    <div>
      <button
        onClick={() => sendGTMEvent({ event: 'buttonClicked', value: 'xyz' })}
      >
        Send Event
      </button>
    </div>
  )
}
```

Refer to the Tag Manager [developer
documentation](https://developers.google.com/tag-platform/tag-manager/datalayer) to learn about the
different variables and events that can be passed into the function.

#### Server-side Tagging

If you're using a server-side tag manager and serving `gtm.js` scripts from your tagging server you can
use `gtmScriptUrl` option to specify the URL of the script.

#### Options

Options to pass to the Google Tag Manager. For a full list of options, read the [Google Tag Manager
docs](https://developers.google.com/tag-platform/tag-manager/datalayer).

| Name | Type | Description |
| --- | --- | --- |
| gtmId | Required* | Your GTM container ID. Usually starts withGTM-. |
| gtmScriptUrl | Optional* | GTM script URL. Defaults tohttps://www.googletagmanager.com/gtm.js. |
| dataLayer | Optional | Data layer object to instantiate the container with. |
| dataLayerName | Optional | Name of the data layer. Defaults todataLayer. |
| auth | Optional | Value of authentication parameter (gtm_auth) for environment snippets. |
| preview | Optional | Value of preview parameter (gtm_preview) for environment snippets. |

*`gtmId` can be omitted when `gtmScriptUrl` is provided to support [Google tag gateway for advertisers](https://developers.google.com/tag-platform/tag-manager/gateway/setup-guide?setup=manual).

### Google Analytics

The `GoogleAnalytics` component can be used to include [Google Analytics
4](https://developers.google.com/analytics/devguides/collection/ga4) to your page via the Google tag
(`gtag.js`). By default, it fetches the original scripts after hydration occurs on the page.

> **Recommendation**: If Google Tag Manager is already included in your application, you can
> configure Google Analytics directly using it, rather than including Google Analytics as a separate
> component. Refer to the
> [documentation](https://developers.google.com/analytics/devguides/collection/ga4/tag-options#what-is-gtm)
> to learn more about the differences between Tag Manager and `gtag.js`.

To load Google Analytics for all routes, include the component directly in your root layout and pass
in your measurement ID:

app/layout.tsxJavaScriptTypeScript

```
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XYZ" />
    </html>
  )
}
```

To load Google Analytics for a single route, include the component in your page file:

 app/page.js

```
import { GoogleAnalytics } from '@next/third-parties/google'

export default function Page() {
  return <GoogleAnalytics gaId="G-XYZ" />
}
```

#### Sending Events

The `sendGAEvent` function can be used to measure user interactions on your page by sending events
using the `dataLayer` object. For this function to work, the `<GoogleAnalytics />` component must be
included in either a parent layout, page, or component, or directly in the same file.

 app/page.js

```
'use client'

import { sendGAEvent } from '@next/third-parties/google'

export function EventButton() {
  return (
    <div>
      <button
        onClick={() => sendGAEvent('event', 'buttonClicked', { value: 'xyz' })}
      >
        Send Event
      </button>
    </div>
  )
}
```

Refer to the Google Analytics [developer
documentation](https://developers.google.com/analytics/devguides/collection/ga4/event-parameters) to learn
more about event parameters.

#### Tracking Pageviews

Google Analytics automatically tracks pageviews when the browser history state changes. This means
that client-side navigations between Next.js routes will send pageview data without any configuration.

To ensure that client-side navigations are being measured correctly, verify that the [“Enhanced
Measurement”](https://support.google.com/analytics/answer/9216061#enable_disable) property is
enabled in your Admin panel and the *“Page changes based on browser history events”* checkbox is
selected.

> **Note**: If you decide to manually send pageview events, make sure to disable the default
> pageview measurement to avoid having duplicate data. Refer to the Google Analytics [developer
> documentation](https://developers.google.com/analytics/devguides/collection/ga4/views?client_type=gtag#manual_pageviews)
> to learn more.

#### Options

Options to pass to the `<GoogleAnalytics>` component.

| Name | Type | Description |
| --- | --- | --- |
| gaId | Required | Yourmeasurement ID. Usually starts withG-. |
| dataLayerName | Optional | Name of the data layer. Defaults todataLayer. |
| nonce | Optional | Anonce. |

### Google Maps Embed

The `GoogleMapsEmbed` component can be used to add a [Google Maps
Embed](https://developers.google.com/maps/documentation/embed/embedding-map) to your page. By
default, it uses the `loading` attribute to lazy-load the embed below the fold.

 app/page.js

```
import { GoogleMapsEmbed } from '@next/third-parties/google'

export default function Page() {
  return (
    <GoogleMapsEmbed
      apiKey="XYZ"
      height={200}
      width="100%"
      mode="place"
      q="Brooklyn+Bridge,New+York,NY"
    />
  )
}
```

#### Options

Options to pass to the Google Maps Embed. For a full list of options, read the [Google Map Embed
docs](https://developers.google.com/maps/documentation/embed/embedding-map).

| Name | Type | Description |
| --- | --- | --- |
| apiKey | Required | Your api key. |
| mode | Required | Map mode |
| height | Optional | Height of the embed. Defaults toauto. |
| width | Optional | Width of the embed. Defaults toauto. |
| style | Optional | Pass styles to the iframe. |
| allowfullscreen | Optional | Property to allow certain map parts to go full screen. |
| loading | Optional | Defaults to lazy. Consider changing if you know your embed will be above the fold. |
| q | Optional | Defines map marker location.This may be required depending on the map mode. |
| center | Optional | Defines the center of the map view. |
| zoom | Optional | Sets initial zoom level of the map. |
| maptype | Optional | Defines type of map tiles to load. |
| language | Optional | Defines the language to use for UI elements and for the display of labels on map tiles. |
| region | Optional | Defines the appropriate borders and labels to display, based on geo-political sensitivities. |

### YouTube Embed

The `YouTubeEmbed` component can be used to load and display a YouTube embed. This component loads
faster by using [lite-youtube-embed](https://github.com/paulirish/lite-youtube-embed) under the
hood.

 app/page.js

```
import { YouTubeEmbed } from '@next/third-parties/google'

export default function Page() {
  return <YouTubeEmbed videoid="ogfYd705cRs" height={400} params="controls=0" />
}
```

#### Options

| Name | Type | Description |
| --- | --- | --- |
| videoid | Required | YouTube video id. |
| width | Optional | Width of the video container. Defaults toauto |
| height | Optional | Height of the video container. Defaults toauto |
| playlabel | Optional | A visually hidden label for the play button for accessibility. |
| params | Optional | The video player params definedhere.Params are passed as a query param string.Eg:params="controls=0&start=10&end=30" |
| style | Optional | Used to apply styles to the video container. |

Was this helpful?

supported.

---

# Codemods

> Use codemods to upgrade your Next.js codebase when new features are released.

[Guides](https://nextjs.org/docs/app/guides)[Upgrading](https://nextjs.org/docs/app/guides/upgrading)Codemods

# Codemods

Last updated  December 10, 2025

Codemods are transformations that run on your codebase programmatically. This allows a large number of changes to be programmatically applied without having to manually go through every file.

Next.js provides Codemod transformations to help upgrade your Next.js codebase when an API is updated or deprecated.

## Usage

In your terminal, navigate (`cd`) into your project's folder, then run:

 Terminal

```
npx @next/codemod <transform> <path>
```

Replacing `<transform>` and `<path>` with appropriate values.

- `transform` - name of transform
- `path` - files or directory to transform
- `--dry` Do a dry-run, no code will be edited
- `--print` Prints the changed output for comparison

## Upgrade

Upgrades your Next.js application, automatically running codemods and updating Next.js, React, and React DOM.

 Terminal

```
npx @next/codemod upgrade [revision]
```

### Options

- `revision` (optional): Specify the upgrade type (`patch`, `minor`, `major`), an NPM dist tag (e.g. `latest`, `canary`, `rc`), or an exact version (e.g. `15.0.0`). Defaults to `minor` for stable versions.
- `--verbose`: Show more detailed output during the upgrade process.

For example:

 Terminal

```
# Upgrade to the latest patch (e.g. 16.0.7 -> 16.0.8)
npx @next/codemod upgrade patch

# Upgrade to the latest minor (e.g. 15.3.7 -> 15.4.8). This is the default.
npx @next/codemod upgrade minor

# Upgrade to the latest major (e.g. 15.5.7 -> 16.0.7)
npx @next/codemod upgrade major

# Upgrade to a specific version
npx @next/codemod upgrade 16

# Upgrade to the canary release
npx @next/codemod upgrade canary
```

> **Good to know**:
>
>
>
> - If the target version is the same as or lower than your current version, the command exits without making changes.
> - During the upgrade, you may be prompted to choose which Next.js codemods to apply and run React 19 codemods if upgrading React.

## Codemods

### 16.0

#### Removeexperimental_pprRoute Segment Config from App Router pages and layouts

##### remove-experimental-ppr

 Terminal

```
npx @next/codemod@latest remove-experimental-ppr .
```

This codemod removes the `experimental_ppr` Route Segment Config from App Router pages and layouts.

 app/page.tsx

```
- export const experimental_ppr = true;
```

#### Removeunstable_prefix from stabilized API

##### remove-unstable-prefix

 Terminal

```
npx @next/codemod@latest remove-unstable-prefix .
```

This codemod removes the `unstable_` prefix from stabilized API.

For example:

```
import { unstable_cacheTag as cacheTag } from 'next/cache'

cacheTag()
```

Transforms into:

```
import { cacheTag } from 'next/cache'

cacheTag()
```

#### Migrate from deprecatedmiddlewareconvention toproxy

##### middleware-to-proxy

 Terminal

```
npx @next/codemod@latest middleware-to-proxy .
```

This codemod migrates projects from using the deprecated `middleware` convention to using the `proxy` convention. It:

- Renames `middleware.<extension>` to `proxy.<extension>` (e.g. `middleware.ts` to `proxy.ts`)
- Renames named export `middleware` to `proxy`
- Renames Next.js config property `experimental.middlewarePrefetch` to `experimental.proxyPrefetch`
- Renames Next.js config property `experimental.middlewareClientMaxBodySize` to `experimental.proxyClientMaxBodySize`
- Renames Next.js config property `experimental.externalMiddlewareRewritesResolve` to `experimental.externalProxyRewritesResolve`
- Renames Next.js config property `skipMiddlewareUrlNormalize` to `skipProxyUrlNormalize`

For example:

 middleware.ts

```
import { NextResponse } from 'next/server'

export function middleware() {
  return NextResponse.next()
}
```

Transforms into:

 proxy.ts

```
import { NextResponse } from 'next/server'

export function proxy() {
  return NextResponse.next()
}
```

#### Migrate fromnext lintto ESLint CLI

##### next-lint-to-eslint-cli

 Terminal

```
npx @next/codemod@canary next-lint-to-eslint-cli .
```

This codemod migrates projects from using `next lint` to using the ESLint CLI with your local ESLint config. It:

- Creates an `eslint.config.mjs` file with Next.js recommended configurations
- Updates `package.json` scripts to use `eslint .` instead of `next lint`
- Adds necessary ESLint dependencies to `package.json`
- Preserves existing ESLint configurations when found

For example:

 package.json

```
{
  "scripts": {
    "lint": "next lint"
  }
}
```

Becomes:

 package.json

```
{
  "scripts": {
    "lint": "eslint ."
  }
}
```

And creates:

 eslint.config.mjs

```
import { dirname } from 'path'
import { fileURLToPath } from 'url'
import { FlatCompat } from '@eslint/eslintrc'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname,
})

const eslintConfig = [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  {
    ignores: [
      'node_modules/**',
      '.next/**',
      'out/**',
      'build/**',
      'next-env.d.ts',
    ],
  },
]

export default eslintConfig
```

### 15.0

#### Transform App Router Route Segment Configruntimevalue fromexperimental-edgetoedge

##### app-dir-runtime-config-experimental-edge

> **Note**: This codemod is App Router specific.

 Terminal

```
npx @next/codemod@latest app-dir-runtime-config-experimental-edge .
```

This codemod transforms [Route Segment Configruntime](https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config#runtime) value `experimental-edge` to `edge`.

For example:

```
export const runtime = 'experimental-edge'
```

Transforms into:

```
export const runtime = 'edge'
```

#### Migrate to async Dynamic APIs

APIs that opted into dynamic rendering that previously supported synchronous access are now asynchronous. You can read more about this breaking change in the [upgrade guide](https://nextjs.org/docs/app/guides/upgrading/version-15).

##### next-async-request-api

 Terminal

```
npx @next/codemod@latest next-async-request-api .
```

This codemod will transform dynamic APIs (`cookies()`, `headers()` and `draftMode()` from `next/headers`) that are now asynchronous to be properly awaited or wrapped with `React.use()` if applicable.
When an automatic migration isn't possible, the codemod will either add a typecast (if a TypeScript file) or a comment to inform the user that it needs to be manually reviewed & updated.

For example:

```
import { cookies, headers } from 'next/headers'
const token = cookies().get('token')

function useToken() {
  const token = cookies().get('token')
  return token
}

export default function Page() {
  const name = cookies().get('name')
}

function getHeader() {
  return headers().get('x-foo')
}
```

Transforms into:

```
import { use } from 'react'
import {
  cookies,
  headers,
  type UnsafeUnwrappedCookies,
  type UnsafeUnwrappedHeaders,
} from 'next/headers'
const token = (cookies() as unknown as UnsafeUnwrappedCookies).get('token')

function useToken() {
  const token = use(cookies()).get('token')
  return token
}

export default async function Page() {
  const name = (await cookies()).get('name')
}

function getHeader() {
  return (headers() as unknown as UnsafeUnwrappedHeaders).get('x-foo')
}
```

When we detect property access on the `params` or `searchParams` props in the page / route entries (`page.js`, `layout.js`, `route.js`, or `default.js`) or the `generateMetadata` / `generateViewport` APIs,
it will attempt to transform the callsite from a sync to an async function, and await the property access. If it can't be made async (such as with a Client Component), it will use `React.use` to unwrap the promise .

For example:

```
// page.tsx
export default function Page({
  params,
  searchParams,
}: {
  params: { slug: string }
  searchParams: { [key: string]: string | string[] | undefined }
}) {
  const { value } = searchParams
  if (value === 'foo') {
    // ...
  }
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const { slug } = params
  return {
    title: `My Page - ${slug}`,
  }
}
```

Transforms into:

```
// page.tsx
export default async function Page(props: {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const searchParams = await props.searchParams
  const { value } = searchParams
  if (value === 'foo') {
    // ...
  }
}

export async function generateMetadata(props: {
  params: Promise<{ slug: string }>
}) {
  const params = await props.params
  const { slug } = params
  return {
    title: `My Page - ${slug}`,
  }
}
```

> **Good to know:** When this codemod identifies a spot that might require manual intervention, but we aren't able to determine the exact fix, it will add a comment or typecast to the code to inform the user that it needs to be manually updated. These comments are prefixed with **@next/codemod**, and typecasts are prefixed with `UnsafeUnwrapped`.
> Your build will error until these comments are explicitly removed. [Read more](https://nextjs.org/docs/messages/sync-dynamic-apis).

#### Replacegeoandipproperties ofNextRequestwith@vercel/functions

##### next-request-geo-ip

 Terminal

```
npx @next/codemod@latest next-request-geo-ip .
```

This codemod installs `@vercel/functions` and transforms `geo` and `ip` properties of `NextRequest` with corresponding `@vercel/functions` features.

For example:

```
import type { NextRequest } from 'next/server'

export function GET(req: NextRequest) {
  const { geo, ip } = req
}
```

Transforms into:

```
import type { NextRequest } from 'next/server'
import { geolocation, ipAddress } from '@vercel/functions'

export function GET(req: NextRequest) {
  const geo = geolocation(req)
  const ip = ipAddress(req)
}
```

### 14.0

#### MigrateImageResponseimports

##### next-og-import

 Terminal

```
npx @next/codemod@latest next-og-import .
```

This codemod moves transforms imports from `next/server` to `next/og` for usage of [Dynamic OG Image Generation](https://nextjs.org/docs/app/getting-started/metadata-and-og-images#generated-open-graph-images).

For example:

```
import { ImageResponse } from 'next/server'
```

Transforms into:

```
import { ImageResponse } from 'next/og'
```

#### Useviewportexport

##### metadata-to-viewport-export

 Terminal

```
npx @next/codemod@latest metadata-to-viewport-export .
```

This codemod migrates certain viewport metadata to `viewport` export.

For example:

```
export const metadata = {
  title: 'My App',
  themeColor: 'dark',
  viewport: {
    width: 1,
  },
}
```

Transforms into:

```
export const metadata = {
  title: 'My App',
}

export const viewport = {
  width: 1,
  themeColor: 'dark',
}
```

### 13.2

#### Use Built-in Font

##### built-in-next-font

 Terminal

```
npx @next/codemod@latest built-in-next-font .
```

This codemod uninstalls the `@next/font` package and transforms `@next/font` imports into the built-in `next/font`.

For example:

```
import { Inter } from '@next/font/google'
```

Transforms into:

```
import { Inter } from 'next/font/google'
```

### 13.0

#### Rename Next Image Imports

##### next-image-to-legacy-image

 Terminal

```
npx @next/codemod@latest next-image-to-legacy-image .
```

Safely renames `next/image` imports in existing Next.js 10, 11, or 12 applications to `next/legacy/image` in Next.js 13. Also renames `next/future/image` to `next/image`.

For example:

 pages/index.js

```
import Image1 from 'next/image'
import Image2 from 'next/future/image'

export default function Home() {
  return (
    <div>
      <Image1 src="/test.jpg" width="200" height="300" />
      <Image2 src="/test.png" width="500" height="400" />
    </div>
  )
}
```

Transforms into:

 pages/index.js

```
// 'next/image' becomes 'next/legacy/image'
import Image1 from 'next/legacy/image'
// 'next/future/image' becomes 'next/image'
import Image2 from 'next/image'

export default function Home() {
  return (
    <div>
      <Image1 src="/test.jpg" width="200" height="300" />
      <Image2 src="/test.png" width="500" height="400" />
    </div>
  )
}
```

#### Migrate to the New Image Component

##### next-image-experimental

 Terminal

```
npx @next/codemod@latest next-image-experimental .
```

Dangerously migrates from `next/legacy/image` to the new `next/image` by adding inline styles and removing unused props.

- Removes `layout` prop and adds `style`.
- Removes `objectFit` prop and adds `style`.
- Removes `objectPosition` prop and adds `style`.
- Removes `lazyBoundary` prop.
- Removes `lazyRoot` prop.

#### Remove<a>Tags From Link Components

##### new-link

 Terminal

```
npx @next/codemod@latest new-link .
```

Remove `<a>` tags inside [Link Components](https://nextjs.org/docs/app/api-reference/components/link).

For example:

```
<Link href="/about">
  <a>About</a>
</Link>
// transforms into
<Link href="/about">
  About
</Link>

<Link href="/about">
  <a onClick={() => console.log('clicked')}>About</a>
</Link>
// transforms into
<Link href="/about" onClick={() => console.log('clicked')}>
  About
</Link>
```

### 11

#### Migrate from CRA

##### cra-to-next

 Terminal

```
npx @next/codemod cra-to-next
```

Migrates a Create React App project to Next.js; creating a Pages Router and necessary config to match behavior. Client-side only rendering is leveraged initially to prevent breaking compatibility due to `window` usage during SSR and can be enabled seamlessly to allow the gradual adoption of Next.js specific features.

Please share any feedback related to this transform [in this discussion](https://github.com/vercel/next.js/discussions/25858).

### 10

#### Add React imports

##### add-missing-react-import

 Terminal

```
npx @next/codemod add-missing-react-import
```

Transforms files that do not import `React` to include the import in order for the new [React JSX transform](https://reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html) to work.

For example:

 my-component.js

```
export default class Home extends React.Component {
  render() {
    return <div>Hello World</div>
  }
}
```

Transforms into:

 my-component.js

```
import React from 'react'
export default class Home extends React.Component {
  render() {
    return <div>Hello World</div>
  }
}
```

### 9

#### Transform Anonymous Components into Named Components

##### name-default-component

 Terminal

```
npx @next/codemod name-default-component
```

**Versions 9 and above.**

Transforms anonymous components into named components to make sure they work with [Fast Refresh](https://nextjs.org/blog/next-9-4#fast-refresh).

For example:

 my-component.js

```
export default function () {
  return <div>Hello World</div>
}
```

Transforms into:

 my-component.js

```
export default function MyComponent() {
  return <div>Hello World</div>
}
```

The component will have a camel-cased name based on the name of the file, and it also works with arrow functions.

### 8

> **Note**: Built-in AMP support and this codemod have been removed in Next.js 16.

#### Transform AMP HOC into page config

##### withamp-to-config

 Terminal

```
npx @next/codemod withamp-to-config
```

Transforms the `withAmp` HOC into Next.js 9 page configuration.

For example:

```
// Before
import { withAmp } from 'next/amp'

function Home() {
  return <h1>My AMP Page</h1>
}

export default withAmp(Home)
```

```
// After
export default function Home() {
  return <h1>My AMP Page</h1>
}

export const config = {
  amp: true,
}
```

### 6

#### UsewithRouter

##### url-to-withrouter

 Terminal

```
npx @next/codemod url-to-withrouter
```

Transforms the deprecated automatically injected `url` property on top level pages to using `withRouter` and the `router` property it injects. Read more here: [https://nextjs.org/docs/messages/url-deprecated](https://nextjs.org/docs/messages/url-deprecated)

For example:

 From

```
import React from 'react'
export default class extends React.Component {
  render() {
    const { pathname } = this.props.url
    return <div>Current pathname: {pathname}</div>
  }
}
```

 To

```
import React from 'react'
import { withRouter } from 'next/router'
export default withRouter(
  class extends React.Component {
    render() {
      const { pathname } = this.props.router
      return <div>Current pathname: {pathname}</div>
    }
  }
)
```

This is one case. All the cases that are transformed (and tested) can be found in the [__testfixtures__directory](https://github.com/vercel/next.js/tree/canary/packages/next-codemod/transforms/__testfixtures__/url-to-withrouter).

Was this helpful?

supported.

---

# How to upgrade to version 14

> Upgrade your Next.js Application from Version 13 to 14.

[Guides](https://nextjs.org/docs/app/guides)[Upgrading](https://nextjs.org/docs/app/guides/upgrading)Version 14

# How to upgrade to version 14

Last updated  April 22, 2025

## Upgrading from 13 to 14

To update to Next.js version 14, run the following command using your preferred package manager:

 Terminal

```
npm i next@next-14 react@18 react-dom@18 && npm i eslint-config-next@next-14 -D
```

 Terminal

```
yarn add next@next-14 react@18 react-dom@18 && yarn add eslint-config-next@next-14 -D
```

 Terminal

```
pnpm i next@next-14 react@18 react-dom@18 && pnpm i eslint-config-next@next-14 -D
```

 Terminal

```
bun add next@next-14 react@18 react-dom@18 && bun add eslint-config-next@next-14 -D
```

> **Good to know:** If you are using TypeScript, ensure you also upgrade `@types/react` and `@types/react-dom` to their latest versions.

### v14 Summary

- The minimum Node.js version has been bumped from 16.14 to 18.17, since 16.x has reached end-of-life.
- The `next export` command has been removed in favor of `output: 'export'` config. Please see the [docs](https://nextjs.org/docs/app/guides/static-exports) for more information.
- The `next/server` import for `ImageResponse` was renamed to `next/og`. A [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#next-og-import) to safely and automatically rename your imports.
- The `@next/font` package has been fully removed in favor of the built-in `next/font`. A [codemod is available](https://nextjs.org/docs/app/guides/upgrading/codemods#built-in-next-font) to safely and automatically rename your imports.
- The WASM target for `next-swc` has been removed.

Was this helpful?

supported.
