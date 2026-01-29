# Accessibility and more

# Accessibility

> Create mobile apps accessible to assistive technology with React Native's suite of APIs designed to work with Android and iOS.

Both Android and iOS provide APIs for integrating apps with assistive technologies like the bundled screen readers VoiceOver (iOS) and TalkBack (Android). React Native has complementary APIs that let your app accommodate all users.

 info

Android and iOS differ slightly in their approaches, and thus the React Native implementations may vary by platform.

## Accessibility properties​

### accessible​

When `true`, indicates that the view is discoverable by assistive technologies such as screen readers and hardware keyboards. Note that this does not necessarily mean that the view will be focused by VoiceOver or TalkBack. There are a number of reasons for this, such as VoiceOver disallowing nested accessibility elements, or TalkBack opting to focus some parent element instead.

By default, all touchable elements are accessible.

On Android, `accessible` will be translated into native [focusable](https://developer.android.com/reference/android/view/View#setFocusable(boolean)). On iOS, it translates into native [isAccessibilityElement](https://developer.apple.com/documentation/uikit/uiaccessibilityelement/isaccessibilityelement?language=objc).

 tsx

```
<View>  <View accessible={true} />  <View /></View>
```

In the above example, accessibility focus is only available on the first child view with the `accessible` property, and not for the parent or sibling without `accessible`.

### accessibilityLabel​

When a view is marked as accessible, it is a good practice to set an `accessibilityLabel` on the view, so that people who use VoiceOver or TalkBack know what element they have selected. A screen reader will verbalize this string when the associated element is selected.

To use, set the `accessibilityLabel` property to a custom string on your View, Text, or Touchable:

 tsx

```
<TouchableOpacity  accessible={true}  accessibilityLabel="Tap me!"  onPress={onPress}>  <View style={styles.button}>    <Text style={styles.buttonText}>Press me!</Text>  </View></TouchableOpacity>
```

In the above example, the `accessibilityLabel` on the TouchableOpacity element would default to "Press me!". The label is constructed by concatenating all Text node children separated by spaces.

### accessibilityLabelledByAndroid​

A reference to another element [nativeID](https://reactnative.dev/docs/view#nativeid) used to build complex forms.
The value of `accessibilityLabelledBy` should match the `nativeID` of the related element:

 tsx

```
<View>  <Text nativeID="formLabel">Label for Input Field</Text>  <TextInput    accessibilityLabel="input"    accessibilityLabelledBy="formLabel"  /></View>
```

In the above example, the screen reader announces `Input, Edit Box for Label for Input Field` when focusing on the TextInput.

### accessibilityHint​

An accessibility hint can be used to provide additional context to the user on the result of the action when it is not clear from the accessibility label alone.

Provide the `accessibilityHint` property a custom string on your View, Text, or Touchable:

 tsx

```
<TouchableOpacity  accessible={true}  accessibilityLabel="Go back"  accessibilityHint="Navigates to the previous screen"  onPress={onPress}>  <View style={styles.button}>    <Text style={styles.buttonText}>Back</Text>  </View></TouchableOpacity>
```

 iOS

In the above example, VoiceOver will read the hint after the label, if the user has hints enabled in the device's VoiceOver settings. Read more about guidelines for `accessibilityHint` in the [iOS Developer Docs](https://developer.apple.com/documentation/objectivec/nsobject/1615093-accessibilityhint)

 Android

In the above example, TalkBack will read the hint after the label. At this time, hints cannot be turned off on Android.

### accessibilityLanguageiOS​

By using the `accessibilityLanguage` property, the screen reader will understand which language to use while reading the element's **label**, **value**, and **hint**. The provided string value must follow the .

 tsx

```
<View  accessible={true}  accessibilityLabel="Pizza"  accessibilityLanguage="it-IT">  <Text>🍕</Text></View>
```

### accessibilityIgnoresInvertColorsiOS​

Inverting screen colors is an accessibility feature available in iOS and iPadOS for people with color blindness, low vision, or vision impairment. If there's a view you don't want to invert when this setting is on, possibly a photo, set this property to `true`.

### accessibilityLiveRegionAndroid​

When components dynamically change, we want TalkBack to alert the end user. This is made possible by the `accessibilityLiveRegion` property. It can be set to `none`, `polite`, and `assertive`:

- **none** Accessibility services should not announce changes to this view.
- **polite** Accessibility services should announce changes to this view.
- **assertive** Accessibility services should interrupt ongoing speech to immediately announce changes to this view.

 tsx

```
<TouchableWithoutFeedback onPress={addOne}>  <View style={styles.embedded}>    <Text>Click me</Text>  </View></TouchableWithoutFeedback><Text accessibilityLiveRegion="polite">  Clicked {count} times</Text>
```

In the above example method `addOne` changes the state variable `count`. When the TouchableWithoutFeedback is triggered, TalkBack reads the text in the Text view because of its `accessibilityLiveRegion="polite"` property.

### accessibilityRole​

`accessibilityRole` communicates the purpose of a component to the user of assistive technology.

`accessibilityRole` can be one of the following:

- **adjustable** Used when an element can be "adjusted" (e.g. a slider).
- **alert** Used when an element contains important text to be presented to the user.
- **button** Used when the element should be treated as a button.
- **checkbox** Used when an element represents a checkbox that can be checked, unchecked, or have a mixed checked state.
- **combobox** Used when an element represents a combo box, which allows the user to select among several choices.
- **header** Used when an element acts as a header for a content section (e.g. the title of a navigation bar).
- **image** Used when the element should be treated as an image. Can be combined with a button or link.
- **imagebutton** Used when the element should be treated as a button and is also an image.
- **keyboardkey** Used when the element acts as a keyboard key.
- **link** Used when the element should be treated as a link.
- **menu** Used when the component is a menu of choices.
- **menubar** Used when a component is a container of multiple menus.
- **menuitem** Used to represent an item within a menu.
- **none** Used when the element has no role.
- **progressbar** Used to represent a component that indicates the progress of a task.
- **radio** Used to represent a radio button.
- **radiogroup** Used to represent a group of radio buttons.
- **scrollbar** Used to represent a scroll bar.
- **search** Used when a text field element should also be treated as a search field.
- **spinbutton** Used to represent a button that opens a list of choices.
- **summary** Used when an element can be used to provide a quick summary of current conditions in the app when the app first launches.
- **switch** Used to represent a switch that can be turned on and off.
- **tab** Used to represent a tab.
- **tablist** Used to represent a list of tabs.
- **text** Used when the element should be treated as static text that cannot change.
- **timer** Used to represent a timer.
- **togglebutton** Used to represent a toggle button. Should be used with accessibilityState checked to indicate if the button is toggled on or off.
- **toolbar** Used to represent a toolbar (a container of action buttons or components).
- **grid** Used with ScrollView, VirtualizedList, FlatList, or SectionList to represent a grid. Adds the in/out of grid announcements to Android's GridView.

### accessibilityShowsLargeContentVieweriOS​

A boolean value that determines whether the large content viewer is shown when the user performs a long press on the element.

Available in iOS 13.0 and later.

### accessibilityLargeContentTitleiOS​

A string that will be used as the title of the large content viewer when it is shown.

Requires `accessibilityShowsLargeContentViewer` to be set to `true`.

 tsx

```
<View  accessibilityShowsLargeContentViewer={true}  accessibilityLargeContentTitle="Home Tab">  <Text>Home</Text></View>
```

### accessibilityState​

Describes the current state of a component to the assistive technology user.

`accessibilityState` is an object. It contains the following fields:

| Name | Description | Type | Required |
| --- | --- | --- | --- |
| disabled | Indicates whether the element is disabled or not. | boolean | No |
| selected | Indicates whether a selectable element is currently selected or not. | boolean | No |
| checked | Indicates the state of a checkable element. This field can either take a boolean or the "mixed" string to represent mixed checkboxes. | boolean or 'mixed' | No |
| busy | Indicates whether an element is currently busy or not. | boolean | No |
| expanded | Indicates whether an expandable element is currently expanded or collapsed. | boolean | No |

To use, set the `accessibilityState` to an object with a specific definition.

### accessibilityValue​

Represents the current value of a component. It can be a textual description of a component's value, or for range-based components, such as sliders and progress bars, it contains range information (minimum, current, and maximum).

`accessibilityValue` is an object. It contains the following fields:

| Name | Description | Type | Required |
| --- | --- | --- | --- |
| min | The minimum value of this component's range. | integer | Required ifnowis set. |
| max | The maximum value of this component's range. | integer | Required ifnowis set. |
| now | The current value of this component's range. | integer | No |
| text | A textual description of this component's value. Will overridemin,now, andmaxif set. | string | No |

### accessibilityViewIsModaliOS​

A boolean value that indicates whether VoiceOver should ignore the elements within views that are siblings of the receiver.

For example, in a window that contains sibling views `A` and `B`, setting `accessibilityViewIsModal` to `true` on view `B` causes VoiceOver to ignore the elements in view `A`. On the other hand, if view `B` contains a child view `C` and you set `accessibilityViewIsModal` to `true` on view `C`, VoiceOver does not ignore the elements in view `A`.

### accessibilityElementsHiddeniOS​

A boolean value indicating whether the given accessibility element, and any accessibility elements it contains, are hidden.

For example, in a window that contains sibling views `A` and `B`, setting `accessibilityElementsHidden` to `true` on view `B` causes VoiceOver to ignore the `B` view and any elements it contains. This is similar to the Android property `importantForAccessibility="no-hide-descendants"`.

### aria-valuemax​

Represents the maximum value for range-based components, such as sliders and progress bars.

### aria-valuemin​

Represents the minimum value for range-based components, such as sliders and progress bars.

### aria-valuenow​

Represents the current value for range-based components, such as sliders and progress bars.

### aria-valuetext​

Represents the textual description of the component.

### aria-busy​

Indicates an element is being modified and that assistive technologies may want to wait until the changes are complete before informing the user about the update.

| Type | Default |
| --- | --- |
| boolean | false |

### aria-checked​

Indicates the state of a checkable element. This field can either take a boolean or the "mixed" string to represent mixed checkboxes.

| Type | Default |
| --- | --- |
| boolean, 'mixed' | false |

### aria-disabled​

Indicates that the element is perceivable but disabled, so it is not editable or otherwise operable.

| Type | Default |
| --- | --- |
| boolean | false |

### aria-expanded​

Indicates whether an expandable element is currently expanded or collapsed.

| Type | Default |
| --- | --- |
| boolean | false |

### aria-hidden​

Indicates whether the element is hidden from assistive technologies.

For example, in a window that contains sibling views `A` and `B`, setting `aria-hidden` to `true` on view `B` causes VoiceOver to ignore the `B` element and its children.

| Type | Default |
| --- | --- |
| boolean | false |

### aria-label​

Defines a string value that can be used to name an element.

| Type |
| --- |
| string |

### aria-labelledbyAndroid​

Identifies the element that labels the element it is applied to. The value of `aria-labelledby` should match the [nativeID](https://reactnative.dev/docs/view#nativeid) of the related element:

 tsx

```
<View>  <Text nativeID="formLabel">Label for Input Field</Text>  <TextInput aria-label="input" aria-labelledby="formLabel" /></View>
```

| Type |
| --- |
| string |

### aria-liveAndroid​

Indicates that an element will be updated and describes the types of updates the user agents, assistive technologies, and user can expect from the live region.

- **off** Accessibility services should not announce changes to this view.
- **polite** Accessibility services should announce changes to this view.
- **assertive** Accessibility services should interrupt ongoing speech to immediately announce changes to this view.

| Type | Default |
| --- | --- |
| enum('assertive','off','polite') | 'off' |

---

### aria-modaliOS​

Boolean value indicating whether VoiceOver should ignore the elements within views that are siblings of the receiver.

| Type | Default |
| --- | --- |
| boolean | false |

### aria-selected​

Indicates whether a selectable element is currently selected or not.

| Type |
| --- |
| boolean |

### experimental_accessibilityOrder​

 Experimental 🧪

**This API is experimental.** Experimental APIs may contain bugs and are likely to change in a future version of React Native. Don't use them in production.

 note

For the sake of brevity, layout is excluded in the following examples even though it dictates the default focus order. Assume the document order matches the layout order.

`experimental_accessibilityOrder` lets you define the order in which assistive technologies focus descendant components. It is an array of [nativeIDs](https://reactnative.dev/docs/view#nativeid) that are set on the components whose order you are controlling. For example:

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View accessible={true} nativeID="C"/></View>
```

Assistive technologies will focus the `View` with `nativeID` of `B`, then `C`, then `A`.

`experimental_accessibilityOrder` will not “turn on” accessibility for the components it references, that still needs to be done. So if we remove `accessible={true}` on `C` above like so

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View nativeID="C"/></View>
```

then the new order will be `B` then `A`, even though `C` is still in `experimental_accessibilityOrder`.

`experimental_accessibilityOrder` will “turn off” accessibility of components it doesn’t reference, however.

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View accessible={true} nativeID="C"/>  <View accessible={true} nativeID="D"/></View>
```

The order of the above example would be `B`, `C`, `A`. `D` will never get focused. In this sense `experimental_accessibilityOrder` is *exhaustive*.

There are still valid reasons to include an non-accessible component in `experimental_accessibilityOrder`. Consider

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View nativeID="C">    <View accessible={true} nativeID="D"/>    <View accessible={true} nativeID="E"/>    <View accessible={true} nativeID="F"/>  </View></View>
```

The focus order will be `B`, `D`, `E`, `F`, `A`. Even though `D`, `E`, and `F` are not directly referenced in `experimental_accessibilityOrder`, `C` is directly referenced. In this instance `C` in an *accessibility container* - it contains accessible elements, but is not accessible itself. If an accessibility container is referenced in `experimental_accessibilityOrder` then the default order of the elements it contains is applied. In this sense `experimental_accessibilityOrder` is *nestable*.

`experimental_accessibilityOrder` can also reference another component with `experimental_accessibilityOrder`

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View nativeID="C" experimental_accessibilityOrder={['F', 'E', 'D']}>    <View accessible={true} nativeID="D"/>    <View accessible={true} nativeID="E"/>    <View accessible={true} nativeID="F"/>  </View></View>
```

The focus order will be `B`, `F`, `E`, `D`, `A`.

A component cannot be both an accessibility container and an accessibility element (`accessible={true}`). So if we have

```
<View experimental_accessibilityOrder={['B', 'C', 'A']}>  <View accessible={true} nativeID="A"/>  <View accessible={true} nativeID="B"/>  <View accessible={true} nativeID="C" experimental_accessibilityOrder={['F', 'E', 'D']}>    <View accessible={true} nativeID="D"/>    <View accessible={true} nativeID="E"/>    <View accessible={true} nativeID="F"/>  </View></View>
```

The focus order would be `B`, `C`, `A`. `D`, `E`, and `F` are no longer in a container, so the exhaustive nature of `experimental_accessibilityOrder` means they will be excluded.

### importantForAccessibilityAndroid​

In the case of two overlapping UI components with the same parent, default accessibility focus can have unpredictable behavior. The `importantForAccessibility` property will resolve this by controlling if a view fires accessibility events and if it is reported to accessibility services. It can be set to `auto`, `yes`, `no` and `no-hide-descendants` (the last value will force accessibility services to ignore the component and all of its children).

 tsx

```
<View style={styles.container}>  <View    style={[styles.layout, {backgroundColor: 'green'}]}    importantForAccessibility="yes">    <Text>First layout</Text>  </View>  <View    style={[styles.layout, {backgroundColor: 'yellow'}]}    importantForAccessibility="no-hide-descendants">    <Text>Second layout</Text>  </View></View>
```

In the above example, the `yellow` layout and its descendants are completely invisible to TalkBack and all other accessibility services. So we can use overlapping views with the same parent without confusing TalkBack.

### onAccessibilityEscapeiOS​

Assign this property to a custom function which will be called when someone performs the "escape" gesture, which is a two finger Z shaped gesture. An escape function should move back hierarchically in the user interface. This can mean moving up or back in a navigation hierarchy or dismissing a modal user interface. If the selected element does not have an `onAccessibilityEscape` function, the system will attempt to traverse up the view hierarchy until it finds a view that does or bonk to indicate it was unable to find one.

### onAccessibilityTapiOS​

Use this property to assign a custom function to be called when someone activates an accessible element by double tapping on it while it's selected.

### onMagicTapiOS​

Assign this property to a custom function which will be called when someone performs the "magic tap" gesture, which is a double-tap with two fingers. A magic tap function should perform the most relevant action a user could take on a component. In the Phone app on iPhone, a magic tap answers a phone call or ends the current one. If the selected element does not have an `onMagicTap` function, the system will traverse up the view hierarchy until it finds a view that does.

### role​

`role` communicates the purpose of a component and has precedence over the [accessibilityRole](https://reactnative.dev/docs/accessibility#accessibilityrole) prop.

`role` can be one of the following:

- **alert** Used when an element contains important text to be presented to the user.
- **button** Used when the element should be treated as a button.
- **checkbox** Used when an element represents a checkbox that can be checked, unchecked, or have a mixed checked state.
- **combobox** Used when an element represents a combo box, which allows the user to select among several choices.
- **grid** Used with ScrollView, VirtualizedList, FlatList, or SectionList to represent a grid. Adds the in/out of grid announcements to the android GridView.
- **heading** Used when an element acts as a header for a content section (e.g. the title of a navigation bar).
- **img** Used when the element should be treated as an image. Can be combined with a button or link, for example.
- **link** Used when the element should be treated as a link.
- **list** Used to identify a list of items.
- **listitem** Used to itentify an item in a list.
- **menu** Used when the component is a menu of choices.
- **menubar** Used when a component is a container of multiple menus.
- **menuitem** Used to represent an item within a menu.
- **none** Used when the element has no role.
- **presentation** Used when the element has no role.
- **progressbar** Used to represent a component that indicates the progress of a task.
- **radio** Used to represent a radio button.
- **radiogroup** Used to represent a group of radio buttons.
- **scrollbar** Used to represent a scroll bar.
- **searchbox** Used when the text field element should also be treated as a search field.
- **slider** Used when an element can be "adjusted" (e.g. a slider).
- **spinbutton** Used to represent a button that opens a list of choices.
- **summary** Used when an element can be used to provide a quick summary of current conditions in the app when the app first launches.
- **switch** Used to represent a switch that can be turned on and off.
- **tab** Used to represent a tab.
- **tablist** Used to represent a list of tabs.
- **timer** Used to represent a timer.
- **toolbar** Used to represent a toolbar (a container of action buttons or components).

## Accessibility Actions​

Accessibility actions allow assistive technology to programmatically invoke the action(s) of a component. To support accessibility actions, a component must do two things:

- Define the list of actions it supports via the `accessibilityActions` property.
- Implement an `onAccessibilityAction` function to handle action requests.

The `accessibilityActions` property should contain a list of action objects. Each action object should contain the following fields:

| Name | Type | Required |
| --- | --- | --- |
| name | string | Yes |
| label | string | No |

Actions either represent standard actions, such as clicking a button or adjusting a slider, or custom actions specific to a given component such as deleting an email message. The `name` field is required for both standard and custom actions, but `label` is optional for standard actions.

When adding support for standard actions, `name` must be one of the following:

- `'magicTap'` - iOS only - While VoiceOver focus is on or inside the component, the user double tapped with two fingers.
- `'escape'` - iOS only - While VoiceOver focus is on or inside the component, the user performed a two-finger scrub gesture (left, right, left).
- `'activate'` - Activate the component. This should perform the same action with, or without, assistive technology. Engaged when a screen reader user double taps the component.
- `'increment'` - Increment an adjustable component. On iOS, VoiceOver generates this action when the component has a role of `'adjustable'` and the user places focus on it and swipes upward. On Android, TalkBack generates this action when the user places accessibility focus on the component and presses the volume-up button.
- `'decrement'` - Decrement an adjustable component. On iOS, VoiceOver generates this action when the component has a role of `'adjustable'` and the user places focus on it and swipes downward. On Android, TalkBack generates this action when the user places accessibility focus on the component and presses the volume-down button.
- `'longpress'` - Android only - This action is generated when the user places accessibility focus on the component, then double-taps and holds one finger on the screen. This should perform the same action with, or without, assistive technology.
- `'expand'` - Android only - This action "expands" the component so that TalkBack will announce an "expanded" hint.
- `'collapse'` - Android only - This action "collapses" the component so that TalkBack will announce a "collapsed" hint.

The `label` field is optional for standard actions and is often unused by assistive technologies. For custom actions, it is a localized string containing a description of the action to be presented to the user.

To handle action requests, a component must implement an `onAccessibilityAction` function. The only argument to this function is an event containing the name of the action to perform. The below example from RNTester shows how to create a component that defines and handles several custom actions.

 tsx

```
<View  accessible={true}  accessibilityActions={[    {name: 'cut', label: 'cut'},    {name: 'copy', label: 'copy'},    {name: 'paste', label: 'paste'},  ]}  onAccessibilityAction={event => {    switch (event.nativeEvent.actionName) {      case 'cut':        Alert.alert('Alert', 'cut action success');        break;      case 'copy':        Alert.alert('Alert', 'copy action success');        break;      case 'paste':        Alert.alert('Alert', 'paste action success');        break;    }  }}/>
```

## Checking if a Screen Reader is Enabled​

The `AccessibilityInfo` API allows you to determine whether or not a screen reader is currently active. See the [AccessibilityInfo documentation](https://reactnative.dev/docs/accessibilityinfo) for details.

## Sending Accessibility EventsAndroid​

Sometimes it is useful to trigger an accessibility event on a UI component (i.e. when a custom view appears on a screen or set accessibility focus to a view). Native UIManager module exposes a method ‘sendAccessibilityEvent’ for this purpose. It takes two arguments: a view tag and a type of event. The supported event types are `typeWindowStateChanged`, `typeViewFocused`, and `typeViewClicked`.

 tsx

```
import {Platform, UIManager, findNodeHandle} from 'react-native';if (Platform.OS === 'android') {  UIManager.sendAccessibilityEvent(    findNodeHandle(this),    UIManager.AccessibilityEventTypes.typeViewFocused,  );}
```

## Testing TalkBack SupportAndroid​

To enable TalkBack, go to the Settings app on your Android device or emulator. Tap Accessibility, then TalkBack. Toggle the "Use service" switch to enable or disable it.

Android emulators don't have TalkBack installed by default. You can install TalkBack on your emulator via the Google Play Store. Make sure to choose an emulator with the Google Play store installed. These are available in Android Studio.

You can use the volume key shortcut to toggle TalkBack. To turn on the volume key shortcut, go to the Settings app, then Accessibility. At the top, turn on the volume key shortcut.

To use the volume key shortcut, press both volume keys for 3 seconds to start an accessibility tool.

Additionally, if you prefer, you can toggle TalkBack via the command line with:

 shell

```
# disableadb shell settings put secure enabled_accessibility_services com.android.talkback/com.google.android.marvin.talkback.TalkBackService# enableadb shell settings put secure enabled_accessibility_services com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService
```

## Testing VoiceOver SupportiOS​

To enable VoiceOver on your iOS or iPadOS device, go to the Settings app, tap General, then Accessibility. There you will find many tools available for people to enable their devices to be more usable, including VoiceOver. To enable VoiceOver, tap on VoiceOver under "Vision" and toggle the switch that appears at the top.

At the very bottom of the Accessibility settings, there is an "Accessibility Shortcut". You can use this to toggle VoiceOver by triple-clicking the Home button.

VoiceOver isn't available via the simulator, but you can use Accessibility Inspector from Xcode to use the macOS VoiceOver through an application. Note it's always best to test with a device as macOS's VoiceOver may result in varied experiences.

## Additional Resources​

- [Making React Native Apps Accessible](https://engineering.fb.com/ios/making-react-native-apps-accessible/)

Is this page useful?

---

# AccessibilityInfo

> Sometimes it's useful to know whether or not the device has a screen reader that is currently active. The AccessibilityInfo API is designed for this purpose. You can use it to query the current state of the screen reader as well as to register to be notified when the state of the screen reader changes.

Sometimes it's useful to know whether or not the device has a screen reader that is currently active. The `AccessibilityInfo` API is designed for this purpose. You can use it to query the current state of the screen reader as well as to register to be notified when the state of the screen reader changes.

## Example​

---

# Reference

## Methods​

### addEventListener()​

 tsx

```
static addEventListener(  eventName: AccessibilityChangeEventName | AccessibilityAnnouncementEventName,  handler: (    event: AccessibilityChangeEvent | AccessibilityAnnouncementFinishedEvent,  ) => void,): EmitterSubscription;
```

Add an event handler. Supported events:

| Event name | Description |
| --- | --- |
| accessibilityServiceChangedAndroid | Fires when some services such as TalkBack, other Android assistive technologies, and third-party accessibility services are enabled. The argument to the event handler is a boolean. The boolean istruewhen a some accessibility services is enabled andfalseotherwise. |
| announcementFinishediOS | Fires when the screen reader has finished making an announcement. The argument to the event handler is a dictionary with these keys:announcement: The string announced by the screen reader.success: A boolean indicating whether the announcement was successfully made. |
| boldTextChangediOS | Fires when the state of the bold text toggle changes. The argument to the event handler is a boolean. The boolean istruewhen bold text is enabled andfalseotherwise. |
| grayscaleChangediOS | Fires when the state of the gray scale toggle changes. The argument to the event handler is a boolean. The boolean istruewhen a gray scale is enabled andfalseotherwise. |
| invertColorsChangediOS | Fires when the state of the invert colors toggle changes. The argument to the event handler is a boolean. The boolean istruewhen invert colors is enabled andfalseotherwise. |
| reduceMotionChanged | Fires when the state of the reduce motion toggle changes. The argument to the event handler is a boolean. The boolean istruewhen a reduce motion is enabled (or when "Transition Animation Scale" in "Developer options" is "Animation off") andfalseotherwise. |
| reduceTransparencyChangediOS | Fires when the state of the reduce transparency toggle changes. The argument to the event handler is a boolean. The boolean istruewhen reduce transparency is enabled andfalseotherwise. |
| screenReaderChanged | Fires when the state of the screen reader changes. The argument to the event handler is a boolean. The boolean istruewhen a screen reader is enabled andfalseotherwise. |

---

### announceForAccessibility()​

 tsx

```
static announceForAccessibility(announcement: string);
```

Post a string to be announced by the screen reader.

---

### announceForAccessibilityWithOptions()​

 tsx

```
static announceForAccessibilityWithOptions(  announcement: string,  options: {queue?: boolean},);
```

Post a string to be announced by the screen reader with modification options. By default announcements will interrupt any existing speech, but on iOS they can be queued behind existing speech by setting `queue` to `true` in the options object.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| announcementRequired | string | The string to be announced |
| optionsRequired | object | queue- queue the announcement behind existing speechiOS |

---

### getRecommendedTimeoutMillis()Android​

 tsx

```
static getRecommendedTimeoutMillis(originalTimeout: number): Promise<number>;
```

Gets the timeout in millisecond that the user needs.
This value is set in "Time to take action (Accessibility timeout)" of "Accessibility" settings.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| originalTimeoutRequired | number | The timeout to return if "Accessibility timeout" is not set. Specify in milliseconds. |

---

### isAccessibilityServiceEnabled()Android​

 tsx

```
static isAccessibilityServiceEnabled(): Promise<boolean>;
```

Check whether any accessibility service is enabled. This includes TalkBack but also any third-party accessibility app that may be installed. To only check whether TalkBack is enabled, use [isScreenReaderEnabled](#isscreenreaderenabled). Returns a promise which resolves to a boolean. The result is `true` when some accessibility services is enabled and `false` otherwise.

 note

Please use [isScreenReaderEnabled](#isscreenreaderenabled) if you only want to check the status of TalkBack.

---

### isBoldTextEnabled()iOS​

 tsx

```
static isBoldTextEnabled(): Promise<boolean>:
```

Query whether a bold text is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when bold text is enabled and `false` otherwise.

---

### isGrayscaleEnabled()iOS​

 tsx

```
static isGrayscaleEnabled(): Promise<boolean>;
```

Query whether grayscale is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when grayscale is enabled and `false` otherwise.

---

### isInvertColorsEnabled()iOS​

 tsx

```
static isInvertColorsEnabled(): Promise<boolean>;
```

Query whether invert colors is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when invert colors is enabled and `false` otherwise.

---

### isReduceMotionEnabled()​

 tsx

```
static isReduceMotionEnabled(): Promise<boolean>;
```

Query whether reduce motion is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when reduce motion is enabled and `false` otherwise.

---

### isReduceTransparencyEnabled()iOS​

 tsx

```
static isReduceTransparencyEnabled(): Promise<boolean>;
```

Query whether reduce transparency is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when a reduce transparency is enabled and `false` otherwise.

---

### isScreenReaderEnabled()​

 tsx

```
static isScreenReaderEnabled(): Promise<boolean>;
```

Query whether a screen reader is currently enabled. Returns a promise which resolves to a boolean. The result is `true` when a screen reader is enabled and `false` otherwise.

---

### prefersCrossFadeTransitions()iOS​

 tsx

```
static prefersCrossFadeTransitions(): Promise<boolean>;
```

Query whether reduce motion and prefer cross-fade transitions settings are currently enabled. Returns a promise which resolves to a boolean. The result is `true` when prefer cross-fade transitions is enabled and `false` otherwise.

---

### 🗑️setAccessibilityFocus()​

 Deprecated

Prefer using `sendAccessibilityEvent` with eventType `focus` instead.

 tsx

```
static setAccessibilityFocus(reactTag: number);
```

Set accessibility focus to a React component.

On Android, this calls `UIManager.sendAccessibilityEvent` method with passed `reactTag` and `UIManager.AccessibilityEventTypes.typeViewFocused` arguments.

 note

Make sure that any `View` you want to receive the accessibility focus has `accessible={true}`.

---

### sendAccessibilityEvent()​

 tsx

```
static sendAccessibilityEvent(host: HostInstance, eventType: AccessibilityEventTypes);
```

Imperatively trigger an accessibility event on a React component, like changing the focused element for a screen reader.

 note

Make sure that any `View` you want to receive the accessibility focus has `accessible={true}`.

| Name | Type | Description |
| --- | --- | --- |
| hostRequired | HostInstance | The component ref to send the event to. |
| eventTypeRequired | AccessibilityEventTypes | One of'click'(Android only),'focus','viewHoverEnter'(Android only), or'windowStateChange'(Android only) |

Is this page useful?

---

# ActionSheetIOS

> Displays native to iOS Action Sheet component.

Displays native to iOS [Action Sheet](https://developer.apple.com/design/human-interface-guidelines/action-sheets) component.

## Example​

# Reference

## Methods​

### showActionSheetWithOptions()​

 tsx

```
static showActionSheetWithOptions: (  options: ActionSheetIOSOptions,  callback: (buttonIndex: number) => void,);
```

Display an iOS action sheet. The `options` object must contain one or more of:

- `options` (array of strings) - a list of button titles (required)
- `cancelButtonIndex` (int) - index of cancel button in `options`
- `cancelButtonTintColor` (string) - the [color](https://reactnative.dev/docs/colors) used for the change the text color of the cancel button
- `destructiveButtonIndex` (int or array of ints) - indices of destructive buttons in `options`
- `title` (string) - a title to show above the action sheet
- `message` (string) - a message to show below the title
- `anchor` (number) - the node to which the action sheet should be anchored (used for iPad)
- `tintColor` (string) - the [color](https://reactnative.dev/docs/colors) used for non-destructive button titles
- `disabledButtonIndices` (array of numbers) - a list of button indices which should be disabled
- `userInterfaceStyle` (string) - the interface style used for the action sheet, can be set to `light` or `dark`, otherwise the default system style will be used

The 'callback' function takes one parameter, the zero-based index of the selected item.

Minimal example:

 tsx

```
ActionSheetIOS.showActionSheetWithOptions(  {    options: ['Cancel', 'Remove'],    destructiveButtonIndex: 1,    cancelButtonIndex: 0,  },  buttonIndex => {    if (buttonIndex === 1) {      /* destructive action */    }  },);
```

---

### dismissActionSheet()​

 tsx

```
static dismissActionSheet();
```

Dismisses the most upper iOS action sheet presented, if no action sheet is present a warning is displayed.

---

### showShareActionSheetWithOptions()​

 tsx

```
static showShareActionSheetWithOptions: (  options: ShareActionSheetIOSOptions,  failureCallback: (error: Error) => void,  successCallback: (success: boolean, method: string) => void,);
```

Display the iOS share sheet. The `options` object should contain one or both of `message` and `url` and can additionally have a `subject` or `excludedActivityTypes`:

- `url` (string) - a URL to share
- `message` (string) - a message to share
- `subject` (string) - a subject for the message
- `excludedActivityTypes` (array) - the activities to exclude from the ActionSheet

 note

If `url` points to a local file, or is a base64-encoded uri, the file it points to will be loaded and shared directly. In this way, you can share images, videos, PDF files, etc. If `url` points to a remote file or address it must conform to URL format as described in [RFC 2396](https://www.ietf.org/rfc/rfc2396.txt). For example, a web URL without a proper protocol (HTTP/HTTPS) will not be shared.

The 'failureCallback' function takes one parameter, an error object. The only property defined on this object is an optional `stack` property of type `string`.

The 'successCallback' function takes two parameters:

- a boolean value signifying success or failure
- a string that, in the case of success, indicates the method of sharing

Is this page useful?

---

# ActivityIndicator

> Displays a circular loading indicator.

Displays a circular loading indicator.

## Example​

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### animating​

Whether to show the indicator (`true`) or hide it (`false`).

| Type | Default |
| --- | --- |
| bool | true |

---

### color​

The foreground color of the spinner.

| Type | Default |
| --- | --- |
| color | null(system accent default color)Android'#999999'iOS |

---

### hidesWhenStoppediOS​

Whether the indicator should hide when not animating.

| Type | Default |
| --- | --- |
| bool | true |

---

### ref​

A ref setter that will be assigned an [element node](https://reactnative.dev/docs/element-nodes) when mounted.

---

### size​

Size of the indicator.

| Type | Default |
| --- | --- |
| enum('small','large')numberAndroid | 'small' |

Is this page useful?
