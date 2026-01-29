# Path Parameters and Numeric Validations¶ and more

# Path Parameters and Numeric Validations¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Path Parameters and Numeric Validations¶

In the same way that you can declare more validations and metadata for query parameters with `Query`, you can declare the same type of validations and metadata for path parameters with `Path`.

## ImportPath¶

First, import `Path` from `fastapi`, and import `Annotated`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Info

FastAPI added support for `Annotated` (and started recommending it) in version 0.95.0.

If you have an older version, you would get errors when trying to use `Annotated`.

Make sure you [Upgrade the FastAPI version](https://fastapi.tiangolo.com/deployment/versions/#upgrading-the-fastapi-versions) to at least 0.95.1 before using `Annotated`.

## Declare metadata¶

You can declare all the same parameters as for `Query`.

For example, to declare a `title` metadata value for the path parameter `item_id` you can type:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

Note

A path parameter is always required as it has to be part of the path. Even if you declared it with `None` or set a default value, it would not affect anything, it would still be always required.

## Order the parameters as you need¶

Tip

This is probably not as important or necessary if you use `Annotated`.

Let's say that you want to declare the query parameter `q` as a required `str`.

And you don't need to declare anything else for that parameter, so you don't really need to use `Query`.

But you still need to use `Path` for the `item_id` path parameter. And you don't want to use `Annotated` for some reason.

Python will complain if you put a value with a "default" before a value that doesn't have a "default".

But you can re-order them, and have the value without a default (the query parameter `q`) first.

It doesn't matter for **FastAPI**. It will detect the parameters by their names, types and default declarations (`Query`, `Path`, etc), it doesn't care about the order.

So, you can declare your function as:

 [Python 3.9+ - non-Annotated](#__tabbed_5_1)

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

But keep in mind that if you use `Annotated`, you won't have this problem, it won't matter as you're not using the function parameter default values for `Query()` or `Path()`.

 [Python 3.9+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_8_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## Order the parameters as you need, tricks¶

Tip

This is probably not as important or necessary if you use `Annotated`.

Here's a **small trick** that can be handy, but you won't need it often.

If you want to:

- declare the `q` query parameter without a `Query` nor any default value
- declare the path parameter `item_id` using `Path`
- have them in a different order
- not use `Annotated`

...Python has a little special syntax for that.

Pass `*`, as the first parameter of the function.

Python won't do anything with that `*`, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as `kwargs`. Even if they don't have a default value.

 [Python 3.9+ - non-Annotated](#__tabbed_9_1)

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

### Better withAnnotated¶

Keep in mind that if you use `Annotated`, as you are not using function parameter default values, you won't have this problem, and you probably won't need to use `*`.

 [Python 3.9+](#__tabbed_11_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_12_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## Number validations: greater than or equal¶

With `Query` and `Path` (and others you'll see later) you can declare number constraints.

Here, with `ge=1`, `item_id` will need to be an integer number "`g`reater than or `e`qual" to `1`.

 [Python 3.9+](#__tabbed_13_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_14_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## Number validations: greater than and less than or equal¶

The same applies for:

- `gt`: `g`reater `t`han
- `le`: `l`ess than or `e`qual

 [Python 3.9+](#__tabbed_15_1)

```
from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_16_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

## Number validations: floats, greater than and less than¶

Number validations also work for `float` values.

Here's where it becomes important to be able to declare `gt` and not just `ge`. As with it you can require, for example, that a value must be greater than `0`, even if it is less than `1`.

So, `0.5` would be a valid value. But `0.0` or `0` would not.

And the same for `lt`.

 [Python 3.9+](#__tabbed_17_1)

```
from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_18_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
```

## Recap¶

With `Query`, `Path` (and others you haven't seen yet) you can declare metadata and string validations in the same ways as with [Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/).

And you can also declare numeric validations:

- `gt`: `g`reater `t`han
- `ge`: `g`reater than or `e`qual
- `lt`: `l`ess `t`han
- `le`: `l`ess than or `e`qual

Info

`Query`, `Path`, and other classes you will see later are subclasses of a common `Param` class.

All of them share the same parameters for additional validation and metadata you have seen.

Technical Details

When you import `Query`, `Path` and others from `fastapi`, they are actually functions.

That when called, return instances of classes of the same name.

So, you import `Query`, which is a function. And when you call it, it returns an instance of a class also named `Query`.

These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.

That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.

---

# Path Parameters¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Path Parameters¶

You can declare path "parameters" or "variables" with the same syntax used by Python format strings:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

The value of the path parameter `item_id` will be passed to your function as the argument `item_id`.

So, if you run this example and go to [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo), you will see a response of:

```
{"item_id":"foo"}
```

## Path parameters with types¶

You can declare the type of a path parameter in the function, using standard Python type annotations:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

In this case, `item_id` is declared to be an `int`.

Check

This will give you editor support inside of your function, with error checks, completion, etc.

## Dataconversion¶

If you run this example and open your browser at [http://127.0.0.1:8000/items/3](http://127.0.0.1:8000/items/3), you will see a response of:

```
{"item_id":3}
```

Check

Notice that the value your function received (and returned) is `3`, as a Python `int`, not a string `"3"`.

So, with that type declaration, **FastAPI** gives you automatic request "parsing".

## Data validation¶

But if you go to the browser at [http://127.0.0.1:8000/items/foo](http://127.0.0.1:8000/items/foo), you will see a nice HTTP error of:

```
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

because the path parameter `item_id` had a value of `"foo"`, which is not an `int`.

The same error would appear if you provided a `float` instead of an `int`, as in: [http://127.0.0.1:8000/items/4.2](http://127.0.0.1:8000/items/4.2)

Check

So, with the same Python type declaration, **FastAPI** gives you data validation.

Notice that the error also clearly states exactly the point where the validation didn't pass.

This is incredibly helpful while developing and debugging code that interacts with your API.

## Documentation¶

And when you open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), you will see an automatic, interactive, API documentation like:

![image](https://fastapi.tiangolo.com/img/tutorial/path-params/image01.png)

Check

Again, just with that same Python type declaration, **FastAPI** gives you automatic, interactive documentation (integrating Swagger UI).

Notice that the path parameter is declared to be an integer.

## Standards-based benefits, alternative documentation¶

And because the generated schema is from the [OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md) standard, there are many compatible tools.

Because of this, **FastAPI** itself provides an alternative API documentation (using ReDoc), which you can access at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc):

![image](https://fastapi.tiangolo.com/img/tutorial/path-params/image02.png)

The same way, there are many compatible tools. Including code generation tools for many languages.

## Pydantic¶

All the data validation is performed under the hood by [Pydantic](https://docs.pydantic.dev/), so you get all the benefits from it. And you know you are in good hands.

You can use the same type declarations with `str`, `float`, `bool` and many other complex data types.

Several of these are explored in the next chapters of the tutorial.

## Order matters¶

When creating *path operations*, you can find situations where you have a fixed path.

Like `/users/me`, let's say that it's to get data about the current user.

And then you can also have a path `/users/{user_id}` to get data about a specific user by some user ID.

Because *path operations* are evaluated in order, you need to make sure that the path for `/users/me` is declared before the one for `/users/{user_id}`:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

Otherwise, the path for `/users/{user_id}` would match also for `/users/me`, "thinking" that it's receiving a parameter `user_id` with a value of `"me"`.

Similarly, you cannot redefine a path operation:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
```

The first one will always be used since the path matches first.

## Predefined values¶

If you have a *path operation* that receives a *path parameter*, but you want the possible valid *path parameter* values to be predefined, you can use a standard Python `Enum`.

### Create anEnumclass¶

Import `Enum` and create a sub-class that inherits from `str` and from `Enum`.

By inheriting from `str` the API docs will be able to know that the values must be of type `string` and will be able to render correctly.

Then create class attributes with fixed values, which will be the available valid values:

 [Python 3.9+](#__tabbed_5_1)

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

Tip

If you are wondering, "AlexNet", "ResNet", and "LeNet" are just names of Machine Learning models.

### Declare apath parameter¶

Then create a *path parameter* with a type annotation using the enum class you created (`ModelName`):

 [Python 3.9+](#__tabbed_6_1)

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

### Check the docs¶

Because the available values for the *path parameter* are predefined, the interactive docs can show them nicely:

![image](https://fastapi.tiangolo.com/img/tutorial/path-params/image03.png)

### Working with Pythonenumerations¶

The value of the *path parameter* will be an *enumeration member*.

#### Compareenumeration members¶

You can compare it with the *enumeration member* in your created enum `ModelName`:

 [Python 3.9+](#__tabbed_7_1)

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

#### Get theenumeration value¶

You can get the actual value (a `str` in this case) using `model_name.value`, or in general, `your_enum_member.value`:

 [Python 3.9+](#__tabbed_8_1)

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

Tip

You could also access the value `"lenet"` with `ModelName.lenet.value`.

#### Returnenumeration members¶

You can return *enum members* from your *path operation*, even nested in a JSON body (e.g. a `dict`).

They will be converted to their corresponding values (strings in this case) before returning them to the client:

 [Python 3.9+](#__tabbed_9_1)

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```

In your client you will get a JSON response like:

```
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Path parameters containing paths¶

Let's say you have a *path operation* with a path `/files/{file_path}`.

But you need `file_path` itself to contain a *path*, like `home/johndoe/myfile.txt`.

So, the URL for that file would be something like: `/files/home/johndoe/myfile.txt`.

### OpenAPI support¶

OpenAPI doesn't support a way to declare a *path parameter* to contain a *path* inside, as that could lead to scenarios that are difficult to test and define.

Nevertheless, you can still do it in **FastAPI**, using one of the internal tools from Starlette.

And the docs would still work, although not adding any documentation telling that the parameter should contain a path.

### Path convertor¶

Using an option directly from Starlette you can declare a *path parameter* containing a *path* using a URL like:

```
/files/{file_path:path}
```

In this case, the name of the parameter is `file_path`, and the last part, `:path`, tells it that the parameter should match any *path*.

So, you can use it with:

 [Python 3.9+](#__tabbed_10_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

Tip

You might need the parameter to contain `/home/johndoe/myfile.txt`, with a leading slash (`/`).

In that case, the URL would be: `/files//home/johndoe/myfile.txt`, with a double slash (`//`) between `files` and `home`.

## Recap¶

With **FastAPI**, by using short, intuitive and standard Python type declarations, you get:

- Editor support: error checks, autocompletion, etc.
- Data "parsing"
- Data validation
- API annotation and automatic documentation

And you only have to declare them once.

That's probably the main visible advantage of **FastAPI** compared to alternative frameworks (apart from the raw performance).

---

# Query Parameter Models¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Query Parameter Models¶

If you have a group of **query parameters** that are related, you can create a **Pydantic model** to declare them.

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

Note

This is supported since FastAPI version `0.115.0`. 🤓

## Query Parameters with a Pydantic Model¶

Declare the **query parameters** that you need in a **Pydantic model**, and then declare the parameter as `Query`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

**FastAPI** will **extract** the data for **each field** from the **query parameters** in the request and give you the Pydantic model you defined.

## Check the Docs¶

You can see the query parameters in the docs UI at `/docs`:

  ![image](https://fastapi.tiangolo.com/img/tutorial/query-param-models/image01.png)

## Forbid Extra Query Parameters¶

In some special use cases (probably not very common), you might want to **restrict** the query parameters that you want to receive.

You can use Pydantic's model configuration to `forbid` any `extra` fields:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: FilterParams = Query()):
    return filter_query
```

If a client tries to send some **extra** data in the **query parameters**, they will receive an **error** response.

For example, if the client tries to send a `tool` query parameter with a value of `plumbus`, like:

```
https://example.com/items/?limit=10&tool=plumbus
```

They will receive an **error** response telling them that the query parameter `tool` is not allowed:

```
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Summary¶

You can use **Pydantic models** to declare **query parameters** in **FastAPI**. 😎

Tip

Spoiler alert: you can also use Pydantic models to declare cookies and headers, but you will read about that later in the tutorial. 🤫
