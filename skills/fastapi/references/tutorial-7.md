# Header Parameter Models¶ and more

# Header Parameter Models¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Header Parameter Models¶

If you have a group of related **header parameters**, you can create a **Pydantic model** to declare them.

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

Note

This is supported since FastAPI version `0.115.0`. 🤓

## Header Parameters with a Pydantic Model¶

Declare the **header parameters** that you need in a **Pydantic model**, and then declare the parameter as `Header`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

**FastAPI** will **extract** the data for **each field** from the **headers** in the request and give you the Pydantic model you defined.

## Check the Docs¶

You can see the required headers in the docs UI at `/docs`:

  ![image](https://fastapi.tiangolo.com/img/tutorial/header-param-models/image01.png)

## Forbid Extra Headers¶

In some special use cases (probably not very common), you might want to **restrict** the headers that you want to receive.

You can use Pydantic's model configuration to `forbid` any `extra` fields:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header()):
    return headers
```

If a client tries to send some **extra headers**, they will receive an **error** response.

For example, if the client tries to send a `tool` header with a value of `plumbus`, they will receive an **error** response telling them that the header parameter `tool` is not allowed:

```
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Disable Convert Underscores¶

The same way as with regular header parameters, when you have underscore characters in the parameter names, they are **automatically converted to hyphens**.

For example, if you have a header parameter `save_data` in the code, the expected HTTP header will be `save-data`, and it will show up like that in the docs.

If for some reason you need to disable this automatic conversion, you can do it as well for Pydantic models for header parameters.

 [Python 3.10+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header(convert_underscores=False)],
):
    return headers
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)[Python 3.10+ - non-Annotated](#__tabbed_6_2)[Python 3.9+ - non-Annotated](#__tabbed_6_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header(convert_underscores=False)],
):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header(convert_underscores=False)):
    return headers
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: CommonHeaders = Header(convert_underscores=False)):
    return headers
```

Warning

Before setting `convert_underscores` to `False`, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

## Summary¶

You can use **Pydantic models** to declare **headers** in **FastAPI**. 😎

---

# Header Parameters¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Header Parameters¶

You can define Header parameters the same way you define `Query`, `Path` and `Cookie` parameters.

## ImportHeader¶

First import `Header`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
```

## DeclareHeaderparameters¶

Then declare the header parameters using the same structure as with `Path`, `Query` and `Cookie`.

You can define the default value as well as all the extra validation or annotation parameters:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}
```

Technical Details

`Header` is a "sister" class of `Path`, `Query` and `Cookie`. It also inherits from the same common `Param` class.

But remember that when you import `Query`, `Path`, `Header`, and others from `fastapi`, those are actually functions that return special classes.

Info

To declare headers, you need to use `Header`, because otherwise the parameters would be interpreted as query parameters.

## Automatic conversion¶

`Header` has a little extra functionality on top of what `Path`, `Query` and `Cookie` provide.

Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (`-`).

But a variable like `user-agent` is invalid in Python.

So, by default, `Header` will convert the parameter names characters from underscore (`_`) to hyphen (`-`) to extract and document the headers.

Also, HTTP headers are case-insensitive, so, you can declare them with standard Python style (also known as "snake_case").

So, you can use `user_agent` as you normally would in Python code, instead of needing to capitalize the first letters as `User_Agent` or something similar.

If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter `convert_underscores` of `Header` to `False`:

 [Python 3.10+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    return {"strange_header": strange_header}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)[Python 3.10+ - non-Annotated](#__tabbed_6_2)[Python 3.9+ - non-Annotated](#__tabbed_6_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    strange_header: Annotated[
        Union[str, None], Header(convert_underscores=False)
    ] = None,
):
    return {"strange_header": strange_header}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    strange_header: str | None = Header(default=None, convert_underscores=False),
):
    return {"strange_header": strange_header}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    strange_header: Union[str, None] = Header(default=None, convert_underscores=False),
):
    return {"strange_header": strange_header}
```

Warning

Before setting `convert_underscores` to `False`, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores.

## Duplicate headers¶

It is possible to receive duplicate headers. That means, the same header with multiple values.

You can define those cases using a list in the type declaration.

You will receive all the values from the duplicate header as a Python `list`.

For example, to declare a header of `X-Token` that can appear more than once, you can write:

 [Python 3.10+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)[Python 3.10+ - non-Annotated](#__tabbed_8_2)[Python 3.9+ - non-Annotated](#__tabbed_8_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Annotated[Union[list[str], None], Header()] = None):
    return {"X-Token values": x_token}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: list[str] | None = Header(default=None)):
    return {"X-Token values": x_token}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: Union[list[str], None] = Header(default=None)):
    return {"X-Token values": x_token}
```

If you communicate with that *path operation* sending two HTTP headers like:

```
X-Token: foo
X-Token: bar
```

The response would be like:

```
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Recap¶

Declare headers with `Header`, using the same common pattern as `Query`, `Path` and `Cookie`.

And don't worry about underscores in your variables, **FastAPI** will take care of converting them.

---

# Metadata and Docs URLs¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Metadata and Docs URLs¶

You can customize several metadata configurations in your **FastAPI** application.

## Metadata for API¶

You can set the following fields that are used in the OpenAPI specification and the automatic API docs UIs:

| Parameter | Type | Description |
| --- | --- | --- |
| title | str | The title of the API. |
| summary | str | A short summary of the API.Available since OpenAPI 3.1.0, FastAPI 0.99.0. |
| description | str | A short description of the API. It can use Markdown. |
| version | string | The version of the API. This is the version of your own application, not of OpenAPI. For example2.5.0. |
| terms_of_service | str | A URL to the Terms of Service for the API. If provided, this has to be a URL. |
| contact | dict | The contact information for the exposed API. It can contain several fields.contactfieldsParameterTypeDescriptionnamestrThe identifying name of the contact person/organization.urlstrThe URL pointing to the contact information. MUST be in the format of a URL.emailstrThe email address of the contact person/organization. MUST be in the format of an email address. |
| Parameter | Type | Description |
| name | str | The identifying name of the contact person/organization. |
| url | str | The URL pointing to the contact information. MUST be in the format of a URL. |
| email | str | The email address of the contact person/organization. MUST be in the format of an email address. |
| license_info | dict | The license information for the exposed API. It can contain several fields.license_infofieldsParameterTypeDescriptionnamestrREQUIRED(if alicense_infois set). The license name used for the API.identifierstrAnSPDXlicense expression for the API. Theidentifierfield is mutually exclusive of theurlfield.Available since OpenAPI 3.1.0, FastAPI 0.99.0.urlstrA URL to the license used for the API. MUST be in the format of a URL. |
| Parameter | Type | Description |
| name | str | REQUIRED(if alicense_infois set). The license name used for the API. |
| identifier | str | AnSPDXlicense expression for the API. Theidentifierfield is mutually exclusive of theurlfield.Available since OpenAPI 3.1.0, FastAPI 0.99.0. |
| url | str | A URL to the license used for the API. MUST be in the format of a URL. |

You can set them as follows:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

Tip

You can write Markdown in the `description` field and it will be rendered in the output.

With this configuration, the automatic API docs would look like:

![image](https://fastapi.tiangolo.com/img/tutorial/metadata/image01.png)

## License identifier¶

Since OpenAPI 3.1.0 and FastAPI 0.99.0, you can also set the `license_info` with an `identifier` instead of a `url`.

For example:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)

@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
```

## Metadata for tags¶

You can also add additional metadata for the different tags used to group your path operations with the parameter `openapi_tags`.

It takes a list containing one dictionary for each tag.

Each dictionary can contain:

- `name` (**required**): a `str` with the same tag name you use in the `tags` parameter in your *path operations* and `APIRouter`s.
- `description`: a `str` with a short description for the tag. It can have Markdown and will be shown in the docs UI.
- `externalDocs`: a `dict` describing external documentation with:
  - `description`: a `str` with a short description for the external docs.
  - `url` (**required**): a `str` with the URL for the external documentation.

### Create metadata for tags¶

Let's try that in an example with tags for `users` and `items`.

Create metadata for your tags and pass it to the `openapi_tags` parameter:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]

@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

Notice that you can use Markdown inside of the descriptions, for example "login" will be shown in bold (**login**) and "fancy" will be shown in italics (*fancy*).

Tip

You don't have to add metadata for all the tags that you use.

### Use your tags¶

Use the `tags` parameter with your *path operations* (and `APIRouter`s) to assign them to different tags:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]

@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]
```

Info

Read more about tags in [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).

### Check the docs¶

Now, if you check the docs, they will show all the additional metadata:

![image](https://fastapi.tiangolo.com/img/tutorial/metadata/image02.png)

### Order of tags¶

The order of each tag metadata dictionary also defines the order shown in the docs UI.

For example, even though `users` would go after `items` in alphabetical order, it is shown before them, because we added their metadata as the first dictionary in the list.

## OpenAPI URL¶

By default, the OpenAPI schema is served at `/openapi.json`.

But you can configure it with the parameter `openapi_url`.

For example, to set it to be served at `/api/v1/openapi.json`:

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

If you want to disable the OpenAPI schema completely you can set `openapi_url=None`, that will also disable the documentation user interfaces that use it.

## Docs URLs¶

You can configure the two documentation user interfaces included:

- **Swagger UI**: served at `/docs`.
  - You can set its URL with the parameter `docs_url`.
  - You can disable it by setting `docs_url=None`.
- **ReDoc**: served at `/redoc`.
  - You can set its URL with the parameter `redoc_url`.
  - You can disable it by setting `redoc_url=None`.

For example, to set Swagger UI to be served at `/documentation` and disable ReDoc:

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

---

# Middleware¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Middleware¶

You can add middleware to **FastAPI** applications.

A "middleware" is a function that works with every **request** before it is processed by any specific *path operation*. And also with every **response** before returning it.

- It takes each **request** that comes to your application.
- It can then do something to that **request** or run any needed code.
- Then it passes the **request** to be processed by the rest of the application (by some *path operation*).
- It then takes the **response** generated by the application (by some *path operation*).
- It can do something to that **response** or run any needed code.
- Then it returns the **response**.

Technical Details

If you have dependencies with `yield`, the exit code will run *after* the middleware.

If there were any background tasks (covered in the [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) section, you will see it later), they will run *after* all the middleware.

## Create a middleware¶

To create a middleware you use the decorator `@app.middleware("http")` on top of a function.

The middleware function receives:

- The `request`.
- A function `call_next` that will receive the `request` as a parameter.
  - This function will pass the `request` to the corresponding *path operation*.
  - Then it returns the `response` generated by the corresponding *path operation*.
- You can then further modify the `response` before returning it.

 [Python 3.9+](#__tabbed_1_1)

```
import time

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Tip

Keep in mind that custom proprietary headers can be added [using theX-prefix](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

But if you have custom headers that you want a client in a browser to be able to see, you need to add them to your CORS configurations ([CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/)) using the parameter `expose_headers` documented in [Starlette's CORS docs](https://www.starlette.dev/middleware/#corsmiddleware).

Technical Details

You could also use `from starlette.requests import Request`.

**FastAPI** provides it as a convenience for you, the developer. But it comes directly from Starlette.

### Before and after theresponse¶

You can add code to be run with the `request`,  before any *path operation* receives it.

And also after the `response` is generated, before returning it.

For example, you could add a custom header `X-Process-Time` containing the time in seconds that it took to process the request and generate a response:

 [Python 3.9+](#__tabbed_2_1)

```
import time

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

Tip

Here we use [time.perf_counter()](https://docs.python.org/3/library/time.html#time.perf_counter) instead of `time.time()` because it can be more precise for these use cases. 🤓

## Multiple middleware execution order¶

When you add multiple middlewares using either `@app.middleware()` decorator or `app.add_middleware()` method, each new middleware wraps the application, forming a stack. The last middleware added is the *outermost*, and the first is the *innermost*.

On the request path, the *outermost* middleware runs first.

On the response path, it runs last.

For example:

```
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

This results in the following execution order:

- **Request**: MiddlewareB → MiddlewareA → route
- **Response**: route → MiddlewareA → MiddlewareB

This stacking behavior ensures that middlewares are executed in a predictable and controllable order.

## Other middlewares¶

You can later read more about other middlewares in the [Advanced User Guide: Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

You will read about how to handle CORS with a middleware in the next section.

---

# Path Operation Configuration¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Path Operation Configuration¶

There are several parameters that you can pass to your *path operation decorator* to configure it.

Warning

Notice that these parameters are passed directly to the *path operation decorator*, not to your *path operation function*.

## Response Status Code¶

You can define the (HTTP) `status_code` to be used in the response of your *path operation*.

You can pass directly the `int` code, like `404`.

But if you don't remember what each number code is for, you can use the shortcut constants in `status`:

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

That status code will be used in the response and will be added to the OpenAPI schema.

Technical Details

You could also use `from starlette import status`.

**FastAPI** provides the same `starlette.status` as `fastapi.status` just as a convenience for you, the developer. But it comes directly from Starlette.

## Tags¶

You can add tags to your *path operation*, pass the parameter `tags` with a `list` of `str` (commonly just one `str`):

 [Python 3.10+](#__tabbed_3_1)

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

@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

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

@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
```

They will be added to the OpenAPI schema and used by the automatic documentation interfaces:

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image01.png)

### Tags with Enums¶

If you have a big application, you might end up accumulating **several tags**, and you would want to make sure you always use the **same tag** for related *path operations*.

In these cases, it could make sense to store the tags in an `Enum`.

**FastAPI** supports that the same way as with plain strings:

 [Python 3.9+](#__tabbed_5_1)

```
from enum import Enum

from fastapi import FastAPI

app = FastAPI()

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
```

## Summary and description¶

You can add a `summary` and `description`:

 [Python 3.10+](#__tabbed_6_1)

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

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_7_1)

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

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
```

## Description from docstring¶

As descriptions tend to be long and cover multiple lines, you can declare the *path operation* description in the function docstring and **FastAPI** will read it from there.

You can write [Markdown](https://en.wikipedia.org/wiki/Markdown) in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).

 [Python 3.10+](#__tabbed_8_1)

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
    """
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_9_1)

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
    """
    return item
```

It will be used in the interactive docs:

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image02.png)

## Response description¶

You can specify the response description with the parameter `response_description`:

 [Python 3.10+](#__tabbed_10_1)

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

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_11_1)

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

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
```

Info

Notice that `response_description` refers specifically to the response, the `description` refers to the *path operation* in general.

Check

OpenAPI specifies that each *path operation* requires a response description.

So, if you don't provide one, **FastAPI** will automatically generate one of "Successful response".

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image03.png)

## Deprecate apath operation¶

If you need to mark a *path operation* as deprecated, but without removing it, pass the parameter `deprecated`:

 [Python 3.9+](#__tabbed_12_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
```

It will be clearly marked as deprecated in the interactive docs:

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image04.png)

Check how deprecated and non-deprecated *path operations* look like:

![image](https://fastapi.tiangolo.com/img/tutorial/path-operation-configuration/image05.png)

## Recap¶

You can configure and add metadata for your *path operations* easily by passing parameters to the *path operation decorators*.
