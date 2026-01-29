# Requestclass¶ and more

# Requestclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Requestclass¶

You can declare a parameter in a *path operation function* or dependency to be of type `Request` and then you can access the raw request object directly, without any validation, etc.

You can import it directly from `fastapi`:

```
from fastapi import Request
```

Tip

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

## fastapi.Request¶

```
Request(scope, receive=empty_receive, send=empty_send)
```

Bases: `HTTPConnection`

  Source code in `starlette/requests.py`

| 203204205206207208209210 | def__init__(self,scope:Scope,receive:Receive=empty_receive,send:Send=empty_send):super().__init__(scope)assertscope["type"]=="http"self._receive=receiveself._send=sendself._stream_consumed=Falseself._is_disconnected=Falseself._form=None |
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

### methodproperty¶

```
method
```

### receiveproperty¶

```
receive
```

### url_for¶

```
url_for(name, /, **path_params)
```

   Source code in `starlette/requests.py`

| 184185186187188189 | defurl_for(self,name:str,/,**path_params:Any)->URL:url_path_provider:Router|Starlette|None=self.scope.get("router")orself.scope.get("app")ifurl_path_providerisNone:raiseRuntimeError("The `url_for` method can only be used inside a Starlette application or with a router.")url_path=url_path_provider.url_path_for(name,**path_params)returnurl_path.make_absolute_url(base_url=self.base_url) |
| --- | --- |

### streamasync¶

```
stream()
```

   Source code in `starlette/requests.py`

| 220221222223224225226227228229230231232233234235236237238 | asyncdefstream(self)->AsyncGenerator[bytes,None]:ifhasattr(self,"_body"):yieldself._bodyyieldb""returnifself._stream_consumed:raiseRuntimeError("Stream consumed")whilenotself._stream_consumed:message=awaitself._receive()ifmessage["type"]=="http.request":body=message.get("body",b"")ifnotmessage.get("more_body",False):self._stream_consumed=Trueifbody:yieldbodyelifmessage["type"]=="http.disconnect":# pragma: no branchself._is_disconnected=TrueraiseClientDisconnect()yieldb"" |
| --- | --- |

### bodyasync¶

```
body()
```

   Source code in `starlette/requests.py`

| 240241242243244245246 | asyncdefbody(self)->bytes:ifnothasattr(self,"_body"):chunks:list[bytes]=[]asyncforchunkinself.stream():chunks.append(chunk)self._body=b"".join(chunks)returnself._body |
| --- | --- |

### jsonasync¶

```
json()
```

   Source code in `starlette/requests.py`

| 248249250251252 | asyncdefjson(self)->Any:ifnothasattr(self,"_json"):# pragma: no branchbody=awaitself.body()self._json=json.loads(body)returnself._json |
| --- | --- |

### form¶

```
form(
    *,
    max_files=1000,
    max_fields=1000,
    max_part_size=1024 * 1024
)
```

   Source code in `starlette/requests.py`

| 289290291292293294295296297298 | defform(self,*,max_files:int|float=1000,max_fields:int|float=1000,max_part_size:int=1024*1024,)->AwaitableOrContextManager[FormData]:returnAwaitableOrContextManagerWrapper(self._get_form(max_files=max_files,max_fields=max_fields,max_part_size=max_part_size)) |
| --- | --- |

### closeasync¶

```
close()
```

   Source code in `starlette/requests.py`

| 300301302 | asyncdefclose(self)->None:ifself._formisnotNone:# pragma: no branchawaitself._form.close() |
| --- | --- |

### is_disconnectedasync¶

```
is_disconnected()
```

   Source code in `starlette/requests.py`

| 304305306307308309310311312313314315316 | asyncdefis_disconnected(self)->bool:ifnotself._is_disconnected:message:Message={}# If message isn't immediately available, move onwithanyio.CancelScope()ascs:cs.cancel()message=awaitself._receive()ifmessage.get("type")=="http.disconnect":self._is_disconnected=Truereturnself._is_disconnected |
| --- | --- |

### send_push_promiseasync¶

```
send_push_promise(path)
```

   Source code in `starlette/requests.py`

| 318319320321322323324 | asyncdefsend_push_promise(self,path:str)->None:if"http.response.push"inself.scope.get("extensions",{}):raw_headers:list[tuple[bytes,bytes]]=[]fornameinSERVER_PUSH_HEADERS_TO_COPY:forvalueinself.headers.getlist(name):raw_headers.append((name.encode("latin-1"),value.encode("latin-1")))awaitself._send({"type":"http.response.push","path":path,"headers":raw_headers}) |
| --- | --- |

---

# Responseclass¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Responseclass¶

You can declare a parameter in a *path operation function* or dependency to be of type `Response` and then you can set data for the response like headers or cookies.

You can also use it directly to create an instance of it and return it from your *path operations*.

You can import it directly from `fastapi`:

```
from fastapi import Response
```

## fastapi.Response¶

```
Response(
    content=None,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

   Source code in `starlette/responses.py`

| 3435363738394041424344454647 | def__init__(self,content:Any=None,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:self.status_code=status_codeifmedia_typeisnotNone:self.media_type=media_typeself.background=backgroundself.body=self.render(content)self.init_headers(headers) |
| --- | --- |

### media_typeclass-attributeinstance-attribute¶

```
media_type = None
```

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### backgroundinstance-attribute¶

```
background = background
```

### bodyinstance-attribute¶

```
body = render(content)
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

---

# Custom Response Classes

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Custom Response Classes - File, HTML, Redirect, Streaming, etc.¶

There are several custom response classes you can use to create an instance and return them directly from your *path operations*.

Read more about it in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).

You can import them directly from `fastapi.responses`:

```
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
```

## FastAPI Responses¶

There are a couple of custom FastAPI response classes, you can use them to optimize JSON performance.

## fastapi.responses.UJSONResponse¶

```
UJSONResponse(
    content,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `JSONResponse`

JSON response using the high-performance ujson library to serialize data to JSON.

Read more about it in the
[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).

  Source code in `starlette/responses.py`

| 181182183184185186187188189 | def__init__(self,content:Any,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:super().__init__(content,status_code,headers,media_type,background) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = 'application/json'
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `fastapi/responses.py`

| 313233 | defrender(self,content:Any)->bytes:assertujsonisnotNone,"ujson must be installed to use UJSONResponse"returnujson.dumps(content,ensure_ascii=False).encode("utf-8") |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.ORJSONResponse¶

```
ORJSONResponse(
    content,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `JSONResponse`

JSON response using the high-performance orjson library to serialize data to JSON.

Read more about it in the
[FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).

  Source code in `starlette/responses.py`

| 181182183184185186187188189 | def__init__(self,content:Any,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:super().__init__(content,status_code,headers,media_type,background) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = 'application/json'
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `fastapi/responses.py`

| 4445464748 | defrender(self,content:Any)->bytes:assertorjsonisnotNone,"orjson must be installed to use ORJSONResponse"returnorjson.dumps(content,option=orjson.OPT_NON_STR_KEYS|orjson.OPT_SERIALIZE_NUMPY) |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## Starlette Responses¶

## fastapi.responses.FileResponse¶

```
FileResponse(
    path,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
    filename=None,
    stat_result=None,
    method=None,
    content_disposition_type="attachment",
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 296297298299300301302303304305306307308309310311312313314315316317318319320321322323324325326327328329330331 | def__init__(self,path:str|os.PathLike[str],status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,filename:str|None=None,stat_result:os.stat_result|None=None,method:str|None=None,content_disposition_type:str="attachment",)->None:self.path=pathself.status_code=status_codeself.filename=filenameifmethodisnotNone:warnings.warn("The 'method' parameter is not used, and it will be removed.",DeprecationWarning,)ifmedia_typeisNone:media_type=guess_type(filenameorpath)[0]or"text/plain"self.media_type=media_typeself.background=backgroundself.init_headers(headers)self.headers.setdefault("accept-ranges","bytes")ifself.filenameisnotNone:content_disposition_filename=quote(self.filename)ifcontent_disposition_filename!=self.filename:content_disposition=f"{content_disposition_type}; filename*=utf-8''{content_disposition_filename}"else:content_disposition=f'{content_disposition_type}; filename="{self.filename}"'self.headers.setdefault("content-disposition",content_disposition)self.stat_result=stat_resultifstat_resultisnotNone:self.set_stat_headers(stat_result) |
| --- | --- |

### chunk_sizeclass-attributeinstance-attribute¶

```
chunk_size = 64 * 1024
```

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeinstance-attribute¶

```
media_type = media_type
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.HTMLResponse¶

```
HTMLResponse(
    content=None,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 3435363738394041424344454647 | def__init__(self,content:Any=None,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:self.status_code=status_codeifmedia_typeisnotNone:self.media_type=media_typeself.background=backgroundself.body=self.render(content)self.init_headers(headers) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = 'text/html'
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.JSONResponse¶

```
JSONResponse(
    content,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 181182183184185186187188189 | def__init__(self,content:Any,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:super().__init__(content,status_code,headers,media_type,background) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = 'application/json'
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 191192193194195196197198 | defrender(self,content:Any)->bytes:returnjson.dumps(content,ensure_ascii=False,allow_nan=False,indent=None,separators=(",",":"),).encode("utf-8") |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.PlainTextResponse¶

```
PlainTextResponse(
    content=None,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 3435363738394041424344454647 | def__init__(self,content:Any=None,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:self.status_code=status_codeifmedia_typeisnotNone:self.media_type=media_typeself.background=backgroundself.body=self.render(content)self.init_headers(headers) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = 'text/plain'
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.RedirectResponse¶

```
RedirectResponse(
    url, status_code=307, headers=None, background=None
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 202203204205206207208209210 | def__init__(self,url:str|URL,status_code:int=307,headers:Mapping[str,str]|None=None,background:BackgroundTask|None=None,)->None:super().__init__(content=b"",status_code=status_code,headers=headers,background=background)self.headers["location"]=quote(str(url),safe=":/%#?=@[]!$&'()*+,;") |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = None
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.Response¶

```
Response(
    content=None,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

   Source code in `starlette/responses.py`

| 3435363738394041424344454647 | def__init__(self,content:Any=None,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:self.status_code=status_codeifmedia_typeisnotNone:self.media_type=media_typeself.background=backgroundself.body=self.render(content)self.init_headers(headers) |
| --- | --- |

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeclass-attributeinstance-attribute¶

```
media_type = None
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |

## fastapi.responses.StreamingResponse¶

```
StreamingResponse(
    content,
    status_code=200,
    headers=None,
    media_type=None,
    background=None,
)
```

Bases: `Response`

  Source code in `starlette/responses.py`

| 222223224225226227228229230231232233234235236237 | def__init__(self,content:ContentStream,status_code:int=200,headers:Mapping[str,str]|None=None,media_type:str|None=None,background:BackgroundTask|None=None,)->None:ifisinstance(content,AsyncIterable):self.body_iterator=contentelse:self.body_iterator=iterate_in_threadpool(content)self.status_code=status_codeself.media_type=self.media_typeifmedia_typeisNoneelsemedia_typeself.background=backgroundself.init_headers(headers) |
| --- | --- |

### body_iteratorinstance-attribute¶

```
body_iterator
```

### charsetclass-attributeinstance-attribute¶

```
charset = 'utf-8'
```

### status_codeinstance-attribute¶

```
status_code = status_code
```

### media_typeinstance-attribute¶

```
media_type = (
    media_type if media_type is None else media_type
)
```

### bodyinstance-attribute¶

```
body = render(content)
```

### backgroundinstance-attribute¶

```
background = background
```

### headersproperty¶

```
headers
```

### render¶

```
render(content)
```

   Source code in `starlette/responses.py`

| 495051525354 | defrender(self,content:Any)->bytes|memoryview:ifcontentisNone:returnb""ifisinstance(content,bytes|memoryview):returncontentreturncontent.encode(self.charset)# type: ignore |
| --- | --- |

### init_headers¶

```
init_headers(headers=None)
```

   Source code in `starlette/responses.py`

| 565758596061626364656667686970717273747576777879808182 | definit_headers(self,headers:Mapping[str,str]|None=None)->None:ifheadersisNone:raw_headers:list[tuple[bytes,bytes]]=[]populate_content_length=Truepopulate_content_type=Trueelse:raw_headers=[(k.lower().encode("latin-1"),v.encode("latin-1"))fork,vinheaders.items()]keys=[h[0]forhinraw_headers]populate_content_length=b"content-length"notinkeyspopulate_content_type=b"content-type"notinkeysbody=getattr(self,"body",None)if(bodyisnotNoneandpopulate_content_lengthandnot(self.status_code<200orself.status_codein(204,304))):content_length=str(len(body))raw_headers.append((b"content-length",content_length.encode("latin-1")))content_type=self.media_typeifcontent_typeisnotNoneandpopulate_content_type:ifcontent_type.startswith("text/")and"charset="notincontent_type.lower():content_type+="; charset="+self.charsetraw_headers.append((b"content-type",content_type.encode("latin-1")))self.raw_headers=raw_headers |
| --- | --- |

### set_cookie¶

```
set_cookie(
    key,
    value="",
    max_age=None,
    expires=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
    partitioned=False,
)
```

   Source code in `starlette/responses.py`

| 90919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133 | defset_cookie(self,key:str,value:str="",max_age:int|None=None,expires:datetime|str|int|None=None,path:str|None="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",partitioned:bool=False,)->None:cookie:http.cookies.BaseCookie[str]=http.cookies.SimpleCookie()cookie[key]=valueifmax_ageisnotNone:cookie[key]["max-age"]=max_ageifexpiresisnotNone:ifisinstance(expires,datetime):cookie[key]["expires"]=format_datetime(expires,usegmt=True)else:cookie[key]["expires"]=expiresifpathisnotNone:cookie[key]["path"]=pathifdomainisnotNone:cookie[key]["domain"]=domainifsecure:cookie[key]["secure"]=Trueifhttponly:cookie[key]["httponly"]=TrueifsamesiteisnotNone:assertsamesite.lower()in["strict","lax","none",],"samesite must be either 'strict', 'lax' or 'none'"cookie[key]["samesite"]=samesiteifpartitioned:ifsys.version_info<(3,14):raiseValueError("Partitioned cookies are only supported in Python 3.14 and above.")# pragma: no covercookie[key]["partitioned"]=True# pragma: no covercookie_val=cookie.output(header="").strip()self.raw_headers.append((b"set-cookie",cookie_val.encode("latin-1"))) |
| --- | --- |

### delete_cookie¶

```
delete_cookie(
    key,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    samesite="lax",
)
```

   Source code in `starlette/responses.py`

| 135136137138139140141142143144145146147148149150151152153 | defdelete_cookie(self,key:str,path:str="/",domain:str|None=None,secure:bool=False,httponly:bool=False,samesite:Literal["lax","strict","none"]|None="lax",)->None:self.set_cookie(key,max_age=0,expires=0,path=path,domain=domain,secure=secure,httponly=httponly,samesite=samesite,) |
| --- | --- |
