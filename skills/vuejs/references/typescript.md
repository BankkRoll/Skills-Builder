# TypeScript with Composition API​ and more

# TypeScript with Composition API​

> Vue.js - The Progressive JavaScript Framework

# TypeScript with Composition API​

[Watch an interactive video lesson on Scrimba](https://scrimba.com/links/vue-ts-composition-api)

> This page assumes you've already read the overview on [Using Vue with TypeScript](https://vuejs.org/guide/typescript/overview).

## Typing Component Props​

### Using<script setup>​

When using `<script setup>`, the `defineProps()` macro supports inferring the props types based on its argument:

vue

```
<script setup lang="ts">
const props = defineProps({
  foo: { type: String, required: true },
  bar: Number
})

props.foo // string
props.bar // number | undefined
</script>
```

This is called "runtime declaration", because the argument passed to `defineProps()` will be used as the runtime `props` option.

However, it is usually more straightforward to define props with pure types via a generic type argument:

vue

```
<script setup lang="ts">
const props = defineProps<{
  foo: string
  bar?: number
}>()
</script>
```

This is called "type-based declaration". The compiler will try to do its best to infer the equivalent runtime options based on the type argument. In this case, our second example compiles into the exact same runtime options as the first example.

You can use either type-based declaration OR runtime declaration, but you cannot use both at the same time.

We can also move the props types into a separate interface:

vue

```
<script setup lang="ts">
interface Props {
  foo: string
  bar?: number
}

const props = defineProps<Props>()
</script>
```

This also works if `Props` is imported from an external source. This feature requires TypeScript to be a peer dependency of Vue.

vue

```
<script setup lang="ts">
import type { Props } from './foo'

const props = defineProps<Props>()
</script>
```

#### Syntax Limitations​

In version 3.2 and below, the generic type parameter for `defineProps()` were limited to a type literal or a reference to a local interface.

This limitation has been resolved in 3.3. The latest version of Vue supports referencing imported and a limited set of complex types in the type parameter position. However, because the type to runtime conversion is still AST-based, some complex types that require actual type analysis, e.g. conditional types, are not supported. You can use conditional types for the type of a single prop, but not the entire props object.

### Props Default Values​

When using type-based declaration, we lose the ability to declare default values for the props. This can be resolved by using [Reactive Props Destructure](https://vuejs.org/guide/components/props#reactive-props-destructure) :

ts

```
interface Props {
  msg?: string
  labels?: string[]
}

const { msg = 'hello', labels = ['one', 'two'] } = defineProps<Props>()
```

In 3.4 and below, Reactive Props Destructure is not enabled by default. An alternative is to use the `withDefaults` compiler macro:

ts

```
interface Props {
  msg?: string
  labels?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  msg: 'hello',
  labels: () => ['one', 'two']
})
```

This will be compiled to equivalent runtime props `default` options. In addition, the `withDefaults` helper provides type checks for the default values, and ensures the returned `props` type has the optional flags removed for properties that do have default values declared.

INFO

Note that default values for mutable reference types (like arrays or objects) should be wrapped in functions when using `withDefaults` to avoid accidental modification and external side effects. This ensures each component instance gets its own copy of the default value. This is **not** necessary when using default values with destructure.

### Without<script setup>​

If not using `<script setup>`, it is necessary to use `defineComponent()` to enable props type inference. The type of the props object passed to `setup()` is inferred from the `props` option.

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    message: String
  },
  setup(props) {
    props.message // <-- type: string
  }
})
```

### Complex prop types​

With type-based declaration, a prop can use a complex type much like any other type:

vue

```
<script setup lang="ts">
interface Book {
  title: string
  author: string
  year: number
}

const props = defineProps<{
  book: Book
}>()
</script>
```

For runtime declaration, we can use the `PropType` utility type:

ts

```
import type { PropType } from 'vue'

const props = defineProps({
  book: Object as PropType<Book>
})
```

This works in much the same way if we're specifying the `props` option directly:

ts

```
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

export default defineComponent({
  props: {
    book: Object as PropType<Book>
  }
})
```

The `props` option is more commonly used with the Options API, so you'll find more detailed examples in the guide to [TypeScript with Options API](https://vuejs.org/guide/typescript/options-api#typing-component-props). The techniques shown in those examples also apply to runtime declarations using `defineProps()`.

## Typing Component Emits​

In `<script setup>`, the `emit` function can also be typed using either runtime declaration OR type declaration:

vue

```
<script setup lang="ts">
// runtime
const emit = defineEmits(['change', 'update'])

// options based
const emit = defineEmits({
  change: (id: number) => {
    // return `true` or `false` to indicate
    // validation pass / fail
  },
  update: (value: string) => {
    // return `true` or `false` to indicate
    // validation pass / fail
  }
})

// type-based
const emit = defineEmits<{
  (e: 'change', id: number): void
  (e: 'update', value: string): void
}>()

// 3.3+: alternative, more succinct syntax
const emit = defineEmits<{
  change: [id: number]
  update: [value: string]
}>()
</script>
```

The type argument can be one of the following:

1. A callable function type, but written as a type literal with [Call Signatures](https://www.typescriptlang.org/docs/handbook/2/functions.html#call-signatures). It will be used as the type of the returned `emit` function.
2. A type literal where the keys are the event names, and values are array / tuple types representing the additional accepted parameters for the event. The example above is using named tuples so each argument can have an explicit name.

As we can see, the type declaration gives us much finer-grained control over the type constraints of emitted events.

When not using `<script setup>`, `defineComponent()` is able to infer the allowed events for the `emit` function exposed on the setup context:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  emits: ['change'],
  setup(props, { emit }) {
    emit('change') // <-- type check / auto-completion
  }
})
```

## Typingref()​

Refs infer the type from the initial value:

ts

```
import { ref } from 'vue'

// inferred type: Ref<number>
const year = ref(2020)

// => TS Error: Type 'string' is not assignable to type 'number'.
year.value = '2020'
```

Sometimes we may need to specify complex types for a ref's inner value. We can do that by using the `Ref` type:

ts

```
import { ref } from 'vue'
import type { Ref } from 'vue'

const year: Ref<string | number> = ref('2020')

year.value = 2020 // ok!
```

Or, by passing a generic argument when calling `ref()` to override the default inference:

ts

```
// resulting type: Ref<string | number>
const year = ref<string | number>('2020')

year.value = 2020 // ok!
```

If you specify a generic type argument but omit the initial value, the resulting type will be a union type that includes `undefined`:

ts

```
// inferred type: Ref<number | undefined>
const n = ref<number>()
```

## Typingreactive()​

`reactive()` also implicitly infers the type from its argument:

ts

```
import { reactive } from 'vue'

// inferred type: { title: string }
const book = reactive({ title: 'Vue 3 Guide' })
```

To explicitly type a `reactive` property, we can use interfaces:

ts

```
import { reactive } from 'vue'

interface Book {
  title: string
  year?: number
}

const book: Book = reactive({ title: 'Vue 3 Guide' })
```

TIP

It's not recommended to use the generic argument of `reactive()` because the returned type, which handles nested ref unwrapping, is different from the generic argument type.

## Typingcomputed()​

`computed()` infers its type based on the getter's return value:

ts

```
import { ref, computed } from 'vue'

const count = ref(0)

// inferred type: ComputedRef<number>
const double = computed(() => count.value * 2)

// => TS Error: Property 'split' does not exist on type 'number'
const result = double.value.split('')
```

You can also specify an explicit type via a generic argument:

ts

```
const double = computed<number>(() => {
  // type error if this doesn't return a number
})
```

## Typing Event Handlers​

When dealing with native DOM events, it might be useful to type the argument we pass to the handler correctly. Let's take a look at this example:

vue

```
<script setup lang="ts">
function handleChange(event) {
  // `event` implicitly has `any` type
  console.log(event.target.value)
}
</script>

<template>
  <input type="text" @change="handleChange" />
</template>
```

Without type annotation, the `event` argument will implicitly have a type of `any`. This will also result in a TS error if `"strict": true` or `"noImplicitAny": true` are used in `tsconfig.json`. It is therefore recommended to explicitly annotate the argument of event handlers. In addition, you may need to use type assertions when accessing the properties of `event`:

ts

```
function handleChange(event: Event) {
  console.log((event.target as HTMLInputElement).value)
}
```

## Typing Provide / Inject​

Provide and inject are usually performed in separate components. To properly type injected values, Vue provides an `InjectionKey` interface, which is a generic type that extends `Symbol`. It can be used to sync the type of the injected value between the provider and the consumer:

ts

```
import { provide, inject } from 'vue'
import type { InjectionKey } from 'vue'

const key = Symbol() as InjectionKey<string>

provide(key, 'foo') // providing non-string value will result in error

const foo = inject(key) // type of foo: string | undefined
```

It's recommended to place the injection key in a separate file so that it can be imported in multiple components.

When using string injection keys, the type of the injected value will be `unknown`, and needs to be explicitly declared via a generic type argument:

ts

```
const foo = inject<string>('foo') // type: string | undefined
```

Notice the injected value can still be `undefined`, because there is no guarantee that a provider will provide this value at runtime.

The `undefined` type can be removed by providing a default value:

ts

```
const foo = inject<string>('foo', 'bar') // type: string
```

If you are sure that the value is always provided, you can also force cast the value:

ts

```
const foo = inject('foo') as string
```

## Typing Template Refs​

With Vue 3.5 and `@vue/language-tools` 2.1 (powering both the IDE language service and `vue-tsc`), the type of refs created by `useTemplateRef()` in SFCs can be **automatically inferred** for static refs based on what element the matching `ref` attribute is used on.

In cases where auto-inference is not possible, you can still cast the template ref to an explicit type via the generic argument:

ts

```
const el = useTemplateRef<HTMLInputElement>('el')
```

Usage before 3.5

Template refs should be created with an explicit generic type argument and an initial value of `null`:

vue

```
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const el = ref<HTMLInputElement | null>(null)

onMounted(() => {
  el.value?.focus()
})
</script>

<template>
  <input ref="el" />
</template>
```

To get the right DOM interface you can check pages like [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#technical_summary).

Note that for strict type safety, it is necessary to use optional chaining or type guards when accessing `el.value`. This is because the initial ref value is `null` until the component is mounted, and it can also be set to `null` if the referenced element is unmounted by `v-if`.

## Typing Component Template Refs​

With Vue 3.5 and `@vue/language-tools` 2.1 (powering both the IDE language service and `vue-tsc`), the type of refs created by `useTemplateRef()` in SFCs can be **automatically inferred** for static refs based on what element or component the matching `ref` attribute is used on.

In cases where auto-inference is not possible (e.g. non-SFC usage or dynamic components), you can still cast the template ref to an explicit type via the generic argument.

In order to get the instance type of an imported component, we need to first get its type via `typeof`, then use TypeScript's built-in `InstanceType` utility to extract its instance type:

App.vuevue

```
<script setup lang="ts">
import { useTemplateRef } from 'vue'
import Foo from './Foo.vue'
import Bar from './Bar.vue'

type FooType = InstanceType<typeof Foo>
type BarType = InstanceType<typeof Bar>

const compRef = useTemplateRef<FooType | BarType>('comp')
</script>

<template>
  <component :is="Math.random() > 0.5 ? Foo : Bar" ref="comp" />
</template>
```

In cases where the exact type of the component isn't available or isn't important, `ComponentPublicInstance` can be used instead. This will only include properties that are shared by all components, such as `$el`:

ts

```
import { useTemplateRef } from 'vue'
import type { ComponentPublicInstance } from 'vue'

const child = useTemplateRef<ComponentPublicInstance>('child')
```

In cases where the component referenced is a [generic component](https://vuejs.org/guide/typescript/overview#generic-components), for instance `MyGenericModal`:

MyGenericModal.vuevue

```
<script setup lang="ts" generic="ContentType extends string | number">
import { ref } from 'vue'

const content = ref<ContentType | null>(null)

const open = (newContent: ContentType) => (content.value = newContent)

defineExpose({
  open
})
</script>
```

It needs to be referenced using `ComponentExposed` from the [vue-component-type-helpers](https://www.npmjs.com/package/vue-component-type-helpers) library as `InstanceType` won't work.

App.vuevue

```
<script setup lang="ts">
import { useTemplateRef } from 'vue'
import MyGenericModal from './MyGenericModal.vue'
import type { ComponentExposed } from 'vue-component-type-helpers'

const modal =
  useTemplateRef<ComponentExposed<typeof MyGenericModal>>('modal')

const openModal = () => {
  modal.value?.open('newValue')
}
</script>
```

Note that with `@vue/language-tools` 2.1+, static template refs' types can be automatically inferred and the above is only needed in edge cases.

## Typing Global Custom Directives​

In order to get type hints and type checking for global custom directives declared with `app.directive()`, you can extend `ComponentCustomProperties`

src/directives/highlight.tsts

```
import type { Directive } from 'vue'

export type HighlightDirective = Directive<HTMLElement, string>

declare module 'vue' {
  export interface ComponentCustomProperties {
    // prefix with v (v-highlight)
    vHighlight: HighlightDirective
  }
}

export default {
  mounted: (el, binding) => {
    el.style.backgroundColor = binding.value
  }
} satisfies HighlightDirective
```

main.tsts

```
import highlight from './directives/highlight'
// ...other code
const app = createApp(App)
app.directive('highlight', highlight)
```

Usage in component

App.vuevue

```
<template>
  <p v-highlight="'blue'">This sentence is important!</p>
</template>
```

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/typescript/composition-api.md)

---

# TypeScript with Options API​

> Vue.js - The Progressive JavaScript Framework

# TypeScript with Options API​

> This page assumes you've already read the overview on [Using Vue with TypeScript](https://vuejs.org/guide/typescript/overview).

TIP

While Vue does support TypeScript usage with Options API, it is recommended to use Vue with TypeScript via Composition API as it offers simpler, more efficient and more robust type inference.

## Typing Component Props​

Type inference for props in Options API requires wrapping the component with `defineComponent()`. With it, Vue is able to infer the types for the props based on the `props` option, taking additional options such as `required: true` and `default` into account:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  // type inference enabled
  props: {
    name: String,
    id: [Number, String],
    msg: { type: String, required: true },
    metadata: null
  },
  mounted() {
    this.name // type: string | undefined
    this.id // type: number | string | undefined
    this.msg // type: string
    this.metadata // type: any
  }
})
```

However, the runtime `props` options only support using constructor functions as a prop's type - there is no way to specify complex types such as objects with nested properties or function call signatures.

To annotate complex props types, we can use the `PropType` utility type:

ts

```
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

interface Book {
  title: string
  author: string
  year: number
}

export default defineComponent({
  props: {
    book: {
      // provide more specific type to `Object`
      type: Object as PropType<Book>,
      required: true
    },
    // can also annotate functions
    callback: Function as PropType<(id: number) => void>
  },
  mounted() {
    this.book.title // string
    this.book.year // number

    // TS Error: argument of type 'string' is not
    // assignable to parameter of type 'number'
    this.callback?.('123')
  }
})
```

### Caveats​

If your TypeScript version is less than `4.7`, you have to be careful when using function values for `validator` and `default` prop options - make sure to use arrow functions:

ts

```
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

interface Book {
  title: string
  year?: number
}

export default defineComponent({
  props: {
    bookA: {
      type: Object as PropType<Book>,
      // Make sure to use arrow functions if your TypeScript version is less than 4.7
      default: () => ({
        title: 'Arrow Function Expression'
      }),
      validator: (book: Book) => !!book.title
    }
  }
})
```

This prevents TypeScript from having to infer the type of `this` inside these functions, which, unfortunately, can cause the type inference to fail. It was a previous [design limitation](https://github.com/microsoft/TypeScript/issues/38845), and now has been improved in [TypeScript 4.7](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-7.html#improved-function-inference-in-objects-and-methods).

## Typing Component Emits​

We can declare the expected payload type for an emitted event using the object syntax of the `emits` option. Also, all non-declared emitted events will throw a type error when called:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  emits: {
    addBook(payload: { bookName: string }) {
      // perform runtime validation
      return payload.bookName.length > 0
    }
  },
  methods: {
    onSubmit() {
      this.$emit('addBook', {
        bookName: 123 // Type error!
      })

      this.$emit('non-declared-event') // Type error!
    }
  }
})
```

## Typing Computed Properties​

A computed property infers its type based on its return value:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      message: 'Hello!'
    }
  },
  computed: {
    greeting() {
      return this.message + '!'
    }
  },
  mounted() {
    this.greeting // type: string
  }
})
```

In some cases, you may want to explicitly annotate the type of a computed property to ensure its implementation is correct:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      message: 'Hello!'
    }
  },
  computed: {
    // explicitly annotate return type
    greeting(): string {
      return this.message + '!'
    },

    // annotating a writable computed property
    greetingUppercased: {
      get(): string {
        return this.greeting.toUpperCase()
      },
      set(newValue: string) {
        this.message = newValue.toUpperCase()
      }
    }
  }
})
```

Explicit annotations may also be required in some edge cases where TypeScript fails to infer the type of a computed property due to circular inference loops.

## Typing Event Handlers​

When dealing with native DOM events, it might be useful to type the argument we pass to the handler correctly. Let's take a look at this example:

vue

```
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  methods: {
    handleChange(event) {
      // `event` implicitly has `any` type
      console.log(event.target.value)
    }
  }
})
</script>

<template>
  <input type="text" @change="handleChange" />
</template>
```

Without type annotation, the `event` argument will implicitly have a type of `any`. This will also result in a TS error if `"strict": true` or `"noImplicitAny": true` are used in `tsconfig.json`. It is therefore recommended to explicitly annotate the argument of event handlers. In addition, you may need to use type assertions when accessing the properties of `event`:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  methods: {
    handleChange(event: Event) {
      console.log((event.target as HTMLInputElement).value)
    }
  }
})
```

## Augmenting Global Properties​

Some plugins install globally available properties to all component instances via [app.config.globalProperties](https://vuejs.org/api/application#app-config-globalproperties). For example, we may install `this.$http` for data-fetching or `this.$translate` for internationalization. To make this play well with TypeScript, Vue exposes a `ComponentCustomProperties` interface designed to be augmented via [TypeScript module augmentation](https://www.typescriptlang.org/docs/handbook/declaration-merging.html#module-augmentation):

ts

```
import axios from 'axios'

declare module 'vue' {
  interface ComponentCustomProperties {
    $http: typeof axios
    $translate: (key: string) => string
  }
}
```

See also:

- [TypeScript unit tests for component type extensions](https://github.com/vuejs/core/blob/main/packages-private/dts-test/componentTypeExtensions.test-d.tsx)

### Type Augmentation Placement​

We can put this type augmentation in a `.ts` file, or in a project-wide `*.d.ts` file. Either way, make sure it is included in `tsconfig.json`. For library / plugin authors, this file should be specified in the `types` property in `package.json`.

In order to take advantage of module augmentation, you will need to ensure the augmentation is placed in a [TypeScript module](https://www.typescriptlang.org/docs/handbook/modules.html). That is to say, the file needs to contain at least one top-level `import` or `export`, even if it is just `export {}`. If the augmentation is placed outside of a module, it will overwrite the original types rather than augmenting them!

ts

```
// Does not work, overwrites the original types.
declare module 'vue' {
  interface ComponentCustomProperties {
    $translate: (key: string) => string
  }
}
```

ts

```
// Works correctly
export {}

declare module 'vue' {
  interface ComponentCustomProperties {
    $translate: (key: string) => string
  }
}
```

## Augmenting Custom Options​

Some plugins, for example `vue-router`, provide support for custom component options such as `beforeRouteEnter`:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  beforeRouteEnter(to, from, next) {
    // ...
  }
})
```

Without proper type augmentation, the arguments of this hook will implicitly have `any` type. We can augment the `ComponentCustomOptions` interface to support these custom options:

ts

```
import { Route } from 'vue-router'

declare module 'vue' {
  interface ComponentCustomOptions {
    beforeRouteEnter?(to: Route, from: Route, next: () => void): void
  }
}
```

Now the `beforeRouteEnter` option will be properly typed. Note this is just an example - well-typed libraries like `vue-router` should automatically perform these augmentations in their own type definitions.

The placement of this augmentation is subject to the [same restrictions](#type-augmentation-placement) as global property augmentations.

See also:

- [TypeScript unit tests for component type extensions](https://github.com/vuejs/core/blob/main/packages-private/dts-test/componentTypeExtensions.test-d.tsx)

## Typing Global Custom Directives​

See: [Typing Custom Global Directives](https://vuejs.org/guide/typescript/composition-api#typing-global-custom-directives)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/typescript/options-api.md)

---

# Using Vue with TypeScript​

> Vue.js - The Progressive JavaScript Framework

# Using Vue with TypeScript​

A type system like TypeScript can detect many common errors via static analysis at build time. This reduces the chance of runtime errors in production, and also allows us to more confidently refactor code in large-scale applications. TypeScript also improves developer ergonomics via type-based auto-completion in IDEs.

Vue is written in TypeScript itself and provides first-class TypeScript support. All official Vue packages come with bundled type declarations that should work out-of-the-box.

## Project Setup​

[create-vue](https://github.com/vuejs/create-vue), the official project scaffolding tool, offers the options to scaffold a [Vite](https://vitejs.dev/)-powered, TypeScript-ready Vue project.

### Overview​

With a Vite-based setup, the dev server and the bundler are transpilation-only and do not perform any type-checking. This ensures the Vite dev server stays blazing fast even when using TypeScript.

- During development, we recommend relying on a good [IDE setup](#ide-support) for instant feedback on type errors.
- If using SFCs, use the [vue-tsc](https://github.com/vuejs/language-tools/tree/master/packages/tsc) utility for command line type checking and type declaration generation. `vue-tsc` is a wrapper around `tsc`, TypeScript's own command line interface. It works largely the same as `tsc` except that it supports Vue SFCs in addition to TypeScript files. You can run `vue-tsc` in watch mode in parallel to the Vite dev server, or use a Vite plugin like [vite-plugin-checker](https://vite-plugin-checker.netlify.app/) which runs the checks in a separate worker thread.
- Vue CLI also provides TypeScript support, but is no longer recommended. See [notes below](#note-on-vue-cli-and-ts-loader).

### IDE Support​

- [Visual Studio Code](https://code.visualstudio.com/) (VS Code) is strongly recommended for its great out-of-the-box support for TypeScript.
  - [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar) is the official VS Code extension that provides TypeScript support inside Vue SFCs, along with many other great features.
    TIP
    Vue - Official extension replaces [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur), our previous official VS Code extension for Vue 2. If you have Vetur currently installed, make sure to disable it in Vue 3 projects.
- [WebStorm](https://www.jetbrains.com/webstorm/) also provides out-of-the-box support for both TypeScript and Vue. Other JetBrains IDEs support them too, either out of the box or via [a free plugin](https://plugins.jetbrains.com/plugin/9442-vue-js). As of version 2023.2, WebStorm and the Vue Plugin come with built-in support for the Vue Language Server. You can set the Vue service to use Volar integration on all TypeScript versions, under Settings > Languages & Frameworks > TypeScript > Vue. By default, Volar will be used for TypeScript versions 5.0 and higher.

### Configuringtsconfig.json​

Projects scaffolded via `create-vue` include pre-configured `tsconfig.json`. The base config is abstracted in the [@vue/tsconfig](https://github.com/vuejs/tsconfig) package. Inside the project, we use [Project References](https://www.typescriptlang.org/docs/handbook/project-references.html) to ensure correct types for code running in different environments (e.g. app code and test code should have different global variables).

When configuring `tsconfig.json` manually, some notable options include:

- [compilerOptions.isolatedModules](https://www.typescriptlang.org/tsconfig#isolatedModules) is set to `true` because Vite uses [esbuild](https://esbuild.github.io/) for transpiling TypeScript and is subject to single-file transpile limitations. [compilerOptions.verbatimModuleSyntax](https://www.typescriptlang.org/tsconfig#verbatimModuleSyntax) is [a superset ofisolatedModules](https://github.com/microsoft/TypeScript/issues/53601) and is a good choice, too - it's what [@vue/tsconfig](https://github.com/vuejs/tsconfig) uses.
- If you're using Options API, you need to set [compilerOptions.strict](https://www.typescriptlang.org/tsconfig#strict) to `true` (or at least enable [compilerOptions.noImplicitThis](https://www.typescriptlang.org/tsconfig#noImplicitThis), which is a part of the `strict` flag) to leverage type checking of `this` in component options. Otherwise `this` will be treated as `any`.
- If you have configured resolver aliases in your build tool, for example the `@/*` alias configured by default in a `create-vue` project, you need to also configure it for TypeScript via [compilerOptions.paths](https://www.typescriptlang.org/tsconfig#paths).
- If you intend to use TSX with Vue, set [compilerOptions.jsx](https://www.typescriptlang.org/tsconfig#jsx) to `"preserve"`, and set [compilerOptions.jsxImportSource](https://www.typescriptlang.org/tsconfig#jsxImportSource) to `"vue"`.

See also:

- [Official TypeScript compiler options docs](https://www.typescriptlang.org/docs/handbook/compiler-options.html)
- [esbuild TypeScript compilation caveats](https://esbuild.github.io/content-types/#typescript-caveats)

### Note on Vue CLI andts-loader​

In webpack-based setups such as Vue CLI, it is common to perform type checking as part of the module transform pipeline, for example with `ts-loader`. This, however, isn't a clean solution because the type system needs knowledge of the entire module graph to perform type checks. Individual module's transform step simply is not the right place for the task. It leads to the following problems:

- `ts-loader` can only type check post-transform code. This doesn't align with the errors we see in IDEs or from `vue-tsc`, which map directly back to the source code.
- Type checking can be slow. When it is performed in the same thread / process with code transformations, it significantly affects the build speed of the entire application.
- We already have type checking running right in our IDE in a separate process, so the cost of dev experience slow down simply isn't a good trade-off.

If you are currently using Vue 3 + TypeScript via Vue CLI, we strongly recommend migrating over to Vite. We are also working on CLI options to enable transpile-only TS support, so that you can switch to `vue-tsc` for type checking.

## General Usage Notes​

### defineComponent()​

To let TypeScript properly infer types inside component options, we need to define components with [defineComponent()](https://vuejs.org/api/general#definecomponent):

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  // type inference enabled
  props: {
    name: String,
    msg: { type: String, required: true }
  },
  data() {
    return {
      count: 1
    }
  },
  mounted() {
    this.name // type: string | undefined
    this.msg // type: string
    this.count // type: number
  }
})
```

`defineComponent()` also supports inferring the props passed to `setup()` when using Composition API without `<script setup>`:

ts

```
import { defineComponent } from 'vue'

export default defineComponent({
  // type inference enabled
  props: {
    message: String
  },
  setup(props) {
    props.message // type: string | undefined
  }
})
```

See also:

- [Note on webpack Treeshaking](https://vuejs.org/api/general#note-on-webpack-treeshaking)
- [type tests fordefineComponent](https://github.com/vuejs/core/blob/main/packages-private/dts-test/defineComponent.test-d.tsx)

TIP

`defineComponent()` also enables type inference for components defined in plain JavaScript.

### Usage in Single-File Components​

To use TypeScript in SFCs, add the `lang="ts"` attribute to `<script>` tags. When `lang="ts"` is present, all template expressions also enjoy stricter type checking.

vue

```
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      count: 1
    }
  }
})
</script>

<template>
  
  {{ count.toFixed(2) }}
</template>
```

`lang="ts"` can also be used with `<script setup>`:

vue

```
<script setup lang="ts">
// TypeScript enabled
import { ref } from 'vue'

const count = ref(1)
</script>

<template>
  
  {{ count.toFixed(2) }}
</template>
```

### TypeScript in Templates​

The `<template>` also supports TypeScript in binding expressions when `<script lang="ts">` or `<script setup lang="ts">` is used. This is useful in cases where you need to perform type casting in template expressions.

Here's a contrived example:

vue

```
<script setup lang="ts">
let x: string | number = 1
</script>

<template>
  
  {{ x.toFixed(2) }}
</template>
```

This can be worked around with an inline type cast:

vue

```
<script setup lang="ts">
let x: string | number = 1
</script>

<template>
  {{ (x as number).toFixed(2) }}
</template>
```

TIP

If using Vue CLI or a webpack-based setup, TypeScript in template expressions requires `vue-loader@^16.8.0`.

### Usage with TSX​

Vue also supports authoring components with JSX / TSX. Details are covered in the [Render Function & JSX](https://vuejs.org/guide/extras/render-function#jsx-tsx) guide.

## Generic Components​

Generic components are supported in two cases:

- In SFCs: [<script setup>with thegenericattribute](https://vuejs.org/api/sfc-script-setup#generics)
- Render function / JSX components: [defineComponent()'s function signature](https://vuejs.org/api/general#function-signature)

## API-Specific Recipes​

- [TS with Composition API](https://vuejs.org/guide/typescript/composition-api)
- [TS with Options API](https://vuejs.org/guide/typescript/options-api)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/typescript/overview.md)
