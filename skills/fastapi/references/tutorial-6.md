# JSON Compatible Encoder¶ and more

# JSON Compatible Encoder¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# JSON Compatible Encoder¶

There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a `dict`, `list`, etc).

For example, if you need to store it in a database.

For that, **FastAPI** provides a `jsonable_encoder()` function.

## Using thejsonable_encoder¶

Let's imagine that you have a database `fake_db` that only receives JSON compatible data.

For example, it doesn't receive `datetime` objects, as those are not compatible with JSON.

So, a `datetime` object would have to be converted to a `str` containing the data in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).

The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a `dict`.

You can use `jsonable_encoder` for that.

It receives an object, like a Pydantic model, and returns a JSON compatible version:

 [Python 3.10+](#__tabbed_1_1)

```
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
```

In this example, it would convert the Pydantic model to a `dict`, and the `datetime` to a `str`.

The result of calling it is something that can be encoded with the Python standard [json.dumps()](https://docs.python.org/3/library/json.html#json.dumps).

It doesn't return a large `str` containing the data in JSON format (as a string). It returns a Python standard data structure (e.g. a `dict`) with values and sub-values that are all compatible with JSON.

Note

`jsonable_encoder` is actually used by **FastAPI** internally to convert data. But it is useful in many other scenarios.

---

# Extra Data Types¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Extra Data Types¶

Up to now, you have been using common data types, like:

- `int`
- `float`
- `str`
- `bool`

But you can also use more complex data types.

And you will still have the same features as seen up to now:

- Great editor support.
- Data conversion from incoming requests.
- Data conversion for response data.
- Data validation.
- Automatic annotation and documentation.

## Other data types¶

Here are some of the additional data types you can use:

- `UUID`:
  - A standard "Universally Unique Identifier", common as an ID in many databases and systems.
  - In requests and responses will be represented as a `str`.
- `datetime.datetime`:
  - A Python `datetime.datetime`.
  - In requests and responses will be represented as a `str` in ISO 8601 format, like: `2008-09-15T15:53:00+05:00`.
- `datetime.date`:
  - Python `datetime.date`.
  - In requests and responses will be represented as a `str` in ISO 8601 format, like: `2008-09-15`.
- `datetime.time`:
  - A Python `datetime.time`.
  - In requests and responses will be represented as a `str` in ISO 8601 format, like: `14:23:55.003`.
- `datetime.timedelta`:
  - A Python `datetime.timedelta`.
  - In requests and responses will be represented as a `float` of total seconds.
  - Pydantic also allows representing it as a "ISO 8601 time diff encoding", [see the docs for more info](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers).
- `frozenset`:
  - In requests and responses, treated the same as a `set`:
    - In requests, a list will be read, eliminating duplicates and converting it to a `set`.
    - In responses, the `set` will be converted to a `list`.
    - The generated schema will specify that the `set` values are unique (using JSON Schema's `uniqueItems`).
- `bytes`:
  - Standard Python `bytes`.
  - In requests and responses will be treated as `str`.
  - The generated schema will specify that it's a `str` with `binary` "format".
- `Decimal`:
  - Standard Python `Decimal`.
  - In requests and responses, handled the same as a `float`.
- You can check all the valid Pydantic data types here: [Pydantic data types](https://docs.pydantic.dev/latest/usage/types/types/).

## Example¶

Here's an example *path operation* with parameters using some of the above types.

 [Python 3.10+](#__tabbed_1_1)

```
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: time | None = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Note that the parameters inside the function have their natural data type, and you can, for example, perform normal date manipulations, like:

 [Python 3.10+](#__tabbed_3_1)

```
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: time | None = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

---

# Extra Models¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Extra Models¶

Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

- The **input model** needs to be able to have a password.
- The **output model** should not have a password.
- The **database model** would probably need to have a hashed password.

Danger

Never store user's plaintext passwords. Always store a "secure hash" that you can then verify.

If you don't know, you will learn what a "password hash" is in the [security chapters](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#password-hashing).

## Multiple models¶

Here's a general idea of how the models could look like with their password fields and the places where they are used:

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

### About**user_in.model_dump()¶

#### Pydantic's.model_dump()¶

`user_in` is a Pydantic model of class `UserIn`.

Pydantic models have a `.model_dump()` method that returns a `dict` with the model's data.

So, if we create a Pydantic object `user_in` like:

```
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

and then we call:

```
user_dict = user_in.model_dump()
```

we now have a `dict` with the data in the variable `user_dict` (it's a `dict` instead of a Pydantic model object).

And if we call:

```
print(user_dict)
```

we would get a Python `dict` with:

```
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### Unpacking adict¶

If we take a `dict` like `user_dict` and pass it to a function (or class) with `**user_dict`, Python will "unpack" it. It will pass the keys and values of the `user_dict` directly as key-value arguments.

So, continuing with the `user_dict` from above, writing:

```
UserInDB(**user_dict)
```

would result in something equivalent to:

```
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

Or more exactly, using `user_dict` directly, with whatever contents it might have in the future:

```
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### A Pydantic model from the contents of another¶

As in the example above we got `user_dict` from `user_in.model_dump()`, this code:

```
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

would be equivalent to:

```
UserInDB(**user_in.model_dump())
```

...because `user_in.model_dump()` is a `dict`, and then we make Python "unpack" it by passing it to `UserInDB` prefixed with `**`.

So, we get a Pydantic model from the data in another Pydantic model.

#### Unpacking adictand extra keywords¶

And then adding the extra keyword argument `hashed_password=hashed_password`, like in:

```
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...ends up being like:

```
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

Warning

The supporting additional functions `fake_password_hasher` and `fake_save_user` are just to demo a possible flow of the data, but they of course are not providing any real security.

## Reduce duplication¶

Reducing code duplication is one of the core ideas in **FastAPI**.

As code duplication increments the chances of bugs, security issues, code desynchronization issues (when you update in one place but not in the others), etc.

And these models are all sharing a lot of the data and duplicating attribute names and types.

We could do better.

We can declare a `UserBase` model that serves as a base for our other models. And then we can make subclasses of that model that inherit its attributes (type declarations, validation, etc).

All the data conversion, validation, documentation, etc. will still work as normally.

That way, we can declare just the differences between the models (with plaintext `password`, with `hashed_password` and without password):

 [Python 3.10+](#__tabbed_3_1)

```
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

## UnionoranyOf¶

You can declare a response to be the `Union` of two or more types, that means, that the response would be any of them.

It will be defined in OpenAPI with `anyOf`.

To do that, use the standard Python type hint [typing.Union](https://docs.python.org/3/library/typing.html#typing.Union):

Note

When defining a [Union](https://docs.pydantic.dev/latest/concepts/types/#unions), include the most specific type first, followed by the less specific type. In the example below, the more specific `PlaneItem` comes before `CarItem` in `Union[PlaneItem, CarItem]`.

  [Python 3.10+](#__tabbed_5_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

### Unionin Python 3.10¶

In this example we pass `Union[PlaneItem, CarItem]` as the value of the argument `response_model`.

Because we are passing it as a **value to an argument** instead of putting it in a **type annotation**, we have to use `Union` even in Python 3.10.

If it was in a type annotation we could have used the vertical bar, as:

```
some_variable: PlaneItem | CarItem
```

But if we put that in the assignment `response_model=PlaneItem | CarItem` we would get an error, because Python would try to perform an **invalid operation** between `PlaneItem` and `CarItem` instead of interpreting that as a type annotation.

## List of models¶

The same way, you can declare responses of lists of objects.

For that, use the standard Python `typing.List` (or just `list` in Python 3.9 and above):

 [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
```

## Response with arbitrarydict¶

You can also declare a response using a plain arbitrary `dict`, declaring just the type of the keys and values, without using a Pydantic model.

This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.

In this case, you can use `typing.Dict` (or just `dict` in Python 3.9 and above):

 [Python 3.9+](#__tabbed_8_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
```

## Recap¶

Use multiple Pydantic models and inherit freely for each case.

You don't need to have a single data model per entity if that entity must be able to have different "states". As the case with the user "entity" with a state including `password`, `password_hash` and no password.

---

# First Steps¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# First Steps¶

The simplest FastAPI file could look like this:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Copy that to a file `main.py`.

Run the live server:

```
<font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>
```

In the output, there's a line with something like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

That line shows the URL where your app is being served, in your local machine.

### Check it¶

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

You will see the JSON response as:

```
{"message": "Hello World"}
```

### Interactive API docs¶

Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs¶

And now, go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI¶

**FastAPI** generates a "schema" with all your API using the **OpenAPI** standard for defining APIs.

#### "Schema"¶

A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

#### API "schema"¶

In this case, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) is a specification that dictates how to define a schema of your API.

This schema definition includes your API paths, the possible parameters they take, etc.

#### Data "schema"¶

The term "schema" might also refer to the shape of some data, like a JSON content.

In that case, it would mean the JSON attributes, and data types they have, etc.

#### OpenAPI and JSON Schema¶

OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using **JSON Schema**, the standard for JSON data schemas.

#### Check theopenapi.json¶

If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.

You can see it directly at: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

It will show a JSON starting with something like:

```
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {

...
```

#### What is OpenAPI for¶

The OpenAPI schema is what powers the two interactive documentation systems included.

And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with **FastAPI**.

You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.

### Deploy your app (optional)¶

You can optionally deploy your FastAPI app to [FastAPI Cloud](https://fastapicloud.com), go and join the waiting list if you haven't. 🚀

If you already have a **FastAPI Cloud** account (we invited you from the waiting list 😉), you can deploy your application with one command.

Before deploying, make sure you are logged in:

```
fastapi login
```

Then deploy your app:

```
fastapi deploy
```

That's it! Now you can access your app at that URL. ✨

## Recap, step by step¶

### Step 1: importFastAPI¶

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

`FastAPI` is a Python class that provides all the functionality for your API.

Technical Details

`FastAPI` is a class that inherits directly from `Starlette`.

You can use all the [Starlette](https://www.starlette.dev/) functionality with `FastAPI` too.

### Step 2: create aFastAPI"instance"¶

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Here the `app` variable will be an "instance" of the class `FastAPI`.

This will be the main point of interaction to create all your API.

### Step 3: create apath operation¶

#### Path¶

"Path" here refers to the last part of the URL starting from the first `/`.

So, in a URL like:

```
https://example.com/items/foo
```

...the path would be:

```
/items/foo
```

Info

A "path" is also commonly called an "endpoint" or a "route".

While building an API, the "path" is the main way to separate "concerns" and "resources".

#### Operation¶

"Operation" here refers to one of the HTTP "methods".

One of:

- `POST`
- `GET`
- `PUT`
- `DELETE`

...and the more exotic ones:

- `OPTIONS`
- `HEAD`
- `PATCH`
- `TRACE`

In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".

---

When building APIs, you normally use these specific HTTP methods to perform a specific action.

Normally you use:

- `POST`: to create data.
- `GET`: to read data.
- `PUT`: to update data.
- `DELETE`: to delete data.

So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "**operations**" too.

#### Define apath operation decorator¶

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

The `@app.get("/")` tells **FastAPI** that the function right below is in charge of handling requests that go to:

- the path `/`
- using a `get` operation

`@decorator` Info

That `@something` syntax in Python is called a "decorator".

You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

A "decorator" takes the function below and does something with it.

In our case, this decorator tells **FastAPI** that the function below corresponds to the **path** `/` with an **operation** `get`.

It is the "**path operation decorator**".

You can also use the other operations:

- `@app.post()`
- `@app.put()`
- `@app.delete()`

And the more exotic ones:

- `@app.options()`
- `@app.head()`
- `@app.patch()`
- `@app.trace()`

Tip

You are free to use each operation (HTTP method) as you wish.

**FastAPI** doesn't enforce any specific meaning.

The information here is presented as a guideline, not a requirement.

For example, when using GraphQL you normally perform all the actions using only `POST` operations.

### Step 4: define thepath operation function¶

This is our "**path operation function**":

- **path**: is `/`.
- **operation**: is `get`.
- **function**: is the function below the "decorator" (below `@app.get("/")`).

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

This is a Python function.

It will be called by **FastAPI** whenever it receives a request to the URL "`/`" using a `GET` operation.

In this case, it is an `async` function.

---

You could also define it as a normal function instead of `async def`:

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```

Note

If you don't know the difference, check the [Async:"In a hurry?"](https://fastapi.tiangolo.com/async/#in-a-hurry).

### Step 5: return the content¶

 [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

You can return a `dict`, `list`, singular values as `str`, `int`, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.

### Step 6: Deploy it¶

Deploy your app to **FastAPI Cloud** with one command: `fastapi deploy`. 🎉

#### About FastAPI Cloud¶

**FastAPI Cloud** is built by the same author and team behind **FastAPI**.

It streamlines the process of **building**, **deploying**, and **accessing** an API with minimal effort.

It brings the same **developer experience** of building apps with FastAPI to **deploying** them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the *FastAPI and friends* open source projects. ✨

#### Deploy to other cloud providers¶

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

## Recap¶

- Import `FastAPI`.
- Create an `app` instance.
- Write a **path operation decorator** using decorators like `@app.get("/")`.
- Define a **path operation function**; for example, `def root(): ...`.
- Run the development server using the command `fastapi dev`.
- Optionally deploy your app with `fastapi deploy`.

---

# Handling Errors¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Handling Errors¶

There are many situations in which you need to notify an error to a client that is using your API.

This client could be a browser with a frontend, a code from someone else, an IoT device, etc.

You could need to tell the client that:

- The client doesn't have enough privileges for that operation.
- The client doesn't have access to that resource.
- The item the client was trying to access doesn't exist.
- etc.

In these cases, you would normally return an **HTTP status code** in the range of **400** (from 400 to 499).

This is similar to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in the request.

The status codes in the 400 range mean that there was an error from the client.

Remember all those **"404 Not Found"** errors (and jokes)?

## UseHTTPException¶

To return HTTP responses with errors to the client you use `HTTPException`.

### ImportHTTPException¶

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

### Raise anHTTPExceptionin your code¶

`HTTPException` is a normal Python exception with additional data relevant for APIs.

Because it's a Python exception, you don't `return` it, you `raise` it.

This also means that if you are inside a utility function that you are calling inside of your *path operation function*, and you raise the `HTTPException` from inside of that utility function, it won't run the rest of the code in the *path operation function*, it will terminate that request right away and send the HTTP error from the `HTTPException` to the client.

The benefit of raising an exception over returning a value will be more evident in the section about Dependencies and Security.

In this example, when the client requests an item by an ID that doesn't exist, raise an exception with a status code of `404`:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

### The resulting response¶

If the client requests `http://example.com/items/foo` (an `item_id` `"foo"`), that client will receive an HTTP status code of 200, and a JSON response of:

```
{
  "item": "The Foo Wrestlers"
}
```

But if the client requests `http://example.com/items/bar` (a non-existent `item_id` `"bar"`), that client will receive an HTTP status code of 404 (the "not found" error), and a JSON response of:

```
{
  "detail": "Item not found"
}
```

Tip

When raising an `HTTPException`, you can pass any value that can be converted to JSON as the parameter `detail`, not only `str`.

You could pass a `dict`, a `list`, etc.

They are handled automatically by **FastAPI** and converted to JSON.

## Add custom headers¶

There are some situations in where it's useful to be able to add custom headers to the HTTP error. For example, for some types of security.

You probably won't need to use it directly in your code.

But in case you needed it for an advanced scenario, you can add custom headers:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
```

## Install custom exception handlers¶

You can add custom exception handlers with [the same exception utilities from Starlette](https://www.starlette.dev/exceptions/).

Let's say you have a custom exception `UnicornException` that you (or a library you use) might `raise`.

And you want to handle this exception globally with FastAPI.

You could add a custom exception handler with `@app.exception_handler()`:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

Here, if you request `/unicorns/yolo`, the *path operation* will `raise` a `UnicornException`.

But it will be handled by the `unicorn_exception_handler`.

So, you will receive a clean error, with an HTTP status code of `418` and a JSON content of:

```
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

Technical Details

You could also use `from starlette.requests import Request` and `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `Request`.

## Override the default exception handlers¶

**FastAPI** has some default exception handlers.

These handlers are in charge of returning the default JSON responses when you `raise` an `HTTPException` and when the request has invalid data.

You can override these exception handlers with your own.

### Override request validation exceptions¶

When a request contains invalid data, **FastAPI** internally raises a `RequestValidationError`.

And it also includes a default exception handler for it.

To override it, import the `RequestValidationError` and use it with `@app.exception_handler(RequestValidationError)` to decorate the exception handler.

The exception handler will receive a `Request` and the exception.

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

Now, if you go to `/items/foo`, instead of getting the default JSON error with:

```
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

you will get a text version, with:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### Override theHTTPExceptionerror handler¶

The same way, you can override the `HTTPException` handler.

For example, you could want to return a plain text response instead of JSON for these errors:

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

Technical Details

You could also use `from starlette.responses import PlainTextResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

Warning

Have in mind that the `RequestValidationError` contains the information of the file name and line where the validation error happens so that you can show it in your logs with the relevant information if you want to.

But that means that if you just convert it to a string and return that information directly, you could be leaking a bit of information about your system, that's why here the code extracts and shows each error independently.

### Use theRequestValidationErrorbody¶

The `RequestValidationError` contains the `body` it received with invalid data.

You could use it while developing your app to log the body and debug it, return it to the user, etc.

 [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Item(BaseModel):
    title: str
    size: int

@app.post("/items/")
async def create_item(item: Item):
    return item
```

Now try sending an invalid item like:

```
{
  "title": "towel",
  "size": "XL"
}
```

You will receive a response telling you that the data is invalid containing the received body:

```
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPI'sHTTPExceptionvs Starlette'sHTTPException¶

**FastAPI** has its own `HTTPException`.

And **FastAPI**'s `HTTPException` error class inherits from Starlette's `HTTPException` error class.

The only difference is that **FastAPI**'s `HTTPException` accepts any JSON-able data for the `detail` field, while Starlette's `HTTPException` only accepts strings for it.

So, you can keep raising **FastAPI**'s `HTTPException` as normally in your code.

But when you register an exception handler, you should register it for Starlette's `HTTPException`.

This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette `HTTPException`, your handler will be able to catch and handle it.

In this example, to be able to have both `HTTPException`s in the same code, Starlette's exceptions is renamed to `StarletteHTTPException`:

```
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### ReuseFastAPI's exception handlers¶

If you want to use the exception along with the same default exception handlers from  **FastAPI**, you can import and reuse the default exception handlers from `fastapi.exception_handlers`:

 [Python 3.9+](#__tabbed_8_1)

```
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
```

In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.
