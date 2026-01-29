# Accessibility​ and more

# Accessibility​

> Vue.js - The Progressive JavaScript Framework

# Accessibility​

Web accessibility (also known as a11y) refers to the practice of creating websites that can be used by anyone — be that a person with a disability, a slow connection, outdated or broken hardware or simply someone in an unfavorable environment. For example, adding subtitles to a video would help both your deaf and hard-of-hearing users and your users who are in a loud environment and can't hear their phone. Similarly, making sure your text isn't too low contrast will help both your low-vision users and your users who are trying to use their phone in bright sunlight.

Ready to start but aren’t sure where?

Checkout the [Planning and managing web accessibility guide](https://www.w3.org/WAI/planning-and-managing/) provided by [World Wide Web Consortium (W3C)](https://www.w3.org/)

## Skip link​

You should add a link at the top of each page that goes directly to the main content area so users can skip content that is repeated on multiple Web pages.

Typically this is done on the top of `App.vue` as it will be the first focusable element on all your pages:

template

```
<span ref="backToTop" tabindex="-1" />
<ul class="skip-links">
  <li>
    <a href="#main" ref="skipLink" class="skip-link">Skip to main content</a>
  </li>
</ul>
```

To hide the link unless it is focused, you can add the following style:

css

```
.skip-links {
  list-style: none;
}
.skip-link {
  white-space: nowrap;
  margin: 1em auto;
  top: 0;
  position: fixed;
  left: 50%;
  margin-left: -72px;
  opacity: 0;
}
.skip-link:focus {
  opacity: 1;
  background-color: white;
  padding: 0.5em;
  border: 1px solid black;
}
```

Once a user changes route, bring focus back to the very beginning of the page, right before the skip link. This can be achieved by calling focus on the `backToTop` template ref (assuming usage of `vue-router`):

vue

```
<script>
export default {
  watch: {
    $route() {
      this.$refs.backToTop.focus()
    }
  }
}
</script>
```

vue

```
<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const backToTop = ref()

watch(
  () => route.path,
  () => {
    backToTop.value.focus()
  }
)
</script>
```

[Read documentation on skip link to main content](https://www.w3.org/WAI/WCAG21/Techniques/general/G1.html)

## Content Structure​

One of the most important pieces of accessibility is making sure that design can support accessible implementation. Design should consider not only color contrast, font selection, text sizing, and language, but also how the content is structured in the application.

### Headings​

Users can navigate an application through headings. Having descriptive headings for every section of your application makes it easier for users to predict the content of each section. When it comes to headings, there are a couple of recommended accessibility practices:

- Nest headings in their ranking order: `<h1>` - `<h6>`
- Don’t skip headings within a section
- Use actual heading tags instead of styling text to give the visual appearance of headings

[Read more about headings](https://www.w3.org/TR/UNDERSTANDING-WCAG20/navigation-mechanisms-descriptive.html)

template

```
<main role="main" aria-labelledby="main-title">
  <h1 id="main-title">Main title</h1>
  <section aria-labelledby="section-title-1">
    <h2 id="section-title-1"> Section Title </h2>
    <h3>Section Subtitle</h3>
    
  </section>
  <section aria-labelledby="section-title-2">
    <h2 id="section-title-2"> Section Title </h2>
    <h3>Section Subtitle</h3>
    
    <h3>Section Subtitle</h3>
    
  </section>
</main>
```

### Landmarks​

[Landmarks](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/landmark_role) provide programmatic access to sections within an application. Users who rely on assistive technology can navigate to each section of the application and skip over content. You can use [ARIA roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles) to help you achieve this.

| HTML | ARIA Role | Landmark Purpose |
| --- | --- | --- |
| header | role="banner" | Prime heading: title of the page |
| nav | role="navigation" | Collection of links suitable for use when navigating the document or related documents |
| main | role="main" | The main or central content of the document. |
| footer | role="contentinfo" | Information about the parent document: footnotes/copyrights/links to privacy statement |
| aside | role="complementary" | Supports the main content, yet is separated and meaningful on its own content |
| search | role="search" | This section contains the search functionality for the application |
| form | role="form" | Collection of form-associated elements |
| section | role="region" | Content that is relevant and that users will likely want to navigate to. Label must be provided for this element |

[Read more about landmarks](https://www.w3.org/TR/wai-aria-1.2/#landmark_roles)

## Semantic Forms​

When creating a form, you can use the following elements: `<form>`, `<label>`, `<input>`, `<textarea>`, and `<button>`

Labels are typically placed on top or to the left of the form fields:

template

```
<form action="/dataCollectionLocation" method="post" autocomplete="on">
  <div v-for="item in formItems" :key="item.id" class="form-item">
    <label :for="item.id">{{ item.label }}: </label>
    <input
      :type="item.type"
      :id="item.id"
      :name="item.id"
      v-model="item.value"
    />
  </div>
  <button type="submit">Submit</button>
</form>
```

Notice how you can include `autocomplete='on'` on the form element and it will apply to all inputs in your form. You can also set different [values for autocomplete attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for each input.

### Labels​

Provide labels to describe the purpose of all form control; linking `for` and `id`:

template

```
<label for="name">Name: </label>
<input type="text" name="name" id="name" v-model="name" />
```

If you inspect this element in your Chrome DevTools and open the Accessibility tab inside the Elements tab, you will see how the input gets its name from the label:

![Chrome Developer Tools showing input accessible name from label](https://vuejs.org/assets/AccessibleLabelChromeDevTools.Cd99Z50e.png)

Warning:

Though you might have seen labels wrapping the input fields like this:

template

```
<label>
  Name:
  <input type="text" name="name" id="name" v-model="name" />
</label>
```

Explicitly setting the labels with a matching id is better supported by assistive technology.

#### aria-label​

You can also give the input an accessible name with [aria-label](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label).

template

```
<label for="name">Name: </label>
<input
  type="text"
  name="name"
  id="name"
  v-model="name"
  :aria-label="nameLabel"
/>
```

Feel free to inspect this element in Chrome DevTools to see how the accessible name has changed:

![Chrome Developer Tools showing input accessible name from aria-label](https://vuejs.org/assets/AccessibleARIAlabelDevTools.CLDgc87f.png)

#### aria-labelledby​

Using [aria-labelledby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-labelledby) is similar to `aria-label` except it is used if the label text is visible on screen. It is paired to other elements by their `id` and you can link multiple `id`s:

template

```
<form
  class="demo"
  action="/dataCollectionLocation"
  method="post"
  autocomplete="on"
>
  <h1 id="billing">Billing</h1>
  <div class="form-item">
    <label for="name">Name: </label>
    <input
      type="text"
      name="name"
      id="name"
      v-model="name"
      aria-labelledby="billing name"
    />
  </div>
  <button type="submit">Submit</button>
</form>
```

![Chrome Developer Tools showing input accessible name from aria-labelledby](https://vuejs.org/assets/AccessibleARIAlabelledbyDevTools.D7s7v8qX.png)

#### aria-describedby​

[aria-describedby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-describedby) is used the same way as `aria-labelledby` except provides a description with additional information that the user might need. This can be used to describe the criteria for any input:

template

```
<form
  class="demo"
  action="/dataCollectionLocation"
  method="post"
  autocomplete="on"
>
  <h1 id="billing">Billing</h1>
  <div class="form-item">
    <label for="name">Full Name: </label>
    <input
      type="text"
      name="name"
      id="name"
      v-model="name"
      aria-labelledby="billing name"
      aria-describedby="nameDescription"
    />
    <p id="nameDescription">Please provide first and last name.</p>
  </div>
  <button type="submit">Submit</button>
</form>
```

You can see the description by inspecting Chrome DevTools:

![Chrome Developer Tools showing input accessible name from aria-labelledby and description with aria-describedby](https://vuejs.org/assets/AccessibleARIAdescribedby.B-uvz_GC.png)

### Placeholder​

Avoid using placeholders as they can confuse many users.

One of the issues with placeholders is that they don't meet the [color contrast criteria](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) by default; fixing the color contrast makes the placeholder look like pre-populated data in the input fields. Looking at the following example, you can see that the Last Name placeholder which meets the color contrast criteria looks like pre-populated data:

![Accessible placeholder](https://vuejs.org/assets/AccessiblePlaceholder.IvJOiQV8.png)

template

```
<form
  class="demo"
  action="/dataCollectionLocation"
  method="post"
  autocomplete="on"
>
  <div v-for="item in formItems" :key="item.id" class="form-item">
    <label :for="item.id">{{ item.label }}: </label>
    <input
      type="text"
      :id="item.id"
      :name="item.id"
      v-model="item.value"
      :placeholder="item.placeholder"
    />
  </div>
  <button type="submit">Submit</button>
</form>
```

css

```
/* https://www.w3schools.com/howto/howto_css_placeholder.asp */

#lastName::placeholder {
  /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: black;
  opacity: 1; /* Firefox */
}

#lastName:-ms-input-placeholder {
  /* Internet Explorer 10-11 */
  color: black;
}

#lastName::-ms-input-placeholder {
  /* Microsoft Edge */
  color: black;
}
```

It is best to provide all the information the user needs to fill out forms outside any inputs.

### Instructions​

When adding instructions for your input fields, make sure to link it correctly to the input. You can provide additional instructions and bind multiple ids inside an [aria-labelledby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-labelledby). This allows for more flexible design.

template

```
<fieldset>
  <legend>Using aria-labelledby</legend>
  <label id="date-label" for="date">Current Date: </label>
  <input
    type="date"
    name="date"
    id="date"
    aria-labelledby="date-label date-instructions"
  />
  <p id="date-instructions">MM/DD/YYYY</p>
</fieldset>
```

Alternatively, you can attach the instructions to the input with [aria-describedby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-describedby):

template

```
<fieldset>
  <legend>Using aria-describedby</legend>
  <label id="dob" for="dob">Date of Birth: </label>
  <input type="date" name="dob" id="dob" aria-describedby="dob-instructions" />
  <p id="dob-instructions">MM/DD/YYYY</p>
</fieldset>
```

### Hiding Content​

Usually it is not recommended to visually hide labels, even if the input has an accessible name. However, if the functionality of the input can be understood with surrounding content, then we can hide the visual label.

Let's look at this search field:

template

```
<form role="search">
  <label for="search" class="hidden-visually">Search: </label>
  <input type="text" name="search" id="search" v-model="search" />
  <button type="submit">Search</button>
</form>
```

We can do this because the search button will help visual users identify the purpose of the input field.

We can use CSS to visually hide elements but keep them available for assistive technology:

css

```
.hidden-visually {
  position: absolute;
  overflow: hidden;
  white-space: nowrap;
  margin: 0;
  padding: 0;
  height: 1px;
  width: 1px;
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
}
```

#### aria-hidden="true"​

Adding `aria-hidden="true"` will hide the element from assistive technology but leave it visually available for other users. Do not use it on focusable elements, purely on decorative, duplicated or offscreen content.

template

```
<p>This is not hidden from screen readers.</p>
<p aria-hidden="true">This is hidden from screen readers.</p>
```

### Buttons​

When using buttons inside a form, you must set the type to prevent submitting the form. You can also use an input to create buttons:

template

```
<form action="/dataCollectionLocation" method="post" autocomplete="on">
  
  <button type="button">Cancel</button>
  <button type="submit">Submit</button>

  
  <input type="button" value="Cancel" />
  <input type="submit" value="Submit" />
</form>
```

### Functional Images​

You can use this technique to create functional images.

- Input fields
  - These images will act as a submit type button on forms
  template
  ```
  <form role="search">
    <label for="search" class="hidden-visually">Search: </label>
    <input type="text" name="search" id="search" v-model="search" />
    <input
      type="image"
      class="btnImg"
      src="https://img.icons8.com/search"
      alt="Search"
    />
  </form>
  ```
- Icons

template

```
<form role="search">
  <label for="searchIcon" class="hidden-visually">Search: </label>
  <input type="text" name="searchIcon" id="searchIcon" v-model="searchIcon" />
  <button type="submit">
    <i class="fas fa-search" aria-hidden="true"></i>
    <span class="hidden-visually">Search</span>
  </button>
</form>
```

## Standards​

The World Wide Web Consortium (W3C) Web Accessibility Initiative (WAI) develops web accessibility standards for the different components:

- [User Agent Accessibility Guidelines (UAAG)](https://www.w3.org/WAI/standards-guidelines/uaag/)
  - web browsers and media players, including some aspects of assistive technologies
- [Authoring Tool Accessibility Guidelines (ATAG)](https://www.w3.org/WAI/standards-guidelines/atag/)
  - authoring tools
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
  - web content - used by developers, authoring tools, and accessibility evaluation tools

### Web Content Accessibility Guidelines (WCAG)​

[WCAG 2.1](https://www.w3.org/TR/WCAG21/) extends on [WCAG 2.0](https://www.w3.org/TR/WCAG20/) and allows implementation of new technologies by addressing changes to the web. The W3C encourages use of the most current version of WCAG when developing or updating Web accessibility policies.

#### WCAG 2.1 Four Main Guiding Principles (abbreviated as POUR):​

- [Perceivable](https://www.w3.org/TR/WCAG21/#perceivable)
  - Users must be able to perceive the information being presented
- [Operable](https://www.w3.org/TR/WCAG21/#operable)
  - Interface forms, controls, and navigation are operable
- [Understandable](https://www.w3.org/TR/WCAG21/#understandable)
  - Information and the operation of user interface must be understandable to all users
- [Robust](https://www.w3.org/TR/WCAG21/#robust)
  - Users must be able to access the content as technologies advance

#### Web Accessibility Initiative – Accessible Rich Internet Applications (WAI-ARIA)​

W3C's WAI-ARIA provides guidance on how to build dynamic content and advanced user interface controls.

- [Accessible Rich Internet Applications (WAI-ARIA) 1.2](https://www.w3.org/TR/wai-aria-1.2/)
- [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/TR/wai-aria-practices-1.2/)

## Resources​

### Documentation​

- [WCAG 2.0](https://www.w3.org/TR/WCAG20/)
- [WCAG 2.1](https://www.w3.org/TR/WCAG21/)
- [Accessible Rich Internet Applications (WAI-ARIA) 1.2](https://www.w3.org/TR/wai-aria-1.2/)
- [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/TR/wai-aria-practices-1.2/)

### Assistive Technologies​

- Screen Readers
  - [NVDA](https://www.nvaccess.org/download/)
  - [VoiceOver](https://www.apple.com/accessibility/mac/vision/)
  - [JAWS](https://www.freedomscientific.com/products/software/jaws/?utm_term=jaws%20screen%20reader&utm_source=adwords&utm_campaign=All+Products&utm_medium=ppc&hsa_tgt=kwd-394361346638&hsa_cam=200218713&hsa_ad=296201131673&hsa_kw=jaws%20screen%20reader&hsa_grp=52663682111&hsa_net=adwords&hsa_mt=e&hsa_src=g&hsa_acc=1684996396&hsa_ver=3&gclid=Cj0KCQjwnv71BRCOARIsAIkxW9HXKQ6kKNQD0q8a_1TXSJXnIuUyb65KJeTWmtS6BH96-5he9dsNq6oaAh6UEALw_wcB)
  - [ChromeVox](https://chrome.google.com/webstore/detail/chromevox-classic-extensi/kgejglhpjiefppelpmljglcjbhoiplfn?hl=en)
- Zooming Tools
  - [MAGic](https://www.freedomscientific.com/products/software/magic/)
  - [ZoomText](https://www.freedomscientific.com/products/software/zoomtext/)
  - [Magnifier](https://support.microsoft.com/en-us/help/11542/windows-use-magnifier-to-make-things-easier-to-see)

### Testing​

- Automated Tools
  - [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)
  - [WAVE](https://chrome.google.com/webstore/detail/wave-evaluation-tool/jbbplnpkjmmeebjpijfedlgcdilocofh)
  - [ARC Toolkit](https://chrome.google.com/webstore/detail/arc-toolkit/chdkkkccnlfncngelccgbgfmjebmkmce?hl=en-US)
- Color Tools
  - [WebAim Color Contrast](https://webaim.org/resources/contrastchecker/)
  - [WebAim Link Color Contrast](https://webaim.org/resources/linkcontrastchecker)
- Other Helpful Tools
  - [HeadingMap](https://chrome.google.com/webstore/detail/headingsmap/flbjommegcjonpdmenkdiocclhjacmbi?hl=en%E2%80%A6)
  - [Color Oracle](https://colororacle.org)
  - [NerdeFocus](https://chrome.google.com/webstore/detail/nerdefocus/lpfiljldhgjecfepfljnbjnbjfhennpd?hl=en-US%E2%80%A6)
  - [Visual Aria](https://chrome.google.com/webstore/detail/visual-aria/lhbmajchkkmakajkjenkchhnhbadmhmk?hl=en-US)
  - [Silktide Website Accessibility Simulator](https://chrome.google.com/webstore/detail/silktide-website-accessib/okcpiimdfkpkjcbihbmhppldhiebhhaf?hl=en-US)

### Users​

The World Health Organization estimates that 15% of the world's population has some form of disability, 2-4% of them severely so. That is an estimated 1 billion people worldwide; making people with disabilities the largest minority group in the world.

There are a huge range of disabilities, which can be divided roughly into four categories:

- *Visual* - These users can benefit from the use of screen readers, screen magnification, controlling screen contrast, or braille display.
- *Auditory* - These users can benefit from captioning, transcripts or sign language video.
- *Motor* - These users can benefit from a range of [assistive technologies for motor impairments](https://webaim.org/articles/motor/assistive): voice recognition software, eye tracking, single-switch access, head wand, sip and puff switch, oversized trackball mouse, adaptive keyboard or other assistive technologies.
- *Cognitive* - These users can benefit from supplemental media, structural organization of content, clear and simple writing.

Check out the following links from WebAim to understand from users:

- [Web Accessibility Perspectives: Explore the Impact and Benefits for Everyone](https://www.w3.org/WAI/perspective-videos/)
- [Stories of Web Users](https://www.w3.org/WAI/people-use-web/user-stories/)

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/best-practices/accessibility.md)

---

# Performance​

> Vue.js - The Progressive JavaScript Framework

# Performance​

## Overview​

Vue is designed to be performant for most common use cases without much need for manual optimizations. However, there are always challenging scenarios where extra fine-tuning is needed. In this section, we will discuss what you should pay attention to when it comes to performance in a Vue application.

First, let's discuss the two major aspects of web performance:

- **Page Load Performance**: how fast the application shows content and becomes interactive on the initial visit. This is usually measured using web vital metrics like [Largest Contentful Paint (LCP)](https://web.dev/lcp/) and [Interaction to Next Paint](https://web.dev/articles/inp).
- **Update Performance**: how fast the application updates in response to user input. For example, how fast a list updates when the user types in a search box, or how fast the page switches when the user clicks a navigation link in a Single-Page Application (SPA).

While it would be ideal to maximize both, different frontend architectures tend to affect how easy it is to attain desired performance in these aspects. In addition, the type of application you are building greatly influences what you should prioritize in terms of performance. Therefore, the first step of ensuring optimal performance is picking the right architecture for the type of application you are building:

- Consult [Ways of Using Vue](https://vuejs.org/guide/extras/ways-of-using-vue) to see how you can leverage Vue in different ways.
- Jason Miller discusses the types of web applications and their respective ideal implementation / delivery in [Application Holotypes](https://jasonformat.com/application-holotypes/).

## Profiling Options​

To improve performance, we need to first know how to measure it. There are a number of great tools that can help in this regard:

For profiling load performance of production deployments:

- [PageSpeed Insights](https://pagespeed.web.dev/)
- [WebPageTest](https://www.webpagetest.org/)

For profiling performance during local development:

- [Chrome DevTools Performance Panel](https://developer.chrome.com/docs/devtools/evaluate-performance/)
  - [app.config.performance](https://vuejs.org/api/application#app-config-performance) enables Vue-specific performance markers in Chrome DevTools' performance timeline.
- [Vue DevTools Extension](https://vuejs.org/guide/scaling-up/tooling#browser-devtools) also provides a performance profiling feature.

## Page Load Optimizations​

There are many framework-agnostic aspects for optimizing page load performance - check out [this web.dev guide](https://web.dev/fast/) for a comprehensive round up. Here, we will primarily focus on techniques that are specific to Vue.

### Choosing the Right Architecture​

If your use case is sensitive to page load performance, avoid shipping it as a pure client-side SPA. You want your server to be directly sending HTML containing the content the users want to see. Pure client-side rendering suffers from slow time-to-content. This can be mitigated with [Server-Side Rendering (SSR)](https://vuejs.org/guide/extras/ways-of-using-vue#fullstack-ssr) or [Static Site Generation (SSG)](https://vuejs.org/guide/extras/ways-of-using-vue#jamstack-ssg). Check out the [SSR Guide](https://vuejs.org/guide/scaling-up/ssr) to learn about performing SSR with Vue. If your app doesn't have rich interactivity requirements, you can also use a traditional backend server to render the HTML and enhance it with Vue on the client.

If your main application has to be an SPA, but has marketing pages (landing, about, blog), ship them separately! Your marketing pages should ideally be deployed as static HTML with minimal JS, by using SSG.

### Bundle Size and Tree-shaking​

One of the most effective ways to improve page load performance is shipping smaller JavaScript bundles. Here are a few ways to reduce bundle size when using Vue:

- Use a build step if possible.
  - Many of Vue's APIs are ["tree-shakable"](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking) if bundled via a modern build tool. For example, if you don't use the built-in `<Transition>` component, it won't be included in the final production bundle. Tree-shaking can also remove other unused modules in your source code.
  - When using a build step, templates are pre-compiled so we don't need to ship the Vue compiler to the browser. This saves **14kb** min+gzipped JavaScript and avoids the runtime compilation cost.
- Be cautious of size when introducing new dependencies! In real-world applications, bloated bundles are most often a result of introducing heavy dependencies without realizing it.
  - If using a build step, prefer dependencies that offer ES module formats and are tree-shaking friendly. For example, prefer `lodash-es` over `lodash`.
  - Check a dependency's size and evaluate whether it is worth the functionality it provides. Note if the dependency is tree-shaking friendly, the actual size increase will depend on the APIs you actually import from it. Tools like [bundlejs.com](https://bundlejs.com/) can be used for quick checks, but measuring with your actual build setup will always be the most accurate.
- If you are using Vue primarily for progressive enhancement and prefer to avoid a build step, consider using [petite-vue](https://github.com/vuejs/petite-vue) (only **6kb**) instead.

### Code Splitting​

Code splitting is where a build tool splits the application bundle into multiple smaller chunks, which can then be loaded on demand or in parallel. With proper code splitting, features required at page load can be downloaded immediately, with additional chunks being lazy loaded only when needed, thus improving performance.

Bundlers like Rollup (which Vite is based upon) or webpack can automatically create split chunks by detecting the ESM dynamic import syntax:

js

```
// lazy.js and its dependencies will be split into a separate chunk
// and only loaded when `loadLazy()` is called.
function loadLazy() {
  return import('./lazy.js')
}
```

Lazy loading is best used on features that are not immediately needed after initial page load. In Vue applications, this can be used in combination with Vue's [Async Component](https://vuejs.org/guide/components/async) feature to create split chunks for component trees:

js

```
import { defineAsyncComponent } from 'vue'

// a separate chunk is created for Foo.vue and its dependencies.
// it is only fetched on demand when the async component is
// rendered on the page.
const Foo = defineAsyncComponent(() => import('./Foo.vue'))
```

For applications using Vue Router, it is strongly recommended to use lazy loading for route components. Vue Router has explicit support for lazy loading, separate from `defineAsyncComponent`. See [Lazy Loading Routes](https://router.vuejs.org/guide/advanced/lazy-loading.html) for more details.

## Update Optimizations​

### Props Stability​

In Vue, a child component only updates when at least one of its received props has changed. Consider the following example:

template

```
<ListItem
  v-for="item in list"
  :id="item.id"
  :active-id="activeId" />
```

Inside the `<ListItem>` component, it uses its `id` and `activeId` props to determine whether it is the currently active item. While this works, the problem is that whenever `activeId` changes, **every** `<ListItem>` in the list has to update!

Ideally, only the items whose active status changed should update. We can achieve that by moving the active status computation into the parent, and make `<ListItem>` directly accept an `active` prop instead:

template

```
<ListItem
  v-for="item in list"
  :id="item.id"
  :active="item.id === activeId" />
```

Now, for most components the `active` prop will remain the same when `activeId` changes, so they no longer need to update. In general, the idea is keeping the props passed to child components as stable as possible.

### v-once​

`v-once` is a built-in directive that can be used to render content that relies on runtime data but never needs to update. The entire sub-tree it is used on will be skipped for all future updates. Consult its [API reference](https://vuejs.org/api/built-in-directives#v-once) for more details.

### v-memo​

`v-memo` is a built-in directive that can be used to conditionally skip the update of large sub-trees or `v-for` lists. Consult its [API reference](https://vuejs.org/api/built-in-directives#v-memo) for more details.

### Computed Stability​

In Vue 3.4 and above, a computed property will only trigger effects when its computed value has changed from the previous one. For example, the following `isEven` computed only triggers effects if the returned value has changed from `true` to `false`, or vice-versa:

js

```
const count = ref(0)
const isEven = computed(() => count.value % 2 === 0)

watchEffect(() => console.log(isEven.value)) // true

// will not trigger new logs because the computed value stays `true`
count.value = 2
count.value = 4
```

This reduces unnecessary effect triggers, but unfortunately doesn't work if the computed creates a new object on each compute:

js

```
const computedObj = computed(() => {
  return {
    isEven: count.value % 2 === 0
  }
})
```

Because a new object is created each time, the new value is technically always different from the old value. Even if the `isEven` property remains the same, Vue won't be able to know unless it performs a deep comparison of the old value and the new value. Such comparison could be expensive and likely not worth it.

Instead, we can optimize this by manually comparing the new value with the old value, and conditionally returning the old value if we know nothing has changed:

js

```
const computedObj = computed((oldValue) => {
  const newValue = {
    isEven: count.value % 2 === 0
  }
  if (oldValue && oldValue.isEven === newValue.isEven) {
    return oldValue
  }
  return newValue
})
```

[Try it in the playground](https://play.vuejs.org/#eNqVVMtu2zAQ/JUFgSZK4UpuczMkow/40AJ9IC3aQ9mDIlG2EokUyKVt1PC/d0lKtoEminMQQC1nZ4c7S+7Yu66L11awGUtNoesOwQi03ZzLuu2URtiBFtUECtV2FkU5gU2OxWpRVaJA2EOlVQuXxHDJJZeFkgYJayVC5hKj6dUxLnzSjZXmV40rZfFrh3Vb/82xVrLH//5DCQNNKPkweNiNVFP+zBsrIJvDjksgGrRahjVAbRZrIWdBVLz2yBfwBrIsg6mD7LncPyryfIVnywupUmz68HOEEqqCI+XFBQzrOKR79MDdx66GCn1jhpQDZx8f0oZ+nBgdRVcH/aMuBt1xZ80qGvGvh/X6nlXwnGpPl6qsLLxTtitzFFTNl0oSN/79AKOCHHQuS5pw4XorbXsr9ImHZN7nHFdx1SilI78MeOJ7Ca+nbvgd+GgomQOv6CNjSQqXaRJuHd03+kHRdg3JoT+A3a7XsfcmpbcWkQS/LZq6uM84C8o5m4fFuOg0CemeOXXX2w2E6ylsgj2gTgeYio/f1l5UEqj+Z3yC7lGuNDlpApswNNTrql7Gd0ZJeqW8TZw5t+tGaMdDXnA2G4acs7xp1OaTj6G2YjLEi5Uo7h+I35mti3H2TQsj9Jp6etjDXC8Fhu3F9y9iS+vDZqtK2xB6ZPNGGNVYpzHA3ltZkuwTnFf70b+1tVz+MIstCmmGQzmh/p56PGf00H4YOfpR7nV8PTxubP8P2GAP9Q==)

Note that you should always perform the full computation before comparing and returning the old value, so that the same dependencies can be collected on every run.

## General Optimizations​

> The following tips affect both page load and update performance.

### Virtualize Large Lists​

One of the most common performance issues in all frontend applications is rendering large lists. No matter how performant a framework is, rendering a list with thousands of items **will** be slow due to the sheer number of DOM nodes that the browser needs to handle.

However, we don't necessarily have to render all these nodes upfront. In most cases, the user's screen size can display only a small subset of our large list. We can greatly improve the performance with **list virtualization**, the technique of only rendering the items that are currently in or close to the viewport in a large list.

Implementing list virtualization isn't easy, luckily there are existing community libraries that you can directly use:

- [vue-virtual-scroller](https://github.com/Akryum/vue-virtual-scroller)
- [vue-virtual-scroll-grid](https://github.com/rocwang/vue-virtual-scroll-grid)
- [vueuc/VVirtualList](https://github.com/07akioni/vueuc)

### Reduce Reactivity Overhead for Large Immutable Structures​

Vue's reactivity system is deep by default. While this makes state management intuitive, it does create a certain level of overhead when the data size is large, because every property access triggers proxy traps that perform dependency tracking. This typically becomes noticeable when dealing with large arrays of deeply nested objects, where a single render needs to access 100,000+ properties, so it should only affect very specific use cases.

Vue does provide an escape hatch to opt-out of deep reactivity by using [shallowRef()](https://vuejs.org/api/reactivity-advanced#shallowref) and [shallowReactive()](https://vuejs.org/api/reactivity-advanced#shallowreactive). Shallow APIs create state that is reactive only at the root level, and exposes all nested objects untouched. This keeps nested property access fast, with the trade-off being that we must now treat all nested objects as immutable, and updates can only be triggered by replacing the root state:

js

```
const shallowArray = shallowRef([
  /* big list of deep objects */
])

// this won't trigger updates...
shallowArray.value.push(newObject)
// this does:
shallowArray.value = [...shallowArray.value, newObject]

// this won't trigger updates...
shallowArray.value[0].foo = 1
// this does:
shallowArray.value = [
  {
    ...shallowArray.value[0],
    foo: 1
  },
  ...shallowArray.value.slice(1)
]
```

### Avoid Unnecessary Component Abstractions​

Sometimes we may create [renderless components](https://vuejs.org/guide/components/slots#renderless-components) or higher-order components (i.e. components that render other components with extra props) for better abstraction or code organization. While there is nothing wrong with this, do keep in mind that component instances are much more expensive than plain DOM nodes, and creating too many of them due to abstraction patterns will incur performance costs.

Note that reducing only a few instances won't have noticeable effect, so don't sweat it if the component is rendered only a few times in the app. The best scenario to consider this optimization is again in large lists. Imagine a list of 100 items where each item component contains many child components. Removing one unnecessary component abstraction here could result in a reduction of hundreds of component instances.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/best-practices/performance.md)

---

# Production Deployment​

> Vue.js - The Progressive JavaScript Framework

# Production Deployment​

## Development vs. Production​

During development, Vue provides a number of features to improve the development experience:

- Warning for common errors and pitfalls
- Props / events validation
- [Reactivity debugging hooks](https://vuejs.org/guide/extras/reactivity-in-depth#reactivity-debugging)
- Devtools integration

However, these features become useless in production. Some of the warning checks can also incur a small amount of performance overhead. When deploying to production, we should drop all the unused, development-only code branches for smaller payload size and better performance.

## Without Build Tools​

If you are using Vue without a build tool by loading it from a CDN or self-hosted script, make sure to use the production build (dist files that end in `.prod.js`) when deploying to production. Production builds are pre-minified with all development-only code branches removed.

- If using global build (accessing via the `Vue` global): use `vue.global.prod.js`.
- If using ESM build (accessing via native ESM imports): use `vue.esm-browser.prod.js`.

Consult the [dist file guide](https://github.com/vuejs/core/tree/main/packages/vue#which-dist-file-to-use) for more details.

## With Build Tools​

Projects scaffolded via `create-vue` (based on Vite) or Vue CLI (based on webpack) are pre-configured for production builds.

If using a custom setup, make sure that:

1. `vue` resolves to `vue.runtime.esm-bundler.js`.
2. The [compile time feature flags](https://vuejs.org/api/compile-time-flags) are properly configured.
3. `process.env.NODE_ENV` is replaced with `"production"` during build.

Additional references:

- [Vite production build guide](https://vitejs.dev/guide/build.html)
- [Vite deployment guide](https://vitejs.dev/guide/static-deploy.html)
- [Vue CLI deployment guide](https://cli.vuejs.org/guide/deployment.html)

## Tracking Runtime Errors​

The [app-level error handler](https://vuejs.org/api/application#app-config-errorhandler) can be used to report errors to tracking services:

js

```
import { createApp } from 'vue'

const app = createApp(...)

app.config.errorHandler = (err, instance, info) => {
  // report error to tracking services
}
```

Services such as [Sentry](https://docs.sentry.io/platforms/javascript/guides/vue/) and [Bugsnag](https://docs.bugsnag.com/platforms/javascript/vue/) also provide official integrations for Vue.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/best-practices/production-deployment.md)

---

# Security​

> Vue.js - The Progressive JavaScript Framework

# Security​

## Reporting Vulnerabilities​

When a vulnerability is reported, it immediately becomes our top concern, with a full-time contributor dropping everything to work on it. To report a vulnerability, please email [security@vuejs.org](mailto:security@vuejs.org).

While the discovery of new vulnerabilities is rare, we also recommend always using the latest versions of Vue and its official companion libraries to ensure your application remains as secure as possible.

## Rule No.1: Never Use Non-trusted Templates​

The most fundamental security rule when using Vue is **never use non-trusted content as your component template**. Doing so is equivalent to allowing arbitrary JavaScript execution in your application - and worse, could lead to server breaches if the code is executed during server-side rendering. An example of such usage:

js

```
Vue.createApp({
  template: `<div>` + userProvidedString + `</div>` // NEVER DO THIS
}).mount('#app')
```

Vue templates are compiled into JavaScript, and expressions inside templates will be executed as part of the rendering process. Although the expressions are evaluated against a specific rendering context, due to the complexity of potential global execution environments, it is impractical for a framework like Vue to completely shield you from potential malicious code execution without incurring unrealistic performance overhead. The most straightforward way to avoid this category of problems altogether is to make sure the contents of your Vue templates are always trusted and entirely controlled by you.

## What Vue Does to Protect You​

### HTML content​

Whether using templates or render functions, content is automatically escaped. That means in this template:

template

```
<h1>{{ userProvidedString }}</h1>
```

if `userProvidedString` contained:

js

```
'<script>alert("hi")</script>'
```

then it would be escaped to the following HTML:

template

```
&lt;script&gt;alert(&quot;hi&quot;)&lt;/script&gt;
```

thus preventing the script injection. This escaping is done using native browser APIs, like `textContent`, so a vulnerability can only exist if the browser itself is vulnerable.

### Attribute bindings​

Similarly, dynamic attribute bindings are also automatically escaped. That means in this template:

template

```
<h1 :title="userProvidedString">
  hello
</h1>
```

if `userProvidedString` contained:

js

```
'" onclick="alert(\'hi\')'
```

then it would be escaped to the following HTML:

template

```
&quot; onclick=&quot;alert('hi')
```

thus preventing the close of the `title` attribute to inject new, arbitrary HTML. This escaping is done using native browser APIs, like `setAttribute`, so a vulnerability can only exist if the browser itself is vulnerable.

## Potential Dangers​

In any web application, allowing unsanitized, user-provided content to be executed as HTML, CSS, or JavaScript is potentially dangerous, so it should be avoided wherever possible. There are times when some risk may be acceptable, though.

For example, services like CodePen and JSFiddle allow user-provided content to be executed, but it's in a context where this is expected and sandboxed to some extent inside iframes. In the cases when an important feature inherently requires some level of vulnerability, it's up to your team to weigh the importance of the feature against the worst-case scenarios the vulnerability enables.

### HTML Injection​

As you learned earlier, Vue automatically escapes HTML content, preventing you from accidentally injecting executable HTML into your application. However, **in cases where you know the HTML is safe**, you can explicitly render HTML content:

- Using a template:
  template
  ```
  <div v-html="userProvidedHtml"></div>
  ```
- Using a render function:
  js
  ```
  h('div', {
    innerHTML: this.userProvidedHtml
  })
  ```
- Using a render function with JSX:
  jsx
  ```
  <div innerHTML={this.userProvidedHtml}></div>
  ```

WARNING

User-provided HTML can never be considered 100% safe unless it's in a sandboxed iframe or in a part of the app where only the user who wrote that HTML can ever be exposed to it. Additionally, allowing users to write their own Vue templates brings similar dangers.

### URL Injection​

In a URL like this:

template

```
<a :href="userProvidedUrl">
  click me
</a>
```

There's a potential security issue if the URL has not been "sanitized" to prevent JavaScript execution using `javascript:`. There are libraries such as [sanitize-url](https://www.npmjs.com/package/@braintree/sanitize-url) to help with this, but note: if you're ever doing URL sanitization on the frontend, you already have a security issue. **User-provided URLs should always be sanitized by your backend before even being saved to a database.** Then the problem is avoided for *every* client connecting to your API, including native mobile apps. Also note that even with sanitized URLs, Vue cannot help you guarantee that they lead to safe destinations.

### Style Injection​

Looking at this example:

template

```
<a
  :href="sanitizedUrl"
  :style="userProvidedStyles"
>
  click me
</a>
```

Let's assume that `sanitizedUrl` has been sanitized, so that it's definitely a real URL and not JavaScript. With the `userProvidedStyles`, malicious users could still provide CSS to "click jack", e.g. styling the link into a transparent box over the "Log in" button. Then if `https://user-controlled-website.com/` is built to resemble the login page of your application, they might have just captured a user's real login information.

You may be able to imagine how allowing user-provided content for a `<style>` element would create an even greater vulnerability, giving that user full control over how to style the entire page. That's why Vue prevents rendering of style tags inside templates, such as:

template

```
<style>{{ userProvidedStyles }}</style>
```

To keep your users fully safe from clickjacking, we recommend only allowing full control over CSS inside a sandboxed iframe. Alternatively, when providing user control through a style binding, we recommend using its [object syntax](https://vuejs.org/guide/essentials/class-and-style#binding-to-objects-1) and only allowing users to provide values for specific properties it's safe for them to control, like this:

template

```
<a
  :href="sanitizedUrl"
  :style="{
    color: userProvidedColor,
    background: userProvidedBackground
  }"
>
  click me
</a>
```

### JavaScript Injection​

We strongly discourage ever rendering a `<script>` element with Vue, since templates and render functions should never have side effects. However, this isn't the only way to include strings that would be evaluated as JavaScript at runtime.

Every HTML element has attributes with values accepting strings of JavaScript, such as `onclick`, `onfocus`, and `onmouseenter`. Binding user-provided JavaScript to any of these event attributes is a potential security risk, so it should be avoided.

WARNING

User-provided JavaScript can never be considered 100% safe unless it's in a sandboxed iframe or in a part of the app where only the user who wrote that JavaScript can ever be exposed to it.

Sometimes we receive vulnerability reports on how it's possible to do cross-site scripting (XSS) in Vue templates. In general, we do not consider such cases to be actual vulnerabilities because there's no practical way to protect developers from the two scenarios that would allow XSS:

1. The developer is explicitly asking Vue to render user-provided, unsanitized content as Vue templates. This is inherently unsafe, and there's no way for Vue to know the origin.
2. The developer is mounting Vue to an entire HTML page which happens to contain server-rendered and user-provided content. This is fundamentally the same problem as #1, but sometimes devs may do it without realizing it. This can lead to possible vulnerabilities where the attacker provides HTML which is safe as plain HTML but unsafe as a Vue template. The best practice is to **never mount Vue on nodes that may contain server-rendered and user-provided content**.

## Best Practices​

The general rule is that if you allow unsanitized, user-provided content to be executed (as either HTML, JavaScript, or even CSS), you might open yourself up to attacks. This advice actually holds true whether using Vue, another framework, or even no framework.

Beyond the recommendations made above for [Potential Dangers](#potential-dangers), we also recommend familiarizing yourself with these resources:

- [HTML5 Security Cheat Sheet](https://html5sec.org/)
- [OWASP's Cross Site Scripting (XSS) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

Then use what you learn to also review the source code of your dependencies for potentially dangerous patterns, if any of them include 3rd-party components or otherwise influence what's rendered to the DOM.

## Backend Coordination​

HTTP security vulnerabilities, such as cross-site request forgery (CSRF/XSRF) and cross-site script inclusion (XSSI), are primarily addressed on the backend, so they aren't a concern of Vue's. However, it's still a good idea to communicate with your backend team to learn how to best interact with their API, e.g., by submitting CSRF tokens with form submissions.

## Server-Side Rendering (SSR)​

There are some additional security concerns when using SSR, so make sure to follow the best practices outlined throughout [our SSR documentation](https://vuejs.org/guide/scaling-up/ssr) to avoid vulnerabilities.

[Edit this page on GitHub](https://github.com/vuejs/docs/edit/main/src/guide/best-practices/security.md)
