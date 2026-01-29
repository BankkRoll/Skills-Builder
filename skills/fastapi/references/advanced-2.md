# Behind a Proxy¶ and more

# Behind a Proxy¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Behind a Proxy¶

In many situations, you would use a **proxy** like Traefik or Nginx in front of your FastAPI app.

These proxies could handle HTTPS certificates and other things.

## Proxy Forwarded Headers¶

A **proxy** in front of your application would normally set some headers on the fly before sending the requests to your **server** to let the server know that the request was **forwarded** by the proxy, letting it know the original (public) URL, including the domain, that it is using HTTPS, etc.

The **server** program (for example **Uvicorn** via **FastAPI CLI**) is capable of interpreting these headers, and then passing that information to your application.

But for security, as the server doesn't know it is behind a trusted proxy, it won't interpret those headers.

Technical Details

The proxy headers are:

- [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
- [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
- [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

### Enable Proxy Forwarded Headers¶

You can start FastAPI CLI with the *CLI Option* `--forwarded-allow-ips` and pass the IP addresses that should be trusted to read those forwarded headers.

If you set it to `--forwarded-allow-ips="*"` it would trust all the incoming IPs.

If your **server** is behind a trusted **proxy** and only the proxy talks to it, this would make it accept whatever is the IP of that **proxy**.

```
fastapi run --forwarded-allow-ips="*"
```

### Redirects with HTTPS¶

For example, let's say you define a *path operation* `/items/`:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items():
    return ["plumbus", "portal gun"]
```

If the client tries to go to `/items`, by default, it would be redirected to `/items/`.

But before setting the *CLI Option* `--forwarded-allow-ips` it could redirect to `http://localhost:8000/items/`.

But maybe your application is hosted at `https://mysuperapp.com`, and the redirection should be to `https://mysuperapp.com/items/`.

By setting `--proxy-headers` now FastAPI would be able to redirect to the right location. 😎

```
https://mysuperapp.com/items/
```

Tip

If you want to learn more about HTTPS, check the guide [About HTTPS](https://fastapi.tiangolo.com/deployment/https/).

### How Proxy Forwarded Headers Work¶

Here's a visual representation of how the **proxy** adds forwarded headers between the client and the **application server**:

The **proxy** intercepts the original client request and adds the special *forwarded* headers (`X-Forwarded-*`) before passing the request to the **application server**.

These headers preserve information about the original request that would otherwise be lost:

- **X-Forwarded-For**: The original client's IP address
- **X-Forwarded-Proto**: The original protocol (`https`)
- **X-Forwarded-Host**: The original host (`mysuperapp.com`)

When **FastAPI CLI** is configured with `--forwarded-allow-ips`, it trusts these headers and uses them, for example to generate the correct URLs in redirects.

## Proxy with a stripped path prefix¶

You could have a proxy that adds a path prefix to your application.

In these cases you can use `root_path` to configure your application.

The `root_path` is a mechanism provided by the ASGI specification (that FastAPI is built on, through Starlette).

The `root_path` is used to handle these specific cases.

And it's also used internally when mounting sub-applications.

Having a proxy with a stripped path prefix, in this case, means that you could declare a path at `/app` in your code, but then, you add a layer on top (the proxy) that would put your **FastAPI** application under a path like `/api/v1`.

In this case, the original path `/app` would actually be served at `/api/v1/app`.

Even though all your code is written assuming there's just `/app`.

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

And the proxy would be **"stripping"** the **path prefix** on the fly before transmitting the request to the app server (probably Uvicorn via FastAPI CLI), keeping your application convinced that it is being served at `/app`, so that you don't have to update all your code to include the prefix `/api/v1`.

Up to here, everything would work as normally.

But then, when you open the integrated docs UI (the frontend), it would expect to get the OpenAPI schema at `/openapi.json`, instead of `/api/v1/openapi.json`.

So, the frontend (that runs in the browser) would try to reach `/openapi.json` and wouldn't be able to get the OpenAPI schema.

Because we have a proxy with a path prefix of `/api/v1` for our app, the frontend needs to fetch the OpenAPI schema at `/api/v1/openapi.json`.

Tip

The IP `0.0.0.0` is commonly used to mean that the program listens on all the IPs available in that machine/server.

The docs UI would also need the OpenAPI schema to declare that this API `server` is located at `/api/v1` (behind the proxy). For example:

```
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        }
    ],
    "paths": {
            // More stuff here
    }
}
```

In this example, the "Proxy" could be something like **Traefik**. And the server would be something like FastAPI CLI with **Uvicorn**, running your FastAPI application.

### Providing theroot_path¶

To achieve this, you can use the command line option `--root-path` like:

```
fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1
```

If you use Hypercorn, it also has the option `--root-path`.

Technical Details

The ASGI specification defines a `root_path` for this use case.

And the `--root-path` command line option provides that `root_path`.

### Checking the currentroot_path¶

You can get the current `root_path` used by your application for each request, it is part of the `scope` dictionary (that's part of the ASGI spec).

Here we are including it in the message just for demonstration purposes.

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

Then, if you start Uvicorn with:

```
fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1
```

The response would be something like:

```
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

### Setting theroot_pathin the FastAPI app¶

Alternatively, if you don't have a way to provide a command line option like `--root-path` or equivalent, you can set the `root_path` parameter when creating your FastAPI app:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI, Request

app = FastAPI(root_path="/api/v1")

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

Passing the `root_path` to `FastAPI` would be the equivalent of passing the `--root-path` command line option to Uvicorn or Hypercorn.

### Aboutroot_path¶

Keep in mind that the server (Uvicorn) won't use that `root_path` for anything else than passing it to the app.

But if you go with your browser to [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app) you will see the normal response:

```
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

So, it won't expect to be accessed at `http://127.0.0.1:8000/api/v1/app`.

Uvicorn will expect the proxy to access Uvicorn at `http://127.0.0.1:8000/app`, and then it would be the proxy's responsibility to add the extra `/api/v1` prefix on top.

## About proxies with a stripped path prefix¶

Keep in mind that a proxy with stripped path prefix is only one of the ways to configure it.

Probably in many cases the default will be that the proxy doesn't have a stripped path prefix.

In a case like that (without a stripped path prefix), the proxy would listen on something like `https://myawesomeapp.com`, and then if the browser goes to `https://myawesomeapp.com/api/v1/app` and your server (e.g. Uvicorn) listens on `http://127.0.0.1:8000` the proxy (without a stripped path prefix) would access Uvicorn at the same path: `http://127.0.0.1:8000/api/v1/app`.

## Testing locally with Traefik¶

You can easily run the experiment locally with a stripped path prefix using [Traefik](https://docs.traefik.io/).

[Download Traefik](https://github.com/containous/traefik/releases), it's a single binary, you can extract the compressed file and run it directly from the terminal.

Then create a file `traefik.toml` with:

```
[entryPoints]
  [entryPoints.http]
    address = ":9999"

[providers]
  [providers.file]
    filename = "routes.toml"
```

This tells Traefik to listen on port 9999 and to use another file `routes.toml`.

Tip

We are using port 9999 instead of the standard HTTP port 80 so that you don't have to run it with admin (`sudo`) privileges.

Now create that other file `routes.toml`:

```
[http]
  [http.middlewares]

    [http.middlewares.api-stripprefix.stripPrefix]
      prefixes = ["/api/v1"]

  [http.routers]

    [http.routers.app-http]
      entryPoints = ["http"]
      service = "app"
      rule = "PathPrefix(`/api/v1`)"
      middlewares = ["api-stripprefix"]

  [http.services]

    [http.services.app]
      [http.services.app.loadBalancer]
        [[http.services.app.loadBalancer.servers]]
          url = "http://127.0.0.1:8000"
```

This file configures Traefik to use the path prefix `/api/v1`.

And then Traefik will redirect its requests to your Uvicorn running on `http://127.0.0.1:8000`.

Now start Traefik:

```
./traefik --configFile=traefik.toml
```

And now start your app, using the `--root-path` option:

```
fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1
```

### Check the responses¶

Now, if you go to the URL with the port for Uvicorn: [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app), you will see the normal response:

```
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

Tip

Notice that even though you are accessing it at `http://127.0.0.1:8000/app` it shows the `root_path` of `/api/v1`, taken from the option `--root-path`.

And now open the URL with the port for Traefik, including the path prefix: [http://127.0.0.1:9999/api/v1/app](http://127.0.0.1:9999/api/v1/app).

We get the same response:

```
{
    "message": "Hello World",
    "root_path": "/api/v1"
}
```

but this time at the URL with the prefix path provided by the proxy: `/api/v1`.

Of course, the idea here is that everyone would access the app through the proxy, so the version with the path prefix `/api/v1` is the "correct" one.

And the version without the path prefix (`http://127.0.0.1:8000/app`), provided by Uvicorn directly, would be exclusively for the *proxy* (Traefik) to access it.

That demonstrates how the Proxy (Traefik) uses the path prefix and how the server (Uvicorn) uses the `root_path` from the option `--root-path`.

### Check the docs UI¶

But here's the fun part. ✨

The "official" way to access the app would be through the proxy with the path prefix that we defined. So, as we would expect, if you try the docs UI served by Uvicorn directly, without the path prefix in the URL, it won't work, because it expects to be accessed through the proxy.

You can check it at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs):

![image](https://fastapi.tiangolo.com/img/tutorial/behind-a-proxy/image01.png)

But if we access the docs UI at the "official" URL using the proxy with port `9999`, at `/api/v1/docs`, it works correctly! 🎉

You can check it at [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs):

![image](https://fastapi.tiangolo.com/img/tutorial/behind-a-proxy/image02.png)

Right as we wanted it. ✔️

This is because FastAPI uses this `root_path` to create the default `server` in OpenAPI with the URL provided by `root_path`.

## Additional servers¶

Warning

This is a more advanced use case. Feel free to skip it.

By default, **FastAPI** will create a `server` in the OpenAPI schema with the URL for the `root_path`.

But you can also provide other alternative `servers`, for example if you want *the same* docs UI to interact with both a staging and a production environment.

If you pass a custom list of `servers` and there's a `root_path` (because your API lives behind a proxy), **FastAPI** will insert a "server" with this `root_path` at the beginning of the list.

For example:

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI, Request

app = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path="/api/v1",
)

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

Will generate an OpenAPI schema like:

```
{
    "openapi": "3.1.0",
    // More stuff here
    "servers": [
        {
            "url": "/api/v1"
        },
        {
            "url": "https://stag.example.com",
            "description": "Staging environment"
        },
        {
            "url": "https://prod.example.com",
            "description": "Production environment"
        }
    ],
    "paths": {
            // More stuff here
    }
}
```

Tip

Notice the auto-generated server with a `url` value of `/api/v1`, taken from the `root_path`.

In the docs UI at [http://127.0.0.1:9999/api/v1/docs](http://127.0.0.1:9999/api/v1/docs) it would look like:

![image](https://fastapi.tiangolo.com/img/tutorial/behind-a-proxy/image03.png)

Tip

The docs UI will interact with the server that you select.

Technical Details

The `servers` property in the OpenAPI specification is optional.

If you don't specify the `servers` parameter and `root_path` is equal to `/`, the `servers` property in the generated OpenAPI schema will be omitted entirely by default, which is the equivalent of a single server with a `url` value of `/`.

### Disable automatic server fromroot_path¶

If you don't want **FastAPI** to include an automatic server using the `root_path`, you can use the parameter `root_path_in_servers=False`:

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI, Request

app = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path="/api/v1",
    root_path_in_servers=False,
)

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
```

and then it won't include it in the OpenAPI schema.

## Mounting a sub-application¶

If you need to mount a sub-application (as described in [Sub Applications - Mounts](https://fastapi.tiangolo.com/advanced/sub-applications/)) while also using a proxy with `root_path`, you can do it normally, as you would expect.

FastAPI will internally use the `root_path` smartly, so it will just work. ✨

---

# Custom Response

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Custom Response - HTML, Stream, File, others¶

By default, **FastAPI** will return the responses using `JSONResponse`.

You can override it by returning a `Response` directly as seen in [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/).

But if you return a `Response` directly (or any subclass, like `JSONResponse`), the data won't be automatically converted (even if you declare a `response_model`), and the documentation won't be automatically generated (for example, including the specific "media type", in the HTTP header `Content-Type` as part of the generated OpenAPI).

But you can also declare the `Response` that you want to be used (e.g. any `Response` subclass), in the *path operation decorator* using the `response_class` parameter.

The contents that you return from your *path operation function* will be put inside of that `Response`.

And if that `Response` has a JSON media type (`application/json`), like is the case with the `JSONResponse` and `UJSONResponse`, the data you return will be automatically converted (and filtered) with any Pydantic `response_model` that you declared in the *path operation decorator*.

Note

If you use a response class with no media type, FastAPI will expect your response to have no content, so it will not document the response format in its generated OpenAPI docs.

## UseORJSONResponse¶

For example, if you are squeezing performance, you can install and use [orjson](https://github.com/ijl/orjson) and set the response to be `ORJSONResponse`.

Import the `Response` class (sub-class) you want to use and declare it in the *path operation decorator*.

For large responses, returning a `Response` directly is much faster than returning a dictionary.

This is because by default, FastAPI will inspect every item inside and make sure it is serializable as JSON, using the same [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/) explained in the tutorial. This is what allows you to return **arbitrary objects**, for example database models.

But if you are certain that the content that you are returning is **serializable with JSON**, you can pass it directly to the response class and avoid the extra overhead that FastAPI would have by passing your return content through the `jsonable_encoder` before passing it to the response class.

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()

@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"item_id": "Foo"}])
```

Info

The parameter `response_class` will also be used to define the "media type" of the response.

In this case, the HTTP header `Content-Type` will be set to `application/json`.

And it will be documented as such in OpenAPI.

Tip

The `ORJSONResponse` is only available in FastAPI, not in Starlette.

## HTML Response¶

To return a response with HTML directly from **FastAPI**, use `HTMLResponse`.

- Import `HTMLResponse`.
- Pass `HTMLResponse` as the parameter `response_class` of your *path operation decorator*.

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
```

Info

The parameter `response_class` will also be used to define the "media type" of the response.

In this case, the HTTP header `Content-Type` will be set to `text/html`.

And it will be documented as such in OpenAPI.

### Return aResponse¶

As seen in [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/), you can also override the response directly in your *path operation*, by returning it.

The same example from above, returning an `HTMLResponse`, could look like:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

Warning

A `Response` returned directly by your *path operation function* won't be documented in OpenAPI (for example, the `Content-Type` won't be documented) and won't be visible in the automatic interactive docs.

Info

Of course, the actual `Content-Type` header, status code, etc, will come from the `Response` object you returned.

### Document in OpenAPI and overrideResponse¶

If you want to override the response from inside of the function but at the same time document the "media type" in OpenAPI, you can use the `response_class` parameter AND return a `Response` object.

The `response_class` will then be used only to document the OpenAPI *path operation*, but your `Response` will be used as is.

#### Return anHTMLResponsedirectly¶

For example, it could be something like:

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()
```

In this example, the function `generate_html_response()` already generates and returns a `Response` instead of returning the HTML in a `str`.

By returning the result of calling `generate_html_response()`, you are already returning a `Response` that will override the default **FastAPI** behavior.

But as you passed the `HTMLResponse` in the `response_class` too, **FastAPI** will know how to document it in OpenAPI and the interactive docs as HTML with `text/html`:

![image](https://fastapi.tiangolo.com/img/tutorial/custom-response/image01.png)

## Available responses¶

Here are some of the available responses.

Keep in mind that you can use `Response` to return anything else, or even create a custom sub-class.

Technical Details

You could also use `from starlette.responses import HTMLResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette.

### Response¶

The main `Response` class, all the other responses inherit from it.

You can return it directly.

It accepts the following parameters:

- `content` - A `str` or `bytes`.
- `status_code` - An `int` HTTP status code.
- `headers` - A `dict` of strings.
- `media_type` - A `str` giving the media type. E.g. `"text/html"`.

FastAPI (actually Starlette) will automatically include a Content-Length header. It will also include a Content-Type header, based on the `media_type` and appending a charset for text types.

 [Python 3.9+](#__tabbed_5_1)

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

### HTMLResponse¶

Takes some text or bytes and returns an HTML response, as you read above.

### PlainTextResponse¶

Takes some text or bytes and returns a plain text response.

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"
```

### JSONResponse¶

Takes some data and returns an `application/json` encoded response.

This is the default response used in **FastAPI**, as you read above.

### ORJSONResponse¶

A fast alternative JSON response using [orjson](https://github.com/ijl/orjson), as you read above.

Info

This requires installing `orjson` for example with `pip install orjson`.

### UJSONResponse¶

An alternative JSON response using [ujson](https://github.com/ultrajson/ultrajson).

Info

This requires installing `ujson` for example with `pip install ujson`.

Warning

`ujson` is less careful than Python's built-in implementation in how it handles some edge-cases.

  [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI
from fastapi.responses import UJSONResponse

app = FastAPI()

@app.get("/items/", response_class=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]
```

Tip

It's possible that `ORJSONResponse` might be a faster alternative.

### RedirectResponse¶

Returns an HTTP redirect. Uses a 307 status code (Temporary Redirect) by default.

You can return a `RedirectResponse` directly:

 [Python 3.9+](#__tabbed_8_1)

```
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")
```

---

Or you can use it in the `response_class` parameter:

 [Python 3.9+](#__tabbed_9_1)

```
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/fastapi", response_class=RedirectResponse)
async def redirect_fastapi():
    return "https://fastapi.tiangolo.com"
```

If you do that, then you can return the URL directly from your *path operation* function.

In this case, the `status_code` used will be the default one for the `RedirectResponse`, which is `307`.

---

You can also use the `status_code` parameter combined with the `response_class` parameter:

 [Python 3.9+](#__tabbed_10_1)

```
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return "https://docs.pydantic.dev/"
```

### StreamingResponse¶

Takes an async generator or a normal generator/iterator and streams the response body.

 [Python 3.9+](#__tabbed_11_1)

```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"

@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer())
```

#### UsingStreamingResponsewith file-like objects¶

If you have a [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) object (e.g. the object returned by `open()`), you can create a generator function to iterate over that file-like object.

That way, you don't have to read it all first in memory, and you can pass that generator function to the `StreamingResponse`, and return it.

This includes many libraries to interact with cloud storage, video processing, and others.

 [Python 3.9+](#__tabbed_12_1)

```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()

@app.get("/")
def main():
    def iterfile():  # (1)
        with open(some_file_path, mode="rb") as file_like:  # (2)
            yield from file_like  # (3)

    return StreamingResponse(iterfile(), media_type="video/mp4")
```

1. This is the generator function. It's a "generator function" because it contains `yield` statements inside.
2. By using a `with` block, we make sure that the file-like object is closed after the generator function is done. So, after it finishes sending the response.
3. This `yield from` tells the function to iterate over that thing named `file_like`. And then, for each part iterated, yield that part as coming from this generator function (`iterfile`).
  So, it is a generator function that transfers the "generating" work to something else internally.
  By doing it this way, we can put it in a `with` block, and that way, ensure that the file-like object is closed after finishing.

Tip

Notice that here as we are using standard `open()` that doesn't support `async` and `await`, we declare the path operation with normal `def`.

### FileResponse¶

Asynchronously streams a file as the response.

Takes a different set of arguments to instantiate than the other response types:

- `path` - The file path to the file to stream.
- `headers` - Any custom headers to include, as a dictionary.
- `media_type` - A string giving the media type. If unset, the filename or path will be used to infer a media type.
- `filename` - If set, this will be included in the response `Content-Disposition`.

File responses will include appropriate `Content-Length`, `Last-Modified` and `ETag` headers.

 [Python 3.9+](#__tabbed_13_1)

```
from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()

@app.get("/")
async def main():
    return FileResponse(some_file_path)
```

You can also use the `response_class` parameter:

 [Python 3.9+](#__tabbed_14_1)

```
from fastapi import FastAPI
from fastapi.responses import FileResponse

some_file_path = "large-video-file.mp4"
app = FastAPI()

@app.get("/", response_class=FileResponse)
async def main():
    return some_file_path
```

In this case, you can return the file path directly from your *path operation* function.

## Custom response class¶

You can create your own custom response class, inheriting from `Response` and using it.

For example, let's say that you want to use [orjson](https://github.com/ijl/orjson), but with some custom settings not used in the included `ORJSONResponse` class.

Let's say you want it to return indented and formatted JSON, so you want to use the orjson option `orjson.OPT_INDENT_2`.

You could create a `CustomORJSONResponse`. The main thing you have to do is create a `Response.render(content)` method that returns the content as `bytes`:

 [Python 3.9+](#__tabbed_15_1)

```
from typing import Any

import orjson
from fastapi import FastAPI, Response

app = FastAPI()

class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

@app.get("/", response_class=CustomORJSONResponse)
async def main():
    return {"message": "Hello World"}
```

Now instead of returning:

```
{"message": "Hello World"}
```

...this response will return:

```
{
  "message": "Hello World"
}
```

Of course, you will probably find much better ways to take advantage of this than formatting JSON. 😉

## Default response class¶

When creating a **FastAPI** class instance or an `APIRouter` you can specify which response class to use by default.

The parameter that defines this is `default_response_class`.

In the example below, **FastAPI** will use `ORJSONResponse` by default, in all *path operations*, instead of `JSONResponse`.

 [Python 3.9+](#__tabbed_16_1)

```
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]
```

Tip

You can still override `response_class` in *path operations* as before.

## Additional documentation¶

You can also declare the media type and many other details in OpenAPI using `responses`: [Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

---

# Using Dataclasses¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Using Dataclasses¶

FastAPI is built on top of **Pydantic**, and I have been showing you how to use Pydantic models to declare requests and responses.

But FastAPI also supports using [dataclasses](https://docs.python.org/3/library/dataclasses.html) the same way:

 [Python 3.10+](#__tabbed_1_1)

```
from dataclasses import dataclass

from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)

```
from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    description: Union[str, None] = None
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

This is still supported thanks to **Pydantic**, as it has [internal support fordataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel).

So, even with the code above that doesn't use Pydantic explicitly, FastAPI is using Pydantic to convert those standard dataclasses to Pydantic's own flavor of dataclasses.

And of course, it supports the same:

- data validation
- data serialization
- data documentation, etc.

This works the same way as with Pydantic models. And it is actually achieved in the same way underneath, using Pydantic.

Info

Keep in mind that dataclasses can't do everything Pydantic models can do.

So, you might still need to use Pydantic models.

But if you have a bunch of dataclasses laying around, this is a nice trick to use them to power a web API using FastAPI. 🤓

## Dataclasses inresponse_model¶

You can also use `dataclasses` in the `response_model` parameter:

 [Python 3.10+](#__tabbed_3_1)

```
from dataclasses import dataclass, field

from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    tax: float | None = None

app = FastAPI()

@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)

```
from dataclasses import dataclass, field
from typing import Union

from fastapi import FastAPI

@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None

app = FastAPI()

@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }
```

The dataclass will be automatically converted to a Pydantic dataclass.

This way, its schema will show up in the API docs user interface:

![image](https://fastapi.tiangolo.com/img/tutorial/dataclasses/image01.png)

## Dataclasses in Nested Data Structures¶

You can also combine `dataclasses` with other type annotations to make nested data structures.

In some cases, you might still have to use Pydantic's version of `dataclasses`. For example, if you have errors with the automatically generated API documentation.

In that case, you can simply swap the standard `dataclasses` with `pydantic.dataclasses`, which is a drop-in replacement:

 [Python 3.10+](#__tabbed_5_1)

```
from dataclasses import field  # (1)

from fastapi import FastAPI
from pydantic.dataclasses import dataclass  # (2)

@dataclass
class Item:
    name: str
    description: str | None = None

@dataclass
class Author:
    name: str
    items: list[Item] = field(default_factory=list)  # (3)

app = FastAPI()

@app.post("/authors/{author_id}/items/", response_model=Author)  # (4)
async def create_author_items(author_id: str, items: list[Item]):  # (5)
    return {"name": author_id, "items": items}  # (6)

@app.get("/authors/", response_model=list[Author])  # (7)
def get_authors():  # (8)
    return [  # (9)
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)

```
from dataclasses import field  # (1)
from typing import Union

from fastapi import FastAPI
from pydantic.dataclasses import dataclass  # (2)

@dataclass
class Item:
    name: str
    description: Union[str, None] = None

@dataclass
class Author:
    name: str
    items: list[Item] = field(default_factory=list)  # (3)

app = FastAPI()

@app.post("/authors/{author_id}/items/", response_model=Author)  # (4)
async def create_author_items(author_id: str, items: list[Item]):  # (5)
    return {"name": author_id, "items": items}  # (6)

@app.get("/authors/", response_model=list[Author])  # (7)
def get_authors():  # (8)
    return [  # (9)
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]
```

1. We still import `field` from standard `dataclasses`.
2. `pydantic.dataclasses` is a drop-in replacement for `dataclasses`.
3. The `Author` dataclass includes a list of `Item` dataclasses.
4. The `Author` dataclass is used as the `response_model` parameter.
5. You can use other standard type annotations with dataclasses as the request body.
  In this case, it's a list of `Item` dataclasses.
6. Here we are returning a dictionary that contains `items` which is a list of dataclasses.
  FastAPI is still capable of serializing the data to JSON.
7. Here the `response_model` is using a type annotation of a list of `Author` dataclasses.
  Again, you can combine `dataclasses` with standard type annotations.
8. Notice that this *path operation function* uses regular `def` instead of `async def`.
  As always, in FastAPI you can combine `def` and `async def` as needed.
  If you need a refresher about when to use which, check out the section *"In a hurry?"* in the docs about [asyncandawait](https://fastapi.tiangolo.com/async/#in-a-hurry).
9. This *path operation function* is not returning dataclasses (although it could), but a list of dictionaries with internal data.
  FastAPI will use the `response_model` parameter (that includes dataclasses) to convert the response.

You can combine `dataclasses` with other type annotations in many different combinations to form complex data structures.

Check the in-code annotation tips above to see more specific details.

## Learn More¶

You can also combine `dataclasses` with other Pydantic models, inherit from them, include them in your own models, etc.

To learn more, check the [Pydantic docs about dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/).

## Version¶

This is available since FastAPI version `0.67.0`. 🔖
