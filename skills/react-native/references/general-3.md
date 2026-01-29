# Animations and more

# Animations

> Animations are very important to create a great user experience. Stationary objects must overcome inertia as they start moving. Objects in motion have momentum and rarely come to a stop immediately. Animations allow you to convey physically believable motion in your interface.

Animations are very important to create a great user experience. Stationary objects must overcome inertia as they start moving. Objects in motion have momentum and rarely come to a stop immediately. Animations allow you to convey physically believable motion in your interface.

React Native provides two complementary animation systems: [Animated](https://reactnative.dev/docs/animations#animated-api) for granular and interactive control of specific values, and [LayoutAnimation](https://reactnative.dev/docs/animations#layoutanimation-api) for animated global layout transactions.

## AnimatedAPI​

The [Animated](https://reactnative.dev/docs/animated) API is designed to concisely express a wide variety of interesting animation and interaction patterns in a very performant way. `Animated` focuses on declarative relationships between inputs and outputs, with configurable transforms in between, and `start`/`stop` methods to control time-based animation execution.

`Animated` exports six animatable component types: `View`, `Text`, `Image`, `ScrollView`, `FlatList` and `SectionList`, but you can also create your own using `Animated.createAnimatedComponent()`.

For example, a container view that fades in when it is mounted may look like this:

Let's break down what's happening here. In the `FadeInView` render method, a new `Animated.Value` called `fadeAnim` is initialized with `useRef`. The opacity property on the `View` is mapped to this animated value. Behind the scenes, the numeric value is extracted and used to set opacity.

When the component mounts, the opacity is set to 0. Then, an easing animation is started on the `fadeAnim` animated value, which will update all of its dependent mappings (in this case, only the opacity) on each frame as the value animates to the final value of 1.

This is done in an optimized way that is faster than calling `setState` and re-rendering. Because the entire configuration is declarative, we will be able to implement further optimizations that serialize the configuration and runs the animation on a high-priority thread.

### Configuring animations​

Animations are heavily configurable. Custom and predefined easing functions, delays, durations, decay factors, spring constants, and more can all be tweaked depending on the type of animation.

`Animated` provides several animation types, the most commonly used one being [Animated.timing()](https://reactnative.dev/docs/animated#timing). It supports animating a value over time using one of various predefined easing functions, or you can use your own. Easing functions are typically used in animation to convey gradual acceleration and deceleration of objects.

By default, `timing` will use an easeInOut curve that conveys gradual acceleration to full speed and concludes by gradually decelerating to a stop. You can specify a different easing function by passing an `easing` parameter. Custom `duration` or even a `delay` before the animation starts is also supported.

For example, if we want to create a 2-second long animation of an object that slightly backs up before moving to its final position:

 tsx

```
Animated.timing(this.state.xPosition, {  toValue: 100,  easing: Easing.back(),  duration: 2000,  useNativeDriver: true,}).start();
```

Take a look at the [Configuring animations](https://reactnative.dev/docs/animated#configuring-animations) section of the `Animated` API reference to learn more about all the config parameters supported by the built-in animations.

### Composing animations​

Animations can be combined and played in sequence or in parallel. Sequential animations can play immediately after the previous animation has finished, or they can start after a specified delay. The `Animated` API provides several methods, such as `sequence()` and `delay()`, each of which take an array of animations to execute and automatically calls `start()`/`stop()` as needed.

For example, the following animation coasts to a stop, then it springs back while twirling in parallel:

 tsx

```
Animated.sequence([  // decay, then spring to start and twirl  Animated.decay(position, {    // coast to a stop    velocity: {x: gestureState.vx, y: gestureState.vy}, // velocity from gesture release    deceleration: 0.997,    useNativeDriver: true,  }),  Animated.parallel([    // after decay, in parallel:    Animated.spring(position, {      toValue: {x: 0, y: 0}, // return to start      useNativeDriver: true,    }),    Animated.timing(twirl, {      // and twirl      toValue: 360,      useNativeDriver: true,    }),  ]),]).start(); // start the sequence group
```

If one animation is stopped or interrupted, then all other animations in the group are also stopped. `Animated.parallel` has a `stopTogether` option that can be set to `false` to disable this.

You can find a full list of composition methods in the [Composing animations](https://reactnative.dev/docs/animated#composing-animations) section of the `Animated` API reference.

### Combining animated values​

You can [combine two animated values](https://reactnative.dev/docs/animated#combining-animated-values) via addition, multiplication, division, or modulo to make a new animated value.

There are some cases where an animated value needs to invert another animated value for calculation. An example is inverting a scale (2x --> 0.5x):

 tsx

```
const a = new Animated.Value(1);const b = Animated.divide(1, a);Animated.spring(a, {  toValue: 2,  useNativeDriver: true,}).start();
```

### Interpolation​

Each property can be run through an interpolation first. An interpolation maps input ranges to output ranges, typically using a linear interpolation but also supports easing functions. By default, it will extrapolate the curve beyond the ranges given, but you can also have it clamp the output value.

A basic mapping to convert a 0-1 range to a 0-100 range would be:

 tsx

```
value.interpolate({  inputRange: [0, 1],  outputRange: [0, 100],});
```

For example, you may want to think about your `Animated.Value` as going from 0 to 1, but animate the position from 150px to 0px and the opacity from 0 to 1. This can be done by modifying `style` from the example above like so:

 tsx

```
style={{    opacity: this.state.fadeAnim, // Binds directly    transform: [{      translateY: this.state.fadeAnim.interpolate({        inputRange: [0, 1],        outputRange: [150, 0]  // 0 : 150, 0.5 : 75, 1 : 0      }),    }],  }}
```

[interpolate()](https://reactnative.dev/docs/animated#interpolate) supports multiple range segments as well, which is handy for defining dead zones and other handy tricks. For example, to get a negation relationship at -300 that goes to 0 at -100, then back up to 1 at 0, and then back down to zero at 100 followed by a dead-zone that remains at 0 for everything beyond that, you could do:

 tsx

```
value.interpolate({  inputRange: [-300, -100, 0, 100, 101],  outputRange: [300, 0, 1, 0, 0],});
```

Which would map like so:

```
Input | Output------|-------  -400|    450  -300|    300  -200|    150  -100|      0   -50|    0.5     0|      1    50|    0.5   100|      0   101|      0   200|      0
```

`interpolate()` also supports mapping to strings, allowing you to animate colors as well as values with units. For example, if you wanted to animate a rotation you could do:

 tsx

```
value.interpolate({  inputRange: [0, 360],  outputRange: ['0deg', '360deg'],});
```

`interpolate()` also supports arbitrary easing functions, many of which are already implemented in the [Easing](https://reactnative.dev/docs/easing) module. `interpolate()` also has configurable behavior for extrapolating the `outputRange`. You can set the extrapolation by setting the `extrapolate`, `extrapolateLeft`, or `extrapolateRight` options. The default value is `extend` but you can use `clamp` to prevent the output value from exceeding `outputRange`.

### Tracking dynamic values​

Animated values can also track other values by setting the `toValue` of an animation to another animated value instead of a plain number. For example, a "Chat Heads" animation like the one used by Messenger on Android could be implemented with a `spring()` pinned on another animated value, or with `timing()` and a `duration` of 0 for rigid tracking. They can also be composed with interpolations:

 tsx

```
Animated.spring(follower, {toValue: leader}).start();Animated.timing(opacity, {  toValue: pan.x.interpolate({    inputRange: [0, 300],    outputRange: [1, 0],  }),  useNativeDriver: true,}).start();
```

The `leader` and `follower` animated values would be implemented using `Animated.ValueXY()`. `ValueXY` is a handy way to deal with 2D interactions, such as panning or dragging. It is a basic wrapper that contains two `Animated.Value` instances and some helper functions that call through to them, making `ValueXY` a drop-in replacement for `Value` in many cases. It allows us to track both x and y values in the example above.

### Tracking gestures​

Gestures, like panning or scrolling, and other events can map directly to animated values using [Animated.event](https://reactnative.dev/docs/animated#event). This is done with a structured map syntax so that values can be extracted from complex event objects. The first level is an array to allow mapping across multiple args, and that array contains nested objects.

For example, when working with horizontal scrolling gestures, you would do the following in order to map `event.nativeEvent.contentOffset.x` to `scrollX` (an `Animated.Value`):

 tsx

```
onScroll={Animated.event(   // scrollX = e.nativeEvent.contentOffset.x   [{nativeEvent: {        contentOffset: {          x: scrollX        }      }    }] )}
```

The following example implements a horizontal scrolling carousel where the scroll position indicators are animated using the `Animated.event` used in the `ScrollView`

#### ScrollView with Animated Event Example​

When using `PanResponder`, you could use the following code to extract the x and y positions from `gestureState.dx` and `gestureState.dy`. We use a `null` in the first position of the array, as we are only interested in the second argument passed to the `PanResponder` handler, which is the `gestureState`.

 tsx

```
onPanResponderMove={Animated.event(  [null, // ignore the native event  // extract dx and dy from gestureState  // like 'pan.x = gestureState.dx, pan.y = gestureState.dy'  {dx: pan.x, dy: pan.y}])}
```

#### PanResponder with Animated Event Example​

### Responding to the current animation value​

You may notice that there is no clear way to read the current value while animating. This is because the value may only be known in the native runtime due to optimizations. If you need to run JavaScript in response to the current value, there are two approaches:

- `spring.stopAnimation(callback)` will stop the animation and invoke `callback` with the final value. This is useful when making gesture transitions.
- `spring.addListener(callback)` will invoke `callback` asynchronously while the animation is running, providing a recent value. This is useful for triggering state changes, for example snapping a bobble to a new option as the user drags it closer, because these larger state changes are less sensitive to a few frames of lag compared to continuous gestures like panning which need to run at 60 fps.

`Animated` is designed to be fully serializable so that animations can be run in a high performance way, independent of the normal JavaScript event loop. This does influence the API, so keep that in mind when it seems a little trickier to do something compared to a fully synchronous system. Check out `Animated.Value.addListener` as a way to work around some of these limitations, but use it sparingly since it might have performance implications in the future.

### Using the native driver​

The `Animated` API is designed to be serializable. By using the [native driver](https://reactnative.dev/blog/2017/02/14/using-native-driver-for-animated), we send everything about the animation to native before starting the animation, allowing native code to perform the animation on the UI thread without having to go through the bridge on every frame. Once the animation has started, the JS thread can be blocked without affecting the animation.

Using the native driver for normal animations can be accomplished by setting `useNativeDriver: true` in animation config when starting it. Animations without a `useNativeDriver` property will default to false for legacy reasons, but emit a warning (and typechecking error in TypeScript).

 tsx

```
Animated.timing(this.state.animatedValue, {  toValue: 1,  duration: 500,  useNativeDriver: true, // <-- Set this to true}).start();
```

Animated values are only compatible with one driver so if you use native driver when starting an animation on a value, make sure every animation on that value also uses the native driver.

The native driver also works with `Animated.event`. This is especially useful for animations that follow the scroll position as without the native driver, the animation will always run a frame behind the gesture due to the async nature of React Native.

 tsx

```
<Animated.ScrollView // <-- Use the Animated ScrollView wrapper  onScroll={Animated.event(    [      {        nativeEvent: {          contentOffset: {y: this.state.animatedValue},        },      },    ],    {useNativeDriver: true}, // <-- Set this to true  )}>  {content}</Animated.ScrollView>
```

You can see the native driver in action by running the [RNTester app](https://github.com/facebook/react-native/blob/main/packages/rn-tester/), then loading the Native Animated Example. You can also take a look at the [source code](https://github.com/facebook/react-native/blob/main/packages/rn-tester/js/examples/NativeAnimation/NativeAnimationsExample.js) to learn how these examples were produced.

#### Caveats​

Not everything you can do with `Animated` is currently supported by the native driver. The main limitation is that you can only animate non-layout properties: things like `transform` and `opacity` will work, but Flexbox and position properties will not. When using `Animated.event`, it will only work with direct events and not bubbling events. This means it does not work with `PanResponder` but does work with things like `ScrollView#onScroll`.

When an animation is running, it can prevent `VirtualizedList` components from rendering more rows. If you need to run a long or looping animation while the user is scrolling through a list, you can use `isInteraction: false` in your animation's config to prevent this issue.

### Bear in mind​

While using transform styles such as `rotateY`, `rotateX`, and others ensure the transform style `perspective` is in place. At this time some animations may not render on Android without it. Example below.

 tsx

```
<Animated.View  style={{    transform: [      {scale: this.state.scale},      {rotateY: this.state.rotateY},      {perspective: 1000}, // without this line this Animation will not render on Android while working fine on iOS    ],  }}/>
```

### Additional examples​

The RNTester app has various examples of `Animated` in use:

- [AnimatedGratuitousApp](https://github.com/facebook/react-native/tree/main/packages/rn-tester/js/examples/AnimatedGratuitousApp)
- [NativeAnimationsExample](https://github.com/facebook/react-native/blob/main/packages/rn-tester/js/examples/NativeAnimation/NativeAnimationsExample.js)

## LayoutAnimationAPI​

`LayoutAnimation` allows you to globally configure `create` and `update` animations that will be used for all views in the next render/layout cycle. This is useful for doing Flexbox layout updates without bothering to measure or calculate specific properties in order to animate them directly, and is especially useful when layout changes may affect ancestors, for example a "see more" expansion that also increases the size of the parent and pushes down the row below which would otherwise require explicit coordination between the components in order to animate them all in sync.

Note that although `LayoutAnimation` is very powerful and can be quite useful, it provides much less control than `Animated` and other animation libraries, so you may need to use another approach if you can't get `LayoutAnimation` to do what you want.

Note that in order to get this to work on **Android** you need to set the following flags via `UIManager`:

 tsx

```
UIManager.setLayoutAnimationEnabledExperimental(true);
```

This example uses a preset value, you can customize the animations as you need, see [LayoutAnimation.js](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/LayoutAnimation/LayoutAnimation.js) for more information.

## Additional notes​

### requestAnimationFrame​

`requestAnimationFrame` is a polyfill from the browser that you might be familiar with. It accepts a function as its only argument and calls that function before the next repaint. It is an essential building block for animations that underlies all of the JavaScript-based animation APIs. In general, you shouldn't need to call this yourself - the animation APIs will manage frame updates for you.

### setNativeProps​

As mentioned [in the Direct Manipulation section](https://reactnative.dev/docs/legacy/direct-manipulation), `setNativeProps` allows us to modify properties of native-backed components (components that are actually backed by native views, unlike composite components) directly, without having to `setState` and re-render the component hierarchy.

We could use this in the Rebound example to update the scale - this might be helpful if the component that we are updating is deeply nested and hasn't been optimized with `shouldComponentUpdate`.

If you find your animations with dropping frames (performing below 60 frames per second), look into using `setNativeProps` or `shouldComponentUpdate` to optimize them. Or you could run the animations on the UI thread rather than the JavaScript thread [with the useNativeDriver option](https://reactnative.dev/blog/2017/02/14/using-native-driver-for-animated). You may also want to defer any computationally intensive work until after animations are complete, using the [InteractionManager](https://reactnative.dev/docs/interactionmanager). You can monitor the frame rate by using the In-App Dev Menu "FPS Monitor" tool.

Is this page useful?

---

# App Extensions

> App extensions let you provide custom functionality and content outside of your main app. There are different types of app extensions on iOS, and they are all covered in the App Extension Programming Guide. In this guide, we'll briefly cover how you may take advantage of app extensions on iOS.

App extensions let you provide custom functionality and content outside of your main app. There are different types of app extensions on iOS, and they are all covered in the [App Extension Programming Guide](https://developer.apple.com/library/content/documentation/General/Conceptual/ExtensibilityPG/index.html#//apple_ref/doc/uid/TP40014214-CH20-SW1). In this guide, we'll briefly cover how you may take advantage of app extensions on iOS.

## Memory use in extensions​

As these extensions are loaded outside of the regular app sandbox, it's highly likely that several of these app extensions will be loaded simultaneously. As you might expect, these extensions have small memory usage limits. Keep these in mind when developing your app extensions. It's always highly recommended to test your application on an actual device, and more so when developing app extensions: too frequently, developers find that their extension works fine in the iOS Simulator, only to get user reports that their extension is not loading on actual devices.

### Today widget​

The memory limit of a Today widget is 16 MB. As it happens, Today widget implementations using React Native may work unreliably because the memory usage tends to be too high. You can tell if your Today widget is exceeding the memory limit if it yields the message 'Unable to Load':

![image](https://reactnative.dev/assets/images/TodayWidgetUnableToLoad-b931f8be6eeb72c037338b9ab9766477.jpg)

Always make sure to test your app extensions in a real device, but be aware that this may not be sufficient, especially when dealing with Today widgets. Debug-configured builds are more likely to exceed the memory limits, while release-configured builds don't fail right away. We highly recommend that you use [Xcode's Instruments](https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/index.html) to analyze your real world memory usage, as it's very likely that your release-configured build is very close to the 16 MB limit. In situations like these, you can quickly go over the 16 MB limit by performing common operations, such as fetching data from an API.

To experiment with the limits of React Native Today widget implementations, try extending the example project in [react-native-today-widget](https://github.com/matejkriz/react-native-today-widget/).

### Other app extensions​

Other types of app extensions have greater memory limits than the Today widget. For instance, Custom Keyboard extensions are limited to 48 MB, and Share extensions are limited to 120 MB. Implementing such app extensions with React Native is more viable. One proof of concept example is [react-native-ios-share-extension](https://github.com/andrewsardone/react-native-ios-share-extension).

Is this page useful?

---

# Appearance

> The Appearance module exposes information about the user's appearance preferences, such as their preferred color scheme (light or dark).

tsx

```
import {Appearance} from 'react-native';
```

The `Appearance` module exposes information about the user's appearance preferences, such as their preferred color scheme (light or dark).

#### Developer notes​

info

The `Appearance` API is inspired by the [Media Queries draft](https://drafts.csswg.org/mediaqueries-5/) from the W3C. The color scheme preference is modeled after the [prefers-color-schemeCSS media feature](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme).

info

The color scheme preference will map to the user's Light or [Dark theme](https://developer.android.com/guide/topics/ui/look-and-feel/darktheme) preference on Android 10 (API level 29) devices and higher.

info

The color scheme preference will map to the user's Light or [Dark Mode](https://developer.apple.com/design/human-interface-guidelines/ios/visual-design/dark-mode/) preference on iOS 13 devices and higher.

note

When taking a screenshot, by default, the color scheme may flicker between light and dark mode. It happens because the iOS takes snapshots on both color schemes and updating the user interface with color scheme is asynchronous.

## Example​

You can use the `Appearance` module to determine if the user prefers a dark color scheme:

 tsx

```
const colorScheme = Appearance.getColorScheme();if (colorScheme === 'dark') {  // Use dark color scheme}
```

Although the color scheme is available immediately, this may change (e.g. scheduled color scheme change at sunrise or sunset). Any rendering logic or styles that depend on the user preferred color scheme should try to call this function on every render, rather than caching the value. For example, you may use the [useColorScheme](https://reactnative.dev/docs/usecolorscheme) React hook as it provides and subscribes to color scheme updates, or you may use inline styles rather than setting a value in a `StyleSheet`.

---

# Reference

## Methods​

### getColorScheme()​

 tsx

```
static getColorScheme(): 'light' | 'dark' | null;
```

Indicates the current user preferred color scheme. The value may be updated later, either through direct user action (e.g. theme selection in device settings or application-level selected user interface style via `setColorScheme`) or on a schedule (e.g. light and dark themes that follow the day/night cycle).

Supported color schemes:

- `'light'`: The user prefers a light color theme.
- `'dark'`: The user prefers a dark color theme.
- `null`: The user has not indicated a preferred color theme.

See also: `useColorScheme` hook.

 note

`getColorScheme()` will always return `light` when debugging with Chrome.

---

### setColorScheme()​

 tsx

```
static setColorScheme('light' | 'dark' | null): void;
```

Force the application to always adopt a light or dark interface style. The default value is `null` which causes the application to inherit the system's interface style. If you assign a different value, the new style applies to the application and all native elements within the application (Alerts, Pickers etc).

Supported color schemes:

- `light`: Apply light user interface style.
- `dark`: Apply dark user interface style.
- null: Follow the system's interface style.

 note

The change will not affect the system's selected interface style or any style set in other applications.

---

### addChangeListener()​

 tsx

```
static addChangeListener(  listener: (preferences: {colorScheme: 'light' | 'dark' | null}) => void,): NativeEventSubscription;
```

Add an event handler that is fired when appearance preferences change.

Is this page useful?

---

# Appendix

> I. Terminology

## I. Terminology​

- **Spec** - TypeScript or Flow code that describes the API for a Turbo Native Module or Fabric Native component. Used by **Codegen** to generate boilerplate code.
- **Native Modules** - Native libraries that have no User Interface (UI) for the user. Examples would be persistent storage, notifications, network events. These are accessible to your JavaScript application code as functions and objects.
- **Native Component** - Native platform views that are available to your application JavaScript code through React Components.
- **Legacy Native Components** - Components which are running on the old React Native architecture.
- **Legacy Native Modules** - Modules which are running on the old React Native architecture.

## II. Codegen Typings​

You may use the following table as a reference for which types are supported and what they map to in each platform:

| Flow | TypeScript | Flow Nullable Support | TypeScript Nullable Support | Android (Java) | iOS (ObjC) |
| --- | --- | --- | --- | --- | --- |
| string | string | ?string | string | null | string | NSString |
| boolean | boolean | ?boolean | boolean | null | Boolean | NSNumber |
| Object Literal{| foo: string, ...|} | { foo: string, ...} as const | ?{| foo: string, ...|} | ?{ foo: string, ...} as const | - | - |
| Object [1] | Object [1] | ?Object | Object | null | ReadableMap | @(untyped dictionary) |
| Array<T> | Array<T> | ?Array<T> | Array<T> | null | ReadableArray | NSArray(orRCTConvertVecToArraywhen used inside objects) |
| Function | Function | ?Function | Function | null | - | - |
| Promise<T> | Promise<T> | ?Promise<T> | Promise<T> | null | com.facebook.react.bridge.Promise | RCTPromiseResolveandRCTPromiseRejectBlock |
| Type Unions'SUCCESS'|'FAIL' | Type Unions'SUCCESS'|'FAIL' | Only as callbacks |  | - | - |
| Callbacks() => | Callbacks() => | Yes |  | com.facebook.react.bridge.Callback | RCTResponseSenderBlock |
| number | number | No |  | double | NSNumber |

### Notes:​

**[1]** We strongly recommend using Object literals instead of Objects.

 info

You may also find it useful to refer to the JavaScript specifications for the core modules in React Native. These are located inside the `Libraries/` directory in the React Native repository.

Is this page useful?

---

# AppRegistry

> Project with Native Code Required

### Project with Native Code Required

If you are using the managed Expo workflow there is only ever one entry component registered with `AppRegistry` and it is handled automatically (or through [registerRootComponent](https://docs.expo.dev/versions/latest/sdk/register-root-component/)). You do not need to use this API.

`AppRegistry` is the JS entry point to running all React Native apps. App root components should register themselves with `AppRegistry.registerComponent`, then the native system can load the bundle for the app and then actually run the app when it's ready by invoking `AppRegistry.runApplication`.

 tsx

```
import {Text, AppRegistry} from 'react-native';const App = () => (  <View>    <Text>App1</Text>  </View>);AppRegistry.registerComponent('Appname', () => App);
```

To "stop" an application when a view should be destroyed, call `AppRegistry.unmountApplicationComponentAtRootTag` with the tag that was passed into `runApplication`. These should always be used as a pair.

`AppRegistry` should be required early in the `require` sequence to make sure the JS execution environment is setup before other modules are required.

---

# Reference

## Methods​

### getAppKeys()​

 tsx

```
static getAppKeys(): string[];
```

Returns an array of strings.

---

### getRegistry()​

 tsx

```
static getRegistry(): {sections: string[]; runnables: Runnable[]};
```

Returns a [Registry](https://reactnative.dev/docs/appregistry#registry) object.

---

### getRunnable()​

 tsx

```
static getRunnable(appKey: string): : Runnable | undefined;
```

Returns a [Runnable](https://reactnative.dev/docs/appregistry#runnable) object.

**Parameters:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |

---

### getSectionKeys()​

 tsx

```
static getSectionKeys(): string[];
```

Returns an array of strings.

---

### getSections()​

 tsx

```
static getSections(): Record<string, Runnable>;
```

Returns a [Runnables](https://reactnative.dev/docs/appregistry#runnables) object.

---

### registerCancellableHeadlessTask()​

 tsx

```
static registerCancellableHeadlessTask(  taskKey: string,  taskProvider: TaskProvider,  taskCancelProvider: TaskCancelProvider,);
```

Register a headless task which can be cancelled. A headless task is a bit of code that runs without a UI.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| taskKeyRequired | string | The native id for this task instance that was used when startHeadlessTask was called. |
| taskProviderRequired | TaskProvider | A promise returning function that takes some data passed from the native side as the only argument. When the promise is resolved or rejected the native side is notified of this event and it may decide to destroy the JS context. |
| taskCancelProviderRequired | TaskCancelProvider | a void returning function that takes no arguments; when a cancellation is requested, the function being executed by taskProvider should wrap up and return ASAP. |

---

### registerComponent()​

 tsx

```
static registerComponent(  appKey: string,  getComponentFunc: ComponentProvider,  section?: boolean,): string;
```

**Parameters:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |
| componentProviderRequired | ComponentProvider |
| section | boolean |

---

### registerConfig()​

 tsx

```
static registerConfig(config: AppConfig[]);
```

**Parameters:**

| Name | Type |
| --- | --- |
| configRequired | AppConfig[] |

---

### registerHeadlessTask()​

 tsx

```
static registerHeadlessTask(  taskKey: string,  taskProvider: TaskProvider,);
```

Register a headless task. A headless task is a bit of code that runs without a UI.

This is a way to run tasks in JavaScript while your app is in the background. It can be used, for example, to sync fresh data, handle push notifications, or play music.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| taskKeyRequired | string | The native id for this task instance that was used when startHeadlessTask was called. |
| taskProviderRequired | TaskProvider | A promise returning function that takes some data passed from the native side as the only argument. When the promise is resolved or rejected the native side is notified of this event and it may decide to destroy the JS context. |

---

### registerRunnable()​

 tsx

```
static registerRunnable(appKey: string, func: Runnable): string;
```

**Parameters:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |
| runRequired | function |

---

### registerSection()​

 tsx

```
static registerSection(  appKey: string,  component: ComponentProvider,);
```

**Parameters:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |
| componentRequired | ComponentProvider |

---

### runApplication()​

 tsx

```
static runApplication(appKey: string, appParameters: any): void;
```

Loads the JavaScript bundle and runs the app.

**Parameters:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |
| appParametersRequired | any |

---

### setComponentProviderInstrumentationHook()​

 tsx

```
static setComponentProviderInstrumentationHook(  hook: ComponentProviderInstrumentationHook,);
```

**Parameters:**

| Name | Type |
| --- | --- |
| hookRequired | function |

A valid `hook` function accepts the following as arguments:

| Name | Type |
| --- | --- |
| componentRequired | ComponentProvider |
| scopedPerformanceLoggerRequired | IPerformanceLogger |

The function must also return a React Component.

---

### setWrapperComponentProvider()​

 tsx

```
static setWrapperComponentProvider(  provider: WrapperComponentProvider,);
```

**Parameters:**

| Name | Type |
| --- | --- |
| providerRequired | ComponentProvider |

---

### startHeadlessTask()​

 tsx

```
static startHeadlessTask(  taskId: number,  taskKey: string,  data: any,);
```

Only called from native code. Starts a headless task.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| taskIdRequired | number | The native id for this task instance to keep track of its execution. |
| taskKeyRequired | string | The key for the task to start. |
| dataRequired | any | The data to pass to the task. |

---

### unmountApplicationComponentAtRootTag()​

 tsx

```
static unmountApplicationComponentAtRootTag(rootTag: number);
```

Stops an application when a view should be destroyed.

**Parameters:**

| Name | Type |
| --- | --- |
| rootTagRequired | number |

## Type Definitions​

### AppConfig​

Application configuration for the `registerConfig` method.

| Type |
| --- |
| object |

**Properties:**

| Name | Type |
| --- | --- |
| appKeyRequired | string |
| component | ComponentProvider |
| run | function |
| section | boolean |

 note

Every config is expected to set either `component` or `run` function.

### Registry​

| Type |
| --- |
| object |

**Properties:**

| Name | Type |
| --- | --- |
| runnables | array ofRunnables |
| sections | array of strings |

### Runnable​

| Type |
| --- |
| object |

**Properties:**

| Name | Type |
| --- | --- |
| component | ComponentProvider |
| run | function |

### Runnables​

An object with key of `appKey` and value of type of [Runnable](https://reactnative.dev/docs/appregistry#runnable).

| Type |
| --- |
| object |

### Task​

A `Task` is a function that accepts any data as argument and returns a Promise that resolves to `undefined`.

| Type |
| --- |
| function |

### TaskCanceller​

A `TaskCanceller` is a function that accepts no argument and returns void.

| Type |
| --- |
| function |

### TaskCancelProvider​

A valid `TaskCancelProvider` is a function that returns a [TaskCanceller](https://reactnative.dev/docs/appregistry#taskcanceller).

| Type |
| --- |
| function |

### TaskProvider​

A valid `TaskProvider` is a function that returns a [Task](https://reactnative.dev/docs/appregistry#task).

| Type |
| --- |
| function |

Is this page useful?

---

# AppState

> AppState can tell you if the app is in the foreground or background, and notify you when the state changes.

`AppState` can tell you if the app is in the foreground or background, and notify you when the state changes.

AppState is frequently used to determine the intent and proper behavior when handling push notifications.

### App States​

- `active` - The app is running in the foreground
- `background` - The app is running in the background. The user is either:
  - in another app
  - on the home screen
  - [Android] on another `Activity` (even if it was launched by your app)
- [iOS] `inactive` - This is a state that occurs when transitioning between foreground & background, and during periods of inactivity such as entering the multitasking view, opening the Notification Center or in the event of an incoming call.

For more information, see [Apple's documentation](https://developer.apple.com/documentation/uikit/app_and_scenes/managing_your_app_s_life_cycle)

## Basic Usage​

To see the current state, you can check `AppState.currentState`, which will be kept up-to-date. However, `currentState` will be null at launch while `AppState` retrieves it over the bridge.

This example will only ever appear to say "Current state is: active" because the app is only visible to the user when in the `active` state, and the null state will happen only momentarily. If you want to experiment with the code we recommend to use your own device instead of embedded preview.

---

# Reference

## Events​

### change​

This event is received when the app state has changed. The listener is called with one of [the current app state values](https://reactnative.dev/docs/appstate#app-states).

### memoryWarningiOS​

Fires when the app receives a memory warning from the operating system.

### focusAndroid​

Received when the app gains focus (the user is interacting with the app).

### blurAndroid​

Received when the user is not actively interacting with the app. Useful in situations when the user pulls down the [notification drawer](https://developer.android.com/guide/topics/ui/notifiers/notifications#bar-and-drawer). `AppState` won't change but the `blur` event will get fired.

## Methods​

### addEventListener()​

 tsx

```
static addEventListener(  type: AppStateEvent,  listener: (state: AppStateStatus) => void,): NativeEventSubscription;
```

Sets up a function that will be called whenever the specified event type on AppState occurs. Valid values for `eventType` are
[listed above](#events). Returns the `EventSubscription`.

## Properties​

### currentState​

 tsx

```
static currentState: AppStateStatus;
```

Is this page useful?

---

# BackHandler

> The Backhandler API detects hardware button presses for back navigation, lets you register event listeners for the system's back action, and lets you control how your application responds. It is Android-only.

The Backhandler API detects hardware button presses for back navigation, lets you register event listeners for the system's back action, and lets you control how your application responds. It is Android-only.

The event subscriptions are called in reverse order (i.e. the last registered subscription is called first).

- **If one subscription returns true,** then subscriptions registered earlier will not be called.
- **If no subscription returns true or none are registered,** it programmatically invokes the default back button functionality to exit the app.

 Warning for modal users

If your app shows an opened `Modal`, `BackHandler` will not publish any events ([seeModaldocs](https://reactnative.dev/docs/modal#onrequestclose)).

## Pattern​

 tsx

```
const subscription = BackHandler.addEventListener(  'hardwareBackPress',  function () {    /**     * this.onMainScreen and this.goBack are just examples,     * you need to use your own implementation here.     *     * Typically you would use the navigator here to go to the last state.     */    if (!this.onMainScreen()) {      this.goBack();      /**       * When true is returned the event will not be bubbled up       * & no other back action will execute       */      return true;    }    /**     * Returning false will let the event to bubble up & let other event listeners     * or the system's default back action to be executed.     */    return false;  },);// Unsubscribe the listener on unmountsubscription.remove();
```

## Example​

The following example implements a scenario where you confirm if the user wants to exit the app:

`BackHandler.addEventListener` creates an event listener & returns a `NativeEventSubscription` object which should be cleared using `NativeEventSubscription.remove` method.

## Usage with React Navigation​

If you are using React Navigation to navigate across different screens, you can follow their guide on [Custom Android back button behaviour](https://reactnavigation.org/docs/custom-android-back-button-handling/)

## Backhandler hook​

[React Native Hooks](https://github.com/react-native-community/hooks#usebackhandler) has a nice `useBackHandler` hook which will simplify the process of setting up event listeners.

---

# Reference

## Methods​

### addEventListener()​

 tsx

```
static addEventListener(  eventName: BackPressEventName,  handler: () => boolean | null | undefined,): NativeEventSubscription;
```

---

### exitApp()​

 tsx

```
static exitApp();
```

Is this page useful?
