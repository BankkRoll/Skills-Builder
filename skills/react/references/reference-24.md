# <title> and more

# <title>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <title>

The [built-in browser<title>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) lets you specify the title of the document.

$

```
<title>My Blog</title>
```

/$

- [Reference](#reference)
  - [<title>](#title)
- [Usage](#usage)
  - [Set the document title](#set-the-document-title)
  - [Use variables in the title](#use-variables-in-the-title)

---

## Reference

### <title>

To specify the title of the document, render the [built-in browser<title>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title). You can render `<title>` from any component and React will always place the corresponding DOM element in the document head.

 $

```
<title>My Blog</title>
```

/$

[See more examples below.](#usage)

#### Props

`<title>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

- `children`: `<title>` accepts only text as a child. This text will become the title of the document. You can also pass your own components as long as they only render text.

#### Special rendering behavior

React will always place the DOM element corresponding to the `<title>` component within the document’s `<head>`, regardless of where in the React tree it is rendered. The `<head>` is the only valid place for `<title>` to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render its `<title>` itself.

There are two exception to this:

- If `<title>` is within an `<svg>` component, then there is no special behavior, because in this context it doesn’t represent the document’s title but rather is an [accessibility annotation for that SVG graphic](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title).
- If the `<title>` has an [itemProp](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemprop) prop, there is no special behavior, because in this case it doesn’t represent the document’s title but rather metadata about a specific part of the page.

### Pitfall

Only render a single `<title>` at a time. If more than one component renders a `<title>` tag at the same time, React will place all of those titles in the document head. When this happens, the behavior of browsers and search engines is undefined.

---

## Usage

### Set the document title

Render the `<title>` component from any component with text as its children. React will put a `<title>` DOM node in the document `<head>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function ContactUsPage() {
  return (
    <ShowRenderedHTML>
      <title>My Site: Contact Us</title>
      <h1>Contact Us</h1>
      <p>Email us at support@example.com</p>
    </ShowRenderedHTML>
  );
}
```

/$

### Use variables in the title

The children of the `<title>` component must be a single string of text. (Or a single number or a single object with a `toString` method.) It might not be obvious, but using JSX curly braces like this:

 $

```
<title>Results page {pageNumber}</title> // 🔴 Problem: This is not a single string
```

/$

… actually causes the `<title>` component to get a two-element array as its children (the string `"Results page"` and the value of `pageNumber`). This will cause an error. Instead, use string interpolation to pass `<title>` a single string:

 $

```
<title>{`Results page ${pageNumber}`}</title>
```

/$[Previous<style>](https://react.dev/reference/react-dom/components/style)[NextAPIs](https://react.dev/reference/react-dom)

---

# React DOM Components

[API Reference](https://react.dev/reference/react)

# React DOM Components

React supports all of the browser built-in [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Element) and [SVG](https://developer.mozilla.org/en-US/docs/Web/SVG/Element) components.

---

## Common components

All of the built-in browser components support some props and events.

- [Common components (e.g.<div>)](https://react.dev/reference/react-dom/components/common)

This includes React-specific props like `ref` and `dangerouslySetInnerHTML`.

---

## Form components

These built-in browser components accept user input:

- [<input>](https://react.dev/reference/react-dom/components/input)
- [<select>](https://react.dev/reference/react-dom/components/select)
- [<textarea>](https://react.dev/reference/react-dom/components/textarea)

They are special in React because passing the `value` prop to them makes them *controlled.*

---

## Resource and Metadata Components

These built-in browser components let you load external resources or annotate the document with metadata:

- [<link>](https://react.dev/reference/react-dom/components/link)
- [<meta>](https://react.dev/reference/react-dom/components/meta)
- [<script>](https://react.dev/reference/react-dom/components/script)
- [<style>](https://react.dev/reference/react-dom/components/style)
- [<title>](https://react.dev/reference/react-dom/components/title)

They are special in React because React can render them into the document head, suspend while resources are loading, and enact other behaviors that are described on the reference page for each specific component.

---

## All HTML components

React supports all built-in browser HTML components. This includes:

- [<aside>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/aside)
- [<audio>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)
- [<b>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/b)
- [<base>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base)
- [<bdi>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/bdi)
- [<bdo>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/bdo)
- [<blockquote>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/blockquote)
- [<body>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/body)
- [<br>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/br)
- [<button>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button)
- [<canvas>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas)
- [<caption>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/caption)
- [<cite>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/cite)
- [<code>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/code)
- [<col>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/col)
- [<colgroup>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/colgroup)
- [<data>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/data)
- [<datalist>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist)
- [<dd>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dd)
- [<del>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/del)
- [<details>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details)
- [<dfn>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dfn)
- [<dialog>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog)
- [<div>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div)
- [<dl>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dl)
- [<dt>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dt)
- [<em>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/em)
- [<embed>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/embed)
- [<fieldset>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/fieldset)
- [<figcaption>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/figcaption)
- [<figure>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/figure)
- [<footer>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/footer)
- [<form>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form)
- [<h1>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/h1)
- [<head>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/head)
- [<header>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/header)
- [<hgroup>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/hgroup)
- [<hr>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/hr)
- [<html>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html)
- [<i>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/i)
- [<iframe>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe)
- [<img>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img)
- [<input>](https://react.dev/reference/react-dom/components/input)
- [<ins>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ins)
- [<kbd>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/kbd)
- [<label>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label)
- [<legend>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/legend)
- [<li>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/li)
- [<link>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link)
- [<main>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main)
- [<map>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/map)
- [<mark>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/mark)
- [<menu>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/menu)
- [<meta>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta)
- [<meter>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meter)
- [<nav>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/nav)
- [<noscript>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/noscript)
- [<object>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/object)
- [<ol>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ol)
- [<optgroup>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/optgroup)
- [<option>](https://react.dev/reference/react-dom/components/option)
- [<output>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/output)
- [<p>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/p)
- [<picture>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)
- [<pre>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/pre)
- [<progress>](https://react.dev/reference/react-dom/components/progress)
- [<q>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/q)
- [<rp>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/rp)
- [<rt>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/rt)
- [<ruby>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ruby)
- [<s>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/s)
- [<samp>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/samp)
- [<script>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script)
- [<section>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/section)
- [<select>](https://react.dev/reference/react-dom/components/select)
- [<slot>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/slot)
- [<small>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/small)
- [<source>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/source)
- [<span>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/span)
- [<strong>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/strong)
- [<style>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style)
- [<sub>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/sub)
- [<summary>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/summary)
- [<sup>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/sup)
- [<table>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table)
- [<tbody>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tbody)
- [<td>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/td)
- [<template>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template)
- [<textarea>](https://react.dev/reference/react-dom/components/textarea)
- [<tfoot>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tfoot)
- [<th>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/th)
- [<thead>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/thead)
- [<time>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/time)
- [<title>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title)
- [<tr>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr)
- [<track>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track)
- [<u>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/u)
- [<ul>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul)
- [<var>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/var)
- [<video>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video)
- [<wbr>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/wbr)

### Note

Similar to the [DOM standard,](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) React uses a `camelCase` convention for prop names. For example, you’ll write `tabIndex` instead of `tabindex`. You can convert existing HTML to JSX with an [online converter.](https://transform.tools/html-to-jsx)

---

### Custom HTML elements

If you render a tag with a dash, like `<my-element>`, React will assume you want to render a [custom HTML element.](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements)

If you render a built-in browser HTML element with an [is](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/is) attribute, it will also be treated as a custom element.

#### Setting values on custom elements

Custom elements have two methods of passing data into them:

1. Attributes: Which are displayed in markup and can only be set to string values
2. Properties: Which are not displayed in markup and can be set to arbitrary JavaScript values

By default, React will pass values bound in JSX as attributes:

 $

```
<my-element value="Hello, world!"></my-element>
```

/$

Non-string JavaScript values passed to custom elements will be serialized by default:

 $

```
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`<my-element value={[1,2,3]}></my-element>
```

/$

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export class MyElement extends HTMLElement {
  constructor() {
    super();
    // The value here will be overwritten by React
    // when initialized as an element
    this.value = undefined;
  }

  connectedCallback() {
    this.innerHTML = this.value.join(", ");
  }
}
```

/$

#### Listening for events on custom elements

A common pattern when using custom elements is that they may dispatch [CustomEvents](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent) rather than accept a function to call when an event occur. You can listen for these events using an `on` prefix when binding to the event via JSX.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export function App() {
  return (
    <my-element
      onspeak={e => console.log(e.detail.message)}
    ></my-element>
  )
}
```

/$

### Note

Events are case-sensitive and support dashes (`-`). Preserve the casing of the event and include all dashes when listening for custom element’s events:

$

```
// Listens for `say-hi` events<my-element onsay-hi={console.log}></my-element>// Listens for `sayHi` events<my-element onsayHi={console.log}></my-element>
```

/$

---

## All SVG components

React supports all built-in browser SVG components. This includes:

- [<a>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/a)
- [<animate>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animate)
- [<animateMotion>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animateMotion)
- [<animateTransform>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/animateTransform)
- [<circle>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/circle)
- [<clipPath>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/clipPath)
- [<defs>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/defs)
- [<desc>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/desc)
- [<discard>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/discard)
- [<ellipse>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/ellipse)
- [<feBlend>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feBlend)
- [<feColorMatrix>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feColorMatrix)
- [<feComponentTransfer>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feComponentTransfer)
- [<feComposite>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feComposite)
- [<feConvolveMatrix>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feConvolveMatrix)
- [<feDiffuseLighting>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDiffuseLighting)
- [<feDisplacementMap>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDisplacementMap)
- [<feDistantLight>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDistantLight)
- [<feDropShadow>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feDropShadow)
- [<feFlood>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFlood)
- [<feFuncA>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncA)
- [<feFuncB>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncB)
- [<feFuncG>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncG)
- [<feFuncR>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncR)
- [<feGaussianBlur>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feGaussianBlur)
- [<feImage>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feImage)
- [<feMerge>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMerge)
- [<feMergeNode>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMergeNode)
- [<feMorphology>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feMorphology)
- [<feOffset>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feOffset)
- [<fePointLight>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/fePointLight)
- [<feSpecularLighting>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feSpecularLighting)
- [<feSpotLight>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feSpotLight)
- [<feTile>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTile)
- [<feTurbulence>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTurbulence)
- [<filter>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/filter)
- [<foreignObject>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/foreignObject)
- [<g>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/g)
- `<hatch>`
- `<hatchpath>`
- [<image>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/image)
- [<line>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/line)
- [<linearGradient>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/linearGradient)
- [<marker>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker)
- [<mask>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mask)
- [<metadata>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/metadata)
- [<mpath>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mpath)
- [<path>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/path)
- [<pattern>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/pattern)
- [<polygon>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polygon)
- [<polyline>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polyline)
- [<radialGradient>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/radialGradient)
- [<rect>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect)
- [<script>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/script)
- [<set>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/set)
- [<stop>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/stop)
- [<style>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/style)
- [<svg>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/svg)
- [<switch>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/switch)
- [<symbol>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/symbol)
- [<text>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text)
- [<textPath>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath)
- [<title>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title)
- [<tspan>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/tspan)
- [<use>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/use)
- [<view>](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/view)

### Note

Similar to the [DOM standard,](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) React uses a `camelCase` convention for prop names. For example, you’ll write `tabIndex` instead of `tabindex`. You can convert existing SVG to JSX with an [online converter.](https://transform.tools/)

Namespaced attributes also have to be written without the colon:

- `xlink:actuate` becomes `xlinkActuate`.
- `xlink:arcrole` becomes `xlinkArcrole`.
- `xlink:href` becomes `xlinkHref`.
- `xlink:role` becomes `xlinkRole`.
- `xlink:show` becomes `xlinkShow`.
- `xlink:title` becomes `xlinkTitle`.
- `xlink:type` becomes `xlinkType`.
- `xml:base` becomes `xmlBase`.
- `xml:lang` becomes `xmlLang`.
- `xml:space` becomes `xmlSpace`.
- `xmlns:xlink` becomes `xmlnsXlink`.

[PrevioususeFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus)[NextCommon (e.g. <div>)](https://react.dev/reference/react-dom/components/common)

---

# createPortal

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react-dom)

# createPortal

`createPortal` lets you render some children into a different part of the DOM.

$

```
<div>  <SomeComponent />  {createPortal(children, domNode, key?)}</div>
```

/$

- [Reference](#reference)
  - [createPortal(children, domNode, key?)](#createportal)
- [Usage](#usage)
  - [Rendering to a different part of the DOM](#rendering-to-a-different-part-of-the-dom)
  - [Rendering a modal dialog with a portal](#rendering-a-modal-dialog-with-a-portal)
  - [Rendering React components into non-React server markup](#rendering-react-components-into-non-react-server-markup)
  - [Rendering React components into non-React DOM nodes](#rendering-react-components-into-non-react-dom-nodes)

---

## Reference

### createPortal(children, domNode, key?)

To create a portal, call `createPortal`, passing some JSX, and the DOM node where it should be rendered:

 $

```
import { createPortal } from 'react-dom';// ...<div>  <p>This child is placed in the parent div.</p>  {createPortal(    <p>This child is placed in the document body.</p>,    document.body  )}</div>
```

/$

[See more examples below.](#usage)

A portal only changes the physical placement of the DOM node. In every other way, the JSX you render into a portal acts as a child node of the React component that renders it. For example, the child can access the context provided by the parent tree, and events bubble up from children to parents according to the React tree.

#### Parameters

- `children`: Anything that can be rendered with React, such as a piece of JSX (e.g. `<div />` or `<SomeComponent />`), a [Fragment](https://react.dev/reference/react/Fragment) (`<>...</>`), a string or a number, or an array of these.
- `domNode`: Some DOM node, such as those returned by `document.getElementById()`. The node must already exist. Passing a different DOM node during an update will cause the portal content to be recreated.
- **optional** `key`: A unique string or number to be used as the portal’s [key.](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)

#### Returns

`createPortal` returns a React node that can be included into JSX or returned from a React component. If React encounters it in the render output, it will place the provided `children` inside the provided `domNode`.

#### Caveats

- Events from portals propagate according to the React tree rather than the DOM tree. For example, if you click inside a portal, and the portal is wrapped in `<div onClick>`, that `onClick` handler will fire. If this causes issues, either stop the event propagation from inside the portal, or move the portal itself up in the React tree.

---

## Usage

### Rendering to a different part of the DOM

*Portals* let your components render some of their children into a different place in the DOM. This lets a part of your component “escape” from whatever containers it may be in. For example, a component can display a modal dialog or a tooltip that appears above and outside of the rest of the page.

To create a portal, render the result of `createPortal` with some JSX and the DOM node where it should go:

 $

```
import { createPortal } from 'react-dom';function MyComponent() {  return (    <div style={{ border: '2px solid black' }}>      <p>This child is placed in the parent div.</p>      {createPortal(        <p>This child is placed in the document body.</p>,        document.body      )}    </div>  );}
```

/$

React will put the DOM nodes for the JSX you passed inside of the DOM node you provided.

Without a portal, the second `<p>` would be placed inside the parent `<div>`, but the portal “teleported” it into the [document.body:](https://developer.mozilla.org/en-US/docs/Web/API/Document/body)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createPortal } from 'react-dom';

export default function MyComponent() {
  return (
    <div style={{ border: '2px solid black' }}>
      <p>This child is placed in the parent div.</p>
      {createPortal(
        <p>This child is placed in the document body.</p>,
        document.body
      )}
    </div>
  );
}
```

/$

Notice how the second paragraph visually appears outside the parent `<div>` with the border. If you inspect the DOM structure with developer tools, you’ll see that the second `<p>` got placed directly into the `<body>`:

 $

```
<body>  <div id="root">    ...      <div style="border: 2px solid black">        <p>This child is placed inside the parent div.</p>      </div>    ...  </div>  <p>This child is placed in the document body.</p></body>
```

/$

A portal only changes the physical placement of the DOM node. In every other way, the JSX you render into a portal acts as a child node of the React component that renders it. For example, the child can access the context provided by the parent tree, and events still bubble up from children to parents according to the React tree.

---

### Rendering a modal dialog with a portal

You can use a portal to create a modal dialog that floats above the rest of the page, even if the component that summons the dialog is inside a container with `overflow: hidden` or other styles that interfere with the dialog.

In this example, the two containers have styles that disrupt the modal dialog, but the one rendered into a portal is unaffected because, in the DOM, the modal is not contained within the parent JSX elements.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import NoPortalExample from './NoPortalExample';
import PortalExample from './PortalExample';

export default function App() {
  return (
    <>
      <div className="clipping-container">
        <NoPortalExample  />
      </div>
      <div className="clipping-container">
        <PortalExample />
      </div>
    </>
  );
}
```

/$

### Pitfall

It’s important to make sure that your app is accessible when using portals. For instance, you may need to manage keyboard focus so that the user can move the focus in and out of the portal in a natural way.

Follow the [WAI-ARIA Modal Authoring Practices](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal) when creating modals. If you use a community package, ensure that it is accessible and follows these guidelines.

---

### Rendering React components into non-React server markup

Portals can be useful if your React root is only part of a static or server-rendered page that isn’t built with React. For example, if your page is built with a server framework like Rails, you can create areas of interactivity within static areas such as sidebars. Compared with having [multiple separate React roots,](https://react.dev/reference/react-dom/client/createRoot#rendering-a-page-partially-built-with-react) portals let you treat the app as a single React tree with shared state even though its parts render to different parts of the DOM.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createPortal } from 'react-dom';

const sidebarContentEl = document.getElementById('sidebar-content');

export default function App() {
  return (
    <>
      <MainContent />
      {createPortal(
        <SidebarContent />,
        sidebarContentEl
      )}
    </>
  );
}

function MainContent() {
  return <p>This part is rendered by React</p>;
}

function SidebarContent() {
  return <p>This part is also rendered by React!</p>;
}
```

/$

---

### Rendering React components into non-React DOM nodes

You can also use a portal to manage the content of a DOM node that’s managed outside of React. For example, suppose you’re integrating with a non-React map widget and you want to render React content inside a popup. To do this, declare a `popupContainer` state variable to store the DOM node you’re going to render into:

 $

```
const [popupContainer, setPopupContainer] = useState(null);
```

/$

When you create the third-party widget, store the DOM node returned by the widget so you can render into it:

 $

```
useEffect(() => {  if (mapRef.current === null) {    const map = createMapWidget(containerRef.current);    mapRef.current = map;    const popupDiv = addPopupToMapWidget(map);    setPopupContainer(popupDiv);  }}, []);
```

/$

This lets you use `createPortal` to render React content into `popupContainer` once it becomes available:

 $

```
return (  <div style={{ width: 250, height: 250 }} ref={containerRef}>    {popupContainer !== null && createPortal(      <p>Hello from React!</p>,      popupContainer    )}  </div>);
```

/$

Here is a complete example you can play with:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { createMapWidget, addPopupToMapWidget } from './map-widget.js';

export default function Map() {
  const containerRef = useRef(null);
  const mapRef = useRef(null);
  const [popupContainer, setPopupContainer] = useState(null);

  useEffect(() => {
    if (mapRef.current === null) {
      const map = createMapWidget(containerRef.current);
      mapRef.current = map;
      const popupDiv = addPopupToMapWidget(map);
      setPopupContainer(popupDiv);
    }
  }, []);

  return (
    <div style={{ width: 250, height: 250 }} ref={containerRef}>
      {popupContainer !== null && createPortal(
        <p>Hello from React!</p>,
        popupContainer
      )}
    </div>
  );
}
```

/$[PreviousAPIs](https://react.dev/reference/react-dom)[NextflushSync](https://react.dev/reference/react-dom/flushSync)

---

# findDOMNode

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react-dom)

# findDOMNode

### Deprecated

This API will be removed in a future major version of React. [See the alternatives.](#alternatives)

`findDOMNode` finds the browser DOM node for a React [class component](https://react.dev/reference/react/Component) instance.

$

```
const domNode = findDOMNode(componentInstance)
```

/$

- [Reference](#reference)
  - [findDOMNode(componentInstance)](#finddomnode)
- [Usage](#usage)
  - [Finding the root DOM node of a class component](#finding-the-root-dom-node-of-a-class-component)
- [Alternatives](#alternatives)
  - [Reading component’s own DOM node from a ref](#reading-components-own-dom-node-from-a-ref)
  - [Reading a child component’s DOM node from a forwarded ref](#reading-a-child-components-dom-node-from-a-forwarded-ref)
  - [Adding a wrapper<div>element](#adding-a-wrapper-div-element)

---

## Reference

### findDOMNode(componentInstance)

Call `findDOMNode` to find the browser DOM node for a given React [class component](https://react.dev/reference/react/Component) instance.

 $

```
import { findDOMNode } from 'react-dom';const domNode = findDOMNode(componentInstance);
```

/$

[See more examples below.](#usage)

#### Parameters

- `componentInstance`: An instance of the [Component](https://react.dev/reference/react/Component) subclass. For example, `this` inside a class component.

#### Returns

`findDOMNode` returns the first closest browser DOM node within the given `componentInstance`. When a component renders to `null`, or renders `false`, `findDOMNode` returns `null`. When a component renders to a string, `findDOMNode` returns a text DOM node containing that value.

#### Caveats

- A component may return an array or a [Fragment](https://react.dev/reference/react/Fragment) with multiple children. In that case `findDOMNode`, will return the DOM node corresponding to the first non-empty child.
- `findDOMNode` only works on mounted components (that is, components that have been placed in the DOM). If you try to call this on a component that has not been mounted yet (like calling `findDOMNode()` in `render()` on a component that has yet to be created), an exception will be thrown.
- `findDOMNode` only returns the result at the time of your call. If a child component renders a different node later, there is no way for you to be notified of this change.
- `findDOMNode` accepts a class component instance, so it can’t be used with function components.

---

## Usage

### Finding the root DOM node of a class component

Call `findDOMNode` with a [class component](https://react.dev/reference/react/Component) instance (usually, `this`) to find the DOM node it has rendered.

 $

```
class AutoselectingInput extends Component {  componentDidMount() {    const input = findDOMNode(this);    input.select()  }  render() {    return <input defaultValue="Hello" />  }}
```

/$

Here, the `input` variable will be set to the `<input>` DOM element. This lets you do something with it. For example, when clicking “Show example” below mounts the input, [input.select()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/select) selects all text in the input:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }

  render() {
    return <input defaultValue="Hello" />
  }
}

export default AutoselectingInput;
```

/$

---

## Alternatives

### Reading component’s own DOM node from a ref

Code using `findDOMNode` is fragile because the connection between the JSX node and the code manipulating the corresponding DOM node is not explicit. For example, try wrapping this `<input />` into a `<div>`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }
  render() {
    return <input defaultValue="Hello" />
  }
}

export default AutoselectingInput;
```

/$

This will break the code because now, `findDOMNode(this)` finds the `<div>` DOM node, but the code expects an `<input>` DOM node. To avoid these kinds of problems, use [createRef](https://react.dev/reference/react/createRef) to manage a specific DOM node.

In this example, `findDOMNode` is no longer used. Instead, `inputRef = createRef(null)` is defined as an instance field on the class. To read the DOM node from it, you can use `this.inputRef.current`. To attach it to the JSX, you render `<input ref={this.inputRef} />`. This connects the code using the DOM node to its JSX:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRef, Component } from 'react';

class AutoselectingInput extends Component {
  inputRef = createRef(null);

  componentDidMount() {
    const input = this.inputRef.current;
    input.select()
  }

  render() {
    return (
      <input ref={this.inputRef} defaultValue="Hello" />
    );
  }
}

export default AutoselectingInput;
```

/$

In modern React without class components, the equivalent code would call [useRef](https://react.dev/reference/react/useRef) instead:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useEffect } from 'react';

export default function AutoselectingInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    const input = inputRef.current;
    input.select();
  }, []);

  return <input ref={inputRef} defaultValue="Hello" />
}
```

/$

[Read more about manipulating the DOM with refs.](https://react.dev/learn/manipulating-the-dom-with-refs)

---

### Reading a child component’s DOM node from a forwarded ref

In this example, `findDOMNode(this)` finds a DOM node that belongs to another component. The `AutoselectingInput` renders `MyInput`, which is your own component that renders a browser `<input>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';
import MyInput from './MyInput.js';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }
  render() {
    return <MyInput />;
  }
}

export default AutoselectingInput;
```

/$

Notice that calling `findDOMNode(this)` inside `AutoselectingInput` still gives you the DOM `<input>`—even though the JSX for this `<input>` is hidden inside the `MyInput` component. This seems convenient for the above example, but it leads to fragile code. Imagine that you wanted to edit `MyInput` later and add a wrapper `<div>` around it. This would break the code of `AutoselectingInput` (which expects to find an `<input>`).

To replace `findDOMNode` in this example, the two components need to coordinate:

1. `AutoSelectingInput` should declare a ref, like [in the earlier example](#reading-components-own-dom-node-from-a-ref), and pass it to `<MyInput>`.
2. `MyInput` should be declared with [forwardRef](https://react.dev/reference/react/forwardRef) to take that ref and forward it down to the `<input>` node.

This version does that, so it no longer needs `findDOMNode`:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { createRef, Component } from 'react';
import MyInput from './MyInput.js';

class AutoselectingInput extends Component {
  inputRef = createRef(null);

  componentDidMount() {
    const input = this.inputRef.current;
    input.select()
  }

  render() {
    return (
      <MyInput ref={this.inputRef} />
    );
  }
}

export default AutoselectingInput;
```

/$

Here is how this code would look like with function components instead of classes:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useRef, useEffect } from 'react';
import MyInput from './MyInput.js';

export default function AutoselectingInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    const input = inputRef.current;
    input.select();
  }, []);

  return <MyInput ref={inputRef} defaultValue="Hello" />
}
```

/$

---

### Adding a wrapper<div>element

Sometimes a component needs to know the position and size of its children. This makes it tempting to find the children with `findDOMNode(this)`, and then use DOM methods like [getBoundingClientRect](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) for measurements.

There is currently no direct equivalent for this use case, which is why `findDOMNode` is deprecated but is not yet removed completely from React. In the meantime, you can try rendering a wrapper `<div>` node around the content as a workaround, and getting a ref to that node. However, extra wrappers can break styling.

 $

```
<div ref={someRef}>  {children}</div>
```

/$

This also applies to focusing and scrolling to arbitrary children.

[PreviousflushSync](https://react.dev/reference/react-dom/flushSync)[Nexthydrate](https://react.dev/reference/react-dom/hydrate)

---

# flushSync

[API Reference](https://react.dev/reference/react)[APIs](https://react.dev/reference/react-dom)

# flushSync

### Pitfall

Using `flushSync` is uncommon and can hurt the performance of your app.

`flushSync` lets you force React to flush any updates inside the provided callback synchronously. This ensures that the DOM is updated immediately.

$

```
flushSync(callback)
```

/$

- [Reference](#reference)
  - [flushSync(callback)](#flushsync)
- [Usage](#usage)
  - [Flushing updates for third-party integrations](#flushing-updates-for-third-party-integrations)
- [Troubleshooting](#troubleshooting)
  - [I’m getting an error: “flushSync was called from inside a lifecycle method”](#im-getting-an-error-flushsync-was-called-from-inside-a-lifecycle-method)

---

## Reference

### flushSync(callback)

Call `flushSync` to force React to flush any pending work and update the DOM synchronously.

 $

```
import { flushSync } from 'react-dom';flushSync(() => {  setSomething(123);});
```

/$

Most of the time, `flushSync` can be avoided. Use `flushSync` as last resort.

[See more examples below.](#usage)

#### Parameters

- `callback`: A function. React will immediately call this callback and flush any updates it contains synchronously. It may also flush any pending updates, or Effects, or updates inside of Effects. If an update suspends as a result of this `flushSync` call, the fallbacks may be re-shown.

#### Returns

`flushSync` returns `undefined`.

#### Caveats

- `flushSync` can significantly hurt performance. Use sparingly.
- `flushSync` may force pending Suspense boundaries to show their `fallback` state.
- `flushSync` may run pending Effects and synchronously apply any updates they contain before returning.
- `flushSync` may flush updates outside the callback when necessary to flush the updates inside the callback. For example, if there are pending updates from a click, React may flush those before flushing the updates inside the callback.

---

## Usage

### Flushing updates for third-party integrations

When integrating with third-party code such as browser APIs or UI libraries, it may be necessary to force React to flush updates. Use `flushSync` to force React to flush any state updates inside the callback synchronously:

 $

```
flushSync(() => {  setSomething(123);});// By this line, the DOM is updated.
```

/$

This ensures that, by the time the next line of code runs, React has already updated the DOM.

**UsingflushSyncis uncommon, and using it often can significantly hurt the performance of your app.** If your app only uses React APIs, and does not integrate with third-party libraries, `flushSync` should be unnecessary.

However, it can be helpful for integrating with third-party code like browser APIs.

Some browser APIs expect results inside of callbacks to be written to the DOM synchronously, by the end of the callback, so the browser can do something with the rendered DOM. In most cases, React handles this for you automatically. But in some cases it may be necessary to force a synchronous update.

For example, the browser `onbeforeprint` API allows you to change the page immediately before the print dialog opens. This is useful for applying custom print styles that allow the document to display better for printing. In the example below, you use `flushSync` inside of the `onbeforeprint` callback to immediately “flush” the React state to the DOM. Then, by the time the print dialog opens, `isPrinting` displays “yes”:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState, useEffect } from 'react';
import { flushSync } from 'react-dom';

export default function PrintApp() {
  const [isPrinting, setIsPrinting] = useState(false);

  useEffect(() => {
    function handleBeforePrint() {
      flushSync(() => {
        setIsPrinting(true);
      })
    }

    function handleAfterPrint() {
      setIsPrinting(false);
    }

    window.addEventListener('beforeprint', handleBeforePrint);
    window.addEventListener('afterprint', handleAfterPrint);
    return () => {
      window.removeEventListener('beforeprint', handleBeforePrint);
      window.removeEventListener('afterprint', handleAfterPrint);
    }
  }, []);

  return (
    <>
      <h1>isPrinting: {isPrinting ? 'yes' : 'no'}</h1>
      <button onClick={() => window.print()}>
        Print
      </button>
    </>
  );
}
```

/$

Without `flushSync`, the print dialog will display `isPrinting` as “no”. This is because React batches the updates asynchronously and the print dialog is displayed before the state is updated.

### Pitfall

`flushSync` can significantly hurt performance, and may unexpectedly force pending Suspense boundaries to show their fallback state.

Most of the time, `flushSync` can be avoided, so use `flushSync` as a last resort.

---

## Troubleshooting

### I’m getting an error: “flushSync was called from inside a lifecycle method”

React cannot `flushSync` in the middle of a render. If you do, it will noop and warn:

 ConsoleWarning: flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task.

This includes calling `flushSync` inside:

- rendering a component.
- `useLayoutEffect` or `useEffect` hooks.
- Class component lifecycle methods.

For example, calling `flushSync` in an Effect will noop and warn:

 $

```
import { useEffect } from 'react';import { flushSync } from 'react-dom';function MyComponent() {  useEffect(() => {    // 🚩 Wrong: calling flushSync inside an effect    flushSync(() => {      setSomething(newValue);    });  }, []);  return <div>{/* ... */}</div>;}
```

/$

To fix this, you usually want to move the `flushSync` call to an event:

 $

```
function handleClick() {  // ✅ Correct: flushSync in event handlers is safe  flushSync(() => {    setSomething(newValue);  });}
```

/$

If it’s difficult to move to an event, you can defer `flushSync` in a microtask:

 $

```
useEffect(() => {  // ✅ Correct: defer flushSync to a microtask  queueMicrotask(() => {    flushSync(() => {      setSomething(newValue);    });  });}, []);
```

/$

This will allow the current render to finish and schedule another syncronous render to flush the updates.

### Pitfall

`flushSync` can significantly hurt performance, but this particular pattern is even worse for performance. Exhaust all other options before calling `flushSync` in a microtask as an escape hatch.

[PreviouscreatePortal](https://react.dev/reference/react-dom/createPortal)[Nextpreconnect](https://react.dev/reference/react-dom/preconnect)

---

# useFormStatus

[API Reference](https://react.dev/reference/react)[Hooks](https://react.dev/reference/react-dom/hooks)

# useFormStatus

`useFormStatus` is a Hook that gives you status information of the last form submission.

$

```
const { pending, data, method, action } = useFormStatus();
```

/$

- [Reference](#reference)
  - [useFormStatus()](#use-form-status)
- [Usage](#usage)
  - [Display a pending state during form submission](#display-a-pending-state-during-form-submission)
  - [Read the form data being submitted](#read-form-data-being-submitted)
- [Troubleshooting](#troubleshooting)
  - [status.pendingis nevertrue](#pending-is-never-true)

---

## Reference

### useFormStatus()

The `useFormStatus` Hook provides status information of the last form submission.

 $

```
import { useFormStatus } from "react-dom";import action from './actions';function Submit() {  const status = useFormStatus();  return <button disabled={status.pending}>Submit</button>}export default function App() {  return (    <form action={action}>      <Submit />    </form>  );}
```

/$

To get status information, the `Submit` component must be rendered within a `<form>`. The Hook returns information like the `pending` property which tells you if the form is actively submitting.

In the above example, `Submit` uses this information to disable `<button>` presses while the form is submitting.

[See more examples below.](#usage)

#### Parameters

`useFormStatus` does not take any parameters.

#### Returns

A `status` object with the following properties:

- `pending`: A boolean. If `true`, this means the parent `<form>` is pending submission. Otherwise, `false`.
- `data`: An object implementing the [FormData interface](https://developer.mozilla.org/en-US/docs/Web/API/FormData) that contains the data the parent `<form>` is submitting. If there is no active submission or no parent `<form>`, it will be `null`.
- `method`: A string value of either `'get'` or `'post'`. This represents whether the parent `<form>` is submitting with either a `GET` or `POST` [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods). By default, a `<form>` will use the `GET` method and can be specified by the [method](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#method) property.

- `action`: A reference to the function passed to the `action` prop on the parent `<form>`. If there is no parent `<form>`, the property is `null`. If there is a URI value provided to the `action` prop, or no `action` prop specified, `status.action` will be `null`.

#### Caveats

- The `useFormStatus` Hook must be called from a component that is rendered inside a `<form>`.
- `useFormStatus` will only return status information for a parent `<form>`. It will not return status information for any `<form>` rendered in that same component or children components.

---

## Usage

### Display a pending state during form submission

To display a pending state while a form is submitting, you can call the `useFormStatus` Hook in a component rendered in a `<form>` and read the `pending` property returned.

Here, we use the `pending` property to indicate the form is submitting.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useFormStatus } from "react-dom";
import { submitForm } from "./actions.js";

function Submit() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
}

function Form({ action }) {
  return (
    <form action={action}>
      <Submit />
    </form>
  );
}

export default function App() {
  return <Form action={submitForm} />;
}
```

/$

### Pitfall

##### useFormStatuswill not return status information for a<form>rendered in the same component.

The `useFormStatus` Hook only returns status information for a parent `<form>` and not for any `<form>` rendered in the same component calling the Hook, or child components.

$

```
function Form() {  // 🚩 `pending` will never be true  // useFormStatus does not track the form rendered in this component  const { pending } = useFormStatus();  return <form action={submit}></form>;}
```

/$

Instead call `useFormStatus` from inside a component that is located inside `<form>`.

$

```
function Submit() {  // ✅ `pending` will be derived from the form that wraps the Submit component  const { pending } = useFormStatus();   return <button disabled={pending}>...</button>;}function Form() {  // This is the <form> `useFormStatus` tracks  return (    <form action={submit}>      <Submit />    </form>  );}
```

/$

### Read the form data being submitted

You can use the `data` property of the status information returned from `useFormStatus` to display what data is being submitted by the user.

Here, we have a form where users can request a username. We can use `useFormStatus` to display a temporary status message confirming what username they have requested.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import {useState, useMemo, useRef} from 'react';
import {useFormStatus} from 'react-dom';

export default function UsernameForm() {
  const {pending, data} = useFormStatus();

  return (
    <div>
      <h3>Request a Username: </h3>
      <input type="text" name="username" disabled={pending}/>
      <button type="submit" disabled={pending}>
        Submit
      </button>
      <br />
      <p>{data ? `Requesting ${data?.get("username")}...`: ''}</p>
    </div>
  );
}
```

/$

---

## Troubleshooting

### status.pendingis nevertrue

`useFormStatus` will only return status information for a parent `<form>`.

If the component that calls `useFormStatus` is not nested in a `<form>`, `status.pending` will always return `false`. Verify `useFormStatus` is called in a component that is a child of a `<form>` element.

`useFormStatus` will not track the status of a `<form>` rendered in the same component. See [Pitfall](#useformstatus-will-not-return-status-information-for-a-form-rendered-in-the-same-component) for more details.

[PreviousHooks](https://react.dev/reference/react-dom/hooks)[NextComponents](https://react.dev/reference/react-dom/components)

---

# Built

[API Reference](https://react.dev/reference/react)

# Built-in React DOM Hooks

The `react-dom` package contains Hooks that are only supported for web applications (which run in the browser DOM environment). These Hooks are not supported in non-browser environments like iOS, Android, or Windows applications. If you are looking for Hooks that are supported in web browsers *and other environments* see [the React Hooks page](https://react.dev/reference/react/hooks). This page lists all the Hooks in the `react-dom` package.

---

## Form Hooks

*Forms* let you create interactive controls for submitting information.  To manage forms in your components, use one of these Hooks:

- [useFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus) allows you to make updates to the UI based on the status of a form.

 $

```
function Form({ action }) {  async function increment(n) {    return n + 1;  }  const [count, incrementFormAction] = useActionState(increment, 0);  return (    <form action={action}>      <button formAction={incrementFormAction}>Count: {count}</button>      <Button />    </form>  );}function Button() {  const { pending } = useFormStatus();  return (    <button disabled={pending} type="submit">      Submit    </button>  );}
```

/$[NextuseFormStatus](https://react.dev/reference/react-dom/hooks/useFormStatus)
