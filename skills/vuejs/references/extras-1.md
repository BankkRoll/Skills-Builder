# Animation Techniques​ and more

# Animation Techniques​

> Vue.js - The Progressive JavaScript Framework

# Animation Techniques​

Vue provides the [<Transition>](https://vuejs.org/guide/built-ins/transition) and [<TransitionGroup>](https://vuejs.org/guide/built-ins/transition-group) components for handling enter / leave and list transitions. However, there are many other ways of using animations on the web, even in a Vue application. Here we will discuss a few additional techniques.

## Class-based Animations​

For elements that are not entering / leaving the DOM, we can trigger animations by dynamically adding a CSS class:

js

```
const disabled = ref(false)

function warnDisabled() {
  disabled.value = true
  setTimeout(() => {
    disabled.value = false
  }, 1500)
}
```

js

```
export default {
  data() {
    return {
      disabled: false
    }
  },
  methods: {
    warnDisabled() {
      this.disabled = true
      setTimeout(() => {
        this.disabled = false
      }, 1500)
    }
  }
}
```

template

```
<div :class="{ shake: disabled }">
  <button @click="warnDisabled">Click me</button>
  <span v-if="disabled">This feature is disabled!</span>
</div>
```

css

```
.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
```

## State-driven Animations​

Some transition effects can be applied by interpolating values, for instance by binding a style to an element while an interaction occurs. Take this example for instance:

js

```
const x = ref(0)

function onMousemove(e) {
  x.value = e.clientX
}
```

js

```
export default {
  data() {
    return {
      x: 0
    }
  },
  methods: {
    onMousemove(e) {
      this.x = e.clientX
    }
  }
}
```

template

```
<div
  @mousemove="onMousemove"
  :style="{ backgroundColor: `hsl(${x}, 80%, 50%)` }"
  class="movearea"
>
  <p>Move your mouse across this div...</p>
  <p>x: {{ x }}</p>
</div>
```

css

```
.movearea {
  transition: 0.3s background-color ease;
}
```

Move your mouse across this div...

x: 0

In addition to color, you can also use style bindings to animate transform, width, or height. You can even animate SVG paths using spring physics - after all, they are all attribute data bindings:

Drag Me[Source code](https://play.vuejs.org/#eNqlVmtv2zYU/SsXboE6mC3bSdwVmpM9MAz9sAIdsA8b5gGhRUrWKpEESTl2DP/3HZKSbbkuUKBA4Ij3ce65D15pP/hZ62TTiEE6WNjMlNqRFa7Rj0tZ1loZR3sygmWu3IgRZarWjROcDpQbVdMbeL45WvKdZHWZ2VbXHZP/LGyWMlPSOloLxoV5L8pi7eiBZrdTr6uEo9L+alhRlLKAPGeVFZ2PdQzwD6CyTWk6oh1+6dBpM2g6isNgch4jWPeCHm4u2Xxkbg2QLrvh8IYeHmm/lARg1xhJTx+moyn9fnfr//nf1/tzzMMfr/dZsj1AnCW7Azhe6J+W8jwsfp2Q7qOypSuV/ELsaMt3Xp3saNxL48yA1Vp4DFg+ojA/0i2ldH/GPqAROcOkzZWpU3oKzxVzYui5wnPS4hz09gZsydc3Us4bidqCZWiD79FQ3ERMgagiydZMFoL/qZpsLSziX4r+mf4LRmgn9ZvsTBOEATjZBjDNCvHXSeiTj8K/wadHR8lv5ZLT8MSnhUFVA5PeyHxHw5YZutCyRW2C9alJLc+jya5n8VmXZsm865MP6hEugp61pevIRUOUDjVouX8hoWsXy8uPF5ThBvtRiGKQGXVPX3OdzozdTov0hGu1QdAR8cYwTzil76e4vrkpA/+Ubt+Fe+ydQzljhotJ3ETYQTg4UWs/qDgRLXi5aQtWMWsflgPuU2OrSiwHUfFTrRoruHqW0B5H9qh1fgyC+Ko6ONdqI6CNA9b3vK4KXo0OiLElfS8h+TVdcKsEC5B9bcgW+dpNcUx1BR09l9ytccASwmkdeoDj/C2OrRPctN9oqQ962nAwz8uqguzV3W/z2S9zOCwm3rILNkG07hmFPgaOGDD3/OiDWEygvWbY7jVESq3bVT6ti1UHkPeiqtQJontaTM46jWMAIJspLTgkybHRcaxXLPtUGNVIPs5UpUxKr/I8/yGo1HZs1wwj4N8T93pLs7f4McWKYdv5F4j/S2bzm2AeKpr6ra63QRCLium87yRouskrj7cuORcyCGtmcKfgCCtijVNBqttEUyxfJIN3UhA7sXVjVpUFFBnqIUwQ56jO2JYvuDUzED3JnlsOd9NpEGJQzNgPSwahVDKirpRBY8aG8bKxKb0LCLhByaqIVTqxYSurKrxhIhulUZrwWIkciPH5ZVxKLvw7toWJjccFT9o2XqL2cjy6z2IlGOe4/rFAp8aUL0HYUoeoF6t78/U72nUEXwvnRYqFuxX153VbqYpHYEy1nySM0GA0iF8q45ppfJUoia+eEG/ZKuxykHZbE6vl9AHj5bgHzmmbTiYZl4n9tNMYwYSLzaRn2O2xweF/7cIdbA==)

## Animating with Watchers​

With some creativity, we can use watchers to animate anything based on some numerical state. For example, we can animate the number itself:

js

```
import { ref, reactive, watch } from 'vue'
import gsap from 'gsap'

const number = ref(0)
const tweened = reactive({
  number: 0
})

// Note: For inputs greater than Number.MAX_SAFE_INTEGER (9007199254740991),
// the result may be inaccurate due to limitations in JavaScript number precision.
watch(number, (n) => {
  gsap.to(tweened, { duration: 0.5, number: Number(n) || 0 })
})
```

template

```
Type a number: <input v-model.number="number" />
<p>{{ tweened.number.toFixed(0) }}</p>
```

js

```
import gsap from 'gsap'

export default {
  data() {
    return {
      number: 0,
      tweened: 0
    }
  },
  // Note: For inputs greater than Number.MAX_SAFE_INTEGER (9007199254740991),
  // the result may be inaccurate due to limitations in JavaScript number precision.
  watch: {
    number(n) {
      gsap.to(this, { duration: 0.5, tweened: Number(n) || 0 })
    }
  }
}
```

template

```
Type a number: <input v-model.number="number" />
<p>{{ tweened.toFixed(0) }}</p>
```

 Type a number:

0

[Try it in the Playground](https://play.vuejs.org/#eNpNUstygzAM/BWNLyEzBDKd6YWSdHrpsacefSGgJG7xY7BImhL+vTKv9ILllXYlr+jEm3PJpUWRidyXjXIEHql1e2mUdrYh6KDBY8yfoiR1wRiuBZVn6OHYWA0r5q6W2pMv3ISHkBPSlNZ4AtPqAzawC2LRdj3DdEU0WA34qB910sBUnsFWmp6LpRmaRo9UHMLIrGG3h4EBQ/OEbDRpxjx51TYFKWtYKHmOF9WP4Qzs+x22EDoA9NLwmaejC/x+vhBqVxeEfAPIK3WBsi6830lRobZSDDjA580hFIt8roxrCS4bbSuskxFmzhhIAenEy92id1CnzZzfd91szETmZ72rH6zYOej7PA3rYXrKE3GUp//m5KunWx3C5CE6enS0hjZXVKczZXCwdfWyoF79YgZPqBliJ9iGSUTEYlzuRrO9X94a/lUGNTklvBTZvAMpwhYCIMWZyPksTVvjvk9JaXUacq9sSlujFJPnvej/AElH3FQ=)

[Try it in the Playground](https://play.vuejs.org/#eNpNUctugzAQ/JWVLyESj6hSL5Sm6qXHnnr0xYENuAXbwus8Svj3GlxIJEvendHMvgb2bkx6cshyVtiyl4b2XMnO6J6gtsLAsdcdbKZwwxVXeJmpCo/CtQQDVwCVIBFtQwzQI7leLRmAct0B+xx28YLQGVFh5aGAjNM3zvRZUNnkizhII7V6w9xTSjqiRtoYBqhcL0hq5c3S5/hu/blKbzfYwbh9LMWVf0W2zusTws60gnDK6OtqEMTaeSGVcQSnpNMVtmmAXzkLAWeQzarCQNkKaz1zkHWysPthWNryjX/IC1bRbgvjWGTG64rssbQqLF3bKUzvHmH6o1aUnFHWDeVw0G31sqJW/mIOT9h5KEw2m7CYhUsmnV/at9XKX3n24v+E5WxdNmfTbieAs4bI2DzLnDI/dVrqLpu4Nz+/a5GzZYls/AM3dcFx)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/extras/animation.md)

---

# Composition API FAQ​

> Vue.js - The Progressive JavaScript Framework

# Composition API FAQ​

TIP

This FAQ assumes prior experience with Vue - in particular, experience with Vue 2 while primarily using Options API.

## What is Composition API?​

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/introduction-to-the-vue-js-3-composition-api?friend=vuejs)

Composition API is a set of APIs that allows us to author Vue components using imported functions instead of declaring options. It is an umbrella term that covers the following APIs:

- [Reactivity API](https://vuejs.org/api/reactivity-core), e.g. `ref()` and `reactive()`, that allows us to directly create reactive state, computed state, and watchers.
- [Lifecycle Hooks](https://vuejs.org/api/composition-api-lifecycle), e.g. `onMounted()` and `onUnmounted()`, that allow us to programmatically hook into the component lifecycle.
- [Dependency Injection](https://vuejs.org/api/composition-api-dependency-injection), i.e. `provide()` and `inject()`, that allow us to leverage Vue's dependency injection system while using Reactivity APIs.

Composition API is a built-in feature of Vue 3 and [Vue 2.7](https://blog.vuejs.org/posts/vue-2-7-naruto.html). For older Vue 2 versions, use the officially maintained [@vue/composition-api](https://github.com/vuejs/composition-api) plugin. In Vue 3, it is also primarily used together with the [<script setup>](https://vuejs.org/api/sfc-script-setup) syntax in Single-File Components. Here's a basic example of a component using Composition API:

vue

```
<script setup>
import { ref, onMounted } from 'vue'

// reactive state
const count = ref(0)

// functions that mutate state and trigger updates
function increment() {
  count.value++
}

// lifecycle hooks
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

Despite an API style based on function composition, **Composition API is NOT functional programming**. Composition API is based on Vue's mutable, fine-grained reactivity paradigm, whereas functional programming emphasizes immutability.

If you are interested in learning how to use Vue with Composition API, you can set the site-wide API preference to Composition API using the toggle at the top of the left sidebar, and then go through the guide from the beginning.

## Why Composition API?​

### Better Logic Reuse​

The primary advantage of Composition API is that it enables clean, efficient logic reuse in the form of [Composable functions](https://vuejs.org/guide/reusability/composables). It solves [all the drawbacks of mixins](https://vuejs.org/guide/reusability/composables#vs-mixins), the primary logic reuse mechanism for Options API.

Composition API's logic reuse capability has given rise to impressive community projects such as [VueUse](https://vueuse.org/), an ever-growing collection of composable utilities. It also serves as a clean mechanism for easily integrating stateful third-party services or libraries into Vue's reactivity system, for example [immutable data](https://vuejs.org/guide/extras/reactivity-in-depth#immutable-data), [state machines](https://vuejs.org/guide/extras/reactivity-in-depth#state-machines), and [RxJS](https://vuejs.org/guide/extras/reactivity-in-depth#rxjs).

### More Flexible Code Organization​

Many users love that we write organized code by default with Options API: everything has its place based on the option it falls under. However, Options API poses serious limitations when a single component's logic grows beyond a certain complexity threshold. This limitation is particularly prominent in components that need to deal with multiple **logical concerns**, which we have witnessed first hand in many production Vue 2 apps.

Take the folder explorer component from Vue CLI's GUI as an example: this component is responsible for the following logical concerns:

- Tracking current folder state and displaying its content
- Handling folder navigation (opening, closing, refreshing...)
- Handling new folder creation
- Toggling show favorite folders only
- Toggling show hidden folders
- Handling current working directory changes

The [original version](https://github.com/vuejs/vue-cli/blob/a09407dd5b9f18ace7501ddb603b95e31d6d93c0/packages/@vue/cli-ui/src/components/folder/FolderExplorer.vue#L198-L404) of the component was written in Options API. If we give each line of code a color based on the logical concern it is dealing with, this is how it looks:

![folder component before](https://vuejs.org/assets/options-api.B_7BnLkD.png)

Notice how code dealing with the same logical concern is forced to be split under different options, located in different parts of the file. In a component that is several hundred lines long, understanding and navigating a single logical concern requires constantly scrolling up and down the file, making it much more difficult than it should be. In addition, if we ever intend to extract a logical concern into a reusable utility, it takes quite a bit of work to find and extract the right pieces of code from different parts of the file.

Here's the same component, before and after the [refactor into Composition API](https://gist.github.com/yyx990803/8854f8f6a97631576c14b63c8acd8f2e):

![folder component after](https://vuejs.org/assets/composition-api-after.ZXskY_32.png)

Notice how the code related to the same logical concern can now be grouped together: we no longer need to jump between different options blocks while working on a specific logical concern. Moreover, we can now move a group of code into an external file with minimal effort, since we no longer need to shuffle the code around in order to extract them. This reduced friction for refactoring is key to the long-term maintainability in large codebases.

### Better Type Inference​

In recent years, more and more frontend developers are adopting [TypeScript](https://www.typescriptlang.org/) as it helps us write more robust code, make changes with more confidence, and provides a great development experience with IDE support. However, the Options API, originally conceived in 2013, was designed without type inference in mind. We had to implement some [absurdly complex type gymnastics](https://github.com/vuejs/core/blob/44b95276f5c086e1d88fa3c686a5f39eb5bb7821/packages/runtime-core/src/componentPublicInstance.ts#L132-L165) to make type inference work with the Options API. Even with all this effort, type inference for Options API can still break down for mixins and dependency injection.

This had led many developers who wanted to use Vue with TS to lean towards Class API powered by `vue-class-component`. However, a class-based API heavily relies on ES decorators, a language feature that was only a stage 2 proposal when Vue 3 was being developed in 2019. We felt it was too risky to base an official API on an unstable proposal. Since then, the decorators proposal has gone through yet another complete overhaul, and finally reached stage 3 in 2022. In addition, class-based API suffers from logic reuse and organization limitations similar to Options API.

In comparison, Composition API utilizes mostly plain variables and functions, which are naturally type friendly. Code written in Composition API can enjoy full type inference with little need for manual type hints. Most of the time, Composition API code will look largely identical in TypeScript and plain JavaScript. This also makes it possible for plain JavaScript users to benefit from partial type inference.

### Smaller Production Bundle and Less Overhead​

Code written in Composition API and `<script setup>` is also more efficient and minification-friendly than Options API equivalent. This is because the template in a `<script setup>` component is compiled as a function inlined in the same scope of the `<script setup>` code. Unlike property access from `this`, the compiled template code can directly access variables declared inside `<script setup>`, without an instance proxy in between. This also leads to better minification because all the variable names can be safely shortened.

## Relationship with Options API​

### Trade-offs​

Some users moving from Options API found their Composition API code less organized, and concluded that Composition API is "worse" in terms of code organization. We recommend users with such opinions to look at that problem from a different perspective.

It is true that Composition API no longer provides the "guard rails" that guide you to put your code into respective buckets. In return, you get to author component code like how you would write normal JavaScript. This means **you can and should apply any code organization best practices to your Composition API code as you would when writing normal JavaScript**. If you can write well-organized JavaScript, you should also be able to write well-organized Composition API code.

Options API does allow you to "think less" when writing component code, which is why many users love it. However, in reducing the mental overhead, it also locks you into the prescribed code organization pattern with no escape hatch, which can make it difficult to refactor or improve code quality in larger scale projects. In this regard, Composition API provides better long term scalability.

### Does Composition API cover all use cases?​

Yes in terms of stateful logic. When using Composition API, there are only a few options that may still be needed: `props`, `emits`, `name`, and `inheritAttrs`.

TIP

Since 3.3 you can directly use `defineOptions` in `<script setup>` to set the component name or `inheritAttrs` property

If you intend to exclusively use Composition API (along with the options listed above), you can shave a few kbs off your production bundle via a [compile-time flag](https://vuejs.org/api/compile-time-flags) that drops Options API related code from Vue. Note this also affects Vue components in your dependencies.

### Can I use both APIs in the same component?​

Yes. You can use Composition API via the [setup()](https://vuejs.org/api/composition-api-setup) option in an Options API component.

However, we only recommend doing so if you have an existing Options API codebase that needs to integrate with new features / external libraries written with Composition API.

### Will Options API be deprecated?​

No, we do not have any plan to do so. Options API is an integral part of Vue and the reason many developers love it. We also realize that many of the benefits of Composition API only manifest in larger-scale projects, and Options API remains a solid choice for many low-to-medium-complexity scenarios.

## Relationship with Class API​

We no longer recommend using Class API with Vue 3, given that Composition API provides great TypeScript integration with additional logic reuse and code organization benefits.

## Comparison with React Hooks​

Composition API provides the same level of logic composition capabilities as React Hooks, but with some important differences.

React Hooks are invoked repeatedly every time a component updates. This creates a number of caveats that can confuse even seasoned React developers. It also leads to performance optimization issues that can severely affect development experience. Here are some examples:

- Hooks are call-order sensitive and cannot be conditional.
- Variables declared in a React component can be captured by a hook closure and become "stale" if the developer fails to pass in the correct dependencies array. This leads to React developers relying on ESLint rules to ensure correct dependencies are passed. However, the rule is often not smart enough and over-compensates for correctness, which leads to unnecessary invalidation and headaches when edge cases are encountered.
- Expensive computations require the use of `useMemo`, which again requires manually passing in the correct dependencies array.
- Event handlers passed to child components cause unnecessary child updates by default, and require explicit `useCallback` as an optimization. This is almost always needed, and again requires a correct dependencies array. Neglecting this leads to over-rendering apps by default and can cause performance issues without realizing it.
- The stale closure problem, combined with Concurrent features, makes it difficult to reason about when a piece of hooks code is run, and makes working with mutable state that should persist across renders (via `useRef`) cumbersome.

> Note: some of the above issues that are related to memoization can be resolved by the upcoming [React Compiler](https://react.dev/learn/react-compiler).

In comparison, Vue Composition API:

- Invokes `setup()` or `<script setup>` code only once. This makes the code align better with the intuitions of idiomatic JavaScript usage as there are no stale closures to worry about. Composition API calls are also not sensitive to call order and can be conditional.
- Vue's runtime reactivity system automatically collects reactive dependencies used in computed properties and watchers, so there's no need to manually declare dependencies.
- No need to manually cache callback functions to avoid unnecessary child updates. In general, Vue's fine-grained reactivity system ensures child components only update when they need to. Manual child-update optimizations are rarely a concern for Vue developers.

We acknowledge the creativity of React Hooks, and it is a major source of inspiration for Composition API. However, the issues mentioned above do exist in its design and we noticed Vue's reactivity model happens to provide a way around them.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/extras/composition-api-faq.md)

---

# Reactivity in Depth​

> Vue.js - The Progressive JavaScript Framework

# Reactivity in Depth​

One of Vue’s most distinctive features is the unobtrusive reactivity system. Component state consists of reactive JavaScript objects. When you modify them, the view updates. It makes state management simple and intuitive, but it’s also important to understand how it works to avoid some common gotchas. In this section, we are going to dig into some of the lower-level details of Vue’s reactivity system.

## What is Reactivity?​

This term comes up in programming quite a bit these days, but what do people mean when they say it? Reactivity is a programming paradigm that allows us to adjust to changes in a declarative manner. The canonical example that people usually show, because it’s a great one, is an Excel spreadsheet:

|  | A | B | C |
| --- | --- | --- | --- |
| 0 | 1 |  |  |
| 1 | 2 |  |  |
| 2 | 3 |  |  |

Here cell A2 is defined via a formula of `= A0 + A1` (you can click on A2 to view or edit the formula), so the spreadsheet gives us 3. No surprises there. But if you update A0 or A1, you'll notice that A2 automagically updates too.

JavaScript doesn’t usually work like this. If we were to write something comparable in JavaScript:

js

```
let A0 = 1
let A1 = 2
let A2 = A0 + A1

console.log(A2) // 3

A0 = 2
console.log(A2) // Still 3
```

When we mutate `A0`, `A2` does not change automatically.

So how would we do this in JavaScript? First, in order to re-run the code that updates `A2`, let's wrap it in a function:

js

```
let A2

function update() {
  A2 = A0 + A1
}
```

Then, we need to define a few terms:

- The `update()` function produces a **side effect**, or **effect** for short, because it modifies the state of the program.
- `A0` and `A1` are considered **dependencies** of the effect, as their values are used to perform the effect. The effect is said to be a **subscriber** to its dependencies.

What we need is a magic function that can invoke `update()` (the **effect**) whenever `A0` or `A1` (the **dependencies**) change:

js

```
whenDepsChange(update)
```

This `whenDepsChange()` function has the following tasks:

1. Track when a variable is read. E.g. when evaluating the expression `A0 + A1`, both `A0` and `A1` are read.
2. If a variable is read when there is a currently running effect, make that effect a subscriber to that variable. E.g. because `A0` and `A1` are read when `update()` is being executed, `update()` becomes a subscriber to both `A0` and `A1` after the first call.
3. Detect when a variable is mutated. E.g. when `A0` is assigned a new value, notify all its subscriber effects to re-run.

## How Reactivity Works in Vue​

We can't really track the reading and writing of local variables like in the example. There's just no mechanism for doing that in vanilla JavaScript. What we **can** do though, is intercept the reading and writing of **object properties**.

There are two ways of intercepting property access in JavaScript: [getter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get#description) / [setters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/set#description) and [Proxies](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy). Vue 2 used getter / setters exclusively due to browser support limitations. In Vue 3, Proxies are used for reactive objects and getter / setters are used for refs. Here's some pseudo-code that illustrates how they work:

js

```
function reactive(obj) {
  return new Proxy(obj, {
    get(target, key) {
      track(target, key)
      return target[key]
    },
    set(target, key, value) {
      target[key] = value
      trigger(target, key)
    }
  })
}

function ref(value) {
  const refObject = {
    get value() {
      track(refObject, 'value')
      return value
    },
    set value(newValue) {
      value = newValue
      trigger(refObject, 'value')
    }
  }
  return refObject
}
```

TIP

Code snippets here and below are meant to explain the core concepts in the simplest form possible, so many details are omitted, and edge cases ignored.

This explains a few [limitations of reactive objects](https://vuejs.org/guide/essentials/reactivity-fundamentals#limitations-of-reactive) that we have discussed in the fundamentals section:

- When you assign or destructure a reactive object's property to a local variable, accessing or assigning to that variable is non-reactive because it no longer triggers the get / set proxy traps on the source object. Note this "disconnect" only affects the variable binding - if the variable points to a non-primitive value such as an object, mutating the object would still be reactive.
- The returned proxy from `reactive()`, although behaving just like the original, has a different identity if we compare it to the original using the `===` operator.

Inside `track()`, we check whether there is a currently running effect. If there is one, we lookup the subscriber effects (stored in a Set) for the property being tracked, and add the effect to the Set:

js

```
// This will be set right before an effect is about
// to be run. We'll deal with this later.
let activeEffect

function track(target, key) {
  if (activeEffect) {
    const effects = getSubscribersForProperty(target, key)
    effects.add(activeEffect)
  }
}
```

Effect subscriptions are stored in a global `WeakMap<target, Map<key, Set<effect>>>` data structure. If no subscribing effects Set was found for a property (tracked for the first time), it will be created. This is what the `getSubscribersForProperty()` function does, in short. For simplicity, we will skip its details.

Inside `trigger()`, we again lookup the subscriber effects for the property. But this time we invoke them instead:

js

```
function trigger(target, key) {
  const effects = getSubscribersForProperty(target, key)
  effects.forEach((effect) => effect())
}
```

Now let's circle back to the `whenDepsChange()` function:

js

```
function whenDepsChange(update) {
  const effect = () => {
    activeEffect = effect
    update()
    activeEffect = null
  }
  effect()
}
```

It wraps the raw `update` function in an effect that sets itself as the current active effect before running the actual update. This enables `track()` calls during the update to locate the current active effect.

At this point, we have created an effect that automatically tracks its dependencies, and re-runs whenever a dependency changes. We call this a **Reactive Effect**.

Vue provides an API that allows you to create reactive effects: [watchEffect()](https://vuejs.org/api/reactivity-core#watcheffect). In fact, you may have noticed that it works pretty similarly to the magical `whenDepsChange()` in the example. We can now rework the original example using actual Vue APIs:

js

```
import { ref, watchEffect } from 'vue'

const A0 = ref(0)
const A1 = ref(1)
const A2 = ref()

watchEffect(() => {
  // tracks A0 and A1
  A2.value = A0.value + A1.value
})

// triggers the effect
A0.value = 2
```

Using a reactive effect to mutate a ref isn't the most interesting use case - in fact, using a computed property makes it more declarative:

js

```
import { ref, computed } from 'vue'

const A0 = ref(0)
const A1 = ref(1)
const A2 = computed(() => A0.value + A1.value)

A0.value = 2
```

Internally, `computed` manages its invalidation and re-computation using a reactive effect.

So what's an example of a common and useful reactive effect? Well, updating the DOM! We can implement simple "reactive rendering" like this:

js

```
import { ref, watchEffect } from 'vue'

const count = ref(0)

watchEffect(() => {
  document.body.innerHTML = `Count is: ${count.value}`
})

// updates the DOM
count.value++
```

In fact, this is pretty close to how a Vue component keeps the state and the DOM in sync - each component instance creates a reactive effect to render and update the DOM. Of course, Vue components use much more efficient ways to update the DOM than `innerHTML`. This is discussed in [Rendering Mechanism](https://vuejs.org/guide/extras/rendering-mechanism).

The `ref()`, `computed()` and `watchEffect()` APIs are all part of the Composition API. If you have only been using Options API with Vue so far, you'll notice that Composition API is closer to how Vue's reactivity system works under the hood. In fact, in Vue 3 the Options API is implemented on top of the Composition API. All property access on the component instance (`this`) triggers getter / setters for reactivity tracking, and options like `watch` and `computed` invoke their Composition API equivalents internally.

## Runtime vs. Compile-time Reactivity​

Vue's reactivity system is primarily runtime-based: the tracking and triggering are all performed while the code is running directly in the browser. The pros of runtime reactivity are that it can work without a build step, and there are fewer edge cases. On the other hand, this makes it constrained by the syntax limitations of JavaScript, leading to the need of value containers like Vue refs.

Some frameworks, such as [Svelte](https://svelte.dev/), choose to overcome such limitations by implementing reactivity during compilation. It analyzes and transforms the code in order to simulate reactivity. The compilation step allows the framework to alter the semantics of JavaScript itself - for example, implicitly injecting code that performs dependency analysis and effect triggering around access to locally defined variables. The downside is that such transforms require a build step, and altering JavaScript semantics is essentially creating a language that looks like JavaScript but compiles into something else.

The Vue team did explore this direction via an experimental feature called [Reactivity Transform](https://vuejs.org/guide/extras/reactivity-transform), but in the end we have decided that it would not be a good fit for the project due to [the reasoning here](https://github.com/vuejs/rfcs/discussions/369#discussioncomment-5059028).

## Reactivity Debugging​

It's great that Vue's reactivity system automatically tracks dependencies, but in some cases we may want to figure out exactly what is being tracked, or what is causing a component to re-render.

### Component Debugging Hooks​

We can debug what dependencies are used during a component's render and which dependency is triggering an update using the `renderTracked``onRenderTracked` and `renderTriggered``onRenderTriggered` lifecycle hooks. Both hooks will receive a debugger event which contains information on the dependency in question. It is recommended to place a `debugger` statement in the callbacks to interactively inspect the dependency:

vue

```
<script setup>
import { onRenderTracked, onRenderTriggered } from 'vue'

onRenderTracked((event) => {
  debugger
})

onRenderTriggered((event) => {
  debugger
})
</script>
```

js

```
export default {
  renderTracked(event) {
    debugger
  },
  renderTriggered(event) {
    debugger
  }
}
```

TIP

Component debug hooks only work in development mode.

The debug event objects have the following type:

ts

```
type DebuggerEvent = {
  effect: ReactiveEffect
  target: object
  type:
    | TrackOpTypes /* 'get' | 'has' | 'iterate' */
    | TriggerOpTypes /* 'set' | 'add' | 'delete' | 'clear' */
  key: any
  newValue?: any
  oldValue?: any
  oldTarget?: Map<any, any> | Set<any>
}
```

### Computed Debugging​

We can debug computed properties by passing `computed()` a second options object with `onTrack` and `onTrigger` callbacks:

- `onTrack` will be called when a reactive property or ref is tracked as a dependency.
- `onTrigger` will be called when the watcher callback is triggered by the mutation of a dependency.

Both callbacks will receive debugger events in the [same format](#debugger-event) as component debug hooks:

js

```
const plusOne = computed(() => count.value + 1, {
  onTrack(e) {
    // triggered when count.value is tracked as a dependency
    debugger
  },
  onTrigger(e) {
    // triggered when count.value is mutated
    debugger
  }
})

// access plusOne, should trigger onTrack
console.log(plusOne.value)

// mutate count.value, should trigger onTrigger
count.value++
```

TIP

`onTrack` and `onTrigger` computed options only work in development mode.

### Watcher Debugging​

Similar to `computed()`, watchers also support the `onTrack` and `onTrigger` options:

js

```
watch(source, callback, {
  onTrack(e) {
    debugger
  },
  onTrigger(e) {
    debugger
  }
})

watchEffect(callback, {
  onTrack(e) {
    debugger
  },
  onTrigger(e) {
    debugger
  }
})
```

TIP

`onTrack` and `onTrigger` watcher options only work in development mode.

## Integration with External State Systems​

Vue's reactivity system works by deeply converting plain JavaScript objects into reactive proxies. The deep conversion can be unnecessary or sometimes unwanted when integrating with external state management systems (e.g. if an external solution also uses Proxies).

The general idea of integrating Vue's reactivity system with an external state management solution is to hold the external state in a [shallowRef](https://vuejs.org/api/reactivity-advanced#shallowref). A shallow ref is only reactive when its `.value` property is accessed - the inner value is left intact. When the external state changes, replace the ref value to trigger updates.

### Immutable Data​

If you are implementing an undo / redo feature, you likely want to take a snapshot of the application's state on every user edit. However, Vue's mutable reactivity system isn't best suited for this if the state tree is large, because serializing the entire state object on every update can be expensive in terms of both CPU and memory costs.

[Immutable data structures](https://en.wikipedia.org/wiki/Persistent_data_structure) solve this by never mutating the state objects - instead, it creates new objects that share the same, unchanged parts with old ones. There are different ways of using immutable data in JavaScript, but we recommend using [Immer](https://immerjs.github.io/immer/) with Vue because it allows you to use immutable data while keeping the more ergonomic, mutable syntax.

We can integrate Immer with Vue via a simple composable:

js

```
import { produce } from 'immer'
import { shallowRef } from 'vue'

export function useImmer(baseState) {
  const state = shallowRef(baseState)
  const update = (updater) => {
    state.value = produce(state.value, updater)
  }

  return [state, update]
}
```

[Try it in the Playground](https://play.vuejs.org/#eNp9VMFu2zAM/RXNl6ZAYnfoTlnSdRt66DBsQ7vtEuXg2YyjRpYEUU5TBPn3UZLtuE1RH2KLfCIfycfsk8/GpNsGkmkyw8IK4xiCa8wVV6I22jq2Zw3CbV2DZQe2srpmZ2km/PmMK8a4KrRCxxbCQY1j1pgyd3DrD0s27++OFh689z/0OOEkTBlPvkNuFfvbAE/Gra/UilzOko0Mh2A+ufcHwd9ij8KtWUjwMsAqlxgjcLU854qrVaMKJ7RiTleVDBRHQpWwO4/xB8xHoRg2v+oyh/MioJepT0ClvTsxhnSUi1LOsthN6iMdCGgkBacTY7NGhjd9ScG2k5W2c56M9rG6ceBPdbOWm1AxO0/a+uiZFjJHpFv7Fj10XhdSFBtyntTJkzaxf/ZtQnYguoFNJkUkmAWGs2xAm47onqT/jPWHxjjYuUkJhba57+yUSaFg4tZWN9X6Y9eIcC8ZJ1FQkzo36QNqRZILQXjroAqnXb+9LQzVD3vtnMFpljXKbKq00HWU3/X7i/QivcxKgS5aUglVXjxNAGvK8KnWZSNJWa0KDoGChzmk3L28jSVcQX1o1d1puwfgOpdSP97BqsfQxhCCK9gFTC+tXu7/coR7R71rxRWXBL2FpHOMOAAeYVGJhBvFL3s+kGKIkW5zSfKfd+RHA2u3gzZEpML9y9JS06YtAq5DLFmOMWXsjkM6rET1YjzUcSMk2J/G1/h8TKGOb8HmV7bdQbqzhmLziv0Bd3Govywg2O1x8Umvua3ARffN/Q/S1sDZDfMN5x2glo3nGGFfGlUS7QEusL0NcxWq+o03OwcKu6Ke/+fwhIb89Y3Sj3Qv0w+9xg7/AWfvyMs=)

### State Machines​

[State Machine](https://en.wikipedia.org/wiki/Finite-state_machine) is a model for describing all the possible states an application can be in, and all the possible ways it can transition from one state to another. While it may be overkill for simple components, it can help make complex state flows more robust and manageable.

One of the most popular state machine implementations in JavaScript is [XState](https://xstate.js.org/). Here's a composable that integrates with it:

js

```
import { createMachine, interpret } from 'xstate'
import { shallowRef } from 'vue'

export function useMachine(options) {
  const machine = createMachine(options)
  const state = shallowRef(machine.initialState)
  const service = interpret(machine)
    .onTransition((newState) => (state.value = newState))
    .start()
  const send = (event) => service.send(event)

  return [state, send]
}
```

[Try it in the Playground](https://play.vuejs.org/#eNp1U81unDAQfpWRL7DSFqqqUiXEJumhyqVVpDa3ugcKZtcJjC1syEqId8/YBu/uIRcEM9/P/DGz71pn0yhYwUpTD1JbMMKO+o6j7LUaLMwwGvGrqk8SBSzQDqqHJMv7EMleTMIRgGOt0Fj4a2xlxZ5EsPkHhytuOjucbApIrDoeO5HsfQCllVVHUYlVbeW0xr2OKcCzHCwkKQAK3fP56fHx5w/irSyqbfFMgA+h0cKBHZYey45jmYfeqWv6sKLXHbnTF0D5f7RWITzUnaxfD5y5ztIkSCY7zjwKYJ5DyVlf2fokTMrZ5sbZDu6Bs6e25QwK94b0svgKyjwYkEyZR2e2Z2H8n/pK04wV0oL8KEjWJwxncTicnb23C3F2slabIs9H1K/HrFZ9HrIPX7Mv37LPuTC5xEacSfa+V83YEW+bBfleFkuW8QbqQZDEuso9rcOKQQ/CxosIHnQLkWJOVdept9+ijSA6NEJwFGePaUekAdFwr65EaRcxu9BbOKq1JDqnmzIi9oL0RRDu4p1u/ayH9schrhlimGTtOLGnjeJRAJnC56FCQ3SFaYriLWjA4Q7SsPOp6kYnEXMbldKDTW/ssCFgKiaB1kusBWT+rkLYjQiAKhkHvP2j3IqWd5iMQ+M=)

### RxJS​

[RxJS](https://rxjs.dev/) is a library for working with asynchronous event streams. The [VueUse](https://vueuse.org/) library provides the [@vueuse/rxjs](https://vueuse.org/rxjs/readme.html) add-on for connecting RxJS streams with Vue's reactivity system.

## Connection to Signals​

Quite a few other frameworks have introduced reactivity primitives similar to refs from Vue's Composition API, under the term "signals":

- [Solid Signals](https://docs.solidjs.com/concepts/signals)
- [Angular Signals](https://angular.dev/guide/signals)
- [Preact Signals](https://preactjs.com/guide/v10/signals/)
- [Qwik Signals](https://qwik.builder.io/docs/components/state/#usesignal)

Fundamentally, signals are the same kind of reactivity primitive as Vue refs. It's a value container that provides dependency tracking on access, and side-effect triggering on mutation. This reactivity-primitive-based paradigm isn't a particularly new concept in the frontend world: it dates back to implementations like [Knockout observables](https://knockoutjs.com/documentation/observables.html) and [Meteor Tracker](https://docs.meteor.com/api/tracker.html) from more than a decade ago. Vue Options API and the React state management library [MobX](https://mobx.js.org/) are also based on the same principles, but hide the primitives behind object properties.

Although not a necessary trait for something to qualify as signals, today the concept is often discussed alongside the rendering model where updates are performed through fine-grained subscriptions. Due to the use of Virtual DOM, Vue currently [relies on compilers to achieve similar optimizations](https://vuejs.org/guide/extras/rendering-mechanism#compiler-informed-virtual-dom). However, we are also exploring a new Solid-inspired compilation strategy, called [Vapor Mode](https://github.com/vuejs/core-vapor), that does not rely on Virtual DOM and takes more advantage of Vue's built-in reactivity system.

### API Design Trade-Offs​

The design of Preact and Qwik's signals are very similar to Vue's [shallowRef](https://vuejs.org/api/reactivity-advanced#shallowref): all three provide a mutable interface via the `.value` property. We will focus the discussion on Solid and Angular signals.

#### Solid Signals​

Solid's `createSignal()` API design emphasizes read / write segregation. Signals are exposed as a read-only getter and a separate setter:

js

```
const [count, setCount] = createSignal(0)

count() // access the value
setCount(1) // update the value
```

Notice how the `count` signal can be passed down without the setter. This ensures that the state can never be mutated unless the setter is also explicitly exposed. Whether this safety guarantee justifies the more verbose syntax could be subject to the requirement of the project and personal taste - but in case you prefer this API style, you can easily replicate it in Vue:

js

```
import { shallowRef, triggerRef } from 'vue'

export function createSignal(value, options) {
  const r = shallowRef(value)
  const get = () => r.value
  const set = (v) => {
    r.value = typeof v === 'function' ? v(r.value) : v
    if (options?.equals === false) triggerRef(r)
  }
  return [get, set]
}
```

[Try it in the Playground](https://play.vuejs.org/#eNpdUk1TgzAQ/Ss7uQAjgr12oNXxH+ix9IAYaDQkMV/qMPx3N6G0Uy9Msu/tvn2PTORJqcI7SrakMp1myoKh1qldI9iopLYwQadpa+krG0TLYYZeyxGSojSSs/d7E8vFh0ka0YhOCmPh0EknbB4mPYfTEeqbIelD1oiqXPRQCS+WjoojAW8A1Wmzm1A39KYZzHNVYiUib85aKeCx46z7rBuySqQe6h14uINN1pDIBWACVUcqbGwtl17EqvIiR3LyzwcmcXFuTi3n8vuF9jlYzYaBajxfMsDcomv6E/m9E51luN2NV99yR3OQKkAmgykss+SkMZerxMLEZFZ4oBYJGAA600VEryAaD6CPaJwJKwnr9ldR2WMedV1Dsi6WwB58emZlsAV/zqmH9LzfvqBfruUmNvZ4QN7VearjenP4aHwmWsABt4x/+tiImcx/z27Jqw==)

#### Angular Signals​

Angular is undergoing some fundamental changes by foregoing dirty-checking and introducing its own implementation of a reactivity primitive. The Angular Signal API looks like this:

js

```
const count = signal(0)

count() // access the value
count.set(1) // set new value
count.update((v) => v + 1) // update based on previous value
```

Again, we can easily replicate the API in Vue:

js

```
import { shallowRef } from 'vue'

export function signal(initialValue) {
  const r = shallowRef(initialValue)
  const s = () => r.value
  s.set = (value) => {
    r.value = value
  }
  s.update = (updater) => {
    r.value = updater(r.value)
  }
  return s
}
```

[Try it in the Playground](https://play.vuejs.org/#eNp9Ul1v0zAU/SuWX9ZCSRh7m9IKGHuAB0AD8WQJZclt6s2xLX+ESlH+O9d2krbr1Df7nnPu17k9/aR11nmgt7SwleHaEQvO6w2TvNXKONITyxtZihWpVKu9g5oMZGtUS66yvJSNF6V5lyjZk71ikslKSeuQ7qUj61G+eL+cgFr5RwGITAkXiyVZb5IAn2/IB+QWeeoHO8GPg1aL0gH+CCl215u7mJ3bW9L3s3IYihyxifMlFRpJqewL1qN3TknysRK8el4zGjNlXtdYa9GFrjryllwvGY18QrisDLQgXZTnSX8pF64zzD7pDWDghbbI5/Hoip7tFL05eLErhVD/HmB75Edpyd8zc9DUaAbso3TrZeU4tjfawSV3vBR/SuFhSfrQUXLHBMvmKqe8A8siK7lmsi5gAbJhWARiIGD9hM7BIfHSgjGaHljzlDyGF2MEPQs6g5dpcAIm8Xs+2XxODTgUn0xVYdJ5RxPhKOd4gdMsA/rgLEq3vEEHlEQPYrbgaqu5APNDh6KWUTyuZC2jcWvfYswZD6spXu2gen4l/mT3Icboz3AWpgNGZ8yVBttM8P2v77DH9wy2qvYC2RfAB7BK+NBjon32ssa2j3ix26/xsrhsftv7vQNpp6FCo4E5RD6jeE93F0Y/tHuT3URd2OLwHyXleRY=)

Compared to Vue refs, Solid and Angular's getter-based API style provide some interesting trade-offs when used in Vue components:

- `()` is slightly less verbose than `.value`, but updating the value is more verbose.
- There is no ref-unwrapping: accessing values always require `()`. This makes value access consistent everywhere. This also means you can pass raw signals down as component props.

Whether these API styles suit you is to some extent subjective. Our goal here is to demonstrate the underlying similarity and trade-offs between these different API designs. We also want to show that Vue is flexible: you are not really locked into the existing APIs. Should it be necessary, you can create your own reactivity primitive API to suit more specific needs.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/extras/reactivity-in-depth.md)
