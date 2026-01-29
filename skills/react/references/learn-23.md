# Writing Markup with JSX

# Writing Markup with JSX

[Learn React](https://react.dev/learn)[Describing the UI](https://react.dev/learn/describing-the-ui)

# Writing Markup with JSX

*JSX* is a syntax extension for JavaScript that lets you write HTML-like markup inside a JavaScript file. Although there are other ways to write components, most React developers prefer the conciseness of JSX, and most codebases use it.

### You will learn

- Why React mixes markup with rendering logic
- How JSX is different from HTML
- How to display information with JSX

## JSX: Putting markup into JavaScript

The Web has been built on HTML, CSS, and JavaScript. For many years, web developers kept content in HTML, design in CSS, and logic in JavaScript—often in separate files! Content was marked up inside HTML while the page’s logic lived separately in JavaScript:

 ![HTML markup with purple background and a div with two child tags: p and form. ](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_html.dark.png&w=750&q=75)![HTML markup with purple background and a div with two child tags: p and form. ](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_html.png&w=750&q=75)

HTML

![Three JavaScript handlers with yellow background: onSubmit, onLogin, and onClick.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_js.dark.png&w=750&q=75)![Three JavaScript handlers with yellow background: onSubmit, onLogin, and onClick.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_js.png&w=750&q=75)

JavaScript

But as the Web became more interactive, logic increasingly determined content. JavaScript was in charge of the HTML! This is why **in React, rendering logic and markup live together in the same place—components.**

 ![React component with HTML and JavaScript from previous examples mixed. Function name is Sidebar which calls the function isLoggedIn, highlighted in yellow. Nested inside the function highlighted in purple is the p tag from before, and a Form tag referencing the component shown in the next diagram.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_sidebar.dark.png&w=750&q=75)![React component with HTML and JavaScript from previous examples mixed. Function name is Sidebar which calls the function isLoggedIn, highlighted in yellow. Nested inside the function highlighted in purple is the p tag from before, and a Form tag referencing the component shown in the next diagram.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_sidebar.png&w=750&q=75)

`Sidebar.js` React component

![React component with HTML and JavaScript from previous examples mixed. Function name is Form containing two handlers onClick and onSubmit highlighted in yellow. Following the handlers is HTML highlighted in purple. The HTML contains a form element with a nested input element, each with an onClick prop.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_form.dark.png&w=750&q=75)![React component with HTML and JavaScript from previous examples mixed. Function name is Form containing two handlers onClick and onSubmit highlighted in yellow. Following the handlers is HTML highlighted in purple. The HTML contains a form element with a nested input element, each with an onClick prop.](https://react.dev/_next/image?url=%2Fimages%2Fdocs%2Fdiagrams%2Fwriting_jsx_form.png&w=750&q=75)

`Form.js` React component

Keeping a button’s rendering logic and markup together ensures that they stay in sync with each other on every edit. Conversely, details that are unrelated, such as the button’s markup and a sidebar’s markup, are isolated from each other, making it safer to change either of them on their own.

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information. The best way to understand this is to convert some HTML markup to JSX markup.

### Note

JSX and React are two separate things. They’re often used together, but you *can* [use them independently](https://reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html#whats-a-jsx-transform) of each other. JSX is a syntax extension, while React is a JavaScript library.

## Converting HTML to JSX

Suppose that you have some (perfectly valid) HTML:

 $

```
<h1>Hedy Lamarr's Todos</h1><img   src="https://i.imgur.com/yXOvdOSs.jpg"   alt="Hedy Lamarr"   class="photo"><ul>    <li>Invent new traffic lights    <li>Rehearse a movie scene    <li>Improve the spectrum technology</ul>
```

/$

And you want to put it into your component:

 $

```
export default function TodoList() {  return (    // ???  )}
```

/$

If you copy and paste it as is, it will not work:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  return (
    // This doesn't quite work!
    <h1>Hedy Lamarr's Todos</h1>
    <img
      src="https://i.imgur.com/yXOvdOSs.jpg"
      alt="Hedy Lamarr"
      class="photo"
    >
    <ul>
      <li>Invent new traffic lights
      <li>Rehearse a movie scene
      <li>Improve the spectrum technology
    </ul>
```

/$

This is because JSX is stricter and has a few more rules than HTML! If you read the error messages above, they’ll guide you to fix the markup, or you can follow the guide below.

### Note

Most of the time, React’s on-screen error messages will help you find where the problem is. Give them a read if you get stuck!

## The Rules of JSX

### 1. Return a single root element

To return multiple elements from a component, **wrap them with a single parent tag.**

For example, you can use a `<div>`:

 $

```
<div>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></div>
```

/$

If you don’t want to add an extra `<div>` to your markup, you can write `<>` and `</>` instead:

 $

```
<>  <h1>Hedy Lamarr's Todos</h1>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"  >  <ul>    ...  </ul></>
```

/$

This empty tag is called a *Fragment.* Fragments let you group things without leaving any trace in the browser HTML tree.

##### Deep Dive

#### Why do multiple JSX tags need to be wrapped?

JSX looks like HTML, but under the hood it is transformed into plain JavaScript objects. You can’t return two objects from a function without wrapping them into an array. This explains why you also can’t return two JSX tags without wrapping them into another tag or a Fragment.

### 2. Close all the tags

JSX requires tags to be explicitly closed: self-closing tags like `<img>` must become `<img />`, and wrapping tags like `<li>oranges` must be written as `<li>oranges</li>`.

This is how Hedy Lamarr’s image and list items look closed:

 $

```
<>  <img     src="https://i.imgur.com/yXOvdOSs.jpg"     alt="Hedy Lamarr"     class="photo"   />  <ul>    <li>Invent new traffic lights</li>    <li>Rehearse a movie scene</li>    <li>Improve the spectrum technology</li>  </ul></>
```

/$

### 3. camelCaseallmost of the things!

JSX turns into JavaScript and attributes written in JSX become keys of JavaScript objects. In your own components, you will often want to read those attributes into variables. But JavaScript has limitations on variable names. For example, their names can’t contain dashes or be reserved words like `class`.

This is why, in React, many HTML and SVG attributes are written in camelCase. For example, instead of `stroke-width` you use `strokeWidth`. Since `class` is a reserved word, in React you write `className` instead, named after the [corresponding DOM property](https://developer.mozilla.org/en-US/docs/Web/API/Element/className):

 $

```
<img   src="https://i.imgur.com/yXOvdOSs.jpg"   alt="Hedy Lamarr"   className="photo"/>
```

/$

You can [find all these attributes in the list of DOM component props.](https://react.dev/reference/react-dom/components/common) If you get one wrong, don’t worry—React will print a message with a possible correction to the [browser console.](https://developer.mozilla.org/docs/Tools/Browser_Console)

### Pitfall

For historical reasons, [aria-*](https://developer.mozilla.org/docs/Web/Accessibility/ARIA) and [data-*](https://developer.mozilla.org/docs/Learn/HTML/Howto/Use_data_attributes) attributes are written as in HTML with dashes.

### Pro-tip: Use a JSX Converter

Converting all these attributes in existing markup can be tedious! We recommend using a [converter](https://transform.tools/html-to-jsx) to translate your existing HTML and SVG to JSX. Converters are very useful in practice, but it’s still worth understanding what is going on so that you can comfortably write JSX on your own.

Here is your final result:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function TodoList() {
  return (
    <>
      <h1>Hedy Lamarr's Todos</h1>
      <img
        src="https://i.imgur.com/yXOvdOSs.jpg"
        alt="Hedy Lamarr"
        className="photo"
      />
      <ul>
        <li>Invent new traffic lights</li>
        <li>Rehearse a movie scene</li>
        <li>Improve the spectrum technology</li>
      </ul>
    </>
  );
}
```

/$

## Recap

Now you know why JSX exists and how to use it in components:

- React components group rendering logic together with markup because they are related.
- JSX is similar to HTML, with a few differences. You can use a [converter](https://transform.tools/html-to-jsx) if you need to.
- Error messages will often point you in the right direction to fixing your markup.

## Try out some challenges

#### Challenge1of1:Convert some HTML to JSX

This HTML was pasted into a component, but it’s not valid JSX. Fix it:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
export default function Bio() {
  return (
    <div class="intro">
      <h1>Welcome to my website!</h1>
    </div>
    <p class="summary">
      You can find my thoughts here.
      <br><br>
      <b>And <i>pictures</b></i> of scientists!
    </p>
  );
}
```

/$

Whether to do it by hand or using the converter is up to you!

[PreviousImporting and Exporting Components](https://react.dev/learn/importing-and-exporting-components)[NextJavaScript in JSX with Curly Braces](https://react.dev/learn/javascript-in-jsx-with-curly-braces)
