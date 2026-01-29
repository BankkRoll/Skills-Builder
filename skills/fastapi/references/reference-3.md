# FastAPIclass¶

# FastAPIclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# FastAPIclass¶

Here's the reference information for the `FastAPI` class, with all its parameters, attributes and methods.

You can import the `FastAPI` class directly from `fastapi`:

```
from fastapi import FastAPI
```

## fastapi.FastAPI¶

```
FastAPI(
    *,
    debug=False,
    routes=None,
    title="FastAPI",
    summary=None,
    description="",
    version="0.1.0",
    openapi_url="/openapi.json",
    openapi_tags=None,
    servers=None,
    dependencies=None,
    default_response_class=Default(JSONResponse),
    redirect_slashes=True,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth=None,
    middleware=None,
    exception_handlers=None,
    on_startup=None,
    on_shutdown=None,
    lifespan=None,
    terms_of_service=None,
    contact=None,
    license_info=None,
    openapi_prefix="",
    root_path="",
    root_path_in_servers=True,
    responses=None,
    callbacks=None,
    webhooks=None,
    deprecated=None,
    include_in_schema=True,
    swagger_ui_parameters=None,
    generate_unique_id_function=Default(generate_unique_id),
    separate_input_output_schemas=True,
    openapi_external_docs=None,
    **extra
)
```

Bases: `Starlette`

`FastAPI` app class, the main entrypoint to use FastAPI.

Read more in the
[FastAPI docs for First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/).

#### Example¶

```
from fastapi import FastAPI

app = FastAPI()
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| debug | Boolean indicating if debug tracebacks should be returned on server
errors.Read more in theStarlette docs for Applications.TYPE:boolDEFAULT:False |
| routes | Note: you probably shouldn't use this parameter, it is inherited
from Starlette and supported for compatibility.A list of routes to serve incoming HTTP and WebSocket requests.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| title | The title of the API.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(title="ChimichangApp")TYPE:strDEFAULT:'FastAPI' |
| summary | A short summary of the API.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(summary="Deadpond's favorite app. Nuff said.")TYPE:Optional[str]DEFAULT:None |
| description | A description of the API. Supports Markdown (usingCommonMark syntax).It will be added to the generated OpenAPI (e.g. visible at/docs).Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(description="""ChimichangApp API helps you do awesome stuff. 🚀## ItemsYou can **read items**.## UsersYou will be able to:* **Create users** (_not implemented_).* **Read users** (_not implemented_).""")TYPE:strDEFAULT:'' |
| version | The version of the API.NoteThis is the version of your application, not the version of
the OpenAPI specification nor the version of FastAPI being used.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(version="0.0.1")TYPE:strDEFAULT:'0.1.0' |
| openapi_url | The URL where the OpenAPI schema will be served from.If you set it toNone, no OpenAPI schema will be served publicly, and
the default automatic endpoints/docsand/redocwill also be
disabled.Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(openapi_url="/api/v1/openapi.json")TYPE:Optional[str]DEFAULT:'/openapi.json' |
| openapi_tags | A list of tags used by OpenAPI, these are the sametagsyou can set
in thepath operations, like:@app.get("/users/", tags=["users"])@app.get("/items/", tags=["items"])The order of the tags can be used to specify the order shown in
tools like Swagger UI, used in the automatic path/docs.It's not required to specify all the tags used.The tags that are not declared MAY be organized randomly or based
on the tools' logic. Each tag name in the list MUST be unique.The value of each item is adictcontaining:name: The name of the tag.description: A short description of the tag.CommonMark syntaxMAY be used for rich
    text representation.externalDocs: Additional external documentation for this tag. If
    provided, it would contain adictwith:description: A short description of the target documentation.CommonMark syntaxMAY be used for
    rich text representation.url: The URL for the target documentation. Value MUST be in
    the form of a URL.Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPItags_metadata=[{"name":"users","description":"Operations with users. The **login** logic is also here.",},{"name":"items","description":"Manage items. So _fancy_ they have their own docs.","externalDocs":{"description":"Items external docs","url":"https://fastapi.tiangolo.com/",},},]app=FastAPI(openapi_tags=tags_metadata)TYPE:Optional[list[dict[str,Any]]]DEFAULT:None |
| servers | Alistofdicts with connectivity information to a target server.You would use it, for example, if your application is served from
different domains and you want to use the same Swagger UI in the
browser to interact with each of them (instead of having multiple
browser tabs open). Or if you want to leave fixed the possible URLs.If the serverslistis not provided, or is an emptylist, theserversproperty in the generated OpenAPI will be:adictwith aurlvalue of the application's mounting point
(root_path) if it's different from/.otherwise, theserversproperty will be omitted from the OpenAPI
schema.Each item in thelistis adictcontaining:url: A URL to the target host. This URL supports Server Variables
and MAY be relative, to indicate that the host location is relative
to the location where the OpenAPI document is being served. Variable
substitutions will be made when a variable is named in{brackets}.description: An optional string describing the host designated by
the URL.CommonMark syntaxMAY be used for
rich text representation.variables: Adictbetween a variable name and its value. The value
    is used for substitution in the server's URL template.Read more in theFastAPI docs for Behind a Proxy.ExamplefromfastapiimportFastAPIapp=FastAPI(servers=[{"url":"https://stag.example.com","description":"Staging environment"},{"url":"https://prod.example.com","description":"Production environment"},])TYPE:Optional[list[dict[str,Union[str,Any]]]]DEFAULT:None |
| dependencies | A list of global dependencies, they will be applied to eachpath operation, including in sub-routers.Read more about it in theFastAPI docs for Global Dependencies.ExamplefromfastapiimportDepends,FastAPIfrom.dependenciesimportfunc_dep_1,func_dep_2app=FastAPI(dependencies=[Depends(func_dep_1),Depends(func_dep_2)])TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| default_response_class | The default response class to be used.Read more in theFastAPI docs for Custom Response - HTML, Stream, File, others.ExamplefromfastapiimportFastAPIfromfastapi.responsesimportORJSONResponseapp=FastAPI(default_response_class=ORJSONResponse)TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| redirect_slashes | Whether to detect and redirect slashes in URLs when the client doesn't
use the same format.ExamplefromfastapiimportFastAPIapp=FastAPI(redirect_slashes=True)# the default@app.get("/items/")asyncdefread_items():return[{"item_id":"Foo"}]With this app, if a client goes to/items(without a trailing slash),
they will be automatically redirected with an HTTP status code of 307
to/items/.TYPE:boolDEFAULT:True |
| docs_url | The path to the automatic interactive API documentation.
It is handled in the browser by Swagger UI.The default URL is/docs. You can disable it by setting it toNone.Ifopenapi_urlis set toNone, this will be automatically disabled.Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(docs_url="/documentation",redoc_url=None)TYPE:Optional[str]DEFAULT:'/docs' |
| redoc_url | The path to the alternative automatic interactive API documentation
provided by ReDoc.The default URL is/redoc. You can disable it by setting it toNone.Ifopenapi_urlis set toNone, this will be automatically disabled.Read more in theFastAPI docs for Metadata and Docs URLs.ExamplefromfastapiimportFastAPIapp=FastAPI(docs_url="/documentation",redoc_url="redocumentation")TYPE:Optional[str]DEFAULT:'/redoc' |
| swagger_ui_oauth2_redirect_url | The OAuth2 redirect endpoint for the Swagger UI.By default it is/docs/oauth2-redirect.This is only used if you use OAuth2 (with the "Authorize" button)
with Swagger UI.TYPE:Optional[str]DEFAULT:'/docs/oauth2-redirect' |
| swagger_ui_init_oauth | OAuth2 configuration for the Swagger UI, by default shown at/docs.Read more about the available configuration options in theSwagger UI docs.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| middleware | List of middleware to be added when creating the application.In FastAPI you would normally do this withapp.add_middleware()instead.Read more in theFastAPI docs for Middleware.TYPE:Optional[Sequence[Middleware]]DEFAULT:None |
| exception_handlers | A dictionary with handlers for exceptions.In FastAPI, you would normally use the decorator@app.exception_handler().Read more in theFastAPI docs for Handling Errors.TYPE:Optional[dict[Union[int,type[Exception]],Callable[[Request,Any],Coroutine[Any,Any,Response]]]]DEFAULT:None |
| on_startup | A list of startup event handler functions.You should instead use thelifespanhandlers.Read more in theFastAPI docs forlifespan.TYPE:Optional[Sequence[Callable[[],Any]]]DEFAULT:None |
| on_shutdown | A list of shutdown event handler functions.You should instead use thelifespanhandlers.Read more in theFastAPI docs forlifespan.TYPE:Optional[Sequence[Callable[[],Any]]]DEFAULT:None |
| lifespan | ALifespancontext manager handler. This replacesstartupandshutdownfunctions with a single context manager.Read more in theFastAPI docs forlifespan.TYPE:Optional[Lifespan[AppType]]DEFAULT:None |
| terms_of_service | A URL to the Terms of Service for your API.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more at theFastAPI docs for Metadata and Docs URLs.Exampleapp=FastAPI(terms_of_service="http://example.com/terms/")TYPE:Optional[str]DEFAULT:None |
| contact | A dictionary with the contact information for the exposed API.It can contain several fields.name: (str) The name of the contact person/organization.url: (str) A URL pointing to the contact information. MUST be in
    the format of a URL.email: (str) The email address of the contact person/organization.
    MUST be in the format of an email address.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more at theFastAPI docs for Metadata and Docs URLs.Exampleapp=FastAPI(contact={"name":"Deadpoolio the Amazing","url":"http://x-force.example.com/contact/","email":"dp@x-force.example.com",})TYPE:Optional[dict[str,Union[str,Any]]]DEFAULT:None |
| license_info | A dictionary with the license information for the exposed API.It can contain several fields.name: (str)REQUIRED(if alicense_infois set). The
    license name used for the API.identifier: (str) AnSPDXlicense expression
    for the API. Theidentifierfield is mutually exclusive of theurlfield. Available since OpenAPI 3.1.0, FastAPI 0.99.0.url: (str) A URL to the license used for the API. This MUST be
    the format of a URL.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more at theFastAPI docs for Metadata and Docs URLs.Exampleapp=FastAPI(license_info={"name":"Apache 2.0","url":"https://www.apache.org/licenses/LICENSE-2.0.html",})TYPE:Optional[dict[str,Union[str,Any]]]DEFAULT:None |
| openapi_prefix | A URL prefix for the OpenAPI URL.TYPE:strDEFAULT:'' |
| root_path | A path prefix handled by a proxy that is not seen by the application
but is seen by external clients, which affects things like Swagger UI.Read more about it at theFastAPI docs for Behind a Proxy.ExamplefromfastapiimportFastAPIapp=FastAPI(root_path="/api/v1")TYPE:strDEFAULT:'' |
| root_path_in_servers | To disable automatically generating the URLs in theserversfield
in the autogenerated OpenAPI using theroot_path.Read more about it in theFastAPI docs for Behind a Proxy.ExamplefromfastapiimportFastAPIapp=FastAPI(root_path_in_servers=False)TYPE:boolDEFAULT:True |
| responses | Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Additional Responses in OpenAPI.And in theFastAPI docs for Bigger Applications.TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| callbacks | OpenAPI callbacks that should apply to allpath operations.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| webhooks | Add OpenAPI webhooks. This is similar tocallbacksbut it doesn't
depend on specificpath operations.It will be added to the generated OpenAPI (e.g. visible at/docs).Note: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.Read more about it in theFastAPI docs for OpenAPI Webhooks.TYPE:Optional[APIRouter]DEFAULT:None |
| deprecated | Mark allpath operationsas deprecated. You probably don't need it,
but it's available.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[bool]DEFAULT:None |
| include_in_schema | To include (or not) all thepath operationsin the generated OpenAPI.
You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Query Parameters and String Validations.TYPE:boolDEFAULT:True |
| swagger_ui_parameters | Parameters to configure Swagger UI, the autogenerated interactive API
documentation (by default at/docs).Read more about it in theFastAPI docs about how to Configure Swagger UI.TYPE:Optional[dict[str,Any]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |
| separate_input_output_schemas | Whether to generate separate OpenAPI schemas for request body and
response body when the results would be more precise.This is particularly useful when automatically generating clients.For example, if you have a model like:frompydanticimportBaseModelclassItem(BaseModel):name:strtags:list[str]=[]WhenItemis used for input, a request body,tagsis not required,
the client doesn't have to provide it.But when usingItemfor output, for a response body,tagsis always
available because it has a default value, even if it's just an empty
list. So, the client should be able to always expect it.In this case, there would be two different schemas, one for input and
another one for output.TYPE:boolDEFAULT:True |
| openapi_external_docs | This field allows you to provide additional external documentation links.
If provided, it must be a dictionary containing:description: A brief description of the external documentation.url: The URL pointing to the external documentation. The valueMUSTbe a valid URL format.Example:fromfastapiimportFastAPIexternal_docs={"description":"Detailed API Reference","url":"https://example.com/api-docs",}app=FastAPI(openapi_external_docs=external_docs)TYPE:Optional[dict[str,Any]]DEFAULT:None |
| **extra | Extra keyword arguments to be stored in the app, not used by FastAPI
anywhere.TYPE:AnyDEFAULT:{} |

  Source code in `fastapi/applications.py`

| 646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406407408409410411412413414415416417418419420421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456457458459460461462463464465466467468469470471472473474475476477478479480481482483484485486487488489490491492493494495496497498499500501502503504505506507508509510511512513514515516517518519520521522523524525526527528529530531532533534535536537538539540541542543544545546547548549550551552553554555556557558559560561562563564565566567568569570571572573574575576577578579580581582583584585586587588589590591592593594595596597598599600601602603604605606607608609610611612613614615616617618619620621622623624625626627628629630631632633634635636637638639640641642643644645646647648649650651652653654655656657658659660661662663664665666667668669670671672673674675676677678679680681682683684685686687688689690691692693694695696697698699700701702703704705706707708709710711712713714715716717718719720721722723724725726727728729730731732733734735736737738739740741742743744745746747748749750751752753754755756757758759760761762763764765766767768769770771772773774775776777778779780781782783784785786787788789790791792793794795796797798799800801802803804805806807808809810811812813814815816817818819820821822823824825826827828829830831832833834835836837838839840841842843844845846847848849850851852853854855856857858859860861862863864865866867868869870871872873874875876877878879880881882883884885886887888889890891892893894895896897898899900901902903904905906907908909910911912913914915916917918919920921922923924925926927928929930931932933934935936937938939940941942943944945946947948949950951952953954955956957958959960961962963964965966967968969970971972973974975976977978979980981982983984985986987988989990991992993994995996 | def__init__(self:AppType,*,debug:Annotated[bool,Doc("""Boolean indicating if debug tracebacks should be returned on servererrors.Read more in the[Starlette docs for Applications](https://www.starlette.dev/applications/#instantiating-the-application)."""),]=False,routes:Annotated[Optional[list[BaseRoute]],Doc("""**Note**: you probably shouldn't use this parameter, it is inheritedfrom Starlette and supported for compatibility.---A list of routes to serve incoming HTTP and WebSocket requests."""),deprecated("""You normally wouldn't use this parameter with FastAPI, it is inheritedfrom Starlette and supported for compatibility.In FastAPI, you normally would use the *path operation methods*,like `app.get()`, `app.post()`, etc."""),]=None,title:Annotated[str,Doc("""The title of the API.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(title="ChimichangApp")```"""),]="FastAPI",summary:Annotated[Optional[str],Doc("""A short summary of the API.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(summary="Deadpond's favorite app. Nuff said.")```"""),]=None,description:Annotated[str,Doc('''A description of the API. Supports Markdown (using[CommonMark syntax](https://commonmark.org/)).It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(description="""ChimichangApp API helps you do awesome stuff. 🚀## ItemsYou can **read items**.## UsersYou will be able to:* **Create users** (_not implemented_).* **Read users** (_not implemented_).""")```'''),]="",version:Annotated[str,Doc("""The version of the API.**Note** This is the version of your application, not the version ofthe OpenAPI specification nor the version of FastAPI being used.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(version="0.0.1")```"""),]="0.1.0",openapi_url:Annotated[Optional[str],Doc("""The URL where the OpenAPI schema will be served from.If you set it to `None`, no OpenAPI schema will be served publicly, andthe default automatic endpoints `/docs` and `/redoc` will also bedisabled.Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(openapi_url="/api/v1/openapi.json")```"""),]="/openapi.json",openapi_tags:Annotated[Optional[list[dict[str,Any]]],Doc("""A list of tags used by OpenAPI, these are the same `tags` you can setin the *path operations*, like:* `@app.get("/users/", tags=["users"])`* `@app.get("/items/", tags=["items"])`The order of the tags can be used to specify the order shown intools like Swagger UI, used in the automatic path `/docs`.It's not required to specify all the tags used.The tags that are not declared MAY be organized randomly or basedon the tools' logic. Each tag name in the list MUST be unique.The value of each item is a `dict` containing:* `name`: The name of the tag.* `description`: A short description of the tag.[CommonMark syntax](https://commonmark.org/) MAY be used for richtext representation.* `externalDocs`: Additional external documentation for this tag. Ifprovided, it would contain a `dict` with:* `description`: A short description of the target documentation.[CommonMark syntax](https://commonmark.org/) MAY be used forrich text representation.* `url`: The URL for the target documentation. Value MUST be inthe form of a URL.Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).**Example**```pythonfrom fastapi import FastAPItags_metadata = [{"name": "users","description": "Operations with users. The **login** logic is also here.",},{"name": "items","description": "Manage items. So _fancy_ they have their own docs.","externalDocs": {"description": "Items external docs","url": "https://fastapi.tiangolo.com/",},},]app = FastAPI(openapi_tags=tags_metadata)```"""),]=None,servers:Annotated[Optional[list[dict[str,Union[str,Any]]]],Doc("""A `list` of `dict`s with connectivity information to a target server.You would use it, for example, if your application is served fromdifferent domains and you want to use the same Swagger UI in thebrowser to interact with each of them (instead of having multiplebrowser tabs open). Or if you want to leave fixed the possible URLs.If the servers `list` is not provided, or is an empty `list`, the`servers` property in the generated OpenAPI will be:* a `dict` with a `url` value of the application's mounting point(`root_path`) if it's different from `/`.* otherwise, the `servers` property will be omitted from the OpenAPIschema.Each item in the `list` is a `dict` containing:* `url`: A URL to the target host. This URL supports Server Variablesand MAY be relative, to indicate that the host location is relativeto the location where the OpenAPI document is being served. Variablesubstitutions will be made when a variable is named in `{`brackets`}`.* `description`: An optional string describing the host designated bythe URL. [CommonMark syntax](https://commonmark.org/) MAY be used forrich text representation.* `variables`: A `dict` between a variable name and its value. The valueis used for substitution in the server's URL template.Read more in the[FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(servers=[{"url": "https://stag.example.com", "description": "Staging environment"},{"url": "https://prod.example.com", "description": "Production environment"},])```"""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of global dependencies, they will be applied to each*path operation*, including in sub-routers.Read more about it in the[FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).**Example**```pythonfrom fastapi import Depends, FastAPIfrom .dependencies import func_dep_1, func_dep_2app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])```"""),]=None,default_response_class:Annotated[type[Response],Doc("""The default response class to be used.Read more in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).**Example**```pythonfrom fastapi import FastAPIfrom fastapi.responses import ORJSONResponseapp = FastAPI(default_response_class=ORJSONResponse)```"""),]=Default(JSONResponse),redirect_slashes:Annotated[bool,Doc("""Whether to detect and redirect slashes in URLs when the client doesn'tuse the same format.**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(redirect_slashes=True)  # the default@app.get("/items/")async def read_items():return [{"item_id": "Foo"}]```With this app, if a client goes to `/items` (without a trailing slash),they will be automatically redirected with an HTTP status code of 307to `/items/`."""),]=True,docs_url:Annotated[Optional[str],Doc("""The path to the automatic interactive API documentation.It is handled in the browser by Swagger UI.The default URL is `/docs`. You can disable it by setting it to `None`.If `openapi_url` is set to `None`, this will be automatically disabled.Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(docs_url="/documentation", redoc_url=None)```"""),]="/docs",redoc_url:Annotated[Optional[str],Doc("""The path to the alternative automatic interactive API documentationprovided by ReDoc.The default URL is `/redoc`. You can disable it by setting it to `None`.If `openapi_url` is set to `None`, this will be automatically disabled.Read more in the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(docs_url="/documentation", redoc_url="redocumentation")```"""),]="/redoc",swagger_ui_oauth2_redirect_url:Annotated[Optional[str],Doc("""The OAuth2 redirect endpoint for the Swagger UI.By default it is `/docs/oauth2-redirect`.This is only used if you use OAuth2 (with the "Authorize" button)with Swagger UI."""),]="/docs/oauth2-redirect",swagger_ui_init_oauth:Annotated[Optional[dict[str,Any]],Doc("""OAuth2 configuration for the Swagger UI, by default shown at `/docs`.Read more about the available configuration options in the[Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/)."""),]=None,middleware:Annotated[Optional[Sequence[Middleware]],Doc("""List of middleware to be added when creating the application.In FastAPI you would normally do this with `app.add_middleware()`instead.Read more in the[FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)."""),]=None,exception_handlers:Annotated[Optional[dict[Union[int,type[Exception]],Callable[[Request,Any],Coroutine[Any,Any,Response]],]],Doc("""A dictionary with handlers for exceptions.In FastAPI, you would normally use the decorator`@app.exception_handler()`.Read more in the[FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)."""),]=None,on_startup:Annotated[Optional[Sequence[Callable[[],Any]]],Doc("""A list of startup event handler functions.You should instead use the `lifespan` handlers.Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,on_shutdown:Annotated[Optional[Sequence[Callable[[],Any]]],Doc("""A list of shutdown event handler functions.You should instead use the `lifespan` handlers.Read more in the[FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,lifespan:Annotated[Optional[Lifespan[AppType]],Doc("""A `Lifespan` context manager handler. This replaces `startup` and`shutdown` functions with a single context manager.Read more in the[FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/)."""),]=None,terms_of_service:Annotated[Optional[str],Doc("""A URL to the Terms of Service for your API.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more at the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonapp = FastAPI(terms_of_service="http://example.com/terms/")```"""),]=None,contact:Annotated[Optional[dict[str,Union[str,Any]]],Doc("""A dictionary with the contact information for the exposed API.It can contain several fields.* `name`: (`str`) The name of the contact person/organization.* `url`: (`str`) A URL pointing to the contact information. MUST be inthe format of a URL.* `email`: (`str`) The email address of the contact person/organization.MUST be in the format of an email address.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more at the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonapp = FastAPI(contact={"name": "Deadpoolio the Amazing","url": "http://x-force.example.com/contact/","email": "dp@x-force.example.com",})```"""),]=None,license_info:Annotated[Optional[dict[str,Union[str,Any]]],Doc("""A dictionary with the license information for the exposed API.It can contain several fields.* `name`: (`str`) **REQUIRED** (if a `license_info` is set). Thelicense name used for the API.* `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expressionfor the API. The `identifier` field is mutually exclusive of the `url`field. Available since OpenAPI 3.1.0, FastAPI 0.99.0.* `url`: (`str`) A URL to the license used for the API. This MUST bethe format of a URL.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more at the[FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).**Example**```pythonapp = FastAPI(license_info={"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html",})```"""),]=None,openapi_prefix:Annotated[str,Doc("""A URL prefix for the OpenAPI URL."""),deprecated(""""openapi_prefix" has been deprecated in favor of "root_path", whichfollows more closely the ASGI standard, is simpler, and moreautomatic."""),]="",root_path:Annotated[str,Doc("""A path prefix handled by a proxy that is not seen by the applicationbut is seen by external clients, which affects things like Swagger UI.Read more about it at the[FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(root_path="/api/v1")```"""),]="",root_path_in_servers:Annotated[bool,Doc("""To disable automatically generating the URLs in the `servers` fieldin the autogenerated OpenAPI using the `root_path`.Read more about it in the[FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root_path).**Example**```pythonfrom fastapi import FastAPIapp = FastAPI(root_path_in_servers=False)```"""),]=True,responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).And in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""OpenAPI callbacks that should apply to all *path operations*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,webhooks:Annotated[Optional[routing.APIRouter],Doc("""Add OpenAPI webhooks. This is similar to `callbacks` but it doesn'tdepend on specific *path operations*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).**Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.Read more about it in the[FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark all *path operations* as deprecated. You probably don't need it,but it's available.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,include_in_schema:Annotated[bool,Doc("""To include (or not) all the *path operations* in the generated OpenAPI.You probably don't need it, but it's available.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,swagger_ui_parameters:Annotated[Optional[dict[str,Any]],Doc("""Parameters to configure Swagger UI, the autogenerated interactive APIdocumentation (by default at `/docs`).Read more about it in the[FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),separate_input_output_schemas:Annotated[bool,Doc("""Whether to generate separate OpenAPI schemas for request body andresponse body when the results would be more precise.This is particularly useful when automatically generating clients.For example, if you have a model like:```pythonfrom pydantic import BaseModelclass Item(BaseModel):name: strtags: list[str] = []```When `Item` is used for input, a request body, `tags` is not required,the client doesn't have to provide it.But when using `Item` for output, for a response body, `tags` is alwaysavailable because it has a default value, even if it's just an emptylist. So, the client should be able to always expect it.In this case, there would be two different schemas, one for input andanother one for output."""),]=True,openapi_external_docs:Annotated[Optional[dict[str,Any]],Doc("""This field allows you to provide additional external documentation links.If provided, it must be a dictionary containing:* `description`: A brief description of the external documentation.* `url`: The URL pointing to the external documentation. The value **MUST**be a valid URL format.**Example**:```pythonfrom fastapi import FastAPIexternal_docs = {"description": "Detailed API Reference","url": "https://example.com/api-docs",}app = FastAPI(openapi_external_docs=external_docs)```"""),]=None,**extra:Annotated[Any,Doc("""Extra keyword arguments to be stored in the app, not used by FastAPIanywhere."""),],)->None:self.debug=debugself.title=titleself.summary=summaryself.description=descriptionself.version=versionself.terms_of_service=terms_of_serviceself.contact=contactself.license_info=license_infoself.openapi_url=openapi_urlself.openapi_tags=openapi_tagsself.root_path_in_servers=root_path_in_serversself.docs_url=docs_urlself.redoc_url=redoc_urlself.swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_urlself.swagger_ui_init_oauth=swagger_ui_init_oauthself.swagger_ui_parameters=swagger_ui_parametersself.servers=serversor[]self.separate_input_output_schemas=separate_input_output_schemasself.openapi_external_docs=openapi_external_docsself.extra=extraself.openapi_version:Annotated[str,Doc("""The version string of OpenAPI.FastAPI will generate OpenAPI version 3.1.0, and will output that asthe OpenAPI version. But some tools, even though they might becompatible with OpenAPI 3.1.0, might not recognize it as a valid.So you could override this value to trick those tools into usingthe generated OpenAPI. Have in mind that this is a hack. But if youavoid using features added in OpenAPI 3.1.0, it might work for youruse case.This is not passed as a parameter to the `FastAPI` class to avoidgiving the false idea that FastAPI would generate a different OpenAPIschema. It is only available as an attribute.**Example**```pythonfrom fastapi import FastAPIapp = FastAPI()app.openapi_version = "3.0.2"```"""),]="3.1.0"self.openapi_schema:Optional[dict[str,Any]]=Noneifself.openapi_url:assertself.title,"A title must be provided for OpenAPI, e.g.: 'My API'"assertself.version,"A version must be provided for OpenAPI, e.g.: '2.1.0'"# TODO: remove when discarding the openapi_prefix parameterifopenapi_prefix:logger.warning('"openapi_prefix" has been deprecated in favor of "root_path", which '"follows more closely the ASGI standard, is simpler, and more ""automatic. Check the docs at ""https://fastapi.tiangolo.com/advanced/sub-applications/")self.webhooks:Annotated[routing.APIRouter,Doc("""The `app.webhooks` attribute is an `APIRouter` with the *pathoperations* that will be used just for documentation of webhooks.Read more about it in the[FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/)."""),]=webhooksorrouting.APIRouter()self.root_path=root_pathoropenapi_prefixself.state:Annotated[State,Doc("""A state object for the application. This is the same object for theentire application, it doesn't change from request to request.You normally wouldn't use this in FastAPI, for most of the cases youwould instead use FastAPI dependencies.This is simply inherited from Starlette.Read more about it in the[Starlette docs for Applications](https://www.starlette.dev/applications/#storing-state-on-the-app-instance)."""),]=State()self.dependency_overrides:Annotated[dict[Callable[...,Any],Callable[...,Any]],Doc("""A dictionary with overrides for the dependencies.Each key is the original dependency callable, and the value is theactual dependency that should be called.This is for testing, to replace expensive dependencies with testingversions.Read more about it in the[FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)."""),]={}self.router:routing.APIRouter=routing.APIRouter(routes=routes,redirect_slashes=redirect_slashes,dependency_overrides_provider=self,on_startup=on_startup,on_shutdown=on_shutdown,lifespan=lifespan,default_response_class=default_response_class,dependencies=dependencies,callbacks=callbacks,deprecated=deprecated,include_in_schema=include_in_schema,responses=responses,generate_unique_id_function=generate_unique_id_function,)self.exception_handlers:dict[Any,Callable[[Request,Any],Union[Response,Awaitable[Response]]]]={}ifexception_handlersisNoneelsedict(exception_handlers)self.exception_handlers.setdefault(HTTPException,http_exception_handler)self.exception_handlers.setdefault(RequestValidationError,request_validation_exception_handler)self.exception_handlers.setdefault(WebSocketRequestValidationError,# Starlette still has incorrect type specification for the handlerswebsocket_request_validation_exception_handler,# type: ignore)self.user_middleware:list[Middleware]=([]ifmiddlewareisNoneelselist(middleware))self.middleware_stack:Union[ASGIApp,None]=Noneself.setup() |
| --- | --- |

### openapi_versioninstance-attribute¶

```
openapi_version = '3.1.0'
```

The version string of OpenAPI.

FastAPI will generate OpenAPI version 3.1.0, and will output that as
the OpenAPI version. But some tools, even though they might be
compatible with OpenAPI 3.1.0, might not recognize it as a valid.

So you could override this value to trick those tools into using
the generated OpenAPI. Have in mind that this is a hack. But if you
avoid using features added in OpenAPI 3.1.0, it might work for your
use case.

This is not passed as a parameter to the `FastAPI` class to avoid
giving the false idea that FastAPI would generate a different OpenAPI
schema. It is only available as an attribute.

**Example**

```
from fastapi import FastAPI

app = FastAPI()

app.openapi_version = "3.0.2"
```

### webhooksinstance-attribute¶

```
webhooks = webhooks or APIRouter()
```

The `app.webhooks` attribute is an `APIRouter` with the *path
operations* that will be used just for documentation of webhooks.

Read more about it in the
[FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).

### stateinstance-attribute¶

```
state = State()
```

A state object for the application. This is the same object for the
entire application, it doesn't change from request to request.

You normally wouldn't use this in FastAPI, for most of the cases you
would instead use FastAPI dependencies.

This is simply inherited from Starlette.

Read more about it in the
[Starlette docs for Applications](https://www.starlette.dev/applications/#storing-state-on-the-app-instance).

### dependency_overridesinstance-attribute¶

```
dependency_overrides = {}
```

A dictionary with overrides for the dependencies.

Each key is the original dependency callable, and the value is the
actual dependency that should be called.

This is for testing, to replace expensive dependencies with testing
versions.

Read more about it in the
[FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).

### openapi¶

```
openapi()
```

Generate the OpenAPI schema of the application. This is called by FastAPI
internally.

The first time it is called it stores the result in the attribute
`app.openapi_schema`, and next times it is called, it just returns that same
result. To avoid the cost of generating the schema every time.

If you need to modify the generated OpenAPI schema, you could modify it.

Read more in the
[FastAPI docs for OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/).

  Source code in `fastapi/applications.py`

| 10461047104810491050105110521053105410551056105710581059106010611062106310641065106610671068106910701071107210731074107510761077 | defopenapi(self)->dict[str,Any]:"""Generate the OpenAPI schema of the application. This is called by FastAPIinternally.The first time it is called it stores the result in the attribute`app.openapi_schema`, and next times it is called, it just returns that sameresult. To avoid the cost of generating the schema every time.If you need to modify the generated OpenAPI schema, you could modify it.Read more in the[FastAPI docs for OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/)."""ifnotself.openapi_schema:self.openapi_schema=get_openapi(title=self.title,version=self.version,openapi_version=self.openapi_version,summary=self.summary,description=self.description,terms_of_service=self.terms_of_service,contact=self.contact,license_info=self.license_info,routes=self.routes,webhooks=self.webhooks.routes,tags=self.openapi_tags,servers=self.servers,separate_input_output_schemas=self.separate_input_output_schemas,external_docs=self.openapi_external_docs,)returnself.openapi_schema |
| --- | --- |

### websocket¶

```
websocket(path, name=None, *, dependencies=None)
```

Decorate a WebSocket function.

Read more about it in the
[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).

**Example**

```
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| path | WebSocket path.TYPE:str |
| name | A name for the WebSocket. Only used internally.TYPE:Optional[str]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be used for this
WebSocket.Read more about it in theFastAPI docs for WebSockets.TYPE:Optional[Sequence[Depends]]DEFAULT:None |

  Source code in `fastapi/applications.py`

| 1271127212731274127512761277127812791280128112821283128412851286128712881289129012911292129312941295129612971298129913001301130213031304130513061307130813091310131113121313131413151316131713181319132013211322132313241325132613271328132913301331133213331334 | defwebsocket(self,path:Annotated[str,Doc("""WebSocket path."""),],name:Annotated[Optional[str],Doc("""A name for the WebSocket. Only used internally."""),]=None,*,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be used for thisWebSocket.Read more about it in the[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)."""),]=None,)->Callable[[DecoratedCallable],DecoratedCallable]:"""Decorate a WebSocket function.Read more about it in the[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).**Example**```pythonfrom fastapi import FastAPI, WebSocketapp = FastAPI()@app.websocket("/ws")async def websocket_endpoint(websocket: WebSocket):await websocket.accept()while True:data = await websocket.receive_text()await websocket.send_text(f"Message text was: {data}")```"""defdecorator(func:DecoratedCallable)->DecoratedCallable:self.add_api_websocket_route(path,func,name=name,dependencies=dependencies,)returnfuncreturndecorator |
| --- | --- |

### include_router¶

```
include_router(
    router,
    *,
    prefix="",
    tags=None,
    dependencies=None,
    responses=None,
    deprecated=None,
    include_in_schema=True,
    default_response_class=Default(JSONResponse),
    callbacks=None,
    generate_unique_id_function=Default(generate_unique_id)
)
```

Include an `APIRouter` in the same app.

Read more about it in the
[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

##### Example¶

```
from fastapi import FastAPI

from .users import users_router

app = FastAPI()

app.include_router(users_router)
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| router | TheAPIRouterto include.TYPE:APIRouter |
| prefix | An optional path prefix for the router.TYPE:strDEFAULT:'' |
| tags | A list of tags to be applied to all thepath operationsin this
router.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Path Operation Configuration.TYPE:Optional[list[Union[str,Enum]]]DEFAULT:None |
| dependencies | A list of dependencies (usingDepends()) to be applied to all thepath operationsin this router.Read more about it in theFastAPI docs for Bigger Applications - Multiple Files.ExamplefromfastapiimportDepends,FastAPIfrom.dependenciesimportget_token_headerfrom.internalimportadminapp=FastAPI()app.include_router(admin.router,dependencies=[Depends(get_token_header)],)TYPE:Optional[Sequence[Depends]]DEFAULT:None |
| responses | Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for Additional Responses in OpenAPI.And in theFastAPI docs for Bigger Applications.TYPE:Optional[dict[Union[int,str],dict[str,Any]]]DEFAULT:None |
| deprecated | Mark all thepath operationsin this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at/docs).ExamplefromfastapiimportFastAPIfrom.internalimportold_apiapp=FastAPI()app.include_router(old_api.router,deprecated=True,)TYPE:Optional[bool]DEFAULT:None |
| include_in_schema | Include (or not) all thepath operationsin this router in the
generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at/docs).ExamplefromfastapiimportFastAPIfrom.internalimportold_apiapp=FastAPI()app.include_router(old_api.router,include_in_schema=False,)TYPE:boolDEFAULT:True |
| default_response_class | Default response class to be used for thepath operationsin this
router.Read more in theFastAPI docs for Custom Response - HTML, Stream, File, others.ExamplefromfastapiimportFastAPIfromfastapi.responsesimportORJSONResponsefrom.internalimportold_apiapp=FastAPI()app.include_router(old_api.router,default_response_class=ORJSONResponse,)TYPE:type[Response]DEFAULT:Default(JSONResponse) |
| callbacks | List ofpath operationsthat will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be used
directly.It will be added to the generated OpenAPI (e.g. visible at/docs).Read more about it in theFastAPI docs for OpenAPI Callbacks.TYPE:Optional[list[BaseRoute]]DEFAULT:None |
| generate_unique_id_function | Customize the function used to generate unique IDs for thepath
operationsshown in the generated OpenAPI.This is particularly useful when automatically generating clients or
SDKs for your API.Read more about it in theFastAPI docs about how to Generate Clients.TYPE:Callable[[APIRoute],str]DEFAULT:Default(generate_unique_id) |

  Source code in `fastapi/applications.py`

| 133613371338133913401341134213431344134513461347134813491350135113521353135413551356135713581359136013611362136313641365136613671368136913701371137213731374137513761377137813791380138113821383138413851386138713881389139013911392139313941395139613971398139914001401140214031404140514061407140814091410141114121413141414151416141714181419142014211422142314241425142614271428142914301431143214331434143514361437143814391440144114421443144414451446144714481449145014511452145314541455145614571458145914601461146214631464146514661467146814691470147114721473147414751476147714781479148014811482148314841485148614871488148914901491149214931494149514961497149814991500150115021503150415051506150715081509151015111512151315141515151615171518151915201521152215231524152515261527152815291530153115321533153415351536153715381539 | definclude_router(self,router:Annotated[routing.APIRouter,Doc("The `APIRouter` to include.")],*,prefix:Annotated[str,Doc("An optional path prefix for the router.")]="",tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to all the *path operations* in thisrouter.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to all the*path operations* in this router.Read more about it in the[FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).**Example**```pythonfrom fastapi import Depends, FastAPIfrom .dependencies import get_token_headerfrom .internal import adminapp = FastAPI()app.include_router(admin.router,dependencies=[Depends(get_token_header)],)```"""),]=None,responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses to be shown in OpenAPI.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).And in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark all the *path operations* in this router as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`).**Example**```pythonfrom fastapi import FastAPIfrom .internal import old_apiapp = FastAPI()app.include_router(old_api.router,deprecated=True,)```"""),]=None,include_in_schema:Annotated[bool,Doc("""Include (or not) all the *path operations* in this router in thegenerated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).**Example**```pythonfrom fastapi import FastAPIfrom .internal import old_apiapp = FastAPI()app.include_router(old_api.router,include_in_schema=False,)```"""),]=True,default_response_class:Annotated[type[Response],Doc("""Default response class to be used for the *path operations* in thisrouter.Read more in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).**Example**```pythonfrom fastapi import FastAPIfrom fastapi.responses import ORJSONResponsefrom .internal import old_apiapp = FastAPI()app.include_router(old_api.router,default_response_class=ORJSONResponse,)```"""),]=Default(JSONResponse),callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->None:"""Include an `APIRouter` in the same app.Read more about it in the[FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).## Example```pythonfrom fastapi import FastAPIfrom .users import users_routerapp = FastAPI()app.include_router(users_router)```"""self.router.include_router(router,prefix=prefix,tags=tags,dependencies=dependencies,responses=responses,deprecated=deprecated,include_in_schema=include_in_schema,default_response_class=default_response_class,callbacks=callbacks,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items():
    return [{"name": "Empanada"}, {"name": "Arepa"}]
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

  Source code in `fastapi/applications.py`

| 154115421543154415451546154715481549155015511552155315541555155615571558155915601561156215631564156515661567156815691570157115721573157415751576157715781579158015811582158315841585158615871588158915901591159215931594159515961597159815991600160116021603160416051606160716081609161016111612161316141615161616171618161916201621162216231624162516261627162816291630163116321633163416351636163716381639164016411642164316441645164616471648164916501651165216531654165516561657165816591660166116621663166416651666166716681669167016711672167316741675167616771678167916801681168216831684168516861687168816891690169116921693169416951696169716981699170017011702170317041705170617071708170917101711171217131714171517161717171817191720172117221723172417251726172717281729173017311732173317341735173617371738173917401741174217431744174517461747174817491750175117521753175417551756175717581759176017611762176317641765176617671768176917701771177217731774177517761777177817791780178117821783178417851786178717881789179017911792179317941795179617971798179918001801180218031804180518061807180818091810181118121813181418151816181718181819182018211822182318241825182618271828182918301831183218331834183518361837183818391840184118421843184418451846184718481849185018511852185318541855185618571858185918601861186218631864186518661867186818691870187118721873187418751876187718781879188018811882188318841885188618871888188918901891189218931894189518961897189818991900190119021903190419051906190719081909191019111912 | defget(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP GET operation.## Example```pythonfrom fastapi import FastAPIapp = FastAPI()@app.get("/items/")def read_items():return [{"name": "Empanada"}, {"name": "Arepa"}]```"""returnself.router.get(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.put("/items/{item_id}")
def replace_item(item_id: str, item: Item):
    return {"message": "Item replaced", "id": item_id}
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

  Source code in `fastapi/applications.py`

| 19141915191619171918191919201921192219231924192519261927192819291930193119321933193419351936193719381939194019411942194319441945194619471948194919501951195219531954195519561957195819591960196119621963196419651966196719681969197019711972197319741975197619771978197919801981198219831984198519861987198819891990199119921993199419951996199719981999200020012002200320042005200620072008200920102011201220132014201520162017201820192020202120222023202420252026202720282029203020312032203320342035203620372038203920402041204220432044204520462047204820492050205120522053205420552056205720582059206020612062206320642065206620672068206920702071207220732074207520762077207820792080208120822083208420852086208720882089209020912092209320942095209620972098209921002101210221032104210521062107210821092110211121122113211421152116211721182119212021212122212321242125212621272128212921302131213221332134213521362137213821392140214121422143214421452146214721482149215021512152215321542155215621572158215921602161216221632164216521662167216821692170217121722173217421752176217721782179218021812182218321842185218621872188218921902191219221932194219521962197219821992200220122022203220422052206220722082209221022112212221322142215221622172218221922202221222222232224222522262227222822292230223122322233223422352236223722382239224022412242224322442245224622472248224922502251225222532254225522562257225822592260226122622263226422652266226722682269227022712272227322742275227622772278227922802281228222832284228522862287228822892290 | defput(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP PUT operation.## Example```pythonfrom fastapi import FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()@app.put("/items/{item_id}")def replace_item(item_id: str, item: Item):return {"message": "Item replaced", "id": item_id}```"""returnself.router.put(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created"}
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

  Source code in `fastapi/applications.py`

| 22922293229422952296229722982299230023012302230323042305230623072308230923102311231223132314231523162317231823192320232123222323232423252326232723282329233023312332233323342335233623372338233923402341234223432344234523462347234823492350235123522353235423552356235723582359236023612362236323642365236623672368236923702371237223732374237523762377237823792380238123822383238423852386238723882389239023912392239323942395239623972398239924002401240224032404240524062407240824092410241124122413241424152416241724182419242024212422242324242425242624272428242924302431243224332434243524362437243824392440244124422443244424452446244724482449245024512452245324542455245624572458245924602461246224632464246524662467246824692470247124722473247424752476247724782479248024812482248324842485248624872488248924902491249224932494249524962497249824992500250125022503250425052506250725082509251025112512251325142515251625172518251925202521252225232524252525262527252825292530253125322533253425352536253725382539254025412542254325442545254625472548254925502551255225532554255525562557255825592560256125622563256425652566256725682569257025712572257325742575257625772578257925802581258225832584258525862587258825892590259125922593259425952596259725982599260026012602260326042605260626072608260926102611261226132614261526162617261826192620262126222623262426252626262726282629263026312632263326342635263626372638263926402641264226432644264526462647264826492650265126522653265426552656265726582659266026612662266326642665266626672668 | defpost(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP POST operation.## Example```pythonfrom fastapi import FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()@app.post("/items/")def create_item(item: Item):return {"message": "Item created"}```"""returnself.router.post(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI

app = FastAPI()

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    return {"message": "Item deleted"}
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

  Source code in `fastapi/applications.py`

| 267026712672267326742675267626772678267926802681268226832684268526862687268826892690269126922693269426952696269726982699270027012702270327042705270627072708270927102711271227132714271527162717271827192720272127222723272427252726272727282729273027312732273327342735273627372738273927402741274227432744274527462747274827492750275127522753275427552756275727582759276027612762276327642765276627672768276927702771277227732774277527762777277827792780278127822783278427852786278727882789279027912792279327942795279627972798279928002801280228032804280528062807280828092810281128122813281428152816281728182819282028212822282328242825282628272828282928302831283228332834283528362837283828392840284128422843284428452846284728482849285028512852285328542855285628572858285928602861286228632864286528662867286828692870287128722873287428752876287728782879288028812882288328842885288628872888288928902891289228932894289528962897289828992900290129022903290429052906290729082909291029112912291329142915291629172918291929202921292229232924292529262927292829292930293129322933293429352936293729382939294029412942294329442945294629472948294929502951295229532954295529562957295829592960296129622963296429652966296729682969297029712972297329742975297629772978297929802981298229832984298529862987298829892990299129922993299429952996299729982999300030013002300330043005300630073008300930103011301230133014301530163017301830193020302130223023302430253026302730283029303030313032303330343035303630373038303930403041 | defdelete(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP DELETE operation.## Example```pythonfrom fastapi import FastAPIapp = FastAPI()@app.delete("/items/{item_id}")def delete_item(item_id: str):return {"message": "Item deleted"}```"""returnself.router.delete(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI

app = FastAPI()

@app.options("/items/")
def get_item_options():
    return {"additions": ["Aji", "Guacamole"]}
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

  Source code in `fastapi/applications.py`

| 304330443045304630473048304930503051305230533054305530563057305830593060306130623063306430653066306730683069307030713072307330743075307630773078307930803081308230833084308530863087308830893090309130923093309430953096309730983099310031013102310331043105310631073108310931103111311231133114311531163117311831193120312131223123312431253126312731283129313031313132313331343135313631373138313931403141314231433144314531463147314831493150315131523153315431553156315731583159316031613162316331643165316631673168316931703171317231733174317531763177317831793180318131823183318431853186318731883189319031913192319331943195319631973198319932003201320232033204320532063207320832093210321132123213321432153216321732183219322032213222322332243225322632273228322932303231323232333234323532363237323832393240324132423243324432453246324732483249325032513252325332543255325632573258325932603261326232633264326532663267326832693270327132723273327432753276327732783279328032813282328332843285328632873288328932903291329232933294329532963297329832993300330133023303330433053306330733083309331033113312331333143315331633173318331933203321332233233324332533263327332833293330333133323333333433353336333733383339334033413342334333443345334633473348334933503351335233533354335533563357335833593360336133623363336433653366336733683369337033713372337333743375337633773378337933803381338233833384338533863387338833893390339133923393339433953396339733983399340034013402340334043405340634073408340934103411341234133414 | defoptions(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP OPTIONS operation.## Example```pythonfrom fastapi import FastAPIapp = FastAPI()@app.options("/items/")def get_item_options():return {"additions": ["Aji", "Guacamole"]}```"""returnself.router.options(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI, Response

app = FastAPI()

@app.head("/items/", status_code=204)
def get_items_headers(response: Response):
    response.headers["X-Cat-Dog"] = "Alone in the world"
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

  Source code in `fastapi/applications.py`

| 341634173418341934203421342234233424342534263427342834293430343134323433343434353436343734383439344034413442344334443445344634473448344934503451345234533454345534563457345834593460346134623463346434653466346734683469347034713472347334743475347634773478347934803481348234833484348534863487348834893490349134923493349434953496349734983499350035013502350335043505350635073508350935103511351235133514351535163517351835193520352135223523352435253526352735283529353035313532353335343535353635373538353935403541354235433544354535463547354835493550355135523553355435553556355735583559356035613562356335643565356635673568356935703571357235733574357535763577357835793580358135823583358435853586358735883589359035913592359335943595359635973598359936003601360236033604360536063607360836093610361136123613361436153616361736183619362036213622362336243625362636273628362936303631363236333634363536363637363836393640364136423643364436453646364736483649365036513652365336543655365636573658365936603661366236633664366536663667366836693670367136723673367436753676367736783679368036813682368336843685368636873688368936903691369236933694369536963697369836993700370137023703370437053706370737083709371037113712371337143715371637173718371937203721372237233724372537263727372837293730373137323733373437353736373737383739374037413742374337443745374637473748374937503751375237533754375537563757375837593760376137623763376437653766376737683769377037713772377337743775377637773778377937803781378237833784378537863787 | defhead(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP HEAD operation.## Example```pythonfrom fastapi import FastAPI, Responseapp = FastAPI()@app.head("/items/", status_code=204)def get_items_headers(response: Response):response.headers["X-Cat-Dog"] = "Alone in the world"```"""returnself.router.head(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()

@app.patch("/items/")
def update_item(item: Item):
    return {"message": "Item updated in place"}
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

  Source code in `fastapi/applications.py`

| 37893790379137923793379437953796379737983799380038013802380338043805380638073808380938103811381238133814381538163817381838193820382138223823382438253826382738283829383038313832383338343835383638373838383938403841384238433844384538463847384838493850385138523853385438553856385738583859386038613862386338643865386638673868386938703871387238733874387538763877387838793880388138823883388438853886388738883889389038913892389338943895389638973898389939003901390239033904390539063907390839093910391139123913391439153916391739183919392039213922392339243925392639273928392939303931393239333934393539363937393839393940394139423943394439453946394739483949395039513952395339543955395639573958395939603961396239633964396539663967396839693970397139723973397439753976397739783979398039813982398339843985398639873988398939903991399239933994399539963997399839994000400140024003400440054006400740084009401040114012401340144015401640174018401940204021402240234024402540264027402840294030403140324033403440354036403740384039404040414042404340444045404640474048404940504051405240534054405540564057405840594060406140624063406440654066406740684069407040714072407340744075407640774078407940804081408240834084408540864087408840894090409140924093409440954096409740984099410041014102410341044105410641074108410941104111411241134114411541164117411841194120412141224123412441254126412741284129413041314132413341344135413641374138413941404141414241434144414541464147414841494150415141524153415441554156415741584159416041614162416341644165 | defpatch(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP PATCH operation.## Example```pythonfrom fastapi import FastAPIfrom pydantic import BaseModelclass Item(BaseModel):name: strdescription: str | None = Noneapp = FastAPI()@app.patch("/items/")def update_item(item: Item):return {"message": "Item updated in place"}```"""returnself.router.patch(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
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
from fastapi import FastAPI

app = FastAPI()

@app.trace("/items/{item_id}")
def trace_item(item_id: str):
    return None
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

  Source code in `fastapi/applications.py`

| 416741684169417041714172417341744175417641774178417941804181418241834184418541864187418841894190419141924193419441954196419741984199420042014202420342044205420642074208420942104211421242134214421542164217421842194220422142224223422442254226422742284229423042314232423342344235423642374238423942404241424242434244424542464247424842494250425142524253425442554256425742584259426042614262426342644265426642674268426942704271427242734274427542764277427842794280428142824283428442854286428742884289429042914292429342944295429642974298429943004301430243034304430543064307430843094310431143124313431443154316431743184319432043214322432343244325432643274328432943304331433243334334433543364337433843394340434143424343434443454346434743484349435043514352435343544355435643574358435943604361436243634364436543664367436843694370437143724373437443754376437743784379438043814382438343844385438643874388438943904391439243934394439543964397439843994400440144024403440444054406440744084409441044114412441344144415441644174418441944204421442244234424442544264427442844294430443144324433443444354436443744384439444044414442444344444445444644474448444944504451445244534454445544564457445844594460446144624463446444654466446744684469447044714472447344744475447644774478447944804481448244834484448544864487448844894490449144924493449444954496449744984499450045014502450345044505450645074508450945104511451245134514451545164517451845194520452145224523452445254526452745284529453045314532453345344535453645374538 | deftrace(self,path:Annotated[str,Doc("""The URL path to be used for this *path operation*.For example, in `http://example.com/items`, the path is `/items`."""),],*,response_model:Annotated[Any,Doc("""The type to use for the response.It could be any valid Pydantic *field* type. So, it doesn't have tobe a Pydantic model, it could be other things, like a `list`, `dict`,etc.It will be used for:* Documentation: the generated OpenAPI (and the UI at `/docs`) willshow it as the response (JSON Schema).* Serialization: you could return an arbitrary object and the`response_model` would be used to serialize that object into thecorresponding JSON.* Filtering: the JSON sent to the client will only contain the data(fields) defined in the `response_model`. If you returned an objectthat contains an attribute `password` but the `response_model` doesnot include that field, the JSON sent to the client would not havethat `password`.* Validation: whatever you return will be serialized with the`response_model`, converting any data as necessary to generate thecorresponding JSON. But if the data in the object returned is notvalid, that would mean a violation of the contract with the client,so it's an error from the API developer. So, FastAPI will raise anerror and return a 500 error code (Internal Server Error).Read more about it in the[FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)."""),]=Default(None),status_code:Annotated[Optional[int],Doc("""The default status code to be used for the response.You could override the status code by returning a response directly.Read more about it in the[FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)."""),]=None,tags:Annotated[Optional[list[Union[str,Enum]]],Doc("""A list of tags to be applied to the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags)."""),]=None,dependencies:Annotated[Optional[Sequence[Depends]],Doc("""A list of dependencies (using `Depends()`) to be applied to the*path operation*.Read more about it in the[FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)."""),]=None,summary:Annotated[Optional[str],Doc("""A summary for the *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,description:Annotated[Optional[str],Doc("""A description for the *path operation*.If not provided, it will be extracted automatically from the docstringof the *path operation function*.It can contain Markdown.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)."""),]=None,response_description:Annotated[str,Doc("""The description for the default response.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]="Successful Response",responses:Annotated[Optional[dict[Union[int,str],dict[str,Any]]],Doc("""Additional responses that could be returned by this *path operation*.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,deprecated:Annotated[Optional[bool],Doc("""Mark this *path operation* as deprecated.It will be added to the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,operation_id:Annotated[Optional[str],Doc("""Custom operation ID to be used by this *path operation*.By default, it is generated automatically.If you provide a custom operation ID, you need to make sure it isunique for the whole API.You can customize theoperation ID generation with the parameter`generate_unique_id_function` in the `FastAPI` class.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=None,response_model_include:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to include only certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_exclude:Annotated[Optional[IncEx],Doc("""Configuration passed to Pydantic to exclude certain fields in theresponse data.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=None,response_model_by_alias:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response modelshould be serialized by alias when an alias is used.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude)."""),]=True,response_model_exclude_unset:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that were not set andhave their default values. This is different from`response_model_exclude_defaults` in that if the fields are set,they will be included in the response, even if the value is the sameas the default.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_defaults:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response datashould have all the fields, including the ones that have the same valueas the default. This is different from `response_model_exclude_unset`in that if the fields are set but contain the same default values,they will be excluded from the response.When `True`, default values are omitted from the response.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter)."""),]=False,response_model_exclude_none:Annotated[bool,Doc("""Configuration passed to Pydantic to define if the response data shouldexclude fields set to `None`.This is much simpler (less smart) than `response_model_exclude_unset`and `response_model_exclude_defaults`. You probably want to use one ofthose two instead of this one, as those allow returning `None` valueswhen it makes sense.Read more about it in the[FastAPI docs for Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_exclude_none)."""),]=False,include_in_schema:Annotated[bool,Doc("""Include this *path operation* in the generated OpenAPI schema.This affects the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi)."""),]=True,response_class:Annotated[type[Response],Doc("""Response class to be used for this *path operation*.This will not be used if you return a response directly.Read more about it in the[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#redirectresponse)."""),]=Default(JSONResponse),name:Annotated[Optional[str],Doc("""Name for this *path operation*. Only used internally."""),]=None,callbacks:Annotated[Optional[list[BaseRoute]],Doc("""List of *path operations* that will be used as OpenAPI callbacks.This is only for OpenAPI documentation, the callbacks won't be useddirectly.It will be added to the generated OpenAPI (e.g. visible at `/docs`).Read more about it in the[FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/)."""),]=None,openapi_extra:Annotated[Optional[dict[str,Any]],Doc("""Extra metadata to be included in the OpenAPI schema for this *pathoperation*.Read more about it in the[FastAPI docs for Path Operation Advanced Configuration](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#custom-openapi-path-operation-schema)."""),]=None,generate_unique_id_function:Annotated[Callable[[routing.APIRoute],str],Doc("""Customize the function used to generate unique IDs for the *pathoperations* shown in the generated OpenAPI.This is particularly useful when automatically generating clients orSDKs for your API.Read more about it in the[FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function)."""),]=Default(generate_unique_id),)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a *path operation* using an HTTP TRACE operation.## Example```pythonfrom fastapi import FastAPIapp = FastAPI()@app.trace("/items/{item_id}")def trace_item(item_id: str):return None```"""returnself.router.trace(path,response_model=response_model,status_code=status_code,tags=tags,dependencies=dependencies,summary=summary,description=description,response_description=response_description,responses=responses,deprecated=deprecated,operation_id=operation_id,response_model_include=response_model_include,response_model_exclude=response_model_exclude,response_model_by_alias=response_model_by_alias,response_model_exclude_unset=response_model_exclude_unset,response_model_exclude_defaults=response_model_exclude_defaults,response_model_exclude_none=response_model_exclude_none,include_in_schema=include_in_schema,response_class=response_class,name=name,callbacks=callbacks,openapi_extra=openapi_extra,generate_unique_id_function=generate_unique_id_function,) |
| --- | --- |

### on_event¶

```
on_event(event_type)
```

Add an event handler for the application.

`on_event` is deprecated, use `lifespan` event handlers instead.

Read more about it in the
[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated).

| PARAMETER | DESCRIPTION |
| --- | --- |
| event_type | The type of event.startuporshutdown.TYPE:str |

  Source code in `fastapi/applications.py`

| 4549455045514552455345544555455645574558455945604561456245634564456545664567456845694570457145724573457445754576 | @deprecated("""on_event is deprecated, use lifespan event handlers instead.Read more about it in the[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).""")defon_event(self,event_type:Annotated[str,Doc("""The type of event. `startup` or `shutdown`."""),],)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add an event handler for the application.`on_event` is deprecated, use `lifespan` event handlers instead.Read more about it in the[FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated)."""returnself.router.on_event(event_type) |
| --- | --- |

### middleware¶

```
middleware(middleware_type)
```

Add a middleware to the application.

Read more about it in the
[FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).

##### Example¶

```
import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| middleware_type | The type of middleware. Currently only supportshttp.TYPE:str |

  Source code in `fastapi/applications.py`

| 457845794580458145824583458445854586458745884589459045914592459345944595459645974598459946004601460246034604460546064607460846094610461146124613461446154616461746184619462046214622 | defmiddleware(self,middleware_type:Annotated[str,Doc("""The type of middleware. Currently only supports `http`."""),],)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add a middleware to the application.Read more about it in the[FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).## Example```pythonimport timefrom typing import Awaitable, Callablefrom fastapi import FastAPI, Request, Responseapp = FastAPI()@app.middleware("http")async def add_process_time_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:start_time = time.time()response = await call_next(request)process_time = time.time() - start_timeresponse.headers["X-Process-Time"] = str(process_time)return response```"""defdecorator(func:DecoratedCallable)->DecoratedCallable:self.add_middleware(BaseHTTPMiddleware,dispatch=func)returnfuncreturndecorator |
| --- | --- |

### exception_handler¶

```
exception_handler(exc_class_or_status_code)
```

Add an exception handler to the app.

Read more about it in the
[FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).

##### Example¶

```
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| exc_class_or_status_code | The Exception class this would handle, or a status code.TYPE:Union[int,type[Exception]] |

  Source code in `fastapi/applications.py`

| 4624462546264627462846294630463146324633463446354636463746384639464046414642464346444645464646474648464946504651465246534654465546564657465846594660466146624663466446654666466746684669 | defexception_handler(self,exc_class_or_status_code:Annotated[Union[int,type[Exception]],Doc("""The Exception class this would handle, or a status code."""),],)->Callable[[DecoratedCallable],DecoratedCallable]:"""Add an exception handler to the app.Read more about it in the[FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).## Example```pythonfrom fastapi import FastAPI, Requestfrom fastapi.responses import JSONResponseclass UnicornException(Exception):def __init__(self, name: str):self.name = nameapp = FastAPI()@app.exception_handler(UnicornException)async def unicorn_exception_handler(request: Request, exc: UnicornException):return JSONResponse(status_code=418,content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},)```"""defdecorator(func:DecoratedCallable)->DecoratedCallable:self.add_exception_handler(exc_class_or_status_code,func)returnfuncreturndecorator |
| --- | --- |
