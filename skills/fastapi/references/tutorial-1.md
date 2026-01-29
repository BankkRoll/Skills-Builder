# Background Tasks¶ and more

# Background Tasks¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Background Tasks¶

You can define background tasks to be run *after* returning a response.

This is useful for operations that need to happen after a request, but that the client doesn't really have to be waiting for the operation to complete before receiving the response.

This includes, for example:

- Email notifications sent after performing an action:
  - As connecting to an email server and sending an email tends to be "slow" (several seconds), you can return the response right away and send the email notification in the background.
- Processing data:
  - For example, let's say you receive a file that must go through a slow process, you can return a response of "Accepted" (HTTP 202) and process the file in the background.

## UsingBackgroundTasks¶

First, import `BackgroundTasks` and define a parameter in your *path operation function* with a type declaration of `BackgroundTasks`:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

**FastAPI** will create the object of type `BackgroundTasks` for you and pass it as that parameter.

## Create a task function¶

Create a function to be run as the background task.

It is just a standard function that can receive parameters.

It can be an `async def` or normal `def` function, **FastAPI** will know how to handle it correctly.

In this case, the task function will write to a file (simulating sending an email).

And as the write operation doesn't use `async` and `await`, we define the function with normal `def`:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

## Add the background task¶

Inside of your *path operation function*, pass your task function to the *background tasks* object with the method `.add_task()`:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

`.add_task()` receives as arguments:

- A task function to be run in the background (`write_notification`).
- Any sequence of arguments that should be passed to the task function in order (`email`).
- Any keyword arguments that should be passed to the task function (`message="some notification"`).

## Dependency Injection¶

Using `BackgroundTasks` also works with the dependency injection system, you can declare a parameter of type `BackgroundTasks` at multiple levels: in a *path operation function*, in a dependency (dependable), in a sub-dependency, etc.

**FastAPI** knows what to do in each case and how to reuse the same object, so that all the background tasks are merged together and are run in the background afterwards:

 [Python 3.10+](#__tabbed_4_1)

```
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_5_1)[Python 3.10+ - non-Annotated](#__tabbed_5_2)[Python 3.9+ - non-Annotated](#__tabbed_5_3)

```
from typing import Annotated, Union

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
```

In this example, the messages will be written to the `log.txt` file *after* the response is sent.

If there was a query in the request, it will be written to the log in a background task.

And then another background task generated at the *path operation function* will write a message using the `email` path parameter.

## Technical Details¶

The class `BackgroundTasks` comes directly from [starlette.background](https://www.starlette.dev/background/).

It is imported/included directly into FastAPI so that you can import it from `fastapi` and avoid accidentally importing the alternative `BackgroundTask` (without the `s` at the end) from `starlette.background`.

By only using `BackgroundTasks` (and not `BackgroundTask`), it's then possible to use it as a *path operation function* parameter and have **FastAPI** handle the rest for you, just like when using the `Request` object directly.

It's still possible to use `BackgroundTask` alone in FastAPI, but you have to create the object in your code and return a Starlette `Response` including it.

You can see more details in [Starlette's official docs for Background Tasks](https://www.starlette.dev/background/).

## Caveat¶

If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like [Celery](https://docs.celeryq.dev).

They tend to require more complex configurations, a message/job queue manager, like RabbitMQ or Redis, but they allow you to run background tasks in multiple processes, and especially, in multiple servers.

But if you need to access variables and objects from the same **FastAPI** app, or you need to perform small background tasks (like sending an email notification), you can simply just use `BackgroundTasks`.

## Recap¶

Import and use `BackgroundTasks` with parameters in *path operation functions* and dependencies to add background tasks.

---

# Bigger Applications

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Bigger Applications - Multiple Files¶

If you are building an application or a web API, it's rarely the case that you can put everything in a single file.

**FastAPI** provides a convenience tool to structure your application while keeping all the flexibility.

Info

If you come from Flask, this would be the equivalent of Flask's Blueprints.

## An example file structure¶

Let's say you have a file structure like this:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

Tip

There are several `__init__.py` files: one in each directory or subdirectory.

This is what allows importing code from one file into another.

For example, in `app/main.py` you could have a line like:

```
from app.routers import items
```

- The `app` directory contains everything. And it has an empty file `app/__init__.py`, so it is a "Python package" (a collection of "Python modules"): `app`.
- It contains an `app/main.py` file. As it is inside a Python package (a directory with a file `__init__.py`), it is a "module" of that package: `app.main`.
- There's also an `app/dependencies.py` file, just like `app/main.py`, it is a "module": `app.dependencies`.
- There's a subdirectory `app/routers/` with another file `__init__.py`, so it's a "Python subpackage": `app.routers`.
- The file `app/routers/items.py` is inside a package, `app/routers/`, so, it's a submodule: `app.routers.items`.
- The same with `app/routers/users.py`, it's another submodule: `app.routers.users`.
- There's also a subdirectory `app/internal/` with another file `__init__.py`, so it's another "Python subpackage": `app.internal`.
- And the file `app/internal/admin.py` is another submodule: `app.internal.admin`.

![image](https://fastapi.tiangolo.com/img/tutorial/bigger-applications/package.drawio.svg)

The same file structure with comments:

```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
```

## APIRouter¶

Let's say the file dedicated to handling just users is the submodule at `/app/routers/users.py`.

You want to have the *path operations* related to your users separated from the rest of the code, to keep it organized.

But it's still part of the same **FastAPI** application/web API (it's part of the same "Python Package").

You can create the *path operations* for that module using `APIRouter`.

### ImportAPIRouter¶

You import it and create an "instance" the same way you would with the class `FastAPI`:

 [Python 3.8+](#__tabbed_1_1)   app/routers/users.py

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

### Path operationswithAPIRouter¶

And then you use it to declare your *path operations*.

Use it the same way you would use the `FastAPI` class:

 [Python 3.8+](#__tabbed_2_1)   app/routers/users.py

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

You can think of `APIRouter` as a "mini `FastAPI`" class.

All the same options are supported.

All the same `parameters`, `responses`, `dependencies`, `tags`, etc.

Tip

In this example, the variable is called `router`, but you can name it however you want.

We are going to include this `APIRouter` in the main `FastAPI` app, but first, let's check the dependencies and another `APIRouter`.

## Dependencies¶

We see that we are going to need some dependencies used in several places of the application.

So we put them in their own `dependencies` module (`app/dependencies.py`).

We will now use a simple dependency to read a custom `X-Token` header:

 [Python 3.9+](#__tabbed_3_1)   app/dependencies.py

```
from typing import Annotated

from fastapi import Header, HTTPException

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/dependencies.py

```
from fastapi import Header, HTTPException

async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
```

Tip

We are using an invented header to simplify this example.

But in real cases you will get better results using the integrated [Security utilities](https://fastapi.tiangolo.com/tutorial/security/).

## Another module withAPIRouter¶

Let's say you also have the endpoints dedicated to handling "items" from your application in the module at `app/routers/items.py`.

You have *path operations* for:

- `/items/`
- `/items/{item_id}`

It's all the same structure as with `app/routers/users.py`.

But we want to be smarter and simplify the code a bit.

We know all the *path operations* in this module have the same:

- Path `prefix`: `/items`.
- `tags`: (just one tag: `items`).
- Extra `responses`.
- `dependencies`: they all need that `X-Token` dependency we created.

So, instead of adding all that to each *path operation*, we can add it to the `APIRouter`.

 [Python 3.8+](#__tabbed_5_1)   app/routers/items.py

```
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
```

As the path of each *path operation* has to start with `/`, like in:

```
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...the prefix must not include a final `/`.

So, the prefix in this case is `/items`.

We can also add a list of `tags` and extra `responses` that will be applied to all the *path operations* included in this router.

And we can add a list of `dependencies` that will be added to all the *path operations* in the router and will be executed/solved for each request made to them.

Tip

Note that, much like [dependencies inpath operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/), no value will be passed to your *path operation function*.

The end result is that the item paths are now:

- `/items/`
- `/items/{item_id}`

...as we intended.

- They will be marked with a list of tags that contain a single string `"items"`.
  - These "tags" are especially useful for the automatic interactive documentation systems (using OpenAPI).
- All of them will include the predefined `responses`.
- All these *path operations* will have the list of `dependencies` evaluated/executed before them.
  - If you also declare dependencies in a specific *path operation*, **they will be executed too**.
  - The router dependencies are executed first, then the [dependenciesin the decorator](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/), and then the normal parameter dependencies.
  - You can also add [Securitydependencies withscopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).

Tip

Having `dependencies` in the `APIRouter` can be used, for example, to require authentication for a whole group of *path operations*. Even if the dependencies are not added individually to each one of them.

Check

The `prefix`, `tags`, `responses`, and `dependencies` parameters are (as in many other cases) just a feature from **FastAPI** to help you avoid code duplication.

### Import the dependencies¶

This code lives in the module `app.routers.items`, the file `app/routers/items.py`.

And we need to get the dependency function from the module `app.dependencies`, the file `app/dependencies.py`.

So we use a relative import with `..` for the dependencies:

 [Python 3.8+](#__tabbed_6_1)   app/routers/items.py

```
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
```

#### How relative imports work¶

Tip

If you know perfectly how imports work, continue to the next section below.

A single dot `.`, like in:

```
from .dependencies import get_token_header
```

would mean:

- Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
- find the module `dependencies` (an imaginary file at `app/routers/dependencies.py`)...
- and from it, import the function `get_token_header`.

But that file doesn't exist, our dependencies are in a file at `app/dependencies.py`.

Remember how our app/file structure looks like:

![image](https://fastapi.tiangolo.com/img/tutorial/bigger-applications/package.drawio.svg)

---

The two dots `..`, like in:

```
from ..dependencies import get_token_header
```

mean:

- Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
- go to the parent package (the directory `app/`)...
- and in there, find the module `dependencies` (the file at `app/dependencies.py`)...
- and from it, import the function `get_token_header`.

That works correctly! 🎉

---

The same way, if we had used three dots `...`, like in:

```
from ...dependencies import get_token_header
```

that would mean:

- Starting in the same package that this module (the file `app/routers/items.py`) lives in (the directory `app/routers/`)...
- go to the parent package (the directory `app/`)...
- then go to the parent of that package (there's no parent package, `app` is the top level 😱)...
- and in there, find the module `dependencies` (the file at `app/dependencies.py`)...
- and from it, import the function `get_token_header`.

That would refer to some package above `app/`, with its own file `__init__.py`, etc. But we don't have that. So, that would throw an error in our example. 🚨

But now you know how it works, so you can use relative imports in your own apps no matter how complex they are. 🤓

### Add some customtags,responses, anddependencies¶

We are not adding the prefix `/items` nor the `tags=["items"]` to each *path operation* because we added them to the `APIRouter`.

But we can still add *more* `tags` that will be applied to a specific *path operation*, and also some extra `responses` specific to that *path operation*:

 [Python 3.8+](#__tabbed_7_1)   app/routers/items.py

```
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
```

Tip

This last path operation will have the combination of tags: `["items", "custom"]`.

And it will also have both responses in the documentation, one for `404` and one for `403`.

## The mainFastAPI¶

Now, let's see the module at `app/main.py`.

Here's where you import and use the class `FastAPI`.

This will be the main file in your application that ties everything together.

And as most of your logic will now live in its own specific module, the main file will be quite simple.

### ImportFastAPI¶

You import and create a `FastAPI` class as normally.

And we can even declare [global dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/) that will be combined with the dependencies for each `APIRouter`:

 [Python 3.9+](#__tabbed_8_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_9_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

### Import theAPIRouter¶

Now we import the other submodules that have `APIRouter`s:

 [Python 3.9+](#__tabbed_10_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_11_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

As the files `app/routers/users.py` and `app/routers/items.py` are submodules that are part of the same Python package `app`, we can use a single dot `.` to import them using "relative imports".

### How the importing works¶

The section:

```
from .routers import items, users
```

means:

- Starting in the same package that this module (the file `app/main.py`) lives in (the directory `app/`)...
- look for the subpackage `routers` (the directory at `app/routers/`)...
- and from it, import the submodule `items` (the file at `app/routers/items.py`) and `users` (the file at `app/routers/users.py`)...

The module `items` will have a variable `router` (`items.router`). This is the same one we created in the file `app/routers/items.py`, it's an `APIRouter` object.

And then we do the same for the module `users`.

We could also import them like:

```
from app.routers import items, users
```

Info

The first version is a "relative import":

```
from .routers import items, users
```

The second version is an "absolute import":

```
from app.routers import items, users
```

To learn more about Python Packages and Modules, read [the official Python documentation about Modules](https://docs.python.org/3/tutorial/modules.html).

### Avoid name collisions¶

We are importing the submodule `items` directly, instead of importing just its variable `router`.

This is because we also have another variable named `router` in the submodule `users`.

If we had imported one after the other, like:

```
from .routers.items import router
from .routers.users import router
```

the `router` from `users` would overwrite the one from `items` and we wouldn't be able to use them at the same time.

So, to be able to use both of them in the same file, we import the submodules directly:

 [Python 3.9+](#__tabbed_12_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_13_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

### Include theAPIRouters forusersanditems¶

Now, let's include the `router`s from the submodules `users` and `items`:

 [Python 3.9+](#__tabbed_14_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_15_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

Info

`users.router` contains the `APIRouter` inside of the file `app/routers/users.py`.

And `items.router` contains the `APIRouter` inside of the file `app/routers/items.py`.

With `app.include_router()` we can add each `APIRouter` to the main `FastAPI` application.

It will include all the routes from that router as part of it.

Technical Details

It will actually internally create a *path operation* for each *path operation* that was declared in the `APIRouter`.

So, behind the scenes, it will actually work as if everything was the same single app.

Check

You don't have to worry about performance when including routers.

This will take microseconds and will only happen at startup.

So it won't affect performance. ⚡

### Include anAPIRouterwith a customprefix,tags,responses, anddependencies¶

Now, let's imagine your organization gave you the `app/internal/admin.py` file.

It contains an `APIRouter` with some admin *path operations* that your organization shares between several projects.

For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a `prefix`, `dependencies`, `tags`, etc. directly to the `APIRouter`:

 [Python 3.8+](#__tabbed_16_1)   app/internal/admin.py

```
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
```

But we still want to set a custom `prefix` when including the `APIRouter` so that all its *path operations* start with `/admin`, we want to secure it with the `dependencies` we already have for this project, and we want to include `tags` and `responses`.

We can declare all that without having to modify the original `APIRouter` by passing those parameters to `app.include_router()`:

 [Python 3.9+](#__tabbed_17_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_18_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

That way, the original `APIRouter` will stay unmodified, so we can still share that same `app/internal/admin.py` file with other projects in the organization.

The result is that in our app, each of the *path operations* from the `admin` module will have:

- The prefix `/admin`.
- The tag `admin`.
- The dependency `get_token_header`.
- The response `418`. 🍵

But that will only affect that `APIRouter` in our app, not in any other code that uses it.

So, for example, other projects could use the same `APIRouter` with a different authentication method.

### Include apath operation¶

We can also add *path operations* directly to the `FastAPI` app.

Here we do it... just to show that we can 🤷:

 [Python 3.9+](#__tabbed_19_1)   app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_20_1)

Tip

Prefer to use the `Annotated` version if possible.

  app/main.py

```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

and it will work correctly, together with all the other *path operations* added with `app.include_router()`.

Very Technical Details

**Note**: this is a very technical detail that you probably can **just skip**.

---

The `APIRouter`s are not "mounted", they are not isolated from the rest of the application.

This is because we want to include their *path operations* in the OpenAPI schema and the user interfaces.

As we cannot just isolate them and "mount" them independently of the rest, the *path operations* are "cloned" (re-created), not included directly.

## Check the automatic API docs¶

Now, run your app:

```
fastapi dev app/main.py
```

And open the docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic API docs, including the paths from all the submodules, using the correct paths (and prefixes) and the correct tags:

![image](https://fastapi.tiangolo.com/img/tutorial/bigger-applications/image01.png)

## Include the same router multiple times with differentprefix¶

You can also use `.include_router()` multiple times with the *same* router using different prefixes.

This could be useful, for example, to expose the same API under different prefixes, e.g. `/api/v1` and `/api/latest`.

This is an advanced usage that you might not really need, but it's there in case you do.

## Include anAPIRouterin another¶

The same way you can include an `APIRouter` in a `FastAPI` application, you can include an `APIRouter` in another `APIRouter` using:

```
router.include_router(other_router)
```

Make sure you do it before including `router` in the `FastAPI` app, so that the *path operations* from `other_router` are also included.

---

# Body

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Body - Fields¶

The same way you can declare additional validation and metadata in *path operation function* parameters with `Query`, `Path` and `Body`, you can declare validation and metadata inside of Pydantic models using Pydantic's `Field`.

## ImportField¶

First, you have to import it:

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

Warning

Notice that `Field` is imported directly from `pydantic`, not from `fastapi` as are all the rest (`Query`, `Path`, `Body`, etc).

## Declare model attributes¶

You can then use `Field` with model attributes:

 [Python 3.10+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
from typing import Annotated, Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```

`Field` works the same way as `Query`, `Path` and `Body`, it has all the same parameters, etc.

Technical Details

Actually, `Query`, `Path` and others you'll see next create objects of subclasses of a common `Param` class, which is itself a subclass of Pydantic's `FieldInfo` class.

And Pydantic's `Field` returns an instance of `FieldInfo` as well.

`Body` also returns objects of a subclass of `FieldInfo` directly. And there are others you will see later that are subclasses of the `Body` class.

Remember that when you import `Query`, `Path`, and others from `fastapi`, those are actually functions that return special classes.

Tip

Notice how each model's attribute with a type, default value and `Field` has the same structure as a *path operation function's* parameter, with `Field` instead of `Path`, `Query` and `Body`.

## Add extra information¶

You can declare extra information in `Field`, `Query`, `Body`, etc. And it will be included in the generated JSON Schema.

You will learn more about adding extra information later in the docs, when learning to declare examples.

Warning

Extra keys passed to `Field` will also be present in the resulting OpenAPI schema for your application.
As these keys may not necessarily be part of the OpenAPI specification, some OpenAPI tools, for example [the OpenAPI validator](https://validator.swagger.io/), may not work with your generated schema.

## Recap¶

You can use Pydantic's `Field` to declare extra validations and metadata for model attributes.

You can also use the extra keyword arguments to pass additional JSON Schema metadata.
