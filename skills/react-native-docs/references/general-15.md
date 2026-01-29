# Optimizing FlatList Configuration and more

# Optimizing FlatList Configuration

> Terms

## Terms​

- **VirtualizedList:** The component behind `FlatList` (React Native's implementation of the [Virtual List](https://bvaughn.github.io/react-virtualized/#/components/List) concept.)
- **Memory consumption:** How much information about your list is being stored in memory, which could lead to an app crash.
- **Responsiveness:** Application ability to respond to interactions. Low responsiveness, for instance, is when you touch on a component and it waits a bit to respond, instead of responding immediately as expected.
- **Blank areas:** When `VirtualizedList` can't render your items fast enough, you may enter a part of your list with non-rendered components that appear as blank space.
- **Viewport:** The visible area of content that is rendered to pixels.
- **Window:** The area in which items should be mounted, which is generally much larger than the viewport.

## Props​

Here are a list of props that can help to improve `FlatList` performance:

### removeClippedSubviews​

| Type | Default |
| --- | --- |
| Boolean | trueon Android, otherwisefalse |

If `true`, views that are outside of the viewport are automatically detached from the native view hierarchy.

**Pros:** This reduces time spent on the main thread, and thus reduces the risk of dropped frames, by excluding views outside of the viewport from the native rendering and drawing traversals.

**Cons:** Be aware that this implementation can have bugs, such as missing content (mainly observed on iOS), especially if you are doing complex things with transforms and/or absolute positioning. Also note this does not save significant memory because the views are not deallocated, only detached.

### maxToRenderPerBatch​

| Type | Default |
| --- | --- |
| Number | 10 |

It is a `VirtualizedList` prop that can be passed through `FlatList`. This controls the amount of items rendered per batch, which is the next chunk of items rendered on every scroll.

**Pros:** Setting a bigger number means less visual blank areas when scrolling (increases the fill rate).

**Cons:** More items per batch means longer periods of JavaScript execution potentially blocking other event processing, like presses, hurting responsiveness.

### updateCellsBatchingPeriod​

| Type | Default |
| --- | --- |
| Number | 50 |

While `maxToRenderPerBatch` tells the amount of items rendered per batch, setting `updateCellsBatchingPeriod` tells your `VirtualizedList` the delay in milliseconds between batch renders (how frequently your component will be rendering the windowed items).

**Pros:** Combining this prop with `maxToRenderPerBatch` gives you the power to, for example, render more items in a less frequent batch, or less items in a more frequent batch.

**Cons:** Less frequent batches may cause blank areas, More frequent batches may cause responsiveness issues.

### initialNumToRender​

| Type | Default |
| --- | --- |
| Number | 10 |

The initial amount of items to render.

**Pros:** Define precise number of items that would cover the screen for every device. This can be a big performance boost for the initial render.

**Cons:** Setting a low `initialNumToRender` may cause blank areas, especially if it's too small to cover the viewport on initial render.

### windowSize​

| Type | Default |
| --- | --- |
| Number | 21 |

The number passed here is a measurement unit where 1 is equivalent to your viewport height. The default value is 21 (10 viewports above, 10 below, and one in between).

**Pros:** Bigger `windowSize` will result in less chance of seeing blank space while scrolling. On the other hand, smaller `windowSize` will result in fewer items mounted simultaneously, saving memory.

**Cons:** For a bigger `windowSize`, you will have more memory consumption. For a lower `windowSize`, you will have a bigger chance of seeing blank areas.

## List items​

Below are some tips about list item components. They are the core of your list, so they need to be fast.

### Use basic components​

The more complex your components are, the slower they will render. Try to avoid a lot of logic and nesting in your list items. If you are reusing this list item component a lot in your app, create a component only for your big lists and make them with as little logic and nesting as possible.

### Use light components​

The heavier your components are, the slower they render. Avoid heavy images (use a cropped version or thumbnail for list items, as small as possible). Talk to your design team, use as little effects and interactions and information as possible in your list. Show them in your item's detail.

### Usememo()​

`React.memo()` creates a memoized component that will be re-rendered only when the props passed to the component change. We can use this function to optimize the components in the FlatList.

 tsx

```
import React, {memo} from 'react';import {View, Text} from 'react-native';const MyListItem = memo(  ({title}: {title: string}) => (    <View>      <Text>{title}</Text>    </View>  ),  (prevProps, nextProps) => {    return prevProps.title === nextProps.title;  },);export default MyListItem;
```

In this example, we have determined that MyListItem should be re-rendered only when the title changes. We passed the comparison function as the second argument to React.memo() so that the component is re-rendered only when the specified prop is changed. If the comparison function returns true, the component will not be re-rendered.

### Use cached optimized images​

You can use the community packages (such as [@d11/react-native-fast-image](https://github.com/ds-horizon/react-native-fast-image) from [Dream11](https://github.com/ds-horizon)) for more performant images. Every image in your list is a `new Image()` instance. The faster it reaches the `loaded` hook, the faster your JavaScript thread will be free again.

### UsegetItemLayout​

If all your list item components have the same height (or width, for a horizontal list), providing the [getItemLayout](https://reactnative.dev/docs/flatlist#getitemlayout) prop removes the need for your `FlatList` to manage async layout calculations. This is a very desirable optimization technique.

If your components have dynamic size and you really need performance, consider asking your design team if they may think of a redesign in order to perform better.

### UsekeyExtractororkey​

You can set the [keyExtractor](https://reactnative.dev/docs/flatlist#keyextractor) to your `FlatList` component. This prop is used for caching and as the React `key` to track item re-ordering.

You can also use a `key` prop in your item component.

### Avoid anonymous function onrenderItem​

For functional components, move the `renderItem` function outside of the returned JSX. Also, ensure that it is wrapped in a `useCallback` hook to prevent it from being recreated each render.

For class components, move the `renderItem` function outside of the render function, so it won't recreate itself each time the render function is called.

 tsx

```
const renderItem = useCallback(({item}) => (   <View key={item.key}>      <Text>{item.title}</Text>   </View> ), []);return (  // ...  <FlatList data={items} renderItem={renderItem} />;  // ...);
```

Is this page useful?

---

# Optimizing JavaScript loading

> Parsing and running JavaScript code requires memory and time. Because of this, as your app grows, it's often useful to delay loading code until it's needed for the first time. React Native comes with some standard optimizations that are on by default, and there are techniques you can adopt in your own code to help React load your app more efficiently. There are also some advanced automatic optimizations (with their own tradeoffs) that are suitable for very large apps.

Parsing and running JavaScript code requires memory and time. Because of this, as your app grows, it's often useful to delay loading code until it's needed for the first time. React Native comes with some standard optimizations that are on by default, and there are techniques you can adopt in your own code to help React load your app more efficiently. There are also some advanced automatic optimizations (with their own tradeoffs) that are suitable for very large apps.

## Recommended: Use Hermes​

Hermes is the default engine for new React Native apps, and is highly optimized for efficient code loading. In release builds, JavaScript code is fully compiled to bytecode ahead of time. Bytecode is loaded to memory on-demand and does not need to be parsed like plain JavaScript does.

 info

Read more about using Hermes in React Native [here](https://reactnative.dev/docs/hermes).

## Recommended: Lazy-load large components​

If a component with a lot of code/dependencies is not likely to be used when initially rendering your app, you can use React's [lazy](https://react.dev/reference/react/lazy) API to defer loading its code until it's rendered for the first time. Typically, you should consider lazy-loading screen-level components in your app, so that adding new screens to your app does not increase its startup time.

 info

Read more about [lazy-loading components with Suspense](https://react.dev/reference/react/lazy#suspense-for-code-splitting), including code examples, in React's documentation.

### Tip: Avoid module side effects​

Lazy-loading components can change the behavior of your app if your component modules (or their dependencies) have *side effects*, such as modifying global variables or subscribing to events outside of a component. Most modules in React apps should not have any side effects.

 SideEffects.tsx

```
import Logger from './utils/Logger';//  🚩 🚩 🚩 Side effect! This must be executed before React can even begin to// render the SplashScreen component, and can unexpectedly break code elsewhere// in your app if you later decide to lazy-load SplashScreen.global.logger = new Logger();export function SplashScreen() {  // ...}
```

## Advanced: Callrequireinline​

Sometimes you may want to defer loading some code until you use it for the first time, without using `lazy` or an asynchronous `import()`. You can do this by using the [require()](https://metrobundler.dev/docs/module-api/#require) function where you would otherwise use a static `import` at the top of the file.

 VeryExpensive.tsx

```
import {Component} from 'react';import {Text} from 'react-native';// ... import some very expensive modulesexport default function VeryExpensive() {  // ... lots and lots of rendering logic  return <Text>Very Expensive Component</Text>;}
```

 Optimized.tsx

```
import {useCallback, useState} from 'react';import {TouchableOpacity, View, Text} from 'react-native';// Usually we would write a static import:// import VeryExpensive from './VeryExpensive';let VeryExpensive = null;export default function Optimize() {  const [needsExpensive, setNeedsExpensive] = useState(false);  const didPress = useCallback(() => {    if (VeryExpensive == null) {      VeryExpensive = require('./VeryExpensive').default;    }    setNeedsExpensive(true);  }, []);  return (    <View style={{marginTop: 20}}>      <TouchableOpacity onPress={didPress}>        <Text>Load</Text>      </TouchableOpacity>      {needsExpensive ? <VeryExpensive /> : null}    </View>  );}
```

## Advanced: Automatically inlinerequirecalls​

If you use the React Native CLI to build your app, `require` calls (but not `import`s) will automatically be inlined for you, both in your code and inside any third-party packages (`node_modules`) you use.

 tsx

```
import {useCallback, useState} from 'react';import {TouchableOpacity, View, Text} from 'react-native';// This top-level require call will be evaluated lazily as part of the component below.const VeryExpensive = require('./VeryExpensive').default;export default function Optimize() {  const [needsExpensive, setNeedsExpensive] = useState(false);  const didPress = useCallback(() => {    setNeedsExpensive(true);  }, []);  return (    <View style={{marginTop: 20}}>      <TouchableOpacity onPress={didPress}>        <Text>Load</Text>      </TouchableOpacity>      {needsExpensive ? <VeryExpensive /> : null}    </View>  );}
```

 info

Some React Native frameworks disable this behavior. In particular, in Expo projects, `require` calls are not inlined by default. You can enable this optimization by editing your project's Metro config and setting `inlineRequires: true` in [getTransformOptions](https://metrobundler.dev/docs/configuration#gettransformoptions).

### Pitfalls of inlinerequires​

Inlining `require` calls changes the order in which modules are evaluated, and can even cause some modules to *never* be evaluated. This is usually safe to do automatically, because JavaScript modules are often written to be side-effect-free.

If one of your modules does have side effects - for example, if it initializes some logging mechanism, or patches a global API used by the rest of your code - then you might see unexpected behavior or even crashes. In those cases, you may want to exclude certain modules from this optimization, or disable it entirely.

To **disable all automatic inlining ofrequirecalls:**

Update your `metro.config.js` to set the `inlineRequires` transformer option to `false`:

 metro.config.js

```
module.exports = {  transformer: {    async getTransformOptions() {      return {        transform: {          inlineRequires: false,        },      };    },  },};
```

To only **exclude certain modules fromrequireinlining:**

There are two relevant transformer options: `inlineRequires.blockList` and `nonInlinedRequires`. See the code snippet for examples of how to use each one.

 metro.config.js

```
module.exports = {  transformer: {    async getTransformOptions() {      return {        transform: {          inlineRequires: {            blockList: {              // require() calls in `DoNotInlineHere.js` will not be inlined.              [require.resolve('./src/DoNotInlineHere.js')]: true,              // require() calls anywhere else will be inlined, unless they              // match any entry nonInlinedRequires (see below).            },          },          nonInlinedRequires: [            // require('react') calls will not be inlined anywhere            'react',          ],        },      };    },  },};
```

See the documentation for [getTransformOptionsin Metro](https://metrobundler.dev/docs/configuration#gettransformoptions) for more details on setting up and fine-tuning your inline `require`s.

## Advanced: Use random access module bundles (non-Hermes)​

 tip

**Not supported whenusing Hermes.** Hermes bytecode is not compatible with the RAM bundle format, and provides the same (or better) performance in all use cases.

Random access module bundles (also known as RAM bundles) work in conjunction with the techniques mentioned above to limit the amount of JavaScript code that needs to be parsed and loaded into memory. Each module is stored as a separate string (or file) which is only parsed when the module needs to be executed.

RAM bundles may be physically split into separate files, or they may use the *indexed* format, consisting of a lookup table of multiple modules in a single file.

On Android enable the RAM format by editing your `android/app/build.gradle` file. Before the line `apply from: "../../node_modules/react-native/react.gradle"` add or amend the `project.ext.react` block:

```
project.ext.react = [  bundleCommand: "ram-bundle",]
```

Use the following lines on Android if you want to use a single indexed file:

```
project.ext.react = [  bundleCommand: "ram-bundle",  extraPackagerArgs: ["--indexed-ram-bundle"]]
```

On iOS, RAM bundles are always indexed ( = single file).

Enable the RAM format in Xcode by editing the build phase "Bundle React Native code and images". Before `../node_modules/react-native/scripts/react-native-xcode.sh` add `export BUNDLE_COMMAND="ram-bundle"`:

```
export BUNDLE_COMMAND="ram-bundle"export NODE_BINARY=node../node_modules/react-native/scripts/react-native-xcode.sh
```

See the documentation for [getTransformOptionsin Metro](https://metrobundler.dev/docs/configuration#gettransformoptions) for more details on setting up and fine-tuning your RAM bundle build.

Is this page useful?

---

# Other Debugging Methods

> This page covers how to use legacy JavaScript debugging methods. If you are getting started with a new React Native or Expo app, we recommend using React Native DevTools.

This page covers how to use legacy JavaScript debugging methods. If you are getting started with a new React Native or Expo app, we recommend using [React Native DevTools](https://reactnative.dev/docs/react-native-devtools).

## Safari Developer Tools (direct JSC debugging)​

You can use Safari to debug the iOS version of your app when using [JavaScriptCore](https://trac.webkit.org/wiki/JavaScriptCore) (JSC) as your app's runtime.

1. **Physical devices only**: Open the Settings app, and navigate to Safari > Advanced, and make sure "Web Inspector" is turned on.
2. On your Mac, open Safari and enable the Develop menu. This can be found under Safari > Settings..., then the Advanced tab, then selecting "Show features for web developers".
3. Find your device under the Develop menu, and select the "JSContext" item from the submenu. This will open Safari's Web Inspector, which includes Console and Sources panels similar to Chrome DevTools.

![Opening Safari Web Inspector](https://reactnative.dev/assets/images/debugging-safari-developer-tools-5aefdee28e230260908d691621c4fa63.jpg)

 tip

While source maps may not be enabled by default, you can follow [this guide](https://blog.nparashuram.com/2019/10/debugging-react-native-ios-apps-with.html) or [video](https://www.youtube.com/watch?v=GrGqIIz51k4) to enable them and set break points at the right places in the source code.

 tip

Every time the app is reloaded, a new JSContext is created. Choosing "Automatically Show Web Inspectors for JSContexts" saves you from having to select the latest JSContext manually.

## Remote JavaScript Debugging (removed)​

 Important

Remote JavaScript Debugging has been removed as of React Native 0.79. See the original [deprecation announcement](https://github.com/react-native-community/discussions-and-proposals/discussions/734).

If you are on an older version of React Native, please go to the docs [for your version](https://reactnative.dev/versions).

![The remote debugger window in Chrome](https://reactnative.dev/assets/images/debugging-chrome-remote-debugger-ddf0ea5593f18b93a26ed3a8ea44e42e.jpg)

Is this page useful?

---

# Out

> React Native is not only for Android and iOS devices - our partners and the community maintain projects that bring React Native to other platforms, such as:

React Native is not only for Android and iOS devices - our partners and the community maintain projects that bring React Native to other platforms, such as:

**From Partners**

- [React Native macOS](https://github.com/microsoft/react-native-macos) - React Native for macOS and Cocoa.
- [React Native Windows](https://github.com/microsoft/react-native-windows) - React Native for Microsoft's Universal Windows Platform (UWP).
- [React Native visionOS](https://github.com/callstack/react-native-visionos) - React Native for Apple's visionOS.

**From Community**

- [React Native tvOS](https://github.com/react-native-tvos/react-native-tvos) - React Native for Apple TV and Android TV devices.
- [React Native Web](https://github.com/necolas/react-native-web) - React Native on the web using React DOM.
- [React Native Skia](https://github.com/react-native-skia/react-native-skia) - React Native using [Skia](https://skia.org/) as a renderer. Currently supports Linux and macOS.

## Creating your own React Native platform​

Right now the process of creating a React Native platform from scratch is not very well documented - one of the goals of the upcoming re-architecture ([Fabric](https://reactnative.dev/blog/2018/06/14/state-of-react-native-2018)) is to make maintaining a platform easier.

### Bundling​

As of React Native 0.57 you can now register your React Native platform with React Native's JavaScript bundler, [Metro](https://metrobundler.dev/). This means you can pass `--platform example` to `npx react-native bundle`, and it will look for JavaScript files with the `.example.js` suffix.

To register your platform with RNPM, your module's name must match one of these patterns:

- `react-native-example` - It will search all top-level modules that start with `react-native-`
- `@org/react-native-example` - It will search for modules that start with `react-native-` under any scope
- `@react-native-example/module` - It will search in all modules under scopes with names starting with `@react-native-`

You must also have an entry in your `package.json` like this:

 json

```
{  "rnpm": {    "haste": {      "providesModuleNodeModules": ["react-native-example"],      "platforms": ["example"]    }  }}
```

`"providesModuleNodeModules"` is an array of modules that will get added to the Haste module search path, and `"platforms"` is an array of platform suffixes that will be added as valid platforms.

Is this page useful?

---

# PanResponder

> PanResponder reconciles several touches into a single gesture. It makes single-touch gestures resilient to extra touches, and can be used to recognize basic multi-touch gestures.

`PanResponder` reconciles several touches into a single gesture. It makes single-touch gestures resilient to extra touches, and can be used to recognize basic multi-touch gestures.

By default, `PanResponder` holds an `InteractionManager` handle to block long-running JS events from interrupting active gestures.

It provides a predictable wrapper of the responder handlers provided by the [gesture responder system](https://reactnative.dev/docs/gesture-responder-system). For each handler, it provides a new `gestureState` object alongside the native event object:

```
onPanResponderMove: (event, gestureState) => {}
```

A native event is a synthetic touch event with form of [PressEvent](https://reactnative.dev/docs/pressevent).

A `gestureState` object has the following:

- `stateID` - ID of the gestureState- persisted as long as there's at least one touch on screen
- `moveX` - the latest screen coordinates of the recently-moved touch
- `moveY` - the latest screen coordinates of the recently-moved touch
- `x0` - the screen coordinates of the responder grant
- `y0` - the screen coordinates of the responder grant
- `dx` - accumulated distance of the gesture since the touch started
- `dy` - accumulated distance of the gesture since the touch started
- `vx` - current velocity of the gesture
- `vy` - current velocity of the gesture
- `numberActiveTouches` - Number of touches currently on screen

## Usage Pattern​

 tsx

```
const ExampleComponent = () => {  const panResponder = React.useRef(    PanResponder.create({      // Ask to be the responder:      onStartShouldSetPanResponder: (evt, gestureState) => true,      onStartShouldSetPanResponderCapture: (evt, gestureState) =>        true,      onMoveShouldSetPanResponder: (evt, gestureState) => true,      onMoveShouldSetPanResponderCapture: (evt, gestureState) =>        true,      onPanResponderGrant: (evt, gestureState) => {        // The gesture has started. Show visual feedback so the user knows        // what is happening!        // gestureState.d{x,y} will be set to zero now      },      onPanResponderMove: (evt, gestureState) => {        // The most recent move distance is gestureState.move{X,Y}        // The accumulated gesture distance since becoming responder is        // gestureState.d{x,y}      },      onPanResponderTerminationRequest: (evt, gestureState) =>        true,      onPanResponderRelease: (evt, gestureState) => {        // The user has released all touches while this view is the        // responder. This typically means a gesture has succeeded      },      onPanResponderTerminate: (evt, gestureState) => {        // Another component has become the responder, so this gesture        // should be cancelled      },      onShouldBlockNativeResponder: (evt, gestureState) => {        // Returns whether this component should block native components from becoming the JS        // responder. Returns true by default. Is currently only supported on android.        return true;      },    }),  ).current;  return <View {...panResponder.panHandlers} />;};
```

## Example​

`PanResponder` works with `Animated` API to help build complex gestures in the UI. The following example contains an animated `View` component which can be dragged freely across the screen

Try the [PanResponder example in RNTester](https://github.com/facebook/react-native/blob/main/packages/rn-tester/js/examples/PanResponder/PanResponderExample.js).

---

# Reference

## Methods​

### create()​

 tsx

```
static create(config: PanResponderCallbacks): PanResponderInstance;
```

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| configRequired | object | Refer below |

The `config` object provides enhanced versions of all of the responder callbacks that provide not only the [PressEvent](https://reactnative.dev/docs/pressevent), but also the `PanResponder` gesture state, by replacing the word `Responder` with `PanResponder` in each of the typical `onResponder*` callbacks. For example, the `config` object would look like:

- `onMoveShouldSetPanResponder: (e, gestureState) => {...}`
- `onMoveShouldSetPanResponderCapture: (e, gestureState) => {...}`
- `onStartShouldSetPanResponder: (e, gestureState) => {...}`
- `onStartShouldSetPanResponderCapture: (e, gestureState) => {...}`
- `onPanResponderReject: (e, gestureState) => {...}`
- `onPanResponderGrant: (e, gestureState) => {...}`
- `onPanResponderStart: (e, gestureState) => {...}`
- `onPanResponderEnd: (e, gestureState) => {...}`
- `onPanResponderRelease: (e, gestureState) => {...}`
- `onPanResponderMove: (e, gestureState) => {...}`
- `onPanResponderTerminate: (e, gestureState) => {...}`
- `onPanResponderTerminationRequest: (e, gestureState) => {...}`
- `onShouldBlockNativeResponder: (e, gestureState) => {...}`

In general, for events that have capture equivalents, we update the gestureState once in the capture phase and can use it in the bubble phase as well.

Be careful with `onStartShould*` callbacks. They only reflect updated `gestureState` for start/end events that bubble/capture to the Node. Once the node is the responder, you can rely on every start/end event being processed by the gesture and `gestureState` being updated accordingly. (numberActiveTouches) may not be totally accurate unless you are the responder.

Is this page useful?

---

# Performance Overview

> A compelling reason to use React Native instead of WebView-based tools is to achieve at least 60 frames per second and provide a native look and feel to your apps. Whenever feasible, we aim for React Native to handle optimizations automatically, allowing you to focus on your app without worrying about performance. However, there are certain areas where we haven't quite reached that level yet, and others where React Native (similar to writing native code directly) cannot determine the best optimization approach for you. In such cases, manual intervention becomes necessary. We strive to deliver buttery-smooth UI performance by default, but there may be instances where that isn't possible.

A compelling reason to use React Native instead of WebView-based tools is to achieve at least 60 frames per second and provide a native look and feel to your apps. Whenever feasible, we aim for React Native to handle optimizations automatically, allowing you to focus on your app without worrying about performance. However, there are certain areas where we haven't quite reached that level yet, and others where React Native (similar to writing native code directly) cannot determine the best optimization approach for you. In such cases, manual intervention becomes necessary. We strive to deliver buttery-smooth UI performance by default, but there may be instances where that isn't possible.

This guide is intended to teach you some basics to help you to [troubleshoot performance issues](https://reactnative.dev/docs/profiling), as well as discuss [common sources of problems and their suggested solutions](https://reactnative.dev/docs/performance#common-sources-of-performance-problems).

## What you need to know about frames​

Your grandparents' generation called movies ["moving pictures"](https://www.youtube.com/watch?v=F1i40rnpOsA) for a reason: realistic motion in video is an illusion created by quickly changing static images at a consistent speed. We refer to each of these images as frames. The number of frames that is displayed each second has a direct impact on how smooth and ultimately life-like a video (or user interface) seems to be. iOS and Android devices display at least 60 frames per second, which gives you and the UI system at most 16.67ms to do all of the work needed to generate the static image (frame) that the user will see on the screen for that interval. If you are unable to do the work necessary to generate that frame within the allotted time slot, then you will "drop a frame" and the UI will appear unresponsive.

Now to confuse the matter a little bit, open up the [Dev Menu](https://reactnative.dev/docs/debugging#opening-the-dev-menu) in your app and toggle `Show Perf Monitor`. You will notice that there are two different frame rates.

![Performance Monitor screenshot](https://reactnative.dev/assets/images/PerfUtil-38a2ddbf1777887d70563a644c72aa64.png)

### JS frame rate (JavaScript thread)​

For most React Native applications, your business logic will run on the JavaScript thread. This is where your React application lives, API calls are made, touch events are processed, and more. Updates to native-backed views are batched and sent over to the native side at the end of each iteration of the event loop, before the frame deadline (if all goes well). If the JavaScript thread is unresponsive for a frame, it will be considered a dropped frame. For example, if you were to set a new state on the root component of a complex application and it resulted in re-rendering computationally expensive component subtrees, it's conceivable that this might take 200ms and result in 12 frames being dropped. Any animations controlled by JavaScript would appear to freeze during that time. If enough frames are dropped, the user will feel it.

An example is responding to touches: if you are doing work across multiple frames on the JavaScript thread, you might notice a delay in responding to `TouchableOpacity`, for example. This is because the JavaScript thread is busy and cannot process the raw touch events sent over from the main thread. As a result, `TouchableOpacity` cannot react to the touch events and command the native view to adjust its opacity.

### UI frame rate (main thread)​

You may have noticed that performance of native stack navigators (such as the [@react-navigation/native-stack](https://reactnavigation.org/docs/native-stack-navigator) provided by React Navigation) is better out of the box than JavaScript-based stack navigators. This is because the transition animations are executed on the native main UI thread, so they are not interrupted by frame drops on the JavaScript thread.

Similarly, you can happily scroll up and down through a `ScrollView` when the JavaScript thread is locked up because the `ScrollView` lives on the main thread. The scroll events are dispatched to the JS thread, but their receipt is not necessary for the scroll to occur.

## Common sources of performance problems​

### Running in development mode (dev=true)​

JavaScript thread performance suffers greatly when running in dev mode. This is unavoidable: a lot more work needs to be done at runtime to provide you with good warnings and error messages. Always make sure to test performance in [release builds](https://reactnative.dev/docs/running-on-device#building-your-app-for-production).

### Usingconsole.logstatements​

When running a bundled app, these statements can cause a big bottleneck in the JavaScript thread. This includes calls from debugging libraries such as [redux-logger](https://github.com/evgenyrodionov/redux-logger), so make sure to remove them before bundling. You can also use this [babel plugin](https://babeljs.io/docs/plugins/transform-remove-console/) that removes all the `console.*` calls. You need to install it first with `npm i babel-plugin-transform-remove-console --save-dev`, and then edit the `.babelrc` file under your project directory like this:

 json

```
{  "env": {    "production": {      "plugins": ["transform-remove-console"]    }  }}
```

This will automatically remove all `console.*` calls in the release (production) versions of your project.

It is recommended to use the plugin even if no `console.*` calls are made in your project. A third party library could also call them.

### FlatListrendering is too slow or scroll performance is bad for large lists​

If your [FlatList](https://reactnative.dev/docs/flatlist) is rendering slowly, be sure that you've implemented [getItemLayout](https://reactnative.dev/docs/flatlist#getitemlayout) to optimize rendering speed by skipping measurement of the rendered items.

There are also other third-party list libraries that are optimized for performance, including [FlashList](https://github.com/shopify/flash-list) and [Legend List](https://github.com/legendapp/legend-list).

### Dropping JS thread FPS because of doing a lot of work on the JavaScript thread at the same time​

"Slow Navigator transitions" is the most common manifestation of this, but there are other times this can happen. Using [InteractionManager](https://reactnative.dev/docs/interactionmanager) can be a good approach, but if the user experience cost is too high to delay work during an animation, then you might want to consider [LayoutAnimation](https://reactnative.dev/docs/layoutanimation).

The [Animated API](https://reactnative.dev/docs/animated) currently calculates each keyframe on-demand on the JavaScript thread unless you [setuseNativeDriver: true](https://reactnative.dev/blog/2017/02/14/using-native-driver-for-animated#how-do-i-use-this-in-my-app), while [LayoutAnimation](https://reactnative.dev/docs/layoutanimation) leverages Core Animation and is unaffected by JS thread and main thread frame drops.

One case for using this is animating in a modal (sliding down from top and fading in a translucent overlay) while initializing and perhaps receiving responses for several network requests, rendering the contents of the modal, and updating the view where the modal was opened from. See the [Animations guide](https://reactnative.dev/docs/animations) for more information about how to use `LayoutAnimation`.

**Caveats:**

- `LayoutAnimation` only works for fire-and-forget animations ("static" animations) -- if it must be interruptible, you will need to use [Animated](https://reactnative.dev/docs/animated).

### Moving a view on the screen (scrolling, translating, rotating) drops UI thread FPS​

This is especially true on Android when you have text with a transparent background positioned on top of an image, or any other situation where alpha compositing would be required to re-draw the view on each frame. You will find that enabling `renderToHardwareTextureAndroid` can help with this significantly. For iOS, `shouldRasterizeIOS` is already enabled by default.

Be careful not to overuse this or your memory usage could go through the roof. Profile your performance and memory usage when using these props. If you don't plan to move a view anymore, turn this property off.

### Animating the size of an image drops UI thread FPS​

On iOS, each time you adjust the width or height of an [Imagecomponent](https://reactnative.dev/docs/image) it is re-cropped and scaled from the original image. This can be very expensive, especially for large images. Instead, use the `transform: [{scale}]` style property to animate the size. An example of when you might do this is when you tap an image and zoom it in to full screen.

### My TouchableX view isn't very responsive​

Sometimes, if we do an action in the same frame that we are adjusting the opacity or highlight of a component that is responding to a touch, we won't see that effect until after the `onPress` function has returned. This may occur if `onPress` sets a state that results in a heavy re-render and a few frames are dropped as a result. A solution to this is to wrap any action inside of your `onPress` handler in `requestAnimationFrame`:

 tsx

```
function handleOnPress() {  requestAnimationFrame(() => {    this.doExpensiveAction();  });}
```

Is this page useful?

---

# PermissionsAndroid

> Project with Native Code Required

### Project with Native Code Required

The following section only applies to projects with native code exposed. If you are using the managed Expo workflow, see the guide on [Permissions](https://docs.expo.dev/guides/permissions/) in the Expo documentation for the appropriate alternative.

`PermissionsAndroid` provides access to Android M's new permissions model. The so-called "normal" permissions are granted by default when the application is installed as long as they appear in `AndroidManifest.xml`. However, "dangerous" permissions require a dialog prompt. You should use this module for those permissions.

On devices before SDK version 23, the permissions are automatically granted if they appear in the manifest, so `check` should always result to `true` and `request` should always resolve to `PermissionsAndroid.RESULTS.GRANTED`.

If a user has previously turned off a permission that you prompt for, the OS will advise your app to show a rationale for needing the permission. The optional `rationale` argument will show a dialog prompt only if necessary - otherwise the normal permission prompt will appear.

### Example​

### Permissions that require prompting the user​

Available as constants under `PermissionsAndroid.PERMISSIONS`:

- `READ_CALENDAR`: 'android.permission.READ_CALENDAR'
- `WRITE_CALENDAR`: 'android.permission.WRITE_CALENDAR'
- `CAMERA`: 'android.permission.CAMERA'
- `READ_CONTACTS`: 'android.permission.READ_CONTACTS'
- `WRITE_CONTACTS`: 'android.permission.WRITE_CONTACTS'
- `GET_ACCOUNTS`: 'android.permission.GET_ACCOUNTS'
- `ACCESS_FINE_LOCATION`: 'android.permission.ACCESS_FINE_LOCATION'
- `ACCESS_COARSE_LOCATION`: 'android.permission.ACCESS_COARSE_LOCATION'
- `ACCESS_BACKGROUND_LOCATION`: 'android.permission.ACCESS_BACKGROUND_LOCATION'
- `RECORD_AUDIO`: 'android.permission.RECORD_AUDIO'
- `READ_PHONE_STATE`: 'android.permission.READ_PHONE_STATE'
- `CALL_PHONE`: 'android.permission.CALL_PHONE'
- `READ_CALL_LOG`: 'android.permission.READ_CALL_LOG'
- `WRITE_CALL_LOG`: 'android.permission.WRITE_CALL_LOG'
- `ADD_VOICEMAIL`: 'com.android.voicemail.permission.ADD_VOICEMAIL'
- `USE_SIP`: 'android.permission.USE_SIP'
- `PROCESS_OUTGOING_CALLS`: 'android.permission.PROCESS_OUTGOING_CALLS'
- `BODY_SENSORS`: 'android.permission.BODY_SENSORS'
- `SEND_SMS`: 'android.permission.SEND_SMS'
- `RECEIVE_SMS`: 'android.permission.RECEIVE_SMS'
- `READ_SMS`: 'android.permission.READ_SMS'
- `RECEIVE_WAP_PUSH`: 'android.permission.RECEIVE_WAP_PUSH'
- `RECEIVE_MMS`: 'android.permission.RECEIVE_MMS'
- `READ_EXTERNAL_STORAGE`: 'android.permission.READ_EXTERNAL_STORAGE'
- `WRITE_EXTERNAL_STORAGE`: 'android.permission.WRITE_EXTERNAL_STORAGE'
- `BLUETOOTH_CONNECT`: 'android.permission.BLUETOOTH_CONNECT'
- `BLUETOOTH_SCAN`: 'android.permission.BLUETOOTH_SCAN'
- `BLUETOOTH_ADVERTISE`: 'android.permission.BLUETOOTH_ADVERTISE'
- `ACCESS_MEDIA_LOCATION`: 'android.permission.ACCESS_MEDIA_LOCATION'
- `ACCEPT_HANDOVER`: 'android.permission.ACCEPT_HANDOVER'
- `ACTIVITY_RECOGNITION`: 'android.permission.ACTIVITY_RECOGNITION'
- `ANSWER_PHONE_CALLS`: 'android.permission.ANSWER_PHONE_CALLS'
- `READ_PHONE_NUMBERS`: 'android.permission.READ_PHONE_NUMBERS'
- `UWB_RANGING`: 'android.permission.UWB_RANGING'
- `BODY_SENSORS_BACKGROUND`: 'android.permission.BODY_SENSORS_BACKGROUND'
- `READ_MEDIA_IMAGES`: 'android.permission.READ_MEDIA_IMAGES'
- `READ_MEDIA_VIDEO`: 'android.permission.READ_MEDIA_VIDEO'
- `READ_MEDIA_AUDIO`: 'android.permission.READ_MEDIA_AUDIO'
- `POST_NOTIFICATIONS`: 'android.permission.POST_NOTIFICATIONS'
- `NEARBY_WIFI_DEVICES`: 'android.permission.NEARBY_WIFI_DEVICES'
- `READ_VOICEMAIL`: 'com.android.voicemail.permission.READ_VOICEMAIL',
- `WRITE_VOICEMAIL`: 'com.android.voicemail.permission.WRITE_VOICEMAIL',

### Result strings for requesting permissions​

Available as constants under `PermissionsAndroid.RESULTS`:

- `GRANTED`: 'granted'
- `DENIED`: 'denied'
- `NEVER_ASK_AGAIN`: 'never_ask_again'

---

# Reference

## Methods​

### check()​

 tsx

```
static check(permission: Permission): Promise<boolean>;
```

Returns a promise resolving to a boolean value as to whether the specified permissions has been granted.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| permission | string | Yes | The permission to check for. |

---

### request()​

 tsx

```
static request(  permission: Permission,  rationale?: Rationale,): Promise<PermissionStatus>;
```

Prompts the user to enable a permission and returns a promise resolving to a string value (see result strings above) indicating whether the user allowed or denied the request or does not want to be asked again.

If `rationale` is provided, this function checks with the OS whether it is necessary to show a dialog explaining why the permission is needed ([https://developer.android.com/training/permissions/requesting.html#explain](https://developer.android.com/training/permissions/requesting.html#explain)) and then shows the system permission dialog.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| permission | string | Yes | The permission to request. |
| rationale | object | No | Seerationalebelow. |

**Rationale:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| title | string | Yes | The title of the dialog. |
| message | string | Yes | The message of the dialog. |
| buttonPositive | string | Yes | The text of the positive button. |
| buttonNegative | string | No | The text of the negative button. |
| buttonNeutral | string | No | The text of the neutral button. |

---

### requestMultiple()​

 tsx

```
static requestMultiple(  permissions: Permission[],): Promise<{[key in Permission]: PermissionStatus}>;
```

Prompts the user to enable multiple permissions in the same dialog and returns an object with the permissions as keys and strings as values (see result strings above) indicating whether the user allowed or denied the request or does not want to be asked again.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| permissions | array | Yes | Array of permissions to request. |

Is this page useful?
