# FlatList and more

# FlatList

> A performant interface for rendering basic, flat lists, supporting the most handy features:

A performant interface for rendering basic, flat lists, supporting the most handy features:

- Fully cross-platform.
- Optional horizontal mode.
- Configurable viewability callbacks.
- Header support.
- Footer support.
- Separator support.
- Pull to Refresh.
- Scroll loading.
- ScrollToIndex support.
- Multiple column support.

If you need section support, use [<SectionList>](https://reactnative.dev/docs/sectionlist).

## Example​

To render multiple columns, use the [numColumns](https://reactnative.dev/docs/flatlist#numcolumns) prop. Using this approach instead of a `flexWrap` layout can prevent conflicts with the item height logic.

More complex, selectable example below.

- By passing `extraData={selectedId}` to `FlatList` we make sure `FlatList` itself will re-render when the state changes. Without setting this prop, `FlatList` would not know it needs to re-render any items because it is a `PureComponent` and the prop comparison will not show any changes.
- `keyExtractor` tells the list to use the `id`s for the react keys instead of the default `key` property.

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

 tsx

```
renderItem({  item: ItemT,  index: number,  separators: {    highlight: () => void;    unhighlight: () => void;    updateProps: (select: 'leading' | 'trailing', newProps: any) => void;  }}): JSX.Element;
```

Takes an item from `data` and renders it into the list.

Provides additional metadata like `index` if you need it, as well as a more generic `separators.updateProps` function which let you set whatever props you want to change the rendering of either the leading separator or trailing separator in case the more common `highlight` and `unhighlight` (which set the `highlighted: boolean` prop) are insufficient for your use case.

| Type |
| --- |
| function |

- `item` (Object): The item from `data` being rendered.
- `index` (number): The index corresponding to this item in the `data` array.
- `separators` (Object)
  - `highlight` (Function)
  - `unhighlight` (Function)
  - `updateProps` (Function)
    - `select` (enum('leading', 'trailing'))
    - `newProps` (Object)

Example usage:

 tsx

```
<FlatList  ItemSeparatorComponent={    Platform.OS !== 'android' &&    (({highlighted}) => (      <View        style={[style.separator, highlighted && {marginLeft: 0}]}      />    ))  }  data={[{title: 'Title Text', key: 'item1'}]}  renderItem={({item, index, separators}) => (    <TouchableHighlight      key={item.key}      onPress={() => this._onPress(item)}      onShowUnderlay={separators.highlight}      onHideUnderlay={separators.unhighlight}>      <View style={{backgroundColor: 'white'}}>        <Text>{item.title}</Text>      </View>    </TouchableHighlight>  )}/>
```

---

### Requireddata​

An array (or array-like list) of items to render. Other data types can be used by targeting [VirtualizedList](https://reactnative.dev/docs/virtualizedlist) directly.

| Type |
| --- |
| ArrayLike |

---

### ItemSeparatorComponent​

Rendered in between each item, but not at the top or bottom. By default, `highlighted` and `leadingItem` props are provided. `renderItem` provides `separators.highlight`/`unhighlight` which will update the `highlighted` prop, but you can also add custom props with `separators.updateProps`. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, function, element |

---

### ListEmptyComponent​

Rendered when the list is empty. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### ListFooterComponent​

Rendered at the bottom of all the items. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### ListFooterComponentStyle​

Styling for internal View for `ListFooterComponent`.

| Type |
| --- |
| View Style |

---

### ListHeaderComponent​

Rendered at the top of all the items. Can be a React Component (e.g. `SomeComponent`), or a React element (e.g. `<SomeComponent />`).

| Type |
| --- |
| component, element |

---

### ListHeaderComponentStyle​

Styling for internal View for `ListHeaderComponent`.

| Type |
| --- |
| View Style |

---

### columnWrapperStyle​

Optional custom style for multi-item rows generated when `numColumns > 1`.

| Type |
| --- |
| View Style |

---

### extraData​

A marker property for telling the list to re-render (since it implements `PureComponent`). If any of your `renderItem`, Header, Footer, etc. functions depend on anything outside of the `data` prop, stick it here and treat it immutably.

| Type |
| --- |
| any |

---

### getItemLayout​

 tsx

```
(data, index) => {length: number, offset: number, index: number}
```

`getItemLayout` is an optional optimization that allows skipping the measurement of dynamic content if you know the size (height or width) of items ahead of time. `getItemLayout` is efficient if you have fixed size items, for example:

 tsx

```
getItemLayout={(data, index) => (    {length: ITEM_HEIGHT, offset: ITEM_HEIGHT * index, index}  )}
```

Adding `getItemLayout` can be a great performance boost for lists of several hundred items. Remember to include separator length (height or width) in your offset calculation if you specify `ItemSeparatorComponent`.

| Type |
| --- |
| function |

---

### horizontal​

If `true`, renders items next to each other horizontally instead of stacked vertically.

| Type |
| --- |
| boolean |

---

### initialNumToRender​

How many items to render in the initial batch. This should be enough to fill the screen but not much more. Note these items will never be unmounted as part of the windowed rendering in order to improve perceived performance of scroll-to-top actions.

| Type | Default |
| --- | --- |
| number | 10 |

---

### initialScrollIndex​

Instead of starting at the top with the first item, start at `initialScrollIndex`. This disables the "scroll to top" optimization that keeps the first `initialNumToRender` items always rendered and immediately renders the items starting at this initial index. Requires `getItemLayout` to be implemented.

| Type |
| --- |
| number |

---

### inverted​

Reverses the direction of scroll. Uses scale transforms of `-1`.

| Type |
| --- |
| boolean |

---

### keyExtractor​

 tsx

```
(item: ItemT, index: number) => string;
```

Used to extract a unique key for a given item at the specified index. Key is used for caching and as the react key to track item re-ordering. The default extractor checks `item.key`, then `item.id`, and then falls back to using the index, like React does.

| Type |
| --- |
| function |

---

### numColumns​

Multiple columns can only be rendered with `horizontal={false}` and will zig-zag like a `flexWrap` layout. Items should all be the same height - masonry layouts are not supported.

| Type |
| --- |
| number |

---

### onRefresh​

 tsx

```
() => void;
```

If provided, a standard RefreshControl will be added for "Pull to Refresh" functionality. Make sure to also set the `refreshing` prop correctly.

| Type |
| --- |
| function |

---

### onViewableItemsChanged​

Called when the viewability of rows changes, as defined by the `viewabilityConfig` prop.

| Type |
| --- |
| (callback: {changed:ViewToken[], viewableItems:ViewToken[]} => void; |

---

### progressViewOffset​

Set this when offset is needed for the loading indicator to show correctly.

| Type |
| --- |
| number |

---

### refreshing​

Set this true while waiting for new data from a refresh.

| Type |
| --- |
| boolean |

---

### removeClippedSubviews​

 warning

Using this property may lead to bugs (missing content) in some circumstances - use at your own risk.

When `true`, offscreen child views are removed from their native backing superview when offscreen. This may improve scroll performance for large lists. On Android the default value is `true`.

| Type |
| --- |
| boolean |

---

### viewabilityConfig​

See [ViewabilityHelper.js](https://github.com/facebook/react-native/blob/main/packages/react-native/Libraries/Lists/ViewabilityHelper.js) for flow type and further documentation.

| Type |
| --- |
| ViewabilityConfig |

`viewabilityConfig` takes a type `ViewabilityConfig` an object with following properties

| Property | Type |
| --- | --- |
| minimumViewTime | number |
| viewAreaCoveragePercentThreshold | number |
| itemVisiblePercentThreshold | number |
| waitForInteraction | boolean |

At least one of the `viewAreaCoveragePercentThreshold` or `itemVisiblePercentThreshold` is required. This needs to be done in the `constructor` to avoid following error ([ref](https://github.com/facebook/react-native/issues/17408)):

```
Error: Changing viewabilityConfig on the fly is not supported
```

 tsx

```
constructor (props) {  super(props)  this.viewabilityConfig = {      waitForInteraction: true,      viewAreaCoveragePercentThreshold: 95  }}
```

 tsx

```
<FlatList    viewabilityConfig={this.viewabilityConfig}  ...
```

#### minimumViewTime​

Minimum amount of time (in milliseconds) that an item must be physically viewable before the viewability callback will be fired. A high number means that scrolling through content without stopping will not mark the content as viewable.

#### viewAreaCoveragePercentThreshold​

Percent of viewport that must be covered for a partially occluded item to count as "viewable", 0-100. Fully visible items are always considered viewable. A value of 0 means that a single pixel in the viewport makes the item viewable, and a value of 100 means that an item must be either entirely visible or cover the entire viewport to count as viewable.

#### itemVisiblePercentThreshold​

Similar to `viewAreaCoveragePercentThreshold`, but considers the percent of the item that is visible, rather than the fraction of the viewable area it covers.

#### waitForInteraction​

Nothing is considered viewable until the user scrolls or `recordInteraction` is called after render.

---

### viewabilityConfigCallbackPairs​

List of `ViewabilityConfig`/`onViewableItemsChanged` pairs. A specific `onViewableItemsChanged` will be called when its corresponding `ViewabilityConfig`'s conditions are met. See `ViewabilityHelper.js` for flow type and further documentation.

| Type |
| --- |
| array of ViewabilityConfigCallbackPair |

## Methods​

### flashScrollIndicators()​

 tsx

```
flashScrollIndicators();
```

Displays the scroll indicators momentarily.

---

### getNativeScrollRef()​

 tsx

```
getNativeScrollRef(): React.ElementRef<typeof ScrollViewComponent>;
```

Provides a reference to the underlying scroll component

---

### getScrollResponder()​

 tsx

```
getScrollResponder(): ScrollResponderMixin;
```

Provides a handle to the underlying scroll responder.

---

### getScrollableNode()​

 tsx

```
getScrollableNode(): any;
```

Provides a handle to the underlying scroll node.

### scrollToEnd()​

 tsx

```
scrollToEnd(params?: {animated?: boolean});
```

Scrolls to the end of the content. May be janky without `getItemLayout` prop.

**Parameters:**

| Name | Type |
| --- | --- |
| params | object |

Valid `params` keys are:

- 'animated' (boolean) - Whether the list should do an animation while scrolling. Defaults to `true`.

---

### scrollToIndex()​

 tsx

```
scrollToIndex: (params: {  index: number;  animated?: boolean;  viewOffset?: number;  viewPosition?: number;});
```

Scrolls to the item at the specified index such that it is positioned in the viewable area such that `viewPosition` 0 places it at the top, 1 at the bottom, and 0.5 centered in the middle.

 note

Cannot scroll to locations outside the render window without specifying the `getItemLayout` prop.

**Parameters:**

| Name | Type |
| --- | --- |
| paramsRequired | object |

Valid `params` keys are:

- 'animated' (boolean) - Whether the list should do an animation while scrolling. Defaults to `true`.
- 'index' (number) - The index to scroll to. Required.
- 'viewOffset' (number) - A fixed number of pixels to offset the final target position.
- 'viewPosition' (number) - A value of `0` places the item specified by index at the top, `1` at the bottom, and `0.5` centered in the middle.

---

### scrollToItem()​

 tsx

```
scrollToItem(params: {  animated?: ?boolean,  item: Item,  viewPosition?: number,});
```

Requires linear scan through data - use `scrollToIndex` instead if possible.

 note

Cannot scroll to locations outside the render window without specifying the `getItemLayout` prop.

**Parameters:**

| Name | Type |
| --- | --- |
| paramsRequired | object |

Valid `params` keys are:

- 'animated' (boolean) - Whether the list should do an animation while scrolling. Defaults to `true`.
- 'item' (object) - The item to scroll to. Required.
- 'viewPosition' (number)

---

### scrollToOffset()​

 tsx

```
scrollToOffset(params: {  offset: number;  animated?: boolean;});
```

Scroll to a specific content pixel offset in the list.

**Parameters:**

| Name | Type |
| --- | --- |
| paramsRequired | object |

Valid `params` keys are:

- 'offset' (number) - The offset to scroll to. In case of `horizontal` being true, the offset is the x-value, in any other case the offset is the y-value. Required.
- 'animated' (boolean) - Whether the list should do an animation while scrolling. Defaults to `true`.

Is this page useful?

---

# Layout with Flexbox

> A component can specify the layout of its children using the Flexbox algorithm. Flexbox is designed to provide a consistent layout on different screen sizes.

A component can specify the layout of its children using the Flexbox algorithm. Flexbox is designed to provide a consistent layout on different screen sizes.

You will normally use a combination of `flexDirection`, `alignItems`, and `justifyContent` to achieve the right layout.

 caution

Flexbox works the same way in React Native as it does in CSS on the web, with a few exceptions.
The defaults are different, with `flexDirection` defaulting to `column` instead of `row`, `alignContent` defaulting to `flex-start` instead of `stretch`, `flexShrink` defaulting to `0` instead of `1`, the `flex` parameter only supporting a single number.

## Flex​

[flex](https://reactnative.dev/docs/layout-props#flex) will define how your items are going to **“fill”** over the available space along your main axis. Space will be divided according to each element's flex property.

In the following example, the red, orange, and green views are all children in the container view that has `flex: 1` set. The red view uses `flex: 1` , the orange view uses `flex: 2`, and the green view uses `flex: 3` . **1+2+3 = 6**, which means that the red view will get `1/6` of the space, the orange `2/6` of the space, and the green `3/6` of the space.

## Flex Direction​

[flexDirection](https://reactnative.dev/docs/layout-props#flexdirection) controls the direction in which the children of a node are laid out. This is also referred to as the main axis. The cross axis is the axis perpendicular to the main axis, or the axis which the wrapping lines are laid out in.

- `column` (**default value**) Align children from top to bottom. If wrapping is enabled, then the next line will start to the right of the first item on the top of the container.
- `row` Align children from left to right. If wrapping is enabled, then the next line will start under the first item on the left of the container.
- `column-reverse` Align children from bottom to top. If wrapping is enabled, then the next line will start to the right of the first item on the bottom of the container.
- `row-reverse` Align children from right to left. If wrapping is enabled, then the next line will start under the first item on the right of the container.

You can learn more [here](https://www.yogalayout.dev/docs/styling/flex-direction).

## Layout Direction​

Layout [direction](https://reactnative.dev/docs/layout-props#direction) specifies the direction in which children and text in a hierarchy should be laid out. Layout direction also affects what edge `start` and `end` refer to. By default, React Native lays out with LTR layout direction. In this mode `start` refers to left and `end` refers to right.

- `LTR` (**default value**) Text and children are laid out from left to right. Margin and padding applied to the start of an element are applied on the left side.
- `RTL` Text and children are laid out from right to left. Margin and padding applied to the start of an element are applied on the right side.

## Justify Content​

[justifyContent](https://reactnative.dev/docs/layout-props#justifycontent) describes how to align children within the main axis of their container. For example, you can use this property to center a child horizontally within a container with `flexDirection` set to `row` or vertically within a container with `flexDirection` set to `column`.

- `flex-start`(**default value**) Align children of a container to the start of the container's main axis.
- `flex-end` Align children of a container to the end of the container's main axis.
- `center` Align children of a container in the center of the container's main axis.
- `space-between` Evenly space off children across the container's main axis, distributing the remaining space between the children.
- `space-around` Evenly space off children across the container's main axis, distributing the remaining space around the children. Compared to `space-between`, using `space-around` will result in space being distributed to the beginning of the first child and end of the last child.
- `space-evenly` Evenly distribute children within the alignment container along the main axis. The spacing between each pair of adjacent items, the main-start edge and the first item, and the main-end edge and the last item, are all exactly the same.

You can learn more [here](https://www.yogalayout.dev/docs/styling/justify-content).

## Align Items​

[alignItems](https://reactnative.dev/docs/layout-props#alignitems) describes how to align children along the cross axis of their container. It is very similar to `justifyContent` but instead of applying to the main axis, `alignItems` applies to the cross axis.

- `stretch` (**default value**) Stretch children of a container to match the `height` of the container's cross axis.
- `flex-start` Align children of a container to the start of the container's cross axis.
- `flex-end` Align children of a container to the end of the container's cross axis.
- `center` Align children of a container in the center of the container's cross axis.
- `baseline` Align children of a container along a common baseline. Individual children can be set to be the reference baseline for their parents.

 info

For `stretch` to have an effect, children must not have a fixed dimension along the secondary axis. In the following example, setting `alignItems: stretch` does nothing until the `width: 50` is removed from the children.

You can learn more [here](https://www.yogalayout.dev/docs/styling/align-items-self).

## Align Self​

[alignSelf](https://reactnative.dev/docs/layout-props#alignself) has the same options and effect as `alignItems` but instead of affecting the children within a container, you can apply this property to a single child to change its alignment within its parent. `alignSelf` overrides any option set by the parent with `alignItems`.

## Align Content​

[alignContent](https://reactnative.dev/docs/layout-props#aligncontent) defines the distribution of lines along the cross-axis. This only has effect when items are wrapped to multiple lines using `flexWrap`.

- `flex-start` (**default value**) Align wrapped lines to the start of the container's cross axis.
- `flex-end` Align wrapped lines to the end of the container's cross axis.
- `stretch` (*default value when using Yoga on the web*) Stretch wrapped lines to match the height of the container's cross axis.
- `center` Align wrapped lines in the center of the container's cross axis.
- `space-between` Evenly space wrapped lines across the container's cross axis, distributing the remaining space between the lines.
- `space-around` Evenly space wrapped lines across the container's cross axis, distributing the remaining space around the lines. Each end of the container has a half-sized space compared to the space between items.
- `space-evenly` Evenly space wrapped lines across the container's cross axis, distributing the remaining space around the lines. Each space is the same size.

You can learn more [here](https://www.yogalayout.dev/docs/styling/align-content).

## Flex Wrap​

The [flexWrap](https://reactnative.dev/docs/layout-props#flexwrap) property is set on containers and it controls what happens when children overflow the size of the container along the main axis. By default, children are forced into a single line (which can shrink elements). If wrapping is allowed, items are wrapped into multiple lines along the main axis if needed.

When wrapping lines, `alignContent` can be used to specify how the lines are placed in the container. Learn more [here](https://www.yogalayout.dev/docs/styling/flex-wrap).

## Flex Basis, Grow, and Shrink​

- [flexBasis](https://reactnative.dev/docs/layout-props#flexbasis) is an axis-independent way of providing the default size of an item along the main axis. Setting the `flexBasis` of a child is similar to setting the `width` of that child if its parent is a container with `flexDirection: row` or setting the `height` of a child if its parent is a container with `flexDirection: column`. The `flexBasis` of an item is the default size of that item, the size of the item before any `flexGrow` and `flexShrink` calculations are performed.
- [flexGrow](https://reactnative.dev/docs/layout-props#flexgrow) describes how much space within a container should be distributed among its children along the main axis. After laying out its children, a container will distribute any remaining space according to the flex grow values specified by its children.
  `flexGrow` accepts any floating point value >= 0, with 0 being the default value. A container will distribute any remaining space among its children weighted by the children’s `flexGrow` values.
- [flexShrink](https://reactnative.dev/docs/layout-props#flexshrink) describes how to shrink children along the main axis in the case in which the total size of the children overflows the size of the container on the main axis. `flexShrink` is very similar to `flexGrow` and can be thought of in the same way if any overflowing size is considered to be negative remaining space. These two properties also work well together by allowing children to grow and shrink as needed.
  `flexShrink` accepts any floating point value >= 0, with 0 being the default value (on the web, the default is 1). A container will shrink its children weighted by the children’s `flexShrink` values.

You can learn more [here](https://www.yogalayout.dev/docs/styling/flex-basis-grow-shrink).

## Row Gap, Column Gap and Gap​

- [rowGap](https://reactnative.dev/docs/layout-props#rowgap) sets the size of the gap (gutter) between an element's rows.
- [columnGap](https://reactnative.dev/docs/layout-props#columngap) sets the size of the gap (gutter) between an element's columns.
- [gap](https://reactnative.dev/docs/layout-props#gap) sets the size of the gap (gutter) between rows and columns. It is a shorthand for `rowGap` and `columnGap`.

You can use `flexWrap` and `alignContent` along with `gap` to add consistent spacing between items.

## Width and Height​

The `width` property specifies the width of an element's content area. Similarly, the `height` property specifies the height of an element's content area.

Both `width` and `height` can take the following values:

- `auto` (**default value**) React Native calculates the width/height for the element based on its content, whether that is other children, text, or an image.
- `pixels` Defines the width/height in absolute pixels. Depending on other styles set on the component, this may or may not be the final dimension of the node.
- `percentage` Defines the width or height in percentage of its parent's width or height, respectively.

## Position​

The `position` type of an element defines how it is positioned relative to either itself, its parent, or its [containing block](https://reactnative.dev/docs/flexbox#the-containing-block).

- `relative` (**default value**) By default, an element is positioned relatively. This means an element is positioned according to the normal flow of the layout, and then offset relative to that position based on the values of `top`, `right`, `bottom`, and `left`. The offset does not affect the position of any sibling or parent elements.
- `absolute` When positioned absolutely, an element doesn't take part in the normal layout flow. It is instead laid out independent of its siblings. The position is determined based on the `top`, `right`, `bottom`, and `left` values. These values will position the element relative to its containing block.
- `static` When positioned statically, an element is positioned according to the normal flow of layout, and will ignore the `top`, `right`, `bottom`, and `left` values. This `position` will also cause the element to not form a containing block for absolute descendants, unless some other superceding style prop is present (e.g. `transform`). This allows `absolute` elements to be positioned to something that is not their parent. Note that **staticis only available on the New Architecture**.

## The Containing Block​

The containing block of an element is an ancestor element which controls its position and size.
The way containing blocks work in React Native is very similar to [how they work on the web](https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block), with some simplifications due to the lack of some web features.

The `top`, `right`, `bottom`, and `left` values of an absolutely positioned element will be
relative to its containing block.

Percentage lengths (e.g.: `width: '50%'` or `padding: '10%'`) applied to absolutely positioned elements will be calculated relatively to the size of its containing block. For example, if the containing block is 100 points wide, then `width: 50%` on an absolutely positioned element will cause it to be 50 points wide.

The following list will help you determine the containing block of any given element:

- If that element has a `position` type of `relative` or `static`, then its containing block is its parent.
- If that element has a `position` type of `absolute`, then its containing block is the nearest ancestor in which one of the following is true:
  - It has a `position` type other than `static`
  - It has a `transform`

## Going Deeper​

Check out the interactive [yoga playground](https://www.yogalayout.dev/playground) that you can use to get a better understanding of flexbox.

We've covered the basics, but there are many other styles you may need for layouts. The full list of props that control layout is documented [here](https://reactnative.dev/docs/layout-props).

Additionally, you can see some examples from [Wix Engineers](https://medium.com/wix-engineering/the-full-react-native-layout-cheat-sheet-a4147802405c).

Is this page useful?

---

# Gesture Responder System

> The gesture responder system manages the lifecycle of gestures in your app. A touch can go through several phases as the app determines what the user's intention is. For example, the app needs to determine if the touch is scrolling, sliding on a widget, or tapping. This can even change during the duration of a touch. There can also be multiple simultaneous touches.

The gesture responder system manages the lifecycle of gestures in your app. A touch can go through several phases as the app determines what the user's intention is. For example, the app needs to determine if the touch is scrolling, sliding on a widget, or tapping. This can even change during the duration of a touch. There can also be multiple simultaneous touches.

The touch responder system is needed to allow components to negotiate these touch interactions without any additional knowledge about their parent or child components.

### Best Practices​

To make your app feel great, every action should have the following attributes:

- Feedback/highlighting- show the user what is handling their touch, and what will happen when they release the gesture
- Cancel-ability- when making an action, the user should be able to abort it mid-touch by dragging their finger away

These features make users more comfortable while using an app, because it allows people to experiment and interact without fear of making mistakes.

### TouchableHighlight and Touchable*​

The responder system can be complicated to use. So we have provided an abstract `Touchable` implementation for things that should be "tappable". This uses the responder system and allows you to configure tap interactions declaratively. Use `TouchableHighlight` anywhere where you would use a button or link on web.

## Responder Lifecycle​

A view can become the touch responder by implementing the correct negotiation methods. There are two methods to ask the view if it wants to become responder:

- `View.props.onStartShouldSetResponder: evt => true,` - Does this view want to become responder on the start of a touch?
- `View.props.onMoveShouldSetResponder: evt => true,` - Called for every touch move on the View when it is not the responder: does this view want to "claim" touch responsiveness?

If the View returns true and attempts to become the responder, one of the following will happen:

- `View.props.onResponderGrant: evt => {}` - The View is now responding for touch events. This is the time to highlight and show the user what is happening
- `View.props.onResponderReject: evt => {}` - Something else is the responder right now and will not release it

If the view is responding, the following handlers can be called:

- `View.props.onResponderMove: evt => {}` - The user is moving their finger
- `View.props.onResponderRelease: evt => {}` - Fired at the end of the touch, ie "touchUp"
- `View.props.onResponderTerminationRequest: evt => true` - Something else wants to become responder. Should this view release the responder? Returning true allows release
- `View.props.onResponderTerminate: evt => {}` - The responder has been taken from the View. Might be taken by other views after a call to `onResponderTerminationRequest`, or might be taken by the OS without asking (happens with control center/ notification center on iOS)

`evt` is a synthetic touch event with the following form:

- `nativeEvent`
  - `changedTouches` - Array of all touch events that have changed since the last event
  - `identifier` - The ID of the touch
  - `locationX` - The X position of the touch, relative to the element
  - `locationY` - The Y position of the touch, relative to the element
  - `pageX` - The X position of the touch, relative to the root element
  - `pageY` - The Y position of the touch, relative to the root element
  - `target` - The node id of the element receiving the touch event
  - `timestamp` - A time identifier for the touch, useful for velocity calculation
  - `touches` - Array of all current touches on the screen

### Capture ShouldSet Handlers​

`onStartShouldSetResponder` and `onMoveShouldSetResponder` are called with a bubbling pattern, where the deepest node is called first. That means that the deepest component will become responder when multiple Views return true for `*ShouldSetResponder` handlers. This is desirable in most cases, because it makes sure all controls and buttons are usable.

However, sometimes a parent will want to make sure that it becomes responder. This can be handled by using the capture phase. Before the responder system bubbles up from the deepest component, it will do a capture phase, firing `on*ShouldSetResponderCapture`. So if a parent View wants to prevent the child from becoming responder on a touch start, it should have a `onStartShouldSetResponderCapture` handler which returns true.

- `View.props.onStartShouldSetResponderCapture: evt => true,`
- `View.props.onMoveShouldSetResponderCapture: evt => true,`

### PanResponder​

For higher-level gesture interpretation, check out [PanResponder](https://reactnative.dev/docs/panresponder).

Is this page useful?

---

# Get Started Without a Framework

> If you have constraints that are not served well by a Framework, or you prefer to write your own Framework, you can create a React Native app without using a Framework.

**Platform support**

If you have constraints that are not served well by a [Framework](https://reactnative.dev/architecture/glossary#react-native-framework), or you prefer to write your own Framework, you can create a React Native app without using a Framework.

To do so, you'll first need to [set up your environment](https://reactnative.dev/docs/set-up-your-environment). Once you're set up, continue with the steps below to create an application and start developing.

### Step 1: Creating a new application​

 warning

If you previously installed a global `react-native-cli` package, please remove it as it may cause unexpected issues:

shell

```
npm uninstall -g react-native-cli @react-native-community/cli
```

You can use [React Native Community CLI](https://github.com/react-native-community/cli) to generate a new project. Let's create a new React Native project called "AwesomeProject":

 shell

```
npx @react-native-community/cli@latest init AwesomeProject
```

This is not necessary if you are integrating React Native into an existing application, or if you've installed [Expo](https://docs.expo.dev/bare/installing-expo-modules/) in your project, or if you're adding Android support to an existing React Native project (see [Integration with Existing Apps](https://reactnative.dev/docs/integration-with-existing-apps)). You can also use a third-party CLI to set up your React Native app, such as [Ignite CLI](https://github.com/infinitered/ignite).

 info

If you are having trouble with iOS, try to reinstall the dependencies by running:

1. `cd ios` to navigate to the `ios` folder.
2. `bundle install` to install [Bundler](https://bundler.io/)
3. `bundle exec pod install` to install the iOS dependencies managed by CocoaPods.

#### [Optional] Using a specific version or template​

If you want to start a new project with a specific React Native version, you can use the `--version` argument:

 shell

```
npx @react-native-community/cli@X.XX.X init AwesomeProject --version X.XX.X
```

You can also start a project with a custom React Native template with the `--template` argument, read more [here](https://github.com/react-native-community/cli/blob/main/docs/init.md#initializing-project-with-custom-template).

### Step 2: Start Metro​

[Metro](https://metrobundler.dev/) is the JavaScript build tool for React Native. To start the Metro development server, run the following from your project folder:

shell

```
npm start
```

shell

```
yarn start
```

 note

If you're familiar with web development, Metro is similar to bundlers such as Vite and webpack, but is designed end-to-end for React Native. For instance, Metro uses [Babel](https://babel.dev/) to transform syntax such as JSX into executable JavaScript.

### Step 3: Start your application​

Let Metro Bundler run in its own terminal. Open a new terminal inside your React Native project folder. Run the following:

shell

```
npm run android
```

shell

```
yarn android
```

If everything is set up correctly, you should see your new app running in your Android emulator shortly.

This is one way to run your app - you can also run it directly from within Android Studio.

 tip

If you can't get this to work, see the [Troubleshooting](https://reactnative.dev/docs/troubleshooting) page.

### Step 4: Modifying your app​

Now that you have successfully run the app, let's modify it.

- Open `App.tsx` in your text editor of choice and edit some lines.
- Press the R key twice or select `Reload` from the Dev Menu (Ctrl + M) to see your changes!

### That's it!​

Congratulations! You've successfully run and modified your first barebone React Native app.

 ![image](https://reactnative.dev/docs/assets/GettingStartedCongratulations.png)

### Now what?​

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [Introduction to React Native](https://reactnative.dev/docs/getting-started).

Is this page useful?

---

# Introduction

> This helpful guide lays out the prerequisites for learning React Native, using these docs, and setting up your environment.

Welcome to the very start of your React Native journey! If you're looking for getting started instructions, they've moved to [their own section](https://reactnative.dev/docs/environment-setup). Continue reading for an introduction to the documentation, Native Components, React, and more!

![ ](https://reactnative.dev/docs/assets/p_android-ios-devices.svg)

Many different kinds of people use React Native: from advanced iOS developers to React beginners, to people getting started programming for the first time in their career. These docs were written for all learners, no matter their experience level or background.

## How to use these docs​

You can start here and read through these docs linearly like a book; or you can read the specific sections you need. Already familiar with React? You can skip [that section](https://reactnative.dev/docs/intro-react)—or read it for a light refresher.

## Prerequisites​

To work with React Native, you will need to have an understanding of JavaScript fundamentals. If you’re new to JavaScript or need a refresher, you can [dive in](https://developer.mozilla.org/en-US/docs/Web/JavaScript) or [brush up](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript) at Mozilla Developer Network.

 info

While we do our best to assume no prior knowledge of React, Android, or iOS development, these are valuable topics of study for the aspiring React Native developer. Where sensible, we have linked to resources and articles that go more in depth.

## Interactive examples​

This introduction lets you get started immediately in your browser with interactive examples like this one:

The above is a Snack Player. It’s a handy tool created by Expo to embed and run React Native projects and share how they render in platforms like Android and iOS. The code is live and editable, so you can play directly with it in your browser. Go ahead and try changing the "Try editing me!" text above to "Hello, world!"

 tip

Optionally, if you want to set up a local development environment, [you can follow our guide to setting up your environment on your local machine](https://reactnative.dev/docs/set-up-your-environment) and paste the code examples into your project. (If you are a web developer, you may already have a local environment set up for mobile browser testing!)

## Developer Notes​

People from many different development backgrounds are learning React Native. You may have experience with a range of technologies, from web to Android to iOS and more. We try to write for developers from all backgrounds. Sometimes we provide explanations specific to one platform or another like so:

info

Android developers may be familiar with this concept.

info

iOS developers may be familiar with this concept.

info

Web developers may be familiar with this concept.

## Formatting​

Menu paths are written in bold and use carets to navigate submenus. Example: **Android Studio > Preferences**

---

Now that you know how this guide works, it's time to get to know the foundation of React Native: [Native Components](https://reactnative.dev/docs/intro-react-native-components).

Is this page useful?
