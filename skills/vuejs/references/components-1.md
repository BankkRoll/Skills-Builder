# Async Components​ and more

# Async Components​

> Vue.js - The Progressive JavaScript Framework

# Async Components​

## Basic Usage​

In large applications, we may need to divide the app into smaller chunks and only load a component from the server when it's needed. To make that possible, Vue has a [defineAsyncComponent](https://vuejs.org/api/general#defineasynccomponent) function:

js

```
import { defineAsyncComponent } from 'vue'

const AsyncComp = defineAsyncComponent(() => {
  return new Promise((resolve, reject) => {
    // ...load component from server
    resolve(/* loaded component */)
  })
})
// ... use `AsyncComp` like a normal component
```

As you can see, `defineAsyncComponent` accepts a loader function that returns a Promise. The Promise's `resolve` callback should be called when you have retrieved your component definition from the server. You can also call `reject(reason)` to indicate the load has failed.

[ES module dynamic import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import) also returns a Promise, so most of the time we will use it in combination with `defineAsyncComponent`. Bundlers like Vite and webpack also support the syntax (and will use it as bundle split points), so we can use it to import Vue SFCs:

js

```
import { defineAsyncComponent } from 'vue'

const AsyncComp = defineAsyncComponent(() =>
  import('./components/MyComponent.vue')
)
```

The resulting `AsyncComp` is a wrapper component that only calls the loader function when it is actually rendered on the page. In addition, it will pass along any props and slots to the inner component, so you can use the async wrapper to seamlessly replace the original component while achieving lazy loading.

As with normal components, async components can be [registered globally](https://vuejs.org/guide/components/registration#global-registration) using `app.component()`:

js

```
app.component('MyComponent', defineAsyncComponent(() =>
  import('./components/MyComponent.vue')
))
```

You can also use `defineAsyncComponent` when [registering a component locally](https://vuejs.org/guide/components/registration#local-registration):

vue

```
<script>
import { defineAsyncComponent } from 'vue'

export default {
  components: {
    AdminPage: defineAsyncComponent(() =>
      import('./components/AdminPageComponent.vue')
    )
  }
}
</script>

<template>
  <AdminPage />
</template>
```

They can also be defined directly inside their parent component:

vue

```
<script setup>
import { defineAsyncComponent } from 'vue'

const AdminPage = defineAsyncComponent(() =>
  import('./components/AdminPageComponent.vue')
)
</script>

<template>
  <AdminPage />
</template>
```

## Loading and Error States​

Asynchronous operations inevitably involve loading and error states - `defineAsyncComponent()` supports handling these states via advanced options:

js

```
const AsyncComp = defineAsyncComponent({
  // the loader function
  loader: () => import('./Foo.vue'),

  // A component to use while the async component is loading
  loadingComponent: LoadingComponent,
  // Delay before showing the loading component. Default: 200ms.
  delay: 200,

  // A component to use if the load fails
  errorComponent: ErrorComponent,
  // The error component will be displayed if a timeout is
  // provided and exceeded. Default: Infinity.
  timeout: 3000
})
```

If a loading component is provided, it will be displayed first while the inner component is being loaded. There is a default 200ms delay before the loading component is shown - this is because on fast networks, an instant loading state may get replaced too fast and end up looking like a flicker.

If an error component is provided, it will be displayed when the Promise returned by the loader function is rejected. You can also specify a timeout to show the error component when the request is taking too long.

## Lazy Hydration​

> This section only applies if you are using [Server-Side Rendering](https://vuejs.org/guide/scaling-up/ssr).

In Vue 3.5+, async components can control when they are hydrated by providing a hydration strategy.

- Vue provides a number of built-in hydration strategies. These built-in strategies need to be individually imported so they can be tree-shaken if not used.
- The design is intentionally low-level for flexibility. Compiler syntax sugar can potentially be built on top of this in the future either in core or in higher level solutions (e.g. Nuxt).

### Hydrate on Idle​

Hydrates via `requestIdleCallback`:

js

```
import { defineAsyncComponent, hydrateOnIdle } from 'vue'

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: hydrateOnIdle(/* optionally pass a max timeout */)
})
```

### Hydrate on Visible​

Hydrate when element(s) become visible via `IntersectionObserver`.

js

```
import { defineAsyncComponent, hydrateOnVisible } from 'vue'

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: hydrateOnVisible()
})
```

Can optionally pass in an options object value for the observer:

js

```
hydrateOnVisible({ rootMargin: '100px' })
```

### Hydrate on Media Query​

Hydrates when the specified media query matches.

js

```
import { defineAsyncComponent, hydrateOnMediaQuery } from 'vue'

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: hydrateOnMediaQuery('(max-width:500px)')
})
```

### Hydrate on Interaction​

Hydrates when specified event(s) are triggered on the component element(s). The event that triggered the hydration will also be replayed once hydration is complete.

js

```
import { defineAsyncComponent, hydrateOnInteraction } from 'vue'

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: hydrateOnInteraction('click')
})
```

Can also be a list of multiple event types:

js

```
hydrateOnInteraction(['wheel', 'mouseover'])
```

### Custom Strategy​

ts

```
import { defineAsyncComponent, type HydrationStrategy } from 'vue'

const myStrategy: HydrationStrategy = (hydrate, forEachElement) => {
  // forEachElement is a helper to iterate through all the root elements
  // in the component's non-hydrated DOM, since the root can be a fragment
  // instead of a single element
  forEachElement(el => {
    // ...
  })
  // call `hydrate` when ready
  hydrate()
  return () => {
    // return a teardown function if needed
  }
}

const AsyncComp = defineAsyncComponent({
  loader: () => import('./Comp.vue'),
  hydrate: myStrategy
})
```

## Using with Suspense​

Async components can be used with the `<Suspense>` built-in component. The interaction between `<Suspense>` and async components is documented in the [dedicated chapter for<Suspense>](https://vuejs.org/guide/built-ins/suspense).

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/components/async.md)

---

# Fallthrough Attributes​

> Vue.js - The Progressive JavaScript Framework

# Fallthrough Attributes​

> This page assumes you've already read the [Components Basics](https://vuejs.org/guide/essentials/component-basics). Read that first if you are new to components.

## Attribute Inheritance​

A "fallthrough attribute" is an attribute or `v-on` event listener that is passed to a component, but is not explicitly declared in the receiving component's [props](https://vuejs.org/guide/components/props) or [emits](https://vuejs.org/guide/components/events#declaring-emitted-events). Common examples of this include `class`, `style`, and `id` attributes.

When a component renders a single root element, fallthrough attributes will be automatically added to the root element's attributes. For example, given a `<MyButton>` component with the following template:

template

```

<button>Click Me</button>
```

And a parent using this component with:

template

```
<MyButton class="large" />
```

The final rendered DOM would be:

html

```
<button class="large">Click Me</button>
```

Here, `<MyButton>` did not declare `class` as an accepted prop. Therefore, `class` is treated as a fallthrough attribute and automatically added to `<MyButton>`'s root element.

### classandstyleMerging​

If the child component's root element already has existing `class` or `style` attributes, it will be merged with the `class` and `style` values that are inherited from the parent. Suppose we change the template of `<MyButton>` in the previous example to:

template

```

<button class="btn">Click Me</button>
```

Then the final rendered DOM would now become:

html

```
<button class="btn large">Click Me</button>
```

### v-onListener Inheritance​

The same rule applies to `v-on` event listeners:

template

```
<MyButton @click="onClick" />
```

The `click` listener will be added to the root element of `<MyButton>`, i.e. the native `<button>` element. When the native `<button>` is clicked, it will trigger the `onClick` method of the parent component. If the native `<button>` already has a `click` listener bound with `v-on`, then both listeners will trigger.

### Nested Component Inheritance​

If a component renders another component as its root node, for example, we refactored `<MyButton>` to render a `<BaseButton>` as its root:

template

```

<BaseButton />
```

Then the fallthrough attributes received by `<MyButton>` will be automatically forwarded to `<BaseButton>`.

Note that:

1. Forwarded attributes do not include any attributes that are declared as props, or `v-on` listeners of declared events by `<MyButton>` - in other words, the declared props and listeners have been "consumed" by `<MyButton>`.
2. Forwarded attributes may be accepted as props by `<BaseButton>`, if declared by it.

## Disabling Attribute Inheritance​

If you do **not** want a component to automatically inherit attributes, you can set `inheritAttrs: false` in the component's options.

Since 3.3 you can also use [defineOptions](https://vuejs.org/api/sfc-script-setup#defineoptions) directly in `<script setup>`:

vue

```
<script setup>
defineOptions({
  inheritAttrs: false
})
// ...setup logic
</script>
```

The common scenario for disabling attribute inheritance is when attributes need to be applied to other elements besides the root node. By setting the `inheritAttrs` option to `false`, you can take full control over where the fallthrough attributes should be applied.

These fallthrough attributes can be accessed directly in template expressions as `$attrs`:

template

```
<span>Fallthrough attributes: {{ $attrs }}</span>
```

The `$attrs` object includes all attributes that are not declared by the component's `props` or `emits` options (e.g., `class`, `style`, `v-on` listeners, etc.).

Some notes:

- Unlike props, fallthrough attributes preserve their original casing in JavaScript, so an attribute like `foo-bar` needs to be accessed as `$attrs['foo-bar']`.
- A `v-on` event listener like `@click` will be exposed on the object as a function under `$attrs.onClick`.

Using our `<MyButton>` component example from the [previous section](#attribute-inheritance) - sometimes we may need to wrap the actual `<button>` element with an extra `<div>` for styling purposes:

template

```
<div class="btn-wrapper">
  <button class="btn">Click Me</button>
</div>
```

We want all fallthrough attributes like `class` and `v-on` listeners to be applied to the inner `<button>`, not the outer `<div>`. We can achieve this with `inheritAttrs: false` and `v-bind="$attrs"`:

template

```
<div class="btn-wrapper">
  <button class="btn" v-bind="$attrs">Click Me</button>
</div>
```

Remember that [v-bindwithout an argument](https://vuejs.org/guide/essentials/template-syntax#dynamically-binding-multiple-attributes) binds all the properties of an object as attributes of the target element.

## Attribute Inheritance on Multiple Root Nodes​

Unlike components with a single root node, components with multiple root nodes do not have an automatic attribute fallthrough behavior. If `$attrs` are not bound explicitly, a runtime warning will be issued.

template

```
<CustomLayout id="custom-layout" @click="changeValue" />
```

If `<CustomLayout>` has the following multi-root template, there will be a warning because Vue cannot be sure where to apply the fallthrough attributes:

template

```
<header>...</header>
<main>...</main>
<footer>...</footer>
```

The warning will be suppressed if `$attrs` is explicitly bound:

template

```
<header>...</header>
<main v-bind="$attrs">...</main>
<footer>...</footer>
```

## Accessing Fallthrough Attributes in JavaScript​

If needed, you can access a component's fallthrough attributes in `<script setup>` using the `useAttrs()` API:

vue

```
<script setup>
import { useAttrs } from 'vue'

const attrs = useAttrs()
</script>
```

If not using `<script setup>`, `attrs` will be exposed as a property of the `setup()` context:

js

```
export default {
  setup(props, ctx) {
    // fallthrough attributes are exposed as ctx.attrs
    console.log(ctx.attrs)
  }
}
```

Note that although the `attrs` object here always reflects the latest fallthrough attributes, it isn't reactive (for performance reasons). You cannot use watchers to observe its changes. If you need reactivity, use a prop. Alternatively, you can use `onUpdated()` to perform side effects with the latest `attrs` on each update.

If needed, you can access a component's fallthrough attributes via the `$attrs` instance property:

js

```
export default {
  created() {
    console.log(this.$attrs)
  }
}
```

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/components/attrs.md)

---

# Component Events​

> Vue.js - The Progressive JavaScript Framework

# Component Events​

> This page assumes you've already read the [Components Basics](https://vuejs.org/guide/essentials/component-basics). Read that first if you are new to components.

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/defining-custom-events-emits?friend=vuejs)

## Emitting and Listening to Events​

A component can emit custom events directly in template expressions (e.g. in a `v-on` handler) using the built-in `$emit` method:

template

```

<button @click="$emit('someEvent')">Click Me</button>
```

The `$emit()` method is also available on the component instance as `this.$emit()`:

js

```
export default {
  methods: {
    submit() {
      this.$emit('someEvent')
    }
  }
}
```

The parent can then listen to it using `v-on`:

template

```
<MyComponent @some-event="callback" />
```

The `.once` modifier is also supported on component event listeners:

template

```
<MyComponent @some-event.once="callback" />
```

Like components and props, event names provide an automatic case transformation. Notice we emitted a camelCase event, but can listen for it using a kebab-cased listener in the parent. As with [props casing](https://vuejs.org/guide/components/props#prop-name-casing), we recommend using kebab-cased event listeners in templates.

TIP

Unlike native DOM events, component emitted events do **not** bubble. You can only listen to the events emitted by a direct child component. If there is a need to communicate between sibling or deeply nested components, use an external event bus or a [global state management solution](https://vuejs.org/guide/scaling-up/state-management).

## Event Arguments​

It's sometimes useful to emit a specific value with an event. For example, we may want the `<BlogPost>` component to be in charge of how much to enlarge the text by. In those cases, we can pass extra arguments to `$emit` to provide this value:

template

```
<button @click="$emit('increaseBy', 1)">
  Increase by 1
</button>
```

Then, when we listen to the event in the parent, we can use an inline arrow function as the listener, which allows us to access the event argument:

template

```
<MyButton @increase-by="(n) => count += n" />
```

Or, if the event handler is a method:

template

```
<MyButton @increase-by="increaseCount" />
```

Then the value will be passed as the first parameter of that method:

js

```
methods: {
  increaseCount(n) {
    this.count += n
  }
}
```

js

```
function increaseCount(n) {
  count.value += n
}
```

TIP

All extra arguments passed to `$emit()` after the event name will be forwarded to the listener. For example, with `$emit('foo', 1, 2, 3)` the listener function will receive three arguments.

## Declaring Emitted Events​

A component can explicitly declare the events it will emit using the [defineEmits()](https://vuejs.org/api/sfc-script-setup#defineprops-defineemits) macro[emits](https://vuejs.org/api/options-state#emits) option:

vue

```
<script setup>
defineEmits(['inFocus', 'submit'])
</script>
```

The `$emit` method that we used in the `<template>` isn't accessible within the `<script setup>` section of a component, but `defineEmits()` returns an equivalent function that we can use instead:

vue

```
<script setup>
const emit = defineEmits(['inFocus', 'submit'])

function buttonClick() {
  emit('submit')
}
</script>
```

The `defineEmits()` macro **cannot** be used inside a function, it must be placed directly within `<script setup>`, as in the example above.

If you're using an explicit `setup` function instead of `<script setup>`, events should be declared using the [emits](https://vuejs.org/api/options-state#emits) option, and the `emit` function is exposed on the `setup()` context:

js

```
export default {
  emits: ['inFocus', 'submit'],
  setup(props, ctx) {
    ctx.emit('submit')
  }
}
```

As with other properties of the `setup()` context, `emit` can safely be destructured:

js

```
export default {
  emits: ['inFocus', 'submit'],
  setup(props, { emit }) {
    emit('submit')
  }
}
```

js

```
export default {
  emits: ['inFocus', 'submit']
}
```

The `emits` option and `defineEmits()` macro also support an object syntax. If using TypeScript you can type arguments, which allows us to perform runtime validation of the payload of the emitted events:

vue

```
<script setup lang="ts">
const emit = defineEmits({
  submit(payload: { email: string, password: string }) {
    // return `true` or `false` to indicate
    // validation pass / fail
  }
})
</script>
```

If you are using TypeScript with `<script setup>`, it's also possible to declare emitted events using pure type annotations:

vue

```
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'change', id: number): void
  (e: 'update', value: string): void
}>()
</script>
```

More details: [Typing Component Emits](https://vuejs.org/guide/typescript/composition-api#typing-component-emits)

js

```
export default {
  emits: {
    submit(payload: { email: string, password: string }) {
      // return `true` or `false` to indicate
      // validation pass / fail
    }
  }
}
```

See also: [Typing Component Emits](https://vuejs.org/guide/typescript/options-api#typing-component-emits)

Although optional, it is recommended to define all emitted events in order to better document how a component should work. It also allows Vue to exclude known listeners from [fallthrough attributes](https://vuejs.org/guide/components/attrs#v-on-listener-inheritance), avoiding edge cases caused by DOM events manually dispatched by 3rd party code.

TIP

If a native event (e.g., `click`) is defined in the `emits` option, the listener will now only listen to component-emitted `click` events and no longer respond to native `click` events.

## Events Validation​

Similar to prop type validation, an emitted event can be validated if it is defined with the object syntax instead of the array syntax.

To add validation, the event is assigned a function that receives the arguments passed to the `this.$emit``emit` call and returns a boolean to indicate whether the event is valid or not.

vue

```
<script setup>
const emit = defineEmits({
  // No validation
  click: null,

  // Validate submit event
  submit: ({ email, password }) => {
    if (email && password) {
      return true
    } else {
      console.warn('Invalid submit event payload!')
      return false
    }
  }
})

function submitForm(email, password) {
  emit('submit', { email, password })
}
</script>
```

js

```
export default {
  emits: {
    // No validation
    click: null,

    // Validate submit event
    submit: ({ email, password }) => {
      if (email && password) {
        return true
      } else {
        console.warn('Invalid submit event payload!')
        return false
      }
    }
  },
  methods: {
    submitForm(email, password) {
      this.$emit('submit', { email, password })
    }
  }
}
```

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/components/events.md)

---

# Props​

> Vue.js - The Progressive JavaScript Framework

# Props​

> This page assumes you've already read the [Components Basics](https://vuejs.org/guide/essentials/component-basics). Read that first if you are new to components.

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/vue-3-reusable-components-with-props?friend=vuejs)

## Props Declaration​

Vue components require explicit props declaration so that Vue knows what external props passed to the component should be treated as fallthrough attributes (which will be discussed in [its dedicated section](https://vuejs.org/guide/components/attrs)).

In SFCs using `<script setup>`, props can be declared using the `defineProps()` macro:

vue

```
<script setup>
const props = defineProps(['foo'])

console.log(props.foo)
</script>
```

In non-`<script setup>` components, props are declared using the [props](https://vuejs.org/api/options-state#props) option:

js

```
export default {
  props: ['foo'],
  setup(props) {
    // setup() receives props as the first argument.
    console.log(props.foo)
  }
}
```

Notice the argument passed to `defineProps()` is the same as the value provided to the `props` options: the same props options API is shared between the two declaration styles.

Props are declared using the [props](https://vuejs.org/api/options-state#props) option:

js

```
export default {
  props: ['foo'],
  created() {
    // props are exposed on `this`
    console.log(this.foo)
  }
}
```

In addition to declaring props using an array of strings, we can also use the object syntax:

js

```
export default {
  props: {
    title: String,
    likes: Number
  }
}
```

js

```
// in <script setup>
defineProps({
  title: String,
  likes: Number
})
```

js

```
// in non-<script setup>
export default {
  props: {
    title: String,
    likes: Number
  }
}
```

For each property in the object declaration syntax, the key is the name of the prop, while the value should be the constructor function of the expected type.

This not only documents your component, but will also warn other developers using your component in the browser console if they pass the wrong type. We will discuss more details about [prop validation](#prop-validation) further down this page.

See also: [Typing Component Props](https://vuejs.org/guide/typescript/options-api#typing-component-props)

If you are using TypeScript with `<script setup>`, it's also possible to declare props using pure type annotations:

vue

```
<script setup lang="ts">
defineProps<{
  title?: string
  likes?: number
}>()
</script>
```

More details: [Typing Component Props](https://vuejs.org/guide/typescript/composition-api#typing-component-props)

## Reactive Props Destructure​

Vue's reactivity system tracks state usage based on property access. E.g. when you access `props.foo` in a computed getter or a watcher, the `foo` prop gets tracked as a dependency.

So, given the following code:

js

```
const { foo } = defineProps(['foo'])

watchEffect(() => {
  // runs only once before 3.5
  // re-runs when the "foo" prop changes in 3.5+
  console.log(foo)
})
```

In version 3.4 and below, `foo` is an actual constant and will never change. In version 3.5 and above, Vue's compiler automatically prepends `props.` when code in the same `<script setup>` block accesses variables destructured from `defineProps`. Therefore the code above becomes equivalent to the following:

js

```
const props = defineProps(['foo'])

watchEffect(() => {
  // `foo` transformed to `props.foo` by the compiler
  console.log(props.foo)
})
```

In addition, you can use JavaScript's native default value syntax to declare default values for the props. This is particularly useful when using the type-based props declaration:

ts

```
const { foo = 'hello' } = defineProps<{ foo?: string }>()
```

If you prefer to have more visual distinction between destructured props and normal variables in your IDE, Vue's VSCode extension provides a setting to enable inlay-hints for destructured props.

### Passing Destructured Props into Functions​

When we pass a destructured prop into a function, e.g.:

js

```
const { foo } = defineProps(['foo'])

watch(foo, /* ... */)
```

This will not work as expected because it is equivalent to `watch(props.foo, ...)` - we are passing a value instead of a reactive data source to `watch`. In fact, Vue's compiler will catch such cases and throw a warning.

Similar to how we can watch a normal prop with `watch(() => props.foo, ...)`, we can watch a destructured prop also by wrapping it in a getter:

js

```
watch(() => foo, /* ... */)
```

In addition, this is the recommended approach when we need to pass a destructured prop into an external function while retaining reactivity:

js

```
useComposable(() => foo)
```

The external function can call the getter (or normalize it with [toValue](https://vuejs.org/api/reactivity-utilities#tovalue)) when it needs to track changes of the provided prop, e.g. in a computed or watcher getter.

## Prop Passing Details​

### Prop Name Casing​

We declare long prop names using camelCase because this avoids having to use quotes when using them as property keys, and allows us to reference them directly in template expressions because they are valid JavaScript identifiers:

js

```
defineProps({
  greetingMessage: String
})
```

js

```
export default {
  props: {
    greetingMessage: String
  }
}
```

template

```
<span>{{ greetingMessage }}</span>
```

Technically, you can also use camelCase when passing props to a child component (except in [in-DOM templates](https://vuejs.org/guide/essentials/component-basics#in-dom-template-parsing-caveats)). However, the convention is using kebab-case in all cases to align with HTML attributes:

template

```
<MyComponent greeting-message="hello" />
```

We use [PascalCase for component tags](https://vuejs.org/guide/components/registration#component-name-casing) when possible because it improves template readability by differentiating Vue components from native elements. However, there isn't as much practical benefit in using camelCase when passing props, so we choose to follow each language's conventions.

### Static vs. Dynamic Props​

So far, you've seen props passed as static values, like in:

template

```
<BlogPost title="My journey with Vue" />
```

You've also seen props assigned dynamically with `v-bind` or its `:` shortcut, such as in:

template

```

<BlogPost :title="post.title" />

<BlogPost :title="post.title + ' by ' + post.author.name" />
```

### Passing Different Value Types​

In the two examples above, we happen to pass string values, but *any* type of value can be passed to a prop.

#### Number​

template

```

<BlogPost :likes="42" />

<BlogPost :likes="post.likes" />
```

#### Boolean​

template

```

<BlogPost is-published />

<BlogPost :is-published="false" />

<BlogPost :is-published="post.isPublished" />
```

#### Array​

template

```

<BlogPost :comment-ids="[234, 266, 273]" />

<BlogPost :comment-ids="post.commentIds" />
```

#### Object​

template

```

<BlogPost
  :author="{
    name: 'Veronica',
    company: 'Veridian Dynamics'
  }"
 />

<BlogPost :author="post.author" />
```

### Binding Multiple Properties Using an Object​

If you want to pass all the properties of an object as props, you can use [v-bindwithout an argument](https://vuejs.org/guide/essentials/template-syntax#dynamically-binding-multiple-attributes) (`v-bind` instead of `:prop-name`). For example, given a `post` object:

js

```
export default {
  data() {
    return {
      post: {
        id: 1,
        title: 'My Journey with Vue'
      }
    }
  }
}
```

js

```
const post = {
  id: 1,
  title: 'My Journey with Vue'
}
```

The following template:

template

```
<BlogPost v-bind="post" />
```

Will be equivalent to:

template

```
<BlogPost :id="post.id" :title="post.title" />
```

## One-Way Data Flow​

All props form a **one-way-down binding** between the child property and the parent one: when the parent property updates, it will flow down to the child, but not the other way around. This prevents child components from accidentally mutating the parent's state, which can make your app's data flow harder to understand.

In addition, every time the parent component is updated, all props in the child component will be refreshed with the latest value. This means you should **not** attempt to mutate a prop inside a child component. If you do, Vue will warn you in the console:

js

```
const props = defineProps(['foo'])

// ❌ warning, props are readonly!
props.foo = 'bar'
```

js

```
export default {
  props: ['foo'],
  created() {
    // ❌ warning, props are readonly!
    this.foo = 'bar'
  }
}
```

There are usually two cases where it's tempting to mutate a prop:

1. **The prop is used to pass in an initial value; the child component wants to use it as a local data property afterwards.** In this case, it's best to define a local data property that uses the prop as its initial value:
  js
  ```
  const props = defineProps(['initialCounter'])
  // counter only uses props.initialCounter as the initial value;
  // it is disconnected from future prop updates.
  const counter = ref(props.initialCounter)
  ```
  js
  ```
  export default {
    props: ['initialCounter'],
    data() {
      return {
        // counter only uses this.initialCounter as the initial value;
        // it is disconnected from future prop updates.
        counter: this.initialCounter
      }
    }
  }
  ```
2. **The prop is passed in as a raw value that needs to be transformed.** In this case, it's best to define a computed property using the prop's value:
  js
  ```
  const props = defineProps(['size'])
  // computed property that auto-updates when the prop changes
  const normalizedSize = computed(() => props.size.trim().toLowerCase())
  ```
  js
  ```
  export default {
    props: ['size'],
    computed: {
      // computed property that auto-updates when the prop changes
      normalizedSize() {
        return this.size.trim().toLowerCase()
      }
    }
  }
  ```

### Mutating Object / Array Props​

When objects and arrays are passed as props, while the child component cannot mutate the prop binding, it **will** be able to mutate the object or array's nested properties. This is because in JavaScript objects and arrays are passed by reference, and it is unreasonably expensive for Vue to prevent such mutations.

The main drawback of such mutations is that it allows the child component to affect parent state in a way that isn't obvious to the parent component, potentially making it more difficult to reason about the data flow in the future. As a best practice, you should avoid such mutations unless the parent and child are tightly coupled by design. In most cases, the child should [emit an event](https://vuejs.org/guide/components/events) to let the parent perform the mutation.

## Prop Validation​

Components can specify requirements for their props, such as the types you've already seen. If a requirement is not met, Vue will warn you in the browser's JavaScript console. This is especially useful when developing a component that is intended to be used by others.

To specify prop validations, you can provide an object with validation requirements to the `defineProps()` macro`props` option, instead of an array of strings. For example:

js

```
defineProps({
  // Basic type check
  //  (`null` and `undefined` values will allow any type)
  propA: Number,
  // Multiple possible types
  propB: [String, Number],
  // Required string
  propC: {
    type: String,
    required: true
  },
  // Required but nullable string
  propD: {
    type: [String, null],
    required: true
  },
  // Number with a default value
  propE: {
    type: Number,
    default: 100
  },
  // Object with a default value
  propF: {
    type: Object,
    // Object or array defaults must be returned from
    // a factory function. The function receives the raw
    // props received by the component as the argument.
    default(rawProps) {
      return { message: 'hello' }
    }
  },
  // Custom validator function
  // full props passed as 2nd argument in 3.4+
  propG: {
    validator(value, props) {
      // The value must match one of these strings
      return ['success', 'warning', 'danger'].includes(value)
    }
  },
  // Function with a default value
  propH: {
    type: Function,
    // Unlike object or array default, this is not a factory
    // function - this is a function to serve as a default value
    default() {
      return 'Default function'
    }
  }
})
```

TIP

Code inside the `defineProps()` argument **cannot access other variables declared in<script setup>**, because the entire expression is moved to an outer function scope when compiled.

js

```
export default {
  props: {
    // Basic type check
    //  (`null` and `undefined` values will allow any type)
    propA: Number,
    // Multiple possible types
    propB: [String, Number],
    // Required string
    propC: {
      type: String,
      required: true
    },
    // Required but nullable string
    propD: {
      type: [String, null],
      required: true
    },
    // Number with a default value
    propE: {
      type: Number,
      default: 100
    },
    // Object with a default value
    propF: {
      type: Object,
      // Object or array defaults must be returned from
      // a factory function. The function receives the raw
      // props received by the component as the argument.
      default(rawProps) {
        return { message: 'hello' }
      }
    },
    // Custom validator function
    // full props passed as 2nd argument in 3.4+
    propG: {
      validator(value, props) {
        // The value must match one of these strings
        return ['success', 'warning', 'danger'].includes(value)
      }
    },
    // Function with a default value
    propH: {
      type: Function,
      // Unlike object or array default, this is not a factory
      // function - this is a function to serve as a default value
      default() {
        return 'Default function'
      }
    }
  }
}
```

Additional details:

- All props are optional by default, unless `required: true` is specified.
- An absent optional prop other than `Boolean` will have `undefined` value.
- The `Boolean` absent props will be cast to `false`. You can change this by setting a `default` for it — i.e.: `default: undefined` to behave as a non-Boolean prop.
- If a `default` value is specified, it will be used if the resolved prop value is `undefined` - this includes both when the prop is absent, or an explicit `undefined` value is passed.

When prop validation fails, Vue will produce a console warning (if using the development build).

If using [Type-based props declarations](https://vuejs.org/api/sfc-script-setup#type-only-props-emit-declarations) , Vue will try its best to compile the type annotations into equivalent runtime prop declarations. For example, `defineProps<{ msg: string }>` will be compiled into `{ msg: { type: String, required: true }}`.

Note

Note that props are validated **before** a component instance is created, so instance properties (e.g. `data`, `computed`, etc.) will not be available inside `default` or `validator` functions.

### Runtime Type Checks​

The `type` can be one of the following native constructors:

- `String`
- `Number`
- `Boolean`
- `Array`
- `Object`
- `Date`
- `Function`
- `Symbol`
- `Error`

In addition, `type` can also be a custom class or constructor function and the assertion will be made with an `instanceof` check. For example, given the following class:

js

```
class Person {
  constructor(firstName, lastName) {
    this.firstName = firstName
    this.lastName = lastName
  }
}
```

You could use it as a prop's type:

js

```
defineProps({
  author: Person
})
```

js

```
export default {
  props: {
    author: Person
  }
}
```

Vue will use `instanceof Person` to validate whether the value of the `author` prop is indeed an instance of the `Person` class.

### Nullable Type​

If the type is required but nullable, you can use the array syntax that includes `null`:

js

```
defineProps({
  id: {
    type: [String, null],
    required: true
  }
})
```

js

```
export default {
  props: {
    id: {
      type: [String, null],
      required: true
    }
  }
}
```

Note that if `type` is just `null` without using the array syntax, it will allow any type.

## Boolean Casting​

Props with `Boolean` type have special casting rules to mimic the behavior of native boolean attributes. Given a `<MyComponent>` with the following declaration:

js

```
defineProps({
  disabled: Boolean
})
```

js

```
export default {
  props: {
    disabled: Boolean
  }
}
```

The component can be used like this:

template

```

<MyComponent disabled />

<MyComponent />
```

When a prop is declared to allow multiple types, the casting rules for `Boolean` will also be applied. However, there is an edge when both `String` and `Boolean` are allowed - the Boolean casting rule only applies if Boolean appears before String:

js

```
// disabled will be casted to true
defineProps({
  disabled: [Boolean, Number]
})

// disabled will be casted to true
defineProps({
  disabled: [Boolean, String]
})

// disabled will be casted to true
defineProps({
  disabled: [Number, Boolean]
})

// disabled will be parsed as an empty string (disabled="")
defineProps({
  disabled: [String, Boolean]
})
```

js

```
// disabled will be casted to true
export default {
  props: {
    disabled: [Boolean, Number]
  }
}

// disabled will be casted to true
export default {
  props: {
    disabled: [Boolean, String]
  }
}

// disabled will be casted to true
export default {
  props: {
    disabled: [Number, Boolean]
  }
}

// disabled will be parsed as an empty string (disabled="")
export default {
  props: {
    disabled: [String, Boolean]
  }
}
```

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/components/props.md)
