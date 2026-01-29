# Static Files and more

# Static Files

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Static Files -StaticFiles¶

You can use the `StaticFiles` class to serve static files, like JavaScript, CSS, images, etc.

Read more about it in the [FastAPI docs for Static Files](https://fastapi.tiangolo.com/tutorial/static-files/).

You can import it directly from `fastapi.staticfiles`:

```
from fastapi.staticfiles import StaticFiles
```

## fastapi.staticfiles.StaticFiles¶

```
StaticFiles(
    *,
    directory=None,
    packages=None,
    html=False,
    check_dir=True,
    follow_symlink=False
)
```

   Source code in `starlette/staticfiles.py`

| 4041424344454647484950515253545556 | def__init__(self,*,directory:PathLike|None=None,packages:list[str|tuple[str,str]]|None=None,html:bool=False,check_dir:bool=True,follow_symlink:bool=False,)->None:self.directory=directoryself.packages=packagesself.all_directories=self.get_directories(directory,packages)self.html=htmlself.config_checked=Falseself.follow_symlink=follow_symlinkifcheck_diranddirectoryisnotNoneandnotos.path.isdir(directory):raiseRuntimeError(f"Directory '{directory}' does not exist") |
| --- | --- |

### directoryinstance-attribute¶

```
directory = directory
```

### packagesinstance-attribute¶

```
packages = packages
```

### all_directoriesinstance-attribute¶

```
all_directories = get_directories(directory, packages)
```

### htmlinstance-attribute¶

```
html = html
```

### config_checkedinstance-attribute¶

```
config_checked = False
```

### follow_symlinkinstance-attribute¶

```
follow_symlink = follow_symlink
```

### get_directories¶

```
get_directories(directory=None, packages=None)
```

Given `directory` and `packages` arguments, return a list of all the
directories that should be used for serving static files from.

  Source code in `starlette/staticfiles.py`

| 58596061626364656667686970717273747576777879808182838485 | defget_directories(self,directory:PathLike|None=None,packages:list[str|tuple[str,str]]|None=None,)->list[PathLike]:"""Given `directory` and `packages` arguments, return a list of all thedirectories that should be used for serving static files from."""directories=[]ifdirectoryisnotNone:directories.append(directory)forpackageinpackagesor[]:ifisinstance(package,tuple):package,statics_dir=packageelse:statics_dir="statics"spec=importlib.util.find_spec(package)assertspecisnotNone,f"Package{package!r}could not be found."assertspec.originisnotNone,f"Package{package!r}could not be found."package_directory=os.path.normpath(os.path.join(spec.origin,"..",statics_dir))assertos.path.isdir(package_directory),(f"Directory '{statics_dir!r}' in package{package!r}could not be found.")directories.append(package_directory)returndirectories |
| --- | --- |

### get_path¶

```
get_path(scope)
```

Given the ASGI scope, return the `path` string to serve up,
with OS specific path separators, and any '..', '.' components removed.

  Source code in `starlette/staticfiles.py`

| 101102103104105106107 | defget_path(self,scope:Scope)->str:"""Given the ASGI scope, return the `path` string to serve up,with OS specific path separators, and any '..', '.' components removed."""route_path=get_route_path(scope)returnos.path.normpath(os.path.join(*route_path.split("/"))) |
| --- | --- |

### get_responseasync¶

```
get_response(path, scope)
```

Returns an HTTP response, given the incoming path, method and request headers.

  Source code in `starlette/staticfiles.py`

| 109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149 | asyncdefget_response(self,path:str,scope:Scope)->Response:"""Returns an HTTP response, given the incoming path, method and request headers."""ifscope["method"]notin("GET","HEAD"):raiseHTTPException(status_code=405)try:full_path,stat_result=awaitanyio.to_thread.run_sync(self.lookup_path,path)exceptPermissionError:raiseHTTPException(status_code=401)exceptOSErrorasexc:# Filename is too long, so it can't be a valid static file.ifexc.errno==errno.ENAMETOOLONG:raiseHTTPException(status_code=404)raiseexcifstat_resultandstat.S_ISREG(stat_result.st_mode):# We have a static file to serve.returnself.file_response(full_path,stat_result,scope)elifstat_resultandstat.S_ISDIR(stat_result.st_mode)andself.html:# We're in HTML mode, and have got a directory URL.# Check if we have 'index.html' file to serve.index_path=os.path.join(path,"index.html")full_path,stat_result=awaitanyio.to_thread.run_sync(self.lookup_path,index_path)ifstat_resultisnotNoneandstat.S_ISREG(stat_result.st_mode):ifnotscope["path"].endswith("/"):# Directory URLs should redirect to always end in "/".url=URL(scope=scope)url=url.replace(path=url.path+"/")returnRedirectResponse(url=url)returnself.file_response(full_path,stat_result,scope)ifself.html:# Check for '404.html' if we're in HTML mode.full_path,stat_result=awaitanyio.to_thread.run_sync(self.lookup_path,"404.html")ifstat_resultandstat.S_ISREG(stat_result.st_mode):returnFileResponse(full_path,stat_result=stat_result,status_code=404)raiseHTTPException(status_code=404) |
| --- | --- |

### lookup_path¶

```
lookup_path(path)
```

   Source code in `starlette/staticfiles.py`

| 151152153154155156157158159160161162163164165166167 | deflookup_path(self,path:str)->tuple[str,os.stat_result|None]:fordirectoryinself.all_directories:joined_path=os.path.join(directory,path)ifself.follow_symlink:full_path=os.path.abspath(joined_path)directory=os.path.abspath(directory)else:full_path=os.path.realpath(joined_path)directory=os.path.realpath(directory)ifos.path.commonpath([full_path,directory])!=str(directory):# Don't allow misbehaving clients to break out of the static files directory.continuetry:returnfull_path,os.stat(full_path)except(FileNotFoundError,NotADirectoryError):continuereturn"",None |
| --- | --- |

### file_response¶

```
file_response(
    full_path, stat_result, scope, status_code=200
)
```

   Source code in `starlette/staticfiles.py`

| 169170171172173174175176177178179180181 | deffile_response(self,full_path:PathLike,stat_result:os.stat_result,scope:Scope,status_code:int=200,)->Response:request_headers=Headers(scope=scope)response=FileResponse(full_path,status_code=status_code,stat_result=stat_result)ifself.is_not_modified(response.headers,request_headers):returnNotModifiedResponse(response.headers)returnresponse |
| --- | --- |

### check_configasync¶

```
check_config()
```

Perform a one-off configuration check that StaticFiles is actually
pointed at a directory, so that we can raise loud errors rather than
just returning 404 responses.

  Source code in `starlette/staticfiles.py`

| 183184185186187188189190191192193194195196197 | asyncdefcheck_config(self)->None:"""Perform a one-off configuration check that StaticFiles is actuallypointed at a directory, so that we can raise loud errors rather thanjust returning 404 responses."""ifself.directoryisNone:returntry:stat_result=awaitanyio.to_thread.run_sync(os.stat,self.directory)exceptFileNotFoundError:raiseRuntimeError(f"StaticFiles directory '{self.directory}' does not exist.")ifnot(stat.S_ISDIR(stat_result.st_mode)orstat.S_ISLNK(stat_result.st_mode)):raiseRuntimeError(f"StaticFiles path '{self.directory}' is not a directory.") |
| --- | --- |

### is_not_modified¶

```
is_not_modified(response_headers, request_headers)
```

Given the request and response headers, return `True` if an HTTP
"Not Modified" response could be returned instead.

  Source code in `starlette/staticfiles.py`

| 199200201202203204205206207208209210211212213214215216217 | defis_not_modified(self,response_headers:Headers,request_headers:Headers)->bool:"""Given the request and response headers, return `True` if an HTTP"Not Modified" response could be returned instead."""ifif_none_match:=request_headers.get("if-none-match"):# The "etag" header is added by FileResponse, so it's always present.etag=response_headers["etag"]returnetagin[tag.strip(" W/")fortaginif_none_match.split(",")]try:if_modified_since=parsedate(request_headers["if-modified-since"])last_modified=parsedate(response_headers["last-modified"])ifif_modified_sinceisnotNoneandlast_modifiedisnotNoneandif_modified_since>=last_modified:returnTrueexceptKeyError:passreturnFalse |
| --- | --- |

---

# Status Codes¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Status Codes¶

You can import the `status` module from `fastapi`:

```
from fastapi import status
```

`status` is provided directly by Starlette.

It contains a group of named constants (variables) with integer status codes.

For example:

- 200: `status.HTTP_200_OK`
- 403: `status.HTTP_403_FORBIDDEN`
- etc.

It can be convenient to quickly access HTTP (and WebSocket) status codes in your app, using autocompletion for the name without having to remember the integer status codes by memory.

Read more about it in the [FastAPI docs about Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).

## Example¶

```
from fastapi import FastAPI, status

app = FastAPI()

@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

## fastapi.status¶

HTTP codes
See HTTP Status Code Registry:
https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

And RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110

### HTTP_100_CONTINUEmodule-attribute¶

```
HTTP_100_CONTINUE = 100
```

### HTTP_101_SWITCHING_PROTOCOLSmodule-attribute¶

```
HTTP_101_SWITCHING_PROTOCOLS = 101
```

### HTTP_102_PROCESSINGmodule-attribute¶

```
HTTP_102_PROCESSING = 102
```

### HTTP_103_EARLY_HINTSmodule-attribute¶

```
HTTP_103_EARLY_HINTS = 103
```

### HTTP_200_OKmodule-attribute¶

```
HTTP_200_OK = 200
```

### HTTP_201_CREATEDmodule-attribute¶

```
HTTP_201_CREATED = 201
```

### HTTP_202_ACCEPTEDmodule-attribute¶

```
HTTP_202_ACCEPTED = 202
```

### HTTP_203_NON_AUTHORITATIVE_INFORMATIONmodule-attribute¶

```
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
```

### HTTP_204_NO_CONTENTmodule-attribute¶

```
HTTP_204_NO_CONTENT = 204
```

### HTTP_205_RESET_CONTENTmodule-attribute¶

```
HTTP_205_RESET_CONTENT = 205
```

### HTTP_206_PARTIAL_CONTENTmodule-attribute¶

```
HTTP_206_PARTIAL_CONTENT = 206
```

### HTTP_207_MULTI_STATUSmodule-attribute¶

```
HTTP_207_MULTI_STATUS = 207
```

### HTTP_208_ALREADY_REPORTEDmodule-attribute¶

```
HTTP_208_ALREADY_REPORTED = 208
```

### HTTP_226_IM_USEDmodule-attribute¶

```
HTTP_226_IM_USED = 226
```

### HTTP_300_MULTIPLE_CHOICESmodule-attribute¶

```
HTTP_300_MULTIPLE_CHOICES = 300
```

### HTTP_301_MOVED_PERMANENTLYmodule-attribute¶

```
HTTP_301_MOVED_PERMANENTLY = 301
```

### HTTP_302_FOUNDmodule-attribute¶

```
HTTP_302_FOUND = 302
```

### HTTP_303_SEE_OTHERmodule-attribute¶

```
HTTP_303_SEE_OTHER = 303
```

### HTTP_304_NOT_MODIFIEDmodule-attribute¶

```
HTTP_304_NOT_MODIFIED = 304
```

### HTTP_305_USE_PROXYmodule-attribute¶

```
HTTP_305_USE_PROXY = 305
```

### HTTP_306_RESERVEDmodule-attribute¶

```
HTTP_306_RESERVED = 306
```

### HTTP_307_TEMPORARY_REDIRECTmodule-attribute¶

```
HTTP_307_TEMPORARY_REDIRECT = 307
```

### HTTP_308_PERMANENT_REDIRECTmodule-attribute¶

```
HTTP_308_PERMANENT_REDIRECT = 308
```

### HTTP_400_BAD_REQUESTmodule-attribute¶

```
HTTP_400_BAD_REQUEST = 400
```

### HTTP_401_UNAUTHORIZEDmodule-attribute¶

```
HTTP_401_UNAUTHORIZED = 401
```

### HTTP_402_PAYMENT_REQUIREDmodule-attribute¶

```
HTTP_402_PAYMENT_REQUIRED = 402
```

### HTTP_403_FORBIDDENmodule-attribute¶

```
HTTP_403_FORBIDDEN = 403
```

### HTTP_404_NOT_FOUNDmodule-attribute¶

```
HTTP_404_NOT_FOUND = 404
```

### HTTP_405_METHOD_NOT_ALLOWEDmodule-attribute¶

```
HTTP_405_METHOD_NOT_ALLOWED = 405
```

### HTTP_406_NOT_ACCEPTABLEmodule-attribute¶

```
HTTP_406_NOT_ACCEPTABLE = 406
```

### HTTP_407_PROXY_AUTHENTICATION_REQUIREDmodule-attribute¶

```
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
```

### HTTP_408_REQUEST_TIMEOUTmodule-attribute¶

```
HTTP_408_REQUEST_TIMEOUT = 408
```

### HTTP_409_CONFLICTmodule-attribute¶

```
HTTP_409_CONFLICT = 409
```

### HTTP_410_GONEmodule-attribute¶

```
HTTP_410_GONE = 410
```

### HTTP_411_LENGTH_REQUIREDmodule-attribute¶

```
HTTP_411_LENGTH_REQUIRED = 411
```

### HTTP_412_PRECONDITION_FAILEDmodule-attribute¶

```
HTTP_412_PRECONDITION_FAILED = 412
```

### HTTP_413_CONTENT_TOO_LARGEmodule-attribute¶

```
HTTP_413_CONTENT_TOO_LARGE = 413
```

### HTTP_414_URI_TOO_LONGmodule-attribute¶

```
HTTP_414_URI_TOO_LONG = 414
```

### HTTP_415_UNSUPPORTED_MEDIA_TYPEmodule-attribute¶

```
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
```

### HTTP_416_RANGE_NOT_SATISFIABLEmodule-attribute¶

```
HTTP_416_RANGE_NOT_SATISFIABLE = 416
```

### HTTP_417_EXPECTATION_FAILEDmodule-attribute¶

```
HTTP_417_EXPECTATION_FAILED = 417
```

### HTTP_418_IM_A_TEAPOTmodule-attribute¶

```
HTTP_418_IM_A_TEAPOT = 418
```

### HTTP_421_MISDIRECTED_REQUESTmodule-attribute¶

```
HTTP_421_MISDIRECTED_REQUEST = 421
```

### HTTP_422_UNPROCESSABLE_CONTENTmodule-attribute¶

```
HTTP_422_UNPROCESSABLE_CONTENT = 422
```

### HTTP_423_LOCKEDmodule-attribute¶

```
HTTP_423_LOCKED = 423
```

### HTTP_424_FAILED_DEPENDENCYmodule-attribute¶

```
HTTP_424_FAILED_DEPENDENCY = 424
```

### HTTP_425_TOO_EARLYmodule-attribute¶

```
HTTP_425_TOO_EARLY = 425
```

### HTTP_426_UPGRADE_REQUIREDmodule-attribute¶

```
HTTP_426_UPGRADE_REQUIRED = 426
```

### HTTP_428_PRECONDITION_REQUIREDmodule-attribute¶

```
HTTP_428_PRECONDITION_REQUIRED = 428
```

### HTTP_429_TOO_MANY_REQUESTSmodule-attribute¶

```
HTTP_429_TOO_MANY_REQUESTS = 429
```

### HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGEmodule-attribute¶

```
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
```

### HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONSmodule-attribute¶

```
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
```

### HTTP_500_INTERNAL_SERVER_ERRORmodule-attribute¶

```
HTTP_500_INTERNAL_SERVER_ERROR = 500
```

### HTTP_501_NOT_IMPLEMENTEDmodule-attribute¶

```
HTTP_501_NOT_IMPLEMENTED = 501
```

### HTTP_502_BAD_GATEWAYmodule-attribute¶

```
HTTP_502_BAD_GATEWAY = 502
```

### HTTP_503_SERVICE_UNAVAILABLEmodule-attribute¶

```
HTTP_503_SERVICE_UNAVAILABLE = 503
```

### HTTP_504_GATEWAY_TIMEOUTmodule-attribute¶

```
HTTP_504_GATEWAY_TIMEOUT = 504
```

### HTTP_505_HTTP_VERSION_NOT_SUPPORTEDmodule-attribute¶

```
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
```

### HTTP_506_VARIANT_ALSO_NEGOTIATESmodule-attribute¶

```
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
```

### HTTP_507_INSUFFICIENT_STORAGEmodule-attribute¶

```
HTTP_507_INSUFFICIENT_STORAGE = 507
```

### HTTP_508_LOOP_DETECTEDmodule-attribute¶

```
HTTP_508_LOOP_DETECTED = 508
```

### HTTP_510_NOT_EXTENDEDmodule-attribute¶

```
HTTP_510_NOT_EXTENDED = 510
```

### HTTP_511_NETWORK_AUTHENTICATION_REQUIREDmodule-attribute¶

```
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511
```

WebSocket codes
https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent

### WS_1000_NORMAL_CLOSUREmodule-attribute¶

```
WS_1000_NORMAL_CLOSURE = 1000
```

### WS_1001_GOING_AWAYmodule-attribute¶

```
WS_1001_GOING_AWAY = 1001
```

### WS_1002_PROTOCOL_ERRORmodule-attribute¶

```
WS_1002_PROTOCOL_ERROR = 1002
```

### WS_1003_UNSUPPORTED_DATAmodule-attribute¶

```
WS_1003_UNSUPPORTED_DATA = 1003
```

### WS_1005_NO_STATUS_RCVDmodule-attribute¶

```
WS_1005_NO_STATUS_RCVD = 1005
```

### WS_1006_ABNORMAL_CLOSUREmodule-attribute¶

```
WS_1006_ABNORMAL_CLOSURE = 1006
```

### WS_1007_INVALID_FRAME_PAYLOAD_DATAmodule-attribute¶

```
WS_1007_INVALID_FRAME_PAYLOAD_DATA = 1007
```

### WS_1008_POLICY_VIOLATIONmodule-attribute¶

```
WS_1008_POLICY_VIOLATION = 1008
```

### WS_1009_MESSAGE_TOO_BIGmodule-attribute¶

```
WS_1009_MESSAGE_TOO_BIG = 1009
```

### WS_1010_MANDATORY_EXTmodule-attribute¶

```
WS_1010_MANDATORY_EXT = 1010
```

### WS_1011_INTERNAL_ERRORmodule-attribute¶

```
WS_1011_INTERNAL_ERROR = 1011
```

### WS_1012_SERVICE_RESTARTmodule-attribute¶

```
WS_1012_SERVICE_RESTART = 1012
```

### WS_1013_TRY_AGAIN_LATERmodule-attribute¶

```
WS_1013_TRY_AGAIN_LATER = 1013
```

### WS_1014_BAD_GATEWAYmodule-attribute¶

```
WS_1014_BAD_GATEWAY = 1014
```

### WS_1015_TLS_HANDSHAKEmodule-attribute¶

```
WS_1015_TLS_HANDSHAKE = 1015
```

---

# Templating

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Templating -Jinja2Templates¶

You can use the `Jinja2Templates` class to render Jinja templates.

Read more about it in the [FastAPI docs for Templates](https://fastapi.tiangolo.com/advanced/templates/).

You can import it directly from `fastapi.templating`:

```
from fastapi.templating import Jinja2Templates
```

## fastapi.templating.Jinja2Templates¶

```
Jinja2Templates(
    directory: (
        str | PathLike[str] | Sequence[str | PathLike[str]]
    ),
    *,
    context_processors: (
        list[Callable[[Request], dict[str, Any]]] | None
    ) = None,
    **env_options: Any
)
```

```
Jinja2Templates(
    *,
    env: Environment,
    context_processors: (
        list[Callable[[Request], dict[str, Any]]] | None
    ) = None
)
```

```
Jinja2Templates(
    directory=None,
    *,
    context_processors=None,
    env=None,
    **env_options
)
```

templates = Jinja2Templates("templates")

return templates.TemplateResponse("index.html", {"request": request})

  Source code in `starlette/templating.py`

| 84858687888990919293949596979899100101102103104105 | def__init__(self,directory:str|PathLike[str]|Sequence[str|PathLike[str]]|None=None,*,context_processors:list[Callable[[Request],dict[str,Any]]]|None=None,env:jinja2.Environment|None=None,**env_options:Any,)->None:ifenv_options:warnings.warn("Extra environment options are deprecated. Use a preconfigured jinja2.Environment instead.",DeprecationWarning,)assertjinja2isnotNone,"jinja2 must be installed to use Jinja2Templates"assertbool(directory)^bool(env),"either 'directory' or 'env' arguments must be passed"self.context_processors=context_processorsor[]ifdirectoryisnotNone:self.env=self._create_env(directory,**env_options)elifenvisnotNone:# pragma: no branchself.env=envself._setup_env_defaults(self.env) |
| --- | --- |

### context_processorsinstance-attribute¶

```
context_processors = context_processors or []
```

### envinstance-attribute¶

```
env = _create_env(directory, **env_options)
```

### get_template¶

```
get_template(name)
```

   Source code in `starlette/templating.py`

| 131132 | defget_template(self,name:str)->jinja2.Template:returnself.env.get_template(name) |
| --- | --- |

### TemplateResponse¶

```
TemplateResponse(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> _TemplateResponse
```

```
TemplateResponse(
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> _TemplateResponse
```

```
TemplateResponse(*args, **kwargs)
```

   Source code in `starlette/templating.py`

| 159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217 | defTemplateResponse(self,*args:Any,**kwargs:Any)->_TemplateResponse:ifargs:ifisinstance(args[0],str):# the first argument is template name (old style)warnings.warn("The `name` is not the first parameter anymore. ""The first parameter should be the `Request` instance.\n"'Replace `TemplateResponse(name, {"request": request})` by `TemplateResponse(request, name)`.',DeprecationWarning,)name=args[0]context=args[1]iflen(args)>1elsekwargs.get("context",{})status_code=args[2]iflen(args)>2elsekwargs.get("status_code",200)headers=args[3]iflen(args)>3elsekwargs.get("headers")media_type=args[4]iflen(args)>4elsekwargs.get("media_type")background=args[5]iflen(args)>5elsekwargs.get("background")if"request"notincontext:raiseValueError('context must include a "request" key')request=context["request"]else:# the first argument is a request instance (new style)request=args[0]name=args[1]iflen(args)>1elsekwargs["name"]context=args[2]iflen(args)>2elsekwargs.get("context",{})status_code=args[3]iflen(args)>3elsekwargs.get("status_code",200)headers=args[4]iflen(args)>4elsekwargs.get("headers")media_type=args[5]iflen(args)>5elsekwargs.get("media_type")background=args[6]iflen(args)>6elsekwargs.get("background")else:# all arguments are kwargsif"request"notinkwargs:warnings.warn("The `TemplateResponse` now requires the `request` argument.\n"'Replace `TemplateResponse(name, {"context": context})` by `TemplateResponse(request, name)`.',DeprecationWarning,)if"request"notinkwargs.get("context",{}):raiseValueError('context must include a "request" key')context=kwargs.get("context",{})request=kwargs.get("request",context.get("request"))name=cast(str,kwargs["name"])status_code=kwargs.get("status_code",200)headers=kwargs.get("headers")media_type=kwargs.get("media_type")background=kwargs.get("background")context.setdefault("request",request)forcontext_processorinself.context_processors:context.update(context_processor(request))template=self.get_template(name)return_TemplateResponse(template,context,status_code=status_code,headers=headers,media_type=media_type,background=background,) |
| --- | --- |

---

# Test Client

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Test Client -TestClient¶

You can use the `TestClient` class to test FastAPI applications without creating an actual HTTP and socket connection, just communicating directly with the FastAPI code.

Read more about it in the [FastAPI docs for Testing](https://fastapi.tiangolo.com/tutorial/testing/).

You can import it directly from `fastapi.testclient`:

```
from fastapi.testclient import TestClient
```

## fastapi.testclient.TestClient¶

```
TestClient(
    app,
    base_url="http://testserver",
    raise_server_exceptions=True,
    root_path="",
    backend="asyncio",
    backend_options=None,
    cookies=None,
    headers=None,
    follow_redirects=True,
    client=("testclient", 50000),
)
```

Bases: `Client`

  Source code in `starlette/testclient.py`

| 373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411 | def__init__(self,app:ASGIApp,base_url:str="http://testserver",raise_server_exceptions:bool=True,root_path:str="",backend:Literal["asyncio","trio"]="asyncio",backend_options:dict[str,Any]|None=None,cookies:httpx._types.CookieTypes|None=None,headers:dict[str,str]|None=None,follow_redirects:bool=True,client:tuple[str,int]=("testclient",50000),)->None:self.async_backend=_AsyncBackend(backend=backend,backend_options=backend_optionsor{})if_is_asgi3(app):asgi_app=appelse:app=cast(ASGI2App,app)# type: ignore[assignment]asgi_app=_WrapASGI2(app)# type: ignore[arg-type]self.app=asgi_appself.app_state:dict[str,Any]={}transport=_TestClientTransport(self.app,portal_factory=self._portal_factory,raise_server_exceptions=raise_server_exceptions,root_path=root_path,app_state=self.app_state,client=client,)ifheadersisNone:headers={}headers.setdefault("user-agent","testclient")super().__init__(base_url=base_url,headers=headers,transport=transport,follow_redirects=follow_redirects,cookies=cookies,) |
| --- | --- |

### headerspropertywritable¶

```
headers
```

HTTP headers to include when sending requests.

### follow_redirectsinstance-attribute¶

```
follow_redirects = follow_redirects
```

### max_redirectsinstance-attribute¶

```
max_redirects = max_redirects
```

### is_closedproperty¶

```
is_closed
```

Check if the client being closed

### trust_envproperty¶

```
trust_env
```

### timeoutpropertywritable¶

```
timeout
```

### event_hookspropertywritable¶

```
event_hooks
```

### authpropertywritable¶

```
auth
```

Authentication class used when none is passed at the request-level.

See also [Authentication](https://fastapi.tiangolo.com/quickstart/#authentication).

### base_urlpropertywritable¶

```
base_url
```

Base URL to use when sending requests with relative URLs.

### cookiespropertywritable¶

```
cookies
```

Cookie values to include when sending requests.

### paramspropertywritable¶

```
params
```

Query parameters to include in the URL when sending requests.

### taskinstance-attribute¶

```
task
```

### portalclass-attributeinstance-attribute¶

```
portal = None
```

### async_backendinstance-attribute¶

```
async_backend = _AsyncBackend(
    backend=backend, backend_options=backend_options or {}
)
```

### appinstance-attribute¶

```
app = asgi_app
```

### app_stateinstance-attribute¶

```
app_state = {}
```

### build_request¶

```
build_request(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Build and return a request instance.

- The `params`, `headers` and `cookies` arguments
  are merged with any values set on the client.
- The `url` argument is merged with any `base_url` set on the client.

See also: [Request instances](https://fastapi.tiangolo.com/advanced/clients/#request-instances)

  Source code in `httpx/_client.py`

| 340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389 | defbuild_request(self,method:str,url:URL|str,*,content:RequestContent|None=None,data:RequestData|None=None,files:RequestFiles|None=None,json:typing.Any|None=None,params:QueryParamTypes|None=None,headers:HeaderTypes|None=None,cookies:CookieTypes|None=None,timeout:TimeoutTypes|UseClientDefault=USE_CLIENT_DEFAULT,extensions:RequestExtensions|None=None,)->Request:"""Build and return a request instance.* The `params`, `headers` and `cookies` argumentsare merged with any values set on the client.* The `url` argument is merged with any `base_url` set on the client.See also: [Request instances][0][0]: /advanced/clients/#request-instances"""url=self._merge_url(url)headers=self._merge_headers(headers)cookies=self._merge_cookies(cookies)params=self._merge_queryparams(params)extensions={}ifextensionsisNoneelseextensionsif"timeout"notinextensions:timeout=(self.timeoutifisinstance(timeout,UseClientDefault)elseTimeout(timeout))extensions=dict(**extensions,timeout=timeout.as_dict())returnRequest(method,url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,extensions=extensions,) |
| --- | --- |

### stream¶

```
stream(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Alternative to `httpx.request()` that streams the response body
instead of loading it into memory at once.

**Parameters**: See `httpx.request`.

See also: [Streaming Responses](https://fastapi.tiangolo.com/quickstart#streaming-responses)

  Source code in `httpx/_client.py`

| 827828829830831832833834835836837838839840841842843844845846847848849850851852853854855856857858859860861862863864865866867868869870871872873874875876877 | @contextmanagerdefstream(self,method:str,url:URL|str,*,content:RequestContent|None=None,data:RequestData|None=None,files:RequestFiles|None=None,json:typing.Any|None=None,params:QueryParamTypes|None=None,headers:HeaderTypes|None=None,cookies:CookieTypes|None=None,auth:AuthTypes|UseClientDefault|None=USE_CLIENT_DEFAULT,follow_redirects:bool|UseClientDefault=USE_CLIENT_DEFAULT,timeout:TimeoutTypes|UseClientDefault=USE_CLIENT_DEFAULT,extensions:RequestExtensions|None=None,)->typing.Iterator[Response]:"""Alternative to `httpx.request()` that streams the response bodyinstead of loading it into memory at once.**Parameters**: See `httpx.request`.See also: [Streaming Responses][0][0]: /quickstart#streaming-responses"""request=self.build_request(method=method,url=url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,timeout=timeout,extensions=extensions,)response=self.send(request=request,auth=auth,follow_redirects=follow_redirects,stream=True,)try:yieldresponsefinally:response.close() |
| --- | --- |

### send¶

```
send(
    request,
    *,
    stream=False,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT
)
```

Send a request.

The request is sent as-is, unmodified.

Typically you'll want to build one with `Client.build_request()`
so that any client-level configuration is merged into the request,
but passing an explicit `httpx.Request()` is supported as well.

See also: [Request instances](https://fastapi.tiangolo.com/advanced/clients/#request-instances)

  Source code in `httpx/_client.py`

| 879880881882883884885886887888889890891892893894895896897898899900901902903904905906907908909910911912913914915916917918919920921922923924925926927928 | defsend(self,request:Request,*,stream:bool=False,auth:AuthTypes|UseClientDefault|None=USE_CLIENT_DEFAULT,follow_redirects:bool|UseClientDefault=USE_CLIENT_DEFAULT,)->Response:"""Send a request.The request is sent as-is, unmodified.Typically you'll want to build one with `Client.build_request()`so that any client-level configuration is merged into the request,but passing an explicit `httpx.Request()` is supported as well.See also: [Request instances][0][0]: /advanced/clients/#request-instances"""ifself._state==ClientState.CLOSED:raiseRuntimeError("Cannot send a request, as the client has been closed.")self._state=ClientState.OPENEDfollow_redirects=(self.follow_redirectsifisinstance(follow_redirects,UseClientDefault)elsefollow_redirects)self._set_timeout(request)auth=self._build_request_auth(request,auth)response=self._send_handling_auth(request,auth=auth,follow_redirects=follow_redirects,history=[],)try:ifnotstream:response.read()returnresponseexceptBaseExceptionasexc:response.close()raiseexc |
| --- | --- |

### close¶

```
close()
```

Close transport and proxies.

  Source code in `httpx/_client.py`

| 12631264126512661267126812691270127112721273 | defclose(self)->None:"""Close transport and proxies."""ifself._state!=ClientState.CLOSED:self._state=ClientState.CLOSEDself._transport.close()fortransportinself._mounts.values():iftransportisnotNone:transport.close() |
| --- | --- |

### request¶

```
request(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456457458459 | defrequest(# type: ignore[override]self,method:str,url:httpx._types.URLTypes,*,content:httpx._types.RequestContent|None=None,data:_RequestData|None=None,files:httpx._types.RequestFiles|None=None,json:Any=None,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:iftimeoutisnothttpx.USE_CLIENT_DEFAULT:warnings.warn("You should not use the 'timeout' argument with the TestClient. ""See https://github.com/Kludex/starlette/issues/1108 for more information.",DeprecationWarning,)url=self._merge_url(url)returnsuper().request(method,url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### get¶

```
get(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 461462463464465466467468469470471472473474475476477478479480481482 | defget(# type: ignore[override]self,url:httpx._types.URLTypes,*,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().get(url,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### options¶

```
options(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 484485486487488489490491492493494495496497498499500501502503504505 | defoptions(# type: ignore[override]self,url:httpx._types.URLTypes,*,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().options(url,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### head¶

```
head(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 507508509510511512513514515516517518519520521522523524525526527528 | defhead(# type: ignore[override]self,url:httpx._types.URLTypes,*,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().head(url,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### post¶

```
post(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 530531532533534535536537538539540541542543544545546547548549550551552553554555556557558559 | defpost(# type: ignore[override]self,url:httpx._types.URLTypes,*,content:httpx._types.RequestContent|None=None,data:_RequestData|None=None,files:httpx._types.RequestFiles|None=None,json:Any=None,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().post(url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### put¶

```
put(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 561562563564565566567568569570571572573574575576577578579580581582583584585586587588589590 | defput(# type: ignore[override]self,url:httpx._types.URLTypes,*,content:httpx._types.RequestContent|None=None,data:_RequestData|None=None,files:httpx._types.RequestFiles|None=None,json:Any=None,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().put(url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### patch¶

```
patch(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 592593594595596597598599600601602603604605606607608609610611612613614615616617618619620621 | defpatch(# type: ignore[override]self,url:httpx._types.URLTypes,*,content:httpx._types.RequestContent|None=None,data:_RequestData|None=None,files:httpx._types.RequestFiles|None=None,json:Any=None,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().patch(url,content=content,data=data,files=files,json=json,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### delete¶

```
delete(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

   Source code in `starlette/testclient.py`

| 623624625626627628629630631632633634635636637638639640641642643644 | defdelete(# type: ignore[override]self,url:httpx._types.URLTypes,*,params:httpx._types.QueryParamTypes|None=None,headers:httpx._types.HeaderTypes|None=None,cookies:httpx._types.CookieTypes|None=None,auth:httpx._types.AuthTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,follow_redirects:bool|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,timeout:httpx._types.TimeoutTypes|httpx._client.UseClientDefault=httpx._client.USE_CLIENT_DEFAULT,extensions:dict[str,Any]|None=None,)->httpx.Response:returnsuper().delete(url,params=params,headers=headers,cookies=cookies,auth=auth,follow_redirects=follow_redirects,timeout=timeout,extensions=extensions,) |
| --- | --- |

### websocket_connect¶

```
websocket_connect(url, subprotocols=None, **kwargs)
```

   Source code in `starlette/testclient.py`

| 646647648649650651652653654655656657658659660661662663664665666667 | defwebsocket_connect(self,url:str,subprotocols:Sequence[str]|None=None,**kwargs:Any,)->WebSocketTestSession:url=urljoin("ws://testserver",url)headers=kwargs.get("headers",{})headers.setdefault("connection","upgrade")headers.setdefault("sec-websocket-key","testserver==")headers.setdefault("sec-websocket-version","13")ifsubprotocolsisnotNone:headers.setdefault("sec-websocket-protocol",", ".join(subprotocols))kwargs["headers"]=headerstry:super().request("GET",url,**kwargs)except_Upgradeasexc:session=exc.sessionelse:raiseRuntimeError("Expected WebSocket upgrade")# pragma: no coverreturnsession |
| --- | --- |

### lifespanasync¶

```
lifespan()
```

   Source code in `starlette/testclient.py`

| 701702703704705706 | asyncdeflifespan(self)->None:scope={"type":"lifespan","state":self.app_state}try:awaitself.app(scope,self.stream_receive.receive,self.stream_send.send)finally:awaitself.stream_send.send(None) |
| --- | --- |

### wait_startupasync¶

```
wait_startup()
```

   Source code in `starlette/testclient.py`

| 708709710711712713714715716717718719720721722723 | asyncdefwait_startup(self)->None:awaitself.stream_receive.send({"type":"lifespan.startup"})asyncdefreceive()->Any:message=awaitself.stream_send.receive()ifmessageisNone:self.task.result()returnmessagemessage=awaitreceive()assertmessage["type"]in("lifespan.startup.complete","lifespan.startup.failed",)ifmessage["type"]=="lifespan.startup.failed":awaitreceive() |
| --- | --- |

### wait_shutdownasync¶

```
wait_shutdown()
```

   Source code in `starlette/testclient.py`

| 725726727728729730731732733734735736737738739 | asyncdefwait_shutdown(self)->None:asyncdefreceive()->Any:message=awaitself.stream_send.receive()ifmessageisNone:self.task.result()returnmessageawaitself.stream_receive.send({"type":"lifespan.shutdown"})message=awaitreceive()assertmessage["type"]in("lifespan.shutdown.complete","lifespan.shutdown.failed",)ifmessage["type"]=="lifespan.shutdown.failed":awaitreceive() |
| --- | --- |

---

# UploadFileclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# UploadFileclass¶

You can define *path operation function* parameters to be of the type `UploadFile` to receive files from the request.

You can import it directly from `fastapi`:

```
from fastapi import UploadFile
```

## fastapi.UploadFile¶

```
UploadFile(file, *, size=None, filename=None, headers=None)
```

Bases: `UploadFile`

A file uploaded in a request.

Define it as a *path operation function* (or dependency) parameter.

If you are using a regular `def` function, you can use the `upload_file.file`
attribute to access the raw standard Python file (blocking, not async), useful and
needed for non-async code.

Read more about it in the
[FastAPI docs for Request Files](https://fastapi.tiangolo.com/tutorial/request-files/).

#### Example¶

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

  Source code in `starlette/datastructures.py`

| 417418419420421422423424425426427428429430431432 | def__init__(self,file:BinaryIO,*,size:int|None=None,filename:str|None=None,headers:Headers|None=None,)->None:self.filename=filenameself.file=fileself.size=sizeself.headers=headersorHeaders()# Capture max size from SpooledTemporaryFile if one is provided. This slightly speeds up future checks.# Note 0 means unlimited mirroring SpooledTemporaryFile's __init__self._max_mem_size=getattr(self.file,"_max_size",0) |
| --- | --- |

### fileinstance-attribute¶

```
file
```

The standard Python file object (non-async).

### filenameinstance-attribute¶

```
filename
```

The original file name.

### sizeinstance-attribute¶

```
size
```

The size of the file in bytes.

### headersinstance-attribute¶

```
headers
```

The headers of the request.

### content_typeinstance-attribute¶

```
content_type
```

The content type of the request, from the headers.

### readasync¶

```
read(size=-1)
```

Read some bytes from the file.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| size | The number of bytes to read from the file.TYPE:intDEFAULT:-1 |

  Source code in `fastapi/datastructures.py`

| 888990919293949596979899100101102103104 | asyncdefread(self,size:Annotated[int,Doc("""The number of bytes to read from the file."""),]=-1,)->bytes:"""Read some bytes from the file.To be awaitable, compatible with async, this is run in threadpool."""returnawaitsuper().read(size) |
| --- | --- |

### writeasync¶

```
write(data)
```

Write some bytes to the file.

You normally wouldn't use this from a file you read in a request.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| data | The bytes to write to the file.TYPE:bytes |

  Source code in `fastapi/datastructures.py`

| 68697071727374757677787980818283848586 | asyncdefwrite(self,data:Annotated[bytes,Doc("""The bytes to write to the file."""),],)->None:"""Write some bytes to the file.You normally wouldn't use this from a file you read in a request.To be awaitable, compatible with async, this is run in threadpool."""returnawaitsuper().write(data) |
| --- | --- |

### seekasync¶

```
seek(offset)
```

Move to a position in the file.

Any next read or write will be done from that position.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| offset | The position in bytes to seek to in the file.TYPE:int |

  Source code in `fastapi/datastructures.py`

| 106107108109110111112113114115116117118119120121122123124 | asyncdefseek(self,offset:Annotated[int,Doc("""The position in bytes to seek to in the file."""),],)->None:"""Move to a position in the file.Any next read or write will be done from that position.To be awaitable, compatible with async, this is run in threadpool."""returnawaitsuper().seek(offset) |
| --- | --- |

### closeasync¶

```
close()
```

Close the file.

To be awaitable, compatible with async, this is run in threadpool.

  Source code in `fastapi/datastructures.py`

| 126127128129130131132 | asyncdefclose(self)->None:"""Close the file.To be awaitable, compatible with async, this is run in threadpool."""returnawaitsuper().close() |
| --- | --- |

---

# WebSockets¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# WebSockets¶

When defining WebSockets, you normally declare a parameter of type `WebSocket` and with it you can read data from the client and send data to it.

It is provided directly by Starlette, but you can import it from `fastapi`:

```
from fastapi import WebSocket
```

Tip

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

## fastapi.WebSocket¶

```
WebSocket(scope, receive, send)
```

Bases: `HTTPConnection`

  Source code in `starlette/websockets.py`

| 27282930313233 | def__init__(self,scope:Scope,receive:Receive,send:Send)->None:super().__init__(scope)assertscope["type"]=="websocket"self._receive=receiveself._send=sendself.client_state=WebSocketState.CONNECTINGself.application_state=WebSocketState.CONNECTING |
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

### stateproperty¶

```
state
```

### client_stateinstance-attribute¶

```
client_state = CONNECTING
```

### application_stateinstance-attribute¶

```
application_state = CONNECTING
```

### url_for¶

```
url_for(name, /, **path_params)
```

   Source code in `starlette/requests.py`

| 184185186187188189 | defurl_for(self,name:str,/,**path_params:Any)->URL:url_path_provider:Router|Starlette|None=self.scope.get("router")orself.scope.get("app")ifurl_path_providerisNone:raiseRuntimeError("The `url_for` method can only be used inside a Starlette application or with a router.")url_path=url_path_provider.url_path_for(name,**path_params)returnurl_path.make_absolute_url(base_url=self.base_url) |
| --- | --- |

### receiveasync¶

```
receive()
```

Receive ASGI websocket messages, ensuring valid state transitions.

  Source code in `starlette/websockets.py`

| 3536373839404142434445464748495051525354555657 | asyncdefreceive(self)->Message:"""Receive ASGI websocket messages, ensuring valid state transitions."""ifself.client_state==WebSocketState.CONNECTING:message=awaitself._receive()message_type=message["type"]ifmessage_type!="websocket.connect":raiseRuntimeError(f'Expected ASGI message "websocket.connect", but got{message_type!r}')self.client_state=WebSocketState.CONNECTEDreturnmessageelifself.client_state==WebSocketState.CONNECTED:message=awaitself._receive()message_type=message["type"]ifmessage_typenotin{"websocket.receive","websocket.disconnect"}:raiseRuntimeError(f'Expected ASGI message "websocket.receive" or "websocket.disconnect", but got{message_type!r}')ifmessage_type=="websocket.disconnect":self.client_state=WebSocketState.DISCONNECTEDreturnmessageelse:raiseRuntimeError('Cannot call "receive" once a disconnect message has been received.') |
| --- | --- |

### sendasync¶

```
send(message)
```

Send ASGI websocket messages, ensuring valid state transitions.

  Source code in `starlette/websockets.py`

| 59606162636465666768697071727374757677787980818283848586878889909192939495969798 | asyncdefsend(self,message:Message)->None:"""Send ASGI websocket messages, ensuring valid state transitions."""ifself.application_state==WebSocketState.CONNECTING:message_type=message["type"]ifmessage_typenotin{"websocket.accept","websocket.close","websocket.http.response.start"}:raiseRuntimeError('Expected ASGI message "websocket.accept", "websocket.close" or "websocket.http.response.start", 'f"but got{message_type!r}")ifmessage_type=="websocket.close":self.application_state=WebSocketState.DISCONNECTEDelifmessage_type=="websocket.http.response.start":self.application_state=WebSocketState.RESPONSEelse:self.application_state=WebSocketState.CONNECTEDawaitself._send(message)elifself.application_state==WebSocketState.CONNECTED:message_type=message["type"]ifmessage_typenotin{"websocket.send","websocket.close"}:raiseRuntimeError(f'Expected ASGI message "websocket.send" or "websocket.close", but got{message_type!r}')ifmessage_type=="websocket.close":self.application_state=WebSocketState.DISCONNECTEDtry:awaitself._send(message)exceptOSError:self.application_state=WebSocketState.DISCONNECTEDraiseWebSocketDisconnect(code=1006)elifself.application_state==WebSocketState.RESPONSE:message_type=message["type"]ifmessage_type!="websocket.http.response.body":raiseRuntimeError(f'Expected ASGI message "websocket.http.response.body", but got{message_type!r}')ifnotmessage.get("more_body",False):self.application_state=WebSocketState.DISCONNECTEDawaitself._send(message)else:raiseRuntimeError('Cannot call "send" once a close message has been sent.') |
| --- | --- |

### acceptasync¶

```
accept(subprotocol=None, headers=None)
```

   Source code in `starlette/websockets.py`

| 100101102103104105106107108109110 | asyncdefaccept(self,subprotocol:str|None=None,headers:Iterable[tuple[bytes,bytes]]|None=None,)->None:headers=headersor[]ifself.client_state==WebSocketState.CONNECTING:# pragma: no branch# If we haven't yet seen the 'connect' message, then wait for it first.awaitself.receive()awaitself.send({"type":"websocket.accept","subprotocol":subprotocol,"headers":headers}) |
| --- | --- |

### receive_textasync¶

```
receive_text()
```

   Source code in `starlette/websockets.py`

| 116117118119120121 | asyncdefreceive_text(self)->str:ifself.application_state!=WebSocketState.CONNECTED:raiseRuntimeError('WebSocket is not connected. Need to call "accept" first.')message=awaitself.receive()self._raise_on_disconnect(message)returncast(str,message["text"]) |
| --- | --- |

### receive_bytesasync¶

```
receive_bytes()
```

   Source code in `starlette/websockets.py`

| 123124125126127128 | asyncdefreceive_bytes(self)->bytes:ifself.application_state!=WebSocketState.CONNECTED:raiseRuntimeError('WebSocket is not connected. Need to call "accept" first.')message=awaitself.receive()self._raise_on_disconnect(message)returncast(bytes,message["bytes"]) |
| --- | --- |

### receive_jsonasync¶

```
receive_json(mode='text')
```

   Source code in `starlette/websockets.py`

| 130131132133134135136137138139140141142 | asyncdefreceive_json(self,mode:str="text")->Any:ifmodenotin{"text","binary"}:raiseRuntimeError('The "mode" argument should be "text" or "binary".')ifself.application_state!=WebSocketState.CONNECTED:raiseRuntimeError('WebSocket is not connected. Need to call "accept" first.')message=awaitself.receive()self._raise_on_disconnect(message)ifmode=="text":text=message["text"]else:text=message["bytes"].decode("utf-8")returnjson.loads(text) |
| --- | --- |

### iter_textasync¶

```
iter_text()
```

   Source code in `starlette/websockets.py`

| 144145146147148149 | asyncdefiter_text(self)->AsyncIterator[str]:try:whileTrue:yieldawaitself.receive_text()exceptWebSocketDisconnect:pass |
| --- | --- |

### iter_bytesasync¶

```
iter_bytes()
```

   Source code in `starlette/websockets.py`

| 151152153154155156 | asyncdefiter_bytes(self)->AsyncIterator[bytes]:try:whileTrue:yieldawaitself.receive_bytes()exceptWebSocketDisconnect:pass |
| --- | --- |

### iter_jsonasync¶

```
iter_json()
```

   Source code in `starlette/websockets.py`

| 158159160161162163 | asyncdefiter_json(self)->AsyncIterator[Any]:try:whileTrue:yieldawaitself.receive_json()exceptWebSocketDisconnect:pass |
| --- | --- |

### send_textasync¶

```
send_text(data)
```

   Source code in `starlette/websockets.py`

| 165166 | asyncdefsend_text(self,data:str)->None:awaitself.send({"type":"websocket.send","text":data}) |
| --- | --- |

### send_bytesasync¶

```
send_bytes(data)
```

   Source code in `starlette/websockets.py`

| 168169 | asyncdefsend_bytes(self,data:bytes)->None:awaitself.send({"type":"websocket.send","bytes":data}) |
| --- | --- |

### send_jsonasync¶

```
send_json(data, mode='text')
```

   Source code in `starlette/websockets.py`

| 171172173174175176177178 | asyncdefsend_json(self,data:Any,mode:str="text")->None:ifmodenotin{"text","binary"}:raiseRuntimeError('The "mode" argument should be "text" or "binary".')text=json.dumps(data,separators=(",",":"),ensure_ascii=False)ifmode=="text":awaitself.send({"type":"websocket.send","text":text})else:awaitself.send({"type":"websocket.send","bytes":text.encode("utf-8")}) |
| --- | --- |

### closeasync¶

```
close(code=1000, reason=None)
```

   Source code in `starlette/websockets.py`

| 180181 | asyncdefclose(self,code:int=1000,reason:str|None=None)->None:awaitself.send({"type":"websocket.close","code":code,"reason":reasonor""}) |
| --- | --- |

When a client disconnects, a `WebSocketDisconnect` exception is raised, you can catch it.

You can import it directly form `fastapi`:

```
from fastapi import WebSocketDisconnect
```

## fastapi.WebSocketDisconnect¶

```
WebSocketDisconnect(code=1000, reason=None)
```

Bases: `Exception`

  Source code in `starlette/websockets.py`

| 212223 | def__init__(self,code:int=1000,reason:str|None=None)->None:self.code=codeself.reason=reasonor"" |
| --- | --- |

### codeinstance-attribute¶

```
code = code
```

### reasoninstance-attribute¶

```
reason = reason or ''
```

## WebSockets - additional classes¶

Additional classes for handling WebSockets.

Provided directly by Starlette, but you can import it from `fastapi`:

```
from fastapi.websockets import WebSocketDisconnect, WebSocketState
```

## fastapi.websockets.WebSocketDisconnect¶

```
WebSocketDisconnect(code=1000, reason=None)
```

Bases: `Exception`

  Source code in `starlette/websockets.py`

| 212223 | def__init__(self,code:int=1000,reason:str|None=None)->None:self.code=codeself.reason=reasonor"" |
| --- | --- |

### codeinstance-attribute¶

```
code = code
```

### reasoninstance-attribute¶

```
reason = reason or ''
```

## fastapi.websockets.WebSocketState¶

Bases: `Enum`

### CONNECTINGclass-attributeinstance-attribute¶

```
CONNECTING = 0
```

### CONNECTEDclass-attributeinstance-attribute¶

```
CONNECTED = 1
```

### DISCONNECTEDclass-attributeinstance-attribute¶

```
DISCONNECTED = 2
```

### RESPONSEclass-attributeinstance-attribute¶

```
RESPONSE = 3
```
