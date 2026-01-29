# Communication between native and React Native and more

# Communication between native and React Native

> In Integrating with Existing Apps guide and Native UI Components guide we learn how to embed React Native in a native component and vice versa. When we mix native and React Native components, we'll eventually find a need to communicate between these two worlds. Some ways to achieve that have been already mentioned in other guides. This article summarizes available techniques.

In [Integrating with Existing Apps guide](https://reactnative.dev/docs/integration-with-existing-apps) and [Native UI Components guide](https://reactnative.dev/docs/legacy/native-components-ios) we learn how to embed React Native in a native component and vice versa. When we mix native and React Native components, we'll eventually find a need to communicate between these two worlds. Some ways to achieve that have been already mentioned in other guides. This article summarizes available techniques.

## Introduction​

React Native is inspired by React, so the basic idea of the information flow is similar. The flow in React is one-directional. We maintain a hierarchy of components, in which each component depends only on its parent and its own internal state. We do this with properties: data is passed from a parent to its children in a top-down manner. If an ancestor component relies on the state of its descendant, one should pass down a callback to be used by the descendant to update the ancestor.

The same concept applies to React Native. As long as we are building our application purely within the framework, we can drive our app with properties and callbacks. But, when we mix React Native and native components, we need some specific, cross-language mechanisms that would allow us to pass information between them.

## Properties​

Properties are the most straightforward way of cross-component communication. So we need a way to pass properties both from native to React Native, and from React Native to native.

### Passing properties from native to React Native​

In order to embed a React Native view in a native component, we use `RCTRootView`. `RCTRootView` is a `UIView` that holds a React Native app. It also provides an interface between native side and the hosted app.

`RCTRootView` has an initializer that allows you to pass arbitrary properties down to the React Native app. The `initialProperties` parameter has to be an instance of `NSDictionary`. The dictionary is internally converted into a JSON object that the top-level JS component can reference.

 objectivec

```
NSArray *imageList = @[@"https://dummyimage.com/600x400/ffffff/000000.png",                       @"https://dummyimage.com/600x400/000000/ffffff.png"];NSDictionary *props = @{@"images" : imageList};RCTRootView *rootView = [[RCTRootView alloc] initWithBridge:bridge                                                 moduleName:@"ImageBrowserApp"                                          initialProperties:props];
```

 tsx

```
import React from 'react';import {View, Image} from 'react-native';export default class ImageBrowserApp extends React.Component {  renderImage(imgURI) {    return <Image source={{uri: imgURI}} />;  }  render() {    return <View>{this.props.images.map(this.renderImage)}</View>;  }}
```

`RCTRootView` also provides a read-write property `appProperties`. After `appProperties` is set, the React Native app is re-rendered with new properties. The update is only performed when the new updated properties differ from the previous ones.

 objectivec

```
NSArray *imageList = @[@"https://dummyimage.com/600x400/ff0000/000000.png",                       @"https://dummyimage.com/600x400/ffffff/ff0000.png"];rootView.appProperties = @{@"images" : imageList};
```

It is fine to update properties anytime. However, updates have to be performed on the main thread. You use the getter on any thread.

 note

Currently, there is a known issue where setting appProperties during the bridge startup, the change can be lost. See [https://github.com/facebook/react-native/issues/20115](https://github.com/facebook/react-native/issues/20115) for more information.

There is no way to update only a few properties at a time. We suggest that you build it into your own wrapper instead.

### Passing properties from React Native to native​

The problem exposing properties of native components is covered in detail in [this article](https://reactnative.dev/docs/legacy/native-components-ios#properties). In short, export properties with `RCT_CUSTOM_VIEW_PROPERTY` macro in your custom native component, then use them in React Native as if the component was an ordinary React Native component.

### Limits of properties​

The main drawback of cross-language properties is that they do not support callbacks, which would allow us to handle bottom-up data bindings. Imagine you have a small RN view that you want to be removed from the native parent view as a result of a JS action. There is no way to do that with props, as the information would need to go bottom-up.

Although we have a flavor of cross-language callbacks ([described here](https://reactnative.dev/docs/legacy/native-modules-ios#callbacks)), these callbacks are not always the thing we need. The main problem is that they are not intended to be passed as properties. Rather, this mechanism allows us to trigger a native action from JS, and handle the result of that action in JS.

## Other ways of cross-language interaction (events and native modules)​

As stated in the previous chapter, using properties comes with some limitations. Sometimes properties are not enough to drive the logic of our app and we need a solution that gives more flexibility. This chapter covers other communication techniques available in React Native. They can be used for internal communication (between JS and native layers in RN) as well as for external communication (between RN and the 'pure native' part of your app).

React Native enables you to perform cross-language function calls. You can execute custom native code from JS and vice versa. Unfortunately, depending on the side we are working on, we achieve the same goal in different ways. For native - we use events mechanism to schedule an execution of a handler function in JS, while for React Native we directly call methods exported by native modules.

### Calling React Native functions from native (events)​

Events are described in detail in [this article](https://reactnative.dev/docs/legacy/native-components-ios#events). Note that using events gives us no guarantees about execution time, as the event is handled on a separate thread.

Events are powerful, because they allow us to change React Native components without needing a reference to them. However, there are some pitfalls that you can fall into while using them:

- As events can be sent from anywhere, they can introduce spaghetti-style dependencies into your project.
- Events share namespace, which means that you may encounter some name collisions. Collisions will not be detected statically, which makes them hard to debug.
- If you use several instances of the same React Native component and you want to distinguish them from the perspective of your event, you'll likely need to introduce identifiers and pass them along with events (you can use the native view's `reactTag` as an identifier).

The common pattern we use when embedding native in React Native is to make the native component's RCTViewManager a delegate for the views, sending events back to JavaScript via the bridge. This keeps related event calls in one place.

### Calling native functions from React Native (native modules)​

Native modules are Objective-C classes that are available in JS. Typically one instance of each module is created per JS bridge. They can export arbitrary functions and constants to React Native. They have been covered in detail in [this article](https://reactnative.dev/docs/legacy/native-modules-ios#content).

The fact that native modules are singletons limits the mechanism in the context of embedding. Let's say we have a React Native component embedded in a native view and we want to update the native, parent view. Using the native module mechanism, we would export a function that not only takes expected arguments, but also an identifier of the parent native view. The identifier would be used to retrieve a reference to the parent view to update. That said, we would need to keep a mapping from identifiers to native views in the module.

Although this solution is complex, it is used in `RCTUIManager`, which is an internal React Native class that manages all React Native views.

Native modules can also be used to expose existing native libraries to JS. The [Geolocation library](https://github.com/michalchudziak/react-native-geolocation) is a living example of the idea.

 caution

All native modules share the same namespace. Watch out for name collisions when creating new ones.

## Layout computation flow​

When integrating native and React Native, we also need a way to consolidate two different layout systems. This section covers common layout problems and provides a brief description of mechanisms to address them.

### Layout of a native component embedded in React Native​

This case is covered in [this article](https://reactnative.dev/docs/legacy/native-components-ios#styles). To summarize, since all our native react views are subclasses of `UIView`, most style and size attributes will work like you would expect out of the box.

### Layout of a React Native component embedded in native​

#### React Native content with fixed size​

The general scenario is when we have a React Native app with a fixed size, which is known to the native side. In particular, a full-screen React Native view falls into this case. If we want a smaller root view, we can explicitly set RCTRootView's frame.

For instance, to make an RN app 200 (logical) pixels high, and the hosting view's width wide, we could do:

 SomeViewController.m

```
- (void)viewDidLoad{  [...]  RCTRootView *rootView = [[RCTRootView alloc] initWithBridge:bridge                                                   moduleName:appName                                            initialProperties:props];  rootView.frame = CGRectMake(0, 0, self.view.width, 200);  [self.view addSubview:rootView];}
```

When we have a fixed size root view, we need to respect its bounds on the JS side. In other words, we need to ensure that the React Native content can be contained within the fixed-size root view. The easiest way to ensure this is to use Flexbox layout. If you use absolute positioning, and React components are visible outside the root view's bounds, you'll get overlap with native views, causing some features to behave unexpectedly. For instance, 'TouchableHighlight' will not highlight your touches outside the root view's bounds.

It's totally fine to update root view's size dynamically by re-setting its frame property. React Native will take care of the content's layout.

#### React Native content with flexible size​

In some cases we'd like to render content of initially unknown size. Let's say the size will be defined dynamically in JS. We have two solutions to this problem.

1. You can wrap your React Native view in a `ScrollView` component. This guarantees that your content will always be available and it won't overlap with native views.
2. React Native allows you to determine, in JS, the size of the RN app and provide it to the owner of the hosting `RCTRootView`. The owner is then responsible for re-laying out the subviews and keeping the UI consistent. We achieve this with `RCTRootView`'s flexibility modes.

`RCTRootView` supports 4 different size flexibility modes:

 RCTRootView.h

```
typedef NS_ENUM(NSInteger, RCTRootViewSizeFlexibility) {  RCTRootViewSizeFlexibilityNone = 0,  RCTRootViewSizeFlexibilityWidth,  RCTRootViewSizeFlexibilityHeight,  RCTRootViewSizeFlexibilityWidthAndHeight,};
```

`RCTRootViewSizeFlexibilityNone` is the default value, which makes a root view's size fixed (but it still can be updated with `setFrame:`). The other three modes allow us to track React Native content's size updates. For instance, setting mode to `RCTRootViewSizeFlexibilityHeight` will cause React Native to measure the content's height and pass that information back to `RCTRootView`'s delegate. An arbitrary action can be performed within the delegate, including setting the root view's frame, so the content fits. The delegate is called only when the size of the content has changed.

 caution

Making a dimension flexible in both JS and native leads to undefined behavior. For example - don't make a top-level React component's width flexible (with `flexbox`) while you're using `RCTRootViewSizeFlexibilityWidth` on the hosting `RCTRootView`.

Let's look at an example.

 FlexibleSizeExampleView.m

```
- (instancetype)initWithFrame:(CGRect)frame{  [...]  _rootView = [[RCTRootView alloc] initWithBridge:bridge  moduleName:@"FlexibilityExampleApp"  initialProperties:@{}];  _rootView.delegate = self;  _rootView.sizeFlexibility = RCTRootViewSizeFlexibilityHeight;  _rootView.frame = CGRectMake(0, 0, self.frame.size.width, 0);}#pragma mark - RCTRootViewDelegate- (void)rootViewDidChangeIntrinsicSize:(RCTRootView *)rootView{  CGRect newFrame = rootView.frame;  newFrame.size = rootView.intrinsicContentSize;  rootView.frame = newFrame;}
```

In the example we have a `FlexibleSizeExampleView` view that holds a root view. We create the root view, initialize it and set the delegate. The delegate will handle size updates. Then, we set the root view's size flexibility to `RCTRootViewSizeFlexibilityHeight`, which means that `rootViewDidChangeIntrinsicSize:` method will be called every time the React Native content changes its height. Finally, we set the root view's width and position. Note that we set there height as well, but it has no effect as we made the height RN-dependent.

You can checkout full source code of the example [here](https://github.com/facebook/react-native/blob/main/packages/rn-tester/RNTester/NativeExampleViews/FlexibleSizeExampleView.mm).

It's fine to change root view's size flexibility mode dynamically. Changing flexibility mode of a root view will schedule a layout recalculation and the delegate `rootViewDidChangeIntrinsicSize:` method will be called once the content size is known.

 note

React Native layout calculation is performed on a separate thread, while native UI view updates are done on the main thread.
This may cause temporary UI inconsistencies between native and React Native. This is a known problem and our team is working on synchronizing UI updates coming from different sources.

 note

React Native does not perform any layout calculations until the root view becomes a subview of some other views.
If you want to hide React Native view until its dimensions are known, add the root view as a subview and make it initially hidden (use `UIView`'s `hidden` property). Then change its visibility in the delegate method.

Is this page useful?

---

# Core Components and APIs

> React Native provides a number of built-in Core Components ready for you to use in your app. You can find them all in the left sidebar (or menu above, if you are on a narrow screen). If you're not sure where to get started, take a look at the following categories:

React Native provides a number of built-in [Core Components](https://reactnative.dev/docs/intro-react-native-components) ready for you to use in your app. You can find them all in the left sidebar (or menu above, if you are on a narrow screen). If you're not sure where to get started, take a look at the following categories:

- [Basic Components](https://reactnative.dev/docs/components-and-apis#basic-components)
- [User Interface](https://reactnative.dev/docs/components-and-apis#user-interface)
- [List Views](https://reactnative.dev/docs/components-and-apis#list-views)
- [Android-specific](https://reactnative.dev/docs/components-and-apis#android-components-and-apis)
- [iOS-specific](https://reactnative.dev/docs/components-and-apis#ios-components-and-apis)
- [Others](https://reactnative.dev/docs/components-and-apis#others)

You're not limited to the components and APIs bundled with React Native. React Native has a community of thousands of developers. If you're looking for a library that does something specific, please refer to [this guide about finding libraries](https://reactnative.dev/docs/libraries#finding-libraries).

## Basic Components​

Most apps will end up using one or more of these basic components.

 [ViewThe most fundamental component for building a UI.](https://reactnative.dev/docs/view)[TextA component for displaying text.](https://reactnative.dev/docs/text)[ImageA component for displaying images.](https://reactnative.dev/docs/image)[TextInputA component for inputting text into the app via a keyboard.](https://reactnative.dev/docs/textinput)[PressableA wrapper component that can detect various stages of press interactions on any of its children.](https://reactnative.dev/docs/pressable)[ScrollViewProvides a scrolling container that can host multiple components and views.](https://reactnative.dev/docs/scrollview)[StyleSheetProvides an abstraction layer similar to CSS stylesheets.](https://reactnative.dev/docs/stylesheet)

## User Interface​

These common user interface controls will render on any platform.

 [ButtonA basic button component for handling touches that should render nicely on any platform.](https://reactnative.dev/docs/button)[SwitchRenders a boolean input.](https://reactnative.dev/docs/switch)

## List Views​

Unlike the more generic [ScrollView](https://reactnative.dev/docs/scrollview), the following list view components only render elements that are currently showing on the screen. This makes them a performant choice for displaying long lists of data.

 [FlatListA component for rendering performant scrollable lists.](https://reactnative.dev/docs/flatlist)[SectionListLikeFlatList, but for sectioned lists.](https://reactnative.dev/docs/sectionlist)

## Android Components and APIs​

Many of the following components provide wrappers for commonly used Android classes.

 [BackHandlerDetect hardware button presses for back navigation.](https://reactnative.dev/docs/backhandler)[DrawerLayoutAndroidRenders aDrawerLayouton Android.](https://reactnative.dev/docs/drawerlayoutandroid)[PermissionsAndroidProvides access to the permissions model introduced in Android M.](https://reactnative.dev/docs/permissionsandroid)[ToastAndroidCreate an Android Toast alert.](https://reactnative.dev/docs/toastandroid)

## iOS Components and APIs​

Many of the following components provide wrappers for commonly used UIKit classes.

 [ActionSheetIOSAPI to display an iOS action sheet or share sheet.](https://reactnative.dev/docs/actionsheetios)

## Others​

These components may be useful for certain applications. For an exhaustive list of components and APIs, check out the sidebar to the left (or menu above, if you are on a narrow screen).

 [ActivityIndicatorDisplays a circular loading indicator.](https://reactnative.dev/docs/activityindicator)[AlertLaunches an alert dialog with the specified title and message.](https://reactnative.dev/docs/alert)[AnimatedA library for creating fluid, powerful animations that are easy to build and maintain.](https://reactnative.dev/docs/animated)[DimensionsProvides an interface for getting device dimensions.](https://reactnative.dev/docs/dimensions)[KeyboardAvoidingViewProvides a view that moves out of the way of the virtual keyboard automatically.](https://reactnative.dev/docs/keyboardavoidingview)[LinkingProvides a general interface to interact with both incoming and outgoing app links.](https://reactnative.dev/docs/linking)[ModalProvides a simple way to present content above an enclosing view.](https://reactnative.dev/docs/modal)[PixelRatioProvides access to the device pixel density.](https://reactnative.dev/docs/pixelratio)[RefreshControlThis component is used inside aScrollViewto add pull to refresh functionality.](https://reactnative.dev/docs/refreshcontrol)[StatusBarComponent to control the app status bar.](https://reactnative.dev/docs/statusbar)Is this page useful?

---

# Debugging Native Code

> Projects with Native Code Only

### Projects with Native Code Only

The following section only applies to projects with native code exposed. If you are using the managed Expo workflow, see the guide on [prebuild](https://docs.expo.dev/workflow/prebuild/) to use this API.

## Accessing Logs​

You can display the native logs for an iOS or Android app by using the following commands in a terminal while the app is running:

 shell

```
# For Android:npx react-native log-android# Or, for iOS:npx react-native log-ios
```

You may also access these through Debug > Open System Log… in the iOS Simulator or by running `adb logcat "*:S" ReactNative:V ReactNativeJS:V` in a terminal while an Android app is running on a device or emulator.

 **💡 Custom Native Logs**

If you are writing a Native Module and want to add custom logs to your module for debugging purposes, you can use the following method:

#### Android (Java/Kotlin)​

In your native module, use the `Log` class to add logs that can be viewed in Logcat:

java

```
import android.util.Log;private void log(String message) {    Log.d("YourModuleName", message);}
```

To view these logs in Logcat, use this command, replacing `YourModuleName` with your custom tag:

shell

```
adb logcat "*:S" ReactNative:V ReactNativeJS:V YourModuleName:D
```

#### iOS (Objective-C/Swift)​

In your native module, use `NSLog` for custom logs:

objective-c

```
NSLog(@"YourModuleName: %@", message);
```

Or, in Swift:

swift

```
print("YourModuleName: \(message)")
```

These logs will appear in the Xcode console when running the app.

## Debugging in a Native IDE​

When working with native code, such as when writing native modules, you can launch the app from Android Studio or Xcode and take advantage of the native debugging features (setting up breakpoints, etc.) as you would in case of building a standard native app.

Another option is to run your application using the React Native CLI and attach the native debugger of the native IDE (Android Studio or Xcode) to the process.

### Android Studio​

On Android Studio you can do this by going on the "Run" option on the menu bar, clicking on "Attach to Process..." and selecting the running React Native app.

### Xcode​

On Xcode click on "Debug" on the top menu bar, select the "Attach to process" option, and select the application in the list of "Likely Targets".

Is this page useful?

---

# Debugging Release Builds

> Symbolicating a stack trace

## Symbolicating a stack trace​

If a React Native app throws an unhandled exception in a release build, the output may be obfuscated and hard to read.

 shell

```
07-15 10:58:25.820 18979 18998 E AndroidRuntime: FATAL EXCEPTION: mqt_native_modules07-15 10:58:25.820 18979 18998 E AndroidRuntime: Process: com.awesomeproject, PID: 18979 07-15 10:58:25.820 18979 18998 E AndroidRuntime: com.facebook.react.common.JavascriptException: Failed, js engine: hermes, stack:07-15 10:58:25.820 18979 18998 E AndroidRuntime: p@1:13216107-15 10:58:25.820 18979 18998 E AndroidRuntime: p@1:13208407-15 10:58:25.820 18979 18998 E AndroidRuntime: f@1:13185407-15 10:58:25.820 18979 18998 E AndroidRuntime: anonymous@1:131119
```

In the above stack trace, entries like `p@1:132161` are minified function names and bytecode offsets. To debug these calls, we want to translate these into file, line, and function name, e.g. `AwesomeProject/App.js:54:initializeMap`. This is known as **symbolication.**

You can symbolicate minified function names and bytecode like the above by passing the stack trace and a generated source map to [metro-symbolicate](https://www.npmjs.com/package/metro-symbolicate).

### Enabling source maps​

Source maps are required to symbolicate stack traces. Make sure that source maps are enabled within the build config for the target platform.

info

On Android, source maps are **enabled** by default.

To enable source map generation, ensure the following `hermesFlags` are present in `android/app/build.gradle`.

groovy

```
react {    hermesFlags = ["-O", "-output-source-map"]}
```

If done correctly you should see the output location of the source map during Metro build output.

text

```
Writing bundle output to:, android/app/build/generated/assets/react/release/index.android.bundleWriting sourcemap output to:, android/app/build/intermediates/sourcemaps/react/release/index.android.bundle.packager.map
```

info

On iOS, source maps are **disabled** by default. Use the following instructions to enable them.

To enable source map generation:

- Open Xcode and edit the build phase "Bundle React Native code and images".
- Above the other exports, add a `SOURCEMAP_FILE` entry with the desired output path.

diff

```
+ export SOURCEMAP_FILE="$(pwd)/../main.jsbundle.map"  WITH_ENVIRONMENT="../node_modules/react-native/scripts/xcode/with-environment.sh"
```

If done correctly you should see the output location of the source map during Metro build output.

text

```
Writing bundle output to:, Build/Intermediates.noindex/ArchiveIntermediates/application/BuildProductsPath/Release-iphoneos/main.jsbundleWriting sourcemap output to:, Build/Intermediates.noindex/ArchiveIntermediates/application/BuildProductsPath/Release-iphoneos/main.jsbundle.map
```

### Usingmetro-symbolicate​

With source maps being generated, we can now translate our stack traces.

 shell

```
# Print usage instructionsnpx metro-symbolicate# From a file containing the stack tracenpx metro-symbolicate android/app/build/generated/sourcemaps/react/release/index.android.bundle.map < stacktrace.txt# From adb logcat (Android)adb logcat -d | npx metro-symbolicate android/app/build/generated/sourcemaps/react/release/index.android.bundle.map
```

### Notes on source maps​

- Multiple source maps may be generated by the build process. Make sure to use the one in the location shown in the examples.
- Make sure that the source map you use corresponds to the exact commit of the crashing app. Small changes in source code can cause large differences in offsets.
- If `metro-symbolicate` exits immediately with success, make sure the input comes from a pipe or redirection and not from a terminal.

Is this page useful?

---

# Debugging Basics

> Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.

note

Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.

## Opening the Dev Menu​

React Native provides an in-app developer menu providing access to debugging features. You can access the Dev Menu by shaking your device or via keyboard shortcuts:

- iOS Simulator: Ctrl + Cmd ⌘ + Z (or Device > Shake)
- Android emulators: Cmd ⌘ + M (macOS) or Ctrl + M (Windows and Linux)

Alternative (Android): `adb shell input keyevent 82`.

![The React Native Dev Menu](https://reactnative.dev/assets/images/debugging-dev-menu-083-70616da2986550a977feb0158f218bdd.jpg)

## Opening DevTools​

[React Native DevTools](https://reactnative.dev/docs/react-native-devtools) is our built-in debugger for React Native. It allows you to inspect and understand how your JavaScript code is running, similar to a web browser.

To open DevTools, either:

- Select "Open DevTools" in the Dev Menu.
- Press j from the CLI.

![React Native DevTools opened to the &quot;Welcome&quot; pane](https://reactnative.dev/assets/images/debugging-rndt-welcome-083-9f56f0124de2d2607022330b0ce41d85.jpg)

On first launch, DevTools will open to a welcome panel, along with an open console drawer where you can view logs and interact with the JavaScript runtime. From the top of the window, you can navigate to other panels, including the integrated React Components Inspector and Profiler.

Learn more in our [React Native DevTools guide](https://reactnative.dev/docs/react-native-devtools).

## LogBox​

LogBox is an in-app tool that displays when warnings or errors are logged by your app.

![A LogBox warning and an expanded LogBox syntax error](https://reactnative.dev/assets/images/debugging-logbox-076-0191f48c03cc7b550d749c4f100fab47.jpg)

### Fatal Errors​

When an unrecoverable error occurs, such as a JavaScript syntax error, LogBox will open with the location of the error. In this state, LogBox is not dismissable since your code cannot be executed. LogBox will automatically dismiss once the syntax error is fixed — either via Fast Refresh or after a manual reload.

### Console Errors and Warnings​

Console errors and warnings are displayed as on-screen notifications with a red or yellow badge.

- **Errors** will display with a notification count. Tap the notification to see an expanded view and to paginate through other logs.
- **Warnings** will display a notification banner without details, prompting you to open React Native DevTools.

When React Native DevTools is open, all errors except fatal errors will be hidden to LogBox. We recommend using the Console panel within React Native DevTools as a source of truth, due to various LogBox options which can hide or adjust the level of certain logs.

 **💡 Ignoring logs**

LogBox can be configured via the `LogBox` API.

js

```
import {LogBox} from 'react-native';
```

#### Ignore all logs​

LogBox notifications can be disabled using `LogBox.ignoreAllLogs()`. This can be useful in situations such as giving product demos.

js

```
LogBox.ignoreAllLogs();
```

#### Ignore specific logs​

Notifications can be disabled on a per-log basis via `LogBox.ignoreLogs()`. This can be useful for noisy warnings or those that cannot be fixed, e.g. in a third-party dependency.

js

```
LogBox.ignoreLogs([  // Exact message  'Warning: componentWillReceiveProps has been renamed',  // Substring or regex match  /GraphQL error: .*/,]);
```

note

LogBox will treat certain errors from React as warnings, which will mean they don't display as an in-app error notification. Advanced users can change this behaviour by customising LogBox's warning filter using [LogBoxData.setWarningFilter()](https://github.com/facebook/react-native/blob/d334f4d77eea538dff87fdcf2ebc090246cfdbb0/packages/react-native/Libraries/LogBox/Data/LogBoxData.js#L338).

## Performance Monitor​

On Android and iOS, an in-app performance overlay can be toggled during development by selecting **"Perf Monitor"** in the Dev Menu. Learn more about this feature [here](https://reactnative.dev/docs/performance).

![The Performance Monitor overlay on iOS and Android](https://reactnative.dev/assets/images/debugging-performance-monitor-3e0023c343ba59b5f62e563a4aa2741a.jpg)

 info

The Performance Monitor runs in-app and is a guide. We recommend investigating the native tooling under Android Studio and Xcode for accurate performance measurements.

---

# DevSettings

> The DevSettings module exposes methods for customizing settings for developers in development.

The `DevSettings` module exposes methods for customizing settings for developers in development.

---

# Reference

## Methods​

### addMenuItem()​

 tsx

```
static addMenuItem(title: string, handler: () => any);
```

Add a custom menu item to the Dev Menu.

**Parameters:**

| Name | Type |
| --- | --- |
| titleRequired | string |
| handlerRequired | function |

**Example:**

 tsx

```
DevSettings.addMenuItem('Show Secret Dev Screen', () => {  Alert.alert('Showing secret dev screen!');});
```

---

### reload()​

 tsx

```
static reload(reason?: string): void;
```

Reload the application. Can be invoked directly or on user interaction.

**Example:**

 tsx

```
<Button title="Reload" onPress={() => DevSettings.reload()} />
```

Is this page useful?

---

# Dimensions

> useWindowDimensions is the preferred API for React components. Unlike Dimensions, it updates as the window's dimensions update. This works nicely with the React paradigm.

info

[useWindowDimensions](https://reactnative.dev/docs/usewindowdimensions) is the preferred API for React components. Unlike `Dimensions`, it updates as the window's dimensions update. This works nicely with the React paradigm.

 tsx

```
import {Dimensions} from 'react-native';
```

You can get the application window's width and height using the following code:

 tsx

```
const windowWidth = Dimensions.get('window').width;const windowHeight = Dimensions.get('window').height;
```

 note

Although dimensions are available immediately, they may change (e.g due to device rotation, foldable devices etc) so any rendering logic or styles that depend on these constants should try to call this function on every render, rather than caching the value (for example, using inline styles rather than setting a value in a `StyleSheet`).

If you are targeting foldable devices or devices which can change the screen size or app window size, you can use the event listener available in the Dimensions module as shown in the below example.

## Example​

# Reference

## Methods​

### addEventListener()​

 tsx

```
static addEventListener(  type: 'change',  handler: ({    window,    screen,  }: DimensionsValue) => void,): EmitterSubscription;
```

Add an event handler. Supported events:

- `change`: Fires when a property within the `Dimensions` object changes. The argument to the event handler is a [DimensionsValue](#dimensionsvalue) type object.

---

### get()​

 tsx

```
static get(dim: 'window' | 'screen'): ScaledSize;
```

Initial dimensions are set before `runApplication` is called so they should be available before any other require's are run, but may be updated later.

Example: `const {height, width} = Dimensions.get('window');`

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| dimRequired | string | Name of dimension as defined when callingset. Returns value for the dimension. |

 note

For Android the `window` dimension will be reduced by the size of status bar (if not translucent) and bottom navigation bar.

## Type Definitions​

### DimensionsValue​

**Properties:**

| Name | Type | Description |
| --- | --- | --- |
| window | ScaledSize | Size of the visible Application window. |
| screen | ScaledSize | Size of the device's screen. |

### ScaledSize​

| Type |
| --- |
| object |

**Properties:**

| Name | Type |
| --- | --- |
| width | number |
| height | number |
| scale | number |
| fontScale | number |

Is this page useful?

---

# Document nodes

> Document nodes represent a complete native view tree. Apps using native navigation would provide a separate document node for each screen. Apps not using native navigation would generally provide a single document for the whole app (similar to single-page apps on Web).

Document nodes represent a complete native view tree. Apps using native navigation would provide a separate document node for each screen. Apps not using native navigation would generally provide a single document for the whole app (similar to single-page apps on Web).

---

## Reference​

### Web-compatible API​

From [Document](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement):

- Properties
  - [childElementCount](https://developer.mozilla.org/en-US/docs/Web/API/Document/childElementCount)
  - [children](https://developer.mozilla.org/en-US/docs/Web/API/Document/children)
  - [documentElement](https://developer.mozilla.org/en-US/docs/Web/API/Document/documentElement)
  - [firstElementChild](https://developer.mozilla.org/en-US/docs/Web/API/Document/firstElementChild)
  - [lastElementChild](https://developer.mozilla.org/en-US/docs/Web/API/Document/lastElementChild)
- Methods
  - [getElementById()](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById)

From [Node](https://developer.mozilla.org/en-US/docs/Web/API/Node):

- Properties
  - [childNodes](https://developer.mozilla.org/en-US/docs/Web/API/Node/childNodes)
  - [firstChild](https://developer.mozilla.org/en-US/docs/Web/API/Node/firstChild)
  - [isConnected](https://developer.mozilla.org/en-US/docs/Web/API/Node/isConnected)
  - [lastChild](https://developer.mozilla.org/en-US/docs/Web/API/Node/lastChild)
  - [nextSibling](https://developer.mozilla.org/en-US/docs/Web/API/Node/nextSibling)
  - [nodeName](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeName)
  - [nodeType](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType)
  - [nodeValue](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeValue)
  - [ownerDocument](https://developer.mozilla.org/en-US/docs/Web/API/Node/ownerDocument)
  - [parentElement](https://developer.mozilla.org/en-US/docs/Web/API/Node/parentElement)
  - [parentNode](https://developer.mozilla.org/en-US/docs/Web/API/Node/parentNode)
  - [previousSibling](https://developer.mozilla.org/en-US/docs/Web/API/Node/previousSibling)
  - [textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
- Methods
  - [compareDocumentPosition()](https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition)
  - [contains()](https://developer.mozilla.org/en-US/docs/Web/API/Node/contains)
  - [getRootNode()](https://developer.mozilla.org/en-US/docs/Web/API/Node/getRootNode)
  - [hasChildNodes()](https://developer.mozilla.org/en-US/docs/Web/API/Node/hasChildNodes)

Is this page useful?

---

# DrawerLayoutAndroid

> React component that wraps the platform DrawerLayout (Android only). The Drawer (typically used for navigation) is rendered with renderNavigationView and direct children are the main view (where your content goes). The navigation view is initially not visible on the screen, but can be pulled in from the side of the window specified by the drawerPosition prop and its width can be set by the drawerWidth prop.

React component that wraps the platform `DrawerLayout` (Android only). The Drawer (typically used for navigation) is rendered with `renderNavigationView` and direct children are the main view (where your content goes). The navigation view is initially not visible on the screen, but can be pulled in from the side of the window specified by the `drawerPosition` prop and its width can be set by the `drawerWidth` prop.

## Example​

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### drawerBackgroundColor​

Specifies the background color of the drawer. The default value is `white`. If you want to set the opacity of the drawer, use rgba. Example:

 tsx

```
return (  <DrawerLayoutAndroid drawerBackgroundColor="rgba(0,0,0,0.5)" />);
```

| Type | Required |
| --- | --- |
| color | No |

---

### drawerLockMode​

Specifies the lock mode of the drawer. The drawer can be locked in 3 states:

- unlocked (default), meaning that the drawer will respond (open/close) to touch gestures.
- locked-closed, meaning that the drawer will stay closed and not respond to gestures.
- locked-open, meaning that the drawer will stay opened and not respond to gestures. The drawer may still be opened and closed programmatically (`openDrawer`/`closeDrawer`).

| Type | Required |
| --- | --- |
| enum('unlocked', 'locked-closed', 'locked-open') | No |

---

### drawerPosition​

Specifies the side of the screen from which the drawer will slide in. By default it is set to `left`.

| Type | Required |
| --- | --- |
| enum('left', 'right') | No |

---

### drawerWidth​

Specifies the width of the drawer, more precisely the width of the view that be pulled in from the edge of the window.

| Type | Required |
| --- | --- |
| number | No |

---

### keyboardDismissMode​

Determines whether the keyboard gets dismissed in response to a drag.

- 'none' (the default), drags do not dismiss the keyboard.
- 'on-drag', the keyboard is dismissed when a drag begins.

| Type | Required |
| --- | --- |
| enum('none', 'on-drag') | No |

---

### onDrawerClose​

Function called whenever the navigation view has been closed.

| Type | Required |
| --- | --- |
| function | No |

---

### onDrawerOpen​

Function called whenever the navigation view has been opened.

| Type | Required |
| --- | --- |
| function | No |

---

### onDrawerSlide​

Function called whenever there is an interaction with the navigation view.

| Type | Required |
| --- | --- |
| function | No |

---

### onDrawerStateChanged​

Function called when the drawer state has changed. The drawer can be in 3 states:

- idle, meaning there is no interaction with the navigation view happening at the time
- dragging, meaning there is currently an interaction with the navigation view
- settling, meaning that there was an interaction with the navigation view, and the navigation view is now finishing its closing or opening animation

| Type | Required |
| --- | --- |
| function | No |

---

### renderNavigationView​

The navigation view that will be rendered to the side of the screen and can be pulled in.

| Type | Required |
| --- | --- |
| function | Yes |

---

### statusBarBackgroundColor​

Make the drawer take the entire screen and draw the background of the status bar to allow it to open over the status bar. It will only have an effect on API 21+.

| Type | Required |
| --- | --- |
| color | No |

## Methods​

### closeDrawer()​

 tsx

```
closeDrawer();
```

Closes the drawer.

---

### openDrawer()​

 tsx

```
openDrawer();
```

Opens the drawer.

Is this page useful?

---

# DropShadowValue Object Type

> The DropShadowValue object is taken by the filter style prop for the dropShadow function. It is comprised of 2 or 3 lengths and an optional color. These values collectively define the drop shadow's color, position, and blurriness.

The `DropShadowValue` object is taken by the [filter](https://reactnative.dev/docs/view-style-props#filter) style prop for the `dropShadow` function. It is comprised of 2 or 3 lengths and an optional color. These values collectively define the drop shadow's color, position, and blurriness.

## Example​

 js

```
{  offsetX: 10,  offsetY: -3,  standardDeviation: '15px',  color: 'blue',}
```

## Keys and values​

### offsetX​

The offset on the x-axis. This can be positive or negative. A positive value indicates right and negative indicates left.

| Type | Optional |
| --- | --- |
| number | string | No |

### offsetY​

The offset on the y-axis. This can be positive or negative. A positive value indicates up and negative indicates down.

| Type | Optional |
| --- | --- |
| number | string | No |

### standardDeviation​

Represents the standard deviation used in the [Gaussian blur](https://en.wikipedia.org/wiki/Gaussian_blur) algorithm. The larger the value the blurrier the shadow is. Only non-negative values are valid. The default is 0.

| Type | Optional |
| --- | --- |
| number | string | Yes |

### color​

The color of the shadow. The default is `black`.

| Type | Optional |
| --- | --- |
| color | Yes |

## Used by​

- [filter](https://reactnative.dev/docs/view-style-props#filter)

Is this page useful?

---

# DynamicColorIOS

> The DynamicColorIOS function is a platform color type specific to iOS.

The `DynamicColorIOS` function is a platform color type specific to iOS.

 tsx

```
DynamicColorIOS({  light: color,  dark: color,  highContrastLight: color, // (optional) will fallback to "light" if not provided  highContrastDark: color, // (optional) will fallback to "dark" if not provided});
```

`DynamicColorIOS` takes a single argument as an object with two mandatory keys: `dark` and `light`, and two optional keys `highContrastLight` and `highContrastDark`. These correspond to the colors you want to use for "light mode" and "dark mode" on iOS, and when high contrast accessibility mode is enabled, high contrast version of them.

At runtime, the system will choose which of the colors to display depending on the current system appearance and accessibility settings. Dynamic colors are useful for branding colors or other app specific colors that still respond automatically to system setting changes.

#### Developer notes​

info

If you’re familiar with `@media (prefers-color-scheme: dark)` in CSS, this is similar! Only instead of defining all the colors in a media query, you define which color to use under what circumstances right there where you're using it. Neat!

info

The `DynamicColorIOS` function is similar to the iOS native methods [UIColor colorWithDynamicProvider:](https://developer.apple.com/documentation/uikit/uicolor/3238040-colorwithdynamicprovider).

## Example​

 tsx

```
import {DynamicColorIOS} from 'react-native';const customDynamicTextColor = DynamicColorIOS({  dark: 'lightskyblue',  light: 'midnightblue',});const customContrastDynamicTextColor = DynamicColorIOS({  dark: 'darkgray',  light: 'lightgray',  highContrastDark: 'black',  highContrastLight: 'white',});
```

Is this page useful?
