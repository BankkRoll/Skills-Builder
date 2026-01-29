# Advanced Security¶ and more

# Advanced Security¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Advanced Security¶

## Additional Features¶

There are some extra features to handle security apart from the ones covered in the [Tutorial - User Guide: Security](https://fastapi.tiangolo.com/tutorial/security/).

Tip

The next sections are **not necessarily "advanced"**.

And it's possible that for your use case, the solution is in one of them.

## Read the Tutorial first¶

The next sections assume you already read the main [Tutorial - User Guide: Security](https://fastapi.tiangolo.com/tutorial/security/).

They are all based on the same concepts, but allow some extra functionalities.

---

# Settings and Environment Variables¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Settings and Environment Variables¶

In many cases your application could need some external settings or configurations, for example secret keys, database credentials, credentials for email services, etc.

Most of these settings are variable (can change), like database URLs. And many could be sensitive, like secrets.

For this reason it's common to provide them in environment variables that are read by the application.

Tip

To understand environment variables you can read [Environment Variables](https://fastapi.tiangolo.com/environment-variables/).

## Types and validation¶

These environment variables can only handle text strings, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).

That means that any value read in Python from an environment variable will be a `str`, and any conversion to a different type or any validation has to be done in code.

## PydanticSettings¶

Fortunately, Pydantic provides a great utility to handle these settings coming from environment variables with [Pydantic: Settings management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

### Installpydantic-settings¶

First, make sure you create your [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install the `pydantic-settings` package:

```
pip install pydantic-settings
```

It also comes included when you install the `all` extras with:

```
pip install "fastapi[all]"
```

### Create theSettingsobject¶

Import `BaseSettings` from Pydantic and create a sub-class, very much like with a Pydantic model.

The same way as with Pydantic models, you declare class attributes with type annotations, and possibly default values.

You can use all the same validation features and tools you use for Pydantic models, like different data types and additional validations with `Field()`.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

settings = Settings()
app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Tip

If you want something quick to copy and paste, don't use this example, use the last one below.

Then, when you create an instance of that `Settings` class (in this case, in the `settings` object), Pydantic will read the environment variables in a case-insensitive way, so, an upper-case variable `APP_NAME` will still be read for the attribute `app_name`.

Next it will convert and validate the data. So, when you use that `settings` object, you will have data of the types you declared (e.g. `items_per_user` will be an `int`).

### Use thesettings¶

Then you can use the new `settings` object in your application:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

settings = Settings()
app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

### Run the server¶

Next, you would run the server passing the configurations as environment variables, for example you could set an `ADMIN_EMAIL` and `APP_NAME` with:

```
ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" fastapi run main.py
```

Tip

To set multiple env vars for a single command just separate them with a space, and put them all before the command.

And then the `admin_email` setting would be set to `"deadpool@example.com"`.

The `app_name` would be `"ChimichangApp"`.

And the `items_per_user` would keep its default value of `50`.

## Settings in another module¶

You could put those settings in another module file as you saw in [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

For example, you could have a file `config.py` with:

 [Python 3.9+](#__tabbed_3_1)

```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

settings = Settings()
```

And then use it in a file `main.py`:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI

from .config import settings

app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Tip

You would also need a file `__init__.py` as you saw in [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

## Settings in a dependency¶

In some occasions it might be useful to provide the settings from a dependency, instead of having a global object with `settings` that is used everywhere.

This could be especially useful during testing, as it's very easy to override a dependency with your own custom settings.

### The config file¶

Coming from the previous example, your `config.py` file could look like:

 [Python 3.9+](#__tabbed_5_1)

```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_6_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
```

Notice that now we don't create a default instance `settings = Settings()`.

### The main app file¶

Now we create a dependency that returns a new `config.Settings()`.

 [Python 3.9+](#__tabbed_7_1)

```
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .config import Settings

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_8_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from functools import lru_cache

from fastapi import Depends, FastAPI

from .config import Settings

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Tip

We'll discuss the `@lru_cache` in a bit.

For now you can assume `get_settings()` is a normal function.

And then we can require it from the *path operation function* as a dependency and use it anywhere we need it.

 [Python 3.9+](#__tabbed_9_1)

```
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .config import Settings

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_10_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from functools import lru_cache

from fastapi import Depends, FastAPI

from .config import Settings

app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

### Settings and testing¶

Then it would be very easy to provide a different settings object during testing by creating a dependency override for `get_settings`:

 [Python 3.9+](#__tabbed_11_1)

```
from fastapi.testclient import TestClient

from .config import Settings
from .main import app, get_settings

client = TestClient(app)

def get_settings_override():
    return Settings(admin_email="testing_admin@example.com")

app.dependency_overrides[get_settings] = get_settings_override

def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_12_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi.testclient import TestClient

from .config import Settings
from .main import app, get_settings

client = TestClient(app)

def get_settings_override():
    return Settings(admin_email="testing_admin@example.com")

app.dependency_overrides[get_settings] = get_settings_override

def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }
```

In the dependency override we set a new value for the `admin_email` when creating the new `Settings` object, and then we return that new object.

Then we can test that it is used.

## Reading a.envfile¶

If you have many settings that possibly change a lot, maybe in different environments, it might be useful to put them on a file and then read them from it as if they were environment variables.

This practice is common enough that it has a name, these environment variables are commonly placed in a file `.env`, and the file is called a "dotenv".

Tip

A file starting with a dot (`.`) is a hidden file in Unix-like systems, like Linux and macOS.

But a dotenv file doesn't really have to have that exact filename.

Pydantic has support for reading from these types of files using an external library. You can read more at [Pydantic Settings: Dotenv (.env) support](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support).

Tip

For this to work, you need to `pip install python-dotenv`.

### The.envfile¶

You could have a `.env` file with:

```
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

### Read settings from.env¶

And then update your `config.py` with:

 [Python 3.9+](#__tabbed_13_1)

```
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    model_config = SettingsConfigDict(env_file=".env")
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_14_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    model_config = SettingsConfigDict(env_file=".env")
```

Tip

The `model_config` attribute is used just for Pydantic configuration. You can read more at [Pydantic: Concepts: Configuration](https://docs.pydantic.dev/latest/concepts/config/).

Here we define the config `env_file` inside of your Pydantic `Settings` class, and set the value to the filename with the dotenv file we want to use.

### Creating theSettingsonly once withlru_cache¶

Reading a file from disk is normally a costly (slow) operation, so you probably want to do it only once and then reuse the same settings object, instead of reading it for each request.

But every time we do:

```
Settings()
```

a new `Settings` object would be created, and at creation it would read the `.env` file again.

If the dependency function was just like:

```
def get_settings():
    return Settings()
```

we would create that object for each request, and we would be reading the `.env` file for each request. ⚠️

But as we are using the `@lru_cache` decorator on top, the `Settings` object will be created only once, the first time it's called. ✔️

 [Python 3.9+](#__tabbed_15_1)

```
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from . import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_16_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from functools import lru_cache

from fastapi import Depends, FastAPI

from . import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

Then for any subsequent call of `get_settings()` in the dependencies for the next requests, instead of executing the internal code of `get_settings()` and creating a new `Settings` object, it will return the same object that was returned on the first call, again and again.

#### lru_cacheTechnical Details¶

`@lru_cache` modifies the function it decorates to return the same value that was returned the first time, instead of computing it again, executing the code of the function every time.

So, the function below it will be executed once for each combination of arguments. And then the values returned by each of those combinations of arguments will be used again and again whenever the function is called with exactly the same combination of arguments.

For example, if you have a function:

```
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
```

your program could execute like this:

In the case of our dependency `get_settings()`, the function doesn't even take any arguments, so it always returns the same value.

That way, it behaves almost as if it was just a global variable. But as it uses a dependency function, then we can override it easily for testing.

`@lru_cache` is part of `functools` which is part of Python's standard library, you can read more about it in the [Python docs for@lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache).

## Recap¶

You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models.

- By using a dependency you can simplify testing.
- You can use `.env` files with it.
- Using `@lru_cache` lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.

---

# Sub Applications

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Sub Applications - Mounts¶

If you need to have two independent FastAPI applications, with their own independent OpenAPI and their own docs UIs, you can have a main app and "mount" one (or more) sub-application(s).

## Mounting aFastAPIapplication¶

"Mounting" means adding a completely "independent" application in a specific path, that then takes care of handling everything under that path, with the *path operations* declared in that sub-application.

### Top-level application¶

First, create the main, top-level, **FastAPI** application, and its *path operations*:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

subapi = FastAPI()

@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}

app.mount("/subapi", subapi)
```

### Sub-application¶

Then, create your sub-application, and its *path operations*.

This sub-application is just another standard FastAPI application, but this is the one that will be "mounted":

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

subapi = FastAPI()

@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}

app.mount("/subapi", subapi)
```

### Mount the sub-application¶

In your top-level application, `app`, mount the sub-application, `subapi`.

In this case, it will be mounted at the path `/subapi`:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

subapi = FastAPI()

@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}

app.mount("/subapi", subapi)
```

### Check the automatic API docs¶

Now, run the `fastapi` command with your file:

```
fastapi dev main.py
```

And open the docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic API docs for the main app, including only its own *path operations*:

![image](https://fastapi.tiangolo.com/img/tutorial/sub-applications/image01.png)

And then, open the docs for the sub-application, at [http://127.0.0.1:8000/subapi/docs](http://127.0.0.1:8000/subapi/docs).

You will see the automatic API docs for the sub-application, including only its own *path operations*, all under the correct sub-path prefix `/subapi`:

![image](https://fastapi.tiangolo.com/img/tutorial/sub-applications/image02.png)

If you try interacting with any of the two user interfaces, they will work correctly, because the browser will be able to talk to each specific app or sub-app.

### Technical Details:root_path¶

When you mount a sub-application as described above, FastAPI will take care of communicating the mount path for the sub-application using a mechanism from the ASGI specification called a `root_path`.

That way, the sub-application will know to use that path prefix for the docs UI.

And the sub-application could also have its own mounted sub-applications and everything would work correctly, because FastAPI handles all these `root_path`s automatically.

You will learn more about the `root_path` and how to use it explicitly in the section about [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

---

# Templates¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Templates¶

You can use any template engine you want with **FastAPI**.

A common choice is Jinja2, the same one used by Flask and other tools.

There are utilities to configure it easily that you can use directly in your **FastAPI** application (provided by Starlette).

## Install dependencies¶

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and install `jinja2`:

```
pip install jinja2
```

## UsingJinja2Templates¶

- Import `Jinja2Templates`.
- Create a `templates` object that you can reuse later.
- Declare a `Request` parameter in the *path operation* that will return a template.
- Use the `templates` you created to render and return a `TemplateResponse`, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
```

Note

Before FastAPI 0.108.0, Starlette 0.29.0, the `name` was the first parameter.

Also, before that, in previous versions, the `request` object was passed as part of the key-value pairs in the context for Jinja2.

Tip

By declaring `response_class=HTMLResponse` the docs UI will be able to know that the response will be HTML.

Technical Details

You could also use `from starlette.templating import Jinja2Templates`.

**FastAPI** provides the same `starlette.templating` as `fastapi.templating` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `Request` and `StaticFiles`.

## Writing templates¶

Then you can write a template at `templates/item.html` with, for example:

```
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1><a href="{{ url_for('read_item', id=id) }}">Item ID: {{ id }}</a></h1>
</body>
</html>
```

### Template Context Values¶

In the HTML that contains:

```
Item ID: {{ id }}
```

...it will show the `id` taken from the "context" `dict` you passed:

```
{"id": id}
```

For example, with an ID of `42`, this would render:

```
Item ID: 42
```

### Templateurl_forArguments¶

You can also use `url_for()` inside of the template, it takes as arguments the same arguments that would be used by your *path operation function*.

So, the section with:

```
<a href="{{ url_for('read_item', id=id) }}">
```

...will generate a link to the same URL that would be handled by the *path operation function* `read_item(id=id)`.

For example, with an ID of `42`, this would render:

```
<a href="/items/42">
```

## Templates and static files¶

You can also use `url_for()` inside of the template, and use it, for example, with the `StaticFiles` you mounted with the `name="static"`.

```
<html>
<head>
    <title>Item Details</title>
    <link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
</head>
<body>
    <h1><a href="{{ url_for('read_item', id=id) }}">Item ID: {{ id }}</a></h1>
</body>
</html>
```

In this example, it would link to a CSS file at `static/styles.css` with:

```
h1 {
    color: green;
}
```

And because you are using `StaticFiles`, that CSS file would be served automatically by your **FastAPI** application at the URL `/static/styles.css`.

## More details¶

For more details, including how to test templates, check [Starlette's docs on templates](https://www.starlette.dev/templates/).

---

# Testing Dependencies with Overrides¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Testing Dependencies with Overrides¶

## Overriding dependencies during testing¶

There are some scenarios where you might want to override a dependency during testing.

You don't want the original dependency to run (nor any of the sub-dependencies it might have).

Instead, you want to provide a different dependency that will be used only during tests (possibly only some specific tests), and will provide a value that can be used where the value of the original dependency was used.

### Use cases: external service¶

An example could be that you have an external authentication provider that you need to call.

You send it a token and it returns an authenticated user.

This provider might be charging you per request, and calling it might take some extra time than if you had a fixed mock user for tests.

You probably want to test the external provider once, but not necessarily call it for every test that runs.

In this case, you can override the dependency that calls that provider, and use a custom dependency that returns a mock user, only for your tests.

### Use theapp.dependency_overridesattribute¶

For these cases, your **FastAPI** application has an attribute `app.dependency_overrides`, it is a simple `dict`.

To override a dependency for testing, you put as a key the original dependency (a function), and as the value, your dependency override (another function).

And then **FastAPI** will call that override instead of the original dependency.

 [Python 3.10+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}

client = TestClient(app)

async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}

app.dependency_overrides[common_parameters] = override_dependency

def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }

def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }

def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Users!", "params": commons}

client = TestClient(app)

async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}

app.dependency_overrides[common_parameters] = override_dependency

def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }

def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }

def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}

client = TestClient(app)

async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}

app.dependency_overrides[common_parameters] = override_dependency

def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }

def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }

def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Items!", "params": commons}

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return {"message": "Hello Users!", "params": commons}

client = TestClient(app)

async def override_dependency(q: Union[str, None] = None):
    return {"q": q, "skip": 5, "limit": 10}

app.dependency_overrides[common_parameters] = override_dependency

def test_override_in_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }

def test_override_in_items_with_q():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }

def test_override_in_items_with_params():
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }
```

Tip

You can set a dependency override for a dependency used anywhere in your **FastAPI** application.

The original dependency could be used in a *path operation function*, a *path operation decorator* (when you don't use the return value), a `.include_router()` call, etc.

FastAPI will still be able to override it.

Then you can reset your overrides (remove them) by setting `app.dependency_overrides` to be an empty `dict`:

```
app.dependency_overrides = {}
```

Tip

If you want to override a dependency only during some tests, you can set the override at the beginning of the test (inside the test function) and reset it at the end (at the end of the test function).

---

# Testing Events: lifespan and startup

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Testing Events: lifespan and startup - shutdown¶

When you need `lifespan` to run in your tests, you can use the `TestClient` with a `with` statement:

 [Python 3.9+](#__tabbed_1_1)

```
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

items = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield
    # clean up items
    items.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]

def test_read_items():
    # Before the lifespan starts, "items" is still empty
    assert items == {}

    with TestClient(app) as client:
        # Inside the "with TestClient" block, the lifespan starts and items added
        assert items == {"foo": {"name": "Fighters"}, "bar": {"name": "Tenders"}}

        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}

        # After the requests is done, the items are still there
        assert items == {"foo": {"name": "Fighters"}, "bar": {"name": "Tenders"}}

    # The end of the "with TestClient" block simulates terminating the app, so
    # the lifespan ends and items are cleaned up
    assert items == {}
```

You can read more details about the ["Running lifespan in tests in the official Starlette documentation site."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

For the deprecated `startup` and `shutdown` events, you can use the `TestClient` as follows:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}

@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]

def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}
```

---

# Testing WebSockets¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Testing WebSockets¶

You can use the same `TestClient` to test WebSockets.

For this, you use the `TestClient` in a `with` statement, connecting to the WebSocket:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
```

Note

For more details, check Starlette's documentation for [testing WebSockets](https://www.starlette.dev/testclient/#testing-websocket-sessions).

---

# Using the Request Directly¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Using the Request Directly¶

Up to now, you have been declaring the parts of the request that you need with their types.

Taking data from:

- The path as parameters.
- Headers.
- Cookies.
- etc.

And by doing so, **FastAPI** is validating that data, converting it and generating documentation for your API automatically.

But there are situations where you might need to access the `Request` object directly.

## Details about theRequestobject¶

As **FastAPI** is actually **Starlette** underneath, with a layer of several tools on top, you can use Starlette's [Request](https://www.starlette.dev/requests/) object directly when you need to.

It would also mean that if you get data from the `Request` object directly (for example, read the body) it won't be validated, converted or documented (with OpenAPI, for the automatic API user interface) by FastAPI.

Although any other parameter declared normally (for example, the body with a Pydantic model) would still be validated, converted, annotated, etc.

But there are specific cases where it's useful to get the `Request` object.

## Use theRequestobject directly¶

Let's imagine you want to get the client's IP address/host inside of your *path operation function*.

For that you need to access the request directly.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```

By declaring a *path operation function* parameter with the type being the `Request` **FastAPI** will know to pass the `Request` in that parameter.

Tip

Note that in this case, we are declaring a path parameter beside the request parameter.

So, the path parameter will be extracted, validated, converted to the specified type and annotated with OpenAPI.

The same way, you can declare any other parameter as normally, and additionally, get the `Request` too.

## Requestdocumentation¶

You can read more details about the [Requestobject in the official Starlette documentation site](https://www.starlette.dev/requests/).

Technical Details

You could also use `from starlette.requests import Request`.

**FastAPI** provides it directly just as a convenience for you, the developer. But it comes directly from Starlette.
