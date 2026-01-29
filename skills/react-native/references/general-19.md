# ScrollView and more

# ScrollView

> Component that wraps platform ScrollView while providing integration with touch locking "responder" system.

Component that wraps platform ScrollView while providing integration with touch locking "responder" system.

Keep in mind that ScrollViews must have a bounded height in order to work, since they contain unbounded-height children into a bounded container (via a scroll interaction). In order to bound the height of a ScrollView, either set the height of the view directly (discouraged) or make sure all parent views have bounded height. Forgetting to transfer `{flex: 1}` down the view stack can lead to errors here, which the element inspector makes quick to debug.

Doesn't yet support other contained responders from blocking this scroll view from becoming the responder.

`<ScrollView>` vs [<FlatList>](https://reactnative.dev/docs/flatlist) - which one to use?

`ScrollView` renders all its react child components at once, but this has a performance downside.

Imagine you have a very long list of items you want to display, maybe several screens worth of content. Creating JS components and native views for everything all at once, much of which may not even be shown, will contribute to slow rendering and increased memory usage.

This is where `FlatList` comes into play. `FlatList` renders items lazily, when they are about to appear, and removes items that scroll way off screen to save memory and processing time.

`FlatList` is also handy if you want to render separators between your items, multiple columns, infinite scroll loading, or any number of other features it supports out of the box.

## Example​

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### StickyHeaderComponent​

A React Component that will be used to render sticky headers, should be used together with `stickyHeaderIndices`. You may need to set this component if your sticky header uses custom transforms, for example, when you want your list to have an animated and hidable header. If a component has not been provided, the default [ScrollViewStickyHeader](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/Components/ScrollView/ScrollViewStickyHeader.js) component will be used.

| Type |
| --- |
| component, element |

---

### alwaysBounceHorizontaliOS​

When true, the scroll view bounces horizontally when it reaches the end even if the content is smaller than the scroll view itself.

| Type | Default |
| --- | --- |
| bool | truewhenhorizontal={true}falseotherwise |

---

### alwaysBounceVerticaliOS​

When true, the scroll view bounces vertically when it reaches the end even if the content is smaller than the scroll view itself.

| Type | Default |
| --- | --- |
| bool | falsewhenhorizontal={true}trueotherwise |

---

### automaticallyAdjustContentInsetsiOS​

Controls whether iOS should automatically adjust the content inset for scroll views that are placed behind a navigation bar or tab bar/toolbar.

| Type | Default |
| --- | --- |
| bool | true |

---

### automaticallyAdjustKeyboardInsetsiOS​

Controls whether the ScrollView should automatically adjust its `contentInset` and `scrollViewInsets` when the Keyboard changes its size.

| Type | Default |
| --- | --- |
| bool | false |

---

### automaticallyAdjustsScrollIndicatorInsetsiOS​

Controls whether iOS should automatically adjust the scroll indicator insets. See Apple's [documentation on the property](https://developer.apple.com/documentation/uikit/uiscrollview/3198043-automaticallyadjustsscrollindica).

| Type | Default |
| --- | --- |
| bool | true |

---

### bouncesiOS​

When true, the scroll view bounces when it reaches the end of the content if the content is larger than the scroll view along the axis of the scroll direction. When `false`, it disables all bouncing even if the `alwaysBounce*` props are `true`.

| Type | Default |
| --- | --- |
| bool | true |

---

### bouncesZoomiOS​

When `true`, gestures can drive zoom past min/max and the zoom will animate to the min/max value at gesture end, otherwise the zoom will not exceed the limits.

| Type | Default |
| --- | --- |
| bool | true |

---

### canCancelContentTouchesiOS​

When `false`, once tracking starts, won't try to drag if the touch moves.

| Type | Default |
| --- | --- |
| bool | true |

---

### centerContentiOS​

When `true`, the scroll view automatically centers the content when the content is smaller than the scroll view bounds; when the content is larger than the scroll view, this property has no effect.

| Type | Default |
| --- | --- |
| bool | false |

---

### contentContainerStyle​

These styles will be applied to the scroll view content container which wraps all of the child views. Example:

```
return (  <ScrollView contentContainerStyle={styles.contentContainer}>  </ScrollView>);...const styles = StyleSheet.create({  contentContainer: {    paddingVertical: 20  }});
```

| Type |
| --- |
| View Style |

---

### contentInsetiOS​

The amount by which the scroll view content is inset from the edges of the scroll view.

| Type | Default |
| --- | --- |
| object:{top: number, left: number, bottom: number, right: number} | {top: 0, left: 0, bottom: 0, right: 0} |

---

### contentInsetAdjustmentBehavioriOS​

This property specifies how the safe area insets are used to modify the content area of the scroll view. Available on iOS 11 and later.

| Type | Default |
| --- | --- |
| enum('automatic','scrollableAxes','never','always') | 'never' |

---

### contentOffset​

Used to manually set the starting scroll offset.

| Type | Default |
| --- | --- |
| Point | {x: 0, y: 0} |

---

### decelerationRate​

A floating-point number that determines how quickly the scroll view decelerates after the user lifts their finger. You may also use string shortcuts `"normal"` and `"fast"` which match the underlying iOS settings for `UIScrollViewDecelerationRateNormal` and `UIScrollViewDecelerationRateFast` respectively.

- `'normal'` 0.998 on iOS, 0.985 on Android.
- `'fast'`, 0.99 on iOS, 0.9 on Android.

| Type | Default |
| --- | --- |
| enum('fast','normal'), number | 'normal' |

---

### directionalLockEnablediOS​

When true, the ScrollView will try to lock to only vertical or horizontal scrolling while dragging.

| Type | Default |
| --- | --- |
| bool | false |

---

### disableIntervalMomentum​

When true, the scroll view stops on the next index (in relation to scroll position at release) regardless of how fast the gesture is. This can be used for pagination when the page is less than the width of the horizontal ScrollView or the height of the vertical ScrollView.

| Type | Default |
| --- | --- |
| bool | false |

---

### disableScrollViewPanResponder​

When true, the default JS pan responder on the ScrollView is disabled, and full control over touches inside the ScrollView is left to its child components. This is particularly useful if `snapToInterval` is enabled, since it does not follow typical touch patterns. Do not use this on regular ScrollView use cases without `snapToInterval` as it may cause unexpected touches to occur while scrolling.

| Type | Default |
| --- | --- |
| bool | false |

---

### endFillColorAndroid​

Sometimes a scrollview takes up more space than its content fills. When this is the case, this prop will fill the rest of the scrollview with a color to avoid setting a background and creating unnecessary overdraw. This is an advanced optimization that is not needed in the general case.

| Type |
| --- |
| color |

---

### fadingEdgeLengthAndroid​

Fades out the edges of the scroll content.

If the value is greater than `0`, the fading edges will be set accordingly to the current scroll direction and position, indicating if there is more content to show.

| Type | Default |
| --- | --- |
| numberobject:{start: number, end: number} | 0 |

---

### horizontal​

When `true`, the scroll view's children are arranged horizontally in a row instead of vertically in a column.

| Type | Default |
| --- | --- |
| bool | false |

---

### indicatorStyleiOS​

The style of the scroll indicators.

- `'default'` same as `black`.
- `'black'`, scroll indicator is `black`. This style is good against a light background.
- `'white'`, scroll indicator is `white`. This style is good against a dark background.

| Type | Default |
| --- | --- |
| enum('default','black','white') | 'default' |

---

### invertStickyHeaders​

If sticky headers should stick at the bottom instead of the top of the ScrollView. This is usually used with inverted ScrollViews.

| Type | Default |
| --- | --- |
| bool | false |

---

### keyboardDismissMode​

Determines whether the keyboard gets dismissed in response to a drag.

- `'none'`, drags do not dismiss the keyboard.
- `'on-drag'`, the keyboard is dismissed when a drag begins.

**iOS Only**

- `'interactive'`, the keyboard is dismissed interactively with the drag and moves in synchrony with the touch, dragging upwards cancels the dismissal. On Android this is not supported and it will have the same behavior as `'none'`.

| Type | Default |
| --- | --- |
| enum('none','on-drag')Androidenum('none','on-drag','interactive')iOS | 'none' |

---

### keyboardShouldPersistTaps​

Determines when the keyboard should stay visible after a tap.

- `'never'` tapping outside of the focused text input when the keyboard is up dismisses the keyboard. When this happens, children won't receive the tap.
- `'always'`, the keyboard will not dismiss automatically, and the scroll view will not catch taps, but children of the scroll view can catch taps.
- `'handled'`, the keyboard will not dismiss automatically when the tap was handled by children of the scroll view (or captured by an ancestor).
- `false`, **deprecated**, use `'never'` instead
- `true`, **deprecated**, use `'always'` instead

| Type | Default |
| --- | --- |
| enum('always','never','handled',false,true) | 'never' |

---

### maintainVisibleContentPosition​

When set, the scroll view will adjust the scroll position so that the first child that is currently visible and at or beyond `minIndexForVisible` will not change position. This is useful for lists that are loading content in both directions, e.g. a chat thread, where new messages coming in might otherwise cause the scroll position to jump. A value of 0 is common, but other values such as 1 can be used to skip loading spinners or other content that should not maintain position.

The optional `autoscrollToTopThreshold` can be used to make the content automatically scroll to the top after making the adjustment if the user was within the threshold of the top before the adjustment was made. This is also useful for chat-like applications where you want to see new messages scroll into place, but not if the user has scrolled up a ways and it would be disruptive to scroll a bunch.

Caveat 1: Reordering elements in the scrollview with this enabled will probably cause jumpiness and jank. It can be fixed, but there are currently no plans to do so. For now, don't re-order the content of any ScrollViews or Lists that use this feature.

Caveat 2: This uses `contentOffset` and `frame.origin` in native code to compute visibility. Occlusion, transforms, and other complexity won't be taken into account as to whether content is "visible" or not.

| Type |
| --- |
| object:{minIndexForVisible: number, autoscrollToTopThreshold: number} |

---

### maximumZoomScaleiOS​

The maximum allowed zoom scale.

| Type | Default |
| --- | --- |
| number | 1.0 |

---

### minimumZoomScaleiOS​

The minimum allowed zoom scale.

| Type | Default |
| --- | --- |
| number | 1.0 |

---

### nestedScrollEnabledAndroid​

Enables nested scrolling for Android API level 21+.

| Type | Default |
| --- | --- |
| bool | false |

---

### onContentSizeChange​

Called when scrollable content view of the ScrollView changes.

The handler function will receive two parameters: the content width and content height `(contentWidth, contentHeight)`.

It's implemented using onLayout handler attached to the content container which this ScrollView renders.

| Type |
| --- |
| function |

---

### onMomentumScrollBegin​

Called when the momentum scroll starts (scroll which occurs as the ScrollView starts gliding).

| Type |
| --- |
| function |

---

### onMomentumScrollEnd​

Called when the momentum scroll ends (scroll which occurs as the ScrollView glides to a stop).

| Type |
| --- |
| function |

---

### onScroll​

Fires at most once per frame during scrolling. The event has the following shape (all values with unspecified type are numbers):

 js

```
{  nativeEvent: {    contentInset: {bottom, left, right, top},    contentOffset: {x, y},    contentSize: {height, width},    layoutMeasurement: {height, width},    velocity: {x, y},    responderIgnoreScroll: boolean,    zoomScale,    // iOS only    targetContentOffset: {x, y}  }}
```

| Type |
| --- |
| function |

---

### onScrollBeginDrag​

Called when the user begins to drag the scroll view.

| Type |
| --- |
| function |

---

### onScrollEndDrag​

Called when the user stops dragging the scroll view and it either stops or begins to glide.

| Type |
| --- |
| function |

---

### onScrollToTopiOS​

Fires when the scroll view scrolls to top after the status bar has been tapped.

| Type |
| --- |
| function |

---

### overScrollModeAndroid​

Used to override default value of overScroll mode.

Possible values:

- `'auto'` - Allow a user to over-scroll this view only if the content is large enough to meaningfully scroll.
- `'always'` - Always allow a user to over-scroll this view.
- `'never'` - Never allow a user to over-scroll this view.

| Type | Default |
| --- | --- |
| enum('auto','always','never') | 'auto' |

---

### pagingEnabled​

When true, the scroll view stops on multiples of the scroll view's size when scrolling. This can be used for horizontal pagination.

| Type | Default |
| --- | --- |
| bool | false |

---

### persistentScrollbarAndroid​

Causes the scrollbars not to turn transparent when they are not in use.

| Type | Default |
| --- | --- |
| bool | false |

---

### pinchGestureEnablediOS​

When true, ScrollView allows use of pinch gestures to zoom in and out.

| Type | Default |
| --- | --- |
| bool | true |

---

### refreshControl​

A RefreshControl component, used to provide pull-to-refresh functionality for the ScrollView. Only works for vertical ScrollViews (`horizontal` prop must be `false`).

See [RefreshControl](https://reactnative.dev/docs/refreshcontrol).

| Type |
| --- |
| element |

---

### removeClippedSubviews​

 warning

Using this property may lead to bugs (missing content) in some circumstances - use at your own risk.

When `true`, offscreen child views are removed from their native backing superview when offscreen. This may improve scroll performance for large lists. On Android the default value is `true`.

| Type |
| --- |
| boolean |

---

### scrollEnabled​

When false, the view cannot be scrolled via touch interaction.

Note that the view can always be scrolled by calling `scrollTo`.

| Type | Default |
| --- | --- |
| bool | true |

---

### scrollEventThrottle​

Limits how often scroll events will be fired while scrolling, specified as a time interval in ms. This may be useful when expensive work is performed in response to scrolling. Values ≤ `16` will disable throttling, regardless of the refresh rate of the device.

| Type | Default |
| --- | --- |
| number | 0 |

---

### scrollIndicatorInsetsiOS​

The amount by which the scroll view indicators are inset from the edges of the scroll view. This should normally be set to the same value as the `contentInset`.

| Type | Default |
| --- | --- |
| object:{top: number, left: number, bottom: number, right: number} | {top: 0, left: 0, bottom: 0, right: 0} |

---

### scrollPerfTagAndroid​

Tag used to log scroll performance on this scroll view. Will force momentum events to be turned on (see sendMomentumEvents). This doesn't do anything out of the box and you need to implement a custom native FpsListener for it to be useful.

| Type |
| --- |
| string |

---

### scrollToOverflowEnablediOS​

When `true`, the scroll view can be programmatically scrolled beyond its content size.

| Type | Default |
| --- | --- |
| bool | false |

---

### scrollsToTopiOS​

When `true`, the scroll view scrolls to top when the status bar is tapped.

| Type | Default |
| --- | --- |
| bool | true |

---

### showsHorizontalScrollIndicator​

When `true`, shows a horizontal scroll indicator.

| Type | Default |
| --- | --- |
| bool | true |

---

### showsVerticalScrollIndicator​

When `true`, shows a vertical scroll indicator.

| Type | Default |
| --- | --- |
| bool | true |

---

### snapToAlignment​

When `snapToInterval` is set, `snapToAlignment` will define the relationship of the snapping to the scroll view.

Possible values:

- `'start'` will align the snap at the left (horizontal) or top (vertical).
- `'center'` will align the snap in the center.
- `'end'` will align the snap at the right (horizontal) or bottom (vertical).

| Type | Default |
| --- | --- |
| enum('start','center','end') | 'start' |

---

### snapToEnd​

Use in conjunction with `snapToOffsets`. By default, the end of the list counts as a snap offset. Set `snapToEnd` to false to disable this behavior and allow the list to scroll freely between its end and the last `snapToOffsets` offset.

| Type | Default |
| --- | --- |
| bool | true |

---

### snapToInterval​

When set, causes the scroll view to stop at multiples of the value of `snapToInterval`. This can be used for paginating through children that have lengths smaller than the scroll view. Typically used in combination with `snapToAlignment` and `decelerationRate="fast"`. Overrides less configurable `pagingEnabled` prop.

| Type |
| --- |
| number |

---

### snapToOffsets​

When set, causes the scroll view to stop at the defined offsets. This can be used for paginating through variously sized children that have lengths smaller than the scroll view. Typically used in combination with `decelerationRate="fast"`. Overrides less configurable `pagingEnabled` and `snapToInterval` props.

| Type |
| --- |
| array of number |

---

### snapToStart​

Use in conjunction with `snapToOffsets`. By default, the beginning of the list counts as a snap offset. Set `snapToStart` to `false` to disable this behavior and allow the list to scroll freely between its start and the first `snapToOffsets` offset.

| Type | Default |
| --- | --- |
| bool | true |

---

### stickyHeaderHiddenOnScroll​

When set to `true`, sticky header will be hidden when scrolling down the list, and it will dock at the top of the list when scrolling up.

| Type | Default |
| --- | --- |
| bool | false |

---

### stickyHeaderIndices​

An array of child indices determining which children get docked to the top of the screen when scrolling. For example, passing `stickyHeaderIndices={[0]}` will cause the first child to be fixed to the top of the scroll view. You can also use like [x,y,z] to make multiple items sticky when they are at the top. This property is not supported in conjunction with `horizontal={true}`.

| Type |
| --- |
| array of number |

---

### zoomScaleiOS​

The current scale of the scroll view content.

| Type | Default |
| --- | --- |
| number | 1.0 |

---

## Methods​

### flashScrollIndicators()​

 tsx

```
flashScrollIndicators();
```

Displays the scroll indicators momentarily.

---

### scrollTo()​

 tsx

```
scrollTo(  options?: {x?: number, y?: number, animated?: boolean} | number,  deprecatedX?: number,  deprecatedAnimated?: boolean,);
```

Scrolls to a given x, y offset, either immediately, with a smooth animation.

**Example:**

`scrollTo({x: 0, y: 0, animated: true})`

 note

The weird function signature is due to the fact that, for historical reasons, the function also accepts separate arguments as an alternative to the options object. This is deprecated due to ambiguity (y before x), and SHOULD NOT BE USED.

---

### scrollToEnd()​

 tsx

```
scrollToEnd(options?: {animated?: boolean});
```

If this is a vertical ScrollView scrolls to the bottom. If this is a horizontal ScrollView scrolls to the right.

Use `scrollToEnd({animated: true})` for smooth animated scrolling, `scrollToEnd({animated: false})` for immediate scrolling. If no options are passed, `animated` defaults to `true`.

Is this page useful?

---

# SectionList

> A performant interface for rendering sectioned lists, supporting the most handy features:

A performant interface for rendering sectioned lists, supporting the most handy features:

- Fully cross-platform.
- Configurable viewability callbacks.
- List header support.
- List footer support.
- Item separator support.
- Section header support.
- Section separator support.
- Heterogeneous data and item rendering support.
- Pull to Refresh.
- Scroll loading.

If you don't need section support and want a simpler interface, use [<FlatList>](https://reactnative.dev/docs/flatlist).

## Example​

This is a convenience wrapper around [<VirtualizedList>](https://reactnative.dev/docs/virtualizedlist), and thus inherits its props (as well as those of [<ScrollView>](https://reactnative.dev/docs/scrollview)) that aren't explicitly listed here, along with the following caveats:

- Internal state is not preserved when content scrolls out of the render window. Make sure all your data is captured in the item data or external stores like Flux, Redux, or Relay.
- This is a `PureComponent` which means that it will not re-render if `props` remain shallow-equal. Make sure that everything your `renderItem` function depends on is passed as a prop (e.g. `extraData`) that is not `===` after updates, otherwise your UI may not update on changes. This includes the `data` prop and parent component state.
- In order to constrain memory and enable smooth scrolling, content is rendered asynchronously offscreen. This means it's possible to scroll faster than the fill rate and momentarily see blank content. This is a tradeoff that can be adjusted to suit the needs of each application, and we are working on improving it behind the scenes.
- By default, the list looks for a `key` prop on each item and uses that for the React key. Alternatively, you can provide a custom `keyExtractor` prop.

---

# Reference

## Props​

### VirtualizedList Props​

Inherits [VirtualizedList Props](https://reactnative.dev/docs/virtualizedlist#props).

---

### RequiredrenderItem​

Default renderer for every item in every section. Can be over-ridden on a per-section basis. Should return a React element.

| Type |
| --- |
| function |

The render function will be passed an object with the following keys:

- 'item' (object) - the item object as specified in this section's `data` key
- 'index' (number) - Item's index within the section.
- 'section' (object) - The full section object as specified in `sections`.
- 'separators' (object) - An object with the following keys:
  - 'highlight' (function) - `() => void`
  - 'unhighlight' (function) - `() => void`
  - 'updateProps' (function) - `(select, newProps) => void`
    - 'select' (enum) - possible values are 'leading', 'trailing'
    - 'newProps' (object)

---

### Requiredsections​

The actual data to render, akin to the `data` prop in [FlatList](https://reactnative.dev/docs/flatlist).

| Type |
| --- |
| array ofSections |

---

### extraData​

A marker property for telling the list to re-render (since it implements `PureComponent`). If any of your `renderItem`, Header, Footer, etc. functions depend on anything outside of the `data` prop, stick it here and treat it immutably.

| Type |
| --- |
| any |

---

### initialNumToRender​

How many items to render in the initial batch. This should be enough to fill the screen but not much more. Note these items will never be unmounted as part of the windowed rendering in order to improve perceived performance of scroll-to-top actions.

| Type | Default |
| --- | --- |
| number | 10 |

---

### inverted​

Reverses the direction of scroll. Uses scale transforms of -1.

| Type | Default |
| --- | --- |
| boolean | false |

---

### ItemSeparatorComponent​

Rendered in between each item, but not at the top or bottom. By default, `highlighted`, `section`, and `[leading/trailing][Item/Section]` props are provided. `renderItem` provides `separators.highlight`/`unhighlight` which will update the `highlighted` prop, but you can also add custom props with `separators.updateProps`. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, function, element |

---

### keyExtractor​

Used to extract a unique key for a given item at the specified index. Key is used for caching and as the React key to track item re-ordering. The default extractor checks `item.key`, then `item.id`, and then falls back to using the index, like React does. Note that this sets keys for each item, but each overall section still needs its own key.

| Type |
| --- |
| (item: object, index: number) => string |

---

### ListEmptyComponent​

Rendered when the list is empty. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### ListFooterComponent​

Rendered at the very end of the list. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### ListHeaderComponent​

Rendered at the very beginning of the list. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### onRefresh​

If provided, a standard RefreshControl will be added for "Pull to Refresh" functionality. Make sure to also set the `refreshing` prop correctly. To offset the RefreshControl from the top (e.g. by 100 pts), use `progressViewOffset={100}`.

| Type |
| --- |
| function |

---

### onViewableItemsChanged​

Called when the viewability of rows changes, as defined by the `viewabilityConfig` prop.

| Type |
| --- |
| (callback: {changed:ViewToken[], viewableItems:ViewToken[]}) => void |

---

### refreshing​

Set this true while waiting for new data from a refresh.

| Type | Default |
| --- | --- |
| boolean | false |

---

### removeClippedSubviews​

 warning

Using this property may lead to bugs (missing content) in some circumstances - use at your own risk.

When `true`, offscreen child views are removed from their native backing superview when offscreen. This may improve scroll performance for large lists. On Android the default value is `true`.

| Type |
| --- |
| boolean |

---

### renderSectionFooter​

Rendered at the bottom of each section.

| Type |
| --- |
| (info: {section:Section}) => element ｜ null |

---

### renderSectionHeader​

Rendered at the top of each section. These stick to the top of the `ScrollView` by default on iOS. See `stickySectionHeadersEnabled`.

| Type |
| --- |
| (info: {section:Section}) => element ｜ null |

---

### SectionSeparatorComponent​

Rendered at the top and bottom of each section (note this is different from `ItemSeparatorComponent` which is only rendered between items). These are intended to separate sections from the headers above and below and typically have the same highlight response as `ItemSeparatorComponent`. Also receives `highlighted`, `[leading/trailing][Item/Section]`, and any custom props from `separators.updateProps`.

| Type |
| --- |
| component, element |

---

### stickySectionHeadersEnabled​

Makes section headers stick to the top of the screen until the next one pushes it off. Only enabled by default on iOS because that is the platform standard there.

| Type | Default |
| --- | --- |
| boolean | falseAndroidtrueiOS |

## Methods​

### flashScrollIndicators()iOS​

 tsx

```
flashScrollIndicators();
```

Displays the scroll indicators momentarily.

---

### recordInteraction()​

 tsx

```
recordInteraction();
```

Tells the list an interaction has occurred, which should trigger viewability calculations, e.g. if `waitForInteractions` is true and the user has not scrolled. This is typically called by taps on items or by navigation actions.

---

### scrollToLocation()​

 tsx

```
scrollToLocation(params: SectionListScrollParams);
```

Scrolls to the item at the specified `sectionIndex` and `itemIndex` (within the section) positioned in the viewable area such that `viewPosition` set to `0` places it at the top (and may be covered by a sticky header), `1` at the bottom, and `0.5` centered in the middle.

 note

You cannot scroll to locations outside the render window without specifying the `getItemLayout` or `onScrollToIndexFailed` prop.

**Parameters:**

| Name | Type |
| --- | --- |
| paramsRequired | object |

Valid `params` keys are:

- 'animated' (boolean) - Whether the list should do an animation while scrolling. Defaults to `true`.
- 'itemIndex' (number) - Index within section for the item to scroll to. Required.
- 'sectionIndex' (number) - Index for section that contains the item to scroll to. Required.
- 'viewOffset' (number) - A fixed number of pixels to offset the final target position, e.g. to compensate for sticky headers.
- 'viewPosition' (number) - A value of `0` places the item specified by index at the top, `1` at the bottom, and `0.5` centered in the middle.

## Type Definitions​

### Section​

An object that identifies the data to be rendered for a given section.

| Type |
| --- |
| any |

**Properties:**

| Name | Type | Description |
| --- | --- | --- |
| dataRequired | array | The data for rendering items in this section. Array of objects, much likeFlatList's data prop. |
| key | string | Optional key to keep track of section re-ordering. If you don't plan on re-ordering sections, the array index will be used by default. |
| renderItem | function | Optionally define an arbitrary item renderer for this section, overriding the defaultrenderItemfor the list. |
| ItemSeparatorComponent | component, element | Optionally define an arbitrary item separator for this section, overriding the defaultItemSeparatorComponentfor the list. |
| keyExtractor | function | Optionally define an arbitrary key extractor for this section, overriding the defaultkeyExtractor. |

Is this page useful?
