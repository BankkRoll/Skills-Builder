# Shadow Props and more

# Shadow Props

> ---

---

# Reference

There are 3 sets of shadow APIs in React Native:

- `boxShadow`: A View style prop and a spec-compliant implementation of the [web style prop of the same name](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow).
- `dropShadow`: A specific filter function available as part of the [filter](https://reactnative.dev/docs/view-style-props#filter) View style prop.
- Various `shadow` props (`shadowColor`, `shadowOffset`, `shadowOpacity`, `shadowRadius`): These map directly to their native counterparts exposed by the platform-level APIs.

The difference between `dropShadow` and `boxShadow` are as follows:

- `dropShadow` exists as part of `filter`, whereas `boxShadow` is a standalone style prop.
- `dropShadow` is an alpha mask, so only pixels with a positive alpha value will "cast" a shadow. `boxShadow` will cast around the border box of the element no matter it's contents (unless it is inset).
- `dropShadow` is only available on Android, `boxShadow` is available on iOS and Android.
- `dropShadow` cannot be inset like `boxShadow`.
- `dropShadow` does not have the `spreadDistance` argument like `boxShadow`.

Both `boxShadow` and `dropShadow` are generally more capable than the `shadow` props. The `shadow` props, however, map to native platform-level APIs, so if you only need a straightforward shadow these props are recommended. Note that only `shadowColor` works on both Android and iOS, all other `shadow` props only work on iOS.

## Props​

### boxShadow​

See [View Style Props](https://reactnative.dev/docs/view-style-props#boxshadow) for documentation.

### dropShadowAndroid​

See [View Style Props](https://reactnative.dev/docs/view-style-props#filter) for documentation.

### shadowColor​

Sets the drop shadow color.

This property will only work on Android API 28 and above. For similar functionality on lower Android APIs, use the [elevationproperty](https://reactnative.dev/docs/view-style-props#elevation-android).

| Type |
| --- |
| color |

---

### shadowOffsetiOS​

Sets the drop shadow offset.

| Type |
| --- |
| object:{width: number,height: number} |

---

### shadowOpacityiOS​

Sets the drop shadow opacity (multiplied by the color's alpha component).

| Type |
| --- |
| number |

---

### shadowRadiusiOS​

Sets the drop shadow blur radius.

| Type |
| --- |
| number |

Is this page useful?

---

# Share

> Example

## Example​

# Reference

## Methods​

### share()​

 tsx

```
static share(content: ShareContent, options?: ShareOptions);
```

Open a dialog to share text content.

In iOS, returns a Promise which will be invoked with an object containing `action` and `activityType`. If the user dismissed the dialog, the Promise will still be resolved with action being `Share.dismissedAction` and all the other keys being undefined. Note that some share options will not appear or work on the iOS simulator.

In Android, returns a Promise which will always be resolved with action being `Share.sharedAction`.

**Properties:**

| Name | Type | Description |
| --- | --- | --- |
| contentRequired | object | message- a message to shareurl- a URL to shareiOStitle- title of the messageAndroidAt least one ofurlandmessageis required. |
| options | object | dialogTitleAndroidexcludedActivityTypesiOSsubject- a subject to share via emailiOStintColoriOSanchor- the node to which the action sheet should be anchored (used for iPad)iOS |

---

## Properties​

### sharedAction​

 tsx

```
static sharedAction: 'sharedAction';
```

The content was successfully shared.

---

### dismissedActioniOS​

 tsx

```
static dismissedAction: 'dismissedAction';
```

The dialog has been dismissed.

Is this page useful?

---

# Publishing to Google Play Store

> Android requires that all apps be digitally signed with a certificate before they can be installed. In order to distribute your Android application via Google Play store it needs to be signed with a release key that then needs to be used for all future updates. Since 2017 it is possible for Google Play to manage signing releases automatically thanks to App Signing by Google Play functionality. However, before your application binary is uploaded to Google Play it needs to be signed with an upload key. The Signing Your Applications page on Android Developers documentation describes the topic in detail. This guide covers the process in brief, as well as lists the steps required to package the JavaScript bundle.

Android requires that all apps be digitally signed with a certificate before they can be installed. In order to distribute your Android application via [Google Play store](https://play.google.com/store) it needs to be signed with a release key that then needs to be used for all future updates. Since 2017 it is possible for Google Play to manage signing releases automatically thanks to [App Signing by Google Play](https://developer.android.com/studio/publish/app-signing#app-signing-google-play) functionality. However, before your application binary is uploaded to Google Play it needs to be signed with an upload key. The [Signing Your Applications](https://developer.android.com/tools/publishing/app-signing.html) page on Android Developers documentation describes the topic in detail. This guide covers the process in brief, as well as lists the steps required to package the JavaScript bundle.

 info

If you are using Expo, read the Expo guide for [Deploying to App Stores](https://docs.expo.dev/distribution/app-stores/) to build and submit your app for the Google Play Store. This guide works with any React Native app to automate the deployment process.

## Generating an upload key​

You can generate a private signing key using `keytool`.

### Windows​

On Windows `keytool` must be run from `C:\Program Files\Java\jdkx.x.x_x\bin`, as administrator.

 shell

```
keytool -genkeypair -v -storetype PKCS12 -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

This command prompts you for passwords for the keystore and key and for the Distinguished Name fields for your key. It then generates the keystore as a file called `my-upload-key.keystore`.

The keystore contains a single key, valid for 10000 days. The alias is a name that you will use later when signing your app, so remember to take note of the alias.

### macOS​

On macOS, if you're not sure where your JDK bin folder is, then perform the following command to find it:

 shell

```
/usr/libexec/java_home
```

It will output the directory of the JDK, which will look something like this:

 shell

```
/Library/Java/JavaVirtualMachines/jdkX.X.X_XXX.jdk/Contents/Home
```

Navigate to that directory by using the command `cd /your/jdk/path` and use the keytool command with sudo permission as shown below.

 shell

```
sudo keytool -genkey -v -keystore my-upload-key.keystore -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

 caution

Remember to keep the keystore file private. In case you've lost upload key or it's been compromised you should [follow these instructions](https://support.google.com/googleplay/android-developer/answer/7384423#reset).

## Setting up Gradle variables​

1. Place the `my-upload-key.keystore` file under the `android/app` directory in your project folder.
2. Edit the file `~/.gradle/gradle.properties` or `android/gradle.properties`, and add the following (replace `*****` with the correct keystore password, alias and key password),

```
MYAPP_UPLOAD_STORE_FILE=my-upload-key.keystoreMYAPP_UPLOAD_KEY_ALIAS=my-key-aliasMYAPP_UPLOAD_STORE_PASSWORD=*****MYAPP_UPLOAD_KEY_PASSWORD=*****
```

These are going to be global Gradle variables, which we can later use in our Gradle config to sign our app.

 Note about using git

Saving the above Gradle variables in `~/.gradle/gradle.properties` instead of `android/gradle.properties` prevents them from being checked in to git. You may have to create the `~/.gradle/gradle.properties` file in your user's home directory before you can add the variables.

 Note about security

If you are not keen on storing your passwords in plaintext, and you are running macOS, you can also [store your credentials in the Keychain Access app](https://pilloxa.gitlab.io/posts/safer-passwords-in-gradle/). Then you can skip the two last rows in `~/.gradle/gradle.properties`.

## Adding signing config to your app's Gradle config​

The last configuration step that needs to be done is to setup release builds to be signed using upload key. Edit the file `android/app/build.gradle` in your project folder, and add the signing config,

 groovy

```
...android {    ...    defaultConfig { ... }    signingConfigs {        release {            if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {                storeFile file(MYAPP_UPLOAD_STORE_FILE)                storePassword MYAPP_UPLOAD_STORE_PASSWORD                keyAlias MYAPP_UPLOAD_KEY_ALIAS                keyPassword MYAPP_UPLOAD_KEY_PASSWORD            }        }    }    buildTypes {        release {            ...            signingConfig signingConfigs.release        }    }}...
```

## Generating the release AAB​

Run the following command in a terminal:

 shell

```
npx react-native build-android --mode=release
```

This command uses Gradle's `bundleRelease` under the hood that bundles all the JavaScript needed to run your app into the AAB ([Android App Bundle](https://developer.android.com/guide/app-bundle)). If you need to change the way the JavaScript bundle and/or drawable resources are bundled (e.g. if you changed the default file/folder names or the general structure of the project), have a look at `android/app/build.gradle` to see how you can update it to reflect these changes.

 note

Make sure `gradle.properties` does not include `org.gradle.configureondemand=true` as that will make the release build skip bundling JS and assets into the app binary.

The generated AAB can be found under `android/app/build/outputs/bundle/release/app-release.aab`, and is ready to be uploaded to Google Play.

In order for Google Play to accept AAB format the App Signing by Google Play needs to be configured for your application on the Google Play Console. If you are updating an existing app that doesn't use App Signing by Google Play, please check our [migration section](#migrating-old-android-react-native-apps-to-use-app-signing-by-google-play) to learn how to perform that configuration change.

## Testing the release build of your app​

Before uploading the release build to the Play Store, make sure you test it thoroughly. First uninstall any previous version of the app you already have installed. Install it on the device using the following command in the project root:

shell

```
npm run android -- --mode="release"
```

shell

```
yarn android --mode release
```

Note that `--mode release` is only available if you've set up signing as described above.

You can terminate any running bundler instances, since all your framework and JavaScript code is bundled in the APK's assets.

## Publishing to other stores​

By default, the generated APK has the native code for both `x86`, `x86_64`, `ARMv7a` and `ARM64-v8a` CPU architectures. This makes it easier to share APKs that run on almost all Android devices. However, this has the downside that there will be some unused native code on any device, leading to unnecessarily bigger APKs.

You can create an APK for each CPU by adding the following line in your `android/app/build.gradle` file:

 diff

```
android {    splits {        abi {            reset()            enable true            universalApk false            include "armeabi-v7a", "arm64-v8a", "x86", "x86_64"        }    }}
```

Upload these files to markets which support device targeting, such as [Amazon AppStore](https://developer.amazon.com/docs/app-submission/device-filtering-and-compatibility.html) or [F-Droid](https://f-droid.org/en/), and the users will automatically get the appropriate APK. If you want to upload to other markets, such as [APKFiles](https://www.apkfiles.com/), which do not support multiple APKs for a single app, change the `universalApk false` line to `true` to create the default universal APK with binaries for both CPUs.

Please note that you will also have to configure distinct version codes, as [suggested in this page](https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions) from the official Android documentation.

## Enabling Proguard to reduce the size of the APK (optional)​

Proguard is a tool that can slightly reduce the size of the APK. It does this by stripping parts of the React Native Java bytecode (and its dependencies) that your app is not using.

 Important

Make sure to thoroughly test your app if you've enabled Proguard. Proguard often requires configuration specific to each native library you're using. See `app/proguard-rules.pro`.

To enable Proguard, edit `android/app/build.gradle`:

 groovy

```
/** * Run Proguard to shrink the Java bytecode in release builds. */def enableProguardInReleaseBuilds = true
```

## Migrating old Android React Native apps to use App Signing by Google Play​

If you are migrating from previous version of React Native chances are your app does not use App Signing by Google Play feature. We recommend you enable that in order to take advantage from things like automatic app splitting. In order to migrate from the old way of signing you need to start by [generating new upload key](#generating-an-upload-key) and then replacing release signing config in `android/app/build.gradle` to use the upload key instead of the release one (see section about [adding signing config to gradle](#adding-signing-config-to-your-apps-gradle-config)). Once that's done you should follow the [instructions from Google Play Help website](https://support.google.com/googleplay/android-developer/answer/7384423) in order to send your original release key to Google Play.

## Default Permissions​

By default, `INTERNET` permission is added to your Android app as pretty much all apps use it. `SYSTEM_ALERT_WINDOW` permission is added to your Android APK in debug mode but it will be removed in production.

Is this page useful?

---

# State

> There are two types of data that control a component: props and state. props are set by the parent and they are fixed throughout the lifetime of a component. For data that is going to change, we have to use state.

There are two types of data that control a component: `props` and `state`. `props` are set by the parent and they are fixed throughout the lifetime of a component. For data that is going to change, we have to use `state`.

In general, you should initialize `state` in the constructor, and then call `setState` when you want to change it.

For example, let's say we want to make text that blinks all the time. The text itself gets set once when the blinking component gets created, so the text itself is a `prop`. The "whether the text is currently on or off" changes over time, so that should be kept in `state`.

In a real application, you probably won't be setting state with a timer. You might set state when you have new data from the server, or from user input. You can also use a state container like [Redux](https://redux.js.org/) or [MobX](https://mobx.js.org/) to control your data flow. In that case you would use Redux or MobX to modify your state rather than calling `setState` directly.

When setState is called, BlinkApp will re-render its Component. By calling setState within the Timer, the component will re-render every time the Timer ticks.

State works the same way as it does in React, so for more details on handling state, you can look at the [React.Component API](https://react.dev/reference/react/Component#setstate). At this point, you may have noticed that most of our examples use the default text color. To customize the text color, you will have to [learn about Style](https://reactnative.dev/docs/style).

Is this page useful?

---

# StatusBar

> Component to control the app's status bar. The status bar is the zone, typically at the top of the screen, that displays the current time, Wi-Fi and cellular network information, battery level and/or other status icons.

Component to control the app's status bar. The status bar is the zone, typically at the top of the screen, that displays the current time, Wi-Fi and cellular network information, battery level and/or other status icons.

### Usage with Navigator​

It is possible to have multiple `StatusBar` components mounted at the same time. The props will be merged in the order the `StatusBar` components were mounted.

### Imperative API​

For cases where using a component is not ideal, there is also an imperative API exposed as static functions on the component. It is however not recommended to use the static API and the component for the same prop because any value set by the static API will get overridden by the one set by the component in the next render.

---

# Reference

## Constants​

### currentHeightAndroid​

The height of the status bar, which includes the notch height, if present.

---

## Props​

### animated​

If the transition between status bar property changes should be animated. Supported for `backgroundColor`, `barStyle` and `hidden` properties.

| Type | Required | Default |
| --- | --- | --- |
| boolean | No | false |

---

### backgroundColorAndroid​

The background color of the status bar.

 warning

Due to edge-to-edge enforcement introduced in Android 15, setting background color of the status bar is deprecated in API level 35 and setting it will have no effect. You can read more about our [edge-to-edge recommendations here](https://github.com/react-native-community/discussions-and-proposals/discussions/827).

| Type | Required | Default |
| --- | --- | --- |
| color | No | default system StatusBar background color, or'black'if not defined |

---

### barStyle​

Sets the color of the status bar text.

On Android, this will only have an impact on API versions 23 and above.

| Type | Required | Default |
| --- | --- | --- |
| StatusBarStyle | No | 'default' |

---

### hidden​

If the status bar is hidden.

| Type | Required | Default |
| --- | --- | --- |
| boolean | No | false |

---

### networkActivityIndicatorVisibleiOS​

If the network activity indicator should be visible.

| Type | Default |
| --- | --- |
| boolean | false |

---

### showHideTransitioniOS​

The transition effect when showing and hiding the status bar using the `hidden` prop.

| Type | Default |
| --- | --- |
| StatusBarAnimation | 'fade' |

---

### translucentAndroid​

If the status bar is translucent. When translucent is set to `true`, the app will draw under the status bar. This is useful when using a semi transparent status bar color.

 warning

Due to edge-to-edge enforcement introduced in Android 15, setting the status bar as translucent is deprecated in API level 35 and setting it will have no effect. You can read more about our [edge-to-edge recommendations here](https://github.com/react-native-community/discussions-and-proposals/discussions/827).

| Type | Default |
| --- | --- |
| boolean | false |

## Methods​

### popStackEntry()​

 tsx

```
static popStackEntry(entry: StatusBarProps);
```

Get and remove the last StatusBar entry from the stack.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| entryRequired | any | Entry returned frompushStackEntry. |

---

### pushStackEntry()​

 tsx

```
static pushStackEntry(props: StatusBarProps): StatusBarProps;
```

Push a StatusBar entry onto the stack. The return value should be passed to `popStackEntry` when complete.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| propsRequired | any | Object containing the StatusBar props to use in the stack entry. |

---

### replaceStackEntry()​

 tsx

```
static replaceStackEntry(  entry: StatusBarProps,  props: StatusBarProps): StatusBarProps;
```

Replace an existing StatusBar stack entry with new props.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| entryRequired | any | Entry returned frompushStackEntryto replace. |
| propsRequired | any | Object containing the StatusBar props to use in the replacement stack entry. |

---

### setBackgroundColor()Android​

 tsx

```
static setBackgroundColor(color: ColorValue, animated?: boolean);
```

Set the background color for the status bar.

 warning

Due to edge-to-edge enforcement introduced in Android 15, setting background color of the status bar is deprecated in API level 35 and setting it will have no effect. You can read more about our [edge-to-edge recommendations here](https://github.com/react-native-community/discussions-and-proposals/discussions/827).

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| colorRequired | string | Background color. |
| animated | boolean | Animate the style change. |

---

### setBarStyle()​

 tsx

```
static setBarStyle(style: StatusBarStyle, animated?: boolean);
```

Set the status bar style.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| styleRequired | StatusBarStyle | Status bar style to set. |
| animated | boolean | Animate the style change. |

---

### setHidden()​

 tsx

```
static setHidden(hidden: boolean, animation?: StatusBarAnimation);
```

Show or hide the status bar.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| hiddenRequired | boolean | Hide the status bar. |
| animationiOS | StatusBarAnimation | Animation when changing the status bar hidden property. |

---

### 🗑️setNetworkActivityIndicatorVisible()iOS​

 Deprecated

The status bar network activity indicator is not supported in iOS 13 and later. This will be removed in a future release.

 tsx

```
static setNetworkActivityIndicatorVisible(visible: boolean);
```

Control the visibility of the network activity indicator.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| visibleRequired | boolean | Show the indicator. |

---

### setTranslucent()Android​

 tsx

```
static setTranslucent(translucent: boolean);
```

Control the translucency of the status bar.

 warning

Due to edge-to-edge enforcement introduced in Android 15, setting the status bar as translucent is deprecated in API level 35 and setting it will have no effect. You can read more about our [edge-to-edge recommendations here](https://github.com/react-native-community/discussions-and-proposals/discussions/827).

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| translucentRequired | boolean | Set as translucent. |

## Type Definitions​

### StatusBarAnimation​

Status bar animation type for transitions on the iOS.

| Type |
| --- |
| enum |

**Constants:**

| Value | Type | Description |
| --- | --- | --- |
| 'fade' | string | Fade animation |
| 'slide' | string | Slide animation |
| 'none' | string | No animation |

---

### StatusBarStyle​

Status bar style type.

| Type |
| --- |
| enum |

**Constants:**

| Value | Type | Description |
| --- | --- | --- |
| 'default' | string | Default status bar style (dark for iOS, light for Android) |
| 'light-content' | string | White texts and icons |
| 'dark-content' | string | Dark texts and icons (requires API>=23 on Android) |

Is this page useful?

---

# Strict TypeScript API (opt in)

> The Strict TypeScript API is a preview of our future, stable JavaScript API for React Native.

The Strict TypeScript API is a preview of our future, stable JavaScript API for React Native.

Specifically, this is a new set of TypeScript types for the `react-native` npm package, available from 0.80 onwards. These provide stronger and more futureproof type accuracy, and will allow us to confidently evolve React Native's API into a stable shape. Opting in to the Strict TypeScript API brings some structural type differences, and is therefore a one-time breaking change.

The new types are:

1. **Generated directly from our source code** — improving coverage and correctness, so you can expect stronger compatibility guarantees.
2. **Restricted toreact-native's index file** — more tightly defining our public API, and meaning we won't break the API when making internal file changes.

When the community is ready, the Strict TypeScript API will become our default API in future — synchronized with deep imports removal.

## Opting in​

We're shipping these new types alongside our existing types, meaning you can choose to migrate when ready. We encourage early adopters and newly created apps to opt in via your `tsconfig.json` file.

Opting in is a **breaking change**, since some of our new types have updated names and shapes, although many apps won't be affected. You can learn about each breaking change in the next section.

 tsconfig.json

```
{  "extends": "@react-native/typescript-config",  "compilerOptions": {    ...    "customConditions": ["react-native-strict-api"]  }}
```

 Under the hood

This will instruct TypeScript to resolve `react-native` types from our new [types_generated/](https://www.npmjs.com/package/react-native?activeTab=code) dir, instead of the previous [types/](https://www.npmjs.com/package/react-native?activeTab=code) dir (manually maintained). No restart of TypeScript or your editor is required.

The Strict TypeScript API follows our [RFC](https://github.com/react-native-community/discussions-and-proposals/pull/894) to remove deep imports from React Native. Therefore, some APIs are no longer exported at root. This is intentional, in order to reduce the overall surface area of React Native's API.

 API feedback

**Sending feedback**: We will be working with the community to finalize which APIs we export over (at least) the next two React Native releases. Please share your feedback in our [feedback thread](https://github.com/react-native-community/discussions-and-proposals/discussions/893).

See also our [announcement blog post](https://reactnative.dev/blog/2025/06/12/moving-towards-a-stable-javascript-api) for more info on our motivation and timelines.

## Migration guide​

### Codegen types should now be imported from thereact-nativepackage​

Types used for codegen, like `Int32`, `Double`, `WithDefault` etc. are now available under a single `CodegenTypes` namespace. Similarly, `codegenNativeComponent` and `codegenNativeCommands` are now available to import from the react-native package instead of using the deep import.

Namespaced `CodegenTypes` as well as `codegenNativeCommands` and `codegenNativeComponent` are also available from `react-native` package when the Strict API is not enabled to make the adoption easier for third-party libraries.

**Before**

```
import codegenNativeComponent from 'react-native/Libraries/Utilities/codegenNativeComponent';import type {  Int32,  WithDefault,} from 'react-native/Libraries/Types/CodegenTypes';interface NativeProps extends ViewProps {  enabled?: WithDefault<boolean, true>;  size?: Int32;}export default codegenNativeComponent<NativeProps>(  'RNCustomComponent',);
```

**After**

```
import {CodegenTypes, codegenNativeComponent} from 'react-native';interface NativeProps extends ViewProps {  enabled?: CodegenTypes.WithDefault<boolean, true>;  size?: CodegenTypes.Int32;}export default codegenNativeComponent<NativeProps>(  'RNCustomComponent',);
```

### Removal of*Statictypes​

**Before**

```
import {Linking, LinkingStatic} from 'react-native';function foo(linking: LinkingStatic) {}foo(Linking);
```

**After**

```
import {Linking} from 'react-native';function foo(linking: Linking) {}foo(Linking);
```

The following APIs were previously named as `*Static` plus a variable declaration of said type. In most cases there was an alias so that value and the type were exported under the same identifier, but some were missing.

(For example there was an `AlertStatic` type, `Alert` variable of type `AlertStatic` and type `Alert` which was an alias for `AlertStatic`. But in the case of `PixelRatio` there was a `PixelRatioStatic` type and a `PixelRatio` variable of that type without additional type aliases.)

**Affected APIs**

- `AlertStatic`
- `ActionSheetIOSStatic`
- `ToastAndroidStatic`
- `InteractionManagerStatic` (In this case there was no relevant `InteractionManager` type alias)
- `UIManagerStatic`
- `PlatformStatic`
- `SectionListStatic`
- `PixelRatioStatic` (In this case there was no relevant `PixelRatio` type alias)
- `AppStateStatic`
- `AccessibilityInfoStatic`
- `ImageResizeModeStatic`
- `BackHandlerStatic`
- `DevMenuStatic` (In this case there was no relevant `DevMenu` type alias)
- `ClipboardStatic`
- `PermissionsAndroidStatic`
- `ShareStatic`
- `DeviceEventEmitterStatic`
- `LayoutAnimationStatic`
- `KeyboardStatic` (In this case there was no relevant `Keyboard` type alias)
- `DevSettingsStatic` (In this case there was no relevant `DevSettings` type alias)
- `I18nManagerStatic`
- `EasingStatic`
- `PanResponderStatic`
- `NativeModulesStatic` (In this case there was no relevant `NativeModules` type alias)
- `LogBoxStatic`
- `PushNotificationIOSStatic`
- `SettingsStatic`
- `VibrationStatic`

### Some core components are now function components instead of class components​

- `View`
- `Image`
- `TextInput`
- `Modal`
- `Text`
- `TouchableWithoutFeedback`
- `Switch`
- `ActivityIndicator`
- `ProgressBarAndroid`
- `InputAccessoryView`
- `Button`
- `SafeAreaView`

Due to this change, accessing ref types of these views requires using `React.ComponentRef<typeof View>` pattern which works as expected for both class and function components, e.g.:

```
const ref = useRef<React.ComponentRef<typeof View>>(null);
```

## Other breaking changes​

### Changes to Animated types​

Animated nodes were previously generic types based on their interpolation output. Now, they are non-generic types with a generic `interpolate` method.

`Animated.LegacyRef` is no longer available.

### Unified types for optional props​

In the new types, every optional prop will be typed as `type | undefined`.

### Removal of some deprecated types​

All types listed in [DeprecatedPropertiesAlias.d.ts](https://github.com/facebook/react-native/blob/0.83-stable/packages/react-native/types/public/DeprecatedPropertiesAlias.d.ts) are inaccessible under the Strict API.

### Removal of leftover component props​

Some properties that were defined in type definitions but were not used by the component or were lacking a definition were removed (for example: `lineBreakMode` on `Text`, `scrollWithoutAnimationTo` on `ScrollView`, transform styles defined outside of transform array).

### Previously accessible private type helpers may now be removed​

Due to the configuration of the previous type definitions, every defined type was accessible from the `react-native` package. This included types that were not explicitly exported and helper types that were only supposed to be used internally.

Notable examples of this are types related to StyleSheet (like `RecursiveArray`, `RegisteredStyle` and `Falsy`) and Animated (like `WithAnimatedArray` and `WithAnimatedObject`).

Is this page useful?

---

# Style

> With React Native, you style your application using JavaScript. All of the core components accept a prop named style. The style names and values usually match how CSS works on the web, except names are written using camel casing, e.g. backgroundColor rather than background-color.

With React Native, you style your application using JavaScript. All of the core components accept a prop named `style`. The style names and [values](https://reactnative.dev/docs/colors) usually match how CSS works on the web, except names are written using camel casing, e.g. `backgroundColor` rather than `background-color`.

The `style` prop can be a plain old JavaScript object. That's what we usually use for example code. You can also pass an array of styles - the last style in the array has precedence, so you can use this to inherit styles.

As a component grows in complexity, it is often cleaner to use `StyleSheet.create` to define several styles in one place. Here's an example:

One common pattern is to make your component accept a `style` prop which in turn is used to style subcomponents. You can use this to make styles "cascade" the way they do in CSS.

There are a lot more ways to customize the text style. Check out the [Text component reference](https://reactnative.dev/docs/text) for a complete list.

Now you can make your text beautiful. The next step in becoming a style expert is to [learn how to control component size](https://reactnative.dev/docs/height-and-width).

## Known issues​

- [react-native#29308](https://github.com/facebook/react-native/issues/29308#issuecomment-792864162): In some cases React Native does not match how CSS works on the web, for example the touch area never extends past the parent view bounds and on Android negative margin is not supported.

Is this page useful?

---

# StyleSheet

> A StyleSheet is an abstraction similar to CSS StyleSheets.

A StyleSheet is an abstraction similar to CSS StyleSheets.

Code quality tips:

- By moving styles away from the render function, you're making the code easier to understand.
- Naming the styles is a good way to add meaning to the low level components in the render function, and encourage reuse.
- In most IDEs, using `StyleSheet.create()` will offer static type checking and suggestions to help you write valid styles.

---

# Reference

## Methods​

### compose()​

 tsx

```
static compose(style1: Object, style2: Object): Object | Object[];
```

Combines two styles such that `style2` will override any styles in `style1`. If either style is falsy, the other one is returned without allocating an array, saving allocations and maintaining reference equality for PureComponent checks.

---

### create()​

 tsx

```
static create(styles: Object extends Record<string, ViewStyle | ImageStyle | TextStyle>): Object;
```

An identity function for creating styles. The main practical benefit of creating styles inside `StyleSheet.create()` is static type checking against native style properties.

---

### flatten()​

 tsx

```
static flatten(style: Array<Object extends Record<string, ViewStyle | ImageStyle | TextStyle>>): Object;
```

Flattens an array of style objects, into one aggregated style object.

---

### setStyleAttributePreprocessor()​

 Experimental

Breaking changes will probably happen a lot and will not be reliably announced. The whole thing might be deleted, who knows? Use at your own risk.

 tsx

```
static setStyleAttributePreprocessor(  property: string,  process: (propValue: any) => any,);
```

Sets a function to use to pre-process a style property value. This is used internally to process color and transform values. You should not use this unless you really know what you are doing and have exhausted other options.

## Properties​

---

### absoluteFill​

A very common pattern is to create overlays with position absolute and zero positioning (`position: 'absolute', left: 0, right: 0, top: 0, bottom: 0`), so `absoluteFill` can be used for convenience and to reduce duplication of these repeated styles. If you want, absoluteFill can be used to create a customized entry in a StyleSheet, e.g.:

---

### absoluteFillObject​

Sometimes you may want `absoluteFill` but with a couple tweaks - `absoluteFillObject` can be used to create a customized entry in a `StyleSheet`, e.g.:

---

### hairlineWidth​

This is defined as the width of a thin line on the platform. It can be used as the thickness of a border or division between two elements. Example:

This constant will always be a round number of pixels (so a line defined by it can look crisp) and will try to match the standard width of a thin line on the underlying platform. However, you should not rely on it being a constant size, because on different platforms and screen densities its value may be calculated differently.

A line with hairline width may not be visible if your simulator is downscaled.

Is this page useful?

---

# Switch

> Renders a boolean input.

Renders a boolean input.

This is a controlled component that requires an `onValueChange` callback that updates the `value` prop in order for the component to reflect user actions. If the `value` prop is not updated, the component will continue to render the supplied `value` prop instead of the expected result of any user actions.

## Example​

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### disabled​

If true the user won't be able to toggle the switch.

| Type | Default |
| --- | --- |
| bool | false |

---

### ios_backgroundColoriOS​

On iOS, custom color for the background. This background color can be seen either when the switch value is `false` or when the switch is disabled (and the switch is translucent).

| Type |
| --- |
| color |

---

### onChange​

Invoked when the user tries to change the value of the switch. Receives the change event as an argument. If you want to only receive the new value, use `onValueChange` instead.

| Type |
| --- |
| function |

---

### onValueChange​

Invoked when the user tries to change the value of the switch. Receives the new value as an argument. If you want to instead receive an event, use `onChange`.

| Type |
| --- |
| function |

---

### ref​

A ref setter that will be assigned an [element node](https://reactnative.dev/docs/element-nodes) when mounted.

---

### thumbColor​

Color of the foreground switch grip. If this is set on iOS, the switch grip will lose its drop shadow.

| Type |
| --- |
| color |

---

### trackColor​

Custom colors for the switch track.

*iOS*: When the switch value is `false`, the track shrinks into the border. If you want to change the color of the background exposed by the shrunken track, use [ios_backgroundColor](https://reactnative.dev/docs/switch#ios_backgroundColor).

| Type |
| --- |
| object: {false:color, true:color} |

---

### value​

The value of the switch. If true the switch will be turned on. Default value is false.

| Type |
| --- |
| bool |

Is this page useful?

---

# Systrace

> Systrace is a standard Android marker-based profiling tool (and is installed when you install the Android platform-tools package). Profiled code blocks are surrounded by start/end markers which are then visualized in a colorful chart format. Both the Android SDK and React Native framework provide standard markers that you can visualize.

`Systrace` is a standard Android marker-based profiling tool (and is installed when you install the Android platform-tools package). Profiled code blocks are surrounded by start/end markers which are then visualized in a colorful chart format. Both the Android SDK and React Native framework provide standard markers that you can visualize.

## Example​

`Systrace` allows you to mark JavaScript (JS) events with a tag and an integer value. Capture the non-Timed JS events in EasyProfiler.

---

# Reference

## Methods​

### isEnabled()​

 tsx

```
static isEnabled(): boolean;
```

---

### beginEvent()​

 tsx

```
static beginEvent(eventName: string | (() => string), args?: EventArgs);
```

beginEvent/endEvent for starting and then ending a profile within the same call stack frame.

---

### endEvent()​

 tsx

```
static endEvent(args?: EventArgs);
```

---

### beginAsyncEvent()​

 tsx

```
static beginAsyncEvent(  eventName: string | (() => string),  args?: EventArgs,): number;
```

beginAsyncEvent/endAsyncEvent for starting and then ending a profile where the end can either occur on another thread or out of the current stack frame, eg await the returned cookie variable should be used as input into the endAsyncEvent call to end the profile.

---

### endAsyncEvent()​

 tsx

```
static endAsyncEvent(  eventName: EventName,  cookie: number,  args?: EventArgs,);
```

---

### counterEvent()​

 tsx

```
static counterEvent(eventName: string | (() => string), value: number);
```

Register the value to the profileName on the systrace timeline.

Is this page useful?

---

# TargetEvent Object Type

> TargetEvent object is returned in the callback as a result of focus change, for example onFocus or onBlur in the TextInput component.

`TargetEvent` object is returned in the callback as a result of focus change, for example `onFocus` or `onBlur` in the [TextInput](https://reactnative.dev/docs/textinput) component.

## Example​

```
{    target: 1127}
```

## Keys and values​

### target​

The node id of the element receiving the TargetEvent.

| Type | Optional |
| --- | --- |
| number,null,undefined | No |

## Used by​

- [TextInput](https://reactnative.dev/docs/textinput)
- [TouchableWithoutFeedback](https://reactnative.dev/docs/touchablewithoutfeedback)

Is this page useful?
