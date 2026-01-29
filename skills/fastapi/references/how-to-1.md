# Use Old 403 Authentication Error Status Codes¶ and more

# Use Old 403 Authentication Error Status Codes¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Use Old 403 Authentication Error Status Codes¶

Before FastAPI version `0.122.0`, when the integrated security utilities returned an error to the client after a failed authentication, they used the HTTP status code `403 Forbidden`.

Starting with FastAPI version `0.122.0`, they use the more appropriate HTTP status code `401 Unauthorized`, and return a sensible `WWW-Authenticate` header in the response, following the HTTP specifications, [RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235#section-3.1), [RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized).

But if for some reason your clients depend on the old behavior, you can revert to it by overriding the method `make_not_authenticated_error` in your security classes.

For example, you can create a subclass of `HTTPBearer` that returns a `403 Forbidden` error instead of the default `401 Unauthorized` error:

 [Python 3.9+](#__tabbed_1_1)

```
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()

class HTTPBearer403(HTTPBearer):
    def make_not_authenticated_error(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )

CredentialsDep = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer403())]

@app.get("/me")
def read_me(credentials: CredentialsDep):
    return {"message": "You are authenticated", "token": credentials.credentials}
```

Tip

Notice that the function returns the exception instance, it doesn't raise it. The raising is done in the rest of the internal code.

---

# Conditional OpenAPI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Conditional OpenAPI¶

If you needed to, you could use settings and environment variables to configure OpenAPI conditionally depending on the environment, and even disable it entirely.

## About security, APIs, and docs¶

Hiding your documentation user interfaces in production *shouldn't* be the way to protect your API.

That doesn't add any extra security to your API, the *path operations* will still be available where they are.

If there's a security flaw in your code, it will still exist.

Hiding the documentation just makes it more difficult to understand how to interact with your API, and could make it more difficult for you to debug it in production. It could be considered simply a form of [Security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity).

If you want to secure your API, there are several better things you can do, for example:

- Make sure you have well defined Pydantic models for your request bodies and responses.
- Configure any required permissions and roles using dependencies.
- Never store plaintext passwords, only password hashes.
- Implement and use well-known cryptographic tools, like pwdlib and JWT tokens, etc.
- Add more granular permission controls with OAuth2 scopes where needed.
- ...etc.

Nevertheless, you might have a very specific use case where you really need to disable the API docs for some environment (e.g. for production) or depending on configurations from environment variables.

## Conditional OpenAPI from settings and env vars¶

You can easily use the same Pydantic settings to configure your generated OpenAPI and the docs UIs.

For example:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"

settings = Settings()

app = FastAPI(openapi_url=settings.openapi_url)

@app.get("/")
def root():
    return {"message": "Hello World"}
```

Here we declare the setting `openapi_url` with the same default of `"/openapi.json"`.

And then we use it when creating the `FastAPI` app.

Then you could disable OpenAPI (including the UI docs) by setting the environment variable `OPENAPI_URL` to the empty string, like:

```
OPENAPI_URL= uvicorn main:app
```

Then if you go to the URLs at `/openapi.json`, `/docs`, or `/redoc` you will just get a `404 Not Found` error like:

```
{
    "detail": "Not Found"
}
```

---

# Configure Swagger UI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Configure Swagger UI¶

You can configure some extra [Swagger UI parameters](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/).

To configure them, pass the `swagger_ui_parameters` argument when creating the `FastAPI()` app object or to the `get_swagger_ui_html()` function.

`swagger_ui_parameters` receives a dictionary with the configurations passed to Swagger UI directly.

FastAPI converts the configurations to **JSON** to make them compatible with JavaScript, as that's what Swagger UI needs.

## Disable Syntax Highlighting¶

For example, you could disable syntax highlighting in Swagger UI.

Without changing the settings, syntax highlighting is enabled by default:

![image](https://fastapi.tiangolo.com/img/tutorial/extending-openapi/image02.png)

But you can disable it by setting `syntaxHighlight` to `False`:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

...and then Swagger UI won't show the syntax highlighting anymore:

![image](https://fastapi.tiangolo.com/img/tutorial/extending-openapi/image03.png)

## Change the Theme¶

The same way you could set the syntax highlighting theme with the key `"syntaxHighlight.theme"` (notice that it has a dot in the middle):

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

That configuration would change the syntax highlighting color theme:

![image](https://fastapi.tiangolo.com/img/tutorial/extending-openapi/image04.png)

## Change Default Swagger UI Parameters¶

FastAPI includes some default configuration parameters appropriate for most of the use cases.

It includes these default configurations:

 [Python 3.8+](#__tabbed_3_1)

```
# Code above omitted 👆

    dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.

        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}

# Code below omitted 👇
```

     👀 Full file preview [Python 3.8+](#__tabbed_4_1)

```
import json
from typing import Annotated, Any, Optional

from annotated_doc import Doc
from fastapi.encoders import jsonable_encoder
from starlette.responses import HTMLResponse

swagger_ui_default_parameters: Annotated[
    dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.

        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}

def get_swagger_ui_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that Swagger UI should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    swagger_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Annotated[
        Optional[str],
        Doc(
            """
            The OAuth2 redirect URL, it is normally automatically handled by FastAPI.
            """
        ),
    ] = None,
    init_oauth: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            A dictionary with Swagger UI OAuth2 initialization configurations.
            """
        ),
    ] = None,
    swagger_ui_parameters: Annotated[
        Optional[dict[str, Any]],
        Doc(
            """
            Configuration parameters for Swagger UI.

            It defaults to [swagger_ui_default_parameters][fastapi.openapi.docs.swagger_ui_default_parameters].
            """
        ),
    ] = None,
) -> HTMLResponse:
    """
    Generate and return the HTML  that loads Swagger UI for the interactive
    API docs (normally served at `/docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load Swagger UI's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
    and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

def get_redoc_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that ReDoc should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    redoc_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the ReDoc JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    redoc_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: Annotated[
        bool,
        Doc(
            """
            Load and use Google Fonts.
            """
        ),
    ] = True,
) -> HTMLResponse:
    """
    Generate and return the HTML response that loads ReDoc for the alternative
    API docs (normally served at `/redoc`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load ReDoc's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="{openapi_url}"></redoc>
    <script src="{redoc_js_url}"> </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

def get_swagger_ui_oauth2_redirect_html() -> HTMLResponse:
    """
    Generate the HTML response with the OAuth2 redirection for Swagger UI.

    You normally don't need to use or change this.
    """
    # copied from https://github.com/swagger-api/swagger-ui/blob/v4.14.0/dist/oauth2-redirect.html
    html = """
    <!doctype html>
    <html lang="en-US">
    <head>
        <title>Swagger UI: OAuth2 Redirect</title>
    </head>
    <body>
    <script>
        'use strict';
        function run () {
            var oauth2 = window.opener.swaggerUIRedirectOauth2;
            var sentState = oauth2.state;
            var redirectUrl = oauth2.redirectUrl;
            var isValid, qp, arr;

            if (/code|token|error/.test(window.location.hash)) {
                qp = window.location.hash.substring(1).replace('?', '&');
            } else {
                qp = location.search.substring(1);
            }

            arr = qp.split("&");
            arr.forEach(function (v,i,_arr) { _arr[i] = '"' + v.replace('=', '":"') + '"';});
            qp = qp ? JSON.parse('{' + arr.join() + '}',
                    function (key, value) {
                        return key === "" ? value : decodeURIComponent(value);
                    }
            ) : {};

            isValid = qp.state === sentState;

            if ((
              oauth2.auth.schema.get("flow") === "accessCode" ||
              oauth2.auth.schema.get("flow") === "authorizationCode" ||
              oauth2.auth.schema.get("flow") === "authorization_code"
            ) && !oauth2.auth.code) {
                if (!isValid) {
                    oauth2.errCb({
                        authId: oauth2.auth.name,
                        source: "auth",
                        level: "warning",
                        message: "Authorization may be unsafe, passed state was changed in server. The passed state wasn't returned from auth server."
                    });
                }

                if (qp.code) {
                    delete oauth2.state;
                    oauth2.auth.code = qp.code;
                    oauth2.callback({auth: oauth2.auth, redirectUrl: redirectUrl});
                } else {
                    let oauthErrorMsg;
                    if (qp.error) {
                        oauthErrorMsg = "["+qp.error+"]: " +
                            (qp.error_description ? qp.error_description+ ". " : "no accessCode received from the server. ") +
                            (qp.error_uri ? "More info: "+qp.error_uri : "");
                    }

                    oauth2.errCb({
                        authId: oauth2.auth.name,
                        source: "auth",
                        level: "error",
                        message: oauthErrorMsg || "[Authorization failed]: no accessCode received from the server."
                    });
                }
            } else {
                oauth2.callback({auth: oauth2.auth, token: qp, isValid: isValid, redirectUrl: redirectUrl});
            }
            window.close();
        }

        if (document.readyState !== 'loading') {
            run();
        } else {
            document.addEventListener('DOMContentLoaded', function () {
                run();
            });
        }
    </script>
    </body>
    </html>
        """
    return HTMLResponse(content=html)
```

You can override any of them by setting a different value in the argument `swagger_ui_parameters`.

For example, to disable `deepLinking` you could pass these settings to `swagger_ui_parameters`:

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"deepLinking": False})

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

## Other Swagger UI Parameters¶

To see all the other possible configurations you can use, read the official [docs for Swagger UI parameters](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/).

## JavaScript-only settings¶

Swagger UI also allows other configurations to be **JavaScript-only** objects (for example, JavaScript functions).

FastAPI also includes these JavaScript-only `presets` settings:

```
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

These are **JavaScript** objects, not strings, so you can't pass them from Python code directly.

If you need to use JavaScript-only configurations like those, you can use one of the methods above. Override all the Swagger UI *path operation* and manually write any JavaScript you need.

---

# Custom Docs UI Static Assets (Self

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Custom Docs UI Static Assets (Self-Hosting)¶

The API docs use **Swagger UI** and **ReDoc**, and each of those need some JavaScript and CSS files.

By default, those files are served from a CDN.

But it's possible to customize it, you can set a specific CDN, or serve the files yourself.

## Custom CDN for JavaScript and CSS¶

Let's say that you want to use a different CDN, for example you want to use `https://unpkg.com/`.

This could be useful if for example you live in a country that restricts some URLs.

### Disable the automatic docs¶

The first step is to disable the automatic docs, as by default, those use the default CDN.

To disable them, set their URLs to `None` when creating your `FastAPI` app:

 [Python 3.9+](#__tabbed_1_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Include the custom docs¶

Now you can create the *path operations* for the custom docs.

You can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:

- `openapi_url`: the URL where the HTML page for the docs can get the OpenAPI schema for your API. You can use here the attribute `app.openapi_url`.
- `title`: the title of your API.
- `oauth2_redirect_url`: you can use `app.swagger_ui_oauth2_redirect_url` here to use the default.
- `swagger_js_url`: the URL where the HTML for your Swagger UI docs can get the **JavaScript** file. This is the custom CDN URL.
- `swagger_css_url`: the URL where the HTML for your Swagger UI docs can get the **CSS** file. This is the custom CDN URL.

And similarly for ReDoc...

 [Python 3.9+](#__tabbed_2_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Tip

The *path operation* for `swagger_ui_redirect` is a helper for when you use OAuth2.

If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.

Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.

### Create apath operationto test it¶

Now, to be able to test that everything works, create a *path operation*:

 [Python 3.9+](#__tabbed_3_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2/bundles/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Test it¶

Now, you should be able to go to your docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), and reload the page, it will load those assets from the new CDN.

## Self-hosting JavaScript and CSS for docs¶

Self-hosting the JavaScript and CSS could be useful if, for example, you need your app to keep working even while offline, without open Internet access, or in a local network.

Here you'll see how to serve those files yourself, in the same FastAPI app, and configure the docs to use them.

### Project file structure¶

Let's say your project file structure looks like this:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Now create a directory to store those static files.

Your new file structure could look like this:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Download the files¶

Download the static files needed for the docs and put them on that `static/` directory.

You can probably right-click each link and select an option similar to "Save link as...".

**Swagger UI** uses the files:

- [swagger-ui-bundle.js](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js)
- [swagger-ui.css](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css)

And **ReDoc** uses the file:

- [redoc.standalone.js](https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js)

After that, your file structure could look like:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Serve the static files¶

- Import `StaticFiles`.
- "Mount" a `StaticFiles()` instance in a specific path.

 [Python 3.9+](#__tabbed_4_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Test the static files¶

Start your application and go to [http://127.0.0.1:8000/static/redoc.standalone.js](http://127.0.0.1:8000/static/redoc.standalone.js).

You should see a very long JavaScript file for **ReDoc**.

It could start with something like:

```
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

That confirms that you are being able to serve static files from your app, and that you placed the static files for the docs in the correct place.

Now we can configure the app to use those static files for the docs.

### Disable the automatic docs for static files¶

The same as when using a custom CDN, the first step is to disable the automatic docs, as those use the CDN by default.

To disable them, set their URLs to `None` when creating your `FastAPI` app:

 [Python 3.9+](#__tabbed_5_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Include the custom docs for static files¶

And the same way as with a custom CDN, now you can create the *path operations* for the custom docs.

Again, you can reuse FastAPI's internal functions to create the HTML pages for the docs, and pass them the needed arguments:

- `openapi_url`: the URL where the HTML page for the docs can get the OpenAPI schema for your API. You can use here the attribute `app.openapi_url`.
- `title`: the title of your API.
- `oauth2_redirect_url`: you can use `app.swagger_ui_oauth2_redirect_url` here to use the default.
- `swagger_js_url`: the URL where the HTML for your Swagger UI docs can get the **JavaScript** file. **This is the one that your own app is now serving**.
- `swagger_css_url`: the URL where the HTML for your Swagger UI docs can get the **CSS** file. **This is the one that your own app is now serving**.

And similarly for ReDoc...

 [Python 3.9+](#__tabbed_6_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

Tip

The *path operation* for `swagger_ui_redirect` is a helper for when you use OAuth2.

If you integrate your API with an OAuth2 provider, you will be able to authenticate and come back to the API docs with the acquired credentials. And interact with it using the real OAuth2 authentication.

Swagger UI will handle it behind the scenes for you, but it needs this "redirect" helper.

### Create apath operationto test static files¶

Now, to be able to test that everything works, create a *path operation*:

 [Python 3.9+](#__tabbed_7_1)

```
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Test Static Files UI¶

Now, you should be able to disconnect your WiFi, go to your docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), and reload the page.

And even without Internet, you would be able to see the docs for your API and interact with it.

---

# Custom Request and APIRoute class¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Custom Request and APIRoute class¶

In some cases, you may want to override the logic used by the `Request` and `APIRoute` classes.

In particular, this may be a good alternative to logic in a middleware.

For example, if you want to read or manipulate the request body before it is processed by your application.

Danger

This is an "advanced" feature.

If you are just starting with **FastAPI** you might want to skip this section.

## Use cases¶

Some use cases include:

- Converting non-JSON request bodies to JSON (e.g. [msgpack](https://msgpack.org/index.html)).
- Decompressing gzip-compressed request bodies.
- Automatically logging all request bodies.

## Handling custom request body encodings¶

Let's see how to make use of a custom `Request` subclass to decompress gzip requests.

And an `APIRoute` subclass to use that custom request class.

### Create a customGzipRequestclass¶

Tip

This is a toy example to demonstrate how it works, if you need Gzip support, you can use the provided [GzipMiddleware](https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware).

First, we create a `GzipRequest` class, which will overwrite the `Request.body()` method to decompress the body in the presence of an appropriate header.

If there's no `gzip` in the header, it will not try to decompress the body.

That way, the same route class can handle gzip compressed or uncompressed requests.

 [Python 3.10+](#__tabbed_1_1)

```
import gzip
from collections.abc import Callable
from typing import Annotated

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_2_1)[Python 3.10+ - non-Annotated](#__tabbed_2_2)[Python 3.9+ - non-Annotated](#__tabbed_2_3)

```
import gzip
from typing import Annotated, Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

Tip

Prefer to use the `Annotated` version if possible.

```
import gzip
from collections.abc import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

Tip

Prefer to use the `Annotated` version if possible.

```
import gzip
from typing import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

### Create a customGzipRouteclass¶

Next, we create a custom subclass of `fastapi.routing.APIRoute` that will make use of the `GzipRequest`.

This time, it will overwrite the method `APIRoute.get_route_handler()`.

This method returns a function. And that function is what will receive a request and return a response.

Here we use it to create a `GzipRequest` from the original request.

 [Python 3.10+](#__tabbed_3_1)

```
import gzip
from collections.abc import Callable
from typing import Annotated

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_4_1)[Python 3.10+ - non-Annotated](#__tabbed_4_2)[Python 3.9+ - non-Annotated](#__tabbed_4_3)

```
import gzip
from typing import Annotated, Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return {"sum": sum(numbers)}
```

Tip

Prefer to use the `Annotated` version if possible.

```
import gzip
from collections.abc import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

Tip

Prefer to use the `Annotated` version if possible.

```
import gzip
from typing import Callable

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler

app = FastAPI()
app.router.route_class = GzipRoute

@app.post("/sum")
async def sum_numbers(numbers: list[int] = Body()):
    return {"sum": sum(numbers)}
```

Technical Details

A `Request` has a `request.scope` attribute, that's just a Python `dict` containing the metadata related to the request.

A `Request` also has a `request.receive`, that's a function to "receive" the body of the request.

The `scope` `dict` and `receive` function are both part of the ASGI specification.

And those two things, `scope` and `receive`, are what is needed to create a new `Request` instance.

To learn more about the `Request` check [Starlette's docs about Requests](https://www.starlette.dev/requests/).

The only thing the function returned by `GzipRequest.get_route_handler` does differently is convert the `Request` to a `GzipRequest`.

Doing this, our `GzipRequest` will take care of decompressing the data (if necessary) before passing it to our *path operations*.

After that, all of the processing logic is the same.

But because of our changes in `GzipRequest.body`, the request body will be automatically decompressed when it is loaded by **FastAPI** when needed.

## Accessing the request body in an exception handler¶

Tip

To solve this same problem, it's probably a lot easier to use the `body` in a custom handler for `RequestValidationError` ([Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body)).

But this example is still valid and it shows how to interact with the internal components.

We can also use this same approach to access the request body in an exception handler.

All we need to do is handle the request inside a `try`/`except` block:

 [Python 3.10+](#__tabbed_5_1)

```
from collections.abc import Callable
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return sum(numbers)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_6_1)[Python 3.10+ - non-Annotated](#__tabbed_6_2)[Python 3.9+ - non-Annotated](#__tabbed_6_3)

```
from typing import Annotated, Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return sum(numbers)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from collections.abc import Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: list[int] = Body()):
    return sum(numbers)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: list[int] = Body()):
    return sum(numbers)
```

If an exception occurs, the`Request` instance will still be in scope, so we can read and make use of the request body when handling the error:

 [Python 3.10+](#__tabbed_7_1)

```
from collections.abc import Callable
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return sum(numbers)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_8_1)[Python 3.10+ - non-Annotated](#__tabbed_8_2)[Python 3.9+ - non-Annotated](#__tabbed_8_3)

```
from typing import Annotated, Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: Annotated[list[int], Body()]):
    return sum(numbers)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from collections.abc import Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: list[int] = Body()):
    return sum(numbers)
```

Tip

Prefer to use the `Annotated` version if possible.

```
from typing import Callable

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler

app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute

@app.post("/")
async def sum_numbers(numbers: list[int] = Body()):
    return sum(numbers)
```

## CustomAPIRouteclass in a router¶

You can also set the `route_class` parameter of an `APIRouter`:

 [Python 3.10+](#__tabbed_9_1)

```
import time
from collections.abc import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

app = FastAPI()
router = APIRouter(route_class=TimedRoute)

@app.get("/")
async def not_timed():
    return {"message": "Not timed"}

@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}

app.include_router(router)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_10_1)

```
import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

app = FastAPI()
router = APIRouter(route_class=TimedRoute)

@app.get("/")
async def not_timed():
    return {"message": "Not timed"}

@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}

app.include_router(router)
```

In this example, the *path operations* under the `router` will use the custom `TimedRoute` class, and will have an extra `X-Response-Time` header in the response with the time it took to generate the response:

 [Python 3.10+](#__tabbed_11_1)

```
import time
from collections.abc import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

app = FastAPI()
router = APIRouter(route_class=TimedRoute)

@app.get("/")
async def not_timed():
    return {"message": "Not timed"}

@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}

app.include_router(router)
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_12_1)

```
import time
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler

app = FastAPI()
router = APIRouter(route_class=TimedRoute)

@app.get("/")
async def not_timed():
    return {"message": "Not timed"}

@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}

app.include_router(router)
```
