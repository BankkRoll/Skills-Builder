# Lifespan Events¶ and more

# Lifespan Events¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Lifespan Events¶

You can define logic (code) that should be executed before the application **starts up**. This means that this code will be executed **once**, **before** the application **starts receiving requests**.

The same way, you can define logic (code) that should be executed when the application is **shutting down**. In this case, this code will be executed **once**, **after** having handled possibly **many requests**.

Because this code is executed before the application **starts** taking requests, and right after it **finishes** handling requests, it covers the whole application **lifespan** (the word "lifespan" will be important in a second 😉).

This can be very useful for setting up **resources** that you need to use for the whole app, and that are **shared** among requests, and/or that you need to **clean up** afterwards. For example, a database connection pool, or loading a shared machine learning model.

## Use Case¶

Let's start with an example **use case** and then see how to solve it with this.

Let's imagine that you have some **machine learning models** that you want to use to handle requests. 🤖

The same models are shared among requests, so, it's not one model per request, or one per user or something similar.

Let's imagine that loading the model can **take quite some time**, because it has to read a lot of **data from disk**. So you don't want to do it for every request.

You could load it at the top level of the module/file, but that would also mean that it would **load the model** even if you are just running a simple automated test, then that test would be **slow** because it would have to wait for the model to load before being able to run an independent part of the code.

That's what we'll solve, let's load the model before the requests are handled, but only right before the application starts receiving requests, not while  the code is being loaded.

## Lifespan¶

You can define this *startup* and *shutdown* logic using the `lifespan` parameter of the `FastAPI` app, and a "context manager" (I'll show you what that is in a second).

Let's start with an example and then see it in detail.

We create an async function `lifespan()` with `yield` like this:

 [Python 3.9+](#__tabbed_1_1)

```
from contextlib import asynccontextmanager

from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

Here we are simulating the expensive *startup* operation of loading the model by putting the (fake) model function in the dictionary with machine learning models before the `yield`. This code will be executed **before** the application **starts taking requests**, during the *startup*.

And then, right after the `yield`, we unload the model. This code will be executed **after** the application **finishes handling requests**, right before the *shutdown*. This could, for example, release resources like memory or a GPU.

Tip

The `shutdown` would happen when you are **stopping** the application.

Maybe you need to start a new version, or you just got tired of running it. 🤷

### Lifespan function¶

The first thing to notice, is that we are defining an async function with `yield`. This is very similar to Dependencies with `yield`.

 [Python 3.9+](#__tabbed_2_1)

```
from contextlib import asynccontextmanager

from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

The first part of the function, before the `yield`, will be executed **before** the application starts.

And the part after the `yield` will be executed **after** the application has finished.

### Async Context Manager¶

If you check, the function is decorated with an `@asynccontextmanager`.

That converts the function into something called an "**async context manager**".

 [Python 3.9+](#__tabbed_3_1)

```
from contextlib import asynccontextmanager

from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

A **context manager** in Python is something that you can use in a `with` statement, for example, `open()` can be used as a context manager:

```
with open("file.txt") as file:
    file.read()
```

In recent versions of Python, there's also an **async context manager**. You would use it with `async with`:

```
async with lifespan(app):
    await do_stuff()
```

When you create a context manager or an async context manager like above, what it does is that, before entering the `with` block, it will execute the code before the `yield`, and after exiting the `with` block, it will execute the code after the `yield`.

In our code example above, we don't use it directly, but we pass it to FastAPI for it to use it.

The `lifespan` parameter of the `FastAPI` app takes an **async context manager**, so we can pass our new `lifespan` async context manager to it.

 [Python 3.9+](#__tabbed_4_1)

```
from contextlib import asynccontextmanager

from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

## Alternative Events (deprecated)¶

Warning

The recommended way to handle the *startup* and *shutdown* is using the `lifespan` parameter of the `FastAPI` app as described above. If you provide a `lifespan` parameter, `startup` and `shutdown` event handlers will no longer be called. It's all `lifespan` or all events, not both.

You can probably skip this part.

There's an alternative way to define this logic to be executed during *startup* and during *shutdown*.

You can define event handlers (functions) that need to be executed before the application starts up, or when the application is shutting down.

These functions can be declared with `async def` or normal `def`.

### startupevent¶

To add a function that should be run before the application starts, declare it with the event `"startup"`:

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI

app = FastAPI()

items = {}

@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]
```

In this case, the `startup` event handler function will initialize the items "database" (just a `dict`) with some values.

You can add more than one event handler function.

And your application won't start receiving requests until all the `startup` event handlers have completed.

### shutdownevent¶

To add a function that should be run when the application is shutting down, declare it with the event `"shutdown"`:

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
```

Here, the `shutdown` event handler function will write a text line `"Application shutdown"` to a file `log.txt`.

Info

In the `open()` function, the `mode="a"` means "append", so, the line will be added after whatever is on that file, without overwriting the previous contents.

Tip

Notice that in this case we are using a standard Python `open()` function that interacts with a file.

So, it involves I/O (input/output), that requires "waiting" for things to be written to disk.

But `open()` doesn't use `async` and `await`.

So, we declare the event handler function with standard `def` instead of `async def`.

### startupandshutdowntogether¶

There's a high chance that the logic for your *startup* and *shutdown* is connected, you might want to start something and then finish it, acquire a resource and then release it, etc.

Doing that in separated functions that don't share logic or variables together is more difficult as you would need to store values in global variables or similar tricks.

Because of that, it's now recommended to instead use the `lifespan` as explained above.

## Technical Details¶

Just a technical detail for the curious nerds. 🤓

Underneath, in the ASGI technical specification, this is part of the [Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html), and it defines events called `startup` and `shutdown`.

Info

You can read more about the Starlette `lifespan` handlers in [Starlette's  Lifespan' docs](https://www.starlette.dev/lifespan/).

Including how to handle lifespan state that can be used in other areas of your code.

## Sub Applications¶

🚨 Keep in mind that these lifespan events (startup and shutdown) will only be executed for the main application, not for [Sub Applications - Mounts](https://fastapi.tiangolo.com/advanced/sub-applications/).

---

# Generating SDKs¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Generating SDKs¶

Because **FastAPI** is based on the **OpenAPI** specification, its APIs can be described in a standard format that many tools understand.

This makes it easy to generate up-to-date **documentation**, client libraries (**SDKs**) in multiple languages, and **testing** or **automation workflows** that stay in sync with your code.

In this guide, you'll learn how to generate a **TypeScript SDK** for your FastAPI backend.

## Open Source SDK Generators¶

A versatile option is the [OpenAPI Generator](https://openapi-generator.tech/), which supports **many programming languages** and can generate SDKs from your OpenAPI specification.

For **TypeScript clients**, [Hey API](https://heyapi.dev/) is a purpose-built solution, providing an optimized experience for the TypeScript ecosystem.

You can discover more SDK generators on [OpenAPI.Tools](https://openapi.tools/#sdk).

Tip

FastAPI automatically generates **OpenAPI 3.1** specifications, so any tool you use must support this version.

## SDK Generators from FastAPI Sponsors¶

This section highlights **venture-backed** and **company-supported** solutions from companies that sponsor FastAPI. These products provide **additional features** and **integrations** on top of high-quality generated SDKs.

By ✨ [sponsoring FastAPI](https://fastapi.tiangolo.com/help-fastapi/#sponsor-the-author) ✨, these companies help ensure the framework and its **ecosystem** remain healthy and **sustainable**.

Their sponsorship also demonstrates a strong commitment to the FastAPI **community** (you), showing that they care not only about offering a **great service** but also about supporting a **robust and thriving framework**, FastAPI. 🙇

For example, you might want to try:

- [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
- [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
- [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

Some of these solutions may also be open source or offer free tiers, so you can try them without a financial commitment. Other commercial SDK generators are available and can be found online. 🤓

## Create a TypeScript SDK¶

Let's start with a simple FastAPI application:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class ResponseMessage(BaseModel):
    message: str

@app.post("/items/", response_model=ResponseMessage)
async def create_item(item: Item):
    return {"message": "item received"}

@app.get("/items/", response_model=list[Item])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]
```

Notice that the *path operations* define the models they use for request payload and response payload, using the models `Item` and `ResponseMessage`.

### API Docs¶

If you go to `/docs`, you will see that it has the **schemas** for the data to be sent in requests and received in responses:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image01.png)

You can see those schemas because they were declared with the models in the app.

That information is available in the app's **OpenAPI schema**, and then shown in the API docs.

That same information from the models that is included in OpenAPI is what can be used to **generate the client code**.

### Hey API¶

Once we have a FastAPI app with the models, we can use Hey API to generate a TypeScript client. The fastest way to do that is via npx.

```
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

This will generate a TypeScript SDK in `./src/client`.

You can learn how to [install@hey-api/openapi-ts](https://heyapi.dev/openapi-ts/get-started) and read about the [generated output](https://heyapi.dev/openapi-ts/output) on their website.

### Using the SDK¶

Now you can import and use the client code. It could look like this, notice that you get autocompletion for the methods:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image02.png)

You will also get autocompletion for the payload to send:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image03.png)

Tip

Notice the autocompletion for `name` and `price`, that was defined in the FastAPI application, in the `Item` model.

You will have inline errors for the data that you send:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image04.png)

The response object will also have autocompletion:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image05.png)

## FastAPI App with Tags¶

In many cases, your FastAPI app will be bigger, and you will probably use tags to separate different groups of *path operations*.

For example, you could have a section for **items** and another section for **users**, and they could be separated by tags:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

class ResponseMessage(BaseModel):
    message: str

class User(BaseModel):
    username: str
    email: str

@app.post("/items/", response_model=ResponseMessage, tags=["items"])
async def create_item(item: Item):
    return {"message": "Item received"}

@app.get("/items/", response_model=list[Item], tags=["items"])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]

@app.post("/users/", response_model=ResponseMessage, tags=["users"])
async def create_user(user: User):
    return {"message": "User received"}
```

### Generate a TypeScript Client with Tags¶

If you generate a client for a FastAPI app using tags, it will normally also separate the client code based on the tags.

This way, you will be able to have things ordered and grouped correctly for the client code:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image06.png)

In this case, you have:

- `ItemsService`
- `UsersService`

### Client Method Names¶

Right now, the generated method names like `createItemItemsPost` don't look very clean:

```
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...that's because the client generator uses the OpenAPI internal **operation ID** for each *path operation*.

OpenAPI requires that each operation ID is unique across all the *path operations*, so FastAPI uses the **function name**, the **path**, and the **HTTP method/operation** to generate that operation ID, because that way it can make sure that the operation IDs are unique.

But I'll show you how to improve that next. 🤓

## Custom Operation IDs and Better Method Names¶

You can **modify** the way these operation IDs are **generated** to make them simpler and have **simpler method names** in the clients.

In this case, you will have to ensure that each operation ID is **unique** in some other way.

For example, you could make sure that each *path operation* has a tag, and then generate the operation ID based on the **tag** and the *path operation* **name** (the function name).

### Custom Generate Unique ID Function¶

FastAPI uses a **unique ID** for each *path operation*, which is used for the **operation ID** and also for the names of any needed custom models, for requests or responses.

You can customize that function. It takes an `APIRoute` and outputs a string.

For example, here it is using the first tag (you will probably have only one tag) and the *path operation* name (the function name).

You can then pass that custom function to **FastAPI** as the `generate_unique_id_function` parameter:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

class Item(BaseModel):
    name: str
    price: float

class ResponseMessage(BaseModel):
    message: str

class User(BaseModel):
    username: str
    email: str

@app.post("/items/", response_model=ResponseMessage, tags=["items"])
async def create_item(item: Item):
    return {"message": "Item received"}

@app.get("/items/", response_model=list[Item], tags=["items"])
async def get_items():
    return [
        {"name": "Plumbus", "price": 3},
        {"name": "Portal Gun", "price": 9001},
    ]

@app.post("/users/", response_model=ResponseMessage, tags=["users"])
async def create_user(user: User):
    return {"message": "User received"}
```

### Generate a TypeScript Client with Custom Operation IDs¶

Now, if you generate the client again, you will see that it has the improved method names:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image07.png)

As you see, the method names now have the tag and then the function name, now they don't include information from the URL path and the HTTP operation.

### Preprocess the OpenAPI Specification for the Client Generator¶

The generated code still has some **duplicated information**.

We already know that this method is related to the **items** because that word is in the `ItemsService` (taken from the tag), but we still have the tag name prefixed in the method name too. 😕

We will probably still want to keep it for OpenAPI in general, as that will ensure that the operation IDs are **unique**.

But for the generated client, we could **modify** the OpenAPI operation IDs right before generating the clients, just to make those method names nicer and **cleaner**.

We could download the OpenAPI JSON to a file `openapi.json` and then we could **remove that prefixed tag** with a script like this:

 [Python 3.9+](#__tabbed_4_1)[Node.js](#__tabbed_4_2)

```
import json
from pathlib import Path

file_path = Path("./openapi.json")
openapi_content = json.loads(file_path.read_text())

for path_data in openapi_content["paths"].values():
    for operation in path_data.values():
        tag = operation["tags"][0]
        operation_id = operation["operationId"]
        to_remove = f"{tag}-"
        new_operation_id = operation_id[len(to_remove) :]
        operation["operationId"] = new_operation_id

file_path.write_text(json.dumps(openapi_content))
```

```
import * as fs from 'fs'

async function modifyOpenAPIFile(filePath) {
  try {
    const data = await fs.promises.readFile(filePath)
    const openapiContent = JSON.parse(data)

    const paths = openapiContent.paths
    for (const pathKey of Object.keys(paths)) {
      const pathData = paths[pathKey]
      for (const method of Object.keys(pathData)) {
        const operation = pathData[method]
        if (operation.tags && operation.tags.length > 0) {
          const tag = operation.tags[0]
          const operationId = operation.operationId
          const toRemove = `${tag}-`
          if (operationId.startsWith(toRemove)) {
            const newOperationId = operationId.substring(toRemove.length)
            operation.operationId = newOperationId
          }
        }
      }
    }

    await fs.promises.writeFile(
      filePath,
      JSON.stringify(openapiContent, null, 2),
    )
    console.log('File successfully modified')
  } catch (err) {
    console.error('Error:', err)
  }
}

const filePath = './openapi.json'
modifyOpenAPIFile(filePath)
```

With that, the operation IDs would be renamed from things like `items-get_items` to just `get_items`, that way the client generator can generate simpler method names.

### Generate a TypeScript Client with the Preprocessed OpenAPI¶

Since the end result is now in an `openapi.json` file, you need to update your input location:

```
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

After generating the new client, you would now have **clean method names**, with all the **autocompletion**, **inline errors**, etc:

![image](https://fastapi.tiangolo.com/img/tutorial/generate-clients/image08.png)

## Benefits¶

When using the automatically generated clients, you would get **autocompletion** for:

- Methods.
- Request payloads in the body, query parameters, etc.
- Response payloads.

You would also have **inline errors** for everything.

And whenever you update the backend code, and **regenerate** the frontend, it would have any new *path operations* available as methods, the old ones removed, and any other change would be reflected on the generated code. 🤓

This also means that if something changed, it will be **reflected** on the client code automatically. And if you **build** the client, it will error out if you have any **mismatch** in the data used.

So, you would **detect many errors** very early in the development cycle instead of having to wait for the errors to show up to your final users in production and then trying to debug where the problem is. ✨

---

# Advanced Middleware¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Advanced Middleware¶

In the main tutorial you read how to add [Custom Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) to your application.

And then you also read how to handle [CORS with theCORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/).

In this section we'll see how to use other middlewares.

## Adding ASGI middlewares¶

As **FastAPI** is based on Starlette and implements the ASGI specification, you can use any ASGI middleware.

A middleware doesn't have to be made for FastAPI or Starlette to work, as long as it follows the ASGI spec.

In general, ASGI middlewares are classes that expect to receive an ASGI app as the first argument.

So, in the documentation for third-party ASGI middlewares they will probably tell you to do something like:

```
from unicorn import UnicornMiddleware

app = SomeASGIApp()

new_app = UnicornMiddleware(app, some_config="rainbow")
```

But FastAPI (actually Starlette) provides a simpler way to do it that makes sure that the internal middlewares handle server errors and custom exception handlers work properly.

For that, you use `app.add_middleware()` (as in the example for CORS).

```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

`app.add_middleware()` receives a middleware class as the first argument and any additional arguments to be passed to the middleware.

## Integrated middlewares¶

**FastAPI** includes several middlewares for common use cases, we'll see next how to use them.

Technical Details

For the next examples, you could also use `from starlette.middleware.something import SomethingMiddleware`.

**FastAPI** provides several middlewares in `fastapi.middleware` just as a convenience for you, the developer. But most of the available middlewares come directly from Starlette.

## HTTPSRedirectMiddleware¶

Enforces that all incoming requests must either be `https` or `wss`.

Any incoming request to `http` or `ws` will be redirected to the secure scheme instead.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

## TrustedHostMiddleware¶

Enforces that all incoming requests have a correctly set `Host` header, in order to guard against HTTP Host Header attacks.

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

The following arguments are supported:

- `allowed_hosts` - A list of domain names that should be allowed as hostnames. Wildcard domains such as `*.example.com` are supported for matching subdomains. To allow any hostname either use `allowed_hosts=["*"]` or omit the middleware.
- `www_redirect` - If set to True, requests to non-www versions of the allowed hosts will be redirected to their www counterparts. Defaults to `True`.

If an incoming request does not validate correctly then a `400` response will be sent.

## GZipMiddleware¶

Handles GZip responses for any request that includes `"gzip"` in the `Accept-Encoding` header.

The middleware will handle both standard and streaming responses.

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

@app.get("/")
async def main():
    return "somebigcontent"
```

The following arguments are supported:

- `minimum_size` - Do not GZip responses that are smaller than this minimum size in bytes. Defaults to `500`.
- `compresslevel` - Used during GZip compression. It is an integer ranging from 1 to 9. Defaults to `9`. Lower value results in faster compression but larger file sizes, while higher value results in slower compression but smaller file sizes.

## Other middlewares¶

There are many other ASGI middlewares.

For example:

- [Uvicorn'sProxyHeadersMiddleware](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)
- [MessagePack](https://github.com/florimondmanca/msgpack-asgi)

To see other available middlewares check [Starlette's Middleware docs](https://www.starlette.dev/middleware/) and the [ASGI Awesome List](https://github.com/florimondmanca/awesome-asgi).

---

# OpenAPI Callbacks¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# OpenAPI Callbacks¶

You could create an API with a *path operation* that could trigger a request to an *external API* created by someone else (probably the same developer that would be *using* your API).

The process that happens when your API app calls the *external API* is named a "callback". Because the software that the external developer wrote sends a request to your API and then your API *calls back*, sending a request to an *external API* (that was probably created by the same developer).

In this case, you could want to document how that external API *should* look like. What *path operation* it should have, what body it should expect, what response it should return, etc.

## An app with callbacks¶

Let's see all this with an example.

Imagine you develop an app that allows creating invoices.

These invoices will have an `id`, `title` (optional), `customer`, and `total`.

The user of your API (an external developer) will create an invoice in your API with a POST request.

Then your API will (let's imagine):

- Send the invoice to some customer of the external developer.
- Collect the money.
- Send a notification back to the API user (the external developer).
  - This will be done by sending a POST request (from *your API*) to some *external API* provided by that external developer (this is the "callback").

## The normalFastAPIapp¶

Let's first see how the normal API app would look like before adding the callback.

It will have a *path operation* that will receive an `Invoice` body, and a query parameter `callback_url` that will contain the URL for the callback.

This part is pretty normal, most of the code is probably already familiar to you:

 [Python 3.10+](#__tabbed_1_1)

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

Tip

The `callback_url` query parameter uses a Pydantic [Url](https://docs.pydantic.dev/latest/api/networks/) type.

The only new thing is the `callbacks=invoices_callback_router.routes` as an argument to the *path operation decorator*. We'll see what that is next.

## Documenting the callback¶

The actual callback code will depend heavily on your own API app.

And it will probably vary a lot from one app to the next.

It could be just one or two lines of code, like:

```
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

But possibly the most important part of the callback is making sure that your API user (the external developer) implements the *external API* correctly, according to the data that *your API* is going to send in the request body of the callback, etc.

So, what we will do next is add the code to document how that *external API* should look like to receive the callback from *your API*.

That documentation will show up in the Swagger UI at `/docs` in your API, and it will let external developers know how to build the *external API*.

This example doesn't implement the callback itself (that could be just a line of code), only the documentation part.

Tip

The actual callback is just an HTTP request.

When implementing the callback yourself, you could use something like [HTTPX](https://www.python-httpx.org) or [Requests](https://requests.readthedocs.io/).

## Write the callback documentation code¶

This code won't be executed in your app, we only need it to *document* how that *external API* should look like.

But, you already know how to easily create automatic documentation for an API with **FastAPI**.

So we are going to use that same knowledge to document how the *external API* should look like... by creating the *path operation(s)* that the external API should implement (the ones your API will call).

Tip

When writing the code to document a callback, it might be useful to imagine that you are that *external developer*. And that you are currently implementing the *external API*, not *your API*.

Temporarily adopting this point of view (of the *external developer*) can help you feel like it's more obvious where to put the parameters, the Pydantic model for the body, for the response, etc. for that *external API*.

### Create a callbackAPIRouter¶

First create a new `APIRouter` that will contain one or more callbacks.

 [Python 3.10+](#__tabbed_3_1)

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

### Create the callbackpath operation¶

To create the callback *path operation* use the same `APIRouter` you created above.

It should look just like a normal FastAPI *path operation*:

- It should probably have a declaration of the body it should receive, e.g. `body: InvoiceEvent`.
- And it could also have a declaration of the response it should return, e.g. `response_model=InvoiceEventReceived`.

 [Python 3.10+](#__tabbed_5_1)

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

There are 2 main differences from a normal *path operation*:

- It doesn't need to have any actual code, because your app will never call this code. It's only used to document the *external API*. So, the function could just have `pass`.
- The *path* can contain an [OpenAPI 3 expression](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression) (see more below) where it can use variables with parameters and parts of the original request sent to *your API*.

### The callback path expression¶

The callback *path* can have an [OpenAPI 3 expression](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression) that can contain parts of the original request sent to *your API*.

In this case, it's the `str`:

```
"{$callback_url}/invoices/{$request.body.id}"
```

So, if your API user (the external developer) sends a request to *your API* to:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

with a JSON body of:

```
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

then *your API* will process the invoice, and at some point later, send a callback request to the `callback_url` (the *external API*):

```
https://www.external.org/events/invoices/2expen51ve
```

with a JSON body containing something like:

```
{
    "description": "Payment celebration",
    "paid": true
}
```

and it would expect a response from that *external API* with a JSON body like:

```
{
    "ok": true
}
```

Tip

Notice how the callback URL used contains the URL received as a query parameter in `callback_url` (`https://www.external.org/events`) and also the invoice `id` from inside of the JSON body (`2expen51ve`).

### Add the callback router¶

At this point you have the *callback path operation(s)* needed (the one(s) that the *external developer*  should implement in the *external API*) in the callback router you created above.

Now use the parameter `callbacks` in *your API's path operation decorator* to pass the attribute `.routes` (that's actually just a `list` of routes/*path operations*) from that callback router:

 [Python 3.10+](#__tabbed_7_1)

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: str | None = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: HttpUrl | None = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)

```
from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Invoice(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float

class InvoiceEvent(BaseModel):
    description: str
    paid: bool

class InvoiceEventReceived(BaseModel):
    ok: bool

invoices_callback_router = APIRouter()

@invoices_callback_router.post(
    "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass

@app.post("/invoices/", callbacks=invoices_callback_router.routes)
def create_invoice(invoice: Invoice, callback_url: Union[HttpUrl, None] = None):
    """
    Create an invoice.

    This will (let's imagine) let the API user (some external developer) create an
    invoice.

    And this path operation will:

    * Send the invoice to the client.
    * Collect the money from the client.
    * Send a notification back to the API user (the external developer), as a callback.
        * At this point is that the API will somehow send a POST request to the
            external API with the notification of the invoice event
            (e.g. "payment successful").
    """
    # Send the invoice, collect the money, send the notification (the callback)
    return {"msg": "Invoice received"}
```

Tip

Notice that you are not passing the router itself (`invoices_callback_router`) to `callback=`, but the attribute `.routes`, as in `invoices_callback_router.routes`.

### Check the docs¶

Now you can start your app and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see your docs including a "Callbacks" section for your *path operation* that shows how the *external API* should look like:

![image](https://fastapi.tiangolo.com/img/tutorial/openapi-callbacks/image01.png)
