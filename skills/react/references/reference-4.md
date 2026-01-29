# Children and more

# Children

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# Children

### Pitfall

Using `Children` is uncommon and can lead to fragile code. [See common alternatives.](#alternatives)

`Children` lets you manipulate and transform the JSX you received as the [childrenprop.](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children)

$

```
const mappedChildren = Children.map(children, child =>  <div className="Row">    {child}  </div>);
```

/$

- [Reference](#reference)
  - [Children.count(children)](#children-count)
  - [Children.forEach(children, fn, thisArg?)](#children-foreach)
  - [Children.map(children, fn, thisArg?)](#children-map)
  - [Children.only(children)](#children-only)
  - [Children.toArray(children)](#children-toarray)
- [Usage](#usage)
  - [Transforming children](#transforming-children)
  - [Running some code for each child](#running-some-code-for-each-child)
  - [Counting children](#counting-children)
  - [Converting children to an array](#converting-children-to-an-array)
- [Alternatives](#alternatives)
  - [Exposing multiple components](#exposing-multiple-components)
  - [Accepting an array of objects as a prop](#accepting-an-array-of-objects-as-a-prop)
  - [Calling a render prop to customize rendering](#calling-a-render-prop-to-customize-rendering)
- [Troubleshooting](#troubleshooting)
  - [I pass a custom component, but theChildrenmethods don’t show its render result](#i-pass-a-custom-component-but-the-children-methods-dont-show-its-render-result)

---

## Reference

### Children.count(children)

Call `Children.count(children)` to count the number of children in the `children` data structure.

 $

```
import { Children } from 'react';function RowList({ children }) {  return (    <>      <h1>Total rows: {Children.count(children)}</h1>      ...    </>  );}
```

/$

[See more examples below.](#counting-children)

#### Parameters

- `children`: The value of the [childrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) received by your component.

#### Returns

The number of nodes inside these `children`.

#### Caveats

- Empty nodes (`null`, `undefined`, and Booleans), strings, numbers, and [React elements](https://react.dev/reference/react/createElement) count as individual nodes. Arrays don’t count as individual nodes, but their children do. **The traversal does not go deeper than React elements:** they don’t get rendered, and their children aren’t traversed. [Fragments](https://react.dev/reference/react/Fragment) don’t get traversed.

---

### Children.forEach(children, fn, thisArg?)

Call `Children.forEach(children, fn, thisArg?)` to run some code for each child in the `children` data structure.

 $

```
import { Children } from 'react';function SeparatorList({ children }) {  const result = [];  Children.forEach(children, (child, index) => {    result.push(child);    result.push(<hr key={index} />);  });  // ...
```

/$

[See more examples below.](#running-some-code-for-each-child)

#### Parameters

- `children`: The value of the [childrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) received by your component.
- `fn`: The function you want to run for each child, similar to the [arrayforEachmethod](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) callback. It will be called with the child as the first argument and its index as the second argument. The index starts at `0` and increments on each call.
- **optional** `thisArg`: The [thisvalue](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this) with which the `fn` function should be called. If omitted, it’s `undefined`.

#### Returns

`Children.forEach` returns `undefined`.

#### Caveats

- Empty nodes (`null`, `undefined`, and Booleans), strings, numbers, and [React elements](https://react.dev/reference/react/createElement) count as individual nodes. Arrays don’t count as individual nodes, but their children do. **The traversal does not go deeper than React elements:** they don’t get rendered, and their children aren’t traversed. [Fragments](https://react.dev/reference/react/Fragment) don’t get traversed.

---

### Children.map(children, fn, thisArg?)

Call `Children.map(children, fn, thisArg?)` to map or transform each child in the `children` data structure.

 $

```
import { Children } from 'react';function RowList({ children }) {  return (    <div className="RowList">      {Children.map(children, child =>        <div className="Row">          {child}        </div>      )}    </div>  );}
```

/$

[See more examples below.](#transforming-children)

#### Parameters

- `children`: The value of the [childrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) received by your component.
- `fn`: The mapping function, similar to the [arraymapmethod](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) callback. It will be called with the child as the first argument and its index as the second argument. The index starts at `0` and increments on each call. You need to return a React node from this function. This may be an empty node (`null`, `undefined`, or a Boolean), a string, a number, a React element, or an array of other React nodes.
- **optional** `thisArg`: The [thisvalue](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this) with which the `fn` function should be called. If omitted, it’s `undefined`.

#### Returns

If `children` is `null` or `undefined`, returns the same value.

Otherwise, returns a flat array consisting of the nodes you’ve returned from the `fn` function. The returned array will contain all nodes you returned except for `null` and `undefined`.

#### Caveats

- Empty nodes (`null`, `undefined`, and Booleans), strings, numbers, and [React elements](https://react.dev/reference/react/createElement) count as individual nodes. Arrays don’t count as individual nodes, but their children do. **The traversal does not go deeper than React elements:** they don’t get rendered, and their children aren’t traversed. [Fragments](https://react.dev/reference/react/Fragment) don’t get traversed.
- If you return an element or an array of elements with keys from `fn`, **the returned elements’ keys will be automatically combined with the key of the corresponding original item fromchildren.** When you return multiple elements from `fn` in an array, their keys only need to be unique locally amongst each other.

---

### Children.only(children)

Call `Children.only(children)` to assert that `children` represent a single React element.

 $

```
function Box({ children }) {  const element = Children.only(children);  // ...
```

/$

#### Parameters

- `children`: The value of the [childrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) received by your component.

#### Returns

If `children` [is a valid element,](https://react.dev/reference/react/isValidElement) returns that element.

Otherwise, throws an error.

#### Caveats

- This method always **throws if you pass an array (such as the return value ofChildren.map) aschildren.** In other words, it enforces that `children` is a single React element, not that it’s an array with a single element.

---

### Children.toArray(children)

Call `Children.toArray(children)` to create an array out of the `children` data structure.

 $

```
import { Children } from 'react';export default function ReversedList({ children }) {  const result = Children.toArray(children);  result.reverse();  // ...
```

/$

#### Parameters

- `children`: The value of the [childrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) received by your component.

#### Returns

Returns a flat array of elements in `children`.

#### Caveats

- Empty nodes (`null`, `undefined`, and Booleans) will be omitted in the returned array. **The returned elements’ keys will be calculated from the original elements’ keys and their level of nesting and position.** This ensures that flattening the array does not introduce changes in behavior.

---

## Usage

### Transforming children

To transform the children JSX that your component [receives as thechildrenprop,](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) call `Children.map`:

 $

```
import { Children } from 'react';function RowList({ children }) {  return (    <div className="RowList">      {Children.map(children, child =>        <div className="Row">          {child}        </div>      )}    </div>  );}
```

/$

In the example above, the `RowList` wraps every child it receives into a `<div className="Row">` container. For example, let’s say the parent component passes three `<p>` tags as the `children` prop to `RowList`:

 $

```
<RowList>  <p>This is the first item.</p>  <p>This is the second item.</p>  <p>This is the third item.</p></RowList>
```

/$

Then, with the `RowList` implementation above, the final rendered result will look like this:

 $

```
<div className="RowList">  <div className="Row">    <p>This is the first item.</p>  </div>  <div className="Row">    <p>This is the second item.</p>  </div>  <div className="Row">    <p>This is the third item.</p>  </div></div>
```

/$

`Children.map` is similar to [to transforming arrays withmap().](https://react.dev/learn/rendering-lists) The difference is that the `children` data structure is considered *opaque.* This means that even if it’s sometimes an array, you should not assume it’s an array or any other particular data type. This is why you should use `Children.map` if you need to transform it.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Children } from 'react';

export default function RowList({ children }) {
  return (
    <div className="RowList">
      {Children.map(children, child =>
        <div className="Row">
          {child}
        </div>
      )}
    </div>
  );
}
```

/$

##### Deep Dive

#### Why is the children prop not always an array?

In React, the `children` prop is considered an *opaque* data structure. This means that you shouldn’t rely on how it is structured. To transform, filter, or count children, you should use the `Children` methods.

In practice, the `children` data structure is often represented as an array internally. However, if there is only a single child, then React won’t create an extra array since this would lead to unnecessary memory overhead. As long as you use the `Children` methods instead of directly introspecting the `children` prop, your code will not break even if React changes how the data structure is actually implemented.

Even when `children` is an array, `Children.map` has useful special behavior. For example, `Children.map` combines the [keys](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key) on the returned elements with the keys on the `children` you’ve passed to it. This ensures the original JSX children don’t “lose” keys even if they get wrapped like in the example above.

### Pitfall

The `children` data structure **does not include rendered output** of the components you pass as JSX. In the example below, the `children` received by the `RowList` only contains two items rather than three:

1. `<p>This is the first item.</p>`
2. `<MoreRows />`

This is why only two row wrappers are generated in this example:

$[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import RowList from './RowList.js';

export default function App() {
  return (
    <RowList>
      <p>This is the first item.</p>
      <MoreRows />
    </RowList>
  );
}

function MoreRows() {
  return (
    <>
      <p>This is the second item.</p>
      <p>This is the third item.</p>
    </>
  );
}
```

/$

**There is no way to get the rendered output of an inner component** like `<MoreRows />` when manipulating `children`. This is why [it’s usually better to use one of the alternative solutions.](#alternatives)

---

### Running some code for each child

Call `Children.forEach` to iterate over each child in the `children` data structure. It does not return any value and is similar to the [arrayforEachmethod.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) You can use it to run custom logic like constructing your own array.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Children } from 'react';

export default function SeparatorList({ children }) {
  const result = [];
  Children.forEach(children, (child, index) => {
    result.push(child);
    result.push(<hr key={index} />);
  });
  result.pop(); // Remove the last separator
  return result;
}
```

/$

### Pitfall

As mentioned earlier, there is no way to get the rendered output of an inner component when manipulating `children`. This is why [it’s usually better to use one of the alternative solutions.](#alternatives)

---

### Counting children

Call `Children.count(children)` to calculate the number of children.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Children } from 'react';

export default function RowList({ children }) {
  return (
    <div className="RowList">
      <h1 className="RowListHeader">
        Total rows: {Children.count(children)}
      </h1>
      {Children.map(children, child =>
        <div className="Row">
          {child}
        </div>
      )}
    </div>
  );
}
```

/$

### Pitfall

As mentioned earlier, there is no way to get the rendered output of an inner component when manipulating `children`. This is why [it’s usually better to use one of the alternative solutions.](#alternatives)

---

### Converting children to an array

Call `Children.toArray(children)` to turn the `children` data structure into a regular JavaScript array. This lets you manipulate the array with built-in array methods like [filter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter), [sort](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort), or [reverse.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse)

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Children } from 'react';

export default function ReversedList({ children }) {
  const result = Children.toArray(children);
  result.reverse();
  return result;
}
```

/$

### Pitfall

As mentioned earlier, there is no way to get the rendered output of an inner component when manipulating `children`. This is why [it’s usually better to use one of the alternative solutions.](#alternatives)

---

## Alternatives

### Note

This section describes alternatives to the `Children` API (with capital `C`) that’s imported like this:

$

```
import { Children } from 'react';
```

/$

Don’t confuse it with [using thechildrenprop](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) (lowercase `c`), which is good and encouraged.

### Exposing multiple components

Manipulating children with the `Children` methods often leads to fragile code. When you pass children to a component in JSX, you don’t usually expect the component to manipulate or transform the individual children.

When you can, try to avoid using the `Children` methods. For example, if you want every child of `RowList` to be wrapped in `<div className="Row">`, export a `Row` component, and manually wrap every row into it like this:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { RowList, Row } from './RowList.js';

export default function App() {
  return (
    <RowList>
      <Row>
        <p>This is the first item.</p>
      </Row>
      <Row>
        <p>This is the second item.</p>
      </Row>
      <Row>
        <p>This is the third item.</p>
      </Row>
    </RowList>
  );
}
```

/$

Unlike using `Children.map`, this approach does not wrap every child automatically. **However, this approach has a significant benefit compared to theearlier example withChildren.mapbecause it works even if you keep extracting more components.** For example, it still works if you extract your own `MoreRows` component:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { RowList, Row } from './RowList.js';

export default function App() {
  return (
    <RowList>
      <Row>
        <p>This is the first item.</p>
      </Row>
      <MoreRows />
    </RowList>
  );
}

function MoreRows() {
  return (
    <>
      <Row>
        <p>This is the second item.</p>
      </Row>
      <Row>
        <p>This is the third item.</p>
      </Row>
    </>
  );
}
```

/$

This wouldn’t work with `Children.map` because it would “see” `<MoreRows />` as a single child (and a single row).

---

### Accepting an array of objects as a prop

You can also explicitly pass an array as a prop. For example, this `RowList` accepts a `rows` array as a prop:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { RowList, Row } from './RowList.js';

export default function App() {
  return (
    <RowList rows={[
      { id: 'first', content: <p>This is the first item.</p> },
      { id: 'second', content: <p>This is the second item.</p> },
      { id: 'third', content: <p>This is the third item.</p> }
    ]} />
  );
}
```

/$

Since `rows` is a regular JavaScript array, the `RowList` component can use built-in array methods like [map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) on it.

This pattern is especially useful when you want to be able to pass more information as structured data together with children. In the below example, the `TabSwitcher` component receives an array of objects as the `tabs` prop:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import TabSwitcher from './TabSwitcher.js';

export default function App() {
  return (
    <TabSwitcher tabs={[
      {
        id: 'first',
        header: 'First',
        content: <p>This is the first item.</p>
      },
      {
        id: 'second',
        header: 'Second',
        content: <p>This is the second item.</p>
      },
      {
        id: 'third',
        header: 'Third',
        content: <p>This is the third item.</p>
      }
    ]} />
  );
}
```

/$

Unlike passing the children as JSX, this approach lets you associate some extra data like `header` with each item. Because you are working with the `tabs` directly, and it is an array, you do not need the `Children` methods.

---

### Calling a render prop to customize rendering

Instead of producing JSX for every single item, you can also pass a function that returns JSX, and call that function when necessary. In this example, the `App` component passes a `renderContent` function to the `TabSwitcher` component. The `TabSwitcher` component calls `renderContent` only for the selected tab:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import TabSwitcher from './TabSwitcher.js';

export default function App() {
  return (
    <TabSwitcher
      tabIds={['first', 'second', 'third']}
      getHeader={tabId => {
        return tabId[0].toUpperCase() + tabId.slice(1);
      }}
      renderContent={tabId => {
        return <p>This is the {tabId} item.</p>;
      }}
    />
  );
}
```

/$

A prop like `renderContent` is called a *render prop* because it is a prop that specifies how to render a piece of the user interface. However, there is nothing special about it: it is a regular prop which happens to be a function.

Render props are functions, so you can pass information to them. For example, this `RowList` component passes the `id` and the `index` of each row to the `renderRow` render prop, which uses `index` to highlight even rows:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { RowList, Row } from './RowList.js';

export default function App() {
  return (
    <RowList
      rowIds={['first', 'second', 'third']}
      renderRow={(id, index) => {
        return (
          <Row isHighlighted={index % 2 === 0}>
            <p>This is the {id} item.</p>
          </Row>
        );
      }}
    />
  );
}
```

/$

This is another example of how parent and child components can cooperate without manipulating the children.

---

## Troubleshooting

### I pass a custom component, but theChildrenmethods don’t show its render result

Suppose you pass two children to `RowList` like this:

 $

```
<RowList>  <p>First item</p>  <MoreRows /></RowList>
```

/$

If you do `Children.count(children)` inside `RowList`, you will get `2`. Even if `MoreRows` renders 10 different items, or if it returns `null`, `Children.count(children)` will still be `2`. From the `RowList`’s perspective, it only “sees” the JSX it has received. It does not “see” the internals of the `MoreRows` component.

The limitation makes it hard to extract a component. This is why [alternatives](#alternatives) are preferred to using `Children`.

[PreviousLegacy React APIs](https://react.dev/reference/react/legacy)[NextcloneElement](https://react.dev/reference/react/cloneElement)

---

# cloneElement

[API Reference](https://react.dev/reference/react)[Legacy React APIs](https://react.dev/reference/react/legacy)

# cloneElement

### Pitfall

Using `cloneElement` is uncommon and can lead to fragile code. [See common alternatives.](#alternatives)

`cloneElement` lets you create a new React element using another element as a starting point.

$

```
const clonedElement = cloneElement(element, props, ...children)
```

/$

- [Reference](#reference)
  - [cloneElement(element, props, ...children)](#cloneelement)
- [Usage](#usage)
  - [Overriding props of an element](#overriding-props-of-an-element)
- [Alternatives](#alternatives)
  - [Passing data with a render prop](#passing-data-with-a-render-prop)
  - [Passing data through context](#passing-data-through-context)
  - [Extracting logic into a custom Hook](#extracting-logic-into-a-custom-hook)

---

## Reference

### cloneElement(element, props, ...children)

Call `cloneElement` to create a React element based on the `element`, but with different `props` and `children`:

 $

```
import { cloneElement } from 'react';// ...const clonedElement = cloneElement(  <Row title="Cabbage">    Hello  </Row>,  { isHighlighted: true },  'Goodbye');console.log(clonedElement); // <Row title="Cabbage" isHighlighted={true}>Goodbye</Row>
```

/$

[See more examples below.](#usage)

#### Parameters

- `element`: The `element` argument must be a valid React element. For example, it could be a JSX node like `<Something />`, the result of calling [createElement](https://react.dev/reference/react/createElement), or the result of another `cloneElement` call.
- `props`: The `props` argument must either be an object or `null`. If you pass `null`, the cloned element will retain all of the original `element.props`. Otherwise, for every prop in the `props` object, the returned element will “prefer” the value from `props` over the value from `element.props`. The rest of the props will be filled from the original `element.props`. If you pass `props.key` or `props.ref`, they will replace the original ones.
- **optional** `...children`: Zero or more child nodes. They can be any React nodes, including React elements, strings, numbers, [portals](https://react.dev/reference/react-dom/createPortal), empty nodes (`null`, `undefined`, `true`, and `false`), and arrays of React nodes. If you don’t pass any `...children` arguments, the original `element.props.children` will be preserved.

#### Returns

`cloneElement` returns a React element object with a few properties:

- `type`: Same as `element.type`.
- `props`: The result of shallowly merging `element.props` with the overriding `props` you have passed.
- `ref`: The original `element.ref`, unless it was overridden by `props.ref`.
- `key`: The original `element.key`, unless it was overridden by `props.key`.

Usually, you’ll return the element from your component or make it a child of another element. Although you may read the element’s properties, it’s best to treat every element as opaque after it’s created, and only render it.

#### Caveats

- Cloning an element **does not modify the original element.**
- You should only **pass children as multiple arguments tocloneElementif they are all statically known,** like `cloneElement(element, null, child1, child2, child3)`. If your children are dynamic, pass the entire array as the third argument: `cloneElement(element, null, listItems)`. This ensures that React will [warn you about missingkeys](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key) for any dynamic lists. For static lists this is not necessary because they never reorder.
- `cloneElement` makes it harder to trace the data flow, so **try thealternativesinstead.**

---

## Usage

### Overriding props of an element

To override the props of some React element, pass it to `cloneElement` with the props you want to override:

 $

```
import { cloneElement } from 'react';// ...const clonedElement = cloneElement(  <Row title="Cabbage" />,  { isHighlighted: true });
```

/$

Here, the resulting cloned element will be `<Row title="Cabbage" isHighlighted={true} />`.

**Let’s walk through an example to see when it’s useful.**

Imagine a `List` component that renders its [children](https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children) as a list of selectable rows with a “Next” button that changes which row is selected. The `List` component needs to render the selected `Row` differently, so it clones every `<Row>` child that it has received, and adds an extra `isHighlighted: true` or `isHighlighted: false` prop:

 $

```
export default function List({ children }) {  const [selectedIndex, setSelectedIndex] = useState(0);  return (    <div className="List">      {Children.map(children, (child, index) =>        cloneElement(child, {          isHighlighted: index === selectedIndex         })      )}
```

/$

Let’s say the original JSX received by `List` looks like this:

 $

```
<List>  <Row title="Cabbage" />  <Row title="Garlic" />  <Row title="Apple" /></List>
```

/$

By cloning its children, the `List` can pass extra information to every `Row` inside. The result looks like this:

 $

```
<List>  <Row    title="Cabbage"    isHighlighted={true}   />  <Row    title="Garlic"    isHighlighted={false}   />  <Row    title="Apple"    isHighlighted={false}   /></List>
```

/$

Notice how pressing “Next” updates the state of the `List`, and highlights a different row:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { Children, cloneElement, useState } from 'react';

export default function List({ children }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {Children.map(children, (child, index) =>
        cloneElement(child, {
          isHighlighted: index === selectedIndex
        })
      )}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % Children.count(children)
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

/$

To summarize, the `List` cloned the `<Row />` elements it received and added an extra prop to them.

### Pitfall

Cloning children makes it hard to tell how the data flows through your app. Try one of the [alternatives.](#alternatives)

---

## Alternatives

### Passing data with a render prop

Instead of using `cloneElement`, consider accepting a *render prop* like `renderItem`. Here, `List` receives `renderItem` as a prop. `List` calls `renderItem` for every item and passes `isHighlighted` as an argument:

 $

```
export default function List({ items, renderItem }) {  const [selectedIndex, setSelectedIndex] = useState(0);  return (    <div className="List">      {items.map((item, index) => {        const isHighlighted = index === selectedIndex;        return renderItem(item, isHighlighted);      })}
```

/$

The `renderItem` prop is called a “render prop” because it’s a prop that specifies how to render something. For example, you can pass a `renderItem` implementation that renders a `<Row>` with the given `isHighlighted` value:

 $

```
<List  items={products}  renderItem={(product, isHighlighted) =>    <Row      key={product.id}      title={product.title}      isHighlighted={isHighlighted}    />  }/>
```

/$

The end result is the same as with `cloneElement`:

 $

```
<List>  <Row    title="Cabbage"    isHighlighted={true}   />  <Row    title="Garlic"    isHighlighted={false}   />  <Row    title="Apple"    isHighlighted={false}   /></List>
```

/$

However, you can clearly trace where the `isHighlighted` value is coming from.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';

export default function List({ items, renderItem }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {items.map((item, index) => {
        const isHighlighted = index === selectedIndex;
        return renderItem(item, isHighlighted);
      })}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % items.length
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

/$

This pattern is preferred to `cloneElement` because it is more explicit.

---

### Passing data through context

Another alternative to `cloneElement` is to [pass data through context.](https://react.dev/learn/passing-data-deeply-with-context)

For example, you can call [createContext](https://react.dev/reference/react/createContext) to define a `HighlightContext`:

 $

```
export const HighlightContext = createContext(false);
```

/$

Your `List` component can wrap every item it renders into a `HighlightContext` provider:

 $

```
export default function List({ items, renderItem }) {  const [selectedIndex, setSelectedIndex] = useState(0);  return (    <div className="List">      {items.map((item, index) => {        const isHighlighted = index === selectedIndex;        return (          <HighlightContext key={item.id} value={isHighlighted}>            {renderItem(item)}          </HighlightContext>        );      })}
```

/$

With this approach, `Row` does not need to receive an `isHighlighted` prop at all. Instead, it reads the context:

 $

```
export default function Row({ title }) {  const isHighlighted = useContext(HighlightContext);  // ...
```

/$

This allows the calling component to not know or worry about passing `isHighlighted` to `<Row>`:

 $

```
<List  items={products}  renderItem={product =>    <Row title={product.title} />  }/>
```

/$

Instead, `List` and `Row` coordinate the highlighting logic through context.

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import { useState } from 'react';
import { HighlightContext } from './HighlightContext.js';

export default function List({ items, renderItem }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {items.map((item, index) => {
        const isHighlighted = index === selectedIndex;
        return (
          <HighlightContext
            key={item.id}
            value={isHighlighted}
          >
            {renderItem(item)}
          </HighlightContext>
        );
      })}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % items.length
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

/$

[Learn more about passing data through context.](https://react.dev/reference/react/useContext#passing-data-deeply-into-the-tree)

---

### Extracting logic into a custom Hook

Another approach you can try is to extract the “non-visual” logic into your own Hook, and use the information returned by your Hook to decide what to render. For example, you could write a `useList` custom Hook like this:

 $

```
import { useState } from 'react';export default function useList(items) {  const [selectedIndex, setSelectedIndex] = useState(0);  function onNext() {    setSelectedIndex(i =>      (i + 1) % items.length    );  }  const selected = items[selectedIndex];  return [selected, onNext];}
```

/$

Then you could use it like this:

 $

```
export default function App() {  const [selected, onNext] = useList(products);  return (    <div className="List">      {products.map(product =>        <Row          key={product.id}          title={product.title}          isHighlighted={selected === product}        />      )}      <hr />      <button onClick={onNext}>        Next      </button>    </div>  );}
```

/$

The data flow is explicit, but the state is inside the `useList` custom Hook that you can use from any component:

 $[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined&environment=create-react-app)

```
import Row from './Row.js';
import useList from './useList.js';
import { products } from './data.js';

export default function App() {
  const [selected, onNext] = useList(products);
  return (
    <div className="List">
      {products.map(product =>
        <Row
          key={product.id}
          title={product.title}
          isHighlighted={selected === product}
        />
      )}
      <hr />
      <button onClick={onNext}>
        Next
      </button>
    </div>
  );
}
```

/$

This approach is particularly useful if you want to reuse this logic between different components.

[PreviousChildren](https://react.dev/reference/react/Children)[NextComponent](https://react.dev/reference/react/Component)
