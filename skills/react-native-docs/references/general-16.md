# PixelRatio and more

# PixelRatio

> PixelRatio gives you access to the device's pixel density and font scale.

`PixelRatio` gives you access to the device's pixel density and font scale.

## Fetching a correctly sized image​

You should get a higher resolution image if you are on a high pixel density device. A good rule of thumb is to multiply the size of the image you display by the pixel ratio.

 tsx

```
const image = getImage({  width: PixelRatio.getPixelSizeForLayoutSize(200),  height: PixelRatio.getPixelSizeForLayoutSize(100),});<Image source={image} style={{width: 200, height: 100}} />;
```

## Pixel grid snapping​

In iOS, you can specify positions and dimensions for elements with arbitrary precision, for example 29.674825. But, ultimately the physical display only have a fixed number of pixels, for example 640×1136 for iPhone SE (1st generation) or 828×1792 for iPhone 11. iOS tries to be as faithful as possible to the user value by spreading one original pixel into multiple ones to trick the eye. The downside of this technique is that it makes the resulting element look blurry.

In practice, we found out that developers do not want this feature and they have to work around it by doing manual rounding in order to avoid having blurry elements. In React Native, we are rounding all the pixels automatically.

We have to be careful when to do this rounding. You never want to work with rounded and unrounded values at the same time as you're going to accumulate rounding errors. Having even one rounding error is deadly because a one pixel border may vanish or be twice as big.

In React Native, everything in JavaScript and within the layout engine works with arbitrary precision numbers. It's only when we set the position and dimensions of the native element on the main thread that we round. Also, rounding is done relative to the root rather than the parent, again to avoid accumulating rounding errors.

## Example​

---

# Reference

## Methods​

### get()​

 tsx

```
static get(): number;
```

Returns the device pixel density. Some examples:

- `PixelRatio.get() === 1`
  - [mdpi Android devices](https://material.io/tools/devices/)
- `PixelRatio.get() === 1.5`
  - [hdpi Android devices](https://material.io/tools/devices/)
- `PixelRatio.get() === 2`
  - iPhone SE, 6S, 7, 8
  - iPhone XR
  - iPhone 11
  - [xhdpi Android devices](https://material.io/tools/devices/)
- `PixelRatio.get() === 3`
  - iPhone 6S Plus, 7 Plus, 8 Plus
  - iPhone X, XS, XS Max
  - iPhone 11 Pro, 11 Pro Max
  - Pixel, Pixel 2
  - [xxhdpi Android devices](https://material.io/tools/devices/)
- `PixelRatio.get() === 3.5`
  - Nexus 6
  - Pixel XL, Pixel 2 XL
  - [xxxhdpi Android devices](https://material.io/tools/devices/)

---

### getFontScale()​

 tsx

```
static getFontScale(): number;
```

Returns the scaling factor for font sizes. This is the ratio that is used to calculate the absolute font size, so any elements that heavily depend on that should use this to do calculations.

- on Android value reflects the user preference set in **Settings > Display > Font size**
- on iOS value reflects the user preference set in **Settings > Display & Brightness > Text Size**, value can also be updated in **Settings > Accessibility > Display & Text Size > Larger Text**

If a font scale is not set, this returns the device pixel ratio.

---

### getPixelSizeForLayoutSize()​

 tsx

```
static getPixelSizeForLayoutSize(layoutSize: number): number;
```

Converts a layout size (dp) to pixel size (px).

Guaranteed to return an integer number.

---

### roundToNearestPixel()​

 tsx

```
static roundToNearestPixel(layoutSize: number): number;
```

Rounds a layout size (dp) to the nearest layout size that corresponds to an integer number of pixels. For example, on a device with a PixelRatio of 3, `PixelRatio.roundToNearestPixel(8.4) = 8.33`, which corresponds to exactly (8.33 * 3) = 25 pixels.

Is this page useful?

---

# Platform

> When building a cross-platform app, you'll want to re-use as much code as possible. Scenarios may arise where it makes sense for the code to be different, for example you may want to implement separate visual components for Android and iOS.

When building a cross-platform app, you'll want to re-use as much code as possible. Scenarios may arise where it makes sense for the code to be different, for example you may want to implement separate visual components for Android and iOS.

React Native provides two ways to organize your code and separate it by platform:

- Using the [Platformmodule](https://reactnative.dev/docs/platform-specific-code#platform-module).
- Using [platform-specific file extensions](https://reactnative.dev/docs/platform-specific-code#platform-specific-extensions).

Certain components may have properties that work on one platform only. All of these props are annotated with `@platform` and have a small badge next to them on the website.

## Platform module​

React Native provides a module that detects the platform in which the app is running. You can use the detection logic to implement platform-specific code. Use this option when only small parts of a component are platform-specific.

 tsx

```
import {Platform, StyleSheet} from 'react-native';const styles = StyleSheet.create({  height: Platform.OS === 'ios' ? 200 : 100,});
```

`Platform.OS` will be `ios` when running on iOS and `android` when running on Android.

There is also a `Platform.select` method available that, given an object where keys can be one of `'ios' | 'android' | 'native' | 'default'`, returns the most fitting value for the platform you are currently running on. That is, if you're running on a phone, `ios` and `android` keys will take preference. If those are not specified, `native` key will be used and then the `default` key.

 tsx

```
import {Platform, StyleSheet} from 'react-native';const styles = StyleSheet.create({  container: {    flex: 1,    ...Platform.select({      ios: {        backgroundColor: 'red',      },      android: {        backgroundColor: 'green',      },      default: {        // other platforms, web for example        backgroundColor: 'blue',      },    }),  },});
```

This will result in a container having `flex: 1` on all platforms, a red background color on iOS, a green background color on Android, and a blue background color on other platforms.

Since it accepts `any` value, you can also use it to return platform-specific components, like below:

 tsx

```
const Component = Platform.select({  ios: () => require('ComponentIOS'),  android: () => require('ComponentAndroid'),})();<Component />;
```

 tsx

```
const Component = Platform.select({  native: () => require('ComponentForNative'),  default: () => require('ComponentForWeb'),})();<Component />;
```

### Detecting the Android versionAndroid​

On Android, the `Platform` module can also be used to detect the version of the Android Platform in which the app is running:

 tsx

```
import {Platform} from 'react-native';if (Platform.Version === 25) {  console.log('Running on Nougat!');}
```

**Note**: `Version` is set to the Android API version not the Android OS version. To find a mapping please refer to [Android Version History](https://en.wikipedia.org/wiki/Android_version_history#Overview).

### Detecting the iOS versioniOS​

On iOS, the `Version` is a result of `-[UIDevice systemVersion]`, which is a string with the current version of the operating system. An example of the system version is "10.3". For example, to detect the major version number on iOS:

 tsx

```
import {Platform} from 'react-native';const majorVersionIOS = parseInt(Platform.Version, 10);if (majorVersionIOS <= 9) {  console.log('Work around a change in behavior');}
```

## Platform-specific extensions​

When your platform-specific code is more complex, you should consider splitting the code out into separate files. React Native will detect when a file has a `.ios.` or `.android.` extension and load the relevant platform file when required from other components.

For example, say you have the following files in your project:

 shell

```
BigButton.ios.jsBigButton.android.js
```

You can then import the component as follows:

 tsx

```
import BigButton from './BigButton';
```

React Native will automatically pick up the right file based on the running platform.

## Native-specific extensions (i.e. sharing code with NodeJS and Web)​

You can also use the `.native.js` extension when a module needs to be shared between NodeJS/Web and React Native but it has no Android/iOS differences. This is especially useful for projects that have common code shared among React Native and ReactJS.

For example, say you have the following files in your project:

 shell

```
Container.js # picked up by webpack, Rollup or any other Web bundlerContainer.native.js # picked up by the React Native bundler for both Android and iOS (Metro)
```

You can still import it without the `.native` extension, as follows:

 tsx

```
import Container from './Container';
```

**Pro tip:** Configure your Web bundler to ignore `.native.js` extensions in order to avoid having unused code in your production bundle, thus reducing the final bundle size.

Is this page useful?

---

# Platform

> Example

## Example​

---

# Reference

## Properties​

### constants​

 tsx

```
static constants: PlatformConstants;
```

Returns an object which contains all available common and specific constants related to the platform.

**Properties:**

| Name | Type | Optional | Description |
| --- | --- | --- | --- |
| isTesting | boolean | No |  |
| reactNativeVersion | object | No | Information about React Native version. Keys aremajor,minor,patchwith optionalprereleaseand values arenumbers. |
| VersionAndroid | number | No | OS version constant specific to Android. |
| ReleaseAndroid | string | No |  |
| SerialAndroid | string | No | Hardware serial number of an Android device. |
| FingerprintAndroid | string | No | A string that uniquely identifies the build. |
| ModelAndroid | string | No | The end-user-visible name for the Android device. |
| BrandAndroid | string | No | The consumer-visible brand with which the product/hardware will be associated. |
| ManufacturerAndroid | string | No | The manufacturer of the Android device. |
| ServerHostAndroid | string | Yes |  |
| uiModeAndroid | string | No | Possible values are:'car','desk','normal','tv','watch'and'unknown'. Read more aboutAndroid ModeType. |
| forceTouchAvailableiOS | boolean | No | Indicate the availability of 3D Touch on a device. |
| interfaceIdiomiOS | string | No | The interface type for the device. Read more aboutUIUserInterfaceIdiom. |
| osVersioniOS | string | No | OS version constant specific to iOS. |
| systemNameiOS | string | No | OS name constant specific to iOS. |

---

### isPadiOS​

 tsx

```
static isPad: boolean;
```

Returns a boolean which defines if device is an iPad.

| Type |
| --- |
| boolean |

---

### isTV​

 tsx

```
static isTV: boolean;
```

Returns a boolean which defines if device is a TV.

| Type |
| --- |
| boolean |

---

### isVision​

 tsx

```
static isVision: boolean;
```

Returns a boolean which defines if device is an Apple Vision. *If you are usingApple Vision Pro (Designed for iPad)isVisionwill befalsebutisPadwill betrue*

| Type |
| --- |
| boolean |

---

### isTesting​

 tsx

```
static isTesting: boolean;
```

Returns a boolean which defines if application is running in Developer Mode with testing flag set.

| Type |
| --- |
| boolean |

---

### OS​

 tsx

```
static OS: 'android' | 'ios';
```

Returns string value representing the current OS.

| Type |
| --- |
| enum('android','ios') |

---

### Version​

 tsx

```
static Version: 'number' | 'string';
```

Returns the version of the OS.

| Type |
| --- |
| numberAndroidstringiOS |

## Methods​

### select()​

 tsx

```
static select(config: Record<string, T>): T;
```

Returns the most fitting value for the platform you are currently running on.

#### Parameters:​

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| config | object | Yes | See config description below. |

Select method returns the most fitting value for the platform you are currently running on. That is, if you're running on a phone, `android` and `ios` keys will take preference. If those are not specified, `native` key will be used and then the `default` key.

The `config` parameter is an object with the following keys:

- `android` (any)
- `ios` (any)
- `native` (any)
- `default` (any)

**Example usage:**

 tsx

```
import {Platform, StyleSheet} from 'react-native';const styles = StyleSheet.create({  container: {    flex: 1,    ...Platform.select({      android: {        backgroundColor: 'green',      },      ios: {        backgroundColor: 'red',      },      default: {        // other platforms, web for example        backgroundColor: 'blue',      },    }),  },});
```

This will result in a container having `flex: 1` on all platforms, a green background color on Android, a red background color on iOS, and a blue background color on other platforms.

Since the value of the corresponding platform key can be of type `any`, [select](https://reactnative.dev/docs/platform#select) method can also be used to return platform-specific components, like below:

 tsx

```
const Component = Platform.select({  ios: () => require('ComponentIOS'),  android: () => require('ComponentAndroid'),})();<Component />;
```

 tsx

```
const Component = Platform.select({  native: () => require('ComponentForNative'),  default: () => require('ComponentForWeb'),})();<Component />;
```

Is this page useful?

---

# PlatformColor

> You can use the PlatformColor function to access native colors on the target platform by supplying the native color’s corresponding string value. You pass a string to the PlatformColor function and, provided it exists on that platform, it will return the corresponding native color, which you can apply in any part of your application.

js

```
PlatformColor(color1, [color2, ...colorN]);
```

You can use the `PlatformColor` function to access native colors on the target platform by supplying the native color’s corresponding string value. You pass a string to the `PlatformColor` function and, provided it exists on that platform, it will return the corresponding native color, which you can apply in any part of your application.

If you pass more than one string value to the `PlatformColor` function, it will treat the first value as the default and the rest as fallback.

 js

```
PlatformColor('bogusName', 'linkColor');
```

Since native colors can be sensitive to themes and/or high contrast, this platform specific logic also translates inside your components.

### Supported colors​

For a full list of the types of system colors supported, see:

- Android:
  - [R.attr](https://developer.android.com/reference/android/R.attr) - `?attr` prefix
  - [R.color](https://developer.android.com/reference/android/R.color) - `@android:color` prefix
- iOS (Objective-C and Swift notations):
  - [UIColor Standard Colors](https://developer.apple.com/documentation/uikit/uicolor/standard_colors)
  - [UIColor UI Element Colors](https://developer.apple.com/documentation/uikit/uicolor/ui_element_colors)

#### Developer notes​

info

If you’re familiar with design systems, another way of thinking about this is that `PlatformColor` lets you tap into the local design system's color tokens so your app can blend right in!

## Example​

The string value provided to the `PlatformColor` function must match the string as it exists on the native platform where the app is running. In order to avoid runtime errors, the function should be wrapped in a platform check, either through a `Platform.OS === 'platform'` or a `Platform.select()`, as shown on the example above.

 note

You can find a complete example that demonstrates proper, intended use of `PlatformColor` in [PlatformColorExample.js](https://github.com/facebook/react-native/blob/main/packages/rn-tester/js/examples/PlatformColor/PlatformColorExample.js).

Is this page useful?

---

# Pressable

> Pressable is a Core Component wrapper that can detect various stages of press interactions on any of its defined children.

Pressable is a Core Component wrapper that can detect various stages of press interactions on any of its defined children.

 tsx

```
<Pressable onPress={onPressFunction}>  <Text>I'm pressable!</Text></Pressable>
```

## How it works​

On an element wrapped by `Pressable`:

- [onPressIn](#onpressin) is called when a press is activated.
- [onPressOut](#onpressout) is called when the press gesture is deactivated.

After pressing [onPressIn](#onpressin), one of two things will happen:

1. The person will remove their finger, triggering [onPressOut](#onpressout) followed by [onPress](#onpress).
2. If the person leaves their finger longer than 500 milliseconds before removing it, [onLongPress](#onlongpress) is triggered. ([onPressOut](#onpressout) will still fire when they remove their finger.)

 ![Diagram of the onPress events in sequence.](https://reactnative.dev/docs/assets/d_pressable_pressing.svg)

Fingers are not the most precise instruments, and it is common for users to accidentally activate the wrong element or miss the activation area. To help, `Pressable` has an optional `HitRect` you can use to define how far a touch can register away from the wrapped element. Presses can start anywhere within a `HitRect`.

`PressRect` allows presses to move beyond the element and its `HitRect` while maintaining activation and being eligible for a "press"—think of sliding your finger slowly away from a button you're pressing down on.

 note

The touch area never extends past the parent view bounds and the Z-index of sibling views always takes precedence if a touch hits two overlapping views.

 ![Diagram of HitRect and PressRect and how they work.](https://reactnative.dev/docs/assets/d_pressable_anatomy.svg)

You can set `HitRect` with `hitSlop` and set `PressRect` with `pressRetentionOffset`.

 info

`Pressable` uses React Native's `Pressability` API. For more information around the state machine flow of Pressability and how it works, check out the implementation for [Pressability](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/Pressability/Pressability.js#L350).

## Example​

## Props​

### android_disableSoundAndroid​

If true, doesn't play Android system sound on press.

| Type | Default |
| --- | --- |
| boolean | false |

### android_rippleAndroid​

Enables the Android ripple effect and configures its properties.

| Type |
| --- |
| RippleConfig |

### children​

Either children or a function that receives a boolean reflecting whether the component is currently pressed.

| Type |
| --- |
| React Node |

### unstable_pressDelay​

Duration (in milliseconds) to wait after press down before calling `onPressIn`.

| Type |
| --- |
| number |

### delayLongPress​

Duration (in milliseconds) from `onPressIn` before `onLongPress` is called.

| Type | Default |
| --- | --- |
| number | 500 |

### disabled​

Whether the press behavior is disabled.

| Type | Default |
| --- | --- |
| boolean | false |

### hitSlop​

Sets additional distance outside of element in which a press can be detected.

| Type |
| --- |
| Rector number |

### onHoverIn​

Called when the hover is activated to provide visual feedback.

| Type |
| --- |
| ({ nativeEvent:MouseEvent}) => void |

### onHoverOut​

Called when the hover is deactivated to undo visual feedback.

| Type |
| --- |
| ({ nativeEvent:MouseEvent}) => void |

### onLongPress​

Called if the time after `onPressIn` lasts longer than 500 milliseconds. This time period can be customized with [delayLongPress](#delaylongpress).

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

### onPress​

Called after `onPressOut`.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

### onPressIn​

Called immediately when a touch is engaged, before `onPressOut` and `onPress`.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

### onPressMove​

Called when the press location moves.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

### onPressOut​

Called when a touch is released.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

### pressRetentionOffset​

Additional distance outside of this view in which a touch is considered a press before `onPressOut` is triggered.

| Type | Default |
| --- | --- |
| Rector number | {bottom: 30, left: 20, right: 20, top: 20} |

### style​

Either view styles or a function that receives a boolean reflecting whether the component is currently pressed and returns view styles.

| Type |
| --- |
| View Styleor({ pressed: boolean }) =>View Style |

### testOnly_pressed​

Used only for documentation or testing (e.g. snapshot testing).

| Type | Default |
| --- | --- |
| boolean | false |

## Type Definitions​

### RippleConfig​

Ripple effect configuration for the `android_ripple` property.

| Type |
| --- |
| object |

**Properties:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| color | color | No | Defines the color of the ripple effect. |
| borderless | boolean | No | Defines if ripple effect should not include border. |
| radius | number | No | Defines the radius of the ripple effect. |
| foreground | boolean | No | Set to true to add the ripple effect to the foreground of the view, instead of the background. This is useful if one of your child views has a background of its own, or you're e.g. displaying images, and you don't want the ripple to be covered by them. |

Is this page useful?

---

# PressEvent Object Type

> PressEvent object is returned in the callback as a result of user press interaction, for example onPress in Button component.

`PressEvent` object is returned in the callback as a result of user press interaction, for example `onPress` in [Button](https://reactnative.dev/docs/button) component.

## Example​

 js

```
{    changedTouches: [PressEvent],    identifier: 1,    locationX: 8,    locationY: 4.5,    pageX: 24,    pageY: 49.5,    target: 1127,    timestamp: 85131876.58868201,    touches: []}
```

## Keys and values​

### changedTouches​

Array of all PressEvents that have changed since the last event.

| Type | Optional |
| --- | --- |
| array of PressEvents | No |

### forceiOS​

Amount of force used during the 3D Touch press. Returns the float value in range from `0.0` to `1.0`.

| Type | Optional |
| --- | --- |
| number | Yes |

### identifier​

Unique numeric identifier assigned to the event.

| Type | Optional |
| --- | --- |
| number | No |

### locationX​

Touch origin X coordinate inside touchable area (relative to the element).

| Type | Optional |
| --- | --- |
| number | No |

### locationY​

Touch origin Y coordinate inside touchable area (relative to the element).

| Type | Optional |
| --- | --- |
| number | No |

### pageX​

Touch origin X coordinate on the screen (relative to the root view).

| Type | Optional |
| --- | --- |
| number | No |

### pageY​

Touch origin Y coordinate on the screen (relative to the root view).

| Type | Optional |
| --- | --- |
| number | No |

### target​

The node id of the element receiving the PressEvent.

| Type | Optional |
| --- | --- |
| number,null,undefined | No |

### timestamp​

Timestamp value when a PressEvent occurred. Value is represented in milliseconds.

| Type | Optional |
| --- | --- |
| number | No |

### touches​

Array of all current PressEvents on the screen.

| Type | Optional |
| --- | --- |
| array of PressEvents | No |

## Used by​

- [Button](https://reactnative.dev/docs/button)
- [PanResponder](https://reactnative.dev/docs/panresponder)
- [Pressable](https://reactnative.dev/docs/pressable)
- [ScrollView](https://reactnative.dev/docs/scrollview)
- [Text](https://reactnative.dev/docs/text)
- [TextInput](https://reactnative.dev/docs/textinput)
- [TouchableHighlight](https://reactnative.dev/docs/touchablenativefeedback)
- [TouchableOpacity](https://reactnative.dev/docs/touchablewithoutfeedback)
- [TouchableNativeFeedback](https://reactnative.dev/docs/touchablenativefeedback)
- [TouchableWithoutFeedback](https://reactnative.dev/docs/touchablewithoutfeedback)
- [View](https://reactnative.dev/docs/view)

Is this page useful?

---

# Profiling

> Profiling is the process of analyzing an app's performance, resource usage, and behavior to identify potential bottlenecks or inefficiencies. It's worth making use of profiling tools to ensure your app works smoothly across different devices and conditions.

Profiling is the process of analyzing an app's performance, resource usage, and behavior to identify potential bottlenecks or inefficiencies. It's worth making use of profiling tools to ensure your app works smoothly across different devices and conditions.

For iOS, Instruments is an invaluable tool, and on Android you should learn to use the [Android Studio Profiler](https://reactnative.dev/docs/profiling#profiling-android-ui-performance-with-system-tracing).

But first, [make sure that Development Mode is OFF!](https://reactnative.dev/docs/performance#running-in-development-mode-devtrue).

## Profiling Android UI Performance with System Tracing​

Android supports 10k+ different phones and is generalized to support software rendering: the framework architecture and need to generalize across many hardware targets unfortunately means you get less for free relative to iOS. But sometimes, there are things you can improve -- and many times it's not native code's fault at all!

The first step for debugging this jank is to answer the fundamental question of where your time is being spent during each 16ms frame. For that, we'll be using the [built-in System Tracing profiler in the Android Studio](https://developer.android.com/studio/profile).

 note

The standalone `systrace` tool has been removed from Android platform-tools. Use the Android Studio Profiler instead, which provides the same functionality with a better user interface.

### 1. Collecting a trace​

First, connect a device that exhibits the stuttering you want to investigate to your computer via USB. Open your project's `android` folder in Android Studio, select your device in the top right pane, and [run your project as profileable](https://developer.android.com/studio/profile#build-and-run).

When your app is built as profileable and is running on the device, get your app to the point right before the navigation/animation you want to profile and start the ["Capture System Activities" task](https://developer.android.com/studio/profile#start-profiling) in the Android Studio Profiler pane.

Once the trace starts collecting, perform the animation or interaction you care about. Then press "Stop recording". You can now [inspect the trace directly in the Android Studio](https://developer.android.com/studio/profile/jank-detection). Alternatively, you can select it in the "Past Recordings" pane, press "Export recording", and open it in a tool like [Perfetto](https://perfetto.dev/).

### 2. Reading the trace​

After opening the trace in Android Studio or Perfetto, you should see something like this:

![Example](https://reactnative.dev/assets/images/SystraceExample-05b3ea44681d0291c1040e5f655fcd95.png)

 Hint

Use the WASD keys to strafe and zoom.

The exact UI might be different but the instructions below will apply regardless of the tool you're using.

 Enable VSync highlighting

Check this checkbox at the top right of the screen to highlight the 16ms frame boundaries:

![Enable VSync Highlighting](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIQAAAAwCAIAAABffUWTAAALlUlEQVR4AdSPWaEFARSCpn88RU6ct94S8+8CT2SKLp2XdsI2VAew9HqlnNs6pKXgomYT5jL0KHRbVradadrjcraUbsjQyXbDo8NYvGtu84xH8daUY9elLbSZC20KGxpkbq1XMz1ep/bQTuvRWaqFdN46d+QuadvFOjHzZJy2R9bNApQ2d9ayjfVyFD3P4Lb0PJZ5veqhd17GCjlTaY4eu5N56Y27InakJmXL1kqULmaXbqy0vE7tEeKxVEtXbsugCZ5O0m6uNyUrru0sm1Bga43NTjJKN900Wzc5mHRr7giS2ZaxhXGseCticjNbLwVKaQGbYHdVP3PccnFnp0gP2evUHjpoZa3Vdg1iiTIkF2+M0sqwuGxrhrQlM5IFqGGUq6lUMqx3XosXs11vkLiu6+LiYHVLZ2RjalxbuXXKaKgNE9du7qyfOrqUvU7tmx2r4G4jScL9c6wck6RjJsPy7qOl8OKjGEL229gOGSXrNqaQSYrDEZrGl5OVzTmyYIQzDi4zQ9i+r6c1GrXn5IOAAvrevH7VVV99Vd0laRKT9UXcMSCR0+8WnzvkIW/dMSiCvFloFFGrgrzxxhvYF9cCrhjDJQXk9VsDORgIBGILfAEhEJOpFQsEgjKsfABBCOrjUIConDHyCGi1+PjiZJSTdSdQ28UmJuzr6bHZbH37vGjs5kIbxoULF7BfZJ1Jv1nr/uQPvRe/Zb327ZwHWzgRCqbe0GXJLUsIIS1yrl/2wlfnlRHdjGCNN39dEBCXqa1T2Ay/7CUKIa+CQkBc5w/a6lq8MV5ZFirAXraPYwb74KuwBWALtmWEYonZbCYK6vYFNOYNr9wwzp8/v8i60fXx923XzJ3XftZ97efaA88VOBHCPHRZckc5IWablOuXJnDm5gkJtiSKsrxIXcm2hDSCqXp0CrIIhfw9g2km5glJH4WfKXB+T6OJkMdy+RPKATzwyF4DIc/3CSpf7KvBR8IkaP3f6KoNQzrlqS5HOcDU6Jg4rwM+/rh03D73dF6qcl/8ZdclhEDQJUn0LKYOifNNwIeLgOVofK7ZcYp5Hc3PobzB9JzDc7i5unkKcaQbSK3D0/EcMhB71AGvomBiCtJU49LnHKekPAqMWe7wOKpNTKARTmRlT7oXew2IdMPb6BFVh9gI4qPdilIzQg5EsjjlWKoITu2tLV/aoeV4OsrLa6ckyVH9XLdnorv6UVZbqwWtpSbWQG0HBp2BNoznwH/O6h4ft1thkip39ByPb1kXfidMr17qOfnN/Pz8y0e+wvcDBNB4pK3l0N04Pj3tz2B6etyOAzaNp2nUQAwN4zDsqAnnnkNKdaDcnVbTlcYOue1VtP9HlbxxmFBgRgOMPAog4CaA56x2BEzUbU2fi9qtG9GD6TnreBSkXEQ3grPUntlN78FuI7uK6CEDQc5Sq93tj6a1NFqkCZEuf5rt9iwFDVXU5pc22O17nlNqj1OKn/aHGm5cNaik6lDmqrVh0FO502fPnoXXZa1qsvuZnV2/beUm8dPOK0/0f3n1+pz4xlffbfoQHhDA5LNSrCE9cJU0aiKmpjHlzKgeZVn/HFqNvsdSsNMgoG3mT41ZcUoX/OowzqbGqDGWyqcAZhkmsSdzljHIGZpS1KZ+qz/Nd8s4j6jVYYP1KLMRnXZjr6Hs2QZ3RmEa9UxN47AzFe3T7HTk2d1pJRcDA8WdZr0ZhiIZTftSTOMgs7Vh4KMCGMpWb+8c+kfq7JkzZxDWVnUYP91x6SnHN+ZXLxltX8XfuXzt+txvmmfNOy6zYeiyUha0Zmg4nkxGIpFwOByJpJInD6DJ7aNJGlWGkRzdjqONJtWslMtALx12kk7LMsr8bBhj8CdHmUJ2GPkUGNMCpuJXhmHBMLIKzM+tkSH6bXBFzpwJb4RVeWABJxk+7jq4e3slZgYYDkao39UAvQ0RRJ31aNKJTtjprGOZ3KTToPjHmtQe+LrcMM6gwSFL5bOZ2T/bOXqGB+4a34ZKF/1d6j35TcvklzBafG99r/UzTCI7DB5JDAPXmeR8o/DhImDRdmGNWkCCgyHbN6ztBlKvBjSaepVZI68CCMxQMGqhF4GdpqAD64qsHkqG6VQsKifs3G3pdHLEk0MGelHHac7xTpCHwskD+Nw/0okcvnmtE/SgXQgPbRj19bsSpxkSg5WoUo9tLtg344fN78fe/Gpubv7S1bnZ974paXgDE8oOAzQeiXZcvLE9wflGjIRsG0nQqJEYYY1sI8RwIJSJhw5sQA7iIGzDeWBl8tqZX1NQjTwKjGk8ppYfQT0DbUZT+Hd4bXAVvmcbKkGpzEgitx538szfOeIIDvfIDuYLbUBO/bZHkMP64JtXO0EPSFr1mipxoNJo3HCM2dowgPUDvvjs7Gz8RHsp+AOzPNgLHC/t72yS3/vsMuZRaj3DfqDwIAQCaDzikMIw4pzPRy8CpRClw/DNxiefQfmHt/lm4jO+ASMBSlkr20rIJliZPDoM7DQFzcijAAKuQC3vQ70SNJNRWMPOq0f8GLqmEu0+zTe5U3FtQglg5oSvfRWtM3AiK/4wtmhCFeWa1zo5MaB0up+ax3AitDHDKNowhl+BVhYPDwdiMo/f93zD/mn7E9s3P2yQ/touf7flU2zZgxAI8kLE2qBa2hbjfD4cdasvRqNosM1HncGjK0sIw8r1K5FzFHEQSsgrYLI8oQ1+7JhCGyzVyKcAAirAYPC1laKeshPWK+T1LKZD/xqES/qDuT5UQL85gNawkBPupzlr+tmOb57rJDC8lagoXd+b7UAbhiRJsVhwShCEQFCUJMQkfl139IPsf/qMf7uYfVVgCydCIPBZ//0aE7zeILVF6hFacc4j4q1WwHlj/3u3YjAgKJekyw0O43LbhP9OUxSDwaDId8gNI51OL7JOhWdx3fj46/8cAufaI+8HIqf5rP9+9ZTiHCtsU6IY9R9eCfshm3i7FW5kjXq9R1qfxveiNXoDOtow0gWF/3DrX4mKh1r9BVC4AUQ9Sum/9k1Eb0RGG0bqDkBEQWEVCghtGMlkEvsCrsWVG0YikSjgWlxrVZBEEXcMSLyIOwYkVsQdAyIWcceAtBVxx4DM5wchiN47uPNP+l8N44MPPggpwO8atlevXhUUzM3NYYsVtt/vh3EPDGNyctLpdH7xxRe6o3Hbgg2jp6enrq6ut7e3r68PfTz44IN79+61WCytra2Itv+LWjPQVCCIwvBb9AChB4hAIpFACIWElCCVSCpAEBGBEgKlQgRKBNAL9BJVSZGqZVnuxzDGvTAw7AXmbHvs/89//jO7zfT7vV5vNBpxz38XY7lc8r6/2Wx8Ph81p1Izz1RDDGa/XC7fbrfP50P4eDyy2ay4HolETqdTIBBwHIcwmUze73eRy55Jt9uNx+ONRmM4HHo8nslkwvXpdBqLxUKh0OVycZsY3+8XbGhgWRa7oZhDpXY8Hg0y1RcjHA6XSiWeR0W832+/3w9cehcPPhwO1WpV3J/L5SREPvQrlQqDQqGw3W5t206lUtDzer2w5ZAvfnebGJACXiKRyGQyzCx6qNT478sgU/02hRuEKtFoFBAsHsFgsNlsIgZ1UavV/kJkdaH5MlgsFtfrldxOpwO41WpFVj6f5/CW28SgzoQzGFP77MGp1AgNM9UQ4/l88tYlxTifzxhQmBrEEKC9Ug74F0tyUULc7/cMZrMZHhIQ6XWckRW/ttttFzqDA5zMo2BKX1KpUZGmmWq1KdY05h03jMdjwnq9XiwWsSHFwg3r9ZrGRchrhszl415AnM/nEiJMWPxJpxVQTS5cwHe7HVzS6fRgMPhNzTxT3e8M/IEJZIhJX6+X+mur1dJ8JLk/q66uJimwGhoaaKEY06eQHP/hwwdkrwG59PEpRZ0+yhXT33D6+3RoRsZoZAwiMAre4QbAhva7EQEI+/TRo/fXr3+gNRqNjNHIIBaMRsZoZIxGxmhkAAAFB1URZ+TqrQAAAABJRU5ErkJggg==)

You should see zebra stripes as in the screenshot above. If you don't, try profiling on a different device: Samsung has been known to have issues displaying vsyncs while the Nexus series is generally pretty reliable.

### 3. Find your process​

Scroll until you see (part of) the name of your package. In this case, I was profiling `com.facebook.adsmanager`, which shows up as `book.adsmanager` because of silly thread name limits in the kernel.

On the left side, you'll see a set of threads which correspond to the timeline rows on the right. There are a few threads we care about for our purposes: the UI thread (which has your package name or the name UI Thread), `mqt_js`, and `mqt_native_modules`. If you're running on Android 5+, we also care about the Render Thread.

- **UI Thread.** This is where standard android measure/layout/draw happens. The thread name on the right will be your package name (in my case book.adsmanager) or UI Thread. The events that you see on this thread should look something like this and have to do with `Choreographer`, `traversals`, and `DispatchUI`:
  ![UI Thread Example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAN8AAAByCAIAAABcGZNLAAAPBUlEQVR4AezXgUbFUBwG8N41AHqEBD3AyJKgJyggUUBkS0iwVqYKM8WcN1hjMIExmzn39/cBh8t3vx9sr6676WmabptXVVUX3SlLJ510GkxZOuncUZ10KkunwZSlk046DaYsnXTSSaeydBpMWTrppNNgytJJJ50GU5ZOg9FZFGF6yjK0m7x+sDa6U5ZOOuk0mLJ00kmnwZSl02B0TgydytJpMGXppJNOgylLJ5100qksnQZTlk466TSYsnTSSafBlKXTYHSGeXd88dLn9OnyMDuZk7P7u+GnhqQ32fg1ebgavx7l6fh1+8m+n8Mqd5t/9f/PEjl/vP5X6qf9XbpOVDrppJNOOumkk84lvoreXj8O9hOJMu/l54rf7HQKnUInnUInnXTS+de+WfjGtVx/PD9ow5w4ZmZmZrYXvGBmZgqzOcxQZmYWlZmZWVBu/4nXT3KUq5X32XLdfc4q76xG1txzBz2f+z0zu+eO9942Vw1VFLY2W46Lpb91caTzmjesU3fTpcm+uxsv39s8N9V/v7vxoqtxsH35Zacz1HGlzXa69VnygikrnW7Lv2f3geqSribzTE5abVRY2mTfvdK8xibzrBes0/3ggJjRrusbf8yS4wp7W+YLsqyu9qridqdpyr089rio7KrijvLCVqZMRa+iU+m8H+gf3eWiNHXlfYPtKzWl3SnxRYcO+O7fe7i/bQl7s/XEzp17X/ua7bbaMZGo3PS6Y0eDWxtOdjovUMy4NdF7Oy2xdNu2bfHRuQIW3FOXy4zkitHum651qSLN1pR2URJEctPraS0kMHa48yoWhsEzI9Uneu9gsVYP0zjVu5suc1mcay/JdYQFJ7bbz2an1VCRKlFhqQwbD8AUmCAN0tcTHEs6n9W9xCVcttvPkDFSQ81IUY6d8iOdV0vyGinscziwteEUt7DnZ1qwlOY3gTUZLvkHkvIyzTLfse6bHqNT6RzruYVwjnbfWGWvLe2ODk+HBlPlIP/6oY6rFMMPUvLIIX9oZnVZjxbrieHOa6wlrnO85xa3eprnCrIsSBGNmCr6E2PyqAtbFMDbksF7GnUh9cB+H1YUoCGGxlngmIiMqf579EuGhWcYtIYlJb4YOe9wnPX3jUDdQZN+cfoUAEfGxgDSkyparCchlQdmtOcmbTaaZ3hC/I6FY6c6hakrjxNCy0MYF5UDhYXZNoCjOybOLWZBGRkAHdEjuwUZCaOlNTJUxz7UvlJZ1F6UY2O+jDklocSTdCqd8OG+30JUxLN3OS+gEPa6CdbPANdpmu58aueSDKvVaJqGg9jILEf9JJeCO+iEBMY76yeNusAKzUZdElThc9nyCrjsK8BIBBjRmuy7A69UwQJJDAmGstNqEWO6QxeHOlaMAtDJAPDOWCb67tIaqglVMmbqZqVUSeMkqUWbeRn16LelapiRwyITZ3bGFtZeN56faQ4NSpjqv0sV+UcBNFCSgVcaZMy1ZT3MAlFnSDxInqFT6QQgBG+gbcmw8B/H2Rl0CknmykGDMG650gm+IMjqopQsT1/LvKigEMaturKetegETaDEUXI0CQ9J4pYrnb4+oa50ypCe8mRCpUyVA3RHMSmAQkeGptB1UmwBFhw0bInmURd6qJuaULqKTtoUi/tjibQzNrBmSxARkgydxkiMjIw2ITqXDQPTt1QNwSiIe4xOPRXhmERsZEnE5a2ik5XGXbLSsk/tcJw3COMWgiEQZCRX4vRBUDZz4mTx47hICiA8bA9GXOjETbMTJYPz5ZZ4doCQfqk7PXBvFZ08J9ApzxVwjPfeMgrQKRoPJYxBCqC+onaZKZVNluP1Ff2INJcyEtdputNZXtCMcJLhLB/oF4kirkUn85Uq/CvYcHuSTqWTfRiHiW1PP6iFcVxgOYUSOf+y++Qu7JIBNcNOKstvkls56XWsDYtEU5xLjNZQRyycV8R9G3VlF8vaI9j8BR02l1KXv2BBa650MiRGi/umME0h2K4FOFFxEspMqQI7GZitdpx22GnQPhKI0JKnLkZ013WaRjIsHY5zMmaGRF+g706nNMuWmrm7ztdISqdnEps2+Y+vkwBrZI0vd+CMLaxxidKwM4Mkcd9sE43vB1b1QknDwiEMNWK9wUvqrpWoAmobmRcDW3WOZmDGUNdPjEe+c8CxrD8emYW7aiqd3p7kPM6xGpkUx7pOMvadL35SOr0noVgcXBQ7pVOT0ql0alI61/88esvnPvzJ7/z+uz/+xOyVFyl97sobmN3bXv+ZVyGaX/7CD57f++xKp9KpdCqdSqfSqXQqnUqn0ql0fnR6+UHXzCYqvm987k39p17NdPJ7ElGCryCdSueHJxenqp0fn1nZMM1LGWExH5xceOvgmTl7r7fRSSwI8W/8TrsFdI49jXDdfASd0vnx2ZWhsicB3uE+/rfbx7FctvV0FlTH+occ3rMfwqBzoMQEnX3F9V0F1ZQcLrPCKxkuqf7+8bmqxCwuC6KT3jF8/rylk3xlQuYb+06eNbfT4I3W0f27du987fb5p7AiqNb0grL4dIpdbR7eYjqJaaJfgtx6mi6/bEA+P8QTZATEFCbUiIgt91h3I/yeqGQJIqkoaqMY0dPU5ZIfYHmhADp5EjZPp9L5qHu2ODYFyF7feyI+IBQKT9S1kPnAxPyp+taO/CoyKcGRH5tZLoxJHq+0cQm4ZD40uUCxdw5fgFQSTZ2zdAyXWd4zdgmsQfBB1zT4vmvkIpfvGrmAow894vu45zgdAetbBs7QddAhH1reSjolWI6Q5LUD8q8TiERMoISfttnOuMe6G+H3ZIBb3naCVEKhSVKSCCkP0Kme/Y39pxYc/eglHhlWpqud11pGsD/ungUvcMT+0ZmlioQMyMNeHp8OlGTg9VbbGFXYmIImBaATrfU/eISSwEf1RWd/b1GddAT3K01DYpc9Q3po9BbTCYKwOLJuQD6hyry8gXxKNP6qWHfXuGNeSgFo4j4lVgsQwRo0KeABOpXOm61jKBnc3Gobz42Md6XzkTudo5ewGxlcOXTi6NNCouZsPZds3f0lplV04ugNOmnZlU5p+bnT6R6Qz10yuHUp4Bbrfs+gk4R28vYSMtzpPE8j6G5Dzai1egTv/9/SqXSOVjQgnGTutE8kBobh2d3pROHWovNm2xh32W5yOVreMFhqFjrx41IdYc4Kj6VZNg9JQeGorCudz0s72VyuE5BPnhBjtqESO+wW627Qed94yxTdBVzeS2G7yWVZQXNJnhM6sSidm6eT3SHPPeJnSs1DRO91TELn9Wd0dhfWwFB+VOLL0Smeffy0qY0TDy3YMorYYnJIcmQWs5d92DVDdYqxeaXlY/sPkQFTaRa7tLzFdMr7JLw6ggteKyAfI6jhxCXEeHWsu0v4PS8zATGtUYAXmnm7mkvkEzUFdEilltK5eTpJH55afN/YZTIfmVri283NfbXJIUmaEsuqdnD076ULr/m+E+zWCcjfcKy78RLBVeMWrBPJ79aO0qm/Fb0gSen0/qR0Kp1Kp9KpdCqdSqfb56vvf/fj7mZvTt/55MfWn8Kvv/ttiv3rH383LD/7/q+Wxx69StIH3/AZTyCndCqdSqfSqXQqnUqn0ql0Kp1K5/2OxgvWmrPmKtK8rV6MD7uaLlprPMUZrV221a2yzLlYrjZZVxotZBjA7TaHN9N5omNhYeS+0rlFdF5qqN3xmv/vKczpK86tTIiJD/C70+641+HsLMh+1NX0n4JYkxTnjvXddkfQoYOurWEJOHgARuWyLS/TkpZEJs7f90RtuTfTGR0cf673qtK5RXQiV1G+Po+ecQOU9swU6GzMSoMnWNm7Yzv4ksFYFhdtSk3EUpccD1vUasp+EsoOfGdMVYsOE/kje3ejf1KRNFNderfdSYHy+GjutudlCp2JgX4GnTwbdEomIzT4dH2lF9I5ZD/O4NNic3bv3Huh/wYKWp5VH+ATMtp4usc8gXH7a7Y3VvbMD9/NTy5bHHlwums5NTqbzPm+a2WZdUtjD5XOTdKJjBnCNm9/cnm7zR7rdwwR9dm3l/zNVpvv/n23Wu2Q11WQDZQlsVG9RbnobmZYMJfUivA5Cm3Rvj4TlcXXWxrg8lqzddlpPrBrJy1Q8VRdhYjozRbbWnSmhwZ5IZ2gBn/8PdExL3TOts8B64jz1KWB20cO+FwevA2XwHpp4GaYf9T5vuu9lkkKUHLQNmspavbYYJROgINL6HnQ2YisFsdEnjFVIpwkgVWKoYVk0MupqhJrWpLQJuKHRWgjXWmyUoUNg3SRFxkmdKaFBBl0Ajqe3WvpHHWeqst3SD4zPh/mplsvVuVaxXKu99pAw4yttE3ANRc1jThOmgobEdEh+wkyUy0XlE7P0DlQkm/PSDG0jTPTeEVxSnAA4nejpcGVztK4KEhCI2ELfClDecFruKzAoBO3LqzLTsCgM+TIIVc6R8oLvZbOlup+IJN8blKJK52gCZSo43jT2biwZG5NNp/HlRenVU21XsT7Z8YXzA3dVTo3TydeG1BIC3YT/ggL9KB2gIjCCbhklp0WGOXQI76YHWprbgYyySXnfVSWkqKdsJsU6M8lmwE8O1jTmiudyDCdHq8tE3wh9Zy52mvpZJcZG5q4NPqQ03qwb7grnbBYlFZJ5uLAzX17DlwauDU3dMfnoG9ltpnyvocDClMrNt+10glJ21w+cmQWz/ugq4lTPDtF2CqJjUQCQYoTEpdPpdTGV1FU4aDNNhQRPW+pRjWf4Nhqw1NTkruj5YWuflzoJCNHKGTbOCp586kIFeTcw84yJTpL6KzObcAOjiDIXjMpMoO/+HeM6bG5fdYp2QZ0mcaUzlfw23gUVHgSweOERDLu4voRSDJsUoU/MoZPp8o6LVOSk5NU9/5v44GSM7i7fXH0AbckPz98z5OdKp0bT6CGLoKm/lb03JLSub7abQGXSqfSqb+zK51Kp9KpdHrV549//ONz7P2rv/3WrS+/fq30qz//9oWZrNKpdCqdSqfS6Z0fpVPpVDqVTqVT6VQ6lU6lU+lUOpVOpVPpVDqVTqVT6VQ6lU6lU+lUOpVOpVPpVDqVTqVT6VQ6lU6lU+lUOpVOpVPpVDr/9reXNp7+8Y+XvPPDgr30wn10skqn0ql06oLpZJVOpfNF+vwbMG/3LSYXRc8AAAAASUVORK5CYII=)
- **JS Thread.** This is where JavaScript is executed. The thread name will be either `mqt_js` or `<...>` depending on how cooperative the kernel on your device is being. To identify it if it doesn't have a name, look for things like `JSCall`, `Bridge.executeJSCall`, etc:
  ![JS Thread Example](data:image/png;base64,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)
- **Native Modules Thread.** This is where native module calls (e.g. the `UIManager`) are executed. The thread name will be either `mqt_native_modules` or `<...>`. To identify it in the latter case, look for things like `NativeCall`, `callJavaModuleMethod`, and `onBatchComplete`:
  ![Native Modules Thread Example](data:image/png;base64,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)
- **Bonus: Render Thread.** If you're using Android L (5.0) and up, you will also have a render thread in your application. This thread generates the actual OpenGL commands used to draw your UI. The thread name will be either `RenderThread` or `<...>`. To identify it in the latter case, look for things like `DrawFrame` and `queueBuffer`:
  ![Render Thread Example](data:image/png;base64,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)

## Identifying a culprit​

A smooth animation should look something like the following:

![Smooth Animation](https://reactnative.dev/assets/images/SystraceWellBehaved-82dfa037cb9e1d29d7daae2d6dba2ffc.png)

Each change in color is a frame -- remember that in order to display a frame, all our UI work needs to be done by the end of that 16ms period. Notice that no thread is working close to the frame boundary. An application rendering like this is rendering at 60 FPS.

If you noticed chop, however, you might see something like this:

![Choppy Animation from JS](https://reactnative.dev/assets/images/SystraceBadJS-b8518ae5e520b074ccc7722fcf30b7ed.png)

Notice that the JS thread is executing almost all the time, and across frame boundaries! This app is not rendering at 60 FPS. In this case, **the problem lies in JS**.

You might also see something like this:

![Choppy Animation from UI](https://reactnative.dev/assets/images/SystraceBadUI-cc4bb271e7a568efc7933d1c6f453d67.png)

In this case, the UI and render threads are the ones that have work crossing frame boundaries. The UI that we're trying to render on each frame is requiring too much work to be done. In this case, **the problem lies in the native views being rendered**.

At this point, you'll have some very helpful information to inform your next steps.

## Resolving JavaScript issues​

If you identified a JS problem, look for clues in the specific JS that you're executing. In the scenario above, we see `RCTEventEmitter` being called multiple times per frame. Here's a zoom-in of the JS thread from the trace above:

![Too much JS](https://reactnative.dev/assets/images/SystraceBadJS2-f454f409a22625f659d465abdab06ce0.png)

This doesn't seem right. Why is it being called so often? Are they actually different events? The answers to these questions will probably depend on your product code. And many times, you'll want to look into [shouldComponentUpdate](https://react.dev/reference/react/Component#shouldcomponentupdate).

## Resolving native UI Issues​

If you identified a native UI problem, there are usually two scenarios:

1. the UI you're trying to draw each frame involves too much work on the GPU, or
2. You're constructing new UI during the animation/interaction (e.g. loading in new content during a scroll).

### Too much GPU work​

In the first scenario, you'll see a trace that has the UI thread and/or Render Thread looking like this:

![Overloaded GPU](https://reactnative.dev/assets/images/SystraceBadUI-cc4bb271e7a568efc7933d1c6f453d67.png)

Notice the long amount of time spent in `DrawFrame` that crosses frame boundaries. This is time spent waiting for the GPU to drain its command buffer from the previous frame.

To mitigate this, you should:

- investigate using `renderToHardwareTextureAndroid` for complex, static content that is being animated/transformed (e.g. the `Navigator` slide/alpha animations)
- make sure that you are **not** using `needsOffscreenAlphaCompositing`, which is disabled by default, as it greatly increases the per-frame load on the GPU in most cases.

### Creating new views on the UI thread​

In the second scenario, you'll see something more like this:

![Creating Views](https://reactnative.dev/assets/images/SystraceBadCreateUI-fc9d228fc136be3574c0c5805ac0d7b5.png)

Notice that first the JS thread thinks for a bit, then you see some work done on the native modules thread, followed by an expensive traversal on the UI thread.

There isn't a quick way to mitigate this unless you're able to postpone creating new UI until after the interaction, or you are able to simplify the UI you're creating. The react native team is working on an infrastructure level solution for this that will allow new UI to be created and configured off the main thread, allowing the interaction to continue smoothly.

### Finding native CPU hotspots​

If the problem seems to be on the native side, you can use the [CPU hotspot profiler](https://developer.android.com/studio/profile/record-java-kotlin-methods) to get more details on what's happening. Open the Android Studio Profiler panel and select "Find CPU Hotspots (Java/Kotlin Method Recording)".

 Choose the Java/Kotlin recording

Make sure you select "Find CPU Hotspots **(Java/Kotlin Recording)**" rather than "Find CPU Hotspots (Callstack Sample)". They have similar icons but do different things.

Perform the interactions and press "Stop recording". Recording is resource-intensive, so keep the interaction short. You can then either inspect the resulting trace in the Android Studio or export it and open it in an online tool like [Firefox Profiler](https://profiler.firefox.com/).

Unlike System Trace, CPU hotspot profiling is slow so it won't give you accurate measurements. However, it should give you an idea of what native methods are being called, and where the time is being spent proportionally during each frame.

Is this page useful?

---

# Props

> Most components can be customized when they are created, with different parameters. These created parameters are called props, short for properties.

Most components can be customized when they are created, with different parameters. These created parameters are called `props`, short for properties.

For example, one basic React Native component is the `Image`. When you create an image, you can use a prop named `source` to control what image it shows.

Notice the braces surrounding `{pic}` - these embed the variable `pic` into JSX. You can put any JavaScript expression inside braces in JSX.

Your own components can also use `props`. This lets you make a single component that is used in many different places in your app, with slightly different properties in each place by referring to `props` in your `render` function. Here's an example:

Using `name` as a prop lets us customize the `Greeting` component, so we can reuse that component for each of our greetings. This example also uses the `Greeting` component in JSX, similar to the [Core Components](https://reactnative.dev/docs/intro-react-native-components). The power to do this is what makes React so cool - if you find yourself wishing that you had a different set of UI primitives to work with, you can invent new ones.

The other new thing going on here is the [View](https://reactnative.dev/docs/view) component. A [View](https://reactnative.dev/docs/view) is useful as a container for other components, to help control style and layout.

With `props` and the basic [Text](https://reactnative.dev/docs/text), [Image](https://reactnative.dev/docs/image), and [View](https://reactnative.dev/docs/view) components, you can build a wide variety of static screens. To learn how to make your app change over time, you need to [learn about State](https://reactnative.dev/docs/state).

Is this page useful?

---

# Publishing to Apple App Store

> The publishing process is the same as any other native iOS app, with some additional considerations to take into account.

The publishing process is the same as any other native iOS app, with some additional considerations to take into account.

 info

If you are using Expo, read the Expo guide for [Deploying to App Stores](https://docs.expo.dev/distribution/app-stores/) to build and submit your app for the Apple App Store. This guide works with any React Native app to automate the deployment process.

### 1. Configure release scheme​

Building an app for distribution in the App Store requires using the `Release` scheme in Xcode. Apps built for `Release` will automatically disable the in-app Dev Menu, which will prevent your users from inadvertently accessing the menu in production. It will also bundle the JavaScript locally, so you can put the app on a device and test whilst not connected to the computer.

To configure your app to be built using the `Release` scheme, go to **Product** → **Scheme** → **Edit Scheme**. Select the **Run** tab in the sidebar, then set the Build Configuration dropdown to `Release`.

![image](https://reactnative.dev/assets/images/ConfigureReleaseScheme-68e17e8d9a2cf2b73adb47865b45399d.png)

#### Pro Tips​

The static bundle is built every time you target a physical device, even in Debug. If you want to save time, turn off bundle generation in Debug by adding the following to your shell script in the Xcode Build Phase `Bundle React Native code and images`:

 shell

```
if [ "${CONFIGURATION}" == "Debug" ]; then  export SKIP_BUNDLING=true fi
```

### 2. Build app for release​

You can now build your app for release by tapping Cmd ⌘ + B or selecting **Product** → **Build** from the menu bar. Once built for release, you'll be able to distribute the app to beta testers and submit the app to the App Store.

 info

You can also use the `React Native CLI` to perform this operation using the option `--mode` with the value `Release` (e.g. from the root of your project: `npm run ios -- --mode="Release"` or `yarn ios --mode Release`).

Once you are done with the testing and ready to publish to App Store, follow along with this guide.

- Launch your terminal, and navigate into the iOS folder of your app and type `open .`.
- Double click on YOUR_APP_NAME.xcworkspace. It should launch Xcode.
- Click on `Product` → `Archive`. Make sure to set the device to "Any iOS Device (arm64)".

 note

Check your Bundle Identifier and make sure it is exactly same as the one you have created in the Identifiers in Apple Developer Dashboard.

- After the archive is completed, in the archive window, click on `Distribute App`.
- Click on `App Store Connect` now (if you want to publish in App Store).
- Click `Upload` → Make sure all the checkboxes are selected, hit `Next`.
- Choose between `Automatically manage signing` and `Manually manage signing` based on your needs.
- Click on `Upload`.
- Now you can find it in the App Store Connect under TestFlight.

Now fill up the necessary information and in the Build Section, select the build of the app and click on `Save` → `Submit For Review`.

### 3. Screenshots​

The Apple Store requires you have screenshots for the latest devices. The reference for such devices would be found [here](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications/). Note that screenshots for some display sizes are not required if they are provided for other sizes.

Is this page useful?
