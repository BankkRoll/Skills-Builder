# Astro Courses and more

# Astro Courses

> Learn Astro with out-of-this-world courses and tutorials.

# Astro Courses

Want to get started learning Astro with a course or tutorial?

You can learn the basics of Astro with our [official docs Build a Blog tutorial](https://docs.astro.build/en/tutorial/0-introduction/), or explore our collection of recommended Astro educational content.

## Education Partners

[Section titled “Education Partners”](#education-partners)

Learn Astro from trusted Astro educators, with video lessons, interactive challenges, and projects!

   [Learn Astro with Coding in Public](https://learnastro.dev/?code=ASTRO_PROMO) A premium interactive course with 150+ video lessons that teaches you how to use Astro’s built-in tooling and features.      [Learn Astro with James Q Quick](https://scrimba.com/intro-to-astro-c00ar0fi5u?via=astro) Build your first Astro site with 35 interactive Scrimba lessons, with video and IDE merged into one unique learning platform.

## Community learning resources

[Section titled “Community learning resources”](#community-learning-resources)

Learn from your fellow astronauts with curated collections of guides, articles, and blog posts.

   [Astro Tips](https://astro-tips.dev/) Advanced, unusual, experimental, and community-written recipes, tutorials, and quick tips.     [Astro Support Squid](https://get.supportsquid.ink/) An open, public Astro support forum and knowledge base outside of the Astro Discord.    Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Components

> An introduction to Astro components.

# Components

**Astro components** are the basic building blocks of any Astro project. They are HTML-only templating components with no client-side runtime and use the `.astro` file extension.

Astro components are extremely flexible. An Astro component can be as small as a snippet of HTML, like a collection of common `<meta>` tags that make SEO easy to work with. Components can be reusable UI elements, like a header or a profile card. Astro components can even contain an entire page layout or, when located in the special `src/pages/` folder, be an entire page itself.

The most important thing to know about Astro components is that they **don’t render on the client**. They render to HTML either at build-time or on-demand. You can include JavaScript code inside of your component frontmatter, and all of it will be stripped from the final page sent to your users’ browsers. The result is a faster site, with zero JavaScript footprint added by default.

When your Astro component does need client-side interactivity, you can add [standard HTML<script>tags](https://docs.astro.build/en/guides/client-side-scripts/) or [UI Framework components](https://docs.astro.build/en/guides/framework-components/#hydrating-interactive-components) as “client islands”.

For components that need to render personalized or dynamic content, you can defer their server rendering by adding a [server directive](https://docs.astro.build/en/reference/directives-reference/#server-directives). These “server islands” will render their content when it is available, without delaying the entire page load.

## Component Structure

[Section titled “Component Structure”](#component-structure)

An Astro component is made up of two main parts: the **Component Script** and the **Component Template**. Each part performs a different job, but together they provide a framework that is both easy to use and expressive enough to handle whatever you might want to build.

 src/components/EmptyComponent.astro

```
---// Component Script (JavaScript)---
```

### The Component Script

[Section titled “The Component Script”](#the-component-script)

Astro uses a code fence (`---`) to identify the component script in your Astro component. If you’ve ever written Markdown before, you may already be familiar with a similar concept called *frontmatter.* Astro’s idea of a component script was directly inspired by this concept.

You can use the component script to write any JavaScript code that you need to render your template. This can include:

- importing other Astro components
- importing other framework components, like React
- importing data, like a JSON file
- fetching content from an API or database
- creating variables that you will reference in your template

 src/components/MyComponent.astro

```
---import SomeAstroComponent from '../components/SomeAstroComponent.astro';import SomeReactComponent from '../components/SomeReactComponent.jsx';import someData from '../data/pokemon.json';
// Access passed-in component props, like `<X title="Hello, World" />`const { title } = Astro.props;
// Fetch external data, even from a private API or databaseconst data = await fetch('SOME_SECRET_API_URL/users').then(r => r.json());---
```

The code fence is designed to guarantee that the JavaScript that you write in it is “fenced in.” It won’t escape into your frontend application, or fall into your user’s hands. You can safely write code here that is expensive or sensitive (like a call to your private database) without worrying about it ever ending up in your user’s browser.

### The Component Template

[Section titled “The Component Template”](#the-component-template)

The component template is below the code fence and determines the HTML output of your component.

If you write plain HTML here, your component will render that HTML in any Astro page it is imported and used.

However, [Astro’s component template syntax](https://docs.astro.build/en/reference/astro-syntax/) also supports **JavaScript expressions**, Astro [<style>](https://docs.astro.build/en/guides/styling/#styling-in-astro) and [<script>](https://docs.astro.build/en/guides/client-side-scripts/) tags, **imported components**, and [special Astro directives](https://docs.astro.build/en/reference/directives-reference/). Data and values defined in the component script can be used in the component template to produce dynamically-created HTML.

 src/components/MyFavoritePokemon.astro

```
---// Your component script here!import Banner from '../components/Banner.astro';import Avatar from '../components/Avatar.astro';import ReactPokemonComponent from '../components/ReactPokemonComponent.jsx';const myFavoritePokemon = [/* ... */];const { title } = Astro.props;---{/* JS comment syntax is also valid! */}
<Banner /><h1>Hello, world!</h1>
<p>{title}</p>
<Avatar server:defer>  <svg slot="fallback" class="generic-avatar" transition:name="avatar">...</svg></Avatar>
<ReactPokemonComponent client:visible />
<ul>  {myFavoritePokemon.map((data) => <li>{data.name}</li>)}</ul>
<p class:list={["add", "dynamic", { classNames: true }]} />
```

## Component-based design

[Section titled “Component-based design”](#component-based-design)

Components are designed to be **reusable** and **composable**. You can use components inside of other components to build more and more advanced UI. For example, a `Button` component could be used to create a `ButtonGroup` component:

 src/components/ButtonGroup.astro

```
---import Button from './Button.astro';---<div>  <Button title="Button 1" />  <Button title="Button 2" />  <Button title="Button 3" /></div>
```

## Component Props

[Section titled “Component Props”](#component-props)

An Astro component can define and accept props. These props then become available to the component template for rendering HTML. Props are available on the `Astro.props` global in your frontmatter script.

Here is an example of a component that receives a `greeting` prop and a `name` prop. Notice that the props to be received are destructured from the global `Astro.props` object.

 src/components/GreetingHeadline.astro

```
---// Usage: <GreetingHeadline greeting="Howdy" name="Partner" />const { greeting, name } = Astro.props;---<h2>{greeting}, {name}!</h2>
```

This component, when imported and rendered in other Astro components, layouts or pages, can pass these props as attributes:

 src/components/GreetingCard.astro

```
---import GreetingHeadline from './GreetingHeadline.astro';const name = 'Astro';---<h1>Greeting Card</h1><GreetingHeadline greeting="Hi" name={name} /><p>I hope you have a wonderful day!</p>
```

You can also define your props with TypeScript with a `Props` type interface. Astro will automatically pick up the `Props` interface in your frontmatter and give type warnings/errors. These props can also be given default values when destructured from `Astro.props`.

 src/components/GreetingHeadline.astro

```
---interface Props {  name: string;  greeting?: string;}
const { greeting = "Hello", name } = Astro.props;---<h2>{greeting}, {name}!</h2>
```

Component props can be given default values to use when none are provided.

 src/components/GreetingHeadline.astro

```
---const { greeting = "Hello", name = "Astronaut" } = Astro.props;---<h2>{greeting}, {name}!</h2>
```

## Slots

[Section titled “Slots”](#slots)

The `<slot />` element is a placeholder for external HTML content, allowing you to inject (or “slot”) child elements from other files into your component template.

By default, all child elements passed to a component will be rendered in its `<slot />`.

  src/components/Wrapper.astro

```
---import Header from './Header.astro';import Logo from './Logo.astro';import Footer from './Footer.astro';
const { title } = Astro.props;---<div id="content-wrapper">  <Header />  <Logo />  <h1>{title}</h1>  <slot />    <Footer /></div>
```

 src/pages/fred.astro

```
---import Wrapper from '../components/Wrapper.astro';---<Wrapper title="Fred's Page">  <h2>All about Fred</h2>  <p>Here is some stuff about Fred.</p></Wrapper>
```

This pattern is the basis of an [Astro layout component](https://docs.astro.build/en/basics/layouts/): an entire page of HTML content can be “wrapped” with `<SomeLayoutComponent></SomeLayoutComponent>` tags and sent to the component to render inside of common page elements defined there.

   See the [Astro.slotsutility functions](https://docs.astro.build/en/reference/astro-syntax/#astroslots) for more ways to access and render slot content.

### Named Slots

[Section titled “Named Slots”](#named-slots)

An Astro component can also have named slots. This allows you to pass only HTML elements with the corresponding slot name into a slot’s location.

Slots are named using the `name` attribute:

 src/components/Wrapper.astro

```
---import Header from './Header.astro';import Logo from './Logo.astro';import Footer from './Footer.astro';
const { title } = Astro.props;---<div id="content-wrapper">  <Header />    <slot name="after-header" />  <Logo />  <h1>{title}</h1>    <slot />  <Footer />    <slot name="after-footer" /></div>
```

To inject HTML content into a particular slot, use the `slot` attribute on any child element to specify the name of the slot. All other child elements of the component will be injected into the default (unnamed) `<slot />`.

 src/pages/fred.astro

```
---import Wrapper from '../components/Wrapper.astro';---<Wrapper title="Fred's Page">  <img src="https://my.photo/fred.jpg" slot="after-header" />  <h2>All about Fred</h2>  <p>Here is some stuff about Fred.</p>  <p slot="after-footer">Copyright 2022</p></Wrapper>
```

To pass multiple HTML elements into a component’s `<slot/>` placeholder without a wrapping `<div>`, use the `slot=""` attribute on [Astro’s<Fragment/>component](https://docs.astro.build/en/reference/astro-syntax/#fragments):

 src/components/CustomTable.astro

```
---// Create a custom table with named slot placeholders for header and body content---<table class="bg-white">  <thead class="sticky top-0 bg-white"><slot name="header" /></thead>  <tbody class="[&_tr:nth-child(odd)]:bg-gray-100"><slot name="body" /></tbody></table>
```

Inject multiple rows and columns of HTML content using a `slot=""` attribute to specify the `"header"` and `"body"` content. Individual HTML elements can also be styled:

 src/components/StockTable.astro

```
---import CustomTable from './CustomTable.astro';---<CustomTable>  <Fragment slot="header">     <tr><th>Product name</th><th>Stock units</th></tr>  </Fragment>
  <Fragment slot="body">     <tr><td>Flip-flops</td><td>64</td></tr>    <tr><td>Boots</td><td>32</td></tr>    <tr><td>Sneakers</td><td class="text-red-500">0</td></tr>  </Fragment></CustomTable>
```

Note that named slots must be an immediate child of the component. You cannot pass named slots through nested elements.

### Fallback Content for Slots

[Section titled “Fallback Content for Slots”](#fallback-content-for-slots)

Slots can also render **fallback content**. When there are no matching children passed to a slot, a `<slot />` element will render its own placeholder children.

 src/components/Wrapper.astro

```
---import Header from './Header.astro';import Logo from './Logo.astro';import Footer from './Footer.astro';
const { title } = Astro.props;---<div id="content-wrapper">  <Header />  <Logo />  <h1>{title}</h1>  <slot>    <p>This is my fallback content, if there is no child passed into slot</p>  </slot>  <Footer /></div>
```

Fallback content will only be displayed when there are no matching elements with the `slot="name"` attribute being passed in to a named slot.

Astro will pass an empty slot when a slot element exists but has no content to pass. Fallback content cannot be used as a default when an empty slot is passed. Fallback content is only displayed when no slot element can be found.

### Transferring slots

[Section titled “Transferring slots”](#transferring-slots)

Slots can be transferred to other components. For example, when creating nested layouts:

 src/layouts/BaseLayout.astro

```
------<html lang="en">  <head>    <meta charset="utf-8" />    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />    <meta name="viewport" content="width=device-width" />    <meta name="generator" content={Astro.generator} />    <slot name="head" />  </head>  <body>    <slot />  </body></html>
```

 src/layouts/HomeLayout.astro

```
---import BaseLayout from './BaseLayout.astro';---<BaseLayout>  <slot name="head" slot="head" />  <slot /></BaseLayout>
```

Now, the default and `head` slots passed to `HomeLayout` will be transferred to the `BaseLayout` parent.

 src/pages/index.astro

```
---import HomeLayout from '../layouts/HomeLayout.astro';---<HomeLayout>  <title slot="head">Astro</title>  <h1>Astro</h1></HomeLayout>
```

## HTML Components

[Section titled “HTML Components”](#html-components)

Astro supports importing and using `.html` files as components or placing these files within the `src/pages/` subdirectory as pages. You may want to use HTML components if you’re reusing code from an existing site built without a framework, or if you want to ensure that your component has no dynamic features.

HTML components must contain only valid HTML, and therefore lack key Astro component features:

- They don’t support frontmatter, server-side imports, or dynamic expressions.
- Any `<script>` tags are left unbundled, treated as if they had an [is:inlinedirective](https://docs.astro.build/en/reference/directives-reference/#isinline).
- They can only [reference assets that are in thepublic/folder](https://docs.astro.build/en/basics/project-structure/#public).

## Next Steps

[Section titled “Next Steps”](#next-steps)   Read more about using [UI framework components](https://docs.astro.build/en/guides/framework-components/) in your Astro project.  Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Pages

> An introduction to Astro pages.

# Pages

**Pages** are files that live in the `src/pages/` subdirectory of your Astro project. They are responsible for handling routing, data loading, and overall page layout for every page in your website.

## Supported page files

[Section titled “Supported page files”](#supported-page-files)

Astro supports the following file types in the `src/pages/` directory:

- [.astro](#astro-pages)
- [.md](#markdownmdx-pages)
- `.mdx` (with the [MDX Integration installed](https://docs.astro.build/en/guides/integrations-guide/mdx/#installation))
- [.html](#html-pages)
- `.js`/`.ts` (as [endpoints](https://docs.astro.build/en/guides/endpoints/))

## File-based routing

[Section titled “File-based routing”](#file-based-routing)

Astro leverages a routing strategy called **file-based routing**. Each file in your `src/pages/` directory becomes an endpoint on your site based on its file path.

A single file can also generate multiple pages using [dynamic routing](https://docs.astro.build/en/guides/routing/#dynamic-routes). This allows you to create pages even if your content lives outside of the special `/pages/` directory, such as in a [content collection](https://docs.astro.build/en/guides/content-collections/) or a [CMS](https://docs.astro.build/en/guides/cms/).

   Read more about [Routing in Astro](https://docs.astro.build/en/guides/routing/).

### Link between pages

[Section titled “Link between pages”](#link-between-pages)

Write standard HTML [<a>elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a) in your Astro pages to link to other pages on your site. Use a **URL path relative to your root domain** as your link, not a relative file path.

For example, to link to `https://example.com/authors/sonali/` from any other page on `example.com`:

 src/pages/index.astro

```
Read more <a href="/authors/sonali/">about Sonali</a>.
```

## Astro Pages

[Section titled “Astro Pages”](#astro-pages)

Astro pages use the `.astro` file extension and support the same features as [Astro components](https://docs.astro.build/en/basics/astro-components/).

 src/pages/index.astro

```
------<html lang="en">  <head>    <title>My Homepage</title>  </head>  <body>    <h1>Welcome to my website!</h1>  </body></html>
```

A page must produce a full HTML document. If not explicitly included, Astro will add the necessary `<!DOCTYPE html>` declaration and `<head>` content to any `.astro` component located within `src/pages/` by default. You can opt-out of this behavior on a per-component basis by marking it as a [partial](#page-partials) page.

To avoid repeating the same HTML elements on every page, you can move common `<head>` and `<body>` elements into your own [layout components](https://docs.astro.build/en/basics/layouts/). You can use as many or as few layout components as you’d like.

 src/pages/index.astro

```
---import MySiteLayout from "../layouts/MySiteLayout.astro";---<MySiteLayout>  <p>My page content, wrapped in a layout!</p></MySiteLayout>
```

   Read more about [layout components](https://docs.astro.build/en/basics/layouts/) in Astro.

## Markdown/MDX Pages

[Section titled “Markdown/MDX Pages”](#markdownmdx-pages)

Astro also treats any Markdown (`.md`) files inside of `src/pages/` as pages in your final website. If you have the [MDX Integration installed](https://docs.astro.build/en/guides/integrations-guide/mdx/#installation), it also treats MDX (`.mdx`) files the same way.

Markdown files can use the special `layout` frontmatter property to specify a [layout component](https://docs.astro.build/en/basics/layouts/) that will wrap their Markdown content in a full `<html>...</html>` page document.

 src/pages/page.md

```
---layout: ../layouts/MySiteLayout.astrotitle: My Markdown page---# Title
This is my page, written in **Markdown.**
```

   Read more about [Markdown](https://docs.astro.build/en/guides/markdown-content/) in Astro.

## HTML Pages

[Section titled “HTML Pages”](#html-pages)

Files with the `.html` file extension can be placed in the `src/pages/` directory and used directly as pages on your site. Note that some key Astro features are not supported in [HTML Components](https://docs.astro.build/en/basics/astro-components/#html-components).

## Custom 404 Error Page

[Section titled “Custom 404 Error Page”](#custom-404-error-page)

For a custom 404 error page, you can create a `404.astro` or `404.md` file in `src/pages`.

This will build to a `404.html` page. Most [deploy services](https://docs.astro.build/en/guides/deploy/) will find and use it.

## Custom 500 Error Page

[Section titled “Custom 500 Error Page”](#custom-500-error-page)

For a custom 500 error page to show for pages that are [rendered on demand](https://docs.astro.build/en/guides/on-demand-rendering/), create the file `src/pages/500.astro`. This custom page is not available for prerendered pages.

If an error occurs rendering this page, your host’s default 500 error page will be shown to your visitor.

**Added in:** `astro@4.10.3`

During development, if you have a `500.astro`, the error thrown at runtime is logged in your terminal, as opposed to being shown in the error overlay.

### error

[Section titled “error”](#error)

**Added in:** `astro@4.11.0`

`src/pages/500.astro` is a special page that is automatically passed an `error` prop for any error thrown during rendering. This allows you to use the details of an error (e.g. from a page, from middleware, etc.) to display information to your visitor.

The `error` prop’s data type can be anything, which may affect how you type or use the value in your code:

 src/pages/500.astro

```
---interface Props {  error: unknown;}
const { error } = Astro.props;---<div>{error instanceof Error ? error.message : "Unknown error"}</div>
```

To avoid leaking sensitive information when displaying content from the `error` prop, consider evaluating the error first, and returning appropriate content based on the error thrown. For example, you should avoid displaying the error’s stack as it contains information about how your code is structured on the server.

## Page Partials

[Section titled “Page Partials”](#page-partials)

**Added in:** `astro@3.4.0`

Partials are page components located within `src/pages/` that are not intended to render as full pages.

Like components located outside of this folder, these files do not automatically include the `<!DOCTYPE html>` declaration, nor any `<head>` content such as scoped styles and scripts.

However, because they are located in the special `src/pages/` directory, the generated HTML is available at a URL corresponding to its file path. This allows a rendering library (e.g. [htmx](https://htmx.org/), [Stimulus](https://stimulus.hotwired.dev/), [jQuery](https://jquery.com/)) to access it on the client and load sections of HTML dynamically on a page without a browser refresh or page navigation.

Partials, when combined with a rendering library, provide an alternative to [Astro islands](https://docs.astro.build/en/concepts/islands/) and [<script>tags](https://docs.astro.build/en/guides/client-side-scripts/) for building dynamic content in Astro.

Page files that can export a value for [partial](https://docs.astro.build/en/reference/routing-reference/#partial) (e.g. `.astro` and `.mdx`, but not `.md`) can be marked as partials.

 src/pages/partial.astro

```
---export const partial = true;---<li>I'm a partial!</li>
```

### Using with a library

[Section titled “Using with a library”](#using-with-a-library)

Partials are used to dynamically update a section of a page using a library such as [htmx](https://htmx.org/).

The following example shows an `hx-post` attribute set to a partial’s URL. The content from the partial page will be used to update the targeted HTML element on this page.

 src/pages/index.astro

```
<html>  <head>    <title>My page</title>    <script src="https://unpkg.com/htmx.org@1.9.6"      integrity="sha384-FhXw7b6AlE/jyjlZH5iHa/tTe9EpJ1Y55RjcgPbjeWMskSxZt1v9qkxLJWNJaGni"      crossorigin="anonymous"></script>  </head>  <body>    <section>      <div id="parent-div">Target here</div>
      <button hx-post="/partials/clicked/"        hx-trigger="click"        hx-target="#parent-div"        hx-swap="innerHTML"      >        Click Me!      </button>    </section>  </body></html>
```

The `.astro` partial must exist at the corresponding file path, and include an export defining the page as a partial:

 src/pages/partials/clicked.astro

```
---export const partial = true;---<div>I was clicked!</div>
```

See the [htmx documentation](https://htmx.org/docs/) for more details on using htmx.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Layouts

> An introduction to layouts in Astro.

# Layouts

**Layouts** are [Astro components](https://docs.astro.build/en/basics/astro-components/) used to provide a reusable UI structure, such as a page template.

We conventionally use the term “layout” for Astro components that provide common UI elements shared across pages such as headers, navigation bars, and footers. A typical Astro layout component provides [Astro, Markdown or MDX pages](https://docs.astro.build/en/basics/astro-pages/) with:

- a **page shell** (`<html>`, `<head>` and `<body>` tags)
- a [<slot />](https://docs.astro.build/en/basics/astro-components/#slots) to specify where individual page content should be injected.

But, there is nothing special about a layout component! They can [accept props](https://docs.astro.build/en/basics/astro-components/#component-props) and [import and use other components](https://docs.astro.build/en/basics/astro-components/#component-structure) like any other Astro component. They can include [UI frameworks components](https://docs.astro.build/en/guides/framework-components/) and [client-side scripts](https://docs.astro.build/en/guides/client-side-scripts/). They do not even have to provide a full page shell, and can instead be used as partial UI templates.

However, if a layout component does contain a page shell, its `<html>` element must be the parent of all other elements in the component.

Layout components are commonly placed in a `src/layouts` directory in your project for organization, but this is not a requirement; you can choose to place them anywhere in your project. You can even colocate layout components alongside your pages by [prefixing the layout names with_](https://docs.astro.build/en/guides/routing/#excluding-pages).

## Sample Layout

[Section titled “Sample Layout”](#sample-layout) src/layouts/MySiteLayout.astro

```
---import BaseHead from '../components/BaseHead.astro';import Footer from '../components/Footer.astro';const { title } = Astro.props;---<html lang="en">  <head>    <meta charset="utf-8">    <meta name="viewport" content="width=device-width, initial-scale=1">    <BaseHead title={title}/>  </head>  <body>    <nav>      <a href="#">Home</a>      <a href="#">Posts</a>      <a href="#">Contact</a>    </nav>    <h1>{title}</h1>    <article>      <slot />     </article>    <Footer />  </body>  <style>    h1 {      font-size: 2rem;    }  </style></html>
```

 src/pages/index.astro

```
---import MySiteLayout from '../layouts/MySiteLayout.astro';---<MySiteLayout title="Home Page">  <p>My page content, wrapped in a layout!</p></MySiteLayout>
```

   Learn more about [slots](https://docs.astro.build/en/basics/astro-components/#slots).

## Using TypeScript with layouts

[Section titled “Using TypeScript with layouts”](#using-typescript-with-layouts)

Any Astro layout can be modified to introduce type safety & autocompletion by providing the types for your props:

 src/components/MyLayout.astro

```
---interface Props {  title: string;  description: string;  publishDate: string;  viewCount: number;}const { title, description, publishDate, viewCount } = Astro.props;---<html lang="en">  <head>    <meta charset="UTF-8">    <meta name="description" content={description}>    <title>{title}</title>  </head>  <body>    <header>      <p>Published on {publishDate}</p>      <p>Viewed by {viewCount} folks</p>    </header>    <main>      <slot />    </main>  </body></html>
```

## Markdown Layouts

[Section titled “Markdown Layouts”](#markdown-layouts)

Page layouts are especially useful for individual Markdown pages which otherwise would not have any page formatting.

Astro provides a special `layout` frontmatter property intended for [individual.mdfiles located withinsrc/pages/using file-based routing](https://docs.astro.build/en/guides/markdown-content/#individual-markdown-pages) to specify which `.astro` component to use as the page layout. This component allows you to provide `<head>` content like meta tags (e.g. `<meta charset="utf-8">`) and styles for the Markdown page. By default, this specified component can automatically access data from the Markdown file.

This is not recognized as a special property when using [content collections](https://docs.astro.build/en/guides/content-collections/) to query and render your content.

 src/pages/page.md

```
---layout: ../layouts/BlogPostLayout.astrotitle: "Hello, World!"author: "Matthew Phillips"date: "09 Aug 2022"---All frontmatter properties are available as props to an Astro layout component.
The `layout` property is the only special one provided by Astro.
You can use it in Markdown files located within `src/pages/`.
```

A typical layout for a Markdown page includes:

1. The `frontmatter` prop to access the Markdown page’s frontmatter and other data.
2. A default [<slot />](https://docs.astro.build/en/basics/astro-components/#slots) to indicate where the page’s Markdown content should be rendered.

 src/layouts/BlogPostLayout.astro

```
---// 1. The frontmatter prop gives access to frontmatter and other dataconst { frontmatter } = Astro.props;---<html>  <head>        <meta name="viewport" content="width=device-width, initial-scale=1">    <meta charset="utf-8">    <title>{frontmatter.title}</title>  </head>  <body>        <h1>{frontmatter.title} by {frontmatter.author}</h1>        <slot />    <p>Written on: {frontmatter.date}</p>  </body></html>
```

You can set a layout’s [Propstype](https://docs.astro.build/en/guides/typescript/#component-props) with the `MarkdownLayoutProps` helper:

 src/layouts/BlogPostLayout.astro

```
---import type { MarkdownLayoutProps } from 'astro';
type Props = MarkdownLayoutProps<{  // Define frontmatter props here  title: string;  author: string;  date: string;}>;
// Now, `frontmatter`, `url`, and other Markdown layout properties// are accessible with type safetyconst { frontmatter, url } = Astro.props;---<html>  <head>    <meta charset="utf-8">    <link rel="canonical" href={new URL(url, Astro.site).pathname}>    <title>{frontmatter.title}</title>  </head>  <body>    <h1>{frontmatter.title} by {frontmatter.author}</h1>    <slot />    <p>Written on: {frontmatter.date}</p>  </body></html>
```

### Markdown Layout Props

[Section titled “Markdown Layout Props”](#markdown-layout-props)

A Markdown layout will have access to the following information via `Astro.props`:

- **file** - The absolute path of this file (e.g. `/home/user/projects/.../file.md`).
- **url** - The URL of the page (e.g. `/en/guides/markdown-content`).
- **frontmatter** - All frontmatter from the Markdown or MDX document.
  - **frontmatter.file** - The same as the top-level `file` property.
  - **frontmatter.url** - The same as the top-level `url` property.
- **headings** - A list of headings (`h1 -> h6`) in the Markdown or MDX document with associated metadata. This list follows the type: `{ depth: number; slug: string; text: string }[]`.
- **rawContent()** - A function that returns the raw Markdown document as a string.
- **compiledContent()** - An async function that returns the Markdown document compiled to an HTML string.

### Importing Layouts Manually (MDX)

[Section titled “Importing Layouts Manually (MDX)”](#importing-layouts-manually-mdx)

You can also use the special Markdown layout property in the frontmatter of MDX files to pass `frontmatter` and `headings` props directly to a specified layout component in the same way.

To pass information to your MDX layout that does not (or cannot) exist in your frontmatter, you can instead import and use a `<Layout />` component. This works like any other Astro component, and will not receive any props automatically. Pass it any necessary props directly:

 src/pages/posts/first-post.mdx

```
---layout: ../../layouts/BaseLayout.astrotitle: 'My first MDX post'publishDate: '21 September 2022'---import BaseLayout from '../../layouts/BaseLayout.astro';
export function fancyJsHelper() {  return "Try doing that with YAML!";}
<BaseLayout title={frontmatter.title} fancyJsHelper={fancyJsHelper}>  Welcome to my new Astro blog, using MDX!</BaseLayout>
```

Then, your values are available to you through `Astro.props` in your layout, and your MDX content will be injected into the page where your `<slot />` component is written:

 src/layouts/BaseLayout.astro

```
---const { title, fancyJsHelper } = Astro.props;---<html>  <head>        <meta charset="utf-8">  </head>  <body>        <h1>{title}</h1>    <slot />     <p>{fancyJsHelper()}</p>      </body></html>
```

When using any layout (either through the frontmatter `layout` property or by importing a layout), you must include the `<meta charset="utf-8">` tag in your layout as Astro will no longer add it automatically to your MDX page.

   Learn more about Astro’s Markdown and MDX support in our [Markdown guide](https://docs.astro.build/en/guides/markdown-content/).

## Nesting Layouts

[Section titled “Nesting Layouts”](#nesting-layouts)

Layout components do not need to contain an entire page worth of HTML. You can break your layouts into smaller components, and combine layout components to create even more flexible, page templates. This pattern is useful when you want to share some code across multiple layouts.

For example, a `BlogPostLayout.astro` layout component could style a post’s title, date and author. Then, a site-wide `BaseLayout.astro` could handle the rest of your page template, like navigation, footers, SEO meta tags, global styles, and fonts. You can also pass props received from your post to another layout, just like any other nested component.

 src/layouts/BlogPostLayout.astro

```
---import BaseLayout from './BaseLayout.astro';const { frontmatter } = Astro.props;---<BaseLayout url={frontmatter.url}>  <h1>{frontmatter.title}</h1>  <h2>Post author: {frontmatter.author}</h2>  <slot /></BaseLayout>
```

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Project structure

> An introduction to the basic file structure of an Astro project.

# Project structure

Your new Astro project generated from the `create astro` CLI wizard already includes some files and folders. Others, you will create yourself and add to Astro’s existing file structure.

Here’s how an Astro project is organized, and some files you will find in your new project.

## Directories and Files

[Section titled “Directories and Files”](#directories-and-files)

Astro leverages an opinionated folder layout for your project. Every Astro project root should include the following directories and files:

- `src/*` - Your project source code (components, pages, styles, images, etc.)
- `public/*` - Your non-code, unprocessed assets (fonts, icons, etc.)
- `package.json` - A project manifest.
- `astro.config.mjs` - An Astro configuration file. (recommended)
- `tsconfig.json` - A TypeScript configuration file. (recommended)

### Example Project Tree

[Section titled “Example Project Tree”](#example-project-tree)

A common Astro project directory might look like this:

- Directorypublic/
  - robots.txt
  - favicon.svg
  - my-cv.pdf
- Directorysrc/
  - Directoryblog/
    - post1.md
    - post2.md
    - post3.md
  - Directorycomponents/
    - Header.astro
    - Button.jsx
  - Directoryimages/
    - image1.jpg
    - image2.jpg
    - image3.jpg
  - Directorylayouts/
    - PostLayout.astro
  - Directorypages/
    - Directoryposts/
      - [post].astro
    - about.astro
    - **index.astro**
    - rss.xml.js
  - Directorystyles/
    - global.css
  - content.config.ts
- astro.config.mjs
- package.json
- tsconfig.json

### src/

[Section titled “src/”](#src)

The `src/` folder is where most of your project source code lives. This includes:

- [Pages](https://docs.astro.build/en/basics/astro-pages/)
- [Layouts](https://docs.astro.build/en/basics/layouts/)
- [Astro components](https://docs.astro.build/en/basics/astro-components/)
- [UI framework components (React, etc.)](https://docs.astro.build/en/guides/framework-components/)
- [Styles (CSS, Sass)](https://docs.astro.build/en/guides/styling/)
- [Markdown](https://docs.astro.build/en/guides/markdown-content/)
- [Images to be optimized and processed by Astro](https://docs.astro.build/en/guides/images/)

Astro processes, optimizes, and bundles your `src/` files to create the final website that is shipped to the browser.  Unlike the static `public/` directory, your `src/` files are built and handled for you by Astro.

Some files (like Astro components) are not even sent to the browser as written but are instead rendered to static HTML. Other files (like CSS) are sent to the browser but may be optimized or bundled with other CSS files for performance.

### src/pages

[Section titled “src/pages”](#srcpages)

Pages routes are created for your site by adding [supported file types](https://docs.astro.build/en/basics/astro-pages/#supported-page-files) to this directory.

### src/components

[Section titled “src/components”](#srccomponents)

**Components** are reusable units of code for your HTML pages. These could be [Astro components](https://docs.astro.build/en/basics/astro-components/), or [UI framework components](https://docs.astro.build/en/guides/framework-components/) like React or Vue.  It is common to group and organize all of your project components together in this folder.

This is a common convention in Astro projects, but it is not required. Feel free to organize your components however you like!

### src/layouts

[Section titled “src/layouts”](#srclayouts)

[Layouts](https://docs.astro.build/en/basics/layouts/) are Astro components that define the UI structure shared by one or more [pages](https://docs.astro.build/en/basics/astro-pages/).

Just like `src/components`, this directory is a common convention but not required.

### src/styles

[Section titled “src/styles”](#srcstyles)

It is a common convention to store your CSS or Sass files in a `src/styles` directory, but this is not required. As long as your styles live somewhere in the `src/` directory and are imported correctly, Astro will handle and optimize them.

### public/

[Section titled “public/”](#public)

The `public/` directory is for files and assets in your project that do not need to be processed during Astro’s build process. The files in this folder will be copied into the build folder untouched, and then your site will be built.

This behavior makes `public/` ideal for common assets that do not require any processing, like some images and fonts, or special files such as `robots.txt` and `manifest.webmanifest`.

You can place CSS and JavaScript in your `public/` directory, but be aware that those files will not be bundled or optimized in your final build.

### package.json

[Section titled “package.json”](#packagejson)

This is a file used by JavaScript package managers to manage your dependencies. It also defines the scripts that are commonly used to run Astro (ex: `npm run dev`, `npm run build`).

There are [two kinds of dependencies](https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file) you can specify in a `package.json`: `dependencies` and `devDependencies`. In most cases, these work the same: Astro needs all dependencies at build time, and your package manager will install both. We recommend putting all of your dependencies in `dependencies` to start, and only use `devDependencies` if you find a specific need to do so.

For help creating a new `package.json` file for your project, check out the [manual setup](https://docs.astro.build/en/install-and-setup/#manual-setup) instructions.

### astro.config.mjs

[Section titled “astro.config.mjs”](#astroconfigmjs)

This file is generated in every starter template and includes configuration options for your Astro project. Here you can specify integrations to use, build options, server options, and more.

Astro supports several file formats for its JavaScript configuration file: `astro.config.js`, `astro.config.mjs`, `astro.config.cjs` and `astro.config.ts`. We recommend using `.mjs` in most cases or `.ts` if you want to write TypeScript in your config file.

TypeScript config file loading is handled using [tsm](https://github.com/lukeed/tsm) and will respect your project’s `tsconfig` options.

See the [configuration reference](https://docs.astro.build/en/reference/configuration-reference/) for complete details.

### tsconfig.json

[Section titled “tsconfig.json”](#tsconfigjson)

This file is generated in every starter template and includes TypeScript configuration options for your Astro project. Some features (like npm package imports) aren’t fully supported in the editor without a `tsconfig.json` file.

See the [TypeScript Guide](https://docs.astro.build/en/guides/typescript/) for details on setting configurations.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)
