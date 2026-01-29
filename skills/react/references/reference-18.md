# <ViewTransition> and more

# <ViewTransition>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react/components)

# <ViewTransition>

### Canary

**The<ViewTransition />API is currently only available in React’s Canary and Experimental channels.**

[Learn more about React’s release channels here.](https://react.dev/community/versioning-policy#all-release-channels)

`<ViewTransition>` lets you animate elements that update inside a Transition.

$

```
import {ViewTransition} from 'react';<ViewTransition>  <div>...</div></ViewTransition>
```

/$

- [Reference](#reference)
  - [<ViewTransition>](#viewtransition)
  - [View Transition Class](#view-transition-class)
  - [Styling View Transitions](#styling-view-transitions)
- [Usage](#usage)
  - [Animating an element on enter/exit](#animating-an-element-on-enter)
  - [Animating a shared element](#animating-a-shared-element)
  - [Animating reorder of items in a list](#animating-reorder-of-items-in-a-list)
  - [Animating from Suspense content](#animating-from-suspense-content)
  - [Opting-out of an animation](#opting-out-of-an-animation)
  - [Customizing animations](#customizing-animations)
  - [Customizing animations with types](#customizing-animations-with-types)
  - [Building View Transition enabled routers](#building-view-transition-enabled-routers)
- [Troubleshooting](#troubleshooting)
  - [My<ViewTransition>is not activating](#my-viewtransition-is-not-activating)
  - [I’m getting an error “There are two<ViewTransition name=%s>components with the same name mounted at the same time.”](#two-viewtransition-with-same-name)

---

## Reference

### <ViewTransition>

Wrap elements in `<ViewTransition>` to animate them when they update inside a [Transition](https://react.dev/reference/react/useTransition). React uses the following heuristics to determine if a View Transition activates for an animation:

- `enter`: If a `ViewTransition` itself gets inserted in this Transition, then this will activate.
- `exit`: If a `ViewTransition` itself gets deleted in this Transition, then this will activate.
- `update`: If a `ViewTransition` has any DOM mutations inside it that React is doing (such as a prop changing) or if the `ViewTransition` boundary itself changes size or position due to an immediate sibling. If there are nested` ViewTransition` then the mutation applies to them and not the parent.
- `share`: If a named `ViewTransition` is inside a deleted subtree and another named `ViewTransition` with the same name is part of an inserted subtree in the same Transition, they form a Shared Element Transition, and it animates from the deleted one to the inserted one.

By default, `<ViewTransition>` animates with a smooth cross-fade (the browser default view transition). You can customize the animation by providing a [View Transition Class](#view-transition-class) to the `<ViewTransition>` component. You can  customize animations for each kind of trigger (see [Styling View Transitions](#styling-view-transitions)).

##### Deep Dive

#### How does<ViewTransition>work?

Under the hood, React applies `view-transition-name` to inline styles of the nearest DOM node nested inside the `<ViewTransition>` component. If there are multiple sibling DOM nodes like `<ViewTransition><div /><div /></ViewTransition>` then React adds a suffix to the name to make each unique but conceptually they’re part of the same one. React doesn’t apply these eagerly but only at the time that boundary should participate in an animation.

React automatically calls `startViewTransition` itself behind the scenes so you should never do that yourself. In fact, if you have something else on the page running a ViewTransition React will interrupt it. So it’s recommended that you use React itself to coordinate these. If you had other ways of trigger ViewTransitions in the past, we recommend that you migrate to the built-in way.

If there are other React ViewTransitions already running then React will wait for them to finish before starting the next one. However, importantly if there are multiple updates happening while the first one is running, those will all be batched into one. If you start A->B. Then in the meantime you get an update to go to C and then D. When the first A->B animation finishes the next one will animate from B->D.

The `getSnapshotBeforeUpdate` life-cycle will be called before `startViewTransition` and some `view-transition-name` will update at the same time.

Then React calls `startViewTransition`. Inside the `updateCallback`, React will:

- Apply its mutations to the DOM and invoke useInsertionEffects.
- Wait for fonts to load.
- Call componentDidMount, componentDidUpdate, useLayoutEffect and refs.
- Wait for any pending Navigation to finish.
- Then React will measure any changes to the layout to see which boundaries will need to animate.

After the ready Promise of the `startViewTransition` is resolved, React will then revert the `view-transition-name`. Then React will invoke the `onEnter`, `onExit`, `onUpdate` and `onShare` callbacks to allow for manual programmatic control over the Animations. This will be after the built-in default ones have already been computed.

If a `flushSync` happens to get in the middle of this sequence, then React will skip the Transition since it relies on being able to complete synchronously.

After the finished Promise of the `startViewTransition` is resolved, React will then invoke `useEffect`. This prevents those from interfering with the performance of the Animation. However, this is not a guarantee because if another `setState` happens while the Animation is running it’ll still have to invoke the `useEffect` earlier to preserve the sequential guarantees.

#### Props

By default, `<ViewTransition>` animates with a smooth cross-fade. You can customize the animation, or specify a shared element transition, with these props:

- **optional** `enter`: A string or object. The [View Transition Class](#view-transition-class) to apply when enter is activated.
- **optional** `exit`: A string or object. The [View Transition Class](#view-transition-class) to apply when exit is activated.
- **optional** `update`: A string or object. The [View Transition Class](#view-transition-class) to apply when an update is activated.
- **optional** `share`: A string or object. The [View Transition Class](#view-transition-class) to apply when a shared element is activated.
- **optional** `default`: A string or object. The [View Transition Class](#view-transition-class) used when no other matching activation prop is found.
- **optional** `name`: A string or object. The name of the View Transition used for shared element transitions. If not provided, React will use a unique name for each View Transition to prevent unexpected animations.

#### Callback

These callbacks allow you to adjust the animation imperatively using the [animate](https://developer.mozilla.org/en-US/docs/Web/API/Element/animate) APIs:

- **optional** `onEnter`: A function. React calls `onEnter` after an “enter” animation.
- **optional** `onExit`: A function. React calls `onExit` after an “exit” animation.
- **optional** `onShare`:  A function. React calls `onShare` after a “share” animation.
- **optional** `onUpdate`:  A function. React calls `onUpdate` after an “update” animation.

Each callback receives as arguments:

- `element`: The DOM element that was animated.
- `types`: The [Transition Types](https://react.dev/reference/react/addTransitionType) included in the animation.

### View Transition Class

The View Transition Class is the CSS class name(s) applied by React during the transition when the ViewTransition activates. It can be a string or an object.

- `string`: the `class` added on the child elements when activated. If `'none'` is provided, no class will be added.
- `object`: the class added on the child elements will be the key matching View Transition type added with `addTransitionType`. The object can also specify a `default` to use if no matching type is found.

The value `'none'` can be used to prevent a View Transition from activating for a specific trigger.

### Styling View Transitions

### Note

In many early examples of View Transitions around the web, you’ll have seen using a [view-transition-name](https://developer.mozilla.org/en-US/docs/Web/CSS/view-transition-name) and then style it using `::view-transition-...(my-name)` selectors. We don’t recommend that for styling. Instead, we normally recommend using a View Transition Class instead.

To customize the animation for a `<ViewTransition>` you can provide a View Transition Class to one of the activation props. The View Transition Class is a CSS class name that React applies to the child elements when the ViewTransition activates.

For example, to customize an “enter” animation, provide a class name to the `enter` prop:

 $

```
<ViewTransition enter="slide-in">
```

/$

When the `<ViewTransition>` activates an “enter” animation, React will add the class name `slide-in`. Then you can refer to this class using [view transition pseudo selectors](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API#pseudo-elements) to build reusable animations:

 $

```
::view-transition-group(.slide-in) {  }::view-transition-old(.slide-in) {}::view-transition-new(.slide-in) {}
```

/$

In the future, CSS libraries may add built-in animations using View Transition Classes to make this easier to use.

#### Caveats

- By default, `setState` updates immediately and does not activate `<ViewTransition>`, only updates wrapped in a [Transition](https://react.dev/reference/react/useTransition). You can also use [<Suspense>](https://react.dev/reference/react/Suspense) to opt-in to a Transition to [reveal content](https://react.dev/reference/react/Suspense#revealing-content-together-at-once).
- `<ViewTransition>` creates an image that can be moved around, scaled and cross-faded. Unlike Layout Animations you may have seen in React Native or Motion, this means that not every individual Element inside of it animates its position. This can lead to better performance and a more continuous feeling, smooth animation compared to animating every individual piece. However, it can also lose continuity in things that should be moving by themselves. So you might have to add more `<ViewTransition>` boundaries manually as a result.
- Many users may prefer not having animations on the page. React doesn’t automatically disable animations for this case. We recommend that using the `@media (prefers-reduced-motion)` media query to disable animations or tone them down based on user preference. In the future, CSS libraries may have this built-in to their presets.
- Currently, `<ViewTransition>` only works in the DOM. We’re working on adding support for React Native and other platforms.

---

## Usage

### Animating an element on enter/exit

Enter/Exit Transitions trigger when a `<ViewTransition>` is added or removed by a component in a transition:

 $

```
function Child() {  return (    <ViewTransition>      <div>Hi</div>    </ViewTransition>  );}function Parent() {  const [show, setShow] = useState();  if (show) {    return <Child />;  }  return null;}
```

/$

When `setShow` is called, `show` switches to `true` and the `Child` component is rendered. When `setShow` is called inside `startTransition`, and `Child` renders a `ViewTransition` before any other DOM nodes, an `enter` animation is triggered.

When `show` switches back to `false`, an `exit` animation is triggered.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from 'react';
import {Video} from "./Video";
import videos from "./data"

function Item() {
  return (
    <ViewTransition>
      <Video video={videos[0]}/>
    </ViewTransition>
  );
}

export default function Component() {
  const [showItem, setShowItem] = useState(false);
  return (
    <>
      <button
        onClick={() => {
          startTransition(() => {
            setShowItem((prev) => !prev);
          });
        }}
      >{showItem ? '➖' : '➕'}</button>

      {showItem ? <Item /> : null}
    </>
  );
}
```

/$

### Pitfall

`<ViewTransition>` only activates if it is placed before any DOM node. If `Child` instead looked like this, no animation would trigger:

$

```
function Component() {  return <ViewTransition>Hi</ViewTransition>;}
```

/$

---

### Animating a shared element

Normally, we don’t recommend assigning a name to a `<ViewTransition>` and instead let React assign it an automatic name. The reason you might want to assign a name is to animate between completely different components when one tree unmounts and another tree mounts at the same time. To preserve continuity.

 $

```
<ViewTransition name={UNIQUE_NAME}>  <Child /></ViewTransition>
```

/$

When one tree unmounts and another mounts, if there’s a pair where the same name exists in the unmounting tree and the mounting tree, they trigger the “share” animation on both. It animates from the unmounting side to the mounting side.

Unlike an exit/enter animation this can be deeply inside the deleted/mounted tree. If a `<ViewTransition>` would also be eligible for exit/enter, then the “share” animation takes precedence.

If Transition first unmounts one side and then leads to a `<Suspense>` fallback being shown before eventually the new name being mounted, then no shared element transition happens.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from "react";
import {Video, Thumbnail, FullscreenVideo} from "./Video";
import videos from "./data";

export default function Component() {
  const [fullscreen, setFullscreen] = useState(false);
  if (fullscreen) {
    return <FullscreenVideo
      video={videos[0]}
      onExit={() => startTransition(() => setFullscreen(false))}
    />
  }
  return <Video
    video={videos[0]}
    onClick={() => startTransition(() => setFullscreen(true))}
  />
}
```

/$

### Note

If either the mounted or unmounted side of a pair is outside the viewport, then no pair is formed. This ensures that it doesn’t fly in or out of the viewport when something is scrolled. Instead it’s treated as a regular enter/exit by itself.

This does not happen if the same Component instance changes position, which triggers an “update”. Those animate regardless if one position is outside the viewport.

There’s currently a quirk where if a deeply nested unmounted `<ViewTransition>` is inside the viewport but the mounted side is not within the viewport, then the unmounted side animates as its own “exit” animation even if it’s deeply nested instead of as part of the parent animation.

### Pitfall

It’s important that there’s only one thing with the same name mounted at a time in the entire app. Therefore it’s important to use unique namespaces for the name to avoid conflicts. To ensure you can do this you might want to add a constant in a separate module that you import.

$

```
export const MY_NAME = "my-globally-unique-name";import {MY_NAME} from './shared-name';...<ViewTransition name={MY_NAME}>
```

/$

---

### Animating reorder of items in a list

 $

```
items.map(item => <Component key={item.id} item={item} />)
```

/$

When reordering a list, without updating the content, the “update” animation triggers on each `<ViewTransition>` in the list if they’re outside a DOM node. Similar to enter/exit animations.

This means that this will trigger the animation on this `<ViewTransition>`:

 $

```
function Component() {  return <ViewTransition><div>...</div></ViewTransition>;}
```

/$ $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from "react";
import {Video} from "./Video";
import videos from "./data";

export default function Component() {
  const [orderedVideos, setOrderedVideos] = useState(videos);
  const reorder = () => {
    startTransition(() => {
      setOrderedVideos((prev) => {
        return [...prev.sort(() => Math.random() - 0.5)];
      });
    });
  };
  return (
    <>
      <button onClick={reorder}>🎲</button>
      <div className="listContainer">
        {orderedVideos.map((video, i) => {
          return (
            <ViewTransition key={video.title}>
              <Video video={video} />
            </ViewTransition>
          );
        })}
      </div>
    </>
  );
}
```

/$

However, this wouldn’t animate each individual item:

 $

```
function Component() {  return <div><ViewTransition>...</ViewTransition></div>;}
```

/$

Instead, any parent `<ViewTransition>` would cross-fade. If there is no parent `<ViewTransition>` then there’s no animation in that case.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from "react";
import {Video} from "./Video";
import videos from "./data";

export default function Component() {
  const [orderedVideos, setOrderedVideos] = useState(videos);
  const reorder = () => {
    startTransition(() => {
      setOrderedVideos((prev) => {
        return [...prev.sort(() => Math.random() - 0.5)];
      });
    });
  };
  return (
    <>
      <button onClick={reorder}>🎲</button>
      <ViewTransition>
        <div className="listContainer">
          {orderedVideos.map((video, i) => {
            return <Video video={video} key={video.title} />;
          })}
        </div>
      </ViewTransition>
    </>
  );
}
```

/$

This means you might want to avoid wrapper elements in lists where you want to allow the Component to control its own reorder animation:

 $

```
items.map(item => <div><Component key={item.id} item={item} /></div>)
```

/$

The above rule also applies if one of the items updates to resize, which then causes the siblings to resize, it’ll also animate its sibling `<ViewTransition>` but only if they’re immediate siblings.

This means that during an update, which causes a lot of re-layout, it doesn’t individually animate every `<ViewTransition>` on the page. That would lead to a lot of noisy animations which distracts from the actual change. Therefore React is more conservative about when an individual animation triggers.

### Pitfall

It’s important to properly use keys to preserve identity when reordering lists. It might seem like you could use “name”, shared element transitions, to animate reorders but that would not trigger if one side was outside the viewport. To animate a reorder you often want to show that it went to a position outside the viewport.

---

### Animating from Suspense content

Just like any Transition, React waits for data and new CSS (`<link rel="stylesheet" precedence="...">`) before running the animation. In addition to this, ViewTransitions also wait up to 500ms for new fonts to load before starting the animation to avoid them flickering in later. For the same reason, an image wrapped in ViewTransition will wait for the image to load.

If it’s inside a new Suspense boundary instance, then the fallback is shown first. After the Suspense boundary fully loads, it triggers the `<ViewTransition>` to animate the reveal to the content.

There are two ways to animate Suspense boundaries depending on where you place the `<ViewTransition>`:

Update:

 $

```
<ViewTransition>  <Suspense fallback={<A />}>    <B />  </Suspense></ViewTransition>
```

/$

In this scenario when the content goes from A to B, it’ll be treated as an “update” and apply that class if appropriate. Both A and B will get the same view-transition-name and therefore they’re acting as a cross-fade by default.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition,
  Suspense
} from 'react';
import {Video, VideoPlaceholder} from "./Video";
import {useLazyVideoData} from "./data"

function LazyVideo() {
  const video = useLazyVideoData();
  return (
    <Video video={video}/>
  );
}

export default function Component() {
  const [showItem, setShowItem] = useState(false);
  return (
    <>
      <button
        onClick={() => {
          startTransition(() => {
            setShowItem((prev) => !prev);
          });
        }}
      >{showItem ? '➖' : '➕'}</button>
      {showItem ? (
        <ViewTransition>
          <Suspense fallback={<VideoPlaceholder />}>
            <LazyVideo />
          </Suspense>
        </ViewTransition>
      ) : null}
    </>
  );
}
```

/$

Enter/Exit:

 $

```
<Suspense fallback={<ViewTransition><A /></ViewTransition>}>  <ViewTransition><B /></ViewTransition></Suspense>
```

/$

In this scenario, these are two separate ViewTransition instances each with their own `view-transition-name`. This will be treated as an “exit” of the `<A>` and an “enter” of the `<B>`.

You can achieve different effects depending on where you choose to place the `<ViewTransition>` boundary.

---

### Opting-out of an animation

Sometimes you’re wrapping a large existing component, like a whole page, and you want to animate some updates, such as changing the theme. However, you don’t want it to opt-in all updates inside the whole page to cross-fade when they’re updating. Especially if you’re incrementally adding more animations.

You can use the class “none” to opt-out of an animation. By wrapping your children in a “none” you can disable animations for updates to them while the parent still triggers.

 $

```
<ViewTransition>  <div className={theme}>    <ViewTransition update="none">      {children}    </ViewTransition>  </div></ViewTransition>
```

/$

This will only animate if the theme changes and not if only the children update. The children can still opt-in again with their own `<ViewTransition>` but at least it’s manual again.

---

### Customizing animations

By default, `<ViewTransition>` includes the default cross-fade from the browser.

To customize animations, you can provide props to the `<ViewTransition>` component to specify which animations to use, based on how the `<ViewTransition>` activates.

For example, we can slow down the default cross fade animation:

 $

```
<ViewTransition default="slow-fade">  <Video /></ViewTransition>
```

/$

And define slow-fade in CSS using view transition classes:

 $

```
::view-transition-old(.slow-fade) {    animation-duration: 500ms;}::view-transition-new(.slow-fade) {    animation-duration: 500ms;}
```

/$ $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from 'react';
import {Video} from "./Video";
import videos from "./data"

function Item() {
  return (
    <ViewTransition default="slow-fade">
      <Video video={videos[0]}/>
    </ViewTransition>
  );
}

export default function Component() {
  const [showItem, setShowItem] = useState(false);
  return (
    <>
      <button
        onClick={() => {
          startTransition(() => {
            setShowItem((prev) => !prev);
          });
        }}
      >{showItem ? '➖' : '➕'}</button>

      {showItem ? <Item /> : null}
    </>
  );
}
```

/$

In addition to setting the `default`, you can also provide configurations for `enter`, `exit`, `update`, and `share` animations.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  useState,
  startTransition
} from 'react';
import {Video} from "./Video";
import videos from "./data"

function Item() {
  return (
    <ViewTransition enter="slide-in" exit="slide-out">
      <Video video={videos[0]}/>
    </ViewTransition>
  );
}

export default function Component() {
  const [showItem, setShowItem] = useState(false);
  return (
    <>
      <button
        onClick={() => {
          startTransition(() => {
            setShowItem((prev) => !prev);
          });
        }}
      >{showItem ? '➖' : '➕'}</button>

      {showItem ? <Item /> : null}
    </>
  );
}
```

/$

### Customizing animations with types

You can use the [addTransitionType](https://react.dev/reference/react/addTransitionType) API to add a class name to the child elements when a specific transition type is activated for a specific activation trigger. This allows you to customize the animation for each type of transition.

For example, to customize the animation for all forward and backward navigations:

 $

```
<ViewTransition default={{  'navigation-back': 'slide-right',  'navigation-forward': 'slide-left', }}>  <div>...</div></ViewTransition> // in your router:startTransition(() => {  addTransitionType('navigation-' + navigationType);});
```

/$

When the ViewTransition activates a “navigation-back” animation, React will add the class name “slide-right”. When the ViewTransition activates a “navigation-forward” animation, React will add the class name “slide-left”.

In the future, routers and other libraries may add support for standard view-transition types and styles.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {
  ViewTransition,
  addTransitionType,
  useState,
  startTransition,
} from "react";
import {Video} from "./Video";
import videos from "./data"

function Item() {
  return (
    <ViewTransition enter={
        {
          "add-video-back": "slide-in-back",
          "add-video-forward": "slide-in-forward"
        }
      }
      exit={
        {
          "remove-video-back": "slide-in-forward",
          "remove-video-forward": "slide-in-back"
        }
      }>
      <Video video={videos[0]}/>
    </ViewTransition>
  );
}

export default function Component() {
  const [showItem, setShowItem] = useState(false);
  return (
    <>
      <div className="button-container">
        <button
          onClick={() => {
            startTransition(() => {
              if (showItem) {
                addTransitionType("remove-video-back")
              } else {
                addTransitionType("add-video-back")
              }
              setShowItem((prev) => !prev);
            });
          }}
        >⬅️</button>
        <button
          onClick={() => {
            startTransition(() => {
              if (showItem) {
                addTransitionType("remove-video-forward")
              } else {
                addTransitionType("add-video-forward")
              }
              setShowItem((prev) => !prev);
            });
          }}
        >➡️</button>
      </div>
      {showItem ? <Item /> : null}
    </>
  );
}
```

/$

### Building View Transition enabled routers

React waits for any pending Navigation to finish to ensure that scroll restoration happens within the animation. If the Navigation is blocked on React, your router must unblock in `useLayoutEffect` since `useEffect` would lead to a deadlock.

If a `startTransition` is started from the legacy popstate event, such as during a “back”-navigation then it must finish synchronously to ensure scroll and form restoration works correctly. This is in conflict with running a View Transition animation. Therefore, React will skip animations from popstate. Therefore animations won’t run for the back button. You can fix this by upgrading your router to use the Navigation API.

---

## Troubleshooting

### My<ViewTransition>is not activating

`<ViewTransition>` only activates if it is placed before any DOM node:

 $

```
function Component() {  return (    <div>      <ViewTransition>Hi</ViewTransition>    </div>  );}
```

/$

To fix, ensure that the `<ViewTransition>` comes before any other DOM nodes:

 $

```
function Component() {  return (    <ViewTransition>      <div>Hi</div>    </ViewTransition>  );}
```

/$

### I’m getting an error “There are two<ViewTransition name=%s>components with the same name mounted at the same time.”

This error occurs when two `<ViewTransition>` components with the same `name` are mounted at the same time:

 $

```
function Item() {  // 🚩 All items will get the same "name".  return <ViewTransition name="item">...</ViewTransition>;}function ItemList({items}) {  return (    <>      {item.map(item => <Item key={item.id} />)}    </>  );}
```

/$

This will cause the View Transition to error. In development, React detects this issue to surface it and logs two errors:

 ConsoleThere are two `<ViewTransition name=%s>` components with the same name mounted at the same time. This is not supported and will cause View Transitions to error. Try to use a more unique name e.g. by using a namespace prefix and adding the id of an item to the name.
   at Item
   at ItemListThe existing `<ViewTransition name=%s>` duplicate has this stack trace.
   at Item
   at ItemList

To fix, ensure that there’s only one `<ViewTransition>` with the same name mounted at a time in the entire app by ensuring the `name` is unique, or adding an `id` to the name:

 $

```
function Item({id}) {  // ✅ All items will get the same "name".  return <ViewTransition name={`item-${id}`}>...</ViewTransition>;}function ItemList({items}) {  return (    <>      {item.map(item => <Item key={item.id} item={item} />)}    </>  );}
```

/$[Previous<Activity>](https://react.dev/reference/react/Activity)[NextAPIs](https://react.dev/reference/react/apis)

---

# compilationMode

[API Reference](https://react.dev/reference/react)[Configuration](https://react.dev/reference/react-compiler/configuration)

# compilationMode

The `compilationMode` option controls how the React Compiler selects which functions to compile.

 $

```
{  compilationMode: 'infer' // or 'annotation', 'syntax', 'all'}
```

/$

- [Reference](#reference)
  - [compilationMode](#compilationmode)
- [Usage](#usage)
  - [Default inference mode](#default-inference-mode)
  - [Incremental adoption with annotation mode](#incremental-adoption)
  - [Using Flow syntax mode](#flow-syntax-mode)
  - [Opting out specific functions](#opting-out)
- [Troubleshooting](#troubleshooting)
  - [Component not being compiled in infer mode](#component-not-compiled-infer)

---

## Reference

### compilationMode

Controls the strategy for determining which functions the React Compiler will optimize.

#### Type

 $

```
'infer' | 'syntax' | 'annotation' | 'all'
```

/$

#### Default value

`'infer'`

#### Options

- **'infer'** (default): The compiler uses intelligent heuristics to identify React components and hooks:
  - Functions explicitly annotated with `"use memo"` directive
  - Functions that are named like components (PascalCase) or hooks (`use` prefix) AND create JSX and/or call other hooks
- **'annotation'**: Only compile functions explicitly marked with the `"use memo"` directive. Ideal for incremental adoption.
- **'syntax'**: Only compile components and hooks that use Flow’s [component](https://flow.org/en/docs/react/component-syntax/) and [hook](https://flow.org/en/docs/react/hook-syntax/) syntax.
- **'all'**: Compile all top-level functions. Not recommended as it may compile non-React functions.

#### Caveats

- The `'infer'` mode requires functions to follow React naming conventions to be detected
- Using `'all'` mode may negatively impact performance by compiling utility functions
- The `'syntax'` mode requires Flow and won’t work with TypeScript
- Regardless of mode, functions with `"use no memo"` directive are always skipped

---

## Usage

### Default inference mode

The default `'infer'` mode works well for most codebases that follow React conventions:

 $

```
{  compilationMode: 'infer'}
```

/$

With this mode, these functions will be compiled:

 $

```
// ✅ Compiled: Named like a component + returns JSXfunction Button(props) {  return <button>{props.label}</button>;}// ✅ Compiled: Named like a hook + calls hooksfunction useCounter() {  const [count, setCount] = useState(0);  return [count, setCount];}// ✅ Compiled: Explicit directivefunction expensiveCalculation(data) {  "use memo";  return data.reduce(/* ... */);}// ❌ Not compiled: Not a component/hook patternfunction calculateTotal(items) {  return items.reduce((a, b) => a + b, 0);}
```

/$

### Incremental adoption with annotation mode

For gradual migration, use `'annotation'` mode to only compile marked functions:

 $

```
{  compilationMode: 'annotation'}
```

/$

Then explicitly mark functions to compile:

 $

```
// Only this function will be compiledfunction ExpensiveList(props) {  "use memo";  return (    <ul>      {props.items.map(item => (        <li key={item.id}>{item.name}</li>      ))}    </ul>  );}// This won't be compiled without the directivefunction NormalComponent(props) {  return <div>{props.content}</div>;}
```

/$

### Using Flow syntax mode

If your codebase uses Flow instead of TypeScript:

 $

```
{  compilationMode: 'syntax'}
```

/$

Then use Flow’s component syntax:

 $

```
// Compiled: Flow component syntaxcomponent Button(label: string) {  return <button>{label}</button>;}// Compiled: Flow hook syntaxhook useCounter(initial: number) {  const [count, setCount] = useState(initial);  return [count, setCount];}// Not compiled: Regular function syntaxfunction helper(data) {  return process(data);}
```

/$

### Opting out specific functions

Regardless of compilation mode, use `"use no memo"` to skip compilation:

 $

```
function ComponentWithSideEffects() {  "use no memo"; // Prevent compilation  // This component has side effects that shouldn't be memoized  logToAnalytics('component_rendered');  return <div>Content</div>;}
```

/$

---

## Troubleshooting

### Component not being compiled in infer mode

In `'infer'` mode, ensure your component follows React conventions:

 $

```
// ❌ Won't be compiled: lowercase namefunction button(props) {  return <button>{props.label}</button>;}// ✅ Will be compiled: PascalCase namefunction Button(props) {  return <button>{props.label}</button>;}// ❌ Won't be compiled: doesn't create JSX or call hooksfunction useData() {  return window.localStorage.getItem('data');}// ✅ Will be compiled: calls a hookfunction useData() {  const [data] = useState(() => window.localStorage.getItem('data'));  return data;}
```

/$[PreviousConfiguration](https://react.dev/reference/react-compiler/configuration)[Nextgating](https://react.dev/reference/react-compiler/gating)

---

# Compiling Libraries

[API Reference](https://react.dev/reference/react)

# Compiling Libraries

This guide helps library authors understand how to use React Compiler to ship optimized library code to their users.

- [Why Ship Compiled Code?](#why-ship-compiled-code)
- [Setting Up Compilation](#setting-up-compilation)
- [Backwards Compatibility](#backwards-compatibility)
  - [1. Install the runtime package](#install-runtime-package)
  - [2. Configure the target version](#configure-target-version)
- [Testing Strategy](#testing-strategy)
- [Troubleshooting](#troubleshooting)
  - [Library doesn’t work with older React versions](#library-doesnt-work-with-older-react-versions)
  - [Compilation conflicts with other Babel plugins](#compilation-conflicts-with-other-babel-plugins)
  - [Runtime module not found](#runtime-module-not-found)
- [Next Steps](#next-steps)

## Why Ship Compiled Code?

As a library author, you can compile your library code before publishing to npm. This provides several benefits:

- **Performance improvements for all users** - Your library users get optimized code even if they aren’t using React Compiler yet
- **No configuration required by users** - The optimizations work out of the box
- **Consistent behavior** - All users get the same optimized version regardless of their build setup

## Setting Up Compilation

Add React Compiler to your library’s build process:

  Terminal

```
npm install -D babel-plugin-react-compiler@latest
```

Configure your build tool to compile your library. For example, with Babel:

 $

```
// babel.config.jsmodule.exports = {  plugins: [    'babel-plugin-react-compiler',  ],  // ... other config};
```

/$

## Backwards Compatibility

If your library supports React versions below 19, you’ll need additional configuration:

### 1. Install the runtime package

We recommend installing react-compiler-runtime as a direct dependency:

  Terminal

```
npm install react-compiler-runtime@latest
```

 $

```
{  "dependencies": {    "react-compiler-runtime": "^1.0.0"  },  "peerDependencies": {    "react": "^17.0.0 || ^18.0.0 || ^19.0.0"  }}
```

/$

### 2. Configure the target version

Set the minimum React version your library supports:

 $

```
{  target: '17', // Minimum supported React version}
```

/$

## Testing Strategy

Test your library both with and without compilation to ensure compatibility. Run your existing test suite against the compiled code, and also create a separate test configuration that bypasses the compiler. This helps catch any issues that might arise from the compilation process and ensures your library works correctly in all scenarios.

## Troubleshooting

### Library doesn’t work with older React versions

If your compiled library throws errors in React 17 or 18:

1. Verify you’ve installed `react-compiler-runtime` as a dependency
2. Check that your `target` configuration matches your minimum supported React version
3. Ensure the runtime package is included in your published bundle

### Compilation conflicts with other Babel plugins

Some Babel plugins may conflict with React Compiler:

1. Place `babel-plugin-react-compiler` early in your plugin list
2. Disable conflicting optimizations in other plugins
3. Test your build output thoroughly

### Runtime module not found

If users see “Cannot find module ‘react-compiler-runtime’“:

1. Ensure the runtime is listed in `dependencies`, not `devDependencies`
2. Check that your bundler includes the runtime in the output
3. Verify the package is published to npm with your library

## Next Steps

- Learn about [debugging techniques](https://react.dev/learn/react-compiler/debugging) for compiled code
- Check the [configuration options](https://react.dev/reference/react-compiler/configuration) for all compiler options
- Explore [compilation modes](https://react.dev/reference/react-compiler/compilationMode) for selective optimization

[Previous"use no memo"](https://react.dev/reference/react-compiler/directives/use-no-memo)

---

# Configuration

[API Reference](https://react.dev/reference/react)

# Configuration

This page lists all configuration options available in React Compiler.

### Note

For most apps, the default options should work out of the box. If you have a special need, you can use these advanced options.

 $

```
// babel.config.jsmodule.exports = {  plugins: [    [      'babel-plugin-react-compiler', {        // compiler options      }    ]  ]};
```

/$

---

## Compilation Control

These options control *what* the compiler optimizes and *how* it selects components and hooks to compile.

- [compilationMode](https://react.dev/reference/react-compiler/compilationMode) controls the strategy for selecting functions to compile (e.g., all functions, only annotated ones, or intelligent detection).

 $

```
{  compilationMode: 'annotation' // Only compile "use memo" functions}
```

/$

---

## Version Compatibility

React version configuration ensures the compiler generates code compatible with your React version.

[target](https://react.dev/reference/react-compiler/target) specifies which React version you’re using (17, 18, or 19).

 $

```
// For React 18 projects{  target: '18' // Also requires react-compiler-runtime package}
```

/$

---

## Error Handling

These options control how the compiler responds to code that doesn’t follow the [Rules of React](https://react.dev/reference/rules).

[panicThreshold](https://react.dev/reference/react-compiler/panicThreshold) determines whether to fail the build or skip problematic components.

 $

```
// Recommended for production{  panicThreshold: 'none' // Skip components with errors instead of failing the build}
```

/$

---

## Debugging

Logging and analysis options help you understand what the compiler is doing.

[logger](https://react.dev/reference/react-compiler/logger) provides custom logging for compilation events.

 $

```
{  logger: {    logEvent(filename, event) {      if (event.kind === 'CompileSuccess') {        console.log('Compiled:', filename);      }    }  }}
```

/$

---

## Feature Flags

Conditional compilation lets you control when optimized code is used.

[gating](https://react.dev/reference/react-compiler/gating) enables runtime feature flags for A/B testing or gradual rollouts.

 $

```
{  gating: {    source: 'my-feature-flags',    importSpecifierName: 'isCompilerEnabled'  }}
```

/$

---

## Common Configuration Patterns

### Default configuration

For most React 19 applications, the compiler works without configuration:

 $

```
// babel.config.jsmodule.exports = {  plugins: [    'babel-plugin-react-compiler'  ]};
```

/$

### React 17/18 projects

Older React versions need the runtime package and target configuration:

 $

```
npm install react-compiler-runtime@latest
```

/$ $

```
{  target: '18' // or '17'}
```

/$

### Incremental adoption

Start with specific directories and expand gradually:

 $

```
{  compilationMode: 'annotation' // Only compile "use memo" functions}
```

/$[NextcompilationMode](https://react.dev/reference/react-compiler/compilationMode)

---

# use memo

[API Reference](https://react.dev/reference/react)[Directives](https://react.dev/reference/react-compiler/directives)

# use memo

`"use memo"` marks a function for React Compiler optimization.

### Note

In most cases, you don’t need `"use memo"`. It’s primarily needed in `annotation` mode where you must explicitly mark functions for optimization. In `infer` mode, the compiler automatically detects components and hooks by their naming patterns (PascalCase for components, `use` prefix for hooks). If a component or hook isn’t being compiled in `infer` mode, you should fix its naming convention rather than forcing compilation with `"use memo"`.

- [Reference](#reference)
  - ["use memo"](#use-memo)
  - [How"use memo"marks functions for optimization](#how-use-memo-marks)
  - [When to use"use memo"](#when-to-use)
- [Usage](#usage)
  - [Working with different compilation modes](#compilation-modes)
- [Troubleshooting](#troubleshooting)
  - [Verifying optimization](#verifying-optimization)
  - [See also](#see-also)

---

## Reference

### "use memo"

Add `"use memo"` at the beginning of a function to mark it for React Compiler optimization.

 $

```
function MyComponent() {  "use memo";  // ...}
```

/$

When a function contains `"use memo"`, the React Compiler will analyze and optimize it during build time. The compiler will automatically memoize values and components to prevent unnecessary re-computations and re-renders.

#### Caveats

- `"use memo"` must be at the very beginning of a function body, before any imports or other code (comments are OK).
- The directive must be written with double or single quotes, not backticks.
- The directive must exactly match `"use memo"`.
- Only the first directive in a function is processed; additional directives are ignored.
- The effect of the directive depends on your [compilationMode](https://react.dev/reference/react-compiler/compilationMode) setting.

### How"use memo"marks functions for optimization

In a React app that uses the React Compiler, functions are analyzed at build time to determine if they can be optimized. By default, the compiler automatically infers which components to memoize, but this can depend on your [compilationMode](https://react.dev/reference/react-compiler/compilationMode) setting if you’ve set it.

`"use memo"` explicitly marks a function for optimization, overriding the default behavior:

- In `annotation` mode: Only functions with `"use memo"` are optimized
- In `infer` mode: The compiler uses heuristics, but `"use memo"` forces optimization
- In `all` mode: Everything is optimized by default, making `"use memo"` redundant

The directive creates a clear boundary in your codebase between optimized and non-optimized code, giving you fine-grained control over the compilation process.

### When to use"use memo"

You should consider using `"use memo"` when:

#### You’re using annotation mode

In `compilationMode: 'annotation'`, the directive is required for any function you want optimized:

 $

```
// ✅ This component will be optimizedfunction OptimizedList() {  "use memo";  // ...}// ❌ This component won't be optimizedfunction SimpleWrapper() {  // ...}
```

/$

#### You’re gradually adopting React Compiler

Start with `annotation` mode and selectively optimize stable components:

 $

```
// Start by optimizing leaf componentsfunction Button({ onClick, children }) {  "use memo";  // ...}// Gradually move up the tree as you verify behaviorfunction ButtonGroup({ buttons }) {  "use memo";  // ...}
```

/$

---

## Usage

### Working with different compilation modes

The behavior of `"use memo"` changes based on your compiler configuration:

 $

```
// babel.config.jsmodule.exports = {  plugins: [    ['babel-plugin-react-compiler', {      compilationMode: 'annotation' // or 'infer' or 'all'    }]  ]};
```

/$

#### Annotation mode

 $

```
// ✅ Optimized with "use memo"function ProductCard({ product }) {  "use memo";  // ...}// ❌ Not optimized (no directive)function ProductList({ products }) {  // ...}
```

/$

#### Infer mode (default)

 $

```
// Automatically memoized because this is named like a Componentfunction ComplexDashboard({ data }) {  // ...}// Skipped: Is not named like a Componentfunction simpleDisplay({ text }) {  // ...}
```

/$

In `infer` mode, the compiler automatically detects components and hooks by their naming patterns (PascalCase for components, `use` prefix for hooks). If a component or hook isn’t being compiled in `infer` mode, you should fix its naming convention rather than forcing compilation with `"use memo"`.

---

## Troubleshooting

### Verifying optimization

To confirm your component is being optimized:

1. Check the compiled output in your build
2. Use React DevTools to check for Memo ✨ badge

### See also

- ["use no memo"](https://react.dev/reference/react-compiler/directives/use-no-memo) - Opt out of compilation
- [compilationMode](https://react.dev/reference/react-compiler/compilationMode) - Configure compilation behavior
- [React Compiler](https://react.dev/learn/react-compiler) - Getting started guide

[PreviousDirectives](https://react.dev/reference/react-compiler/directives)[Next"use no memo"](https://react.dev/reference/react-compiler/directives/use-no-memo)
