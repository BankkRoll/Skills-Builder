# TouchableWithoutFeedback and more

# TouchableWithoutFeedback

> If you're looking for a more extensive and future-proof way to handle touch-based input, check out the Pressable API.

tip

If you're looking for a more extensive and future-proof way to handle touch-based input, check out the [Pressable](https://reactnative.dev/docs/pressable) API.

Do not use unless you have a very good reason. All elements that respond to press should have a visual feedback when touched.

`TouchableWithoutFeedback` supports only one child. If you wish to have several child components, wrap them in a View. Importantly, `TouchableWithoutFeedback` works by cloning its child and applying responder props to it. It is therefore required that any intermediary components pass through those props to the underlying React Native component.

## Usage Pattern​

 tsx

```
function MyComponent(props: MyComponentProps) {  return (    <View {...props} style={{flex: 1, backgroundColor: '#fff'}}>      <Text>My Component</Text>    </View>  );}<TouchableWithoutFeedback onPress={() => alert('Pressed!')}>  <MyComponent /></TouchableWithoutFeedback>;
```

## Example​

---

# Reference

## Props​

### accessibilityIgnoresInvertColorsiOS​

A value indicating this view should or should not be inverted when color inversion is turned on. A value of `true` will tell the view to not be inverted even if color inversion is turned on.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibilityignoresinvertcolors) for more information.

| Type |
| --- |
| Boolean |

---

### accessible​

When `true`, indicates that the view is an accessibility element. By default, all the touchable elements are accessible.

| Type |
| --- |
| bool |

---

### accessibilityLabel​

Overrides the text that's read by the screen reader when the user interacts with the element. By default, the label is constructed by traversing all the children and accumulating all the `Text` nodes separated by space.

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

### accessibilityHint​

An accessibility hint helps users understand what will happen when they perform an action on the accessibility element when that result is not clear from the accessibility label.

| Type |
| --- |
| string |

---

### accessibilityRole​

`accessibilityRole` communicates the purpose of a component to the user of an assistive technology.

`accessibilityRole` can be one of the following:

- `'none'` - Used when the element has no role.
- `'button'` - Used when the element should be treated as a button.
- `'link'` - Used when the element should be treated as a link.
- `'search'` - Used when the text field element should also be treated as a search field.
- `'image'` - Used when the element should be treated as an image. Can be combined with button or link, for example.
- `'keyboardkey'` - Used when the element acts as a keyboard key.
- `'text'` - Used when the element should be treated as static text that cannot change.
- `'adjustable'` - Used when an element can be "adjusted" (e.g. a slider).
- `'imagebutton'` - Used when the element should be treated as a button and is also an image.
- `'header'` - Used when an element acts as a header for a content section (e.g. the title of a navigation bar).
- `'summary'` - Used when an element can be used to provide a quick summary of current conditions in the app when the app first launches.
- `'alert'` - Used when an element contains important text to be presented to the user.
- `'checkbox'` - Used when an element represents a checkbox which can be checked, unchecked, or have mixed checked state.
- `'combobox'` - Used when an element represents a combo box, which allows the user to select among several choices.
- `'menu'` - Used when the component is a menu of choices.
- `'menubar'` - Used when a component is a container of multiple menus.
- `'menuitem'` - Used to represent an item within a menu.
- `'progressbar'` - Used to represent a component which indicates progress of a task.
- `'radio'` - Used to represent a radio button.
- `'radiogroup'` - Used to represent a group of radio buttons.
- `'scrollbar'` - Used to represent a scroll bar.
- `'spinbutton'` - Used to represent a button which opens a list of choices.
- `'switch'` - Used to represent a switch which can be turned on and off.
- `'tab'` - Used to represent a tab.
- `'tablist'` - Used to represent a list of tabs.
- `'timer'` - Used to represent a timer.
- `'toolbar'` - Used to represent a tool bar (a container of action buttons or components).

| Type |
| --- |
| string |

---

### accessibilityState​

Describes the current state of a component to the user of an assistive technology.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibilitystate-ios-android) for more information.

| Type |
| --- |
| object:{disabled: bool, selected: bool, checked: bool or 'mixed', busy: bool, expanded: bool} |

---

### accessibilityActions​

Accessibility actions allow an assistive technology to programmatically invoke the actions of a component. The `accessibilityActions` property should contain a list of action objects. Each action object should contain the field name and label.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibility-actions) for more information.

| Type |
| --- |
| array |

---

### aria-busy​

Indicates an element is being modified and that assistive technologies may want to wait until the changes are complete before informing the user about the update.

| Type | Default |
| --- | --- |
| boolean | false |

---

### aria-checked​

Indicates the state of a checkable element. This field can either take a boolean or the "mixed" string to represent mixed checkboxes.

| Type | Default |
| --- | --- |
| boolean, 'mixed' | false |

---

### aria-disabled​

Indicates that the element is perceivable but disabled, so it is not editable or otherwise operable.

| Type | Default |
| --- | --- |
| boolean | false |

---

### aria-expanded​

Indicates whether an expandable element is currently expanded or collapsed.

| Type | Default |
| --- | --- |
| boolean | false |

---

### aria-hidden​

Indicates whether the element is hidden from assistive technologies.

For example, in a window that contains sibling views `A` and `B`, setting `aria-hidden` to `true` on view `B` causes VoiceOver to ignore the `B` element and its children.

| Type | Default |
| --- | --- |
| boolean | false |

---

### aria-label​

Defines a string value that labels an interactive element.

| Type |
| --- |
| string |

---

### aria-liveAndroid​

Indicates that an element will be updated, and describes the types of updates the user agents, assistive technologies, and user can expect from the live region.

- **off** Accessibility services should not announce changes to this view.
- **polite** Accessibility services should announce changes to this view.
- **assertive** Accessibility services should interrupt ongoing speech to immediately announce changes to this view.

| Type | Default |
| --- | --- |
| enum('assertive','off','polite') | 'off' |

---

### aria-modaliOS​

Boolean value indicating whether VoiceOver should ignore the elements within views that are siblings of the receiver. Has precedence over the [accessibilityViewIsModal](#accessibilityviewismodal-ios) prop.

| Type | Default |
| --- | --- |
| boolean | false |

---

### aria-selected​

Indicates whether a selectable element is currently selected or not.

| Type |
| --- |
| boolean |

### onAccessibilityAction​

Invoked when the user performs the accessibility actions. The only argument to this function is an event containing the name of the action to perform.

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibility-actions) for more information.

| Type |
| --- |
| function |

---

### accessibilityValue​

Represents the current value of a component. It can be a textual description of a component's value, or for range-based components, such as sliders and progress bars, it contains range information (minimum, current, and maximum).

See the [Accessibility guide](https://reactnative.dev/docs/accessibility#accessibilityvalue-ios-android) for more information.

| Type |
| --- |
| object:{min: number, max: number, now: number, text: string} |

---

### aria-valuemax​

Represents the maximum value for range-based components, such as sliders and progress bars. Has precedence over the `max` value in the `accessibilityValue` prop.

| Type |
| --- |
| number |

---

### aria-valuemin​

Represents the minimum value for range-based components, such as sliders and progress bars. Has precedence over the `min` value in the `accessibilityValue` prop.

| Type |
| --- |
| number |

---

### aria-valuenow​

Represents the current value for range-based components, such as sliders and progress bars. Has precedence over the `now` value in the `accessibilityValue` prop.

| Type |
| --- |
| number |

---

### aria-valuetext​

Represents the textual description of the component. Has precedence over the `text` value in the `accessibilityValue` prop.

| Type |
| --- |
| string |

---

### delayLongPress​

Duration (in milliseconds) from `onPressIn` before `onLongPress` is called.

| Type |
| --- |
| number |

---

### delayPressIn​

Duration (in milliseconds), from the start of the touch, before `onPressIn` is called.

| Type |
| --- |
| number |

---

### delayPressOut​

Duration (in milliseconds), from the release of the touch, before `onPressOut` is called.

| Type |
| --- |
| number |

---

### disabled​

If true, disable all interactions for this component.

| Type |
| --- |
| bool |

---

### hitSlop​

This defines how far your touch can start away from the button. This is added to `pressRetentionOffset` when moving off of the button.

 note

The touch area never extends past the parent view bounds and the Z-index of sibling views always takes precedence if a touch hits two overlapping views.

| Type |
| --- |
| Rector number |

### id​

Used to locate this view from native code. Has precedence over `nativeID` prop.

| Type |
| --- |
| string |

---

### onBlur​

Invoked when the item loses focus.

| Type |
| --- |
| ({nativeEvent:TargetEvent}) => void |

---

### onFocus​

Invoked when the item receives focus.

| Type |
| --- |
| ({nativeEvent:TargetEvent}) => void |

---

### onLayout​

Invoked on mount and on layout changes.

| Type |
| --- |
| ({nativeEvent:LayoutEvent}) => void |

---

### onLongPress​

Called if the time after `onPressIn` lasts longer than 370 milliseconds. This time period can be customized with [delayLongPress](#delaylongpress).

| Type |
| --- |
| function |

---

### onPress​

Called when the touch is released, but not if cancelled (e.g. by a scroll that steals the responder lock). The first function argument is an event in form of [PressEvent](https://reactnative.dev/docs/pressevent).

| Type |
| --- |
| function |

---

### onPressIn​

Called as soon as the touchable element is pressed and invoked even before onPress. This can be useful when making network requests. The first function argument is an event in form of [PressEvent](https://reactnative.dev/docs/pressevent).

| Type |
| --- |
| function |

---

### onPressOut​

Called as soon as the touch is released even before onPress. The first function argument is an event in form of [PressEvent](https://reactnative.dev/docs/pressevent).

| Type |
| --- |
| function |

---

### pressRetentionOffset​

When the scroll view is disabled, this defines how far your touch may move off of the button, before deactivating the button. Once deactivated, try moving it back and you'll see that the button is once again reactivated! Move it back and forth several times while the scroll view is disabled. Ensure you pass in a constant to reduce memory allocations.

| Type |
| --- |
| Rector number |

---

### nativeID​

| Type |
| --- |
| string |

---

### testID​

Used to locate this view in end-to-end tests.

| Type |
| --- |
| string |

---

### touchSoundDisabledAndroid​

If true, doesn't play a system sound on touch.

| Type |
| --- |
| Boolean |

Is this page useful?

---

# Transforms

> Transforms are style properties that will help you modify the appearance and position of your components using 2D or 3D transformations. However, once you apply transforms, the layouts remain the same around the transformed component hence it might overlap with the nearby components. You can apply margin to the transformed component, the nearby components or padding to the container to prevent such overlaps.

Transforms are style properties that will help you modify the appearance and position of your components using 2D or 3D transformations. However, once you apply transforms, the layouts remain the same around the transformed component hence it might overlap with the nearby components. You can apply margin to the transformed component, the nearby components or padding to the container to prevent such overlaps.

## Example​

---

# Reference

## Transform​

`transform` accepts an array of transformation objects or space-separated string values. Each object specifies the property that will be transformed as the key, and the value to use in the transformation. Objects should not be combined. Use a single key/value pair per object.

The rotate transformations require a string so that the transform may be expressed in degrees (deg) or radians (rad). For example:

 js

```
{  transform: [{rotateX: '45deg'}, {rotateZ: '0.785398rad'}],}
```

The same could also be achieved using a space-separated string:

 js

```
{  transform: 'rotateX(45deg) rotateZ(0.785398rad)',}
```

The skew transformations require a string so that the transform may be expressed in degrees (deg). For example:

 js

```
{  transform: [{skewX: '45deg'}],}
```

### Matrix Transform​

The `matrix` transform accepts a 4x4 transformation matrix as an array of 16 numbers. This allows you to apply complex transformations that combine translation, rotation, scaling, and skewing in a single operation.

The matrix is specified in column-major order:

 js

```
{  transform: [    {      matrix: [        scaleX,        skewY,        0,        0,        skewX,        scaleY,        0,        0,        0,        0,        1,        0,        translateX,        translateY,        0,        1,      ],    },  ];}
```

For example, to apply a combination of scale and skew:

 js

```
{  transform: [    {      matrix: [        1, 0.5, 0, 0, 0.5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,      ],    },  ];}
```

 note

Matrix transforms are useful when you need to apply pre-calculated transformation matrices, such as those from animation libraries or when building UI editor applications. For basic transformations, it's recommended to use the individual transform properties (scale, rotate, translate, etc.) as they are more readable.

| Type | Required |
| --- | --- |
| array of objects:{matrix: number[]},{perspective: number},{rotate: string},{rotateX: string},{rotateY: string},{rotateZ: string},{scale: number},{scaleX: number},{scaleY: number},{translateX: number},{translateY: number},{skewX: string},{skewY: string}or string | No |

---

### 🗑️decomposedMatrix,rotation,scaleX,scaleY,transformMatrix,translateX,translateY​

 Deprecated

Use the [transform](https://reactnative.dev/docs/transforms#transform) prop instead.

## Transform Origin​

The `transformOrigin` property sets the origin for a view's transformations. The transform origin is the point around which a transformation is applied. By default, the origin of a transform is `center`.

# Example

### Values​

Transform origin supports `px`, `percentage` and keywords `top`, `left`, `right`, `bottom`, `center` values.

The `transformOrigin` property may be specified using one, two, or three values, where each value represents an offset.

#### One-value syntax:​

- The value must be a `px`, a `percentage`, or one of the keywords `left`, `center`, `right`, `top`, and `bottom`.

 js

```
{  transformOrigin: '20px',  transformOrigin: 'bottom',}
```

#### Two-value syntax:​

- First value (x-offset) must be a `px`, a `percentage`, or one of the keywords `left`, `center`, and `right`.
- The second value (y-offset) must be a `px`, a `percentage`, or one of the keywords `top`, `center`, and `bottom`.

 js

```
{  transformOrigin: '10px 2px',  transformOrigin: 'left top',  transformOrigin: 'top right',}
```

#### Three-value syntax:​

- The first two values are the same as for the two-value syntax.
- The third value (z-offset) must be a `px`. It always represents the Z offset.

 js

```
{  transformOrigin: '2px 30% 10px',  transformOrigin: 'right bottom 20px',}
```

#### Array syntax​

`transformOrigin` also supports an array syntax. It makes it convenient to use it with Animated APIs. It also avoids string parsing, so should be more efficient.

 js

```
{  // Using numeric values  transformOrigin: [10, 30, 40],  // Mixing numeric and percentage values  transformOrigin: [10, '20%', 0],}
```

You may refer to MDN's guide on [Transform origin](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-origin) for additional information.

Is this page useful?

---

# Troubleshooting

> These are some common issues you may run into while setting up React Native. If you encounter something that is not listed here, try searching for the issue in GitHub.

These are some common issues you may run into while setting up React Native. If you encounter something that is not listed here, try [searching for the issue in GitHub](https://github.com/facebook/react-native/issues/).

### Port already in use​

The [Metro bundler](https://metrobundler.dev/) runs on port 8081. If another process is already using that port, you can either terminate that process, or change the port that the bundler uses.

#### Terminating a process on port 8081​

Run the following command to find the id for the process that is listening on port 8081:

 shell

```
sudo lsof -i :8081
```

Then run the following to terminate the process:

 shell

```
kill -9 <PID>
```

On Windows you can find the process using port 8081 using [Resource Monitor](https://stackoverflow.com/questions/48198/how-can-you-find-out-which-process-is-listening-on-a-port-on-windows) and stop it using Task Manager.

#### Using a port other than 8081​

You can configure the bundler to use a port other than 8081 by using the `port` parameter, from the root of your project run:

shell

```
npm start -- --port=8088
```

shell

```
yarn start --port 8088
```

You will also need to update your applications to load the JavaScript bundle from the new port. If running on device from Xcode, you can do this by updating occurrences of `8081` to your chosen port in the `ios/__App_Name__.xcodeproj/project.pbxproj` file.

### NPM locking error​

If you encounter an error such as `npm WARN locking Error: EACCES` while using the React Native CLI, try running the following:

 shell

```
sudo chown -R $USER ~/.npmsudo chown -R $USER /usr/local/lib/node_modules
```

### Missing libraries for React​

If you added React Native manually to your project, make sure you have included all the relevant dependencies that you are using, like `RCTText.xcodeproj`, `RCTImage.xcodeproj`. Next, the binaries built by these dependencies have to be linked to your app binary. Use the `Linked Frameworks and Binaries` section in the Xcode project settings. More detailed steps are here: [Linking Libraries](https://reactnative.dev/docs/linking-libraries-ios#content).

If you are using CocoaPods, verify that you have added React along with the subspecs to the `Podfile`. For example, if you were using the `<Text />`, `<Image />` and `fetch()` APIs, you would need to add these in your `Podfile`:

```
pod 'React', :path => '../node_modules/react-native', :subspecs => [  'RCTText',  'RCTImage',  'RCTNetwork',  'RCTWebSocket',]
```

Next, make sure you have run `pod install` and that a `Pods/` directory has been created in your project with React installed. CocoaPods will instruct you to use the generated `.xcworkspace` file henceforth to be able to use these installed dependencies.

#### React Native does not compile when being used as a CocoaPod​

There is a CocoaPods plugin called [cocoapods-fix-react-native](https://github.com/orta/cocoapods-fix-react-native) which handles any potential post-fixing of the source code due to differences when using a dependency manager.

#### Argument list too long: recursive header expansion failed​

In the project's build settings, `User Search Header Paths` and `Header Search Paths` are two configs that specify where Xcode should look for `#import` header files specified in the code. For Pods, CocoaPods uses a default array of specific folders to look in. Verify that this particular config is not overwritten, and that none of the folders configured are too large. If one of the folders is a large folder, Xcode will attempt to recursively search the entire directory and throw above error at some point.

To revert the `User Search Header Paths` and `Header Search Paths` build settings to their defaults set by CocoaPods - select the entry in the Build Settings panel, and hit delete. It will remove the custom override and return to the CocoaPod defaults.

### No transports available​

React Native implements a polyfill for WebSockets. These [polyfills](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/Core/InitializeCore.js) are initialized as part of the react-native module that you include in your application through `import React from 'react'`. If you load another module that requires WebSockets, such as [Firebase](https://github.com/facebook/react-native/issues/3645), be sure to load/require it after react-native:

```
import React from 'react';import Firebase from 'firebase';
```

## Shell Command Unresponsive Exception​

If you encounter a ShellCommandUnresponsiveException exception such as:

```
Execution failed for task ':app:installDebug'.  com.android.builder.testing.api.DeviceException: com.android.ddmlib.ShellCommandUnresponsiveException
```

Restart the ADB server by running the following commands in your terminal:

```
adb kill-serveradb start-server
```

## Unable to start react-native package manager (on Linux)​

### Case 1: Error "code":"ENOSPC","errno":"ENOSPC"​

Issue caused by the number of directories [inotify](https://github.com/guard/listen/blob/master/README.md#increasing-the-amount-of-inotify-watchers) (used by watchman on Linux) can monitor. To solve it, run this command in your terminal window

 shell

```
echo fs.inotify.max_user_watches=582222 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

### Error: spawnSync ./gradlew EACCES​

If you run into issue where executing `npm run android` or `yarn android` on macOS throws the above error, try to run `sudo chmod +x android/gradlew` command to make `gradlew` files into executable.

Is this page useful?

---

# Native Modules

> Your React Native application code may need to interact with native platform APIs that aren't provided by React Native or an existing library. You can write the integration code yourself using a Turbo Native Module. This guide will show you how to write one.

Your React Native application code may need to interact with native platform APIs that aren't provided by React Native or an existing library. You can write the integration code yourself using a **Turbo Native Module**. This guide will show you how to write one.

The basic steps are:

1. **define a typed JavaScript specification** using one of the most popular JavaScript type annotation languages: Flow or TypeScript;
2. **configure your dependency management system to run Codegen**, which converts the specification into native language interfaces;
3. **write your application code** using your specification; and
4. **write your native platform code using the generated interfaces** to write and hook your native code into the React Native runtime environment.

Lets work through each of these steps by building an example Turbo Native Module. The rest of this guide assume that you have created your application running the command:

 shell

```
npx @react-native-community/cli@latest init TurboModuleExample --version 0.83
```

## Native Persistent Storage​

This guide will show you how to write an implementation of the [Web Storage API](https://html.spec.whatwg.org/multipage/webstorage.html#dom-localstorage-dev): `localStorage`. The API is relatable to a React developer who might be writing application code on your project.

To make this work on mobile, we need to use Android and iOS APIs:

- Android: [SharedPreferences](https://developer.android.com/reference/android/content/SharedPreferences), and
- iOS: [NSUserDefaults](https://developer.apple.com/documentation/foundation/nsuserdefaults).

### 1. Declare Typed Specification​

React Native provides a tool called [Codegen](https://reactnative.dev/docs/the-new-architecture/what-is-codegen), which takes a specification written in TypeScript or Flow and generates platform specific code for Android and iOS. The specification declares the methods and data types that will pass back and forth between your native code and the React Native JavaScript runtime. A Turbo Native Module is both your specification, the native code you write, and the Codegen interfaces generated from your specification.

To create a specs file:

1. Inside the root folder of your app, create a new folder called `specs`.
2. Create a new file called `NativeLocalStorage.ts`.

 info

You can see all of the types you can use in your specification and the native types that are generated in the [Appendix](https://reactnative.dev/docs/appendix) documentation.

 info

If you want to change the name of your module and the related specs file, make sure to always use 'Native' as prefix (e.g. `NativeStorage` or `NativeUsersDefault`).

Here is an implementation of the `localStorage` specification:

specs/NativeLocalStorage.ts

```
import type {TurboModule} from 'react-native';import {TurboModuleRegistry} from 'react-native';export interface Spec extends TurboModule {  setItem(value: string, key: string): void;  getItem(key: string): string | null;  removeItem(key: string): void;  clear(): void;}export default TurboModuleRegistry.getEnforcing<Spec>(  'NativeLocalStorage',);
```

NativeLocalStorage.js

```
import type {TurboModule} from 'react-native';import {TurboModule, TurboModuleRegistry} from 'react-native';export interface Spec extends TurboModule {  setItem(value: string, key: string): void;  getItem(key: string): ?string;  removeItem(key: string): void;  clear(): void;}
```

### 2. Configure Codegen to run​

The specification is used by the React Native Codegen tools to generate platform specific interfaces and boilerplate for us. To do this, Codegen needs to know where to find our specification and what to do with it. Update your `package.json` to include:

 package.json

```
"start": "react-native start",     "test": "jest"   },   "codegenConfig": {     "name": "NativeLocalStorageSpec",     "type": "modules",     "jsSrcsDir": "specs",     "android": {       "javaPackageName": "com.nativelocalstorage"     }   },   "dependencies": {
```

With everything wired up for Codegen, we need to prepare our native code to hook into our generated code.

Codegen is executed through the `generateCodegenArtifactsFromSchema` Gradle task:

bash

```
cd android./gradlew generateCodegenArtifactsFromSchemaBUILD SUCCESSFUL in 837ms14 actionable tasks: 3 executed, 11 up-to-date
```

This is automatically run when you build your Android application.

Codegen is run as part of the script phases that's automatically added to the project generated by CocoaPods.

bash

```
cd iosbundle installbundle exec pod install
```

The output will look like this:

shell

```
...Framework build type is static library[Codegen] Adding script_phases to ReactCodegen.[Codegen] Generating ./build/generated/ios/ReactCodegen.podspec.json[Codegen] Analyzing /Users/me/src/TurboModuleExample/package.json[Codegen] Searching for codegen-enabled libraries in the app.[Codegen] Found TurboModuleExample[Codegen] Searching for codegen-enabled libraries in the project dependencies.[Codegen] Found react-native...
```

### 3. Write Application Code using the Turbo Native Module​

Using `NativeLocalStorage`, here’s a modified `App.tsx` that includes some text we want persisted, an input field and some buttons to update this value.

The `TurboModuleRegistry` supports 2 modes of retrieving a Turbo Native Module:

- `get<T>(name: string): T | null` which will return `null` if the Turbo Native Module is unavailable.
- `getEnforcing<T>(name: string): T` which will throw an exception if the Turbo Native Module is unavailable. This assumes the module is always available.

 App.tsx

```
import React from 'react';import {  SafeAreaView,  StyleSheet,  Text,  TextInput,  Button,} from 'react-native';import NativeLocalStorage from './specs/NativeLocalStorage';const EMPTY = '<empty>';function App(): React.JSX.Element {  const [value, setValue] = React.useState<string | null>(null);  const [editingValue, setEditingValue] = React.useState<    string | null  >(null);  React.useEffect(() => {    const storedValue = NativeLocalStorage?.getItem('myKey');    setValue(storedValue ?? '');  }, []);  function saveValue() {    NativeLocalStorage?.setItem(editingValue ?? EMPTY, 'myKey');    setValue(editingValue);  }  function clearAll() {    NativeLocalStorage?.clear();    setValue('');  }  function deleteValue() {    NativeLocalStorage?.removeItem('myKey');    setValue('');  }  return (    <SafeAreaView style={{flex: 1}}>      <Text style={styles.text}>        Current stored value is: {value ?? 'No Value'}      </Text>      <TextInput        placeholder="Enter the text you want to store"        style={styles.textInput}        onChangeText={setEditingValue}      />      <Button title="Save" onPress={saveValue} />      <Button title="Delete" onPress={deleteValue} />      <Button title="Clear" onPress={clearAll} />    </SafeAreaView>  );}const styles = StyleSheet.create({  text: {    margin: 10,    fontSize: 20,  },  textInput: {    margin: 10,    height: 40,    borderColor: 'black',    borderWidth: 1,    paddingLeft: 5,    paddingRight: 5,    borderRadius: 5,  },});export default App;
```

### 4. Write your Native Platform code​

With everything prepared, we're going to start writing native platform code. We do this in 2 parts:

 note

This guide shows you how to create a Turbo Native Module that only works with the New Architecture. If you need to support both the New Architecture and the Legacy Architecture, please refer to our [backwards compatibility guide](https://github.com/reactwg/react-native-new-architecture/blob/main/docs/backwards-compat.md).

Now it's time to write some Android platform code to make sure `localStorage` survives after the application is closed.

The first step is to implement the generated `NativeLocalStorageSpec` interface:

android/app/src/main/java/com/nativelocalstorage/NativeLocalStorageModule.java

```
package com.nativelocalstorage;import android.content.Context;import android.content.SharedPreferences;import com.nativelocalstorage.NativeLocalStorageSpec;import com.facebook.react.bridge.ReactApplicationContext;public class NativeLocalStorageModule extends NativeLocalStorageSpec {  public static final String NAME = "NativeLocalStorage";  public NativeLocalStorageModule(ReactApplicationContext reactContext) {    super(reactContext);  }  @Override  public String getName() {    return NAME;  }  @Override  public void setItem(String value, String key) {    SharedPreferences sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE);    SharedPreferences.Editor editor = sharedPref.edit();    editor.putString(key, value);    editor.apply();  }  @Override  public String getItem(String key) {    SharedPreferences sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE);    String username = sharedPref.getString(key, null);    return username;  }  @Override  public void removeItem(String key) {    SharedPreferences sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE);    sharedPref.edit().remove(key).apply();  }  @Override  public void clear() {    SharedPreferences sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE);    sharedPref.edit().clear().apply();  }}
```

android/app/src/main/java/com/nativelocalstorage/NativeLocalStorageModule.kt

```
package com.nativelocalstorageimport android.content.Contextimport android.content.SharedPreferencesimport com.nativelocalstorage.NativeLocalStorageSpecimport com.facebook.react.bridge.ReactApplicationContextclass NativeLocalStorageModule(reactContext: ReactApplicationContext) : NativeLocalStorageSpec(reactContext) {  override fun getName() = NAME  override fun setItem(value: String, key: String) {    val sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE)    val editor = sharedPref.edit()    editor.putString(key, value)    editor.apply()  }  override fun getItem(key: String): String? {    val sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE)    val username = sharedPref.getString(key, null)    return username.toString()  }  override fun removeItem(key: String) {    val sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE)    val editor = sharedPref.edit()    editor.remove(key)    editor.apply()  }  override fun clear() {    val sharedPref = getReactApplicationContext().getSharedPreferences("my_prefs", Context.MODE_PRIVATE)    val editor = sharedPref.edit()    editor.clear()    editor.apply()  }  companion object {    const val NAME = "NativeLocalStorage"  }}
```

Next we need to create `NativeLocalStoragePackage`. It provides an object to register our Module in the React Native runtime, by wrapping it as a Base Native Package:

android/app/src/main/java/com/nativelocalstorage/NativeLocalStoragePackage.java

```
package com.nativelocalstorage;import com.facebook.react.BaseReactPackage;import com.facebook.react.bridge.NativeModule;import com.facebook.react.bridge.ReactApplicationContext;import com.facebook.react.module.model.ReactModuleInfo;import com.facebook.react.module.model.ReactModuleInfoProvider;import java.util.HashMap;import java.util.Map;public class NativeLocalStoragePackage extends BaseReactPackage {  @Override  public NativeModule getModule(String name, ReactApplicationContext reactContext) {    if (name.equals(NativeLocalStorageModule.NAME)) {      return new NativeLocalStorageModule(reactContext);    } else {      return null;    }  }  @Override  public ReactModuleInfoProvider getReactModuleInfoProvider() {    return new ReactModuleInfoProvider() {      @Override      public Map<String, ReactModuleInfo> getReactModuleInfos() {        Map<String, ReactModuleInfo> map = new HashMap<>();        map.put(NativeLocalStorageModule.NAME, new ReactModuleInfo(          NativeLocalStorageModule.NAME,       // name          NativeLocalStorageModule.NAME,       // className          false, // canOverrideExistingModule          false, // needsEagerInit          false, // isCXXModule          true   // isTurboModule        ));        return map;      }    };  }}
```

android/app/src/main/java/com/nativelocalstorage/NativeLocalStoragePackage.kt

```
package com.nativelocalstorageimport com.facebook.react.BaseReactPackageimport com.facebook.react.bridge.NativeModuleimport com.facebook.react.bridge.ReactApplicationContextimport com.facebook.react.module.model.ReactModuleInfoimport com.facebook.react.module.model.ReactModuleInfoProviderclass NativeLocalStoragePackage : BaseReactPackage() {  override fun getModule(name: String, reactContext: ReactApplicationContext): NativeModule? =    if (name == NativeLocalStorageModule.NAME) {      NativeLocalStorageModule(reactContext)    } else {      null    }  override fun getReactModuleInfoProvider() = ReactModuleInfoProvider {    mapOf(      NativeLocalStorageModule.NAME to ReactModuleInfo(        name = NativeLocalStorageModule.NAME,        className = NativeLocalStorageModule.NAME,        canOverrideExistingModule = false,        needsEagerInit = false,        isCxxModule = false,        isTurboModule = true      )    )  }}
```

Finally, we need to tell the React Native in our main application how to find this `Package`. We call this "registering" the package in React Native.

In this case, you add it to be returned by the [getPackages](https://github.com/facebook/react-native/blob/8d8b8c343e62115a5509e1aed62047053c2f6e39/packages/react-native/ReactAndroid/src/main/java/com/facebook/react/ReactNativeHost.java#L233) method.

 info

Later you’ll learn how to distribute your Native Modules as [npm packages](https://reactnative.dev/docs/the-new-architecture/create-module-library#publish-the-library-on-npm), which our build tooling will autolink for you.

android/app/src/main/java/com/turobmoduleexample/MainApplication.java

```
package com.inappmodule;import android.app.Application;import com.facebook.react.PackageList;import com.facebook.react.ReactApplication;import com.facebook.react.ReactHost;import com.facebook.react.ReactNativeHost;import com.facebook.react.ReactPackage;import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint;import com.facebook.react.defaults.DefaultReactHost;import com.facebook.react.defaults.DefaultReactNativeHost;import com.facebook.soloader.SoLoader;import com.nativelocalstorage.NativeLocalStoragePackage;import java.util.ArrayList;import java.util.List;public class MainApplication extends Application implements ReactApplication {  private final ReactNativeHost reactNativeHost = new DefaultReactNativeHost(this) {    @Override    public List<ReactPackage> getPackages() {      List<ReactPackage> packages = new PackageList(this).getPackages();      // Packages that cannot be autolinked yet can be added manually here, for example:      // packages.add(new MyReactNativePackage());      packages.add(new NativeLocalStoragePackage());      return packages;    }    @Override    public String getJSMainModuleName() {      return "index";    }    @Override    public boolean getUseDeveloperSupport() {      return BuildConfig.DEBUG;    }    @Override    public boolean isNewArchEnabled() {      return BuildConfig.IS_NEW_ARCHITECTURE_ENABLED;    }    @Override    public boolean isHermesEnabled() {      return BuildConfig.IS_HERMES_ENABLED;    }  };  @Override  public ReactHost getReactHost() {    return DefaultReactHost.getDefaultReactHost(getApplicationContext(), reactNativeHost);  }  @Override  public void onCreate() {    super.onCreate();    SoLoader.init(this, false);    if (BuildConfig.IS_NEW_ARCHITECTURE_ENABLED) {      // If you opted-in for the New Architecture, we load the native entry point for this app.      DefaultNewArchitectureEntryPoint.load();    }  }}
```

android/app/src/main/java/com/turobmoduleexample/MainApplication.kt

```
package com.inappmoduleimport android.app.Applicationimport com.facebook.react.PackageListimport com.facebook.react.ReactApplicationimport com.facebook.react.ReactHostimport com.facebook.react.ReactNativeHostimport com.facebook.react.ReactPackageimport com.facebook.react.defaults.DefaultNewArchitectureEntryPoint.loadimport com.facebook.react.defaults.DefaultReactHost.getDefaultReactHostimport com.facebook.react.defaults.DefaultReactNativeHostimport com.facebook.soloader.SoLoaderimport com.nativelocalstorage.NativeLocalStoragePackageclass MainApplication : Application(), ReactApplication {  override val reactNativeHost: ReactNativeHost =      object : DefaultReactNativeHost(this) {        override fun getPackages(): List<ReactPackage> =            PackageList(this).packages.apply {              // Packages that cannot be autolinked yet can be added manually here, for example:              // add(MyReactNativePackage())              add(NativeLocalStoragePackage())            }        override fun getJSMainModuleName(): String = "index"        override fun getUseDeveloperSupport(): Boolean = BuildConfig.DEBUG        override val isNewArchEnabled: Boolean = BuildConfig.IS_NEW_ARCHITECTURE_ENABLED        override val isHermesEnabled: Boolean = BuildConfig.IS_HERMES_ENABLED      }  override val reactHost: ReactHost    get() = getDefaultReactHost(applicationContext, reactNativeHost)  override fun onCreate() {    super.onCreate()    SoLoader.init(this, false)    if (BuildConfig.IS_NEW_ARCHITECTURE_ENABLED) {      // If you opted-in for the New Architecture, we load the native entry point for this app.      load()    }  }}
```

You can now build and run your code on an emulator:

bash

```
npm run android
```

bash

```
yarn run android
```

Now it's time to write some iOS platform code to make sure `localStorage` survives after the application is closed.

## Prepare your Xcode Project​

We need to prepare your iOS project using Xcode. After completing these **6 steps** you'll have `RCTNativeLocalStorage` that implements the generated `NativeLocalStorageSpec` interface.

1. Open the CocoaPods generated Xcode Workspace:

 bash

```
cd iosopen TurboModuleExample.xcworkspace
```

 ![Open Xcode Workspace](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/1.webp)

1. Right click on app and select `New Group`, call the new group `NativeLocalStorage`.

 ![Right click on app and select New Group](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/2.webp)

1. In the `NativeLocalStorage` group, create `New`→`File from Template`.

 ![Create a new file using the Cocoa Touch Class template](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/3.webp)

1. Use the `Cocoa Touch Class`.

 ![Use the Cocoa Touch Class template](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/4.webp)

1. Name the Cocoa Touch Class `RCTNativeLocalStorage` with the `Objective-C` language.

 ![Create an Objective-C RCTNativeLocalStorage class](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/5.webp)

1. Rename `RCTNativeLocalStorage.m` → `RCTNativeLocalStorage.mm` making it an Objective-C++ file.

 ![Convert to and Objective-C++ file](https://reactnative.dev/docs/assets/turbo-native-modules/xcode/6.webp)

## Implement localStorage with NSUserDefaults​

Start by updating `RCTNativeLocalStorage.h`:

 NativeLocalStorage/RCTNativeLocalStorage.h

```
//  RCTNativeLocalStorage.h//  TurboModuleExample#import <Foundation/Foundation.h>#import <NativeLocalStorageSpec/NativeLocalStorageSpec.h>NS_ASSUME_NONNULL_BEGIN@interface RCTNativeLocalStorage : NSObject@interface RCTNativeLocalStorage : NSObject <NativeLocalStorageSpec>@end
```

Then update our implementation to use `NSUserDefaults` with a custom [suite name](https://developer.apple.com/documentation/foundation/nsuserdefaults/1409957-initwithsuitename).

 NativeLocalStorage/RCTNativeLocalStorage.mm

```
//  RCTNativeLocalStorage.m//  TurboModuleExample#import "RCTNativeLocalStorage.h"static NSString *const RCTNativeLocalStorageKey = @"local-storage";@interface RCTNativeLocalStorage()@property (strong, nonatomic) NSUserDefaults *localStorage;@end@implementation RCTNativeLocalStorage- (id) init {  if (self = [super init]) {    _localStorage = [[NSUserDefaults alloc] initWithSuiteName:RCTNativeLocalStorageKey];  }  return self;}- (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:(const facebook::react::ObjCTurboModule::InitParams &)params {  return std::make_shared<facebook::react::NativeLocalStorageSpecJSI>(params);}- (NSString * _Nullable)getItem:(NSString *)key {  return [self.localStorage stringForKey:key];}- (void)setItem:(NSString *)value          key:(NSString *)key {  [self.localStorage setObject:value forKey:key];}- (void)removeItem:(NSString *)key {  [self.localStorage removeObjectForKey:key];}- (void)clear {  NSDictionary *keys = [self.localStorage dictionaryRepresentation];  for (NSString *key in keys) {    [self removeItem:key];  }}+ (NSString *)moduleName{  return @"NativeLocalStorage";}@end
```

Important things to note:

- You can use Xcode to jump to the Codegen `@protocol NativeLocalStorageSpec`. You can also use Xcode to generate stubs for you.

## Register the Native Module in your app​

The last step consist in updating the `package.json` to tell React Native about the link between the JS specs of the Native Module and the concrete implementation of those specs in native code.

Modify the `package.json` as it follows:

 package.json

```
"start": "react-native start",     "test": "jest"   },   "codegenConfig": {     "name": "NativeLocalStorageSpec",     "type": "modules",     "jsSrcsDir": "specs",     "android": {       "javaPackageName": "com.sampleapp.specs"     },     "ios": {        "modulesProvider": {          "NativeLocalStorage": "RCTNativeLocalStorage"        }     }   },   "dependencies": {
```

At this point, you need to re-install the pods to make sure that codegen runs again to generate the new files:

 bash

```
# from the ios folderbundle exec pod installopen SampleApp.xcworkspace
```

If you now build your application from Xcode, you should be able to build successfully.

## Build and run your code on a Simulator​

bash

```
npm run ios
```

bash

```
yarn run ios
```

 Is this page useful?
