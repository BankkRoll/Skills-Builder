# HTTPConnectionclass¶ and more

# HTTPConnectionclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# HTTPConnectionclass¶

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

You can import it from `fastapi.requests`:

```
from fastapi.requests import HTTPConnection
```

## fastapi.requests.HTTPConnection¶

```
HTTPConnection(scope, receive=None)
```

Bases: `Mapping[str, Any]`

A base class for incoming HTTP connections, that is used to provide
any functionality that is common to both `Request` and `WebSocket`.

  Source code in `starlette/requests.py`

| 777879 | def__init__(self,scope:Scope,receive:Receive|None=None)->None:assertscope["type"]in("http","websocket")self.scope=scope |
| --- | --- |

### scopeinstance-attribute¶

```
scope = scope
```

### appproperty¶

```
app
```

### urlproperty¶

```
url
```

### base_urlproperty¶

```
base_url
```

### headersproperty¶

```
headers
```

### query_paramsproperty¶

```
query_params
```

### path_paramsproperty¶

```
path_params
```

### cookiesproperty¶

```
cookies
```

### clientproperty¶

```
client
```

### sessionproperty¶

```
session
```

### authproperty¶

```
auth
```

### userproperty¶

```
user
```

### stateproperty¶

```
state
```

### url_for¶

```
url_for(name, /, **path_params)
```

   Source code in `starlette/requests.py`

| 184185186187188189 | defurl_for(self,name:str,/,**path_params:Any)->URL:url_path_provider:Router|Starlette|None=self.scope.get("router")orself.scope.get("app")ifurl_path_providerisNone:raiseRuntimeError("The `url_for` method can only be used inside a Starlette application or with a router.")url_path=url_path_provider.url_path_for(name,**path_params)returnurl_path.make_absolute_url(base_url=self.base_url) |
| --- | --- |

---

# Middleware¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Middleware¶

There are several middlewares available provided by Starlette directly.

Read more about them in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

## fastapi.middleware.cors.CORSMiddleware¶

```
CORSMiddleware(
    app,
    allow_origins=(),
    allow_methods=("GET",),
    allow_headers=(),
    allow_credentials=False,
    allow_origin_regex=None,
    expose_headers=(),
    max_age=600,
)
```

   Source code in `starlette/middleware/cors.py`

| 16171819202122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273 | def__init__(self,app:ASGIApp,allow_origins:Sequence[str]=(),allow_methods:Sequence[str]=("GET",),allow_headers:Sequence[str]=(),allow_credentials:bool=False,allow_origin_regex:str|None=None,expose_headers:Sequence[str]=(),max_age:int=600,)->None:if"*"inallow_methods:allow_methods=ALL_METHODScompiled_allow_origin_regex=Noneifallow_origin_regexisnotNone:compiled_allow_origin_regex=re.compile(allow_origin_regex)allow_all_origins="*"inallow_originsallow_all_headers="*"inallow_headerspreflight_explicit_allow_origin=notallow_all_originsorallow_credentialssimple_headers={}ifallow_all_origins:simple_headers["Access-Control-Allow-Origin"]="*"ifallow_credentials:simple_headers["Access-Control-Allow-Credentials"]="true"ifexpose_headers:simple_headers["Access-Control-Expose-Headers"]=", ".join(expose_headers)preflight_headers={}ifpreflight_explicit_allow_origin:# The origin value will be set in preflight_response() if it is allowed.preflight_headers["Vary"]="Origin"else:preflight_headers["Access-Control-Allow-Origin"]="*"preflight_headers.update({"Access-Control-Allow-Methods":", ".join(allow_methods),"Access-Control-Max-Age":str(max_age),})allow_headers=sorted(SAFELISTED_HEADERS|set(allow_headers))ifallow_headersandnotallow_all_headers:preflight_headers["Access-Control-Allow-Headers"]=", ".join(allow_headers)ifallow_credentials:preflight_headers["Access-Control-Allow-Credentials"]="true"self.app=appself.allow_origins=allow_originsself.allow_methods=allow_methodsself.allow_headers=[h.lower()forhinallow_headers]self.allow_all_origins=allow_all_originsself.allow_all_headers=allow_all_headersself.preflight_explicit_allow_origin=preflight_explicit_allow_originself.allow_origin_regex=compiled_allow_origin_regexself.simple_headers=simple_headersself.preflight_headers=preflight_headers |
| --- | --- |

### appinstance-attribute¶

```
app = app
```

### allow_originsinstance-attribute¶

```
allow_origins = allow_origins
```

### allow_methodsinstance-attribute¶

```
allow_methods = allow_methods
```

### allow_headersinstance-attribute¶

```
allow_headers = [(lower()) for h in allow_headers]
```

### allow_all_originsinstance-attribute¶

```
allow_all_origins = allow_all_origins
```

### allow_all_headersinstance-attribute¶

```
allow_all_headers = allow_all_headers
```

### preflight_explicit_allow_origininstance-attribute¶

```
preflight_explicit_allow_origin = (
    preflight_explicit_allow_origin
)
```

### allow_origin_regexinstance-attribute¶

```
allow_origin_regex = compiled_allow_origin_regex
```

### simple_headersinstance-attribute¶

```
simple_headers = simple_headers
```

### preflight_headersinstance-attribute¶

```
preflight_headers = preflight_headers
```

### is_allowed_origin¶

```
is_allowed_origin(origin)
```

   Source code in `starlette/middleware/cors.py`

| 9596979899100101102 | defis_allowed_origin(self,origin:str)->bool:ifself.allow_all_origins:returnTrueifself.allow_origin_regexisnotNoneandself.allow_origin_regex.fullmatch(origin):returnTruereturnorigininself.allow_origins |
| --- | --- |

### preflight_response¶

```
preflight_response(request_headers)
```

   Source code in `starlette/middleware/cors.py`

| 104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140 | defpreflight_response(self,request_headers:Headers)->Response:requested_origin=request_headers["origin"]requested_method=request_headers["access-control-request-method"]requested_headers=request_headers.get("access-control-request-headers")headers=dict(self.preflight_headers)failures=[]ifself.is_allowed_origin(origin=requested_origin):ifself.preflight_explicit_allow_origin:# The "else" case is already accounted for in self.preflight_headers# and the value would be "*".headers["Access-Control-Allow-Origin"]=requested_originelse:failures.append("origin")ifrequested_methodnotinself.allow_methods:failures.append("method")# If we allow all headers, then we have to mirror back any requested# headers in the response.ifself.allow_all_headersandrequested_headersisnotNone:headers["Access-Control-Allow-Headers"]=requested_headerselifrequested_headersisnotNone:forheaderin[h.lower()forhinrequested_headers.split(",")]:ifheader.strip()notinself.allow_headers:failures.append("headers")break# We don't strictly need to use 400 responses here, since its up to# the browser to enforce the CORS policy, but its more informative# if we do.iffailures:failure_text="Disallowed CORS "+", ".join(failures)returnPlainTextResponse(failure_text,status_code=400,headers=headers)returnPlainTextResponse("OK",status_code=200,headers=headers) |
| --- | --- |

### simple_responseasync¶

```
simple_response(scope, receive, send, request_headers)
```

   Source code in `starlette/middleware/cors.py`

| 142143144 | asyncdefsimple_response(self,scope:Scope,receive:Receive,send:Send,request_headers:Headers)->None:send=functools.partial(self.send,send=send,request_headers=request_headers)awaitself.app(scope,receive,send) |
| --- | --- |

### sendasync¶

```
send(message, send, request_headers)
```

   Source code in `starlette/middleware/cors.py`

| 146147148149150151152153154155156157158159160161162163164165166167 | asyncdefsend(self,message:Message,send:Send,request_headers:Headers)->None:ifmessage["type"]!="http.response.start":awaitsend(message)returnmessage.setdefault("headers",[])headers=MutableHeaders(scope=message)headers.update(self.simple_headers)origin=request_headers["Origin"]has_cookie="cookie"inrequest_headers# If request includes any cookie headers, then we must respond# with the specific origin instead of '*'.ifself.allow_all_originsandhas_cookie:self.allow_explicit_origin(headers,origin)# If we only allow specific origins, then we have to mirror back# the Origin header in the response.elifnotself.allow_all_originsandself.is_allowed_origin(origin=origin):self.allow_explicit_origin(headers,origin)awaitsend(message) |
| --- | --- |

### allow_explicit_originstaticmethod¶

```
allow_explicit_origin(headers, origin)
```

   Source code in `starlette/middleware/cors.py`

| 169170171172 | @staticmethoddefallow_explicit_origin(headers:MutableHeaders,origin:str)->None:headers["Access-Control-Allow-Origin"]=originheaders.add_vary_header("Origin") |
| --- | --- |

It can be imported from `fastapi`:

```
from fastapi.middleware.cors import CORSMiddleware
```

## fastapi.middleware.gzip.GZipMiddleware¶

```
GZipMiddleware(app, minimum_size=500, compresslevel=9)
```

   Source code in `starlette/middleware/gzip.py`

| 12131415 | def__init__(self,app:ASGIApp,minimum_size:int=500,compresslevel:int=9)->None:self.app=appself.minimum_size=minimum_sizeself.compresslevel=compresslevel |
| --- | --- |

### appinstance-attribute¶

```
app = app
```

### minimum_sizeinstance-attribute¶

```
minimum_size = minimum_size
```

### compresslevelinstance-attribute¶

```
compresslevel = compresslevel
```

It can be imported from `fastapi`:

```
from fastapi.middleware.gzip import GZipMiddleware
```

## fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware¶

```
HTTPSRedirectMiddleware(app)
```

   Source code in `starlette/middleware/httpsredirect.py`

| 78 | def__init__(self,app:ASGIApp)->None:self.app=app |
| --- | --- |

### appinstance-attribute¶

```
app = app
```

It can be imported from `fastapi`:

```
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

## fastapi.middleware.trustedhost.TrustedHostMiddleware¶

```
TrustedHostMiddleware(
    app, allowed_hosts=None, www_redirect=True
)
```

   Source code in `starlette/middleware/trustedhost.py`

| 1314151617181920212223242526272829 | def__init__(self,app:ASGIApp,allowed_hosts:Sequence[str]|None=None,www_redirect:bool=True,)->None:ifallowed_hostsisNone:allowed_hosts=["*"]forpatterninallowed_hosts:assert"*"notinpattern[1:],ENFORCE_DOMAIN_WILDCARDifpattern.startswith("*")andpattern!="*":assertpattern.startswith("*."),ENFORCE_DOMAIN_WILDCARDself.app=appself.allowed_hosts=list(allowed_hosts)self.allow_any="*"inallowed_hostsself.www_redirect=www_redirect |
| --- | --- |

### appinstance-attribute¶

```
app = app
```

### allowed_hostsinstance-attribute¶

```
allowed_hosts = list(allowed_hosts)
```

### allow_anyinstance-attribute¶

```
allow_any = '*' in allowed_hosts
```

### www_redirectinstance-attribute¶

```
www_redirect = www_redirect
```

It can be imported from `fastapi`:

```
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```

## fastapi.middleware.wsgi.WSGIMiddleware¶

```
WSGIMiddleware(app)
```

   Source code in `starlette/middleware/wsgi.py`

| 7576 | def__init__(self,app:Callable[...,Any])->None:self.app=app |
| --- | --- |

### appinstance-attribute¶

```
app = app
```

It can be imported from `fastapi`:

```
from fastapi.middleware.wsgi import WSGIMiddleware
```

---

# OpenAPIdocs¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# OpenAPIdocs¶

Utilities to handle OpenAPI automatic UI documentation, including Swagger UI (by default at `/docs`) and ReDoc (by default at `/redoc`).

## fastapi.openapi.docs.get_swagger_ui_html¶

```
get_swagger_ui_html(
    *,
    openapi_url,
    title,
    swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url=None,
    init_oauth=None,
    swagger_ui_parameters=None
)
```

Generate and return the HTML  that loads Swagger UI for the interactive
API docs (normally served at `/docs`).

You would only call this function yourself if you needed to override some parts,
for example the URLs to use to load Swagger UI's JavaScript and CSS.

Read more about it in the
[FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| openapi_url | The OpenAPI URL that Swagger UI should load and use.This is normally done automatically by FastAPI using the default URL/openapi.json.TYPE:str |
| title | The HTML<title>content, normally shown in the browser tab.TYPE:str |
| swagger_js_url | The URL to use to load the Swagger UI JavaScript.It is normally set to a CDN URL.TYPE:strDEFAULT:'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js' |
| swagger_css_url | The URL to use to load the Swagger UI CSS.It is normally set to a CDN URL.TYPE:strDEFAULT:'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css' |
| swagger_favicon_url | The URL of the favicon to use. It is normally shown in the browser tab.TYPE:strDEFAULT:'https://fastapi.tiangolo.com/img/favicon.png' |
| oauth2_redirect_url | The OAuth2 redirect URL, it is normally automatically handled by FastAPI.TYPE:Optional[str]DEFAULT:None |
| init_oauth | A dictionary with Swagger UI OAuth2 initialization configurations.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| swagger_ui_parameters | Configuration parameters for Swagger UI.It defaults toswagger_ui_default_parameters.TYPE:Optional[dict[str,Any]]DEFAULT:None |

  Source code in `fastapi/openapi/docs.py`

| 2627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158 | defget_swagger_ui_html(*,openapi_url:Annotated[str,Doc("""The OpenAPI URL that Swagger UI should load and use.This is normally done automatically by FastAPI using the default URL`/openapi.json`."""),],title:Annotated[str,Doc("""The HTML `<title>` content, normally shown in the browser tab."""),],swagger_js_url:Annotated[str,Doc("""The URL to use to load the Swagger UI JavaScript.It is normally set to a CDN URL."""),]="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",swagger_css_url:Annotated[str,Doc("""The URL to use to load the Swagger UI CSS.It is normally set to a CDN URL."""),]="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",swagger_favicon_url:Annotated[str,Doc("""The URL of the favicon to use. It is normally shown in the browser tab."""),]="https://fastapi.tiangolo.com/img/favicon.png",oauth2_redirect_url:Annotated[Optional[str],Doc("""The OAuth2 redirect URL, it is normally automatically handled by FastAPI."""),]=None,init_oauth:Annotated[Optional[dict[str,Any]],Doc("""A dictionary with Swagger UI OAuth2 initialization configurations."""),]=None,swagger_ui_parameters:Annotated[Optional[dict[str,Any]],Doc("""Configuration parameters for Swagger UI.It defaults to [swagger_ui_default_parameters][fastapi.openapi.docs.swagger_ui_default_parameters]."""),]=None,)->HTMLResponse:"""Generate and return the HTML  that loads Swagger UI for the interactiveAPI docs (normally served at `/docs`).You would only call this function yourself if you needed to override some parts,for example the URLs to use to load Swagger UI's JavaScript and CSS.Read more about it in the[FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/)."""current_swagger_ui_parameters=swagger_ui_default_parameters.copy()ifswagger_ui_parameters:current_swagger_ui_parameters.update(swagger_ui_parameters)html=f"""<!DOCTYPE html><html><head><link type="text/css" rel="stylesheet" href="{swagger_css_url}"><link rel="shortcut icon" href="{swagger_favicon_url}"><title>{title}</title></head><body><div id="swagger-ui"></div><script src="{swagger_js_url}"></script><script>const ui = SwaggerUIBundle({{url: '{openapi_url}',"""forkey,valueincurrent_swagger_ui_parameters.items():html+=f"{json.dumps(key)}:{json.dumps(jsonable_encoder(value))},\n"ifoauth2_redirect_url:html+=f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"html+="""presets: [SwaggerUIBundle.presets.apis,SwaggerUIBundle.SwaggerUIStandalonePreset],})"""ifinit_oauth:html+=f"""ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})"""html+="""</script></body></html>"""returnHTMLResponse(html) |
| --- | --- |

## fastapi.openapi.docs.get_redoc_html¶

```
get_redoc_html(
    *,
    openapi_url,
    title,
    redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
    redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts=True
)
```

Generate and return the HTML response that loads ReDoc for the alternative
API docs (normally served at `/redoc`).

You would only call this function yourself if you needed to override some parts,
for example the URLs to use to load ReDoc's JavaScript and CSS.

Read more about it in the
[FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| openapi_url | The OpenAPI URL that ReDoc should load and use.This is normally done automatically by FastAPI using the default URL/openapi.json.TYPE:str |
| title | The HTML<title>content, normally shown in the browser tab.TYPE:str |
| redoc_js_url | The URL to use to load the ReDoc JavaScript.It is normally set to a CDN URL.TYPE:strDEFAULT:'https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js' |
| redoc_favicon_url | The URL of the favicon to use. It is normally shown in the browser tab.TYPE:strDEFAULT:'https://fastapi.tiangolo.com/img/favicon.png' |
| with_google_fonts | Load and use Google Fonts.TYPE:boolDEFAULT:True |

  Source code in `fastapi/openapi/docs.py`

| 161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253 | defget_redoc_html(*,openapi_url:Annotated[str,Doc("""The OpenAPI URL that ReDoc should load and use.This is normally done automatically by FastAPI using the default URL`/openapi.json`."""),],title:Annotated[str,Doc("""The HTML `<title>` content, normally shown in the browser tab."""),],redoc_js_url:Annotated[str,Doc("""The URL to use to load the ReDoc JavaScript.It is normally set to a CDN URL."""),]="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",redoc_favicon_url:Annotated[str,Doc("""The URL of the favicon to use. It is normally shown in the browser tab."""),]="https://fastapi.tiangolo.com/img/favicon.png",with_google_fonts:Annotated[bool,Doc("""Load and use Google Fonts."""),]=True,)->HTMLResponse:"""Generate and return the HTML response that loads ReDoc for the alternativeAPI docs (normally served at `/redoc`).You would only call this function yourself if you needed to override some parts,for example the URLs to use to load ReDoc's JavaScript and CSS.Read more about it in the[FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/)."""html=f"""<!DOCTYPE html><html><head><title>{title}</title><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1">"""ifwith_google_fonts:html+="""<link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">"""html+=f"""<link rel="shortcut icon" href="{redoc_favicon_url}"><style>body{{margin: 0;padding: 0;}}</style></head><body><noscript>ReDoc requires Javascript to function. Please enable it to browse the documentation.</noscript><redoc spec-url="{openapi_url}"></redoc><script src="{redoc_js_url}"> </script></body></html>"""returnHTMLResponse(html) |
| --- | --- |

## fastapi.openapi.docs.get_swagger_ui_oauth2_redirect_html¶

```
get_swagger_ui_oauth2_redirect_html()
```

Generate the HTML response with the OAuth2 redirection for Swagger UI.

You normally don't need to use or change this.

  Source code in `fastapi/openapi/docs.py`

| 256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342343344 | defget_swagger_ui_oauth2_redirect_html()->HTMLResponse:"""Generate the HTML response with the OAuth2 redirection for Swagger UI.You normally don't need to use or change this."""# copied from https://github.com/swagger-api/swagger-ui/blob/v4.14.0/dist/oauth2-redirect.htmlhtml="""<!doctype html><html lang="en-US"><head><title>Swagger UI: OAuth2 Redirect</title></head><body><script>'use strict';function run () {var oauth2 = window.opener.swaggerUIRedirectOauth2;var sentState = oauth2.state;var redirectUrl = oauth2.redirectUrl;var isValid, qp, arr;if (/code|token|error/.test(window.location.hash)) {qp = window.location.hash.substring(1).replace('?', '&');} else {qp = location.search.substring(1);}arr = qp.split("&");arr.forEach(function (v,i,_arr) { _arr[i] = '"' + v.replace('=', '":"') + '"';});qp = qp ? JSON.parse('{' + arr.join() + '}',function (key, value) {return key === "" ? value : decodeURIComponent(value);}) :{};isValid = qp.state === sentState;if ((oauth2.auth.schema.get("flow") === "accessCode" ||oauth2.auth.schema.get("flow") === "authorizationCode" ||oauth2.auth.schema.get("flow") === "authorization_code") && !oauth2.auth.code) {if (!isValid) {oauth2.errCb({authId: oauth2.auth.name,source: "auth",level: "warning",message: "Authorization may be unsafe, passed state was changed in server. The passed state wasn't returned from auth server."});}if (qp.code) {delete oauth2.state;oauth2.auth.code = qp.code;oauth2.callback({auth: oauth2.auth, redirectUrl: redirectUrl});} else {let oauthErrorMsg;if (qp.error) {oauthErrorMsg = "["+qp.error+"]: " +(qp.error_description ? qp.error_description+ ". " : "no accessCode received from the server. ") +(qp.error_uri ? "More info: "+qp.error_uri : "");}oauth2.errCb({authId: oauth2.auth.name,source: "auth",level: "error",message: oauthErrorMsg || "[Authorization failed]: no accessCode received from the server."});}} else {oauth2.callback({auth: oauth2.auth, token: qp, isValid: isValid, redirectUrl: redirectUrl});}window.close();}if (document.readyState !== 'loading') {run();} else {document.addEventListener('DOMContentLoaded', function () {run();});}</script></body></html>"""returnHTMLResponse(content=html) |
| --- | --- |

## fastapi.openapi.docs.swagger_ui_default_parametersmodule-attribute¶

```
swagger_ui_default_parameters = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}
```

Default configurations for Swagger UI.

You can use it as a template to add any other configurations needed.

---

# OpenAPImodels¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# OpenAPImodels¶

OpenAPI Pydantic models used to generate and validate the generated OpenAPI.

## fastapi.openapi.models¶

### SchemaTypemodule-attribute¶

```
SchemaType = Literal[
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
]
```

### SchemaOrBoolmodule-attribute¶

```
SchemaOrBool = Union[Schema, bool]
```

### SecuritySchememodule-attribute¶

```
SecurityScheme = Union[
    APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer
]
```

### BaseModelWithConfig¶

Bases: `BaseModel`

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Contact¶

Bases: `BaseModelWithConfig`

#### nameclass-attributeinstance-attribute¶

```
name = None
```

#### urlclass-attributeinstance-attribute¶

```
url = None
```

#### emailclass-attributeinstance-attribute¶

```
email = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### License¶

Bases: `BaseModelWithConfig`

#### nameinstance-attribute¶

```
name
```

#### identifierclass-attributeinstance-attribute¶

```
identifier = None
```

#### urlclass-attributeinstance-attribute¶

```
url = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Info¶

Bases: `BaseModelWithConfig`

#### titleinstance-attribute¶

```
title
```

#### summaryclass-attributeinstance-attribute¶

```
summary = None
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### termsOfServiceclass-attributeinstance-attribute¶

```
termsOfService = None
```

#### contactclass-attributeinstance-attribute¶

```
contact = None
```

#### licenseclass-attributeinstance-attribute¶

```
license = None
```

#### versioninstance-attribute¶

```
version
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### ServerVariable¶

Bases: `BaseModelWithConfig`

#### enumclass-attributeinstance-attribute¶

```
enum = None
```

#### defaultinstance-attribute¶

```
default
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Server¶

Bases: `BaseModelWithConfig`

#### urlinstance-attribute¶

```
url
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### variablesclass-attributeinstance-attribute¶

```
variables = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Reference¶

Bases: `BaseModel`

#### refclass-attributeinstance-attribute¶

```
ref = Field(alias='$ref')
```

### Discriminator¶

Bases: `BaseModel`

#### propertyNameinstance-attribute¶

```
propertyName
```

#### mappingclass-attributeinstance-attribute¶

```
mapping = None
```

### XML¶

Bases: `BaseModelWithConfig`

#### nameclass-attributeinstance-attribute¶

```
name = None
```

#### namespaceclass-attributeinstance-attribute¶

```
namespace = None
```

#### prefixclass-attributeinstance-attribute¶

```
prefix = None
```

#### attributeclass-attributeinstance-attribute¶

```
attribute = None
```

#### wrappedclass-attributeinstance-attribute¶

```
wrapped = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### ExternalDocumentation¶

Bases: `BaseModelWithConfig`

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### urlinstance-attribute¶

```
url
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Schema¶

Bases: `BaseModelWithConfig`

#### schema_class-attributeinstance-attribute¶

```
schema_ = Field(default=None, alias='$schema')
```

#### vocabularyclass-attributeinstance-attribute¶

```
vocabulary = Field(default=None, alias='$vocabulary')
```

#### idclass-attributeinstance-attribute¶

```
id = Field(default=None, alias='$id')
```

#### anchorclass-attributeinstance-attribute¶

```
anchor = Field(default=None, alias='$anchor')
```

#### dynamicAnchorclass-attributeinstance-attribute¶

```
dynamicAnchor = Field(default=None, alias='$dynamicAnchor')
```

#### refclass-attributeinstance-attribute¶

```
ref = Field(default=None, alias='$ref')
```

#### dynamicRefclass-attributeinstance-attribute¶

```
dynamicRef = Field(default=None, alias='$dynamicRef')
```

#### defsclass-attributeinstance-attribute¶

```
defs = Field(default=None, alias='$defs')
```

#### commentclass-attributeinstance-attribute¶

```
comment = Field(default=None, alias='$comment')
```

#### allOfclass-attributeinstance-attribute¶

```
allOf = None
```

#### anyOfclass-attributeinstance-attribute¶

```
anyOf = None
```

#### oneOfclass-attributeinstance-attribute¶

```
oneOf = None
```

#### not_class-attributeinstance-attribute¶

```
not_ = Field(default=None, alias='not')
```

#### if_class-attributeinstance-attribute¶

```
if_ = Field(default=None, alias='if')
```

#### thenclass-attributeinstance-attribute¶

```
then = None
```

#### else_class-attributeinstance-attribute¶

```
else_ = Field(default=None, alias='else')
```

#### dependentSchemasclass-attributeinstance-attribute¶

```
dependentSchemas = None
```

#### prefixItemsclass-attributeinstance-attribute¶

```
prefixItems = None
```

#### itemsclass-attributeinstance-attribute¶

```
items = None
```

#### containsclass-attributeinstance-attribute¶

```
contains = None
```

#### propertiesclass-attributeinstance-attribute¶

```
properties = None
```

#### patternPropertiesclass-attributeinstance-attribute¶

```
patternProperties = None
```

#### additionalPropertiesclass-attributeinstance-attribute¶

```
additionalProperties = None
```

#### propertyNamesclass-attributeinstance-attribute¶

```
propertyNames = None
```

#### unevaluatedItemsclass-attributeinstance-attribute¶

```
unevaluatedItems = None
```

#### unevaluatedPropertiesclass-attributeinstance-attribute¶

```
unevaluatedProperties = None
```

#### typeclass-attributeinstance-attribute¶

```
type = None
```

#### enumclass-attributeinstance-attribute¶

```
enum = None
```

#### constclass-attributeinstance-attribute¶

```
const = None
```

#### multipleOfclass-attributeinstance-attribute¶

```
multipleOf = Field(default=None, gt=0)
```

#### maximumclass-attributeinstance-attribute¶

```
maximum = None
```

#### exclusiveMaximumclass-attributeinstance-attribute¶

```
exclusiveMaximum = None
```

#### minimumclass-attributeinstance-attribute¶

```
minimum = None
```

#### exclusiveMinimumclass-attributeinstance-attribute¶

```
exclusiveMinimum = None
```

#### maxLengthclass-attributeinstance-attribute¶

```
maxLength = Field(default=None, ge=0)
```

#### minLengthclass-attributeinstance-attribute¶

```
minLength = Field(default=None, ge=0)
```

#### patternclass-attributeinstance-attribute¶

```
pattern = None
```

#### maxItemsclass-attributeinstance-attribute¶

```
maxItems = Field(default=None, ge=0)
```

#### minItemsclass-attributeinstance-attribute¶

```
minItems = Field(default=None, ge=0)
```

#### uniqueItemsclass-attributeinstance-attribute¶

```
uniqueItems = None
```

#### maxContainsclass-attributeinstance-attribute¶

```
maxContains = Field(default=None, ge=0)
```

#### minContainsclass-attributeinstance-attribute¶

```
minContains = Field(default=None, ge=0)
```

#### maxPropertiesclass-attributeinstance-attribute¶

```
maxProperties = Field(default=None, ge=0)
```

#### minPropertiesclass-attributeinstance-attribute¶

```
minProperties = Field(default=None, ge=0)
```

#### requiredclass-attributeinstance-attribute¶

```
required = None
```

#### dependentRequiredclass-attributeinstance-attribute¶

```
dependentRequired = None
```

#### formatclass-attributeinstance-attribute¶

```
format = None
```

#### contentEncodingclass-attributeinstance-attribute¶

```
contentEncoding = None
```

#### contentMediaTypeclass-attributeinstance-attribute¶

```
contentMediaType = None
```

#### contentSchemaclass-attributeinstance-attribute¶

```
contentSchema = None
```

#### titleclass-attributeinstance-attribute¶

```
title = None
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### defaultclass-attributeinstance-attribute¶

```
default = None
```

#### deprecatedclass-attributeinstance-attribute¶

```
deprecated = None
```

#### readOnlyclass-attributeinstance-attribute¶

```
readOnly = None
```

#### writeOnlyclass-attributeinstance-attribute¶

```
writeOnly = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### discriminatorclass-attributeinstance-attribute¶

```
discriminator = None
```

#### xmlclass-attributeinstance-attribute¶

```
xml = None
```

#### externalDocsclass-attributeinstance-attribute¶

```
externalDocs = None
```

#### exampleclass-attributeinstance-attribute¶

```
example = None
```

   Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Example¶

Bases: `TypedDict`

#### summaryinstance-attribute¶

```
summary
```

#### descriptioninstance-attribute¶

```
description
```

#### valueinstance-attribute¶

```
value
```

#### externalValueinstance-attribute¶

```
externalValue
```

### ParameterInType¶

Bases: `Enum`

#### queryclass-attributeinstance-attribute¶

```
query = 'query'
```

#### headerclass-attributeinstance-attribute¶

```
header = 'header'
```

#### pathclass-attributeinstance-attribute¶

```
path = 'path'
```

#### cookieclass-attributeinstance-attribute¶

```
cookie = 'cookie'
```

### Encoding¶

Bases: `BaseModelWithConfig`

#### contentTypeclass-attributeinstance-attribute¶

```
contentType = None
```

#### headersclass-attributeinstance-attribute¶

```
headers = None
```

#### styleclass-attributeinstance-attribute¶

```
style = None
```

#### explodeclass-attributeinstance-attribute¶

```
explode = None
```

#### allowReservedclass-attributeinstance-attribute¶

```
allowReserved = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### MediaType¶

Bases: `BaseModelWithConfig`

#### schema_class-attributeinstance-attribute¶

```
schema_ = Field(default=None, alias='schema')
```

#### exampleclass-attributeinstance-attribute¶

```
example = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### encodingclass-attributeinstance-attribute¶

```
encoding = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### ParameterBase¶

Bases: `BaseModelWithConfig`

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### requiredclass-attributeinstance-attribute¶

```
required = None
```

#### deprecatedclass-attributeinstance-attribute¶

```
deprecated = None
```

#### styleclass-attributeinstance-attribute¶

```
style = None
```

#### explodeclass-attributeinstance-attribute¶

```
explode = None
```

#### allowReservedclass-attributeinstance-attribute¶

```
allowReserved = None
```

#### schema_class-attributeinstance-attribute¶

```
schema_ = Field(default=None, alias='schema')
```

#### exampleclass-attributeinstance-attribute¶

```
example = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### contentclass-attributeinstance-attribute¶

```
content = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Parameter¶

Bases: `ParameterBase`

#### nameinstance-attribute¶

```
name
```

#### in_class-attributeinstance-attribute¶

```
in_ = Field(alias='in')
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### requiredclass-attributeinstance-attribute¶

```
required = None
```

#### deprecatedclass-attributeinstance-attribute¶

```
deprecated = None
```

#### styleclass-attributeinstance-attribute¶

```
style = None
```

#### explodeclass-attributeinstance-attribute¶

```
explode = None
```

#### allowReservedclass-attributeinstance-attribute¶

```
allowReserved = None
```

#### schema_class-attributeinstance-attribute¶

```
schema_ = Field(default=None, alias='schema')
```

#### exampleclass-attributeinstance-attribute¶

```
example = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### contentclass-attributeinstance-attribute¶

```
content = None
```

### Header¶

Bases: `ParameterBase`

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### requiredclass-attributeinstance-attribute¶

```
required = None
```

#### deprecatedclass-attributeinstance-attribute¶

```
deprecated = None
```

#### styleclass-attributeinstance-attribute¶

```
style = None
```

#### explodeclass-attributeinstance-attribute¶

```
explode = None
```

#### allowReservedclass-attributeinstance-attribute¶

```
allowReserved = None
```

#### schema_class-attributeinstance-attribute¶

```
schema_ = Field(default=None, alias='schema')
```

#### exampleclass-attributeinstance-attribute¶

```
example = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### contentclass-attributeinstance-attribute¶

```
content = None
```

### RequestBody¶

Bases: `BaseModelWithConfig`

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### contentinstance-attribute¶

```
content
```

#### requiredclass-attributeinstance-attribute¶

```
required = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Link¶

Bases: `BaseModelWithConfig`

#### operationRefclass-attributeinstance-attribute¶

```
operationRef = None
```

#### operationIdclass-attributeinstance-attribute¶

```
operationId = None
```

#### parametersclass-attributeinstance-attribute¶

```
parameters = None
```

#### requestBodyclass-attributeinstance-attribute¶

```
requestBody = None
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### serverclass-attributeinstance-attribute¶

```
server = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Response¶

Bases: `BaseModelWithConfig`

#### descriptioninstance-attribute¶

```
description
```

#### headersclass-attributeinstance-attribute¶

```
headers = None
```

#### contentclass-attributeinstance-attribute¶

```
content = None
```

#### linksclass-attributeinstance-attribute¶

```
links = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Operation¶

Bases: `BaseModelWithConfig`

#### tagsclass-attributeinstance-attribute¶

```
tags = None
```

#### summaryclass-attributeinstance-attribute¶

```
summary = None
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### externalDocsclass-attributeinstance-attribute¶

```
externalDocs = None
```

#### operationIdclass-attributeinstance-attribute¶

```
operationId = None
```

#### parametersclass-attributeinstance-attribute¶

```
parameters = None
```

#### requestBodyclass-attributeinstance-attribute¶

```
requestBody = None
```

#### responsesclass-attributeinstance-attribute¶

```
responses = None
```

#### callbacksclass-attributeinstance-attribute¶

```
callbacks = None
```

#### deprecatedclass-attributeinstance-attribute¶

```
deprecated = None
```

#### securityclass-attributeinstance-attribute¶

```
security = None
```

#### serversclass-attributeinstance-attribute¶

```
servers = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### PathItem¶

Bases: `BaseModelWithConfig`

#### refclass-attributeinstance-attribute¶

```
ref = Field(default=None, alias='$ref')
```

#### summaryclass-attributeinstance-attribute¶

```
summary = None
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### getclass-attributeinstance-attribute¶

```
get = None
```

#### putclass-attributeinstance-attribute¶

```
put = None
```

#### postclass-attributeinstance-attribute¶

```
post = None
```

#### deleteclass-attributeinstance-attribute¶

```
delete = None
```

#### optionsclass-attributeinstance-attribute¶

```
options = None
```

#### headclass-attributeinstance-attribute¶

```
head = None
```

#### patchclass-attributeinstance-attribute¶

```
patch = None
```

#### traceclass-attributeinstance-attribute¶

```
trace = None
```

#### serversclass-attributeinstance-attribute¶

```
servers = None
```

#### parametersclass-attributeinstance-attribute¶

```
parameters = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### SecuritySchemeType¶

Bases: `Enum`

#### apiKeyclass-attributeinstance-attribute¶

```
apiKey = 'apiKey'
```

#### httpclass-attributeinstance-attribute¶

```
http = 'http'
```

#### oauth2class-attributeinstance-attribute¶

```
oauth2 = 'oauth2'
```

#### openIdConnectclass-attributeinstance-attribute¶

```
openIdConnect = 'openIdConnect'
```

### SecurityBase¶

Bases: `BaseModelWithConfig`

#### type_class-attributeinstance-attribute¶

```
type_ = Field(alias='type')
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### APIKeyIn¶

Bases: `Enum`

#### queryclass-attributeinstance-attribute¶

```
query = 'query'
```

#### headerclass-attributeinstance-attribute¶

```
header = 'header'
```

#### cookieclass-attributeinstance-attribute¶

```
cookie = 'cookie'
```

### APIKey¶

Bases: `SecurityBase`

#### type_class-attributeinstance-attribute¶

```
type_ = Field(default=apiKey, alias='type')
```

#### in_class-attributeinstance-attribute¶

```
in_ = Field(alias='in')
```

#### nameinstance-attribute¶

```
name
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

### HTTPBase¶

Bases: `SecurityBase`

#### type_class-attributeinstance-attribute¶

```
type_ = Field(default=http, alias='type')
```

#### schemeinstance-attribute¶

```
scheme
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

### HTTPBearer¶

Bases: `HTTPBase`

#### schemeclass-attributeinstance-attribute¶

```
scheme = 'bearer'
```

#### bearerFormatclass-attributeinstance-attribute¶

```
bearerFormat = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### type_class-attributeinstance-attribute¶

```
type_ = Field(default=http, alias='type')
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

### OAuthFlow¶

Bases: `BaseModelWithConfig`

#### refreshUrlclass-attributeinstance-attribute¶

```
refreshUrl = None
```

#### scopesclass-attributeinstance-attribute¶

```
scopes = {}
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### OAuthFlowImplicit¶

Bases: `OAuthFlow`

#### authorizationUrlinstance-attribute¶

```
authorizationUrl
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### refreshUrlclass-attributeinstance-attribute¶

```
refreshUrl = None
```

#### scopesclass-attributeinstance-attribute¶

```
scopes = {}
```

### OAuthFlowPassword¶

Bases: `OAuthFlow`

#### tokenUrlinstance-attribute¶

```
tokenUrl
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### refreshUrlclass-attributeinstance-attribute¶

```
refreshUrl = None
```

#### scopesclass-attributeinstance-attribute¶

```
scopes = {}
```

### OAuthFlowClientCredentials¶

Bases: `OAuthFlow`

#### tokenUrlinstance-attribute¶

```
tokenUrl
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### refreshUrlclass-attributeinstance-attribute¶

```
refreshUrl = None
```

#### scopesclass-attributeinstance-attribute¶

```
scopes = {}
```

### OAuthFlowAuthorizationCode¶

Bases: `OAuthFlow`

#### authorizationUrlinstance-attribute¶

```
authorizationUrl
```

#### tokenUrlinstance-attribute¶

```
tokenUrl
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### refreshUrlclass-attributeinstance-attribute¶

```
refreshUrl = None
```

#### scopesclass-attributeinstance-attribute¶

```
scopes = {}
```

### OAuthFlows¶

Bases: `BaseModelWithConfig`

#### implicitclass-attributeinstance-attribute¶

```
implicit = None
```

#### passwordclass-attributeinstance-attribute¶

```
password = None
```

#### clientCredentialsclass-attributeinstance-attribute¶

```
clientCredentials = None
```

#### authorizationCodeclass-attributeinstance-attribute¶

```
authorizationCode = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### OAuth2¶

Bases: `SecurityBase`

#### type_class-attributeinstance-attribute¶

```
type_ = Field(default=oauth2, alias='type')
```

#### flowsinstance-attribute¶

```
flows
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

### OpenIdConnect¶

Bases: `SecurityBase`

#### type_class-attributeinstance-attribute¶

```
type_ = Field(default=openIdConnect, alias='type')
```

#### openIdConnectUrlinstance-attribute¶

```
openIdConnectUrl
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

### Components¶

Bases: `BaseModelWithConfig`

#### schemasclass-attributeinstance-attribute¶

```
schemas = None
```

#### responsesclass-attributeinstance-attribute¶

```
responses = None
```

#### parametersclass-attributeinstance-attribute¶

```
parameters = None
```

#### examplesclass-attributeinstance-attribute¶

```
examples = None
```

#### requestBodiesclass-attributeinstance-attribute¶

```
requestBodies = None
```

#### headersclass-attributeinstance-attribute¶

```
headers = None
```

#### securitySchemesclass-attributeinstance-attribute¶

```
securitySchemes = None
```

#### linksclass-attributeinstance-attribute¶

```
links = None
```

#### callbacksclass-attributeinstance-attribute¶

```
callbacks = None
```

#### pathItemsclass-attributeinstance-attribute¶

```
pathItems = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### Tag¶

Bases: `BaseModelWithConfig`

#### nameinstance-attribute¶

```
name
```

#### descriptionclass-attributeinstance-attribute¶

```
description = None
```

#### externalDocsclass-attributeinstance-attribute¶

```
externalDocs = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

### OpenAPI¶

Bases: `BaseModelWithConfig`

#### openapiinstance-attribute¶

```
openapi
```

#### infoinstance-attribute¶

```
info
```

#### jsonSchemaDialectclass-attributeinstance-attribute¶

```
jsonSchemaDialect = None
```

#### serversclass-attributeinstance-attribute¶

```
servers = None
```

#### pathsclass-attributeinstance-attribute¶

```
paths = None
```

#### webhooksclass-attributeinstance-attribute¶

```
webhooks = None
```

#### componentsclass-attributeinstance-attribute¶

```
components = None
```

#### securityclass-attributeinstance-attribute¶

```
security = None
```

#### tagsclass-attributeinstance-attribute¶

```
tags = None
```

#### externalDocsclass-attributeinstance-attribute¶

```
externalDocs = None
```

#### model_configclass-attributeinstance-attribute¶

```
model_config = {'extra': 'allow'}
```

---

# OpenAPI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# OpenAPI¶

There are several utilities to handle OpenAPI.

You normally don't need to use them unless you have a specific advanced use case that requires it.
