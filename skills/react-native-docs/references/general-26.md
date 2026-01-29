# Using TypeScript and more

# Using TypeScript

> TypeScript is a language which extends JavaScript by adding type definitions. New React Native projects target TypeScript by default, but also support JavaScript and Flow.

[TypeScript](https://www.typescriptlang.org/) is a language which extends JavaScript by adding type definitions. New React Native projects target TypeScript by default, but also support JavaScript and Flow.

## Getting Started with TypeScript​

New projects created by the [React Native CLI](https://reactnative.dev/docs/getting-started-without-a-framework#step-1-creating-a-new-application) or popular templates like [Ignite](https://github.com/infinitered/ignite) will use TypeScript by default.

TypeScript may also be used with [Expo](https://expo.io), which maintains TypeScript templates, or will prompt you to automatically install and configure TypeScript when a `.ts` or `.tsx` file is added to your project.

 shell

```
npx create-expo-app --template
```

## Adding TypeScript to an Existing Project​

1. Add TypeScript, types, and ESLint plugins to your project.

shell

```
npm install -D typescript @react-native/typescript-config @types/jest @types/react @types/react-test-renderer
```

shell

```
yarn add --dev typescript @react-native/typescript-config @types/jest @types/react @types/react-test-renderer
```

 note

This command adds the latest version of every dependency. The versions may need to be changed to match the existing packages used by your project. You can use a tool like [React Native Upgrade Helper](https://react-native-community.github.io/upgrade-helper/) to see the versions shipped by React Native.

1. Add a TypeScript config file. Create a `tsconfig.json` in the root of your project:

 tsconfig.json

```
{  "extends": "@react-native/typescript-config"}
```

1. Rename a JavaScript file to be `*.tsx`

 warning

You should leave the `./index.js` entrypoint file as it is otherwise you may run into an issue when it comes to bundling a production build.

1. Run `tsc` to type-check your new TypeScript files.

shell

```
npx tsc
```

shell

```
yarn tsc
```

## Using JavaScript Instead of TypeScript​

React Native defaults new applications to TypeScript, but JavaScript may still be used. Files with a `.jsx` extension are treated as JavaScript instead of TypeScript, and will not be typechecked. JavaScript modules may still be imported by TypeScript modules, along with the reverse.

## How TypeScript and React Native works​

Out of the box, TypeScript sources are transformed by [Babel](https://reactnative.dev/docs/javascript-environment#javascript-syntax-transformers) during bundling. We recommend that you use the TypeScript compiler only for type checking. This is the default behavior of `tsc` for newly created applications. If you have existing TypeScript code being ported to React Native, there are [one or two caveats](https://babeljs.io/docs/en/next/babel-plugin-transform-typescript) to using Babel instead of TypeScript.

## What does React Native + TypeScript look like​

You can provide an interface for a React Component's [Props](https://reactnative.dev/docs/props) and [State](https://reactnative.dev/docs/state) via `React.Component<Props, State>` which will provide type-checking and editor auto-completing when working with that component in JSX.

 components/Hello.tsx

```
import {useState} from 'react';import {Button, StyleSheet, Text, View} from 'react-native';export type Props = {  name: string;  baseEnthusiasmLevel?: number;};function Hello({name, baseEnthusiasmLevel = 0}: Props) {  const [enthusiasmLevel, setEnthusiasmLevel] = useState(    baseEnthusiasmLevel,  );  const onIncrement = () =>    setEnthusiasmLevel(enthusiasmLevel + 1);  const onDecrement = () =>    setEnthusiasmLevel(      enthusiasmLevel > 0 ? enthusiasmLevel - 1 : 0,    );  const getExclamationMarks = (numChars: number) =>    numChars > 0 ? Array(numChars + 1).join('!') : '';  return (    <View style={styles.container}>      <Text style={styles.greeting}>        Hello {name}        {getExclamationMarks(enthusiasmLevel)}      </Text>      <View>        <Button          title="Increase enthusiasm"          accessibilityLabel="increment"          onPress={onIncrement}          color="blue"        />        <Button          title="Decrease enthusiasm"          accessibilityLabel="decrement"          onPress={onDecrement}          color="red"        />      </View>    </View>  );}const styles = StyleSheet.create({  container: {    flex: 1,    alignItems: 'center',    justifyContent: 'center',  },  greeting: {    fontSize: 20,    fontWeight: 'bold',    margin: 16,  },});export default Hello;
```

You can explore the syntax more in the [TypeScript playground](https://www.typescriptlang.org/play?strictNullChecks=false&jsx=3#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgcilQ3wG4BYAKFEljgG8AhAVxhggDsAaOAZRgCeAGyS8AFkiQweAFSQAPaXABqwJAHcAvnGy4CRdDAC0HFDGAA3JGSpUFteILBI4ABRxgAznAC8DKnBwpiBIAFxwnjBQwBwA5hSUgQBGKJ5IAKIcMGLMnsCpIAAySFZCAPzhHMwgSUhQCZq2lGickXAAEkhCQhDhyIYAdABiAMIAPO4QXgB8vnAAFPRBKCE8KWmZ2bn5nkUlXXMADHCaAJS+s-QBcC0cbQDaSFk5eQXFpTxpMJsvO3ulAF05v0MANcqIYGYkPN1hlnts3vshKcEtdbm1OABJDhoIghLJzebnHyzL4-BG7d5deZPLavSlIuAAajgAEYUWjWvBOAARJC4pD4+B+IkXCJScn0-7U2m-RGlOCzY5lOCyinSoRwIxsuDhQ4cyicu7wWIS+RoIQrMzATgAWRQUAA1t4RVUQCMxA7PJVqrUoMTZm6PV7FXBlXAAIJQKAoATzIOeqDeFnsgYAKwgMXm+AAhPhzuF8DZDYk4EQYMwoBwFtdAmNVBoIoIRD56JFhEhPANbpCYnVNNNa4E4GM5Iomx3W+2RF3YkQpDFYgOh8OOl0evR8ARGqXV4F6MEkDu98P6KbvubLSBrXaHc6afCpVTkce92MAPRjmCD3fD+tqdQfxPOsWDYTgVz3cwYBbAAibEBVSFw1SlGCINXdA0E7PIkmAIRgEEQoUFqIQfBgmIBSFVDfxPTh3Cw1ssRxPFaVfYCbggHooFIpIhGYJAqLY98gOAsZQPYDg0OHKDYL5BC0lVR8-gEti4AwrDgBwvCCKIrpSIAE35ZismUtjaKITxPAYjhZKMmBWOAlpONIog9JMvchIgj8G0AocvIA4SDU0VFmi5CcZzmfgO3ESQYG7AwYGhK5Sx7FA+ygcIktXTARHkcJWS4IcUDw2IOExBKQG9OAYMwrI6hggrfzTXJzEwAQRk4BKsnCaraTq65NAawI5xixcMqHTAOt4YAAC8wjgAAmQ5BuHCasgAdSQYBYjEGBCySDi9PwZbAmvKBYhiPKADZloGqgzmC+xoHgAzMBQZghHgTpuggBIgA).

## Where to Find Useful Advice​

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [React's documentation on TypeScript](https://react.dev/learn/typescript)
- [React + TypeScript Cheatsheets](https://github.com/typescript-cheatsheets/react-typescript-cheatsheet#reacttypescript-cheatsheets) has a good overview on how to use React with TypeScript

## Using Custom Path Aliases with TypeScript​

To use custom path aliases with TypeScript, you need to set the path aliases to work from both Babel and TypeScript. Here's how:

1. Edit your `tsconfig.json` to have your [custom path mappings](https://www.typescriptlang.org/docs/handbook/module-resolution.html#path-mapping). Set anything in the root of `src` to be available with no preceding path reference, and allow any test file to be accessed by using `tests/File.tsx`:

 diff

```
{-  "extends": "@react-native/typescript-config"+  "extends": "@react-native/typescript-config",+  "compilerOptions": {+    "baseUrl": ".",+    "paths": {+      "*": ["src/*"],+      "tests": ["tests/*"],+      "@components/*": ["src/components/*"],+    },+  }}
```

1. Add [babel-plugin-module-resolver](https://github.com/tleunen/babel-plugin-module-resolver) as a development package to your project:

shell

```
npm install --save-dev babel-plugin-module-resolver
```

shell

```
yarn add --dev babel-plugin-module-resolver
```

1. Finally, configure your `babel.config.js` (note that the syntax for your `babel.config.js` is different from your `tsconfig.json`):

 diff

```
{   presets: ['module:metro-react-native-babel-preset'],+  plugins: [+    [+       'module-resolver',+       {+         root: ['./src'],+         extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],+         alias: {+           tests: ['./tests/'],+           "@components": "./src/components",+         }+       }+    ]+  ]}
```

Is this page useful?

---

# Upgrading to new versions

> Upgrading to new versions of React Native will give you access to more APIs, views, developer tools and other goodies. Upgrading requires a small amount of effort, but we try to make it straightforward for you.

Upgrading to new versions of React Native will give you access to more APIs, views, developer tools and other goodies. Upgrading requires a small amount of effort, but we try to make it straightforward for you.

## Expo projects​

Upgrading your Expo project to a new version of React Native requires updating the `react-native`, `react`, and `expo` package versions in your `package.json` file. Expo recommends upgrading SDK versions incrementally, one at a time. Doing so will help you pinpoint breakages and issues that arise during the upgrade process. See the [Upgrading Expo SDK Walkthrough](https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/) for up-to-date information about upgrading your project.

## React Native projects​

Because typical React Native projects are essentially made up of an Android project, an iOS project, and a JavaScript project, upgrading can be rather tricky. The [Upgrade Helper](https://react-native-community.github.io/upgrade-helper/) is a web tool to help you out when upgrading your apps by providing the full set of changes happening between any two versions. It also shows comments on specific files to help understanding why that change is needed.

### 1. Select the versions​

You first need to select from and to which version you wish to upgrade, by default the latest major versions are selected. After selecting you can click the button "Show me how to upgrade".

💡 Major updates will show a "useful content" section on the top with links to help you out when upgrading.

### 2. Upgrade dependencies​

The first file that is shown is the `package.json`, it's good to update the dependencies that are showing in there. For example, if `react-native` and `react` appears as changes then you can install it in your project by running following commands:

shell

```
# {{VERSION}} and {{REACT_VERSION}} are the release versions showing in the diffnpm install react-native@{{VERSION}}npm install react@{{REACT_VERSION}}
```

shell

```
# {{VERSION}} and {{REACT_VERSION}} are the release versions showing in the diffyarn add react-native@{{VERSION}}yarn add react@{{REACT_VERSION}}
```

### 3. Upgrade your project files​

The new release may contain updates to other files that are generated when you run `npx react-native init`, those files are listed after the `package.json` in the [Upgrade Helper](https://react-native-community.github.io/upgrade-helper/) page. If there aren't other changes then you only need to rebuild the project to continue developing. In case there are changes you need to manually apply them into your project.

### Troubleshooting​

#### I have done all the changes but my app is still using an old version​

These sort of errors are usually related to caching, it's recommended to install [react-native-clean-project](https://github.com/pmadruga/react-native-clean-project) to clear all your project's cache and then you can run it again.

Is this page useful?

---

# useColorScheme

> The useColorScheme React hook provides and subscribes to color scheme updates from the Appearance module. The return value indicates the current user preferred color scheme. The value may be updated later, either through direct user action (e.g. theme selection in device settings) or on a schedule (e.g. light and dark themes that follow the day/night cycle).

tsx

```
import {useColorScheme} from 'react-native';
```

The `useColorScheme` React hook provides and subscribes to color scheme updates from the [Appearance](https://reactnative.dev/docs/appearance) module. The return value indicates the current user preferred color scheme. The value may be updated later, either through direct user action (e.g. theme selection in device settings) or on a schedule (e.g. light and dark themes that follow the day/night cycle).

### Supported color schemes​

- `"light"`: The user prefers a light color theme.
- `"dark"`: The user prefers a dark color theme.
- `null`: The user has not indicated a preferred color theme.

---

## Example​

You can find a complete example that demonstrates the use of this hook alongside a React context to add support for light and dark themes to your application in [AppearanceExample.js](https://github.com/facebook/react-native/blob/main/packages/rn-tester/js/examples/Appearance/AppearanceExample.js).

Is this page useful?

---

# useWindowDimensions

> useWindowDimensions automatically updates all of its values when screen size or font scale changes. You can get your application window's width and height like so:

tsx

```
import {useWindowDimensions} from 'react-native';
```

`useWindowDimensions` automatically updates all of its values when screen size or font scale changes. You can get your application window's width and height like so:

 tsx

```
const {height, width} = useWindowDimensions();
```

## Example​

## Properties​

### fontScale​

 tsx

```
useWindowDimensions().fontScale;
```

The scale of the font currently used. Some operating systems allow users to scale their font sizes larger or smaller for reading comfort. This property will let you know what is in effect.

---

### height​

 tsx

```
useWindowDimensions().height;
```

The height in pixels of the window or screen your app occupies.

---

### scale​

 tsx

```
useWindowDimensions().scale;
```

The pixel ratio of the device your app is running on. The values can be:

- `1` which indicates that one point equals one pixel (usually PPI/DPI of 96, 76 on some platforms).
- `2` or `3` which indicates a Retina or high DPI display.

---

### width​

 tsx

```
useWindowDimensions().width;
```

The width in pixels of the window or screen your app occupies.

Is this page useful?

---

# Using List Views

> React Native provides a suite of components for presenting lists of data. Generally, you'll want to use either FlatList or SectionList.

React Native provides a suite of components for presenting lists of data. Generally, you'll want to use either [FlatList](https://reactnative.dev/docs/flatlist) or [SectionList](https://reactnative.dev/docs/sectionlist).

The `FlatList` component displays a scrolling list of changing, but similarly structured, data. `FlatList` works well for long lists of data, where the number of items might change over time. Unlike the more generic [ScrollView](https://reactnative.dev/docs/using-a-scrollview), the `FlatList` only renders elements that are currently showing on the screen, not all the elements at once.

The `FlatList` component requires two props: `data` and `renderItem`. `data` is the source of information for the list. `renderItem` takes one item from the source and returns a formatted component to render.

This example creates a basic `FlatList` of hardcoded data. Each item in the `data` props is rendered as a `Text` component. The `FlatListBasics` component then renders the `FlatList` and all `Text` components.

If you want to render a set of data broken into logical sections, maybe with section headers, similar to `UITableView` on iOS, then a [SectionList](https://reactnative.dev/docs/sectionlist) is the way to go.

One of the most common uses for a list view is displaying data that you fetch from a server. To do that, you will need to [learn about networking in React Native](https://reactnative.dev/docs/network).

Is this page useful?

---

# Using a ScrollView

> The ScrollView is a generic scrolling container that can contain multiple components and views. The scrollable items can be heterogeneous, and you can scroll both vertically and horizontally (by setting the horizontal property).

The [ScrollView](https://reactnative.dev/docs/scrollview) is a generic scrolling container that can contain multiple components and views. The scrollable items can be heterogeneous, and you can scroll both vertically and horizontally (by setting the `horizontal` property).

This example creates a vertical `ScrollView` with both images and text mixed together.

ScrollViews can be configured to allow paging through views using swiping gestures by using the `pagingEnabled` props. Swiping horizontally between views can also be implemented on Android using the [ViewPager](https://github.com/react-native-community/react-native-viewpager) component.

On iOS a ScrollView with a single item can be used to allow the user to zoom content. Set up the `maximumZoomScale` and `minimumZoomScale` props and your user will be able to use pinch and expand gestures to zoom in and out.

The ScrollView works best to present a small number of things of a limited size. All the elements and views of a `ScrollView` are rendered, even if they are not currently shown on the screen. If you have a long list of items which cannot fit on the screen, you should use a `FlatList` instead. So let's [learn about list views](https://reactnative.dev/docs/using-a-listview) next.

Is this page useful?

---

# Vibration

> Vibrates the device.

Vibrates the device.

## Example​

  info

Android apps should request the `android.permission.VIBRATE` permission by adding `<uses-permission android:name="android.permission.VIBRATE"/>` to `AndroidManifest.xml`.

 note

The Vibration API is implemented as a `AudioServicesPlaySystemSound(kSystemSoundID_Vibrate)` call on iOS.

---

# Reference

## Methods​

### cancel()​

 tsx

```
static cancel();
```

Call this to stop vibrating after having invoked `vibrate()` with repetition enabled.

---

### vibrate()​

 tsx

```
static vibrate(  pattern?: number | number[],  repeat?: boolean);
```

Triggers a vibration with a fixed duration.

**On Android,** the vibration duration defaults to 400 milliseconds, and an arbitrary vibration duration can be specified by passing a number as the value for the `pattern` argument. **On iOS,** the vibration duration is fixed at roughly 400 milliseconds.

The `vibrate()` method can take a `pattern` argument with an array of numbers that represent time in milliseconds. You may set `repeat` to true to run through the vibration pattern in a loop until `cancel()` is called.

**On Android,** the odd indices of the `pattern` array represent the vibration duration, while the even ones represent the separation time. **On iOS,** the numbers in the `pattern` array represent the separation time, as the vibration duration is fixed.

**Parameters:**

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| pattern | numberAndroidarray of numbers | 400 | Vibration duration in milliseconds.Vibration pattern as an array of numbers in milliseconds. |
| repeat | boolean | false | Repeat vibration pattern untilcancel(). |

Is this page useful?

---

# View Style Props

> Example

### Example​

# Reference

## Props​

### backfaceVisibility​

| Type |
| --- |
| enum('visible','hidden') |

---

### backgroundColor​

| Type |
| --- |
| color |

---

### borderBottomColor​

| Type |
| --- |
| color |

---

### borderBlockColor​

| Type |
| --- |
| color |

---

### borderBlockEndColor​

| Type |
| --- |
| color |

---

### borderBlockStartColor​

| Type |
| --- |
| color |

---

### borderBottomEndRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderBottomLeftRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderBottomRightRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderBottomStartRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderStartEndRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderStartStartRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderEndEndRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderEndStartRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderBottomWidth​

| Type |
| --- |
| number |

---

### borderColor​

| Type |
| --- |
| color |

---

### borderCurveiOS​

On iOS 13+, it is possible to change the corner curve of borders.

| Type |
| --- |
| enum('circular','continuous') |

---

### borderEndColor​

| Type |
| --- |
| color |

---

### borderLeftColor​

| Type |
| --- |
| color |

---

### borderLeftWidth​

| Type |
| --- |
| number |

---

### borderRadius​

If the rounded border is not visible, try applying `overflow: 'hidden'` as well.

| Type |
| --- |
| number, string (percentage value) |

---

### borderRightColor​

| Type |
| --- |
| color |

---

### borderRightWidth​

| Type |
| --- |
| number |

---

### borderStartColor​

| Type |
| --- |
| color |

---

### borderStyle​

| Type |
| --- |
| enum('solid','dotted','dashed') |

---

### borderTopColor​

| Type |
| --- |
| color |

---

### borderTopEndRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderTopLeftRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderTopRightRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderTopStartRadius​

| Type |
| --- |
| number, string (percentage value) |

---

### borderTopWidth​

| Type |
| --- |
| number, string (percentage value) |

---

### borderWidth​

| Type |
| --- |
| number |

### boxShadow​

 note

`boxShadow` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page). Outset shadows are only supported on **Android 9+**. Inset shadows are only supported on **Android 10+**.

Adds a shadow effect to an element, with the ability to control the position, color, size, and blurriness of the shadow. This shadow either appears around the outside or inside of the border box of the element, depending on whether or not the shadow is *inset*. This is a spec-compliant implementation of the [web style prop of the same name](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow). Read more about all the arguments available in the [BoxShadowValue](https://reactnative.dev/docs/boxshadowvalue) documentation.

These shadows can be composed together so that a single `boxShadow` can be comprised of multiple different shadows.

`boxShadow` takes either a string which mimics the [web syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow#syntax) or an array of [BoxShadowValue](https://reactnative.dev/docs/boxshadowvalue) objects.

| Type |
| --- |
| array of BoxShadowValue objects | string |

### cursoriOS​

On iOS 17+, Setting to `pointer` allows hover effects when a pointer (such as a trackpad or stylus on iOS, or the users' gaze on visionOS) is over the view.

| Type |
| --- |
| enum('auto','pointer') |

---

### elevationAndroid​

Sets the elevation of a view, using Android's underlying [elevation API](https://developer.android.com/training/material/shadows-clipping.html#Elevation). This adds a drop shadow to the item and affects z-order for overlapping views. Only supported on Android 5.0+, has no effect on earlier versions.

| Type |
| --- |
| number |

---

### filter​

 note

`filter` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Adds a graphical filter to the `View`. This filter is comprised of any number of *filter functions*, which each represent some atomic change to the graphical composition of the `View`. The complete list of valid filter functions is defined below. `filter` will apply to descendants of the `View` as well as the `View` itself. `filter` implies `overflow: hidden`, so descendants will be clipped to fit the bounds of the `View`.

The following filter functions work across all platforms:

- `brightness`: Changes the brightness of the `View`. Takes a non-negative number or percentage.
- `opacity`: Changes the opacity, or alpha, of the `View`. Takes a non-negative number or percentage.

 note

Due to issues with performance and spec compliance, these are the only two filter functions available on iOS. There are plans to explore some potential workarounds using SwiftUI instead of UIKit for this implementation.

 Android

The following filter functions work on Android only:

- `blur`: Blurs the `View` with a [Gaussian blur](https://en.wikipedia.org/wiki/Gaussian_blur), where the specified length represents the radius used in the blurring algorithm. Any non-negative DIP value is valid (no percents). The larger the value, the blurrier the result.
- `contrast`: Changes the contrast of the `View`. Takes a non-negative number or percentage.
- `dropShadow`: Adds a shadow around the alpha mask of the `View` (only non-zero alpha pixels in the `View` will cast a shadow). Takes an optional color representing the shadow color, and 2 or 3 lengths. If 2 lengths are specified they are interpreted as `offsetX` and `offsetY` which will translate the shadow in the X and Y dimensions respectfully. If a 3rd length is given it is interpreted as the standard deviation of the Gaussian blur used on the shadow - so a larger value will blur the shadow more. Read more about the arguments in [DropShadowValue](https://reactnative.dev/docs/dropshadowvalue).
- `grayscale`: Converts the `View` to [grayscale](https://en.wikipedia.org/wiki/Grayscale) by the specified amount. Takes a non-negative number or percentage, where `1` or `100%` represents complete grayscale.
- `hueRotate`: Changes the [hue](https://en.wikipedia.org/wiki/Hue) of the View. The argument of this function defines the angle of a color wheel around which the hue will be rotated, so e.g., `360deg` would have no effect. This angle can have either `deg` or `rad` units.
- `invert`: Inverts the colors in the `View`. Takes a non-negative number or percentage, where `1` or `100%` represents complete inversion.
- `sepia`: Converts the `View` to [sepia](https://en.wikipedia.org/wiki/Sepia_(color)). Takes a non-negative number or percentage, where `1` or `100%` represents complete sepia.
- `saturate`: Changes the [saturation](https://en.wikipedia.org/wiki/Colorfulness) of the `View`. Takes a non-negative number or percentage.

 note

`blur` and `dropShadow` are only supported on **Android 12+**

`filter` takes either an array of objects comprising of the above filter functions or a string which mimics the [web syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/filter#syntax).

| Type |
| --- |
| array of objects:{brightness: number|string},{opacity: number|string},{blur: number|string},{contrast: number|string},{dropShadow: DropShadowValue|string},{grayscale: number|string},{hueRotate: number|string},{invert: number|string},{sepia: number|string},{saturate: number|string}or string |

---

### mixBlendMode​

 note

`mixBlendMode` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Controls how the `View` blends its colors with the other elements in its **stacking context**. Check out the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode) for a full overview of each blending function.

For more granular control over what should be blending together see [isolation](https://reactnative.dev/docs/layout-props#isolation).

##### mixBlendMode Values​

- `normal`: The element is drawn on top of its background without blending.
- `multiply`: The source color is multiplied by the destination color and replaces the destination.
- `screen`: Multiplies the complements of the backdrop and source color values, then complements the result.
- `overlay`: Multiplies or screens the colors, depending on the backdrop color value.
- `darken`: Selects the darker of the backdrop and source colors.
- `lighten`: Selects the lighter of the backdrop and source colors.
- `color-dodge`: Brightens the backdrop color to reflect the source color. Painting with black produces no changes.
- `color-burn`: Darkens the backdrop color to reflect the source color. Painting with white produces no change.
- `hard-light`: Multiplies or screens the colors, depending on the source color value. The effect is similar to shining a harsh spotlight on the backdrop.
- `soft-light`: Darkens or lightens the colors, depending on the source color value. The effect is similar to shining a diffused spotlight on the backdrop.
- `difference`: Subtracts the darker of the two constituent colors from the lighter color.
- `exclusion`: Produces an effect similar to that of the Difference mode but lower in contrast.
- `hue`: Creates a color with the hue of the source color and the saturation and luminosity of the backdrop color.
- `saturation`: Creates a color with the saturation of the source color and the hue and luminosity of the backdrop color.
- `color`: Creates a color with the hue and saturation of the source color and the luminosity of the backdrop color. This preserves the gray levels of the backdrop and is useful for coloring monochrome images or tinting color images.
- `luminosity`: Creates a color with the luminosity of the source color and the hue and saturation of the backdrop color. This produces an inverse effect to that of the Color mode.

| Type |
| --- |
| enum('normal','multiply','screen','overlay','darken','lighten','color-dodge','color-burn','hard-light','soft-light','difference','exclusion','hue','saturation','color','luminosity') |

---

### opacity​

| Type |
| --- |
| number |

---

### outlineColor​

 note

`outlineColor` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Sets the color of an element's outline. See [web documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/outline-color) for more details.

| Type |
| --- |
| color |

---

### outlineOffset​

 note

`outlineOffset` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Sets the amount of space between an outline and the bounds of an element. Does not affect layout. See [web documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/outline-offset) for more details.

| Type |
| --- |
| number |

---

### outlineStyle​

 note

`outlineStyle` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Sets the style of an element's outline. See [web documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/outline-style) for more details.

| Type |
| --- |
| enum('solid','dotted','dashed') |

---

### outlineWidth​

 note

`outlineWidth` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

The width of an outline which is drawn around an element, outside the border. Does not affect layout. See [web documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/outline-width) for more details.

| Type |
| --- |
| number |

---

### pointerEvents​

Controls whether the `View` can be the target of touch events.

- `'auto'`: The View can be the target of touch events.
- `'none'`: The View is never the target of touch events.
- `'box-none'`: The View is never the target of touch events but its subviews can be.
- `'box-only'`: The view can be the target of touch events but its subviews cannot be.

| Type |
| --- |
| enum('auto','box-none','box-only','none') |

Is this page useful?
