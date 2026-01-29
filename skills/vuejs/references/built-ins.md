# KeepAlive​ and more

# KeepAlive​

> Vue.js - The Progressive JavaScript Framework

# KeepAlive​

`<KeepAlive>` is a built-in component that allows us to conditionally cache component instances when dynamically switching between multiple components.

## Basic Usage​

In the Component Basics chapter, we introduced the syntax for [Dynamic Components](https://vuejs.org/guide/essentials/component-basics#dynamic-components), using the `<component>` special element:

template

```
<component :is="activeComponent" />
```

By default, an active component instance will be unmounted when switching away from it. This will cause any changed state it holds to be lost. When this component is displayed again, a new instance will be created with only the initial state.

In the example below, we have two stateful components - A contains a counter, while B contains a message synced with an input via `v-model`. Try updating the state of one of them, switch away, and then switch back to it:

 A B[

Current component: A

Count: 0]

You'll notice that when switched back, the previous changed state would have been reset.

Creating fresh component instance on switch is normally useful behavior, but in this case, we'd really like the two component instances to be preserved even when they are inactive. To solve this problem, we can wrap our dynamic component with the `<KeepAlive>` built-in component:

template

```

<KeepAlive>
  <component :is="activeComponent" />
</KeepAlive>
```

Now, the state will be persisted across component switches:

 A B[

Current component: A

Count: 0]

[Try it in the Playground](https://play.vuejs.org/#eNqtUsFOwzAM/RWrl4IGC+cqq2h3RFw495K12YhIk6hJi1DVf8dJSllBaAJxi+2XZz8/j0lhzHboeZIl1NadMA4sd73JKyVaozsHI9hnJqV+feJHmODY6RZS/JEuiL1uTTEXtiREnnINKFeAcgZUqtbKOqj7ruPKwe6s2VVguq4UJXEynAkDx1sjmeMYAdBGDFBLZu2uShre6ioJeaxIduAyp0KZ3oF7MxwRHWsEQmC4bXXDJWbmxpjLBiZ7DwptMUFyKCiJNP/BWUbO8gvnA+emkGKIgkKqRrRWfh+Z8MIWwpySpfbxn6wJKMGV4IuSs0UlN1HVJae7bxYvBuk+2IOIq7sLnph8P9u5DJv5VfpWWLaGqTzwZTCOM/M0IaMvBMihd04ruK+lqF/8Ajxms8EFbCiJxR8khsP6ncQosLWnWV6a/kUf2nqu75Fby04chA0iPftaYryhz6NBRLjdtajpHZTWPio=)

[Try it in the Playground](https://play.vuejs.org/#eNqtU8tugzAQ/JUVl7RKWveMXFTIseofcHHAiawasPxArRD/3rVNSEhbpVUrIWB3x7PM7jAkuVL3veNJmlBTaaFsVraiUZ22sO0alcNedw2s7kmIPHS1ABQLQDEBAMqWvwVQzffMSQuDz1aI6VreWpPCEBtsJppx4wE1s+zmNoIBNLdOt8cIjzut8XAKq3A0NAIY/QNveFEyi8DA8kZJZjlGALQWPVSSGfNYJjVvujIJeaxItuMyo6JVzoJ9VxwRmtUCIdDfNV3NJWam5j7HpPOY8BEYkwxySiLLP1AWkbK4oHzmXOVS9FFOSM3jhFR4WTNfRslcO54nSwJKcCD4RsnZmJJNFPXJEl8t88quOuc39fCrHalsGyWcnJL62apYNoq12UQ8DLEFjCMy+kKA7Jy1XQtPlRTVqx+Jx6zXOJI1JbH4jejg3T+KbswBzXnFlz9Tjes/V/3CjWEHDsL/OYNvdCE8Wu3kLUQEhy+ljh+brFFu)

TIP

When used in [in-DOM templates](https://vuejs.org/guide/essentials/component-basics#in-dom-template-parsing-caveats), it should be referenced as `<keep-alive>`.

## Include / Exclude​

By default, `<KeepAlive>` will cache any component instance inside. We can customize this behavior via the `include` and `exclude` props. Both props can be a comma-delimited string, a `RegExp`, or an array containing either types:

template

```

<KeepAlive include="a,b">
  <component :is="view" />
</KeepAlive>

<KeepAlive :include="/a|b/">
  <component :is="view" />
</KeepAlive>

<KeepAlive :include="['a', 'b']">
  <component :is="view" />
</KeepAlive>
```

The match is checked against the component's [name](https://vuejs.org/api/options-misc#name) option, so components that need to be conditionally cached by `KeepAlive` must explicitly declare a `name` option.

TIP

Since version 3.2.34, a single-file component using `<script setup>` will automatically infer its `name` option based on the filename, removing the need to manually declare the name.

## Max Cached Instances​

We can limit the maximum number of component instances that can be cached via the `max` prop. When `max` is specified, `<KeepAlive>` behaves like an [LRU cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_(LRU)): if the number of cached instances is about to exceed the specified max count, the least recently accessed cached instance will be destroyed to make room for the new one.

template

```
<KeepAlive :max="10">
  <component :is="activeComponent" />
</KeepAlive>
```

## Lifecycle of Cached Instance​

When a component instance is removed from the DOM but is part of a component tree cached by `<KeepAlive>`, it goes into a **deactivated** state instead of being unmounted. When a component instance is inserted into the DOM as part of a cached tree, it is **activated**.

A kept-alive component can register lifecycle hooks for these two states using [onActivated()](https://vuejs.org/api/composition-api-lifecycle#onactivated) and [onDeactivated()](https://vuejs.org/api/composition-api-lifecycle#ondeactivated):

vue

```
<script setup>
import { onActivated, onDeactivated } from 'vue'

onActivated(() => {
  // called on initial mount
  // and every time it is re-inserted from the cache
})

onDeactivated(() => {
  // called when removed from the DOM into the cache
  // and also when unmounted
})
</script>
```

A kept-alive component can register lifecycle hooks for these two states using [activated](https://vuejs.org/api/options-lifecycle#activated) and [deactivated](https://vuejs.org/api/options-lifecycle#deactivated) hooks:

js

```
export default {
  activated() {
    // called on initial mount
    // and every time it is re-inserted from the cache
  },
  deactivated() {
    // called when removed from the DOM into the cache
    // and also when unmounted
  }
}
```

Note that:

- `onActivated``activated` is also called on mount, and `onDeactivated``deactivated` on unmount.
- Both hooks work for not only the root component cached by `<KeepAlive>`, but also the descendant components in the cached tree.

---

**Related**

- [<KeepAlive>API reference](https://vuejs.org/api/built-in-components#keepalive)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/built-ins/keep-alive.md)

---

# Suspense​

> Vue.js - The Progressive JavaScript Framework

# Suspense​

Experimental Feature

`<Suspense>` is an experimental feature. It is not guaranteed to reach stable status and the API may change before it does.

`<Suspense>` is a built-in component for orchestrating async dependencies in a component tree. It can render a loading state while waiting for multiple nested async dependencies down the component tree to be resolved.

## Async Dependencies​

To explain the problem `<Suspense>` is trying to solve and how it interacts with these async dependencies, let's imagine a component hierarchy like the following:

```
<Suspense>
└─ <Dashboard>
   ├─ <Profile>
   │  └─ <FriendStatus> (component with async setup())
   └─ <Content>
      ├─ <ActivityFeed> (async component)
      └─ <Stats> (async component)
```

In the component tree there are multiple nested components whose rendering depends on some async resource to be resolved first. Without `<Suspense>`, each of them will need to handle its own loading / error and loaded states. In the worst case scenario, we may see three loading spinners on the page, with content displayed at different times.

The `<Suspense>` component gives us the ability to display top-level loading / error states while we wait on these nested async dependencies to be resolved.

There are two types of async dependencies that `<Suspense>` can wait on:

1. Components with an async `setup()` hook. This includes components using `<script setup>` with top-level `await` expressions.
2. [Async Components](https://vuejs.org/guide/components/async).

### async setup()​

A Composition API component's `setup()` hook can be async:

js

```
export default {
  async setup() {
    const res = await fetch(...)
    const posts = await res.json()
    return {
      posts
    }
  }
}
```

If using `<script setup>`, the presence of top-level `await` expressions automatically makes the component an async dependency:

vue

```
<script setup>
const res = await fetch(...)
const posts = await res.json()
</script>

<template>
  {{ posts }}
</template>
```

### Async Components​

Async components are **"suspensible"** by default. This means that if it has a `<Suspense>` in the parent chain, it will be treated as an async dependency of that `<Suspense>`. In this case, the loading state will be controlled by the `<Suspense>`, and the component's own loading, error, delay and timeout options will be ignored.

The async component can opt-out of `Suspense` control and let the component always control its own loading state by specifying `suspensible: false` in its options.

## Loading State​

The `<Suspense>` component has two slots: `#default` and `#fallback`. Both slots only allow for **one** immediate child node. The node in the default slot is shown if possible. If not, the node in the fallback slot will be shown instead.

template

```
<Suspense>
  
  <Dashboard />

  
  <template #fallback>
    Loading...
  </template>
</Suspense>
```

On initial render, `<Suspense>` will render its default slot content in memory. If any async dependencies are encountered during the process, it will enter a **pending** state. During the pending state, the fallback content will be displayed. When all encountered async dependencies have been resolved, `<Suspense>` enters a **resolved** state and the resolved default slot content is displayed.

If no async dependencies were encountered during the initial render, `<Suspense>` will directly go into a resolved state.

Once in a resolved state, `<Suspense>` will only revert to a pending state if the root node of the `#default` slot is replaced. New async dependencies nested deeper in the tree will **not** cause the `<Suspense>` to revert to a pending state.

When a revert happens, fallback content will not be immediately displayed. Instead, `<Suspense>` will display the previous `#default` content while waiting for the new content and its async dependencies to be resolved. This behavior can be configured with the `timeout` prop: `<Suspense>` will switch to fallback content if it takes longer than `timeout` milliseconds to render the new default content. A `timeout` value of `0` will cause the fallback content to be displayed immediately when default content is replaced.

## Events​

The `<Suspense>` component emits 3 events: `pending`, `resolve` and `fallback`. The `pending` event occurs when entering a pending state. The `resolve` event is emitted when new content has finished resolving in the `default` slot. The `fallback` event is fired when the contents of the `fallback` slot are shown.

The events could be used, for example, to show a loading indicator in front of the old DOM while new components are loading.

## Error Handling​

`<Suspense>` currently does not provide error handling via the component itself - however, you can use the [errorCaptured](https://vuejs.org/api/options-lifecycle#errorcaptured) option or the [onErrorCaptured()](https://vuejs.org/api/composition-api-lifecycle#onerrorcaptured) hook to capture and handle async errors in the parent component of `<Suspense>`.

## Combining with Other Components​

It is common to want to use `<Suspense>` in combination with the [<Transition>](https://vuejs.org/guide/built-ins/transition) and [<KeepAlive>](https://vuejs.org/guide/built-ins/keep-alive) components. The nesting order of these components is important to get them all working correctly.

In addition, these components are often used in conjunction with the `<RouterView>` component from [Vue Router](https://router.vuejs.org/).

The following example shows how to nest these components so that they all behave as expected. For simpler combinations you can remove the components that you don't need:

template

```
<RouterView v-slot="{ Component }">
  <template v-if="Component">
    <Transition mode="out-in">
      <KeepAlive>
        <Suspense>
          
          <component :is="Component"></component>

          
          <template #fallback>
            Loading...
          </template>
        </Suspense>
      </KeepAlive>
    </Transition>
  </template>
</RouterView>
```

Vue Router has built-in support for [lazily loading components](https://router.vuejs.org/guide/advanced/lazy-loading.html) using dynamic imports. These are distinct from async components and currently they will not trigger `<Suspense>`. However, they can still have async components as descendants and those can trigger `<Suspense>` in the usual way.

## Nested Suspense​

- Only supported in 3.3+

When we have multiple async components (common for nested or layout-based routes) like this:

template

```
<Suspense>
  <component :is="DynamicAsyncOuter">
    <component :is="DynamicAsyncInner" />
  </component>
</Suspense>
```

`<Suspense>` creates a boundary that will resolve all the async components down the tree, as expected. However, when we change `DynamicAsyncOuter`, `<Suspense>` awaits it correctly, but when we change `DynamicAsyncInner`, the nested `DynamicAsyncInner` renders an empty node until it has been resolved (instead of the previous one or fallback slot).

In order to solve that, we could have a nested suspense to handle the patch for the nested component, like:

template

```
<Suspense>
  <component :is="DynamicAsyncOuter">
    <Suspense suspensible> 
      <component :is="DynamicAsyncInner" />
    </Suspense>
  </component>
</Suspense>
```

If you don't set the `suspensible` prop, the inner `<Suspense>` will be treated like a sync component by the parent `<Suspense>`. That means that it has its own fallback slot and if both `Dynamic` components change at the same time, there might be empty nodes and multiple patching cycles while the child `<Suspense>` is loading its own dependency tree, which might not be desirable. When it's set, all the async dependency handling is given to the parent `<Suspense>` (including the events emitted) and the inner `<Suspense>` serves solely as another boundary for the dependency resolution and patching.

---

**Related**

- [<Suspense>API reference](https://vuejs.org/api/built-in-components#suspense)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/built-ins/suspense.md)

---

# Teleport​

> Vue.js - The Progressive JavaScript Framework

# Teleport​

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/vue-3-teleport?friend=vuejs)

`<Teleport>` is a built-in component that allows us to "teleport" a part of a component's template into a DOM node that exists outside the DOM hierarchy of that component.

## Basic Usage​

Sometimes a part of a component's template belongs to it logically, but from a visual standpoint, it should be displayed somewhere else in the DOM, perhaps even outside of the Vue application.

The most common example of this is when building a full-screen modal. Ideally, we want the code for the modal's button and the modal itself to be written within the same single-file component, since they are both related to the open / close state of the modal. But that means the modal will be rendered alongside the button, deeply nested in the application's DOM hierarchy. This can create some tricky issues when positioning the modal via CSS.

Consider the following HTML structure.

template

```
<div class="outer">
  <h3>Vue Teleport Example</h3>
  <div>
    <MyModal />
  </div>
</div>
```

And here is the implementation of `<MyModal>`:

vue

```
<script setup>
import { ref } from 'vue'

const open = ref(false)
</script>

<template>
  <button @click="open = true">Open Modal</button>

  <div v-if="open" class="modal">
    <p>Hello from the modal!</p>
    <button @click="open = false">Close</button>
  </div>
</template>

<style scoped>
.modal {
  position: fixed;
  z-index: 999;
  top: 20%;
  left: 50%;
  width: 300px;
  margin-left: -150px;
}
</style>
```

vue

```
<script>
export default {
  data() {
    return {
      open: false
    }
  }
}
</script>

<template>
  <button @click="open = true">Open Modal</button>

  <div v-if="open" class="modal">
    <p>Hello from the modal!</p>
    <button @click="open = false">Close</button>
  </div>
</template>

<style scoped>
.modal {
  position: fixed;
  z-index: 999;
  top: 20%;
  left: 50%;
  width: 300px;
  margin-left: -150px;
}
</style>
```

The component contains a `<button>` to trigger the opening of the modal, and a `<div>` with a class of `.modal`, which will contain the modal's content and a button to self-close.

When using this component inside the initial HTML structure, there are a number of potential issues:

- `position: fixed` only places the element relative to the viewport when no ancestor element has `transform`, `perspective` or `filter` property set. If, for example, we intend to animate the ancestor `<div class="outer">` with a CSS transform, it would break the modal layout!
- The modal's `z-index` is constrained by its containing elements. If there is another element that overlaps with `<div class="outer">` and has a higher `z-index`, it would cover our modal.

`<Teleport>` provides a clean way to work around these, by allowing us to break out of the nested DOM structure. Let's modify `<MyModal>` to use `<Teleport>`:

template

```
<button @click="open = true">Open Modal</button>

<Teleport to="body">
  <div v-if="open" class="modal">
    <p>Hello from the modal!</p>
    <button @click="open = false">Close</button>
  </div>
</Teleport>
```

The `to` target of `<Teleport>` expects a CSS selector string or an actual DOM node. Here, we are essentially telling Vue to "**teleport** this template fragment **to** the **body** tag".

You can click the button below and inspect the `<body>` tag via your browser's devtools:

You can combine `<Teleport>` with [<Transition>](https://vuejs.org/guide/built-ins/transition) to create animated modals - see [Example here](https://vuejs.org/examples/#modal).

TIP

The teleport `to` target must be already in the DOM when the `<Teleport>` component is mounted. Ideally, this should be an element outside the entire Vue application. If targeting another element rendered by Vue, you need to make sure that element is mounted before the `<Teleport>`.

## Using with Components​

`<Teleport>` only alters the rendered DOM structure - it does not affect the logical hierarchy of the components. That is to say, if `<Teleport>` contains a component, that component will remain a logical child of the parent component containing the `<Teleport>`. Props passing and event emitting will continue to work the same way.

This also means that injections from a parent component work as expected, and that the child component will be nested below the parent component in the Vue Devtools, instead of being placed where the actual content moved to.

## Disabling Teleport​

In some cases, we may want to conditionally disable `<Teleport>`. For example, we may want to render a component as an overlay for desktop, but inline on mobile. `<Teleport>` supports the `disabled` prop which can be dynamically toggled:

template

```
<Teleport :disabled="isMobile">
  ...
</Teleport>
```

We could then dynamically update `isMobile`.

## Multiple Teleports on the Same Target​

A common use case would be a reusable `<Modal>` component, with the potential for multiple instances to be active at the same time. For this kind of scenario, multiple `<Teleport>` components can mount their content to the same target element. The order will be a simple append, with later mounts located after earlier ones, but all within the target element.

Given the following usage:

template

```
<Teleport to="#modals">
  <div>A</div>
</Teleport>
<Teleport to="#modals">
  <div>B</div>
</Teleport>
```

The rendered result would be:

html

```
<div id="modals">
  <div>A</div>
  <div>B</div>
</div>
```

## Deferred Teleport​

In Vue 3.5 and above, we can use the `defer` prop to defer the target resolving of a Teleport until other parts of the application have mounted. This allows the Teleport to target a container element that is rendered by Vue, but in a later part of the component tree:

template

```
<Teleport defer to="#late-div">...</Teleport>

<div id="late-div"></div>
```

Note that the target element must be rendered in the same mount / update tick with the Teleport - i.e. if the `<div>` is only mounted a second later, the Teleport will still report an error. The defer works similarly to the `mounted` lifecycle hook.

---

**Related**

- [<Teleport>API reference](https://vuejs.org/api/built-in-components#teleport)
- [Handling Teleports in SSR](https://vuejs.org/guide/scaling-up/ssr#teleports)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/built-ins/teleport.md)

---

# TransitionGroup​

> Vue.js - The Progressive JavaScript Framework

# TransitionGroup​

`<TransitionGroup>` is a built-in component designed for animating the insertion, removal, and order change of elements or components that are rendered in a list.

## Differences from<Transition>​

`<TransitionGroup>` supports the same props, CSS transition classes, and JavaScript hook listeners as `<Transition>`, with the following differences:

- By default, it doesn't render a wrapper element. But you can specify an element to be rendered with the `tag` prop.
- [Transition modes](https://vuejs.org/guide/built-ins/transition#transition-modes) are not available, because we are no longer alternating between mutually exclusive elements.
- Elements inside are **always required** to have a unique `key` attribute.
- CSS transition classes will be applied to individual elements in the list, **not** to the group / container itself.

TIP

When used in [in-DOM templates](https://vuejs.org/guide/essentials/component-basics#in-dom-template-parsing-caveats), it should be referenced as `<transition-group>`.

## Enter / Leave Transitions​

Here is an example of applying enter / leave transitions to a `v-for` list using `<TransitionGroup>`:

template

```
<TransitionGroup name="list" tag="ul">
  <li v-for="item in items" :key="item">
    {{ item }}
  </li>
</TransitionGroup>
```

css

```
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
```

- 1
- 2
- 3
- 4
- 5

## Move Transitions​

The above demo has some obvious flaws: when an item is inserted or removed, its surrounding items instantly "jump" into place instead of moving smoothly. We can fix this by adding a few additional CSS rules:

css

```
.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  position: absolute;
}
```

Now it looks much better - even animating smoothly when the whole list is shuffled:

- 1
- 2
- 3
- 4
- 5

[Full Example](https://vuejs.org/examples/#list-transition)

### Custom TransitionGroup classes​

You can also specify custom transition classes for the moving element by passing the `moveClass` prop to `<TransitionGroup>`, just like [custom transition classes on<Transition>](https://vuejs.org/guide/built-ins/transition#custom-transition-classes).

## Staggering List Transitions​

By communicating with JavaScript transitions through data attributes, it's also possible to stagger transitions in a list. First, we render the index of an item as a data attribute on the DOM element:

template

```
<TransitionGroup
  tag="ul"
  :css="false"
  @before-enter="onBeforeEnter"
  @enter="onEnter"
  @leave="onLeave"
>
  <li
    v-for="(item, index) in computedList"
    :key="item.msg"
    :data-index="index"
  >
    {{ item.msg }}
  </li>
</TransitionGroup>
```

Then, in JavaScript hooks, we animate the element with a delay based on the data attribute. This example is using the [GSAP library](https://gsap.com/) to perform the animation:

js

```
function onEnter(el, done) {
  gsap.to(el, {
    opacity: 1,
    height: '1.6em',
    delay: el.dataset.index * 0.15,
    onComplete: done
  })
}
```

- Bruce Lee
- Jackie Chan
- Chuck Norris
- Jet Li
- Kung Fury

[Full Example in the Playground](https://play.vuejs.org/#eNqlVMuu0zAQ/ZVRNklRm7QLWETtBW4FSFCxYkdYmGSSmjp28KNQVfl3xk7SFyvEponPGc+cOTPNOXrbdenRYZRHa1Nq3lkwaF33VEjedkpbOIPGeg6lajtnsYIeaq1aiOlSfAlqDOtG3L8SUchSSWNBcPrZwNdCAqVqTZND/KxdibBDjKGf3xIfWXngCNs9k4/Udu/KA3xWWnPz1zW0sOOP6CcnG3jv9ImIQn67SvrpUJ9IE/WVxPHsSkw97gbN0zFJZrB5grNPrskcLUNXac2FRZ0k3GIbIvxLSsVTq3bqF+otM5jMUi5L4So0SSicHplwOKOyfShdO1lariQo+Yy10vhO+qwoZkNFFKmxJ4Gp6ljJrRe+vMP3yJu910swNXqXcco1h0pJHDP6CZHEAAcAYMydwypYCDAkJRdX6Sts4xGtUDAKotIVs9Scpd4q/A0vYJmuXo5BSm7JOIEW81DVo77VR207ZEf8F23LB23T+X9VrbNh82nn6UAz7ASzSCeANZe0AnBctIqqbIoojLCIIBvoL5pJw31DH7Ry3VDKsoYinSii4ZyXxhBQM2Fwwt58D7NeoB8QkXfDvwRd2XtceOsCHkwc8KCINAk+vADJppQUFjZ0DsGVGT3uFn1KSjoPeKLoaYtvCO/rIlz3vH9O5FiU/nXny/pDT6YGKZngg0/Zg1GErrMbp6N5NHxJFi3N/4dRkj5IYf5ULxCmiPJpI4rIr4kHimhvbWfyLHOyOzQpNZZ57jXNy4nRGFLTR/0fWBqe7w==)

[Full Example in the Playground](https://play.vuejs.org/#eNqtVE2P0zAQ/SujXNqgNmkPcIjaBbYCJKg4cSMcTDJNTB07+KNsVfW/M3aabNpyQltViT1vPPP8Zian6H3bJgeHURatTKF5ax9yyZtWaQuVYS3stGpg4peTXOayUNJYEJwea/ieS4ATNKbKYPKoXYGwRZzAeTYGPrNizxE2NZO30KZ2xR6+Kq25uTuGFrb81vrFyQo+On0kIJc/PCV8CmxL3DEnLJy8e8ksm8bdGkCjdVr2O4DfDvWRgtGN/JYC0SOkKVTTOotl1jv3hi3d+DngENILkey4sKinU26xiWH9AH6REN/Eqq36g3rDDE7jhMtCuBLN1NbcJIFEHN9RaNDWqjQDAyUfcac0fpA+CYoRCRSJsUeBiWpZwe2RSrK4w2rkVe2rdYG6LD5uH3EGpZI4iuurTdwDNBjpRJclg+UlhP914UnMZfIGm8kIKVEwciYivhoGLQlQ4hO8gkWyfD1yVHJDKgu0mAUmPXLuxRkYb5Ed8H8YL/7BeGx7Oa6hkLmk/yodBoo21BKtYBZpB7DikroKDvNGUeZ1HoVmyCNIO/ibZtJwy5X8pJVru9CWVeTpRB51+6wwhgw7Jgz2tnc/Q6/M0ZeWwKvmGZye0Wu78PIGexC6swdGxEnw/q6HOYUkt9DwMwhKxfS6GpY+KPHc45G8+6EYAV7reTjucf/uwUtSmvvTME1wDuISlVTwTqf0RiiyrtKR0tEs6r5l84b645dRkr5zoT8oXwBMHg2Tlke+jbwhj2prW5OlqZPtvkroYqnH3lK9nLgI46scnf8Cn22kBA==)

---

**Related**

- [<TransitionGroup>API reference](https://vuejs.org/api/built-in-components#transitiongroup)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/built-ins/transition-group.md)

---

# Transition​

> Vue.js - The Progressive JavaScript Framework

# Transition​

Vue offers two built-in components that can help work with transitions and animations in response to changing state:

- `<Transition>` for applying animations when an element or component is entering and leaving the DOM. This is covered on this page.
- `<TransitionGroup>` for applying animations when an element or component is inserted into, removed from, or moved within a `v-for` list. This is covered in [the next chapter](https://vuejs.org/guide/built-ins/transition-group).

Aside from these two components, we can also apply animations in Vue using other techniques such as toggling CSS classes or state-driven animations via style bindings. These additional techniques are covered in the [Animation Techniques](https://vuejs.org/guide/extras/animation) chapter.

## The<Transition>Component​

`<Transition>` is a built-in component: this means it is available in any component's template without having to register it. It can be used to apply enter and leave animations on elements or components passed to it via its default slot. The enter or leave can be triggered by one of the following:

- Conditional rendering via `v-if`
- Conditional display via `v-show`
- Dynamic components toggling via the `<component>` special element
- Changing the special `key` attribute

This is an example of the most basic usage:

template

```
<button @click="show = !show">Toggle</button>
<Transition>
  <p v-if="show">hello</p>
</Transition>
```

css

```
/* we will explain what these classes do next! */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
```

hello

[Try it in the Playground](https://play.vuejs.org/#eNpVkEFuwyAQRa8yZZNWqu1sunFJ1N4hSzYUjRNUDAjGVJHluxcCipIV/OG/pxEr+/a+TwuykfGogvYEEWnxR2H17F0gWCHgBBtMwc2wy9WdsMIqZ2OuXtwfHErhlcKCb8LyoVoynwPh7I0kzAmA/yxEzsKXMlr9HgRr9Es5BTue3PlskA+1VpFTkDZq0i3niYfU6anRmbqgMY4PZeH8OjwBfHhYIMdIV1OuferQEoZOKtIJ328TgzJhm8BabHR3jeC8VJqusO8/IqCM+CnsVqR3V/mfRxO5amnkCPuK5B+6rcG2fydshks=)

[Try it in the Playground](https://play.vuejs.org/#eNpVkMFuAiEQhl9lyqlNuouXXrZo2nfwuBeKs0qKQGBAjfHdZZfVrAmB+f/M/2WGK/v1vs0JWcdEVEF72vQWz94Fgh0OMhmCa28BdpLk+0etAQJSCvahAOLBnTqgkLA6t/EpVzmCP7lFEB69kYRFAYi/ROQs/Cij1f+6ZyMG1vA2vj3bbN1+b1Dw2lYj2yBt1KRnXRwPudHDnC6pAxrjBPe1n78EBF8MUGSkixnLNjdoCUMjFemMn5NjUGacnboqPVkdOC+Vpgus2q8IKCN+T+suWENwxyWJXKXMyQ5WNVJ+aBqD3e6VSYoi)

TIP

`<Transition>` only supports a single element or component as its slot content. If the content is a component, the component must also have only one single root element.

When an element in a `<Transition>` component is inserted or removed, this is what happens:

1. Vue will automatically sniff whether the target element has CSS transitions or animations applied. If it does, a number of [CSS transition classes](#transition-classes) will be added / removed at appropriate timings.
2. If there are listeners for [JavaScript hooks](#javascript-hooks), these hooks will be called at appropriate timings.
3. If no CSS transitions / animations are detected and no JavaScript hooks are provided, the DOM operations for insertion and/or removal will be executed on the browser's next animation frame.

## CSS-Based Transitions​

### Transition Classes​

There are six classes applied for enter / leave transitions.

![Transition Diagram](https://vuejs.org/assets/transition-classes.DYG5-69l.png)

1. `v-enter-from`: Starting state for enter. Added before the element is inserted, removed one frame after the element is inserted.
2. `v-enter-active`: Active state for enter. Applied during the entire entering phase. Added before the element is inserted, removed when the transition/animation finishes. This class can be used to define the duration, delay and easing curve for the entering transition.
3. `v-enter-to`: Ending state for enter. Added one frame after the element is inserted (at the same time `v-enter-from` is removed), removed when the transition/animation finishes.
4. `v-leave-from`: Starting state for leave. Added immediately when a leaving transition is triggered, removed after one frame.
5. `v-leave-active`: Active state for leave. Applied during the entire leaving phase. Added immediately when a leaving transition is triggered, removed when the transition/animation finishes. This class can be used to define the duration, delay and easing curve for the leaving transition.
6. `v-leave-to`: Ending state for leave. Added one frame after a leaving transition is triggered (at the same time `v-leave-from` is removed), removed when the transition/animation finishes.

`v-enter-active` and `v-leave-active` give us the ability to specify different easing curves for enter / leave transitions, which we'll see an example of in the following sections.

### Named Transitions​

A transition can be named via the `name` prop:

template

```
<Transition name="fade">
  ...
</Transition>
```

For a named transition, its transition classes will be prefixed with its name instead of `v`. For example, the applied class for the above transition will be `fade-enter-active` instead of `v-enter-active`. The CSS for the fade transition should look like this:

css

```
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
```

### CSS Transitions​

`<Transition>` is most commonly used in combination with [native CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions), as seen in the basic example above. The `transition` CSS property is a shorthand that allows us to specify multiple aspects of a transition, including properties that should be animated, duration of the transition, and [easing curves](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function).

Here is a more advanced example that transitions multiple properties, with different durations and easing curves for enter and leave:

template

```
<Transition name="slide-fade">
  <p v-if="show">hello</p>
</Transition>
```

css

```
/*
  Enter and leave animations can use different
  durations and timing functions.
*/
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
```

hello

[Try it in the Playground](https://play.vuejs.org/#eNqFkc9uwjAMxl/F6wXQKIVNk1AX0HbZC4zDDr2E4EK0NIkStxtDvPviFQ0OSFzyx/m+n+34kL16P+lazMpMRBW0J4hIrV9WVjfeBYIDBKzhCHVwDQySdFDZyipnY5Lu3BcsWDCk0OKosqLoKcmfLoSNN5KQbyTWLZGz8KKMVp+LKju573ivsuXKbbcG4d3oDcI9vMkNiqL3JD+AWAVpoyadGFY2yATW5nVSJj9rkspDl+v6hE/hHRrjRMEdpdfiDEkBUVxWaEWkveHj5AzO0RKGXCrSHcKBIfSPKEEaA9PJYwSUEXPX0nNlj8y6RBiUHd5AzCOodq1VvsYfjWE4G6fgEy/zMcxG17B9ZTyX8bV85C5y1S40ZX/kdj+GD1P/zVQA56XStC9h2idJI/z7huz4CxoVvE4=)

[Try it in the Playground](https://play.vuejs.org/#eNqFkc1uwjAMgF/F6wk0SmHTJNQFtF32AuOwQy+hdSFamkSJ08EQ776EbMAkJKTIf7I/O/Y+ezVm3HvMyoy52gpDi0rh1mhL0GDLvSTYVwqg4cQHw2QDWCRv1Z8H4Db6qwSyHlPkEFUQ4bHixA0OYWckJ4wesZUn0gpeainqz3mVRQzM4S7qKlss9XotEd6laBDu4Y03yIpUE+oB2NJy5QSJwFC8w0iIuXkbMkN9moUZ6HPR/uJDeINSalaYxCjOkBBgxeWEijnayWiOz+AcFaHNeU2ix7QCOiFK4FLCZPzoALnDXHt6Pq7hP0Ii7/EGYuag9itR5yv8FmgH01EIPkUxG8F0eA2bJmut7kbX+pG+6NVq28WTBTN+92PwMDHbSAXQhteCdiVMUpNwwuMassMP8kfAJQ==)

### CSS Animations​

[Native CSS animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations) are applied in the same way as CSS transitions, with the difference being that `*-enter-from` is not removed immediately after the element is inserted, but on an `animationend` event.

For most CSS animations, we can simply declare them under the `*-enter-active` and `*-leave-active` classes. Here's an example:

template

```
<Transition name="bounce">
  <p v-if="show" style="text-align: center;">
    Hello here is some bouncy text!
  </p>
</Transition>
```

css

```
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.25);
  }
  100% {
    transform: scale(1);
  }
}
```

Hello here is some bouncy text!

[Try it in the Playground](https://play.vuejs.org/#eNqNksGOgjAQhl9lJNmoBwRNvCAa97YP4JFLbQZsLG3TDqzG+O47BaOezCYkpfB9/0wHbsm3c4u+w6RIyiC9cgQBqXO7yqjWWU9wA4813KH2toUpo9PKVEZaExg92V/YRmBGvsN5ZcpsTGGfN4St04Iw7qg8dkTWwF5qJc/bKnnYk7hWye5gm0ZjmY0YKwDlwQsTFCnWjGiRpaPtjETG43smHPSpqh9pVQKBrjpyrfCNMilZV8Aqd5cNEF4oFVo1pgCJhtBvnjEAP6i1hRN6BBUg2BZhKHUdvMmjWhYHE9dXY/ygzN4PasqhB75djM2mQ7FUSFI9wi0GCJ6uiHYxVsFUGcgX67CpzP0lahQ9/k/kj9CjDzgG7M94rT1PLLxhQ0D+Na4AFI9QW98WEKTQOMvnLAOwDrD+wC0Xq/Ubusw/sU+QL/45hskk9z8Bddbn)

[Try it in the Playground](https://play.vuejs.org/#eNqNUs2OwiAQfpWxySZ66I8mXioa97YP4LEXrNNKpEBg2tUY330pqOvJmBBgyPczP1yTb2OyocekTJirrTC0qRSejbYEB2x4LwmulQI4cOLTWbwDWKTeqkcE4I76twSyPcaX23j4zS+WP3V9QNgZyQnHiNi+J9IKtrUU9WldJaMMrGEynlWy2em2lcjyCPMUALazXDlBwtMU79CT9rpXNXp4tGYGhlQ0d7UqAUcXOeI6bluhUtKmhEVhzisgPFPKpWhVCTUqQrt6ygD8oJQajmgRhAOnO4RgdQm8yd0tNzGv/D8x/8Dy10IVCzn4axaTTYNZymsSA8YuciU6PrLL6IKpUFBkS7cKXXwQJfIBPyP6IQ1oHUaB7QkvjfUdcy+wIFB8PeZIYwmNtl0JruYSp8XMk+/TXL7BzbPF8gU6L95hn8D4OUJnktsfM1vavg==)

### Custom Transition Classes​

You can also specify custom transition classes by passing the following props to `<Transition>`:

- `enter-from-class`
- `enter-active-class`
- `enter-to-class`
- `leave-from-class`
- `leave-active-class`
- `leave-to-class`

These will override the conventional class names. This is especially useful when you want to combine Vue's transition system with an existing CSS animation library, such as [Animate.css](https://daneden.github.io/animate.css/):

template

```

<Transition
  name="custom-classes"
  enter-active-class="animate__animated animate__tada"
  leave-active-class="animate__animated animate__bounceOutRight"
>
  <p v-if="show">hello</p>
</Transition>
```

[Try it in the Playground](https://play.vuejs.org/#eNqNUctuwjAQ/BXXF9oDsZB6ogbRL6hUcbSEjLMhpn7JXtNWiH/vhqS0R3zxPmbWM+szf02pOVXgSy6LyTYhK4A1rVWwPsWM7MwydOzCuhw9mxF0poIKJoZC0D5+stUAeMRc4UkFKcYpxKcEwSenEYYM5b4ixsA2xlnzsVJ8Yj8Mt+LrbTwcHEgxwojCmNxmHYpFG2kaoxO0B2KaWjD6uXG6FCiKj00ICHmuDdoTjD2CavJBCna7KWjZrYK61b9cB5pI93P3sQYDbxXf7aHHccpVMolO7DS33WSQjPXgXJRi2Cl1xZ8nKkjxf0dBFvx2Q7iZtq94j5jKUgjThmNpjIu17ZzO0JjohT7qL+HsvohJWWNKEc/NolncKt6Goar4y/V7rg/wyw9zrLOy)

[Try it in the Playground](https://play.vuejs.org/#eNqNUcFuwjAM/RUvp+1Ao0k7sYDYF0yaOFZCJjU0LE2ixGFMiH9f2gDbcVKU2M9+tl98Fm8hNMdMYi5U0tEEXraOTsFHho52mC3DuXUAHTI+PlUbIBLn6G4eQOr91xw4ZqrIZXzKVY6S97rFYRqCRabRY7XNzN7BSlujPxetGMvAAh7GtxXLtd/vLSlZ0woFQK0jumTY+FJt7ORwoMLUObEfZtpiSpRaUYPkmOIMNZsj1VhJRWeGMsFmczU6uCOMHd64lrCQ/s/d+uw0vWf+MPuea5Vp5DJ0gOPM7K4Ci7CerPVKhipJ/moqgJJ//8ipxN92NFdmmLbSip45pLmUunOH1Gjrc7ezGKnRfpB4wJO0ZpvkdbJGpyRfmufm+Y4Mxo1oK16n9UwNxOUHwaK3iQ==)

### Using Transitions and Animations Together​

Vue needs to attach event listeners in order to know when a transition has ended. It can either be `transitionend` or `animationend`, depending on the type of CSS rules applied. If you are only using one or the other, Vue can automatically detect the correct type.

However, in some cases you may want to have both on the same element, for example having a CSS animation triggered by Vue, along with a CSS transition effect on hover. In these cases, you will have to explicitly declare the type you want Vue to care about by passing the `type` prop, with a value of either `animation` or `transition`:

template

```
<Transition type="animation">...</Transition>
```

### Nested Transitions and Explicit Transition Durations​

Although the transition classes are only applied to the direct child element in `<Transition>`, we can transition nested elements using nested CSS selectors:

template

```
<Transition name="nested">
  <div v-if="show" class="outer">
    <div class="inner">
      Hello
    </div>
  </div>
</Transition>
```

css

```
/* rules that target nested elements */
.nested-enter-active .inner,
.nested-leave-active .inner {
  transition: all 0.3s ease-in-out;
}

.nested-enter-from .inner,
.nested-leave-to .inner {
  transform: translateX(30px);
  opacity: 0;
}

/* ... other necessary CSS omitted */
```

We can even add a transition delay to the nested element on enter, which creates a staggered enter animation sequence:

css

```
/* delay enter of nested element for staggered effect */
.nested-enter-active .inner {
  transition-delay: 0.25s;
}
```

However, this creates a small issue. By default, the `<Transition>` component attempts to automatically figure out when the transition has finished by listening to the **first** `transitionend` or `animationend` event on the root transition element. With a nested transition, the desired behavior should be waiting until the transitions of all inner elements have finished.

In such cases you can specify an explicit transition duration (in milliseconds) using the `duration` prop on the `<Transition>` component. The total duration should match the delay plus transition duration of the inner element:

template

```
<Transition :duration="550">...</Transition>
```

Hello

[Try it in the Playground](https://play.vuejs.org/#eNqVVd9v0zAQ/leO8LAfrE3HNKSFbgKmSYMHQNAHkPLiOtfEm2NHttN2mvq/c7bTNi1jgFop9t13d9995ziPyfumGc5bTLJkbLkRjQOLrm2uciXqRhsHj2BwBiuYGV3DAUEPcpUrrpUlaKUXcOkBh860eJSrcRqzUDxtHNaNZA5pBzCets5pBe+4FPz+Mk+66Bf+mSdXE12WEsdphMWQiWHKCicoLCtaw/yKIs/PR3kCitVIG4XWYUEJfATFFGIO84GYdRUIyCWzlra6dWg2wA66dgqlts7c+d8tSqk34JTQ6xqb9TjdUiTDOO21TFvrHqRfDkPpExiGKvBITjdl/L40ulVFBi8R8a3P17CiEKrM4GzULIOlFmpQoSgrl8HpKFpX3kFZu2y0BNhJxznvwaJCA1TEYcC4E3MkKp1VIptjZ43E3KajDJiUMBqeWUBmcUBUqJGYOT2GAiV7gJAA9Iy4GyoBKLH2z+N0W3q/CMC2yCCkyajM63Mbc+9z9mfvZD+b071MM23qLC69+j8PvX5HQUDdMC6cL7BOTtQXCJwpas/qHhWIBdYtWGgtDWNttWTmThu701pf1W6+v1Hd8Xbz+k+VQxmv8i7Fv1HZn+g/iv2nRkjzbd6npf/Rkz49DifQ3dLZBBYOJzC4rqgCwsUbmLYlCAUVU4XsCd1NrCeRHcYXb1IJC/RX2hEYCwJTvHYVMZoavbBI09FmU+LiFSzIh0AIXy1mqZiFKaKCmVhiEVJ7GftHZTganUZ56EYLL3FykjhL195MlMM7qxXdmEGDPOG6boRE86UJVPMki+p4H01WLz4Fm78hSdBo5xXy+yfsd3bpbXny1SA1M8c82fgcMyW66L75/hmXtN44a120ktDPOL+h1bL1HCPsA42DaPdwge3HcO/TOCb2ZumQJtA15Yl65Crg84S+BdfPtL6lezY8C3GkZ7L6Bc1zNR0=)

If necessary, you can also specify separate values for enter and leave durations using an object:

template

```
<Transition :duration="{ enter: 500, leave: 800 }">...</Transition>
```

### Performance Considerations​

You may notice that the animations shown above are mostly using properties like `transform` and `opacity`. These properties are efficient to animate because:

1. They do not affect the document layout during the animation, so they do not trigger expensive CSS layout calculation on every animation frame.
2. Most modern browsers can leverage GPU hardware acceleration when animating `transform`.

In comparison, properties like `height` or `margin` will trigger CSS layout, so they are much more expensive to animate, and should be used with caution.

## JavaScript Hooks​

You can hook into the transition process with JavaScript by listening to events on the `<Transition>` component:

template

```
<Transition
  @before-enter="onBeforeEnter"
  @enter="onEnter"
  @after-enter="onAfterEnter"
  @enter-cancelled="onEnterCancelled"
  @before-leave="onBeforeLeave"
  @leave="onLeave"
  @after-leave="onAfterLeave"
  @leave-cancelled="onLeaveCancelled"
>
  
</Transition>
```

js

```
// called before the element is inserted into the DOM.
// use this to set the "enter-from" state of the element
function onBeforeEnter(el) {}

// called one frame after the element is inserted.
// use this to start the entering animation.
function onEnter(el, done) {
  // call the done callback to indicate transition end
  // optional if used in combination with CSS
  done()
}

// called when the enter transition has finished.
function onAfterEnter(el) {}

// called when the enter transition is cancelled before completion.
function onEnterCancelled(el) {}

// called before the leave hook.
// Most of the time, you should just use the leave hook
function onBeforeLeave(el) {}

// called when the leave transition starts.
// use this to start the leaving animation.
function onLeave(el, done) {
  // call the done callback to indicate transition end
  // optional if used in combination with CSS
  done()
}

// called when the leave transition has finished and the
// element has been removed from the DOM.
function onAfterLeave(el) {}

// only available with v-show transitions
function onLeaveCancelled(el) {}
```

js

```
export default {
  // ...
  methods: {
    // called before the element is inserted into the DOM.
    // use this to set the "enter-from" state of the element
    onBeforeEnter(el) {},

    // called one frame after the element is inserted.
    // use this to start the animation.
    onEnter(el, done) {
      // call the done callback to indicate transition end
      // optional if used in combination with CSS
      done()
    },

    // called when the enter transition has finished.
    onAfterEnter(el) {},

    // called when the enter transition is cancelled before completion.
    onEnterCancelled(el) {},

    // called before the leave hook.
    // Most of the time, you should just use the leave hook.
    onBeforeLeave(el) {},

    // called when the leave transition starts.
    // use this to start the leaving animation.
    onLeave(el, done) {
      // call the done callback to indicate transition end
      // optional if used in combination with CSS
      done()
    },

    // called when the leave transition has finished and the
    // element has been removed from the DOM.
    onAfterLeave(el) {},

    // only available with v-show transitions
    onLeaveCancelled(el) {}
  }
}
```

These hooks can be used in combination with CSS transitions / animations or on their own.

When using JavaScript-only transitions, it is usually a good idea to add the `:css="false"` prop. This explicitly tells Vue to skip auto CSS transition detection. Aside from being slightly more performant, this also prevents CSS rules from accidentally interfering with the transition:

template

```
<Transition
  ...
  :css="false"
>
  ...
</Transition>
```

With `:css="false"`, we are also fully responsible for controlling when the transition ends. In this case, the `done` callbacks are required for the `@enter` and `@leave` hooks. Otherwise, the hooks will be called synchronously and the transition will finish immediately.

Here's a demo using the [GSAP library](https://gsap.com/) to perform the animations. You can, of course, use any other animation library you want, for example [Anime.js](https://animejs.com/) or [Motion One](https://motion.dev/):

[Try it in the Playground](https://play.vuejs.org/#eNqNVMtu2zAQ/JUti8I2YD3i1GigKmnaorcCveTQArpQFCWzlkiCpBwHhv+9Sz1qKYckJ3FnlzvD2YVO5KvW4aHlJCGpZUZoB5a7Vt9lUjRaGQcnMLyEM5RGNbDA0sX/VGWpHnB/xEQmmZIWe+zUI9z6m0tnWr7ymbKVzAklQclvvFSG/5COmyWvV3DKJHTdQiRHZN0jAJbRmv9OIA432/UE+jODlKZMuKcErnx8RrazP8woR7I1FEryKaVTU8aiNdRfwWZTQtQwi1HAGF/YB4BTyxNY8JpaJ1go5K/WLTfhdg1Xq8V4SX5Xja65w0ovaCJ8Jvsnpwc+l525F2XH4ac3Cj8mcB3HbxE9qnvFMRzJ0K3APuhIjPefmTTyvWBAGvWbiDuIgeNYRh3HCCDNW+fQmHtWC7a/zciwaO/8NyN3D6qqap5GfVnXAC89GCqt8Bp77vu827+A+53AJrOFzMhQdMnO8dqPpMO74Yx4wqxFtKS1HbBOMdIX4gAMffVp71+Qq2NG4BCIcngBKk8jLOvfGF30IpBGEwcwtO6p9sdwbNXPIadsXxnVyiKB9x83+c3N9WePN9RUQgZO6QQ2sT524KMo3M5Pf4h3XFQ7NwFyZQpuAkML0doEtvEHhPvRDPRkTfq/QNDgRvy1SuIvpFOSDQmbkWTckf7hHsjIzjltkyhqpd5XIVNN5HNfGlW09eAcMp3J+R+pEn7L)

[Try it in the Playground](https://play.vuejs.org/#eNqNVFFvmzAQ/is3pimNlABNF61iaddt2tukvfRhk/xiwIAXsJF9pKmq/PedDTSwh7ZSFLjvzvd9/nz4KfjatuGhE0ES7GxmZIu3TMmm1QahtLyFwugGFu51wRQAU+Lok7koeFcjPDk058gvlv07gBHYGTVGALbSDwmg6USPnNzjtHL/jcBK5zZxxQwZavVNFNqIHwqF8RUAWs2jn4IffCfqQz+mik5lKLWi3GT1hagHRU58aAUSshpV2YzX4ncCcbjZDp099GcG6ZZnEh8TuPR8S0/oTJhQjmQryLUSU0rUU8a8M9wtoWZTQtIwi0nAGJ/ZB0BwKxJYiJpblFko1a8OLzbhdgWXy8WzP99109YCqdIJmgifyfYuzmUzfFF2HH56o/BjAldx/BbRo7pXHKMjGbrl1IcciWn9fyaNfC8YsIueR5wCFFTGUVAEsEs7pOmDu6yW2f6GBW5o4QbeuScLbu91WdZiF/VlvgEtujdcWek09tx3qZ+/tXAzQU1mA8mCoeicneO1OxKP9yM+4ElmLaEFr+2AecVEn8sDZOSrSzv/1qk+sgAOa1kMOyDlu4jK+j1GZ70E7KKJAxRafKzdazi26s8h5dm+NLpTeQLvP27S6+urz/7T5aaUao26TWATt0cPPsgcK3f6Q1wJWVY4AVJtcmHWhueyo89+G38guD+agT5YBf39s25oIv5arehu8krYkLAs8BeG86DfuANYUCG2NomiTrX7Msx0E7ncl0bnXT04566M4PQPykWaWw==)

## Reusable Transitions​

Transitions can be reused through Vue's component system. To create a reusable transition, we can create a component that wraps the `<Transition>` component and passes down the slot content:

MyTransition.vuevue

```
<script>
// JavaScript hooks logic...
</script>

<template>
  
  <Transition
    name="my-transition"
    @enter="onEnter"
    @leave="onLeave">
    <slot></slot> 
  </Transition>
</template>

<style>
/*
  Necessary CSS...
  Note: avoid using <style scoped> here since it
  does not apply to slot content.
*/
</style>
```

Now `MyTransition` can be imported and used just like the built-in version:

template

```
<MyTransition>
  <div v-if="show">Hello</div>
</MyTransition>
```

## Transition on Appear​

If you also want to apply a transition on the initial render of a node, you can add the `appear` prop:

template

```
<Transition appear>
  ...
</Transition>
```

## Transition Between Elements​

In addition to toggling an element with `v-if` / `v-show`, we can also transition between two elements using `v-if` / `v-else` / `v-else-if`, as long as we make sure that there is only one element being shown at any given moment:

template

```
<Transition>
  <button v-if="docState === 'saved'">Edit</button>
  <button v-else-if="docState === 'edited'">Save</button>
  <button v-else-if="docState === 'editing'">Cancel</button>
</Transition>
```

Click to cycle through states:

[Try it in the Playground](https://play.vuejs.org/#eNqdk8tu2zAQRX9loI0SoLLcFN2ostEi6BekmwLa0NTYJkKRBDkSYhj+9wxJO3ZegBGu+Lhz7syQ3Bd/nJtNIxZN0QbplSMISKNbdkYNznqCPXhcwwHW3g5QsrTsTGekNYGgt/KBBCEsouimDGLCvrztTFtnGGN4QTg4zbK4ojY4YSDQTuOiKwbhN8pUXm221MDd3D11xfJeK/kIZEHupEagrbfjZssxzAgNs5nALIC2VxNILUJg1IpMxWmRUAY9U6IZ2/3zwgRFyhowYoieQaseq9ElDaTRrkYiVkyVWrPiXNdiAcequuIkPo3fMub5Sg4l9oqSevmXZ22dwR8YoQ74kdsL4Go7ZTbR74HT/KJfJlxleGrG8l4YifqNYVuf251vqOYr4llbXz4C06b75+ns1a3BPsb0KrBy14Aymnerlbby8Vc8cTajG35uzFITpu0t5ufzHQdeH6LBsezEO0eJVbB6pBiVVLPTU6jQEPpKyMj8dnmgkQs+HmQcvVTIQK1hPrv7GQAFt9eO9Bk6fZ8Ub52Qiri8eUo+4dbWD02exh79v/nBP+H2PStnwz/jelJ1geKvk/peHJ4BoRZYow==)

## Transition Modes​

In the previous example, the entering and leaving elements are animated at the same time, and we had to make them `position: absolute` to avoid the layout issue when both elements are present in the DOM.

However, in some cases this isn't an option, or simply isn't the desired behavior. We may want the leaving element to be animated out first, and for the entering element to only be inserted **after** the leaving animation has finished. Orchestrating such animations manually would be very complicated - luckily, we can enable this behavior by passing `<Transition>` a `mode` prop:

template

```
<Transition mode="out-in">
  ...
</Transition>
```

Here's the previous demo with `mode="out-in"`:

Click to cycle through states:

`<Transition>` also supports `mode="in-out"`, although it's much less frequently used.

## Transition Between Components​

`<Transition>` can also be used around [dynamic components](https://vuejs.org/guide/essentials/component-basics#dynamic-components):

template

```
<Transition name="fade" mode="out-in">
  <component :is="activeComponent"></component>
</Transition>
```

 A  B Component A

[Try it in the Playground](https://play.vuejs.org/#eNqtksFugzAMhl/F4tJNKtDLLoxWKnuDacdcUnC3SCGJiMmEqr77EkgLbXfYYZyI8/v77dinZG9M5npMiqS0dScMgUXqzY4p0RrdEZzAfnEp9fc7HuEMx063sPIZq6viTbdmHy+yfDwF5K2guhFUUcBUnkNvcelBGrjTooHaC7VCRXBAoT6hQTRyAH2w2DlsmKq1sgS8JuEwUCfxdgF7Gqt5ZqrMp+58X/5A2BrJCcOJSskPKP0v+K8UyvQENBjcsqTjjdAsAZe2ukHpI3dm/q5wXPZBPFqxZAf7gCrzGfufDlVwqB4cPjqurCChFSjeBvGRN+iTA9afdE+pUD43FjG/bSHsb667Mr9qJot89vCBMl8+oiotDTL8ZsE39UnYpRN0fQlK5A5jEE6BSVdiAdrwWtAAm+zFAnKLr0ydA3pJDDt0x/PrMrJifgGbKdFPfCwpWU+TuWz5omzfVCNcfJJ5geL8pqtFn5E07u7fSHFOj6TzDyUDNEM=)

[Try it in the Playground](https://play.vuejs.org/#eNqtks9ugzAMxl/F4tJNamGXXVhWqewVduSSgStFCkkUDFpV9d0XJyn9t8MOkxBg5/Pvi+Mci51z5TxhURdi7LxytG2NGpz1BB92cDvYezvAqqxixNLVjaC5ETRZ0Br8jpIe93LSBMfWAHRBYQ0aGms4Jvw6Q05rFvSS5NNzEgN4pMmbcwQgO1Izsj5CalhFRLDj1RN/wis8olpaCQHh4LQk5IiEll+owy+XCGXcREAHh+9t4WWvbFvAvBlsjzpk7gx5TeqJtdG4LbawY5KoLtR/NGjYoHkw+PTSjIqUNWDkwOK97DHUMjVEdqKNMqE272E5dajV+JvpVlSLJllUF4+QENX1ERox0kHzb8m+m1CEfpOgYYgpqVHOmJNpgLQQa7BOdooO8FK+joByxLc4tlsiX6s7HtnEyvU1vKTCMO+4pWKdBnO+0FfbDk31as5HsvR+Hl9auuozk+J1/hspz+mRdPoBYtonzg==)

## Dynamic Transitions​

`<Transition>` props like `name` can also be dynamic! It allows us to dynamically apply different transitions based on state change:

template

```
<Transition :name="transitionName">
  
</Transition>
```

This can be useful when you've defined CSS transitions / animations using Vue's transition class conventions and want to switch between them.

You can also apply different behavior in JavaScript transition hooks based on the current state of your component. Finally, the ultimate way of creating dynamic transitions is through [reusable transition components](#reusable-transitions) that accept props to change the nature of the transition(s) to be used. It may sound cheesy, but the only limit really is your imagination.

## Transitions with the Key Attribute​

Sometimes you need to force the re-render of a DOM element in order for a transition to occur.

Take this counter component for example:

vue

```
<script setup>
import { ref } from 'vue';
const count = ref(0);

setInterval(() => count.value++, 1000);
</script>

<template>
  <Transition>
    <span :key="count">{{ count }}</span>
  </Transition>
</template>
```

vue

```
<script>
export default {
  data() {
    return {
      count: 1,
      interval: null
    }
  },
  mounted() {
    this.interval = setInterval(() => {
      this.count++;
    }, 1000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
  }
}
</script>

<template>
  <Transition>
    <span :key="count">{{ count }}</span>
  </Transition>
</template>
```

If we had excluded the `key` attribute, only the text node would be updated and thus no transition would occur. However, with the `key` attribute in place, Vue knows to create a new `span` element whenever `count` changes and thus the `Transition` component has 2 different elements to transition between.

[Try it in the Playground](https://play.vuejs.org/#eNp9UsFu2zAM/RVCl6Zo4nhYd/GcAtvQQ3fYhq1HXTSFydTKkiDJbjLD/z5KMrKgLXoTHx/5+CiO7JNz1dAja1gbpFcuQsDYuxtuVOesjzCCxx1MsPO2gwuiXnzkhhtpTYggbW8ibBJlUV/mBJXfmYh+EHqxuITNDYzcQGFWBPZ4dUXEaQnv6jrXtOuiTJoUROycFhEpAmi3agCpRQgbzp68cA49ZyV174UJKiprckxIcMJA84hHImc9oo7jPOQ0kQ4RSvH6WXW7JiV6teszfQpDPGqEIK3DLSGpQbazsyaugvqLDVx77JIhbqp5wsxwtrRvPFI7NWDhEGtYYVrQSsgELzOiUQw4I2Vh8TRgA9YJqeIR6upDABQh9TpTAPE7WN3HlxLp084Foi3N54YN1KWEVpOMkkO2ZJHsmp3aVw/BGjqMXJE22jml0X93STRw1pReKSe0tk9fMxZ9nzwVXP5B+fgK/hAOCePsh8dAt4KcnXJR+D3S16X07a9veKD3KdnZba+J/UbyJ+Zl0IyF9rk3Wxr7jJenvcvnrcz+PtweItKuZ1Np0MScMp8zOvkvb1j/P+776jrX0UbZ9A+fYSTP)

[Try it in the Playground](https://play.vuejs.org/#eNp9U8tu2zAQ/JUFTwkSyw6aXlQ7QB85pIe2aHPUhZHWDhOKJMiVYtfwv3dJSpbbBgEMWJydndkdUXvx0bmi71CUYhlqrxzdVAa3znqCBtey0wT7ygA0kuTZeX4G8EidN+MJoLadoRKuLkdAGULfS12C6bSGDB/i3yFx2tiAzaRIjyoUYxesICDdDaczZq1uJrNETY4XFx8G5Uu4WiwW55PBA66txy8YyNvdZFNrlP4o/Jdpbq4M/5bzYxZ8IGydloR8Alg2qmcVGcKqEi9eOoe+EqnExXsvTVCkrBkQxoKTBspn3HFDmprp+32ODA4H9mLCKDD/R2E5Zz9+Ws5PpuBjoJ1GCLV12DASJdKGa2toFtRvLOHaY8vx8DrFMGdiOJvlS48sp3rMHGb1M4xRzGQdYU6REY6rxwHJGdJxwBKsk7WiHSyK9wFQhqh14gDyIVjd0f8Wa2/bUwOyWXwQLGGRWzicuChvKC4F8bpmrTbFU7CGL2zqiJm2Tmn03100DZUox5ddCam1ffmaMPJd3Cnj9SPWz6/gT2EbsUr88Bj4VmAljjWSfoP88mL59tc33PLzsdjaptPMfqP4E1MYPGOmfepMw2Of8NK0d238+JTZ3IfbLSFnPSwVB53udyX4q/38xurTuO+K6/Fqi8MffqhR/A==)

---

**Related**

- [<Transition>API reference](https://vuejs.org/api/built-in-components#transition)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/built-ins/transition.md)
