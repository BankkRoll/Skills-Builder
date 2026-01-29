# Scripts and event handling and more

# Scripts and event handling

> How to add client-side interactivity to Astro components using native browser JavaScript APIs.

# Scripts and event handling

You can send JavaScript to the browser and add functionality to your Astro components using `<script>` tags in the component template.

Scripts add interactivity to your site, such as handling events or updating content dynamically, without the need for a [UI framework](https://docs.astro.build/en/guides/framework-components/) like React, Svelte, or Vue. This avoids the overhead of shipping framework JavaScript and doesn’t require you to know any additional framework to create a full-featured website or application.

## Client-Side Scripts

[Section titled “Client-Side Scripts”](#client-side-scripts)

Scripts can be used to add event listeners, send analytics data, play animations, and everything else JavaScript can do on the web.

Astro automatically enhances the HTML standard `<script>` tag with bundling, TypeScript, and more. See [how astro processes scripts](#script-processing) for more details.

 src/components/ConfettiButton.astro

```
<button data-confetti-button>Celebrate!</button>
<script>  // Import from npm package.  import confetti from 'canvas-confetti';
  // Find our component DOM on the page.  const buttons = document.querySelectorAll('[data-confetti-button]');
  // Add event listeners to fire confetti when a button is clicked.  buttons.forEach((button) => {    button.addEventListener('click', () => confetti());  });</script>
```

   See [when your scripts will not be processed](#unprocessed-scripts) to troubleshoot script behavior, or to learn how to opt-out of this processing intentionally.

## Script processing

[Section titled “Script processing”](#script-processing)

By default, Astro processes `<script>` tags that contain no attributes (other than `src`) in the following ways:

- **TypeScript support:** All scripts are TypeScript by default.
- **Import bundling:** Import local files or npm modules, which will be bundled together.
- **Type Module:** Processed scripts become [type="module"](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) automatically.
- **Deduplication:** If a component that contains a `<script>` is used multiple times on a page, the script will only be included once.
- **Automatic inlining:** If the script is small enough, Astro will inline it directly into the HTML to reduce the number of requests.

 src/components/Example.astro

```
<script>  // Processed! Bundled! TypeScript!  // Importing local scripts and from npm packages works.</script>
```

### Unprocessed scripts

[Section titled “Unprocessed scripts”](#unprocessed-scripts)

Astro will not process a `<script>` tag if it has any attribute other than `src`.

You can add the [is:inline](https://docs.astro.build/en/reference/directives-reference/#isinline) directive to intentionally opt out of processing for a script.

 src/components/InlineScript.astro

```
<script is:inline>  // Will be rendered into the HTML exactly as written!  // Not transformed: no TypeScript and no import resolution by Astro.  // If used inside a component, this code is duplicated for each instance.</script>
```

### Include JavaScript files on your page

[Section titled “Include JavaScript files on your page”](#include-javascript-files-on-your-page)

You may want to write your scripts as separate `.js`/`.ts` files or need to reference an external script on another server. You can do this by referencing these in a `<script>` tag’s `src` attribute.

#### Import local scripts

[Section titled “Import local scripts”](#import-local-scripts)

**When to use this:** when your script lives inside of `src/`.

Astro will process these scripts according to the [script processing rules](#script-processing).

 src/components/LocalScripts.astro

```
<script src="../scripts/local.js"></script>
<script src="./script-with-types.ts"></script>
```

#### Load external scripts

[Section titled “Load external scripts”](#load-external-scripts)

**When to use this:** when your JavaScript file lives inside of `public/` or on a CDN.

To load scripts outside of your project’s `src/` folder, include the `is:inline` directive. This approach skips the JavaScript processing, bundling, and optimizations that are provided by Astro when you import scripts as described above.

 src/components/ExternalScripts.astro

```
<script is:inline src="/my-script.js"></script>
<script is:inline src="https://my-analytics.com/script.js"></script>
```

## Common script patterns

[Section titled “Common script patterns”](#common-script-patterns)

### Handleonclickand other events

[Section titled “Handle onclick and other events”](#handle-onclick-and-other-events)

Some UI frameworks use custom syntax for event handling like `onClick={...}` (React/Preact) or `@click="..."` (Vue). Astro follows standard HTML more closely and does not use custom syntax for events.

Instead, you can use [addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) in a `<script>` tag to handle user interactions.

 src/components/AlertButton.astro

```
<button class="alert">Click me!</button>
<script>  // Find all buttons with the `alert` class on the page.  const buttons = document.querySelectorAll('button.alert');
  // Handle clicks on each button.  buttons.forEach((button) => {    button.addEventListener('click', () => {      alert('Button was clicked!');    });  });</script>
```

If you have multiple `<AlertButton />` components on a page, Astro will not run the script multiple times. Scripts are bundled and only included once per page. Using `querySelectorAll` ensures that this script attaches the event listener to every button with the `alert` class found on the page.

### Web components with custom elements

[Section titled “Web components with custom elements”](#web-components-with-custom-elements)

You can create your own HTML elements with custom behavior using the Web Components standard. Defining a [custom element](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements) in a `.astro` component allows you to build interactive components without needing a UI framework library.

In this example, we define a new `<astro-heart>` HTML element that tracks how many times you click the heart button and updates the `<span>` with the latest count.

 src/components/AstroHeart.astro

```
<astro-heart>  <button aria-label="Heart">💜</button> × <span>0</span></astro-heart>
<script>  // Define the behaviour for our new type of HTML element.  class AstroHeart extends HTMLElement {    connectedCallback() {      let count = 0;
      const heartButton = this.querySelector('button');      const countSpan = this.querySelector('span');
      // Each time the button is clicked, update the count.      heartButton.addEventListener('click', () => {        count++;        countSpan.textContent = count.toString();      });    }  }
  // Tell the browser to use our AstroHeart class for <astro-heart> elements.  customElements.define('astro-heart', AstroHeart);</script>
```

There are two advantages to using a custom element here:

1. Instead of searching the whole page using `document.querySelector()`, you can use `this.querySelector()`, which only searches within the current custom element instance. This makes it easier to work with only the children of one component instance at a time.
2. Although a `<script>` only runs once, the browser will run our custom element’s `connectedCallback()` method each time it finds `<astro-heart>` on the page. This means you can safely write code for one component at a time, even if you intend to use this component multiple times on a page.

   You can learn more about custom elements in [web.dev’s Reusable Web Components guide](https://web.dev/custom-elements-v1/) and [MDN’s introduction to custom elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements).

### Pass frontmatter variables to scripts

[Section titled “Pass frontmatter variables to scripts”](#pass-frontmatter-variables-to-scripts)

In Astro components, the code in [the frontmatter](https://docs.astro.build/en/basics/astro-components/#the-component-script) (between the `---` fences) runs on the server and is not available in the browser.

To pass server-side variables to client-side scripts, store them in [data-*attributes](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) on HTML elements. Scripts can then access these values using the `dataset` property.

In this example component, a `message` prop is stored in a `data-message` attribute, so the custom element can read `this.dataset.message` and get the value of the prop in the browser.

 src/components/AstroGreet.astro

```
---const { message = 'Welcome, world!' } = Astro.props;---
<astro-greet data-message={message}>  <button>Say hi!</button></astro-greet>
<script>  class AstroGreet extends HTMLElement {    connectedCallback() {      // Read the message from the data attribute.      const message = this.dataset.message;      const button = this.querySelector('button');      button.addEventListener('click', () => {        alert(message);      });    }  }
  customElements.define('astro-greet', AstroGreet);</script>
```

Now we can use our component multiple times and be greeted by a different message for each one.

 src/pages/example.astro

```
---import AstroGreet from '../components/AstroGreet.astro';---
<AstroGreet />
<AstroGreet message="Lovely day to build components!" /><AstroGreet message="Glad you made it! 👋" />
```

### Combining scripts and UI Frameworks

[Section titled “Combining scripts and UI Frameworks”](#combining-scripts-and-ui-frameworks)

Elements rendered by a UI framework may not be available yet when a `<script>` tag executes. If your script also needs to handle [UI framework components](https://docs.astro.build/en/guides/framework-components/), using a custom element is recommended.

 Learn     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# ApostropheCMS & Astro

> Edit content on the page in your Astro project using Apostrophe as your CMS.

# ApostropheCMS & Astro

[ApostropheCMS](https://apostrophecms.com/) is a content management system supporting on-page editing in Astro.

## Integrating with Astro

[Section titled “Integrating with Astro”](#integrating-with-astro)

In this section, you will use the [Apostrophe integration](https://apostrophecms.com/extensions/astro-integration) to connect ApostropheCMS to Astro.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

To get started, you will need to have the following:

1. **An on-demand rendered Astro project** with the [Node.js adapter](https://docs.astro.build/en/guides/integrations-guide/node/) installed and `output: 'server'` configured - If you don’t have an Astro project yet, our [installation guide](https://docs.astro.build/en/install-and-setup/) will get you up and running in no time.
2. **An ApostropheCMS project with a configured environment variable calledAPOS_EXTERNAL_FRONT_KEY** - This environment variable can be set to any random string. If you don’t have an ApostropheCMS project yet, the [installation guide](https://docs.apostrophecms.org/guide/development-setup.html) will get one setup quickly. We highly recommend using the [Apostrophe CLI tool](https://apostrophecms.com/extensions/apos-cli) to facilitate this.

### Setting up project communication

[Section titled “Setting up project communication”](#setting-up-project-communication)

Your Astro project needs to have an `APOS_EXTERNAL_FRONT_KEY` environment variable set to the same value as the one in your ApostropheCMS project to allow communication between the two. This shared key acts as a means to verify requests between the frontend (Astro) and the backend (ApostropheCMS).

Create a `.env` file in the root of your Astro project with the following variable:

 .env

```
APOS_EXTERNAL_FRONT_KEY='RandomStrongString'
```

Your root directory should now include this new file:

- Directorysrc/
  - …
- **.env**
- astro.config.mjs
- package.json

### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

To connect Astro with your ApostropheCMS project, install the official Apostrophe integration in your Astro project using the command below for your preferred package manager.

- [npm](#tab-panel-2747)
- [pnpm](#tab-panel-2748)
- [Yarn](#tab-panel-2749)

   Terminal window

```
npm install @apostrophecms/apostrophe-astro vite @astrojs/node
```

   Terminal window

```
pnpm add @apostrophecms/apostrophe-astro vite @astrojs/node
```

   Terminal window

```
yarn add @apostrophecms/apostrophe-astro vite @astrojs/node
```

### Configuring Astro

[Section titled “Configuring Astro”](#configuring-astro)

Configure both the `apostrophe-astro` integration and `vite` in your `astro.config.mjs` file.

The following example provides the base URL of your Apostrophe instance and paths to folders in your project to map between the ApostropheCMS [widgets](https://docs.apostrophecms.org/guide/core-widgets.html) and [page template](https://docs.apostrophecms.org/guide/pages.html) types and your Astro project. It also configures Vite’s server-side rendering.

 astro.config.mjs

```
import { defineConfig } from 'astro/config';import node from '@astrojs/node';import apostrophe from '@apostrophecms/apostrophe-astro';import { loadEnv } from 'vite';
const env = loadEnv("", process.cwd(), 'APOS');
export default defineConfig({  output: 'server',  adapter: node({    mode: 'standalone'  }),  integrations: [    apostrophe({      aposHost: 'http://localhost:3000',      widgetsMapping: './src/widgets',      templatesMapping: './src/templates'    })  ],  vite: {    ssr: {      // Do not externalize the @apostrophecms/apostrophe-astro plugin, we need      // to be able to use virtual: URLs there      noExternal: [ '@apostrophecms/apostrophe-astro' ],    },    define: {      'process.env.APOS_EXTERNAL_FRONT_KEY': JSON.stringify(env.APOS_EXTERNAL_FRONT_KEY),      'process.env.APOS_HOST': JSON.stringify(env.APOS_HOST)    }  }});
```

For complete configuration options and explanations, see the [apostrophe-astrodocumentation](https://apostrophecms.com/extensions/astro-integration#configuration-astro).

### Connecting ApostropheCMS widgets to Astro components

[Section titled “Connecting ApostropheCMS widgets to Astro components”](#connecting-apostrophecms-widgets-to-astro-components)

ApostropheCMS widgets are blocks of structured content that can be added to the page such as layout columns, images, and text blocks. You will need to create an Astro component for each widget in your Apostrophe project, plus a file to map those components to the corresponding Apostrophe widget.

Create a new folder at `src/widgets/` for your Astro components and the mapping file, `index.js`.

Mapped components located in this folder receive a `widget` property containing your widget’s schema fields, and any custom props, through `Astro.props`. These values are then available for on-page editing.

The following example shows a `RichTextWidget.astro` component accessing the content from its corresponding ApostropheCMS widget to allow for in-context editing:

 src/widgets/RichTextWidget.astro

```
---const { widget } = Astro.props;const { content } = widget;---<Fragment set:html={ content }></Fragment>
```

Some standard Apostrophe widgets, such as images and videos, require **placeholders** because they do not contain editable content by default. The following example creates a standard `ImageWidget.astro` component that sets the `src` value conditionally to either the value of the `aposPlaceholder` image passed by the widget, a fallback image from the Astro project, or the image selected by the content manager using the Apostrophe `attachment` helper:

 src/widgets/ImageWidget.astro

```
---const { widget } = Astro.props;const placeholder = widget?.aposPlaceholder;const src = placeholder ?  '/images/image-widget-placeholder.jpg' :  widget?._image[0]?.attachment?._urls['full'];---<style>  .img-widget {    width: 100%;  }</style><img class="img-widget" {src} />
```

For more examples, see [theastro-frontendstarter project widget examples](https://github.com/apostrophecms/astro-frontend/tree/main/src/widgets).

Each `.astro` component must be mapped to the corresponding core Apostrophe widget in `src/widgets/index.js`.

The example below adds the previous two components to this file:

 src/widgets/index.js

```
import RichTextWidget from './RichTextWidget.astro';import ImageWidget from './ImageWidget.astro';
const widgetComponents = {  '@apostrophecms/rich-text': RichTextWidget,  '@apostrophecms/image': ImageWidget};
export default widgetComponents;
```

See [the ApostropheCMS documentation](https://apostrophecms.com/extensions/astro-integration) for naming conventions for standard, pro, and custom-project-level widgets

The project directory should now look like this:

- Directorysrc/
  - Directorywidgets/
    - **index.js**
    - **ImageWidget.astro**
    - **RichTextWidget.astro**
- .env
- astro.config.mjs
- package.json

### Adding page types

[Section titled “Adding page types”](#adding-page-types)

Much like widgets, any page type template in your ApostropheCMS project needs to have a corresponding template component in your Astro project. You will also need a file that maps the Apostrophe page types to individual components.

Create a new folder at `src/templates/` for your Astro components and the mapping file, `index.js`. Mapped components located in this folder receive a `page` property containing the schema fields of your page, and any custom props, through `Astro.props`. These components can also access an `AposArea` component to render Apostrophe areas.

The following example shows a `HomePage.astro` component rendering a page template from its corresponding `home-page` ApostropheCMS page type, including an area schema field named `main`:

 src/templates/HomePage.astro

```
---import AposArea from '@apostrophecms/apostrophe-astro/components/AposArea.astro';const { page, user, query } = Astro.props.aposData;const { main } = page;---
<section class="bp-content">  <h1>{ page.title }</h1>  <AposArea area={main} /></section>
```

Each `.astro` component must be mapped to the corresponding core Apostrophe page type in `src/templates/index.js`.

The example below adds the previous `HomePage.astro` component to this file:

 src/templates/index.js

```
import HomePage from './HomePage.astro';
const templateComponents = {  '@apostrophecms/home-page': HomePage};
export default templateComponents;
```

See [the ApostropheCMS documentation](https://apostrophecms.com/extensions/astro-integration/#how-apostrophe-template-names-work) for template naming conventions, including special pages and piece page types.

The project directory should now look like this:

- Directorysrc/
  - Directorywidgets/
    - index.js
    - ImageWidget.astro
    - RichTextWidget.astro
  - Directorytemplates/
    - **HomePage.astro**
    - **index.js**
- .env
- astro.config.mjs
- package.json

### Creating the […slug.astro] component and fetching Apostrophe data

[Section titled “Creating the […slug.astro] component and fetching Apostrophe data”](#creating-the-slugastro-component-and-fetching-apostrophe-data)

Since Apostrophe is responsible for connecting URLs to content, including creating new content and pages on the fly, you will only need one top-level Astro page component: the `[...slug].astro` route.

The following example shows a minimal `[...slug].astro` component:

 src/pages/[...slug].astro

```
---import aposPageFetch from '@apostrophecms/apostrophe-astro/lib/aposPageFetch.js';import AposLayout from '@apostrophecms/apostrophe-astro/components/layouts/AposLayout.astro';import AposTemplate from '@apostrophecms/apostrophe-astro/components/AposTemplate.astro';
const aposData = await aposPageFetch(Astro.request);const bodyClass = `myclass`;
if (aposData.redirect) {  return Astro.redirect(aposData.url, aposData.status);}if (aposData.notFound) {  Astro.response.status = 404;}---<AposLayout title={aposData.page?.title} {aposData} {bodyClass}>    <Fragment slot="standardHead">      <meta name="description" content={aposData.page?.seoDescription} />      <meta name="viewport" content="width=device-width, initial-scale=1" />      <meta charset="UTF-8" />    </Fragment>    <AposTemplate {aposData} slot="main"/></AposLayout>
```

See [the ApostropheCMS documentation](https://apostrophecms.com/extensions/astro-integration#creating-the-slugastro-component-and-fetching-apostrophe-data) for additional templating options, including slots available in the `AposTemplate` component.

## Making a blog with Astro and ApostropheCMS

[Section titled “Making a blog with Astro and ApostropheCMS”](#making-a-blog-with-astro-and-apostrophecms)

With the integration set up, you can now create a blog with Astro and ApostropheCMS. Your blog will use an Apostrophe piece, a stand-alone content type that can be included on any page, and a piece page type, a specialized page type that is used for displaying those pieces either individually or collectively.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

1. **An ApostropheCMS project with the Apostrophe CLI tool installed** - You can create a new project or use an existing one. However, this tutorial will only show how to create a blog piece and piece page type. You will have to integrate any other existing project code independently. If you don’t have the CLI tool installed, consult the [Apostrophe CLI installation instructions](https://docs.apostrophecms.org/guide/setting-up.html#the-apostrophe-cli-tool).
2. **An Astro project integrated with ApostropheCMS** - To create a project from scratch, see [integrating with Astro](#integrating-with-astro) for instructions on how to set up the integration, or use the [astro-frontend](https://github.com/apostrophecms/astro-frontend) starter project.

### Creating a blog piece and piece page type

[Section titled “Creating a blog piece and piece page type”](#creating-a-blog-piece-and-piece-page-type)

To create your blog piece and piece page type for their display, navigate to the root of your ApostropheCMS project in your terminal. Use the ApostropheCMS CLI tool to create the new piece and piece page type with the following command:

 Terminal window

```
apos add piece blog --page
```

This will create two new modules in your project, one for the blog piece type and one for the corresponding piece page type. Next, open the `app.js` file at the root of your ApostropheCMS project in your code editor and add your new modules.

 app.js

```
require('apostrophe')({  // other configuration options  modules: {    // other project modules    blog: {},    'blog-page': {}  }});
```

The `blog-page` module also needs to be added to the `@apostrophecms/page` module `types` option array so that it can be selected in the page creation modal. In your ApostropheCMS project, open the `modules/@apostrophecms/page/index.js` file and add the `blog-page`.

 modules/@apostrophecms/page/index.js

```
module.exports = {  options: {    types: [      {        name: '@apostrophecms/home-page',        label: 'Home'      },      // Any other project pages      {        name: 'blog-page',        label: 'Blog'      }    ]  }};
```

### Creating the blog schema

[Section titled “Creating the blog schema”](#creating-the-blog-schema)

In an ApostropheCMS project, editors are offered a set of input fields for adding content. Here is an example of a simple blog post that adds three input fields, an `authorName`, `publicationDate` and `content` area where content managers can add multiple widget instances. In this case, we are specifying they can add the image and rich-text widgets we created during the [integration setup](#connecting-apostrophecms-widgets-to-astro-components).

 modules/blog/index.js

```
module.exports = {  extend: '@apostrophecms/piece-type',  options: {    label: 'Blog',    // Additionally add a `pluralLabel` option if needed.  },  fields: {    add: {      authorName: {        type: 'string',        label: 'Author'      },      publicationDate: {        type: 'date',        label: 'Publication date'      },      content: {        type: 'area',        label: 'Content',        options: {          widgets: {            '@apostrophecms/rich-text': {},            '@apostrophecms/image': {}          }        }      }    },    group: {      basics: {        label: 'Basic',        fields: [ 'authorName', 'publicationDate', 'content' ]      }    }  }};
```

At this point, all the components coming from the ApostropheCMS project are set up. Start the local site from the command line using `npm run dev`, making sure to pass in the `APOS_EXTERNAL_FRONT_KEY` environment variable set to your selected string:

 Terminal window

```
APOS_EXTERNAL_FRONT_KEY='MyRandomString' npm run dev
```

### Displaying the blog posts

[Section titled “Displaying the blog posts”](#displaying-the-blog-posts)

To display a page with all the blog posts create a `BlogIndex.astro` component file in the `src/templates` directory of your Astro project and add the following code:

After fetching both the page and pieces data from the `aposData` prop, this component creates markup using both fields from the blog piece schema we created, but also from the `piece.title` and `piece._url` that is added to each piece by Apostrophe.

 src/templates/BlogIndex.astro

```
---import dayjs from 'dayjs';
const { page, pieces } = Astro.props.aposData;---
<section class="bp-content">  <h1>{ page.title }</h1>
  <h2>Blog Posts</h2>
  {pieces.map(piece => (    <h4>      Released On { dayjs(piece.publicationDate).format('MMMM D, YYYY') }    </h4>    <h3>      <a href={ piece._url }>{ piece.title }</a>    </h3>    <h4>{ piece.authorName }</h4>  ))}</section>
```

To display individual blog posts, create a `BlogShow.astro` file in the Astro project `src/templates` folder with the following code:

This component uses the `<AposArea>` component to display any widgets added to the `content` area and the `authorName` and `publicationDate` content entered into the fields of the same names.

 src/templates/BlogShow.astro

```
---import AposArea from '@apostrophecms/apostrophe-astro/components/AposArea.astro';import dayjs from 'dayjs';
const { page, piece } = Astro.props.aposData;const { main } = piece;---
<section class="bp-content">  <h1>{ piece.title }</h1>  <h3>Created by: { piece.authorName }  <h4>    Released On { dayjs(piece.publicationDate).format('MMMM D, YYYY') }  </h4>  <AposArea area={content} /></section>
```

Finally, these Astro components must be mapped to the corresponding ApostropheCMS page types. Open the Astro project `src/templates/index.js` file and modify it to contain the following code:

 src/templates/index.js

```
import HomePage from './HomePage.astro';import BlogIndexPage from './BlogIndexPage.astro';import BlogShowPage from './BlogShowPage.astro';
const templateComponents = {  '@apostrophecms/home-page': HomePage,  '@apostrophecms/blog-page:index': BlogIndexPage,  '@apostrophecms/blog-page:show': BlogShowPage};
export default templateComponents;
```

### Creating blog posts

[Section titled “Creating blog posts”](#creating-blog-posts)

Adding blog posts to your site is accomplished by using the ApostropheCMS content and management tools to create those posts and by publishing at least one index page to display them.

With the Astro dev server running, navigate to the login page located at [http://localhost:4321/login](http://localhost:4321/login) in your browser preview. Use the credentials that were added during the [creation of the ApostropheCMS project](https://docs.apostrophecms.org/guide/development-setup.html#creating-a-project) to log in as an administrator. Your ApostropheCMS project should still be running.

Once you are logged in, your browser will be redirected to the home page of your project and will display an admin bar at the top for editing content and managing your project.

To add your first blog post, click on the `Blogs` button in the admin bar to open the blog piece creation modal. Clicking on the `New Blog` button in the upper right will open an editing modal where you can add content. The `content` area field will allow you to add as many image and rich text widgets as you desire.

You can repeat this step and add as many posts as you want. You will also follow these steps every time you want to add a new post.

To publish a page for displaying all your posts, click on the `Pages` button in the admin bar. From the page tree modal click on the `New Page` button. In the `Type` dropdown in the right column select `Blog`. Add a title for the page and then click `Publish and View`. You will only need to do this once.

Any new blog posts that are created will be automatically displayed on this page. Individual blog posts can be displayed by clicking on the link created on the index page.

The `content` area of individual posts can be edited directly on the page by navigating to the post and clicking `edit` in the admin bar. Other fields can be edited by using the editing modal opened when clicking the `Blogs` menu item in the admin bar.

### Deploying your site

[Section titled “Deploying your site”](#deploying-your-site)

To deploy your website, you need to host both your Astro and ApostropheCMS projects.

For Astro, visit our [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

For the ApostropheCMS project, follow the instructions for your hosting type in our [hosting guide](https://docs.apostrophecms.org/guide/hosting.html). Finally, you’ll need to supply an `APOS_HOST` environment variable to the Astro project to reflect the correct URL where your ApostropheCMS site has been deployed.

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [Astro integration for ApostropheCMS](https://apostrophecms.com/extensions/astro-integration) - ApostropheCMS Astro plugin, integration guide and starter projects for both Apostrophe and Astro
- [Sample Astro project for use with ApostropheCMS](https://github.com/apostrophecms/astro-frontend) - A simple Astro project with several pages and Apostrophe widgets already created.
- [Sample ApostropheCMS starter-kit for use with Astro](https://apostrophecms.com/starter-kits/astro-integration-starter-kit) - An ApostropheCMS project with core page modifications for use with Astro.

## Community Resources

[Section titled “Community Resources”](#community-resources)

- [Integrating ApostropheCMS with Astro, Pt. 1](https://apostrophecms.com/blog/how-to-integrate-astro-with-apostrophecms-pt-1) by Antonello Zaini
- [Integrating ApostropheCMS with Astro, Pt. 2](https://apostrophecms.com/blog/how-to-integrate-astro-with-apostrophecms-pt-2) by Antonello Zaini
- [Show & Tell Live | Astro & Apostrophe](https://youtu.be/cwJhtJhAhwA?si=6iUU9EjidfdnOdCh)

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Builder.io & Astro

> Add content to your Astro project using Builder.io’s visual CMS

# Builder.io & Astro

[Builder.io](https://www.builder.io/) is a visual CMS that supports drag-and-drop content editing for building websites.

This recipe will show you how to connect your Builder space to Astro with zero client-side JavaScript.

## Prerequisites

[Section titled “Prerequisites”](#prerequisites)

To get started, you will need to have the following:

- **A Builder account and space** - If you don’t have an account yet, [sign up for free](https://www.builder.io/) and create a new space. If you already have a space with Builder, feel free to use it, but you will need to modify the code to match the model name (`blogpost`) and custom data fields.
- **A Builder API key** - This public key will be used to fetch your content from Builder. [Read Builder’s guide on how to find your key](https://www.builder.io/c/docs/using-your-api-key#finding-your-public-api-key).

## Setting up credentials

[Section titled “Setting up credentials”](#setting-up-credentials)

To add your Builder API key and your Builder model name to Astro, create a `.env` file in the root of your project (if one does not already exist) and add the following variables:

 .env

```
BUILDER_API_PUBLIC_KEY=YOUR_API_KEYBUILDER_BLOGPOST_MODEL='blogpost'
```

Now, you should be able to use this API key in your project.

If you would like to have IntelliSense for your environment variables, you can create a `env.d.ts` file in the `src/` directory and configure `ImportMetaEnv` like this:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly BUILDER_API_PUBLIC_KEY: string;}
```

Your project should now include these files:

- Directorysrc/
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json

   Learn more about [environment variables](https://docs.astro.build/en/guides/environment-variables/) and `.env` files in Astro.

## Making a blog with Astro and Builder

[Section titled “Making a blog with Astro and Builder”](#making-a-blog-with-astro-and-builder)

### Creating a model for a blog post

[Section titled “Creating a model for a blog post”](#creating-a-model-for-a-blog-post)

The instructions below create an Astro blog using a Builder model (Type: “Section”) called `blogpost` that contains two required text fields: `title` and `slug`.

In the Builder app create the model that will represent a blog post: go to the **Models** tab and click the **+ Create Model** button to create model with the following fields and values:

- **Type:** Section
- **Name:** “blogpost”
- **Description:** “This model is for a blog post”

In your new model use the **+ New Custom Field** button to create 2 new fields:

1. Text field
  - **Name:** “title”
  - **Required:** Yes
  - **Default value** “I forgot to give this a title”
  (leave the other parameters as their defaults)
2. Text field
  - **Name:** “slug”
  - **Required:** Yes
  - **Default value** “some-slugs-take-their-time”
  (leave the other parameters as their defaults)

Then click the **Save** button in the upper right.

### Setting up the preview

[Section titled “Setting up the preview”](#setting-up-the-preview)

To use Builder’s visual editor, create the page `src/pages/builder-preview.astro` that will render the special `<builder-component>`:

- Directorysrc/
  - Directorypages/
    - **builder-preview.astro**
  - env.d.ts
- .env
- astro.config.mjs
- package.json

Then add the following content:

 src/pages/builder-preview.astro

```
---const builderAPIpublicKey = import.meta.env.BUILDER_API_PUBLIC_KEY;const builderModel = import.meta.env.BUILDER_BLOGPOST_MODEL;---
<html lang="en">  <head>    <title>Preview for builder.io</title>  </head>  <body>    <header>This is your header</header>
    <builder-component model={builderModel} api-key={builderAPIpublicKey}    ></builder-component>    <script async src="https://cdn.builder.io/js/webcomponents"></script>
    <footer>This is your footer</footer>  </body></html>
```

In the above example, `<builder-component>` tells Builder where to insert the content from its CMS.

#### Setting the new route as the preview URL

[Section titled “Setting the new route as the preview URL”](#setting-the-new-route-as-the-preview-url)

1. Copy the full URL of your preview, including the protocol, to your clipboard (e.g. `https://{your host}/builder-preview`).
2. Go to the **Models** tab in your Builder space, pick the model you’ve created and paste the URL from step 1 into the **Preview URL** field. Make sure the URL is complete and includes the protocol, for example `https://`.
3. Click the **Save** button in the upper right.

#### Testing the preview URL setup

[Section titled “Testing the preview URL setup”](#testing-the-preview-url-setup)

1. Make sure your site is live (e.g. your dev server is running) and the `/builder-preview` route is working.
2. In your Builder space under the **Content** tab, click on **New** to create a new content entry for your `blogpost` model.
3. In the Builder editor that just opened, you should be able to see the `builder-preview.astro` page with a big **Add Block** in the middle.

### Creating a blog post

[Section titled “Creating a blog post”](#creating-a-blog-post)

1. In Builder’s visual editor, create a new content entry with the following values:
  - **title:** ‘First post, woohoo!’
  - **slug:** ‘first-post-woohoo’
2. Complete your post using the **Add Block** button and add a text field with some post content.
3. In the text field above the editor, give your entry a name. This is how it will be listed in the Builder app.
4. When you’re ready click the **Publish** button in the upper right corner.
5. Create as many posts as you like, ensuring that all content entries contain a `title` and a `slug` as well as some post content.

### Displaying a list of blog posts

[Section titled “Displaying a list of blog posts”](#displaying-a-list-of-blog-posts)

Add the following content to `src/pages/index.astro` in order to fetch and display a list of all post titles, each linking to its own page:

 src/pages/index.astro

```
---
const builderAPIpublicKey = import.meta.env.BUILDER_API_PUBLIC_KEY;const builderModel = import.meta.env.BUILDER_BLOGPOST_MODEL;
const { results: posts } = await fetch(  `https://cdn.builder.io/api/v3/content/${builderModel}?${new URLSearchParams({    apiKey: builderAPIpublicKey,    fields: ["data.slug", "data.title"].join(","),    cachebust: "true",  }).toString()}`)  .then((res) => res.json())  .catch();---
<html lang="en">  <head>    <title>Blog Index</title>  </head>  <body>    <ul>      {        posts.flatMap(({ data: { slug, title } }) => (          <li>            <a href={`/posts/${slug}`}>{title}</a>          </li>        ))      }    </ul>  </body></html>
```

Fetching via the content API returns an array of objects containing data for each post. The `fields` query parameter tells Builder which data is included (see highlighted code). `slug` and `title` should match the names of the custom data fields you’ve added to your Builder model.

The `posts` array returned from the fetch displays a list of blog post titles on the home page. The individual page routes will be created in the next step.

Go to your index route and you should be able to see a list of links each with the title of a blog post!

### Displaying a single blog post

[Section titled “Displaying a single blog post”](#displaying-a-single-blog-post)

Create the page `src/pages/posts/[slug].astro` that will [dynamically generate a page](https://docs.astro.build/en/guides/routing/#dynamic-routes) for each post.

- Directorysrc/
  - Directorypages/
    - index.astro
    - Directoryposts/
      - **[slug].astro**
  - env.d.ts
- .env
- astro.config.mjs
- package.json

This file must contain:

- A [getStaticPaths()](https://docs.astro.build/en/reference/routing-reference/#getstaticpaths) function to fetch `slug` information from Builder and create a static route for each blog post.
- A `fetch()` to the Builder API using the `slug` identifier to return post content and metadata (e.g. a `title`).
- A `<Fragment />` in the template to render the post content as HTML.

Each of these is highlighted in the following code snippet.

 src/pages/posts/[slug].astro

```
---export async function getStaticPaths() {  const builderModel = import.meta.env.BUILDER_BLOGPOST_MODEL;  const builderAPIpublicKey = import.meta.env.BUILDER_API_PUBLIC_KEY;  const { results: posts } = await fetch(    `https://cdn.builder.io/api/v3/content/${builderModel}?${new URLSearchParams(      {        apiKey: builderAPIpublicKey,        fields: ["data.slug", "data.title"].join(","),        cachebust: "true",      }    ).toString()}`  )    .then((res) => res.json())    .catch    // ...catch some errors...);    ();  return posts.map(({ data: { slug, title } }) => ({    params: { slug },    props: { title },  }))}const { slug } = Astro.params;const { title } = Astro.props;const builderModel = import.meta.env.BUILDER_BLOGPOST_MODEL;const builderAPIpublicKey = import.meta.env.BUILDER_API_PUBLIC_KEY;// Builder's API requires this field but for this use case the url doesn't seem to matter - the API returns the same HTMLconst encodedUrl = encodeURIComponent("moot");const { html: postHTML } = await fetch(  `https://cdn.builder.io/api/v1/qwik/${builderModel}?${new URLSearchParams({    apiKey: builderAPIpublicKey,    url: encodedUrl,    "query.data.slug": slug,    cachebust: "true",  }).toString()}`)  .then((res) => res.json())  .catch();---<html lang="en">  <head>    <title>{title}</title>  </head>  <body>    <header>This is your header</header>    <article>      <Fragment set:html={postHTML} />    </article>    <footer>This is your footer</footer>  </body></html>
```

Now when you click on a link on your index route, you will be taken to the individual blog post page.

### Publishing your site

[Section titled “Publishing your site”](#publishing-your-site)

To deploy your website, visit our [deployment guides](https://docs.astro.build/en/guides/deploy/) and follow the instructions for your preferred hosting provider.

#### Rebuild on Builder changes

[Section titled “Rebuild on Builder changes”](#rebuild-on-builder-changes)

If your project is using Astro’s default static mode, you will need to set up a webhook to trigger a new build when your content changes. If you are using Netlify or Vercel as your hosting provider, you can use its webhook feature to trigger a new build whenever you click **Publish** in the Builder editor.

##### Netlify

[Section titled “Netlify”](#netlify)

1. Go to your site dashboard, then **Site Settings** and click on **Build & deploy**.
2. Under the **Continuous Deployment** tab, find the **Build hooks** section and click on **Add build hook**.
3. Provide a name for your webhook and select the branch you want to trigger the build on. Click on **Save** and copy the generated URL.

##### Vercel

[Section titled “Vercel”](#vercel)

1. Go to your project dashboard and click on **Settings**.
2. Under the **Git** tab, find the **Deploy Hooks** section.
3. Provide a name for your webhook and the branch you want to trigger the build on. Click **Add** and copy the generated URL.

##### Adding a webhook to Builder

[Section titled “Adding a webhook to Builder”](#adding-a-webhook-to-builder)

1. In your Builder dashboard, go into your **blogpost** model. Under **Show More Options**, select **Edit Webhooks** at the bottom.
2. Add a new webhook by clicking on **Webhook**. Paste the URL generated by your hosting provider into the **Url** field.
3. Click on **Show Advanced** under the URL field and toggle the option to select **Disable Payload**. With the payload disabled, Builder sends a simpler POST request to your hosting provider, which can be helpful as your site grows. Click **Done** to save this selection.

With this webhook in place, whenever you click the **Publish** button in the Builder editor, your hosting provider rebuilds your site - and Astro fetches the newly published data for you. Nothing to do but lean back and pump out that sweet sweet content!

## Official resources

[Section titled “Official resources”](#official-resources)

- Check out [the official Builder.io starter project](https://github.com/BuilderIO/builder/tree/main/examples/astro-solidjs), which uses Astro and SolidJS.
- The [official Builder quickstart guide](https://www.builder.io/c/docs/quickstart#step-1-add-builder-as-a-dependency) covers both the use of the REST API as well as data fetching through an integration with a JavaScript framework like Qwik, React or Vue.
- [Builder’s API explorer](https://builder.io/api-explorer) can help if you need to troubleshoot your API calls.

## Community resources

[Section titled “Community resources”](#community-resources)

- Read [Connecting Builder.io’s Visual CMS to Astro](https://www.hamatoyogi.dev/blog/astro-log/connecting-builderio-to-astro) by Yoav Ganbar.

## More CMS guides

- ![](https://docs.astro.build/logos/apostrophecms.svg)
  ### ApostropheCMS
- ![](https://docs.astro.build/logos/builderio.svg)
  ### Builder.io
- ![](https://docs.astro.build/logos/buttercms.svg)
  ### ButterCMS
- ![](https://docs.astro.build/logos/caisy.svg)
  ### Caisy
- ![](https://docs.astro.build/logos/cloudcannon.svg)
  ### CloudCannon
- ![](https://docs.astro.build/logos/contentful.svg)
  ### Contentful
- ![](https://docs.astro.build/logos/cosmic.svg)
  ### Cosmic
- ![](https://docs.astro.build/logos/craft-cms.svg)
  ### Craft CMS
- ![](https://docs.astro.build/logos/craft-cross-cms.svg)
  ### Craft Cross CMS
- ![](https://docs.astro.build/logos/crystallize.svg)
  ### Crystallize
- ![](https://docs.astro.build/logos/datocms.svg)
  ### DatoCMS
- ![](https://docs.astro.build/logos/decap-cms.svg)
  ### Decap CMS
- ![](https://docs.astro.build/logos/directus.svg)
  ### Directus
- ![](https://docs.astro.build/logos/drupal.svg)
  ### Drupal
- ![](https://docs.astro.build/logos/flotiq.svg)
  ### Flotiq
- ![](https://docs.astro.build/logos/frontmatter-cms.svg)
  ### Front Matter CMS
- ![](https://docs.astro.build/logos/ghost.png)
  ### Ghost
- ![](https://docs.astro.build/logos/gitcms.svg)
  ### GitCMS
- ![](https://docs.astro.build/logos/hashnode.png)
  ### Hashnode
- ![](https://docs.astro.build/logos/hygraph.svg)
  ### Hygraph
- ![](https://docs.astro.build/logos/jekyllpad.svg)
  ### JekyllPad
- ![](https://docs.astro.build/logos/keystatic.svg)
  ### Keystatic
- ![](https://docs.astro.build/logos/keystonejs.svg)
  ### KeystoneJS
- ![](https://docs.astro.build/logos/kontent-ai.svg)
  ### Kontent.ai
- ![](https://docs.astro.build/logos/microcms.svg)
  ### microCMS
- ![](https://docs.astro.build/logos/optimizely.svg)
  ### Optimizely CMS
- ![](https://docs.astro.build/logos/payload.svg)
  ### Payload CMS
- ![](https://docs.astro.build/logos/preprcms.svg)
  ### Prepr CMS
- ![](https://docs.astro.build/logos/prismic.svg)
  ### Prismic
- ![](https://docs.astro.build/logos/sanity.svg)
  ### Sanity
- ![](https://docs.astro.build/logos/sitecore.svg)
  ### Sitecore XM
- ![](https://docs.astro.build/logos/sitepins.svg)
  ### Sitepins
- ![](https://docs.astro.build/logos/spinal.svg)
  ### Spinal
- ![](https://docs.astro.build/logos/statamic.svg)
  ### Statamic
- ![](https://docs.astro.build/logos/storyblok.svg)
  ### Storyblok
- ![](https://docs.astro.build/logos/strapi.svg)
  ### Strapi
- ![](https://docs.astro.build/logos/studiocms.svg)
  ### StudioCMS
- ![](https://docs.astro.build/logos/tina-cms.svg)
  ### Tina CMS
- ![](https://docs.astro.build/logos/umbraco.svg)
  ### Umbraco
- ![](https://docs.astro.build/logos/wordpress.svg)
  ### Wordpress

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)
