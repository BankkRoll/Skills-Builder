# Easing and more

# Easing

> The Easing module implements common easing functions. This module is used by Animated.timing() to convey physically believable motion in animations.

The `Easing` module implements common easing functions. This module is used by [Animated.timing()](https://reactnative.dev/docs/animated#timing) to convey physically believable motion in animations.

You can find a visualization of some common easing functions at [https://easings.net/](https://easings.net/)

### Predefined animations​

The `Easing` module provides several predefined animations through the following methods:

- [back](https://reactnative.dev/docs/easing#back) provides a basic animation where the object goes slightly back before moving forward
- [bounce](https://reactnative.dev/docs/easing#bounce) provides a bouncing animation
- [ease](https://reactnative.dev/docs/easing#ease) provides a basic inertial animation
- [elastic](https://reactnative.dev/docs/easing#elastic) provides a basic spring interaction

### Standard functions​

Three standard easing functions are provided:

- [linear](https://reactnative.dev/docs/easing#linear)
- [quad](https://reactnative.dev/docs/easing#quad)
- [cubic](https://reactnative.dev/docs/easing#cubic)

The [poly](https://reactnative.dev/docs/easing#poly) function can be used to implement quartic, quintic, and other higher power functions.

### Additional functions​

Additional mathematical functions are provided by the following methods:

- [bezier](https://reactnative.dev/docs/easing#bezier) provides a cubic bezier curve
- [circle](https://reactnative.dev/docs/easing#circle) provides a circular function
- [sin](https://reactnative.dev/docs/easing#sin) provides a sinusoidal function
- [exp](https://reactnative.dev/docs/easing#exp) provides an exponential function

The following helpers are used to modify other easing functions.

- [in](https://reactnative.dev/docs/easing#in) runs an easing function forwards
- [inOut](https://reactnative.dev/docs/easing#inout) makes any easing function symmetrical
- [out](https://reactnative.dev/docs/easing#out) runs an easing function backwards

## Example​

---

# Reference

## Methods​

### step0()​

 tsx

```
static step0(n: number);
```

A stepping function, returns 1 for any positive value of `n`.

---

### step1()​

 tsx

```
static step1(n: number);
```

A stepping function, returns 1 if `n` is greater than or equal to 1.

---

### linear()​

 tsx

```
static linear(t: number);
```

A linear function, `f(t) = t`. Position correlates to elapsed time one to one.

[https://cubic-bezier.com/#0,0,1,1](https://cubic-bezier.com/#0,0,1,1)

---

### ease()​

 tsx

```
static ease(t: number);
```

A basic inertial interaction, similar to an object slowly accelerating to speed.

[https://cubic-bezier.com/#.42,0,1,1](https://cubic-bezier.com/#.42,0,1,1)

---

### quad()​

 tsx

```
static quad(t: number);
```

A quadratic function, `f(t) = t * t`. Position equals the square of elapsed time.

[https://easings.net/#easeInQuad](https://easings.net/#easeInQuad)

---

### cubic()​

 tsx

```
static cubic(t: number);
```

A cubic function, `f(t) = t * t * t`. Position equals the cube of elapsed time.

[https://easings.net/#easeInCubic](https://easings.net/#easeInCubic)

---

### poly()​

 tsx

```
static poly(n: number);
```

A power function. Position is equal to the Nth power of elapsed time.

n = 4: [https://easings.net/#easeInQuart](https://easings.net/#easeInQuart) n = 5: [https://easings.net/#easeInQuint](https://easings.net/#easeInQuint)

---

### sin()​

 tsx

```
static sin(t: number);
```

A sinusoidal function.

[https://easings.net/#easeInSine](https://easings.net/#easeInSine)

---

### circle()​

 tsx

```
static circle(t: number);
```

A circular function.

[https://easings.net/#easeInCirc](https://easings.net/#easeInCirc)

---

### exp()​

 tsx

```
static exp(t: number);
```

An exponential function.

[https://easings.net/#easeInExpo](https://easings.net/#easeInExpo)

---

### elastic()​

 tsx

```
static elastic(bounciness: number);
```

A basic elastic interaction, similar to a spring oscillating back and forth.

Default bounciness is 1, which overshoots a little bit once. 0 bounciness doesn't overshoot at all, and bounciness of N > 1 will overshoot about N times.

[https://easings.net/#easeInElastic](https://easings.net/#easeInElastic)

---

### back()​

 tsx

```
static back(s)
```

Use with `Animated.parallel()` to create a basic effect where the object animates back slightly as the animation starts.

---

### bounce()​

 tsx

```
static bounce(t: number);
```

Provides a basic bouncing effect.

[https://easings.net/#easeInBounce](https://easings.net/#easeInBounce)

---

### bezier()​

 tsx

```
static bezier(x1: number, y1: number, x2: number, y2: number);
```

Provides a cubic bezier curve, equivalent to CSS Transitions' `transition-timing-function`.

A useful tool to visualize cubic bezier curves can be found at [https://cubic-bezier.com/](https://cubic-bezier.com/)

---

### in()​

 tsx

```
static in(easing: number);
```

Runs an easing function forwards.

---

### out()​

 tsx

```
static out(easing: number);
```

Runs an easing function backwards.

---

### inOut()​

 tsx

```
static inOut(easing: number);
```

Makes any easing function symmetrical. The easing function will run forwards for half of the duration, then backwards for the rest of the duration.

Is this page useful?

---

# Element nodes

> Element nodes represent native components in the native view tree (similar to Element nodes on Web).

Element nodes represent native components in the native view tree (similar to [Element](https://developer.mozilla.org/en-US/docs/Web/API/Element) nodes on Web).

They are provided by all native components, and by many built-in components, via refs:

  info

Note that some built-in components are only a container for other components (including native components). For example, `ScrollView` internally renders a native scroll view and a native view, which are accessible through the ref it provides using methods like `getNativeScrollRef()` and `getInnerViewRef()`.

---

## Reference​

### Web-compatible API​

From [HTMLElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement):

- Properties
  - [offsetHeight](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetHeight)
  - [offsetLeft](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetLeft)
  - [offsetParent](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetParent)
  - [offsetTop](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetTop)
  - [offsetWidth](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/offsetWidth)
- Methods
  - [blur()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/blur).
  - [focus()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus).
    - ⚠️ The `options` parameter is not supported.

From [Element](https://developer.mozilla.org/en-US/docs/Web/API/Element):

- Properties
  - [childElementCount](https://developer.mozilla.org/en-US/docs/Web/API/Element/childElementCount)
  - [children](https://developer.mozilla.org/en-US/docs/Web/API/Element/children)
  - [clientHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight)
  - [clientLeft](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientLeft)
  - [clientTop](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientTop)
  - [clientWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientWidth)
  - [firstElementChild](https://developer.mozilla.org/en-US/docs/Web/API/Element/firstElementChild)
  - [id](https://developer.mozilla.org/en-US/docs/Web/API/Element/id)
    - ℹ️ Returns the value of the `id` or `nativeID` props.
  - [lastElementChild](https://developer.mozilla.org/en-US/docs/Web/API/Element/lastElementChild)
  - [nextElementSibling](https://developer.mozilla.org/en-US/docs/Web/API/Element/nextElementSibling)
  - [nodeName](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeName)
  - [nodeType](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType)
  - [nodeValue](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeValue)
  - [previousElementSibling](https://developer.mozilla.org/en-US/docs/Web/API/Element/previousElementSibling)
  - [scrollHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight)
  - [scrollLeft](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollLeft)
    - ⚠️ For built-in components, only `ScrollView` instances can return a value other than zero.
  - [scrollTop](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollTop)
    - ⚠️ For built-in components, only `ScrollView` instances can return a value other than zero.
  - [scrollWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth)
  - [tagName](https://developer.mozilla.org/en-US/docs/Web/API/Element/tagName)
    - ℹ️ Returns a normalized native component name prefixed with `RN:`, like `RN:View`.
  - [textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
- Methods
  - [getBoundingClientRect()](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect)
  - [hasPointerCapture()](https://developer.mozilla.org/en-US/docs/Web/API/Element/hasPointerCapture)
  - [setPointerCapture()](https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture)
  - [releasePointerCapture()](https://developer.mozilla.org/en-US/docs/Web/API/Element/releasePointerCapture)

From [Node](https://developer.mozilla.org/en-US/docs/Web/API/Node):

- Properties
  - [childNodes](https://developer.mozilla.org/en-US/docs/Web/API/Node/childNodes)
  - [firstChild](https://developer.mozilla.org/en-US/docs/Web/API/Node/firstChild)
  - [isConnected](https://developer.mozilla.org/en-US/docs/Web/API/Node/isConnected)
  - [lastChild](https://developer.mozilla.org/en-US/docs/Web/API/Node/lastChild)
  - [nextSibling](https://developer.mozilla.org/en-US/docs/Web/API/Node/nextSibling)
  - [nodeName](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeName)
  - [nodeType](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeType)
  - [nodeValue](https://developer.mozilla.org/en-US/docs/Web/API/Node/nodeValue)
  - [ownerDocument](https://developer.mozilla.org/en-US/docs/Web/API/Node/ownerDocument)
    - ℹ️ Will return the [document instance](https://reactnative.dev/docs/next/document-instances) where this component was rendered.
  - [parentElement](https://developer.mozilla.org/en-US/docs/Web/API/Node/parentElement)
  - [parentNode](https://developer.mozilla.org/en-US/docs/Web/API/Node/parentNode)
  - [previousSibling](https://developer.mozilla.org/en-US/docs/Web/API/Node/previousSibling)
  - [textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
- Methods
  - [compareDocumentPosition()](https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition)
  - [contains()](https://developer.mozilla.org/en-US/docs/Web/API/Node/contains)
  - [getRootNode()](https://developer.mozilla.org/en-US/docs/Web/API/Node/getRootNode)
    - ℹ️ Will return a reference to itself if the component is not mounted.
  - [hasChildNodes()](https://developer.mozilla.org/en-US/docs/Web/API/Node/hasChildNodes)

### Legacy API​

- [measure()](https://reactnative.dev/docs/next/legacy/direct-manipulation#measurecallback)
- [measureInWindow()](https://reactnative.dev/docs/next/legacy/direct-manipulation#measureinwindowcallback)
- [measureLayout()](https://reactnative.dev/docs/next/legacy/direct-manipulation#measurelayoutrelativetonativecomponentref-onsuccess-onfail)
- [setNativeProps()](https://reactnative.dev/docs/next/legacy/direct-manipulation#setnativeprops-with-touchableopacity)

Is this page useful?

---

# Get Started with React Native

> React Native allows developers who know React to create native apps. At the same time, native developers can use React Native to gain parity between native platforms by writing common features once.

**React Native allows developers who know React to create native apps.** At the same time, native developers can use React Native to gain parity between native platforms by writing common features once.

We believe that the best way to experience React Native is through a **Framework**, a toolbox with all the necessary APIs to let you build production ready apps.

You can also use React Native without a Framework, however we’ve found that most developers benefit from using a React Native Framework like [Expo](https://expo.dev). Expo provides features like file-based routing, high-quality universal libraries, and the ability to write plugins that modify native code without having to manage native files.

 Can I use React Native without a Framework?

Yes. You can use React Native without a Framework. **However, if you’re building a new app with React Native, we recommend using a Framework.**

In short, you’ll be able to spend time writing your app instead of writing an entire Framework yourself in addition to your app.

The React Native community has spent years refining approaches to navigation, accessing native APIs, dealing with native dependencies, and more. Most apps need these core features. A React Native Framework provides them from the start of your app.

Without a Framework, you’ll either have to write your own solutions to implement core features, or you’ll have to piece together a collection of pre-existing libraries to create a skeleton of a Framework. This takes real work, both when starting your app, then later when maintaining it.

If your app has unusual constraints that are not served well by a Framework, or you prefer to solve these problems yourself, you can make a React Native app without a Framework using Android Studio, Xcode. If you’re interested in this path, learn how to [set up your environment](https://reactnative.dev/docs/set-up-your-environment) and how to [get started without a framework](https://reactnative.dev/docs/getting-started-without-a-framework).

## Start a new React Native project with Expo​

 **Platform support**

Expo is a production-grade React Native Framework. Expo provides developer tooling that makes developing apps easier, such as file-based routing, a standard library of native modules, and much more.

Expo's Framework is free and open source, with an active community on [GitHub](https://github.com/expo) and [Discord](https://chat.expo.dev). The Expo team works in close collaboration with the React Native team at Meta to bring the latest React Native features to the Expo SDK.

The team at Expo also provides Expo Application Services (EAS), an optional set of services that complements Expo, the Framework, in each step of the development process.

To create a new Expo project, run the following in your terminal:

 shell

```
npx create-expo-app@latest
```

Once you’ve created your app, check out the rest of Expo’s getting started guide to start developing your app.

 [Continue with Expo](https://docs.expo.dev/get-started/set-up-your-environment)Is this page useful?

---

# Native Components

> If you want to build new React Native Components that wrap around a Host Component like a unique kind of CheckBox on Android, or a UIButton on iOS, you should use a Fabric Native Component.

If you want to build *new* React Native Components that wrap around a [Host Component](https://reactnative.dev/architecture/glossary#host-view-tree-and-host-view) like a unique kind of [CheckBox](https://developer.android.com/reference/androidx/appcompat/widget/AppCompatCheckBox) on Android, or a [UIButton](https://developer.apple.com/documentation/uikit/uibutton?language=objc) on iOS, you should use a Fabric Native Component.

This guide will show you how to build Fabric Native Components, by implementing a web view component. The steps to doing this are:

1. Define a JavaScript specification using Flow or TypeScript.
2. Configure the dependencies management system to generate code from the provided spec and to be auto-linked.
3. Implement the Native code.
4. Use the Component in an App.

You're going to need a plain template generated application to use the component:

 bash

```
npx @react-native-community/cli@latest init Demo --install-pods false
```

## Creating a WebView Component​

This guide will show you how to create a Web View component. We will be creating the component by using the Android's [WebView](https://developer.android.com/reference/android/webkit/WebView) component, and the iOS [WKWebView](https://developer.apple.com/documentation/webkit/wkwebview?language=objc) component.

Let's start by creating the folders structure to hold our component's code:

 bash

```
mkdir -p Demo/{specs,android/app/src/main/java/com/webview}
```

This gives you the following layout where you'll working:

```
Demo├── android/app/src/main/java/com/webview└── ios└── specs
```

- The `android/app/src/main/java/com/webview` folder is the folder that will contain our Android code.
- The `ios` folder is the folder that will contain our iOS code.
- The `specs` folder is the folder that will contain the Codegen's specification file.

## 1. Define Specification for Codegen​

Your specification must be defined in either [TypeScript](https://www.typescriptlang.org/) or [Flow](https://flow.org/) (see [Codegen](https://reactnative.dev/docs/the-new-architecture/what-is-codegen) documentation for more details). This is used by Codegen to generate the C++, Objective-C++ and Java to connect your platform code to the JavaScript runtime that React runs in.

The specification file must be named `<MODULE_NAME>NativeComponent.{ts|js}` to work with Codegen. The suffix `NativeComponent` is not only a convention, it is actually used by Codegen to detect a spec file.

Use this specification for our WebView Component:

Demo/specs/WebViewNativeComponent.ts

```
import type {  CodegenTypes,  HostComponent,  ViewProps,} from 'react-native';import {codegenNativeComponent} from 'react-native';type WebViewScriptLoadedEvent = {  result: 'success' | 'error';};export interface NativeProps extends ViewProps {  sourceURL?: string;  onScriptLoaded?: CodegenTypes.BubblingEventHandler<WebViewScriptLoadedEvent> | null;}export default codegenNativeComponent<NativeProps>(  'CustomWebView',) as HostComponent<NativeProps>;
```

Demo/RCTWebView/js/RCTWebViewNativeComponent.js

```
// @flow strict-localimport type {CodegenTypes, HostComponent, ViewProps} from 'react-native';import {codegenNativeComponent} from 'react-native';type WebViewScriptLoadedEvent = $ReadOnly<{|  result: "success" | "error",|}>;type NativeProps = $ReadOnly<{|  ...ViewProps,  sourceURL?: string;  onScriptLoaded?: CodegenTypes.BubblingEventHandler<WebViewScriptLoadedEvent>?;|}>;export default (codegenNativeComponent<NativeProps>(  'CustomWebView',): HostComponent<NativeProps>);
```

This specification is composed of three main parts, excluding the imports:

- The `WebViewScriptLoadedEvent` is a supporting data type for the data the event needs to pass from native to JavaScript.
- The `NativeProps` is a definition of the props that we can set on the component.
- The `codegenNativeComponent` statement allows us to codegenerate the code for the custom component and that defines a name for the component used to match the native implementations.

As with Native Modules, you can have multiple specification files in the `specs/` directory. For more information about the types you can use, and the platform types these map to, see the [appendix](https://reactnative.dev/docs/appendix#codegen-typings).

## 2. Configure Codegen to run​

The specification is used by the React Native's Codegen tools to generate platform specific interfaces and boilerplate for us. To do this, Codegen needs to know where to find our specification and what to do with it. Update your `package.json` to include:

 json

```
"start": "react-native start",    "test": "jest"  },  "codegenConfig": {    "name": "AppSpec",    "type": "components",    "jsSrcsDir": "specs",    "android": {      "javaPackageName": "com.webview"    },    "ios": {      "componentProvider": {        "CustomWebView": "RCTWebView"      }    }  },  "dependencies": {
```

With everything wired up for Codegen, we need to prepare our native code to hook into our generated code.

Note that for iOS, we are declaratively mapping the name of the JS component that is exported by the spec (`CustomWebView`) with the iOS class that will implement the component natively.

## 2. Building your Native Code​

Now it's time to write the native platform code so that when React requires to render a view, the platform can create the right native view and can render it on screen.

You should work through both the Android and iOS platforms.

 note

This guide shows you how to create a Native Component that only works with the New Architecture. If you need to support both the New Architecture and the Legacy Architecture, please refer to our [backwards compatibility guide](https://github.com/reactwg/react-native-new-architecture/blob/main/docs/backwards-compat.md).

Now it's time to write some Android platform code to be able to render the web view. The steps you need to follow are:

- Running Codegen
- Write the code for the `ReactWebView`
- Write the code for the `ReactWebViewManager`
- Write the code for the `ReactWebViewPackage`
- Register the `ReactWebViewPackage` in the application

### 1. Run Codegen through Gradle​

Run this once to generate boilerplate that your IDE of choice can use.

 Demo/

```
cd android./gradlew generateCodegenArtifactsFromSchema
```

Codegen will generate the `ViewManager` interface you need to implement and the `ViewManager` delegate for the web view.

### 2. Write theReactWebView​

The `ReactWebView` is the component that wraps the Android native view that React Native will render when using our custom Component.

Create a `ReactWebView.java` or a `ReactWebView.kt` file in the `android/src/main/java/com/webview` folder with this code:

Demo/android/src/main/java/com/webview/ReactWebView.java

```
package com.webview;import android.content.Context;import android.util.AttributeSet;import android.webkit.WebView;import android.webkit.WebViewClient;import com.facebook.react.bridge.Arguments;import com.facebook.react.bridge.WritableMap;import com.facebook.react.bridge.ReactContext;import com.facebook.react.uimanager.UIManagerHelper;import com.facebook.react.uimanager.events.Event;public class ReactWebView extends WebView {  public ReactWebView(Context context) {    super(context);    configureComponent();  }  public ReactWebView(Context context, AttributeSet attrs) {    super(context, attrs);    configureComponent();  }  public ReactWebView(Context context, AttributeSet attrs, int defStyleAttr) {    super(context, attrs, defStyleAttr);    configureComponent();  }  private void configureComponent() {    this.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));    this.setWebViewClient(new WebViewClient() {      @Override      public void onPageFinished(WebView view, String url) {        emitOnScriptLoaded(OnScriptLoadedEventResult.success);      }    });  }  public void emitOnScriptLoaded(OnScriptLoadedEventResult result) {    ReactContext reactContext = (ReactContext) context;    int surfaceId = UIManagerHelper.getSurfaceId(reactContext);    EventDispatcher eventDispatcher = UIManagerHelper.getEventDispatcherForReactTag(reactContext, getId());    WritableMap payload = Arguments.createMap();    payload.putString("result", result.name());    OnScriptLoadedEvent event = new OnScriptLoadedEvent(surfaceId, getId(), payload);    if (eventDispatcher != null) {      eventDispatcher.dispatchEvent(event);    }  }  public enum OnScriptLoadedEventResult {    success,    error  }  private class OnScriptLoadedEvent extends Event<OnScriptLoadedEvent> {    private final WritableMap payload;    OnScriptLoadedEvent(int surfaceId, int viewId, WritableMap payload) {      super(surfaceId, viewId);      this.payload = payload;    }    @Override    public String getEventName() {      return "onScriptLoaded";    }    @Override    public WritableMap getEventData() {      return payload;    }  }}
```

Demo/android/src/main/java/com/webview/ReactWebView.kt

```
package com.webviewimport android.content.Contextimport android.util.AttributeSetimport android.webkit.WebViewimport android.webkit.WebViewClientimport com.facebook.react.bridge.Argumentsimport com.facebook.react.bridge.WritableMapimport com.facebook.react.bridge.ReactContextimport com.facebook.react.uimanager.UIManagerHelperimport com.facebook.react.uimanager.events.Eventclass ReactWebView: WebView {  constructor(context: Context) : super(context) {    configureComponent()  }  constructor(context: Context, attrs: AttributeSet?) : super(context, attrs) {    configureComponent()  }  constructor(context: Context, attrs: AttributeSet?, defStyleAttr: Int) : super(context, attrs, defStyleAttr) {    configureComponent()  }  private fun configureComponent() {    this.layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)    this.webViewClient = object : WebViewClient() {      override fun onPageFinished(view: WebView, url: String) {        emitOnScriptLoaded(OnScriptLoadedEventResult.success)      }    }  }  fun emitOnScriptLoaded(result: OnScriptLoadedEventResult) {    val reactContext = context as ReactContext    val surfaceId = UIManagerHelper.getSurfaceId(reactContext)    val eventDispatcher = UIManagerHelper.getEventDispatcherForReactTag(reactContext, id)    val payload =        Arguments.createMap().apply {          putString("result", result.name)        }    val event = OnScriptLoadedEvent(surfaceId, id, payload)    eventDispatcher?.dispatchEvent(event)  }  enum class OnScriptLoadedEventResult {    success,    error;  }  inner class OnScriptLoadedEvent(      surfaceId: Int,      viewId: Int,      private val payload: WritableMap  ) : Event<OnScriptLoadedEvent>(surfaceId, viewId) {    override fun getEventName() = "onScriptLoaded"    override fun getEventData() = payload  }}
```

The `ReactWebView` extends the Android `WebView` so you can reuse all the properties already defined by the platform with ease.

The class defines the three Android constructors but defers their actual implementation to the private `configureComponent` function. This function takes care of initializing all the components specific properties: in this case you are setting the layout of the `WebView` and you are defining the `WebClient` that you use to customize the behavior of the `WebView`. In this code, the `ReactWebView` emits an event when the page finishes loading, by implementing the `WebClient`'s `onPageFinished` method.

The code then defines a helper function to actually emit an event. To emit an event, you have to:

- grab a reference to the `ReactContext`;
- retrieve the `surfaceId` of the view that you are presenting;
- grab a reference to the `eventDispatcher` associated with the view;
- build the payload for the event using a `WritableMap` object;
- create the event object that you need to send to JavaScript;
- call the `eventDispatcher.dispatchEvent` to send the event.

The last part of the file contains the definition of the data types you need to send the event:

- The `OnScriptLoadedEventResult`, with the possible outcomes of the `OnScriptLoaded` event.
- The actual `OnScriptLoadedEvent` that needs to extend the React Native's `Event` class.

### 3. Write theWebViewManager​

The `WebViewManager` is the class that connects the React Native runtime with the native view.

When React receives the instruction from the app to render a specific component, React uses the registered view manager to create the view and to pass all the required properties.

This is the code of the `ReactWebViewManager`.

Demo/android/src/main/java/com/webview/ReactWebViewManager.java

```
package com.webview;import com.facebook.react.bridge.ReactApplicationContext;import com.facebook.react.module.annotations.ReactModule;import com.facebook.react.uimanager.SimpleViewManager;import com.facebook.react.uimanager.ThemedReactContext;import com.facebook.react.uimanager.ViewManagerDelegate;import com.facebook.react.uimanager.annotations.ReactProp;import com.facebook.react.viewmanagers.CustomWebViewManagerInterface;import com.facebook.react.viewmanagers.CustomWebViewManagerDelegate;import java.util.HashMap;import java.util.Map;@ReactModule(name = ReactWebViewManager.REACT_CLASS)class ReactWebViewManager extends SimpleViewManager<ReactWebView> implements CustomWebViewManagerInterface<ReactWebView> {  private final CustomWebViewManagerDelegate<ReactWebView, ReactWebViewManager> delegate =          new CustomWebViewManagerDelegate<>(this);  @Override  public ViewManagerDelegate<ReactWebView> getDelegate() {    return delegate;  }  @Override  public String getName() {    return REACT_CLASS;  }  @Override  public ReactWebView createViewInstance(ThemedReactContext context) {    return new ReactWebView(context);  }  @ReactProp(name = "sourceUrl")  @Override  public void setSourceURL(ReactWebView view, String sourceURL) {    if (sourceURL == null) {      view.emitOnScriptLoaded(ReactWebView.OnScriptLoadedEventResult.error);      return;    }    view.loadUrl(sourceURL, new HashMap<>());  }  public static final String REACT_CLASS = "CustomWebView";  @Override  public Map<String, Object> getExportedCustomBubblingEventTypeConstants() {    Map<String, Object> map = new HashMap<>();    Map<String, Object> bubblingMap = new HashMap<>();    bubblingMap.put("phasedRegistrationNames", new HashMap<String, String>() {{      put("bubbled", "onScriptLoaded");      put("captured", "onScriptLoadedCapture");    }});    map.put("onScriptLoaded", bubblingMap);    return map;  }}
```

Demo/android/src/main/java/com/webview/ReactWebViewManager.kt

```
package com.webviewimport com.facebook.react.bridge.ReactApplicationContext;import com.facebook.react.module.annotations.ReactModule;import com.facebook.react.uimanager.SimpleViewManager;import com.facebook.react.uimanager.ThemedReactContext;import com.facebook.react.uimanager.ViewManagerDelegate;import com.facebook.react.uimanager.annotations.ReactProp;import com.facebook.react.viewmanagers.CustomWebViewManagerInterface;import com.facebook.react.viewmanagers.CustomWebViewManagerDelegate;@ReactModule(name = ReactWebViewManager.REACT_CLASS)class ReactWebViewManager(context: ReactApplicationContext) : SimpleViewManager<ReactWebView>(), CustomWebViewManagerInterface<ReactWebView> {  private val delegate: CustomWebViewManagerDelegate<ReactWebView, ReactWebViewManager> =    CustomWebViewManagerDelegate(this)  override fun getDelegate(): ViewManagerDelegate<ReactWebView> = delegate  override fun getName(): String = REACT_CLASS  override fun createViewInstance(context: ThemedReactContext): ReactWebView = ReactWebView(context)  @ReactProp(name = "sourceUrl")  override fun setSourceURL(view: ReactWebView, sourceURL: String?) {    if (sourceURL == null) {      view.emitOnScriptLoaded(ReactWebView.OnScriptLoadedEventResult.error)      return;    }    view.loadUrl(sourceURL, emptyMap())  }  companion object {    const val REACT_CLASS = "CustomWebView"  }  override fun getExportedCustomBubblingEventTypeConstants(): Map<String, Any> =      mapOf(          "onScriptLoaded" to              mapOf(                  "phasedRegistrationNames" to                      mapOf(                          "bubbled" to "onScriptLoaded",                          "captured" to "onScriptLoadedCapture"                      )))}
```

The `ReactWebViewManager` extends the `SimpleViewManager` class from React and implements the `CustomWebViewManagerInterface`, generated by Codegen.

It holds a reference of the `CustomWebViewManagerDelegate`, another element generated by Codegen.

It then overrides the `getName` function, which must return the same name used in the spec's `codegenNativeComponent` function call.

The `createViewInstance` function is responsible to instantiate a new `ReactWebView`.

Then, the ViewManager needs to define how all the React's components props will update the native view. In the example, you need to decide how to handle the `sourceURL` property that React will set on the `WebView`.

Finally, if the component can emit an event, you need to map the event name by overriding the `getExportedCustomBubblingEventTypeConstants` for bubbling events, or the `getExportedCustomDirectEventTypeConstants` for direct events.

### 4. Write theReactWebViewPackage​

As you do with Native Modules, Native Components also need to implement the `ReactPackage` class. This is an object that you can use to register the component in the React Native runtime.

This is the code for the `ReactWebViewPackage`:

Demo/android/src/main/java/com/webview/ReactWebViewPackage.java

```
package com.webview;import com.facebook.react.BaseReactPackage;import com.facebook.react.bridge.NativeModule;import com.facebook.react.bridge.ReactApplicationContext;import com.facebook.react.module.model.ReactModuleInfo;import com.facebook.react.module.model.ReactModuleInfoProvider;import com.facebook.react.uimanager.ViewManager;import java.util.Collections;import java.util.HashMap;import java.util.List;import java.util.Map;public class ReactWebViewPackage extends BaseReactPackage {  @Override  public List<ViewManager<?, ?>> createViewManagers(ReactApplicationContext reactContext) {    return Collections.singletonList(new ReactWebViewManager(reactContext));  }  @Override  public NativeModule getModule(String s, ReactApplicationContext reactApplicationContext) {    if (ReactWebViewManager.REACT_CLASS.equals(s)) {      return new ReactWebViewManager(reactApplicationContext);    }    return null;  }  @Override  public ReactModuleInfoProvider getReactModuleInfoProvider() {    return new ReactModuleInfoProvider() {      @Override      public Map<String, ReactModuleInfo> getReactModuleInfos() {        Map<String, ReactModuleInfo> map = new HashMap<>();        map.put(ReactWebViewManager.REACT_CLASS, new ReactModuleInfo(                ReactWebViewManager.REACT_CLASS, // name                ReactWebViewManager.REACT_CLASS, // className                false,                           // canOverrideExistingModule                false,                           // needsEagerInit                false,                           // isCxxModule                true                             // isTurboModule        ));        return map;      }    };  }}
```

Demo/android/src/main/java/com/webview/ReactWebViewPackage.kt

```
package com.webviewimport com.facebook.react.BaseReactPackageimport com.facebook.react.bridge.NativeModuleimport com.facebook.react.bridge.ReactApplicationContextimport com.facebook.react.module.model.ReactModuleInfoimport com.facebook.react.module.model.ReactModuleInfoProviderimport com.facebook.react.uimanager.ViewManagerclass ReactWebViewPackage : BaseReactPackage() {  override fun createViewManagers(reactContext: ReactApplicationContext): List<ViewManager<*, *>> {    return listOf(ReactWebViewManager(reactContext))  }  override fun getModule(s: String, reactApplicationContext: ReactApplicationContext): NativeModule? {    when (s) {      ReactWebViewManager.REACT_CLASS -> ReactWebViewManager(reactApplicationContext)    }    return null  }  override fun getReactModuleInfoProvider(): ReactModuleInfoProvider = ReactModuleInfoProvider {    mapOf(ReactWebViewManager.REACT_CLASS to ReactModuleInfo(      name = ReactWebViewManager.REACT_CLASS,      className = ReactWebViewManager.REACT_CLASS,      canOverrideExistingModule = false,      needsEagerInit = false,      isCxxModule = false,      isTurboModule = true,    )    )  }}
```

The `ReactWebViewPackage` extends the `BaseReactPackage` and implements all the methods required to properly register our component.

- the `createViewManagers` method is the factory method that creates the `ViewManager` that manage the custom views.
- the `getModule` method returns the proper ViewManager depending on the View that React Native needs to render.
- the `getReactModuleInfoProvider` provides all the information required when registering the module in the runtime,

### 5. Register theReactWebViewPackagein the application​

Finally, you need to register the `ReactWebViewPackage` in the application. We do that by modifying the `MainApplication` file by adding the `ReactWebViewPackage` to the list of packages returned by the `getPackages` function.

 Demo/app/src/main/java/com/demo/MainApplication.kt

```
package com.demoimport android.app.Applicationimport com.facebook.react.PackageListimport com.facebook.react.ReactApplicationimport com.facebook.react.ReactHostimport com.facebook.react.ReactNativeHostimport com.facebook.react.ReactPackageimport com.facebook.react.defaults.DefaultNewArchitectureEntryPoint.loadimport com.facebook.react.defaults.DefaultReactHost.getDefaultReactHostimport com.facebook.react.defaults.DefaultReactNativeHostimport com.facebook.react.soloader.OpenSourceMergedSoMappingimport com.facebook.soloader.SoLoaderimport com.webview.ReactWebViewPackageclass MainApplication : Application(), ReactApplication {  override val reactNativeHost: ReactNativeHost =      object : DefaultReactNativeHost(this) {        override fun getPackages(): List<ReactPackage> =            PackageList(this).packages.apply {              add(ReactWebViewPackage())            }        override fun getJSMainModuleName(): String = "index"        override fun getUseDeveloperSupport(): Boolean = BuildConfig.DEBUG        override val isNewArchEnabled: Boolean = BuildConfig.IS_NEW_ARCHITECTURE_ENABLED        override val isHermesEnabled: Boolean = BuildConfig.IS_HERMES_ENABLED      }  override val reactHost: ReactHost    get() = getDefaultReactHost(applicationContext, reactNativeHost)  override fun onCreate() {    super.onCreate()    SoLoader.init(this, OpenSourceMergedSoMapping)    if (BuildConfig.IS_NEW_ARCHITECTURE_ENABLED) {      load()    }  }}
```

Now it's time to write some iOS platform code to be able to render the web view. The steps you need to follow are:

- Run Codegen.
- Write the code for the `RCTWebView`
- Register the `RCTWebView` in the application

### 1. Run Codegen​

You can [manually run](https://reactnative.dev/docs/the-new-architecture/codegen-cli) the Codegen, however it's simpler to use the application you're going to demo the component in to do this for you.

 bash

```
cd iosbundle installbundle exec pod install
```

Importantly you will see logging output from Codegen, which we're going to use in Xcode to build our WebView native component.

 warning

You should be careful about committing generated code to your repository. Generated code is specific to each version of React Native. Use npm [peerDependencies](https://nodejs.org/en/blog/npm/peer-dependencies) to restrict compatibility with version of React Native.

### 3. Write theRCTWebView​

We need to prepare your iOS project using Xcode by completing these **5 steps**:

1. Open the CocoaPods generated Xcode Workspace:

 bash

```
cd iosopen Demo.xcworkspace
```

 ![Open Xcode Workspace](https://reactnative.dev/docs/assets/fabric-native-components/1.webp)

1. Right click on app and select `New Group`, call the new group `WebView`.

 ![Right click on app and select New Group](https://reactnative.dev/docs/assets/fabric-native-components/2.webp)

1. In the `WebView` group, create `New`→`File from Template`.

 ![Create a new file using the Cocoa Touch Class template](https://reactnative.dev/docs/assets/fabric-native-components/3.webp)

1. Use the `Objective-C File` template, and name it `RCTWebView`.

 ![Create an Objective-C RCTWebView class](https://reactnative.dev/docs/assets/fabric-native-components/4.webp)

1. Repeat step 4 and create a header file named `RCTWebView.h`.
2. Rename `RCTWebView.m` → `RCTWebView.mm` making it an Objective-C++ file.

 Demo/ios

```
Podfile...Demo├── AppDelegate.swift...├── RCTWebView.h└── RCTWebView.mm
```

After creating the header file and the implementation file, you can start implementing them.

This is the code for the `RCTWebView.h` file, which declares the component interface.

 Demo/RCTWebView/RCTWebView.h

```
#import <React/RCTViewComponentView.h>#import <UIKit/UIKit.h>NS_ASSUME_NONNULL_BEGIN@interface RCTWebView : RCTViewComponentView// You would declare native methods you'd want to access from the view here@endNS_ASSUME_NONNULL_END
```

This class defines an `RCTWebView` which extends the `RCTViewComponentView` class. This is the base class for all the native components and it is provided by React Native.

The code for the implementation file (`RCTWebView.mm`) is the following:

 Demo/RCTWebView/RCTWebView.mm

```
#import "RCTWebView.h"#import <react/renderer/components/AppSpec/ComponentDescriptors.h>#import <react/renderer/components/AppSpec/EventEmitters.h>#import <react/renderer/components/AppSpec/Props.h>#import <react/renderer/components/AppSpec/RCTComponentViewHelpers.h>#import <WebKit/WebKit.h>using namespace facebook::react;@interface RCTWebView () <RCTCustomWebViewViewProtocol, WKNavigationDelegate>@end@implementation RCTWebView {  NSURL * _sourceURL;  WKWebView * _webView;}-(instancetype)init{  if(self = [super init]) {    _webView = [WKWebView new];    _webView.navigationDelegate = self;    [self addSubview:_webView];  }  return self;}- (void)updateProps:(Props::Shared const &)props oldProps:(Props::Shared const &)oldProps{  const auto &oldViewProps = *std::static_pointer_cast<CustomWebViewProps const>(_props);  const auto &newViewProps = *std::static_pointer_cast<CustomWebViewProps const>(props);  // Handle your props here  if (oldViewProps.sourceURL != newViewProps.sourceURL) {    NSString *urlString = [NSString stringWithCString:newViewProps.sourceURL.c_str() encoding:NSUTF8StringEncoding];    _sourceURL = [NSURL URLWithString:urlString];    if ([self urlIsValid:newViewProps.sourceURL]) {      [_webView loadRequest:[NSURLRequest requestWithURL:_sourceURL]];    }  }  [super updateProps:props oldProps:oldProps];}-(void)layoutSubviews{  [super layoutSubviews];  _webView.frame = self.bounds;}#pragma mark - WKNavigationDelegate-(void)webView:(WKWebView *)webView didFinishNavigation:(WKNavigation *)navigation{  CustomWebViewEventEmitter::OnScriptLoaded result = CustomWebViewEventEmitter::OnScriptLoaded{CustomWebViewEventEmitter::OnScriptLoadedResult::Success};  self.eventEmitter.onScriptLoaded(result);}- (BOOL)urlIsValid:(std::string)propString{  if (propString.length() > 0 && !_sourceURL) {    CustomWebViewEventEmitter::OnScriptLoaded result = CustomWebViewEventEmitter::OnScriptLoaded{CustomWebViewEventEmitter::OnScriptLoadedResult::Error};    self.eventEmitter.onScriptLoaded(result);    return NO;  }  return YES;}// Event emitter convenience method- (const CustomWebViewEventEmitter &)eventEmitter{  return static_cast<const CustomWebViewEventEmitter &>(*_eventEmitter);}+ (ComponentDescriptorProvider)componentDescriptorProvider{  return concreteComponentDescriptorProvider<CustomWebViewComponentDescriptor>();}@end
```

This code is written in Objective-C++ and contains various details:

- the `@interface` implements two protocols:
  - `RCTCustomWebViewViewProtocol`, generated by Codegen;
  - `WKNavigationDelegate`, provided by the WebKit framework to handle the web view navigation events;
- the `init` method that instantiates the `WKWebView`, adds it to the subviews and that sets the `navigationDelegate`;
- the `updateProps` method that is called by React Native when the component's props change;
- the `layoutSubviews` method that describes how the custom view needs to be laid out;
- the `webView:didFinishNavigation:` method that lets you handle what to do when the `WKWebView` finishes loading the page;
- the `urlIsValid:(std::string)propString` method that checks whether the URL received as prop is valid;
- the `eventEmitter` method which is a utility to retrieve a strongly typed `eventEmitter` instance
- the `componentDescriptorProvider` which returns the `ComponentDescriptor` generated by Codegen;

#### Add WebKit framework​

 note

This step is only required because we are creating a Web view. Web components on iOS needs to be linked against the WebKit framework provided by Apple. If your component doesn't need to access web-specific features, you can skip this step.

A web view requires access to some features that Apple provides through one of the frameworks shipped with Xcode and the devices: WebKit.
You can see it in the native code by the `#import <WebKit/WebKit.h>` line added in the `RCTWebView.mm`.

To link the WebKit framework in your app, follow these steps:

1. In Xcode, Click on your project
2. Select the app target
3. Select the General tab
4. Scroll down until you find the *"Frameworks, Libraries, and Embedded Contents"* section, and press the `+` button

 ![Add webkit framework to your app 1](https://reactnative.dev/docs/assets/AddWebKitFramework1.png)

1. In the search bar, filter for WebKit
2. Select the WebKit framework
3. Click on Add.

 ![Add webkit framework to your app 2](https://reactnative.dev/docs/assets/AddWebKitFramework2.png)

## 3. Use your Native Component​

Finally, you can use the new component in your app. Update your generated `App.tsx` to:

 Demo/App.tsx

```
import React from 'react';import {Alert, StyleSheet, View} from 'react-native';import WebView from './specs/WebViewNativeComponent';function App(): React.JSX.Element {  return (    <View style={styles.container}>      <WebView        sourceURL="https://react.dev/"        style={styles.webview}        onScriptLoaded={() => {          Alert.alert('Page Loaded');        }}      />    </View>  );}const styles = StyleSheet.create({  container: {    flex: 1,    alignItems: 'center',    alignContent: 'center',  },  webview: {    width: '100%',    height: '100%',  },});export default App;
```

This code creates an app that uses the new `WebView` component we created to load the `react.dev` website.

The app also shows an alert when the web page is loaded.

## 4. Run your App using the WebView Component​

bash

```
yarn run android
```

bash

```
yarn run ios
```

| Android | iOS |
| --- | --- |
|  |  |

Is this page useful?

---

# Fast Refresh

> Fast Refresh is a React Native feature that allows you to get near-instant feedback for changes in your React components. Fast Refresh is enabled by default, and you can toggle "Enable Fast Refresh" in the React Native Dev Menu. With Fast Refresh enabled, most edits should be visible within a second or two.

Fast Refresh is a React Native feature that allows you to get near-instant feedback for changes in your React components. Fast Refresh is enabled by default, and you can toggle "Enable Fast Refresh" in the [React Native Dev Menu](https://reactnative.dev/docs/debugging#accessing-the-in-app-developer-menu). With Fast Refresh enabled, most edits should be visible within a second or two.

## How It Works​

- If you edit a module that **only exports React component(s)**, Fast Refresh will update the code only for that module, and re-render your component. You can edit anything in that file, including styles, rendering logic, event handlers, or effects.
- If you edit a module with exports that *aren't* React components, Fast Refresh will re-run both that module, and the other modules importing it. So if both `Button.js` and `Modal.js` import `Theme.js`, editing `Theme.js` will update both components.
- Finally, if you **edit a file** that's **imported by modules outside of the React tree**, Fast Refresh **will fall back to doing a full reload**. You might have a file which renders a React component but also exports a value that is imported by a **non-React component**. For example, maybe your component also exports a constant, and a non-React utility module imports it. In that case, consider migrating the constant to a separate file and importing it into both files. This will re-enable Fast Refresh to work. Other cases can usually be solved in a similar way.

## Error Resilience​

If you make a **syntax error** during a Fast Refresh session, you can fix it and save the file again. The redbox will disappear. Modules with syntax errors are prevented from running, so you won't need to reload the app.

If you make a **runtime error during the module initialization** (for example, typing `Style.create` instead of `StyleSheet.create`), the Fast Refresh session will continue once you fix the error. The redbox will disappear, and the module will be updated.

If you make a mistake that leads to a **runtime error inside your component**, the Fast Refresh session will *also* continue after you fix the error. In that case, React will remount your application using the updated code.

If you have [error boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) in your app (which is a good idea for graceful failures in production), they will retry rendering on the next edit after a redbox. In that sense, having an error boundary can prevent you from always getting kicked out to the root app screen. However, keep in mind that error boundaries shouldn't be *too* granular. They are used by React in production, and should always be designed intentionally.

## Limitations​

Fast Refresh tries to preserve local React state in the component you're editing, but only if it's safe to do so. Here's a few reasons why you might see local state being reset on every edit to a file:

- Local state is not preserved for class components (only function components and Hooks preserve state).
- The module you're editing might have *other* exports in addition to a React component.
- Sometimes, a module would export the result of calling higher-order component like `createNavigationContainer(MyScreen)`. If the returned component is a class, state will be reset.

In the longer term, as more of your codebase moves to function components and Hooks, you can expect state to be preserved in more cases.

## Tips​

- Fast Refresh preserves React local state in function components (and Hooks) by default.
- Sometimes you might want to *force* the state to be reset, and a component to be remounted. For example, this can be handy if you're tweaking an animation that only happens on mount. To do this, you can add `// @refresh reset` anywhere in the file you're editing. This directive is local to the file, and instructs Fast Refresh to remount components defined in that file on every edit.

## Fast Refresh and Hooks​

When possible, Fast Refresh attempts to preserve the state of your component between edits. In particular, `useState` and `useRef` preserve their previous values as long as you don't change their arguments or the order of the Hook calls.

Hooks with dependencies—such as `useEffect`, `useMemo`, and `useCallback`—will *always* update during Fast Refresh. Their list of dependencies will be ignored while Fast Refresh is happening.

For example, when you edit `useMemo(() => x * 2, [x])` to `useMemo(() => x * 10, [x])`, it will re-run even though `x` (the dependency) has not changed. If React didn't do that, your edit wouldn't reflect on the screen!

Sometimes, this can lead to unexpected results. For example, even a `useEffect` with an empty array of dependencies would still re-run once during Fast Refresh. However, writing code resilient to an occasional re-running of `useEffect` is a good practice even without Fast Refresh. This makes it easier for you to later introduce new dependencies to it.

Is this page useful?
