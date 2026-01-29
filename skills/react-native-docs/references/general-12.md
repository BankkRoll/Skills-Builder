# React Fundamentals and more

# React Fundamentals

> To understand React Native fully, you need a solid foundation in React. This short introduction to React can help you get started or get refreshed.

React Native runs on [React](https://react.dev/), a popular open source library for building user interfaces with JavaScript. To make the most of React Native, it helps to understand React itself. This section can get you started or can serve as a refresher course.

We’re going to cover the core concepts behind React:

- components
- JSX
- props
- state

If you want to dig deeper, we encourage you to check out [React’s official documentation](https://react.dev/learn).

## Your first component​

The rest of this introduction to React uses cats in its examples: friendly, approachable creatures that need names and a cafe to work in. Here is your very first Cat component:

Here is how you do it: To define your `Cat` component, first use JavaScript’s [import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) to import React and React Native’s [Text](https://reactnative.dev/docs/next/text) Core Component:

 tsx

```
import React from 'react';import {Text} from 'react-native';
```

Your component starts as a function:

 tsx

```
const Cat = () => {};
```

You can think of components as blueprints. Whatever a function component returns is rendered as a **React element.** React elements let you describe what you want to see on the screen.

Here the `Cat` component will render a `<Text>` element:

 tsx

```
const Cat = () => {  return <Text>Hello, I am your cat!</Text>;};
```

You can export your function component with JavaScript’s [export default](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export) for use throughout your app like so:

 tsx

```
const Cat = () => {  return <Text>Hello, I am your cat!</Text>;};export default Cat;
```

 tip

This is one of many ways to export your component. This kind of export works well with the Snack Player. However, depending on your app’s file structure, you might need to use a different convention. This [handy cheatsheet on JavaScript imports and exports](https://medium.com/dailyjs/javascript-module-cheatsheet-7bd474f1d829) can help.

Now take a closer look at that `return` statement. `<Text>Hello, I am your cat!</Text>` is using a kind of JavaScript syntax that makes writing elements convenient: JSX.

## JSX​

React and React Native use **JSX,** a syntax that lets you write elements inside JavaScript like so: `<Text>Hello, I am your cat!</Text>`. The React docs have [a comprehensive guide to JSX](https://react.dev/learn/writing-markup-with-jsx) you can refer to learn even more. Because JSX is JavaScript, you can use variables inside it. Here you are declaring a name for the cat, `name`, and embedding it with curly braces inside `<Text>`.

Any JavaScript expression will work between curly braces, including function calls like `{getFullName("Rum", "Tum", "Tugger")}`:

You can think of curly braces as creating a portal into JS functionality in your JSX!

 tip

Because JSX is included in the React library, it won’t work if you don’t have `import React from 'react'` at the top of your file!

## Custom Components​

You’ve already met [React Native’s Core Components](https://reactnative.dev/docs/intro-react-native-components). React lets you nest these components inside each other to create new components. These nestable, reusable components are at the heart of the React paradigm.

For example, you can nest [Text](https://reactnative.dev/docs/text) and [TextInput](https://reactnative.dev/docs/textinput) inside a [View](https://reactnative.dev/docs/view) below, and React Native will render them together:

#### Developer notes​

info

If you’re familiar with web development, `<View>` and `<Text>` might remind you of HTML! You can think of them as the `<div>` and `<p>` tags of application development.

info

On Android, you usually put your views inside `LinearLayout`, `FrameLayout`, `RelativeLayout`, etc. to define how the view’s children will be arranged on the screen. In React Native, `View` uses Flexbox for its children’s layout. You can learn more in [our guide to layout with Flexbox](https://reactnative.dev/docs/flexbox).

You can render this component multiple times and in multiple places without repeating your code by using `<Cat>`:

Any component that renders other components is a **parent component.** Here, `Cafe` is the parent component and each `Cat` is a **child component.**

You can put as many cats in your cafe as you like. Each `<Cat>` renders a unique element—which you can customize with props.

## Props​

**Props** is short for “properties”. Props let you customize React components. For example, here you pass each `<Cat>` a different `name` for `Cat` to render:

Most of React Native’s Core Components can be customized with props, too. For example, when using [Image](https://reactnative.dev/docs/image), you pass it a prop named [source](https://reactnative.dev/docs/image#source) to define what image it shows:

`Image` has [many different props](https://reactnative.dev/docs/image#props), including [style](https://reactnative.dev/docs/image#style), which accepts a JS object of design and layout related property-value pairs.

 note

Notice the double curly braces `{{ }}` surrounding `style`‘s width and height. In JSX, JavaScript values are referenced with `{}`. This is handy if you are passing something other than a string as props, like an array or number: `<Cat food={["fish", "kibble"]} age={2} />`. However, JS objects are **also** denoted with curly braces: `{width: 200, height: 200}`. Therefore, to pass a JS object in JSX, you must wrap the object in **another pair** of curly braces: `{{width: 200, height: 200}}`

You can build many things with props and the Core Components [Text](https://reactnative.dev/docs/text), [Image](https://reactnative.dev/docs/image), and [View](https://reactnative.dev/docs/view)! But to build something interactive, you’ll need state.

## State​

While you can think of props as arguments you use to configure how components render, **state** is like a component’s personal data storage. State is useful for handling data that changes over time or that comes from user interaction. State gives your components memory!

 info

As a general rule, use props to configure a component when it renders. Use state to keep track of any component data that you expect to change over time.

The following example takes place in a cat cafe where two hungry cats are waiting to be fed. Their hunger, which we expect to change over time (unlike their names), is stored as state. To feed the cats, press their buttons—which will update their state.

You can add state to a component by calling [React’suseStateHook](https://react.dev/learn/state-a-components-memory). A Hook is a kind of function that lets you “hook into” React features. For example, `useState` is a Hook that lets you add state to function components. You can learn more about [other kinds of Hooks in the React documentation.](https://react.dev/reference/react)

First, you will want to import `useState` from React like so:

 tsx

```
import React, {useState} from 'react';
```

Then you declare the component’s state by calling `useState` inside its function. In this example, `useState` creates an `isHungry` state variable:

 tsx

```
const Cat = (props: CatProps) => {  const [isHungry, setIsHungry] = useState(true);  // ...};
```

 tip

You can use `useState` to track any kind of data: strings, numbers, Booleans, arrays, objects. For example, you can track the number of times a cat has been petted with `const [timesPetted, setTimesPetted] = useState(0)`!

Calling `useState` does two things:

- it creates a “state variable” with an initial value—in this case the state variable is `isHungry` and its initial value is `true`
- it creates a function to set that state variable’s value—`setIsHungry`

It doesn’t matter what names you use. But it can be handy to think of the pattern as `[<getter>, <setter>] = useState(<initialValue>)`.

Next you add the [Button](https://reactnative.dev/docs/button) Core Component and give it an `onPress` prop:

 tsx

```
<Button  onPress={() => {    setIsHungry(false);  }}  //../>
```

Now, when someone presses the button, `onPress` will fire, calling the `setIsHungry(false)`. This sets the state variable `isHungry` to `false`. When `isHungry` is false, the `Button`’s `disabled` prop is set to `true` and its `title` also changes:

 tsx

```
<Button  //..  disabled={!isHungry}  title={isHungry ? 'Give me some food, please!' : 'Thank you!'}/>
```

 info

You might’ve noticed that although `isHungry` is a [const](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/const), it is seemingly reassignable! What is happening is when a state-setting function like `setIsHungry` is called, its component will re-render. In this case the `Cat` function will run again—and this time, `useState` will give us the next value of `isHungry`.

Finally, put your cats inside a `Cafe` component:

 tsx

```
const Cafe = () => {  return (    <>      <Cat name="Munkustrap" />      <Cat name="Spot" />    </>  );};
```

 info

See the `<>` and `</>` above? These bits of JSX are [fragments](https://react.dev/reference/react/Fragment). Adjacent JSX elements must be wrapped in an enclosing tag. Fragments let you do that without nesting an extra, unnecessary wrapping element like `View`.

---

Now that you’ve covered both React and React Native’s Core Components, let’s dive deeper on some of these core components by looking at [handling<TextInput>](https://reactnative.dev/docs/handling-text-input).

Is this page useful?

---

# JavaScript Environment

> JavaScript Runtime

## JavaScript Runtime​

When using React Native, you're going to be running your JavaScript code in up to three environments:

- In most cases, React Native will use [Hermes](https://reactnative.dev/docs/hermes), an open-source JavaScript engine optimized for React Native.
- If Hermes is disabled, React Native will use [JavaScriptCore](https://trac.webkit.org/wiki/JavaScriptCore), the JavaScript engine that powers Safari. Note that on iOS, JavaScriptCore does not use JIT due to the absence of writable executable memory in iOS apps.
- When using Chrome debugging, all JavaScript code runs within Chrome itself, communicating with native code via WebSockets. Chrome uses [V8](https://v8.dev/) as its JavaScript engine.

While these environments are very similar, you may end up hitting some inconsistencies. It is best to avoid relying on specifics of any runtime.

## JavaScript Syntax Transformers​

Syntax transformers make writing code more enjoyable by allowing you to use new JavaScript syntax without having to wait for support on all interpreters.

React Native ships with the [Babel JavaScript compiler](https://babeljs.io). Check [Babel documentation](https://babeljs.io/docs/plugins/#transform-plugins) on its supported transformations for more details.

A full list of React Native's enabled transformations can be found in [@react-native/babel-preset](https://github.com/facebook/react-native/tree/main/packages/react-native-babel-preset).

| Transformation | Code |
| --- | --- |
| ECMAScript 5 |  |
| Reserved Words | promise.catch(function(){...}); |
| ECMAScript 2015 (ES6) |  |
| Arrow functions | <ConPress={()=>this.setState({pressed:true})}/> |
| Block scoping | letgreeting='hi'; |
| Call spread | Math.max(...array); |
| Classes | classCextendsReact.Component{render(){return<View/>;}} |
| Computed Properties | constkey='abc';constobj={[key]:10}; |
| Constants | constanswer=42; |
| Destructuring | const{isActive,style}=this.props; |
| for…of | for(varnumof[1,2,3]){...}; |
| Function Name | letnumber=x=>x; |
| Literals | constb=0b11;consto=0o7;constu='Hello\u{000A}\u{0009}!'; |
| Modules | importReact,{Component}from'react'; |
| Object Concise Method | constobj={method(){return10;}}; |
| Object Short Notation | constname='vjeux';constobj={name}; |
| Parameters | functiontest(x='hello',{a,b},...args){} |
| Rest Params | function(type,...args){}; |
| Shorthand Properties | consto={a,b,c}; |
| Sticky Regex | consta=/o+/y; |
| Template Literals | constwho='world';conststr=`Hello${who}`; |
| Unicode Regex | conststring='foo💩bar';constmatch=string.match(/foo(.)bar/u); |
| ECMAScript 2016 (ES7) |  |
| Exponentiation Operator | letx=10**2; |
| ECMAScript 2017 (ES8) |  |
| Async Functions | asyncfunctiondoStuffAsync(){constfoo=awaitdoOtherStuffAsync();}; |
| Function Trailing Comma | functionf(a,b,c,){}; |
| ECMAScript 2018 (ES9) |  |
| Object Spread | constextended={...obj,a:10}; |
| ECMAScript 2019 (ES10) |  |
| Optional Catch Binding | try{throw0;}catch{doSomethingWhichDoesNotCareAboutTheValueThrown();} |
| ECMAScript 2020 (ES11) |  |
| Dynamic Imports | constpackage=awaitimport('package');package.function() |
| Nullish Coalescing Operator | constfoo=object.foo??'default'; |
| Optional Chaining | constname=obj.user?.name; |
| ECMAScript 2022 (ES13) |  |
| Class Fields | classBork{statica='foo';staticb;x='bar';y;} |
| Stage 1 Proposal |  |
| Export Default From | exportvfrom'mod'; |
| Miscellaneous |  |
| Babel Template | template(`const %%importName%% = require(%%source%%);`); |
| Flow | functionfoo(x:?number):string{}; |
| ESM to CJS | exportdefault42; |
| JSX | <Viewstyle={{color:'red'}}/> |
| Object Assign | Object.assign(a,b); |
| React Display Name | constbar=createReactClass({}); |
| TypeScript | functionfoo(x:{hello:true,target:'react native!'}):string{}; |

## Polyfills​

Many standard functions are also available on all the supported JavaScript runtimes.

#### Browser​

- [CommonJSrequire](https://nodejs.org/docs/latest/api/modules.html)
- `console.{log, warn, error, info, debug, trace, table, group, groupCollapsed, groupEnd}`
- [XMLHttpRequest,fetch](https://reactnative.dev/docs/network#content)
- [{set, clear}{Timeout, Interval, Immediate}, {request, cancel}AnimationFrame](https://reactnative.dev/docs/timers#content)

#### ECMAScript 2015 (ES6)​

- [Array.from](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from)
- `Array.prototype.{find, findIndex}`
- [Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
- `String.prototype.{startsWith, endsWith, repeat, includes}`

#### ECMAScript 2016 (ES7)​

- `Array.prototype.includes`

#### ECMAScript 2017 (ES8)​

- `Object.{entries, values}`

#### Specific​

- `__DEV__`

Is this page useful?

---

# Keyboard

> Keyboard module to control keyboard events.

`Keyboard` module to control keyboard events.

### Usage​

The Keyboard module allows you to listen for native events and react to them, as well as make changes to the keyboard, like dismissing it.

---

# Reference

## Methods​

### addListener()​

 tsx

```
static addListener: (  eventType: KeyboardEventName,  listener: KeyboardEventListener,) => EmitterSubscription;
```

The `addListener` function connects a JavaScript function to an identified native keyboard notification event.

This function then returns the reference to the listener.

**Parameters:**

| Name | Type | Description |
| --- | --- | --- |
| eventNameRequired | string | The string that identifies the event you're listening for. See the list below. |
| callbackRequired | function | The function to be called when the event fires |

**eventName**

This can be any of the following:

- `keyboardWillShow`
- `keyboardDidShow`
- `keyboardWillHide`
- `keyboardDidHide`
- `keyboardWillChangeFrame`
- `keyboardDidChangeFrame`

 note

Only `keyboardDidShow` and `keyboardDidHide` events are available on Android. The events will not be fired when using Android 10 or below if your activity has `android:windowSoftInputMode` set to `adjustResize` or `adjustNothing`.

---

### dismiss()​

 tsx

```
static dismiss();
```

Dismisses the active keyboard and removes focus.

---

### scheduleLayoutAnimation​

 tsx

```
static scheduleLayoutAnimation(event: KeyboardEvent);
```

Useful for syncing TextInput (or other keyboard accessory view) size of position changes with keyboard movements.

---

### isVisible()​

 tsx

```
static isVisible(): boolean;
```

Whether the keyboard is last known to be visible.

---

### metrics()​

 tsx

```
static metrics(): KeyboardMetrics | undefined;
```

Return the metrics of the soft-keyboard if visible.

Is this page useful?

---

# KeyboardAvoidingView

> This component will automatically adjust its height, position, or bottom padding based on the keyboard height to remain visible while the virtual keyboard is displayed.

This component will automatically adjust its height, position, or bottom padding based on the keyboard height to remain visible while the virtual keyboard is displayed.

## Example​

---

# Reference

## Props​

### View Props​

Inherits [View Props](https://reactnative.dev/docs/view#props).

---

### behavior​

Specify how to react to the presence of the keyboard.

 note

Android and iOS both interact with this prop differently. On both iOS and Android, setting `behavior` is recommended.

| Type |
| --- |
| enum('height','position','padding') |

---

### contentContainerStyle​

The style of the content container (View) when behavior is `'position'`.

| Type |
| --- |
| View Style |

---

### enabled​

Enabled or disabled KeyboardAvoidingView.

| Type | Default |
| --- | --- |
| boolean | true |

---

### keyboardVerticalOffset​

This is the distance between the top of the user screen and the react native view, may be non-zero in some use cases.

| Type | Default |
| --- | --- |
| number | 0 |

Is this page useful?
