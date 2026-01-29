# <form> and more

# <form>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <form>

The [built-in browser<form>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) lets you create interactive controls for submitting information.

$

```
<form action={search}>    <input name="query" />    <button type="submit">Search</button></form>
```

/$

- [Reference](#reference)
  - [<form>](#form)
- [Usage](#usage)
  - [Handle form submission on the client](#handle-form-submission-on-the-client)
  - [Handle form submission with a Server Function](#handle-form-submission-with-a-server-function)
  - [Display a pending state during form submission](#display-a-pending-state-during-form-submission)
  - [Optimistically updating form data](#optimistically-updating-form-data)
  - [Handling form submission errors](#handling-form-submission-errors)
  - [Display a form submission error without JavaScript](#display-a-form-submission-error-without-javascript)
  - [Handling multiple submission types](#handling-multiple-submission-types)

---

## Reference

### <form>

To create interactive controls for submitting information, render the [built-in browser<form>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form).

 $

```
<form action={search}>    <input name="query" />    <button type="submit">Search</button></form>
```

/$

[See more examples below.](#usage)

#### Props

`<form>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

[action](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#action): a URL or function. When a URL is passed to `action` the form will behave like the HTML form component. When a function is passed to `action` the function will handle the form submission in a Transition following [the Action prop pattern](https://react.dev/reference/react/useTransition#exposing-action-props-from-components). The function passed to `action` may be async and will be called with a single argument containing the [form data](https://developer.mozilla.org/en-US/docs/Web/API/FormData) of the submitted form. The `action` prop can be overridden by a `formAction` attribute on a `<button>`, `<input type="submit">`, or `<input type="image">` component.

#### Caveats

- When a function is passed to `action` or `formAction` the HTTP method will be POST regardless of value of the `method` prop.

---

## Usage

### Handle form submission on the client

Pass a function to the `action` prop of form to run the function when the form is submitted. [formData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) will be passed to the function as an argument so you can access the data submitted by the form. This differs from the conventional [HTML action](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#action), which only accepts URLs. After the `action` function succeeds, all uncontrolled field elements in the form are reset.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Search() {
  function search(formData) {
    const query = formData.get("query");
    alert(`You searched for '${query}'`);
  }
  return (
    <form action={search}>
      <input name="query" />
      <button type="submit">Search</button>
    </form>
  );
}
```

/$

### Handle form submission with a Server Function

Render a `<form>` with an input and submit button. Pass a Server Function (a function marked with ['use server'](https://react.dev/reference/rsc/use-server)) to the `action` prop of form to run the function when the form is submitted.

Passing a Server Function to `<form action>` allow users to submit forms without JavaScript enabled or before the code has loaded. This is beneficial to users who have a slow connection, device, or have JavaScript disabled and is similar to the way forms work when a URL is passed to the `action` prop.

You can use hidden form fields to provide data to the `<form>`’s action. The Server Function will be called with the hidden form field data as an instance of [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

 $

```
import { updateCart } from './lib.js';function AddToCart({productId}) {  async function addToCart(formData) {    'use server'    const productId = formData.get('productId')    await updateCart(productId)  }  return (    <form action={addToCart}>        <input type="hidden" name="productId" value={productId} />        <button type="submit">Add to Cart</button>    </form>  );}
```

/$

In lieu of using hidden form fields to provide data to the `<form>`’s action, you can call the `bind` method to supply it with extra arguments. This will bind a new argument (`productId`) to the function in addition to the `formData` that is passed as an argument to the function.

 $

```
import { updateCart } from './lib.js';function AddToCart({productId}) {  async function addToCart(productId, formData) {    "use server";    await updateCart(productId)  }  const addProductToCart = addToCart.bind(null, productId);  return (    <form action={addProductToCart}>      <button type="submit">Add to Cart</button>    </form>  );}
```

/$

When `<form>` is rendered by a [Server Component](https://react.dev/reference/rsc/use-client), and a [Server Function](https://react.dev/reference/rsc/server-functions) is passed to the `<form>`’s `action` prop, the form is [progressively enhanced](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement).

### Display a pending state during form submission

To display a pending state when a form is being submitted, you can call the `useFormStatus` Hook in a component rendered in a `<form>` and read the `pending` property returned.

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

To learn more about the `useFormStatus` Hook see the [reference documentation](https://react.dev/reference/react-dom/hooks/useFormStatus).

### Optimistically updating form data

The `useOptimistic` Hook provides a way to optimistically update the user interface before a background operation, like a network request, completes. In the context of forms, this technique helps to make apps feel more responsive. When a user submits a form, instead of waiting for the server’s response to reflect the changes, the interface is immediately updated with the expected outcome.

For example, when a user types a message into the form and hits the “Send” button, the `useOptimistic` Hook allows the message to immediately appear in the list with a “Sending…” label, even before the message is actually sent to a server. This “optimistic” approach gives the impression of speed and responsiveness. The form then attempts to truly send the message in the background. Once the server confirms the message has been received, the “Sending…” label is removed.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useOptimistic, useState, useRef } from "react";
import { deliverMessage } from "./actions.js";

function Thread({ messages, sendMessage }) {
  const formRef = useRef();
  async function formAction(formData) {
    addOptimisticMessage(formData.get("message"));
    formRef.current.reset();
    await sendMessage(formData);
  }
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [
      ...state,
      {
        text: newMessage,
        sending: true
      }
    ]
  );

  return (
    <>
      {optimisticMessages.map((message, index) => (
        <div key={index}>
          {message.text}
          {!!message.sending && <small> (Sending...)</small>}
        </div>
      ))}
      <form action={formAction} ref={formRef}>
        <input type="text" name="message" placeholder="Hello!" />
        <button type="submit">Send</button>
      </form>
    </>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    { text: "Hello there!", sending: false, key: 1 }
  ]);
  async function sendMessage(formData) {
    const sentMessage = await deliverMessage(formData.get("message"));
    setMessages((messages) => [...messages, { text: sentMessage }]);
  }
  return <Thread messages={messages} sendMessage={sendMessage} />;
}
```

/$

### Handling form submission errors

In some cases the function called by a `<form>`’s `action` prop throws an error. You can handle these errors by wrapping `<form>` in an Error Boundary. If the function called by a `<form>`’s `action` prop throws an error, the fallback for the error boundary will be displayed.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { ErrorBoundary } from "react-error-boundary";

export default function Search() {
  function search() {
    throw new Error("search error");
  }
  return (
    <ErrorBoundary
      fallback={<p>There was an error while submitting the form</p>}
    >
      <form action={search}>
        <input name="query" />
        <button type="submit">Search</button>
      </form>
    </ErrorBoundary>
  );
}
```

/$

### Display a form submission error without JavaScript

Displaying a form submission error message before the JavaScript bundle loads for progressive enhancement requires that:

1. `<form>` be rendered by a [Client Component](https://react.dev/reference/rsc/use-client)
2. the function passed to the `<form>`’s `action` prop be a [Server Function](https://react.dev/reference/rsc/server-functions)
3. the `useActionState` Hook be used to display the error message

`useActionState` takes two parameters: a [Server Function](https://react.dev/reference/rsc/server-functions) and an initial state. `useActionState` returns two values, a state variable and an action. The action returned by `useActionState` should be passed to the `action` prop of the form. The state variable returned by `useActionState` can be used to display an error message. The value returned by the Server Function passed to `useActionState` will be used to update the state variable.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useActionState } from "react";
import { signUpNewUser } from "./api";

export default function Page() {
  async function signup(prevState, formData) {
    "use server";
    const email = formData.get("email");
    try {
      await signUpNewUser(email);
      alert(`Added "${email}"`);
    } catch (err) {
      return err.toString();
    }
  }
  const [message, signupAction] = useActionState(signup, null);
  return (
    <>
      <h1>Signup for my newsletter</h1>
      <p>Signup with the same email twice to see an error</p>
      <form action={signupAction} id="signup-form">
        <label htmlFor="email">Email: </label>
        <input name="email" id="email" placeholder="react@example.com" />
        <button>Sign up</button>
        {!!message && <p>{message}</p>}
      </form>
    </>
  );
}
```

/$

Learn more about updating state from a form action with the [useActionState](https://react.dev/reference/react/useActionState) docs

### Handling multiple submission types

Forms can be designed to handle multiple submission actions based on the button pressed by the user. Each button inside a form can be associated with a distinct action or behavior by setting the `formAction` prop.

When a user taps a specific button, the form is submitted, and a corresponding action, defined by that button’s attributes and action, is executed. For instance, a form might submit an article for review by default but have a separate button with `formAction` set to save the article as a draft.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Search() {
  function publish(formData) {
    const content = formData.get("content");
    const button = formData.get("button");
    alert(`'${content}' was published with the '${button}' button`);
  }

  function save(formData) {
    const content = formData.get("content");
    alert(`Your draft of '${content}' has been saved!`);
  }

  return (
    <form action={publish}>
      <textarea name="content" rows={4} cols={40} />
      <br />
      <button type="submit" name="button" value="submit">Publish</button>
      <button formAction={save}>Save draft</button>
    </form>
  );
}
```

/$[PreviousCommon (e.g. <div>)](https://react.dev/reference/react-dom/components/common)[Next<input>](https://react.dev/reference/react-dom/components/input)

---

# <input>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <input>

The [built-in browser<input>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) lets you render different kinds of form inputs.

$

```
<input />
```

/$

- [Reference](#reference)
  - [<input>](#input)
- [Usage](#usage)
  - [Displaying inputs of different types](#displaying-inputs-of-different-types)
  - [Providing a label for an input](#providing-a-label-for-an-input)
  - [Providing an initial value for an input](#providing-an-initial-value-for-an-input)
  - [Reading the input values when submitting a form](#reading-the-input-values-when-submitting-a-form)
  - [Controlling an input with a state variable](#controlling-an-input-with-a-state-variable)
  - [Optimizing re-rendering on every keystroke](#optimizing-re-rendering-on-every-keystroke)
- [Troubleshooting](#troubleshooting)
  - [My text input doesn’t update when I type into it](#my-text-input-doesnt-update-when-i-type-into-it)
  - [My checkbox doesn’t update when I click on it](#my-checkbox-doesnt-update-when-i-click-on-it)
  - [My input caret jumps to the beginning on every keystroke](#my-input-caret-jumps-to-the-beginning-on-every-keystroke)
  - [I’m getting an error: “A component is changing an uncontrolled input to be controlled”](#im-getting-an-error-a-component-is-changing-an-uncontrolled-input-to-be-controlled)

---

## Reference

### <input>

To display an input, render the [built-in browser<input>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) component.

 $

```
<input name="myInput" />
```

/$

[See more examples below.](#usage)

#### Props

`<input>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

- [formAction](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formaction): A string or function. Overrides the parent `<form action>` for `type="submit"` and `type="image"`. When a URL is passed to `action` the form will behave like a standard HTML form. When a function is passed to `formAction` the function will handle the form submission. See [<form action>](https://react.dev/reference/react-dom/components/form#props).

You can [make an input controlled](#controlling-an-input-with-a-state-variable) by passing one of these props:

- [checked](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement#checked): A boolean. For a checkbox input or a radio button, controls whether it is selected.
- [value](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement#value): A string. For a text input, controls its text. (For a radio button, specifies its form data.)

When you pass either of them, you must also pass an `onChange` handler that updates the passed value.

These `<input>` props are only relevant for uncontrolled inputs:

- [defaultChecked](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement#defaultChecked): A boolean. Specifies [the initial value](#providing-an-initial-value-for-an-input) for `type="checkbox"` and `type="radio"` inputs.
- [defaultValue](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement#defaultValue): A string. Specifies [the initial value](#providing-an-initial-value-for-an-input) for a text input.

These `<input>` props are relevant both for uncontrolled and controlled inputs:

- [accept](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#accept): A string. Specifies which filetypes are accepted by a `type="file"` input.
- [alt](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#alt): A string. Specifies the alternative image text for a `type="image"` input.
- [capture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#capture): A string. Specifies the media (microphone, video, or camera) captured by a `type="file"` input.
- [autoComplete](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#autocomplete): A string. Specifies one of the possible [autocomplete behaviors.](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete#values)
- [autoFocus](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#autofocus): A boolean. If `true`, React will focus the element on mount.
- [dirname](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#dirname): A string. Specifies the form field name for the element’s directionality.
- [disabled](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#disabled): A boolean. If `true`, the input will not be interactive and will appear dimmed.
- `children`: `<input>` does not accept children.
- [form](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#form): A string. Specifies the `id` of the `<form>` this input belongs to. If omitted, it’s the closest parent form.
- [formAction](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formaction): A string. Overrides the parent `<form action>` for `type="submit"` and `type="image"`.
- [formEnctype](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formenctype): A string. Overrides the parent `<form enctype>` for `type="submit"` and `type="image"`.
- [formMethod](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formmethod): A string. Overrides the parent `<form method>` for `type="submit"` and `type="image"`.
- [formNoValidate](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formnovalidate): A string. Overrides the parent `<form noValidate>` for `type="submit"` and `type="image"`.
- [formTarget](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#formtarget): A string. Overrides the parent `<form target>` for `type="submit"` and `type="image"`.
- [height](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#height): A string. Specifies the image height for `type="image"`.
- [list](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#list): A string. Specifies the `id` of the `<datalist>` with the autocomplete options.
- [max](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#max): A number. Specifies the maximum value of numerical and datetime inputs.
- [maxLength](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#maxlength): A number. Specifies the maximum length of text and other inputs.
- [min](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#min): A number. Specifies the minimum value of numerical and datetime inputs.
- [minLength](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#minlength): A number. Specifies the minimum length of text and other inputs.
- [multiple](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#multiple): A boolean. Specifies whether multiple values are allowed for `<type="file"` and `type="email"`.
- [name](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#name): A string. Specifies the name for this input that’s [submitted with the form.](#reading-the-input-values-when-submitting-a-form)
- `onChange`: An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Required for [controlled inputs.](#controlling-an-input-with-a-state-variable) Fires immediately when the input’s value is changed by the user (for example, it fires on every keystroke). Behaves like the browser [inputevent.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event)
- `onChangeCapture`: A version of `onChange` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInput](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires immediately when the value is changed by the user. For historical reasons, in React it is idiomatic to use `onChange` instead which works similarly.
- `onInputCapture`: A version of `onInput` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onInvalid](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/invalid_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires if an input fails validation on form submit. Unlike the built-in `invalid` event, the React `onInvalid` event bubbles.
- `onInvalidCapture`: A version of `onInvalid` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [onSelect](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/select_event): An [Eventhandler](https://react.dev/reference/react-dom/components/common#event-handler) function. Fires after the selection inside the `<input>` changes. React extends the `onSelect` event to also fire for empty selection and on edits (which may affect the selection).
- `onSelectCapture`: A version of `onSelect` that fires in the [capture phase.](https://react.dev/learn/responding-to-events#capture-phase-events)
- [pattern](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#pattern): A string. Specifies the pattern that the `value` must match.
- [placeholder](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#placeholder): A string. Displayed in a dimmed color when the input value is empty.
- [readOnly](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#readonly): A boolean. If `true`, the input is not editable by the user.
- [required](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#required): A boolean. If `true`, the value must be provided for the form to submit.
- [size](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#size): A number. Similar to setting width, but the unit depends on the control.
- [src](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#src): A string. Specifies the image source for a `type="image"` input.
- [step](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#step): A positive number or an `'any'` string. Specifies the distance between valid values.
- [type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#type): A string. One of the [input types.](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#input_types)
- [width](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#width):  A string. Specifies the image width for a `type="image"` input.

#### Caveats

- Checkboxes need `checked` (or `defaultChecked`), not `value` (or `defaultValue`).
- If a text input receives a string `value` prop, it will be [treated as controlled.](#controlling-an-input-with-a-state-variable)
- If a checkbox or a radio button receives a boolean `checked` prop, it will be [treated as controlled.](#controlling-an-input-with-a-state-variable)
- An input can’t be both controlled and uncontrolled at the same time.
- An input cannot switch between being controlled or uncontrolled over its lifetime.
- Every controlled input needs an `onChange` event handler that synchronously updates its backing value.

---

## Usage

### Displaying inputs of different types

To display an input, render an `<input>` component. By default, it will be a text input. You can pass `type="checkbox"` for a checkbox, `type="radio"` for a radio button, [or one of the other input types.](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#input_types)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function MyForm() {
  return (
    <>
      <label>
        Text input: <input name="myInput" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label>
          <input type="radio" name="myRadio" value="option1" />
          Option 1
        </label>
        <label>
          <input type="radio" name="myRadio" value="option2" />
          Option 2
        </label>
        <label>
          <input type="radio" name="myRadio" value="option3" />
          Option 3
        </label>
      </p>
    </>
  );
}
```

/$

---

### Providing a label for an input

Typically, you will place every `<input>` inside a [<label>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) tag. This tells the browser that this label is associated with that input. When the user clicks the label, the browser will automatically focus the input. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the associated input.

If you can’t nest `<input>` into a `<label>`, associate them by passing the same ID to `<input id>` and [<label htmlFor>.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement/htmlFor) To avoid conflicts between multiple instances of one component, generate such an ID with [useId.](https://react.dev/reference/react/useId)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useId } from 'react';

export default function Form() {
  const ageInputId = useId();
  return (
    <>
      <label>
        Your first name:
        <input name="firstName" />
      </label>
      <hr />
      <label htmlFor={ageInputId}>Your age:</label>
      <input id={ageInputId} name="age" type="number" />
    </>
  );
}
```

/$

---

### Providing an initial value for an input

You can optionally specify the initial value for any input. Pass it as the `defaultValue` string for text inputs. Checkboxes and radio buttons should specify the initial value with the `defaultChecked` boolean instead.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function MyForm() {
  return (
    <>
      <label>
        Text input: <input name="myInput" defaultValue="Some initial value" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" defaultChecked={true} />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label>
          <input type="radio" name="myRadio" value="option1" />
          Option 1
        </label>
        <label>
          <input
            type="radio"
            name="myRadio"
            value="option2"
            defaultChecked={true}
          />
          Option 2
        </label>
        <label>
          <input type="radio" name="myRadio" value="option3" />
          Option 3
        </label>
      </p>
    </>
  );
}
```

/$

---

### Reading the input values when submitting a form

Add a [<form>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) around your inputs with a [<button type="submit">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) inside. It will call your `<form onSubmit>` event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling `e.preventDefault()`. Read the form data with [new FormData(e.target)](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function MyForm() {
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
        Text input: <input name="myInput" defaultValue="Some initial value" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" defaultChecked={true} />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label><input type="radio" name="myRadio" value="option1" /> Option 1</label>
        <label><input type="radio" name="myRadio" value="option2" defaultChecked={true} /> Option 2</label>
        <label><input type="radio" name="myRadio" value="option3" /> Option 3</label>
      </p>
      <hr />
      <button type="reset">Reset form</button>
      <button type="submit">Submit form</button>
    </form>
  );
}
```

/$

### Note

Give a `name` to every `<input>`, for example `<input name="firstName" defaultValue="Taylor" />`. The `name` you specified will be used as a key in the form data, for example `{ firstName: "Taylor" }`.

### Pitfall

By default, a `<button>` inside a `<form>` without a `type` attribute will submit it. This can be surprising! If you have your own custom `Button` React component, consider using [<button type="button">](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) instead of `<button>` (with no type). Then, to be explicit, use `<button type="submit">` for buttons that *are* supposed to submit the form.

---

### Controlling an input with a state variable

An input like `<input />` is *uncontrolled.* Even if you [pass an initial value](#providing-an-initial-value-for-an-input) like `<input defaultValue="Initial text" />`, your JSX only specifies the initial value. It does not control what the value should be right now.

**To render acontrolledinput, pass thevalueprop to it (orcheckedfor checkboxes and radios).** React will force the input to always have the `value` you passed. Usually, you would do this by declaring a [state variable:](https://react.dev/reference/react/useState)

 $

```
function Form() {  const [firstName, setFirstName] = useState(''); // Declare a state variable...  // ...  return (    <input      value={firstName} // ...force the input's value to match the state variable...      onChange={e => setFirstName(e.target.value)} // ... and update the state variable on any edits!    />  );}
```

/$

A controlled input makes sense if you needed state anyway—for example, to re-render your UI on every edit:

 $

```
function Form() {  const [firstName, setFirstName] = useState('');  return (    <>      <label>        First name:        <input value={firstName} onChange={e => setFirstName(e.target.value)} />      </label>      {firstName !== '' && <p>Your name is {firstName}.</p>}      ...
```

/$

It’s also useful if you want to offer multiple ways to adjust the input state (for example, by clicking a button):

 $

```
function Form() {  // ...  const [age, setAge] = useState('');  const ageAsNumber = Number(age);  return (    <>      <label>        Age:        <input          value={age}          onChange={e => setAge(e.target.value)}          type="number"        />        <button onClick={() => setAge(ageAsNumber + 10)}>          Add 10 years        </button>
```

/$

The `value` you pass to controlled components should not be `undefined` or `null`. If you need the initial value to be empty (such as with the `firstName` field below), initialize your state variable to an empty string (`''`).

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function Form() {
  const [firstName, setFirstName] = useState('');
  const [age, setAge] = useState('20');
  const ageAsNumber = Number(age);
  return (
    <>
      <label>
        First name:
        <input
          value={firstName}
          onChange={e => setFirstName(e.target.value)}
        />
      </label>
      <label>
        Age:
        <input
          value={age}
          onChange={e => setAge(e.target.value)}
          type="number"
        />
        <button onClick={() => setAge(ageAsNumber + 10)}>
          Add 10 years
        </button>
      </label>
      {firstName !== '' &&
        <p>Your name is {firstName}.</p>
      }
      {ageAsNumber > 0 &&
        <p>Your age is {ageAsNumber}.</p>
      }
    </>
  );
}
```

/$

### Pitfall

**If you passvaluewithoutonChange, it will be impossible to type into the input.** When you control an input by passing some `value` to it, you *force* it to always have the value you passed. So if you pass a state variable as a `value` but forget to update that state variable synchronously during the `onChange` event handler, React will revert the input after every keystroke back to the `value` that you specified.

---

### Optimizing re-rendering on every keystroke

When you use a controlled input, you set the state on every keystroke. If the component containing your state re-renders a large tree, this can get slow. There’s a few ways you can optimize re-rendering performance.

For example, suppose you start with a form that re-renders all page content on every keystroke:

 $

```
function App() {  const [firstName, setFirstName] = useState('');  return (    <>      <form>        <input value={firstName} onChange={e => setFirstName(e.target.value)} />      </form>      <PageContent />    </>  );}
```

/$

Since `<PageContent />` doesn’t rely on the input state, you can move the input state into its own component:

 $

```
function App() {  return (    <>      <SignupForm />      <PageContent />    </>  );}function SignupForm() {  const [firstName, setFirstName] = useState('');  return (    <form>      <input value={firstName} onChange={e => setFirstName(e.target.value)} />    </form>  );}
```

/$

This significantly improves performance because now only `SignupForm` re-renders on every keystroke.

If there is no way to avoid re-rendering (for example, if `PageContent` depends on the search input’s value), [useDeferredValue](https://react.dev/reference/react/useDeferredValue#deferring-re-rendering-for-a-part-of-the-ui) lets you keep the controlled input responsive even in the middle of a large re-render.

---

## Troubleshooting

### My text input doesn’t update when I type into it

If you render an input with `value` but no `onChange`, you will see an error in the console:

 $

```
// 🔴 Bug: controlled text input with no onChange handler<input value={something} />
```

/$ ConsoleYou provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`.

As the error message suggests, if you only wanted to [specify theinitialvalue,](#providing-an-initial-value-for-an-input) pass `defaultValue` instead:

 $

```
// ✅ Good: uncontrolled input with an initial value<input defaultValue={something} />
```

/$

If you want [to control this input with a state variable,](#controlling-an-input-with-a-state-variable) specify an `onChange` handler:

 $

```
// ✅ Good: controlled input with onChange<input value={something} onChange={e => setSomething(e.target.value)} />
```

/$

If the value is intentionally read-only, add a `readOnly` prop to suppress the error:

 $

```
// ✅ Good: readonly controlled input without on change<input value={something} readOnly={true} />
```

/$

---

### My checkbox doesn’t update when I click on it

If you render a checkbox with `checked` but no `onChange`, you will see an error in the console:

 $

```
// 🔴 Bug: controlled checkbox with no onChange handler<input type="checkbox" checked={something} />
```

/$ ConsoleYou provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.

As the error message suggests, if you only wanted to [specify theinitialvalue,](#providing-an-initial-value-for-an-input) pass `defaultChecked` instead:

 $

```
// ✅ Good: uncontrolled checkbox with an initial value<input type="checkbox" defaultChecked={something} />
```

/$

If you want [to control this checkbox with a state variable,](#controlling-an-input-with-a-state-variable) specify an `onChange` handler:

 $

```
// ✅ Good: controlled checkbox with onChange<input type="checkbox" checked={something} onChange={e => setSomething(e.target.checked)} />
```

/$

### Pitfall

You need to read `e.target.checked` rather than `e.target.value` for checkboxes.

If the checkbox is intentionally read-only, add a `readOnly` prop to suppress the error:

 $

```
// ✅ Good: readonly controlled input without on change<input type="checkbox" checked={something} readOnly={true} />
```

/$

---

### My input caret jumps to the beginning on every keystroke

If you [control an input,](#controlling-an-input-with-a-state-variable) you must update its state variable to the input’s value from the DOM during `onChange`.

You can’t update it to something other than `e.target.value` (or `e.target.checked` for checkboxes):

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

If this doesn’t fix the problem, it’s possible that the input gets removed and re-added from the DOM on every keystroke. This can happen if you’re accidentally [resetting state](https://react.dev/learn/preserving-and-resetting-state) on every re-render, for example if the input or one of its parents always receives a different `key` attribute, or if you nest component function definitions (which is not supported and causes the “inner” component to always be considered a different tree).

---

### I’m getting an error: “A component is changing an uncontrolled input to be controlled”

If you provide a `value` to the component, it must remain a string throughout its lifetime.

You cannot pass `value={undefined}` first and later pass `value="some string"` because React won’t know whether you want the component to be uncontrolled or controlled. A controlled component should always receive a string `value`, not `null` or `undefined`.

If your `value` is coming from an API or a state variable, it might be initialized to `null` or `undefined`. In that case, either set it to an empty string (`''`) initially, or pass `value={someValue ?? ''}` to ensure `value` is a string.

Similarly, if you pass `checked` to a checkbox, ensure it’s always a boolean.

[Previous<form>](https://react.dev/reference/react-dom/components/form)[Next<option>](https://react.dev/reference/react-dom/components/option)

---

# <link>

[API Reference](https://react.dev/reference/react)[Components](https://react.dev/reference/react-dom/components)

# <link>

The [built-in browser<link>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link) lets you use external resources such as stylesheets or annotate the document with link metadata.

$

```
<link rel="icon" href="favicon.ico" />
```

/$

- [Reference](#reference)
  - [<link>](#link)
- [Usage](#usage)
  - [Linking to related resources](#linking-to-related-resources)
  - [Linking to a stylesheet](#linking-to-a-stylesheet)
  - [Controlling stylesheet precedence](#controlling-stylesheet-precedence)
  - [Deduplicated stylesheet rendering](#deduplicated-stylesheet-rendering)
  - [Annotating specific items within the document with links](#annotating-specific-items-within-the-document-with-links)

---

## Reference

### <link>

To link to external resources such as stylesheets, fonts, and icons, or to annotate the document with link metadata, render the [built-in browser<link>component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link). You can render `<link>` from any component and React will [in most cases](#special-rendering-behavior) place the corresponding DOM element in the document head.

 $

```
<link rel="icon" href="favicon.ico" />
```

/$

[See more examples below.](#usage)

#### Props

`<link>` supports all [common element props.](https://react.dev/reference/react-dom/components/common#common-props)

- `rel`: a string, required. Specifies the [relationship to the resource](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel). React [treats links withrel="stylesheet"differently](#special-rendering-behavior) from other links.

These props apply when `rel="stylesheet"`:

- `precedence`: a string. Tells React where to rank the `<link>` DOM node relative to others in the document `<head>`, which determines which stylesheet can override the other. React will infer that precedence values it discovers first are “lower” and precedence values it discovers later are “higher”. Many style systems can work fine using a single precedence value because style rules are atomic. Stylesheets with the same precedence go together whether they are `<link>` or inline `<style>` tags or loaded using [preinit](https://react.dev/reference/react-dom/preinit) functions.
- `media`: a string. Restricts the stylesheet to a certain [media query](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries).
- `title`: a string. Specifies the name of an [alternative stylesheet](https://developer.mozilla.org/en-US/docs/Web/CSS/Alternative_style_sheets).

These props apply when `rel="stylesheet"` but disable React’s [special treatment of stylesheets](#special-rendering-behavior):

- `disabled`: a boolean. Disables the stylesheet.
- `onError`: a function. Called when the stylesheet fails to load.
- `onLoad`: a function. Called when the stylesheet finishes being loaded.

These props apply when `rel="preload"` or `rel="modulepreload"`:

- `as`: a string. The type of resource. Its possible values are `audio`, `document`, `embed`, `fetch`, `font`, `image`, `object`, `script`, `style`, `track`, `video`, `worker`.
- `imageSrcSet`: a string. Applicable only when `as="image"`. Specifies the [source set of the image](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).
- `imageSizes`: a string. Applicable only when `as="image"`. Specifies the [sizes of the image](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

These props apply when `rel="icon"` or `rel="apple-touch-icon"`:

- `sizes`: a string. The [sizes of the icon](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images).

These props apply in all cases:

- `href`: a string. The URL of the linked resource.
- `crossOrigin`: a string. The [CORS policy](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) to use. Its possible values are `anonymous` and `use-credentials`. It is required when `as` is set to `"fetch"`.
- `referrerPolicy`: a string. The [Referrer header](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#referrerpolicy) to send when fetching. Its possible values are `no-referrer-when-downgrade` (the default), `no-referrer`, `origin`, `origin-when-cross-origin`, and `unsafe-url`.
- `fetchPriority`: a string. Suggests a relative priority for fetching the resource. The possible values are `auto` (the default), `high`, and `low`.
- `hrefLang`: a string. The language of the linked resource.
- `integrity`: a string. A cryptographic hash of the resource, to [verify its authenticity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity).
- `type`: a string. The MIME type of the linked resource.

Props that are **not recommended** for use with React:

- `blocking`: a string. If set to `"render"`, instructs the browser not to render the page until the stylesheet is loaded. React provides more fine-grained control using Suspense.

#### Special rendering behavior

React will always place the DOM element corresponding to the `<link>` component within the document’s `<head>`, regardless of where in the React tree it is rendered. The `<head>` is the only valid place for `<link>` to exist within the DOM, yet it’s convenient and keeps things composable if a component representing a specific page can render `<link>` components itself.

There are a few exceptions to this:

- If the `<link>` has a `rel="stylesheet"` prop, then it has to also have a `precedence` prop to get this special behavior. This is because the order of stylesheets within the document is significant, so React needs to know how to order this stylesheet relative to others, which you specify using the `precedence` prop. If the `precedence` prop is omitted, there is no special behavior.
- If the `<link>` has an [itemProp](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemprop) prop, there is no special behavior, because in this case it doesn’t apply to the document but instead represents metadata about a specific part of the page.
- If the `<link>` has an `onLoad` or `onError` prop, because in that case you are managing the loading of the linked resource manually within your React component.

#### Special behavior for stylesheets

In addition, if the `<link>` is to a stylesheet (namely, it has `rel="stylesheet"` in its props), React treats it specially in the following ways:

- The component that renders `<link>` will [suspend](https://react.dev/reference/react/Suspense) while the stylesheet is loading.
- If multiple components render links to the same stylesheet, React will de-duplicate them and only put a single link into the DOM. Two links are considered the same if they have the same `href` prop.

There are two exception to this special behavior:

- If the link doesn’t have a `precedence` prop, there is no special behavior, because the order of stylesheets within the document is significant, so React needs to know how to order this stylesheet relative to others, which you specify using the `precedence` prop.
- If you supply any of the `onLoad`, `onError`, or `disabled` props, there is no special behavior, because these props indicate that you are managing the loading of the stylesheet manually within your component.

This special treatment comes with two caveats:

- React will ignore changes to props after the link has been rendered. (React will issue a warning in development if this happens.)
- React may leave the link in the DOM even after the component that rendered it has been unmounted.

---

## Usage

### Linking to related resources

You can annotate the document with links to related resources such as an icon, canonical URL, or pingback. React will place this metadata within the document `<head>` regardless of where in the React tree it is rendered.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function BlogPage() {
  return (
    <ShowRenderedHTML>
      <link rel="icon" href="favicon.ico" />
      <link rel="pingback" href="http://www.example.com/xmlrpc.php" />
      <h1>My Blog</h1>
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

/$

### Linking to a stylesheet

If a component depends on a certain stylesheet in order to be displayed correctly, you can render a link to that stylesheet within the component. Your component will [suspend](https://react.dev/reference/react/Suspense) while the stylesheet is loading. You must supply the `precedence` prop, which tells React where to place this stylesheet relative to others — stylesheets with higher precedence can override those with lower precedence.

### Note

When you want to use a stylesheet, it can be beneficial to call the [preinit](https://react.dev/reference/react-dom/preinit) function. Calling this function may allow the browser to start fetching the stylesheet earlier than if you just render a `<link>` component, for example by sending an [HTTP Early Hints response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103).

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function SiteMapPage() {
  return (
    <ShowRenderedHTML>
      <link rel="stylesheet" href="sitemap.css" precedence="medium" />
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

/$

### Controlling stylesheet precedence

Stylesheets can conflict with each other, and when they do, the browser goes with the one that comes later in the document. React lets you control the order of stylesheets with the `precedence` prop. In this example, three components render stylesheets, and the ones with the same precedence are grouped together in the `<head>`.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function HomePage() {
  return (
    <ShowRenderedHTML>
      <FirstComponent />
      <SecondComponent />
      <ThirdComponent/>
      ...
    </ShowRenderedHTML>
  );
}

function FirstComponent() {
  return <link rel="stylesheet" href="first.css" precedence="first" />;
}

function SecondComponent() {
  return <link rel="stylesheet" href="second.css" precedence="second" />;
}

function ThirdComponent() {
  return <link rel="stylesheet" href="third.css" precedence="first" />;
}
```

/$

Note the `precedence` values themselves are arbitrary and their naming is up to you. React will infer that precedence values it discovers first are “lower” and precedence values it discovers later are “higher”.

### Deduplicated stylesheet rendering

If you render the same stylesheet from multiple components, React will place only a single `<link>` in the document head.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function HomePage() {
  return (
    <ShowRenderedHTML>
      <Component />
      <Component />
      ...
    </ShowRenderedHTML>
  );
}

function Component() {
  return <link rel="stylesheet" href="styles.css" precedence="medium" />;
}
```

/$

### Annotating specific items within the document with links

You can use the `<link>` component with the `itemProp` prop to annotate specific items within the document with links to related resources. In this case, React will *not* place these annotations within the document `<head>` but will place them like any other React component.

 $

```
<section itemScope>  <h3>Annotating specific items</h3>  <link itemProp="author" href="http://example.com/" />  <p>...</p></section>
```

/$[Previous<textarea>](https://react.dev/reference/react-dom/components/textarea)[Next<meta>](https://react.dev/reference/react-dom/components/meta)
