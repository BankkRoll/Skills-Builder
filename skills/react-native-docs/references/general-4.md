# BoxShadowValue Object Type and more

# BoxShadowValue Object Type

> The BoxShadowValue object is taken by the boxShadow style prop. It is comprised of 2-4 lengths, an optional color, and an optional inset boolean. These values collectively define the box shadow's color, position, size, and blurriness.

The `BoxShadowValue` object is taken by the [boxShadow](https://reactnative.dev/docs/view-style-props#boxshadow) style prop. It is comprised of 2-4 lengths, an optional color, and an optional `inset` boolean. These values collectively define the box shadow's color, position, size, and blurriness.

## Example​

 js

```
{  offsetX: 10,  offsetY: -3,  blurRadius: '15px',  spreadDistance: '10px',  color: 'red',  inset: true,}
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

### blurRadius​

Represents the radius used in the [Gaussian blur](https://en.wikipedia.org/wiki/Gaussian_blur) algorithm. The larger the value the blurrier the shadow is. Only non-negative values are valid. The default is 0.

| Type | Optional |
| --- | --- |
| number | string | Yes |

### spreadDistance​

How much larger or smaller the shadow grows or shrinks. A positive value will grow the shadow, a negative value will shrink the shadow.

| Type | Optional |
| --- | --- |
| number | string | Yes |

### color​

The color of the shadow. The default is `black`.

| Type | Optional |
| --- | --- |
| color | Yes |

### inset​

Whether the shadow is inset or not. Inset shadows will appear around the inside of the element's border box as opposed to the outside.

| Type | Optional |
| --- | --- |
| boolean | Yes |

## Used by​

- [boxShadow](https://reactnative.dev/docs/view-style-props#boxshadow)

Is this page useful?

---

# Speeding up your Build phase

> Building your React Native app could be expensive and take several minutes of developers time.

Building your React Native app could be **expensive** and take several minutes of developers time.
This can be problematic as your project grows and generally in bigger organizations with multiple React Native developers.

To mitigate this performance hit, this page shares some suggestions on how to **improve your build time**.

 info

Please note that those suggestions are advanced feature that requires some amount of understanding of how the native build tools work.

## Build only one ABI during development (Android-only)​

When building your android app locally, by default you build all the 4 [Application Binary Interfaces (ABIs)](https://developer.android.com/ndk/guides/abis) : `armeabi-v7a`, `arm64-v8a`, `x86` & `x86_64`.

However, you probably don't need to build all of them if you're building locally and testing your emulator or on a physical device.

This should reduce your **native build time** by a ~75% factor.

If you're using the React Native CLI, you can add the `--active-arch-only` flag to the `run-android` command. This flag will make sure the correct ABI is picked up from either the running emulator or the plugged in phone. To confirm that this approach is working fine, you'll see a message like `info Detected architectures arm64-v8a` on console.

```
$ yarn react-native run-android --active-arch-only[ ... ]info Running jetifier to migrate libraries to AndroidX. You can disable it using "--no-jetifier" flag.Jetifier found 1037 file(s) to forward-jetify. Using 32 workers...info JS server already running.info Detected architectures arm64-v8ainfo Installing the app...
```

This mechanism relies on the `reactNativeArchitectures` Gradle property.

Therefore, if you're building directly with Gradle from the command line and without the CLI, you can specify the ABI you want to build as follows:

```
$ ./gradlew :app:assembleDebug -PreactNativeArchitectures=x86,x86_64
```

This can be useful if you wish to build your Android App on a CI and use a matrix to parallelize the build of the different architectures.

If you wish, you can also override this value locally, using the `gradle.properties` file you have in the [top-level folder](https://github.com/facebook/react-native/blob/19cf70266eb8ca151aa0cc46ac4c09cb987b2ceb/template/android/gradle.properties#L30-L33) of your project:

```
# Use this property to specify which architecture you want to build.# You can also override it from the CLI using# ./gradlew <task> -PreactNativeArchitectures=x86_64reactNativeArchitectures=armeabi-v7a,arm64-v8a,x86,x86_64
```

Once you build a **release version** of your app, don't forget to remove those flags as you want to build an apk/app bundle that works for all the ABIs and not only for the one you're using in your daily development workflow.

## Enable Configuration Caching (Android-only)​

Since React Native 0.79, you can also enable Gradle Configuration Caching.

When you’re running an Android build with `yarn android`, you will be executing a Gradle build that is composed by two steps ([source](https://docs.gradle.org/current/userguide/build_lifecycle.html)):

- Configuration phase, when all the `.gradle` files are evaluated.
- Execution phase, when the tasks are actually executed so the Java/Kotlin code is compiled and so on.

You will now be able to enable Configuration Caching, which will allow you to skip the Configuration phase on subsequent builds.

This is beneficial when making frequent changes to the native code as it improves build times.

For example here you can see how rebuilding faster it is to rebuild RN-Tester after a change in the native code:

![gradle config caching](https://reactnative.dev/assets/images/gradle-config-caching-dd203827a57e8eb16b2b26c02a0725d8.gif)

You can enable Gradle Configuration Caching by adding the following line in your `android/gradle.properties` file:

```
org.gradle.configuration-cache=true
```

Please refer to the [official Gradle documentation](https://docs.gradle.org/current/userguide/configuration_cache.html) for more resources on Configuration Caching.

## Using a Maven Mirror (Android-only)​

When building Android apps, your Gradle builds will need to download the necessary dependencies from Maven Central and other repositories from the internet.

If your organization is running a Maven repository mirror, you should consider using it as it will speed up your build, by downloading the artifacts from the mirror rather than from the internet.

You can configure a mirror by specifying the `exclusiveEnterpriseRepository` property in your `android/gradle.properties` file:

 diff

```
# Use this property to enable or disable the Hermes JS engine.# If set to false, you will be using JSC instead.hermesEnabled=true# Use this property to configure a Maven enterprise repository# that will be used exclusively to fetch all of your dependencies.+exclusiveEnterpriseRepository=https://my.internal.proxy.net/
```

By setting this property, your build will fetch dependencies **exclusively** from your specified repository and not from others.

## Use a compiler cache​

If you're running frequent native builds (either C++ or Objective-C), you might benefit from using a **compiler cache**.

Specifically you can use two type of caches: local compiler caches and distributed compiler caches.

### Local caches​

 info

The following instructions will work for **both Android & iOS**.
If you're building only Android apps, you should be good to go.
If you're building also iOS apps, please follow the instructions in the [Xcode Specific Setup](#xcode-specific-setup) section below.

We suggest to use [ccache](https://ccache.dev/) to cache the compilation of your native builds.
Ccache works by wrapping the C++ compilers, storing the compilation results, and skipping the compilation
if an intermediate compilation result was originally stored.

Ccache is available in the package manager for most operating systems. On macOS, we can install ccache with `brew install ccache`.
Or you can follow the [official installation instructions](https://github.com/ccache/ccache/blob/master/doc/install.md) to install from source.

You can then do two clean builds (e.g. on Android you can first run `yarn react-native run-android`, delete the `android/app/build` folder and run the first command once more). You will notice that the second build was way faster than the first one (it should take seconds rather than minutes).
While building, you can verify that `ccache` works correctly and check the cache hits/miss rate `ccache -s`

```
$ ccache -sSummary:  Hits:             196 /  3068 (6.39 %)    Direct:           0 /  3068 (0.00 %)    Preprocessed:   196 /  3068 (6.39 %)  Misses:          2872    Direct:        3068    Preprocessed:  2872  Uncacheable:        1Primary storage:  Hits:             196 /  6136 (3.19 %)  Misses:          5940  Cache size (GB): 0.60 / 20.00 (3.00 %)
```

Note that `ccache` aggregates the stats over all builds. You can use `ccache --zero-stats` to reset them before a build to verify the cache-hit ratio.

Should you need to wipe your cache, you can do so with `ccache --clear`

#### Xcode Specific Setup​

To make sure `ccache` works correctly with iOS and Xcode, you need to enable React Native support for ccache in `ios/Podfile`.

Open `ios/Podfile` in your editor and uncomment the `ccache_enabled` line.

 ruby

```
post_install do |installer|    # https://github.com/facebook/react-native/blob/main/packages/react-native/scripts/react_native_pods.rb#L197-L202    react_native_post_install(      installer,      config[:reactNativePath],      :mac_catalyst_enabled => false,      # TODO: Uncomment the line below      :ccache_enabled => true    )  end
```

#### Using this approach on a CI​

Ccache uses the `/Users/$USER/Library/Caches/ccache` folder on macOS to store the cache.
Therefore you could save & restore the corresponding folder also on CI to speedup your builds.

However, there are a couple of things to be aware:

1. On CI, we recommend to do a full clean build, to avoid poisoned cache problems. If you follow the approach mentioned in the previous paragraph, you should be able to parallelize the native build on 4 different ABIs and you will most likely not need `ccache` on CI.
2. `ccache` relies on timestamps to compute a cache hit. This doesn't work well on CI as files are re-downloaded at every CI run. To overcome this, you'll need to use the `compiler_check content` option which relies instead on [hashing the content of the file](https://ccache.dev/manual/4.3.html).

### Distributed caches​

Similar to local caches, you might want to consider using a distributed cache for your native builds.
This could be specifically useful in bigger organizations that are doing frequent native builds.

We recommend to use [sccache](https://github.com/mozilla/sccache) to achieve this.
We defer to the sccache [distributed compilation quickstart](https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md) for instructions on how to setup and use this tool.

Is this page useful?

---

# 🗑️ Building For TV Devices

> TV devices support has been implemented with the intention of making existing React Native applications work on Apple TV and Android TV, with few or no changes needed in the JavaScript code for the applications.

TV devices support has been implemented with the intention of making existing React Native applications work on Apple TV and Android TV, with few or no changes needed in the JavaScript code for the applications.

 Deprecated

TV support has moved to the [React Native for TV](https://github.com/react-native-tvos/react-native-tvos#readme) repository. Please see the **README** there for information on projects for Apple TV or Android TV.

Is this page useful?

---

# Button

> A basic button component that should render nicely on any platform. Supports a minimal level of customization.

A basic button component that should render nicely on any platform. Supports a minimal level of customization.

If this button doesn't look right for your app, you can build your own button using [Pressable](https://reactnative.dev/docs/pressable). For inspiration, look at the [source code for the Button component](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/Components/Button.js).

 tsx

```
<Button  onPress={onPressLearnMore}  title="Learn More"  color="#841584"  accessibilityLabel="Learn more about this purple button"/>
```

## Example​

---

# Reference

## Props​

### RequiredonPress​

Handler to be called when the user taps the button.

| Type |
| --- |
| ({nativeEvent:PressEvent}) |

---

### Requiredtitle​

Text to display inside the button. On Android the given title will be converted to the uppercased form.

| Type |
| --- |
| string |

---

### accessibilityLabel​

Text to display for blindness accessibility features.

| Type |
| --- |
| string |

---

### accessibilityLanguageiOS​

A value indicating which language should be used by the screen reader when the user interacts with the element. It should follow the .

See the [iOSaccessibilityLanguagedoc](https://developer.apple.com/documentation/objectivec/nsobject/1615192-accessibilitylanguage) for more information.

| Type |
| --- |
| string |

---

### accessibilityActions​

Accessibility actions allow an assistive technology to programmatically invoke the actions of a component. The `accessibilityActions` property should contain a list of action objects. Each action object should contain the field name and label.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibility-actions) for more information.

| Type | Required |
| --- | --- |
| array | No |

---

### onAccessibilityAction​

Invoked when the user performs the accessibility actions. The only argument to this function is an event containing the name of the action to perform.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibility-actions) for more information.

| Type | Required |
| --- | --- |
| function | No |

---

### color​

Color of the text (iOS), or background color of the button (Android).

| Type | Default |
| --- | --- |
| color | '#2196F3'Android'#007AFF'iOS |

---

### disabled​

If `true`, disable all interactions for this component.

| Type | Default |
| --- | --- |
| bool | false |

---

### hasTVPreferredFocusTV​

TV preferred focus.

| Type | Default |
| --- | --- |
| bool | false |

---

### nextFocusDownAndroidTV​

Designates the next view to receive focus when the user navigates down. See the [Android documentation](https://developer.android.com/reference/android/view/View.html#attr_android:nextFocusDown).

| Type |
| --- |
| number |

---

### nextFocusForwardAndroidTV​

Designates the next view to receive focus when the user navigates forward. See the [Android documentation](https://developer.android.com/reference/android/view/View.html#attr_android:nextFocusForward).

| Type |
| --- |
| number |

---

### nextFocusLeftAndroidTV​

Designates the next view to receive focus when the user navigates left. See the [Android documentation](https://developer.android.com/reference/android/view/View.html#attr_android:nextFocusLeft).

| Type |
| --- |
| number |

---

### nextFocusRightAndroidTV​

Designates the next view to receive focus when the user navigates right. See the [Android documentation](https://developer.android.com/reference/android/view/View.html#attr_android:nextFocusRight).

| Type |
| --- |
| number |

---

### nextFocusUpAndroidTV​

Designates the next view to receive focus when the user navigates up. See the [Android documentation](https://developer.android.com/reference/android/view/View.html#attr_android:nextFocusUp).

| Type |
| --- |
| number |

---

### testID​

Used to locate this view in end-to-end tests.

| Type |
| --- |
| string |

---

### touchSoundDisabledAndroid​

If `true`, doesn't play system sound on touch.

| Type | Default |
| --- | --- |
| boolean | false |

Is this page useful?

---

# Color Reference

> Components in React Native are styled using JavaScript. Color properties usually match how CSS works on the web. General guides on the color usage on each platform could be found below:

Components in React Native are [styled using JavaScript](https://reactnative.dev/docs/style). Color properties usually match how [CSS works on the web](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value). General guides on the color usage on each platform could be found below:

- [Android](https://material.io/design/color/color-usage.html)
- [iOS](https://developer.apple.com/design/human-interface-guidelines/ios/visual-design/color/)

## Color APIs​

React Native has several color APIs designed to allow you to take full advantage of your platform's design and user preferences.

- [PlatformColor](https://reactnative.dev/docs/platformcolor) lets you reference the platform's color system.
- [DynamicColorIOS](https://reactnative.dev/docs/dynamiccolorios) is iOS specific and allows you to specify which colors should be used in light or Dark Mode.

## Color representations​

### Red Green Blue (RGB)​

React Native supports `rgb()` and `rgba()` in both hexadecimal and functional notation:

- `'#f0f'` (#rgb)
- `'#ff00ff'` (#rrggbb)
- `'#f0ff'` (#rgba)
- `'#ff00ff00'` (#rrggbbaa)
- `'rgb(255, 0, 255)'`
- `'rgb(255 0 255)'`
- `'rgba(255, 0, 255, 1.0)'`
- `'rgba(255 0 255 / 1.0)'`

### Hue Saturation Lightness (HSL)​

React Native supports `hsl()` and `hsla()` in functional notation:

- `'hsl(360, 100%, 100%)'`
- `'hsl(360 100% 100%)'`
- `'hsla(360, 100%, 100%, 1.0)'`
- `'hsla(360 100% 100% / 1.0)'`

### Hue Whiteness Blackness (HWB)​

React Native supports `hwb()` in functional notation:

- `'hwb(0, 0%, 100%)'`
- `'hwb(360, 100%, 100%)'`
- `'hwb(0 0% 0%)'`
- `'hwb(70 50% 0%)'`

### Color ints​

React Native supports also colors as an `int` values (in RGB color mode):

- `0xff00ff00` (0xrrggbbaa)

 caution

This might appear similar to the Android [Color](https://developer.android.com/reference/android/graphics/Color) ints representation but on Android values are stored in SRGB color mode (0xaarrggbb).

### Named colors​

In React Native you can also use color name strings as values.

 info

React Native only supports lowercase color names. Uppercase color names are not supported.

#### transparent​

This is a shortcut for `rgba(0,0,0,0)`, same like in [CSS3](https://www.w3.org/TR/css-color-3/#transparent).

#### Color keywords​

Named colors implementation follows the [CSS3/SVG specification](https://www.w3.org/TR/css-color-3/#svg-color):

- aliceblue (`#f0f8ff`)
- antiquewhite (`#faebd7`)
- aqua (`#00ffff`)
- aquamarine (`#7fffd4`)
- azure (`#f0ffff`)
- beige (`#f5f5dc`)
- bisque (`#ffe4c4`)
- black (`#000000`)
- blanchedalmond (`#ffebcd`)
- blue (`#0000ff`)
- blueviolet (`#8a2be2`)
- brown (`#a52a2a`)
- burlywood (`#deb887`)
- cadetblue (`#5f9ea0`)
- chartreuse (`#7fff00`)
- chocolate (`#d2691e`)
- coral (`#ff7f50`)
- cornflowerblue (`#6495ed`)
- cornsilk (`#fff8dc`)
- crimson (`#dc143c`)
- cyan (`#00ffff`)
- darkblue (`#00008b`)
- darkcyan (`#008b8b`)
- darkgoldenrod (`#b8860b`)
- darkgray (`#a9a9a9`)
- darkgreen (`#006400`)
- darkgrey (`#a9a9a9`)
- darkkhaki (`#bdb76b`)
- darkmagenta (`#8b008b`)
- darkolivegreen (`#556b2f`)
- darkorange (`#ff8c00`)
- darkorchid (`#9932cc`)
- darkred (`#8b0000`)
- darksalmon (`#e9967a`)
- darkseagreen (`#8fbc8f`)
- darkslateblue (`#483d8b`)
- darkslategrey (`#2f4f4f`)
- darkturquoise (`#00ced1`)
- darkviolet (`#9400d3`)
- deeppink (`#ff1493`)
- deepskyblue (`#00bfff`)
- dimgray (`#696969`)
- dimgrey (`#696969`)
- dodgerblue (`#1e90ff`)
- firebrick (`#b22222`)
- floralwhite (`#fffaf0`)
- forestgreen (`#228b22`)
- fuchsia (`#ff00ff`)
- gainsboro (`#dcdcdc`)
- ghostwhite (`#f8f8ff`)
- gold (`#ffd700`)
- goldenrod (`#daa520`)
- gray (`#808080`)
- green (`#008000`)
- greenyellow (`#adff2f`)
- grey (`#808080`)
- honeydew (`#f0fff0`)
- hotpink (`#ff69b4`)
- indianred (`#cd5c5c`)
- indigo (`#4b0082`)
- ivory (`#fffff0`)
- khaki (`#f0e68c`)
- lavender (`#e6e6fa`)
- lavenderblush (`#fff0f5`)
- lawngreen (`#7cfc00`)
- lemonchiffon (`#fffacd`)
- lightblue (`#add8e6`)
- lightcoral (`#f08080`)
- lightcyan (`#e0ffff`)
- lightgoldenrodyellow (`#fafad2`)
- lightgray (`#d3d3d3`)
- lightgreen (`#90ee90`)
- lightgrey (`#d3d3d3`)
- lightpink (`#ffb6c1`)
- lightsalmon (`#ffa07a`)
- lightseagreen (`#20b2aa`)
- lightskyblue (`#87cefa`)
- lightslategrey (`#778899`)
- lightsteelblue (`#b0c4de`)
- lightyellow (`#ffffe0`)
- lime (`#00ff00`)
- limegreen (`#32cd32`)
- linen (`#faf0e6`)
- magenta (`#ff00ff`)
- maroon (`#800000`)
- mediumaquamarine (`#66cdaa`)
- mediumblue (`#0000cd`)
- mediumorchid (`#ba55d3`)
- mediumpurple (`#9370db`)
- mediumseagreen (`#3cb371`)
- mediumslateblue (`#7b68ee`)
- mediumspringgreen (`#00fa9a`)
- mediumturquoise (`#48d1cc`)
- mediumvioletred (`#c71585`)
- midnightblue (`#191970`)
- mintcream (`#f5fffa`)
- mistyrose (`#ffe4e1`)
- moccasin (`#ffe4b5`)
- navajowhite (`#ffdead`)
- navy (`#000080`)
- oldlace (`#fdf5e6`)
- olive (`#808000`)
- olivedrab (`#6b8e23`)
- orange (`#ffa500`)
- orangered (`#ff4500`)
- orchid (`#da70d6`)
- palegoldenrod (`#eee8aa`)
- palegreen (`#98fb98`)
- paleturquoise (`#afeeee`)
- palevioletred (`#db7093`)
- papayawhip (`#ffefd5`)
- peachpuff (`#ffdab9`)
- peru (`#cd853f`)
- pink (`#ffc0cb`)
- plum (`#dda0dd`)
- powderblue (`#b0e0e6`)
- purple (`#800080`)
- rebeccapurple (`#663399`)
- red (`#ff0000`)
- rosybrown (`#bc8f8f`)
- royalblue (`#4169e1`)
- saddlebrown (`#8b4513`)
- salmon (`#fa8072`)
- sandybrown (`#f4a460`)
- seagreen (`#2e8b57`)
- seashell (`#fff5ee`)
- sienna (`#a0522d`)
- silver (`#c0c0c0`)
- skyblue (`#87ceeb`)
- slateblue (`#6a5acd`)
- slategray (`#708090`)
- snow (`#fffafa`)
- springgreen (`#00ff7f`)
- steelblue (`#4682b4`)
- tan (`#d2b48c`)
- teal (`#008080`)
- thistle (`#d8bfd8`)
- tomato (`#ff6347`)
- turquoise (`#40e0d0`)
- violet (`#ee82ee`)
- wheat (`#f5deb3`)
- white (`#ffffff`)
- whitesmoke (`#f5f5f5`)
- yellow (`#ffff00`)
- yellowgreen (`#9acd32`)

Is this page useful?

---

# Communication between native and React Native

> In Integrating with Existing Apps guide and Native UI Components guide we learn how to embed React Native in a native component and vice versa. When we mix native and React Native components, we'll eventually find a need to communicate between these two worlds. Some ways to achieve that have been already mentioned in other guides. This article summarizes available techniques.

In [Integrating with Existing Apps guide](https://reactnative.dev/docs/integration-with-existing-apps) and [Native UI Components guide](https://reactnative.dev/docs/legacy/native-components-android) we learn how to embed React Native in a native component and vice versa. When we mix native and React Native components, we'll eventually find a need to communicate between these two worlds. Some ways to achieve that have been already mentioned in other guides. This article summarizes available techniques.

## Introduction​

React Native is inspired by React, so the basic idea of the information flow is similar. The flow in React is one-directional. We maintain a hierarchy of components, in which each component depends only on its parent and its own internal state. We do this with properties: data is passed from a parent to its children in a top-down manner. If an ancestor component relies on the state of its descendant, one should pass down a callback to be used by the descendant to update the ancestor.

The same concept applies to React Native. As long as we are building our application purely within the framework, we can drive our app with properties and callbacks. But, when we mix React Native and native components, we need some specific, cross-language mechanisms that would allow us to pass information between them.

## Properties​

Properties are the most straightforward way of cross-component communication. So we need a way to pass properties both from native to React Native, and from React Native to native.

### Passing properties from native to React Native​

You can pass properties down to the React Native app by providing a custom implementation of `ReactActivityDelegate` in your main activity. This implementation should override `getLaunchOptions` to return a `Bundle` with the desired properties.

java

```
public class MainActivity extends ReactActivity {  @Override  protected ReactActivityDelegate createReactActivityDelegate() {    return new ReactActivityDelegate(this, getMainComponentName()) {      @Override      protected Bundle getLaunchOptions() {        Bundle initialProperties = new Bundle();        ArrayList<String> imageList = new ArrayList<String>(Arrays.asList(                "https://dummyimage.com/600x400/ffffff/000000.png",                "https://dummyimage.com/600x400/000000/ffffff.png"        ));        initialProperties.putStringArrayList("images", imageList);        return initialProperties;      }    };  }}
```

kotlin

```
class MainActivity : ReactActivity() {    override fun createReactActivityDelegate(): ReactActivityDelegate {        return object : ReactActivityDelegate(this, mainComponentName) {            override fun getLaunchOptions(): Bundle {                val imageList = arrayListOf("https://dummyimage.com/600x400/ffffff/000000.png", "https://dummyimage.com/600x400/000000/ffffff.png")                val initialProperties = Bundle().apply { putStringArrayList("images", imageList) }                return initialProperties            }        }    }}
```

 tsx

```
import React from 'react';import {View, Image} from 'react-native';export default class ImageBrowserApp extends React.Component {  renderImage(imgURI) {    return <Image source={{uri: imgURI}} />;  }  render() {    return <View>{this.props.images.map(this.renderImage)}</View>;  }}
```

`ReactRootView` provides a read-write property `appProperties`. After `appProperties` is set, the React Native app is re-rendered with new properties. The update is only performed when the new updated properties differ from the previous ones.

java

```
Bundle updatedProps = mReactRootView.getAppProperties();ArrayList<String> imageList = new ArrayList<String>(Arrays.asList(        "https://dummyimage.com/600x400/ff0000/000000.png",        "https://dummyimage.com/600x400/ffffff/ff0000.png"));updatedProps.putStringArrayList("images", imageList);mReactRootView.setAppProperties(updatedProps);
```

kotlin

```
var updatedProps: Bundle = reactRootView.getAppProperties()var imageList = arrayListOf("https://dummyimage.com/600x400/ff0000/000000.png", "https://dummyimage.com/600x400/ffffff/ff0000.png")
```

It is fine to update properties anytime. However, updates have to be performed on the main thread. You use the getter on any thread.

There is no way to update only a few properties at a time. We suggest that you build it into your own wrapper instead.

 info

Currently, JS function `componentWillUpdateProps` of the top level RN component will not be called after a prop update. However, you can access the new props in `componentDidMount` function.

### Passing properties from React Native to native​

The problem exposing properties of native components is covered in detail in [this article](https://reactnative.dev/docs/legacy/native-components-android#3-expose-view-property-setters-using-reactprop-or-reactpropgroup-annotation). In short, properties that are to be reflected in JavaScript needs to be exposed as setter method annotated with `@ReactProp`, then use them in React Native as if the component was an ordinary React Native component.

### Limits of properties​

The main drawback of cross-language properties is that they do not support callbacks, which would allow us to handle bottom-up data bindings. Imagine you have a small RN view that you want to be removed from the native parent view as a result of a JS action. There is no way to do that with props, as the information would need to go bottom-up.

Although we have a flavor of cross-language callbacks ([described here](https://reactnative.dev/docs/legacy/native-modules-android#callbacks)), these callbacks are not always the thing we need. The main problem is that they are not intended to be passed as properties. Rather, this mechanism allows us to trigger a native action from JS, and handle the result of that action in JS.

## Other ways of cross-language interaction (events and native modules)​

As stated in the previous chapter, using properties comes with some limitations. Sometimes properties are not enough to drive the logic of our app and we need a solution that gives more flexibility. This chapter covers other communication techniques available in React Native. They can be used for internal communication (between JS and native layers in RN) as well as for external communication (between RN and the 'pure native' part of your app).

React Native enables you to perform cross-language function calls. You can execute custom native code from JS and vice versa. Unfortunately, depending on the side we are working on, we achieve the same goal in different ways. For native - we use events mechanism to schedule an execution of a handler function in JS, while for React Native we directly call methods exported by native modules.

### Calling React Native functions from native (events)​

Events are described in detail in [this article](https://reactnative.dev/docs/legacy/native-components-android#events). Note that using events gives us no guarantees about execution time, as the event is handled on a separate thread.

Events are powerful, because they allow us to change React Native components without needing a reference to them. However, there are some pitfalls that you can fall into while using them:

- As events can be sent from anywhere, they can introduce spaghetti-style dependencies into your project.
- Events share namespace, which means that you may encounter some name collisions. Collisions will not be detected statically, which makes them hard to debug.
- If you use several instances of the same React Native component and you want to distinguish them from the perspective of your event, you'll likely need to introduce identifiers and pass them along with events (you can use the native view's `reactTag` as an identifier).

### Calling native functions from React Native (native modules)​

Native modules are Java/Kotlin classes that are available in JS. Typically one instance of each module is created per JS bridge. They can export arbitrary functions and constants to React Native. They have been covered in detail in [this article](https://reactnative.dev/docs/legacy/native-modules-android).

 warning

All native modules share the same namespace. Watch out for name collisions when creating new ones.

Is this page useful?
