# Query Parameters¶ and more

# Query Parameters¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Query Parameters¶

When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

The query is the set of key-value pairs that go after the `?` in a URL, separated by `&` characters.

For example, in the URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...the query parameters are:

- `skip`: with a value of `0`
- `limit`: with a value of `10`

As they are part of the URL, they are "naturally" strings.

But when you declare them with Python types (in the example above, as `int`), they are converted to that type and validated against it.

All the same process that applied for path parameters also applies for query parameters:

- Editor support (obviously)
- Data "parsing"
- Data validation
- Automatic documentation

## Defaults¶

As query parameters are not a fixed part of a path, they can be optional and can have default values.

In the example above they have default values of `skip=0` and `limit=10`.

So, going to the URL:

```
http://127.0.0.1:8000/items/
```

would be the same as going to:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

But if you go to, for example:

```
http://127.0.0.1:8000/items/?skip=20
```

The parameter values in your function will be:

- `skip=20`: because you set it in the URL
- `limit=10`: because that was the default value

## Optional parameters¶

The same way, you can declare optional query parameters, by setting their default to `None`:

 [Python 3.10+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_3_1)

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

In this case, the function parameter `q` will be optional, and will be `None` by default.

Check

Also notice that **FastAPI** is smart enough to notice that the path parameter `item_id` is a path parameter and `q` is not, so, it's a query parameter.

## Query parameter type conversion¶

You can also declare `bool` types, and they will be converted:

 [Python 3.10+](#__tabbed_4_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_5_1)

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

In this case, if you go to:

```
http://127.0.0.1:8000/items/foo?short=1
```

or

```
http://127.0.0.1:8000/items/foo?short=True
```

or

```
http://127.0.0.1:8000/items/foo?short=true
```

or

```
http://127.0.0.1:8000/items/foo?short=on
```

or

```
http://127.0.0.1:8000/items/foo?short=yes
```

or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter `short` with a `bool` value of `True`. Otherwise as `False`.

## Multiple path and query parameters¶

You can declare multiple path parameters and query parameters at the same time, **FastAPI** knows which is which.

And you don't have to declare them in any specific order.

They will be detected by name:

 [Python 3.10+](#__tabbed_6_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_7_1)

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```

## Required query parameters¶

When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.

If you don't want to add a specific value but just make it optional, set the default as `None`.

But when you want to make a query parameter required, you can just not declare any default value:

 [Python 3.9+](#__tabbed_8_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
```

Here the query parameter `needy` is a required query parameter of type `str`.

If you open in your browser a URL like:

```
http://127.0.0.1:8000/items/foo-item
```

...without adding the required parameter `needy`, you will see an error like:

```
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

As `needy` is a required parameter, you would need to set it in the URL:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...this would work:

```
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

And of course, you can define some parameters as required, some as having a default value, and some entirely optional:

 [Python 3.10+](#__tabbed_9_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

In this case, there are 3 query parameters:

- `needy`, a required `str`.
- `skip`, an `int` with a default value of `0`.
- `limit`, an optional `int`.

Tip

You could also use `Enum`s the same way as with [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values).

---

# Request Files¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Request Files¶

You can define files to be uploaded by the client using `File`.

Info

To receive uploaded files, first install [python-multipart](https://github.com/Kludex/python-multipart).

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
$ pip install python-multipart
```

This is because uploaded files are sent as "form data".

## ImportFile¶

Import `File` and `UploadFile` from `fastapi`:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

## DefineFileParameters¶

Create file parameters the same way you would for `Body` or `Form`:

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

Info

`File` is a class that inherits directly from `Form`.

But remember that when you import `Query`, `Path`, `File` and others from `fastapi`, those are actually functions that return special classes.

Tip

To declare File bodies, you need to use `File`, because otherwise the parameters would be interpreted as query parameters or body (JSON) parameters.

The files will be uploaded as "form data".

If you declare the type of your *path operation function* parameter as `bytes`, **FastAPI** will read the file for you and you will receive the contents as `bytes`.

Keep in mind that this means that the whole contents will be stored in memory. This will work well for small files.

But there are several cases in which you might benefit from using `UploadFile`.

## File Parameters withUploadFile¶

Define a file parameter with a type of `UploadFile`:

 [Python 3.9+](#__tabbed_5_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_6_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

Using `UploadFile` has several advantages over `bytes`:

- You don't have to use `File()` in the default value of the parameter.
- It uses a "spooled" file:
  - A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
- This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
- You can get metadata from the uploaded file.
- It has a [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) `async` interface.
- It exposes an actual Python [SpooledTemporaryFile](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) object that you can pass directly to other libraries that expect a file-like object.

### UploadFile¶

`UploadFile` has the following attributes:

- `filename`: A `str` with the original file name that was uploaded (e.g. `myimage.jpg`).
- `content_type`: A `str` with the content type (MIME type / media type) (e.g. `image/jpeg`).
- `file`: A [SpooledTemporaryFile](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) (a [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) object). This is the actual Python file object that you can pass directly to other functions or libraries that expect a "file-like" object.

`UploadFile` has the following `async` methods. They all call the corresponding file methods underneath (using the internal `SpooledTemporaryFile`).

- `write(data)`: Writes `data` (`str` or `bytes`) to the file.
- `read(size)`: Reads `size` (`int`) bytes/characters of the file.
- `seek(offset)`: Goes to the byte position `offset` (`int`) in the file.
  - E.g., `await myfile.seek(0)` would go to the start of the file.
  - This is especially useful if you run `await myfile.read()` once and then need to read the contents again.
- `close()`: Closes the file.

As all these methods are `async` methods, you need to "await" them.

For example, inside of an `async` *path operation function* you can get the contents with:

```
contents = await myfile.read()
```

If you are inside of a normal `def` *path operation function*, you can access the `UploadFile.file` directly, for example:

```
contents = myfile.file.read()
```

`async` Technical Details

When you use the `async` methods, **FastAPI** runs the file methods in a threadpool and awaits for them.

Starlette Technical Details

**FastAPI**'s `UploadFile` inherits directly from **Starlette**'s `UploadFile`, but adds some necessary parts to make it compatible with **Pydantic** and the other parts of FastAPI.

## What is "Form Data"¶

The way HTML forms (`<form></form>`) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

**FastAPI** will make sure to read that data from the right place instead of JSON.

Technical Details

Data from forms is normally encoded using the "media type" `application/x-www-form-urlencoded` when it doesn't include files.

But when the form includes files, it is encoded as `multipart/form-data`. If you use `File`, **FastAPI** will know it has to get the files from the correct part of the body.

If you want to read more about these encodings and form fields, head to the [MDNweb docs forPOST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).

Warning

You can declare multiple `File` and `Form` parameters in a *path operation*, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

## Optional File Upload¶

You can make a file optional by using standard type annotations and setting a default value of `None`:

 [Python 3.10+](#__tabbed_7_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)[Python 3.10+ - non-Annotated](#__tabbed_8_2)[Python 3.9+ - non-Annotated](#__tabbed_8_3)

```
from typing import Annotated, Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[Union[bytes, None], File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
```

## UploadFilewith Additional Metadata¶

You can also use `File()` with `UploadFile`, for example, to set additional metadata:

 [Python 3.9+](#__tabbed_9_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_10_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}
```

## Multiple File Uploads¶

It's possible to upload several files at the same time.

They would be associated to the same "form field" sent using "form data".

To use that, declare a list of `bytes` or `UploadFile`:

 [Python 3.9+](#__tabbed_11_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_12_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files/")
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

You will receive, as declared, a `list` of `bytes` or `UploadFile`s.

Technical Details

You could also use `from starlette.responses import HTMLResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

### Multiple File Uploads with Additional Metadata¶

And the same way as before, you can use `File()` to set additional parameters, even for `UploadFile`:

 [Python 3.9+](#__tabbed_13_1)

```
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_14_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
```

## Recap¶

Use `File`, `bytes`, and `UploadFile` to declare files to be uploaded in the request, sent as form data.

---

# Form Models¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Form Models¶

You can use **Pydantic models** to declare **form fields** in FastAPI.

Info

To use forms, first install [python-multipart](https://github.com/Kludex/python-multipart).

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
$ pip install python-multipart
```

Note

This is supported since FastAPI version `0.113.0`. 🤓

## Pydantic Models for Forms¶

You just need to declare a **Pydantic model** with the fields you want to receive as **form fields**, and then declare the parameter as `Form`:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(data: FormData = Form()):
    return data
```

**FastAPI** will **extract** the data for **each field** from the **form data** in the request and give you the Pydantic model you defined.

## Check the Docs¶

You can verify it in the docs UI at `/docs`:

  ![image](https://fastapi.tiangolo.com/img/tutorial/request-form-models/image01.png)

## Forbid Extra Form Fields¶

In some special use cases (probably not very common), you might want to **restrict** the form fields to only those declared in the Pydantic model. And **forbid** any **extra** fields.

Note

This is supported since FastAPI version `0.114.0`. 🤓

You can use Pydantic's model configuration to `forbid` any `extra` fields:

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post("/login/")
async def login(data: FormData = Form()):
    return data
```

If a client tries to send some extra data, they will receive an **error** response.

For example, if the client tries to send the form fields:

- `username`: `Rick`
- `password`: `Portal Gun`
- `extra`: `Mr. Poopybutthole`

They will receive an error response telling them that the field `extra` is not allowed:

```
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## Summary¶

You can use Pydantic models to declare form fields in FastAPI. 😎

---

# Request Forms and Files¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Request Forms and Files¶

You can define files and form fields at the same time using `File` and `Form`.

Info

To receive uploaded files and/or form data, first install [python-multipart](https://github.com/Kludex/python-multipart).

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
$ pip install python-multipart
```

## ImportFileandForm¶

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

## DefineFileandFormparameters¶

Create file and form parameters the same way you would for `Body` or `Query`:

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
```

The files and form fields will be uploaded as form data and you will receive the files and form fields.

And you can declare some of the files as `bytes` and some as `UploadFile`.

Warning

You can declare multiple `File` and `Form` parameters in a *path operation*, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `multipart/form-data` instead of `application/json`.

This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

## Recap¶

Use `File` and `Form` together when you need to receive data and files in the same request.

---

# Form Data¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Form Data¶

When you need to receive form fields instead of JSON, you can use `Form`.

Info

To use forms, first install [python-multipart](https://github.com/Kludex/python-multipart).

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then install it, for example:

```
$ pip install python-multipart
```

## ImportForm¶

Import `Form` from `fastapi`:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_2_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

## DefineFormparameters¶

Create form parameters the same way you would for `Body` or `Query`:

 [Python 3.9+](#__tabbed_3_1)

```
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

     🤓 Other versions and variants [Python 3.9+ - non-Annotated](#__tabbed_4_1)

Tip

Prefer to use the `Annotated` version if possible.

```
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

For example, in one of the ways the OAuth2 specification can be used (called "password flow") it is required to send a `username` and `password` as form fields.

The spec requires the fields to be exactly named `username` and `password`, and to be sent as form fields, not JSON.

With `Form` you can declare the same configurations as with `Body` (and `Query`, `Path`, `Cookie`), including validation, examples, an alias (e.g. `user-name` instead of `username`), etc.

Info

`Form` is a class that inherits directly from `Body`.

Tip

To declare form bodies, you need to use `Form` explicitly, because without it the parameters would be interpreted as query parameters or body (JSON) parameters.

## About "Form Fields"¶

The way HTML forms (`<form></form>`) sends the data to the server normally uses a "special" encoding for that data, it's different from JSON.

**FastAPI** will make sure to read that data from the right place instead of JSON.

Technical Details

Data from forms is normally encoded using the "media type" `application/x-www-form-urlencoded`.

But when the form includes files, it is encoded as `multipart/form-data`. You'll read about handling files in the next chapter.

If you want to read more about these encodings and form fields, head to the [MDNweb docs forPOST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).

Warning

You can declare multiple `Form` parameters in a *path operation*, but you can't also declare `Body` fields that you expect to receive as JSON, as the request will have the body encoded using `application/x-www-form-urlencoded` instead of `application/json`.

This is not a limitation of **FastAPI**, it's part of the HTTP protocol.

## Recap¶

Use `Form` to declare form data input parameters.
