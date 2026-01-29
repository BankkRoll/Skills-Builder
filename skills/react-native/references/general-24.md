# TextInput and more

# TextInput

> A foundational component for inputting text into the app via a keyboard. Props provide configurability for several features, such as auto-correction, auto-capitalization, placeholder text, and different keyboard types, such as a numeric keypad.

A foundational component for inputting text into the app via a keyboard. Props provide configurability for several features, such as auto-correction, auto-capitalization, placeholder text, and different keyboard types, such as a numeric keypad.

The most basic use case is to plop down a `TextInput` and subscribe to the `onChangeText` events to read the user input. There are also other events, such as `onSubmitEditing` and `onFocus` that can be subscribed to. A minimal example:

Two methods exposed via the native element are `.focus()` and `.blur()` that will focus or blur the TextInput programmatically.

Note that some props are only available with `multiline={true/false}`. Additionally, border styles that apply to only one side of the element (e.g., `borderBottomColor`, `borderLeftWidth`, etc.) will not be applied if `multiline=true`. To achieve the same effect, you can wrap your `TextInput` in a `View`:

`TextInput` has a border at the bottom of its view by default. This border has its padding set by the background image provided by the system, and it cannot be changed. Solutions to avoid this are to either not set height explicitly, in which case the system will take care of displaying the border in the correct position, or to not display the border by setting `underlineColorAndroid` to transparent.

Note that on Android performing text selection in an input can change the app's activity `windowSoftInputMode` param to `adjustResize`. This may cause issues with components that have position: 'absolute' while the keyboard is active. To avoid this behavior either specify `windowSoftInputMode` in AndroidManifest.xml ( [https://developer.android.com/guide/topics/manifest/activity-element.html](https://developer.android.com/guide/topics/manifest/activity-element.html) ) or control this param programmatically with native code.

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### allowFontScaling​

Specifies whether fonts should scale to respect Text Size accessibility settings. The default is `true`.

| Type |
| --- |
| bool |

---

### autoCapitalize​

Tells `TextInput` to automatically capitalize certain characters. This property is not supported by some keyboard types such as `name-phone-pad`.

- `characters`: all characters.
- `words`: first letter of each word.
- `sentences`: first letter of each sentence (*default*).
- `none`: don't auto capitalize anything.

| Type |
| --- |
| enum('none', 'sentences', 'words', 'characters') |

---

### autoComplete​

Specifies autocomplete hints for the system, so it can provide autofill. On Android, the system will always attempt to offer autofill by using heuristics to identify the type of content. To disable autocomplete, set `autoComplete` to `off`.

The following values work across platforms:

- `additional-name`
- `address-line1`
- `address-line2`
- `birthdate-day` (iOS 17+)
- `birthdate-full` (iOS 17+)
- `birthdate-month` (iOS 17+)
- `birthdate-year` (iOS 17+)
- `cc-csc` (iOS 17+)
- `cc-exp` (iOS 17+)
- `cc-exp-day` (iOS 17+)
- `cc-exp-month` (iOS 17+)
- `cc-exp-year` (iOS 17+)
- `cc-number`
- `country`
- `current-password`
- `email`
- `family-name`
- `given-name`
- `honorific-prefix`
- `honorific-suffix`
- `name`
- `new-password`
- `off`
- `one-time-code`
- `postal-code`
- `street-address`
- `tel`
- `username`

 iOS

The following values work on iOS only:

- `cc-family-name` (iOS 17+)
- `cc-given-name` (iOS 17+)
- `cc-middle-name` (iOS 17+)
- `cc-name` (iOS 17+)
- `cc-type` (iOS 17+)
- `nickname`
- `organization`
- `organization-title`
- `url`

 Android

The following values work on Android only:

- `gender`
- `name-family`
- `name-given`
- `name-middle`
- `name-middle-initial`
- `name-prefix`
- `name-suffix`
- `password`
- `password-new`
- `postal-address`
- `postal-address-country`
- `postal-address-extended`
- `postal-address-extended-postal-code`
- `postal-address-locality`
- `postal-address-region`
- `sms-otp`
- `tel-country-code`
- `tel-device`
- `tel-national`
- `username-new`

| Type |
| --- |
| enum('additional-name', 'address-line1', 'address-line2', 'birthdate-day', 'birthdate-full', 'birthdate-month', 'birthdate-year', 'cc-csc', 'cc-exp', 'cc-exp-day', 'cc-exp-month', 'cc-exp-year', 'cc-number', 'country', 'current-password', 'email', 'family-name', 'given-name', 'honorific-prefix', 'honorific-suffix', 'name', 'new-password', 'off', 'one-time-code', 'postal-code', 'street-address', 'tel', 'username', 'cc-family-name', 'cc-given-name', 'cc-middle-name', 'cc-name', 'cc-type', 'nickname', 'organization', 'organization-title', 'url', 'gender', 'name-family', 'name-given', 'name-middle', 'name-middle-initial', 'name-prefix', 'name-suffix', 'password', 'password-new', 'postal-address', 'postal-address-country', 'postal-address-extended', 'postal-address-extended-postal-code', 'postal-address-locality', 'postal-address-region', 'sms-otp', 'tel-country-code', 'tel-device', 'tel-national', 'username-new') |

---

### autoCorrect​

If `false`, disables auto-correct. The default value is `true`.

| Type |
| --- |
| bool |

---

### autoFocus​

If `true`, focuses the input. The default value is `false`.

| Type |
| --- |
| bool |

---

### 🗑️blurOnSubmit​

 Deprecated

Note that `submitBehavior` now takes the place of `blurOnSubmit` and will override any behavior defined by `blurOnSubmit`. See [submitBehavior](https://reactnative.dev/docs/textinput#submitbehavior).

If `true`, the text field will blur when submitted. The default value is true for single-line fields and false for multiline fields. Note that for multiline fields, setting `blurOnSubmit` to `true` means that pressing return will blur the field and trigger the `onSubmitEditing` event instead of inserting a newline into the field.

| Type |
| --- |
| bool |

---

### caretHidden​

If `true`, caret is hidden. The default value is `false`.

| Type |
| --- |
| bool |

---

### clearButtonModeiOS​

When the clear button should appear on the right side of the text view. This property is supported only for single-line TextInput component. The default value is `never`.

| Type |
| --- |
| enum('never', 'while-editing', 'unless-editing', 'always') |

---

### clearTextOnFocusiOS​

If `true`, clears the text field automatically when editing begins.

| Type |
| --- |
| bool |

---

### contextMenuHidden​

If `true`, context menu is hidden. The default value is `false`.

| Type |
| --- |
| bool |

---

### dataDetectorTypesiOS​

Determines the types of data converted to clickable URLs in the text input. Only valid if `multiline={true}` and `editable={false}`. By default no data types are detected.

You can provide one type or an array of many types.

Possible values for `dataDetectorTypes` are:

- `'phoneNumber'`
- `'link'`
- `'address'`
- `'calendarEvent'`
- `'none'`
- `'all'`

| Type |
| --- |
| enum('phoneNumber', 'link', 'address', 'calendarEvent', 'none', 'all'), ,array of enum('phoneNumber', 'link', 'address', 'calendarEvent', 'none', 'all') |

---

### defaultValue​

Provides an initial value that will change when the user starts typing. Useful for use-cases where you do not want to deal with listening to events and updating the value prop to keep the controlled state in sync.

| Type |
| --- |
| string |

---

### disableKeyboardShortcutsiOS​

If `true`, the keyboard shortcuts (undo/redo and copy buttons) are disabled.

| Type | Default |
| --- | --- |
| bool | false |

---

### cursorColorAndroid​

When provided it will set the color of the cursor (or "caret") in the component. Unlike the behavior of `selectionColor` the cursor color will be set independently from the color of the text selection box.

| Type |
| --- |
| color |

---

### disableFullscreenUIAndroid​

When `false`, if there is a small amount of space available around a text input (e.g. landscape orientation on a phone), the OS may choose to have the user edit the text inside of a full screen text input mode. When `true`, this feature is disabled and users will always edit the text directly inside of the text input. Defaults to `false`.

| Type |
| --- |
| bool |

---

### editable

If `false`, text is not editable. The default value is `true`.

| Type |
| --- |
| bool |

---

### enablesReturnKeyAutomaticallyiOS​

If `true`, the keyboard disables the return key when there is no text and automatically enables it when there is text. The default value is `false`.

| Type |
| --- |
| bool |

---

### enterKeyHint​

Determines what text should be shown to the return key. Has precedence over the `returnKeyType` prop.

The following values work across platforms:

- `done`
- `next`
- `search`
- `send`
- `go`

*Android Only*

The following values work on Android only:

- `previous`

*iOS Only*

The following values work on iOS only:

- `enter`

| Type |
| --- |
| enum('enter', 'done', 'next', 'previous', 'search', 'send', 'go') |

---

### importantForAutofillAndroid​

Tells the operating system whether the individual fields in your app should be included in a view structure for autofill purposes on Android API Level 26+. Possible values are `auto`, `no`, `noExcludeDescendants`, `yes`, and `yesExcludeDescendants`. The default value is `auto`.

- `auto`: Let the Android System use its heuristics to determine if the view is important for autofill.
- `no`: This view isn't important for autofill.
- `noExcludeDescendants`: This view and its children aren't important for autofill.
- `yes`: This view is important for autofill.
- `yesExcludeDescendants`: This view is important for autofill, but its children aren't important for autofill.

| Type |
| --- |
| enum('auto', 'no', 'noExcludeDescendants', 'yes', 'yesExcludeDescendants') |

---

### inlineImageLeftAndroid​

If defined, the provided image resource will be rendered on the left. The image resource must be inside `/android/app/src/main/res/drawable` and referenced like

```
<TextInput inlineImageLeft='search_icon'/>
```

| Type |
| --- |
| string |

---

### inlineImagePaddingAndroid​

Padding between the inline image, if any, and the text input itself.

| Type |
| --- |
| number |

---

### inputAccessoryViewIDiOS​

An optional identifier which links a custom [InputAccessoryView](https://reactnative.dev/docs/inputaccessoryview) to this text input. The InputAccessoryView is rendered above the keyboard when this text input is focused.

| Type |
| --- |
| string |

---

### inputAccessoryViewButtonLabeliOS​

An optional label that overrides the default [InputAccessoryView](https://reactnative.dev/docs/inputaccessoryview) button label.

By default, the default button label is not localized. Use this property to provide a localized version.

| Type |
| --- |
| string |

---

### inputMode​

Works like the `inputmode` attribute in HTML, it determines which keyboard to open, e.g. `numeric` and has precedence over `keyboardType`.

Support the following values:

- `none`
- `text`
- `decimal`
- `numeric`
- `tel`
- `search`
- `email`
- `url`

| Type |
| --- |
| enum('decimal', 'email', 'none', 'numeric', 'search', 'tel', 'text', 'url') |

---

### keyboardAppearanceiOS​

Determines the color of the keyboard.

| Type |
| --- |
| enum('default', 'light', 'dark') |

---

### keyboardType​

Determines which keyboard to open, e.g.`numeric`.

See screenshots of all the types [here](https://davidl.fr/blog/keyboard-react-native-ios-android#all-react-native-keyboard-type-examples-i-os-on-the-left-android-on-the-right).

The following values work across platforms:

- `default`
- `number-pad`
- `decimal-pad`
- `numeric`
- `email-address`
- `phone-pad`
- `url`

*iOS Only*

The following values work on iOS only:

- `ascii-capable`
- `numbers-and-punctuation`
- `name-phone-pad`
- `twitter`
- `web-search`

*Android Only*

The following values work on Android only:

- `visible-password`

| Type |
| --- |
| enum('default', 'email-address', 'numeric', 'phone-pad', 'ascii-capable', 'numbers-and-punctuation', 'url', 'number-pad', 'name-phone-pad', 'decimal-pad', 'twitter', 'web-search', 'visible-password') |

---

### lineBreakStrategyIOSiOS​

Set line break strategy on iOS 14+. Possible values are `none`, `standard`, `hangul-word` and `push-out`.

| Type | Default |
| --- | --- |
| enum('none','standard','hangul-word','push-out') | 'none' |

---

### lineBreakModeIOSiOS​

Set line break mode on iOS. Possible values are `wordWrapping`, `char`, `clip`, `head`, `middle` and `tail`.

| Type | Default |
| --- | --- |
| enum('wordWrapping','char','clip','head','middle','tail') | 'wordWrapping' |

---

### maxFontSizeMultiplier​

Specifies largest possible scale a font can reach when `allowFontScaling` is enabled. Possible values:

- `null/undefined` (default): inherit from the parent node or the global default (0)
- `0`: no max, ignore parent/global default
- `>= 1`: sets the `maxFontSizeMultiplier` of this node to this value

| Type |
| --- |
| number |

---

### maxLength​

Limits the maximum number of characters that can be entered. Use this instead of implementing the logic in JS to avoid flicker.

| Type |
| --- |
| number |

---

### multiline​

If `true`, the text input can be multiple lines. The default value is `false`.

 note

It is important to note that this aligns the text to the top on iOS, and centers it on Android. Use with `textAlignVertical` set to `top` for the same behavior in both platforms.

| Type |
| --- |
| bool |

---

### numberOfLines​

 note

`numberOfLines` on iOS is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Sets the maximum number of lines for a `TextInput`. Use it with multiline set to `true` to be able to fill the lines.

| Type |
| --- |
| number |

---

### onBlur​

Callback that is called when the text input is blurred.

 note

If you are attempting to access the `text` value from `nativeEvent` keep in mind that the resulting value you get can be `undefined` which can cause unintended errors. If you are trying to find the last value of TextInput, you can use the  event, which is fired upon completion of editing.

| Type |
| --- |
| ({nativeEvent:TargetEvent}) => void |

---

### onChange​

Callback that is called when the text input's text changes.

| Type |
| --- |
| ({nativeEvent: {eventCount, target, text}}) => void |

---

### onChangeText​

Callback that is called when the text input's text changes. Changed text is passed as a single string argument to the callback handler.

| Type |
| --- |
| function |

---

### onContentSizeChange​

Callback that is called when the text input's content size changes.

Only called for multiline text inputs.

| Type |
| --- |
| ({nativeEvent: {contentSize: {width, height} }}) => void |

---

### onEndEditing

Callback that is called when text input ends.

| Type |
| --- |
| function |

---

### onPressIn​

Callback that is called when a touch is engaged.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

---

### onPressOut​

Callback that is called when a touch is released.

| Type |
| --- |
| ({nativeEvent:PressEvent}) => void |

---

### onFocus​

Callback that is called when the text input is focused.

| Type |
| --- |
| ({nativeEvent:TargetEvent}) => void |

---

### onKeyPress​

Callback that is called when a key is pressed. This will be called with object where `keyValue` is `'Enter'` or `'Backspace'` for respective keys and the typed-in character otherwise including `' '` for space. Fires before `onChange` callbacks. Note: on Android only the inputs from soft keyboard are handled, not the hardware keyboard inputs.

| Type |
| --- |
| ({nativeEvent: {key: keyValue} }) => void |

---

### onLayout​

Invoked on mount and on layout changes.

| Type |
| --- |
| ({nativeEvent:LayoutEvent}) => void |

---

### onScroll​

Invoked on content scroll. May also contain other properties from `ScrollEvent` but on Android `contentSize` is not provided for performance reasons.

| Type |
| --- |
| ({nativeEvent: {contentOffset: {x, y} }}) => void |

---

### onSelectionChange​

Callback that is called when the text input selection is changed.

| Type |
| --- |
| ({nativeEvent: {selection: {start, end} }}) => void |

---

### onSubmitEditing

Callback that is called when the text input's submit button is pressed.

| Type |
| --- |
| ({nativeEvent: {text, eventCount, target}}) => void |

Note that on iOS this method isn't called when using `keyboardType="phone-pad"`.

---

### placeholder​

The string that will be rendered before text input has been entered.

| Type |
| --- |
| string |

---

### placeholderTextColor​

The text color of the placeholder string.

| Type |
| --- |
| color |

---

### readOnly​

If `true`, text is not editable. The default value is `false`.

| Type |
| --- |
| bool |

---

### returnKeyLabelAndroid​

Sets the return key to the label. Use it instead of `returnKeyType`.

| Type |
| --- |
| string |

---

### returnKeyType​

Determines how the return key should look. On Android you can also use `returnKeyLabel`.

*Cross platform*

The following values work across platforms:

- `done`
- `go`
- `next`
- `search`
- `send`

*Android Only*

The following values work on Android only:

- `none`
- `previous`

*iOS Only*

The following values work on iOS only:

- `default`
- `emergency-call`
- `google`
- `join`
- `route`
- `yahoo`

| Type |
| --- |
| enum('done', 'go', 'next', 'search', 'send', 'none', 'previous', 'default', 'emergency-call', 'google', 'join', 'route', 'yahoo') |

### rejectResponderTerminationiOS​

If `true`, allows TextInput to pass touch events to the parent component. This allows components such as SwipeableListView to be swipeable from the TextInput on iOS, as is the case on Android by default. If `false`, TextInput always asks to handle the input (except when disabled). The default value is `true`.

| Type |
| --- |
| bool |

---

### rowsAndroid​

Sets the number of lines for a `TextInput`. Use it with multiline set to `true` to be able to fill the lines.

| Type |
| --- |
| number |

---

### scrollEnablediOS​

If `false`, scrolling of the text view will be disabled. The default value is `true`. Only works with `multiline={true}`.

| Type |
| --- |
| bool |

---

### secureTextEntry​

If `true`, the text input obscures the text entered so that sensitive text like passwords stay secure. The default value is `false`. Does not work with `multiline={true}`.

| Type |
| --- |
| bool |

---

### selection​

The start and end of the text input's selection. Set start and end to the same value to position the cursor.

| Type |
| --- |
| object:{start: number,end: number} |

---

### selectionColor​

The highlight, selection handle and cursor color of the text input.

| Type |
| --- |
| color |

---

### selectionHandleColorAndroid​

Sets the color of the selection handle. Unlike `selectionColor`, it allows the selection handle color to be customized independently of the selection's color.

| Type |
| --- |
| color |

---

### selectTextOnFocus​

If `true`, all text will automatically be selected on focus.

| Type |
| --- |
| bool |

---

### showSoftInputOnFocus​

When `false`, it will prevent the soft keyboard from showing when the field is focused. The default value is `true`.

| Type |
| --- |
| bool |

---

### smartInsertDeleteiOS​

If `false`, the iOS system will not insert an extra space after a paste operation neither delete one or two spaces after a cut or delete operation.

| Type | Default |
| --- | --- |
| bool | true |

---

### spellCheckiOS​

If `false`, disables spell-check style (i.e. red underlines). The default value is inherited from `autoCorrect`.

| Type |
| --- |
| bool |

---

### submitBehavior​

When the return key is pressed,

For single line inputs:

- `'newline'` defaults to `'blurAndSubmit'`
- `undefined` defaults to `'blurAndSubmit'`

For multiline inputs:

- `'newline'` adds a newline
- `undefined` defaults to `'newline'`

For both single line and multiline inputs:

- `'submit'` will only send a submit event and not blur the input
- `'blurAndSubmit`' will both blur the input and send a submit event

| Type |
| --- |
| enum('submit', 'blurAndSubmit', 'newline') |

---

### textAlign​

Align the input text to the left, center, or right sides of the input field.

Possible values for `textAlign` are:

- `left`
- `center`
- `right`

| Type |
| --- |
| enum('left', 'center', 'right') |

---

### textContentTypeiOS​

Give the keyboard and the system information about the expected semantic meaning for the content that users enter.

 note

[autoComplete](#autocomplete), provides the same functionality and is available for all platforms. You can use [Platform.select](https://reactnative.dev/docs/next/platform#select) for differing platform behaviors.

Avoid using both `textContentType` and `autoComplete`. For backwards compatibility, `textContentType` takes precedence when both properties are set.

You can set `textContentType` to `username` or `password` to enable autofill of login details from the device keychain.

`newPassword` can be used to indicate a new password input the user may want to save in the keychain, and `oneTimeCode` can be used to indicate that a field can be autofilled by a code arriving in an SMS.

To disable autofill, set `textContentType` to `none`.

Possible values for `textContentType` are:

- `none`
- `addressCity`
- `addressCityAndState`
- `addressState`
- `birthdate` (iOS 17+)
- `birthdateDay` (iOS 17+)
- `birthdateMonth` (iOS 17+)
- `birthdateYear` (iOS 17+)
- `countryName`
- `creditCardExpiration` (iOS 17+)
- `creditCardExpirationMonth` (iOS 17+)
- `creditCardExpirationYear` (iOS 17+)
- `creditCardFamilyName` (iOS 17+)
- `creditCardGivenName` (iOS 17+)
- `creditCardMiddleName` (iOS 17+)
- `creditCardName` (iOS 17+)
- `creditCardNumber`
- `creditCardSecurityCode` (iOS 17+)
- `creditCardType` (iOS 17+)
- `emailAddress`
- `familyName`
- `fullStreetAddress`
- `givenName`
- `jobTitle`
- `location`
- `middleName`
- `name`
- `namePrefix`
- `nameSuffix`
- `newPassword`
- `nickname`
- `oneTimeCode`
- `organizationName`
- `password`
- `postalCode`
- `streetAddressLine1`
- `streetAddressLine2`
- `sublocality`
- `telephoneNumber`
- `URL`
- `username`

| Type |
| --- |
| enum('none', 'addressCity', 'addressCityAndState', 'addressState', 'birthdate', 'birthdateDay', 'birthdateMonth', 'birthdateYear', 'countryName', 'creditCardExpiration', 'creditCardExpirationMonth', 'creditCardExpirationYear', 'creditCardFamilyName', 'creditCardGivenName', 'creditCardMiddleName', 'creditCardName', 'creditCardNumber', 'creditCardSecurityCode', 'creditCardType', 'emailAddress', 'familyName', 'fullStreetAddress', 'givenName', 'jobTitle', 'location', 'middleName', 'name', 'namePrefix', 'nameSuffix', 'newPassword', 'nickname', 'oneTimeCode', 'organizationName', 'password', 'postalCode', 'streetAddressLine1', 'streetAddressLine2', 'sublocality', 'telephoneNumber', 'URL', 'username') |

---

### passwordRulesiOS​

When using `textContentType` as `newPassword` on iOS we can let the OS know the minimum requirements of the password so that it can generate one that will satisfy them. In order to create a valid string for `PasswordRules` take a look to the [Apple Docs](https://developer.apple.com/password-rules/).

 tip

If passwords generation dialog doesn't appear please make sure that:

- AutoFill is enabled: **Settings** → **Passwords & Accounts** → toggle "On" the **AutoFill Passwords**,
- iCloud Keychain is used: **Settings** → **Apple ID** → **iCloud** → **Keychain** → toggle "On" the **iCloud Keychain**.

| Type |
| --- |
| string |

---

### style​

Note that not all Text styles are supported, an incomplete list of what is not supported includes:

- `borderLeftWidth`
- `borderTopWidth`
- `borderRightWidth`
- `borderBottomWidth`
- `borderTopLeftRadius`
- `borderTopRightRadius`
- `borderBottomRightRadius`
- `borderBottomLeftRadius`

[Styles](https://reactnative.dev/docs/style)

| Type |
| --- |
| Text |

---

### textBreakStrategyAndroid​

Set text break strategy on Android API Level 23+, possible values are `simple`, `highQuality`, `balanced` The default value is `highQuality`.

| Type |
| --- |
| enum('simple', 'highQuality', 'balanced') |

---

### underlineColorAndroidAndroid​

The color of the `TextInput` underline.

| Type |
| --- |
| color |

---

### value​

The value to show for the text input. `TextInput` is a controlled component, which means the native value will be forced to match this value prop if provided. For most uses, this works great, but in some cases this may cause flickering - one common cause is preventing edits by keeping value the same. In addition to setting the same value, either set `editable={false}`, or set/update `maxLength` to prevent unwanted edits without flicker.

| Type |
| --- |
| string |

## Methods​

### .focus()​

 tsx

```
focus();
```

Makes the native input request focus.

### .blur()​

 tsx

```
blur();
```

Makes the native input lose focus.

### clear()​

 tsx

```
clear();
```

Removes all text from the `TextInput`.

---

### isFocused()​

 tsx

```
isFocused(): boolean;
```

Returns `true` if the input is currently focused; `false` otherwise.

# Known issues

- [react-native#19096](https://github.com/facebook/react-native/issues/19096): Doesn't support Android's `onKeyPreIme`.
- [react-native#19366](https://github.com/facebook/react-native/issues/19366): Calling .focus() after closing Android's keyboard via back button doesn't bring keyboard up again.
- [react-native#26799](https://github.com/facebook/react-native/issues/26799): Doesn't support Android's `secureTextEntry` when `keyboardType="email-address"` or `keyboardType="phone-pad"`.

Is this page useful?

---

# Timers

> Timers are an important part of an application and React Native implements the browser timers.

Timers are an important part of an application and React Native implements the [browser timers](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Timeouts_and_intervals).

## Timers​

- `setTimeout` and `clearTimeout`
- `setInterval` and `clearInterval`
- `setImmediate` and `clearImmediate`
- `requestAnimationFrame` and `cancelAnimationFrame`

`requestAnimationFrame(fn)` is not the same as `setTimeout(fn, 0)` - the former will fire after all the frames have flushed, whereas the latter will fire as quickly as possible (over 1000x per second on a iPhone 5S).

`setImmediate` is executed at the end of the current JavaScript execution block, right before sending the batched response back to native. Note that if you call `setImmediate` within a `setImmediate` callback, it will be executed right away, it won't yield back to native in between.

The `Promise` implementation uses `setImmediate` as its asynchronicity implementation.

 note

When debugging on Android, if the times between the debugger and device have drifted; things such as animation, event behavior, etc., might not work properly or the results may not be accurate.
Please correct this by running `adb shell "date `date +%m%d%H%M%Y.%S%3N`"` on your debugger machine. Root access is required for the use in real device.

## InteractionManager​

 Deprecated

The `InteractionManager` behavior has been changed to be the same as `setImmediate`, which should be used instead.

One reason why well-built native apps feel so smooth is by avoiding expensive operations during interactions and animations. In React Native, we currently have a limitation that there is only a single JS execution thread, but you can use `InteractionManager` to make sure long-running work is scheduled to start after any interactions/animations have completed.

Applications can schedule tasks to run after interactions with the following:

 tsx

```
InteractionManager.runAfterInteractions(() => {  // ...long-running synchronous task...});
```

Compare this to other scheduling alternatives:

- requestAnimationFrame(): for code that animates a view over time.
- setImmediate/setTimeout/setInterval(): run code later, note this may delay animations.
- runAfterInteractions(): run code later, without delaying active animations.

The touch handling system considers one or more active touches to be an 'interaction' and will delay `runAfterInteractions()` callbacks until all touches have ended or been cancelled.

`InteractionManager` also allows applications to register animations by creating an interaction 'handle' on animation start, and clearing it upon completion:

 tsx

```
const handle = InteractionManager.createInteractionHandle();// run animation... (`runAfterInteractions` tasks are queued)// later, on animation completion:InteractionManager.clearInteractionHandle(handle);// queued tasks run if all handles were cleared
```

Is this page useful?

---

# ToastAndroid

> React Native's ToastAndroid API exposes the Android platform's ToastAndroid module as a JS module. It provides the method show(message, duration) which takes the following parameters:

React Native's ToastAndroid API exposes the Android platform's ToastAndroid module as a JS module. It provides the method `show(message, duration)` which takes the following parameters:

- *message* A string with the text to toast
- *duration* The duration of the toast—either `ToastAndroid.SHORT` or `ToastAndroid.LONG`

You can alternatively use `showWithGravity(message, duration, gravity)` to specify where the toast appears in the screen's layout. May be `ToastAndroid.TOP`, `ToastAndroid.BOTTOM` or `ToastAndroid.CENTER`.

The `showWithGravityAndOffset(message, duration, gravity, xOffset, yOffset)` method adds the ability to specify an offset with in pixels.

 note

Starting with Android 11 (API level 30), setting the gravity has no effect on text toasts. Read about the changes [here](https://developer.android.com/about/versions/11/behavior-changes-11#text-toast-api-changes).

---

# Reference

## Methods​

### show()​

 tsx

```
static show(message: string, duration: number);
```

---

### showWithGravity()​

This property will only work on Android API 29 and below. For similar functionality on higher Android APIs, consider using snackbar or notification.

 tsx

```
static showWithGravity(message: string, duration: number, gravity: number);
```

---

### showWithGravityAndOffset()​

This property will only work on Android API 29 and below. For similar functionality on higher Android APIs, consider using snackbar or notification.

 tsx

```
static showWithGravityAndOffset(  message: string,  duration: number,  gravity: number,  xOffset: number,  yOffset: number,);
```

## Properties​

### SHORT​

Indicates the duration on the screen.

 tsx

```
static SHORT: number;
```

---

### LONG​

Indicates the duration on the screen.

 tsx

```
static LONG: number;
```

---

### TOP​

Indicates the position on the screen.

 tsx

```
static TOP: number;
```

---

### BOTTOM​

Indicates the position on the screen.

 tsx

```
static BOTTOM: number;
```

---

### CENTER​

Indicates the position on the screen.

 tsx

```
static CENTER: number;
```

Is this page useful?

---

# TouchableHighlight

> If you're looking for a more extensive and future-proof way to handle touch-based input, check out the Pressable API.

tip

If you're looking for a more extensive and future-proof way to handle touch-based input, check out the [Pressable](https://reactnative.dev/docs/pressable) API.

A wrapper for making views respond properly to touches. On press down, the opacity of the wrapped view is decreased, which allows the underlay color to show through, darkening or tinting the view.

The underlay comes from wrapping the child in a new View, which can affect layout, and sometimes cause unwanted visual artifacts if not used correctly, for example if the backgroundColor of the wrapped view isn't explicitly set to an opaque color.

TouchableHighlight must have one child (not zero or more than one). If you wish to have several child components, wrap them in a View.

 tsx

```
function MyComponent(props: MyComponentProps) {  return (    <View {...props} style={{flex: 1, backgroundColor: '#fff'}}>      <Text>My Component</Text>    </View>  );}<TouchableHighlight  activeOpacity={0.6}  underlayColor="#DDDDDD"  onPress={() => alert('Pressed!')}>  <MyComponent /></TouchableHighlight>;
```

## Example​

---

# Reference

## Props​

### TouchableWithoutFeedback Props​

Inherits [TouchableWithoutFeedback Props](https://reactnative.dev/docs/touchablewithoutfeedback#props).

---

### activeOpacity​

Determines what the opacity of the wrapped view should be when touch is active. The value should be between 0 and 1. Defaults to 0.85. Requires `underlayColor` to be set.

| Type |
| --- |
| number |

---

### onHideUnderlay​

Called immediately after the underlay is hidden.

| Type |
| --- |
| function |

---

### onShowUnderlay​

Called immediately after the underlay is shown.

| Type |
| --- |
| function |

---

### ref​

A ref setter that will be assigned an [element node](https://reactnative.dev/docs/element-nodes) when mounted.

---

### style​

| Type |
| --- |
| View.style |

---

### underlayColor​

The color of the underlay that will show through when the touch is active.

| Type |
| --- |
| color |

---

### hasTVPreferredFocusiOS​

*(Apple TV only)* TV preferred focus (see documentation for the View component).

| Type |
| --- |
| bool |

---

### nextFocusDownAndroid​

TV next focus down (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusForwardAndroid​

TV next focus forward (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusLeftAndroid​

TV next focus left (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusRightAndroid​

TV next focus right (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusUpAndroid​

TV next focus up (see documentation for the View component).

| Type |
| --- |
| number |

---

### testOnly_pressed​

Handy for snapshot tests.

| Type |
| --- |
| bool |

Is this page useful?

---

# TouchableNativeFeedback

> If you're looking for a more extensive and future-proof way to handle touch-based input, check out the Pressable API.

tip

If you're looking for a more extensive and future-proof way to handle touch-based input, check out the [Pressable](https://reactnative.dev/docs/pressable) API.

A wrapper for making views respond properly to touches (Android only). On Android this component uses native state drawable to display touch feedback.

At the moment it only supports having a single View instance as a child node, as it's implemented by replacing that View with another instance of RCTView node with some additional properties set.

Background drawable of native feedback touchable can be customized with `background` property.

## Example​

---

# Reference

## Props​

### TouchableWithoutFeedback Props​

Inherits [TouchableWithoutFeedback Props](https://reactnative.dev/docs/touchablewithoutfeedback#props).

---

### background​

Determines the type of background drawable that's going to be used to display feedback. It takes an object with `type` property and extra data depending on the `type`. It's recommended to use one of the static methods to generate that dictionary.

| Type |
| --- |
| backgroundPropType |

---

### useForeground​

Set to true to add the ripple effect to the foreground of the view, instead of the background. This is useful if one of your child views has a background of its own, or you're e.g. displaying images, and you don't want the ripple to be covered by them.

Check TouchableNativeFeedback.canUseNativeForeground() first, as this is only available on Android 6.0 and above. If you try to use this on older versions you will get a warning and fallback to background.

| Type |
| --- |
| bool |

---

### hasTVPreferredFocusAndroid​

TV preferred focus (see documentation for the View component).

| Type |
| --- |
| bool |

---

### nextFocusDownAndroid​

TV next focus down (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusForwardAndroid​

TV next focus forward (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusLeftAndroid​

TV next focus left (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusRightAndroid​

TV next focus right (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusUpAndroid​

TV next focus up (see documentation for the View component).

| Type |
| --- |
| number |

## Methods​

### SelectableBackground()​

 tsx

```
static SelectableBackground(  rippleRadius: number | null,): ThemeAttributeBackgroundPropType;
```

Creates an object that represents android theme's default background for selectable elements (`?android:attr/selectableItemBackground`). `rippleRadius` parameter controls the radius of the ripple effect.

---

### SelectableBackgroundBorderless()​

 tsx

```
static SelectableBackgroundBorderless(  rippleRadius: number | null,): ThemeAttributeBackgroundPropType;
```

Creates an object that represent android theme's default background for borderless selectable elements (`?android:attr/selectableItemBackgroundBorderless`). Available on android API level 21+. `rippleRadius` parameter controls the radius of the ripple effect.

---

### Ripple()​

 tsx

```
static Ripple(  color: ColorValue,  borderless: boolean,  rippleRadius?: number | null,): RippleBackgroundPropType;
```

Creates an object that represents ripple drawable with specified color (as a string). If property `borderless` evaluates to true the ripple will render outside of the view bounds (see native actionbar buttons as an example of that behavior). This background type is available on Android API level 21+.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| color | string | Yes | The ripple color |
| borderless | boolean | Yes | If the ripple can render outside its bounds |
| rippleRadius | ?number | No | controls the radius of the ripple effect |

---

### canUseNativeForeground()​

 tsx

```
static canUseNativeForeground(): boolean;
```

Is this page useful?

---

# TouchableOpacity

> If you're looking for a more extensive and future-proof way to handle touch-based input, check out the Pressable API.

tip

If you're looking for a more extensive and future-proof way to handle touch-based input, check out the [Pressable](https://reactnative.dev/docs/pressable) API.

A wrapper for making views respond properly to touches. On press down, the opacity of the wrapped view is decreased, dimming it.

Opacity is controlled by wrapping the children in an `Animated.View`, which is added to the view hierarchy. Be aware that this can affect layout.

## Example​

---

# Reference

## Props​

### TouchableWithoutFeedback Props​

Inherits [TouchableWithoutFeedback Props](https://reactnative.dev/docs/touchablewithoutfeedback#props).

---

### style​

| Type |
| --- |
| View.style |

---

### activeOpacity​

Determines what the opacity of the wrapped view should be when touch is active. Defaults to `0.2`.

| Type |
| --- |
| number |

---

### hasTVPreferredFocusiOS​

*(Apple TV only)* TV preferred focus (see documentation for the View component).

| Type |
| --- |
| bool |

---

### nextFocusDownAndroid​

TV next focus down (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusForwardAndroid​

TV next focus forward (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusLeftAndroid​

TV next focus left (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusRightAndroid​

TV next focus right (see documentation for the View component).

| Type |
| --- |
| number |

---

### nextFocusUpAndroid​

TV next focus up (see documentation for the View component).

| Type |
| --- |
| number |

---

### ref​

A ref setter that will be assigned an [element node](https://reactnative.dev/docs/element-nodes) when mounted.

Is this page useful?
