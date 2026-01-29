# Request Body¶ and more

# Request Body¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Request Body¶

When you need to send data from a client (let's say, a browser) to your API, you send it as a **request body**.

A **request** body is data sent by the client to your API. A **response** body is the data your API sends to the client.

Your API almost always has to send a **response** body. But clients don't necessarily need to send **request bodies** all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body.

To declare a **request** body, you use [Pydantic](https://docs.pydantic.dev/) models with all their power and benefits.

Info

To send data, you should use one of: `POST` (the more common), `PUT`, `DELETE` or `PATCH`.

Sending a body with a `GET` request has an undefined behavior in the specifications, nevertheless, it is supported by FastAPI, only for very complex/extreme use cases.

As it is discouraged, the interactive docs with Swagger UI won't show the documentation for the body when using `GET`, and proxies in the middle might not support it.

## Import Pydantic'sBaseModel¶

First, you need to import `BaseModel` from `pydantic`:

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## Create your data model¶

Then you declare your data model as a class that inherits from `BaseModel`.

Use standard Python types for all the attributes:

 [Python 3.10+](#__tabbed_3_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

The same as when declaring query parameters, when a model attribute has a default value, it is not required. Otherwise, it is required. Use `None` to make it just optional.

For example, this model above declares a JSON "`object`" (or Python `dict`) like:

```
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...as `description` and `tax` are optional (with a default value of `None`), this JSON "`object`" would also be valid:

```
{
    "name": "Foo",
    "price": 45.2
}
```

## Declare it as a parameter¶

To add it to your *path operation*, declare it the same way you declared path and query parameters:

 [Python 3.10+](#__tabbed_5_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

...and declare its type as the model you created, `Item`.

## Results¶

With just that Python type declaration, **FastAPI** will:

- Read the body of the request as JSON.
- Convert the corresponding types (if needed).
- Validate the data.
  - If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
- Give you the received data in the parameter `item`.
  - As you declared it in the function to be of type `Item`, you will also have all the editor support (completion, etc) for all of the attributes and their types.
- Generate [JSON Schema](https://json-schema.org) definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
- Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.

## Automatic docs¶

The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:

![image](https://fastapi.tiangolo.com/img/tutorial/body/image01.png)

And will also be used in the API docs inside each *path operation* that needs them:

![image](https://fastapi.tiangolo.com/img/tutorial/body/image02.png)

## Editor support¶

In your editor, inside your function you will get type hints and completion everywhere (this wouldn't happen if you received a `dict` instead of a Pydantic model):

![image](https://fastapi.tiangolo.com/img/tutorial/body/image03.png)

You also get error checks for incorrect type operations:

![image](https://fastapi.tiangolo.com/img/tutorial/body/image04.png)

This is not by chance, the whole framework was built around that design.

And it was thoroughly tested at the design phase, before any implementation, to ensure it would work with all the editors.

There were even some changes to Pydantic itself to support this.

The previous screenshots were taken with [Visual Studio Code](https://code.visualstudio.com).

But you would get the same editor support with [PyCharm](https://www.jetbrains.com/pycharm/) and most of the other Python editors:

![image](https://fastapi.tiangolo.com/img/tutorial/body/image05.png)

Tip

If you use [PyCharm](https://www.jetbrains.com/pycharm/) as your editor, you can use the [Pydantic PyCharm Plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin/).

It improves editor support for Pydantic models, with:

- auto-completion
- type checks
- refactoring
- searching
- inspections

## Use the model¶

Inside of the function, you can access all the attributes of the model object directly:

 [Python 3.10+](#__tabbed_7_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

## Request body + path parameters¶

You can declare path parameters and request body at the same time.

**FastAPI** will recognize that the function parameters that match path parameters should be **taken from the path**, and that function parameters that are declared to be Pydantic models should be **taken from the request body**.

 [Python 3.10+](#__tabbed_9_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

## Request body + path + query parameters¶

You can also declare **body**, **path** and **query** parameters, all at the same time.

**FastAPI** will recognize each of them and take the data from the correct place.

 [Python 3.10+](#__tabbed_11_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_12_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```

The function parameters will be recognized as follows:

- If the parameter is also declared in the **path**, it will be used as a path parameter.
- If the parameter is of a **singular type** (like `int`, `float`, `str`, `bool`, etc) it will be interpreted as a **query** parameter.
- If the parameter is declared to be of the type of a **Pydantic model**, it will be interpreted as a request **body**.

Note

FastAPI will know that the value of `q` is not required because of the default value `= None`.

The `str | None` (Python 3.10+) or `Union` in `Union[str, None]` (Python 3.9+) is not used by FastAPI to determine that the value is not required, it will know it's not required because it has a default value of `= None`.

But adding the type annotations will allow your editor to give you better support and detect errors.

## Without Pydantic¶

If you don't want to use Pydantic models, you can also use **Body** parameters. See the docs for [Body - Multiple Parameters: Singular values in body](https://fastapi.tiangolo.com/tutorial/body-multiple-params/#singular-values-in-body).

---

# Cookie Parameter Models¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Cookie Parameter Models¶

If you have a group of **cookies** that are related, you can create a **Pydantic model** to declare them. 🍪

This would allow you to **re-use the model** in **multiple places** and also to declare validations and metadata for all the parameters at once. 😎

Note

This is supported since FastAPI version `0.115.0`. 🤓

Tip

This same technique applies to `Query`, `Cookie`, and `Header`. 😎

## Cookies with a Pydantic Model¶

Declare the **cookie** parameters that you need in a **Pydantic model**, and then declare the parameter as `Cookie`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None

@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

**FastAPI** will **extract** the data for **each field** from the **cookies** received in the request and give you the Pydantic model you defined.

## Check the Docs¶

You can see the defined cookies in the docs UI at `/docs`:

  ![image](https://fastapi.tiangolo.com/img/tutorial/cookie-param-models/image01.png)

Info

Have in mind that, as **browsers handle cookies** in special ways and behind the scenes, they **don't** easily allow **JavaScript** to touch them.

If you go to the **API docs UI** at `/docs` you will be able to see the **documentation** for cookies for your *path operations*.

But even if you **fill the data** and click "Execute", because the docs UI works with **JavaScript**, the cookies won't be sent, and you will see an **error** message as if you didn't write any values.

## Forbid Extra Cookies¶

In some special use cases (probably not very common), you might want to **restrict** the cookies that you want to receive.

Your API now has the power to control its own cookie consent. 🤪🍪

You can use Pydantic's model configuration to `forbid` any `extra` fields:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None

@app.get("/items/")
async def read_items(cookies: Cookies = Cookie()):
    return cookies
```

If a client tries to send some **extra cookies**, they will receive an **error** response.

Poor cookie banners with all their effort to get your consent for the API to reject it. 🍪

For example, if the client tries to send a `santa_tracker` cookie with a value of `good-list-please`, the client will receive an **error** response telling them that the `santa_tracker` cookie is not allowed:

```
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## Summary¶

You can use **Pydantic models** to declare **cookies** in **FastAPI**. 😎

---

# Cookie Parameters¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Cookie Parameters¶

You can define Cookie parameters the same way you define `Query` and `Path` parameters.

## ImportCookie¶

First import `Cookie`:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```

## DeclareCookieparameters¶

Then declare the cookie parameters using the same structure as with `Path` and `Query`.

You can define the default value as well as all the extra validation or annotation parameters:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Cookie, FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```

Technical Details

`Cookie` is a "sister" class of `Path` and `Query`. It also inherits from the same common `Param` class.

But remember that when you import `Query`, `Path`, `Cookie` and others from `fastapi`, those are actually functions that return special classes.

Info

To declare cookies, you need to use `Cookie`, because otherwise the parameters would be interpreted as query parameters.

Info

Have in mind that, as **browsers handle cookies** in special ways and behind the scenes, they **don't** easily allow **JavaScript** to touch them.

If you go to the **API docs UI** at `/docs` you will be able to see the **documentation** for cookies for your *path operations*.

But even if you **fill the data** and click "Execute", because the docs UI works with **JavaScript**, the cookies won't be sent, and you will see an **error** message as if you didn't write any values.

## Recap¶

Declare cookies with `Cookie`, using the same common pattern as `Query` and `Path`.

---

# CORS (Cross

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# CORS (Cross-Origin Resource Sharing)¶

[CORS or "Cross-Origin Resource Sharing"](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) refers to the situations when a frontend running in a browser has JavaScript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

## Origin¶

An origin is the combination of protocol (`http`, `https`), domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`), and port (`80`, `443`, `8080`).

So, all these are different origins:

- `http://localhost`
- `https://localhost`
- `http://localhost:8080`

Even if they are all in `localhost`, they use different protocols or ports, so, they are different "origins".

## Steps¶

So, let's say you have a frontend running in your browser at `http://localhost:8080`, and its JavaScript is trying to communicate with a backend running at `http://localhost` (because we don't specify a port, the browser will assume the default port `80`).

Then, the browser will send an HTTP `OPTIONS` request to the `:80`-backend, and if the backend sends the appropriate headers authorizing the communication from this different origin (`http://localhost:8080`) then the `:8080`-browser will let the JavaScript in the frontend send its request to the `:80`-backend.

To achieve this, the `:80`-backend must have a list of "allowed origins".

In this case, the list would have to include `http://localhost:8080` for the `:8080`-frontend to work correctly.

## Wildcards¶

It's also possible to declare the list as `"*"` (a "wildcard") to say that all are allowed.

But that will only allow certain types of communication, excluding everything that involves credentials: Cookies, Authorization headers like those used with Bearer Tokens, etc.

So, for everything to work correctly, it's better to specify explicitly the allowed origins.

## UseCORSMiddleware¶

You can configure it in your **FastAPI** application using the `CORSMiddleware`.

- Import `CORSMiddleware`.
- Create a list of allowed origins (as strings).
- Add it as a "middleware" to your **FastAPI** application.

You can also specify whether your backend allows:

- Credentials (Authorization headers, Cookies, etc).
- Specific HTTP methods (`POST`, `PUT`) or all of them with the wildcard `"*"`.
- Specific HTTP headers or all of them with the wildcard `"*"`.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

The default parameters used by the `CORSMiddleware` implementation are restrictive by default, so you'll need to explicitly enable particular origins, methods, or headers, in order for browsers to be permitted to use them in a Cross-Domain context.

The following arguments are supported:

- `allow_origins` - A list of origins that should be permitted to make cross-origin requests. E.g. `['https://example.org', 'https://www.example.org']`. You can use `['*']` to allow any origin.
- `allow_origin_regex` - A regex string to match against origins that should be permitted to make cross-origin requests. e.g. `'https://.*\.example\.org'`.
- `allow_methods` - A list of HTTP methods that should be allowed for cross-origin requests. Defaults to `['GET']`. You can use `['*']` to allow all standard methods.
- `allow_headers` - A list of HTTP request headers that should be supported for cross-origin requests. Defaults to `[]`. You can use `['*']` to allow all headers. The `Accept`, `Accept-Language`, `Content-Language` and `Content-Type` headers are always allowed for [simple CORS requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests).
- `allow_credentials` - Indicate that cookies should be supported for cross-origin requests. Defaults to `False`.
  None of `allow_origins`, `allow_methods` and `allow_headers` can be set to `['*']` if `allow_credentials` is set to `True`. All of them must be [explicitly specified](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards).
- `expose_headers` - Indicate any response headers that should be made accessible to the browser. Defaults to `[]`.
- `max_age` - Sets a maximum time in seconds for browsers to cache CORS responses. Defaults to `600`.

The middleware responds to two particular types of HTTP request...

### CORS preflight requests¶

These are any `OPTIONS` request with `Origin` and `Access-Control-Request-Method` headers.

In this case the middleware will intercept the incoming request and respond with appropriate CORS headers, and either a `200` or `400` response for informational purposes.

### Simple requests¶

Any request with an `Origin` header. In this case the middleware will pass the request through as normal, but will include appropriate CORS headers on the response.

## More info¶

For more info about CORS, check the [Mozilla CORS documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

Technical Details

You could also use `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** provides several middlewares in `fastapi.middleware` just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.

---

# Debugging¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Debugging¶

You can connect the debugger in your editor, for example with Visual Studio Code or PyCharm.

## Calluvicorn¶

In your FastAPI application, import and run `uvicorn` directly:

 [Python 3.9+](#__tabbed_1_1)

```
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### About__name__ == "__main__"¶

The main purpose of the `__name__ == "__main__"` is to have some code that is executed when your file is called with:

```
python myapp.py
```

but is not called when another file imports it, like in:

```
from myapp import app
```

#### More details¶

Let's say your file is named `myapp.py`.

If you run it with:

```
python myapp.py
```

then the internal variable `__name__` in your file, created automatically by Python, will have as value the string `"__main__"`.

So, the section:

```
uvicorn.run(app, host="0.0.0.0", port=8000)
```

will run.

---

This won't happen if you import that module (file).

So, if you have another file `importer.py` with:

```
from myapp import app

# Some more code
```

in that case, the automatically created variable `__name__` inside of `myapp.py` will not have the value `"__main__"`.

So, the line:

```
uvicorn.run(app, host="0.0.0.0", port=8000)
```

will not be executed.

Info

For more information, check [the official Python docs](https://docs.python.org/3/library/__main__.html).

## Run your code with your debugger¶

Because you are running the Uvicorn server directly from your code, you can call your Python program (your FastAPI application) directly from the debugger.

---

For example, in Visual Studio Code, you can:

- Go to the "Debug" panel.
- "Add configuration...".
- Select "Python"
- Run the debugger with the option "`Python: Current File (Integrated Terminal)`".

It will then start the server with your **FastAPI** code, stop at your breakpoints, etc.

Here's how it might look:

![image](https://fastapi.tiangolo.com/img/tutorial/debugging/image01.png)

---

If you use Pycharm, you can:

- Open the "Run" menu.
- Select the option "Debug...".
- Then a context menu shows up.
- Select the file to debug (in this case, `main.py`).

It will then start the server with your **FastAPI** code, stop at your breakpoints, etc.

Here's how it might look:

![image](https://fastapi.tiangolo.com/img/tutorial/debugging/image02.png)
