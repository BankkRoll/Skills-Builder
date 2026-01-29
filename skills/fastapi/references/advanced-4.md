# OpenAPI Webhooks¶ and more

# OpenAPI Webhooks¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# OpenAPI Webhooks¶

There are cases where you want to tell your API **users** that your app could call *their* app (sending a request) with some data, normally to **notify** of some type of **event**.

This means that instead of the normal process of your users sending requests to your API, it's **your API** (or your app) that could **send requests to their system** (to their API, their app).

This is normally called a **webhook**.

## Webhooks steps¶

The process normally is that **you define** in your code what is the message that you will send, the **body of the request**.

You also define in some way at which **moments** your app will send those requests or events.

And **your users** define in some way (for example in a web dashboard somewhere) the **URL** where your app should send those requests.

All the **logic** about how to register the URLs for webhooks and the code to actually send those requests is up to you. You write it however you want to in **your own code**.

## Documenting webhooks withFastAPIand OpenAPI¶

With **FastAPI**, using OpenAPI, you can define the names of these webhooks, the types of HTTP operations that your app can send (e.g. `POST`, `PUT`, etc.) and the request **bodies** that your app would send.

This can make it a lot easier for your users to **implement their APIs** to receive your **webhook** requests, they might even be able to autogenerate some of their own API code.

Info

Webhooks are available in OpenAPI 3.1.0 and above, supported by FastAPI `0.99.0` and above.

## An app with webhooks¶

When you create a **FastAPI** application, there is a `webhooks` attribute that you can use to define *webhooks*, the same way you would define *path operations*, for example with `@app.webhooks.post()`.

 [Python 3.9+](#__tabbed_1_1)

```
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

@app.webhooks.post("new-subscription")
def new_subscription(body: Subscription):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """

@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]
```

The webhooks that you define will end up in the **OpenAPI** schema and the automatic **docs UI**.

Info

The `app.webhooks` object is actually just an `APIRouter`, the same type you would use when structuring your app with multiple files.

Notice that with webhooks you are actually not declaring a *path* (like `/items/`), the text you pass there is just an **identifier** of the webhook (the name of the event), for example in `@app.webhooks.post("new-subscription")`, the webhook name is `new-subscription`.

This is because it is expected that **your users** would define the actual **URL path** where they want to receive the webhook request in some other way (e.g. a web dashboard).

### Check the docs¶

Now you can start your app and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see your docs have the normal *path operations* and now also some **webhooks**:

![image](https://fastapi.tiangolo.com/img/tutorial/openapi-webhooks/image01.png)

---

# Path Operation Advanced Configuration¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Path Operation Advanced Configuration¶

## OpenAPI operationId¶

Warning

If you are not an "expert" in OpenAPI, you probably don't need this.

You can set the OpenAPI `operationId` to be used in your *path operation* with the parameter `operation_id`.

You would have to make sure that it is unique for each operation.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", operation_id="some_specific_id_you_define")
async def read_items():
    return [{"item_id": "Foo"}]
```

### Using thepath operation functionname as the operationId¶

If you want to use your APIs' function names as `operationId`s, you can iterate over all of them and override each *path operation's* `operation_id` using their `APIRoute.name`.

You should do it after adding all your *path operations*.

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.routing import APIRoute

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

use_route_names_as_operation_ids(app)
```

Tip

If you manually call `app.openapi()`, you should update the `operationId`s before that.

Warning

If you do this, you have to make sure each one of your *path operation functions* has a unique name.

Even if they are in different modules (Python files).

## Exclude from OpenAPI¶

To exclude a *path operation* from the generated OpenAPI schema (and thus, from the automatic documentation systems), use the parameter `include_in_schema` and set it to `False`:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", include_in_schema=False)
async def read_items():
    return [{"item_id": "Foo"}]
```

## Advanced description from docstring¶

You can limit the lines used from the docstring of a *path operation function* for OpenAPI.

Adding an `\f` (an escaped "form feed" character) causes **FastAPI** to truncate the output used for OpenAPI at this point.

It won't show up in the documentation, but other tools (such as Sphinx) will be able to use the rest.

 [Python 3.10+](#__tabbed_4_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_5_1)

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
    tags: set[str] = set()

@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item
```

## Additional Responses¶

You probably have seen how to declare the `response_model` and `status_code` for a *path operation*.

That defines the metadata about the main response of a *path operation*.

You can also declare additional responses with their models, status codes, etc.

There's a whole chapter here in the documentation about it, you can read it at [Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

## OpenAPI Extra¶

When you declare a *path operation* in your application, **FastAPI** automatically generates the relevant metadata about that *path operation* to be included in the OpenAPI schema.

Technical details

In the OpenAPI specification it is called the [Operation Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object).

It has all the information about the *path operation* and is used to generate the automatic documentation.

It includes the `tags`, `parameters`, `requestBody`, `responses`, etc.

This *path operation*-specific OpenAPI schema is normally generated automatically by **FastAPI**, but you can also extend it.

Tip

This is a low level extension point.

If you only need to declare additional responses, a more convenient way to do it is with [Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

You can extend the OpenAPI schema for a *path operation* using the parameter `openapi_extra`.

### OpenAPI Extensions¶

This `openapi_extra` can be helpful, for example, to declare [OpenAPI Extensions](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", openapi_extra={"x-aperture-labs-portal": "blue"})
async def read_items():
    return [{"item_id": "portal-gun"}]
```

If you open the automatic API docs, your extension will show up at the bottom of the specific *path operation*.

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-advanced-configuration/image01.png)

And if you see the resulting OpenAPI (at `/openapi.json` in your API), you will see your extension as part of the specific *path operation* too:

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
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Custom OpenAPIpath operationschema¶

The dictionary in `openapi_extra` will be deeply merged with the automatically generated OpenAPI schema for the *path operation*.

So, you could add additional data to the automatically generated schema.

For example, you could decide to read and validate the request with your own code, without using the automatic features of FastAPI with Pydantic, but you could still want to define the request in the OpenAPI schema.

You could do that with `openapi_extra`:

 [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI, Request

app = FastAPI()

def magic_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "Maaaagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }

@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    data = magic_data_reader(raw_body)
    return data
```

In this example, we didn't declare any Pydantic model. In fact, the request body is not even parsed as JSON, it is read directly as `bytes`, and the function `magic_data_reader()` would be in charge of parsing it in some way.

Nevertheless, we can declare the expected schema for the request body.

### Custom OpenAPI content type¶

Using this same trick, you could use a Pydantic model to define the JSON Schema that is then included in the custom OpenAPI schema section for the *path operation*.

And you could do this even if the data type in the request is not JSON.

For example, in this application we don't use FastAPI's integrated functionality to extract the JSON Schema from Pydantic models nor the automatic validation for JSON. In fact, we are declaring the request content type as YAML, not JSON:

 [Python 3.9+](#__tabbed_8_1)

```
import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError

app = FastAPI()

class Item(BaseModel):
    name: str
    tags: list[str]

@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    return item
```

Nevertheless, although we are not using the default integrated functionality, we are still using a Pydantic model to manually generate the JSON Schema for the data that we want to receive in YAML.

Then we use the request directly, and extract the body as `bytes`. This means that FastAPI won't even try to parse the request payload as JSON.

And then in our code, we parse that YAML content directly, and then we are again using the same Pydantic model to validate the YAML content:

 [Python 3.9+](#__tabbed_9_1)

```
import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError

app = FastAPI()

class Item(BaseModel):
    name: str
    tags: list[str]

@app.post(
    "/items/",
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        item = Item.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    return item
```

Tip

Here we reuse the same Pydantic model.

But the same way, we could have validated it in some other way.

---

# Response

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Response - Change Status Code¶

You probably read before that you can set a default [Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).

But in some cases you need to return a different status code than the default.

## Use case¶

For example, imagine that you want to return an HTTP status code of "OK" `200` by default.

But if the data didn't exist, you want to create it, and return an HTTP status code of "CREATED" `201`.

But you still want to be able to filter and convert the data you return with a `response_model`.

For those cases, you can use a `Response` parameter.

## Use aResponseparameter¶

You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies and headers).

And then you can set the `status_code` in that *temporal* response object.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks = {"foo": "Listen to the Bar Fighters"}

@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
```

And then you can return any object you need, as you normally would (a `dict`, a database model, etc).

And if you declared a `response_model`, it will still be used to filter and convert the object you returned.

**FastAPI** will use that *temporal* response to extract the status code (also cookies and headers), and will put them in the final response that contains the value you returned, filtered by any `response_model`.

You can also declare the `Response` parameter in dependencies, and set the status code in them. But keep in mind that the last one to be set will win.

---

# Response Cookies¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Response Cookies¶

## Use aResponseparameter¶

You can declare a parameter of type `Response` in your *path operation function*.

And then you can set cookies in that *temporal* response object.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
```

And then you can return any object you need, as you normally would (a `dict`, a database model, etc).

And if you declared a `response_model`, it will still be used to filter and convert the object you returned.

**FastAPI** will use that *temporal* response to extract the cookies (also headers and status code), and will put them in the final response that contains the value you returned, filtered by any `response_model`.

You can also declare the `Response` parameter in dependencies, and set cookies (and headers) in them.

## Return aResponsedirectly¶

You can also create cookies when returning a `Response` directly in your code.

To do that, you can create a response as described in [Return a Response Directly](https://fastapi.tiangolo.com/advanced/response-directly/).

Then set Cookies in it, and then return it:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response
```

Tip

Keep in mind that if you return a response directly instead of using the `Response` parameter, FastAPI will return it directly.

So, you will have to make sure your data is of the correct type. E.g. it is compatible with JSON, if you are returning a `JSONResponse`.

And also that you are not sending any data that should have been filtered by a `response_model`.

### More info¶

Technical Details

You could also use `from starlette.responses import Response` or `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

And as the `Response` can be used frequently to set headers and cookies, **FastAPI** also provides it at `fastapi.Response`.

To see all the available parameters and options, check the [documentation in Starlette](https://www.starlette.dev/responses/#set-cookie).

---

# Return a Response Directly¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Return a Response Directly¶

When you create a **FastAPI** *path operation* you can normally return any data from it: a `dict`, a `list`, a Pydantic model, a database model, etc.

By default, **FastAPI** would automatically convert that return value to JSON using the `jsonable_encoder` explained in [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).

Then, behind the scenes, it would put that JSON-compatible data (e.g. a `dict`) inside of a `JSONResponse` that would be used to send the response to the client.

But you can return a `JSONResponse` directly from your *path operations*.

It might be useful, for example, to return custom headers or cookies.

## Return aResponse¶

In fact, you can return any `Response` or any sub-class of it.

Tip

`JSONResponse` itself is a sub-class of `Response`.

And when you return a `Response`, **FastAPI** will pass it directly.

It won't do any data conversion with Pydantic models, it won't convert the contents to any type, etc.

This gives you a lot of flexibility. You can return any data type, override any data declaration or validation, etc.

## Using thejsonable_encoderin aResponse¶

Because **FastAPI** doesn't make any changes to a `Response` you return, you have to make sure its contents are ready for it.

For example, you cannot put a Pydantic model in a `JSONResponse` without first converting it to a `dict` with all the data types (like `datetime`, `UUID`, etc) converted to JSON-compatible types.

For those cases, you can use the `jsonable_encoder` to convert your data before passing it to a response:

 [Python 3.10+](#__tabbed_1_1)

```
from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)
```

Technical Details

You could also use `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

## Returning a customResponse¶

The example above shows all the parts you need, but it's not very useful yet, as you could have just returned the `item` directly, and **FastAPI** would put it in a `JSONResponse` for you, converting it to a `dict`, etc. All that by default.

Now, let's see how you could use that to return a custom response.

Let's say that you want to return an [XML](https://en.wikipedia.org/wiki/XML) response.

You could put your XML content in a string, put that in a `Response`, and return it:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
```

## Notes¶

When you return a `Response` directly its data is not validated, converted (serialized), or documented automatically.

But you can still document it as described in [Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

You can see in later sections how to use/declare these custom `Response`s while still having automatic data conversion, documentation, etc.

---

# Response Headers¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Response Headers¶

## Use aResponseparameter¶

You can declare a parameter of type `Response` in your *path operation function* (as you can do for cookies).

And then you can set headers in that *temporal* response object.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}
```

And then you can return any object you need, as you normally would (a `dict`, a database model, etc).

And if you declared a `response_model`, it will still be used to filter and convert the object you returned.

**FastAPI** will use that *temporal* response to extract the headers (also cookies and status code), and will put them in the final response that contains the value you returned, filtered by any `response_model`.

You can also declare the `Response` parameter in dependencies, and set headers (and cookies) in them.

## Return aResponsedirectly¶

You can also add headers when you return a `Response` directly.

Create a response as described in [Return a Response Directly](https://fastapi.tiangolo.com/advanced/response-directly/) and pass the headers as an additional parameter:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
```

Technical Details

You could also use `from starlette.responses import Response` or `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

And as the `Response` can be used frequently to set headers and cookies, **FastAPI** also provides it at `fastapi.Response`.

## Custom Headers¶

Keep in mind that custom proprietary headers can be added [using theX-prefix](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations (read more in [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/)), using the parameter `expose_headers` documented in [Starlette's CORS docs](https://www.starlette.dev/middleware/#corsmiddleware).

---

# HTTP Basic Auth¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# HTTP Basic Auth¶

For the simplest cases, you can use HTTP Basic Auth.

In HTTP Basic Auth, the application expects a header that contains a username and a password.

If it doesn't receive it, it returns an HTTP 401 "Unauthorized" error.

And returns a header `WWW-Authenticate` with a value of `Basic`, and an optional `realm` parameter.

That tells the browser to show the integrated prompt for a username and password.

Then, when you type that username and password, the browser sends them in the header automatically.

## Simple HTTP Basic Auth¶

- Import `HTTPBasic` and `HTTPBasicCredentials`.
- Create a "`security` scheme" using `HTTPBasic`.
- Use that `security` with a dependency in your *path operation*.
- It returns an object of type `HTTPBasicCredentials`:
  - It contains the `username` and `password` sent.

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
```

When you try to open the URL for the first time (or click the "Execute" button in the docs) the browser will ask you for your username and password:

![image](https://fastapi.tiangolo.com/img/tutorial/security/image12.png)

## Check the username¶

Here's a more complete example.

Use a dependency to check if the username and password are correct.

For this, use the Python standard module [secrets](https://docs.python.org/3/library/secrets.html) to check the username and password.

`secrets.compare_digest()` needs to take `bytes` or a `str` that only contains ASCII characters (the ones in English), this means it wouldn't work with characters like `á`, as in `Sebastián`.

To handle that, we first convert the `username` and `password` to `bytes` encoding them with UTF-8.

Then we can use `secrets.compare_digest()` to ensure that `credentials.username` is `"stanleyjobson"`, and that `credentials.password` is `"swordfish"`.

 [Python 3.9+](#__tabbed_3_1)

```
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
```

This would be similar to:

```
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

But by using the `secrets.compare_digest()` it will be secure against a type of attacks called "timing attacks".

### Timing Attacks¶

But what's a "timing attack"?

Let's imagine some attackers are trying to guess the username and password.

And they send a request with a username `johndoe` and a password `love123`.

Then the Python code in your application would be equivalent to something like:

```
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

But right at the moment Python compares the first `j` in `johndoe` to the first `s` in `stanleyjobson`, it will return `False`, because it already knows that those two strings are not the same, thinking that "there's no need to waste more computation comparing the rest of the letters". And your application will say "Incorrect username or password".

But then the attackers try with username `stanleyjobsox` and password `love123`.

And your application code does something like:

```
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python will have to compare the whole `stanleyjobso` in both `stanleyjobsox` and `stanleyjobson` before realizing that both strings are not the same. So it will take some extra microseconds to reply back "Incorrect username or password".

#### The time to answer helps the attackers¶

At that point, by noticing that the server took some microseconds longer to send the "Incorrect username or password" response, the attackers will know that they got *something* right, some of the initial letters were right.

And then they can try again knowing that it's probably something more similar to `stanleyjobsox` than to `johndoe`.

#### A "professional" attack¶

Of course, the attackers would not try all this by hand, they would write a program to do it, possibly with thousands or millions of tests per second. And they would get just one extra correct letter at a time.

But doing that, in some minutes or hours the attackers would have guessed the correct username and password, with the "help" of our application, just using the time taken to answer.

#### Fix it withsecrets.compare_digest()¶

But in our code we are actually using `secrets.compare_digest()`.

In short, it will take the same time to compare `stanleyjobsox` to `stanleyjobson` than it takes to compare `johndoe` to `stanleyjobson`. And the same for the password.

That way, using `secrets.compare_digest()` in your application code, it will be safe against this whole range of security attacks.

### Return the error¶

After detecting that the credentials are incorrect, return an `HTTPException` with a status code 401 (the same returned when no credentials are provided) and add the header `WWW-Authenticate` to make the browser show the login prompt again:

 [Python 3.9+](#__tabbed_5_1)

```
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_6_1)

Tip

Prefer to use the `Annotated` version if possible.

```
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
```
