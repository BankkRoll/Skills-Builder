# Extending OpenAPI¶ and more

# Extending OpenAPI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Extending OpenAPI¶

There are some cases where you might need to modify the generated OpenAPI schema.

In this section you will see how.

## The normal process¶

The normal (default) process, is as follows.

A `FastAPI` application (instance) has an `.openapi()` method that is expected to return the OpenAPI schema.

As part of the application object creation, a *path operation* for `/openapi.json` (or for whatever you set your `openapi_url`) is registered.

It just returns a JSON response with the result of the application's `.openapi()` method.

By default, what the method `.openapi()` does is check the property `.openapi_schema` to see if it has contents and return them.

If it doesn't, it generates them using the utility function at `fastapi.openapi.utils.get_openapi`.

And that function `get_openapi()` receives as parameters:

- `title`: The OpenAPI title, shown in the docs.
- `version`: The version of your API, e.g. `2.5.0`.
- `openapi_version`: The version of the OpenAPI specification used. By default, the latest: `3.1.0`.
- `summary`: A short summary of the API.
- `description`: The description of your API, this can include markdown and will be shown in the docs.
- `routes`: A list of routes, these are each of the registered *path operations*. They are taken from `app.routes`.

Info

The parameter `summary` is available in OpenAPI 3.1.0 and above, supported by FastAPI 0.99.0 and above.

## Overriding the defaults¶

Using the information above, you can use the same utility function to generate the OpenAPI schema and override each part that you need.

For example, let's add [ReDoc's OpenAPI extension to include a custom logo](https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo).

### NormalFastAPI¶

First, write all your **FastAPI** application as normally:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Generate the OpenAPI schema¶

Then, use the same utility function to generate the OpenAPI schema, inside a `custom_openapi()` function:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Modify the OpenAPI schema¶

Now you can add the ReDoc extension, adding a custom `x-logo` to the `info` "object" in the OpenAPI schema:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Cache the OpenAPI schema¶

You can use the property `.openapi_schema` as a "cache", to store your generated schema.

That way, your application won't have to generate the schema every time a user opens your API docs.

It will be generated only once, and then the same cached schema will be used for the next requests.

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Override the method¶

Now you can replace the `.openapi()` method with your new function.

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Check it¶

Once you go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) you will see that you are using your custom logo (in this example, **FastAPI**'s logo):

![image](https://fastapi.tiangolo.com/img/tutorial/extending-openapi/image01.png)

---

# General

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# General - How To - Recipes¶

Here are several pointers to other places in the docs, for general or frequent questions.

## Filter Data - Security¶

To ensure that you don't return more data than you should, read the docs for [Tutorial - Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/).

## Documentation Tags - OpenAPI¶

To add tags to your *path operations*, and group them in the docs UI, read the docs for [Tutorial - Path Operation Configurations - Tags](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).

## Documentation Summary and Description - OpenAPI¶

To add a summary and description to your *path operations*, and show them in the docs UI, read the docs for [Tutorial - Path Operation Configurations - Summary and Description](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#summary-and-description).

## Documentation Response description - OpenAPI¶

To define the description of the response, shown in the docs UI, read the docs for [Tutorial - Path Operation Configurations - Response description](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#response-description).

## Documentation Deprecate aPath Operation- OpenAPI¶

To deprecate a *path operation*, and show it in the docs UI, read the docs for [Tutorial - Path Operation Configurations - Deprecation](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation).

## Convert any Data to JSON-compatible¶

To convert any data to JSON-compatible, read the docs for [Tutorial - JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).

## OpenAPI Metadata - Docs¶

To add metadata to your OpenAPI schema, including a license, version, contact, etc, read the docs for [Tutorial - Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/).

## OpenAPI Custom URL¶

To customize the OpenAPI URL (or remove it), read the docs for [Tutorial - Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

## OpenAPI Docs URLs¶

To update the URLs used for the automatically generated docs user interfaces, read the docs for [Tutorial - Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

---

# GraphQL¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# GraphQL¶

As **FastAPI** is based on the **ASGI** standard, it's very easy to integrate any **GraphQL** library also compatible with ASGI.

You can combine normal FastAPI *path operations* with GraphQL on the same application.

Tip

**GraphQL** solves some very specific use cases.

It has **advantages** and **disadvantages** when compared to common **web APIs**.

Make sure you evaluate if the **benefits** for your use case compensate the **drawbacks**. 🤓

## GraphQL Libraries¶

Here are some of the **GraphQL** libraries that have **ASGI** support. You could use them with **FastAPI**:

- [Strawberry](https://strawberry.rocks/) 🍓
  - With [docs for FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
- [Ariadne](https://ariadnegraphql.org/)
  - With [docs for FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
- [Tartiflette](https://tartiflette.io/)
  - With [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) to provide ASGI integration
- [Graphene](https://graphene-python.org/)
  - With [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL with Strawberry¶

If you need or want to work with **GraphQL**, [Strawberry](https://strawberry.rocks/) is the **recommended** library as it has the design closest to **FastAPI's** design, it's all based on **type annotations**.

Depending on your use case, you might prefer to use a different library, but if you asked me, I would probably suggest you try **Strawberry**.

Here's a small preview of how you could integrate Strawberry with FastAPI:

 [Python 3.9+](#__tabbed_1_1)

```
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    name: str
    age: int

@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

You can learn more about Strawberry in the [Strawberry documentation](https://strawberry.rocks/).

And also the docs about [Strawberry with FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## OlderGraphQLAppfrom Starlette¶

Previous versions of Starlette included a `GraphQLApp` class to integrate with [Graphene](https://graphene-python.org/).

It was deprecated from Starlette, but if you have code that used it, you can easily **migrate** to [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3), that covers the same use case and has an **almost identical interface**.

Tip

If you need GraphQL, I still would recommend you check out [Strawberry](https://strawberry.rocks/), as it's based on type annotations instead of custom classes and types.

## Learn More¶

You can learn more about **GraphQL** in the [official GraphQL documentation](https://graphql.org/).

You can also read more about each those libraries described above in their links.

---

# Migrate from Pydantic v1 to Pydantic v2¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Migrate from Pydantic v1 to Pydantic v2¶

If you have an old FastAPI app, you might be using Pydantic version 1.

FastAPI version 0.100.0 had support for either Pydantic v1 or v2. It would use whichever you had installed.

FastAPI version 0.119.0 introduced partial support for Pydantic v1 from inside of Pydantic v2 (as `pydantic.v1`), to facilitate the migration to v2.

FastAPI 0.126.0 dropped support for Pydantic v1, while still supporting `pydantic.v1` for a little while.

Warning

The Pydantic team stopped support for Pydantic v1 for the latest versions of Python, starting with **Python 3.14**.

This includes `pydantic.v1`, which is no longer supported in Python 3.14 and above.

If you want to use the latest features of Python, you will need to make sure you use Pydantic v2.

If you have an old FastAPI app with Pydantic v1, here I'll show you how to migrate it to Pydantic v2, and the **features in FastAPI 0.119.0** to help you with a gradual migration.

## Official Guide¶

Pydantic has an official [Migration Guide](https://docs.pydantic.dev/latest/migration/) from v1 to v2.

It also includes what has changed, how validations are now more correct and strict, possible caveats, etc.

You can read it to understand better what has changed.

## Tests¶

Make sure you have [tests](https://fastapi.tiangolo.com/tutorial/testing/) for your app and you run them on continuous integration (CI).

This way, you can do the upgrade and make sure everything is still working as expected.

## bump-pydantic¶

In many cases, when you use regular Pydantic models without customizations, you will be able to automate most of the process of migrating from Pydantic v1 to Pydantic v2.

You can use [bump-pydantic](https://github.com/pydantic/bump-pydantic) from the same Pydantic team.

This tool will help you to automatically change most of the code that needs to be changed.

After this, you can run the tests and check if everything works. If it does, you are done. 😎

## Pydantic v1 in v2¶

Pydantic v2 includes everything from Pydantic v1 as a submodule `pydantic.v1`. But this is no longer supported in versions above Python 3.13.

This means that you can install the latest version of Pydantic v2 and import and use the old Pydantic v1 components from this submodule, as if you had the old Pydantic v1 installed.

 [Python 3.10+](#__tabbed_1_1)

```
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    size: float
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float
```

### FastAPI support for Pydantic v1 in v2¶

Since FastAPI 0.119.0, there's also partial support for Pydantic v1 from inside of Pydantic v2, to facilitate the migration to v2.

So, you could upgrade Pydantic to the latest version 2, and change the imports to use the `pydantic.v1` submodule, and in many cases it would just work.

 [Python 3.10+](#__tabbed_3_1)

```
from fastapi import FastAPI
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    size: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
```

Warning

Have in mind that as the Pydantic team no longer supports Pydantic v1 in recent versions of Python, starting from Python 3.14, using `pydantic.v1` is also not supported in Python 3.14 and above.

### Pydantic v1 and v2 on the same app¶

It's **not supported** by Pydantic to have a model of Pydantic v2 with its own fields defined as Pydantic v1 models or vice versa.

...but, you can have separated models using Pydantic v1 and v2 in the same app.

In some cases, it's even possible to have both Pydantic v1 and v2 models in the same **path operation** in your FastAPI app:

 [Python 3.10+](#__tabbed_5_1)

```
from fastapi import FastAPI
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    size: float

class ItemV2(BaseModelV2):
    name: str
    description: str | None = None
    size: float

app = FastAPI()

@app.post("/items/", response_model=ItemV2)
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float

class ItemV2(BaseModelV2):
    name: str
    description: Union[str, None] = None
    size: float

app = FastAPI()

@app.post("/items/", response_model=ItemV2)
async def create_item(item: Item):
    return item
```

In this example above, the input model is a Pydantic v1 model, and the output model (defined in `response_model=ItemV2`) is a Pydantic v2 model.

### Pydantic v1 parameters¶

If you need to use some of the FastAPI-specific tools for parameters like `Body`, `Query`, `Form`, etc. with Pydantic v1 models, you can import them from `fastapi.temp_pydantic_v1_params` while you finish the migration to Pydantic v2:

 [Python 3.10+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import FastAPI
from fastapi.temp_pydantic_v1_params import Body
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    size: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Annotated[Item, Body(embed=True)]) -> Item:
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)

```
from typing import Annotated, Union

from fastapi import FastAPI
from fastapi.temp_pydantic_v1_params import Body
from pydantic.v1 import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Annotated[Item, Body(embed=True)]) -> Item:
    return item
```

### Migrate in steps¶

Tip

First try with `bump-pydantic`, if your tests pass and that works, then you're done in one command. ✨

If `bump-pydantic` doesn't work for your use case, you can use the support for both Pydantic v1 and v2 models in the same app to do the migration to Pydantic v2 gradually.

You could fist upgrade Pydantic to use the latest version 2, and change the imports to use `pydantic.v1` for all your models.

Then, you can start migrating your models from Pydantic v1 to v2 in groups, in gradual steps. 🚶

---

# Separate OpenAPI Schemas for Input and Output or Not¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Separate OpenAPI Schemas for Input and Output or Not¶

Since **Pydantic v2** was released, the generated OpenAPI is a bit more exact and **correct** than before. 😎

In fact, in some cases, it will even have **two JSON Schemas** in OpenAPI for the same Pydantic model, for input and output, depending on if they have **default values**.

Let's see how that works and how to change it if you need to do that.

## Pydantic Models for Input and Output¶

Let's say you have a Pydantic model with default values, like this one:

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

# Code below omitted 👇
```

     👀 Full file preview [Python 3.10+](#__tabbed_2_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

      🤓 Other versions and variants [Python 3.9+](#__tabbed_3_1)

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

### Model for Input¶

If you use this model as an input like here:

 [Python 3.10+](#__tabbed_4_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

# Code below omitted 👇
```

     👀 Full file preview [Python 3.10+](#__tabbed_5_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

      🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

...then the `description` field will **not be required**. Because it has a default value of `None`.

### Input Model in Docs¶

You can confirm that in the docs, the `description` field doesn't have a **red asterisk**, it's not marked as required:

  ![image](https://fastapi.tiangolo.com/img/tutorial/separate-openapi-schemas/image01.png)

### Model for Output¶

But if you use the same model as an output, like here:

 [Python 3.10+](#__tabbed_7_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

...then because `description` has a default value, if you **don't return anything** for that field, it will still have that **default value**.

### Model for Output Response Data¶

If you interact with the docs and check the response, even though the code didn't add anything in one of the `description` fields, the JSON response contains the default value (`null`):

  ![image](https://fastapi.tiangolo.com/img/tutorial/separate-openapi-schemas/image02.png)

This means that it will **always have a value**, it's just that sometimes the value could be `None` (or `null` in JSON).

That means that, clients using your API don't have to check if the value exists or not, they can **assume the field will always be there**, but just that in some cases it will have the default value of `None`.

The way to describe this in OpenAPI, is to mark that field as **required**, because it will always be there.

Because of that, the JSON Schema for a model can be different depending on if it's used for **input or output**:

- for **input** the `description` will **not be required**
- for **output** it will be **required** (and possibly `None`, or in JSON terms, `null`)

### Model for Output in Docs¶

You can check the output model in the docs too, **both** `name` and `description` are marked as **required** with a **red asterisk**:

  ![image](https://fastapi.tiangolo.com/img/tutorial/separate-openapi-schemas/image03.png)

### Model for Input and Output in Docs¶

And if you check all the available Schemas (JSON Schemas) in OpenAPI, you will see that there are two, one `Item-Input` and one `Item-Output`.

For `Item-Input`, `description` is **not required**, it doesn't have a red asterisk.

But for `Item-Output`, `description` is **required**, it has a red asterisk.

  ![image](https://fastapi.tiangolo.com/img/tutorial/separate-openapi-schemas/image04.png)

With this feature from **Pydantic v2**, your API documentation is more **precise**, and if you have autogenerated clients and SDKs, they will be more precise too, with a better **developer experience** and consistency. 🎉

## Do not Separate Schemas¶

Now, there are some cases where you might want to have the **same schema for input and output**.

Probably the main use case for this is if you already have some autogenerated client code/SDKs and you don't want to update all the autogenerated client code/SDKs yet, you probably will want to do it at some point, but maybe not right now.

In that case, you can disable this feature in **FastAPI**, with the parameter `separate_input_output_schemas=False`.

Info

Support for `separate_input_output_schemas` was added in FastAPI `0.102.0`. 🤓

  [Python 3.10+](#__tabbed_9_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI(separate_input_output_schemas=False)

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)

```
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None

app = FastAPI(separate_input_output_schemas=False)

@app.post("/items/")
def create_item(item: Item):
    return item

@app.get("/items/")
def read_items() -> list[Item]:
    return [
        Item(
            name="Portal Gun",
            description="Device to travel through the multi-rick-verse",
        ),
        Item(name="Plumbus"),
    ]
```

### Same Schema for Input and Output Models in Docs¶

And now there will be one single schema for input and output for the model, only `Item`, and it will have `description` as **not required**:

  ![image](https://fastapi.tiangolo.com/img/tutorial/separate-openapi-schemas/image05.png)

---

# Testing a Database¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Testing a Database¶

You can study about databases, SQL, and SQLModel in the [SQLModel docs](https://sqlmodel.tiangolo.com/). 🤓

There's a mini [tutorial on using SQLModel with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/). ✨

That tutorial includes a section about [testing SQL databases](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/). 😎
