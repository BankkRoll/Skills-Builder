# APIRouterclass¶

# APIRouterclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# APIRouterclass¶

Here's the reference information for the `APIRouter` class, with all its parameters, attributes and methods.

You can import the `APIRouter` class directly from `fastapi`:

```
from fastapi import APIRouter
```

## fastapi.APIRouter¶

```
APIRouter(
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    responses=None,
    callbacks=None,
    routes=None,
    redirect_slashes=True,
    default=None,
    dependency_overrides_provider=None,
    route_class=APIRoute,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Bases: `Router`

`APIRouter` class, used to group *path operations*, for example to structure
an app in multiple files. It would then be included in the `FastAPI` app, or
in another `APIRouter` (ultimately included in the app).

Read more about it in the
[FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

#### Example¶

```
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| prefix | An optional path prefix for the router.TYPE:strDEFAULT:'' |
| tags | A list of tags to be applied to all thepath operationsin this
router.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to all thepath operationsin this router.Read more about it in theFastAPI docs for Bigger Applications - Multiple Files.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| default_response_class | The default response class to be used.Read more in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| responses | Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Additional Responses in OpenAPI.And in theFastAPI docs for Bigger Applications.TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| callbacks | OpenAPI callbacks that should apply to allpath operationsin this
router.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| routes | Note: you probably shouldn't use this parameter, it is inherited
from Starlette and supported for compatibility.A list of routes to serve incoming HTTP and WebSocket requests.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| redirect_slashes | Whether to detect and redirect slashes in URLs when the client doesn't
use the same format.TYPE:boolDEFAULT:True |
| default | Default function handler for this router. Used to handle
404 Not Found errors.TYPE:Optional[ASGIApp]DEFAULT:None |
| dependency_overrides_provider | Only used internally by FastAPI to handle dependency overrides.You shouldn't need to use it. It normally points to theFastAPIapp
object.TYPE:Optional[Any]DEFAULT:None |
| route_class | Custom route (path operation) class to be used by this router.Read more about it in theFastAPI docs for Custom Request and APIRoute class.TYPE:type[APIRoute]DEFAULT:APIRoute |
| on_startup | A list of startup event handler functions.You should instead use thelifespanhandlers.Read more in theFastAPI docs forlifespan.TYPE:Optional[Sequence[Callable[[],Any]]]DEFAULT:None |
| on_shutdown | A list of shutdown event handler functions.You should instead use thelifespanhandlers.Read more in theFastAPI docs forlifespan.TYPE:Optional[Sequence[Callable[[],Any]]]DEFAULT:None |
| lifespan | ALifespancontext manager handler. This replacesstartupandshutdownfunctions with a single context manager.Read more in theFastAPI docs forlifespan.TYPE:Optional[Lifespan[Any]]DEFAULT:None |
| deprecated | Mark allpath operationsin this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[bool]DEFAULT:None |
| include_in_schema | To include (or not) all thepath operationsin this router in the
generated OpenAPI.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 691692693694695696697698699700701702703704705706707708709710711712713714715716717718719720721722723724725726727728729730731732733734735736737738739740741742743744745746747748749750751752753754755756757758759760761762763764765766767768769770771772773774775776777778779780781782783784785786787788789790791792793794795796797798799800801802803804805806807808809810811812813814815816817818819820821822823824825826827828829830831832833834835836837838839840841842843844845846847848849850851852853854855856857858859860861862863864865866867868869870871872873874875876877878879880881882883884885886887888889890891892893894895896897898899900901902903904905906907908909910911912913914915916917918919920921922923924925926927928929 | def__init__(self,*,prefix:Annotated[str,Doc("An optional path prefix for the router.")]="",tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to all the *path operations* in thisrouter.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to all the*path operations* in this router.Read more about it in the[FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,default_response_class:Annotated[type[Response],Doc("""The default response class to be used.Read more in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class)."""),]=Default(JSONResponse),responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).And in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""OpenAPI callbacks that should apply to all *path operations* in thisrouter.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,routes:Annotated[Optional[list[BaseRoute]],Doc("""**Note**: you probably shouldn't use this parameter, it is inheritedfrom Starlette and supported for compatibility.---A list of routes to serve incoming HTTP and WebSocket requests."""),deprecated("""You normally wouldn't use this parameter with FastAPI, it is inheritedfrom Starlette and supported for compatibility.In FastAPI, you normally would use the *path operation methods*,like `router.get()`, `router.post()`, etc."""),]=None,redirect_slashes:Annotated[bool,Doc("""Whether to detect and redirect slashes in URLs when the client doesn'tuse the same format."""),]=True,default:Annotated[Optional[ASGIApp],Doc("""Default function handler for this router. Used to handle404 Not Found errors."""),]=None,dependency_overrides_provider:Annotated[Optional[Any],Doc("""Only used internally by FastAPI to handle dependency overrides.You shouldn't need to use it. It normally points to the `FastAPI` appobject."""),]=None,route_class:Annotated[type[APIRoute],Doc("""Custom route (*path operation*) class to be used by this router.Read more about it in the[FastAPI docs for Custom Request and APIRoute class](https://fastapi.tiangolo.com/how-to/custom-request-and-route/#custom-apiroute-class-in-a-router)."""),]=APIRoute,on_startup:Annotated[Optional[Sequence[Callable[[],Any]]],Doc("""A list of startup event handler functions.You should instead use the `lifespan` handlers.Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,on_shutdown:Annotated[Optional[Sequence[Callable[[],Any]]],Doc("""A list of shutdown event handler functions.You should instead use the `lifespan` handlers.Read more in the[FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,# the generic to Lifespan[AppType] is the type of the top level application# which the router cannot know statically, so we use typing.Anylifespan:Annotated[Optional[Lifespan[Any]],Doc("""A `Lifespan` context manager handler. This replaces `startup` and`shutdown` functions with a single context manager.Read more in the[FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark all *path operations* in this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) all the *path operations* in this router in thegenerated OpenAPI.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->None:super().__init__(routes=routes,redirect_slashes=redirect_slashes,default=default,on_startup=on_startup,on_shutdown=on_shutdown,lifespan=lifespan,)ifprefix:assertprefix.startswith("/"),"A path prefix must start with '/'"assertnotprefix.endswith("/"),("A path prefix must not end with '/', as the routes will start with '/'")self.prefix=prefixself.tags:list[Union[str,Enum]]=tagsor[]self.dependencies=list(dependenciesor[])self.deprecated=deprecatedself.include_in_schema=include_in_schemaself.responses=responsesor{}self.callbacks=callbacksor[]self.dependency_overrides_provider=dependency_overrides_providerself.route_class=route_classself.default_response_class=default_response_classself.generate_unique_id_function=generate_unique_id_function |
| --- | --- |

### websocket¶

```
websocket(path, name=None, *, dependencies=None)
```

Decorate a WebSocket function.

Read more about it in the
[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).

**Example**

##### Example¶

```
from fastapi import APIRouter, FastAPI, WebSocket

app = FastAPI()
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | WebSocket path.TYPE:str |
| name | A name for the WebSocket. Only used internally.TYPE:Optional[str]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be used for this
WebSocket.Read more about it in theFastAPI docs for WebSockets.TYPE:Optional[Sequence[Depends]]DEFAULT:None |

  Source code in `fastapi/routing.py`

| 111511161117111811191120112111221123112411251126112711281129113011311132113311341135113611371138113911401141114211431144114511461147114811491150115111521153115411551156115711581159116011611162116311641165116611671168116911701171117211731174117511761177117811791180 | defwebsocket(self,path:Annotated[str,Doc("""WebSocket path."""),],name:Annotated[Optional[str],Doc("""A name for the WebSocket. Only used internally."""),]=None,*,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be used for thisWebSocket.Read more about it in the[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)."""),]=None,)->Callable[[DecoratedCallable],DecoratedCallable]:"""Decorate a WebSocket function.Read more about it in the[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).**Example**## Example```pythonfrom fastapi import APIRouter, FastAPI, WebSocketapp = FastAPI()router = APIRouter()@router.websocket("/ws")async def websocket_endpoint(websocket: WebSocket):await websocket.accept()while True:data = await websocket.receive_text()await websocket.send_text(f"Message text was: {data}")app.include_router(router)```"""defdecorator(func:DecoratedCallable)->DecoratedCallable:self.add_api_websocket_route(path,func,name=name,dependencies=dependencies)returnfuncreturndecorator |
| --- | --- |

### include_router¶

```
include_router(
    router,
    *,
    prefix="",
    tags=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    responses=None,
    callbacks=None,
    deprecated=None,
    include_in_schema=True,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Include another `APIRouter` in the same current `APIRouter`.

Read more about it in the
[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

##### Example¶

```
from fastapi import APIRouter, FastAPI

app = FastAPI()
internal_router = APIRouter()
users_router = APIRouter()

@users_router.get("/users/")
def read_users():
    return [{"name": "Rick"}, {"name": "Morty"}]

internal_router.include_router(users_router)
app.include_router(internal_router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| router | TheAPIRouterto include.TYPE:APIRouter |
| prefix | An optional path prefix for the router.TYPE:strDEFAULT:'' |
| tags | A list of tags to be applied to all thepath operationsin this
router.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to all thepath operationsin this router.Read more about it in theFastAPI docs for Bigger Applications - Multiple Files.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| default_response_class | The default response class to be used.Read more in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| responses | Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Additional Responses in OpenAPI.And in theFastAPI docs for Bigger Applications.TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| callbacks | OpenAPI callbacks that should apply to allpath operationsin this
router.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| deprecated | Mark allpath operationsin this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[bool]DEFAULT:None |
| include_in_schema | Include (or not) all thepath operationsin this router in the
generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).TYPE:boolDEFAULT:True |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 119111921193119411951196119711981199120012011202120312041205120612071208120912101211121212131214121512161217121812191220122112221223122412251226122712281229123012311232123312341235123612371238123912401241124212431244124512461247124812491250125112521253125412551256125712581259126012611262126312641265126612671268126912701271127212731274127512761277127812791280128112821283128412851286128712881289129012911292129312941295129612971298129913001301130213031304130513061307130813091310131113121313131413151316131713181319132013211322132313241325132613271328132913301331133213331334133513361337133813391340134113421343134413451346134713481349135013511352135313541355135613571358135913601361136213631364136513661367136813691370137113721373137413751376137713781379138013811382138313841385138613871388138913901391139213931394139513961397139813991400140114021403140414051406140714081409141014111412141314141415141614171418141914201421142214231424142514261427142814291430143114321433 | definclude_router(self,router:Annotated["APIRouter",Doc("The `APIRouter` to include.")],*,prefix:Annotated[str,Doc("An optional path prefix for the router.")]="",tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to all the *path operations* in thisrouter.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to all the*path operations* in this router.Read more about it in the[FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,default_response_class:Annotated[type[Response],Doc("""The default response class to be used.Read more in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class)."""),]=Default(JSONResponse),responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).And in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""OpenAPI callbacks that should apply to all *path operations* in thisrouter.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark all *path operations* in this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,include_in_schema:Annotated[bool,Doc("""Include (or not) all the *path operations* in this router in thegenerated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`)."""),]=True,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->None:"""Include another `APIRouter` in the same current `APIRouter`.Read more about it in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).## Example```pythonfrom fastapi import APIRouter, FastAPIapp = FastAPI()internal_router = APIRouter()users_router = APIRouter()@users_router.get("/users/")def read_users():return [{"name": "Rick"}, {"name": "Morty"}]internal_router.include_router(users_router)app.include_router(internal_router)```"""ifprefix:assertprefix.startswith("/"),"A path prefix must start with '/'"assertnotprefix.endswith("/"),("A path prefix must not end with '/', as the routes will start with '/'")else:forrinrouter.routes:path=getattr(r,"path")# noqa: B009name=getattr(r,"name","unknown")ifpathisnotNoneandnotpath:raiseFastAPIError(f"Prefix and path cannot be both empty (path operation:{name})")ifresponsesisNone:responses={}forrouteinrouter.routes:ifisinstance(route,APIRoute):combined_responses={**responses,**route.responses}use_response_class=get_value_or_default(route.response_class,router.default_response_class,default_response_class,self.default_response_class,)current_tags=[]iftags:current_tags.extend(tags)ifroute.tags:current_tags.extend(route.tags)current_dependencies:list[params.Depends]=[]ifdependencies:current_dependencies.extend(dependencies)ifroute.dependencies:current_dependencies.extend(route.dependencies)current_callbacks=[]ifcallbacks:current_callbacks.extend(callbacks)ifroute.callbacks:current_callbacks.extend(route.callbacks)current_generate_unique_id=get_value_or_default(route.generate_unique_id_function,router.generate_unique_id_function,generate_unique_id_function,self.generate_unique_id_function,)self.add_api_route(prefix+route.path,route.endpoint,response_model=route.response_model,status_code=route.status_code,tags=current_tags,dependencies=current_dependencies,summary=route.summary,description=route.description,response_description=route.response_description,responses=combined_responses,deprecated=route.deprecatedordeprecatedorself.deprecated,methods=route.methods,operation_id=route.operation_id,response_model_include=route.response_model_include,response_model_exclude=route.response_model_exclude,response_model_by_alias=route.response_model_by_alias,response_model_exclude_unset=route.response_model_exclude_unset,response_model_exclude_defaults=route.response_model_exclude_defaults,response_model_exclude_none=route.response_model_exclude_none,include_in_schema=route.include_in_schemaandself.include_in_schemaandinclude_in_schema,response_class=use_response_class,name=route.name,route_class_override=type(route),callbacks=current_callbacks,openapi_extra=route.openapi_extra,generate_unique_id_function=current_generate_unique_id,)elifisinstance(route,routing.Route):methods=list(route.methodsor[])self.add_route(prefix+route.path,route.endpoint,methods=methods,include_in_schema=route.include_in_schema,name=route.name,)elifisinstance(route,APIWebSocketRoute):current_dependencies=[]ifdependencies:current_dependencies.extend(dependencies)ifroute.dependencies:current_dependencies.extend(route.dependencies)self.add_api_websocket_route(prefix+route.path,route.endpoint,dependencies=current_dependencies,name=route.name,)elifisinstance(route,routing.WebSocketRoute):self.add_websocket_route(prefix+route.path,route.endpoint,name=route.name)forhandlerinrouter.on_startup:self.add_event_handler("startup",handler)forhandlerinrouter.on_shutdown:self.add_event_handler("shutdown",handler)self.lifespan_context=_merge_lifespan_context(self.lifespan_context,router.lifespan_context,) |
| --- | --- |

### get¶

```
get(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP GET operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/items/")
def read_items():
    return [{"name": "Empanada"}, {"name": "Arepa"}]

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 1435143614371438143914401441144214431444144514461447144814491450145114521453145414551456145714581459146014611462146314641465146614671468146914701471147214731474147514761477147814791480148114821483148414851486148714881489149014911492149314941495149614971498149915001501150215031504150515061507150815091510151115121513151415151516151715181519152015211522152315241525152615271528152915301531153215331534153515361537153815391540154115421543154415451546154715481549155015511552155315541555155615571558155915601561156215631564156515661567156815691570157115721573157415751576157715781579158015811582158315841585158615871588158915901591159215931594159515961597159815991600160116021603160416051606160716081609161016111612161316141615161616171618161916201621162216231624162516261627162816291630163116321633163416351636163716381639164016411642164316441645164616471648164916501651165216531654165516561657165816591660166116621663166416651666166716681669167016711672167316741675167616771678167916801681168216831684168516861687168816891690169116921693169416951696169716981699170017011702170317041705170617071708170917101711171217131714171517161717171817191720172117221723172417251726172717281729173017311732173317341735173617371738173917401741174217431744174517461747174817491750175117521753175417551756175717581759176017611762176317641765176617671768176917701771177217731774177517761777177817791780178117821783178417851786178717881789179017911792179317941795179617971798179918001801180218031804180518061807180818091810 | defget(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP GET operation.## Example```pythonfrom fastapi import APIRouter, FastAPIapp = FastAPI()router = APIRouter()@router.get("/items/")def read_items():return [{"name": "Empanada"}, {"name": "Arepa"}]app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["GET"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### put¶

```
put(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP PUT operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.put("/items/{item_id}")
def replace_item(item_id: str, item: Item):
    return {"message": "Item replaced", "id": item_id}

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 181218131814181518161817181818191820182118221823182418251826182718281829183018311832183318341835183618371838183918401841184218431844184518461847184818491850185118521853185418551856185718581859186018611862186318641865186618671868186918701871187218731874187518761877187818791880188118821883188418851886188718881889189018911892189318941895189618971898189919001901190219031904190519061907190819091910191119121913191419151916191719181919192019211922192319241925192619271928192919301931193219331934193519361937193819391940194119421943194419451946194719481949195019511952195319541955195619571958195919601961196219631964196519661967196819691970197119721973197419751976197719781979198019811982198319841985198619871988198919901991199219931994199519961997199819992000200120022003200420052006200720082009201020112012201320142015201620172018201920202021202220232024202520262027202820292030203120322033203420352036203720382039204020412042204320442045204620472048204920502051205220532054205520562057205820592060206120622063206420652066206720682069207020712072207320742075207620772078207920802081208220832084208520862087208820892090209120922093209420952096209720982099210021012102210321042105210621072108210921102111211221132114211521162117211821192120212121222123212421252126212721282129213021312132213321342135213621372138213921402141214221432144214521462147214821492150215121522153215421552156215721582159216021612162216321642165216621672168216921702171217221732174217521762177217821792180218121822183218421852186218721882189219021912192 | defput(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP PUT operation.## Example```pythonfrom fastapi import APIRouter, FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()router = APIRouter()@router.put("/items/{item_id}")def replace_item(item_id: str, item: Item):return {"message": "Item replaced", "id": item_id}app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["PUT"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### post¶

```
post(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP POST operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return {"message": "Item created"}

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 219421952196219721982199220022012202220322042205220622072208220922102211221222132214221522162217221822192220222122222223222422252226222722282229223022312232223322342235223622372238223922402241224222432244224522462247224822492250225122522253225422552256225722582259226022612262226322642265226622672268226922702271227222732274227522762277227822792280228122822283228422852286228722882289229022912292229322942295229622972298229923002301230223032304230523062307230823092310231123122313231423152316231723182319232023212322232323242325232623272328232923302331233223332334233523362337233823392340234123422343234423452346234723482349235023512352235323542355235623572358235923602361236223632364236523662367236823692370237123722373237423752376237723782379238023812382238323842385238623872388238923902391239223932394239523962397239823992400240124022403240424052406240724082409241024112412241324142415241624172418241924202421242224232424242524262427242824292430243124322433243424352436243724382439244024412442244324442445244624472448244924502451245224532454245524562457245824592460246124622463246424652466246724682469247024712472247324742475247624772478247924802481248224832484248524862487248824892490249124922493249424952496249724982499250025012502250325042505250625072508250925102511251225132514251525162517251825192520252125222523252425252526252725282529253025312532253325342535253625372538253925402541254225432544254525462547254825492550255125522553255425552556255725582559256025612562256325642565256625672568256925702571257225732574 | defpost(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP POST operation.## Example```pythonfrom fastapi import APIRouter, FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()router = APIRouter()@router.post("/items/")def create_item(item: Item):return {"message": "Item created"}app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["POST"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### delete¶

```
delete(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP DELETE operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.delete("/items/{item_id}")
def delete_item(item_id: str):
    return {"message": "Item deleted"}

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 2576257725782579258025812582258325842585258625872588258925902591259225932594259525962597259825992600260126022603260426052606260726082609261026112612261326142615261626172618261926202621262226232624262526262627262826292630263126322633263426352636263726382639264026412642264326442645264626472648264926502651265226532654265526562657265826592660266126622663266426652666266726682669267026712672267326742675267626772678267926802681268226832684268526862687268826892690269126922693269426952696269726982699270027012702270327042705270627072708270927102711271227132714271527162717271827192720272127222723272427252726272727282729273027312732273327342735273627372738273927402741274227432744274527462747274827492750275127522753275427552756275727582759276027612762276327642765276627672768276927702771277227732774277527762777277827792780278127822783278427852786278727882789279027912792279327942795279627972798279928002801280228032804280528062807280828092810281128122813281428152816281728182819282028212822282328242825282628272828282928302831283228332834283528362837283828392840284128422843284428452846284728482849285028512852285328542855285628572858285928602861286228632864286528662867286828692870287128722873287428752876287728782879288028812882288328842885288628872888288928902891289228932894289528962897289828992900290129022903290429052906290729082909291029112912291329142915291629172918291929202921292229232924292529262927292829292930293129322933293429352936293729382939294029412942294329442945294629472948294929502951 | defdelete(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP DELETE operation.## Example```pythonfrom fastapi import APIRouter, FastAPIapp = FastAPI()router = APIRouter()@router.delete("/items/{item_id}")def delete_item(item_id: str):return {"message": "Item deleted"}app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["DELETE"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### options¶

```
options(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP OPTIONS operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.options("/items/")
def get_item_options():
    return {"additions": ["Aji", "Guacamole"]}

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 2953295429552956295729582959296029612962296329642965296629672968296929702971297229732974297529762977297829792980298129822983298429852986298729882989299029912992299329942995299629972998299930003001300230033004300530063007300830093010301130123013301430153016301730183019302030213022302330243025302630273028302930303031303230333034303530363037303830393040304130423043304430453046304730483049305030513052305330543055305630573058305930603061306230633064306530663067306830693070307130723073307430753076307730783079308030813082308330843085308630873088308930903091309230933094309530963097309830993100310131023103310431053106310731083109311031113112311331143115311631173118311931203121312231233124312531263127312831293130313131323133313431353136313731383139314031413142314331443145314631473148314931503151315231533154315531563157315831593160316131623163316431653166316731683169317031713172317331743175317631773178317931803181318231833184318531863187318831893190319131923193319431953196319731983199320032013202320332043205320632073208320932103211321232133214321532163217321832193220322132223223322432253226322732283229323032313232323332343235323632373238323932403241324232433244324532463247324832493250325132523253325432553256325732583259326032613262326332643265326632673268326932703271327232733274327532763277327832793280328132823283328432853286328732883289329032913292329332943295329632973298329933003301330233033304330533063307330833093310331133123313331433153316331733183319332033213322332333243325332633273328 | defoptions(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP OPTIONS operation.## Example```pythonfrom fastapi import APIRouter, FastAPIapp = FastAPI()router = APIRouter()@router.options("/items/")def get_item_options():return {"additions": ["Aji", "Guacamole"]}app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["OPTIONS"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### head¶

```
head(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP HEAD operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.head("/items/", status_code=204)
def get_items_headers(response: Response):
    response.headers["X-Cat-Dog"] = "Alone in the world"

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 333033313332333333343335333633373338333933403341334233433344334533463347334833493350335133523353335433553356335733583359336033613362336333643365336633673368336933703371337233733374337533763377337833793380338133823383338433853386338733883389339033913392339333943395339633973398339934003401340234033404340534063407340834093410341134123413341434153416341734183419342034213422342334243425342634273428342934303431343234333434343534363437343834393440344134423443344434453446344734483449345034513452345334543455345634573458345934603461346234633464346534663467346834693470347134723473347434753476347734783479348034813482348334843485348634873488348934903491349234933494349534963497349834993500350135023503350435053506350735083509351035113512351335143515351635173518351935203521352235233524352535263527352835293530353135323533353435353536353735383539354035413542354335443545354635473548354935503551355235533554355535563557355835593560356135623563356435653566356735683569357035713572357335743575357635773578357935803581358235833584358535863587358835893590359135923593359435953596359735983599360036013602360336043605360636073608360936103611361236133614361536163617361836193620362136223623362436253626362736283629363036313632363336343635363636373638363936403641364236433644364536463647364836493650365136523653365436553656365736583659366036613662366336643665366636673668366936703671367236733674367536763677367836793680368136823683368436853686368736883689369036913692369336943695369636973698369937003701370237033704370537063707370837093710 | defhead(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP HEAD operation.## Example```pythonfrom fastapi import APIRouter, FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()router = APIRouter()@router.head("/items/", status_code=204)def get_items_headers(response: Response):response.headers["X-Cat-Dog"] = "Alone in the world"app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["HEAD"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### patch¶

```
patch(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP PATCH operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.patch("/items/")
def update_item(item: Item):
    return {"message": "Item updated in place"}

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 371237133714371537163717371837193720372137223723372437253726372737283729373037313732373337343735373637373738373937403741374237433744374537463747374837493750375137523753375437553756375737583759376037613762376337643765376637673768376937703771377237733774377537763777377837793780378137823783378437853786378737883789379037913792379337943795379637973798379938003801380238033804380538063807380838093810381138123813381438153816381738183819382038213822382338243825382638273828382938303831383238333834383538363837383838393840384138423843384438453846384738483849385038513852385338543855385638573858385938603861386238633864386538663867386838693870387138723873387438753876387738783879388038813882388338843885388638873888388938903891389238933894389538963897389838993900390139023903390439053906390739083909391039113912391339143915391639173918391939203921392239233924392539263927392839293930393139323933393439353936393739383939394039413942394339443945394639473948394939503951395239533954395539563957395839593960396139623963396439653966396739683969397039713972397339743975397639773978397939803981398239833984398539863987398839893990399139923993399439953996399739983999400040014002400340044005400640074008400940104011401240134014401540164017401840194020402140224023402440254026402740284029403040314032403340344035403640374038403940404041404240434044404540464047404840494050405140524053405440554056405740584059406040614062406340644065406640674068406940704071407240734074407540764077407840794080408140824083408440854086408740884089409040914092 | defpatch(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP PATCH operation.## Example```pythonfrom fastapi import APIRouter, FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()router = APIRouter()@router.patch("/items/")def update_item(item: Item):return {"message": "Item updated in place"}app.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["PATCH"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### trace¶

```
trace(
    path,
    *,
    response_model=Default(None),
    status_code=None,
    tags=None,
    dependencies=None,
    summary=None,
    description=None,
    response_description="Successful Response",
    responses=None,
    deprecated=None,
    operation_id=None,
    response_model_include=None,
    response_model_exclude=None,
    response_model_by_alias=True,
    response_model_exclude_unset=False,
    response_model_exclude_defaults=False,
    response_model_exclude_none=False,
    include_in_schema=True,
    response_class=Default(JSONResponse),
    name=None,
    callbacks=None,
    openapi_extra=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Add a *path operation* using an HTTP TRACE operation.

##### Example¶

```
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.trace("/items/{item_id}")
def trace_item(item_id: str):
    return None

app.include_router(router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | The URL path to be used for thispath operation.For example, inhttp://example.com/items, the path is/items.TYPE:str |
| response_model | The type to use for the response.It could be any valid Pydanticfieldtype. So, it doesn't have to
be a Pydantic model, it could be other things, like alist,dict,
etc.It will be used for:Documentation: the generated OpenAPI (and the UI at/docs) will
    show it as the response (JSON Schema).Serialization: you could return an arbitrary object and theresponse_modelwould be used to serialize that object into the
    corresponding JSON.Filtering: the JSON sent to the client will only contain the data
    (fields) defined in theresponse_model. If you returned an object
    that contains an attributepasswordbut theresponse_modeldoes
    not include that field, the JSON sent to the client would not have
    thatpassword.Validation: whatever you return will be serialized with theresponse_model, converting any data as necessary to generate the
    corresponding JSON. But if the data in the object returned is not
    valid, that would mean a violation of the contract with the client,
    so it's an error from the API developer. So, FastAPI will raise an
    error and return a 500 error code (Internal Server Error).Read more about it in theFastAPI docs for Response Model.TYPE:AnyDEFAULT:Default(None) |
| status_code | The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in theFastAPI docs for Response Status Code.TYPE:Optional[int]DEFAULT:None |
| tags | A list of tags to be applied to thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to thepath operation.Read more about it in theFastAPI docs for Dependencies in path operation decorators.TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| summary | A summary for thepath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| description | A description for thepath operation.If not provided, it will be extracted automatically from the docstring
of thepath operation function.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[str]DEFAULT:None |
| response_description | The description for the default response.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:strDEFAULT:'Successful Response' |
| responses | Additional responses that could be returned by thispath operation.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark thispath operationas deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[bool]DEFAULT:None |
| operation_id | Custom operation ID to be used by thispath operation.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it is
unique for the whole API.You can customize the
operation ID generation with the parametergenerate_unique_id_functionin theFastAPIclass.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Optional[str]DEFAULT:None |
| response_model_include | Configuration passed to Pydantic to include only certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_exclude | Configuration passed to Pydantic to exclude certain fields in the
response data.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:Optional[IncEx]DEFAULT:None |
| response_model_by_alias | Configuration passed to Pydantic to define if the response model
should be serialized by alias when an alias is used.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:True |
| response_model_exclude_unset | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that were not set and
have their default values. This is different fromresponse_model_exclude_defaultsin that if the fields are set,
they will be included in the response, even if the value is the same
as the default.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_defaults | Configuration passed to Pydantic to define if the response data
should have all the fields, including the ones that have the same value
as the default. This is different fromresponse_model_exclude_unsetin that if the fields are set but contain the same default values,
they will be excluded from the response.WhenTrue, default values are omitted from the response.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| response_model_exclude_none | Configuration passed to Pydantic to define if the response data should
exclude fields set toNone.This is much simpler (less smart) thanresponse_model_exclude_unsetandresponse_model_exclude_defaults. You probably want to use one of
those two instead of this one, as those allow returningNonevalues
when it makes sense.Read more about it in theFastAPI docs for Response Model - Return Type.TYPE:boolDEFAULT:False |
| include_in_schema | Include thispath operationin the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| response_class | Response class to be used for thispath operation.This will not be used if you return a response directly.Read more about it in theFastAPI docs for Custom Response - HTML, Stream, File, others.TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| name | Name for thispath operation. Only used internally.TYPE:Optional[str]DEFAULT:None |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| openapi_extra | Extra metadata to be included in the OpenAPI schema for thispath
operation.Read more about it in theFastAPI docs for Path Operation Advanced Configuration.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/routing.py`

| 409440954096409740984099410041014102410341044105410641074108410941104111411241134114411541164117411841194120412141224123412441254126412741284129413041314132413341344135413641374138413941404141414241434144414541464147414841494150415141524153415441554156415741584159416041614162416341644165416641674168416941704171417241734174417541764177417841794180418141824183418441854186418741884189419041914192419341944195419641974198419942004201420242034204420542064207420842094210421142124213421442154216421742184219422042214222422342244225422642274228422942304231423242334234423542364237423842394240424142424243424442454246424742484249425042514252425342544255425642574258425942604261426242634264426542664267426842694270427142724273427442754276427742784279428042814282428342844285428642874288428942904291429242934294429542964297429842994300430143024303430443054306430743084309431043114312431343144315431643174318431943204321432243234324432543264327432843294330433143324333433443354336433743384339434043414342434343444345434643474348434943504351435243534354435543564357435843594360436143624363436443654366436743684369437043714372437343744375437643774378437943804381438243834384438543864387438843894390439143924393439443954396439743984399440044014402440344044405440644074408440944104411441244134414441544164417441844194420442144224423442444254426442744284429443044314432443344344435443644374438443944404441444244434444444544464447444844494450445144524453445444554456445744584459446044614462446344644465446644674468446944704471447244734474 | deftrace(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[params.Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP TRACE operation.## Example```pythonfrom fastapi import APIRouter, FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()router = APIRouter()@router.trace("/items/{item_id}")def trace_item(item_id: str):return Noneapp.include_router(router)```"""returnself.api_route(path=path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,methods=["TRACE"],operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### on_event¶

```
on_event(event_type)
```

Add an event handler for the router.

`on_event` is deprecated, use `lifespan` event handlers instead.

Read more about it in the
[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated).

| PARAMETER | DESCRIPTION |
| --- | --- |
| event_type | The type of event.startuporshutdown.TYPE:str |

  Source code in `fastapi/routing.py`

| 447644774478447944804481448244834484448544864487448844894490449144924493449444954496449744984499450045014502450345044505450645074508 | @deprecated("""on_event is deprecated, use lifespan event handlers instead.Read more about it in the[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).""")defon_event(self,event_type:Annotated[str,Doc("""The type of event. `startup` or `shutdown`."""),],)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add an event handler for the router.`on_event` is deprecated, use `lifespan` event handlers instead.Read more about it in the[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated)."""defdecorator(func:DecoratedCallable)->DecoratedCallable:self.add_event_handler(event_type,func)returnfuncreturndecorator |
| --- | --- |
