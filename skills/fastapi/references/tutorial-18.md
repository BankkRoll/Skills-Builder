# Static Files¶ and more

# Static Files¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Static Files¶

You can serve static files automatically from a directory using `StaticFiles`.

## UseStaticFiles¶

- Import `StaticFiles`.
- "Mount" a `StaticFiles()` instance in a specific path.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

Technical Details

You could also use `from starlette.staticfiles import StaticFiles`.

**FastAPI** provides the same `starlette.staticfiles` as `fastapi.staticfiles` just as a convenience for you, the developer. But it actually comes directly from Starlette.

### What is "Mounting"¶

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

This is different from using an `APIRouter` as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

You can read more about this in the [Advanced User Guide](https://fastapi.tiangolo.com/advanced/).

## Details¶

The first `"/static"` refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with `"/static"` will be handled by it.

The `directory="static"` refers to the name of the directory that contains your static files.

The `name="static"` gives it a name that can be used internally by **FastAPI**.

All these parameters can be different than "`static`", adjust them with the needs and specific details of your own application.

## More info¶

For more details and options check [Starlette's docs about Static Files](https://www.starlette.dev/staticfiles/).

---

# Testing¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Testing¶

Thanks to [Starlette](https://www.starlette.dev/testclient/), testing **FastAPI** applications is easy and enjoyable.

It is based on [HTTPX](https://www.python-httpx.org), which in turn is designed based on Requests, so it's very familiar and intuitive.

With it, you can use [pytest](https://docs.pytest.org/) directly with **FastAPI**.

## UsingTestClient¶

Info

To use `TestClient`, first install [httpx](https://www.python-httpx.org).

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
$ pip install httpx
```

Import `TestClient`.

Create a `TestClient` by passing your **FastAPI** application to it.

Create functions with a name that starts with `test_` (this is standard `pytest` conventions).

Use the `TestClient` object the same way as you do with `httpx`.

Write simple `assert` statements with the standard Python expressions that you need to check (again, standard `pytest`).

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

Tip

Notice that the testing functions are normal `def`, not `async def`.

And the calls to the client are also normal calls, not using `await`.

This allows you to use `pytest` directly without complications.

Technical Details

You could also use `from starlette.testclient import TestClient`.

**FastAPI** provides the same `starlette.testclient` as `fastapi.testclient` just as a convenience for you, the developer. But it comes directly from Starlette.

Tip

If you want to call `async` functions in your tests apart from sending requests to your FastAPI application (e.g. asynchronous database functions), have a look at the [Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/) in the advanced tutorial.

## Separating tests¶

In a real application, you probably would have your tests in a different file.

And your **FastAPI** application might also be composed of several files/modules, etc.

### FastAPIapp file¶

Let's say you have a file structure as described in [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/):

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

In the file `main.py` you have your **FastAPI** app:

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

### Testing file¶

Then you could have a file `test_main.py` with your tests. It could live on the same Python package (the same directory with a `__init__.py` file):

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Because this file is in the same package, you can use relative imports to import the object `app` from the `main` module (`main.py`):

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

...and have the code for the tests just like before.

## Testing: extended example¶

Now let's extend this example and add more details to see how to test different parts.

### ExtendedFastAPIapp file¶

Let's continue with the same file structure as before:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Let's say that now the file `main.py` with your **FastAPI** app has some other **path operations**.

It has a `GET` operation that could return an error.

It has a `POST` operation that could return several errors.

Both *path operations* require an `X-Token` header.

 [Python 3.10+](#__tabbed_4_1)

```
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_5_1)[Python 3.10+ - non-Annotated](#__tabbed_5_2)[Python 3.9+ - non-Annotated](#__tabbed_5_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()

class Item(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()

class Item(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[item.id] = item
    return item
```

### Extended testing file¶

You could then update `test_main.py` with the extended tests:

 [Python 3.10+](#__tabbed_6_1)

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_7_1)[Python 3.10+ - non-Annotated](#__tabbed_7_2)[Python 3.9+ - non-Annotated](#__tabbed_7_3)

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_nonexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
```

Whenever you need the client to pass information in the request and you don't know how to, you can search (Google) how to do it in `httpx`, or even how to do it with `requests`, as HTTPX's design is based on Requests' design.

Then you just do the same in your tests.

E.g.:

- To pass a *path* or *query* parameter, add it to the URL itself.
- To pass a JSON body, pass a Python object (e.g. a `dict`) to the parameter `json`.
- If you need to send *Form Data* instead of JSON, use the `data` parameter instead.
- To pass *headers*, use a `dict` in the `headers` parameter.
- For *cookies*, a `dict` in the `cookies` parameter.

For more information about how to pass data to the backend (using `httpx` or the `TestClient`) check the [HTTPX documentation](https://www.python-httpx.org).

Info

Note that the `TestClient` receives data that can be converted to JSON, not Pydantic models.

If you have a Pydantic model in your test and you want to send its data to the application during testing, you can use the `jsonable_encoder` described in [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).

## Run it¶

After that, you just need to install `pytest`.

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
pip install pytest
```

It will detect the files and tests automatically, execute them, and report the results back to you.

Run the tests with:

```
pytest
```
