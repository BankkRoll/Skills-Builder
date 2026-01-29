# Reactivity Fundamentals​ and more

# Reactivity Fundamentals​

> Vue.js - The Progressive JavaScript Framework

# Reactivity Fundamentals​

API Preference

This page and many other chapters later in the guide contain different content for the Options API and the Composition API. Your current preference is Options APIComposition API. You can toggle between the API styles using the "API Preference" switches at the top of the left sidebar.

## Declaring Reactive State​

With the Options API, we use the `data` option to declare reactive state of a component. The option value should be a function that returns an object. Vue will call the function when creating a new component instance, and wrap the returned object in its reactivity system. Any top-level properties of this object are proxied on the component instance (`this` in methods and lifecycle hooks):

js

```
export default {
  data() {
    return {
      count: 1
    }
  },

  // `mounted` is a lifecycle hook which we will explain later
  mounted() {
    // `this` refers to the component instance.
    console.log(this.count) // => 1

    // data can be mutated as well
    this.count = 2
  }
}
```

[Try it in the Playground](https://play.vuejs.org/#eNpFUNFqhDAQ/JXBpzsoHu2j3B2U/oYPpnGtoetGkrW2iP/eRFsPApthd2Zndilex7H8mqioimu0wY16r4W+Rx8ULXVmYsVSC9AaNafz/gcC6RTkHwHWT6IVnne85rI+1ZLr5YJmyG1qG7gIA3Yd2R/LhN77T8y9sz1mwuyYkXazcQI2SiHz/7iP3VlQexeb5KKjEKEe2lPyMIxeSBROohqxVO4E6yV6ppL9xykTy83tOQvd7tnzoZtDwhrBO2GYNFloYWLyxrzPPOi44WWLWUt618txvASUhhRCKSHgbZt2scKy7HfCujGOqWL9BVfOgyI=)

These instance properties are only added when the instance is first created, so you need to ensure they are all present in the object returned by the `data` function. Where necessary, use `null`, `undefined` or some other placeholder value for properties where the desired value isn't yet available.

It is possible to add a new property directly to `this` without including it in `data`. However, properties added this way will not be able to trigger reactive updates.

Vue uses a `$` prefix when exposing its own built-in APIs via the component instance. It also reserves the prefix `_` for internal properties. You should avoid using names for top-level `data` properties that start with either of these characters.

### Reactive Proxy vs. Original​

In Vue 3, data is made reactive by leveraging [JavaScript Proxies](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy). Users coming from Vue 2 should be aware of the following edge case:

js

```
export default {
  data() {
    return {
      someObject: {}
    }
  },
  mounted() {
    const newObject = {}
    this.someObject = newObject

    console.log(newObject === this.someObject) // false
  }
}
```

When you access `this.someObject` after assigning it, the value is a reactive proxy of the original `newObject`. **Unlike in Vue 2, the originalnewObjectis left intact and will not be made reactive: make sure to always access reactive state as a property ofthis.**

## Declaring Reactive State​

### ref()​

In Composition API, the recommended way to declare reactive state is using the [ref()](https://vuejs.org/api/reactivity-core#ref) function:

js

```
import { ref } from 'vue'

const count = ref(0)
```

`ref()` takes the argument and returns it wrapped within a ref object with a `.value` property:

js

```
const count = ref(0)

console.log(count) // { value: 0 }
console.log(count.value) // 0

count.value++
console.log(count.value) // 1
```

> See also: [Typing Refs](https://vuejs.org/guide/typescript/composition-api#typing-ref)

To access refs in a component's template, declare and return them from a component's `setup()` function:

js

```
import { ref } from 'vue'

export default {
  // `setup` is a special hook dedicated for the Composition API.
  setup() {
    const count = ref(0)

    // expose the ref to the template
    return {
      count
    }
  }
}
```

template

```
<div>{{ count }}</div>
```

Notice that we did **not** need to append `.value` when using the ref in the template. For convenience, refs are automatically unwrapped when used inside templates (with a few [caveats](#caveat-when-unwrapping-in-templates)).

You can also mutate a ref directly in event handlers:

template

```
<button @click="count++">
  {{ count }}
</button>
```

For more complex logic, we can declare functions that mutate refs in the same scope and expose them as methods alongside the state:

js

```
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)

    function increment() {
      // .value is needed in JavaScript
      count.value++
    }

    // don't forget to expose the function as well.
    return {
      count,
      increment
    }
  }
}
```

Exposed methods can then be used as event handlers:

template

```
<button @click="increment">
  {{ count }}
</button>
```

Here's the example live on [Codepen](https://codepen.io/vuejs-examples/pen/WNYbaqo), without using any build tools.

### <script setup>​

Manually exposing state and methods via `setup()` can be verbose. Luckily, it can be avoided when using [Single-File Components (SFCs)](https://vuejs.org/guide/scaling-up/sfc). We can simplify the usage with `<script setup>`:

vue

```
<script setup>
import { ref } from 'vue'

const count = ref(0)

function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">
    {{ count }}
  </button>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNo9jUEKgzAQRa8yZKMiaNcllvYe2dgwQqiZhDhxE3L3jrW4/DPvv1/UK8Zhz6juSm82uciwIef4MOR8DImhQMIFKiwpeGgEbQwZsoE2BhsyMUwH0d66475ksuwCgSOb0CNx20ExBCc77POase8NVUN6PBdlSwKjj+vMKAlAvzOzWJ52dfYzGXXpjPoBAKX856uopDGeFfnq8XKp+gWq4FAi)

Top-level imports, variables and functions declared in `<script setup>` are automatically usable in the template of the same component. Think of the template as a JavaScript function declared in the same scope - it naturally has access to everything declared alongside it.

TIP

For the rest of the guide, we will be primarily using SFC + `<script setup>` syntax for the Composition API code examples, as that is the most common usage for Vue developers.

If you are not using SFC, you can still use Composition API with the [setup()](https://vuejs.org/api/composition-api-setup) option.

### Why Refs?​

You might be wondering why we need refs with the `.value` instead of plain variables. To explain that, we will need to briefly discuss how Vue's reactivity system works.

When you use a ref in a template, and change the ref's value later, Vue automatically detects the change and updates the DOM accordingly. This is made possible with a dependency-tracking based reactivity system. When a component is rendered for the first time, Vue **tracks** every ref that was used during the render. Later on, when a ref is mutated, it will **trigger** a re-render for components that are tracking it.

In standard JavaScript, there is no way to detect the access or mutation of plain variables. However, we can intercept the get and set operations of an object's properties using getter and setter methods.

The `.value` property gives Vue the opportunity to detect when a ref has been accessed or mutated. Under the hood, Vue performs the tracking in its getter, and performs triggering in its setter. Conceptually, you can think of a ref as an object that looks like this:

js

```
// pseudo code, not actual implementation
const myRef = {
  _value: 0,
  get value() {
    track()
    return this._value
  },
  set value(newValue) {
    this._value = newValue
    trigger()
  }
}
```

Another nice trait of refs is that unlike plain variables, you can pass refs into functions while retaining access to the latest value and the reactivity connection. This is particularly useful when refactoring complex logic into reusable code.

The reactivity system is discussed in more details in the [Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth) section.

## Declaring Methods​

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/methods-in-vue-3?friend=vuejs)

To add methods to a component instance we use the `methods` option. This should be an object containing the desired methods:

js

```
export default {
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  },
  mounted() {
    // methods can be called in lifecycle hooks, or other methods!
    this.increment()
  }
}
```

Vue automatically binds the `this` value for `methods` so that it always refers to the component instance. This ensures that a method retains the correct `this` value if it's used as an event listener or callback. You should avoid using arrow functions when defining `methods`, as that prevents Vue from binding the appropriate `this` value:

js

```
export default {
  methods: {
    increment: () => {
      // BAD: no `this` access here!
    }
  }
}
```

Just like all other properties of the component instance, the `methods` are accessible from within the component's template. Inside a template they are most commonly used as event listeners:

template

```
<button @click="increment">{{ count }}</button>
```

[Try it in the Playground](https://play.vuejs.org/#eNplj9EKwyAMRX8l+LSx0e65uLL9hy+dZlTWqtg4BuK/z1baDgZicsPJgUR2d656B2QN45P02lErDH6c9QQKn10YCKIwAKqj7nAsPYBHCt6sCUDaYKiBS8lpLuk8/yNSb9XUrKg20uOIhnYXAPV6qhbF6fRvmOeodn6hfzwLKkx+vN5OyIFwdENHmBMAfwQia+AmBy1fV8E2gWBtjOUASInXBcxLvN4MLH0BCe1i4Q==)

In the example above, the method `increment` will be called when the `<button>` is clicked.

### Deep Reactivity​

In Vue, state is deeply reactive by default. This means you can expect changes to be detected even when you mutate nested objects or arrays:

js

```
export default {
  data() {
    return {
      obj: {
        nested: { count: 0 },
        arr: ['foo', 'bar']
      }
    }
  },
  methods: {
    mutateDeeply() {
      // these will work as expected.
      this.obj.nested.count++
      this.obj.arr.push('baz')
    }
  }
}
```

Refs can hold any value type, including deeply nested objects, arrays, or JavaScript built-in data structures like `Map`.

A ref will make its value deeply reactive. This means you can expect changes to be detected even when you mutate nested objects or arrays:

js

```
import { ref } from 'vue'

const obj = ref({
  nested: { count: 0 },
  arr: ['foo', 'bar']
})

function mutateDeeply() {
  // these will work as expected.
  obj.value.nested.count++
  obj.value.arr.push('baz')
}
```

Non-primitive values are turned into reactive proxies via [reactive()](#reactive), which is discussed below.

It is also possible to opt-out of deep reactivity with [shallow refs](https://vuejs.org/api/reactivity-advanced#shallowref). For shallow refs, only `.value` access is tracked for reactivity. Shallow refs can be used for optimizing performance by avoiding the observation cost of large objects, or in cases where the inner state is managed by an external library.

Further reading:

- [Reduce Reactivity Overhead for Large Immutable Structures](https://vuejs.org/guide/best-practices/performance#reduce-reactivity-overhead-for-large-immutable-structures)
- [Integration with External State Systems](https://vuejs.org/guide/extras/reactivity-in-depth#integration-with-external-state-systems)

### DOM Update Timing​

When you mutate reactive state, the DOM is updated automatically. However, it should be noted that the DOM updates are not applied synchronously. Instead, Vue buffers them until the "next tick" in the update cycle to ensure that each component updates only once no matter how many state changes you have made.

To wait for the DOM update to complete after a state change, you can use the [nextTick()](https://vuejs.org/api/general#nexttick) global API:

js

```
import { nextTick } from 'vue'

async function increment() {
  count.value++
  await nextTick()
  // Now the DOM is updated
}
```

js

```
import { nextTick } from 'vue'

export default {
  methods: {
    async increment() {
      this.count++
      await nextTick()
      // Now the DOM is updated
    }
  }
}
```

## reactive()​

There is another way to declare reactive state, with the `reactive()` API. Unlike a ref which wraps the inner value in a special object, `reactive()` makes an object itself reactive:

js

```
import { reactive } from 'vue'

const state = reactive({ count: 0 })
```

> See also: [Typing Reactive](https://vuejs.org/guide/typescript/composition-api#typing-reactive)

Usage in template:

template

```
<button @click="state.count++">
  {{ state.count }}
</button>
```

Reactive objects are [JavaScript Proxies](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) and behave just like normal objects. The difference is that Vue is able to intercept the access and mutation of all properties of a reactive object for reactivity tracking and triggering.

`reactive()` converts the object deeply: nested objects are also wrapped with `reactive()` when accessed. It is also called by `ref()` internally when the ref value is an object. Similar to shallow refs, there is also the [shallowReactive()](https://vuejs.org/api/reactivity-advanced#shallowreactive) API for opting-out of deep reactivity.

### Reactive Proxy vs. Original​

It is important to note that the returned value from `reactive()` is a [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) of the original object, which is not equal to the original object:

js

```
const raw = {}
const proxy = reactive(raw)

// proxy is NOT equal to the original.
console.log(proxy === raw) // false
```

Only the proxy is reactive - mutating the original object will not trigger updates. Therefore, the best practice when working with Vue's reactivity system is to **exclusively use the proxied versions of your state**.

To ensure consistent access to the proxy, calling `reactive()` on the same object always returns the same proxy, and calling `reactive()` on an existing proxy also returns that same proxy:

js

```
// calling reactive() on the same object returns the same proxy
console.log(reactive(raw) === proxy) // true

// calling reactive() on a proxy returns itself
console.log(reactive(proxy) === proxy) // true
```

This rule applies to nested objects as well. Due to deep reactivity, nested objects inside a reactive object are also proxies:

js

```
const proxy = reactive({})

const raw = {}
proxy.nested = raw

console.log(proxy.nested === raw) // false
```

### Limitations ofreactive()​

The `reactive()` API has a few limitations:

1. **Limited value types:** it only works for object types (objects, arrays, and [collection types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects#keyed_collections) such as `Map` and `Set`). It cannot hold [primitive types](https://developer.mozilla.org/en-US/docs/Glossary/Primitive) such as `string`, `number` or `boolean`.
2. **Cannot replace entire object:** since Vue's reactivity tracking works over property access, we must always keep the same reference to the reactive object. This means we can't easily "replace" a reactive object because the reactivity connection to the first reference is lost:
  js
  ```
  let state = reactive({ count: 0 })
  // the above reference ({ count: 0 }) is no longer being tracked
  // (reactivity connection is lost!)
  state = reactive({ count: 1 })
  ```
3. **Not destructure-friendly:** when we destructure a reactive object's primitive type property into local variables, or when we pass that property into a function, we will lose the reactivity connection:
  js
  ```
  const state = reactive({ count: 0 })
  // count is disconnected from state.count when destructured.
  let { count } = state
  // does not affect original state
  count++
  // the function receives a plain number and
  // won't be able to track changes to state.count
  // we have to pass the entire object in to retain reactivity
  callSomeFunction(state.count)
  ```

Due to these limitations, we recommend using `ref()` as the primary API for declaring reactive state.

## Additional Ref Unwrapping Details​

### As Reactive Object Property​

A ref is automatically unwrapped when accessed or mutated as a property of a reactive object. In other words, it behaves like a normal property:

js

```
const count = ref(0)
const state = reactive({
  count
})

console.log(state.count) // 0

state.count = 1
console.log(count.value) // 1
```

If a new ref is assigned to a property linked to an existing ref, it will replace the old ref:

js

```
const otherCount = ref(2)

state.count = otherCount
console.log(state.count) // 2
// original ref is now disconnected from state.count
console.log(count.value) // 1
```

Ref unwrapping only happens when nested inside a deep reactive object. It does not apply when it is accessed as a property of a [shallow reactive object](https://vuejs.org/api/reactivity-advanced#shallowreactive).

### Caveat in Arrays and Collections​

Unlike reactive objects, there is **no** unwrapping performed when the ref is accessed as an element of a reactive array or a native collection type like `Map`:

js

```
const books = reactive([ref('Vue 3 Guide')])
// need .value here
console.log(books[0].value)

const map = reactive(new Map([['count', ref(0)]]))
// need .value here
console.log(map.get('count').value)
```

### Caveat when Unwrapping in Templates​

Ref unwrapping in templates only applies if the ref is a top-level property in the template render context.

In the example below, `count` and `object` are top-level properties, but `object.id` is not:

js

```
const count = ref(0)
const object = { id: ref(1) }
```

Therefore, this expression works as expected:

template

```
{{ count + 1 }}
```

...while this one does **NOT**:

template

```
{{ object.id + 1 }}
```

The rendered result will be `[object Object]1` because `object.id` is not unwrapped when evaluating the expression and remains a ref object. To fix this, we can destructure `id` into a top-level property:

js

```
const { id } = object
```

template

```
{{ id + 1 }}
```

Now the render result will be `2`.

Another thing to note is that a ref does get unwrapped if it is the final evaluated value of a text interpolation (i.e. a `{{ }}` tag), so the following will render `1`:

template

```
{{ object.id }}
```

This is just a convenience feature of text interpolation and is equivalent to `{{ object.id.value }}`.

### Stateful Methods​

In some cases, we may need to dynamically create a method function, for example creating a debounced event handler:

js

```
import { debounce } from 'lodash-es'

export default {
  methods: {
    // Debouncing with Lodash
    click: debounce(function () {
      // ... respond to click ...
    }, 500)
  }
}
```

However, this approach is problematic for components that are reused because a debounced function is **stateful**: it maintains some internal state on the elapsed time. If multiple component instances share the same debounced function, they will interfere with one another.

To keep each component instance's debounced function independent of the others, we can create the debounced version in the `created` lifecycle hook:

js

```
export default {
  created() {
    // each instance now has its own copy of debounced handler
    this.debouncedClick = _.debounce(this.click, 500)
  },
  unmounted() {
    // also a good idea to cancel the timer
    // when the component is removed
    this.debouncedClick.cancel()
  },
  methods: {
    click() {
      // ... respond to click ...
    }
  }
}
```

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/reactivity-fundamentals.md)

---

# Template Refs​

> Vue.js - The Progressive JavaScript Framework

# Template Refs​

While Vue's declarative rendering model abstracts away most of the direct DOM operations for you, there may still be cases where we need direct access to the underlying DOM elements. To achieve this, we can use the special `ref` attribute:

template

```
<input ref="input">
```

`ref` is a special attribute, similar to the `key` attribute discussed in the `v-for` chapter. It allows us to obtain a direct reference to a specific DOM element or child component instance after it's mounted. This may be useful when you want to, for example, programmatically focus an input on component mount, or initialize a 3rd party library on an element.

## Accessing the Refs​

To obtain the reference with Composition API, we can use the [useTemplateRef()](https://vuejs.org/api/composition-api-helpers#usetemplateref)  helper:

vue

```
<script setup>
import { useTemplateRef, onMounted } from 'vue'

// the first argument must match the ref value in the template
const input = useTemplateRef('my-input')

onMounted(() => {
  input.value.focus()
})
</script>

<template>
  <input ref="my-input" />
</template>
```

When using TypeScript, Vue's IDE support and `vue-tsc` will automatically infer the type of `input.value` based on what element or component the matching `ref` attribute is used on.

Usage before 3.5

In versions before 3.5 where `useTemplateRef()` was not introduced, we need to declare a ref with a name that matches the template ref attribute's value:

vue

```
<script setup>
import { ref, onMounted } from 'vue'

// declare a ref to hold the element reference
// the name must match template ref value
const input = ref(null)

onMounted(() => {
  input.value.focus()
})
</script>

<template>
  <input ref="input" />
</template>
```

If not using `<script setup>`, make sure to also return the ref from `setup()`:

js

```
export default {
  setup() {
    const input = ref(null)
    // ...
    return {
      input
    }
  }
}
```

The resulting ref is exposed on `this.$refs`:

vue

```
<script>
export default {
  mounted() {
    this.$refs.input.focus()
  }
}
</script>

<template>
  <input ref="input" />
</template>
```

Note that you can only access the ref **after the component is mounted.** If you try to access `$refs.input``input` in a template expression, it will be `undefined``null` on the first render. This is because the element doesn't exist until after the first render!

If you are trying to watch the changes of a template ref, make sure to account for the case where the ref has `null` value:

js

```
watchEffect(() => {
  if (input.value) {
    input.value.focus()
  } else {
    // not mounted yet, or the element was unmounted (e.g. by v-if)
  }
})
```

See also: [Typing Template Refs](https://vuejs.org/guide/typescript/composition-api#typing-template-refs)

## Ref on Component​

> This section assumes knowledge of [Components](https://vuejs.org/guide/essentials/component-basics). Feel free to skip it and come back later.

`ref` can also be used on a child component. In this case the reference will be that of a component instance:

vue

```
<script setup>
import { useTemplateRef, onMounted } from 'vue'
import Child from './Child.vue'

const childRef = useTemplateRef('child')

onMounted(() => {
  // childRef.value will hold an instance of <Child />
})
</script>

<template>
  <Child ref="child" />
</template>
```

Usage before 3.5vue

```
<script setup>
import { ref, onMounted } from 'vue'
import Child from './Child.vue'

const child = ref(null)

onMounted(() => {
  // child.value will hold an instance of <Child />
})
</script>

<template>
  <Child ref="child" />
</template>
```

vue

```
<script>
import Child from './Child.vue'

export default {
  components: {
    Child
  },
  mounted() {
    // this.$refs.child will hold an instance of <Child />
  }
}
</script>

<template>
  <Child ref="child" />
</template>
```

If the child component is using Options API or not using `<script setup>`, theThe referenced instance will be identical to the child component's `this`, which means the parent component will have full access to every property and method of the child component. This makes it easy to create tightly coupled implementation details between the parent and the child, so component refs should be only used when absolutely needed - in most cases, you should try to implement parent / child interactions using the standard props and emit interfaces first.

An exception here is that components using `<script setup>` are **private by default**: a parent component referencing a child component using `<script setup>` won't be able to access anything unless the child component chooses to expose a public interface using the `defineExpose` macro:

vue

```
<script setup>
import { ref } from 'vue'

const a = 1
const b = ref(2)

// Compiler macros, such as defineExpose, don't need to be imported
defineExpose({
  a,
  b
})
</script>
```

When a parent gets an instance of this component via template refs, the retrieved instance will be of the shape `{ a: number, b: number }` (refs are automatically unwrapped just like on normal instances).

Note that defineExpose must be called before any await operation. Otherwise, properties and methods exposed after the await operation will not be accessible.

See also: [Typing Component Template Refs](https://vuejs.org/guide/typescript/composition-api#typing-component-template-refs)

The `expose` option can be used to limit the access to a child instance:

js

```
export default {
  expose: ['publicData', 'publicMethod'],
  data() {
    return {
      publicData: 'foo',
      privateData: 'bar'
    }
  },
  methods: {
    publicMethod() {
      /* ... */
    },
    privateMethod() {
      /* ... */
    }
  }
}
```

In the above example, a parent referencing this component via template ref will only be able to access `publicData` and `publicMethod`.

## Refs insidev-for​

> Requires v3.5 or above

When `ref` is used inside `v-for`, the corresponding ref should contain an Array value, which will be populated with the elements after mount:

vue

```
<script setup>
import { ref, useTemplateRef, onMounted } from 'vue'

const list = ref([
  /* ... */
])

const itemRefs = useTemplateRef('items')

onMounted(() => console.log(itemRefs.value))
</script>

<template>
  <ul>
    <li v-for="item in list" ref="items">
      {{ item }}
    </li>
  </ul>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNp9UsluwjAQ/ZWRLwQpDepyQoDUIg6t1EWUW91DFAZq6tiWF4oU5d87dtgqVRyyzLw3b+aN3bB7Y4ptQDZkI1dZYTw49MFMuBK10dZDAxZXOQSHC6yNLD3OY6zVsw7K4xJaWFldQ49UelxxVWnlPEhBr3GszT6uc7jJ4fazf4KFx5p0HFH+Kme9CLle4h6bZFkfxhNouAIoJVqfHQSKbSkDFnVpMhEpovC481NNVcr3SaWlZzTovJErCqgydaMIYBRk+tKfFLC9Wmk75iyqg1DJBWfRxT7pONvTAZom2YC23QsMpOg0B0l0NDh2YjnzjpyvxLrYOK1o3ckLZ5WujSBHr8YL2gxnw85lxEop9c9TynkbMD/kqy+svv/Jb9wu5jh7s+jQbpGzI+ZLu0byEuHZ+wvt6Ays9TJIYl8A5+i0DHHGjvYQ1JLGPuOlaR/TpRFqvXCzHR2BO5iKg0Zmm/ic0W2ZXrB+Gve2uEt1dJKs/QXbwePE)

Usage before 3.5

In versions before 3.5 where `useTemplateRef()` was not introduced, we need to declare a ref with a name that matches the template ref attribute's value. The ref should also contain an array value:

vue

```
<script setup>
import { ref, onMounted } from 'vue'

const list = ref([
  /* ... */
])

const itemRefs = ref([])

onMounted(() => console.log(itemRefs.value))
</script>

<template>
  <ul>
    <li v-for="item in list" ref="itemRefs">
      {{ item }}
    </li>
  </ul>
</template>
```

When `ref` is used inside `v-for`, the resulting ref value will be an array containing the corresponding elements:

vue

```
<script>
export default {
  data() {
    return {
      list: [
        /* ... */
      ]
    }
  },
  mounted() {
    console.log(this.$refs.items)
  }
}
</script>

<template>
  <ul>
    <li v-for="item in list" ref="items">
      {{ item }}
    </li>
  </ul>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNpFjk0KwjAQha/yCC4Uaou6kyp4DuOi2KkGYhKSiQildzdNa4WQmTc/37xeXJwr35HEUdTh7pXjszT0cdYzWuqaqBm9NEDbcLPeTDngiaM3PwVoFfiI667AvsDhNpWHMQzF+L9sNEztH3C3JlhNpbaPNT9VKFeeulAqplfY5D1p0qurxVQSqel0w5QUUEedY8q0wnvbWX+SYgRAmWxIiuSzm4tBinkc6HvkuSE7TIBKq4lZZWhdLZfE8AWp4l3T)

It should be noted that the ref array does **not** guarantee the same order as the source array.

## Function Refs​

Instead of a string key, the `ref` attribute can also be bound to a function, which will be called on each component update and gives you full flexibility on where to store the element reference. The function receives the element reference as the first argument:

template

```
<input :ref="(el) => { /* assign el to a property or ref */ }">
```

Note we are using a dynamic `:ref` binding so we can pass it a function instead of a ref name string. When the element is unmounted, the argument will be `null`. You can, of course, use a method instead of an inline function.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/template-refs.md)

---

# Template Syntax​

> Vue.js - The Progressive JavaScript Framework

# Template Syntax​

[Watch an interactive video lesson on Scrimba](https://scrimba.com/links/vue-template-syntax)

Vue uses an HTML-based template syntax that allows you to declaratively bind the rendered DOM to the underlying component instance's data. All Vue templates are syntactically valid HTML that can be parsed by spec-compliant browsers and HTML parsers.

Under the hood, Vue compiles the templates into highly-optimized JavaScript code. Combined with the reactivity system, Vue can intelligently figure out the minimal number of components to re-render and apply the minimal amount of DOM manipulations when the app state changes.

If you are familiar with Virtual DOM concepts and prefer the raw power of JavaScript, you can also [directly write render functions](https://vuejs.org/guide/extras/render-function) instead of templates, with optional JSX support. However, do note that they do not enjoy the same level of compile-time optimizations as templates.

## Text Interpolation​

The most basic form of data binding is text interpolation using the "Mustache" syntax (double curly braces):

template

```
<span>Message: {{ msg }}</span>
```

The mustache tag will be replaced with the value of the `msg` property [from the corresponding component instance](https://vuejs.org/guide/essentials/reactivity-fundamentals#declaring-reactive-state). It will also be updated whenever the `msg` property changes.

## Raw HTML​

The double mustaches interpret the data as plain text, not HTML. In order to output real HTML, you will need to use the [v-htmldirective](https://vuejs.org/api/built-in-directives#v-html):

template

```
<p>Using text interpolation: {{ rawHtml }}</p>
<p>Using v-html directive: <span v-html="rawHtml"></span></p>
```

Using text interpolation: <span style="color: red">This should be red.</span>

Using v-html directive: This should be red.

Here we're encountering something new. The `v-html` attribute you're seeing is called a **directive**. Directives are prefixed with `v-` to indicate that they are special attributes provided by Vue, and as you may have guessed, they apply special reactive behavior to the rendered DOM. Here, we're basically saying "keep this element's inner HTML up-to-date with the `rawHtml` property on the current active instance."

The contents of the `span` will be replaced with the value of the `rawHtml` property, interpreted as plain HTML - data bindings are ignored. Note that you cannot use `v-html` to compose template partials, because Vue is not a string-based templating engine. Instead, components are preferred as the fundamental unit for UI reuse and composition.

Security Warning

Dynamically rendering arbitrary HTML on your website can be very dangerous because it can easily lead to [XSS vulnerabilities](https://en.wikipedia.org/wiki/Cross-site_scripting). Only use `v-html` on trusted content and **never** on user-provided content.

## Attribute Bindings​

Mustaches cannot be used inside HTML attributes. Instead, use a [v-binddirective](https://vuejs.org/api/built-in-directives#v-bind):

template

```
<div v-bind:id="dynamicId"></div>
```

The `v-bind` directive instructs Vue to keep the element's `id` attribute in sync with the component's `dynamicId` property. If the bound value is `null` or `undefined`, then the attribute will be removed from the rendered element.

### Shorthand​

Because `v-bind` is so commonly used, it has a dedicated shorthand syntax:

template

```
<div :id="dynamicId"></div>
```

Attributes that start with `:` may look a bit different from normal HTML, but it is in fact a valid character for attribute names and all Vue-supported browsers can parse it correctly. In addition, they do not appear in the final rendered markup. The shorthand syntax is optional, but you will likely appreciate it when you learn more about its usage later.

> For the rest of the guide, we will be using the shorthand syntax in code examples, as that's the most common usage for Vue developers.

### Same-name Shorthand​

- Only supported in 3.4+

If the attribute has the same name as the variable name of the JavaScript value being bound, the syntax can be further shortened to omit the attribute value:

template

```

<div :id></div>

<div v-bind:id></div>
```

This is similar to the property shorthand syntax when declaring objects in JavaScript. Note this is a feature that is only available in Vue 3.4 and above.

### Boolean Attributes​

[Boolean attributes](https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#boolean-attributes) are attributes that can indicate true / false values by their presence on an element. For example, [disabled](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/disabled) is one of the most commonly used boolean attributes.

`v-bind` works a bit differently in this case:

template

```
<button :disabled="isButtonDisabled">Button</button>
```

The `disabled` attribute will be included if `isButtonDisabled` has a [truthy value](https://developer.mozilla.org/en-US/docs/Glossary/Truthy). It will also be included if the value is an empty string, maintaining consistency with `<button disabled="">`. For other [falsy values](https://developer.mozilla.org/en-US/docs/Glossary/Falsy) the attribute will be omitted.

### Dynamically Binding Multiple Attributes​

If you have a JavaScript object representing multiple attributes that looks like this:

js

```
const objectOfAttrs = {
  id: 'container',
  class: 'wrapper',
  style: 'background-color:green'
}
```

js

```
data() {
  return {
    objectOfAttrs: {
      id: 'container',
      class: 'wrapper'
    }
  }
}
```

You can bind them to a single element by using `v-bind` without an argument:

template

```
<div v-bind="objectOfAttrs"></div>
```

## Using JavaScript Expressions​

So far we've only been binding to simple property keys in our templates. But Vue actually supports the full power of JavaScript expressions inside all data bindings:

template

```
{{ number + 1 }}

{{ ok ? 'YES' : 'NO' }}

{{ message.split('').reverse().join('') }}

<div :id="`list-${id}`"></div>
```

These expressions will be evaluated as JavaScript in the data scope of the current component instance.

In Vue templates, JavaScript expressions can be used in the following positions:

- Inside text interpolations (mustaches)
- In the attribute value of any Vue directives (special attributes that start with `v-`)

### Expressions Only​

Each binding can only contain **one single expression**. An expression is a piece of code that can be evaluated to a value. A simple check is whether it can be used after `return`.

Therefore, the following will **NOT** work:

template

```

{{ var a = 1 }}

{{ if (ok) { return message } }}
```

### Calling Functions​

It is possible to call a component-exposed method inside a binding expression:

template

```
<time :title="toTitleDate(date)" :datetime="date">
  {{ formatDate(date) }}
</time>
```

TIP

Functions called inside binding expressions will be called every time the component updates, so they should **not** have any side effects, such as changing data or triggering asynchronous operations.

### Restricted Globals Access​

Template expressions are sandboxed and only have access to a [restricted list of globals](https://github.com/vuejs/core/blob/main/packages/shared/src/globalsAllowList.ts#L3). The list exposes commonly used built-in globals such as `Math` and `Date`.

Globals not explicitly included in the list, for example user-attached properties on `window`, will not be accessible in template expressions. You can, however, explicitly define additional globals for all Vue expressions by adding them to [app.config.globalProperties](https://vuejs.org/api/application#app-config-globalproperties).

## Directives​

Directives are special attributes with the `v-` prefix. Vue provides a number of [built-in directives](https://vuejs.org/api/built-in-directives), including `v-html` and `v-bind` which we have introduced above.

Directive attribute values are expected to be single JavaScript expressions (with the exception of `v-for`, `v-on` and `v-slot`, which will be discussed in their respective sections later). A directive's job is to reactively apply updates to the DOM when the value of its expression changes. Take [v-if](https://vuejs.org/api/built-in-directives#v-if) as an example:

template

```
<p v-if="seen">Now you see me</p>
```

Here, the `v-if` directive would remove or insert the `<p>` element based on the truthiness of the value of the expression `seen`.

### Arguments​

Some directives can take an "argument", denoted by a colon after the directive name. For example, the `v-bind` directive is used to reactively update an HTML attribute:

template

```
<a v-bind:href="url"> ... </a>

<a :href="url"> ... </a>
```

Here, `href` is the argument, which tells the `v-bind` directive to bind the element's `href` attribute to the value of the expression `url`. In the shorthand, everything before the argument (i.e., `v-bind:`) is condensed into a single character, `:`.

Another example is the `v-on` directive, which listens to DOM events:

template

```
<a v-on:click="doSomething"> ... </a>

<a @click="doSomething"> ... </a>
```

Here, the argument is the event name to listen to: `click`. `v-on` has a corresponding shorthand, namely the `@` character. We will talk about event handling in more detail too.

### Dynamic Arguments​

It is also possible to use a JavaScript expression in a directive argument by wrapping it with square brackets:

template

```

<a v-bind:[attributeName]="url"> ... </a>

<a :[attributeName]="url"> ... </a>
```

Here, `attributeName` will be dynamically evaluated as a JavaScript expression, and its evaluated value will be used as the final value for the argument. For example, if your component instance has a data property, `attributeName`, whose value is `"href"`, then this binding will be equivalent to `v-bind:href`.

Similarly, you can use dynamic arguments to bind a handler to a dynamic event name:

template

```
<a v-on:[eventName]="doSomething"> ... </a>

<a @[eventName]="doSomething"> ... </a>
```

In this example, when `eventName`'s value is `"focus"`, `v-on:[eventName]` will be equivalent to `v-on:focus`.

#### Dynamic Argument Value Constraints​

Dynamic arguments are expected to evaluate to a string, with the exception of `null`. The special value `null` can be used to explicitly remove the binding. Any other non-string value will trigger a warning.

#### Dynamic Argument Syntax Constraints​

Dynamic argument expressions have some syntax constraints because certain characters, such as spaces and quotes, are invalid inside HTML attribute names. For example, the following is invalid:

template

```

<a :['foo' + bar]="value"> ... </a>
```

If you need to pass a complex dynamic argument, it's probably better to use a [computed property](https://vuejs.org/guide/essentials/computed), which we will cover shortly.

When using in-DOM templates (templates directly written in an HTML file), you should also avoid naming keys with uppercase characters, as browsers will coerce attribute names into lowercase:

template

```
<a :[someAttr]="value"> ... </a>
```

The above will be converted to `:[someattr]` in in-DOM templates. If your component has a `someAttr` property instead of `someattr`, your code won't work. Templates inside Single-File Components are **not** subject to this constraint.

### Modifiers​

Modifiers are special postfixes denoted by a dot, which indicate that a directive should be bound in some special way. For example, the `.prevent` modifier tells the `v-on` directive to call `event.preventDefault()` on the triggered event:

template

```
<form @submit.prevent="onSubmit">...</form>
```

You'll see other examples of modifiers later, [forv-on](https://vuejs.org/guide/essentials/event-handling#event-modifiers) and [forv-model](https://vuejs.org/guide/essentials/forms#modifiers), when we explore those features.

And finally, here's the full directive syntax visualized:

![directive syntax graph](https://vuejs.org/assets/directive.DtZKvoAo.png)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/template-syntax.md)
