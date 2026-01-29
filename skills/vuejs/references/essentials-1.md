# Creating a Vue Application​ and more

# Creating a Vue Application​

> Vue.js - The Progressive JavaScript Framework

# Creating a Vue Application​

## The Application Instance​

Every Vue application starts by creating a new **application instance** with the [createApp](https://vuejs.org/api/application#createapp) function:

js

```
import { createApp } from 'vue'

const app = createApp({
  /* root component options */
})
```

## The Root Component​

The object we are passing into `createApp` is in fact a component. Every app requires a "root component" that can contain other components as its children.

If you are using Single-File Components, we typically import the root component from another file:

js

```
import { createApp } from 'vue'
// import the root component App from a single-file component.
import App from './App.vue'

const app = createApp(App)
```

While many examples in this guide only need a single component, most real applications are organized into a tree of nested, reusable components. For example, a Todo application's component tree might look like this:

```
App (root component)
├─ TodoList
│  └─ TodoItem
│     ├─ TodoDeleteButton
│     └─ TodoEditButton
└─ TodoFooter
   ├─ TodoClearButton
   └─ TodoStatistics
```

In later sections of the guide, we will discuss how to define and compose multiple components together. Before that, we will focus on what happens inside a single component.

## Mounting the App​

An application instance won't render anything until its `.mount()` method is called. It expects a "container" argument, which can either be an actual DOM element or a selector string:

html

```
<div id="app"></div>
```

js

```
app.mount('#app')
```

The content of the app's root component will be rendered inside the container element. The container element itself is not considered part of the app.

The `.mount()` method should always be called after all app configurations and asset registrations are done. Also note that its return value, unlike the asset registration methods, is the root component instance instead of the application instance.

### In-DOM Root Component Template​

The template for the root component is usually part of the component itself, but it is also possible to provide the template separately by writing it directly inside the mount container:

html

```
<div id="app">
  <button @click="count++">{{ count }}</button>
</div>
```

js

```
import { createApp } from 'vue'

const app = createApp({
  data() {
    return {
      count: 0
    }
  }
})

app.mount('#app')
```

Vue will automatically use the container's `innerHTML` as the template if the root component does not already have a `template` option.

In-DOM templates are often used in applications that are [using Vue without a build step](https://vuejs.org/guide/quick-start#using-vue-from-cdn). They can also be used in conjunction with server-side frameworks, where the root template might be generated dynamically by the server.

## App Configurations​

The application instance exposes a `.config` object that allows us to configure a few app-level options, for example, defining an app-level error handler that captures errors from all descendant components:

js

```
app.config.errorHandler = (err) => {
  /* handle error */
}
```

The application instance also provides a few methods for registering app-scoped assets. For example, registering a component:

js

```
app.component('TodoDeleteButton', TodoDeleteButton)
```

This makes the `TodoDeleteButton` available for use anywhere in our app. We will discuss registration for components and other types of assets in later sections of the guide. You can also browse the full list of application instance APIs in its [API reference](https://vuejs.org/api/application).

Make sure to apply all app configurations before mounting the app!

## Multiple Application Instances​

You are not limited to a single application instance on the same page. The `createApp` API allows multiple Vue applications to co-exist on the same page, each with its own scope for configuration and global assets:

js

```
const app1 = createApp({
  /* ... */
})
app1.mount('#container-1')

const app2 = createApp({
  /* ... */
})
app2.mount('#container-2')
```

If you are using Vue to enhance server-rendered HTML and only need Vue to control specific parts of a large page, avoid mounting a single Vue application instance on the entire page. Instead, create multiple small application instances and mount them on the elements they are responsible for.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/application.md)

---

# Class and Style Bindings​

> Vue.js - The Progressive JavaScript Framework

# Class and Style Bindings​

A common need for data binding is manipulating an element's class list and inline styles. Since `class` and `style` are both attributes, we can use `v-bind` to assign them a string value dynamically, much like with other attributes. However, trying to generate those values using string concatenation can be annoying and error-prone. For this reason, Vue provides special enhancements when `v-bind` is used with `class` and `style`. In addition to strings, the expressions can also evaluate to objects or arrays.

## Binding HTML Classes​

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/dynamic-css-classes-with-vue-3?friend=vuejs)[Watch a free video lesson on Vue School](https://vueschool.io/lessons/vue-fundamentals-capi-dynamic-css-classes-with-vue?friend=vuejs)

### Binding to Objects​

We can pass an object to `:class` (short for `v-bind:class`) to dynamically toggle classes:

template

```
<div :class="{ active: isActive }"></div>
```

The above syntax means the presence of the `active` class will be determined by the [truthiness](https://developer.mozilla.org/en-US/docs/Glossary/Truthy) of the data property `isActive`.

You can have multiple classes toggled by having more fields in the object. In addition, the `:class` directive can also co-exist with the plain `class` attribute. So given the following state:

js

```
const isActive = ref(true)
const hasError = ref(false)
```

js

```
data() {
  return {
    isActive: true,
    hasError: false
  }
}
```

And the following template:

template

```
<div
  class="static"
  :class="{ active: isActive, 'text-danger': hasError }"
></div>
```

It will render:

template

```
<div class="static active"></div>
```

When `isActive` or `hasError` changes, the class list will be updated accordingly. For example, if `hasError` becomes `true`, the class list will become `"static active text-danger"`.

The bound object doesn't have to be inline:

js

```
const classObject = reactive({
  active: true,
  'text-danger': false
})
```

js

```
data() {
  return {
    classObject: {
      active: true,
      'text-danger': false
    }
  }
}
```

template

```
<div :class="classObject"></div>
```

This will render:

template

```
<div class="active"></div>
```

We can also bind to a [computed property](https://vuejs.org/guide/essentials/computed) that returns an object. This is a common and powerful pattern:

js

```
const isActive = ref(true)
const error = ref(null)

const classObject = computed(() => ({
  active: isActive.value && !error.value,
  'text-danger': error.value && error.value.type === 'fatal'
}))
```

js

```
data() {
  return {
    isActive: true,
    error: null
  }
},
computed: {
  classObject() {
    return {
      active: this.isActive && !this.error,
      'text-danger': this.error && this.error.type === 'fatal'
    }
  }
}
```

template

```
<div :class="classObject"></div>
```

### Binding to Arrays​

We can bind `:class` to an array to apply a list of classes:

js

```
const activeClass = ref('active')
const errorClass = ref('text-danger')
```

js

```
data() {
  return {
    activeClass: 'active',
    errorClass: 'text-danger'
  }
}
```

template

```
<div :class="[activeClass, errorClass]"></div>
```

Which will render:

template

```
<div class="active text-danger"></div>
```

If you would like to also toggle a class in the list conditionally, you can do it with a ternary expression:

template

```
<div :class="[isActive ? activeClass : '', errorClass]"></div>
```

This will always apply `errorClass`, but `activeClass` will only be applied when `isActive` is truthy.

However, this can be a bit verbose if you have multiple conditional classes. That's why it's also possible to use the object syntax inside the array syntax:

template

```
<div :class="[{ [activeClass]: isActive }, errorClass]"></div>
```

### With Components​

> This section assumes knowledge of [Components](https://vuejs.org/guide/essentials/component-basics). Feel free to skip it and come back later.

When you use the `class` attribute on a component with a single root element, those classes will be added to the component's root element and merged with any existing class already on it.

For example, if we have a component named `MyComponent` with the following template:

template

```

<p class="foo bar">Hi!</p>
```

Then add some classes when using it:

template

```

<MyComponent class="baz boo" />
```

The rendered HTML will be:

template

```
<p class="foo bar baz boo">Hi!</p>
```

The same is true for class bindings:

template

```
<MyComponent :class="{ active: isActive }" />
```

When `isActive` is truthy, the rendered HTML will be:

template

```
<p class="foo bar active">Hi!</p>
```

If your component has multiple root elements, you would need to define which element will receive this class. You can do this using the `$attrs` component property:

template

```

<p :class="$attrs.class">Hi!</p>
<span>This is a child component</span>
```

template

```
<MyComponent class="baz" />
```

Will render:

html

```
<p class="baz">Hi!</p>
<span>This is a child component</span>
```

You can learn more about component attribute inheritance in [Fallthrough Attributes](https://vuejs.org/guide/components/attrs) section.

## Binding Inline Styles​

### Binding to Objects​

`:style` supports binding to JavaScript object values - it corresponds to an [HTML element'sstyleproperty](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style):

js

```
const activeColor = ref('red')
const fontSize = ref(30)
```

js

```
data() {
  return {
    activeColor: 'red',
    fontSize: 30
  }
}
```

template

```
<div :style="{ color: activeColor, fontSize: fontSize + 'px' }"></div>
```

Although camelCase keys are recommended, `:style` also supports kebab-cased CSS property keys (corresponds to how they are used in actual CSS) - for example:

template

```
<div :style="{ 'font-size': fontSize + 'px' }"></div>
```

It is often a good idea to bind to a style object directly so that the template is cleaner:

js

```
const styleObject = reactive({
  color: 'red',
  fontSize: '30px'
})
```

js

```
data() {
  return {
    styleObject: {
      color: 'red',
      fontSize: '13px'
    }
  }
}
```

template

```
<div :style="styleObject"></div>
```

Again, object style binding is often used in conjunction with computed properties that return objects.

`:style` directives can also coexist with regular style attributes, just like `:class`.

Template:

template

```
<h1 style="color: red" :style="'font-size: 1em'">hello</h1>
```

It will render:

template

```
<h1 style="color: red; font-size: 1em;">hello</h1>
```

### Binding to Arrays​

We can bind `:style` to an array of multiple style objects. These objects will be merged and applied to the same element:

template

```
<div :style="[baseStyles, overridingStyles]"></div>
```

### Auto-prefixing​

When you use a CSS property that requires a [vendor prefix](https://developer.mozilla.org/en-US/docs/Glossary/Vendor_Prefix) in `:style`, Vue will automatically add the appropriate prefix. Vue does this by checking at runtime to see which style properties are supported in the current browser. If the browser doesn't support a particular property then various prefixed variants will be tested to try to find one that is supported.

### Multiple Values​

You can provide an array of multiple (prefixed) values to a style property, for example:

template

```
<div :style="{ display: ['-webkit-box', '-ms-flexbox', 'flex'] }"></div>
```

This will only render the last value in the array which the browser supports. In this example, it will render `display: flex` for browsers that support the unprefixed version of flexbox.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/class-and-style.md)

---

# Components Basics​

> Vue.js - The Progressive JavaScript Framework

# Components Basics​

[Watch an interactive video lesson on Scrimba](https://scrimba.com/links/vue-component-basics)

Components allow us to split the UI into independent and reusable pieces, and think about each piece in isolation. It's common for an app to be organized into a tree of nested components:

![Component Tree](https://vuejs.org/assets/components.B1JZbf0_.png)

This is very similar to how we nest native HTML elements, but Vue implements its own component model that allows us to encapsulate custom content and logic in each component. Vue also plays nicely with native Web Components. If you are curious about the relationship between Vue Components and native Web Components, [read more here](https://vuejs.org/guide/extras/web-components).

## Defining a Component​

When using a build step, we typically define each Vue component in a dedicated file using the `.vue` extension - known as a [Single-File Component](https://vuejs.org/guide/scaling-up/sfc) (SFC for short):

vue

```
<script>
export default {
  data() {
    return {
      count: 0
    }
  }
}
</script>

<template>
  <button @click="count++">You clicked me {{ count }} times.</button>
</template>
```

vue

```
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <button @click="count++">You clicked me {{ count }} times.</button>
</template>
```

When not using a build step, a Vue component can be defined as a plain JavaScript object containing Vue-specific options:

js

```
export default {
  data() {
    return {
      count: 0
    }
  },
  template: `
    <button @click="count++">
      You clicked me {{ count }} times.
    </button>`
}
```

js

```
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)
    return { count }
  },
  template: `
    <button @click="count++">
      You clicked me {{ count }} times.
    </button>`
  // Can also target an in-DOM template:
  // template: '#my-template-element'
}
```

The template is inlined as a JavaScript string here, which Vue will compile on the fly. You can also use an ID selector pointing to an element (usually native `<template>` elements) - Vue will use its content as the template source.

The example above defines a single component and exports it as the default export of a `.js` file, but you can use named exports to export multiple components from the same file.

## Using a Component​

TIP

We will be using SFC syntax for the rest of this guide - the concepts around components are the same regardless of whether you are using a build step or not. The [Examples](https://vuejs.org/examples/) section shows component usage in both scenarios.

To use a child component, we need to import it in the parent component. Assuming we placed our counter component inside a file called `ButtonCounter.vue`, the component will be exposed as the file's default export:

vue

```
<script>
import ButtonCounter from './ButtonCounter.vue'

export default {
  components: {
    ButtonCounter
  }
}
</script>

<template>
  <h1>Here is a child component!</h1>
  <ButtonCounter />
</template>
```

To expose the imported component to our template, we need to [register](https://vuejs.org/guide/components/registration) it with the `components` option. The component will then be available as a tag using the key it is registered under.

vue

```
<script setup>
import ButtonCounter from './ButtonCounter.vue'
</script>

<template>
  <h1>Here is a child component!</h1>
  <ButtonCounter />
</template>
```

With `<script setup>`, imported components are automatically made available to the template.

It's also possible to globally register a component, making it available to all components in a given app without having to import it. The pros and cons of global vs. local registration is discussed in the dedicated [Component Registration](https://vuejs.org/guide/components/registration) section.

Components can be reused as many times as you want:

template

```
<h1>Here are many child components!</h1>
<ButtonCounter />
<ButtonCounter />
<ButtonCounter />
```

[Try it in the Playground](https://play.vuejs.org/#eNqVUE1LxDAQ/StjLqusNHotcfHj4l8QcontLBtsJiGdiFL6301SdrEqyEJyeG9m3ps3k3gIoXlPKFqhxi7awDtN1gUfGR4Ts6cnn4gxwj56B5tGrtgyutEEoAk/6lCPe5MGhqmwnc9KhMRjuxCwFi3UrCk/JU/uGTC6MBjGglgdbnfPGBFM/s7QJ3QHO/TfxC+UzD21d72zPItU8uQrrsWvnKsT/ZW2N2wur45BI3KKdETlFlmphZsF58j/RgdQr3UJuO8G273daVFFtlstahngxSeoNezBIUzTYgPzDGwdjk1VkYvMj4jzF0nwsyQ=)

[Try it in the Playground](https://play.vuejs.org/#eNqVj91KAzEQhV/lmJsqlY3eSlr8ufEVhNys6ZQGNz8kE0GWfXez2SJUsdCLuZiZM9+ZM4qnGLvPQuJBqGySjYxMXOJWe+tiSIznwhz8SyieKWGfgsOqkyfTGbDSXsmFUG9rw+Ti0DPNHavD/faVEqGv5Xr/BXOwww4mVBNPnvOVklXTtKeO8qKhkj++4lb8+fL/mCMS7TEdAy6BtDfBZ65fVgA2s+L67uZMUEC9N0s8msGaj40W7Xa91qKtgbdQ0Ha0gyOM45E+TWDrKHeNIhfMr0DTN4U0me8=)

Notice that when clicking on the buttons, each one maintains its own, separate `count`. That's because each time you use a component, a new **instance** of it is created.

In SFCs, it's recommended to use `PascalCase` tag names for child components to differentiate from native HTML elements. Although native HTML tag names are case-insensitive, Vue SFC is a compiled format so we are able to use case-sensitive tag names in it. We are also able to use `/>` to close a tag.

If you are authoring your templates directly in a DOM (e.g. as the content of a native `<template>` element), the template will be subject to the browser's native HTML parsing behavior. In such cases, you will need to use `kebab-case` and explicit closing tags for components:

template

```

<button-counter></button-counter>
<button-counter></button-counter>
<button-counter></button-counter>
```

See [in-DOM template parsing caveats](#in-dom-template-parsing-caveats) for more details.

## Passing Props​

If we are building a blog, we will likely need a component representing a blog post. We want all the blog posts to share the same visual layout, but with different content. Such a component won't be useful unless you can pass data to it, such as the title and content of the specific post we want to display. That's where props come in.

Props are custom attributes you can register on a component. To pass a title to our blog post component, we must declare it in the list of props this component accepts, using the [props](https://vuejs.org/api/options-state#props) option[defineProps](https://vuejs.org/api/sfc-script-setup#defineprops-defineemits) macro:

BlogPost.vuevue

```
<script>
export default {
  props: ['title']
}
</script>

<template>
  <h4>{{ title }}</h4>
</template>
```

When a value is passed to a prop attribute, it becomes a property on that component instance. The value of that property is accessible within the template and on the component's `this` context, just like any other component property.

BlogPost.vuevue

```
<script setup>
defineProps(['title'])
</script>

<template>
  <h4>{{ title }}</h4>
</template>
```

`defineProps` is a compile-time macro that is only available inside `<script setup>` and does not need to be explicitly imported. Declared props are automatically exposed to the template. `defineProps` also returns an object that contains all the props passed to the component, so that we can access them in JavaScript if needed:

js

```
const props = defineProps(['title'])
console.log(props.title)
```

See also: [Typing Component Props](https://vuejs.org/guide/typescript/composition-api#typing-component-props)

If you are not using `<script setup>`, props should be declared using the `props` option, and the props object will be passed to `setup()` as the first argument:

js

```
export default {
  props: ['title'],
  setup(props) {
    console.log(props.title)
  }
}
```

A component can have as many props as you like and, by default, any value can be passed to any prop.

Once a prop is registered, you can pass data to it as a custom attribute, like this:

template

```
<BlogPost title="My journey with Vue" />
<BlogPost title="Blogging with Vue" />
<BlogPost title="Why Vue is so fun" />
```

In a typical app, however, you'll likely have an array of posts in your parent component:

js

```
export default {
  // ...
  data() {
    return {
      posts: [
        { id: 1, title: 'My journey with Vue' },
        { id: 2, title: 'Blogging with Vue' },
        { id: 3, title: 'Why Vue is so fun' }
      ]
    }
  }
}
```

js

```
const posts = ref([
  { id: 1, title: 'My journey with Vue' },
  { id: 2, title: 'Blogging with Vue' },
  { id: 3, title: 'Why Vue is so fun' }
])
```

Then want to render a component for each one, using `v-for`:

template

```
<BlogPost
  v-for="post in posts"
  :key="post.id"
  :title="post.title"
 />
```

[Try it in the Playground](https://play.vuejs.org/#eNp9UU1rhDAU/CtDLrawVfpxklRo74We2kPtQdaoaTUJ8bmtiP+9ia6uC2VBgjOZeXnz3sCejAkPnWAx4+3eSkNJqmRjtCU817p81S2hsLpBEEYL4Q1BqoBUid9Jmosi62rC4Nm9dn4lFLXxTGAt5dG482eeUXZ1vdxbQZ1VCwKM0zr3x4KBATKPcbsDSapFjOClx5d2JtHjR1KFN9fTsfbWcXdy+CZKqcqL+vuT/r3qvQqyRatRdMrpF/nn/DNhd7iPR+v8HCDRmDoj4RHxbfyUDjeFto8p8yEh1Rw2ZV4JxN+iP96FMvest8RTTws/gdmQ8HUr7ikere+yHduu62y//y3NWG38xIOpeODyXcoE8OohGYZ5VhhHHjl83sD4B3XgyGI=)

[Try it in the Playground](https://play.vuejs.org/#eNp9kU9PhDAUxL/KpBfWBCH+OZEuid5N9qSHrQezFKhC27RlDSF8d1tYQBP1+N78OpN5HciD1sm54yQj1J6M0A6Wu07nTIpWK+MwwPASI0qjWkQejVbpsVHVQVl30ZJ0WQRHjwFMnpT0gPZLi32w2h2DMEAUGW5iOOEaniF66vGuOiN5j0/hajx7B4zxxt5ubIiphKz+IO828qXugw5hYRXKTnqSydcrJmk61/VF/eB4q5s3x8Pk6FJjauDO16Uye0ZCBwg5d2EkkED2wfuLlogibMOTbMpf9tMwP8jpeiMfRdM1l8Tk+/F++Y6Cl0Lyg1Ha7o7R5Bn9WwSg9X0+DPMxMI409fPP1PELlVmwdQ==)

Notice how [v-bindsyntax](https://vuejs.org/api/built-in-directives#v-bind) (`:title="post.title"`) is used to pass dynamic prop values. This is especially useful when you don't know the exact content you're going to render ahead of time.

That's all you need to know about props for now, but once you've finished reading this page and feel comfortable with its content, we recommend coming back later to read the full guide on [Props](https://vuejs.org/guide/components/props).

## Listening to Events​

As we develop our `<BlogPost>` component, some features may require communicating back up to the parent. For example, we may decide to include an accessibility feature to enlarge the text of blog posts, while leaving the rest of the page at its default size.

In the parent, we can support this feature by adding a `postFontSize` data propertyref:

js

```
data() {
  return {
    posts: [
      /* ... */
    ],
    postFontSize: 1
  }
}
```

js

```
const posts = ref([
  /* ... */
])

const postFontSize = ref(1)
```

Which can be used in the template to control the font size of all blog posts:

template

```
<div :style="{ fontSize: postFontSize + 'em' }">
  <BlogPost
    v-for="post in posts"
    :key="post.id"
    :title="post.title"
   />
</div>
```

Now let's add a button to the `<BlogPost>` component's template:

BlogPost.vuevue

```

<template>
  <div class="blog-post">
    <h4>{{ title }}</h4>
    <button>Enlarge text</button>
  </div>
</template>
```

The button doesn't do anything yet - we want clicking the button to communicate to the parent that it should enlarge the text of all posts. To solve this problem, components provide a custom events system. The parent can choose to listen to any event on the child component instance with `v-on` or `@`, just as we would with a native DOM event:

template

```
<BlogPost
  ...
  @enlarge-text="postFontSize += 0.1"
 />
```

Then the child component can emit an event on itself by calling the built-in [$emitmethod](https://vuejs.org/api/component-instance#emit), passing the name of the event:

BlogPost.vuevue

```

<template>
  <div class="blog-post">
    <h4>{{ title }}</h4>
    <button @click="$emit('enlarge-text')">Enlarge text</button>
  </div>
</template>
```

Thanks to the `@enlarge-text="postFontSize += 0.1"` listener, the parent will receive the event and update the value of `postFontSize`.

[Try it in the Playground](https://play.vuejs.org/#eNqNUsFOg0AQ/ZUJMaGNbbHqidCmmujNxMRED9IDhYWuhV0CQy0S/t1ZYIEmaiRkw8y8N/vmMZVxl6aLY8EM23ByP+Mprl3Bk1RmCPexjJ5ljhBmMgFzYemEIpiuAHAFOzXQgIVeESNUKutL4gsmMLfbBPStVFTP1Bl46E2mup4xLDKhI4CUsMR+1zFABTywYTkD5BgzG8ynEj4kkVgJnxz38Eqaut5jxvXAUCIiLqI/8TcD/m1fKhTwHHIJYSEIr+HbnqikPkqBL/yLSMs23eDooNexel8pQJaksYeMIgAn4EewcyxjtnKNCsK+zbgpXILJEnW30bCIN7ZTPcd5KDNqoWjARWufa+iyfWBlV13wYJRvJtWVJhiKGyZiL4vYHNkJO8wgaQVXi6UGr51+Ndq5LBqMvhyrH9eYGePtOVu3n3YozWSqFsBsVJmt3SzhzVaYY2nm9l82+7GX5zTGjlTM1SyNmy5SeX+7rqr2r0NdOxbFXWVXIEoBGz/m/oHIF0rB5Pz6KTV6aBOgEo7Vsn51ov4GgAAf2A==)

[Try it in the Playground](https://play.vuejs.org/#eNp1Uk1PwkAQ/SuTxqQYgYp6ahaiJngzITHRA/UAZQor7W7TnaK16X93th8UEuHEvPdm5s3bls5Tmo4POTq+I0yYyZTAIOXpLFAySXVGUEKGEVQQZToBl6XukXqO9XahDbXc2OsAO5FlAIEKtWJByqCBqR01WFqiBLnxYTIEkhSjD+5rAV86zxQW8C1pB+88Aaphr73rtXbNVqrtBeV9r/zYFZYHacBoiHLFykB9Xgfq1NmLVvQmf7E1OGFaeE0anAMXhEkarwhtRWIjD+AbKmKcBk4JUdvtn8+6ARcTu87hLuCf6NJpSoDDKNIZj7BtIFUTUuB0tL/HomXHcnOC18d1TF305COqeJVtcUT4Q62mtzSF2/GkE8/E8b1qh8Ljw/if8I7nOkPn9En/+Ug2GEmFi0ynZrB0azOujbfB54kki5+aqumL8bING28Yr4xh+2vePrI39CnuHmZl2TwwVJXwuG6ZdU6kFTyGsQz33HyFvH5wvvyaB80bACwgvKbrYgLVH979DQc=)

We can optionally declare emitted events using the [emits](https://vuejs.org/api/options-state#emits) option[defineEmits](https://vuejs.org/api/sfc-script-setup#defineprops-defineemits) macro:

BlogPost.vuevue

```
<script>
export default {
  props: ['title'],
  emits: ['enlarge-text']
}
</script>
```

BlogPost.vuevue

```
<script setup>
defineProps(['title'])
defineEmits(['enlarge-text'])
</script>
```

This documents all the events that a component emits and optionally [validates them](https://vuejs.org/guide/components/events#events-validation). It also allows Vue to avoid implicitly applying them as native listeners to the child component's root element.

Similar to `defineProps`, `defineEmits` is only usable in `<script setup>` and doesn't need to be imported. It returns an `emit` function that is equivalent to the `$emit` method. It can be used to emit events in the `<script setup>` section of a component, where `$emit` isn't directly accessible:

vue

```
<script setup>
const emit = defineEmits(['enlarge-text'])

emit('enlarge-text')
</script>
```

See also: [Typing Component Emits](https://vuejs.org/guide/typescript/composition-api#typing-component-emits)

If you are not using `<script setup>`, you can declare emitted events using the `emits` option. You can access the `emit` function as a property of the setup context (passed to `setup()` as the second argument):

js

```
export default {
  emits: ['enlarge-text'],
  setup(props, ctx) {
    ctx.emit('enlarge-text')
  }
}
```

That's all you need to know about custom component events for now, but once you've finished reading this page and feel comfortable with its content, we recommend coming back later to read the full guide on [Custom Events](https://vuejs.org/guide/components/events).

## Content Distribution with Slots​

Just like with HTML elements, it's often useful to be able to pass content to a component, like this:

template

```
<AlertBox>
  Something bad happened.
</AlertBox>
```

Which might render something like:

This is an Error for Demo Purposes

Something bad happened.

This can be achieved using Vue's custom `<slot>` element:

AlertBox.vuevue

```
<template>
  <div class="alert-box">
    <strong>This is an Error for Demo Purposes</strong>
    <slot />
  </div>
</template>

<style scoped>
.alert-box {
  /* ... */
}
</style>
```

As you'll see above, we use the `<slot>` as a placeholder where we want the content to go – and that's it. We're done!

[Try it in the Playground](https://play.vuejs.org/#eNpVUcFOwzAM/RUTDruwFhCaUCmThsQXcO0lbbKtIo0jx52Kpv07TreWouTynl+en52z2oWQnXqrClXGhtrA28q3XUBi2DlL/IED7Ak7WGX5RKQHq8oDVN4Oo9TYve4dwzmxDcp7bz3HAs5/LpfKyy3zuY0Atl1wmm1CXE5SQeLNX9hZPrb+ALU2cNQhWG9NNkrnLKIt89lGPahlyDTVogVAadoTNE7H+F4pnZTrGodKjUUpRyb0h+0nEdKdRL3CW7GmfNY5ZLiiMhfP/ynG0SL/OAuxwWCNMNncbVqSQyrgfrPZvCVcIxkrxFMYIKJrDZA1i8qatGl72ehLGEY6aGNkNwU8P96YWjffB8Lem/Xkvn9NR6qy+fRd14FSgopvmtQmzTT9Toq9VZdfIpa5jQ==)

[Try it in the Playground](https://play.vuejs.org/#eNpVUEtOwzAQvcpgFt3QBBCqUAiRisQJ2GbjxG4a4Xis8aQKqnp37PyUyqv3mZn3fBVH55JLr0Umcl9T6xi85t4VpW07h8RwNJr4Cwc4EXawS9KFiGO70ubpNBcmAmDdOSNZR8T5Yg0IoOQf7DSfW9tAJRWcpXPaapWM1nVt8ObpukY8ie29GHNzAiBX7QVqI73/LIWMzn2FQylGMcieCW1TfBMhPYSoE5zFitLVZ5BhQnkadt6nGKt5/jMafI1Oq8Ak6zW4xrEaDVIGj4fD4SPiCknpQLy4ATyaVgFptVH2JFXb+wze3DDSTioV/iaD1+eZqWT92xD2Vu2X7af3+IJ6G7/UToVigpJnTzwTO42eWDnELsTtH/wUqH4=)

That's all you need to know about slots for now, but once you've finished reading this page and feel comfortable with its content, we recommend coming back later to read the full guide on [Slots](https://vuejs.org/guide/components/slots).

## Dynamic Components​

Sometimes, it's useful to dynamically switch between components, like in a tabbed interface:

[Open example in the Playground](https://play.vuejs.org/#eNqNVE2PmzAQ/Ssj9kArLSHbrXpwk1X31mMPvS17cIxJrICNbJMmivLfO/7AEG2jRiDkefP85sNmztlr3y8OA89ItjJMi96+VFJ0vdIWfqqOQ6NVB/midIYj5sn9Sxlrkt9b14RXzXbiMElEO5IAKsmPnljzhg6thbNDmcLdkktrSADAJ/IYlj5MXEc9Z1w8VFNLP30ed2luBy1HC4UHrVH2N90QyJ1kHnUALN1gtLeIQu6juEUMkb8H5sXHqiS+qzK1Cw3Lu76llqMFsKrFAVhLjVlXWc07VWUeR89msFbhhhAWDkWjNJIwPgjp06iy5CV7fgrOOTgKv+XoKIIgpnoGyiymSmZ1wnq9dqJweZ8p/GCtYHtUmBMdLXFitgDnc9ju68b0yxDO1WzRTEcFRLiUJsEqSw3wwi+rMpFDj0psEq5W5ax1aBp7at1y4foWzq5R0hYN7UR7ImCoNIXhWjTfnW+jdM01gaf+CEa1ooYHzvnMVWhaiwEP90t/9HBP61rILQJL3POMHw93VG+FLKzqUYx3c2yjsOaOwNeRO2B8zKHlzBKQWJNH1YHrplV/iiMBOliFILYNK5mOKdSTMviGCTyNojFdTKBoeWNT3s8f/Vpsd7cIV61gjHkXnotR6OqVkJbrQKdsv9VqkDWBh2bpnn8VXaDcHPexE4wFzsojO9eDUOSVPF+65wN/EW7sHRsi5XaFqaexn+EH9Xcpe8zG2eWG3O0/NVzUaeJMk+jGhUXlNPXulw5j8w7t2bi8X32cuf/Vv/wF/SL98A==)

[Open example in the Playground](https://play.vuejs.org/#eNqNVMGOmzAQ/ZURe2BXCiHbrXpwk1X31mMPvS1V5RiTWAEb2SZNhPLvHdvggLZRE6TIM/P8/N5gpk/e2nZ57HhCkrVhWrQWDLdd+1pI0bRKW/iuGg6VVg2ky9wFDp7G8g9lrIl1H80Bb5rtxfFKMcRzUA+aV3AZQKEEhWRKGgus05pL+5NuYeNwj6mTkT4VckRYujVY63GT17twC6/Fr4YjC3kp5DoPNtEgBpY3bU0txwhgXYojsJoasymSkjeqSHweK9vOWoUbXIC/Y1YpjaDH3wt39hMI6TUUSYSQAz8jArPT5Mj+nmIhC6zpAu1TZlEhmXndbBwpXH5NGL6xWrADMsyaMj1lkAzQ92E7mvYe8nCcM24xZApbL5ECiHCSnP73KyseGnvh6V/XedwS2pVjv3C1ziddxNDYc+2WS9fC8E4qJW1W0UbUZwKGSpMZrkX11dW2SpdcE3huT2BULUp44JxPSpmmpegMgU/tyadbWpZC7jCxwj0v+OfTDdU7ITOrWiTjzTS3Vei8IfB5xHZ4PmqoObMEJHryWXXkuqrVn+xEgHZWYRKbh06uLyv4iQq+oIDnkXSQiwKymlc26n75WNdit78FmLWCMeZL+GKMwlKrhLRcBzhlh51WnSwJPFQr9/zLdIZ007w/O6bR4MQe2bseBJMzer5yzwf8MtzbOzYMkNsOY0+HfoZv1d+lZJGMg8fNqdsfbbio4b77uRVv7I0Li8xxZN1PHWbeHdyTWXc/+zgw/8t/+QsROe9h)

The above is made possible by Vue's `<component>` element with the special `is` attribute:

template

```

<component :is="currentTab"></component>
```

template

```

<component :is="tabs[currentTab]"></component>
```

In the example above, the value passed to `:is` can contain either:

- the name string of a registered component, OR
- the actual imported component object

You can also use the `is` attribute to create regular HTML elements.

When switching between multiple components with `<component :is="...">`, a component will be unmounted when it is switched away from. We can force the inactive components to stay "alive" with the built-in [<KeepAlive>component](https://vuejs.org/guide/built-ins/keep-alive).

## in-DOM Template Parsing Caveats​

If you are writing your Vue templates directly in the DOM, Vue will have to retrieve the template string from the DOM. This leads to some caveats due to browsers' native HTML parsing behavior.

TIP

It should be noted that the limitations discussed below only apply if you are writing your templates directly in the DOM. They do NOT apply if you are using string templates from the following sources:

- Single-File Components
- Inlined template strings (e.g. `template: '...'`)
- `<script type="text/x-template">`

### Case Insensitivity​

HTML tags and attribute names are case-insensitive, so browsers will interpret any uppercase characters as lowercase. That means when you’re using in-DOM templates, PascalCase component names and camelCased prop names or `v-on` event names all need to use their kebab-cased (hyphen-delimited) equivalents:

js

```
// camelCase in JavaScript
const BlogPost = {
  props: ['postTitle'],
  emits: ['updatePost'],
  template: `
    <h3>{{ postTitle }}</h3>
  `
}
```

template

```

<blog-post post-title="hello!" @update-post="onUpdatePost"></blog-post>
```

### Self Closing Tags​

We have been using self-closing tags for components in previous code samples:

template

```
<MyComponent />
```

This is because Vue's template parser respects `/>` as an indication to end any tag, regardless of its type.

In in-DOM templates, however, we must always include explicit closing tags:

template

```
<my-component></my-component>
```

This is because the HTML spec only allows [a few specific elements](https://html.spec.whatwg.org/multipage/syntax.html#void-elements) to omit closing tags, the most common being `<input>` and `<img>`. For all other elements, if you omit the closing tag, the native HTML parser will think you never terminated the opening tag. For example, the following snippet:

template

```
<my-component /> 
<span>hello</span>
```

will be parsed as:

template

```
<my-component>
  <span>hello</span>
</my-component> 
```

### Element Placement Restrictions​

Some HTML elements, such as `<ul>`, `<ol>`, `<table>` and `<select>` have restrictions on what elements can appear inside them, and some elements such as `<li>`, `<tr>`, and `<option>` can only appear inside certain other elements.

This will lead to issues when using components with elements that have such restrictions. For example:

template

```
<table>
  <blog-post-row></blog-post-row>
</table>
```

The custom component `<blog-post-row>` will be hoisted out as invalid content, causing errors in the eventual rendered output. We can use the special [isattribute](https://vuejs.org/api/built-in-special-attributes#is) as a workaround:

template

```
<table>
  <tr is="vue:blog-post-row"></tr>
</table>
```

TIP

When used on native HTML elements, the value of `is` must be prefixed with `vue:` in order to be interpreted as a Vue component. This is required to avoid confusion with native [customized built-in elements](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-elements-customized-builtin-example).

That's all you need to know about in-DOM template parsing caveats for now - and actually, the end of Vue's *Essentials*. Congratulations! There's still more to learn, but first, we recommend taking a break to play with Vue yourself - build something fun, or check out some of the [Examples](https://vuejs.org/examples/) if you haven't already.

Once you feel comfortable with the knowledge you've just digested, move on with the guide to learn more about components in depth.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/component-basics.md)

---

# Computed Properties​

> Vue.js - The Progressive JavaScript Framework

# Computed Properties​

[Watch a free video lesson on Vue School](https://vueschool.io/lessons/computed-properties-in-vue-3?friend=vuejs)[Watch a free video lesson on Vue School](https://vueschool.io/lessons/vue-fundamentals-capi-computed-properties-in-vue-with-the-composition-api?friend=vuejs)

## Basic Example​

In-template expressions are very convenient, but they are meant for simple operations. Putting too much logic in your templates can make them bloated and hard to maintain. For example, if we have an object with a nested array:

js

```
export default {
  data() {
    return {
      author: {
        name: 'John Doe',
        books: [
          'Vue 2 - Advanced Guide',
          'Vue 3 - Basic Guide',
          'Vue 4 - The Mystery'
        ]
      }
    }
  }
}
```

js

```
const author = reactive({
  name: 'John Doe',
  books: [
    'Vue 2 - Advanced Guide',
    'Vue 3 - Basic Guide',
    'Vue 4 - The Mystery'
  ]
})
```

And we want to display different messages depending on if `author` already has some books or not:

template

```
<p>Has published books:</p>
<span>{{ author.books.length > 0 ? 'Yes' : 'No' }}</span>
```

At this point, the template is getting a bit cluttered. We have to look at it for a second before realizing that it performs a calculation depending on `author.books`. More importantly, we probably don't want to repeat ourselves if we need to include this calculation in the template more than once.

That's why for complex logic that includes reactive data, it is recommended to use a **computed property**. Here's the same example, refactored:

js

```
export default {
  data() {
    return {
      author: {
        name: 'John Doe',
        books: [
          'Vue 2 - Advanced Guide',
          'Vue 3 - Basic Guide',
          'Vue 4 - The Mystery'
        ]
      }
    }
  },
  computed: {
    // a computed getter
    publishedBooksMessage() {
      // `this` points to the component instance
      return this.author.books.length > 0 ? 'Yes' : 'No'
    }
  }
}
```

template

```
<p>Has published books:</p>
<span>{{ publishedBooksMessage }}</span>
```

[Try it in the Playground](https://play.vuejs.org/#eNqFkN1KxDAQhV/l0JsqaFfUq1IquwiKsF6JINaLbDNui20S8rO4lL676c82eCFCIDOZMzkzXxetlUoOjqI0ykypa2XzQtC3ktqC0ydzjUVXCIAzy87OpxjQZJ0WpwxgzlZSp+EBEKylFPGTrATuJcUXobST8sukeA8vQPzqCNe4xJofmCiJ48HV/FfbLLrxog0zdfmn4tYrXirC9mgs6WMcBB+nsJ+C8erHH0rZKmeJL0sot2tqUxHfDONuyRi2p4BggWCr2iQTgGTcLGlI7G2FHFe4Q/xGJoYn8SznQSbTQviTrRboPrHUqoZZ8hmQqfyRmTDFTC1bqalsFBN5183o/3NG33uvoWUwXYyi/gdTEpwK)

Here we have declared a computed property `publishedBooksMessage`.

Try to change the value of the `books` array in the application `data` and you will see how `publishedBooksMessage` is changing accordingly.

You can data-bind to computed properties in templates just like a normal property. Vue is aware that `this.publishedBooksMessage` depends on `this.author.books`, so it will update any bindings that depend on `this.publishedBooksMessage` when `this.author.books` changes.

See also: [Typing Computed Properties](https://vuejs.org/guide/typescript/options-api#typing-computed-properties)

vue

```
<script setup>
import { reactive, computed } from 'vue'

const author = reactive({
  name: 'John Doe',
  books: [
    'Vue 2 - Advanced Guide',
    'Vue 3 - Basic Guide',
    'Vue 4 - The Mystery'
  ]
})

// a computed ref
const publishedBooksMessage = computed(() => {
  return author.books.length > 0 ? 'Yes' : 'No'
})
</script>

<template>
  <p>Has published books:</p>
  <span>{{ publishedBooksMessage }}</span>
</template>
```

[Try it in the Playground](https://play.vuejs.org/#eNp1kE9Lw0AQxb/KI5dtoTainkoaaREUoZ5EEONhm0ybYLO77J9CCfnuzta0vdjbzr6Zeb95XbIwZroPlMySzJW2MR6OfDB5oZrWaOvRwZIsfbOnCUrdmuCpQo+N1S0ET4pCFarUynnI4GttMT9PjLpCAUq2NIN41bXCkyYxiZ9rrX/cDF/xDYiPQLjDDRbVXqqSHZ5DUw2tg3zP8lK6pvxHe2DtvSasDs6TPTAT8F2ofhzh0hTygm5pc+I1Yb1rXE3VMsKsyDm5JcY/9Y5GY8xzHI+wnIpVw4nTI/10R2rra+S4xSPEJzkBvvNNs310ztK/RDlLLjy1Zic9cQVkJn+R7gIwxJGlMXiWnZEq77orhH3Pq2NH9DjvTfpfSBSbmA==)

Here we have declared a computed property `publishedBooksMessage`. The `computed()` function expects to be passed a [getter function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get#description), and the returned value is a **computed ref**. Similar to normal refs, you can access the computed result as `publishedBooksMessage.value`. Computed refs are also auto-unwrapped in templates so you can reference them without `.value` in template expressions.

A computed property automatically tracks its reactive dependencies. Vue is aware that the computation of `publishedBooksMessage` depends on `author.books`, so it will update any bindings that depend on `publishedBooksMessage` when `author.books` changes.

See also: [Typing Computed](https://vuejs.org/guide/typescript/composition-api#typing-computed)

## Computed Caching vs. Methods​

You may have noticed we can achieve the same result by invoking a method in the expression:

template

```
<p>{{ calculateBooksMessage() }}</p>
```

js

```
// in component
methods: {
  calculateBooksMessage() {
    return this.author.books.length > 0 ? 'Yes' : 'No'
  }
}
```

js

```
// in component
function calculateBooksMessage() {
  return author.books.length > 0 ? 'Yes' : 'No'
}
```

Instead of a computed property, we can define the same function as a method. For the end result, the two approaches are indeed exactly the same. However, the difference is that **computed properties are cached based on their reactive dependencies.** A computed property will only re-evaluate when some of its reactive dependencies have changed. This means as long as `author.books` has not changed, multiple access to `publishedBooksMessage` will immediately return the previously computed result without having to run the getter function again.

This also means the following computed property will never update, because `Date.now()` is not a reactive dependency:

js

```
computed: {
  now() {
    return Date.now()
  }
}
```

js

```
const now = computed(() => Date.now())
```

In comparison, a method invocation will **always** run the function whenever a re-render happens.

Why do we need caching? Imagine we have an expensive computed property `list`, which requires looping through a huge array and doing a lot of computations. Then we may have other computed properties that in turn depend on `list`. Without caching, we would be executing `list`’s getter many more times than necessary! In cases where you do not want caching, use a method call instead.

## Writable Computed​

Computed properties are by default getter-only. If you attempt to assign a new value to a computed property, you will receive a runtime warning. In the rare cases where you need a "writable" computed property, you can create one by providing both a getter and a setter:

js

```
export default {
  data() {
    return {
      firstName: 'John',
      lastName: 'Doe'
    }
  },
  computed: {
    fullName: {
      // getter
      get() {
        return this.firstName + ' ' + this.lastName
      },
      // setter
      set(newValue) {
        // Note: we are using destructuring assignment syntax here.
        [this.firstName, this.lastName] = newValue.split(' ')
      }
    }
  }
}
```

Now when you run `this.fullName = 'John Doe'`, the setter will be invoked and `this.firstName` and `this.lastName` will be updated accordingly.

vue

```
<script setup>
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

const fullName = computed({
  // getter
  get() {
    return firstName.value + ' ' + lastName.value
  },
  // setter
  set(newValue) {
    // Note: we are using destructuring assignment syntax here.
    [firstName.value, lastName.value] = newValue.split(' ')
  }
})
</script>
```

Now when you run `fullName.value = 'John Doe'`, the setter will be invoked and `firstName` and `lastName` will be updated accordingly.

## Getting the Previous Value​

- Only supported in 3.4+

In case you need it, you can get the previous value returned by the computed property accessing the second argument of the getter:

In case you need it, you can get the previous value returned by the computed property accessing the first argument of the getter:

js

```
export default {
  data() {
    return {
      count: 2
    }
  },
  computed: {
    // This computed will return the value of count when it's less or equal to 3.
    // When count is >=4, the last value that fulfilled our condition will be returned
    // instead until count is less or equal to 3
    alwaysSmall(_, previous) {
      if (this.count <= 3) {
        return this.count
      }

      return previous
    }
  }
}
```

vue

```
<script setup>
import { ref, computed } from 'vue'

const count = ref(2)

// This computed will return the value of count when it's less or equal to 3.
// When count is >=4, the last value that fulfilled our condition will be returned
// instead until count is less or equal to 3
const alwaysSmall = computed((previous) => {
  if (count.value <= 3) {
    return count.value
  }

  return previous
})
</script>
```

In case you're using a writable computed:

js

```
export default {
  data() {
    return {
      count: 2
    }
  },
  computed: {
    alwaysSmall: {
      get(_, previous) {
        if (this.count <= 3) {
          return this.count
        }

        return previous;
      },
      set(newValue) {
        this.count = newValue * 2
      }
    }
  }
}
```

vue

```
<script setup>
import { ref, computed } from 'vue'

const count = ref(2)

const alwaysSmall = computed({
  get(previous) {
    if (count.value <= 3) {
      return count.value
    }

    return previous
  },
  set(newValue) {
    count.value = newValue * 2
  }
})
</script>
```

## Best Practices​

### Getters should be side-effect free​

It is important to remember that computed getter functions should only perform pure computation and be free of side effects. For example, **don't mutate other state, make async requests, or mutate the DOM inside a computed getter!** Think of a computed property as declaratively describing how to derive a value based on other values - its only responsibility should be computing and returning that value. Later in the guide we will discuss how we can perform side effects in reaction to state changes with [watchers](https://vuejs.org/guide/essentials/watchers).

### Avoid mutating computed value​

The returned value from a computed property is derived state. Think of it as a temporary snapshot - every time the source state changes, a new snapshot is created. It does not make sense to mutate a snapshot, so a computed return value should be treated as read-only and never be mutated - instead, update the source state it depends on to trigger new computations.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/essentials/computed.md)
