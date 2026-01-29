# Background Tasks and more

# Background Tasks

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Background Tasks -BackgroundTasks¶

You can declare a parameter in a *path operation function* or dependency function with the type `BackgroundTasks`, and then you can use it to schedule the execution of background tasks after the response is sent.

You can import it directly from `fastapi`:

```
from fastapi import BackgroundTasks
```

## fastapi.BackgroundTasks¶

```
BackgroundTasks(tasks=None)
```

Bases: `BackgroundTasks`

A collection of background tasks that will be called after a response has been
sent to the client.

Read more about it in the
[FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

#### Example¶

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

  Source code in `starlette/background.py`

| 2728 | def__init__(self,tasks:Sequence[BackgroundTask]|None=None):self.tasks=list(tasks)iftaskselse[] |
| --- | --- |

### funcinstance-attribute¶

```
func = func
```

### argsinstance-attribute¶

```
args = args
```

### kwargsinstance-attribute¶

```
kwargs = kwargs
```

### is_asyncinstance-attribute¶

```
is_async = is_async_callable(func)
```

### tasksinstance-attribute¶

```
tasks = list(tasks) if tasks else []
```

### add_task¶

```
add_task(func, *args, **kwargs)
```

Add a function to be called in the background after the response is sent.

Read more about it in the
[FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| func | The function to call after the response is sent.It can be a regulardeffunction or anasync deffunction.TYPE:Callable[P,Any] |

  Source code in `fastapi/background.py`

| 39404142434445464748495051525354555657585960 | defadd_task(self,func:Annotated[Callable[P,Any],Doc("""The function to call after the response is sent.It can be a regular `def` function or an `async def` function."""),],*args:P.args,**kwargs:P.kwargs,)->None:"""Add a function to be called in the background after the response is sent.Read more about it in the[FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)."""returnsuper().add_task(func,*args,**kwargs) |
| --- | --- |

---

# Dependencies

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Dependencies -Depends()andSecurity()¶

## Depends()¶

Dependencies are handled mainly with the special function `Depends()` that takes a callable.

Here is the reference for it and its parameters.

You can import it directly from `fastapi`:

```
from fastapi import Depends
```

## fastapi.Depends¶

```
Depends(dependency=None, *, use_cache=True, scope=None)
```

Declare a FastAPI dependency.

It takes a single "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you.

Read more about it in the
[FastAPI docs for Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).

**Example**

```
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| dependency | A "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you, just pass the object
directly.TYPE:Optional[Callable[...,Any]]DEFAULT:None |
| use_cache | By default, after a dependency is called the first time in a request, if
the dependency is declared again for the rest of the request (for example
if the dependency is needed by several dependencies), the value will be
re-used for the rest of the request.Setuse_cachetoFalseto disable this behavior and ensure the
dependency is called again (if declared more than once) in the same request.TYPE:boolDEFAULT:True |
| scope | Mainly for dependencies withyield, define when the dependency function
should start (the code beforeyield) and when it should end (the code
afteryield)."function": start the dependency before thepath operation functionthat handles the request, end the dependency after thepath operation
    functionends, butbeforethe response is sent back to the client.
    So, the dependency function will be executedaroundthepath operationfunction."request": start the dependency before thepath operation functionthat handles the request (similar to when using"function"), but endafterthe response is sent back to the client. So, the dependency
    function will be executedaroundtherequestand response cycle.TYPE:Union[Literal['function', 'request'], None]DEFAULT:None |

  Source code in `fastapi/param_functions.py`

| 220922102211221222132214221522162217221822192220222122222223222422252226222722282229223022312232223322342235223622372238223922402241224222432244224522462247224822492250225122522253225422552256225722582259226022612262226322642265226622672268226922702271227222732274227522762277227822792280228122822283228422852286 | defDepends(# noqa: N802dependency:Annotated[Optional[Callable[...,Any]],Doc("""A "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you, just pass the objectdirectly."""),]=None,*,use_cache:Annotated[bool,Doc("""By default, after a dependency is called the first time in a request, ifthe dependency is declared again for the rest of the request (for exampleif the dependency is needed by several dependencies), the value will bere-used for the rest of the request.Set `use_cache` to `False` to disable this behavior and ensure thedependency is called again (if declared more than once) in the same request."""),]=True,scope:Annotated[Union[Literal["function","request"],None],Doc("""Mainly for dependencies with `yield`, define when the dependency functionshould start (the code before `yield`) and when it should end (the codeafter `yield`).* `"function"`: start the dependency before the *path operation function*that handles the request, end the dependency after the *path operationfunction* ends, but **before** the response is sent back to the client.So, the dependency function will be executed **around** the *path operation**function***.* `"request"`: start the dependency before the *path operation function*that handles the request (similar to when using `"function"`), but end**after** the response is sent back to the client. So, the dependencyfunction will be executed **around** the **request** and response cycle."""),]=None,)->Any:"""Declare a FastAPI dependency.It takes a single "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you.Read more about it in the[FastAPI docs for Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).**Example**```pythonfrom typing import Annotatedfrom fastapi import Depends, FastAPIapp = FastAPI()async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):return {"q": q, "skip": skip, "limit": limit}@app.get("/items/")async def read_items(commons: Annotated[dict, Depends(common_parameters)]):return commons```"""returnparams.Depends(dependency=dependency,use_cache=use_cache,scope=scope) |
| --- | --- |

## Security()¶

For many scenarios, you can handle security (authorization, authentication, etc.) with dependencies, using `Depends()`.

But when you want to also declare OAuth2 scopes, you can use `Security()` instead of `Depends()`.

You can import `Security()` directly from `fastapi`:

```
from fastapi import Security
```

## fastapi.Security¶

```
Security(dependency=None, *, scopes=None, use_cache=True)
```

Declare a FastAPI Security dependency.

The only difference with a regular dependency is that it can declare OAuth2
scopes that will be integrated with OpenAPI and the automatic UI docs (by default
at `/docs`).

It takes a single "dependable" callable (like a function).

Don't call it directly, FastAPI will call it for you.

Read more about it in the
[FastAPI docs for Security](https://fastapi.tiangolo.com/tutorial/security/) and
in the
[FastAPI docs for OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).

**Example**

```
from typing import Annotated

from fastapi import Security, FastAPI

from .db import User
from .security import get_current_active_user

app = FastAPI()

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| dependency | A "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you, just pass the object
directly.TYPE:Optional[Callable[...,Any]]DEFAULT:None |
| scopes | OAuth2 scopes required for thepath operationthat uses this Security
dependency.The term "scope" comes from the OAuth2 specification, it seems to be
intentionally vague and interpretable. It normally refers to permissions,
in cases to roles.These scopes are integrated with OpenAPI (and the API docs at/docs).
So they are visible in the OpenAPI specification.
)TYPE:Optional[Sequence[str]]DEFAULT:None |
| use_cache | By default, after a dependency is called the first time in a request, if
the dependency is declared again for the rest of the request (for example
if the dependency is needed by several dependencies), the value will be
re-used for the rest of the request.Setuse_cachetoFalseto disable this behavior and ensure the
dependency is called again (if declared more than once) in the same request.TYPE:boolDEFAULT:True |

  Source code in `fastapi/param_functions.py`

| 228922902291229222932294229522962297229822992300230123022303230423052306230723082309231023112312231323142315231623172318231923202321232223232324232523262327232823292330233123322333233423352336233723382339234023412342234323442345234623472348234923502351235223532354235523562357235823592360236123622363236423652366236723682369 | defSecurity(# noqa: N802dependency:Annotated[Optional[Callable[...,Any]],Doc("""A "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you, just pass the objectdirectly."""),]=None,*,scopes:Annotated[Optional[Sequence[str]],Doc("""OAuth2 scopes required for the *path operation* that uses this Securitydependency.The term "scope" comes from the OAuth2 specification, it seems to beintentionally vague and interpretable. It normally refers to permissions,in cases to roles.These scopes are integrated with OpenAPI (and the API docs at `/docs`).So they are visible in the OpenAPI specification.)"""),]=None,use_cache:Annotated[bool,Doc("""By default, after a dependency is called the first time in a request, ifthe dependency is declared again for the rest of the request (for exampleif the dependency is needed by several dependencies), the value will bere-used for the rest of the request.Set `use_cache` to `False` to disable this behavior and ensure thedependency is called again (if declared more than once) in the same request."""),]=True,)->Any:"""Declare a FastAPI Security dependency.The only difference with a regular dependency is that it can declare OAuth2scopes that will be integrated with OpenAPI and the automatic UI docs (by defaultat `/docs`).It takes a single "dependable" callable (like a function).Don't call it directly, FastAPI will call it for you.Read more about it in the[FastAPI docs for Security](https://fastapi.tiangolo.com/tutorial/security/) andin the[FastAPI docs for OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).**Example**```pythonfrom typing import Annotatedfrom fastapi import Security, FastAPIfrom .db import Userfrom .security import get_current_active_userapp = FastAPI()@app.get("/users/me/items/")async def read_own_items(current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]):return [{"item_id": "Foo", "owner": current_user.username}]```"""returnparams.Security(dependency=dependency,scopes=scopes,use_cache=use_cache) |
| --- | --- |

---

# Encoders

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Encoders -jsonable_encoder¶

## fastapi.encoders.jsonable_encoder¶

```
jsonable_encoder(
    obj,
    include=None,
    exclude=None,
    by_alias=True,
    exclude_unset=False,
    exclude_defaults=False,
    exclude_none=False,
    custom_encoder=None,
    sqlalchemy_safe=True,
)
```

Convert any object to something that can be encoded in JSON.

This is used internally by FastAPI to make sure anything you return can be
encoded as JSON before it is sent to the client.

You can also use it yourself, for example to convert objects before saving them
in a database that supports only JSON.

Read more about it in the
[FastAPI docs for JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| obj | The input object to convert to JSON.TYPE:Any |
| include | Pydantic'sincludeparameter, passed to Pydantic models to set the
fields to include.TYPE:Optional[IncEx]DEFAULT:None |
| exclude | Pydantic'sexcludeparameter, passed to Pydantic models to set the
fields to exclude.TYPE:Optional[IncEx]DEFAULT:None |
| by_alias | Pydantic'sby_aliasparameter, passed to Pydantic models to define if
the output should use the alias names (when provided) or the Python
attribute names. In an API, if you set an alias, it's probably because you
want to use it in the result, so you probably want to leave this set toTrue.TYPE:boolDEFAULT:True |
| exclude_unset | Pydantic'sexclude_unsetparameter, passed to Pydantic models to define
if it should exclude from the output the fields that were not explicitly
set (and that only had their default values).TYPE:boolDEFAULT:False |
| exclude_defaults | Pydantic'sexclude_defaultsparameter, passed to Pydantic models to define
if it should exclude from the output the fields that had the same default
value, even when they were explicitly set.TYPE:boolDEFAULT:False |
| exclude_none | Pydantic'sexclude_noneparameter, passed to Pydantic models to define
if it should exclude from the output any fields that have aNonevalue.TYPE:boolDEFAULT:False |
| custom_encoder | Pydantic'scustom_encoderparameter, passed to Pydantic models to define
a custom encoder.TYPE:Optional[dict[Any,Callable[[Any],Any]]]DEFAULT:None |
| sqlalchemy_safe | Exclude from the output any fields that start with the name_sa.This is mainly a hack for compatibility with SQLAlchemy objects, they
store internal SQLAlchemy-specific state in attributes named with_sa,
and those objects can't (and shouldn't be) serialized to JSON.TYPE:boolDEFAULT:True |

  Source code in `fastapi/encoders.py`

| 111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331332333334335336337338339340341342343344345346 | defjsonable_encoder(obj:Annotated[Any,Doc("""The input object to convert to JSON."""),],include:Annotated[Optional[IncEx],Doc("""Pydantic's `include` parameter, passed to Pydantic models to set thefields to include."""),]=None,exclude:Annotated[Optional[IncEx],Doc("""Pydantic's `exclude` parameter, passed to Pydantic models to set thefields to exclude."""),]=None,by_alias:Annotated[bool,Doc("""Pydantic's `by_alias` parameter, passed to Pydantic models to define ifthe output should use the alias names (when provided) or the Pythonattribute names. In an API, if you set an alias, it's probably because youwant to use it in the result, so you probably want to leave this set to`True`."""),]=True,exclude_unset:Annotated[bool,Doc("""Pydantic's `exclude_unset` parameter, passed to Pydantic models to defineif it should exclude from the output the fields that were not explicitlyset (and that only had their default values)."""),]=False,exclude_defaults:Annotated[bool,Doc("""Pydantic's `exclude_defaults` parameter, passed to Pydantic models to defineif it should exclude from the output the fields that had the same defaultvalue, even when they were explicitly set."""),]=False,exclude_none:Annotated[bool,Doc("""Pydantic's `exclude_none` parameter, passed to Pydantic models to defineif it should exclude from the output any fields that have a `None` value."""),]=False,custom_encoder:Annotated[Optional[dict[Any,Callable[[Any],Any]]],Doc("""Pydantic's `custom_encoder` parameter, passed to Pydantic models to definea custom encoder."""),]=None,sqlalchemy_safe:Annotated[bool,Doc("""Exclude from the output any fields that start with the name `_sa`.This is mainly a hack for compatibility with SQLAlchemy objects, theystore internal SQLAlchemy-specific state in attributes named with `_sa`,and those objects can't (and shouldn't be) serialized to JSON."""),]=True,)->Any:"""Convert any object to something that can be encoded in JSON.This is used internally by FastAPI to make sure anything you return can beencoded as JSON before it is sent to the client.You can also use it yourself, for example to convert objects before saving themin a database that supports only JSON.Read more about it in the[FastAPI docs for JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/)."""custom_encoder=custom_encoderor{}ifcustom_encoder:iftype(obj)incustom_encoder:returncustom_encoder[type(obj)](obj)else:forencoder_type,encoder_instanceincustom_encoder.items():ifisinstance(obj,encoder_type):returnencoder_instance(obj)ifincludeisnotNoneandnotisinstance(include,(set,dict)):include=set(include)ifexcludeisnotNoneandnotisinstance(exclude,(set,dict)):exclude=set(exclude)ifisinstance(obj,BaseModel):obj_dict=obj.model_dump(mode="json",include=include,exclude=exclude,by_alias=by_alias,exclude_unset=exclude_unset,exclude_none=exclude_none,exclude_defaults=exclude_defaults,)returnjsonable_encoder(obj_dict,exclude_none=exclude_none,exclude_defaults=exclude_defaults,sqlalchemy_safe=sqlalchemy_safe,)ifdataclasses.is_dataclass(obj):assertnotisinstance(obj,type)obj_dict=dataclasses.asdict(obj)returnjsonable_encoder(obj_dict,include=include,exclude=exclude,by_alias=by_alias,exclude_unset=exclude_unset,exclude_defaults=exclude_defaults,exclude_none=exclude_none,custom_encoder=custom_encoder,sqlalchemy_safe=sqlalchemy_safe,)ifisinstance(obj,Enum):returnobj.valueifisinstance(obj,PurePath):returnstr(obj)ifisinstance(obj,(str,int,float,type(None))):returnobjifisinstance(obj,PydanticUndefinedType):returnNoneifisinstance(obj,dict):encoded_dict={}allowed_keys=set(obj.keys())ifincludeisnotNone:allowed_keys&=set(include)ifexcludeisnotNone:allowed_keys-=set(exclude)forkey,valueinobj.items():if((notsqlalchemy_safeor(notisinstance(key,str))or(notkey.startswith("_sa")))and(valueisnotNoneornotexclude_none)andkeyinallowed_keys):encoded_key=jsonable_encoder(key,by_alias=by_alias,exclude_unset=exclude_unset,exclude_none=exclude_none,custom_encoder=custom_encoder,sqlalchemy_safe=sqlalchemy_safe,)encoded_value=jsonable_encoder(value,by_alias=by_alias,exclude_unset=exclude_unset,exclude_none=exclude_none,custom_encoder=custom_encoder,sqlalchemy_safe=sqlalchemy_safe,)encoded_dict[encoded_key]=encoded_valuereturnencoded_dictifisinstance(obj,(list,set,frozenset,GeneratorType,tuple,deque)):encoded_list=[]foriteminobj:encoded_list.append(jsonable_encoder(item,include=include,exclude=exclude,by_alias=by_alias,exclude_unset=exclude_unset,exclude_defaults=exclude_defaults,exclude_none=exclude_none,custom_encoder=custom_encoder,sqlalchemy_safe=sqlalchemy_safe,))returnencoded_listiftype(obj)inENCODERS_BY_TYPE:returnENCODERS_BY_TYPE[type(obj)](obj)forencoder,classes_tupleinencoders_by_class_tuples.items():ifisinstance(obj,classes_tuple):returnencoder(obj)ifis_pydantic_v1_model_instance(obj):raisePydanticV1NotSupportedError("pydantic.v1 models are no longer supported by FastAPI."f" Please update the model{obj!r}.")try:data=dict(obj)exceptExceptionase:errors:list[Exception]=[]errors.append(e)try:data=vars(obj)exceptExceptionase:errors.append(e)raiseValueError(errors)fromereturnjsonable_encoder(data,include=include,exclude=exclude,by_alias=by_alias,exclude_unset=exclude_unset,exclude_defaults=exclude_defaults,exclude_none=exclude_none,custom_encoder=custom_encoder,sqlalchemy_safe=sqlalchemy_safe,) |
| --- | --- |

---

# Exceptions

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Exceptions -HTTPExceptionandWebSocketException¶

These are the exceptions that you can raise to show errors to the client.

When you raise an exception, as would happen with normal Python, the rest of the execution is aborted. This way you can raise these exceptions from anywhere in the code to abort a request and show the error to the client.

You can use:

- `HTTPException`
- `WebSocketException`

These exceptions can be imported directly from `fastapi`:

```
from fastapi import HTTPException, WebSocketException
```

## fastapi.HTTPException¶

```
HTTPException(status_code, detail=None, headers=None)
```

Bases: `HTTPException`

An HTTP exception you can raise in your own code to show errors to the client.

This is for client errors, invalid authentication, invalid data, etc. Not for server
errors in your code.

Read more about it in the
[FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).

#### Example¶

```
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| status_code | HTTP status code to send to the client.TYPE:int |
| detail | Any data to be sent to the client in thedetailkey of the JSON
response.TYPE:AnyDEFAULT:None |
| headers | Any headers to send to the client in the response.TYPE:Optional[dict[str,str]]DEFAULT:None |

  Source code in `fastapi/exceptions.py`

| 4546474849505152535455565758596061626364656667686970717273 | def__init__(self,status_code:Annotated[int,Doc("""HTTP status code to send to the client."""),],detail:Annotated[Any,Doc("""Any data to be sent to the client in the `detail` key of the JSONresponse."""),]=None,headers:Annotated[Optional[dict[str,str]],Doc("""Any headers to send to the client in the response."""),]=None,)->None:super().__init__(status_code=status_code,detail=detail,headers=headers) |
| --- | --- |

### status_codeinstance-attribute¶

```
status_code = status_code
```

### detailinstance-attribute¶

```
detail = detail
```

### headersinstance-attribute¶

```
headers = headers
```

## fastapi.WebSocketException¶

```
WebSocketException(code, reason=None)
```

Bases: `WebSocketException`

A WebSocket exception you can raise in your own code to show errors to the client.

This is for client errors, invalid authentication, invalid data, etc. Not for server
errors in your code.

Read more about it in the
[FastAPI docs for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).

#### Example¶

```
from typing import Annotated

from fastapi import (
    Cookie,
    FastAPI,
    WebSocket,
    WebSocketException,
    status,
)

app = FastAPI()

@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    item_id: str,
):
    if session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Session cookie is: {session}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| code | A closing code from thevalid codes defined in the specification.TYPE:int |
| reason | The reason to close the WebSocket connection.It is UTF-8-encoded data. The interpretation of the reason is up to the
application, it is not specified by the WebSocket specification.It could contain text that could be human-readable or interpretable
by the client code, etc.TYPE:Union[str, None]DEFAULT:None |

  Source code in `fastapi/exceptions.py`

| 118119120121122123124125126127128129130131132133134135136137138139140141142143144 | def__init__(self,code:Annotated[int,Doc("""A closing code from the[valid codes defined in the specification](https://datatracker.ietf.org/doc/html/rfc6455#section-7.4.1)."""),],reason:Annotated[Union[str,None],Doc("""The reason to close the WebSocket connection.It is UTF-8-encoded data. The interpretation of the reason is up to theapplication, it is not specified by the WebSocket specification.It could contain text that could be human-readable or interpretableby the client code, etc."""),]=None,)->None:super().__init__(code=code,reason=reason) |
| --- | --- |

### codeinstance-attribute¶

```
code = code
```

### reasoninstance-attribute¶

```
reason = reason or ''
```
