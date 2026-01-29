# Declare Request Example Data¶ and more

# Declare Request Example Data¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Declare Request Example Data¶

You can declare examples of the data your app can receive.

Here are several ways to do it.

## Extra JSON Schema data in Pydantic models¶

You can declare `examples` for a Pydantic model that will be added to the generated JSON Schema.

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

That extra info will be added as-is to the output **JSON Schema** for that model, and it will be used in the API docs.

You can use the attribute `model_config` that takes a `dict` as described in [Pydantic's docs: Configuration](https://docs.pydantic.dev/latest/api/config/).

You can set `"json_schema_extra"` with a `dict` containing any additional data you would like to show up in the generated JSON Schema, including `examples`.

Tip

You could use the same technique to extend the JSON Schema and add your own custom extra info.

For example you could use it to add metadata for a frontend user interface, etc.

Info

OpenAPI 3.1.0 (used since FastAPI 0.99.0) added support for `examples`, which is part of the **JSON Schema** standard.

Before that, it only supported the keyword `example` with a single example. That is still supported by OpenAPI 3.1.0, but is deprecated and is not part of the JSON Schema standard. So you are encouraged to migrate `example` to `examples`. 🤓

You can read more at the end of this page.

## Fieldadditional arguments¶

When using `Field()` with Pydantic models, you can also declare additional `examples`:

 [Python 3.10+](#__tabbed_3_1)

```
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

## examplesin JSON Schema - OpenAPI¶

When using any of:

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

you can also declare a group of `examples` with additional information that will be added to their **JSON Schemas** inside of **OpenAPI**.

### Bodywithexamples¶

Here we pass `examples` containing one example of the data expected in `Body()`:

 [Python 3.10+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)[Python 3.10+ - non-Annotated](#__tabbed_6_2)[Python 3.9+ - non-Annotated](#__tabbed_6_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        ],
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        ],
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

### Example in the docs UI¶

With any of the methods above it would look like this in the `/docs`:

![image](https://fastapi.tiangolo.com/img/tutorial/body-fields/image01.png)

### Bodywith multipleexamples¶

You can of course also pass multiple `examples`:

 [Python 3.10+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)[Python 3.10+ - non-Annotated](#__tabbed_8_2)[Python 3.9+ - non-Annotated](#__tabbed_8_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
            {
                "name": "Bar",
                "price": "35.4",
            },
            {
                "name": "Baz",
                "price": "thirty five point four",
            },
        ],
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
            {
                "name": "Bar",
                "price": "35.4",
            },
            {
                "name": "Baz",
                "price": "thirty five point four",
            },
        ],
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

When you do this, the examples will be part of the internal **JSON Schema** for that body data.

Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, doesn't support showing multiple examples for the data in **JSON Schema**. But read below for a workaround.

### OpenAPI-specificexamples¶

Since before **JSON Schema** supported `examples` OpenAPI had support for a different field also called `examples`.

This **OpenAPI-specific** `examples` goes in another section in the OpenAPI specification. It goes in the **details for eachpath operation**, not inside each JSON Schema.

And Swagger UI has supported this particular `examples` field for a while. So, you can use it to **show** different **examples in the docs UI**.

The shape of this OpenAPI-specific field `examples` is a `dict` with **multiple examples** (instead of a `list`), each with extra information that will be added to **OpenAPI** too.

This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the *path operation* directly.

### Using theopenapi_examplesParameter¶

You can declare the OpenAPI-specific `examples` in FastAPI with the parameter `openapi_examples` for:

- `Path()`
- `Query()`
- `Header()`
- `Cookie()`
- `Body()`
- `Form()`
- `File()`

The keys of the `dict` identify each example, and each value is another `dict`.

Each specific example `dict` in the `examples` can contain:

- `summary`: Short description for the example.
- `description`: A long description that can contain Markdown text.
- `value`: This is the actual example shown, e.g. a `dict`.
- `externalValue`: alternative to `value`, a URL pointing to the example. Although this might not be supported by as many tools as `value`.

You can use it like this:

 [Python 3.10+](#__tabbed_9_1)

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)[Python 3.10+ - non-Annotated](#__tabbed_10_2)[Python 3.9+ - non-Annotated](#__tabbed_10_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        openapi_examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        openapi_examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```

### OpenAPI Examples in the Docs UI¶

With `openapi_examples` added to `Body()` the `/docs` would look like:

![image](https://fastapi.tiangolo.com/img/tutorial/body-fields/image02.png)

## Technical Details¶

Tip

If you are already using **FastAPI** version **0.99.0 or above**, you can probably **skip** these details.

They are more relevant for older versions, before OpenAPI 3.1.0 was available.

You can consider this a brief OpenAPI and JSON Schema **history lesson**. 🤓

Warning

These are very technical details about the standards **JSON Schema** and **OpenAPI**.

If the ideas above already work for you, that might be enough, and you probably don't need these details, feel free to skip them.

Before OpenAPI 3.1.0, OpenAPI used an older and modified version of **JSON Schema**.

JSON Schema didn't have `examples`, so OpenAPI added its own `example` field to its own modified version.

OpenAPI also added `example` and `examples` fields to other parts of the specification:

- [Parameter Object(in the specification)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#parameter-object) that was used by FastAPI's:
  - `Path()`
  - `Query()`
  - `Header()`
  - `Cookie()`
- [Request Body Object, in the fieldcontent, on theMedia Type Object(in the specification)](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#media-type-object) that was used by FastAPI's:
  - `Body()`
  - `File()`
  - `Form()`

Info

This old OpenAPI-specific `examples` parameter is now `openapi_examples` since FastAPI `0.103.0`.

### JSON Schema'sexamplesfield¶

But then JSON Schema added an [examples](https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.5) field to a new version of the specification.

And then the new OpenAPI 3.1.0 was based on the latest version (JSON Schema 2020-12) that included this new field `examples`.

And now this new `examples` field takes precedence over the old single (and custom) `example` field, that is now deprecated.

This new `examples` field in JSON Schema is **just alist** of examples, not a dict with extra metadata as in the other places in OpenAPI (described above).

Info

Even after OpenAPI 3.1.0 was released with this new simpler integration with JSON Schema, for a while, Swagger UI, the tool that provides the automatic docs, didn't support OpenAPI 3.1.0 (it does since version 5.0.0 🎉).

Because of that, versions of FastAPI previous to 0.99.0 still used versions of OpenAPI lower than 3.1.0.

### Pydantic and FastAPIexamples¶

When you add `examples` inside a Pydantic model, using `schema_extra` or `Field(examples=["something"])` that example is added to the **JSON Schema** for that Pydantic model.

And that **JSON Schema** of the Pydantic model is included in the **OpenAPI** of your API, and then it's used in the docs UI.

In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used `example` or `examples` with any of the other utilities (`Query()`, `Body()`, etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the *path operation* declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).

But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.

### Swagger UI and OpenAPI-specificexamples¶

Now, as Swagger UI didn't support multiple JSON Schema examples (as of 2023-08-26), users didn't have a way to show multiple examples in the docs.

To solve that, FastAPI `0.103.0` **added support** for declaring the same old **OpenAPI-specific** `examples` field with the new parameter `openapi_examples`. 🤓

### Summary¶

I used to say I didn't like history that much... and look at me now giving "tech history" lessons. 😅

In short, **upgrade to FastAPI 0.99.0 or above**, and things are much **simpler, consistent, and intuitive**, and you don't have to know all these historic details. 😎

---

# Security

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Security - First Steps¶

Let's imagine that you have your **backend** API in some domain.

And you have a **frontend** in another domain or in a different path of the same domain (or in a mobile application).

And you want to have a way for the frontend to authenticate with the backend, using a **username** and **password**.

We can use **OAuth2** to build that with **FastAPI**.

But let's save you the time of reading the full long specification just to find those little pieces of information you need.

Let's use the tools provided by **FastAPI** to handle security.

## How it looks¶

Let's first just use the code and see how it works, and then we'll come back to understand what's happening.

## Createmain.py¶

Copy the example in a file `main.py`:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Run it¶

Info

The [python-multipart](https://github.com/Kludex/python-multipart) package is automatically installed with **FastAPI** when you run the `pip install "fastapi[standard]"` command.

However, if you use the `pip install fastapi` command, the `python-multipart` package is not included by default.

To install it manually, make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it with:

```
$ pip install python-multipart
```

This is because **OAuth2** uses "form data" for sending the `username` and `password`.

Run the example with:

```
fastapi dev main.py
```

## Check it¶

Go to the interactive docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see something like this:

![image](https://fastapi.tiangolo.com/img/tutorial/security/image01.png)

Authorize button!

You already have a shiny new "Authorize" button.

And your *path operation* has a little lock in the top-right corner that you can click.

And if you click it, you have a little authorization form to type a `username` and `password` (and other optional fields):

![image](https://fastapi.tiangolo.com/img/tutorial/security/image02.png)

Note

It doesn't matter what you type in the form, it won't work yet. But we'll get there.

This is of course not the frontend for the final users, but it's a great automatic tool to document interactively all your API.

It can be used by the frontend team (that can also be yourself).

It can be used by third party applications and systems.

And it can also be used by yourself, to debug, check and test the same application.

## Thepasswordflow¶

Now let's go back a bit and understand what is all that.

The `password` "flow" is one of the ways ("flows") defined in OAuth2, to handle security and authentication.

OAuth2 was designed so that the backend or API could be independent of the server that authenticates the user.

But in this case, the same **FastAPI** application will handle the API and the authentication.

So, let's review it from that simplified point of view:

- The user types the `username` and `password` in the frontend, and hits `Enter`.
- The frontend (running in the user's browser) sends that `username` and `password` to a specific URL in our API (declared with `tokenUrl="token"`).
- The API checks that `username` and `password`, and responds with a "token" (we haven't implemented any of this yet).
  - A "token" is just a string with some content that we can use later to verify this user.
  - Normally, a token is set to expire after some time.
    - So, the user will have to log in again at some point later.
    - And if the token is stolen, the risk is less. It is not like a permanent key that will work forever (in most of the cases).
- The frontend stores that token temporarily somewhere.
- The user clicks in the frontend to go to another section of the frontend web app.
- The frontend needs to fetch some more data from the API.
  - But it needs authentication for that specific endpoint.
  - So, to authenticate with our API, it sends a header `Authorization` with a value of `Bearer` plus the token.
  - If the token contains `foobar`, the content of the `Authorization` header would be: `Bearer foobar`.

## FastAPI'sOAuth2PasswordBearer¶

**FastAPI** provides several tools, at different levels of abstraction, to implement these security features.

In this example we are going to use **OAuth2**, with the **Password** flow, using a **Bearer** token. We do that using the `OAuth2PasswordBearer` class.

Info

A "bearer" token is not the only option.

But it's the best one for our use case.

And it might be the best for most use cases, unless you are an OAuth2 expert and know exactly why there's another option that better suits your needs.

In that case, **FastAPI** also provides you with the tools to build it.

When we create an instance of the `OAuth2PasswordBearer` class we pass in the `tokenUrl` parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the `username` and `password` in order to get a token.

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Tip

Here `tokenUrl="token"` refers to a relative URL `token` that we haven't created yet. As it's a relative URL, it's equivalent to `./token`.

Because we are using a relative URL, if your API was located at `https://example.com/`, then it would refer to `https://example.com/token`. But if your API was located at `https://example.com/api/v1/`, then it would refer to `https://example.com/api/v1/token`.

Using a relative URL is important to make sure your application keeps working even in an advanced use case like [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

This parameter doesn't create that endpoint / *path operation*, but declares that the URL `/token` will be the one that the client should use to get the token. That information is used in OpenAPI, and then in the interactive API documentation systems.

We will soon also create the actual path operation.

Info

If you are a very strict "Pythonista" you might dislike the style of the parameter name `tokenUrl` instead of `token_url`.

That's because it is using the same name as in the OpenAPI spec. So that if you need to investigate more about any of these security schemes you can just copy and paste it to find more information about it.

The `oauth2_scheme` variable is an instance of `OAuth2PasswordBearer`, but it is also a "callable".

It could be called as:

```
oauth2_scheme(some, parameters)
```

So, it can be used with `Depends`.

### Use it¶

Now you can pass that `oauth2_scheme` in a dependency with `Depends`.

 [Python 3.9+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_6_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

This dependency will provide a `str` that is assigned to the parameter `token` of the *path operation function*.

**FastAPI** will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).

Technical Details

**FastAPI** will know that it can use the class `OAuth2PasswordBearer` (declared in a dependency) to define the security scheme in OpenAPI because it inherits from `fastapi.security.oauth2.OAuth2`, which in turn inherits from `fastapi.security.base.SecurityBase`.

All the security utilities that integrate with OpenAPI (and the automatic API docs) inherit from `SecurityBase`, that's how **FastAPI** can know how to integrate them in OpenAPI.

## What it does¶

It will go and look in the request for that `Authorization` header, check if the value is `Bearer` plus some token, and will return the token as a `str`.

If it doesn't see an `Authorization` header, or the value doesn't have a `Bearer` token, it will respond with a 401 status code error (`UNAUTHORIZED`) directly.

You don't even have to check if the token exists to return an error. You can be sure that if your function is executed, it will have a `str` in that token.

You can try it already in the interactive docs:

![image](https://fastapi.tiangolo.com/img/tutorial/security/image03.png)

We are not verifying the validity of the token yet, but that's a start already.

## Recap¶

So, in just 3 or 4 extra lines, you already have some primitive form of security.
