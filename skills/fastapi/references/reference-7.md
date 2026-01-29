# Security Tools¶

# Security Tools¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Security Tools¶

When you need to declare dependencies with OAuth2 scopes you use `Security()`.

But you still need to define what is the dependable, the callable that you pass as a parameter to `Depends()` or `Security()`.

There are multiple tools that you can use to create those dependables, and they get integrated into OpenAPI so they are shown in the automatic docs UI, they can be used by automatically generated clients and SDKs, etc.

You can import them from `fastapi.security`:

```
from fastapi.security import (
    APIKeyCookie,
    APIKeyHeader,
    APIKeyQuery,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPDigest,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordRequestFormStrict,
    OpenIdConnect,
    SecurityScopes,
)
```

## API Key Security Schemes¶

## fastapi.security.APIKeyCookie¶

```
APIKeyCookie(
    *,
    name,
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `APIKeyBase`

API key authentication using a cookie.

This defines the name of the cookie that should be provided in the request with
the API key and integrates that into the OpenAPI documentation. It extracts
the key value sent in the cookie automatically and provides it as the dependency
result. But it doesn't define how to set that cookie.

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be a string containing the key value.

#### Example¶

```
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyCookie

app = FastAPI()

cookie_scheme = APIKeyCookie(name="session")

@app.get("/items/")
async def read_items(session: str = Depends(cookie_scheme)):
    return {"session": session}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| name | Cookie name.TYPE:str |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the cookie is not provided,APIKeyCookiewill
automatically cancel the request and send the client an error.Ifauto_erroris set toFalse, when the cookie is not available,
instead of erroring out, the dependency result will beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in a cookie or
in an HTTP Bearer token).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/api_key.py`

| 265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303304305306307308309310311312313314 | def__init__(self,*,name:Annotated[str,Doc("Cookie name.")],scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the cookie is not provided, `APIKeyCookie` willautomatically cancel the request and send the client an error.If `auto_error` is set to `False`, when the cookie is not available,instead of erroring out, the dependency result will be `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in a cookie orin an HTTP Bearer token)."""),]=True,):super().__init__(location=APIKeyIn.cookie,name=name,scheme_name=scheme_name,description=description,auto_error=auto_error,) |
| --- | --- |

### modelinstance-attribute¶

```
model = APIKey(
    **{"in": location}, name=name, description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The WWW-Authenticate header is not standardized for API Key authentication but
the HTTP specification requires that an error of 401 "Unauthorized" must
include a WWW-Authenticate header.

Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized

For this, this method sends a custom challenge `APIKey`.

  Source code in `fastapi/security/api_key.py`

| 293031323334353637383940414243 | defmake_not_authenticated_error(self)->HTTPException:"""The WWW-Authenticate header is not standardized for API Key authentication butthe HTTP specification requires that an error of 401 "Unauthorized" mustinclude a WWW-Authenticate header.Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorizedFor this, this method sends a custom challenge `APIKey`."""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"APIKey"},) |
| --- | --- |

### check_api_key¶

```
check_api_key(api_key)
```

   Source code in `fastapi/security/api_key.py`

| 454647484950 | defcheck_api_key(self,api_key:Optional[str])->Optional[str]:ifnotapi_key:ifself.auto_error:raiseself.make_not_authenticated_error()returnNonereturnapi_key |
| --- | --- |

## fastapi.security.APIKeyHeader¶

```
APIKeyHeader(
    *,
    name,
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `APIKeyBase`

API key authentication using a header.

This defines the name of the header that should be provided in the request with
the API key and integrates that into the OpenAPI documentation. It extracts
the key value sent in the header automatically and provides it as the dependency
result. But it doesn't define how to send that key to the client.

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be a string containing the key value.

#### Example¶

```
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader

app = FastAPI()

header_scheme = APIKeyHeader(name="x-key")

@app.get("/items/")
async def read_items(key: str = Depends(header_scheme)):
    return {"key": key}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| name | Header name.TYPE:str |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the header is not provided,APIKeyHeaderwill
automatically cancel the request and send the client an error.Ifauto_erroris set toFalse, when the header is not available,
instead of erroring out, the dependency result will beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in a header or
in an HTTP Bearer token).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/api_key.py`

| 177178179180181182183184185186187188189190191192193194195196197198199200201202203204205206207208209210211212213214215216217218219220221222223224225226 | def__init__(self,*,name:Annotated[str,Doc("Header name.")],scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the header is not provided, `APIKeyHeader` willautomatically cancel the request and send the client an error.If `auto_error` is set to `False`, when the header is not available,instead of erroring out, the dependency result will be `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in a header orin an HTTP Bearer token)."""),]=True,):super().__init__(location=APIKeyIn.header,name=name,scheme_name=scheme_name,description=description,auto_error=auto_error,) |
| --- | --- |

### modelinstance-attribute¶

```
model = APIKey(
    **{"in": location}, name=name, description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The WWW-Authenticate header is not standardized for API Key authentication but
the HTTP specification requires that an error of 401 "Unauthorized" must
include a WWW-Authenticate header.

Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized

For this, this method sends a custom challenge `APIKey`.

  Source code in `fastapi/security/api_key.py`

| 293031323334353637383940414243 | defmake_not_authenticated_error(self)->HTTPException:"""The WWW-Authenticate header is not standardized for API Key authentication butthe HTTP specification requires that an error of 401 "Unauthorized" mustinclude a WWW-Authenticate header.Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorizedFor this, this method sends a custom challenge `APIKey`."""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"APIKey"},) |
| --- | --- |

### check_api_key¶

```
check_api_key(api_key)
```

   Source code in `fastapi/security/api_key.py`

| 454647484950 | defcheck_api_key(self,api_key:Optional[str])->Optional[str]:ifnotapi_key:ifself.auto_error:raiseself.make_not_authenticated_error()returnNonereturnapi_key |
| --- | --- |

## fastapi.security.APIKeyQuery¶

```
APIKeyQuery(
    *,
    name,
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `APIKeyBase`

API key authentication using a query parameter.

This defines the name of the query parameter that should be provided in the request
with the API key and integrates that into the OpenAPI documentation. It extracts
the key value sent in the query parameter automatically and provides it as the
dependency result. But it doesn't define how to send that API key to the client.

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be a string containing the key value.

#### Example¶

```
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyQuery

app = FastAPI()

query_scheme = APIKeyQuery(name="api_key")

@app.get("/items/")
async def read_items(api_key: str = Depends(query_scheme)):
    return {"api_key": api_key}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| name | Query parameter name.TYPE:str |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the query parameter is not provided,APIKeyQuerywill
automatically cancel the request and send the client an error.Ifauto_erroris set toFalse, when the query parameter is not
available, instead of erroring out, the dependency result will beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in a query
parameter or in an HTTP Bearer token).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/api_key.py`

| 858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138 | def__init__(self,*,name:Annotated[str,Doc("Query parameter name."),],scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the query parameter is not provided, `APIKeyQuery` willautomatically cancel the request and send the client an error.If `auto_error` is set to `False`, when the query parameter is notavailable, instead of erroring out, the dependency result will be`None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in a queryparameter or in an HTTP Bearer token)."""),]=True,):super().__init__(location=APIKeyIn.query,name=name,scheme_name=scheme_name,description=description,auto_error=auto_error,) |
| --- | --- |

### modelinstance-attribute¶

```
model = APIKey(
    **{"in": location}, name=name, description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The WWW-Authenticate header is not standardized for API Key authentication but
the HTTP specification requires that an error of 401 "Unauthorized" must
include a WWW-Authenticate header.

Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized

For this, this method sends a custom challenge `APIKey`.

  Source code in `fastapi/security/api_key.py`

| 293031323334353637383940414243 | defmake_not_authenticated_error(self)->HTTPException:"""The WWW-Authenticate header is not standardized for API Key authentication butthe HTTP specification requires that an error of 401 "Unauthorized" mustinclude a WWW-Authenticate header.Ref: https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorizedFor this, this method sends a custom challenge `APIKey`."""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"APIKey"},) |
| --- | --- |

### check_api_key¶

```
check_api_key(api_key)
```

   Source code in `fastapi/security/api_key.py`

| 454647484950 | defcheck_api_key(self,api_key:Optional[str])->Optional[str]:ifnotapi_key:ifself.auto_error:raiseself.make_not_authenticated_error()returnNonereturnapi_key |
| --- | --- |

## HTTP Authentication Schemes¶

## fastapi.security.HTTPBasic¶

```
HTTPBasic(
    *,
    scheme_name=None,
    realm=None,
    description=None,
    auto_error=True
)
```

Bases: `HTTPBase`

HTTP Basic authentication.

Ref: https://datatracker.ietf.org/doc/html/rfc7617

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be an `HTTPBasicCredentials` object containing the
`username` and the `password`.

Read more about it in the
[FastAPI docs for HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/).

#### Example¶

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| realm | HTTP Basic authentication realm.TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the HTTP Basic authentication is not provided (a
header),HTTPBasicwill automatically cancel the request and send the
client an error.Ifauto_erroris set toFalse, when the HTTP Basic authentication
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in HTTP Basic
authentication or in an HTTP Bearer token).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/http.py`

| 142143144145146147148149150151152153154155156157158159160161162163164165166167168169170171172173174175176177178179180181182183184185186187188189190191192193194195196197 | def__init__(self,*,scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,realm:Annotated[Optional[str],Doc("""HTTP Basic authentication realm."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the HTTP Basic authentication is not provided (aheader), `HTTPBasic` will automatically cancel the request and send theclient an error.If `auto_error` is set to `False`, when the HTTP Basic authenticationis not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in HTTP Basicauthentication or in an HTTP Bearer token)."""),]=True,):self.model=HTTPBaseModel(scheme="basic",description=description)self.scheme_name=scheme_nameorself.__class__.__name__self.realm=realmself.auto_error=auto_error |
| --- | --- |

### modelinstance-attribute¶

```
model = HTTPBase(scheme='basic', description=description)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### realminstance-attribute¶

```
realm = realm
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

   Source code in `fastapi/security/http.py`

| 878889909192 | defmake_not_authenticated_error(self)->HTTPException:returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers=self.make_authenticate_headers(),) |
| --- | --- |

### make_authenticate_headers¶

```
make_authenticate_headers()
```

   Source code in `fastapi/security/http.py`

| 199200201202 | defmake_authenticate_headers(self)->dict[str,str]:ifself.realm:return{"WWW-Authenticate":f'Basic realm="{self.realm}"'}return{"WWW-Authenticate":"Basic"} |
| --- | --- |

## fastapi.security.HTTPBearer¶

```
HTTPBearer(
    *,
    bearerFormat=None,
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `HTTPBase`

HTTP Bearer token authentication.

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be an `HTTPAuthorizationCredentials` object containing
the `scheme` and the `credentials`.

#### Example¶

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()

security = HTTPBearer()

@app.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| bearerFormat | Bearer token format.TYPE:Optional[str]DEFAULT:None |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the HTTP Bearer token is not provided (in anAuthorizationheader),HTTPBearerwill automatically cancel the
request and send the client an error.Ifauto_erroris set toFalse, when the HTTP Bearer token
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in an HTTP
Bearer token or in a cookie).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/http.py`

| 256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303 | def__init__(self,*,bearerFormat:Annotated[Optional[str],Doc("Bearer token format.")]=None,scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the HTTP Bearer token is not provided (in an`Authorization` header), `HTTPBearer` will automatically cancel therequest and send the client an error.If `auto_error` is set to `False`, when the HTTP Bearer tokenis not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in an HTTPBearer token or in a cookie)."""),]=True,):self.model=HTTPBearerModel(bearerFormat=bearerFormat,description=description)self.scheme_name=scheme_nameorself.__class__.__name__self.auto_error=auto_error |
| --- | --- |

### modelinstance-attribute¶

```
model = HTTPBearer(
    bearerFormat=bearerFormat, description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_authenticate_headers¶

```
make_authenticate_headers()
```

   Source code in `fastapi/security/http.py`

| 8485 | defmake_authenticate_headers(self)->dict[str,str]:return{"WWW-Authenticate":f"{self.model.scheme.title()}"} |
| --- | --- |

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

   Source code in `fastapi/security/http.py`

| 878889909192 | defmake_not_authenticated_error(self)->HTTPException:returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers=self.make_authenticate_headers(),) |
| --- | --- |

## fastapi.security.HTTPDigest¶

```
HTTPDigest(
    *, scheme_name=None, description=None, auto_error=True
)
```

Bases: `HTTPBase`

HTTP Digest authentication.

**Warning**: this is only a stub to connect the components with OpenAPI in FastAPI,
but it doesn't implement the full Digest scheme, you would need to to subclass it
and implement it in your code.

Ref: https://datatracker.ietf.org/doc/html/rfc7616

#### Usage¶

Create an instance object and use that object as the dependency in `Depends()`.

The dependency result will be an `HTTPAuthorizationCredentials` object containing
the `scheme` and the `credentials`.

#### Example¶

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest

app = FastAPI()

security = HTTPDigest()

@app.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}
```

| PARAMETER | DESCRIPTION |
| --- | --- |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if the HTTP Digest is not provided,HTTPDigestwill
automatically cancel the request and send the client an error.Ifauto_erroris set toFalse, when the HTTP Digest is not
available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, in HTTP
Digest or in a cookie).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/http.py`

| 361362363364365366367368369370371372373374375376377378379380381382383384385386387388389390391392393394395396397398399400401402403404405406 | def__init__(self,*,scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if the HTTP Digest is not provided, `HTTPDigest` willautomatically cancel the request and send the client an error.If `auto_error` is set to `False`, when the HTTP Digest is notavailable, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, in HTTPDigest or in a cookie)."""),]=True,):self.model=HTTPBaseModel(scheme="digest",description=description)self.scheme_name=scheme_nameorself.__class__.__name__self.auto_error=auto_error |
| --- | --- |

### modelinstance-attribute¶

```
model = HTTPBase(scheme='digest', description=description)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_authenticate_headers¶

```
make_authenticate_headers()
```

   Source code in `fastapi/security/http.py`

| 8485 | defmake_authenticate_headers(self)->dict[str,str]:return{"WWW-Authenticate":f"{self.model.scheme.title()}"} |
| --- | --- |

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

   Source code in `fastapi/security/http.py`

| 878889909192 | defmake_not_authenticated_error(self)->HTTPException:returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers=self.make_authenticate_headers(),) |
| --- | --- |

## HTTP Credentials¶

## fastapi.security.HTTPAuthorizationCredentials¶

Bases: `BaseModel`

The HTTP authorization credentials in the result of using `HTTPBearer` or
`HTTPDigest` in a dependency.

The HTTP authorization header value is split by the first space.

The first part is the `scheme`, the second part is the `credentials`.

For example, in an HTTP Bearer token scheme, the client will send a header
like:

```
Authorization: Bearer deadbeef12346
```

In this case:

- `scheme` will have the value `"Bearer"`
- `credentials` will have the value `"deadbeef12346"`

### schemeinstance-attribute¶

```
scheme
```

The HTTP authorization scheme extracted from the header value.

### credentialsinstance-attribute¶

```
credentials
```

The HTTP authorization credentials extracted from the header value.

## fastapi.security.HTTPBasicCredentials¶

Bases: `BaseModel`

The HTTP Basic credentials given as the result of using `HTTPBasic` in a
dependency.

Read more about it in the
[FastAPI docs for HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/).

### usernameinstance-attribute¶

```
username
```

The HTTP Basic username.

### passwordinstance-attribute¶

```
password
```

The HTTP Basic password.

## OAuth2 Authentication¶

## fastapi.security.OAuth2¶

```
OAuth2(
    *,
    flows=OAuthFlows(),
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `SecurityBase`

This is the base class for OAuth2 authentication, an instance of it would be used
as a dependency. All other OAuth2 classes inherit from it and customize it for
each OAuth2 flow.

You normally would not create a new class inheriting from it but use one of the
existing subclasses, and maybe compose them if you want to support multiple flows.

Read more about it in the
[FastAPI docs for Security](https://fastapi.tiangolo.com/tutorial/security/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| flows | The dictionary of OAuth2 flows.TYPE:Union[OAuthFlows,dict[str,dict[str,Any]]]DEFAULT:OAuthFlows() |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if no HTTP Authorization header is provided, required for
OAuth2 authentication, it will automatically cancel the request and
send the client an error.Ifauto_erroris set toFalse, when the HTTP Authorization header
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, with OAuth2
or in a cookie).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/oauth2.py`

| 319320321322323324325326327328329330331332333334335336337338339340341342343344345346347348349350351352353354355356357358359360361362363364365366367368369370371372373374375 | def__init__(self,*,flows:Annotated[Union[OAuthFlowsModel,dict[str,dict[str,Any]]],Doc("""The dictionary of OAuth2 flows."""),]=OAuthFlowsModel(),scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if no HTTP Authorization header is provided, required forOAuth2 authentication, it will automatically cancel the request andsend the client an error.If `auto_error` is set to `False`, when the HTTP Authorization headeris not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, with OAuth2or in a cookie)."""),]=True,):self.model=OAuth2Model(flows=cast(OAuthFlowsModel,flows),description=description)self.scheme_name=scheme_nameorself.__class__.__name__self.auto_error=auto_error |
| --- | --- |

### modelinstance-attribute¶

```
model = OAuth2(
    flows=cast(OAuthFlows, flows), description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The OAuth 2 specification doesn't define the challenge that should be used,
because a `Bearer` token is not really the only option to authenticate.

But declaring any other authentication challenge would be application-specific
as it's not defined in the specification.

For practical reasons, this method uses the `Bearer` challenge by default, as
it's probably the most common one.

If you are implementing an OAuth2 authentication scheme other than the provided
ones in FastAPI (based on bearer tokens), you might want to override this.

Ref: https://datatracker.ietf.org/doc/html/rfc6749

  Source code in `fastapi/security/oauth2.py`

| 377378379380381382383384385386387388389390391392393394395396397 | defmake_not_authenticated_error(self)->HTTPException:"""The OAuth 2 specification doesn't define the challenge that should be used,because a `Bearer` token is not really the only option to authenticate.But declaring any other authentication challenge would be application-specificas it's not defined in the specification.For practical reasons, this method uses the `Bearer` challenge by default, asit's probably the most common one.If you are implementing an OAuth2 authentication scheme other than the providedones in FastAPI (based on bearer tokens), you might want to override this.Ref: https://datatracker.ietf.org/doc/html/rfc6749"""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"Bearer"},) |
| --- | --- |

## fastapi.security.OAuth2AuthorizationCodeBearer¶

```
OAuth2AuthorizationCodeBearer(
    authorizationUrl,
    tokenUrl,
    refreshUrl=None,
    scheme_name=None,
    scopes=None,
    description=None,
    auto_error=True,
)
```

Bases: `OAuth2`

OAuth2 flow for authentication using a bearer token obtained with an OAuth2 code
flow. An instance of it would be used as a dependency.

| PARAMETER | DESCRIPTION |
| --- | --- |
| tokenUrl | The URL to obtain the OAuth2 token.TYPE:str |
| refreshUrl | The URL to refresh the token and obtain a new one.TYPE:Optional[str]DEFAULT:None |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| scopes | The OAuth2 scopes that would be required by thepath operationsthat
use this dependency.TYPE:Optional[dict[str,str]]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if no HTTP Authorization header is provided, required for
OAuth2 authentication, it will automatically cancel the request and
send the client an error.Ifauto_erroris set toFalse, when the HTTP Authorization header
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, with OAuth2
or in a cookie).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/oauth2.py`

| 523524525526527528529530531532533534535536537538539540541542543544545546547548549550551552553554555556557558559560561562563564565566567568569570571572573574575576577578579580581582583584585586587588589590591592593594595596597598599600601602603604605606607608609610 | def__init__(self,authorizationUrl:str,tokenUrl:Annotated[str,Doc("""The URL to obtain the OAuth2 token."""),],refreshUrl:Annotated[Optional[str],Doc("""The URL to refresh the token and obtain a new one."""),]=None,scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,scopes:Annotated[Optional[dict[str,str]],Doc("""The OAuth2 scopes that would be required by the *path operations* thatuse this dependency."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if no HTTP Authorization header is provided, required forOAuth2 authentication, it will automatically cancel the request andsend the client an error.If `auto_error` is set to `False`, when the HTTP Authorization headeris not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, with OAuth2or in a cookie)."""),]=True,):ifnotscopes:scopes={}flows=OAuthFlowsModel(authorizationCode=cast(Any,{"authorizationUrl":authorizationUrl,"tokenUrl":tokenUrl,"refreshUrl":refreshUrl,"scopes":scopes,},))super().__init__(flows=flows,scheme_name=scheme_name,description=description,auto_error=auto_error,) |
| --- | --- |

### modelinstance-attribute¶

```
model = OAuth2(
    flows=cast(OAuthFlows, flows), description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The OAuth 2 specification doesn't define the challenge that should be used,
because a `Bearer` token is not really the only option to authenticate.

But declaring any other authentication challenge would be application-specific
as it's not defined in the specification.

For practical reasons, this method uses the `Bearer` challenge by default, as
it's probably the most common one.

If you are implementing an OAuth2 authentication scheme other than the provided
ones in FastAPI (based on bearer tokens), you might want to override this.

Ref: https://datatracker.ietf.org/doc/html/rfc6749

  Source code in `fastapi/security/oauth2.py`

| 377378379380381382383384385386387388389390391392393394395396397 | defmake_not_authenticated_error(self)->HTTPException:"""The OAuth 2 specification doesn't define the challenge that should be used,because a `Bearer` token is not really the only option to authenticate.But declaring any other authentication challenge would be application-specificas it's not defined in the specification.For practical reasons, this method uses the `Bearer` challenge by default, asit's probably the most common one.If you are implementing an OAuth2 authentication scheme other than the providedones in FastAPI (based on bearer tokens), you might want to override this.Ref: https://datatracker.ietf.org/doc/html/rfc6749"""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"Bearer"},) |
| --- | --- |

## fastapi.security.OAuth2PasswordBearer¶

```
OAuth2PasswordBearer(
    tokenUrl,
    scheme_name=None,
    scopes=None,
    description=None,
    auto_error=True,
    refreshUrl=None,
)
```

Bases: `OAuth2`

OAuth2 flow for authentication using a bearer token obtained with a password.
An instance of it would be used as a dependency.

Read more about it in the
[FastAPI docs for Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| tokenUrl | The URL to obtain the OAuth2 token. This would be thepath operationthat hasOAuth2PasswordRequestFormas a dependency.TYPE:str |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| scopes | The OAuth2 scopes that would be required by thepath operationsthat
use this dependency.TYPE:Optional[dict[str,str]]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if no HTTP Authorization header is provided, required for
OAuth2 authentication, it will automatically cancel the request and
send the client an error.Ifauto_erroris set toFalse, when the HTTP Authorization header
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, with OAuth2
or in a cookie).TYPE:boolDEFAULT:True |
| refreshUrl | The URL to refresh the token and obtain a new one.TYPE:Optional[str]DEFAULT:None |

  Source code in `fastapi/security/oauth2.py`

| 418419420421422423424425426427428429430431432433434435436437438439440441442443444445446447448449450451452453454455456457458459460461462463464465466467468469470471472473474475476477478479480481482483484485486487488489490491492493494495496497498499500501502503504 | def__init__(self,tokenUrl:Annotated[str,Doc("""The URL to obtain the OAuth2 token. This would be the *path operation*that has `OAuth2PasswordRequestForm` as a dependency."""),],scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,scopes:Annotated[Optional[dict[str,str]],Doc("""The OAuth2 scopes that would be required by the *path operations* thatuse this dependency."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if no HTTP Authorization header is provided, required forOAuth2 authentication, it will automatically cancel the request andsend the client an error.If `auto_error` is set to `False`, when the HTTP Authorization headeris not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, with OAuth2or in a cookie)."""),]=True,refreshUrl:Annotated[Optional[str],Doc("""The URL to refresh the token and obtain a new one."""),]=None,):ifnotscopes:scopes={}flows=OAuthFlowsModel(password=cast(Any,{"tokenUrl":tokenUrl,"refreshUrl":refreshUrl,"scopes":scopes,},))super().__init__(flows=flows,scheme_name=scheme_name,description=description,auto_error=auto_error,) |
| --- | --- |

### modelinstance-attribute¶

```
model = OAuth2(
    flows=cast(OAuthFlows, flows), description=description
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

The OAuth 2 specification doesn't define the challenge that should be used,
because a `Bearer` token is not really the only option to authenticate.

But declaring any other authentication challenge would be application-specific
as it's not defined in the specification.

For practical reasons, this method uses the `Bearer` challenge by default, as
it's probably the most common one.

If you are implementing an OAuth2 authentication scheme other than the provided
ones in FastAPI (based on bearer tokens), you might want to override this.

Ref: https://datatracker.ietf.org/doc/html/rfc6749

  Source code in `fastapi/security/oauth2.py`

| 377378379380381382383384385386387388389390391392393394395396397 | defmake_not_authenticated_error(self)->HTTPException:"""The OAuth 2 specification doesn't define the challenge that should be used,because a `Bearer` token is not really the only option to authenticate.But declaring any other authentication challenge would be application-specificas it's not defined in the specification.For practical reasons, this method uses the `Bearer` challenge by default, asit's probably the most common one.If you are implementing an OAuth2 authentication scheme other than the providedones in FastAPI (based on bearer tokens), you might want to override this.Ref: https://datatracker.ietf.org/doc/html/rfc6749"""returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"Bearer"},) |
| --- | --- |

## OAuth2 Password Form¶

## fastapi.security.OAuth2PasswordRequestForm¶

```
OAuth2PasswordRequestForm(
    *,
    grant_type=None,
    username,
    password,
    scope="",
    client_id=None,
    client_secret=None
)
```

This is a dependency class to collect the `username` and `password` as form data
for an OAuth2 password flow.

The OAuth2 specification dictates that for a password flow the data should be
collected using form data (instead of JSON) and that it should have the specific
fields `username` and `password`.

All the initialization parameters are extracted from the request.

Read more about it in the
[FastAPI docs for Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/).

#### Example¶

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    data = {}
    data["scopes"] = []
    for scope in form_data.scopes:
        data["scopes"].append(scope)
    if form_data.client_id:
        data["client_id"] = form_data.client_id
    if form_data.client_secret:
        data["client_secret"] = form_data.client_secret
    return data
```

Note that for OAuth2 the scope `items:read` is a single scope in an opaque string.
You could have custom internal logic to separate it by colon characters (`:`) or
similar, and get the two parts `items` and `read`. Many applications do that to
group and organize permissions, you could do it as well in your application, just
know that that it is application specific, it's not part of the specification.

| PARAMETER | DESCRIPTION |
| --- | --- |
| grant_type | The OAuth2 spec says it is required and MUST be the fixed string
"password". Nevertheless, this dependency class is permissive and
allows not passing it. If you want to enforce it, use instead theOAuth2PasswordRequestFormStrictdependency.TYPE:Union[str, None]DEFAULT:None |
| username | usernamestring. The OAuth2 spec requires the exact field nameusername.TYPE:str |
| password | passwordstring. The OAuth2 spec requires the exact field namepassword.TYPE:str |
| scope | A single string with actually several scopes separated by spaces. Each
scope is also a string.For example, a single string with:```python
"items:read items:write users:read profile openid"
````would represent the scopes:items:readitems:writeusers:readprofileopenidTYPE:strDEFAULT:'' |
| client_id | If there's aclient_id, it can be sent as part of the form fields.
But the OAuth2 specification recommends sending theclient_idandclient_secret(if any) using HTTP Basic auth.TYPE:Union[str, None]DEFAULT:None |
| client_secret | If there's aclient_password(and aclient_id), they can be sent
as part of the form fields. But the OAuth2 specification recommends
sending theclient_idandclient_secret(if any) using HTTP Basic
auth.TYPE:Union[str, None]DEFAULT:None |

  Source code in `fastapi/security/oauth2.py`

| 5960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133134135136137138139140141142143144145146147 | def__init__(self,*,grant_type:Annotated[Union[str,None],Form(pattern="^password$"),Doc("""The OAuth2 spec says it is required and MUST be the fixed string"password". Nevertheless, this dependency class is permissive andallows not passing it. If you want to enforce it, use instead the`OAuth2PasswordRequestFormStrict` dependency."""),]=None,username:Annotated[str,Form(),Doc("""`username` string. The OAuth2 spec requires the exact field name`username`."""),],password:Annotated[str,Form(json_schema_extra={"format":"password"}),Doc("""`password` string. The OAuth2 spec requires the exact field name`password`."""),],scope:Annotated[str,Form(),Doc("""A single string with actually several scopes separated by spaces. Eachscope is also a string.For example, a single string with:```python"items:read items:write users:read profile openid"````would represent the scopes:* `items:read`* `items:write`* `users:read`* `profile`* `openid`"""),]="",client_id:Annotated[Union[str,None],Form(),Doc("""If there's a `client_id`, it can be sent as part of the form fields.But the OAuth2 specification recommends sending the `client_id` and`client_secret` (if any) using HTTP Basic auth."""),]=None,client_secret:Annotated[Union[str,None],Form(json_schema_extra={"format":"password"}),Doc("""If there's a `client_password` (and a `client_id`), they can be sentas part of the form fields. But the OAuth2 specification recommendssending the `client_id` and `client_secret` (if any) using HTTP Basicauth."""),]=None,):self.grant_type=grant_typeself.username=usernameself.password=passwordself.scopes=scope.split()self.client_id=client_idself.client_secret=client_secret |
| --- | --- |

### grant_typeinstance-attribute¶

```
grant_type = grant_type
```

### usernameinstance-attribute¶

```
username = username
```

### passwordinstance-attribute¶

```
password = password
```

### scopesinstance-attribute¶

```
scopes = split()
```

### client_idinstance-attribute¶

```
client_id = client_id
```

### client_secretinstance-attribute¶

```
client_secret = client_secret
```

## fastapi.security.OAuth2PasswordRequestFormStrict¶

```
OAuth2PasswordRequestFormStrict(
    grant_type,
    username,
    password,
    scope="",
    client_id=None,
    client_secret=None,
)
```

Bases: `OAuth2PasswordRequestForm`

This is a dependency class to collect the `username` and `password` as form data
for an OAuth2 password flow.

The OAuth2 specification dictates that for a password flow the data should be
collected using form data (instead of JSON) and that it should have the specific
fields `username` and `password`.

All the initialization parameters are extracted from the request.

The only difference between `OAuth2PasswordRequestFormStrict` and
`OAuth2PasswordRequestForm` is that `OAuth2PasswordRequestFormStrict` requires the
client to send the form field `grant_type` with the value `"password"`, which
is required in the OAuth2 specification (it seems that for no particular reason),
while for `OAuth2PasswordRequestForm` `grant_type` is optional.

Read more about it in the
[FastAPI docs for Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/).

#### Example¶

```
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]):
    data = {}
    data["scopes"] = []
    for scope in form_data.scopes:
        data["scopes"].append(scope)
    if form_data.client_id:
        data["client_id"] = form_data.client_id
    if form_data.client_secret:
        data["client_secret"] = form_data.client_secret
    return data
```

Note that for OAuth2 the scope `items:read` is a single scope in an opaque string.
You could have custom internal logic to separate it by colon characters (`:`) or
similar, and get the two parts `items` and `read`. Many applications do that to
group and organize permissions, you could do it as well in your application, just
know that that it is application specific, it's not part of the specification.

  the OAuth2 spec says it is required and MUST be the fixed string "password".

This dependency is strict about it. If you want to be permissive, use instead the
OAuth2PasswordRequestForm dependency class.

username: username string. The OAuth2 spec requires the exact field name "username".
password: password string. The OAuth2 spec requires the exact field name "password".
scope: Optional string. Several scopes (each one a string) separated by spaces. E.g.
    "items:read items:write users:read profile openid"
client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
    using HTTP Basic auth, as: client_id:client_secret
client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
    using HTTP Basic auth, as: client_id:client_secret

| PARAMETER | DESCRIPTION |
| --- | --- |
| grant_type | The OAuth2 spec says it is required and MUST be the fixed string
"password". This dependency is strict about it. If you want to be
permissive, use instead theOAuth2PasswordRequestFormdependency
class.TYPE:str |
| username | usernamestring. The OAuth2 spec requires the exact field nameusername.TYPE:str |
| password | passwordstring. The OAuth2 spec requires the exact field namepassword.TYPE:str |
| scope | A single string with actually several scopes separated by spaces. Each
scope is also a string.For example, a single string with:```python
"items:read items:write users:read profile openid"
````would represent the scopes:items:readitems:writeusers:readprofileopenidTYPE:strDEFAULT:'' |
| client_id | If there's aclient_id, it can be sent as part of the form fields.
But the OAuth2 specification recommends sending theclient_idandclient_secret(if any) using HTTP Basic auth.TYPE:Union[str, None]DEFAULT:None |
| client_secret | If there's aclient_password(and aclient_id), they can be sent
as part of the form fields. But the OAuth2 specification recommends
sending theclient_idandclient_secret(if any) using HTTP Basic
auth.TYPE:Union[str, None]DEFAULT:None |

  Source code in `fastapi/security/oauth2.py`

| 214215216217218219220221222223224225226227228229230231232233234235236237238239240241242243244245246247248249250251252253254255256257258259260261262263264265266267268269270271272273274275276277278279280281282283284285286287288289290291292293294295296297298299300301302303 | def__init__(self,grant_type:Annotated[str,Form(pattern="^password$"),Doc("""The OAuth2 spec says it is required and MUST be the fixed string"password". This dependency is strict about it. If you want to bepermissive, use instead the `OAuth2PasswordRequestForm` dependencyclass."""),],username:Annotated[str,Form(),Doc("""`username` string. The OAuth2 spec requires the exact field name`username`."""),],password:Annotated[str,Form(),Doc("""`password` string. The OAuth2 spec requires the exact field name`password`."""),],scope:Annotated[str,Form(),Doc("""A single string with actually several scopes separated by spaces. Eachscope is also a string.For example, a single string with:```python"items:read items:write users:read profile openid"````would represent the scopes:* `items:read`* `items:write`* `users:read`* `profile`* `openid`"""),]="",client_id:Annotated[Union[str,None],Form(),Doc("""If there's a `client_id`, it can be sent as part of the form fields.But the OAuth2 specification recommends sending the `client_id` and`client_secret` (if any) using HTTP Basic auth."""),]=None,client_secret:Annotated[Union[str,None],Form(),Doc("""If there's a `client_password` (and a `client_id`), they can be sentas part of the form fields. But the OAuth2 specification recommendssending the `client_id` and `client_secret` (if any) using HTTP Basicauth."""),]=None,):super().__init__(grant_type=grant_type,username=username,password=password,scope=scope,client_id=client_id,client_secret=client_secret,) |
| --- | --- |

### grant_typeinstance-attribute¶

```
grant_type = grant_type
```

### usernameinstance-attribute¶

```
username = username
```

### passwordinstance-attribute¶

```
password = password
```

### scopesinstance-attribute¶

```
scopes = split()
```

### client_idinstance-attribute¶

```
client_id = client_id
```

### client_secretinstance-attribute¶

```
client_secret = client_secret
```

## OAuth2 Security Scopes in Dependencies¶

## fastapi.security.SecurityScopes¶

```
SecurityScopes(scopes=None)
```

This is a special class that you can define in a parameter in a dependency to
obtain the OAuth2 scopes required by all the dependencies in the same chain.

This way, multiple dependencies can have different scopes, even when used in the
same *path operation*. And with this, you can access all the scopes required in
all those dependencies in a single place.

Read more about it in the
[FastAPI docs for OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| scopes | This will be filled by FastAPI.TYPE:Optional[list[str]]DEFAULT:None |

  Source code in `fastapi/security/oauth2.py`

| 636637638639640641642643644645646647648649650651652653654655656657658659660661662663 | def__init__(self,scopes:Annotated[Optional[list[str]],Doc("""This will be filled by FastAPI."""),]=None,):self.scopes:Annotated[list[str],Doc("""The list of all the scopes required by dependencies."""),]=scopesor[]self.scope_str:Annotated[str,Doc("""All the scopes required by all the dependencies in a single stringseparated by spaces, as defined in the OAuth2 specification."""),]=" ".join(self.scopes) |
| --- | --- |

### scopesinstance-attribute¶

```
scopes = scopes or []
```

The list of all the scopes required by dependencies.

### scope_strinstance-attribute¶

```
scope_str = join(scopes)
```

All the scopes required by all the dependencies in a single string
separated by spaces, as defined in the OAuth2 specification.

## OpenID Connect¶

## fastapi.security.OpenIdConnect¶

```
OpenIdConnect(
    *,
    openIdConnectUrl,
    scheme_name=None,
    description=None,
    auto_error=True
)
```

Bases: `SecurityBase`

OpenID Connect authentication class. An instance of it would be used as a
dependency.

**Warning**: this is only a stub to connect the components with OpenAPI in FastAPI,
but it doesn't implement the full OpenIdConnect scheme, for example, it doesn't use
the OpenIDConnect URL. You would need to to subclass it and implement it in your
code.

| PARAMETER | DESCRIPTION |
| --- | --- |
| openIdConnectUrl | The OpenID Connect URL.TYPE:str |
| scheme_name | Security scheme name.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| description | Security scheme description.It will be included in the generated OpenAPI (e.g. visible at/docs).TYPE:Optional[str]DEFAULT:None |
| auto_error | By default, if no HTTP Authorization header is provided, required for
OpenID Connect authentication, it will automatically cancel the request
and send the client an error.Ifauto_erroris set toFalse, when the HTTP Authorization header
is not available, instead of erroring out, the dependency result will
beNone.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can be
provided in one of multiple optional ways (for example, with OpenID
Connect or in a cookie).TYPE:boolDEFAULT:True |

  Source code in `fastapi/security/open_id_connect_url.py`

| 222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778 | def__init__(self,*,openIdConnectUrl:Annotated[str,Doc("""The OpenID Connect URL."""),],scheme_name:Annotated[Optional[str],Doc("""Security scheme name.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,description:Annotated[Optional[str],Doc("""Security scheme description.It will be included in the generated OpenAPI (e.g. visible at `/docs`)."""),]=None,auto_error:Annotated[bool,Doc("""By default, if no HTTP Authorization header is provided, required forOpenID Connect authentication, it will automatically cancel the requestand send the client an error.If `auto_error` is set to `False`, when the HTTP Authorization headeris not available, instead of erroring out, the dependency result willbe `None`.This is useful when you want to have optional authentication.It is also useful when you want to have authentication that can beprovided in one of multiple optional ways (for example, with OpenIDConnect or in a cookie)."""),]=True,):self.model=OpenIdConnectModel(openIdConnectUrl=openIdConnectUrl,description=description)self.scheme_name=scheme_nameorself.__class__.__name__self.auto_error=auto_error |
| --- | --- |

### modelinstance-attribute¶

```
model = OpenIdConnect(
    openIdConnectUrl=openIdConnectUrl,
    description=description,
)
```

### scheme_nameinstance-attribute¶

```
scheme_name = scheme_name or __name__
```

### auto_errorinstance-attribute¶

```
auto_error = auto_error
```

### make_not_authenticated_error¶

```
make_not_authenticated_error()
```

   Source code in `fastapi/security/open_id_connect_url.py`

| 808182838485 | defmake_not_authenticated_error(self)->HTTPException:returnHTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Not authenticated",headers={"WWW-Authenticate":"Bearer"},) |
| --- | --- |
