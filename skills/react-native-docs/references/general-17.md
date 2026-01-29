# React Native DevTools and more

# React Native DevTools

> React Native DevTools is our modern debugging experience for React Native. Purpose-built from the ground up, it aims to be fundamentally more integrated, correct, and reliable than previous debugging methods.

React Native DevTools is our modern debugging experience for React Native. Purpose-built from the ground up, it aims to be fundamentally more integrated, correct, and reliable than previous debugging methods.

![React Native DevTools opened to the &quot;Welcome&quot; pane](https://reactnative.dev/assets/images/debugging-rndt-welcome-083-9f56f0124de2d2607022330b0ce41d85.jpg)

React Native DevTools is designed for debugging React app concerns, and not to replace native tools. If you want to inspect React Native’s underlying platform layers (for example, while developing a Native Module), please use the debugging tools available in Android Studio and Xcode (see [Debugging Native Code](https://reactnative.dev/docs/debugging-native-code)).

 **💡 Compatibility** — released in 0.76

React Native DevTools supports all React Native apps running Hermes. It replaces the previous Flipper, Experimental Debugger, and Hermes debugger (Chrome) frontends.

It is not possible to set up React Native DevTools with any older versions of React Native.

- **Chrome Browser DevTools — unsupported**
  - Connecting to React Native via `chrome://inspect` is no longer supported. Features may not work correctly, as the latest versions of Chrome DevTools (which are built to match the latest browser capabilities and APIs) have not been tested, and this frontend lacks our customisations. Instead, we ship a supported version with React Native DevTools.
- **Visual Studio Code — unsupported** (pre-existing)
  - Third party extensions such as [Expo Tools](https://github.com/expo/vscode-expo) and [Radon IDE](https://ide.swmansion.com/) may have improved compatibility, but are not directly supported by the React team.

 **💡 Feedback & FAQs**

We want the tooling you use to debug React across all platforms to be reliable, familiar, simple, and cohesive. All the features described on this page are built with these principles in mind, and we also want to offer more capabilities in future.

We are actively iterating on the future of React Native DevTools, and have created a centralized [GitHub discussion](https://github.com/react-native-community/discussions-and-proposals/discussions/819) to keep track of issues, frequently asked questions, and feedback.

## Core features​

React Native DevTools is based on the Chrome DevTools frontend. If you have a web development background, its features should be familiar. As a starting point, we recommend browsing the [Chrome DevTools docs](https://developer.chrome.com/docs/devtools) which contain full guides as well as video resources.

### Console​

![A series of logs React Native DevTools Sources view, alongside a device](https://reactnative.dev/assets/images/debugging-rndt-console-536fe8a6f470b09b93ace9b4f67b4612.jpg)

The Console panel allows you to view and filter messages, evaluate JavaScript, inspect object properties, and more.

[Console features reference | Chrome DevTools](https://developer.chrome.com/docs/devtools/console/reference)

#### Useful tips​

- If your app has a lot of logs, use the filter box or change the log levels that are shown.
- Watch values over time with [Live Expressions](https://developer.chrome.com/docs/devtools/console/live-expressions).
- Persist messages across reloads with [Preserve Logs](https://developer.chrome.com/docs/devtools/console/reference#persist).
- Use Ctrl + L to clear the console view.

### Sources & breakpoints​

![A paused breakpoint in the React Native DevTools Sources view, alongside a device](https://reactnative.dev/assets/images/debugging-rndt-sources-paused-with-device-c7585ed4a3ab596e32c2109efd9c22a0.jpg)

The Sources panel allows you to view the source files in your app and register breakpoints. Use a breakpoint to define a line of code where your app should pause — allowing you to inspect the live state of the program and incrementally step through code.

[Pause your code with breakpoints | Chrome DevTools](https://developer.chrome.com/docs/devtools/javascript/breakpoints)

 tip

#### Mini-guide​

Breakpoints are a fundamental tool in your debugging toolkit!

1. Navigate to a source file using the sidebar or Cmd ⌘+P / Ctrl+P.
2. Click in the line number column next to a line of code to add a breakpoint.
3. Use the navigation controls at the top right to [step through code](https://developer.chrome.com/docs/devtools/javascript/reference#stepping) when paused.

#### Useful tips​

- A "Paused in Debugger" overlay appears when your app is paused. Tap it to resume.
- Pay attention to the right-hand panels when on a breakpoint, which allow you to inspect the current scope and call stack, and set watch expressions.
- Use a `debugger;` statement to quickly set a breakpoint from your text editor. This will reach the device immediately via Fast Refresh.
- There are multiple kinds of breakpoints! For example, [Conditional Breakpoints and Logpoints](https://developer.chrome.com/docs/devtools/javascript/breakpoints#overview).

### NetworkSince 0.83​

![A network request in the React Native DevTools Network panel](https://reactnative.dev/assets/images/debugging-rndt-network-462cd5e39a5525592501627bb0087747.jpg)

The Network panel allows you to view and inspect the network requests made by your app. Logged requests provide detailed metadata such as timings and headers sent/received, as well as response previews.

Network requests are recorded automatically when DevTools is open. We support most features from Chrome, with some exceptions. See more below.

 **💡 Network event coverage, Expo support**

**Which network events are captured?**

Today, we record all network calls through `fetch()`, `XMLHttpRequest`, and `<Image>` — with support for custom networking libraries, such as Expo Fetch, coming later.

**Expo Network differences**

Because of this, apps using Expo will continue to see the "Expo Network" panel — a separate implementation by the Expo framework which will log these additional request sources but has slightly reduced features.

- Coverage for Expo-specific network events.
- No request initiator support.
- No Performance panel integration.

We're working with Expo to integrate Expo Fetch and third party networking libraries with our new Network inspection pipeline in future releases.

**Unimplemented features**

At launch, these are the features we don't yet support in React Native:

- WebSocket events
- Network response mocking
- Simulated network throttling

 **💡 Response previews buffer size**

If you are inspecting a large volume of response data, please note that response previews are cached in an on-device buffer with a maximum size of 100MB. This means we may evict response previews (but not metadata) if the cache becomes too large, oldest request first.

#### Useful tips​

- Use the Initiator tab to see the call stack of where a network request was initiated in your app.
- Network events will also be shown in the Network track in the Performance panel.

### PerformanceSince 0.83​

![A performance trace in the React Native DevTools Performance panel](https://reactnative.dev/assets/images/debugging-rndt-performance-084166527768b90dbb936b240707bdcb.jpg)

Performance tracing allows you to record a performance session within your app to understand how your JavaScript code is running and what operations took the most time. In React Native, we show JavaScript execution, React Performance tracks, Network events, and custom [User Timings](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/User_timing), rendered in a single performance timeline.

#### Useful tips​

- Use [Annotations](https://developer.chrome.com/docs/devtools/performance/annotations) to label and mark up a performance trace — useful before [downloading and sharing](https://developer.chrome.com/docs/devtools/performance/save-trace) with a teammate.
- Use the [PerformanceObserverAPI](https://reactnative.dev/docs/global-PerformanceObserver) in your app to observe performance events at runtime — useful if you want to capture performance telemetry.

#### Learn more​

- [React Performance tracks](https://react.dev/reference/dev-tools/react-performance-tracks)
- [Performance APIs > User Timings | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/User_timing)
- ["Debug Like a Senior — React Native Performance Panel" | Software Mansion](https://blog.swmansion.com/react-native-debugging-new-performance-panel-in-react-native-0-83-21ca90871f6d)

### Memory​

![Inspecting a heap snapshot in the Memory panel](https://reactnative.dev/assets/images/debugging-rndt-memory-741d3be5a43f872d0d4485d9f71456c8.jpg)

The Memory panel allows you to take a heap snapshot and view the memory usage of your JavaScript code over time.

[Record heap snapshots | Chrome DevTools](https://developer.chrome.com/docs/devtools/memory-problems/heap-snapshots)

#### Useful tips​

- Use Cmd ⌘+F / Ctrl+F to filter for specific objects in the heap.
- Taking an [allocation timeline report](https://developer.chrome.com/docs/devtools/memory-problems/allocation-profiler) can be useful to see memory usage over time as a graph, to identify possible memory leaks.

## React DevTools features​

In the integrated Components and Profiler panels, you'll find all the features of the [React DevTools](https://react.dev/learn/react-developer-tools) browser extension. These work seamlessly in React Native DevTools.

### React Components​

![Selecting and locating elements using the React Components panel](https://reactnative.dev/assets/images/debugging-rndt-react-components-628d33c662dc37b0a7c3c21d840fc63c.gif)

The React Components panel allows you to inspect and update the rendered React component tree.

- Hover or select an element in DevTools to highlight it on the device.
- To locate an element in DevTools, click the top-left "Select element" button, then tap any element in the app.

#### Useful tips​

- Props and state on a component can be viewed and modified at runtime using the right hand panel.
- Components optimized with [React Compiler](https://react.dev/learn/react-compiler) will be annotated with a "Memo ✨" badge.

 tip

#### Protip: Highlight re-renders​

Re-renders can be a significant contributor to performance issues in React apps. DevTools can highlight component re-renders as they happen.

- To enable, click the View Settings (`⚙︎`) icon and check "Highlight updates when components render".

![Location of the &quot;highlight updates&quot; setting, next to a recording of the live render overlay](https://reactnative.dev/assets/images/debugging-rndt-highlight-renders-bc20258bbc79dba4fe1866c227943e37.gif)

### React Profiler​

![A profile rendered as a flame graph](https://reactnative.dev/assets/images/debugging-rndt-react-profiler-df4337af110cbdc1da74837b2beacec2.jpg)

The React Profiler panel allows you to record performance profiles to understand the timing of component renders and React commits.

For more info, see the [original 2018 guide](https://legacy.reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html#reading-performance-data) (note that parts of this may be outdated).

## Reconnecting DevTools​

Occasionally, DevTools might disconnect from the target device. This can happen if:

- The app is closed.
- The app is rebuilt (a new native build is installed).
- The app crashes on the native side.
- The dev server (Metro) is quit.
- A physical device is disconnected.

On disconnect, a dialog will be shown with the message "Debugging connection was closed".

![A reconnect dialog shown when a device is disconnected](https://reactnative.dev/assets/images/debugging-reconnect-menu-fc38b7d074e730cc41346286561f75b8.jpg)

From here, you can either:

- **Dismiss**: Select the close (`×`) icon or click outside the dialog to return to the DevTools UI in the last state before disconnection.
- **Reconnect**: Select "Reconnect DevTools", having addressed the reason for disconnection.

Is this page useful?

---

# React Native Gradle Plugin

> This guide describes how to configure the React Native Gradle Plugin (often referred as RNGP), when building your React Native application for Android.

This guide describes how to configure the **React Native Gradle Plugin** (often referred as RNGP), when building your React Native application for Android.

## Using the plugin​

The React Native Gradle Plugin is distributed as a separate NPM package which is installed automatically with `react-native`.

The plugin is **already configured** for new projects created using `npx react-native init`. You don't need to do any extra steps to install it if you created your app with this command.

If you're integrating React Native into an existing project, please refer to [the corresponding page](https://reactnative.dev/docs/next/integration-with-existing-apps#configuring-gradle): it contains specific instructions on how to install the plugin.

## Configuring the plugin​

By default, the plugin will work **out of the box** with sensible defaults. You should refer to this guide and customize the behavior only if you need it.

To configure the plugin you can modify the `react` block, inside your `android/app/build.gradle`:

 groovy

```
apply plugin: "com.facebook.react"/** * This is the configuration block to customize your React Native Android app. * By default you don't need to apply any configuration, just uncomment the lines you need. */react {  // Custom configuration goes here.}
```

Each configuration key is described below:

### root​

This is the root folder of your React Native project, i.e. where the `package.json` file lives. Default is `..`. You can customize it as follows:

 groovy

```
root = file("../")
```

### reactNativeDir​

This is the folder where the `react-native` package lives. Default is `../node_modules/react-native`.
If you're in a monorepo or using a different package manager, you can use adjust `reactNativeDir` to your setup.

You can customize it as follows:

 groovy

```
reactNativeDir = file("../node_modules/react-native")
```

### codegenDir​

This is the folder where the `react-native-codegen` package lives. Default is `../node_modules/react-native-codegen`.
If you're in a monorepo or using a different package manager, you can adjust `codegenDir` to your setup.

You can customize it as follows:

 groovy

```
codegenDir = file("../node_modules/@react-native/codegen")
```

### cliFile​

This is the entrypoint file for the React Native CLI. Default is `../node_modules/react-native/cli.js`.
The entrypoint file is needed as the plugin needs to invoke the CLI for bundling and creating your app.

If you're in a monorepo or using a different package manager, you can adjust `cliFile` to your setup.
You can customize it as follows:

 groovy

```
cliFile = file("../node_modules/react-native/cli.js")
```

### debuggableVariants​

This is the list of variants that are debuggable (see [using variants](#using-variants) for more context on variants).

By default the plugin is considering as `debuggableVariants` only `debug`, while `release` is not. If you have other
variants (like `staging`, `lite`, etc.) you'll need to adjust this accordingly.

Variants that are listed as `debuggableVariants` will not come with a shipped bundle, so you'll need Metro to run them.

You can customize it as follows:

 groovy

```
debuggableVariants = ["liteDebug", "prodDebug"]
```

### nodeExecutableAndArgs​

This is the list of node command and arguments that should be invoked for all the scripts. By default is `[node]` but can be customized to add extra flags as follows:

 groovy

```
nodeExecutableAndArgs = ["node"]
```

### bundleCommand​

This is the name of the `bundle` command to be invoked when creating the bundle for your app. That's useful if you're using [RAM Bundles](https://reactnative.dev/docs/0.74/ram-bundles-inline-requires). By default is `bundle` but can be customized to add extra flags as follows:

 groovy

```
bundleCommand = "ram-bundle"
```

### bundleConfig​

This is the path to a configuration file that will be passed to `bundle --config <file>` if provided. Default is empty (no config file will be probided). More information on bundling config files can be found [on the CLI documentation](https://github.com/react-native-community/cli/blob/main/docs/commands.md#bundle). Can be customized as follow:

 groovy

```
bundleConfig = file(../rn-cli.config.js)
```

### bundleAssetName​

This is the name of the bundle file that should be generated. Default is `index.android.bundle`. Can be customized as follow:

 groovy

```
bundleAssetName = "MyApplication.android.bundle"
```

### entryFile​

The entry file used for bundle generation. The default is to search for `index.android.js` or `index.js`. Can be customized as follow:

 groovy

```
entryFile = file("../js/MyApplication.android.js")
```

### extraPackagerArgs​

A list of extra flags that will be passed to the `bundle` command. The list of available flags is in [the CLI documentation](https://github.com/react-native-community/cli/blob/main/docs/commands.md#bundle). Default is empty. Can be customized as follows:

 groovy

```
extraPackagerArgs = []
```

### hermesCommand​

The path to the `hermesc` command (the Hermes Compiler). React Native comes with a version of the Hermes compiler bundled with it, so you generally won't be needing to customize this. The plugin will use the correct compiler for your system by default.

### hermesFlags​

The list of flags to pass to `hermesc`. By default is `["-O", "-output-source-map"]`. You can customize it as follows

 groovy

```
hermesFlags = ["-O", "-output-source-map"]
```

### enableBundleCompression​

Whether the Bundle Asset should be compressed when packaged into a `.apk`, or not.

Disabling compression for the `.bundle` allows it to be directly memory-mapped to RAM, hence improving startup time - at the cost of a larger resulting app size on disk. Please note that the `.apk` download size will be mostly unaffected as the `.apk` files are compressed before downloading

By default this is disabled, and you should not turn it on, unless you're really concerned about disk space for your application.

## Using Flavors & Build Variants​

When building Android apps, you might want to use [custom flavors](https://developer.android.com/studio/build/build-variants#product-flavors) to have different versions of your app starting from the same project.

Please refer to the [official Android guide](https://developer.android.com/studio/build/build-variants) to configure custom build types (like `staging`) or custom flavors (like `full`, `lite`, etc.).
By default new apps are created with two build types (`debug` and `release`) and no custom flavors.

The combination of all the build types and all the flavors generates a set of **build variants**. For instance for `debug`/`staging`/`release` build types and `full`/`lite` you will have 6 build variants: `fullDebug`, `fullStaging`, `fullRelease` and so on.

If you're using custom variants beyond `debug` and `release`, you need to instruct the React Native Gradle Plugin specifying which of your variants are **debuggable** using the [debuggableVariants](#debuggablevariants) configuration as follows:

 diff

```
apply plugin: "com.facebook.react"react {+ debuggableVariants = ["fullStaging", "fullDebug"]}
```

This is necessary because the plugin will skip the JS bundling for all the `debuggableVariants`: you'll need Metro to run them. For example, if you list `fullStaging` in the `debuggableVariants`, you won't be able to publish it to a store as it will be missing the bundle.

## What is the plugin doing under the hood?​

The React Native Gradle Plugin is responsible for configuring your Application build to ship React Native applications to production.
The plugin is also used inside 3rd party libraries, to run the [Codegen](https://github.com/reactwg/react-native-new-architecture/blob/main/docs/codegen.md) used for the New Architecture.

Here is a summary of the plugin responsibilities:

- Add a `createBundle<Variant>JsAndAssets` task for every non debuggable variant, that is responsible of invoking the `bundle`, `hermesc` and `compose-source-map` commands.
- Setting up the proper version of the `com.facebook.react:react-android` and `com.facebook.react:hermes-android` dependency, reading the React Native version from the `package.json` of `react-native`.
- Setting up the proper Maven repositories (Maven Central, Google Maven Repo, JSC local Maven repo, etc.) needed to consume all the necessary Maven Dependencies.
- Setting up the NDK to let you build apps that are using the New Architecture.
- Setting up the `buildConfigFields` so that you can know at runtime if Hermes or the New Architecture are enabled.
- Setting up the Metro DevServer Port as an Android resource so the app knows on which port to connect.
- Invoking the [React Native Codegen](https://github.com/reactwg/react-native-new-architecture/blob/main/docs/codegen.md) if a library or app is using the Codegen for the New Architecture.

Is this page useful?

---

# React Node Object Type

> A React Node is one of the following types:

A React Node is one of the following types:

- Boolean (which is ignored)
- `null` or `undefined` (which is ignored)
- Number
- String
- A React element (result of JSX)
- An array of any of the above, possibly a nested one

Is this page useful?

---

# Rect Object Type

> Rect accepts numeric pixel values to describe how far to extend a rectangular area. These values are added to the original area's size to expand it.

`Rect` accepts numeric pixel values to describe how far to extend a rectangular area. These values are added to the original area's size to expand it.

## Example​

 js

```
{    bottom: 20,    left: null,    right: undefined,    top: 50}
```

## Keys and values​

### bottom​

| Type | Required |
| --- | --- |
| number,null,undefined | No |

### left​

| Type | Required |
| --- | --- |
| number,null,undefined | No |

### right​

| Type | Required |
| --- | --- |
| number,null,undefined | No |

### top​

| Type | Required |
| --- | --- |
| number,null,undefined | No |

## Used by​

- [Image](https://reactnative.dev/docs/image)
- [Pressable](https://reactnative.dev/docs/pressable)
- [Text](https://reactnative.dev/docs/text)
- [TouchableWithoutFeedback](https://reactnative.dev/docs/touchablewithoutfeedback)

Is this page useful?

---

# RefreshControl

> This component is used inside a ScrollView or ListView to add pull to refresh functionality. When the ScrollView is at scrollY: 0, swiping down triggers an onRefresh event.

This component is used inside a ScrollView or ListView to add pull to refresh functionality. When the ScrollView is at `scrollY: 0`, swiping down triggers an `onRefresh` event.

## Example​

  note

`refreshing` is a controlled prop, this is why it needs to be set to `true` in the `onRefresh` function otherwise the refresh indicator will stop immediately.

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### Requiredrefreshing​

Whether the view should be indicating an active refresh.

| Type |
| --- |
| boolean |

---

### colorsAndroid​

The colors (at least one) that will be used to draw the refresh indicator.

| Type |
| --- |
| array ofcolors |

---

### enabledAndroid​

Whether the pull to refresh functionality is enabled.

| Type | Default |
| --- | --- |
| boolean | true |

---

### onRefresh​

Called when the view starts refreshing.

| Type |
| --- |
| function |

---

### progressBackgroundColorAndroid​

The background color of the refresh indicator.

| Type |
| --- |
| color |

---

### progressViewOffset​

Progress view top offset.

| Type | Default |
| --- | --- |
| number | 0 |

---

### sizeAndroid​

Size of the refresh indicator.

| Type | Default |
| --- | --- |
| enum('default','large') | 'default' |

---

### tintColoriOS​

The color of the refresh indicator.

| Type |
| --- |
| color |

---

### titleiOS​

The title displayed under the refresh indicator.

| Type |
| --- |
| string |

---

### titleColoriOS​

The color of the refresh indicator title.

| Type |
| --- |
| color |

Is this page useful?

---

# Releases Overview

> New React Native releases are shipped every two months, usually resulting in six (6) new minors per year.

New React Native releases are shipped **every two months**, usually resulting in six (6) new minors per year.

Below is the schedule and current status of recent and upcoming React Native releases:

| Version | Branch-cut Date | Release Date | Support | Blogpost |
| --- | --- | --- | --- | --- |
| 0.89.x | 2026-11-03 | 2026-12-07 | Future |  |
| 0.88.x | 2026-09-07 | 2026-10-12 | Future |  |
| 0.87.x | 2026-07-06 | 2026-08-10 | Future |  |
| 0.86.x | 2026-05-04 | 2026-06-08 | Future |  |
| 0.85.x | 2026-03-02 | 2026-04-06 | Future |  |
| 0.84.x | 2026-01-05 | 2026-02-09 | Future |  |
| 0.83.x | 2025-11-03 | 2025-12-10 | Active | Details |
| 0.82.x | 2025-09-01 | 2025-10-06 | Active | Details |
| 0.81.x | 2025-07-10 | 2025-08-12 | End of Cycle | Details |
| 0.80.x | 2025-05-07 | 2025-06-12 | Unsupported | Details |
| 0.79.x | 2025-03-04 | 2025-04-08 | Unsupported | Details |
| 0.78.x | 2025-01-15 | 2025-02-19 | Unsupported | Details |
| 0.77.x | 2024-11-26 | 2025-01-21 | Unsupported | Details |

The different support level presented in the table are defined as such:

- **Future**
  - After a new version branch gets cut, creating new Release Candidates to allow the community to test the upcoming version is very important. New RC releases are done at a high pace, as soon as viable.
- **Active**
  - Stable releases in active support receive frequent updates. Latest stable has the highest priority, and at the start of its stable cycle (right after .0 is released) multiple patches will be done as soon as possible to stabilize the version and ensure a good upgrade experience to the community.
- **End of Cycle**
  - A version in this support bracket will receive less patches, unless some important regressions need to be addressed. Once a next version becomes the new latest stable, before the version in EoC moves over into Unsupported one last patch released will be produced with the latest receive pick requests.
- **Unsupported**
  - When a version is in the unsupported stage, no new released are to be expected. Only very important regressions might create exceptions to this rule; it is recommended that codebases using an unsupported version upgrade as soon as possible.

## Commitment to Stability​

In order to support users upgrading React Native versions, we’re committed to maintain the **latest 3 minor series** (e.g. 0.78.x, 0.77.x and 0.76.x when 0.78 is the latest release).

For those releases we’ll be publishing regular updates and bug fixes.

You can read more about our support policy on [the react-native-releases working group](https://github.com/reactwg/react-native-releases/blob/main/docs/support.md).

More information on our versioning, and what we consider a breaking change is available in our [versioning policy](https://reactnative.dev/docs/releases/versioning-policy) page.

Is this page useful?

---

# RootTag

> RootTag is an opaque identifier assigned to the native root view of your React Native surface — i.e. the ReactRootView or RCTRootView instance for Android or iOS respectively. In short, it is a surface identifier.

`RootTag` is an opaque identifier assigned to the native root view of your React Native surface — i.e. the `ReactRootView` or `RCTRootView` instance for Android or iOS respectively. In short, it is a surface identifier.

## When to use a RootTag?​

For most React Native developers, you likely won’t need to deal with `RootTag`s.

`RootTag`s are useful for when an app renders **multiple React Native root views** and you need to handle native API calls differently depending on the surface. An example of this is when an app is using native navigation and each screen is a separate React Native root view.

In native navigation, every React Native root view is rendered in a platform’s navigation view (e.g., `Activity` for Android, `UINavigationViewController` for iOS). By this, you are able to leverage the navigation paradigms of the platform such as native look and feel and navigation transitions. The functionality to interact with the native navigation APIs can be exposed to React Native via a [native module](https://reactnative.dev/docs/next/native-modules-intro).

For example, to update the title bar of a screen, you would call the navigation module’s API `setTitle("Updated Title")`, but it would need to know which screen in the stack to update. A `RootTag` is necessary here to identify the root view and its hosting container.

Another use case for `RootTag` is when your app needs to attribute a certain JavaScript call to native based on its originating root view. A `RootTag` is necessary to differentiate the source of the call from different surfaces.

## How to access the RootTag... if you need it​

In versions 0.65 and below, RootTag is accessed via a [legacy context](https://github.com/facebook/react-native/blob/v0.64.1/Libraries/ReactNative/AppContainer.js#L56). To prepare React Native for Concurrent features coming in React 18 and beyond, we are migrating to the latest [Context API](https://react.dev/reference/react/createContext) via `RootTagContext` in 0.66. Version 0.65 supports both the legacy context and the recommended `RootTagContext` to allow developers time to migrate their call-sites. See the breaking changes summary.

How to access `RootTag` via the `RootTagContext`.

 js

```
import {RootTagContext} from 'react-native';import NativeAnalytics from 'native-analytics';import NativeNavigation from 'native-navigation';function ScreenA() {  const rootTag = useContext(RootTagContext);  const updateTitle = title => {    NativeNavigation.setTitle(rootTag, title);  };  const handleOneEvent = () => {    NativeAnalytics.logEvent(rootTag, 'one_event');  };  // ...}class ScreenB extends React.Component {  static contextType: typeof RootTagContext = RootTagContext;  updateTitle(title) {    NativeNavigation.setTitle(this.context, title);  }  handleOneEvent() {    NativeAnalytics.logEvent(this.context, 'one_event');  }  // ...}
```

Learn more about the Context API for [classes](https://react.dev/reference/react/Component#static-contexttype) and [hooks](https://react.dev/reference/react/useContext) from the React docs.

### Breaking Change in 0.65​

`RootTagContext` was formerly named `unstable_RootTagContext` and changed to `RootTagContext` in 0.65. Please update any usages of `unstable_RootTagContext` in your codebase.

### Breaking Change in 0.66​

The legacy context access to `RootTag` will be removed and replaced by `RootTagContext`. Beginning in 0.65, we encourage developers to proactively migrate `RootTag` accesses to `RootTagContext`.

## Future Plans​

With the new React Native architecture progressing, there will be future iterations to `RootTag`, with the intention to keep the `RootTag` type opaque and prevent thrash in React Native codebases. Please do not rely on the fact that RootTag currently aliases to a number! If your app relies on RootTags, keep an eye on our version change logs, which you can find [here](https://github.com/facebook/react-native/blob/main/CHANGELOG.md).

Is this page useful?
