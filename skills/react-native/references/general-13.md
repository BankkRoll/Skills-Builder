# Layout Props and more

# Layout Props

> More detailed examples about those properties can be found on the Layout with Flexbox page.

info

More detailed examples about those properties can be found on the [Layout with Flexbox](https://reactnative.dev/docs/flexbox) page.

### Example​

The following example shows how different properties can affect or shape a React Native layout. You can try for example to add or remove squares from the UI while changing the values of the property `flexWrap`.

---

# Reference

## Props​

### alignContent​

`alignContent` controls how rows align in the cross direction, overriding the `alignContent` of the parent.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/align-content) for more details.

| Type | Required |
| --- | --- |
| enum('flex-start', 'flex-end', 'center', 'stretch', 'space-between', 'space-around', 'space-evenly') | No |

---

### alignItems​

`alignItems` aligns children in the cross direction. For example, if children are flowing vertically, `alignItems` controls how they align horizontally. It works like `align-items` in CSS (default: stretch).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/align-items) for more details.

| Type | Required |
| --- | --- |
| enum('flex-start', 'flex-end', 'center', 'stretch', 'baseline') | No |

---

### alignSelf​

`alignSelf` controls how a child aligns in the cross direction, overriding the `alignItems` of the parent. It works like `align-self` in CSS (default: auto).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/align-self) for more details.

| Type | Required |
| --- | --- |
| enum('auto', 'flex-start', 'flex-end', 'center', 'stretch', 'baseline') | No |

---

### aspectRatio​

Aspect ratio controls the size of the undefined dimension of a node.

- On a node with a set width/height, aspect ratio controls the size of the unset dimension
- On a node with a set flex basis, aspect ratio controls the size of the node in the cross axis if unset
- On a node with a measure function, aspect ratio works as though the measure function measures the flex basis
- On a node with flex grow/shrink, aspect ratio controls the size of the node in the cross axis if unset
- Aspect ratio takes min/max dimensions into account

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### borderBottomWidth​

`borderBottomWidth` works like `border-bottom-width` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/border-bottom-width) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### borderEndWidth​

When direction is `ltr`, `borderEndWidth` is equivalent to `borderRightWidth`. When direction is `rtl`, `borderEndWidth` is equivalent to `borderLeftWidth`.

| Type | Required |
| --- | --- |
| number | No |

---

### borderLeftWidth​

`borderLeftWidth` works like `border-left-width` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/border-left-width) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### borderRightWidth​

`borderRightWidth` works like `border-right-width` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/border-right-width) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### borderStartWidth​

When direction is `ltr`, `borderStartWidth` is equivalent to `borderLeftWidth`. When direction is `rtl`, `borderStartWidth` is equivalent to `borderRightWidth`.

| Type | Required |
| --- | --- |
| number | No |

---

### borderTopWidth​

`borderTopWidth` works like `border-top-width` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/border-top-width) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### borderWidth​

`borderWidth` works like `border-width` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/border-width) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### bottom​

`bottom` is the number of logical pixels to offset the bottom edge of this component.

It works similarly to `bottom` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/bottom) for more details of how `bottom` affects layout.

| Type | Required |
| --- | --- |
| number, string | No |

---

### boxSizing​

`boxSizing` defines how the element's various sizing props (`width`, `height`, `minWidth`, `minHeight`, etc.) are computed. If `boxSizing` is `border-box`, these sizes apply to the border box of the element. If it is `content-box`, they apply to the content box of the element. The default value is `border-box`. The [web documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing) is a good source of information if you wish to learn more about how this prop works.

| Type | Required |
| --- | --- |
| enum('border-box', 'content-box') | No |

---

### columnGap​

`columnGap` works like `column-gap` in CSS. Only pixel units are supported in React Native.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/column-gap) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### direction​

`direction` specifies the directional flow of the user interface. The default is `inherit`, except for root node which will have value based on the current locale.

See [MDN CSS Reference](https://www.yogalayout.dev/docs/styling/layout-direction) for more details.

| Type | Required |
| --- | --- |
| enum('inherit', 'ltr', 'rtl') | No |

---

### display​

`display` sets the display type of this component.

It works similarly to `display` in CSS but only supports the values 'flex', 'none', and 'contents'. The default is `flex`.

| Type | Required |
| --- | --- |
| enum('none', 'flex', 'contents') | No |

---

### end​

When the direction is `ltr`, `end` is equivalent to `right`. When the direction is `rtl`, `end` is equivalent to `left`.

This style takes precedence over the `left` and `right` styles.

| Type | Required |
| --- | --- |
| number, string | No |

---

### flex​

In React Native `flex` does not work the same way that it does in CSS. `flex` is a number rather than a string, and it works according to the [Yoga](https://github.com/facebook/yoga) layout engine.

When `flex` is a positive number, it makes the component flexible, and it will be sized proportional to its flex value. So a component with `flex` set to `2` will take twice the space as a component with `flex` set to 1. `flex: <positive number>` equates to `flexGrow: <positive number>, flexShrink: 1, flexBasis: 0`.

When `flex` is `0`, the component is sized according to `width` and `height`, and it is inflexible.

When `flex` is `-1`, the component is normally sized according to `width` and `height`. However, if there's not enough space, the component will shrink to its `minWidth` and `minHeight`.

`flexGrow`, `flexShrink`, and `flexBasis` work the same as in CSS.

| Type | Required |
| --- | --- |
| number | No |

---

### flexBasis​

`flexBasis` is an axis-independent way of providing the default size of an item along the main axis. Setting the `flexBasis` of a child is similar to setting the `width` of that child if its parent is a container with `flexDirection: row` or setting the `height` of a child if its parent is a container with `flexDirection: column`. The `flexBasis` of an item is the default size of that item, the size of the item before any `flexGrow` and `flexShrink` calculations are performed.

| Type | Required |
| --- | --- |
| number, string | No |

---

### flexDirection​

`flexDirection` controls which directions children of a container go. `row` goes left to right, `column` goes top to bottom, and you may be able to guess what the other two do. It works like `flex-direction` in CSS, except the default is `column`.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction) for more details.

| Type | Required |
| --- | --- |
| enum('row', 'row-reverse', 'column', 'column-reverse') | No |

---

### flexGrow​

`flexGrow` describes how any space within a container should be distributed among its children along the main axis. After laying out its children, a container will distribute any remaining space according to the flex grow values specified by its children.

`flexGrow` accepts any floating point value >= 0, with 0 being the default value. A container will distribute any remaining space among its children weighted by the children’s `flexGrow` values.

| Type | Required |
| --- | --- |
| number | No |

---

### flexShrink​

[flexShrink](https://reactnative.dev/docs/layout-props#flexshrink) describes how to shrink children along the main axis in the case in which the total size of the children overflows the size of the container on the main axis. `flexShrink` is very similar to `flexGrow` and can be thought of in the same way if any overflowing size is considered to be negative remaining space. These two properties also work well together by allowing children to grow and shrink as needed.

`flexShrink` accepts any floating point value >= 0, with 0 being the default value. A container will shrink its children weighted by the children’s `flexShrink` values.

| Type | Required |
| --- | --- |
| number | No |

---

### flexWrap​

`flexWrap` controls whether children can wrap around after they hit the end of a flex container. It works like `flex-wrap` in CSS (default: nowrap).

Note it does not work anymore with `alignItems: stretch` (the default), so you may want to use `alignItems: flex-start` for example (breaking change details: [https://github.com/facebook/react-native/releases/tag/v0.28.0](https://github.com/facebook/react-native/releases/tag/v0.28.0)).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/flex-wrap) for more details.

| Type | Required |
| --- | --- |
| enum('wrap', 'nowrap', 'wrap-reverse') | No |

---

### gap​

`gap` works like `gap` in CSS. Only pixel units are supported in React Native.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/gap) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### height​

`height` sets the height of this component.

It works similarly to `height` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/height) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### inset​

 note

`inset` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Setting `inset` has the same effect as setting each of `top`, `bottom`, `right` and `left` props.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/inset) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetBlock​

 note

`insetBlock` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Equivalent to [top](https://reactnative.dev/docs/layout-props#top) and [bottom](https://reactnative.dev/docs/layout-props#bottom).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-block) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetBlockEnd​

 note

`insetBlockEnd` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Equivalent to [bottom](https://reactnative.dev/docs/layout-props#bottom).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-block-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetBlockStart​

 note

`insetBlockStart` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Equivalent to [top](https://reactnative.dev/docs/layout-props#top).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-block-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetInline​

 note

`insetInline` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

Equivalent to [right](https://reactnative.dev/docs/layout-props#right) and [left](https://reactnative.dev/docs/layout-props#left).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-inline) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetInlineEnd​

 note

`insetInlineEnd` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

When direction is `ltr`, `insetInlineEnd` is equivalent to [right](https://reactnative.dev/docs/layout-props#right). When direction is `rtl`, `insetInlineEnd` is equivalent to [left](https://reactnative.dev/docs/layout-props#left).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-inline-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### insetInlineStart​

 note

`insetInlineStart` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

When direction is `ltr`, `insetInlineStart` is equivalent to [left](https://reactnative.dev/docs/layout-props#left). When direction is `rtl`, `insetInlineStart` is equivalent to [right](https://reactnative.dev/docs/layout-props#right).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/inset-inline-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### isolation​

 note

`isolation` is only available on the [New Architecture](https://reactnative.dev/architecture/landing-page)

`isolation` lets you form a [stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Stacking_context).

There are two values:

- `auto` (default): Does nothing.
- `isolate`: Forms a stacking context.

| Type | Required |
| --- | --- |
| enum('auto', 'isolate') | No |

---

### justifyContent​

`justifyContent` aligns children in the main direction. For example, if children are flowing vertically, `justifyContent` controls how they align vertically. It works like `justify-content` in CSS (default: flex-start).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/justify-content) for more details.

| Type | Required |
| --- | --- |
| enum('flex-start', 'flex-end', 'center', 'space-between', 'space-around', 'space-evenly') | No |

---

### left​

`left` is the number of logical pixels to offset the left edge of this component.

It works similarly to `left` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/left) for more details of how `left` affects layout.

| Type | Required |
| --- | --- |
| number, string | No |

---

### margin​

Setting `margin` has the same effect as setting each of `marginTop`, `marginLeft`, `marginBottom`, and `marginRight`.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/margin) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginBottom​

`marginBottom` works like `margin-bottom` in CSS. See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/margin-bottom) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginBlock​

Equivalent to [marginVertical](https://reactnative.dev/docs/layout-props#marginvertical).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-block) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginBlockEnd​

Equivalent to [marginBottom](https://reactnative.dev/docs/layout-props#marginbottom).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-block-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginBlockStart​

Equivalent to [marginTop](https://reactnative.dev/docs/layout-props#margintop).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-block-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginEnd​

When direction is `ltr`, `marginEnd` is equivalent to `marginRight`. When direction is `rtl`, `marginEnd` is equivalent to `marginLeft`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginHorizontal​

Setting `marginHorizontal` has the same effect as setting both `marginLeft` and `marginRight`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginInline​

Equivalent to [marginHorizontal](https://reactnative.dev/docs/layout-props#marginhorizontal).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-inline) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginInlineEnd​

When direction is `ltr`, `marginInlineEnd` is equivalent to [marginEnd](https://reactnative.dev/docs/layout-props#marginend) (i.e. `marginRight`). When direction is `rtl`, `marginInlineEnd` is equivalent to [marginEnd](https://reactnative.dev/docs/layout-props#marginend) (i.e. `marginLeft`).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-inline-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginInlineStart​

When direction is `ltr`, `marginInlineStart` is equivalent to [marginStart](https://reactnative.dev/docs/layout-props#marginstart) (i.e. `marginLeft`). When direction is `rtl`, `marginInlineStart` is equivalent to [marginStart](https://reactnative.dev/docs/layout-props#marginstart) (i.e. `marginRight`).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/margin-inline-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginLeft​

`marginLeft` works like `margin-left` in CSS. See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/margin-left) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginRight​

`marginRight` works like `margin-right` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/margin-right) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginStart​

When direction is `ltr`, `marginStart` is equivalent to `marginLeft`. When direction is `rtl`, `marginStart` is equivalent to `marginRight`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginTop​

`marginTop` works like `margin-top` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/margin-top) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### marginVertical​

Setting `marginVertical` has the same effect as setting both `marginTop` and `marginBottom`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### maxHeight​

`maxHeight` is the maximum height for this component, in logical pixels.

It works similarly to `max-height` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/max-height) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### maxWidth​

`maxWidth` is the maximum width for this component, in logical pixels.

It works similarly to `max-width` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/max-width) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### minHeight​

`minHeight` is the minimum height for this component, in logical pixels.

It works similarly to `min-height` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/min-height) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### minWidth​

`minWidth` is the minimum width for this component, in logical pixels.

It works similarly to `min-width` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### overflow​

`overflow` controls how children are measured and displayed. `overflow: hidden` causes views to be clipped while `overflow: scroll` causes views to be measured independently of their parents' main axis. It works like `overflow` in CSS (default: visible).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow) for more details.

| Type | Required |
| --- | --- |
| enum('visible', 'hidden', 'scroll') | No |

---

### padding​

Setting `padding` has the same effect as setting each of `paddingTop`, `paddingBottom`, `paddingLeft`, and `paddingRight`.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/padding) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingBottom​

`paddingBottom` works like `padding-bottom` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/padding-bottom) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingBlock​

Equivalent to [paddingVertical](https://reactnative.dev/docs/layout-props#paddingvertical).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-block) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingBlockEnd​

Equivalent to [paddingBottom](https://reactnative.dev/docs/layout-props#paddingbottom).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-block-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingBlockStart​

Equivalent to [paddingTop](https://reactnative.dev/docs/layout-props#paddingtop).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-block-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingEnd​

When direction is `ltr`, `paddingEnd` is equivalent to `paddingRight`. When direction is `rtl`, `paddingEnd` is equivalent to `paddingLeft`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingHorizontal​

Setting `paddingHorizontal` is like setting both of `paddingLeft` and `paddingRight`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingInline​

Equivalent to [paddingHorizontal](https://reactnative.dev/docs/layout-props#paddinghorizontal).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-inline) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingInlineEnd​

When direction is `ltr`, `paddingInlineEnd` is equivalent to [paddingEnd](https://reactnative.dev/docs/layout-props#paddingend) (i.e. `paddingRight`). When direction is `rtl`, `paddingInlineEnd` is equivalent to [paddingEnd](https://reactnative.dev/docs/layout-props#paddingend) (i.e. `paddingLeft`).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-inline-end) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingInlineStart​

When direction is `ltr`, `paddingInlineStart` is equivalent to [paddingStart](https://reactnative.dev/docs/layout-props#paddingstart) (i.e. `paddingLeft`). When direction is `rtl`, `paddingInlineStart` is equivalent to [paddingStart](https://reactnative.dev/docs/layout-props#paddingstart) (i.e. `paddingRight`).

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/padding-inline-start) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingLeft​

`paddingLeft` works like `padding-left` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/padding-left) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingRight​

`paddingRight` works like `padding-right` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/padding-right) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingStart​

When direction is `ltr`, `paddingStart` is equivalent to `paddingLeft`. When direction is `rtl`, `paddingStart` is equivalent to `paddingRight`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingTop​

`paddingTop` works like `padding-top` in CSS.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/padding-top) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### paddingVertical​

Setting `paddingVertical` is like setting both of `paddingTop` and `paddingBottom`.

| Type | Required |
| --- | --- |
| number, string | No |

---

### position​

`position` in React Native is similar to [regular CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/position), but everything is set to `relative` by default.

`relative` will position an element according to the normal flow of the layout. Insets (`top`, `bottom`, `left`, `right`) will offset relative to this layout.

`absolute` takes the element out of the normal flow of the layout. Insets will offset relative to its [containing block](https://reactnative.dev/docs/flexbox#the-containing-block).

`static` will position an element according to the normal flow of the layout. Insets will have no effect.
`static` elements do not form a containing block for absolute descendants.

For more information, see the [Layout with Flexbox docs](https://reactnative.dev/docs/flexbox#position). Also, [the Yoga documentation](https://www.yogalayout.dev/docs/styling/position) has more details on how `position` differs between React Native and CSS.

| Type | Required |
| --- | --- |
| enum('absolute', 'relative', 'static') | No |

---

### right​

`right` is the number of logical pixels to offset the right edge of this component.

It works similarly to `right` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/right) for more details of how `right` affects layout.

| Type | Required |
| --- | --- |
| number, string | No |

---

### rowGap​

`rowGap` works like `row-gap` in CSS. Only pixel units are supported in React Native.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/row-gap) for more details.

| Type | Required |
| --- | --- |
| number | No |

---

### start​

When the direction is `ltr`, `start` is equivalent to `left`. When the direction is `rtl`, `start` is equivalent to `right`.

This style takes precedence over the `left`, `right`, and `end` styles.

| Type | Required |
| --- | --- |
| number, string | No |

---

### top​

`top` is the number of logical pixels to offset the top edge of this component.

It works similarly to `top` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/top) for more details of how `top` affects layout.

| Type | Required |
| --- | --- |
| number, string | No |

---

### width​

`width` sets the width of this component.

It works similarly to `width` in CSS, but in React Native you must use points or percentages. Ems and other units are not supported.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/width) for more details.

| Type | Required |
| --- | --- |
| number, string | No |

---

### zIndex​

`zIndex` controls which components display on top of others. Normally, you don't use `zIndex`. Components render according to their order in the document tree, so later components draw over earlier ones. `zIndex` may be useful if you have animations or custom modal interfaces where you don't want this behavior.

It works like the CSS `z-index` property - components with a larger `zIndex` will render on top. Think of the z-direction like it's pointing from the phone into your eyeball.

On iOS, `zIndex` may require `View`s to be siblings of each other for it to work as expected.

See [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/z-index) for more details.

| Type | Required |
| --- | --- |
| number | No |

Is this page useful?

---

# LayoutAnimation

> Automatically animates views to their new positions when the next layout happens.

Automatically animates views to their new positions when the next layout happens.

A common way to use this API is to call it before updating the state hook in functional components and calling `setState` in class components.

Note that in order to get this to work on **Android** you need to set the following flags via `UIManager`:

 js

```
if (Platform.OS === 'android') {  if (UIManager.setLayoutAnimationEnabledExperimental) {    UIManager.setLayoutAnimationEnabledExperimental(true);  }}
```

## Example​

---

# Reference

## Methods​

### configureNext()​

 tsx

```
static configureNext(  config: LayoutAnimationConfig,  onAnimationDidEnd?: () => void,  onAnimationDidFail?: () => void,);
```

Schedules an animation to happen on the next layout.

#### Parameters:​

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| config | object | Yes | See config description below. |
| onAnimationDidEnd | function | No | Called when the animation finished. |
| onAnimationDidFail | function | No | Called when the animation failed. |

The `config` parameter is an object with the keys below. [create](https://reactnative.dev/docs/layoutanimation#create) returns a valid object for `config`, and the [Presets](https://reactnative.dev/docs/layoutanimation#presets) objects can also all be passed as the `config`.

- `duration` in milliseconds
- `create`, optional config for animating in new views
- `update`, optional config for animating views that have been updated
- `delete`, optional config for animating views as they are removed

The config that's passed to `create`, `update`, or `delete` has the following keys:

- `type`, the [animation type](https://reactnative.dev/docs/layoutanimation#types) to use
- `property`, the [layout property](https://reactnative.dev/docs/layoutanimation#properties) to animate (optional, but recommended for `create` and `delete`)
- `springDamping` (number, optional and only for use with `type: Type.spring`)
- `initialVelocity` (number, optional)
- `delay` (number, optional)
- `duration` (number, optional)

---

### create()​

 tsx

```
static create(duration, type, creationProp)
```

Helper that creates an object (with `create`, `update`, and `delete` fields) to pass into [configureNext](https://reactnative.dev/docs/layoutanimation#configurenext). The `type` parameter is an [animation type](https://reactnative.dev/docs/layoutanimation#types), and the `creationProp` parameter is a [layout property](https://reactnative.dev/docs/layoutanimation#properties).

**Example:**

## Properties​

### Types​

An enumeration of animation types to be used in the [create](https://reactnative.dev/docs/layoutanimation#create) method, or in the `create`/`update`/`delete` configs for [configureNext](https://reactnative.dev/docs/layoutanimation#configurenext). (example usage: `LayoutAnimation.Types.easeIn`)

| Types |
| --- |
| spring |
| linear |
| easeInEaseOut |
| easeIn |
| easeOut |
| keyboard |

---

### Properties​

An enumeration of layout properties to be animated to be used in the [create](https://reactnative.dev/docs/layoutanimation#create) method, or in the `create`/`update`/`delete` configs for [configureNext](https://reactnative.dev/docs/layoutanimation#configurenext). (example usage: `LayoutAnimation.Properties.opacity`)

| Properties |
| --- |
| opacity |
| scaleX |
| scaleY |
| scaleXY |

---

### Presets​

A set of predefined animation configs to pass into [configureNext](https://reactnative.dev/docs/layoutanimation#configurenext).

| Presets | Value |
| --- | --- |
| easeInEaseOut | create(300, 'easeInEaseOut', 'opacity') |
| linear | create(500, 'linear', 'opacity') |
| spring | {duration: 700, create: {type: 'linear', property: 'opacity'}, update: {type: 'spring', springDamping: 0.4}, delete: {type: 'linear', property: 'opacity'} } |

---

### easeInEaseOut​

Calls `configureNext()` with `Presets.easeInEaseOut`.

---

### linear​

Calls `configureNext()` with `Presets.linear`.

---

### spring​

Calls `configureNext()` with `Presets.spring`.

**Example:**

 Is this page useful?

---

# LayoutEvent Object Type

> LayoutEvent object is returned in the callback as a result of component layout change, for example onLayout in View component.

`LayoutEvent` object is returned in the callback as a result of component layout change, for example `onLayout` in [View](https://reactnative.dev/docs/view) component.

## Example​

 js

```
{    layout: {        width: 520,        height: 70.5,        x: 0,        y: 42.5    },    target: 1127}
```

## Keys and values​

### height​

Height of the component after the layout changes.

| Type | Optional |
| --- | --- |
| number | No |

### width​

Width of the component after the layout changes.

| Type | Optional |
| --- | --- |
| number | No |

### x​

Component X coordinate inside the parent component.

| Type | Optional |
| --- | --- |
| number | No |

### y​

Component Y coordinate inside the parent component.

| Type | Optional |
| --- | --- |
| number | No |

### target​

The node id of the element receiving the LayoutEvent.

| Type | Optional |
| --- | --- |
| number,null,undefined | No |

## Used by​

- [Image](https://reactnative.dev/docs/image)
- [Pressable](https://reactnative.dev/docs/pressable)
- [ScrollView](https://reactnative.dev/docs/scrollview)
- [Text](https://reactnative.dev/docs/text)
- [TextInput](https://reactnative.dev/docs/textinput)
- [TouchableWithoutFeedback](https://reactnative.dev/docs/touchablewithoutfeedback)
- [View](https://reactnative.dev/docs/view)

Is this page useful?

---

# Using Libraries

> This guide introduces React Native developers to finding, installing, and using third-party libraries in their apps.

React Native provides a set of built-in [Core Components and APIs](https://reactnative.dev/docs/components-and-apis) ready to use in your app. You're not limited to the components and APIs bundled with React Native. React Native has a community of thousands of developers. If the Core Components and APIs don't have what you are looking for, you may be able to find and install a library from the community to add the functionality to your app.

## Selecting a Package Manager​

React Native libraries are typically installed from the [npm registry](https://www.npmjs.com/) using a Node.js package manager such as [npm CLI](https://docs.npmjs.com/cli/npm) or [Yarn Classic](https://classic.yarnpkg.com/en/).

If you have Node.js installed on your computer then you already have the npm CLI installed. Some developers prefer to use Yarn Classic for slightly faster install times and additional advanced features like Workspaces. Both tools work great with React Native. We will assume npm for the rest of this guide for simplicity of explanation.

 note

The terms "library" and "package" are used interchangeably in the JavaScript community.

## Installing a Library​

To install a library in your project, navigate to your project directory in your terminal and run the installation command. Let's try this with `react-native-webview`:

shell

```
npm install react-native-webview
```

shell

```
yarn add react-native-webview
```

The library that we installed includes native code, and we need to link to our app before we use it.

## Linking Native Code on iOS​

React Native uses CocoaPods to manage iOS project dependencies and most React Native libraries follow this same convention. If a library you are using does not, then please refer to their README for additional instruction. In most cases, the following instructions will apply.

Run `pod install` in our `ios` directory in order to link it to our native iOS project. A shortcut for doing this without switching to the `ios` directory is to run `npx pod-install`.

 bash

```
npx pod-install
```

Once this is complete, re-build the app binary to start using your new library:

shell

```
npm run ios
```

shell

```
yarn ios
```

## Linking Native Code on Android​

React Native uses Gradle to manage Android project dependencies. After you install a library with native dependencies, you will need to re-build the app binary to use your new library:

shell

```
npm run android
```

shell

```
yarn android
```

## Finding Libraries​

[React Native Directory](https://reactnative.directory) is a searchable database of libraries built specifically for React Native. This is the first place to look for a library for your React Native app.

Many of the libraries you will find on the directory are from [React Native Community](https://github.com/react-native-community/) or [Expo](https://docs.expo.dev/versions/latest/).

Libraries built by the React Native Community are driven by volunteers and individuals at companies that depend on React Native. They often support iOS, tvOS, Android, Windows, but this varies across projects. Many of the libraries in this organization were once React Native Core Components and APIs.

Libraries built by Expo are all written in TypeScript and support iOS, Android, and `react-native-web` wherever possible.

After React Native Directory, the [npm registry](https://www.npmjs.com/) is the next best place if you can't find a library specifically for React Native on the directory. The npm registry is the definitive source for JavaScript libraries, but the libraries that it lists may not all be compatible with React Native. React Native is one of many JavaScript programming environments, including Node.js, web browsers, Electron, and more, and npm includes libraries that work for all of these environments.

## Determining Library Compatibility​

### Does it work with React Native?​

Usually libraries built *specifically for other platforms* will not work with React Native. Examples include `react-select` which is built for the web and specifically targets `react-dom`, and `rimraf` which is built for Node.js and interacts with your computer file system. Other libraries like `lodash` use only JavaScript language features and work in any environment. You will gain a sense for this over time, but until then the easiest way to find out is to try it yourself. You can remove packages using `npm uninstall` if it turns out that it does not work in React Native.

### Does it work for the platforms that my app supports?​

[React Native Directory](https://reactnative.directory) allows you to filter by platform compatibility, such as iOS, Android, Web, and Windows. If the library you would like to use is not currently listed there, refer to the README for the library to learn more.

### Does it work with my app version of React Native?​

The latest version of a library is typically compatible with the latest version of React Native. If you are using an older version, you should refer to the README to know which version of the library you should install. You can install a particular version of the library by running `npm install <library-name>@<version-number>`, for example: `npm install @react-native-community/netinfo@^2.0.0`.

Is this page useful?

---

# Linking Libraries

> Not every app uses all the native capabilities, and including the code to support all those features would impact the binary size... But we still want to support adding these features whenever you need them.

Not every app uses all the native capabilities, and including the code to support all those features would impact the binary size... But we still want to support adding these features whenever you need them.

With that in mind we exposed many of these features as independent static libraries.

For most of the libs it will be as quick as dragging two files, sometimes a third step will be necessary, but no more than that.

 note

All the libraries we ship with React Native live in the `Libraries` folder in the root of the repository. Some of them are pure JavaScript, and you only need to `require` it.
Other libraries also rely on some native code, in that case you'll have to add these files to your app, otherwise the app will throw an error as soon as you try to use the library.

## Here are the few steps to link your libraries that contain native code​

### Automatic linking​

Install a library with native dependencies:

 shell

```
npm install <library-with-native-dependencies> --save
```

 info

`--save` or `--save-dev` flag is very important for this step. React Native will link your libs based on `dependencies` and `devDependencies` in your `package.json` file.

That's it! Next time you build your app the native code will be linked thanks to the [autolinking](https://github.com/react-native-community/cli/blob/main/docs/autolinking.md) mechanism.

### Manual linking​

#### Step 1​

If the library has native code, there must be an `.xcodeproj` file inside its folder. Drag this file to your project on Xcode (usually under the `Libraries` group on Xcode);

![image](https://reactnative.dev/assets/images/AddToLibraries-92a6a7f58c75a8344d9bbeeae4ac167b.png)

#### Step 2​

Click on your main project file (the one that represents the `.xcodeproj`) select `Build Phases` and drag the static library from the `Products` folder inside the Library you are importing to `Link Binary With Libraries`

![image](https://reactnative.dev/assets/images/AddToBuildPhases-3e79422ff24780db618eae2d7a5ea604.png)

#### Step 3​

Not every library will need this step, what you need to consider is:

*Do I need to know the contents of the library at compile time?*

What that means is, are you using this library on the native side or only in JavaScript? If you are only using it in JavaScript, you are good to go!

If you do need to call it from native, then we need to know the library's headers. To achieve that you have to go to your project's file, select `Build Settings` and search for `Header Search Paths`. There you should include the path to your library. (This documentation used to recommend using `recursive`, but this is no longer recommended, as it can cause subtle build failures, especially with CocoaPods.)

![image](https://reactnative.dev/assets/images/AddToSearchPaths-721692ba7f3a91a1f4e4f73e7d88f2ca.png)

Is this page useful?
