# Linking and more

# Linking

> Linking gives you a general interface to interact with both incoming and outgoing app links.

`Linking` gives you a general interface to interact with both incoming and outgoing app links.

Every Link (URL) has a URL Scheme, some websites are prefixed with `https://` or `http://` and the `http` is the URL Scheme. Let's call it scheme for short.

In addition to `https`, you're likely also familiar with the `mailto` scheme. When you open a link with the mailto scheme, your operating system will open an installed mail application. Similarly, there are schemes for making phone calls and sending SMS. Read more about [built-in URL](#built-in-url-schemes) schemes below.

Like using the mailto scheme, it's possible to link to other applications by using custom url schemes. For example, when you get a **Magic Link** email from Slack, the **Launch Slack** button is an anchor tag with an href that looks something like: `slack://secret/magic-login/other-secret`. Like with Slack, you can tell the operating system that you want to handle a custom scheme. When the Slack app opens, it receives the URL that was used to open it. This is often referred to as deep linking. Read more about how to [get the deep link](#get-the-deep-link) into your app.

A custom URL scheme isn't the only way to open your application on mobile. For example, if you want to email someone a link to be opened on mobile, using a custom URL scheme isn't ideal because the user might open the email on a desktop, where the link wouldn't work. Instead, you should use standard `https` links, such as `https://www.myapp.io/records/1234546`. On mobile, these links can be configured to open your app. On Android, this feature is called **Deep Links**, while on iOS, it is known as **Universal Links**.

### Built-in URL Schemes​

As mentioned in the introduction, there are some URL schemes for core functionality that exist on every platform. The following is a non-exhaustive list, but covers the most commonly used schemes.

| Scheme | Description | iOS | Android |
| --- | --- | --- | --- |
| mailto | Open mail app, eg: mailto:hello@world.dev | ✅ | ✅ |
| tel | Open phone app, eg: tel:+123456789 | ✅ | ✅ |
| sms | Open SMS app, eg: sms:+123456789 | ✅ | ✅ |
| https/http | Open web browser app, eg:https://expo.dev | ✅ | ✅ |

### Enabling Deep Links​

### Projects with Native Code Only

The following section only applies to projects with native code exposed. If you are using the managed Expo workflow, see the guide on [Linking](https://docs.expo.dev/guides/linking/) in the Expo documentation for the appropriate alternative.

If you want to enable deep links in your app, please read the below guide:

info

For instructions on how to add support for deep linking on Android, refer to [Enabling Deep Links for App Content - Add Intent Filters for Your Deep Links](https://developer.android.com/training/app-indexing/deep-linking.html#adding-filters).

If you wish to receive the intent in an existing instance of MainActivity, you may set the `launchMode` of MainActivity to `singleTask` in `AndroidManifest.xml`. See [<activity>](https://developer.android.com/guide/topics/manifest/activity-element.html) documentation for more information.

xml

```
<activity  android:name=".MainActivity"  android:launchMode="singleTask">
```

note

On iOS, you'll need to add the `LinkingIOS` folder into your header search paths as described in step 3 [here](https://reactnative.dev/docs/linking-libraries-ios#step-3). If you also want to listen to incoming app links during your app's execution, you'll need to add the following lines to your `*AppDelegate.m`:

AppDelegate.mm

```
// iOS 9.x or newer#import <React/RCTLinkingManager.h>- (BOOL)application:(UIApplication *)application   openURL:(NSURL *)url   options:(NSDictionary<UIApplicationOpenURLOptionsKey,id> *)options{  return [RCTLinkingManager application:application openURL:url options:options];}
```

If your app is using [Universal Links](https://developer.apple.com/ios/universal-links/), you'll need to add the following code as well:

AppDelegate.mm

```
- (BOOL)application:(UIApplication *)application continueUserActivity:(nonnull NSUserActivity *)userActivity restorationHandler:(nonnull void (^)(NSArray<id<UIUserActivityRestoring>> * _Nullable))restorationHandler{ return [RCTLinkingManager application:application                  continueUserActivity:userActivity                    restorationHandler:restorationHandler];}
```

AppDelegate.swift

```
override func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {  return RCTLinkingManager.application(app, open: url, options: options)}
```

If your app is using [Universal Links](https://developer.apple.com/ios/universal-links/), you'll need to add the following code as well:

AppDelegate.swift

```
override func application(  _ application: UIApplication,  continue userActivity: NSUserActivity,  restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {    return RCTLinkingManager.application(      application,      continue: userActivity,      restorationHandler: restorationHandler    )  }
```

### Handling Deep Links​

There are two ways to handle URLs that open your app.

#### 1. If the app is already open, the app is foregrounded and a Linking 'url' event is fired​

You can handle these events with `Linking.addEventListener('url', callback)` - it calls `callback({url})` with the linked URL

#### 2. If the app is not already open, it is opened and the url is passed in as the initialURL​

You can handle these events with `Linking.getInitialURL()` - it returns a Promise that resolves to the URL, if there is one.

---

## Example​

### Open Links and Deep Links (Universal Links)​

### Open Custom Settings​

### Get the Deep Link​

### Send Intents (Android)​

# Reference

## Methods​

### addEventListener()​

 tsx

```
static addEventListener(  type: 'url',  handler: (event: {url: string}) => void,): EmitterSubscription;
```

Add a handler to Linking changes by listening to the `url` event type and providing the handler.

---

### canOpenURL()​

 tsx

```
static canOpenURL(url: string): Promise<boolean>;
```

Determine whether or not an installed app can handle a given URL.

The method returns a `Promise` object. When it is determined whether or not the given URL can be handled, the promise is resolved and the first parameter is whether or not it can be opened.

The `Promise` will reject on Android if it was impossible to check if the URL can be opened or when targeting Android 11 (SDK 30) if you didn't specify the relevant intent queries in `AndroidManifest.xml`. Similarly on iOS, the promise will reject if you didn't add the specific scheme in the `LSApplicationQueriesSchemes` key inside `Info.plist` (see bellow).

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| urlRequired | string | The URL to open. |

 note

For web URLs, the protocol (`"http://"`, `"https://"`) must be set accordingly!

 warning

This method has limitations on iOS 9+. From [the official Apple documentation](https://developer.apple.com/documentation/uikit/uiapplication/1622952-canopenurl):

- If your app is linked against an earlier version of iOS but is running in iOS 9.0 or later, you can call this method up to 50 times. After reaching that limit, subsequent calls always resolve to `false`. If the user reinstalls or upgrades the app, iOS resets the limit.
- As of iOS 9, your app also needs to provide the `LSApplicationQueriesSchemes` key inside `Info.plist` or `canOpenURL()` will always resolve to `false`.

 info

When targeting Android 11 (SDK 30) you must specify the intents for the schemes you want to handle in `AndroidManifest.xml`. A list of common intents can be found [here](https://developer.android.com/guide/components/intents-common).

For example to handle `https` schemes the following needs to be added to your manifest:

```
<manifest ...>  <queries>    <intent>      <action android:name="android.intent.action.VIEW" />      <data android:scheme="https"/>    </intent>  </queries></manifest>
```

---

### getInitialURL()​

 tsx

```
static getInitialURL(): Promise<string | null>;
```

If the app launch was triggered by an app link, it will give the link url, otherwise it will give `null`.

 info

To support deep linking on Android, refer [https://developer.android.com/training/app-indexing/deep-linking.html#handling-intents](https://developer.android.com/training/app-indexing/deep-linking.html#handling-intents).

 tip

`getInitialURL` may return `null` when Remote JS Debugging is active. Disable the debugger to ensure it gets passed.

---

### openSettings()​

 tsx

```
static openSettings(): Promise<void>;
```

Open the Settings app and displays the app’s custom settings, if it has any.

---

### openURL()​

 tsx

```
static openURL(url: string): Promise<any>;
```

Try to open the given `url` with any of the installed apps.

You can use other URLs, like a location (e.g. "geo:37.484847,-122.148386" on Android or "[https://maps.apple.com/?ll=37.484847,-122.148386](https://maps.apple.com/?ll=37.484847,-122.148386)" on iOS), a contact, or any other URL that can be opened with the installed apps.

The method returns a `Promise` object. If the user confirms the open dialog or the url automatically opens, the promise is resolved. If the user cancels the open dialog or there are no registered applications for the url, the promise is rejected.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| urlRequired | string | The URL to open. |

 note

This method will fail if the system doesn't know how to open the specified URL. If you're passing in a non-http(s) URL, it's best to check `canOpenURL()` first. For web URLs, the protocol (`"http://"`, `"https://"`) must be set accordingly!

 warning

This method may behave differently in a simulator e.g. `"tel:"` links are not able to be handled in the iOS simulator as there's no access to the dialer app.

---

### sendIntent()Android​

 tsx

```
static sendIntent(  action: string,  extras?: Array<{key: string; value: string | number | boolean}>,): Promise<void>;
```

Launch an Android intent with extras.

**Parameters:**

| Name | Type |
| --- | --- |
| actionRequired | string |
| extras | Array<{key: string, value: string ｜ number ｜ boolean}> |

Is this page useful?

---

# Metro

> React Native uses Metro to build your JavaScript code and assets.

React Native uses [Metro](https://metrobundler.dev/) to build your JavaScript code and assets.

## Configuring Metro​

Configuration options for Metro can be customized in your project's `metro.config.js` file. This can export either:

- **An object (recommended)** that will be merged on top of Metro's internal config defaults.
- [A function](#advanced-using-a-config-function) that will be called with Metro's internal config defaults and should return a final config object.

 tip

Please see [Configuring Metro](https://metrobundler.dev/docs/configuration) on the Metro website for documentation on all available config options.

In React Native, your Metro config should extend either [@react-native/metro-config](https://www.npmjs.com/package/@react-native/metro-config) or [@expo/metro-config](https://www.npmjs.com/package/@expo/metro-config). These packages contain essential defaults necessary to build and run React Native apps.

Below is the default `metro.config.js` file in a React Native template project:

 js

```
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');/** * Metro configuration * https://metrobundler.dev/docs/configuration * * @type {import('metro-config').MetroConfig} */const config = {};module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

Metro options you wish to customize can be done so within the `config` object.

### Advanced: Using a config function​

Exporting a config function is an opt-in to managing the final config yourself — **Metro will not apply any internal defaults**. This pattern can be useful when needing to read the base default config object from Metro or to set options dynamically.

 info

**From@react-native/metro-config0.72.1**, it is no longer necessary to use a config function to access the complete default config. See the **Tip** section below.

 js

```
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');module.exports = function (baseConfig) {  const defaultConfig = mergeConfig(baseConfig, getDefaultConfig(__dirname));  const {resolver: {assetExts, sourceExts}} = defaultConfig;  return mergeConfig(    defaultConfig,    {      resolver: {        assetExts: assetExts.filter(ext => ext !== 'svg'),        sourceExts: [...sourceExts, 'svg'],      },    },  );};
```

 tip

Using a config function is for advanced use cases. A simpler method than the above, e.g. for customising `sourceExts`, would be to read these defaults from `@react-native/metro-config`.

**Alternative**

js

```
const defaultConfig = getDefaultConfig(__dirname);const config = {  resolver: {    sourceExts: [...defaultConfig.resolver.sourceExts, 'svg'],  },};module.exports = mergeConfig(defaultConfig, config);
```

**However!**, we recommend copying and editing when overriding these config values — placing the source of truth in your config file.

✅ **Recommended**

js

```
const config = {  resolver: {    sourceExts: ['js', 'ts', 'tsx', 'svg'],  },};
```

## Learn more about Metro​

- [Metro website](https://metrobundler.dev/)
- [Video: "Metro & React Native DevX" talk at App.js 2023](https://www.youtube.com/watch?v=c9D4pg0y9cI)

Is this page useful?

---

# Modal

> The Modal component is a basic way to present content above an enclosing view.

The Modal component is a basic way to present content above an enclosing view.

## Example​

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### 🗑️animated​

 Deprecated

Use the [animationType](https://reactnative.dev/docs/modal#animationtype) prop instead.

---

### animationType​

The `animationType` prop controls how the modal animates.

Possible values:

- `slide` slides in from the bottom
- `fade` fades into view
- `none` appears without an animation

| Type | Default |
| --- | --- |
| enum('none','slide','fade') | none |

---

### backdropColor​

The `backdropColor` of the modal (or background color of the modal's container.) Defaults to `white` if not provided and transparent is `false`. Ignored if `transparent` is `true`.

| Type | Default |
| --- | --- |
| color | white |

---

### hardwareAcceleratedAndroid​

The `hardwareAccelerated` prop controls whether to force hardware acceleration for the underlying window.

| Type | Default |
| --- | --- |
| bool | false |

---

### navigationBarTranslucentAndroid​

The `navigationBarTranslucent` prop determines whether your modal should go under the system navigation bar. However, `statusBarTranslucent` also needs to be set to `true` to make navigation bar translucent.

| Type | Default |
| --- | --- |
| bool | false |

---

### onDismissiOS​

The `onDismiss` prop allows passing a function that will be called once the modal has been dismissed.

| Type |
| --- |
| function |

---

### onOrientationChangeiOS​

The `onOrientationChange` callback is called when the orientation changes while the modal is being displayed. The orientation provided is only 'portrait' or 'landscape'. This callback is also called on initial render, regardless of the current orientation.

| Type |
| --- |
| function |

---

### allowSwipeDismissaliOS​

Controls whether the modal can be dismissed by swiping down on iOS.
This requires you to implement the `onRequestClose` prop to handle the dismissal.

| Type | Default |
| --- | --- |
| bool | false |

---

### ref​

A ref setter that will be assigned an [element node](https://reactnative.dev/docs/element-nodes) when mounted.

---

### onRequestClose​

The `onRequestClose` callback is called when the user taps the hardware back button on Android or the menu button on Apple TV. Because of this required prop, be aware that `BackHandler` events will not be emitted as long as the modal is open.
On iOS, this callback is called when a Modal is being dismissed using a drag gesture when `presentationStyle` is `pageSheet or formSheet`. When `allowSwipeDismissal` is enabled this callback will be called after dismissing the modal.

| Type |
| --- |
| functionRequiredAndroidTVfunctioniOS |

---

### onShow​

The `onShow` prop allows passing a function that will be called once the modal has been shown.

| Type |
| --- |
| function |

---

### presentationStyleiOS​

The `presentationStyle` prop controls how the modal appears (generally on larger devices such as iPad or plus-sized iPhones). See [https://developer.apple.com/reference/uikit/uimodalpresentationstyle](https://developer.apple.com/reference/uikit/uimodalpresentationstyle) for details.

Possible values:

- `fullScreen` covers the screen completely
- `pageSheet` covers portrait-width view centered (only on larger devices)
- `formSheet` covers narrow-width view centered (only on larger devices)
- `overFullScreen` covers the screen completely, but allows transparency

| Type | Default |
| --- | --- |
| enum('fullScreen','pageSheet','formSheet','overFullScreen') | fullScreeniftransparent={false}overFullScreeniftransparent={true} |

---

### statusBarTranslucentAndroid​

The `statusBarTranslucent` prop determines whether your modal should go under the system statusbar.

| Type | Default |
| --- | --- |
| bool | false |

---

### supportedOrientationsiOS​

The `supportedOrientations` prop allows the modal to be rotated to any of the specified orientations. On iOS, the modal is still restricted by what's specified in your app's Info.plist's UISupportedInterfaceOrientations field.

 note

When using `presentationStyle` of `pageSheet` or `formSheet`, this property will be ignored on iOS.

| Type | Default |
| --- | --- |
| array of enums('portrait','portrait-upside-down','landscape','landscape-left','landscape-right') | ['portrait'] |

---

### transparent​

The `transparent` prop determines whether your modal will fill the entire view. Setting this to `true` will render the modal over a transparent background.

| Type | Default |
| --- | --- |
| bool | false |

---

### visible​

The `visible` prop determines whether your modal is visible.

| Type | Default |
| --- | --- |
| bool | true |

Is this page useful?

---

# More Resources

> There’s always more to learn: developer workflows, shipping to app stores, internationalization, security and more.

There’s always more to learn: developer workflows, shipping to app stores, internationalization, security and more.

## Where to go from here​

- [Set up your environment](https://reactnative.dev/docs/environment-setup)
- [Set up your development workflow](https://reactnative.dev/docs/running-on-device)
- [Design and layout your app](https://reactnative.dev/docs/flexbox)
- [Debug your app](https://reactnative.dev/docs/debugging)
- [Make your app cross platform](https://reactnative.dev/docs/platform-specific-code)
- [Get involved in the React Native community](https://reactnative.dev/community/overview)

## Dive deep​

- [React’s Documentation](https://react.dev/learn)
- [MDN’s JavaScript tutorials, reference, and guides](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Android](https://developer.android.com/docs) and [iOS](https://developer.apple.com/documentation/uikit) platform docs

## IDEs​

We recommend using the [VS Code](https://code.visualstudio.com/) code editor and its handy [React Native tools](https://marketplace.visualstudio.com/items?itemName=msjsdiag.vscode-react-native).

## Platforms to try​

[Expo](https://docs.expo.dev/) is a framework of tools and services for React Native that focuses on helping you build, ship, and iterate on your app, to use preview deployment workflows that are popular with web development, and to automate your development workflows. Expo also makes it possible to build React Native apps without ever touching Xcode or Android Studio, and it doesn't get in the way if you want to use those tools.

[Ignite](https://github.com/infinitered/ignite) is a starter kit CLI with several React Native boilerplates. The latest, Ignite Maverick, uses MobX-State-Tree for state management, React Navigation, and other common libraries. It has generators for screens, models, and more, and supports Expo out of the box. Ignite also comes with a component library that is tuned for custom designs, theming support, and testing. If you are looking for a preconfigured tech stack, Ignite could be perfect for you.

## Example Apps​

Try out apps from the [Showcase](https://reactnative.dev/showcase) to see what React Native is capable of! Looking for something more hands on? Check out this [set of example apps on GitHub](https://github.com/ReactNativeNews/React-Native-Apps). You can look at their source code—try running one on a simulator or device.

## Find, make, and share your own Native Components and TurboModules​

React Native has a community of thousands of developers like you making content, tools, tutorials—and Native Components!

Can’t find what you’re looking for in the Core Components? Visit [React Native Directory](https://reactnative.directory) to find what the community has been creating.

 caution

This documentation references a legacy set of API and needs to be updated to reflect the New Architecture

Interested in making your own Native Component or Module? Making modules for your own use case and sharing them with others on NPM and GitHub helps grow the React Native ecosystem and community! Read the guides to making your own Native Modules ([Android](https://reactnative.dev/docs/legacy/native-modules-android), [iOS](https://reactnative.dev/docs/legacy/native-modules-ios)) and Native Components ([Android](https://reactnative.dev/docs/legacy/native-components-android), [iOS](https://reactnative.dev/docs/legacy/native-components-ios)).

Is this page useful?

---

# Native Platform

> Your application may need access to platform features that aren’t directly available from react-native or one of the hundreds of third-party libraries maintained by the community. Maybe you want to reuse some existing Objective-C, Swift, Java, Kotlin or C++ code from the JavaScript runtime. Whatever your reason, React Native exposes a powerful set of API to connect your native code to your JavaScript application code.

Your application may need access to platform features that aren’t directly available from react-native or one of the hundreds of [third-party libraries](https://reactnative.directory/) maintained by the community. Maybe you want to reuse some existing Objective-C, Swift, Java, Kotlin or C++ code from the JavaScript runtime. Whatever your reason, React Native exposes a powerful set of API to connect your native code to your JavaScript application code.

This guide introduces:

- **Native Modules:** native libraries that have no User Interface (UI) for the user. Examples would be persistent storage, notifications, network events. These are accessible to your user as JavaScript functions and objects.
- **Native Component:** native platform views, widgets and controllers that are available to your application's JavaScript code through React Components.

 note

You might have previously been familiar with:

- [Legacy Native Modules](https://reactnative.dev/docs/legacy/native-modules-intro);
- [Legacy Native Components](https://reactnative.dev/docs/legacy/native-components-android);

These are our deprecated native module and component API. You can still use many of these legacy libraries with the New Architecture thanks to our interop layers. You should consider:

- using alternative libraries,
- upgrading to newer library versions that have first-class support for the New Architecture, or
- port these libraries yourself to Turbo Native Modules or Fabric Native Components.

1. Native Modules
  - [Android & iOS](https://reactnative.dev/docs/turbo-native-modules-introduction)
  - [Cross-Platform with C++](https://reactnative.dev/docs/the-new-architecture/pure-cxx-modules)
  - [Advanced: Custom C++ Types](https://reactnative.dev/docs/the-new-architecture/custom-cxx-types)
2. Fabric Native Components
  - [Android & iOS](https://reactnative.dev/docs/fabric-native-components-introduction)

Is this page useful?

---

# Navigating Between Screens

> Mobile apps are rarely made up of a single screen. Managing the presentation of, and transition between, multiple screens is typically handled by what is known as a navigator.

Mobile apps are rarely made up of a single screen. Managing the presentation of, and transition between, multiple screens is typically handled by what is known as a navigator.

This guide covers the various navigation components available in React Native. If you are getting started with navigation, you will probably want to use [React Navigation](https://reactnative.dev/docs/navigation#react-navigation). React Navigation provides a straightforward navigation solution, with the ability to present common stack navigation and tabbed navigation patterns on both Android and iOS.

If you're integrating React Native into an app that already manages navigation natively, or looking for an alternative to React Navigation, the following library provides native navigation on both platforms: [react-native-navigation](https://github.com/wix/react-native-navigation).

## React Navigation​

The community solution to navigation is a standalone library that allows developers to set up the screens of an app with a few lines of code.

### Starter template​

If you're starting a new project, you can use the React Navigation template to quickly set up a new project with [Expo](https://expo.dev/):

 shell

```
npx create-expo-app@latest --template react-navigation/template
```

See the project's `README.md` for more information on how to get started.

### Installation and setup​

First, you need to install them in your project:

 shell

```
npm install @react-navigation/native @react-navigation/native-stack
```

Next, install the required peer dependencies. You need to run different commands depending on whether your project is an Expo managed project or a bare React Native project.

- If you have an Expo managed project, install the dependencies with `expo`:
   shell
  ```
  npx expo install react-native-screens react-native-safe-area-context
  ```
- If you have a bare React Native project, install the dependencies with `npm`:
   shell
  ```
  npm install react-native-screens react-native-safe-area-context
  ```
  For iOS with bare React Native project, make sure you have [CocoaPods](https://cocoapods.org/) installed. Then install the pods to complete the installation:
   shell
  ```
  cd iospod installcd ..
  ```

Once you've installed and configured the dependencies, you can move on to setting up your project to use React Navigation.

When using React Navigation, you configure [navigators](https://reactnavigation.org/docs/glossary-of-terms#navigator) in your app. Navigators handle the transition between screens in your app and provide UI such as header, tab bar etc.

Now you are ready to build and run your app on the device/simulator.

### Usage​

Now you can create an app with a home screen and a profile screen:

 tsx

```
import * as React from 'react';import {createStaticNavigation} from '@react-navigation/native';import {createNativeStackNavigator} from '@react-navigation/native-stack';const RootStack = createNativeStackNavigator({  screens: {    Home: {      screen: HomeScreen,      options: {title: 'Welcome'},    },    Profile: {      screen: ProfileScreen,    },  },});const Navigation = createStaticNavigation(RootStack);export default function App() {  return <Navigation />;}
```

In this example, `RootStack` is a navigator with 2 screens (`Home` and `Profile`), defined in the `screens` property in `createNativeStackNavigator`. Similarly, you can define as many screens as you like.

You can specify options such as the screen title for each screen in the `options` property of each screen. Each screen definition also needs a `screen` property that is a React component or another navigator.

Inside each screen component, you can use the `useNavigation` hook to get the `navigation` object, which has various methods to link to other screens. For example, you can use `navigation.navigate` to go to the `Profile` screen:

 tsx

```
import {useNavigation} from '@react-navigation/native';function HomeScreen() {  const navigation = useNavigation();  return (    <Button      title="Go to Jane's profile"      onPress={() =>        navigation.navigate('Profile', {name: 'Jane'})      }    />  );}function ProfileScreen({route}) {  return <Text>This is {route.params.name}'s profile</Text>;}
```

This `native-stack` navigator uses the native APIs: `UINavigationController` on iOS and `Fragment` on Android so that navigation built with `createNativeStackNavigator` will behave the same and have the similar performance characteristics as apps built natively on top of those APIs.

React Navigation also has packages for different kind of navigators such as tabs and drawer. You can use them to implement various patterns in your app.

For a complete intro to React Navigation, follow the [React Navigation Getting Started Guide](https://reactnavigation.org/docs/getting-started).

Is this page useful?

---

# Networking

> Many mobile apps need to load resources from a remote URL. You may want to make a POST request to a REST API, or you may need to fetch a chunk of static content from another server.

Many mobile apps need to load resources from a remote URL. You may want to make a POST request to a REST API, or you may need to fetch a chunk of static content from another server.

## Using Fetch​

React Native provides the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) for your networking needs. Fetch will seem familiar if you have used `XMLHttpRequest` or other networking APIs before. You may refer to MDN's guide on [Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) for additional information.

### Making requests​

In order to fetch content from an arbitrary URL, you can pass the URL to fetch:

 tsx

```
fetch('https://mywebsite.com/mydata.json');
```

Fetch also takes an optional second argument that allows you to customize the HTTP request. You may want to specify additional headers, or make a POST request:

 tsx

```
fetch('https://mywebsite.com/endpoint/', {  method: 'POST',  headers: {    Accept: 'application/json',    'Content-Type': 'application/json',  },  body: JSON.stringify({    firstParam: 'yourValue',    secondParam: 'yourOtherValue',  }),});
```

Take a look at the [Fetch Request docs](https://developer.mozilla.org/en-US/docs/Web/API/Request) for a full list of properties.

### Handling the response​

The above examples show how you can make a request. In many cases, you will want to do something with the response.

Networking is an inherently asynchronous operation. Fetch method will return a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) that makes it straightforward to write code that works in an asynchronous manner:

 tsx

```
const getMoviesFromApi = () => {  return fetch('https://reactnative.dev/movies.json')    .then(response => response.json())    .then(json => {      return json.movies;    })    .catch(error => {      console.error(error);    });};
```

You can also use the `async` / `await` syntax in a React Native app:

 tsx

```
const getMoviesFromApiAsync = async () => {  try {    const response = await fetch(      'https://reactnative.dev/movies.json',    );    const json = await response.json();    return json.movies;  } catch (error) {    console.error(error);  }};
```

Don't forget to catch any errors that may be thrown by `fetch`, otherwise they will be dropped silently.

 info

By default, iOS 9.0 or later enforce App Transport Security (ATS). ATS requires any HTTP connection to use HTTPS. If you need to fetch from a cleartext URL (one that begins with `http`) you will first need to [add an ATS exception](https://reactnative.dev/docs/integration-with-existing-apps#test-your-integration). If you know ahead of time what domains you will need access to, it is more secure to add exceptions only for those domains; if the domains are not known until runtime you can [disable ATS completely](https://reactnative.dev/docs/publishing-to-app-store#1-enable-app-transport-security). Note however that from January 2017, [Apple's App Store review will require reasonable justification for disabling ATS](https://forums.developer.apple.com/thread/48979). See [Apple's documentation](https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW33) for more information.

 tip

On Android, as of API Level 28, clear text traffic is also blocked by default. This behaviour can be overridden by setting [android:usesCleartextTraffic](https://developer.android.com/guide/topics/manifest/application-element#usesCleartextTraffic) in the app manifest file.

## Using Other Networking Libraries​

The [XMLHttpRequest API](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) is built into React Native. This means that you can use third party libraries such as [frisbee](https://github.com/niftylettuce/frisbee) or [axios](https://github.com/axios/axios) that depend on it, or you can use the XMLHttpRequest API directly if you prefer.

 tsx

```
const request = new XMLHttpRequest();request.onreadystatechange = e => {  if (request.readyState !== 4) {    return;  }  if (request.status === 200) {    console.log('success', request.responseText);  } else {    console.warn('error');  }};request.open('GET', 'https://mywebsite.com/endpoint/');request.send();
```

 Caution

The security model for XMLHttpRequest is different than on web as there is no concept of [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) in native apps.

## WebSocket Support​

React Native also supports [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket), a protocol which provides full-duplex communication channels over a single TCP connection.

 tsx

```
const ws = new WebSocket('ws://host.com/path');ws.onopen = () => {  // connection opened  ws.send('something'); // send a message};ws.onmessage = e => {  // a message was received  console.log(e.data);};ws.onerror = e => {  // an error occurred  console.log(e.message);};ws.onclose = e => {  // connection closed  console.log(e.code, e.reason);};
```

## Known Issues withfetchand cookie based authentication​

The following options are currently not working with `fetch`

- `redirect:manual`
- `credentials:omit`

- Having same name headers on Android will result in only the latest one being present. A temporary solution can be found here: [https://github.com/facebook/react-native/issues/18837#issuecomment-398779994](https://github.com/facebook/react-native/issues/18837#issuecomment-398779994).
- Cookie based authentication is currently unstable. You can view some of the issues raised here: [https://github.com/facebook/react-native/issues/23185](https://github.com/facebook/react-native/issues/23185)
- As a minimum on iOS, when redirected through a `302`, if a `Set-Cookie` header is present, the cookie is not set properly. Since the redirect cannot be handled manually this might cause a scenario where infinite requests occur if the redirect is the result of an expired session.

## Configuring NSURLSession on iOS​

For some applications it may be appropriate to provide a custom `NSURLSessionConfiguration` for the underlying `NSURLSession` that is used for network requests in a React Native application running on iOS. For instance, one may need to set a custom user agent string for all network requests coming from the app or supply `NSURLSession` with an ephemeral `NSURLSessionConfiguration`. The function `RCTSetCustomNSURLSessionConfigurationProvider` allows for such customization. Remember to add the following import to the file in which `RCTSetCustomNSURLSessionConfigurationProvider` will be called:

 objectivec

```
#import <React/RCTHTTPRequestHandler.h>
```

`RCTSetCustomNSURLSessionConfigurationProvider` should be called early in the application life cycle such that it is readily available when needed by React, for instance:

 objectivec

```
-(void)application:(__unused UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {  // set RCTSetCustomNSURLSessionConfigurationProvider  RCTSetCustomNSURLSessionConfigurationProvider(^NSURLSessionConfiguration *{     NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];     // configure the session     return configuration;  });  // set up React  _bridge = [[RCTBridge alloc] initWithDelegate:self launchOptions:launchOptions];}
```

Is this page useful?

---

# Nodes from refs

> React Native apps render a native view tree that represents the UI, similar to how React DOM does on Web (the DOM tree). React Native provides imperative access to this tree via refs, which are returned by all native components (including those rendered by built-in components like View).

React Native apps render a native view tree that represents the UI, similar to how React DOM does on Web (the DOM tree). React Native provides imperative access to this tree via [refs](https://react.dev/learn/manipulating-the-dom-with-refs), which are returned by all native components (including those rendered by built-in components like [View](https://reactnative.dev/docs/next/view)).

React Native provides 3 types of nodes:

- [Elements](https://reactnative.dev/docs/next/element-nodes): element nodes represent native components in the native view tree (similar to [Element](https://developer.mozilla.org/en-US/docs/Web/API/Element) nodes on Web). They are provided by all native components via refs.
- [Text](https://reactnative.dev/docs/next/text-nodes): text nodes represent raw text content on the tree (similar to [Text](https://developer.mozilla.org/en-US/docs/Web/API/Text) nodes on Web). They are not directly accessible via `refs`, but can be accessed using methods like [childNodes](https://developer.mozilla.org/en-US/docs/Web/API/Node/childNodes) on element refs.
- [Documents](https://reactnative.dev/docs/next/document-nodes): document nodes represent a complete native view tree (similar to [Document](https://developer.mozilla.org/en-US/docs/Web/API/Document) nodes on Web). Like text nodes, they can only be accessed through other nodes, using properties like [ownerDocument](https://developer.mozilla.org/en-US/docs/Web/API/Node/ownerDocument).

As on Web, these nodes can be used to traverse the rendered UI tree, access layout information or execute imperative operations like `focus`.

 info

**Unlike on Web, these nodes do not allow mutation** (e.g.: [node.appendChild](https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild)), as the tree contents are fully managed by the React renderer.

Is this page useful?
