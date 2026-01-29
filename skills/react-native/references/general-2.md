# Alert and more

# Alert

> Launches an alert dialog with the specified title and message.

Launches an alert dialog with the specified title and message.

Optionally provide a list of buttons. Tapping any button will fire the respective onPress callback and dismiss the alert. By default, the only button will be an 'OK' button.

This is an API that works both on Android and iOS and can show static alerts. Alert that prompts the user to enter some information is available on iOS only.

## Example​

## iOS​

On iOS you can specify any number of buttons. Each button can optionally specify a style or be emphasized, available options are represented by the [AlertButtonStyle](#alertbuttonstyle-ios) enum and the `isPreferred` field on [AlertButton](https://reactnative.dev/docs/alert#alertbutton).

## Android​

On Android at most three buttons can be specified. Android has a concept of a neutral, negative and a positive button:

- If you specify one button, it will be the 'positive' one (such as 'OK')
- Two buttons mean 'negative', 'positive' (such as 'Cancel', 'OK')
- Three buttons mean 'neutral', 'negative', 'positive' (such as 'Later', 'Cancel', 'OK')

Alerts on Android can be dismissed by tapping outside of the alert box. It is disabled by default and can be enabled by providing an optional [AlertOptions](https://reactnative.dev/docs/alert#alertoptions) parameter with the cancelable property set to `true` i.e.
`{cancelable: true}`.

The cancel event can be handled by providing an `onDismiss` callback property inside the `options` parameter.

### ExampleAndroid​

---

# Reference

## Methods​

### alert()​

 tsx

```
static alert (  title: string,  message?: string,  buttons?: AlertButton[],  options?: AlertOptions,);
```

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| titleRequired | string | The dialog's title. Passingnullor empty string will hide the title. |
| message | string | An optional message that appears below the dialog's title. |
| buttons | AlertButton[] | An optional array containing buttons configuration. |
| options | AlertOptions | An optional Alert configuration. |

---

### prompt()iOS​

 tsx

```
static prompt: (  title: string,  message?: string,  callbackOrButtons?: ((text: string) => void) | AlertButton[],  type?: AlertType,  defaultValue?: string,  keyboardType?: string,);
```

Create and display a prompt to enter some text in form of Alert.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| titleRequired | string | The dialog's title. |
| message | string | An optional message that appears above the text input. |
| callbackOrButtons | functionAlertButton[] | If passed a function, it will be called with the prompt's value(text: string) => void, when the user taps 'OK'.If passed an array, buttons will be configured based on the array content. |
| type | AlertType | This configures the text input. |
| defaultValue | string | The default text in text input. |
| keyboardType | string | The keyboard type of first text field (if exists). One of TextInputkeyboardTypes. |
| options | AlertOptions | An optional Alert configuration. |

---

## Type Definitions​

### AlertButtonStyleiOS​

An iOS Alert button style.

| Type |
| --- |
| enum |

**Constants:**

| Value | Description |
| --- | --- |
| 'default' | Default button style. |
| 'cancel' | Cancel button style. |
| 'destructive' | Destructive button style. |

---

### AlertTypeiOS​

An iOS Alert type.

| Type |
| --- |
| enum |

**Constants:**

| Value | Description |
| --- | --- |
| 'default' | Default alert with no inputs |
| 'plain-text' | Plain text input alert |
| 'secure-text' | Secure text input alert |
| 'login-password' | Login and password alert |

---

### AlertButton​

An object describing the configuration of a button in the alert.

| Type |
| --- |
| array of objects |

**Objects properties:**

| Name | Type | Description |
| --- | --- | --- |
| text | string | Button label. |
| onPress | function | Callback function when button is pressed. |
| styleiOS | AlertButtonStyle | Button style, on Android this property will be ignored. |
| isPreferrediOS | boolean | Whether button should be emphasized, on Android this property will be ignored. |

---

### AlertOptions​

| Type |
| --- |
| object |

**Properties:**

| Name | Type | Description |
| --- | --- | --- |
| cancelableAndroid | boolean | Defines if alert can be dismissed by tapping outside of the alert box. |
| userInterfaceStyleiOS | string | The interface style used for the alert, can be set tolightordark, otherwise the default system style will be used. |
| onDismissAndroid | function | Callback function fired when alert has been dismissed. |

Is this page useful?

---

# Animated

> The Animated library is designed to make animations fluid, powerful, and painless to build and maintain. Animated focuses on declarative relationships between inputs and outputs, configurable transforms in between, and start/stop methods to control time-based animation execution.

The `Animated` library is designed to make animations fluid, powerful, and painless to build and maintain. `Animated` focuses on declarative relationships between inputs and outputs, configurable transforms in between, and `start`/`stop` methods to control time-based animation execution.

The core workflow for creating an animation is to create an `Animated.Value`, hook it up to one or more style attributes of an animated component, and then drive updates via animations using `Animated.timing()`.

 note

Don't modify the animated value directly. You can use the [useRefHook](https://react.dev/reference/react/useRef) to return a mutable ref object. This ref object's `current` property is initialized as the given argument and persists throughout the component lifecycle.

## Example​

The following example contains a `View` which will fade in and fade out based on the animated value `fadeAnim`

Refer to the [Animations](https://reactnative.dev/docs/animations#animated-api) guide to see additional examples of `Animated` in action.

## Overview​

There are two value types you can use with `Animated`:

- [Animated.Value()](https://reactnative.dev/docs/animated#value) for single values
- [Animated.ValueXY()](https://reactnative.dev/docs/animated#valuexy) for vectors

`Animated.Value` can bind to style properties or other props, and can be interpolated as well. A single `Animated.Value` can drive any number of properties.

### Configuring animations​

`Animated` provides three types of animation types. Each animation type provides a particular animation curve that controls how your values animate from their initial value to the final value:

- [Animated.decay()](https://reactnative.dev/docs/animated#decay) starts with an initial velocity and gradually slows to a stop.
- [Animated.spring()](https://reactnative.dev/docs/animated#spring) provides a basic spring physics model.
- [Animated.timing()](https://reactnative.dev/docs/animated#timing) animates a value over time using [easing functions](https://reactnative.dev/docs/easing).

In most cases, you will be using `timing()`. By default, it uses a symmetric easeInOut curve that conveys the gradual acceleration of an object to full speed and concludes by gradually decelerating to a stop.

### Working with animations​

Animations are started by calling `start()` on your animation. `start()` takes a completion callback that will be called when the animation is done. If the animation finished running normally, the completion callback will be invoked with `{finished: true}`. If the animation is done because `stop()` was called on it before it could finish (e.g. because it was interrupted by a gesture or another animation), then it will receive `{finished: false}`.

 tsx

```
Animated.timing({}).start(({finished}) => {  /* completion callback */});
```

### Using the native driver​

By using the native driver, we send everything about the animation to native before starting the animation, allowing native code to perform the animation on the UI thread without having to go through the bridge on every frame. Once the animation has started, the JS thread can be blocked without affecting the animation.

You can use the native driver by specifying `useNativeDriver: true` in your animation configuration. See the [Animations](https://reactnative.dev/docs/animations#using-the-native-driver) guide to learn more.

### Animatable components​

Only animatable components can be animated. These unique components do the magic of binding the animated values to the properties, and do targeted native updates to avoid the cost of the React render and reconciliation process on every frame. They also handle cleanup on unmount so they are safe by default.

- [createAnimatedComponent()](https://reactnative.dev/docs/animated#createanimatedcomponent) can be used to make a component animatable.

`Animated` exports the following animatable components using the above wrapper:

- `Animated.Image`
- `Animated.ScrollView`
- `Animated.Text`
- `Animated.View`
- `Animated.FlatList`
- `Animated.SectionList`

### Composing animations​

Animations can also be combined in complex ways using composition functions:

- [Animated.delay()](https://reactnative.dev/docs/animated#delay) starts an animation after a given delay.
- [Animated.parallel()](https://reactnative.dev/docs/animated#parallel) starts a number of animations at the same time.
- [Animated.sequence()](https://reactnative.dev/docs/animated#sequence) starts the animations in order, waiting for each to complete before starting the next.
- [Animated.stagger()](https://reactnative.dev/docs/animated#stagger) starts animations in order and in parallel, but with successive delays.

Animations can also be chained together by setting the `toValue` of one animation to be another `Animated.Value`. See [Tracking dynamic values](https://reactnative.dev/docs/animations#tracking-dynamic-values) in the Animations guide.

By default, if one animation is stopped or interrupted, then all other animations in the group are also stopped.

### Combining animated values​

You can combine two animated values via addition, subtraction, multiplication, division, or modulo to make a new animated value:

- [Animated.add()](https://reactnative.dev/docs/animated#add)
- [Animated.subtract()](https://reactnative.dev/docs/animated#subtract)
- [Animated.divide()](https://reactnative.dev/docs/animated#divide)
- [Animated.modulo()](https://reactnative.dev/docs/animated#modulo)
- [Animated.multiply()](https://reactnative.dev/docs/animated#multiply)

### Interpolation​

The `interpolate()` function allows input ranges to map to different output ranges. By default, it will extrapolate the curve beyond the ranges given, but you can also have it clamp the output value. It uses linear interpolation by default but also supports easing functions.

- [interpolate()](https://reactnative.dev/docs/animatedvalue#interpolate)

Read more about interpolation in the [Animation](https://reactnative.dev/docs/animations#interpolation) guide.

### Handling gestures and other events​

Gestures, like panning or scrolling, and other events can map directly to animated values using `Animated.event()`. This is done with a structured map syntax so that values can be extracted from complex event objects. The first level is an array to allow mapping across multiple args, and that array contains nested objects.

- [Animated.event()](https://reactnative.dev/docs/animated#event)

For example, when working with horizontal scrolling gestures, you would do the following in order to map `event.nativeEvent.contentOffset.x` to `scrollX` (an `Animated.Value`):

 tsx

```
onScroll={Animated.event(   // scrollX = e.nativeEvent.contentOffset.x   [{nativeEvent: {        contentOffset: {          x: scrollX        }      }    }] )}
```

---

# Reference

## Methods​

When the given value is a ValueXY instead of a Value, each config option may be a vector of the form `{x: ..., y: ...}` instead of a scalar.

### decay()​

 tsx

```
static decay(value, config): CompositeAnimation;
```

Animates a value from an initial velocity to zero based on a decay coefficient.

Config is an object that may have the following options:

- `velocity`: Initial velocity. Required.
- `deceleration`: Rate of decay. Default 0.997.
- `isInteraction`: Whether or not this animation creates an "interaction handle" on the `InteractionManager`. Default true.
- `useNativeDriver`: Uses the native driver when true. Required.

---

### timing()​

 tsx

```
static timing(value, config): CompositeAnimation;
```

Animates a value along a timed easing curve. The [Easing](https://reactnative.dev/docs/easing) module has tons of predefined curves, or you can use your own function.

Config is an object that may have the following options:

- `duration`: Length of animation (milliseconds). Default 500.
- `easing`: Easing function to define curve. Default is `Easing.inOut(Easing.ease)`.
- `delay`: Start the animation after delay (milliseconds). Default 0.
- `isInteraction`: Whether or not this animation creates an "interaction handle" on the `InteractionManager`. Default true.
- `useNativeDriver`: Uses the native driver when true. Required.

---

### spring()​

 tsx

```
static spring(value, config): CompositeAnimation;
```

Animates a value according to an analytical spring model based on [damped harmonic oscillation](https://en.wikipedia.org/wiki/Harmonic_oscillator#Damped_harmonic_oscillator). Tracks velocity state to create fluid motions as the `toValue` updates, and can be chained together.

Config is an object that may have the following options.

Note that you can only define one of bounciness/speed, tension/friction, or stiffness/damping/mass, but not more than one:

The friction/tension or bounciness/speed options match the spring model in [Facebook Pop](https://github.com/facebook/pop), [Rebound](https://github.com/facebookarchive/rebound), and [Origami](https://origami.design/).

- `friction`: Controls "bounciness"/overshoot. Default 7.
- `tension`: Controls speed. Default 40.
- `speed`: Controls speed of the animation. Default 12.
- `bounciness`: Controls bounciness. Default 8.

Specifying stiffness/damping/mass as parameters makes `Animated.spring` use an analytical spring model based on the motion equations of a [damped harmonic oscillator](https://en.wikipedia.org/wiki/Harmonic_oscillator#Damped_harmonic_oscillator). This behavior is slightly more precise and faithful to the physics behind spring dynamics, and closely mimics the implementation in iOS's CASpringAnimation.

- `stiffness`: The spring stiffness coefficient. Default 100.
- `damping`: Defines how the spring’s motion should be damped due to the forces of friction. Default 10.
- `mass`: The mass of the object attached to the end of the spring. Default 1.

Other configuration options are as follows:

- `velocity`: The initial velocity of the object attached to the spring. Default 0 (object is at rest).
- `overshootClamping`: Boolean indicating whether the spring should be clamped and not bounce. Default false.
- `restDisplacementThreshold`: The threshold of displacement from rest below which the spring should be considered at rest. Default 0.001.
- `restSpeedThreshold`: The speed at which the spring should be considered at rest in pixels per second. Default 0.001.
- `delay`: Start the animation after delay (milliseconds). Default 0.
- `isInteraction`: Whether or not this animation creates an "interaction handle" on the `InteractionManager`. Default true.
- `useNativeDriver`: Uses the native driver when true. Required.

---

### add()​

 tsx

```
static add(a: Animated, b: Animated): AnimatedAddition;
```

Creates a new Animated value composed from two Animated values added together.

---

### subtract()​

 tsx

```
static subtract(a: Animated, b: Animated): AnimatedSubtraction;
```

Creates a new Animated value composed by subtracting the second Animated value from the first Animated value.

---

### divide()​

 tsx

```
static divide(a: Animated, b: Animated): AnimatedDivision;
```

Creates a new Animated value composed by dividing the first Animated value by the second Animated value.

---

### multiply()​

 tsx

```
static multiply(a: Animated, b: Animated): AnimatedMultiplication;
```

Creates a new Animated value composed from two Animated values multiplied together.

---

### modulo()​

 tsx

```
static modulo(a: Animated, modulus: number): AnimatedModulo;
```

Creates a new Animated value that is the (non-negative) modulo of the provided Animated value

---

### diffClamp()​

 tsx

```
static diffClamp(a: Animated, min: number, max: number): AnimatedDiffClamp;
```

Create a new Animated value that is limited between 2 values. It uses the difference between the last value so even if the value is far from the bounds it will start changing when the value starts getting closer again. (`value = clamp(value + diff, min, max)`).

This is useful with scroll events, for example, to show the navbar when scrolling up and to hide it when scrolling down.

---

### delay()​

 tsx

```
static delay(time: number): CompositeAnimation;
```

Starts an animation after the given delay.

---

### sequence()​

 tsx

```
static sequence(animations: CompositeAnimation[]): CompositeAnimation;
```

Starts an array of animations in order, waiting for each to complete before starting the next. If the current running animation is stopped, no following animations will be started.

---

### parallel()​

 tsx

```
static parallel(  animations: CompositeAnimation[],  config?: ParallelConfig): CompositeAnimation;
```

Starts an array of animations all at the same time. By default, if one of the animations is stopped, they will all be stopped. You can override this with the `stopTogether` flag.

---

### stagger()​

 tsx

```
static stagger(  time: number,  animations: CompositeAnimation[]): CompositeAnimation;
```

Array of animations may run in parallel (overlap), but are started in sequence with successive delays. Nice for doing trailing effects.

---

### loop()​

 tsx

```
static loop(  animation: CompositeAnimation[],  config?: LoopAnimationConfig): CompositeAnimation;
```

Loops a given animation continuously, so that each time it reaches the end, it resets and begins again from the start. Will loop without blocking the JS thread if the child animation is set to `useNativeDriver: true`. In addition, loops can prevent `VirtualizedList`-based components from rendering more rows while the animation is running. You can pass `isInteraction: false` in the child animation config to fix this.

Config is an object that may have the following options:

- `iterations`: Number of times the animation should loop. Default `-1` (infinite).

---

### event()​

 tsx

```
static event(  argMapping: Mapping[],  config?: EventConfig): (...args: any[]) => void;
```

Takes an array of mappings and extracts values from each arg accordingly, then calls `setValue` on the mapped outputs. e.g.

 tsx

```
onScroll={Animated.event(  [{nativeEvent: {contentOffset: {x: this._scrollX}}}],  {listener: (event: ScrollEvent) => console.log(event)}, // Optional async listener)} ...onPanResponderMove: Animated.event(  [    null, // raw event arg ignored    {dx: this._panX},  ], // gestureState arg  {    listener: (      event: GestureResponderEvent,      gestureState: PanResponderGestureState    ) => console.log(event, gestureState),  } // Optional async listener);
```

Config is an object that may have the following options:

- `listener`: Optional async listener.
- `useNativeDriver`: Uses the native driver when true. Required.

---

### forkEvent()​

 jsx

```
static forkEvent(event: AnimatedEvent, listener: Function): AnimatedEvent;
```

Advanced imperative API for snooping on animated events that are passed in through props. It permits to add a new javascript listener to an existing `AnimatedEvent`. If `animatedEvent` is a javascript listener, it will merge the 2 listeners into a single one, and if `animatedEvent` is null/undefined, it will assign the javascript listener directly. Use values directly where possible.

---

### unforkEvent()​

 jsx

```
static unforkEvent(event: AnimatedEvent, listener: Function);
```

---

### start()​

 tsx

```
static start(callback?: (result: {finished: boolean}) => void);
```

Animations are started by calling start() on your animation. start() takes a completion callback that will be called when the animation is done or when the animation is done because stop() was called on it before it could finish.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | (result: {finished: boolean}) => void | No | Function that will be called after the animation finished running normally or when the animation is done because stop() was called on it before it could finish |

Start example with callback:

 tsx

```
Animated.timing({}).start(({finished}) => {  /* completion callback */});
```

---

### stop()​

 tsx

```
static stop();
```

Stops any running animation.

---

### reset()​

 tsx

```
static reset();
```

Stops any running animation and resets the value to its original.

## Properties​

### Value​

Standard value class for driving animations. Typically initialized with `useAnimatedValue(0);` or `new Animated.Value(0);` in class components.

You can read more about `Animated.Value` API on the separate [page](https://reactnative.dev/docs/animatedvalue).

---

### ValueXY​

2D value class for driving 2D animations, such as pan gestures.

You can read more about `Animated.ValueXY` API on the separate [page](https://reactnative.dev/docs/animatedvaluexy).

---

### Interpolation​

Exported to use the Interpolation type in flow.

---

### Node​

Exported for ease of type checking. All animated values derive from this class.

---

### createAnimatedComponent​

Make any React component Animatable. Used to create `Animated.View`, etc.

---

### attachNativeEvent​

Imperative API to attach an animated value to an event on a view. Prefer using `Animated.event` with `useNativeDriver: true` if possible.

Is this page useful?

---

# Animated.Value

> Standard value for driving animations. One Animated.Value can drive multiple properties in a synchronized fashion, but can only be driven by one mechanism at a time. Using a new mechanism (e.g. starting a new animation, or calling setValue) will stop any previous ones.

Standard value for driving animations. One `Animated.Value` can drive multiple properties in a synchronized fashion, but can only be driven by one mechanism at a time. Using a new mechanism (e.g. starting a new animation, or calling `setValue`) will stop any previous ones.

Typically initialized with `useAnimatedValue(0);` or `new Animated.Value(0);` in class components.

---

# Reference

## Methods​

### setValue()​

 tsx

```
setValue(value: number);
```

Directly set the value. This will stop any animations running on the value and update all the bound properties.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| value | number | Yes | Value |

---

### setOffset()​

 tsx

```
setOffset(offset: number);
```

Sets an offset that is applied on top of whatever value is set, whether via `setValue`, an animation, or `Animated.event`. Useful for compensating things like the start of a pan gesture.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| offset | number | Yes | Offset value |

---

### flattenOffset()​

 tsx

```
flattenOffset();
```

Merges the offset value into the base value and resets the offset to zero. The final output of the value is unchanged.

---

### extractOffset()​

 tsx

```
extractOffset();
```

Sets the offset value to the base value, and resets the base value to zero. The final output of the value is unchanged.

---

### addListener()​

 tsx

```
addListener(callback: (state: {value: number}) => void): string;
```

Adds an asynchronous listener to the value so you can observe updates from animations. This is useful because there is no way to synchronously read the value because it might be driven natively.

Returns a string that serves as an identifier for the listener.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | Yes | The callback function which will receive an object with avaluekey set to the new value. |

---

### removeListener()​

 tsx

```
removeListener(id: string);
```

Unregister a listener. The `id` param shall match the identifier previously returned by `addListener()`.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| id | string | Yes | Id for the listener being removed. |

---

### removeAllListeners()​

 tsx

```
removeAllListeners();
```

Remove all registered listeners.

---

### stopAnimation()​

 tsx

```
stopAnimation(callback?: (value: number) => void);
```

Stops any running animation or tracking. `callback` is invoked with the final value after stopping the animation, which is useful for updating state to match the animation position with layout.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | No | A function that will receive the final value. |

---

### resetAnimation()​

 tsx

```
resetAnimation(callback?: (value: number) => void);
```

Stops any animation and resets the value to its original.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | No | A function that will receive the original value. |

---

### interpolate()​

 tsx

```
interpolate(config: InterpolationConfigType);
```

Interpolates the value before updating the property, e.g. mapping 0-1 to 0-10.

See `AnimatedInterpolation.js`

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| config | object | Yes | See below. |

The `config` object is composed of the following keys:

- `inputRange`: an array of numbers
- `outputRange`: an array of numbers or strings
- `easing` (optional): a function that returns a number, given an input number
- `extrapolate` (optional): a string such as 'extend', 'identity', or 'clamp'
- `extrapolateLeft` (optional): a string such as 'extend', 'identity', or 'clamp'
- `extrapolateRight` (optional): a string such as 'extend', 'identity', or 'clamp'

---

### animate()​

 tsx

```
animate(animation, callback);
```

Typically only used internally, but could be used by a custom Animation class.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| animation | Animation | Yes | SeeAnimation.js. |
| callback | function | Yes | Callback function. |

Is this page useful?

---

# Animated.ValueXY

> 2D Value for driving 2D animations, such as pan gestures. Almost identical API to normal Animated.Value, but multiplexed. Contains two regular Animated.Values under the hood.

2D Value for driving 2D animations, such as pan gestures. Almost identical API to normal [Animated.Value](https://reactnative.dev/docs/animatedvalue), but multiplexed. Contains two regular `Animated.Value`s under the hood.

## Example​

---

# Reference

## Methods​

### setValue()​

 tsx

```
setValue(value: {x: number; y: number});
```

Directly set the value. This will stop any animations running on the value and update all the bound properties.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| value | {x: number; y: number} | Yes | Value |

---

### setOffset()​

 tsx

```
setOffset(offset: {x: number; y: number});
```

Sets an offset that is applied on top of whatever value is set, whether via `setValue`, an animation, or `Animated.event`. Useful for compensating things like the start of a pan gesture.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| offset | {x: number; y: number} | Yes | Offset value |

---

### flattenOffset()​

 tsx

```
flattenOffset();
```

Merges the offset value into the base value and resets the offset to zero. The final output of the value is unchanged.

---

### extractOffset()​

 tsx

```
extractOffset();
```

Sets the offset value to the base value, and resets the base value to zero. The final output of the value is unchanged.

---

### addListener()​

 tsx

```
addListener(callback: (value: {x: number; y: number}) => void);
```

Adds an asynchronous listener to the value so you can observe updates from animations. This is useful because there is no way to synchronously read the value because it might be driven natively.

Returns a string that serves as an identifier for the listener.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | Yes | The callback function which will receive an object with avaluekey set to the new value. |

---

### removeListener()​

 tsx

```
removeListener(id: string);
```

Unregister a listener. The `id` param shall match the identifier previously returned by `addListener()`.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| id | string | Yes | Id for the listener being removed. |

---

### removeAllListeners()​

 tsx

```
removeAllListeners();
```

Remove all registered listeners.

---

### stopAnimation()​

 tsx

```
stopAnimation(callback?: (value: {x: number; y: number}) => void);
```

Stops any running animation or tracking. `callback` is invoked with the final value after stopping the animation, which is useful for updating state to match the animation position with layout.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | No | A function that will receive the final value. |

---

### resetAnimation()​

 tsx

```
resetAnimation(callback?: (value: {x: number; y: number}) => void);
```

Stops any animation and resets the value to its original.

**Parameters:**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| callback | function | No | A function that will receive the original value. |

---

### getLayout()​

 tsx

```
getLayout(): {left: Animated.Value, top: Animated.Value};
```

Converts `{x, y}` into `{left, top}` for use in style, e.g.

 tsx

```
style={this.state.anim.getLayout()}
```

---

### getTranslateTransform()​

 tsx

```
getTranslateTransform(): [  {translateX: Animated.Value},  {translateY: Animated.Value},];
```

Converts `{x, y}` into a useable translation transform, e.g.

 tsx

```
style={{  transform: this.state.anim.getTranslateTransform()}}
```

Is this page useful?
