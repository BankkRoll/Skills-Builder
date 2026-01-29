# <meta> and more

# <meta>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <meta>

The [built-in browser<meta>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta) lets you add metadata to the document.

$

```
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

/$

- [Reference](#reference)
  - [<meta>](#meta)
- [Usage](#usage)
  - [Annotating the document with metadata](#annotating-the-document-with-metadata)
  - [Annotating specific items within the document with metadata](#annotating-specific-items-within-the-document-with-metadata)

---

## Reference

### <meta>

To add document metadata, render the [built-in browser<meta>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta). You can render `<meta>` from any component and React will always place the corresponding DOM element in the document head.

 $

```
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

/$

[See more examples below.](#usage)

#### Props

`<meta>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

It should have *exactly one* of the following props: `name`, `httpEquiv`, `charset`, `itemProp`. The `<meta>` component does something different depending on which of these props is specified.

- `name`: a string. Specifies the [kind of metadata](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name) to be attached to the document.
- `charset`: a string. Specifies the character set used by the document. The only valid value is `"utf-8"`.
- `httpEquiv`: a string. Specifies a directive for processing the document.
- `itemProp`: a string. Specifies metadata about a particular item within the document rather than the document as a whole.
- `content`: a string. Specifies the metadata to be attached when used with the `name` or `itemProp` props or the behavior of the directive when used with the `httpEquiv` prop.

#### Special rendering behavior

React will always place the DOM element corresponding to the `<meta>` component within the document’s `<head>`, regardless of where in the React tree it is rendered. The `<head>` is the only valid place for `<meta>` to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render `<meta>` components itself.

There is one exception to this: if `<meta>` has an [itemProp](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemprop) prop, there is no special behavior, because in this case it doesn’t represent metadata about the document but rather metadata about a specific part of the page.

---

## Usage

### Annotating the document with metadata

You can annotate the document with metadata such as keywords, a summary, or the author’s name. React will place this metadata within the document `<head>` regardless of where in the React tree it is rendered.

 $

```
<meta name="author" content="John Smith" /><meta name="keywords" content="React, JavaScript, semantic markup, html" /><meta name="description" content="API reference for the <meta> component in React DOM" />
```

/$

You can render the `<meta>` component from any component. React will put a `<meta>` DOM node in the document `<head>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function SiteMapPage() {
  return (
    <ShowRenderedHTML>
      <meta name="keywords" content="React" />
      <meta name="description" content="A site map for the React website" />
      <h1>Site Map</h1>
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

/$

### Annotating specific items within the document with metadata

You can use the `<meta>` component with the `itemProp` prop to annotate specific items within the document with metadata. In this case, React will *not* place these annotations within the document `<head>` but will place them like any other React component.

 $

```
<section itemScope>  <h3>Annotating specific items</h3>  <meta itemProp="description" content="API reference for using <meta> with itemProp" />  <p>...</p></section>
```

/$[Previous<link>](https://react.dev/reference/react-dom/components/link)[Next<script>](https://react.dev/reference/react-dom/components/script)

---

# <option>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <option>

The [built-in browser<option>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option) lets you render an option inside a [<select>](https://react.dev/reference/react-dom/components/select) box.

$

```
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

/$

- [Reference](#reference)
  - [<option>](#option)
- [Usage](#usage)
  - [Displaying a select box with options](#displaying-a-select-box-with-options)

---

## Reference

### <option>

The [built-in browser<option>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option) lets you render an option inside a [<select>](https://react.dev/reference/react-dom/components/select) box.

 $

```
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

/$

[See more examples below.](#usage)

#### Props

`<option>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

Additionally, `<option>` supports these props:

- [disabled](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option#disabled): A boolean. If `true`, the option will not be selectable and will appear dimmed.
- [label](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option#label): A string. Specifies the meaning of the option. If not specified, the text inside the option is used.
- [value](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option#value): The value to be used [when submitting the parent<select>in a form](https://react.dev/reference/react-dom/components/select#reading-the-select-box-value-when-submitting-a-form) if this option is selected.

#### Caveats

- React does not support the `selected` attribute on `<option>`. Instead, pass this option’s `value` to the parent [<select defaultValue>](https://react.dev/reference/react-dom/components/select#providing-an-initially-selected-option) for an uncontrolled select box, or [<select value>](https://react.dev/reference/react-dom/components/select#controlling-a-select-box-with-a-state-variable) for a controlled select.

---

## Usage

### Displaying a select box with options

Render a `<select>` with a list of `<option>` components inside to display a select box. Give each `<option>` a `value` representing the data to be submitted with the form.

[Read more about displaying a<select>with a list of<option>components.](https://react.dev/reference/react-dom/components/select)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function FruitPicker() {
  return (
    <label>
      Pick a fruit:
      <select name="selectedFruit">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

/$[Previous<input>](https://react.dev/reference/react-dom/components/input)[Next<progress>](https://react.dev/reference/react-dom/components/progress)

---

# <progress>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <progress>

The [built-in browser<progress>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress) lets you render a progress indicator.

$

```
<progress value={0.5} />
```

/$

- [Reference](#reference)
  - [<progress>](#progress)
- [Usage](#usage)
  - [Controlling a progress indicator](#controlling-a-progress-indicator)

---

## Reference

### <progress>

To display a progress indicator, render the [built-in browser<progress>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress) component.

 $

```
<progress value={0.5} />
```

/$

[See more examples below.](#usage)

#### Props

`<progress>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

Additionally, `<progress>` supports these props:

- [max](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress#max): A number. Specifies the maximum `value`. Defaults to `1`.
- [value](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress#value): A number between `0` and `max`, or `null` for indeterminate progress. Specifies how much was done.

---

## Usage

### Controlling a progress indicator

To display a progress indicator, render a `<progress>` component. You can pass a number `value` between `0` and the `max` value you specify. If you don’t pass a `max` value, it will assumed to be `1` by default.

If the operation is not ongoing, pass `value={null}` to put the progress indicator into an indeterminate state.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function App() {
  return (
    <>
      <progress value={0} />
      <progress value={0.5} />
      <progress value={0.7} />
      <progress value={75} max={100} />
      <progress value={1} />
      <progress value={null} />
    </>
  );
}
```

/$[Previous<option>](https://react.dev/reference/react-dom/components/option)[Next<select>](https://react.dev/reference/react-dom/components/select)

---

# <script>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <script>

The [built-in browser<script>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script) lets you add a script to your document.

$

```
<script> alert("hi!") </script>
```

/$

- [Reference](#reference)
  - [<script>](#script)
- [Usage](#usage)
  - [Rendering an external script](#rendering-an-external-script)
  - [Rendering an inline script](#rendering-an-inline-script)

---

## Reference

### <script>

To add inline or external scripts to your document, render the [built-in browser<script>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script). You can render `<script>` from any component and React will [in certain cases](#special-rendering-behavior) place the corresponding DOM element in the document head and de-duplicate identical scripts.

 $

```
<script> alert("hi!") </script><script src="script.js" />
```

/$

[See more examples below.](#usage)

#### Props

`<script>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

It should have *either* `children` or a `src` prop.

- `children`: a string. The source code of an inline script.
- `src`: a string. The URL of an external script.

Other supported props:

- `async`: a boolean. Allows the browser to defer execution of the script until the rest of the document has been processed — the preferred behavior for performance.
- `crossOrigin`: a string. The [CORS policy](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) to use. Its possible values are `anonymous` and `use-credentials`.
- `fetchPriority`: a string. Lets the browser rank scripts in priority when fetching multiple scripts at the same time. Can be `"high"`, `"low"`, or `"auto"` (the default).
- `integrity`: a string. A cryptographic hash of the script, to [verify its authenticity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
- `noModule`: a boolean. Disables the script in browsers that support ES modules — allowing for a fallback script for browsers that do not.
- `nonce`: a string. A cryptographic [nonce to allow the resource](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) when using a strict Content Security Policy.
- `referrer`: a string. Says [what Referer header to send](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#referrerpolicy) when fetching the script and any resources that the script fetches in turn.
- `type`: a string. Says whether the script is a [classic script, ES module, or import map](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type).

Props that disable React’s [special treatment of scripts](#special-rendering-behavior):

- `onError`: a function. Called when the script fails to load.
- `onLoad`: a function. Called when the script finishes being loaded.

Props that are **not recommended** for use with React:

- `blocking`: a string. If set to `"render"`, instructs the browser not to render the page until the scriptsheet is loaded. React provides more fine-grained control using Suspense.
- `defer`: a string. Prevents the browser from executing the script until the document is done loading. Not compatible with streaming server-rendered components. Use the `async` prop instead.

#### Special rendering behavior

React can move `<script>` components to the document’s `<head>` and de-duplicate identical scripts.

To opt into this behavior, provide the `src` and `async={true}` props. React will de-duplicate scripts if they have the same `src`. The `async` prop must be true to allow scripts to be safely moved.

This special treatment comes with two caveats:

- React will ignore changes to props after the script has been rendered. (React will issue a warning in development if this happens.)
- React may leave the script in the DOM even after the component that rendered it has been unmounted. (This has no effect as scripts just execute once when they are inserted into the DOM.)

---

## Usage

### Rendering an external script

If a component depends on certain scripts in order to be displayed correctly, you can render a `<script>` within the component.
However, the component might be committed before the script has finished loading.
You can start depending on the script content once the `load` event is fired e.g. by using the `onLoad` prop.

React will de-duplicate scripts that have the same `src`, inserting only one of them into the DOM even if multiple components render it.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

function Map({lat, long}) {
  return (
    <>
      <script async src="map-api.js" onLoad={() => console.log('script loaded')} />
      <div id="map" data-lat={lat} data-long={long} />
    </>
  );
}

export default function Page() {
  return (
    <ShowRenderedHTML>
      <Map />
    </ShowRenderedHTML>
  );
}
```

/$

### Note

When you want to use a script, it can be beneficial to call the [preinit](https://react.dev/reference/react-dom/preinit) function. Calling this function may allow the browser to start fetching the script earlier than if you just render a `<script>` component, for example by sending an [HTTP Early Hints response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103).

### Rendering an inline script

To include an inline script, render the `<script>` component with the script source code as its children. Inline scripts are not de-duplicated or moved to the document `<head>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

function Tracking() {
  return (
    <script>
      ga('send', 'pageview');
    </script>
  );
}

export default function Page() {
  return (
    <ShowRenderedHTML>
      <h1>My Website</h1>
      <Tracking />
      <p>Welcome</p>
    </ShowRenderedHTML>
  );
}
```

/$[Previous<meta>](https://react.dev/reference/react-dom/components/meta)[Next<style>](https://react.dev/reference/react-dom/components/style)

---

# <select>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <select>

The [built-in browser<select>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) lets you render a select box with options.

$

```
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

/$

- [Reference](#reference)
  - [<select>](#select)
- [Usage](#usage)
  - [Displaying a select box with options](#displaying-a-select-box-with-options)
  - [Providing a label for a select box](#providing-a-label-for-a-select-box)
  - [Providing an initially selected option](#providing-an-initially-selected-option)
  - [Enabling multiple selection](#enabling-multiple-selection)
  - [Reading the select box value when submitting a form](#reading-the-select-box-value-when-submitting-a-form)
  - [Controlling a select box with a state variable](#controlling-a-select-box-with-a-state-variable)

---

## Reference

### <select>

To display a select box, render the [built-in browser<select>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) component.

 $

```
<select>  <option value="someOption">Some option</option>  <option value="otherOption">Other option</option></select>
```

/$

[See more examples below.](#usage)

#### Props

`<select>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

You can [make a select box controlled](#controlling-a-select-box-with-a-state-variable) by passing a `value` prop:

- `value`: A string (or an array of strings for [multiple={true}](#enabling-multiple-selection)). Controls which option is selected. Every value string match the `value` of some `<option>` nested inside the `<select>`.

When you pass `value`, you must also pass an `onChange` handler that updates the passed value.

If your `<select>` is uncontrolled, you may pass the `defaultValue` prop instead:

- `defaultValue`: A string (or an array of strings for [multiple={true}](#enabling-multiple-selection)). Specifies [the initially selected option.](#providing-an-initially-selected-option)

These `<select>` props are relevant both for uncontrolled and controlled select boxes:

- [autoComplete](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#autocomplete): A string. Specifies one of the possible [autocomplete behaviors.](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete#values)
- [autoFocus](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#autofocus): A boolean. If `true`, React will focus the element on mount.
- `children`: `<select>` accepts [<option>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/option), [<optgroup>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/optgroup), and [<datalist>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist) components as children. You can also pass your own components as long as they eventually render one of the allowed components. If you pass your own components that eventually render `<option>` tags, each `<option>` you render must have a `value`.
- [disabled](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#disabled): A boolean. If `true`, the select box will not be interactive and will appear dimmed.
- [form](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#form): A string. Specifies the `id` of the `<form>` this select box belongs to. If omitted, it’s the closest parent form.
- [multiple](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#multiple): A boolean. If `true`, the browser allows [multiple selection.](#enabling-multiple-selection)
- [name](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#name): A string. Specifies the name for this select box that’s [submitted with the form.](#reading-the-select-box-value-when-submitting-a-form)
- `onChange`: An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Required for [controlled select boxes.](#controlling-a-select-box-with-a-state-variable) Fires immediately when the user picks a different option. Behaves like the browser [inputevent.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event)
- `onChangeCapture`: A version of `onChange` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInput](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires immediately when the value is changed by the user. For historical reasons, in React it is idiomatic to use `onChange` instead which works similarly.
- `onInputCapture`: A version of `onInput` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInvalid](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/invalid_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires if an input fails validation on form submit. Unlike the built-in `invalid` event, the React `onInvalid` event bubbles.
- `onInvalidCapture`: A version of `onInvalid` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [required](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#required): A boolean. If `true`, the value must be provided for the form to submit.
- [size](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select#size): A number. For `multiple={true}` selects, specifies the preferred number of initially visible items.

#### Caveats

- Unlike in HTML, passing a `selected` attribute to `<option>` is not supported. Instead, use [<select defaultValue>](#providing-an-initially-selected-option) for uncontrolled select boxes and [<select value>](#controlling-a-select-box-with-a-state-variable) for controlled select boxes.
- If a select box receives a `value` prop, it will be [treated as controlled.](#controlling-a-select-box-with-a-state-variable)
- A select box can’t be both controlled and uncontrolled at the same time.
- A select box cannot switch between being controlled or uncontrolled over its lifetime.
- Every controlled select box needs an `onChange` event handler that synchronously updates its backing value.

---

## Usage

### Displaying a select box with options

Render a `<select>` with a list of `<option>` components inside to display a select box. Give each `<option>` a `value` representing the data to be submitted with the form.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function FruitPicker() {
  return (
    <label>
      Pick a fruit:
      <select name="selectedFruit">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

/$

---

### Providing a label for a select box

Typically, you will place every `<select>` inside a [<label>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) tag. This tells the browser that this label is associated with that select box. When the user clicks the label, the browser will automatically focus the select box. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the select box.

If you can’t nest `<select>` into a `<label>`, associate them by passing the same ID to `<select id>` and [<label htmlFor>.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement/htmlFor) To avoid conflicts between multiple instances of one component, generate such an ID with [useId.](https://react.dev/reference/react/useId)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useId } from 'react';

export default function Form() {
  const vegetableSelectId = useId();
  return (
    <>
      <label>
        Pick a fruit:
        <select name="selectedFruit">
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <hr />
      <label htmlFor={vegetableSelectId}>
        Pick a vegetable:
      </label>
      <select id={vegetableSelectId} name="selectedVegetable">
        <option value="cucumber">Cucumber</option>
        <option value="corn">Corn</option>
        <option value="tomato">Tomato</option>
      </select>
    </>
  );
}
```

/$

---

### Providing an initially selected option

By default, the browser will select the first `<option>` in the list. To select a different option by default, pass that `<option>`’s `value` as the `defaultValue` to the `<select>` element.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function FruitPicker() {
  return (
    <label>
      Pick a fruit:
      <select name="selectedFruit" defaultValue="orange">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

/$

### Pitfall

Unlike in HTML, passing a `selected` attribute to an individual `<option>` is not supported.

---

### Enabling multiple selection

Pass `multiple={true}` to the `<select>` to let the user select multiple options. In that case, if you also specify `defaultValue` to choose the initially selected options, it must be an array.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function FruitPicker() {
  return (
    <label>
      Pick some fruits:
      <select
        name="selectedFruit"
        defaultValue={['orange', 'banana']}
        multiple={true}
      >
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

/$

---

### Reading the select box value when submitting a form

Add a [<form>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) around your select box with a [<button type="submit">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) inside. It will call your `<form onSubmit>` event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling `e.preventDefault()`. Read the form data with [new FormData(e.target)](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function EditPost() {
  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();
    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    // You can pass formData as a fetch body directly:
    fetch('/some-api', { method: form.method, body: formData });
    // You can generate a URL out of it, as the browser does by default:
    console.log(new URLSearchParams(formData).toString());
    // You can work with it as a plain object.
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson); // (!) This doesn't include multiple select values
    // Or you can get an array of name-value pairs.
    console.log([...formData.entries()]);
  }

  return (
    <form method="post" onSubmit={handleSubmit}>
      <label>
        Pick your favorite fruit:
        <select name="selectedFruit" defaultValue="orange">
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <label>
        Pick all your favorite vegetables:
        <select
          name="selectedVegetables"
          multiple={true}
          defaultValue={['corn', 'tomato']}
        >
          <option value="cucumber">Cucumber</option>
          <option value="corn">Corn</option>
          <option value="tomato">Tomato</option>
        </select>
      </label>
      <hr />
      <button type="reset">Reset</button>
      <button type="submit">Submit</button>
    </form>
  );
}
```

/$

### Note

Give a `name` to your `<select>`, for example `<select name="selectedFruit" />`. The `name` you specified will be used as a key in the form data, for example `{ selectedFruit: "orange" }`.

If you use `<select multiple={true}>`, the [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) you’ll read from the form will include each selected value as a separate name-value pair. Look closely at the console logs in the example above.

### Pitfall

By default, *any* `<button>` inside a `<form>` will submit it. This can be surprising! If you have your own custom `Button` React component, consider returning [<button type="button">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/button) instead of `<button>`. Then, to be explicit, use `<button type="submit">` for buttons that *are* supposed to submit the form.

---

### Controlling a select box with a state variable

A select box like `<select />` is *uncontrolled.* Even if you [pass an initially selected value](#providing-an-initially-selected-option) like `<select defaultValue="orange" />`, your JSX only specifies the initial value, not the value right now.

**To render acontrolledselect box, pass thevalueprop to it.** React will force the select box to always have the `value` you passed. Typically, you will control a select box by declaring a [state variable:](https://react.dev/reference/react/useState)

 $

```
function FruitPicker() {  const [selectedFruit, setSelectedFruit] = useState('orange'); // Declare a state variable...  // ...  return (    <select      value={selectedFruit} // ...force the select's value to match the state variable...      onChange={e => setSelectedFruit(e.target.value)} // ... and update the state variable on any change!    >      <option value="apple">Apple</option>      <option value="banana">Banana</option>      <option value="orange">Orange</option>    </select>  );}
```

/$

This is useful if you want to re-render some part of the UI in response to every selection.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function FruitPicker() {
  const [selectedFruit, setSelectedFruit] = useState('orange');
  const [selectedVegs, setSelectedVegs] = useState(['corn', 'tomato']);
  return (
    <>
      <label>
        Pick a fruit:
        <select
          value={selectedFruit}
          onChange={e => setSelectedFruit(e.target.value)}
        >
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <hr />
      <label>
        Pick all your favorite vegetables:
        <select
          multiple={true}
          value={selectedVegs}
          onChange={e => {
            const options = [...e.target.selectedOptions];
            const values = options.map(option => option.value);
            setSelectedVegs(values);
          }}
        >
          <option value="cucumber">Cucumber</option>
          <option value="corn">Corn</option>
          <option value="tomato">Tomato</option>
        </select>
      </label>
      <hr />
      <p>Your favorite fruit: {selectedFruit}</p>
      <p>Your favorite vegetables: {selectedVegs.join(', ')}</p>
    </>
  );
}
```

/$

### Pitfall

**If you passvaluewithoutonChange, it will be impossible to select an option.** When you control a select box by passing some `value` to it, you *force* it to always have the value you passed. So if you pass a state variable as a `value` but forget to update that state variable synchronously during the `onChange` event handler, React will revert the select box after every keystroke back to the `value` that you specified.

Unlike in HTML, passing a `selected` attribute to an individual `<option>` is not supported.

[Previous<progress>](https://react.dev/reference/react-dom/components/progress)[Next<textarea>](https://react.dev/reference/react-dom/components/textarea)

---

# <style>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <style>

The [built-in browser<style>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style) lets you add inline CSS stylesheets to your document.

$

```
<style>{` p { color: red; } `}</style>
```

/$

- [Reference](#reference)
  - [<style>](#style)
- [Usage](#usage)
  - [Rendering an inline CSS stylesheet](#rendering-an-inline-css-stylesheet)

---

## Reference

### <style>

To add inline styles to your document, render the [built-in browser<style>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style). You can render `<style>` from any component and React will [in certain cases](#special-rendering-behavior) place the corresponding DOM element in the document head and de-duplicate identical styles.

 $

```
<style>{` p { color: red; } `}</style>
```

/$

[See more examples below.](#usage)

#### Props

`<style>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

- `children`: a string, required. The contents of the stylesheet.
- `precedence`: a string. Tells React where to rank the `<style>` DOM node relative to others in the document `<head>`, which determines which stylesheet can override the other. React will infer that precedence values it discovers first are “lower” and precedence values it discovers later are “higher”. Many style systems can work fine using a single precedence value because style rules are atomic. Stylesheets with the same precedence go together whether they are `<link>` or inline `<style>` tags or loaded using [preinit](https://react.dev/reference/react-dom/preinit) functions.
- `href`: a string. Allows React to [de-duplicate styles](#special-rendering-behavior) that have the same `href`.
- `media`: a string. Restricts the stylesheet to a certain [media query](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries).
- `nonce`: a string. A cryptographic [nonce to allow the resource](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) when using a strict Content Security Policy.
- `title`: a string. Specifies the name of an [alternative stylesheet](https://developer.mozilla.org/en-US/docs/Web/CSS/Alternative_style_sheets).

Props that are **not recommended** for use with React:

- `blocking`: a string. If set to `"render"`, instructs the browser not to render the page until the stylesheet is loaded. React provides more fine-grained control using Suspense.

#### Special rendering behavior

React can move `<style>` components to the document’s `<head>`, de-duplicate identical stylesheets, and [suspend](https://react.dev/reference/react/Suspense) while the stylesheet is loading.

To opt into this behavior, provide the `href` and `precedence` props. React will de-duplicate styles if they have the same `href`. The precedence prop tells React where to rank the `<style>` DOM node relative to others in the document `<head>`, which determines which stylesheet can override the other.

This special treatment comes with three caveats:

- React will ignore changes to props after the style has been rendered. (React will issue a warning in development if this happens.)
- React will drop all extraneous props when using the `precedence` prop (beyond `href` and `precedence`).
- React may leave the style in the DOM even after the component that rendered it has been unmounted.

---

## Usage

### Rendering an inline CSS stylesheet

If a component depends on certain CSS styles in order to be displayed correctly, you can render an inline stylesheet within the component.

The `href` prop should uniquely identify the stylesheet, because React will de-duplicate stylesheets that have the same `href`.
If you supply a `precedence` prop, React will reorder inline stylesheets based on the order these values appear in the component tree.

Inline stylesheets will not trigger Suspense boundaries while they’re loading.
Even if they load async resources like fonts or images.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';
import { useId } from 'react';

function PieChart({data, colors}) {
  const id = useId();
  const stylesheet = colors.map((color, index) =>
    `#${id} .color-${index}: \{ color: "${color}"; \}`
  ).join();
  return (
    <>
      <style href={"PieChart-" + JSON.stringify(colors)} precedence="medium">
        {stylesheet}
      </style>
      <svg id={id}>
        …
      </svg>
    </>
  );
}

export default function App() {
  return (
    <ShowRenderedHTML>
      <PieChart data="..." colors={['red', 'green', 'blue']} />
    </ShowRenderedHTML>
  );
}
```

/$[Previous<script>](https://react.dev/reference/react-dom/components/script)[Next<title>](https://react.dev/reference/react-dom/components/title)

---

# <textarea>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <textarea>

The [built-in browser<textarea>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea) lets you render a multiline text input.

$

```
<textarea />
```

/$

- [Reference](#reference)
  - [<textarea>](#textarea)
- [Usage](#usage)
  - [Displaying a text area](#displaying-a-text-area)
  - [Providing a label for a text area](#providing-a-label-for-a-text-area)
  - [Providing an initial value for a text area](#providing-an-initial-value-for-a-text-area)
  - [Reading the text area value when submitting a form](#reading-the-text-area-value-when-submitting-a-form)
  - [Controlling a text area with a state variable](#controlling-a-text-area-with-a-state-variable)
- [Troubleshooting](#troubleshooting)
  - [My text area doesn’t update when I type into it](#my-text-area-doesnt-update-when-i-type-into-it)
  - [My text area caret jumps to the beginning on every keystroke](#my-text-area-caret-jumps-to-the-beginning-on-every-keystroke)
  - [I’m getting an error: “A component is changing an uncontrolled input to be controlled”](#im-getting-an-error-a-component-is-changing-an-uncontrolled-input-to-be-controlled)

---

## Reference

### <textarea>

To display a text area, render the [built-in browser<textarea>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea) component.

 $

```
<textarea name="postContent" />
```

/$

[See more examples below.](#usage)

#### Props

`<textarea>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

You can [make a text area controlled](#controlling-a-text-area-with-a-state-variable) by passing a `value` prop:

- `value`: A string. Controls the text inside the text area.

When you pass `value`, you must also pass an `onChange` handler that updates the passed value.

If your `<textarea>` is uncontrolled, you may pass the `defaultValue` prop instead:

- `defaultValue`: A string. Specifies [the initial value](#providing-an-initial-value-for-a-text-area) for a text area.

These `<textarea>` props are relevant both for uncontrolled and controlled text areas:

- [autoComplete](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#autocomplete): Either `'on'` or `'off'`. Specifies the autocomplete behavior.
- [autoFocus](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#autofocus): A boolean. If `true`, React will focus the element on mount.
- `children`: `<textarea>` does not accept children. To set the initial value, use `defaultValue`.
- [cols](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#cols): A number. Specifies the default width in average character widths. Defaults to `20`.
- [disabled](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#disabled): A boolean. If `true`, the input will not be interactive and will appear dimmed.
- [form](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#form): A string. Specifies the `id` of the `<form>` this input belongs to. If omitted, it’s the closest parent form.
- [maxLength](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#maxlength): A number. Specifies the maximum length of text.
- [minLength](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#minlength): A number. Specifies the minimum length of text.
- [name](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#name): A string. Specifies the name for this input that’s [submitted with the form.](#reading-the-textarea-value-when-submitting-a-form)
- `onChange`: An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Required for [controlled text areas.](#controlling-a-text-area-with-a-state-variable) Fires immediately when the input’s value is changed by the user (for example, it fires on every keystroke). Behaves like the browser [inputevent.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event)
- `onChangeCapture`: A version of `onChange` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInput](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires immediately when the value is changed by the user. For historical reasons, in React it is idiomatic to use `onChange` instead which works similarly.
- `onInputCapture`: A version of `onInput` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInvalid](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/invalid_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires if an input fails validation on form submit. Unlike the built-in `invalid` event, the React `onInvalid` event bubbles.
- `onInvalidCapture`: A version of `onInvalid` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onSelect](https://developer.mozilla.org/en-US/docs/Web/API/HTMLTextAreaElement/select_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires after the selection inside the `<textarea>` changes. React extends the `onSelect` event to also fire for empty selection and on edits (which may affect the selection).
- `onSelectCapture`: A version of `onSelect` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [placeholder](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#placeholder): A string. Displayed in a dimmed color when the text area value is empty.
- [readOnly](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#readonly): A boolean. If `true`, the text area is not editable by the user.
- [required](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#required): A boolean. If `true`, the value must be provided for the form to submit.
- [rows](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#rows): A number. Specifies the default height in average character heights. Defaults to `2`.
- [wrap](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#wrap): Either `'hard'`, `'soft'`, or `'off'`. Specifies how the text should be wrapped when submitting a form.

#### Caveats

- Passing children like `<textarea>something</textarea>` is not allowed. [UsedefaultValuefor initial content.](#providing-an-initial-value-for-a-text-area)
- If a text area receives a string `value` prop, it will be [treated as controlled.](#controlling-a-text-area-with-a-state-variable)
- A text area can’t be both controlled and uncontrolled at the same time.
- A text area cannot switch between being controlled or uncontrolled over its lifetime.
- Every controlled text area needs an `onChange` event handler that synchronously updates its backing value.

---

## Usage

### Displaying a text area

Render `<textarea>` to display a text area. You can specify its default size with the [rows](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#rows) and [cols](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea#cols) attributes, but by default the user will be able to resize it. To disable resizing, you can specify `resize: none` in the CSS.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function NewPost() {
  return (
    <label>
      Write your post:
      <textarea name="postContent" rows={4} cols={40} />
    </label>
  );
}
```

/$

---

### Providing a label for a text area

Typically, you will place every `<textarea>` inside a [<label>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) tag. This tells the browser that this label is associated with that text area. When the user clicks the label, the browser will focus the text area. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the text area.

If you can’t nest `<textarea>` into a `<label>`, associate them by passing the same ID to `<textarea id>` and [<label htmlFor>.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement/htmlFor) To avoid conflicts between instances of one component, generate such an ID with [useId.](https://react.dev/reference/react/useId)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useId } from 'react';

export default function Form() {
  const postTextAreaId = useId();
  return (
    <>
      <label htmlFor={postTextAreaId}>
        Write your post:
      </label>
      <textarea
        id={postTextAreaId}
        name="postContent"
        rows={4}
        cols={40}
      />
    </>
  );
}
```

/$

---

### Providing an initial value for a text area

You can optionally specify the initial value for the text area. Pass it as the `defaultValue` string.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function EditPost() {
  return (
    <label>
      Edit your post:
      <textarea
        name="postContent"
        defaultValue="I really enjoyed biking yesterday!"
        rows={4}
        cols={40}
      />
    </label>
  );
}
```

/$

### Pitfall

Unlike in HTML, passing initial text like `<textarea>Some content</textarea>` is not supported.

---

### Reading the text area value when submitting a form

Add a [<form>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) around your textarea with a [<button type="submit">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) inside. It will call your `<form onSubmit>` event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling `e.preventDefault()`. Read the form data with [new FormData(e.target)](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function EditPost() {
  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target;
    const formData = new FormData(form);

    // You can pass formData as a fetch body directly:
    fetch('/some-api', { method: form.method, body: formData });

    // Or you can work with it as a plain object:
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson);
  }

  return (
    <form method="post" onSubmit={handleSubmit}>
      <label>
        Post title: <input name="postTitle" defaultValue="Biking" />
      </label>
      <label>
        Edit your post:
        <textarea
          name="postContent"
          defaultValue="I really enjoyed biking yesterday!"
          rows={4}
          cols={40}
        />
      </label>
      <hr />
      <button type="reset">Reset edits</button>
      <button type="submit">Save post</button>
    </form>
  );
}
```

/$

### Note

Give a `name` to your `<textarea>`, for example `<textarea name="postContent" />`. The `name` you specified will be used as a key in the form data, for example `{ postContent: "Your post" }`.

### Pitfall

By default, *any* `<button>` inside a `<form>` will submit it. This can be surprising! If you have your own custom `Button` React component, consider returning [<button type="button">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/button) instead of `<button>`. Then, to be explicit, use `<button type="submit">` for buttons that *are* supposed to submit the form.

---

### Controlling a text area with a state variable

A text area like `<textarea />` is *uncontrolled.* Even if you [pass an initial value](#providing-an-initial-value-for-a-text-area) like `<textarea defaultValue="Initial text" />`, your JSX only specifies the initial value, not the value right now.

**To render acontrolledtext area, pass thevalueprop to it.** React will force the text area to always have the `value` you passed. Typically, you will control a text area by declaring a [state variable:](https://react.dev/reference/react/useState)

 $

```
function NewPost() {  const [postContent, setPostContent] = useState(''); // Declare a state variable...  // ...  return (    <textarea      value={postContent} // ...force the input's value to match the state variable...      onChange={e => setPostContent(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

/$

This is useful if you want to re-render some part of the UI in response to every keystroke.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
{
  "dependencies": {
    "react": "latest",
    "react-dom": "latest",
    "react-scripts": "latest",
    "remarkable": "2.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --env=jsdom",
    "eject": "react-scripts eject"
  },
  "devDependencies": {}
}
```

/$

### Pitfall

**If you passvaluewithoutonChange, it will be impossible to type into the text area.** When you control a text area by passing some `value` to it, you *force* it to always have the value you passed. So if you pass a state variable as a `value` but forget to update that state variable synchronously during the `onChange` event handler, React will revert the text area after every keystroke back to the `value` that you specified.

---

## Troubleshooting

### My text area doesn’t update when I type into it

If you render a text area with `value` but no `onChange`, you will see an error in the console:

 $

```
// 🔴 Bug: controlled text area with no onChange handler<textarea value={something} />
```

/$ ConsoleYou provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`.

As the error message suggests, if you only wanted to [specify theinitialvalue,](#providing-an-initial-value-for-a-text-area) pass `defaultValue` instead:

 $

```
// ✅ Good: uncontrolled text area with an initial value<textarea defaultValue={something} />
```

/$

If you want [to control this text area with a state variable,](#controlling-a-text-area-with-a-state-variable) specify an `onChange` handler:

 $

```
// ✅ Good: controlled text area with onChange<textarea value={something} onChange={e => setSomething(e.target.value)} />
```

/$

If the value is intentionally read-only, add a `readOnly` prop to suppress the error:

 $

```
// ✅ Good: readonly controlled text area without on change<textarea value={something} readOnly={true} />
```

/$

---

### My text area caret jumps to the beginning on every keystroke

If you [control a text area,](#controlling-a-text-area-with-a-state-variable) you must update its state variable to the text area’s value from the DOM during `onChange`.

You can’t update it to something other than `e.target.value`:

 $

```
function handleChange(e) {  // 🔴 Bug: updating an input to something other than e.target.value  setFirstName(e.target.value.toUpperCase());}
```

/$

You also can’t update it asynchronously:

 $

```
function handleChange(e) {  // 🔴 Bug: updating an input asynchronously  setTimeout(() => {    setFirstName(e.target.value);  }, 100);}
```

/$

To fix your code, update it synchronously to `e.target.value`:

 $

```
function handleChange(e) {  // ✅ Updating a controlled input to e.target.value synchronously  setFirstName(e.target.value);}
```

/$

If this doesn’t fix the problem, it’s possible that the text area gets removed and re-added from the DOM on every keystroke. This can happen if you’re accidentally [resetting state](https://react.dev/learn/preserving-and-resetting-state) on every re-render. For example, this can happen if the text area or one of its parents always receives a different `key` attribute, or if you nest component definitions (which is not allowed in React and causes the “inner” component to remount on every render).

---

### I’m getting an error: “A component is changing an uncontrolled input to be controlled”

If you provide a `value` to the component, it must remain a string throughout its lifetime.

You cannot pass `value={undefined}` first and later pass `value="some string"` because React won’t know whether you want the component to be uncontrolled or controlled. A controlled component should always receive a string `value`, not `null` or `undefined`.

If your `value` is coming from an API or a state variable, it might be initialized to `null` or `undefined`. In that case, either set it to an empty string (`''`) initially, or pass `value={someValue ?? ''}` to ensure `value` is a string.

[Previous<select>](https://react.dev/reference/react-dom/components/select)[Next<link>](https://react.dev/reference/react-dom/components/link)
