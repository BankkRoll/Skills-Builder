# Additional Responses in OpenAPI¶ and more

# Additional Responses in OpenAPI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Additional Responses in OpenAPI¶

Warning

This is a rather advanced topic.

If you are starting with **FastAPI**, you might not need this.

You can declare additional responses, with additional status codes, media types, descriptions, etc.

Those additional responses will be included in the OpenAPI schema, so they will also appear in the API docs.

But for those additional responses you have to make sure you return a `Response` like `JSONResponse` directly, with your status code and content.

## Additional Response withmodel¶

You can pass to your *path operation decorators* a parameter `responses`.

It receives a `dict`: the keys are status codes for each response (like `200`), and the values are other `dict`s with the information for each of them.

Each of those response `dict`s can have a key `model`, containing a Pydantic model, just like `response_model`.

**FastAPI** will take that model, generate its JSON Schema and include it in the correct place in OpenAPI.

For example, to declare another response with a status code `404` and a Pydantic model `Message`, you can write:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})
```

Note

Keep in mind that you have to return the `JSONResponse` directly.

Info

The `model` key is not part of OpenAPI.

**FastAPI** will take the Pydantic model from there, generate the JSON Schema, and put it in the correct place.

The correct place is:

- In the key `content`, that has as value another JSON object (`dict`) that contains:
  - A key with the media type, e.g. `application/json`, that contains as value another JSON object, that contains:
    - A key `schema`, that has as the value the JSON Schema from the model, here's the correct place.
      - **FastAPI** adds a reference here to the global JSON Schemas in another place in your OpenAPI instead of including it directly. This way, other applications and clients can use those JSON Schemas directly, provide better code generation tools, etc.

The generated responses in the OpenAPI for this *path operation* will be:

```
{
    "responses": {
        "404": {
            "description": "Additional Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Message"
                    }
                }
            }
        },
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Item"
                    }
                }
            }
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }
}
```

The schemas are referenced to another place inside the OpenAPI schema:

```
{
    "components": {
        "schemas": {
            "Message": {
                "title": "Message",
                "required": [
                    "message"
                ],
                "type": "object",
                "properties": {
                    "message": {
                        "title": "Message",
                        "type": "string"
                    }
                }
            },
            "Item": {
                "title": "Item",
                "required": [
                    "id",
                    "value"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "string"
                    },
                    "value": {
                        "title": "Value",
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            }
        }
    }
}
```

## Additional media types for the main response¶

You can use this same `responses` parameter to add different media types for the same main response.

For example, you can add an additional media type of `image/png`, declaring that your *path operation* can return a JSON object (with media type `application/json`) or a PNG image:

 [Python 3.10+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_3_1)

```
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: Union[bool, None] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

Note

Notice that you have to return the image using a `FileResponse` directly.

Info

Unless you specify a different media type explicitly in your `responses` parameter, FastAPI will assume the response has the same media type as the main response class (default `application/json`).

But if you have specified a custom response class with `None` as its media type, FastAPI will use `application/json` for any additional response that has an associated model.

## Combining information¶

You can also combine response information from multiple places, including the `response_model`, `status_code`, and `responses` parameters.

You can declare a `response_model`, using the default status code `200` (or a custom one if you need), and then declare additional information for that same response in `responses`, directly in the OpenAPI schema.

**FastAPI** will keep the additional information from `responses`, and combine it with the JSON Schema from your model.

For example, you can declare a response with a status code `404` that uses a Pydantic model and has a custom `description`.

And a response with a status code `200` that uses your `response_model`, but includes a custom `example`:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})
```

It will all be combined and included in your OpenAPI, and shown in the API docs:

![image](https://fastapi.tiangolo.com/img/tutorial/additional-responses/image01.png)

## Combine predefined responses and custom ones¶

You might want to have some predefined responses that apply to many *path operations*, but you want to combine them with custom responses needed by each *path operation*.

For those cases, you can use the Python technique of "unpacking" a `dict` with `**dict_to_unpack`:

```
old_dict = {
    "old key": "old value",
    "second old key": "second old value",
}
new_dict = {**old_dict, "new key": "new value"}
```

Here, `new_dict` will contain all the key-value pairs from `old_dict` plus the new key-value pair:

```
{
    "old key": "old value",
    "second old key": "second old value",
    "new key": "new value",
}
```

You can use that technique to reuse some predefined responses in your *path operations* and combine them with additional custom ones.

For example:

 [Python 3.10+](#__tabbed_5_1)

```
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}},
)
async def read_item(item_id: str, img: Union[bool, None] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return {"id": "foo", "value": "there goes my hero"}
```

## More information about OpenAPI responses¶

To see what exactly you can include in the responses, you can check these sections in the OpenAPI specification:

- [OpenAPI Responses Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#responses-object), it includes the `Response Object`.
- [OpenAPI Response Object](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#response-object), you can include anything from this directly in each response inside your `responses` parameter. Including `description`, `headers`, `content` (inside of this is that you declare different media types and JSON Schemas), and `links`.

---

# Additional Status Codes¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Additional Status Codes¶

By default, **FastAPI** will return the responses using a `JSONResponse`, putting the content you return from your *path operation* inside of that `JSONResponse`.

It will use the default status code or the one you set in your *path operation*.

## Additional status codes¶

If you want to return additional status codes apart from the main one, you can do that by returning a `Response` directly, like a `JSONResponse`, and set the additional status code directly.

For example, let's say that you want to have a *path operation* that allows to update items, and returns HTTP status codes of 200 "OK" when successful.

But you also want it to accept new items. And when the items didn't exist before, it creates them, and returns an HTTP status code of 201 "Created".

To achieve that, import `JSONResponse`, and return your content there directly, setting the `status_code` that you want:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Annotated[str | None, Body()] = None,
    size: Annotated[int | None, Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Annotated[Union[str, None], Body()] = None,
    size: Annotated[Union[int, None], Body()] = None,
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: str | None = Body(default=None),
    size: int | None = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}

@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: Union[str, None] = Body(default=None),
    size: Union[int, None] = Body(default=None),
):
    if item_id in items:
        item = items[item_id]
        item["name"] = name
        item["size"] = size
        return item
    else:
        item = {"name": name, "size": size}
        items[item_id] = item
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

Warning

When you return a `Response` directly, like in the example above, it will be returned directly.

It won't be serialized with a model, etc.

Make sure it has the data you want it to have, and that the values are valid JSON (if you are using `JSONResponse`).

Technical Details

You could also use `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `status`.

## OpenAPI and API docs¶

If you return additional status codes and responses directly, they won't be included in the OpenAPI schema (the API docs), because FastAPI doesn't have a way to know beforehand what you are going to return.

But you can document that in your code, using: [Additional Responses](https://fastapi.tiangolo.com/advanced/additional-responses/).

---

# Advanced Dependencies¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Advanced Dependencies¶

## Parameterized dependencies¶

All the dependencies we have seen are a fixed function or class.

But there could be cases where you want to be able to set parameters on the dependency, without having to declare many different functions or classes.

Let's imagine that we want to have a dependency that checks if the query parameter `q` contains some fixed content.

But we want to be able to parameterize that fixed content.

## A "callable" instance¶

In Python there's a way to make an instance of a class a "callable".

Not the class itself (which is already a callable), but an instance of that class.

To do that, we declare a method `__call__`:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

In this case, this `__call__` is what **FastAPI** will use to check for additional parameters and sub-dependencies, and this is what will be called to pass a value to the parameter in your *path operation function* later.

## Parameterize the instance¶

And now, we can use `__init__` to declare the parameters of the instance that we can use to "parameterize" the dependency:

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

In this case, **FastAPI** won't ever touch or care about `__init__`, we will use it directly in our code.

## Create an instance¶

We could create an instance of this class with:

 [Python 3.9+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_6_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

And that way we are able to "parameterize" our dependency, that now has `"bar"` inside of it, as the attribute `checker.fixed_content`.

## Use the instance as a dependency¶

Then, we could use this `checker` in a `Depends(checker)`, instead of `Depends(FixedContentQueryChecker)`, because the dependency is the instance, `checker`, not the class itself.

And when solving the dependency, **FastAPI** will call this `checker` like:

```
checker(q="somequery")
```

...and pass whatever that returns as the value of the dependency in our *path operation function* as the parameter `fixed_content_included`:

 [Python 3.9+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_8_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI

app = FastAPI()

class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

checker = FixedContentQueryChecker("bar")

@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

Tip

All this might seem contrived. And it might not be very clear how is it useful yet.

These examples are intentionally simple, but show how it all works.

In the chapters about security, there are utility functions that are implemented in this same way.

If you understood all this, you already know how those utility tools for security work underneath.

## Dependencies withyield,HTTPException,exceptand Background Tasks¶

Warning

You most probably don't need these technical details.

These details are useful mainly if you had a FastAPI application older than 0.121.0 and you are facing issues with dependencies with `yield`.

Dependencies with `yield` have evolved over time to account for the different use cases and to fix some issues, here's a summary of what has changed.

### Dependencies withyieldandscope¶

In version 0.121.0, FastAPI added support for `Depends(scope="function")` for dependencies with `yield`.

Using `Depends(scope="function")`, the exit code after `yield` is executed right after the *path operation function* is finished, before the response is sent back to the client.

And when using `Depends(scope="request")` (the default), the exit code after `yield` is executed after the response is sent.

You can read more about it in the docs for [Dependencies withyield- Early exit andscope](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope).

### Dependencies withyieldandStreamingResponse, Technical Details¶

Before FastAPI 0.118.0, if you used a dependency with `yield`, it would run the exit code after the *path operation function* returned but right before sending the response.

The intention was to avoid holding resources for longer than necessary, waiting for the response to travel through the network.

This change also meant that if you returned a `StreamingResponse`, the exit code of the dependency with `yield` would have been already run.

For example, if you had a database session in a dependency with `yield`, the `StreamingResponse` would not be able to use that session while streaming data because the session would have already been closed in the exit code after `yield`.

This behavior was reverted in 0.118.0, to make the exit code after `yield` be executed after the response is sent.

Info

As you will see below, this is very similar to the behavior before version 0.106.0, but with several improvements and bug fixes for corner cases.

#### Use Cases with Early Exit Code¶

There are some use cases with specific conditions that could benefit from the old behavior of running the exit code of dependencies with `yield` before sending the response.

For example, imagine you have code that uses a database session in a dependency with `yield` only to verify a user, but the database session is never used again in the *path operation function*, only in the dependency, **and** the response takes a long time to be sent, like a `StreamingResponse` that sends data slowly, but for some reason doesn't use the database.

In this case, the database session would be held until the response is finished being sent, but if you don't use it, then it wouldn't be necessary to hold it.

Here's how it could look like:

 [Python 3.10+](#__tabbed_9_1)

```
import time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost/db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

def get_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")

def generate_stream(query: str):
    for ch in query:
        yield ch
        time.sleep(0.1)

@app.get("/generate", dependencies=[Depends(get_user)])
def generate(query: str):
    return StreamingResponse(content=generate_stream(query))
```

The exit code, the automatic closing of the `Session` in:

 [Python 3.10+](#__tabbed_10_1)

```
# Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session

# Code below omitted 👇
```

     👀 Full file preview [Python 3.10+](#__tabbed_11_1)

```
import time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost/db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

def get_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")

def generate_stream(query: str):
    for ch in query:
        yield ch
        time.sleep(0.1)

@app.get("/generate", dependencies=[Depends(get_user)])
def generate(query: str):
    return StreamingResponse(content=generate_stream(query))
```

...would be run after the the response finishes sending the slow data:

 [Python 3.10+](#__tabbed_12_1)

```
# Code above omitted 👆

def generate_stream(query: str):
    for ch in query:
        yield ch
        time.sleep(0.1)

@app.get("/generate", dependencies=[Depends(get_user)])
def generate(query: str):
    return StreamingResponse(content=generate_stream(query))
```

     👀 Full file preview [Python 3.10+](#__tabbed_13_1)

```
import time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost/db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

def get_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")

def generate_stream(query: str):
    for ch in query:
        yield ch
        time.sleep(0.1)

@app.get("/generate", dependencies=[Depends(get_user)])
def generate(query: str):
    return StreamingResponse(content=generate_stream(query))
```

But as `generate_stream()` doesn't use the database session, it is not really necessary to keep the session open while sending the response.

If you have this specific use case using SQLModel (or SQLAlchemy), you could explicitly close the session after you don't need it anymore:

 [Python 3.10+](#__tabbed_14_1)

```
# Code above omitted 👆

def get_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")
    session.close()

# Code below omitted 👇
```

     👀 Full file preview [Python 3.10+](#__tabbed_15_1)

```
import time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost/db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

def get_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized")
    session.close()

def generate_stream(query: str):
    for ch in query:
        yield ch
        time.sleep(0.1)

@app.get("/generate", dependencies=[Depends(get_user)])
def generate(query: str):
    return StreamingResponse(content=generate_stream(query))
```

That way the session would release the database connection, so other requests could use it.

If you have a different use case that needs to exit early from a dependency with `yield`, please create a [GitHub Discussion Question](https://github.com/fastapi/fastapi/discussions/new?category=questions) with your specific use case and why you would benefit from having early closing for dependencies with `yield`.

If there are compelling use cases for early closing in dependencies with `yield`, I would consider adding a new way to opt in to early closing.

### Dependencies withyieldandexcept, Technical Details¶

Before FastAPI 0.110.0, if you used a dependency with `yield`, and then you captured an exception with `except` in that dependency, and you didn't raise the exception again, the exception would be automatically raised/forwarded to any exception handlers or the internal server error handler.

This was changed in version 0.110.0 to fix unhandled memory consumption from forwarded exceptions without a handler (internal server errors), and to make it consistent with the behavior of regular Python code.

### Background Tasks and Dependencies withyield, Technical Details¶

Before FastAPI 0.106.0, raising exceptions after `yield` was not possible, the exit code in dependencies with `yield` was executed *after* the response was sent, so [Exception Handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers) would have already run.

This was designed this way mainly to allow using the same objects "yielded" by dependencies inside of background tasks, because the exit code would be executed after the background tasks were finished.

This was changed in FastAPI 0.106.0 with the intention to not hold resources while waiting for the response to travel through the network.

Tip

Additionally, a background task is normally an independent set of logic that should be handled separately, with its own resources (e.g. its own database connection).

So, this way you will probably have cleaner code.

If you used to rely on this behavior, now you should create the resources for background tasks inside the background task itself, and use internally only data that doesn't depend on the resources of dependencies with `yield`.

For example, instead of using the same database session, you would create a new database session inside of the background task, and you would obtain the objects from the database using this new session. And then instead of passing the object from the database as a parameter to the background task function, you would pass the ID of that object and then obtain the object again inside the background task function.

---

# Async Tests¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Async Tests¶

You have already seen how to test your **FastAPI** applications using the provided `TestClient`. Up to now, you have only seen how to write synchronous tests, without using `async` functions.

Being able to use asynchronous functions in your tests could be useful, for example, when you're querying your database asynchronously. Imagine you want to test sending requests to your FastAPI application and then verify that your backend successfully wrote the correct data in the database, while using an async database library.

Let's look at how we can make that work.

## pytest.mark.anyio¶

If we want to call asynchronous functions in our tests, our test functions have to be asynchronous. AnyIO provides a neat plugin for this, that allows us to specify that some test functions are to be called asynchronously.

## HTTPX¶

Even if your **FastAPI** application uses normal `def` functions instead of `async def`, it is still an `async` application underneath.

The `TestClient` does some magic inside to call the asynchronous FastAPI application in your normal `def` test functions, using standard pytest. But that magic doesn't work anymore when we're using it inside asynchronous functions. By running our tests asynchronously, we can no longer use the `TestClient` inside our test functions.

The `TestClient` is based on [HTTPX](https://www.python-httpx.org), and luckily, we can use it directly to test the API.

## Example¶

For a simple example, let's consider a file structure similar to the one described in [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) and [Testing](https://fastapi.tiangolo.com/tutorial/testing/):

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

The file `main.py` would have:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Tomato"}
```

The file `test_main.py` would have the tests for `main.py`, it could look like this now:

 [Python 3.9+](#__tabbed_2_1)

```
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
```

## Run it¶

You can run your tests as usual via:

```
pytest
```

## In Detail¶

The marker `@pytest.mark.anyio` tells pytest that this test function should be called asynchronously:

 [Python 3.9+](#__tabbed_3_1)

```
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
```

Tip

Note that the test function is now `async def` instead of just `def` as before when using the `TestClient`.

Then we can create an `AsyncClient` with the app, and send async requests to it, using `await`.

 [Python 3.9+](#__tabbed_4_1)

```
import pytest
from httpx import ASGITransport, AsyncClient

from .main import app

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
```

This is the equivalent to:

```
response = client.get('/')
```

...that we used to make our requests with the `TestClient`.

Tip

Note that we're using async/await with the new `AsyncClient` - the request is asynchronous.

Warning

If your application relies on lifespan events, the `AsyncClient` won't trigger these events. To ensure they are triggered, use `LifespanManager` from [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage).

## Other Asynchronous Function Calls¶

As the testing function is now asynchronous, you can now also call (and `await`) other `async` functions apart from sending requests to your FastAPI application in your tests, exactly as you would call them anywhere else in your code.

Tip

If you encounter a `RuntimeError: Task attached to a different loop` when integrating asynchronous function calls in your tests (e.g. when using [MongoDB's MotorClient](https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop)), remember to instantiate objects that need an event loop only within async functions, e.g. an `@app.on_event("startup")` callback.
